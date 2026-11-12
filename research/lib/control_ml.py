"""Positive control for the ML machinery: does it find an edge when one is there?

A 16th feature is planted that really does know the future: `peek` = rho x (the row's own
28-day risk-adjusted return) + noise, so its correlation with the outcome is about rho. This
is deliberate look-ahead and could never be traded; nothing here is a strategy and nothing is
logged as a try. If the same code that found nothing in the real features turns a planted
signal into forecast skill and into Sharpe, the null result is not a plumbing fault. It also
shows how big an edge has to be before 32 years of data can reveal it.

    uv run --with numpy --with scikit-learn python research/lib/control_ml.py
"""

from __future__ import annotations

import math
import zlib

import common as c
import ml
import mltest
import numpy as np

RHOS = (0.0, 0.03, 0.05, 0.10, 0.20)


def _noise(day: int, sym: str) -> float:
    return float(np.random.default_rng([int(day), zlib.crc32(sym.encode())]).standard_normal())


def with_peek(rows: ml.Rows, rho: float) -> ml.Rows:
    vol = np.exp(rows.x[:, ml.LOG_VOL])
    ra = np.clip(rows.fwd / (vol * math.sqrt(ml.HORIZON / 365)), -3, 3)
    eps = np.array([_noise(d, s) for d, s in zip(rows.day, rows.sym, strict=True)])
    peek = rho * ra + math.sqrt(1 - rho**2) * eps
    return ml.Rows(rows.day, np.column_stack([rows.x, peek]), rows.fwd, rows.sym)


def strategy(spec: ml.Spec, rho: float, tag: str, sizing: str = "base") -> c.ResearchStrategy:
    def f(view: c.View) -> c.Weights:
        memo = view.panel.cache
        year = ml.fit_year(view.today)
        key = ("ctl-model", spec.name, rho, year)
        if key not in memo:
            train = with_peek(ml.training_rows(view.panel, ml.first_friday(year)), rho)
            model = ml.fit(spec, train)
            memo[key] = (model, ml.oof_quantile(model, train))
        model, low = memo[key]  # type: ignore[misc]
        held = c.live(view)
        rows = with_peek(ml.labelled(view.panel, view.today), rho)  # LOOKS AHEAD: control only
        if not len(rows):
            return {}
        fc, q = model.forecast(rows.x), model.confidence(rows.x)
        log = memo.setdefault(("ml-fc", tag), {})
        out = {}
        for s, p, qi in zip(rows.sym, fc, q, strict=True):
            log[(view.today, s)] = float(p)  # type: ignore[index]
            w = ml.position(sizing, float(p), float(qi), low)
            if s in held and w > 0:
                out[s] = w / len(held)
        return out

    return f


def main() -> None:
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline",
                log=False)  # fmt: skip
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    out = [
        "# Positive control: can the ML machinery find an edge that is really there?",
        "",
        "Not a strategy and not a try: a 16th feature `peek` is planted that knows the future "
        "(correlation rho with the row's own 28-day risk-adjusted return, the rest noise). "
        "Everything else is the `ml-linear` and `ml-gbm` primary pipeline, unchanged: same "
        "rows, purged walk-forward, purged CV, gym and costs. `peek0.00` is pure noise. One "
        "table per position rule (`protocol.md`).",
        "",
    ]
    tags = {}
    titles = {
        "base": "first rule: full slot at average confidence",
        "prop": "`-prop`: position in proportion to confidence",
        "low": "`-low`: out on the weakest quarter of forecasts",
    }
    for sizing, title in titles.items():
        runs = []
        for spec in (ml.LOGIT, ml.GBM):
            for rho in RHOS:
                tag = f"{spec.name}+peek{rho:.2f}"
                tags[tag] = 0.5
                name = tag if sizing == "base" else f"{tag}-{sizing}"
                rule = c.weekly(strategy(spec, rho, tag, sizing))
                runs.append(c.go("control", name, rule, six, "baseline", log=False))
        out += [f"## Six assets, 1994-2025, {title}", ""]
        out += [c.table([*runs, twin, ew], versus=twin, eras=False), ""]
    out += ["## Forecast skill (the same for every position rule)", ""]
    out += [*mltest.skill_table(six, tags), ""]
    c.write_result("ml-control", "\n".join(out))


if __name__ == "__main__":
    main()
