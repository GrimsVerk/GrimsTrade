"""Time-series momentum (Moskowitz, Ooi & Pedersen 2012, "Time series momentum", JFE).

Paper's standard setup: each asset's signal is the sign of its own past 12-month return; each
position is scaled to 40% annualised volatility using an exponentially weighted volatility
estimate with a 60-day center of mass; assets are equally weighted.

Our gym is long-only and unlevered, so: an asset with a positive 12-month return gets
min(1, 40% / vol) / N of equity, where N counts the assets with 12 months of history; a negative
signal means cash instead of a short. Zero risk-free rate (docs/DECISIONS.md), so the 12-month
return stands in for the excess return.
"""

from grimstrade.data import UNIVERSE, History
from grimstrade.signals import BARS_PER_YEAR, daily_returns, ewma_vol, trailing_return

LOOKBACK_DAYS = 365  # 12 months
TARGET_VOL = 0.40
CENTER_OF_MASS = 60  # days


def decide(history: History) -> tuple[dict[str, float], str]:
    signals: dict[str, float] = {}
    for sym, bars in sorted(history.items()):
        r = trailing_return(bars, LOOKBACK_DAYS)
        if r is not None:
            signals[sym] = r
    if not signals:
        return {}, "ts momentum: no asset has 12 months of history yet, stay in cash"
    n = len(signals)
    weights: dict[str, float] = {}
    notes = []
    for sym, r in signals.items():
        if r <= 0:
            notes.append(f"{sym} {r:+.0%} out")
            continue
        per_year = BARS_PER_YEAR[UNIVERSE[sym]]
        vol = ewma_vol(daily_returns(history[sym]), CENTER_OF_MASS, per_year)
        if not vol:
            continue
        weights[sym] = min(1.0, TARGET_VOL / vol) / n
        notes.append(f"{sym} {r:+.0%} in (vol {vol:.0%})")
    return weights, "ts momentum 12m: " + ", ".join(notes)
