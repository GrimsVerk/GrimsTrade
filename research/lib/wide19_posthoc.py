"""wide-19 post hoc (not a try): why Z is 0 for `cred-xs`, and the correlation-corrected Z.

    uv run --with numpy python research/lib/wide19_posthoc.py

At the last decision Friday of each set: the mean cross-sectional variance of x against
V = 1/52, the mean pairwise correlation rho of the assets' weekly returns (over Fridays where
both have one), and Z had the noise part of the cross-sectional variance been V (1 - rho),
as it is for correlated risks, instead of V. Also `cred-lr`'s raw time variance of x.
"""

from __future__ import annotations

from datetime import timedelta

import common as c
import numpy as np
from wide19 import LAST, LR_MIN_RETURNS, V, State, weekly_returns


def main() -> None:
    for name in ("six", "etf", "idx"):
        ctx = c.ctx(name)
        d = min(ctx.end, LAST)
        while d.weekday() != 4:
            d -= timedelta(days=1)
        view = ctx.panel.view(c.harness.decide_time(d))
        st = State(view)
        cnt = (~np.isnan(st.xm)).sum(axis=0)
        cols = st.xm[:, cnt >= 2]
        s2 = float(np.mean(np.nanvar(cols, axis=0, ddof=1)))
        first = min(int(view.dates(s)[0]) for s in st.syms)
        grid = d.toordinal() - 7 * np.arange((d.toordinal() - first) // 7 + 1, -1, -1)
        r = np.array([weekly_returns(view.dates(s), view.close(s), grid) for s in st.syms])
        rhos = []
        for i in range(len(r)):
            for j in range(i + 1, len(r)):
                ok = ~np.isnan(r[i]) & ~np.isnan(r[j])
                if ok.sum() > 104:
                    rhos.append(float(np.corrcoef(r[i][ok], r[j][ok])[0, 1]))
        rho = float(np.mean(rhos))
        a = s2 - V * (1 - rho)
        z = max(a, 0) / (max(a, 0) + V)
        nret = (~np.isnan(r)).sum(axis=1)
        dev = st.xm[nret >= LR_MIN_RETURNS] - st.mu[nret >= LR_MIN_RETURNS, None]
        tv = float(np.nanmean(dev * dev))
        print(f"{name} {d}: mean S2 {s2:.4f} vs V {V:.4f} (ratio {s2 / V:.2f}); rho {rho:.2f};"
              f" corrected a {a:.4f}, Z {z:.2f}; cred-lr time var {tv:.4f} ({tv / V:.2f} V),"
              f" Z {st.z['cred-lr']:.2f}")  # fmt: skip


if __name__ == "__main__":
    main()
