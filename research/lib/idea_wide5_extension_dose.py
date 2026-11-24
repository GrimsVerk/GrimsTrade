"""uv run python research/lib/idea_wide5_extension_dose.py
(card: cards/extension-dose.md; needs `python -I research/lib/wide5_auctions.py` first)"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import date

import common as c
import numpy as np
import wide1 as w
import wide5 as g
import wide5_rules as r

from grimstrade.data import Bar

IDEA = "extension-dose"
P_BAR = 0.10 / 56  # the list of 46 plus W1-W10 (cards/extension-dose.md)
FIRST = date(2002, 7, 30)  # TLT's first day
HALVES = ("2002-07 to 2013", "2014 to end of train")
PERIODS = (
    ("all", FIRST, c.TRAIN_END),
    (HALVES[0], FIRST, date(2013, 12, 31)),
    (HALVES[1], date(2014, 1, 1), c.TRAIN_END),
)
BUCKETS = {"TLT": (20.0, 99.0), "IEF": (7.0, 10.05)}

_series: dict[str, tuple[list[date], dict[int, float], dict[int, bool]]] = {}


def series(bond: str) -> tuple[list[date], dict[int, float], dict[int, bool]]:
    """E(m) on the exchange calendar (SPY's sessions) from 1994, and the rule's classes."""
    if bond not in _series:
        cal = w.calendar("SPY")
        lo, hi = BUCKETS[bond]
        ds = r.month_end_doses(cal, g.auctions(), lo, hi, date(1994, 1, 1), c.TRAIN_END)
        _series[bond] = (cal, ds, r.classify(ds))
    return _series[bond]


def overlay(bond: str, high: bool) -> c.ResearchStrategy:
    cal, _, cls = series(bond)
    return g.overlay(bond, r.ext_sessions(cal, cls, high))


def study(sym: str, bars: Sequence[Bar]) -> tuple[list[str], dict[str, float]]:
    cal, ds, cls = series(sym)
    days = [b.date for b in bars]
    idx = {d: i for i, d in enumerate(days)}
    opens = np.array([b.open for b in bars])
    evs = [(cal[j], ds[j], cls[j], idx[cal[j]]) for j in sorted(cls)
           if cal[j] in idx and cal[j] >= FIRST and idx[cal[j]] >= 3]  # fmt: skip
    ex = r.open_excess(opens, [i - 3 for *_, i in evs], 4, 0)
    rows = [(d, e, h, float(x)) for (d, e, h, _), x in zip(evs, ex, strict=True)]
    lines, got = g.study_rows(sym, rows, PERIODS, ("high", "low"))
    es = np.array([e for _, e, _, _ in evs])
    got["n"], got["nhigh"] = len(evs), sum(h for _, _, h, _ in evs)
    got["e_med"], got["e_sd"] = float(np.median(es)), float(es.std())
    got["e_lo"], got["e_hi"] = float(es.min()), float(es.max())
    return lines, got


def main() -> None:
    out = ["# extension-dose: the month-end bond window only when the index extends a lot", ""]
    out += ["Card: `cards/extension-dose.md`. Protocol: `protocol.md`.", ""]
    six = c.ctx("six")
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "ext-high", overlay("TLT", True), six, "variant")
    plc = c.go(IDEA, "ext-low", overlay("TLT", False), six, "robustness")
    runs = [run, plc, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin, "2000-09")

    out += ["## Event study (descriptive): open of T-3 to open of T+1", ""]
    out += ["Excess = log return minus the average 4-session open-to-open log return since "
            "2002-07-30, in bps (t). High = E(m) above the median of the previous 24 months "
            "(the rule's months). Slope = bps per year of extension (OLS, HC1 t). TLT against "
            "the 20+ year bucket, IEF against the 7-10 year bucket.", ""]  # fmt: skip
    out += ["| Bond | Period | High months | Excess (t) | Low months | Excess (t) | Slope | t |",
            "|---|---|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    etf = c.ctx("etf")
    tl, tg = study("TLT", six.hist["TLT"])
    il, ig = study("IEF", etf.hist["IEF"])
    out += [*tl, *il, ""]
    for name, x in (("TLT, 20+", tg), ("IEF, 7-10", ig)):
        out += [f"- {name}: {x['n']:.0f} month ends, {x['nhigh']:.0f} high; E(m) median "
                f"{x['e_med']:+.3f} years, standard deviation {x['e_sd']:.3f}, range "
                f"{x['e_lo']:+.3f} to {x['e_hi']:+.3f}."]  # fmt: skip
    out += [""]
    ok, text = g.reading(tg, HALVES, "high", "low")
    out += [f"Card's reading for TLT at our fills: {text}", ""]

    out += ["## Out of universe: the 8 other ETFs, overlay into IEF by the 7-10 bucket", ""]
    t_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    a_e = c.go(IDEA, "ext-high", overlay("IEF", True), etf, "robustness")
    out += [c.table([a_e, t_e], t_e, eras=False), ""]
    sign_e = w.versus(a_e, t_e)["diff"]

    dv, dt, de, dp = c.describe(run), c.describe(twin), c.describe(ew), c.describe(plc)
    d = vs["diff"]
    bars = [
        (f"1. `ext-high` beats twin `tsmom12` with p < {P_BAR:.5f} (0.10 / 56; biased up by "
         "the seen month-end mean)", d > 0 and vs["p"] < P_BAR,
         f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in at least 3 of {vs['eras']:.0f} eras (from 2000-09)",
         vs["ahead"] >= 3, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and positive on the ETF set", d > 0 and sign_e > 0, f"etf {sign_e:+.3f}"),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) Beats its placebo `ext-low` on Sharpe", dv["sharpe"] > dp["sharpe"],
         f"{dv['sharpe']:.3f} vs {dp['sharpe']:.3f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `ext-high`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
