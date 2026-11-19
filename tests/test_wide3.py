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


def _mania(n: int = 700, start: int = 450) -> Any:
    """Flat attention, then a surge that rises for 20 days and falls back over 60."""
    import numpy as np

    v = np.full(n, 100.0)
    for k in range(20):
        v[start + k] = 100.0 + 50.0 * (k + 1)
    for k in range(60):
        v[start + 20 + k] = max(1100.0 - 15.0 * k, 100.0)
    return v


def test_attention_holds_on_the_rise_and_leaves_after_the_peak() -> None:
    (idea,) = _mods("idea_wide3_attention_peak")
    first = date(2018, 1, 1)
    views = {"BTC": (first, _mania())}
    rising = first + timedelta(days=450 + 15)  # sees days up to 464: still rising
    after = first + timedelta(days=450 + 35)  # 15 days past the peak, surge still on
    late = first + timedelta(days=690)  # the epidemic is over
    assert not idea.out_of_mania(views, "BTC", rising)
    assert idea.out_of_mania(views, "BTC", after)
    assert not idea.out_of_mania(views, "BTC", late)
    assert not idea.out_of_mania(views, "ETH", after)  # no data: the twin


def test_attention_uses_no_view_of_the_decision_day_or_later() -> None:
    (idea,) = _mods("idea_wide3_attention_peak")
    first = date(2018, 1, 1)
    v = _mania()
    day = first + timedelta(days=480)
    other = v.copy()
    other[480:] = 1e6  # a scrambled future from the decision day on
    for d in (day, day - timedelta(days=10), day - timedelta(days=25)):
        a = idea.out_of_mania({"BTC": (first, v)}, "BTC", d)
        b = idea.out_of_mania({"BTC": (first, other)}, "BTC", d)
        assert a == b


def test_attention_rule_only_drops_coin_slots() -> None:
    (idea,) = _mods("idea_wide3_attention_peak")
    up = [50.0 + 0.1 * k for k in range(700)]
    hist = {"SPY": _bars(up), "BTC": _bars(up)}
    first = hist["SPY"][0].date
    views = {"BTC": (first, _mania(1200, 500)), "SPY": (first, _mania(1200, 500))}
    w = _friday_weights(idea.peak_rule(views), hist)
    twin = _friday_weights(_mods("common")[0].slots(_mods("common")[0].tsmom_signal), hist)
    assert any("BTC" not in w[d] and "BTC" in twin[d] for d in w)
    assert all("SPY" in w[d] for d in w if "SPY" in twin[d])


def test_opex_pin_adds_idle_cash_only_in_the_expiry_week() -> None:
    idea, c = _mods("idea_wide3_opex_pin", "common")
    up = [50.0 + 0.1 * k for k in range(700)]
    down = [100.0 - 0.05 * k for k in range(700)]
    hist = {"SPY": _bars(down), "QQQ": _bars(up), "TLT": _bars(down)}
    mine = _friday_weights(idea.pin, hist)
    twin = _friday_weights(c.slots(c.tsmom_signal), hist)
    pre = [d for d in mine if idea.is_third_friday(d + timedelta(days=7))]
    other = [d for d in mine if d not in pre]
    assert pre and other
    for d in pre:  # QQQ in trend (1/3), the idle 2/3 split over SPY and QQQ
        assert abs(mine[d]["QQQ"] - (1 / 3 + 1 / 3)) < 1e-9
        assert abs(mine[d]["SPY"] - 1 / 3) < 1e-9 and "TLT" not in mine[d]
    assert all(mine[d] == twin[d] for d in other)


def test_opex_pin_uses_no_later_data() -> None:
    (idea,) = _mods("idea_wide3_opex_pin")
    up = [50.0 + 0.1 * k for k in range(700)]
    cut = 500
    other = up[:cut] + [5.0 + (k % 7) for k in range(len(up) - cut)]
    a = _friday_weights(idea.pin, {"SPY": _bars(up), "QQQ": _bars(_walk(-0.001, 1.0))})
    b = _friday_weights(idea.pin, {"SPY": _bars(other), "QQQ": _bars(_walk(-0.001, 1.0))})
    last_seen = _bars(up)[cut - 1].date
    same = [d for d in a if d <= last_seen]
    assert len(same) > 20 and all(a[d] == b[d] for d in same)
