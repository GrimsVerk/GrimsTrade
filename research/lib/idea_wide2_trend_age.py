"""uv run --with numpy python research/lib/idea_wide2_trend_age.py
(card: cards/trend-age.md)"""

from __future__ import annotations

import math
from datetime import timedelta

import common as c
import wide1 as w

IDEA = "trend-age"
WEEKS = 4  # the signal must hold at this Friday and the WEEKS - 1 Fridays before it
P_BAR = 0.10 / 42  # Bonferroni: this card was picked out of 42 uncarded mechanisms


def aged_signal(view: c.View, s: str) -> bool:
    """`tsmom12` true now and at each of the three decisions 7, 14 and 21 days earlier. Every
    earlier check uses `view.at`, the view that decision day had: nothing later is read."""
    if not c.tsmom_signal(view, s):
        return False
    today = view.today
    friday = today + timedelta(days=(4 - today.weekday()) % 7)  # today, or a holiday Friday
    for k in range(1, WEEKS):
        past = view.at(friday - timedelta(days=7 * k))
        if not c.tsmom_signal(past, s):
            return False
    return True


def spells(run: c.Run, syms: list[str]) -> tuple[list[str], list[int]]:
    """On-spells of the twin's weekly decisions, per asset: lengths in weeks. A spell still
    open at the end of the period is left out (its length is not known)."""
    lines = ["| Asset | On-spells | Ended within 4 weeks | Median length (weeks) |",
             "|---|---:|---:|---:|"]  # fmt: skip
    fridays = [d for d in run.decisions if d.time.date().weekday() == 4]
    every: list[int] = []
    for s in syms:
        lens, cur = [], 0
        for d in fridays:
            if d.weights.get(s, 0) > 0:
                cur += 1
            elif cur:
                lens.append(cur)
                cur = 0
        every += lens
        if lens:
            med = sorted(lens)[len(lens) // 2]
            lines.append(f"| {s} | {len(lens)} | {sum(x <= 4 for x in lens)} | {med} |")
    return lines, every


def hazard(lens: list[int]) -> list[str]:
    out = ["| Age (weeks) | Spells alive | Ended at that age | Weekly hazard |"]
    out.append("|---|---:|---:|---:|")
    for a in (1, 2, 3, 4):
        alive, ended = sum(x >= a for x in lens), sum(x == a for x in lens)
        out.append(f"| {a} | {alive} | {ended} | {ended / alive if alive else math.nan:.1%} |")
    weeks = sum(x - 4 for x in lens if x > 4)
    ended = sum(x > 4 for x in lens)
    rate = ended / weeks if weeks else math.nan
    out.append(f"| 5+ | {weeks} spell-weeks | {ended} | {rate:.1%} |")
    return out


def main() -> None:
    out = ["# trend-age: hold a trend only once it has survived four weeks", ""]
    out += ["Card: `cards/trend-age.md`. Protocol: `protocol.md`.", ""]
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    rule = c.weekly(c.slots(aged_signal))
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    age = c.go(IDEA, "age4", rule, six, "variant")
    runs = [age, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(age, twin)

    out += ["## On-spells of the twin's signal (descriptive)", ""]
    lines, lens = spells(twin, six.panel.syms)
    out += [*lines, "", *hazard(lens), ""]

    out += ["## Out of universe", ""]
    signs: dict[str, float] = {}
    for name in ("etf", "coin"):
        u = c.ctx(name)
        t = c.go("baselines", "tsmom12", twin_s, u, "baseline", log=False)
        a = c.go(IDEA, "age4", rule, u, "robustness")
        out += [c.table([a, t], t, eras=False), ""]
        signs[name] = w.versus(a, t)["diff"]
    idx = []
    for name in c.OOU_INDEXES:
        u = c.ctx(name)
        t = c.go("baselines", "tsmom12", twin_s, u, "baseline", log=False)
        a = c.go(IDEA, "age4", rule, u, "robustness")
        out += [c.table([a, t], t, eras=False), ""]
        idx.append(w.versus(a, t)["diff"])
    signs["idx"] = sum(idx) / len(idx)

    dv, dt, de = c.describe(age), c.describe(twin), c.describe(ew)
    d = vs["diff"]
    same = sum((x > 0) == (d > 0) for x in signs.values())
    need = 4 if vs["eras"] == 5 else 3
    bars = [
        (f"1. `age4` beats twin `tsmom12` with p < {P_BAR:.4f} (0.10 / 42)",
         d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in at least {need} of {vs['eras']:.0f} eras",
         vs["ahead"] >= need, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and the same sign in at least 2 of 3 out-of-universe sets",
         d > 0 and same >= 2, ", ".join(f"{k} {v:+.3f}" for k, v in signs.items())),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `age4`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
