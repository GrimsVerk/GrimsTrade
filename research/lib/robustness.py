"""Front-runners on the prices the live system trades (raw, no dividends) and at double costs.

uv run --with numpy python research/lib/robustness.py
"""

from __future__ import annotations

import common as c
import harness
import rules

from grimstrade import gym

IDEA = "robustness"


def front_runners() -> dict[str, c.ResearchStrategy]:
    return {
        "equal-weight": c.weekly(c.equal_weight),
        "tsmom12": c.weekly(c.slots(c.tsmom_signal)),
        "sma200": c.weekly(c.slots(c.sma_signal)),
        "ensemble-tsmom": c.weekly(rules.ensemble_tsmom),
        "trend-vol": c.weekly(rules.trend_vol(0.40)),
    }


def main() -> None:
    out = ["# Robustness of the front-runners", ""]
    out += ["Six live assets, train period. Same rules as in their own result files.", ""]
    raw = c.ctx("six", adjusted=False)
    runs = [c.go(IDEA, f"{n}-raw", f, raw, "robustness") for n, f in front_runners().items()]
    out += ["## Raw prices (what the live scoreboard will show: no dividends)", ""]
    out += [c.table(runs, versus=runs[0]), ""]
    six = c.ctx("six")
    double = {k: gym.Costs(fee=2 * v.fee, slip=2 * v.slip) for k, v in gym.COSTS.items()}
    runs = [
        harness.run(IDEA, f"{n}-2xcost", f, kind="robustness", panel=six.panel, history=six.hist,
                    start=six.start, end=six.end, costs=double, log=not c.DRY)
        for n, f in front_runners().items()
    ]  # fmt: skip
    out += ["## Total-return prices, double costs (120 bps crypto, 8 bps ETF round trip)", ""]
    out += [c.table(runs, versus=runs[0]), ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
