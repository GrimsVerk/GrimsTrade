"""Replication of slow-1's `usd_13w` on data the screen never used (card: research/usd-1.md).

    uv run python -I research/lib/usd1.py --check       # slow-1's public numbers, coverage
    uv run python -I research/lib/usd1.py --fetch       # the Fed's old index (robustness only)
    uv run python -I research/lib/usd1.py --run --log   # the replication (once): json + rows
    uv run python -I research/lib/usd1.py --report      # results/usd-1.md from the json

Sign fixed on the card: a dollar that rose over 13 weeks is followed by a worse stretch, so
every statistic is S = -IC (S > 0 = same sign as the screen). Sets: `before` (four stock indexes,
Fridays whose window closes by 2000-01-07), `markets` (18 risk markets of the 33-market pool from
2000), `coins` (Coin Metrics wide book without BTC and ETH). Chance: the weekly dollar series is
rotated in time, one rotation for all sets. Descriptive: no backtest, train bars only. Needs RL
2's `tables2.pkl`, breadth-1's Coin Metrics panel and the shared cache; writes only
`<cache_root>/derived/usd-1/` (and `<cache_root>/downloads/usd-1/` with `--fetch`).
"""

from __future__ import annotations

import csv
import fcntl
import json
import math
import pickle
import sys
import urllib.request
from collections.abc import Sequence
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import breadth_xs as xs  # noqa: E402
import harness  # noqa: E402
import info1_features as inf  # noqa: E402
import macro  # noqa: E402
import rl2_data  # noqa: E402
import rl_env  # noqa: E402
import slow1_ic as s1  # noqa: E402

HORIZONS = (13, 4)  # 13 weeks carries the bar; 4 weeks is a secondary reading
N_ROT = 2000
GRID_START = date(1971, 1, 1)  # a Friday; the dollar file starts 1971-01-04
SCREEN_START = date(2000, 1, 7)  # slow-1's first Friday
CHANGE_DAYS = 91
LAG_FED = 7  # the Fed's H.10 release was weekly
MIN_RESID_CELLS = 26
MIN_COIN_CELLS = 52  # per-coin S is only counted from a year of cells
MIN_COINS = 5
P_BAR = 0.05
POWER = 1.645 + 0.84  # true IC caught four times in five by a one-sided 5% test
IDEA = "usd-1"

BEFORE = ["GSPC", "N225", "FTSE", "GDAXI"]
MARKET_ETFS = ["IWM", "EFA", "EEM", "VNQ", "DBC", "SLV"]
MARKET_IDX = ["N225", "FTSE", "GDAXI"]
LEFT_OUT = {"etf": ["IEF", "LQD"], "idx": ["GSPC"]}
SIX_COINS = ["ltc", "xrp", "bch", "etc", "xlm", "dash"]
ERAS = {
    "before": [("1971-79", 1971, 1979), ("1980-89", 1980, 1989), ("1990-99", 1990, 1999)],
    "markets": [("2000-09", 2000, 2009), ("2010-16", 2010, 2016), ("2017-21", 2017, 2021),
                ("2022-25", 2022, 2025)],
    "coins": [("2017-21", 2017, 2021), ("2022-25", 2022, 2025)],
}  # fmt: skip
ERAS["six"] = ERAS["markets"]
# slow-1's published numbers for `usd_13w` (results/slow-1.md), for the reproduction
PUBLIC = {
    13: {"ic": -0.115, "cells": 5930, "wf_per": 0.151, "wf_pool": 0.125,
         "per_asset": {"BTC": -0.363, "ETH": -0.427, "SPY": -0.096, "QQQ": -0.109,
                       "GLD": -0.031, "TLT": 0.034}},
    4: {"ic": -0.053, "cells": 5984, "wf_per": 0.045, "wf_pool": 0.026,
        "per_asset": {"BTC": -0.211, "ETH": -0.195, "SPY": -0.041, "QQQ": -0.059,
                      "GLD": -0.032, "TLT": 0.065}},
}  # fmt: skip
FED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=DTWEXM"
FED_STAMP = "2026-11-18"


def out_dir() -> Path:
    p = macro.cache_root() / "derived" / "usd-1"
    p.mkdir(parents=True, exist_ok=True)
    return p


def fed_path() -> Path:
    return macro.cache_root() / "downloads" / "usd-1" / "fred-graph" / FED_STAMP / "DTWEXM.csv"


# ---------- the grid and the dollar ----------


def grid() -> list[date]:
    out, d = [], GRID_START
    while d <= harness.TRAIN_END:
        out.append(d)
        d += timedelta(days=7)
    return out


def usd_change(obs: inf.Obs, lag: int, fridays: Sequence[date]) -> np.ndarray:
    """`usd_13w` as info-1 defined it, for any dollar series: log change over 91 calendar days,
    usable `lag` days after the observation, at most `inf.MAX_AGE` days old."""
    ds, v = obs
    return inf.asof(ds, inf.calendar_change(ds, v, CHANGE_DAYS), lag, fridays)


def fred_latest(series: str) -> inf.Obs:
    recs = macro.market_records(series)
    return [r.obs for r in recs], np.array([r.value for r in recs])


def fed_major() -> inf.Obs | None:
    """The Fed's discontinued major-currencies index, if `--fetch` got it. Read as data only."""
    p = fed_path()
    if not p.exists():
        return None
    ds, vs = [], []
    with p.open(newline="") as f:
        for row in csv.reader(f):
            try:
                d, x = date.fromisoformat(row[0].strip()), float(row[1])
            except (ValueError, IndexError):
                continue
            ds.append(d)
            vs.append(x)
    return (ds, np.array(vs)) if len(ds) > 1000 else None


def fetch_fed() -> None:
    """One plain request for the public CSV. On 2026-11-18 FRED did not answer it (timeout, then
    a reset): the robustness row that needs this file was dropped, as the card allows."""
    p = fed_path()
    if p.exists():
        print("already there:", p)
        return
    req = urllib.request.Request(FED_URL, headers={"User-Agent": "research-script"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        body: bytes = resp.read()
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(body)
    print("saved", p, len(body), "bytes")


# ---------- statistics (x is one number per Friday, the same for every asset) ----------


def fill_inside(x: np.ndarray) -> tuple[np.ndarray, int]:
    """x with the NaNs inside its finite span carried forward (count returned)."""
    rows = np.flatnonzero(np.isfinite(x))
    out = x.copy()
    holes = 0
    for i in range(int(rows[0]) + 1, int(rows[-1]) + 1):
        if not np.isfinite(out[i]):
            out[i] = out[i - 1]
            holes += 1
    return out, holes


def rotations(x: np.ndarray, us: np.ndarray) -> np.ndarray:
    """[1 + R, G]: x (row 0) and its circular rotations inside its own finite span, each by at
    least `s1.MIN_SHIFT` weeks from either end. x must have no NaN inside the span."""
    rows = np.flatnonzero(np.isfinite(x))
    r0, r1 = int(rows[0]), int(rows[-1]) + 1
    if not np.isfinite(x[r0:r1]).all():
        raise ValueError("NaN inside the span: fill_inside first")
    out = np.repeat(x[None], len(us) + 1, 0)
    for k, u in enumerate(us):
        out[k + 1, r0:r1] = np.roll(x[r0:r1], s1.shift_of(float(u), r1 - r0))
    return out


def s_many(xr: np.ndarray, z: np.ndarray) -> np.ndarray:
    """S = -corr(x, z) over the finite cells of z [G, n], for every row of xr [R, G]."""
    rows = np.isfinite(xr[0])
    zz = z[rows]
    m = np.isfinite(zz)
    z0 = np.where(m, zz, 0.0)
    n = m.sum(1).astype(float)
    zs = z0.sum(1)
    tot = n.sum()
    out = np.full(len(xr), np.nan)
    if tot < 3:
        return out
    x = xr[:, rows]
    sx, sxx, sxz = x @ n, (x * x) @ n, x @ zs
    sz, szz = zs.sum(), float((z0 * z0).sum())
    vx, vz = sxx - sx * sx / tot, szz - sz * sz / tot
    ok = (vx > 0) & (vz > 0)
    out[ok] = -(sxz[ok] - sx[ok] * sz / tot) / np.sqrt(vx[ok] * vz)
    return out


def residual(z: np.ndarray, ref: np.ndarray, min_cells: int = MIN_RESID_CELLS) -> np.ndarray:
    """Each column of z minus its least-squares fit (intercept and slope) on ref, over the cells
    where both exist; NaN elsewhere and for a column with fewer than `min_cells` such cells."""
    out = np.full(z.shape, np.nan)
    for j in range(z.shape[1]):
        m = np.isfinite(z[:, j]) & np.isfinite(ref)
        if m.sum() < min_cells:
            continue
        r, y = ref[m] - ref[m].mean(), z[m, j]
        v = float(r @ r)
        b = float(r @ y) / v if v > 0 else 0.0
        out[m, j] = y - y.mean() - b * r
    return out


def walk_forward(
    x: np.ndarray, z: np.ndarray, years: np.ndarray, per: bool
) -> tuple[float, float, int, int]:
    """slow-1's walk-forward IC with the block years generalised: (pooled slope, slope per asset
    or NaN, test blocks, blocks whose fitted pooled slope is negative, the card's sign)."""
    g, n = z.shape
    m = np.isfinite(z) & np.isfinite(x)[:, None]
    xm = np.repeat(np.nan_to_num(x)[:, None], n, 1)
    ym = np.repeat(years[:, None], n, 1)
    am = np.repeat(np.arange(n)[None, :], g, 0)
    pp, pq, ys = [], [], []
    neg = 0
    for y0 in range(1972, 2026, 2):
        tr = m & (ym < y0 - 1)
        te = m & (ym >= y0) & (ym < y0 + 2)
        if not te.any() or int(tr.any(1).sum()) < s1.MIN_TRAIN_WEEKS:
            continue
        xtr, xte, ztr = xm[tr], xm[te], z[tr]
        pq.append(s1.fit_predict(xtr[:, None], ztr, xte[:, None]))
        neg += float((xtr - xtr.mean()) @ (ztr - ztr.mean())) < 0
        if per:
            pp.append(
                s1.fit_predict(s1.per_design(xtr, am[tr], n), ztr, s1.per_design(xte, am[te], n))
            )
        ys.append(z[te])
    if not ys:
        return math.nan, math.nan, 0, 0
    y = np.concatenate(ys)
    wf_per = s1.corr(np.concatenate(pp), y) if per else math.nan
    return s1.corr(np.concatenate(pq), y), wf_per, len(ys), neg


def measure(
    name: str,
    z: np.ndarray,
    xr: np.ndarray,
    fridays: Sequence[date],
    h: int,
    syms: Sequence[str],
    per: bool,
    eras: Sequence[tuple[str, int, int]] = (),
    wf: bool = True,
) -> dict[str, Any]:
    """Every statistic of one set at one horizon. `null` holds S under each rotation."""
    x = xr[0]
    years = np.array([d.year for d in fridays])
    z = np.where(np.isfinite(x)[:, None], z, np.nan)
    m = np.isfinite(z)
    rows = np.flatnonzero(m.any(1))
    rec: dict[str, Any] = {"name": name, "h": h, "cells": int(m.sum())}
    if rec["cells"] < 50:
        return rec
    s_all = s_many(xr, z)
    null = s_all[1:]
    rec["first"], rec["last"] = (
        fridays[int(rows[0])].isoformat(),
        fridays[int(rows[-1])].isoformat(),
    )
    rec["weeks"], rec["assets"] = len(rows), int(m.any(0).sum())
    rec["s"], rec["null"] = float(s_all[0]), null
    rec["p"] = float((null >= s_all[0]).mean())
    rec["null_mean"], rec["sd"] = float(null.mean()), float(null.std())
    rec["neff"], rec["detectable"] = 1 / float(null.var()), POWER * float(null.std())
    nov = []
    for ph in range(h):
        keep = (np.arange(len(x)) - int(rows[0])) % h == ph
        nov.append(float(s_many(xr[:1], np.where(keep[:, None], z, np.nan))[0]))
    rec["nov_mean"], rec["nov_min"], rec["nov_max"] = (
        float(np.nanmean(nov)), float(np.nanmin(nov)), float(np.nanmax(nov)),
    )  # fmt: skip
    with np.errstate(invalid="ignore"):
        basket = np.where(m.any(1), np.where(m, z, 0.0).sum(1) / np.maximum(m.sum(1), 1), np.nan)
    b_all = s_many(xr, basket[:, None])
    rec["basket"], rec["basket_p"] = float(b_all[0]), float((b_all[1:] >= b_all[0]).mean())
    per_s = {
        syms[j]: float(s_many(xr[:1], z[:, [j]])[0])
        for j in range(z.shape[1])
        if m[:, j].sum() >= (MIN_COIN_CELLS if len(syms) > 30 else 3)
    }
    if len(syms) > 30:
        v = np.array(list(per_s.values()))
        rec["coins_counted"], rec["coins_pos"] = len(v), int((v > 0).sum())
        rec["per_asset"] = {k: per_s[k] for k in SIX_COINS if k in per_s}
    else:
        rec["per_asset"] = per_s
    rec["eras"] = {}
    for era, a, b in eras:
        zk = np.where(((years >= a) & (years <= b))[:, None], z, np.nan)
        rec["eras"][era] = [float(s_many(xr[:1], zk)[0]), int(np.isfinite(zk).any(1).sum())]
    if wf:
        rec["wf_pool"], rec["wf_per"], rec["blocks"], rec["blocks_neg"] = walk_forward(
            x, z, years, per
        )
    return rec


def pooled(recs: Sequence[dict[str, Any]]) -> dict[str, Any]:
    """P = mean over the sets of S / (its null sd); p from the same joint rotations."""
    obs = float(np.mean([r["s"] / r["sd"] for r in recs]))
    null = np.mean([r["null"] / r["sd"] for r in recs], axis=0)
    return {
        "sets": [r["name"] for r in recs], "h": recs[0]["h"], "stat": obs,
        "p": float((null >= obs).mean()), "sd": float(null.std()),
        "positive": int(sum(r["s"] > 0 for r in recs)),
    }  # fmt: skip


# ---------- the sets ----------


def on_grid(
    t: rl_env.Table, z: np.ndarray, gi: dict[date, int], cols: Sequence[int], first: date
) -> np.ndarray:
    out = np.full((len(gi), len(cols)), np.nan)
    for i, d in enumerate(t.fridays):
        if d in gi and d >= first:
            out[gi[d]] = z[i, list(cols)]
    return out


def before_table() -> rl_env.Table:
    """The four indexes on Fridays 1971..1999, bars cut at slow-1's first Friday (so every
    window closes by then). Built once with the same code as RL 1's tables; our own arrays."""
    path = out_dir() / "before.pkl"
    if path.exists():
        with path.open("rb") as f:
            return pickle.load(f)  # type: ignore[no-any-return]
    hist = harness.load_history("train", True, BEFORE)
    hist = {s: [b for b in bars if b.date <= SCREEN_START] for s, bars in hist.items()}
    t = rl_env.build_table(
        hist, lambda d: [math.nan] * len(rl_env.MACRO_FEATS), GRID_START, date(1999, 12, 31)
    )
    with path.open("wb") as f:
        pickle.dump(t, f)
    return t


def cm_z(px: np.ndarray, elig: np.ndarray, h: int, halflife: float = 60) -> np.ndarray:
    """[D, N] `z_h` on Coin Metrics' clock (card: `coins`). A decision on day t knows prices
    stamped up to t - 1 (`elig` is already lagged that way) and earns the log return from the
    price stamped t + 1 to the price stamped t + 1 + 7h; a price that stops is carried forward."""
    d_n, n = px.shape
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.vstack([np.full((1, n), np.nan), np.log(px[1:] / px[:-1])])
    lam = 0.5 ** (1 / halflife)
    num, den = np.zeros(n), np.zeros(n)
    vol = np.full((d_n, n), np.nan)
    for d in range(d_n):
        f = np.isfinite(lr[d])
        num = np.where(f, lam * num + np.nan_to_num(lr[d]) ** 2, num)
        den = np.where(f, lam * den + 1.0, den)
        with np.errstate(invalid="ignore", divide="ignore"):
            vol[d] = np.sqrt(num / den * 365)
    pf = xs.ffill(px)
    z = np.full((d_n, n), np.nan)
    t = np.arange(1, d_n - 1 - 7 * h)
    with np.errstate(invalid="ignore", divide="ignore"):
        r = np.log(pf[t + 1 + 7 * h] / pf[t + 1])
        v = vol[t - 1]
        ok = elig[t] & (v > 0) & np.isfinite(r)
        z[t] = np.where(ok, np.clip(r / (v * math.sqrt(7 * h / 365)), -5, 5), np.nan)
    return z


def coin_set(fridays: Sequence[date], h: int) -> tuple[list[str], np.ndarray, np.ndarray]:
    """(alt names, z of the alts [G, n], reference = mean z of BTC and ETH [G])."""
    b = bb.cm_book()
    z = cm_z(b.px, b.elig, h)
    alt = [j for j, s in enumerate(b.names) if s not in ("btc", "eth")]
    ref_cols = [b.names.index("btc"), b.names.index("eth")]
    zg = np.full((len(fridays), len(alt)), np.nan)
    ref = np.full(len(fridays), np.nan)
    started = False
    for i, d in enumerate(fridays):
        k = (d - b.day0).days
        if not 0 <= k < len(z):
            continue
        started = started or int(b.elig[k, alt].sum()) >= MIN_COINS
        if started:
            zg[i] = z[k, alt]
            with np.errstate(invalid="ignore"):
                rr = z[k, ref_cols]
                ref[i] = np.nanmean(rr) if np.isfinite(rr).any() else np.nan
    return [b.names[j] for j in alt], zg, ref


def build(h: int, fridays: Sequence[date]) -> dict[str, Any]:
    """Every z panel of horizon h on the grid: {name: (syms, z)} plus the references."""
    gi = {d: i for i, d in enumerate(fridays)}
    tabs = rl2_data.load()
    out: dict[str, Any] = {}
    tb = before_table()
    out["before"] = (list(tb.book.syms), on_grid(tb, s1.horizon_z(tb, h), gi, range(4), GRID_START))
    syms: list[str] = []
    cols = []
    left_s: list[str] = []
    left = []
    for key, want in (("etf", MARKET_ETFS), ("sec", harness.SECTORS), ("idx", MARKET_IDX)):
        t = tabs[key].t
        z = s1.horizon_z(t, h)
        syms += want
        cols.append(on_grid(t, z, gi, [t.book.syms.index(s) for s in want], SCREEN_START))
        for s in LEFT_OUT.get(key, []):
            left_s.append(s)
            left.append(on_grid(t, z, gi, [t.book.syms.index(s)], SCREEN_START))
    out["markets"] = (syms, np.column_stack(cols))
    out["left-out"] = (left_s, np.column_stack(left))
    t6 = tabs["six"].t
    z6 = on_grid(t6, s1.horizon_z(t6, h), gi, range(len(t6.book.syms)), SCREEN_START)
    out["six"] = (list(t6.book.syms), z6)
    out["spy"] = z6[:, t6.book.syms.index("SPY")]
    names, zc, ref = coin_set(fridays, h)
    out["coins"] = (names, zc)
    out["coin_ref"] = ref
    tc = tabs["coin"].t
    out["six-coins"] = (
        list(tc.book.syms),
        on_grid(tc, s1.horizon_z(tc, h), gi, range(len(tc.book.syms)), GRID_START),
    )
    return out


# ---------- the run ----------


def run(log: bool) -> None:
    fr = grid()
    us = np.random.default_rng(0).random(N_ROT)
    x_dxy = usd_change(inf.yahoo_close("DX-Y.NYB"), inf.LAG_MARKET, fr)
    xr = rotations(x_dxy, us)
    alt_x: dict[str, np.ndarray] = {}
    holes: dict[str, int] = {}
    for key, obs in (("DTWEXBGS", fred_latest("DTWEXBGS")), ("DTWEXM", fed_major())):
        if obs is not None:
            xa, holes[key] = fill_inside(usd_change(obs, LAG_FED, fr))
            alt_x[key] = rotations(xa, us)
    res: dict[str, Any] = {
        "stamp": datetime.now(UTC).strftime("%Y-%m-%d %H:%M"), "n_rot": N_ROT,
        "main": [], "pooled": [], "resid": [], "six": [], "robust": [], "holes": holes,
    }  # fmt: skip
    nulls: dict[str, np.ndarray] = {}

    def keep(group: str, rec: dict[str, Any]) -> dict[str, Any]:
        if "null" in rec:
            nulls[f"{group}|{rec['name']}|{rec['h']}"] = rec["null"]
        res[group].append({k: v for k, v in rec.items() if k != "null"})
        return rec

    for h in HORIZONS:
        p = build(h, fr)
        main = []
        for name in ("before", "markets", "coins"):
            syms, z = p[name]
            main.append(
                keep("main", measure(name, z, xr, fr, h, syms, name != "coins", ERAS[name]))
            )
        res["pooled"].append(pooled(main))
        for name, ref in (("markets", p["spy"]), ("coins", p["coin_ref"])):
            syms, z = p[name]
            zr = residual(z, ref)
            rec = measure(f"{name}-resid", zr, xr, fr, h, syms, False, ERAS[name], wf=False)
            rec["dropped"] = int(np.isfinite(z).any(0).sum() - np.isfinite(zr).any(0).sum())
            keep("resid", rec)
        syms, z = p["six"]
        keep("six", measure("six", z, xr, fr, h, syms, True, ERAS["six"]))
        # robustness (cannot change the verdict)
        syms, z = p["six-coins"]
        keep("robust", measure("coins: the protocol's six, gym bars", z, xr, fr, h, syms, True))
        syms, z = p["before"]
        y74 = np.array([d.year >= 1974 for d in fr])
        keep(
            "robust",
            measure("before: from 1974", np.where(y74[:, None], z, np.nan), xr, fr, h, syms, True),
        )
        if "DTWEXM" in alt_x:
            keep(
                "robust",
                measure(
                    "before: Fed major-currencies index", z, alt_x["DTWEXM"], fr, h, syms, True
                ),
            )
        for name in ("markets", "coins"):
            syms, z = p[name]
            keep(
                "robust",
                measure(
                    f"{name}: Fed broad index (2006+)", z, alt_x["DTWEXBGS"], fr, h, syms,
                    name != "coins",
                ),
            )  # fmt: skip
        syms, z = p["left-out"]
        for j, s in enumerate(syms):
            keep("robust", measure(f"left out: {s} from 2000", z[:, [j]], xr, fr, h, [s], False))
    res["verdict"] = verdict(res)
    np.savez_compressed(out_dir() / "nulls.npz", **nulls)  # type: ignore[arg-type]
    (out_dir() / "usd1.json").write_text(json.dumps(res, indent=1))
    if log:
        log_rows(res)
    print(render(res))


def verdict(res: dict[str, Any]) -> dict[str, Any]:
    h = HORIZONS[0]
    pl = next(p for p in res["pooled"] if p["h"] == h)
    bf = next(r for r in res["main"] if r["h"] == h and r["name"] == "before")
    a = pl["stat"] > 0 and pl["p"] < P_BAR
    b = pl["positive"] >= 2
    c = bf["s"] > 0 and bf["p"] < P_BAR
    word = (
        "replicates" if a and b and c else "echo only" if a and b else "does not replicate"
    )  # fmt: skip
    return {"a": bool(a), "b": bool(b), "c": bool(c), "word": word}


# ---------- output ----------


def _desc(r: dict[str, Any]) -> str:
    return (
        f"{r['name']} h={r['h']}w (S {r['s']:+.3f}, p {r['p']:.3f}, null sd {r['sd']:.3f}, "
        f"{r['cells']} cells, {r['weeks']} weeks)"
    )


def log_rows(res: dict[str, Any]) -> None:
    stamp = res["stamp"]
    end = harness.TRAIN_END.isoformat()
    lines = []
    for group, kind in (("main", "screen"), ("resid", "screen"), ("robust", "robustness")):
        for r in res[group]:
            if "s" not in r:
                desc, first, last = (
                    f"{r['name']} h={r['h']}w (no data: {r['cells']} cells)",
                    "-",
                    end,
                )
            else:
                desc, first, last = _desc(r), r["first"], r["last"]
            lines.append(
                f"| {stamp} | {IDEA} | {desc} | {kind} | train | {first} | {last} | - | - | - | - |"
            )
    for p in res["pooled"]:
        desc = (
            f"pooled {'+'.join(p['sets'])} h={p['h']}w (P {p['stat']:+.2f}, p {p['p']:.3f}, "
            f"{p['positive']} of 3 sets S > 0)"
        )
        lines.append(
            f"| {stamp} | {IDEA} | {desc} | screen | train | {GRID_START} | {end} | - | - | - | - |"
        )
    with harness.TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write("\n".join(lines) + "\n")


def _n(x: Any, spec: str = "+.3f") -> str:
    return "" if x is None or not np.isfinite(x) else format(x, spec)


HEAD = (
    "| Set | From | To | Weeks | Cells | Assets | S | p | Null sd | N eff | Detectable | "
    "Non-overlap | Basket S (p) | WF pool | WF per | Blocks with the card's sign |\n"
    "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---|"
)


def _row(r: dict[str, Any], label: str | None = None) -> str:
    nm = label or f"`{r['name']}`"
    if "s" not in r:
        return f"| {nm} | no data | | | {r['cells']} |" + " |" * 11
    nov = f"{r['nov_mean']:+.3f} ({r['nov_min']:+.2f}..{r['nov_max']:+.2f})"
    blocks = f"{r['blocks_neg']} of {r['blocks']}" if r.get("blocks") else ""
    return (
        f"| {nm} | {r['first']} | {r['last']} | {r['weeks']} | {r['cells']} | {r['assets']} | "
        f"{r['s']:+.3f} | {r['p']:.3f} | {r['sd']:.3f} | {r['neff']:.0f} | {r['detectable']:.3f} | "
        f"{nov} | {r['basket']:+.3f} ({r['basket_p']:.3f}) | {_n(r.get('wf_pool'))} | "
        f"{_n(r.get('wf_per'))} | {blocks} |"
    )


def render(res: dict[str, Any]) -> str:
    v = res["verdict"]
    yes = {True: "yes", False: "no"}
    out = [
        "# USD 1: replication of `usd_13w` (table)",
        "",
        "Script `lib/usd1.py`, card `research/usd-1.md`. Descriptive: no backtest, train bars",
        "only, held-out year not loaded. `usd_13w` = the dollar index's (DXY) log change over the",
        "last 91 days, known the day before the Friday. **S = minus the correlation** of `usd_13w`",
        "with the coming `h` weeks' risk-adjusted return over all cells (every Friday, overlapping",
        "windows): **S > 0 = same sign as slow-1 found** (dollar up, then worse returns). p = the",
        f"share of {res['n_rot']} rotations of the weekly dollar series (one for all sets) with",
        "S at least as large, one-sided. Null sd = the spread of S under those rotations; N eff =",
        "1 / its variance (independent observations the S is worth); Detectable = 2.49 x null sd",
        "(the true IC this test would catch four times in five). Non-overlap = S on every `h`-th",
        "Friday, mean (min..max) over the `h` starting weeks. Basket S = the same correlation with",
        "one number per Friday (the set's average). WF = slow-1's walk-forward IC (slope refitted",
        "every two years; `pool` one slope, `per` a slope per asset), with the number of test",
        "blocks whose fitted pooled slope has the card's sign (negative).",
        "",
        f"**Verdict at 13 weeks: {v['word']}.** (a) pooled P > 0 with p < 0.05: {yes[v['a']]}. "
        f"(b) S > 0 in at least 2 of 3 sets: {yes[v['b']]}. (c) `before`, the only set that "
        f"shares no date with the screen, S > 0 with p < 0.05: {yes[v['c']]}.",
        "",
    ]
    for h in HORIZONS:
        tag = "the bar" if h == HORIZONS[0] else "secondary, not in the bar"
        out += [f"## Horizon {h} weeks ({tag})", "", HEAD]
        for r in res["main"]:
            if r["h"] == h:
                out.append(_row(r))
        pl = next(p for p in res["pooled"] if p["h"] == h)
        out.append(
            f"| **pooled** (sets count equally) | | | | | | P {pl['stat']:+.2f} | {pl['p']:.3f} | "
            f"{pl['sd']:.2f} | | | | | | | {pl['positive']} of 3 sets S > 0 |"
        )
        for r in res["resid"]:
            if r["h"] == h:
                out.append(_row(r))
        for r in res["six"]:
            if r["h"] == h:
                out.append(_row(r, "`six` (discovery sample, not a test)"))
        out.append("")
    out += [
        "`-resid` = the same set after taking out, per asset, the part of its return that the",
        "screen's own assets explain (SPY for `markets`; the mean of BTC and ETH for `coins`).",
        "S > 0 there means the dollar reaches those assets harder than it reached the screen's.",
        "P = the mean over the three sets of S / null sd.",
        "",
    ]
    for h in HORIZONS:
        out += [
            f"## S by era, {h} weeks (descriptive)",
            "",
            "| Set | Era | Weeks | S |",
            "|---|---|---:|---:|",
        ]
        for r in [*res["main"], *res["resid"]]:
            if r["h"] == h:
                for era, (s, w) in r.get("eras", {}).items():
                    out.append(f"| `{r['name']}` | {era} | {w} | {_n(s)} |")
        out.append("")
    for h in HORIZONS:
        out += [
            f"## S per asset, {h} weeks (descriptive)",
            "",
            "| Set | Asset | S |",
            "|---|---|---:|",
        ]
        for r in [*res["main"], *res["resid"], *res["six"]]:
            if r["h"] != h or "s" not in r:
                continue
            for s, val in r["per_asset"].items():
                out.append(f"| `{r['name']}` | {s} | {_n(val)} |")
            if "coins_counted" in r:
                out.append(
                    f"| `{r['name']}` | coins with S > 0 (of those with a year of cells) | "
                    f"{r['coins_pos']} of {r['coins_counted']} |"
                )
        out.append("")
    out += ["## Robustness (run with the same rotations; cannot change the verdict)", ""]
    for h in HORIZONS:
        out += [f"### {h} weeks", "", HEAD]
        for r in res["robust"]:
            if r["h"] == h:
                out.append(_row(r, r["name"]))
        out.append("")
    if res.get("holes"):
        out.append(
            "Fridays inside a Fed series' span with no value under the 21-day rule, carried "
            f"forward: {res['holes']}."
        )
    return "\n".join(out)


# ---------- reproduction of slow-1's public numbers, and coverage ----------


def check() -> None:
    fr = grid()
    gi = {d: i for i, d in enumerate(fr)}
    x = usd_change(inf.yahoo_close("DX-Y.NYB"), inf.LAG_MARKET, fr)
    t6 = rl2_data.load()["six"].t
    with np.errstate(all="ignore"):
        pub_x = inf.features(t6)["usd_13w"][:, 0]
    mine = np.array([x[gi[d]] for d in t6.fridays])
    same = np.array_equal(np.isfinite(mine), np.isfinite(pub_x)) and np.allclose(
        mine[np.isfinite(mine)], pub_x[np.isfinite(pub_x)]
    )
    print("usd_13w on the grid == info-1's feature on the six-asset Fridays:", same)
    i0 = int(np.flatnonzero(np.isfinite(x))[0])
    holes = int((~np.isfinite(x[i0:])).sum())
    print("dollar: first Friday with a value", fr[i0], "| NaN inside the span:", holes)
    xr = x[None]
    years = np.array([d.year for d in fr])
    for h in HORIZONS:
        p = build(h, fr)
        syms, z = p["six"]
        zz = np.where(np.isfinite(x)[:, None], z, np.nan)
        pub = PUBLIC[h]
        worst = abs(-float(s_many(xr, zz)[0]) - pub["ic"])
        for j, s in enumerate(syms):
            worst = max(worst, abs(-float(s_many(xr, zz[:, [j]])[0]) - pub["per_asset"][s]))
        wf_pool, wf_per, _, _ = walk_forward(x, zz, years, True)
        worst = max(worst, abs(wf_pool - pub["wf_pool"]), abs(wf_per - pub["wf_per"]))
        print(
            f"h={h}: six-asset cells {int(np.isfinite(zz).sum())} (public {pub['cells']}); largest "
            f"difference from slow-1's IC, per-asset IC and walk-forward ICs = {worst:.4f}"
        )
        # coverage of the replication sets: dates and counts only
        for name in ("before", "markets", "coins", "six-coins", "left-out"):
            syms, z = p[name]
            m = np.isfinite(z) & np.isfinite(x)[:, None]
            rows = np.flatnonzero(m.any(1))
            print(
                f"  {name}: {int(m.sum())} cells, {len(rows)} weeks, {fr[int(rows[0])]} .. "
                f"{fr[int(rows[-1])]}, {int(m.any(0).sum())} assets"
            )
        # clock check (plumbing): BTC on Coin Metrics' clock against BTC on the gym's bars
        b = bb.cm_book()
        zb = cm_z(b.px, b.elig, h)[:, b.names.index("btc")]
        a = np.array(
            [zb[(d - b.day0).days] if 0 <= (d - b.day0).days < len(zb) else np.nan for d in fr]
        )
        g = p["six"][1][:, p["six"][0].index("BTC")]
        ok = np.isfinite(a) & np.isfinite(g)
        print(f"  clock check: corr(BTC z, Coin Metrics clock vs gym bars) = "
              f"{s1.corr(a[ok], g[ok]):.3f} on {int(ok.sum())} Fridays")  # fmt: skip
    print("Fed major-currencies file present:", fed_major() is not None)


if __name__ == "__main__":
    if "--check" in sys.argv:
        check()
    elif "--fetch" in sys.argv:
        fetch_fed()
    elif "--report" in sys.argv:
        print(render(json.loads((out_dir() / "usd1.json").read_text())))
    elif "--run" in sys.argv:
        run("--log" in sys.argv)
    else:
        sys.exit(__doc__)
