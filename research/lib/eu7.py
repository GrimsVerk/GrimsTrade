"""eu-7: trend on the stock funds only (A) and hold-the-seven with a fixed cash share (B) on
the small coin-free euro book, against trend (T) and holding (H) (cards/eu-7.md).

    uv run --with numpy --with xlrd python research/lib/eu7.py check   # plumbing: no number
    uv run --with numpy --with xlrd python research/lib/eu7.py run     # 24 rows and the result

Needs what eu6.py needs (CSVs from `eu1_data.py build`, the git-ignored saved runs of eu-3, eu-5
and eu-6 under research/data/runs/, Shiller's ie_data.xls and the datahub gold csv in the cache
root of research/macro.local.json). T, H and M are eu-5's / eu-6's saved runs, re-scored without
new rows. Every new run is a row in tries.md (idea `eu-7`); a run whose file already exists
under research/data/runs/eu-7/ is re-scored without a new row. Train period only.
"""

from __future__ import annotations

import csv
import sys
from collections.abc import Mapping, Sequence
from datetime import date

import common as c
import eu1
import eu2
import eu3
import eu4_run as e4
import eu5
import eu6
import harness
import numpy as np
from harness import TRAIN_END, Run

from grimstrade import gym, report

IDEA = "eu-7"
W_START = eu1.W_START
EUW, USW = eu1.EUW, eu1.USW
SIZES = eu6.SIZES
TIERS = eu6.TIERS
US_START = eu6.US_START
STOCKS_EU = ("SXR8", "EXSA", "IQQE")
STOCKS_US = ("SPY", "EFA", "EEM")
BAND_7 = eu5.band_525(7)  # 3.57% of the book
N_FAMILY = 12
P_FAM = 0.10 / N_FAMILY  # 0.0083
DD_KEEP, CRASH_KEEP, CRASH_NEED = 0.02, 0.03, 5  # "keeps the insurance"
SH_GAIN, UW_GAIN, ORD_CUT, GAINS_NEED = 0.05, 3.0, 0.25, 2  # "loses less of the rest"
DD_TIE, UW_TIE, CRASH_TIE, LOSS_MAX = eu6.DD_TIE, eu6.UW_TIE, eu6.CRASH_TIE, eu6.LOSS_MAX
KEYS = ["T", "A", "B", "H"]
NAMES = {
    "T": "T trend (tsmom12, all seven)",
    "A": "A trend on stocks only",
    "B": "B hold7 + fixed cash",
    "H": "H hold7",
    "M": "M mix60 (ref)",
}


# ---- the rules ----


def exposure(t_decs: Sequence[gym.Decision]) -> float:
    """e: T's average target exposure on W (positions, not returns), rounded to a whole %."""
    return round(float(np.mean([sum(d.weights.values()) for d in t_decs])), 2)


def a_strategy(stocks: Sequence[str]) -> c.ResearchStrategy:
    def f(view: harness.View) -> dict[str, float]:
        held = c.live(view)
        return {s: 1 / len(held) for s in held if s not in stocks or c.tsmom_signal(view, s)}

    return c.weekly(f)


def b_strategy(e: float) -> c.ResearchStrategy:
    def f(view: harness.View) -> dict[str, float]:
        held = c.live(view)
        return {s: e / len(held) for s in held}

    return c.weekly(f)


def b_band(e: float) -> float:
    return min(0.05, 0.25 * e / 7)


def euw_decisions(pan: harness.Panel, e: float | None = None) -> dict[str, list[gym.Decision]]:
    t = eu5.r_decisions(pan)
    e = exposure(t) if e is None else e
    a = harness.decisions(a_strategy(STOCKS_EU), pan, W_START, TRAIN_END)
    return {
        "T": t,
        "A": a,
        "B": harness.decisions(b_strategy(e), pan, W_START, TRAIN_END),
        "H": harness.decisions(eu1.EW, pan, W_START, TRAIN_END),
    }


def simulate(
    variant: str, decs: list[gym.Decision], syms: Sequence[str],
    costs: Mapping[str, gym.Costs], band: float, st: eu2.FeeState, kind: str, start: date,
) -> eu5.Out:  # fmt: skip
    """As eu6.simulate, under idea eu-7."""
    hist, _ = eu1.panel_for(syms)
    with eu2.fixed_fees(st):
        res = gym.simulate(decs, hist, costs=costs, band=band)
    sc = report.score(f"{IDEA}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    expo = float(np.mean([sum(d.weights.values()) for d in decs]))
    run = Run(IDEA, variant, "train", sc, days, equity, expo, decs)
    path = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    if not path.exists():
        harness._log(run, kind, start, TRAIN_END)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date", "equity"])
            w.writerows((d.isoformat(), repr(float(x))) for d, x in zip(days, equity, strict=True))
        print("logged", variant, flush=True)
    else:
        print("re-scored", variant, flush=True)
    years = (days[-1] - days[0]).days / 365
    en, ex, ot = eu3.count_fills(res.fills)
    return eu5.Out(run, res, st.orders / years, en / years, ex / years, ot / years,
                   st.paid / years)  # fmt: skip


# ---- the long monthly proxy (stocks, 10y Treasuries, gold) ----


def proxy_ab(months: list[date], r: np.ndarray, e: float) -> eu6.Proxy:
    """A: stock slot on the lagged 12-month signal, bonds and gold 1/3 always; B: e/3 each."""
    first = 13
    out = {}
    for key in ("A", "B"):
        rets, turn = [], 0.0
        w_prev = np.zeros(3)
        for i in range(first, len(months)):
            if key == "A":
                up = bool(np.prod(r[i - 13 : i - 1, 0]) > 1)
                w = np.array([1 / 3 if up else 0.0, 1 / 3, 1 / 3])
                if w[1] != 1 / 3 or w[2] != 1 / 3:
                    raise AssertionError("proxy A: bonds and gold not at 1/3")
            else:
                w = np.full(3, e / 3)
            turn += float(np.abs(w - w_prev).sum())
            gross = float(w @ r[i] + (1 - w.sum()))
            rets.append(gross - 1)
            w_prev = w * r[i] / gross
        out[key] = (months[first:], np.array(rets), turn / (len(rets) / 12))
    return out


def log_monthly(variant: str, kind: str, ms: list[date], rets: np.ndarray, turn: float) -> None:
    old = eu6.IDEA
    eu6.IDEA = IDEA  # eu6.log_monthly files the row and the flag under its module's IDEA
    try:
        eu6.log_monthly(variant, kind, ms, rets, turn)
    finally:
        eu6.IDEA = old


# ---- plumbing ----


def check() -> None:
    eu6.check()  # T and H reproduce eu-5's / eu-3's saved runs; mix weights; proxy months
    _, pan = eu1.panel_for(EUW)
    t = eu5.r_decisions(pan)
    e = exposure(t)
    if not (0 < e < 1 and abs(e * 100 - round(e * 100)) < 1e-9):
        raise AssertionError("e is not a whole percent in (0, 1)")
    d = euw_decisions(pan, e)
    if len(d["A"]) != len(t) or len(d["B"]) != len(t):
        raise AssertionError("decision days differ")
    for ta, a, b in zip(t, d["A"], d["B"], strict=True):
        if ta.time != a.time or ta.time != b.time:
            raise AssertionError("decision times differ")
        for s in EUW:
            if s in STOCKS_EU:
                if abs(a.weights.get(s, 0.0) - ta.weights.get(s, 0.0)) > 1e-9:
                    raise AssertionError(f"A's stock weight differs from T on {a.time} {s}")
            elif abs(a.weights.get(s, 0.0) - 1 / 7) > 1e-9:
                raise AssertionError(f"A does not hold {s} at 1/7 on {a.time}")
            if abs(b.weights.get(s, 0.0) - e / 7) > 1e-9:
                raise AssertionError(f"B does not hold {s} at e/7 on {b.time}")
    _, pu = eu1.panel_for(USW)
    tu = harness.decisions(eu1.TSMOM, pu, US_START, TRAIN_END)
    au = harness.decisions(a_strategy(STOCKS_US), pu, US_START, TRAIN_END)
    bu = harness.decisions(b_strategy(e), pu, US_START, TRAIN_END)
    for x, a, b in zip(tu, au, bu, strict=True):
        for s in USW:
            want = x.weights.get(s, 0.0) if s in STOCKS_US else 1 / 7
            if abs(a.weights.get(s, 0.0) - want) > 1e-9:
                raise AssertionError(f"usw A off on {a.time} {s}")
            if abs(b.weights.get(s, 0.0) - e / 7) > 1e-9:
                raise AssertionError(f"usw B off on {b.time} {s}")
    ms, r = eu6.proxy_returns()
    proxy_ab(ms, r, e)
    print("check ok", flush=True)


# ---- the report ----


def fmt_crit(name: str, o: eu5.Out) -> tuple[str, dict[str, float]]:
    d = c.describe(o.run)
    cr = {
        "sharpe": d["sharpe"], "mdd": d["mdd"], "uw": eu6.underwater_months(o.run),
        "w12": eu6.worst_12m(o.run), "orders": o.orders_yr,
    }  # fmt: skip
    line = (
        f"| {name} | {d['sharpe']:.2f} ({d['se']:.2f}) | {d['cagr']:+.1%} | {d['vol']:.1%} | "
        f"{d['mdd']:.1%} | {cr['uw']:.0f} mo | {cr['w12']:+.1%} | {o.orders_yr:.1f} | "
        f"{d['exposure']:.0%} |"
    )
    return line, cr


def report_all() -> None:
    check()
    zero = eu2.FeeState
    _, pan = eu1.panel_for(EUW)
    dec = euw_decisions(pan)
    e = exposure(dec["T"])
    band_b = b_band(e)
    bands = {"T": BAND_7, "A": BAND_7, "B": band_b, "H": BAND_7}
    m_decs = harness.decisions(eu6.fixed(eu6.MIX_EU), pan, W_START, TRAIN_END)

    def run_cell(k: str, tag: str, st: eu2.FeeState) -> eu5.Out:
        if k == "T":
            return eu5.simulate(f"D2-band25r@euw/{tag}", dec["T"], EUW, eu2.COSTS, BAND_7, st,
                                "variant")  # fmt: skip
        if k == "H":
            return eu6.simulate(f"hold7@euw/{tag}", dec["H"], EUW, eu2.COSTS, BAND_7, st,
                                "baseline", W_START)  # fmt: skip
        if k == "M":
            return eu6.simulate(f"mix60@euw/{tag}", m_decs, EUW, eu2.COSTS, eu6.BAND_MIX, st,
                                "baseline", W_START)  # fmt: skip
        name = {"A": "trendstocks", "B": "hold7cash"}[k]
        return simulate(f"{name}@euw/{tag}", dec[k], EUW, eu2.COSTS, bands[k], st, "variant",
                        W_START)  # fmt: skip

    out0 = {k: run_cell(k, "slip", zero(0, 0)) for k in [*KEYS, "M"]}

    # 2008 US proxy
    _, pu = eu1.panel_for(USW)
    gcost = eu1.COSTS["gym"]
    us = {
        "T": eu6.simulate("trend525@usw-2007", harness.decisions(eu1.TSMOM, pu, US_START,
                          TRAIN_END), USW, gcost, BAND_7, zero(0, 0), "robustness", US_START),
        "A": simulate("trendstocks@usw-2007", harness.decisions(a_strategy(STOCKS_US), pu,
                      US_START, TRAIN_END), USW, gcost, BAND_7, zero(0, 0), "robustness",
                      US_START),
        "B": simulate("hold7cash@usw-2007", harness.decisions(b_strategy(e), pu, US_START,
                      TRAIN_END), USW, gcost, band_b, zero(0, 0), "robustness", US_START),
        "H": eu6.simulate("hold7@usw-2007", harness.decisions(eu1.EW, pu, US_START, TRAIN_END),
                          USW, gcost, BAND_7, zero(0, 0), "baseline", US_START),
    }  # fmt: skip
    for k, o in us.items():
        o.run.variant = f"{k} @usw 2007-"

    # long monthly proxy
    ms, rr = eu6.proxy_returns()
    lp = {**eu6.proxy_books(ms, rr), **proxy_ab(ms, rr, e)}
    for k in ("A", "B"):
        mm, rets, turn = lp[k]
        name = {"A": "trendstocks", "B": "hold7cash"}[k]
        log_monthly(f"{name}-proxy@long-monthly", "robustness", mm, rets, turn)

    txt = ["# eu-7 results: trend on stocks only (A), hold-seven with fixed cash (B) "
           "(cards/eu-7.md)", ""]  # fmt: skip
    txt += [
        f"Train only. `euw` in EUR, window W (decisions 2012-01-02 .. 2025-11-09), total-return "
        f"prices, ETF slippage 0.05% a side, cash at 0. T = `tsmom12` + 5/25 band (eu-5's D2); "
        f"A = `tsmom12` slots on SXR8, EXSA, IQQE, IBGS/IBGL/4GLD/EXXY at 1/7 always, band "
        f"3.57%; B = all seven at e/7 with e = T's average exposure = {e:.2f} (cash "
        f"{1 - e:.0%}), band {band_b:.2%}; H = equal weight + 5/25 band; M = 60/40 (eu-6, ref). "
        f"Sharpe on calendar days, zero risk-free rate.",
        "",
        "## 1. The human criteria at no fixed fee",
        "",
        "| Rule | Sharpe (SE) | CAGR | Vol | Worst loss (max DD) | Longest under water | "
        "Worst 12 months | Orders/yr | Avg exposure |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    crit: dict[str, dict[str, float]] = {}
    for k in [*KEYS, "M"]:
        line, crit[k] = fmt_crit(NAMES[k], out0[k])
        txt.append(line)

    txt += [
        "",
        "## 2. Sharpe differences (no fixed fee)",
        "",
        f"Paired stationary bootstrap (block 20 days, 2,000 draws, seed 0). A lead of A or B "
        f"counts as real only at p < {P_FAM:.4f} (eu family {N_FAMILY}).",
        "",
        "| Pair | dSharpe | Bootstrap SE | 90% range | p (first better) | p (second better) |",
        "|---|---:|---:|---|---:|---:|",
    ]
    p_at = p_bt = 1.0
    for a, b in (("A", "T"), ("A", "H"), ("B", "T"), ("B", "H"), ("A", "B")):
        dd, se, lo, hi, p = eu6.boot(out0[a].run, out0[b].run)
        txt.append(f"| {a} - {b} | {dd:+.2f} | {se:.2f} | {lo:+.2f} .. {hi:+.2f} | {p:.3f} | "
                   f"{1 - p:.3f} |")  # fmt: skip
        if (a, b) == ("A", "T"):
            p_at = p
        if (a, b) == ("B", "T"):
            p_bt = p

    # crash windows
    crash_names = [n for n, _, _ in e4.inside_crashes()]
    allk = [*KEYS, "M"]
    cr = {k: e4.crash_rets(out0[k].run) for k in allk}
    m_us = harness.decisions(eu6.fixed(eu6.MIX_US), pu, US_START, TRAIN_END)
    us_m = eu6.simulate("mix60@usw-2007", m_us, USW, gcost, eu6.BAND_MIX, zero(0, 0),
                        "baseline", US_START)  # fmt: skip
    gfc = {k: eu1.crash_ret(us[k].run, *eu6.GFC) for k in KEYS} | {
        "M": eu1.crash_ret(us_m.run, *eu6.GFC)
    }
    dot = {k: eu6.m_window(lp[k][0], lp[k][1], *eu6.DOTCOM) for k in allk}
    gfc_m = {k: eu6.m_window(lp[k][0], lp[k][1], *eu6.GFC_M) for k in allk}
    windows = [("2000-02 (long monthly proxy)", dot), ("2008 (usw proxy, USD)", gfc)]
    windows += [(n, {k: cr[k][i] for k in allk}) for i, n in enumerate(crash_names)]
    txt += ["", "## 3. Crash windows (total return inside each)", ""]
    txt += ["| Window | " + " | ".join(NAMES[k] for k in allk) + " | Best of T/A/B/H "
            "(within 1 pt) |", "|---|" + "---:|" * len(allk) + "---|"]  # fmt: skip
    wins = {k: 0 for k in KEYS}
    near_t = {k: 0 for k in ("A", "B")}
    for n, vals in windows:
        top = max(vals[k] for k in KEYS)
        best = [k for k in KEYS if vals[k] >= top - CRASH_TIE]
        for k in best:
            wins[k] += 1
        for k in near_t:
            if vals[k] >= vals["T"] - CRASH_KEEP:
                near_t[k] += 1
        txt.append(f"| {n} | " + " | ".join(f"{vals[k]:+.1%}" for k in allk)
                   + f" | {', '.join(best)} |")  # fmt: skip
    txt.append("| 2008, second view (long monthly proxy; not counted) | "
               + " | ".join(f"{gfc_m[k]:+.1%}" for k in allk) + " | - |")  # fmt: skip
    txt += [
        "",
        "Windows best (of 6, within 1 pt): " + ", ".join(f"{k} {wins[k]}" for k in KEYS)
        + ". Windows within 3 pts of T: " + ", ".join(f"{k} {near_t[k]}" for k in near_t) + ".",
        "",
        "Proxy books in full (shown, not judged):",
        "",
        c.table([us[k].run for k in KEYS], versus=us["T"].run),
        "",
        "Long monthly proxy (stocks / 10y Treasuries / gold, 1972-2025, monthly averages, cash "
        "at 0, no fees; Sharpe from monthly returns):",
        "",
        "| Rule | Sharpe | CAGR | Max DD | Turnover/yr |",
        "|---|---:|---:|---:|---:|",
    ]  # fmt: skip
    for k in allk:
        s = eu6.m_stats(lp[k][1])
        txt.append(f"| {k} proxy | {s['sharpe']:.2f} | {s['cagr']:+.1%} | {s['mdd']:.1%} | "
                   f"{lp[k][2]:.2f} |")  # fmt: skip

    # the answer (card's three tests)
    t = crit["T"]
    txt += [
        "",
        "## 4. The card's answer: keep the insurance, lose less of the rest?",
        "",
        "| Rule | Max DD vs T (<= +2 pts) | Crash windows within 3 pts of T (>= 5 of 6) | "
        "Keeps insurance | Sharpe vs T (>= +0.05; p) | Under water vs T (>= 3 mo shorter) | "
        "Orders vs T (>= 25% fewer) | Gains (>= 2 of 3) | Held-out card? |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    passes: dict[str, bool] = {}
    for k, p in (("A", p_at), ("B", p_bt)):
        x = crit[k]
        dd_ok = x["mdd"] <= t["mdd"] + DD_KEEP
        cw_ok = near_t[k] >= CRASH_NEED
        keep = dd_ok and cw_ok
        g_sh = x["sharpe"] >= t["sharpe"] + SH_GAIN
        g_uw = x["uw"] <= t["uw"] - UW_GAIN
        g_or = x["orders"] <= t["orders"] * (1 - ORD_CUT)
        gains = int(g_sh) + int(g_uw) + int(g_or)
        passes[k] = keep and gains >= GAINS_NEED
        real = "real" if p < P_FAM else "not real"
        txt.append(
            f"| {NAMES[k]} | {x['mdd'] - t['mdd']:+.1%} ({eu5.yn(dd_ok)}) | {near_t[k]} "
            f"({eu5.yn(cw_ok)}) | **{eu5.yn(keep)}** | {x['sharpe'] - t['sharpe']:+.2f} "
            f"(p={p:.3f}, {real}; {eu5.yn(g_sh)}) | {x['uw'] - t['uw']:+.0f} mo "
            f"({eu5.yn(g_uw)}) | {x['orders'] / t['orders'] - 1:+.0%} ({eu5.yn(g_or)}) | "
            f"{gains} ({eu5.yn(gains >= GAINS_NEED)}) | **{eu5.yn(passes[k])}** |"
        )
    passed = [k for k in ("A", "B") if passes[k]]
    if passed:
        pick = max(passed, key=lambda k: crit[k]["sharpe"])
        txt += ["", f"Named for a held-out-year card (mechanical: higher no-fee Sharpe of those "
                f"passing): **{pick}**."]  # fmt: skip
    else:
        txt += ["", "Neither rule passes both tests: the held-out year stays unspent."]

    # fees
    txt += ["", "## 5. Fixed fees by tier and book", ""]
    txt += [
        "Loss = own Sharpe at no fee minus Sharpe at the tier. P1 winner = highest Sharpe at "
        f"the cell; 'real' only if the bootstrap p of the leader vs the runner-up < {P_FAM:.4f}, "
        "else a tie, decided by fewer orders a year at no fee.",
        "",
        "| Tier | Book | " + " | ".join(f"{k} Sharpe (loss; orders; fees/yr)" for k in KEYS)
        + " | P1 winner |",
        "|---|---:|" + "---|" * len(KEYS) + "---|",
    ]  # fmt: skip
    p1: dict[tuple[str, int], str] = {}
    loss: dict[tuple[str, str, int], float] = {}
    by_orders = sorted(KEYS, key=lambda k: crit[k]["orders"])
    for tname, ttag, sch in TIERS:
        for size in SIZES:
            tag = f"{ttag}-{size // 1000}k"
            cell = {k: run_cell(k, tag, zero(sch.per_order / size, sch.per_year / size))
                    for k in KEYS}  # fmt: skip
            shs = {k: c.describe(cell[k].run)["sharpe"] for k in KEYS}
            ranked = sorted(KEYS, key=lambda k: -shs[k])
            _, _, _, _, p = eu6.boot(cell[ranked[0]].run, cell[ranked[1]].run)
            if p < P_FAM:
                win = f"{ranked[0]} (real, p={p:.4f})"
                p1[(tname, size)] = ranked[0]
            else:
                tied = [k for k in by_orders if k in ranked[:2]]
                win = f"tie {ranked[0]}~{ranked[1]} (p={p:.2f}) -> {tied[0]}"
                p1[(tname, size)] = tied[0]
            parts = []
            for k in KEYS:
                loss[(k, tname, size)] = crit[k]["sharpe"] - shs[k]
                parts.append(f"{shs[k]:.2f} ({loss[(k, tname, size)]:.3f}; "
                             f"{cell[k].orders_yr:.1f}; {cell[k].fees_yr:.2%})")  # fmt: skip
            txt.append(f"| {tname} | {size // 1000}k | " + " | ".join(parts) + f" | {win} |")

    # preferences
    def tie_pick(cands: list[str]) -> str:
        return min(cands, key=lambda k: crit[k]["orders"])

    lo_dd = min(crit[k]["mdd"] for k in KEYS)
    p2c = [k for k in KEYS if crit[k]["mdd"] <= lo_dd + DD_TIE]
    p2 = p2c[0] if len(p2c) == 1 else max(p2c, key=lambda k: crit[k]["w12"])
    lo_uw = min(crit[k]["uw"] for k in KEYS)
    p3c = [k for k in KEYS if crit[k]["uw"] <= lo_uw + UW_TIE]
    p3 = tie_pick(p3c)
    top_w = max(wins.values())
    p4c = [k for k in KEYS if wins[k] == top_w]
    p4 = tie_pick(p4c)
    p5 = by_orders[0]
    txt += [
        "",
        "## 6. Which wins under which preference (among T, A, B, H)",
        "",
        "| Preference | Winner | Why |",
        "|---|---|---|",
        "| P1 Sharpe after fees | per cell, table 5 | "
        + ", ".join(f"{tn} {s // 1000}k: {p1[(tn, s)]}" for tn, _, _ in TIERS for s in SIZES)
        + " |",
        f"| P2 worst loss | **{p2}** | max DD "
        + ", ".join(f"{k} {crit[k]['mdd']:.1%}" for k in KEYS)
        + f"; tie band 2 pts (candidates {', '.join(p2c)}; then worst 12 months "
        + ", ".join(f"{k} {crit[k]['w12']:+.1%}" for k in p2c) + ") |",
        f"| P3 waiting | **{p3}** | longest under water "
        + ", ".join(f"{k} {crit[k]['uw']:.0f} mo" for k in KEYS)
        + f" (tie band 3 mo: {', '.join(p3c)}; then fewer orders) |",
        f"| P4 crash insurance | **{p4}** | windows best of 6: "
        + ", ".join(f"{k} {wins[k]}" for k in KEYS) + " |",
        f"| P5 cost | **{p5}** | orders/yr "
        + ", ".join(f"{k} {crit[k]['orders']:.1f}" for k in KEYS) + " |",
        "",
        "## 7. Worth running? (the winner of the preference, if its fee loss <= 0.10)",
        "",
        "| Preference | " + " | ".join(f"{tn} {s // 1000}k" for tn, _, _ in TIERS for s in SIZES)
        + " |",
        "|---|" + "---|" * (len(TIERS) * len(SIZES)),
    ]  # fmt: skip
    for pname, winner in (("P1 Sharpe", None), ("P2 worst loss", p2), ("P3 waiting", p3),
                          ("P4 crash insurance", p4), ("P5 cost", p5)):  # fmt: skip
        cells = []
        for tn, _, _ in TIERS:
            for s in SIZES:
                w = p1[(tn, s)] if winner is None else winner
                ok = loss[(w, tn, s)] <= LOSS_MAX
                cells.append(f"{w} ({'yes' if ok else 'no: fees'})")
        txt.append(f"| {pname} | " + " | ".join(cells) + " |")
    # descriptive
    db, dt = c.describe(out0["B"].run), c.describe(out0["T"].run)
    txt += [
        "",
        f"Descriptive: vol B {db['vol']:.1%}, T {dt['vol']:.1%}; Sharpe B {db['sharpe']:.2f}, "
        f"H {crit['H']['sharpe']:.2f} (cash at 0: holding less scales return and risk).",
    ]
    c.write_result(IDEA, "\n".join(txt))


if __name__ == "__main__":
    {"check": check, "run": report_all}[sys.argv[1]]()
