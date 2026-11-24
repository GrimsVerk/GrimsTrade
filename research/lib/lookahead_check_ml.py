"""Look-ahead check for the fitted models: the fast path (one panel holding all bars, models
cached) must give the same weights as the gym's own backtest, which hands the strategy only the
bars closed before the decision and so refits every model from scratch on truncated history.
Weights saturate at 0 or 1, so two sharper checks come first: pooled rows built from truncated
history, and raw forecasts after every later bar has been scrambled.

    uv run --with numpy --with scikit-learn python research/lib/lookahead_check_ml.py
"""

from datetime import date

import common as c
import harness
import ml
import numpy as np

from grimstrade.data import UNIVERSE, Bar

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
    # Scramble test (from the code review): multiply every bar that closes after a decision
    # by random factors. Training rows, features, chosen settings, forecasts and the `low`
    # threshold at that decision must not move by a single bit.
    specs = [ml.LOGIT, ml.RIDGE, ml.GBM, ml.GBM_REG, ml.META_GBM, ml.GBM_PAY, ml.LOGIT_PAY,
             ml.TREE_PAY, ml.GBM_RAW]  # fmt: skip
    for day in (date(2003, 6, 13), date(2015, 1, 2), date(2025, 10, 31)):
        rng = np.random.default_rng(1)
        t = harness.decide_time(day)
        fake = {}
        for s, bars in six.hist.items():
            fake[s] = []
            for b in bars:
                if harness.close_time(UNIVERSE[s], b.date) > t:
                    k = float(np.exp(rng.normal(0, 0.5)))
                    b = Bar(b.date, b.open * k, b.high * k, b.low * k, b.close * k, b.volume)
                fake[s].append(b)
        v1, v2 = six.panel.view(t), harness.Panel(fake).view(t)
        fit_day = ml.first_friday(ml.fit_year(v1.today))
        r1, r2 = ml.training_rows(v1.panel, fit_day), ml.training_rows(v2.panel, fit_day)
        assert np.array_equal(r1.x, r2.x) and np.array_equal(r1.fwd, r2.fwd)
        f1, f2 = ml.rows_at(v1), ml.rows_at(v2)
        assert f1.keys() == f2.keys() and all(np.array_equal(f1[s], f2[s]) for s in f1)
        x = np.array(list(f1.values()))
        for spec in specs:
            m1, m2 = ml.model_for(v1, spec), ml.model_for(v2, spec)
            assert m1 is not None and m2 is not None and m1.setting == m2.setting
            assert np.array_equal(m1.forecast(x), m2.forecast(x)), spec.name
        g1, g2 = ml.model_for(v1, ml.GBM), ml.model_for(v2, ml.GBM)
        assert g1 is not None and g2 is not None and ml.low_for(v1, g1) == ml.low_for(v2, g2)
        print(f"{day}: later bars scrambled, {len(specs)} models forecast the same to the bit")
    for name, rule in rules.items():
        harness.check_against_gym(c.weekly(rule), six.hist, DAYS)
        print(f"{name}: same weights on {len(DAYS)} days with truncated history")
