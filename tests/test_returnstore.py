"""The committed weekly-returns store (`grimstrade.returnstore`, card research/register-4.md):
what is written reads back the same on any machine, byte for byte, and `research/register2.py`
gets the same series from the store as from the local caches it was exported from."""

from __future__ import annotations

import gzip
import importlib.util
import json
import math
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Any

import pytest

from grimstrade import returnstore
from grimstrade.returnstore import Row

ROOT = Path(__file__).resolve().parents[1]
FRIDAY = date(2012, 1, 6)


def fridays(n: int, first: date = FRIDAY) -> list[str]:
    return [(first + timedelta(days=7 * k)).isoformat() for k in range(n)]


def row(idea: str, variant: str, rets: list[float], source: str = "curve") -> Row:
    return Row.of(source, idea, variant, "2012-01-02", 0.123456789, fridays(len(rets)), rets)


def test_rows_read_back_rounded_to_a_millionth(tmp_path: Path) -> None:
    a = row("trend", "tsmom12, slow", [0.0123456789, -0.5, 0.0, float("nan"), float("inf")])
    b = row("live", "equal_weight", [1e-7, -4e-7, 6e-7], source="live@abc")
    returnstore.write(tmp_path, [a, b])
    got = {r.idea: r for r in returnstore.read(tmp_path)}
    assert got["trend"].variant == "tsmom12, slow"  # a comma survives the CSV
    assert got["trend"].sharpe == 0.123456789  # full precision: it decides the match
    assert got["trend"].rets[:3] == (0.012346, -0.5, 0.0)
    assert math.isnan(got["trend"].rets[3]) and got["trend"].rets[4] == math.inf
    assert got["live"].rets == (0.0, -0.0, 1e-6)
    assert got["live"].weeks() == fridays(3)
    assert {r.key() for r in got.values()} == {a.key(), b.key()}


def test_the_same_series_give_the_same_bytes(tmp_path: Path) -> None:
    rows = [row("trend", f"v{k}", [0.01 * k, -0.02, 0.03]) for k in range(5)]
    returnstore.write(tmp_path / "one", rows)
    returnstore.write(tmp_path / "two", [*reversed(rows), rows[0]])  # order, duplicates
    one = (tmp_path / "one" / "trend.csv.gz").read_bytes()
    assert one == (tmp_path / "two" / "trend.csv.gz").read_bytes()
    assert one[4:8] == b"\0\0\0\0"  # gzip timestamp zero
    text = gzip.decompress(one).decode()
    assert text.splitlines()[0] == ",".join(returnstore.HEADER)
    assert len(text.splitlines()) == 6


def test_write_keeps_exactly_the_families_given(tmp_path: Path) -> None:
    returnstore.write(tmp_path, [row("a", "x", [0.1]), row("b/c d", "y", [0.2])])
    assert sorted(p.name for p in tmp_path.iterdir()) == ["a.csv.gz", "b_c_d.csv.gz"]
    returnstore.write(tmp_path, [row("a", "x", [0.1])])
    assert [p.name for p in tmp_path.iterdir()] == ["a.csv.gz"]


def test_weeks_must_be_consecutive_fridays() -> None:
    with pytest.raises(returnstore.StoreError, match="consecutive Fridays"):
        Row.of("curve", "a", "x", "2012-01-02", 0.1, ["2012-01-06", "2012-01-20"], [0.1, 0.2])
    with pytest.raises(returnstore.StoreError, match="consecutive Fridays"):
        Row.of("curve", "a", "x", "2012-01-02", 0.1, ["2012-01-05"], [0.1])


def test_no_store_reads_empty(tmp_path: Path) -> None:
    assert returnstore.read(tmp_path / "missing") == []


def test_a_bad_file_is_refused(tmp_path: Path) -> None:
    tmp_path.joinpath("a.csv.gz").write_bytes(gzip.compress(b"wrong,header\n"))
    with pytest.raises(returnstore.StoreError, match="header"):
        returnstore.read(tmp_path)


def test_register2_reads_the_store_like_the_local_caches(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Export local series, delete the caches (a clean checkout): the same series, matched to
    the same register rows. A curve that fits no row stays out of the store."""
    pytest.importorskip("numpy")
    spec = importlib.util.spec_from_file_location("register2", ROOT / "research" / "register2.py")
    assert spec is not None and spec.loader is not None
    r2 = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = r2
    try:
        spec.loader.exec_module(r2)
        work, store, register = tmp_path / "work", tmp_path / "returns", tmp_path / "tries.jsonl"
        monkeypatch.setattr(r2, "WORK", work)
        monkeypatch.setattr(r2, "STORE", store)
        monkeypatch.setattr(r2, "REGISTER", register)

        def curve(variant: str, drift: float) -> Any:
            days = [date(2012, 1, 2) + timedelta(days=k) for k in range(400)]
            eq = [
                (d, 100 * (1 + drift) ** k * (1 + 0.01 * math.sin(k))) for k, d in enumerate(days)
            ]
            return r2.series_of("curve", "trend", variant, eq)

        fit, stray = curve("tsmom12", 0.0004), curve("other", 0.0002)
        base = curve("ew", 0.0003)
        base.source, base.idea = "harness@abc", "baselines"
        rows = [
            {"id": "a-1", "idea": "trend", "variant": "tsmom12", "kind": "variant",
             "period": "train", "from": "2012-01-02", "sharpe": round(fit.sharpe, 2)},
            {"id": "b-1", "idea": "baselines", "variant": "ew", "kind": "baseline",
             "period": "train", "from": "2012-01-02", "sharpe": round(base.sharpe, 2)},
        ]  # fmt: skip
        register.write_text("".join(json.dumps(x) + "\n" for x in rows))
        r2.save(work / "curves.jsonl", [fit, stray])
        r2.save(work / "baselines.jsonl", [base])

        local = r2.sources()
        assert len(r2.to_store(local[3], rows)) == 2  # not exported yet: the warning's count
        r2.export()
        stored = returnstore.read(store)
        assert sorted(r.variant for r in stored) == ["ew", "tsmom12"]
        with_local = r2.sources()
        for p in work.iterdir():
            p.unlink()
        clean = r2.sources()
        assert clean[3] == []
        for k in range(3):
            assert [s.to_json() for s in clean[k]] == [
                s.to_json() for s in with_local[k] if s.variant != "other"
            ]
        got = r2.match(clean[0], rows) | r2.match(clean[1], rows)
        assert {i: s.variant for i, s in got.items()} == {"a-1": "tsmom12", "b-1": "ew"}
        assert got["a-1"].rets == list(returnstore.quantize(fit.rets))
        before = {p.name: p.read_bytes() for p in store.iterdir()}
        r2.export()  # nothing new: the store is unchanged
        assert {p.name: p.read_bytes() for p in store.iterdir()} == before
    finally:
        sys.modules.pop(spec.name, None)
