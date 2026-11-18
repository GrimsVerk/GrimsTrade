"""The plain rules and the run-2 rules on BTC alone and ETH alone (the survey's one positive
crypto claim is slow trend on Bitcoin).

    uv run --with numpy python research/lib/crypto_alone.py
"""

from __future__ import annotations

import common as c
import rules

IDEA = "crypto-alone"


def main() -> None:
    out = ["# BTC alone and ETH alone", ""]
    out += [
        "Each asset on its own, in or out (or scaled). Train period, gym costs (60 bps a round "
        "trip). `equal-weight` is buy-and-hold. The first three rows are baselines; the last "
        "three are the run-2 rules, unchanged (robustness rows).",
        "",
    ]
    base = {
        "equal-weight": c.weekly(c.equal_weight),
        "sma200": c.weekly(c.slots(c.sma_signal)),
        "tsmom12": c.weekly(c.slots(c.tsmom_signal)),
    }
    more = {
        "e4": c.weekly(rules.ensemble_tsmom),
        "t40": c.weekly(rules.vol_target(0.40)),
        "tv40": c.weekly(rules.trend_vol(0.40)),
    }
    for sym in ("BTC", "ETH"):
        u = c.ctx(sym)
        runs = [c.go(IDEA, n, f, u, "baseline") for n, f in base.items()]
        runs += [c.go(IDEA, n, f, u, "robustness") for n, f in more.items()]
        out += [f"## {sym}, from {u.start}", "", c.table(runs, versus=runs[0]), ""]
        out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
        out += [
            "Annualised log growth: " + ", ".join(f"{r.variant} {c.growth(r):+.1%}" for r in runs)
        ]
        out += [""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
