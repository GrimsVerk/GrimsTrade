"""Lane wide-7, step 2: event-study gate for W13 `festival-gold` (research/wide-7.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).

Run: `uv run python -I research/lib/wide7_festival.py`  (DRY=1: day counts only)
Output: research/results/festival-gold.md
"""

from __future__ import annotations

import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide6_rules as r6  # noqa: E402
import wide7_rules as r  # noqa: E402

SPLIT = date(2011, 1, 1)
RUN = 15
LAGS = 10
OUT = Path(__file__).resolve().parents[1] / "results" / "festival-gold.md"
DRY = bool(os.environ.get("DRY"))
FESTS = sorted(r.DHANTERAS + r.LUNAR_NEW_YEAR)


def gld() -> tuple[list[date], np.ndarray]:
    bars = harness.load_history("train", syms=["GLD"])["GLD"]
    c = np.log(np.array([b.close for b in bars]))
    return [b.date for b in bars[1:]], np.diff(c)


def fit(
    days: list[date], ret: np.ndarray, fest: list[date], n: int = RUN, months: bool = True
) -> tuple[float, float]:
    e = r.run_flags(days, fest, n)
    base = r.month_matrix(days) if months else np.ones((len(days), 1))
    beta, t = r6.ols_dk(ret, np.hstack([e[:, None], base]), days, LAGS)
    return float(beta[0]) * 1e4, float(t[0])


def shifted(fest: list[date], k: int) -> list[date]:
    return [f + timedelta(days=7 * k) for f in fest]


def main() -> None:
    days, ret = gld()
    pre = [i for i, d in enumerate(days) if d < SPLIT]
    post = [i for i, d in enumerate(days) if d >= SPLIT]
    sub = {
        "all": (days, ret),
        "to 2010": ([days[i] for i in pre], ret[pre]),
        "2011 on": ([days[i] for i in post], ret[post]),
    }
    if DRY:
        for k, (dd, _) in sub.items():
            e = r.run_flags(dd, FESTS, RUN)
            print(k, len(dd), int(e.sum()), dd[0], dd[-1])
        return
    b_all, t_all = fit(days, ret, FESTS)
    b_pre, t_pre = fit(*sub["to 2010"], FESTS)
    b_post, t_post = fit(*sub["2011 on"], FESTS)
    shifts = {k: fit(days, ret, shifted(FESTS, k))[0] for k in range(-7, 8)}
    rank = 1 + sum(v > shifts[0] for k, v in shifts.items() if k != 0)
    passed = b_all > 0 and t_all >= 2 and b_pre > 0 and b_post > 0 and rank <= 3
    out = [
        "# Festival gold: event-study gate (wide-7, W13)",
        "",
        "Rule: `research/wide-7.md` (pushed before this ran). Script",
        "`research/lib/wide7_festival.py`.",
        "GLD daily log returns on calendar-month dummies plus a festival-run dummy (the 15",
        "sessions strictly before Dhanteras or the Lunar New Year); b = festival-run day minus",
        "the same month's mean, bps a day; Newey-West t, 10 lags.",
        "",
        "## Gate",
        "",
        "| Test | b, bps a day (t) | Needed |",
        "|---|---:|---|",
        f"| All GLD days 2004-11..2025-11 | {b_all:+.2f} ({t_all:+.2f}) | b > 0, t >= 2 |",
        f"| To 2010 (Baur's years) | {b_pre:+.2f} ({t_pre:+.2f}) | b > 0 |",
        f"| 2011 on | {b_post:+.2f} ({t_post:+.2f}) | b > 0 |",
        f"| Rank of true dates among 15 weekly shifts | {rank} | top 3 |",
        "",
        f"**Gate: {'PASS' if passed else 'fail'}.**",
        "",
        "Shifts by k weeks (bps a day): "
        + ", ".join(f"{k:+d}: {v:+.1f}" for k, v in shifts.items()),
        "",
        "## Shown",
        "",
        "| Period | Both, 15 | Dhanteras only | Lunar New Year only | Both, no months |"
        " Both, 5 sessions |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for k, (dd, rr) in sub.items():
        cells = [
            fit(dd, rr, FESTS),
            fit(dd, rr, r.DHANTERAS),
            fit(dd, rr, r.LUNAR_NEW_YEAR),
            fit(dd, rr, FESTS, months=False),
            fit(dd, rr, FESTS, n=5),
        ]
        out.append(f"| {k} | " + " | ".join(f"{b:+.2f} ({t:+.2f})" for b, t in cells) + " |")
    out += [
        "",
        "## Mean GLD return by calendar month, bps a day (Baur's autumn effect)",
        "",
        "| Month | To 2010 | 2011 on |",
        "|---|---:|---:|",
    ]
    for m in range(1, 13):
        a = [
            float(np.mean([x for d, x in zip(dd, rr, strict=True) if d.month == m])) * 1e4
            for dd, rr in (sub["to 2010"], sub["2011 on"])
        ]
        out.append(f"| {m} | {a[0]:+.1f} | {a[1]:+.1f} |")
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
