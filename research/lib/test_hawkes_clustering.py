"""uv run --with numpy --with numba python research/lib/test_hawkes_clustering.py"""

import common as c
import rules_fit
import testkit

if __name__ == "__main__":
    testkit.standard(
        "hawkes-clustering",
        "hawkes-clustering: self-exciting crash days",
        {"down2": c.weekly(c.slots(rules_fit.hawkes_quiet))},
        {"vol-calm": c.weekly(c.slots(c.vol_calm_signal))},
        per_asset=True,
    )
