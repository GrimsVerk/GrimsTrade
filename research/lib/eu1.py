"""eu-1: `tsmom12` on European UCITS ETFs/ETCs in EUR, against the US books (card cards/eu-1.md).

    uv run --with numpy python research/lib/eu1.py

Needs the CSVs from `eu1_data.py build`. Every run is a row in tries.md (idea `eu-1`); a run whose
equity file already exists under the git-ignored research/data/runs/eu-1/ is re-scored without a
new row (so a rerun on this machine does not double-count; on a fresh machine rows are logged
again: copy that folder or accept duplicate rows). Train period only.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date

import common as c
import harness
import numpy as np
from harness import TRAIN_END, Run, load_history

from grimstrade import gym
from grimstrade.data import CRYPTO, ETF, UNIVERSE

IDEA = "eu-1"
W_START = date(2012, 1, 2)
NATIVE_START = date(2009, 1, 2)
SPLICE_START = date(2000, 1, 3)

COSTS = {
    "gym": dict(gym.COSTS),
    "nl": {ETF: gym.Costs(fee=0.0010, slip=0.0005), CRYPTO: gym.COSTS[CRYPTO]},
    "harsh": {ETF: gym.Costs(fee=0.0025, slip=0.0015), CRYPTO: gym.COSTS[CRYPTO]},
}

US6 = ["SPY", "QQQ", "GLD", "TLT", "BTC", "ETH"]
US6_EUR = [f"{s}-EUR" for s in US6]
EU6 = ["SXR8", "SXRV", "4GLD", "IBGL", "BTC-EUR", "ETH-EUR"]
EU6_IS04 = ["SXR8", "SXRV", "4GLD", "IS04", "BTC-EUR", "ETH-EUR"]
EU6_S = ["SXR8-S", "SXRV-S", "4GLD-S", "IBGL-S", "BTC-EUR", "ETH-EUR"]
USW = ["SPY", "EFA", "EEM", "IEF", "TLT", "GLD", "DBC"]
USW_EUR = [f"{s}-EUR" for s in USW]
EUW = ["SXR8", "EXSA", "IQQE", "IBGS", "IBGL", "4GLD", "EXXY"]
SINGLE_PAIRS = [("SXR8", "SPY"), ("SXRV", "QQQ"), ("4GLD", "GLD"), ("IBGL", "TLT")]

CRASHES: list[tuple[str, date, date]] = [
    ("2011 euro crisis", date(2011, 5, 2), date(2011, 10, 3)),
    ("2015-16", date(2015, 5, 21), date(2016, 2, 11)),
    ("2018-Q4", date(2018, 9, 20), date(2018, 12, 24)),
    ("2020 covid", date(2020, 2, 19), date(2020, 3, 23)),
    ("2022 rate shock", date(2022, 1, 3), date(2022, 10, 12)),
]

for _s in [*US6_EUR, *EU6, *EU6_IS04, *EU6_S, *USW_EUR, *EUW, "IWDA"]:
    if _s not in UNIVERSE:
        UNIVERSE[_s] = CRYPTO if _s in ("BTC-EUR", "ETH-EUR") else ETF

TSMOM = c.weekly(c.slots(c.tsmom_signal))
EW = c.weekly(c.equal_weight)


@dataclass
class Book:
    name: str
    syms: list[str]
    costs: str


_cache: dict[tuple[str, ...], tuple[dict[str, list[harness.Bar]], harness.Panel]] = {}


def panel_for(syms: Sequence[str]) -> tuple[dict[str, list[harness.Bar]], harness.Panel]:
    key = tuple(syms)
    if key not in _cache:
        hist = load_history("train", True, list(syms))
        _cache[key] = (hist, harness.Panel(hist))
    return _cache[key]


def go(
    variant: str, strategy: c.ResearchStrategy, syms: Sequence[str], costs: str, kind: str,
    start: date,
) -> Run:  # fmt: skip
    hist, pan = panel_for(syms)
    saved = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    log = not saved.exists()
    run = harness.run(
        IDEA, variant, strategy, kind=kind, period="train", panel=pan, history=hist,
        start=start, end=TRAIN_END, costs=COSTS[costs], log=log,
    )  # fmt: skip
    print(f"{'logged' if log else 're-scored'} {variant}", flush=True)
    return run


def pair(book: Book, start: date, suffix: str = "") -> tuple[Run, Run]:
    t = go(f"tsmom12@{book.name}{suffix}", TSMOM, book.syms, book.costs, "robustness", start)
    e = go(f"equal-weight@{book.name}{suffix}", EW, book.syms, book.costs, "baseline", start)
    return t, e


def crash_table(runs: Sequence[Run]) -> str:
    head = "| Run |" + "".join(f" {n} |" for n, _, _ in CRASHES)
    lines = [head, "|---|" + "---:|" * len(CRASHES)]
    for run in runs:
        row = f"| {run.variant} |"
        for _, a, b in CRASHES:
            r = run.rets_between(a, b)
            ok = len(r) > 5 and run.days[0] <= a
            row += f" {float(np.prod(1 + r) - 1):+.1%} |" if ok else " - |"
        lines.append(row)
    return "\n".join(lines)


def crash_ret(run: Run, a: date, b: date) -> float:
    r = run.rets_between(a, b)
    return float(np.prod(1 + r) - 1) if len(r) > 5 and run.days[0] <= a else math.nan


def criteria(eu: tuple[Run, Run], us: tuple[Run, Run]) -> tuple[list[str], str]:
    """The card's four tests for one pair. Returns table lines and the verdict."""
    (te, ee), (tu, eu_) = eu, us
    de, du = c.describe(te), c.describe(tu)
    dee, deu = c.describe(ee), c.describe(eu_)
    gap_e, gap_u = de["sharpe"] - dee["sharpe"], du["sharpe"] - deu["sharpe"]
    ok1 = abs(gap_e - gap_u) <= 0.15
    ok2 = de["mdd"] <= du["mdd"] + 0.05 and de["mdd"] < dee["mdd"]
    ratio = de["turnover"] / du["turnover"] if du["turnover"] > 0 else math.nan
    ok3 = 0.67 <= ratio <= 1.5
    inside = [(n, a, b) for n, a, b in CRASHES if a >= W_START]
    match = 0
    for _, a, b in inside:
        se = np.sign(crash_ret(te, a, b) - crash_ret(ee, a, b))
        su = np.sign(crash_ret(tu, a, b) - crash_ret(eu_, a, b))
        match += int(se == su)
    ok4 = match >= 3
    lines = [
        "| Test | EUR book | US book | Pass |",
        "|---|---:|---:|---|",
        f"| 1. Sharpe tsmom12 - EW (within 0.15) | {gap_e:+.2f} | {gap_u:+.2f} | {_yn(ok1)} |",
        f"| 2. tsmom12 max DD (<= US + 5 pts, < EUR EW {dee['mdd']:.1%}) | {de['mdd']:.1%} | "
        f"{du['mdd']:.1%} | {_yn(ok2)} |",
        f"| 3. tsmom12 turnover/yr (0.67x-1.5x; ratio {ratio:.2f}) | {de['turnover']:.2f} | "
        f"{du['turnover']:.2f} | {_yn(ok3)} |",
        f"| 4. crash sign of tsmom12 - EW matches (>= 3 of 4) | {match} of {len(inside)} | | "
        f"{_yn(ok4)} |",
    ]
    if ok1 and ok2 and ok3 and ok4:
        verdict = "holds"
    elif ok2 and ok4:
        verdict = "holds in part"
    else:
        verdict = "breaks"
    return lines, verdict


def _yn(ok: bool) -> str:
    return "yes" if ok else "**no**"


def main() -> None:
    out = ["# eu-1 results: `tsmom12` on European UCITS ETFs in EUR", ""]
    out += [
        "Train period only. Total-return prices. Sharpe on calendar days, zero risk-free rate, "
        "each book in its own currency. Costs: `gym` (ETFs 0 + 2 bps), `nl` (Dutch broker, "
        "ETFs 0.10% + 0.05%), `harsh` (ETFs 0.25% + 0.15%); coins 0.25% + 0.05% throughout. "
        "Card: `cards/eu-1.md`. Era columns are Sharpe ratios.",
        "",
    ]
    books = {
        "us6": Book("us6", US6, "gym"),
        "us6-eur": Book("us6-eur", US6_EUR, "gym"),
        "eu6": Book("eu6", EU6, "nl"),
        "usw": Book("usw", USW, "gym"),
        "usw-eur": Book("usw-eur", USW_EUR, "gym"),
        "euw": Book("euw", EUW, "nl"),
    }
    res = {k: pair(b, W_START) for k, b in books.items()}
    bh_iwda = go("hold-IWDA", c.weekly(c.hold("IWDA")), ["IWDA"], "nl", "baseline", W_START)
    bh_spy = go("hold-SPY", c.weekly(c.hold("SPY")), ["SPY"], "gym", "baseline", W_START)

    out += ["## 1. Window W, 2012-01-02 .. 2025-11-09", ""]
    for title, keys in [
        ("The live six: US in USD, US in EUR, UCITS in EUR", ["us6", "us6-eur", "eu6"]),
        ("Asset classes, no coins: US in USD, US in EUR, UCITS in EUR", ["usw", "usw-eur", "euw"]),
    ]:
        runs = [r for k in keys for r in res[k]]
        out += [f"### {title}", "", c.table(runs), ""]
    out += ["Buy and hold, for scale:", "", c.table([bh_iwda, bh_spy]), ""]

    out += ["## 2. The card's tests", ""]
    verdicts = {}
    for name, eu, us in [("A: eu6 vs us6", "eu6", "us6"), ("B: euw vs usw", "euw", "usw")]:
        lines, v = criteria(res[eu], res[us])
        verdicts[name] = v
        out += [f"### Pair {name}: **{v}**", "", *lines, ""]

    out += ["## 3. Crash windows (total return inside each, own currency)", ""]
    crash_runs = [r for k in books for r in res[k]]
    out += [crash_table([*crash_runs, bh_iwda, bh_spy]), ""]

    out += ["## 4. Costs and the bond slot", ""]
    cost_runs = [res["eu6"][0], res["euw"][0]]
    for book, syms in [("eu6", EU6), ("euw", EUW)]:
        for k in ("gym", "harsh"):
            cost_runs.append(go(f"tsmom12@{book}/{k}", TSMOM, syms, k, "robustness", W_START))
    out += [c.table(cost_runs, eras=False), ""]
    is04 = pair(Book("eu6-is04", EU6_IS04, "nl"), W_START)
    out += [
        "IS04 (US Treasuries 20+, EUR-hedged; joins 2016) in place of IBGL:",
        "",
        c.table([res["eu6"][0], *is04, res["eu6"][1]]),
        "",
    ]

    out += ["## 5. Single assets: the filter against holding, slot by slot", ""]
    singles = []
    for eu_sym, us_sym in SINGLE_PAIRS:
        for sym, costs in ((eu_sym, "nl"), (us_sym, "gym")):
            t = go(f"tsmom12@{sym}", TSMOM, [sym], costs, "robustness", W_START)
            h = go(f"hold@{sym}", c.weekly(c.hold(sym)), [sym], costs, "baseline", W_START)
            singles += [t, h]
    out += [c.table(singles, eras=False), ""]
    out += [crash_table(singles), ""]

    out += ["## 6. Longer windows (robustness only)", ""]
    euw09 = pair(Book("euw", EUW, "nl"), NATIVE_START, "-2009")
    usw09 = pair(Book("usw", USW, "gym"), NATIVE_START, "-2009")
    out += ["### Asset classes from 2009-01-02 (native UCITS histories)", ""]
    out += [c.table([*euw09, *usw09]), "", crash_table([*euw09, *usw09]), ""]
    s00 = pair(Book("eu6-S", EU6_S, "nl"), SPLICE_START, "-2000")
    u00 = pair(Book("us6", US6, "gym"), SPLICE_START, "-2000")
    out += [
        "### The six from 2000-01-03, spliced (`-S`: US ETFs in EUR before 2008-2010)",
        "",
        c.table([*s00, *u00]),
        "",
        "Crash windows, plus the house's own 2000-02 and 2008 stress windows:",
        "",
        crash_table([*s00, *u00]),
        "",
        c.stress_table([*s00, *u00]),
        "",
    ]
    out += ["## Verdicts", ""] + [f"- Pair {k}: **{v}**" for k, v in verdicts.items()]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
