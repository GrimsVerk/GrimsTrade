"""Building blocks shared by the idea tests: eligibility, volatility, plain twins, schedules,
reporting. The rules here are fixed in research/protocol.md."""

from __future__ import annotations

import math
import os
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from datetime import date, timedelta

import harness
import numpy as np
import stats
from harness import (
    ERAS,
    HELD_END,
    HELD_START,
    OOU_COINS,
    OOU_ETFS,
    OOU_INDEXES,
    STRESS,
    SYMS,
    TRAIN_END,
    TRAIN_START,
    Panel,
    ResearchStrategy,
    Run,
    View,
    Weights,
    load_history,
)

from grimstrade.data import CRYPTO, UNIVERSE, Bar


def bpy(s: str) -> int:
    """Bars per year on the asset's own clock."""
    return 365 if UNIVERSE[s] == CRYPTO else 252


def eligible(view: View, s: str) -> bool:
    """An asset may be held once it has a year of bars. Baselines follow the same rule, so a
    strategy that needs a year of history is compared like for like."""
    return view.n.get(s, 0) >= bpy(s)


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
    Stateless in effect (the per-panel memo only avoids recomputing a Friday seven times)."""
    token = object()

    def f(view: View) -> Weights:
        today = view.today
        day = today - timedelta(days=(today.weekday() - weekday) % 7)
        key = (token, day)
        memo = view.panel.cache
        if key not in memo:
            memo[key] = strategy(view if day == today else view.at(day))
        return memo[key]  # type: ignore[return-value]

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


def vol_series(view: View, s: str, halflife: float) -> np.ndarray:
    """Annualised EWMA volatility after each visible bar (entry i uses returns up to bar i+1 only).
    Precomputed once per panel; causal by construction, and checked by `check_against_gym`."""
    key = ("vol", s, halflife)
    cache = view.panel.cache
    if key not in cache:
        lr = view.panel.lr[s]
        lam = 0.5 ** (1 / halflife)
        out = np.empty(len(lr))
        num = den = 0.0
        for i, x in enumerate(lr):
            num = lam * num + x * x
            den = lam * den + 1.0
            out[i] = math.sqrt(num / den * bpy(s))
        cache[key] = out
    full: np.ndarray = cache[key]  # type: ignore[assignment]
    return full[: max(view.n[s] - 1, 0)]


FIT_MIN_BARS = 1000  # fitted rules and the vol-calm twin hold the slot until this much history


def vol_calm_signal(view: View, s: str) -> bool:
    """Plain twin of the regime models: volatility below its own expanding median."""
    if view.n[s] < FIT_MIN_BARS:
        return True
    v = vol_series(view, s, 30)
    return bool(v[-1] < np.median(v[20:]))


def sixty_forty(view: View) -> Weights:
    held = live(view)
    return {s: w for s, w in (("SPY", 0.6), ("TLT", 0.4)) if s in held}


def hold(sym: str) -> ResearchStrategy:
    return lambda view: {sym: 1.0} if eligible(view, sym) else {}


# --- universes and the run helper ---

DRY = bool(os.environ.get("DRY"))  # plumbing check: last 120 days only, nothing logged


@dataclass
class Ctx:
    name: str
    period: str
    hist: dict[str, list[Bar]]
    panel: Panel
    start: date
    end: date


def _cut(bars: list[Bar], last: date) -> list[Bar]:
    return [b for b in bars if b.date <= last]


def ctx(name: str = "six", period: str = "train", adjusted: bool = True) -> Ctx:
    """A test universe: `six`, `etf`, `coin`, `idx` (four indexes as one portfolio) or a single
    symbol such as `GSPC` (cut at 1993-01-28, before SPY exists), `N225`, `SPY`."""
    sets = {"six": SYMS, "etf": OOU_ETFS, "coin": OOU_COINS, "idx": OOU_INDEXES}
    syms = sets.get(name, [name])
    hist = load_history(period, adjusted, syms)
    if name == "GSPC":
        hist = {"GSPC": [b for b in _cut(hist["GSPC"], date(1993, 1, 28)) if b.date.year >= 1961]}
    elif name == "idx":
        hist["GSPC"] = [b for b in hist["GSPC"] if b.date.year >= 1961]
    if period == "train":
        first = min(b[0].date for b in hist.values())
        start = max(TRAIN_START, first + timedelta(days=366)) if name != "six" else TRAIN_START
        if name in ("GSPC", "idx"):
            start = date(1962, 1, 2)
        elif name in OOU_INDEXES:
            start = first + timedelta(days=366)  # all the history an index has
        end = min(TRAIN_END, max(b[-1].date for b in hist.values()) - timedelta(days=1))
    else:
        start, end = HELD_START, HELD_END
    if DRY:
        start = end - timedelta(days=120)
    return Ctx(name, period, hist, Panel(hist), start, end)


def go(
    idea: str,
    variant: str,
    strategy: ResearchStrategy,
    c: Ctx,
    kind: str = "variant",
    log: bool = True,
    start: date | None = None,
) -> Run:
    """Run a strategy on a universe and log the try (variant name is tagged with the universe)."""
    tag = variant if c.name == "six" else f"{variant}@{c.name}"
    return harness.run(
        idea, tag, strategy, kind=kind, period=c.period, panel=c.panel, history=c.hist,
        start=max(start, c.start) if start else c.start, end=c.end, log=log and not DRY,
    )  # fmt: skip


def write_result(idea: str, text: str) -> None:
    path = harness.RESEARCH / "results" / (f"{idea}.md" if not DRY else f"{idea}.dry.md")
    path.parent.mkdir(exist_ok=True)
    path.write_text(text.rstrip() + "\n")
    print(text)


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
    all_es = [era_sharpes(r) for r in runs]
    names = [n for n, _, _ in ERAS if any(not math.isnan(e[n]) for e in all_es)]
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
