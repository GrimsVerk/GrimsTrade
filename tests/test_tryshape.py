"""The shape (record length, skew, excess kurtosis) logged next to each harness try."""

from __future__ import annotations

import importlib.util
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from types import SimpleNamespace

import pytest

from grimstrade import data, returnstore, tryshape

ROOT = Path(__file__).resolve().parents[1]
ROW = "| 2026-11-19 01:00 | idea-x | v1 | variant | train | 1994-02-01 | 2025-11-09 | 0.50 |"


def weekday_curve(fridays: list[float]) -> tuple[list[date], list[float]]:
    """Bars on weekdays only; Friday k has equity fridays[k], other days drift. The second
    Friday has no bar (a holiday): Thursday's equity, set to the Friday value, carries over."""
    start = date(2025, 1, 3)  # a Friday
    days, eq = [], []
    for k, f in enumerate(fridays):
        fri = start + timedelta(days=7 * k)
        for j in range(-4, 1):
            d = fri + timedelta(days=j)
            if d < start or (k == 1 and j == 0):
                continue
            days.append(d)
            eq.append(f if j == 0 or (k == 1 and j == -1) else f * 0.97)
    return days, eq


def test_shape_of_a_two_point_return_series_matches_hand_values() -> None:
    # Returns +10%, -10%, +10%: a two-point law with p = 2/3 for the high value.
    days, eq = weekday_curve([100.0, 110.0, 99.0, 108.9])
    assert tryshape.weekly_returns(days, eq) == pytest.approx([0.1, -0.1, 0.1])
    s = tryshape.of_equity(days, eq)
    assert s is not None
    p = 2 / 3
    assert s.weeks == 3
    assert s.skew == pytest.approx((1 - 2 * p) / math.sqrt(p * (1 - p)), abs=1e-4)
    assert s.excess_kurtosis == pytest.approx((1 - 6 * p * (1 - p)) / (p * (1 - p)), abs=1e-4)
    sd = math.sqrt((2 * (0.1 - 1 / 30) ** 2 + (0.1 + 1 / 30) ** 2) / 3)
    assert s.sharpe_weekly == pytest.approx(1 / 30 / sd * math.sqrt(365.25 / 7), abs=1e-4)


def test_no_variation_or_too_short_logs_nothing(tmp_path: Path) -> None:
    flat_days = [date(2025, 1, 3) + timedelta(days=k) for k in range(30)]
    path = tmp_path / "shapes.jsonl"
    assert tryshape.log(path, ROW, flat_days, [1.0] * 30) is None
    assert tryshape.log(path, ROW, flat_days[:5], [1.0, 2, 3, 4, 5]) is None  # one Friday
    assert not path.exists()


def test_log_appends_and_read_joins_by_row_text(tmp_path: Path) -> None:
    path = tmp_path / "research" / "tries-shape.jsonl"
    days, eq = weekday_curve([100.0, 110.0, 99.0, 108.9])
    first = tryshape.log(path, ROW + "\n", days, eq)
    days2, eq2 = weekday_curve([100.0, 90.0, 99.0, 89.1, 95.0])
    other = ROW.replace("v1", "v2")
    second = tryshape.log(path, other, days2, eq2)
    lines = path.read_text().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["row"] == ROW  # stored stripped, as the register compares
    got = tryshape.read(path.read_text())
    assert got == {ROW: first, other: second}
    # Append-only: a later log never touches the earlier line.
    tryshape.log(path, ROW, days2, eq2)
    assert path.read_text().splitlines()[:2] == lines
    assert tryshape.read(path.read_text())[ROW] == first  # a re-run keeps the first line


def test_read_rejects_a_line_that_is_not_a_shape() -> None:
    with pytest.raises(ValueError, match="not a shape line"):
        tryshape.read('{"row": "| 2026 |"}\n', "x")
    with pytest.raises(ValueError, match="not a shape line"):
        tryshape.read("not json\n", "x")


def test_harness_log_writes_the_shape_next_to_the_row(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    np = pytest.importorskip("numpy")
    universe = dict(data.UNIVERSE)
    spec = importlib.util.spec_from_file_location(
        "harness_under_test", ROOT / "research" / "lib" / "harness.py"
    )
    assert spec is not None and spec.loader is not None
    harness = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = harness
    try:
        spec.loader.exec_module(harness)
        tries, shapes = tmp_path / "tries.md", tmp_path / "tries-shape.jsonl"
        monkeypatch.setattr(harness, "TRIES", tries)
        monkeypatch.setattr(harness, "SHAPES", shapes)
        store = tmp_path / "returns"
        monkeypatch.setattr(harness, "STORE", store)
        days, eq = weekday_curve([100.0, 110.0, 99.0, 108.9])
        full = [days[0] + timedelta(days=k) for k in range((days[-1] - days[0]).days + 1)]
        known = dict(zip(days, eq, strict=True))
        cur, filled = eq[0], []
        for d in full:
            cur = known.get(d, cur)
            filled.append(cur)
        run = harness.Run(
            "idea-x", "v1", "train", SimpleNamespace(turnover=0.5), full,
            np.array(filled) * 100, 1.0, [],
        )  # fmt: skip
        harness._log(run, "variant", date(1994, 2, 1), date(2025, 11, 9))
        row = tries.read_text().strip()
        got = tryshape.read(shapes.read_text())
        assert list(got) == [row]
        assert got[row] == tryshape.of_equity(days, eq)
        # register-5: the train try's weekly returns went into the store, family idea-x
        (stored,) = returnstore.read(store)
        assert [p.name for p in store.iterdir()] == ["idea-x.csv.gz"]
        assert (stored.source, stored.idea, stored.variant) == ("curve", "idea-x", "v1")
        assert f"| {stored.sharpe:.2f} |" in row
        want = returnstore.quantize(tryshape.weekly_returns(days, eq))
        assert list(stored.rets) == want
        # register-7: a robustness try is logged, but its returns are not stored by default
        robust = harness.Run(
            "idea-x", "v2", "train", SimpleNamespace(turnover=0.5), full,
            np.array(filled) * 101, 1.0, [],
        )  # fmt: skip
        harness._log(robust, "robustness", date(1994, 2, 1), date(2025, 11, 9))
        assert len(tries.read_text().splitlines()) == 2
        assert [r.variant for r in returnstore.read(store)] == ["v1"]
    finally:
        sys.modules.pop(spec.name, None)
        data.UNIVERSE.clear()
        data.UNIVERSE.update(universe)
