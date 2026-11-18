"""uv run --with numpy --with scikit-learn python research/lib/idea_ml_gbm.py"""

import common as c
import ml
import mltest
import numpy as np


def extra(six: c.Ctx, runs: dict[str, c.Run]) -> list[str]:
    out = ["## Settings chosen by purged CV (six assets)", ""]
    out += mltest.settings_section(six, [ml.GBM_CV]) + [""]
    year = ml.fit_year(six.end)
    model = six.panel.cache[("ml-model", "gbm", year)]
    assert isinstance(model, ml.Fitted)
    rows = ml.training_rows(six.panel, ml.first_friday(year))
    imp = ml.permutation_importance(model, rows)
    out += ["## What the last `gbm` model leans on", ""]
    out += ["Drop in AUC on its own training rows when one feature is shuffled (in-sample: it "
            "shows what the model uses, not what is true):", ""]  # fmt: skip
    out += [", ".join(f"`{n}` {v:+.3f}" for n, v in imp), ""]
    return out


def more_bars(runs: dict[str, c.Run]) -> list[mltest.Bar]:
    gbm, logit, twin = (c.describe(runs[n])["sharpe"] for n in ("gbm", "logit", "tsmom12"))
    sweep = [c.describe(runs[s.name])["sharpe"] for s in ml.GBM_SWEEP]
    med = float(np.median(sweep))
    return [
        ("6. Not behind `ml-linear/logit` on Sharpe", gbm >= logit, f"{gbm:.2f} vs {logit:.2f}"),
        ("7. Median Sharpe of the five sweep settings ahead of `tsmom12`", med > twin,
         f"{med:.2f} vs {twin:.2f}; sweep " + ", ".join(f"{x:.2f}" for x in sweep)),
    ]  # fmt: skip


if __name__ == "__main__":
    variants = {
        "gbm": c.weekly(ml.strategy(ml.GBM)),
        "gbm-hard": c.weekly(ml.strategy(ml.GBM, hard=True, tag="gbm-hard")),
        "gbm-reg": c.weekly(ml.strategy(ml.GBM_REG)),
        "gbm-cv": c.weekly(ml.strategy(ml.GBM_CV)),
    }
    variants |= {s.name: c.weekly(ml.strategy(s)) for s in ml.GBM_SWEEP}
    tags = {n: 0.5 for n in variants if n != "gbm-hard"} | {"gbm-reg": 0.0, "logit": 0.5}
    mltest.standard(
        "ml-gbm",
        "ml-gbm: gradient boosting on simple features",
        variants,
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal)), "sma200": c.weekly(c.slots(c.sma_signal))},
        also={"logit": c.weekly(ml.strategy(ml.LOGIT))},
        extra=extra,
        more_bars=more_bars,
        skill_tags=tags,
    )
