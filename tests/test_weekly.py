"""The owner's weekly summary: plain words, after costs, compared over the same days."""

from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from grimstrade import ledger, weekly
from grimstrade.data import Bar
from grimstrade.gym import Result

D0 = date(2026, 11, 1)


def curve(values: list[float], start: date = D0) -> Result:
    return Result(
        cash=0,
        positions={},
        equity=[(start + timedelta(days=i), v) for i, v in enumerate(values)],
    )


def test_change_over_a_window() -> None:
    r = curve([10_000, 10_500, 11_000, 9_900])
    assert weekly.change(r, D0 + timedelta(days=1), D0 + timedelta(days=3)) == pytest.approx(
        9_900 / 10_500 - 1
    )
    # Before the first mark the strategy still held its start cash.
    assert weekly.change(r, D0 - timedelta(days=5), D0 + timedelta(days=2)) == pytest.approx(0.1)


@pytest.mark.parametrize(
    ("dsr", "words"),
    [(None, "too early"), (0.3, "no sign"), (0.7, "maybe"), (0.92, "promising"), (0.99, "strong")],
)
def test_sureness_in_words(dsr: float | None, words: str) -> None:
    assert words in weekly.sureness(dsr)


def write(root: Path, strategy: str, day: date, weights: dict[str, float]) -> None:
    t = datetime.combine(day, datetime.min.time(), tzinfo=UTC).replace(hour=22, minute=30)
    seen = {"BTC": [Bar(day - timedelta(days=1), 1, 1, 1, 1, 1)]}
    ledger.write_decision(root, t, strategy, weights, seen, "test")


def test_summary_compares_a_late_starter_over_its_own_days(tmp_path: Path) -> None:
    # BTC doubles in the first 10 days, then drifts down 1%/day for 10 days.
    prices = [100.0 * (1.07**i) for i in range(11)] + [196.7 * 0.99**i for i in range(1, 11)]
    history = {
        "BTC": [Bar(D0 + timedelta(days=i), p, p, p, p, 1) for i, p in enumerate(prices)],
        "SPY": [],
    }
    write(tmp_path, "buy_hold_btc", D0, {"BTC": 1.0})
    write(tmp_path, "buy_hold_spy", D0, {"SPY": 1.0})
    # Started in cash after the rally: lost nothing while BTC fell, so it beats holding BTC
    # over its own days even though holding BTC is far ahead since the start.
    write(tmp_path, "ts_momentum", D0 + timedelta(days=11), {})
    text = weekly.render(tmp_path, history, tmp_path)
    assert text.startswith("# Weekly summary: the week to")
    assert "Hold Bitcoin" in text and "Trend following" in text
    row = next(line for line in text.splitlines() if line.startswith("| Trend following"))
    # Beats holding BTC over its days; ties with SPY (no SPY data, flat), and a tie isn't a win.
    assert "| 1 of 2 |" in row and "too early to tell" in row
    assert "**In short:** 0 of 1 strategies are ahead of every yardstick" in text
    assert len(text.splitlines()) < 40  # one screen


def test_summary_without_any_record(tmp_path: Path) -> None:
    assert "No trading days" in weekly.render(tmp_path, {}, tmp_path)
