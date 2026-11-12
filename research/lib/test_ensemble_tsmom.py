"""uv run --with numpy python research/lib/test_ensemble_tsmom.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "ensemble-tsmom",
        "ensemble-tsmom: trend measured at four horizons at once",
        {"e4": c.weekly(rules.ensemble_tsmom)},
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal)), "sma200": c.weekly(c.slots(c.sma_signal))},
        per_asset=True,
    )
