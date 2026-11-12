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
    strategies that hold exactly the same thing are ranked apart, by start date alone; a new
    strategy can never be compared with a benchmark that started earlier."""
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
    data.append(tmp_path, "QQQ", flat(18, 600.0)[:17])  # through Wednesday 2026-11-18
    assert report.freshness(data.load_all(tmp_path)).endswith(", QQQ 2026-11-18.")
    assert report.freshness({}) == "No prices stored yet."


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
    "tried", and that count includes every backtest variant the research lane logs: 219 on
    2026-11-12, one
    day in. The Sharpe a strategy must then show before "95% sure" is about 6.3 after six months,
    4.4 after a year, 2.0 after five. A strategy with a true Sharpe of 1.0 (very good) passes
    after three years in about 1 world in 100. Cautious, not dishonest, but the board will say
    "no sign of skill" about everything for years, and DESIGN.md's graduation bar ("at least 6
    months") cannot be met by any realistic strategy."""
    from statistics import NormalDist

    from grimstrade import stats

    def needed(tries: int, days: int) -> float:
        luck = stats.expected_max_sharpe(tries, stats.null_sharpe_variance(days))
        return (luck + NormalDist().inv_cdf(0.95) / math.sqrt(days - 1)) * math.sqrt(365)

    assert needed(219, 182) == pytest.approx(6.3, abs=0.1)
    assert needed(219, 365) == pytest.approx(4.4, abs=0.1)
    assert needed(219, 5 * 365) == pytest.approx(2.0, abs=0.1)
    assert needed(9, 182) == pytest.approx(4.5, abs=0.1)  # even counting only the 9 live ones

    rng = random.Random(12)
    days, daily_sd = 3 * 365, 0.01
    daily_mean = 1.0 / math.sqrt(365) * daily_sd  # true annualised Sharpe 1.0
    scores = [
        report.score(f"good{i}", result_from_returns([rng.gauss(daily_mean, daily_sd)
                                                      for _ in range(days)]))
        for i in range(100)
    ]  # fmt: skip
    passed = 0
    for s in scores:  # each one alone on the board, 219 strategies tried
        (deflated,) = report.deflate([s], report.Trials(count=219))
        passed += (deflated.dsr or 0) >= 0.95
    assert statistics.fmean(s.sharpe for s in scores) == pytest.approx(1.0, abs=0.15)
    assert passed <= 3
