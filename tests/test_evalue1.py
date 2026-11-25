"""The e-processes in research/evalue1.py compute what research/cards/evalue-forward-1.md says."""

from __future__ import annotations

import importlib
import math
import sys
from pathlib import Path
from typing import Any

import numpy as np

RESEARCH = Path(__file__).resolve().parents[1] / "research"


def _ev() -> Any:
    sys.path.insert(0, str(RESEARCH))
    try:
        return importlib.import_module("evalue1")
    finally:
        sys.path.remove(str(RESEARCH))


def test_phi_pos_matches_erf() -> None:
    ev = _ev()
    x = np.linspace(0, 8, 401)
    want = np.array([0.5 * (1 + math.erf(v / math.sqrt(2))) for v in x])
    assert np.max(np.abs(ev.phi_pos(x) - want)) < 2e-7


def test_mixture_closed_form_matches_the_integral() -> None:
    ev = _ev()
    tau = 0.05
    lam = np.linspace(0, 1.5, 300_001)
    dens = 2 / (tau * math.sqrt(2 * math.pi)) * np.exp(-(lam**2) / (2 * tau**2))
    for s, v in ((3.0, 400.0), (-2.0, 100.0), (25.0, 900.0), (0.0, 50.0)):
        integrand = np.exp(lam * s - lam**2 * v / 2) * dens
        num = float(np.sum((integrand[1:] + integrand[:-1]) / 2 * np.diff(lam)))
        got = float(ev.mixture_log_e(np.array([s]), np.array([v]), tau)[0])
        assert math.isclose(got, math.log(num), abs_tol=1e-5)


def test_ons_matches_a_scalar_reference_and_reports_crossings() -> None:
    ev = _ev()
    rng = np.random.default_rng(3)
    y = np.clip(rng.normal(0.15, 0.3, size=(3, 400)), -1, 1)
    first, best = ev.ons_log_wealth(y, (math.log(20), math.log(1e200)))
    for i in range(3):
        lam, a, logk, top, hit = 0.0, 1.0, 0.0, 0.0, math.inf
        for t, yt in enumerate(y[i]):
            assert 0.0 <= lam <= 0.5
            logk += math.log1p(lam * yt)
            g = yt / (1 + lam * yt)
            a += g * g
            lam = min(max(lam + 2 / (2 - math.log(3)) * g / a, 0.0), 0.5)
            top = max(top, logk)
            if logk >= math.log(20) and math.isinf(hit):
                hit = t + 1
        assert math.isclose(best[i], top, rel_tol=1e-9, abs_tol=1e-12)
        assert first[i, 0] == hit
        assert math.isinf(first[i, 1])  # 1e200 is out of reach in 400 weeks


def test_e_processes_keep_ville_bound_under_an_iid_symmetric_null() -> None:
    ev = _ev()
    rng = np.random.default_rng(11)
    x = rng.standard_t(5, size=(4000, 600)) / math.sqrt(5 / 3)  # mean 0, symmetric, fat tails
    th = (math.log(20),)
    f1, _ = ev.ons_log_wealth(np.clip(x / 5, -1, 1), th)
    f2 = ev.first_cross(ev.mixture_log_e(np.cumsum(x, 1), np.cumsum(x * x, 1)), th)
    assert np.isfinite(f1).mean() <= 0.05
    assert np.isfinite(f2).mean() <= 0.05
    # the naive weekly-peeking t-test does not keep its level
    t = ev.t_stats(x)
    t[:, :1] = -np.inf
    assert (t >= 1.645).any(axis=1).mean() > 0.2


def test_t_stats_match_the_textbook_formula() -> None:
    ev = _ev()
    x = np.array([[0.5, -0.2, 0.9, 0.1, 0.3]])
    t = ev.t_stats(x)
    for n in range(2, 6):
        v = x[0, :n]
        want = v.mean() / (v.std(ddof=1) / math.sqrt(n))
        assert math.isclose(t[0, n - 1], want, rel_tol=1e-12)
