"""Train the rl-2 residual agents walk-forward with early stopping (research/rl-2.md).

    uv run --with torch python research/lib/rl2_train.py <variant> <seed> [fold years...]

Per fold: the last 104 usable Fridays of the training window are a purged validation slice;
PPO runs at most MAX_UPDATES updates on the Fridays before it; the deterministic policy is
scored on the validation slice every EVAL_EVERY updates (update 0 = zero tilt = tsmom12) and
the best checkpoint is kept. Saves research/data/rl/models2/<variant>/s<seed>/<Y>.pt
(git-ignored) and a JSON line per fold to log.jsonl.
"""

from __future__ import annotations

import copy
import json
import math
import os
import sys
import time
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path

import numpy as np
import rl2_data
import rl_env
import torch
from rl2_env import TURNOVER_PENALTY, ResEnv, RObs, RTable, residual
from rl_env import Obs
from rl_train import FOLDS, HORIZON, Net, Scaler, fit_scaler, train_end
from torch import nn

MODELS = Path(os.environ.get("RL_MODELS", str(rl2_data.harness.DATA / "rl" / "models2")))
VAL_WEEKS = 104
MAX_UPDATES = int(os.environ.get("RL_UPDATES", "60"))
EVAL_EVERY = 5
MIN_TRAIN_WEEKS = 26
REWARD_SCALE = 100.0
N_PAD = 9  # the widest book (sectors)
A_DIM = len(rl_env.ASSET_FEATS) + 2  # features + current weight + base weight (+3 on-chain)
G_DIM = len(rl_env.MACRO_FEATS) + 1  # macro + cash weight
SMALL = {"six": 48, "gspc": 16}
POOL = {"six": 16, "etf": 12, "sec": 12, "coin": 8, "idx": 8, "gspc": 8}


@dataclass(frozen=True)
class Variant:
    name: str
    hidden: int
    books: dict[str, int]  # book -> parallel episodes per update
    chain: bool = False  # on-chain inputs for coins (tables2c.pkl)

    @property
    def a_dim(self) -> int:
        return A_DIM + (3 if self.chain else 0)


VARIANTS = {
    v.name: v
    for v in [
        Variant("res-lin", 0, SMALL),
        Variant("res-mlp", 32, SMALL),
        Variant("res-pool", 32, POOL),
        Variant("res-mlp-chain", 32, SMALL, chain=True),  # card added after the three above
    ]
}


@dataclass
class Split:
    lo: int  # first Friday with an eligible asset
    hi: int  # training Fridays: lo .. hi-1
    val: tuple[int, int] | None  # validation Fridays v0 .. v1-1


def split(rt: RTable, year: int, validate: bool) -> Split | None:
    t = rt.t
    end = train_end(t, year)
    has = t.elig.any(1)
    if not has[:end].any():
        return None
    lo = int(np.argmax(has))
    if not validate:
        return Split(lo, end, None) if end - lo >= MIN_TRAIN_WEEKS else None
    v0 = end - VAL_WEEKS
    if v0 <= lo:
        return None
    cut = t.fridays[v0] - timedelta(days=14)  # the week's reward ends 7 days before v0
    hi = sum(1 for d in t.fridays if d <= cut)
    return Split(lo, hi, (v0, end)) if hi - lo >= MIN_TRAIN_WEEKS else None


def new_net(hidden: int, a_dim: int = A_DIM) -> Net:
    net = Net(a_dim, G_DIM, hidden)
    last = net.score[-1] if isinstance(net.score, nn.Sequential) else net.score
    assert isinstance(last, nn.Linear)
    nn.init.zeros_(last.weight)
    nn.init.zeros_(last.bias)
    with torch.no_grad():
        net.log_std.fill_(math.log(0.5))
    return net


def to_tensors(ro: RObs, sc: Scaler, dev: torch.device) -> dict[str, torch.Tensor]:
    o = ro.o
    pad = N_PAD - o.X.shape[1]
    el = o.elig & ro.live
    xa = np.concatenate([sc.asset(o.X) * o.elig[..., None], o.w[..., None], ro.b[..., None]], 2)
    xa = np.pad(xa, ((0, 0), (0, pad), (0, 0)))
    el = np.pad(el, ((0, 0), (0, pad)))
    g = np.concatenate([sc.shared(o.G), o.cash[:, None]], axis=1)
    f = torch.float32
    return {
        "xa": torch.as_tensor(xa, dtype=f, device=dev),
        "g": torch.as_tensor(g, dtype=f, device=dev),
        "el": torch.as_tensor(el, device=dev),
    }


def cat(parts: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    return {k: torch.cat([p[k] for p in parts]) for k in parts[0]}


def log_prob(net: Net, mu: torch.Tensor, a: torch.Tensor, el: torch.Tensor) -> torch.Tensor:
    std = net.log_std.exp()
    lp = -0.5 * ((a - mu) / std) ** 2 - net.log_std - 0.5 * math.log(2 * math.pi)
    return (lp * el.float()).sum(1)


def scores(net: Net, sc: Scaler, ro: RObs, dev: torch.device) -> np.ndarray:
    with torch.no_grad():
        mu, _ = net(to_tensors(ro, sc, dev))
    return mu[:, : ro.o.X.shape[1]].cpu().numpy().astype(np.float64)


def policy(net: Net, sc: Scaler, rt: RTable, dev: torch.device):  # type: ignore[no-untyped-def]
    """Deterministic residual policy for `rl_env.run_policy` (weights at Friday i)."""

    def pol(o: Obs, i: int) -> np.ndarray:
        n_env = o.X.shape[0]
        b = np.repeat(rt.B[i][None], n_env, 0)
        live = np.repeat(rt.L[i][None], n_env, 0)
        return residual(b, live, o.elig, rt.coin, scores(net, sc, RObs(o, b, live), dev))

    return pol


def base_policy(rt: RTable):  # type: ignore[no-untyped-def]
    return lambda o, i: np.repeat(rt.B[i][None], o.X.shape[0], 0)


def active_score(rt: RTable, w: np.ndarray, eq: np.ndarray, eq_b: np.ndarray, i0: int) -> float:
    """Mean weekly reward of a deterministic run: active log growth minus the turnover penalty."""
    act = w[:, 0] - rt.B[i0 : i0 + len(w)]
    turn = np.abs(np.diff(np.concatenate([np.zeros_like(act[:1]), act]), axis=0)).sum(1)
    g = np.diff(np.log(eq[:, 0])) - np.diff(np.log(eq_b[:, 0]))
    return float((g - TURNOVER_PENALTY * turn).mean())


def train_fold(
    v: Variant, tabs: dict[str, RTable], year: int, seed: int, dev: torch.device
) -> tuple[Net, Scaler, dict[str, object]]:
    rng = np.random.default_rng([seed, year, 2])
    torch.manual_seed(seed * 10_000 + year + 7)
    sp = {k: split(tabs[k], year, k != "gspc") for k in v.books}
    used = {k: s for k, s in sp.items() if s is not None}
    sc = fit_scaler([(tabs[k].t, s.hi) for k, s in used.items()], macro=True)
    envs = [(k, ResEnv(tabs[k], v.books[k], rng, s.lo, s.hi, HORIZON)) for k, s in used.items()]
    vals = {k: s.val for k, s in used.items() if s.val is not None}
    base_eq = {
        k: rl_env.run_policy(tabs[k].t, base_policy(tabs[k]), a, b)[1] for k, (a, b) in vals.items()
    }
    net = new_net(v.hidden, v.a_dim).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=3e-4)
    gamma, lam, clip, epochs, n_mb = 0.99, 0.95, 0.2, 4, 4

    def validate() -> float:
        out = []
        for k, (a, b) in vals.items():
            w, eq = rl_env.run_policy(tabs[k].t, policy(net, sc, tabs[k], dev), a, b)
            out.append(active_score(tabs[k], w, eq, base_eq[k], a))
        return float(np.mean(out))

    val_scores = [validate()]
    best, best_u, best_state = val_scores[0], 0, copy.deepcopy(net.state_dict())
    for u in range(1, MAX_UPDATES + 1):
        buf: dict[str, list[torch.Tensor]] = {k: [] for k in ("a", "lp", "v", "r", "d")}
        obs_l: list[dict[str, torch.Tensor]] = []
        for _t in range(HORIZON):
            ros = [e.obs() for _, e in envs]
            o = cat([to_tensors(ro, sc, dev) for ro in ros])
            with torch.no_grad():
                mu, val = net(o)
                mu = mu[:, :-1]  # no cash score: cash is what the weights leave
                a = mu + net.log_std.exp() * torch.randn_like(mu)
                lp = log_prob(net, mu, a, o["el"])
            a_np = a.cpu().numpy().astype(np.float64)
            rs, ds, i = [], [], 0
            for (_, e), ro in zip(envs, ros, strict=True):
                r, d = e.step(a_np[i : i + e.n, : ro.o.X.shape[1]])
                rs.append(r)
                ds.append(d)
                i += e.n
            obs_l.append(o)
            buf["a"].append(a)
            buf["lp"].append(lp)
            buf["v"].append(val)
            buf["r"].append(torch.as_tensor(np.concatenate(rs) * REWARD_SCALE, device=dev))
            buf["d"].append(torch.as_tensor(np.concatenate(ds), device=dev))
        with torch.no_grad():
            _, v_last = net(cat([to_tensors(e.obs(), sc, dev) for _, e in envs]))
        r_t = torch.stack(buf["r"]).float()
        d_t = torch.stack(buf["d"]).float()
        v_t = torch.stack(buf["v"])
        adv = torch.zeros_like(r_t)
        gae = torch.zeros_like(v_last)
        for t in reversed(range(HORIZON)):
            nxt = v_last if t == HORIZON - 1 else v_t[t + 1]
            nonterm = 1 - d_t[t]
            delta = r_t[t] + gamma * nxt * nonterm - v_t[t]
            gae = delta + gamma * lam * nonterm * gae
            adv[t] = gae
        ret = adv + v_t
        flat = cat(obs_l)
        fa, flp = torch.cat(buf["a"]), torch.cat(buf["lp"])
        fadv, fret = adv.reshape(-1), ret.reshape(-1)
        fadv = (fadv - fadv.mean()) / (fadv.std() + 1e-8)
        for _e in range(epochs):
            for mb in torch.randperm(fa.shape[0], device=dev).chunk(n_mb):
                o = {k: x[mb] for k, x in flat.items()}
                mu, val = net(o)
                mu = mu[:, :-1]
                ratio = (log_prob(net, mu, fa[mb], o["el"]) - flp[mb]).exp()
                pg = -torch.min(ratio * fadv[mb], ratio.clamp(1 - clip, 1 + clip) * fadv[mb])
                loss = pg.mean() + 0.5 * ((val - fret[mb]) ** 2).mean() - 0.001 * net.log_std
                opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(net.parameters(), 0.5)
                opt.step()
        if u % EVAL_EVERY == 0:
            val_scores.append(validate())
            if val_scores[-1] > best:
                best, best_u, best_state = val_scores[-1], u, copy.deepcopy(net.state_dict())
    net.load_state_dict(best_state)
    info: dict[str, object] = {
        "chosen_update": best_u,
        "val_scores": [round(x * 52, 5) for x in val_scores],  # per year
        "books": {k: [s.lo, s.hi, s.val] for k, s in used.items()},
        "std": float(net.log_std.exp().detach()),
    }
    return net, sc, info


def main() -> None:
    torch.set_num_threads(1)
    v = VARIANTS[sys.argv[1]]
    seed = int(sys.argv[2])
    years = [int(y) for y in sys.argv[3:]] or FOLDS
    dev = torch.device(os.environ.get("RL_DEVICE", "cpu"))  # timing test: CPU is fast enough
    tabs = rl2_data.load(v.chain)
    out = MODELS / v.name / f"s{seed}"
    out.mkdir(parents=True, exist_ok=True)
    for y in years:
        if (out / f"{y}.pt").exists():
            continue
        t0 = time.time()
        net, sc, info = train_fold(v, tabs, y, seed, dev)
        torch.save({"state": net.state_dict(), "scaler": sc.__dict__, "hidden": v.hidden,
                    **info}, out / f"{y}.pt")  # fmt: skip
        rec = {"variant": v.name, "seed": seed, "fold": y, "seconds": round(time.time() - t0, 1),
               "device": str(dev), "max_updates": MAX_UPDATES, **info}  # fmt: skip
        with (out / "log.jsonl").open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
