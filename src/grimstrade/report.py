"""Scoreboard: return, Sharpe, max drawdown and turnover per strategy.

`uv run python -m grimstrade.report --root trail` scores the live ledger (the honest record).
Add `--backtest` to also run the live strategies over all stored history (hindsight: a sanity
check of the plumbing, never evidence).
"""

from __future__ import annotations

import argparse
import math
import statistics
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from grimstrade import data, gym, ledger
from grimstrade.data import History
from grimstrade.gym import Decision, Result

DAYS_PER_YEAR = 365


@dataclass(frozen=True)
class Score:
    name: str
    start: date | None
    days: int
    equity: float
    total_return: float
    sharpe: float
    max_drawdown: float
    turnover: float  # traded value / mean equity, per year


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
                 mdd, turnover)  # fmt: skip


def live_results(root: Path, history: History) -> dict[str, Result]:
    by_strategy: dict[str, list[Decision]] = {}
    for row in ledger.decisions(root):
        d = Decision(ledger.parse_time(row["time"]), row["weights"])
        by_strategy.setdefault(row["strategy"], []).append(d)
    return {name: gym.simulate(decs, history) for name, decs in by_strategy.items()}


def backtest_results(history: History, names: list[str] | None = None) -> dict[str, Result]:
    from grimstrade.strategies import LIVE

    firsts = [b[0].date for b in history.values() if b]
    lasts = [b[-1].date for b in history.values() if b]
    if not firsts:
        return {}
    start, end = max(firsts) + timedelta(days=1), max(lasts)
    return {
        name: gym.simulate(gym.backtest(LIVE[name], history, start, end), history)
        for name in (names or list(LIVE))
    }


def table(scores: list[Score]) -> str:
    lines = [
        "| Strategy | Since | Days | Equity (USD) | Return | Sharpe | Max drawdown | Turnover/yr |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for s in sorted(scores, key=lambda s: s.total_return, reverse=True):
        lines.append(
            f"| {s.name} | {s.start or '-'} | {s.days} | {s.equity:,.0f} | {s.total_return:+.1%} "
            f"| {s.sharpe:.2f} | {s.max_drawdown:.1%} | {s.turnover:.2f} |"
        )
    return "\n".join(lines)


def render(root: Path, history: History, backtest: bool = False) -> str:
    live = [score(n, r) for n, r in live_results(root, history).items()]
    out = [
        "# Scoreboard",
        "",
        "Forward paper trading on real prices, fake money (10,000 USD start per strategy). "
        "Fills at the next open after each decision, after fees and slippage.",
        "",
        table(live) if live else "No decisions yet.",
        "",
        f"Strategies tried so far: {ledger.tries(root)}. "
        "Sharpe: daily, 365 days/yr, zero risk-free rate.",
    ]
    if backtest:
        bt = [score(n, r) for n, r in backtest_results(history).items()]
        out += ["", "## Backtest over stored history (hindsight, not the record)", "", table(bt)]
    return "\n".join(out) + "\n"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("trail"))
    p.add_argument("--backtest", action="store_true")
    args = p.parse_args()
    print(render(args.root, data.load_all(args.root), args.backtest))


if __name__ == "__main__":
    main()
