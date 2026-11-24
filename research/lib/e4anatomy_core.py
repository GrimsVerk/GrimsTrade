"""e4-anatomy-1 engine: where `e4`'s lead over `tsmom12` comes from, by regime and by leg.
Card: research/cards/e4-anatomy-1.md. numpy only; no data access (see `e4anatomy.py`).

A descriptive re-score: the rules are pooled-1's / pooled-2's frozen code, re-run here with the
four `e4` legs kept apart. Per series, exactly:

    d = SR_e4 - SR_ts = (mu_e4 - mu_ts) / sd_e4 * sqrt(P)            return part
                      + mu_ts * (1 / sd_e4 - 1 / sd_ts) * sqrt(P)     risk part

and the return part splits by period into regimes and, before costs, into legs:
dr = sum over L in (30, 91, 182) of (h_L - h_365) / 4 x market return, plus the cost term.
"""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass, field
from datetime import date
from typing import Any

import numpy as np
import pooled1_core as pc

E4_DAYS = (30, 91, 182, 365)
E4_MONTHS = (1, 3, 6, 12)
LEGS = ("1m", "3m", "6m")  # each against the 12-month leg, weight 1/4
FAST, REBOUND = 92, 365  # insure-1: calendar days peak -> trough; rebound span after the trough
MEDIUM = 365
PPY = {"w": 52, "m": 12}
# regime codes; priority fall > rebound > whipsaw > calm
FASTC, MEDC, LONGC, REBC, WHIPC, CALMC = 0, 1, 2, 3, 4, 5
REGIMES = ("fast", "slow-medium", "slow-long", "rebound", "whipsaw", "calm")


# --------------------------------------------------------------------------- regimes


def zigzag(px: np.ndarray, down: float, up: float) -> tuple[list[tuple[int, int]], int | None]:
    """insure-1's zigzag, step for step: confirmed (peak, trough) index pairs, and the peak of
    an unfinished fall at the end (None if the series ends outside a fall)."""
    out: list[tuple[int, int]] = []
    falling, pk, tr = False, 0, 0
    for i in range(1, len(px)):
        if not falling:
            if px[i] > px[pk]:
                pk = i
            elif px[i] <= px[pk] * (1 - down):
                falling, tr = True, i
        else:
            if px[i] < px[tr]:
                tr = i
            elif px[i] >= px[tr] * (1 + up):
                out.append((pk, tr))
                falling, pk = False, i
    return out, (pk if falling else None)


def fall_labels(
    ords: np.ndarray, px: np.ndarray, down: float, up: float, rebound_n: int | None = None
) -> np.ndarray:
    """Label every point of a level series (index i = the move px[i-1] -> px[i]): falls
    (peak, trough] as fast / medium / long by calendar days peak -> trough, rebounds
    (trough, min(trough + 365 days, next peak)], calm otherwise (whipsaw is added later).
    With `rebound_n` the rebound is that many points instead of 365 days (monthly series)."""
    lab = np.full(len(px), CALMC, dtype=np.int8)
    pairs, open_pk = zigzag(px, down, up)
    peaks = [a for a, _ in pairs[1:]] + ([open_pk] if open_pk is not None else [])
    for j, (a, b) in enumerate(pairs):
        days = int(ords[b] - ords[a])
        code = FASTC if days <= FAST else (MEDC if days <= MEDIUM else LONGC)
        lab[a + 1 : b + 1] = code
        if rebound_n is None:
            e = int(np.searchsorted(ords, int(ords[b]) + REBOUND, side="right")) - 1
        else:
            e = min(len(px) - 1, b + rebound_n)
        if j < len(peaks):
            e = min(e, peaks[j])
        lab[b + 1 : e + 1] = REBC
    return lab


def whipsaw(sig: np.ndarray, half: int) -> np.ndarray:
    """True at decision i if the 0/1 signal changes at least twice among decisions
    i - half .. i + half (changes between consecutive decisions inside that window)."""
    ch = np.zeros(len(sig), dtype=np.int64)
    ch[1:] = (np.diff(sig) != 0).astype(np.int64)
    cs = np.concatenate([[0], np.cumsum(ch)])
    n = len(sig)
    out = np.zeros(n, dtype=bool)
    for i in range(n):
        lo, hi = max(0, i - half), min(n - 1, i + half)
        out[i] = (cs[hi + 1] - cs[lo + 1]) >= 2  # changes at lo+1 .. hi
    return out


# --------------------------------------------------------------------------- legs, weekly


@dataclass
class WeeklyLegs:
    at: dict[int, dict[int, float]]  # leg days -> {session index: 0/1}
    e4: dict[int, float]  # pooled-1's own e4 expression at each decision
    fri: list[int]  # Friday ordinals of eligible decisions
    sig12: list[float]  # the 12-month leg at those Fridays
    first_ok: int = -1


def decide_legs(d: np.ndarray, px: np.ndarray, av: np.ndarray) -> WeeklyLegs:
    """`pooled2_core.decide_weekly` (av = d: `pooled1_core.decide`), with each leg kept."""
    out = WeeklyLegs({x: {} for x in E4_DAYS}, {}, [], [])
    for fri, j in pc.fridays(d):
        if j < 0:
            continue
        js = min(j, int(np.searchsorted(av, fri, side="right")) - 1)
        ok = js >= 0 and js + 1 >= pc.BPY and not math.isnan(pc.trailing_logret(d, px, js, 365))
        if not ok:
            for x in E4_DAYS:
                out.at[x][j] = 0.0
            out.e4[j] = 0.0
            continue
        if out.first_ok < 0:
            out.first_ok = j
        for x in E4_DAYS:
            out.at[x][j] = 1.0 if pc.up(d, px, js, x) else 0.0
        out.e4[j] = sum(pc.up(d, px, js, x) for x in E4_DAYS) / 4
        out.fri.append(fri)
        out.sig12.append(out.at[365][j])
    return out


def week_keys(d: np.ndarray, start: int) -> tuple[np.ndarray, np.ndarray]:
    """(Friday ordinals, inverse index of each session from `start`), as `pc.weekly` groups."""
    keys = np.array([pc.friday_of(int(o)) for o in d[start:]])
    return np.unique(keys, return_inverse=True)


@dataclass
class Series:
    """One series' scored periods: e4 and tsmom12 returns, the return difference split by leg,
    the mean position gap, and labels per reading."""

    name: str
    group: str
    freq: str
    periods: np.ndarray  # period end ordinals (Friday / first of the month)
    r_e4: np.ndarray
    r_ts: np.ndarray
    legs: dict[str, np.ndarray]  # "1m", "3m", "6m", "cost", "resid": sum = r_e4 - r_ts
    gap: np.ndarray  # mean position e4 - tsmom12 over the period
    labels: dict[str, np.ndarray] = field(default_factory=dict)


def run_weekly(
    name: str,
    group: str,
    d: np.ndarray,
    px: np.ndarray,
    av: np.ndarray,
    cost: float,
    readings: dict[str, tuple[float, int]],
) -> Series:
    """pooled-1 / pooled-2 weekly engine with legs. `readings`: name -> (zigzag threshold,
    whipsaw half-window in decisions)."""
    lg = decide_legs(d, px, av)
    if lg.first_ok < 0:
        raise ValueError(f"{name}: never eligible")
    start = lg.first_ok + 1 + pc.LAG
    n = len(px)
    h = {x: pc.held(n, lg.at[x]) for x in E4_DAYS}
    h_e4 = pc.held(n, lg.e4)
    bar = np.zeros(n)
    bar[1:] = px[1:] / px[:-1] - 1
    r_e4_d = pc.returns(px, h_e4, cost)
    r_ts_d = pc.returns(px, h[365], cost)
    f, w_e4 = pc.weekly(d, r_e4_d, start)
    _, w_ts = pc.weekly(d, r_ts_d, start)
    uniq, inv = week_keys(d, start)
    assert np.array_equal(uniq, f)

    def wsum(x: np.ndarray) -> np.ndarray:
        out = np.zeros(len(uniq))
        np.add.at(out, inv, x[start:])
        return out

    legs = {k: wsum((h[x] - h[365]) / 4 * bar) for k, x in zip(LEGS, E4_DAYS[:3], strict=True)}
    legs["cost"] = wsum(
        -cost * np.abs(np.diff(h_e4, prepend=0.0)) + cost * np.abs(np.diff(h[365], prepend=0.0))
    )
    legs["resid"] = (w_e4 - w_ts) - sum(legs.values())
    cnt = np.zeros(len(uniq))
    np.add.at(cnt, inv, 1.0)
    gap = wsum(h_e4 - h[365]) / cnt
    last = np.zeros(len(uniq), dtype=np.int64)
    np.maximum.at(last, inv, np.arange(start, n))
    s = Series(name, group, "w", f, w_e4, w_ts, legs, gap)
    fri = np.array(lg.fri, dtype=np.int64)
    sig = np.array(lg.sig12)
    for rd, (thr, half) in readings.items():
        lab = fall_labels(d, px, thr, thr)[last].copy()
        ws = whipsaw(sig, half)
        k = np.searchsorted(fri, f, side="right") - 1  # latest decision on or before the week
        wk = np.where(k >= 0, ws[np.clip(k, 0, None)], False)
        lab[(lab == CALMC) & wk] = WHIPC
        s.labels[rd] = lab
    return s


# --------------------------------------------------------------------------- legs, monthly


def run_monthly(
    name: str,
    group: str,
    months: Sequence[date],
    r_ret: np.ndarray,
    gap: int,
    cost: float,
    readings: dict[str, tuple[float, int]],
) -> Series:
    """`pooled2_core.run_monthly` (signals on r_ret) with legs; split exact."""
    lv = np.concatenate([[1.0], np.cumprod(1.0 + r_ret)])
    n = len(r_ret)
    first = 12 + gap
    if first >= n - 12:
        raise ValueError(f"{name}: too short")
    p = {k: np.zeros(n) for k in E4_MONTHS}
    p_e4 = np.zeros(n)
    for t in range(first, n):
        s_ = t - gap
        for k in E4_MONTHS:
            p[k][t] = 1.0 if lv[s_] / lv[s_ - k] > 1 else 0.0
        p_e4[t] = sum(lv[s_] / lv[s_ - k] > 1 for k in E4_MONTHS) / 4
    net_e4 = p_e4 * r_ret - cost * np.abs(np.diff(p_e4, prepend=0.0))
    net_ts = p[12] * r_ret - cost * np.abs(np.diff(p[12], prepend=0.0))
    sl = slice(first, n)
    legs = {
        lab: ((p[k] - p[12]) / 4 * r_ret)[sl] for lab, k in zip(LEGS, E4_MONTHS[:3], strict=True)
    }
    legs["cost"] = (
        -cost * np.abs(np.diff(p_e4, prepend=0.0)) + cost * np.abs(np.diff(p[12], prepend=0.0))
    )[sl]
    legs["resid"] = (net_e4 - net_ts)[sl] - sum(legs.values())
    per = np.array([m.toordinal() for m in months[first:]], dtype=np.int64)
    s = Series(name, group, "m", per, net_e4[sl], net_ts[sl], legs, (p_e4 - p[12])[sl])
    # level index i + 1 is the level after return i, dated by the month it ends in
    m0 = months[0]
    prev = date(m0.year - (m0.month == 1), (m0.month - 2) % 12 + 1, 1)
    ords = np.array([prev.toordinal(), *[m.toordinal() for m in months]], dtype=np.int64)
    for rd, (thr, half) in readings.items():
        lab_lv = fall_labels(ords, lv, thr, thr, rebound_n=12)
        lab = lab_lv[1:][sl].copy()  # return i -> level index i + 1
        ws = whipsaw(p[12][first:], max(1, round(half * 3 / 13)))
        lab[(lab == CALMC) & ws] = WHIPC
        s.labels[rd] = lab
    return s


# --------------------------------------------------------------------------- decomposition


@dataclass
class Parts:
    d: float
    ret: float  # return part
    risk: float  # risk part
    by_regime: dict[str, float]
    by_leg: dict[str, float]
    leg_regime: dict[str, dict[str, float]]
    share: dict[str, float]  # time share by regime
    var_share: dict[str, float]  # share of var(e4) - var(ts) by regime
    gap: dict[str, float]  # mean position gap e4 - tsmom12 by regime
    sd_e4: float
    sd_ts: float
    mu_ts: float


def sharpe(x: np.ndarray, ppy: int) -> float:
    sd = x.std()
    return float(x.mean() / sd * math.sqrt(ppy)) if sd > 0 else 0.0


def parts(s: Series, reading: str) -> Parts:
    P = PPY[s.freq]
    T = len(s.r_e4)
    mu_e, mu_t = float(s.r_e4.mean()), float(s.r_ts.mean())
    sd_e, sd_t = float(s.r_e4.std()), float(s.r_ts.std())
    sc = math.sqrt(P) / sd_e / T
    dr = s.r_e4 - s.r_ts
    lab = s.labels[reading]
    by_regime, share, var_share, gap = {}, {}, {}, {}
    leg_regime: dict[str, dict[str, float]] = {}
    dv = (s.r_e4 - mu_e) ** 2 - (s.r_ts - mu_t) ** 2
    vtot = float(dv.sum())
    for c, nm in enumerate(REGIMES):
        m = lab == c
        by_regime[nm] = float(dr[m].sum() * sc)
        share[nm] = float(m.mean())
        var_share[nm] = float(dv[m].sum() / vtot) if vtot != 0 else math.nan
        gap[nm] = float(s.gap[m].mean()) if m.any() else math.nan
        leg_regime[nm] = {k: float(v[m].sum() * sc) for k, v in s.legs.items()}
    ret = (mu_e - mu_t) / sd_e * math.sqrt(P)
    risk = mu_t * (1 / sd_e - 1 / sd_t) * math.sqrt(P)
    d = sharpe(s.r_e4, P) - sharpe(s.r_ts, P)
    by_leg = {k: float(v.sum() * sc) for k, v in s.legs.items()}
    if abs(sum(by_regime.values()) - ret) > 1e-9 or abs(ret + risk - d) > 1e-9:
        raise AssertionError(f"{s.name}: decomposition does not add up")
    if abs(sum(by_leg.values()) - ret) > 1e-9:
        raise AssertionError(f"{s.name}: legs do not add up")
    return Parts(
        d, ret, risk, by_regime, by_leg, leg_regime, share, var_share, gap, sd_e, sd_t, mu_t
    )


def merge_slow(x: dict[str, float]) -> dict[str, float]:
    """fast / slow (medium + long) / rebound / whipsaw / calm."""
    return {
        "fast": x["fast"],
        "slow": x["slow-medium"] + x["slow-long"],
        "rebound": x["rebound"],
        "whipsaw": x["whipsaw"],
        "calm": x["calm"],
    }


MERGED = ("fast", "slow", "rebound", "whipsaw", "calm")


def merge_slow_legs(x: dict[str, dict[str, float]]) -> dict[str, dict[str, float]]:
    """`merge_slow` for the leg x regime table."""
    keys = x["fast"].keys()
    return {
        "fast": dict(x["fast"]),
        "slow": {k: x["slow-medium"][k] + x["slow-long"][k] for k in keys},
        "rebound": dict(x["rebound"]),
        "whipsaw": dict(x["whipsaw"]),
        "calm": dict(x["calm"]),
    }


def merge_slow_gap(p: Parts) -> dict[str, float]:
    """Mean position gap by merged regime (slow = time-weighted mean of medium and long)."""
    g, sh = p.gap, p.share
    w = sh["slow-medium"] + sh["slow-long"]
    if w > 0:
        a = g["slow-medium"] if sh["slow-medium"] > 0 else 0.0
        b = g["slow-long"] if sh["slow-long"] > 0 else 0.0
        slow = (a * sh["slow-medium"] + b * sh["slow-long"]) / w
    else:
        slow = math.nan
    return {"fast": g["fast"], "slow": slow, "rebound": g["rebound"], "whipsaw": g["whipsaw"],
            "calm": g["calm"]}  # fmt: skip


def mix_split(
    S_a: dict[str, float],
    C_a: dict[str, float],
    S_b: dict[str, float],
    C_b: dict[str, float],
    risk_a: float,
    risk_b: float,
) -> dict[str, float]:
    """D_a - D_b = mix + rates + risk, both orders (exact). rate = C / S (0 if S = 0)."""

    def rate(C: dict[str, float], S: dict[str, float], k: str) -> float:
        return C[k] / S[k] if S[k] > 0 else 0.0

    ks = list(S_a)
    mix_b = sum((S_a[k] - S_b[k]) * rate(C_b, S_b, k) for k in ks)
    rates_b = sum(S_a[k] * (rate(C_a, S_a, k) - rate(C_b, S_b, k)) for k in ks)
    mix_a = sum((S_a[k] - S_b[k]) * rate(C_a, S_a, k) for k in ks)
    rates_a = sum(S_b[k] * (rate(C_a, S_a, k) - rate(C_b, S_b, k)) for k in ks)
    return {
        "gap": sum(C_a.values()) + risk_a - sum(C_b.values()) - risk_b,
        "mix_at_b_rates": mix_b,
        "rates_at_a_mix": rates_b,
        "mix_at_a_rates": mix_a,
        "rates_at_b_mix": rates_a,
        "risk": risk_a - risk_b,
    }


def mix_reading(m: dict[str, float]) -> str:
    """The card's reading of the gap (applied to reading B)."""
    g = m["gap"]
    if g == 0:
        return "no gap"
    if min(m["mix_at_b_rates"], m["mix_at_a_rates"]) / g >= 0.5:
        return "explained by regime mix"
    if min(m["rates_at_a_mix"], m["rates_at_b_mix"]) / g >= 0.5:
        return "by rates"
    if m["risk"] / g >= 0.5:
        return "by the risk part"
    return "mixed"


# --------------------------------------------------------------------------- bootstrap


def month_index(o: int) -> int:
    x = date.fromordinal(int(o))
    return x.year * 12 + x.month - 1


@dataclass
class Cal:
    """Per-month sums, one channel each: X[channel][series, month]."""

    cal: np.ndarray
    X: dict[str, np.ndarray]


def month_cells(series: Sequence[Series], reading: str, fixed: Sequence[Parts]) -> Cal:
    """Channels: n (periods), n_<regime> (periods in regime), c_<regime> (dr scaled by the
    full-sample sqrt(P) / sd_e4), ts (r_ts scaled by sqrt(P) x (1/sd_e4 - 1/sd_ts))."""
    mi = [np.array([month_index(int(o)) for o in s.periods]) for s in series]
    lo = min(int(x.min()) for x in mi)
    hi = max(int(x.max()) for x in mi)
    cal = np.arange(lo, hi + 1)
    names = ["n", "ts"] + [f"n_{r}" for r in REGIMES] + [f"c_{r}" for r in REGIMES]
    X = {k: np.zeros((len(series), len(cal))) for k in names}
    for i, (s, p) in enumerate(zip(series, fixed, strict=True)):
        idx = mi[i] - lo
        P = PPY[s.freq]
        sc = math.sqrt(P) / p.sd_e4
        dr = s.r_e4 - s.r_ts
        lab = s.labels[reading]
        np.add.at(X["n"][i], idx, 1.0)
        np.add.at(X["ts"][i], idx, s.r_ts * math.sqrt(P) * (1 / p.sd_e4 - 1 / p.sd_ts))
        for c, r in enumerate(REGIMES):
            m = lab == c
            np.add.at(X[f"n_{r}"][i], idx[m], 1.0)
            np.add.at(X[f"c_{r}"][i], idx[m], dr[m] * sc)
    return Cal(cal, X)


def _block(a: np.ndarray, length: int) -> np.ndarray:
    nm = a.shape[-1]
    ext = np.concatenate([a, a[..., :length]], axis=-1)
    cs = np.concatenate([np.zeros(a.shape[:-1] + (1,)), np.cumsum(ext, axis=-1)], axis=-1)
    return cs[..., length : length + nm] - cs[..., :nm]


def pool_stats(X: dict[str, np.ndarray], mask: np.ndarray, min_n: np.ndarray) -> dict[str, Any]:
    """Pool means of S (time shares), C (return part per regime) and the risk part, from sums.
    Series with fewer than min_n periods are left out (as pooled-2's one-year minimum)."""
    n = X["n"]
    ok = mask & (n >= min_n)
    with np.errstate(invalid="ignore", divide="ignore"):
        S = {r: float(np.mean(X[f"n_{r}"][ok] / n[ok])) for r in REGIMES}
        C = {r: float(np.mean(X[f"c_{r}"][ok] / n[ok])) for r in REGIMES}
        risk = float(np.mean(X["ts"][ok] / n[ok]))
    return {"S": S, "C": C, "risk": risk}


def boot_draws(
    cal: Cal, min_n: np.ndarray, block: int = 12, draws: int = 2000, seed: int = 0
) -> list[dict[str, np.ndarray]]:
    """Joint circular block bootstrap of calendar months: per draw, the per-series totals of
    each channel (the same months for every series)."""
    nm = len(cal.cal)
    nb = -(-nm // block)
    tail = nm - (nb - 1) * block
    full = {k: _block(v, block) for k, v in cal.X.items()}
    part = {k: _block(v, tail) for k, v in cal.X.items()}
    rng = np.random.default_rng(seed)
    out = []
    for _ in range(draws):
        st = rng.integers(0, nm, nb)
        out.append({k: full[k][:, st[:-1]].sum(-1) + part[k][:, st[-1]] for k in cal.X})
    return out


def totals(cal: Cal) -> dict[str, np.ndarray]:
    return {k: v.sum(-1) for k, v in cal.X.items()}
