"""Strategies: one file each, one function `decide(history) -> (target weights, reason)`.

`history` holds only bars closed before the decision. Weights are shares of equity, >= 0, sum <= 1;
the rest is cash. Add a strategy: new file, add it to LIVE, register a try (see AGENTS.md).
"""

from grimstrade.gym import Strategy
from grimstrade.strategies import buy_hold_btc, buy_hold_spy, equal_weight, sixty_forty

# name -> strategy. Names are permanent: they key the ledger.
LIVE: dict[str, Strategy] = {
    "buy_hold_btc": buy_hold_btc.decide,
    "buy_hold_spy": buy_hold_spy.decide,
    "sixty_forty": sixty_forty.decide,
    "equal_weight": equal_weight.decide,
}
