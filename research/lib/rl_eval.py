"""Judge the rl-1 agents (research/rl-1.md, "Pass bar"). Train period only.

    uv run --with torch python research/lib/rl_eval.py [variant ...]

For each variant: the ten seeds and their ensemble decide every Friday from 2000-01-07 with the
fold model in force (walk-forward); every decision list is replayed through `gym.simulate` and
logged in tries.md (ensemble `variant`, seeds and out-of-universe `robustness`). Baselines are
re-scored from the same first day with their logged configuration (not logged again). Also: the
in-sample against out-of-sample Sharpe of every fold model (the overfitting gap) and what the
ensemble does. Writes research/results/rl-1-<variant>.md and research/data/rl/eval-<variant>.json.
"""

from __future__ import annotations

import csv
import json
import math
import os
import sys
from collections.abc import Callable, Mapping, Sequence
from datetime import date

import common as c
import harness
import numpy as np
import rl_data
import rl_env
import stats
import torch
from harness import TRAIN_END, Run
from ml import first_friday
from rl_env import Obs, Table
from rl_train import FOLDS, MODELS, VARIANTS, Net, Scaler, to_tensors, to_weights, train_end

from grimstrade import gym, report
from grimstrade.data import Bar

IDEA = "rl-1"
OOS_START = date(2000, 1, 7)
SINCE = date(2003, 1, 1)
SEEDS = range(10)
OOU = {"etf": harness.OOU_ETFS, "coin": harness.OOU_COINS, "idx": harness.OOU_INDEXES}
UP12 = rl_env.ASSET_FEATS.index("up_12m")
CPU = torch.device("cpu")
DRY = os.environ.get("RL_DRY") == "1"  # plumbing check: log nothing, write *.dry files


def load_models(variant: str) -> dict[int, list[tuple[Net, Scaler]]]:
    out: dict[int, list[tuple[Net, Scaler]]] = {}
    for y in FOLDS:
        out[y] = []
        for s in SEEDS:
            ck = torch.load(
                MODELS / variant / f"s{s}" / f"{y}.pt", weights_only=False, map_location=CPU
            )
            net = Net(len(rl_env.ASSET_FEATS) + 1, len(rl_env.MACRO_FEATS) + 1, ck["hidden"])
            net.load_state_dict(ck["state"])
            net.eval()
            out[y].append((net, Scaler(**ck["scaler"])))
    return out


def fold_of(d: date) -> int:
    return max(y for y in FOLDS if first_friday(y) <= d)


def det(net: Net, sc: Scaler, o: Obs) -> np.ndarray:
    with torch.no_grad():
        t = to_tensors(o, sc, CPU)
        mu, _ = net(t)
        return to_weights(mu, t["el"]).numpy().astype(np.float64)[:, : o.X.shape[1]]


def rows(o: Obs, idx: list[int]) -> Obs:
    return Obs(o.X[idx], o.elig[idx], o.G[idx], o.w[idx], o.cash[idx])


def clean(w: np.ndarray) -> np.ndarray:
    return np.where(w > 1e-6, w, 0.0)


def seeds_and_ensemble(
    models: Mapping[int, list[tuple[Net, Scaler]]], table: Table, fixed_fold: int | None = None
) -> Callable[[Obs, int], np.ndarray]:
    """Rows 0-9: seed s on its own account; row 10: the ensemble account (mean of the seeds'
    weights, each seed reading the ensemble account's state)."""

    def policy(o: Obs, i: int) -> np.ndarray:
        y = fixed_fold if fixed_fold is not None else fold_of(table.fridays[i])
        out = np.zeros_like(o.w)
        ens = np.zeros(o.w.shape[1])
        for s, (net, sc) in enumerate(models[y]):
            w = det(net, sc, rows(o, [s, 10]))
            out[s] = w[0]
            ens += w[1] / len(models[y])
        out[10] = ens
        return clean(out)

    return policy


def tsmom_policy(o: Obs, i: int) -> np.ndarray:
    n = o.elig.sum(1, keepdims=True).clip(min=1)
    return np.where(o.elig & (o.X[:, :, UP12] > 0.5), 1.0 / n, 0.0)


def log_run(
    variant: str, kind: str, decs: list[gym.Decision], hist: Mapping[str, Sequence[Bar]],
    start: date, end: date,
) -> Run:  # fmt: skip
    """`harness.run` after the decisions: the real gym, the score, the tries.md row."""
    res = gym.simulate(decs, hist)
    days, eq = harness._calendar(res.equity)
    run = Run(
        IDEA, variant, "train", report.score(f"{IDEA}/{variant}", res), days, eq,
        float(np.mean([sum(d.weights.values()) for d in decs])), decs,
    )  # fmt: skip
    if DRY:
        return run
    harness._log(run, kind, start, end)
    path = harness.DATA / "runs" / IDEA / f"{variant}.train.csv"
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["date", "equity"])
        w.writerows((d.isoformat(), repr(float(e))) for d, e in zip(days, eq, strict=True))
    return run


def baselines(hist: Mapping[str, Sequence[Bar]], start: date) -> dict[str, Run]:
    pan = harness.Panel(hist)
    twins = {
        "tsmom12": c.weekly(c.slots(c.tsmom_signal)),
        "sma200": c.weekly(c.slots(c.sma_signal)),
        "inverse-vol": c.weekly(c.inverse_vol),
        "equal-weight": c.weekly(c.equal_weight),
    }
    return {
        n: harness.run(
            IDEA, n, f, kind="baseline", panel=pan, history=hist, start=start, log=False
        )  # fmt: skip
        for n, f in twins.items()
    }


def sharpe_between(run: Run, a: date, b: date = TRAIN_END) -> float:
    return stats.sharpe(run.rets_between(a, b))


def vs(a: Run, b: Run, since: date | None = None) -> tuple[float, float]:
    lo = max(a.days[0], b.days[0], since or a.days[0])
    hi = min(a.days[-1], b.days[-1])
    d, p, _, _ = stats.sharpe_diff_boot(a.rets_between(lo, hi), b.rets_between(lo, hi))
    return d, p


def weekly_sharpe(eq: np.ndarray) -> float:
    r = np.diff(np.log(eq))
    return float(r.mean() / r.std() * math.sqrt(52)) if len(r) > 2 and r.std() > 0 else math.nan


def overfit_table(models: Mapping[int, list[tuple[Net, Scaler]]], t: Table) -> list[dict]:
    """Each fold model on its own training window and on the two years it traded (fresh
    accounts, weekly marks from the batched simulator): ensemble, median seed, tsmom12."""
    out = []
    for y in FOLDS:
        pol = seeds_and_ensemble(models, t, fixed_fold=y)
        a = t.index(first_friday(y))
        b = t.index(first_friday(y + 2)) if y + 2 <= 2025 else len(t.fridays) - 1
        rec: dict[str, float] = {"fold": y}
        for name, (i0, i1) in {"in": (0, train_end(t, y)), "out": (a, b)}.items():
            _, eq = rl_env.run_policy(t, pol, i0, i1, 11)
            _, eq_t = rl_env.run_policy(t, tsmom_policy, i0, i1, 1)
            sh = [weekly_sharpe(eq[:, e]) for e in range(11)]
            rec[f"{name}_ens"] = sh[10]
            rec[f"{name}_med"] = float(np.median(sh[:10]))
            rec[f"{name}_tsmom"] = weekly_sharpe(eq_t[:, 0])
        out.append(rec)
    return out


def behaviour(t: Table, i0: int, w: np.ndarray) -> dict[str, float]:
    """What the ensemble does: cash, coins, and how its holdings follow the trend flag."""
    el = t.elig[i0 : i0 + len(w)]
    up = t.X[i0 : i0 + len(w), :, UP12] > 0.5
    coin = np.array([rl_env.UNIVERSE[s] == rl_env.CRYPTO for s in t.book.syms])
    risk = w.sum(1)
    n = el.sum(1)
    slot = np.where(el, w * n[:, None], np.nan)  # weight as a multiple of an equal slot
    vix = t.G[i0 : i0 + len(w), rl_env.MACRO_FEATS.index("vix")]
    ok = ~np.isnan(vix)
    return {
        "cash": float(1 - risk.mean()),
        "coins": float(w[:, coin].sum(1).mean()),
        "slot_up": float(np.nanmean(np.where(up, slot, np.nan))),
        "slot_down": float(np.nanmean(np.where(el & ~up, slot, np.nan))),
        "corr_risk_vix": float(np.corrcoef(risk[ok], vix[ok])[0, 1]),
        "weekly_change": float(np.abs(np.diff(w, axis=0)).sum(1).mean() / 2),
    }


def describe(run: Run) -> dict[str, float]:
    d = c.describe(run)
    return {**d, "since2003": sharpe_between(run, SINCE), **c.era_sharpes(run)}


def _json(x: object) -> object:
    return x.item() if hasattr(x, "item") else str(x)


def evaluate(variant: str) -> dict:
    tabs = rl_data.load()
    t = tabs["six"]
    hist = harness.load_history("train")
    models = load_models(variant)
    i0 = t.index(OOS_START)
    W, _ = rl_env.run_policy(t, seeds_and_ensemble(models, t), i0, len(t.fridays), 11)
    base = baselines(hist, OOS_START)
    ts = base["tsmom12"]
    runs = {}
    for e in range(11):
        name = variant if e == 10 else f"{variant}-s{e}"
        decs = rl_env.daily_decisions(t, i0, W[:, e], TRAIN_END)
        runs[name] = log_run(name, "variant" if e == 10 else "robustness", decs, hist,
                             OOS_START, TRAIN_END)  # fmt: skip
    ens = runs[variant]
    seeds = [runs[f"{variant}-s{e}"] for e in range(10)]
    d_ts, p_ts = vs(ens, ts)
    d03, p03 = vs(ens, ts, SINCE)
    eras = ["2000-09", "2010-16", "2017-21", "2022-25"]
    e_ens, e_ts = c.era_sharpes(ens), c.era_sharpes(ts)
    ahead = sum(e_ens[k] > e_ts[k] for k in eras)
    seed_sh = [stats.sharpe(r.rets) for r in seeds]
    seed_ahead = sum(s > stats.sharpe(ts.rets) for s in seed_sh)
    # out of universe: the fold models unchanged, ensemble only
    oou = {}
    for name, syms in OOU.items():
        tt = tabs[name]
        h = harness.load_history("train", True, syms)
        j0 = max(tt.index(OOS_START), int(np.argmax(tt.elig.any(1))))
        Wo, _ = rl_env.run_policy(tt, seeds_and_ensemble(models, tt), j0, len(tt.fridays), 11)
        start = tt.fridays[j0]
        r = log_run(
            f"{variant}@{name}",
            "robustness",
            rl_env.daily_decisions(tt, j0, Wo[:, 10], TRAIN_END),
            h,
            start,
            TRAIN_END,
        )
        b = harness.run(IDEA, "tsmom12", c.weekly(c.slots(c.tsmom_signal)), kind="baseline",
                        history=h, start=start, log=False)  # fmt: skip
        oou[name] = {"from": str(start), "sharpe": stats.sharpe(r.rets),
                     "tsmom12": stats.sharpe(b.rets), "diff": vs(r, b)[0]}  # fmt: skip
    same_sign = sum(np.sign(o["diff"]) == np.sign(d_ts) for o in oou.values())
    bars = {
        "1 beats tsmom12 p<0.10": d_ts > 0 and p_ts < 0.10,
        "2 ahead in >=3 of 4 eras": ahead >= 3,
        "3 worst loss <= tsmom12 + 5 pts": c.describe(ens)["mdd"] <= c.describe(ts)["mdd"] + 0.05,
        "4 not behind tsmom12 since 2003, ahead of sma200/inverse-vol/equal weight": d03 >= 0
        and all(
            stats.sharpe(ens.rets) > stats.sharpe(base[k].rets)
            and sharpe_between(ens, SINCE) > sharpe_between(base[k], SINCE)
            for k in ("sma200", "inverse-vol", "equal-weight")
        ),
        "5 >= 7 of 10 seeds ahead of tsmom12": seed_ahead >= 7,
        "6 out-of-universe sign in >= 2 of 3": same_sign >= 2,
    }
    out = {
        "variant": variant,
        "ensemble": describe(ens),
        "baselines": {k: describe(v) for k, v in base.items()},
        "vs_tsmom12": {"diff": d_ts, "p": p_ts, "since2003_diff": d03, "since2003_p": p03,
                       "eras_ahead": ahead},  # fmt: skip
        "seeds": {"sharpe": seed_sh, "ahead": seed_ahead,
                  "since2003": [sharpe_between(r, SINCE) for r in seeds],
                  "mdd": [c.describe(r)["mdd"] for r in seeds]},  # fmt: skip
        "oou": oou,
        "bars": bars,
        "passed": all(bars.values()),
        "behaviour": behaviour(t, i0, W[:, 10]),
        "behaviour_tsmom12": behaviour(t, i0, np.array(
            [tsmom_policy(Obs(t.X[i][None], t.elig[i][None], t.G[i][None],
                              np.zeros((1, 6)), np.ones(1)), i)[0]
             for i in range(i0, len(t.fridays))])),
        "overfit": overfit_table(models, t),
    }  # fmt: skip
    (harness.DATA / "rl").mkdir(parents=True, exist_ok=True)
    (harness.DATA / "rl" / f"eval-{variant}{'.dry' if DRY else ''}.json").write_text(
        json.dumps(out, indent=1, default=_json)
    )
    return out


if __name__ == "__main__":
    for v in sys.argv[1:] or list(VARIANTS):
        res = evaluate(v)
        print(json.dumps({k: res[k] for k in ("variant", "vs_tsmom12", "passed", "bars")},
                         default=_json), flush=True)  # fmt: skip
