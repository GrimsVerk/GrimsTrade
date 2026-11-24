"""uv run python research/lib/idea_wide5_dealer_backlog.py
(card: cards/dealer-backlog.md; needs `python -I research/lib/wide5_auctions.py` first)"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date

import common as c
import numpy as np
import wide1 as w
import wide5 as g
import wide5_rules as r

from grimstrade.data import Bar

IDEA = "dealer-backlog"
P_BAR = 0.10 / 56  # the list of 46 plus W1-W10 (cards/dealer-backlog.md)
BASE = date(2008, 7, 1)
HALVES = ("2008-07 to 2016", "2017 to end of train")
PERIODS = (
    ("all", BASE, c.TRAIN_END),
    (HALVES[0], BASE, date(2016, 12, 31)),
    (HALVES[1], date(2017, 1, 1), c.TRAIN_END),
)


def events(group: str) -> list[tuple[date, float]]:
    return [e for e in r.dealer_surprises(g.auctions(), group) if e[0] <= c.TRAIN_END]


def overlay(bond: str, group: str, positive: bool) -> c.ResearchStrategy:
    return g.overlay(bond, r.backlog_sessions(w.calendar(bond), events(group), positive))


def study(sym: str, bars: Sequence[Bar], group: str) -> tuple[list[str], dict[str, float]]:
    days = [b.date for b in bars]
    idx = {d: i for i, d in enumerate(days)}
    opens = np.array([b.open for b in bars])
    closes = np.array([b.close for b in bars])
    base_lo = next(i for i, d in enumerate(days) if d >= BASE)
    evs = [(d, u, idx[d]) for d, u in events(group) if d in idx and d >= BASE]
    fill = r.open_excess(opens, [i + 1 for _, _, i in evs], 5, base_lo)
    close = r.open_excess(closes, [i for _, _, i in evs], 5, base_lo)  # close A to close A+5
    a = [(d, u, u > 0, float(x)) for (d, u, _), x in zip(evs, fill, strict=True)]
    b = [(d, u, u > 0, float(x)) for (d, u, _), x in zip(evs, close, strict=True)]
    la, ga = g.study_rows(f"{sym}, fills", a, PERIODS, ("pos", "neg"))
    lb, _ = g.study_rows(f"{sym}, closes", b, PERIODS, ("pos", "neg"))
    us = np.array([u for _, u, _ in evs])
    ga["n"], ga["npos"], ga["u_sd"] = len(evs), int((us > 0).sum()), float(us.std())
    return [*la, *lb], ga


def main() -> None:
    out = ["# dealer-backlog: idle cash into the long bond after auctions dealers absorbed", ""]
    out += ["Card: `cards/dealer-backlog.md`. Protocol: `protocol.md`.", ""]
    six = c.ctx("six")
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "backlog", overlay("TLT", "long", True), six, "variant")
    plc = c.go(IDEA, "backlog-neg", overlay("TLT", "long", False), six, "robustness")
    runs = [run, plc, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin, "2000-09")

    out += ["## Event study (descriptive): five sessions after the auction", ""]
    out += ["Fills = open of A+1 to open of A+6; closes = close of A to close of A+5. Excess = "
            "log return minus the average 5-session log return of the same kind since "
            "2008-07-01, in bps (t). u = dealer share of competitive awards minus the median "
            "of the previous 12 auctions of the group, in points. Slope = bps per point of u "
            "(OLS, HC1 t). TLT on 20- and 30-year auctions, IEF on 10-year auctions.",
            ""]  # fmt: skip
    out += ["| Bond | Period | u > 0 | Excess (t) | u <= 0 | Excess (t) | Slope | t |",
            "|---|---|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    etf = c.ctx("etf")
    tl, tg = study("TLT", six.hist["TLT"], "long")
    il, _ = study("IEF", etf.hist["IEF"], "ten")
    out += [*tl, *il, ""]
    out += [f"Long auctions since 2008-07 (TLT sessions): {tg['n']:.0f}, of which "
            f"{tg['npos']:.0f} with u > 0; standard deviation of u {tg['u_sd']:.1f} points.",
            ""]  # fmt: skip
    ok, text = g.reading(tg, HALVES, "pos", "neg")
    out += [f"Card's reading for TLT at our fills: {text}", ""]

    out += ["## Out of universe: the 8 other ETFs, overlay into IEF after 10-year auctions", ""]
    t_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    a_e = c.go(IDEA, "backlog", overlay("IEF", "ten", True), etf, "robustness")
    out += [c.table([a_e, t_e], t_e, eras=False), ""]
    sign_e = w.versus(a_e, t_e)["diff"]

    dv, dt, de, dp = c.describe(run), c.describe(twin), c.describe(ew), c.describe(plc)
    d = vs["diff"]
    bars = [
        (f"1. `backlog` beats twin `tsmom12` with p < {P_BAR:.5f} (0.10 / 56)",
         d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in at least 3 of {vs['eras']:.0f} eras (from 2000-09)",
         vs["ahead"] >= 3, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and positive on the ETF set", d > 0 and sign_e > 0, f"etf {sign_e:+.3f}"),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) Beats its placebo `backlog-neg` on Sharpe", dv["sharpe"] > dp["sharpe"],
         f"{dv['sharpe']:.3f} vs {dp['sharpe']:.3f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `backlog`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
