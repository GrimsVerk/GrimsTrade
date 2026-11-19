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
