"""Long non-equity return series: US Treasury bonds, G10 currencies, commodities (data-long-3).

Raw files come from `long_x_fetch.py` (keyless, cached under `<cache_root>/data-long-3/`, never
committed). This module only parses and derives; it does no network I/O, and every reader cuts
at `LAST` (2025-10-31, the last full month before the held-out year that starts 2025-11-11).
Method, validation and caveats: research/data-long-3.md.

Conventions
- A series is a list of (date, value) in date order. Monthly series are dated the first of the
  month they describe. A return dated d is earned over the period that ends at d.
- `available` gives the first day a value could have been known (publication lag); a monthly
  signal must use only values whose `available` date is on or before its decision day.

Bond returns (`bond_returns`): constant-maturity par bond rebuilt from a yield, the method of
Swinkels (2019, "Data: International government bond returns since 1947") and of Damodaran's
T-bond return: at each step buy a par bond of maturity M at yield y0 (coupon y0, semiannual
compounding), hold it for dt years, reprice it at y1 with maturity M - dt using the annuity
formula with a fractional number of periods, and add the coupon accrued over dt.
"""

from __future__ import annotations

import csv
import io
import math
import re
import xml.etree.ElementTree as ET
import zipfile
from collections.abc import Iterable, Sequence
from datetime import date, timedelta
from pathlib import Path

LAST = date(2025, 10, 31)  # last day any reader returns (held-out year starts 2025-11-11)
VINTAGE = "2025-11-10"
DEM_PER_EUR = 1.95583  # irrevocable conversion rate, 1999-01-01

Series = list[tuple[date, float]]


# ---------------------------------------------------------------- ALFRED / FRED csv


def parse_alfred(text: str, last: date = LAST) -> Series:
    """(date, value) from an ALFRED/FRED graph csv; '.' and blanks are missing and dropped."""
    rows = csv.reader(io.StringIO(text))
    header = next(rows)
    if len(header) != 2 or header[0] not in ("observation_date", "DATE"):
        raise ValueError(f"unexpected header {header}")
    out: Series = []
    for row in rows:
        if len(row) < 2 or not row[0]:
            continue
        d = date.fromisoformat(row[0])
        if d > last:
            break
        v = row[1].strip()
        if v in ("", "."):
            continue
        if out and d <= out[-1][0]:
            raise ValueError(f"disorder at {d}")
        out.append((d, float(v)))
    return out


def month_end(s: Sequence[tuple[date, float]]) -> Series:
    """Last observation of each calendar month, dated the first of that month."""
    out: dict[date, float] = {}
    for d, v in s:
        out[d.replace(day=1)] = v
    return sorted(out.items())


def monthly_join(*series: Sequence[tuple[date, float]]) -> list[tuple[date, tuple[float, ...]]]:
    """Months present in every series, with the values side by side."""
    maps = [dict(s) for s in series]
    common = set(maps[0]).intersection(*maps[1:])
    return [(d, tuple(m[d] for m in maps)) for d in sorted(common)]


def _next_month(d: date) -> date:
    return date(d.year + d.month // 12, d.month % 12 + 1, 1)


def consecutive(s: Sequence[tuple[date, float]]) -> Series:
    """The longest tail of a monthly series with no missing month (gaps break the chain)."""
    start = 0
    for i in range(1, len(s)):
        if s[i][0] != _next_month(s[i - 1][0]):
            start = i
    return list(s[start:])


# ---------------------------------------------------------------- bonds


def par_price(coupon: float, y: float, m: float) -> float:
    """Price per 1 face of a bond with annual coupon rate `coupon` (decimal, paid semiannually)
    and m years left, at yield y (semiannual compounding), annuity formula with fractional
    periods (accrued interest ignored: it is added separately by the caller)."""
    if m <= 0:
        return 1.0
    n = 2.0 * m
    v = (1.0 + y / 2.0) ** (-n)
    if abs(y) < 1e-12:
        return coupon * m + 1.0
    return coupon / y * (1.0 - v) + v


def bond_step(y0: float, y1: float, maturity: float, dt: float) -> float:
    """Total return over dt years of a par bond bought at y0 (percent), repriced at y1."""
    c = y0 / 100.0
    return par_price(c, y1 / 100.0, maturity - dt) - 1.0 + c * dt


def bond_step_duration(y0: float, y1: float, maturity: float, dt: float) -> float:
    """Second-order approximation: carry - modified duration x dy + convexity/2 x dy^2."""
    y = y0 / 100.0
    dy = (y1 - y0) / 100.0
    if abs(y) < 1e-9:
        dur, conv = maturity, maturity**2
    else:
        z = 1.0 + y / 2.0
        n = 2.0 * maturity
        dur = (1.0 - z ** (-n)) / y  # modified duration of a par bond
        # convexity of a par bond, numerically (central difference of par_price)
        h = 1e-4
        p_up, p_dn = par_price(y, y + h, maturity), par_price(y, y - h, maturity)
        conv = (p_up + p_dn - 2.0) / h**2
    return y * dt - dur * dy + 0.5 * conv * dy * dy


def bond_returns(
    yields: Sequence[tuple[date, float]], maturity: float, monthly: bool = False
) -> Series:
    """Returns of a constant-maturity par bond from a yield series (percent).

    Daily: dt = calendar days between observations / 365 (a missing day simply lengthens the
    next step). Monthly (yields already month-end, dated the first of the month): dt = 1/12.
    The return dated d runs from the previous observation to d."""
    out: Series = []
    for (d0, y0), (d1, y1) in zip(yields, yields[1:], strict=False):
        dt = 1.0 / 12.0 if monthly else (d1 - d0).days / 365.0
        if monthly and d1 != _next_month(d0):
            raise ValueError(f"monthly gap {d0} -> {d1}")
        out.append((d1, bond_step(y0, y1, maturity, dt)))
    return out


# ---------------------------------------------------------------- currencies

# FRED H.10 id -> (currency, True if quoted as foreign units per USD)
FX_QUOTE: dict[str, tuple[str, bool]] = {
    "DEXJPUS": ("JPY", True),
    "DEXUSUK": ("GBP", False),
    "DEXSZUS": ("CHF", True),
    "DEXCAUS": ("CAD", True),
    "DEXGEUS": ("DEM", True),
    "DEXUSEU": ("EUR", False),
    "DEXUSAL": ("AUD", False),
    "DEXUSNZ": ("NZD", False),
    "DEXSDUS": ("SEK", True),
    "DEXNOUS": ("NOK", True),
}


def usd_per_unit(s: Sequence[tuple[date, float]], per_usd: bool) -> Series:
    """USD value of one foreign unit (so a rise = the foreign currency gains)."""
    return [(d, 1.0 / v if per_usd else v) for d, v in s if v > 0]


def splice_eur(dem_usd_per_unit: Series, eur_usd_per_unit: Series) -> Series:
    """One euro line: DEM before the first EUR quote, converted at 1.95583 DEM per EUR."""
    first = eur_usd_per_unit[0][0]
    pre = [(d, v * DEM_PER_EUR) for d, v in dem_usd_per_unit if d < first]
    return pre + list(eur_usd_per_unit)


def simple_returns(s: Sequence[tuple[date, float]]) -> Series:
    return [(d1, v1 / v0 - 1.0) for (_, v0), (d1, v1) in zip(s, s[1:], strict=False)]


def fx_excess_monthly(
    spot_me: Sequence[tuple[date, float]],
    i_foreign: Sequence[tuple[date, float]],
    i_us: Sequence[tuple[date, float]],
) -> list[tuple[date, float, float]]:
    """(month, spot return, carry-inclusive excess return) of holding the foreign currency for
    one month funded in USD. Spot is month-end USD per unit; rates are percent a year, monthly
    averages dated the first of their month. The return dated m runs from the end of m-1 to the
    end of m and earns the rate differential of month m-1 (the latest monthly average that
    existed when the position was opened; the true deposit was locked at end-m-1)."""
    fi, ui = dict(i_foreign), dict(i_us)
    out: list[tuple[date, float, float]] = []
    for (m0, s0), (m1, s1) in zip(spot_me, spot_me[1:], strict=False):
        if m1 != _next_month(m0) or m0 not in fi or m0 not in ui:
            continue
        spot = s1 / s0 - 1.0
        carry = (1.0 + fi[m0] / 1200.0) / (1.0 + ui[m0] / 1200.0)
        out.append((m1, spot, (1.0 + spot) * carry - 1.0))
    return out


def first_available(*series: Sequence[tuple[date, float]]) -> Series:
    """Merge rate series by priority: for each date the first series that has it."""
    out: dict[date, float] = {}
    for s in reversed(series):
        out.update(dict(s))
    return sorted(out.items())


# ---------------------------------------------------------------- publication timing


def available(series_kind: str, d: date) -> date:
    """First day the value dated d was public (conservative, see the doc's timing table)."""
    if series_kind == "h15-daily":  # yields for day d: H.15 posts them the next business day
        return _bday(d, 1)
    if series_kind == "h10-daily":  # noon NY rates: H.10 weekly release, the following Monday
        return d + timedelta(days=7 - d.weekday())
    if series_kind == "h15-monthly":  # monthly average of month d: first business day after
        return _bday(_next_month(d) - timedelta(days=1), 1)
    if series_kind == "oecd-monthly":  # OECD MEI: published within about 2 months
        return _next_month(_next_month(_next_month(d)))
    if series_kind == "pink-sheet":  # World Bank: 2nd-4th business day of the next month
        return _bday(_next_month(d) - timedelta(days=1), 4)
    if series_kind == "ppi":  # BLS PPI: mid next month, revised 4 months later
        return _next_month(d) + timedelta(days=16)
    raise ValueError(series_kind)


def _bday(d: date, n: int) -> date:
    while n:
        d += timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


# ---------------------------------------------------------------- World Bank Pink Sheet

_NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
_REL = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"


def _col(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref)
    assert letters
    n = 0
    for ch in letters.group(0):
        n = n * 26 + ord(ch) - 64
    return n - 1


def xlsx_rows(path: Path, sheet: str) -> list[list[str]]:
    """Cell text of one sheet of an .xlsx (stdlib only: zip + xml). Numbers stay strings."""
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            root = ET.fromstring(z.read("xl/sharedStrings.xml"))
            for si in root.findall("m:si", _NS):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{_NS['m']}}}t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rels}
        rid = next(s.get(_REL) for s in wb.iter(f"{{{_NS['m']}}}sheet") if s.get("name") == sheet)
        tgt = str(target[rid]).lstrip("/")
        name = tgt if tgt.startswith("xl/") else "xl/" + tgt
        root = ET.fromstring(z.read(name))
    rows: list[list[str]] = []
    for r in root.iter(f"{{{_NS['m']}}}row"):
        cells: dict[int, str] = {}
        for c in r.findall("m:c", _NS):
            v = c.find("m:v", _NS)
            if c.get("t") == "inlineStr":
                text = "".join(t.text or "" for t in c.iter(f"{{{_NS['m']}}}t"))
            elif v is None or v.text is None:
                continue
            elif c.get("t") == "s":
                text = shared[int(v.text)]
            else:
                text = v.text
            cells[_col(str(c.get("r")))] = text
        rows.append([cells.get(i, "") for i in range(max(cells) + 1)] if cells else [])
    return rows


_MONTH = re.compile(r"^(\d{4})M(\d{2})$")


def parse_pink(rows: Sequence[Sequence[str]], last: date = LAST) -> dict[str, Series]:
    """Monthly prices by commodity name from the 'Monthly Prices' sheet rows.

    Layout: a header row whose later cells are commodity names, a units row below it, then one
    row per month with a first cell like '1960M01'. Missing cells ('', '..', '…') are dropped."""
    head = next(i for i, r in enumerate(rows) if len(r) > 3 and _MONTH.match(_first_month(rows)))
    del head
    first = next(i for i, r in enumerate(rows) if r and _MONTH.match(r[0].strip()))
    names_row = next(
        i for i in range(first - 1, -1, -1) if sum(1 for x in rows[i][1:] if x.strip()) > 3
    )
    # the units row sits directly above the first month; names are the row above the units
    if names_row == first - 1 and _looks_like_units(rows[names_row]):
        names_row -= 1
    names = [x.strip() for x in rows[names_row]]
    out: dict[str, Series] = {n: [] for n in names[1:] if n}
    for r in rows[first:]:
        if not r or not _MONTH.match(r[0].strip()):
            continue
        y, m = _MONTH.match(r[0].strip()).groups()  # type: ignore[union-attr]
        d = date(int(y), int(m), 1)
        if d > last:
            break
        for j, n in enumerate(names):
            if j == 0 or not n or j >= len(r):
                continue
            x = r[j].strip()
            try:
                v = float(x)
            except ValueError:
                continue
            if math.isfinite(v):
                out[n].append((d, v))
    return {k: v for k, v in out.items() if v}


def _first_month(rows: Sequence[Sequence[str]]) -> str:
    for r in rows:
        if r and _MONTH.match(r[0].strip()):
            return r[0].strip()
    raise ValueError("no month rows")


def _looks_like_units(r: Sequence[str]) -> bool:
    return sum(1 for x in r if x.strip().startswith("($")) >= 2


# ---------------------------------------------------------------- Yahoo chart json


def yahoo_adjclose(obj: dict, last: date = LAST) -> Series:  # type: ignore[type-arg]
    """(UTC date, adjusted close) from a Yahoo v8 chart response; meta is ignored."""
    from datetime import UTC, datetime

    res = obj["chart"]["result"][0]
    ts = res["timestamp"]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    out: Series = []
    for t, a in zip(ts, adj, strict=True):
        d = datetime.fromtimestamp(t, UTC).date()
        if a is None or d > last:
            continue
        out.append((d, float(a)))
    return out


# ---------------------------------------------------------------- statistics for validation


def stats_pair(a: Sequence[float], b: Sequence[float], per_year: int) -> dict[str, float]:
    """Correlation, tracking error a year, mean gap a year (a - b), both means a year."""
    n = len(a)
    if n != len(b) or n < 3:
        raise ValueError("need equal series of 3+")
    ma, mb = sum(a) / n, sum(b) / n
    va = sum((x - ma) ** 2 for x in a) / (n - 1)
    vb = sum((x - mb) ** 2 for x in b) / (n - 1)
    cov = sum((x - ma) * (y - mb) for x, y in zip(a, b, strict=True)) / (n - 1)
    gaps = [x - y for x, y in zip(a, b, strict=True)]
    mg = sum(gaps) / n
    vg = sum((g - mg) ** 2 for g in gaps) / (n - 1)
    return {
        "n": float(n),
        "corr": cov / math.sqrt(va * vb),
        "te": math.sqrt(vg * per_year),
        "gap": mg * per_year,
        "mean_a": ma * per_year,
        "mean_b": mb * per_year,
        "vol_a": math.sqrt(va * per_year),
        "vol_b": math.sqrt(vb * per_year),
    }


def max_drawdown(returns: Iterable[float]) -> float:
    peak = level = 1.0
    worst = 0.0
    for r in returns:
        level *= 1.0 + r
        peak = max(peak, level)
        worst = max(worst, 1.0 - level / peak)
    return worst
