"""Benchmark: all in BTC, always."""

from grimstrade.data import History


def decide(history: History) -> tuple[dict[str, float], str]:
    return {"BTC": 1.0}, "benchmark: buy and hold BTC"
