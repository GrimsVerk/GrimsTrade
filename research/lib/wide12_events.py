"""Pure functions for the wide-12 gate W23 `custody-selling` (research/wide-12.md step 2).

Re-uses wide-11's z-score, price lookups, Driscoll-Kraay OLS, rank and null width; adds the
H.4.1 reader, the 4-week custody flow and the Monday-entry outcome.
"""

from __future__ import annotations

import math
import zipfile
from collections.abc import Mapping
from datetime import date, timedelta
from pathlib import Path
from typing import IO
from xml.etree import ElementTree as ET

from wide11_events import Closes

SERIES = "RESH4FG_N.WW"  # custody holdings, marketable Treasuries, Wednesday level
FLOW_DAYS = 28
ENTRY_DAYS = 5  # Monday after the Wednesday (release Thursday 16:30 New York)


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def read_series(stream: IO[bytes], name: str, last: date) -> dict[date, float]:
    """{date: value} of one series of a Fed DDP SDMX XML stream; dates after `last` and
    non-numeric values skipped."""
    out: dict[date, float] = {}
    for _, el in ET.iterparse(stream, events=("end",)):
        if _local(el.tag) != "Series":
            continue
        if el.attrib.get("SERIES_NAME") == name:
            for obs in el:
                if _local(obs.tag) != "Obs":
                    continue
                d = date.fromisoformat(obs.attrib["TIME_PERIOD"])
                try:
                    v = float(obs.attrib.get("OBS_VALUE", ""))
                except ValueError:
                    continue
                if d <= last and not math.isnan(v):
                    out[d] = v
            el.clear()
            return out
        el.clear()
    return out


def read_h41(path: Path, name: str, last: date) -> dict[date, float]:
    with zipfile.ZipFile(path) as z, z.open("H41_data.xml") as f:
        return read_series(f, name, last)


def flows(level: Mapping[date, float], days: int = FLOW_DAYS) -> dict[date, float]:
    """f(W) = ln(H(W) / H(W - days)); only where both levels exist and are positive."""
    out: dict[date, float] = {}
    for d, v in level.items():
        p = level.get(d - timedelta(days=days))
        if p is not None and p > 0 and v > 0:
            out[d] = math.log(v / p)
    return out


def outcome(px: Closes, w: date, exit_days: int, last: date) -> float:
    """ln(exit / entry): entry = close of the first bar dated >= W + 5, exit = close of the
    first bar dated >= W + exit_days (33 for the 4-week gate, 12 for the 1-week cell). NaN if
    a bar is missing, the exit bar is dated after W + exit_days + 7 or after `last`."""
    a = px.first_on_or_after(w + timedelta(days=ENTRY_DAYS))
    b = px.first_on_or_after(w + timedelta(days=exit_days))
    if a is None or b is None or b > last or b > w + timedelta(days=exit_days + 7) or b <= a:
        return math.nan
    return math.log(px.c[b] / px.c[a])


# ---- W24 `inflation-disagreement` (research/wide-12.md step 3) ----

# Placebo shifts in quarters: odd 7..45, both signs (40).
SHIFTS_W24: list[int] = [s * k for k in range(7, 46, 2) for s in (1, -1)]
ZQ_WINDOW = 40
ZQ_MIN = 20
_NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"


def _col_index(ref: str) -> int:
    """'B12' -> 1 (zero-based column)."""
    n = 0
    for ch in ref:
        if not ch.isalpha():
            break
        n = n * 26 + (ord(ch.upper()) - 64)
    return n - 1


def read_xlsx_sheet(path: Path | IO[bytes], sheet: str) -> list[list[str]]:
    """Cells of one worksheet as text rows (columns placed by their letter; blanks '')."""
    with zipfile.ZipFile(path) as z:
        wb = ET.fromstring(z.read("xl/workbook.xml"))
        rid = next(
            s.attrib[f"{{{_NS_R}}}id"]
            for s in wb.iter()
            if _local(s.tag) == "sheet" and s.attrib.get("name") == sheet
        )
        rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
        target = next(r.attrib["Target"] for r in rels if r.attrib.get("Id") == rid)
        target = target.lstrip("/")
        name = target if target.startswith("xl/") else "xl/" + target
        shared: list[str] = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")):
                shared.append("".join(t.text or "" for t in si.iter() if _local(t.tag) == "t"))
        root = ET.fromstring(z.read(name))
    out: list[list[str]] = []
    for row in root.iter():
        if _local(row.tag) != "row":
            continue
        cells: dict[int, str] = {}
        for c in row:
            if _local(c.tag) != "c":
                continue
            kind = c.attrib.get("t", "n")
            if kind == "inlineStr":
                text = "".join(t.text or "" for t in c.iter() if _local(t.tag) == "t")
            else:
                v = next((x.text or "" for x in c if _local(x.tag) == "v"), "")
                text = shared[int(v)] if kind == "s" and v else v
            cells[_col_index(c.attrib.get("r", "A"))] = text
        width = max(cells) + 1 if cells else 0
        out.append([cells.get(i, "") for i in range(width)])
    return out


def quarter_index(label: str) -> int:
    """'2010Q1' -> 2010 * 4 + 0."""
    y, q = label.strip().upper().split("Q")
    return int(y) * 4 + int(q) - 1


def quarter_column(rows: list[list[str]], column: str) -> dict[int, float]:
    """{quarter index: value} of `column` below the header row that holds `Survey_Date(T)`;
    non-numeric values ('#N/A', blank) skipped."""
    for i, r in enumerate(rows):
        if r and r[0].strip() == "Survey_Date(T)":
            j = r.index(column)
            out: dict[int, float] = {}
            for rr in rows[i + 1 :]:
                if not rr or len(rr) <= j or "Q" not in rr[0].upper():
                    continue
                try:
                    v = float(rr[j])
                except ValueError:
                    continue
                if not math.isnan(v):
                    out[quarter_index(rr[0])] = v
            return out
    raise KeyError(column)


def zscores_q(d: Mapping[int, float]) -> dict[int, float]:
    """z(q) = (D(q) - mean) / sd over surveys q-40 .. q-1 present, needing >= 20."""
    out: dict[int, float] = {}
    for q, v in d.items():
        w = [d[p] for p in range(q - ZQ_WINDOW, q) if p in d]
        if len(w) < ZQ_MIN:
            continue
        m = sum(w) / len(w)
        sd = math.sqrt(sum((x - m) ** 2 for x in w) / (len(w) - 1))
        if sd > 0:
            out[q] = (v - m) / sd
    return out


def entry_target(q: int) -> date:
    """First day of the third month of quarter q (after the survey's mid-quarter release)."""
    return date(q // 4, 3 * (q % 4) + 3, 1)


def outcome_q(px: Closes, q: int, last: date) -> float:
    """ln(exit / entry): entry = first bar >= entry_target(q), exit = first bar >=
    entry_target(q + 1); NaN if a bar is missing, more than 7 days late, or after `last`."""
    ta, tb = entry_target(q), entry_target(q + 1)
    a = px.first_on_or_after(ta)
    b = px.first_on_or_after(tb)
    if a is None or b is None or b > last or a > ta + timedelta(days=7):
        return math.nan
    if b > tb + timedelta(days=7) or b <= a:
        return math.nan
    return math.log(px.c[b] / px.c[a])
