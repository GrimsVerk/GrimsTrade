"""How well does each single feature rank next month's direction, with no model at all?

    uv run --with numpy --with scikit-learn python research/lib/feature_skill.py

Not a strategy and not a try: no backtest is run. Reads the same six-asset rows the models
were scored on (Fridays from the start of the train period, 28-day labels) and writes
`results/ml-feature-skill.md`. Also measures how strong the planted control signals really
were. Prompted by the independent code review of 2026-11-12.
"""

from __future__ import annotations

import math
from datetime import timedelta

import common as c
import control_ml
import ml
import numpy as np
from sklearn.metrics import roc_auc_score

DRAWS = 400


def auc(up: np.ndarray, f: np.ndarray) -> float:
    return float(roc_auc_score(up, f)) if 0 < up.mean() < 1 else math.nan


def within(up: np.ndarray, f: np.ndarray, sym: np.ndarray) -> float:
    """Mean AUC inside each asset, weighted by rows: skill at timing, not at picking assets."""
    parts = [(auc(up[sym == s], f[sym == s]), int((sym == s).sum())) for s in np.unique(sym)]
    return float(np.average([a for a, _ in parts], weights=[n for _, n in parts]))


def rows_of(u: c.Ctx) -> ml.Rows:
    start = max(u.start, ml.first_fit_day(u.panel, u.start))  # as the model tests
    days = [d for d in ml.fridays(u.panel, u.end - timedelta(ml.HORIZON)) if d >= start]
    return ml._concat([ml.labelled(u.panel, d) for d in days])


def main() -> None:
    six = c.ctx("six")
    rows = rows_of(six)
    others = {name: rows_of(c.ctx(name)) for name in ("etf", "coin", "idx")}
    up, sym = rows.fwd > 0, np.array(rows.sym)
    block = np.array([(d // 91) for d in rows.day])  # 13-week blocks, resampled whole
    ids = np.unique(block)
    members = {b: np.flatnonzero(block == b) for b in ids}
    rng = np.random.default_rng(0)
    picks = [np.concatenate([members[b] for b in rng.choice(ids, len(ids))]) for _ in range(DRAWS)]

    out = [
        "# Forecast skill of each feature on its own (no model)",
        "",
        "Not a strategy and not a try: no backtest. The six live assets, every Friday of the "
        f"train period from {six.start}, 28-day labels: {len(rows)} rows, {up.mean():.1%} went "
        "up. AUC of the raw feature as a ranking of which asset-months go up (0.50 = coin "
        "toss; below 0.50 = the feature ranks them backwards). Standard error from resampling "
        '13-week blocks. "Within asset" is the average AUC inside each asset: skill at '
        "timing, with the differences between assets taken out. The last three columns are "
        "the same AUC on the other market sets, over the periods of the model tests ("
        + ", ".join(f"{k}: {len(v)} rows" for k, v in others.items())
        + ").",
        "",
        "| Feature | AUC | SE | Within asset | Other ETFs | Other coins | Indexes |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    table = []
    for j, name in enumerate(ml.FEATURES):
        f = rows.x[:, j]
        se = float(np.nanstd([auc(up[k], f[k]) for k in picks]))
        rest = " | ".join(f"{auc(o.fwd > 0, o.x[:, j]):.3f}" for o in others.values())
        table.append((auc(up, f), name, se, within(up, f, sym), rest))
    for a, name, se, w, rest in sorted(table, reverse=True):
        out.append(f"| `{name}` | {a:.3f} | {se:.3f} | {w:.3f} | {rest} |")

    vol = np.exp(rows.x[:, ml.LOG_VOL])
    ra = np.clip(rows.fwd / (vol * math.sqrt(ml.HORIZON / 365)), -3, 3)
    out += [
        "",
        "## How strong the planted control signals really were",
        "",
        "`lib/control_ml.py` plants `peek` = rho x risk-adjusted return + noise. The noise "
        "draw happens to correlate slightly with the outcome by chance (the 0.00 row), so "
        "each planted signal is about 0.02 stronger than its label:",
        "",
        "| Label (rho) | Correlation with the risk-adjusted return | ...with the 28-day log "
        "return | AUC of `peek` alone |",
        "|---:|---:|---:|---:|",
    ]
    for rho in control_ml.RHOS:
        peek = control_ml.with_peek(rows, rho).x[:, -1]
        out.append(
            f"| {rho:.2f} | {np.corrcoef(peek, ra)[0, 1]:.3f} | "
            f"{np.corrcoef(peek, rows.fwd)[0, 1]:.3f} | {auc(up, peek):.3f} |"
        )
    c.write_result("ml-feature-skill", "\n".join(out))


if __name__ == "__main__":
    main()
