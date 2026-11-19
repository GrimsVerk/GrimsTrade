"""Markdown tables for lanes/bt.md from the CSVs in lanes/bt-data (no new runs)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "lanes" / "bt-data"
COLS = ["mean", "median", "p05", "p95", "P<-5%", "P<-10%", "P>0"]


def md(df: pd.DataFrame) -> str:
    head = "| " + " | ".join(df.columns) + " |"
    sep = "|" + "|".join("---" if i == 0 else "---:" for i in range(len(df.columns))) + "|"
    rows = ["| " + " | ".join(str(v) for v in r) + " |" for r in df.itertuples(index=False)]
    return "\n".join([head, sep, *rows])


def window(res: pd.DataFrame, index: str, sample: str) -> str:
    t = res[(res["index"] == index) & (res["sample"] == sample)].copy()
    for c in ["mean", "median", "p05", "p95"]:
        t[c] = (t[c] * 100).map(lambda x: f"{x:+.2f}")
    for c in ["P<-5%", "P<-10%", "P>0"]:
        t[c] = (t[c] * 100).map(lambda x: f"{x:.1f}")
    n = f"{int(t['n_days'].max())} start days, ~{t['n_eff'].max():.0f} independent windows, "
    n += f"{int(t['spells'].iloc[0])} separate spells"
    return f"**{index}, sample `{sample}`** ({n}); R-1 in %, P in % of start days\n\n" + md(
        t[["strategy", *COLS]]
    )


def main() -> None:
    res = pd.concat(
        [pd.read_csv(DATA / "window-summary.csv"), pd.read_csv(DATA / "window-now-like.csv")]
    )
    for idx, sample in [
        ("GSPC", "all"),
        ("GSPC", "late"),
        ("GSPC", "now-like"),
        ("GSPC", "crash-window"),
        ("IXIC", "late"),
        ("IXIC", "now-like"),
        ("OBX", "late"),
        ("OSEBX", "runup"),
    ]:
        print(window(res, idx, sample))
        print()
    # compact cross-sample view: p05 / median per strategy
    keep = [
        ("GSPC", "all"),
        ("GSPC", "all-1928-1989"),
        ("GSPC", "all-1990-2025"),
        ("GSPC", "cape-hi"),
        ("GSPC", "runup"),
        ("GSPC", "lowvix"),
        ("GSPC", "late"),
        ("GSPC", "late-1990-2025"),
        ("IXIC", "all"),
        ("OBX", "all"),
        ("OSEBX", "all"),
    ]
    rows = []
    for idx, s in keep:
        t = res[(res["index"] == idx) & (res["sample"] == s)].set_index("strategy")
        rows.append(
            {
                "index/sample": f"{idx} {s}",
                **{
                    k: f"{t.loc[k, 'p05'] * 100:+.1f} / {t.loc[k, 'median'] * 100:+.1f}"
                    for k in ["fallback", "staged5", "staged-half", "trig-sma50", "bracket"]
                    if k in t.index
                },
            }
        )
    print("p05 / median of R-1 (%) across samples\n")
    print(md(pd.DataFrame(rows)))
    print()

    full = pd.read_csv(DATA / "rules-full.csv")
    eps = pd.read_csv(DATA / "rules-episodes.csv")
    g = eps[eps["index"] == "GSPC"]
    av = g.pivot(index="rule", columns="episode", values="avoided")
    pt = g.pivot(index="rule", columns="episode", values="rule_peak_trough")
    lag = g.pivot(index="rule", columns="episode", values="lag_days")
    order = ["buyhold", "sma10m", "sma200d", "tsmom12", "dd8", "dd10", "vix30", "vixts", "baa"]
    order += ["hyglqd", "cape30", "capepct"]
    epcols = ["1929", "1937", "1973-74", "1987", "2000-02", "2007-09", "2020", "2022"]

    def fmt(tab: pd.DataFrame, f: str) -> pd.DataFrame:
        t = tab.reindex(order)[epcols]
        t = t.apply(lambda col: col.map(lambda x: "-" if pd.isna(x) else format(x, f)))
        return t.reset_index()

    falls = g[g["rule"] == "buyhold"].set_index("episode")
    hdr = ", ".join(
        f"{e}: {falls.loc[e, 'peak']} to {falls.loc[e, 'trough']} ({fall * 100:.0f}%)"
        for e in epcols
        for fall in [falls.loc[e, "fall"]]
    )
    print("Episodes (S&P 500 close, peak to trough): " + hdr + "\n")
    print("Return of the rule from the peak to the trough (buy-and-hold = the fall)\n")
    print(md(fmt(pt * 100, "+.0f")))
    print()
    print("Share of the fall avoided by the first exit ((exit - trough) / (peak - trough))\n")
    print(md(fmt(av, ".2f")))
    print()
    print("Lag of the first exit, trading days after the peak (negative = before)\n")
    print(md(fmt(lag, ".0f")))
    print()
    f = full.copy()
    for c in [
        "cagr",
        "bh_cagr",
        "maxdd",
        "in_mkt",
        "false_alarm",
        "normal_yr_diff",
        "whip_cost_avg",
    ]:
        f[c] = (f[c] * 100).map(lambda x: "-" if pd.isna(x) else f"{x:.1f}")
    f["sharpe"] = f["sharpe"].map(lambda x: f"{x:.2f}")
    f["trips_per_yr"] = f["trips_per_yr"].map(lambda x: f"{x:.2f}")
    keep_cols = ["index", "rule", "cagr", "maxdd", "sharpe", "in_mkt", "trips_per_yr", "whipsaws"]
    keep_cols += ["whip_cost_avg", "false_alarm", "normal_yr_diff"]
    print(
        "Full sample (GSPC 1927-12-30..2025-11-07, IXIC 1971-02-05..2025-11-07), % where relevant\n"
    )
    print(md(f[keep_cols]))
    ix = eps[eps["index"] == "IXIC"][["rule", "exit", "lag_days", "avoided", "rule_peak_trough"]]
    ix = ix.assign(
        avoided=ix["avoided"].map(lambda x: f"{x:.2f}"),
        rule_peak_trough=(ix["rule_peak_trough"] * 100).map(lambda x: f"{x:+.0f}"),
    )
    print("\nNasdaq 2000-03-10 .. 2002-10-09 (-78%)\n")
    print(md(ix))


if __name__ == "__main__":
    main()
