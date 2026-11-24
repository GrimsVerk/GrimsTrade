"""Part B of research/cards/exit-rules.md: classic exit rules on crash episodes.

Long the index or cash (cash earns 0). A rule's state is decided at the close of day t and
traded at the close of day t+1, so the position held over day t+2's return is the state of day t.
Inputs that do not exist yet (before 1990 for VIX, etc.) leave the rule invested.

Usage: bt_rules.py <out_dir> [--log]
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_data as d  # noqa: E402

TRIES = Path(__file__).resolve().parents[2] / "tries.md"

EPISODES = {
    "1929": ("1929-01-01", "1932-12-31"),
    "1937": ("1937-01-01", "1938-12-31"),
    "1973-74": ("1972-06-01", "1974-12-31"),
    "1987": ("1987-06-01", "1987-12-31"),
    "2000-02": ("2000-01-01", "2002-12-31"),
    "2007-09": ("2007-06-01", "2009-06-30"),
    "2020": ("2020-01-01", "2020-06-30"),
    "2022": ("2021-11-01", "2022-12-31"),
}
RULES = [
    "sma10m",
    "sma200d",
    "tsmom12",
    "dd8",
    "dd10",
    "vix30",
    "vixts",
    "baa",
    "hyglqd",
    "cape30",
    "capepct",
]


def month_end_flags(px: pd.Series, cond_m: pd.Series) -> pd.Series:
    """Monthly decision (at the last close of each month) held on every day until the next."""
    return cond_m.reindex(px.index).ffill().fillna(1.0).astype(bool)


def hysteresis(out_cond: pd.Series, in_cond: pd.Series) -> pd.Series:
    """In by default; go out when out_cond, come back when in_cond."""
    o = out_cond.fillna(False).to_numpy()
    i = in_cond.fillna(True).to_numpy()
    state = np.ones(len(o), dtype=bool)
    cur = True
    for k in range(len(o)):
        if cur and o[k]:
            cur = False
        elif not cur and i[k]:
            cur = True
        state[k] = cur
    return pd.Series(state, index=out_cond.index)


def dd_stop(px: pd.Series, stop: float) -> pd.Series:
    """Out when the close is `stop` below the highest close since the later of 252 days ago and
    the last re-entry; back in when the close is above its 50-day average."""
    p = px.to_numpy()
    sma50 = px.rolling(50).mean().to_numpy()
    state = np.ones(len(p), dtype=bool)
    cur, anchor = True, 0
    for k in range(len(p)):
        if cur:
            lo = max(anchor, k - 251)
            peak = p[lo : k + 1].max()
            if p[k] <= (1 - stop) * peak:
                cur = False
        elif not np.isnan(sma50[k]) and p[k] > sma50[k]:
            cur, anchor = True, k
        state[k] = cur
    return pd.Series(state, index=px.index)


def signals(px: pd.Series) -> dict[str, pd.Series]:
    days = px.index
    me = px.groupby([days.year, days.month]).tail(1)
    sig: dict[str, pd.Series] = {}
    sig["sma10m"] = month_end_flags(
        px, (me >= me.rolling(10).mean()).where(me.rolling(10).count() == 10)
    )
    sig["sma200d"] = (px >= px.rolling(200).mean()) | px.rolling(200).mean().isna()
    sig["tsmom12"] = month_end_flags(px, (me >= me.shift(12)).where(me.shift(12).notna()))
    sig["dd8"] = dd_stop(px, 0.08)
    sig["dd10"] = dd_stop(px, 0.10)
    vix = d.vix().reindex(days)
    sig["vix30"] = hysteresis(vix > 30, vix < 20)
    ratio = (d.vix() / d.vix3m()).dropna().reindex(days)
    sig["vixts"] = hysteresis(ratio > 1.0, ratio < 0.9)
    baa = d.fred("BAA10Y")
    m20 = baa.rolling(20).mean()
    lo = m20.rolling("365D").min()
    hostile = (m20 > lo + 0.5).where(m20.notna())
    hostile.index = hostile.index + pd.Timedelta(days=1)  # public the day after
    h = hostile.reindex(hostile.index.union(days)).ffill().reindex(days)
    sig["baa"] = ~(h.fillna(0.0).astype(bool))
    try:
        hl = (d.yahoo("HYG") / d.yahoo("LQD")).dropna()
        ok = (hl >= hl.rolling(200).mean()).where(hl.rolling(200).count() == 200)
        sig["hyglqd"] = ok.reindex(days).fillna(1.0).astype(bool)
    except FileNotFoundError:
        sig["hyglqd"] = pd.Series(True, index=days)
    cape = d.cape_lagged()
    c = d.asof_daily(cape, days)
    sig["cape30"] = ~(c > 30)
    pct = d.asof_daily(d.expanding_pct(cape), days)
    sig["capepct"] = ~(pct >= 0.95)
    return {k: v.reindex(days).fillna(True).astype(bool) for k, v in sig.items()}


def run(px: pd.Series, state: pd.Series) -> pd.DataFrame:
    """Daily strategy returns; held[t] = state[t-2] (decide t, trade close t+1)."""
    r = px.pct_change().fillna(0.0)
    held = state.shift(2).fillna(True).astype(float)
    df = pd.DataFrame({"px": px, "r": r, "held": held, "state": state})
    df["sr"] = df["held"] * df["r"]
    return df


def trades(df: pd.DataFrame) -> pd.DataFrame:
    """Round trips: exit executed at close t+1 after state turns False at t; re-entry likewise."""
    st = df["state"].astype(int)
    ch = st.diff().fillna(0)
    px = df["px"].to_numpy()
    idx = df.index
    exits = np.flatnonzero(ch.to_numpy() == -1)
    entries = np.flatnonzero(ch.to_numpy() == 1)
    cols = ["exit_date", "exit_px", "entry_date", "entry_px", "cost", "false_alarm"]
    rows = []
    for e in exits:
        if e + 1 >= len(px):
            continue
        ex_k = e + 1
        nxt = entries[entries > e]
        en_k = nxt[0] + 1 if len(nxt) and nxt[0] + 1 < len(px) else None
        ex_p = px[ex_k]
        en_p = px[en_k] if en_k is not None else np.nan
        low = px[ex_k : (en_k if en_k is not None else len(px))].min()
        rows.append(
            {
                "exit_date": idx[ex_k],
                "exit_px": ex_p,
                "entry_date": idx[en_k] if en_k is not None else pd.NaT,
                "entry_px": en_p,
                "cost": en_p / ex_p - 1 if en_k is not None else np.nan,
                "false_alarm": low > 0.90 * ex_p,
            }
        )
    return pd.DataFrame(rows, columns=cols)


def sharpe_cal(df: pd.DataFrame) -> float:
    eq = (1 + df["sr"]).cumprod()
    cal = eq.reindex(pd.date_range(eq.index[0], eq.index[-1], freq="D")).ffill()
    r = cal.pct_change().dropna()
    return float(r.mean() / r.std() * np.sqrt(365)) if r.std() > 0 else np.nan


def full_stats(df: pd.DataFrame, tr: pd.DataFrame, ep_years: set[int]) -> dict[str, float]:
    years = (df.index[-1] - df.index[0]).days / 365.25
    eq = (1 + df["sr"]).cumprod()
    bh = (1 + df["r"]).cumprod()
    dd = 1 - eq / eq.cummax()
    yr = df.groupby(df.index.year).apply(lambda g: (1 + g["sr"]).prod() - (1 + g["r"]).prod())
    normal = yr[~yr.index.isin(list(ep_years))]
    closed = tr.dropna(subset=["cost"])
    whip = closed[closed["cost"] > 0]
    return {
        "cagr": eq.iloc[-1] ** (1 / years) - 1,
        "bh_cagr": bh.iloc[-1] ** (1 / years) - 1,
        "maxdd": dd.max(),
        "bh_maxdd": (1 - bh / bh.cummax()).max(),
        "sharpe": sharpe_cal(df),
        "in_mkt": df["held"].mean(),
        "trips_per_yr": len(tr) / years,
        "n_exits": len(tr),
        "whipsaws": len(whip),
        "whip_cost_avg": whip["cost"].mean() if len(whip) else np.nan,
        "false_alarm": tr["false_alarm"].mean() if len(tr) else np.nan,
        "normal_yr_diff": normal.mean(),
        "normal_years": len(normal),
    }


def episode_stats(df: pd.DataFrame, tr: pd.DataFrame, a: str, b: str) -> dict[str, object]:
    w = df.loc[a:b, "px"]
    peak_d = w.idxmax()
    trough_d = w.loc[peak_d:].idxmin()
    P, T = w[peak_d], w[trough_d]
    k_peak = df.index.get_loc(peak_d)
    k_trough = df.index.get_loc(trough_d)
    held_at_peak = bool(df["held"].iloc[k_peak + 1]) if k_peak + 1 < len(df) else True
    ex = tr[(tr["exit_date"] >= df.index[max(0, k_peak - 60)]) & (tr["exit_date"] <= trough_d)]
    prev = tr[tr["exit_date"] <= peak_d]
    if not held_at_peak and len(prev):
        e_date, e_px = prev["exit_date"].iloc[-1], prev["exit_px"].iloc[-1]
    elif len(ex):
        e_date, e_px = ex["exit_date"].iloc[0], ex["exit_px"].iloc[0]
    else:
        e_date, e_px = pd.NaT, np.nan
    if pd.isna(e_date):
        lag, avoided = np.nan, 0.0
    else:
        lag = df.index.get_loc(e_date) - k_peak
        avoided = (e_px - T) / (P - T)
    seg = df.iloc[k_peak + 1 : k_trough + 1]
    rule_pt = (1 + seg["sr"]).prod() - 1
    k_after = min(len(df) - 1, k_trough + 252)
    seg2 = df.iloc[k_peak + 1 : k_after + 1]
    return {
        "peak": peak_d.date(),
        "trough": trough_d.date(),
        "fall": T / P - 1,
        "exit": e_date.date() if not pd.isna(e_date) else None,
        "lag_days": lag,
        "avoided": avoided,
        "rule_peak_trough": rule_pt,
        "rule_peak_trough+1y": (1 + seg2["sr"]).prod() - 1,
        "bh_peak_trough+1y": (1 + seg2["r"]).prod() - 1,
    }


def log_rows(rows: list[tuple[str, str, str, str, str, float, float, float, float]]) -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    with TRIES.open("a") as f:
        for idea, var, kind, a, b, sh, ret, mdd, turn in rows:
            f.write(
                f"| {now} | {idea} | {var} | {kind} | train | {a} | {b} | {sh:.2f} | "
                f"{ret * 100:+.1f}% | {mdd * 100:.1f}% | {turn:.2f} |\n"
            )


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    log = "--log" in sys.argv
    ep_years = {y for a, b in EPISODES.values() for y in range(int(a[:4]), int(b[:4]) + 1)}
    full_rows, ep_rows, logrows = [], [], []
    for name in ["GSPC", "IXIC"]:
        px = d.yahoo("^" + name)
        px = px[px.index <= d.TRAIN_END]
        sig = signals(px)
        sig["buyhold"] = pd.Series(True, index=px.index)
        eps = EPISODES if name == "GSPC" else {"2000-02": EPISODES["2000-02"]}
        for rule in ["buyhold", *RULES]:
            df = run(px, sig[rule])
            tr = trades(df)
            fs = full_stats(df, tr, ep_years)
            full_rows.append({"index": name, "rule": rule, **fs})
            for ep, (a, b) in eps.items():
                if pd.Timestamp(a) < px.index[0]:
                    continue
                ep_rows.append(
                    {"index": name, "rule": rule, "episode": ep, **episode_stats(df, tr, a, b)}
                )
            kind = (
                "baseline" if rule == "buyhold" else ("variant" if name == "GSPC" else "robustness")
            )
            tot = (1 + df["sr"]).prod() - 1
            logrows.append(
                (
                    "exit-rules",
                    f"{rule}@{name} (index, cash 0, trade next close)",
                    kind,
                    str(px.index[0].date()),
                    str(px.index[-1].date()),
                    fs["sharpe"],
                    tot,
                    fs["maxdd"],
                    2 * fs["trips_per_yr"],
                )
            )
            if rule != "buyhold":
                tr.to_csv(out / f"trades-{name}-{rule}.csv", index=False)
    full = pd.DataFrame(full_rows)
    eps_df = pd.DataFrame(ep_rows)
    full.to_csv(out / "rules-full.csv", index=False)
    eps_df.to_csv(out / "rules-episodes.csv", index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 30)
    print(full.round(3).to_string(index=False))
    print(eps_df.round(3).to_string(index=False))
    if log:
        log_rows(logrows)


if __name__ == "__main__":
    main()
