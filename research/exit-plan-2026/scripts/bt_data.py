"""Loaders for the exit-plan backtests (lane bt). Data are untrusted downloads: parsed as JSON/CSV
only. Paths come from the environment so nothing machine-specific is committed:

- BT_CACHE: the cache dated 2026-11-12 (yahoo-1d/2026-11-12, cboe/2026-11-12, fred/api/latest,
  shiller/ie_data.xls under it). Default: GRIMSTRADE_DATA, then `cache_root` in the gitignored
  research/macro.local.json (copy research/macro.local.json.example).
- BT_FRESH: the scratch dir with the Yahoo refresh (bt_fetch.sh); optional.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

TRAIN_END = pd.Timestamp("2025-11-09")


LOCAL = Path(__file__).resolve().parents[2] / "macro.local.json"  # gitignored, has .example


def cache() -> Path:
    root = os.environ.get("BT_CACHE") or os.environ.get("GRIMSTRADE_DATA")
    if not root and LOCAL.exists():
        root = json.loads(LOCAL.read_text())["cache_root"]
    if not root:
        raise SystemExit(
            f"set BT_CACHE or GRIMSTRADE_DATA, or copy {LOCAL.name}.example to {LOCAL.name}"
        )
    return Path(root).expanduser()


def _yahoo(path: Path) -> pd.Series:
    r = json.loads(path.read_text())["chart"]["result"][0]
    ts = pd.to_datetime(r["timestamp"], unit="s").normalize()
    close = r["indicators"]["quote"][0]["close"]
    s = pd.Series(close, index=ts, dtype="float64").dropna()
    s = s[~s.index.duplicated(keep="last")]
    return s[s > 0].sort_index()


def yahoo(sym: str, fresh: bool = True) -> pd.Series:
    """Daily closes; the fresh download if present, else the 2026-11-12 cache."""
    f = os.environ.get("BT_FRESH")
    if fresh and f and (Path(f) / f"{sym}.json").exists():
        try:
            return _yahoo(Path(f) / f"{sym}.json")
        except (KeyError, TypeError, IndexError):
            pass
    return _yahoo(cache() / "yahoo-1d" / "2026-11-12" / f"{sym}.json")


def cboe(name: str) -> pd.Series:
    df = pd.read_csv(cache() / "cboe" / "2026-11-12" / f"{name}_History.csv")
    s = pd.Series(df["CLOSE"].astype(float).values, index=pd.to_datetime(df["DATE"]))
    return s.sort_index()


def vix() -> pd.Series:
    """CBOE file, extended with the fresh Yahoo series for later days."""
    s = cboe("VIX")
    try:
        y = yahoo("^VIX")
        s = pd.concat([s, y[y.index > s.index[-1]]])
    except FileNotFoundError:
        pass
    return s


def vix3m() -> pd.Series:
    y = yahoo("^VIX3M")
    c = cboe("VIX3M")
    s = pd.concat([y, c[~c.index.isin(y.index)]]).sort_index()
    return s


def fred(series: str) -> pd.Series:
    d = cache() / "fred" / "api" / "latest" / series
    f = sorted(d.glob("*.json"))[-1]
    obs = json.loads(f.read_text())["observations"]
    s = pd.Series(
        [float(o["value"]) if o["value"] not in (".", "") else np.nan for o in obs],
        index=pd.to_datetime([o["date"] for o in obs]),
    )
    return s.dropna()


def shiller_monthly() -> pd.DataFrame:
    """Monthly real price, real earnings, Shiller CAPE (needs xlrd: `uv run --with xlrd`)."""
    import xlrd  # noqa: PLC0415

    sh = xlrd.open_workbook(str(cache() / "shiller" / "ie_data.xls")).sheet_by_name("Data")
    rows = [sh.row_values(i) for i in range(sh.nrows)]
    head = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
    out = []
    for r in rows[head + 1 :]:
        if not isinstance(r[0], float):
            continue
        y = int(r[0])
        m = round((r[0] - y) * 100)
        num = [(x if isinstance(x, float) else np.nan) for x in (r[7], r[10], r[12])]
        out.append((pd.Timestamp(y, m, 1), *num))
    df = pd.DataFrame(out, columns=["month", "real_price", "real_earn", "cape_shiller"])
    return df.set_index("month")


def cape_lagged(lag: int = 3) -> pd.Series:
    """CAPE with earnings shifted `lag` months: price(m) / mean real earnings(m-lag-119..m-lag).
    Indexed by the first day it may be used (first day of month m+1)."""
    df = shiller_monthly()
    e10 = df["real_earn"].shift(lag).rolling(120, min_periods=120).mean()
    cape = (df["real_price"] / e10).dropna()
    cape.index = cape.index + pd.offsets.MonthBegin(1)
    return cape


def expanding_pct(s: pd.Series) -> pd.Series:
    """Share of earlier values below the current one (no look-ahead)."""
    v = s.to_numpy()
    out = np.full(len(v), np.nan)
    for i in range(1, len(v)):
        out[i] = (v[:i] < v[i]).mean()
    return pd.Series(out, index=s.index)


def asof_daily(monthly: pd.Series, days: pd.DatetimeIndex) -> pd.Series:
    """Value in force on each day (the last monthly value whose use date is on or before it)."""
    return monthly.reindex(monthly.index.union(days)).ffill().reindex(days)
