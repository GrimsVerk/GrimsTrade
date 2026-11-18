"""uv run python research/lib/idea_wide3_opex_pin.py
(card: cards/opex-pin.md)"""

from __future__ import annotations

import math
from collections.abc import Sequence
from datetime import date, timedelta

import common as c
import numpy as np
import wide1 as w

from grimstrade.data import Bar

IDEA = "opex-pin"
P_BAR = 0.10 / 49  # the list of 46 plus wide-3's three new mechanisms (cards/opex-pin.md)
STOCKS = {
    "six": ("SPY", "QQQ"),
    "etf": ("IWM", "EFA", "EEM", "VNQ"),
    "idx": ("GSPC", "N225", "FTSE", "GDAXI"),
}


def is_third_friday(d: date) -> bool:
    return d.weekday() == 4 and 15 <= d.day <= 21


def decision_friday(view: c.View) -> date:
    """The calendar Friday of a weekly decision (the latest close may be a Thursday when the
    Friday is a holiday)."""
    t = view.today
    return t + timedelta(days=(4 - t.weekday()) % 7)


def overlay(stocks: Sequence[str], lag_weeks: int) -> c.ResearchStrategy:
    """`tsmom12` plus the idle cash on the eligible `stocks` in the week whose closing Friday is
    `lag_weeks` after the decision's next Friday is the third Friday (`pin`: 0, `pin-after`: 1:
    the week after expiry)."""

    def f(view: c.View) -> c.Weights:
        live = c.live(view)
        out = {s: 1 / len(live) for s in live if c.tsmom_signal(view, s)}
        fri = decision_friday(view)
        if not is_third_friday(fri + timedelta(days=7 - 7 * lag_weeks)):
            return out
        st = [s for s in stocks if s in live]
        idle = 1.0 - sum(out.values())
        if st and idle > 1e-9:
            for s in st:
                out[s] = out.get(s, 0.0) + idle / len(st)
        return out

    return f


def pin(view: c.View) -> c.Weights:
    return overlay(STOCKS["six"], 0)(view)


def week_events(bars: Sequence[Bar], first: date, last: date) -> tuple[np.ndarray, np.ndarray]:
    """Friday-to-Friday close log returns (last close on or before each Friday) in [first, last]:
    (returns of the expiry weeks, returns of all weeks)."""
    days = [b.date.toordinal() for b in bars]
    closes = [b.close for b in bars]

    def close_on_or_before(d: date) -> float:
        i = int(np.searchsorted(days, d.toordinal(), side="right")) - 1
        return closes[i] if i >= 0 else math.nan

    f = first + timedelta(days=(4 - first.weekday()) % 7)
    exp, allw = [], []
    while f + timedelta(days=7) <= last:
        a, b = close_on_or_before(f), close_on_or_before(f + timedelta(days=7))
        if not (math.isnan(a) or math.isnan(b)) and a > 0:
            r = math.log(b / a)
            allw.append(r)
            if is_third_friday(f + timedelta(days=7)):
                exp.append(r)
        f += timedelta(days=7)
    return np.array(exp), np.array(allw)


def study_row(name: str, bars: Sequence[Bar], first: date, last: date) -> tuple[str, float, float]:
    exp, allw = week_events(bars, first, last)
    if len(exp) < 3:
        return f"| {name} | {len(exp)} | - | - |", math.nan, math.nan
    x = exp - allw.mean()
    t = w.tstat(x)
    return (f"| {name} | {len(exp)} | {x.mean() * 1e4:+.1f} | {t:+.2f} |", float(x.mean()), t)


def main() -> None:
    out = ["# opex-pin: idle cash into stocks for the option-expiry week", ""]
    out += ["Card: `cards/opex-pin.md`. Protocol: `protocol.md`.", ""]
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "pin", c.weekly(pin), six, "variant")
    after = c.go(IDEA, "pin-after", c.weekly(overlay(STOCKS["six"], 1)), six, "robustness")
    runs = [run, after, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin)
    acted = sum(a.weights != b.weights for a, b in zip(run.decisions, twin.decisions, strict=True)
                if a.time.date().weekday() == 4)  # fmt: skip
    out += [f"Fridays on which `pin` differs from the twin: {acted}.", ""]

    out += ["## Event study (descriptive): expiry week minus the average week, close to close", ""]
    out += ["| Series and period | Expiry weeks | Excess, bps a week | t |", "|---|---:|---:|---:|"]
    spy = six.hist["SPY"]
    rows = []
    for name, a, b in (("SPY 1994-2025", date(1994, 2, 1), c.TRAIN_END),
                       ("SPY 1994-99", date(1994, 2, 1), date(1999, 12, 31)),
                       ("SPY 2000-09", date(2000, 1, 1), date(2009, 12, 31)),
                       ("SPY 2010-16", date(2010, 1, 1), date(2016, 12, 31)),
                       ("SPY 2017-21", date(2017, 1, 1), date(2021, 12, 31)),
                       ("SPY 2022-25", date(2022, 1, 1), c.TRAIN_END)):  # fmt: skip
        line, m, t = study_row(name, spy, a, b)
        out.append(line)
        rows.append((name, m, t))
    gspc = c.ctx("GSPC").hist["GSPC"]
    pre = study_row("S&P 500 index 1962-01 to 1983-02 (placebo)", gspc, date(1962, 1, 1),
                    date(1983, 2, 28))  # fmt: skip
    post = study_row("S&P 500 index 1983-03 to 1993-01", gspc, date(1983, 3, 1),
                     date(1993, 1, 28))  # fmt: skip
    out += [pre[0], post[0], ""]
    spy_m, spy_t = rows[0][1], rows[0][2]
    supported = spy_m > 0 and spy_t >= 2 and pre[1] < post[1]
    out += [f"Card's reading: SPY excess positive with t >= 2 and placebo below 1983-1993: "
            f"**{'supported' if supported else 'not supported'}**.", ""]  # fmt: skip

    out += ["## Out of universe", ""]
    signs: dict[str, float] = {}
    for name in ("etf", "idx"):
        u = c.ctx(name)
        t = c.go("baselines", "tsmom12", twin_s, u, "baseline", log=False)
        a = c.go(IDEA, "pin", c.weekly(overlay(STOCKS[name], 0)), u, "robustness")
        out += [c.table([a, t], t, eras=False), ""]
        signs[name] = w.versus(a, t)["diff"]

    dv, dt, de, da = c.describe(run), c.describe(twin), c.describe(ew), c.describe(after)
    d = vs["diff"]
    bars = [
        (f"1. `pin` beats twin `tsmom12` with p < {P_BAR:.4f} (0.10 / 49)",
         d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in at least 4 of {vs['eras']:.0f} eras",
         vs["ahead"] >= 4, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and positive on both applicable out-of-universe sets",
         d > 0 and all(x > 0 for x in signs.values()),
         ", ".join(f"{k} {v:+.3f}" for k, v in signs.items())),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) Beats its placebo `pin-after` on Sharpe", dv["sharpe"] > da["sharpe"],
         f"{dv['sharpe']:.3f} vs {da['sharpe']:.3f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `pin`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
