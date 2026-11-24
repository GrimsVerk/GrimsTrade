"""The own-vol 70% paper book (`strategies/own_vol.py`): no look-ahead, the sizing of the research
rule it copies (risk-menu-3, `research/lib/riskmenu3_run.py`), and no leverage."""

from __future__ import annotations

import importlib
import math
import random
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from grimstrade import gym
from grimstrade.data import UNIVERSE, Bar, History, visible_history
from grimstrade.strategies import LIVE, NOTES, own_vol

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
ALL = ("BTC", "ETH", "SPY", "QQQ", "GLD", "TLT")
FIRST, LAST = date(2019, 1, 1), date(2023, 12, 31)


def _lib() -> tuple[Any, Any, Any, Any]:
    sys.path.insert(0, str(LIB))
    try:
        mods = ("riskmenu3_run", "lstrend2_run", "common", "harness")
        return tuple(importlib.import_module(m) for m in mods)  # type: ignore[return-value]
    finally:
        sys.path.remove(str(LIB))


def market(seed: int = 7, first: date = FIRST, last: date = LAST) -> History:
    """Random walks with regimes, so `tsmom12` goes in and out of each asset. ETFs skip
    weekends. Seeded: the same bars on every run."""
    rng = random.Random(seed)
    out: dict[str, list[Bar]] = {}
    for s in ALL:
        px, d = 100.0, first
        bars: list[Bar] = []
        drift = rng.uniform(-0.0006, 0.0012)
        vol = 0.04 if UNIVERSE[s] == "crypto" else 0.012
        while d <= last:
            if d.day == 1 and rng.random() < 0.15:
                drift = rng.uniform(-0.002, 0.002)
            if UNIVERSE[s] == "crypto" or d.weekday() < 5:
                px *= math.exp(drift + vol * rng.gauss(0, 1) * (2 if d.year == 2022 else 1))
                bars.append(Bar(d, px, px, px, px, 1.0))
            d += timedelta(days=1)
        out[s] = bars
    return out


def at(d: date) -> datetime:
    return datetime.combine(d, gym.DECIDE_AT, tzinfo=UTC)


def share(history: History) -> float:
    """The book's share of `tsmom12` in a decision: its weights over `tsmom12`'s."""
    weights, _ = own_vol.own_vol(0.70, ())(history)
    sleeve = own_vol.Sleeve(history)
    assert sleeve.today is not None
    base = sleeve.held(sleeve.today)
    return sum(weights.values()) / sum(base.values())


H = market()
BOOK = own_vol.own_vol(0.70, ())  # no prior: the warm-up ends 24 sigmas after the first, 2023


def test_it_is_a_live_book_under_a_new_name_with_a_note() -> None:
    assert LIVE["own_vol_70"] is own_vol.decide
    assert "own-vol" in NOTES["own_vol_70"] and "no look-ahead" in NOTES["own_vol_70"]


# --- no look-ahead ---


def test_bars_after_the_decision_do_not_change_it() -> None:
    t = at(date(2023, 6, 14))
    seen = visible_history(H, t)
    weights, reason = BOOK(seen)
    assert "k " in reason  # past the warm-up: the k path is the one checked
    rng = random.Random(1)
    later = {
        s: [b if b in seen[s] else Bar(b.date, *(b.close * rng.uniform(0.3, 3),) * 4, 1.0)
            for b in bars]
        for s, bars in H.items()
    }  # fmt: skip
    assert visible_history(later, t) == seen
    assert BOOK(visible_history(later, t)) == (weights, reason)


def test_a_backtest_over_changed_futures_agrees_up_to_the_change() -> None:
    cut = date(2023, 6, 20)
    crash = {s: [b if b.date < cut else Bar(b.date, *(b.close / 2,) * 4, 1.0) for b in bars]
             for s, bars in H.items()}  # fmt: skip
    a = gym.backtest(BOOK, H, date(2023, 5, 25), date(2023, 7, 10))
    b = gym.backtest(BOOK, crash, date(2023, 5, 25), date(2023, 7, 10))
    before = [x for x in a if x.time.date() < cut - timedelta(days=1)]
    assert before == b[: len(before)]
    assert a != b  # the crash does reach the later decisions


def test_the_share_is_fixed_for_the_month_and_the_weights_for_the_week() -> None:
    june = [share(visible_history(H, at(date(2023, 6, d)))) for d in (1, 9, 17, 30)]
    assert june == pytest.approx([june[0]] * 4, abs=1e-12)
    assert share(visible_history(H, at(date(2023, 7, 3)))) != pytest.approx(june[0])
    sleeve = own_vol.Sleeve(visible_history(H, at(date(2023, 6, 14))))  # a Wednesday
    assert sleeve.held(date(2023, 6, 14)) == sleeve.on_friday(date(2023, 6, 9))


# --- the research harness's sizing ---


def test_friday_weights_are_the_research_tsmom12() -> None:
    _r3, _l2, c, harness = _lib()
    panel = harness.Panel(H)
    research = c.slots(c.tsmom_signal)
    sleeve = own_vol.Sleeve(H)
    held_some = 0
    for f in sleeve.fridays:
        want = research(panel.view(harness.decide_time(f)))
        got = sleeve.on_friday(f)
        assert got.keys() == want.keys(), f
        assert all(got[s] == pytest.approx(want[s]) for s in got)
        held_some += 0 < len(got) < len(ALL)
    assert held_some > 50  # the fixture moves assets in and out


def test_sigma_is_the_research_sleeve_sigma() -> None:
    _r3, l2, _c, _h = _lib()
    sleeve = own_vol.Sleeve(H)
    assert sleeve.start is not None
    research = l2.Sleeve(sleeve.ret, sleeve.start, lambda d: 1.0, lambda d: 1.0)
    m, checked = date(2019, 2, 1), 0
    while m <= LAST:
        end = m - timedelta(days=1)
        want, got = research.sigma(end), sleeve.sigma(end)
        if math.isnan(want):
            assert got is None
        else:
            assert got == pytest.approx(want, rel=1e-12)
            checked += 1
        m = own_vol.next_month(m)
    assert checked >= 30


def research_plan(r3: Any, sigma_of: dict[str, float]) -> dict[str, float | None]:
    """risk-menu-3's own month-by-month share (`vt_expanding`), fed the given sigmas."""
    caught: list[Any] = []

    class Fake:
        def sigma(self, end: date) -> float:
            return sigma_of.get(own_vol.month(end + timedelta(days=1)), math.nan)

    real = r3.rm.mix
    r3.rm.mix = lambda s1, s2, tgt, a, held: caught.append(tgt)
    try:
        r3.vt_expanding(Fake(), 0.70, lambda d: 0)
    finally:
        r3.rm.mix = real
    keep = object()
    out: dict[str, float | None] = {}
    for d in r3.rm.months_in(*r3.W):
        a = caught[0](d, keep)[0]
        out[own_vol.month(d)] = None if a is keep else a
    return out


def test_monthly_share_matches_risk_menu_3_including_warm_up_and_a_zero_sigma() -> None:
    r3, _l2, _c, _h = _lib()
    rng = random.Random(3)
    sig: dict[str, float] = {}
    m = date(2001, 1, 1)
    for i in range(60):
        sig[own_vol.month(m)] = 0.0 if i in (30, 31) else rng.uniform(0.05, 0.4)
        m = own_vol.next_month(m)
    sig["2001-01"] = math.nan  # a month whose sigma is unknown
    want = research_plan(r3, sig)
    mine = {k: (None if math.isnan(v) else v) for k, v in sig.items()}
    prev = 0.70
    for month in sorted(sig):
        got, _how = own_vol.plan(mine, month)
        w = want[month]
        assert got == pytest.approx(prev if w is None else w, rel=1e-12), month
        prev = got
    assert len({round(want[k] or 0, 6) for k in sig}) > 20  # the rule did size, not just 70%


def test_book_sizing_on_the_fixture_matches_the_research_rule() -> None:
    r3, l2, _c, _h = _lib()
    sleeve = own_vol.Sleeve(H)
    assert sleeve.start is not None
    research = l2.Sleeve(sleeve.ret, sleeve.start, lambda d: 1.0, lambda d: 1.0)
    sig, m = {}, date(2019, 2, 1)
    while m <= LAST:
        sig[own_vol.month(m)] = research.sigma(m - timedelta(days=1))
        m = own_vol.next_month(m)
    want = research_plan(r3, sig)
    for d in (date(2023, 1, 20), date(2023, 6, 14), date(2023, 12, 28)):
        assert share(visible_history(H, at(d))) == pytest.approx(want[own_vol.month(d)])
    assert share(visible_history(H, at(date(2022, 6, 14)))) == pytest.approx(0.70)  # warm-up


def test_the_prior_gives_the_research_k() -> None:
    r3, _l2, _c, _h = _lib()
    sigmas = [s for _, s in own_vol.PRIOR]
    assert len(sigmas) == 362 and own_vol.PRIOR[-1][0] == "2025-10"
    k = own_vol.solve_k(tuple(sigmas), 0.70)
    assert k == pytest.approx(r3.solve_k(sigmas, 0.70), rel=1e-12)
    assert k == pytest.approx(0.083779, abs=2e-6)  # vt_expanding's k on 2025-10-01


def test_the_live_book_uses_the_prior_from_its_first_known_sigma() -> None:
    live = market(first=date(2024, 12, 11), last=date(2027, 3, 31))
    early, reason = own_vol.decide(visible_history(live, at(date(2026, 11, 20))))
    assert "no sigma yet" in reason  # 52 weeks of the book's own tsmom12 not stored yet
    weights, reason = own_vol.decide(visible_history(live, at(date(2027, 2, 10))))
    assert "k 0.08" in reason and "warm-up" not in reason


# --- no leverage ---


def test_a_calm_sleeve_is_capped_at_the_full_tsmom12_book() -> None:
    got, how = own_vol.plan({"2030-01": 0.001}, "2030-01", prior=(("2029-12", 0.3),) * 30)
    assert got == 1.0 and "k " in how  # k / sigma is far above 1
    calm = own_vol.own_vol(0.70, (("2000-01", 50.0),) * 30)  # k far above any sigma here
    seen = visible_history(H, at(date(2023, 6, 14)))
    weights, reason = calm(seen)
    gym.validate(weights)
    sleeve = own_vol.Sleeve(seen)
    assert sleeve.today is not None
    assert weights == pytest.approx(sleeve.held(sleeve.today))
    assert sum(weights.values()) <= 1 + 1e-12 and "share 100%" in reason
