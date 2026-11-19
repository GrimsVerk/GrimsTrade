"""uv run --with numpy --with scikit-learn python research/lib/idea_ml_payoff.py"""

import common as c
import ml
import mltest
from sklearn.tree import export_text


def extra(six: c.Ctx, runs: dict[str, c.Run]) -> list[str]:
    out = ["## The two-question rule `tree-pay` found", ""]
    out += ["At three of its yearly fits (left branch = condition true; class 1.0 = hold):", ""]
    for year in (2000, 2012, ml.fit_year(six.end)):
        model = six.panel.cache.get(("ml-model", "tree-pay", year))
        if isinstance(model, ml.Fitted):
            text = export_text(model.est, feature_names=ml.FEATURES, decimals=2)
            out += [f"Fit of {year} ({model.n_rows} rows):", "", "```", text.rstrip(), "```", ""]
    out += ["## Settings chosen by purged CV (six assets)", ""]
    out += mltest.settings_section(six, [ml.LOGIT_PAY]) + [""]
    return out


def hard(spec: ml.Spec) -> c.ResearchStrategy:
    return c.weekly(ml.strategy(spec, sizing="hard"))


if __name__ == "__main__":
    mltest.standard(
        "ml-payoff",
        "ml-payoff: train the model on what a position earns, not on which way the price goes",
        {
            "gbm-pay": hard(ml.GBM_PAY),
            "logit-pay": hard(ml.LOGIT_PAY),
            "tree-pay": hard(ml.TREE_PAY),
            "gbm-raw": hard(ml.GBM_RAW),
        },
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal))},
        also={"gbm": c.weekly(ml.strategy(ml.GBM)), "logit": c.weekly(ml.strategy(ml.LOGIT))},
        extra=extra,
        skill_tags={
            "gbm-pay": 0.5,
            "logit-pay": 0.5,
            "tree-pay": 0.5,
            "gbm-raw": 0.0,
            "gbm": 0.5,
            "logit": 0.5,
        },  # fmt: skip
        payoff=True,
    )
