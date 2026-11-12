"""Building blocks shared by the idea tests: eligibility, volatility, plain twins, schedules,
reporting. The rules here are fixed in research/protocol.md."""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from datetime import date, timedelta

import numpy as np
import stats
from harness import ERAS, STRESS, ResearchStrategy, Run, View, Weights

from grimstrade.data import CRYPTO, UNIVERSE


def bpy(s: str) -> int:
    """Bars per year on the asset's own clock."""
    return 365 if UNIVERSE[s] == CRYPTO else 252


def eligible(view: View, s: str) -> bool:
    """An asset may be held once it has a year of bars. Baselines follow the same rule, so a
    strategy that needs a year of history is compared like for like."""
    return view.n[s] >= bpy(s)


def live(view: View) -> list[str]:
    return [s for s in view.syms if eligible(view, s)]


def ewma_vol(lr: np.ndarray, halflife: float, bars_per_year: int, min_bars: int = 20) -> float:
    """Annualised EWMA volatility of log returns (zero mean). NaN if too little data."""
    if len(lr) < min_bars:
        return math.nan
    n = min(len(lr), int(halflife * 8))
    x = lr[-n:]
    w = 0.5 ** (np.arange(n)[::-1] / halflife)
    return float(math.sqrt((w * x * x).sum() / w.sum() * bars_per_year))


def asset_vol(view: View, s: str, halflife: float = 30) -> float:
    return ewma_vol(view.logret(s), halflife, bpy(s))


def trailing_logret(view: View, s: str, days: int) -> float:
    """Log return over the last `days` calendar days (NaN if history is shorter)."""
    d, c = view.dates(s), view.close(s)
    if len(c) < 2:
        return math.nan
    target = d[-1] - days
    if d[0] > target:
        return math.nan
    i = int(np.searchsorted(d, target, side="right")) - 1
    return float(math.log(c[-1] / c[i]))


def sma_ratio(view: View, s: str, bars: int) -> float:
    c = view.close(s)
    return float(c[-1] / c[-bars:].mean()) if len(c) >= bars else math.nan


def sma_bars(s: str) -> int:
    """200 trading days is about 290 calendar days: the classic slow trend filter, per clock."""
    return 290 if UNIVERSE[s] == CRYPTO else 200


# --- plain strategies: benchmarks and the "plain twins" exotic ideas must beat ---


def equal_weight(view: View) -> Weights:
    held = live(view)
    return {s: 1 / len(held) for s in held}


def slots(signal: Callable[[View, str], bool]) -> ResearchStrategy:
    """Each eligible asset gets an equal slot; the slot is held if signal(view, asset) is true,
    else it sits in cash. The standard wrapper for comparing on/off filters like for like."""

    def f(view: View) -> Weights:
        held = live(view)
        return {s: 1 / len(held) for s in held if signal(view, s)}

    return f


def sma_signal(view: View, s: str) -> bool:
    r = sma_ratio(view, s, sma_bars(s))
    return (not math.isnan(r)) and r > 1


def tsmom_signal(view: View, s: str) -> bool:
    r = trailing_logret(view, s, 365)
    return (not math.isnan(r)) and r > 0


def inverse_vol(view: View) -> Weights:
    """Unlevered risk parity, naive form: weights proportional to 1/vol, summing to 1."""
    inv = {s: 1 / v for s in live(view) if (v := asset_vol(view, s, 60)) > 0}
    tot = sum(inv.values())
    return {s: x / tot for s, x in inv.items()}


def weekly(strategy: ResearchStrategy, weekday: int = 4) -> ResearchStrategy:
    """Re-decide only on one weekday (default Friday): other days repeat that day's decision.
    Stateless in effect (the memo only avoids recomputing the same Friday seven times)."""
    memo: dict[tuple[int, date], Weights] = {}

    def f(view: View) -> Weights:
        today = view.today
        day = today - timedelta(days=(today.weekday() - weekday) % 7)
        key = (id(view.panel), day)
        if key not in memo:
            memo.clear()
            memo[key] = strategy(view if day == today else view.at(day))
        return memo[key]

    return f


def monthly(strategy: ResearchStrategy) -> ResearchStrategy:
    """Re-decide on the last business day of each month (as known from the bars seen so far)."""

    def f(view: View) -> Weights:
        g = view.panel.grid_dates[: view.n_grid]
        i = len(g) - 1
        # walk back to the last grid day that was a month end (next grid day is in a new month)
        while i > 0 and not (i + 1 < len(g) and g[i + 1].month != g[i].month):
            i -= 1
        return strategy(view.at(g[i])) if i > 0 else {}

    return f


# --- reporting ---


def era_sharpes(run: Run) -> dict[str, float]:
    out = {}
    for name, a, b in ERAS:
        r = run.rets_between(a, b)
        out[name] = stats.sharpe(r) if len(r) >= 250 and r.std() > 0 else math.nan
    return out


def describe(run: Run) -> dict[str, float]:
    r = run.rets
    return {
        "sharpe": stats.sharpe(r),
        "se": stats.sharpe_se(r),
        "cagr": stats.cagr(r),
        "vol": stats.vol(r),
        "mdd": stats.max_drawdown(r),
        "turnover": run.score.turnover,
        "exposure": run.exposure,
    }


def _f(x: float, spec: str = ".2f") -> str:
    return "-" if math.isnan(x) else format(x, spec)


def table(runs: Sequence[Run], versus: Run | None = None, eras: bool = True) -> str:
    """One row per run. With `versus`: the Sharpe difference to that run on the same days, a
    paired block-bootstrap p-value, and in how many eras the run's Sharpe beats it."""
    head = "| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure |"
    sep = "|---|---:|---:|---:|---:|---:|---:|"
    names = [n for n, _, _ in ERAS]
    if eras:
        head += "".join(f" {n} |" for n in names)
        sep += "---:|" * len(names)
    if versus is not None:
        head += f" dSharpe vs {versus.variant} (p; 90% range) | Eras ahead |"
        sep += "---:|---:|"
    lines = [head, sep]
    for run in runs:
        d = describe(run)
        row = (
            f"| {run.variant} | {d['sharpe']:.2f} ({d['se']:.2f}) | {d['cagr']:+.1%} | "
            f"{d['vol']:.1%} | {d['mdd']:.1%} | {d['turnover']:.1f} | {d['exposure']:.0%} |"
        )
        es = era_sharpes(run)
        if eras:
            row += "".join(f" {_f(es[n])} |" for n in names)
        if versus is not None:
            if run is versus:
                row += " - | - |"
            else:
                a, b = align(run, versus)
                diff, p, lo, hi = stats.sharpe_diff_boot(a, b)
                ev = era_sharpes(versus)
                both = [n for n in names if not (math.isnan(es[n]) or math.isnan(ev[n]))]
                ahead = sum(es[n] > ev[n] for n in both)
                row += f" {diff:+.2f} (p={p:.2f}; {lo:+.2f}..{hi:+.2f}) | {ahead}/{len(both)} |"
        lines.append(row)
    return "\n".join(lines)


def align(a: Run, b: Run) -> tuple[np.ndarray, np.ndarray]:
    """Daily returns of two runs on their common days."""
    lo, hi = max(a.days[0], b.days[0]), min(a.days[-1], b.days[-1])
    return a.rets_between(lo, hi), b.rets_between(lo, hi)


def stress_table(runs: Sequence[Run]) -> str:
    """Total return of each run inside each named stress window (blank if not running yet)."""
    head = "| Variant |" + "".join(f" {n} |" for n, _, _ in STRESS)
    lines = [head, "|---|" + "---:|" * len(STRESS)]
    for run in runs:
        row = f"| {run.variant} |"
        for _, a, b in STRESS:
            r = run.rets_between(a, b)
            ok = len(r) > 5 and run.days[0] <= a
            row += f" {float(np.prod(1 + r) - 1):+.0%} |" if ok else " - |"
        lines.append(row)
    return "\n".join(lines)


def growth(run: Run) -> float:
    """Mean daily log growth, annualised: what a Kelly bettor maximises."""
    return float(np.log1p(run.rets).mean() * 365)
