"""deep-1: rebuild the daily series (equity and target weights) of the models already tested.

    uv run --with numpy --with scikit-learn --with numba python research/lib/deep1_models.py \
        <universe> [model ...]
    ML_HORIZON=7 uv run ... research/lib/deep1_models.py <universe> gbm-wk

Universes: six, etf, coin, idx, SPY (the two single-asset timing cards). Each model is run through
the harness exactly as its card ran it. A configuration that already has a row in `tries.md` is
re-scored without logging and checked against the logged Sharpe; a configuration that has none
(a card's rule on a set it was not run on) is logged as `robustness` under idea `deep-1`.
Series go to `<cache_root>/derived/deep-1/series/<universe>/<model>.npz` (never committed).
"""

from __future__ import annotations

import os
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import common as c
import harness
import macro
import numpy as np
import rules
import stats

OUT = macro.cache_root() / "derived" / "deep-1"
AR_START = date(2002, 1, 1)  # absorption-ratio: first full month in which its shift exists
SAFE = ("TLT", "GLD", "IEF", "LQD")

Factory = Callable[[c.Ctx], c.ResearchStrategy]
First = Callable[[c.Ctx], date]


@dataclass(frozen=True)
class Model:
    name: str
    idea: str  # idea under which the configuration is logged in tries.md
    variant: str  # its variant name there
    make: Factory
    family: str  # benchmark | twin | run1 | ml | macro | timing
    first: First | None = None  # first day the rule can act (default: the universe's start)
    sets: tuple[str, ...] = ("six", "etf", "coin", "idx")
    pool: bool = True  # a complement in Part B


def _w(f: c.ResearchStrategy) -> Factory:
    return lambda u: c.weekly(f)


def _ml(spec_name: str, **kw: object) -> Factory:
    def make(u: c.Ctx) -> c.ResearchStrategy:
        import ml  # needs scikit-learn; imported only when an ML model is built

        return c.weekly(ml.strategy(getattr(ml, spec_name), **kw))  # type: ignore[arg-type]

    return make


def _ml_first(u: c.Ctx) -> date:
    import ml

    return max(u.start, ml.first_fit_day(u.panel, u.start))


def _fit(name: str) -> Factory:
    def make(u: c.Ctx) -> c.ResearchStrategy:
        import rules_fit  # needs numba

        f = getattr(rules_fit, name)
        return c.weekly(c.slots(f))

    return make


def _risk(u: c.Ctx) -> list[str]:
    return [s for s in u.panel.syms if s not in SAFE]


def _absorption(u: c.Ctx) -> c.ResearchStrategy:
    import idea_absorption_ratio as ar

    risk = ["SPY", "QQQ", "BTC", "ETH"] if u.name == "six" else _risk(u)
    return c.weekly(ar.rule("train", 0, risk))


def _macro(gate: str, coins_only: bool = False) -> Factory:
    def make(u: c.Ctx) -> c.ResearchStrategy:
        f = getattr(macro.features(), gate)
        return c.weekly(rules.macro_gate(f, trend=True, coins_only=coins_only))

    return make


def _timing(which: str) -> Factory:
    def make(u: c.Ctx) -> c.ResearchStrategy:
        sym = u.name
        if which == "window":
            import idea_month_end_liquidity as m

            signal = m.in_window
        else:
            import idea_dip_rsi2 as d

            signal = d.held

        def rule(view: c.View) -> c.Weights:
            return {sym: 1.0} if c.eligible(view, sym) and signal(view, sym) else {}

        return rule

    return make


SIX = ("six",)
MODELS: list[Model] = [
    Model("tsmom12", "baselines", "tsmom12", _w(c.slots(c.tsmom_signal)), "twin", pool=False),
    Model("equal-weight", "baselines", "equal-weight", _w(c.equal_weight), "benchmark"),
    Model("sma200", "baselines", "sma200", _w(c.slots(c.sma_signal)), "twin"),
    Model("inverse-vol", "baselines", "inverse-vol", _w(c.inverse_vol), "twin"),
    Model("vol-calm", "baselines", "vol-calm", _w(c.slots(c.vol_calm_signal)), "twin"),
    Model("sixty-forty", "baselines", "sixty-forty", _w(c.sixty_forty), "benchmark", sets=SIX),
    Model("bh-spy", "baselines", "bh-spy", _w(c.hold("SPY")), "benchmark", sets=SIX, pool=False),
    Model("bh-btc", "baselines", "bh-btc", _w(c.hold("BTC")), "benchmark", sets=SIX, pool=False),
    Model("kelly", "kelly-shrunk", "k0.2", _w(rules.kelly(0.2)), "run1"),
    Model("hmm", "hmm-regime", "hard", _fit("hmm_hard"), "run1"),
    Model("fracdiff", "fracdiff-momentum", "d0.4", _w(c.slots(rules.fracdiff_signal(0.4))), "run1"),
    Model("dd-control", "drawdown-control", "d1.0", _w(rules.drawdown_control(1.0)), "run1"),
    Model("universal", "universal-portfolio", "up", _w(rules.universal_portfolio), "run1"),
    Model("absorption", "absorption-ratio", "six", _absorption, "run1",
          first=lambda u: max(u.start, AR_START)),
    Model("hawkes", "hawkes-clustering", "down2", _fit("hawkes_quiet"), "run1"),
    Model("vol-target", "vol-target", "t40", _w(rules.vol_target(0.40)), "run1"),
    Model("ensemble", "ensemble-tsmom", "e4", _w(rules.ensemble_tsmom), "run1"),
    Model("trend-vol", "trend-vol", "tv40", _w(rules.trend_vol(0.40)), "run1"),
    Model("trend-safe", "trend-to-safe", "safe", _w(rules.trend_to_safe), "run1"),
    Model("logit", "ml-linear", "logit", _ml("LOGIT"), "ml", first=_ml_first),
    Model("gbm", "ml-gbm", "gbm", _ml("GBM"), "ml", first=_ml_first),
    Model("meta-gbm", "ml-filter", "meta-gbm", _ml("META_GBM"), "ml", first=_ml_first),
    Model("gbm-prop", "ml-sizing", "gbm-prop", _ml("GBM", sizing="prop", tag="gbm-prop"), "ml",
          first=_ml_first),
    Model("gbm-pay", "ml-payoff", "gbm-pay", _ml("GBM_PAY", sizing="hard"), "ml",
          first=_ml_first),
    Model("gbm-pool", "ml-pooled", "gbm-pool", _ml("GBM_POOL"), "ml", first=_ml_first),
    Model("gbm-wk", "ml-weekly", "gbm-wk", _ml("GBM_WK"), "ml", first=_ml_first),
    Model("hike-and", "fed-hiking", "hike-and", _macro("fed_hiking"), "macro"),
    Model("real-and", "real-rate", "real-and", _macro("real_rate_rising"), "macro"),
    Model("curve-and", "yield-curve", "curve-and", _macro("curve_inverted"), "macro"),
    Model("m2-and", "liquidity", "m2-and", _macro("real_m2_negative"), "macro"),
    Model("walcl-and", "liquidity", "walcl-and", _macro("qt"), "macro"),
    Model("spread-and", "credit-spread", "spread-and", _macro("spread_widening"), "macro"),
    Model("halving-and", "halving", "halving-and", _macro("halving_bear", True), "macro",
          sets=SIX, pool=False),
    Model("month-end", "month-end-liquidity", "window", _timing("window"), "timing",
          sets=("SPY",), pool=False),
    Model("dip-rsi2", "dip-rsi2", "rsi2", _timing("rsi2"), "timing", sets=("SPY",), pool=False),
]  # fmt: skip
BY_NAME = {m.name: m for m in MODELS}
WEEKLY_ML = {"gbm-wk"}  # must run in a process started with ML_HORIZON=7


def models_for(universe: str) -> list[Model]:
    return [m for m in MODELS if universe in m.sets]


def pool_for(universe: str) -> list[Model]:
    return [m for m in models_for(universe) if m.pool]


# --- the tries.md lookup ---


def logged(idea: str, tag: str, start: date) -> float | None:
    """Sharpe of the train row with this idea, variant and first day, if `tries.md` has one."""
    for line in harness.TRIES.read_text().splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) >= 8 and cells[1] == idea and cells[2] == tag and cells[4] == "train" \
                and cells[5] == start.isoformat():  # fmt: skip
            return float(cells[7])
    return None


# --- series ---


@dataclass
class Series:
    """A model on a universe's calendar. `days[k]` for k = 0..n; `rets[k]` is the return of day
    `days[k + 1]`; `w[k]` the target weights decided on `days[k]` (held from the next open).
    Before the model's `first` day: NaN returns and zero weights."""

    name: str
    syms: list[str]
    days: np.ndarray  # ordinals, n + 1
    rets: np.ndarray  # n
    w: np.ndarray  # n x len(syms)
    first: int  # ordinal of the first day the model acts

    def date(self, k: int) -> date:
        return date.fromordinal(int(self.days[k]))


def path(universe: str, name: str) -> Path:
    return OUT / "series" / universe / f"{name}.npz"


def load(universe: str, name: str) -> Series:
    z = np.load(path(universe, name), allow_pickle=False)
    return Series(name, [str(s) for s in z["syms"]], z["days"], z["rets"], z["w"], int(z["first"]))


def to_series(run: harness.Run, u: c.Ctx, name: str) -> Series:
    """Put a run that may start late onto the universe's full calendar. If the history ends on
    the last decision day (the look-ahead check), a last day with an unknown return is added so
    that every decision has a row."""
    syms = u.panel.syms
    lo = u.start.toordinal()
    hi = max(run.days[-1].toordinal(), run.days[0].toordinal() + len(run.decisions))
    days = np.arange(lo, hi + 1, dtype=np.int64)
    n = len(days) - 1
    off = run.days[0].toordinal() - lo
    rets = np.full(n, np.nan)
    rets[off : off + len(run.rets)] = run.rets
    w = np.zeros((n, len(syms)))
    for k, d in enumerate(run.decisions):
        for s, x in d.weights.items():
            w[off + k, syms.index(s)] = x
    return Series(name, syms, days, rets, w, run.days[0].toordinal())


def save(universe: str, s: Series) -> None:
    p = path(universe, s.name)
    p.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(p, syms=np.array(s.syms), days=s.days, rets=s.rets, w=s.w, first=s.first)


def asset_returns(u: c.Ctx, days: np.ndarray) -> np.ndarray:
    """Close-to-close return of every asset on every calendar day after `days[0]` (0 on days
    without a bar): row k is day `days[k + 1]`, as in `Series.rets`."""
    lo, hi = int(days[0]), int(days[-1])
    out = np.zeros((hi - lo, len(u.panel.syms)))
    for j, s in enumerate(u.panel.syms):
        o, cl = u.panel.ord[s], u.panel.c[s]
        for i in range(1, len(o)):
            if lo < o[i] <= hi:
                out[o[i] - lo - 1, j] = cl[i] / cl[i - 1] - 1
    return out


def build(universe: str, names: list[str]) -> None:
    u = c.ctx(universe)
    for m in models_for(universe):
        if names and m.name not in names:
            continue
        horizon = int(os.environ.get("ML_HORIZON", "28"))
        if (m.name in WEEKLY_ML) != (horizon == 7):
            if names:
                raise SystemExit(f"{m.name}: wrong ML_HORIZON ({horizon})")
            continue
        t0 = time.time()
        start = m.first(u) if m.first else u.start
        tag = m.variant if universe == "six" else f"{m.variant}@{universe}"
        old = logged(m.idea, tag, start)
        if old is None:  # a configuration nobody ran: count it
            run = c.go("deep-1", f"{m.idea}/{m.variant}", m.make(u), u, "robustness", start=start)
        else:
            run = c.go(m.idea, m.variant, m.make(u), u, "robustness", log=False, start=start)
        sh = stats.sharpe(run.rets)
        note = "new, logged" if old is None else ("ok" if abs(sh - old) < 0.006 else "MISMATCH")
        print(f"{universe:5s} {m.name:13s} from {start} Sharpe {sh:.2f} "
              f"(logged {old if old is not None else '-'}) {note} [{time.time() - t0:.0f}s]",
              flush=True)  # fmt: skip
        if not c.DRY:
            save(universe, to_series(run, u, m.name))


if __name__ == "__main__":
    (OUT / "series" / sys.argv[1]).mkdir(parents=True, exist_ok=True)
    build(sys.argv[1], sys.argv[2:])
