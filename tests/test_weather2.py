"""The weather-2 functions compute what research/weather-2.md says they do."""

from __future__ import annotations

import importlib
import io
import struct
import sys
import zipfile
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


def _ev() -> Any:
    sys.path.insert(0, str(LIB))
    try:
        return importlib.import_module("weather2_events")
    finally:
        sys.path.remove(str(LIB))


def _square(x0: float, y0: float, x1: float, y1: float) -> list[tuple[float, float]]:
    return [(x0, y0), (x0, y1), (x1, y1), (x1, y0), (x0, y0)]


def _zip(polys: list[tuple[list[list[tuple[float, float]]], float, str]], fdate: str) -> bytes:
    """A minimal shapefile zip: polygon records (type 5) and a dbf with Fcst_Date/Prob/Cat."""
    recs = b""
    for i, (rings, _, _) in enumerate(polys):
        pts = [p for r in rings for p in r]
        parts, n = [], 0
        for r in rings:
            parts.append(n)
            n += len(r)
        c = struct.pack("<i4d", 5, 0, 0, 0, 0) + struct.pack("<ii", len(rings), len(pts))
        c += struct.pack(f"<{len(parts)}i", *parts)
        c += b"".join(struct.pack("<2d", *p) for p in pts)
        recs += struct.pack(">ii", i + 1, len(c) // 2) + c
    shp = b"\0" * 100 + recs
    fields = [("Fcst_Date", b"D", 8), ("Prob", b"F", 13), ("Cat", b"C", 10)]
    rlen = 1 + sum(f[2] for f in fields)
    hlen = 32 + 32 * len(fields) + 1
    head = struct.pack("<4xIHH20x", len(polys), hlen, rlen)
    for name, typ, size in fields:
        head += name.encode().ljust(11, b"\0") + typ + b"\0" * 4 + bytes([size]) + b"\0" * 15
    head += b"\r"
    body = b"".join(
        b" " + fdate.encode() + f"{p:13.5e}".encode() + c.encode().ljust(10) for _, p, c in polys
    )
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as z:
        z.writestr("x.shp", shp)
        z.writestr("x.dbf", head + body)
    return buf.getvalue()


def test_parse_and_point_signal_take_innermost_polygon() -> None:
    ev = _ev()
    blob = _zip(
        [
            ([_square(-100, 30, -80, 50)], 33.0, "Below"),
            ([_square(-95, 35, -85, 45)], 50.0, "Below"),
            ([_square(-120, 30, -110, 50), _square(-118, 35, -112, 45)], 40.0, "Above"),
        ],
        "20150110",
    )
    issue, polys = ev.parse_outlook_zip(blob)
    assert issue == date(2015, 1, 10)
    assert len(polys) == 3
    assert abs(ev.point_signal(polys, -90, 40) - -(50 - 100 / 3) / 100) < 1e-12
    assert abs(ev.point_signal(polys, -98, 32) - -(33 - 100 / 3) / 100) < 1e-12
    assert abs(ev.point_signal(polys, -119, 40) - (40 - 100 / 3) / 100) < 1e-12
    assert ev.point_signal(polys, -115, 40) == 0.0  # inside the hole
    assert ev.point_signal(polys, -70, 40) == 0.0  # equal chances


def test_session_doses_use_issues_strictly_before_and_drop_no_news() -> None:
    ev = _ev()
    k = {date(2015, 1, 5): 0.1, date(2015, 1, 6): 0.3, date(2015, 1, 8): 0.2}
    sessions = [date(2015, 1, 6), date(2015, 1, 7), date(2015, 1, 8), date(2015, 1, 9)]
    x = ev.session_doses(sessions, k)
    # Jan 7: issue Jan 6 vs Jan 5; Jan 8: latest before is still Jan 6 -> dropped;
    # Jan 9: Jan 8 vs Jan 6.
    assert set(x) == {date(2015, 1, 7), date(2015, 1, 9)}
    assert abs(x[date(2015, 1, 7)] - 0.2) < 1e-12
    assert abs(x[date(2015, 1, 9)] - -0.1) < 1e-12


def test_held_out_issues_never_enter_a_dose() -> None:
    ev = _ev()
    k = {date(2025, 11, 7): 0.0, date(2025, 11, 9): 0.1, date(2025, 11, 10): 5.0}
    x = ev.session_doses([date(2025, 11, 10), date(2025, 11, 11)], k)
    assert x == {}  # Nov 11 would need the Nov 10 issue, which is past the cut


def test_placebo_session_is_closest_offset_within_three_days() -> None:
    ev = _ev()
    by = {2016: [date(2016, 11, 2), date(2016, 11, 4), date(2016, 11, 9)]}
    assert ev.placebo_session(date(2015, 11, 3), 2016, by) == date(2016, 11, 2)  # tie: early
    assert ev.placebo_session(date(2015, 11, 8), 2016, by) == date(2016, 11, 9)
    assert ev.placebo_session(date(2015, 11, 20), 2016, by) is None


def test_nnls_weights_recover_a_known_mix() -> None:
    ev = _ev()
    rng = np.random.default_rng(0)
    a = rng.uniform(0, 40, size=(200, 3))
    w = ev.nnls_weights(a @ np.array([0.5, 0.3, 0.2]), a)
    assert np.allclose(w, [0.5, 0.3, 0.2])
