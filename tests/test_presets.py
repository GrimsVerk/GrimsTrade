"""Risk presets Careful and Middle: slot sizes, trend rule and swing cap, on synthetic bars."""

import math
from datetime import date, timedelta

import pytest

from grimstrade.data import UNIVERSE, Bar, History
from grimstrade.strategies import LIVE, NOTES, presets

END = date(2026, 11, 10)
ALL = ("BTC", "ETH", "SPY", "QQQ", "GLD", "TLT")


def series(sym: str, days: int, trend: float, wiggle: float) -> list[Bar]:
    """`days` calendar days ending at END, drifting by `trend` a day with a +-`wiggle` zigzag in
    log price. ETFs skip weekends."""
    out = []
    for i in range(days):
        d = END - timedelta(days=days - 1 - i)
        if UNIVERSE[sym] == "etf" and d.weekday() >= 5:
            continue
        px = 100 * math.exp(trend * i + wiggle * (-1) ** i)
        out.append(Bar(d, px, px, px, px, 1.0))
    return out


def market(trends: dict[str, float], wiggle: float = 0.001, days: int = 500) -> History:
    return {s: series(s, days, t, wiggle) for s, t in trends.items()}


def test_presets_are_live_and_registered_as_tries() -> None:
    for name in ("preset_careful", "preset_middle"):
        assert name in LIVE and name in NOTES


def test_middle_gives_each_coin_ten_percent_and_splits_the_rest_over_the_etfs() -> None:
    weights, _ = presets.middle(market(dict.fromkeys(ALL, 0.001)))
    assert weights["BTC"] == pytest.approx(0.10) and weights["ETH"] == pytest.approx(0.10)
    for s in ("SPY", "QQQ", "GLD", "TLT"):
        assert weights[s] == pytest.approx(0.20)
    assert sum(weights.values()) == pytest.approx(1.0)


def test_a_falling_asset_leaves_its_slot_in_cash() -> None:
    weights, reason = presets.middle(market({**dict.fromkeys(ALL, 0.001), "TLT": -0.001}))
    assert "TLT" not in weights and "TLT out" in reason
    assert weights["SPY"] == pytest.approx(0.20)  # the others keep their own slot size


def test_careful_holds_calm_assets_at_full_slot() -> None:
    weights, _ = presets.careful(market(dict.fromkeys(ALL, 0.001)))
    assert weights["BTC"] == pytest.approx(0.05)
    assert weights["SPY"] == pytest.approx(0.90 / 4)


def test_careful_shrinks_a_jumpy_asset_to_the_twenty_percent_cap() -> None:
    weights, _ = presets.careful(market({"BTC": 0.002}, wiggle=0.02))
    vol = 0.04 * math.sqrt(365)  # log returns zigzag about +-0.04 (plus the 0.002 drift)
    assert weights["BTC"] == pytest.approx(0.05 * 0.20 / vol, rel=0.01)


def test_middle_has_no_swing_cap() -> None:
    weights, _ = presets.middle(market({"BTC": 0.002}, wiggle=0.02))
    assert weights["BTC"] == pytest.approx(0.10)


def test_under_a_year_of_bars_stays_in_cash() -> None:
    weights, reason = presets.careful(market(dict.fromkeys(ALL, 0.001), days=300))
    assert weights == {} and "stay in cash" in reason
