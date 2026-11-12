"""Scoreboard: return, Sharpe, deflated Sharpe, max drawdown and turnover per strategy.

`uv run python -m grimstrade.report --root trail` scores the live ledger (the honest record).
Add `--backtest` to also print the backtest report: the live strategies replayed over all stored
history (hindsight: a sanity check of the plumbing and the ideas, never evidence).
"""

from __future__ import annotations

import argparse
import math
import statistics
from collections.abc import Sequence
from dataclasses import dataclass, replace
from datetime import date, timedelta
from pathlib import Path

from grimstrade import data, gym, ledger, stats
from grimstrade.data import History
from grimstrade.gym import Decision, Result
from grimstrade.stats import Moments

DAYS_PER_YEAR = 365
# Under this many days the deflated Sharpe isn't shown: too early to say anything.
MIN_DAYS_FOR_DSR = 30
# The backtest report's second window: the most recent year.
RECENT_DAYS = 365


@dataclass(frozen=True)
class Score:
    name: str
    start: date | None
    days: int
    equity: float
    total_return: float
    sharpe: float  # annualised
    max_drawdown: float
    turnover: float  # traded value / mean equity, per year
    moments: Moments | None = None  # of daily returns, for the deflated Sharpe
    dsr: float | None = None  # probability the true Sharpe > 0, given the number of tries


def score(name: str, res: Result) -> Score:
    eq = [e for _, e in res.equity]
    if len(eq) < 2:
        last = eq[-1] if eq else gym.START_CASH
        return Score(name, res.equity[0][0] if eq else None, len(eq), last, 0.0, 0.0, 0.0, 0.0)
    rets = [b / a - 1 for a, b in zip(eq, eq[1:], strict=False)]
    sd = statistics.pstdev(rets)
    sharpe = statistics.fmean(rets) / sd * math.sqrt(DAYS_PER_YEAR) if sd > 0 else 0.0
    peak, mdd = eq[0], 0.0
    for e in eq:
        peak = max(peak, e)
        mdd = max(mdd, 1 - e / peak)
    traded = sum(abs(f.qty) * f.price for f in res.fills)
    turnover = traded / statistics.fmean(eq) * DAYS_PER_YEAR / len(eq)
    return Score(name, res.equity[0][0], len(eq), eq[-1], eq[-1] / gym.START_CASH - 1, sharpe,
                 mdd, turnover, stats.moments(rets))  # fmt: skip


@dataclass(frozen=True)
class Trials:
    """Every strategy tried anywhere (`count`), and the annualised Sharpes we know of tries that
    are not on the table being scored (the research lane's variants)."""

    count: int
    other_sharpes: tuple[float, ...] = ()


def deflate(scores: Sequence[Score], trials: Trials) -> list[Score]:
    """Fill in each score's deflated Sharpe, given all the strategies tried.

    The variance of Sharpe ratios across trials is the larger of (a) what pure luck gives over this
    record's length and (b) the spread of the Sharpes in `scores` together with the other tries'
    known Sharpes (rule in docs/DECISIONS.md).
    """
    ready = [s.moments for s in scores if s.moments and s.days >= MIN_DAYS_FOR_DSR]
    daily = [m.sharpe for m in ready] + [x / math.sqrt(DAYS_PER_YEAR) for x in trials.other_sharpes]
    spread = statistics.variance(daily) if len(daily) >= 2 else 0.0
    out = []
    for s in scores:
        if s.moments is None or s.days < MIN_DAYS_FOR_DSR:
            out.append(s)
            continue
        var = max(stats.null_sharpe_variance(s.moments.periods), spread)
        out.append(replace(s, dsr=stats.deflated_sharpe(s.moments, max(trials.count, 1), var)))
    return out


def live_results(root: Path, history: History) -> dict[str, Result]:
    by_strategy: dict[str, list[Decision]] = {}
    for row in ledger.decisions(root):
        d = Decision(ledger.parse_time(row["time"]), row["weights"])
        by_strategy.setdefault(row["strategy"], []).append(d)
    return {name: gym.simulate(decs, history) for name, decs in by_strategy.items()}


def backtest_results(
    history: History, names: list[str] | None = None, start: date | None = None
) -> dict[str, Result]:
    """Replay the live strategies from `start` (default: the day after the latest first bar, so
    every asset has data) to the last stored bar. A strategy that raises is left out (the daily
    runner already reports it as a problem)."""
    from grimstrade.strategies import LIVE

    firsts = [b[0].date for b in history.values() if b]
    lasts = [b[-1].date for b in history.values() if b]
    if not firsts:
        return {}
    start, end = start or max(firsts) + timedelta(days=1), max(lasts)
    out = {}
    for name in names or list(LIVE):
        try:
            out[name] = gym.simulate(gym.backtest(LIVE[name], history, start, end), history)
        except Exception:  # noqa: BLE001, S112 - one broken strategy must not hide the others
            continue
    return out


def table(scores: list[Score]) -> str:
    lines = [
        "| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Deflated Sharpe "
        "| Max drawdown | Turnover/yr |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for s in sorted(scores, key=lambda s: s.total_return, reverse=True):
        dsr = "-" if s.dsr is None else f"{s.dsr:.0%}"
        lines.append(
            f"| {s.name} | {s.start or '-'} | {s.days} | {s.equity:,.0f} | {s.total_return:+.1%} "
            f"| {s.sharpe:.2f} | {dsr} | {s.max_drawdown:.1%} | {s.turnover:.2f} |"
        )
    return "\n".join(lines)


def footnote(trials: Trials) -> str:
    return (
        f"Strategies tried so far (the record's plus the research lane's): {trials.count}. "
        "Sharpe: daily, 365 days/yr, zero risk-free rate. Deflated Sharpe: how confident we can be "
        "that the Sharpe beats the best that luck alone would give across all the strategies "
        f"tried (Bailey & López de Prado 2014); shown after {MIN_DAYS_FOR_DSR} days."
    )


def count_tries(root: Path, repo: Path) -> Trials:
    """All strategies tried: registered ones, live ones not yet registered, the research lane's
    (visible or recorded), with the research variants' Sharpes. Read-only."""
    from grimstrade.strategies import LIVE

    return Trials(ledger.total_tries(root, repo, LIVE), tuple(ledger.research_sharpes(repo, root)))


def live_scores(root: Path, history: History, trials: Trials) -> list[Score]:
    return deflate([score(n, r) for n, r in live_results(root, history).items()], trials)


def render(root: Path, history: History, repo: Path = Path(".")) -> str:
    trials = count_tries(root, repo)
    live = live_scores(root, history, trials)
    out = [
        "# Scoreboard",
        "",
        "Forward paper trading on real prices, fake money (10,000 USD start per strategy). "
        "Fills at the next open after each decision, after fees and slippage.",
        "",
        table(live) if live else "No decisions yet.",
        "",
        footnote(trials),
    ]
    return "\n".join(out) + "\n"


def backtest_scores(history: History, trials: Trials, start: date | None = None) -> list[Score]:
    return deflate([score(n, r) for n, r in backtest_results(history, start=start).items()], trials)


def _left_out(scores: Sequence[Score]) -> list[str]:
    """A note naming live strategies missing from a backtest table (they raised in the replay)."""
    from grimstrade.strategies import LIVE

    missing = sorted(set(LIVE) - {s.name for s in scores})
    return [f"Left out, the replay raised an error: {', '.join(missing)}.", ""] if missing else []


def render_backtest(root: Path, history: History, repo: Path = Path(".")) -> str:
    trials = count_tries(root, repo)
    lasts = [b[-1].date for b in history.values() if b]
    out = [
        "# Backtest (hindsight, NOT the record)",
        "",
        "The live strategies replayed over the stored price history with the same gym rules "
        "(next-open fills, fees, slippage). This is hindsight: the strategies were chosen "
        "knowing roughly how such rules did in the past. Only the forward record in "
        "`scoreboard.md` counts as evidence.",
        "",
    ]
    if not lasts:
        return "\n".join([*out, "No stored history yet."]) + "\n"
    full = backtest_scores(history, trials)
    out += [
        "## All stored history",
        "",
        "Strategies that need a year of history sit in cash at first.",
        "",
        table(full),
        "",
        *_left_out(full),
        f"## Last {RECENT_DAYS} days",
        "",
        "With under two years stored, a strategy needing a year of history may still start this "
        "window in cash.",
        "",
        table(backtest_scores(history, trials, max(lasts) - timedelta(days=RECENT_DAYS - 1))),
        "",
        footnote(trials),
    ]
    return "\n".join(out) + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("trail"))
    p.add_argument("--repo", type=Path, default=Path("."), help="code checkout (research/ files)")
    p.add_argument("--backtest", action="store_true")
    args = p.parse_args()
    history = data.load_all(args.root)
    print(render(args.root, history, args.repo))
    if args.backtest:
        print(render_backtest(args.root, history, args.repo))


if __name__ == "__main__":
    main()
