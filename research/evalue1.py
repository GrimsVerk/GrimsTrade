"""evalue-forward-1: anytime-valid sequential tests for the forward record (card:
research/cards/evalue-forward-1.md).

    uv run --with numpy python research/evalue1.py > research/results/evalue-forward-1.md

Simulation only. Reads only the committed weekly returns store (`research/register/returns/`,
train only, cut at 2025-11-09). No backtest, no price bar, no network. Deterministic (fixed
seeds). Prints markdown.

E1: one-sided betting e-process with the ONS betting fraction on the clipped difference
(Waudby-Smith and Ramdas 2024; Shekhar and Ramdas 2023; Cutkosky and Orabona 2018).
E2: one-sided half-normal mixture of the self-normalised supermartingale
exp(lambda S - lambda^2 V / 2) (Robbins 1970; de la Pena 1999).
F: fixed-horizon one-sided t-test read once. P: the same t-test looked at every week.
"""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from statistics import NormalDist

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "research"))

Z = NormalDist()
Z80 = Z.inv_cdf(0.80)
BAR_Z = 4.70  # BAR.md at N = 504
ALPHAS = (("0.025 (registry, per rule)", 0.025), ("0.05 (z 1.645)", 0.05))
ALPHAS += ((f"{1 - Z.cdf(BAR_Z):.1e} (the bar, z 4.70)", 1 - Z.cdf(BAR_Z)),)
CLIP = 5.0  # E1 clips the difference at 5 train sds
TAU = 0.05  # E2 mixture scale, per-week signal-to-noise
ONS_C = 2 / (2 - math.log(3))
LAM_MAX = 0.5
BLOCK = 52
YEARS = 100
WEEKS = 52 * YEARS
SEED = 20261125
LAST = date(2025, 11, 10)  # nothing on or after this day is read
MIN_OVERLAP = 20 * 52
RHO_BAND = (0.77, 0.95)
RHOS = (0.77, 0.88, 0.95)
EDGES = (0.0, 0.05, 0.10, 0.30)
SHARPES = (0.0, 0.5, 1.0)
N_NULL = 10_000
N_ALT = 2_000
BATCH = 1_000
CHECK_YEARS = (5, 10, 20, 50, 100)


# --- the e-processes (pure functions; tests/test_evalue1.py checks them) ---


def phi_pos(x: np.ndarray) -> np.ndarray:
    """Standard normal cdf for x >= 0 (Abramowitz and Stegun 7.1.26, |error| < 1.5e-7)."""
    u = x / math.sqrt(2)
    t = 1 / (1 + 0.3275911 * u)
    poly = t * (
        0.254829592 + t * (-0.284496736 + t * (1.421413741 + t * (-1.453152027 + t * 1.061405429)))
    )
    erf = 1 - poly * np.exp(-(u**2))
    return np.asarray(0.5 * (1 + erf))


def mixture_log_e(s: np.ndarray, v: np.ndarray, tau: float = TAU) -> np.ndarray:
    """log E2: half-normal(0, tau^2) mixture over lambda >= 0 of exp(lambda s - lambda^2 v / 2).
    For s <= 0 every integrand is <= 1, so E2 <= 1; returned as min(formula, 0) there is not
    needed for crossing, but the formula is exact for all s."""
    a = 1 + tau**2 * v
    arg = tau * s / np.sqrt(a)
    pos = arg >= 0
    phi = np.where(pos, phi_pos(np.abs(arg)), 1 - phi_pos(np.abs(arg)))
    with np.errstate(divide="ignore"):
        log_phi = np.log(np.maximum(phi, 1e-300))
    return np.asarray(math.log(2) - 0.5 * np.log(a) + tau**2 * s**2 / (2 * a) + log_phi)


def ons_log_wealth(y: np.ndarray, thresholds: tuple[float, ...]) -> tuple[np.ndarray, np.ndarray]:
    """E1 on y (paths x weeks, values in [-1, 1]). Returns the first week (1-based, inf if never)
    at which log wealth reaches each log threshold (paths x thresholds), and the running maximum
    of log wealth per path."""
    n, t_max = y.shape
    lam = np.zeros(n)
    a = np.ones(n)
    logk = np.zeros(n)
    best = np.zeros(n)
    first = np.full((n, len(thresholds)), np.inf)
    th = np.array(thresholds)
    for t in range(t_max):
        yt = y[:, t]
        logk += np.log1p(lam * yt)
        g = yt / (1 + lam * yt)
        a += g * g
        lam = np.clip(lam + ONS_C * g / a, 0.0, LAM_MAX)
        np.maximum(best, logk, out=best)
        hit = (logk[:, None] >= th[None, :]) & np.isinf(first)
        if hit.any():
            first[hit] = t + 1
    return first, best


def first_cross(log_e: np.ndarray, thresholds: tuple[float, ...]) -> np.ndarray:
    """First week (1-based, inf if never) at which each row of log_e reaches each threshold."""
    out = np.full((log_e.shape[0], len(thresholds)), np.inf)
    for j, th in enumerate(thresholds):
        hit = log_e >= th
        any_hit = hit.any(axis=1)
        out[any_hit, j] = hit[any_hit].argmax(axis=1) + 1
    return out


def t_stats(x: np.ndarray) -> np.ndarray:
    """One-sample t-statistic of the mean after each week (nan for the first week)."""
    n = np.arange(1, x.shape[1] + 1, dtype=float)
    s = np.cumsum(x, axis=1)
    v = np.cumsum(x * x, axis=1)
    with np.errstate(divide="ignore", invalid="ignore"):
        var = (v - s * s / n) / (n - 1)
        return np.asarray(s / n / np.sqrt(var / n))


# --- the paths ---


@dataclass
class Pair:
    """Standardised tsmom12 (b) and a donor's standardised residual on it (e), week-paired."""

    name: str
    b: np.ndarray
    e: np.ndarray


def block_index(
    rng: np.random.Generator, length: int, n: int, weeks: int, block: int = BLOCK
) -> np.ndarray:
    nb = -(-weeks // block)
    starts = rng.integers(0, length, size=(n, nb))
    idx = (starts[:, :, None] + np.arange(block)[None, None, :]).reshape(n, -1)[:, :weeks]
    return np.asarray(idx % length)


def donors() -> tuple[np.ndarray, list[Pair], dict[str, float]]:
    """The primary tsmom12 series (standardised) and the donor pairs the card names."""
    from powermap1 import align, klass, load

    from grimstrade import returnstore as rs

    series = load(rs.read(ROOT / rs.STORE))
    by = {(s.idea, s.variant): s for s in series}
    primary = by[("baselines", "tsmom12")]
    b_all = primary.r[np.isfinite(primary.r)]
    b_std = (b_all - b_all.mean()) / b_all.std(ddof=0)
    pairs: list[Pair] = []
    info = {"stored": float(len(series)), "c1": 0.0}
    for s in series:
        if s is primary or klass(s.idea, s.variant) != "C1 slow trend / allocation":
            continue
        info["c1"] += 1
        x, y = align(s, primary)
        if len(x) < MIN_OVERLAP or x.std() == 0:
            continue
        rho = float(np.corrcoef(x, y)[0, 1])
        if not RHO_BAND[0] <= rho <= RHO_BAND[1]:
            continue
        beta = np.polyfit(y, x, 1)
        e = x - np.polyval(beta, y)
        yb = (y - y.mean()) / y.std(ddof=0)
        eb = e - e.mean()
        eb = eb - (eb @ yb) / (yb @ yb) * yb  # exactly orthogonal on the overlap
        pairs.append(Pair(f"{s.idea}/{s.variant}", yb, eb / eb.std(ddof=0)))
    return b_std, pairs, info


def diff_paths(
    rng: np.random.Generator,
    pairs: list[Pair] | None,
    rho: float,
    d: float,
    n: int,
    block: int = BLOCK,
) -> np.ndarray:
    """X_t (paths x weeks), the difference in train sds; pairs None = iid normal control."""
    mean = d / (math.sqrt(52) * math.sqrt(2 * (1 - rho)))
    if pairs is None:
        return np.asarray(rng.standard_normal((n, WEEKS)) + mean)
    pick = rng.integers(0, len(pairs), size=n)
    x = np.empty((n, WEEKS))
    for k in np.unique(pick):
        rows = np.flatnonzero(pick == k)
        p = pairs[int(k)]
        idx = block_index(rng, len(p.b), len(rows), WEEKS, block)
        x[rows] = ((rho - 1) * p.b[idx] + math.sqrt(1 - rho**2) * p.e[idx]) / math.sqrt(
            2 * (1 - rho)
        )
    return x + mean


def own_paths(
    rng: np.random.Generator, b: np.ndarray | None, sr: float, n: int, block: int = BLOCK
) -> np.ndarray:
    """X_t for a book against zero: resampled standardised tsmom12 (or normal) plus S / sqrt(52)."""
    mean = sr / math.sqrt(52)
    if b is None:
        return np.asarray(rng.standard_normal((n, WEEKS)) + mean)
    return np.asarray(b[block_index(rng, len(b), n, WEEKS, block)] + mean)


# --- one cell ---


@dataclass
class Cell:
    n: int
    e1: np.ndarray  # first crossing week, paths x alphas
    e2: np.ndarray
    peek: np.ndarray
    fixed_power: np.ndarray  # years 1..100 x alphas: share with t > z at that horizon
    e1_max: float
    e2_max: float


def run_cell(make: object, n: int, seed: tuple[int, ...]) -> Cell:
    rng = np.random.default_rng(list(seed))
    logs = tuple(math.log(1 / a) for _, a in ALPHAS)
    zs = np.array([Z.inv_cdf(1 - a) for _, a in ALPHAS])
    e1s, e2s, pks, fixed = [], [], [], np.zeros((YEARS, len(ALPHAS)))
    m1 = m2 = -math.inf
    for start in range(0, n, BATCH):
        m = min(BATCH, n - start)
        x = make(rng, m)  # type: ignore[operator]
        f1, best1 = ons_log_wealth(np.clip(x / CLIP, -1, 1), logs)
        le2 = mixture_log_e(np.cumsum(x, axis=1), np.cumsum(x * x, axis=1))
        f2 = first_cross(le2, logs)
        t = t_stats(x)
        t[:, :1] = -np.inf
        fp = np.full((m, len(ALPHAS)), np.inf)
        for j, z in enumerate(zs):
            hit = t >= z
            ok = hit.any(axis=1)
            fp[ok, j] = hit[ok].argmax(axis=1) + 1
        at = t[:, 52 * np.arange(1, YEARS + 1) - 1]
        fixed += (at[:, :, None] >= zs[None, None, :]).sum(axis=0)
        e1s.append(f1)
        e2s.append(f2)
        pks.append(fp)
        m1 = max(m1, float(best1.max()))
        m2 = max(m2, float(le2.max()))
    return Cell(n, np.vstack(e1s), np.vstack(e2s), np.vstack(pks), fixed / n, m1, m2)


# --- printing ---


def by_year(first: np.ndarray, j: int, y: int) -> float:
    return float((first[:, j] <= 52 * y).mean())


def quantile_years(first: np.ndarray, j: int, q: float) -> str:
    v = np.sort(first[:, j])
    k = v[int(math.ceil(q * len(v))) - 1]
    return f"{k / 52:.1f}" if np.isfinite(k) else f">{YEARS}"


def fixed_80(cell: Cell, j: int) -> str:
    ok = np.flatnonzero(cell.fixed_power[:, j] >= 0.8)
    return f"{ok[0] + 1}" if len(ok) else f">{YEARS}"


def formula_years(z: float, snr_annual: float) -> str:
    y = ((z + Z80) / snr_annual) ** 2
    return f"{y:,.0f}" if y >= 10 else f"{y:.1f}"


def upper95(k: int, n: int) -> float:
    """Clopper-Pearson one-sided 97.5% upper bound on a binomial rate (bisection)."""

    def cdf(p: float) -> float:
        if p >= 1:
            return 0.0
        return sum(
            math.exp(
                math.lgamma(n + 1)
                - math.lgamma(i + 1)
                - math.lgamma(n - i + 1)
                + i * math.log(p)
                + (n - i) * math.log1p(-p)
            )
            for i in range(k + 1)
        )

    lo, hi = k / n, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if cdf(mid) > 0.025:
            lo = mid
        else:
            hi = mid
    return hi


def alt_rows(label: str, cell: Cell, snr: float, j: int) -> list[str]:
    z = Z.inv_cdf(1 - ALPHAS[j][1])
    rows = []
    for name, first in (("E1 betting (ONS)", cell.e1), ("E2 mixture", cell.e2)):
        cells = " | ".join(f"{by_year(first, j, y):.2f}" for y in CHECK_YEARS)
        rows.append(
            f"| {label} | {name} | {cells} | {quantile_years(first, j, 0.5)} "
            f"| {quantile_years(first, j, 0.8)} | {fixed_80(cell, j)} | {formula_years(z, snr)} |"
        )
    cells = " | ".join(f"{cell.fixed_power[y - 1, j]:.2f}" for y in CHECK_YEARS)
    rows.append(
        f"| {label} | F fixed horizon (power at Y) | {cells} | - | - "
        f"| {fixed_80(cell, j)} | {formula_years(z, snr)} |"
    )
    return rows


HEAD = (
    "| Scenario | Test | by 5 y | 10 y | 20 y | 50 y | 100 y | median years | 80% years "
    "| F 80% years (sim) | Fixed 80% years (formula) |\n"
    "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"
)


def null_rows(label: str, cell: Cell) -> list[str]:
    out = []
    for name, first in (
        ("E1 betting (ONS)", cell.e1),
        ("E2 mixture", cell.e2),
        ("P peeking t-test", cell.peek),
    ):
        cells = []
        for j in range(len(ALPHAS)):
            k = int(np.isfinite(first[:, j]).sum())
            cells.append(f"{k / cell.n:.4f} (<= {upper95(k, cell.n):.4f})")
        out.append(f"| {label} | {name} | " + " | ".join(cells) + " |")
    cells = [
        f"{cell.fixed_power[9, j]:.4f} / {cell.fixed_power[99, j]:.4f}" for j in range(len(ALPHAS))
    ]
    out.append(f"| {label} | F fixed, read once at 10 y / 100 y | " + " | ".join(cells) + " |")
    return out


def main() -> None:
    b, pairs, info = donors()
    lines = [
        "# evalue-forward-1: results",
        "",
        "Generated by `uv run --with numpy python research/evalue1.py` "
        "(card `research/cards/evalue-forward-1.md`). Paths of 100 years of weekly differences; "
        f"seed {SEED}. Store: {info['stored']:.0f} series, {info['c1']:.0f} of class C1; "
        f"**{len(pairs)} donors** (C1, >= 20 years of overlap with `baselines/tsmom12`, rho in "
        f"[{RHO_BAND[0]}, {RHO_BAND[1]}]). Primary `tsmom12`: {len(b)} weeks to 2025-11-07.",
        "",
    ]
    donor_kurt = [float((p.e**4).mean() - 3) for p in pairs]
    b_kurt = float((b**4).mean() - 3)
    lines.append(
        f"Shape: `tsmom12` weekly excess kurtosis {b_kurt:.1f}, skew {float((b**3).mean()):+.2f}; "
        f"donor residuals' excess kurtosis median {float(np.median(donor_kurt)):.1f} "
        f"(range {min(donor_kurt):.1f} to {max(donor_kurt):.1f})."
    )
    lines.append("")
    thr = ", ".join(f"{name}: 1/alpha = {1 / a:,.0f}" for name, a in ALPHAS)
    lines += [f"Levels: {thr}.", ""]

    cells: dict[tuple[str, str, float, float], Cell] = {}
    idx = 0
    for scen, src in (("resampled", pairs), ("gaussian", None)):
        for rho in RHOS:
            for d in EDGES:
                idx += 1
                n = N_NULL if d == 0 else N_ALT

                def make(
                    rng: np.random.Generator,
                    m: int,
                    src: list[Pair] | None = src,
                    rho: float = rho,
                    d: float = d,
                ) -> np.ndarray:
                    return diff_paths(rng, src, rho, d, m)

                cells[(scen, "diff", rho, d)] = run_cell(make, n, (SEED, idx))
        for sr in SHARPES:
            idx += 1
            n = N_NULL if sr == 0 else N_ALT
            bsrc = b if scen == "resampled" else None

            def make_own(
                rng: np.random.Generator,
                m: int,
                bsrc: np.ndarray | None = bsrc,
                sr: float = sr,
            ) -> np.ndarray:
                return own_paths(rng, bsrc, sr, m)

            cells[(scen, "own", 0.0, sr)] = run_cell(make_own, n, (SEED, idx))

    lines += [
        "## 1. False rejections under the null (edge 0)",
        "",
        "Share of paths that ever reject within 100 years (Clopper-Pearson 97.5% upper bound), "
        f"{N_NULL:,} paths per cell. F: share with t > z read once at 10 / 100 years.",
        "",
        "| Scenario | Test | " + " | ".join(n for n, _ in ALPHAS) + " |",
        "|---|---|---:|---:|---:|",
    ]
    for scen in ("resampled", "gaussian"):
        for rho in RHOS:
            lines += null_rows(f"{scen}, vs tsmom12, rho {rho}", cells[(scen, "diff", rho, 0.0)])
        lines += null_rows(f"{scen}, own Sharpe vs 0", cells[(scen, "own", 0.0, 0.0)])
    lines += [
        "",
        "Largest log E over all null paths (the bar needs log(1/alpha) = "
        f"{math.log(1 / ALPHAS[2][1]):.2f}; alpha 0.025 needs {math.log(40):.2f}):",
        "",
        "| Scenario | E1 max log wealth | E2 max log E |",
        "|---|---:|---:|",
    ]
    for scen in ("resampled", "gaussian"):
        for rho in RHOS:
            c = cells[(scen, "diff", rho, 0.0)]
            lines.append(f"| {scen}, rho {rho} | {c.e1_max:.2f} | {c.e2_max:.2f} |")
        c = cells[(scen, "own", 0.0, 0.0)]
        lines.append(f"| {scen}, own Sharpe vs 0 | {c.e1_max:.2f} | {c.e2_max:.2f} |")

    for j, (aname, _) in enumerate(ALPHAS):
        lines += [
            "",
            f"## {j + 2}. Edges, alpha {aname}",
            "",
            "Share of paths rejected by year Y (sequential: ever crossed 1/alpha by Y; F: t > z "
            f"read once at Y), {N_ALT:,} paths per cell. Years: median and 80th percentile of the "
            "stopping time; F 80% years: first whole year with simulated power >= 0.8; formula: "
            "power-map-1's ((z + 0.84) sqrt(2 (1 - rho)) / d)^2 with k = 1.",
            "",
            HEAD,
        ]
        for scen in ("resampled", "gaussian"):
            for rho in RHOS:
                for d in EDGES[1:]:
                    snr = d / math.sqrt(2 * (1 - rho))
                    lines += alt_rows(
                        f"{scen}, rho {rho}, d +{d:.2f}", cells[(scen, "diff", rho, d)], snr, j
                    )
            for sr in SHARPES[1:]:
                lines += alt_rows(
                    f"{scen}, own Sharpe {sr} vs 0", cells[(scen, "own", 0.0, sr)], sr, j
                )
    lines += diagnostic(b, pairs)
    print("\n".join(lines))


def variance_ratio(x: np.ndarray, weeks: int = 52) -> float:
    """Variance of non-overlapping `weeks`-week sums over `weeks` times the weekly variance."""
    n = len(x) // weeks * weeks
    return float(x[:n].reshape(-1, weeks).sum(1).var() / weeks / x.var())


def diagnostic(b: np.ndarray, pairs: list[Pair]) -> list[str]:
    """Added after the first results (not in the card): is the null over-rejection fat tails or
    serial dependence? Same donors, blocks of 1 week (fat tails kept, dependence removed) against
    the card's 52 weeks, alpha 0.025, 4,000 paths, rho 0.88 and tsmom12 against zero."""
    rho = 0.88
    vr = [
        variance_ratio(((rho - 1) * p.b + math.sqrt(1 - rho**2) * p.e) / math.sqrt(2 * (1 - rho)))
        for p in pairs
    ]
    out = [
        "",
        "## 5. Diagnostic (added after the first results, not in the card)",
        "",
        "Why the resampled nulls over-reject: the 52-week variance ratio (variance of yearly "
        "sums / 52 weekly variances; 1 for a martingale difference) of the donors' difference "
        f"series at rho {rho}: median {float(np.median(vr)):.2f}, p10 "
        f"{float(np.percentile(vr, 10)):.2f}, p90 {float(np.percentile(vr, 90)):.2f}; of "
        f"`tsmom12` itself {variance_ratio(b):.2f} (31 yearly sums, rough). Rejection under the "
        "null at alpha 0.025 within 100 years, 4,000 paths:",
        "",
        "| Null | Block (weeks) | E1 | E2 | F read once at 10 y | F at 100 y |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for k, block in enumerate((1, 52)):

        def mk_d(rng: np.random.Generator, m: int, block: int = block) -> np.ndarray:
            return diff_paths(rng, pairs, rho, 0.0, m, block)

        def mk_o(rng: np.random.Generator, m: int, block: int = block) -> np.ndarray:
            return own_paths(rng, b, 0.0, m, block)

        for name, mk, tag in ((f"vs tsmom12, rho {rho}", mk_d, 1), ("own Sharpe vs 0", mk_o, 2)):
            c = run_cell(mk, 4000, (SEED, 900 + 10 * k + tag))
            out.append(
                f"| {name} | {block} | {float(np.isfinite(c.e1[:, 0]).mean()):.4f} "
                f"| {float(np.isfinite(c.e2[:, 0]).mean()):.4f} | {c.fixed_power[9, 0]:.4f} "
                f"| {c.fixed_power[99, 0]:.4f} |"
            )
    return out


if __name__ == "__main__":
    main()
