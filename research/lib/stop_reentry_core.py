"""stop-reentry core: the weekly coin stop with a cool-off after a stop-out and a reset reference
high (card: research/cards/coin-cap.md, "Sixth reading"). Pure numpy, no harness import, so the
tests can load it alone. Rows are calendar days, as in `cointop1_core`.

`stop-cool-13`, per coin, on each Friday decision:

1. Stop-out: held at the previous decision, the twin holds now, and the stop condition is known
   and fails. Out, and a cool-off starts.
2. Cool-off: out for the decisions of the next `COOL_DAYS - 1` days (13 Friday decisions in
   all, the stop-out's included); the first decision that may hold again is 91 days after the
   stop-out.
3. The stop condition is `log(close / H) / vol >= -k` with `H` the highest close of the last 365
   days not before the latest stop-out decision (its own close counts).
4. Otherwise hold iff the twin holds and the stop condition holds; an unknown vol or high is not
   held and starts no cool-off.
"""

from __future__ import annotations

import math

import numpy as np

COOL_WEEKS = 13
COOL_DAYS = 7 * COOL_WEEKS  # 91: cointop-1's median twin lag (106 d) - the stop's exit day (15 d)
YEAR = 365


def stop_state(
    close_now: float, vol_now: float, hi: float, k: float
) -> tuple[bool, bool]:  # (known, ok)
    """The stop condition from the latest usable close, its vol and the reference high."""
    if not (math.isfinite(close_now) and math.isfinite(vol_now) and math.isfinite(hi)):
        return False, False
    if vol_now <= 0 or hi <= 0 or close_now <= 0:
        return False, False
    return True, math.log(close_now / hi) / vol_now >= -k


def cool_hold(
    pl: np.ndarray,
    vl: np.ndarray,
    d: np.ndarray,
    twin: np.ndarray,
    k: float,
    cool_days: int = COOL_DAYS,
) -> tuple[np.ndarray, np.ndarray]:
    """Hold flags `[len(d), coins]` of `stop-cool` at the decision rows `d`, and a flag per
    decision that is a stop-out. `pl` and `vl` are the price and the 60-day EWMA vol already
    lagged by the book's as-of shift (row t may be used at a decision on day t); `twin` the
    twin's hold at the decisions."""
    n_dec, n_c = twin.shape
    hold = np.zeros((n_dec, n_c), dtype=bool)
    outs = np.zeros((n_dec, n_c), dtype=bool)
    for j in range(n_c):
        prev = False
        s_row = -1  # latest stop-out decision row
        until = -1  # first row that may hold again
        for i, t in enumerate(d):
            t = int(t)
            if t < until:
                prev = False
                continue
            lo = max(t - YEAR + 1, s_row, 0)
            win = pl[lo : t + 1, j]
            win = win[np.isfinite(win)]
            hi = float(win.max()) if len(win) else math.nan
            known, ok = stop_state(float(pl[t, j]), float(vl[t, j]), hi, k)
            if prev and twin[i, j] and known and not ok:
                outs[i, j] = True
                s_row, until = t, t + cool_days
                prev = False
                continue
            prev = bool(twin[i, j] and ok)
            hold[i, j] = prev
    return hold, outs


def reentries(pos: np.ndarray, top: int, hi: int) -> int:
    """Re-entries after the first exit inside a fall's window (coin-cap-4 step 1's count): the
    first row after the top with position 0, then every 0 -> 1 change up to row `hi`."""
    ex = next((t for t in range(top + 1, hi + 1) if pos[t] == 0), -1)
    if ex < 0:
        return 0
    return sum(1 for t in range(max(ex, top + 1), hi + 1) if pos[t] == 1 and pos[t - 1] == 0)


def after_low(r: np.ndarray, low: int, days: int = 182) -> float:
    """Summed daily returns of one slot over the `days` rows after a fall's low (clipped)."""
    return float(r[low + 1 : min(low + 1 + days, len(r))].sum())
