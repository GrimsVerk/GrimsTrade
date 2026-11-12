"""Risk parity, inverse-volatility version (Asness, Frazzini & Pedersen 2012, "Leverage aversion
and risk parity", FAJ).

Each asset gets a weight proportional to 1 / its volatility, so each contributes roughly the same
risk; weights sum to 100% (the paper levers the result up to a volatility target; we can't lever).
Volatility: the paper's 3-year rolling window, here of daily returns. An asset needs at least one
year of history to be included (we start with about two years of data).
"""

from datetime import timedelta

from grimstrade.data import UNIVERSE, History
from grimstrade.signals import BARS_PER_YEAR, daily_returns, realized_vol

WINDOW_DAYS = 3 * 365
MIN_DAYS = 365


def decide(history: History) -> tuple[dict[str, float], str]:
    inverse: dict[str, float] = {}
    vols: dict[str, float] = {}
    for sym, bars in sorted(history.items()):
        if not bars or bars[-1].date - bars[0].date < timedelta(days=MIN_DAYS):
            continue
        window = [b for b in bars if b.date > bars[-1].date - timedelta(days=WINDOW_DAYS)]
        vol = realized_vol(daily_returns(window), BARS_PER_YEAR[UNIVERSE[sym]])
        if vol:
            vols[sym] = vol
            inverse[sym] = 1 / vol
    if not inverse:
        return {}, "risk parity: no asset has a year of history yet, stay in cash"
    total = sum(inverse.values())
    weights = {s: v / total for s, v in inverse.items()}
    notes = ", ".join(f"{s} vol {vols[s]:.0%} -> {weights[s]:.0%}" for s in weights)
    return weights, f"risk parity (inverse vol, 3y): {notes}"
