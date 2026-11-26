"""w41-neg-1 (`cabinet-drift`): annual dose, demeaning, rows, statistic and verdict, offline."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))
import w41neg1 as w  # type: ignore[import-not-found]  # noqa: E402


def test_dose_years_marks_event_years_from_first_cabinet_to_end() -> None:
    z = w.dose_years({"A": [1922, 1922, 1925]}, {"A": 1920, "B": 1921}, ["A", "B", "C"], end=1926)
    assert sorted(z) == ["A", "B"]  # C has no cabinet data: no dose
    assert z["A"] == {1920: 0, 1921: 0, 1922: 1, 1923: 0, 1924: 0, 1925: 1, 1926: 0}
    assert set(z["B"].values()) == {0.0}
    zc = w.dose_years({"A": [1922, 1922]}, {"A": 1920}, ["A"], end=1923, count=True)
    assert zc["A"][1922] == 2.0


def test_demean_removes_the_year_mean_over_present_countries() -> None:
    d = w.demean({"A": {1: 0.3, 2: 0.1}, "B": {1: 0.1}}, ["A", "B"])
    assert math.isclose(d["A"][1], 0.1) and math.isclose(d["B"][1], -0.1)
    assert d["A"][2] == 0.0  # alone in year 2


def test_rows_need_outcome_dose_and_three_control_years() -> None:
    d = {"A": {t: 0.0 for t in range(1918, 1925)}}
    z = {"A": {t: 0.0 for t in range(1920, 1925)}}
    rows = w.rows_for(d, z, ["A", "B"], [1920, 1921, 1922, 1925])
    assert rows == [("A", 1921), ("A", 1922)]  # 1920: no dose of 1919; 1925: no outcome


def _panel(beta: float, seed: int = 1) -> tuple[w.Panel, w.Panel, list[tuple[str, int]]]:
    rng = np.random.default_rng(seed)
    years = range(1900, 1960)
    z = {i: {t: float(rng.random() < 0.3) for t in years} for i in "ABCDE"}
    d = {i: {t: 0.0 for t in years} for i in "ABCDE"}
    for i in "ABCDE":
        for t in years:
            if t - 1 in z[i]:
                d[i][t] = beta * z[i][t - 1] + 0.05 * rng.standard_normal()
    return d, z, w.rows_for(d, z, list("ABCDE"), list(range(1905, 1960)))


def test_fit_recovers_a_planted_negative_effect_in_percent() -> None:
    d, z, rows = _panel(-0.05)
    f = w.fit(d, z, rows)
    assert f.n == len(rows)
    assert -6.5 < f.b < -3.5 and f.t < -3
    assert abs(w.fit(d, z, rows, k=3).t) < 3  # an earlier calendar carries no effect


def test_fit_returns_nan_with_too_few_rows() -> None:
    d, z, rows = _panel(0.0)
    assert math.isnan(w.fit(d, z, rows[:5]).b)


def test_rank_bootstrap_p_and_verdict() -> None:
    assert w.rank_low(-2.0, [-3.0, -1.0, math.nan, 0.0]) == 2
    assert w.boot_p(-2.0, [-3.0, -1.0, 0.0]) == 0.5
    good = w.Fit(-1.0, -2.5, 300)
    halves = [w.Fit(-0.5, -1.0, 150), w.Fit(-1.5, -2.0, 150)]
    assert w.verdict(good, 1, 0.01, halves).startswith("NOT DEAD YET")
    assert w.verdict(good, 3, 0.01, halves).startswith("DEAD")
    assert w.verdict(good, 1, 0.06, halves).startswith("DEAD")
    assert w.verdict(w.Fit(0.5, 2.5, 300), 1, 0.01, halves) == "DEAD (wrong sign: b >= 0)"
    assert w.verdict(good, 1, 0.01, [halves[0], w.Fit(0.1, 0.1, 150)]).startswith("DEAD")
