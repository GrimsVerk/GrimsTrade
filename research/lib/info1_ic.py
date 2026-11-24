"""Weekly IC screen of the info-1 candidates (card: research/info-1.md, "Measures").

    uv run python research/lib/info1_ic.py            # prints the table (dry: logs nothing)
    uv run python research/lib/info1_ic.py --log > research/results/info-1.md   # + tries rows

Target, rows and period as `results/rl-3-inputs.md`: `rl3_plant.week_z` on the six assets,
Fridays 2000-01-07 .. end of train. Descriptive only: no backtest. With `--log` every candidate
gets one `screen` row in tries.md (run once).
"""

from __future__ import annotations

import sys
from datetime import UTC, date, datetime

import harness
import info1_features as inf
import numpy as np
import rl2_data
import rl3_plant

N_SHIFT = 500
MIN_SHIFT = 52
MIN_TRAIN_WEEKS = 104
TREND = slice(0, 7)  # z7, z30, z91, z182, z365, up_12m, sma_gap (ml.FEATURES order)


def corr(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 3 or a.std() == 0 or b.std() == 0:
        return float("nan")
    return float(np.corrcoef(a, b)[0, 1])


def rank(a: np.ndarray) -> np.ndarray:
    r = np.empty(len(a))
    r[np.argsort(a, kind="stable")] = np.arange(len(a))
    return r


def walk_forward(
    blocks: list[tuple[np.ndarray, np.ndarray]],
    design: list[np.ndarray],
    z: np.ndarray,
) -> float:
    """OLS per block on the training rows (inputs standardised there); predictions use the
    slopes only (no intercept). IC of all out-of-sample predictions with z."""
    preds, ys = [], []
    for tr, te in blocks:
        Xtr = np.column_stack([d[tr] for d in design])
        Xte = np.column_stack([d[te] for d in design])
        mu, sd = Xtr.mean(0), Xtr.std(0)
        live = sd > 0
        Xtr = (Xtr[:, live] - mu[live]) / sd[live]
        Xte = (Xte[:, live] - mu[live]) / sd[live]
        b = np.linalg.lstsq(np.column_stack([np.ones(len(Xtr)), Xtr]), z[tr], rcond=None)[0]
        preds.append(Xte @ b[1:])
        ys.append(z[te])
    if not preds:
        return float("nan")
    return corr(np.concatenate(preds), np.concatenate(ys))


def main(log: bool) -> None:
    t = rl2_data.load()["six"].t
    z = rl3_plant.week_z(t)
    F, n = z.shape
    i0 = t.fridays.index(date(2000, 1, 7))
    keep = np.isfinite(z)
    keep[:i0] = False
    with np.errstate(all="ignore"):
        feats = inf.features(t)
    years = np.repeat(np.array([d.year for d in t.fridays])[:, None], n, 1)
    week = np.repeat(np.arange(F)[:, None], n, 1)
    asset = np.repeat(np.arange(n)[None, :], F, 0)
    up = t.X[:, :, 5] > 0.5
    rng = np.random.default_rng(0)
    shifts = rng.integers(MIN_SHIFT, F - MIN_SHIFT, N_SHIFT)
    syms = t.book.syms

    rows = []
    for name in inf.CANDIDATES:
        x = feats[name]
        m = keep & np.isfinite(x)
        if m.sum() < 50:
            rows.append({"name": name, "cells": int(m.sum())})
            continue
        xm, zm = x[m], z[m]
        ic = corr(xm, zm)
        ric = corr(rank(xm), rank(zm))
        mh = m & up
        ic_held = corr(x[mh], z[mh])
        per = {syms[j]: corr(x[m & (asset == j)], z[m & (asset == j)]) for j in range(n)}
        null = []
        for s in shifts:
            xs = np.roll(x, s, axis=0)
            ms = keep & np.isfinite(xs)
            if ms.sum() >= 50:
                null.append(abs(corr(xs[ms], z[ms])))
        chance = float(np.nanpercentile(null, 95))
        # walk-forward
        blocks = []
        for y0 in range(2000, 2026, 2):
            tr = m & (years < y0 - 1)
            te = m & (years >= y0) & (years < y0 + 2)
            if te.sum() and len(np.unique(week[tr])) >= MIN_TRAIN_WEEKS:
                blocks.append((tr, te))
        dummies = [(asset == j).astype(float) for j in range(n)]
        per_slope = [x * d for d in dummies]
        xz = np.nan_to_num(x)
        per_slope = [np.nan_to_num(p) for p in per_slope]
        wf_per = walk_forward(blocks, per_slope, z)
        wf_pool = walk_forward(blocks, [xz], z)
        trend = [t.X[:, :, k] for k in range(TREND.start, TREND.stop)]
        wf_trend = walk_forward(blocks, trend, z)
        wf_both = walk_forward(blocks, trend + per_slope, z)
        overlap = max(abs(corr(xm, t.X[:, :, k][m])) for k in range(TREND.start, TREND.stop))
        wf_cells = int(sum(te.sum() for _, te in blocks))
        rows.append({
            "name": name, "first": t.fridays[int(np.flatnonzero(m.any(1))[0])],
            "cells": int(m.sum()), "weeks": int(m.any(1).sum()), "ic": ic, "ric": ric,
            "held": ic_held, "chance": chance, "per": per, "wf_per": wf_per,
            "wf_pool": wf_pool, "gain": wf_both - wf_trend, "wf_trend": wf_trend,
            "overlap": overlap, "wf_cells": wf_cells,
        })  # fmt: skip
    report(rows, syms)
    if log:
        stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
        with harness.TRIES.open("a") as f:
            for r in rows:
                if "ic" not in r:
                    desc = f"{r['name']} (no data: {r['cells']} cells)"
                    first = "-"
                else:
                    desc = (f"{r['name']} (IC {r['ic']:+.3f}, chance {r['chance']:.3f}, "
                            f"WF {best_wf(r):+.3f}, gain {r['gain']:+.3f})")  # fmt: skip
                    first = r["first"].isoformat()
                f.write(f"| {stamp} | info-1-screen | {desc} | screen | train | {first} | "
                        "2025-11-09 | - | - | - | - |\n")  # fmt: skip


def best_wf(r: dict[str, object]) -> float:
    a, b = float(r["wf_per"]), float(r["wf_pool"])  # type: ignore[arg-type]
    vals = [v for v in (a, b) if np.isfinite(v)]
    return max(vals) if vals else float("nan")


def verdict(r: dict[str, object]) -> str:
    wf = best_wf(r)
    above = abs(float(r["ic"])) > float(r["chance"])  # type: ignore[arg-type]
    gain = float(r["gain"])  # type: ignore[arg-type]
    if above and (wf >= 0.10 or gain >= 0.05):
        return "**useful**"
    if above and wf >= 0.05:
        return "second look"
    return "no"


def report(rows: list[dict[str, object]], syms: list[str]) -> None:
    print("# Info 1: weekly IC screen of new information (six assets, 2000-01-07 to 2025-11-09)\n")
    print("Script `lib/info1_ic.py`, card `research/info-1.md`. IC = Pearson correlation with the")
    print("coming week's risk-adjusted return (`rl3_plant.week_z`). Chance = 95th percentile of")
    print(f"|IC| with the feature's weekly series circularly shifted ({N_SHIFT} shifts of >= 52")
    print("weeks). WF = walk-forward IC (OLS refitted every two years, a year's gap); `per` = a")
    print("slope per asset, `pool` = one slope. Gain = WF IC of trend inputs + feature minus trend")
    print("inputs alone, same rows. Overlap = largest |corr| with the 7 trend inputs.\n")
    print("| Candidate | From | Weeks | Cells | IC | rank IC | IC held | Chance | WF per | WF pool"
          " | WF trend | Gain | Overlap | Verdict |")  # fmt: skip
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        if "ic" not in r:
            print(f"| `{r['name']}` | no data | | {r['cells']} | | | | | | | | | | |")
            continue
        print(
            f"| `{r['name']}` | {r['first']} | {r['weeks']} | {r['cells']} | {r['ic']:+.3f} | "
            f"{r['ric']:+.3f} | {r['held']:+.3f} | {r['chance']:.3f} | {r['wf_per']:+.3f} | "
            f"{r['wf_pool']:+.3f} | {r['wf_trend']:+.3f} | {r['gain']:+.3f} | "
            f"{r['overlap']:.2f} | {verdict(r)} |"
        )
    print("\n## IC per asset (in sample)\n")
    print("| Candidate | " + " | ".join(syms) + " |")
    print("|---|" + "---:|" * len(syms))
    for r in rows:
        if "per" in r:
            per = r["per"]
            assert isinstance(per, dict)
            cells = " | ".join("" if not np.isfinite(per[s]) else f"{per[s]:+.3f}" for s in syms)
            print(f"| `{r['name']}` | {cells} |")


if __name__ == "__main__":
    main("--log" in sys.argv)
