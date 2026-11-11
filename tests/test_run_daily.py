import json
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from grimstrade import ledger, report, run_daily
from grimstrade.gym import Fill, Result
from grimstrade.strategies import LIVE

DAY0 = date(2026, 10, 1)


def fake_market(url: str) -> bytes:
    """Kraken-style JSON for crypto, Stooq CSV for ETFs (Yahoo 'down'). Prices rise 1/day."""
    days = [DAY0 + timedelta(days=i) for i in range(60)]
    if "kraken" in url:
        ts = [int(datetime(d.year, d.month, d.day, tzinfo=UTC).timestamp()) for d in days]
        rows = [[t, str(100 + i), str(101 + i), str(99 + i), str(100.5 + i), "0", "10", 1]
                for i, t in enumerate(ts)]  # fmt: skip
        return json.dumps({"error": [], "result": {"PAIR": rows, "last": ts[-1]}}).encode()
    if "stooq" in url:
        lines = ["Date,Open,High,Low,Close,Volume"]
        lines += [f"{d},{50 + i},{51 + i},{49 + i},{50.5 + i},1000"
                  for i, d in enumerate(days) if d.weekday() < 5]  # fmt: skip
        return "\n".join(lines).encode()
    raise OSError("blocked")


def test_daily_runs_build_an_append_only_record(tmp_path: Path) -> None:
    first = datetime(2026, 11, 2, 22, 30, tzinfo=UTC)
    assert run_daily.run(tmp_path, first, fake_market) == []
    rows = ledger.decisions(tmp_path)
    assert {r["strategy"] for r in rows} == set(LIVE)
    # Decided at 22:30 on 11-02: crypto seen through 11-01, ETFs through 11-02.
    assert rows[0]["data_through"]["BTC"] == "2026-11-01"
    assert rows[0]["data_through"]["SPY"] == "2026-11-02"
    text_after_first = (tmp_path / ledger.DECISIONS).read_text()

    # Re-run the same evening: nothing new, so no new decisions.
    run_daily.run(tmp_path, first + timedelta(minutes=30), fake_market)
    assert (tmp_path / ledger.DECISIONS).read_text() == text_after_first

    # Next evening: one more decision each, appended.
    run_daily.run(tmp_path, first + timedelta(days=1), fake_market)
    assert (tmp_path / ledger.DECISIONS).read_text().startswith(text_after_first)
    assert len(ledger.decisions(tmp_path)) == 2 * len(LIVE)
    assert ledger.tries(tmp_path) == len(LIVE)

    # The first decision fills at the 11-03 open, which is only stored once that bar closes.
    state = json.loads((tmp_path / "state" / "portfolio.json").read_text())
    assert state["buy_hold_btc"]["fills"] == 0
    run_daily.run(tmp_path, first + timedelta(days=2), fake_market)
    state = json.loads((tmp_path / "state" / "portfolio.json").read_text())
    btc = state["buy_hold_btc"]
    assert btc["fills"] == 1 and set(btc["positions"]) == {"BTC"}
    assert btc["equity"] > 10_000  # fake prices only go up
    assert (tmp_path / "reports" / "scoreboard.md").read_text().startswith("# Scoreboard")


def test_a_failing_source_is_reported_but_the_rest_still_runs(tmp_path: Path) -> None:
    def no_etfs(url: str) -> bytes:
        if "kraken" in url:
            return fake_market(url)
        raise OSError("blocked")

    problems = run_daily.run(tmp_path, datetime(2026, 11, 2, 22, 30, tzinfo=UTC), no_etfs)
    assert len(problems) == 4
    assert len(ledger.decisions(tmp_path, "buy_hold_btc")) == 1


def test_score_math() -> None:
    days = [date(2026, 11, d) for d in range(1, 5)]
    res = Result(
        cash=0, positions={}, equity=list(zip(days, [10_000, 11_000, 9_900, 10_890], strict=True))
    )
    res.fills.append(Fill(datetime(2026, 11, 1, tzinfo=UTC), "BTC", 1.0, 10_000, 0))
    s = report.score("x", res)
    assert s.total_return == pytest.approx(0.089)
    assert s.max_drawdown == pytest.approx(0.1)
    assert s.sharpe > 0
    mean_eq = (10_000 + 11_000 + 9_900 + 10_890) / 4
    assert s.turnover == pytest.approx(10_000 / mean_eq * 365 / 4)
