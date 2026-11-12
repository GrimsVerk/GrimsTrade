"""Building blocks shared by the idea tests: volatility, trend baselines, schedules, reporting."""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from datetime import date, timedelta

import numpy as np
import stats
from harness import HALF_SPLIT, SYMS, ResearchStrategy, Run, View, Weights

from grimstrade.data import CRYPTO, UNIVERSE

# Bars per year for each asset's own series.
BARS_PER_YEAR = {s: 365 if UNIVERSE[s] == CRYPTO else 252 for s in SYMS}


def ewma_vol(lr: np.ndarray, halflife: float, bars_per_year: int, min_bars: int = 20) -> float:
    """Annualised EWMA volatility of log returns (zero mean). NaN if too little data."""
    if len(lr) < min_bars:
        return math.nan
    n = min(len(lr), int(halflife * 8))
    x = lr[-n:]
    w = 0.5 ** (np.arange(n)[::-1] / halflife)
    return float(math.sqrt((w * x * x).sum() / w.sum() * bars_per_year))


def asset_vol(view: View, s: str, halflife: float = 30) -> float:
    return ewma_vol(view.logret(s), halflife, BARS_PER_YEAR[s])


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


# 200 trading days is about 290 calendar days: the classic slow trend filter, per asset clock.
SMA_BARS = {s: 290 if UNIVERSE[s] == CRYPTO else 200 for s in SYMS}


def equal_weight(view: View) -> Weights:
    live = [s for s in view.syms if view.n[s] > 0]
    return {s: 1 / len(live) for s in live}


def filtered_equal_weight(signal: Callable[[View, str], bool]) -> ResearchStrategy:
    """Each asset gets a fixed 1/6 slot; the slot is held if signal(view, asset) is true, else it
    sits in cash. The standard wrapper for comparing on/off filters like for like."""

    def f(view: View) -> Weights:
        return {s: 1 / len(SYMS) for s in view.syms if view.n[s] > 0 and signal(view, s)}

    return f


def sma_signal(view: View, s: str) -> bool:
    r = sma_ratio(view, s, SMA_BARS[s])
    return (not math.isnan(r)) and r > 1


def tsmom_signal(view: View, s: str) -> bool:
    r = trailing_logret(view, s, 365)
    return (not math.isnan(r)) and r > 0


def weekly(strategy: ResearchStrategy, weekday: int = 4) -> ResearchStrategy:
    """Re-decide only on one weekday (default Friday): other days repeat that day's decision.
    Stateless, so it works unchanged as a live strategy."""

    def f(view: View) -> Weights:
        today = view.today
        back = (today.weekday() - weekday) % 7
        return strategy(view if back == 0 else view.at(today - timedelta(days=back)))

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


def describe(run: Run) -> dict[str, float]:
    r = run.rets
    first = run.rets_between(run.days[0], HALF_SPLIT - timedelta(days=1))
    second = run.rets_between(HALF_SPLIT, run.days[-1])
    return {
        "sharpe": stats.sharpe(r),
        "se": stats.sharpe_se(r),
        "cagr": stats.cagr(r),
        "vol": stats.vol(r),
        "mdd": stats.max_drawdown(r),
        "turnover": run.score.turnover,
        "exposure": run.exposure,
        "sharpe_h1": stats.sharpe(first) if len(first) > 30 else math.nan,
        "sharpe_h2": stats.sharpe(second) if len(second) > 30 else math.nan,
    }


def table(runs: Sequence[Run], versus: Run | None = None, halves: bool = True) -> str:
    head = "| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure |"
    sep = "|---|---:|---:|---:|---:|---:|---:|"
    if halves:
        head += " Sharpe 2017-21H1 | Sharpe 2021H2-25 |"
        sep += "---:|---:|"
    if versus is not None:
        head += f" dSharpe vs {versus.variant} (p) |"
        sep += "---:|"
    lines = [head, sep]
    for run in runs:
        d = describe(run)
        row = (
            f"| {run.variant} | {d['sharpe']:.2f} ({d['se']:.2f}) | {d['cagr']:+.1%} | "
            f"{d['vol']:.1%} | {d['mdd']:.1%} | {d['turnover']:.1f} | {d['exposure']:.0%} |"
        )
        if halves:
            row += f" {d['sharpe_h1']:.2f} | {d['sharpe_h2']:.2f} |"
        if versus is not None:
            if run is versus:
                row += " - |"
            else:
                diff, p, lo, hi = stats.sharpe_diff_boot(run.rets, versus.rets)
                row += f" {diff:+.2f} (p={p:.2f}, 90% {lo:+.2f}..{hi:+.2f}) |"
        lines.append(row)
    return "\n".join(lines)


def held_dates() -> tuple[date, date]:
    from harness import HELD_END, HELD_START

    return HELD_START, HELD_END
