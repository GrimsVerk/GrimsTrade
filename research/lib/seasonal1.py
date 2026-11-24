"""seasonal-1: `seasonal-20y` as an overlay on `tsmom12` and standalone. Card:
research/cards/seasonal-20y.md (pushed before any number).

    uv run python -I research/lib/seasonal1.py --dry   # counts only, nothing run or logged
    uv run python -I research/lib/seasonal1.py         # the one real run

Data (cache root from research/macro.local.json or GRIMSTRADE_DATA; read only): Ken French
daily market and 10 industries; insure-2's 13 Yahoo developed-market indices; the harness's six
assets with ^GSPC, ^IXIC and ^TNX as season proxies. Nothing after 2025-11-10 is parsed. Rows go
to research/tries.md the moment a configuration runs; a configuration whose equity file exists
under research/data/runs/ is re-scored without a new row. Writes research/results/seasonal-1.md.
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import seasonal1_rules as sr  # noqa: E402
import stats  # noqa: E402
import trend_1926 as t  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade import gym  # noqa: E402
from grimstrade.data import ETF, UNIVERSE, Bar  # noqa: E402

IDEA = "seasonal-20y"
OUT = harness.RESEARCH / "results" / "seasonal-1.md"
LAST = harness.TRAIN_LAST_BAR
END = harness.TRAIN_END
COST = 0.0002
FRENCH = "french/2026-11-12"
GEO_RAW = "insure-2/raw-2026-11-18/yahoo"
PROXY_RAW = "yahoo-1d/2026-11-12"
GEO = {
    "N225": "Japan", "GSPTSE": "Canada", "FTSE": "UK", "AORD": "Australia", "HSI": "HongKong",
    "GDAXI": "Germany", "STI": "Singapore", "FCHI": "France", "SSMI": "Switzerland",
    "BFX": "Belgium", "AEX": "Netherlands", "ATX": "Austria", "IBEX": "Spain",
}  # fmt: skip
PROXIES = {"SPY": ("^GSPC", "price"), "QQQ": ("^IXIC", "price"), "TLT": ("^TNX", "yield")}
SPLITS = (("1981", date(1981, 1, 1)), ("2008", date(2008, 1, 1)))
DRAWS, BLOCK = 2000, 8.0
BAR_Z, BAR_Z_LOW = 4.69, 3.29
STRATS = ("overlay", "alone", "tsmom12", "hold")


# --- loaders (raw cache, read only) ---


def load_yahoo(path: Path) -> tuple[list[date], list[float]]:
    """Daily closes (local trading day) up to LAST."""
    res = json.loads(path.read_text())["chart"]["result"][0]
    off = int(res["meta"].get("gmtoffset") or 0)
    closes: dict[date, float] = {}
    for ts, cl in zip(res["timestamp"], res["indicators"]["quote"][0]["close"], strict=True):
        if cl is None or cl <= 0:
            continue
        d = datetime.fromtimestamp(ts + off, UTC).date()
        if d <= LAST:
            closes[d] = float(cl)
    days = sorted(closes)
    return days, [closes[d] for d in days]


def returns_of(closes: Sequence[float]) -> np.ndarray:
    px = np.asarray(closes, dtype=float)
    r = np.zeros(len(px))
    r[1:] = px[1:] / px[:-1] - 1
    return r


def load_french(root: Path) -> tuple[list[date], dict[str, np.ndarray]]:
    snap = root / FRENCH
    fac = t.parse_factors(t._lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), LAST)
    ind = t.parse_industries(t._lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), LAST)
    days = sorted(set(fac) & set(ind))
    out = {"Mkt": np.array([fac[d][0] for d in days])}
    for j, n in enumerate(t.INDUSTRIES):
        out[n] = np.array([ind[d][j] for d in days])
    return days, out


# --- universes ---


@dataclass
class Test:
    name: str
    hist: dict[str, list[Bar]]
    seasons: dict[str, sr.Season]
    live: sr.Live
    start: date
    costs: Mapping[str, gym.Costs]
    primary: bool = False


LONG_COSTS = {**gym.COSTS, ETF: gym.Costs(fee=0.0, slip=COST)}


def long_test(
    name: str, series: Mapping[str, tuple[Sequence[date], np.ndarray]], late: bool
) -> Test:
    hist: dict[str, list[Bar]] = {}
    seasons: dict[str, sr.Season] = {}
    for label, (days, ret) in series.items():
        sym = f"S1-{label}"
        UNIVERSE[sym] = ETF  # research process only; src/ is untouched
        bars = t.bars(days, ret, late)
        hist[sym] = bars
        seasons[sym] = sr.season_of([b.date for b in bars], [b.close for b in bars])
    first = min(min(s.on) for s in seasons.values() if s.on)
    start = date(first // 12, first % 12 + 1, 1) - timedelta(days=7)
    return Test(name, hist, seasons, sr.signal_live(seasons), start, LONG_COSTS)


def proxy_season(root: Path, ticker: str, kind: str) -> sr.Season:
    days, closes = load_yahoo(root / PROXY_RAW / f"{ticker}.json")
    px, when = sr.month_ends(days, closes)
    r = sr.yield_to_bond(px) if kind == "yield" else sr.monthly_logret(px)
    return sr.Season(sr.season_table(r), when)


def primary_test(root: Path) -> Test:
    hist = harness.load_history("train")
    seasons = {s: proxy_season(root, tk, kind) for s, (tk, kind) in PROXIES.items()}
    return Test("six", hist, seasons, sr.proto_live, harness.TRAIN_START, gym.COSTS, True)


def tests(root: Path) -> list[Test]:
    days, fr = load_french(root)
    out = [
        long_test("US-ind10", {n: (days, fr[n]) for n in t.INDUSTRIES}, False),
        long_test("US-Mkt", {"Mkt": (days, fr["Mkt"])}, False),
    ]
    out += [long_test(f"US-{n}", {n: (days, fr[n])}, False) for n in t.INDUSTRIES]
    out.append(long_test("US-ind10-late", {n: (days, fr[n]) for n in t.INDUSTRIES}, True))
    geo = {}
    for tk, n in GEO.items():
        d, cl = load_yahoo(root / GEO_RAW / f"{tk}.json")
        geo[n] = (d, returns_of(cl))
    out.append(long_test("geo13", geo, False))
    out += [long_test(f"geo-{n}", {n: geo[n]}, False) for n in GEO.values()]
    out.append(primary_test(root))
    return out


# --- runs ---


def strategy(name: str, te: Test) -> harness.ResearchStrategy:
    if name == "overlay":
        return sr.overlay(te.seasons, te.live)
    if name == "alone":
        return sr.alone(te.seasons, te.live)
    if name == "tsmom12":
        return sr.tsmom(te.live)
    return sr.hold(te.live)


def variant(name: str, te: Test) -> str:
    base = {"overlay": "seasonal-20y-overlay", "alone": "seasonal-20y-alone"}.get(name, name)
    return base if te.primary else f"{base}@{te.name}"


def kind_of(name: str, te: Test) -> str:
    if not te.primary:
        return "robustness"
    return "variant" if name in ("overlay", "alone") else "baseline"


def run_all(te: Test) -> dict[str, harness.Run]:
    panel = harness.Panel(te.hist)
    out = {}
    for name in STRATS:
        v = variant(name, te)
        done = (harness.DATA / "runs" / IDEA / f"{v}.train.csv").exists()
        out[name] = harness.run(
            IDEA, v, strategy(name, te), kind=kind_of(name, te), period="train",
            panel=panel, history=te.hist, start=te.start, end=END, costs=te.costs, log=not done,
        )  # fmt: skip
    return out


# --- statistics ---


def weekly(run: harness.Run) -> tuple[np.ndarray, np.ndarray]:
    """Friday-to-Friday returns from the calendar equity: (ordinal of the end Friday, return)."""
    idx = [i for i, d in enumerate(run.days) if d.weekday() == 4]
    eq = run.equity[idx]
    ords = np.array([run.days[i].toordinal() for i in idx[1:]], dtype=np.int64)
    return ords, eq[1:] / eq[:-1] - 1


def wsharpe(r: np.ndarray) -> float:
    sd = r.std()
    return float(r.mean() / sd * math.sqrt(52)) if sd > 0 else 0.0


@dataclass
class Diff:
    a: float
    b: float
    d: float
    se: float
    weeks: int

    @property
    def z(self) -> float:
        return self.d / self.se if self.se > 0 else 0.0


def paired(a: np.ndarray, b: np.ndarray) -> Diff | None:
    if len(a) < 52:
        return None
    rng = np.random.default_rng(0)
    ds = np.empty(DRAWS)
    for k in range(DRAWS):
        i = stats._stationary_indices(len(a), BLOCK, rng)
        ds[k] = wsharpe(a[i]) - wsharpe(b[i])
    return Diff(wsharpe(a), wsharpe(b), wsharpe(a) - wsharpe(b), float(ds.std()), len(a))


def windows() -> list[tuple[str, date, date]]:
    w = [("whole", date.min, date.max)]
    for lab, cut in SPLITS:
        w += [(f"before {lab}", date.min, cut), (f"from {lab}", cut, date.max)]
    return w


def compare(runs: Mapping[str, harness.Run], a: str, b: str) -> dict[str, Diff | None]:
    oa, ra = weekly(runs[a])
    ob, rb = weekly(runs[b])
    common = np.intersect1d(oa, ob)
    ra, rb = ra[np.isin(oa, common)], rb[np.isin(ob, common)]
    out: dict[str, Diff | None] = {}
    for lab, lo, hi in windows():
        m = (common >= lo.toordinal()) & (common < hi.toordinal())
        out[lab] = paired(ra[m], rb[m])
    return out


def label(c: Mapping[str, Diff | None]) -> str:
    """The card's reading of one comparison."""
    w, e, late, post = c["whole"], c["before 1981"], c["from 1981"], c["from 2008"]
    if w and w.z >= 1.645 and all(x and x.d > 0 for x in (e, late, post)):
        return "present"
    if e and e.z >= 1.645 and late and (late.d <= 0 or late.z < 1):
        return "early only"
    if w and w.z < 1.645:
        return "absent"
    return "mixed"


# --- placebo (monthly arithmetic, US book) ---


def placebo(days: Sequence[date], fr: Mapping[str, np.ndarray]) -> list[tuple[int, float, int]]:
    """Standalone minus hold, annualised monthly Sharpe, for shifts s = 0 (true) .. 10."""
    rs, simple = {}, {}
    for n in t.INDUSTRIES:
        px, _ = sr.month_ends(days, list(np.cumprod(1 + np.nan_to_num(fr[n]))))
        rs[n] = sr.monthly_logret(px)
        simple[n] = {k: math.expm1(v) for k, v in rs[n].items()}
    true = {n: sr.season_table(rs[n]) for n in t.INDUSTRIES}
    last = sr.key(date(2025, 10, 1))  # last complete holding month
    months = sorted({m for n in t.INDUSTRIES for m in true[n] if m <= last})
    out = []
    for s in range(11):
        tab = true if s == 0 else {n: sr.season_table(rs[n], s) for n in t.INDUSTRIES}
        a, b = [], []
        for m in months:
            live = [n for n in t.INDUSTRIES if m in true[n] and m in simple[n]]
            if not live:
                continue
            a.append(sum(simple[n][m] for n in live if tab[n].get(m, True)) / len(live))
            b.append(sum(simple[n][m] for n in live) / len(live))
        x, y = np.array(a), np.array(b)
        sh = (x.mean() / x.std() - y.mean() / y.std()) * math.sqrt(12)
        out.append((s, float(sh), len(x)))
    return out


# --- report ---


def fd(x: Diff | None) -> str:
    if x is None:
        return "- | - | - | - | -"
    return f"{x.a:.2f} | {x.b:.2f} | {x.d:+.2f} | {x.se:.2f} | {x.z:+.2f} ({x.weeks})"


def table(rows: list[tuple[str, dict[str, Diff | None]]]) -> list[str]:
    out = [
        "| Test | Window | Rule | Comparator | Difference | SE | z (weeks) |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for name, c in rows:
        for lab, x in c.items():
            out.append(f"| {name} | {lab} | {fd(x)} |")
    return out


def dry(ts: Sequence[Test]) -> None:
    for te in ts:
        firsts = [min(s.on) for s in te.seasons.values() if s.on]
        f = min(firsts) if firsts else None
        n_sig = sum(len(s.on) for s in te.seasons.values())
        print(f"{te.name}: {len(te.hist)} assets, {len(te.seasons)} with a season, "
              f"first holding month {f and (f // 12, f % 12 + 1)}, {n_sig} asset-months, "
              f"start {te.start}")  # fmt: skip


def main() -> None:
    root = cache_root()
    ts = tests(root)
    if "--dry" in sys.argv:
        dry(ts)
        return
    over: list[tuple[str, dict[str, Diff | None]]] = []
    solo: list[tuple[str, dict[str, Diff | None]]] = []
    expo: list[str] = []
    labels: list[str] = []
    for te in ts:
        runs = run_all(te)
        co, ca = compare(runs, "overlay", "tsmom12"), compare(runs, "alone", "hold")
        over.append((te.name, co))
        solo.append((te.name, ca))
        e = {k: r.exposure for k, r in runs.items()}
        expo.append(
            f"| {te.name} | {te.start} | " + " | ".join(f"{e[k]:.0%}" for k in STRATS) + " |"
        )
        labels.append(f"| {te.name} | {label(ca)} | {label(co)} |")
        print(te.name, "done", flush=True)
    days, fr = load_french(root)
    pl = placebo(days, fr)
    lines = [
        "# seasonal-1: `seasonal-20y` results",
        "",
        "Card `cards/seasonal-20y.md`; script `lib/seasonal1.py` (one real run). Sharpe on "
        "weekly returns, annualised; difference = rule minus comparator on the same weeks; SE "
        f"from {DRAWS} paired stationary-bootstrap draws (mean block {BLOCK:.0f} weeks, seed 0).",
        "",
        "## Readings (card labels)",
        "",
        "| Test | Standalone vs hold | Overlay vs tsmom12 |",
        "|---|---|---|",
        *labels,
        "",
        f"Pick bar (primary `six`, overlay vs `tsmom12`): z >= {BAR_Z} (BAR.md); "
        f"{BAR_Z_LOW} = the counting method decides.",
        "",
        "## Overlay vs `tsmom12`",
        "",
        *table(over),
        "",
        "## Standalone vs hold",
        "",
        *table(solo),
        "",
        "## Average exposure (sum of weights)",
        "",
        "| Test | Start | " + " | ".join(STRATS) + " |",
        "|---|---|" + "---:|" * len(STRATS),
        *expo,
        "",
        "## Placebo (US ten-industry book, monthly arithmetic, standalone minus hold)",
        "",
        "s = 0 is the true rule; s > 0 replaces the same month by months 12 j + s before.",
        "",
        "| s | Sharpe difference | Months |",
        "|---:|---:|---:|",
        *[f"| {s} | {d:+.3f} | {n} |" for s, d, n in pl],
        "",
        f"Rank of the true difference among the 11 (1 = highest): "
        f"{1 + sum(d > pl[0][1] for _, d, _ in pl[1:])}.",
        "",
    ]
    OUT.write_text("\n".join(lines))
    print(OUT.read_text())


if __name__ == "__main__":
    main()
