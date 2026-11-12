"""Idea-lab harness: run a research strategy through the real gym and log the try.

Research strategies are functions `f(view) -> weights` over a `View` (numpy arrays of the bars
closed before the decision). `decisions()` is a fast equivalent of `grimstrade.gym.backtest`
(bisect instead of a full scan per day); `as_gym()` wraps the same function as a plain gym strategy
so `check_against_gym()` can prove both paths give identical decisions. Fills, costs and equity
always come from `grimstrade.gym.simulate`, untouched.

Periods (fixed before any test was run):
- train:    decisions 2017-01-01 .. 2025-11-09, bars after 2025-11-10 are not even loaded.
- held-out: decisions 2025-11-11 .. 2026-11-09 (the most recent 12 months). Checked at most once
  per idea; `run()` refuses a second held-out variant for the same idea.

Run scripts with numpy available:  uv run --with numpy python research/lib/<script>.py
"""

from __future__ import annotations

import bisect
import csv
import fcntl
import sys
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from grimstrade import data, gym, report  # noqa: E402
from grimstrade.data import UNIVERSE, Bar, close_time  # noqa: E402
from grimstrade.gym import DECIDE_AT, Decision  # noqa: E402

RESEARCH = ROOT / "research"
DATA = RESEARCH / "data"
TRIES = RESEARCH / "tries.md"

TRAIN_START = date(2017, 1, 1)
TRAIN_END = date(2025, 11, 9)  # last train decision
TRAIN_LAST_BAR = date(2025, 11, 10)  # train runs never load a later bar
HELD_START = date(2025, 11, 11)
HELD_END = date(2026, 11, 9)
# Halves of the train period, for stability checks.
HALF_SPLIT = date(2021, 6, 1)

SYMS = list(UNIVERSE)
Weights = dict[str, float]
ResearchStrategy = Callable[["View"], Weights]


def load_history(period: str = "train", adjusted: bool = False) -> dict[str, list[Bar]]:
    """Raw bars from the research cache. `train` cuts everything after TRAIN_LAST_BAR."""
    if period not in ("train", "heldout"):
        raise ValueError(period)
    hist = data.load_all(RESEARCH)  # reads research/data/bars/<SYM>.csv
    if adjusted:
        for s in SYMS:
            if (DATA / "adj" / f"{s}.csv").exists():
                hist[s] = _load_csv(DATA / "adj" / f"{s}.csv")
    if not all(hist.values()):
        raise FileNotFoundError("no price cache: run research/lib/fetch.py first")
    if period == "train":
        hist = {s: [b for b in bars if b.date <= TRAIN_LAST_BAR] for s, bars in hist.items()}
    return hist


def _load_csv(path: Path) -> list[Bar]:
    with path.open(newline="") as f:
        return [
            Bar(date.fromisoformat(r["date"]), float(r["open"]), float(r["high"]),
                float(r["low"]), float(r["close"]), float(r["volume"]))
            for r in csv.DictReader(f)
        ]  # fmt: skip


def decide_time(d: date) -> datetime:
    return datetime.combine(d, DECIDE_AT, tzinfo=UTC)


class Panel:
    """Bars as numpy arrays, with the gym's visibility rule precomputed."""

    def __init__(self, history: Mapping[str, Sequence[Bar]]):
        self.syms = [s for s in SYMS if s in history]
        self.close_times: dict[str, list[datetime]] = {}
        self.ord: dict[str, np.ndarray] = {}
        self.o: dict[str, np.ndarray] = {}
        self.h: dict[str, np.ndarray] = {}
        self.l: dict[str, np.ndarray] = {}
        self.c: dict[str, np.ndarray] = {}
        self.v: dict[str, np.ndarray] = {}
        self.lr: dict[str, np.ndarray] = {}  # lr[i] = log(c[i+1] / c[i])
        for s in self.syms:
            bars = history[s]
            self.close_times[s] = [close_time(UNIVERSE[s], b.date) for b in bars]
            self.ord[s] = np.array([b.date.toordinal() for b in bars], dtype=np.int64)
            self.o[s] = np.array([b.open for b in bars])
            self.h[s] = np.array([b.high for b in bars])
            self.l[s] = np.array([b.low for b in bars])
            self.c[s] = np.array([b.close for b in bars])
            self.v[s] = np.array([b.volume for b in bars])
            self.lr[s] = np.diff(np.log(self.c[s])) if len(bars) > 1 else np.array([])
        # Business-day grid: one row per SPY bar date, the last close of every asset visible at
        # that day's decision time (NaN before an asset starts). For joint statistics.
        grid_sym = "SPY" if "SPY" in self.syms else self.syms[0]
        self.grid_dates = [date.fromordinal(int(x)) for x in self.ord[grid_sym]]
        self.grid_times = [decide_time(d) for d in self.grid_dates]
        g = np.full((len(self.grid_dates), len(self.syms)), np.nan)
        for j, s in enumerate(self.syms):
            for i, t in enumerate(self.grid_times):
                n = bisect.bisect_right(self.close_times[s], t)
                if n:
                    g[i, j] = self.c[s][n - 1]
        self.grid = g

    def view(self, t: datetime) -> View:
        n = {s: bisect.bisect_right(self.close_times[s], t) for s in self.syms}
        return View(self, n, bisect.bisect_right(self.grid_times, t))


@dataclass
class View:
    """What a decision may see: for each asset, the first n[s] bars."""

    panel: Panel
    n: dict[str, int]
    n_grid: int

    @property
    def syms(self) -> list[str]:
        return self.panel.syms

    @property
    def today(self) -> date:
        """Decision date, derived from the data: the date of the latest visible close time."""
        last = [self.panel.close_times[s][k - 1] for s, k in self.n.items() if k]
        return max(last).date()

    def has(self, s: str, bars: int) -> bool:
        return self.n.get(s, 0) >= bars

    def close(self, s: str) -> np.ndarray:
        return self.panel.c[s][: self.n[s]]

    def open(self, s: str) -> np.ndarray:
        return self.panel.o[s][: self.n[s]]

    def high(self, s: str) -> np.ndarray:
        return self.panel.h[s][: self.n[s]]

    def low(self, s: str) -> np.ndarray:
        return self.panel.l[s][: self.n[s]]

    def volume(self, s: str) -> np.ndarray:
        return self.panel.v[s][: self.n[s]]

    def logret(self, s: str) -> np.ndarray:
        return self.panel.lr[s][: max(self.n[s] - 1, 0)]

    def dates(self, s: str) -> np.ndarray:
        return self.panel.ord[s][: self.n[s]]

    def grid(self, rows: int | None = None) -> np.ndarray:
        """Business-day closes, columns in `syms` order; the last `rows` visible rows."""
        g = self.panel.grid[: self.n_grid]
        return g if rows is None else g[-rows:]

    def grid_logret(self, rows: int) -> np.ndarray:
        g = self.grid(rows + 1)
        return np.diff(np.log(g), axis=0)

    def at(self, d: date) -> View:
        """The view a decision on an earlier day `d` had (for scheduled rebalancing)."""
        if d > self.today:
            raise ValueError("no looking forward")
        return self.panel.view(decide_time(d))


def clean(w: Mapping[str, float]) -> Weights:
    out = {s: float(x) for s, x in w.items() if x > 1e-6}
    tot = sum(out.values())
    if tot > 1.0:
        out = {s: x / tot * (1 - 1e-12) for s, x in out.items()}
    return out


def decisions(strategy: ResearchStrategy, panel: Panel, start: date, end: date) -> list[Decision]:
    out = []
    d = start
    while d <= end:
        t = decide_time(d)
        out.append(Decision(t, clean(strategy(panel.view(t)))))
        d += timedelta(days=1)
    return out


def as_gym(strategy: ResearchStrategy) -> gym.Strategy:
    """The same strategy as a plain gym strategy (slow: rebuilds the panel on every call)."""

    def decide(history: data.History) -> tuple[Weights, str]:
        panel = Panel({s: b for s, b in history.items() if b})
        far = datetime.max.replace(tzinfo=UTC)
        return clean(strategy(panel.view(far))), "research"

    return decide


def check_against_gym(
    strategy: ResearchStrategy, history: Mapping[str, Sequence[Bar]], days: Sequence[date]
) -> None:
    """Assert the fast path and `gym.backtest` produce the same weights on the given days."""
    panel = Panel(history)
    slow = as_gym(strategy)
    for d in days:
        fast = decisions(strategy, panel, d, d)[0].weights
        ref = gym.backtest(slow, history, d, d)[0].weights
        if set(fast) != set(ref) or any(abs(fast[s] - ref[s]) > 1e-9 for s in fast):
            raise AssertionError(f"{d}: fast {fast} != gym {ref}")


@dataclass
class Run:
    idea: str
    variant: str
    period: str
    score: report.Score
    days: list[date]
    equity: np.ndarray
    exposure: float  # mean sum of target weights

    @property
    def rets(self) -> np.ndarray:
        return self.equity[1:] / self.equity[:-1] - 1

    def rets_between(self, a: date, b: date) -> np.ndarray:
        idx = [i for i, d in enumerate(self.days) if a <= d <= b]
        e = self.equity[idx[0] : idx[-1] + 1]
        return e[1:] / e[:-1] - 1


def _period_dates(period: str) -> tuple[date, date]:
    return (TRAIN_START, TRAIN_END) if period == "train" else (HELD_START, HELD_END)


def _heldout_used(idea: str) -> bool:
    for line in TRIES.read_text().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[1] == idea and cells[3] == "variant" and cells[4] == "heldout":
            return True
    return False


def _log(run: Run, kind: str, start: date, end: date) -> None:
    s = run.score
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {run.idea} | {run.variant} | {kind} | "
        f"{run.period} | {start} | {end} | {s.sharpe:.2f} | {s.total_return:+.1%} | "
        f"{s.max_drawdown:.1%} | {s.turnover:.2f} |\n"
    )
    with TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row)


def run(
    idea: str,
    variant: str,
    strategy: ResearchStrategy,
    *,
    kind: str = "variant",
    period: str = "train",
    panel: Panel | None = None,
    history: Mapping[str, Sequence[Bar]] | None = None,
    start: date | None = None,
    end: date | None = None,
    costs: Mapping[str, gym.Costs] = gym.COSTS,
    log: bool = True,
) -> Run:
    """Backtest one variant through the gym and append it to tries.md.

    `log=False` is only for re-scoring an already logged variant (e.g. reading its equity curve
    again); every new configuration must be logged.
    """
    if kind not in ("variant", "baseline", "robustness"):
        raise ValueError(kind)
    if period == "heldout" and kind == "variant" and log and _heldout_used(idea):
        raise RuntimeError(f"{idea}: the held-out period was already checked once")
    hist = history if history is not None else load_history(period)
    pan = panel if panel is not None else Panel(hist)
    a, b = _period_dates(period)
    a, b = start or a, end or b
    decs = decisions(strategy, pan, a, b)
    res = gym.simulate(decs, hist, costs=costs)
    sc = report.score(f"{idea}/{variant}", res)
    out = Run(
        idea, variant, period, sc,
        [d for d, _ in res.equity],
        np.array([e for _, e in res.equity]),
        float(np.mean([sum(d.weights.values()) for d in decs])),
    )  # fmt: skip
    if log:
        _log(out, kind, a, b)
        path = DATA / "runs" / idea / f"{variant}.{period}.csv"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", newline="") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(["date", "equity"])
            w.writerows((d.isoformat(), repr(float(e))) for d, e in zip(out.days, out.equity))  # noqa: B905
    return out
