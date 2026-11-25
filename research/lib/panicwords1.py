"""Lane panic-words-1: gate W34 `panic-words` (research/cards/panic-words-1.md; the rule was
pushed before this script's first run).

Descriptive only: no strategy, no backtest. Every month used is before 1965 (train cut
2025-10-31 holds trivially). The American Stories files are untrusted downloads in the shared
cache: run with `python -I`; they are only read as JSON, never extracted to disk.

Fetch:  `uv run python -I research/lib/fetch_panicwords1.py`
Count:  `uv run python -I research/lib/panicwords1.py count`  (monthly counts into the cache)
Run:    `uv run python -I research/lib/panicwords1.py`  (DRY=1: article and title counts only)
Output: research/results/panic-words.md, research/results/panic-words-counts.csv
"""

from __future__ import annotations

import json
import math
import os
import sys
import tarfile
from collections.abc import Sequence
from concurrent.futures import ProcessPoolExecutor
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import panicwords1_events as ev  # noqa: E402
import trend_1926 as t26  # noqa: E402
import wide11_events as e11  # noqa: E402
import wide13_events as e13  # noqa: E402
from macro import cache_root  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
LAST = date(2025, 10, 31)
FIRST_YEAR, LAST_YEAR = 1925, 1963
GATE = (1927 * 12 + 6, 1963 * 12 + 11)  # dose months 1927-07 .. 1963-12
HALF = 1945 * 12 + 11  # 1945-12: last month of the first half
FRENCH_SNAP = "2026-11-12"
LAGS = 3


def _root() -> Path:
    return cache_root() / "panic-words-1"


def ym(m: int) -> str:
    return f"{m // 12}-{m % 12 + 1:02d}"


# ---------------------------------------------------------------- counting


def count_year(year: int) -> dict[str, dict[str, int]]:
    """month -> {scans, articles, panic, crash, titles} for one year file (streamed)."""
    acc: dict[int, list[int]] = {}
    titles: dict[int, set[str]] = {}
    path = _root() / "americanstories" / f"faro_{year}.tar.gz"
    with tarfile.open(path, mode="r|gz") as tar:
        for mem in tar:
            if not (mem.isfile() and mem.name.endswith(".json")):
                continue
            f = tar.extractfile(mem)
            if f is None:
                continue
            try:
                obj = json.load(f)
            except ValueError:
                continue
            m = ev.scan_month(obj, mem.name)
            if m is None:
                continue
            n, p, c = ev.count_scan(obj)
            a = acc.setdefault(m, [0, 0, 0, 0])
            a[0] += 1
            a[1] += n
            a[2] += p
            a[3] += c
            lc = obj.get("lccn") or {}
            titles.setdefault(m, set()).add(str(lc.get("lccn", "")))
    out = {
        str(m): {
            "scans": v[0],
            "articles": v[1],
            "panic": v[2],
            "crash": v[3],
            "titles": len(titles[m]),
        }
        for m, v in sorted(acc.items())
    }
    dst = _root() / "counts" / f"{year}.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out))
    return out


def count_all() -> None:
    years = [
        y
        for y in range(FIRST_YEAR, LAST_YEAR + 1)
        if not (_root() / "counts" / f"{y}.json").exists()
        and (_root() / "americanstories" / f"faro_{y}.tar.gz").exists()
    ]
    with ProcessPoolExecutor(max_workers=3) as ex:
        for y, out in zip(years, ex.map(count_year, years), strict=True):
            print(f"{y}: {len(out)} months counted", flush=True)


def load_counts() -> dict[int, dict[str, int]]:
    out: dict[int, dict[str, int]] = {}
    for y in range(FIRST_YEAR, LAST_YEAR + 1):
        p = _root() / "counts" / f"{y}.json"
        if not p.exists():
            raise FileNotFoundError(f"{p}: run the count step first")
        for k, v in json.loads(p.read_text()).items():
            m = int(k)
            if m // 12 == y:  # a scan dated outside its year file is dropped
                out[m] = v
    return out


# ---------------------------------------------------------------- the gate


def load_market() -> dict[int, tuple[float, float]]:
    path = cache_root() / "french" / FRENCH_SNAP / "F-F_Research_Data_Factors_daily_CSV.zip"
    fac = t26.parse_factors(t26._lines(path), LAST)
    return ev.monthly_market({d: v[0] for d, v in fac.items() if d.year < 1966})


def fit(
    months: Sequence[int], y: dict[int, float], dose: dict[int, float], ctrl: list[dict[int, float]]
) -> tuple[float, float, int]:
    """(b, t, rows) of the dose: y = a + b dose + controls, Newey-West 3 lags over the month.
    The one code path for every cell, true and placebo."""
    nan = math.nan
    ys = np.array([y.get(m, nan) for m in months])
    cols = [np.ones(len(months)), np.array([dose.get(m, nan) for m in months])]
    cols += [np.array([c.get(m, nan) for m in months]) for c in ctrl]
    beta, tt, n = e11.ols_dk(cols, ys, np.array(months), LAGS)
    return float(beta[1]), float(tt[1]), n


def shifted(d: dict[int, float], k: int) -> dict[int, float]:
    """d_k(m) = d(m - k): an earlier dose."""
    return {m + k: v for m, v in d.items()}


def null_block(t: float, placebo: list[float]) -> tuple[int, list[str]]:
    rank = e11.rank_highest(-t, [-p for p in placebo])  # predicted sign negative
    sd, share = e11.null_spread(placebo)
    q5, med, q95 = e13.quantiles(placebo)
    return rank, [
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {q5:+.2f}, 50% {med:+.2f}, 95% {q95:+.2f}; smallest"
        f" {min(placebo):+.2f}, largest {max(placebo):+.2f}.",
    ]


def main() -> None:
    if sys.argv[1:] == ["count"]:
        count_all()
        return
    counts = load_counts()
    mkt = load_market()
    months = list(range(GATE[0], GATE[1] + 1))
    arts = {m: v["articles"] for m, v in counts.items()}
    d = ev.dose(arts, {m: v["panic"] for m, v in counts.items()})
    dc = ev.dose(arts, {m: v["crash"] for m, v in counts.items()})
    y = {m: mkt[m + 1][0] for m in months if m + 1 in mkt}
    y3 = {
        m: mkt[m + 1][0] + mkt[m + 2][0] + mkt[m + 3][0]
        for m in months
        if all(m + j in mkt for j in (1, 2, 3))
    }
    c1 = {m: mkt[m][0] for m in months if m in mkt}
    c12 = {m: ev.past_return(mkt, m, 12, 1) for m in months}
    v = {m: mkt[m][1] for m in months if m in mkt}
    ctrl = [c1, c12, v]
    common = [m for m in months if all(m - k in d for k in ev.SHIFTS_W34) and m in d]

    if DRY:
        for yr in range(FIRST_YEAR, LAST_YEAR + 1):
            ms = [counts[m] for m in counts if m // 12 == yr]
            print(
                f"{yr}: months {len(ms)}, scans {sum(x['scans'] for x in ms)}, articles"
                f" {sum(x['articles'] for x in ms)}, titles/month max"
                f" {max((x['titles'] for x in ms), default=0)}, months < {ev.MIN_ARTICLES}"
                f" articles {sum(x['articles'] < ev.MIN_ARTICLES for x in ms)}"
            )
        print("dose months", len(d), ym(min(d)), "..", ym(max(d)))
        print("gate rows", fit(months, y, {m: 0.0 + (m % 7) for m in d}, ctrl)[2])
        ns = [
            fit(months, y, {m: 0.0 + (m % 7) for m in shifted(d, k)}, ctrl)[2]
            for k in ev.SHIFTS_W34
        ]
        print("placebo rows min", min(ns), "max", max(ns), "common rows", len(common))
        return

    b, t, n = fit(months, y, d, ctrl)
    sd_d = float(np.std([d[m] for m in months if m in d and m in y]))
    placebo = [fit(months, y, shifted(d, k), ctrl)[1] for k in ev.SHIFTS_W34]
    rank, null = null_block(t, placebo)
    passed = b < 0 and t <= -2 and rank <= 2

    def cell(name: str, r: tuple[float, float, int]) -> str:
        return f"| {name} | {r[0] * 100:+.3f} | {r[1]:+.2f} | {r[2]} |"

    shown = [
        cell("(a) no controls", fit(months, y, d, [])),
        cell('(b) "crash" dose, controls', fit(months, y, dc, ctrl)),
        cell("(c) months m+1..m+3", fit(months, y3, d, ctrl)),
        cell("(e) 1927-07 .. 1945-12", fit([m for m in months if m <= HALF], y, d, ctrl)),
        cell("(e) 1946-01 .. 1963-12", fit([m for m in months if m > HALF], y, d, ctrl)),
    ]
    tc = fit(common, y, d, ctrl)
    pc = [fit(common, y, shifted(d, k), ctrl)[1] for k in ev.SHIFTS_W34]
    rank_c, null_c = null_block(tc[1], pc)
    # (f) feedback: the dose on the dose month's and the past year's market return
    fm = [m for m in months if m in d]
    beta, tf, nf = e11.ols_dk(
        [np.ones(len(fm)), np.array([c1.get(m, math.nan) for m in fm]),
         np.array([c12.get(m, math.nan) for m in fm])],
        np.array([d[m] for m in fm]), np.array(fm), LAGS,
    )  # fmt: skip

    lines = [
        "# W34 `panic-words`: result",
        "",
        "Card: `research/cards/panic-words-1.md`. Script: `research/lib/panicwords1.py`. Data:"
        " American Stories (Dell et al. 2023, CC-BY 4.0) monthly article counts"
        " (`panic-words-counts.csv`); US market from Ken French's daily file.",
        "",
        f"**Gate (dose months {ym(GATE[0])} .. {ym(GATE[1])}, {n} rows):** b = {b * 100:+.3f}%"
        f" next-month log return per unit of d ({b * sd_d * 100:+.3f}% per sd of d, sd"
        f" {sd_d:.3f}), Newey-West t {t:+.2f}; rank {rank} of 41 (lowest = 1)."
        f" **{'PASS (kill-only)' if passed else 'FAIL'}.**",
        "",
        *null,
        "",
        "| k (months; earlier dose) | t |",
        "|---:|---:|",
        *[f"| {k} | {p:+.2f} |" for k, p in zip(ev.SHIFTS_W34, placebo, strict=True)],
        "",
        "## Shown (not gating)",
        "",
        "| Cell | b (% per unit d) | t | rows |",
        "|---|---:|---:|---:|",
        *shown,
        f"| (d) common rows {ym(common[0])} .. {ym(common[-1])} | {tc[0] * 100:+.3f} |"
        f" {tc[1]:+.2f} | {tc[2]} |",
        "",
        f"(d) on the common rows: rank {rank_c} of 41. " + null_c[0],
        "",
        f"(f) feedback, d(m) on the dose month's return c1 and the past year's c12 ({nf} rows):"
        f" c1 {beta[1]:+.3f} (t {tf[1]:+.2f}), c12 {beta[2]:+.3f} (t {tf[2]:+.2f}).",
        "",
    ]
    RESULTS.mkdir(exist_ok=True)
    (RESULTS / "panic-words.md").write_text("\n".join(lines))
    rows = ["month,scans,articles,panic,crash,titles"]
    rows += [
        f"{ym(m)},{c['scans']},{c['articles']},{c['panic']},{c['crash']},{c['titles']}"
        for m, c in sorted(counts.items())
    ]
    (RESULTS / "panic-words-counts.csv").write_text("\n".join(rows) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
