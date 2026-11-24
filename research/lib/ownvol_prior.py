"""Export the monthly sigmas behind risk-menu-3's no-look-ahead own-vol rule, as the live book
`own_vol_70`'s starting window (docs/DECISIONS.md 2026-11-24, own-vol 70% paper book).

    uv run python -I research/lib/ownvol_prior.py

risk-menu-3 (`riskmenu3_run.vt_expanding`) solves k on each 1st from every monthly sigma known by
then: sigma_m = `tsmom12`'s volatility over the 52 complete weeks before the previous day. This
prints those sigmas for every 1st of W = 1994-02-01..2025-10-31 where sigma is finite and > 0
(the ones the rule puts in its expanding window), in the form `strategies/own_vol.py` keeps as
`PRIOR`, and checks that k solved on them is the last k `vt_expanding` itself solves on this
checkout (2025-10-01). That k (0.083779) differs from the 0.083859 risk-menu-3 printed on
2026-11-19 because the gym changed since (crypto fee tiers #32, ETF dividends #30, landed in
#115); the rule is the same. Train data only: nothing
after 2025-10-31 is read. Logs no try (a re-score of a logged config).
"""

from __future__ import annotations

import json
import math
import sys
from datetime import timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness  # noqa: E402
import lstrend2_run as l2  # noqa: E402
import riskmenu3_run as r3  # noqa: E402
import riskmenu_run as rm  # noqa: E402


def main() -> None:
    s1, _rf, _drag, run = l2.tsmom12_sleeve()
    seen: list[tuple[str, float]] = []
    for d in rm.months_in(*r3.W):
        sg = s1.sigma(d - timedelta(days=1))
        if math.isfinite(sg) and sg > 0:
            seen.append((f"{d:%Y-%m}", sg))
    k = r3.solve_k([s for _, s in seen], 0.70)
    _mx, ks = r3.vt_expanding(s1, 0.70, rm.held_count(run))
    k_rule = ks[max(ks)]
    ref = json.loads((harness.RESEARCH / "results" / "risk-menu-3.json").read_text())
    k_pub = ref["k"]["vt-own 70% x"]["k_last"]
    print(
        f"{len(seen)} sigmas {seen[0][0]}..{seen[-1][0]}; k {k:.6f}, vt_expanding {k_rule:.6f} "
        f"on {max(ks)}, risk-menu-3 as printed {k_pub:.6f}"
    )
    if abs(k - k_rule) > 1e-12:
        raise SystemExit("k does not match vt_expanding")
    print("PRIOR = (")
    for i in range(0, len(seen), 4):
        print("    " + " ".join(f'("{m}", {s:.6f}),' for m, s in seen[i : i + 4]))
    print(")")


if __name__ == "__main__":
    main()
