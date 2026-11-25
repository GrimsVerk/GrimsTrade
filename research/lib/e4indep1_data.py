"""e4-indep-1 data: monthly stock levels never used for `e4` (card research/cards/e4-indep-1.md).

Pure parsing plus one polite fetch; no rule, no statistic. Raw files stay in the local cache
(`<cache_root>/e4-indep-1/`), never in git.

- NBER Macrohistory, chapter XI (securities markets), rectangular files
  `https://data.nber.org/databases/macrohistory/rectdata/11/<id>.dat`, lines "YYYY MM value"
  with "." for a missing month. Keyless; the NBER asks for attribution.
- Shiller `ie_data.xls` (already cached by earlier lanes; `wide21_events.parse_shiller`).
- Kenneth R. French, international country files (cached by data-long-4): column `Mkt`,
  value-weight USD return with dividends, in percent.

A *segment* is a run of consecutive calendar months with a level each. Returns are labelled by
the month their end level belongs to, so the return of month m runs from the level of m-1 to
that of m.
"""

from __future__ import annotations

import math
import subprocess
import time
import zipfile
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

NBER_URL = "https://data.nber.org/databases/macrohistory/rectdata/11/{sid}.dat"
NBER_DOC = "https://data.nber.org/databases/macrohistory/rectdata/11/docs/{sid}.txt"
NBER_IDS = ("m11025a", "m11012a", "m11012b", "m11012c", "m11023a", "m11023b", "m11024")
UA = "research-script/1.0 (keyless public data)"
SHILLER = "shiller/2026-11-12/ie_data.xls"
FRENCH_INTL = "data-long-4/french/2026-11-24/F-F_International_Countries.zip"
CUT = date(1927, 6, 1)  # last return month of the pre-1927 pool (the 41's first scored: 1927-07)
LAST = date(2025, 10, 1)  # last return month of anything (held-out year from 2025-11-11)


def mi(y: int, m: int) -> int:
    """Month index y * 12 + m - 1."""
    return y * 12 + m - 1


def month_of(k: int) -> date:
    return date(k // 12, k % 12 + 1, 1)


def parse_nber(text: str) -> dict[int, float]:
    """{month index: level} from an NBER rectdata file; "." and non-positive values skipped."""
    out: dict[int, float] = {}
    for line in text.splitlines():
        p = line.split()
        if len(p) < 3 or not p[0].isdigit() or not p[1].isdigit():
            continue
        y, m = int(p[0]), int(p[1])
        if not 1 <= m <= 12:
            continue
        try:
            v = float(p[2])
        except ValueError:
            continue
        if math.isfinite(v) and v > 0:
            out[mi(y, m)] = v
    return out


def segments(
    levels: Mapping[int, float], lo: int | None = None, hi: int | None = None
) -> list[list[tuple[int, float]]]:
    """Runs of consecutive months (each [(month index, level), ...]) within [lo, hi]."""
    ks = sorted(k for k in levels if (lo is None or k >= lo) and (hi is None or k <= hi))
    out: list[list[tuple[int, float]]] = []
    for k in ks:
        if out and out[-1][-1][0] == k - 1:
            out[-1].append((k, levels[k]))
        else:
            out.append([(k, levels[k])])
    return out


@dataclass
class Seg:
    """One segment's monthly returns: r[i] is the return of month months[i]."""

    name: str
    months: list[date]
    r: list[float]
    gap: int


def seg_returns(name: str, seg: Sequence[tuple[int, float]], gap: int) -> Seg:
    ks = [k for k, _ in seg]
    lv = [v for _, v in seg]
    r = [lv[i + 1] / lv[i] - 1.0 for i in range(len(lv) - 1)]
    return Seg(name, [month_of(k) for k in ks[1:]], r, gap)


def returns_segments(
    name: str, rets: Mapping[int, float], gap: int, lo: int | None = None, hi: int | None = None
) -> list[Seg]:
    """Segments of consecutive monthly returns {month index: return} (already returns)."""
    out = []
    for run in segments({k: 1.0 + v for k, v in rets.items()}, lo, hi):
        out.append(Seg(name, [month_of(k) for k, _ in run], [v - 1.0 for _, v in run], gap))
    return out


def parse_french_mkt(text: str, last: date = LAST) -> dict[int, float]:
    """{month index: Mkt return (decimal)} from the first monthly block of a French country file;
    -99.99 is missing; months after `last` are left out."""
    out: dict[int, float] = {}
    started = False
    cut = mi(last.year, last.month)
    for line in text.splitlines():
        p = line.split()
        if p and len(p[0]) == 6 and p[0].isdigit():
            started = True
            k = mi(int(p[0][:4]), int(p[0][4:]))
            v = float(p[1])
            if v > -99.0 and k <= cut:
                out[k] = v / 100.0
        elif started:
            break  # the monthly block ends at the first non-data line
    return out


def french_country(root: Path, member: str, last: date = LAST) -> dict[int, float]:
    with zipfile.ZipFile(root / FRENCH_INTL) as z:
        return parse_french_mkt(z.read(member).decode("latin-1"), last)


def shiller_prices(root: Path, cut: date) -> dict[int, float]:
    """{month index: P} from Shiller's file (monthly average of the composite), through `cut`."""
    import wide21_events as ev
    import xlrd  # type: ignore[import-untyped]

    sheet = xlrd.open_workbook(str(root / SHILLER)).sheet_by_name("Data")
    sh = ev.parse_shiller((sheet.row_values(i) for i in range(sheet.nrows)), cut)
    return {k: p for k, (p, _) in sh.items()}


def shiller_total(root: Path, cut: date) -> dict[int, float]:
    """{month index: total-return level}: P(m) + D(m) / 12 reinvested (Shiller's convention)."""
    import wide21_events as ev
    import xlrd

    sheet = xlrd.open_workbook(str(root / SHILLER)).sheet_by_name("Data")
    sh = ev.parse_shiller((sheet.row_values(i) for i in range(sheet.nrows)), cut)
    ks = sorted(sh)
    out = {ks[0]: 1.0}
    for a, b in zip(ks, ks[1:], strict=False):
        pa, pb, db = sh[a][0], sh[b][0], sh[b][1]
        out[b] = out[a] * (pb + db / 12.0) / pa
    return out


def nber(root: Path, sid: str) -> dict[int, float]:
    return parse_nber((root / "e4-indep-1" / "nber" / f"{sid}.dat").read_text(encoding="latin-1"))


def fetch(root: Path, ids: Iterable[str] = NBER_IDS) -> None:
    """Fetch the NBER files once (2 s between calls); existing files are kept."""
    d = root / "e4-indep-1" / "nber"
    d.mkdir(parents=True, exist_ok=True)
    for sid in ids:
        for url, suf in ((NBER_URL, ".dat"), (NBER_DOC, ".txt")):
            f = d / f"{sid}{suf}"
            if f.exists():
                continue
            out = subprocess.run(
                ["curl", "-sS", "-f", "-m", "60", "-A", UA, url.format(sid=sid)],
                check=True,
                capture_output=True,
            )
            f.write_bytes(out.stdout)
            time.sleep(2)
