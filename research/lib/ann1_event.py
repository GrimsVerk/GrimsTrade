"""Lane ann-1: descriptive event study of returns around scheduled FOMC announcements.

No strategy, no backtest, no `tries.md` row. The decision rule (gate statistic and window) is in
`research/ann-1.md` and was pushed before this script was first run.

Inputs (read as data only, json.load):
- `<cache_root>/derived/survey-2/fomc.csv`: day 0 of each scheduled meeting (statement day).
- `<cache_root>/yahoo-1d/2026-11-12/<SYM>.json`: daily bars; opens are scaled by
  adjclose / close so every window is a total return.
- `<cache_root>/alpaca/1m-sip/SPY/<YYYY-MM>.json`: SPY minute bars 2016 on (raw prices), for
  the 2 pm to 2 pm window (price = close of the last regular bar starting before 13:55 ET).

No bar after 2025-11-09 (end of train) is read. Output: `research/results/ann-1.md`.

Run: `python -I research/lib/ann1_event.py` (with research/macro.local.json present).
"""

from __future__ import annotations

import csv
import json
import math
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import macro  # noqa: E402

LAST = date(2025, 11, 9)  # end of train; nothing later is read
NY = ZoneInfo("America/New_York")
SNAP = "2026-11-12"
CUT = time(13, 55)

# Windows by day 0 (inclusive). "after" is the gate window of research/ann-1.md.
WINDOWS: list[tuple[str, date, date]] = [
    ("1994-02..2011-03 (Lucca-Moench sample)", date(1994, 1, 1), date(2011, 3, 31)),
    ("2011-04..2014-12 (post-sample, pre-journal)", date(2011, 4, 1), date(2014, 12, 31)),
    ("2015-01..2025-11 (after publication; GATE)", date(2015, 1, 1), LAST),
    ("  of which 2015-2019", date(2015, 1, 1), date(2019, 12, 31)),
    ("  of which 2020-2025/11", date(2020, 1, 1), LAST),
]


@dataclass(frozen=True)
class Series:
    days: list[date]
    opens: np.ndarray  # total-return scaled
    closes: np.ndarray  # total-return (adjclose)


@dataclass(frozen=True)
class Stat:
    n: int
    mean_event: float
    mean_other: float
    diff: float
    t: float


def welch(a: Sequence[float], b: Sequence[float]) -> Stat:
    """Mean of `a` minus mean of `b`, with Welch's t. NaN t if either side has < 2 values."""
    x = np.asarray(a, dtype=float)
    y = np.asarray(b, dtype=float)
    if len(x) < 2 or len(y) < 2:
        mx = float(x.mean()) if len(x) else math.nan
        my = float(y.mean()) if len(y) else math.nan
        return Stat(len(x), mx, my, mx - my, math.nan)
    d = float(x.mean() - y.mean())
    se = math.sqrt(x.var(ddof=1) / len(x) + y.var(ddof=1) / len(y))
    return Stat(len(x), float(x.mean()), float(y.mean()), d, d / se if se > 0 else math.nan)


def window_returns(s: Series, kind: str) -> tuple[list[date], np.ndarray]:
    """For each index i, the return of window `kind` keyed by the day that would be day 0.

    - `cc0`: close i-1 -> close i (day 0's close-to-close; the gate statistic).
    - `cc-1`: close i-2 -> close i-1 (the day before day 0).
    - `oo0`: open i -> open i+1 (bought at day 0's open, sold at day +1's open).
    - `oo-1`: open i-1 -> open i+1 (bought at day -1's open, sold at day +1's open).
    Indices where the window does not fit are left out.
    """
    o, c, n = s.opens, s.closes, len(s.days)
    keys: list[date] = []
    vals: list[float] = []
    for i in range(n):
        if kind == "cc0" and i >= 1:
            v = c[i] / c[i - 1] - 1
        elif kind == "cc-1" and i >= 2:
            v = c[i - 1] / c[i - 2] - 1
        elif kind == "oo0" and i + 1 < n:
            v = o[i + 1] / o[i] - 1
        elif kind == "oo-1" and i >= 1 and i + 1 < n:
            v = o[i + 1] / o[i - 1] - 1
        else:
            continue
        keys.append(s.days[i])
        vals.append(float(v))
    return keys, np.asarray(vals)


def split(
    keys: Sequence[date], vals: np.ndarray, events: set[date], lo: date, hi: date
) -> tuple[list[float], list[float]]:
    """Values whose key is a day 0 in [lo, hi], and all other values in [lo, hi]."""
    ev: list[float] = []
    ot: list[float] = []
    for k, v in zip(keys, vals, strict=True):
        if lo <= k <= hi and math.isfinite(v):
            (ev if k in events else ot).append(float(v))
    return ev, ot


def price_before(bars: Sequence[tuple[datetime, float]], day: date, cut: time = CUT) -> float:
    """Close of the last regular-session bar of `day` (ET) that starts before `cut`, else NaN.
    `bars` are (start time in ET, close), sorted."""
    best = math.nan
    for t, c in bars:
        if t.date() == day and time(9, 30) <= t.time() < cut:
            best = c
    return best


# ---------------------------------------------------------------- data access (not tested)


def fomc_days() -> list[date]:
    path = macro.cache_root() / "derived" / "survey-2" / "fomc.csv"
    with path.open() as f:
        return [date.fromisoformat(r["day0"]) for r in csv.DictReader(f)]


def load_yahoo(sym: str) -> Series:
    path = macro.cache_root() / "yahoo-1d" / SNAP / f"{sym}.json"
    r = json.loads(path.read_text())["chart"]["result"][0]
    q = r["indicators"]["quote"][0]
    adj = r["indicators"]["adjclose"][0]["adjclose"]
    days: list[date] = []
    opens: list[float] = []
    closes: list[float] = []
    for ts, o, c, a in zip(r["timestamp"], q["open"], q["close"], adj, strict=True):
        d = datetime.fromtimestamp(ts, tz=UTC).date()
        if d > LAST or o is None or c is None or a is None or c <= 0:
            continue
        days.append(d)
        opens.append(o * a / c)
        closes.append(a)
    return Series(days, np.asarray(opens), np.asarray(closes))


def minute_prices(days: Sequence[date]) -> dict[date, float]:
    """SPY price just before 13:55 ET on each of `days` from 2016 on (minute cache)."""
    root = macro.cache_root() / "alpaca" / "1m-sip" / "SPY"
    months = sorted({(d.year, d.month) for d in days if d.year >= 2016})
    out: dict[date, float] = {}
    for y, m in months:
        path = root / f"{y:04d}-{m:02d}.json"
        if not path.exists():
            continue
        bars: list[tuple[datetime, float]] = []
        for page in json.loads(path.read_text()):
            for b in page["bars"].get("SPY", []):
                t = datetime.fromisoformat(b["t"].replace("Z", "+00:00")).astimezone(NY)
                if t.date() <= LAST:
                    bars.append((t, float(b["c"])))
        by_day: dict[date, list[tuple[datetime, float]]] = {}
        for t, c in bars:
            by_day.setdefault(t.date(), []).append((t, c))
        for d, bs in by_day.items():
            p = price_before(sorted(bs), d)
            if math.isfinite(p):
                out[d] = p
    return out


def fmt(st: Stat) -> str:
    return (
        f"{st.n} | {st.mean_event * 1e4:+.1f} | {st.mean_other * 1e4:+.1f} | "
        f"{st.diff * 1e4:+.1f} | {st.t:+.2f}"
    )


LABELS = {
    "cc0": "day 0 close-to-close",
    "cc-1": "day -1 close-to-close",
    "oo0": "open day 0 -> open day +1",
    "oo-1": "open day -1 -> open day +1",
}


def main() -> None:
    events = set(fomc_days())
    lines = [
        "# Ann 1: FOMC event study (descriptive, no strategy)",
        "",
        "Generated by `research/lib/ann1_event.py`. Scheduled FOMC statement days (day 0) from",
        "survey-2's calendar; bars to 2025-11-09. Returns in bps; `other` = every other trading",
        "day (or window start) in the same years; t = Welch. Gate (research/ann-1.md): SPY,",
        "day 0 close-to-close, 2015-01..2025-11, FOMC minus other > 0 with t >= 2.",
        "",
    ]
    gate: Stat | None = None
    for sym in ("SPY", "^GSPC", "TLT", "BTC-USD"):
        s = load_yahoo(sym)
        lines += [f"## {sym} (from {s.days[0]})", ""]
        lines += ["| Window | Statistic | FOMC days | FOMC mean | Other mean | Diff | t |"]
        lines += ["|---|---|---:|---:|---:|---:|---:|"]
        kinds = ("cc0", "cc-1") if sym == "^GSPC" else ("cc0", "cc-1", "oo0", "oo-1")
        for kind in kinds:
            keys, vals = window_returns(s, kind)
            for name, lo, hi in WINDOWS:
                if hi < s.days[0]:
                    continue
                st = welch(*split(keys, vals, events, lo, hi))
                lines.append(f"| {name} | {LABELS[kind]} | {fmt(st)} |")
                if sym == "SPY" and kind == "cc0" and "GATE" in name:
                    gate = st
        lines.append("")

    spy = load_yahoo("SPY")
    px = minute_prices(spy.days)
    keys2: list[date] = []
    vals2: list[float] = []
    for i in range(1, len(spy.days)):
        a, b = spy.days[i - 1], spy.days[i]
        if a in px and b in px:
            keys2.append(b)
            vals2.append(px[b] / px[a] - 1)
    lines += [
        "## SPY, 2 pm to 2 pm (13:55 ET to 13:55 ET; minute bars, raw prices)",
        "",
        "Lucca and Moench's own window, ending just before the 2 pm statement.",
        "",
        "| Window | FOMC days | FOMC mean | Other mean | Diff | t |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    arr2 = np.asarray(vals2)
    for name, lo, hi in [
        ("2016-01..2025-11", date(2016, 1, 1), LAST),
        ("  of which 2016-2019", date(2016, 1, 1), date(2019, 12, 31)),
        ("  of which 2020-2025/11", date(2020, 1, 1), LAST),
    ]:
        lines.append(f"| {name} | {fmt(welch(*split(keys2, arr2, events, lo, hi)))} |")
    lines.append("")

    assert gate is not None
    passed = gate.diff > 0 and gate.t >= 2
    lines += [
        "## Gate",
        "",
        f"SPY day 0 close-to-close, 2015-01..2025-11: {gate.n} meetings, FOMC minus other "
        f"{gate.diff * 1e4:+.1f} bps, t {gate.t:+.2f}. Rule met: {'yes' if passed else 'no'}.",
        "",
    ]
    out = macro.RESEARCH / "results" / "ann-1.md"
    out.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
