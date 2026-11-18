"""What if cash earned the Treasury-bill rate? A what-if on top of the gym's equity curves.

    uv run --with numpy python research/lib/cash_interest.py

The gym pays 0 on cash. Here each day's return gets (share of the book in cash) x (T-bill yield
/ 365) added, and Sharpe is measured on returns above the T-bill rate: the convention most of
the literature uses. No new strategy is run; the front-runners are re-scored (`log=False`).
"""

from __future__ import annotations

import bisect
from datetime import date

import common as c
import harness
import numpy as np
import robustness
import stats

from grimstrade import data


def bill_yield() -> tuple[list[date], list[float]]:
    bars = [b for b in data.load(harness.RESEARCH, "IRX") if b.date <= harness.TRAIN_LAST_BAR]
    return [b.date for b in bars], [b.close / 100 for b in bars]


def rescored(run: harness.Run, days: list[date], yields: list[float]) -> tuple[np.ndarray, ...]:
    """(returns with interest on cash, daily T-bill rate), aligned to run.rets."""
    expo = {d.time.date(): sum(d.weights.values()) for d in run.decisions}
    r = run.rets.copy()
    rf = np.empty(len(r))
    cash = 0.0
    for k, d in enumerate(run.days[1:]):
        i = bisect.bisect_right(days, d) - 1
        rf[k] = yields[max(i, 0)] / 365
        r[k] += cash * rf[k]
        cash = 1 - expo.get(d, 1 - cash)  # target cash share after that day's decision
    return r, rf


def main() -> None:
    days, yields = bill_yield()
    six = c.ctx("six")
    rows = []
    for name, f in robustness.front_runners().items():
        run = c.go("baselines", name, f, six, "baseline", log=False)
        r, rf = rescored(run, days, yields)
        rows.append((name, run, r, rf))
    out = ["# What if cash earned the Treasury-bill rate?", ""]
    out += [
        "Six live assets, train period, total-return prices. Left: the gym as it is (cash earns "
        "0, Sharpe against 0). Right: cash earns the 13-week T-bill yield and Sharpe is measured "
        f"above that yield. Average T-bill yield over the period: {np.mean(rows[0][3]) * 365:.1%}.",
        "",
        "| Variant | Avg cash share | Sharpe (gym) | CAGR (gym) | Sharpe above T-bills | "
        "CAGR with interest | Lead over equal weight: gym | above T-bills |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    base_gym = stats.sharpe(rows[0][1].rets)
    base_ex = stats.sharpe(rows[0][2] - rows[0][3])
    for name, run, r, rf in rows:
        sg, se = stats.sharpe(run.rets), stats.sharpe(r - rf)
        out.append(
            f"| {name} | {1 - run.exposure:.0%} | {sg:.2f} | {stats.cagr(run.rets):+.1%} | "
            f"{se:.2f} | {stats.cagr(r):+.1%} | {sg - base_gym:+.2f} | {se - base_ex:+.2f} |"
        )
    out += [""]
    for era, a, b in harness.ERAS[2:]:
        parts = []
        for name, run, r, rf in rows:
            i = max((a - run.days[1]).days, 0)
            j = min((b - run.days[1]).days, len(r) - 1)
            parts.append(f"{name} {stats.sharpe((r - rf)[i : j + 1]):.2f}")
        out.append(f"- Sharpe above T-bills, {era}: " + ", ".join(parts))
    c.write_result("cash-interest", "\n".join(out))


if __name__ == "__main__":
    main()
