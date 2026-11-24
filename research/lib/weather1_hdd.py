"""Lane weather-1: HDD-surprise gate on next-week UNG returns (card `research/weather-1.md`).

Descriptive gate, run once as carded. Reads (never fetches) the CPC files and UNG train bars
from `<cache_root>/weather-1/` (`research/macro.local.json`). XLE from the research cache.

Run: `uv run python -I research/lib/weather1_hdd.py`  (DRY=1: counts only, no statistic)
Output: research/results/hdd-gas.md
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections.abc import Sequence
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import macro  # noqa: E402
import weather1_events as ev  # noqa: E402
from wide10_events import ols_hc1  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "hdd-gas.md"
DRY = bool(os.environ.get("DRY"))
WINTERS = list(range(2007, 2025))  # 2007-08 .. 2024-25
HALVES = (list(range(2007, 2016)), list(range(2016, 2025)))
N_PLACEBO = 40
Perm = tuple[int, ...] | None


def load_hdd(folder: Path) -> dict[date, float]:
    hdd: dict[date, float] = {}
    for y in range(1981, 2026):
        hdd.update(ev.parse_cpc((folder / f"UtilityGas.Heating.{y}.txt").read_text()))
    return hdd


class Asset:
    def __init__(self, name: str, days: list[date], close: np.ndarray):
        keep = [i for i, d in enumerate(days) if d <= harness.TRAIN_LAST_BAR]
        self.name = name
        self.days = [days[i] for i in keep]
        self.logc = np.log(close[keep])


def load_ung(path: Path) -> Asset:
    res = json.loads(path.read_text())["chart"]["result"][0]
    ts = res["timestamp"]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    pairs = [
        (datetime.fromtimestamp(t, UTC).date(), float(c))
        for t, c in zip(ts, adj, strict=True)
        if c is not None and c > 0
    ]
    return Asset("UNG", [p[0] for p in pairs], np.array([p[1] for p in pairs]))


def load_harness(sym: str) -> Asset:
    bars = harness.load_history("train", syms=[sym])[sym]
    return Asset(sym, [b.date for b in bars], np.array([b.close for b in bars]))


class Design:
    def __init__(self, hdd: dict[date, float]):
        cache: dict[date, float] = {}
        self.fridays = ev.season_fridays(WINTERS[0], WINTERS[-1])
        self.x = {f: ev.dose(hdd, f, cache) for f in self.fridays}
        self.by_winter: dict[int, list[date]] = {}
        for f in self.fridays:
            self.by_winter.setdefault(ev.winter_of(f), []).append(f)

    def dose(self, f: date, perm: Perm) -> float:
        if perm is None:
            return self.x[f]
        i = WINTERS.index(ev.winter_of(f))
        g = ev.placebo_friday(f, WINTERS[perm[i]], self.by_winter)
        return math.nan if g is None else self.x[g]

    def points(
        self,
        a: Asset,
        perm: Perm = None,
        winters: Sequence[int] = WINTERS,
        hold: int = ev.HOLD,
        same_week: bool = False,
    ) -> tuple[np.ndarray, np.ndarray]:
        xs, ys = [], []
        for f in self.fridays:
            if ev.winter_of(f) not in winters:
                continue
            ij = (
                ev.same_week_bars(a.days, f)
                if same_week
                else ev.entry_exit(a.days, f, harness.TRAIN_LAST_BAR, hold)
            )
            x = self.dose(f, perm)
            if ij is None or math.isnan(x):
                continue
            xs.append(x / 10.0)  # per 10 degree days
            ys.append(100.0 * float(a.logc[ij[1]] - a.logc[ij[0]]))  # percentage points
        return np.array(xs), np.array(ys)

    def fit(self, a: Asset, perm: Perm = None, **kw: object) -> tuple[float, float, int]:
        x, y = self.points(a, perm, **kw)  # type: ignore[arg-type]
        b, t = ols_hc1(x, y)
        return b, t, len(x)


def quintile_means(x: np.ndarray, y: np.ndarray) -> tuple[float, float]:
    lo, hi = np.quantile(x, [0.2, 0.8])
    return float(y[x >= hi].mean()), float(y[x <= lo].mean())


def main() -> None:
    root = macro.cache_root() / "weather-1"
    hdd = load_hdd(root / "cpc-dd")
    design = Design(hdd)
    ung = load_ung(root / "yahoo" / "UNG.json")
    perms = ev.derangements(len(WINTERS), N_PLACEBO)
    if DRY:
        x, _ = design.points(ung)
        print("hdd days", len(hdd), min(hdd), max(hdd))
        print("UNG bars", len(ung.days), ung.days[0], ung.days[-1])
        print("season fridays", len(design.fridays), "weeks with y", len(x))
        print("placebo sizes", min(len(design.points(ung, p)[0]) for p in perms))
        return

    b, t, n = design.fit(ung)
    pl = [design.fit(ung, p)[1] for p in perms]
    rank = 1 + sum(1 for v in pl if v > t)
    halves = [design.fit(ung, winters=h) for h in HALVES]
    gate = {
        "b > 0, t >= 2": b > 0 and t >= 2,
        "rank <= 2 of 41": rank <= 2,
        "b > 0 both halves": all(h[0] > 0 for h in halves),
    }
    arr = np.array(pl)
    q = np.quantile(arr, [0.05, 0.5, 0.95])
    sd = float(arr.std(ddof=1))
    share = float(np.mean(np.abs(arr) >= 2))

    xle = load_harness("XLE")
    shown = [
        ("UNG dose week (same-week check)", design.fit(ung, same_week=True)),
        ("UNG next 10 sessions", design.fit(ung, hold=10)),
        ("XLE next 5 sessions", design.fit(xle)),
        ("XLE dose week (same-week check)", design.fit(xle, same_week=True)),
    ]
    x, y = design.points(ung)
    cold, warm = quintile_means(x, y)

    L = [
        "# HDD surprise and next-week natural gas: gate (weather-1)",
        "",
        "Rule: `research/weather-1.md` (pushed before any return data was loaded). Script",
        "`research/lib/weather1_hdd.py`. Dose: CPC CONUS utility-gas-weighted HDD, 7 days to",
        "Friday, minus a rolling 20-year +-7-day normal. y: UNG log return, close of the first",
        "session on/after Friday + 4 days to 5 sessions later. Slope in percentage points per",
        "10 degree days, HC1 t. Winters 2007-08 .. 2024-25, train bars only.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Slope (t, n) | {b:+.3f} ({t:+.2f}, {n}) | > 0, t >= 2 | {gate['b > 0, t >= 2']} |",
        f"| Rank of t among 41 (1 = highest) | {rank} | <= 2 | {gate['rank <= 2 of 41']} |",
        f"| Slope 2007-15 / 2016-24 winters (t, n) | {halves[0][0]:+.3f} ({halves[0][1]:+.2f},"
        f" {halves[0][2]}) / {halves[1][0]:+.3f} ({halves[1][1]:+.2f}, {halves[1][2]}) |"
        f" both > 0 | {gate['b > 0 both halves']} |",
        "",
        f"**Gate: {'pass' if all(gate.values()) else 'fail'}.**",
        "",
        "## Placebo null (40 winter derangements)",
        "",
        f"SD of placebo t {sd:.2f}; share |t| >= 2 {share:.0%}; 5/50/95% {q[0]:+.2f} /"
        f" {q[1]:+.2f} / {q[2]:+.2f}; min {arr.min():+.2f}, max {arr.max():+.2f}.",
        "",
        "Placebo t, in draw order: " + ", ".join(f"{v:+.2f}" for v in pl),
        "",
        "## Shown (carded, not gating)",
        "",
        "| Cell | Slope per 10 DD (t, n) |",
        "|---|---:|",
    ]
    for name, (sb, st, sn) in shown:
        L.append(f"| {name} | {sb:+.3f} ({st:+.2f}, {sn}) |")
    L += [
        "",
        f"UNG next-week mean y, coldest quintile of x {cold:+.2f}%, warmest {warm:+.2f}%.",
        f"x: mean {x.mean() * 10:+.1f} DD, SD {x.std(ddof=1) * 10:.1f} DD;"
        f" y: mean {y.mean():+.2f}%, SD {y.std(ddof=1):.2f}%.",
        "",
    ]
    OUT.write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
