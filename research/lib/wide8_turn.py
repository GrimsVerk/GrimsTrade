"""Lane wide-8, step 1: the placebo null and the proposed forward entry for the turn-of-year ETF
loser rebound (research/wide-8.md), and the January-2027 scorer.

Null run (train bars only; never computes a December anchor):
    uv run python -I research/lib/wide8_turn.py          (DRY=1: window counts only)
writes research/results/turn-of-year-null.md and research/forward/proposed-wide8.jsonl.

Forward scoring (from 2027-01-12, after research/lib/fetch.py has refreshed research/data/adj):
    SCORE=1 uv run python -I research/lib/wide8_turn.py
reads the frozen null from the entry and prints the verdict for the first scoreable turn from
2026/27 on. It refuses any turn before 2026/27 (those years suggested the lead or are held out).
"""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide8_rules as r  # noqa: E402

ETFS = ["SPY", "QQQ", "IWM", "XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY",
        "EFA", "EEM", "VNQ", "TLT", "IEF", "LQD", "GLD", "SLV", "DBC"]  # fmt: skip
YEARS = range(1994, 2026)
PLACEBO_MONTHS = range(1, 12)  # never 12
FIRST_TURN = 2026  # tax year of the first unseen turn (2026/27)
ALPHA = 0.02
BSTAR = 0.089  # wide-7's post-2012 pooled slope (seen, optimistic)
ID = "turn-of-year-losers@1"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "research" / "results" / "turn-of-year-null.md"
ENTRY = ROOT / "research" / "forward" / "proposed-wide8.jsonl"
CODE = ["research/lib/wide8_rules.py", "research/lib/wide8_turn.py"]
DRY = bool(os.environ.get("DRY"))

Window = list[tuple[float, float]]


def series(syms: list[str], period: str) -> dict[str, tuple[list[date], np.ndarray]]:
    if period == "train":
        hist = harness.load_history("train", syms=syms)
    else:  # forward scoring: the whole adjusted cache, no cut
        hist = {s: harness._load_csv(harness.DATA / "adj" / f"{s}.csv") for s in syms}
    return {
        s: ([b.date for b in v], np.log(np.array([b.close for b in v]))) for s, v in hist.items()
    }


def points(data: dict[str, tuple[list[date], np.ndarray]], y: int, m: int, last: date) -> Window:
    out: Window = []
    for days, logc in data.values():
        if days:
            p = r.window_point(days, logc, y, m, min(last, days[-1]))
            if p is not None:
                out.append(p)
    return out


def params() -> dict[str, object]:
    return {
        "universe": ETFS,
        "dose": "YTD = log(close last bar of November Y / close last bar on or before 31 Dec "
        "Y-1); L = max(0, -YTD); loser = L > 0",
        "window": "R = log(close last bar on or before 10 Jan Y+1 / close last bar on or before "
        "31 Dec Y)",
        "statistic": "plain OLS t of the slope of R on L across funds, with an intercept",
        "eligible": f">= {r.MIN_FUNDS} funds with dose and window, >= {r.MIN_LOSERS} losers",
        "p": "(1 + #null t >= t) / (1 + #null), null frozen in this entry",
        "pass": f"b > 0 and p <= {ALPHA}",
        "first_turn": "tax year 2026 (31 Dec 2026 .. 8 Jan 2027); if not eligible, the next "
        "eligible turn",
    }


def git(*args: str) -> str:
    return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True,
                          text=True).stdout.strip()  # fmt: skip


def null_run() -> None:
    data = series(ETFS, "train")
    wins: dict[tuple[int, int], Window] = {}
    for y in YEARS:
        for m in PLACEBO_MONTHS:
            pts = points(data, y, m, harness.TRAIN_LAST_BAR)
            if r.eligible(pts):
                wins[(y, m)] = pts
    if DRY:
        print("eligible placebo windows", len(wins), "years", len({y for y, _ in wins}))
        for m in PLACEBO_MONTHS:
            print(" month", m, sum(mm == m for _, mm in wins))
        return
    ts = {k: r.cross_t([p[0] for p in v], [p[1] for p in v]) for k, v in wins.items()}
    null = sorted(t for _, t in ts.values())
    arr = np.array(null)
    q = {k: float(np.quantile(arr, k)) for k in (0.02, 0.05, 0.5, 0.95, 0.98)}
    win_list = list(wins.values())
    pw = {b: r.power(win_list, null, b, ALPHA) for b in (BSTAR, BSTAR / 2)}
    crit = min(t for t in null if r.empirical_p(t, null) <= ALPHA)
    big = sum(abs(t) >= 2 for t in null) / len(null)

    if git("status", "--porcelain", "--", *CODE):
        raise SystemExit("commit the code first: the entry hashes the committed files")
    code = {f: hashlib.sha256((ROOT / f).read_bytes()).hexdigest() for f in CODE}
    prm = params()
    dat = {
        "source": "Yahoo chart endpoint (keyless), dividend-adjusted daily closes, as "
        "research/lib/fetch.py writes research/data/adj",
        "mode": "replayable",
        "null": "placebo anchors m = 1..11 of years 1994-2025, train bars only (<= 2025-11-10)",
    }
    entry = {
        "id": ID,
        "code": code,
        "code_ref": git("rev-parse", "HEAD"),
        "params": prm,
        "data": dat,
        "rule_hash": r.rule_hash(code, prm, dat),
        "metric": "placebo_rank (one-sided empirical p of a cross-sectional t against a frozen "
        "null; not one of forward.py's three metrics: needs adding at freeze)",
        "effect": BSTAR,
        "sd": None,
        "skew": None,
        "kurtosis": None,
        "per_year": 1,
        "alpha": ALPHA,
        "power": round(pw[BSTAR], 3),
        "min_sample": 1,
        "years_needed": 1,
        "null_t": [round(t, 6) for t in null],
        "source": "wide-7 (PR #81), W14 gate, shown cell: turn-of-year slope +0.089 per unit "
        "loss, t 3.9 by year clusters, tax years 2012-2024 (seen; its placebo window reached "
        "|t| 4); research/wide-8.md step 1",
        "note": f"Null: {len(null)} placebo windows; t >= {crit:.2f} needed for p <= {ALPHA}. "
        f"Power {pw[BSTAR]:.2f} at b* {BSTAR}, {pw[BSTAR / 2]:.2f} at half. Reads held-out-year "
        "bars as the dose only.",
        "status": "proposed by lane wide-8 on 2026-11-18; NOT frozen by the owner",
    }
    ENTRY.parent.mkdir(parents=True, exist_ok=True)
    ENTRY.write_text(json.dumps(entry, sort_keys=True) + "\n")

    out = [
        "# Turn-of-year loser rebound: placebo null and power (wide-8, step 1)",
        "",
        "Rule: `research/wide-8.md` step 1 (pushed before this ran). Script",
        "`research/lib/wide8_turn.py`. Train bars only; no December anchor is computed.",
        "",
        f"Eligible placebo windows: {len(null)} (anchors January-November, "
        f"{len({y for y, _ in wins})} years).",
        "",
        "| Null quantile of t | 2% | 5% | 50% | 95% | 98% |",
        "|---|---:|---:|---:|---:|---:|",
        "| t | " + " | ".join(f"{q[k]:+.2f}" for k in (0.02, 0.05, 0.5, 0.95, 0.98)) + " |",
        "",
        f"- Standard deviation of the null t: {arr.std(ddof=1):.2f} (N(0, 1) would give 1).",
        f"- Share of placebo windows with |t| >= 2: {big:.0%} (N(0, 1) would give 5%).",
        f"- t needed for a pass (p <= {ALPHA}): {crit:.2f}.",
        f"- Power (share of placebo windows passing once b* L is added): {pw[BSTAR]:.0%} at b* "
        f"= {BSTAR}, {pw[BSTAR / 2]:.0%} at b* = {BSTAR / 2:.4f}.",
        "",
        "## Null t by anchor month (mean, sd, count)",
        "",
        "| Month | Mean t | Sd | Windows |",
        "|---:|---:|---:|---:|",
    ]
    for m in PLACEBO_MONTHS:
        v = np.array([t for (_, mm), (_, t) in ts.items() if mm == m])
        if len(v) > 1:
            out.append(f"| {m} | {v.mean():+.2f} | {v.std(ddof=1):.2f} | {len(v)} |")
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


def score() -> None:
    entry = json.loads(ENTRY.read_text())
    data = series(ETFS, "forward")
    last = max(d[0][-1] for d in data.values() if d[0])
    for y in range(FIRST_TURN, last.year):
        if r.month_end(y, 12) > last:
            break
        pts = points(data, y, 12, last)
        if not pts:
            print(y, "not scoreable yet (bars do not run past 10 January)")
            return
        v = r.verdict(pts, entry["null_t"], entry["alpha"])
        print(y, json.dumps(v))
        if v["verdict"] in ("pass", "fail"):
            return
    print("no eligible turn scoreable yet")


if __name__ == "__main__":
    score() if os.environ.get("SCORE") else null_run()
