"""uv run --with numpy --with scikit-learn python research/lib/idea_ml_filter.py"""

import common as c
import ml
import mltest

if __name__ == "__main__":
    mltest.standard(
        "ml-filter",
        "ml-filter: the 12-month trend rule with a model deciding how much to trust it",
        {
            "meta-gbm": c.weekly(ml.strategy(ml.META_GBM)),
            "meta-logit": c.weekly(ml.strategy(ml.META_LOGIT)),
            "and-gbm": c.weekly(ml.strategy(ml.GBM, trend_only=True, tag="and-gbm")),
        },
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal))},
        skill_tags={"meta-gbm": 0.5, "meta-logit": 0.5},
    )
