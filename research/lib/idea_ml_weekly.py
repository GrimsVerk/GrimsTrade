"""ML_HORIZON=7 uv run --with numpy --with scikit-learn python research/lib/idea_ml_weekly.py"""

import common as c
import ml
import mltest


def extra(six: c.Ctx, runs: dict[str, c.Run]) -> list[str]:
    out = ["## Settings chosen by purged CV (six assets)", ""]
    return out + mltest.settings_section(six, [ml.LOGIT_WK]) + [""]


if __name__ == "__main__":
    assert ml.HORIZON == 7, "run with ML_HORIZON=7"
    mltest.standard(
        "ml-weekly",
        "ml-weekly: the same models forecasting one week ahead instead of four",
        {
            "gbm-wk": c.weekly(ml.strategy(ml.GBM_WK)),
            "logit-wk": c.weekly(ml.strategy(ml.LOGIT_WK)),
            "gbm-wk-low": c.weekly(ml.strategy(ml.GBM_WK, sizing="low", tag="gbm-wk-low")),
        },
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal))},
        extra=extra,
        skill_tags={"gbm-wk": 0.5, "logit-wk": 0.5},
    )
