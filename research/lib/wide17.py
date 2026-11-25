"""Lane wide-17: gates W29 `temperature-premium` and W30 `outbreak-premium`
(research/cards/wide-17.md; rules pushed before this script's first run).

Descriptive only: no strategy, no backtest. Train bars only, cut at 2025-10-31 (this night's
lane rule); temperature months and outbreak reports after 2025-10-31 are never read. Dose files
are untrusted downloads in the shared cache: run with `python -I`.

Fetch the doses once:  `uv run python -I research/lib/wide17.py fetch`
Run:                   `uv run python -I research/lib/wide17.py`  (DRY=1: counts only)
Output: research/results/temperature-premium.md and research/results/outbreak-premium.md
"""

from __future__ import annotations

import math
import os
import sys
import urllib.request
from collections.abc import Callable, Hashable, Sequence
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as e13  # noqa: E402
import wide17_events as ev  # noqa: E402

from grimstrade import cache  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)  # lane rule: nothing after this date is read
SNAP = "2026-11-24"
GISTEMP = "https://data.giss.nasa.gov/gistemp/tabledata_v4/GLB.Ts+dSST.csv"
DON = (
    "https://www.who.int/api/news/diseaseoutbreaknews?$orderby=PublicationDate%20asc"
    "&$filter=PublicationDate%20le%202025-10-31T23:59:59Z&$select=Title,PublicationDate"
    "&$top=100&$skip={skip}"
)
DON_COUNT = (
    "https://www.who.int/api/news/diseaseoutbreaknews/$count"
    "?$filter=PublicationDate%20le%202025-10-31T23:59:59Z"
)
UA = "Mozilla/5.0 (daily-bar research script)"
HS = (28, 91, 182, 364)

Key = Hashable
Row = tuple[str, Key]
DoseFn = Callable[[Key], float]
YFn = Callable[[str, Key], float]


def _get(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=120) as r:
        data: bytes = r.read()
    return data


def fetch() -> None:
    """Download both dose files into `<cache_root>/wide-17/` (write-once, manifest)."""
    root = dw.cache_root()
    rel = f"wide-17/gistemp/{SNAP}/GLB.Ts+dSST.csv"
    if not (root / rel).exists():
        cache.write_once(root, rel, _get(GISTEMP), GISTEMP)
    total = int(_get(DON_COUNT).decode("utf-8-sig").strip())
    for i, skip in enumerate(range(0, total, 100)):
        rel = f"wide-17/who-don/{SNAP}/page-{i:02d}.json"
        if not (root / rel).exists():
            url = DON.format(skip=skip)
            cache.write_once(root, rel, _get(url), url)
    print("fetched into", root / "wide-17", "DON items", total)


def load_gistemp() -> dict[int, float]:
    p = dw.cache_root() / f"wide-17/gistemp/{SNAP}/GLB.Ts+dSST.csv"
    return ev.parse_gistemp(p.read_text(encoding="utf-8", errors="replace"), LAST)


def load_don() -> list[date]:
    folder = dw.cache_root() / f"wide-17/who-don/{SNAP}"
    return ev.parse_don_pages([p.read_text() for p in sorted(folder.glob("page-*.json"))], LAST)


def fit(
    assets: Sequence[str],
    keys: Sequence[Key],
    y_fn: YFn,
    doses: Sequence[DoseFn],
    period: Callable[[Key], int],
    lags: int,
    controls: Sequence[YFn] = (),
) -> tuple[float, float, int]:
    """(b, t, rows) of the first dose: y = asset intercepts + doses + controls, Driscoll-Kraay
    t (Newey-West over `period` when there is one asset). The one code path for every cell."""
    rs: list[Row] = [(a, k) for a in assets for k in keys]
    y = np.array([y_fn(a, k) for a, k in rs])
    cols = [np.array([1.0 if a == m else 0.0 for a, _ in rs]) for m in assets]
    cols += [np.array([d(k) for _, k in rs]) for d in doses]
    cols += [np.array([c(a, k) for a, k in rs]) for c in controls]
    beta, tt, n = e11.ols_dk(cols, y, np.array([period(k) for _, k in rs]), lags)
    j = len(assets)
    return float(beta[j]), float(tt[j]), n


def gate_block(
    title: str,
    b: float,
    t: float,
    n: int,
    placebo: list[float],
    shifts: Sequence[int],
    unit: str,
    step: str,
) -> list[str]:
    rank = e11.rank_highest(t, placebo)
    sd, share = e11.null_spread(placebo)
    q5, med, q95 = e13.quantiles(placebo)
    met = [b > 0 and t >= 2, rank <= 2]
    return [
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| {title}, b (t), {n} rows | {b * 100:+.3f}% {unit} ({t:+.2f}) | > 0, t >= 2 |"
        f" {met[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {met[1]} |",
        "",
        f"**Gate: {'PASS (kill-only design: not dead yet)' if all(met) else 'fail'}.**"
        f" Empirical one-sided p = {rank}/41 = {rank / 41:.3f}. (t - placebo median) /"
        f" placebo sd = {(t - med) / sd:+.2f} (descriptive only).",
        "",
        f"## Placebo null (dose calendar moved k {step}s; k > 0 an earlier dose)",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {q5:+.2f}, 50% {med:+.2f}, 95% {q95:+.2f}; smallest"
        f" {min(placebo):+.2f}, largest {max(placebo):+.2f}.",
        "",
        f"| k ({step}s) | t |",
        "|---:|---:|",
        *[f"| {k:+d} | {v:+.2f} |" for k, v in zip(shifts, placebo, strict=True)],
        "",
        "## Shown (not gating)",
        "",
        "| Cut | b, % per unit (t) | Rows |",
        "|---|---:|---:|",
    ]


def cell(name: str, r: tuple[float, float, int]) -> str:
    return f"| {name} | {r[0] * 100:+.3f} ({r[1]:+.2f}) | {r[2]} |"


# ---------------------------------------------------------------- W29


def temperature_premium(px: dict[str, e13.Closes]) -> None:
    anom = load_gistemp()
    d = ev.temp_dose(anom)
    inn = ev.temp_innovation(anom)
    lo, hi = ev.month_index(date(1993, 2, 1)), ev.month_index(date(2025, 10, 1))
    dose_months = list(range(lo - 2, hi - 1))  # outcome month = dose month + 2

    def y(h: int = 1, start: int = 1) -> YFn:
        return lambda s, m: ev.month_return(px[s], int(m) + start, int(m) + start + h, LAST)

    def at(src: dict[int, float], k: int = 0) -> list[DoseFn]:
        return [lambda m: ev.shifted_month(src, int(m), k)]

    def per(m: Key) -> int:
        return int(m)  # type: ignore[call-overload]

    if DRY:
        print("W29 months read", len(anom), "first", min(anom), "last", max(anom),
              "=", ev.month_last_day(max(anom)))  # fmt: skip
        print("W29 dose months", len(d), "gate dose months", len(dose_months),
              "with d", sum(m in d for m in dose_months))  # fmt: skip
        for s in ("SPY", "QQQ", "TLT", "GLD", "BTC", "ETH"):
            ok = sum(not math.isnan(y()(s, m)) and m in d for m in dose_months)
            print("W29", s, "rows with outcome and dose", ok)
        ns = [
            sum(not math.isnan(ev.shifted_month(d, m, k)) and not math.isnan(y()("SPY", m))
                for m in dose_months)
            for k in ev.SHIFTS_W29
        ]  # fmt: skip
        print("W29 placebos", len(ev.SHIFTS_W29), "rows min", min(ns), "max", max(ns))
        return

    b, t, n = fit(["SPY"], dose_months, y(), at(d), per, 3)
    placebo = [fit(["SPY"], dose_months, y(), at(d, k), per, 3)[1] for k in ev.SHIFTS_W29]
    late = [m for m in dose_months if m + 2 >= ev.month_index(date(2013, 1, 1))]
    out = [
        "# Global temperature shocks and SPY's next month (wide-17, W29 `temperature-premium`)",
        "",
        "Rule: `research/cards/wide-17.md` (pushed before this ran). Script",
        "`research/lib/wide17.py`. Dose d(m) = 12-month mean of the GISTEMP v4 global",
        "land-ocean anomaly minus its mean over the 10 years before (deg C; 2026-11-24 vintage).",
        "y = log return of SPY over calendar month m + 2 (close of the last bar of m + 1 to the",
        "close of the last bar of m + 2). Newey-West t, 3 lags, one row a month.",
        "",
        *gate_block(
            "Outcome months 1993-02..2025-10",
            b,
            t,
            n,
            placebo,
            ev.SHIFTS_W29,
            "per deg C",
            "month",
        ),  # fmt: skip
        cell("QQQ instead of SPY", fit(["QQQ"], dose_months, y(), at(d), per, 3)),
        cell("TLT instead of SPY", fit(["TLT"], dose_months, y(), at(d), per, 3)),
        cell("GLD instead of SPY", fit(["GLD"], dose_months, y(), at(d), per, 3)),
        cell(
            "BTC and ETH pooled (DK 3 lags)", fit(["BTC", "ETH"], dose_months, y(), at(d), per, 3)
        ),
        cell(
            "12-month horizon (months m+2..m+13, NW 12 lags)",
            fit(["SPY"], dose_months, y(h=12), at(d), per, 12),
        ),  # fmt: skip
        cell(
            "Monthly innovation A(m) - mean of the 120 months before",
            fit(["SPY"], dose_months, y(), at(inn), per, 3),
        ),  # fmt: skip
        cell(
            "Outcome months 2013-01..2025-10 (after the literature)",
            fit(["SPY"], late, y(), at(d), per, 3),
        ),  # fmt: skip
        cell(
            "Reaction: SPY over month m+1 (release month; premium story: negative)",
            fit(["SPY"], dose_months, y(start=0), at(d), per, 3),
        ),  # fmt: skip
        "",
        f"Dose sd over the gate months: {np.nanstd([d.get(m, np.nan) for m in dose_months]):.3f}"
        " deg C.",
        "",
    ]
    (RESULTS / "temperature-premium.md").write_text("\n".join(out))
    print("\n".join(out))


# ---------------------------------------------------------------- W30


def outbreak_premium(px: dict[str, e13.Closes]) -> None:
    days = load_don()
    weeks = e13.fridays(date(2004, 1, 9), LAST)
    counts = ev.weekly_counts(days, weeks)
    x = ev.outbreak_dose(counts)
    z = {f: 2.0 * math.sqrt(n + 0.375) for f, n in counts.items()}
    gate_dates = e13.fridays(date(2005, 1, 7), date(2025, 9, 26))
    ref = date(2005, 1, 7)

    def per(f: Key) -> int:
        return round((f - ref).days / 7)  # type: ignore[operator]

    def y(exit_: int = 31) -> YFn:
        return lambda s, f: e13.window_return(px[s], f, 3, exit_, 7, LAST)  # type: ignore[arg-type]

    def at(src: dict[date, float], k: int = 0) -> list[DoseFn]:
        return [lambda f: e13.shifted(src, f, k)]  # type: ignore[arg-type]

    def react(s: str, f: Key) -> float:
        return e13.past_return(px[s], f, 7)  # type: ignore[arg-type]

    ctrl: list[YFn] = [
        (lambda s, f, h=h: e13.past_return(px[s], f, h))  # type: ignore[misc]
        for h in HS
    ]

    if DRY:
        print("W30 reports read", len(days), "first", min(days), "last", max(days))
        print("W30 weeks", len(weeks), "dose weeks", len(x), "gate Fridays", len(gate_dates),
              "with x", sum(f in x for f in gate_dates))  # fmt: skip
        for s in ("SPY", "QQQ", "GLD", "TLT", "XLV", "BTC", "ETH"):
            ok = sum(not math.isnan(y()(s, f)) and f in x for f in gate_dates)
            print("W30", s, "rows with outcome and dose", ok)
        ns = [
            sum(not math.isnan(e13.shifted(x, f, k)) and not math.isnan(y()("SPY", f))
                for f in gate_dates)
            for k in e13.SHIFTS
        ]  # fmt: skip
        print("W30 placebos", len(e13.SHIFTS), "rows min", min(ns), "max", max(ns))
        return

    b, t, n = fit(["SPY"], gate_dates, y(), at(x), per, 4)
    placebo = [fit(["SPY"], gate_dates, y(), at(x, k), per, 4)[1] for k in e13.SHIFTS]
    late = [f for f in gate_dates if f >= date(2015, 1, 2)]
    xs = [x[f] for f in gate_dates if f in x]
    out = [
        "# WHO outbreak reports and SPY over the next 4 weeks (wide-17, W30 `outbreak-premium`)",
        "",
        "Rule: `research/cards/wide-17.md` (pushed before this ran). Script",
        "`research/lib/wide17.py`. Dose x(F) = 2 sqrt(n + 3/8) minus its mean over the 52",
        "weeks before, n = WHO Disease Outbreak News items published Saturday..Friday F.",
        "y = log return of SPY from the close of the first bar >= F + 3 to the first bar",
        ">= F + 31. Newey-West t, 4 lags, one row a week. Placebos both ways (allowed: WHO",
        "reporting does not answer prices).",
        "",
        *gate_block(
            "Fridays 2005-01-07..2025-09-26",
            b,
            t,
            n,
            placebo,
            e13.SHIFTS,
            "per unit of x",
            "week",
        ),  # fmt: skip
        cell("QQQ instead of SPY", fit(["QQQ"], gate_dates, y(), at(x), per, 4)),
        cell("GLD instead of SPY", fit(["GLD"], gate_dates, y(), at(x), per, 4)),
        cell("TLT instead of SPY", fit(["TLT"], gate_dates, y(), at(x), per, 4)),
        cell("XLV (health care) instead of SPY", fit(["XLV"], gate_dates, y(), at(x), per, 4)),
        cell("BTC and ETH pooled (DK 4 lags)", fit(["BTC", "ETH"], gate_dates, y(), at(x), per, 4)),
        cell("Raw Anscombe count z instead of x", fit(["SPY"], gate_dates, y(), at(z), per, 4)),
        cell(
            "1-week horizon (exit >= F + 10, 1 lag)", fit(["SPY"], gate_dates, y(10), at(x), per, 1)
        ),  # fmt: skip
        cell(
            "Fridays 2015-01-02..2025-09-26 (after Donadelli et al.)",
            fit(["SPY"], late, y(), at(x), per, 4),
        ),  # fmt: skip
        cell(
            "With SPY's past 4/13/26/52-week returns",
            fit(["SPY"], gate_dates, y(), at(x), per, 4, ctrl),
        ),  # fmt: skip
        cell(
            "Reaction: SPY over the dose week itself (premium story: negative)",
            fit(["SPY"], gate_dates, react, at(x), per, 4),
        ),  # fmt: skip
        "",
        f"Dose: {len(days)} reports to 2025-10-31; x sd over the gate weeks {np.std(xs):.2f};"
        f" weeks with no report {sum(counts[f] == 0 for f in gate_dates)} of {len(gate_dates)}.",
        "",
    ]
    (RESULTS / "outbreak-premium.md").write_text("\n".join(out))
    print("\n".join(out))


def main() -> None:
    if sys.argv[1:] == ["fetch"]:
        fetch()
        return
    syms = ["SPY", "QQQ", "TLT", "GLD", "BTC", "ETH", "XLV"]
    hist = harness.load_history("train", syms=syms)
    px = {
        s: e13.Closes({b.date: b.close for b in bars if b.date <= LAST}) for s, bars in hist.items()
    }
    which = os.environ.get("GATE", "both")
    if which in ("both", "W29"):
        temperature_premium(px)
    if which in ("both", "W30"):
        outbreak_premium(px)


if __name__ == "__main__":
    main()
