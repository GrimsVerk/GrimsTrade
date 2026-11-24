"""breadth-book-1: the mechanical universe rules and the statistics, without the harness (the
harness changes the global asset list on import, so tests import only this file).

Card: `research/cards/breadth-book-1.md`. Every rule here reads only data dated on or before
its cut-off (2006-12-31 for the ETF pool, 2019-12-31 for the coin list, the month end for the
effective number of bets); the tests change later data and check nothing moves.
"""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from datetime import date, timedelta

import numpy as np

# ---------------------------------------------------------------- ETF pool (card: fixed lists)

LIVE_ETFS = ["SPY", "QQQ", "GLD", "TLT"]
LIVE_COINS = ["BTC", "ETH"]
SIX = LIVE_ETFS + LIVE_COINS

CLASSES: dict[str, list[str]] = {
    "us-equity": ["SPY", "QQQ", "IWM", "VNQ",
                  "XLK", "XLF", "XLE", "XLV", "XLY", "XLP", "XLI", "XLB", "XLU"],
    "bonds": ["TLT", "IEF", "LQD", "SHY", "IEI"],
    "commodities": ["GLD", "SLV", "DBC", "PPLT", "PALL", "CPER", "DBB", "USO", "BNO", "UGA",
                    "UNG", "CORN", "WEAT", "SOYB", "CANE", "DBA"],
    "intl-equity": ["EFA", "EEM", "EWA", "EWG", "EWP", "EWQ", "EWI", "EWJ", "EWN", "EWU"],
    "currencies": ["FXE", "FXY", "FXB", "FXA", "FXC", "FXF"],
}  # fmt: skip
CLASS_ORDER = ["us-equity", "bonds", "commodities", "intl-equity", "currencies"]
POOL = [s for c in CLASS_ORDER for s in CLASSES[c]]

FIRST_BAR_BY = date(2006, 7, 3)
LIQ_FROM, LIQ_TO = date(2006, 7, 1), date(2006, 12, 31)
MIN_DOLLAR_VOLUME = 1_000_000.0

# A raw daily bar for the pool rule: (date, close, volume), split-adjusted, not dividend-adjusted.
RawBar = tuple[date, float, float]


def dollar_volume_2006(bars: Sequence[RawBar]) -> float | None:
    """Median daily dollar volume over 2006-H2, or None if the ETF is not eligible (first bar
    after 2006-07-03). Reads no bar after 2006-12-31."""
    seen = [b for b in bars if b[0] <= LIQ_TO]
    if not seen or seen[0][0] > FIRST_BAR_BY:
        return None
    dv = [c * v for d, c, v in seen if d >= LIQ_FROM]
    return float(np.median(dv)) if dv else None


def eligible_pool(raw: Mapping[str, Sequence[RawBar]]) -> dict[str, float]:
    """ETF -> 2006-H2 median dollar volume, for the pool ETFs that pass both rules."""
    out = {}
    for s in POOL:
        dv = dollar_volume_2006(raw.get(s, []))
        if dv is not None and dv >= MIN_DOLLAR_VOLUME:
            out[s] = dv
    return out


def class_of(s: str) -> str:
    return next(c for c in CLASS_ORDER if s in CLASSES[c])


def round_robin(dv: Mapping[str, float]) -> list[str]:
    """Card order: round-robin over CLASS_ORDER, inside a class by dollar volume (largest first;
    ties by ticker); a class that runs out is skipped."""
    queues = [sorted((s for s in dv if class_of(s) == c), key=lambda s: (-dv[s], s))
              for c in CLASS_ORDER]  # fmt: skip
    out: list[str] = []
    while any(queues):
        for q in queues:
            if q:
                out.append(q.pop(0))
    return out


def by_volume(dv: Mapping[str, float]) -> list[str]:
    return sorted(dv, key=lambda s: (-dv[s], s))


def nested(order: Sequence[str], n: int, base: Sequence[str] = ()) -> list[str]:
    """`base`, then the ordered assets not already in it, up to n assets (all if n is larger)."""
    out = list(base)
    for s in order:
        if len(out) >= n:
            break
        if s not in out:
            out.append(s)
    return out


# ---------------------------------------------------------------- coin list (2019-12-31 caps)

COIN_ASOF = date(2019, 12, 31)
COIN_YEAR_FROM = date(2019, 1, 1)


def coin_list(
    px: Mapping[str, Mapping[date, float]],
    cap: Mapping[str, Mapping[date, float]],
    k: int,
    asof: date = COIN_ASOF,
) -> list[str]:
    """The k largest coins by 30-day median market cap ending `asof`, among coins with a price on
    every day of the year to `asof`, not stablecoins (90-day vol >= 20%), not wrappers (90-day
    correlation of daily returns with btc or eth < 0.95, btc and eth kept). Reads nothing after
    `asof`. Names are Coin Metrics asset ids (lower case)."""
    year = [COIN_YEAR_FROM + timedelta(i) for i in range((asof - COIN_YEAR_FROM).days + 1)]
    last90 = year[-91:]

    def rets(a: str) -> np.ndarray:
        p = np.array([px[a][d] for d in last90])
        return np.asarray(np.diff(np.log(p)))

    ok: dict[str, float] = {}
    for a in px:
        p = px[a]
        if not all(d in p and p[d] > 0 for d in year):
            continue
        r = rets(a)
        if r.std() * math.sqrt(365) < 0.20:
            continue
        if a not in ("btc", "eth"):
            refs = [rets(b) for b in ("btc", "eth") if b in px]
            if any(np.corrcoef(r, x)[0, 1] >= 0.95 for x in refs):
                continue
        caps = [cap.get(a, {}).get(d) for d in year[-30:]]
        vals = [c for c in caps if c is not None and c > 0]
        if vals:
            ok[a] = float(np.median(vals))
    return sorted(ok, key=lambda a: (-ok[a], a))[:k]


# ---------------------------------------------------------------- effective number of bets


def participation(corr: np.ndarray) -> float:
    """(sum of eigenvalues)^2 / sum of squared eigenvalues of a correlation matrix: 1 for
    identical series, n for n independent ones."""
    lam = np.linalg.eigvalsh(corr)
    lam = np.clip(lam, 0, None)
    return float(lam.sum() ** 2 / (lam**2).sum())


def mean_offdiag(corr: np.ndarray) -> float:
    n = len(corr)
    return float((corr.sum() - n) / (n * (n - 1))) if n > 1 else math.nan


def neff_at(
    weekly_lr: np.ndarray, row: int, cols: Sequence[int], window: int = 104
) -> tuple[float, float]:
    """(participation ratio, mean pairwise correlation) of the `cols` series over the `window`
    weekly log returns ending at `row` (inclusive). Columns with a gap in the window are
    dropped. Reads no row after `row`."""
    if row + 1 < window:
        return math.nan, math.nan
    x = weekly_lr[row + 1 - window : row + 1][:, list(cols)]
    keep = [j for j in range(x.shape[1]) if np.isfinite(x[:, j]).all() and x[:, j].std() > 0]
    if len(keep) < 2:
        return (1.0 if keep else math.nan), math.nan
    c = np.corrcoef(x[:, keep], rowvar=False)
    return participation(c), mean_offdiag(c)


# ---------------------------------------------------------------- paired Sharpe difference


def sharpe(r: np.ndarray) -> float:
    sd = r.std()
    return float(r.mean() / sd * math.sqrt(365)) if sd > 0 else 0.0


def _stationary(n: int, mean_block: float, rng: np.random.Generator) -> np.ndarray:
    restart = rng.random(n) < 1 / mean_block
    restart[0] = True
    pos = np.arange(n)
    last = np.maximum.accumulate(np.where(restart, pos, 0))
    starts = rng.integers(n, size=n)
    out: np.ndarray = (starts[last] + pos - last) % n
    return out


def paired(
    a: np.ndarray, b: np.ndarray, draws: int = 2000, mean_block: float = 20, seed: int = 0
) -> tuple[float, float, float, float]:
    """Sharpe(a) - Sharpe(b) on the same days: (difference, bootstrap SE, z, one-sided p that a
    does not beat b)."""
    if len(a) != len(b):
        raise ValueError("series must cover the same days")
    rng = np.random.default_rng(seed)
    diffs = np.empty(draws)
    for k in range(draws):
        i = _stationary(len(a), mean_block, rng)
        diffs[k] = sharpe(a[i]) - sharpe(b[i])
    d = sharpe(a) - sharpe(b)
    se = float(diffs.std())
    return d, se, (d / se if se > 0 else math.nan), float((diffs <= 0).mean())
