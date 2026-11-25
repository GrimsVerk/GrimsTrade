"""Lane wide-26, record-closing check: W18 `elimination-mood` (research/cards/wide-26b.md;
rule pushed before the match file was fetched and before this script's first run).

Descriptive only. Cached files only (wide-26/intl-results, wide-24's index closes); nothing
after 2025-10-31. Run with `python -I`.

Run:  `uv run python -I research/lib/wide26_w18.py`  (DRY=1: counts only)
Output: research/results/elimination-mood.md
"""

from __future__ import annotations

import os
import sys
from collections import Counter
from collections.abc import Sequence
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import datawide1 as dw  # noqa: E402
import gatepower as gp  # noqa: E402
import wide24 as w24  # noqa: E402
import wide24_events as e24  # noqa: E402
import wide26_events as ev  # noqa: E402

RESULTS = Path(__file__).resolve().parents[1] / "results"
DRY = bool(os.environ.get("DRY"))
MATCHES = "wide-26/intl-results/2026-11-25"
GATE = (date(2006, 1, 1), date(2025, 10, 31))
TEAM = {
    "Germany": "GDAXI", "England": "FTSE", "Japan": "N225", "France": "FCHI",
    "Italy": "FTSEMIB.MI", "Spain": "IBEX", "Netherlands": "AEX", "Belgium": "BFX",
    "Switzerland": "SSMI", "Sweden": "OMX", "Austria": "ATX", "Brazil": "BVSP",
    "Mexico": "MXX", "South Korea": "KS11", "Australia": "AORD", "United States": "^GSPC",
    "Canada": "GSPTSE", "New Zealand": "NZ50", "Indonesia": "JKSE", "Malaysia": "KLSE",
    "India": "BSESN", "Israel": "TA125.TA", "Singapore": "STI", "Taiwan": "TWII",
    "Hong Kong": "HSI",
}  # fmt: skip

Rows = dict[str, tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]]


def load() -> tuple[list[tuple[str, int, str, int, str]], dict[str, w24.Market]]:
    root = dw.cache_root()
    m = ev.parse_matches((root / MATCHES / "results.csv").read_text())
    so = ev.parse_shootouts((root / MATCHES / "shootouts.csv").read_text())
    events = [e for e in ev.knockout_events(m, so) if e[1] <= GATE[1].toordinal()]
    mk = {}
    for name in w24.COUNTRY:
        path = root / w24.GSPC if name == "^GSPC" else root / w24.YAHOO / f"{name}.json"
        mk[name] = w24.load_market(path, name)
    return events, mk


def rows(mk: dict[str, w24.Market], after: int = 0) -> Rows:
    a, b = GATE[0].toordinal(), GATE[1].toordinal()
    out = {}
    for name, m in mk.items():
        r = ev.session_rows(m.dates, m.logc, w24.others(mk, name), a, b, after)
        if len(r[0]):
            out[name] = r
    return out


def doses(
    mk: dict[str, w24.Market],
    rw: Rows,
    events: Sequence[tuple[str, int, str, int, str]],
    kind: str = "elim",
    weight: str = "one",
    shift: int = 0,
    only: str | None = None,
) -> dict[str, np.ndarray]:
    per: dict[str, list[tuple[int, float]]] = {n: [] for n in mk}
    for team, day, k, num, t in events:
        if k != kind or team not in TEAM or (only and t != only):
            continue
        per[TEAM[team]].append((day, 1.0 if weight == "one" else float(num - 3)))
    return {n: ev.next_session_dose(mk[n].dates, per[n], shift)[r[0]] for n, r in rw.items()}


def fit(rw: Rows, dz: dict[str, np.ndarray], outcome: int = 1) -> tuple[float, float, int]:
    """(b, Driscoll-Kraay t, rows): y (outcome 1) or raw (2) on market dummies and D."""
    names = list(rw)
    n = sum(len(rw[k][0]) for k in names)
    k = len(names)
    x = np.zeros((n, k + 1))
    y = np.zeros(n)
    per = np.zeros(n, dtype=int)
    i = 0
    for j, name in enumerate(names):
        r = rw[name]
        m = len(r[0])
        x[i : i + m, j] = 1.0
        x[i : i + m, k] = dz[name]
        y[i : i + m] = r[outcome]
        per[i : i + m] = r[3]
        i += m
    b, t = gp.dk_fit(x, y, per, ev.W18_LAGS, k)
    return b, t, n


def main() -> None:
    events, mk = load()
    rw = rows(mk)
    gate_ev = [
        e for e in events
        if e[2] == "elim" and e[0] in TEAM and e[1] >= GATE[0].toordinal() - 1
    ]  # fmt: skip
    dz = doses(mk, rw, events)
    n_ev = int(sum(v.sum() for v in dz.values()))
    print(f"rows {sum(len(r[0]) for r in rw.values())} in {len(rw)} markets")
    print(f"eliminations of mapped teams 2006-2025: {len(gate_ev)}; on gate rows: {n_ev}")
    print("by team:", dict(Counter(e[0] for e in gate_ev).most_common()))
    print("by tournament-year:", dict(Counter(
        f"{'WC' if e[4].startswith('FIFA') else 'EU'}{date.fromordinal(e[1]).year}"
        for e in gate_ev)))  # fmt: skip
    print("round of elimination (match number):", dict(Counter(e[3] for e in gate_ev)))
    a1 = e24.acf1(list(dz.values()))
    print(f"pooled dose acf1 {a1:+.3f}")
    if DRY:
        return
    b, t, n = fit(rw, dz)
    pl = [fit(rw, doses(mk, rw, events, shift=k))[1] for k in ev.W18_SHIFTS]
    rk = ev.rank_lowest(t, pl)
    sd, share, q5, q50, q95, lo, hi = ev.null_spread(pl)
    ok = b < 0 and t <= -2 and rk <= 2
    rw2 = rows(mk, after=1)
    cells = [
        ("Round weight (match number - 3)", fit(rw, doses(mk, rw, events, weight="round"))),
        ("Group-stage exits", fit(rw, doses(mk, rw, events, kind="group"))),
        ("Knockout wins (placebo dose, predicted 0)", fit(rw, doses(mk, rw, events, kind="win"))),
        ("Own return, no world subtraction", fit(rw, dz, outcome=2)),
        ("World Cup only", fit(rw, doses(mk, rw, events, only="FIFA World Cup"))),
        ("Two sessions (s0-1 close to s0+1 close)", fit(rw2, doses(mk, rw2, events))),
    ]
    big = []
    for name, r in rw.items():
        for j in np.nonzero(dz[name])[0]:
            big.append((abs(r[1][j]), name, date.fromordinal(int(r[3][j])), r[1][j]))
    big.sort(reverse=True)
    lines = [
        "# W18 `elimination-mood` (record-closing check): results",
        "",
        "Rule: [`cards/wide-26b.md`](../cards/wide-26b.md) (pushed before the match file was",
        "fetched and before any return). Code: `research/lib/wide26_w18.py`,",
        "`research/lib/wide26_events.py`. Outcome: the losing country's index log return on the",
        "first session after the match day, minus the other cached markets' mean change; market",
        "dummies; Driscoll-Kraay 5 lags; rows 2006-01-01 .. 2025-10-31.",
        "",
        f"- Eliminations of mapped teams: {len(gate_ev)} ({n_ev} on gate rows); pooled dose acf1 "
        f"{a1:+.3f} ('both families' rule does not apply).",
        f"- **b {100 * b:+.3f}% per elimination, DK t {t:+.2f}, {n} rows; rank {rk} of 41 "
        f"shifted calendars (lowest = 1).**",
        f"- Null: SD {sd:.2f}, {share:.0%} past |t| 2, 5/50/95% {q5:+.2f} / {q50:+.2f} / "
        f"{q95:+.2f}, extremes {lo:+.2f} / {hi:+.2f}.",
        f"- **Verdict: {'PASS (kill-only)' if ok else 'FAIL'}.** "
        f"{'Run R18 next.' if ok else 'R18 not run (the card runs it only after a pass).'}",
        "",
        "## Shown cells (not gating)",
        "",
        "| Cell | b, % | t | Rows |",
        "|---|---:|---:|---:|",
        f"| **Gate** | **{100 * b:+.3f}** | **{t:+.2f}** | **{n}** |",
        *[f"| {c} | {100 * v[0]:+.3f} | {v[1]:+.2f} | {v[2]} |" for c, v in cells],
        "",
        "## Eliminations by team (2006-2025)",
        "",
        ", ".join(f"{k} {v}" for k, v in Counter(e[0] for e in gate_ev).most_common()),
        "",
        "## The five largest |y| event sessions",
        "",
        "| Market | Session | y, % |",
        "|---|---|---:|",
        *[f"| {m} | {d} | {100 * y:+.2f} |" for _, m, d, y in big[:5]],
        "",
    ]
    print("\n".join(lines))
    (RESULTS / "elimination-mood.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
