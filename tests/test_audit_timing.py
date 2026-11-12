"""Honesty audit 2026-11: the timing rules (no look-ahead).

The rules in docs/DESIGN.md held up: the first tests here pin them against the real US session
calendar and random decision times. One gap is left (T1 in docs/audits/honesty-2026-11.md).
"""

import random
from datetime import UTC, date, datetime, time, timedelta
from zoneinfo import ZoneInfo

import pytest

from grimstrade import data, gym
from grimstrade.data import CRYPTO, ETF, UNIVERSE, Bar, History
from grimstrade.gym import Decision

NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}
NEW_YORK = ZoneInfo("America/New_York")


def weekdays(first: date, last: date) -> list[date]:
    days = [first + timedelta(days=i) for i in range((last - first).days + 1)]
    return [d for d in days if d.weekday() < 5]


def test_assumed_etf_session_contains_the_real_one_all_year() -> None:
    """Assumed open (13:30 UTC) is never after the real 09:30 New York open, assumed close
    (21:00 UTC) never before the real 16:00 close, summer and winter, including the weeks when
    the US has changed its clocks and Europe has not. Half days close earlier: also safe."""
    offsets = set()
    for d in weekdays(date(2026, 1, 1), date(2028, 12, 31)):
        real_open = datetime.combine(d, time(9, 30), tzinfo=NEW_YORK).astimezone(UTC)
        real_close = datetime.combine(d, time(16, 0), tzinfo=NEW_YORK).astimezone(UTC)
        assert data.open_time(ETF, d) <= real_open
        assert data.close_time(ETF, d) >= real_close
        # A source that stamps the bar anywhere in the session gives the right UTC date.
        assert real_open.date() == d == real_close.date()
        offsets.add(real_open.hour)
    assert offsets == {13, 14}  # both daylight-saving cases were really exercised


def market(first: date, days: int, rng: random.Random) -> History:
    """BTC every day, SPY on weekdays, random prices: the open differs from the last close."""

    def bars(dates: list[date]) -> list[Bar]:
        out = []
        for d in dates:
            o, c = rng.uniform(50, 150), rng.uniform(50, 150)
            out.append(Bar(d, o, max(o, c), min(o, c), c, 1.0))
        return out

    all_days = [first + timedelta(days=i) for i in range(days)]
    return {"BTC": bars(all_days), "SPY": bars([d for d in all_days if d.weekday() < 5])}


@pytest.mark.parametrize("first", [date(2026, 3, 2), date(2026, 10, 26)])  # both clock changes
def test_random_decision_times_never_see_or_fill_at_the_wrong_bar(first: date) -> None:
    rng = random.Random(3)
    history = market(first, 21, rng)
    start = datetime.combine(first, time(0, 0), tzinfo=UTC)
    # Decision times in the first 17 days, so each asset still has a bar that opens later.
    times = [start + timedelta(minutes=rng.randrange(17 * 24 * 60)) for _ in range(300)]
    # Plus the exact boundaries, where an off-by-one would hide.
    for day in range(1, 8):
        for hh, mm in ((0, 0), (13, 30), (21, 0), (21, 15), (22, 30)):
            times.append(start + timedelta(days=day, hours=hh, minutes=mm))

    for t in times:
        seen = data.visible_history(history, t)
        for sym, bars in seen.items():
            cls = UNIVERSE[sym]
            assert all(data.close_time(cls, b.date) <= t for b in bars)
            hidden = history[sym][len(bars) :]
            assert all(data.close_time(cls, b.date) > t for b in hidden)

        res = gym.simulate([Decision(t, {"BTC": 0.5, "SPY": 0.5})], history, costs=NO_COSTS)
        assert {f.symbol for f in res.fills} == {"BTC", "SPY"}
        for f in res.fills:
            cls = UNIVERSE[f.symbol]
            later = [b for b in history[f.symbol] if data.open_time(cls, b.date) > t]
            assert f.time == data.open_time(cls, later[0].date) > t
            assert f.price == later[0].open  # the first open after the decision, no other


def test_a_bar_still_in_progress_is_never_final() -> None:
    d = date(2026, 11, 10)
    b = [Bar(d, 1, 1, 1, 1, 1)]
    start = datetime.combine(d, time(0, 0), tzinfo=UTC)
    for minutes in range(0, 24 * 60 + 15, 5):  # the whole UTC day and 14 minutes after it
        assert data.settled(b, CRYPTO, start + timedelta(minutes=minutes)) == []
    for minutes in range(0, 21 * 60 + 15, 5):  # up to 21:14 UTC
        assert data.settled(b, ETF, start + timedelta(minutes=minutes)) == []
    assert data.settled(b, ETF, start + timedelta(hours=21, minutes=15)) == b


@pytest.mark.xfail(
    strict=True,
    reason="audit T1: a decision stamped seconds before an open is filled at that open, though "
    "it cannot have been committed and pushed before that price existed",
)
def test_a_decision_is_not_filled_before_it_could_have_been_pushed() -> None:
    history: History = {
        "BTC": [Bar(date(2026, 11, d), 100.0 * d, 100.0 * d, 100.0 * d, 100.0 * d, 1.0)
                for d in (1, 2, 3)]
    }  # fmt: skip
    # A late run (GitHub's cron can slip by an hour or more): decided 23:59:30 on the 1st.
    decided = datetime(2026, 11, 1, 23, 59, 30, tzinfo=UTC)
    res = gym.simulate([Decision(decided, {"BTC": 1.0})], history, costs=NO_COSTS)
    (fill,) = res.fills
    # Today: filled 30 seconds later, at the open of the 2nd. The commit that proves the decision
    # lands after that open, so from outside it looks the same as a decision made knowing it.
    assert fill.time - decided >= timedelta(minutes=10)
