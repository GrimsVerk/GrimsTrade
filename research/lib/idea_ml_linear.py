"""uv run --with numpy --with scikit-learn python research/lib/idea_ml_linear.py"""

import common as c
import ml
import mltest


def extra(six: c.Ctx, runs: dict[str, c.Run]) -> list[str]:
    out = ["## Settings chosen by purged CV (six assets)", ""]
    out += mltest.settings_section(six, [ml.LOGIT, ml.RIDGE]) + [""]
    model = six.panel.cache[("ml-model", "logit", ml.fit_year(six.end))]
    assert isinstance(model, ml.Fitted)
    coef = model.est[-1].coef_[0]
    order = sorted(zip(ml.FEATURES, coef, strict=True), key=lambda t: -abs(t[1]))
    out += ["## What the last logistic model weighs (standardised coefficients)", ""]
    out += [", ".join(f"`{n}` {v:+.2f}" for n, v in order), ""]
    return out


if __name__ == "__main__":
    mltest.standard(
        "ml-linear",
        "ml-linear: a regularised linear model on simple features",
        {
            "logit": c.weekly(ml.strategy(ml.LOGIT)),
            "logit-hard": c.weekly(ml.strategy(ml.LOGIT, hard=True, tag="logit-hard")),
            "ridge": c.weekly(ml.strategy(ml.RIDGE)),
        },
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal)), "sma200": c.weekly(c.slots(c.sma_signal))},
        extra=extra,
        skill_tags={"logit": 0.5, "ridge": 0.0},
    )
