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
    # Pooled rows: a pool built only from bars up to the fit day gives the same training rows.
    for year in (1990, 2008, 2020, 2025):
        day = ml.first_friday(year)
        cut = {}
        for name, hist in ml.pool_history().items():
            short_hist = {s: [b for b in bars if b.date <= day] for s, bars in hist.items()}
            if any(short_hist.values()):
                cut[name] = harness.Panel(short_hist)
        full, short = ml.pooled_rows(day), ml.pooled_rows(day, cut)
        assert len(full) == len(short) and full.sym == short.sym
        assert (full.day == short.day).all() and (full.fwd == short.fwd).all()
        assert (full.x == short.x).all()
        print(f"pooled rows at the {year} fit: {len(full)}, the same from truncated history")
    rules["gbm-pool"] = ml.strategy(ml.GBM_POOL)
    rules["gbm-pool-low"] = ml.strategy(ml.GBM_POOL, sizing="low")
    for name, rule in rules.items():
        harness.check_against_gym(c.weekly(rule), six.hist, DAYS)
        print(f"{name}: same weights on {len(DAYS)} days with truncated history")
