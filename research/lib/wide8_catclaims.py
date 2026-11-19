"""Lane wide-8, step 3: event-study gate for W15 `cat-claims` (research/wide-8.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).
Needs NOAA's keyless HURDAT2 file in research/data/hurdat/ (see wide-8.md).

Run: `uv run python -I research/lib/wide8_catclaims.py`  (DRY=1: event counts only)
Output: research/results/cat-claims.md
"""

from __future__ import annotations

import os
import sys
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide6_rules as r6  # noqa: E402
import wide8_events as ev  # noqa: E402

HURDAT = harness.DATA / "hurdat" / "hurdat2-1851-2025-092326.txt"
OUT = Path(__file__).resolve().parents[1] / "results" / "cat-claims.md"
DRY = bool(os.environ.get("DRY"))
FIRST = date(2002, 8, 1)
SPLIT = date(2014, 1, 1)
N = 20
HEDGE = 0.5
SHIFTS = [k for k in range(-11, 12) if k != 0]

Event = tuple[str, date, int]


def load() -> dict[str, tuple[list[date], np.ndarray]]:
    hist = harness.load_history("train", syms=["LQD", "TLT", "IEF"])
    return {
        s: ([b.date for b in v], np.log(np.array([b.close for b in v]))) for s, v in hist.items()
    }


def outcome(px: dict[str, tuple[list[date], np.ndarray]], d: date, n: int, kind: str) -> float:
    def ret(s: str) -> float:
        return ev.after_return(px[s][0], px[s][1], d, n)

    if kind == "spread":
        return ret("LQD") - HEDGE * ret("TLT")
    if kind == "ief":
        return ret("LQD") - ret("IEF")
    return ret(kind)


def usable(
    events: list[Event], px: dict[str, tuple[list[date], np.ndarray]], n: int
) -> list[Event]:
    return [e for e in events if e[1] >= FIRST and not np.isnan(outcome(px, e[1], n, "spread"))]


def fit(
    events: list[Event], px: dict[str, tuple[list[date], np.ndarray]], kind: str = "spread",
    n: int = N,
) -> tuple[float, float, int]:  # fmt: skip
    ev_ = usable(events, px, n)
    if len(ev_) < 5:
        return float("nan"), float("nan"), len(ev_)
    y = np.array([outcome(px, d, n, kind) for _, d, _ in ev_])
    x = np.column_stack([np.ones(len(ev_)), [c for _, _, c in ev_]])
    beta, t = r6.ols_dk(y, x, [d.year for _, d, _ in ev_], 0)
    return float(beta[1]), float(t[1]), len(ev_)


def pct(x: float) -> str:
    return f"{x * 100:+.2f}"


def main() -> None:
    storms = ev.parse_hurdat(HURDAT.read_text())
    events = ev.landfall_events(storms)
    px = load()
    use = usable(events, px, N)
    if DRY:
        print("events", len(use), "seasons", len({d.year for _, d, _ in use}))
        print("by category", sorted(Counter(c for _, _, c in use).items()))
        print("halves", sum(d < SPLIT for _, d, _ in use), sum(d >= SPLIT for _, d, _ in use))
        return
    b, t, n = fit(events, px)
    b1, t1, n1 = fit([e for e in events if e[1] < SPLIT], px)
    b2, t2, n2 = fit([e for e in events if e[1] >= SPLIT], px)
    shifted = []
    for k in SHIFTS:
        moved = [(s, ev.shift_years(d, k), c) for s, d, c in use]
        shifted.append(fit(moved, px)[0])
    rank = ev.rank_most_negative(b, shifted)
    g = [b < 0 and t <= -2, b1 < 0 and b2 < 0, rank <= 2]
    out = [
        "# Hurricane landfalls and bonds: event-study gate (wide-8, W15)",
        "",
        "Rule: `research/wide-8.md` step 3 (pushed before this ran). Script",
        "`research/lib/wide8_catclaims.py`. Events: US mainland landfalls in NOAA HURDAT2.",
        "Y = log LQD - 0.5 log TLT over 20 sessions after the event day; slope on the",
        "Saffir-Simpson category (0 = tropical storm), percentage points per category, t",
        "clustered by season.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Slope, all events 2002-2025 (t, n) | {pct(b)} ({t:+.2f}, {n}) | < 0, t <= -2 | "
        f"{g[0]} |",
        f"| Slope 2002-2013 / 2014-2025 (t) | {pct(b1)} ({t1:+.2f}, {n1}) / {pct(b2)} "
        f"({t2:+.2f}, {n2}) | both < 0 | {g[1]} |",
        f"| Rank among 23 calendars (1 = most negative) | {rank} | <= 2 | {g[2]} |",
        "",
        f"**Gate: {'PASS' if all(g) else 'fail'}.**",
        "",
        "## Shown",
        "",
        "| Outcome | Slope per category, 20 sessions (t) | 60 sessions (t) |",
        "|---|---:|---:|",
    ]
    for kind, label in (("spread", "LQD - 0.5 TLT"), ("LQD", "LQD"), ("TLT", "TLT"),
                        ("ief", "LQD - IEF")):  # fmt: skip
        b20, t20, _ = fit(events, px, kind)
        b60, t60, _ = fit(events, px, kind, 60)
        out.append(f"| {label} | {pct(b20)} ({t20:+.2f}) | {pct(b60)} ({t60:+.2f}) |")
    major = [outcome(px, d, N, "spread") for _, d, c in use if c >= 3]
    ts_ = [outcome(px, d, N, "spread") for _, d, c in use if c == 0]
    out += [
        "",
        f"Mean Y, major landfalls (category >= 3, n {len(major)}) minus tropical-storm landfalls "
        f"(n {len(ts_)}): {pct(float(np.mean(major)) - float(np.mean(ts_)))} points.",
        "",
        "Events by category: "
        + ", ".join(f"{c}: {k}" for c, k in sorted(Counter(c for _, _, c in use).items())),
        "",
        "## Events (category >= 3)",
        "",
        "| Storm | Event day | Category | Y, 20 sessions |",
        "|---|---|---:|---:|",
    ]
    for s, d, c in use:
        if c >= 3:
            nm = storms[s][0].title()
            out.append(f"| {nm} ({s}) | {d} | {c} | {pct(outcome(px, d, N, 'spread'))} |")
    out += ["", "## Shifted calendars (slope, points per category)", "", "| k years | Slope |",
            "|---:|---:|"]  # fmt: skip
    out += [f"| {k:+d} | {pct(v)} |" for k, v in zip(SHIFTS, shifted, strict=True)]
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
