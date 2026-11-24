"""Cross-sectional weekly IC of the volume features in the top-100 coin book (card 2 in
research/volume-1.md). Descriptive only: no backtest.

    uv run python research/lib/volume1_coins.py --log > research/results/volume-1-coins.md

Book: `breadth_books.cm_book()` (the loader cointop-1 uses), train cut. Features:
`volume1_ic.daily_features` with 7 bars a week, a value stamped x used from x + 1. With `--log`
every candidate gets one `screen` row in tries.md (run once).
"""

from __future__ import annotations

import sys
from datetime import UTC, date, datetime, timedelta

import numpy as np

N_SHIFT = 500
MIN_SHIFT = 52
MIN_COINS = 20
START = date(2019, 1, 4)
BAR_IC = 0.03
IDEA = "volume-1-coins-screen"


def row_ranks(x: np.ndarray, m: np.ndarray) -> np.ndarray:
    """Ranks 0..k-1 among the masked entries of each row (ties by column order)."""
    a = np.where(m, x, np.inf)
    return np.argsort(np.argsort(a, axis=1, kind="stable"), axis=1, kind="stable").astype(float)


def xs_ic(sig: np.ndarray, z: np.ndarray, elig: np.ndarray, min_n: int = MIN_COINS) -> np.ndarray:
    """Per row: rank correlation of `sig` and `z` across the columns that are eligible and
    finite in both; NaN with fewer than `min_n` such columns."""
    m = elig & np.isfinite(sig) & np.isfinite(z)
    n = m.sum(1)
    mean = ((n - 1) / 2)[:, None]
    ca = np.where(m, row_ranks(sig, m) - mean, 0.0)
    cb = np.where(m, row_ranks(z, m) - mean, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        ic = (ca * cb).sum(1) / np.sqrt((ca**2).sum(1) * (cb**2).sum(1))
    return np.where(n >= min_n, ic, np.nan)


def main(log: bool) -> None:
    import breadth_books as bb
    import breadth_xs as xs
    import harness
    from volume1_ic import CANDIDATES, daily_features

    book = bb.cm_book()
    vol = bb.cm_panel()["vol"]
    px = book.px
    dec, skip = bb.decisions(book, "weekly", bb.start_day(book))
    dec = dec[dec >= (START - book.day0).days]
    d, b, e = xs.schedule(px.shape[0], dec, skip)
    with np.errstate(all="ignore"):
        lr = np.vstack([np.full((1, px.shape[1]), np.nan), np.log(px[1:] / px[:-1])])
        vol90 = xs.roll_std(lr, 90) * np.sqrt(365)
        v = vol90[d - book.shift]
        z = np.clip(xs.fwd_logret(px, b, e) / (v * np.sqrt(7 / 365)), -5, 5)
        z[~(v > 0)] = np.nan
    elig = book.elig[d]
    r0 = max(int(d[0]) - 400, 0)
    feats = {c: np.full((len(d), px.shape[1]), np.nan) for c in CANDIDATES}
    for j in np.flatnonzero(elig.any(0)):
        f = daily_features(px[r0:, j], vol[r0:, j], 7)
        for c in CANDIDATES:
            feats[c][:, j] = f[c][d - r0 - book.shift]
    years = np.array([(book.day0 + timedelta(days=int(i))).year for i in d])
    shifts = np.random.default_rng(0).integers(MIN_SHIFT, len(d) - MIN_SHIFT, N_SHIFT)
    null = np.full((N_SHIFT, len(CANDIDATES)), np.nan)
    with np.errstate(all="ignore"):
        for a, s in enumerate(shifts):
            for k, c in enumerate(CANDIDATES):
                null[a, k] = abs(np.nanmean(xs_ic(np.roll(feats[c], int(s), 0), z, elig)))
    family = float(np.nanpercentile(np.nanmax(null, axis=1), 95))
    first = book.day0 + timedelta(days=int(d[0]))
    print("# Volume 1, card 2: cross-sectional weekly IC of volume in the top-100 coin book\n")
    print("Script `lib/volume1_coins.py`, card 2 in `research/volume-1.md`. IC = mean over Fridays")
    print(f"({first} to 2025-11-09) of the rank correlation across eligible coins between the")
    print("feature and the coming week's risk-adjusted return. Chance = 95th percentile of |IC|")
    print(
        f"with the feature panel circularly shifted in time ({N_SHIFT} shifts of >= 52 weeks, the"
    )
    print(f"same for all six). **Family chance level (maxT): {family:.3f}.**\n")
    print("| Candidate | Weeks | Coins | IC | t | Weeks > 0 | 2019-21 | 2022-25 | Chance | Family"
          " | Verdict |")  # fmt: skip
    print("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|")
    rows = []
    for k, c in enumerate(CANDIDATES):
        ic = xs_ic(feats[c], z, elig)
        ok = np.isfinite(ic)
        x = ic[ok]
        n = (elig & np.isfinite(feats[c]) & np.isfinite(z)).sum(1)[ok].mean()
        mean = float(x.mean())
        t = float(mean / x.std(ddof=1) * np.sqrt(len(x)))
        e1 = float(ic[ok & (years <= 2021)].mean())
        e2 = float(ic[ok & (years >= 2022)].mean())
        chance = float(np.nanpercentile(null[:, k], 95))
        above = abs(mean) > family
        if above and abs(mean) >= BAR_IC and e1 * e2 > 0:
            verdict = "**useful**"
        elif above:
            verdict = "second look"
        else:
            verdict = "no"
        print(f"| `{c}` | {len(x)} | {n:.0f} | {mean:+.3f} | {t:+.1f} | {(x > 0).mean():.0%} | "
              f"{e1:+.3f} | {e2:+.3f} | {chance:.3f} | {family:.3f} | {verdict} |")  # fmt: skip
        rows.append(f"{c} (xs rank IC {mean:+.3f}, t {t:+.1f}, chance {chance:.3f}, family "
                    f"{family:.3f}, {verdict.strip('*')})")  # fmt: skip
    if log:
        stamp = datetime.now(UTC).strftime("%Y-%m-%d %H:%M")
        with harness.TRIES.open("a") as f:
            for desc in rows:
                f.write(f"| {stamp} | {IDEA} | {desc} | screen | train | {first.isoformat()} | "
                        "2025-11-09 | - | - | - | - |\n")  # fmt: skip


if __name__ == "__main__":
    main("--log" in sys.argv)
