"""uv run --with numpy --with scikit-learn python research/lib/idea_ml_sizing.py"""

import common as c
import ml
import mltest


def rule(spec: ml.Spec, sizing: str) -> c.ResearchStrategy:
    return c.weekly(ml.strategy(spec, sizing=sizing, tag=f"{spec.name}-{sizing}"))


if __name__ == "__main__":
    mltest.standard(
        "ml-sizing",
        "ml-sizing: the same models with a position rule that follows the forecast",
        {
            "gbm-prop": rule(ml.GBM, "prop"),
            "logit-prop": rule(ml.LOGIT, "prop"),
            "gbm-low": rule(ml.GBM, "low"),
            "logit-low": rule(ml.LOGIT, "low"),
            "gbm-reg-prop": rule(ml.GBM_REG, "prop"),
            "ridge-prop": rule(ml.RIDGE, "prop"),
        },
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal))},
        also={"gbm": c.weekly(ml.strategy(ml.GBM)), "logit": c.weekly(ml.strategy(ml.LOGIT))},
    )
