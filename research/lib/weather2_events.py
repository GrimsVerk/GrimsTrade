"""Lane weather-2: pure functions for the CPC outlook-revision gate (card `research/weather-2.md`).

No network. Parses the CPC outlook shapefiles (bytes in, polygons out), evaluates the
outlook at points, builds the gas-weighted outlook index K per issue, the per-session
revision dose and the placebo session mapping. The runner is `weather2_rev.py`.
"""

from __future__ import annotations

import bisect
import io
import math
import struct
import zipfile
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date

import numpy as np

LAST_ISSUE = date(2025, 11, 9)  # held-out cut: later issues are dropped
SEASON_MONTHS = (11, 12, 1, 2, 3)
THIRD = 100.0 / 3.0

# Census divisions (CPC degree-day numbering 1-9) by state FIPS; contiguous states and DC.
DIVISION = {
    **{s: 1 for s in ("09", "23", "25", "33", "44", "50")},
    **{s: 2 for s in ("34", "36", "42")},
    **{s: 3 for s in ("17", "18", "26", "39", "55")},
    **{s: 4 for s in ("19", "20", "27", "29", "31", "38", "46")},
    **{s: 5 for s in ("10", "11", "12", "13", "24", "37", "45", "51", "54")},
    **{s: 6 for s in ("01", "21", "28", "47")},
    **{s: 7 for s in ("05", "22", "40", "48")},
    **{s: 8 for s in ("04", "08", "16", "30", "32", "35", "49", "56")},
    **{s: 9 for s in ("06", "41", "53")},
}


@dataclass(frozen=True)
class Poly:
    """One outlook polygon: tercile probability, category, rings of (lon, lat) points."""

    prob: float
    cat: str
    rings: tuple[np.ndarray, ...]
    bbox: tuple[float, float, float, float]


def _dbf(b: bytes) -> list[dict[str, str]]:
    nrec, hlen, rlen = struct.unpack("<IHH", b[4:12])
    fields: list[tuple[str, int]] = []
    o = 32
    while b[o] != 13:
        name = b[o : o + 11].split(b"\0")[0].decode("ascii", "replace").strip().lower()
        fields.append((name, b[o + 16]))
        o += 32
    out = []
    for r in range(nrec):
        rec = b[hlen + r * rlen : hlen + (r + 1) * rlen]
        if not rec or rec[:1] == b"*":
            out.append({})
            continue
        row, p = {}, 1
        for name, size in fields:
            row[name] = rec[p : p + size].decode("latin-1").strip()
            p += size
        out.append(row)
    return out


def _shp(b: bytes) -> list[tuple[np.ndarray, ...]]:
    """Rings of each polygon record (shape type 5 or 15/25: only x, y read; null shapes: ())."""
    out: list[tuple[np.ndarray, ...]] = []
    o = 100
    while o + 8 <= len(b):
        _, clen = struct.unpack(">ii", b[o : o + 8])
        c = b[o + 8 : o + 8 + 2 * clen]
        o += 8 + 2 * clen
        (stype,) = struct.unpack("<i", c[:4])
        if stype == 0:
            out.append(())
            continue
        nparts, npts = struct.unpack("<ii", c[36:44])
        parts = list(struct.unpack(f"<{nparts}i", c[44 : 44 + 4 * nparts]))
        p0 = 44 + 4 * nparts
        xy = np.frombuffer(c[p0 : p0 + 16 * npts], dtype="<f8").reshape(npts, 2)
        bounds = [*parts, npts]
        out.append(tuple(xy[bounds[i] : bounds[i + 1]] for i in range(nparts)))
    return out


def parse_outlook_zip(blob: bytes) -> tuple[date | None, list[Poly]]:
    """(issue date from `Fcst_Date`, polygons) of one CPC `{610,814}temp_*.zip`."""
    z = zipfile.ZipFile(io.BytesIO(blob))
    names = z.namelist()
    shp = next(n for n in names if n.lower().endswith(".shp"))
    dbf = next(n for n in names if n.lower().endswith(".dbf"))
    rings = _shp(z.read(shp))
    rows = _dbf(z.read(dbf))
    issue: date | None = None
    polys = []
    for rg, row in zip(rings, rows, strict=True):
        fd = row.get("fcst_date", "")
        if issue is None and len(fd) == 8 and fd.isdigit():
            issue = date(int(fd[:4]), int(fd[4:6]), int(fd[6:8]))
        if not rg:
            continue
        try:
            prob = float(row.get("prob", "nan"))
        except ValueError:
            continue
        allp = np.vstack(rg)
        bbox = (
            float(allp[:, 0].min()),
            float(allp[:, 1].min()),
            float(allp[:, 0].max()),
            float(allp[:, 1].max()),
        )
        polys.append(Poly(prob, row.get("cat", "").strip().lower(), rg, bbox))
    return issue, polys


def inside(p: Poly, lon: float, lat: float) -> bool:
    """Even-odd rule over all rings (holes included)."""
    x0, y0, x1, y1 = p.bbox
    if not (x0 <= lon <= x1 and y0 <= lat <= y1):
        return False
    hit = False
    for r in p.rings:
        xa, ya = r[:, 0], r[:, 1]
        xb, yb = np.roll(xa, -1), np.roll(ya, -1)
        cross = (ya > lat) != (yb > lat)
        with np.errstate(divide="ignore", invalid="ignore"):
            xint = xa + (lat - ya) * (xb - xa) / (yb - ya)
        hit ^= bool(np.count_nonzero(cross & (lon < xint)) % 2)
    return hit


def point_signal(polys: Sequence[Poly], lon: float, lat: float) -> float:
    """(Prob - 1/3) signed by category of the highest-Prob polygon containing the point."""
    best: Poly | None = None
    for p in polys:
        if (best is None or p.prob > best.prob) and inside(p, lon, lat):
            best = p
    if best is None or math.isnan(best.prob):
        return 0.0
    if best.cat.startswith("above"):
        return (best.prob - THIRD) / 100.0
    if best.cat.startswith("below"):
        return -(best.prob - THIRD) / 100.0
    return 0.0


@dataclass(frozen=True)
class Point:
    fips: str
    pop: float
    lat: float
    lon: float


def parse_centroids(text: str) -> list[Point]:
    """Census `CenPop2010_Mean_ST.txt`: contiguous states and DC only."""
    out = []
    for line in text.lstrip("﻿").splitlines()[1:]:
        c = [v.strip() for v in line.split(",")]
        if len(c) < 5 or c[0] not in DIVISION:
            continue
        out.append(Point(c[0], float(c[2]), float(c[3]), float(c[4])))
    return out


def conus_value(
    polys: Sequence[Poly], points: Sequence[Point], weights: Mapping[int, float]
) -> float:
    """Gas-weighted CONUS signal: population-weighted state mean per division, then w_k."""
    num = dict.fromkeys(weights, 0.0)
    den = dict.fromkeys(weights, 0.0)
    for pt in points:
        k = DIVISION[pt.fips]
        num[k] += pt.pop * point_signal(polys, pt.lon, pt.lat)
        den[k] += pt.pop
    return sum(w * num[k] / den[k] for k, w in weights.items() if den[k] > 0)


def nnls_weights(conus: np.ndarray, divisions: np.ndarray) -> np.ndarray:
    """Non-negative least squares of CONUS on the division columns, normalised to sum 1."""
    from scipy.optimize import nnls

    w, _ = nnls(divisions, conus)
    return np.asarray(w / w.sum())


def winter_of(d: date) -> int:
    return d.year if d.month >= 11 else d.year - 1


def offset(d: date) -> int:
    return (d - date(winter_of(d), 11, 1)).days


def session_doses(sessions: Sequence[date], k: Mapping[date, float]) -> dict[date, float]:
    """x(t) = K(I(t)) - K(I(t')), I(t) the latest issue strictly before t, t' the previous
    session. Sessions with no new issue since t', or without both issues, get no dose."""
    issues = sorted(d for d in k if d <= LAST_ISSUE)
    out: dict[date, float] = {}

    def latest(t: date) -> date | None:
        i = bisect.bisect_left(issues, t) - 1
        return issues[i] if i >= 0 else None

    for prev, t in zip(sessions, sessions[1:], strict=False):
        a, b = latest(prev), latest(t)
        if a is None or b is None or a == b:
            continue
        out[t] = k[b] - k[a]
    return out


def placebo_session(t: date, winter: int, by_winter: Mapping[int, Sequence[date]]) -> date | None:
    """Session of `winter` whose offset from Nov 1 is closest to t's (<= 3 days, ties early)."""
    o = offset(t)
    best: date | None = None
    for s in by_winter.get(winter, ()):
        dlt = abs(offset(s) - o)
        if dlt <= 3 and (best is None or dlt < abs(offset(best) - o)):
            best = s
    return best
