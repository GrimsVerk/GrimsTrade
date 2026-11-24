# ruff: noqa: E501
"""Run rl-6, step 1: power analysis for a slower funding carry (research/rl-6.md). Train period
only; the held-out year is never loaded.

    uv run python -I research/lib/rl6_power.py

No strategy number is computed for output: the script prints only the *noise* of carry-shaped
books (standard deviation, autocorrelation, number of independent periods), their mechanical
turnover, and the smallest mean edge that noise lets a test detect. Book means, Sharpes and
p-values are never printed or written (every series is demeaned before it is summarised).

Books (carry-2's third-against-third shape, 0.5 of equity a leg, ranked inside each venue,
pooled with equal capital per venue that week): `w1` = weekly on 7-day funding; `m4-f7`,
`m4-f28`, `m4-f56` = rebalanced every 4 weeks (four phase books, one week apart, averaged) on
7-, 28- and 56-day mean funding. Weights are held flat between rebalances (no drift): close
enough for a noise estimate.
"""

from __future__ import annotations

import sys
from math import sqrt
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from breadth_xs import roll_mean  # noqa: E402
from rl5_screen import pool, third_book  # noqa: E402

Z_10 = 1.2816  # one-sided p < 0.10 (the carry cards' bar)
Z_BONF = 2.2414  # one-sided p < 0.10 / 8: an 8th shape on this data (carry-2 two, carry-3 five)
Z_POW80 = 0.8416  # 80% power
STEP = 4
RESULTS = Path(__file__).resolve().parents[1] / "results"


# --- pure helpers ---


def phase_weights(sig: np.ndarray, m: np.ndarray, step: int, phase: int) -> np.ndarray:
    """[W, n] weights of one phase book: on weeks i with i % step == phase (and on the first week,
    so the book is never empty) the third book on `sig` among `m`; held flat in between."""
    w_n, n = sig.shape
    out = np.zeros((w_n, n))
    cur = np.zeros(n)
    for i in range(w_n):
        if i % step == phase or not cur.any():
            cur = third_book(sig[i], m[i])
        out[i] = cur
    return out


def book_weeks(weights: np.ndarray, fwd: np.ndarray) -> np.ndarray:
    """[W] the week's return of a weight path (NaN where the book is empty). A held coin with
    no return that week counts as 0."""
    r = (weights * np.nan_to_num(np.expm1(fwd))).sum(1)
    r[~np.any(weights != 0, axis=1)] = np.nan
    return r


def turnover_per_year(weights: np.ndarray) -> float:
    """Sum of absolute weight changes a year (the first week's build-up excluded)."""
    if len(weights) < 2:
        return 0.0
    return float(np.abs(np.diff(weights, axis=0)).sum(1).mean() * 52)


def noise(x: np.ndarray, block: int = STEP) -> dict[str, float]:
    """Noise of a weekly series, its mean removed first: sd, lag-1..3 autocorrelation, and the
    sd of non-overlapping `block`-week sums (a rough long-run sd that covers autocorrelation)."""
    x = x[np.isfinite(x)]
    d = x - x.mean()
    sd = float(d.std(ddof=1))
    ac = [float((d[k:] * d[:-k]).sum() / (d * d).sum()) for k in (1, 2, 3)]
    nb = len(d) // block
    sums = d[: nb * block].reshape(nb, block).sum(1)
    return {
        "weeks": float(len(d)),
        "sd": sd,
        "ac1": ac[0],
        "ac2": ac[1],
        "ac3": ac[2],
        "blocks": float(nb),
        "sd_block": float(sums.std(ddof=1)),
        "sd_eff": float(max(sd, sums.std(ddof=1) / sqrt(block))),
    }


def mde(sd_week: float, weeks: float, z_alpha: float, z_power: float = Z_POW80) -> float:
    """Smallest true mean weekly edge detected with the given one-sided level and power:
    (z_alpha + z_power) x sd / sqrt(weeks)."""
    return (z_alpha + z_power) * sd_week / sqrt(weeks)


def years_needed(sharpe: float, z_alpha: float, z_power: float = Z_POW80) -> float:
    """Years of data for a true annual Sharpe to be detected: ((z_a + z_b) / Sharpe)^2."""
    return ((z_alpha + z_power) / sharpe) ** 2


# --- data and report ---


def load() -> dict[str, dict[str, Any]]:
    import carry2
    import rl4_perp

    files = {"B-out": "binance", "Bybit": "bybit", "Hyperliquid": "hyperliquid"}
    out: dict[str, dict[str, Any]] = {}
    for lab, (v, r) in rl4_perp.load().items():
        z = np.load(carry2.derived() / f"{files[lab]}.npz")
        col = {str(s): j for j, s in enumerate(z["names"])}
        fsig = z["fsig"][:, [col[s] for s in v.names]]
        with np.errstate(invalid="ignore", divide="ignore"):
            sigs = {h: -roll_mean(fsig, h, 0.5)[r.day] for h in (7, 28, 56)}
        out[lab] = {"day": r.day, "m": r.m, "fwd": r.fwd, "sig": sigs}
    return out


def books(sets: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Per book: pooled weekly series (for its noise only) and mean venue turnover a year."""
    res: dict[str, dict[str, Any]] = {}
    shapes = {"w1": (7, 1), "m4-f7": (7, STEP), "m4-f28": (28, STEP), "m4-f56": (56, STEP)}
    for name, (h, step) in shapes.items():
        days, series, turns = [], [], []
        for s in sets.values():
            ws = [phase_weights(s["sig"][h], s["m"], step, p) for p in range(step)]
            r = np.nanmean(np.stack([book_weeks(w, s["fwd"]) for w in ws]), axis=0)
            turns.append(np.mean([turnover_per_year(w) for w in ws]))
            days.append(s["day"])
            series.append(r)
        d, x = pool(days, series)
        res[name] = {"day": d, "x": x, "turnover": float(np.mean(turns))}
    return res


def write(res: dict[str, dict[str, Any]]) -> Path:
    base = res["w1"]
    L = [
        "# RL 6: noise and power of carry-shaped books (train only, no means)",
        "",
        "Script `lib/rl6_power.py`, run once (`research/rl-6.md`). Pooled weekly returns of",
        "third-against-third funding books (0.5 a leg, equal capital per venue), gross of costs, mean",
        "removed before every number. MDE = smallest true mean edge detected with 80% power:",
        "(z_alpha + 0.84) x sd_eff / sqrt(weeks); sd_eff = max(weekly sd, sd of 4-week sums / 2).",
        f"z_alpha: {Z_10} (one-sided p < 0.10) and {Z_BONF} (p < 0.10 / 8, an 8th shape on this data).",
        "",
        "| Book | Weeks | Weekly sd | ac1 / ac2 / ac3 | 4-week sums (sd) | Turnover/yr | MDE/week at 0.10 | MDE/week at 0.10/8 | MDE/yr at 0.10/8 | MDE Sharpe at 0.10/8 |",
        "|---|---:|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name, b in res.items():
        nz = noise(b["x"])
        m10 = mde(nz["sd_eff"], nz["weeks"], Z_10)
        mb = mde(nz["sd_eff"], nz["weeks"], Z_BONF)
        L.append(
            f"| `{name}` | {nz['weeks']:.0f} | {nz['sd']:.2%} | {nz['ac1']:+.2f} / {nz['ac2']:+.2f} / {nz['ac3']:+.2f} "
            f"| {nz['blocks']:.0f} ({nz['sd_block']:.2%}) | {b['turnover']:.0f}x | {m10:.2%} | {mb:.2%} "
            f"| {mb * 52:.1%} | {mb / nz['sd_eff'] * sqrt(52):.2f} |"
        )
    L += [
        "",
        "Paired difference to `w1` (same weeks): the sd of slow minus weekly, and the smallest gap",
        "in mean weekly return a paired test detects (80% power). Next to it, the cost a slower book",
        "saves for certain: (turnover of `w1` - turnover of the slow book) x cost a side, per week.",
        "",
        "| Slow book | Weeks | sd_eff of difference | Gap MDE/week at 0.10 | at 0.10/8 | Cost saved/week at 8 bps | at 10 bps | at 30 bps |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, b in res.items():
        if name == "w1":
            continue
        common, ia, ib = np.intersect1d(base["day"], b["day"], return_indices=True)
        diff = b["x"][ib] - base["x"][ia]
        nz = noise(diff)
        saved = (base["turnover"] - b["turnover"]) / 52
        L.append(
            f"| `{name}` | {len(common)} | {nz['sd_eff']:.2%} | {mde(nz['sd_eff'], nz['weeks'], Z_10):.2%} "
            f"| {mde(nz['sd_eff'], nz['weeks'], Z_BONF):.2%} | {saved * 0.0008:.3%} | {saved * 0.001:.3%} | {saved * 0.003:.3%} |"
        )
    L += [
        "",
        "Years of data needed to detect a true annual Sharpe (80% power, `years_needed`):",
        "",
        "| True Sharpe | at p < 0.10 | at p < 0.10 / 8 |",
        "|---:|---:|---:|",
    ]
    for s in (0.3, 0.5, 0.79, 1.0):
        L.append(f"| {s:.2f} | {years_needed(s, Z_10):.1f} | {years_needed(s, Z_BONF):.1f} |")
    path = RESULTS / "rl-6-power.md"
    path.write_text("\n".join(L) + "\n")
    return path


def main() -> None:
    print(write(books(load())).read_text())


if __name__ == "__main__":
    main()
