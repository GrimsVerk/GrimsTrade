"""uv run --with numpy python research/lib/idea_wide1_rebalance.py
(card: cards/rebalance-pressure.md)"""

from __future__ import annotations

import bisect
import math
from collections.abc import Sequence
from datetime import date

import common as c
import numpy as np
import wide1 as w
import wide1_rules as rules

IDEA = "rebalance-pressure"
THRESHOLD = 0.02
HALF = date(2014, 1, 1)
SIX = (("SPY", "QQQ"), ("TLT",), ("SPY",), ("TLT",))
ETF = (("IWM", "EFA", "EEM", "VNQ"), ("IEF", "LQD"), ("IWM", "EFA", "EEM", "VNQ"), ("IEF", "LQD"))


def gap(view: c.View, cal: Sequence[date], t: int, stocks: Sequence[str], bonds: Sequence[str]):
    """g at the close of M = T-5: mean month-to-date log return of the eligible `stocks` minus
    that of the eligible `bonds`. NaN if a side has none, or M is not yet closed."""
    refs = rules.month_refs(cal, t)
    if refs is None:
        return math.nan
    m, p = refs
    sides = []
    for group in (stocks, bonds):
        rets = []
        for s in group:
            if not c.eligible(view, s):
                continue
            a, b = w.close_on(view, s, cal[p]), w.close_on(view, s, cal[m])
            if not (math.isnan(a) or math.isnan(b)):
                rets.append(math.log(b / a))
        if not rets:
            return math.nan
        sides.append(sum(rets) / len(rets))
    return sides[0] - sides[1]


def rule(spec: tuple[Sequence[str], ...], rebound: bool) -> c.ResearchStrategy:
    stocks, bonds, g_stocks, g_bonds = spec
    cal = w.calendar(stocks[0])
    base = c.weekly(c.slots(c.tsmom_signal))

    def f(view: c.View) -> c.Weights:
        held = base(view)
        d = w.last_session(view, stocks[0])
        if d is None:
            return held
        i = bisect.bisect_left(cal, d)
        if i >= len(cal) or cal[i] != d:
            return held
        phase = rules.month_phase(cal, i)
        if phase is None or (phase[0] == "rebound" and not rebound):
            return held
        g = gap(view, cal, phase[1], g_stocks, g_bonds)
        if math.isnan(g) or abs(g) < THRESHOLD:
            return held
        leader, other = (stocks, bonds) if g > 0 else (bonds, stocks)
        if phase[0] == "pressure":
            return rules.tilt(held, leader, other)
        return rules.tilt(held, other, leader)

    return f


def events(hist, cal: Sequence[date], stocks: Sequence[str], bonds: Sequence[str],
           first: date, last: date) -> list[tuple[date, float, float, float]]:  # fmt: skip
    """(T, g, spread return over sessions T-4 .. T, spread return over T+1 .. T+3), spread =
    mean of `stocks` minus mean of `bonds`, open to open, for every month end in [first, last].
    g uses closes up to M = T-5 only; the returns come after it."""
    closes = {s: {b.date: b.close for b in hist[s]} for s in (*stocks, *bonds)}

    def side(group: Sequence[str], a: date, b: date, kind: str) -> float:
        xs = []
        for s in group:
            if kind == "close":
                if a in closes[s] and b in closes[s]:
                    xs.append(math.log(closes[s][b] / closes[s][a]))
            else:
                x = w.open_to_open(hist[s], a, b)
                if not math.isnan(x):
                    xs.append(x)
        return sum(xs) / len(xs) if xs else math.nan

    out = []
    for t in range(6, len(cal) - 5):
        if cal[t + 1].month == cal[t].month or not first <= cal[t] <= last:
            continue
        refs = rules.month_refs(cal, t)
        if refs is None:
            continue
        m, p = refs
        g = side(stocks, cal[p], cal[m], "close") - side(bonds, cal[p], cal[m], "close")
        press = side(stocks, cal[t - 4], cal[t + 1], "open") - side(
            bonds, cal[t - 4], cal[t + 1], "open"
        )
        reb = side(stocks, cal[t + 1], cal[t + 4], "open") - side(
            bonds, cal[t + 1], cal[t + 4], "open"
        )
        if not (math.isnan(g) or math.isnan(press) or math.isnan(reb)):
            out.append((cal[t], g, press, reb))
    return out


def study(ev: list[tuple[date, float, float, float]]) -> tuple[list[str], dict[str, float]]:
    """The event study of the card: signed spread returns for the months the rule acts in."""
    lines = [
        "| Period | Months | Acted (|g| >= 2%) | Pressure: bps per month, signed against g (t) | "
        "Rebound: bps, signed with g (t) | corr(g, window spread), all months |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    signed: dict[str, float] = {}
    spans = [
        ("2003-2013", date(2003, 1, 1), date(2013, 12, 31)),
        ("2014-2025", HALF, date(2025, 12, 31)),
        ("all", date(2003, 1, 1), date(2025, 12, 31)),
    ]
    for name, a, b in spans:
        sel = [e for e in ev if a <= e[0] <= b]
        act = [e for e in sel if abs(e[1]) >= THRESHOLD]
        if len(act) < 3:
            lines.append(f"| {name} | {len(sel)} | {len(act)} | - | - | - |")
            signed[name] = math.nan
            continue
        press = np.array([-math.copysign(1, e[1]) * e[2] for e in act])
        reb = np.array([math.copysign(1, e[1]) * e[3] for e in act])
        corr = float(np.corrcoef([e[1] for e in sel], [e[2] for e in sel])[0, 1])
        signed[name] = float(press.mean())
        lines.append(
            f"| {name} | {len(sel)} | {len(act)} | {press.mean() * 1e4:+.1f} "
            f"({w.tstat(press):+.2f}) | {reb.mean() * 1e4:+.1f} ({w.tstat(reb):+.2f}) | "
            f"{corr:+.2f} |"
        )
    return lines, signed


def main() -> None:
    out = ["# rebalance-pressure: lean against the month-end trades of balanced funds", ""]
    out += ["Card: `cards/rebalance-pressure.md`. Protocol: `protocol.md`.", ""]
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), six, "baseline",
                log=False)  # fmt: skip
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    me = c.go(IDEA, "me", rule(SIX, False), six, "variant")
    reb = c.go(IDEA, "me-rebound", rule(SIX, True), six, "variant")
    runs = [me, reb, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(me, twin, "2000-09")
    vs_reb = w.versus(reb, twin, "2000-09")
    acted = sum(1 for a, b in zip(me.decisions, twin.decisions, strict=True)
                if a.weights != b.weights)  # fmt: skip
    out += [f"Decision days on which `me` differs from `tsmom12`: {acted}.", ""]

    out += ["## Event study: SPY minus TLT, open to open, around month ends", ""]
    ev = events(six.hist, w.calendar("SPY"), ("SPY",), ("TLT",), date(2003, 8, 1), c.TRAIN_END)
    lines, signed = study(ev)
    out += [*lines, ""]
    out += [
        "Pressure window: bought at the open of T-4, sold at the open of T+1. Rebound window: "
        "open of T+1 to open of T+4. A positive number is the sign the card predicts.",
        "",
    ]

    out += ["## Out of universe: the 8 other ETFs (stocks IWM, EFA, EEM, VNQ; bonds IEF, LQD)", ""]
    etf = c.ctx("etf")
    twin_e = c.go("baselines", "tsmom12", c.weekly(c.slots(c.tsmom_signal)), etf, "baseline",
                  log=False)  # fmt: skip
    me_e = c.go(IDEA, "me", rule(ETF, False), etf, "robustness")
    out += [c.table([me_e, twin_e], twin_e), ""]
    vs_e = w.versus(me_e, twin_e)
    ev_e = events(etf.hist, w.calendar("IWM"), ETF[0], ETF[1], date(2003, 8, 1), c.TRAIN_END)
    lines_e, _ = study(ev_e)
    out += [*lines_e, ""]

    dv, dt, de = c.describe(me), c.describe(twin), c.describe(ew)
    d = vs["diff"]
    both = all(not math.isnan(signed[k]) and signed[k] > 0 for k in ("2003-2013", "2014-2025"))
    bars = [
        ("1. `me` beats twin `tsmom12` with p < 0.10", d > 0 and vs["p"] < 0.10,
         f"difference {d:+.3f}, p = {vs['p']:.2f}"),
        (f"2. Ahead of the twin in at least 3 of {vs['eras']:.0f} eras (from 2000-09)",
         vs["ahead"] >= 3, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Same sign on the one applicable out-of-universe set", d > 0 and vs_e["diff"] > 0,
         f"ETF set {vs_e['diff']:+.3f} (p = {vs_e['p']:.2f})"),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) Signed window spread positive in 2003-2013 and in 2014-2025", both,
         ", ".join(f"{k} {signed[k] * 1e4:+.1f} bps" for k in ("2003-2013", "2014-2025"))),
    ]  # fmt: skip
    out += ["## Pass bar (primary variant `me`)", "", *w.bars_report(bars)]
    out += [f"`me-rebound` against `tsmom12`: {vs_reb['diff']:+.3f} (p = {vs_reb['p']:.2f}), "
            f"ahead in {vs_reb['ahead']:.0f} of {vs_reb['eras']:.0f} eras.", ""]  # fmt: skip
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
