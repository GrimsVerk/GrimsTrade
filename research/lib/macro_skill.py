"""Macro features scored without a model (run macro-1): which are worth keeping as RL inputs.

    uv run --with numpy python research/lib/macro_skill.py

For every Friday in train, each feature as known that day (`macro.Features`, look-ahead safe)
against the log return of each asset over the next 28 days. Rank correlation (Spearman) on all
Fridays; the t-value uses every fourth Friday only (non-overlapping labels). Also the rank
correlation with the asset's own 12-month return (does the feature say anything the trend rule
does not already know?). No backtest, nothing logged in tries.md (like ml-feature-skill).
"""

from __future__ import annotations

import math
from datetime import date, timedelta

import harness
import macro
import numpy as np

ASSETS = ["SPY", "TLT", "GLD", "BTC"]


def _rank(x: np.ndarray) -> np.ndarray:
    r = np.empty(len(x))
    r[np.argsort(x, kind="stable")] = np.arange(len(x))
    return r


def spearman(x: np.ndarray, y: np.ndarray) -> float:
    if len(x) < 10 or np.std(x) == 0:
        return math.nan
    return float(np.corrcoef(_rank(x), _rank(y))[0, 1])


def main() -> None:
    f = macro.features()
    feats = {k: v for k, v in vars(f).items() if isinstance(v, macro.Step)}
    hist = harness.load_history("train")
    out = [
        "# Macro features scored alone (no model)",
        "",
        "Run macro-1. Script `lib/macro_skill.py`. Each feature as known on the Friday (look-ahead",
        "safe, `lib/macro.py`) against the next 28-day log return. rho = Spearman rank correlation",
        "on all Fridays; t from every fourth Friday (non-overlapping). `vs 12m` = rank correlation",
        "with the asset's own trailing 12-month return (overlap with what `tsmom12` knows). Train",
        "only (to 2025-11-09). |t| above 2 on a few dozen independent years is weak evidence, and",
        "20 features x 4 assets x 2 windows means a few such values by luck alone.",
        "",
    ]
    for start in (date(1994, 2, 4), date(2003, 1, 3)):
        out += [f"## Fridays from {start}", ""]
        out += ["| Feature | " + " | ".join(f"{a} rho (t) | {a} vs 12m" for a in ASSETS) + " |"]
        out += ["|---|" + "---:|---:|" * len(ASSETS)]
        cols: dict[str, tuple[list[float], list[float], list[float]]] = {}
        rows: dict[str, dict[str, list[float]]] = {k: {a: [] for a in ASSETS} for k in feats}
        for a in ASSETS:
            bars = hist[a]
            d = np.array([b.date.toordinal() for b in bars])
            c = np.array([b.close for b in bars])
            xs, ys, ts = [], [], []
            fr = start
            while fr <= harness.TRAIN_END - timedelta(days=28):
                i = int(np.searchsorted(d, fr.toordinal(), side="right")) - 1
                j = int(np.searchsorted(d, fr.toordinal() + 28, side="right")) - 1
                k = int(np.searchsorted(d, fr.toordinal() - 365, side="right")) - 1
                if k >= 0 and i > k and d[0] <= fr.toordinal() - 365:
                    xs.append(fr.toordinal())
                    ys.append(math.log(c[j] / c[i]))
                    ts.append(math.log(c[i] / c[k]))
                fr += timedelta(days=7)
            cols[a] = ([float(x) for x in xs], ys, ts)
            for name, step in feats.items():
                rows[name][a] = [step.at(date.fromordinal(int(x))) for x in xs]
        for name in feats:
            cells = []
            for a in ASSETS:
                _, ys, ts = cols[a]
                x = np.array(rows[name][a])
                ok = ~np.isnan(x)
                y, t = np.array(ys)[ok], np.array(ts)[ok]
                x = x[ok]
                rho = spearman(x, y)
                sub = np.arange(len(x)) % 4 == 0
                r4 = spearman(x[sub], y[sub])
                tval = r4 * math.sqrt((sub.sum() - 2) / max(1 - r4 * r4, 1e-9)) if r4 == r4 else 0
                cells.append(f"{rho:+.2f} ({tval:+.1f}) | {spearman(x, t):+.2f}")
            out.append(f"| {name} | " + " | ".join(cells) + " |")
        out.append("")
    text = "\n".join(out)
    (harness.RESEARCH / "results" / "macro-skill.md").write_text(text + "\n")
    print(text)


if __name__ == "__main__":
    main()
