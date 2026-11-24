"""The daily run: fetch bars, ask every live strategy, append to the ledger, replay, score.

`uv run python -m grimstrade.run_daily --root trail` (trail/ = the paper-trail branch checkout).
Plain Python, no LLM. Exits 1 if any data source failed (after still doing what it could), and
2 without writing anything if the ledger's history was rewritten.

`--intraday DIR` runs only the finer-data collection (`grimstrade.intraday`) into DIR and always
exits 0. The daily job calls it in a later step, after the record is committed and pushed, so it
can never break or delay the trades, the ledger or the record checks. DIR is not part of the
record (the sources' terms forbid re-publishing; docs/DECISIONS.md), and nothing that trades or
scores reads it.
"""

from __future__ import annotations

import argparse
import hashlib
import inspect
import json
import sys
from collections import Counter
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from itertools import groupby
from pathlib import Path
from typing import Any

from grimstrade import (
    data,
    gym,
    intraday,
    ledger,
    rates,
    reconcile,
    report,
    signals,
    sources,
    weekly,
)
from grimstrade.strategies import LIVE, NOTES

# First run: fetch this much history (Kraken serves at most 720 daily bars).
BOOTSTRAP_DAYS = 700


WRITTEN_EACH_RUN = ("state/portfolio.json", "state/witness.txt", "reports/scoreboard.md",
                    "reports/backtest.md", "reports/weekly.md")  # fmt: skip


def check_record(root: Path, now: datetime) -> None:
    """Raise LedgerTampered unless the record under `root` can be believed: its history as a
    whole (`ledger.check_history`), every file only ever grew, none is a symbolic link, and the
    bars are rows the runner could have written. The bars are the record too: every score is
    recomputed from them."""
    ledger.check_history(root, now)
    bars = [data.bars_path(root, sym).relative_to(root) for sym in data.UNIVERSE]
    record = (data.REVISIONS, data.SOURCES_LOG, data.DIVIDENDS, rates.RATES)
    for rel in (*ledger.APPEND_ONLY, *bars, *record):
        ledger.refuse_links(root, rel)
        ledger.check_append_only(root / rel)
    for name in WRITTEN_EACH_RUN:  # a link here would swallow what the run writes
        ledger.refuse_links(root, Path(name))
    # Appending is all it takes to add a row by hand, and the append-only check has nothing to
    # say about an append. What no run would write: rows `data.load` refuses (a second row for a
    # stored day, an ETF bar on a weekend) and a bar that has not closed yet.
    for sym, cls in data.UNIVERSE.items():
        try:
            stored = data.load(root, sym)
        except ValueError as e:
            raise ledger.LedgerTampered(str(e)) from e
        if stored and data.close_time(cls, stored[-1].date) > now:
            raise ledger.LedgerTampered(f"{sym}: the bar for {stored[-1].date} has not closed yet")
    # Dividends are paid into every score: a row no run would write (a second payout for one day,
    # one on a day with no session, one far too large) is refused like a bad bar.
    try:
        dividends = data.load_dividends(root)
    except ValueError as e:
        raise ledger.LedgerTampered(str(e)) from e
    for sym, divs in dividends.items():
        stored = data.load(root, sym)
        for d in divs:
            if problem := data.dividend_problem(sym, d, stored):
                raise ledger.LedgerTampered(problem)
    # The cash rate is credited in every score: a row no run writes is refused like a bad bar.
    try:
        stored_rates = rates.load(root)
    except ValueError as e:
        raise ledger.LedgerTampered(str(e)) from e
    if stored_rates and max(r.seen for r in stored_rates) > now:
        raise ledger.LedgerTampered("a stored cash rate claims to be stored in the future")


def fingerprint(decide: gym.Strategy) -> str:
    """A short hash of the code behind a strategy: its own file plus the shared signal helpers.
    Written into each decision, so a strategy that changes under the same name cannot pass as
    one unbroken track record. The raw text is hashed (stable across Python versions), so a
    change of comments or layout shows up as a change too. Empty if the source can't be read:
    a missing fingerprint must never cost a decision."""
    try:
        files = [sys.modules[decide.__module__], signals]
        text = "".join(inspect.getsource(m) for m in files)
    except (OSError, TypeError, KeyError):
        return ""
    return hashlib.sha256(text.encode()).hexdigest()[:12]


def state_row(r: gym.Result) -> dict[str, Any]:
    """One book's row in `state/portfolio.json`."""
    return {
        "cash": round(r.cash, 2),
        "positions": {s: q for s, q in r.positions.items() if q},
        "equity": round(r.equity[-1][1], 2) if r.equity else gym.START_CASH,
        "marked_on": r.equity[-1][0].isoformat() if r.equity else None,
        "fills": len(r.fills),
    }


def run(
    root: Path, now: datetime, get: sources.Get = sources.http_get, repo: Path = Path(".")
) -> list[str]:
    """One daily run. Returns the list of data problems (empty if all went well).

    `repo` is the code checkout, whose `research/` files (on every branch but the record's) count
    towards the number of strategies tried."""
    check_record(root, now)

    problems = []
    for sym in data.UNIVERSE:
        stored = data.load(root, sym)
        since = (
            stored[-1].date + timedelta(days=1)
            if stored
            else now.date() - timedelta(days=BOOTSTRAP_DAYS)
        )
        try:
            source, bars = sources.fetch_from(sym, since, now, get)
            before = len(stored)
            try:
                added = data.append(root, sym, bars)
            finally:  # append may store some bars and then refuse the rest: log what got in
                new = data.load(root, sym)[before:]
                data.log_source(root, sym, source, new, ledger.iso(now))
            print(f"{sym}: +{added} bars ({source})")
        except Exception as e:  # noqa: BLE001 - one bad source must not stop the others
            problems.append(str(e))
            print(f"{sym}: FAILED {e}", file=sys.stderr)

    problems += _dividends(root, get)
    problems += _rates(root, now, get)
    problems += _overdue(root, now)
    problems += _etf_holes(root)
    problems += _revisions(root, now, get)
    history = data.load_all(root)
    seen = data.visible_history(history, now)
    through = {s: b[-1].date.isoformat() for s, b in seen.items() if b}
    lines_before = len(ledger.decisions(root))
    for name, decide in LIVE.items():
        ledger.register_try(root, name, NOTES[name], now)
        previous = ledger.decisions(root, name)
        if previous and previous[-1]["data_through"] == through:
            print(f"{name}: no new data since the last decision, skipped")
            continue
        try:
            weights, reason = decide(seen)
            gym.validate(weights)
        except Exception as e:  # noqa: BLE001 - one broken strategy must not stop the others
            problems.append(f"{name}: {e}")
            print(f"{name}: FAILED {e}", file=sys.stderr)
            continue
        ledger.write_decision(root, now, name, weights, seen, reason, fingerprint(decide))
        print(f"{name}: {weights} ({reason})")

    ledger.record_research(root, repo, now)
    results = report.live_results(root, history)
    state = {name: state_row(r) for name, r in results.items()}
    state_path = root / "state" / "portfolio.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    # The record just written, checked against the rules (`grimstrade.reconcile`): a failure is a
    # problem line like a failed source, so the run exits 1 and the record is still committed.
    new_lines = ledger.decisions(root)[lines_before:]
    checked = reconcile.check_state(root, results)
    checked += reconcile.check_lines(new_lines, data.load_all(root), LIVE)
    for line in checked:
        print(f"FAILED {line}", file=sys.stderr)
    print(f"reconcile: {len(results)} books, {len(new_lines)} new lines, {len(checked)} problems")
    problems += checked
    ledger.record_problems(root, now, problems)
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "scoreboard.md").write_text(report.render(root, history, repo))
    (reports / "backtest.md").write_text(report.render_backtest(root, history, repo))
    (reports / "weekly.md").write_text(weekly.render(root, history, repo))
    return problems


def _dividends(root: Path, get: sources.Get) -> list[str]:
    """Append each ETF's distributions not stored yet (Yahoo, keyless). Each run asks for the
    whole stored span, so a failed or late answer is caught up by the next run; a refused
    distribution (no session on its day, far too large) is a problem line on every run."""
    out = []
    for sym, ticker in sources.DIVIDEND_TICKERS.items():
        bars = data.load(root, sym)
        if not bars:
            continue
        try:
            fetched = sources.yahoo_dividends(ticker, bars[0].date, get)
        except Exception as e:  # noqa: BLE001 - one bad answer must not stop the run
            out.append(f"{sym}: dividends not fetched: {e}")
            print(f"{sym}: dividends FAILED {e}", file=sys.stderr)
            continue
        added, refused = data.append_dividends(root, sym, fetched, bars)
        out += refused
        if added:
            print(f"{sym}: +{added} dividends (yahoo)")
    return out


def _rates(root: Path, now: datetime, get: sources.Get) -> list[str]:
    """Append the T-bill rates not stored yet: from the first stored bar on the first run, then
    from the day after the newest stored rate. Yahoo `^IRX` first, the Treasury for sessions
    Yahoo lacks (DECISIONS, 2026-11-24, second bill-rate source); each stored row's source goes
    in `data/sources.jsonl`. Only when no source answered is it a problem line; the gym carries
    the last known rate forward meanwhile (DECISIONS, 2026-11-18, cash interest)."""
    stored = rates.load(root)
    if stored:
        since = stored[-1].date + timedelta(days=1)
    else:
        firsts = [b[0].date for b in data.load_all(root).values() if b]
        since = min(firsts) if firsts else now.date() - timedelta(days=BOOTSTRAP_DAYS)
    try:
        found, failed, answered = rates.fetch(since, now, get)
        for f in failed:
            print(f"rates: FAILED {f}", file=sys.stderr)
        if not answered:
            return [f"rates not fetched: {'; '.join(failed)}"]
        source_of = {r.date: src for src, r in found}
        try:
            added, refused = rates.append(root, [r for _, r in found])
        finally:  # append may store some rows and then refuse the rest: log what got in
            new = rates.load(root)[len(stored) :]
            for src, run in groupby(new, key=lambda r: source_of[r.date]):
                data.log_days(root, rates.SYMBOL, src, [r.date for r in run], ledger.iso(now))
    except Exception as e:  # noqa: BLE001 - one bad answer must not stop the run
        print(f"rates: FAILED {e}", file=sys.stderr)
        return [f"rates not fetched: {e}"]
    by = Counter(source_of[r.date] for r in new)
    print(f"rates: +{added} ({', '.join(f'{n} {s}' for s, n in sorted(by.items())) or 'none new'})")
    return refused


# Crypto closes every day: a new bar is overdue when the newest stored one closed longer ago
# than this. ETFs: when this many weekday sessions have closed since the newest stored bar (one
# missing session can be a market holiday, two in a row never are).
CRYPTO_OVERDUE = timedelta(hours=36)
ETF_SESSIONS_OVERDUE = 2


def _overdue(root: Path, now: datetime) -> list[str]:
    """A problem line per symbol whose newest stored bar is older than it can honestly be. Sources
    that answer "nothing new" for days produce no error anywhere else: the data just stops, and
    whoever holds that asset looks calm."""
    out = []
    for sym, cls in data.UNIVERSE.items():
        stored = data.load(root, sym)
        if not stored:
            continue
        last = stored[-1].date
        if cls == data.CRYPTO:
            age = now - data.close_time(cls, last)
            if age > CRYPTO_OVERDUE:
                out.append(f"{sym}: no new bar for {age.days} days (newest stored: {last})")
            continue
        missed, day = 0, last + timedelta(days=1)
        while data.close_time(cls, day) + data.SETTLE <= now:
            missed += day.weekday() < 5
            day += timedelta(days=1)
        if missed >= ETF_SESSIONS_OVERDUE:
            out.append(f"{sym}: no new bar for {missed} sessions (newest stored: {last})")
    return out


def _etf_holes(root: Path, recent: int = 10) -> list[str]:
    """The ETFs trade on one calendar, so a session one of them lacks while another has it (and
    has later ones too) is a hole in the data, not a holiday. It can't be filled any more (only
    newer bars are appended); it can at least be said."""
    days = {
        sym: [b.date for b in data.load(root, sym)[-recent:]]
        for sym, cls in data.UNIVERSE.items()
        if cls == data.ETF
    }
    days = {sym: d for sym, d in days.items() if d}
    out = []
    for sym, mine in days.items():
        others = {d for other, theirs in days.items() if other != sym for d in theirs}
        missing = sorted(d for d in others if mine[0] < d < mine[-1] and d not in mine)
        if missing:
            listed = ", ".join(d.isoformat() for d in missing)
            out.append(f"{sym}: no bar for {listed}, a session the other ETFs have")
    return out


def _revisions(root: Path, now: datetime, get: sources.Get) -> list[str]:
    """Ask each symbol's first-choice source again for the last few stored days and log what it
    now says differently (a bar is stored soon after its close; sources correct theirs later).
    Best effort: a failure here is not a data problem, the ingest above already reported those.
    Returns a problem line for each new difference of 1 basis point or more."""
    out = []
    for sym in data.UNIVERSE:
        stored = data.load(root, sym)
        if not stored:
            continue
        source, ticker = sources.SOURCES[sym][0]
        since = stored[-1].date - timedelta(days=data.REVISION_DAYS)
        try:
            again = data.settled(source(ticker, since, get), data.UNIVERSE[sym], now)
            sources.check_sane(again)
        except Exception:  # noqa: BLE001, S112 - best effort, see the docstring
            continue
        # A stored day the source does not list at all, inside the days it does list: a bar
        # nobody could have fetched (a holiday, or a row added by hand).
        listed = {b.date for b in again}
        for b in stored:
            if listed and min(listed) < b.date < max(listed) and b.date not in listed:
                out.append(f"{sym} {b.date}: a bar is stored, but {source.__name__} lists no "
                           "such day")  # fmt: skip
        for day, diff in data.log_revisions(root, sym, source.__name__, again, ledger.iso(now)):
            print(f"{sym} {day}: the source now differs from the stored bar by {diff:.4%}")
            if diff >= 1e-4:
                out.append(f"{sym} {day}: {source.__name__} now shows prices {diff:.2%} away from "
                           "the stored bar (kept as stored; see data/revisions.jsonl)")  # fmt: skip
    return out


def collect_intraday(
    base: Path,
    root: Path,
    now: datetime,
    get: sources.Get = sources.http_get,
    collect: Callable[[Path, datetime, sources.Get], dict[str, str]] = intraday.collect,
) -> dict[str, str]:
    """Collect the finer data into `base`; best effort, never raises. Refuses a `base` inside the
    record `root`: the record checks know nothing of these files, and the terms forbid
    publishing them."""
    if base.resolve().is_relative_to(root.resolve()):
        out = {"intraday": f"error: {base} is inside the record {root}; not collecting"}
    else:
        try:
            out = collect(base, now, get)
        except Exception as e:  # noqa: BLE001 - nothing here may stop the daily job
            out = {"intraday": f"error: {e!r}"}
    for name, result in sorted(out.items()):
        print(f"intraday {name}: {result}")
    return out


def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("trail"))
    p.add_argument("--repo", type=Path, default=Path("."), help="code checkout (research/ files)")
    p.add_argument("--intraday", type=Path, help="only collect the finer data into this folder")
    args = p.parse_args(argv)
    if args.intraday is not None:
        collect_intraday(args.intraday, args.root, datetime.now(UTC))
        return
    try:
        problems = run(args.root, datetime.now(UTC), repo=args.repo)
    except ledger.LedgerTampered as e:
        print(f"REFUSING TO RUN: {e}", file=sys.stderr)
        sys.exit(2)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
