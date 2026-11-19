"""Train the rl-1 agents walk-forward (research/rl-1.md, "Agents" and "Walk-forward").

    uv run --with torch python research/lib/rl_train.py <variant> <seed> [fold years...]

Saves one model per fold to research/data/rl/models/<variant>/s<seed>/<Y>.pt (git-ignored) with
the fold's input scaling, and a JSON line per fold to .../log.jsonl (time, steps, GPU memory).
Variants are fixed in the plan; nothing here is chosen from out-of-sample results.
"""

from __future__ import annotations

import json
import math
import os
import sys
import time
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np
import rl_data
import torch
from rl_env import Obs, Table, WeekEnv
from torch import nn

MODELS = Path(os.environ.get("RL_MODELS", str(rl_data.harness.DATA / "rl" / "models")))
FOLDS = list(range(2000, 2025, 2))  # model Y trades from the first Friday of Y to that of Y + 2
EMBARGO_DAYS = 7
HORIZON = 52  # weeks per training episode
N_SIX, N_GSPC = 48, 16  # parallel episodes: three quarters six assets, a quarter S&P 500 index
UPDATES = int(os.environ.get("RL_UPDATES", "500"))  # PPO budget per fold (set from timing)
STEPS_PER_FOLD = UPDATES * HORIZON * (N_SIX + N_GSPC)
ES_ITERS = int(os.environ.get("RL_ES_ITERS", "125"))
REWARD_SCALE = 10.0


@dataclass(frozen=True)
class Variant:
    name: str
    hidden: int  # 0 = linear score
    algo: str  # "ppo" or "es"
    dd: float = 0.0  # drawdown penalty
    macro: bool = True


VARIANTS = {
    v.name: v
    for v in [
        Variant("ppo-lin", 0, "ppo"),
        Variant("ppo-mlp", 32, "ppo"),
        Variant("ppo-mlp-dd", 32, "ppo", dd=1.0),
        Variant("ppo-mlp-px", 32, "ppo", macro=False),
        Variant("es-lin", 0, "es"),
    ]
}


# --- folds and scaling ---


def train_end(t: Table, year: int) -> int:
    """Number of Fridays usable for training a model that trades from 1 January `year`: the
    week's reward must end EMBARGO_DAYS before it, and inside the book's bars."""
    cut = date(year, 1, 1).toordinal() - EMBARGO_DAYS - 7
    last = (t.book.first.toordinal() + len(t.book.opens) - 1) - 7
    return sum(1 for d in t.fridays if d.toordinal() <= min(cut, last))


@dataclass
class Scaler:
    mu_a: np.ndarray
    sd_a: np.ndarray
    mu_g: np.ndarray
    sd_g: np.ndarray
    macro: bool

    def asset(self, x: np.ndarray) -> np.ndarray:
        return (x - self.mu_a) / self.sd_a

    def shared(self, g: np.ndarray) -> np.ndarray:
        z = np.nan_to_num((g - self.mu_g) / self.sd_g, nan=0.0)
        return z if self.macro else np.zeros_like(z)


def fit_scaler(parts: list[tuple[Table, int]], macro: bool) -> Scaler:
    xa = np.concatenate([t.X[:e][t.elig[:e]] for t, e in parts])
    g = np.concatenate([t.G[:e] for t, e in parts])
    sd_a = xa.std(0)
    sd_g = np.nanstd(g, 0)
    return Scaler(
        xa.mean(0), np.where(sd_a > 1e-9, sd_a, 1.0),
        np.nanmean(g, 0), np.where(sd_g > 1e-9, sd_g, 1.0), macro,
    )  # fmt: skip


# --- policy ---

N_PAD = 6


def to_tensors(o: Obs, sc: Scaler, dev: torch.device) -> dict[str, torch.Tensor]:
    n = o.X.shape[1]
    pad = max(N_PAD - n, 0)
    xa = sc.asset(o.X) * o.elig[..., None]
    w = o.w
    el = o.elig
    if pad:
        xa = np.pad(xa, ((0, 0), (0, pad), (0, 0)))
        w = np.pad(w, ((0, 0), (0, pad)))
        el = np.pad(el, ((0, 0), (0, pad)))
    g = np.concatenate([sc.shared(o.G), o.cash[:, None]], axis=1)
    f = torch.float32
    return {
        "xa": torch.as_tensor(np.concatenate([xa, w[..., None]], axis=2), dtype=f, device=dev),
        "g": torch.as_tensor(g, dtype=f, device=dev),
        "el": torch.as_tensor(el, device=dev),
    }


def cat_obs(parts: list[dict[str, torch.Tensor]]) -> dict[str, torch.Tensor]:
    return {k: torch.cat([p[k] for p in parts]) for k in parts[0]}


class Net(nn.Module):
    """Shared per-asset score, a cash score, a value head. Scores -> masked softmax weights."""

    def __init__(self, a_dim: int, g_dim: int, hidden: int):
        super().__init__()
        inp = a_dim + g_dim
        if hidden:
            self.score: nn.Module = nn.Sequential(
                nn.Linear(inp, hidden), nn.Tanh(), nn.Linear(hidden, hidden), nn.Tanh(),
                nn.Linear(hidden, 1),
            )  # fmt: skip
        else:
            self.score = nn.Linear(inp, 1)
        self.cash = nn.Linear(g_dim, 1)
        self.value = nn.Sequential(
            nn.Linear(inp + 1, 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(), nn.Linear(64, 1)
        )
        self.log_std = nn.Parameter(torch.tensor(math.log(0.7)))

    def forward(self, o: dict[str, torch.Tensor]) -> tuple[torch.Tensor, torch.Tensor]:
        xa, g, el = o["xa"], o["g"], o["el"]
        n = xa.shape[1]
        ge = g[:, None, :].expand(-1, n, -1)
        s = self.score(torch.cat([xa, ge], dim=2)).squeeze(-1)
        mu = torch.cat([s, self.cash(g)], dim=1)  # [B, n + 1]
        elf = el.float()
        pooled = (xa * elf[..., None]).sum(1) / elf.sum(1, keepdim=True).clamp(min=1)
        v = self.value(torch.cat([pooled, g, elf.mean(1, keepdim=True)], dim=1)).squeeze(-1)
        return mu, v


def mask_all(el: torch.Tensor) -> torch.Tensor:
    return torch.cat([el, torch.ones_like(el[:, :1])], dim=1)


def to_weights(a: torch.Tensor, el: torch.Tensor) -> torch.Tensor:
    m = mask_all(el)
    w = torch.softmax(a.masked_fill(~m, -1e9), dim=1)[:, :-1]
    return torch.where(w > 1e-6, w, torch.zeros_like(w))


def log_prob(net: Net, mu: torch.Tensor, a: torch.Tensor, el: torch.Tensor) -> torch.Tensor:
    m = mask_all(el).float()
    std = net.log_std.exp()
    lp = -0.5 * ((a - mu) / std) ** 2 - net.log_std - 0.5 * math.log(2 * math.pi)
    return (lp * m).sum(1)


# --- training ---


def envs(
    tabs: dict[str, Table], year: int, rng: np.random.Generator, dd: float, n_six: int,
    n_gspc: int,
) -> list[WeekEnv]:  # fmt: skip
    six, gspc = tabs["six"], tabs["gspc"]
    return [
        WeekEnv(six, n_six, rng, 0, train_end(six, year), HORIZON, dd),
        WeekEnv(gspc, n_gspc, rng, 0, train_end(gspc, year), HORIZON, dd),
    ]


def act_split(w: np.ndarray, es: list[WeekEnv]) -> list[np.ndarray]:
    out, i = [], 0
    for e in es:
        n = len(e.t.book.syms)
        out.append(w[i : i + e.n, :n].astype(np.float64))
        i += e.n
    return out


def train_ppo(
    v: Variant, tabs: dict[str, Table], year: int, seed: int, dev: torch.device
) -> tuple[Net, Scaler, dict[str, float]]:
    rng = np.random.default_rng([seed, year])
    torch.manual_seed(seed * 10_000 + year)
    sc = fit_scaler([(tabs[k], train_end(tabs[k], year)) for k in ("six", "gspc")], v.macro)
    es = envs(tabs, year, rng, v.dd, N_SIX, N_GSPC)
    a_dim = tabs["six"].X.shape[2] + 1
    net = Net(a_dim, tabs["six"].G.shape[1] + 1, v.hidden).to(dev)
    opt = torch.optim.Adam(net.parameters(), lr=3e-4)
    gamma, lam, clip, epochs, n_mb = 0.99, 0.95, 0.2, 4, 4
    last_ret = 0.0
    for _ in range(UPDATES):
        buf: dict[str, list[torch.Tensor]] = {k: [] for k in ("o", "a", "lp", "v", "r", "d")}
        obs_l: list[dict[str, torch.Tensor]] = []
        for _t in range(HORIZON):
            o = cat_obs([to_tensors(e.obs(), sc, dev) for e in es])
            with torch.no_grad():
                mu, val = net(o)
                a = mu + net.log_std.exp() * torch.randn_like(mu)
                lp = log_prob(net, mu, a, o["el"])
                w = to_weights(a, o["el"]).cpu().numpy()
            rs, ds = [], []
            for e, we in zip(es, act_split(w, es), strict=True):
                r, d = e.step(we)
                rs.append(r)
                ds.append(d)
            obs_l.append(o)
            buf["a"].append(a)
            buf["lp"].append(lp)
            buf["v"].append(val)
            buf["r"].append(torch.as_tensor(np.concatenate(rs) * REWARD_SCALE, device=dev))
            buf["d"].append(torch.as_tensor(np.concatenate(ds), device=dev))
        with torch.no_grad():
            _, v_last = net(cat_obs([to_tensors(e.obs(), sc, dev) for e in es]))
        r_t = torch.stack(buf["r"]).float()
        d_t = torch.stack(buf["d"]).float()
        v_t = torch.stack(buf["v"])
        adv = torch.zeros_like(r_t)
        gae = torch.zeros_like(v_last)
        for t in reversed(range(HORIZON)):
            nxt = v_last if t == HORIZON - 1 else v_t[t + 1]
            nonterm = 1 - d_t[t]  # an episode's end counts as terminal (fixed in the plan)
            delta = r_t[t] + gamma * nxt * nonterm - v_t[t]
            gae = delta + gamma * lam * nonterm * gae
            adv[t] = gae
        ret = adv + v_t
        last_ret = float(r_t.sum(0).mean() / REWARD_SCALE)
        flat = cat_obs(obs_l)
        fa, flp = torch.cat(buf["a"]), torch.cat(buf["lp"])
        fadv, fret = adv.reshape(-1), ret.reshape(-1)
        fadv = (fadv - fadv.mean()) / (fadv.std() + 1e-8)
        nb = fa.shape[0]
        for _e in range(epochs):
            perm = torch.randperm(nb, device=dev)
            for mb in perm.chunk(n_mb):
                o = {k: x[mb] for k, x in flat.items()}
                mu, val = net(o)
                lp = log_prob(net, mu, fa[mb], o["el"])
                ratio = (lp - flp[mb]).exp()
                pg = -torch.min(ratio * fadv[mb], ratio.clamp(1 - clip, 1 + clip) * fadv[mb])
                loss = pg.mean() + 0.5 * ((val - fret[mb]) ** 2).mean() - 0.001 * net.log_std
                opt.zero_grad()
                loss.backward()
                nn.utils.clip_grad_norm_(net.parameters(), 0.5)
                opt.step()
    return net, sc, {"last_rollout_logret": last_ret, "std": float(net.log_std.exp().detach())}


def linear_params(net: Net) -> list[nn.Parameter]:
    return [*net.score.parameters(), *net.cash.parameters()]


def train_es(
    v: Variant, tabs: dict[str, Table], year: int, seed: int, dev: torch.device
) -> tuple[Net, Scaler, dict[str, float]]:
    """OpenAI-style ES on the linear policy: antithetic pairs, centred ranks, Adam."""
    rng = np.random.default_rng([seed, year, 1])
    torch.manual_seed(seed * 10_000 + year)
    sc = fit_scaler([(tabs[k], train_end(tabs[k], year)) for k in ("six", "gspc")], v.macro)
    a_dim = tabs["six"].X.shape[2] + 1
    net = Net(a_dim, tabs["six"].G.shape[1] + 1, 0).to(dev)
    params = linear_params(net)
    theta = nn.utils.parameters_to_vector(params).detach().clone()
    opt = torch.optim.Adam([theta.requires_grad_()], lr=0.02)
    pairs, n6, ng, sigma = 16, 6, 2, 0.1
    pop = 2 * pairs
    w_lin = net.score
    assert isinstance(w_lin, nn.Linear)
    fit_mean = 0.0
    for _ in range(ES_ITERS):
        eps = torch.randn(pairs, theta.numel(), device=dev)
        thetas = torch.cat([theta.detach() + sigma * eps, theta.detach() - sigma * eps])
        es = envs(tabs, year, rng, v.dd, n6 * pop, ng * pop)
        # same episodes for every member: copy the first member's starts to all
        for e, k in zip(es, (n6, ng), strict=True):
            e.f[:] = np.tile(e.f[:k], pop)
            e.stop[:] = np.tile(e.stop[:k], pop)
        member = torch.cat(
            [torch.arange(pop, device=dev).repeat_interleave(k) for k in (n6, ng)]
        )  # fmt: skip
        total = torch.zeros(member.numel(), device=dev)
        alive = torch.ones(member.numel(), dtype=torch.bool, device=dev)
        th = thetas[member]
        n_s = a_dim + net.cash.in_features
        for _t in range(HORIZON):
            o = cat_obs([to_tensors(e.obs(), sc, dev) for e in es])
            mu = linear_scores(o, th, n_s)
            w = to_weights(mu, o["el"]).cpu().numpy()
            rs, ds = [], []
            for e, we in zip(es, act_split(w, es), strict=True):
                r, d = e.step(we)
                rs.append(r)
                ds.append(d)
            total += torch.as_tensor(np.concatenate(rs), device=dev).float() * alive
            alive &= ~torch.as_tensor(np.concatenate(ds), device=dev)
        fit = torch.zeros(pop, device=dev).index_add_(0, member, total)
        fit_mean = float(fit.mean() / (n6 + ng))
        ranks = fit.argsort().argsort().float()
        util = ranks / (pop - 1) - 0.5
        grad = (util[:pairs] - util[pairs:]) @ eps / (pop * sigma)
        opt.zero_grad()
        theta.grad = -grad
        opt.step()
    nn.utils.vector_to_parameters(theta.detach(), params)
    return net, sc, {"last_mean_logret": fit_mean}


def linear_scores(o: dict[str, torch.Tensor], th: torch.Tensor, n_s: int) -> torch.Tensor:
    """Scores of the linear policy with one parameter row per environment. Layout as
    parameters_to_vector: score weight [inp], score bias, cash weight [g], cash bias."""
    xa, g = o["xa"], o["g"]
    n = xa.shape[1]
    inp = torch.cat([xa, g[:, None, :].expand(-1, n, -1)], dim=2)
    d = inp.shape[2]
    s = (inp * th[:, None, :d]).sum(2) + th[:, d : d + 1]
    gd = g.shape[1]
    c = (g * th[:, d + 1 : d + 1 + gd]).sum(1, keepdim=True) + th[:, d + 1 + gd : d + 2 + gd]
    return torch.cat([s, c], dim=1)


def main() -> None:
    torch.set_num_threads(1)
    v = VARIANTS[sys.argv[1]]
    seed = int(sys.argv[2])
    years = [int(y) for y in sys.argv[3:]] or FOLDS
    dev = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tabs = rl_data.load()
    out = MODELS / v.name / f"s{seed}"
    out.mkdir(parents=True, exist_ok=True)
    for y in years:
        if (out / f"{y}.pt").exists():
            continue
        t0 = time.time()
        fn = train_ppo if v.algo == "ppo" else train_es
        net, sc, info = fn(v, tabs, y, seed, dev)
        torch.save({"state": net.state_dict(), "scaler": sc.__dict__, "hidden": v.hidden},
                   out / f"{y}.pt")  # fmt: skip
        rec = {
            "variant": v.name, "seed": seed, "fold": y, "seconds": round(time.time() - t0, 1),
            "device": str(dev), "updates": UPDATES, "es_iters": ES_ITERS,
            "gpu_mem_mb": round(torch.cuda.max_memory_allocated() / 2**20, 1)
            if dev.type == "cuda" else 0.0,
            **info,
        }  # fmt: skip
        with (out / "log.jsonl").open("a") as f:
            f.write(json.dumps(rec) + "\n")
        print(json.dumps(rec), flush=True)


if __name__ == "__main__":
    main()
