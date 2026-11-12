"""uv run --with numpy python research/lib/idea_vol_target.py"""

import common as c
import rules
import testkit

if __name__ == "__main__":
    testkit.standard(
        "vol-target",
        "vol-target: cap each slot by an absolute volatility budget",
        {f"t{t}": c.weekly(rules.vol_target(t / 100)) for t in (40, 25)},
        {"equal-weight": c.weekly(c.equal_weight), "inverse-vol": c.weekly(c.inverse_vol)},
        per_asset=False,
    )
