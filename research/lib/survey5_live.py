"""survey-5 live-check (card: research/cards/live-check.md). Descriptive, nothing selected.

    uv run --with openpyxl python -I research/lib/survey5_live.py <cache_root>

Reads the live fund series written by `survey5_fetch.py` and the AQR TSMOM workbook from the
cache (data only), re-scores four configurations already in `tries.md` through the harness
(`log=False`), appends one `live-check` row per configuration to `tries.md`, and writes
`research/results/live-check.md`. No month after 2025-10 of any series is read.
"""

from __future__ import annotations

import csv
import math
import sys
from collections import defaultdict
from datetime import UTC, date, datetime
from pathlib import Path
from statistics import NormalDist

sys.path.insert(0, str(Path(__file__).resolve().parent))

import cash_interest as ci  # noqa: E402
import common as c  # noqa: E402
import harness  # noqa: E402
import numpy as np  # noqa: E402
import risk_map  # noqa: E402
import stats  # noqa: E402
import trend_where as tw  # noqa: E402

IDEA = "survey-5"
LAST_MONTH = (2025, 10)  # the held-out year starts 2025-11-11: nothing later is read
L = ((2010, 2), LAST_MONTH)
L07 = ((2007, 4), LAST_MONTH)
P_AQR = ((1985, 1), (2009, 12))
P_OURS = ((1994, 2), (2009, 12))
TREND = ["RYMFX", "AQMIX", "ASFYX", "WTMF", "PQTIX", "ABYIX", "DBMF", "KMLM", "CTA"]
RISKPAR = ["ABRZX", "AQRIX", "RPAR"]
ALONE = ["LFMIX", "SPLV", "USMV", "QSPIX", "QRPIX"]
CRASH_YEARS = [2008, 2020, 2022]
H_LIT = {"Harvey-Liu ceiling (H2)": 0.25, "bank-strategy median (H1)": 0.73}

Month = tuple[int, int]
Series = dict[Month, float]


def months(a: Month, b: Month) -> list[Month]:
    out, (y, m) = [], a
    while (y, m) <= b:
        out.append((y, m))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def cut(s: Series, w: tuple[Month, Month]) -> Series:
    return {k: v for k, v in s.items() if w[0] <= k <= w[1]}


def sharpe_m(s: Series) -> float:
    x = np.array(list(s.values()))
    return float(x.mean() / x.std(ddof=1) * math.sqrt(12)) if len(x) > 12 else math.nan


def corr(a: Series, b: Series, min_n: int = 36) -> tuple[float, int]:
    ks = sorted(set(a) & set(b))
    if len(ks) < min_n:
        return math.nan, len(ks)
    x, y = np.array([a[k] for k in ks]), np.array([b[k] for k in ks])
    return float(np.corrcoef(x, y)[0, 1]), len(ks)


def compound(s: Series, keys: list[Month]) -> float:
    if not all(k in s for k in keys):
        return math.nan
    return float(np.prod([1 + s[k] for k in keys]) - 1)


# --- the T-bill, by calendar day and by month ---


def bill_daily() -> dict[date, float]:
    days, ylds = ci.bill_yield()
    out: dict[date, float] = {}
    d, i = days[0], 0
    while d <= date(2025, 10, 31):
        while i + 1 < len(days) and days[i + 1] <= d:
            i += 1
        out[d] = ylds[i] / 365
        d = date.fromordinal(d.toordinal() + 1)
    return out


def bill_monthly(daily: dict[date, float]) -> Series:
    acc: dict[Month, float] = defaultdict(lambda: 1.0)
    for d, r in daily.items():
        acc[(d.year, d.month)] *= 1 + r
    return {k: v - 1 for k, v in acc.items()}


# --- our configurations ---


def monthly_excess(days: list[date], r: np.ndarray, rf: np.ndarray) -> Series:
    acc: dict[Month, list[float]] = defaultdict(lambda: [1.0, 1.0])
    for d, x, f in zip(days, r, rf, strict=True):
        a = acc[(d.year, d.month)]
        a[0] *= 1 + x
        a[1] *= 1 + f
    return {k: a[0] - a[1] for k, a in acc.items() if k <= LAST_MONTH}


def ours() -> tuple[dict[str, harness.Run], dict[str, Series]]:
    six = c.ctx("six")
    configs = {
        "tsmom12": c.weekly(c.slots(c.tsmom_signal)),
        "tsmom12-c00": c.weekly(risk_map.menu("tsmom12", 0.0)),
        "where-vol": tw.Where("vol").strategy(),
        "sixty-forty": c.weekly(c.sixty_forty),
        "hold-c17": c.weekly(c.equal_weight),
    }
    days, ylds = ci.bill_yield()
    runs, series = {}, {}
    for name, f in configs.items():
        run = c.go(IDEA, name, f, six, "baseline", log=False)  # re-score of a logged config
        r, rf = ci.rescored(run, days, ylds)
        runs[name] = run
        series[name] = monthly_excess(run.days[1:], r, rf)
        print(f"{name}: Sharpe (repo convention, train) {stats.sharpe(run.rets):.2f}", flush=True)
    return runs, series


# --- live funds and the AQR factor ---


def fund_monthly(root: Path, t: str, rf: Series) -> Series:
    last: dict[Month, float] = {}
    with (root / "derived" / "survey-5" / f"{t}.csv").open() as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if (d.year, d.month) <= LAST_MONTH:
                last[(d.year, d.month)] = float(row["adjclose"])
    ks = sorted(last)
    out = {}
    for a, b in zip(ks, ks[1:], strict=False):
        if months(a, b)[1:2] == [b]:  # consecutive months only
            out[b] = last[b] / last[a] - 1 - rf[b]
    return out


def spy_monthly(rf: Series) -> Series:
    last: dict[Month, float] = {}
    for b in c.load_history("train", True, ["SPY"])["SPY"]:
        last[(b.date.year, b.date.month)] = b.close
    ks = sorted(k for k in last if k <= LAST_MONTH)
    return {b: last[b] / last[a] - 1 - rf[b] for a, b in zip(ks, ks[1:], strict=False)}


def aqr_factor(root: Path) -> Series:
    import openpyxl  # only this script needs it: uv run --with openpyxl

    wb = openpyxl.load_workbook(
        root / "downloads" / "survey-5" / "aqr" / "tsmom.xlsx", read_only=True
    )
    ws = wb["TSMOM Factors"]
    out: Series = {}
    header = None
    for row in ws.iter_rows(values_only=True):
        if header is None:
            if row and row[1] == "TSMOM":
                header = row
            continue
        d, v = row[0], row[1]
        ok = isinstance(d, datetime) and isinstance(v, (int, float))
        if ok and (d.year, d.month) <= LAST_MONTH:
            out[(d.year, d.month)] = float(v)
    return out


def composite(members: dict[str, Series]) -> Series:
    acc: dict[Month, list[float]] = defaultdict(list)
    for s in members.values():
        for k, v in s.items():
            acc[k].append(v)
    return {k: float(np.mean(v)) for k, v in acc.items()}


# --- step 3: forward-1's sample size ---


def periods_needed(sharpe: float, per_year: float, alpha: float, skew: float, kurt: float) -> int:
    """forward-1 (`grimstrade.forward.min_periods_sharpe`), same formula, power 0.8."""
    if sharpe <= 0:
        return 10**9
    sr = sharpe / math.sqrt(per_year)
    k = 1 - skew * sr + (kurt - 1) / 4 * sr**2
    z = NormalDist().inv_cdf(1 - alpha) + NormalDist().inv_cdf(0.8)
    return math.ceil(1 + k * (z / sr) ** 2)


def weekly_rets(run: harness.Run) -> np.ndarray:
    return weekly_from(run.rets)


def weekly_from(r: np.ndarray) -> np.ndarray:
    n = len(r) // 7
    return np.array([np.prod(1 + r[7 * i : 7 * i + 7]) - 1 for i in range(n)])


def moments(x: np.ndarray) -> tuple[float, float, float]:
    m, s = x.mean(), x.std()
    z = (x - m) / s
    return float(m / x.std(ddof=1) * math.sqrt(52)), float((z**3).mean()), float((z**4).mean())


def weeks_for_gap(s1: float, s2: float, rho: float, gap: float, alpha: float) -> float:
    """Weeks for a one-sided test of Sharpe(a) > Sharpe(b) to find an annual gap `gap` with
    power 0.8: Jobson-Korkie with Memmel's (2003) correction, normal returns; s1, s2 annual."""
    a, b, d = s1 / math.sqrt(52), s2 / math.sqrt(52), gap / math.sqrt(52)
    v = 2 * (1 - rho) + 0.5 * (a * a + b * b - 2 * a * b * rho * rho)
    z = NormalDist().inv_cdf(1 - alpha) + NormalDist().inv_cdf(0.8)
    return v * (z / d) ** 2 if d > 0 else math.inf


def sharpe_gap_power(runs: dict[str, harness.Run], h: float) -> list[str]:
    """Added after the first run (not on the card): the card's lead measure (mean weekly
    difference) is below 0, because `tsmom12` earns less than holding at lower risk. Its case is
    a higher Sharpe, so this asks how long a forward test of the Sharpe gap takes."""
    out = [
        "",
        "### Added after the first run: the Sharpe gap to holding everything",
        "",
        "Not on the card. The card's lead measure (mean weekly `tsmom12` minus `hold-c17`) is "
        "below 0: `tsmom12` earns a little less than holding, at lower risk. Its case is the "
        "higher Sharpe, so: weeks for a one-sided test of Sharpe(`tsmom12`) > Sharpe(`hold-c17`) "
        "(Jobson-Korkie with Memmel's correction; normal returns, so if anything too few), "
        "power 0.8, in years.",
        "",
        "| Window or haircut | Sharpe `tsmom12` | Sharpe `hold-c17` | Weekly correlation | Gap | "
        "Years, a 0.025 | a 0.10 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    t, hd = runs["tsmom12"], runs["hold-c17"]
    rows = []
    for label, a, b in (("backtest 1994-2025", t.days[0], t.days[-1]),
                        ("live window L (2010-02..2025-10)", date(2010, 2, 1),
                         date(2025, 10, 31))):  # fmt: skip
        x = weekly_from(t.rets_between(a, b))
        y = weekly_from(hd.rets_between(a, b))
        s1, s2 = moments(x)[0], moments(y)[0]
        rho = float(np.corrcoef(x, y)[0, 1])
        rows.append((label, s1, s2, rho, s1 - s2))
    lab, s1, s2, rho, g = rows[0]
    for name, hh in (("backtest gap x (1 - h), measured h", h), ("same, h = 25% (H2)", 0.25)):
        rows.append((f"{name} {hh:.0%}", s1, s1 - g * (1 - hh), rho, g * (1 - hh)))
    for label, s1, s2, rho, g in rows:
        yrs = [weeks_for_gap(s1, s2, rho, g, a) / 52 for a in (0.025, 0.10)]
        cells = [f"{x:.0f}" if math.isfinite(x) else "never (gap <= 0)" for x in yrs]
        out.append(f"| {label} | {s1:.2f} | {s2:.2f} | {rho:.2f} | {g:+.2f} | {cells[0]} | "
                   f"{cells[1]} |")  # fmt: skip
    return out


# --- output ---


def f2(x: float) -> str:
    return "-" if math.isnan(x) else f"{x:.2f}"


def pct(x: float) -> str:
    return "-" if math.isnan(x) else f"{x:+.1%}"


def span(s: Series) -> str:
    ks = sorted(s)
    return f"{ks[0][0]}-{ks[0][1]:02d} .. {ks[-1][0]}-{ks[-1][1]:02d}" if ks else "-"


def log_rows(runs: dict[str, harness.Run]) -> None:
    if f"| {IDEA} | tsmom12@live-L | live-check |" in harness.TRIES.read_text():
        return  # logged by the first run; a rerun only rewrites the tables
    a, b = date(2010, 2, 1), date(2025, 10, 31)
    lines = []
    for name in ("tsmom12", "tsmom12-c00", "where-vol", "sixty-forty"):
        r = runs[name].rets_between(a, b)
        eq = np.cumprod(1 + r)
        mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
        lines.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {name}@live-L | live-check | train | "
            f"{a} | {b} | {stats.sharpe(r):.2f} | {eq[-1] - 1:+.1%} | {mdd:.1%} | "
            f"{runs[name].score.turnover:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(lines)


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    rf = bill_monthly(bill_daily())
    runs, our = ours()
    funds = {t: fund_monthly(root, t, rf) for t in TREND + RISKPAR + ALONE}
    aqr = aqr_factor(root)
    spy = spy_monthly(rf)
    tc = composite({t: funds[t] for t in TREND})
    rc = composite({t: funds[t] for t in RISKPAR})
    four = ["tsmom12", "tsmom12-c00", "where-vol", "sixty-forty"]
    allser: dict[str, Series] = {
        **{n: our[n] for n in four}, "TC (trend funds)": tc, "RC (risk-parity funds)": rc,
        "AQR TSMOM factor (paper)": aqr, **funds, "SPY": spy, "hold-c17": our["hold-c17"],
    }  # fmt: skip

    out = [
        "# live-check: our backtests against live funds of their family",
        "",
        "Card: `cards/live-check.md` (committed before any number). Descriptive, nothing selected, "
        "held-out year unread (no month after 2025-10). All figures are monthly returns **above "
        "the 13-week T-bill**; our rules earn the bill on cash (`cash_interest.rescored`). Sharpe "
        "= monthly mean / sd x sqrt 12. Live funds: net asset value with distributions "
        "(after fees and real costs). TC = equal weight of the trend funds alive each month ("
        + ", ".join(TREND)
        + "); RC = the same for "
        + ", ".join(RISKPAR)
        + ".",
        "",
        "## 1. Sharpe by window",
        "",
        "L = 2010-02..2025-10 (the live window), L07 = 2007-04..2025-10 (RYMFX's), P = "
        "1985-01..2009-12 for the AQR factor (the paper's sample) and 1994-02..2009-12 for ours.",
        "",
        "| Series | Months in L | Sharpe L | Sharpe L07 | Sharpe P | Own life | Sharpe own life |",
        "|---|---:|---:|---:|---:|---|---:|",
    ]
    for name, s in allser.items():
        sl, s07 = cut(s, L), cut(s, L07)
        p = cut(s, P_AQR if name.startswith("AQR") else P_OURS)
        full07 = len(s07) == len(months(*L07))
        out.append(
            f"| {name} | {len(sl)} | {f2(sharpe_m(sl))} | {f2(sharpe_m(s07)) if full07 else '-'} | "
            f"{f2(sharpe_m(p)) if len(p) > 24 else '-'} | {span(s)} | "
            f"{f2(sharpe_m(s))} |"
        )

    out += [
        "",
        "## 2. Correlation of monthly excess returns (months in common within L)",
        "",
        "Rows: ours. Funds need 36 months in common; n in brackets.",
        "",
    ]
    cols = ["TC (trend funds)", "RC (risk-parity funds)", "AQR TSMOM factor (paper)", "SPY"]
    cols += TREND + RISKPAR + ALONE
    out.append("| Ours | " + " | ".join(cols) + " |")
    out.append("|---|" + "---:|" * len(cols))
    for n in four:
        cells = []
        for col in cols:
            r, k = corr(cut(our[n], L), cut(allser[col], L))
            cells.append(f"{f2(r)} ({k})")
        out.append(f"| {n} | " + " | ".join(cells) + " |")
    r_tc_aqr, k_tc_aqr = corr(cut(tc, L), cut(aqr, L))
    r_aqmix_aqr, k2 = corr(cut(funds["AQMIX"], L), cut(aqr, L))
    r_rc_6040, _ = corr(cut(rc, L), cut(our["sixty-forty"], L))
    out += [
        "",
        f"Live against paper: TC with the AQR factor {f2(r_tc_aqr)} ({k_tc_aqr} months); AQMIX "
        f"with the AQR factor {f2(r_aqmix_aqr)} ({k2}). TC with SPY "
        f"{f2(corr(cut(tc, L), cut(spy, L))[0])}; "
        f"RC with SPY {f2(corr(cut(rc, L), cut(spy, L))[0])}.",
        "",
        "## 3. Crash years (calendar-year excess return; 2020-02..03 two-month return)",
        "",
        "| Series | 2008 | 2020 | 2020-02..03 | 2022 |",
        "|---|---:|---:|---:|---:|",
    ]
    for name, s in allser.items():
        yrs = [compound(s, [(y, m) for m in range(1, 13)]) for y in CRASH_YEARS]
        cov = compound(s, [(2020, 2), (2020, 3)])
        out.append(f"| {name} | {pct(yrs[0])} | {pct(yrs[1])} | {pct(cov)} | {pct(yrs[2])} |")

    # 4. haircut
    sr_aqr_p, sr_aqr_l = sharpe_m(cut(aqr, P_AQR)), sharpe_m(cut(aqr, L))
    sr_aqmix, sr_tc = sharpe_m(cut(funds["AQMIX"], L)), sharpe_m(cut(tc, L))
    h = 1 - sr_aqmix / sr_aqr_p if sr_aqr_p > 0 else math.nan
    out += [
        "",
        "## 4. Haircut, trend family",
        "",
        "| Step | From | To | Sharpe from | Sharpe to | Kept |",
        "|---|---|---|---:|---:|---:|",
        f"| (a) post-sample decay of the published portfolio | AQR factor, P | AQR factor, L | "
        f"{f2(sr_aqr_p)} | {f2(sr_aqr_l)} | {sr_aqr_l / sr_aqr_p:.0%} |",
        f"| (b) implementation and fees | AQR factor, L | AQMIX, L | {f2(sr_aqr_l)} | "
        f"{f2(sr_aqmix)} | {sr_aqmix / sr_aqr_l if sr_aqr_l else math.nan:.0%} |",
        f"| (b') same, the fund panel | AQR factor, L | TC, L | {f2(sr_aqr_l)} | {f2(sr_tc)} | "
        f"{sr_tc / sr_aqr_l if sr_aqr_l else math.nan:.0%} |",
        f"| **(c) total: h = 1 - kept** | AQR factor, P | AQMIX, L | {f2(sr_aqr_p)} | "
        f"{f2(sr_aqmix)} | {1 - h:.0%} (h = {h:.0%}) |",
    ]
    for n in ("tsmom12", "tsmom12-c00"):
        a, b = sharpe_m(cut(our[n], P_OURS)), sharpe_m(cut(our[n], L))
        out.append(f"| (d) our split | `{n}`, 1994-2009 | `{n}`, L | {f2(a)} | {f2(b)} | "
                   f"{b / a if a else math.nan:.0%} |")  # fmt: skip

    # 5. Sharpe gaps in L
    out += ["", "## 5. Sharpe gap in L (ours minus its live family)", ""]
    for n, fam, fname in (("tsmom12", tc, "TC"), ("tsmom12-c00", tc, "TC"),
                          ("where-vol", rc, "RC"), ("sixty-forty", rc, "RC")):  # fmt: skip
        ks = sorted(set(cut(our[n], L)) & set(cut(fam, L)))
        a = sharpe_m({k: our[n][k] for k in ks})
        b = sharpe_m({k: fam[k] for k in ks})
        out.append(f"- `{n}` {f2(a)} vs {fname} {f2(b)} on the same {len(ks)} months: "
                   f"{a - b:+.2f}.")  # fmt: skip

    # step 3 inputs
    wk = weekly_rets(runs["tsmom12"])
    sr_w, sk, ku = moments(wk)
    diff = weekly_rets(runs["tsmom12"]) - weekly_rets(runs["hold-c17"])
    sr_d, sk_d, ku_d = moments(diff)
    base = stats.sharpe(runs["tsmom12"].rets)
    out += [
        "",
        "## 6. For step 3: expected live Sharpe of `tsmom12` and forward length",
        "",
        f"`tsmom12` backtest 1994-2025: Sharpe {base:.2f} (repo convention: daily, 365, zero "
        f"rate). Weekly returns: Sharpe {sr_w:.2f}, skew {sk:+.2f}, kurtosis {ku:.1f}. Weekly "
        f"`tsmom12` minus `hold-c17`: Sharpe {sr_d:.2f}, skew {sk_d:+.2f}, kurtosis {ku_d:.1f}.",
        "",
        "Weeks needed (forward-1's `sharpe` formula, power 0.8, one-sided), in years of 52 weeks:",
        "",
        "| Haircut h | Expected live Sharpe | Years, Sharpe > 0, a 0.025 | a 0.10 | Expected lead "
        "over holding (Sharpe of difference) | Years, lead > 0, a 0.025 | a 0.10 |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    hs = {"none (the backtest)": 0.0, f"measured (c), {h:.0%}": h}
    hs.update({f"{k}, {v:.0%}": v for k, v in H_LIT.items()})
    for label, hh in hs.items():
        if math.isnan(hh):
            continue
        e, ed = base * (1 - hh), sr_d * (1 - hh)
        y = [periods_needed(e, 52, a, sk, ku) / 52 for a in (0.025, 0.10)]
        yd = [periods_needed(ed, 52, a, sk_d, ku_d) / 52 for a in (0.025, 0.10)]
        ydt = [f"{x:.0f}" if ed > 0 else "never (mean below 0)" for x in yd]
        out.append(f"| {label} | {e:.2f} | {y[0]:.1f} | {y[1]:.1f} | {ed:.2f} | {ydt[0]} | "
                   f"{ydt[1]} |")  # fmt: skip
    out += sharpe_gap_power(runs, h)
    text = "\n".join(out) + "\n"
    path = harness.RESEARCH / "results" / "live-check.md"
    path.write_text(text)
    print(text)
    if not c.DRY:
        log_rows(runs)


if __name__ == "__main__":
    main()
