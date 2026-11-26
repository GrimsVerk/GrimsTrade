"""Offline tests for research/lib/wide30.py (W47 `payout-ratio`)."""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "research" / "lib"))

import wide30 as w  # type: ignore[import-not-found]  # noqa: E402


def test_parse_shiller_keeps_positive_d_and_e_only() -> None:
    rows: list[list[object]] = [
        ["Date", "P", "D", "E"],
        [1871.01, 4.44, 0.26, 0.4],
        [1871.1, 4.5, 0.26, 0.0],  # zero E: missing
        [1871.11, 4.5, "", 0.4],  # blank D: missing
        [1871.12, 4.5, 0.3],  # short row
    ]
    out = w.parse_shiller(rows)
    assert list(out) == [w.mi(1871, 1)]
    assert math.isclose(out[w.mi(1871, 1)], math.log(0.26 / 0.4))


def test_parse_shiller_reads_october_as_month_10() -> None:
    out = w.parse_shiller([[1990.1, 300.0, 10.0, 20.0]])
    assert list(out) == [w.mi(1990, 10)]


def test_detrend_uses_past_only_and_needs_full_base() -> None:
    p = {m: float(m) for m in range(100)}
    h = w.detrend(p, base=10)
    assert min(h) == 10
    assert math.isclose(h[10], 10 - 4.5)  # mean of 0..9
    gap = dict(p)
    del gap[50]
    assert 55 not in w.detrend(gap, base=10)


def test_reindex_moves_entry_to_m_plus_4() -> None:
    assert w.reindex({5: 1.0}) == {8: 1.0}
    assert w.mi(1991, 1) + 3 == w.ROW_FIRST


def test_pass_rule_and_rank() -> None:
    assert w.passes_pos(1.0, 2.5, 1, 2)
    assert w.passes_pos(1.0, 2.5, 2, None)
    assert not w.passes_pos(1.0, 1.9, 1, 1)
    assert not w.passes_pos(-1.0, 2.5, 1, 1)
    assert not w.passes_pos(1.0, 2.5, 1, 3)
    assert w.pos_rank(3.0, [1.0, 2.0, 4.0]) == 2
