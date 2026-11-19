"""The wide-12 functions compute what research/wide-12.md step 2 says they do."""

from __future__ import annotations

import importlib
import io
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide12_events")
    finally:
        sys.path.remove(str(LIB))


def _closes(bars: dict[date, float]) -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("wide11_events").Closes(bars)
    finally:
        sys.path.remove(str(LIB))


XML = b"""<?xml version="1.0"?>
<m:DataSet xmlns:m="urn:x" xmlns:k="urn:k">
 <k:Series SERIES_NAME="OTHER.WW"><k:Obs TIME_PERIOD="2020-01-01" OBS_VALUE="9"/></k:Series>
 <k:Series SERIES_NAME="RESH4FG_N.WW">
  <k:Annotations/>
  <k:Obs TIME_PERIOD="2020-01-01" OBS_VALUE="100"/>
  <k:Obs TIME_PERIOD="2020-01-08" OBS_VALUE="ND"/>
  <k:Obs TIME_PERIOD="2020-01-29" OBS_VALUE="110"/>
  <k:Obs TIME_PERIOD="2020-02-05" OBS_VALUE="120"/>
 </k:Series>
</m:DataSet>"""


def test_read_series_picks_the_named_series_skips_bad_and_late_values() -> None:
    ev = _ev()
    got = ev.read_series(io.BytesIO(XML), "RESH4FG_N.WW", date(2020, 1, 31))
    assert got == {date(2020, 1, 1): 100.0, date(2020, 1, 29): 110.0}


def test_flow_is_the_log_change_over_exactly_28_days() -> None:
    ev = _ev()
    lv = {date(2020, 1, 1): 100.0, date(2020, 1, 29): 110.0, date(2020, 2, 5): 120.0}
    f = ev.flows(lv)
    assert f == {date(2020, 1, 29): math.log(1.1)}


def test_outcome_enters_monday_after_release_and_never_sees_later_bars() -> None:
    ev = _ev()
    w = date(2020, 1, 1)  # a Wednesday
    bars = {w + timedelta(days=i): 100.0 + i for i in range(0, 60)}
    px = _closes(bars)
    y = ev.outcome(px, w, 33, date(2030, 1, 1))
    assert math.isclose(y, math.log(133.0 / 105.0))
    # exit after the last train bar: dropped
    assert math.isnan(ev.outcome(px, w, 33, w + timedelta(days=30)))
    # exit bar too late (gap of more than a week): dropped
    gap = {
        d: v for d, v in bars.items() if not (w + timedelta(days=30) <= d <= w + timedelta(days=41))
    }
    assert math.isnan(ev.outcome(_closes(gap), w, 33, date(2030, 1, 1)))
