"""Benchmark: 60% SPY, 40% TLT, rebalanced when drift passes the gym's band."""

from grimstrade.data import History


def decide(history: History) -> tuple[dict[str, float], str]:
    return {"SPY": 0.6, "TLT": 0.4}, "benchmark: 60/40 SPY/TLT"
