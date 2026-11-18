"""Part A, post-hoc sample (NOT on the card): starts that look like 2026-11-17.

Defined 2026-11-18 after Part C showed that the S&P 500 is 6% below its 2026-10-06 high, at its
200-day average, with VIX 25: a fresh correction in a high-CAPE market, not the card's `late`
state (which needs the index within 5% of its high). Same 12 strategies, same windows as
bt_window.py; logged as `robustness` because the sample was chosen after seeing today's data.

`now-like`: lagged CAPE at or above the 90th percentile of its history, index 4-12% below its
all-time high, that high set within the last 63 trading days, 24-month return at least +15%.
`now-like-vix`: also VIX close at or above 20 (1990 on).

Usage: bt_window_now.py <out_dir> [--log]   (reads window-<index>.csv.gz from bt_window.py)
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_data as d  # noqa: E402
import bt_window as bw  # noqa: E402


def now_like(px: pd.Series, cape: pd.Series, vix: pd.Series) -> tuple[pd.Series, pd.Series]:
    days = px.index
    pct = d.asof_daily(d.expanding_pct(cape), days)
    ath = px.cummax()
    dd = px / ath - 1
    k = np.arange(len(px))
    last_ath = pd.Series(np.where(px.to_numpy() >= ath.to_numpy(), k, np.nan), index=days).ffill()
    fresh = (k - last_ath) <= 63
    run = px / px.shift(504) - 1 >= 0.15
    m = (pct >= 0.90) & (dd <= -0.04) & (dd >= -0.12) & fresh & run
    v = vix.reindex(days)
    return m, m & (v >= 20)


def main() -> None:
    out = Path(sys.argv[1])
    log = "--log" in sys.argv
    vix = d.vix()
    cape = d.cape_lagged()
    cape = cape[cape.index <= d.TRAIN_END]
    tables, logrows = [], []
    for name, sym in [("GSPC", "^GSPC"), ("IXIC", "^IXIC")]:
        px = d.yahoo(sym)
        px = px[px.index <= d.TRAIN_END]
        df = pd.read_csv(out / f"window-{name}.csv.gz", index_col=0, parse_dates=True)
        m1, m2 = now_like(px, cape, vix)
        for mname, m in [("now-like", m1), ("now-like-vix", m2)]:
            t = bw.summarize(df, m, mname)
            t.insert(0, "index", name)
            sel = m.reindex(df.index).fillna(False).astype(bool)
            t["spells"] = bw.episodes_of(sel)
            tables.append(t)
            sub = df[sel]
            spells = sub.index.to_series().diff().dt.days.fillna(999) > 30
            print(name, mname, "spell starts:", [x.date().isoformat() for x in sub.index[spells]])
            for s in bw.STRATS:
                x = sub[s].dropna()
                if len(x) == 0:
                    continue
                logrows.append(
                    (
                        "exit-window",
                        f"{s}@{name} {mname} (post hoc sample; mean R-1; MaxDD col = worst R)",
                        "robustness",
                        str(x.index[0].date()),
                        str(x.index[-1].date()),
                        float(x.mean()),
                        float(x.min()),
                    )
                )
    res = pd.concat(tables, ignore_index=True)
    res.to_csv(out / "window-now-like.csv", index=False)
    fmt = res.copy()
    for c in ["mean", "median", "p05", "p95"]:
        fmt[c] = (fmt[c] * 100).round(2)
    for c in ["P<-5%", "P<-10%", "P>0"]:
        fmt[c] = (fmt[c] * 100).round(1)
    pd.set_option("display.width", 200)
    print(fmt.to_string(index=False))
    if log:
        bw.log_rows(logrows)


if __name__ == "__main__":
    main()
