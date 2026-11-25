"""Lane gate-null-2, Part 3 (research/cards/gate-null-2.md): descriptive re-score of W32, R32
and W33 (parked-gates-1) under phase (F2) and IAAFT (F3) surrogate doses. No new verdict.

The regression is `parkedgates1.fit` (the gates' own code path); the dose closures below are
the gates' own (`at`, `regs`) with the dose dict as an argument. Dose files are untrusted
downloads in the shared cache: run with `python -I`.

Run:  `uv run python -I research/lib/gatenull2_rescore_c.py`
Output: research/results/gate-null-2-rescore/{W32,R32,W33}.json
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Callable, Mapping
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gatenull2 as g  # noqa: E402
import harness  # noqa: E402
import parkedgates1 as pg  # noqa: E402
import parkedgates1_events as ev  # noqa: E402
import wide13_events as e13  # noqa: E402
import wide17_events as e17  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "gate-null-2-rescore"
Col = Callable[[str, int], float]


def at(src: Mapping[int, float], k: int = 0) -> list[Col]:
    return [lambda _s, m: e17.shifted_month(src, m, k)]


def save(rec: dict[str, object]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{rec['gate']}.json").write_text(json.dumps(rec, indent=1) + "\n")
    keys = ("gate", "true_t", "stored_rank", "shift_rank", "phase_rank", "iaaft_rank")
    print({k: rec.get(k) for k in keys}, f"acf1 {rec['dose_acf1']:.3f}")


def w32(px: dict[str, e13.Closes]) -> None:
    pdsi = ev.parse_pdsi(pg._read(f"climdiv/{pg.SNAP}/climdiv-pdsist-v1.0.0-20261105"), pg.LAST)
    d = ev.drought_dose(pdsi)
    months = list(range(e17.month_index(date(2002, 7, 1)), e17.month_index(date(2025, 6, 1)) + 1))

    def y(s: str, m: int) -> float:
        return e17.month_return(px[s], m + 1, m + 4, pg.LAST)

    t = pg.fit(["TLT"], months, y, at(d), 3)[1]
    sh = [pg.fit(["TLT"], months, y, at(d, k), 3)[1] for k in e17.SHIFTS_W29]
    fam = {f: [pg.fit(["TLT"], months, y, at(s), 3)[1] for s in g.surrogate_doses(d, f)]
           for f in ("phase", "iaaft")}  # fmt: skip
    save(g.rescore_record(
        "W32", "TLT next quarter on -PDSI 2002-07..2025-06, NW 3; surrogates of the full "
        "monthly -PDSI series 1895-2025 (one dose dict)", -1, -3.71, 1, t, sh,
        fam["phase"], fam["iaaft"], [d[m] for m in sorted(d)],
    ))  # fmt: skip


def r32() -> None:
    pdsi = ev.parse_pdsi(pg._read(f"climdiv/{pg.SNAP}/climdiv-pdsist-v1.0.0-20261105"), pg.LAST)
    d = ev.drought_dose(pdsi)
    ye = ev.month_end_values(
        ev.parse_fred_daily(pg._read(f"fred/{pg.SNAP}/{pg.DGS10}.csv"), pg.LAST)
    )
    rep = list(range(e17.month_index(date(1962, 1, 1)), e17.month_index(date(2002, 3, 1)) + 1))

    def dy(_s: str, m: int) -> float:
        a, b = ye.get(m + 1), ye.get(m + 4)
        return math.nan if a is None or b is None else b - a

    t = pg.fit(["Y"], rep, dy, at(d), 3)[1]
    sh = [pg.fit(["Y"], rep, dy, at(d, k), 3)[1] for k in e17.SHIFTS_W29]
    fam = {f: [pg.fit(["Y"], rep, dy, at(s), 3)[1] for s in g.surrogate_doses(d, f)]
           for f in ("phase", "iaaft")}  # fmt: skip
    save(g.rescore_record(
        "R32", "10-year yield change m+1..m+4 on -PDSI 1962-01..2002-03, NW 3; surrogates of "
        "the full monthly -PDSI series (same dicts as W32)", 1, -0.19, 21, t, sh,
        fam["phase"], fam["iaaft"], [d[m] for m in sorted(d)],
    ))  # fmt: skip


def w33(px: dict[str, e13.Closes]) -> None:
    recv = ev.parse_fred(pg._read(f"fred/{pg.SNAP}/{pg.RECV}.csv"), pg.LAST)
    mv = ev.parse_fred(pg._read(f"fred/{pg.SNAP}/{pg.MV}.csv"), pg.LAST)
    sq = ev.susceptible_dose(recv, mv)
    s3 = ev.monthly_known(sq, 3)
    months = list(range(e17.month_index(date(1965, 1, 1)), e17.month_index(date(2025, 9, 1)) + 1))

    def r(sym: str, m: int) -> float:
        return e17.month_return(px[sym], m - 1, m, pg.LAST)

    def y(sym: str, m: int) -> float:
        return r(sym, m + 1)

    def regs(sm: Mapping[int, float], k: int = 0) -> list[Col]:  # the gate's own closures
        def f(a: str, m: int) -> float:
            return ev.fall(r(a, m))

        def s(_a: str, m: int) -> float:
            return e17.shifted_month(sm, m, k)

        def c(a: str, m: int) -> float:
            return e17.month_return(px[a], m - 13, m - 1, pg.LAST)

        return [lambda a, m: f(a, m) * s(a, m), f, s, c, lambda a, m: f(a, m) * c(a, m)]

    t = pg.fit(["GSPC"], months, y, regs(s3), 3)[1]
    sh = [pg.fit(["GSPC"], months, y, regs(s3, k), 3)[1] for k in ev.SHIFTS_W33]
    fam = {
        f: [pg.fit(["GSPC"], months, y, regs(ev.monthly_known(q, 3)), 3)[1]
            for q in g.surrogate_doses(sq, f)]
        for f in ("phase", "iaaft")
    }  # fmt: skip
    save(g.rescore_record(
        "W33", "GSPC next month, b3 of F x s with F, s, c, F c, NW 3, 1965-01..2025-09; "
        "surrogates of the quarterly s (1961-12 on), then made monthly with the 3-month release "
        "lag; F and the controls unchanged", 1, 0.05, 41, t, sh, fam["phase"], fam["iaaft"],
        [sq[q] for q in sorted(sq)],
    ))  # fmt: skip


def main() -> None:
    hist = harness.load_history("train", syms=["TLT", "GSPC"])
    px = {s: e13.Closes({b.date: b.close for b in bars if b.date <= pg.LAST})
          for s, bars in hist.items()}  # fmt: skip
    w32(px)
    r32()
    w33(px)


if __name__ == "__main__":
    main()
