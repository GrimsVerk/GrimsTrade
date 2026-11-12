"""uv run --with numpy python research/lib/test_fracdiff_momentum.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "fracdiff-momentum",
        "fracdiff-momentum: a power-law memory for trend",
        {f"d{d}": c.weekly(c.slots(rules.fracdiff_signal(d))) for d in (0.4, 0.3, 0.5)},
        {
            "tsmom12-k": c.weekly(c.slots(rules.warmed(c.tsmom_signal))),
            "sma200-k": c.weekly(c.slots(rules.warmed(c.sma_signal))),
        },
        per_asset=True,
        fresh_twins=True,
        note="Twins `-k` are the plain twins switched on only after the rule's own two-year "
        "window, so warm-up does not decide the comparison.",
    )
