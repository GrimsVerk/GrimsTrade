"""The daily run: fetch bars, ask every live strategy, append to the ledger, replay, score.

`uv run python -m grimstrade.run_daily --root trail` (trail/ = the paper-trail branch checkout).
Plain Python, no LLM. Exits 1 if any data source failed (after still doing what it could), and
2 without writing anything if the ledger's history was rewritten.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime, timedelta
from pathlib import Path

from grimstrade import data, gym, ledger, report, sources, weekly
from grimstrade.strategies import LIVE, NOTES

# First run: fetch this much history (Kraken serves at most 720 daily bars).
BOOTSTRAP_DAYS = 700


def run(
    root: Path, now: datetime, get: sources.Get = sources.http_get, repo: Path = Path(".")
) -> list[str]:
    """One daily run. Returns the list of data problems (empty if all went well).

    `repo` is the code checkout, whose `research/` files (and research-* branches) count towards
    the number of strategies tried."""
    for rel in ledger.APPEND_ONLY:
        ledger.check_append_only(root / rel)
    for sym in data.UNIVERSE:  # the bars are the record too: every score is recomputed from them
        ledger.check_append_only(data.bars_path(root, sym))
    for rel in (data.REVISIONS, data.SOURCES_LOG):
        ledger.check_append_only(root / rel)

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

    problems += _overdue(root, now)
    problems += _etf_holes(root)
    problems += _revisions(root, now, get)
    history = data.load_all(root)
    seen = data.visible_history(history, now)
    through = {s: b[-1].date.isoformat() for s, b in seen.items() if b}
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
        ledger.write_decision(root, now, name, weights, seen, reason)
        print(f"{name}: {weights} ({reason})")

    ledger.record_research(root, repo, now)
    results = report.live_results(root, history)
    state = {
        name: {
            "cash": round(r.cash, 2),
            "positions": {s: q for s, q in r.positions.items() if q},
            "equity": round(r.equity[-1][1], 2) if r.equity else gym.START_CASH,
            "marked_on": r.equity[-1][0].isoformat() if r.equity else None,
            "fills": len(r.fills),
        }
        for name, r in results.items()
    }
    state_path = root / "state" / "portfolio.json"
    state_path.parent.mkdir(parents=True, exist_ok=True)
    state_path.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
    reports = root / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "scoreboard.md").write_text(report.render(root, history, repo))
    (reports / "backtest.md").write_text(report.render_backtest(root, history, repo))
    (reports / "weekly.md").write_text(weekly.render(root, history, repo))
    return problems


# A new bar is overdue when the newest stored one closed longer ago than this. Crypto closes
# every day; ETFs can pause four calendar days (Thursday to Monday around a Friday holiday).
OVERDUE = {data.CRYPTO: timedelta(hours=36), data.ETF: timedelta(days=4, hours=12)}


def _overdue(root: Path, now: datetime) -> list[str]:
    """A problem line per symbol whose newest stored bar is older than it can honestly be. Sources
    that answer "nothing new" for days produce no error anywhere else: the data just stops, and
    whoever holds that asset looks calm."""
    out = []
    for sym, cls in data.UNIVERSE.items():
        stored = data.load(root, sym)
        if stored and now - data.close_time(cls, stored[-1].date) > OVERDUE[cls]:
            days = (now - data.close_time(cls, stored[-1].date)).days
            out.append(f"{sym}: no new bar for {days} days (newest stored: {stored[-1].date})")
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
        for day, diff in data.log_revisions(root, sym, source.__name__, again, ledger.iso(now)):
            print(f"{sym} {day}: the source now differs from the stored bar by {diff:.4%}")
            if diff >= 1e-4:
                out.append(f"{sym} {day}: {source.__name__} now shows prices {diff:.2%} away from "
                           "the stored bar (kept as stored; see data/revisions.jsonl)")  # fmt: skip
    return out


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path("trail"))
    p.add_argument("--repo", type=Path, default=Path("."), help="code checkout (research/ files)")
    args = p.parse_args()
    try:
        problems = run(args.root, datetime.now(UTC), repo=args.repo)
    except ledger.LedgerTampered as e:
        print(f"REFUSING TO RUN: {e}", file=sys.stderr)
        sys.exit(2)
    if problems:
        sys.exit(1)


if __name__ == "__main__":
    main()
