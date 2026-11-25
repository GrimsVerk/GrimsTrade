"""`reconcile.rebuild_state` pinned on the synthetic book of `test_reconcile_daily`.

The values were taken from `reconcile.py` before it reused `gym.cash_rate` / `gym.interest`
(lane reconcile-reuse-1): the reuse must not move a single bit. Two rate sets: the fixture's
own, and one given out of order with a negative step and days before any rate is known (rate 0,
floored at 0).
"""

from __future__ import annotations

from datetime import date, timedelta

import test_reconcile_daily as t

from grimstrade import gym, reconcile

OUT_OF_ORDER = [
    (t.at(t.START + timedelta(days=12), 21), 0.06),
    (t.at(t.START + timedelta(days=5), 21), -0.01),
]


def rebuilt(rates: gym.Rates, marked: bool = True) -> dict[str, object]:
    h, decs, _, row = t.book()
    res = gym.simulate(decs, h, dividends=t.DIVIDENDS, rates=rates)
    found, ruled = reconcile.fill_problems(res.fills, decs, h)
    assert found == []
    day = date.fromisoformat(row["marked_on"]) if marked else None
    state, low = reconcile.rebuild_state(
        res.fills, ruled, decs, h, t.DIVIDENDS, rates, day, res.start_cash
    )
    assert low == []
    return state


def test_rebuild_state_is_pinned_on_the_fixture_rates() -> None:
    s = rebuilt(t.RATES)
    assert s == {
        "cash": 931.7273215719141,
        "positions": {"BTC": 40.5620309645476, "SPY": 41.83699367195831},
        "equity": 9372.68280749425,
        "fills": 44,
    }


def test_rebuild_state_is_pinned_without_a_marked_day() -> None:
    s = rebuilt(t.RATES, marked=False)  # no interest at all, equity is the start cash
    assert (s["cash"], s["equity"]) == (920.2882804607752, 10_000.0)


def test_rebuild_state_is_pinned_on_unsorted_negative_rates() -> None:
    s = rebuilt(OUT_OF_ORDER)
    assert s == {
        "cash": 931.7119760426448,
        "positions": {"BTC": 40.55721907564341, "SPY": 41.83101411572463},
        "equity": 9371.59532592367,
        "fills": 44,
    }
