"""The owner's risk presets from the risk map (research run 3, `research/risk-map.md`), live in
paper side by side so their forward records can be compared (owner 2026-11-12: run all of them).

- Careful: trend rule + tight swing cap (20% a year), 5% of the account per coin.
- Middle: plain trend rule, 10% of the account per coin.
- Bold: hold all six in equal parts; that is the `equal_weight` benchmark, already live.

Same rule as `research/lib/risk_map.py` `menu()`, nothing tuned on our data:
1. Eligible assets are those with a year of bars (365 for crypto, 252 for ETFs).
2. Slots: each eligible coin gets the crypto size; the rest of the account is split equally over
   the eligible ETFs (if no ETF is eligible, coins keep only their own slots; the rest is cash).
3. Trend rule: a slot is held only while the asset's 12-month return is positive, else cash.
4. Swing cap (Careful only): the slot is scaled by min(1, cap / vol), where vol is the
   annualised root mean square of the last 20 daily log returns. The leftover is cash.
"""

import math
from collections.abc import Callable

from grimstrade.data import CRYPTO, UNIVERSE, History
from grimstrade.signals import BARS_PER_YEAR, trailing_return

LOOKBACK_DAYS = 365  # 12 months
VOL_BARS = 20

Decide = Callable[[History], tuple[dict[str, float], str]]


def vol20(closes: list[float], per_year: int) -> float | None:
    """Annualised zero-mean volatility of the last 20 daily log returns (None if too few)."""
    if len(closes) < VOL_BARS + 1:
        return None
    tail = closes[-(VOL_BARS + 1) :]
    lr = [math.log(b / a) for a, b in zip(tail, tail[1:], strict=False) if a > 0 and b > 0]
    if not lr:
        return None
    return math.sqrt(sum(x * x for x in lr) / len(lr) * per_year)


def preset(name: str, crypto_size: float, cap: float | None) -> Decide:
    def decide(history: History) -> tuple[dict[str, float], str]:
        held = [s for s, bars in sorted(history.items())
                if len(bars) >= BARS_PER_YEAR[UNIVERSE[s]]]  # fmt: skip
        if not held:
            return {}, f"{name}: no asset has a year of history yet, stay in cash"
        coins = [s for s in held if UNIVERSE[s] == CRYPTO]
        rest = [s for s in held if UNIVERSE[s] != CRYPTO]
        slot = {s: crypto_size for s in coins}
        if rest:
            slot.update({s: (1 - crypto_size * len(coins)) / len(rest) for s in rest})
        weights: dict[str, float] = {}
        notes = []
        for s in held:
            bars = history[s]
            r = trailing_return(bars, LOOKBACK_DAYS)
            if r is None or r <= 0:
                notes.append(f"{s} out")
                continue
            w = slot[s]
            if cap is not None:
                vol = vol20([b.close for b in bars], BARS_PER_YEAR[UNIVERSE[s]])
                if vol:
                    w *= min(1.0, cap / vol)
            if w > 0:
                weights[s] = w
                notes.append(f"{s} {w:.0%}")
        return weights, f"{name}: " + ", ".join(notes)

    return decide


careful = preset("careful", crypto_size=0.05, cap=0.20)
middle = preset("middle", crypto_size=0.10, cap=None)
