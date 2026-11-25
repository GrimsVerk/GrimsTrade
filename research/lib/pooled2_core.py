"""pooled-2 engine: `tsmom12`, `e4` and `vt-own-70-x` on non-equity series, and the pooled test on
one monthly calendar. Card: research/cards/pooled-2.md. numpy only; no data access (`pooled2.py`).

Weekly (daily data): pooled-1's engine (`pooled1_core`), with the signal at Friday F read from the
last session whose value was public by F (`av`, from `long_x.available`), and own-vol's sigma
skipping the most recent complete week. With `av = d` and `skip = 0` both reduce to pooled-1's
code exactly (tests). Monthly (monthly-only data): the frozen monthly versions of the card, with a
gap of g months between the last return a signal reads and the return it trades.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from datetime import date, timedelta

import numpy as np
import pooled1_core as pc

RULES = ("tsmom12", "e4", "vt-own-70-x")
VARIANTS = RULES[1:]
TARGET = 0.70
E4_DAYS = (30, 91, 182, 365)
E4_MONTHS = (1, 3, 6, 12)
SIGMA_MONTHS = 36
MIN_PERIODS = {"w": 52, "m": 12}  # one year of periods for a Sharpe in a bootstrap draw
PPY = {"w": 52, "m": 12}


# --------------------------------------------------------------------------- weekly


def decide_weekly(
    d: np.ndarray, px: np.ndarray, av: np.ndarray, upto: int | None = None
) -> pc.Decisions:
    """`tsmom12` and `e4` Friday decisions (stored at the Friday's session j, as pooled-1), read
    from session js = the last one with av[js] <= Friday (and js <= j). av = d gives pooled-1."""
    out = pc.Decisions({"tsmom12": {}, "e4": {}})
    for fri, j in pc.fridays(d):
        if j < 0 or (upto is not None and j > upto):
            continue
        js = min(j, int(np.searchsorted(av, fri, side="right")) - 1)
        ok = js >= 0 and js + 1 >= pc.BPY and not math.isnan(pc.trailing_logret(d, px, js, 365))
        if not ok:
            out.at["tsmom12"][j] = 0.0
            out.at["e4"][j] = 0.0
            continue
        if out.first_ok < 0:
            out.first_ok = j
        out.at["tsmom12"][j] = 1.0 if pc.up(d, px, js, 365) else 0.0
        out.at["e4"][j] = sum(pc.up(d, px, js, x) for x in E4_DAYS) / 4
    return out


def sigma52_skip(d: np.ndarray, x: np.ndarray, k: int, start: int, skip: int) -> float:
    """`pooled1_core.sigma52` with the 52 weeks ending `skip` weeks earlier (skip 0 = pooled-1)."""
    end = date.fromordinal(int(d[k])) - timedelta(days=1)
    last_sun = end - timedelta(days=(end.weekday() + 1) % 7) - timedelta(days=7 * skip)
    mon0 = last_sun - timedelta(days=52 * 7 - 1)
    if mon0.toordinal() < int(d[start]):
        return math.nan
    lo = int(np.searchsorted(d, mon0.toordinal(), side="left"))
    hi = int(np.searchsorted(d, last_sun.toordinal(), side="right"))
    wk = np.zeros(52)
    np.add.at(wk, (d[lo:hi] - mon0.toordinal()) // 7, x[lo:hi])
    return float(wk.std(ddof=1) * math.sqrt(52))


def own_vol_weekly(
    d: np.ndarray,
    x: np.ndarray,
    g: np.ndarray,
    start: int,
    target: float = TARGET,
    skip: int = 1,
    reset_cost: float = pc.RESET_COST,
    upto: int | None = None,
) -> tuple[np.ndarray, dict[int, float]]:
    """`pooled1_core.own_vol` step for step, with `sigma52_skip` and a reset cost argument."""
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
            sg = sigma52_skip(d, x, k, start, skip)
            if math.isfinite(sg) and sg > 0:
                seen.append(sg)
            if len(seen) < pc.WARMUP or not math.isfinite(sg):
                a = target
            elif sg == 0:
                a = v
            else:
                a = min(1.0, pc.solve_k(seen, target) / sg)
            plan[k] = a
            cost = reset_cost * abs(a - v) * g[k]
            v = a
        out[k] = v * x[k] - cost
        n1 = v * (1 + x[k])
        v = n1 / (n1 + 1 - v)
    return out, plan


# --------------------------------------------------------------------------- monthly


def levels(r: np.ndarray) -> np.ndarray:
    """lv[0] = 1 before the first return, lv[i + 1] = level after return i."""
    return np.concatenate([[1.0], np.cumprod(1.0 + r)])


def decide_monthly(r_sig: np.ndarray, gap: int) -> tuple[dict[str, np.ndarray], int]:
    """Positions over each return t from levels through return t-1-gap (lv[t-gap]); the first
    eligible t is 12 + gap. Returns ({rule: positions}, first eligible t)."""
    lv = levels(r_sig)
    n = len(r_sig)
    pos = {"tsmom12": np.zeros(n), "e4": np.zeros(n)}
    first = 12 + gap
    for t in range(first, n):
        s = t - gap
        pos["tsmom12"][t] = 1.0 if lv[s] / lv[s - 12] > 1 else 0.0
        pos["e4"][t] = sum(lv[s] / lv[s - k] > 1 for k in E4_MONTHS) / 4
    return pos, first


def own_vol_monthly(
    x: np.ndarray,
    g: np.ndarray,
    start: int,
    gap: int,
    target: float = TARGET,
    reset_cost: float = pc.RESET_COST,
    window: int = SIGMA_MONTHS,
) -> tuple[np.ndarray, dict[int, float]]:
    """Monthly own-vol: reset at every month after `start` to min(1, k / sigma), sigma = sd
    (ddof 1) x sqrt 12 of the sleeve returns t-gap-window .. t-gap-1 (all at or after `start`),
    k = `solve_k` over the sigmas seen; warm-up 24 sigmas at the target; drift within the month."""
    n = len(x)
    out = np.zeros(n)
    plan: dict[int, float] = {}
    seen: list[float] = []
    v = target
    for t in range(start, n):
        cost = 0.0
        if t > start:
            lo, hi = t - gap - window, t - gap
            sg = float(x[lo:hi].std(ddof=1) * math.sqrt(12)) if lo >= start else math.nan
            if math.isfinite(sg) and sg > 0:
                seen.append(sg)
            if len(seen) < pc.WARMUP or not math.isfinite(sg):
                a = target
            elif sg == 0:
                a = v
            else:
                a = min(1.0, pc.solve_k(seen, target) / sg)
            plan[t] = a
            cost = reset_cost * abs(a - v) * g[t]
            v = a
        out[t] = v * x[t] - cost
        n1 = v * (1 + x[t])
        v = n1 / (n1 + 1 - v)
    return out, plan


# --------------------------------------------------------------------------- one market


@dataclass
class Mkt:
    """Scored period returns of each rule on one series. `periods` are ordinals of the period's
    end (weekly: the Friday; monthly: the first of the month the return ends in)."""

    name: str
    group: str
    freq: str  # "w" or "m"
    periods: np.ndarray
    rets: dict[str, np.ndarray] = field(default_factory=dict)
    turnover: dict[str, float] = field(default_factory=dict)  # position change a year


def run_weekly(
    name: str,
    group: str,
    d: np.ndarray,
    px_ret: np.ndarray,
    av: np.ndarray,
    cost: float,
    reset_cost: float = pc.RESET_COST,
    px_sig: np.ndarray | None = None,
    skip: int = 1,
) -> Mkt:
    dec = decide_weekly(d, px_ret if px_sig is None else px_sig, av)
    if dec.first_ok < 0:
        raise ValueError(f"{name}: never eligible")
    start = dec.first_ok + 1 + pc.LAG
    n = len(px_ret)
    daily: dict[str, np.ndarray] = {}
    pos: dict[str, np.ndarray] = {}
    for r, at in dec.at.items():
        pos[r] = pc.held(n, at)
        daily[r] = pc.returns(px_ret, pos[r], cost)
    daily["vt-own-70-x"], _ = own_vol_weekly(
        d, daily["tsmom12"], pos["tsmom12"], start, TARGET, skip, reset_cost
    )
    years = (int(d[-1]) - int(d[start])) / 365.25
    m = Mkt(name, group, "w", np.zeros(0, dtype=np.int64))
    for r in RULES:
        f, w = pc.weekly(d, daily[r], start)
        m.periods = f
        m.rets[r] = w
        if r in pos:
            m.turnover[r] = float(np.abs(np.diff(pos[r][start - 1 :])).sum() / years)
    return m


def run_monthly(
    name: str,
    group: str,
    months: Sequence[date],
    r_ret: np.ndarray,
    gap: int,
    cost: float,
    reset_cost: float = pc.RESET_COST,
    r_sig: np.ndarray | None = None,
) -> Mkt:
    pos, start = decide_monthly(r_ret if r_sig is None else r_sig, gap)
    if start >= len(r_ret) - 12:
        raise ValueError(f"{name}: too short")
    net = {r: p * r_ret - cost * np.abs(np.diff(p, prepend=0.0)) for r, p in pos.items()}
    net["vt-own-70-x"], _ = own_vol_monthly(
        net["tsmom12"], pos["tsmom12"], start, gap, TARGET, reset_cost
    )
    per = np.array([mo.toordinal() for mo in months[start:]], dtype=np.int64)
    m = Mkt(name, group, "m", per)
    years = (len(r_ret) - start) / 12
    for r in RULES:
        m.rets[r] = net[r][start:]
        if r in pos:
            m.turnover[r] = float(np.abs(np.diff(pos[r][start - 1 :])).sum() / years)
    return m


def from_pooled1(m: pc.Market) -> Mkt:
    """A pooled-1 equity market (its own run) as weekly scored returns of the three rules."""
    out = Mkt(m.name, "EQ-" + m.group, "w", np.zeros(0, dtype=np.int64))
    years = (int(m.d[-1]) - int(m.d[m.start])) / 365.25
    for r in RULES:
        f, w = pc.weekly(m.d, m.daily[r], m.start)
        out.periods, out.rets[r] = f, w
        if r in m.pos:
            out.turnover[r] = float(np.abs(np.diff(m.pos[r][m.start - 1 :])).sum() / years)
    return out


def stats(m: Mkt, r: str) -> tuple[float, float, float, float]:
    """(Sharpe at the series' frequency, total return, max drawdown, turnover or nan)."""
    w = m.rets[r]
    sd = w.std()
    sh = float(w.mean() / sd * math.sqrt(PPY[m.freq])) if sd > 0 else 0.0
    eq = np.cumprod(1 + w)
    mdd = float((1 - eq / np.maximum.accumulate(eq)).max())
    return sh, float(eq[-1] - 1), mdd, m.turnover.get(r, math.nan)


# --------------------------------------------------------------------------- monthly cells


def month_index(o: int) -> int:
    x = date.fromordinal(int(o))
    return x.year * 12 + x.month - 1


@dataclass
class Cells:
    """Per-month sums of each rule's period returns: S[k][rule, market, month], k = n, s1, s2."""

    cal: np.ndarray  # month index (year * 12 + month - 1)
    names: list[str]
    groups: list[str]
    freq: list[str]
    S: tuple[np.ndarray, np.ndarray, np.ndarray]


def cells(markets: Sequence[Mkt], rules: Sequence[str] = RULES) -> Cells:
    mi = [np.array([month_index(int(o)) for o in m.periods]) for m in markets]
    lo = min(int(x.min()) for x in mi)
    hi = max(int(x.max()) for x in mi)
    cal = np.arange(lo, hi + 1)
    shape = (len(rules), len(markets), len(cal))
    s0, s1, s2 = np.zeros(shape), np.zeros(shape), np.zeros(shape)
    for i, m in enumerate(markets):
        idx = mi[i] - lo
        for a, r in enumerate(rules):
            w = m.rets[r]
            np.add.at(s0[a, i], idx, 1.0)
            np.add.at(s1[a, i], idx, w)
            np.add.at(s2[a, i], idx, w * w)
    return Cells(
        cal,
        [m.name for m in markets],
        [m.group for m in markets],
        [m.freq for m in markets],
        (s0, s1, s2),
    )


def sharpe_from(
    s0: np.ndarray, s1: np.ndarray, s2: np.ndarray, ppy: np.ndarray, min_n: np.ndarray
) -> np.ndarray:
    """Sharpe[rule, market] from sums, annualised per market; nan below min_n periods."""
    with np.errstate(invalid="ignore", divide="ignore"):
        mu = s1 / s0
        var = s2 / s0 - mu * mu
        out = mu / np.sqrt(var) * np.sqrt(ppy)
    return np.where((s0 >= min_n) & (var > 0), out, np.nan)


def diffs(c: Cells, S: Sequence[np.ndarray]) -> np.ndarray:
    """d[variant, market] from total sums S = (n, s1, s2)[rule, market]."""
    ppy = np.array([PPY[f] for f in c.freq], dtype=float)
    mn = np.array([MIN_PERIODS[f] for f in c.freq], dtype=float)
    sh = sharpe_from(S[0], S[1], S[2], ppy, mn)
    return sh[1:] - sh[:1]


def block_sums(a: np.ndarray, length: int) -> np.ndarray:
    """Sums over the circular block of `length` months starting at each month."""
    nm = a.shape[-1]
    ext = np.concatenate([a, a[..., :length]], axis=-1)
    cs = np.concatenate([np.zeros(a.shape[:-1] + (1,)), np.cumsum(ext, axis=-1)], axis=-1)
    return cs[..., length : length + nm] - cs[..., :nm]


@dataclass
class Boot:
    d: np.ndarray  # d[variant, market]
    draws: np.ndarray  # D per draw: [set, variant, draw]
    sets: dict[str, np.ndarray]
    dm: np.ndarray  # per-market d per draw: [variant, market, draw]


def bootstrap(
    c: Cells,
    sets: Mapping[str, np.ndarray],
    block: int = 12,
    draws: int = 2000,
    seed: int = 0,
    sel: np.ndarray | None = None,
) -> Boot:
    """Joint circular block bootstrap of calendar months (one draw for every market)."""
    S = tuple(s if sel is None else s[..., sel] for s in c.S)
    nm = S[0].shape[-1]
    d0 = diffs(c, [x.sum(-1) for x in S])
    nb = -(-nm // block)
    tail = nm - (nb - 1) * block
    full = [block_sums(s, block) for s in S]
    part = [block_sums(s, tail) for s in S]
    rng = np.random.default_rng(seed)
    names = list(sets)
    out = np.full((len(names), d0.shape[0], draws), np.nan)
    dm = np.full((d0.shape[0], d0.shape[1], draws), np.nan)
    for b in range(draws):
        st = rng.integers(0, nm, nb)
        s = [f[..., st[:-1]].sum(-1) + q[..., st[-1]] for f, q in zip(full, part, strict=True)]
        db = diffs(c, s)
        dm[:, :, b] = db
        with np.errstate(invalid="ignore"):
            for i, nmz in enumerate(names):
                m = sets[nmz]
                out[i, :, b] = (
                    np.nanmean(db[:, m], axis=1) if np.isfinite(db[:, m]).any() else np.nan
                )
    return Boot(d0, out, dict(sets), dm)


def pooled(bt: Boot, set_name: str, v: int) -> pc.Pooled:
    return pc.pooled(pc.Boot(bt.d, bt.draws, bt.sets), set_name, v)


def balanced(bt: Boot, a: str, b: str, v: int) -> tuple[float, float]:
    """(D, SE) of the class-balanced mean (D_a + D_b) / 2, same draws."""
    names = list(bt.sets)
    da = float(np.nanmean(bt.d[v, bt.sets[a]]))
    db = float(np.nanmean(bt.d[v, bt.sets[b]]))
    x = (bt.draws[names.index(a), v] + bt.draws[names.index(b), v]) / 2
    x = x[np.isfinite(x)]
    return (da + db) / 2, float(x.std(ddof=1))


def mean_pair_corr(bt: Boot, v: int, mask: np.ndarray) -> float:
    """Mean pairwise correlation, over draws, of the per-market d within a set."""
    x = bt.dm[v][mask]
    x = x[np.isfinite(x).all(axis=1)]
    if len(x) < 2:
        return math.nan
    cc = np.corrcoef(x)
    iu = np.triu_indices(len(x), 1)
    return float(cc[iu].mean())


def verdict(
    p: pc.Pooled,
    groups_pos: int,
    pre_pos: bool,
    z_bar: float = 2.50,
    z_proj: float = 4.70,
    kill_hi: float = 0.03,
    need_groups: int = 2,
) -> str:
    """The card's verdicts, in its order (judged pool: 2 of 3 groups)."""
    if p.z >= z_bar and groups_pos >= need_groups and pre_pos:
        return "selectable candidate" if p.z >= z_proj else "real small edge"
    if p.hi < kill_hi or p.z <= -z_bar:
        return "killed"
    return "still open"
