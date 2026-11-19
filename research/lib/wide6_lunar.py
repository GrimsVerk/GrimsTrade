"""Lane wide-6, step 2: event-study gate for W3 `lunar` (research/wide-6.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).

Run: `uv run python -I research/lib/wide6_lunar.py`  (DRY=1: day counts only, no statistics)
Output: research/results/lunar.md
"""

from __future__ import annotations

import os
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide6_rules as r  # noqa: E402

GATE = ("SPY", date(2007, 1, 1), date(2025, 11, 10))
OUT = Path(__file__).resolve().parents[1] / "results" / "lunar.md"
DRY = bool(os.environ.get("DRY"))
SHOWN: list[tuple[str, date, date, str]] = [
    ("GSPC", date(1962, 1, 1), date(1972, 12, 31), "before the paper's sample"),
    ("GSPC", date(1973, 1, 1), date(2001, 7, 31), "paper's sample"),
    ("GSPC", date(2001, 8, 1), date(2006, 12, 31), "after sample, before journal"),
    ("GSPC", date(2007, 1, 1), date(2016, 12, 31), "post-publication, first half"),
    ("GSPC", date(2017, 1, 1), date(2025, 11, 10), "post-publication, second half"),
    ("SPY", date(1993, 2, 1), date(2001, 7, 31), "paper's sample"),
    ("SPY", date(2007, 1, 1), date(2016, 12, 31), "gate, first half"),
    ("SPY", date(2017, 1, 1), date(2025, 11, 10), "gate, second half"),
    ("QQQ", date(2007, 1, 1), date(2025, 11, 10), "gate window"),
    ("N225", date(2007, 1, 1), date(2025, 11, 10), "gate window"),
    ("FTSE", date(2007, 1, 1), date(2025, 11, 10), "gate window"),
    ("GDAXI", date(2007, 1, 1), date(2025, 11, 10), "gate window"),
    ("BTC", date(2014, 1, 1), date(2025, 11, 10), "coin, all days"),
]


def returns(sym: str, lo: date, hi: date) -> tuple[list[date], np.ndarray]:
    bars = harness.load_history("train", syms=[sym])[sym]
    c = np.log(np.array([b.close for b in bars]))
    days = [b.date for b in bars]
    keep = [i for i in range(1, len(days)) if lo <= days[i] <= hi]
    return [days[i] for i in keep], np.array([c[i] - c[i - 1] for i in keep])


def stat(
    days: list[date], ret: np.ndarray, half: int, shift: int = 0
) -> tuple[float, float, int, int]:
    p = r.moon_period(days, half, shift)
    a, b = ret[p == 1], ret[p == -1]
    d, t = r.welch_t(a, b)
    return d * 1e4, t, len(a), len(b)


def shift_rank(days: list[date], ret: np.ndarray, half: int) -> tuple[int, list[float]]:
    diffs = [stat(days, ret, half, k)[0] for k in range(29)]
    return 1 + sum(x > diffs[0] for x in diffs[1:]), diffs


def main() -> None:
    sym, lo, hi = GATE
    days, ret = returns(sym, lo, hi)
    if DRY:
        p = r.moon_period(days, 7)
        print(sym, len(days), int((p == 1).sum()), int((p == -1).sum()), int((p == 0).sum()))
        return
    d, t, na, nb = stat(days, ret, 7)
    rank, diffs = shift_rank(days, ret, 7)
    passed = d > 0 and t >= 2 and rank <= 3
    out = [
        "# Lunar phases: event-study gate (wide-6, W3)",
        "",
        "Rule: `research/wide-6.md` (pushed before this ran). Script",
        "`research/lib/wide6_lunar.py`.",
        "Daily close-to-close log returns; new-moon period minus full-moon period, bps a day;",
        "Welch t; 15-day window (N = 7) unless stated. Rank = place of the true phase among 29",
        "phase shifts (1 = largest difference).",
        "",
        "## Gate: SPY, 2007-01 to 2025-11-10",
        "",
        "| Days new / full | New minus full, bps a day (t) | Rank of 29 | Gate |",
        "|---|---:|---:|---|",
        f"| {na} / {nb} | {d:+.2f} ({t:+.2f}) | {rank} | **{'PASS' if passed else 'fail'}** |",
        "",
        "Phase shifts 0..28 days (bps a day): " + ", ".join(f"{x:+.1f}" for x in diffs),
        "",
        "## Shown",
        "",
        "| Series | Years | What | Days new / full | 15-day: bps (t), rank | 7-day: bps (t) |",
        "|---|---|---|---|---:|---:|",
    ]
    for s, a, b, what in SHOWN:
        dd, rr = returns(s, a, b)
        d15, t15, n1, n2 = stat(dd, rr, 7)
        rk, _ = shift_rank(dd, rr, 7)
        d7, t7, _, _ = stat(dd, rr, 3)
        out.append(
            f"| {s} | {a:%Y-%m}..{b:%Y-%m} | {what} | {n1} / {n2} | {d15:+.2f} ({t15:+.2f}), "
            f"{rk} | {d7:+.2f} ({t7:+.2f}) |"
        )
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
