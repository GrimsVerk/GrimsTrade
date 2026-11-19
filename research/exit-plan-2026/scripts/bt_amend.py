"""The 2026-11-18 card amendment (research/cards/exit-rules.md): lit-lane tests.

Part A: staged3, staged5-sma200, staged-half-sma200. Part B: sma200d-b2, sma200d-c2, kl3m10, rv2,
sma200d-rv, plus all Part B rules on OBX/OSEBX and an added 2018 Q4 episode. Screen: GSY flags
for US tech (French HiTec). Train period only for tests.

Usage: bt_amend.py <out_dir> [--log]
"""

from __future__ import annotations

import io
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_data as d  # noqa: E402
import bt_rules as br  # noqa: E402
import bt_window as bw  # noqa: E402
import bt_window_now as bwn  # noqa: E402

F = bw.F
N = bw.N
NEW_A = ["staged3", "staged5-sma200", "staged-half-sma200"]
NEW_B = ["sma200d-b2", "sma200d-c2", "kl3m10", "rv2", "sma200d-rv"]
SETS = [("GSPC", "^GSPC"), ("IXIC", "^IXIC"), ("OBX", "OBX.OL"), ("OSEBX", "OSEBX.OL")]
EXTRA_EP = {"2018Q4": ("2018-09-01", "2018-12-31")}


# ---------------- Part A ----------------
def outcomes_new(px: pd.Series) -> pd.DataFrame:
    p = px.to_numpy()
    n = len(p)
    starts = np.arange(252, n - N)
    W = np.stack([p[starts + k] for k in range(N + 1)], axis=1)
    rel = W / W[:, [0]]
    sma = px.rolling(200).mean().to_numpy()
    S = np.stack([sma[starts + k] for k in range(F)], axis=1)
    fire = bw.first_true(W[:, :F] < S)
    rows = np.arange(len(starts))
    sale = np.where(fire >= 0, fire + 1, F)
    out = {"staged3": rel[:, [0, 11, 22]].mean(axis=1)}
    tr = np.array([0, 5, 10, 15, 20])
    parts = []
    for t in tr:
        sold_at = np.where((fire >= 0) & (t > fire), fire + 1, t)
        parts.append(rel[rows, sold_at])
    out["staged5-sma200"] = np.mean(parts, axis=0)
    out["staged-half-sma200"] = 0.5 * rel[:, 0] + 0.5 * rel[rows, sale]
    df = pd.DataFrame(out, index=px.index[starts]) - 1.0
    df["min_fwd"] = rel[:, 1:].min(axis=1) - 1.0
    df["end_day"] = px.index[starts + N]
    return df


def summarize(df: pd.DataFrame, mask: pd.Series, name: str) -> pd.DataFrame:
    keep = bw.STRATS
    bw.STRATS = NEW_A
    try:
        return bw.summarize(df, mask, name)
    finally:
        bw.STRATS = keep


def part_a(out: Path, logrows: list) -> pd.DataFrame:
    vix = d.vix()
    cape = d.cape_lagged()
    cape = cape[cape.index <= d.TRAIN_END]
    tabs = []
    for name, sym in SETS:
        px = d.yahoo(sym)
        px = px[px.index <= d.TRAIN_END]
        df = outcomes_new(px)
        df = df[df["end_day"] <= d.TRAIN_END]
        st = bw.states(px, vix, cape)
        nl, _ = bwn.now_like(px, cape, vix)
        masks = {
            "all": pd.Series(True, index=df.index),
            "late": st["late"],
            "runup": st["runup"],
            "now-like": nl,
            "crash-window": df["min_fwd"] <= -0.10,
        }
        for mname, m in masks.items():
            t = summarize(df, m, mname)
            t.insert(0, "index", name)
            tabs.append(t)
        for s in NEW_A:
            x = df[s].dropna()
            kind = "variant" if name == "GSPC" else "robustness"
            logrows.append(
                (
                    "exit-window",
                    f"{s}@{name} (amendment; mean R-1 all starts; MaxDD col = worst R)",
                    kind,
                    str(x.index[0].date()),
                    str(x.index[-1].date()),
                    "n/a",
                    float(x.mean()),
                    -float(x.min()),
                    "n/a",
                )
            )
    res = pd.concat(tabs, ignore_index=True)
    res.to_csv(out / "amend-window.csv", index=False)
    return res


# ---------------- Part B ----------------
def consec(cond: pd.Series, k: int) -> pd.Series:
    return cond.astype(int).rolling(k).sum() >= k


def new_signals(px: pd.Series) -> dict[str, pd.Series]:
    sma = px.rolling(200).mean()
    lr = np.log(px).diff()
    rv = lr.rolling(21).std() * np.sqrt(252)
    med = rv.rolling(252).median()
    r63 = px / px.shift(63) - 1
    s: dict[str, pd.Series] = {}
    s["sma200d-b2"] = br.hysteresis(px < 0.98 * sma, px > sma)
    s["sma200d-c2"] = br.hysteresis(consec(px < sma, 2), consec(px > sma, 2))
    s["kl3m10"] = br.hysteresis(r63 < -0.10, r63 > 0)
    s["rv2"] = br.hysteresis(rv > 2 * med, rv < 1.25 * med)
    s["sma200d-rv"] = br.hysteresis((px < sma) & (rv > 1.5 * med), px > sma)
    return s


def part_b(out: Path, logrows: list) -> tuple[pd.DataFrame, pd.DataFrame]:
    ep_years = {y for a, b in br.EPISODES.values() for y in range(int(a[:4]), int(b[:4]) + 1)}
    full_rows, ep_rows = [], []
    for name, sym in SETS:
        px = d.yahoo(sym)
        px = px[px.index <= d.TRAIN_END]
        sig = new_signals(px)
        oslo = name in ("OBX", "OSEBX")
        if oslo:
            sig = {**br.signals(px), **sig, "buyhold": pd.Series(True, index=px.index)}
        rules = (["buyhold", *br.RULES] if oslo else []) + NEW_B
        eps = {**br.EPISODES, **EXTRA_EP}
        for rule in rules:
            df = br.run(px, sig[rule])
            tr = br.trades(df)
            fs = br.full_stats(df, tr, ep_years)
            full_rows.append({"index": name, "rule": rule, **fs})
            for ep, (a, b) in eps.items():
                if pd.Timestamp(a) < px.index[0] + pd.Timedelta(days=300):
                    continue
                ep_rows.append(
                    {"index": name, "rule": rule, "episode": ep, **br.episode_stats(df, tr, a, b)}
                )
            if rule == "buyhold":
                kind = "baseline"
            elif name == "GSPC" and rule in NEW_B:
                kind = "variant"
            else:
                kind = "robustness"
            logrows.append(
                (
                    "exit-rules",
                    f"{rule}@{name} (amendment; index, cash 0, trade next close)",
                    kind,
                    str(px.index[0].date()),
                    str(px.index[-1].date()),
                    f"{fs['sharpe']:.2f}",
                    float((1 + df["sr"]).prod() - 1),
                    float(fs["maxdd"]),
                    f"{2 * fs['trips_per_yr']:.2f}",
                )
            )
    # the 2018 Q4 episode for the original rules on the S&P and Nasdaq (robustness)
    for name, sym in [("GSPC", "^GSPC"), ("IXIC", "^IXIC")]:
        px = d.yahoo(sym)
        px = px[px.index <= d.TRAIN_END]
        sig = br.signals(px)
        sig["buyhold"] = pd.Series(True, index=px.index)
        for rule in ["buyhold", *br.RULES]:
            df = br.run(px, sig[rule])
            tr = br.trades(df)
            a, b = EXTRA_EP["2018Q4"]
            ep_rows.append(
                {"index": name, "rule": rule, "episode": "2018Q4", **br.episode_stats(df, tr, a, b)}
            )
    full = pd.DataFrame(full_rows)
    eps_df = pd.DataFrame(ep_rows)
    full.to_csv(out / "amend-rules-full.csv", index=False)
    eps_df.to_csv(out / "amend-rules-episodes.csv", index=False)
    return full, eps_df


# ---------------- GSY screen ----------------
def french_daily(fname: str, col: str) -> pd.Series:
    z = zipfile.ZipFile(d.cache() / "french" / "2026-11-12" / fname)
    text = z.read(z.namelist()[0]).decode("latin1").splitlines()
    head = next(i for i, ln in enumerate(text) if ln.startswith(","))
    rows = []
    for ln in text[head + 1 :]:
        if not ln.strip() or not ln.strip()[:8].isdigit():
            break
        rows.append(ln)
    df = pd.read_csv(io.StringIO("\n".join([text[head], *rows])), index_col=0)
    df.index = pd.to_datetime(df.index.astype(str), format="%Y%m%d")
    df.columns = [c.strip() for c in df.columns]
    return df[col] / 100.0


def gsy() -> tuple[pd.DataFrame, list[str]]:
    hi = french_daily("10_Industry_Portfolios_daily_CSV.zip", "HiTec")
    mkt = french_daily("F-F_Research_Data_Factors_daily_CSV.zip", "Mkt-RF") + french_daily(
        "F-F_Research_Data_Factors_daily_CSV.zip", "RF"
    )
    hm = (1 + hi).groupby(pd.Grouper(freq="ME")).prod()
    mm = (1 + mkt).groupby(pd.Grouper(freq="ME")).prod()
    lh, lm = np.log(hm), np.log(mm)
    r24 = np.exp(lh.rolling(24).sum()) - 1
    r24m = np.exp(lm.rolling(24).sum()) - 1
    r12_old = np.exp(lh.shift(12).rolling(12).sum()) - 1
    accel = r24 - r12_old
    vol = hi.rolling(63).std() * np.sqrt(252)
    volm = vol.groupby(pd.Grouper(freq="ME")).last()
    dvol = volm - volm.shift(12)
    tab = pd.DataFrame(
        {
            "r24": r24,
            "r24_net": r24 - r24m,
            "accel": accel,
            "dvol_1y": dvol,
            "vol63": volm,
        }
    )
    flag_months = tab.index[tab["r24"] >= 1.0]
    spells, prev = [], None
    for m in flag_months:
        if prev is None or (m - prev).days > 62:
            spells.append(m.strftime("%Y-%m"))
        else:
            spells[-1] = spells[-1].split("..")[0] + ".." + m.strftime("%Y-%m")
        prev = m
    return tab, spells


def log(rows: list) -> None:
    from datetime import UTC, datetime  # noqa: PLC0415

    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
    with bw.TRIES.open("a") as f:
        for idea, var, kind, a, b, sh, ret, mdd, turn in rows:
            f.write(
                f"| {now} | {idea} | {var} | {kind} | train | {a} | {b} | {sh} | "
                f"{ret * 100:+.2f}% | {mdd * 100:.1f}% | {turn} |\n"
            )


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    logrows: list = []
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 500)
    pd.set_option("display.max_columns", 30)
    a = part_a(out, logrows)
    fa = a.copy()
    for c in ["mean", "median", "p05", "p95"]:
        fa[c] = (fa[c] * 100).round(2)
    for c in ["P<-5%", "P<-10%", "P>0"]:
        fa[c] = (fa[c] * 100).round(1)
    print(fa.to_string(index=False))
    full, eps = part_b(out, logrows)
    print(full.round(3).to_string(index=False))
    print(eps.round(3).to_string(index=False))
    tab, spells = gsy()
    print("\nGSY HiTec (French, value-weighted), last 6 months:")
    print(tab.tail(6).round(3).to_string())
    print("Months with 2-year HiTec return >= 100%:", spells)
    print("Max r24:", round(tab["r24"].max(), 3), tab["r24"].idxmax().date())
    if "--log" in sys.argv:
        log(logrows)


if __name__ == "__main__":
    main()
