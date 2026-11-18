"""uv run --with numpy python research/lib/idea_wide1_auction.py
(card: cards/auction-concession.md; needs `wide1_auctions.py` to have been run once)"""

from __future__ import annotations

import math
from datetime import date

import common as c
import timing
import wide1 as w

IDEA = "auction-concession"
SPLIT = date(2013, 1, 1)  # the paper (data to 2008) was published in 2013
GROUP = {"TLT": "long", "IEF": "mid"}


def gated(sym: str) -> c.ResearchStrategy:
    """The weekly `tsmom12` book, with `sym`'s slot empty while an announced auction is 1-5
    sessions ahead (decided daily)."""
    base = c.weekly(c.slots(c.tsmom_signal))

    def f(view: c.View) -> c.Weights:
        held = base(view)
        if sym in held and w.auction_out(view, sym, GROUP[sym]):
            return {s: x for s, x in held.items() if s != sym}
        return held

    return f


def in_signal(view: c.View, sym: str) -> bool:
    return not w.auction_out(view, sym, GROUP[sym])


def main() -> None:
    out = ["# auction-concession: step aside while dealers make room for a Treasury auction", ""]
    out += ["Card: `cards/auction-concession.md`. Protocol: `protocol.md`.", ""]
    n_long = sum(1 for _, a in w.auctions("long") if date(2003, 8, 1) <= a <= c.TRAIN_END)
    n_mid = sum(1 for _, a in w.auctions("mid") if date(2003, 8, 1) <= a <= c.TRAIN_END)
    out += [
        f"Auctions from 2003-08 to the end of train: {n_long} of 20/30-year bonds (TLT), "
        f"{n_mid} of 7/10-year notes (IEF).",
        "",
    ]

    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline",
                log=False)  # fmt: skip
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    v = c.go(IDEA, "six", gated("TLT"), six, "variant")
    out += ["## `six`: the six live assets, train period", "", c.table([v, twin, ew], twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table([v, twin, ew]), ""]
    main_vs = w.versus(v, twin, "2000-09")
    post_six = w.since(v, twin, SPLIT)
    out += [f"Sharpe difference to `tsmom12` from {SPLIT}: {post_six:+.2f}.", ""]

    out += ["# `tlt`: TLT alone, held except in the five sessions ending with the auction", ""]
    tlt = timing.one(IDEA, "tlt", in_signal, "TLT", "variant", SPLIT)
    out += tlt["text"]
    out += [
        'Read: "days held" are the sessions outside the auction window, "days not held" the '
        "five sessions ending with an auction day.",
        "",
    ]

    out += ["# Out of universe: the 8 other ETFs, IEF gated by 7- and 10-year auctions", ""]
    etf = c.ctx("etf")
    twin_e = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), etf, "baseline",
                  log=False)  # fmt: skip
    ve = c.go(IDEA, "six", gated("IEF"), etf, "robustness")
    out += [c.table([ve, twin_e], twin_e), ""]
    etf_vs = w.versus(ve, twin_e)
    ief = timing.one(IDEA, "tlt", in_signal, "IEF", "robustness", SPLIT)
    out += ief["text"]

    dv, dt, de = c.describe(v), c.describe(twin), c.describe(ew)
    d = main_vs["diff"]
    bars = [
        ("1. `six` beats twin `tsmom12` with p < 0.10", d > 0 and main_vs["p"] < 0.10,
         f"difference {d:+.3f}, p = {main_vs['p']:.2f}"),
        (f"2. Ahead of the twin in at least 3 of {main_vs['eras']:.0f} eras (from 2000-09)",
         main_vs["ahead"] >= 3, f"{main_vs['ahead']:.0f} of {main_vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Same sign out of universe: the ETF-set book and IEF alone",
         d > 0 and etf_vs["diff"] > 0 and ief["diff"] > 0,
         f"ETF set {etf_vs['diff']:+.3f} (p = {etf_vs['p']:.2f}), IEF alone {ief['diff']:+.2f} "
         f"(p = {ief['p']:.2f})"),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) `tlt` beats its `constant` twin with p < 0.10",
         tlt["diff"] > 0 and tlt["p"] < 0.10, f"{tlt['diff']:+.2f}, p = {tlt['p']:.2f}"),
        (f"7. (card) From {SPLIT}: `six` not behind `tsmom12`, `tlt` not behind `constant`",
         post_six >= 0 and tlt["post"] >= 0, f"{post_six:+.3f}, {tlt['post']:+.2f}"),
    ]  # fmt: skip
    out += ["# Pass bar (primary variant `six`)", "", *w.bars_report(bars)]
    if not math.isnan(tlt["t"]):
        out += [f"Welch t of in-window against out-of-window days: TLT {tlt['t']:+.2f}, "
                f"IEF {ief['t']:+.2f} (positive = the days held earned more).", ""]  # fmt: skip
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
