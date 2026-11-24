"""turbulence-1: financial turbulence vs a matched volatility trigger as a crash overlay on
`tsmom12` (card `research/cards/turbulence.md`, written and pushed before any number).

    uv run --with numpy python research/lib/turbulence1.py

Signal on the panel's business-day grid (row i = closes visible at that day's decision):
d_i = Mahalanobis distance of today's return vector from the mean of the 252 rows before it,
under their covariance shrunk a tenth toward its diagonal, divided by the number of assets;
m_i = the same with correlations set to zero (magnitude surprise, a plain volatility measure);
T, M = 5-row means; C = T / M (correlation surprise, Kinlaw and Turkington 2014). A trigger is
on when the value exceeds the p-th percentile of its own previous 756 rows (at least 252 of
them). The overlay sends `tsmom12`'s risk slots to cash on any day the trigger is on.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import common as c
import harness
import numpy as np
import stats
from harness import Panel, Run

IDEA = "turbulence"
RISK_SIX = ("SPY", "QQQ", "BTC", "ETH")
RISK_IDX = ("GSPC", "N225", "FTSE", "GDAXI")
SHRINK = 0.1
# Fast crashes (card): peak-to-trough of the S&P 500 index close inside these windows.
FAST: list[tuple[str, date, date]] = [
    ("1987", date(1987, 8, 1), date(1987, 12, 31)),
    ("1998", date(1998, 7, 1), date(1998, 10, 31)),
    ("2011", date(2011, 4, 1), date(2011, 12, 31)),
    ("2015", date(2015, 7, 1), date(2015, 10, 31)),
    ("2018-Q4", date(2018, 9, 1), date(2018, 12, 31)),
    ("2020", date(2020, 2, 1), date(2020, 4, 30)),
]
REBOUND_DAYS = 91


@dataclass(frozen=True)
class Spec:
    """One trigger: which series (`T`, `M` or `C`), its percentile and the window lengths."""

    sig: str
    p: float
    window: int = 252
    smooth: int = 5
    hist: int = 756
    min_hist: int = 252


def signals(grid: np.ndarray, window: int = 252, smooth: int = 5) -> dict[str, np.ndarray]:
    """d, m, T, M, C and n per grid row; row i uses grid rows <= i only."""
    rows, k = grid.shape
    r = np.full((rows, k), np.nan)
    with np.errstate(invalid="ignore", divide="ignore"):
        r[1:] = np.diff(np.log(grid), axis=0)
    d = np.full(rows, np.nan)
    m = np.full(rows, np.nan)
    n = np.zeros(rows, dtype=int)
    for i in range(window, rows):
        block = r[i - window : i + 1]
        cols = np.flatnonzero(~np.isnan(block).any(axis=0))
        if len(cols) == 0:
            continue
        x = block[:-1][:, cols]
        mu = x.mean(axis=0)
        cov = np.atleast_2d(np.cov(x, rowvar=False))
        var = np.diag(cov)
        if (var <= 0).any():
            continue
        cov_s = (1 - SHRINK) * cov + SHRINK * np.diag(var)
        e = block[-1, cols] - mu
        d[i] = float(e @ np.linalg.solve(cov_s, e)) / len(cols)
        m[i] = float((e * e / var).sum()) / len(cols)
        n[i] = len(cols)
    tt = np.full(rows, np.nan)
    mm = np.full(rows, np.nan)
    cc = np.full(rows, np.nan)
    for i in range(smooth - 1, rows):
        a, b = d[i - smooth + 1 : i + 1], m[i - smooth + 1 : i + 1]
        if np.isnan(a).any():
            continue
        tt[i], mm[i] = a.mean(), b.mean()
        if (n[i - smooth + 1 : i + 1] >= 2).all() and mm[i] > 0:
            cc[i] = tt[i] / mm[i]
    return {"d": d, "m": m, "T": tt, "M": mm, "C": cc, "n": n.astype(float)}


def trigger(x: np.ndarray, p: float, hist: int = 756, min_hist: int = 252) -> np.ndarray:
    """x_i above the p-th percentile of its previous `hist` rows (the current row excluded)."""
    on = np.zeros(len(x), dtype=bool)
    for i in range(len(x)):
        if np.isnan(x[i]):
            continue
        past = x[max(0, i - hist) : i]
        past = past[~np.isnan(past)]
        if len(past) >= min_hist:
            on[i] = x[i] > np.percentile(past, p)
    return on


def on_array(panel: Panel, spec: Spec) -> np.ndarray:
    key = ("turbulence1", spec)
    if key not in panel.cache:
        skey = ("turbulence1-signals", spec.window, spec.smooth)
        if skey not in panel.cache:
            panel.cache[skey] = signals(panel.grid, spec.window, spec.smooth)
        sig: dict[str, np.ndarray] = panel.cache[skey]  # type: ignore[assignment]
        panel.cache[key] = trigger(sig[spec.sig], spec.p, spec.hist, spec.min_hist)
    out: np.ndarray = panel.cache[key]  # type: ignore[assignment]
    return out


def overlay(base: c.ResearchStrategy, spec: Spec, risk: Sequence[str]) -> c.ResearchStrategy:
    """`base`'s weights, with the risk slots dropped to cash on days the trigger is on."""

    def f(view: c.View) -> c.Weights:
        w = base(view)
        row = view.n_grid - 1
        if row >= 0 and on_array(view.panel, spec)[row]:
            return {s: x for s, x in w.items() if s not in risk}
        return w

    return f


def tsmom12() -> c.ResearchStrategy:
    return c.weekly(c.slots(c.tsmom_signal))


def window_rows(panel: Panel, a: date, b: date) -> np.ndarray:
    g = panel.grid_dates
    return np.array([i for i, d in enumerate(g) if a <= d <= b], dtype=int)


def share_on(panel: Panel, spec: Spec, rows: np.ndarray) -> float:
    return float(on_array(panel, spec)[rows].mean())


def matched(panel: Panel, sig: str, target: float, rows: np.ndarray) -> Spec:
    """The percentile at which `sig`'s trigger is on on `target` share of the window's rows
    (a calibration on the whole window: a control, not a rule anyone could run)."""
    lo, hi = 50.0, 99.9
    for _ in range(30):
        mid = (lo + hi) / 2
        if share_on(panel, Spec(sig, mid), rows) > target:
            lo = mid
        else:
            hi = mid
    best = min((lo, hi), key=lambda q: abs(share_on(panel, Spec(sig, q), rows) - target))
    return Spec(sig, round(best, 3))


def boot(a: np.ndarray, b: np.ndarray, draws: int = 2000) -> tuple[float, float, float]:
    """Sharpe(a) - Sharpe(b), one-sided bootstrap p, z = difference / bootstrap SD."""
    rng = np.random.default_rng(0)
    diffs = np.empty(draws)
    for k in range(draws):
        i = stats._stationary_indices(len(a), 20, rng)
        diffs[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
    diff = stats.sharpe(a) - stats.sharpe(b)
    sd = float(diffs.std())
    return diff, float((diffs <= 0).mean()), diff / sd if sd > 0 else math.nan


def episodes(gspc: Sequence[harness.Bar]) -> list[tuple[str, date, date]]:
    out = []
    for name, a, b in FAST:
        bars = [x for x in gspc if a <= x.date <= b]
        trough = min(bars, key=lambda x: x.close)
        peak = max((x for x in bars if x.date < trough.date), key=lambda x: x.close)
        out.append((name, peak.date, trough.date))
    return out


def eq_at(run: Run, d: date) -> float:
    k = (d - run.days[0]).days
    return float(run.equity[k]) if 0 <= k < len(run.days) else math.nan


def crash_rows(runs: Sequence[Run], eps: list[tuple[str, date, date]]) -> list[str]:
    head = "| Rule |" + "".join(f" {n} fall / rebound |" for n, _, _ in eps)
    lines = [head, "|---|" + "---:|" * len(eps)]
    for run in runs:
        row = f"| {run.variant} |"
        for _, pk, tr in eps:
            e0, e1 = eq_at(run, pk), eq_at(run, tr)
            e2 = eq_at(run, tr + timedelta(days=REBOUND_DAYS))
            if math.isnan(e0) or math.isnan(e2) or run.days[0] > pk - timedelta(days=30):
                row += " - |"
            else:
                row += f" {e1 / e0 - 1:+.1%} / {e2 / e1 - 1:+.1%} |"
        lines.append(row)
    return lines


def crash_values(run: Run, eps: list[tuple[str, date, date]]) -> dict[str, tuple[float, float]]:
    out = {}
    for name, pk, tr in eps:
        e0, e1 = eq_at(run, pk), eq_at(run, tr)
        e2 = eq_at(run, tr + timedelta(days=REBOUND_DAYS))
        if not (math.isnan(e0) or math.isnan(e2) or run.days[0] > pk - timedelta(days=30)):
            out[name] = (e1 / e0 - 1, e2 / e0 - 1)
    return out


def fires(panel: Panel, spec: Spec, eps: list[tuple[str, date, date]]) -> str:
    """Per episode: first grid day on or after the peak with the trigger on (business days
    after the peak, '-' if none before the trough) and the share of peak..trough days on."""
    on = on_array(panel, spec)
    g = panel.grid_dates
    out = []
    for name, pk, tr in eps:
        rows = [i for i, d in enumerate(g) if pk <= d <= tr]
        if not rows or g[0] > pk - timedelta(days=400):
            continue
        hit = [k for k, i in enumerate(rows) if on[i]]
        first = str(hit[0]) if hit else "-"
        out.append(f"{name} {first} ({len(hit) / len(rows):.0%})")
    return ", ".join(out)


def cut_share(run: Run, base: Run) -> float:
    """Share of decision days on which the overlay held less than `tsmom12`."""
    n = sum(
        sum(a.weights.values()) < sum(b.weights.values()) - 1e-9
        for a, b in zip(run.decisions, base.decisions, strict=True)
    )
    return n / len(run.decisions)


def universe(
    name: str, risk: Sequence[str], primary: bool, out: list[str], eps: list[tuple[str, date, date]]
) -> dict[str, Run]:
    u = c.ctx(name)
    rows = window_rows(u.panel, u.start, u.end)
    kv = "variant" if primary else "robustness"
    base = tsmom12()
    sig = signals(u.panel.grid)
    u.panel.cache[("turbulence1-signals", 252, 5)] = sig
    turb, corr = Spec("T", 90), Spec("C", 90)
    s_t, s_c = share_on(u.panel, turb, rows), share_on(u.panel, corr, rows)
    specs: list[tuple[str, Spec, str]] = [
        ("turb", turb, kv),
        ("corr", corr, kv),
        ("mag", Spec("M", 90), "baseline"),
        ("mag-match", matched(u.panel, "M", s_t, rows), "baseline"),
        ("mag-match-c", matched(u.panel, "M", s_c, rows), "baseline"),
    ]
    if primary:
        t75 = Spec("T", 75)
        specs += [
            ("turb-q75", t75, "robustness"),
            ("mag-match-q75", matched(u.panel, "M", share_on(u.panel, t75, rows), rows),
             "baseline"),
        ]  # fmt: skip
    runs: dict[str, Run] = {
        "tsmom12": c.go("baselines", "tsmom12", base, u, "baseline", log=False),
        "equal-weight": c.go(
            "baselines", "equal-weight", c.weekly(c.equal_weight), u, "baseline", log=False
        ),
    }
    for nm, spec, kind in specs:
        runs[nm] = c.go(IDEA, nm, overlay(base, spec, risk), u, kind)

    ok = ~np.isnan(sig["T"]) & ~np.isnan(sig["M"]) & ~np.isnan(sig["C"])
    lt, lm, lc = (np.log(sig[k][ok]) for k in ("T", "M", "C"))
    title = "six assets (primary)" if primary else f"out of universe: `{name}`"
    out += [f"## {title}, {u.start}..{u.end}", ""]
    nn = sig["n"][rows]
    out += [
        f"Assets in the signal on the test's days: 1 on {(nn == 1).mean():.0%}, 2-3 on "
        f"{((nn >= 2) & (nn <= 3)).mean():.0%}, 4+ on {(nn >= 4).mean():.0%} (0 on "
        f"{(nn == 0).mean():.0%}). Correlation of log T, log M, log C: T-M "
        f"{np.corrcoef(lt, lm)[0, 1]:.2f}, T-C {np.corrcoef(lt, lc)[0, 1]:.2f}, M-C "
        f"{np.corrcoef(lm, lc)[0, 1]:.2f}.",
        "",
        "| Rule | Signal, percentile | Trigger on (share of days) | Cuts `tsmom12` (share) |",
        "|---|---|---:|---:|",
    ]
    for nm, spec, _ in specs:
        out.append(
            f"| {nm} | {spec.sig}, {spec.p:g} | {share_on(u.panel, spec, rows):.1%} | "
            f"{cut_share(runs[nm], runs['tsmom12']):.1%} |"
        )
    order = [nm for nm, _, _ in specs] + ["tsmom12", "equal-weight"]
    out += ["", c.table([runs[k] for k in order], versus=runs["tsmom12"]), ""]
    out += ["Paired comparisons (stationary bootstrap, block 20, 2,000 draws, seed 0):", ""]
    out += ["| Pair | dSharpe | p (one-sided) | z |", "|---|---:|---:|---:|"]
    pairs = [
        ("turb", "mag-match"), ("corr", "mag-match-c"), ("turb", "mag"), ("turb", "tsmom12"),
        ("corr", "tsmom12"), ("mag-match", "tsmom12"), ("mag", "tsmom12"),
    ]  # fmt: skip
    if primary:
        pairs += [("turb-q75", "mag-match-q75"), ("turb-q75", "tsmom12")]
    for a_, b_ in pairs:
        x, y = c.align(runs[a_], runs[b_])
        dd, p, z = boot(x, y)
        out.append(f"| {a_} - {b_} | {dd:+.3f} | {p:.2f} | {z:+.2f} |")
    out += ["", "Slow stress windows (total return inside each):", ""]
    out += [c.stress_table([runs[k] for k in order]), ""]
    out += [f"Fast crashes (S&P 500 index peak -> trough, then {REBOUND_DAYS} days):", ""]
    out += crash_rows([runs[k] for k in order], eps)
    out += ["", "First day the trigger is on after the peak (business days; share of the fall on):"]
    out += [""] + [f"- {nm}: {fires(u.panel, spec, eps)}" for nm, spec, _ in specs] + [""]
    return runs


def bar_lines(six: dict[str, Run], idx: dict[str, Run]) -> list[str]:
    out = ["## Pass bar (card)", ""]
    for v, twin in [("turb", "mag-match"), ("corr", "mag-match-c")]:
        a, b = c.align(six[v], six[twin])
        dd, p, _ = boot(a, b)
        ev, et = c.era_sharpes(six[v]), c.era_sharpes(six[twin])
        both = [n for n in ev if not (math.isnan(ev[n]) or math.isnan(et[n]))]
        ahead = sum(ev[n] > et[n] for n in both)
        need = 4 if len(both) >= 5 else 3
        dv, dt, de = c.describe(six[v]), c.describe(six[twin]), c.describe(six["equal-weight"])
        oou = c.describe(idx[v])["sharpe"] - c.describe(idx[twin])["sharpe"]
        x, y = c.align(six[v], six["tsmom12"])
        d12, p12, z12 = boot(x, y)
        checks = [
            (f"1. Sharpe beats `{twin}` with p < 0.10", dd > 0 and p < 0.10,
             f"{dd:+.3f}, p {p:.2f}"),
            (f"2. Ahead of the twin in at least {need} of {len(both)} eras", ahead >= need,
             f"{ahead} of {len(both)}"),
            ("3. Max drawdown at most 5 points worse than the twin's",
             dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
            ("4. Same sign on `idx`", dd > 0 and oou > 0, f"idx {oou:+.3f}"),
            ("5. Beats equal weight", dv["sharpe"] > de["sharpe"],
             f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
            ("6. Project bar: z >= 4.69 against `tsmom12`", z12 >= 4.69,
             f"{d12:+.3f}, z {z12:+.2f}, p {p12:.2f}"),
        ]  # fmt: skip
        out += [f"### `{v}`", ""]
        out += [f"- {'PASS' if ok else 'FAIL'}: {t} ({det})" for t, ok, det in checks]
        out += ["", f"**`{v}` {'PASSES' if all(k for _, k, _ in checks) else 'FAILS'}.**", ""]
    return out


def crash_summary(
    six: dict[str, Run], idx: dict[str, Run], eps: list[tuple[str, date, date]]
) -> list[str]:
    """Card's descriptive reading: `turb` vs `mag-match` in the fall, `idx` deciding where
    both sets have the episode."""
    out = ["## Fast crashes: `turb` against `mag-match` (card's descriptive reading)", ""]
    out += ["| Episode | Set | `turb` fall | `mag-match` fall | `tsmom12` fall | "
            "`turb` - twin, fall | `turb` - twin, fall + rebound |",
            "|---|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    better, total, nets = 0, 0, []
    for name, _, _ in eps:
        for set_name, runs in (("idx", idx), ("six", six)):
            tv = crash_values(runs["turb"], eps)
            mv = crash_values(runs["mag-match"], eps)
            bv = crash_values(runs["tsmom12"], eps)
            if name in tv and name in mv:
                (tf, tn), (mf, mn), (bf, _) = tv[name], mv[name], bv[name]
                out.append(
                    f"| {name} | {set_name} | {tf:+.1%} | {mf:+.1%} | {bf:+.1%} | "
                    f"{tf - mf:+.1%} | {tn - mn:+.1%} |"
                )
                total += 1
                better += tf > mf
                nets.append(tn - mn)
                break  # idx decides where both have it
    mean_net = float(np.mean(nets)) if nets else math.nan
    helps = better >= 5 and mean_net >= 0
    out += [
        "",
        f"`turb` lost less than `mag-match` in the fall in {better} of {total} episodes; mean "
        f"(fall + rebound) difference {mean_net:+.1%}. Card's reading (at least 5 of 6 and not "
        f"worse on average): **{'not dead (kill-only design)' if helps else 'does not help'}**.",
        "",
    ]
    return out


def main() -> None:
    gspc = c.ctx("idx").hist["GSPC"]
    eps = episodes(gspc)
    out = ["# turbulence-1: turbulence vs a matched volatility trigger on `tsmom12`", ""]
    out += [
        "Card: `cards/turbulence.md`. Write-up: `turbulence-1.md`. Fast-crash dates (S&P 500 "
        "index close, peak -> trough): " + ", ".join(f"{n} {a}..{b}" for n, a, b in eps) + ".",
        "",
    ]
    six = universe("six", RISK_SIX, True, out, eps)
    idx = universe("idx", RISK_IDX, False, out, eps)
    out += bar_lines(six, idx)
    out += crash_summary(six, idx, eps)
    c.write_result("turbulence-1", "\n".join(out))


if __name__ == "__main__":
    main()
