"""Scoreboard: return, Sharpe, deflated Sharpe, max drawdown and turnover per strategy.

`uv run python -m grimstrade.report --root trail` scores the live ledger (the honest record).
Add `--backtest` to also print the backtest report: the live strategies replayed over all stored
history (hindsight: a sanity check of the plumbing and the ideas, never evidence).
"""

from __future__ import annotations

import argparse
import math
import re
import statistics
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

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
    if not eq:
        return Score(name, None, 0, res.start_cash, 0.0, 0.0, 0.0, 0.0)
    # Every day has a return, the first one measured from the start cash: a fill on the first
    # day (a run before the US open) must count in the Sharpe and the drawdown, not only in the
    # total return.
    rets = [b / a - 1 for a, b in zip([res.start_cash, *eq], eq, strict=False)]
    sd = statistics.pstdev(rets)
    # Returns per year from the real time span, not from an assumed spacing: 365 when there is a
    # point every calendar day (the live record: crypto has a bar every day), fewer when days are
    # missing (an ETF-only history has ~252), so the Sharpe does not depend on the spacing.
    span_days = (res.equity[-1][0] - res.equity[0][0]).days + 1
    per_year = len(rets) * DAYS_PER_YEAR / span_days
    sharpe = statistics.fmean(rets) / sd * math.sqrt(per_year) if sd > 0 else 0.0
    peak, mdd = res.start_cash, 0.0
    for e in eq:
        peak = max(peak, e)
        mdd = max(mdd, 1 - e / peak)
    traded = sum(abs(f.qty) * f.price for f in res.fills)
    turnover = traded / statistics.fmean(eq) * DAYS_PER_YEAR / span_days
    return Score(name, res.equity[0][0], len(eq), eq[-1], eq[-1] / res.start_cash - 1, sharpe,
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
    # A decision counts from when it reached the record (its commit), see `ledger.in_force`.
    for counts_from, row in ledger.in_force(root)[0]:
        by_strategy.setdefault(row["strategy"], []).append(Decision(counts_from, row["weights"]))
    return {name: gym.simulate(decs, history) for name, decs in by_strategy.items()}


def restarted(
    counted: Sequence[tuple[datetime, dict[str, Any]]], history: History, name: str, at: datetime
) -> Result:
    """Strategy `name` as if it had started at `at` with fresh cash: the weights it had in force
    at `at`, then its later decisions (`counted` = `ledger.in_force(root)[0]`). The fair yardstick
    for a strategy that started at `at`: same cash, same first opens, same costs. Comparing with
    the yardstick's own curve instead gives it (or denies it) the gap between the starter's
    decision and its first fills, for good."""
    mine = [(t, row["weights"]) for t, row in counted if row["strategy"] == name]
    in_force_then = [w for t, w in mine if t <= at]
    decisions = [Decision(at, in_force_then[-1])] if in_force_then else []
    decisions += [Decision(t, w) for t, w in mine if t > at]
    return gym.simulate(decisions, history)


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


def table(scores: list[Score], beaten: Mapping[str, tuple[int, int]] | None = None) -> str:
    """`beaten` (see `yardsticks_beaten`) adds the one column that can be compared between rows
    that started on different days."""
    extra = " Beats yardsticks |" if beaten is not None else ""
    lines = [
        f"| Strategy | Since | Days | Equity (USD) | Return |{extra} Sharpe | Deflated Sharpe "
        "| Max drawdown | Turnover/yr |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|" + ("---:|" if beaten is not None else ""),
    ]
    for s in sorted(scores, key=lambda s: s.total_return, reverse=True):
        # Never print a certainty: 99.6% must not round to "100%".
        dsr = "-" if s.dsr is None else ">99%" if s.dsr > 0.99 else f"{s.dsr:.0%}"
        beats = ""
        if beaten is not None:
            beats = " {} of {} |".format(*beaten[s.name]) if s.name in beaten else " - |"
        lines.append(
            f"| {plain_name(s.name)} | {s.start or '-'} | {s.days} | {s.equity:,.0f} "
            f"| {s.total_return:+.1%} "
            f"|{beats} {sharpe_cell(s)} | {dsr} | {s.max_drawdown:.1%} | {s.turnover:.2f} |"
        )
    return "\n".join(lines)


def yardsticks_beaten(
    root: Path, history: History, scores: Sequence[Score]
) -> dict[str, tuple[int, int]]:
    """For each strategy that is not itself a yardstick: (yardsticks it is ahead of, yardsticks
    there are). Each yardstick is restarted with fresh cash at the strategy's own start
    (`restarted`), so a strategy that began later is not judged on days it never traded."""
    from grimstrade.strategies import BENCHMARKS

    counted = ledger.in_force(root)[0]
    began: dict[str, datetime] = {}
    for t, row in counted:
        began.setdefault(row["strategy"], t)
    benches = [b for b in BENCHMARKS if b in began]
    out = {}
    for s in scores:
        if s.name in BENCHMARKS or s.name not in began:
            continue
        ahead = sum(
            s.total_return > score(b, restarted(counted, history, b, began[s.name])).total_return
            for b in benches
        )
        out[s.name] = (ahead, len(benches))
    return out


def sharpe_cell(s: Score) -> str:
    """The Sharpe ratio with its standard error, or "-" while the record is too short to mean
    anything (four good days annualise to "Sharpe 30"). Standard error of a Sharpe estimate from
    T daily returns: sqrt((1 + SR^2 / 2) / T) per day (Lo 2002), annualised like the Sharpe."""
    if s.moments is None or s.days < MIN_DAYS_FOR_DSR:
        return "-"
    error = math.sqrt((1 + s.moments.sharpe**2 / 2) / s.moments.periods * DAYS_PER_YEAR)
    return f"{s.sharpe:.2f} ±{error:.1f}"


def sharpe_needed(tries: int, days: int, confidence: float = 0.95) -> float:
    """The annualised Sharpe a record of `days` days must show before its deflated Sharpe reads
    `confidence`, with `tries` strategies tried. A floor: ordinary (normal) returns, and tries
    whose Sharpes differ by luck alone; fat tails or a wider spread of tries raise it.

    Solves PSR(SR) = confidence for SR: (SR - SR0)^2 (T - 1) = z^2 (1 + SR^2 / 2)."""
    sr0 = stats.expected_max_sharpe(max(tries, 1), stats.null_sharpe_variance(days))
    z, t = statistics.NormalDist().inv_cdf(confidence), days - 1
    a, b, c = t - z * z / 2, -2 * sr0 * t, sr0 * sr0 * t - z * z
    return (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a) * math.sqrt(DAYS_PER_YEAR)


def years_of_patience(trials: Trials) -> str:
    """What the deflated Sharpe column asks for, in numbers: the owner will otherwise read "no
    sign of skill" about every strategy for years without knowing that an honest board with this
    many tries says that about a good strategy too."""
    need = [f"{sharpe_needed(trials.count, round(y * DAYS_PER_YEAR)):.1f}" for y in (0.5, 1, 3, 5)]
    return (
        f"with {trials.count} strategies tried, 95% needs a Sharpe ratio (return for the risk "
        f"taken) above about {need[0]} after six months, {need[1]} after one year, {need[2]} after "
        f"three and {need[3]} after five; a very good strategy has about 1"
    )


def footnote(trials: Trials) -> str:
    return (
        f"Strategies tried so far (the record's plus the research lane's): {trials.count}. "
        "Sharpe: daily, 365 days/yr, zero risk-free rate, with its standard error (±): the true "
        "value lies within about two of those, 19 times in 20. Deflated Sharpe: how confident we "
        "can be that the Sharpe beats the best that luck alone would give across all the "
        f"strategies tried (Bailey & López de Prado 2014). Both are shown after {MIN_DAYS_FOR_DSR} "
        "days; before that they mean nothing. The deflated Sharpe is strict: "
        f"{years_of_patience(trials)}. A low number is not a verdict against a strategy; it says "
        "the record is still too short."
    )


def freshness(history: History) -> str:
    """The newest stored bar per asset, with a loud note on any asset that has fallen behind.

    When a source stops, the gym keeps valuing that asset at its last price: no swings, no
    losses, a flat line that reads as a calm strategy. The table can't show that; this line does.
    Crypto has a bar every day; ETFs may lag by a long weekend."""
    lasts = {s: bars[-1].date for s, bars in history.items() if bars}
    if not lasts:
        return "No prices stored yet."
    newest = max(lasts.values())
    parts = []
    for sym, last in lasts.items():
        behind = (newest - last).days
        allowed = 2 if data.UNIVERSE[sym] == data.CRYPTO else 5
        stale = f" (**STALE: {behind} days behind, valued at its last price**)"
        parts.append(f"{sym} {last}" + (stale if behind > allowed else ""))
    return "Prices through: " + ", ".join(parts) + "."


def undecided_days(root: Path, history: History) -> dict[str, int]:
    """Per strategy, the days of new prices on which it made no decision: the run failed, GitHub
    skipped it, its push was lost, the source was down, the strategy raised, or it was retired.
    It kept its old position through them, and no other number shows that.

    Counted on an asset with a bar every day (crypto). Each decision says which bars it saw
    (`data_through`); a jump of more than one day between two decisions, or any stored day after
    the last one, was never decided on. A run that is merely late skips nothing."""
    daily = [s for s, cls in data.UNIVERSE.items() if cls == data.CRYPTO and history.get(s)]
    if not daily:
        return {}
    sym = daily[0]
    saw: dict[str, list[date]] = {}
    for row in ledger.decisions(root):
        through = row["data_through"].get(sym)
        if through:
            saw.setdefault(row["strategy"], []).append(date.fromisoformat(through))
    out = {}
    for name, days in saw.items():
        between = sum(max((b - a).days - 1, 0) for a, b in zip(days, days[1:], strict=False))
        missed = between + max((history[sym][-1].date - days[-1]).days, 0)
        if missed:
            out[name] = missed
    return out


def accepted_rewrites(root: Path) -> list[str]:
    """Rewrites or back-dated pushes of the record branch that a person accepted
    (scripts/check-trail-activity.sh keeps them, append-only)."""
    path = root / ledger.ACCEPTED_REWRITES
    return [x for x in path.read_text().splitlines() if x.strip()] if path.exists() else []


def unwitnessed(root: Path) -> str:
    """Why the last run could not (fully) compare the record with GitHub's activity log; empty
    if it could, or if no run has tried (a local folder)."""
    path = root / ledger.WITNESS
    text = path.read_text().strip() if path.exists() else ""
    return text if text.startswith("NOT") else ""


def code_changes(root: Path) -> dict[str, int]:
    """Per strategy, how often the code behind it changed between two of its decisions (the
    `code_hash` each decision carries). The table shows one row and one unbroken record per
    name; after a change it is in truth another strategy, and another try. Once a name has
    fingerprints, a line without one (written by hand) is a change as well."""
    last: dict[str, str] = {}
    out: dict[str, int] = {}
    for row in ledger.decisions(root):
        name, seen = row["strategy"], row.get("code_hash") or ""
        if name not in last and not seen:
            continue  # written before decisions carried a fingerprint
        if last.get(name, seen) != seen:
            out[name] = out.get(name, 0) + 1
        last[name] = seen
    return out


def plain_name(name: str) -> str:
    """A strategy name as it may appear in a table: names come from the ledger, and one holding
    "|" and a line break would otherwise add a row of invented numbers to the scoreboard."""
    return re.sub(r"[^A-Za-z0-9_.-]", "_", name)[:40]


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
        table(live, yardsticks_beaten(root, history, live)) if live else "No decisions yet.",
        "",
        "Rows started on different days, and Return runs from each row's own start: compare rows "
        'by "Beats yardsticks" (each yardstick restarted with fresh cash at that row\'s start), '
        "not by Return.",
        "",
        freshness(history),
        "",
        footnote(trials),
    ]
    changed = code_changes(root)
    if changed:
        out += [
            "",
            "**Code changed under the same name:** "
            + ", ".join(f"{plain_name(name)} ({n}x)" for name, n in sorted(changed.items()))
            + ". Such a row joins the records of different versions of the strategy; judge it "
            "from the last change on, and count each version as one more strategy tried.",
        ]
    idle = undecided_days(root, history)
    if idle:
        out += [
            "",
            "Days of new prices with no decision (a failed, skipped or lost run, a source that "
            "was down, a strategy that raised or was retired; the old position was held): "
            + ", ".join(
                f"{plain_name(k)} {n}" for k, n in sorted(idle.items(), key=lambda x: -x[1])
            )
            + ".",
        ]
    events = accepted_rewrites(root)
    if events:
        out += [
            "",
            f"**The record branch itself was rewritten or back-dated ({len(events)} event"
            f"{'s' * (len(events) != 1)}), and a person accepted it:** {'; '.join(events)}. "
            "What the record said before that cannot be checked from here.",
        ]
    unchecked = unwitnessed(root)
    if unchecked:
        out += [
            "",
            f"**The last run could not ask GitHub whether the record branch was rewritten:** "
            f"{unchecked}. Until a run can, a replaced record would go unnoticed.",
        ]
    troubled = ledger.problem_runs(root)
    if troubled:
        last = troubled[-1]
        shown = "; ".join(str(x)[:140] for x in last["problems"][:3])
        more = len(last["problems"]) - 3
        out += [
            "",
            f"Runs that reported problems: {len(troubled)}. Latest, {last['time']}: {shown}"
            + (f"; and {more} more" if more > 0 else "")
            + ". All of them: `ledger/problems.jsonl`.",
        ]
    revised = data.revisions(root)
    if revised:
        days = {(str(r["symbol"]), str(r["date"])) for r in revised}
        worst = max(float(str(r["largest_diff"])) for r in revised)
        out += [
            "",
            f"Stored bars whose source later showed other prices: {len(days)} (largest "
            f"difference {worst:.2%}). The stored values are kept; details in "
            "`data/revisions.jsonl`.",
        ]
    late = ledger.in_force(root)[1]
    if late:
        out += [
            "",
            f"**Late decisions: {late}.** They reached the record more than "
            f"{ledger.LATE // timedelta(minutes=1)} minutes after their own timestamp, so they "
            "count from the time they were committed, not from the time they claim.",
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
    from grimstrade import run_daily  # (it imports this module)

    try:  # the same checks as the daily run: a report of a rewritten record is worth nothing
        run_daily.check_record(args.root, datetime.now(UTC))
    except ledger.LedgerTampered as e:
        print(f"REFUSING TO REPORT: {e}", file=sys.stderr)
        sys.exit(2)
    history = data.load_all(args.root)
    print(render(args.root, history, args.repo))
    if args.backtest:
        print(render_backtest(args.root, history, args.repo))


if __name__ == "__main__":
    main()
