"""Slow-horizon IC screen of run slow-1 (card: research/slow-1.md). Descriptive: no backtest.

    uv run python research/lib/slow1_ic.py --check      # h = 1 reproduction of the public tables
    uv run python research/lib/slow1_ic.py --run --log  # the screen (once): json + tries rows
    uv run python research/lib/slow1_ic.py --report     # results/slow-1.md from the json

Targets: `horizon_z(t, h)`, the h-week version of `rl3_plant.week_z`, h = 4 and 13. Inputs:
info-1's 23 candidates and rl-3's real inputs (49 in all). Walk-forward IC as `info1_ic`.
Chance: circular rotation of each input inside its own span; maxT over the whole family.
Needs RL 2's `tables2.pkl` and the shared cache (`research/macro.local.json`); writes only
`<cache_root>/derived/slow-1/`.
"""

from __future__ import annotations

import fcntl
import json
import math
import re
import sys
import time
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import harness
import info1_features as inf
import macro
import ml
import numpy as np
import rl2_data
import rl3_plant
import rl_env

HORIZONS = (4, 13)
N_ROT = 1000
N_ROT_COMBO = 500
MIN_SHIFT = 52
MIN_SPAN = 157
MIN_TRAIN_WEEKS = 104
MIN_TRAIN_CELLS = 104  # a combined-forecast input with fewer training cells is 0 in that block
MIN_NULL = 200
START = date(2000, 1, 7)
TREND = ["z7", "z30", "z91", "z182", "z365", "up_12m", "sma_gap"]
SLOW4 = ["cot_spec_z3y", "vrp", "puell", "curve"]
COMBOS = ["slow4", "all-sign", "all-ridge"]
BAR_WF, NEAR_WF, BAR_GAIN = 0.10, 0.05, 0.05
PLANT_RHO = 0.10
IDEA = "slow-1-screen"


def out_dir() -> Path:
    p = macro.cache_root() / "derived" / "slow-1"
    p.mkdir(parents=True, exist_ok=True)
    return p


# ---------- target ----------


def horizon_z(t: rl_env.Table, h: int) -> np.ndarray:
    """[F, n] log return from the first open after Friday i to the first open after Friday i + h,
    over (EWMA vol x sqrt(7h/365)), clipped to +-5; NaN where the asset is not eligible or the
    window does not close inside the book. h = 1 is `rl3_plant.week_z`."""
    op = t.book.opens
    nxt = rl3_plant._next_open(op)
    k_n, n = op.shape
    z = np.full(t.elig.shape, np.nan)
    cols = np.arange(n)
    with np.errstate(all="ignore"):
        for i, k in enumerate(t.kf):
            if k + 7 * h >= k_n:
                continue
            a, b = nxt[k], nxt[k + 7 * h]
            ok = t.elig[i] & (b < k_n) & (a < b)
            if not ok.any():
                continue
            r = np.log(op[np.minimum(b, k_n - 1), cols] / op[np.minimum(a, k_n - 1), cols])
            vol = np.exp(t.X[i, :, ml.LOG_VOL])
            z[i] = np.where(ok, np.clip(r / (vol * math.sqrt(7 * h / 365)), -5, 5), np.nan)
    return z


# ---------- inputs ----------


def inputs(t: rl_env.Table, coin: np.ndarray) -> tuple[dict[str, np.ndarray], dict[str, str]]:
    """{name: [F, n]} (NaN where unknown or not applicable) and {name: group}."""
    with np.errstate(all="ignore"):
        feats = inf.features(t)
    out: dict[str, np.ndarray] = {}
    grp: dict[str, str] = {}
    for k in inf.CANDIDATES:
        out[k] = feats[k]
        grp[k] = "info-1"
    n = len(t.book.syms)
    for k, f in enumerate(rl_env.ASSET_FEATS):
        if f == "coin":
            continue
        x = np.where(t.elig, t.X[:, :, k], np.nan)
        if f == "halving":
            x[:, ~coin] = np.nan
        out[f] = x
        grp[f] = "trend" if f in TREND else "price"
    for k, f in enumerate(rl_env.MACRO_FEATS):
        out[f] = np.repeat(t.G[:, [k]], n, 1)
        grp[f] = "macro"
    return out, grp


# ---------- statistics ----------


def corr(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 3:
        return float("nan")
    a = a - a.mean()
    b = b - b.mean()
    d = math.sqrt(float(a @ a) * float(b @ b))
    return float(a @ b) / d if d > 0 else float("nan")


def rank(a: np.ndarray) -> np.ndarray:
    r = np.empty(len(a))
    r[np.argsort(a, kind="stable")] = np.arange(len(a))
    return r


def fit_predict(xtr: np.ndarray, ztr: np.ndarray, xte: np.ndarray) -> np.ndarray:
    """OLS with intercept on the training rows (columns standardised there); the prediction uses
    the slopes only, as `info1_ic.walk_forward`."""
    mu = xtr.mean(0)
    a = xtr - mu
    sd = a.std(0)
    live = sd > 0
    if not live.any():
        return np.zeros(len(xte))
    a = a[:, live] / sd[live]
    b = np.linalg.lstsq(a.T @ a, a.T @ ztr, rcond=None)[0]
    return ((xte[:, live] - mu[live]) / sd[live]) @ b  # type: ignore[no-any-return]


class Grid:
    def __init__(self, t: rl_env.Table):
        f, n = t.elig.shape
        self.f, self.n = f, n
        self.years = np.repeat(np.array([d.year for d in t.fridays])[:, None], n, 1)
        self.asset = np.repeat(np.arange(n)[None, :], f, 0)
        self.i0 = t.fridays.index(START)
        self.row = np.repeat(np.arange(f)[:, None], n, 1)

    def blocks(self, m: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
        out = []
        for y0 in range(2000, 2026, 2):
            tr = m & (self.years < y0 - 1)
            te = m & (self.years >= y0) & (self.years < y0 + 2)
            if te.any() and int(tr.any(1).sum()) >= MIN_TRAIN_WEEKS:
                out.append((tr, te))
        return out


def per_design(x: np.ndarray, a: np.ndarray, n: int) -> np.ndarray:
    d = np.zeros((len(x), n))
    d[np.arange(len(x)), a] = x
    return d


def wf_single(
    g: Grid, x: np.ndarray, z: np.ndarray, m: np.ndarray
) -> tuple[float, float, list[tuple[np.ndarray, np.ndarray]]]:
    """Walk-forward IC of one input: (slope per asset, pooled slope, the blocks used)."""
    bl = g.blocks(m)
    if not bl:
        return float("nan"), float("nan"), bl
    pp, pq, ys = [], [], []
    for tr, te in bl:
        xtr, xte, ztr = x[tr], x[te], z[tr]
        pp.append(
            fit_predict(per_design(xtr, g.asset[tr], g.n), ztr, per_design(xte, g.asset[te], g.n))
        )
        pq.append(fit_predict(xtr[:, None], ztr, xte[:, None]))
        ys.append(z[te])
    y = np.concatenate(ys)
    return corr(np.concatenate(pp), y), corr(np.concatenate(pq), y), bl


def wf_cols(
    cols: list[np.ndarray], z: np.ndarray, bl: list[tuple[np.ndarray, np.ndarray]]
) -> float:
    if not bl:
        return float("nan")
    preds, ys = [], []
    for tr, te in bl:
        xtr = np.column_stack([c[tr] for c in cols])
        xte = np.column_stack([c[te] for c in cols])
        preds.append(fit_predict(xtr, z[tr], xte))
        ys.append(z[te])
    return corr(np.concatenate(preds), np.concatenate(ys))


def span(x: np.ndarray, base: np.ndarray) -> tuple[int, int]:
    rows = np.flatnonzero((np.isfinite(x) & base).any(1))
    return (int(rows[0]), int(rows[-1]) + 1) if len(rows) else (0, 0)


def rotate(x: np.ndarray, r0: int, r1: int, s: int) -> np.ndarray:
    """The rows r0..r1-1 of x rotated in time by s (all assets together); the rest unchanged."""
    out = x.copy()
    out[r0:r1] = np.roll(x[r0:r1], s, axis=0)
    return out


def shift_of(u: float, length: int) -> int:
    return MIN_SHIFT + int(u * (length - 2 * MIN_SHIFT))


def measure(
    name: str,
    x: np.ndarray,
    z: np.ndarray,
    h: int,
    t: rl_env.Table,
    g: Grid,
    us: np.ndarray,
    trend: list[np.ndarray] | None,
) -> dict[str, Any]:
    """All measures of one input at one horizon, with its rotation null."""
    keep = np.isfinite(z)
    keep[: g.i0] = False
    base = t.elig & (g.row >= g.i0)
    m = keep & np.isfinite(x)
    rec: dict[str, Any] = {"name": name, "h": h, "cells": int(m.sum())}
    if m.sum() < 50:
        return rec
    xz = np.nan_to_num(x)
    xm, zm = x[m], z[m]
    up = t.X[:, :, ml.UP12] > 0.5
    syms = t.book.syms
    rec["first"] = t.fridays[int(np.flatnonzero(m.any(1))[0])].isoformat()
    rec["weeks"] = int(m.any(1).sum())
    rec["ic"] = corr(xm, zm)
    rec["ric"] = corr(rank(xm), rank(zm))
    rec["held"] = corr(x[m & up], z[m & up])
    rec["per_asset"] = {
        syms[j]: corr(x[m & (g.asset == j)], z[m & (g.asset == j)]) for j in range(g.n)
    }
    nov = []
    for p in range(h):
        mp = m & ((g.row - g.i0) % h == p)
        nov.append(corr(x[mp], z[mp]))
    rec["nov_mean"], rec["nov_min"], rec["nov_max"] = (
        float(np.nanmean(nov)),
        float(np.nanmin(nov)),
        float(np.nanmax(nov)),
    )
    wf_per, wf_pool, bl = wf_single(g, xz, z, m)
    rec["wf_per"], rec["wf_pool"] = wf_per, wf_pool
    rec["wf_cells"] = int(sum(te.sum() for _, te in bl))
    rec["wf_blocks"] = len(bl)
    if trend is not None:
        per_cols = [xz * (g.asset == j) for j in range(g.n)]
        rec["wf_trend"] = wf_cols(trend, z, bl)
        rec["gain"] = wf_cols(trend + per_cols, z, bl) - rec["wf_trend"]
    r0, r1 = span(x, base)
    rec["span"] = r1 - r0
    null_ic = np.full(len(us), np.nan)
    null_per = np.full(len(us), np.nan)
    null_pool = np.full(len(us), np.nan)
    if r1 - r0 >= MIN_SPAN:
        for r, u in enumerate(us):
            xs = rotate(x, r0, r1, shift_of(float(u), r1 - r0))
            ms = keep & np.isfinite(xs)
            if ms.sum() < 50:
                continue
            null_ic[r] = corr(xs[ms], z[ms])
            null_per[r], null_pool[r], _ = wf_single(g, np.nan_to_num(xs), z, ms)
    rec["null_ic"], rec["null_per"], rec["null_pool"] = null_ic, null_per, null_pool
    return rec


# ---------- combined forecasts ----------


def combo_gains(
    u_arr: np.ndarray,
    names: list[str],
    z: np.ndarray,
    t: rl_env.Table,
    g: Grid,
) -> dict[str, float]:
    """Walk-forward gain of each combined forecast over `tsmom12`'s own state (`up_12m`, a slope
    per asset). u_arr [K, F, n]: the non-trend inputs, NaN where missing."""
    keep = np.isfinite(z)
    keep[: g.i0] = False
    bl = g.blocks(keep)
    up = np.where(t.elig, t.X[:, :, ml.UP12], 0.0)
    i4 = [names.index(k) for k in SLOW4]
    preds: dict[str, list[np.ndarray]] = {k: [] for k in ["B", *COMBOS]}
    ys = []
    with np.errstate(all="ignore"):
        for tr, te in bl:
            atr, ate = g.asset[tr], g.asset[te]
            ztr = z[tr]
            btr, bte = per_design(up[tr], atr, g.n), per_design(up[te], ate, g.n)
            utr, ute = u_arr[:, tr], u_arr[:, te]
            fin = np.isfinite(utr)
            cnt = fin.sum(1)
            mu = np.where(fin, utr, 0.0).sum(1) / np.maximum(cnt, 1)
            dev = np.where(fin, utr - mu[:, None], 0.0)
            sd = np.sqrt((dev * dev).sum(1) / np.maximum(cnt, 1))
            ok = (cnt >= MIN_TRAIN_CELLS) & (sd > 0)
            mu, sd = np.where(ok, mu, 0.0), np.where(ok, sd, 1.0)
            s_tr = np.where(ok[:, None], np.nan_to_num((utr - mu[:, None]) / sd[:, None]), 0.0)
            s_te = np.where(ok[:, None], np.nan_to_num((ute - mu[:, None]) / sd[:, None]), 0.0)
            preds["B"].append(fit_predict(btr, ztr, bte))
            x4tr = [per_design(s_tr[k], atr, g.n) for k in i4]
            x4te = [per_design(s_te[k], ate, g.n) for k in i4]
            preds["slow4"].append(
                fit_predict(np.column_stack([btr, *x4tr]), ztr, np.column_stack([bte, *x4te]))
            )
            sign = np.sign(s_tr @ (ztr - ztr.mean()))
            ctr, cte = (sign[:, None] * s_tr).mean(0), (sign[:, None] * s_te).mean(0)
            preds["all-sign"].append(
                fit_predict(np.column_stack([btr, ctr]), ztr, np.column_stack([bte, cte]))
            )
            preds["all-ridge"].append(ridge_predict(btr, s_tr.T, ztr, bte, s_te.T, float(len(ztr))))
            ys.append(z[te])
    y = np.concatenate(ys)
    base_ic = corr(np.concatenate(preds["B"]), y)
    out = {"B": base_ic}
    for k in COMBOS:
        out[k] = corr(np.concatenate(preds[k]), y) - base_ic
    return out


def ridge_predict(
    btr: np.ndarray, str_: np.ndarray, ztr: np.ndarray, bte: np.ndarray, ste: np.ndarray, lam: float
) -> np.ndarray:
    """Least squares on [B, S] with penalty lam on the S slopes only; slopes-only prediction."""
    xtr = np.column_stack([btr, str_])
    xte = np.column_stack([bte, ste])
    mu = xtr.mean(0)
    a = xtr - mu
    pen = np.r_[np.zeros(btr.shape[1]), np.full(str_.shape[1], lam)]
    b = np.linalg.lstsq(a.T @ a + np.diag(pen), a.T @ ztr, rcond=None)[0]
    return (xte - mu) @ b  # type: ignore[no-any-return]


# ---------- planted control ----------


def planted(z: np.ndarray, i0: int, kind: str, h: int, seed: int) -> np.ndarray:
    """A synthetic input whose pooled in-sample IC with z (cells from row i0) is PLANT_RHO.
    `fast`: noise with the target's own h-week overlap; `slow`: AR(1) noise, 26-week half-life."""
    f, n = z.shape
    rng = np.random.default_rng(seed)
    if kind == "fast":
        w = rng.standard_normal((f + h, n))
        e = np.sum([w[j : j + f] for j in range(h)], axis=0) / math.sqrt(h)
    else:
        phi = 0.5 ** (1 / 26)
        w = rng.standard_normal((f + 200, n))
        acc = np.zeros_like(w)
        for i in range(1, len(w)):
            acc[i] = phi * acc[i - 1] + w[i]
        e = acc[200:]
    keep = np.isfinite(z)
    keep[:i0] = False
    zs = z[keep] - z[keep].mean()
    zs /= zs.std()
    ev = e[keep] - e[keep].mean()
    ev -= (ev @ zs) / (zs @ zs) * zs
    ev /= ev.std()
    out = np.full(z.shape, np.nan)
    out[keep] = PLANT_RHO * zs + math.sqrt(1 - PLANT_RHO**2) * ev
    return out


# ---------- the run ----------


def load() -> tuple[rl_env.Table, np.ndarray]:
    rt = rl2_data.load()["six"]
    return rt.t, rt.coin


def run(log: bool) -> None:
    t0 = time.time()
    t, coin = load()
    g = Grid(t)
    xs, grp = inputs(t, coin)
    names = list(xs)
    us = np.random.default_rng(0).random(N_ROT)
    trend = [np.where(t.elig, t.X[:, :, k], 0.0) for k in range(len(TREND))]
    recs: list[dict[str, Any]] = []
    for h in HORIZONS:
        z = horizon_z(t, h)
        for name in names:
            rec = measure(name, xs[name], z, h, t, g, us, None if name in TREND else trend)
            rec["group"] = grp[name]
            recs.append(rec)
            print(f"h={h} {name} {time.time() - t0:.0f}s", file=sys.stderr, flush=True)
    # controls (same rotations, judged against the same critical value, outside the family)
    ctrl: list[dict[str, Any]] = []
    for h in HORIZONS:
        z = horizon_z(t, h)
        for j, kind in enumerate(("fast", "slow")):
            x = planted(z, g.i0, kind, h, 100 * h + j)
            rec = measure(f"plant10-{kind}", x, z, h, t, g, us, trend)
            rec["group"] = "control"
            ctrl.append(rec)
    # combined forecasts
    non_trend = [k for k in names if k not in TREND]
    u_arr = np.stack([xs[k] for k in non_trend])
    rng = np.random.default_rng(0)
    length = g.f - g.i0
    shifts = rng.integers(MIN_SHIFT, length - MIN_SHIFT, N_ROT_COMBO)
    combos: dict[str, Any] = {}
    for h in HORIZONS:
        z = horizon_z(t, h)
        obs = combo_gains(u_arr, non_trend, z, t, g)
        null = {k: np.full(N_ROT_COMBO, np.nan) for k in COMBOS}
        for r, s in enumerate(shifts):
            ur = u_arr.copy()
            ur[:, g.i0 :] = np.roll(u_arr[:, g.i0 :], int(s), axis=1)
            gr = combo_gains(ur, non_trend, z, t, g)
            for k in COMBOS:
                null[k][r] = gr[k]
        combos[str(h)] = {"obs": obs, "null": {k: v.tolist() for k, v in null.items()}}
        print(f"combos h={h} {time.time() - t0:.0f}s", file=sys.stderr, flush=True)
    np.savez_compressed(
        out_dir() / "nulls.npz",
        **{
            f"{r['name']}|{r['h']}|{k}": r[f"null_{k}"]
            for r in [*recs, *ctrl]
            if "ic" in r
            for k in ("ic", "per", "pool")
        },
    )
    res = finish(recs, ctrl, combos, t.book.syms)
    res["n_non_trend"] = len(non_trend)
    res["seconds"] = time.time() - t0
    (out_dir() / "slow1.json").write_text(json.dumps(res, indent=1))
    if log:
        log_rows(res)
    print(render(res))


def _stats(obs: float, null: np.ndarray) -> tuple[float, float, float, float, int]:
    """(null mean, null sd, studentised obs, single-test p, usable rotations)."""
    v = null[np.isfinite(null)]
    if len(v) < MIN_NULL or not np.isfinite(obs) or v.std() == 0:
        return float("nan"), float("nan"), float("nan"), float("nan"), len(v)
    return (
        float(v.mean()),
        float(v.std()),
        float((obs - v.mean()) / v.std()),
        float((v >= obs).mean()),
        len(v),
    )


def finish(
    recs: list[dict[str, Any]],
    ctrl: list[dict[str, Any]],
    combos: dict[str, Any],
    syms: list[str],
) -> dict[str, Any]:
    """Studentise, maxT critical values, verdicts; drops the raw null arrays."""
    zcols = []
    for rec in recs:
        if "ic" not in rec:
            continue
        for mdl in ("per", "pool"):
            v = rec[f"null_{mdl}"]
            ok = np.isfinite(v)
            if ok.sum() >= MIN_NULL and v[ok].std() > 0 and np.isfinite(rec[f"wf_{mdl}"]):
                zc = np.full(len(v), np.nan)
                zc[ok] = (v[ok] - v[ok].mean()) / v[ok].std()
                zcols.append(zc)
    zmat = np.column_stack(zcols)
    crit = float(np.percentile(np.nanmax(zmat, axis=1), 95))
    out_recs = []
    for rec in [*recs, *ctrl]:
        if "ic" not in rec:
            out_recs.append(rec)
            continue
        r = {k: v for k, v in rec.items() if not k.startswith("null_")}
        v = rec["null_ic"][np.isfinite(rec["null_ic"])]
        r["n_null"] = len(v)
        if len(v) >= MIN_NULL:
            r["chance"] = float(np.percentile(np.abs(v), 95))
            r["neff"] = float(1 / v.var()) if v.var() > 0 else float("nan")
        else:
            r["chance"], r["neff"] = float("nan"), float("nan")
        best = None
        for mdl in ("per", "pool"):
            mean, sd, zz, p, _ = _stats(rec[f"wf_{mdl}"], rec[f"null_{mdl}"])
            r[f"mean_{mdl}"], r[f"sd_{mdl}"], r[f"z_{mdl}"], r[f"p_{mdl}"] = mean, sd, zz, p
            r[f"mde_{mdl}"] = mean + (crit + 0.84) * sd
            if np.isfinite(zz) and (best is None or zz > r[f"z_{best}"]):
                best = mdl
        r["best"] = best
        r["verdict"] = verdict(r, crit)
        out_recs.append(r)
    # combined forecasts: maxT over the 6 gains
    cz, cres = [], []
    for h, c in combos.items():
        for k in COMBOS:
            v = np.array(c["null"][k])
            mean, sd, zz, p, n_ok = _stats(c["obs"][k], v)
            cz.append((v - mean) / sd)
            cres.append({
                "h": int(h), "name": k, "gain": c["obs"][k], "base": c["obs"]["B"],
                "mean": mean, "sd": sd, "z": zz, "p": p, "n_null": n_ok,
            })  # fmt: skip
    ccrit = float(np.percentile(np.nanmax(np.column_stack(cz), axis=1), 95))
    for c in cres:
        c["verdict"] = (
            "**survives**" if c["gain"] >= BAR_GAIN and c["z"] >= ccrit else "no"
        )  # fmt: skip
    return {
        "stamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M"),
        "crit": crit, "family": len(zcols), "combo_crit": ccrit, "syms": syms,
        "recs": [r for r in out_recs if r.get("group") != "control"],
        "controls": [r for r in out_recs if r.get("group") == "control"],
        "combos": cres,
    }  # fmt: skip


def best_wf(r: dict[str, Any]) -> float:
    vals = [r[k] for k in ("wf_per", "wf_pool") if np.isfinite(r[k])]
    return max(vals) if vals else float("nan")


def verdict(r: dict[str, Any], crit: float) -> str:
    over, near = False, False
    for mdl in ("per", "pool"):
        wf, zz, p = r[f"wf_{mdl}"], r[f"z_{mdl}"], r[f"p_{mdl}"]
        if not (np.isfinite(wf) and np.isfinite(zz)):
            continue
        over |= wf >= BAR_WF and zz >= crit
        near |= wf >= NEAR_WF and p < 0.05
    if over:
        return "trend (already in `tsmom12`)" if r.get("group") == "trend" else "**survives**"
    return "near" if near else "no"


# ---------- output ----------


def log_rows(res: dict[str, Any]) -> None:
    stamp = res["stamp"]
    lines = []
    for r in res["recs"]:
        if "ic" not in r:
            desc, first = f"{r['name']} h={r['h']}w (no data: {r['cells']} cells)", "-"
        else:
            b = r["best"]
            zz = f"{r[f'z_{b}']:+.2f}" if b else "nan"
            desc = (
                f"{r['name']} h={r['h']}w (IC {r['ic']:+.3f}, chance {r['chance']:.3f}, "
                f"WF {best_wf(r):+.3f}, z {zz} vs {res['crit']:.2f}, {r['verdict'].strip('*')})"
            )
            first = r["first"]
        lines.append(
            f"| {stamp} | {IDEA} | {desc} | screen | train | {first} | 2025-11-09 | - | - | - | - |"
        )
    for c in res["combos"]:
        desc = (
            f"combined {c['name']} h={c['h']}w (gain {c['gain']:+.3f} over up_12m "
            f"{c['base']:+.3f}, z {c['z']:+.2f} vs {res['combo_crit']:.2f}, "
            f"{c['verdict'].strip('*')})"
        )
        lines.append(
            f"| {stamp} | {IDEA} | {desc} | screen | train | 2000-01-07 | 2025-11-09 "
            "| - | - | - | - |"
        )
    for r in res["controls"]:
        b = r["best"]
        desc = (
            f"{r['name']} h={r['h']}w (planted IC {r['ic']:+.3f}, WF {best_wf(r):+.3f}, "
            f"z {r[f'z_{b}']:+.2f} vs {res['crit']:.2f})"
        )
        lines.append(
            f"| {stamp} | slow-1-control | {desc} | control | train | {r['first']} | 2025-11-09 "
            "| - | - | - | - |"
        )
    with harness.TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write("\n".join(lines) + "\n")


def _n(x: Any, spec: str = "+.3f") -> str:
    return "" if x is None or not np.isfinite(x) else format(x, spec)


def render(res: dict[str, Any]) -> str:
    crit = res["crit"]
    out = [
        "# Slow 1: 4-week and 13-week IC screen (six assets, 2000-01-07 to 2025-11-09)",
        "",
        "Script `lib/slow1_ic.py`, card `research/slow-1.md`. Descriptive: no backtest, held-out",
        "year not loaded. IC = Pearson correlation of the input with the coming `h` weeks'",
        "risk-adjusted return (`horizon_z`), all Fridays (overlapping windows). Non-overlap = the",
        "same IC on every `h`-th Friday, mean (min..max) over the `h` starting weeks. Chance =",
        f"95th percentile of |IC| over {N_ROT} circular rotations of the input in its own span;",
        "N eff = 1 / variance of that null (independent observations the IC is worth). WF =",
        "walk-forward IC (OLS refitted every two years, a year's gap; `per` = a slope per asset,",
        "`pool` = one slope). z = the better WF IC minus its null mean, over its null sd. Wk-eq =",
        "best WF IC / sqrt(h), the weekly IC of the same value. Detectable = the smallest true WF",
        "IC the screen would flag four times in five. Gain = WF IC of the 7 trend inputs + the",
        "input minus the trend inputs alone.",
        "",
        f"**Family: {res['family']} walk-forward ICs. maxT critical value (5% family-wise, "
        f"one-sided): z >= {crit:.2f}.** An input survives with WF IC >= {BAR_WF:.2f} and "
        f"z >= {crit:.2f}.",
        "",
    ]
    for h in HORIZONS:
        out += [f"## Horizon {h} weeks", ""]
        out.append(
            "| Input | Kind | From | Weeks | Cells | IC | rank IC | IC held | Non-overlap "
            "| Chance | N eff | WF per | WF pool | z | Wk-eq | Detectable | Gain | Verdict |"
        )
        out.append(
            "|---|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|---|"
        )
        for r in [x for x in res["recs"] if x["h"] == h]:
            out.append(_row(r))
        out.append("")
    out += ["## Closest to the bar (top 12 by z, both horizons)", ""]
    out.append("| Input | h | WF IC | model | z | single-test p | Wk-eq | N eff | Verdict |")
    out.append("|---|---:|---:|---|---:|---:|---:|---:|---|")
    ranked = sorted(
        [r for r in res["recs"] if r.get("best")], key=lambda r: -r[f"z_{r['best']}"]
    )[:12]  # fmt: skip
    for r in ranked:
        b = r["best"]
        out.append(
            f"| `{r['name']}` | {r['h']} | {r[f'wf_{b}']:+.3f} | {b} | {r[f'z_{b}']:+.2f} | "
            f"{r[f'p_{b}']:.3f} | {r[f'wf_{b}'] / math.sqrt(r['h']):+.3f} | {_n(r['neff'], '.0f')} "
            f"| {r['verdict']} |"
        )
    out += ["", "## Combined forecasts (gain over `tsmom12`'s own state)", ""]
    out += [
        "`B` = walk-forward forecast from `up_12m` alone (a slope per asset). Gain = walk-forward",
        f"IC of the combined model minus `B`'s. Null: the {res.get('n_non_trend', 42)} non-trend",
        f"inputs rotated together, {N_ROT_COMBO} rotations. maxT critical value over the 6 gains:",
        f"z >= {res['combo_crit']:.2f}. Survives with gain >= +{BAR_GAIN:.2f} and z above that.",
        "",
        "| Combined | h | WF IC of `B` | Gain | Null mean | Null sd | z | p | Verdict |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|",
    ]
    for c in res["combos"]:
        out.append(
            f"| `{c['name']}` | {c['h']} | {c['base']:+.3f} | {c['gain']:+.3f} | {c['mean']:+.3f} "
            f"| {c['sd']:.3f} | {c['z']:+.2f} | {c['p']:.3f} | {c['verdict']} |"
        )
    out += ["", "## Planted controls (true in-sample IC 0.10; not strategies)", ""]
    out.append(
        "| Control | h | IC | Chance | N eff | WF per | WF pool | z | Flagged "
        f"(WF >= {BAR_WF:.2f} and z >= {crit:.2f}) |"
    )
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---|")
    for r in res["controls"]:
        b = r["best"]
        flag = "yes" if r["verdict"] == "**survives**" else "no"
        out.append(
            f"| `{r['name']}` | {r['h']} | {r['ic']:+.3f} | {r['chance']:.3f} | {r['neff']:.0f} | "
            f"{r['wf_per']:+.3f} | {r['wf_pool']:+.3f} | {r[f'z_{b}']:+.2f} | {flag} |"
        )
    syms = res["syms"]
    for h in HORIZONS:
        out += ["", f"## IC per asset, {h} weeks (in sample, descriptive)", ""]
        out.append("| Input | " + " | ".join(syms) + " |")
        out.append("|---|" + "---:|" * len(syms))
        for r in [x for x in res["recs"] if x["h"] == h and "per_asset" in x]:
            cells = " | ".join(_n(r["per_asset"][s]) for s in syms)
            out.append(f"| `{r['name']}` | {cells} |")
    return "\n".join(out)


def _row(r: dict[str, Any]) -> str:
    if "ic" not in r:
        return f"| `{r['name']}` | {r['group']} | no data | | {r['cells']} |" + " |" * 13
    b = r["best"]
    zz = _n(r[f"z_{b}"], "+.2f") if b else ""
    mde = _n(r[f"mde_{b}"], ".3f") if b else ""
    wk = _n(best_wf(r) / math.sqrt(r["h"]))
    nov = f"{r['nov_mean']:+.3f} ({r['nov_min']:+.2f}..{r['nov_max']:+.2f})"
    return (
        f"| `{r['name']}` | {r['group']} | {r['first']} | {r['weeks']} | {r['cells']} | "
        f"{r['ic']:+.3f} | {r['ric']:+.3f} | {_n(r['held'])} | {nov} | {_n(r['chance'], '.3f')} | "
        f"{_n(r['neff'], '.0f')} | {_n(r['wf_per'])} | {_n(r['wf_pool'])} | {zz} | {wk} | {mde} | "
        f"{_n(r.get('gain'))} | {r['verdict']} |"
    )


# ---------- h = 1 reproduction of the public tables ----------


def _md_table(path: Path, first_col: str) -> dict[str, list[str]]:
    rows: dict[str, list[str]] = {}
    on = False
    for line in path.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == first_col:
            on = True
            continue
        if on and line.startswith("| `"):
            rows.setdefault(cells[0].strip("`"), cells[1:])
        elif on and not line.startswith("|"):
            on = False
    return rows


def check() -> None:
    """Run the pipeline at h = 1 and compare with results/info-1.md and rl-3-inputs.md. Prints
    only the differences (the weekly numbers are already public)."""
    t, coin = load()
    g = Grid(t)
    xs, _ = inputs(t, coin)
    z = horizon_z(t, 1)
    zw = rl3_plant.week_z(t)
    ok = np.isfinite(zw)
    same = np.array_equal(np.isfinite(z), ok) and np.allclose(z[ok], zw[ok])
    print("horizon_z(h=1) == week_z:", same)
    trend = [np.where(t.elig, t.X[:, :, k], 0.0) for k in range(len(TREND))]
    us = np.random.default_rng(0).random(3)
    pub = _md_table(harness.RESEARCH / "results" / "info-1.md", "Candidate")
    worst = 0.0
    for name in inf.CANDIDATES:
        r = measure(name, xs[name], z, 1, t, g, us, trend)
        p = pub[name]
        mine = [r["ic"], r["ric"], r["held"], r["wf_per"], r["wf_pool"], r["wf_trend"], r["gain"]]
        theirs = [p[3], p[4], p[5], p[7], p[8], p[9], p[10]]
        for a, b in zip(mine, theirs, strict=True):
            if "nan" in b:
                continue
            worst = max(worst, abs(a - float(b)))
        if int(p[2]) != r["cells"]:
            print("cells differ", name, p[2], r["cells"])
    print(f"info-1 table: largest difference in 7 columns x 23 inputs = {worst:.4f}")
    text = (harness.RESEARCH / "results" / "rl-3-inputs.md").read_text().split("## cells")[0]
    worst = 0.0
    for m in re.finditer(r"\| `(\w+)` \| ([+-][0-9.]+) \|", text):
        if m.group(1) in xs:
            r = measure(m.group(1), xs[m.group(1)], z, 1, t, g, us[:0], None)
            d = abs(r["ic"] - float(m.group(2)))
            if d > 0.0006:
                print("  differs:", m.group(1), f"{d:.4f}")
            worst = max(worst, d)
    print(f"rl-3 inputs table: largest IC difference = {worst:.4f}")
    # plumbing of the rest (no statistic printed)
    non_trend = [k for k in xs if k not in TREND]
    u_arr = np.stack([xs[k] for k in non_trend])
    cg = combo_gains(u_arr, non_trend, z, t, g)
    pl = planted(z, g.i0, "slow", 1, 0)
    keep = np.isfinite(z)
    keep[: g.i0] = False
    print("combined forecasts computed:", sorted(cg), "| non-trend inputs:", len(non_trend))
    print("planted IC exact:", abs(corr(pl[keep], z[keep]) - PLANT_RHO) < 1e-9)
    print("inputs:", len(xs))


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--report" in sys.argv:
        print(render(json.loads((out_dir() / "slow1.json").read_text())))
    elif "--run" in sys.argv:
        run("--log" in sys.argv)
    else:
        sys.exit(__doc__)
