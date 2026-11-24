"""The wide-1 rules (research/lib/wide1_rules.py) do what their cards in research/cards/ say.

- vol-echo: "in" for exactly three decisions, starting the day before a shock leaves the
  window, and never from data after the decision.
- auction-concession: out after the closes of A-5 .. A-1, never before the announcement.
- rebalance-pressure: the tilt is on after the closes of T-5 .. T-1, the rebound after T and
  the first two sessions of the next month; a tilt never adds an asset the base does not hold.
- contagion-catchup: an asset whose relative moved and which did not gets the high signal.
"""

from __future__ import annotations

import importlib
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _rules() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide1_rules")
    finally:
        sys.path.remove(str(LIB))


def _weekdays(start: date, n: int) -> list[date]:
    out: list[date] = []
    d = start
    while len(out) < n:
        if d.weekday() < 5:
            out.append(d)
        d += timedelta(days=1)
    return out


def test_echo_holds_three_sessions_when_the_shock_leaves() -> None:
    r = _rules()
    lr = np.full(60, 0.001)
    lr[5] = 0.05  # one shock
    held = r.echo_in(lr, 21, 0.20)
    # the shock leaves the 21-return window at the close after return 25: decisions 26, 27, 28
    assert list(np.flatnonzero(held)) == [26, 27, 28]


def test_echo_uses_no_later_data() -> None:
    r = _rules()
    rng = np.random.default_rng(0)
    lr = rng.standard_t(3, 400) * 0.01
    other = lr.copy()
    other[300:] = rng.standard_t(3, 100) * 0.05  # scramble the future
    a, b = r.echo_in(lr, 21, 0.20), r.echo_in(other, 21, 0.20)
    assert np.array_equal(a[:301], b[:301])


def test_auction_group_and_terms() -> None:
    r = _rules()
    assert r.term_years("29-Year 9-Month") == 29.75
    assert r.auction_group("Bond", "30-Year", "No", "No") == "long"
    assert r.auction_group("Bond", "20-Year", "No", "No") == "long"
    assert r.auction_group("Note", "10-Year", "No", "No") == "mid"
    assert r.auction_group("Note", "6-Year 11-Month", "No", "No") == "mid"
    assert r.auction_group("Note", "5-Year", "No", "No") is None
    assert r.auction_group("Bond", "30-Year", "Yes", "No") is None  # TIPS
    assert r.auction_group("Note", "2-Year", "No", "Yes") is None  # floater


def test_auction_out_days_respect_the_announcement() -> None:
    r = _rules()
    cal = _weekdays(date(2024, 1, 1), 40)
    auction = cal[20]
    # announced long before: out after the closes of A-5 .. A-1
    assert r.out_days(cal, [(cal[0], auction)]) == set(cal[15:20])
    # announced three sessions before: nothing earlier than the announcement
    assert r.out_days(cal, [(cal[17], auction)]) == set(cal[17:20])
    # an auction on a closed day counts as the next session
    saturday = auction + timedelta(days=(5 - auction.weekday()) % 7)
    nxt = next(i for i, d in enumerate(cal) if d > saturday)
    assert r.out_days(cal, [(cal[0], saturday)]) == set(cal[nxt - 5 : nxt])


def test_month_phase_windows() -> None:
    r = _rules()
    cal = _weekdays(date(2024, 1, 1), 70)  # January to early April 2024
    t = max(i for i, d in enumerate(cal) if d.month == 2)  # last session of February
    for k in range(1, 6):
        assert r.month_phase(cal, t - k) == ("pressure", t)
    assert r.month_phase(cal, t - 6) is None
    assert r.month_phase(cal, t) == ("rebound", t)
    assert r.month_phase(cal, t + 1) == ("rebound", t)
    assert r.month_phase(cal, t + 2) == ("rebound", t)
    assert r.month_phase(cal, t + 3) is None
    m, p = r.month_refs(cal, t)
    assert m == t - 5 and cal[p].month == 1 and cal[p + 1].month == 2
    # the calendar ends inside the last month: its end is unknown, so no phase
    assert r.month_phase(cal, len(cal) - 1) is None


def test_tilt_moves_half_and_never_adds_an_asset() -> None:
    r = _rules()
    base = {"SPY": 0.2, "QQQ": 0.2, "TLT": 0.2, "GLD": 0.2}
    w = r.tilt(base, ["SPY", "QQQ"], ["TLT"])
    assert np.isclose(w["SPY"], 0.1) and np.isclose(w["QQQ"], 0.1) and np.isclose(w["TLT"], 0.4)
    assert np.isclose(sum(w.values()), sum(base.values())) and w["GLD"] == 0.2
    # the receiving side is not held by the base: the freed weight stays in cash
    w2 = r.tilt({"SPY": 0.2, "QQQ": 0.2}, ["SPY", "QQQ"], ["TLT"])
    assert "TLT" not in w2 and np.isclose(sum(w2.values()), 0.2)
    # the leader is not held: nothing changes
    assert r.tilt({"TLT": 0.2}, ["SPY", "QQQ"], ["TLT"]) == {"TLT": 0.2}


def test_catchup_points_at_the_asset_that_has_not_moved() -> None:
    r = _rules()
    rng = np.random.default_rng(1)
    common = rng.normal(0, 0.01, 252)
    daily = np.column_stack(
        [
            common + rng.normal(0, 0.002, 252),
            common + rng.normal(0, 0.002, 252),
            rng.normal(0, 0.01, 252),
        ]
    )
    z = np.array([2.0, 0.0, 0.0])  # asset 0 moved; its relative, asset 1, did not
    lam, cu = r.catchup(z, daily)
    assert lam[1] > 1.5 and cu[1] > 1.5  # the relative is "susceptible"
    assert cu[0] < -1.5  # the one that moved has nothing to catch up
    assert abs(cu[2]) < 0.5  # the unrelated asset is left alone
    slots = r.top_slots(["A", "B", "C"], cu, [True, True, True], 1)
    assert slots == {"B": 1.0}
    assert r.top_slots(["A", "B", "C"], cu, [True, False, True], 1) == {}  # out of trend: cash
    # an asset with no full window has no relatives: its signal is minus its own move
    daily[0, 2] = np.nan
    lam2, cu2 = r.catchup(np.array([2.0, 0.0, 1.0]), daily)
    assert lam2[2] == 0.0 and cu2[2] == -1.0


def test_rank_ic() -> None:
    r = _rules()
    x = np.arange(10.0)
    assert np.isclose(r.rank_ic(x, x**3), 1.0)
    assert np.isclose(r.rank_ic(x, -x), -1.0)
    assert np.isnan(r.rank_ic(x[:3], x[:3]))
