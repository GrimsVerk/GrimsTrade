"""Crypto short-term mean reversion: Connors' RSI(2) rule (Connors & Alvarez 2008, "Short Term
Trading Strategies That Work"), the textbook version of the short-term reversal effect
(Lehmann 1990), applied to BTC and ETH.

Per coin, with the common published parameters: buy after a sharp short dip (2-day RSI under
10; the book's tested system uses 5) but only in an uptrend (close above its 200-day average);
sell once the close is back above its 5-day average. Each coin in a trade gets half the money;
otherwise cash. Signals fill about a day later than Connors' (docs/DECISIONS.md, execution
timing).

The rule depends on whether we are already in a trade, so it is replayed over the coin's whole
visible history on every decision (no hidden state; the same answer live and in a backtest).
"""

from collections.abc import Sequence

from grimstrade.data import Bar, History

COINS = ("BTC", "ETH")
RSI_DAYS = 2
ENTRY_RSI = 10.0
TREND_DAYS = 200
EXIT_DAYS = 5


def in_trade(bars: Sequence[Bar]) -> tuple[bool, str]:
    """Replay the rule over `bars`; return whether a trade is open after the last bar, and why."""
    closes = [b.close for b in bars]
    if len(closes) < TREND_DAYS:
        return False, f"under {TREND_DAYS} days of history"
    prefix = [0.0]
    for c in closes:
        prefix.append(prefix[-1] + c)

    def mean_through(i: int, days: int) -> float:
        return (prefix[i + 1] - prefix[i + 1 - days]) / days

    avg_gain = avg_loss = 0.0
    holding = False
    why = ""
    for i in range(1, len(closes)):
        change = closes[i] - closes[i - 1]
        gain, loss = max(change, 0.0), max(-change, 0.0)
        if i <= RSI_DAYS:  # seed Wilder's averages with a plain mean
            avg_gain += gain / RSI_DAYS
            avg_loss += loss / RSI_DAYS
            continue
        avg_gain = (avg_gain * (RSI_DAYS - 1) + gain) / RSI_DAYS
        avg_loss = (avg_loss * (RSI_DAYS - 1) + loss) / RSI_DAYS
        if i + 1 < TREND_DAYS:
            continue
        rsi = 100.0 if avg_loss == 0 else 100 - 100 / (1 + avg_gain / avg_loss)
        trend, fast = mean_through(i, TREND_DAYS), mean_through(i, EXIT_DAYS)
        if holding and closes[i] > fast:
            holding, why = False, f"exit: close above {EXIT_DAYS}-day average"
        elif not holding and closes[i] > trend and rsi < ENTRY_RSI:
            holding, why = True, f"entry: RSI(2) {rsi:.0f} in an uptrend"
    if not why:
        why = "no signal yet"
    return holding, ("holding, last " if holding else "flat, last ") + why


def decide(history: History) -> tuple[dict[str, float], str]:
    weights: dict[str, float] = {}
    notes = []
    for coin in COINS:
        holding, why = in_trade(history.get(coin, []))
        if holding:
            weights[coin] = 1 / len(COINS)
        notes.append(f"{coin} {why}")
    return weights, "crypto RSI(2) mean reversion: " + "; ".join(notes)
