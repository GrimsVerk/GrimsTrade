# ruff: noqa: E501
"""`ls-ppo` of run rl-4 (card part 2 in research/rl-4.md): a PPO policy on carry-2's perpetual
cross-section. Run only if an RL variant passed part 1's gate. Train period only.

    uv run --with torch python -I research/lib/rl4_perp_rl.py --train [--warm]
    uv run --with torch python -I research/lib/rl4_perp_rl.py --books [--log]

Policy: one linear score per coin from the four ranked inputs (four weights, shared by all coins
and venues). Book: long the top third by score, short the bottom third (carry-2's book). Reward:
the book's weekly return after 10 bps on every change of target weight and after funding, from
the same weekly total returns the forecaster's target uses (a fast simulator: weights do not
drift inside the week). Reported numbers come from `rl4_perp.run_books`, i.e. the same
`short_engine.simulate` replay as every other book. Weights go to
`<cache_root>/derived/rl-4/ppo-theta.json`.
"""

from __future__ import annotations

import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import rl4_perp as P  # noqa: E402
import rl4_sup  # noqa: E402

N_ENV, HORIZON, MAX_UPDATES, EVAL_EVERY = 64, 26, 60, 5
SEEDS = range(10)
REWARD_SCALE = 100.0
PURGE = 14  # days between the last training week and the validation slice


@dataclass
class Weeks:
    """One venue's weeks, padded to a common number of columns."""

    day: np.ndarray  # [W]
    x: np.ndarray  # [W, n, 4]
    m: np.ndarray  # [W, n]
    ret: np.ndarray  # [W, n] the week's total return of a long position, plain (0 outside m)


def pad(rows: P.Rows, n: int) -> Weeks:
    w, k = rows.m.shape
    x = np.zeros((w, n, rows.x.shape[2]))
    m = np.zeros((w, n), bool)
    ret = np.zeros((w, n))
    x[:, :k], m[:, :k] = rows.x, rows.m
    ret[:, :k] = np.where(rows.m, np.expm1(np.nan_to_num(rows.fwd)), 0.0)
    return Weeks(rows.day, x, m, ret)


def split(days: list[np.ndarray], fit_day: int) -> tuple[list[np.ndarray], list[np.ndarray]]:
    """Per venue: (training week indices, validation week indices). The validation slice is the
    last quarter of the usable venue-weeks by date; training stops PURGE days before it."""
    ok = [P.usable(d, fit_day) for d in days]
    pooled = np.sort(np.concatenate([d[o] for d, o in zip(days, ok, strict=True)]))
    cut = pooled[int(len(pooled) * 0.75)]
    tr = [np.flatnonzero(o & (d < cut - PURGE)) for d, o in zip(days, ok, strict=True)]
    va = [np.flatnonzero(o & (d >= cut)) for d, o in zip(days, ok, strict=True)]
    return tr, va


def book(score: np.ndarray, m: np.ndarray) -> np.ndarray:
    return np.array([P.long_short(score[b], m[b]) for b in range(len(score))])


def week_reward(w: np.ndarray, prev: np.ndarray, ret: np.ndarray) -> np.ndarray:
    out: np.ndarray = (w * ret).sum(-1) - P.PERP_COST * np.abs(w - prev).sum(-1)
    return out


def validate(theta: np.ndarray, venues: list[Weeks], va: list[np.ndarray]) -> float:
    """Mean weekly reward of the deterministic policy over the validation venue-weeks."""
    if not np.any(theta):
        return 0.0
    rs = []
    for v, idx in zip(venues, va, strict=True):
        prev = np.zeros(v.m.shape[1])
        for i in idx:
            w = P.long_short(v.x[i] @ theta, v.m[i])
            rs.append(float(week_reward(w, prev, v.ret[i])))
            prev = w
    return float(np.mean(rs)) if rs else 0.0


def train(
    venues: list[Weeks], fit_day: int, seed: int, theta0: np.ndarray
) -> tuple[np.ndarray, dict[str, object]]:
    import torch

    rng = np.random.default_rng([seed, fit_day, 4])
    torch.manual_seed(seed * 10_000 + fit_day)
    tr, va = split([v.day for v in venues], fit_day)
    sizes = np.array([len(t) for t in tr], dtype=float)
    theta = torch.tensor(theta0, dtype=torch.float32, requires_grad=True)
    log_std = torch.tensor(math.log(0.5), requires_grad=True)
    value = torch.zeros((), requires_grad=True)
    opt = torch.optim.Adam([theta, log_std, value], lr=3e-4)
    gamma, lam, clip, epochs, n_mb = 0.99, 0.95, 0.2, 4, 4
    n = venues[0].m.shape[1]
    ven = np.zeros(N_ENV, dtype=np.int64)
    pos = np.zeros(N_ENV, dtype=np.int64)  # index into tr[ven]
    left = np.zeros(N_ENV, dtype=np.int64)
    prev = np.zeros((N_ENV, n))

    def reset(rows: np.ndarray) -> None:
        for e in np.flatnonzero(rows):
            ven[e] = rng.choice(len(venues), p=sizes / sizes.sum())
            pos[e] = rng.integers(0, max(len(tr[ven[e]]) - 1, 1))
            left[e] = min(HORIZON, len(tr[ven[e]]) - pos[e])
            prev[e] = 0.0

    def logp(mu: torch.Tensor, a: torch.Tensor, m: torch.Tensor) -> torch.Tensor:
        lp = -0.5 * ((a - mu) / log_std.exp()) ** 2 - log_std - 0.5 * math.log(2 * math.pi)
        return (lp * m).sum(1)

    reset(np.ones(N_ENV, bool))
    vals = [validate(theta0, venues, va)]
    best, best_u, best_theta = vals[0], 0, theta0.copy()
    for u in range(1, MAX_UPDATES + 1):
        xs, ms, acts, lps, rews, dones = [], [], [], [], [], []
        for _ in range(HORIZON):
            wk = np.array([tr[ven[e]][pos[e]] for e in range(N_ENV)])
            x = np.stack([venues[ven[e]].x[wk[e]] for e in range(N_ENV)])
            m = np.stack([venues[ven[e]].m[wk[e]] for e in range(N_ENV)])
            ret = np.stack([venues[ven[e]].ret[wk[e]] for e in range(N_ENV)])
            xt = torch.as_tensor(x, dtype=torch.float32)
            mt = torch.as_tensor(m, dtype=torch.float32)
            with torch.no_grad():
                mu = xt @ theta
                a = mu + log_std.exp() * torch.randn_like(mu)
                lp = logp(mu, a, mt)
            w = book(a.numpy().astype(np.float64), m)
            r = week_reward(w, prev, ret)
            prev[:] = w
            pos += 1
            left -= 1
            d = left <= 0
            reset(d)
            xs.append(xt)
            ms.append(mt)
            acts.append(a)
            lps.append(lp)
            rews.append(torch.as_tensor(r * REWARD_SCALE, dtype=torch.float32))
            dones.append(torch.as_tensor(d, dtype=torch.float32))
        r_t, d_t = torch.stack(rews), torch.stack(dones)
        with torch.no_grad():
            v = value.expand(N_ENV)
            adv = torch.zeros_like(r_t)
            gae = torch.zeros(N_ENV)
            for t in reversed(range(HORIZON)):
                nonterm = 1 - d_t[t]
                delta = r_t[t] + gamma * v * nonterm - v
                gae = delta + gamma * lam * nonterm * gae
                adv[t] = gae
            ret_t = (adv + v).reshape(-1)
            fadv = adv.reshape(-1)
            fadv = (fadv - fadv.mean()) / (fadv.std() + 1e-8)
        fx, fm, fa, flp = torch.cat(xs), torch.cat(ms), torch.cat(acts), torch.cat(lps)
        for _e in range(epochs):
            for mb in torch.randperm(fa.shape[0]).chunk(n_mb):
                ratio = (logp(fx[mb] @ theta, fa[mb], fm[mb]) - flp[mb]).exp()
                pg = -torch.min(ratio * fadv[mb], ratio.clamp(1 - clip, 1 + clip) * fadv[mb])
                loss = pg.mean() + 0.5 * ((value - ret_t[mb]) ** 2).mean() - 0.001 * log_std
                opt.zero_grad()
                loss.backward()
                torch.nn.utils.clip_grad_norm_([theta, log_std, value], 0.5)
                opt.step()
        if u % EVAL_EVERY == 0:
            th = theta.detach().numpy().astype(np.float64)
            vals.append(validate(th, venues, va))
            if vals[-1] > best:
                best, best_u, best_theta = vals[-1], u, th.copy()
    info: dict[str, object] = {"chosen_update": best_u, "val": [round(x * 52, 4) for x in vals],
                               "train_weeks": [len(t) for t in tr], "val_weeks": [len(x) for x in va]}  # fmt: skip
    return best_theta, info


def path() -> Path:
    import macro

    d = macro.cache_root() / "derived" / "rl-4"
    d.mkdir(parents=True, exist_ok=True)
    return d / "ppo-theta.json"


def train_all(warm: bool) -> None:
    sets = P.load()
    n = max(r.m.shape[1] for _, r in sets.values())
    venues = [pad(r, n) for _, r in sets.values()]
    lasso = P.fold_models(sets, "lasso")
    out: dict[str, object] = {"warm": warm, "folds": {}}
    for f in sorted(lasso):
        theta0 = rl4_sup.C * lasso[f].beta / lasso[f].sd if warm else np.zeros(len(P.INPUTS))
        res = [train(venues, f, s, np.asarray(theta0, dtype=np.float64)) for s in SEEDS]
        out["folds"][str(f)] = {"theta": [t.tolist() for t, _ in res], "info": [i for _, i in res]}  # type: ignore[index]
        print(
            "fold",
            P._date(f),
            "kept updates",
            sorted(i["chosen_update"] for _, i in res),
            flush=True,
        )  # type: ignore[type-var]
        path().write_text(json.dumps(out, indent=1))


def models(seed: int | None) -> dict[int, rl4_sup.Fit]:
    """The trained policies as forecasters for `rl4_perp.run_books`: one seed, or the ensemble
    (the mean of the ten seeds' scores, which for a linear score is the mean of their weights)."""
    j = json.loads(path().read_text())
    k = len(P.INPUTS)
    out = {}
    for f, v in j["folds"].items():
        th = np.array(v["theta"])
        out[int(f)] = rl4_sup.Fit(
            np.zeros(k), np.ones(k), th.mean(0) if seed is None else th[seed], None
        )
    return out


def main() -> None:
    if "--train" in sys.argv:
        train_all("--warm" in sys.argv)
    elif "--books" in sys.argv:
        log = "--log" in sys.argv
        out = P.run_books("ppo", log, "ppo", models(None))
        seeds = {}
        for s in SEEDS:
            o = P.run_books("ppo", log, f"ppo-s{s}", models(s))
            seeds[s] = {"pooled": o["pooled"]["rows"]["ls-ml"]["sharpe"],
                        **{k: v["rows"]["ls-ml"]["sharpe"] for k, v in o["sets"].items()}}  # fmt: skip
        out["seeds"] = seeds
        path().with_name("books-ppo.json").write_text(json.dumps(out, indent=1, default=str))
        print(P.write_books(out, "ppo", "ppo").read_text())


if __name__ == "__main__":
    main()
