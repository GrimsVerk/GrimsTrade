"""uv run python research/lib/wide3_pageviews.py, then
uv run python research/lib/idea_wide3_attention_peak.py
(card: cards/attention-peak.md)"""

from __future__ import annotations

import csv
import math
from collections.abc import Mapping
from datetime import date, timedelta

import common as c
import numpy as np
import wide1 as w
from wide3_pageviews import OUT, TITLES

IDEA = "attention-peak"
P_BAR = 0.10 / 46  # Bonferroni over wide-1's whole list of 46 mechanisms (wide-3.md, step 1)
SURGE = 3.0
RECENT, BASE, PEAK, WEEK = 28, 365, 56, 7

Views = Mapping[str, tuple[date, np.ndarray]]  # coin -> (first day, daily views from it)


def load_views() -> dict[str, tuple[date, np.ndarray]]:
    """Daily views per coin, the card's titles summed; a missing day inside the series is 0.
    The series starts on the first day any of the coin's titles has data."""
    out = {}
    for coin, titles in TITLES.items():
        days: dict[date, int] = {}
        for t in titles:
            path = OUT / f"{t}.csv"
            if not path.exists():
                continue
            with path.open(newline="") as f:
                for r in csv.DictReader(f):
                    d = date.fromisoformat(r["date"])
                    days[d] = days.get(d, 0) + int(r["views"])
        if not days:
            continue
        first, last = min(days), max(days)
        n = (last - first).days + 1
        v = np.zeros(n)
        for d, x in days.items():
            v[(d - first).days] = x
        out[coin] = (first, v)
    return out


def out_of_mania(views: Views, coin: str, today: date) -> bool:
    """The card's test on the views up to the day before `today`: surge and past the peak."""
    if coin not in views:
        return False
    first, v = views[coin]
    n = (today - first).days  # views of days first .. today-1
    if n < BASE + RECENT:
        return False
    x = v[:n]
    recent = x[-RECENT:].mean()
    base = float(np.median(x[-(BASE + RECENT) : -RECENT]))
    if not (recent > 0 and recent >= SURGE * base):
        return False
    tail = x[-(PEAK + WEEK - 1) :]
    ma7 = np.convolve(tail, np.ones(WEEK) / WEEK, mode="valid")  # ends on each of the last 56 days
    return bool(ma7[-1] < ma7.max())


def peak_rule(views: Views) -> c.ResearchStrategy:
    """`tsmom12`'s equal slots; a coin's slot is cash while its attention epidemic is past its
    peak. ETFs are never touched."""

    def f(view: c.View) -> c.Weights:
        live = c.live(view)
        today = view.today
        return {s: 1 / len(live) for s in live
                if c.tsmom_signal(view, s)
                and not (s in TITLES and out_of_mania(views, s, today))}  # fmt: skip

    return f


def spells(views: Views, coin: str, fridays: list[date]) -> list[tuple[date, date]]:
    """Runs of consecutive Fridays on which the coin is out."""
    out: list[tuple[date, date]] = []
    for d in fridays:
        if out_of_mania(views, coin, d):
            if out and (d - out[-1][1]).days <= 7:
                out[-1] = (out[-1][0], d)
            else:
                out.append((d, d))
    return out


def main() -> None:
    views = load_views()
    out = ["# attention-peak: leave a coin once its attention epidemic has peaked", ""]
    out += ["Card: `cards/attention-peak.md`. Protocol: `protocol.md`.", ""]
    out += ["Page-view series per coin (first day): "
            + ", ".join(f"{k} {v[0]}" for k, v in views.items()) + ".", ""]  # fmt: skip
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    rule = c.weekly(peak_rule(views))
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "peak", rule, six, "variant")
    runs = [run, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin, "2017-21")

    out += ["## Out spells", ""]
    out += ["| Coin | First Friday out | Last Friday out | Fridays | Twin held it (Fridays) | "
            "Coin return, first out Friday to the Friday after the last (log) |",
            "|---|---|---|---:|---:|---:|"]  # fmt: skip
    held = {d.time.date(): d.weights for d in twin.decisions}
    fr = sorted(d for d in held if d.weekday() == 4)
    for sym in ("BTC", "ETH"):
        closes = {b.date: b.close for b in six.hist[sym]}
        for a, b in spells(views, sym, fr):
            nxt = b + timedelta(days=7)
            r = (math.log(closes[nxt] / closes[a])
                 if a in closes and nxt in closes else math.nan)  # fmt: skip
            k = (b - a).days // 7 + 1
            tw_n = sum(sym in held[d] for d in fr if a <= d <= b)
            out.append(f"| {sym} | {a} | {b} | {k} | {tw_n} | {r:+.1%} |")
    out.append("")

    out += ["## Out of universe: the 6 other coins", ""]
    coin = c.ctx("coin")
    twin_c = c.go("baselines", "tsmom12", twin_s, coin, "baseline", log=False)
    run_c = c.go(IDEA, "peak", rule, coin, "robustness")
    out += [c.table([run_c, twin_c], twin_c, eras=False), ""]
    vs_c = w.versus(run_c, twin_c)
    fr_c = sorted(d.time.date() for d in twin_c.decisions if d.time.date().weekday() == 4)
    n_out = {k: len(spells(views, k, fr_c)) for k in c.OOU_COINS}
    out += ["Out spells per other coin: "
            + ", ".join(f"{k} {v}" for k, v in n_out.items()) + ".", ""]  # fmt: skip

    dv, dt, de = c.describe(run), c.describe(twin), c.describe(ew)
    d = vs["diff"]
    bars = [
        (f"1. `peak` beats twin `tsmom12` with p < {P_BAR:.4f} (0.10 / 46)",
         d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in both eras from 2017-21 ({vs['eras']:.0f} counted)",
         vs["ahead"] >= 2 and vs["eras"] == 2, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and positive on the one applicable out-of-universe set",
         d > 0 and vs_c["diff"] > 0, f"coin set {vs_c['diff']:+.3f} (p = {vs_c['p']:.2f})"),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `peak`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
