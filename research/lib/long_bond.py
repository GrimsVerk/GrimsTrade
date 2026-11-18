"""Monthly long US bond total return from Shiller's ie_data file (research/data-long-1.md).

Source: https://shillerdata.com/ (ie_data.xls). Download it by hand into
`<cache_root>/shiller/ie_data.xls`; never commit it. Cache root: GRIMSTRADE_DATA or
`research/macro.local.json` (git-ignored, copy the `.example`).

Sheet "Data": the header is split over the rows above the row whose first cell is "Date".
Column labels confirmed on the Yale copy (2023-09): "Rate GS10" (long rate, %),
"Monthly Total Bond Returns" (gross one-month return on a 10y bond rebuilt from GS10, 0.98 =
-2%), "Real Total Bond Returns" (CPI-deflated index). Dates are year.month floats, so
1871.1 is October 1871. The shillerdata.com file (fetched 2026-11-18, the "ie_data.xls" link on
the home page) parses to 1,870 months, 1871-01 to 2026-10.
"""

from __future__ import annotations

import importlib
import json
import os
from collections.abc import Sequence
from datetime import date
from pathlib import Path
from typing import Any

RESEARCH = Path(__file__).resolve().parents[1]
CONFIG = RESEARCH / "macro.local.json"
RETURN_LABEL = "Monthly Total Bond Returns"
YIELD_LABEL = "Rate GS10"


def cache_root() -> Path:
    env = os.environ.get("GRIMSTRADE_DATA")
    if env:
        return Path(env).expanduser()
    if CONFIG.exists():
        return Path(json.loads(CONFIG.read_text())["cache_root"]).expanduser()
    raise FileNotFoundError(f"set GRIMSTRADE_DATA or copy {CONFIG.name}.example to {CONFIG.name}")


def _label(rows: Sequence[Sequence[Any]], header_end: int, col: int) -> str:
    parts = []
    for row in rows[: header_end + 1]:
        cell = row[col] if col < len(row) else None
        if isinstance(cell, str) and cell.strip():
            parts.append(cell.strip())
    return " ".join(parts)


def _month(x: float) -> date:
    year = int(x)
    month = round((x - year) * 100)
    if not 1 <= month <= 12:
        raise ValueError(f"bad Shiller date {x!r}")
    return date(year, month, 1)


def parse(rows: Sequence[Sequence[Any]]) -> list[tuple[date, float]]:
    """(first of month, gross monthly bond return) from the raw cells of sheet "Data"."""
    header_end = next(i for i, r in enumerate(rows) if r and r[0] == "Date")
    width = max(len(r) for r in rows[: header_end + 1])
    labels = [_label(rows, header_end, c) for c in range(width)]
    matches = [c for c, lab in enumerate(labels) if lab == RETURN_LABEL]
    if len(matches) != 1:
        raise ValueError(f"expected one {RETURN_LABEL!r} column, got labels {labels}")
    col = matches[0]
    out: list[tuple[date, float]] = []
    for row in rows[header_end + 1 :]:
        if not row or not isinstance(row[0], int | float) or col >= len(row):
            continue
        r = row[col]
        if isinstance(r, int | float) and r == r and r > 0:
            out.append((_month(float(row[0])), float(r)))
    days = [d for d, _ in out]
    if days != sorted(set(days)):
        raise ValueError("dates not strictly increasing")
    return out


def total_return_index(returns: Sequence[tuple[date, float]], start: float = 1.0) -> list[float]:
    level, out = start, []
    for _, r in returns:
        level *= r
        out.append(level)
    return out


def load(path: Path | None = None) -> list[tuple[date, float]]:
    """Read the cached ie_data.xls (needs `xlrd`, not a repo dependency: `uv run --with xlrd`)."""
    path = path or cache_root() / "shiller" / "ie_data.xls"
    xlrd: Any = importlib.import_module("xlrd")
    sheet = xlrd.open_workbook(str(path)).sheet_by_name("Data")
    return parse([sheet.row_values(i) for i in range(sheet.nrows)])
