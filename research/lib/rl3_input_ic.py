"""How much of the planted kind of signal do the REAL rl inputs hold? (run rl-3, descriptive)

    uv run python research/lib/rl3_input_ic.py > research/results/rl-3-inputs.md

Correlation of each real input of RL 2's agents with the coming week's risk-adjusted return
(`rl3_plant.week_z`, the target `peek` copies) on the six assets, Fridays 2000-01-07 to the end
of train; then all inputs together: in-sample least squares (an upper bound, overfit) and
walk-forward least squares refitted every two years on the Fridays before. No backtest, no tries
row (like ml-feature-skill). Added after the agent results; not part of the card's verdict.
"""

from __future__ import annotations

from datetime import date

import numpy as np
import rl2_data
import rl3_plant
import rl_env


def main() -> None:
    t = rl2_data.load()["six"].t
    z = rl3_plant.week_z(t)
    i0 = t.index(date(2000, 1, 7))
    keep = np.isfinite(z)
    keep[:i0] = False
    n_a = z.shape[1]
    G = np.repeat(t.G[:, None, :], n_a, 1)
    up = t.X[:, :, 5] > 0.5
    print("# RL 3: weekly IC of the real inputs (six assets, 2000-01-07 to 2025-11-09)\n")
    print(
        "Script `lib/rl3_input_ic.py` (descriptive, no backtest). IC = correlation with the coming"
    )
    print("week's risk-adjusted return, the target the planted input copies. Macro inputs repeat")
    print("across assets, so their real standard error is larger than 1/sqrt(cells).\n")
    for name, mask in [("all eligible cells", keep), ("cells `tsmom12` holds", keep & up)]:
        res = []
        for k, f in enumerate(rl_env.ASSET_FEATS):
            x = t.X[:, :, k][mask]
            if x.std() > 0:
                res.append((f, float(np.corrcoef(x, z[mask])[0, 1])))
        for k, f in enumerate(rl_env.MACRO_FEATS):
            g = G[:, :, k][mask]
            ok = np.isfinite(g)
            res.append((f, float(np.corrcoef(g[ok], z[mask][ok])[0, 1])))
        res.sort(key=lambda r: -abs(r[1]))
        print(f"## {name}: {mask.sum()} cells (1/sqrt = {1 / np.sqrt(mask.sum()):.3f})\n")
        print("| Input | IC |\n|---|---:|")
        for f, c in res:
            print(f"| `{f}` | {c:+.3f} |")
        print()
    feats = [k for k in range(t.X.shape[2]) if t.X[:, :, k][keep].std() > 0]
    X = np.concatenate([t.X[:, :, feats], np.nan_to_num(G)], 2)
    A = X[keep]
    A = np.column_stack([np.ones(len(A)), (A - A.mean(0)) / A.std(0).clip(1e-9)])
    beta = np.linalg.lstsq(A, z[keep], rcond=None)[0]
    r_in = float(np.corrcoef(A @ beta, z[keep])[0, 1])
    yrs = np.repeat(np.array([d.year for d in t.fridays])[:, None], n_a, 1)
    ok = np.isfinite(z)
    preds, ys = [], []
    for y0 in range(2000, 2026, 2):
        tr = ok & (yrs < y0 - 1)  # a year's gap: no overlap with the traded years
        te = ok & (yrs >= y0) & (yrs < y0 + 2)
        mu, sd = X[tr].mean(0), X[tr].std(0).clip(1e-9)
        b = np.linalg.lstsq(np.column_stack([np.ones(tr.sum()), (X[tr] - mu) / sd]), z[tr],
                            rcond=None)[0]  # fmt: skip
        preds.append(np.column_stack([np.ones(te.sum()), (X[te] - mu) / sd]) @ b)
        ys.append(z[te])
    r_wf = float(np.corrcoef(np.concatenate(preds), np.concatenate(ys))[0, 1])
    print(f"## All {A.shape[1] - 1} inputs together\n")
    print(f"- In-sample least squares (overfit upper bound): correlation {r_in:+.3f}; pure chance")
    print(f"  with this many inputs gives about {np.sqrt((A.shape[1] - 1) / len(A)):.3f}.")
    print(f"- Walk-forward least squares (refitted every two years, a year's gap): IC {r_wf:+.3f}.")


if __name__ == "__main__":
    main()
