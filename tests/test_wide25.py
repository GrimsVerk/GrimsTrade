"""wide-25 (W41 `cabinet-collapse`): parsing, events, dose, design and statistic, offline."""

from __future__ import annotations

import math
import sys
from datetime import date
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))
import wide25 as w  # type: ignore[import-not-found]  # noqa: E402

DAT = """
     Value-Weight Dollar Returns      All 4 Data Items Not Reqd
          Mkt   High    Low
197501   10.00   1.0   2.0
197502  -99.99   1.0   2.0
197503    5.00   1.0   2.0

     Value-Weight Local  Returns      All 4 Data Items Not Reqd
          Mkt   High    Low
197501    1.00   1.0   2.0
197502    2.00   1.0   2.0
"""


def test_parse_block_reads_the_named_monthly_block_and_skips_missing() -> None:
    usd = w.parse_block(DAT, 0)
    assert usd == {w.mi(1975, 1): 0.10, w.mi(1975, 3): 0.05}
    loc = w.parse_block(DAT, 1)
    assert loc == {w.mi(1975, 1): 0.01, w.mi(1975, 2): 0.02}
    assert w.parse_block(DAT, 0, last=w.mi(1975, 1)) == {w.mi(1975, 1): 0.10}


def row(
    cid: str, country: str, start: str, election: str, prev: str = "", caretaker: str = "0"
) -> dict[str, str]:
    return {
        "cabinet_id": cid,
        "country_name_short": country,
        "start_date": start,
        "election_date": election,
        "previous_cabinet_id": prev,
        "caretaker": caretaker,
    }


ROWS = [
    row("1", "AAA", "1990-01-10", "1990-01-01"),
    row("1", "AAA", "1990-01-10", "1990-01-01"),  # second party row of the same cabinet
    row("2", "AAA", "1991-05-03", "1990-01-01", "1"),  # mid-term change
    row("3", "AAA", "1994-02-01", "1994-01-20", "2"),  # after an election
    row("4", "AAA", "1994-06-01", "1994-01-20", "3", "1"),  # mid-term caretaker
    row("5", "AAA", "1998-01-20", "1998-01-20", "4", "1"),  # caretaker from election day
    row("6", "AAA", "1998-09-01", "1998-01-20", "5"),  # post-election formation
    row("7", "BBB", "1992-03-01", "1992-02-01", "99"),  # previous not in the file
]


def test_events_are_new_cabinets_in_the_same_parliament() -> None:
    cabs = w.parse_cabinets(ROWS)
    assert len(cabs) == 7
    ev = w.events(cabs)
    assert [c.cid for c in ev] == ["2", "4", "6"]
    assert [w.post_election(c, cabs) for c in ev] == [False, False, True]
    assert w.first_start(cabs) == {"AAA": w.mi(1990, 1), "BBB": w.mi(1992, 3)}


def test_dose_is_defined_from_first_start_and_marks_event_months() -> None:
    cabs = w.parse_cabinets(ROWS)
    ev = w.events(cabs)
    d = w.dose_months(ev, w.first_start(cabs), ["AAA", "BBB", "CCC"], end=w.mi(1999, 12))
    assert set(d) == {"AAA", "BBB"}
    a = d["AAA"]
    assert min(a) == w.mi(1990, 1) and max(a) == w.mi(1999, 12)
    assert a[w.mi(1991, 5)] == 1.0 and a[w.mi(1994, 6)] == 1.0 and a[w.mi(1998, 9)] == 1.0
    assert sum(a.values()) == 3.0
    assert sum(d["BBB"].values()) == 0.0


def test_excess_subtracts_the_mean_of_the_other_markets() -> None:
    rets = {"A": {0: 0.10, 1: 0.0}, "B": {0: 0.0, 1: 0.0}, "C": {0: 0.0}}
    e = w.excess(rets)
    la = math.log1p(0.10)
    assert math.isclose(e["A"][0], la)
    assert math.isclose(e["B"][0], -la / 2)
    assert math.isclose(e["A"][1], 0.0) and 1 not in e["C"]


def synthetic(
    effect: float, seed: int = 1
) -> tuple[dict[str, dict[int, float]], dict[str, dict[int, float]]]:
    """Two countries, 400 months; an event every 20 months in A; e = noise + effect spread
    over the six months after each event."""
    rng = np.random.default_rng(seed)
    dose = {c: dict.fromkeys(range(400), 0.0) for c in "AB"}
    for m in range(30, 380, 20):
        dose["A"][m] = 1.0
    e = {c: {m: float(rng.normal(0, 0.01)) for m in range(400)} for c in "AB"}
    for m, v in dose["A"].items():
        if v:
            for j in range(1, 7):
                e["A"][m + j] += effect / 6
    return e, dose


def test_fit_finds_a_planted_premium_and_its_sign() -> None:
    e, dose = synthetic(0.05)
    spec = w.Spec(first_row=12, last_dose=390)
    rows = w.base_rows(e, dose, spec)
    b, t, n = w.fit(rows, dose, w.Spec(first_row=12, last_dose=390, controls=False))
    assert n == len(rows) > 700
    assert 2.5 < b < 6.0 and t > 5  # overlapping windows of the D = 0 rows share the effect
    # the coefficient is plain OLS on D and the country dummies
    x = np.array([[dose[r[0]][r[1]], r[0] == "A", r[0] == "B"] for r in rows], dtype=float)
    beta = np.linalg.lstsq(x, 100 * np.array([r[2] for r in rows]), rcond=None)[0]
    assert math.isclose(b, beta[0], rel_tol=1e-9)
    # with the past-return controls (which partly overlap a planted run) the sign survives
    bc, tc, _ = w.fit(rows, dose, spec)
    assert bc > 2.0 and tc > 3
    # an earlier-dose shift that breaks the timing loses it
    bs, ts, ns = w.fit(rows, dose, spec, shift=9)
    assert abs(ts) < t and ns <= n


def test_fit_drops_rows_whose_shifted_dose_is_undefined() -> None:
    e, dose = synthetic(0.0)
    spec = w.Spec(first_row=12, last_dose=390)
    rows = w.base_rows(e, dose, spec)
    _, _, n0 = w.fit(rows, dose, spec)
    _, _, n1 = w.fit(rows, dose, spec, shift=50)
    assert n1 == n0 - 2 * (50 - 12)


def test_reaction_rows_use_the_event_month_and_the_one_before() -> None:
    e = {"A": {m: 0.0 for m in range(40)}}
    e["A"][20] = 0.03
    e["A"][19] = 0.01
    dose = {"A": dict.fromkeys(range(40), 0.0)}
    spec = w.Spec(reaction=True, first_row=1, last_dose=39)
    rows = {r[1]: r[2] for r in w.base_rows(e, dose, spec)}
    assert math.isclose(rows[20], 0.04) and math.isclose(rows[21], 0.03)


def test_surrogate_keeps_each_countrys_event_count_on_its_rows() -> None:
    e, dose = synthetic(0.0)
    spec = w.Spec(first_row=12, last_dose=390)
    rows = w.base_rows(e, dose, spec)
    s = w.surrogate(dose, rows, np.random.default_rng(0))
    n_true = sum(1 for r in rows if r[0] == "A" and dose["A"][r[1]] > 0)
    assert sum(s["A"].values()) == n_true and sum(s["B"].values()) == 0
    assert set(s["A"]) == {r[1] for r in rows if r[0] == "A"}


def test_shift_set_and_null_stats() -> None:
    assert len(w.SHIFTS) == 40 and all(k % 2 == 1 and k % 12 for k in w.SHIFTS)
    ns = w.null_stats([-2.5, 0.0, 1.0, 2.0, float("nan")])
    assert ns["n"] == 4 and ns["share2"] == 0.5 and ns["min"] == -2.5 and ns["max"] == 2.0


def test_month_index_round_trip() -> None:
    assert w.ym(w.mi(2022, 12)) == "2022-12"
    assert w.mi(1976, 1) - w.mi(1975, 12) == 1
    assert date(2022, 12, 1).month == 12
