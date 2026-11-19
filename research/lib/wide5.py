"""Glue between the wide-5 rules (`wide5_rules.py`) and the harness: the parsed auction file,
the idle-cash overlay and the event-study table shared by both cards."""

from __future__ import annotations

import csv
from collections.abc import Callable, Sequence
from datetime import date

import common as c
import macro
import numpy as np
import wide1 as w
import wide4_rules as r4
import wide5_rules as r

_auctions: list[r.Auction] = []


def auctions() -> list[r.Auction]:
    """The nominal fixed-rate auctions parsed by `wide5_auctions.py`."""
    if not _auctions:
        path = macro.cache_root() / "derived" / "wide-5" / "auctions.csv"
        with path.open(newline="") as f:
            for x in csv.DictReader(f):
                _auctions.append(r.Auction(
                    x["cusip"], int(x["years"]), date.fromisoformat(x["announced"]),
                    date.fromisoformat(x["auction"]), date.fromisoformat(x["issue"]),
                    date.fromisoformat(x["maturity"]), float(x["accepted"]),
                    float(x["comp"]) if x["comp"] else None,
                    float(x["dealer"]) if x["dealer"] else None,
                ))  # fmt: skip
    return _auctions


def overlay(bond: str, on: set[date]) -> c.ResearchStrategy:
    """`tsmom12` plus the idle cash in `bond` after the close of the sessions in `on`."""
    base = c.weekly(c.slots(c.tsmom_signal))

    def f(view: c.View) -> c.Weights:
        held = base(view)
        last = w.last_session(view, bond)
        if last is None or last not in on or not c.eligible(view, bond):
            return held
        idle = 1.0 - sum(held.values())
        if idle <= 1e-9:
            return held
        out = dict(held)
        out[bond] = out.get(bond, 0.0) + idle
        return out

    return f


def study_rows(
    label: str,
    events: Sequence[tuple[date, float, bool, float]],
    periods: Sequence[tuple[str, date, date]],
    names: tuple[str, str],
) -> tuple[list[str], dict[str, float]]:
    """Table rows from events (date, dose, in the traded group, excess in log units): per period
    the two groups' mean (t, count) in bps and the slope of the excess on the dose (HC1 t)."""
    lines, got = [], {}
    for name, lo, hi in periods:
        sub = [e for e in events if lo <= e[0] <= hi and not np.isnan(e[3])]
        a = np.array([e[3] for e in sub if e[2]]) * 1e4
        b = np.array([e[3] for e in sub if not e[2]]) * 1e4
        x = np.array([e[1] for e in sub])
        y = np.array([e[3] for e in sub]) * 1e4
        sl, t = r4.hc1_slope(x, y)
        lines.append(
            f"| {label} | {name} | {len(a)} | {a.mean():+.1f} ({w.tstat(a):+.2f}) | {len(b)} | "
            f"{b.mean():+.1f} ({w.tstat(b):+.2f}) | {sl:+.2f} | {t:+.2f} |"
        )
        got[f"{name}:{names[0]}"], got[f"{name}:{names[1]}"] = float(a.mean()), float(b.mean())
        got[f"{name}:slope"], got[f"{name}:t"] = sl, t
    return lines, got


def reading(got: dict[str, float], halves: tuple[str, str], hi: str, lo: str) -> tuple[bool, str]:
    ok_a = got["all:slope"] > 0 and got["all:t"] >= 2
    ok_b = got[f"all:{hi}"] > got[f"all:{lo}"]
    ok_c = got[f"{halves[0]}:slope"] > 0 and got[f"{halves[1]}:slope"] > 0
    ok = ok_a and ok_b and ok_c
    yn: Callable[[bool], str] = lambda v: "yes" if v else "no"  # noqa: E731
    return ok, (
        f"(a) slope > 0 with t >= 2 {yn(ok_a)}; (b) traded-group mean above the other "
        f"{yn(ok_b)}; (c) slope positive in both halves {yn(ok_c)}. Mechanism "
        f"**{'supported' if ok else 'not supported'}**."
    )
