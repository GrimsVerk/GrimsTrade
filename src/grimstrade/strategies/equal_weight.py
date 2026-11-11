"""Benchmark: equal weight across every universe asset that has data."""

from grimstrade.data import History


def decide(history: History) -> tuple[dict[str, float], str]:
    live = sorted(s for s, bars in history.items() if bars)
    if not live:
        return {}, "benchmark: equal weight (no data yet, stay in cash)"
    return {s: 1.0 / len(live) for s in live}, f"benchmark: equal weight over {len(live)} assets"
