"""Weekly IC screen of the six assets' own volume (card: research/volume-1.md).

    uv run python research/lib/volume1_ic.py            # prints the table (dry: logs nothing)
    uv run python research/lib/volume1_ic.py --log > research/results/volume-1.md   # + tries rows

Target, rows, walk-forward and bar as `info1_ic.py` (reused). New here: six volume features from
the bar cache (`harness.load_history("train")`, a bar dated x used from x + 1) and a family
chance level (maxT over the six candidates, the same circular shifts for all). Descriptive only:
no backtest. With `--log` every candidate gets one `screen` row in tries.md (run once).
"""

from __future__ import annotations

import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime

import numpy as np
from info1_features import asof, roll_z

from grimstrade.data import CRYPTO, UNIVERSE, Bar

# `info1_ic` (and through it the RL table code, which changes global state on import) is
# imported inside the functions that need it, so the feature tests stay light.

CANDIDATES = ["vol_chg4", "vol_chg13", "vol_z52", "vw_trend13", "updown13", "pv_div13"]
LAG = 1  # a bar dated x is used from x + 1
MIN_SHARE = 0.8  # share of a window's bars that must be present
BTC_FROM = date(2015, 7, 20)  # Coinbase volume only (Bitstamp before: another level)
IDEA = "volume-1-screen"


def win_mean(v: np.ndarray, n: int) -> np.ndarray:
    """Trailing mean of the finite values among the last n; NaN under MIN_SHARE present."""
    out = np.full(len(v), np.nan)
    for i in range(n - 1, len(v)):
        w = v[i - n + 1 : i + 1]
        w = w[np.isfinite(w)]
        if len(w) >= MIN_SHARE * n:
            out[i] = w.mean()
    return out


def shifted(v: np.ndarray, n: int) -> np.ndarray:
    """v[i - n] at i (NaN for the first n)."""
    out = np.full(len(v), np.nan)
    if n < len(v):
        out[n:] = v[: len(v) - n]
    return out


def daily_features(close: np.ndarray, volume: np.ndarray, w: int) -> dict[str, np.ndarray]:
    """The six candidates on one asset's own bars (card, "Candidates"); all windows trailing.
    `w` = bars per week. Volume <= 0 or non-finite is missing."""
    v = np.where(np.isfinite(volume) & (volume > 0), volume, np.nan).astype(float)
    r = np.diff(np.log(close), prepend=np.nan)
    out: dict[str, np.ndarray] = {}
    with np.errstate(all="ignore"):
        for name, k in (("vol_chg4", 4 * w), ("vol_chg13", 13 * w)):
            m = win_mean(v, k)
            out[name] = np.log(m / shifted(m, k))
        out["vol_z52"] = roll_z(np.log(win_mean(v, w)), 52 * w, 26 * w)
        n = 13 * w
        vw = np.full(len(v), np.nan)
        ew = np.full(len(v), np.nan)
        sgn = np.full(len(v), np.nan)
        for i in range(n - 1, len(v)):
            vv, rr = v[i - n + 1 : i + 1], r[i - n + 1 : i + 1]
            ok = np.isfinite(vv) & np.isfinite(rr)
            if ok.sum() < MIN_SHARE * n:
                continue
            vv, rr = vv[ok], rr[ok]
            sd = rr.std()
            if sd <= 0:
                continue
            se = sd / np.sqrt(len(rr))
            vw[i] = float((vv * rr).sum() / vv.sum()) / se
            ew[i] = float(rr.mean()) / se
            sgn[i] = np.sign(rr.sum())
        out["vw_trend13"] = vw
        out["updown13"] = vw - ew
        out["pv_div13"] = sgn * out["vol_chg13"]
    return out


def features(
    history: Mapping[str, Sequence[Bar]], syms: Sequence[str], fridays: Sequence[date]
) -> dict[str, np.ndarray]:
    """{candidate: [F, n]} at the Friday decisions, NaN where unknown."""
    out = {c: np.full((len(fridays), len(syms)), np.nan) for c in CANDIDATES}
    for j, s in enumerate(syms):
        bars = list(history[s])
        if s == "BTC":
            bars = [b for b in bars if b.date >= BTC_FROM]
        if not bars:
            continue
        days = [b.date for b in bars]
        w = 7 if UNIVERSE[s] == CRYPTO else 5
        f = daily_features(np.array([b.close for b in bars]), np.array([b.volume for b in bars]), w)
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
    z = rl3_plant.week_z(t)
    F, n = z.shape
    syms = t.book.syms
    i0 = t.fridays.index(date(2000, 1, 7))
    keep = np.isfinite(z)
    keep[:i0] = False
    feats = features(harness.load_history("train"), syms, t.fridays)
    years = np.repeat(np.array([d.year for d in t.fridays])[:, None], n, 1)
    week = np.repeat(np.arange(F)[:, None], n, 1)
    asset = np.repeat(np.arange(n)[None, :], F, 0)
    shifts = np.random.default_rng(0).integers(MIN_SHIFT, F - MIN_SHIFT, N_SHIFT)
    single, family = family_chance(feats, z, keep, shifts)
    trend = [t.X[:, :, k] for k in range(TREND.start, TREND.stop)]

    rows: list[dict[str, object]] = []
    for name in CANDIDATES:
        x = feats[name]
        m = keep & np.isfinite(x)
        xm, zm = x[m], z[m]
        blocks = []
        for y0 in range(2000, 2026, 2):
            tr = m & (years < y0 - 1)
            te = m & (years >= y0) & (years < y0 + 2)
            if te.sum() and len(np.unique(week[tr])) >= MIN_TRAIN_WEEKS:
                blocks.append((tr, te))
        per_slope = [np.nan_to_num(x * (asset == j)) for j in range(n)]
        wf_trend = walk_forward(blocks, trend, z)
        rows.append({
            "name": name, "first": t.fridays[int(np.flatnonzero(m.any(1))[0])],
            "cells": int(m.sum()), "weeks": int(m.any(1).sum()), "ic": corr(xm, zm),
            "ric": corr(rank(xm), rank(zm)), "chance": single[name],
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
    print("# Volume 1: weekly IC screen of own trading volume (six assets, to 2025-11-09)\n")
    print("Script `lib/volume1_ic.py`, card `research/volume-1.md`. IC = Pearson correlation")
    print("with the coming week's risk-adjusted return (`rl3_plant.week_z`). Chance = 95th")
    print(f"percentile of |IC| with the feature circularly shifted ({n_shift} shifts of >= 52")
    print("weeks, the same shifts for all six). **Family chance level (maxT over the six):")
    print(f"{family:.3f}**; a candidate is above chance only above that. WF = walk-forward IC")
    print("(OLS refitted every two years, a year's gap); `per` = a slope per asset, `pool` = one")
    print("slope. Gain = WF IC of trend inputs + feature minus trend inputs alone. Overlap =")
    print("largest |corr| with the 7 trend inputs.\n")
    print("| Candidate | From | Weeks | Cells | IC | rank IC | Chance | Family | WF per | WF pool"
          " | WF trend | Gain | Overlap | Verdict |")  # fmt: skip
    print("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in rows:
        print(
            f"| `{r['name']}` | {r['first']} | {r['weeks']} | {r['cells']} | {r['ic']:+.3f} | "
            f"{r['ric']:+.3f} | {r['chance']:.3f} | {family:.3f} | {r['wf_per']:+.3f} | "
            f"{r['wf_pool']:+.3f} | {r['wf_trend']:+.3f} | {r['gain']:+.3f} | "
            f"{r['overlap']:.2f} | {verdict(r, family)} |"
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
