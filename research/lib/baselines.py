"""Benchmarks and plain twins on every test universe, logged once as baselines.

    uv run --with numpy python research/lib/baselines.py

Idea scripts re-score these with `log=False` (same configuration, already counted here).
"""

from __future__ import annotations

import common as c

IDEA = "baselines"
SINGLES = ["GSPC", "N225", "FTSE", "GDAXI"]


def twins() -> dict[str, c.ResearchStrategy]:
    return {
        "equal-weight": c.weekly(c.equal_weight),
        "sma200": c.weekly(c.slots(c.sma_signal)),
        "tsmom12": c.weekly(c.slots(c.tsmom_signal)),
        "inverse-vol": c.weekly(c.inverse_vol),
        "vol-calm": c.weekly(c.slots(c.vol_calm_signal)),
    }


def main() -> None:
    out = ["# Baselines: benchmarks and plain twins", ""]
    out += [
        "Train period, total-return prices, gym costs. Sharpe on calendar days, zero risk-free "
        "rate; era columns are Sharpe ratios. See `protocol.md`.",
        "",
    ]
    six = c.ctx("six")
    runs = [
        c.go(IDEA, "bh-spy", c.weekly(c.hold("SPY")), six, "baseline"),
        c.go(IDEA, "bh-btc", c.weekly(c.hold("BTC")), six, "baseline"),
        c.go(IDEA, "sixty-forty", c.weekly(c.sixty_forty), six, "baseline"),
    ]
    runs += [c.go(IDEA, n, f, six, "baseline") for n, f in twins().items()]
    ew = next(r for r in runs if r.variant == "equal-weight")
    out += ["## The six live assets, 1994-2025", "", c.table(runs, versus=ew), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    for name, title in [("etf", "8 other ETFs"), ("coin", "6 other coins"), ("idx", "4 indexes")]:
        u = c.ctx(name)
        runs = [c.go(IDEA, n, f, u, "baseline") for n, f in twins().items()]
        out += [f"## Out of universe: {title}, from {u.start}", "", c.table(runs, runs[0]), ""]
    for name in SINGLES:
        u = c.ctx(name)
        runs = [c.go(IDEA, n, f, u, "baseline") for n, f in twins().items() if n != "inverse-vol"]
        out += [f"## Out of universe: {name} alone, from {u.start}", "", c.table(runs, runs[0]), ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
