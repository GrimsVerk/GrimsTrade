"""eu-8: idle cash earning a money-market rate (step 1) for the small coin-free euro book
(cards/eu-8.md).

    uv run python research/lib/eu8.py fetch                            # ECB rates, keyless
    uv run --with numpy --with xlrd python research/lib/eu8.py check   # plumbing: no number
    uv run --with numpy --with xlrd python research/lib/eu8.py cash    # step 1: 16 rows

Needs what eu7.py needs (CSVs from `eu1_data.py build`, the git-ignored saved runs of eu-3, eu-5,
eu-6, eu-7 under research/data/runs/, Shiller and gold files in the cache root of
research/macro.local.json) plus the two ECB files that `fetch` saves under the same cache root.
Every new row goes to tries.md (idea `eu-8`); a row whose flag file exists under
research/data/runs/eu-8/ is not logged again. Train period only.
"""

from __future__ import annotations

import bisect
import csv
import subprocess
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date

import common as c
import eu1
import eu2
import eu4_run as e4
import eu5
import eu6
import eu7
import harness
import long_bond
import numpy as np
import stats
from harness import TRAIN_END, TRAIN_LAST_BAR, Run

from grimstrade import data, gym

IDEA = "eu-8"
W_START = eu1.W_START
EUW, USW = eu1.EUW, eu1.USW
US_START = eu6.US_START
N_FAMILY = 12
P_FAM = 0.10 / N_FAMILY
ESTR_FROM = date(2019, 10, 1)
ECB_DIR = "ecb-2026-11-18"
ECB_FILES = {
    "eonia_m.csv": "https://data-api.ecb.europa.eu/service/data/FM/"
    "M.U2.EUR.4F.MM.EONIA.HSTA?format=csvdata",
    "estr.csv": "https://data-api.ecb.europa.eu/service/data/EST/B.EU000A2X2A25.WT?format=csvdata",
}
NAMES = {
    "T": "T trend (tsmom12, all seven)",
    "B": "B hold7 + 33% cash",
    "H": "H hold7",
    "M": "M mix60",
}
KEYS1 = ["T", "B", "H", "M"]
JUDGED1 = ["T", "B", "H"]  # eu-7's preferences were among T, A, B, H; A is not re-scored here
RateFn = Callable[[date], float]  # daily rate (already divided by the day count)


# ---- the rates ----


def fetch() -> None:
    out = long_bond.cache_root() / ECB_DIR
    out.mkdir(parents=True, exist_ok=True)
    for name, url in ECB_FILES.items():
        subprocess.run(["curl", "-sf", "-o", str(out / name), url], check=True)
        print("saved", out / name, flush=True)


def _ecb(name: str) -> list[tuple[str, float]]:
    path = long_bond.cache_root() / ECB_DIR / name
    with path.open(newline="") as f:
        return [(r["TIME_PERIOD"], float(r["OBS_VALUE"]) / 100) for r in csv.DictReader(f)]


def eur_rate(floor: bool) -> RateFn:
    """EONIA monthly average before 2019-10-01, EUR STR (last print) after; ACT/360."""
    monthly = dict(_ecb("eonia_m.csv"))
    est = [(date.fromisoformat(t), v) for t, v in _ecb("estr.csv")]
    est = [(d, v) for d, v in est if d <= TRAIN_LAST_BAR]
    ed, ev = [d for d, _ in est], [v for _, v in est]

    def f(d: date) -> float:
        if d < ESTR_FROM:
            y = monthly[f"{d.year}-{d.month:02d}"]
        else:
            y = ev[bisect.bisect_right(ed, d) - 1]
        return (max(y, 0.0) if floor else y) / 360

    return f


def _irx() -> tuple[list[date], list[float]]:
    bars = [b for b in data.load(harness.RESEARCH, "IRX") if b.date <= TRAIN_LAST_BAR]
    return [b.date for b in bars], [b.close / 100 for b in bars]


def usd_rate() -> RateFn:
    days, ys = _irx()

    def f(d: date) -> float:
        return ys[max(bisect.bisect_right(days, d) - 1, 0)] / 365

    return f


def usd_monthly(months: Sequence[date]) -> np.ndarray:
    """Average IRX yield inside month m, / 12: cash return for the proxy month m -> m+1."""
    days, ys = _irx()
    acc: dict[tuple[int, int], list[float]] = {}
    for d, y in zip(days, ys, strict=True):
        acc.setdefault((d.year, d.month), []).append(y)
    return np.array([float(np.mean(acc[(m.year, m.month)])) / 12 for m in months])


# ---- interest on the gym's actual cash ----


def cash_share(out: eu5.Out) -> np.ndarray:
    """Share of the book in cash at the end of each calendar day of out.run."""
    flows: dict[date, float] = {}
    for fl in out.res.fills:
        d = fl.time.date()
        flows[d] = flows.get(d, 0.0) - fl.qty * fl.price - fl.fee
    days = out.run.days
    cash = np.empty(len(days))
    cur = gym.START_CASH + sum(v for d, v in flows.items() if d < days[0])
    for k, d in enumerate(days):
        cur += flows.get(d, 0.0)
        cash[k] = cur
    if abs(cash[-1] - out.res.cash) > 1e-6 * gym.START_CASH:
        raise AssertionError(f"rebuilt cash {cash[-1]:.4f} != gym cash {out.res.cash:.4f}")
    return cash / out.run.equity


@dataclass
class Paid:
    run: Run  # equity with interest on cash
    rf: np.ndarray  # the daily rate, aligned to run.rets
    out: eu5.Out

    @property
    def excess(self) -> np.ndarray:
        return self.run.rets - self.rf


def with_interest(out: eu5.Out, rate: RateFn, name: str) -> Paid:
    share = cash_share(out)
    days = out.run.days
    rf = np.array([rate(d) for d in days[1:]])
    r = out.run.rets + share[:-1] * rf
    eq = gym.START_CASH * np.concatenate([[1.0], np.cumprod(1 + r)])
    o = out.run
    return Paid(Run(IDEA, name, "train", o.score, days, eq, o.exposure, o.decisions), rf, out)


def log_row(p: Paid, kind: str, start: date) -> None:
    path = harness.DATA / "runs" / IDEA / f"{p.run.variant}.train.csv"
    if path.exists():
        print("re-scored", p.run.variant, flush=True)
        return
    harness._log(p.run, kind, start, TRAIN_END)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "equity"])
        w.writerows((d.isoformat(), repr(float(x))) for d, x in zip(p.run.days, p.run.equity,
                                                                      strict=True))  # fmt: skip
    print("logged", p.run.variant, flush=True)


def log_monthly(variant: str, kind: str, ms: list[date], rets: np.ndarray, turn: float) -> None:
    old = eu6.IDEA
    eu6.IDEA = IDEA  # eu6.log_monthly files the row and the flag under its module's IDEA
    try:
        eu6.log_monthly(variant, kind, ms, rets, turn)
    finally:
        eu6.IDEA = old


def boot_arr(x: np.ndarray, y: np.ndarray) -> tuple[float, float, float, float, float]:
    """As eu6.boot, on two aligned return arrays."""
    rng = np.random.default_rng(0)
    diffs = np.empty(2000)
    for k in range(2000):
        i = stats._stationary_indices(len(x), 20, rng)
        diffs[k] = stats.sharpe(x[i]) - stats.sharpe(y[i])
    return (
        stats.sharpe(x) - stats.sharpe(y), float(diffs.std()), float(np.quantile(diffs, 0.05)),
        float(np.quantile(diffs, 0.95)), float((diffs <= 0).mean()),
    )  # fmt: skip


# ---- the long monthly proxy with interest on cash ----


Weigher = Callable[[np.ndarray, int], np.ndarray]


def proxy_weights(e: float) -> dict[str, Weigher]:
    """eu-6's T/H/M and eu-7's B on [stocks, bonds, gold]; signal from r[i-13 .. i-2]."""
    return {
        "T": lambda r, i: np.where(np.prod(r[i - 13 : i - 1], axis=0) > 1, 1 / 3, 0.0),
        "H": lambda r, i: np.full(3, 1 / 3),
        "M": lambda r, i: np.array([0.6, 0.4, 0.0]),
        "B": lambda r, i: np.full(3, e / 3),
    }


def proxy_paid(
    months: list[date], r: np.ndarray, rf: np.ndarray, weigh: Weigher, rate_on: bool = True
) -> tuple[list[date], np.ndarray, np.ndarray, float]:
    """(months, net returns, cash rate per month, turnover/yr) from month 13 on."""
    first = 13
    rets, turn, w_prev = [], 0.0, np.zeros(3)
    for i in range(first, len(months)):
        w = weigh(r, i)
        turn += float(np.abs(w - w_prev).sum())
        cash = 1 - w.sum()
        gross = float(w @ r[i] + cash * (1 + (rf[i] if rate_on else 0.0)))
        rets.append(gross - 1)
        w_prev = w * r[i] / gross
    return months[first:], np.array(rets), rf[first:], turn / (len(rets) / 12)


def months_stats(rets: np.ndarray, rf: np.ndarray) -> dict[str, float]:
    s = eu6.m_stats(rets)
    ex = rets - rf
    s["xsharpe"] = float(ex.mean() / ex.std() * np.sqrt(12))
    return s


# ---- shared runs ----


def euw_outs() -> tuple[dict[str, eu5.Out], float]:
    """T, B, H, M on euw at no fixed fee (no rows: these are eu-5/6/7's runs)."""
    zero = eu2.FeeState
    _, pan = eu1.panel_for(EUW)
    dec = eu7.euw_decisions(pan)
    e = eu7.exposure(dec["T"])
    m_decs = harness.decisions(eu6.fixed(eu6.MIX_EU), pan, W_START, TRAIN_END)
    sim = eu6.simulate
    outs = {
        "T": sim(None, dec["T"], EUW, eu2.COSTS, eu7.BAND_7, zero(0, 0), "", W_START),
        "B": sim(None, dec["B"], EUW, eu2.COSTS, eu7.b_band(e), zero(0, 0), "", W_START),
        "H": sim(None, dec["H"], EUW, eu2.COSTS, eu7.BAND_7, zero(0, 0), "", W_START),
        "M": sim(None, m_decs, EUW, eu2.COSTS, eu6.BAND_MIX, zero(0, 0), "", W_START),
    }
    return outs, e


def usw_outs(e: float, end: date = TRAIN_END) -> dict[str, eu5.Out]:
    zero = eu2.FeeState
    _, pu = eu1.panel_for(USW)
    g = eu1.COSTS["gym"]
    sim = eu6.simulate

    def dec(f: c.ResearchStrategy) -> list[gym.Decision]:
        return harness.decisions(f, pu, US_START, end)

    return {
        "T": sim(None, dec(eu1.TSMOM), USW, g, eu7.BAND_7, zero(0, 0), "", US_START),
        "B": sim(None, dec(eu7.b_strategy(e)), USW, g, eu7.b_band(e), zero(0, 0), "", US_START),
        "H": sim(None, dec(eu1.EW), USW, g, eu7.BAND_7, zero(0, 0), "", US_START),
        "M": sim(None, dec(eu6.fixed(eu6.MIX_US)), USW, g, eu6.BAND_MIX, zero(0, 0), "",
                 US_START),
    }  # fmt: skip


# ---- plumbing ----


def check() -> None:
    eu7.check()
    outs, e = euw_outs()
    for k, o in outs.items():
        sh = cash_share(o)  # raises if the rebuilt cash path misses the gym's final cash
        if not (np.all(sh > -1e-9) and np.all(sh < 1 + 1e-9)):
            raise AssertionError(f"{k}: cash share outside [0, 1]")
        ref = eu6.saved(["eu-7", "hold7cash@euw", "slip.train.csv"]) if k == "B" else None
        if ref is not None and not np.allclose(ref, o.run.equity, rtol=1e-12):
            raise AssertionError("B differs from eu-7's saved run")
    zero_rate: RateFn = lambda d: 0.0  # noqa: E731
    p = with_interest(outs["T"], zero_rate, "x")
    if not np.allclose(p.run.equity, outs["T"].run.equity, rtol=1e-12):
        raise AssertionError("a zero rate must leave the equity unchanged")
    for floor in (False, True):
        f = eur_rate(floor)
        for d in (W_START, ESTR_FROM, TRAIN_END):
            f(d)  # every day of W has a rate
    for o in usw_outs(e).values():
        cash_share(o)
    ms, _ = eu6.proxy_returns()
    if len(usd_monthly(ms)) != len(ms):
        raise AssertionError("monthly rate gap")
    print("check ok", flush=True)


# ---- step 1: the report ----


def crit(p: Paid) -> dict[str, float]:
    r, x = p.run.rets, p.excess
    return {
        "xsharpe": stats.sharpe(x), "sharpe": stats.sharpe(r), "se": stats.sharpe_se(x),
        "cagr": stats.cagr(r), "vol": stats.vol(r), "mdd": stats.max_drawdown(r),
        "uw": eu6.underwater_months(p.run), "w12": eu6.worst_12m(p.run),
        "orders": p.out.orders_yr, "rate": float(np.mean(p.rf) * 365),
        "cash": float(np.mean(cash_share(p.out))),
    }  # fmt: skip


def prefs(cr: Mapping[str, Mapping[str, float]], wins: Mapping[str, int],
          keys: Sequence[str]) -> dict[str, str]:  # fmt: skip
    """eu-7's P2-P5 rules among keys; P1 at no fee on the excess Sharpe."""

    def few(ks: list[str]) -> str:
        return min(ks, key=lambda k: cr[k]["orders"])

    lo_dd = min(cr[k]["mdd"] for k in keys)
    p2c = [k for k in keys if cr[k]["mdd"] <= lo_dd + eu7.DD_TIE]
    lo_uw = min(cr[k]["uw"] for k in keys)
    top = max(wins[k] for k in keys)
    best = sorted(keys, key=lambda k: -cr[k]["xsharpe"])
    return {
        "P1": best[0],
        "P2": p2c[0] if len(p2c) == 1 else max(p2c, key=lambda k: cr[k]["w12"]),
        "P3": few([k for k in keys if cr[k]["uw"] <= lo_uw + eu7.UW_TIE]),
        "P4": few([k for k in keys if wins[k] == top]),
        "P5": few(list(keys)),
    }


def crash_table(
    rows: Mapping[str, Mapping[str, float]], keys: Sequence[str], judged: Sequence[str]
) -> tuple[list[str], dict[str, int]]:
    wins = {k: 0 for k in judged}
    lines = []
    for n, vals in rows.items():
        top = max(vals[k] for k in judged)
        best = [k for k in judged if vals[k] >= top - eu7.CRASH_TIE]
        for k in best:
            wins[k] += 1
        lines.append(f"| {n} | " + " | ".join(f"{vals[k]:+.1%}" for k in keys)
                     + f" | {', '.join(best)} |")  # fmt: skip
    return lines, wins


def step1() -> None:
    check()
    outs, e = euw_outs()
    rates = {"a": eur_rate(False), "b": eur_rate(True)}
    tag = {"T": "trend525", "B": "hold7cash", "H": "hold7", "M": "mix60"}
    paid: dict[str, dict[str, Paid]] = {}
    for v, rf in rates.items():
        suffix = "estr" if v == "a" else "estr0"
        paid[v] = {k: with_interest(outs[k], rf, f"{tag[k]}-{suffix}@euw/slip") for k in KEYS1}
        for p in paid[v].values():
            log_row(p, "robustness", W_START)
    zero = {k: with_interest(outs[k], lambda d: 0.0, f"{tag[k]}@euw (cash 0)") for k in KEYS1}

    us_o = usw_outs(e)
    ur = usd_rate()
    us = {k: with_interest(us_o[k], ur, f"{tag[k]}-irx@usw-2007") for k in KEYS1}
    for p in us.values():
        log_row(p, "robustness", US_START)
    us0 = {k: with_interest(us_o[k], lambda d: 0.0, k) for k in KEYS1}

    ms, rr = eu6.proxy_returns()
    rfm = usd_monthly(ms)
    pw = proxy_weights(e)
    lp = {k: proxy_paid(ms, rr, rfm, pw[k]) for k in KEYS1}
    lp0 = {k: proxy_paid(ms, rr, rfm, pw[k], rate_on=False) for k in KEYS1}
    for k in KEYS1:
        mm, rets, _, turn = lp[k]
        log_monthly(f"{tag[k]}-irx-proxy@long-monthly", "robustness", mm, rets, turn)

    def windows(pp: Mapping[str, Paid], usp: Mapping[str, Paid],
                lpp: Mapping[str, tuple]) -> dict[str, dict[str, float]]:  # fmt: skip
        names = [n for n, _, _ in e4.inside_crashes()]
        cr = {k: e4.crash_rets(pp[k].run) for k in KEYS1}
        w = {
            "2000-02 (long monthly proxy)": {
                k: eu6.m_window(lpp[k][0], lpp[k][1], *eu6.DOTCOM) for k in KEYS1},
            "2008 (usw proxy, USD)": {k: eu1.crash_ret(usp[k].run, *eu6.GFC) for k in KEYS1},
        }  # fmt: skip
        for i, n in enumerate(names):
            w[n] = {k: cr[k][i] for k in KEYS1}
        return w

    txt = ["# eu-8 step 1: idle cash earns a money-market rate (cards/eu-8.md)", ""]
    cr: dict[str, dict[str, dict[str, float]]] = {}
    cr["0"] = {k: crit(p) for k, p in zero.items()}
    for v in rates:
        cr[v] = {k: crit(p) for k, p in paid[v].items()}
    txt += [
        "Train only. `euw` in EUR, window W (decisions 2012-01-02 .. 2025-11-09), no fixed fee, "
        f"eu-6/eu-7's runs re-scored. Rate (a): ECB EONIA monthly average before 2019-10-01, EUR "
        f"STR daily after, ACT/360, negative years included (average {cr['a']['T']['rate']:.2%}"
        f" a year over W); (b): the same floored at 0 (average {cr['b']['T']['rate']:.2%}). "
        "Interest on the gym's actual end-of-day cash. Excess Sharpe = Sharpe of returns above "
        "the rate (primary); Sharpe vs 0 as before.",
        "",
        "## 1. `euw`, no fixed fee",
        "",
        "| Rule | Cash | Avg cash share | Excess Sharpe (SE) | Sharpe vs 0 | CAGR | Vol | "
        "Worst loss | Longest under water | Worst 12 months | Orders/yr |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for k in KEYS1:
        for v, lab in (("0", "0 (eu-6/7)"), ("a", "(a) EONIA/EUR STR"), ("b", "(b) floored")):
            x = cr[v][k]
            xs = "-" if v == "0" else f"{x['xsharpe']:.2f} ({x['se']:.2f})"
            txt.append(
                f"| {NAMES[k]} | {lab} | {x['cash']:.0%} | {xs} | {x['sharpe']:.2f} | "
                f"{x['cagr']:+.1%} | {x['vol']:.1%} | {x['mdd']:.1%} | {x['uw']:.0f} mo | "
                f"{x['w12']:+.1%} | {x['orders']:.1f} |"
            )
    txt += [
        "",
        "## 2. Excess-Sharpe differences, rate (a)",
        "",
        f"Paired stationary bootstrap (block 20, 2,000 draws, seed 0); real only at p < "
        f"{P_FAM:.4f}. Cash at 0 (eu-6/7) for reference.",
        "",
        "| Pair | dSharpe, cash 0 | dSharpe, rate (a) | Bootstrap SE | 90% range | "
        "p (first better) |",
        "|---|---:|---:|---:|---|---:|",
    ]
    gaps: dict[tuple[str, str], tuple[float, float, float]] = {}
    for a, b in (("B", "T"), ("H", "T"), ("M", "T"), ("B", "H"), ("H", "M")):
        d0 = cr["0"][a]["sharpe"] - cr["0"][b]["sharpe"]
        dd, se, lo, hi, p = boot_arr(paid["a"][a].excess, paid["a"][b].excess)
        gaps[(a, b)] = (d0, dd, p)
        txt.append(f"| {a} - {b} | {d0:+.2f} | {dd:+.2f} | {se:.2f} | {lo:+.2f} .. {hi:+.2f} | "
                   f"{p:.3f} |")  # fmt: skip

    w0 = windows(zero, us0, lp0)
    wa = windows(paid["a"], us, lp)
    txt += ["", "## 3. Crash windows, rate (a) (cash at 0 in brackets)", "",
            "| Window | " + " | ".join(NAMES[k] for k in KEYS1) + " | Best of T/B/H (1 pt) |",
            "|---|" + "---:|" * len(KEYS1) + "---|"]  # fmt: skip
    lines, wins = crash_table(wa, KEYS1, JUDGED1)
    _, wins0 = crash_table(w0, KEYS1, JUDGED1)
    for line, (n, vals) in zip(lines, wa.items(), strict=True):
        parts = line.split(" | ")
        cells = [f"{vals[k]:+.1%} ({w0[n][k]:+.1%})" for k in KEYS1]
        txt.append(" | ".join([parts[0], *cells, parts[-1]]))
    txt += ["", "Windows best (of 6): " + ", ".join(f"{k} {wins[k]}" for k in JUDGED1)
            + " (cash 0: " + ", ".join(f"{k} {wins0[k]}" for k in JUDGED1) + ")."]  # fmt: skip

    txt += ["", "## 4. Proxies with the US T-bill rate (IRX)", "",
            "`usw` 2007-03-01 .. 2025-11-09 (USD, daily):", "",
            "| Rule | Excess Sharpe | Sharpe vs 0 (cash 0) | CAGR (cash 0) | Worst loss (cash 0) "
            "| 2008 (cash 0) |", "|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    usc = {k: crit(us[k]) for k in KEYS1}
    usc0 = {k: crit(us0[k]) for k in KEYS1}
    for k in KEYS1:
        x, x0 = usc[k], usc0[k]
        txt.append(
            f"| {k} | {x['xsharpe']:.2f} | {x['sharpe']:.2f} ({x0['sharpe']:.2f}) | "
            f"{x['cagr']:+.1%} ({x0['cagr']:+.1%}) | {x['mdd']:.1%} ({x0['mdd']:.1%}) | "
            f"{wa['2008 (usw proxy, USD)'][k]:+.1%} ({w0['2008 (usw proxy, USD)'][k]:+.1%}) |"
        )
    txt += ["", "Long monthly proxy (stocks / 10y Treasuries / gold, 1972-2025, cash earns the "
            "month's average IRX / 12; Sharpe from monthly returns):", "",
            "| Rule | Excess Sharpe | Sharpe vs 0 (cash 0) | CAGR (cash 0) | Max DD (cash 0) |",
            "|---|---:|---:|---:|---:|"]  # fmt: skip
    lps = {k: months_stats(lp[k][1], lp[k][2]) for k in KEYS1}
    lps0 = {k: months_stats(lp0[k][1], lp0[k][2]) for k in KEYS1}
    for k in KEYS1:
        s, s0 = lps[k], lps0[k]
        txt.append(
            f"| {k} | {s['xsharpe']:.2f} | {s['sharpe']:.2f} ({s0['sharpe']:.2f}) | "
            f"{s['cagr']:+.1%} ({s0['cagr']:+.1%}) | {s['mdd']:.1%} ({s0['mdd']:.1%}) |"
        )

    # the card's K1-K8
    a, z = cr["a"], cr["0"]
    pa, p0 = prefs(a, wins, JUDGED1), prefs(z, wins0, JUDGED1)
    p0["P1"] = max(JUDGED1, key=lambda k: z[k]["sharpe"])
    order0 = sorted(KEYS1, key=lambda k: -z[k]["sharpe"])
    order_a = sorted(KEYS1, key=lambda k: -a[k]["xsharpe"])
    flips = [
        f"{x}>{y}" for i, x in enumerate(order0) for y in order0[i + 1:]
        if a[y]["xsharpe"] - a[x]["xsharpe"] > 0.05
    ]  # fmt: skip
    real = [f"{x}-{y}" for (x, y), (_, _, p) in gaps.items() if p < P_FAM or p > 1 - P_FAM]
    k1 = not flips and not real
    bt = gaps[("B", "T")][1]
    k2 = bt >= 0.05 and gaps[("B", "T")][2] >= P_FAM
    gap0 = z["H"]["cagr"] - z["T"]["cagr"]
    gapa = a["H"]["cagr"] - a["T"]["cagr"]
    k7 = usc["B"]["mdd"] >= 1.5 * usc["T"]["mdd"]
    k8 = lps["H"]["xsharpe"] - lps["T"]["xsharpe"] <= 0.05
    hold = {True: "holds", False: "**changes**"}
    txt += [
        "",
        "## 5. The card's conclusions K1-K8 (rate (a))",
        "",
        "| | eu-6/7 (cash 0) | With rate (a) | Verdict |",
        "|---|---|---|---|",
        f"| K1 Sharpe order | {' > '.join(order0)} (vs 0) | {' > '.join(order_a)} (excess); "
        f"flips > 0.05: {', '.join(flips) or 'none'}; real gaps: {', '.join(real) or 'none'} | "
        f"{hold[k1]} |",
        f"| K2 B - T Sharpe | {gaps[('B', 'T')][0]:+.2f} | {bt:+.2f} "
        f"(p {gaps[('B', 'T')][2]:.3f}) | {hold[k2]} |",
        f"| K3 P2 worst loss | {p0['P2']} | {pa['P2']} (max DD "
        + ", ".join(f"{k} {a[k]['mdd']:.1%}" for k in JUDGED1)
        + f") | {hold[pa['P2'] == 'B']} |",
        f"| K4 P3 under water | {p0['P3']} | {pa['P3']} ("
        + ", ".join(f"{k} {a[k]['uw']:.0f} mo" for k in JUDGED1)
        + f") | {hold[pa['P3'] == 'H']} |",
        f"| K5 P4 crash insurance | {p0['P4']} | {pa['P4']} (windows "
        + ", ".join(f"{k} {wins[k]}" for k in JUDGED1)
        + f") | {hold[pa['P4'] == 'T']} |",
        f"| K6 H - T CAGR | {gap0:+.1%} | {gapa:+.1%} | {hold[gap0 - gapa < 0.01]} |",
        f"| K7 2008 proxy worst loss B vs T | {usc0['B']['mdd']:.1%} vs {usc0['T']['mdd']:.1%} | "
        f"{usc['B']['mdd']:.1%} vs {usc['T']['mdd']:.1%} | {hold[k7]} |",
        f"| K8 long proxy T vs H Sharpe | {lps0['T']['sharpe']:.2f} vs {lps0['H']['sharpe']:.2f}"
        f" | {lps['T']['xsharpe']:.2f} vs {lps['H']['xsharpe']:.2f} (excess) | {hold[k8]} |",
        "",
        f"P1 at no fee (excess Sharpe, among T/B/H): {pa['P1']} (cash 0: {p0['P1']}). "
        f"Rate (b), floored, shown in table 1 only.",
    ]
    c.write_result(f"{IDEA}-cash", "\n".join(txt))


if __name__ == "__main__":
    cmds: dict[str, Callable[[], None]] = {"fetch": fetch, "check": check, "cash": step1}
    cmds[sys.argv[1]]()
