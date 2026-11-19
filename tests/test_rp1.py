"""The rp-1 rule (research/lib/rp1_rule.py) does what its card says (research/rp-1.md): the
protocol's inverse-vol slot sizes, with `where-vol`'s yes/no deciding which slots are filtered,
and no bar after the decision is read."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _lib() -> tuple[Any, Any, Any]:
    sys.path.insert(0, str(LIB))
    try:
        return (
            importlib.import_module("rp1_rule"),
            importlib.import_module("common"),
            importlib.import_module("harness"),
        )
    finally:
        sys.path.remove(str(LIB))


def _bars(closes: list[float], start: date = date(2018, 1, 1)) -> list[Bar]:
    out, d = [], start
    for x in closes:
        while d.weekday() >= 5:
            d += timedelta(days=1)
        out.append(Bar(d, x, x, x, x, 1.0))
        d += timedelta(days=1)
    return out


def _hist() -> dict[str, list[Bar]]:
    # SPY: calm rise, then a fall (its trend turns off); TLT: a choppy, more volatile rise
    spy = [100.0 * 1.001**k for k in range(400)] + [
        100.0 * 1.001**400 * 0.998**k for k in range(300)
    ]
    tlt = [100.0 * 1.0005**k * (1.02 if k % 2 else 0.98) for k in range(700)]
    return {"SPY": _bars(spy), "TLT": _bars(tlt)}


class _Fixed:
    def __init__(self, keep: bool):
        self.keep = keep

    def answers(self, panel: Any, refit: object) -> dict[str, bool]:
        return {s: self.keep for s in panel.syms}


def _fridays(hist: dict[str, list[Bar]]) -> list[date]:
    return [b.date for b in hist["SPY"][300:] if b.date.weekday() == 4]


def test_all_no_is_inverse_vol_and_all_yes_filters_it() -> None:
    rule, c, h = _lib()
    hist = _hist()
    panel = h.Panel(hist)
    off_seen = False
    for fri in _fridays(hist):
        view = panel.view(h.decide_time(fri))
        iv = c.inverse_vol(view)
        assert math.isclose(sum(iv.values()), 1.0)
        assert rule.where_rp(_Fixed(False))(view) == iv
        held = rule.where_rp(_Fixed(True))(view)
        for s, x in iv.items():
            on = c.tsmom_signal(view, s)
            assert held.get(s, 0.0) == (x if on else 0.0)
            off_seen |= not on
        assert iv["SPY"] > iv["TLT"]  # the calmer asset gets the larger slot
    assert off_seen


def test_no_bar_after_the_decision_is_read() -> None:
    rule, _, h = _lib()
    hist = _hist()
    cut = hist["SPY"][550].date
    changed = {
        s: [b if b.date <= cut else Bar(b.date, 1, 1, 1, 1, 1) for b in v] for s, v in hist.items()
    }
    a, b = h.Panel(hist), h.Panel(changed)
    for fri in [d for d in _fridays(hist) if d <= cut]:
        t = h.decide_time(fri)
        assert rule.where_rp(_Fixed(True))(a.view(t)) == rule.where_rp(_Fixed(True))(b.view(t))
