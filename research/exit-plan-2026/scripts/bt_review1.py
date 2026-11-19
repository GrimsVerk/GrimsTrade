"""Card amendment 2 (research/cards/exit-rules.md, review round 1): post-hoc 200-day splits.

Same Part A windows and strategies as bt_window.py / bt_amend.py (train period). New cuts by the
state on day 0, chosen after seeing today's readings, so every row is `robustness`:

- `now-like-below200` / `now-like-above200` (S&P 500, Nasdaq): `now-like` split by whether the
  day-0 close is below its 200-day average.
- `late-above200` (OSEBX, OBX): `late` with the day-0 close at or above its 200-day average.

Usage: bt_review1.py <out_dir> [--log]
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bt_amend as ba  # noqa: E402
import bt_data as d  # noqa: E402
import bt_window as bw  # noqa: E402
import bt_window_now as bwn  # noqa: E402

STRATS = ["now", "fallback", "staged-half", "staged-half-sma200"]
SETS = [("GSPC", "^GSPC"), ("IXIC", "^IXIC"), ("OSEBX", "OSEBX.OL"), ("OBX", "OBX.OL")]


def main() -> None:
    out = Path(sys.argv[1])
    out.mkdir(parents=True, exist_ok=True)
    vix = d.vix()
    cape = d.cape_lagged()
    cape = cape[cape.index <= d.TRAIN_END]
    tabs, logrows = [], []
    for name, sym in SETS:
        px = d.yahoo(sym)
        px = px[px.index <= d.TRAIN_END]
        a = bw.outcomes(px, vix)
        b = ba.outcomes_new(px)
        df = pd.concat(
            [a[["now", "fallback", "staged-half", "end_day"]], b[["staged-half-sma200"]]], axis=1
        )
        df = df[df["end_day"] <= d.TRAIN_END]
        below = px < px.rolling(200).mean()
        if name in ("GSPC", "IXIC"):
            nl, _ = bwn.now_like(px, cape, vix)
            cuts = {"now-like-below200": nl & below, "now-like-above200": nl & ~below}
        else:
            st = bw.states(px, vix, cape)
            cuts = {"late-above200": st["late"] & ~below}
        for cname, m in cuts.items():
            keep = bw.STRATS
            bw.STRATS = STRATS
            try:
                t = bw.summarize(df, m, cname)
            finally:
                bw.STRATS = keep
            t.insert(0, "index", name)
            sel = m.reindex(df.index).fillna(False).astype(bool)
            t["spells"] = bw.episodes_of(sel)
            tabs.append(t)
            sub = df[sel]
            for s in STRATS[1:]:
                x = sub[s].dropna()
                if len(x) == 0:
                    continue
                logrows.append(
                    (
                        "exit-window",
                        f"{s}@{name} {cname} "
                        "(post hoc review-1 cut; mean R-1; MaxDD col = worst R)",
                        "robustness",
                        str(x.index[0].date()),
                        str(x.index[-1].date()),
                        float(x.mean()),
                        float(x.min()),
                    )
                )
    res = pd.concat(tabs, ignore_index=True)
    res.to_csv(out / "review1-window.csv", index=False)
    fmt = res.copy()
    for c in ["mean", "median", "p05", "p95"]:
        fmt[c] = (fmt[c] * 100).round(2)
    for c in ["P<-5%", "P<-10%", "P>0"]:
        fmt[c] = (fmt[c] * 100).round(1)
    pd.set_option("display.width", 200)
    print(fmt.to_string(index=False))
    if "--log" in sys.argv:
        bw.log_rows(logrows)


if __name__ == "__main__":
    main()
