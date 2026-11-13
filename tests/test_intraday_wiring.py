"""The finer-data collection is wired into the daily job without touching the record.

`run_daily --intraday DIR` runs in its own workflow step after the record is pushed; these tests
check that a crash there changes nothing in the record, that a rerun adds nothing, that nothing
that trades or scores reads the collected files, and the guard that keeps the Actions-cache store
from being replaced by a shorter copy.
"""

import inspect
import json
import os
import subprocess
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
from test_run_daily import fake_market

from grimstrade import intraday, run_daily

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src" / "grimstrade"
DAILY = ROOT / ".github" / "workflows" / "daily.yml"
STORE = ROOT / "scripts" / "intraday-store.sh"
NOW = datetime(2026, 11, 12, 22, 45, tzinfo=UTC)


def fake_intraday(url: str) -> bytes:
    """Coinbase candles, Yahoo hourly chart and Kraken funding for the hours before NOW."""
    hours = [NOW.replace(minute=0) - timedelta(hours=h) for h in range(48, 0, -1)]
    ts = [int(t.timestamp()) for t in hours]
    if "coinbase" in url:
        return json.dumps([[t, 99.0, 101.0, 100.0, 100.5, 3.0] for t in ts]).encode()
    if "yahoo" in url:
        q = {k: [1.0] * len(ts) for k in ("open", "high", "low", "close", "volume")}
        chart = {"result": [{"timestamp": ts, "indicators": {"quote": [q]}}]}
        return json.dumps({"chart": chart}).encode()
    if "kraken" in url:
        rates = [{"timestamp": intraday.iso(t), "fundingRate": 1.0, "relativeFundingRate": 1e-5}
                 for t in hours]  # fmt: skip
        return json.dumps({"rates": rates}).encode()
    raise OSError("blocked")


def tree(root: Path) -> dict[str, bytes]:
    files = sorted(p for p in root.rglob("*") if p.is_file())
    return {str(p.relative_to(root)): p.read_bytes() for p in files}


def crash(base: Path, now: datetime, get: intraday.Get) -> dict[str, str]:
    raise RuntimeError("collector bug")


def test_a_collector_crash_leaves_the_daily_run_unchanged(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    day1 = datetime(2026, 11, 2, 22, 30, tzinfo=UTC)
    plain, crashed = tmp_path / "plain" / "trail", tmp_path / "crashed" / "trail"
    for root in (plain, crashed):
        root.mkdir(parents=True)

    assert run_daily.run(plain, day1, fake_market, plain) == []
    assert run_daily.run(plain, day1 + timedelta(days=1), fake_market, plain) == []

    assert run_daily.run(crashed, day1, fake_market, crashed) == []
    side = tmp_path / "crashed" / "intraday"
    out = run_daily.collect_intraday(side, crashed, day1, collect=crash)
    assert out["intraday"].startswith("error: RuntimeError")
    monkeypatch.setattr(intraday, "collect", crash)  # the CLI path too: returns, exit code 0
    run_daily.main(["--root", str(crashed), "--intraday", str(side)])
    assert run_daily.run(crashed, day1 + timedelta(days=1), fake_market, crashed) == []

    assert tree(crashed) == tree(plain)


def test_a_second_run_on_the_same_day_adds_nothing(tmp_path: Path) -> None:
    base, root = tmp_path / "intraday", tmp_path / "trail"
    first = run_daily.collect_intraday(base, root, NOW, fake_intraday)
    assert all(v.startswith("+") and v != "+0" for v in first.values()), first
    stored = tree(base)
    again = run_daily.collect_intraday(base, root, NOW + timedelta(minutes=5), fake_intraday)
    assert set(again.values()) == {"+0"}
    assert tree(base) == stored


def test_the_store_may_not_sit_inside_the_record(tmp_path: Path) -> None:
    root = tmp_path / "trail"
    root.mkdir()
    out = run_daily.collect_intraday(root / "data" / "intraday", root, NOW, fake_intraday)
    assert out["intraday"].startswith("error")
    assert tree(root) == {}


def test_nothing_that_trades_or_scores_reads_the_intraday_files() -> None:
    users = sorted(
        str(p.relative_to(SRC))
        for p in SRC.rglob("*.py")
        if "intraday" in p.read_text() and p.name != "intraday.py"
    )
    assert users == ["run_daily.py"]
    for fn in (run_daily.run, run_daily.check_record, run_daily._revisions, run_daily._overdue):
        assert "intraday" not in inspect.getsource(fn)


def test_the_workflow_collects_only_after_the_record_is_pushed() -> None:
    text = DAILY.read_text()
    commit = text.index("- name: Commit the record")
    steps = text[commit:].split("\n      - ")[1:]
    assert [s.splitlines()[0] for s in steps] == [
        "name: Restore the intraday store",
        "name: Check the intraday store",
        "name: Collect intraday data",
        "name: Save the intraday store",
    ]
    for step in steps:
        assert "continue-on-error: true" in step
        assert "trail/" not in step and "path: trail" not in step
    assert text.index("grimstrade.run_daily --root trail\n") < commit


def store(tmp_path: Path, matched: str, gh: str) -> str:
    fake = tmp_path / "bin"
    fake.mkdir(exist_ok=True)
    (fake / "gh").write_text(f"#!/usr/bin/env bash\n{gh}\n")
    (fake / "gh").chmod(0o755)
    out = tmp_path / "out"
    out.write_text("")
    env = {**os.environ, "PATH": f"{fake}:{os.environ['PATH']}", "GITHUB_OUTPUT": str(out),
           "GITHUB_REPOSITORY": "o/r", "MATCHED_KEY": matched}  # fmt: skip
    subprocess.run([str(STORE)], env=env, check=True, capture_output=True)
    return out.read_text().strip()


def test_the_store_guard_never_lets_a_short_copy_replace_the_store(tmp_path: Path) -> None:
    assert store(tmp_path, "intraday-9-1", "exit 1") == "ok=yes"  # restored
    assert store(tmp_path, "", "echo 0") == "ok=yes"  # no store yet: start one
    assert store(tmp_path, "", "echo 1") == "ok=no"  # a store exists, the restore missed
    assert store(tmp_path, "", "exit 1") == "ok=no"  # can't tell: skip today
