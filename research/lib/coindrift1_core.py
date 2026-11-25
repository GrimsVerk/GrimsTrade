"""Pure-numpy pieces of lane coin-drift-1 (card `research/cards/coin-drift-run.md`).

Everything is a calendar-day matrix `[days, coins]` as in `breadth_xs` and `cointop1_core`. No
harness import here (the harness changes the global asset list), so the tests load this file
alone.

- `simulate`: a coin-only account traded as the gym trades (`gym._execute`): each day the
  target in force is that of the latest set day; a held slot is traded back to its target only
  once it is `k x target x equity` away (the band carried as a share of the slot); entries and
  full exits always trade; buys short of cash sell over-weight slots down to target (audit G2);
  Kraken taker tiers by the coin volume of the 30 days before; slip on the price.
- `shuffle_p1`, `shuffle_p2`: the placebo prices (returns shuffled across coins in 7-day blocks;
  P2 also puts the weeks of the cross-coin mean in a random order).
- `trend_up`: the book's trend condition (365-day log return > 0), lagged one day.
- `sharpes`, `joint_boot`: Sharpe per row and the paired date bootstrap of the real difference
  and of its excess over the mean placebo difference.
"""

from __future__ import annotations

from dataclasses import dataclass

import breadth_xs as xs
import numpy as np

from grimstrade import gym
from grimstrade.data import CRYPTO

COIN = gym.COSTS[CRYPTO]
TIERS = np.array([t[0] for t in COIN.tiers])
RATES = np.array([t[1] for t in COIN.tiers])
WINDOW = 30  # days of fills that set the fee tier (gym.VOLUME_WINDOW)
BLOCK = 7


def fee_at(volume: float) -> float:
    """Kraken taker fee for a 30-day coin volume (gym.Costs.fee_at)."""
    i = int(np.searchsorted(TIERS, volume, side="right")) - 1
    return float(RATES[i]) if i >= 0 else COIN.fee


@dataclass
class Account:
    rets: np.ndarray  # daily account returns, rows first + 1 .. end
    rf: np.ndarray  # what a dollar of cash earned on those days
    first: int  # first row (the first set day)
    fills: int  # coin fills that neither open nor close a position (drift trims and top-ups)
    all_fills: int
    fee: float  # total fees paid, as a sum of fee / equity of the day
    slip: float  # slip paid, the same way
    volume: float  # traded value / equity, summed
    coin_share: float  # mean share of equity in coins on days a coin is held


def simulate(
    px: np.ndarray,
    targets: np.ndarray,
    base: np.ndarray,
    k: float,
    costs: bool = True,
    rate: np.ndarray | None = None,
    start_cash: float = gym.START_CASH,
) -> Account:
    """Daily account from the first set day `base[0]`. `targets[j]` is in force from row
    `base[j]` to the day before `base[j + 1]`; trades happen at the price stamped on the day.
    `rate[t]` is the annual cash rate of day `t` (0 if None). A missing price: no trade, valued
    at the last price; a held coin whose target is 0 is then sold at that last price."""
    n_days, n = px.shape
    filled = xs.ffill(px)
    filled = np.where(np.isfinite(filled), filled, 0.0)
    known = np.isfinite(px)
    slip = COIN.slip if costs else 0.0
    rate_d = np.zeros(n_days) if rate is None else rate / gym.DAYS_PER_YEAR
    first = int(base[0])
    which = np.searchsorted(base, np.arange(n_days), side="right") - 1
    q = np.zeros(n)
    cash = start_cash
    eq = np.zeros(n_days)
    vol_day = np.zeros(n_days)
    fills = all_fills = 0
    fee_sum = slip_sum = vol_sum = 0.0
    shares = []
    for t in range(first, n_days):
        p = filled[t]
        w = targets[which[t]]
        e = cash + float(q @ p)
        held = q > 0
        delta = w * e - q * p
        full_exit = (w == 0) & held
        tradable = known[t] & (p > 0)
        entry = (w > 0) & ~held & tradable
        outside = (w > 0) & tradable & (np.abs(delta) >= k * w * e)
        buy_need = float(delta[(entry | outside) & (delta > 0)].sum())
        funding = (buy_need > cash) & tradable & (delta < -1e-9 * e) & held
        trade = full_exit | entry | outside | funding
        fee = fee_at(float(vol_day[max(t - WINDOW + 1, 0) : t].sum())) if costs else 0.0
        sells = np.flatnonzero(trade & (delta < 0))
        traded = 0.0
        for j in sells:
            pj = p[j] * (1 - slip)
            qty = q[j] if full_exit[j] else min(-delta[j] / p[j], q[j])
            value = qty * pj
            cash += value * (1 - fee)
            q[j] -= qty
            traded += value
            fee_sum += value * fee / e
            slip_sum += qty * p[j] * slip / e
            all_fills += 1
            fills += int(not full_exit[j])
        buys = np.flatnonzero(trade & (delta > 0))
        if len(buys):
            buys = buys[np.argsort(delta[buys], kind="stable")]  # smaller buys first (gym)
            pb = p[buys] * (1 + slip)
            wanted = delta[buys] / p[buys] * pb * (1 + fee)
            before = np.cumsum(wanted) - wanted
            spend = np.clip(cash - before, 0.0, wanted)
            qty = spend / (pb * (1 + fee))
            ok = qty > 0
            cash -= float(spend.sum())
            was_held = held[buys]
            q[buys] += qty
            traded += float((qty * pb).sum())
            fee_sum += float((qty * pb * fee).sum()) / e
            slip_sum += float((qty * p[buys] * slip).sum()) / e
            all_fills += int(ok.sum())
            fills += int((ok & was_held).sum())
        vol_day[t] = traded
        vol_sum += traded / e if e > 0 else 0.0
        cash += cash * rate_d[t]
        eq[t] = cash + float(q @ p)
        coin = float(q @ p)
        if coin > 1e-9 * eq[t]:
            shares.append(coin / eq[t])
    rets = eq[first + 1 :] / eq[first:-1] - 1
    return Account(
        rets, rate_d[first + 1 :], first, fills, all_fills, fee_sum, slip_sum, vol_sum,
        float(np.mean(shares)) if shares else float("nan"),
    )  # fmt: skip


def trend_up(px: np.ndarray, shift: int = 1) -> np.ndarray:
    """The book's twin condition: 365-day log return above zero, usable `shift` days later."""
    with np.errstate(invalid="ignore"):
        up = xs.logret(px, 365, 0) > 0
    return xs.lag(up.astype(float), shift) == 1


def _logret_rows(px: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(log of the carried price, its daily change; 0 where unknown)."""
    filled = xs.ffill(px)
    with np.errstate(invalid="ignore", divide="ignore"):
        lp = np.log(filled)
    x = np.zeros_like(lp)
    x[1:] = lp[1:] - lp[:-1]
    x[~np.isfinite(x)] = 0.0
    return lp, x


def _blocks(px: np.ndarray, elig: np.ndarray, cols: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """(first row, shufflable coins) per 7-day block: coins of `cols` with a known price on
    every day of the block and the day before, eligible on the block's first day."""
    known = np.isfinite(px)
    out = []
    for s in range(1, px.shape[0] - BLOCK + 1, BLOCK):
        ok = cols & elig[s] & known[s - 1 : s + BLOCK].all(0)
        out.append((s, np.flatnonzero(ok)))
    return out


def _rebuild(px: np.ndarray, lp: np.ndarray, x: np.ndarray) -> np.ndarray:
    """Prices from (shuffled) daily log changes: each coin keeps its first price and its missing
    days."""
    known = np.isfinite(px)
    first = np.where(known.any(0), known.argmax(0), px.shape[0])
    rows = np.arange(px.shape[0])[:, None]
    x = np.where(rows > first[None, :], x, 0.0)
    start = lp[np.minimum(first, px.shape[0] - 1), np.arange(px.shape[1])]
    out = np.exp(start[None, :] + np.cumsum(x, axis=0))
    return np.where(known, out, np.nan)


def shuffle_p1(px: np.ndarray, elig: np.ndarray, cols: np.ndarray, seed: int) -> np.ndarray:
    """P1: in each 7-day block, one random permutation of the shufflable coins' daily returns."""
    rng = np.random.default_rng(seed)
    lp, x = _logret_rows(px)
    y = x.copy()
    for s, S in _blocks(px, elig, cols):
        if len(S) >= 2:
            y[s : s + BLOCK, S] = x[s : s + BLOCK, S[rng.permutation(len(S))]]
    return _rebuild(px, lp, y)


def shuffle_p2(px: np.ndarray, elig: np.ndarray, cols: np.ndarray, seed: int) -> np.ndarray:
    """P2: P1 on the returns net of the day's cross-coin mean, and the weeks of that mean put in
    a random order (a week's seven days stay together)."""
    rng = np.random.default_rng(seed)
    lp, x = _logret_rows(px)
    y = x.copy()
    blocks = [(s, S) for s, S in _blocks(px, elig, cols) if len(S) >= 2]
    means = [x[s : s + BLOCK, S].mean(1) for s, S in blocks]
    order = rng.permutation(len(blocks))
    for i, ((s, S), src) in enumerate(zip(blocks, order, strict=True)):
        e = x[s : s + BLOCK, S] - means[i][:, None]
        y[s : s + BLOCK, S] = means[src][:, None] + e[:, rng.permutation(len(S))]
    return _rebuild(px, lp, y)


def sharpes(r: np.ndarray) -> np.ndarray:
    """Annualised Sharpe (365 days) of each row of `r` (or of a 1-d series)."""
    r = np.atleast_2d(r)
    sd = r.std(axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(sd > 0, r.mean(axis=-1) / sd * np.sqrt(365), 0.0)


def joint_boot(
    a: np.ndarray,
    b: np.ndarray,
    pa: np.ndarray | None = None,
    pb: np.ndarray | None = None,
    draws: int = 2000,
    mean_block: float = 20,
    seed: int = 0,
) -> dict[str, float]:
    """Paired stationary bootstrap over dates. d = Sharpe(a) - Sharpe(b); with placebo pairs
    `pa`, `pb` (`[shuffles, days]`) also the excess d - mean(Sharpe(pa) - Sharpe(pb)), every
    series resampled on the same dates."""
    import stats  # research/lib/stats.py (no harness import)

    rng = np.random.default_rng(seed)
    d0 = float(sharpes(a)[0] - sharpes(b)[0])
    out = {"d": d0}
    have = pa is not None and pb is not None
    if have:
        assert pa is not None and pb is not None
        dp = sharpes(pa) - sharpes(pb)
        out["excess"] = d0 - float(dp.mean())
    dd = np.empty(draws)
    ex = np.empty(draws)
    for i in range(draws):
        idx = stats._stationary_indices(len(a), mean_block, rng)
        dd[i] = sharpes(a[idx])[0] - sharpes(b[idx])[0]
        if have:
            assert pa is not None and pb is not None
            ex[i] = dd[i] - float((sharpes(pa[:, idx]) - sharpes(pb[:, idx])).mean())
    out["se"] = float(dd.std())
    out["z"] = d0 / out["se"] if out["se"] > 0 else float("nan")
    out["p"] = float((dd <= 0).mean())
    if have:
        out["ex_se"] = float(ex.std())
        out["ex_z"] = out["excess"] / out["ex_se"] if out["ex_se"] > 0 else float("nan")
    return out
