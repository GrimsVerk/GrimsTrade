"""Lane wide-10, step 2: event-study gate for W20 `fed-purchase-flow` (research/wide-10.md).

Descriptive only: no strategy, no backtest, no `tries.md` row. The decision rule was pushed
before this script's first run. Train bars only (load_history("train") cuts at 2025-11-10).
Operations: NY Fed Markets API (keyless), one JSON file per quarter in research/data/nyfed/.

Run: `uv run python -I research/lib/wide10_fedflow.py`  (DRY=1: counts only; FETCH=1 downloads)
Output: research/results/fed-purchase-flow.md
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402
import wide10_events as ev  # noqa: E402

DIR = harness.DATA / "nyfed"
OUT = Path(__file__).resolve().parents[1] / "results" / "fed-purchase-flow.md"
DRY = bool(os.environ.get("DRY"))
URL = "https://markets.newyorkfed.org/api/tsy/all/results/details/search.json"
GATE = (date(2014, 1, 2), date(2025, 11, 10))
PAPER = (date(2009, 3, 1), date(2013, 12, 31))
DASH = (date(2020, 3, 1), date(2020, 4, 30))
QUARTERS = [(y, q) for y in range(2009, 2026) for q in range(1, 5)]


def qfile(y: int, q: int) -> Path:
    return DIR / f"details-{y}q{q}.json"


def fetch() -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    for y, q in QUARTERS:
        start = date(y, 3 * q - 2, 1)
        if start > harness.TRAIN_LAST_BAR or qfile(y, q).exists():
            continue
        end = min(date(y + (q == 4), 1 if q == 4 else 3 * q + 1, 1), harness.TRAIN_LAST_BAR)
        url = f"{URL}?startDate={start}&endDate={end}"
        with urllib.request.urlopen(url, timeout=120) as r:  # noqa: S310 (fixed https URL)
            qfile(y, q).write_bytes(r.read())


def operations() -> list[dict[str, object]]:
    ops: dict[str, dict[str, object]] = {}
    for y, q in QUARTERS:
        p = qfile(y, q)
        if not p.exists():
            continue
        for op in json.loads(p.read_text()).get("treasury", {}).get("auctions", []):
            if date.fromisoformat(op["operationDate"]) <= harness.TRAIN_LAST_BAR:
                ops[str(op["operationId"])] = op  # quarter edges may repeat an operation
    return list(ops.values())


class Series:
    def __init__(self, sym: str):
        bars = harness.load_history("train", syms=[sym])[sym]
        self.days = [b.date for b in bars]
        o = np.array([b.open for b in bars])
        c = np.array([b.close for b in bars])
        self.oc = np.log(c / o)
        self.cc = np.concatenate([[np.nan], np.diff(np.log(c))])

    def mask(self, span: tuple[date, date], drop: tuple[date, date] | None = None) -> np.ndarray:
        m = np.array([span[0] <= d <= span[1] for d in self.days])
        if drop:
            m &= np.array([not (drop[0] <= d <= drop[1]) for d in self.days])
        return m


def fit(x: np.ndarray, y: np.ndarray, m: np.ndarray) -> tuple[float, float, int]:
    b, t = ev.ols_hc1(x[m], y[m])
    return b, t, int(m.sum())


def main() -> None:
    if os.environ.get("FETCH"):
        fetch()
    ops = operations()
    tlt = Series("TLT")
    long_par = ev.daily_par(ops, 20, None)
    x = ev.dose_series(tlt.days, long_par)
    g = tlt.mask(GATE)
    if DRY:
        types = Counter((str(o["operationType"]), ev.keep_operation(o)) for o in ops)
        for (name, kept), n in sorted(types.items()):
            print(f"type {name!r} kept={kept}: {n}")
        days = set(tlt.days)
        print("long-dose days total", len(long_par), "not a TLT day", len(set(long_par) - days))
        for name, span in (("gate", GATE), ("paper", PAPER)):
            m = tlt.mask(span)
            print(name, "TLT days", int(m.sum()), "dosed days", int((x[m] > 0).sum()))
        print("placebos", len(ev.SHIFTS_W20), sorted(ev.SHIFTS_W20))
        print(
            "min placebo days",
            min(int((g & ~np.isnan(ev.shifted(x, k))).sum()) for k in ev.SHIFTS_W20),
        )
        return
    b, t, n = fit(x, tlt.oc, g)
    placebo = [fit(ev.shifted(x, k), tlt.oc, g)[1] for k in ev.SHIFTS_W20]
    rank = ev.rank_highest(t, placebo)
    sd, share = ev.null_spread(placebo)
    gate = [b > 0 and t >= 2, rank <= 2]
    dosed = g & (x > 0)
    lpar = np.expm1(x[dosed])

    def bp(v: float) -> str:
        return f"{v * 1e4:+.1f}"

    out = [
        "# Fed purchase operations and TLT: event-study gate (wide-10, W20)",
        "",
        "Rule: `research/wide-10.md` step 2 (pushed before this ran). Script",
        "`research/lib/wide10_fedflow.py`. Operations: NY Fed Markets API (keyless). y = TLT",
        "open-to-close log return of day d; x = ln(1 + $bn par of 20+ year coupons the Fed bought",
        "on d). Slopes in bps of return per unit of x; White (HC1) t.",
        "",
        "## Gate",
        "",
        "| Test | Value | Needed | Met |",
        "|---|---:|---|---|",
        f"| TLT 2014-01-02..2025-11-10 b (t), {n} days | {bp(b)} ({t:+.2f}) |"
        f" > 0, t >= 2 | {gate[0]} |",
        f"| Rank of true t among 41 calendars (1 = highest) | {rank} | <= 2 | {gate[1]} |",
        "",
        f"**Gate: {'PASS' if all(gate) else 'fail'}.** Empirical one-sided p = {rank}/41 ="
        f" {rank / 41:.3f}. Dosed days in the gate sample: {int(dosed.sum())}, mean L"
        f" ${lpar.mean():.2f}bn, median ${np.median(lpar):.2f}bn, largest ${lpar.max():.2f}bn.",
        "",
        "## Placebo null (dose calendar moved k trading days), TLT 2014-2025",
        "",
        f"40 placebo t: standard deviation {sd:.2f}, share with |t| >= 2 {share:.0%};"
        f" quantiles 5% {np.quantile(placebo, 0.05):+.2f}, 50% {np.quantile(placebo, 0.5):+.2f},"
        f" 95% {np.quantile(placebo, 0.95):+.2f}; smallest {min(placebo):+.2f}, largest"
        f" {max(placebo):+.2f}.",
        "",
        "| k (days) | t |",
        "|---:|---:|",
    ]
    out += [f"| {k:+d} | {v:+.2f} |" for k, v in zip(ev.SHIFTS_W20, placebo, strict=True)]
    out += ["", "## Shown (not gating)", "", "| Cut | b (t) | Days |", "|---|---:|---:|"]

    def row(name: str, r: tuple[float, float, int]) -> None:
        out.append(f"| {name} | {bp(r[0])} ({r[1]:+.2f}) | {r[2]} |")

    row("TLT, papers' years 2009-03..2013-12", fit(x, tlt.oc, tlt.mask(PAPER)))
    row("TLT gate sample, indicator dose (L > 0)", fit((x > 0).astype(float), tlt.oc, g))
    row("TLT gate sample without 2020-03..2020-04", fit(x, tlt.oc, tlt.mask(GATE, DASH)))
    row("TLT close-to-close of d, gate sample", fit(x, tlt.cc, g))
    nxt = np.concatenate([tlt.oc[1:], [np.nan]])
    row("TLT next day's open-to-close on today's x, gate sample", fit(x, nxt, g))
    ief = Series("IEF")
    xi = ev.dose_series(ief.days, ev.daily_par(ops, 7, 10))
    row("IEF on its 7-10 year dose, gate sample", fit(xi, ief.oc, ief.mask(GATE)))
    row("IEF on its 7-10 year dose, papers' years", fit(xi, ief.oc, ief.mask(PAPER)))
    spy = Series("SPY")
    xs = ev.dose_series(spy.days, ev.daily_par(ops, 0, None))
    row("SPY on all coupon par bought, gate sample", fit(xs, spy.oc, spy.mask(GATE)))
    row("SPY on all coupon par bought, papers' years", fit(xs, spy.oc, spy.mask(PAPER)))
    out.append("")
    OUT.write_text("\n".join(out))
    print("\n".join(out))


if __name__ == "__main__":
    main()
