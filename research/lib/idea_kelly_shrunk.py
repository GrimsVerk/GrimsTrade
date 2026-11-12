"""uv run --with numpy python research/lib/idea_kelly_shrunk.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "kelly-shrunk",
        "kelly-shrunk: fractional Kelly under an equal-Sharpe prior",
        {f"k{k}": c.weekly(rules.kelly(k)) for k in (0.2, 0.1, 0.4)},
        {"inverse-vol": c.weekly(c.inverse_vol)},
        per_asset=False,
    )
