"""coin-cap-3 core: the coin stop read every day instead of on Fridays (card:
research/cards/coin-cap.md, "Fourth reading"). Pure numpy, no harness import, so the tests can
load it alone. Rows are calendar days, as in `cointop1_core`.

- `daily_hold`: the two daily variants from the weekly twin and a daily stop condition.
- `stop_ok`: the stop condition per row, lagged by the book's as-of shift.
- `switches`, `short_round_trips`, `deepest_fall_span`: turnover and the BTC mechanism note.
"""

from __future__ import annotations

import breadth_xs as xs
import cointop1_core as core
import numpy as np

MODES = ("d", "dx")  # daily check; daily exit with Friday re-entry
SHORT_TRIP = 7  # out and back in within this many days counts as a short round trip


def stop_ok(px: np.ndarray, shift: int, k: float) -> np.ndarray:
    """cointop-1's stop condition `dd_1y >= -k` per row, from values stamped `shift` rows earlier
    or before (row t of the result may be used at a decision on day t)."""
    dd = xs.lag(core.dd_1y(px, core.ewma_vol(px, 60)), shift)
    return np.asarray(core.stop_cond(dd, k))


def daily_hold(
    week_d: np.ndarray,
    week_hold: np.ndarray,
    day_d: np.ndarray,
    ok: np.ndarray,
    mode: str,
) -> np.ndarray:
    """Hold flags `[len(day_d), coins]` for daily decisions on rows `day_d` (consecutive calendar
    days). `week_hold` is the weekly twin's hold at the Friday rows `week_d`; `ok` the stop
    condition per row.

    - `d`: hold iff the latest twin decision at or before the day holds and `ok` holds that day.
    - `dx`: as `d`, but once `ok` fails on a day after the Friday decision in force, out until the
      next Friday decision (re-entry only on Fridays).

    On a Friday both equal the weekly stop (`week_hold & ok[friday]`)."""
    if mode not in MODES:
        raise ValueError(mode)
    w_of = np.searchsorted(week_d, day_d, side="right") - 1
    out = np.zeros((len(day_d), week_hold.shape[1]), dtype=bool)
    run = np.ones(week_hold.shape[1], dtype=bool)
    prev_w = -1
    for k, t in enumerate(day_d):
        w = int(w_of[k])
        if w < 0:
            continue
        if w != prev_w:
            run = np.ones(week_hold.shape[1], dtype=bool)
            prev_w = w
        run = run & ok[t] if mode == "dx" else ok[t]
        out[k] = week_hold[w] & run
    return out


def switches(pos: np.ndarray) -> np.ndarray:
    """Rows at which each coin's position differs from the row before (bool `[days, coins]`)."""
    out = np.zeros(pos.shape, dtype=bool)
    out[1:] = pos[1:] != pos[:-1]
    return out


def short_round_trips(pos: np.ndarray, px: np.ndarray, gap: int = SHORT_TRIP) -> list[float]:
    """For one coin: every exit (1 -> 0) followed by a re-entry (0 -> 1) within `gap` days, as
    the price at re-entry over the price at exit, minus 1 (positive: bought back higher)."""
    out: list[float] = []
    exit_row = -1
    for t in range(1, len(pos)):
        if pos[t - 1] == 1 and pos[t] == 0:
            exit_row = t
        elif pos[t - 1] == 0 and pos[t] == 1 and exit_row >= 0:
            if t - exit_row <= gap:
                out.append(float(px[t - 1] / px[exit_row - 1] - 1))
            exit_row = -1
    return out


def deepest_fall_span(r: np.ndarray) -> tuple[float, int, int]:
    """`coin_cap2_core.deepest_fall` with where it happens: (depth, peak, trough) as indices into
    the P&L path (0 = before the first return, i = after the i-th return)."""
    path = np.concatenate([[0.0], np.cumsum(r)])
    dd = np.maximum.accumulate(path) - path
    trough = int(dd.argmax())
    peak = int(path[: trough + 1].argmax())
    return float(dd[trough]), peak, trough
