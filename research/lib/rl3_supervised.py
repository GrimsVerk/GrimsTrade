"""Post-hoc learner check of run rl-3 (research/rl-3.md, "After the results"): a supervised
forecaster in place of PPO, on the same planted tables and residual action.

    uv run --with torch python research/lib/rl3_supervised.py   # logs control rows

Per walk-forward fold (RL 2's 13 folds and embargo): ordinary least squares of the coming week's
risk-adjusted return (`rl3_plant.week_z`) on all 28 inputs (17 asset inputs + `peek` + 10 macro,
missing macro = 0), fitted on the six assets' training Fridays, inputs scaled with training
statistics. Score = forecast / its standard deviation on the training rows (unit scale, like
`peek`), so k = 1 of the ceiling's rules; k fixed before the run, not chosen. Replayed through
`gym.simulate` with RL 2's residual action. Not pre-registered: written after the agent results.
"""

from __future__ import annotations

import json

import numpy as np

STRENGTHS = ["0.00", "0.05", "0.10", "0.20"]


def main() -> None:
    import rl2_env
    import rl3_plant
    import stats
    from harness import TRAIN_END
    from ml import first_friday
    from rl3_eval import OOS_START, OUT, SINCE, _common
    from rl3_train import tables
    from rl_train import FOLDS, train_end

    r1, hist, base = _common()
    ts = base["tsmom12"]
    out = {}
    for rho in STRENGTHS:
        rt = tables(float(rho))["six"]
        t = rt.t
        z = rl3_plant.week_z(t)
        X = np.concatenate([t.X, np.nan_to_num(np.repeat(t.G[:, None, :], z.shape[1], 1))], 2)
        i0 = t.index(OOS_START)
        S = np.zeros(z.shape)
        for y in FOLDS:
            e = train_end(t, y)
            tr = np.isfinite(z[:e])
            A = X[:e][tr]
            mu, sd = A.mean(0), A.std(0)
            sd = np.where(sd > 1e-9, sd, 1.0)
            Af = np.column_stack([np.ones(len(A)), (A - mu) / sd])
            beta = np.linalg.lstsq(Af, z[:e][tr], rcond=None)[0]
            scale = float((Af @ beta).std()) or 1.0
            a = t.index(first_friday(y))
            b = t.index(first_friday(y + 2)) if y + 2 <= 2025 else len(t.fridays)
            fx = np.concatenate([np.ones((b - a, z.shape[1], 1)), (X[a:b] - mu) / sd], 2)
            S[a:b] = np.where(t.elig[a:b], (fx @ beta) / scale, 0.0)
        keep = np.isfinite(z) & t.elig
        keep[:i0] = False
        ic = float(np.corrcoef(S[keep], z[keep])[0, 1])
        ic_peek = float(np.corrcoef(S[keep], t.X[:, :, -1][keep])[0, 1])
        sc = S[i0:]
        key = f"sup-ols-{rho}"
        run = r1.log_run(key, "control", rl2_env.res_decisions(rt, i0, sc[:, None, :],
                         rl2_env.base_daily(hist, t.book.syms, OOS_START, TRAIN_END), TRAIN_END),
                         hist, OOS_START, TRAIN_END)  # fmt: skip
        w = rl2_env.residual(rt.B[i0:], rt.L[i0:], t.elig[i0:], rt.coin, sc)
        d, p = r1.vs(run, ts)
        out[rho] = {**r1.describe(run), "diff": d, "p": p,
                    "since2003_diff": r1.vs(run, ts, SINCE)[0], "forecast_ic": ic,
                    "corr_forecast_peek": ic_peek,
                    "active": rl2_env.active_share(w, rt.B[i0:])}  # fmt: skip
        print(rho, f"Sharpe {stats.sharpe(run.rets):.3f} d {d:+.3f} p {p:.2f} IC {ic:+.3f} "
              f"corr(peek) {ic_peek:+.2f}", flush=True)  # fmt: skip
    (OUT / "sup3.json").write_text(json.dumps(out, indent=1, default=r1._json))


if __name__ == "__main__":
    main()
