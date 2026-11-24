"""gap-2002-1: `tsmom12` minus holding, 2002-01..2025-10, per series. Card: research/gap-2002-1.md.

    uv run python -I research/lib/gap2002.py

Descriptive re-score of insure-2 (French US market and 10 value-weighted industries, paper
series) and insure-3 (S&P 500 total return), with their own loaders. Per series and cash
convention (0, bills): the gap in log points a year, split by date into fall gain, rebound lag
and calm drag (insure-1's 25% / 25% zigzag and 365-day rebound), and insure-2's by-peak
accounting as a check. Writes research/results/gap-2002-1.md. Nothing after 2025-10-31 is parsed.
"""

from __future__ import annotations

import sys
from collections.abc import Sequence
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import harness  # noqa: E402

LO, HI = date(2002, 1, 1), date(2025, 10, 31)
YEARS = (HI - LO).days / 365.25  # insure-2's divisor
DOWN = UP = 0.25
REBOUND = 365
OUT = harness.RESEARCH / "results" / "gap-2002-1.md"


@dataclass
class Gap:
    g: float  # rule minus holding over the window, log points a year
    i: float  # by date: fall sessions
    b: float  # by date: rebound sessions
    c: float  # calm sessions (same in both readings)
    i_peak: float  # by peak (insure-2): episodes peaking in the window, in full
    b_peak: float
    cagr_gap: float  # CAGR hold - CAGR rule, simple points a year

    @property
    def peak_total(self) -> float:
        return self.i_peak + self.b_peak + self.c


def zigzag(px: np.ndarray, down: float, up: float) -> list[tuple[int, int]]:
    """Confirmed (peak, trough) index pairs (insure-1's zigzag)."""
    out: list[tuple[int, int]] = []
    falling, pk, tr = False, 0, 0
    for i in range(1, len(px)):
        if not falling:
            if px[i] > px[pk]:
                pk = i
            elif px[i] <= px[pk] * (1 - down):
                falling, tr = True, i
        else:
            if px[i] < px[tr]:
                tr = i
            elif px[i] >= px[tr] * (1 + up):
                out.append((pk, tr))
                falling, pk = False, i
    return out


def split(days: Sequence[date], hold: np.ndarray, rule: np.ndarray, lo: date = LO,
          hi: date = HI) -> Gap:  # fmt: skip
    """Simple returns per session (index 0 ignored) -> the window's gap and its parts."""
    hl = np.zeros(len(hold))
    hl[1:] = np.log1p(hold[1:])
    d = np.zeros(len(rule))
    d[1:] = 100 * (np.log1p(rule[1:]) - hl[1:])
    px = np.exp(np.cumsum(hl))
    cum = np.cumsum(d)
    ords = np.array([x.toordinal() for x in days])
    part = np.zeros(len(d), dtype=int)  # 0 calm, 1 fall, 2 rebound
    pairs = zigzag(px, DOWN, UP)
    i_pk = b_pk = 0.0
    for j, (a, b) in enumerate(pairs):
        e = int(np.searchsorted(ords, days[b].toordinal() + REBOUND, side="right")) - 1
        if j + 1 < len(pairs):
            e = min(e, pairs[j + 1][0])
        part[a + 1 : b + 1] = 1
        part[b + 1 : e + 1] = 2
        if lo <= days[a] <= hi:
            i_pk += float(cum[b] - cum[a])
            b_pk += float(cum[e] - cum[b])
    win = (ords >= lo.toordinal()) & (ords <= hi.toordinal())
    win[0] = False
    yrs = YEARS
    parts = [float(d[win & (part == k)].sum()) / yrs for k in (0, 1, 2)]
    k0 = int(np.argmax(win)) - 1  # the session before the window: the start level
    k1 = int(np.nonzero(win)[0][-1])
    cy = (days[k1] - days[k0]).days / 365.25
    cg_h = float(np.exp(hl[win].sum() / cy) - 1)
    cg_r = float(np.exp(np.log1p(rule[win]).sum() / cy) - 1)
    return Gap(float(d[win].sum()) / yrs, parts[1], parts[2], parts[0], i_pk / yrs, b_pk / yrs,
               100 * (cg_h - cg_r))  # fmt: skip


def french() -> list[tuple[str, list[date], np.ndarray, np.ndarray, np.ndarray]]:
    """insure-2 step 1's 11 series: name, days, holding, rule at cash 0, rule at bills."""
    import insure1 as i1
    import trend_1926 as t
    from macro import cache_root

    snap = sorted(p for p in (cache_root() / "french").iterdir() if p.is_dir())[-1]
    fac = t.parse_factors(i1._lines(snap / "F-F_Research_Data_Factors_daily_CSV.zip"), i1.LAST)
    ind = t.parse_industries(i1._lines(snap / "10_Industry_Portfolios_daily_CSV.zip"), i1.LAST)
    days = sorted(d for d in fac if d >= i1.FIRST)
    rf = {d: fac[d][1] for d in days}
    raw = [(t.MKT, days, np.array([fac[d][0] for d in days]))]
    for j, n in enumerate(t.INDUSTRIES):
        r = np.array([ind[d][j] for d in days])
        keep = ~np.isnan(r)
        raw.append((n, [d for d, ok in zip(days, keep, strict=True) if ok], r[keep]))
    out = []
    for n, dd, r in raw:
        s = i1.build(n, dd, r, rf, None)  # paper series only, as insure-2 step 1
        hold = np.zeros(len(s.px))
        hold[1:] = s.px[1:] / s.px[:-1] - 1
        out.append((n, s.days, hold, s.paper, s.paper + (1 - s.pos) * s.rf))
    return out


def spx() -> tuple[list[date], np.ndarray, np.ndarray, np.ndarray]:
    import insure3 as i3

    days, s, _, _ = i3.load()
    return days, s["hold"], s["trend@cash0"], s["trend"]


def row(name: str, g0: Gap, gb: Gap) -> str:
    return (
        f"| {name} | {g0.g:+.2f} | {gb.g:+.2f} | {g0.i:+.2f} | {g0.b:+.2f} | {g0.c:+.2f} | "
        f"{gb.i:+.2f} | {gb.b:+.2f} | {gb.c:+.2f} | {g0.i_peak:+.2f} | {g0.b_peak:+.2f} | "
        f"{g0.peak_total:+.2f} | {g0.cagr_gap:.2f} | {gb.cagr_gap:.2f} |"
    )


def mean_gap(gs: Sequence[Gap]) -> Gap:
    f = ("g", "i", "b", "c", "i_peak", "b_peak", "cagr_gap")
    return Gap(*[float(np.mean([getattr(x, k) for x in gs])) for k in f])


def main() -> None:
    head = [
        "| Series | Gap, cash 0 | Gap, bills | Fall I (0) | Rebound B (0) | Calm C (0) | "
        "Fall I (bills) | Rebound B (bills) | Calm C (bills) | By peak: I (0) | By peak: B (0) "
        "| By peak: total (0) | CAGR gap, pts (0) | CAGR gap, pts (bills) |",
        "|---|" + "---:|" * 13,
    ]
    fr = [(n, split(d, h, r0), split(d, h, rb)) for n, d, h, r0, rb in french()]
    sd, sh, s0, sb = spx()
    sp = ("S&P 500 TR (insure-3)", split(sd, sh, s0), split(sd, sh, sb))
    m11 = ("Mean, 11 French series", mean_gap([x[1] for x in fr]), mean_gap([x[2] for x in fr]))
    m10 = ("Mean, 10 industries", mean_gap([x[1] for x in fr[1:]]),
           mean_gap([x[2] for x in fr[1:]]))  # fmt: skip
    md = [
        "# gap-2002-1 results (generated by `research/lib/gap2002.py`; do not edit)",
        "",
        f"Window: returns of sessions {LO}..{HI}, Y = {YEARS:.2f} years. Every number is rule "
        "minus holding in log points a year (negative = the rule trails), except the CAGR "
        "columns (CAGR hold minus CAGR rule, simple points a year, positive = the rule trails). "
        "Fall I + rebound B + calm C = gap, by date. By peak = insure-2's accounting (episodes "
        "whose peak lies in the window, I and B in full; C the same). Falls: 25% / 25% zigzag on "
        "each series' own total-return index, rebound = 365 days after the trough or the next "
        "peak if earlier. French series: insure-2's paper series, bills = French RF. S&P 500 TR: "
        "insure-3's series, bills = `^IRX`.",
        "",
        *head,
        *[row(*x) for x in fr],
        row(*m10),
        row(*m11),
        row(*sp),
        "",
        "Check against insure-2 (2002-2025, cash 0, pooled by peak, -2.19): "
        f"{m11[1].peak_total:+.2f}.",
        "",
    ]
    OUT.write_text("\n".join(md))
    print("\n".join(md))


if __name__ == "__main__":
    main()
