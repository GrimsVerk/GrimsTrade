"""Post-hoc descriptions for run wide-1, written after the four verdicts, to see where each
result comes from. Not strategies: nothing here was selectable, nothing is logged in tries.md.

    uv run --with numpy python research/lib/wide1_posthoc.py

Train bars only. A session's return runs from its open to the next session's open (what the
gym earns for holding it)."""

from __future__ import annotations

import bisect
import csv
import math
from datetime import date

import common as c
import idea_wide1_rebalance as rebalance
import macro
import numpy as np
import timing
import wide1 as w
import wide1_rules as rules
from harness import load_history

OFFSETS = range(-9, 6)
KINDS = {"30-year": (25, 99), "20-year": (19, 25), "10-year": (9, 11), "7-year": (6, 8)}
PAIRS = [("TLT", "30-year"), ("TLT", "20-year"), ("TLT", "10-year"), ("TLT", "7-year"),
         ("IEF", "10-year"), ("IEF", "7-year")]  # fmt: skip
SPANS = [("2003-2012", date(2003, 8, 1), date(2012, 12, 31)),
         ("2013-2019", date(2013, 1, 1), date(2019, 12, 31)),
         ("2020-2025", date(2020, 1, 1), date(2025, 12, 31))]  # fmt: skip
GROUP = {"TLT": "long", "IEF": "mid"}


def auction_days(kind: str) -> list[date]:
    lo, hi = KINDS[kind]
    path = macro.cache_root() / "derived" / "wide-1" / "auctions.csv"
    with path.open(newline="") as f:
        days = {date.fromisoformat(r["auction"]) for r in csv.DictReader(f)
                if lo <= rules.term_years(r["term"]) < hi}  # fmt: skip
    return sorted(d for d in days if date(2003, 8, 1) <= d <= c.TRAIN_END)


def cell(x: np.ndarray) -> str:
    return f"{x.mean() * 1e4:+.1f} ({w.tstat(x):+.1f})" if len(x) > 2 else "-"


def session_returns(bars) -> tuple[list[date], np.ndarray]:  # type: ignore[no-untyped-def]
    days = [b.date for b in bars]
    return days, np.array([bars[i + 1].open / bars[i].open - 1 for i in range(len(bars) - 1)])


def auction_profile(hist) -> list[str]:  # type: ignore[no-untyped-def]
    out = ["## auction-concession: each session around each kind of auction", ""]
    out += [
        "Mean return per session in bps (t). Session 0 is the auction day; the card's rule is "
        "out for sessions -4 .. 0.",
        "",
    ]
    head = "| ETF | Auction | Events |" + "".join(f" {k:+d} |" for k in OFFSETS)
    head += " Sum -4..0 | Sum +1..+5 | Sum -9..-5 |"
    out += [head, "|---|---|---:|" + "---:|" * (len(OFFSETS) + 3)]
    eras = ["| ETF | Auction |" + "".join(f" {n}: sum -4..0 (events) |" for n, _, _ in SPANS)]
    eras += ["|---|---|" + "---:|" * len(SPANS)]
    k0 = -OFFSETS[0]
    for sym, kind in PAIRS:
        days, ret = session_returns(hist[sym])
        rows = []
        for a in auction_days(kind):
            j = bisect.bisect_left(days, a)
            if j + OFFSETS[0] >= 0 and j + OFFSETS[-1] < len(ret):
                rows.append((a, [ret[j + k] for k in OFFSETS]))
        m = np.array([r for _, r in rows])
        line = f"| {sym} | {kind} | {len(rows)} |"
        line += "".join(f" {cell(m[:, i])} |" for i in range(m.shape[1]))
        pre, post = m[:, k0 - 4 : k0 + 1].sum(1), m[:, k0 + 1 : k0 + 6].sum(1)
        early = m[:, k0 - 9 : k0 - 4].sum(1)
        out.append(line + f" {cell(pre)} | {cell(post)} | {cell(early)} |")
        era_line = f"| {sym} | {kind} |"
        for _, lo, hi in SPANS:
            sel = np.array([sum(r[k0 - 4 : k0 + 1]) for a, r in rows if lo <= a <= hi])
            era_line += f" {cell(sel)} ({len(sel)}) |"
        eras.append(era_line)
    return [*out, "", "The card's window (sessions -4 .. 0) by period:", "", *eras, ""]


def auction_by_period(hist) -> list[str]:  # type: ignore[no-untyped-def]
    """The card's own in/out split, period by period (the full-sample split mixes periods with
    different shares of out days and different bond markets)."""
    out = ["## auction-concession: the rule's days out and days in, period by period", ""]
    out += ["| ETF | Period | Days in | bps a day in | Days out | bps a day out | Share out | "
            "Welch t (in minus out) |", "|---|---|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    for sym in ("TLT", "IEF"):
        days, ret = session_returns(hist[sym])
        gone = rules.out_days(w.calendar(sym), w.auctions(GROUP[sym]))
        for name, lo, hi in [*SPANS, ("all", SPANS[0][1], SPANS[-1][2])]:
            ins, outs = [], []
            for i in range(len(days) - 2):
                if lo <= days[i] <= hi:  # decided after the close of days[i]: session i + 1
                    (outs if days[i] in gone else ins).append(ret[i + 1])
            a, b = np.array(ins), np.array(outs)
            out.append(
                f"| {sym} | {name} | {len(a)} | {a.mean() * 1e4:+.1f} | {len(b)} | "
                f"{b.mean() * 1e4:+.1f} | {len(b) / (len(a) + len(b)):.0%} | "
                f"{timing.welch(a, b):+.2f} |"
            )
    return [*out, ""]


def rebalance_legs(hist) -> list[str]:  # type: ignore[no-untyped-def]
    """Which leg carries the month-end spread: the stock leg, the bond leg, or both."""
    cal = w.calendar("SPY")
    out = ["## rebalance-pressure: the two legs of the month-end spread", ""]
    out += [
        "Months the rule acted in (|g| >= 2%). Returns over sessions T-4 .. T, in bps (t), "
        "signed so that positive is what the card predicts: the month's leader falls, the "
        "month's loser rises.",
        "",
        "| Period | Leader | Months | Leader's side, sign flipped | Loser's side | Spread |",
        "|---|---|---:|---:|---:|---:|",
    ]
    closes = {s: {b.date: b.close for b in hist[s]} for s in ("SPY", "TLT")}
    ev = []
    for t in range(6, len(cal) - 5):
        if cal[t + 1].month == cal[t].month or not date(2003, 8, 1) <= cal[t] <= c.TRAIN_END:
            continue
        refs = rules.month_refs(cal, t)
        if refs is None:
            continue
        m, p = refs
        if any(cal[i] not in closes[s] for s in closes for i in (m, p)):
            continue
        g = math.log(closes["SPY"][cal[m]] / closes["SPY"][cal[p]]) - math.log(
            closes["TLT"][cal[m]] / closes["TLT"][cal[p]]
        )
        spy = w.open_to_open(hist["SPY"], cal[t - 4], cal[t + 1])
        tlt = w.open_to_open(hist["TLT"], cal[t - 4], cal[t + 1])
        if abs(g) >= rebalance.THRESHOLD and not (math.isnan(spy) or math.isnan(tlt)):
            ev.append((cal[t], g, spy, tlt))
    spans = [("2003-2013", date(2003, 1, 1), date(2013, 12, 31)),
             ("2014-2025", date(2014, 1, 1), date(2025, 12, 31))]  # fmt: skip
    for name, lo, hi in spans:
        for who, sel in (
            ("stocks", [e for e in ev if lo <= e[0] <= hi and e[1] > 0]),
            ("bonds", [e for e in ev if lo <= e[0] <= hi and e[1] < 0]),
        ):
            if len(sel) < 3:
                continue
            lead = np.array([-(e[2] if who == "stocks" else e[3]) for e in sel])
            lose = np.array([(e[3] if who == "stocks" else e[2]) for e in sel])
            out.append(
                f"| {name} | {who} | {len(sel)} | {cell(lead)} | {cell(lose)} | "
                f"{cell(lead + lose)} |"
            )
    return [*out, ""]


def main() -> None:
    hist = load_history("train", True, ["TLT", "IEF", "SPY"])
    out = ["# wide-1: where the results come from (post hoc)", ""]
    out += [
        "Written after the four verdicts. Descriptive only: nothing here was selectable and "
        "nothing is logged in `tries.md`. A reading taken from these tables is a hypothesis for "
        "a new card, not a result. Train bars only.",
        "",
    ]
    out += auction_by_period(hist)
    out += auction_profile(hist)
    out += rebalance_legs(hist)
    c.write_result("wide-1-posthoc", "\n".join(out))


if __name__ == "__main__":
    main()
