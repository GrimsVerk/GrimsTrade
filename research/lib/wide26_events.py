"""Pure functions for wide-26's gate W43 `drought-food-margin` (research/cards/wide-26.md).
No function here reads a file, a price or the network.

Months are month indices (year * 12 + month - 1, `wide17_events.month_index`)."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence

import numpy as np

CORN_BELT = "361"  # nClimDiv: Corn Belt, productivity weighted
NATIONAL = "110"  # nClimDiv: contiguous US (W32's dose)
SEED = 26


def yyyymm_index(s: str) -> int:
    """'196001' -> month index of January 1960."""
    return int(s[:4]) * 12 + int(s[4:6]) - 1


def parse_block(text: str, title: str, last: int) -> tuple[list[str], dict[int, list[float]]]:
    """Column names and {month index: values in percent} of the French CSV block whose title
    line is `title`. Missing (-99.99, -999) -> NaN. Months after `last` are left out."""
    lines = text.splitlines()
    head = next(i for i, x in enumerate(lines) if x.strip() == title)
    names = [x.strip() for x in lines[head + 1].split(",")][1:]
    out: dict[int, list[float]] = {}
    started = False
    for line in lines[head + 2 :]:
        cells = [x.strip() for x in line.split(",")]
        if len(cells) == len(names) + 1 and len(cells[0]) == 6 and cells[0].isdigit():
            started = True
            m = yyyymm_index(cells[0])
            if m <= last:
                out[m] = [math.nan if float(v) <= -99 else float(v) for v in cells[1:]]
        elif started:
            break
    return names, out


def parse_factors(text: str, last: int) -> dict[int, tuple[float, float]]:
    """{month index: (Mkt-RF, RF)} in percent from the monthly block of the French
    F-F_Research_Data_Factors CSV (the first block; it ends at the annual block)."""
    lines = text.splitlines()
    head = next(i for i, x in enumerate(lines) if x.replace(" ", "") == ",Mkt-RF,SMB,HML,RF")
    out: dict[int, tuple[float, float]] = {}
    for line in lines[head + 1 :]:
        cells = [x.strip() for x in line.split(",")]
        if len(cells) != 5 or len(cells[0]) != 6 or not cells[0].isdigit():
            break
        m = yyyymm_index(cells[0])
        if m <= last:
            out[m] = (float(cells[1]), float(cells[4]))
    return out


def beta(ex: Mapping[int, float], mkt: Mapping[int, float], end: int, n: int = 60) -> float:
    """OLS slope (with intercept) of ex on mkt over months end-n+1 .. end; NaN unless all n
    months have both values."""
    months = range(end - n + 1, end + 1)
    xs, ys = [], []
    for m in months:
        x, y = mkt.get(m, math.nan), ex.get(m, math.nan)
        if math.isnan(x) or math.isnan(y):
            return math.nan
        xs.append(x)
        ys.append(y)
    xa, ya = np.array(xs), np.array(ys)
    xd = xa - xa.mean()
    return float((xd @ (ya - ya.mean())) / (xd @ xd))


def outcome(
    ex: Mapping[int, float],
    mkt: Mapping[int, float],
    m: int,
    first: int = 2,
    length: int = 3,
    adjust: str = "beta",
) -> float:
    """y(m) = sum over j = m+first .. m+first+length-1 of ex_j - b mkt_j, where b is the
    60-month beta ending m+first-1 ('beta'), 1 ('raw'), or 0 ('none': ex itself). NaN if a
    month is missing."""
    if adjust == "beta":
        b = beta(ex, mkt, m + first - 1)
    elif adjust == "raw":
        b = 1.0
    else:
        b = 0.0
    if math.isnan(b):
        return math.nan
    s = 0.0
    for j in range(m + first, m + first + length):
        x, y = mkt.get(j, math.nan), ex.get(j, math.nan)
        if math.isnan(x) or math.isnan(y):
            return math.nan
        s += y - b * x
    return s


def shift_dose(dose: Mapping[int, float], k: int) -> dict[int, float]:
    """D_k(m) = D(m - k)."""
    return {m + k: v for m, v in dose.items()}


def drying(pdsi: Mapping[int, float]) -> dict[int, float]:
    """PDSI(m-3) - PDSI(m) (positive = drier)."""
    return {m: pdsi[m - 3] - v for m, v in pdsi.items() if m - 3 in pdsi}


def acf1(dose: Mapping[int, float]) -> float:
    """Lag-1 autocorrelation over consecutive months present in `dose`."""
    ms = sorted(dose)
    a = np.array([dose[m] for m in ms])
    a = a - a.mean()
    num = sum(a[i] * a[i + 1] for i in range(len(ms) - 1) if ms[i + 1] == ms[i] + 1)
    return float(num / (a @ a))


def regress(
    months: Sequence[int], y: Mapping[int, float], dose: Mapping[int, float], lags: int
) -> tuple[float, float, int]:
    """(b, Newey-West t of b, rows) of y = a + b D over `months` with both present (one row
    per month; Bartlett weights over month distance)."""
    import wide11_events as e11

    rows = [m for m in months if m in dose and not math.isnan(y.get(m, math.nan))]
    if len(rows) < 10:
        return math.nan, math.nan, len(rows)
    d = np.array([dose[m] for m in rows])
    ya = np.array([y[m] for m in rows])
    coef, t, n = e11.ols_dk([np.ones(len(rows)), d], ya, np.array(rows), lags)
    return float(coef[1]), float(t[1]), n


def rank_lowest(true: float, others: Sequence[float]) -> int:
    """1 + the number of others strictly below `true` (1 = the lowest)."""
    return 1 + sum(1 for o in others if o < true)


def null_spread(ts: Sequence[float]) -> tuple[float, float, float, float, float, float, float]:
    """(sd, share |t| >= 2, q5, median, q95, min, max) of placebo t values (NaN dropped)."""
    a = np.asarray([v for v in ts if not math.isnan(v)], dtype=float)
    q5, q50, q95 = (float(v) for v in np.quantile(a, [0.05, 0.5, 0.95]))
    return (
        float(a.std(ddof=1)),
        float(np.mean(np.abs(a) >= 2)),
        q5,
        q50,
        q95,
        float(a.min()),
        float(a.max()),
    )


# ---------------------------------------------------------------- W18 elimination-mood
# (research/cards/wide-26b.md: a record-closing check of wide-8's W18)

TOURNAMENTS = ("FIFA World Cup", "UEFA Euro")
W18_SHIFTS = [23 * k for k in range(-20, 0)] + [23 * k for k in range(1, 21)]
W18_LAGS = 5


def parse_matches(text: str) -> list[tuple[int, str, str, int, int, str]]:
    """(date ordinal, home, away, home goals, away goals, tournament) of every row of the
    `results.csv` of martj42/international_results with numeric scores."""
    import csv
    import io
    from datetime import date

    out = []
    for r in csv.DictReader(io.StringIO(text)):
        hs, as_ = r["home_score"], r["away_score"]
        if not (hs.isdigit() and as_.isdigit()):
            continue
        d = date.fromisoformat(r["date"]).toordinal()
        out.append((d, r["home_team"], r["away_team"], int(hs), int(as_), r["tournament"]))
    return out


def parse_shootouts(text: str) -> dict[tuple[int, str, str], str]:
    """{(date ordinal, home, away): winner} from `shootouts.csv`."""
    import csv
    import io
    from datetime import date

    return {
        (date.fromisoformat(r["date"]).toordinal(), r["home_team"], r["away_team"]): r["winner"]
        for r in csv.DictReader(io.StringIO(text))
    }


def knockout_events(
    matches: Sequence[tuple[int, str, str, int, int, str]],
    shootouts: Mapping[tuple[int, str, str], str],
    tournaments: Sequence[str] = TOURNAMENTS,
) -> list[tuple[str, int, str, int, str]]:
    """(team, match date ordinal, kind, match number, tournament) per the W18 card. kind:
    'elim' = the team's first knockout match (4th or later of the edition) that it lost, in play
    or on penalties; 'win' = each knockout match it won; 'group' = the last match of a team that
    played exactly three. Editions: tournament x calendar year of the match. A drawn knockout
    match without a shootout record is skipped (unknown winner)."""
    from datetime import date

    ed: dict[tuple[str, int, str], list[tuple[int, str]]] = {}
    for d, h, a, hs, as_, t in matches:
        if t not in tournaments:
            continue
        y = date.fromordinal(d).year
        for team, _opp, gf, ga in ((h, a, hs, as_), (a, h, as_, hs)):
            if gf > ga:
                res = "W"
            elif gf < ga:
                res = "L"
            else:
                w = shootouts.get((d, h, a))
                res = "D" if w is None else ("W" if w == team else "L")
            ed.setdefault((t, y, team), []).append((d, res))
    out: list[tuple[str, int, str, int, str]] = []
    for (t, _, team), ms in ed.items():
        ms.sort()
        if len(ms) == 3:
            out.append((team, ms[2][0], "group", 3, t))
        lost = False
        for n, (d, res) in enumerate(ms, start=1):
            if n < 4 or res == "D":
                continue
            if res == "W":
                out.append((team, d, "win", n, t))
            elif not lost:
                out.append((team, d, "elim", n, t))
                lost = True
    return sorted(out, key=lambda e: (e[1], e[0]))


def next_session_dose(
    dates: np.ndarray, days: Sequence[tuple[int, float]], shift: int = 0
) -> np.ndarray:
    """Dose over sessions: each (match day, weight) lands on the first session dated on or
    after match day + 1 + shift; days outside the session range drop."""
    d = np.zeros(len(dates))
    if len(dates) == 0:
        return d
    for day, w in days:
        x = day + 1 + shift
        if x < dates[0] or x > dates[-1]:
            continue
        s = int(np.searchsorted(dates, x, side="left"))
        if s < len(dates):
            d[s] += w
    return d


def session_rows(
    dates: np.ndarray,
    logc: np.ndarray,
    others: Sequence[tuple[np.ndarray, np.ndarray]],
    first_day: int,
    last_day: int,
    after: int = 0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """(s, y, raw, period) for sessions s >= 1 dated in [first_day, last_day] with session
    s + after present and dated <= last_day: raw = ln C(s+after) - ln C(s-1), y = raw minus the
    other markets' mean change between the dates of s-1 and s+after (`world_change` of
    wide-24); period = the calendar date of session s."""
    import wide24_events as e24

    n = len(dates)
    s = np.arange(1, max(1, n - after))
    s = s[(dates[s] >= first_day) & (dates[s] <= last_day) & (dates[s + after] <= last_day)]
    w = e24.world_change(dates[s - 1], dates[s + after], others)
    raw = logc[s + after] - logc[s - 1]
    ok = np.isfinite(w)
    s, w, raw = s[ok], w[ok], raw[ok]
    return s, raw - w, raw, dates[s].astype(int)
