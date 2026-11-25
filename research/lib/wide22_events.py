"""Pure functions for the wide-22 gate W36 `grid-load-premium` (research/cards/wide-22.md).
No function here reads a file, a price or the network. Months are indexed as in
`wide17_events.month_index` (January 2000 -> 24000)."""

from __future__ import annotations

import csv
import math
from collections.abc import Iterable, Mapping, Sequence
from datetime import date

import numpy as np

# Earlier doses only (prices lead output; gate-null step 1): k = 25, 27, ..., 103 months.
SHIFTS: list[int] = list(range(25, 104, 2))
LAG = 3  # usage month m is paired with the market return of month m + 3
SEED = 22


def month_index(d: date) -> int:
    return d.year * 12 + d.month - 1


def parse_mer(text: str, msn: str, last: date) -> dict[int, float]:
    """Monthly values of one series (MSN code) from an EIA Monthly Energy Review table CSV
    (columns MSN, YYYYMM, Value, ...). Annual rows (month 13), values that are not numbers and
    months after the month of `last` are left out."""
    cut = month_index(last)
    out: dict[int, float] = {}
    for row in csv.reader(text.splitlines()):
        if len(row) < 3 or row[0].strip() != msn:
            continue
        ym = row[1].strip()
        if len(ym) != 6 or not ym.isdigit():
            continue
        y, mo = int(ym[:4]), int(ym[4:])
        if not 1 <= mo <= 12:
            continue
        try:
            v = float(row[2])
        except ValueError:
            continue
        m = y * 12 + mo - 1
        if m <= cut and v > 0:
            out[m] = v
    return out


def yoy(u: Mapping[int, float]) -> dict[int, float]:
    """g(m) = 100 ln(U(m) / U(m - 12)), only where both months exist."""
    return {m: 100.0 * math.log(v / u[m - 12]) for m, v in u.items() if m - 12 in u}


def parse_french_monthly(lines: Iterable[str], last: date) -> dict[int, tuple[float, float]]:
    """{month: (Mkt-RF, RF)} in percent from French's monthly factor CSV: the first block of
    rows whose first field is a six-digit YYYYMM; months after the month of `last` dropped.
    Stops at the first non-monthly row after the block (the annual block follows)."""
    cut = month_index(last)
    out: dict[int, tuple[float, float]] = {}
    started = False
    for line in lines:
        parts = [p.strip() for p in line.split(",")]
        key = parts[0] if parts else ""
        if len(key) == 6 and key.isdigit() and len(parts) >= 5:
            started = True
            m = int(key[:4]) * 12 + int(key[4:]) - 1
            if m <= cut:
                out[m] = (float(parts[1]), float(parts[4]))
        elif started:
            break
    return out


def parse_fred(text: str, last: date) -> dict[int, float]:
    """Monthly values from a FRED `fredgraph.csv` (date, value); '.' and months after the month
    of `last` dropped."""
    cut = month_index(last)
    out: dict[int, float] = {}
    for row in csv.reader(text.splitlines()):
        if len(row) < 2:
            continue
        try:
            d = date.fromisoformat(row[0].strip())
            v = float(row[1])
        except ValueError:
            continue
        m = month_index(d)
        if m <= cut and v > 0:
            out[m] = v
    return out


def shifted(d: Mapping[int, float], k: int) -> dict[int, float]:
    """d_k(m) = d(m - k): for k > 0 an earlier dose."""
    return {m + k: v for m, v in d.items()}


def window_sum(y: Mapping[int, float], first: int, h: int) -> dict[int, float]:
    """{m: sum of y(m + first + j), j = 0..h-1} where all h months exist (first > 0: months
    ahead of m; first <= 0 with h: a trailing window ending at m + first + h - 1)."""
    if not y:
        return {}
    out: dict[int, float] = {}
    for m in range(min(y) - first - h + 1, max(y) - first + 1):
        vals = [y.get(m + first + j) for j in range(h)]
        if all(v is not None for v in vals):
            out[m] = sum(v for v in vals if v is not None)
    return out


def contiguous(d: Mapping[int, float]) -> list[int]:
    """The longest run of consecutive months in `d` (sorted)."""
    ms = sorted(d)
    best: list[int] = []
    run: list[int] = []
    for m in ms:
        if run and m != run[-1] + 1:
            run = []
        run.append(m)
        if len(run) > len(best):
            best = list(run)
    return best


def phase_surrogates(
    d: Mapping[int, float], n: int = 40, seed: int = SEED
) -> list[dict[int, float]]:
    """n phase-randomised surrogates of the dose on its longest contiguous run of months (same
    mean and amplitude spectrum, random Fourier phases; Theiler et al. 1992). Deterministic for
    a given seed."""
    ms = contiguous(d)
    x = np.array([d[m] for m in ms])
    mu = float(x.mean())
    f = np.fft.rfft(x - mu)
    rng = np.random.default_rng(seed)
    out: list[dict[int, float]] = []
    for _ in range(n):
        ph = rng.uniform(0.0, 2.0 * math.pi, len(f))
        ph[0] = 0.0
        if len(x) % 2 == 0:
            ph[-1] = 0.0
        s = np.fft.irfft(np.abs(f) * np.exp(1j * ph), n=len(x)) + mu
        out.append({m: float(v) for m, v in zip(ms, s, strict=True)})
    return out


def rank_lowest(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly below `true` (1 = the lowest)."""
    return 1 + sum(o < true for o in others)
