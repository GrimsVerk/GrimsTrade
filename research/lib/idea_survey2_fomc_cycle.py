"""uv run python research/lib/idea_survey2_fomc_cycle.py
(card: cards/fomc-cycle.md; needs `python -I research/lib/survey2_fomc.py` to have been run)"""

from __future__ import annotations

import csv
import math
from collections.abc import Sequence
from datetime import date

import common as c
import macro
import numpy as np
import survey2_rules as r
import wide1 as w

from grimstrade.data import Bar

IDEA = "fomc-cycle"
P_BAR = 0.10 / 61  # wide-1's 54 plus survey-2's 7 candidates (cards/fomc-cycle.md)
POST = date(2017, 1, 1)  # after the published sample (1994-2016)
STOCKS = {"SPY", "QQQ", "IWM", "EFA", "EEM", "GSPC", "N225", "FTSE", "GDAXI"}
PERIODS = (
    ("1994-2013 (first draft's sample)", date(1994, 1, 1), date(2013, 12, 31)),
    ("2014-2016 (authors' holdout)", date(2014, 1, 1), date(2016, 12, 31)),
    ("2017 to end of train (after publication)", POST, c.TRAIN_END),
)

_day0s: list[date] = []
_labels: dict[tuple[str, date], bool | None] = {}


def day0s() -> list[date]:
    if not _day0s:
        path = macro.cache_root() / "derived" / "survey-2" / "fomc.csv"
        with path.open(newline="") as f:
            _day0s.extend(sorted(date.fromisoformat(x["day0"]) for x in csv.DictReader(f)))
    return _day0s


def next_label(view: c.View, sym: str) -> bool | None:
    """Label of the session a decision now fills on (the next session of `sym`)."""
    d = w.last_session(view, sym)
    if d is None:
        return None
    key = (sym, d)
    if key not in _labels:
        nxt = r.next_session(w.calendar(sym), d)
        _labels[key] = None if nxt is None else r.label(nxt, day0s())
    return _labels[key]


def gate(even: bool) -> c.ResearchStrategy:
    """`tsmom12`; a stock slot is kept only when its next session is in an `even` week."""
    base = c.weekly(c.slots(c.tsmom_signal))

    def f(view: c.View) -> c.Weights:
        held = base(view)
        out = dict(held)
        for s in held:
            if s in STOCKS:
                lab = next_label(view, s)
                if lab is not None and lab != even:
                    del out[s]
        return out

    return f


def overlay() -> c.ResearchStrategy:
    """`tsmom12` plus the idle cash, in equal parts, in the eligible stock assets whose next
    session is in an even week."""
    base = c.weekly(c.slots(c.tsmom_signal))

    def f(view: c.View) -> c.Weights:
        held = base(view)
        idle = 1.0 - sum(held.values())
        tgt = [s for s in view.syms if s in STOCKS and c.eligible(view, s)]
        tgt = [s for s in tgt if next_label(view, s) is True]
        if idle <= 1e-9 or not tgt:
            return held
        out = dict(held)
        for s in tgt:
            out[s] = out.get(s, 0.0) + idle / len(tgt)
        return out

    return f


def welch(a: np.ndarray, b: np.ndarray) -> float:
    se = math.sqrt(a.var(ddof=1) / len(a) + b.var(ddof=1) / len(b))
    return float((a.mean() - b.mean()) / se) if se > 0 else math.nan


def study(sym: str, bars: Sequence[Bar]) -> tuple[list[str], dict[str, float]]:
    days = [b.date for b in bars]
    lc = np.log(np.array([b.close for b in bars]))
    lo = np.log(np.array([b.open for b in bars]))
    lab = [r.label(d, day0s()) for d in days]
    lines, got = [], {}
    for name, a, b in PERIODS:
        row = f"| {sym} | {name} |"
        for kind in ("close", "open"):
            ev, od = [], []
            for i in range(1, len(days) - 1):
                if not a <= days[i] <= b or lab[i] is None:
                    continue
                # close: close(i-1) -> close(i); open: open(i) -> open(i+1), the interval a
                # decision after session i-1 holds
                x = lc[i] - lc[i - 1] if kind == "close" else lo[i + 1] - lo[i]
                (ev if lab[i] else od).append(x * 1e4)
            e, o = np.array(ev), np.array(od)
            t = welch(e, o)
            row += f" {len(e)} / {len(o)} | {e.mean():+.1f} | {o.mean():+.1f} | "
            row += f"{e.mean() - o.mean():+.1f} ({t:+.2f}) |"
            got[f"{name}:{kind}:spread"], got[f"{name}:{kind}:t"] = e.mean() - o.mean(), t
        lines.append(row)
    return lines, got


def main() -> None:
    out = ["# fomc-cycle: stock slots only in even weeks of the FOMC cycle", ""]
    out += ["Card: `cards/fomc-cycle.md`. Survey and ranking: `survey-2.md`. Protocol: "
            "`protocol.md`.", ""]  # fmt: skip
    ds = day0s()
    out += [f"Scheduled FOMC announcement days used: {len(ds)}, {ds[0]} .. {ds[-1]}.", ""]
    six = c.ctx("six")
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    g = c.go(IDEA, "even-gate", gate(True), six, "variant")
    ov = c.go(IDEA, "even-overlay", overlay(), six, "variant")
    plc = c.go(IDEA, "odd-gate", gate(False), six, "robustness")
    runs = [g, ov, plc, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    post = {x.variant: w.since(x, twin, POST) for x in (g, ov, plc)}
    out += ["Sharpe minus the twin's from 2017-01-01 (after the published sample): "
            + ", ".join(f"`{k}` {v:+.3f}" for k, v in post.items()) + ".", ""]  # fmt: skip

    out += ["## Event study (descriptive): mean daily log return in even and odd weeks, bps", ""]
    out += ["Close = close-to-close (the paper's measure); open = next open to next open (what "
            "our fills earn), labelled by the session it starts on. Spread = even minus odd "
            "(Welch t).", ""]  # fmt: skip
    head = "| Asset | Period | close: n even / odd | even | odd | spread (t) |"
    head += " open: n even / odd | even | odd | spread (t) |"
    out += [head, "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    sl, sg = study("SPY", six.hist["SPY"])
    ql, _ = study("QQQ", six.hist["QQQ"])
    out += [*sl, *ql, ""]

    out += ["## Out of universe", ""]
    etf, idx = c.ctx("etf"), c.ctx("idx")
    t_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    g_e = c.go(IDEA, "even-gate", gate(True), etf, "robustness")
    o_e = c.go(IDEA, "even-overlay", overlay(), etf, "robustness")
    out += ["Other ETFs (gate on IWM, EFA, EEM):", "", c.table([g_e, o_e, t_e], t_e, False), ""]
    t_i = c.go("baselines", "tsmom12", twin_s, idx, "baseline", log=False)
    g_i = c.go(IDEA, "even-gate", gate(True), idx, "robustness")
    o_i = c.go(IDEA, "even-overlay", overlay(), idx, "robustness")
    out += ["Four indexes as one portfolio (gate on all four from 1994-02):", "",
            c.table([g_i, o_i, t_i], t_i, False), ""]  # fmt: skip

    de, dp = c.describe(ew), c.describe(plc)
    dt = c.describe(twin)
    for run, oe, oi, extra in ((g, g_e, g_i, True), (ov, o_e, o_i, False)):
        vs = w.versus(run, twin)
        dv = c.describe(run)
        d = vs["diff"]
        se, si = w.versus(oe, t_e)["diff"], w.versus(oi, t_i)["diff"]
        spread, st = sg[f"{PERIODS[2][0]}:close:spread"], sg[f"{PERIODS[2][0]}:close:t"]
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
            ("6. (card) Not behind the twin from 2017-01-01", post[run.variant] >= 0,
             f"{post[run.variant]:+.3f}"),
        ]  # fmt: skip
        if extra:
            ok7 = spread > 0 and st >= 2
            txt7 = "7. (card) SPY close-to-close spread from 2017 > 0 with t >= 2"
            bars.append((txt7, ok7, f"{spread:+.1f} bps a day, t {st:+.2f}"))
        ok8 = dv["sharpe"] > dp["sharpe"]
        txt8 = "8. (card) Beats the placebo `odd-gate` on Sharpe"
        bars.append((txt8, ok8, f"{dv['sharpe']:.3f} vs {dp['sharpe']:.3f}"))
        out += [f"## Pass bar: `{run.variant}`", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
