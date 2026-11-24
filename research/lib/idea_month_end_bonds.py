"""uv run --with numpy python research/lib/idea_month_end_bonds.py
(card: cards/month-end-bonds.md)

Train bars only: nothing after 2025-11-10 is loaded, not even dates. RESCORE=1 reruns without
logging (only after a crash in the reporting, for configurations already in tries.md)."""

from __future__ import annotations

import bisect
import math
import os
from collections.abc import Sequence
from datetime import date, timedelta

import common as c
import monthend_rules as rules
import numpy as np
import wide1 as w
from harness import TRAIN_END, Panel, load_history

from grimstrade.data import Bar

IDEA = "month-end-bonds"
SHARE = 0.19  # the twin's constant weight: four sessions in about 21
COST = 0.0004  # one round trip in an ETF at the gym's 2 bps a side
HALF = date(2014, 1, 1)
Y1_END = date(2003, 7, 30)  # the last bar no earlier test loaded
LOG = not os.environ.get("RESCORE")


def rule(sym: str, cal: Sequence[date]) -> c.ResearchStrategy:
    def f(view: c.View) -> c.Weights:
        d = w.last_session(view, sym)
        if d is None:
            return {}
        i = bisect.bisect_left(cal, d)
        if i >= len(cal) or cal[i] != d:
            return {}
        return {sym: 1.0} if rules.holds_after(cal, i) else {}

    return f


def own_ctx(name: str, sym: str, bars: list[Bar]) -> c.Ctx:
    """The asset alone from its first bar: no eligibility year (the card's exception)."""
    hist = {sym: bars}
    start = bars[0].date + timedelta(days=1)
    end = min(TRAIN_END, bars[-1].date - timedelta(days=1))
    return c.Ctx(name, "train", hist, Panel(hist), start, end)


def study(bars: Sequence[Bar], spans: Sequence[tuple[str, date, date]]) -> tuple[list[str], dict]:
    """Per span: the month-end window return at the gym's fills, gross, and net of cost and of
    four average sessions of the same span."""
    days = [b.date for b in bars]
    opens = [b.open for b in bars]
    sess = np.array([opens[i + 1] / opens[i] - 1 for i in range(len(opens) - 1)])
    ev = rules.window_returns(days, opens)
    lines = [
        "| Period | Months | Window, gross: bps (t) | Average session, bps | Net excess: bps (t) | "
        "Share of months up, gross |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    res: dict[str, tuple[float, float, int]] = {}
    for name, a, b in spans:
        x = np.array([r for d, r in ev if a <= d <= b])
        inside = np.array([a <= d <= b for d in days[:-1]])
        if len(x) < 3 or not inside.any():
            lines.append(f"| {name} | {len(x)} | - | - | - | - |")
            res[name] = (math.nan, math.nan, len(x))
            continue
        mean_day = float(sess[inside].mean())
        net = x - COST - 4 * mean_day
        res[name] = (float(net.mean()), w.tstat(net), len(x))
        lines.append(
            f"| {name} | {len(x)} | {x.mean() * 1e4:+.1f} ({w.tstat(x):+.2f}) | "
            f"{mean_day * 1e4:+.2f} | {net.mean() * 1e4:+.1f} ({w.tstat(net):+.2f}) | "
            f"{(x > 0).mean():.0%} |"
        )
    return lines, res


def main() -> None:
    hist = load_history("train", True, ["LQD", "TLT"])
    lqd, tlt = hist["LQD"], hist["TLT"]
    tlt_y1 = [b for b in tlt if b.date <= Y1_END]

    # the two runs of the card, then the twin and buy-and-hold of LQD
    cl = own_ctx("LQD", "LQD", lqd)
    ct = own_ctx("TLT-y1", "TLT", tlt_y1)
    run_l = c.go(IDEA, "last4", rule("LQD", [b.date for b in lqd]), cl, "variant", log=LOG)
    run_t = c.go(IDEA, "last4", rule("TLT", [b.date for b in tlt_y1]), ct, "variant", log=LOG)
    twin = c.go(IDEA, "constant", lambda view: {"LQD": SHARE}, cl, "baseline", log=LOG)
    hold = c.go(IDEA, "hold", lambda view: {"LQD": 1.0}, cl, "baseline", log=LOG)

    out = ["# month-end-bonds: hold the bond for the last four sessions of the month", ""]
    out += [
        "Card: `cards/month-end-bonds.md` (written before any number). Train bars only; the "
        "held-out year was not loaded. One run each of `last4@LQD` and `last4@TLT-y1`. Twin "
        f"`constant` holds LQD at a constant {SHARE:.0%}; `hold` is buy-and-hold.",
        "",
    ]
    out += [f"## LQD, {cl.start} to {cl.end} (gym: next-open fills, 2 bps a side)", ""]
    out += [c.table([run_l, twin, hold], twin), ""]
    first = lqd[0].date
    spans = [
        ("all", first, TRAIN_END),
        ("to 2013", first, HALF - timedelta(days=1)),
        ("from 2014", HALF, TRAIN_END),
        ("first year (to 2003-07-30)", first, Y1_END),
        ("2003-07-31 on", Y1_END + timedelta(days=1), TRAIN_END),
    ]
    out += ["## LQD: the window, month by month", ""]
    lines_l, res_l = study(lqd, spans)
    out += [*lines_l, ""]
    out += [
        "Window = bought at the open of T-3, sold at the open of T+1 (T = last session of the "
        "month). Net excess = window return minus 4 bps of cost minus four average sessions of "
        'the same period. "First year" is a row of the same run, not a separate try.',
        "",
    ]
    ev_l = dict(rules.window_returns([b.date for b in lqd], [b.open for b in lqd]))
    ev_t = dict(rules.window_returns([b.date for b in tlt], [b.open for b in tlt]))
    both = sorted(set(ev_l) & set(ev_t))
    corr = float(np.corrcoef([ev_l[d] for d in both], [ev_t[d] for d in both])[0, 1])
    out += [
        f"Correlation of LQD's window return with TLT's in the same {len(both)} months: "
        f"{corr:+.2f} (no bar; how much of the LQD result is the same Treasury move).",
        "",
    ]

    out += [f"## TLT, first year only (bars {tlt_y1[0].date} to {tlt_y1[-1].date})", ""]
    out += [c.table([run_t], eras=False), ""]
    lines_t, res_t = study(tlt_y1, [("first year", tlt_y1[0].date, Y1_END)])
    out += [*lines_t, ""]

    vs = w.versus(run_l, twin)
    dl, dh = c.describe(run_l), c.describe(hold)
    net, t, n = res_l["all"]
    h1, h2 = res_l["to 2013"][0], res_l["from 2014"][0]
    bars = [
        ("1. LQD: net excess over all months positive with t >= 2.0", net > 0 and t >= 2.0,
         f"{net * 1e4:+.1f} bps, t {t:+.2f}, {n} months"),
        ("2. LQD: net excess positive in both halves", h1 > 0 and h2 > 0,
         f"to 2013 {h1 * 1e4:+.1f} bps, from 2014 {h2 * 1e4:+.1f} bps"),
        ("3. LQD: gym Sharpe above the twin with p < 0.10", vs["diff"] > 0 and vs["p"] < 0.10,
         f"difference {vs['diff']:+.3f}, p = {vs['p']:.2f}"),
        ("4. LQD: gym Sharpe above buy-and-hold", dl["sharpe"] > dh["sharpe"],
         f"{dl['sharpe']:.2f} vs {dh['sharpe']:.2f}"),
    ]  # fmt: skip
    out += ["## Pass bar: `last4@LQD`", "", *w.bars_report(bars)]
    ty = res_t["first year"]
    out += [
        "## TLT's first year (can only fail to contradict)",
        "",
        f"- {'NOT CONTRADICTED' if ty[0] > 0 else 'CONTRADICTED'}: net excess "
        f"{ty[0] * 1e4:+.1f} bps a month (t {ty[1]:+.2f}, {ty[2]} months).",
        "",
    ]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
