"""Lane wide-9, step 2: event-study gate for W17 `fork-premium` (research/wide-9.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).

Run: `uv run python -I research/lib/wide9_fork.py`  (DRY=1: counts only)
Output: research/results/fork-premium.md
"""

from __future__ import annotations

import math
import os
import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide9_events as ev  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "fork-premium.md"
DRY = bool(os.environ.get("DRY"))
SHIFTS = [k * 30 for k in range(-20, 21) if k != 0]
MIN_EVENTS = 10

Event = tuple[str, date, int]


def log_closes(sym: str) -> dict[date, float]:
    bars = harness.load_history("train", adjusted=False, syms=[sym])[sym]
    return {b.date: math.log(b.close) for b in bars}


def rows(
    e: dict[date, float], events: list[Event], shift: int = 0, n: int = 10
) -> list[tuple[Event, float, float]]:
    out = []
    for name, d, s in events:
        lg = ev.legs(e, d + timedelta(days=shift), n)
        if lg is not None:
            out.append(((name, d, s), lg[0], lg[1]))
    return out


def stat(rs: list[tuple[Event, float, float]]) -> tuple[float, float]:
    return ev.one_sample_t([pre - post for _, pre, post in rs])


def pct(v: float) -> str:
    return f"{v * 100:+.2f}%"


def main() -> None:
    eth, btc = log_closes("ETH"), log_closes("BTC")
    e = {d: eth[d] - btc[d] for d in eth if d in btc}
    true = rows(e, ev.FORKS)
    placebos = {k: rows(e, ev.FORKS, k) for k in SHIFTS}
    kept = {k: r for k, r in placebos.items() if len(r) >= MIN_EVENTS}
    if DRY:
        print("events", len(true), "scope 1:", sum(x[0][2] for x in true))
        print("placebos kept", len(kept), "of", len(SHIFTS))
        print("events per placebo", sorted(len(r) for r in kept.values()))
        return
    y = [pre - post for _, pre, post in true]
    m, t = stat(true)
    pt = [stat(r)[1] for r in kept.values()]
    rank = ev.rank_highest(t, pt)
    b = ev.ols_slope([x[0][2] for x in true], y)
    pre_m = float(np.mean([p for _, p, _ in true]))
    post_m = float(np.mean([q for _, _, q in true]))
    g = [m > 0 and t >= 2, rank <= 2, b > 0, pre_m > 0 and post_m < 0]
    sd, share = ev.null_spread(pt)
    out = [
        "# Ethereum upgrades: event-study gate (wide-9, W17)",
        "",
        "Rule: `research/wide-9.md` step 2 (pushed before this ran). Script",
        "`research/lib/wide9_fork.py`. E = log(ETH / BTC) at the daily close (UTC). Pre =",
        "E(d-1) - E(d-11), Post = E(d+9) - E(d-1), Y = Pre - Post; plain one-sample t.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| Mean Y (t), {len(true)} events | {pct(m)} ({t:+.2f}) | > 0, t >= 2 | {g[0]} |",
        f"| Rank of true t among {1 + len(pt)} calendars (1 = highest) | {rank} | <= 2 | {g[1]} |",
        f"| Slope of Y on scope | {pct(b)} | > 0 | {g[2]} |",
        f"| Mean Pre, mean Post | {pct(pre_m)}, {pct(post_m)} | > 0, < 0 | {g[3]} |",
        "",
        f"**Gate: {'PASS' if all(g) else 'fail'}.** Empirical one-sided p = {rank}/"
        f"{1 + len(pt)} = {rank / (1 + len(pt)):.3f}.",
        "",
        "## Events",
        "",
        "| Fork | Day | Scope | Pre | Post | Y |",
        "|---|---|---:|---:|---:|---:|",
    ]
    out += [
        f"| {nm} | {d} | {s} | {pct(p)} | {pct(q)} | {pct(p - q)} |" for (nm, d, s), p, q in true
    ]
    no_dao = [r for r in true if r[0][0] != "DAO fork"]
    m0, t0 = stat(no_dao)
    eth_rows = rows(eth, ev.FORKS)
    m_eth, t_eth = stat(eth_rows)
    m5, t5 = stat(rows(e, ev.FORKS, n=5))
    out += [
        "",
        "## Shown",
        "",
        "| Cell | Mean Y (t) | Events |",
        "|---|---:|---:|",
        f"| Scope 1 | {pct(np.mean([p - q for x, p, q in true if x[2] == 1]))} | "
        f"{sum(x[0][2] for x in true)} |",
        f"| Scope 0 | {pct(np.mean([p - q for x, p, q in true if x[2] == 0]))} | "
        f"{sum(1 - x[0][2] for x in true)} |",
        f"| Without the DAO fork | {pct(m0)} ({t0:+.2f}) | {len(no_dao)} |",
        f"| ETH alone (not against BTC) | {pct(m_eth)} ({t_eth:+.2f}) | {len(eth_rows)} |",
        f"| 5-day windows | {pct(m5)} ({t5:+.2f}) | {len(rows(e, ev.FORKS, n=5))} |",
        "",
        "## Placebo null (calendar moved by k x 30 days)",
        "",
        f"{len(pt)} placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {np.quantile(pt, 0.05):+.2f}, 50% {np.quantile(pt, 0.5):+.2f},"
        f" 95% {np.quantile(pt, 0.95):+.2f}; largest {max(pt):+.2f}.",
        "",
        "| Shift (days) | Events | Mean Y | t |",
        "|---:|---:|---:|---:|",
    ]
    for k, r in kept.items():
        mk, tk = stat(r)
        out.append(f"| {k:+d} | {len(r)} | {pct(mk)} | {tk:+.2f} |")
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
