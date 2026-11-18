"""Trend 1926: where the replay check's gaps come from, and what they could change.

    uv run python -I research/lib/trend_1926_gaps.py                  # era 1, 1927-1961
    TREND_ERA=1962 uv run python -I research/lib/trend_1926_gaps.py   # era 2, 1962-2001

A re-scoring only: the primary runs are rebuilt through `trend_1926.pair` (an equity file under
the git-ignored research/data/runs/trend-1926/ means no new `tries.md` row; without it the run
is logged as in `trend_1926.py`). For each series it lists the sessions where the gym's rule run
and trend-tune's gym-free paper series differ by more than 0.0001, shows the week's Friday and
whether that Friday was a session, and then re-scores every window with the gym's return on
those sessions replaced by the paper's. The ten-industry book has no paper series; there each
gap is added at a tenth of its size (slot drift ignored), an approximation.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import trend_1926 as t  # noqa: E402
import trend_tune as tt  # noqa: E402

TOL = 1e-4


def gaps(pr: t.Pair, u: t.c.Ctx, name: str) -> dict[date, tuple[float, float]]:
    """Session -> (gym return, paper return) wherever they differ by more than 1e-6."""
    p = tt.paper(u.panel, t.sym(name), (12,))
    eq = dict(zip(pr.rule.days, pr.rule.equity, strict=True))
    first = (t.START + timedelta(days=14)).toordinal()
    out = {}
    for i in range(1, len(p.ord)):
        d, dp = date.fromordinal(int(p.ord[i])), date.fromordinal(int(p.ord[i - 1]))
        if p.ord[i] <= first or d not in eq or dp not in eq:
            continue
        g, q = eq[d] / eq[dp] - 1, float(p.ret[12][i])
        if abs(g - q) > 1e-6:
            out[d] = (g, q)
    return out


def friday_of(d: date) -> date:
    return d - timedelta(days=(d.weekday() - 4) % 7)


def row(label: str, pr: t.Pair, rule_rets: np.ndarray) -> str:
    cells = []
    for w in t.WINDOWS:
        m = w.mask(t.day_ords(pr.rule))
        a = t.window_diff(pr, w)
        b = t.compare(rule_rets[m], pr.hold.rets[m])
        cells.append(f" {a.diff:+.3f} / {b.diff:+.3f} |")
    return f"| {label} |" + "".join(cells)


def main() -> None:
    raw = t.load()
    sessions = set(raw.days)
    series = [t.MKT, *t.INDUSTRIES]
    pairs: dict[str, t.Pair] = {}
    found: dict[str, dict[date, tuple[float, float]]] = {}
    for n in series:
        pairs[n], u = t.pair(raw, [n], n, "")
        found[n] = gaps(pairs[n], u, n)
    book, _ = t.pair(raw, t.INDUSTRIES, t.BOOK, "")

    out = ["Sessions where the gym and the paper series differ by more than 0.0001:", ""]
    out += ["| Series | Session | Week's Friday | Friday a session? | Gym | Paper | Gym - paper |"]
    out += ["|---|---|---|---|---:|---:|---:|"]
    big = 0
    for n in series:
        for d, (g, q) in sorted(found[n].items()):
            if abs(g - q) > TOL:
                big += 1
                fri = friday_of(d - timedelta(days=1))
                out.append(
                    f"| {t.sym(n)} | {d} {d:%a} | {fri} | {'yes' if fri in sessions else 'no'} | "
                    f"{g:+.4f} | {q:+.4f} | {g - q:+.4f} |"
                )
    rest = [abs(g - q) for f in found.values() for g, q in f.values() if abs(g - q) <= TOL]
    small = len(rest)
    fri, hol = friday_of(t.START + timedelta(days=6)), []
    while fri < raw.days[-1]:
        if fri not in sessions:
            hol.append(fri)
        fri += timedelta(days=7)
    out += [
        "",
        f"{big} such sessions in all; {small} more differ by 1e-6 to 1e-4 (largest "
        f"{max(rest, default=0):.6f}). Fridays without a "
        f"session after the first decision: {len(hol)}.",
        "",
        "Sharpe of the rule minus Sharpe of holding, as published / with the paper's return on "
        "the gap sessions:",
        "",
        "| Series |" + "".join(f" {w.key} |" for w in t.WINDOWS),
        "|---|" + "---:|" * len(t.WINDOWS),
    ]
    adj_book = book.rule.rets.copy()
    book_idx = {d: k for k, d in enumerate(book.rule.days[1:])}
    for n in series:
        r = pairs[n].rule.rets.copy()
        idx = {d: k for k, d in enumerate(pairs[n].rule.days[1:])}
        for d, (g, q) in found[n].items():
            r[idx[d]] = q
            if n != t.MKT:
                adj_book[book_idx[d]] += (q - g) / 10
        out.append(row(t.sym(n), pairs[n], r))
    out.append(row(f"{t.sym(t.BOOK)} (approx.)", book, adj_book))
    print("\n".join(out))


if __name__ == "__main__":
    main()
