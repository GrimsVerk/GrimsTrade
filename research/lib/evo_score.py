"""The fast scorer of evo-1 (research/evo-1.md, "Scoring"): the daily returns of a weekly rule
from its Friday weight matrix, without the gym's event loop.

A `Book` is one asset set over one span of decisions. It mirrors what `gym.simulate` does with
the decisions of a weekly research strategy (`common.weekly`, `harness.decisions`):

- A decision is made every calendar day from `start` at 22:30 UTC and repeats the weights of
  the Friday `common.weekly` maps it to (the Friday on or before the decision's `View.today`).
- Each asset fills at its next open: the target in force for a bar opening on day `d` is the
  one decided on day `d - 1` (crypto opens at 00:00 UTC, ETFs at 13:30 UTC, both after the
  22:30 decision of the day before). The overnight part of a bar (previous close to open) is
  held at the target of the previous bar's fill, the open-to-close part at the new target.
- Costs (fee + slippage) are charged on the fill day on the change of target weight.
- Cash-limited coin buys: after a change of targets, coins fill (Saturday 00:00) before the
  ETFs are sold (Monday 13:30), so a coin buy can only use the cash there is. Until the first
  ETF open after the change, each coin holds what it had (cut to its new target if that is
  lower) plus its share of the free cash, smallest buy first (the gym's order); from the next
  coin open on, the full target. Without this, a `full` rule that rotates from ETFs into coins
  every weekend scores up to ~0.1 Sharpe better here than in the gym.
- Both parts of a bar dated `d` land on calendar day `d` (the gym's end-of-day equity); days
  without a bar return 0, so the Sharpe uses every calendar day like `harness`.

What it ignores: the 1% rebalance band, the drift of weights between fills and the trades the
gym makes to pull drifted weights back to target, compounding inside a day.
`tests/test_evo_score.py` states and checks the tolerance against `gym.simulate`.
"""

from __future__ import annotations

import bisect
import math
from collections.abc import Sequence
from datetime import date, timedelta

import numpy as np
from harness import Panel, decide_time

from grimstrade.data import CRYPTO, UNIVERSE
from grimstrade.gym import COSTS, Costs


def fridays_between(first: date, last: date) -> list[date]:
    """Every Friday from the one on or before `first` to the one on or before `last`."""
    d = _friday_of(first)
    out = []
    while d <= last:
        out.append(d)
        d += timedelta(days=7)
    return out


def _friday_of(d: date) -> date:
    return d - timedelta(days=(d.weekday() - 4) % 7)


class Book:
    """Index arrays that turn a (Fridays x assets) weight matrix into daily returns.

    `fridays` must be the rows of the weight matrix (`evo_feat.friday_feats(panel, fridays)`)
    and cover every Friday a decision in `[start, end]` maps to. Decisions stop at `end`; the
    last target is held to the last bar, as in the gym.

    Flat layout of the weights an evaluation gathers from: the coins' cash-limited weights
    after each change of targets (`n_changes` x assets), then a zero row (nothing decided yet),
    then the Friday rows.
    """

    def __init__(
        self,
        panel: Panel,
        fridays: Sequence[date],
        start: date,
        end: date,
        costs: dict[str, Costs] = COSTS,
    ) -> None:
        self.syms = list(panel.syms)
        self.fridays = list(fridays)
        self.start, self.end = start, end
        a_n = self.a_n = len(self.syms)
        self.coin = np.array([UNIVERSE[s] == CRYPTO for s in self.syms])
        row_of = {f: i for i, f in enumerate(self.fridays)}

        # Decision row per decision day, from View.today as `common.weekly` sees it.
        times = {s: panel.close_times[s] for s in self.syms}
        n_dec = (end - start).days + 1
        dec_row = np.full(n_dec, -1, dtype=np.int64)
        for k in range(n_dec):
            t = decide_time(start + timedelta(days=k))
            last = [times[s][i - 1] for s in self.syms if (i := bisect.bisect_right(times[s], t))]
            if not last:
                continue
            f = _friday_of(max(last).date())
            if f not in row_of:
                if f < self.fridays[0]:
                    continue
                raise ValueError(f"{f}: Friday missing from the weight rows")
            dec_row[k] = row_of[f]
        self.dec_row = dec_row
        used = dec_row[dec_row >= 0]
        self.rows_used = (int(used.min()), int(used.max())) if len(used) else (0, -1)

        # Changes of target: decision day index, row before (-1: none), row after.
        prev = np.concatenate([[-1], dec_row[:-1]])
        ch = np.flatnonzero((dec_row != prev) & (dec_row >= 0))
        self.ch_k = ch
        self.ch_prev = prev[ch]
        self.ch_new = dec_row[ch]
        n_ch = self.n_ch = len(ch)
        self.base = n_ch * a_n + a_n  # offset of Friday row 0 in the flat layout
        # First ETF bar date after each change (coins are cash-limited until that ETF open).
        etf_days = np.unique(
            np.concatenate(
                [panel.ord[s] for j, s in enumerate(self.syms) if not self.coin[j]]
                or [np.array([], dtype=np.int64)]
            )
        )
        start_ord = start.toordinal()
        ch_ord = start_ord + ch
        nxt = np.searchsorted(etf_days, ch_ord, side="right")
        far = np.iinfo(np.int64).max
        self.ch_etf_open = np.where(
            nxt < len(etf_days), etf_days[np.minimum(nxt, len(etf_days) - 1)], far
        )

        def slot(day: date, j: int) -> int:
            """Flat index of the weight held by asset j from its fill at the open on `day`."""
            k = (day - start).days - 1  # the decision before that open
            if k < 0:
                return n_ch * a_n + j  # the zero row
            k = min(k, n_dec - 1)
            row = int(dec_row[k])
            if self.coin[j] and n_ch:
                e = int(np.searchsorted(ch, k, side="right")) - 1
                if e >= 0 and day.toordinal() <= self.ch_etf_open[e]:
                    return e * a_n + j  # cash-limited after change e
            return self.base + row * a_n + j if row >= 0 else n_ch * a_n + j

        last_day = max(
            (date.fromordinal(int(panel.ord[s][-1])) for s in self.syms if len(panel.ord[s])),
            default=start,
        )
        self.first_day = start + timedelta(days=1)
        self.days = (last_day - self.first_day).days + 1  # calendar days with a return
        day_k, flat_o, flat_i, r_o, r_i, cost = [], [], [], [], [], []
        for j, s in enumerate(self.syms):
            ords, o, c = panel.ord[s], panel.o[s], panel.c[s]
            cs = costs[UNIVERSE[s]]
            for b in range(1, len(ords)):
                d = date.fromordinal(int(ords[b]))
                if d < self.first_day:
                    continue
                day_k.append((d - self.first_day).days)
                flat_o.append(slot(date.fromordinal(int(ords[b - 1])), j))
                flat_i.append(slot(d, j))
                r_o.append(o[b] / c[b - 1] - 1)
                r_i.append(c[b] / o[b] - 1)
                cost.append(cs.fee + cs.slip)
        order = np.argsort(np.array(day_k, dtype=np.int64), kind="stable")
        self.day_k = np.array(day_k, dtype=np.int64)[order]
        self.flat_o = np.array(flat_o, dtype=np.int64)[order]
        self.flat_i = np.array(flat_i, dtype=np.int64)[order]
        self.r_o = np.array(r_o)[order]
        self.r_i = np.array(r_i)[order]
        self.cost = np.array(cost)[order]

    def day_index(self, d: date) -> int:
        """Number of return days strictly before calendar day `d`."""
        return min(max((d - self.first_day).days, 0), self.days)

    def date_of(self, k: int) -> date:
        return self.first_day + timedelta(days=k)

    def _flat(self, w: np.ndarray, n_ch: int) -> np.ndarray:
        """The flat weights: cash-limited coin weights of the first `n_ch` changes, zero row,
        Friday rows."""
        a_n = self.a_n
        out = np.zeros(self.base + w.shape[0] * a_n)
        out[self.base :] = w.ravel()
        if n_ch and self.coin.any():
            wz = np.vstack([np.zeros(a_n), w])
            p, n = wz[self.ch_prev[:n_ch] + 1], wz[self.ch_new[:n_ch] + 1]
            cn = self.coin
            pc, nc = p[:, cn], n[:, cn]
            held = np.minimum(pc, nc)  # sells happen first
            cash = np.maximum(1.0 - p[:, ~cn].sum(axis=1) - held.sum(axis=1), 0.0)
            want = nc - held
            idx = np.argsort(want, axis=1, kind="stable")
            ws = np.take_along_axis(want, idx, axis=1)
            before = np.cumsum(ws, axis=1) - ws
            got = np.clip(cash[:, None] - before, 0.0, ws)
            alloc = np.empty_like(got)
            np.put_along_axis(alloc, idx, got, axis=1)
            eff = np.zeros((n_ch, a_n))
            eff[:, cn] = held + alloc
            out[: n_ch * a_n] = eff.ravel()
        return out

    def daily(self, w: np.ndarray, before: date | None = None) -> np.ndarray:
        """Daily returns after costs on the calendar days from `start + 1` to the last bar (or
        to the day before `before`). `w` has one row per Friday (at least up to the last row a
        kept day uses), one column per asset."""
        k_n = self.days if before is None else self.day_index(before)
        e = int(np.searchsorted(self.day_k, k_n, side="left"))
        n_ch = self.n_ch
        if before is not None:
            n_ch = int(np.searchsorted(self.ch_k, (before - self.start).days - 1, side="left"))
        wp = self._flat(w, n_ch)
        fo, fi = self.flat_o[:e], self.flat_i[:e]
        wo, wi = wp[fo], wp[fi]
        contrib = wo * self.r_o[:e] + wi * self.r_i[:e] - self.cost[:e] * np.abs(wi - wo)
        out: np.ndarray = np.bincount(self.day_k[:e], weights=contrib, minlength=k_n)
        return out

    def invested(self, w: np.ndarray, before: date | None = None) -> tuple[float, int]:
        """(sum of the row totals, number of rows) over the Friday rows the decisions in the
        window use: the card's invested share is the ratio, pooled over books."""
        a, b = self.rows_used
        if before is not None:
            k = (before - self.start).days  # decisions on days < before
            used = self.dec_row[: max(k, 0)]
            used = used[used >= 0]
            if not len(used):
                return 0.0, 0
            a, b = int(used.min()), int(used.max())
        if b < a:
            return 0.0, 0
        return float(w[a : b + 1].sum()), b - a + 1


def sharpe_of(parts: Sequence[np.ndarray]) -> float:
    """Sharpe (365 days, zero rate, population sd: `stats.sharpe`) of the concatenated series,
    without building it."""
    n = sum(len(p) for p in parts)
    if n == 0:
        return 0.0
    s1 = sum(float(p.sum()) for p in parts)
    s2 = sum(float((p * p).sum()) for p in parts)
    m = s1 / n
    var = s2 / n - m * m
    return m / math.sqrt(var) * math.sqrt(365) if var > 1e-30 else 0.0
