"""Benchmark: all in SPY, always."""

from grimstrade.data import History


def decide(history: History) -> tuple[dict[str, float], str]:
    return {"SPY": 1.0}, "benchmark: buy and hold SPY"
