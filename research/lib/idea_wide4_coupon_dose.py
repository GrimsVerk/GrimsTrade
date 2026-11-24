"""uv run python research/lib/idea_wide4_coupon_dose.py
(card: cards/coupon-dose.md; needs `python -I research/lib/wide4_coupons.py` to have been run)"""

from __future__ import annotations

import csv
from collections.abc import Sequence
from datetime import date

import common as c
import macro
import numpy as np
import wide1 as w
import wide4_rules as r

from grimstrade.data import Bar

IDEA = "coupon-dose"
P_BAR = 0.10 / 54  # the list of 46 plus W1-W8 (cards/coupon-dose.md)
FIRST = date(2002, 7, 30)  # TLT's first day
SPLIT = date(2014, 1, 1)


def load_payments() -> list[r.Payment]:
    path = macro.cache_root() / "derived" / "wide-4" / "payments.csv"
    out = []
    with path.open(newline="") as f:
        for row in csv.DictReader(f):
            day, known = date.fromisoformat(row["date"]), date.fromisoformat(row["announced"])
            out.append(r.Payment(day, row["kind"], float(row["amount"]), known))
    return out


_doses: dict[str, tuple[list[date], dict[int, tuple[float, float]]]] = {}


def doses(sym: str) -> tuple[list[date], dict[int, tuple[float, float]]]:
    """Mid-month doses on `sym`'s own calendar, 1994 to the end of train."""
    if sym not in _doses:
        cal = w.calendar(sym)
        _doses[sym] = (cal, r.mid_month_doses(cal, load_payments(), date(1994, 1, 1), c.TRAIN_END))
    return _doses[sym]


def overlay(bond: str, positive: bool) -> c.ResearchStrategy:
    """`tsmom12` plus the idle cash in `bond` after the close of P-1 .. P+2."""
    base = c.weekly(c.slots(c.tsmom_signal))
    cal, ds = doses(bond)
    on = r.overlay_sessions(cal, ds, positive)

    def f(view: c.View) -> c.Weights:
        held = base(view)
        last = w.last_session(view, bond)
        if last is None or last not in on or not c.eligible(view, bond):
            return held
        idle = 1.0 - sum(held.values())
        if idle <= 1e-9:
            return held
        out = dict(held)
        out[bond] = out.get(bond, 0.0) + idle
        return out

    return f


def study(sym: str, bars: Sequence[Bar]) -> tuple[list[str], dict[str, float]]:
    cal, ds = doses(sym)
    days = [b.date for b in bars]
    lc = np.log(np.array([b.close for b in bars]))
    idx = {d: i for i, d in enumerate(days)}
    four = lc[4:] - lc[:-4]
    mean4 = float(four.mean())
    rows = []
    for j, (net, pct) in sorted(ds.items()):
        p = cal[j]
        if p < FIRST or p not in idx:
            continue
        i = idx[p]
        if i - 1 < 0 or i + 3 >= len(lc):
            continue
        rows.append((p, net, pct, float(lc[i + 3] - lc[i - 1]) - mean4))
    lines, got = [], {}
    periods = (
        ("all", FIRST, c.TRAIN_END),
        ("2002-07 to 2013", FIRST, date(2013, 12, 31)),
        ("2014 to end of train", SPLIT, c.TRAIN_END),
    )
    for name, lo, hi in periods:
        sub = [x for x in rows if lo <= x[0] <= hi]
        pos = np.array([x[3] for x in sub if x[1] > 0]) * 1e4
        neg = np.array([x[3] for x in sub if x[1] <= 0]) * 1e4
        b, t = r.hc1_slope(np.array([x[2] for x in sub]), np.array([x[3] for x in sub]) * 1e4)
        lines.append(
            f"| {sym} | {name} | {len(pos)} | {pos.mean():+.1f} ({w.tstat(pos):+.2f}) | "
            f"{len(neg)} | {neg.mean():+.1f} ({w.tstat(neg):+.2f}) | {b:+.1f} | {t:+.2f} |"
        )
        got[f"{name}:pos"], got[f"{name}:neg"] = float(pos.mean()), float(neg.mean())
        got[f"{name}:slope"], got[f"{name}:t"] = b, t
    nets = np.array([x[1] for x in rows])
    pcts = np.array([x[2] for x in rows])
    got["n"], got["npos"] = len(rows), int((nets > 0).sum())
    got["net_med"], got["pct_sd"] = float(np.median(nets)), float(pcts.std())
    return lines, got


def main() -> None:
    out = ["# coupon-dose: idle cash into the long bond when Treasury cash is paid back", ""]
    out += ["Card: `cards/coupon-dose.md`. Protocol: `protocol.md`.", ""]
    six = c.ctx("six")
    twin_s = c.weekly(c.slots(c.tsmom_signal))
    twin = c.go("baselines", "tsmom12", twin_s, six, "baseline", log=False)
    ew = c.go("baselines", "equal-weight", c.weekly(c.equal_weight), six, "baseline", log=False)
    run = c.go(IDEA, "dose", overlay("TLT", True), six, "variant")
    plc = c.go(IDEA, "dose-neg", overlay("TLT", False), six, "robustness")
    runs = [run, plc, twin, ew]
    out += ["## The six live assets, train period", "", c.table(runs, twin), ""]
    out += ["Total return inside each stress window:", "", c.stress_table(runs), ""]
    vs = w.versus(run, twin, "2000-09")

    out += ["## Event study (descriptive): sessions P .. P+3, close of P-1 to close of P+3", ""]
    out += ["Excess = log return minus the average 4-session log return since 2002-07-30, in "
            "bps (t). Slope = bps of excess per 1% of outstanding notes and bonds paid back "
            "net (OLS, HC1 t).", ""]  # fmt: skip
    out += ["| Bond | Period | Positive doses | Excess (t) | Non-positive | Excess (t) | Slope | "
            "t |", "|---|---|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    etf = c.ctx("etf")
    tl, tg = study("TLT", six.hist["TLT"])
    il, _ = study("IEF", etf.hist["IEF"])
    out += [*tl, *il, ""]
    out += [f"Mid-month days since 2002-07 (TLT): {tg['n']:.0f}, of which {tg['npos']:.0f} with a "
            f"positive net dose; median net dose {tg['net_med']:+.1f} $bn; standard deviation "
            f"of the dose {tg['pct_sd']:.3f}% of outstanding.", ""]  # fmt: skip
    ok_a = tg["all:slope"] > 0 and tg["all:t"] >= 2
    ok_b = tg["all:pos"] > tg["all:neg"]
    ok_c = tg["2002-07 to 2013:slope"] > 0 and tg["2014 to end of train:slope"] > 0
    out += [f"Card's reading for TLT: (a) slope > 0 with t >= 2 {'yes' if ok_a else 'no'}; "
            f"(b) positive-dose mean above the rest {'yes' if ok_b else 'no'}; (c) slope "
            f"positive in both halves {'yes' if ok_c else 'no'}. Mechanism **"
            f"{'supported' if ok_a and ok_b and ok_c else 'not supported'}**.", ""]  # fmt: skip

    out += ["## Out of universe: the 8 other ETFs, overlay into IEF", ""]
    t_e = c.go("baselines", "tsmom12", twin_s, etf, "baseline", log=False)
    a_e = c.go(IDEA, "dose", overlay("IEF", True), etf, "robustness")
    out += [c.table([a_e, t_e], t_e, eras=False), ""]
    sign_e = w.versus(a_e, t_e)["diff"]

    dv, dt, de, dp = c.describe(run), c.describe(twin), c.describe(ew), c.describe(plc)
    d = vs["diff"]
    bars = [
        (f"1. `dose` beats twin `tsmom12` with p < {P_BAR:.5f} (0.10 / 54)",
         d > 0 and vs["p"] < P_BAR, f"difference {d:+.3f}, p = {vs['p']:.4f}"),
        (f"2. Ahead of the twin in at least 3 of {vs['eras']:.0f} eras (from 2000-09)",
         vs["ahead"] >= 3, f"{vs['ahead']:.0f} of {vs['eras']:.0f}"),
        ("3. Max drawdown not more than 5 points worse than the twin's",
         dv["mdd"] <= dt["mdd"] + 0.05, f"{dv['mdd']:.1%} vs {dt['mdd']:.1%}"),
        ("4. Positive, and positive on the ETF set", d > 0 and sign_e > 0, f"etf {sign_e:+.3f}"),
        ("5. Beats equal weight on Sharpe", dv["sharpe"] > de["sharpe"],
         f"{dv['sharpe']:.2f} vs {de['sharpe']:.2f}"),
        ("6. (card) Beats its placebo `dose-neg` on Sharpe", dv["sharpe"] > dp["sharpe"],
         f"{dv['sharpe']:.3f} vs {dp['sharpe']:.3f}"),
    ]  # fmt: skip
    out += ["## Pass bar (only variant `dose`)", "", *w.bars_report(bars)]
    c.write_result(IDEA, "\n".join(out))


if __name__ == "__main__":
    main()
