"""Look-ahead-safe macro features (research run macro-1). Standard library only.

The rule (research/protocol.md, "Macro tests"): a number may be used at the decision on day `d`
only if it was public before `d`, that is, from the day after it became public.

- Revised series (ALFRED vintages: PAYEMS, M2SL, CPIAUCSL, UNRATE, INDPRO, WALCL): a record
  became public on its `realtime_start`. The feature on day `d` is computed from the vintage that
  was current on `d - 1`: for each observation, the record with `realtime_start <= d - 1 <=
  realtime_end`. Today's revised numbers are never used.
- Before a series' first ALFRED vintage (WALCL: 2011-07-07) there is no record of what was
  known. Those observations take their value from the first vintage and count as public
  `FIRST_VINTAGE_LAG` days after the observation date (later than the real release).
- Market series that are not revised (DFF, DGS10, T10Y2Y, BAA10Y, ...): the observation for day
  `x` counts as public on `x`, so it is used from `x + 1` (the brief's rule; FRED posts daily
  rates the next business day, and fills come at the next open after that).

A feature is a `Step`: a list of (first decision day it may be used, value). `Step.at(d)` is
the value a decision on day `d` may see, NaN if none yet.

Cache root: `research/macro.local.json` (git-ignored, copy `macro.local.json.example`) or the
environment variable GRIMSTRADE_DATA. Downloaded files are read as data only (json.load).
"""

from __future__ import annotations

import bisect
import json
import math
import os
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

RESEARCH = Path(__file__).resolve().parents[1]
CONFIG = RESEARCH / "macro.local.json"
FAR = date(9999, 12, 31)
DAY = timedelta(days=1)

VINTAGED = ("PAYEMS", "M2SL", "CPIAUCSL", "UNRATE", "INDPRO", "WALCL")
# Days after the observation date at which an observation older than the first vintage counts
# as public. Monthly series are dated the 1st of the month and come out mid-next-month; WALCL
# (Wednesday) comes out the next day. Both lags are longer than the real ones.
FIRST_VINTAGE_LAG = {"WALCL": 7}
MONTHLY_LAG = 45

# Bitcoin halvings (block heights 210,000 / 420,000 / 630,000 / 840,000). The schedule is fixed
# by the protocol years ahead; the date was predictable to within weeks.
HALVINGS = (date(2012, 11, 28), date(2016, 7, 9), date(2020, 5, 11), date(2024, 4, 19))


def cache_root() -> Path:
    env = os.environ.get("GRIMSTRADE_DATA")
    if env:
        return Path(env).expanduser()
    if CONFIG.exists():
        return Path(json.loads(CONFIG.read_text())["cache_root"]).expanduser()
    raise FileNotFoundError(f"set GRIMSTRADE_DATA or copy {CONFIG.name}.example to {CONFIG.name}")


@dataclass(frozen=True)
class Rec:
    """One published value: observation date, first and last day of its vintage, value."""

    obs: date
    start: date
    end: date
    value: float


def _records(raw: Iterable[dict[str, str]]) -> list[Rec]:
    out = []
    for r in raw:
        if r["value"] in (".", ""):
            continue
        out.append(
            Rec(date.fromisoformat(r["date"]), date.fromisoformat(r["realtime_start"]),
                date.fromisoformat(r["realtime_end"]), float(r["value"]))
        )  # fmt: skip
    return out


def vintage_records(series: str, raw: Iterable[dict[str, str]] | None = None) -> list[Rec]:
    """ALFRED records, plus a back-filled record for observations older than the first vintage."""
    if raw is None:
        path = cache_root() / "fred" / "api" / "vintages" / f"{series}.json"
        raw = json.loads(path.read_text())["observations"]
    recs = _records(raw)
    first = min(r.start for r in recs)
    lag = timedelta(days=FIRST_VINTAGE_LAG.get(series, MONTHLY_LAG))
    back = [
        Rec(r.obs, r.obs + lag, first - DAY, r.value)
        for r in recs
        if r.start == first and r.obs + lag < first
    ]
    return sorted(back + recs, key=lambda r: (r.start, r.obs))


def market_records(series: str, raw: Iterable[dict[str, str]] | None = None) -> list[Rec]:
    """An unrevised daily series: the value for day x is public on x (used from x + 1)."""
    if raw is None:
        folder = cache_root() / "fred" / "api" / "latest" / series
        path = sorted(folder.glob("*.json"))[-1]
        raw = json.loads(path.read_text())["observations"]
    return [Rec(r.obs, r.obs, FAR, r.value) for r in sorted(_records(raw), key=lambda r: r.obs)]


class Step:
    """A piecewise-constant feature: value[i] may be used by decisions on days >= days[i]."""

    def __init__(self, days: Sequence[date], values: Sequence[float]):
        if any(b < a for a, b in zip(days, days[1:], strict=False)):
            raise ValueError("days must be sorted")
        self.days = list(days)
        self.values = list(values)
        self._ord = [d.toordinal() for d in self.days]

    def at(self, d: date) -> float:
        i = bisect.bisect_right(self._ord, d.toordinal())
        return self.values[i - 1] if i else math.nan

    def map(self, f: Callable[[float], float]) -> Step:
        return Step(self.days, [f(v) for v in self.values])


def snapshot(recs: Sequence[Rec], asof: date) -> dict[date, float]:
    """The vintage current on `asof`: what a reader of FRED saw that day. Slow; for checks."""
    return {r.obs: r.value for r in recs if r.start <= asof <= r.end}


SnapFn = Callable[[dict[date, float], list[date]], float]


def vintage_feature(recs: Sequence[Rec], fn: SnapFn) -> Step:
    """Apply `fn(snapshot, sorted obs dates)` to every vintage; usable from the day after."""
    # the vintage changes when a record starts, and the day after one ends (a deleted value)
    starts = sorted({r.start for r in recs} | {r.end + DAY for r in recs if r.end < FAR})
    by_start: dict[date, list[Rec]] = {}
    for r in recs:
        by_start.setdefault(r.start, []).append(r)
    ends: dict[date, list[Rec]] = {}
    for r in recs:
        ends.setdefault(r.end, []).append(r)
    end_days = sorted(ends)
    cur: dict[date, Rec] = {}
    days, vals = [], []
    k = 0
    for v in starts:
        # drop records whose vintage ended before v (an observation removed, or superseded)
        while k < len(end_days) and end_days[k] < v:
            for r in ends[end_days[k]]:
                if cur.get(r.obs) is r:
                    del cur[r.obs]
            k += 1
        for r in by_start.get(v, []):
            cur[r.obs] = r
        snap = {o: r.value for o, r in cur.items()}
        days.append(v + DAY)
        vals.append(fn(snap, sorted(snap)) if snap else math.nan)
    return Step(days, vals)


def market_feature(
    recs: Sequence[Rec], fn: Callable[[list[date], list[float], int], float]
) -> Step:
    """`fn(obs dates, values, i)` may read entries 0..i only; usable from obs[i] + 1 day."""
    obs = [r.obs for r in recs]
    vals = [r.value for r in recs]
    return Step([o + DAY for o in obs], [fn(obs, vals, i) for i in range(len(obs))])


# --- building blocks for features ---


def months_back(d: date, n: int) -> date:
    y, m = divmod(d.year * 12 + d.month - 1 - n, 12)
    return date(y, m + 1, 1)


def yoy(snap: dict[date, float], obs: list[date]) -> float:
    """Growth over 12 months of a monthly series, latest observation in the snapshot, percent."""
    last = obs[-1]
    prev = snap.get(months_back(last, 12))
    return 100 * (snap[last] / prev - 1) if prev else math.nan


def yoy_weekly(snap: dict[date, float], obs: list[date]) -> float:
    """Growth over 52 weeks of a weekly series (WALCL), percent."""
    last = obs[-1]
    i = bisect.bisect_right(obs, last - timedelta(days=364)) - 1
    if i < 0 or (last - obs[i]).days > 371:
        return math.nan
    return 100 * (snap[last] / snap[obs[i]] - 1)


def change_3m(snap: dict[date, float], obs: list[date]) -> float:
    """Change of the latest monthly value against the lowest of the 12 months before (Sahm-like),
    in the series' units."""
    last = obs[-1]
    prior = [snap[o] for o in obs if months_back(last, 12) <= o < last]
    if len(prior) < 11:
        return math.nan
    cur = sum(snap.get(months_back(last, k), math.nan) for k in range(3)) / 3
    return cur - min(prior)


def rolling_mean(n: int) -> Callable[[list[date], list[float], int], float]:
    def f(obs: list[date], vals: list[float], i: int) -> float:
        return sum(vals[i - n + 1 : i + 1]) / n if i >= n - 1 else math.nan

    return f


def last_value(obs: list[date], vals: list[float], i: int) -> float:
    return vals[i]


def combine(a: Step, b: Step, f: Callable[[float, float], float]) -> Step:
    """f(a, b) on the union of both steps' days (each side at its own latest value)."""
    days = sorted(set(a.days) | set(b.days))
    return Step(days, [f(a.at(d), b.at(d)) for d in days])


def lagged_change(s: Step, days: int) -> Step:
    """Value minus the value the same feature had `days` calendar days earlier."""
    lag = timedelta(days=days)
    return Step(s.days, [v - s.at(d - lag) for d, v in zip(s.days, s.values, strict=True)])


def window_min(s: Step, days: int) -> Step:
    """Lowest value over the last `days` calendar days (on the step's own days)."""
    out = []
    for i, d in enumerate(s.days):
        j = bisect.bisect_left(s.days, d - timedelta(days=days))
        out.append(min(s.values[j : i + 1]))
    return Step(s.days, out)


def days_since_halving(d: date) -> float:
    past = [h for h in HALVINGS if h < d]
    return float((d - past[-1]).days) if past else math.nan


# --- the feature set (fixed on the cards before any test) ---


class Features:
    """All macro features, loaded once. Attributes are `Step`s indexed by decision day."""

    def __init__(self) -> None:
        dff = market_records("DFF")
        self.dff30 = market_feature(dff, rolling_mean(30))  # fed funds, 30-day mean, percent
        self.dff_chg182 = lagged_change(self.dff30, 182)
        cpi = vintage_records("CPIAUCSL")
        self.cpi_yoy = vintage_feature(cpi, yoy)
        self.real_ff = combine(self.dff30, self.cpi_yoy, lambda a, b: a - b)
        self.real_ff_chg365 = lagged_change(self.real_ff, 365)
        self.curve = market_feature(market_records("T10Y2Y"), last_value)
        self.curve_min365 = window_min(self.curve, 365)
        self.baa20 = market_feature(market_records("BAA10Y"), rolling_mean(20))
        self.baa_rise = combine(self.baa20, window_min(self.baa20, 365), lambda a, b: a - b)
        self.m2_yoy = vintage_feature(vintage_records("M2SL"), yoy)
        self.real_m2 = combine(self.m2_yoy, self.cpi_yoy, lambda a, b: a - b)
        self.walcl_yoy = vintage_feature(vintage_records("WALCL"), yoy_weekly)
        # inputs listed for the RL agent (scored, not traded)
        self.unrate_rise = vintage_feature(vintage_records("UNRATE"), change_3m)
        self.indpro_yoy = vintage_feature(vintage_records("INDPRO"), yoy)
        self.payems_yoy = vintage_feature(vintage_records("PAYEMS"), yoy)
        self.dgs10 = market_feature(market_records("DGS10"), last_value)
        self.vix = market_feature(market_records("VIXCLS"), last_value)

    # Hostile phases (True = step risk assets aside). NaN inputs count as "not hostile".
    def fed_hiking(self, d: date) -> bool:
        return self.dff_chg182.at(d) > 0.25

    def real_rate_rising(self, d: date) -> bool:
        return self.real_ff_chg365.at(d) > 1.0

    def curve_inverted(self, d: date) -> bool:
        return self.curve_min365.at(d) < 0

    def real_m2_negative(self, d: date) -> bool:
        return self.real_m2.at(d) < 0

    def qt(self, d: date) -> bool:
        return self.walcl_yoy.at(d) < 0

    def spread_widening(self, d: date) -> bool:
        return self.baa_rise.at(d) > 0.5

    def halving_bear(self, d: date) -> bool:
        return 548 <= days_since_halving(d) < 913


_FEATURES: Features | None = None


def features() -> Features:
    global _FEATURES
    if _FEATURES is None:
        _FEATURES = Features()
    return _FEATURES


def spells(
    gate: Callable[[date], bool], a: date, b: date, gap: int = 30
) -> list[tuple[date, date]]:
    """Hostile spells between a and b: runs of hostile days, gaps under `gap` days merged, spells
    under `gap` days dropped. The count of independent episodes a result rests on."""
    out: list[list[date]] = []
    d = a
    while d <= b:
        if gate(d):
            if out and (d - out[-1][1]).days <= gap:
                out[-1][1] = d
            else:
                out.append([d, d])
        d += DAY
    return [(x, y) for x, y in out if (y - x).days >= gap]
