"""The evo-1 inputs are what the card says and see nothing after the decision.

- The grammar's `mom(365) > 0` gives exactly the harness `tsmom12` weights, and `gap(290) > 0`
  exactly `sma200`'s, on every Friday of a synthetic panel.
- Inputs of a Friday do not change when later bars are scrambled.
"""

from __future__ import annotations

import importlib
import math
import random
import sys
from collections.abc import Iterator
from datetime import date, timedelta
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

from grimstrade import data
from grimstrade.data import Bar

LIB = Path(__file__).resolve().parents[1] / "research" / "lib"
START = date(2019, 1, 1)
DAYS = 1100


@pytest.fixture(scope="module")
def lib() -> Iterator[dict[str, ModuleType]]:
    pytest.importorskip("numpy")
    saved_universe = dict(data.UNIVERSE)  # the research lib adds its own symbols on import
    saved_path = list(sys.path)
    sys.path.insert(0, str(LIB))
    names = ("harness", "common", "evo_gp", "evo_feat")
    yield {n: importlib.import_module(n) for n in names}
    data.UNIVERSE.clear()
    data.UNIVERSE.update(saved_universe)
    sys.path[:] = saved_path


def _bars(seed: int, first: int, weekends: bool, scramble_from: date | None = None) -> list[Bar]:
    rng = random.Random(seed)
    late = random.Random(seed + 1000)
    out, px = [], 100.0
    for k in range(first, DAYS):
        d = START + timedelta(days=k)
        if not weekends and d.weekday() >= 5:
            continue
        r = rng.gauss(0.0002, 0.02)
        if scramble_from is not None and d > scramble_from:
            r = late.gauss(0.0, 0.05)
        o = px * math.exp(rng.gauss(0, 0.004))
        px *= math.exp(r)
        out.append(Bar(d, o, max(o, px) * 1.001, min(o, px) * 0.999, px, 1.0))
    return out


def _history(scramble_from: date | None = None) -> dict[str, list[Bar]]:
    return {
        "BTC": _bars(1, 200, True, scramble_from),
        "SPY": _bars(2, 0, False, scramble_from),
        "GLD": _bars(3, 0, False, scramble_from),
        "TLT": _bars(4, 400, False, scramble_from),
    }


def _fridays() -> list[date]:
    days = [START + timedelta(days=k) for k in range(30, DAYS)]
    return [d for d in days if d.weekday() == 4]


def test_grammar_twins_equal_the_harness_rules(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    h, c, gp, ef = lib["harness"], lib["common"], lib["evo_gp"], lib["evo_feat"]
    panel = h.Panel(_history())
    fridays = _fridays()
    feats, elig = ef.friday_feats(panel, fridays)
    assert set(gp.INPUTS) <= set(feats)
    sma: Any = ("slot", ("if", ("gtc", ("gap", 290), 0.0), ("const", 1.0), ("const", 0.0)))
    for rule, signal in ((gp.TSMOM12, c.tsmom_signal), (sma, c.sma_signal)):
        w = gp.weights(rule, feats, elig)
        twin = c.slots(signal)
        held = 0
        for t, d in enumerate(fridays):
            want = twin(panel.view(h.decide_time(d)))
            got = {s: float(w[t, j]) for j, s in enumerate(panel.syms) if w[t, j] > 0}
            assert got == want, (d, got, want)
            held += len(want)
        assert held > 100  # the comparison is not empty
    assert elig[0].sum() == 0 and elig[-1].sum() == 4
    assert np.nanmin(feats[("dd", 91)]) <= np.nanmax(feats[("dd", 91)]) <= 0
    for name in ("rank", "breadth", "vrank", "vbreadth"):
        x = feats[(name, 61)][elig]
        assert np.nanmin(x) >= 0 and np.nanmax(x) <= 1


def test_inputs_do_not_see_later_bars(lib: dict[str, ModuleType]) -> None:
    import numpy as np

    h, ef = lib["harness"], lib["evo_feat"]
    cut = START + timedelta(days=800)
    fridays = [d for d in _fridays() if d <= cut]
    a, elig_a = ef.friday_feats(h.Panel(_history()), fridays)
    b, elig_b = ef.friday_feats(h.Panel(_history(scramble_from=cut)), fridays)
    assert np.array_equal(elig_a, elig_b)
    for key in a:
        assert np.array_equal(a[key], b[key], equal_nan=True), key
    later = [
        cut + timedelta(days=k) for k in range(1, 200) if (cut + timedelta(days=k)).weekday() == 4
    ]
    c2, _ = ef.friday_feats(h.Panel(_history()), later)
    d2, _ = ef.friday_feats(h.Panel(_history(scramble_from=cut)), later)
    assert not np.array_equal(c2[("mom", 30)], d2[("mom", 30)], equal_nan=True)  # the test bites
