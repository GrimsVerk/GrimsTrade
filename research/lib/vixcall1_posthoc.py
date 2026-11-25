"""vix-call-1, post-hoc checks (run after the one run; no tries rows). Card: cards/vix-call-1.md.

    uv run python -I research/lib/vixcall1_posthoc.py

1. V1's log growth gap to `tsmom12` with the 2020 fall cut out, the cut extended by 0, 21, 63
   and 126 sessions past the trough (does the result depend on where the cut ends?).
2. The leg's log return per year spent with trend in and with trend out.
Prints only; the numbers are quoted in research/vix-call-1.md.
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import insure3 as i3  # noqa: E402
import vixcall1 as vc  # noqa: E402


def main() -> None:
    full_days, s3, _, chk = i3.load()
    lo = full_days.index(chk["VXTH_start"])
    days = full_days[lo:]
    cut = {k: s3[k][lo:].copy() for k in ("hold", "trend", "VXTH")}
    for v in cut.values():
        v[0] = 0.0
    lg = vc.leg(cut["VXTH"], cut["hold"])
    v1 = vc.overlay(cut["trend"], lg)
    a, b = days.index(date(2020, 2, 19)), days.index(date(2020, 3, 23))
    for extra in (0, 21, 63, 126):
        m = vc.keep_mask(len(days), a, b + extra)
        g = vc.log_gap(v1, cut["trend"], m)
        print(f"2020 cut + {extra} sessions: V1 log gap to trend {g:+.1f}")
    pos = chk["pos"][lo:]
    for state, name in ((1, "in"), (0, "out")):
        m = pos == state
        m[0] = False
        rate = 100 * float(np.log1p(lg[m]).sum()) / (m.sum() / 252)
        print(f"leg, trend {name} ({m.mean():.1%} of sessions): {rate:+.2f} log pts a year")


if __name__ == "__main__":
    main()
