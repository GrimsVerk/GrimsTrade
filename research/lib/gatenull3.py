"""gate-null-3: the one number the records lack for the retro-check (research/cards/gate-null-3.md).

W36's dose (year-on-year growth of US industrial electricity sales, the gate's 619 rows): lag-1
autocorrelation, skew and |end - start| / SD (the surrogate-choice inputs). Reads the cached
W36 inputs through `wide22.load()`; no download. Run: `uv run python -I research/lib/gatenull3.py`.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))


def acf1(x: Sequence[float]) -> float:
    """Lag-1 sample autocorrelation (mean-removed, full-sample variance in the denominator)."""
    a = np.asarray(x, dtype=float) - float(np.mean(x))
    return float((a[1:] * a[:-1]).sum() / (a * a).sum())


def skew(x: Sequence[float]) -> float:
    """Sample skewness (biased, population moments)."""
    a = np.asarray(x, dtype=float)
    d = a - a.mean()
    return float((d**3).mean() / (d**2).mean() ** 1.5)


def end_gap(x: Sequence[float]) -> float:
    """|last - first| in units of the sample SD (the surrogate end-match check)."""
    a = np.asarray(x, dtype=float)
    return float(abs(a[-1] - a[0]) / a.std())


def main() -> None:
    import wide22 as w
    import wide22_events as ev

    ind, _res, mkt = w.load()
    g = ev.yoy(ind)
    y = {m - ev.LAG: v for m, v in mkt.items()}
    months = [m for m in sorted(g) if m in y]
    x = [g[m] for m in months]
    print(f"W36 dose rows {len(months)} (span {months[-1] - months[0] + 1} months)")
    print(f"acf1 {acf1(x):.3f}  skew {skew(x):+.2f}  |end-start|/SD {end_gap(x):.2f}")


if __name__ == "__main__":
    main()
