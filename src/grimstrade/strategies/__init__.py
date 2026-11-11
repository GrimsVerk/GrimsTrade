"""Strategies: one file each, one function `decide(history) -> (target weights, reason)`.

`history` holds only bars closed before the decision. Weights are shares of equity, >= 0, sum <= 1;
the rest is cash. Add a strategy: new file, add it to LIVE and NOTES (the runner registers the try
in `ledger/tries.jsonl` on its next run; see AGENTS.md).
"""

from grimstrade.gym import Strategy
from grimstrade.strategies import (
    buy_hold_btc,
    buy_hold_spy,
    crypto_mean_reversion,
    equal_weight,
    risk_parity,
    sixty_forty,
    ts_momentum,
    vol_target,
    xs_momentum,
)

# name -> strategy. Names are permanent: they key the ledger.
LIVE: dict[str, Strategy] = {
    "buy_hold_btc": buy_hold_btc.decide,
    "buy_hold_spy": buy_hold_spy.decide,
    "sixty_forty": sixty_forty.decide,
    "equal_weight": equal_weight.decide,
    "ts_momentum": ts_momentum.decide,
    "xs_momentum": xs_momentum.decide,
    "vol_target_spy": vol_target.decide,
    "risk_parity": risk_parity.decide,
    "crypto_mean_reversion": crypto_mean_reversion.decide,
}

# The yardsticks every other strategy must beat after costs.
BENCHMARKS = ("buy_hold_btc", "buy_hold_spy", "sixty_forty", "equal_weight")

# name -> note for its line in ledger/tries.jsonl (written once, the first time it runs).
NOTES: dict[str, str] = {
    **{name: "benchmark (M0)" for name in BENCHMARKS},
    "ts_momentum": "M1 classic: time-series momentum, Moskowitz/Ooi/Pedersen 2012, paper params",
    "xs_momentum": "M1 classic: cross-sectional momentum 6/6, Jegadeesh/Titman 1993, top third",
    "vol_target_spy": "M1 classic: SPY vol targeting 10%, 1-month vol, Moreira/Muir 2017",
    "risk_parity": "M1 classic: inverse-vol risk parity, 3y vol, Asness/Frazzini/Pedersen 2012",
    "crypto_mean_reversion": "M1 classic: BTC/ETH RSI(2)<10 above 200d SMA, exit >5d SMA, Connors",
}
