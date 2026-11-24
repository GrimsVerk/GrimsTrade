"""pooled-1 engine: eight frozen `tsmom12` variants on one market, and the pooled paired test.
Card: research/cards/pooled-1.md. numpy only; no data access (see `pooled1.py`).

One market = daily closes (dates ascending). Decisions each calendar Friday from the closes
dated on or before it (`trend_tune.paper`'s rule), filled one session late: a decision on the
close of session j is traded at the close of session j + 1 and earns from session j + 2.
2 bps a side on every change of position, cash earns 0. The own-vol rules are an overlay on the
market's `tsmom12` daily returns (monthly reset, drift in between, 5 bps on the traded notional).
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np

COST = 0.0002  # one way, share of the position changed (insure-2's index cost)
RESET_COST = 0.0005  # own-vol monthly reset, share of the traded notional (risk-menu)
LAG = 1  # sessions between the decision close and the fill close
BPY = 252  # bars a year (`common.bpy` for a non-coin asset)
FRIDAY = 4
WARMUP = 24  # own-vol: monthly sigmas before k is solved (risk-menu-3)
STOP_K, FADE_L, VOL_HL = 0.25, 28, 60  # cointop-1's chosen settings
TV_TARGET = 0.40  # trend-vol
RULES = (
    "tsmom12",
    "e4",
    "or3-12",
    "arm3-12",
    "vt-own-70-x",
    "vt-own-26-x",
    "tv40",
    "fade-28",
    "stop-0.25",
)
VARIANTS = RULES[1:]


# --- signals at one decision (only closes up to index j are read) ---


def trailing_logret(d: np.ndarray, px: np.ndarray, j: int, days: int) -> float:
    """`common.trailing_logret` on the view of bars 0..j: log return over `days` calendar days."""
    target = d[j] - days
    if d[0] > target:
        return math.nan
    i = int(np.searchsorted(d[: j + 1], target, side="right")) - 1
    return float(math.log(px[j] / px[i]))


def up(d: np.ndarray, px: np.ndarray, j: int, days: int) -> bool:
    r = trailing_logret(d, px, j, days)
    return (not math.isnan(r)) and r > 0


def vol20(lr: np.ndarray, j: int) -> float:
    """`rules.vol20` on the view of bars 0..j (lr = all log returns; the view sees lr[:j])."""
    x = lr[max(0, j - 20) : j]
    return float(math.sqrt((x * x).mean() * BPY)) if len(x) else 0.0


def ewma_vol_path(px: np.ndarray, halflife: float = VOL_HL) -> np.ndarray:
    """`common.vol_series`: entry i is the annualised EWMA vol after log return i (bars i, i+1)."""
    lr = np.diff(np.log(px))
    lam = 0.5 ** (1 / halflife)
    out = np.empty(len(lr))
    num = den = 0.0
    for i, x in enumerate(lr):
        num = lam * num + x * x
        den = lam * den + 1.0
        out[i] = math.sqrt(num / den * BPY)
    return out


def stop_ok(d: np.ndarray, px: np.ndarray, ev: np.ndarray, j: int) -> bool:
    """`cointop1_carry.stop_ok` on bars 0..j: within STOP_K vol-years of the one-year high."""
    if j < 20 or not ev[j - 1] > 0:  # the view's vol series has j entries, the last is ev[j-1]
        return False
    lo = int(np.searchsorted(d[: j + 1], d[j] - 365, side="right"))
    hi = px[lo : j + 1].max()
    return bool(math.log(px[j] / hi) / ev[j - 1] >= -STOP_K)


# --- Friday decisions ---


def fridays(d: np.ndarray) -> list[tuple[int, int]]:
    """(Friday ordinal, index of the last session on or before it), as `tt.paper` loops."""
    first, last = int(d[0]), int(d[-1])
    fri = first + (FRIDAY - date.fromordinal(first).weekday()) % 7
    out = []
    while fri < last:
        out.append((fri, int(np.searchsorted(d, fri, side="right")) - 1))
        fri += 7
    return out


@dataclass
class Decisions:
    """Target position per rule at each decision session index (later Fridays on the same
    session overwrite earlier ones, as the paper loop does), and the first eligible index."""

    at: dict[str, dict[int, float]] = field(default_factory=dict)
    first_ok: int = -1


def decide(d: np.ndarray, px: np.ndarray, upto: int | None = None) -> Decisions:
    """Every price rule's Friday decisions (own-vol is an overlay, see `own_vol`). With `upto`
    only decisions on sessions <= upto are made (look-ahead tests)."""
    ev = ewma_vol_path(px)
    lr = np.diff(np.log(px))
    out = Decisions(
        {r: {} for r in ("tsmom12", "e4", "or3-12", "arm3-12", "tv40", "fade-28", "stop-0.25")}
    )
    pos_arm, armed, reentered = 0.0, False, False
    for _, j in fridays(d):
        if j < 0 or (upto is not None and j > upto):
            continue
        ok = j + 1 >= BPY and not math.isnan(trailing_logret(d, px, j, 365))
        if not ok:
            pos_arm, armed, reentered = 0.0, False, False
            for r in out.at:
                out.at[r][j] = 0.0
            continue
        if out.first_ok < 0:
            out.first_ok = j
        slow = up(d, px, j, 365)
        fast = up(d, px, j, 91)
        out.at["tsmom12"][j] = 1.0 if slow else 0.0
        out.at["e4"][j] = sum(up(d, px, j, x) for x in (30, 91, 182, 365)) / 4
        out.at["or3-12"][j] = 1.0 if (slow or fast) else 0.0
        # arm3-12: `fastreentry2.positions`, step for step
        if slow:
            pos_arm, armed, reentered = 1.0, False, False
        else:
            if pos_arm > 0 and reentered:
                pos_arm = 1.0 if fast else 0.0
            else:
                pos_arm = 1.0 if (armed and fast) else 0.0
            reentered = pos_arm > 0
            if not fast:
                armed = True
        out.at["arm3-12"][j] = pos_arm
        v = vol20(lr, j)
        out.at["tv40"][j] = (min(1.0, TV_TARGET / v) if v > 0 else 1.0) if slow else 0.0
        out.at["fade-28"][j] = 1.0 if (slow and up(d, px, j, FADE_L)) else 0.0
        out.at["stop-0.25"][j] = 1.0 if (slow and stop_ok(d, px, ev, j)) else 0.0
    return out


def held(n: int, at: Mapping[int, float], lag: int = LAG) -> np.ndarray:
    """Position earning return k (px[k] / px[k-1] - 1): the latest decision at index <= k-1-lag."""
    ff = np.zeros(n)
    cur = 0.0
    for i in range(n):
        cur = at.get(i, cur)
        ff[i] = cur
    h = np.zeros(n)
    if n > 1 + lag:
        h[1 + lag :] = ff[: n - 1 - lag]
    return h


def returns(px: np.ndarray, h: np.ndarray, cost: float = COST) -> np.ndarray:
    bar = np.zeros(len(px))
    bar[1:] = px[1:] / px[:-1] - 1
    return h * bar - cost * np.abs(np.diff(h, prepend=0.0))


# --- own-vol overlay ---


def sigma52(d: np.ndarray, x: np.ndarray, k: int, start: int) -> float:
    """`lstrend2_run.Sleeve.sigma(day k - 1)`: std (ddof 1) x sqrt 52 of the 52 complete
    Monday-Sunday weekly sums of x before day k; nan unless those weeks lie after `start`."""
    end = date.fromordinal(int(d[k])) - timedelta(days=1)
    last_sun = end - timedelta(days=(end.weekday() + 1) % 7)
    mon0 = last_sun - timedelta(days=52 * 7 - 1)
    if mon0.toordinal() < int(d[start]):
        return math.nan
    lo = int(np.searchsorted(d, mon0.toordinal(), side="left"))
    hi = int(np.searchsorted(d, last_sun.toordinal(), side="right"))
    wk = np.zeros(52)
    np.add.at(wk, (d[lo:hi] - mon0.toordinal()) // 7, x[lo:hi])
    return float(wk.std(ddof=1) * math.sqrt(52))


def solve_k(sig: Sequence[float], target: float) -> float:
    """`riskmenu3_run.solve_k`: k with mean(min(1, k / sigma)) = target."""
    s = np.array(sig)
    lo, hi = 0.0, 10.0
    for _ in range(60):
        k = (lo + hi) / 2
        lo, hi = (k, hi) if np.minimum(1.0, k / s).mean() < target else (lo, k)
    return (lo + hi) / 2


def own_vol(
    d: np.ndarray, x: np.ndarray, g: np.ndarray, start: int, target: float, upto: int | None = None
) -> tuple[np.ndarray, dict[int, float]]:
    """Book return per session: `tsmom12` sleeve (daily return x, gross position g) at share v,
    cash 0 the rest. v = target from `start`; reset on the first session of each month to
    min(1, k_d / sigma) with k_d from the sigmas seen so far (warm-up: target; sigma 0: keep
    the drifted share); drift in between. Returns (book returns, share set at each reset)."""
    n = len(x)
    out = np.zeros(n)
    plan: dict[int, float] = {}
    seen: list[float] = []
    v = target
    last = n - 1 if upto is None else upto
    for k in range(start, last + 1):
        cost = 0.0
        new_month = k > start and (
            date.fromordinal(int(d[k])).month != date.fromordinal(int(d[k - 1])).month
        )
        if new_month:
            sg = sigma52(d, x, k, start)
            if math.isfinite(sg) and sg > 0:
                seen.append(sg)
            if len(seen) < WARMUP or not math.isfinite(sg):
                a = target
            elif sg == 0:
                a = v
            else:
                a = min(1.0, solve_k(seen, target) / sg)
            plan[k] = a
            cost = RESET_COST * abs(a - v) * g[k]
            v = a
        out[k] = v * x[k] - cost
        n1 = v * (1 + x[k])
        v = n1 / (n1 + 1 - v)
    return out, plan


# --- one market ---


@dataclass
class Market:
    name: str
    group: str
    d: np.ndarray  # session ordinals
    px: np.ndarray  # closes
    start: int = -1  # first session whose return is scored
    daily: dict[str, np.ndarray] = field(default_factory=dict)
    pos: dict[str, np.ndarray] = field(default_factory=dict)


def run_market(name: str, group: str, d: np.ndarray, px: np.ndarray) -> Market:
    m = Market(name, group, d, px)
    dec = decide(d, px)
    if dec.first_ok < 0:
        raise ValueError(f"{name}: never eligible")
    m.start = dec.first_ok + 1 + LAG
    n = len(px)
    for r, at in dec.at.items():
        h = held(n, at)
        m.pos[r] = h
        m.daily[r] = returns(px, h)
    for r, t in (("vt-own-70-x", 0.70), ("vt-own-26-x", 0.26)):
        m.daily[r], _ = own_vol(d, m.daily["tsmom12"], m.pos["tsmom12"], m.start, t)
    return m


def friday_of(o: int) -> int:
    """The Friday ending the week (Saturday..Friday) that holds day ordinal o."""
    return o + (FRIDAY - date.fromordinal(o).weekday()) % 7


def weekly(d: np.ndarray, r: np.ndarray, start: int) -> tuple[np.ndarray, np.ndarray]:
    """(Friday ordinals, compounded weekly returns) of daily returns r[start:]."""
    keys = np.array([friday_of(int(o)) for o in d[start:]])
    uniq, inv = np.unique(keys, return_inverse=True)
    lg = np.zeros(len(uniq))
    np.add.at(lg, inv, np.log1p(r[start:]))
    return uniq, np.expm1(lg)


def sharpe(w: np.ndarray) -> float:
    sd = w.std()
    return float(w.mean() / sd * math.sqrt(52)) if sd > 0 else 0.0


# --- pooled test ---


@dataclass
class Panel:
    """Weekly returns on one Friday calendar: R[rule, market, week], NaN outside a market."""

    cal: np.ndarray
    names: list[str]
    groups: list[str]
    R: np.ndarray


def panel(markets: Sequence[Market], rules: Sequence[str] = RULES) -> Panel:
    lo = min(friday_of(int(m.d[m.start])) for m in markets)
    hi = max(friday_of(int(m.d[-1])) for m in markets)
    cal = np.arange(lo, hi + 1, 7)
    R = np.full((len(rules), len(markets), len(cal)), np.nan)
    for i, m in enumerate(markets):
        for a, r in enumerate(rules):
            f, w = weekly(m.d, m.daily[r], m.start)
            R[a, i, (f - lo) // 7] = w
    return Panel(cal, [m.name for m in markets], [m.group for m in markets], R)


def sharpe_from(s0: np.ndarray, s1: np.ndarray, s2: np.ndarray, min_n: int = 52) -> np.ndarray:
    with np.errstate(invalid="ignore", divide="ignore"):
        mu = s1 / s0
        var = s2 / s0 - mu * mu
        out = mu / np.sqrt(var) * math.sqrt(52)
    return np.where((s0 >= min_n) & (var > 0), out, np.nan)


def diffs_of(s0: np.ndarray, s1: np.ndarray, s2: np.ndarray) -> np.ndarray:
    """d[variant, market] = Sharpe(variant) - Sharpe(rule 0, the twin), from week sums."""
    sh = sharpe_from(s0, s1, s2)
    return sh[1:] - sh[:1]


def sums(R: np.ndarray, sel: np.ndarray | None = None) -> tuple[np.ndarray, ...]:
    x = R if sel is None else R[:, :, sel]
    ok = ~np.isnan(x)
    z = np.where(ok, x, 0.0)
    return ok.sum(-1).astype(float), z.sum(-1), (z * z).sum(-1)


def block_sums(R: np.ndarray, length: int) -> tuple[np.ndarray, ...]:
    """Sums over the circular block of `length` weeks starting at each week: (n, s1, s2)."""
    nw = R.shape[-1]
    ok = ~np.isnan(R)
    z = np.where(ok, R, 0.0)
    out = []
    for a in (ok.astype(float), z, z * z):
        ext = np.concatenate([a, a[..., :length]], axis=-1)
        cs = np.concatenate([np.zeros(a.shape[:-1] + (1,)), np.cumsum(ext, axis=-1)], axis=-1)
        out.append(cs[..., length : length + nw] - cs[..., :nw])
    return tuple(out)


@dataclass
class Boot:
    d: np.ndarray  # point estimate, d[variant, market]
    draws: np.ndarray  # D per draw for each pooled set: [set, variant, draw]
    sets: dict[str, np.ndarray]  # set name -> market mask


def bootstrap(
    p: Panel,
    sets: Mapping[str, np.ndarray],
    block: int = 52,
    draws: int = 2000,
    seed: int = 0,
    sel: np.ndarray | None = None,
) -> Boot:
    """Joint circular block bootstrap of calendar weeks (the same draw for every market)."""
    R = p.R if sel is None else p.R[:, :, sel]
    nw = R.shape[-1]
    d0 = diffs_of(*sums(R))
    nb = -(-nw // block)
    tail = nw - (nb - 1) * block
    full = block_sums(R, block)
    part = block_sums(R, tail)
    rng = np.random.default_rng(seed)
    names = list(sets)
    out = np.full((len(names), d0.shape[0], draws), np.nan)
    for b in range(draws):
        st = rng.integers(0, nw, nb)
        s = [f[..., st[:-1]].sum(-1) + q[..., st[-1]] for f, q in zip(full, part, strict=True)]
        db = diffs_of(*s)
        for i, nm in enumerate(names):
            out[i, :, b] = np.nanmean(db[:, sets[nm]], axis=1)
    return Boot(d0, out, dict(sets))


@dataclass
class Pooled:
    D: float
    se: float
    z: float
    lo: float
    hi: float
    plo: float
    phi: float
    n_pos: int
    n: int


def pooled(bt: Boot, set_name: str, v: int) -> Pooled:
    i = list(bt.sets).index(set_name)
    mask = bt.sets[set_name]
    dv = bt.d[v, mask]
    D = float(np.nanmean(dv))
    x = bt.draws[i, v]
    x = x[np.isfinite(x)]
    se = float(x.std(ddof=1))
    z = D / se if se > 0 else 0.0
    return Pooled(
        D,
        se,
        z,
        D - 1.96 * se,
        D + 1.96 * se,
        float(np.percentile(x, 2.5)),
        float(np.percentile(x, 97.5)),
        int((dv > 0).sum()),
        int(np.isfinite(dv).sum()),
    )


def verdict(
    p: Pooled,
    groups_pos: int,
    pre_pos: bool,
    z_bar: float = 2.50,
    z_proj: float = 4.69,
    kill_hi: float = 0.03,
) -> str:
    """The card's verdicts, in its order."""
    if p.z >= z_bar and groups_pos >= 3 and pre_pos:
        return "selectable candidate" if p.z >= z_proj else "real small edge"
    if p.hi < kill_hi or p.z <= -z_bar:
        return "killed"
    return "still open"
