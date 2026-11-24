"""wide-16 post hoc (after the one real run of `cost-band`): fee saving or drift bet?

    uv run --with numpy python research/lib/wide16_posthoc.py

Not a try: the rule and `tsmom12` replayed with coin fills free (not tradable), to split the
gain into the fee saved and the return of letting coin slots drift; and the coin share of the
book while coins are held. Nothing is logged.
"""

from __future__ import annotations

from datetime import date

import common as c
import harness
import numpy as np
import stats
import wide16

from grimstrade import gym
from grimstrade.data import CRYPTO, ETF, UNIVERSE


def rets(res: gym.Result) -> np.ndarray:
    _, eq = harness._calendar(res.equity)
    out: np.ndarray = eq[1:] / eq[:-1] - 1
    return out


def coin_share(res: gym.Result, hist: dict[str, list], first: date) -> float:
    """Mean share of equity in coins at each day's end, over days with a coin held."""
    pos: dict[str, float] = {s: 0.0 for s in hist}
    close = {s: {b.date: b.close for b in bars} for s, bars in hist.items()}
    last: dict[str, float] = {}
    fills = sorted(res.fills, key=lambda f: f.time)
    j, shares = 0, []
    for d, e in res.equity:
        while j < len(fills) and fills[j].time.date() <= d:
            pos[fills[j].symbol] += fills[j].qty
            j += 1
        for s in hist:
            if d in close[s]:
                last[s] = close[s][d]
        coin = sum(q * last.get(s, 0.0) for s, q in pos.items() if UNIVERSE[s] == CRYPTO)
        if d >= first and coin > 1e-9 * e:
            shares.append(coin / e)
    return float(np.mean(shares)) if shares else float("nan")


def main() -> None:
    free = {CRYPTO: gym.Costs(fee=0.0, slip=0.0), ETF: gym.COSTS[ETF]}
    for name in ("six", "coin"):
        ctx = c.ctx(name)
        decs = harness.decisions(wide16.rule(), ctx.panel, ctx.start, ctx.end)
        first = max(wide16.COIN_ERA, ctx.start)
        base = gym.simulate(decs, ctx.hist)
        base_free = gym.simulate(decs, ctx.hist, costs=free)
        print(f"\n{name}: `tsmom12` coin share while held {coin_share(base, ctx.hist, first):.3f}")
        for v, b in wide16.BANDS.items():
            r = gym.simulate(decs, ctx.hist, band=b)
            r_free = gym.simulate(decs, ctx.hist, band=b, costs=free)
            total = stats.sharpe(rets(r)) - stats.sharpe(rets(base))
            drift = stats.sharpe(rets(r_free)) - stats.sharpe(rets(base_free))
            print(f"  {v}: dSharpe {total:+.4f} = drift bet (coin fills free) {drift:+.4f} "
                  f"+ fees and tiers {total - drift:+.4f}; coin share while held "
                  f"{coin_share(r, ctx.hist, first):.3f}")  # fmt: skip


if __name__ == "__main__":
    main()
