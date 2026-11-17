# ruff: noqa: E501
"""The forecasters and the gate of run rl-4 (research/rl-4.md, card part 1). A control experiment.

    uv run --with torch python research/lib/rl4_sup.py --smoke        # shapes only, no numbers
    uv run --with torch python research/lib/rl4_sup.py [variant ...]  # logs control rows
    uv run python research/lib/rl4_sup.py --report                    # results/rl-4.md

Per walk-forward fold (rl-3's 13 folds and embargo) a forecaster of the coming week's
risk-adjusted return (`rl3_plant.week_z`) is fitted on the eligible cells before the fold's cut.
score = C x (forecast - intercept) goes through RL 2's residual action and `gym.simulate`.
Writes research/data/rl/sup4-<variant>-<rho>.json. The ceiling is rl-3's (ceil3-<rho>.json).
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

IDEA = "rl-4-control"
C = 10.0  # score per unit of forecast (card: a clean IC-0.10 forecast gets unit scale)
STRENGTHS = ["0.00", "0.05", "0.10", "0.20"]
UP12, LOG_VOL, PEEK = 5, 7, 17  # columns of the planted asset inputs (17 real + peek)
N_ASSET, N_MACRO = 18, 10
SMALL = ("six", "gspc")
POOL = ("six", "gspc", "etf", "sec", "coin", "idx")
EXTRA_SEEDS = {"etf": 303, "sec": 304, "coin": 305, "idx": 306}  # rl-3 fixed six 301, gspc 302
RIDGE_GRID = [10.0, 3.0, 1.0, 0.3, 0.1, 0.03, 0.01]  # penalty / rows, largest first
LASSO_GRID = [0.08, 0.05, 0.03, 0.02, 0.01, 0.005]  # sklearn alpha, largest first
CV_FOLDS, CV_GAP = 5, 14  # days dropped on each side of a validation fold (purge + embargo)
CAPTURE, NOISE_LOSS = 0.33, -0.025  # gate bars 2 and 4
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "data" / "rl"


@dataclass(frozen=True)
class Spec:
    name: str
    cols: tuple[int, ...] | None  # asset columns used; None = all 18 asset + 10 macro
    books: tuple[str, ...]
    fit: str  # ols | ridge | lasso


SPECS = {
    s.name: s
    for s in [
        Spec("ols28", None, SMALL, "ols"),
        Spec("ols3", (PEEK, UP12, LOG_VOL), SMALL, "ols"),
        Spec("ridge28", None, SMALL, "ridge"),
        Spec("lasso28", None, SMALL, "lasso"),
        Spec("ols28-pool", None, POOL, "ols"),
        Spec("ols1", (PEEK,), SMALL, "ols"),  # post-hoc diagnostic, not on the card
    ]
}
POSTHOC = {"ols1"}


# --- pure helpers (numpy and scikit-learn only; tests import these) ---


def design(xa: np.ndarray, g: np.ndarray, cols: tuple[int, ...] | None) -> np.ndarray:
    """[F, n, k] inputs of one book: the chosen asset columns, or all of them plus the macro
    inputs repeated across assets (NaN where a macro series has not started)."""
    if cols is not None:
        return xa[:, :, list(cols)]
    return np.concatenate([xa, np.repeat(g[:, None, :], xa.shape[1], 1)], 2)


@dataclass
class Fit:
    mu: np.ndarray
    sd: np.ndarray
    beta: np.ndarray  # on standardised inputs; the intercept is not part of the score
    penalty: float | None

    def score(self, x: np.ndarray) -> np.ndarray:
        """C x (forecast - intercept) for inputs of any leading shape."""
        return C * (np.nan_to_num((x - self.mu) / self.sd) @ self.beta)


def standardise(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mu = np.nan_to_num(np.nanmean(np.where(np.isfinite(x), x, np.nan), 0))
    sd = np.nan_to_num(np.nanstd(np.where(np.isfinite(x), x, np.nan), 0))
    sd = np.where(sd > 1e-9, sd, 1.0)
    return np.nan_to_num((x - mu) / sd), mu, sd


def cv_folds(days: np.ndarray) -> list[tuple[np.ndarray, np.ndarray]]:
    """Purged folds in time order: (training rows, validation rows) as boolean masks. Equal row
    counts per fold; training rows within CV_GAP days of the validation fold are dropped."""
    order = np.argsort(days, kind="mergesort")
    out = []
    for part in np.array_split(order, CV_FOLDS):
        val = np.zeros(len(days), bool)
        val[part] = True
        lo, hi = days[part].min(), days[part].max()
        out.append((~val & ((days < lo - CV_GAP) | (days > hi + CV_GAP)), val))
    return out


def _solve(kind: str, xs: np.ndarray, y: np.ndarray, pen: float) -> np.ndarray:
    yc = y - y.mean()
    if kind == "ols":
        return np.asarray(np.linalg.lstsq(xs, yc, rcond=None)[0])
    if kind == "ridge":
        a = xs.T @ xs + pen * len(y) * np.eye(xs.shape[1])
        return np.asarray(np.linalg.solve(a, xs.T @ yc))
    from sklearn.linear_model import Lasso

    return np.asarray(Lasso(alpha=pen, max_iter=20_000).fit(xs, yc).coef_)


def fit(kind: str, x: np.ndarray, y: np.ndarray, days: np.ndarray) -> Fit:
    """Fit on training rows x [N, k], target y, row dates `days` (ordinals, for the purged CV)."""
    xs, mu, sd = standardise(x)
    if kind == "ols":
        return Fit(mu, sd, _solve("ols", xs, y, 0.0), None)
    grid = RIDGE_GRID if kind == "ridge" else LASSO_GRID
    folds = cv_folds(days)
    mse = []
    for pen in grid:
        errs = []
        for tr, va in folds:
            b = _solve(kind, xs[tr], y[tr], pen)
            errs.append(float(((y[va] - y[tr].mean() - xs[va] @ b) ** 2).mean()))
        mse.append(float(np.mean(errs)))
    pen = grid[int(np.argmin(mse))]  # ties go to the larger penalty (the grid is largest first)
    return Fit(mu, sd, _solve(kind, xs, y, pen), pen)


def gate(
    by_rho: dict[str, dict[str, Any]], ceiling_010: float, rl: bool = False
) -> dict[str, bool]:
    """The card's bars from a learner's results at each strength (keys: diff, p, seeds_ahead)."""
    r0, r1, r2 = by_rho["0.00"], by_rho["0.10"], by_rho["0.20"]

    def found(r: dict[str, Any]) -> bool:
        return bool(r["diff"] > 0 and r["p"] < 0.10)

    bars = {
        "1 finds 0.10 (gain > 0, p < 0.10)": found(r1),
        "2 captures >= 33% of the ceiling at 0.10": r1["diff"] / ceiling_010 >= CAPTURE,
        "3 finds 0.20": found(r2),
        "4 noise: not found, gain >= -0.025": (not found(r0)) and r0["diff"] >= NOISE_LOSS,
    }
    if rl:
        bars["5 >= 7 of 10 seeds ahead at 0.10"] = r1["seeds_ahead"] >= 7
    return bars


# --- the run (needs the price cache and RL 2's tables) ---


def planted(rho: float, books: tuple[str, ...]) -> dict[str, Any]:
    import rl2_data
    import rl3_plant

    seeds = {**rl3_plant.SEEDS, **EXTRA_SEEDS}
    tabs = rl2_data.load()
    return {k: rl3_plant.plant(tabs[k], rho, seeds[k]) for k in books}


def fold_fits(spec: Spec, tabs: dict[str, Any]) -> dict[int, Fit]:
    import rl3_plant
    from rl_train import FOLDS, train_end

    parts = []
    for rt in tabs.values():
        t = rt.t
        z = rl3_plant.week_z(t)
        d = np.repeat(np.array([x.toordinal() for x in t.fridays])[:, None], z.shape[1], 1)
        parts.append((t, z, design(t.X, t.G, spec.cols), d))
    out = {}
    for y in FOLDS:
        xs, ys, ds = [], [], []
        for t, z, x, d in parts:
            e = train_end(t, y)
            tr = np.isfinite(z[:e]) & t.elig[:e]
            xs.append(x[:e][tr])
            ys.append(z[:e][tr])
            ds.append(d[:e][tr])
        out[y] = fit(spec.fit, np.concatenate(xs), np.concatenate(ys), np.concatenate(ds))
    return out


def scores(spec: Spec, tabs: dict[str, Any], fits: dict[int, Fit]) -> np.ndarray:
    """[F, n] scores on the six assets: fold Y's model from the first Friday of Y to that of Y + 2."""
    from ml import first_friday
    from rl_train import FOLDS

    t = tabs["six"].t
    x = design(t.X, t.G, spec.cols)
    s = np.zeros(t.elig.shape)
    for y in FOLDS:
        a = t.index(first_friday(y))
        b = t.index(first_friday(y + 2)) if y + 2 <= 2025 else len(t.fridays)
        s[a:b] = np.where(t.elig[a:b], fits[y].score(x[a:b]), 0.0)
    return s


def evaluate(name: str) -> None:
    import common as c
    import rl2_env
    import rl3_eval
    import rl3_plant
    import stats
    from harness import TRAIN_END

    rl3_eval.IDEA = IDEA
    r1, hist, base = rl3_eval._common()
    ts = base["tsmom12"]
    spec = SPECS[name]
    start, since = rl3_eval.OOS_START, rl3_eval.SINCE
    for rho in STRENGTHS:
        tabs = planted(float(rho), spec.books)
        fits = fold_fits(spec, tabs)
        rt = tabs["six"]
        t = rt.t
        s_all = scores(spec, tabs, fits)
        i0 = t.index(start)
        sc = s_all[i0:]
        bd = rl2_env.base_daily(hist, t.book.syms, start, TRAIN_END)
        key = f"{name}-{rho}"
        run = r1.log_run(key, "control", rl2_env.res_decisions(rt, i0, sc[:, None, :], bd, TRAIN_END),
                         hist, start, TRAIN_END)  # fmt: skip
        w = rl2_env.residual(rt.B[i0:], rt.L[i0:], t.elig[i0:], rt.coin, sc)
        z = rl3_plant.week_z(t)
        keep = np.isfinite(z) & t.elig
        keep[:i0] = False
        pk = t.X[:, :, PEEK]
        el = t.elig[i0:] & rt.L[i0:]
        tilt = w - rt.B[i0:]
        d, p = r1.vs(run, ts)
        e_run, e_ts = c.era_sharpes(run), c.era_sharpes(ts)
        live = s_all[keep].std() > 0
        out = {
            "variant": name, "rho": float(rho), **r1.describe(run), "diff": d, "p": p,
            "since2003_diff": r1.vs(run, ts, since)[0],
            "eras_ahead": sum(e_run[k] > e_ts[k] for k in rl3_eval.ERAS),
            "tsmom12": r1.describe(ts),
            "forecast_ic": float(np.corrcoef(s_all[keep], z[keep])[0, 1]) if live else 0.0,
            "corr_score_peek": float(np.corrcoef(s_all[keep], pk[keep])[0, 1]) if live else 0.0,
            "tilt_peek_corr": float(np.corrcoef(tilt[el], pk[i0:][el])[0, 1]) if tilt[el].std() > 0 else 0.0,
            "active": rl2_env.active_share(w, rt.B[i0:]),
            "score_sd": float(s_all[keep].std()),
            "penalties": [f.penalty for f in fits.values()],
            "peek_beta": [float(f.beta[spec.cols.index(PEEK) if spec.cols else PEEK]) for f in fits.values()],
            "nonzero": [int((f.beta != 0).sum()) for f in fits.values()],
        }  # fmt: skip
        (OUT / f"sup4-{key}.json").write_text(json.dumps(out, indent=1, default=r1._json))
        print(key, f"Sharpe {stats.sharpe(run.rets):.3f} d {d:+.3f} p {p:.2f} "
              f"IC {out['forecast_ic']:+.3f} corr(tilt,peek) {out['tilt_peek_corr']:+.2f}", flush=True)  # fmt: skip


def smoke() -> None:
    """Plumbing check: fits one fold of every forecaster and prints shapes only."""
    from rl_train import FOLDS

    for name, spec in SPECS.items():
        tabs = planted(0.10, spec.books)
        fits = fold_fits(spec, tabs)
        s = scores(spec, tabs, fits)
        print(name, "books", len(tabs), "beta", fits[FOLDS[-1]].beta.shape, "scores", s.shape,
              "finite", bool(np.isfinite(s).all()), flush=True)  # fmt: skip


# --- report (no backtests) ---


def f(x: object, spec: str = ".2f") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "-"
    return format(x, spec)


def _ceiling() -> dict[str, float]:
    out = {}
    for rho in STRENGTHS:
        cj = json.loads((OUT / f"ceil3-{rho}.json").read_text())
        out[rho] = cj["rules"][cj["best"]]["sharpe"] - cj["tsmom12"]["sharpe"]
    return out


def collect() -> tuple[dict[str, dict[str, dict[str, Any]]], dict[str, float]]:
    """{learner: {rho: result}} for the forecasters (sup4-*) and the PPO runs (eval3-ppo3*)."""
    res: dict[str, dict[str, dict[str, Any]]] = {}
    for p in sorted(OUT.glob("sup4-*.json")):
        j = json.loads(p.read_text())
        res.setdefault(j["variant"], {})[f"{j['rho']:.2f}"] = j
    for p in sorted(OUT.glob("eval3-ppo3*.json")):
        j = json.loads(p.read_text())
        e, vt = j["ensemble"], j["vs_tsmom12"]
        res.setdefault(j["config"].rsplit("-", 1)[0], {})[f"{j['rho']:.2f}"] = {
            **e, "diff": vt["diff"], "p": vt["p"], "since2003_diff": vt["since2003_diff"],
            "eras_ahead": vt["eras_ahead"], "tilt_peek_corr": j["tilt_peek_corr"],
            "active": j["active_share"], "seeds_ahead": j["seeds"]["ahead"],
            "seed_sharpes": j["seeds"]["sharpe"], "zero_share": j["chosen_zero_share"],
        }  # fmt: skip
    return res, _ceiling()


def report() -> None:
    res, ceil = collect()
    order = [k for k in [*SPECS, "ppo3", "ppo3-warm"] if k in res]
    L = [
        "# RL 4, part 1: the planted-signal gate (train period, out of sample 2000-01-07 to 2025-11-09)",
        "",
        "A control experiment, not a strategy (`research/rl-4.md`). Scripts `lib/rl4_sup.py`,",
        "`lib/rl4_train.py`. rl-3's planted input `peek` (exact IC in every calendar year) on the six",
        "assets, rl-3's residual action, every row a replay through `gym.simulate`. Gain and p against",
        "`tsmom12` (Sharpe 0.99 on the same days): paired stationary bootstrap, one-sided. Ceiling =",
        "rl-3's best known-signal rule: "
        + ", ".join(f"{ceil[r]:+.3f} at {r}" for r in STRENGTHS)
        + ".",
        "Captured = gain / ceiling.",
        "",
        "## The gate",
        "",
        "| Learner | Gain at 0.10 (p) | Captured at 0.10 | Gain at 0.20 (p) | Captured at 0.20 | Gain at 0.00 (p) | Bars passed | Gate |",
        "|---|---:|---:|---:|---:|---:|---|---|",
    ]
    for k in order:
        r = res[k]
        if not all(s in r for s in ("0.00", "0.10", "0.20")):
            continue
        bars = gate(r, ceil["0.10"], rl=k.startswith("ppo"))
        ok = [b.split()[0] for b, v in bars.items() if v]
        L.append(
            f"| `{k}`{' (post-hoc)' if k in POSTHOC else ''} | {f(r['0.10']['diff'], '+.3f')} ({f(r['0.10']['p'])}) | {r['0.10']['diff'] / ceil['0.10']:.0%} "
            f"| {f(r['0.20']['diff'], '+.3f')} ({f(r['0.20']['p'])}) | {r['0.20']['diff'] / ceil['0.20']:.0%} "
            f"| {f(r['0.00']['diff'], '+.3f')} ({f(r['0.00']['p'])}) | {', '.join(ok) or 'none'} of {len(bars)} "
            f"| {'**passes**' if all(bars.values()) else 'fails'} |"
        )
    L += [
        "",
        "## Every learner and strength",
        "",
        "| Learner | IC | Sharpe | Gain vs tsmom12 (p) | Captured | Since 2003 | Eras ahead | Worst loss "
        "| Active share | corr(tilt, peek) | Forecast IC | Weight on `peek`: median [min..max] | Penalty: median [min..max] | Inputs kept (median) | Seeds ahead |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|",
    ]
    for k in order:
        for rho in STRENGTHS:
            if rho not in res[k]:
                continue
            r = res[k][rho]
            cap = f"{r['diff'] / ceil[rho]:.0%}" if ceil[rho] > 0.005 else "-"
            pb = r.get("peek_beta")
            pen = [x for x in r.get("penalties", []) if x is not None]
            L.append(
                f"| `{k}` | {rho} | {f(r['sharpe'])} | {f(r['diff'], '+.3f')} ({f(r['p'])}) | {cap} "
                f"| {f(r['since2003_diff'], '+.3f')} | {r['eras_ahead']}/4 | {f(r['mdd'], '.1%')} "
                f"| {f(r['active'], '.1%')} | {f(r['tilt_peek_corr'], '+.2f')} | {f(r.get('forecast_ic'), '+.3f')} "
                f"| {f'{np.median(pb):+.3f} [{min(pb):+.3f}..{max(pb):+.3f}]' if pb else '-'} "
                f"| {f'{np.median(pen):g} [{min(pen):g}..{max(pen):g}]' if pen else '-'} "
                f"| {f(float(np.median(r['nonzero'])), '.0f') if 'nonzero' in r else '-'} "
                f"| {str(r['seeds_ahead']) + '/10' if 'seeds_ahead' in r else '-'} |"
            )
    ppo = [k for k in order if k.startswith("ppo")]
    if ppo:
        L += ["", "## PPO seeds", "",
              "| Learner | IC | Seeds: median [min..max] Sharpe | Seeds ahead | Fold models kept at update 0 |",
              "|---|---:|---|---:|---:|"]  # fmt: skip
        for k in ppo:
            for rho in STRENGTHS:
                if rho in res[k]:
                    r = res[k][rho]
                    s = r["seed_sharpes"]
                    L.append(f"| `{k}` | {rho} | {f(float(np.median(s)))} [{f(min(s))}..{f(max(s))}] "
                             f"| {r['seeds_ahead']}/10 | {f(r['zero_share'], '.0%')} |")  # fmt: skip
    (ROOT / "research" / "results" / "rl-4.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
    elif "--smoke" in sys.argv:
        smoke()
    else:
        for n in sys.argv[1:] or [k for k in SPECS if k not in POSTHOC]:
            evaluate(n)
