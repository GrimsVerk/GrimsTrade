"""Descriptive bear-market statistics for the reentry lane (no rule is selected here).

Bear market = a fall of at least 20% from an all-time high in daily closes (price index, no
dividends). For each: peak, trough, depth, months peak->trough, trough->recovery of the old peak.
After the first close at -20%, -30%, -40%: forward 1/3/5-year price returns and how much further
it fell. Trend re-entry lag: first month-end close above the 10-month average and first daily
close above the 200-day average after the trough. VIX peak vs price trough (1990 on).

Run: GRIMSTRADE_DATA=... uv run --with xlrd --with pandas python <this file>
"""

from __future__ import annotations

import json

import pandas as pd
from reentry_data import cache_root, daily_close

LEVELS = (0.20, 0.30, 0.40)


def fred(series: str) -> pd.Series:
    path = cache_root() / "fred" / "api" / "latest" / series / "2026-11-12.json"
    obs = json.loads(path.read_text())["observations"]
    s = pd.Series(
        {pd.Timestamp(o["date"]): float(o["value"]) for o in obs if o["value"] not in (".", "")}
    )
    return s.sort_index()


# First cut of an easing cycle (FOMC announcement dates, federalreserve.gov history). The
# daily effective rate is too noisy before 2008 to find these mechanically.
FIRST_CUTS = ("1998-09-29", "2001-01-03", "2007-09-18", "2019-07-31", "2024-09-18")


def credit_peaks(s: pd.Series, eps: list[dict]) -> pd.DataFrame:
    """Baa-Treasury spread peak (1986 on), between equity peak and trough + 180 days."""
    spread = fred("BAA10Y")
    rows = []
    for ep in eps:
        p_day, t_day = s.index[ep["peak_i"]], s.index[ep["trough_i"]]
        if p_day < spread.index[0]:
            continue
        seg = spread[(spread.index >= p_day) & (spread.index <= t_day + pd.Timedelta(days=180))]
        rows.append(
            {
                "peak": ep["peak"],
                "trough": ep["trough"],
                "spread_max_date": seg.idxmax().date(),
                "spread_max": seg.max(),
                "days_spread_minus_trough": (seg.idxmax() - t_day).days,
                "px_at_spread_max_vs_trough": s[s.index <= seg.idxmax()].iloc[-1]
                / s.iloc[ep["trough_i"]]
                - 1,
            }
        )
    return pd.DataFrame(rows)


def after_first_cut(s: pd.Series) -> pd.DataFrame:
    """Worst close within 3 years after the first cut of each easing cycle, and when."""
    rows = []
    for d in FIRST_CUTS:
        day = pd.Timestamp(d)
        p0 = s[s.index <= day].iloc[-1]
        seg = s[(s.index > day) & (s.index <= day + pd.DateOffset(years=3))]
        rows.append(
            {
                "first_cut": d,
                "close": p0,
                "min_3y_date": seg.idxmin().date(),
                "min_3y_vs_cut": seg.min() / p0 - 1,
                "ret_1y": s[s.index >= day + pd.DateOffset(years=1)].iloc[0] / p0 - 1,
            }
        )
    return pd.DataFrame(rows)


def bears(s: pd.Series) -> list[dict]:
    ath = s.cummax()
    dd = s / ath - 1
    out = []
    i, n = 0, len(s)
    vals, idx = s.to_numpy(), s.index
    while i < n:
        if dd.iloc[i] > -0.20:
            i += 1
            continue
        peak_val = ath.iloc[i]
        peak_i = int((s.iloc[: i + 1] == peak_val).to_numpy().nonzero()[0][-1])
        j = i
        while j < n and vals[j] < peak_val:
            j += 1
        seg = s.iloc[peak_i:j]
        trough_i = peak_i + int(seg.to_numpy().argmin())
        ep = {
            "peak": idx[peak_i].date(),
            "trough": idx[trough_i].date(),
            "depth": vals[trough_i] / peak_val - 1,
            "m_down": (idx[trough_i] - idx[peak_i]).days / 30.44,
            "recovered": idx[j].date() if j < n else None,
            "m_up": (idx[j] - idx[trough_i]).days / 30.44 if j < n else None,
            "peak_i": peak_i,
            "trough_i": trough_i,
            "end_i": j,
        }
        out.append(ep)
        i = j
    return out


def forward(s: pd.Series, eps: list[dict]) -> pd.DataFrame:
    rows = []
    for ep in eps:
        peak_val = s.iloc[ep["peak_i"]]
        seg = s.iloc[ep["peak_i"] : ep["end_i"]]
        for lv in LEVELS:
            hit = seg[seg <= peak_val * (1 - lv)]
            if hit.empty:
                continue
            d0, v0 = hit.index[0], hit.iloc[0]
            row = {"peak": ep["peak"], "level": f"-{int(lv * 100)}%", "date": d0.date()}
            row["further_fall"] = s.iloc[ep["trough_i"]] / v0 - 1
            for yrs in (1, 3, 5):
                t = d0 + pd.DateOffset(years=yrs)
                after = s[s.index >= t]
                row[f"fwd{yrs}y"] = after.iloc[0] / v0 - 1 if not after.empty else None
            rows.append(row)
    return pd.DataFrame(rows)


def trend_lag(s: pd.Series, eps: list[dict]) -> pd.DataFrame:
    me = s.groupby(s.index.to_period("M")).last()
    me.index = s.groupby(s.index.to_period("M")).apply(lambda x: x.index[-1])
    sma10 = me.rolling(10).mean()
    sma200 = s.rolling(200).mean()
    rows = []
    for ep in eps:
        t_day, t_val = s.index[ep["trough_i"]], s.iloc[ep["trough_i"]]
        row = {"peak": ep["peak"], "trough": ep["trough"]}
        # false re-entries: month-end crosses back above the 10-month average between the
        # first -20% close and the trough (each would have bought before the bottom)
        p_day = s.index[ep["peak_i"]]
        first20 = s[(s.index >= p_day) & (s <= s.iloc[ep["peak_i"]] * 0.8)].index[0]
        above = (me > sma10)[(me.index >= first20) & (me.index <= t_day)]
        row["false_x"] = int((above & ~above.shift(1, fill_value=True)).sum())
        m_hit = me[(me.index > t_day) & (me > sma10)]
        if not m_hit.empty:
            row["sma10_date"] = m_hit.index[0].date()
            row["sma10_months"] = (m_hit.index[0] - t_day).days / 30.44
            row["sma10_above_low"] = m_hit.iloc[0] / t_val - 1
        d_hit = s[(s.index > t_day) & (s > sma200)]
        if not d_hit.empty:
            row["sma200_date"] = d_hit.index[0].date()
            row["sma200_months"] = (d_hit.index[0] - t_day).days / 30.44
            row["sma200_above_low"] = d_hit.iloc[0] / t_val - 1
        rows.append(row)
    return pd.DataFrame(rows)


def vix_vs_trough(s: pd.Series, eps: list[dict]) -> pd.DataFrame:
    vix = daily_close("^VIX")
    rows = []
    for ep in eps:
        a = s.index[ep["peak_i"]]
        b = s.index[ep["trough_i"]] + pd.Timedelta(days=90)
        if a < vix.index[0]:
            continue
        seg = vix[(vix.index >= a) & (vix.index <= b)]
        if seg.empty:
            continue
        vd = seg.idxmax()
        t_day = s.index[ep["trough_i"]]
        px_at_vix = s[s.index <= vd].iloc[-1]
        rows.append(
            {
                "peak": ep["peak"],
                "trough": ep["trough"],
                "vix_max_date": vd.date(),
                "vix_max": seg.max(),
                "days_vix_minus_trough": (vd - t_day).days,
                "px_at_vix_vs_trough": px_at_vix / s.iloc[ep["trough_i"]] - 1,
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    pd.set_option("display.width", 200)
    pd.set_option("display.float_format", lambda x: f"{x:.3f}")
    for sym in ("^GSPC", "^IXIC"):
        s = daily_close(sym)
        s = s[s.index <= "2026-11-11"]
        eps = bears(s)
        print(f"\n=== {sym} bear markets (>=20% from ATH, price only) {s.index[0].date()}..")
        cols = ["peak", "trough", "depth", "m_down", "recovered", "m_up"]
        print(pd.DataFrame(eps)[cols].to_string(index=False))
        fw = forward(s, eps)
        print(f"\n--- {sym} after first close at each drawdown level")
        print(fw.to_string(index=False))
        for lv, g in fw.groupby("level"):
            fwd = {k: g[k].dropna() for k in ("fwd1y", "fwd3y", "fwd5y")}
            print(
                f"{lv}: n={len(g)} median further fall {g['further_fall'].median():.3f}, "
                f"share falling >=10% more {(g['further_fall'] <= -0.10).mean():.2f}; "
                + ", ".join(
                    f"{k} median {v.median():.3f} share>0 {(v > 0).mean():.2f} (n={len(v)})"
                    for k, v in fwd.items()
                )
            )
        print(f"\n--- {sym} trend re-entry after the trough")
        tl = trend_lag(s, eps)
        print(tl.to_string(index=False))
        print(
            "median: sma10 months",
            f"{tl['sma10_months'].median():.1f}",
            "above low",
            f"{tl['sma10_above_low'].median():.3f}",
            "| sma200 months",
            f"{tl['sma200_months'].median():.1f}",
            "above low",
            f"{tl['sma200_above_low'].median():.3f}",
        )
        print(f"\n--- {sym} VIX peak vs price trough")
        print(vix_vs_trough(s, eps).to_string(index=False))
        print(f"\n--- {sym} Baa-10y spread peak vs the equity trough")
        print(credit_peaks(s, eps).to_string(index=False))
        print(f"\n--- {sym} after the first Fed cut of an easing cycle")
        print(after_first_cut(s).to_string(index=False))


if __name__ == "__main__":
    main()
