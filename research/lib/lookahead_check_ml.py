"""Look-ahead check for the fitted models: the fast path (one panel holding all bars, models
cached) must give the same weights as the gym's own backtest, which hands the strategy only the
bars closed before the decision and so refits every model from scratch on truncated history.

    uv run --with numpy --with scikit-learn python research/lib/lookahead_check_ml.py
"""

from datetime import date

import common as c
import harness
import ml

DAYS = [date(1996, 5, 17), date(2003, 6, 13), date(2012, 3, 7), date(2020, 3, 20),
        date(2025, 1, 3), date(2025, 10, 31)]  # fmt: skip

if __name__ == "__main__":
    six = c.ctx("six")
    rules = {
        "logit": ml.strategy(ml.LOGIT),
        "ridge": ml.strategy(ml.RIDGE),
        "gbm": ml.strategy(ml.GBM),
        "gbm-reg": ml.strategy(ml.GBM_REG),
        "meta-gbm": ml.strategy(ml.META_GBM),
        "gbm-low": ml.strategy(ml.GBM, sizing="low"),
        "gbm-pay": ml.strategy(ml.GBM_PAY, sizing="hard"),
        "logit-pay": ml.strategy(ml.LOGIT_PAY, sizing="hard"),
        "tree-pay": ml.strategy(ml.TREE_PAY, sizing="hard"),
        "gbm-raw": ml.strategy(ml.GBM_RAW, sizing="hard"),
    }
    for name, rule in rules.items():
        harness.check_against_gym(c.weekly(rule), six.hist, DAYS)
        print(f"{name}: same weights on {len(DAYS)} days with truncated history")
