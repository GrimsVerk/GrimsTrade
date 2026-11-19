"""How big an edge over equal weight would luck alone produce, given the tries made?

    uv run --with numpy python research/lib/deflation.py

Reads the saved equity curves of every `variant` row on the six assets (no new backtests).
"""

from __future__ import annotations

import csv

import harness
import numpy as np
import stats


def curve(idea: str, variant: str) -> dict[str, float]:
    path = harness.DATA / "runs" / idea / f"{variant}.train.csv"
    with path.open() as f:
        return {r["date"]: float(r["equity"]) for r in csv.DictReader(f)}


def main() -> None:
    rows = []
    for line in harness.TRIES.read_text().splitlines():
        cells = [x.strip() for x in line.strip().strip("|").split("|")]
        if len(cells) >= 5 and cells[3] == "variant" and "@" not in cells[2]:
            rows.append((cells[1], cells[2]))
    ew = curve("baselines", "equal-weight")
    diffs, ses = [], []
    for idea, variant in rows:
        v = curve(idea, variant)
        days = sorted(set(v) & set(ew))
        a = np.array([v[d] for d in days])
        b = np.array([ew[d] for d in days])
        ra, rb = a[1:] / a[:-1] - 1, b[1:] / b[:-1] - 1
        d, _, lo, hi = stats.sharpe_diff_boot(ra, rb, draws=500)
        diffs.append((d, f"{idea}/{variant}"))
        ses.append((hi - lo) / 3.29)
    n = len(rows)
    se = float(np.median(ses))
    luck = stats.expected_max_sharpe(n, se**2)
    best = max(diffs)
    out = [
        "# How much of the best result could be luck?",
        "",
        f"Variants that could have been selected, on the six assets: {n}. Typical standard error "
        f"of a Sharpe difference to equal weight over the train period: {se:.2f}.",
        "",
        f"If none of the {n} had any edge at all, the best of them would still be expected to "
        f"beat equal weight by about **{luck:+.2f}** Sharpe (Bailey & Lopez de Prado's expected "
        f"maximum). The best one actually seen: **{best[0]:+.2f}** (`{best[1]}`).",
        "",
        "Sharpe difference to equal weight, every selectable variant, best first:",
        "",
        "| Variant | dSharpe vs equal weight |",
        "|---|---:|",
    ]
    out += [f"| {name} | {d:+.2f} |" for d, name in sorted(diffs, reverse=True)]
    (harness.RESEARCH / "results" / "deflation.md").write_text("\n".join(out) + "\n")
    print("\n".join(out))


if __name__ == "__main__":
    main()
