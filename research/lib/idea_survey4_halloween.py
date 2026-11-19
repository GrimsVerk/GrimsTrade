"""uv run python research/lib/idea_survey4_halloween.py   (card: cards/halloween.md)

Halloween indicator (Bouman and Jacobsen, AER 2002; Andrade, Chhaochharia, Fuerst, FAJ 2013;
Zhang and Jacobsen, JIMF 2021): the stock slots are held only in weeks that start in November
to April."""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date, timedelta

import cash_interest
import common as c
import harness
import numpy as np
import stats
import survey4_rules as r
import wide1 as w

from grimstrade.data import Bar

IDEA = "halloween"
P_BAR = 0.10 / 65  # the wide-* lineage's family: 61 + survey-4's 4 (cards/halloween.md)
POST1 = date(1998, 11, 1)  # after Bouman and Jacobsen's sample
POST2 = date(2012, 5, 1)  # after Andrade, Chhaochharia and Fuerst's new data
STOCKS = {"SPY", "QQQ", "IWM", "EFA", "EEM", "GSPC", "N225", "FTSE", "GDAXI"}
CHECK_DAYS = [date(1999, 10, 1), date(2008, 10, 10), date(2018, 12, 21), date(2023, 6, 2)]


def friday_of(d: date) -> date:
    """The weekly decision day that governs session d (`common.weekly`: last Friday <= d)."""
    return d - timedelta(days=(d.weekday() - 4) % 7)


def strat(alone: bool = False) -> c.ResearchStrategy:
    """`tsmom12`; stock slots only in winter weeks. `alone`: stock slots full in winter weeks
    whatever the trend (R12's rule), cash in summer weeks."""

    def f(view: c.View) -> c.Weights:
        held = c.live(view)
        if not held:
            return {}
        slot = 1 / len(held)
        winter = r.winter_week(view.today)
        out = {}
        for s in held:
            if s in STOCKS:
                if winter and (alone or c.tsmom_signal(view, s)):
                    out[s] = slot
            elif c.tsmom_signal(view, s):
                out[s] = slot
        return out

    return c.weekly(f)


def welch(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 3 or len(b) < 3:
        return math.nan
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return float((a.mean() - b.mean()) / se) if se > 0 else math.nan


def study(
    sym: str, bars: Sequence[Bar], windows: Sequence[tuple[str, date, date]], kind: str
) -> tuple[list[str], dict[str, tuple[float, float]]]:
    """Mean next-interval return (bps a day) in winter vs summer weeks, by the rule's week
    assignment. `open`: open(d+1) -> open(d+2); `close`: close(d) -> close(d+1)."""
    days = [x.date for x in bars]
    lc = np.log(np.array([x.close for x in bars]))
    lo = np.log(np.array([x.open for x in bars]))
    lines, got = [], {}
    for name, a, b in windows:
        win, summ = [], []
        for i in range(len(days) - 2):
            if not a <= days[i] <= b:
                continue
            x = lo[i + 2] - lo[i + 1] if kind == "open" else lc[i + 1] - lc[i]
            (win if r.winter_week(friday_of(days[i])) else summ).append(x * 1e4)
        u, d_ = np.array(win), np.array(summ)
        t = welch(u, d_)
        lines.append(
            f"| {sym} ({kind}) | {name} | {len(u)} / {len(d_)} | {u.mean():+.1f} | "
            f"{d_.mean():+.1f} | {u.mean() - d_.mean():+.1f} ({t:+.2f}) |"
        )
        got[name] = (float(u.mean() - d_.mean()), t)
    return lines, got


def window_diff(p: harness.Run, t: harness.Run, a: date, b: date) -> float:
    lo, hi = max(a, p.days[0], t.days[0]), min(b, p.days[-1], t.days[-1])
    if (hi - lo).days < 200:
        return math.nan
    return float(stats.sharpe(p.rets_between(lo, hi)) - stats.sharpe(t.rets_between(lo, hi)))


def main() -> None:
    six, etf, idx = c.ctx("six"), c.ctx("etf"), c.ctx("idx")
    variants = [("halloween", strat(False)), ("halloween-alone", strat(True))]
    if not c.DRY:  # no look-ahead: the fast path equals gym.backtest on sample Fridays
        for _, s in variants:
            harness.check_against_gym(s, six.hist, CHECK_DAYS)
        harness.check_against_gym(strat(False), etf.hist, CHECK_DAYS[1:])

    out = ["# halloween: stock trend slots only from November to April", ""]
    out += ["Card: `cards/halloween.md`. Survey: `survey-4.md` (pick B). Protocol: "
            "`protocol.md`. No-look-ahead check against `gym.backtest` on "
            + ", ".join(str(d) for d in CHECK_DAYS) + ": passed.", ""]  # fmt: skip
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    runs = {name: c.go(IDEA, name, s, six, "variant") for name, s in variants}
    allr = [*runs.values(), twin, ew]
    out += ["## The six live assets, train period", "", c.table(allr, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(allr), ""]

    bd, by = cash_interest.bill_yield()
    out += ["Sharpe above T-bills with T-bill interest on cash (`cash_interest.rescored`; no row):",
            ""]  # fmt: skip
    for run in allr:
        rr, rf = cash_interest.rescored(run, bd, by)
        out.append(f"- `{run.variant}`: {stats.sharpe(rr - rf):.2f} "
                   f"(gym: {stats.sharpe(run.rets):.2f})")  # fmt: skip
    out.append("")

    t_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    t_i = c.go("baselines", "tsmom12", twin_s, idx, "baseline", log=False)
    oe = {n: c.go(IDEA, n, strat(n.endswith("alone")), etf, "robustness") for n, _ in variants}
    oi = {n: c.go(IDEA, n, strat(n.endswith("alone")), idx, "robustness") for n, _ in variants}
    out += ["## Out of universe", "", "Other ETFs (gate on IWM, EFA, EEM):", "",
            c.table([*oe.values(), t_e], t_e), "",
            "Four indexes as one portfolio from 1962 (gate on all four):", "",
            c.table([*oi.values(), t_i], t_i), ""]  # fmt: skip

    wins = [("1994 - 1998-10 (in R12's sample)", date(1994, 2, 1), POST1 - timedelta(days=1)),
            ("1998-11 - 2012-04 (R13's new data)", POST1, POST2 - timedelta(days=1)),
            ("2012-05 to end of train (after)", POST2, c.TRAIN_END)]  # fmt: skip
    out += ["## In and after the samples: Sharpe minus the twin's", ""]
    out += ["| Run | " + " | ".join(n for n, _, _ in wins) + " |", "|---|" + "---:|" * len(wins)]
    for name, run in runs.items():
        cells = [window_diff(run, twin, a, b) for _, a, b in wins]
        out.append(f"| {name} | " + " | ".join(f"{x:+.3f}" for x in cells) + " |")
    out.append("")

    out += ["## Event study (descriptive): winter minus summer weeks, bps a day", ""]
    out += ["Mean daily log return by the rule's week assignment (the Monday after the governing "
            "Friday in November-April = winter). SPY: next open to next open; S&P 500 index: "
            "close to close. All days, whatever the trend.", ""]  # fmt: skip
    out += ["| Asset | Window | n winter / summer | winter | summer | spread (t) |",
            "|---|---|---:|---:|---:|---:|"]  # fmt: skip
    sl, sg = study("SPY", six.hist["SPY"], wins, "open")
    gw = [("1962-1969 (before R12)", date(1962, 1, 1), date(1969, 12, 31)),
          ("1970-1993 (in R12's sample)", date(1970, 1, 1), date(1993, 1, 28))]  # fmt: skip
    gl, _ = study("GSPC", c.ctx("GSPC").hist["GSPC"], gw, "close")
    ql, _ = study("QQQ", six.hist["QQQ"], wins[1:], "open")
    out += [*gl, *sl, *ql, ""]

    de, dt = c.describe(ew), c.describe(twin)
    sp2, st2 = sg[wins[2][0]]
    for name, run in runs.items():
        vs = w.versus(run, twin)
        dv = c.describe(run)
        se, si = w.versus(oe[name], t_e)["diff"], w.versus(oi[name], t_i)["diff"]
        p1, p2 = w.since(run, twin, POST1), w.since(run, twin, POST2)
        d = vs["diff"]
        bars = [
            (f"1. Beats twin `tsmom12` with p < {P_BAR:.5f} (0.10 / 65)",
             d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
            (f"2. Ahead of the twin in at least 4 of {vs['eras']:.0f} eras",
             vs["ahead"] >= 4, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
            ("3. Max drawdown not more than 5 points worse than the twin's",
             dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
            ("4. Positive on the ETF and index sets", se > 0 and si > 0,
             f"etf {se:+.3f}, idx {si:+.3f}"),
            ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
             f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
            ("6. (card) Not behind the twin from 1998-11-01", p1 >= 0, f"{p1:+.3f}"),
            ("7. (card) Not behind the twin from 2012-05-01, SPY winter-minus-summer > 0",
             p2 >= 0 and sp2 > 0, f"{p2:+.3f}; SPY {sp2:+.1f} bps a day (t {st2:+.2f})"),
        ]  # fmt: skip
        out += [f"## Pass bar: `{name}`", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
