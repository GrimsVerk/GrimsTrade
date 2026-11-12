"""uv run --with numpy python research/lib/idea_trend_to_safe.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "trend-to-safe",
        "trend-to-safe: bonds or gold instead of cash when a risk asset is out of trend",
        {"safe": c.weekly(rules.trend_to_safe)},
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal))},
        per_asset=True,
        sets=("etf",),
    )
