"""eu-6: trend vs holding the seven funds vs a 60/40 mix, small coin-free euro book (cards/eu-6.md).

    uv run --with numpy --with xlrd python research/lib/eu6.py check   # plumbing: no number
    uv run --with numpy --with xlrd python research/lib/eu6.py run     # 26 rows and the result

Needs the CSVs from `eu1_data.py build`, the saved runs of eu-3 and eu-5 under the git-ignored
research/data/runs/ (T is eu-5's D2, re-scored without new rows), and for the long monthly proxy
Shiller's ie_data.xls and the datahub gold csv in the cache root (`long_bond.py`,
`long_gold.py`, copied unchanged from the data-long lanes). Every new run is a row in tries.md
(idea `eu-6`); a run whose equity file already exists under research/data/runs/eu-6/ is
re-scored without a new row. Train period only.
"""

from __future__ import annotations

import csv
import math
import sys
from collections.abc import Mapping, Sequence
from datetime import UTC, date, datetime

import common as c
import eu1
import eu2
import eu3
import eu4_run as e4
import eu5
import harness
import long_bond
import long_gold
import numpy as np
import stats
from harness import TRAIN_END, Run

from grimstrade import gym, report

IDEA = "eu-6"
W_START = eu1.W_START
EUW, USW = eu1.EUW, eu1.USW
SIZES = eu3.SIZES
TIERS = e4.TIERS
US_START = date(2007, 3, 1)
MIX_EU = {"SXR8": 0.2, "EXSA": 0.2, "IQQE": 0.2, "IBGS": 0.2, "IBGL": 0.2}
MIX_US = {"SPY": 0.2, "EFA": 0.2, "EEM": 0.2, "IEF": 0.2, "TLT": 0.2}
BAND_7 = eu5.band_525(7)  # 3.57% of the book
BAND_MIX = min(0.05, 0.25 * 0.2)  # 5%
P_REAL = 0.10 / 3
DD_TIE, UW_TIE, CRASH_TIE, LOSS_MAX = 0.02, 3.0, 0.01, 0.10
DOTCOM = (date(2000, 3, 1), date(2002, 10, 1))  # monthly levels: start of 2000-03 .. 2002-10
GFC_M = (date(2007, 10, 1), date(2009, 3, 1))
GFC = (date(2007, 10, 9), date(2009, 3, 9))
NAMES = {"T": "T trend (tsmom12 + 5/25)", "H": "H hold7 (EW + 5/25)", "M": "M mix60 (60/40 + 5%)"}


def fixed(mix: Mapping[str, float]) -> c.ResearchStrategy:
    return c.weekly(lambda view: {s: w for s, w in mix.items() if c.eligible(view, s)})


def simulate(
    variant: str | None, decs: list[gym.Decision], syms: Sequence[str],
    costs: Mapping[str, gym.Costs], band: float, st: eu2.FeeState, kind: str, start: date,
) -> eu5.Out:  # fmt: skip
    """As eu5.simulate, under idea eu-6 and with its own start date."""
    hist, _ = eu1.panel_for(syms)
    with eu2.fixed_fees(st):
        res = gym.simulate(decs, hist, costs=costs, band=band)
    sc = report.score(f"{IDEA}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    expo = float(np.mean([sum(d.weights.values()) for d in decs]))
    run = Run(IDEA, variant or "-", "train", sc, days, equity, expo, decs)
    if variant is not None:
        path = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
        if not path.exists():
            harness._log(run, kind, start, TRAIN_END)
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("w", newline="") as f:
                w = csv.writer(f, lineterminator="\n")
                w.writerow(["date", "equity"])
                w.writerows((d.isoformat(), repr(float(e))) for d, e in zip(days, equity))  # noqa: B905
            print("logged", variant, flush=True)
        else:
            print("re-scored", variant, flush=True)
    years = (days[-1] - days[0]).days / 365
    en, ex, ot = eu3.count_fills(res.fills)
    return eu5.Out(run, res, st.orders / years, en / years, ex / years, ot / years,
                   st.paid / years)  # fmt: skip


def saved(path_parts: Sequence[str]) -> np.ndarray | None:
    path = harness.DATA.joinpath("runs", *path_parts)
    if not path.exists():
        return None
    with path.open() as f:
        return np.array([float(r["equity"]) for r in csv.DictReader(f)])


# ---- the long monthly proxy (stocks, 10y Treasuries, gold; 1971-2025) ----


def _shiller_stock() -> list[tuple[date, float]]:
    """(month m, gross total return m -> m+1) = (P[m+1] + D[m]/12) / P[m] (monthly averages)."""
    import importlib

    xlrd = importlib.import_module("xlrd")
    path = long_bond.cache_root() / "shiller" / "ie_data.xls"
    sheet = xlrd.open_workbook(str(path)).sheet_by_name("Data")
    rows = [sheet.row_values(i) for i in range(sheet.nrows)]
    h = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
    if rows[h][1] != "P" or rows[h][2] != "D":
        raise ValueError("unexpected Shiller columns")
    pd = []
    for r in rows[h + 1 :]:
        if isinstance(r[0], float) and isinstance(r[1], float) and isinstance(r[2], float):
            pd.append((long_bond._month(r[0]), r[1], r[2]))
    return [(m, (p1 + d / 12) / p) for (m, p, d), (_, p1, _) in zip(pd, pd[1:], strict=False)]


def proxy_returns() -> tuple[list[date], np.ndarray]:
    """Months m (1971-01 .. 2025-09) and gross returns m -> m+1 of [stocks, bonds, gold]."""
    st = dict(_shiller_stock())
    bd = dict(long_bond.load())
    gp = long_gold.load()
    gd = {a: p1 / p0 for (a, p0), (_, p1) in zip(gp, gp[1:], strict=False)}  # label = start month
    months, out = [], []
    m = long_gold.FREE_FROM
    while m <= date(2025, 9, 1):
        if not (m in st and m in bd and m in gd):
            raise ValueError(f"proxy gap at {m}")
        months.append(m)
        out.append([st[m], bd[m], gd[m]])
        m = long_gold._next(m)
    return months, np.array(out)


Proxy = dict[str, tuple[list[date], np.ndarray, float]]


def proxy_books(months: list[date], r: np.ndarray) -> Proxy:
    """Monthly net returns from the first month with a lagged 12-month signal; and turnover/yr."""
    first = 13  # signal at m uses r[m-13 .. m-2]: L[m-1] / L[m-13]
    out = {}
    for key in ("T", "H", "M"):
        rets, turn = [], 0.0
        w_prev = np.zeros(3)
        for i in range(first, len(months)):
            if key == "T":
                sig = np.prod(r[i - 13 : i - 1], axis=0) > 1
                w = np.where(sig, 1 / 3, 0.0)
            elif key == "H":
                w = np.full(3, 1 / 3)
            else:
                w = np.array([0.6, 0.4, 0.0])
            turn += float(np.abs(w - w_prev).sum())
            gross = float(w @ r[i] + (1 - w.sum()))
            rets.append(gross - 1)
            w_prev = w * r[i] / gross  # drifted weights at month end
        years = len(rets) / 12
        out[key] = (months[first:], np.array(rets), turn / years)
    return out


def m_window(ms: list[date], rets: np.ndarray, a: date, b: date) -> float:
    """Return from the level at the start of month a to the start of month b."""
    sel = [x for m, x in zip(ms, rets, strict=True) if a <= m < b]
    return float(np.prod(1 + np.array(sel)) - 1)


def m_stats(rets: np.ndarray) -> dict[str, float]:
    lev = np.concatenate([[1.0], np.cumprod(1 + rets)])
    return {
        "sharpe": float(rets.mean() / rets.std() * math.sqrt(12)),
        "cagr": float(lev[-1] ** (12 / len(rets)) - 1),
        "ret": float(lev[-1] - 1),
        "mdd": float((1 - lev / np.maximum.accumulate(lev)).max()),
    }


def log_monthly(variant: str, kind: str, ms: list[date], rets: np.ndarray, turn: float) -> None:
    flag = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    if flag.exists():
        print("re-scored", variant, flush=True)
        return
    s = m_stats(rets)
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | {kind} | train | {ms[0]} | "
        f"{ms[-1]} | {s['sharpe']:.2f} | {s['ret']:+.1%} | {s['mdd']:.1%} | {turn:.2f} |\n"
    )
    with harness.TRIES.open("a") as f:
        f.write(row)
    flag.parent.mkdir(parents=True, exist_ok=True)
    with flag.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["month", "ret"])
        w.writerows((m.isoformat(), repr(float(x))) for m, x in zip(ms, rets, strict=True))
    print("logged", variant, flush=True)


# ---- the human criteria ----


def underwater_months(run: Run) -> float:
    eq = run.equity
    peak, start, worst = eq[0], 0, 0
    for i, e in enumerate(eq):
        if e >= peak:
            worst = max(worst, i - start)
            peak, start = e, i
    worst = max(worst, len(eq) - 1 - start)
    return worst / 30.44


def worst_12m(run: Run) -> float:
    eq = run.equity
    return float((eq[365:] / eq[:-365] - 1).min())


def boot(a: Run, b: Run) -> tuple[float, float, float, float, float]:
    """(Sharpe a - b, bootstrap SE, 5%, 95%, one-sided p for 'a better'); protocol settings."""
    x, y = c.align(a, b)
    rng = np.random.default_rng(0)
    diffs = np.empty(2000)
    for k in range(2000):
        i = stats._stationary_indices(len(x), 20, rng)
        diffs[k] = stats.sharpe(x[i]) - stats.sharpe(y[i])
    return (
        stats.sharpe(x) - stats.sharpe(y), float(diffs.std()), float(np.quantile(diffs, 0.05)),
        float(np.quantile(diffs, 0.95)), float((diffs <= 0).mean()),
    )  # fmt: skip


def euw_setups(pan: harness.Panel) -> dict[str, tuple[list[gym.Decision], float]]:
    return {
        "T": (eu5.r_decisions(pan), BAND_7),
        "H": (harness.decisions(eu1.EW, pan, W_START, TRAIN_END), BAND_7),
        "M": (harness.decisions(fixed(MIX_EU), pan, W_START, TRAIN_END), BAND_MIX),
    }


def check() -> None:
    zero = eu2.FeeState
    _, pan = eu1.panel_for(EUW)
    su = euw_setups(pan)
    t = simulate(None, su["T"][0], EUW, eu2.COSTS, BAND_7, zero(0, 0), "", W_START)
    ref = saved(["eu-5", "D2-band25r@euw", "slip.train.csv"])
    if ref is None or not np.allclose(ref, t.run.equity, rtol=1e-12):
        raise AssertionError("T differs from eu-5's saved D2 run")
    h1 = simulate(None, su["H"][0], EUW, eu2.COSTS, eu3.BAND, zero(0, 0), "", W_START)
    ref = saved(["eu-3", "equal-weight@euw", "slip.train.csv"])
    if ref is None or not np.allclose(ref, h1.run.equity, rtol=1e-12):
        raise AssertionError("H at the 1% band differs from eu-3's saved equal-weight run")
    for d in su["M"][0]:
        if set(d.weights) != set(MIX_EU) or any(abs(d.weights[s] - 0.2) > 1e-9 for s in MIX_EU):
            raise AssertionError(f"mix weights off on {d.time}")
    _, pu = eu1.panel_for(USW)
    for d in harness.decisions(fixed(MIX_US), pu, US_START, TRAIN_END):
        if set(d.weights) != set(MIX_US):
            raise AssertionError(f"US mix incomplete on {d.time}")
    ms, r = proxy_returns()
    if len(ms) != (2025 - 1971) * 12 + 9 or not np.all(r > 0):
        raise AssertionError("proxy months missing")
    print("check ok", flush=True)


def report_all() -> None:
    check()
    zero = eu2.FeeState
    _, pan = eu1.panel_for(EUW)
    su = euw_setups(pan)
    years_w = (TRAIN_END - W_START).days / 365

    # no fee
    out0: dict[str, eu5.Out] = {
        "T": eu5.simulate("D2-band25r@euw/slip", su["T"][0], EUW, eu2.COSTS, BAND_7, zero(0, 0),
                          "variant"),
        "H": simulate("hold7@euw/slip", su["H"][0], EUW, eu2.COSTS, BAND_7, zero(0, 0),
                      "baseline", W_START),
        "M": simulate("mix60@euw/slip", su["M"][0], EUW, eu2.COSTS, BAND_MIX, zero(0, 0),
                      "baseline", W_START),
    }  # fmt: skip
    for k, o in out0.items():
        o.run.variant = NAMES[k]
    r_ref = eu3.simulate("tsmom12@euw/slip", eu3.make_decisions(eu3.R, pan), EUW, zero(0, 0),
                         "robustness")  # fmt: skip
    r_ref.run.variant = "R tsmom12 (1% band, ref)"
    ew_ref = eu3.simulate("equal-weight@euw/slip", su["H"][0], EUW, zero(0, 0), "baseline")
    ew_ref.run.variant = "EW (1% band, ref)"

    # 2008 US proxy (usw, USD, from 2007-03-01)
    _, pu = eu1.panel_for(USW)
    gcost = eu1.COSTS["gym"]
    us = {
        "T": simulate("trend525@usw-2007", harness.decisions(eu1.TSMOM, pu, US_START, TRAIN_END),
                      USW, gcost, BAND_7, zero(0, 0), "robustness", US_START),
        "H": simulate("hold7@usw-2007", harness.decisions(eu1.EW, pu, US_START, TRAIN_END), USW,
                      gcost, BAND_7, zero(0, 0), "baseline", US_START),
        "M": simulate("mix60@usw-2007", harness.decisions(fixed(MIX_US), pu, US_START,
                      TRAIN_END), USW, gcost, BAND_MIX, zero(0, 0), "baseline", US_START),
    }  # fmt: skip
    for k, o in us.items():
        o.run.variant = f"{k} @usw 2007-"

    # long monthly proxy
    ms, rr = proxy_returns()
    lp = proxy_books(ms, rr)
    for k, kind in (("T", "robustness"), ("H", "baseline"), ("M", "baseline")):
        mm, rets, turn = lp[k]
        log_monthly(f"{k.lower()}-proxy@long-monthly", kind, mm, rets, turn)

    keys = ["T", "H", "M"]
    txt = ["# eu-6 results: trend vs holding vs 60/40 on `euw` (cards/eu-6.md)", ""]
    txt += [
        "Train only. `euw` in EUR, window W (decisions 2012-01-02 .. 2025-11-09), total-return "
        "prices, ETF slippage 0.05% a side, cash at 0. T = `tsmom12` + 5/25 band (eu-5's D2, "
        "re-scored); H = equal weight of the seven + 5/25 band (3.57%); M = SXR8, EXSA, IQQE, "
        "IBGS, IBGL 20% each + 5% band. Sharpe on calendar days, zero risk-free rate.",
        "",
        "## 1. The human criteria at no fixed fee",
        "",
        "| Rule | Sharpe (SE) | CAGR | Vol | Worst loss (max DD) | Longest under water | "
        "Worst 12 months | Orders/yr | Avg exposure |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    crit: dict[str, dict[str, float]] = {}
    for k in keys:
        o = out0[k]
        d = c.describe(o.run)
        crit[k] = {"sharpe": d["sharpe"], "mdd": d["mdd"], "uw": underwater_months(o.run),
                   "w12": worst_12m(o.run), "orders": o.orders_yr}  # fmt: skip
        txt.append(
            f"| {o.run.variant} | {d['sharpe']:.2f} ({d['se']:.2f}) | {d['cagr']:+.1%} | "
            f"{d['vol']:.1%} | {d['mdd']:.1%} | {crit[k]['uw']:.0f} mo | {crit[k]['w12']:+.1%} | "
            f"{o.orders_yr:.1f} | {d['exposure']:.0%} |"
        )
    for o in (r_ref, ew_ref):
        d = c.describe(o.run)
        txt.append(
            f"| {o.run.variant} | {d['sharpe']:.2f} ({d['se']:.2f}) | {d['cagr']:+.1%} | "
            f"{d['vol']:.1%} | {d['mdd']:.1%} | {underwater_months(o.run):.0f} mo | "
            f"{worst_12m(o.run):+.1%} | {o.orders_yr:.1f} | {d['exposure']:.0%} |"
        )
    # descriptive: H scaled to T's vol
    vt, vh = c.describe(out0["T"].run)["vol"], c.describe(out0["H"].run)["vol"]
    k_sc = vt / vh
    hs = out0["H"].run.rets * k_sc
    eq_s = np.concatenate([[1.0], np.cumprod(1 + hs)])
    sc_run = Run(IDEA, "H scaled", "train", out0["H"].run.score, out0["H"].run.days, eq_s, 0, [])
    txt += [
        "",
        f"Descriptive (no row, hindsight constant): H scaled to T's vol ({k_sc:.0%} invested, "
        f"rest cash at 0): Sharpe {stats.sharpe(hs):.2f}, CAGR {stats.cagr(hs):+.1%}, worst loss "
        f"{stats.max_drawdown(hs):.1%}, longest under water {underwater_months(sc_run):.0f} mo, "
        f"worst 12 months {worst_12m(sc_run):+.1%}.",
        "",
        "## 2. Sharpe differences and their uncertainty (no fixed fee)",
        "",
        f"Paired stationary bootstrap (block 20 days, 2,000 draws). A lead is real only at p < "
        f"{P_REAL:.3f} (three comparisons).",
        "",
        "| Pair | dSharpe | Bootstrap SE | 90% range | p (first better) | p (second better) |",
        "|---|---:|---:|---|---:|---:|",
    ]
    for a, b in (("T", "H"), ("T", "M"), ("H", "M")):
        dd, se, lo, hi, p = boot(out0[a].run, out0[b].run)
        txt.append(f"| {a} - {b} | {dd:+.2f} | {se:.2f} | {lo:+.2f} .. {hi:+.2f} | {p:.2f} | "
                   f"{1 - p:.2f} |")  # fmt: skip

    # crash windows
    crash_names = [n for n, _, _ in e4.inside_crashes()]
    cr = {k: e4.crash_rets(out0[k].run) for k in keys}
    gfc = {k: eu1.crash_ret(us[k].run, *GFC) for k in keys}
    dot = {k: m_window(lp[k][0], lp[k][1], *DOTCOM) for k in keys}
    gfc_m = {k: m_window(lp[k][0], lp[k][1], *GFC_M) for k in keys}
    windows = [("2000-02 (long monthly proxy)", dot), ("2008 (usw proxy, USD)", gfc)]
    windows += [(n, {k: cr[k][i] for k in keys}) for i, n in enumerate(crash_names)]
    txt += ["", "## 3. Crash windows (total return inside each)", ""]
    txt += ["| Window | " + " | ".join(NAMES[k] for k in keys) + " | Best (within 1 pt) |",
            "|---|---:|---:|---:|---|"]  # fmt: skip
    wins = {k: 0 for k in keys}
    for n, vals in windows:
        top = max(vals.values())
        best = [k for k in keys if vals[k] >= top - CRASH_TIE]
        for k in best:
            wins[k] += 1
        txt.append(f"| {n} | " + " | ".join(f"{vals[k]:+.1%}" for k in keys)
                   + f" | {', '.join(best)} |")  # fmt: skip
    txt.append("| 2008, second view (long monthly proxy; not counted) | "
               + " | ".join(f"{gfc_m[k]:+.1%}" for k in keys) + " | - |")  # fmt: skip
    txt += ["", "Windows won (of 6): " + ", ".join(f"{k} {wins[k]}" for k in keys) + ".", ""]
    txt += [
        "Proxy books in full (shown, not judged):",
        "",
        c.table([us[k].run for k in keys], versus=us["T"].run),
        "",
        "Long monthly proxy (stocks / 10y Treasuries / gold, 1972-2025, monthly averages, cash "
        "at 0, no fees; Sharpe from monthly returns):",
        "",
        "| Rule | Sharpe | CAGR | Max DD | Turnover/yr |",
        "|---|---:|---:|---:|---:|",
    ]
    for k in keys:
        s = m_stats(lp[k][1])
        txt.append(f"| {k} proxy | {s['sharpe']:.2f} | {s['cagr']:+.1%} | {s['mdd']:.1%} | "
                   f"{lp[k][2]:.2f} |")  # fmt: skip

    # fees
    txt += ["", "## 4. Fixed fees by tier and book", ""]
    txt += [
        "Loss = own Sharpe at no fee minus Sharpe at the tier. Winner (P1) = highest Sharpe at the "
        f"cell; 'real' only if the bootstrap p of the leader vs the runner-up < {P_REAL:.3f}, "
        "else a tie, decided by fewer orders a year (at no fee).",
        "",
        "| Tier | Book | T Sharpe (loss; orders; fees/yr) | H Sharpe (loss; orders; fees/yr) | "
        "M Sharpe (loss; orders; fees/yr) | P1 winner | T fee loss <= 0.10 |",
        "|---|---:|---|---|---|---|---|",
    ]
    p1: dict[tuple[str, int], str] = {}
    t_ok: dict[tuple[str, int], bool] = {}
    by_orders = sorted(keys, key=lambda k: crit[k]["orders"])
    for tname, ttag, sch in TIERS:
        for size in SIZES:
            cell: dict[str, eu5.Out] = {}
            for k in keys:
                st = zero(sch.per_order / size, sch.per_year / size)
                if k == "T":
                    cell[k] = eu5.simulate(f"D2-band25r@euw/{ttag}-{size // 1000}k", su["T"][0],
                                           EUW, eu2.COSTS, BAND_7, st, "variant")  # fmt: skip
                else:
                    name = {"H": "hold7", "M": "mix60"}[k]
                    cell[k] = simulate(f"{name}@euw/{ttag}-{size // 1000}k", su[k][0], EUW,
                                       eu2.COSTS, su[k][1], st, "baseline", W_START)  # fmt: skip
            shs = {k: c.describe(cell[k].run)["sharpe"] for k in keys}
            ranked = sorted(keys, key=lambda k: -shs[k])
            _, _, _, _, p = boot(cell[ranked[0]].run, cell[ranked[1]].run)
            if p < P_REAL:
                win = f"{ranked[0]} (real, p={p:.3f})"
                p1[(tname, size)] = ranked[0]
            else:
                tied = [k for k in by_orders if k in ranked[:2]]
                win = f"tie {ranked[0]}~{ranked[1]} (p={p:.2f}) -> {tied[0]}"
                p1[(tname, size)] = tied[0]
            t_loss = crit["T"]["sharpe"] - shs["T"]
            t_ok[(tname, size)] = t_loss <= LOSS_MAX
            parts = []
            for k in keys:
                parts.append(f"{shs[k]:.2f} ({crit[k]['sharpe'] - shs[k]:.3f}; "
                             f"{cell[k].orders_yr:.1f}; {cell[k].fees_yr:.2%})")  # fmt: skip
            txt.append(f"| {tname} | {size // 1000}k | " + " | ".join(parts)
                       + f" | {win} | {'yes' if t_ok[(tname, size)] else 'no'} |")  # fmt: skip

    # preferences
    def tie_pick(cands: list[str]) -> str:
        return min(cands, key=lambda k: crit[k]["orders"])

    lo_dd = min(crit[k]["mdd"] for k in keys)
    p2c = [k for k in keys if crit[k]["mdd"] <= lo_dd + DD_TIE]
    p2 = p2c[0] if len(p2c) == 1 else max(p2c, key=lambda k: crit[k]["w12"])
    lo_uw = min(crit[k]["uw"] for k in keys)
    p3c = [k for k in keys if crit[k]["uw"] <= lo_uw + UW_TIE]
    p3 = tie_pick(p3c)
    top_w = max(wins.values())
    p4 = tie_pick([k for k in keys if wins[k] == top_w])
    p5 = by_orders[0]
    txt += [
        "",
        "## 5. Which wins under which preference",
        "",
        "| Preference | Winner | Why |",
        "|---|---|---|",
        "| P1 Sharpe after fees | per cell, table 4 | "
        + ", ".join(f"{t} {s // 1000}k: {p1[(t, s)]}" for t, _, _ in TIERS for s in SIZES)
        + " |",
        f"| P2 worst loss | **{p2}** | max DD "
        + ", ".join(f"{k} {crit[k]['mdd']:.1%}" for k in keys)
        + f"; tie band {DD_TIE:.0%} "
        f"(candidates {', '.join(p2c)}; then worst 12 months) |",
        f"| P3 waiting | **{p3}** | longest under water "
        + ", ".join(f"{k} {crit[k]['uw']:.0f} mo" for k in keys)
        + f" (tie band 3 mo: "
        f"{', '.join(p3c)}; then fewer orders) |",
        f"| P4 crash insurance | **{p4}** | windows won of 6: "
        + ", ".join(f"{k} {wins[k]}" for k in keys)
        + " |",
        f"| P5 cost | **{p5}** | orders/yr "
        + ", ".join(f"{k} {crit[k]['orders']:.1f}" for k in keys)
        + " |",
        "",
        "## 6. Is trend worth it? (T wins the preference and T's fee loss <= 0.10)",
        "",
        "| Preference | "
        + " | ".join(f"{t} {s // 1000}k" for t, _, _ in TIERS for s in SIZES)
        + " |",
        "|---|" + "---|" * (len(TIERS) * len(SIZES)),
    ]
    for pname, winner in (("P1 Sharpe", None), ("P2 worst loss", p2), ("P3 waiting", p3),
                          ("P4 crash insurance", p4), ("P5 cost", p5)):  # fmt: skip
        cells = []
        for t, _, _ in TIERS:
            for s in SIZES:
                w = p1[(t, s)] if winner is None else winner
                cells.append("**yes**" if w == "T" and t_ok[(t, s)] else "no")
        txt.append(f"| {pname} | " + " | ".join(cells) + " |")
    txt += ["", f"Window W is {years_w:.1f} years."]
    c.write_result(IDEA, "\n".join(txt))


if __name__ == "__main__":
    {"check": check, "run": report_all}[sys.argv[1]]()
