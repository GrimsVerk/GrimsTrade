# ruff: noqa: E501
"""Judge the rl-3 planted-signal controls (research/rl-3.md, "Found"). Train period only.

    uv run --with torch python research/lib/rl3_eval.py <config ...>    # logs control rows
    uv run --with torch python research/lib/rl3_eval.py --ceiling       # the known-signal rules
    uv run python research/lib/rl3_eval.py --report                     # results/rl-3.md

As rl2_eval on the six assets (no out-of-universe sets: nothing is planted there). Every
decision list is replayed through `gym.simulate` and logged in tries.md as `control`. Writes
research/data/rl/eval3-<config>.json and ceil3-<rho>.json.
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Callable
from datetime import date
from pathlib import Path

import numpy as np

IDEA = "rl-3-control"
OOS_START = date(2000, 1, 7)
SINCE = date(2003, 1, 1)
SEEDS = range(10)
ERAS = ["2000-09", "2010-16", "2017-21", "2022-25"]
RHOS = ["0.00", "0.02", "0.05", "0.10", "0.20"]
KS: list[float | str] = [0.5, 1.0, 2.0, 4.0, "sign"]
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "data" / "rl"


def _common():  # type: ignore[no-untyped-def]
    import harness
    import rl_eval as r1

    r1.IDEA = IDEA  # log_run writes rl-3-control rows
    hist = harness.load_history("train")
    return r1, hist, r1.baselines(hist, OOS_START)


def evaluate(cfg: str) -> dict:  # noqa: PLR0915
    import common as c
    import rl2_env
    import rl3_plant
    import rl_env
    import stats
    import torch
    from harness import TRAIN_END
    from ml import first_friday
    from rl2_env import RObs, residual
    from rl2_train import FOLDS, G_DIM, base_policy, scores, split
    from rl3_train import MODELS, config, tables
    from rl_env import Obs
    from rl_train import Net, Scaler

    r1, hist, base = _common()
    v, *_ = config(cfg)
    cpu = torch.device("cpu")
    rt = tables(v.rho)["six"]
    t = rt.t
    models: dict[int, list[tuple[Net, Scaler, int]]] = {}
    for y in FOLDS:
        models[y] = []
        for s in SEEDS:
            ck = torch.load(
                MODELS / cfg / f"s{s}" / f"{y}.pt", weights_only=False, map_location=cpu
            )
            net = Net(v.a_dim, G_DIM, ck["hidden"])
            net.load_state_dict(ck["state"])
            net.eval()
            models[y].append((net, Scaler(**ck["scaler"]), int(ck["chosen_update"])))

    def fold_of(d: date) -> int:
        return max(y for y in FOLDS if first_friday(y) <= d)

    def make_policy(rec: dict[int, np.ndarray] | None, fixed: int | None = None
                    ) -> Callable[[Obs, int], np.ndarray]:  # fmt: skip
        def pol(o: Obs, i: int) -> np.ndarray:
            y = fixed if fixed is not None else fold_of(t.fridays[i])
            b = np.repeat(rt.B[i][None], 2, 0)
            live = np.repeat(rt.L[i][None], 2, 0)
            S = np.zeros((2, 10, o.X.shape[1]))
            out = np.zeros_like(o.w)
            for s, (net, sc, _) in enumerate(models[y]):
                idx = [s, 10]
                oo = Obs(o.X[idx], o.elig[idx], o.G[idx], o.w[idx], o.cash[idx])
                S[:, s] = scores(net, sc, RObs(oo, b, live), cpu)
                w = residual(b, live, oo.elig, rt.coin, S[:, s])
                out[s] = w[0]
                out[10] += w[1] / 10
            if rec is not None:
                rec[i] = S
            return out

        return pol

    i0 = t.index(OOS_START)
    rec: dict[int, np.ndarray] = {}
    W, _ = rl_env.run_policy(t, make_policy(rec), i0, len(t.fridays), 11)
    S = np.array([rec[i] for i in range(i0, len(t.fridays))])
    bd = rl2_env.base_daily(hist, t.book.syms, OOS_START, TRAIN_END)
    runs = {}
    for e in range(11):
        sl = S[:, 1] if e == 10 else S[:, 0, [e]]
        key = cfg if e == 10 else f"{cfg}-s{e}"
        runs[key] = r1.log_run(key, "control", rl2_env.res_decisions(rt, i0, sl, bd, TRAIN_END),
                               hist, OOS_START, TRAIN_END)  # fmt: skip
    ts = base["tsmom12"]
    ens = runs[cfg]
    seeds = [runs[f"{cfg}-s{e}"] for e in SEEDS]
    d_ts, p_ts = r1.vs(ens, ts)
    d03, p03 = r1.vs(ens, ts, SINCE)
    e_ens, e_ts = c.era_sharpes(ens), c.era_sharpes(ts)
    ahead = sum(e_ens[k] > e_ts[k] for k in ERAS)
    seed_sh = [stats.sharpe(r.rets) for r in seeds]
    seed_ahead = sum(s > stats.sharpe(ts.rets) for s in seed_sh)
    Bw = rt.B[i0 : i0 + len(W)]
    act = rl2_env.active_share(W[:, 10], Bw)
    # does the tilt follow the planted input? corr(w - b, peek) over eligible cells
    pk = t.X[i0 : i0 + len(W), :, -1]
    el = t.elig[i0 : i0 + len(W)] & rt.L[i0 : i0 + len(W)]
    tilt = W[:, 10] - Bw
    tilt_corr = float(np.corrcoef(tilt[el], pk[el])[0, 1]) if tilt[el].std() > 0 else 0.0
    found = {
        "1 beats tsmom12 p<0.10": d_ts > 0 and p_ts < 0.10,
        "2 ahead in >=3 of 4 eras": ahead >= 3,
        "3 worst loss <= tsmom12 + 5 pts": c.describe(ens)["mdd"] <= c.describe(ts)["mdd"] + 0.05,
        "4 ahead of tsmom12 since 2003": d03 > 0,
        "5 >= 7 of 10 seeds ahead": seed_ahead >= 7,
        "6 active share >= 2%": act >= 0.02,
    }
    gap = []
    for y in FOLDS:
        sp = split(rt, y, True)
        a = t.index(first_friday(y))
        b2 = t.index(first_friday(y + 2)) if y + 2 <= 2025 else len(t.fridays) - 1
        slices = {"out": (a, b2)}
        if sp is not None and sp.val is not None:
            slices = {"train": (sp.lo, sp.hi), "val": sp.val, **slices}
        rec_f: dict[str, object] = {"fold": y, "chosen": [m[2] for m in models[y]]}
        for k, (j, j1) in slices.items():
            Wf, eq = rl_env.run_policy(t, make_policy(None, y), j, j1, 11)
            _, eq_b = rl_env.run_policy(t, base_policy(rt), j, j1, 1)
            rec_f[f"{k}_ens"] = rl2_env.weekly_sharpe(eq[:, 10])
            rec_f[f"{k}_tsmom"] = rl2_env.weekly_sharpe(eq_b[:, 0])
            rec_f[f"{k}_active"] = rl2_env.active_share(Wf[:, 10], rt.B[j:j1])
        gap.append(rec_f)
    chosen = [m[2] for y in FOLDS for m in models[y]]
    out = {
        "config": cfg,
        "rho": v.rho,
        "realised_ic_oos": rl3_plant.realised_ic(t, t.X[:, :, -1], OOS_START),
        "ensemble": r1.describe(ens),
        "vs_tsmom12": {
            "diff": d_ts,
            "p": p_ts,
            "since2003_diff": d03,
            "since2003_p": p03,
            "eras_ahead": ahead,
        },  # fmt: skip
        "seeds": {
            "sharpe": seed_sh,
            "ahead": seed_ahead,
            "active": [rl2_env.active_share(W[:, e], Bw) for e in SEEDS],
        },  # fmt: skip
        "active_share": act,
        "tilt_peek_corr": tilt_corr,
        "chosen_zero_share": float(np.mean([x == 0 for x in chosen])),
        "chosen_median": float(np.median(chosen)),
        "found_bars": found,
        "found": all(found.values()),
        "gap": gap,
    }
    (OUT / f"eval3-{cfg}.json").write_text(json.dumps(out, indent=1, default=r1._json))
    return out


def ceiling() -> None:
    """The known-signal rules: score = k x peek through the same residual action and gym."""
    import rl2_env
    import stats
    from harness import TRAIN_END
    from rl3_train import tables

    r1, hist, base = _common()
    ts = base["tsmom12"]
    for rho in RHOS:
        rt = tables(float(rho))["six"]
        t = rt.t
        i0 = t.index(OOS_START)
        bd = rl2_env.base_daily(hist, t.book.syms, OOS_START, TRAIN_END)
        pk = t.X[i0:, :, -1]
        res = {}
        for k in KS:
            sc = np.sign(pk) * 50.0 if k == "sign" else float(k) * pk
            key = f"ceiling-{rho}-k{k}"
            run = r1.log_run(key, "control",
                             rl2_env.res_decisions(rt, i0, sc[:, None, :], bd, TRAIN_END),
                             hist, OOS_START, TRAIN_END)  # fmt: skip
            w = rl2_env.residual(rt.B[i0:], rt.L[i0:], t.elig[i0:], rt.coin, sc)
            d, p = r1.vs(run, ts)
            res[str(k)] = {**r1.describe(run), "diff": d, "p": p,
                           "since2003_diff": r1.vs(run, ts, SINCE)[0],
                           "active": rl2_env.active_share(w, rt.B[i0:])}  # fmt: skip
            print(rho, k, round(stats.sharpe(run.rets), 3), round(d, 3), flush=True)
        best = max(res, key=lambda x: res[x]["sharpe"])
        (OUT / f"ceil3-{rho}.json").write_text(json.dumps(
            {"rho": float(rho), "rules": res, "best": best, "tsmom12": r1.describe(ts)},
            indent=1, default=r1._json))  # fmt: skip


# --- report (no backtests) ---


def f(x: object, spec: str = ".2f") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "-"
    return format(x, spec)


def report() -> None:
    ev = {p.stem[6:]: json.loads(p.read_text()) for p in sorted(OUT.glob("eval3-*.json"))}
    ce = {p.stem[6:]: json.loads(p.read_text()) for p in sorted(OUT.glob("ceil3-*.json"))}
    ts = next(iter(ce.values()))["tsmom12"] if ce else None
    L = [
        "# RL 3: results of the planted-signal control (train period, out of sample 2000-01-07 to 2025-11-09)",
        "",
        "A control experiment, not a strategy (`research/rl-3.md`). Script `lib/rl3_eval.py`. RL 2's",
        "residual agents (`res-lin`, `res-mlp`) with one planted input `peek` whose correlation with",
        "the coming week's risk-adjusted return is exactly `rho` in every calendar year. Every row is",
        "a replay through `gym.simulate`. Ensemble = mean of the ten seeds' weights. dSharpe and p",
        "against `tsmom12`: paired stationary bootstrap, one-sided. Ceiling = the best known-signal",
        "rule (score = k x peek, no learning), picked in hindsight. Captured = (agent - tsmom12) /",
        "(ceiling - tsmom12) on Sharpe.",
        "",
    ]
    if ts:
        L += [f"`tsmom12` on the same window: Sharpe {f(ts['sharpe'])}, since 2003 {f(ts['since2003'])}, "
              f"worst loss {f(ts['mdd'], '.1%')}.", ""]  # fmt: skip
    L += [
        "## Agents",
        "",
        "| Config | rho | Sharpe | dSharpe vs tsmom12 (p) | Since 2003 d | Eras ahead | Worst loss "
        "| Seeds ahead | Seeds: median [min..max] | Active share | corr(tilt, peek) | Folds kept at update 0 "
        "| Captured | Found (bars passed) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---|---:|---:|---:|---:|---|",
    ]
    for k, e in ev.items():
        d, vt, s = e["ensemble"], e["vs_tsmom12"], e["seeds"]["sharpe"]
        rho = f"{e['rho']:.2f}"
        cap = "-"
        if rho in ce and ts:
            top = ce[rho]["rules"][ce[rho]["best"]]["sharpe"] - ts["sharpe"]
            cap = f"{(d['sharpe'] - ts['sharpe']) / top:.0%}" if top > 0.005 else "-"
        passed = [b.split()[0] for b, ok in e["found_bars"].items() if ok]
        L.append(
            f"| `{k}` | {rho} | {f(d['sharpe'])} | {f(vt['diff'], '+.3f')} ({f(vt['p'])}) "
            f"| {f(vt['since2003_diff'], '+.3f')} | {vt['eras_ahead']}/4 | {f(d['mdd'], '.1%')} "
            f"| {e['seeds']['ahead']}/10 | {f(float(np.median(s)))} [{f(min(s))}..{f(max(s))}] "
            f"| {f(e['active_share'], '.1%')} | {f(e['tilt_peek_corr'], '+.2f')} "
            f"| {f(e['chosen_zero_share'], '.0%')} | {cap} "
            f"| {'**yes**' if e['found'] else 'no'} ({', '.join(passed) or 'none'}) |"
        )
    if ce:
        L += ["", "## Ceiling: known-signal rules (no learning)", "",
              "| rho | k | Sharpe | dSharpe vs tsmom12 (p) | Since 2003 d | Worst loss | Turnover/yr "
              "| Active share | Best |", "|---:|---|---:|---:|---:|---:|---:|---:|---|"]  # fmt: skip
        for rho, cj in ce.items():
            for k, r in cj["rules"].items():
                L.append(f"| {rho} | {k} | {f(r['sharpe'])} | {f(r['diff'], '+.3f')} ({f(r['p'])}) "
                         f"| {f(r['since2003_diff'], '+.3f')} | {f(r['mdd'], '.1%')} "
                         f"| {f(r['turnover'], '.1f')} | {f(r['active'], '.1%')} "
                         f"| {'yes' if k == cj['best'] else ''} |")  # fmt: skip
    for k, e in ev.items():
        L += ["", f"## Gap per fold: `{k}` (weekly Sharpe; ensemble / tsmom12)", "",
              "| Fold | Updates chosen (10 seeds) | Training part | Validation | Out of sample "
              "| Active share out of sample |", "|---:|---|---|---|---|---:|"]  # fmt: skip
        for g in e["gap"]:
            cells = [f"{f(g.get(x + '_ens'))} / {f(g.get(x + '_tsmom'))}" if x + "_ens" in g else "-"
                     for x in ("train", "val", "out")]  # fmt: skip
            L.append(f"| {g['fold']} | {' '.join(str(x) for x in sorted(g['chosen']))} "
                     f"| {cells[0]} | {cells[1]} | {cells[2]} | {f(g['out_active'], '.1%')} |")  # fmt: skip
    (ROOT / "research" / "results" / "rl-3.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
    elif "--ceiling" in sys.argv:
        ceiling()
    else:
        for name in sys.argv[1:]:
            r = evaluate(name)
            print(json.dumps({k: r[k] for k in ("config", "vs_tsmom12", "active_share",
                                                "tilt_peek_corr", "found")}, default=str), flush=True)  # fmt: skip
