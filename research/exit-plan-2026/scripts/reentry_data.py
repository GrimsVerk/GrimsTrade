"""Loaders for the reentry lane (card `research/cards/reentry.md`).

Cache root: GRIMSTRADE_DATA or `research/macro.local.json` (see `research/lib/long_bond.py`).
Run with `uv run --with xlrd python research/exit-plan-2026/scripts/<script>.py`.
"""

from __future__ import annotations

import importlib
import json
import sys
import zipfile
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lib"))
from long_bond import cache_root  # noqa: E402

YAHOO_DAY = "2026-11-12"


def daily_close(symbol: str) -> pd.Series:
    """Daily closes from the cached Yahoo chart JSON, indexed by date."""
    path = cache_root() / "yahoo-1d" / YAHOO_DAY / f"{symbol}.json"
    res = json.loads(path.read_text())["chart"]["result"][0]
    ts = pd.to_datetime(res["timestamp"], unit="s", utc=True)
    off = res["meta"].get("gmtoffset", 0)
    idx = (ts + pd.Timedelta(seconds=off)).tz_localize(None).normalize()
    s = pd.Series(res["indicators"]["quote"][0]["close"], index=idx, dtype=float)
    s = s[~s.index.duplicated(keep="last")].dropna()
    return s[s > 0].sort_index()


def month_end(daily: pd.Series) -> pd.Series:
    """Last close of each calendar month, indexed by month period."""
    m = daily.groupby(daily.index.to_period("M")).last()
    return m


def shiller() -> pd.DataFrame:
    """Shiller monthly D, E, CPI (nominal), indexed by month period."""
    xlrd: Any = importlib.import_module("xlrd")
    path = cache_root() / "shiller" / "ie_data.xls"
    sheet = xlrd.open_workbook(str(path)).sheet_by_name("Data")
    rows = [sheet.row_values(i) for i in range(sheet.nrows)]
    start = next(i for i, r in enumerate(rows) if r and r[0] == "Date") + 1
    out = []
    for r in rows[start:]:
        if not isinstance(r[0], float):
            continue
        year = int(r[0])
        month = round((r[0] - year) * 100)

        def num(x: Any) -> float:
            return float(x) if isinstance(x, int | float) else np.nan

        out.append((pd.Period(year=year, month=month, freq="M"), num(r[2]), num(r[3]), num(r[4])))
    df = pd.DataFrame(out, columns=["month", "D", "E", "CPI"]).set_index("month")
    return df


def french_rf() -> pd.Series:
    """Monthly 1-month T-bill return (decimal) from Ken French, indexed by month period."""
    path = cache_root() / "french" / YAHOO_DAY / "F-F_Research_Data_Factors_CSV.zip"
    with zipfile.ZipFile(path) as z:
        text = z.read(z.namelist()[0]).decode("latin-1")
    lines = text.splitlines()
    start = next(i for i, ln in enumerate(lines) if ln.startswith(",Mkt-RF"))
    rows = []
    for ln in lines[start + 1 :]:
        parts = [p.strip() for p in ln.split(",")]
        if len(parts) < 5 or len(parts[0]) != 6 or not parts[0].isdigit():
            break
        rows.append(
            (
                pd.Period(year=int(parts[0][:4]), month=int(parts[0][4:]), freq="M"),
                float(parts[4]) / 100,
            )
        )
    return pd.Series(dict(rows)).sort_index()


def lagged_cape(close_m: pd.Series, sh: pd.DataFrame) -> pd.Series:
    """CAPE at month m: (C_m / CPI_{m-1}) / mean_{k=3..122}(E_{m-k} / CPI_{m-k}). Card rule."""
    real_e = sh["E"] / sh["CPI"]  # NaN for the latest months (not yet reported)
    e10 = real_e.rolling(120, min_periods=120).mean()  # mean of E_{s-119..s}
    e10_lag = e10.shift(3)  # at m: mean of E_{m-122..m-3}
    cpi_lag = sh["CPI"].shift(1)
    df = pd.DataFrame({"C": close_m}).join(e10_lag.rename("E10")).join(cpi_lag.rename("CPI1"))
    return (df["C"] / df["CPI1"]) / df["E10"]


def monthly_frame(symbol: str = "^GSPC", dividends: bool = True) -> pd.DataFrame:
    """Month-end close, running ATH of daily closes, total return, RF, lagged CAPE."""
    daily = daily_close(symbol)
    ath_daily = daily.cummax()
    df = pd.DataFrame({"C": month_end(daily), "ATH": month_end(ath_daily)})
    sh = shiller()
    rf = french_rf()
    df["RF"] = rf.reindex(df.index).ffill()
    if dividends:
        d = sh["D"].reindex(df.index).ffill()
        df["R"] = (df["C"] + d / 12) / df["C"].shift(1) - 1
    else:
        df["R"] = df["C"] / df["C"].shift(1) - 1
    gspc = month_end(daily_close("^GSPC"))
    df["CAPE"] = lagged_cape(gspc, sh).reindex(df.index)
    df["DD"] = df["C"] / df["ATH"] - 1
    df["SMA10"] = df["C"].rolling(10).mean()
    # first full month only (the first month has no previous close)
    return df.iloc[1:]


if __name__ == "__main__":
    f = monthly_frame()
    print(f.head(3).to_string())
    print(f.tail(3).to_string())
    print(f[["CAPE"]].dropna().describe().to_string())
