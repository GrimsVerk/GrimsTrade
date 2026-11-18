"""uv run --with numpy --with scikit-learn python research/lib/idea_ml_pooled.py"""

import common as c
import ml
import mltest
import numpy as np


def extra(six: c.Ctx, runs: dict[str, c.Run]) -> list[str]:
    day = ml.first_friday(ml.fit_year(six.end))
    out = ["## Training rows at the last fit, by set", ""]
    out += ["| Set | Assets | Rows | Share that went up |", "|---|---:|---:|---:|"]
    total = 0
    for name, panel in ml.pool_panels().items():
        rows = ml.pooled_rows(day, {name: panel})
        total += len(rows)
        out.append(f"| {name} | {len(panel.syms)} | {len(rows)} | {np.mean(rows.fwd > 0):.1%} |")
    own = len(ml.training_rows(six.panel, day))
    out += ["", f"{total} rows in all, against {own} for the six-asset models.", ""]
    out += ["## Settings chosen by purged CV (six assets)", ""]
    out += mltest.settings_section(six, [ml.LOGIT_POOL]) + [""]
    return out


if __name__ == "__main__":
    mltest.standard(
        "ml-pooled",
        "ml-pooled: the same models trained on 33 markets instead of six",
        {
            "gbm-pool": c.weekly(ml.strategy(ml.GBM_POOL)),
            "logit-pool": c.weekly(ml.strategy(ml.LOGIT_POOL)),
            "gbm-pool-low": c.weekly(ml.strategy(ml.GBM_POOL, sizing="low", tag="gbm-pool-low")),
        },
        {"tsmom12": c.weekly(c.slots(c.tsmom_signal))},
        also={"gbm": c.weekly(ml.strategy(ml.GBM)), "logit": c.weekly(ml.strategy(ml.LOGIT))},
        extra=extra,
        skill_tags={"gbm-pool": 0.5, "logit-pool": 0.5, "gbm": 0.5, "logit": 0.5},
    )
