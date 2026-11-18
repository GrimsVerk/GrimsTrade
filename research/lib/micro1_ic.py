"""Weekly IC screen of minute-bar features (card: research/micro-1.md).

    .venv/bin/python -I research/lib/micro1_days.py <cache root>     # daily table, once
    uv run python research/lib/micro1_ic.py            # prints the table (dry: logs nothing)
    uv run python research/lib/micro1_ic.py --log > research/results/micro-1.md   # + tries rows

Target, walk-forward and bars as `info1_ic.py` (reused); family chance level (maxT) as
volume-1. New here: six features from the daily table `micro1_days.py` builds out of the minute
bars (a day dated x used from x + 1), on the 2016-2025 window the minute bars cover.
Descriptive only: no backtest. With `--log` every candidate gets one `screen` row in tries.md.
"""

from __future__ import annotations

import csv
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np
from info1_features import asof, roll_z

CANDIDATES = ["rv_chg", "rv_z52", "jump4", "sjump4", "overnight13", "intraday13"]
FIELDS = ("rv", "bv", "rsp", "rsn", "overnight", "intraday")
COINS = ("BTC", "ETH")
LAG = 1  # a day dated x is used from x + 1
MIN_SHARE = 0.8  # share of a window's days that must be present
FIRST_FRIDAY = date(2016, 1, 8)
IDEA = "micro-1-screen"

Day = dict[str, np.ndarray]


def win_mean(v: np.ndarray, n: int) -> np.ndarray:
    """Trailing mean of the finite values among the last n; NaN under MIN_SHARE present."""
    out = np.full(len(v), np.nan)
    for i in range(n - 1, len(v)):
        w = v[i - n + 1 : i + 1]
        w = w[np.isfinite(w)]
        if len(w) >= MIN_SHARE * n:
            out[i] = w.mean()
    return out


def win_t(v: np.ndarray, n: int) -> np.ndarray:
    """Trailing mean / sd x sqrt(count) of the finite values among the last n."""
    out = np.full(len(v), np.nan)
    for i in range(n - 1, len(v)):
        w = v[i - n + 1 : i + 1]
        w = w[np.isfinite(w)]
        if len(w) >= MIN_SHARE * n and w.std() > 0:
            out[i] = w.mean() / w.std() * np.sqrt(len(w))
    return out


def daily_features(d: Mapping[str, np.ndarray], w: int) -> dict[str, np.ndarray]:
    """The six candidates on one asset's daily table (card, "Candidates"); all windows
    trailing. `w` = days per week."""
    rv = np.where(d["rv"] > 0, d["rv"], np.nan)
    ok = np.isfinite(rv)
    bv, rsp, rsn = (np.where(ok, d[k], np.nan) for k in ("bv", "rsp", "rsn"))
    out: dict[str, np.ndarray] = {}
    with np.errstate(all="ignore"):
        week = win_mean(rv, w)
        out["rv_chg"] = np.log(week / win_mean(rv, 13 * w))
        out["rv_z52"] = roll_z(np.log(week), 52 * w, 26 * w)
        month = win_mean(rv, 4 * w)
        out["jump4"] = 1 - win_mean(bv, 4 * w) / month
        out["sjump4"] = (win_mean(rsp, 4 * w) - win_mean(rsn, 4 * w)) / month
        out["overnight13"] = win_t(d["overnight"], 13 * w)
        out["intraday13"] = win_t(d["intraday"], 13 * w)
    return out


def calendar_grid(days: Sequence[date], d: Mapping[str, np.ndarray]) -> tuple[list[date], Day]:
    """Every calendar day from the first to the last, NaN where the table has no row (coins)."""
    grid = [days[0] + timedelta(days=i) for i in range((days[-1] - days[0]).days + 1)]
    pos = np.array([(x - days[0]).days for x in days])
    out = {}
    for k, v in d.items():
        full = np.full(len(grid), np.nan)
        full[pos] = v
        out[k] = full
    return grid, out


def load_days(path: Path) -> dict[str, tuple[list[date], Day]]:
    """{asset: (days, {field: values})} from the daily table, days ascending."""
    raw: dict[str, list[tuple[date, list[float]]]] = {}
    with path.open(newline="") as f:
        for r in csv.DictReader(f):
            raw.setdefault(r["asset"], []).append(
                (date.fromisoformat(r["date"]), [float(r[k]) for k in FIELDS])
            )
    out = {}
    for s, rows in raw.items():
        rows.sort(key=lambda x: x[0])
        vals = np.array([v for _, v in rows], float)
        out[s] = ([d for d, _ in rows], {k: vals[:, i] for i, k in enumerate(FIELDS)})
    return out


def features(
    table: Mapping[str, tuple[Sequence[date], Mapping[str, np.ndarray]]],
    syms: Sequence[str],
    fridays: Sequence[date],
) -> dict[str, np.ndarray]:
    """{candidate: [F, n]} at the Friday decisions, NaN where unknown."""
    out = {c: np.full((len(fridays), len(syms)), np.nan) for c in CANDIDATES}
    for j, s in enumerate(syms):
        if s not in table:
            continue
        days, d = table[s]
        w = 5
        if s in COINS:
            days, d = calendar_grid(days, d)
            w = 7
        f = daily_features(d, w)
        for c in CANDIDATES:
            out[c][:, j] = asof(days, f[c], LAG, fridays)
    return out


def family_chance(
    feats: Mapping[str, np.ndarray], z: np.ndarray, keep: np.ndarray, shifts: np.ndarray
) -> tuple[dict[str, float], float]:
    """Single-test chance level per candidate and the maxT family level: the 95th percentile
    over the shifts of |IC| and of the largest |IC| among the candidates (same shift for all)."""
    from info1_ic import corr

    null = np.full((len(shifts), len(feats)), np.nan)
    for a, s in enumerate(shifts):
        for b, x in enumerate(feats.values()):
            xs = np.roll(x, int(s), axis=0)
            ms = keep & np.isfinite(xs)
            if ms.sum() >= 50:
                null[a, b] = abs(corr(xs[ms], z[ms]))
    single = {c: float(np.nanpercentile(null[:, b], 95)) for b, c in enumerate(feats)}
    return single, float(np.nanpercentile(np.nanmax(null, axis=1), 95))


def verdict(r: dict[str, object], family: float) -> str:
    from info1_ic import best_wf

    wf = best_wf(r)
    above = abs(float(r["ic"])) > family  # type: ignore[arg-type]
    gain = float(r["gain"])  # type: ignore[arg-type]
    if above and (wf >= 0.10 or gain >= 0.05):
        return "**useful**"
    if above and wf >= 0.05:
        return "second look"
    return "no"


def main(log: bool) -> None:
    import harness
    import macro
    import rl2_data
    import rl3_plant
    from info1_ic import (
        MIN_SHIFT,
        MIN_TRAIN_WEEKS,
        N_SHIFT,
        TREND,
        best_wf,
        corr,
        rank,
        walk_forward,
    )

    t = rl2_data.load()["six"].t
    i0 = next(i for i, d in enumerate(t.fridays) if d >= FIRST_FRIDAY)
    fridays = t.fridays[i0:]
    z = rl3_plant.week_z(t)[i0:]
    F, n = z.shape
    syms = t.book.syms
    keep = np.isfinite(z)
    table = load_days(macro.cache_root() / "derived" / "micro-1" / "days.csv")
    missing = [s for s in syms if s not in table]
    if missing:
        raise SystemExit(f"no minute data for {missing}")
    feats = features(table, syms, fridays)
    years = np.repeat(np.array([d.year for d in fridays])[:, None], n, 1)
    week = np.repeat(np.arange(F)[:, None], n, 1)
    asset = np.repeat(np.arange(n)[None, :], F, 0)
    shifts = np.random.default_rng(0).integers(MIN_SHIFT, F - MIN_SHIFT, N_SHIFT)
    single, family = family_chance(feats, z, keep, shifts)
    trend = [t.X[i0:, :, k] for k in range(TREND.start, TREND.stop)]

    rows: list[dict[str, object]] = []
    for name in CANDIDATES:
        x = feats[name]
        m = keep & np.isfinite(x)
        xm, zm = x[m], z[m]
        blocks = []
        for y0 in range(2016, 2026, 2):
            tr = m & (years < y0 - 1)
            te = m & (years >= y0) & (years < y0 + 2)
            if te.sum() and len(np.unique(week[tr])) >= MIN_TRAIN_WEEKS:
                blocks.append((tr, te))
        per_slope = [np.nan_to_num(x * (asset == j)) for j in range(n)]
        wf_trend = walk_forward(blocks, trend, z)
        rows.append({
            "name": name, "first": fridays[int(np.flatnonzero(m.any(1))[0])],
            "cells": int(m.sum()), "weeks": int(m.any(1).sum()), "blocks": len(blocks),
            "ic": corr(xm, zm), "ric": corr(rank(xm), rank(zm)), "chance": single[name],
            "per": {syms[j]: corr(x[m & (asset == j)], z[m & (asset == j)]) for j in range(n)},
            "wf_per": walk_forward(blocks, per_slope, z),
            "wf_pool": walk_forward(blocks, [np.nan_to_num(x)], z), "wf_trend": wf_trend,
            "gain": walk_forward(blocks, trend + per_slope, z) - wf_trend,
            "overlap": max(abs(corr(xm, k[m])) for k in trend),
        })  # fmt: skip
    report(rows, syms, family, N_SHIFT)
    if log:
        stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
        with harness.TRIES.open("a") as f:
            for r in rows:
                desc = (f"{r['name']} (IC {r['ic']:+.3f}, chance {r['chance']:.3f}, family "
                        f"{family:.3f}, WF {best_wf(r):+.3f}, gain {r['gain']:+.3f})")  # fmt: skip
                first = r["first"]
                assert isinstance(first, date)
                f.write(f"| {stamp} | {IDEA} | {desc} | screen | train | {first.isoformat()} | "
                        "2025-11-09 | - | - | - | - |\n")  # fmt: skip


def report(rows: list[dict[str, object]], syms: list[str], family: float, n_shift: int) -> None:
    print("# Micro 1: weekly IC screen of minute-bar features (six assets, 2016 to 2025-11-09)\n")
    print("Script `lib/micro1_ic.py`, card `research/micro-1.md`. IC = Pearson correlation")
    print("with the coming week's risk-adjusted return (`rl3_plant.week_z`). Chance = 95th")
    print(f"percentile of |IC| with the feature circularly shifted ({n_shift} shifts of >= 52")
    print("weeks inside the 2016-2025 window, the same shifts for all six). **Family chance")
    print(f"level (maxT over the six): {family:.3f}**; a candidate is above chance only above")
    print("that. WF = walk-forward IC (OLS refitted every two years, a year's gap; `Blocks` =")
    print("test blocks that had >= 104 training weeks); `per` = a slope per asset, `pool` = one")
    print("slope. Gain = WF IC of trend inputs + feature minus trend inputs alone. Overlap =")
    print("largest |corr| with the 7 trend inputs.\n")
    print("| Candidate | From | Weeks | Cells | IC | rank IC | Chance | Family | Blocks | WF per"
          " | WF pool | WF trend | Gain | Overlap | Verdict |")  # fmt: skip
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        print(
            f"| `{r['name']}` | {r['first']} | {r['weeks']} | {r['cells']} | {r['ic']:+.3f} | "
            f"{r['ric']:+.3f} | {r['chance']:.3f} | {family:.3f} | {r['blocks']} | "
            f"{r['wf_per']:+.3f} | {r['wf_pool']:+.3f} | {r['wf_trend']:+.3f} | "
            f"{r['gain']:+.3f} | {r['overlap']:.2f} | {verdict(r, family)} |"
        )
    print("\n## IC per asset (in sample; shown, not judged)\n")
    print("| Candidate | " + " | ".join(syms) + " |")
    print("|---|" + "---:|" * len(syms))
    for r in rows:
        per = r["per"]
        assert isinstance(per, dict)
        cells = " | ".join("" if not np.isfinite(per[s]) else f"{per[s]:+.3f}" for s in syms)
        print(f"| `{r['name']}` | {cells} |")


if __name__ == "__main__":
    main("--log" in sys.argv)
