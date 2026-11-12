"""The risk menu (card: research/cards/risk-map.md).

  uv run --with numpy python research/lib/risk_map.py run   # backtests: logs 20 tries
  uv run --with numpy python research/lib/risk_map.py       # tables and chart from saved runs

The second form reads the equity curves the first one saved in research/data/runs/risk-map/
(git-ignored), so the report can be rebuilt without logging tries again.
"""

from __future__ import annotations

import csv
import sys
from dataclasses import dataclass
from datetime import date

import common as c
import harness
import numpy as np
import rules
import stats

from grimstrade.data import CRYPTO, UNIVERSE

IDEA = "risk-map"
RULES = ["hold", "tsmom12", "tv60", "tv40", "tv20"]
CAPS = {"tv60": 0.60, "tv40": 0.40, "tv20": 0.20}
SIZES: dict[str, float | None] = {"c00": 0.0, "c05": 0.05, "c10": 0.10, "c17": None}
WINDOWS = [
    ("1994-2025", date(1994, 2, 1)),
    ("2003-2025", date(2003, 1, 1)),
    ("2013-2025", date(2013, 1, 1)),
]
RULE_WORDS = {
    "hold": "Hold everything",
    "tsmom12": "Trend rule",
    "tv60": "Trend, swings capped (loose)",
    "tv40": "Trend, swings capped (medium)",
    "tv20": "Trend, swings capped (tight)",
}
SIZE_WORDS = {"c00": "none", "c05": "5% per coin", "c10": "10% per coin", "c17": "a sixth per coin"}


def menu(rule: str, size: float | None) -> c.ResearchStrategy:
    cap = CAPS.get(rule)

    def f(view: c.View) -> c.Weights:
        held = c.live(view)
        if not held:
            return {}
        coins = [s for s in held if UNIVERSE[s] == CRYPTO]
        rest = [s for s in held if UNIVERSE[s] != CRYPTO]
        if size is None:
            slot = {s: 1 / len(held) for s in held}
        else:
            slot = {s: size for s in coins}
            slot.update({s: (1 - size * len(coins)) / len(rest) for s in rest})
        out = {}
        for s in held:
            w = slot[s]
            if w <= 0 or (rule != "hold" and not c.tsmom_signal(view, s)):
                continue
            out[s] = w * rules.vol_cap(view, s, cap) if cap else w
        return out

    return f


def names() -> list[tuple[str, str, str]]:
    return [(f"{r}-{z}", r, z) for r in RULES for z in SIZES]


def run_all() -> None:
    six = c.ctx("six")
    for name, r, z in names():
        out = c.go(IDEA, name, c.weekly(menu(r, SIZES[z])), six)
        print(name, f"{stats.sharpe(out.rets):.2f}", flush=True)


@dataclass
class Row:
    name: str
    rule: str
    size: str
    cagr: float
    mdd: float
    worst_year: int
    worst_year_ret: float
    under_days: int  # longest spell below an earlier high
    under_open: bool  # that spell had not ended by the last day
    sharpe: float
    vol: float


def load(name: str) -> tuple[list[date], np.ndarray]:
    path = harness.DATA / "runs" / IDEA / f"{name}.train.csv"
    with path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    return [date.fromisoformat(r["date"]) for r in rows], np.array([float(r["equity"]) for r in rows])


def measure(name: str, rule: str, size: str, days: list[date], eq: np.ndarray, start: date) -> Row:
    i = max((start - days[0]).days, 0)
    days, eq = days[i:], eq[i:]
    r = eq[1:] / eq[:-1] - 1
    peak = np.maximum.accumulate(eq)
    # longest spell below an earlier high
    best, open_, since = 0, False, 0
    for k in range(1, len(eq)):
        if eq[k] >= peak[k - 1]:
            since = k
        elif k - since > best:
            best, open_ = k - since, k == len(eq) - 1
    years: dict[int, list[float]] = {}
    for d, e in zip(days, eq, strict=True):
        years.setdefault(d.year, []).append(e)
    yr = {}
    prev = eq[0]
    for y in sorted(years):
        yr[y] = years[y][-1] / prev - 1
        prev = years[y][-1]
    wy = min(yr, key=lambda y: yr[y])
    return Row(name, rule, size, stats.cagr(r), float((1 - eq / peak).max()), wy, yr[wy], best,
               open_, stats.sharpe(r), stats.vol(r))  # fmt: skip


def span(days: int, open_: bool) -> str:
    y = days / 365.25
    s = f"{y:.1f} years" if y >= 1 else f"{round(days / 30.44)} months"
    return s + (" and counting" if open_ else "")


def rows_for(start: date) -> list[Row]:
    return [measure(n, r, z, *load(n), start) for n, r, z in names()]


def detail_table(rows: list[Row]) -> str:
    out = [
        "| Variant | Growth a year | Worst drop | Worst year | Longest below a high | Sharpe | Vol |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for x in rows:
        out.append(
            f"| {x.name} | {x.cagr:+.1%} | {x.mdd:.1%} | {x.worst_year_ret:+.1%} ({x.worst_year}) |"
            f" {span(x.under_days, x.under_open)} | {x.sharpe:.2f} | {x.vol:.1%} |"
        )
    return "\n".join(out)


def report() -> None:
    out = ["# risk-map: every choice on the menu, three windows", ""]
    out += [
        "Card: `cards/risk-map.md`. Six live assets, dividend-adjusted prices, the gym's costs,"
        " decided each Friday. One backtest per variant from 1994-02-01 to 2025-11-09; the later"
        " windows are slices of the same account, with the worst drop and the time below a high"
        " counted from the window's first day. Built by `lib/risk_map.py`.",
        "",
        "Names: `hold` always holds; `tsmom12` holds a slot only when the asset is up over a"
        " year; `tv60`, `tv40`, `tv20` add a cap on each slot's volatility (60%, 40%, 20% a"
        " year). `c00`, `c05`, `c10`: 0%, 5%, 10% in each coin; `c17`: equal slots (a sixth"
        " each once all six assets exist).",
        "",
    ]
    for label, start in WINDOWS:
        out += [f"## {label}", "", detail_table(rows_for(start)), ""]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    if sys.argv[1:] == ["run"]:
        run_all()
    report()
