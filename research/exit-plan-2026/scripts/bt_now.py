"""Part C of research/cards/exit-rules.md: where every indicator stands on the latest data.

Description only, no backtest. Rerun for the final refresh with ONE command from the repo root
(fetches the public Yahoo series into the scratch dir, then prints everything):

    uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_now.py \
        --fetch <scratch>/bt-dl

- <scratch>/bt-dl is a scratch dir outside the repo. The downloads are untrusted data, parsed as
  JSON only; never commit them.
- The cache root (CBOE VIX file, FRED Baa spread, Shiller CAPE) comes from BT_CACHE or
  GRIMSTRADE_DATA, else `cache_root` in the gitignored research/macro.local.json (copy the
  .example next to it).
- A US bar dated today (New York date) is dropped until 16:20 New York time, an Oslo bar dated
  today until 16:30 Oslo time: before then it is intraday, not a close. 16:20, not 16:10,
  because VIX and VIX3M close at 16:15 (review round 2); VIX is cut at the S&P's last bar.
  `--us-last YYYY-MM-DD`
  overrides the US cut (bars after that date are dropped).
- Without --fetch it reads BT_FRESH (an earlier download) or the 2026-11-12 cache.

Output: index table (incl. OSEBX/OBX), then per holding type its index's 200-day state and which
Part A sample its day-0 state matches, then VIX, credit, CAPE and the Part B rule states. The
monthly rules (`sma10m`, `tsmom12`) are printed as the decision in force (made at the last
completed month-end close) and, separately, as the live value if the month ended today.
"""

from __future__ import annotations

import os
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_data as d  # noqa: E402
import bt_rules as br  # noqa: E402
import bt_window as bw  # noqa: E402
import bt_window_now as bwn  # noqa: E402

FETCH = ["^GSPC", "^IXIC", "^VIX", "^VIX3M", "HYG", "LQD", "OSEBX.OL", "OBX.OL", "URTH"]
US_CLOSE = ("America/New_York", (16, 20))
OSLO_CLOSE = ("Europe/Oslo", (16, 30))
MONTHLY = ("sma10m", "tsmom12")

# holding type -> index that stands in for it (name, symbol, US calendar?)
HOLDINGS = [
    ("Oslo-listed shares or a Nordic fund", "OSEBX", "OSEBX.OL", False),
    ("  cross-check", "OBX", "OBX.OL", False),
    ("Global index fund", "S&P 500", "^GSPC", True),
    ("  cross-check (MSCI World ETF, USD)", "URTH", "URTH", True),
    ("US / tech stocks or tech fund", "Nasdaq Comp", "^IXIC", True),
]


def fetch(out: Path) -> None:
    """Public Yahoo chart endpoint, no key. Saved as files; read later as JSON only."""
    out.mkdir(parents=True, exist_ok=True)
    now = int(time.time())
    for sym in FETCH:
        enc = sym.replace("^", "%5E")
        url = (
            f"https://query1.finance.yahoo.com/v8/finance/chart/{enc}?period1=-1325635200"
            f"&period2={now}&interval=1d&includeAdjustedClose=true"
        )
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (research script)"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310 (fixed https host)
                (out / f"{sym}.json").write_bytes(r.read())
            print("fetched", sym)
        except OSError as e:
            print("FAILED", sym, type(e).__name__, e, "(an older file, if any, is used)")
        time.sleep(1)


def drop_open_bar(px: pd.Series, where: tuple[str, tuple[int, int]]) -> pd.Series:
    tz, close_hm = where
    now = pd.Timestamp.now(tz=tz)
    if len(px) and px.index[-1].date() == now.date() and (now.hour, now.minute) < close_hm:
        return px.iloc[:-1]
    return px


def load(sym: str, us: bool, us_last: pd.Timestamp | None) -> pd.Series:
    px = d.yahoo(sym)
    if us and us_last is not None:
        return px[px.index <= us_last]
    return drop_open_bar(px, US_CLOSE if us else OSLO_CLOSE)


def month_done(day: pd.Timestamp) -> bool:
    """True if `day` is the last weekday of its month (exchange holidays are not modelled)."""
    return day == day + pd.offsets.BMonthEnd(0)


def completed_month_ends(px: pd.Series) -> pd.Series:
    me = px.groupby([px.index.year, px.index.month]).tail(1)
    last = px.index[-1]
    if month_done(last):
        return me
    return me[me.index < last.replace(day=1)]


def index_reading(name: str, px: pd.Series) -> dict[str, object]:
    last_me = completed_month_ends(px)
    sma10m_done = last_me.iloc[-10:].mean()
    live_base = last_me.iloc[-9:] if not month_done(px.index[-1]) else last_me.iloc[-10:-1]
    sma10m_live = pd.concat([live_base, px.iloc[-1:]]).mean()
    ath = px.max()
    p = px.iloc[-1]
    return {
        "index": name,
        "date": px.index[-1].date(),
        "close": round(p, 2),
        "vs_sma50_%": round((p / px.iloc[-50:].mean() - 1) * 100, 2),
        "sma50": round(px.iloc[-50:].mean(), 2),
        "vs_sma200_%": round((p / px.iloc[-200:].mean() - 1) * 100, 2),
        "sma200": round(px.iloc[-200:].mean(), 2),
        "last_month_end": last_me.index[-1].date(),
        "month_end_vs_sma10m_%": round((last_me.iloc[-1] / sma10m_done - 1) * 100, 2),
        "live_vs_sma10m_%": round((p / sma10m_live - 1) * 100, 2),
        "sma10m_live": round(sma10m_live, 2),
        "dd_from_ath_%": round((p / ath - 1) * 100, 2),
        "ath_date": px.idxmax().date(),
        "ret_12m_%": round((p / px.asof(px.index[-1] - pd.DateOffset(years=1)) - 1) * 100, 2),
        "ret_24m_%": round((p / px.asof(px.index[-1] - pd.DateOffset(years=2)) - 1) * 100, 2),
        "high_since_20d": round(px.iloc[-20:].max(), 2),
    }


def holding_state(
    kind: str, name: str, px: pd.Series, vix: pd.Series, cape: pd.Series
) -> dict[str, object]:
    sma = px.rolling(200).mean()
    below = (px < sma).to_numpy()
    k = len(px) - 1
    switches = np.flatnonzero(below[1:] != below[:-1])
    last_cross = px.index[switches[-1] + 1].date() if len(switches) else None
    run = k - (switches[-1] + 1) + 1 if len(switches) else k + 1
    st = bw.states(px, vix, cape).iloc[-1]
    nl = bool(bwn.now_like(px, cape, vix)[0].iloc[-1])
    side = "below" if below[-1] else "above"
    if st["late"]:
        sample = f"late (card){'' if below[-1] else ' = late-above200 (post hoc cut)'}"
    elif nl:
        sample = f"now-like (post hoc) / now-like-{side}200 (post hoc cut)"
    elif st["runup"]:
        sample = "runup (card), CAPE not top 10%"
    else:
        sample = "none of late / runup / now-like"
    return {
        "holding type": kind,
        "index": name,
        "date": px.index[-1].date(),
        "close": round(px.iloc[-1], 2),
        "sma200": round(sma.iloc[-1], 2),
        "vs_sma200_%": round((px.iloc[-1] / sma.iloc[-1] - 1) * 100, 2),
        "200d side": side,
        "closes on this side": run,
        "last cross": last_cross,
        "from high %": round((px.iloc[-1] / px.max() - 1) * 100, 2),
        "24m (504d) %": round((px.iloc[-1] / px.iloc[-505] - 1) * 100, 1),
        "runup": bool(st["runup"]),
        "late": bool(st["late"]),
        "now-like": nl,
        "sample today": sample,
    }


def main() -> None:
    argv = sys.argv
    if "--fetch" in argv:
        dl = Path(argv[argv.index("--fetch") + 1]).expanduser()
        fetch(dl)
        os.environ["BT_FRESH"] = str(dl)
    us_last = pd.Timestamp(argv[argv.index("--us-last") + 1]) if "--us-last" in argv else None
    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", 40)
    pd.set_option("display.max_colwidth", 80)
    rows = []
    for sym, name, us in [
        ("^GSPC", "S&P 500", True),
        ("^IXIC", "Nasdaq Comp", True),
        ("OSEBX.OL", "OSEBX", False),
        ("OBX.OL", "OBX", False),
        ("URTH", "URTH", True),
    ]:
        try:
            rows.append(index_reading(name, load(sym, us, us_last)))
        except (OSError, KeyError, IndexError) as e:
            print("no data for", sym, type(e).__name__)
    print(pd.DataFrame(rows).T.to_string())

    us_end = load("^GSPC", True, us_last).index[-1]  # last complete US close
    vix = d.vix()
    vix = vix[vix.index <= us_end]
    cape = d.cape_lagged()
    print("\nHolding types: the index's 200-day state and the Part A sample it matches today")
    hs = []
    for kind, name, sym, us in HOLDINGS:
        try:
            hs.append(holding_state(kind, name, load(sym, us, us_last), vix, cape))
        except (OSError, KeyError, IndexError) as e:
            print("no data for", sym, type(e).__name__)
    print(pd.DataFrame(hs).T.to_string())
    print("(Oslo and URTH use the US CAPE for `late` / `now-like`.)")

    v3 = d.vix3m()
    v3 = v3[v3.index <= vix.index[-1]]
    print("\nVIX", vix.index[-1].date(), round(vix.iloc[-1], 2))
    print(
        "VIX 50d mean",
        round(vix.iloc[-50:].mean(), 2),
        "ratio",
        round(vix.iloc[-1] / vix.iloc[-50:].mean(), 3),
    )
    print(
        "VIX 20d max",
        round(vix.iloc[-20:].max(), 2),
        "1y pct rank",
        round((vix.iloc[-252:] < vix.iloc[-1]).mean(), 2),
    )
    print(
        "VIX3M",
        v3.index[-1].date(),
        round(v3.iloc[-1], 2),
        "VIX/VIX3M",
        round(vix.iloc[-1] / v3.iloc[-1], 3),
    )
    r = (vix / v3).dropna()
    print("VIX/VIX3M last 10:", {k.date().isoformat(): v for k, v in r.iloc[-10:].round(3).items()})
    hl = (load("HYG", True, us_last) / load("LQD", True, us_last)).dropna()
    print(
        "\nHYG/LQD",
        hl.index[-1].date(),
        round(hl.iloc[-1], 4),
        "vs 200d %",
        round((hl.iloc[-1] / hl.iloc[-200:].mean() - 1) * 100, 2),
        "vs 50d %",
        round((hl.iloc[-1] / hl.iloc[-50:].mean() - 1) * 100, 2),
    )
    baa = d.fred("BAA10Y")
    m20 = baa.rolling(20).mean()
    lo = m20.rolling("365D").min()
    print(
        "BAA10Y (cached; refresh FRED by hand)",
        baa.index[-1].date(),
        baa.iloc[-1],
        "20d mean",
        round(m20.iloc[-1], 3),
        "365d min of 20d mean",
        round(lo.iloc[-1], 3),
        "hostile at >",
        round(lo.iloc[-1] + 0.5, 3),
    )
    sh = d.shiller_monthly()
    cs = sh["cape_shiller"].dropna()
    print("\nCAPE (Shiller column, unlagged)", cs.index[-1].date(), round(cs.iloc[-1], 2))
    print(
        "  rank in history",
        round((cs.iloc[:-1] < cs.iloc[-1]).mean(), 4),
        "max",
        round(cs.max(), 2),
        cs.idxmax().date(),
    )
    print("CAPE lagged 3m (use date)", cape.index[-1].date(), round(cape.iloc[-1], 2))
    print("  expanding pct", round(d.expanding_pct(cape).iloc[-1], 4))

    print("\nPart B rule states on the latest data (True = invested):")
    for sym in ["^GSPC", "^IXIC"]:
        px = load(sym, True, us_last)
        sig = br.signals(px)
        me_day = completed_month_ends(px).index[-1]
        state = {k: bool(v.iloc[-1]) for k, v in sig.items() if k not in MONTHLY}
        for k in MONTHLY:
            state[f"{k} (in force, decided {me_day.date()})"] = bool(sig[k].loc[me_day])
            state[f"{k} (live, if the month ended {px.index[-1].date()})"] = bool(sig[k].iloc[-1])
        print(sym, px.index[-1].date(), state)
        dd = sig["dd8"]
        ch = np.flatnonzero(dd.astype(int).diff().fillna(0).to_numpy())
        print("  dd8 last change", dd.index[ch[-1]].date() if len(ch) else None)


if __name__ == "__main__":
    main()
