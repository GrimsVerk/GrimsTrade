"""The daily run's own reconcile: is the record it just wrote what the rules give?

A light, permanent form of research/reconcile-1.md, run at the end of every daily run
(`run_daily.run`). Two checks, each a list of problem lines (the runner's mechanism: they go to
`ledger/problems.jsonl` and make the run exit 1, while the record is still committed):

1. **Fills and the stored state**, every book, the whole record. The replay's fills are checked
   against the stored bars and the cost rules without the gym's simulation code: each fill is at
   the open of a stored bar of its asset, a decision counted from before it (`ledger.in_force`),
   its price is that open x (1 +/- slippage), its fee the asset class's tier rate (by its fills in
   the 30 days before) x the traded value. Then `state/portfolio.json`, as stored, is rebuilt from
   those fills at the rule prices and fees, the stored distributions and the stored cash rate:
   cash (to the cent), units held, equity, fill count; cash and units never below zero.
2. **This run's ledger lines.** Each line the run appended holds exactly the weights its strategy
   returns on the bars stored now, as visible at the line's own time.

A failure here never stops another book or the record: each book is checked on its own and any
error becomes a problem line too.
"""

from __future__ import annotations

import bisect
import json
import traceback
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path
from typing import Any

from grimstrade import data, gym, ledger, rates
from grimstrade.data import UNIVERSE, Dividends, History, open_time, visible_history
from grimstrade.gym import Decision, Fill, Result, Strategy

# Tolerance (research/reconcile-1.md): floating point only.
REL = 1e-9
CENT = 0.005  # the state's cash and equity are written rounded to cents
# Lines per book and check; the rest are counted in one more line.
MAX_LINES = 3

PREFIX = "reconcile"


def same(a: float, b: float) -> bool:
    return abs(a - b) <= REL * max(1.0, abs(a), abs(b))


def same_cents(written: float, computed: float) -> bool:
    return abs(written - computed) <= CENT + REL * abs(computed)


def _capped(book: str, check: str, found: Sequence[str]) -> list[str]:
    out = [f"{PREFIX} {book}: {check}: {x}" for x in found[:MAX_LINES]]
    if len(found) > MAX_LINES:
        out.append(f"{PREFIX} {book}: {check}: and {len(found) - MAX_LINES} more")
    return out


# --- 1. fills and the stored state ---


def _rule_price(f: Fill, opens: Mapping[tuple[str, datetime], float], c: gym.Costs) -> float | None:
    px = opens.get((f.symbol, f.time))
    if px is None:
        return None
    return px * (1 + c.slip if f.qty > 0 else 1 - c.slip)


def fill_problems(
    fills: Sequence[Fill],
    decisions: Sequence[Decision],
    history: History,
    costs: Mapping[str, gym.Costs] = gym.COSTS,
) -> tuple[list[str], list[tuple[float, float]]]:
    """(problems, the rule's (price, fee) per fill): one problem per broken fill, its first broken
    rule. A fill off any open keeps its own price and fee in the second list."""
    opens = {
        (s, open_time(UNIVERSE[s], b.date)): b.open for s, bars in history.items() for b in bars
    }
    starts = sorted(d.time for d in decisions)
    out: list[str] = []
    ruled: list[tuple[float, float]] = []
    for i, f in enumerate(fills):
        c = costs[UNIVERSE[f.symbol]]
        what = f"{f.symbol} {f.qty:+.6g} at {f.time:%Y-%m-%d %H:%M}"
        px = _rule_price(f, opens, c)
        if px is None:
            out.append(f"{what}: not at the open of a stored bar")
            ruled.append((f.price, f.fee))
            continue
        since = f.time - gym.VOLUME_WINDOW
        volume = sum(
            abs(g.qty) * g.price
            for g in fills[:i]
            if since < g.time < f.time and UNIVERSE[g.symbol] == UNIVERSE[f.symbol]
        )
        fee = abs(f.qty) * px * c.fee_at(volume)
        ruled.append((px, fee))
        if bisect.bisect_left(starts, f.time) == 0:  # the gym orders a decision after an open
            out.append(f"{what}: no decision counted from before it")
        elif not same(f.price, px):
            out.append(f"{what}: price {f.price!r}, the rules give {px!r}")
        elif not same(f.fee, fee):
            out.append(f"{what}: fee {f.fee!r}, the rules give {fee!r}")
    return out, ruled


def _rate_on(steps: gym.Rates, known: Sequence[datetime], day: date) -> float:
    """The annual cash rate on UTC day `day`: the newest known at the day's start, never < 0."""
    i = bisect.bisect_right(known, datetime.combine(day, time(0, 0), tzinfo=UTC))
    return max(steps[i - 1][1], 0.0) if i else 0.0


def rebuild_state(
    fills: Sequence[Fill],
    ruled: Sequence[tuple[float, float]],
    decisions: Sequence[Decision],
    history: History,
    dividends: Dividends,
    cash_rates: gym.Rates,
    marked_on: date | None,
    start_cash: float = gym.START_CASH,
) -> tuple[dict[str, Any], list[str]]:
    """What `state/portfolio.json` must hold for one book, rebuilt from its fills at the rule
    prices and fees: cash and units move with each fill, a distribution pays the units held
    before its ex-date's open, and from the first decision's day each day's closing cash earns
    that day's rate / 365 (the marked day not yet: it is not over). Also returns problems: cash
    or units below zero at any point."""
    events: list[tuple[datetime, int, str, float, float]] = []  # time, order, symbol, qty, cash
    for f, (px, fee) in zip(fills, ruled, strict=True):
        flow = -f.qty * px - fee
        events.append((f.time, 1, f.symbol, f.qty, flow))
    for sym, divs in dividends.items():
        if sym not in history:
            continue
        for dv in divs:
            events.append((open_time(UNIVERSE[sym], dv.ex_date), 0, sym, 0.0, dv.amount))
    events.sort(key=lambda e: (e[0], e[1]))
    cash, units = start_cash, {s: 0.0 for s in history}
    low_cash, low_units = 0.0, 0.0
    steps = sorted(cash_rates, key=lambda r: r[0])
    known = [t for t, _ in steps]
    first = min((d.time for d in decisions), default=None)
    day = first.date() if first is not None else None
    for t, order, sym, qty, amount in events:
        while day is not None and t.date() > day and (marked_on is None or day < marked_on):
            cash += cash * _rate_on(steps, known, day) / gym.DAYS_PER_YEAR
            day += timedelta(days=1)
        if order == 0:  # a distribution: on the units held before this open
            if (paid := units[sym] * amount) > 0:
                cash += paid
        else:
            cash += amount
            units[sym] += qty
            low_cash = min(low_cash, cash)
            low_units = min(low_units, units[sym])
    while day is not None and marked_on is not None and day < marked_on:
        cash += cash * _rate_on(steps, known, day) / gym.DAYS_PER_YEAR
        day += timedelta(days=1)
    last_close = {s: bars[-1].close for s, bars in history.items() if bars}
    equity = cash + sum(q * last_close.get(s, 0.0) for s, q in units.items())
    problems = []
    if low_cash < -REL * start_cash:
        problems.append(f"cash falls below zero ({low_cash!r})")
    if low_units < -REL:
        problems.append(f"units fall below zero ({low_units!r})")
    state = {
        "cash": cash,
        "positions": {s: q for s, q in units.items() if q},
        "equity": equity if marked_on is not None else start_cash,
        "fills": len(fills),
    }
    return state, problems


def state_gaps(written: Mapping[str, Any], rebuilt: Mapping[str, Any]) -> list[str]:
    gaps = []
    for key in ("cash", "equity"):
        if not same_cents(written[key], rebuilt[key]):
            gaps.append(f"{key} {written[key]!r}, the fills give {rebuilt[key]:.4f}")
    if written["fills"] != rebuilt["fills"]:
        gaps.append(f"{written['fills']} fills, the replay has {rebuilt['fills']}")
    wp, rp = written["positions"], rebuilt["positions"]
    for s in sorted(set(wp) | set(rp)):
        if not same(wp.get(s, 0.0), rp.get(s, 0.0)):
            gaps.append(f"{s} units {wp.get(s, 0.0)!r}, the fills give {rp.get(s, 0.0)!r}")
    return gaps


def check_book(
    book: str,
    written: Mapping[str, Any] | None,
    res: Result,
    decisions: Sequence[Decision],
    history: History,
    dividends: Dividends,
    cash_rates: gym.Rates,
) -> list[str]:
    if written is None:
        return [f"{PREFIX} {book}: no row in state/portfolio.json"]
    found, ruled = fill_problems(res.fills, decisions, history)
    out = _capped(book, "fill", found)
    marked = date.fromisoformat(written["marked_on"]) if written.get("marked_on") else None
    rebuilt, low = rebuild_state(
        res.fills, ruled, decisions, history, dividends, cash_rates, marked, res.start_cash
    )
    out += _capped(book, "state", low + state_gaps(written, rebuilt))
    return out


def check_state(root: Path, results: Mapping[str, Result]) -> list[str]:
    """Check 1 for every book: `results` are the replay the run scored (`report.live_results`),
    everything else is read back from the record under `root`."""
    try:
        state = json.loads((root / "state" / "portfolio.json").read_text())
        history = data.load_all(root)
        dividends = data.load_dividends(root)
        cash_rates = rates.steps(rates.load(root), live=True)
        by_book: dict[str, list[Decision]] = {}
        for t, row in ledger.in_force(root)[0]:
            by_book.setdefault(row["strategy"], []).append(Decision(t, row["weights"]))
    except Exception as e:  # noqa: BLE001 - the check must never stop the run
        return [f"{PREFIX}: could not read the record: {e!r}"]
    out = [
        f"{PREFIX} {b}: in the state but not in the replay"
        for b in sorted(set(state) - set(results))
    ]
    for book, res in sorted(results.items()):
        try:
            out += check_book(
                book, state.get(book), res, by_book.get(book, []), history, dividends, cash_rates
            )
        except Exception as e:  # noqa: BLE001 - one book's failure must not hide the others
            where = traceback.extract_tb(e.__traceback__)[-1]
            out.append(f"{PREFIX} {book}: the check raised {e!r} (line {where.lineno})")
    return out


# --- 2. this run's ledger lines ---


def check_lines(
    rows: Sequence[Mapping[str, Any]], history: History, strategies: Mapping[str, Strategy]
) -> list[str]:
    """Each ledger line in `rows` against its strategy re-run on `history` as visible at the
    line's own time."""
    out = []
    for r in rows:
        book = r.get("strategy", "?")
        try:
            got, _ = strategies[book](visible_history(history, ledger.parse_time(r["time"])))
            wrote = r["weights"]
            off = sorted(
                s for s in set(got) | set(wrote) if not same(got.get(s, 0.0), wrote.get(s, 0.0))
            )
            if off:
                gaps = ", ".join(f"{s} {wrote.get(s, 0.0)!r} vs {got.get(s, 0.0)!r}" for s in off)
                out.append(f"{PREFIX} {book}: ledger line {r['time']}: weights {gaps} (strategy)")
        except Exception as e:  # noqa: BLE001 - one line's failure must not hide the others
            out.append(f"{PREFIX} {book}: ledger line {r.get('time')}: the check raised {e!r}")
    return out
