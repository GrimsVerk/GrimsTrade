"""uv run --with numpy python research/lib/idea_wide2_patch_leaving.py
(card: cards/patch-leaving.md)"""

from __future__ import annotations

import math

import common as c
import wide1 as w

IDEA = "patch-leaving"
P_BAR = 0.10 / 42  # Bonferroni: every pick out of wide-1's 42 uncarded mechanisms is counted


def zscore(view: c.View, s: str) -> float:
    """The protocol's z(365): 365-day log return over annualised EWMA volatility (60 bars)."""
    r, v = c.trailing_logret(view, s, 365), c.asset_vol(view, s, 60)
    return r / v if not (math.isnan(r) or math.isnan(v)) and v > 0 else math.nan


def mvt(view: c.View) -> c.Weights:
    """The twin's total weight, split equally among the assets it holds whose z is at least the
    mean z of all eligible assets. Reads only the bars the view shows."""
    live = c.live(view)
    held = [s for s in live if c.tsmom_signal(view, s)]
    if not held:
        return {}
    z = {s: zscore(view, s) for s in live}
    known = [x for x in z.values() if not math.isnan(x)]
    m = sum(known) / len(known) if known else math.nan
    stay = [s for s in held if not math.isnan(z[s]) and z[s] >= m] or held
    total = len(held) / len(live)
    return {s: total / len(stay) for s in stay}


def main() -> None:
    out = ["# patch-leaving: leave an asset when its trend is below the average", ""]
    out += ["Card: `cards/patch-leaving.md`. Protocol: `protocol.md`.", ""]
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    rule = c.weekly(mvt)
    six = c.ctx("six")
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "mvt", rule, six, "variant")
    runs = [run, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin)
    fr = [d for d in run.decisions if d.time.date().weekday() == 4 and d.weights]
    names = sum(len(d.weights) for d in fr) / len(fr)
    coins = sum(d.weights.get("BTC", 0) + d.weights.get("ETH", 0) for d in fr) / len(fr)
    tf = [d for d in twin.decisions if d.time.date().weekday() == 4 and d.weights]
    tnames = sum(len(d.weights) for d in tf) / len(tf)
    tcoins = sum(d.weights.get("BTC", 0) + d.weights.get("ETH", 0) for d in tf) / len(tf)
    out += [f"Assets held on an average invested Friday: {names:.1f} (twin {tnames:.1f}). "
            f"Average weight in BTC and ETH: {coins:.1%} (twin {tcoins:.1%}).", ""]  # fmt: skip

    out += ["## Out of universe", ""]
    signs: dict[str, float] = {}
    for name in ("etf", "coin", "idx"):
        u = c.ctx(name)
        t = c.go("baselines", "tsmom12", twin_s, u, "baseline", log=False)
        a = c.go(IDEA, "mvt", rule, u, "robustness")
        out += [c.table([a, t], t, eras=False), ""]
        signs[name] = w.versus(a, t)["diff"]

    dv, dt, de = c.describe(run), c.describe(twin), c.describe(ew)
    d = vs["diff"]
    same = sum((x > 0) == (d > 0) for x in signs.values())
    need = 4 if vs["eras"] == 5 else 3
    bars = [
        (f"1. `mvt` beats twin `tsmom12` with p < {P_BAR:.4f} (0.10 / 42)",
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
    out += ["## Pass bar (only variant `mvt`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
