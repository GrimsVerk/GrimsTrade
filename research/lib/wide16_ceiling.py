"""wide-16 step 1b: what `tsmom12`'s coin trades cost, and the most any cost rule could gain.

    uv run --with numpy python research/lib/wide16_ceiling.py

Descriptive, baseline only (no new rule): `tsmom12` replayed through `gym.simulate` with the
gym's costs and with zero cost on coin fills, train period only. Nothing is logged as a try
(zero-cost trading is not a rule anyone can run); one `note` row in `tries.md` by hand.
"""

from __future__ import annotations

import math
from collections import defaultdict
from datetime import date

import common as c
import harness
import numpy as np
import stats

from grimstrade import gym
from grimstrade.data import CRYPTO, ETF, UNIVERSE

COIN_ERA = date(2015, 1, 1)  # reporting split only: BTC is eligible from late 2014 in the cache


def boot_se(a: np.ndarray, b: np.ndarray, draws: int = 2000) -> tuple[float, float]:
    """Sharpe difference and its paired stationary-bootstrap SE (20-day blocks, seed 0)."""
    rng = np.random.default_rng(0)
    diffs = np.empty(draws)
    for k in range(draws):
        i = stats._stationary_indices(len(a), 20, rng)
        diffs[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
    return stats.sharpe(a) - stats.sharpe(b), float(diffs.std())


def daily(res: gym.Result) -> tuple[list[date], np.ndarray]:
    days, eq = harness._calendar(res.equity)
    return days, eq


def main() -> None:
    six = c.ctx("six")
    strat = c.weekly(c.slots(c.tsmom_signal))
    decs = harness.decisions(strat, six.panel, six.start, six.end)
    free = {CRYPTO: gym.Costs(fee=0.0, slip=0.0), ETF: gym.COSTS[ETF]}
    base = gym.simulate(decs, six.hist)
    zero = gym.simulate(decs, six.hist, costs=free)
    days, e0 = daily(base)
    _, e1 = daily(zero)
    r0, r1 = e0[1:] / e0[:-1] - 1, e1[1:] / e1[:-1] - 1
    print(
        f"tsmom12 Sharpe {stats.sharpe(r0):.3f} (logged 1.05); no coin costs {stats.sharpe(r1):.3f}"
    )

    # classify coin fills: entry (from zero), exit (to zero), drift (anything else)
    pos: dict[str, float] = defaultdict(float)
    fees: dict[str, float] = defaultdict(float)
    slip: dict[str, float] = defaultdict(float)
    vol: dict[str, float] = defaultdict(float)
    n: dict[str, int] = defaultdict(int)
    eq_by_day = dict(base.equity)
    drift_cost: list[tuple[date, float]] = []
    for f in base.fills:
        before = pos[f.symbol]
        pos[f.symbol] += f.qty
        if UNIVERSE[f.symbol] != CRYPTO:
            continue
        kind = "entry" if before <= 1e-12 else ("exit" if pos[f.symbol] <= 1e-9 else "drift")
        d = f.time.date()
        eqd = eq_by_day.get(d) or next(v for k, v in reversed(base.equity) if k <= d)
        val = abs(f.qty) * f.price
        fees[kind] += f.fee / eqd
        slip[kind] += val * gym.COSTS[CRYPTO].slip / eqd
        vol[kind] += val / eqd
        n[kind] += 1
        if kind == "drift":
            drift_cost.append((d, (f.fee + val * gym.COSTS[CRYPTO].slip) / eqd))
    years = (six.end - COIN_ERA).days / 365.25
    print(f"\ncoin fills from 2015 (cost as share of equity, per year over {years:.1f} years)")
    for k in ("entry", "exit", "drift"):
        print(f"  {k:5s}: {n[k] / years:6.1f} fills/yr, volume {vol[k] / years:5.2f} x equity/yr, "
              f"fee {fees[k] / years:.3%}/yr, slip {slip[k] / years:.3%}/yr")  # fmt: skip

    for label, a in (("whole train 1994-2025", 0), ("from 2015", (COIN_ERA - days[0]).days)):
        d, se = boot_se(r1[a:], r0[a:])
        print(f"\nceiling, {label}: dSharpe {d:+.4f}, paired SE {se:.4f}, z {d / se:+.2f}")
    # drift-only ceiling (approximate): add each coin drift fill's fee and slip back to that day's
    # return of the costed book (no compounding of the saving; a slight understatement)
    i_of = {d: k for k, d in enumerate(days)}
    add = np.zeros(len(r0))
    for d, x in drift_cost:
        k = i_of.get(d)
        if k is not None and k >= 1:
            add[k - 1] += x
    for label, a in (("whole train 1994-2025", 0), ("from 2015", (COIN_ERA - days[0]).days)):
        d, se = boot_se(r0[a:] + add[a:], r0[a:])
        print(f"drift-only ceiling, {label}: dSharpe {d:+.4f}, paired SE {se:.4f}, z {d / se:+.2f}")
    g = r1 - r0
    print(f"active return of the ceiling: mean {g.mean() * 365:.3%}/yr, "
          f"sd {g.std() * math.sqrt(365):.3%}/yr")  # fmt: skip


if __name__ == "__main__":
    main()
