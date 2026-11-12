"""Machine-learning rung: features, purged walk-forward fitting, forecast-to-position rules.

Everything here follows research/protocol.md, section "Machine-learning tests". The one way
data enters is `Panel.view(decide_time(day))`, so a row for Friday `d` is built from what a
decision on `d` could see, and its label from what a decision on `d + 28` could see. A fit on
date F only takes rows with `d + 28 + 7 <= F`.

Needs scikit-learn:  uv run --with numpy --with scikit-learn python research/lib/idea_ml_*.py
"""

from __future__ import annotations

import math
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, timedelta
from functools import cache
from typing import Any

import numpy as np
from common import (
    ResearchStrategy,
    View,
    Weights,
    bpy,
    live,
    sma_bars,
    sma_ratio,
    trailing_logret,
    vol_series,
)
from harness import (
    OOU_COINS,
    OOU_ETFS,
    OOU_INDEXES,
    SECTORS,
    SYMS,
    Panel,
    decide_time,
    load_history,
)
from sklearn.ensemble import HistGradientBoostingClassifier, HistGradientBoostingRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.metrics import log_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

HORIZON = 28  # label: log return over the next 28 days
EMBARGO = 7  # extra gap between the last usable label and the fit date
MIN_ROWS = 1000  # no model before this many labelled rows
CV_FOLDS = 5
Q_FLOOR = 0.05  # floor of (training average - neutral) in the confidence ratio
LOW_QUANTILE = 0.25  # `low` rule: out below this quantile of out-of-fold forecasts
WARMUP_END = date(1993, 1, 28)  # S&P 500 index rows up to the day before SPY exists

HORIZONS = (7, 30, 91, 182, 365)
FEATURES = [
    "z7", "z30", "z91", "z182", "z365", "up_12m", "sma_gap", "log_vol", "vol_shock", "dd_1y",
    "since_high", "breadth", "univ_mom_1m", "univ_vol_shock", "rank_12m",
]  # fmt: skip
N_OWN = 11
Z30, Z365, UP12, LOG_VOL, VOL_SHOCK = 1, 4, 5, 7, 8


# --- schedule (run 1's rule for fitted models: refit on the first Friday of each year) ---


def first_friday(year: int) -> date:
    d = date(year, 1, 1)
    return d + timedelta(days=(4 - d.weekday()) % 7)


def fit_year(today: date) -> int:
    return today.year if today >= first_friday(today.year) else today.year - 1


# --- features ---


def own_features(view: View, s: str) -> np.ndarray | None:
    """The 11 features of one asset, from its own visible closes. None if any is undefined."""
    key = ("ml-own", s, view.n[s])
    memo = view.panel.cache
    if key in memo:
        return memo[key]  # type: ignore[return-value]
    out: np.ndarray | None = None
    slow, fast = vol_series(view, s, 60), vol_series(view, s, 10)
    rets = [trailing_logret(view, s, h) for h in HORIZONS]
    gap = sma_ratio(view, s, sma_bars(s))
    if len(slow) and slow[-1] > 0 and fast[-1] > 0 and not any(map(math.isnan, [*rets, gap])):
        vol = float(slow[-1])
        z = [float(np.clip(r / (vol * math.sqrt(h / 365)), -5, 5)) for r, h in zip(rets, HORIZONS)]  # noqa: B905
        c = view.close(s)[-bpy(s) :]
        hi = int(np.argmax(c))
        out = np.array(
            [
                *z,
                1.0 if rets[-1] > 0 else 0.0,
                math.log(gap) / vol,
                math.log(vol),
                math.log(float(fast[-1]) / vol),
                math.log(c[-1] / c[hi]) / vol,
                (len(c) - 1 - hi) / bpy(s),
            ]
        )
    memo[key] = out
    return out


def rows_at(view: View) -> dict[str, np.ndarray]:
    """Full feature vector of every eligible asset at this view (own + cross-asset)."""
    key = ("ml-rows", tuple(view.n[s] for s in view.syms))
    memo = view.panel.cache
    if key in memo:
        return memo[key]  # type: ignore[return-value]
    own = {s: f for s in live(view) if (f := own_features(view, s)) is not None}
    out: dict[str, np.ndarray] = {}
    if own:
        m = np.array(list(own.values()))
        breadth, mom, shock = m[:, UP12].mean(), m[:, Z30].mean(), m[:, VOL_SHOCK].mean()
        order = m[:, Z365].argsort().argsort()
        for k, (s, f) in enumerate(own.items()):
            rank = order[k] / (len(own) - 1) if len(own) > 1 else 0.5
            out[s] = np.concatenate([f, [breadth, mom, shock, rank]])
    memo[key] = out
    return out


# --- labelled rows ---


@dataclass
class Rows:
    day: np.ndarray  # ordinal of the Friday the row was decided on
    x: np.ndarray  # (n, 15)
    fwd: np.ndarray  # log return over the next 28 days
    sym: list[str]

    def __len__(self) -> int:
        return len(self.fwd)


def _empty() -> Rows:
    return Rows(np.array([], dtype=np.int64), np.empty((0, len(FEATURES))), np.array([]), [])


def _concat(parts: list[Rows]) -> Rows:
    parts = [p for p in parts if len(p)]
    if not parts:
        return _empty()
    return Rows(
        np.concatenate([p.day for p in parts]),
        np.vstack([p.x for p in parts]),
        np.concatenate([p.fwd for p in parts]),
        [s for p in parts for s in p.sym],
    )


def labelled(panel: Panel, d: date) -> Rows:
    """Rows decided on Friday `d` with their 28-day labels. Uses bars visible at `d + 28`: the
    caller must only ask for days whose label window has closed (see `training_rows`)."""
    key = ("ml-lab", d)
    if key not in panel.cache:
        now, later = panel.view(decide_time(d)), panel.view(decide_time(d + timedelta(HORIZON)))
        days, xs, fwd, syms = [], [], [], []
        for s, x in rows_at(now).items():
            if later.n[s] > now.n[s]:
                days.append(d.toordinal())
                xs.append(x)
                fwd.append(math.log(panel.c[s][later.n[s] - 1] / panel.c[s][now.n[s] - 1]))
                syms.append(s)
        panel.cache[key] = (
            Rows(np.array(days, dtype=np.int64), np.array(xs), np.array(fwd), syms)
            if days
            else _empty()
        )
    return panel.cache[key]  # type: ignore[return-value]


def fridays(panel: Panel, last: date) -> list[date]:
    first = min(date.fromordinal(int(o[0])) for o in panel.ord.values() if len(o))
    d = first + timedelta(days=(4 - first.weekday()) % 7)
    out = []
    while d <= last:
        out.append(d)
        d += timedelta(days=7)
    return out


@cache
def warmup_rows() -> Rows:
    """S&P 500 index, 1962 to the day before SPY's first bar: extra training rows for any
    universe that holds SPY. All of it predates the first decision of every test."""
    bars = [b for b in load_history("train", True, ["GSPC"])["GSPC"] if b.date <= WARMUP_END]
    panel = Panel({"GSPC": [b for b in bars if b.date.year >= 1961]})
    last = WARMUP_END - timedelta(HORIZON)
    return _concat([labelled(panel, d) for d in fridays(panel, last)])


def training_rows(panel: Panel, fit_day: date) -> Rows:
    """Rows usable at a fit on `fit_day`: label window closed at least EMBARGO days before."""
    last = fit_day - timedelta(HORIZON + EMBARGO)
    parts = [labelled(panel, d) for d in fridays(panel, last)]
    if "SPY" in panel.syms:
        parts.insert(0, warmup_rows())
    return _concat(parts)


# --- pooled training rows (protocol.md, "Pooled training") ---

POOL_SETS = {"six": SYMS, "etf": OOU_ETFS, "sector": SECTORS, "coin": OOU_COINS, "idx": OOU_INDEXES}


def pool_history() -> dict[str, dict[str, list[Any]]]:
    out = {}
    for name, syms in POOL_SETS.items():
        hist = load_history("train", True, syms)
        if name == "idx":  # as `common.ctx("idx")`: the S&P 500 index from 1961
            hist["GSPC"] = [b for b in hist["GSPC"] if b.date.year >= 1961]
        out[name] = hist
    return out


@cache
def pool_panels() -> dict[str, Panel]:
    return {name: Panel(hist) for name, hist in pool_history().items()}


def pooled_rows(fit_day: date, panels: Mapping[str, Panel] | None = None) -> Rows:
    """Rows of all five sets usable at a fit on `fit_day`, each set with its own cross-asset
    features. No warm-up rows: the index set already holds the S&P 500 from 1962. The same rows
    whichever universe is traded."""
    last = fit_day - timedelta(HORIZON + EMBARGO)
    panels = pool_panels() if panels is None else panels
    return _concat([labelled(p, d) for p in panels.values() for d in fridays(p, last)])


def rows_for(spec: Spec, panel: Panel, fit_day: date) -> Rows:
    return pooled_rows(fit_day) if spec.pool else training_rows(panel, fit_day)


# --- models ---


@dataclass(frozen=True)
class Spec:
    """A model configuration. More than one entry in `grid` means: chosen by purged CV at
    every fit. `meta`: train only on rows where the 12-month trend rule was holding."""

    name: str
    family: str  # "logit" | "ridge" | "gbm" | "tree"
    target: str  # "up" | "ra" | "raw"
    grid: tuple[tuple[tuple[str, float], ...], ...]
    meta: bool = False
    weight: str = ""  # "pay": rows weighted by |28-day log return| (protocol: payoff weights)
    pool: bool = False  # train on the rows of all five sets (protocol: pooled training)


def _grid(*settings: Mapping[str, float]) -> tuple[tuple[tuple[str, float], ...], ...]:
    return tuple(tuple(sorted(s.items())) for s in settings)


GBM_BASE = {
    "learning_rate": 0.05, "max_iter": 100, "max_depth": 3, "min_samples_leaf": 100,
    "l2_regularization": 1.0,
}  # fmt: skip


def gbm_spec(name: str, target: str = "up", meta: bool = False, **change: float) -> Spec:
    return Spec(name, "gbm", target, _grid({**GBM_BASE, **change}), meta)


LOGIT = Spec("logit", "logit", "up", _grid(*[{"C": c} for c in (0.001, 0.01, 0.1, 1.0)]))
RIDGE = Spec("ridge", "ridge", "ra", _grid(*[{"alpha": a} for a in (10, 100, 1000, 10000)]))
GBM = gbm_spec("gbm")
GBM_REG = gbm_spec("gbm-reg", target="ra")
GBM_CV = Spec(
    "gbm-cv", "gbm", "up",
    _grid(*[{**GBM_BASE, "max_depth": d, "max_iter": n} for d in (1, 3) for n in (25, 100, 400)]),
)  # fmt: skip
GBM_SWEEP = [
    gbm_spec("gbm-d1", max_depth=1),
    gbm_spec("gbm-d6", max_depth=6),
    gbm_spec("gbm-n25", max_iter=25),
    gbm_spec("gbm-n400", max_iter=400),
    gbm_spec("gbm-leaf20", min_samples_leaf=20),
]
GBM_PAY = Spec("gbm-pay", "gbm", "up", _grid(GBM_BASE), weight="pay")
LOGIT_PAY = Spec("logit-pay", "logit", "up", LOGIT.grid, weight="pay")
TREE_PAY = Spec(
    "tree-pay", "tree", "up", _grid({"max_depth": 2, "min_samples_leaf": 200}), weight="pay"
)
GBM_RAW = gbm_spec("gbm-raw", target="raw")
GBM_POOL = Spec("gbm-pool", "gbm", "up", _grid(GBM_BASE), pool=True)
LOGIT_POOL = Spec("logit-pool", "logit", "up", LOGIT.grid, pool=True)
META_GBM = gbm_spec("meta-gbm", meta=True)
META_LOGIT = Spec("meta-logit", "logit", "up", LOGIT.grid, meta=True)


def _estimator(spec: Spec, setting: tuple[tuple[str, float], ...]) -> Any:
    p = dict(setting)
    if spec.family == "logit":
        return make_pipeline(StandardScaler(), LogisticRegression(C=p["C"], max_iter=2000))
    if spec.family == "ridge":
        return make_pipeline(StandardScaler(), Ridge(alpha=p["alpha"]))
    if spec.family == "tree":
        return DecisionTreeClassifier(
            max_depth=int(p["max_depth"]),
            min_samples_leaf=int(p["min_samples_leaf"]),
            random_state=0,
        )
    kw = {
        "learning_rate": p["learning_rate"],
        "max_iter": int(p["max_iter"]),
        "max_depth": int(p["max_depth"]),
        "min_samples_leaf": int(p["min_samples_leaf"]),
        "l2_regularization": p["l2_regularization"],
        "early_stopping": False,
        "random_state": 0,
    }
    cls = HistGradientBoostingClassifier if spec.target == "up" else HistGradientBoostingRegressor
    return cls(**kw)


def target(spec: Spec, rows: Rows) -> np.ndarray:
    if spec.target == "up":
        return (rows.fwd > 0).astype(float)
    if spec.target == "raw":
        return rows.fwd.copy()
    vol = np.exp(rows.x[:, LOG_VOL])
    return np.clip(rows.fwd / (vol * math.sqrt(HORIZON / 365)), -3, 3)


def row_weights(spec: Spec, rows: Rows) -> np.ndarray | None:
    """Payoff weights: |28-day log return| over its mean in these rows. None = unweighted."""
    if spec.weight != "pay":
        return None
    w = np.abs(rows.fwd)
    return w / w.mean()


def _fit_est(
    spec: Spec,
    setting: tuple[tuple[str, float], ...],
    x: np.ndarray,
    y: np.ndarray,
    w: np.ndarray | None,
) -> Any:
    est = _estimator(spec, setting)
    if w is None:
        return est.fit(x, y)
    if hasattr(est, "steps"):
        return est.fit(x, y, **{f"{est.steps[-1][0]}__sample_weight": w})
    return est.fit(x, y, sample_weight=w)


def _forecast(spec: Spec, est: Any, x: np.ndarray) -> np.ndarray:
    out = est.predict_proba(x)[:, 1] if spec.target == "up" else est.predict(x)
    return np.asarray(out, dtype=float)


def purged_folds(day: np.ndarray, k: int = CV_FOLDS) -> list[tuple[np.ndarray, np.ndarray]]:
    """Purged, embargoed K-fold in time order. For a validation block of decision days [a, b]:
    training rows whose label window overlaps the block's (a - 28 <= d <= b + 28) are purged,
    and the 28 days after that (d <= b + 56) are embargoed."""
    out = []
    for block in np.array_split(np.unique(day), k):
        a, b = block[0], block[-1]
        val = (day >= a) & (day <= b)
        train = (day < a - HORIZON) | (day > b + 2 * HORIZON)
        out.append((train, val))
    return out


def cv_score(spec: Spec, setting: tuple[tuple[str, float], ...], rows: Rows) -> float:
    y, w = target(spec, rows), row_weights(spec, rows)
    scores = []
    for train, val in purged_folds(rows.day):
        est = _fit_est(spec, setting, rows.x[train], y[train], None if w is None else w[train])
        f = _forecast(spec, est, rows.x[val])
        wv = None if w is None else w[val]
        if spec.target == "up":
            f = np.clip(f, 1e-6, 1 - 1e-6)
            scores.append(log_loss(y[val], f, labels=[0.0, 1.0], sample_weight=wv))
        else:
            scores.append(float(np.average((f - y[val]) ** 2, weights=wv)))
    return float(np.mean(scores))


@dataclass
class Fitted:
    spec: Spec
    est: Any
    avg: float  # mean label in the training rows
    setting: tuple[tuple[str, float], ...]
    n_rows: int

    @property
    def neutral(self) -> float:
        return 0.5 if self.spec.target == "up" else 0.0

    def forecast(self, x: np.ndarray) -> np.ndarray:
        return _forecast(self.spec, self.est, x)

    def confidence(self, x: np.ndarray) -> np.ndarray:
        return (self.forecast(x) - self.neutral) / max(self.avg - self.neutral, Q_FLOOR)


def fit(spec: Spec, rows: Rows) -> Fitted:
    if spec.meta:
        keep = rows.x[:, UP12] == 1
        rows = Rows(rows.day[keep], rows.x[keep], rows.fwd[keep], [])
    setting = spec.grid[0]
    if len(spec.grid) > 1:
        setting = min(spec.grid, key=lambda g: cv_score(spec, g, rows))
    y, w = target(spec, rows), row_weights(spec, rows)
    est = _fit_est(spec, setting, rows.x, y, w)
    return Fitted(spec, est, float(np.average(y, weights=w)), setting, len(y))


def oof_quantile(model: Fitted, rows: Rows, q: float = LOW_QUANTILE) -> float:
    """A quantile of the model's out-of-fold forecasts on its training rows (purged folds,
    the setting in force). The threshold of the `low` position rule."""
    spec = model.spec
    if spec.meta:
        keep = rows.x[:, UP12] == 1
        rows = Rows(rows.day[keep], rows.x[keep], rows.fwd[keep], [])
    y, w = target(spec, rows), row_weights(spec, rows)
    parts = []
    for train, val in purged_folds(rows.day):
        est = _fit_est(
            spec, model.setting, rows.x[train], y[train], None if w is None else w[train]
        )
        parts.append(_forecast(spec, est, rows.x[val]))
    return float(np.quantile(np.concatenate(parts), q))


SIZINGS = ("base", "hard", "prop", "low")


def position(sizing: str, forecast: float, q: float, low: float) -> float:
    """Share of the slot to hold (protocol.md: the first rule and its `-hard`, `-prop`, `-low`
    forms). `q` is the confidence ratio, `low` the out-of-fold 25th-percentile forecast."""
    if sizing == "base":
        return min(max(q, 0.0), 1.0)
    if sizing == "hard":
        return 1.0 if q > 0 else 0.0
    if sizing == "prop":
        return min(max(q / 2, 0.0), 1.0)
    if sizing == "low":
        return 1.0 if forecast >= low else 0.0
    raise ValueError(sizing)


def model_for(view: View, spec: Spec) -> Fitted | None:
    """The model in force at this view: fitted on the first Friday of the year (of the bars
    visible then). None while fewer than MIN_ROWS labelled rows exist."""
    year = fit_year(view.today)
    key = ("ml-model", spec.name, year)
    memo = view.panel.cache
    if key not in memo:
        fit_day = first_friday(year)
        assert fit_day <= view.today
        rows = rows_for(spec, view.panel, fit_day)
        memo[key] = fit(spec, rows) if len(rows) >= MIN_ROWS else None
    return memo[key]  # type: ignore[return-value]


def low_for(view: View, model: Fitted) -> float:
    """The `low` threshold of the model in force (same fit day, same rows as the model)."""
    year = fit_year(view.today)
    key = ("ml-low", model.spec.name, year)
    memo = view.panel.cache
    if key not in memo:
        memo[key] = oof_quantile(model, rows_for(model.spec, view.panel, first_friday(year)))
    return memo[key]  # type: ignore[return-value]


def first_fit_day(panel: Panel, not_before: date) -> date:
    """The first yearly fit day with at least MIN_ROWS rows (trading starts there)."""
    last = max(date.fromordinal(int(o[-1])) for o in panel.ord.values() if len(o))
    for year in range(not_before.year, last.year + 1):
        if len(training_rows(panel, first_friday(year))) >= MIN_ROWS:
            return max(first_friday(year), not_before)
    raise ValueError("never enough rows")


# --- strategies ---


def strategy(
    spec: Spec,
    *,
    sizing: str = "base",
    hard: bool = False,
    trend_only: bool = False,
    tag: str | None = None,
) -> ResearchStrategy:
    """Equal slots; each slot scaled by `position(sizing, ...)`. `hard=True` is the old name for
    sizing="hard". `trend_only`: only where tsmom12 holds. Forecasts are remembered per panel
    under `tag` for the skill tables."""
    sizing = "hard" if hard else sizing
    assert sizing in SIZINGS
    tag = tag or spec.name
    trend_only = trend_only or spec.meta

    def f(view: View) -> Weights:
        model = model_for(view, spec)
        held = live(view)
        rows = rows_at(view)
        syms = [s for s in held if s in rows and not (trend_only and rows[s][UP12] != 1)]
        if model is None or not syms:
            return {}
        x = np.array([rows[s] for s in syms])
        fc, q = model.forecast(x), model.confidence(x)
        low = low_for(view, model) if sizing == "low" else math.nan
        log = view.panel.cache.setdefault(("ml-fc", tag), {})
        out = {}
        for s, p, qi in zip(syms, fc, q, strict=True):
            log[(view.today, s)] = float(p)  # type: ignore[index]
            w = position(sizing, float(p), float(qi), low)
            if w > 0:
                out[s] = w / len(held)
        return out

    return f


# --- reading the forecasts back (skill tables; no new backtests) ---


def skill(panel: Panel, tag: str, neutral: float = 0.5) -> dict[str, float]:
    """How well the walk-forward forecasts ranked the realised 28-day outcomes."""
    log: dict[tuple[date, str], float] = panel.cache.get(("ml-fc", tag), {})  # type: ignore[assignment]
    last = max(date.fromordinal(int(o[-1])) for o in panel.ord.values() if len(o))
    fc, up, base, size = [], [], [], []
    for (d, s), p in log.items():
        if d.weekday() != 4 or d + timedelta(HORIZON) > last:
            continue
        rows = labelled(panel, d)
        if s in rows.sym:
            k = rows.sym.index(s)
            fc.append(p)
            up.append(rows.fwd[k] > 0)
            base.append(rows.x[k, UP12])
            size.append(abs(rows.fwd[k]))
    f, u, b, w = np.array(fc), np.array(up), np.array(base), np.array(size)
    if len(f) < 50 or u.all() or not u.any():
        return {"n": float(len(f))}
    return {
        "n": float(len(f)),
        "up_share": float(u.mean()),
        "auc": float(roc_auc_score(u, f)),
        "hit": float(((f > neutral) == u).mean()),
        "said_up": float((f > neutral).mean()),
        "auc_up12": float(roc_auc_score(u, b)) if 0 < b.mean() < 1 else math.nan,
        "hit_up12": float(((b == 1) == u).mean()),
        # the same hit rates with each month counted by the size of its move
        "gain": float(np.average((f > neutral) == u, weights=w)),
        "gain_always": float(np.average(u, weights=w)),
        "gain_up12": float(np.average((b == 1) == u, weights=w)),
    }


def settings_used(panel: Panel, spec: Spec) -> list[tuple[int, int, str]]:
    """(year, training rows, setting chosen) for every fit of this spec on this panel."""
    out = []
    for key, m in panel.cache.items():
        if isinstance(key, tuple) and key[:2] == ("ml-model", spec.name) and m is not None:
            assert isinstance(m, Fitted)
            varied = {k for g in spec.grid for k, v in g if dict(spec.grid[0])[k] != v}
            text = ", ".join(f"{k}={v:g}" for k, v in m.setting if k in varied) or "fixed"
            out.append((int(key[2]), m.n_rows, text))
    return sorted(out)


def permutation_importance(model: Fitted, rows: Rows, seed: int = 0) -> list[tuple[str, float]]:
    """Drop in AUC (or rise in squared error) when one feature is shuffled, on the given rows."""
    rng = np.random.default_rng(seed)
    y = target(model.spec, rows)

    def score(x: np.ndarray) -> float:
        f = model.forecast(x)
        if model.spec.target == "up":
            return float(roc_auc_score(y, f))
        return -float(((f - y) ** 2).mean())

    base = score(rows.x)
    out = []
    for j, name in enumerate(FEATURES):
        drops = []
        for _ in range(5):
            x = rows.x.copy()
            x[:, j] = rng.permutation(x[:, j])
            drops.append(base - score(x))
        out.append((name, float(np.mean(drops))))
    return sorted(out, key=lambda t: -t[1])
