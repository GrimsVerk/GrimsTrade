"""uv run --with numpy python research/lib/idea_wide2_crowded_trend.py
(card: cards/crowded-trend.md)"""

from __future__ import annotations

import common as c
import wide1 as w

IDEA = "crowded-trend"
MIN_ASSETS = 3
P_BAR = 0.10 / 42  # Bonferroni: every pick out of wide-1's 42 uncarded mechanisms is counted


def crowd(view: c.View) -> c.Weights:
    """`tsmom12` weights, halved when at least three assets are eligible and all are in trend.
    Reads only the bars the view shows."""
    live = c.live(view)
    held = [s for s in live if c.tsmom_signal(view, s)]
    full = len(live) >= MIN_ASSETS and len(held) == len(live)
    return {s: (0.5 if full else 1.0) / len(live) for s in held}


def main() -> None:
    out = ["# crowded-trend: halve the book when every asset is in trend", ""]
    out += ["Card: `cards/crowded-trend.md`. Protocol: `protocol.md`.", ""]
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    rule = c.weekly(crowd)
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "crowd", rule, six, "variant")
    runs = [run, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin)
    pairs = [(a, b) for a, b in zip(run.decisions, twin.decisions, strict=True)
             if a.time.date().weekday() == 4]  # fmt: skip
    acted = sum(a.weights != b.weights for a, b in pairs)
    out += [f"Fridays on which the rule halves the book: {acted} of {len(pairs)} "
            f"({acted / len(pairs):.0%}).", ""]  # fmt: skip

    out += ["## Out of universe", ""]
    signs: dict[str, float] = {}
    for name in ("etf", "coin", "idx"):
        u = c.ctx(name)
        t = c.go("baselines", "tsmom12", twin_s, u, "baseline", log=False)
        a = c.go(IDEA, "crowd", rule, u, "robustness")
        out += [c.table([a, t], t, eras=False), ""]
        signs[name] = w.versus(a, t)["diff"]

    dv, dt, de = c.describe(run), c.describe(twin), c.describe(ew)
    d = vs["diff"]
    same = sum((x > 0) == (d > 0) for x in signs.values())
    need = 4 if vs["eras"] == 5 else 3
    bars = [
        (f"1. `crowd` beats twin `tsmom12` with p < {P_BAR:.4f} (0.10 / 42)",
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
    out += ["## Pass bar (only variant `crowd`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
