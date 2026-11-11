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

from grimstrade import data, gym, ledger, report, sources
from grimstrade.strategies import LIVE, NOTES

# First run: fetch this much history (Kraken serves at most 720 daily bars).
BOOTSTRAP_DAYS = 700


def run(
    root: Path, now: datetime, get: sources.Get = sources.http_get, repo: Path = Path(".")
) -> list[str]:
    """One daily run. Returns the list of data problems (empty if all went well).

    `repo` is the code checkout, whose `research/` files (and research-* branches) count towards
    the number of strategies tried."""
    for rel in (ledger.DECISIONS, ledger.TRIES):
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
            added = data.append(root, sym, sources.fetch(sym, since, now, get))
            print(f"{sym}: +{added} bars")
        except Exception as e:  # noqa: BLE001 - one bad source must not stop the others
            problems.append(str(e))
            print(f"{sym}: FAILED {e}", file=sys.stderr)

    history = data.load_all(root)
    seen = data.visible_history(history, now)
    through = {s: b[-1].date.isoformat() for s, b in seen.items() if b}
    for name, decide in LIVE.items():
        ledger.register_try(root, name, NOTES[name], now)
        previous = ledger.decisions(root, name)
        if previous and previous[-1]["data_through"] == through:
            print(f"{name}: no new data since the last decision, skipped")
            continue
        weights, reason = decide(seen)
        gym.validate(weights)
        ledger.write_decision(root, now, name, weights, seen, reason)
        print(f"{name}: {weights} ({reason})")

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
    return problems


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
