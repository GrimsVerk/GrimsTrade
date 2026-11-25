"""Loaders and episode counts for the keyless sources of research run data-wide-2.

`research/data-wide-2.md` ranks keyless public data sets by how many independent market-years
and falls of 25% or more they add to what the project has already scored. This module:

- parses each cached source into monthly level series (`Monthly`): Yale ICF London IMM
  (security-level monthly prices 1869-1929, built into per-country indices by a chained median
  of month-to-month log changes), Yale St Petersburg / NYSE indices, Norges Bank HMS (stocks,
  bond yields, exchange rates), SNB historical capital-market tables, AQR "Commodities for the
  Long Run", and the Bank of England "millennium" monthly sheet in its long CSV form;
- counts market-years and falls (`falls`, `count_new`) against the coverage already scored
  (`SEEN`, written from the research records before any count was run).

Parsers take text or rows, so the tests run offline on small literal samples. Raw files are
untrusted downloads in the git-ignored cache (`<cache_root>/data-wide-2/...`; xlsx files are
read with the stdlib `read_xlsx_rows`, no macro or formula is evaluated). Run with `python -I`.
Nothing here computes a strategy or a return statistic of any rule.
"""

from __future__ import annotations

import csv
import io
import json
import math
import re
import statistics
import zipfile
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
LAST_YM = 2025 * 12 + 9  # 2025-10: nothing later is kept (held-out year starts 2025-11-11)


def cache_root() -> Path:
    cfg = ROOT / "research" / "macro.local.json"
    return Path(json.loads(cfg.read_text())["cache_root"]).expanduser()


def ym(year: int, month: int) -> int:
    """Months since year 0 (January = 0)."""
    return year * 12 + month - 1


def ym_str(m: int) -> str:
    return f"{m // 12:04d}-{m % 12 + 1:02d}"


@dataclass
class Monthly:
    """One monthly level series. `asset` is stock, bond, fx or commodity; `market` an ISO3
    country code (or a commodity name); `level` is a price-like level (bond yields are turned
    into a perpetuity price 1/y, exchange rates into USD or GBP per unit of the local
    currency), so a fall of the level is a loss for a holder."""

    name: str
    asset: str
    market: str
    months: list[int]
    level: list[float]
    timing: str = "unknown"  # month-end, average, mixed, unknown
    note: str = ""
    extra: dict[str, int] = field(default_factory=dict)

    def cut(self, last: int = LAST_YM) -> Monthly:
        keep = [i for i, m in enumerate(self.months) if m <= last]
        self.months = [self.months[i] for i in keep]
        self.level = [self.level[i] for i in keep]
        return self


def from_points(
    name: str, asset: str, market: str, pts: Iterable[tuple[int, float]], **kw: str
) -> Monthly:
    clean = sorted({m: v for m, v in pts if v is not None and math.isfinite(v) and v > 0}.items())
    return Monthly(name, asset, market, [m for m, _ in clean], [v for _, v in clean], **kw).cut()


def chain_returns(pts: Iterable[tuple[int, float]], base: float = 100.0) -> list[tuple[int, float]]:
    """Level from simple monthly returns; the first return's month gets base * (1 + r)."""
    out, lvl = [], base
    for m, r in sorted(pts):
        lvl *= 1.0 + r
        out.append((m, lvl))
    return out


# ---------------------------------------------------------------- generic readers


def _num(x: object) -> float | None:
    if x is None:
        return None
    if isinstance(x, int | float):
        return float(x)
    s = str(x).strip().replace("−", "-")
    if s in ("", ".", "-", "..", "NA", "n.a."):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def read_xlsx_rows(path: Path, sheet: str | int = 0) -> list[list[object]]:
    """Cell values of one worksheet of an .xlsx (stdlib only; formulas give their cached
    value, which may be absent). Rows keep their column positions (A = index 0)."""
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rel_ns = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    with zipfile.ZipFile(path) as z:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", ns):
                shared.append("".join(t.text or "" for t in si.iter(f"{{{ns['m']}}}t")))
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        sheets = wb.findall("m:sheets/m:sheet", ns)
        pick = (
            sheets[sheet]
            if isinstance(sheet, int)
            else next(s for s in sheets if s.get("name") == sheet)
        )
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = next(r.get("Target") for r in rels if r.get("Id") == pick.get(rel_ns))
        target = str(target).lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        root = ET.fromstring(z.read(target))
    rows: list[list[object]] = []
    for row in root.iter(f"{{{ns['m']}}}row"):
        vals: dict[int, object] = {}
        for c in row.findall("m:c", ns):
            ref = re.match(r"([A-Z]+)", c.get("r") or "")
            col = 0
            for ch in ref.group(1) if ref else "":
                col = col * 26 + ord(ch) - 64
            v = c.find("m:v", ns)
            t = c.get("t")
            if t == "s" and v is not None and v.text is not None:
                vals[col - 1] = shared[int(v.text)]
            elif t == "inlineStr":
                vals[col - 1] = "".join(x.text or "" for x in c.iter(f"{{{ns['m']}}}t"))
            elif v is not None and v.text is not None:
                vals[col - 1] = _num(v.text) if t != "str" else v.text
        rows.append([vals.get(i) for i in range(max(vals) + 1)] if vals else [])
    return rows


def excel_serial(x: float) -> date:
    return date(1899, 12, 30) + timedelta(days=int(x))


# ---------------------------------------------------------------- Yale ICF


def parse_imm_rows(
    rows: Iterable[dict[str, str]],
    kind: str = "Government Bond",
    currency: str | None = "GBP",
    min_pairs: int = 1,
) -> list[Monthly]:
    """Per-country monthly index from the IMM clean file (`Totaldata.csv`): for each security of
    `kind`, the log change of `PriceMonthLate` between consecutive calendar months; the country
    index chains the median change over its securities (months with no pair carry no point).
    Only securities quoted in `currency` (default sterling, 96% of the government-bond rows), so
    a country index is what a London holder earned in price, not a mix of currencies. A month
    needs at least `min_pairs` securities with a price in it and the month before.
    `extra` holds the number of securities and of month pairs."""
    last: dict[str, tuple[int, float]] = {}
    moves: dict[str, dict[int, list[float]]] = defaultdict(lambda: defaultdict(list))
    secs: dict[str, set[str]] = defaultdict(set)
    for r in rows:
        if r.get("Type") != kind or (currency is not None and r.get("Currency") != currency):
            continue
        p = _num(r.get("PriceMonthLate"))
        if p is None or p <= 0:
            continue
        m = ym(int(r["Year"]), int(r["Month"]))
        sid, iso = r["NewID"], r["ISO"] or "UNK"
        prev = last.get(sid)
        if prev is not None and prev[0] == m - 1:
            moves[iso][m].append(math.log(p / prev[1]))
        last[sid] = (m, p)
        secs[iso].add(sid)
    out = []
    for iso, by_m in moves.items():
        pts, lvl = [], 100.0
        for m in sorted(by_m):
            if len(by_m[m]) < min_pairs:
                continue
            lvl *= math.exp(statistics.median(by_m[m]))
            pts.append((m, lvl))
        s = from_points(
            f"IMM {kind} {iso}", "bond" if "Bond" in kind else "stock", iso, pts, timing="month-end"
        )
        s.extra = {"securities": len(secs[iso]), "pairs": sum(len(v) for v in by_m.values())}
        out.append(s)
    return out


def parse_yale_nyse(text: str, column: str = "2020 Index Returns") -> Monthly:
    """Goetzmann-Ibbotson-Peng NYSE price-weighted index 1815-1925 (a CSV file named .xls)."""
    names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    mon = {m: i for i, m in enumerate(names, 1)}
    pts = []
    for r in csv.DictReader(io.StringIO(text)):
        lab = r[""]
        mm, yy = lab.split("-")
        r_ = _num(r.get(column))
        if r_ is not None:
            pts.append((ym(int(yy), mon[mm]), r_))
    return from_points(
        "Yale NYSE 1815-1925", "stock", "USA", chain_returns(pts), timing="month-end"
    )


def parse_spse_nyse(rows: Sequence[Sequence[object]]) -> list[Monthly]:
    """Yale `SPSENYSE18651917ind.xls`: month (Excel serial shifted by +100 years), NYSE, SPSE
    price-weighted dollar capital-appreciation indices, January 1865 = 100."""
    nyse, spse = [], []
    for r in rows[1:]:
        if not r or _num(r[0]) is None:
            continue
        d = excel_serial(float(r[0]))  # type: ignore[arg-type]
        m = ym(d.year - 100, d.month)
        a, b = _num(r[1]), _num(r[2])
        if a is not None:
            nyse.append((m, a))
        if b is not None:
            spse.append((m, b))
    return [
        from_points("Yale NYSE (SPSE comparison, USD)", "stock", "USA", nyse, timing="month-end"),
        from_points("Yale St Petersburg SE (USD)", "stock", "RUS", spse, timing="month-end"),
    ]


# ---------------------------------------------------------------- central banks

_YM = re.compile(r"^\s*(1[6-9]\d\d|20\d\d)\s*[: ]\s*(\d{1,2})\s*$")


def _ym_label(x: object) -> int | None:
    if isinstance(x, int | float) and 1e4 < x < 1e5:  # Excel serial date
        d = excel_serial(float(x))
        return ym(d.year, d.month)
    m = _YM.match(str(x)) if x is not None else None
    if m:
        return ym(int(m.group(1)), int(m.group(2)))
    if x is not None and re.match(r"^\d{4}-\d{2}-\d{2}", str(x)):
        return ym(int(str(x)[:4]), int(str(x)[5:7]))
    return None


def parse_labelled_columns(
    rows: Sequence[Sequence[object]], col: int, *, label_col: int = 0
) -> list[tuple[int, float]]:
    """(month, value) pairs from a sheet whose `label_col` holds 'YYYY MM', 'YYYY:MM', an ISO
    date or an Excel serial, and column `col` the value ('.' and blanks are missing)."""
    out = []
    for r in rows:
        if len(r) <= col:
            continue
        m = _ym_label(r[label_col])
        v = _num(r[col])
        if m is not None and v is not None:
            out.append((m, v))
    return out


def find_col(rows: Sequence[Sequence[object]], header: str, *, max_rows: int = 40) -> int:
    for r in rows[:max_rows]:
        for i, c in enumerate(r):
            if c is not None and str(c).strip() == header:
                return i
    raise KeyError(header)


def yields_to_price(pts: Iterable[tuple[int, float]]) -> list[tuple[int, float]]:
    """Perpetuity price proxy 100 / yield (yield in percent)."""
    return [(m, 100.0 / y) for m, y in pts if y > 0]


# ---------------------------------------------------------------- AQR, BoE


def parse_aqr_comlr(rows: Sequence[Sequence[object]], col: int = 1) -> Monthly:
    """AQR 'Commodities for the Long Run' index-level file: date, then monthly returns; column
    1 = excess return of the equal-weight commodity futures portfolio."""
    pts = []
    for r in rows:
        if len(r) <= col or r[0] is None:
            continue
        s = str(r[0])
        x = _num(r[col])
        if re.match(r"^\d{4}-\d{2}-\d{2}", s) and x is not None:
            pts.append((ym(int(s[:4]), int(s[5:7])), x))
        elif isinstance(r[0], int | float) and x is not None and 0 < r[0] < 1e5:
            d = excel_serial(float(r[0]))
            pts.append((ym(d.year, d.month), x))
    return from_points(
        "AQR COMLR equal-weight excess",
        "commodity",
        "EW-futures",
        chain_returns(pts),
        timing="month-end",
    )


def parse_boe_long_csv(
    text: str, prefix: str, asset: str, market: str = "GBR", *, yield_: bool = False
) -> Monthly:
    """Bank of England 'A millennium of macroeconomic data' monthly sheet in the long CSV form
    (period, year, month, variable_id, ..., value)."""
    pts = []
    name = prefix
    for r in csv.DictReader(io.StringIO(text)):
        if r["variable_id"].startswith(prefix):
            v = _num(r["value"])
            if v is not None:
                pts.append((ym(int(r["year"]), int(r["month"])), v))
                name = r["variable"]
    if yield_:
        pts = yields_to_price(pts)
    return from_points(f"BoE {name}", asset, market, pts)


def splice(a: Monthly, b: Monthly, name: str) -> Monthly:
    """a, then b rescaled to a's level at a's last month (b must hold that month, else a)."""
    last = a.months[-1]
    if last not in b.months:
        return a
    k = a.level[-1] / b.level[b.months.index(last)]
    pts = list(zip(a.months, a.level, strict=True))
    pts += [(m, v * k) for m, v in zip(b.months, b.level, strict=True) if m > last]
    return from_points(name, a.asset, a.market, pts, timing=a.timing)


# ---------------------------------------------------------------- counting


def falls(
    months: Sequence[int], level: Sequence[float], threshold: float = 0.25
) -> list[tuple[int, int, float]]:
    """Peak-to-trough falls of at least `threshold`, one per episode: an episode starts when
    the level is `threshold` below its running peak and ends when the level regains that
    peak; it is reported as (peak month, trough month, depth)."""
    out: list[tuple[int, int, float]] = []
    peak_i, trough_i, in_fall = 0, 0, False
    for i, x in enumerate(level):
        if x >= level[peak_i]:
            if in_fall:
                out.append((months[peak_i], months[trough_i], 1 - level[trough_i] / level[peak_i]))
                in_fall = False
            peak_i = trough_i = i
            continue
        if x < level[trough_i]:
            trough_i = i
        if 1 - level[trough_i] / level[peak_i] >= threshold:
            in_fall = True
    if in_fall:
        out.append((months[peak_i], months[trough_i], 1 - level[trough_i] / level[peak_i]))
    return out


def years_covered(months: Iterable[int], min_months: int = 6) -> set[int]:
    c: dict[int, int] = defaultdict(int)
    for m in months:
        c[m // 12] += 1
    return {y for y, n in c.items() if n >= min_months}


# Coverage already scored or cached for scoring, by (asset, market): inclusive year ranges.
# Written from the research records (e4-indep-1, pooled-1, pooled-2, data-long-1..4) before
# any count of this lane was run. A market not listed has no scored coverage.
_FRENCH21 = "AUS AUT BEL CAN DNK FIN FRA DEU HKG IRL ITA JPN MYS NLD NZL NOR SGP ESP SWE CHE GBR"
_YAHOO = {
    "NLD": 1992, "AUS": 1984, "AUT": 1992, "BEL": 1991, "IND": 1997, "BRA": 1993, "FRA": 1990,
    "GBR": 1984, "ITA": 1997, "DEU": 1987, "CAN": 1979, "HKG": 1986, "ESP": 1993, "IDN": 1990,
    "MYS": 1993, "KOR": 1996, "MEX": 1991, "JPN": 1965, "NZL": 2003, "CHE": 1990, "SGP": 1987,
    "ISR": 1992, "TWN": 1997,
}  # fmt: skip
SEEN: dict[tuple[str, str], list[tuple[int, int]]] = defaultdict(list)
SEEN[("stock", "USA")] = [(1871, 2025)]
SEEN[("stock", "GBR")] = [(1867, 1914), (1919, 1924)]
SEEN[("stock", "DEU")] = [(1870, 1913)]
SEEN[("stock", "FRA")] = [(1899, 1914), (1919, 1927)]
for _c in _FRENCH21.split():
    SEEN[("stock", _c)].append((1975, 2025))
for _c, _y in _YAHOO.items():
    SEEN[("stock", _c)].append((_y, 2025))
# JST R6 annual equity, scored by insure-1870-1 (per-country start, and a full-span run to 2020)
_JST = {
    "AUS": 1871, "BEL": 1871, "CHE": 1901, "DEU": 1871, "DNK": 1876, "ESP": 1901, "FIN": 1897,
    "FRA": 1871, "GBR": 1872, "ITA": 1886, "JPN": 1887, "NLD": 1901, "NOR": 1882, "PRT": 1881,
    "SWE": 1872, "USA": 1873,
}  # fmt: skip
for _c, _y in _JST.items():
    SEEN[("stock", _c)].append((_y, 2020))
SEEN[("bond", "USA")] = [(1871, 2025)]
for _c, _y in {"AUS": 1969, "CAN": 1955, "CHE": 1955, "DEU": 1956, "GBR": 1960, "JPN": 1989,
               "NOR": 1985, "NZL": 1970, "SWE": 1986}.items():  # fmt: skip
    SEEN[("bond", _c)].append((_y, 2025))
for _c in ["JPN", "GBR", "CHE", "CAN", "DEU", "AUS", "NZL", "SWE", "NOR", "EMU"]:
    SEEN[("fx", _c)].append((1971, 2025))
SEEN[("commodity", "EW-futures")] = [(1913, 2025)]  # PPI commodity groups 1913-, Pink Sheet 1960-


def seen(asset: str, market: str, year: int) -> bool:
    return any(a <= year <= b for a, b in SEEN.get((asset, market), []))


def seen_calendar(asset: str, year: int) -> bool:
    """Is `year` covered by any scored series of this asset class?"""
    return any(a <= year <= b for (cls, _), rs in SEEN.items() if cls == asset for a, b in rs)


@dataclass(frozen=True)
class Count:
    name: str
    asset: str
    market: str
    first: str
    last: str
    months: int
    new_years: int
    new_calendar_years: int
    falls_new: int
    falls_all: int
    new_pre1927: int  # new years before 1927: e4-indep-1's "no time overlap with the 41" window
    falls_pre1927: int


def count_new(s: Monthly, threshold: float = 0.25) -> Count:
    yrs = years_covered(s.months)
    new = {y for y in yrs if not seen(s.asset, s.market, y)}
    cal = {y for y in new if not seen_calendar(s.asset, y)}
    fl = falls(s.months, s.level, threshold)
    fl_new = [f for f in fl if f[1] // 12 in new]
    return Count(
        s.name, s.asset, s.market,
        ym_str(s.months[0]) if s.months else "-", ym_str(s.months[-1]) if s.months else "-",
        len(s.months), len(new), len(cal), len(fl_new), len(fl),
        sum(1 for y in new if y < 1927), sum(1 for f in fl_new if f[1] // 12 < 1927),
    )  # fmt: skip
