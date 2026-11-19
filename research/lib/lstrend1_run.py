"""ls-trend-1: long-short, volatility-scaled TSMOM on a wider ETF set against live trend funds
(card: research/cards/ls-trend.md). Descriptive replication, nothing selected.

    uv run --with openpyxl python -I research/lib/lstrend1_run.py <cache_root>

Reads the ETF series written by `lstrend1_fetch.py`, the live fund series and the AQR workbook
written by `survey5_fetch.py` (data only), re-scores `tsmom12` and `tsmom12-c00` as survey-5 did
(`log=False`), appends one `replication` row per cell to `tries.md` (first run only) and writes
`research/results/ls-trend.md`. No day after 2025-10-31 of any series is read.
"""

from __future__ import annotations

import csv
import math
import os
import sys
from collections import defaultdict
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness  # noqa: E402
import numpy as np  # noqa: E402
import stats  # noqa: E402
import survey5_live as s5  # noqa: E402
from survey5_live import Month, Series, compound, corr, cut, months, sharpe_m  # noqa: E402

IDEA = "ls-trend-1"
LAST_DAY = date(2025, 10, 31)
L, L07 = s5.L, s5.L07
CLASSES: dict[str, list[str]] = {
    "equity": ["SPY", "EWA", "EWG", "EWP", "EWQ", "EWI", "EWJ", "EWN", "EWU"],
    "bonds": ["SHY", "IEI", "IEF", "TLT"],
    "commodities": ["GLD", "SLV", "PPLT", "PALL", "CPER", "DBB", "USO", "BNO", "UGA", "UNG",
                    "CORN", "WEAT", "SOYB", "CANE", "DBA"],
    "currencies": ["FXE", "FXY", "FXB", "FXA", "FXC", "FXF"],
}  # fmt: skip
CLASS_OF = {t: k for k, ts in CLASSES.items() for t in ts} | {"QQQ": "equity"}
WIDE = [t for ts in CLASSES.values() for t in ts]
NARROW = ["SPY", "QQQ", "GLD", "TLT"]
TARGET_VOL = 0.40
DELTA = 60 / 61  # centre of mass 60 days
COST = 0.0005  # per side, on traded notional
BORROW = 0.01  # a year, on short notional
CRASH: dict[str, tuple[Month, Month]] = {
    "2008": ((2008, 1), (2008, 12)),
    "2020-02..03": ((2020, 2), (2020, 3)),
    "2022": ((2022, 1), (2022, 12)),
}


def month_end_day(m: Month) -> date:
    return date(m[0] + m[1] // 12, m[1] % 12 + 1, 1) - timedelta(days=1)


CRASH_DAYS = {k: (date(a[0], a[1], 1), month_end_day(b)) for k, (a, b) in CRASH.items()}


def load_prices(root: Path, t: str) -> dict[date, float]:
    out = {}
    with (root / "derived" / "ls-trend-1" / f"{t}.csv").open() as f:
        for row in csv.DictReader(f):
            d = date.fromisoformat(row["date"])
            if d <= LAST_DAY:
                out[d] = float(row["adjclose"])
    return out


class Book:
    """Daily excess returns of one cell, with its per-asset daily contributions."""

    def __init__(self, name: str, assets: list[str], long_short: bool) -> None:
        self.name, self.assets, self.long_short = name, assets, long_short
        self.days: list[date] = []
        self.ret: list[float] = []  # daily excess return
        self.contrib: dict[str, list[float]] = defaultdict(list)  # per asset, aligned to days
        self.sign: dict[str, list[float]] = defaultdict(list)  # sign of the weight that day
        self.cost_today = 0.0
        self.gross: list[float] = []
        self.net: list[float] = []
        self.traded = 0.0
        self.cost_paid = 0.0
        self.borrow_paid = 0.0


def run_books(
    prices: dict[str, dict[date, float]], rf_day: dict[date, float], books: list[Book]
) -> None:
    cal = sorted(set().union(*(p.keys() for p in prices.values())))
    first = {t: min(p) for t, p in prices.items()}
    # daily simple returns per asset (vs the asset's previous bar)
    rets: dict[str, dict[date, float]] = {}
    for t, p in prices.items():
        ds = sorted(p)
        rets[t] = {b: p[b] / p[a] - 1 for a, b in zip(ds, ds[1:], strict=False)}
    # trading-day bill return: compounding over the calendar days since the previous bar
    rf_t: dict[date, float] = {}
    for a, b in zip(cal, cal[1:], strict=False):
        g, d = 1.0, a + timedelta(days=1)
        while d <= b:
            g *= 1 + rf_day.get(d, 0.0)
            d += timedelta(days=1)
        rf_t[b] = g - 1
    month_end = {
        a for a, b in zip(cal, cal[1:], strict=False) if (a.year, a.month) != (b.year, b.month)
    }
    # EWMA mean and second moment of daily returns, updated after each close (ex ante for next)
    m1: dict[str, float] = {}
    m2: dict[str, float] = {}
    nret: dict[str, int] = defaultdict(int)
    bill_index = {cal[0]: 1.0}
    for a, b in zip(cal, cal[1:], strict=False):
        bill_index[b] = bill_index[a] * (1 + rf_t[b])
    weights = {bk.name: dict.fromkeys(bk.assets, 0.0) for bk in books}
    pending: dict[str, tuple[int, dict[str, float]]] = {}
    for i, d in enumerate(cal):
        # 1. apply a decision that becomes effective today (decided two bars ago at month end:
        #    held from the close of the next trading day after the decision)
        for bk in books:
            if bk.name in pending and pending[bk.name][0] == i:
                new = pending.pop(bk.name)[1]
                old = weights[bk.name]
                turn = sum(abs(new.get(t, 0.0) - old.get(t, 0.0)) for t in bk.assets)
                bk.traded += turn
                weights[bk.name] = new
                bk.cost_paid += turn * COST
                bk.cost_today = turn * COST
        # 2. P&L of today's return with the weights in force
        if i > 0:
            days = (d - cal[i - 1]).days
            for bk in books:
                w = weights[bk.name]
                tot = 0.0
                for t in bk.assets:
                    x = rets[t].get(d)
                    e = (x - rf_t[d]) if x is not None else 0.0
                    c = w.get(t, 0.0) * e
                    if w.get(t, 0.0) < 0:
                        c -= -w[t] * BORROW * days / 365
                        bk.borrow_paid += -w[t] * BORROW * days / 365
                    bk.contrib[t].append(c)
                    bk.sign[t].append(float(np.sign(w.get(t, 0.0))))
                    tot += c
                tot -= bk.cost_today
                bk.cost_today = 0.0
                bk.days.append(d)
                bk.ret.append(tot)
                bk.gross.append(sum(abs(v) for v in w.values()))
                bk.net.append(sum(w.values()))
        # 3. update the volatility estimates with today's close
        for t in prices:
            x = rets[t].get(d)
            if x is None:
                continue
            if t not in m1:
                m1[t], m2[t] = x, x * x
            else:
                m1[t] = DELTA * m1[t] + (1 - DELTA) * x
                m2[t] = DELTA * m2[t] + (1 - DELTA) * x * x
            nret[t] += 1
        # 4. month end: decide, effective from the close of the next trading day
        if d in month_end and i + 2 < len(cal):
            for bk in books:
                alive = []
                for t in bk.assets:
                    back = d - timedelta(days=365)
                    if first[t] > back or nret[t] < 60:
                        continue
                    p = prices[t]
                    past = max(x for x in p if x <= back)
                    pb = max(x for x in bill_index if x <= back)
                    ex = (p[d] / p[past]) / (bill_index[d] / bill_index[pb]) - 1
                    sigma = math.sqrt(max(m2[t] - m1[t] ** 2, 1e-12) * 261)
                    alive.append((t, 1.0 if ex > 0 else -1.0, sigma))
                n = len(alive)
                new = {}
                for t, sgn, sigma in alive:
                    if sgn < 0 and not bk.long_short:
                        sgn = 0.0
                    new[t] = sgn * TARGET_VOL / sigma / n
                pending[bk.name] = (i + 2, new)


def monthly(days: list[date], x: list[float], rf_t: dict[date, float]) -> Series:
    acc: dict[Month, list[float]] = defaultdict(lambda: [1.0, 1.0])
    for d, r in zip(days, x, strict=True):
        a = acc[(d.year, d.month)]
        a[0] *= 1 + r + rf_t[d]
        a[1] *= 1 + rf_t[d]
    return {k: a[0] - a[1] for k, a in acc.items()}


def aqr_classes(root: Path) -> dict[str, Series]:
    import openpyxl

    wb = openpyxl.load_workbook(
        root / "downloads" / "survey-5" / "aqr" / "tsmom.xlsx", read_only=True
    )
    ws = wb["TSMOM Factors"]
    names = {1: "all", 2: "commodities", 3: "equity", 4: "bonds", 5: "currencies"}
    out: dict[str, Series] = {v: {} for v in names.values()}
    header = None
    for row in ws.iter_rows(values_only=True):
        if header is None:
            if row and row[1] == "TSMOM":
                header = row
            continue
        d = row[0]
        if not isinstance(d, datetime) or (d.year, d.month) > s5.LAST_MONTH:
            continue
        for j, n in names.items():
            if isinstance(row[j], (int, float)):
                out[n][(d.year, d.month)] = float(row[j])
    return out


def vol_m(s: Series) -> float:
    x = np.array(list(s.values()))
    return float(x.std(ddof=1) * math.sqrt(12)) if len(x) > 12 else math.nan


def f2(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:.2f}"


def pct(x: float) -> str:
    return "-" if not math.isfinite(x) else f"{x:+.1%}"


def crash_ret(s: Series, w: tuple[Month, Month]) -> float:
    return compound(s, months(*w))


def main() -> None:
    root = Path(sys.argv[1]).expanduser()
    rf_day = s5.bill_daily()
    rf_m = s5.bill_monthly(rf_day)
    prices = {t: load_prices(root, t) for t in [*WIDE, "QQQ"]}
    books = [
        Book("wide-LS", WIDE, True),
        Book("wide-LO", WIDE, False),
        Book("narrow-LS", NARROW, True),
        Book("narrow-LO", NARROW, False),
    ]
    run_books(prices, rf_day, books)
    cal = sorted(set().union(*(p.keys() for p in prices.values())))
    rf_t = {}
    for a, b in zip(cal, cal[1:], strict=False):
        g, d = 1.0, a + timedelta(days=1)
        while d <= b:
            g *= 1 + rf_day.get(d, 0.0)
            d += timedelta(days=1)
        rf_t[b] = g - 1
    ours = {bk.name: monthly(bk.days, bk.ret, rf_t) for bk in books}
    # drop months before each book first holds a position
    for bk in books:
        start = next(d for d, g in zip(bk.days, bk.gross, strict=True) if g > 0)
        first_full = (start.year + start.month // 12, start.month % 12 + 1)
        ours[bk.name] = {k: v for k, v in ours[bk.name].items() if k >= first_full}

    _, s5_ours = s5.ours()
    funds = {t: s5.fund_monthly(root, t, rf_m) for t in s5.TREND}
    tc = s5.composite(funds)
    aqr = aqr_classes(root)
    spy = s5.spy_monthly(rf_m)
    ref: dict[str, Series] = {
        "TC (trend funds)": tc, "AQR TSMOM factor": aqr["all"], "RYMFX": funds["RYMFX"],
        "AQMIX": funds["AQMIX"], "tsmom12": s5_ours["tsmom12"],
        "tsmom12-c00": s5_ours["tsmom12-c00"], "SPY": spy,
    }  # fmt: skip
    cells = [bk.name for bk in books]
    out = [
        "# ls-trend: long-short TSMOM on a wider ETF set against live trend funds",
        "",
        "Card: `cards/ls-trend.md` (committed before any number). Descriptive replication, "
        "nothing selected, nothing after 2025-10 read. Monthly returns **above the 13-week "
        "T-bill**. Rule of Moskowitz, Ooi, Pedersen 2012: sign of the 12-month excess return, "
        "40% / ex ante vol per asset, equal weight across the assets alive, monthly, one day "
        f"later than the paper; costs {COST * 1e4:.0f} bps a side, borrow {BORROW:.1%} a year "
        "on shorts, leverage financed at the bill. Wide = 34 ETFs (9 equity, 4 Treasury, 15 "
        "commodity, 6 currency); narrow = SPY, QQQ, GLD, TLT (`tsmom12-c00`'s assets). LS = "
        "long-short, LO = long-only (short signals to cash). L = 2010-02..2025-10, L07 = "
        "2007-04..2025-10.",
        "",
        "## 1. Sharpe, risk, leverage, costs",
        "",
        "| Series | First month | Sharpe L | Sharpe L07 | Vol L07 | Worst year (L07) | "
        "Mean gross | Mean net | Turnover/yr | Costs/yr | Borrow/yr |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for bk in books:
        s = ours[bk.name]
        k0 = min(s)
        yrs = (bk.days[-1] - bk.days[0]).days / 365.25
        live = [i for i, g in enumerate(bk.gross) if g > 0]
        years = {y: compound(s, months((y, 1), (y, 12))) for y in range(2007, 2025)}
        wy = min((v, y) for y, v in years.items() if math.isfinite(v) and y >= 2008)
        out.append(
            f"| {bk.name} | {k0[0]}-{k0[1]:02d} | {f2(sharpe_m(cut(s, L)))} | "
            f"{f2(sharpe_m(cut(s, L07)))} | {vol_m(cut(s, L07)):.1%} | {wy[0]:+.1%} ({wy[1]}) | "
            f"{np.mean([bk.gross[i] for i in live]):.2f} | "
            f"{np.mean([bk.net[i] for i in live]):+.2f} | "
            f"{bk.traded / yrs:.1f} | {bk.cost_paid / yrs:.2%} | {bk.borrow_paid / yrs:.2%} |"
        )
    for n, s in ref.items():
        out.append(f"| {n} | {min(s)[0]}-{min(s)[1]:02d} | {f2(sharpe_m(cut(s, L)))} | "
                   f"{f2(sharpe_m(cut(s, L07)))} | {vol_m(cut(s, L07)):.1%} | "
                   "- | - | - | - | - | - |")  # fmt: skip

    # 2. correlations in L
    cols = ["TC (trend funds)", "AQR TSMOM factor", "SPY", "tsmom12", "tsmom12-c00",
            *s5.TREND]  # fmt: skip
    colser = {**ref, **funds}
    out += ["", "## 2. Correlation of monthly excess returns in L (n in brackets; funds need 36)",
            "", "| Cell | " + " | ".join(cols) + " | RYMFX in L07 |",
            "|---|" + "---:|" * (len(cols) + 1)]  # fmt: skip
    for n in cells:
        row = []
        for cn in cols:
            r, k = corr(cut(ours[n], L), cut(colser[cn], L))
            row.append(f"{f2(r)} ({k})")
        r, k = corr(cut(ours[n], L07), cut(funds["RYMFX"], L07))
        out.append(f"| {n} | " + " | ".join(row) + f" | {f2(r)} ({k}) |")
    for a, b in (("wide-LS", "wide-LO"), ("narrow-LS", "narrow-LO"), ("wide-LS", "narrow-LS")):
        r, k = corr(cut(ours[a], L), cut(ours[b], L))
        out.append(f"\n{a} with {b} in L: {f2(r)} ({k} months).")

    # 3. crash windows
    out += ["", "## 3. Crash windows (compounded monthly excess return)", "",
            "Raw, and at 10% volatility (x 10% / the series' own monthly vol in L07, or over its "
            "own life to 2025-10 if shorter; a display scaling, ex post).", "",
            "| Series | Vol used | " + " | ".join(CRASH) + " | " +
            " | ".join(f"{k} at 10% vol" for k in CRASH) + " |",
            "|---|---:|" + "---:|" * (2 * len(CRASH))]  # fmt: skip
    allser = {**{n: ours[n] for n in cells}, **ref,
              **{f"AQR {k}": v for k, v in aqr.items() if k != "all"},
              **{t: funds[t] for t in ("ASFYX", "PQTIX", "ABYIX", "DBMF")}}  # fmt: skip
    for n, s in allser.items():
        v = vol_m(cut(s, L07)) if min(s) <= L07[0] else vol_m(cut(s, (min(s), s5.LAST_MONTH)))
        raw = [crash_ret(s, w) for w in CRASH.values()]
        sc = [x * 0.10 / v if math.isfinite(x) else math.nan for x in raw]
        out.append(f"| {n} | {v:.1%} | " + " | ".join(pct(x) for x in raw) + " | "
                   + " | ".join(pct(x) for x in sc) + " |")  # fmt: skip

    # 4. leg decomposition
    out += ["", "## 4. Where the crash gains came from (additive daily contributions, % of "
            "capital, raw scale; costs not included in the legs)", ""]  # fmt: skip
    for bk in books:
        if not bk.long_short:
            continue
        out += [f"### {bk.name}", "", "| Window | Class | Long legs | Short legs | Total | "
                "Share of window total |", "|---|---|---:|---:|---:|---:|"]  # fmt: skip
        idx = {d: i for i, d in enumerate(bk.days)}
        for wn, (a, b) in CRASH_DAYS.items():
            ii = [idx[d] for d in bk.days if a <= d <= b]
            per: dict[tuple[str, str], float] = defaultdict(float)
            for t in bk.assets:
                for i in ii:
                    sgn = bk.sign[t][i]
                    if sgn != 0:
                        per[(CLASS_OF[t], "long" if sgn > 0 else "short")] += bk.contrib[t][i]
            tot = sum(per.values())
            for k in [*CLASSES, "all"]:
                if k == "all":
                    lo = sum(v for (c, s), v in per.items() if s == "long")
                    sh = sum(v for (c, s), v in per.items() if s == "short")
                else:
                    lo, sh = per[(k, "long")], per[(k, "short")]
                share = (lo + sh) / tot if tot > 0 else math.nan
                out.append(f"| {wn} | {k} | {pct(lo)} | {pct(sh)} | {pct(lo + sh)} | "
                           f"{'-' if not math.isfinite(share) else f'{share:.0%}'} |")  # fmt: skip
            lo_all = sum(v for (c, s), v in per.items() if s == "long")
            sh_all = sum(v for (c, s), v in per.items() if s == "short")
            if tot > 0:
                out.append(f"| {wn} | **short legs' share of the gain** | | | | "
                           f"**{sh_all / tot:.0%}** (long {lo_all / tot:.0%}) |")  # fmt: skip
        out.append("")
    out += ["### AQR TSMOM factor by asset class (sum of monthly returns in the window)", "",
            "| Window | " + " | ".join(CLASSES) + " | all |", "|---|" + "---:|" * 5]  # fmt: skip
    for wn, w in CRASH.items():
        cl = [sum(aqr[k].get(m, math.nan) for m in months(*w)) for k in [*CLASSES, "all"]]
        out.append(f"| {wn} | " + " | ".join(pct(x) for x in cl) + " |")
    out.append("")
    out.append("(The factor's class columns are each scaled on their own, so they do not add "
               "to `all`; read the signs and the order.)")  # fmt: skip

    # 5. 2 x 2 effects
    def scaled(n: str, w: tuple[Month, Month]) -> float:
        s = ours[n]
        return crash_ret(s, w) * 0.10 / vol_m(cut(s, L07))

    out += ["", "## 5. The 2 x 2: short effect and universe effect", "",
            "Crash returns at 10% vol; correlation with TC in L.", "",
            "| Effect | " + " | ".join(CRASH) + " | Corr. with TC |",
            "|---|" + "---:|" * (len(CRASH) + 1)]  # fmt: skip
    ctc = {n: corr(cut(ours[n], L), cut(tc, L))[0] for n in cells}
    for label, a, b in (("short effect, wide (wide-LS - wide-LO)", "wide-LS", "wide-LO"),
                        ("short effect, narrow (narrow-LS - narrow-LO)", "narrow-LS", "narrow-LO"),
                        ("universe effect, LS (wide-LS - narrow-LS)", "wide-LS", "narrow-LS"),
                        ("universe effect, LO (wide-LO - narrow-LO)", "wide-LO",
                         "narrow-LO")):  # fmt: skip
        diffs = [pct(scaled(a, w) - scaled(b, w)) for w in CRASH.values()]
        out.append(f"| {label} | " + " | ".join(diffs) + f" | {ctc[a] - ctc[b]:+.2f} |")

    # card's reading rule
    out += ["", "## 6. Card's reading rule", ""]
    for n in cells:
        r08, r22 = crash_ret(ours[n], CRASH["2008"]), crash_ret(ours[n], CRASH["2022"])
        ok = r08 > 0 and r22 > 0 and ctc[n] >= 0.5
        out.append(f"- {n}: 2008 {pct(r08)}, 2022 {pct(r22)}, corr. with TC {f2(ctc[n])} -> "
                   f"{'reproduces' if ok else 'does not reproduce'} the funds' crash "
                   "behaviour.")  # fmt: skip

    text = "\n".join(out) + "\n"
    (harness.RESEARCH / "results" / "ls-trend.md").write_text(text)
    print(text)
    if not os.environ.get("NOLOG"):  # plumbing checks only; the first full run logs
        log_rows(books)


def log_rows(books: list[Book]) -> None:
    if f"| {IDEA} | wide-LS@live-L | replication |" in harness.TRIES.read_text():
        return  # logged by the first run; a rerun only rewrites the tables
    a, b = date(2010, 2, 1), LAST_DAY
    lines = []
    for bk in books:
        daily = {d: r for d, r in zip(bk.days, bk.ret, strict=True) if a <= d <= b}
        cal = [a + timedelta(days=i) for i in range((b - a).days + 1)]
        r = np.array([daily.get(d, 0.0) for d in cal])
        eq = np.cumprod(1 + r)
        mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
        yrs = (bk.days[-1] - bk.days[0]).days / 365.25
        lines.append(
            f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {bk.name}@live-L | replication | "
            f"train | {a} | {b} | {stats.sharpe(r):.2f} | {eq[-1] - 1:+.1%} | {mdd:.1%} | "
            f"{bk.traded / yrs:.2f} |\n"
        )
    with harness.TRIES.open("a") as f:
        f.writelines(lines)


if __name__ == "__main__":
    main()
