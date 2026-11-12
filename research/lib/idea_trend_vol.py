"""uv run --with numpy python research/lib/idea_trend_vol.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "trend-vol",
        "trend-vol: 12-month trend, with each slot capped by volatility",
        {"tv40": c.weekly(rules.trend_vol(0.40))},
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal))},
        per_asset=True,
    )
