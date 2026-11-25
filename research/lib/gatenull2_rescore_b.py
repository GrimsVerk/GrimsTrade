"""Lane gate-null-2, Part 3 (research/cards/gate-null-2.md), group b: descriptive re-score of
gates W29, W30 (wide17), W31 (wide20), W34 (panicwords1), W35 (wide21), weather-1 and weather-2
under phase-randomised (F2) and IAAFT (F3) surrogates of each gate's dose. No new verdict.

Each gate's true t and its own 40 placebos are rebuilt through the gate's own fit function
(checked against the stored t and rank); then each of 40 surrogate doses goes through the same
fit at k = 0 in place of the dose. Reads existing caches only (no download); train bars only;
never writes a gate's own result file.

Run:  `uv run python -I research/lib/gatenull2_rescore_b.py [GATE ...]`
Output: research/results/gate-null-2-rescore/<gate>.json
"""

from __future__ import annotations

import json
import math
import sys
from collections.abc import Callable, Mapping
from datetime import date
from pathlib import Path
from typing import Any

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gatenull2 as g  # noqa: E402
import harness  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "results" / "gate-null-2-rescore"
TOL = 0.02


def finish(
    gate: str,
    design: str,
    sign: int,
    stored_t: float,
    stored_rank: int,
    true_t: float,
    shift_t: list[float],
    fit_dose: Callable[[dict[Any, float]], float],
    dose: Mapping[Any, float],
    note: str = "",
) -> dict[str, Any]:
    """Check the rebuild, fit the 40 F2 and 40 F3 surrogates, write the JSON record."""
    rank = int(g.rank_high(sign * true_t, sign * np.asarray(shift_t)))
    clean = {k: v for k, v in dose.items() if v == v and math.isfinite(v)}
    ok = abs(true_t - stored_t) <= TOL and rank == stored_rank
    if not ok:
        rec: dict[str, Any] = {
            "gate": gate,
            "reproduced": False,
            "note": f"rebuild t {true_t:+.3f} (stored {stored_t:+.2f}), shift rank {rank}"
            f" (stored {stored_rank}); not re-scored. {note}",
        }
    else:
        phase_t = [fit_dose(s) for s in g.surrogate_doses(clean, "phase")]
        iaaft_t = [fit_dose(s) for s in g.surrogate_doses(clean, "iaaft")]
        keys = sorted(clean)
        rec = g.rescore_record(
            gate,
            design,
            sign,
            stored_t,
            stored_rank,
            true_t,
            shift_t,
            phase_t,
            iaaft_t,
            [clean[k] for k in keys],
            note,
        )
        rec["reproduced"] = True
        rec["dose_span"] = [str(keys[0]), str(keys[-1])]
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{gate}.json").write_text(json.dumps(rec, indent=1))
    return rec


def _px(syms: list[str], last: date) -> dict[str, Any]:
    import wide13_events as e13

    hist = harness.load_history("train", syms=syms)
    return {
        s: e13.Closes({b.date: b.close for b in bars if b.date <= last}) for s, bars in hist.items()
    }


# ---------------------------------------------------------------- W29, W30 (wide17)


def w29() -> dict[str, Any]:
    import wide17 as w
    import wide17_events as ev

    px = _px(["SPY"], w.LAST)
    d = ev.temp_dose(w.load_gistemp())
    lo, hi = ev.month_index(date(1993, 2, 1)), ev.month_index(date(2025, 10, 1))
    months = list(range(lo - 2, hi - 1))

    def y(s: str, m: Any) -> float:
        return ev.month_return(px[s], int(m) + 1, int(m) + 2, w.LAST)

    def per(m: Any) -> int:
        return int(m)

    def tfit(src: Mapping[int, float], k: int = 0) -> float:
        return w.fit(["SPY"], months, y, [lambda m: ev.shifted_month(src, int(m), k)], per, 3)[1]

    t = tfit(d)
    shift_t = [tfit(d, k) for k in ev.SHIFTS_W29]
    return finish(
        "W29",
        "SPY month m+2 log return on GISTEMP 12-month anomaly minus prior decade, NW 3, outcome"
        " months 1993-02..2025-10; surrogates of the whole monthly dose series (1890s-2025)",
        1,
        1.63,
        9,
        t,
        shift_t,
        tfit,
        d,
    )


def w30() -> dict[str, Any]:
    import wide13_events as e13
    import wide17 as w
    import wide17_events as ev

    px = _px(["SPY"], w.LAST)
    days = w.load_don()
    weeks = e13.fridays(date(2004, 1, 9), w.LAST)
    x = ev.outbreak_dose(ev.weekly_counts(days, weeks))
    gate_dates = e13.fridays(date(2005, 1, 7), date(2025, 9, 26))
    ref = date(2005, 1, 7)

    def per(f: Any) -> int:
        return round((f - ref).days / 7)

    def y(s: str, f: Any) -> float:
        return e13.window_return(px[s], f, 3, 31, 7, w.LAST)

    def tfit(src: Mapping[date, float], k: int = 0) -> float:
        return w.fit(["SPY"], gate_dates, y, [lambda f: e13.shifted(src, f, k)], per, 4)[1]

    t = tfit(x)
    shift_t = [tfit(x, k) for k in e13.SHIFTS]
    return finish(
        "W30",
        "SPY 4-week return (F+3..F+31) on detrended Anscombe count of WHO outbreak reports, NW 4,"
        " Fridays 2005-01..2025-09; surrogates of the weekly dose series (2005-2025)",
        1,
        1.68,
        9,
        t,
        shift_t,
        tfit,
        x,
        "the 2021-06-11 re-dating spike (wide-17 erratum) is kept: IAAFT moves it to a random week",
    )


# ---------------------------------------------------------------- W31 (wide20)


def w31() -> dict[str, Any]:
    import wide20 as w
    import wide20_events as ev

    events = w.load_events()
    hist = harness.load_history("train", syms=["SPY"])
    sym, lo, hi = w.GATE
    spy = w.Series(hist[sym], lo, hi)
    gate_ev = ev.in_window(events, spy.lo, spy.hi)
    t = w.fit(spy, gate_ev)[1]
    shift_t = w.placebos(spy, gate_ev)
    x = ev.dose(spy.dates, gate_ev)
    dose = {i: float(v) for i, v in enumerate(x)}

    def tfit(src: Mapping[int, float]) -> float:
        arr = np.array([src[i] for i in range(len(x))])
        return ev.ols_hc1(arr, spy.r)[1]

    return finish(
        "W31",
        "SPY daily return on log2(deaths/25) of aviation accidents (>= 50 deaths) on days 0-1,"
        " HC1, 4,488 sessions 2008-2025: the dose as a daily series on SPY's bar calendar (0 on"
        " non-event bars), surrogates of that series, refit with the gate's own ols_hc1",
        -1,
        -0.59,
        10,
        t,
        shift_t,
        tfit,
        dose,
        "phase surrogates smear the spikes into a Gaussian-like series; IAAFT keeps the zeros and"
        " spike values (but not the days-0-1 pairing exactly)",
    )


# ---------------------------------------------------------------- W34 (panicwords1)


def w34() -> dict[str, Any]:
    import panicwords1 as w
    import panicwords1_events as ev

    counts = w.load_counts()
    mkt = w.load_market()
    months = list(range(w.GATE[0], w.GATE[1] + 1))
    arts = {m: v["articles"] for m, v in counts.items()}
    d = ev.dose(arts, {m: v["panic"] for m, v in counts.items()})
    y = {m: mkt[m + 1][0] for m in months if m + 1 in mkt}
    c1 = {m: mkt[m][0] for m in months if m in mkt}
    c12 = {m: ev.past_return(mkt, m, 12, 1) for m in months}
    v = {m: mkt[m][1] for m in months if m in mkt}
    ctrl = [c1, c12, v]

    def tfit(src: dict[int, float]) -> float:
        return w.fit(months, y, src, ctrl)[1]

    t = tfit(d)
    shift_t = [tfit(w.shifted(d, k)) for k in ev.SHIFTS_W34]
    return finish(
        "W34",
        "French market next month on detrended ln share of newspaper articles with 'panic', three"
        " price controls, NW 3, dose months 1927-07..1963-12; surrogates of the monthly dose"
        " series (1925-1963), controls unchanged",
        -1,
        1.19,
        37,
        t,
        shift_t,
        tfit,
        d,
    )


# ---------------------------------------------------------------- W35 (wide21)


def w35() -> dict[str, Any]:
    import wide21 as w
    import wide21_events as ev

    sn, sh = w.load()
    x = ev.trailing_dose(sn)
    lo = ev_month(1871)

    def y1(m: int) -> float:
        return ev.shiller_return(sh, m, 1)

    months = [m for m in range(lo, max(sh) + 1) if not math.isnan(y1(m))]

    def tfit(src: Mapping[int, float], k: int = 0) -> float:
        return w.fit(months, y1, lambda m: ev.shifted(src, m, k), 12)[1]

    t = tfit(x)
    shift_t = [tfit(x, k) for k in ev.SHIFTS]
    return finish(
        "W35",
        "Shiller S&P 500 next month on trailing 12-month mean sunspot number, NW 12, dose months"
        " 1871-01..2023-07; surrogates of the whole monthly dose series (1749-2025)",
        -1,
        -0.87,
        3,
        t,
        shift_t,
        tfit,
        x,
        "the dose is cyclic (about 132 months): phase surrogates keep the spectral peak with a"
        " random phase, which is the family wide-21 asked for",
    )


def ev_month(year: int) -> int:
    import wide17_events as e17

    return e17.month_index(date(year, 1, 1))


# ---------------------------------------------------------------- weather-1, weather-2


def weather1() -> dict[str, Any]:
    import macro
    import weather1_events as ev
    import weather1_hdd as w

    root = macro.cache_root() / "weather-1"
    design = w.Design(w.load_hdd(root / "cpc-dd"))
    ung = w.load_ung(root / "yahoo" / "UNG.json")
    perms = ev.derangements(len(w.WINTERS), w.N_PLACEBO)
    t = design.fit(ung)[1]
    shift_t = [design.fit(ung, p)[1] for p in perms]
    orig = dict(design.x)

    def tfit(src: dict[date, float]) -> float:
        design.x = {f: src.get(f, math.nan) for f in orig}
        try:
            return design.fit(ung)[1]
        finally:
            design.x = orig

    return finish(
        "weather-1",
        "UNG next-5-session return on the gas-weighted 7-day HDD surprise, HC1, Fridays of 18"
        " winters 2007-08..2024-25: surrogates of the in-season Friday dose series, winters"
        " concatenated in time order (the summer gaps are not in the series)",
        1,
        -0.29,
        19,
        t,
        shift_t,
        tfit,
        orig,
        "shift_t here are the gate's own 40 winter derangements, not shifted calendars",
    )


def weather2() -> dict[str, Any]:
    import macro
    import weather1_events as ev1
    import weather2_rev as w

    root = macro.cache_root()
    raw = json.loads((root / "weather-2" / "k-cache.json").read_text())
    val = {ld: {date.fromisoformat(d): v for d, v in m.items()} for ld, m in raw["val"].items()}
    k = w.combine(val, ("610", "814"))
    ung = w.load_ung(root / "weather-1" / "yahoo" / "UNG.json")
    design = w.Design(k, ung.days)
    perms = ev1.derangements(len(w.WINTERS), w.N_PLACEBO)
    t = design.fit(ung)[1]
    shift_t = [design.fit(ung, w.y_primary, p)[1] for p in perms]
    orig = dict(design.x)

    def tfit(src: dict[date, float]) -> float:
        design.x = {s: src.get(s, math.nan) for s in orig}
        try:
            return design.fit(ung)[1]
        finally:
            design.x = orig

    return finish(
        "weather-2",
        "UNG open-to-close on the change of a gas-weighted CPC 6-10/8-14 day cold-outlook index,"
        " HC1, 1,327 sessions of 13 winters 2012-13..2024-25: surrogates of the in-season session"
        " dose series, winters concatenated in time order",
        1,
        -0.68,
        36,
        t,
        shift_t,
        tfit,
        orig,
        "shift_t here are the gate's own 40 winter derangements, not shifted calendars",
    )


GATES: dict[str, Callable[[], dict[str, Any]]] = {
    "W29": w29,
    "W30": w30,
    "W31": w31,
    "W34": w34,
    "W35": w35,
    "weather-1": weather1,
    "weather-2": weather2,
}


def main() -> None:
    which = sys.argv[1:] or list(GATES)
    for name in which:
        try:
            r = GATES[name]()
        except FileNotFoundError as e:
            OUT.mkdir(parents=True, exist_ok=True)
            r = {"gate": name, "reproduced": False, "note": f"cached input missing: {e}"}
            (OUT / f"{name}.json").write_text(json.dumps(r, indent=1))
        if r.get("reproduced"):
            print(
                f"{name}: t {r['true_t']:+.2f} stored rank {r['stored_rank']} shift"
                f" {r['shift_rank']} phase {r['phase_rank']} iaaft {r['iaaft_rank']}"
                f" acf1 {r['dose_acf1']:.3f} N_eff {r['dose_neff']:.0f}"
                f" phase sd {r['phase_null']['sd']:.2f} iaaft sd {r['iaaft_null']['sd']:.2f}"
                f" shift sd {r['shift_null']['sd']:.2f}",
                flush=True,
            )
        else:
            print(f"{name}: NOT re-scored: {r['note']}", flush=True)


if __name__ == "__main__":
    main()
