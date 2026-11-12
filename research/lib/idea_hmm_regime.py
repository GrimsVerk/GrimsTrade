"""uv run --with numpy --with numba python research/lib/idea_hmm_regime.py"""

import common as c
import rules_fit
import testkit

if __name__ == "__main__":
    testkit.standard(
        "hmm-regime",
        "hmm-regime: a two-state hidden Markov model as a risk switch",
        {"hard": c.weekly(c.slots(rules_fit.hmm_hard)), "soft": c.weekly(rules_fit.hmm_soft)},
        {
            "vol-calm": c.weekly(c.slots(c.vol_calm_signal)),
            "sma200": c.weekly(c.slots(c.sma_signal)),
        },
        per_asset=True,
    )
