"""Candidate inputs of research run info-1, look-ahead safe (card in research/info-1.md).

Every source becomes a series of (observation date, value) in time order. Derived values
(rolling means, z-scores, changes) use only earlier-or-equal observations. Each observation
then gets the day it may first be used (`avail`, the card's as-of rule per source), and a
Friday decision `d` takes the latest observation with `avail <= d` that is at most `MAX_AGE`
days old (else NaN). Files are read from the shared cache (`macro.cache_root()`), never run.

    features(table) -> {name: [F, n] array}, NaN where unknown or not applicable.
"""

from __future__ import annotations

import csv
import io
import json
import math
import zipfile
from collections.abc import Callable, Iterable, Sequence
from datetime import UTC, date, datetime
from pathlib import Path
from typing import TYPE_CHECKING

import macro

if TYPE_CHECKING:  # rl_env pulls in the source registry; keep it out of test imports
    from rl_env import Table
import numpy as np

MAX_AGE = 21
LAG_MARKET = 1  # market series: from the day after the observation
LAG_CRYPTO = 2  # crypto rows stamped UTC day x: from x + 2
LAG_COT = 4  # Tuesday positions, released Friday after the close: from Saturday
COT_DROP = (  # report dates whose release was delayed by a shutdown (card)
    (date(2013, 10, 1), date(2013, 10, 29)),
    (date(2018, 12, 21), date(2019, 3, 5)),
    (date(2025, 9, 30), date(9999, 1, 1)),
)
COT_CODES = {
    "SPY": "13874A",
    "QQQ": "209742",
    "TLT": "020601",
    "GLD": "088691",
    "BTC": "133741",
    "ETH": "146021",
}
COINS = {
    "BTC": ("BTCUSDT", "BTC-PERPETUAL", "btc", "BTC"),
    "ETH": ("ETHUSDT", "ETH-PERPETUAL", "eth", "ETH"),
}

Obs = tuple[list[date], np.ndarray]  # observation dates ascending, values


def asof(obs: Sequence[date], vals: np.ndarray, lag: int, fridays: Sequence[date]) -> np.ndarray:
    """Value at each Friday: the latest observation with obs + lag <= Friday, at most MAX_AGE
    days old at the Friday; NaN otherwise. Non-finite observations are skipped."""
    v = np.asarray(vals, float)
    keep = np.isfinite(v)
    o = np.array([d.toordinal() for d in obs], dtype=np.int64)[keep]
    v = v[keep]
    out = np.full(len(fridays), np.nan)
    if len(o) == 0:
        return out
    f = np.array([d.toordinal() for d in fridays], dtype=np.int64)
    idx = np.searchsorted(o + lag, f, side="right") - 1
    ok = (idx >= 0) & (f - o[np.maximum(idx, 0)] <= MAX_AGE)
    out[ok] = v[idx[ok]]
    return out


# ---------- small series helpers (all trailing) ----------


def roll_mean(v: np.ndarray, n: int) -> np.ndarray:
    out = np.full(len(v), np.nan)
    for i in range(n - 1, len(v)):
        w = v[i - n + 1 : i + 1]
        if np.isfinite(w).all():
            out[i] = w.mean()
    return out


def roll_z(v: np.ndarray, n: int, min_n: int) -> np.ndarray:
    out = np.full(len(v), np.nan)
    for i in range(len(v)):
        w = v[max(0, i - n + 1) : i + 1]
        w = w[np.isfinite(w)]
        if len(w) >= min_n and w.std() > 0 and np.isfinite(v[i]):
            out[i] = (v[i] - w.mean()) / w.std()
    return out


def daily_mean(days: Iterable[date], vals: Iterable[float]) -> Obs:
    acc: dict[date, list[float]] = {}
    for d, x in zip(days, vals, strict=True):
        if math.isfinite(x):
            acc.setdefault(d, []).append(x)
    ds = sorted(acc)
    return ds, np.array([float(np.mean(acc[d])) for d in ds])


def calendar_change(obs: Sequence[date], v: np.ndarray, days: int, log: bool = True) -> np.ndarray:
    """v[i] against the last observation at or before obs[i] - days (log ratio or difference)."""
    o = np.array([d.toordinal() for d in obs])
    j = np.searchsorted(o, o - days, side="right") - 1
    out = np.full(len(v), np.nan)
    ok = j >= 0
    a, b = v[ok], v[j[ok]]
    out[ok] = np.log(a / b) if log else a - b
    return out


def calendar_mean_ratio(obs: Sequence[date], v: np.ndarray, short: int, long: int) -> np.ndarray:
    """log(mean over the last `short` days / mean over the last `long` days); needs >= 90% of
    the long window's days present."""
    o = np.array([d.toordinal() for d in obs])
    out = np.full(len(v), np.nan)
    for i in range(len(v)):
        ws = (o > o[i] - short) & (o <= o[i])
        wl = (o > o[i] - long) & (o <= o[i])
        s, lg = v[ws], v[wl]
        s, lg = s[np.isfinite(s)], lg[np.isfinite(lg)]
        if len(lg) >= 0.9 * long and len(s) and s.mean() > 0 and lg.mean() > 0:
            out[i] = math.log(s.mean() / lg.mean())
    return out


def utc_day(ms: float) -> date:
    return datetime.fromtimestamp(ms / 1000, UTC).date()


# ---------- readers ----------


def root() -> Path:
    return macro.cache_root()


def cot_rows(report: str) -> dict[str, Obs]:
    """{asset: (report dates, rows)} for the six assets' contracts; rows are dicts."""
    folder = root() / "cftc" / report
    by: dict[str, dict[date, dict[str, str]]] = {a: {} for a in COT_CODES}
    code_to = {c: a for a, c in COT_CODES.items()}
    for zp in sorted(folder.glob("*.zip")):
        with zipfile.ZipFile(zp) as z:
            for name in z.namelist():
                rd = csv.DictReader(io.TextIOWrapper(z.open(name), "latin-1"))
                for row in rd:
                    row = {k.strip(): v for k, v in row.items() if k}
                    a = code_to.get(
                        row.get(
                            "CFTC Contract Market Code", row.get("CFTC_Contract_Market_Code", "")
                        ).strip()
                    )
                    if a is None:
                        continue
                    ds = (
                        row.get("As of Date in Form YYMMDD")
                        or row.get("As_of_Date_In_Form_YYMMDD")
                        or ""
                    ).strip()
                    yy = int(ds[:2])
                    d = date(2000 + yy if yy < 50 else 1900 + yy, int(ds[2:4]), int(ds[4:6]))
                    if any(lo <= d <= hi for lo, hi in COT_DROP):
                        continue
                    by[a][d] = row
    out: dict[str, Obs] = {}
    for a, m in by.items():
        ds = sorted(m)
        out[a] = (ds, np.array([m[d] for d in ds], dtype=object))
    return out


def _num(row: dict[str, str], *keys: str) -> float:
    for k in keys:
        if k in row and row[k].strip() not in ("", "."):
            return float(row[k])
    return math.nan


def cboe_index(name: str, col: str) -> Obs:
    p = root() / "cboe" / "2026-11-12" / f"{name}_History.csv"
    ds, vs = [], []
    with p.open() as f:
        for row in csv.DictReader(f):
            try:
                d = datetime.strptime(row["DATE"].strip(), "%m/%d/%Y").date()
                x = float(row[col])
            except (ValueError, KeyError):
                continue
            ds.append(d)
            vs.append(x)
    return ds, np.array(vs)


def cboe_pc(name: str) -> Obs:
    p = root() / "cboe-pc" / "2026-11-13" / f"{name}.csv"
    ds, vs = [], []
    with p.open() as f:
        for row in csv.reader(f):
            if len(row) < 5:
                continue
            try:
                d = datetime.strptime(row[0].strip(), "%m/%d/%Y").date()
                x = float(row[4])
            except ValueError:
                continue
            ds.append(d)
            vs.append(x)
    return ds, np.array(vs)


def yahoo_close(sym: str) -> Obs:
    raw = json.loads((root() / "yahoo-1d" / "2026-11-12" / f"{sym}.json").read_text())
    r = raw["chart"]["result"][0]
    off = int(r["meta"].get("gmtoffset", 0))
    closes = r["indicators"]["quote"][0]["close"]
    m: dict[date, float] = {}
    for ts, c in zip(r["timestamp"], closes, strict=True):
        if c is not None:
            m[datetime.fromtimestamp(ts + off, UTC).date()] = float(c)
    ds = sorted(m)
    return ds, np.array([m[d] for d in ds])


def binance_daily(kind: str, pair: str) -> Obs:
    base = root() / "binance" / "futures" / "um" / "monthly" / kind / pair
    files = sorted(base.glob("*.zip") if kind == "fundingRate" else (base / "1h").glob("*.zip"))
    days: list[date] = []
    vals: list[float] = []
    for zp in files:
        with zipfile.ZipFile(zp) as z:
            for name in z.namelist():
                for row in csv.reader(io.TextIOWrapper(z.open(name), "utf-8")):
                    try:
                        t = float(row[0])
                        x = float(row[2] if kind == "fundingRate" else row[4])
                    except (ValueError, IndexError):
                        continue
                    days.append(utc_day(t))
                    vals.append(x)
    return daily_mean(days, vals)


def deribit_daily(kind: str, inst: str) -> Obs:
    days: list[date] = []
    vals: list[float] = []
    for p in sorted((root() / "deribit" / kind / inst).glob("*.json")):
        res = json.loads(p.read_text()).get("result")
        if kind == "funding":
            for r in res or []:
                days.append(utc_day(r["timestamp"]))
                vals.append(float(r["interest_8h"]))
        else:
            for r in (res or {}).get("data", []):
                days.append(utc_day(r[0]))
                vals.append(float(r[4]))
    return daily_mean(days, vals)


def coinmetrics(asset: str, metric: str) -> Obs:
    p = root() / "coinmetrics" / "full" / "2026-11-13" / "assets" / asset / "page-000.json"
    rows = json.loads(p.read_text())["data"]
    ds, vs = [], []
    for r in rows:
        x = r.get(metric)
        ds.append(date.fromisoformat(str(r["time"])[:10]))
        vs.append(float(x) if x not in (None, "") else math.nan)
    return ds, np.array(vs)


def fear_greed() -> Obs:
    raw = json.loads((root() / "fear-greed" / "2026-11-12" / "fng.json").read_text())
    m = {utc_day(float(r["timestamp"]) * 1000): float(r["value"]) for r in raw["data"]}
    ds = sorted(m)
    return ds, np.array([m[d] for d in ds])


# ---------- features ----------


def book_series(t: Table, sym: str) -> Obs:
    """Daily closes of one asset of the table's book (bars only; no bars after train)."""
    j = t.book.syms.index(sym)
    c = t.book.closes[:, j]
    k = np.flatnonzero(np.isfinite(c))
    return [t.book.date(int(i)) for i in k], c[k]


def realised_vol(obs: Sequence[date], close: np.ndarray, n: int, per_year: int) -> np.ndarray:
    r = np.diff(np.log(close), prepend=np.nan)
    out = np.full(len(r), np.nan)
    for i in range(n, len(r)):
        out[i] = r[i - n + 1 : i + 1].std() * math.sqrt(per_year)
    return out


def align(a: Obs, b: Obs, f: Callable[[np.ndarray, np.ndarray], np.ndarray]) -> Obs:
    mb = dict(zip(a[0], a[1], strict=True))
    ds = [d for d in b[0] if d in mb]
    bv = dict(zip(b[0], b[1], strict=True))
    return ds, f(np.array([mb[d] for d in ds]), np.array([bv[d] for d in ds]))


def features(t: Table) -> dict[str, np.ndarray]:
    fr = t.fridays
    syms = t.book.syms
    n = len(syms)
    out: dict[str, np.ndarray] = {}

    def common(name: str, s: Obs, lag: int) -> None:
        out[name] = np.repeat(asof(s[0], s[1], lag, fr)[:, None], n, 1)

    def own(name: str, per: dict[str, Obs], lag: int) -> None:
        arr = np.full((len(fr), n), np.nan)
        for a, s in per.items():
            arr[:, syms.index(a)] = asof(s[0], s[1], lag, fr)
        out[name] = arr

    # COT
    leg = cot_rows("legacy")
    spec: dict[str, Obs] = {}
    for a, (ds, rows) in leg.items():
        v = np.array(
            [
                (
                    _num(r, "Noncommercial Positions-Long (All)")
                    - _num(r, "Noncommercial Positions-Short (All)")
                )
                / _num(r, "Open Interest (All)")
                for r in rows
            ]
        )
        spec[a] = (ds, v)
    own("cot_spec", spec, LAG_COT)
    own(
        "cot_spec_chg4",
        {a: (d, v - np.r_[[np.nan] * 4, v[:-4]]) for a, (d, v) in spec.items()},
        LAG_COT,
    )
    own("cot_spec_z3y", {a: (d, roll_z(v, 156, 104)) for a, (d, v) in spec.items()}, LAG_COT)
    tff = cot_rows("tff")
    for name, grp in (("cot_lev", "Lev_Money"), ("cot_am", "Asset_Mgr")):
        per: dict[str, Obs] = {}
        for a, (ds, rows) in tff.items():
            if a == "GLD" or not len(ds):
                continue
            v = np.array(
                [
                    (_num(r, f"{grp}_Positions_Long_All") - _num(r, f"{grp}_Positions_Short_All"))
                    / _num(r, "Open_Interest_All")
                    for r in rows
                ]
            )
            per[a] = (ds, v)
        own(name, per, LAG_COT)

    # crypto derivatives and on-chain
    fb, pb, fd, dv, pu, hg, tg = {}, {}, {}, {}, {}, {}, {}
    for a, (pair, inst, cm, dsym) in COINS.items():
        ds, v = binance_daily("fundingRate", pair)
        fb[a] = (ds, roll_mean(v, 7)) if len(ds) else (ds, v)
        ds, v = binance_daily("premiumIndexKlines", pair)
        pb[a] = (ds, roll_mean(v, 7)) if len(ds) else (ds, v)
        ds, v = deribit_daily("funding", inst)
        fd[a] = (ds, roll_mean(v, 7)) if len(ds) else (ds, v)
        dvol = deribit_daily("dvol", dsym)
        cs = book_series(t, a)
        rv = (cs[0], realised_vol(cs[0], cs[1], 30, 365) * 100)
        dv[a] = align(dvol, rv, lambda x, y: np.log(x / y))
        ds, v = coinmetrics(cm, "IssTotUSD")
        pu[a] = (ds, np.log(v / calendar_mean_ratio_level(ds, v, 365)))
        ds, v = coinmetrics(cm, "HashRate")
        hg[a] = (ds, calendar_mean_ratio(ds, v, 30, 365))
        ds, v = coinmetrics(cm, "TxCnt")
        tg[a] = (ds, calendar_mean_ratio(ds, v, 30, 365))
    own("fund_bn", fb, LAG_CRYPTO)
    own("prem_bn", pb, LAG_CRYPTO)
    own("fund_drb", fd, LAG_CRYPTO)
    own("dvol_rv", dv, LAG_CRYPTO)
    own("puell", pu, LAG_CRYPTO)
    own("hash_growth", hg, LAG_CRYPTO)
    own("tx_growth", tg, LAG_CRYPTO)
    ds, v = fear_greed()
    fg = (ds, roll_mean(v, 7) / 100)
    own("fng", {a: fg for a in COINS}, LAG_CRYPTO)

    # options / volatility (common)
    vix = cboe_index("VIX", "CLOSE")
    common(
        "vix_term", align(vix, cboe_index("VIX3M", "CLOSE"), lambda x, y: np.log(x / y)), LAG_MARKET
    )
    common(
        "vix_term6",
        align(vix, cboe_index("VIX6M", "CLOSE"), lambda x, y: np.log(x / y)),
        LAG_MARKET,
    )
    sk = cboe_index("SKEW", "SKEW")
    common("skew_z", (sk[0], roll_z(sk[1], 252, 200)), LAG_MARKET)
    common(
        "vvix_vix", align(cboe_index("VVIX", "VVIX"), vix, lambda x, y: np.log(x / y)), LAG_MARKET
    )
    spy = book_series(t, "SPY")
    rv_spy = (spy[0], realised_vol(spy[0], spy[1], 21, 252) * 100)
    common("vrp", align(vix, rv_spy, lambda x, y: x - y), LAG_MARKET)
    for name in ("total", "equity"):
        ds, v = cboe_pc(f"{name}pc")
        common(f"pc_{name}", (ds, roll_mean(v, 10)), LAG_MARKET)

    # cross-asset (common)
    for name, sym in (("usd_13w", "DX-Y.NYB"), ("oil_13w", "CL=F")):
        ds, v = yahoo_close(sym)
        common(name, (ds, calendar_change(ds, v, 91)), LAG_MARKET)
    hy, ief = yahoo_close("HYG"), yahoo_close("IEF")
    hyc = (hy[0], calendar_change(hy[0], hy[1], 91))
    iefc = (ief[0], calendar_change(ief[0], ief[1], 91))
    common("hy_ief_13w", align(hyc, iefc, lambda x, y: x - y), LAG_MARKET)
    return out


def calendar_mean_ratio_level(obs: Sequence[date], v: np.ndarray, long: int) -> np.ndarray:
    """Trailing mean over the last `long` calendar days (>= 90% of days present), else NaN."""
    o = np.array([d.toordinal() for d in obs])
    out = np.full(len(v), np.nan)
    for i in range(len(v)):
        w = v[(o > o[i] - long) & (o <= o[i])]
        w = w[np.isfinite(w)]
        if len(w) >= 0.9 * long and w.mean() > 0:
            out[i] = w.mean()
    return out


CANDIDATES = [
    "cot_spec",
    "cot_spec_chg4",
    "cot_spec_z3y",
    "cot_lev",
    "cot_am",
    "fund_bn",
    "prem_bn",
    "fund_drb",
    "dvol_rv",
    "puell",
    "hash_growth",
    "tx_growth",
    "fng",
    "vix_term",
    "vix_term6",
    "skew_z",
    "vvix_vix",
    "vrp",
    "pc_total",
    "pc_equity",
    "usd_13w",
    "oil_13w",
    "hy_ief_13w",
]
COMMON = {
    "vix_term",
    "vix_term6",
    "skew_z",
    "vvix_vix",
    "vrp",
    "pc_total",
    "pc_equity",
    "usd_13w",
    "oil_13w",
    "hy_ief_13w",
}
