"""rl-7 data: every long monthly series the project has cached, as monthly return segments.

Card: research/cards/rl-7.md. No rule, learner or statistic here: only loading. Sources (all
already in the local cache, nothing fetched):

- pooled-1's 41 stock markets (`pooled1.load_all`: French US 10 industries daily from 1926, 23
  Yahoo country indices, 8 ETFs), month-end closes, signal gap 0.
- pooled-2's non-equity series (`pooled2.load_nonequity`): 3 US Treasury rebuilds and 8 G10
  currencies (daily, month-end levels of the excess-return index, gap 1 because H.15/H.10
  values are public a day to a week later), 9 foreign 10-year bonds, the euro, 7 PPI commodity
  indices and gold (monthly, pooled-2's own gaps).
- e4-indep-1's stock markets (`e4indep1.PRIMARY`, `SECONDARY`): US 1871-1927 (Shiller), GB, DE,
  FR before 1927 (NBER), and DK, FI, IE, NO, SE (French country files, 1975 on).

Nothing after 2025-10 is read (each loader cuts there).
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import e4indep1_data as ed  # noqa: E402

LAST_K = ed.mi(2025, 10)
COST = {"equity": 0.0002, "rates": 0.0002, "fx": 0.0003, "commodity": 0.0010}


@dataclass
class Series:
    """One market. Each segment is (first month index, returns): r[i] is the return of month
    first + i; segments are runs of consecutive months."""

    name: str
    group: str
    cls: str
    gap: int
    segs: list[tuple[int, np.ndarray]] = field(default_factory=list)

    @property
    def cost(self) -> float:
        return COST[self.cls]

    def months(self) -> int:
        return sum(len(r) for _, r in self.segs)


def month_end_levels(days: np.ndarray, px: np.ndarray) -> dict[int, float]:
    """{month index: last level in that month} from day ordinals and levels; through LAST_K."""
    out: dict[int, float] = {}
    for o, p in zip(days, px, strict=True):
        d = date.fromordinal(int(o))
        k = ed.mi(d.year, d.month)
        if k <= LAST_K and np.isfinite(p) and p > 0:
            out[k] = float(p)  # days are in order: the last one wins
    return out


def segs_from_levels(lv: dict[int, float]) -> list[tuple[int, np.ndarray]]:
    out = []
    for run in ed.segments(lv):
        if len(run) < 2:
            continue
        v = np.array([x for _, x in run])
        out.append((run[1][0], v[1:] / v[:-1] - 1.0))
    return out


def segs_from_months(months: list[date], r: np.ndarray) -> list[tuple[int, np.ndarray]]:
    rets = {ed.mi(m.year, m.month): float(x) for m, x in zip(months, r, strict=True)}
    rets = {k: v for k, v in rets.items() if k <= LAST_K}
    return [
        (run[0][0], np.array([v - 1.0 for _, v in run]))
        for run in ed.segments({k: 1.0 + v for k, v in rets.items()})
    ]


def load_equity41() -> list[Series]:
    import pooled1

    out = []
    for name, group, days, px in pooled1.load_all():
        o = np.array([d.toordinal() for d in days])
        out.append(Series(name, group, "equity", 0, segs_from_levels(month_end_levels(o, px))))
    return out


def load_nonequity() -> list[Series]:
    import pooled2

    out = []
    for s in pooled2.load_nonequity():
        if s.freq == "w":
            assert s.d is not None and s.px_ret is not None
            segs = segs_from_levels(month_end_levels(s.d, s.px_ret))
            out.append(Series(s.name, s.group, s.cls, 1, segs))
        else:
            assert s.months is not None and s.r_ret is not None
            out.append(Series(s.name, s.group, s.cls, s.gap, segs_from_months(s.months, s.r_ret)))
    return out


def load_indep() -> list[Series]:
    import e4indep1 as e4
    import long_bond

    root = long_bond.cache_root()
    by: dict[str, Series] = {}
    for spec in [*e4.PRIMARY, *e4.SECONDARY]:
        name = f"{spec.market}-{'pre1927' if spec.group == 'P4' else 'french'}"
        s = by.setdefault(name, Series(name, spec.group, "equity", spec.gap))
        for seg in e4.load_segs(root, spec):
            k0 = ed.mi(seg.months[0].year, seg.months[0].month)
            r = np.array(seg.r)
            keep = [k0 + i <= LAST_K for i in range(len(r))]
            if any(keep):
                s.segs.append((k0, r[np.array(keep)]))
        # one gap per market: the largest of its segments' gaps (DE, FR mix 0 and 1)
        s.gap = max(s.gap, spec.gap)
    return list(by.values())


def load_all() -> list[Series]:
    return load_equity41() + load_nonequity() + load_indep()


def spans() -> None:
    """Print each series' span and month count (no returns, no statistic)."""
    tot = 0
    for s in load_all():
        lo = min(k for k, _ in s.segs)
        hi = max(k + len(r) - 1 for k, r in s.segs)
        n = s.months()
        tot += n
        print(
            f"{s.name:24s} {s.group:7s} {s.cls:9s} gap {s.gap} segs {len(s.segs)} "
            f"{ed.month_of(lo).isoformat()[:7]}..{ed.month_of(hi).isoformat()[:7]} months {n}"
        )
    print("total months", tot)


if __name__ == "__main__":
    spans()
