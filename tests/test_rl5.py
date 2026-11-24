"""The return-spread screen of run rl-5 does what the card says (research/rl-5.md).

- The book is +0.5 in the top third and -0.5 in the bottom third, nothing below 10 coins.
- A planted input earns its spread; its mirror image earns the same with the other sign.
- A book that does not change pays no cost after its first week.
- Holm's adjusted p-values are the textbook ones.
"""

from __future__ import annotations

import importlib
import sys
from collections.abc import Iterator
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"


@pytest.fixture(scope="module")
def scr() -> Iterator[ModuleType]:
    pytest.importorskip("numpy")
    pytest.importorskip("sklearn")
    saved = list(sys.path)
    sys.path.insert(0, str(LIB))
    yield importlib.import_module("rl5_screen")
    sys.path[:] = saved


def made_up(np: Any, weeks: int = 200, n: int = 30) -> tuple[Any, Any, Any, Any]:
    rng = np.random.default_rng(7)
    x = rng.standard_normal((weeks, n))
    fwd = np.log1p(0.01 * x + 0.05 * rng.standard_normal((weeks, n)))
    noise = rng.standard_normal((weeks, n))
    m = np.ones((weeks, n), bool)
    day = 1000 + 7 * np.arange(weeks)
    return day, m, fwd, np.stack([x, -x, noise], axis=2)


def test_third_book_is_half_long_half_short(scr: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    x = np.arange(12.0)
    x[5] = np.nan
    w = scr.third_book(x, np.ones(12, bool))
    assert w[w > 0].sum() == pytest.approx(0.5)
    assert w[w < 0].sum() == pytest.approx(-0.5)
    assert w[11] > 0 and w[0] < 0 and w[5] == 0
    assert (w > 0).sum() == 4  # a third of the 11 coins that have the input
    assert not scr.third_book(np.arange(9.0), np.ones(9, bool)).any()  # fewer than 10 coins


def test_unchanged_book_pays_only_once(scr: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    raw = np.tile(np.arange(12.0), (5, 1))
    gross, paid = scr.venue_weeks(raw, np.ones((5, 12), bool), np.zeros((5, 12)))
    assert paid[0] == pytest.approx(scr.COST)  # the whole book, gross exposure 1
    assert paid[1:] == pytest.approx(0.0)
    assert gross == pytest.approx(0.0)


def test_screen_finds_the_planted_input_and_its_sign(scr: ModuleType) -> None:
    np: Any = pytest.importorskip("numpy")
    day, m, fwd, raw = made_up(np)
    rows = scr.screen({"A": (day, m, fwd, raw), "B": (day + 0, m, fwd, raw)})["rows"]
    planted, mirror, noise = rows
    assert planted["sign"] == 1.0 and mirror["sign"] == -1.0
    assert planted["net"] == pytest.approx(mirror["net"])
    assert planted["gross"] > planted["net"] > 0  # costs are charged
    assert planted["pass"] and mirror["pass"] and not noise["pass"]
    assert planted["weeks"] == 200  # two venues on the same Fridays pool to one week each


def test_holm_adjusted_p(scr: ModuleType) -> None:
    assert scr.holm([0.01, 0.04, 0.03]) == pytest.approx([0.03, 0.06, 0.06])
    assert scr.holm([0.5, 0.9]) == pytest.approx([1.0, 1.0])
    assert scr.p_two_sided(-1.0) == 1.0
    assert scr.p_two_sided(1.96) == pytest.approx(0.05, abs=1e-3)
