"""Part A of research/cards/exit-rules.md: how to sell within ~28 trading days.

For every start day 0 (train period only), each strategy gives R = average sale price / P0.
Signals seen at close t are executed at close t+1; limits are booked at the limit price on the
first close at or above it. Fallback day F = 22, last day N = 28.

Usage: bt_window.py <out_dir> [--log]   (writes CSV tables; --log appends rows to tries.md)
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_data as d  # noqa: E402

F = 22
N = 28
TRIES = Path(__file__).resolve().parents[2] / "tries.md"

STRATS = [
    "now",
    "fallback",
    "staged5",
    "staged-half",
    "trig-sma200",
    "trig-sma50",
    "trig-trail5",
    "trig-trail8",
    "trig-vix",
    "limit3",
    "limit5",
    "bracket",
]


def first_true(mask: np.ndarray) -> np.ndarray:
    """Index of the first True per row, or -1."""
    any_ = mask.any(axis=1)
    idx = mask.argmax(axis=1)
    return np.where(any_, idx, -1)


def outcomes(px: pd.Series, vix: pd.Series | None) -> pd.DataFrame:
    """R - 1 for every strategy and start date whose window ends inside the series."""
    p = px.to_numpy()
    n = len(p)
    starts = np.arange(252, n - N)  # need 200d history for the SMA trigger
    # window matrix W[i, k] = close of day k after start i, k = 0..N
    W = np.stack([p[starts + k] for k in range(N + 1)], axis=1)
    p0 = W[:, [0]]
    rel = W / p0
    sma200 = px.rolling(200).mean().to_numpy()
    sma50 = px.rolling(50).mean().to_numpy()
    S200 = np.stack([sma200[starts + k] for k in range(F)], axis=1)
    S50 = np.stack([sma50[starts + k] for k in range(F)], axis=1)
    rows = np.arange(len(starts))

    def trig_sale(fire_day: np.ndarray) -> np.ndarray:
        # fired at close of day t (0..F-1) -> sold at close t+1 (<= F); else at day F
        day = np.where(fire_day >= 0, fire_day + 1, F)
        return rel[rows, day]

    out: dict[str, np.ndarray] = {}
    out["now"] = np.ones(len(starts))
    out["fallback"] = rel[:, F]
    out["staged5"] = rel[:, [0, 5, 10, 15, 20]].mean(axis=1)
    out["staged-half"] = 0.5 * (rel[:, 0] + rel[:, F])
    out["trig-sma200"] = trig_sale(first_true(W[:, :F] < S200))
    out["trig-sma50"] = trig_sale(first_true(W[:, :F] < S50))
    runmax = np.maximum.accumulate(W[:, :F], axis=1)
    out["trig-trail5"] = trig_sale(first_true(W[:, :F] <= 0.95 * runmax))
    out["trig-trail8"] = trig_sale(first_true(W[:, :F] <= 0.92 * runmax))
    if vix is not None:
        v = vix.reindex(px.index).ffill()
        ratio = (v / v.rolling(50).mean()).to_numpy()
        V = np.stack([ratio[starts + k] for k in range(F)], axis=1)
        r = trig_sale(first_true(np.nan_to_num(V, nan=0.0) > 1.3))
        r[np.isnan(V[:, 0])] = np.nan
        out["trig-vix"] = r
    else:
        out["trig-vix"] = np.full(len(starts), np.nan)

    def limit(lim: float, stop: float | None) -> np.ndarray:
        hit = first_true(rel[:, 1 : F + 1] >= lim)  # days 1..F
        hit = np.where(hit >= 0, hit + 1, -1)
        res = np.where(hit >= 0, lim, rel[:, F])
        if stop is None:
            return res
        fire = first_true(W[:, :F] <= stop * runmax)
        sday = np.where(fire >= 0, fire + 1, 10**6)
        lday = np.where(hit >= 0, hit, 10**6)
        stop_first = (sday < lday) & (sday <= F)
        return np.where(stop_first, rel[rows, np.minimum(sday, F)], res)

    out["limit3"] = limit(1.03, None)
    out["limit5"] = limit(1.05, None)
    out["bracket"] = limit(1.03, 0.95)
    df = pd.DataFrame(out, index=px.index[starts]) - 1.0
    df["min_fwd"] = rel[:, 1:].min(axis=1) - 1.0
    df["end_day"] = px.index[starts + N]
    return df


def states(px: pd.Series, vix: pd.Series | None, cape: pd.Series) -> pd.DataFrame:
    days = px.index
    c = d.asof_daily(cape, days)
    # expanding percentile of the monthly lagged CAPE, as known on each day
    pct = d.asof_daily(d.expanding_pct(cape), days)
    ath = px.cummax()
    near = px >= 0.95 * ath
    run = px / px.shift(504) - 1 >= 0.25
    st = pd.DataFrame(index=days)
    st["cape"] = c
    st["cape-hi"] = pct >= 0.90
    st["runup"] = near & run
    if vix is not None:
        v = vix.reindex(days)
        st["lowvix"] = v < 16
    else:
        st["lowvix"] = False
    st["late"] = st["cape-hi"] & st["runup"]
    return st


def summarize(df: pd.DataFrame, mask: pd.Series, name: str) -> pd.DataFrame:
    sub = df[mask.reindex(df.index).fillna(False).astype(bool)]
    rows = []
    for s in STRATS:
        x = sub[s].dropna().to_numpy()
        if len(x) == 0:
            continue
        rows.append(
            {
                "sample": name,
                "strategy": s,
                "n_days": len(x),
                "n_eff": round(len(x) / N, 1),
                "mean": x.mean(),
                "median": np.median(x),
                "p05": np.quantile(x, 0.05),
                "p95": np.quantile(x, 0.95),
                "P<-5%": (x < -0.05).mean(),
                "P<-10%": (x < -0.10).mean(),
                "P>0": (x > 0).mean(),
            }
        )
    return pd.DataFrame(rows)


def episodes_of(mask: pd.Series, gap: int = 21) -> int:
    """Number of separate spells (runs of True, gaps under `gap` days merged)."""
    idx = np.flatnonzero(mask.to_numpy())
    if len(idx) == 0:
        return 0
    return int(1 + (np.diff(idx) > gap).sum())


def log_rows(rows: list[tuple[str, str, str, str, str, float, float]]) -> None:
    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    with TRIES.open("a") as f:
        for idea, var, kind, a, b, mean, worst in rows:
            f.write(
                f"| {now} | {idea} | {var} | {kind} | train | {a} | {b} | n/a | "
                f"{mean * 100:+.2f}% | {-worst * 100:.1f}% | n/a |\n"
            )


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    log = "--log" in sys.argv
    vix = d.vix()
    cape = d.cape_lagged()
    cape = cape[cape.index <= d.TRAIN_END]
    sets = {
        "GSPC": d.yahoo("^GSPC"),
        "IXIC": d.yahoo("^IXIC"),
        "OSEBX": d.yahoo("OSEBX.OL"),
        "OBX": d.yahoo("OBX.OL"),
    }
    tables = []
    logrows = []
    for name, px in sets.items():
        px = px[px.index <= d.TRAIN_END]
        df = outcomes(px, vix)
        df = df[df["end_day"] <= d.TRAIN_END]
        st = states(px, vix, cape)
        crash = df["min_fwd"] <= -0.10
        masks = {
            "all": pd.Series(True, index=df.index),
            "cape-hi": st["cape-hi"],
            "runup": st["runup"],
            "lowvix": st["lowvix"],
            "late": st["late"],
            "crash-window": crash,
        }
        if name == "GSPC":
            masks["all-1928-1989"] = pd.Series(df.index.year < 1990, index=df.index)
            masks["all-1990-2025"] = pd.Series(df.index.year >= 1990, index=df.index)
            masks["late-1990-2025"] = st["late"] & pd.Series(st.index.year >= 1990, st.index)
        for mname, m in masks.items():
            t = summarize(df, m, mname)
            t.insert(0, "index", name)
            sel = m.reindex(df.index).fillna(False).astype(bool)
            t["spells"] = episodes_of(sel)
            tables.append(t)
        b = df.index[-1].date()
        for s in STRATS:
            x = df[s].dropna()
            if len(x) == 0:
                continue
            kind = "variant" if name == "GSPC" else "robustness"
            kind = "baseline" if s == "now" else kind
            logrows.append(
                (
                    "exit-window",
                    f"{s}@{name} (mean R-1 all starts; MaxDD col = worst R)",
                    kind,
                    str(x.index[0].date()),
                    str(b),
                    float(x.mean()),
                    float(x.min()),
                )
            )
        df.to_csv(out / f"window-{name}.csv.gz")
    res = pd.concat(tables, ignore_index=True)
    res.to_csv(out / "window-summary.csv", index=False)
    pd.set_option("display.width", 200)
    pd.set_option("display.max_rows", 500)
    fmt = res.copy()
    for c in ["mean", "median", "p05", "p95"]:
        fmt[c] = (fmt[c] * 100).round(2)
    for c in ["P<-5%", "P<-10%", "P>0"]:
        fmt[c] = (fmt[c] * 100).round(1)
    print(fmt.to_string(index=False))
    if log:
        log_rows(logrows)


if __name__ == "__main__":
    main()
