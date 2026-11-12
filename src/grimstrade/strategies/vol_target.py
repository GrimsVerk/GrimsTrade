"""Volatility targeting on SPY, in the style of Harvey et al. 2018 ("The impact of volatility
targeting", JPM); the idea's academic case is Moreira & Muir 2017 ("Volatility-managed
portfolios", JF), who scale by inverse variance, monthly, with leverage.

Hold SPY scaled by target / recent volatility: less stock when markets are wild, more when calm.
Volatility is the realized volatility of the last month of daily returns (21 trading days, i.e. one
month); the target is 10% a year (Harvey et al.'s standard). Unlevered: at most 100% SPY,
the rest in cash. Compare it with buy_hold_spy.
"""

from grimstrade.data import UNIVERSE, History
from grimstrade.signals import BARS_PER_YEAR, daily_returns, realized_vol

ASSET = "SPY"
TARGET_VOL = 0.10
WINDOW = 21  # trading days, one month


def decide(history: History) -> tuple[dict[str, float], str]:
    bars = history.get(ASSET, [])
    vol = realized_vol(daily_returns(bars[-(WINDOW + 1) :]), BARS_PER_YEAR[UNIVERSE[ASSET]])
    if len(bars) < WINDOW + 1 or not vol:
        return {}, f"vol target: under {WINDOW} days of {ASSET} returns, stay in cash"
    w = min(1.0, TARGET_VOL / vol)
    return {ASSET: w}, f"vol target {TARGET_VOL:.0%}: {ASSET} 1-month vol {vol:.1%} -> {w:.0%}"
