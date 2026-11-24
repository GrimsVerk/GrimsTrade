"""Lane weather-2: CPC outlook-revision gate on UNG (card `research/weather-2.md`).

Descriptive gate, run once as carded. Reads (never fetches) the outlook shapefiles and the
Census centroids from `<cache_root>/weather-2/`, the CPC degree-day files and UNG train bars
from `<cache_root>/weather-1/`, XLE from the research cache.

Run: `uv run python -I research/lib/weather2_rev.py`
  DOSE=1: build and describe the dose only (no price is read)
  DRY=1: counts only, no statistic
Output: research/results/cpc-revision.md
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections.abc import Callable, Sequence
from datetime import UTC, date, datetime
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import macro  # noqa: E402
import weather1_events as ev1  # noqa: E402
import weather2_events as ev  # noqa: E402
from wide10_events import ols_hc1  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "cpc-revision.md"
DRY = bool(os.environ.get("DRY"))
DOSE_ONLY = bool(os.environ.get("DOSE"))
WINTERS = list(range(2012, 2025))  # 2012-13 .. 2024-25
HALVES = (list(range(2012, 2018)), list(range(2018, 2025)))
N_PLACEBO = 40
Perm = tuple[int, ...] | None


def gas_weights(dd: Path) -> dict[int, float]:
    conus: dict[date, float] = {}
    div: dict[int, dict[date, float]] = {k: {} for k in range(1, 10)}
    for y in range(1981, 2007):
        text = (dd / f"UtilityGas.Heating.{y}.txt").read_text()
        conus.update(ev1.parse_cpc(text))
        for k in div:
            div[k].update(ev1.parse_cpc(text, region=str(k)))
    days = sorted(d for d in conus if all(d in div[k] for k in div))
    a = np.array([[div[k][d] for k in range(1, 10)] for d in days])
    w = ev.nnls_weights(np.array([conus[d] for d in days]), a)
    return {k: float(w[k - 1]) for k in range(1, 10)}


def build_k(root: Path, weights: dict[int, float]) -> tuple[dict[str, dict[date, float]], dict]:
    """Per-lead CONUS value by issue date (Fcst_Date), and parsing notes."""
    points = ev.parse_centroids((root / "census" / "CenPop2010_Mean_ST.txt").read_text())
    val: dict[str, dict[date, float]] = {"610": {}, "814": {}}
    notes = {"files": 0, "date_mismatch": 0, "no_polygons": 0, "points": len(points)}
    for f in sorted((root / "cpc-gis").glob("*temp_*.zip")):
        lead = f.name[:3]
        fdate = datetime.strptime(f.name[8:16], "%Y%m%d").date()
        issue, polys = ev.parse_outlook_zip(f.read_bytes())
        notes["files"] += 1
        if issue is None:
            issue = fdate
        if issue != fdate:
            notes["date_mismatch"] += 1
        if issue > ev.LAST_ISSUE:
            continue
        if not polys:
            notes["no_polygons"] += 1
        val[lead][issue] = ev.conus_value(polys, points, weights)
    return val, notes


class Asset:
    def __init__(self, name: str, days: list[date], o: np.ndarray, c: np.ndarray, adj: np.ndarray):
        keep = [i for i, d in enumerate(days) if d <= harness.TRAIN_LAST_BAR]
        self.name = name
        self.days = [days[i] for i in keep]
        self.idx = {d: i for i, d in enumerate(self.days)}
        self.lo, self.lc = np.log(o[keep]), np.log(c[keep])
        self.la = np.log(adj[keep])
        self.lao = self.lo + self.la - self.lc  # open on the adjusted scale


def load_ung(path: Path) -> Asset:
    res = json.loads(path.read_text())["chart"]["result"][0]
    q = res["indicators"]["quote"][0]
    adj = res["indicators"]["adjclose"][0]["adjclose"]
    rows = [
        (datetime.fromtimestamp(t, UTC).date(), o, c, a)
        for t, o, c, a in zip(res["timestamp"], q["open"], q["close"], adj, strict=True)
        if None not in (o, c, a) and min(o, c, a) > 0
    ]
    return Asset(
        "UNG",
        [r[0] for r in rows],
        np.array([r[1] for r in rows]),
        np.array([r[2] for r in rows]),
        np.array([r[3] for r in rows]),
    )


def load_xle() -> Asset:
    bars = harness.load_history("train", syms=["XLE"])["XLE"]
    c = np.array([b.close for b in bars])
    return Asset("XLE", [b.date for b in bars], np.array([b.open for b in bars]), c, c)


Outcome = Callable[[Asset, int], float]


def y_primary(a: Asset, i: int) -> float:
    return 100.0 * float(a.lc[i] - a.lo[i])


def y_check(a: Asset, i: int) -> float:  # close of the session before t' to open of t
    return math.nan if i < 2 else 100.0 * float(a.lao[i] - a.la[i - 2])


def y_next_close(a: Asset, i: int) -> float:
    return math.nan if i + 1 >= len(a.days) else 100.0 * float(a.la[i + 1] - a.la[i])


def y_five(a: Asset, i: int) -> float:
    return math.nan if i + 4 >= len(a.days) else 100.0 * float(a.la[i + 4] - a.lao[i])


class Design:
    def __init__(self, k: dict[date, float], sessions: list[date]):
        self.x = {
            t: v
            for t, v in ev.session_doses(sessions, k).items()
            if t.month in ev.SEASON_MONTHS and ev.winter_of(t) in WINTERS
        }
        self.by_winter: dict[int, list[date]] = {}
        for t in sorted(self.x):
            self.by_winter.setdefault(ev.winter_of(t), []).append(t)

    def dose(self, t: date, perm: Perm) -> float:
        if perm is None:
            return self.x[t]
        i = WINTERS.index(ev.winter_of(t))
        s = ev.placebo_session(t, WINTERS[perm[i]], self.by_winter)
        return math.nan if s is None else self.x[s]

    def points(
        self, a: Asset, y: Outcome, perm: Perm = None, winters: Sequence[int] = WINTERS
    ) -> tuple[np.ndarray, np.ndarray]:
        xs, ys = [], []
        for t in sorted(self.x):
            if ev.winter_of(t) not in winters or t not in a.idx:
                continue
            xs.append(self.dose(t, perm) / 0.10)
            ys.append(y(a, a.idx[t]))
        return np.array(xs), np.array(ys)

    def fit(
        self, a: Asset, y: Outcome = y_primary, perm: Perm = None, **kw: object
    ) -> tuple[float, float, int]:
        x, yy = self.points(a, y, perm, **kw)  # type: ignore[arg-type]
        ok = ~(np.isnan(x) | np.isnan(yy))
        b, t = ols_hc1(x[ok], yy[ok])
        return b, t, int(ok.sum())


def combine(val: dict[str, dict[date, float]], leads: Sequence[str]) -> dict[date, float]:
    days = set.intersection(*(set(val[ld]) for ld in leads))
    return {d: -float(np.mean([val[ld][d] for ld in leads])) for d in days}


def main() -> None:
    root = macro.cache_root()
    weights = gas_weights(root / "weather-1" / "cpc-dd")
    cache = root / "weather-2" / "k-cache.json"
    if cache.exists():
        raw = json.loads(cache.read_text())
        val = {ld: {date.fromisoformat(d): v for d, v in m.items()} for ld, m in raw["val"].items()}
        notes = raw["notes"]
    else:
        val, notes = build_k(root / "weather-2", weights)
        out = {ld: {d.isoformat(): v for d, v in m.items()} for ld, m in val.items()}
        cache.write_text(json.dumps({"val": out, "notes": notes}))
    k = combine(val, ("610", "814"))
    kk = np.array([k[d] for d in sorted(k)])
    print("weights", {kw: round(v, 3) for kw, v in weights.items()})
    print("notes", notes, "issues with K", len(k), min(k), max(k))
    print(f"K mean {kk.mean():+.4f} sd {kk.std():.4f}; share zero {np.mean(kk == 0):.2%}")
    if DOSE_ONLY:
        return

    ung = load_ung(root / "weather-1" / "yahoo" / "UNG.json")
    design = Design(k, ung.days)
    perms = ev1.derangements(len(WINTERS), N_PLACEBO)
    if DRY:
        x, _ = design.points(ung, y_primary)
        print("UNG bars", len(ung.days), ung.days[0], ung.days[-1])
        print("sessions with dose", len(design.x), "per winter",
              {w: len(v) for w, v in design.by_winter.items()})  # fmt: skip
        print("x sd (units of 0.10)", float(np.nanstd(x)))
        print("placebo sizes", min(int((~np.isnan(design.points(ung, y_primary, p)[0])).sum())
                                   for p in perms))  # fmt: skip
        return

    def placebo_rank(a: Asset, y: Outcome, d: Design = design) -> tuple[int, list[float]]:
        t0 = d.fit(a, y)[1]
        pl = [d.fit(a, y, p)[1] for p in perms]
        return 1 + sum(1 for v in pl if v > t0), pl

    b, t, n = design.fit(ung)
    rank, pl = placebo_rank(ung, y_primary)
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

    xle = load_xle()
    d610 = Design(combine(val, ("610",)), ung.days)
    d814 = Design(combine(val, ("814",)), ung.days)
    shown: list[tuple[str, tuple[float, float, int], int]] = []
    for name, a, y, d in [
        ("UNG dose check: close before t' to open t (not tradable)", ung, y_check, design),
        ("UNG close t to close t+1", ung, y_next_close, design),
        ("UNG open t to close t+4 (overlapping)", ung, y_five, design),
        ("UNG primary, 6-10 day outlook only", ung, y_primary, d610),
        ("UNG primary, 8-14 day outlook only", ung, y_primary, d814),
        ("XLE primary", xle, y_primary, design),
    ]:
        shown.append((name, d.fit(a, y), placebo_rank(a, y, d)[0]))
    x, y = design.points(ung, y_primary)
    lo, hi = np.quantile(x, [0.2, 0.8])
    top, bot = float(y[x >= hi].mean()), float(y[x <= lo].mean())

    wtxt = ", ".join(f"{kw}: {v:.3f}" for kw, v in weights.items())
    L = [
        "# CPC outlook revisions and next-session natural gas: gate (weather-2)",
        "",
        "Rule: `research/weather-2.md` (card pushed before any price was loaded). Script",
        "`research/lib/weather2_rev.py`. Dose: change in the gas-weighted cold-outlook index K",
        "(mean of the 6-10 and 8-14 day CPC outlooks, signed tercile probability minus 1/3, at",
        "state population centroids) between the latest issues before session t and before the",
        "previous session. y: UNG open-to-close of session t, in percent. Slope in percentage",
        "points per 0.10 of K, HC1 t. Winters 2012-13 .. 2024-25, train bars only.",
        "",
        f"Gas weights by Census division (NNLS 1981-2006, sum 1): {wtxt}.",
        f"Outlook files parsed {notes['files']}, Fcst_Date differing from the file name"
        f" {notes['date_mismatch']}, files without polygons {notes['no_polygons']}, points"
        f" {notes['points']}. Issues with K: {len(k)}.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Slope (t, n) | {b:+.3f} ({t:+.2f}, {n}) | > 0, t >= 2 | {gate['b > 0, t >= 2']} |",
        f"| Rank of t among 41 (1 = highest) | {rank} | <= 2 | {gate['rank <= 2 of 41']} |",
        f"| Slope 2012-17 / 2018-24 winters (t, n) | {halves[0][0]:+.3f} ({halves[0][1]:+.2f},"
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
        "| Cell | Slope per 0.10 (t, n) | Rank of t among 41 |",
        "|---|---:|---:|",
    ]
    for name, (sb, st, sn), r in shown:
        L.append(f"| {name} | {sb:+.3f} ({st:+.2f}, {sn}) | {r} |")
    L += [
        "",
        f"UNG mean y, top quintile of x (colder revisions) {top:+.3f}%, bottom {bot:+.3f}%.",
        f"x: mean {np.nanmean(x) * 0.1:+.4f}, SD {np.nanstd(x, ddof=1) * 0.1:.4f} (K units);"
        f" y: mean {np.nanmean(y):+.3f}%, SD {np.nanstd(y, ddof=1):.3f}%.",
        "",
    ]
    OUT.write_text("\n".join(L))
    print("\n".join(L))


if __name__ == "__main__":
    main()
