"""Lane parked-gates-1: gates W32 `drought-inflation` and W33 `margin-susceptibles`
(research/cards/parked-gates-1.md; rules pushed before this script's first run).

Descriptive only: no strategy, no backtest. Train bars only, cut at 2025-10-31 (this night's
lane rule); drought months and Financial Accounts quarters after 2025-10-31 are never read. Dose
files are untrusted downloads in the shared cache: run with `python -I`.

Fetch the doses once:  `uv run python -I research/lib/parkedgates1.py fetch`
Run:                   `uv run python -I research/lib/parkedgates1.py`  (DRY=1: counts only)
Output: research/results/drought-inflation.md and research/results/margin-susceptibles.md
"""

from __future__ import annotations

import math
import os
import subprocess
import sys
import urllib.request
from collections.abc import Callable, Hashable, Sequence
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import harness  # noqa: E402
import parkedgates1_events as ev  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as e13  # noqa: E402
import wide17_events as e17  # noqa: E402

from grimstrade import cache  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)  # lane rule: nothing after this date is read
SNAP = "2026-11-25"
CLIMDIV = (
    "https://www.ncei.noaa.gov/monitoring-content/data/us/climdiv/monthly/current/"
    "climdiv-pdsist-v1.0.0-20261105"
)
FRED = "https://fred.stlouisfed.org/graph/fredgraph.csv?id={id}"
RECV, MV = "BOGZ1FL663067003Q", "BOGZ1LM893064105Q"
DGS10, FOOD = "DGS10", "CPIUFDSL"  # R32 (cards/parked-gates-1b.md)
UA = "Mozilla/5.0 (daily-bar research script)"

Key = Hashable
DoseFn = Callable[[int], float]
YFn = Callable[[str, int], float]


def _get(url: str) -> bytes:
    """GET with a generic User-Agent; FRED's graph CSV times out under urllib from this
    machine (2026-11-25), so curl with its default User-Agent is the fallback."""
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data: bytes = r.read()
        return data
    except TimeoutError:
        out = subprocess.run(
            ["curl", "-sS", "-f", "-m", "120", url], check=True, capture_output=True
        )
        return out.stdout


def fetch() -> None:
    """Download the three dose files into `<cache_root>/parked-gates-1/` (write-once)."""
    root = dw.cache_root()
    rel = f"parked-gates-1/climdiv/{SNAP}/climdiv-pdsist-v1.0.0-20261105"
    if not (root / rel).exists():
        cache.write_once(root, rel, _get(CLIMDIV), CLIMDIV)
    for sid in (RECV, MV, DGS10, FOOD):
        rel = f"parked-gates-1/fred/{SNAP}/{sid}.csv"
        if not (root / rel).exists():
            url = FRED.format(id=sid)
            cache.write_once(root, rel, _get(url), url)
    print("fetched into", root / "parked-gates-1")


def _read(rel: str) -> str:
    return (dw.cache_root() / "parked-gates-1" / rel).read_text(encoding="utf-8", errors="replace")


def fit(
    assets: Sequence[str],
    months: Sequence[int],
    y_fn: YFn,
    cols_fn: Sequence[Callable[[str, int], float]],
    lags: int,
    j: int = 0,
) -> tuple[float, float, int]:
    """(b, t, rows) of regressor j: y = asset intercepts + regressors, Driscoll-Kraay t over the
    month (Newey-West with one asset). The one code path for every cell, true and placebo."""
    rs = [(a, m) for a in assets for m in months]
    y = np.array([y_fn(a, m) for a, m in rs])
    cols = [np.array([1.0 if a == s else 0.0 for a, _ in rs]) for s in assets]
    cols += [np.array([c(a, m) for a, m in rs]) for c in cols_fn]
    beta, tt, n = e11.ols_dk(cols, y, np.array([m for _, m in rs]), lags)
    k = len(assets) + j
    return float(beta[k]), float(tt[k]), n


def null_lines(
    t: float, placebo: list[float], shifts: Sequence[int], sign: int
) -> tuple[int, list[str]]:
    """Rank of the true t in the predicted direction (1 = most extreme) and the null block."""
    rank = e11.rank_highest(sign * t, [sign * p for p in placebo])
    sd, share = e11.null_spread(placebo)
    q5, med, q95 = e13.quantiles(placebo)
    lines = [
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {q5:+.2f}, 50% {med:+.2f}, 95% {q95:+.2f}; smallest"
        f" {min(placebo):+.2f}, largest {max(placebo):+.2f}.",
        "",
        "| k (months; > 0 an earlier dose) | t |",
        "|---:|---:|",
        *[f"| {k:+d} | {v:+.2f} |" for k, v in zip(shifts, placebo, strict=True)],
        "",
    ]
    return rank, lines


def cell(name: str, r: tuple[float, float, int], scale: float = 100.0) -> str:
    return f"| {name} | {r[0] * scale:+.3f} ({r[1]:+.2f}) | {r[2]} |"


# ---------------------------------------------------------------- W32


def drought_inflation(px: dict[str, e13.Closes]) -> None:
    pdsi = ev.parse_pdsi(_read(f"climdiv/{SNAP}/climdiv-pdsist-v1.0.0-20261105"), LAST)
    d = ev.drought_dose(pdsi)
    ch = ev.drought_change(pdsi)
    lo, hi = e17.month_index(date(2002, 7, 1)), e17.month_index(date(2025, 6, 1))
    months = list(range(lo, hi + 1))

    def y(start: int = 1, h: int = 3) -> YFn:
        return lambda s, m: e17.month_return(px[s], m + start, m + start + h, LAST)

    def at(src: dict[int, float], k: int = 0) -> list[Callable[[str, int], float]]:
        return [lambda _s, m: e17.shifted_month(src, m, k)]

    if DRY:
        print("W32 PDSI months read", len(pdsi), "first", min(pdsi), "last", max(pdsi),
              "=", e17.month_last_day(max(pdsi)))  # fmt: skip
        for s in ("TLT", "GLD", "DBC", "IEF", "SPY"):
            ok = sum(not math.isnan(y()(s, m)) and m in d for m in months)
            print("W32", s, "rows with outcome and dose", ok)
        ns = [
            sum(not math.isnan(e17.shifted_month(d, m, k)) and not math.isnan(y()("TLT", m))
                for m in months)
            for k in e17.SHIFTS_W29
        ]  # fmt: skip
        print("W32 placebos", len(e17.SHIFTS_W29), "rows min", min(ns), "max", max(ns))
        return

    b, t, n = fit(["TLT"], months, y(), at(d), 3)
    placebo = [fit(["TLT"], months, y(), at(d, k), 3)[1] for k in e17.SHIFTS_W29]
    rank, null = null_lines(t, placebo, e17.SHIFTS_W29, -1)
    met = [b < 0 and t <= -2, rank <= 2]
    season = [m for m in months if m % 12 in (4, 5, 6, 7, 8)]
    out = [
        "# US drought and TLT over the next quarter (parked-gates-1, W32 `drought-inflation`)",
        "",
        "Rule: `research/cards/parked-gates-1.md` (pushed before this ran). Script",
        "`research/lib/parkedgates1.py`. Dose D(m) = -PDSI(m), contiguous US (NOAA nClimDiv,",
        "2026-11-05 vintage). y = log return of TLT from the last bar of month m+1 to the last",
        "bar of month m+4. Newey-West t, 3 lags, one row a dose month.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Dose months 2002-07..2025-06, b (t), {n} rows | {b * 100:+.3f}% per PDSI unit"
        f" ({t:+.2f}) | < 0, t <= -2 | {met[0]} |",
        f"| Rank of true t among 41 calendars (1 = lowest) | {rank} | <= 2 | {met[1]} |",
        "",
        f"**Gate: {'PASS (kill-only design: not dead yet)' if all(met) else 'fail'}.**"
        f" Empirical one-sided p = {rank}/41 = {rank / 41:.3f}.",
        "",
        "## Placebo null (dose calendar moved k months, both ways)",
        "",
        *null,
        "## Shown (not gating)",
        "",
        "| Cut | b, % per unit (t) | Rows |",
        "|---|---:|---:|",
        cell("GLD instead of TLT (predicted > 0)", fit(["GLD"], months, y(), at(d), 3)),
        cell("DBC instead of TLT (predicted > 0)", fit(["DBC"], months, y(), at(d), 3)),
        cell("IEF instead of TLT", fit(["IEF"], months, y(), at(d), 3)),
        cell("SPY instead of TLT", fit(["SPY"], months, y(), at(d), 3)),
        cell("1-month horizon (month m+2 only)", fit(["TLT"], months, y(h=1), at(d), 3)),
        cell("6-month horizon (m+2..m+7, NW 6 lags)", fit(["TLT"], months, y(h=6), at(d), 6)),
        cell("Growing-season dose months only (May-Sep)", fit(["TLT"], season, y(), at(d), 3)),
        cell("3-month change PDSI(m-3) - PDSI(m) as dose", fit(["TLT"], months, y(), at(ch), 3)),
        cell(
            "Reaction: TLT over month m+1 (release month)",
            fit(["TLT"], months, y(start=0, h=1), at(d), 3),
        ),  # fmt: skip
        "",
        f"Dose sd over the gate months: {np.std([d[m] for m in months if m in d]):.2f} PDSI units.",
        "",
    ]
    (RESULTS / "drought-inflation.md").write_text("\n".join(out))
    print("\n".join(out))


# ---------------------------------------------------------------- W33


def margin_susceptibles(px: dict[str, e13.Closes]) -> None:
    recv = ev.parse_fred(_read(f"fred/{SNAP}/{RECV}.csv"), LAST)
    mv = ev.parse_fred(_read(f"fred/{SNAP}/{MV}.csv"), LAST)
    sq = ev.susceptible_dose(recv, mv)
    s3 = ev.monthly_known(sq, 3)
    s6 = ev.monthly_known(sq, 6)
    lo, hi = e17.month_index(date(1965, 1, 1)), e17.month_index(date(2025, 9, 1))
    months = list(range(lo, hi + 1))

    def r(sym: str, m: int) -> float:
        return e17.month_return(px[sym], m - 1, m, LAST)

    def y(sym: str, m: int) -> float:
        return r(sym, m + 1)

    def regs(
        sm: dict[int, float], k: int = 0, controls: bool = True, binary: bool = False
    ) -> list[Callable[[str, int], float]]:
        def f(a: str, m: int) -> float:
            v = r(a, m)
            if binary:
                return v if math.isnan(v) else float(v < -0.05)
            return ev.fall(v)

        def s(_a: str, m: int) -> float:
            return e17.shifted_month(sm, m, k)

        def c(a: str, m: int) -> float:
            return e17.month_return(px[a], m - 13, m - 1, LAST)

        cols: list[Callable[[str, int], float]] = [lambda a, m: f(a, m) * s(a, m), f, s]
        if controls:
            cols += [c, lambda a, m: f(a, m) * c(a, m)]
        return cols

    if DRY:
        print("W33 receivables quarters", len(recv), "first", min(recv), "last", max(recv),
              "=", e17.month_last_day(max(recv)))  # fmt: skip
        print("W33 market-value quarters", len(mv), "first", min(mv), "last", max(mv))
        print("W33 s quarters", len(sq), "first", min(sq), "monthly s", len(s3))
        ok = sum(not math.isnan(y("GSPC", m)) and m in s3 for m in months)
        print("W33 gate months", len(months), "rows with outcome and s", ok)
        ns = [
            sum(not math.isnan(e17.shifted_month(s3, m, k)) and not math.isnan(y("GSPC", m))
                for m in months)
            for k in ev.SHIFTS_W33
        ]  # fmt: skip
        print("W33 placebos", len(ev.SHIFTS_W33), "rows min", min(ns), "max", max(ns))
        spy = sum(not math.isnan(y("SPY", m)) and not math.isnan(r("SPY", m)) for m in months)
        print("W33 SPY rows", spy)
        return

    b, t, n = fit(["GSPC"], months, y, regs(s3), 3)
    placebo = [fit(["GSPC"], months, y, regs(s3, k), 3)[1] for k in ev.SHIFTS_W33]
    rank, null = null_lines(t, placebo, ev.SHIFTS_W33, 1)
    met = [b > 0 and t >= 2, rank <= 2]
    early = [m for m in months if m <= e17.month_index(date(1994, 12, 1))]
    late = [m for m in months if m > e17.month_index(date(1994, 12, 1))]
    # Added after the dry run, before the real run: Z.1 is annual before 1952, so s starts
    # 1961-12 and placebos up to k = 103 lack rows before 1970-10. Same rows for all 41 fits:
    same = [m for m in months if m >= e17.month_index(date(1970, 10, 1))]
    b_s, t_s, n_s = fit(["GSPC"], same, y, regs(s3), 3)
    p_s = [fit(["GSPC"], same, y, regs(s3, k), 3)[1] for k in ev.SHIFTS_W33]
    rank_s = e11.rank_highest(t_s, p_s)
    sd_s, share_s = e11.null_spread(p_s)
    out = [
        "# Margin credit as the susceptible stock of a crash (parked-gates-1, W33"
        " `margin-susceptibles`)",
        "",
        "Rule: `research/cards/parked-gates-1.md` (pushed before this ran). Script",
        "`research/lib/parkedgates1.py`. s = ln(broker receivables from customers / equities",
        "market value) minus its 40-quarter mean (Z.1 via FRED, today's vintage), known from",
        "3 months after the quarter end. y = GSPC log return over month m+1 on F = min(r(m), 0),",
        "s, F s, c = GSPC return over months m-12..m-1, F c. Newey-West t, 3 lags. b3 = F s.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Months 1965-01..2025-09, b3 (t), {n} rows | {b:+.3f} ({t:+.2f}) | > 0, t >= 2 |"
        f" {met[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {met[1]} |",
        "",
        f"**Gate: {'PASS (kill-only design: not dead yet)' if all(met) else 'fail'}.**"
        f" Empirical one-sided p = {rank}/41 = {rank / 41:.3f}.",
        "",
        "## Placebo null (s calendar moved k months back only)",
        "",
        *null,
        "## Shown (not gating)",
        "",
        "| Cut | b3 (t) | Rows |",
        "|---|---:|---:|",
        cell("Without controls", fit(["GSPC"], months, y, regs(s3, controls=False), 3), 1),
        cell(
            "Binary trigger 1[r(m) < -5%] x s",
            fit(["GSPC"], months, y, regs(s3, binary=True), 3),
            1,
        ),  # fmt: skip
        cell(
            "Stricter release lag (quarter end <= m - 6)", fit(["GSPC"], months, y, regs(s6), 3), 1
        ),
        cell("SPY instead of GSPC", fit(["SPY"], months, y, regs(s3), 3), 1),
        cell("Months 1965-01..1994-12", fit(["GSPC"], early, y, regs(s3), 3), 1),
        cell("Months 1995-01..2025-09", fit(["GSPC"], late, y, regs(s3), 3), 1),
        cell("Main effect b1 (F)", fit(["GSPC"], months, y, regs(s3), 3, j=1), 1),
        cell("Main effect b2 (s)", fit(["GSPC"], months, y, regs(s3), 3, j=2), 1),
        "",
        f"Same rows for all 41 fits (months 1970-10..2025-09, added after the dry run): b3"
        f" {b_s:+.3f} (t {t_s:+.2f}), {n_s} rows, rank {rank_s} of 41; placebo SD {sd_s:.2f},"
        f" share |t| >= 2 {share_s:.0%}.",
        "",
        f"s sd over the gate months: {np.std([s3[m] for m in months if m in s3]):.3f};"
        f" months with a fall below -5%: {sum(r('GSPC', m) < -0.05 for m in months)}.",
        "",
    ]
    (RESULTS / "margin-susceptibles.md").write_text("\n".join(out))
    print("\n".join(out))


# ---------------------------------------------------------------- R32 (cards/parked-gates-1b.md)


def replication(px: dict[str, e13.Closes]) -> None:
    pdsi = ev.parse_pdsi(_read(f"climdiv/{SNAP}/climdiv-pdsist-v1.0.0-20261105"), LAST)
    d = ev.drought_dose(pdsi)
    ye = ev.month_end_values(ev.parse_fred_daily(_read(f"fred/{SNAP}/{DGS10}.csv"), LAST))
    cpi = ev.parse_fred_monthly(_read(f"fred/{SNAP}/{FOOD}.csv"), LAST)
    mi = e17.month_index

    def span(a: date, b: date) -> list[int]:
        return list(range(mi(a), mi(b) + 1))

    rep = span(date(1962, 1, 1), date(2002, 3, 1))
    w32 = span(date(2002, 7, 1), date(2025, 6, 1))
    full = span(date(1962, 1, 1), date(2025, 6, 1))

    def dy(start: int = 1, h: int = 3) -> YFn:
        def f(_s: str, m: int) -> float:
            a, b = ye.get(m + start), ye.get(m + start + h)
            return math.nan if a is None or b is None else b - a

        return f

    def food(_s: str, m: int) -> float:
        a, b = cpi.get(m + 1), cpi.get(m + 4)
        return math.nan if a is None or b is None else math.log(b / a)

    def tlt(s: str, m: int) -> float:
        return e17.month_return(px["TLT"], m + 1, m + 4, LAST)

    def at(k: int = 0) -> list[Callable[[str, int], float]]:
        return [lambda _s, m: e17.shifted_month(d, m, k)]

    if DRY:
        print("R32 yield months", len(ye), "first", min(ye), "last", max(ye))
        print("R32 food CPI months", len(cpi), "first", min(cpi), "last", max(cpi))
        print("R32 rows", sum(not math.isnan(dy()("", m)) and m in d for m in rep), "of", len(rep))
        return

    b, t, n = fit(["Y"], rep, dy(), at(), 3)
    placebo = [fit(["Y"], rep, dy(), at(k), 3)[1] for k in e17.SHIFTS_W29]
    rank, null = null_lines(t, placebo, e17.SHIFTS_W29, 1)
    met = [b > 0 and t >= 2, rank <= 2]
    season = [m for m in rep if m % 12 in (4, 5, 6, 7, 8)]

    def without(lo: date, hi: date) -> list[int]:
        return [m for m in w32 if not mi(lo) <= m <= mi(hi)]

    drops = [
        ("2002-07..2003-12", date(2002, 7, 1), date(2003, 12, 1)),
        ("2006-01..2008-12", date(2006, 1, 1), date(2008, 12, 1)),
        ("2011-01..2013-12", date(2011, 1, 1), date(2013, 12, 1)),
        ("2020-01..2023-06", date(2020, 1, 1), date(2023, 6, 1)),
        ("2021-08..2022-10 (outcome touches 2022)", date(2021, 8, 1), date(2022, 10, 1)),
    ]
    out = [
        "# Drought and the 10-year yield, 1962-2002 (parked-gates-1, R32: replication of W32)",
        "",
        "Rule: `research/cards/parked-gates-1b.md` (pushed after W32's result, before this ran).",
        "Dose D(m) = -PDSI(m), contiguous US. y = DGS10 at the end of month m+4 minus DGS10 at",
        "the end of month m+1 (percentage points). Newey-West t, 3 lags, one row a dose month.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Dose months 1962-01..2002-03, b (t), {n} rows | {b * 100:+.2f} bp per PDSI unit"
        f" ({t:+.2f}) | > 0, t >= 2 | {met[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {met[1]} |",
        "",
        f"**Gate: {'PASS (kill-only design: not dead yet)' if all(met) else 'fail'}.**"
        f" Empirical one-sided p = {rank}/41 = {rank / 41:.3f}.",
        "",
        "## Placebo null (dose calendar moved k months, both ways)",
        "",
        *null,
        "## Shown (not gating)",
        "",
        "| Cut | b (t) | Rows |",
        "|---|---:|---:|",
        cell("Yield, dose months 2002-07..2025-06 (bp per unit)", fit(["Y"], w32, dy(), at(), 3)),
        cell("Yield, dose months 1962-01..2025-06 (bp per unit)", fit(["Y"], full, dy(), at(), 3)),
        cell("Yield, growing season May-Sep 1962-2002 (bp)", fit(["Y"], season, dy(), at(), 3)),
        cell("Reaction: yield over month m+1, 1962-2002 (bp)", fit(["Y"], rep, dy(0, 1), at(), 3)),
        cell(
            "Food CPI log change m+1..m+4, 1962-2025 (% per unit)", fit(["Y"], full, food, at(), 3)
        ),
        cell(
            "Food CPI log change m+1..m+4, 1962-2002 (% per unit)", fit(["Y"], rep, food, at(), 3)
        ),
        "",
        "## Post hoc on W32's gate sample (TLT, % per unit; descriptive, picked after W32)",
        "",
        "| Dose months left out | b (t) | Rows |",
        "|---|---:|---:|",
        cell("none (W32's gate)", fit(["TLT"], w32, tlt, at(), 3)),
        *[cell(name, fit(["TLT"], without(lo, hi), tlt, at(), 3)) for name, lo, hi in drops],
        "",
    ]
    (RESULTS / "drought-inflation-r32.md").write_text("\n".join(out))
    print("\n".join(out))


def main() -> None:
    if sys.argv[1:] == ["fetch"]:
        fetch()
        return
    syms = ["TLT", "GLD", "DBC", "IEF", "SPY", "GSPC"]
    hist = harness.load_history("train", syms=syms)
    px = {
        s: e13.Closes({b.date: b.close for b in bars if b.date <= LAST}) for s, bars in hist.items()
    }
    which = os.environ.get("GATE", "both")
    if which in ("both", "W32"):
        drought_inflation(px)
    if which in ("both", "W33"):
        margin_susceptibles(px)
    if which == "R32":
        replication(px)


if __name__ == "__main__":
    main()
