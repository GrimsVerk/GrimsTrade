"""The wide-3 rules do what their cards say (research/cards/hedge-regime.md,
research/cards/attention-peak.md), and read no bar or page view after the decision."""

from __future__ import annotations

import importlib
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _mods(*names: str) -> list[Any]:
    sys.path.insert(0, str(LIB))
    try:
        return [importlib.import_module(n) for n in names]
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


def _walk(drift: float, wiggle: float, n: int = 700) -> list[float]:
    x, out = 100.0, []
    for k in range(n):
        x *= math.exp(drift + wiggle * 0.01 * (((k * 7) % 5) - 2))
        out.append(x)
    return out


def _friday_weights(rule: Any, hist: dict[str, list[Bar]]) -> dict[date, Any]:
    c, h = _mods("common", "harness")
    first, last = hist["SPY"][300].date, hist["SPY"][-1].date
    ds = h.decisions(c.weekly(rule), h.Panel(hist), first, last)
    return {d.time.date(): d.weights for d in ds if d.time.date().weekday() == 4}


def test_hedge_holds_a_falling_bond_only_while_it_hedges() -> None:
    (idea,) = _mods("idea_wide3_hedge_regime")
    stocks = _walk(0.0005, 1.0)
    for sign, held in ((-1.0, True), (1.0, False)):
        hist = {"SPY": _bars(stocks), "QQQ": _bars(stocks), "TLT": _bars(_walk(-0.0005, sign))}
        w = _friday_weights(idea.hedge, hist)
        late = [d for d in w if d > hist["SPY"][560].date]
        assert late and all(("TLT" in w[d]) == held for d in late)
        assert all(abs(w[d]["SPY"] - 1 / 3) < 1e-9 for d in late)


def test_hedge_uses_no_later_data() -> None:
    (idea,) = _mods("idea_wide3_hedge_regime")
    stocks = _walk(0.0005, 1.0)
    bond = _walk(-0.0005, -1.0)
    cut = 560
    other = bond[:cut] + [50.0 + (k % 3) for k in range(len(bond) - cut)]  # scrambled future
    a = _friday_weights(idea.hedge, {"SPY": _bars(stocks), "QQQ": _bars(stocks),
                                     "TLT": _bars(bond)})  # fmt: skip
    b = _friday_weights(idea.hedge, {"SPY": _bars(stocks), "QQQ": _bars(stocks),
                                     "TLT": _bars(other)})  # fmt: skip
    last_seen = _bars(bond)[cut - 1].date
    same = [d for d in a if d <= last_seen]
    assert len(same) > 20 and any("TLT" in a[d] for d in same)
    assert all(a[d] == b[d] for d in same)
