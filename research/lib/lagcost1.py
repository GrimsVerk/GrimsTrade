"""lagcost-1: what execution lag costs each live paper book (card: research/lagcost-1.md).

    uv run --with numpy python research/lib/lagcost1.py [--jobs 3] [--books a,b] [DRY=1]

Lag k, in bars of the asset's own clock: a decision whose newest bar of an asset class is bar d
fills that class at the open of bar d+1+k. One decision per calendar day D, stamped D+1 00:00 UTC
minus 1 microsecond; the live `decide` function sees each ETF's bars dated <= D minus its last
k_etf bars and each coin's bars dated <= D - k_coin. `gym.simulate` (unchanged) fills each asset
at its first open after the stamp: coins at D+1 00:00, ETFs at the next ETF open. (e0, c1) is
exactly `gym.backtest` at 22:30 (tests/test_lagcost1.py). `scheduled()` is the live schedule: one
decision at a fixed UTC time on D+1 with the gym's own visibility rule.

Train only (`harness.load_history("train")`: no bar after 2025-11-10). Every run is logged to
research/tries.md as `robustness`, idea = the book's live name; a run whose equity curve is
identical to an earlier run of the same book and period is not logged again.
"""

from __future__ import annotations

import argparse
import bisect
import math
import os
import sys
from collections.abc import Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from datetime import UTC, date, datetime, time, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness  # noqa: E402  (puts src/ on the path)
import numpy as np  # noqa: E402
import stats  # noqa: E402

from grimstrade import gym, report  # noqa: E402
from grimstrade.data import CRYPTO, UNIVERSE, Bar, close_time  # noqa: E402
from grimstrade.gym import Decision, Strategy  # noqa: E402

EPS = timedelta(microseconds=1)
LIVE_AT = time(3, 0)  # the live job starts 02:00-06:13 UTC the next day (DECISIONS 2026-11-24)
REFERENCE = (0, 0)
# (k_etf, k_coin), in the card's order.
CONFIGS: list[tuple[int, int]] = [
    (0, 0), (1, 0), (2, 0), (5, 0), (0, 1), (0, 2), (0, 5), (1, 1), (2, 2), (5, 5),
]  # fmt: skip
BACKTEST = (0, 1)  # today's backtest schedule (gym.DECIDE_AT 22:30)
SCHED = "sched-0300"
PERIODS = {
    "primary": (harness.TRAIN_START, harness.TRAIN_END),
    "coin": (date(2012, 1, 2), harness.TRAIN_END),
}
DRAWS = 1000
BLOCK = 20.0
SEED = 0

History = Mapping[str, Sequence[Bar]]


def name(cfg: tuple[int, int] | str) -> str:
    return cfg if isinstance(cfg, str) else f"lag-e{cfg[0]}-c{cfg[1]}"


def stamp(d: date) -> datetime:
    """The decision time of day D: just before D+1 00:00 UTC, the next coin open."""
    return datetime.combine(d + timedelta(days=1), time(0, 0), tzinfo=UTC) - EPS


def lagged_view(
    hist: History, dates: Mapping[str, Sequence[date]], d: date, k_etf: int, k_coin: int
) -> dict[str, Sequence[Bar]]:
    """What the decision of day D sees: coin bars dated <= D - k_coin, ETF bars dated <= D minus
    the last k_etf of them."""
    view = {}
    for s, bars in hist.items():
        if UNIVERSE[s] == CRYPTO:
            n = bisect.bisect_right(dates[s], d - timedelta(days=k_coin))
        else:
            n = max(bisect.bisect_right(dates[s], d) - k_etf, 0)
        view[s] = bars[:n]
    return view


def lagged(
    strategy: Strategy, hist: History, start: date, end: date, k_etf: int, k_coin: int
) -> list[Decision]:
    dates = {s: [b.date for b in bars] for s, bars in hist.items()}
    out = []
    d = start
    while d <= end:
        weights, _ = strategy(lagged_view(hist, dates, d, k_etf, k_coin))
        out.append(Decision(stamp(d), dict(weights)))
        d += timedelta(days=1)
    return out


def scheduled(
    strategy: Strategy, hist: History, start: date, end: date, at: time, day_offset: int
) -> list[Decision]:
    """One decision a day at `at` UTC on day D + day_offset, seeing the bars closed by then (the
    gym's rule; `gym.backtest` is at=22:30, day_offset=0)."""
    closes = {s: [close_time(UNIVERSE[s], b.date) for b in bars] for s, bars in hist.items()}
    out = []
    d = start
    while d <= end:
        t = datetime.combine(d + timedelta(days=day_offset), at, tzinfo=UTC)
        view = {s: bars[: bisect.bisect_right(closes[s], t)] for s, bars in hist.items()}
        weights, _ = strategy(view)
        out.append(Decision(t, dict(weights)))
        d += timedelta(days=1)
    return out


def to_run(book: str, variant: str, decs: list[Decision], hist: History) -> harness.Run:
    res = gym.simulate(decs, hist)
    sc = report.score(f"{book}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    exposure = float(np.mean([sum(d.weights.values()) for d in decs]))
    return harness.Run(book, variant, "train", sc, days, equity, exposure, decs)


def align(a: harness.Run, b: harness.Run, burn: int = 0) -> tuple[np.ndarray, np.ndarray]:
    """Daily returns of two runs on their common days, the first `burn` days dropped (the
    first entry into the market, which a later first decision delays once)."""
    lo = max(a.days[0], b.days[0]) + timedelta(days=burn)
    hi = min(a.days[-1], b.days[-1])
    return a.rets_between(lo, hi), b.rets_between(lo, hi)


def paired(a: np.ndarray, b: np.ndarray) -> dict[str, float]:
    """Sharpe(a) - Sharpe(b) and CAGR(a) - CAGR(b) on the same days, with a paired stationary
    bootstrap SE and 95% interval."""
    rng = np.random.default_rng(SEED)
    ds, dc = np.empty(DRAWS), np.empty(DRAWS)
    for k in range(DRAWS):
        i = stats._stationary_indices(len(a), BLOCK, rng)
        ds[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
        dc[k] = stats.cagr(a[i]) - stats.cagr(b[i])
    return {
        "dsharpe": stats.sharpe(a) - stats.sharpe(b),
        "se": float(ds.std(ddof=1)),
        "lo": float(np.quantile(ds, 0.025)),
        "hi": float(np.quantile(ds, 0.975)),
        "dcagr": stats.cagr(a) - stats.cagr(b),
        "clo": float(np.quantile(dc, 0.025)),
        "chi": float(np.quantile(dc, 0.975)),
    }


def describe(run: harness.Run) -> dict[str, float]:
    r = run.rets
    return {
        "sharpe": stats.sharpe(r),
        "cagr": stats.cagr(r),
        "mdd": stats.max_drawdown(r),
        "turnover": run.score.turnover,
    }


@dataclass
class BookResult:
    book: str
    period: str
    start: date
    end: date
    runs: dict[str, harness.Run]  # variant -> run (only distinct curves)
    same: dict[str, str]  # variant -> the earlier variant with the identical curve
    metrics: dict[str, dict[str, float]]
    pairs: dict[str, dict[str, float]]  # "a|b" -> paired stats of a minus b


def one_book(book: str, period: str, dry: bool, burn: int = 0) -> BookResult:
    hist = harness.load_history("train")
    start, end = PERIODS[period]
    if dry:
        start = end - timedelta(days=120)
    strategy = gym_strategy(book)
    runs: dict[str, harness.Run] = {}
    same: dict[str, str] = {}
    variants: list[tuple[str, list[Decision]]] = [
        (name(c), lagged(strategy, hist, start, end, *c)) for c in CONFIGS
    ]
    variants.append((SCHED, scheduled(strategy, hist, start, end, LIVE_AT, 1)))
    for v, decs in variants:
        run = to_run(book, v, decs, hist)
        twin = next((u for u, r in runs.items() if np.array_equal(r.equity, run.equity)), None)
        if twin is not None and len(run.days) == len(runs[twin].days):
            same[v] = twin
        else:
            runs[v] = run
    got = {**runs, **{v: runs[u] for v, u in same.items()}}
    metrics = {v: describe(r) for v, r in got.items()}
    ref = name(REFERENCE)
    wanted = [(v, ref) for v in got if v != ref] + [(SCHED, name(BACKTEST)), (ref, SCHED)]
    pairs = {}
    for a, b in wanted:
        if got[a] is got[b]:
            pairs[f"{a}|{b}"] = dict.fromkeys(
                ("dsharpe", "se", "lo", "hi", "dcagr", "clo", "chi"), 0.0
            )
        else:
            pairs[f"{a}|{b}"] = paired(*align(got[a], got[b], burn))
    return BookResult(book, period, start, end, runs, same, metrics, pairs)


def gym_strategy(book: str) -> Strategy:
    from grimstrade.strategies import LIVE

    return LIVE[book]


# --- report ---


def _pp(x: float) -> str:
    return f"{x * 100:+.2f}"


def table(br: BookResult) -> list[str]:
    ref = name(REFERENCE)
    out = [
        f"### {br.book}, {br.period} ({br.start}..{br.end})",
        "",
        "| Variant | Sharpe | CAGR | Worst loss | Turnover/yr | dSharpe vs e0-c0 (SE; 95%) "
        "| dCAGR pts/yr (95%) |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for v in [name(c) for c in CONFIGS] + [SCHED]:
        m = br.metrics[v]
        note = f" (= {br.same[v]})" if v in br.same else ""
        row = (
            f"| {v}{note} | {m['sharpe']:.3f} | {m['cagr']:+.2%} | {m['mdd']:.1%} | "
            f"{m['turnover']:.2f} |"
        )
        if v == ref:
            row += " - | - |"
        else:
            p = br.pairs[f"{v}|{ref}"]
            row += (
                f" {p['dsharpe']:+.3f} ({p['se']:.3f}; {p['lo']:+.3f}..{p['hi']:+.3f}) | "
                f"{_pp(p['dcagr'])} ({_pp(p['clo'])}..{_pp(p['chi'])}) |"
            )
        out.append(row)
    s = br.pairs[f"{SCHED}|{name(BACKTEST)}"]
    out += [
        "",
        f"Live schedule minus backtest schedule (sched-0300 - e0-c1): dSharpe {s['dsharpe']:+.3f} "
        f"(SE {s['se']:.3f}; {s['lo']:+.3f}..{s['hi']:+.3f}), dCAGR {_pp(s['dcagr'])} pts/yr "
        f"({_pp(s['clo'])}..{_pp(s['chi'])}).",
        "",
    ]
    return out


def summary(results: list[BookResult]) -> list[str]:
    """Per book and period: what c0 recovers over today's coin lag (e0-c0 minus e0-c1), what
    a run before 00:00 UTC for all books recovers over the live schedule (e0-c0 minus
    sched-0300), and the live-vs-backtest gap."""
    out = [
        "| Book | Period | Coins c1 -> c0: dSharpe (95%) | dCAGR pts/yr (95%) "
        "| Live -> e0-c0: dSharpe (95%) | dCAGR (95%) | Live - backtest: dSharpe (95%) "
        "| dCAGR (95%) |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    ref = name(REFERENCE)
    for br in results:
        c = br.pairs[f"{name(BACKTEST)}|{ref}"]  # c1 minus c0; flip the sign
        live = br.pairs[f"{ref}|{SCHED}"]
        s = br.pairs[f"{SCHED}|{name(BACKTEST)}"]
        out.append(
            f"| {br.book} | {br.period} | {-c['dsharpe']:+.3f} ({-c['hi']:+.3f}..{-c['lo']:+.3f}) "
            f"| {_pp(-c['dcagr'])} ({_pp(-c['chi'])}..{_pp(-c['clo'])}) "
            f"| {live['dsharpe']:+.3f} ({live['lo']:+.3f}..{live['hi']:+.3f}) "
            f"| {_pp(live['dcagr'])} ({_pp(live['clo'])}..{_pp(live['chi'])}) "
            f"| {s['dsharpe']:+.3f} ({s['lo']:+.3f}..{s['hi']:+.3f}) "
            f"| {_pp(s['dcagr'])} ({_pp(s['clo'])}..{_pp(s['chi'])}) |"
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--books", default="")
    # Re-score only (rows already logged by the first run): paired statistics from day `burn`.
    ap.add_argument("--burn", type=int, default=0)
    ap.add_argument("--no-log", action="store_true")
    args = ap.parse_args()
    dry = bool(os.environ.get("DRY"))
    from grimstrade.strategies import LIVE

    books = args.books.split(",") if args.books else list(LIVE)
    jobs = [(b, p) for p in PERIODS for b in books]
    with ProcessPoolExecutor(max_workers=args.jobs) as ex:
        results = list(
            ex.map(one_book, *zip(*jobs, strict=True), [dry] * len(jobs), [args.burn] * len(jobs))
        )
    text = [
        "# lagcost-1: what execution lag costs each live book",
        "",
        "Card and reading: `research/lagcost-1.md`. Train only, research cache, gym costs, cash "
        "earns nothing. Sharpe on daily returns, 365 days, zero risk-free rate. Lag e<k>-c<k>: "
        "ETF and coin fills k bars after the first open after the signal. Paired differences "
        f"against e0-c0 on the same days: stationary bootstrap, {DRAWS} draws, mean block "
        f"{BLOCK:.0f} days, seed {SEED}. `(= x)`: identical equity curve to x, logged once.",
        "",
        "## Summary",
        "",
        *summary(results),
        "",
        "## Per book",
        "",
    ]
    for br in results:
        text += table(br)
        if not dry and not args.no_log:
            for v, run in br.runs.items():
                tag = v if br.period == "primary" else f"{v}@coin"
                harness._log(
                    harness.Run(
                        br.book, tag, "train", run.score, run.days, run.equity, run.exposure,
                        run.decisions,
                    ),
                    "robustness",
                    br.start,
                    br.end,
                )  # fmt: skip
    stem = "lagcost-1" + (f"-burn{args.burn}" if args.burn else "") + (".dry" if dry else "")
    if args.burn:
        text.insert(
            3,
            f"Re-score of the logged runs: paired statistics from day {args.burn + 1} "
            "of the common days (the first entry dropped); levels as in lagcost-1.md.",
        )
        text.insert(4, "")
    path = harness.RESEARCH / "results" / f"{stem}.md"
    path.write_text("\n".join(text).rstrip() + "\n")
    print("\n".join(text))
    if any(math.isnan(m["sharpe"]) for br in results for m in br.metrics.values()):
        print("lagcost1: a Sharpe is NaN", file=sys.stderr)


if __name__ == "__main__":
    main()
