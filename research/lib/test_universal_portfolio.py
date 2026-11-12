"""uv run --with numpy python research/lib/test_universal_portfolio.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "universal-portfolio",
        "universal-portfolio: Cover's universal portfolio",
        {"up": c.weekly(rules.universal_portfolio)},
        {
            "equal-weight": c.weekly(c.equal_weight),
            "uniform-cash": c.weekly(rules.uniform_with_cash),
        },
        per_asset=False,
        fresh_twins=False,
    )
