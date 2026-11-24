"""Pure-numpy pieces of research run cointop-1 (card in research/cointop-1.md).

Everything is a calendar-day matrix `[days, coins]` as in `breadth_xs`. No harness import here
(the harness changes the global asset list), so the tests can load this file alone.

- `find_tops`: the card's top (a high followed by a fall of at least 50%; a low is settled by a
  doubling). Made with hindsight: a description, never a rule input.
- `ewma_vol`, `roll_max`, `conditions`: the inputs of the three exit rules, row `t` from prices
  stamped `t` or earlier. The caller lags them one day (Coin Metrics' as-of rule).
- `paper`: per-coin paper series of 0/1 positions decided weekly, with costs.
- `pooled_sharpe`, `pooled_boot`: the card's selection score and its date bootstrap.
- `auc`: rank AUC with ties, for the "what precedes a top" table.
"""

from __future__ import annotations

from dataclasses import dataclass

import breadth_xs as xs
import numpy as np
import stats

COST = 0.003  # 30 bps a side (protocol, crypto)
STOP_GRID = (0.25, 0.5, 0.75, 1.0)
DAYS_GRID = (28, 56, 91, 182)


@dataclass
class Top:
    top: int  # row of the high
    halved: int  # first row at or below half of the high
    low: int  # row of the lowest price that followed (so far, if the low is not settled)
    settled: int  # row at which the price had doubled from the low; -1 if still open


def find_tops(p: np.ndarray) -> tuple[list[Top], int]:
    """Tops of one price series (NaN where unknown). Returns the tops and the row of the running
    high the series ends on if it ends in a rise (an "open" high, not a top), else -1."""
    tops: list[Top] = []
    idx = np.flatnonzero(np.isfinite(p))
    if len(idx) == 0:
        return tops, -1
    hi = int(idx[0])
    cur: Top | None = None
    for i in idx[1:]:
        i = int(i)
        if cur is None:
            if p[i] > p[hi]:
                hi = i
            elif p[i] <= p[hi] / 2:
                cur = Top(hi, i, i, -1)
        elif p[i] < p[cur.low]:
            cur.low = i
        elif p[i] >= 2 * p[cur.low]:
            cur.settled = i
            tops.append(cur)
            cur = None
            hi = i  # the first close at twice the low is the highest since the low
    if cur is not None:
        tops.append(cur)
        return tops, -1
    return tops, hi


def ewma_vol(px: np.ndarray, halflife: float, min_bars: int = 20) -> np.ndarray:
    """Annualised EWMA volatility of daily log returns (zero mean), the recursion of
    `common.vol_series`. Row t uses returns up to row t. A missing return leaves the state as it
    was. NaN until `min_bars` returns have been seen."""
    lam = 0.5 ** (1 / halflife)
    with np.errstate(invalid="ignore", divide="ignore"):
        lr = np.log(px[1:] / px[:-1])
    out = np.full(px.shape, np.nan)
    num = np.zeros(px.shape[1])
    den = np.zeros(px.shape[1])
    cnt = np.zeros(px.shape[1])
    for t in range(1, px.shape[0]):
        x = lr[t - 1]
        f = np.isfinite(x)
        x2 = np.where(f, x, 0.0) ** 2
        num = np.where(f, lam * num + x2, num)
        den = np.where(f, lam * den + 1.0, den)
        cnt += f
        with np.errstate(invalid="ignore", divide="ignore"):
            out[t] = np.where(cnt >= min_bars, np.sqrt(num / np.maximum(den, 1e-300) * 365), np.nan)
    return out


def roll_max(px: np.ndarray, w: int) -> np.ndarray:
    """Highest known price of the last `w` rows including the current one (fewer at the start);
    NaN where no price is known yet in the window."""
    a = np.where(np.isfinite(px), px, -np.inf)
    pad = np.vstack([np.full((w - 1, px.shape[1]), -np.inf), a])
    m = np.lib.stride_tricks.sliding_window_view(pad, w, 0).max(-1)
    return np.where(np.isfinite(m), m, np.nan)


def zscore(px: np.ndarray, vol: np.ndarray, h: int) -> np.ndarray:
    """The protocol's z(h): log return over h days / (vol x sqrt(h / 365)), clipped to +-5."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.clip(xs.logret(px, h, 0) / (vol * np.sqrt(h / 365)), -5, 5)


def dd_1y(px: np.ndarray, vol: np.ndarray) -> np.ndarray:
    """log(price / highest price of the last 365 days) / vol."""
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.log(px / roll_max(px, 365)) / vol


def breadth_share(r: np.ndarray, universe: np.ndarray, min_coins: int = 30) -> np.ndarray:
    """Per row: share of the universe's coins with a known return `r` that is positive. NaN where
    fewer than `min_coins` are known (the rule then counts the condition as met)."""
    known = universe & np.isfinite(r)
    n = known.sum(1)
    pos = (known & (r > 0)).sum(1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n >= min_coins, pos / np.maximum(n, 1), np.nan)


def stop_cond(dd: np.ndarray, k: float) -> np.ndarray:
    with np.errstate(invalid="ignore"):
        return dd >= -k  # an unknown drawdown is not held (like an unknown trend)


def fade_cond(r: np.ndarray) -> np.ndarray:
    with np.errstate(invalid="ignore"):
        return r > 0


def breadth_cond(share: np.ndarray, n_coins: int) -> np.ndarray:
    """At least half of the book is up; an unknown share counts as met. Same for every coin."""
    ok = ~(share < 0.5)
    return np.broadcast_to(ok[:, None], (len(share), n_coins))


def paper(
    px: np.ndarray, hold: np.ndarray, base: np.ndarray, cost: float = COST
) -> tuple[np.ndarray, np.ndarray]:
    """Per-coin paper series. `hold[k]` (0/1 per coin) is set at the close of day `base[k]` and
    earns the returns of the days after it until the next set day. Returns (daily simple returns
    after costs, the position earning each day's return). A missing price earns nothing: a coin
    whose price stops is carried at its last price."""
    n_days = px.shape[0]
    filled = xs.ffill(px)
    r = np.zeros_like(filled)
    with np.errstate(invalid="ignore", divide="ignore"):
        r[1:] = filled[1:] / filled[:-1] - 1
    r[~np.isfinite(r)] = 0.0
    pos = np.zeros(px.shape)
    for k, b in enumerate(base):
        end = base[k + 1] + 1 if k + 1 < len(base) else n_days
        pos[b + 1 : end] = hold[k]
    out = pos * r
    prev = np.zeros(px.shape[1])
    for k, b in enumerate(base):
        chg = np.abs(hold[k] - prev)
        out[b] = (1 + out[b]) * (1 - cost * chg) - 1
        prev = hold[k].astype(float)
    return out, pos


def in_force(flag: np.ndarray, base: np.ndarray, n_days: int) -> np.ndarray:
    """Spread a per-decision flag `[decisions, coins]` over the days each decision is in force
    (the days after its set day up to the next set day)."""
    out = np.zeros((n_days, flag.shape[1]), dtype=flag.dtype)
    for k, b in enumerate(base):
        end = base[k + 1] + 1 if k + 1 < len(base) else n_days
        out[b + 1 : end] = flag[k]
    return out


def coin_days(universe_k: np.ndarray, base: np.ndarray, n_days: int) -> np.ndarray:
    """The coin-days a pooled score counts: the days a coin was in the universe at the decision
    in force, plus the day on either side (where the entry and exit costs fall)."""
    u = in_force(universe_k.astype(bool), base, n_days)
    m = u.copy()
    m[1:] |= u[:-1]
    m[:-1] |= u[1:]
    return m


def pooled_sharpe(ret: np.ndarray, mask: np.ndarray) -> float:
    x = ret[mask]
    sd = x.std()
    return float(x.mean() / sd * np.sqrt(365)) if sd > 0 else 0.0


def _date_moments(ret: np.ndarray, mask: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    x = np.where(mask, ret, 0.0)
    return mask.sum(1).astype(float), x.sum(1), (x * x).sum(1)


def _sharpe_from(n: np.ndarray, s: np.ndarray, q: np.ndarray) -> np.ndarray:
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = s / n
        var = q / n - mean**2
        return np.where(var > 0, mean / np.sqrt(var) * np.sqrt(365), 0.0)


def pooled_boot(
    a: np.ndarray,
    b: np.ndarray,
    mask: np.ndarray,
    draws: int = 2000,
    mean_block: float = 20,
    seed: int = 0,
) -> tuple[float, float, float, float]:
    """Pooled single-coin Sharpe of `a` minus `b` with a stationary bootstrap over dates (all
    coins of a drawn date together). Returns (difference, one-sided p, 5%, 95%)."""
    rows = np.flatnonzero(mask.any(1))
    ma = [m[rows] for m in _date_moments(a, mask)]
    mb = [m[rows] for m in _date_moments(b, mask)]
    rng = np.random.default_rng(seed)
    diffs = np.empty(draws)
    for k in range(draws):
        i = stats._stationary_indices(len(rows), mean_block, rng)
        sa = _sharpe_from(ma[0][i].sum(), ma[1][i].sum(), ma[2][i].sum())
        sb = _sharpe_from(mb[0][i].sum(), mb[1][i].sum(), mb[2][i].sum())
        diffs[k] = sa - sb
    d = pooled_sharpe(a, mask) - pooled_sharpe(b, mask)
    lo, hi = float(np.quantile(diffs, 0.05)), float(np.quantile(diffs, 0.95))
    return d, float((diffs <= 0).mean()), lo, hi


def choose(scores: list[float]) -> tuple[int, list[float]]:
    """The card's choice: the grid value whose score, averaged with its grid neighbours', is
    highest; a tie goes to the looser setting (the later grid value). Returns (index, smoothed)."""
    n = len(scores)
    sm = [float(np.mean(scores[max(i - 1, 0) : min(i + 2, n)])) for i in range(n)]
    best = max(range(n), key=lambda i: (round(sm[i], 9), i))
    return best, sm


def auc(x: np.ndarray, y: np.ndarray) -> float:
    """Chance that a labelled row (y true) has a higher x than an unlabelled one; ties count
    half. NaN if either group is empty."""
    n1 = int(y.sum())
    n0 = len(y) - n1
    if n1 == 0 or n0 == 0:
        return float("nan")
    _, inv, counts = np.unique(x, return_inverse=True, return_counts=True)
    upper = np.cumsum(counts)
    rank = (upper - counts + (counts + 1) / 2)[inv]
    return float((rank[y].sum() - n1 * (n1 + 1) / 2) / (n1 * n0))
