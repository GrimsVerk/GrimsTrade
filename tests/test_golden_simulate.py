"""Golden outputs of `gym.simulate`: the replay's results must not change, to the last bit.

`gym.simulate` scores every live strategy, the ledger and every backtest, so a refactor of its
event loop must leave every number exactly as it was. Recorded from the code before the stepwise
engine (`gym.Replay`) replaced simulate's own loop (lane gymreplay-1, 2026-11-24): for every live
strategy (`strategies.LIVE`), `simulate(backtest(...))` on

- a fixed synthetic dataset: all six assets, one starting late, a missing crypto day, ETF
  holidays, distributions, a stepped cash rate (one step negative, so clamped to 0);
- hand-made decisions that hit the loop's edges: two decisions at one time, a decision at an
  open's exact time, one before any bar, one after the last bar, sparse weekly gaps;
- the paper-trail record's stored bars at a pinned commit (with synthetic distributions and
  rates on top), and its live ledger replay (`report.live_results`). Skipped where that commit
  is not in the local clone (CI checks out `main` only).

Each result is hashed from the repr of every float (equity curve, cash growth, fills, cash,
positions, income), so "equal" means bit-identical. Rewrite the fixture
(`uv run python tests/test_golden_simulate.py --write`) only for a change that is meant to
change the replay's numbers, and say so in the PR.
"""

from __future__ import annotations

import hashlib
import json
import math
import random
import subprocess
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from grimstrade import data, gym, report
from grimstrade.data import UNIVERSE, Bar, Dividend, open_time
from grimstrade.gym import Decision, Result
from grimstrade.strategies import LIVE

FIXTURE = Path(__file__).parent / "fixtures" / "golden_simulate.json"
REPO = Path(__file__).resolve().parents[1]
# The paper-trail commit whose stored bars and ledger the golden numbers were taken from.
TRAIL_COMMIT = "9e58ad6527a80646fe70bfcd760f9e34d711d3fd"

FIRST, LAST = date(2019, 1, 1), date(2023, 6, 30)
BACKTEST_FROM = date(2022, 7, 1)
HOLIDAYS = {date(y, m, d) for y in range(2019, 2024) for m, d in ((1, 1), (7, 4), (12, 25))}


def digest(res: Result) -> dict[str, Any]:
    payload = {
        "cash": res.cash,
        "start_cash": res.start_cash,
        "positions": sorted(res.positions.items()),
        "fills": [(f.time.isoformat(), f.symbol, f.qty, f.price, f.fee) for f in res.fills],
        "equity": [(d.isoformat(), e) for d, e in res.equity],
        "cash_growth": res.cash_growth,
        "income": [(t.isoformat(), s, a) for t, s, a in res.income],
    }
    text = json.dumps(payload)  # floats as repr: round-trip exact
    return {
        "sha256": hashlib.sha256(text.encode()).hexdigest(),
        "fills": len(res.fills),
        "days": len(res.equity),
        "cash": res.cash,
        "equity": res.equity[-1][1] if res.equity else None,
    }


# --- synthetic data ---


def walk(
    first: date, last: date, seed: int, etf: bool, skip: frozenset[date] = frozenset()
) -> list[Bar]:
    rng = random.Random(seed)
    out, px, d = [], 100.0, first
    while d <= last:
        trading = not etf or (d.weekday() < 5 and d not in HOLIDAYS)
        if trading and d not in skip:
            o = px * math.exp(rng.gauss(0, 0.006)) if etf else px * math.exp(rng.gauss(0, 0.002))
            c = o * math.exp(rng.gauss(0.0003, 0.025 if not etf else 0.012))
            out.append(Bar(d, o, max(o, c) * 1.01, min(o, c) * 0.99, c, 1.0))
            px = c
        d += timedelta(days=1)
    return out


def synthetic() -> tuple[dict[str, list[Bar]], dict[str, list[Dividend]], gym.Rates]:
    history = {
        "BTC": walk(FIRST, LAST, 11, etf=False, skip=frozenset({date(2022, 3, 5)})),
        "ETH": walk(date(2020, 6, 1), LAST, 12, etf=False),  # starts late
        "SPY": walk(FIRST, LAST, 13, etf=True),
        "QQQ": walk(FIRST, LAST, 14, etf=True),
        "GLD": walk(FIRST, LAST, 15, etf=True),
        "TLT": walk(FIRST, LAST, 16, etf=True),
    }
    dividends = {sym: fake_dividends(history[sym], amount) for sym, amount in
                 (("SPY", 1.4), ("QQQ", 0.5), ("TLT", 0.25))}  # fmt: skip
    return history, dividends, fake_rates(FIRST)


def fake_dividends(bars: list[Bar], amount: float) -> list[Dividend]:
    """A distribution on the first session of every third month (TLT: every month)."""
    out, seen = [], set()
    for b in bars:
        key = (b.date.year, b.date.month)
        if key not in seen and (amount < 0.3 or b.date.month % 3 == 0):
            out.append(Dividend(b.date, amount))
        seen.add(key)
    return out


def fake_rates(first: date) -> gym.Rates:
    steps = [(0, 0.015), (200, 0.0005), (420, -0.001), (700, 0.03), (900, 0.0475), (1300, 0.052)]
    base = datetime.combine(first, datetime.min.time(), tzinfo=UTC) + timedelta(hours=21)
    return [(base + timedelta(days=k), r) for k, r in steps]


def edge_decisions(history: dict[str, list[Bar]]) -> list[Decision]:
    rng = random.Random(5)
    syms = list(history)

    def weights() -> dict[str, float]:
        w = {s: rng.random() for s in rng.sample(syms, rng.randint(0, len(syms)))}
        total = sum(w.values())
        return {s: v / total * rng.uniform(0.3, 1.0) for s, v in w.items()} if total else {}

    out = [Decision(datetime(2018, 12, 1, tzinfo=UTC), {"SPY": 0.5})]  # before any bar
    d = date(2021, 7, 2)
    while d < date(2023, 6, 20):
        t = datetime.combine(d, gym.DECIDE_AT, tzinfo=UTC)
        out.append(Decision(t, weights()))
        if rng.random() < 0.1:  # two decisions at one time: the later one counts
            out.append(Decision(t, weights()))
        if rng.random() < 0.1:  # at an ETF open's exact time: fills at the next open
            out.append(Decision(open_time(UNIVERSE["SPY"], d + timedelta(days=1)), weights()))
        d += timedelta(days=rng.choice((1, 1, 2, 7, 12)))  # sparse: weekly gaps, longer
    out.append(Decision(datetime(2023, 7, 15, 12, tzinfo=UTC), {"BTC": 0.4}))  # after the bars
    rng.shuffle(out)  # simulate sorts them (stable: equal times keep this order)
    return out


def synthetic_results() -> dict[str, Result]:
    history, dividends, rates = synthetic()
    out = {
        name: gym.simulate(gym.backtest(decide, history, BACKTEST_FROM, LAST), history,
                           dividends=dividends, rates=rates)
        for name, decide in LIVE.items()
    }  # fmt: skip
    out["edges"] = gym.simulate(edge_decisions(history), history, dividends=dividends, rates=rates)
    out["edges_no_costs_band0"] = gym.simulate(
        edge_decisions(history),
        history,
        start_cash=12_345.0,
        costs={c: gym.Costs(0.0, 0.0) for c in (data.CRYPTO, data.ETF)},
        band=0.0,
        dividends=dividends,
        rates=rates,
    )
    out["no_decisions"] = gym.simulate([], history, dividends=dividends, rates=rates)
    return out


# --- the paper-trail record ---


def trail_root(tmp: Path) -> Path | None:
    """The record's files at TRAIL_COMMIT, extracted under `tmp`; None if the commit is not
    in this clone."""
    have = subprocess.run(["git", "-C", str(REPO), "cat-file", "-e", f"{TRAIL_COMMIT}^{{commit}}"],
                          capture_output=True, check=False)  # fmt: skip
    if have.returncode != 0:
        return None
    archive = subprocess.run(["git", "-C", str(REPO), "archive", TRAIL_COMMIT, "data", "ledger"],
                             capture_output=True, check=True)  # fmt: skip
    tmp.mkdir(parents=True, exist_ok=True)
    subprocess.run(["tar", "-x", "-C", str(tmp)], input=archive.stdout, check=True)
    return tmp


def trail_results(root: Path) -> dict[str, Result]:
    history = data.load_all(root)
    firsts = [b[0].date for b in history.values() if b]
    start, end = max(firsts) + timedelta(days=1), max(b[-1].date for b in history.values() if b)
    dividends = {s: fake_dividends(history[s], a) for s, a in (("SPY", 1.7), ("TLT", 0.3))}
    rates = fake_rates(min(firsts))
    out = {}
    for name, decide in LIVE.items():
        decisions = gym.backtest(decide, history, start, end)
        out[name] = gym.simulate(decisions, history)
        out[f"{name}+div+rates"] = gym.simulate(decisions, history, dividends=dividends,
                                                rates=rates)  # fmt: skip
    for name, res in report.live_results(root, history).items():
        out[f"ledger:{name}"] = res
    return out


def digests(results: dict[str, Result]) -> dict[str, dict[str, Any]]:
    return {name: digest(res) for name, res in results.items()}


def check(got: dict[str, dict[str, Any]], want: dict[str, dict[str, Any]]) -> None:
    assert sorted(got) == sorted(want)
    wrong = {name: (got[name], want[name]) for name in want if got[name] != want[name]}
    assert not wrong, f"replay changed for {sorted(wrong)}: {wrong}"


def golden() -> dict[str, Any]:
    out: dict[str, Any] = json.loads(FIXTURE.read_text())
    return out


def test_every_live_strategy_replays_exactly_as_recorded_on_synthetic_data() -> None:
    got = digests(synthetic_results())
    assert all(got[name]["fills"] > 0 for name in LIVE)  # each one really trades
    check(got, golden()["synthetic"])


def test_every_live_strategy_replays_exactly_as_recorded_on_the_paper_trail(tmp_path: Path) -> None:
    root = trail_root(tmp_path / "trail")
    if root is None:
        pytest.skip(f"paper-trail commit {TRAIL_COMMIT[:10]} not in this clone")
    check(digests(trail_results(root)), golden()["paper_trail"])


if __name__ == "__main__":
    if sys.argv[1:] != ["--write"]:
        sys.exit("usage: test_golden_simulate.py --write  (records the current replay as golden)")
    import tempfile

    with tempfile.TemporaryDirectory() as tmp:
        root = trail_root(Path(tmp) / "trail")
        assert root is not None, f"fetch the paper-trail branch first ({TRAIL_COMMIT[:10]})"
        fixture = {
            "trail_commit": TRAIL_COMMIT,
            "synthetic": digests(synthetic_results()),
            "paper_trail": digests(trail_results(root)),
        }
    FIXTURE.write_text(json.dumps(fixture, indent=1, sort_keys=True) + "\n")
    print(f"wrote {FIXTURE}")
