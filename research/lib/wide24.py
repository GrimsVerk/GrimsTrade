"""Lane wide-24: gate W40 `quake-drift` and replication R40 (research/cards/wide-24.md; rule
pushed before this script's first run).

Descriptive only: no strategy, no backtest. Nothing after 2025-10-31 is used. The cached files
(USGS ComCat, Natural Earth places, Yahoo index JSON) are untrusted downloads: run with
`python -I`.

Gate W40:     `uv run python -I research/lib/wide24.py`      (DRY=1: counts only)
Replication:  `uv run python -I research/lib/wide24.py r40`  (only after a W40 pass)
Output: research/results/quake-drift.md (and quake-drift-r40.md)
"""

from __future__ import annotations

import json
import math
import os
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import gatepower as gp  # noqa: E402
import wide24_events as ev  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)
FIRST = date(1965, 1, 1)
GATE = (date(1998, 1, 1), LAST)
REPL = (FIRST, date(1997, 12, 31))
POST_SV = date(2012, 1, 1)
USGS = "data-wide-1/usgs/2026-11-19"
PLACES = "wide-24/naturalearth/ne_10m_populated_places_simple.geojson"
YAHOO = "insure-2/raw-2026-11-18/yahoo"
GSPC = "yahoo-1d/2026-11-12/^GSPC.json"
COUNTRY = {
    "N225": "JPN", "TWII": "TWN", "MXX": "MEX", "JKSE": "IDN", "NZ50": "NZL",
    "FTSEMIB.MI": "ITA", "BSESN": "IND", "^GSPC": "USA", "KS11": "KOR", "AORD": "AUS",
    "GSPTSE": "CAN", "KLSE": "MYS", "STI": "SGP", "HSI": "HKG", "TA125.TA": "ISR",
    "AEX": "NLD", "ATX": "AUT", "BFX": "BEL", "BVSP": "BRA", "FCHI": "FRA", "FTSE": "GBR",
    "GDAXI": "DEU", "IBEX": "ESP", "OMX": "SWE", "SSMI": "CHE",
}  # fmt: skip


@dataclass(frozen=True)
class Market:
    name: str
    tz: str
    dates: np.ndarray  # local session dates (ordinals), increasing
    logc: np.ndarray


@dataclass(frozen=True)
class Pair:
    market: str
    day: int  # local date of the origin time in the market's time zone
    w: float
    s: float  # exposure, percent
    ev: ev.Event


def load_market(path: Path, name: str) -> Market:
    r = json.loads(path.read_text())["chart"]["result"][0]
    tz = r["meta"]["exchangeTimezoneName"]
    zi = ZoneInfo(tz)
    closes = r["indicators"]["quote"][0]["close"]
    by: dict[int, float] = {}
    for ts, c in zip(r["timestamp"], closes, strict=True):
        if c is None or not math.isfinite(float(c)) or float(c) <= 0:
            continue
        d = datetime.fromtimestamp(ts, zi).date()
        if d <= LAST:
            by[d.toordinal()] = float(c)
    ks = sorted(by)
    return Market(name, tz, np.array(ks), np.log(np.array([by[k] for k in ks])))


def load() -> tuple[
    list[ev.Event], dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]], dict[str, Market]
]:
    root = dw.cache_root()
    qs = dw.load_quakes(root / USGS)
    events = [ev.Event(q.time.timestamp(), q.lat, q.lon, q.depth_km, q.mag) for q in qs]
    feats = json.loads((root / PLACES).read_text())["features"]
    places: dict[str, list[tuple[float, float, float]]] = {}
    for f in feats:
        p = f["properties"]
        places.setdefault(str(p.get("adm0_a3")), []).append(
            (float(p["latitude"]), float(p["longitude"]), max(0.0, float(p.get("pop_max") or 0)))
        )
    pl = {
        c: (
            np.array([a for a, _, _ in v]),
            np.array([b for _, b, _ in v]),
            np.array([w for _, _, w in v]),
        )
        for c, v in places.items()
    }
    mk: dict[str, Market] = {}
    for name in COUNTRY:
        path = root / GSPC if name == "^GSPC" else root / YAHOO / f"{name}.json"
        mk[name] = load_market(path, name)
    return events, pl, mk


def catalogue(events: Sequence[ev.Event]) -> tuple[list[ev.Event], int]:
    lo = datetime(FIRST.year, 1, 1, tzinfo=UTC).timestamp()
    hi = datetime(LAST.year, LAST.month, LAST.day, 23, 59, 59, tzinfo=UTC).timestamp()
    sel = ev.select(events, lo, hi)
    return ev.decluster(sel), len(sel)


def pairs(
    events: Sequence[ev.Event],
    pl: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]],
    mk: dict[str, Market],
    radius: float | None = None,
    binary: bool = False,
    min_mag: float = 0.0,
) -> dict[str, list[Pair]]:
    out: dict[str, list[Pair]] = {m: [] for m in mk}
    for e in events:
        if e.mag < min_mag:
            continue
        for m, c in COUNTRY.items():
            lat, lon, pop = pl.get(c, (np.array([]), np.array([]), np.array([])))
            s = ev.exposure(e, lat, lon, pop, radius)
            if s <= 0:
                continue
            w = ev.weight(s, binary)
            if w == 0:
                continue
            day = datetime.fromtimestamp(e.time, ZoneInfo(mk[m].tz)).date().toordinal()
            out[m].append(Pair(m, day, w, s, e))
    return out


def others(mk: dict[str, Market], name: str) -> list[tuple[np.ndarray, np.ndarray]]:
    return [(m.dates, m.logc) for k, m in mk.items() if k != name]


def all_rows(mk: dict[str, Market], window: tuple[date, date], h: int = ev.H) -> dict[str, ev.Rows]:
    a, b = window[0].toordinal(), window[1].toordinal()
    out = {}
    for name, m in mk.items():
        r = ev.rows(m.dates, m.logc, others(mk, name), a, b, h)
        if len(r.s):
            out[name] = r
    return out


def doses(
    mk: dict[str, Market], rw: dict[str, ev.Rows], pr: dict[str, list[Pair]], shift: int = 0
) -> dict[str, np.ndarray]:
    return {
        n: ev.dose(len(mk[n].dates), mk[n].dates, [(p.day, p.w) for p in pr[n]], shift)[r.s]
        for n, r in rw.items()
    }


def fit(
    rw: dict[str, ev.Rows],
    dz: dict[str, np.ndarray],
    lags: int = ev.LAGS,
    outcome: str = "y",
    controls: bool = True,
) -> tuple[float, float, int]:
    """(b, Driscoll-Kraay t, rows): y on market dummies, D, r2, r20. One code path for the true
    dose, the placebos, the surrogates and the shown cells."""
    names = list(rw)
    n = sum(len(rw[k].s) for k in names)
    k = len(names)
    x = np.zeros((n, k + (3 if controls else 1)))
    y = np.zeros(n)
    per = np.zeros(n, dtype=int)
    i = 0
    for j, name in enumerate(names):
        r = rw[name]
        m = len(r.s)
        x[i : i + m, j] = 1.0
        x[i : i + m, k] = dz[name]
        if controls:
            x[i : i + m, k + 1] = r.r2
            x[i : i + m, k + 2] = r.r20
        y[i : i + m] = getattr(r, outcome)
        per[i : i + m] = r.period
        i += m
    b, t = gp.dk_fit(x, y, per, lags, k)
    return b, t, n


def day_surrogates(dz: dict[str, np.ndarray], rng: np.random.Generator) -> dict[str, np.ndarray]:
    out = {}
    for n, d in dz.items():
        s = np.zeros(len(d))
        for w in d[d != 0]:
            s[rng.integers(len(d))] += w
        out[n] = s
    return out


def iso(d: int) -> str:
    return date.fromordinal(d).isoformat()


def null_line(name: str, t: float, others_t: Sequence[float]) -> str:
    sd, share, q5, q50, q95, lo, hi = ev.null_spread(others_t)
    return (
        f"**{name}**: true t {t:+.2f}, rank {ev.rank_lowest(t, others_t)} of {len(others_t) + 1}"
        f" from the lowest; SD of the {len(others_t)} t {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" 5% {q5:+.2f}, 50% {q50:+.2f}, 95% {q95:+.2f}; smallest {lo:+.2f}, largest {hi:+.2f}."
    )


def counts(
    mk: dict[str, Market],
    rw: dict[str, ev.Rows],
    pr: dict[str, list[Pair]],
    dz: dict[str, np.ndarray],
) -> list[str]:
    lines = [
        "| Market | Rows | First row | Last row | (event, market) pairs in rows | Sum of w |",
        "|---|---:|---|---|---:|---:|",
    ]
    for n, r in rw.items():
        d = dz[n]
        lines.append(
            f"| {n} | {len(r.s)} | {iso(int(mk[n].dates[r.s[0]]))}"
            f" | {iso(int(mk[n].dates[r.s[-1]]))}"
            f" | {int(np.count_nonzero(d))} | {d.sum():.1f} |"
        )
    tot = sum(len(r.s) for r in rw.values())
    nz = sum(int(np.count_nonzero(d)) for d in dz.values())
    sw = sum(float(d.sum()) for d in dz.values())
    lines.append(f"| all | {tot} | | | {nz} | {sw:.1f} |")
    lines.append("")
    lines.append(
        "Pooled lag-1 autocorrelation of the dose (within market, row to row):"
        f" {ev.acf1([dz[n] for n in rw]):+.3f}."
    )
    return lines


def top_events(
    mk: dict[str, Market], rw: dict[str, ev.Rows], pr: dict[str, list[Pair]], k: int = 15
) -> list[str]:
    lines = [
        "| UTC origin | Market | M | depth km | S % | w | event session"
        " | y (excess, 20 sessions) |",
        "|---|---|---:|---:|---:|---:|---|---:|",
    ]
    rows_ = []
    for n, r in rw.items():
        pos = {int(s): i for i, s in enumerate(r.s)}
        for p in pr[n]:
            s = ev.first_session(mk[n].dates, p.day)
            if s in pos:
                rows_.append((p.w, n, p, s, float(r.y[pos[s]])))
    rows_.sort(key=lambda z: -z[0])
    for w, n, p, s, y in rows_[:k]:
        t = datetime.fromtimestamp(p.ev.time, UTC).strftime("%Y-%m-%d %H:%M")
        lines.append(
            f"| {t} | {n} | {p.ev.mag:.1f} | {p.ev.depth_km:.0f} | {p.s:.2f} | {w:.2f}"
            f" | {iso(int(mk[n].dates[s]))} | {y * 100:+.2f}% |"
        )
    return lines


def gate(window: tuple[date, date], label: str, out_name: str) -> None:
    events, pl, mk = load()
    ev_all, n_sel = catalogue(events)
    pr = pairs(ev_all, pl, mk)
    rw = all_rows(mk, window)
    dz = doses(mk, rw, pr)
    head = [
        f"# {label}",
        "",
        f"Card: `research/cards/wide-24.md`. Run {datetime.now(UTC):%Y-%m-%d %H:%M} UTC.",
        f"Catalogue: {n_sel} events M >= 6.0, depth <= 70 km, 1965-01-01 .. 2025-10-31;"
        f" {len(ev_all)} after declustering;"
        f" (event, market) pairs with exposure > 0: {sum(len(v) for v in pr.values())}.",
        "",
    ]
    if DRY:
        print("\n".join(head + counts(mk, rw, pr, dz)))
        return
    b, t, n = fit(rw, dz)
    plac = [fit(rw, doses(mk, rw, pr, k))[1] for k in ev.SHIFTS]
    rng = np.random.default_rng(ev.SEED)
    rnd = [fit(rw, day_surrogates(dz, rng))[1] for _ in range(40)]
    rank = ev.rank_lowest(t, plac)
    verdict = b < 0 and t <= -2 and rank <= 2
    lines = (
        head
        + counts(mk, rw, pr, dz)
        + [
            "",
            f"## Gate: b {b * 100:+.3f}% over 20 sessions per unit of dose, DK t {t:+.2f},"
            f" rows {n}, rank {rank} of 41 shifted calendars:"
            f" **{'PASS (kill-only)' if verdict else 'FAIL'}**",
            "",
            null_line("Shifted calendars (decider)", t, plac),
            "",
            null_line("Random-day surrogates (shown)", t, rnd),
            "",
            "| shift (days) | t |",
            "|---:|---:|",
            *[f"| {k} | {v:+.2f} |" for k, v in zip(ev.SHIFTS, plac, strict=True)],
            "",
            "## Shown cells (not gating)",
            "",
            "| Cell | b, % per unit | t | Rows |",
            "|---|---:|---:|---:|",
        ]
    )
    cells: list[tuple[str, float, float, int]] = [("Gate", b, t, n)]

    def add(name: str, res: tuple[float, float, int]) -> None:
        cells.append((name, *res))

    add("Reaction r2 on D, no controls, DK 5", fit(rw, dz, 5, "r2", controls=False))
    rw60 = all_rows(mk, window, 60)
    add("60-session horizon, DK 90", fit(rw60, doses(mk, rw60, pr), 90))
    add("Own return, no world subtraction", fit(rw, dz, outcome="raw"))
    add(
        "Binary dose (1 per event with S >= 1%)",
        fit(rw, doses(mk, rw, pairs(ev_all, pl, mk, binary=True))),
    )
    add("Fixed radius 100 km", fit(rw, doses(mk, rw, pairs(ev_all, pl, mk, radius=100.0))))
    add("M >= 6.5 only", fit(rw, doses(mk, rw, pairs(ev_all, pl, mk, min_mag=6.5))))
    jp = {"N225": rw["N225"]} if "N225" in rw else {}
    if jp:
        add("Japan only (N225)", fit(jp, {"N225": dz["N225"]}))
    tohoku = date(2011, 3, 11)
    ev_nt = [
        e
        for e in ev_all
        if not (datetime.fromtimestamp(e.time, UTC).date() == tohoku and e.mag >= 8.5)
    ]
    add("Without Tohoku (2011-03-11)", fit(rw, doses(mk, rw, pairs(ev_nt, pl, mk))))
    if window[1] >= POST_SV:
        rwp = all_rows(mk, (max(window[0], POST_SV), window[1]))
        add("Rows from 2012-01-01 (after Scholtens-Voorhorst)", fit(rwp, doses(mk, rwp, pr)))
    lines += [f"| {c} | {bb * 100:+.3f} | {tt:+.2f} | {nn} |" for c, bb, tt, nn in cells[1:]]
    lines += ["", "## The 15 largest-weight events in the rows", "", *top_events(mk, rw, pr)]
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / out_name).write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "r40":
        gate(REPL, "R40 quake-drift replication, 1965-1997", "quake-drift-r40.md")
    else:
        gate(GATE, "W40 quake-drift, 1998-2025", "quake-drift.md")


if __name__ == "__main__":
    main()
