"""GSY 1: a Greenwood-Shleifer-You run-up flag as an exit overlay on `tsmom12`.
Card: research/cards/gsy-runup.md. Write-up: research/gsy-1.md.

    uv run python -I research/lib/gsy.py replicate   # step 2: descriptive, no strategy
    uv run python -I research/lib/gsy.py runs        # step 3: the card's variants

Ken French's industry files (cache root from research/macro.local.json or GRIMSTRADE_DATA; read
as data, never written). Nothing after 2025-11-10 (the train cut) is parsed; the held-out year
is never loaded. Rows go to research/tries.md the moment a configuration runs; a configuration
whose equity file exists under the git-ignored research/data/runs/ is re-scored without a row.
"""

from __future__ import annotations

import math
import sys
import zipfile
from collections.abc import Iterator, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as c  # noqa: E402
import gsy_signals as g  # noqa: E402
import harness  # noqa: E402
import stats  # noqa: E402
from macro import cache_root  # noqa: E402

from grimstrade.data import ETF, UNIVERSE, Bar  # noqa: E402

IDEA = "gsy-runup"
FRENCH = "french/2026-11-12"  # cached daily 10 industries and factors
EXTRA = "french-gsy/2026-11-18"  # downloaded for this lane
LAST = date(2025, 11, 10)  # train runs never load a later bar
LAST_MONTH = 202510  # last whole month before the held-out year
THRESHOLDS = (1.0, 1.5)


# --- loaders (raw cache, read only) ---


def _lines(path: Path) -> list[str]:
    z = zipfile.ZipFile(path)
    return z.read(z.namelist()[0]).decode("latin1").splitlines()


def _block(lines: Sequence[str], title: str) -> tuple[list[str], Iterator[list[str]]]:
    """Column names and the data rows (cells) of the block whose title line is `title`."""
    head = next(i for i, x in enumerate(lines) if x.strip() == title)
    names = [x.strip() for x in lines[head + 1].split(",")][1:]

    def rows() -> Iterator[list[str]]:
        started = False
        for line in lines[head + 2 :]:
            cells = [x.strip() for x in line.split(",")]
            if len(cells) == len(names) + 1 and cells[0].isdigit():
                started = True
                yield cells
            elif started:
                return

    return names, rows()


def _ret(x: str) -> float:
    v = float(x)
    return math.nan if v <= -99 else v / 100


@dataclass
class Monthly:
    months: list[int]  # yyyymm
    names: list[str]
    ret: np.ndarray  # months x industries, simple
    mkt: np.ndarray  # market total return, simple
    firms: np.ndarray  # months x industries, number of firms


def monthly(path: Path, factors: Path) -> Monthly:
    lines = _lines(path)
    names, rows = _block(lines, "Average Value Weighted Returns -- Monthly")
    data = {int(c[0]): [_ret(x) for x in c[1:]] for c in rows if int(c[0]) <= LAST_MONTH}
    _, frows = _block(lines, "Number of Firms in Portfolios")
    firms = {int(c[0]): [float(x) for x in c[1:]] for c in frows if int(c[0]) <= LAST_MONTH}
    fl = _lines(factors)
    head = next(i for i, x in enumerate(fl) if x.replace(" ", "") == ",Mkt-RF,SMB,HML,RF")
    fac: dict[int, float] = {}
    for line in fl[head + 1 :]:
        cells = [x.strip() for x in line.split(",")]
        if len(cells) != 5 or len(cells[0]) != 6 or not cells[0].isdigit():
            break
        if int(cells[0]) <= LAST_MONTH:
            fac[int(cells[0])] = (float(cells[1]) + float(cells[4])) / 100
    months = sorted(data)
    if months != sorted(fac):
        raise ValueError("industry and factor months disagree")
    return Monthly(
        months, names, np.array([data[m] for m in months]), np.array([fac[m] for m in months]),
        np.array([firms[m] for m in months]),
    )  # fmt: skip


def paths() -> dict[str, Path]:
    root = cache_root()
    e = root / EXTRA
    return {
        "49m": e / "49m" / "49_Industry_Portfolios_CSV.zip",
        "30m": e / "30m" / "30_Industry_Portfolios_CSV.zip",
        "10m": e / "10m" / "10_Industry_Portfolios_CSV.zip",
        "30d": e / "30d" / "30_Industry_Portfolios_daily_CSV.zip",
        "10d": root / FRENCH / "10_Industry_Portfolios_daily_CSV.zip",
        "fm": root / FRENCH / "F-F_Research_Data_Factors_CSV.zip",
        "fd": root / FRENCH / "F-F_Research_Data_Factors_daily_CSV.zip",
    }


# --- step 2: replication ---


def _row(months: list[int], ym: int) -> int:
    return months.index(ym)


def replicate() -> str:
    p = paths()
    out = [
        "## Step 2. Replication of GSY's conditional crash probability (descriptive)",
        "",
        "Monthly value-weighted French industries. Episode: the first month an industry's "
        "24-month return is at least the threshold, raw and net of the market, with no run-up "
        "month in that industry in the 24 months before. `Crash`: a peak-to-trough fall of 40% "
        "or more within the next 24 months (peak counted from the signal month on). `Strict`: "
        "a month-end 40% or more below the signal month's level within 24 months. `Base`: the "
        "same two shares over every industry-month in the window (no condition). Only "
        "episodes whose 24 months after end by 2025-10 count.",
        "",
        "| Industries | Window (signal months) | Threshold | Episodes | Crash | Strict | "
        "Median return next 6 m | Median return next 24 m | Base crash | Base strict |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    windows = [
        ("1928-07 to 2014-12 (GSY)", 192807, 201412),
        ("1928-07 to 2001-12", 192807, 200112),
        ("2002-01 to 2023-10", 200201, 202310),
        ("2015-01 to 2023-10", 201501, 202310),
    ]
    detail: list[str] = []
    for key in ("49m", "30m", "10m"):
        mo = monthly(p[key], p["fm"])
        idx = g.index_of(mo.ret)
        mk = g.index_of(mo.mkt[:, None])[:, 0]
        for label, a, b in windows:
            for th in THRESHOLDS:
                eps, base, hit, hit_s = g.episodes(
                    idx, mk, th, _row(mo.months, a), _row(mo.months, b)
                )
                med6 = float(np.median([e.r6 for e in eps])) if eps else math.nan
                med24 = float(np.median([e.r24 for e in eps])) if eps else math.nan
                out.append(
                    f"| {key[:-1]} | {label} | {th:.0%} | {len(eps)} | "
                    f"{_pc(g.share([e.crash for e in eps]))} | "
                    f"{_pc(g.share([e.strict for e in eps]))} | {_pc(med6)} | {_pc(med24)} | "
                    f"{_pc(hit / base if base else math.nan)} | "
                    f"{_pc(hit_s / base if base else math.nan)} |"
                )
                if key == "49m" and a == 192807 and b == 201412 and th == 1.0:
                    detail = [
                        f"| {mo.months[e.month]} | {mo.names[e.industry]} | "
                        f"{'yes' if e.crash else 'no'} | {'yes' if e.strict else 'no'} | "
                        f"{_pc(e.r6)} | {_pc(e.r24)} |"
                        for e in eps
                    ]
    out += [
        "",
        "**Added after the table above was seen (a re-reading, not the card's definition):** "
        "the same episodes, keeping only those whose industry had at least 10 firms in the "
        "signal month (a small-industry filter GSY may have used; not checked in the paper).",
        "",
        "| Industries | Window | Threshold | Episodes | Crash | Strict |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for key in ("49m", "30m"):
        mo = monthly(p[key], p["fm"])
        idx = g.index_of(mo.ret)
        mk = g.index_of(mo.mkt[:, None])[:, 0]
        for label, a, b in windows[:3]:
            for th in THRESHOLDS:
                eps, *_ = g.episodes(idx, mk, th, _row(mo.months, a), _row(mo.months, b))
                big = [e for e in eps if mo.firms[e.month, e.industry] >= 10]
                out.append(
                    f"| {key[:-1]} | {label} | {th:.0%} | {len(big)} | "
                    f"{_pc(g.share([e.crash for e in big]))} | "
                    f"{_pc(g.share([e.strict for e in big]))} |"
                )
    out += [
        "",
        "49 industries, 100%, 1928-2014: every episode.",
        "",
        "| Signal month | Industry | Crash | Strict | Next 6 m | Next 24 m |",
        "|---|---|---|---|---:|---:|",
        *detail,
        "",
    ]
    return "\n".join(out)


def _pc(x: float) -> str:
    return "-" if math.isnan(x) else f"{x * 100:.0f}%"


# --- step 3: the card's variants through the gym ---

VARIANTS = ["flag100-cash", "flag150-cash", "flag100-sma", "flag150-sma", "flag100-vol",
            "flag150-vol"]  # fmt: skip
DISC = ("disc", date(1928, 7, 2), date(2001, 12, 31))  # (key, first decision, last bar)
CHECK = ("check", date(2002, 1, 2), LAST)
DRAWS = 2000
ROUTE_S_P = 0.10 / 12  # Bonferroni: 6 variants x 2 routes


@dataclass
class Daily:
    days: list[date]
    names: list[str]
    ret: np.ndarray  # days x industries, simple; NaN = missing
    mkt: np.ndarray


def _ymd(s: str) -> date:
    return date(int(s[:4]), int(s[4:6]), int(s[6:]))


def daily(path: Path, factors: Path) -> Daily:
    names, rows = _block(_lines(path), "Average Value Weighted Returns -- Daily")
    data: dict[date, list[float]] = {}
    for cells in rows:
        d = _ymd(cells[0])
        if d > LAST:
            break  # nothing later is parsed
        data[d] = [_ret(x) for x in cells[1:]]
    fl = _lines(factors)
    head = next(i for i, x in enumerate(fl) if x.replace(" ", "") == ",Mkt-RF,SMB,HML,RF")
    fac: dict[date, float] = {}
    for line in fl[head + 1 :]:
        cells = [x.strip() for x in line.split(",")]
        if len(cells) != 5 or len(cells[0]) != 8 or not cells[0].isdigit():
            break
        d = _ymd(cells[0])
        if d > LAST:
            break
        fac[d] = (float(cells[1]) + float(cells[4])) / 100
    days = sorted(data)
    if days != sorted(fac):
        raise ValueError("industry and factor sessions disagree")
    return Daily(days, names, np.array([data[d] for d in days]), np.array([fac[d] for d in days]))


def to_bars(days: Sequence[date], ret: np.ndarray) -> list[Bar]:
    """Total-return bars (100 before the first return); open = previous close, so the gym's
    next-open fill is at the close the signal saw (trend-1926's primary fill)."""
    out: list[Bar] = []
    prev = 100.0
    for d, x in zip(days, ret, strict=True):
        if math.isnan(x):
            continue
        cl = prev * (1 + float(x))
        out.append(Bar(d, prev, max(prev, cl), min(prev, cl), cl, 0.0))
        prev = cl
    return out


@dataclass
class Book:
    label: str  # G30 / G10
    period: str  # disc / check
    start: date
    end: date
    hist: dict[str, list[Bar]]
    panel: harness.Panel
    ords: dict[str, np.ndarray]
    close: dict[str, np.ndarray]
    exits: dict[str, dict[str, np.ndarray]]  # variant -> symbol -> exit condition per bar
    runup: dict[float, dict[str, np.ndarray]]
    full_crashes: dict[str, list[g.Crash]] = field(default_factory=dict)


def build(dl: Daily, label: str, period: tuple[str, date, date]) -> Book:
    key, start, last = period
    keep = [i for i, d in enumerate(dl.days) if d <= last]
    days = [dl.days[i] for i in keep]
    m = g.index_of(dl.mkt[keep][:, None])[:, 0]
    m_ords = np.array([d.toordinal() for d in days], dtype=np.int64)
    hist: dict[str, list[Bar]] = {}
    ords: dict[str, np.ndarray] = {}
    close: dict[str, np.ndarray] = {}
    exits: dict[str, dict[str, np.ndarray]] = {v: {} for v in VARIANTS}
    runup: dict[float, dict[str, np.ndarray]] = {t: {} for t in THRESHOLDS}
    for j, name in enumerate(dl.names):
        s = f"{label}-{name}"
        UNIVERSE[s] = ETF  # research process only; src/ is untouched
        hist[s] = to_bars(days, dl.ret[keep, j])
        o = np.array([b.date.toordinal() for b in hist[s]], dtype=np.int64)
        cl = np.array([b.close for b in hist[s]])
        ords[s], close[s] = o, cl
        sma, vr = g.below_sma(o, cl), g.vol_rising(o, cl)
        for t in THRESHOLDS:
            ru = g.runup(o, cl, m_ords, m, t)
            runup[t][s] = ru
            flag = g.flag_active(o, ru)
            tag = f"flag{round(t * 100)}"
            exits[f"{tag}-cash"][s] = flag
            exits[f"{tag}-sma"][s] = flag & sma
            exits[f"{tag}-vol"][s] = flag & vr
    end = max(b[-1].date for b in hist.values()) - timedelta(days=1)
    end = min(end, harness.TRAIN_END)
    if c.DRY:  # plumbing check: the last 500 days only, nothing logged
        start = end - timedelta(days=500)
    return Book(label, key, start, end, hist, harness.Panel(hist), ords, close, exits, runup)


def overlay(exits: dict[str, np.ndarray]) -> c.ResearchStrategy:
    """`tsmom12`'s equal slots, each held only while the exit condition is false at the last
    visible close."""

    def f(view: harness.View) -> harness.Weights:
        held = c.live(view)
        return {
            s: 1 / len(held)
            for s in held
            if c.tsmom_signal(view, s) and not exits[s][view.n[s] - 1]
        }

    return c.weekly(f)


def run_once(variant: str, strategy: c.ResearchStrategy, bk: Book, kind: str) -> c.Run:
    """Run and log a configuration once; later calls re-score it without a new row."""
    tag = f"{variant}@{bk.label}-{bk.period}"
    done = (harness.DATA / "runs" / IDEA / f"{tag}.train.csv").exists()
    return harness.run(
        IDEA, tag, strategy, kind=kind, period="train", panel=bk.panel, history=bk.hist,
        start=bk.start, end=bk.end, log=not done and not c.DRY,
    )  # fmt: skip


# --- metrics ---


def held_by_day(run: c.Run) -> tuple[int, dict[str, np.ndarray]]:
    """(first decision ordinal, symbol -> held flag per decision day)."""
    first = run.decisions[0].time.date().toordinal()
    syms = {s for d in run.decisions for s in d.weights}
    out = {s: np.array([d.weights.get(s, 0.0) > 0 for d in run.decisions]) for s in syms}
    return first, out


@dataclass
class CrashStats:
    n: int = 0
    out: int = 0  # out of the slot on crash day
    by_overlay: int = 0  # out while tsmom12 was in
    exit_to_x: list[int] = field(default_factory=list)
    peak_to_exit: list[int] = field(default_factory=list)


def crash_stats(bk: Book, run: c.Run, twin: c.Run | None) -> CrashStats:
    first, held = held_by_day(run)
    _, twin_held = held_by_day(twin) if twin is not None else (first, {})
    n_days = len(run.decisions)
    cs = CrashStats()
    for s in bk.hist:
        h = held.get(s, np.zeros(n_days, bool))
        th = twin_held.get(s, np.zeros(n_days, bool))
        for cr in g.crashes(bk.ords[s], bk.close[s]):
            k = cr.x - 1 - first  # decision in force on crash day: the day before
            if k < 0 or k >= n_days:
                continue
            cs.n += 1
            if h[k]:
                continue
            cs.out += 1
            if twin is not None and th[k]:
                cs.by_overlay += 1
            ins = np.flatnonzero(h[: k + 1])
            if len(ins):
                ex = first + int(ins[-1]) + 1  # first day out
                cs.exit_to_x.append(cr.x - ex)
                cs.peak_to_exit.append(ex - cr.peak)
    return cs


@dataclass
class Alarms:
    spells: int = 0
    false: int = 0
    move: float = 0.0  # log points of price move over the overlay's spells (+ = given up)


def alarms(bk: Book, run: c.Run, twin: c.Run, crashes: dict[str, list[g.Crash]]) -> Alarms:
    first, held = held_by_day(run)
    _, twin_held = held_by_day(twin)
    n_days = len(run.decisions)
    out = Alarms()
    for s in bk.hist:
        h = held.get(s, np.zeros(n_days, bool))
        th = twin_held.get(s, np.zeros(n_days, bool))
        ov = th & ~h
        k = 0
        while k < n_days:
            if not ov[k]:
                k += 1
                continue
            e = k
            while e + 1 < n_days and ov[e + 1]:
                e += 1
            a, b = first + k, first + e + 1
            out.spells += 1
            if not any(a < cr.x <= a + g.YEARS2 for cr in crashes[s]):
                out.false += 1
            px = g.value_at(bk.ords[s], bk.close[s], np.array([a, b]))
            out.move += float(np.log(px[1] / px[0]))
            k = e + 1
    return out


def flag_episodes(bk: Book, t: float) -> int:
    n = 0
    lo, hi = bk.start.toordinal(), bk.end.toordinal()
    for s, ru in bk.runup[t].items():
        o = bk.ords[s]
        prev = g.flag_active(o, ru)
        starts = ru & ~np.concatenate([[False], prev[:-1]])
        n += int(((o >= lo) & (o <= hi) & starts).sum())
    return n


@dataclass
class Cmp:
    sharpe: float
    twin: float
    diff: float
    p: float
    p125: float
    mdd: float
    mdd_twin: float
    cagr: float
    time_in: float


def compare(a: np.ndarray, b: np.ndarray, exposure: float) -> Cmp:
    d, p, _, _ = stats.sharpe_diff_boot(a, b, draws=DRAWS, mean_block=20, seed=0)
    _, p125, _, _ = stats.sharpe_diff_boot(a, b, draws=DRAWS, mean_block=125, seed=0)
    return Cmp(stats.sharpe(a), stats.sharpe(b), d, p, p125, stats.max_drawdown(a),
               stats.max_drawdown(b), stats.cagr(a), exposure)  # fmt: skip


def window(run: c.Run, lo: date, hi: date) -> np.ndarray:
    return run.rets_between(lo, hi)


@dataclass
class Row:
    variant: str
    book: str
    period: str
    cmp: Cmp
    cr: CrashStats
    al: Alarms | None
    sub: dict[str, float]  # extra windows: Sharpe difference


def evaluate(bk: Book, run: c.Run, twin: c.Run, full: dict[str, list[g.Crash]]) -> Row:
    cmp = compare(run.rets, twin.rets, run.exposure)
    subs = (
        {
            "1928-64": (date(1928, 1, 1), date(1964, 12, 31)),
            "1965-01": (date(1965, 1, 1), date(2001, 12, 31)),
        }
        if bk.period == "disc"
        else {"2015-25": (date(2015, 1, 1), date(2025, 12, 31))}
    )
    sub = {
        k: stats.sharpe(window(run, a, b)) - stats.sharpe(window(twin, a, b))
        for k, (a, b) in subs.items()
    }
    same = run is twin
    return Row(
        run.variant.split("@")[0], bk.label, bk.period, cmp,
        crash_stats(bk, run, None if same else twin),
        None if same else alarms(bk, run, twin, full), sub,
    )  # fmt: skip


def runs() -> str:
    p = paths()
    rows: list[Row] = []
    holds: dict[tuple[str, str], Cmp] = {}
    episodes: dict[tuple[str, str], tuple[int, int]] = {}
    for label, key in (("G30", "30d"), ("G10", "10d")):
        dl = daily(p[key], p["fd"])
        full = build(dl, label, CHECK)  # for labelling false alarms only (outcomes, not signals)
        crashes = {s: g.crashes(full.ords[s], full.close[s]) for s in full.hist}
        for period in (DISC, CHECK):
            bk = full if period is CHECK else build(dl, label, period)
            twin = run_once("tsmom12", c.weekly(c.slots(c.tsmom_signal)), bk, "baseline")
            hold = run_once("equal-weight", c.weekly(c.equal_weight), bk, "baseline")
            holds[(label, bk.period)] = compare(hold.rets, twin.rets, hold.exposure)
            rows.append(evaluate(bk, twin, twin, crashes))
            episodes[(label, bk.period)] = (flag_episodes(bk, 1.0), flag_episodes(bk, 1.5))
            kind = "variant" if label == "G30" else "robustness"
            for v in VARIANTS:
                run = run_once(v, overlay(bk.exits[v]), bk, kind)
                rows.append(evaluate(bk, run, twin, crashes))
                print(f"{label} {bk.period} {v}: {rows[-1].cmp.diff:+.3f}", flush=True)
    return report(rows, holds, episodes)


# --- report ---


def _med(xs: list[int]) -> str:
    return "-" if not xs else f"{float(np.median(xs)):.0f}"


def verdicts(rows: list[Row]) -> dict[str, tuple[bool, bool]]:
    get = {(r.variant, r.book, r.period): r for r in rows}
    out = {}
    for v in VARIANTS:
        d, k, d10 = get[(v, "G30", "disc")], get[(v, "G30", "check")], get[(v, "G10", "disc")]
        t_d, t_k = get[("tsmom12", "G30", "disc")], get[("tsmom12", "G30", "check")]
        s = d.cmp.diff > 0 and d.cmp.p < ROUTE_S_P and k.cmp.diff > 0 and d10.cmp.diff > 0
        w = all(
            r.cmp.mdd_twin - r.cmp.mdd >= 0.05
            and r.cmp.diff >= -0.05
            and r.cr.out / max(r.cr.n, 1) > t.cr.out / max(t.cr.n, 1)
            for r, t in ((d, t_d), (k, t_k))
        )
        out[v] = (s, w)
    return out


def report(
    rows: list[Row],
    holds: dict[tuple[str, str], Cmp],
    episodes: dict[tuple[str, str], tuple[int, int]],
) -> str:
    out = ["## Step 3. The card's variants against `tsmom12`", ""]
    out += [
        "Equal-slot books of the 30 (`G30`, primary) and 10 (`G10`, robustness) French "
        "industries, daily, value-weighted. `disc` = decisions 1928-07-02 to 2001-12-30; "
        "`check` = 2002-01-02 to 2025-11-09. Sharpe on calendar days, cash 0, 2 bps a side. "
        "`dSharpe` = variant minus `tsmom12` on the same days; p one-sided bootstrap (block 20 "
        "days; `p125` block 125). Crashes: falls of 40% or more from a running peak in an "
        "industry's daily index, crash day in the period; `out` = slot in cash on the crash "
        "day; `by overlay` = out while `tsmom12` held. `exit->X`: median calendar days from "
        "the exit to the crash day; `peak->exit`: median days from the peak to the exit "
        "(negative = out before the peak). Alarms: spells where the overlay held cash while "
        "`tsmom12` held; `false` = no 40% crash in that industry within 730 days of the "
        "spell's start (crashes from the full 1926-2025 data); `given up` = sum of the price "
        "moves over those spells, log points (positive = the overlay missed a rise).",
        "",
        "Flag episodes in the period (independent bets), 100% / 150%: "
        + "; ".join(f"{b}-{pd} {a[0]} / {a[1]}" for (b, pd), a in episodes.items())
        + ".",
        "",
        "Equal weight (holding) against `tsmom12`, Sharpe hold / `tsmom12`, worst loss hold / "
        "`tsmom12`: "
        + "; ".join(
            f"{b}-{pd} {h.sharpe:.2f} / {h.twin:.2f}, {_pc(h.mdd)} / {_pc(h.mdd_twin)}"
            for (b, pd), h in holds.items()
        )
        + ".",
        "",
    ]
    for book in ("G30", "G10"):
        for period in ("disc", "check"):
            sub = [r for r in rows if r.book == book and r.period == period]
            keys = list(sub[0].sub)
            out += [
                f"### {book}, {period}",
                "",
                "| Variant | Sharpe | dSharpe (p; p125) | "
                + "".join(f"d {k} | " for k in keys)
                + "Worst loss (tsmom12) | Growth/yr | Time in | Crashes out / n | by overlay "
                "| exit->X | peak->exit | Alarms: spells, false | given up |",
                "|---|---:|---:|" + "---:|" * len(keys) + "---:|---:|---:|---:|---:|---:|---:|"
                "---:|---:|",
            ]
            for r in sub:
                m = r.cmp
                twin_row = r.variant == "tsmom12"
                d = "-" if twin_row else f"{m.diff:+.2f} ({m.p:.2f}; {m.p125:.2f})"
                sd = "".join(("- | " if twin_row else f"{r.sub[k]:+.2f} | ") for k in keys)
                al = (
                    "- | -"
                    if r.al is None
                    else f"{r.al.spells}, {r.al.false} | {r.al.move * 100:+.0f}"
                )
                out.append(
                    f"| {r.variant} | {m.sharpe:.2f} | {d} | {sd}{_pc(m.mdd)} ({_pc(m.mdd_twin)})"
                    f" | {m.cagr * 100:.1f}% | {_pc(m.time_in)} | {r.cr.out} / {r.cr.n} | "
                    f"{'-' if twin_row else r.cr.by_overlay} | {_med(r.cr.exit_to_x)} | "
                    f"{_med(r.cr.peak_to_exit)} | {al} |"
                )
            out.append("")
    vd = verdicts(rows)
    out += [
        "### The card's pass bar, applied mechanically",
        "",
        f"Route S: `G30` discovery dSharpe > 0 with p < {ROUTE_S_P:.4f}, check dSharpe > 0, "
        "`G10` discovery dSharpe > 0. Route W: worst loss at least 5 points smaller than "
        "`tsmom12`'s and dSharpe >= -0.05 in discovery and check, and a larger share of crashes "
        "out than `tsmom12` in both.",
        "",
        "| Variant | Route S | Route W | Verdict |",
        "|---|---|---|---|",
    ]
    for v, (s, w) in vd.items():
        yn = {True: "yes", False: "no"}
        out.append(f"| {v} | {yn[s]} | {yn[w]} | {'passes' if s or w else 'dead'} |")
    return "\n".join(out) + "\n"


def main() -> None:
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "replicate":
        text = replicate()
        path = Path(__file__).resolve().parents[1] / "results" / "gsy-1-replication.md"
        path.write_text(
            "# gsy-1: replication of GSY on French industries\n\nCard: "
            "`cards/gsy-runup.md`, step 2. Written by `lib/gsy.py replicate`.\n\n" + text
        )
        print(text)
    elif step == "runs":
        text = runs()
        name = "gsy-1.dry.md" if c.DRY else "gsy-1.md"
        path = harness.RESEARCH / "results" / name
        path.write_text(
            "# gsy-1: GSY run-up flag as an exit overlay on `tsmom12`\n\nCard: "
            "`cards/gsy-runup.md`, step 3. Written by `lib/gsy.py runs`. Replication: "
            "`results/gsy-1-replication.md`.\n\n" + text
        )
        print(text)
    else:
        raise SystemExit("usage: gsy.py replicate | runs")


if __name__ == "__main__":
    main()
