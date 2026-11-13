# ruff: noqa: E501
"""Judge the rl-2 residual agents (research/rl-2.md, "Pass bar"). Train period only.

    uv run --with torch python research/lib/rl2_eval.py [variant ...]   # logs tries: run once
    uv run python research/lib/rl2_eval.py --report                   # results/rl-2.md

For each variant: ten seeds and their ensemble decide every Friday from 2000-01-07 with the fold
model in force; each day's weights are the residual on that day's `tsmom12` decision; every
decision list is replayed through `gym.simulate` and logged in tries.md (ensemble `variant`,
seeds and out-of-universe `robustness`). Also the training / validation / out-of-sample gap per
fold, the updates early stopping chose, and the active share. Writes
research/data/rl/eval2-<variant>.json.
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Callable, Mapping
from datetime import date

import numpy as np

IDEA = "rl-2"
OOS_START = date(2000, 1, 7)
SINCE = date(2003, 1, 1)
SEEDS = range(10)
VARIANTS = ["res-lin", "res-mlp", "res-pool", "res-mlp-chain"]
ERAS = ["2000-09", "2010-16", "2017-21", "2022-25"]


def evaluate(variant: str) -> dict:  # noqa: PLR0915
    import common as c
    import harness
    import rl2_data
    import rl2_env
    import rl_env
    import rl_eval as r1
    import stats
    import torch
    from harness import TRAIN_END
    from ml import first_friday
    from rl2_env import RObs, RTable, residual
    from rl2_train import FOLDS, G_DIM, MODELS, base_policy, scores, split
    from rl2_train import VARIANTS as V2
    from rl_env import Obs
    from rl_train import Net, Scaler

    r1.IDEA = IDEA  # log_run writes rl-2 rows
    cpu = torch.device("cpu")
    tabs = rl2_data.load(V2[variant].chain)
    hists = rl2_data.histories()
    models: dict[int, list[tuple[Net, Scaler, int]]] = {}
    for y in FOLDS:
        models[y] = []
        for s in SEEDS:
            ck = torch.load(MODELS / variant / f"s{s}" / f"{y}.pt", weights_only=False,
                            map_location=cpu)  # fmt: skip
            net = Net(V2[variant].a_dim, G_DIM, ck["hidden"])
            net.load_state_dict(ck["state"])
            net.eval()
            models[y].append((net, Scaler(**ck["scaler"]), int(ck["chosen_update"])))

    def fold_of(d: date) -> int:
        return max(y for y in FOLDS if first_friday(y) <= d)

    def make_policy(rt: RTable, rec: dict[int, np.ndarray] | None, fixed: int | None = None
                    ) -> Callable[[Obs, int], np.ndarray]:  # fmt: skip
        """Rows 0-9: seed s on its own account; row 10: the ensemble account (mean of the
        seeds' residual weights, each seed reading the ensemble account). rec[i] = scores
        [2, 10, n]: own account, ensemble account."""

        def pol(o: Obs, i: int) -> np.ndarray:
            y = fixed if fixed is not None else fold_of(rt.t.fridays[i])
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

    def run_book(name: str, start: date, log_seeds: bool) -> tuple[dict, np.ndarray, int]:
        rt = tabs[name]
        t = rt.t
        hist = harness.load_history("train", True, t.book.syms)
        j0 = max(t.index(start), int(np.argmax(t.elig.any(1))))
        rec: dict[int, np.ndarray] = {}
        W, _ = rl_env.run_policy(t, make_policy(rt, rec), j0, len(t.fridays), 11)
        S = np.array([rec[i] for i in range(j0, len(t.fridays))])  # [weeks, 2, 10, n]
        bd = rl2_env.base_daily(hist, t.book.syms, t.fridays[j0], TRAIN_END)
        tag = variant if name == "six" else f"{variant}@{name}"
        runs = {}
        for e in range(11) if log_seeds else [10]:
            if e == 10:
                decs = rl2_env.res_decisions(rt, j0, S[:, 1], bd, TRAIN_END)
                key = tag
            else:
                decs = rl2_env.res_decisions(rt, j0, S[:, 0, [e]], bd, TRAIN_END)
                key = f"{tag}-s{e}"
            kind = "variant" if (e == 10 and name == "six") else "robustness"
            runs[key] = r1.log_run(key, kind, decs, hist, t.fridays[j0], TRAIN_END)
        return runs, W, j0

    rt = tabs["six"]
    t = rt.t
    hist = hists["six"]
    runs, W, i0 = run_book("six", OOS_START, True)
    base = r1.baselines(hist, OOS_START)
    ts = base["tsmom12"]
    ens = runs[variant]
    seeds = [runs[f"{variant}-s{e}"] for e in SEEDS]
    d_ts, p_ts = r1.vs(ens, ts)
    d03, p03 = r1.vs(ens, ts, SINCE)
    e_ens, e_ts = c.era_sharpes(ens), c.era_sharpes(ts)
    ahead = sum(e_ens[k] > e_ts[k] for k in ERAS)
    seed_sh = [stats.sharpe(r.rets) for r in seeds]
    seed_ahead = sum(s > stats.sharpe(ts.rets) for s in seed_sh)
    Bw = rt.B[i0 : i0 + len(W)]
    act = rl2_env.active_share(W[:, 10], Bw)
    act_seeds = [rl2_env.active_share(W[:, e], Bw) for e in SEEDS]
    oou = {}
    for name in ("etf", "coin", "idx"):
        r_o, _, j0 = run_book(name, OOS_START, False)
        r = r_o[f"{variant}@{name}"]
        start = tabs[name].t.fridays[j0]
        h = harness.load_history("train", True, tabs[name].t.book.syms)
        b = harness.run(IDEA, "tsmom12", c.weekly(c.slots(c.tsmom_signal)), kind="baseline",
                        history=h, start=start, log=False)  # fmt: skip
        oou[name] = {"from": str(start), "sharpe": stats.sharpe(r.rets),
                     "tsmom12": stats.sharpe(b.rets), "diff": r1.vs(r, b)[0]}  # fmt: skip
    same_sign = sum(np.sign(o["diff"]) == np.sign(d_ts) for o in oou.values())
    bars = {
        "1 beats tsmom12 p<0.10": d_ts > 0 and p_ts < 0.10,
        "2 ahead in >=3 of 4 eras": ahead >= 3,
        "3 worst loss <= tsmom12 + 5 pts": c.describe(ens)["mdd"] <= c.describe(ts)["mdd"] + 0.05,
        "4 ahead of tsmom12 since 2003, ahead of sma200/inverse-vol/equal weight": d03 > 0
        and all(
            stats.sharpe(ens.rets) > stats.sharpe(base[k].rets)
            and r1.sharpe_between(ens, SINCE) > r1.sharpe_between(base[k], SINCE)
            for k in ("sma200", "inverse-vol", "equal-weight")
        ),
        "5 >= 7 of 10 seeds ahead of tsmom12": seed_ahead >= 7,
        "6 out-of-universe sign in >= 2 of 3": same_sign >= 2,
        "7 active share >= 2%": act >= 0.02,
    }
    # the gap: each fold model on its training part, validation slice, two traded years
    gap = []
    for y in FOLDS:
        sp = split(rt, y, True)
        a = t.index(first_friday(y))
        b2 = t.index(first_friday(y + 2)) if y + 2 <= 2025 else len(t.fridays) - 1
        slices = {"out": (a, b2)}
        if sp is not None and sp.val is not None:
            slices = {"train": (sp.lo, sp.hi), "val": sp.val, **slices}
        rec_f: dict[str, object] = {"fold": y,
                                    "chosen": [m[2] for m in models[y]]}  # fmt: skip
        for k, (j, j1) in slices.items():
            Wf, eq = rl_env.run_policy(t, make_policy(rt, None, y), j, j1, 11)
            _, eq_b = rl_env.run_policy(t, base_policy(rt), j, j1, 1)
            rec_f[f"{k}_ens"] = rl2_env.weekly_sharpe(eq[:, 10])
            rec_f[f"{k}_tsmom"] = rl2_env.weekly_sharpe(eq_b[:, 0])
            rec_f[f"{k}_active"] = rl2_env.active_share(Wf[:, 10], rt.B[j:j1])
        gap.append(rec_f)
    out = {
        "variant": variant,
        "ensemble": r1.describe(ens),
        "baselines": {k: r1.describe(v) for k, v in base.items()},
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
            "active": act_seeds,
            "since2003": [r1.sharpe_between(r, SINCE) for r in seeds],
            "mdd": [c.describe(r)["mdd"] for r in seeds],
        },  # fmt: skip
        "active_share": act,
        "oou": oou,
        "bars": bars,
        "passed": all(bars.values()),
        "behaviour": r1.behaviour(t, i0, W[:, 10]),
        "behaviour_tsmom12": r1.behaviour(t, i0, Bw),
        "gap": gap,
    }
    path = harness.DATA / "rl" / f"eval2-{variant}{'.dry' if r1.DRY else ''}.json"
    path.write_text(json.dumps(out, indent=1, default=r1._json))
    return out


# --- report (no backtests) ---


def f(x: object, spec: str = ".2f") -> str:
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "-"
    return format(x, spec)


def report() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    data = root / "research" / "data" / "rl"
    ev: Mapping[str, dict] = {
        v: json.loads((data / f"eval2-{v}.json").read_text())
        for v in VARIANTS
        if (data / f"eval2-{v}.json").exists()
    }
    first = next(iter(ev.values()))
    L = [
        "# RL 2: results (train period, out of sample 2000-01-07 to 2025-11-09)",
        "",
        "Script `lib/rl2_eval.py`. Residual agents: `tsmom12` plus a tilt of at most half a slot,",
        "walk-forward (retrained every two years), early stopping on a purged validation slice.",
        "Every row is a replay through `gym.simulate`. Ensemble = mean of the ten seeds' weights.",
        "dSharpe and p against `tsmom12`: paired stationary bootstrap, one-sided. Active share =",
        "half the sum of |w - tsmom12 weight|, averaged over Fridays.",
        "",
        "## Six assets",
        "",
        "| Strategy | Sharpe | Since 2003 | dSharpe vs tsmom12 (p) | Since 2003 d (p) | Worst loss "
        "| Growth/yr | Turnover/yr | Active share | Seeds: median Sharpe [min..max] | Seeds ahead "
        "| Bars passed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---:|---|",
    ]
    for k, b in first["baselines"].items():
        L.append(f"| `{k}` | {f(b['sharpe'])} | {f(b['since2003'])} | | | {f(b['mdd'], '.1%')} "
                 f"| {f(b['cagr'], '+.1%')} | {f(b['turnover'], '.1f')} | | | | |")  # fmt: skip
    for v, e in ev.items():
        d, s, vt = e["ensemble"], e["seeds"]["sharpe"], e["vs_tsmom12"]
        passed = [k.split()[0] for k, ok in e["bars"].items() if ok]
        L.append(
            f"| `{v}` | {f(d['sharpe'])} | {f(d['since2003'])} | {f(vt['diff'], '+.3f')} "
            f"({f(vt['p'])}) | {f(vt['since2003_diff'], '+.3f')} ({f(vt['since2003_p'])}) "
            f"| {f(d['mdd'], '.1%')} | {f(d['cagr'], '+.1%')} | {f(d['turnover'], '.1f')} "
            f"| {f(e['active_share'], '.1%')} | {f(float(np.median(s)))} [{f(min(s))}..{f(max(s))}] "
            f"| {e['seeds']['ahead']}/10 | {', '.join(passed) or 'none'} |"
        )
    L += ["", "## Eras (Sharpe)", "", "| Strategy | " + " | ".join(ERAS) + " |",
          "|---|" + "---:|" * len(ERAS)]  # fmt: skip
    for k, b in first["baselines"].items():
        L.append(f"| `{k}` | " + " | ".join(f(b.get(x)) for x in ERAS) + " |")
    for v, e in ev.items():
        L.append(f"| `{v}` | " + " | ".join(f(e["ensemble"].get(x)) for x in ERAS) + " |")
    L += ["", "## Out of universe (fold models unchanged; ensemble)", "",
          "| Variant | Set | From | Sharpe | tsmom12 | Difference |", "|---|---|---|---:|---:|---:|"]  # fmt: skip
    for v, e in ev.items():
        for k, o in e["oou"].items():
            L.append(f"| `{v}` | {k} | {o['from']} | {f(o['sharpe'])} | {f(o['tsmom12'])} "
                     f"| {f(o['diff'], '+.2f')} |")  # fmt: skip
    L += ["", "## What the ensemble does (six assets, 2000-2025)", "",
          "| Strategy | Cash | Coins | Weight in an uptrend (slots) | Weight in a downtrend (slots) "
          "| Weekly change |", "|---|---:|---:|---:|---:|---:|"]  # fmt: skip
    rows = [("tsmom12", first["behaviour_tsmom12"])] + [(v, e["behaviour"]) for v, e in ev.items()]
    for v, bh in rows:
        L.append(f"| `{v}` | {f(bh['cash'], '.0%')} | {f(bh['coins'], '.0%')} "
                 f"| {f(bh['slot_up'])} | {f(bh['slot_down'])} | {f(bh['weekly_change'], '.1%')} |")  # fmt: skip
    for v, e in ev.items():
        L += ["", f"## Gap per fold: `{v}` (weekly Sharpe; ensemble / tsmom12; active share)", "",
              "| Fold | Updates chosen (10 seeds) | Training part | Validation | Out of sample "
              "| Active share out of sample |", "|---:|---|---|---|---|---:|"]  # fmt: skip
        for g in e["gap"]:
            cells = []
            for k in ("train", "val", "out"):
                cells.append(f"{f(g.get(k + '_ens'))} / {f(g.get(k + '_tsmom'))}"
                             if k + "_ens" in g else "-")  # fmt: skip
            ch = sorted(g["chosen"])
            L.append(f"| {g['fold']} | {' '.join(str(x) for x in ch)} | {cells[0]} | {cells[1]} "
                     f"| {cells[2]} | {f(g['out_active'], '.1%')} |")  # fmt: skip
    (root / "research" / "results" / "rl-2.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    if "--report" in sys.argv:
        report()
    else:
        for v in sys.argv[1:] or VARIANTS:
            res = evaluate(v)
            print(json.dumps({k: res[k] for k in ("variant", "vs_tsmom12", "active_share",
                                                  "passed", "bars")}, default=str), flush=True)  # fmt: skip
