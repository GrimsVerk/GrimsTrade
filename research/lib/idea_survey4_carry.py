"""uv run python research/lib/idea_survey4_carry.py   (card: cards/ts-carry.md)

Time-series carry (Koijen, Moskowitz, Pedersen, Vrugt, JFE 2018; Baltussen, Swinkels, van Vliet,
JFE 2021): a stock or bond slot of `tsmom12` is held only while the asset's carry (dividend
yield or 10-year yield, minus the T-bill yield) is above a cut-off."""

from __future__ import annotations

import csv
import math
from collections.abc import Sequence
from datetime import date, timedelta

import cash_interest
import common as c
import harness
import macro
import numpy as np
import stats
import survey3_rules as r3
import survey4_rules as r
import wide1 as w
from harness import TRAIN_LAST_BAR

from grimstrade import data
from grimstrade.data import Bar

IDEA = "ts-carry"
P_BAR = 0.10 / 65  # the wide-* lineage's family: 61 + survey-4's 4 (cards/ts-carry.md)
POST = date(2012, 10, 1)  # after the paper's sample (ends 2012-09)
EQUITY = {"SPY", "QQQ", "IWM", "EFA", "EEM", "VNQ", "GSPC"}
BOND = {"TLT", "IEF", "LQD"}
# Run 1 (2026-11-18 22:13) logged every row, but `gate` returned a numpy bool, so `carry-mean`
# never gated and its three rows equal the twin. Rows of the other configurations were correct
# (their cut-off is a Python float); in the rerun they are re-scored without a new row.
LOGGED_OK = {"carry", "carry-bond", "carry-equity", "carry@etf", "carry@GSPC"}
CHECK_DAYS = [date(1999, 10, 1), date(2008, 10, 10), date(2018, 12, 21), date(2023, 6, 2)]

_carry: dict[str, macro.Step] = {}
_mean: dict[str, macro.Step] = {}


def _cut(bars: Sequence[Bar]) -> list[Bar]:
    return [b for b in bars if b.date <= TRAIN_LAST_BAR]


def bill() -> macro.Step:
    """13-week T-bill yield (Yahoo ^IRX), a close on day x usable from x + 1."""
    bars = _cut(data.load(harness.RESEARCH, "IRX"))
    days = [b.date for b in bars]
    return macro.Step(r3.usable_from(days), [b.close / 100 for b in bars])


def y10() -> macro.Step:
    recs = [x for x in macro.market_records("DGS10") if x.obs <= TRAIN_LAST_BAR]
    return macro.Step(r3.usable_from([x.obs for x in recs]), [x.value / 100 for x in recs])


def shiller_div() -> macro.Step:
    """Shiller's annual dividend rate for month m, usable from the first day of month m + 4."""
    path = macro.cache_root() / "derived" / "survey-4" / "shiller_div.csv"
    days, vals = [], []
    with path.open() as f:
        for row in csv.DictReader(f):
            y, m = (int(x) for x in row["month"].split("-"))
            m += 4
            y, m = y + (m - 1) // 12, (m - 1) % 12 + 1
            days.append(date(y, m, 1))
            vals.append(float(row["div"]))
    return macro.Step(days, vals)


def build(sym: str) -> None:
    """Carry and its running mean at each session of `sym` (train bars only)."""
    if sym in _carry:
        return
    b = bill()
    raw = _cut(data.load(harness.RESEARCH, sym))
    days = [x.date for x in raw]
    if sym in BOND:
        y = y10()
        vals = [y.at(d) - b.at(d) for d in days]
    elif sym == "GSPC":
        dv = shiller_div()
        vals = [dv.at(x.date) / x.close - b.at(x.date) for x in raw]
    else:
        adj_bars = _cut(harness._load_csv(harness.DATA / "adj" / f"{sym}.csv"))
        adj = {x.date: x.close for x in adj_bars}
        rc = [x.close for x in raw]
        divs = r.dividends(days, rc, [adj[d] for d in days])
        dy = r.trailing_yield(days, rc, divs)
        vals = [float(dy[i]) - b.at(d) for i, d in enumerate(days)]
    _carry[sym] = macro.Step(days, vals)
    _mean[sym] = macro.Step(days, list(r.running_mean(vals)))


def carry_at(sym: str, d: date, mean: bool = False) -> tuple[float, float]:
    """(carry, cut-off) as of session d; cut-off 0 or the running mean."""
    build(sym)
    v = _carry[sym].at(d)
    return v, (_mean[sym].at(d) if mean else 0.0)


def gate(view: c.View, s: str, mean: bool) -> bool | None:
    """True if the slot may be held, False if carry says cash, None if no gate applies."""
    d = w.last_session(view, s)
    if d is None:
        return None
    v, cut = carry_at(s, d, mean)
    if math.isnan(v) or math.isnan(cut):
        return None
    return bool(v > cut)  # a numpy bool would never be `is False` (bug fixed 2026-11-18)


ALL_LEGS = frozenset(EQUITY | BOND)


def strat(mean: bool = False, legs: frozenset[str] = ALL_LEGS) -> c.ResearchStrategy:
    base = c.slots(c.tsmom_signal)

    def f(view: c.View) -> c.Weights:
        held = base(view)
        return {s: x for s, x in held.items() if not (s in legs and gate(view, s, mean) is False)}

    return c.weekly(f)


def go(name: str, s: c.ResearchStrategy, ctx: c.Ctx, kind: str) -> harness.Run:
    tag = name if ctx.name == "six" else f"{name}@{ctx.name}"
    return c.go(IDEA, name, s, ctx, kind, log=tag not in LOGGED_OK)


def welch(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) < 3 or len(b) < 3:
        return math.nan
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return float((a.mean() - b.mean()) / se) if se > 0 else math.nan


def study(
    sym: str, bars: Sequence[Bar], windows: Sequence[tuple[str, date, date]], kind: str, mean: bool
) -> tuple[list[str], dict[str, tuple[float, float]]]:
    """On days the asset's own 365-day return is up: mean next-interval return (bps a day) with
    carry above vs not above the cut-off. `open`: open(d+1) -> open(d+2); `close`: d -> d+1."""
    days = [x.date for x in bars]
    ords = np.array([d.toordinal() for d in days])
    lc = np.log(np.array([x.close for x in bars]))
    lo = np.log(np.array([x.open for x in bars]))
    lines, got = [], {}
    for name, a, b in windows:
        up, dn = [], []
        for i in range(len(days) - 2):
            if not a <= days[i] <= b:
                continue
            j = int(np.searchsorted(ords, ords[i] - 365, side="right")) - 1
            if ords[0] > ords[i] - 365 or lc[i] - lc[j] <= 0:
                continue
            v, cut = carry_at(sym, days[i], mean)
            if math.isnan(v) or math.isnan(cut):
                continue
            x = lo[i + 2] - lo[i + 1] if kind == "open" else lc[i + 1] - lc[i]
            (up if v > cut else dn).append(x * 1e4)
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


def removed(run: harness.Run, twin: harness.Run, syms: Sequence[str]) -> str:
    """Share of the twin's held days per asset that the variant holds in cash."""
    a = {d.time.date(): d.weights for d in twin.decisions}
    b = {d.time.date(): d.weights for d in run.decisions}
    parts = []
    for s in syms:
        held = [k for k, wt in a.items() if wt.get(s, 0) > 0]
        if held:
            out = sum(1 for k in held if b.get(k, {}).get(s, 0) == 0)
            parts.append(f"{s} {out / len(held):.0%}")
    return ", ".join(parts)


def above_bills(run: harness.Run, days: list[date], ys: list[float]) -> float:
    rr, rf = cash_interest.rescored(run, days, ys)
    return float(stats.sharpe(rr - rf))


def main() -> None:
    six, etf, gspc = c.ctx("six"), c.ctx("etf"), c.ctx("GSPC")
    eq_legs = frozenset(EQUITY)
    bond_legs = frozenset(BOND)
    variants = [("carry", strat(False)), ("carry-mean", strat(True))]
    if not c.DRY:  # no look-ahead: the fast path equals gym.backtest on sample Fridays
        for _, s in variants:
            harness.check_against_gym(s, six.hist, CHECK_DAYS)
        harness.check_against_gym(strat(False), etf.hist, CHECK_DAYS[1:])

    out = ["# ts-carry: stock and bond trend slots only while carry is positive", ""]
    out += ["Card: `cards/ts-carry.md`. Survey: `survey-4.md` (pick A). Protocol: `protocol.md`. "
            "No-look-ahead check against `gym.backtest` on "
            + ", ".join(str(d) for d in CHECK_DAYS) + ": passed.", ""]  # fmt: skip
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    runs = {name: go(name, s, six, "variant") for name, s in variants}
    rb = go("carry-bond", strat(False, bond_legs), six, "robustness")
    re_ = go("carry-equity", strat(False, eq_legs), six, "robustness")
    allr = [*runs.values(), rb, re_, twin, ew]
    out += ["## The six live assets, train period", "", c.table(allr, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(allr), ""]

    out += ["Share of `tsmom12`'s held days that each run holds in cash instead:", ""]
    for run in [*runs.values(), rb, re_]:
        out.append(f"- `{run.variant}`: {removed(run, twin, ['SPY', 'QQQ', 'TLT'])}")
    out.append("")

    bd, by = cash_interest.bill_yield()
    out += ["Sharpe above T-bills with T-bill interest on cash (`cash_interest.rescored`; no row):",
            ""]  # fmt: skip
    for run in [*runs.values(), rb, re_, twin, ew]:
        sp = above_bills(run, bd, by)
        out.append(f"- `{run.variant}`: {sp:.2f} (gym: {stats.sharpe(run.rets):.2f})")
    out.append("")

    t_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    t_g = c.go("baselines", "tsmom12", twin_s, gspc, "baseline", log=False)
    oe = {n: go(n, strat(n == "carry-mean"), etf, "robustness") for n, _ in variants}
    og = {n: go(n, strat(n == "carry-mean"), gspc, "robustness") for n, _ in variants}
    out += ["## Out of universe", "", "Other ETFs:", "", c.table([*oe.values(), t_e], t_e), ""]
    out += ["S&P 500 index alone, 1962-1993 (Shiller dividends, 3-month lag):", "",
            c.table([*og.values(), t_g], t_g, eras=False), ""]  # fmt: skip

    out += ["## Before, in and after the paper's sample: Sharpe minus the twin's", ""]
    out += ["| Run | 1994 - 2012-09 (in sample) | 2012-10 to end of train (after) |",
            "|---|---:|---:|"]  # fmt: skip
    for run in [*runs.values(), rb, re_]:
        lo, hi = run.days[0], POST - timedelta(days=1)
        pre = stats.sharpe(run.rets_between(lo, hi)) - stats.sharpe(twin.rets_between(lo, hi))
        out.append(f"| {run.variant} | {pre:+.3f} | {w.since(run, twin, POST):+.3f} |")
    out.append("")

    out += ["## Event study (descriptive): own trend up, split by carry, bps a day", ""]
    out += ["Mean daily log return on days the asset's own 365-day return is positive, by carry "
            "above / not above the cut-off as of that day; spread = above minus not above (Welch "
            "t). ETFs: next open to next open (what a decision after day d holds). S&P 500 "
            "index: close to close.", ""]  # fmt: skip
    out += ["| Asset | Window | n above / not | above | not | spread (t) |",
            "|---|---|---:|---:|---:|---:|"]  # fmt: skip
    w_etf = [("1994 - 2012-09 (in sample)", date(1994, 1, 1), POST - timedelta(days=1)),
             ("2012-10 to end of train (after)", POST, c.TRAIN_END)]  # fmt: skip
    w_idx = [("1962-1987 (before the sample)", date(1962, 1, 1), date(1987, 12, 31)),
             ("1988-1993 (in sample)", date(1988, 1, 1), date(1993, 1, 28))]  # fmt: skip
    post_name = w_etf[1][0]
    spreads: dict[bool, dict[str, tuple[float, float]]] = {}
    for mean, tag in ((False, "cut-off 0"), (True, "cut-off running mean")):
        out.append(f"| **{tag}** | | | | | |")
        spreads[mean] = {}
        for sym in ("SPY", "TLT"):
            ln, got = study(sym, six.hist[sym], w_etf, "open", mean)
            out += ln
            spreads[mean][sym] = got.get(post_name, (math.nan, math.nan))
        ln, _ = study("GSPC", gspc.hist["GSPC"], w_idx, "close", mean)
        out += ln
    out.append("")

    de, dt = c.describe(ew), c.describe(twin)
    for name, run in runs.items():
        vs = w.versus(run, twin)
        dv = c.describe(run)
        se, sg = w.versus(oe[name], t_e)["diff"], w.versus(og[name], t_g)["diff"]
        post = w.since(run, twin, POST)
        d = vs["diff"]
        mean = name == "carry-mean"
        (s1, t1), (s2, t2) = spreads[mean]["SPY"], spreads[mean]["TLT"]
        ok7 = s1 > 0 and s2 > 0 and max(t1, t2) >= 2
        bars = [
            (f"1. Beats twin `tsmom12` with p < {P_BAR:.5f} (0.10 / 65)",
             d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
            (f"2. Ahead of the twin in at least 4 of {vs['eras']:.0f} eras",
             vs["ahead"] >= 4, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
            ("3. Max drawdown not more than 5 points worse than the twin's",
             dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
            ("4. Positive on the ETF set and the S&P 500 index", se > 0 and sg > 0,
             f"etf {se:+.3f}, S&P 500 {sg:+.3f}"),
            ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
             f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
            ("6. (card) Not behind the twin from 2012-10-01", post >= 0, f"{post:+.3f}"),
            ("7. (card) After 2012-10: SPY and TLT carry spreads > 0, one with t >= 2", ok7,
             f"SPY {s1:+.1f} bps (t {t1:+.2f}), TLT {s2:+.1f} bps (t {t2:+.2f})"),
        ]  # fmt: skip
        out += [f"## Pass bar: `{name}`", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
