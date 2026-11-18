"""uv run --with numpy python research/lib/idea_wide3_hedge_regime.py
(card: cards/hedge-regime.md)"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date

import common as c
import harness
import numpy as np
import wide1 as w

IDEA = "hedge-regime"
WINDOW = 252
P_BAR = 0.10 / 46  # Bonferroni over wide-1's whole list of 46 mechanisms (wide-3.md, step 1)
SETS = {"six": (("TLT",), ("SPY", "QQQ")), "etf": (("IEF", "LQD"), ("IWM", "EFA", "EEM", "VNQ"))}


def order_parameter(view: c.View, bond: str, stocks: Sequence[str]) -> float:
    """Correlation of the bond's daily log returns with the equal mean of the eligible stocks'
    over the last 252 business-day grid rows. NaN if a side is missing anywhere in the window."""
    st = [s for s in stocks if s in view.syms and c.eligible(view, s)]
    if bond not in view.syms or not st or view.n_grid < WINDOW + 1:
        return math.nan
    lr = view.grid_logret(WINDOW)
    b = lr[:, view.syms.index(bond)]
    s = lr[:, [view.syms.index(x) for x in st]].mean(axis=1)
    if np.isnan(b).any() or np.isnan(s).any() or b.std() == 0 or s.std() == 0:
        return math.nan
    return float(np.corrcoef(b, s)[0, 1])


def hedge_rule(bonds: Sequence[str], stocks: Sequence[str]) -> c.ResearchStrategy:
    """`tsmom12`'s equal slots; a bond also holds its slot out of trend while rho < 0."""

    def f(view: c.View) -> c.Weights:
        live = c.live(view)
        out = {s: 1 / len(live) for s in live if c.tsmom_signal(view, s)}
        for b in bonds:
            if b in live and b not in out and order_parameter(view, b, stocks) < 0:
                out[b] = 1 / len(live)
        return out

    return f


def hedge(view: c.View) -> c.Weights:
    """The rule on the six assets (TLT against SPY and QQQ)."""
    return hedge_rule(*SETS["six"])(view)


def main() -> None:
    out = ["# hedge-regime: hold the long bond out of trend while it hedges stocks", ""]
    out += ["Card: `cards/hedge-regime.md`. Protocol: `protocol.md`.", ""]
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "hedge", c.weekly(hedge), six, "variant")
    runs = [run, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin, "2000-09")

    # the order parameter on Fridays, and the weeks the rule adds TLT
    fridays = [d.time.date() for d in run.decisions if d.time.date().weekday() == 4]
    rhos = []
    for d in fridays:
        v = six.panel.view(harness.decide_time(d))
        rhos.append((d, order_parameter(v, "TLT", ("SPY", "QQQ"))))
    known = [(d, r) for d, r in rhos if not math.isnan(r)]
    neg = sum(r < 0 for _, r in known)
    flips = sum((a[1] < 0) != (b[1] < 0) for a, b in zip(known, known[1:], strict=False))
    share = neg / len(known)
    out += [f"TLT's rho is defined on {len(known)} Fridays ({known[0][0]} on); below zero on "
            f"{neg} ({share:.0%}); the sign changes {flips} times (weekly).", ""]  # fmt: skip
    by_year: dict[int, list[float]] = {}
    for d, r in known:
        by_year.setdefault(d.year, []).append(r)
    out += ["| Year | mean rho | share of Fridays below zero |", "|---|---:|---:|"]
    for y, xs in sorted(by_year.items()):
        out.append(f"| {y} | {np.mean(xs):+.2f} | {np.mean([x < 0 for x in xs]):.0%} |")
    out.append("")
    tlt = {b.date: b.close for b in six.hist["TLT"]}
    tdays = sorted(tlt)
    added = []
    for a, b in zip(run.decisions, twin.decisions, strict=True):
        d = a.time.date()
        if d.weekday() == 4 and "TLT" in a.weights and "TLT" not in b.weights:
            added.append(d)
    rets = []
    for d in added:
        i = int(np.searchsorted([x.toordinal() for x in tdays], d.toordinal(), side="right")) - 1
        j = min(i + 5, len(tdays) - 1)
        if i >= 0 and j > i:
            rets.append(math.log(tlt[tdays[j]] / tlt[tdays[i]]))
    if rets:
        r = np.array(rets)
        out += [f"Fridays on which `hedge` holds TLT and the twin does not: {len(added)}. TLT over "
                f"the next five sessions (close to close): mean {r.mean() * 1e4:+.1f} bps a week, "
                f"t {w.tstat(r):+.2f}; sum {r.sum():+.1%} (log).", ""]  # fmt: skip

    out += ["## Out of universe: the 8 other ETFs (IEF, LQD against IWM, EFA, EEM, VNQ)", ""]
    etf = c.ctx("etf")
    twin_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    run_e = c.go(IDEA, "hedge", c.weekly(hedge_rule(*SETS["etf"])), etf, "robustness")
    out += [c.table([run_e, twin_e], twin_e, eras=False), ""]
    vs_e = w.versus(run_e, twin_e)

    dv, dt, de = c.describe(run), c.describe(twin), c.describe(ew)
    d = vs["diff"]
    bars = [
        (f"1. `hedge` beats twin `tsmom12` with p < {P_BAR:.4f} (0.10 / 46)",
         d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in at least 3 of {vs['eras']:.0f} eras (from 2000-09)",
         vs["ahead"] >= 3, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and positive on the one applicable out-of-universe set",
         d > 0 and vs_e["diff"] > 0, f"ETF set {vs_e['diff']:+.3f} (p = {vs_e['p']:.2f})"),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `hedge`)", "", *w.bars_report(bars)]
    out += [f"Difference since 2003-07-01 (TLT eligible): "
            f"{w.since(run, twin, date(2003, 7, 1)):+.3f}.", ""]  # fmt: skip
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
