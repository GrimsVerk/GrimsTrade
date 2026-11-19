"""eu-8 step 2: idea C, trend on the stock and long-bond funds only (cards/eu-8.md, step 2).

    uv run --with numpy --with xlrd python research/lib/eu8c.py check   # plumbing: no number
    uv run --with numpy --with xlrd python research/lib/eu8c.py run     # 13 rows and the result

Needs what eu8.py needs. Stage 1 (US proxies 1994-2011) is judged first and printed first; stage
2 (EUR 2012-2025) uses eu-7's test unchanged. Every new run is a row in tries.md (idea `eu-8`).
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
import eu7
import eu8
import harness
import numpy as np
import stats
from harness import TRAIN_END, Run

from grimstrade import gym, report

IDEA = eu8.IDEA
W_START, US_START = eu8.W_START, eu8.US_START
EUW, USW = eu8.EUW, eu8.USW
FILT_EU = ("SXR8", "EXSA", "IQQE", "IBGL")
FILT_US = ("SPY", "EFA", "EEM", "TLT")
US_END = date(2011, 12, 31)
M_FROM, M_TO = date(1994, 1, 1), date(2011, 12, 1)
N_FAMILY = 13
P_FAM = 0.10 / N_FAMILY  # 0.0077
BAND_7 = eu7.BAND_7
KEYS = ["T", "B", "C", "H"]
NAMES = {
    "T": "T trend (tsmom12, all seven)",
    "A": "A trend on stocks only (eu-7, ref)",
    "B": "B hold7 + 33% cash",
    "C": "C trend on stocks + long bonds",
    "H": "H hold7",
}


def c_strategy(filtered: Sequence[str]) -> c.ResearchStrategy:
    return eu7.a_strategy(filtered)  # filter only the named funds, the rest at 1/n always


def cut(hist: Mapping[str, list[harness.Bar]], last: date) -> dict[str, list[harness.Bar]]:
    return {s: [b for b in bars if b.date <= last] for s, bars in hist.items()}


def sim(
    variant: str | None, decs: list[gym.Decision], syms: Sequence[str],
    costs: Mapping[str, gym.Costs], band: float, st: eu2.FeeState, kind: str, start: date,
    last: date | None = None,
) -> eu5.Out:  # fmt: skip
    """As eu7.simulate, under idea eu-8; `last` cuts the history (no later bar is loaded)."""
    hist, _ = eu1.panel_for(syms)
    if last is not None:
        hist = cut(hist, last)
    with eu2.fixed_fees(st):
        res = gym.simulate(decs, hist, costs=costs, band=band)
    sc = report.score(f"{IDEA}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    expo = float(np.mean([sum(d.weights.values()) for d in decs]))
    run = Run(IDEA, variant or "-", "train", sc, days, equity, expo, decs)
    if variant is not None:
        path = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
        if not path.exists():
            harness._log(run, kind, start, last or TRAIN_END)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["date", "equity"])
                pairs = zip(days, equity, strict=True)
                w.writerows((d.isoformat(), repr(float(x))) for d, x in pairs)
            print("logged", variant, flush=True)
        else:
            print("re-scored", variant, flush=True)
    years = (days[-1] - days[0]).days / 365
    en, ex, ot = eu3.count_fills(res.fills)
    return eu5.Out(run, res, st.orders / years, en / years, ex / years, ot / years,
                   st.paid / years)  # fmt: skip


# ---- monthly proxy ----


def c_weigh(r: np.ndarray, i: int) -> np.ndarray:
    sig = np.prod(r[i - 13 : i - 1, :2], axis=0) > 1  # stocks and bonds on the lagged signal
    return np.array([1 / 3 if sig[0] else 0.0, 1 / 3 if sig[1] else 0.0, 1 / 3])


def m_underwater(rets: np.ndarray) -> int:
    lev = np.concatenate([[1.0], np.cumprod(1 + rets)])
    peak, start, worst = lev[0], 0, 0
    for i, x in enumerate(lev):
        if x >= peak:
            worst = max(worst, i - start)
            peak, start = x, i
    return max(worst, len(lev) - 1 - start)


def monthly(e: float) -> dict[str, tuple[list[date], np.ndarray, float]]:
    """Cash at 0. Full series from 1972 (for the 2000-02 window) per rule."""
    ms, rr = eu6.proxy_returns()
    rf = np.zeros(len(ms))
    w = eu8.proxy_weights(e) | {"C": c_weigh}
    out = {}
    for k in KEYS:
        mm, rets, _, turn = eu8.proxy_paid(ms, rr, rf, w[k], rate_on=False)
        out[k] = (mm, rets, turn)
    return out


def m_slice(mm: list[date], rets: np.ndarray) -> tuple[list[date], np.ndarray]:
    idx = [i for i, m in enumerate(mm) if M_FROM <= m <= M_TO]
    return [mm[i] for i in idx], rets[idx]


def m_turn(k: str, e: float) -> float:
    """Turnover a year inside 1994-2011 (weights re-derived; drift as eu6.proxy_books)."""
    ms, rr = eu6.proxy_returns()
    w = eu8.proxy_weights(e) | {"C": c_weigh}
    turn, w_prev, n = 0.0, np.zeros(3), 0
    for i in range(13, len(ms)):
        wi = w[k](rr, i)
        if M_FROM <= ms[i] <= M_TO:
            turn += float(np.abs(wi - w_prev).sum())
            n += 1
        gross = float(wi @ rr[i] + (1 - wi.sum()))
        w_prev = wi * rr[i] / gross
    return turn / (n / 12)


# ---- slices of daily runs ----


def d_slice(out: eu5.Out, a: date, b: date) -> dict[str, float]:
    r = out.run.rets_between(a, b)
    n = sum(1 for f in out.res.fills if a <= f.time.date() <= b)
    years = (b - a).days / 365
    return {"sharpe": stats.sharpe(r), "mdd": stats.max_drawdown(r), "orders": n / years,
            "cagr": stats.cagr(r)}  # fmt: skip


# ---- plumbing ----


def decisions_all(e: float) -> tuple[dict[str, list[gym.Decision]], list[gym.Decision]]:
    _, pan = eu1.panel_for(EUW)
    d = eu7.euw_decisions(pan, e)
    d["C"] = harness.decisions(c_strategy(FILT_EU), pan, W_START, TRAIN_END)
    _, pu = eu1.panel_for(USW)
    cu = harness.decisions(c_strategy(FILT_US), pu, US_START, US_END)
    return d, cu


def check() -> None:
    eu8.check()
    _, pan = eu1.panel_for(EUW)
    e = eu7.exposure(eu5.r_decisions(pan))
    d, cu = decisions_all(e)
    if len(d["C"]) != len(d["T"]):
        raise AssertionError("decision days differ")
    for t, x in zip(d["T"], d["C"], strict=True):
        if t.time != x.time:
            raise AssertionError("decision times differ")
        for s in EUW:
            want = t.weights.get(s, 0.0) if s in FILT_EU else 1 / 7
            if abs(x.weights.get(s, 0.0) - want) > 1e-9:
                raise AssertionError(f"C off on {x.time} {s}")
    _, pu = eu1.panel_for(USW)
    tu = harness.decisions(eu1.TSMOM, pu, US_START, US_END)
    for t, x in zip(tu, cu, strict=True):
        for s in USW:
            want = t.weights.get(s, 0.0) if s in FILT_US else 1 / 7
            if abs(x.weights.get(s, 0.0) - want) > 1e-9:
                raise AssertionError(f"usw C off on {x.time} {s}")
    if cu[-1].time.date() > US_END:
        raise AssertionError("usw C decides after 2011")
    hist, _ = eu1.panel_for(USW)
    if max(b.date for bars in cut(hist, US_END).values() for b in bars) > US_END:
        raise AssertionError("usw history for C not cut")
    ms, rr = eu6.proxy_returns()
    for i in range(13, len(ms)):
        if c_weigh(rr, i)[2] != 1 / 3:
            raise AssertionError("monthly C: gold not at 1/3")
    print("check ok", flush=True)


# ---- the report ----


def report_all() -> None:
    check()
    zero = eu2.FeeState
    _, pan = eu1.panel_for(EUW)
    e = eu7.exposure(eu5.r_decisions(pan))
    d, cu = decisions_all(e)
    g = eu1.COSTS["gym"]

    # ---- stage 1: US proxies 1994-2011 ----
    us_o = eu8.usw_outs(e)
    us_c = sim("trendsl@usw-2007-2011", cu, USW, g, BAND_7, zero(0, 0), "robustness", US_START,
               US_END)  # fmt: skip
    us_all = {k: us_o[k] for k in ("T", "B", "H")} | {"C": us_c}
    us_s = {k: d_slice(o, US_START, US_END) for k, o in us_all.items()}
    gfc = {k: eu1.crash_ret(o.run, *eu6.GFC) for k, o in us_all.items()}
    lm = monthly(e)
    mm_c, r_c = m_slice(lm["C"][0], lm["C"][1])
    eu8.log_monthly("trendsl-proxy@long-monthly-1994-2011", "robustness", mm_c, r_c,
                    m_turn("C", e))  # fmt: skip
    ms1 = {}
    for k in KEYS:
        mm, rets = m_slice(lm[k][0], lm[k][1])
        s = eu6.m_stats(rets)
        s["uw"] = m_underwater(rets)
        s["turn"] = m_turn(k, e)
        ms1[k] = s
    dot = {k: eu6.m_window(lm[k][0], lm[k][1], *eu6.DOTCOM) for k in KEYS}

    t1, x1 = ms1["T"], ms1["C"]
    keep1 = (
        x1["mdd"] <= t1["mdd"] + eu7.DD_KEEP
        and us_s["C"]["mdd"] <= us_s["T"]["mdd"] + eu7.DD_KEEP
        and dot["C"] >= dot["T"] - eu7.CRASH_KEEP
        and gfc["C"] >= gfc["T"] - eu7.CRASH_KEEP
    )
    g_sh1 = x1["sharpe"] >= t1["sharpe"] + eu7.SH_GAIN
    g_uw1 = x1["uw"] <= t1["uw"] - eu7.UW_GAIN
    g_or1 = us_s["C"]["orders"] <= us_s["T"]["orders"] * (1 - eu7.ORD_CUT)
    gains1 = int(g_sh1) + int(g_uw1) + int(g_or1)
    pass1 = keep1 and gains1 >= eu7.GAINS_NEED

    yn = eu5.yn
    txt = ["# eu-8 step 2: idea C, trend on the stock and long-bond funds (cards/eu-8.md)", ""]
    txt += [
        "Train only, cash at 0 (eu-7's terms). C = `tsmom12` slots on SXR8, EXSA, IQQE, IBGL; "
        "IBGS, 4GLD, EXXY at 1/7 always; band 3.57%. On `usw`: SPY, EFA, EEM, TLT filtered; IEF, "
        "GLD, DBC held. Monthly proxy: stocks and 10y Treasuries filtered, gold held.",
        "",
        "## Stage 1: US proxies 1994-2011 (judged first)",
        "",
        "| Rule | Monthly 1994-2011: Sharpe | CAGR | Max DD | Longest under water | "
        "Turnover/yr | `usw` 2007-03..2011-12: Sharpe | Max DD | Orders/yr | 2000-02 | 2008 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for k in KEYS:
        s, u = ms1[k], us_s[k]
        txt.append(
            f"| {NAMES[k]} | {s['sharpe']:.2f} | {s['cagr']:+.1%} | {s['mdd']:.1%} | "
            f"{s['uw']} mo | {s['turn']:.2f} | {u['sharpe']:.2f} | {u['mdd']:.1%} | "
            f"{u['orders']:.1f} | {dot[k]:+.1%} | {gfc[k]:+.1%} |"
        )
    txt += [
        "",
        "| Test (C vs T) | Value | Pass |",
        "|---|---|---|",
        f"| Max DD monthly <= T + 2 pts | {x1['mdd'] - t1['mdd']:+.1%} | "
        f"{yn(x1['mdd'] <= t1['mdd'] + eu7.DD_KEEP)} |",
        f"| Max DD `usw` <= T + 2 pts | {us_s['C']['mdd'] - us_s['T']['mdd']:+.1%} | "
        f"{yn(us_s['C']['mdd'] <= us_s['T']['mdd'] + eu7.DD_KEEP)} |",
        f"| 2000-02 >= T - 3 pts | {dot['C'] - dot['T']:+.1%} | "
        f"{yn(dot['C'] >= dot['T'] - eu7.CRASH_KEEP)} |",
        f"| 2008 >= T - 3 pts | {gfc['C'] - gfc['T']:+.1%} | "
        f"{yn(gfc['C'] >= gfc['T'] - eu7.CRASH_KEEP)} |",
        f"| **Keeps the insurance** | | {yn(keep1)} |",
        f"| Sharpe monthly >= T + 0.05 | {x1['sharpe'] - t1['sharpe']:+.2f} | {yn(g_sh1)} |",
        f"| Under water monthly >= 3 mo shorter | {x1['uw'] - t1['uw']:+d} mo | {yn(g_uw1)} |",
        f"| Orders `usw` >= 25% fewer | {us_s['C']['orders'] / us_s['T']['orders'] - 1:+.0%} | "
        f"{yn(g_or1)} |",
        f"| **Loses less of the rest** (2 of 3) | {gains1} | {yn(gains1 >= eu7.GAINS_NEED)} |",
        f"| **Stage 1** | | {yn(pass1)} |",
    ]

    # ---- stage 2: EUR 2012-2025 ----
    outs, _ = eu8.euw_outs()
    band_b = eu7.b_band(e)
    o0 = {k: outs[k] for k in ("T", "B", "H")}
    o0["C"] = sim("trendsl@euw/slip", d["C"], EUW, eu2.COSTS, BAND_7, zero(0, 0), "variant",
                  W_START)  # fmt: skip
    a_ref = eu6.simulate(None, d["A"], EUW, eu2.COSTS, BAND_7, zero(0, 0), "", W_START)
    crit = {}
    txt += ["", "## Stage 2: EUR 2012-2025 (eu-7's test)", "",
            "| Rule | Sharpe (SE) | CAGR | Vol | Worst loss (max DD) | Longest under water | "
            "Worst 12 months | Orders/yr | Avg exposure |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
    for k in KEYS:
        line, crit[k] = eu7.fmt_crit(NAMES[k], o0[k])
        txt.append(line)
    txt.append(eu7.fmt_crit(NAMES["A"], a_ref)[0])

    txt += ["", f"Paired bootstrap (block 20, 2,000 draws, seed 0); real only at p < "
            f"{P_FAM:.4f} (eu family {N_FAMILY}).", "",
            "| Pair | dSharpe | SE | 90% range | p (first better) |",
            "|---|---:|---:|---|---:|"]  # fmt: skip
    p_ct = 1.0
    for a, b in (("C", "T"), ("C", "H"), ("C", "B")):
        dd, se, lo, hi, p = eu6.boot(o0[a].run, o0[b].run)
        txt.append(f"| {a} - {b} | {dd:+.2f} | {se:.2f} | {lo:+.2f} .. {hi:+.2f} | {p:.3f} |")
        if b == "T":
            p_ct = p

    names = [n for n, _, _ in e4.inside_crashes()]
    cr = {k: e4.crash_rets(o0[k].run) for k in KEYS}
    windows = {"2000-02 (long monthly proxy)": dot, "2008 (usw proxy, USD)": gfc}
    for i, n in enumerate(names):
        windows[n] = {k: cr[k][i] for k in KEYS}
    lines, wins = eu8.crash_table(windows, KEYS, KEYS)
    near = sum(1 for v in windows.values() if v["C"] >= v["T"] - eu7.CRASH_KEEP)
    txt += ["", "| Window | " + " | ".join(NAMES[k] for k in KEYS) + " | Best (within 1 pt) |",
            "|---|" + "---:|" * len(KEYS) + "---|", *lines, "",
            "Windows best (of 6): " + ", ".join(f"{k} {wins[k]}" for k in KEYS)
            + f". C within 3 pts of T: {near} of 6."]  # fmt: skip

    t, x = crit["T"], crit["C"]
    dd_ok = x["mdd"] <= t["mdd"] + eu7.DD_KEEP
    cw_ok = near >= eu7.CRASH_NEED
    keep2 = dd_ok and cw_ok
    g_sh = x["sharpe"] >= t["sharpe"] + eu7.SH_GAIN
    g_uw = x["uw"] <= t["uw"] - eu7.UW_GAIN
    g_or = x["orders"] <= t["orders"] * (1 - eu7.ORD_CUT)
    gains2 = int(g_sh) + int(g_uw) + int(g_or)
    pass2 = keep2 and gains2 >= eu7.GAINS_NEED
    real = "real" if p_ct < P_FAM else "not real"
    txt += [
        "",
        "| Test (C vs T) | Value | Pass |",
        "|---|---|---|",
        f"| Max DD <= T + 2 pts | {x['mdd'] - t['mdd']:+.1%} | {yn(dd_ok)} |",
        f"| Crash windows within 3 pts of T >= 5 of 6 | {near} | {yn(cw_ok)} |",
        f"| **Keeps the insurance** | | {yn(keep2)} |",
        f"| Sharpe >= T + 0.05 | {x['sharpe'] - t['sharpe']:+.2f} (p={p_ct:.3f}, {real}) | "
        f"{yn(g_sh)} |",
        f"| Under water >= 3 mo shorter | {x['uw'] - t['uw']:+.0f} mo | {yn(g_uw)} |",
        f"| Orders >= 25% fewer | {x['orders'] / t['orders'] - 1:+.0%} | {yn(g_or)} |",
        f"| **Loses less of the rest** (2 of 3) | {gains2} | {yn(gains2 >= eu7.GAINS_NEED)} |",
        f"| **Stage 2** | | {yn(pass2)} |",
        "",
        f"Worth a held-out-year card: {yn(pass1 and pass2)} (needs stage 1 and stage 2).",
    ]

    # with the euro rate (a): robustness row
    pc = eu8.with_interest(o0["C"], eu8.eur_rate(False), "trendsl-estr@euw/slip")
    eu8.log_row(pc, "robustness", W_START)
    pt = eu8.with_interest(o0["T"], eu8.eur_rate(False), "T")
    xc, xt = eu8.crit(pc), eu8.crit(pt)
    txt += ["", f"With rate (a) of step 1 (shown): C excess Sharpe {xc['xsharpe']:.2f}, CAGR "
            f"{xc['cagr']:+.1%}, worst loss {xc['mdd']:.1%}; T {xt['xsharpe']:.2f}, "
            f"{xt['cagr']:+.1%}, {xt['mdd']:.1%}."]  # fmt: skip

    # fees and preferences (eu-7's rules, among T, B, C, H)
    txt += ["", "## Fixed fees by tier and book", "",
            "| Tier | Book | " + " | ".join(f"{k} Sharpe (loss; orders)" for k in KEYS)
            + " | P1 winner |", "|---|---:|" + "---|" * len(KEYS) + "---|"]  # fmt: skip
    by_orders = sorted(KEYS, key=lambda k: crit[k]["orders"])
    p1: dict[tuple[str, int], str] = {}
    loss: dict[tuple[str, str, int], float] = {}
    for tname, ttag, sch in eu7.TIERS:
        for size in eu7.SIZES:
            tag = f"{ttag}-{size // 1000}k"

            def st() -> eu2.FeeState:
                return zero(sch.per_order / size, sch.per_year / size)  # noqa: B023

            cell = {
                "T": eu5.simulate(f"D2-band25r@euw/{tag}", d["T"], EUW, eu2.COSTS, BAND_7, st(),
                                  "variant"),
                "H": eu6.simulate(f"hold7@euw/{tag}", d["H"], EUW, eu2.COSTS, BAND_7, st(),
                                  "baseline", W_START),
                "B": eu7.simulate(f"hold7cash@euw/{tag}", d["B"], EUW, eu2.COSTS, band_b, st(),
                                  "variant", W_START),
                "C": sim(f"trendsl@euw/{tag}", d["C"], EUW, eu2.COSTS, BAND_7, st(), "variant",
                         W_START),
            }  # fmt: skip
            shs = {k: c.describe(cell[k].run)["sharpe"] for k in KEYS}
            ranked = sorted(KEYS, key=lambda k: -shs[k])
            _, _, _, _, p = eu6.boot(cell[ranked[0]].run, cell[ranked[1]].run)
            if p < P_FAM:
                p1[(tname, size)] = ranked[0]
                win = f"{ranked[0]} (real, p={p:.4f})"
            else:
                tied = [k for k in by_orders if k in ranked[:2]]
                p1[(tname, size)] = tied[0]
                win = f"tie {ranked[0]}~{ranked[1]} (p={p:.2f}) -> {tied[0]}"
            parts = []
            for k in KEYS:
                loss[(k, tname, size)] = crit[k]["sharpe"] - shs[k]
                parts.append(f"{shs[k]:.2f} ({loss[(k, tname, size)]:.3f}; "
                             f"{cell[k].orders_yr:.1f})")  # fmt: skip
            txt.append(f"| {tname} | {size // 1000}k | " + " | ".join(parts) + f" | {win} |")

    pc_ = {k: crit[k] | {"xsharpe": crit[k]["sharpe"]} for k in KEYS}
    pr = eu8.prefs(pc_, wins, KEYS)
    txt += [
        "",
        "## Which wins under which preference (among T, B, C, H)",
        "",
        "| Preference | Winner | Why | Fee loss <= 0.10 in all 9 cells? |",
        "|---|---|---|---|",
        "| P1 Sharpe after fees | " + ", ".join(sorted(set(p1.values()))) + " | per cell: "
        + ", ".join(f"{tn} {s // 1000}k {p1[(tn, s)]}" for tn, _, _ in eu7.TIERS
                    for s in eu7.SIZES) + " | - |",
    ]  # fmt: skip
    why = {
        "P2": "max DD " + ", ".join(f"{k} {crit[k]['mdd']:.1%}" for k in KEYS),
        "P3": "under water " + ", ".join(f"{k} {crit[k]['uw']:.0f} mo" for k in KEYS),
        "P4": "windows best "
        + ", ".join(f"{k} {wins[k]}" for k in KEYS)
        + " (a tie goes to fewer orders, eu-7's rule)",
        "P5": "orders/yr " + ", ".join(f"{k} {crit[k]['orders']:.1f}" for k in KEYS),
    }
    labels = {"P2": "P2 worst loss", "P3": "P3 waiting", "P4": "P4 crash insurance",
              "P5": "P5 cost"}  # fmt: skip
    for pk in ("P2", "P3", "P4", "P5"):
        w = pr[pk]
        bad = [f"{tn} {s // 1000}k" for tn, _, _ in eu7.TIERS for s in eu7.SIZES
               if loss[(w, tn, s)] > eu7.LOSS_MAX]  # fmt: skip
        txt.append(f"| {labels[pk]} | **{w}** | {why[pk]} | "
                   f"{'yes' if not bad else 'no: ' + ', '.join(bad)} |")  # fmt: skip
    c.write_result(f"{IDEA}-c", "\n".join(txt))


if __name__ == "__main__":
    {"check": check, "run": report_all}[sys.argv[1]]()
