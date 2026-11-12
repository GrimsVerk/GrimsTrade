"""Honesty audit 2026-11: what the scoreboard will claim, and how wrong that can be.

Findings S1-S6 in docs/audits/honesty-2026-11.md. Randomness is seeded, so the tests are
deterministic.
"""

import math
import random
import statistics
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path

import pytest

from grimstrade import data, gym, ledger, report
from grimstrade.data import Bar, History
from grimstrade.gym import Decision, Result

NO_COSTS = {"crypto": gym.Costs(0, 0), "etf": gym.Costs(0, 0)}
DAY1 = date(2026, 11, 2)  # a Monday


def result_from_returns(returns: list[float], first: date = DAY1) -> Result:
    equity = [gym.START_CASH]
    for r in returns:
        equity.append(equity[-1] * (1 + r))
    days = [first + timedelta(days=i) for i in range(len(equity))]
    return Result(cash=0, positions={}, equity=list(zip(days, equity, strict=True)))


def sharpe_cell(row: str) -> str:
    header = report.table([]).splitlines()[0]
    names = [c.strip() for c in header.strip("|").split("|")]
    return [c.strip() for c in row.strip("|").split("|")][names.index("Sharpe")]


def test_a_record_of_a_few_days_shows_no_sharpe_number() -> None:
    """Audit S1 (fixed): the scoreboard printed a Sharpe ratio to two decimals from the second
    day. Under ~30 days it is pure noise: four good days read as "Sharpe 30"."""
    s = report.score("lucky", result_from_returns([0.01, 0.02, 0.005, 0.015]))
    assert s.sharpe > 20  # what four up-days annualise to
    assert sharpe_cell(report.table([s]).splitlines()[2]) == "-"
    # From 30 days on the number comes with its standard error: here 180 days of coin flips.
    rng = random.Random(1)
    s = report.score("coin", result_from_returns([rng.gauss(0, 0.02) for _ in range(180)]))
    cell = sharpe_cell(report.table([s]).splitlines()[2])
    assert cell == f"{s.sharpe:.2f} ±1.4"
    assert abs(s.sharpe) < 2 * 1.4  # and the truth (zero) is inside two standard errors


def test_nine_strategies_with_no_skill_after_six_months_the_best_looks_skilled() -> None:
    """Audit S2, sized: nine coin-flip strategies (zero true edge, 2% daily swings), 180 days,
    which is the graduation bar's "at least 6 months". Over 300 such worlds the best of the nine
    shows an annualised Sharpe of about 2.1 on average, and above 2 in over half of them. One
    strategy alone lands outside +-1 a third of the time. The table shows these numbers bare."""
    rng = random.Random(2026)
    best, single = [], []
    for _ in range(300):
        sharpes = [
            report.score("x", result_from_returns([rng.gauss(0, 0.02) for _ in range(180)])).sharpe
            for _ in range(9)
        ]
        best.append(max(sharpes))
        single.append(sharpes[0])
    assert statistics.fmean(best) == pytest.approx(2.1, abs=0.25)
    assert sum(b > 2 for b in best) / len(best) > 0.5
    assert statistics.pstdev(single) == pytest.approx(math.sqrt(365 / 180), abs=0.2)  # ~1.4
    assert sum(abs(x) > 1 for x in single) / len(single) > 0.33


def test_the_same_strategy_started_later_ranks_differently() -> None:
    """Audit S3: the table sorts by total return since each strategy's own first day. Two
    strategies that hold exactly the same thing are ranked apart, by start date alone. Still
    true of the Return column; the scoreboard now has a column that can be compared (next test)."""
    bars = [
        Bar(DAY1 + timedelta(days=i), 100.0 + 2 * i, 102.0 + 2 * i, 100.0 + 2 * i, 102.0 + 2 * i, 1)
        for i in range(60)
    ]
    hist: History = {"BTC": bars}
    at = datetime.combine(DAY1, time(22, 30), tzinfo=UTC)
    old = gym.simulate([Decision(at, {"BTC": 1.0})], hist, costs=NO_COSTS)
    new = gym.simulate([Decision(at + timedelta(days=30), {"BTC": 1.0})], hist, costs=NO_COSTS)
    s_old, s_new = report.score("benchmark", old), report.score("newcomer", new)
    assert s_old.total_return > 2 * s_new.total_return  # same holding, half the "return"
    rows = report.table([s_new, s_old]).splitlines()[2:]
    assert rows[0].startswith("| benchmark") and rows[1].startswith("| newcomer")


def test_the_scoreboard_says_how_fresh_each_assets_data_is(tmp_path: Path) -> None:
    """Audit S4 (fixed): when a source stopped, the scoreboard kept valuing that asset at its
    last price and did not say so: frozen prices look like a calm, flat strategy."""

    def flat(n: int, px: float) -> list[Bar]:
        return [Bar(DAY1 + timedelta(days=i), px, px, px, px, 1.0) for i in range(n)]

    data.append(tmp_path, "BTC", flat(19, 100.0))  # through 2026-11-20
    data.append(tmp_path, "SPY", flat(5, 500.0))  # through Friday 2026-11-06, then the source died
    seen = {"SPY": data.load(tmp_path, "SPY")[:1]}
    when = datetime.combine(DAY1, time(22, 30), tzinfo=UTC)
    ledger.write_decision(tmp_path, when, "buy_hold_spy", {"SPY": 1.0}, seen, "t")
    text = report.render(tmp_path, data.load_all(tmp_path))
    assert "buy_hold_spy" in text
    assert "Prices through: BTC 2026-11-20, SPY 2026-11-06 (**STALE: 14 days behind" in text
    # An ordinary weekend (ETFs two days behind crypto) is not stale.
    weekdays = [b for b in flat(17, 600.0) if b.date.weekday() < 5]
    data.append(tmp_path, "QQQ", weekdays)  # through Wednesday 2026-11-18
    assert report.freshness(data.load_all(tmp_path)).endswith(", QQQ 2026-11-18.")
    assert report.freshness({}) == "No prices stored yet."
    # The owner's page carries the warning too, but only when something is stale.
    from grimstrade import weekly

    page = weekly.render(tmp_path, data.load_all(tmp_path), tmp_path)
    assert (
        "**Warning, old prices.** Prices through: BTC 2026-11-20, SPY 2026-11-06 (**STALE" in page
    )
    fresh_only = {s: b for s, b in data.load_all(tmp_path).items() if s != "SPY"}
    assert "Warning" not in weekly.render(tmp_path, fresh_only, tmp_path)


def test_the_scoreboard_counts_days_a_strategy_never_decided_on(tmp_path: Path) -> None:
    """Audit S4 (second half, fixed): a run that fails, is skipped by GitHub's scheduler or loses
    its push leaves no decision that day, and a strategy that raises keeps its old position.
    The scoreboard showed none of it: a strategy that decided on 3 days of 6 looked like one
    that decided on all of them."""
    flat = [Bar(DAY1 + timedelta(days=i), 100.0, 100.0, 100.0, 100.0, 1.0) for i in range(7)]

    def decide(name: str, bars_seen: int, when: datetime) -> None:
        ledger.write_decision(tmp_path, when, name, {"BTC": 1.0}, {"BTC": flat[:bars_seen]}, "t")

    evening = datetime.combine(DAY1, time(22, 30), tzinfo=UTC)
    for day in range(1, 7):  # every evening, seeing the bar that closed the midnight before
        decide("steady", day, evening + timedelta(days=day))
    for day in (1, 2, 5):  # the runs of days 3 and 4 never happened, and it stopped after day 5
        decide("gappy", day, evening + timedelta(days=day))
    # A run that is hours late (03:12 instead of 22:30) but sees each day's bar skips nothing.
    for day in range(1, 7):
        decide("late", day, evening + timedelta(days=day, hours=4, minutes=42))
    data.append(tmp_path, "BTC", flat[:6])
    history = data.load_all(tmp_path)
    assert report.undecided_days(tmp_path, history) == {"gappy": 3}
    text = report.render(tmp_path, history)
    assert "Days of new prices with no decision" in text and "gappy 3." in text
    # Without an asset that has a bar every day there is nothing to count on.
    assert report.undecided_days(tmp_path, {"SPY": history["BTC"]}) == {}


def test_sharpe_does_not_depend_on_how_many_calendar_days_have_a_point() -> None:
    """Audit S5 (fixed): Sharpe was annualised with sqrt(365) whatever the spacing of the equity
    points; with a point on weekdays only (an ETF-only history) it came out 20% too high."""
    rng = random.Random(4)
    days = [DAY1 + timedelta(days=i) for i in range(3 * 365)]
    spy, px = [], 100.0
    for d in days:
        if d.weekday() < 5:
            close = px * math.exp(rng.gauss(0.0005, 0.01))
            spy.append(Bar(d, px, max(px, close), min(px, close), close, 1.0))
            px = close
    btc = [Bar(d, 1.0, 1.0, 1.0, 1.0, 1.0) for d in days]
    decision = Decision(datetime.combine(DAY1, time(22, 30), tzinfo=UTC), {"SPY": 1.0})
    with_weekends = report.score("a", gym.simulate([decision], {"SPY": spy, "BTC": btc}))
    weekdays_only = report.score("a", gym.simulate([decision], {"SPY": spy}))
    assert with_weekends.days > weekdays_only.days
    # Same portfolio, same prices: the Sharpe ratio and the turnover must be the same.
    assert weekdays_only.sharpe == pytest.approx(with_weekends.sharpe, rel=0.03)
    assert weekdays_only.turnover == pytest.approx(with_weekends.turnover, rel=0.01)


def test_sharpe_with_365_days_matches_the_trading_day_convention_for_etfs() -> None:
    """Checked and sound: with one equity point per calendar day (crypto guarantees that in the
    live record), flat weekends lower the mean and the variance together, and the 365-day Sharpe
    of an ETF-only strategy equals the usual 252-trading-day one."""
    rng = random.Random(4)
    days = [DAY1 + timedelta(days=i) for i in range(3 * 365)]
    spy, px = [], 100.0
    for d in days:
        if d.weekday() < 5:
            close = px * math.exp(rng.gauss(0.0005, 0.01))
            spy.append(Bar(d, px, max(px, close), min(px, close), close, 1.0))
            px = close
    btc = [Bar(d, 1.0, 1.0, 1.0, 1.0, 1.0) for d in days]
    decision = Decision(datetime.combine(DAY1, time(22, 30), tzinfo=UTC), {"SPY": 1.0})
    live = report.score("a", gym.simulate([decision], {"SPY": spy, "BTC": btc}, costs=NO_COSTS))
    closes = [b.close for b in spy[1:]]  # held from the second bar's open
    rets = [b / a - 1 for a, b in zip(closes, closes[1:], strict=False)]
    trading_day_sharpe = statistics.fmean(rets) / statistics.pstdev(rets) * math.sqrt(252)
    assert live.sharpe == pytest.approx(trading_day_sharpe, rel=0.03)


def test_todays_equity_is_provisional_and_changes_tomorrow() -> None:
    """Audit S6 (low): at 22:30 UTC today's crypto bar is still open, so the scoreboard's newest
    equity point mixes today's ETF close with crypto at yesterday's close. The same date shows
    another number once the bar arrives: the published last row is not final."""
    btc = [Bar(DAY1 + timedelta(days=i), 100.0, 130.0, 100.0, c, 1.0)
           for i, c in enumerate([100.0, 100.0, 130.0])]  # fmt: skip
    spy = [Bar(DAY1 + timedelta(days=i), 50.0, 50.0, 50.0, 50.0, 1.0) for i in range(3)]
    decision = Decision(datetime.combine(DAY1, time(22, 30), tzinfo=UTC), {"BTC": 1.0})
    tonight = gym.simulate([decision], {"BTC": btc[:2], "SPY": spy}, costs=NO_COSTS)
    tomorrow = gym.simulate([decision], {"BTC": btc, "SPY": spy}, costs=NO_COSTS)
    today = DAY1 + timedelta(days=2)
    last_day, last_equity = tonight.equity[-1]
    assert last_day == today and last_equity == pytest.approx(10_000)
    assert dict(tomorrow.equity)[today] == pytest.approx(13_000)


def test_the_deflated_sharpe_bar_is_out_of_reach_for_years() -> None:
    """Audit S2 (part 2), sized: the scoreboard's deflated Sharpe allows for every strategy
    "tried", and that count includes every backtest variant the research lane logs: 256 on
    2026-11-12, one
    day in. The Sharpe a strategy must then show before "95% sure" is about 6.4 after six months,
    4.5 after a year, 2.0 after five. A strategy with a true Sharpe of 1.0 (very good) passes
    after three years in about 1 world in 100. Cautious, not dishonest, but the board will say
    "no sign of skill" about everything for years, and DESIGN.md's graduation bar ("at least 6
    months") cannot be met by any realistic strategy."""
    from statistics import NormalDist

    from grimstrade import stats

    def needed(tries: int, days: int) -> float:
        luck = stats.expected_max_sharpe(tries, stats.null_sharpe_variance(days))
        return (luck + NormalDist().inv_cdf(0.95) / math.sqrt(days - 1)) * math.sqrt(365)

    assert needed(256, 182) == pytest.approx(6.4, abs=0.05)
    assert needed(256, 365) == pytest.approx(4.5, abs=0.05)
    assert needed(256, 3 * 365) == pytest.approx(2.6, abs=0.05)
    assert needed(256, 5 * 365) == pytest.approx(2.0, abs=0.05)
    assert needed(256, 10 * 365) == pytest.approx(1.4, abs=0.05)
    assert needed(9, 182) == pytest.approx(4.5, abs=0.05)  # even counting only the 9 live ones
    assert needed(9, 3 * 365) == pytest.approx(1.8, abs=0.05)

    rng = random.Random(12)
    days, daily_sd = 3 * 365, 0.01
    daily_mean = 1.0 / math.sqrt(365) * daily_sd  # true annualised Sharpe 1.0
    scores = [
        report.score(f"good{i}", result_from_returns([rng.gauss(daily_mean, daily_sd)
                                                      for _ in range(days)]))
        for i in range(100)
    ]  # fmt: skip
    passed = 0
    for s in scores:  # each one alone on the board, 256 strategies tried
        (deflated,) = report.deflate([s], report.Trials(count=256))
        passed += (deflated.dsr or 0) >= 0.95
    assert statistics.fmean(s.sharpe for s in scores) == pytest.approx(1.0, abs=0.15)
    assert passed <= 3


def test_the_pages_say_how_high_the_deflated_sharpe_bar_is(tmp_path: Path) -> None:
    """Audit S2 (the part that could be fixed): the pages showed the deflated Sharpe without
    saying what it takes to pass, so "no sign of skill yet" would read as a verdict on each
    strategy for years. Both pages now state the Sharpe needed for 95%, and that number agrees
    with what the column does."""
    assert report.sharpe_needed(256, 182) == pytest.approx(6.4, abs=0.1)
    assert report.sharpe_needed(256, 3 * 365) == pytest.approx(2.6, abs=0.1)
    rng = random.Random(7)
    days = 365
    noise = [rng.gauss(0, 1) for _ in range(days)]
    mean, sd = statistics.fmean(noise), statistics.pstdev(noise)
    for factor, passes in ((1.1, True), (0.9, False)):  # a record just above the bar, just below
        daily = report.sharpe_needed(256, days) * factor / math.sqrt(365)
        returns = [0.01 * ((x - mean) / sd + daily) for x in noise]
        (s,) = report.deflate(
            [report.score("x", result_from_returns(returns))], report.Trials(count=256)
        )
        assert s.dsr is not None and (s.dsr >= 0.95) == passes
    words = "above about 6.4 after six months, 4.5 after one year, 2.6 after three"
    assert words in report.footnote(report.Trials(count=256))
    # The owner's page says it too.
    from grimstrade import weekly

    bars = [Bar(DAY1 + timedelta(days=i), 100.0, 100.0, 100.0, 100.0, 1.0) for i in range(3)]
    data.append(tmp_path, "BTC", bars)
    when = datetime.combine(DAY1, time(22, 30), tzinfo=UTC)
    ledger.write_decision(tmp_path, when, "buy_hold_btc", {"BTC": 1.0}, {"BTC": bars[:1]}, "t")
    page = weekly.render(tmp_path, data.load_all(tmp_path), tmp_path)
    assert "Strong evidence takes years, not months" in page and "after six months" in page
    # Audit G4 (open, sized): the page says which way the missing dividends tilt the comparison.
    assert "yardsticks 1 to 2% a year too easy to beat" in page


def test_a_fill_on_the_first_day_counts_in_sharpe_and_drawdown() -> None:
    """Audit S7 (fixed; found by the independent reviewer): the first equity point was used as
    the baseline. Normally that is the untouched start cash, but a decision made before the US
    open (a manual run, as on 2026-11-12 01:51 UTC, or a cron run that slips past midnight) fills
    ETFs the same day, and that day's result then vanished from Sharpe and max drawdown."""
    monday = DAY1
    spy = [Bar(monday, 100.0, 100.0, 90.0, 90.0, 1.0)] + [
        Bar(monday + timedelta(days=i), 90.0, 90.0, 90.0, 90.0, 1.0) for i in (1, 2, 3)
    ]
    btc = [Bar(monday + timedelta(days=i), 1.0, 1.0, 1.0, 1.0, 1.0) for i in range(4)]
    decision = Decision(datetime.combine(monday, time(10, 0), tzinfo=UTC), {"SPY": 1.0})
    res = gym.simulate([decision], {"SPY": spy, "BTC": btc}, costs=NO_COSTS)
    assert res.equity[0] == (monday, 9_000.0)  # bought at 100 at the open, closed at 90
    s = report.score("early", res)
    assert s.total_return == pytest.approx(-0.10)
    assert s.max_drawdown == pytest.approx(0.10)  # was 0.0%
    assert s.sharpe < 0  # was 0.00
    # A record of a single day used to show "Equity 9,000, Return +0.0%".
    one_day = gym.simulate([decision], {"SPY": spy[:1], "BTC": btc[:1]}, costs=NO_COSTS)
    assert report.score("early", one_day).total_return == pytest.approx(-0.10)
    # And a run with another start cash is scored against that cash, not against 10,000.
    rich = gym.simulate([decision], {"SPY": spy[1:], "BTC": btc}, start_cash=100_000.0)
    assert report.score("rich", rich).total_return == pytest.approx(0.0, abs=1e-3)


def test_a_deflated_sharpe_is_never_printed_as_certain() -> None:
    s = report.score("x", result_from_returns([0.01] * 40))
    row = report.table([s.__class__(**{**s.__dict__, "dsr": 0.9996})]).splitlines()[2]
    assert "| >99% |" in row and "100%" not in row


@pytest.mark.parametrize(
    ("hour", "bars"),
    [
        # Decided Monday 22:30; SPY gaps down 5% overnight. The yardstick's own curve from
        # Monday's close carries that loss; the copy, in cash overnight, does not.
        (22, [(100, 100), (95, 95), (95, 95), (95, 95)]),
        # Decided Monday 10:00, before the open: the copy is filled at Monday's open and has
        # Monday's 5% rise. The yardstick's curve from the end of Monday does not.
        (10, [(100, 105), (105, 105), (105, 105), (105, 105)]),
    ],
)
def test_an_exact_copy_of_a_yardstick_never_beats_it(
    tmp_path: Path, hour: int, bars: list[tuple[float, float]]
) -> None:
    """Audit S8 (fixed; found by the independent reviewer): the weekly page compared a strategy
    with each yardstick's own curve from the end of the strategy's first day. That hands one of
    the two the move between the strategy's decision and its first fills, for good: over 149
    real start days the reviewer measured a mean gap of 0.54% and up to 4.9 points for an exact
    copy of buy-and-hold SPY. Now the yardstick is restarted with fresh cash at the same moment."""
    history: History = {
        "SPY": [Bar(DAY1 + timedelta(days=i), o, max(o, c), min(o, c), c, 1.0)
                for i, (o, c) in enumerate(bars)],
        "BTC": [Bar(DAY1 + timedelta(days=i), 1.0, 1.0, 1.0, 1.0, 1.0) for i in range(-7, 4)],
    }  # fmt: skip
    seen: History = {"SPY": [Bar(DAY1 - timedelta(days=8), 100, 100, 100, 100, 1)]}
    week_before = datetime.combine(DAY1 - timedelta(days=7), time(22, 30), tzinfo=UTC)
    ledger.write_decision(tmp_path, week_before, "buy_hold_spy", {"SPY": 1.0}, seen, "yardstick")
    started = datetime.combine(DAY1, time(hour, 0), tzinfo=UTC)
    ledger.write_decision(tmp_path, started, "vol_target_spy", {"SPY": 1.0}, seen, "exact copy")
    from grimstrade import weekly

    text = weekly.render(tmp_path, history, tmp_path)
    row = next(line for line in text.splitlines() if line.startswith("| Stocks, but less"))
    assert "| 0 of 1 |" in row


def test_the_scoreboard_has_a_column_that_is_fair_to_late_starters(tmp_path: Path) -> None:
    """Audit S3 (fixed): next to the returns since each row's own start, the scoreboard shows
    how many yardsticks a strategy beats when each yardstick is restarted at that row's start."""
    # BTC doubles in 30 days, then goes sideways. A copy of "hold BTC" that starts on day 30
    # shows about half the yardstick's return, and still has not lost to it.
    prices = [100.0 + 100.0 * min(i, 30) / 30 for i in range(60)]
    bars = [Bar(DAY1 + timedelta(days=i), p, p, p, p, 1.0) for i, p in enumerate(prices)]
    history: History = {"BTC": bars}
    seen: History = {"BTC": bars[:1]}
    start = datetime.combine(DAY1, time(22, 30), tzinfo=UTC)
    ledger.write_decision(tmp_path, start, "buy_hold_btc", {"BTC": 1.0}, seen, "yardstick")
    late = start + timedelta(days=30)
    ledger.write_decision(tmp_path, late, "ts_momentum", {"BTC": 1.0}, seen, "a late copy")
    ledger.write_decision(tmp_path, late, "xs_momentum", {}, seen, "stays in cash")
    board = report.render(tmp_path, history, tmp_path)
    rows = {line.split("|")[1].strip(): line for line in board.splitlines() if line.startswith("|")}
    assert "| +9" in rows["buy_hold_btc"] and "| - |" in rows["buy_hold_btc"]  # +9x%, no verdict
    assert "| 0 of 1 |" in rows["ts_momentum"]  # the same thing: not ahead, whatever the Return
    assert "| 1 of 1 |" in rows["xs_momentum"]  # cash beat a sideways BTC bought with costs
    assert 'compare rows by "Beats yardsticks"' in board
