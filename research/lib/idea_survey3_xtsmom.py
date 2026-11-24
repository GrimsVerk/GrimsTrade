"""uv run python research/lib/idea_survey3_xtsmom.py   (card: cards/xtsmom.md)

Cross-asset time-series momentum (Pitkäjärvi, Suominen, Vaittinen, JFE 2020): the stock slots
of `tsmom12` are held only while the 10-year bond's trailing return is also positive."""

from __future__ import annotations

import math
from collections.abc import Callable, Sequence
from datetime import date

import common as c
import harness
import macro
import numpy as np
import stats
import survey3_rules as r
import wide1 as w
from harness import TRAIN_LAST_BAR

from grimstrade.data import Bar

IDEA = "xtsmom"
P_BAR = 0.10 / 61  # the wide-* lineage's family: 54 + survey-2's 7 (cards/xtsmom.md)
POST = date(2017, 1, 1)  # after the paper's sample (1980-2015, maybe 2016)
STOCKS = {"SPY", "QQQ", "IWM", "EFA", "EEM", "GSPC", "N225", "FTSE", "GDAXI"}
BONDS = {"TLT", "IEF", "LQD"}
US_STOCK = {"six": "SPY", "etf": "IWM"}
WINDOWS = (
    ("1962-1979 (before the sample)", date(1962, 1, 1), date(1979, 12, 31)),
    ("1980-1993 (in sample)", date(1980, 1, 1), date(1993, 12, 31)),
    ("1994-2015 (in sample)", date(1994, 1, 1), date(2015, 12, 31)),
    ("2016 (maybe in sample)", date(2016, 1, 1), date(2016, 12, 31)),
    ("2017 to end of train (after)", POST, c.TRAIN_END),
)
CHECK_DAYS = [date(1999, 10, 1), date(2008, 10, 10), date(2018, 12, 21), date(2023, 6, 2)]

Signal = Callable[[c.View, str], bool | None]
_steps: dict[int, macro.Step] = {}


def bond_step(lookback: int) -> macro.Step:
    """Trailing return of the 10-year par bond from `DGS10`, usable from the day after."""
    if lookback not in _steps:
        recs = [x for x in macro.market_records("DGS10") if x.obs <= TRAIN_LAST_BAR]
        days = [x.obs for x in recs]
        tr = r.trailing(days, r.bond_returns(days, [x.value for x in recs]), lookback)
        _steps[lookback] = macro.Step(r.usable_from(days), tr)
    return _steps[lookback]


def y10_up(lookback: int) -> Signal:
    def f(view: c.View, s: str) -> bool | None:
        d = w.last_session(view, s)
        v = bond_step(lookback).at(d) if d is not None else math.nan
        return None if math.isnan(v) else v > 0

    return f


def tlt_up(view: c.View, s: str) -> bool | None:
    v = c.trailing_logret(view, "TLT", 365) if "TLT" in view.syms else math.nan
    return None if math.isnan(v) else v > 0


def xt(signal: Signal, us_stock: str | None = None) -> c.ResearchStrategy:
    """`tsmom12`; a stock slot only while `signal` says bonds trend up. With `us_stock`, also
    the paper's bond leg: a bond slot only while that stock's 365-day return is negative."""
    base = c.slots(c.tsmom_signal)

    def f(view: c.View) -> c.Weights:
        held = base(view)
        out = dict(held)
        for s in held:
            if s in STOCKS and signal(view, s) is False:
                del out[s]
            elif us_stock and s in BONDS:
                v = c.trailing_logret(view, us_stock, 365)
                if not math.isnan(v) and v >= 0:
                    del out[s]
        return out

    return c.weekly(f)


def window_diff(p: harness.Run, t: harness.Run, a: date, b: date) -> float:
    lo, hi = max(a, p.days[0], t.days[0]), min(b, p.days[-1], t.days[-1])
    if (hi - lo).days < 200:
        return math.nan
    return stats.sharpe(p.rets_between(lo, hi)) - stats.sharpe(t.rets_between(lo, hi))


def windows_line(name: str, p: harness.Run, t: harness.Run) -> str:
    cells = [window_diff(p, t, a, b) for _, a, b in WINDOWS]
    return f"| {name} | " + " | ".join("-" if math.isnan(x) else f"{x:+.3f}" for x in cells) + " |"


def welch(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 3 or len(b) < 3:
        return math.nan
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return float((a.mean() - b.mean()) / se) if se > 0 else math.nan


def study(sym: str, bars: Sequence[Bar], lookback: int, kind: str) -> tuple[list[str], dict]:
    """On days the asset's own 365-day return is up: mean next-interval return (bps) split by
    the bond signal. `open`: open(d+1) -> open(d+2); `close`: close(d) -> close(d+1)."""
    days = [b.date for b in bars]
    ords = np.array([d.toordinal() for d in days])
    lc = np.log(np.array([b.close for b in bars]))
    lo = np.log(np.array([b.open for b in bars]))
    step = bond_step(lookback)
    lines, got = [], {}
    for name, a, b in WINDOWS:
        up, dn = [], []
        for i in range(len(days) - 2):
            if not a <= days[i] <= b:
                continue
            j = int(np.searchsorted(ords, days[i].toordinal() - 365, side="right")) - 1
            if j < 0 or ords[0] > days[i].toordinal() - 365 or lc[i] - lc[j] <= 0:
                continue
            v = step.at(days[i])
            if math.isnan(v):
                continue
            x = lo[i + 2] - lo[i + 1] if kind == "open" else lc[i + 1] - lc[i]
            (up if v > 0 else dn).append(x * 1e4)
        if not up and not dn:
            continue
        u, d_ = np.array(up), np.array(dn)
        t = welch(u, d_)
        um = u.mean() if len(u) else math.nan
        dm = d_.mean() if len(d_) else math.nan
        lines.append(
            f"| {sym} ({kind}) | {name} | {len(u)} / {len(d_)} | {um:+.1f} | {dm:+.1f} | "
            f"{um - dm:+.1f} ({t:+.2f}) |"
        )
        got[name] = (um - dm, t)
    return lines, got


def main() -> None:
    six, etf, idx = c.ctx("six"), c.ctx("etf"), c.ctx("idx")
    variants: list[tuple[str, c.ResearchStrategy, c.ResearchStrategy | None]] = [
        ("xtsmom", xt(y10_up(365)), xt(y10_up(365))),
        ("xtsmom-b6", xt(y10_up(182)), xt(y10_up(182))),
        ("xtsmom-full", xt(y10_up(365), "SPY"), None),
    ]
    if not c.DRY:  # no look-ahead: the fast path equals gym.backtest on sample Fridays
        for _, strat, _ in variants:
            harness.check_against_gym(strat, six.hist, CHECK_DAYS)
        harness.check_against_gym(xt(y10_up(365), "IWM"), etf.hist, CHECK_DAYS[1:])

    out = ["# xtsmom: stock slots only while bonds also trend up", ""]
    out += ["Card: `cards/xtsmom.md`. Survey: `survey-2.md` (S5), `survey-3.md`. Protocol: "
            "`protocol.md`. No-look-ahead check against `gym.backtest` on "
            + ", ".join(str(d) for d in CHECK_DAYS) + ": passed.", ""]  # fmt: skip
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    runs = {name: c.go(IDEA, name, s, six, "variant") for name, s, _ in variants}
    tlt = c.go(IDEA, "xtsmom-tlt", xt(tlt_up), six, "robustness")
    allr = [*runs.values(), tlt, twin, ew]
    out += ["## The six live assets, train period", "", c.table(allr, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(allr), ""]

    t_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    t_i = c.go("baselines", "tsmom12", twin_s, idx, "baseline", log=False)
    oe = {
        "xtsmom": c.go(IDEA, "xtsmom", xt(y10_up(365)), etf, "robustness"),
        "xtsmom-b6": c.go(IDEA, "xtsmom-b6", xt(y10_up(182)), etf, "robustness"),
        "xtsmom-full": c.go(IDEA, "xtsmom-full", xt(y10_up(365), "IWM"), etf, "robustness"),
    }
    oi = {
        "xtsmom": c.go(IDEA, "xtsmom", xt(y10_up(365)), idx, "robustness"),
        "xtsmom-b6": c.go(IDEA, "xtsmom-b6", xt(y10_up(182)), idx, "robustness"),
    }
    oi["xtsmom-full"] = oi["xtsmom"]  # no bond in the index set: the bond leg does not apply

    out += ["## In the paper's years and after: Sharpe minus the twin's, by window", ""]
    out += ["| Run | " + " | ".join(n for n, _, _ in WINDOWS) + " |",
            "|---|" + "---:|" * len(WINDOWS)]  # fmt: skip
    for name, run in runs.items():
        out.append(windows_line(f"{name} (six)", run, twin))
    out.append(windows_line("xtsmom-tlt (six, robustness)", tlt, twin))
    for name, run in oe.items():
        out.append(windows_line(f"{name} (ETFs)", run, t_e))
    for name in ("xtsmom", "xtsmom-b6"):
        out.append(windows_line(f"{name} (indexes)", oi[name], t_i))
    out += ["", "(`-`: the run has no days, or fewer than 200, in that window.)", ""]

    out += ["## Event study (descriptive): own trend up, split by the bond signal, bps a day", ""]
    out += ["Mean daily log return on days the asset's own 365-day return is positive, by the "
            "10-year bond's trailing return as of the day before (up / down); spread = up minus "
            "down (Welch t). SPY: next open to next open (what a decision after day d holds). "
            "S&P 500 index: close to close (its early opens are unreliable).", ""]  # fmt: skip
    out += ["| Asset | Window | n up / down | up | down | spread (t) |",
            "|---|---|---:|---:|---:|---:|"]  # fmt: skip
    gspc = c.ctx("GSPC")
    spreads = {}
    for lb, tag in ((365, "12m"), (182, "6m")):
        out.append(f"| **bond look-back {tag}** | | | | | |")
        sl, sg = study("SPY", six.hist["SPY"], lb, "open")
        gl, _ = study("GSPC", gspc.hist["GSPC"], lb, "close")
        out += [*gl, *sl]
        spreads[lb] = sg[WINDOWS[4][0]]
    out.append("")

    de, dt = c.describe(ew), c.describe(twin)
    post_name = WINDOWS[4][0]
    for name, run in runs.items():
        vs = w.versus(run, twin)
        dv = c.describe(run)
        se, si = w.versus(oe[name], t_e)["diff"], w.versus(oi[name], t_i)["diff"]
        post = w.since(run, twin, POST)
        d = vs["diff"]
        bars = [
            (f"1. Beats twin `tsmom12` with p < {P_BAR:.5f} (0.10 / 61)",
             d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
            (f"2. Ahead of the twin in at least 4 of {vs['eras']:.0f} eras",
             vs["ahead"] >= 4, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
            ("3. Max drawdown not more than 5 points worse than the twin's",
             dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
            ("4. Positive on the ETF and index sets", se > 0 and si > 0,
             f"etf {se:+.3f}, idx {si:+.3f}"),
            ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
             f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
            ("6. (card) Not behind the twin from 2017-01-01", post >= 0, f"{post:+.3f}"),
        ]  # fmt: skip
        if name != "xtsmom-full":
            sp, st = spreads[182 if name == "xtsmom-b6" else 365]
            txt7 = f"7. (card) SPY up-trend days {post_name}: bond-up minus bond-down > 0, t >= 2"
            bars.append((txt7, sp > 0 and st >= 2, f"{sp:+.1f} bps a day, t {st:+.2f}"))
        out += [f"## Pass bar: `{name}`", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
