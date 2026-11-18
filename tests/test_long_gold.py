"""datahub gold loader reads monthly prices, refuses gaps, and finds the newest snapshot."""

from __future__ import annotations

import importlib.util
import shutil
import sys
from datetime import date
from pathlib import Path
from types import ModuleType

import pytest

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "research" / "lib" / "long_gold.py"
FIXTURE = ROOT / "tests" / "fixtures" / "gold_monthly.csv"


@pytest.fixture(scope="module")
def lg() -> ModuleType:
    spec = importlib.util.spec_from_file_location("long_gold_under_test", PATH)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_load_and_returns(lg: ModuleType) -> None:
    px = lg.load(FIXTURE)
    assert px[0] == (date(1970, 11, 1), 37.0)
    assert px[-1] == (date(1971, 3, 1), 39.0)
    assert len(px) == 5
    r = lg.returns(px, since=lg.FREE_FROM)
    assert [d for d, _ in r] == [date(1971, 1, 1), date(1971, 2, 1), date(1971, 3, 1)]
    assert [g for _, g in r] == pytest.approx([38 / 37, 39 / 38, 1.0])


def test_parse_rejects_gap_and_bad_header(lg: ModuleType) -> None:
    with pytest.raises(ValueError):
        lg.parse(["Date,Price", "1971-01,38", "1971-03,39"])
    with pytest.raises(ValueError):
        lg.parse(["month,usd", "1971-01,38"])


def test_latest_snapshot(lg: ModuleType, tmp_path: Path) -> None:
    for day in ("2026-01-02", "2026-11-18"):
        (tmp_path / "datahub-gold" / day).mkdir(parents=True)
        shutil.copy(FIXTURE, tmp_path / "datahub-gold" / day / "monthly.csv")
    assert lg.latest(tmp_path) == tmp_path / "datahub-gold" / "2026-11-18" / "monthly.csv"
