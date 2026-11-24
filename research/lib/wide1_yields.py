"""Step 4 of research run wide-1: a descriptive check of three post-hoc patterns on bond yields
from before TLT and IEF existed (definitions fixed in research/wide-1.md before looking).

    uv run python -I research/lib/wide1_yields.py

Not a strategy: nothing goes through the harness, nothing is logged in tries.md. Yields are read
from the FRED cache as data only; nothing after 2025-11-10 is used. Returns are close to close.
"""

from __future__ import annotations

import bisect
import csv
import math
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import macro  # noqa: E402
import wide1 as w  # noqa: E402
import wide1_rules as rules  # noqa: E402
from harness import TRAIN_LAST_BAR, load_history  # noqa: E402

SEEN = date(2003, 8, 1)  # our TLT and IEF tests start 2003-07-31
PERIODS = [
    ("1962-1979", date(1962, 1, 1), date(1979, 12, 31)),
    ("1980-1989", date(1980, 1, 1), date(1989, 12, 31)),
    ("1990-2003/07", date(1990, 1, 1), date(2003, 7, 31)),
    ("unseen, pooled", date(1962, 1, 1), date(2003, 7, 31)),
    ("seen 2003/08-2025", SEEN, date(2025, 12, 31)),
]
THRESHOLD = 0.02


def duration(y: float, n: int) -> float:
    """Modified duration of a par bond of maturity `n` years at yield `y` (semi-annual)."""
    return (1 - (1 + y / 2) ** (-2 * n)) / y if y > 0 else float(n)


def bond(series: str, n: int) -> tuple[list[date], np.ndarray]:
    """(dates, return of the session ending on each date) of a par bond of maturity `n`, from the
    yield series: -duration x change in yield + carry for the days elapsed. NaN across gaps."""
    recs = [r for r in macro.market_records(series) if r.obs <= TRAIN_LAST_BAR]
    days = [r.obs for r in recs]
    y = np.array([r.value / 100 for r in recs])
    ret = np.full(len(days), np.nan)
    for i in range(1, len(days)):
        gap = (days[i] - days[i - 1]).days
        if gap <= 10:
            ret[i] = -duration(y[i - 1], n) * (y[i] - y[i - 1]) + y[i - 1] * gap / 365
    return days, ret


def cell(x: np.ndarray) -> str:
    return f"{x.mean() * 1e4:+.1f} ({w.tstat(x):+.1f}; {len(x)})" if len(x) > 2 else f"- ({len(x)})"


def auction_days(lo: float, hi: float) -> list[date]:
    path = macro.cache_root() / "derived" / "wide-1" / "auctions.csv"
    with path.open(newline="") as f:
        days = {date.fromisoformat(r["auction"]) for r in csv.DictReader(f)
                if lo <= rules.term_years(r["term"]) < hi}  # fmt: skip
    return sorted(d for d in days if d <= c.TRAIN_END)


def q1() -> list[str]:
    out = ["## Q1. The dip before auctions", ""]
    out += [
        "Return of the matching par bond around each nominal auction, bps (t; events). Expected "
        "if real: negative in sessions A-4 .. A, positive in A+1 .. A+5.",
        "",
        "| Auction | Period | Sessions A-4 .. A | Sessions A+1 .. A+5 | Sessions A-9 .. A-5 |",
        "|---|---|---:|---:|---:|",
    ]
    for label, series, n, lo, hi in (("30-year bond", "DGS30", 30, 25, 99),
                                     ("10-year note", "DGS10", 10, 9, 11)):  # fmt: skip
        days, ret = bond(series, n)
        rows = []
        for a in auction_days(lo, hi):
            j = bisect.bisect_left(days, a)
            if j - 9 < 1 or j + 5 >= len(days) or (days[j] - a).days > 3:
                continue
            win = ret[j - 9 : j + 6]
            if not np.isnan(win).any():
                rows.append((a, win[5:10].sum(), win[10:15].sum(), win[0:5].sum()))
        for name, p0, p1 in PERIODS[1:]:
            sel = [r for r in rows if p0 <= r[0] <= p1]
            cols = [cell(np.array([r[k] for r in sel])) for k in (1, 2, 3)]
            out.append(f"| {label} | {name} | {cols[0]} | {cols[1]} | {cols[2]} |")
    return [*out, ""]


def q2() -> list[str]:
    out = ["## Q2. The month-end bond rally", ""]
    out += [
        "Return of the par bond over the last four sessions of the month and the first three of "
        "the next, minus as many average days of the same period, bps (t; months). Expected if "
        "real: positive in the last four.",
        "",
        "| Bond | Period | Last four sessions, excess | First three of next month, excess | "
        "Average day |",
        "|---|---|---:|---:|---:|",
    ]
    for label, series, n in (("10-year", "DGS10", 10), ("30-year", "DGS30", 30)):
        days, ret = bond(series, n)
        for name, p0, p1 in PERIODS:
            inside = np.array([p0 <= d <= p1 for d in days]) & ~np.isnan(ret)
            if inside.sum() < 250:
                continue
            mean_day = float(ret[inside].mean())
            last4, next3 = [], []
            for t in range(4, len(days) - 4):
                if days[t + 1].month == days[t].month or not p0 <= days[t] <= p1:
                    continue
                a, b = ret[t - 3 : t + 1], ret[t + 1 : t + 4]
                if not (np.isnan(a).any() or np.isnan(b).any()):
                    last4.append(a.sum() - 4 * mean_day)
                    next3.append(b.sum() - 3 * mean_day)
            out.append(
                f"| {label} | {name} | {cell(np.array(last4))} | {cell(np.array(next3))} | "
                f"{mean_day * 1e4:+.1f} |"
            )
    return [*out, ""]


def q3() -> list[str]:
    out = ["## Q3. The month-end loser bounce", ""]
    out += [
        "Months with |g| >= 2% at the close of T-5 (g = stocks minus the 10-year bond, month to "
        "date). Returns over sessions T-4 .. T, bps (t; months), signed so that positive is the "
        "expected direction: the month's leader falls, the month's loser rises.",
        "",
        "| Period | Leader | Leader's side, sign flipped | Loser's side | Spread, signed |",
        "|---|---|---:|---:|---:|",
    ]
    hist = load_history("train", True, ["GSPC", "SPY"])
    stock: dict[date, float] = {}
    level = 1.0
    spy0 = hist["SPY"][0].date
    for sym, bars in (("GSPC", [b for b in hist["GSPC"] if b.date < spy0]), ("SPY", hist["SPY"])):
        prev = None
        for b in bars:
            if prev is not None:
                level *= b.close / prev
            prev = b.close
            stock[b.date] = level
        del sym
    bdays, bret = bond("DGS10", 10)
    blevel: dict[date, float] = {}
    lv = 1.0
    for d, r in zip(bdays, bret, strict=True):
        if not math.isnan(r):
            lv *= 1 + r
        blevel[d] = lv
    cal = sorted(d for d in stock if d in blevel and d >= date(1962, 1, 2))
    ev = []
    for t in range(6, len(cal) - 1):
        if cal[t + 1].month == cal[t].month:
            continue
        refs = rules.month_refs(cal, t)
        if refs is None:
            continue
        m, p = refs
        g = math.log(stock[cal[m]] / stock[cal[p]]) - math.log(blevel[cal[m]] / blevel[cal[p]])
        s = stock[cal[t]] / stock[cal[m]] - 1
        b = blevel[cal[t]] / blevel[cal[m]] - 1
        if abs(g) >= THRESHOLD:
            ev.append((cal[t], g, s, b))
    for name, p0, p1 in PERIODS:
        for who, sel in (
            ("stocks", [e for e in ev if p0 <= e[0] <= p1 and e[1] > 0]),
            ("bonds", [e for e in ev if p0 <= e[0] <= p1 and e[1] < 0]),
            ("either", [e for e in ev if p0 <= e[0] <= p1]),
        ):
            lead = np.array([-(e[2] if e[1] > 0 else e[3]) for e in sel])
            lose = np.array([(e[3] if e[1] > 0 else e[2]) for e in sel])
            out.append(f"| {name} | {who} | {cell(lead)} | {cell(lose)} | {cell(lead + lose)} |")
    return [*out, ""]


def cross_check() -> list[str]:
    """Added after the first output: Q1's seen-period number from yields (-54 bps) is far from
    the ETF table's (-15 bps, open to open). The same windows on the ETFs' own closes tell
    whether that is the yield series (a new bond replaces the old one in it at an auction) or
    the fills."""
    out = ["## Cross-check on ETF closes, 2003-08 to 2025 (added after the first output)", ""]
    out += [
        "The same close-to-close windows as Q1 and Q2, on the ETFs' own total-return closes "
        "instead of the yield series. bps (t; events).",
        "",
        "| ETF | Window | Close to close | Excess over average days | Open to open (gym fills) |",
        "|---|---|---:|---:|---:|",
    ]
    halves = [
        "| ETF | Window | 2003-2013, close to close | 2014-2025, close to close |",
        "|---|---|---:|---:|",
    ]
    hist = load_history("train", True, ["TLT", "IEF"])
    for sym, lo, hi, label in (("TLT", 25, 99, "30-year"), ("IEF", 9, 11, "10-year")):
        bars = [b for b in hist[sym] if b.date >= date(2003, 7, 31)]
        days = [b.date for b in bars]
        ret = np.array(
            [math.nan] + [bars[i].close / bars[i - 1].close - 1 for i in range(1, len(bars))]
        )
        mean_day = float(np.nanmean(ret))
        opens = [b.open for b in bars]

        def o2o(a: int, b: int, opens: list[float] = opens) -> float:
            """Sessions a .. b held: bought at the open of a, sold at the open of b + 1."""
            return opens[b + 1] / opens[a] - 1

        rows: dict[str, list[tuple[date, float, float]]] = {k: [] for k in "abcd"}
        for a in auction_days(lo, hi):
            j = bisect.bisect_left(days, a)
            if j - 5 >= 1 and j + 6 < len(days) and days[j] == a:
                rows["a"].append((a, ret[j - 4 : j + 1].sum(), o2o(j - 4, j)))
                rows["b"].append((a, ret[j + 1 : j + 6].sum(), o2o(j + 1, j + 5)))
        for t in range(5, len(days) - 5):
            if days[t + 1].month != days[t].month:
                rows["c"].append((days[t], ret[t - 3 : t + 1].sum(), o2o(t - 3, t)))
                rows["d"].append((days[t], ret[t + 1 : t + 4].sum(), o2o(t + 1, t + 3)))
        for key, name, n in (
            ("a", f"{label} auctions, sessions A-4 .. A", 5),
            ("b", f"{label} auctions, sessions A+1 .. A+5", 5),
            ("c", "last four sessions of the month", 4),
            ("d", "first three sessions of the month", 3),
        ):
            cc = np.array([r[1] for r in rows[key]])
            oo = np.array([r[2] for r in rows[key]])
            out.append(f"| {sym} | {name} | {cell(cc)} | {cell(cc - n * mean_day)} | {cell(oo)} |")
            first = np.array([r[1] for r in rows[key] if r[0] < date(2014, 1, 1)])
            second = np.array([r[1] for r in rows[key] if r[0] >= date(2014, 1, 1)])
            halves.append(f"| {sym} | {name} | {cell(first)} | {cell(second)} |")
    out += ["", "The same, by half of the period:", "", *halves]
    return [*out, ""]


def main() -> None:
    out = ["# wide-1, step 4: three post-hoc patterns on data no rule has seen", ""]
    out += [
        'Definitions fixed in `wide-1.md` ("Step 4") before this data was read. Descriptive: no '
        "rule is selected, nothing is logged in `tries.md`. Bond returns are an approximation "
        "from FRED constant-maturity yields (`DGS10` from 1962, `DGS30` from 1977), close to "
        'close. "Unseen" = before 2003-08, when our TLT and IEF tests start. One deviation '
        "from the definition: carry is booked per calendar day elapsed (yield x days / 365), "
        "not as yield / 252 per session, so weekends are handled; the average is the same.",
        "",
    ]
    out += q1() + q2() + q3() + cross_check()
    c.write_result("wide-1-yields", "\n".join(out))


if __name__ == "__main__":
    main()
