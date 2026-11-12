"""The owner's weekly one-screen summary, `reports/weekly.md`, in plain language.

Who is ahead of the yardsticks after costs, and how sure we are (the deflated Sharpe in words).
Written by the daily runner on every run, so it is always current; it reads as "the week to
<latest date>". Only the forward record counts here; backtests are in `backtest.md`.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from grimstrade import gym, ledger, report
from grimstrade.data import History
from grimstrade.gym import Result
from grimstrade.strategies import BENCHMARKS

# Plain-language names for the owner. Unknown strategies show their code name.
PLAIN: dict[str, str] = {
    "buy_hold_btc": "Hold Bitcoin",
    "buy_hold_spy": "Hold the US stock market (SPY)",
    "sixty_forty": "60% stocks, 40% bonds",
    "equal_weight": "Equal parts of all six",
    "ts_momentum": "Trend following: hold what rose over the last year",
    "xs_momentum": "Winners: hold the best risers of the last 6 months",
    "vol_target_spy": "Stocks, but less of them when markets are wild",
    "risk_parity": "Balanced risk: less of the wild assets, more of the calm",
    "crypto_mean_reversion": "Buy sharp crypto dips in an uptrend",
}


def equity_on(res: Result, d: date) -> float:
    """Equity at the end of the last day on or before `d` (the start cash before any mark)."""
    value = gym.START_CASH
    for day, e in res.equity:
        if day > d:
            break
        value = e
    return value


def change(res: Result, start: date, end: date) -> float:
    """Return from the end of `start` to the end of `end`."""
    return equity_on(res, end) / equity_on(res, start) - 1


# Real money is only discussed after this long (and beating every yardstick, 95%+ sure).
PROOF_DAYS = 182


def sureness(dsr: float | None, ahead: bool = True) -> str:
    """The deflated Sharpe in words. It says whether the risk-adjusted return beats luck, not
    whether the strategy beats the yardsticks, so "strong" needs `ahead` (beats all of them)."""
    if dsr is None:
        return "too early to tell"
    if dsr >= 0.95:
        if not ahead:
            return f"beats luck, but trails a yardstick ({dsr:.0%})"
        return f"strong evidence ({dsr:.0%})"
    if dsr >= 0.90:
        return f"promising ({dsr:.0%})"
    if dsr >= 0.50:
        return f"maybe, could be luck ({dsr:.0%})"
    return f"no sign of skill yet ({dsr:.0%})"


def verdict(days: int, proven: int, early: int) -> str:
    """The "In short" judgement. `proven` strategies beat every yardstick and luck (95%+) over at
    least PROOF_DAYS of their own record; `early` ones over less. `days`: the oldest record."""
    if days < report.MIN_DAYS_FOR_DSR:
        return f"the record is only {days} day{'s' * (days != 1)} old, far too early to judge."
    out = []
    if proven:
        out.append(f"{proven} beat every yardstick with strong evidence over 6+ months.")
    if early:
        out.append(f"{early} look{'s' * (early == 1)} strong, but under 6 months of record that "
                   "can still be the luck of the period; keep watching.")  # fmt: skip
    return " ".join(out) or "no strategy has shown real skill yet; keep watching."


def render(root: Path, history: History, repo: Path = Path(".")) -> str:
    results = report.live_results(root, history)
    marks = [r.equity[-1][0] for r in results.values() if r.equity]
    if not marks:
        return "# Weekly summary\n\nNo trading days recorded yet.\n"
    today = max(marks)
    week_ago = today - timedelta(days=7)
    trials = report.count_tries(root, repo)
    scores = {s.name: s for s in report.live_scores(root, history, trials)}
    benches = [b for b in BENCHMARKS if b in results]
    others = [n for n in results if n not in BENCHMARKS]

    def row(name: str) -> list[str]:
        r, s = results[name], scores[name]
        return [PLAIN.get(name, name), f"{s.equity:,.0f}", f"{change(r, week_ago, today):+.1%}",
                f"{s.total_return:+.1%}"]  # fmt: skip

    ahead_of_all = []
    lines = [
        f"# Weekly summary: the week to {today:%A %d %B %Y}",
        "",
        "Fake money on real prices. Every strategy started with 10,000 USD; all figures are "
        "after trading fees and slippage. Dividends are not credited yet, which makes the fund "
        "yardsticks 1 to 2% a year too easy to beat. A strategy only matters if it beats the "
        "yardsticks below.",
        "",
        "## Yardsticks",
        "",
        "| Yardstick | Now (USD) | This week | Since start |",
        "|---|---:|---:|---:|",
        *("| " + " | ".join(row(b)) + " |" for b in benches),
        "",
        "## Strategies",
        "",
        "| Strategy | Now (USD) | This week | Since start | Beats yardsticks* | How sure** |",
        "|---|---:|---:|---:|---|---|",
    ]
    # Against each yardstick restarted with fresh cash at the moment the strategy started: same
    # first prices, same costs. (The yardstick's own curve would hand one of the two the move
    # between the strategy's first decision and its first fills.)
    beaten = report.yardsticks_beaten(root, history, list(scores.values()))
    for name in sorted(others, key=lambda n: scores[n].total_return, reverse=True):
        s = scores[name]
        won, of = beaten.get(name, (0, 0))
        ahead = of > 0 and won == of
        if ahead:
            ahead_of_all.append(name)
        lines.append(
            "| " + " | ".join([*row(name), f"{won} of {of}", sureness(s.dsr, ahead)]) + " |"
        )
    days = max(s.days for s in scores.values())
    strong = [n for n in ahead_of_all if (scores[n].dsr or 0) >= 0.95]
    proven = [n for n in strong if scores[n].days >= PROOF_DAYS]
    lines[2:2] = [
        f"**In short:** {len(ahead_of_all)} of {len(others)} strategies are ahead of every "
        f"yardstick so far; {verdict(days, len(proven), len(strong) - len(proven))}",
        "",
    ]
    week = [r for r in ledger.problem_runs(root) if r["time"][:10] > week_ago.isoformat()]
    if week:
        lines[4:4] = [
            f"**Note:** {len(week)} run{'s' * (len(week) != 1)} this week reported problems "
            "(a price source or a strategy failing); see the end of `scoreboard.md`.",
            "",
        ]
    fresh = report.freshness(history)
    if "STALE" in fresh:  # a stopped price source makes whoever holds that asset look calm
        lines[4:4] = [f"**Warning, old prices.** {fresh}", ""]
    lines += [
        "",
        "\\* Compared with each yardstick started afresh at the moment the strategy started "
        "(same first prices, same costs).  ",
        "\\*\\* How confident we can be that its return for the risk taken is real and not "
        f"luck, allowing for all {trials.count} strategies we have tried (deflated Sharpe). It "
        "does not by itself mean it beats the yardsticks. Real money is only discussed after 6 "
        "months, beating every yardstick, and strong evidence (95%+).  ",
        f"Strong evidence takes years, not months: {report.years_of_patience(trials)}. Until "
        'then "no sign of skill yet" is what an honest table says about a good strategy too.',
        "",
        "Details: `scoreboard.md`. Backtests (hindsight, not evidence): `backtest.md`.",
    ]
    return "\n".join(lines) + "\n"
