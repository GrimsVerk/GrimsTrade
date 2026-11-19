"""uv run python research/lib/idea_wide4_tax_drain.py
(card: cards/tax-drain.md; needs `python -I research/lib/wide4_dts.py` to have been run once)"""

from __future__ import annotations

import csv
import math
from collections.abc import Callable, Sequence
from datetime import date

import common as c
import macro
import numpy as np
import wide1 as w
import wide4_rules as r

IDEA = "tax-drain"
P_BAR = 0.10 / 49  # the list of 46 plus wide-3's three new mechanisms (cards/tax-drain.md)
GATED = {"six": ("SPY", "QQQ", "TLT"), "etf": ("IWM", "VNQ", "IEF", "LQD"), "idx": ("GSPC",)}
CAL = {"six": "SPY", "etf": "IWM", "idx": "GSPC"}
MAIN = (r.TGA_START, date(2099, 12, 31))
PLACEBO = (date(1990, 1, 1), r.TTL_END)
REGIMES: dict[str, Callable[[date], bool]] = {
    "A (TT&L era, placebo)": lambda d: r.regime(d) == "A",
    "B (TGA era, abundant reserves)": lambda d: r.regime(d) == "B",
    "C (TGA era, reserves shrinking)": lambda d: r.regime(d) == "C",
    "B+C (TGA era)": lambda d: r.regime(d) in ("B", "C"),
    "C, quarterly corporate dates only": lambda d: r.regime(d) == "C" and d.month in (4, 6, 9, 12),
}


def out_set(universe: str, active: tuple[date, date]) -> set[date]:
    cal = w.calendar(CAL[universe]) if universe != "idx" else _gspc_cal()
    ds = r.tax_sessions(cal, r.statutory_dates(cal[0].year, cal[-1].year))
    return r.out_sessions(cal, ds, active)


_gspc: list[date] = []


def _gspc_cal() -> list[date]:
    if not _gspc:
        _gspc.extend(b.date for b in c.ctx("idx").hist["GSPC"])
    return _gspc


def gated(universe: str, active: tuple[date, date]) -> c.ResearchStrategy:
    """The weekly `tsmom12` book with the gated slots empty after the close of D-2 .. D+2."""
    base = c.weekly(c.slots(c.tsmom_signal))
    out = out_set(universe, active)
    syms = GATED[universe]

    def f(view: c.View) -> c.Weights:
        held = base(view)
        last = w.last_session(view, CAL[universe])
        if last is not None and last in out:
            return {s: x for s, x in held.items() if s not in syms}
        return held

    return f


def study(name: str, cal: Sequence[date], level: np.ndarray, lo: int, hi: int, log: bool,
          scale: float, unit: str) -> tuple[list[str], dict[str, tuple[float, float]]]:  # fmt: skip
    ds = r.tax_sessions(cal, r.statutory_dates(cal[0].year, cal[-1].year))
    lines, got = [], {}
    for reg, keep in REGIMES.items():
        x = r.window_excess(cal, level, ds, keep, lo, hi, log) * scale
        if len(x) < 3:
            lines.append(f"| {name} | {reg} | {len(x)} | - | - |")
            got[reg] = (math.nan, math.nan)
            continue
        t = w.tstat(x)
        lines.append(f"| {name} | {reg} | {len(x)} | {x.mean():+.1f} {unit} | {t:+.2f} |")
        got[reg] = (float(x.mean()), t)
    return lines, got


def tga_series() -> tuple[list[date], np.ndarray]:
    path = macro.cache_root() / "derived" / "wide-4" / "tga.csv"
    days, vals = [], []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if d <= c.TRAIN_END:
                days.append(d)
                vals.append(float(row["tga"]))
    return days, np.array(vals)


def main() -> None:
    out = ["# tax-drain: step out of stocks and long bonds while tax receipts drain reserves", ""]
    out += ["Card: `cards/tax-drain.md`. Protocol: `protocol.md`.", ""]
    six = c.ctx("six")
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "drain", gated("six", MAIN), six, "variant")
    plc = c.go(IDEA, "drain-ttl", gated("six", PLACEBO), six, "robustness")
    runs = [run, plc, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin, "2000-09")
    vp = w.versus(plc, twin)
    since = w.since(run, twin, r.TGA_START)
    out += [f"Sharpe difference to `tsmom12` from {r.TGA_START}: {since:+.3f}. "
            f"Placebo `drain-ttl`: {vp['diff']:+.3f} (p {vp['p']:.2f}).", ""]  # fmt: skip
    n_out = len([d for d in out_set("six", MAIN) if d <= c.TRAIN_END])
    out += [f"Decision days with the gate on (TGA era): {n_out}.", ""]

    out += ["## First stage (descriptive): does the Treasury's account at the Fed rise?", ""]
    out += ["Change in the TGA's closing balance from session D-2 to D+1 (Daily Treasury "
            "Statement, from 2005-10-03), minus the average 3-session change of the same "
            "regime.", ""]  # fmt: skip
    out += ["| Series | Regime | Tax dates | Excess | t |", "|---|---|---:|---:|---:|"]
    tcal, tlev = tga_series()
    lines, fs = study("TGA", tcal, tlev, 2, 1, False, 1.0, "$bn")
    out += [*lines, ""]

    out += ["## Event study (descriptive): sessions D-1 .. D+3, close to close", ""]
    out += ["Log return from the close of D-2 to the close of D+3, minus the average 5-session "
            "return of the same regime.", ""]  # fmt: skip
    out += ["| Series | Regime | Tax dates | Excess | t |", "|---|---|---:|---:|---:|"]
    etf = c.ctx("etf")
    hists = {"SPY": six.hist["SPY"], "TLT": six.hist["TLT"], "IEF": etf.hist["IEF"],
             "LQD": etf.hist["LQD"]}  # fmt: skip
    ev: dict[str, dict[str, tuple[float, float]]] = {}
    for sym, bars in hists.items():
        cal = [b.date for b in bars]
        lines, ev[sym] = study(sym, cal, np.array([b.close for b in bars]), 2, 3, True, 1e4,
                               "bps")  # fmt: skip
        out += lines
    out += [""]
    a_t = fs["A (TT&L era, placebo)"]
    bc_t = fs["B+C (TGA era)"]
    ok_a = bc_t[0] > a_t[0] and bc_t[1] >= 2
    spy = ev["SPY"]
    bc, cc, aa = spy["B+C (TGA era)"], spy["C (TGA era, reserves shrinking)"], spy[
        "A (TT&L era, placebo)"]  # fmt: skip
    ok_b = (bc[0] < 0 and bc[1] <= -2) or (cc[0] < 0 and cc[1] <= -2)
    ok_c = aa[0] >= bc[0]
    out += [f"Card's reading: (a) first stage {'yes' if ok_a else 'no'}; (b) SPY negative with "
            f"t <= -2 in B+C or C {'yes' if ok_b else 'no'}; (c) placebo A not more negative "
            f"{'yes' if ok_c else 'no'}. Mechanism **"
            f"{'supported' if ok_a and ok_b and ok_c else 'not supported'}**.", ""]  # fmt: skip

    out += ["## Out of universe", ""]
    signs: dict[str, float] = {}
    for name in ("etf", "idx"):
        u = etf if name == "etf" else c.ctx(name)
        t = c.go("baselines", "tsmom12", twin_s, u, "baseline", log=False)
        a = c.go(IDEA, "drain", gated(name, MAIN), u, "robustness")
        out += [c.table([a, t], t, eras=False), ""]
        signs[name] = w.versus(a, t)["diff"]

    dv, dt, de = c.describe(run), c.describe(twin), c.describe(ew)
    d = vs["diff"]
    bars = [
        (f"1. `drain` beats twin `tsmom12` with p < {P_BAR:.4f} (0.10 / 49)",
         d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in at least 3 of {vs['eras']:.0f} eras (from 2000-09)",
         vs["ahead"] >= 3, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and positive on both out-of-universe sets",
         d > 0 and all(x > 0 for x in signs.values()),
         ", ".join(f"{k} {v:+.3f}" for k, v in signs.items())),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) Gain over the twin larger than the placebo `drain-ttl`'s",
         d > vp["diff"], f"{d:+.3f} vs {vp['diff']:+.3f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `drain`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
