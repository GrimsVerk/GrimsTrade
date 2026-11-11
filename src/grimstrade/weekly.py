"""The owner's weekly one-screen summary, `reports/weekly.md`, in plain language.

Who is ahead of the yardsticks after costs, and how sure we are (the deflated Sharpe in words).
Written by the daily runner on every run, so it is always current; it reads as "the week to
<latest date>". Only the forward record counts here; backtests are in `backtest.md`.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

from grimstrade import gym, report
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


def sureness(dsr: float | None) -> str:
    if dsr is None:
        return "too early to tell"
    if dsr >= 0.95:
        return f"strong evidence ({dsr:.0%})"
    if dsr >= 0.90:
        return f"promising ({dsr:.0%})"
    if dsr >= 0.50:
        return f"maybe, could be luck ({dsr:.0%})"
    return f"no sign of skill yet ({dsr:.0%})"


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
        "after trading fees. A strategy only matters if it beats the yardsticks below.",
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
    for name in sorted(others, key=lambda n: scores[n].total_return, reverse=True):
        s = scores[name]
        start = s.start - timedelta(days=1) if s.start else today
        beaten = [b for b in benches if s.total_return > change(results[b], start, today)]
        if benches and len(beaten) == len(benches):
            ahead_of_all.append(name)
        beats = f"{len(beaten)} of {len(benches)}"
        lines.append("| " + " | ".join([*row(name), beats, sureness(s.dsr)]) + " |")
    days = max(s.days for s in scores.values())
    proven = [n for n in others if (scores[n].dsr or 0) >= 0.95 and n in ahead_of_all]
    if days < report.MIN_DAYS_FOR_DSR:
        verdict = f"the record is only {days} days old, far too early to judge anything."
    elif proven:
        verdict = f"{len(proven)} strategy(ies) beat every yardstick with strong evidence."
    else:
        verdict = "no strategy has shown real skill yet; keep watching."
    lines[2:2] = [
        f"**In short:** {len(ahead_of_all)} of {len(others)} strategies are ahead of every "
        f"yardstick so far; {verdict}",
        "",
    ]
    lines += [
        "",
        "\\* Compared over the same days the strategy has been running.  ",
        "\\*\\* The chance its edge is skill rather than luck, allowing for all "
        f"{trials} strategies we have tried (deflated Sharpe). Real money is only discussed "
        "after 6 months, beating every yardstick, and strong evidence (95%+).",
        "",
        "Details: `scoreboard.md`. Backtests (hindsight, not evidence): `backtest.md`.",
    ]
    return "\n".join(lines) + "\n"
