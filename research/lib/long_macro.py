"""Long consumer prices, country equity yields and policy rates (data-long-4).

Raw files come from `long_macro_fetch.py` (keyless, cached under `<cache_root>/data-long-4/`,
never committed). This module only parses and derives; it does no network I/O, and every
reader cuts at `LAST` (2025-10-31). Method, checks and caveats: research/data-long-4.md.

Conventions (as data-long-3, `long_x.py`): a series is a list of (date, value) in date order;
monthly values are dated the first of their month, annual values 1 January of their year.
`available` gives the first day a value could have been known.
"""

from __future__ import annotations

import csv
import io
import math
import re
import zipfile
from collections.abc import Sequence
from datetime import date
from pathlib import Path

LAST = date(2025, 10, 31)
# French's annual ratios: the row of year t uses December t-1 prices (alignment measured in the
# write-up), so the 2025 row is train data; later rows are dropped.
LAST_RATIO_YEAR = 2025
QUARTERLY = frozenset({"AU", "NZ"})  # BIS "monthly" CPI repeats the quarter's value

Series = list[tuple[date, float]]

# French international file names -> ISO2 (the 11 data-long-3 economies that French covers,
# plus the other countries in the zip, kept for completeness)
FRENCH_FILES = {
    "UK.Dat": "GB", "Japan.Dat": "JP", "Swtzrlnd.Dat": "CH", "Canada.Dat": "CA",
    "Germany.Dat": "DE", "Austrlia.Dat": "AU", "NewZland.Dat": "NZ", "Sweden.Dat": "SE",
    "Norway.Dat": "NO", "Austria.Dat": "AT", "Belgium.Dat": "BE", "Denmark.Dat": "DK",
    "Finland.Dat": "FI", "France.Dat": "FR", "HongKong.Dat": "HK", "Ireland.Dat": "IE",
    "Italy.Dat": "IT", "Malaysia.Dat": "MY", "Nethrlnd.Dat": "NL", "Singapor.Dat": "SG",
    "Spain.Dat": "ES",
}  # fmt: skip
# JST iso3 -> ISO2 for the data-long-3 economies (JST has no New Zealand)
JST_ISO = {
    "USA": "US", "JPN": "JP", "GBR": "GB", "CHE": "CH", "CAN": "CA", "DEU": "DE",
    "AUS": "AU", "SWE": "SE", "NOR": "NO",
}  # fmt: skip


def _next_month(d: date) -> date:
    return date(d.year + d.month // 12, d.month % 12 + 1, 1)


def _add_months(d: date, n: int) -> date:
    for _ in range(n):
        d = _next_month(d)
    return d


# ---------------------------------------------------------------- BIS SDMX csv


def _period(p: str) -> date:
    if re.fullmatch(r"\d{4}", p):
        return date(int(p), 1, 1)
    m = re.fullmatch(r"(\d{4})-(\d{2})", p)
    if m:
        return date(int(m.group(1)), int(m.group(2)), 1)
    m = re.fullmatch(r"(\d{4})-Q([1-4])", p)
    if m:
        return date(int(m.group(1)), 3 * int(m.group(2)) - 2, 1)
    raise ValueError(f"period {p!r}")


def parse_bis(text: str, last: date = LAST) -> dict[str, Series]:
    """{REF_AREA: series} from a BIS SDMX csv with one series per area (blank values dropped).

    A period is kept only when it ends on or before `last`."""
    out: dict[str, dict[date, float]] = {}
    for r in csv.DictReader(io.StringIO(text)):
        v = (r.get("OBS_VALUE") or "").strip()
        if v in ("", "NaN"):
            continue
        p = r["TIME_PERIOD"]
        d = _period(p)
        end = date(d.year, 12, 31) if len(p) == 4 else _add_months(d, 3 if "Q" in p else 1)
        if (len(p) == 4 and end > last) or (len(p) != 4 and end > _next_month(last)):
            continue
        area = out.setdefault(r["REF_AREA"], {})
        if d in area:
            raise ValueError(f"duplicate {r['REF_AREA']} {p}: more than one series per area")
        area[d] = float(v)
    return {k: sorted(v.items()) for k, v in out.items()}


def quarter_ends(s: Sequence[tuple[date, float]]) -> Series:
    """A repeated-quarterly monthly series as one value per quarter, dated the quarter's first
    month (BIS AU/NZ: the three months of a quarter carry the same value)."""
    return [(d, v) for d, v in s if d.month in (1, 4, 7, 10)]


def yoy(s: Sequence[tuple[date, float]], months: int = 12) -> Series:
    """Percent change over `months` of a monthly index (only where both ends exist)."""
    m = dict(s)
    out: Series = []
    for d, v in s:
        back = date(d.year - months // 12, d.month, 1) if months % 12 == 0 else None
        if back is not None and back in m and m[back] > 0:
            out.append((d, 100.0 * (v / m[back] - 1.0)))
    return out


# ---------------------------------------------------------------- Kenneth R. French .Dat


_RET_HEAD = re.compile(
    r"Value-Weight (Dollar|Local)\s+Returns\s+All 4 Data Items (Not Reqd|Required)"
)
_MISSING = (-99.99, -999.0, -99.0)


def _num(x: str) -> float:
    v = float(x)
    return math.nan if any(abs(v - m) < 1e-9 for m in _MISSING) else v


def parse_french_country(text: str, last: date = LAST) -> dict[str, object]:
    """One French international country file.

    Returns {"monthly": {(currency, items): {column: series in percent}},
             "annual_ratios": {items: {column: series}}}, with currency "Dollar"/"Local",
    items "Not Reqd"/"Required", columns as in the file (Mkt, BE/ME High, ..., Yld Zero) and
    ratio columns Firms, B/M, E/P, CE/P, Yld (ratios x 100, i.e. percent). Annual return
    blocks are skipped (they compound the monthly ones). Missing (-99.99) values are dropped."""
    cols = [
        "Mkt", "BE/ME High", "BE/ME Low", "E/P High", "E/P Low", "CE/P High", "CE/P Low",
        "Yld High", "Yld Low", "Yld Zero",
    ]  # fmt: skip
    monthly: dict[tuple[str, str], dict[str, Series]] = {}
    ratios: dict[str, dict[str, Series]] = {}
    block: tuple[str, ...] | None = None
    ratio_cols: list[str] = []
    for line in text.splitlines():
        h = _RET_HEAD.search(line)
        if h:
            block = ("ret", h.group(1), h.group(2))
            continue
        if line.startswith("All 4 Data Items") and block and block[0] == "ratio?":
            block = ("ratio", "Required" if "Required" in line else "Not Reqd")
            continue
        if line.startswith("Average of Annual"):
            block = ("ratio?",)
            continue
        parts = line.split()
        if parts and parts[0] == "Firms":
            ratio_cols = parts
            continue
        if not parts or not re.fullmatch(r"\d{4}(\d{2})?", parts[0]) or block is None:
            continue
        key = parts[0]
        vals = [_num(x) for x in parts[1:]]
        if block[0] == "ret" and len(key) == 6:
            d = date(int(key[:4]), int(key[4:]), 1)
            if d > last:
                continue
            tab = monthly.setdefault((block[1], block[2]), {c: [] for c in cols})
            for c, v in zip(cols, vals, strict=True):
                if not math.isnan(v):
                    tab[c].append((d, v))
        elif block[0] == "ratio" and len(key) == 4:
            if int(key) > LAST_RATIO_YEAR:
                continue
            tab = ratios.setdefault(block[1], {c: [] for c in ratio_cols})
            for c, v in zip(ratio_cols, vals, strict=True):
                if not math.isnan(v):
                    tab[c].append((date(int(key), 1, 1), v))
    return {"monthly": monthly, "annual_ratios": ratios}


def read_french_zip(path: Path, last: date = LAST) -> dict[str, dict[str, object]]:
    """{ISO2: parse_french_country(...)} for every country file in one French zip."""
    out: dict[str, dict[str, object]] = {}
    with zipfile.ZipFile(path) as z:
        for name in z.namelist():
            cc = FRENCH_FILES.get(name)
            if cc:
                out[cc] = parse_french_country(z.read(name).decode("latin-1"), last)
    return out


def dividend_yield(
    with_div: Sequence[tuple[date, float]], without_div: Sequence[tuple[date, float]]
) -> Series:
    """Trailing 12-month dividend yield (percent) of an index from its monthly returns (in
    percent) with and without dividends.

    P is the price index from the returns without dividends (P = 1 before the first month);
    the month's dividend is D(t) = (r_with - r_without) / 100 x P(t-1); the yield at the end of
    month t is the sum of the last 12 D over P(t). Months missing from either series break the
    chain (the 12-month window restarts)."""
    w = dict(with_div)
    out: Series = []
    p = 1.0
    divs: list[float] = []
    prev: date | None = None
    for d, rx in without_div:
        if d not in w:
            divs, prev = [], None
            continue
        if prev is not None and d != _next_month(prev):
            divs = []
        divs.append((w[d] - rx) / 100.0 * p)
        p *= 1.0 + rx / 100.0
        divs = divs[-12:]
        if len(divs) == 12 and p > 0:
            out.append((d, 100.0 * sum(divs) / p))
        prev = d
    return out


# ---------------------------------------------------------------- JST Macrohistory


def parse_jst(
    rows: Sequence[Sequence[str]], variables: Sequence[str]
) -> dict[str, dict[str, Series]]:
    """{variable: {iso3: annual series}} from the rows of the JST R6 sheet (header row first).

    Values 'NA' and blanks are dropped; years after LAST.year - 1 are dropped (none exist in R6,
    which ends in 2020)."""
    head = list(rows[0])
    iy, ii = head.index("year"), head.index("iso")
    idx = {v: head.index(v) for v in variables}
    out: dict[str, dict[str, Series]] = {v: {} for v in variables}
    for r in rows[1:]:
        if len(r) <= ii or not r[iy]:
            continue
        y = int(float(r[iy]))
        if y >= LAST.year:
            continue
        for v, j in idx.items():
            x = r[j].strip() if j < len(r) else ""
            if x in ("", "NA"):
                continue
            out[v].setdefault(r[ii], []).append((date(y, 1, 1), float(x)))
    for v in out:
        for k in out[v]:
            out[v][k].sort()
    return out


# ---------------------------------------------------------------- derived helpers


def real_fx(
    usd_per_unit: Sequence[tuple[date, float]],
    cpi_foreign: Sequence[tuple[date, float]],
    cpi_us: Sequence[tuple[date, float]],
) -> Series:
    """Log real exchange rate of a currency against USD: ln(S x P_f / P_us), monthly on the
    months all three have. Higher = the currency is dearer in real terms (a value signal would
    compare it with its own past, e.g. 5 years earlier; that choice belongs to a card)."""
    f, u = dict(cpi_foreign), dict(cpi_us)
    return [
        (d, math.log(s * f[d] / u[d]))
        for d, s in usd_per_unit
        if d in f and d in u and s > 0 and f[d] > 0 and u[d] > 0
    ]


def known_monthly(s: Sequence[tuple[date, float]], kind: str, last: date = LAST) -> Series:
    """The value of `s` as known at the end of each month: dated d, the latest observation whose
    `available(kind, ...)` is on or before the 1st of the month after d. Runs from the first
    month anything is known to the month of `last`.

    For AU/NZ CPI pass `quarter_ends(s)` with kind "cpi-quarterly": the BIS months of a quarter
    repeat the quarter's value (2025-07 already holds Q3 2025, published late October), so the
    monthly m+2 rule on the repeated months would look ahead."""
    obs = sorted(s)
    out: Series = []
    if not obs:
        return out
    d, end, i = obs[0][0].replace(day=1), last.replace(day=1), 0
    cur: float | None = None
    while d <= end:
        while i < len(obs) and available(kind, obs[i][0]) <= _next_month(d):
            cur = obs[i][1]
            i += 1
        if cur is not None:
            out.append((d, cur))
        d = _next_month(d)
    return out


def real_fx_known(
    usd_per_unit: Sequence[tuple[date, float]],
    cpi_foreign: Sequence[tuple[date, float]],
    cpi_us: Sequence[tuple[date, float]],
    quarterly_foreign: bool,
) -> Series:
    """`real_fx` with each CPI as known at the end of the spot's month (`known_monthly`): the
    foreign index by "cpi-quarterly" on its quarter values when `quarterly_foreign` (AU, NZ),
    else by "cpi-monthly"; the US index by "cpi-monthly". The spot is the month-end rate."""
    if quarterly_foreign:
        pf = known_monthly(quarter_ends(cpi_foreign), "cpi-quarterly")
    else:
        pf = known_monthly(cpi_foreign, "cpi-monthly")
    return real_fx(usd_per_unit, pf, known_monthly(cpi_us, "cpi-monthly"))


def available(kind: str, d: date) -> date:
    """First day the value dated d was public (conservative, see research/data-long-4.md)."""
    if kind == "cpi-monthly":  # CPI of month m: published 2-7 weeks after the end of m
        return _add_months(d, 2)
    if kind == "cpi-quarterly":  # AU/NZ: quarter starting d, published 3-5 weeks after the end
        return _add_months(d, 5)  # of the quarter; coded as quarter start + 5 months
    if kind == "policy-monthly":  # announced on the day: known at the end of the month
        return _next_month(d)
    if kind == "french-monthly":  # dividends and prices of month m: known at its end
        return _next_month(d)
    if kind == "french-annual":  # ratios of year t: accounting data of fiscal year t-1
        return date(d.year, 7, 1)
    if kind == "jst-annual":  # year t: known in the course of t+1
        return date(d.year + 1, 7, 1)
    raise ValueError(kind)
