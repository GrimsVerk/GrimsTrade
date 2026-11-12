"""Honesty audit 2026-11: ways the ledger can lie that `check_append_only` does not catch.

Each xfail test demonstrates one finding in docs/audits/honesty-2026-11.md and turns green when
that finding is fixed (strict: an unexpected pass fails the suite, so the marker gets removed).
"""

import subprocess
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import pytest

from grimstrade import ledger, report
from grimstrade.data import Bar, History

DAY1 = date(2026, 11, 1)


def git(repo: Path, *args: str, when: datetime | None = None) -> str:
    env = None
    if when is not None:
        stamp = when.strftime("%Y-%m-%dT%H:%M:%S+00:00")
        env = {"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp, "PATH": "/usr/bin:/bin"}
    out = subprocess.run(
        ["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
        cwd=repo,
        check=True,
        capture_output=True,
        env=env,
    )
    return out.stdout.decode().strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    git(tmp_path, "init", "-q", "-b", "paper-trail")
    return tmp_path


def at(d: date, hh: int = 22, mm: int = 30) -> datetime:
    return datetime(d.year, d.month, d.day, hh, mm, tzinfo=UTC)


def btc(opens_closes: list[tuple[float, float]]) -> list[Bar]:
    return [
        Bar(DAY1 + timedelta(days=i), o, max(o, c), min(o, c), c, 1.0)
        for i, (o, c) in enumerate(opens_closes)
    ]


def decide(repo: Path, when: datetime, strategy: str, weights: dict[str, float]) -> None:
    seen: History = {"BTC": [Bar(when.date() - timedelta(days=1), 1, 1, 1, 100.0, 1)]}
    ledger.write_decision(repo, when, strategy, weights, seen, "test")


def commit(repo: Path, message: str, when: datetime) -> None:
    git(repo, "add", "-A")
    git(repo, "commit", "-qm", message, when=when)


def test_a_backdated_decision_is_not_credited(repo: Path) -> None:
    """Audit L1 (fixed): append-only is not the same as written-in-time. A line appended after
    the outcome, stamped with an earlier time, used to be filled at the old open. Now a decision
    counts from the moment its commit was made."""
    # BTC: flat on day 1, opens day 2 at 100, doubles by day 3, then stays at 200.
    history: History = {"BTC": btc([(100, 100), (100, 150), (150, 200), (200, 200), (200, 200)])}
    # Day 1, 22:30: the honest run. Everyone stays in cash. Committed the same minute.
    decide(repo, at(DAY1), "honest", {})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    # Day 4: BTC has doubled. Someone appends a line that claims "on day 1 at 22:31 I went all in".
    decide(repo, at(DAY1, 22, 31), "cheat", {"BTC": 1.0})
    commit(repo, "Daily run day 4", when=at(DAY1 + timedelta(days=3), 22, 31))

    # It is an append, so the append-only check has nothing to say...
    ledger.check_append_only(repo / ledger.DECISIONS)
    # ...but the order is filled at the first open after it was committed (day 5, at 200), not at
    # the day-2 open (100) it was aiming for: no profit from hindsight.
    (fill,) = report.live_results(repo, history)["cheat"].fills
    assert fill.time == datetime(2026, 11, 5, tzinfo=UTC)
    assert fill.price == pytest.approx(200 * 1.0005)
    assert report.score("cheat", report.live_results(repo, history)["cheat"]).total_return < 0
    # And the scoreboard says so.
    (_, late) = ledger.in_force(repo)
    assert late == 1
    assert "**Late decisions: 1.**" in report.render(repo, history)


def test_a_backdated_commit_gains_nothing_before_the_commit_under_it(repo: Path) -> None:
    """Audit L1 (second pass): `in_force` believed every commit's own date. A forger who back-dates
    the commit as well as the line was caught only from outside (GitHub's activity log), and not
    at all where that log cannot be asked. A commit cannot be older than its parent, whatever it
    claims: it now counts from the latest time on its path."""
    history: History = {"BTC": btc([(100, 100), (100, 150), (150, 200), (200, 200), (200, 200)])}
    decide(repo, at(DAY1), "honest", {})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    decide(repo, at(DAY1 + timedelta(days=2)), "honest", {})
    commit(repo, "Daily run day 3", when=at(DAY1 + timedelta(days=2), 22, 31))
    # Day 4: BTC has doubled. A line dated day 1, in a commit that says day 1 as well.
    decide(repo, at(DAY1, 22, 32), "cheat", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 33))

    ledger.check_append_only(repo / ledger.DECISIONS)
    # It counts from the day-3 commit under it: filled at the day-4 open (200), not at day 2's.
    (fill,) = report.live_results(repo, history)["cheat"].fills
    assert fill.time == datetime(2026, 11, 4, tzinfo=UTC)
    assert fill.price == pytest.approx(200 * 1.0005)
    counted, late = ledger.in_force(repo)
    assert late == 1
    # The honest strategy's two decisions are untouched.
    assert [t for t, row in counted if row["strategy"] == "honest"] == [
        at(DAY1, 22, 31),
        at(DAY1 + timedelta(days=2), 22, 31),
    ]


def test_padding_with_blank_lines_does_not_move_a_backdated_decision(repo: Path) -> None:
    """Found by the independent reviewer in the first version of the L1 fix: line positions were
    counted in text characters, commits in bytes. Blank "\\r\\n" lines are two bytes but one
    character, so padding the ledger with them moved a later line's position back into an older
    commit, and a back-dated decision counted as on time again."""
    history: History = {"BTC": btc([(100, 100), (100, 150), (150, 200), (200, 200), (200, 200)])}
    path = repo / ledger.DECISIONS
    decide(repo, at(DAY1), "honest", {})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    with path.open("ab") as f:
        f.write(b"\r\n" * 30_000)  # looks like nothing: blank lines
    commit(repo, "tidy", when=at(DAY1, 22, 40))
    decide(repo, at(DAY1 + timedelta(days=1)), "honest", {})
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    # Day 4: the back-dated line, stamped just after the padding commit.
    decide(repo, at(DAY1, 22, 41), "cheat", {"BTC": 1.0})
    commit(repo, "Daily run day 4", when=at(DAY1 + timedelta(days=3), 22, 31))

    ledger.check_append_only(path)  # appends only, so this passes
    counted, late = ledger.in_force(repo)
    cheat = [(t, row) for t, row in counted if row["strategy"] == "cheat"]
    assert [t for t, _ in cheat] == [at(DAY1 + timedelta(days=3), 22, 31)] and late == 1
    assert len([row for _, row in counted if row["strategy"] == "honest"]) == 2
    (fill,) = report.live_results(repo, history)["cheat"].fills
    assert fill.time == datetime(2026, 11, 5, tzinfo=UTC)  # after the commit, not day 2


def test_a_decision_counts_from_its_commit(repo: Path) -> None:
    """Audit T1 (fixed with L1): a late run stamped 23:59:30 whose commit lands after midnight
    is not filled at the 00:00 open that already existed when it was recorded."""
    history: History = {"BTC": btc([(100, 100), (200, 200), (300, 300), (300, 300)])}
    stamped = datetime(2026, 11, 1, 23, 59, 30, tzinfo=UTC)
    decide(repo, stamped, "s", {"BTC": 1.0})
    # Before the commit exists (the run itself, scoring its own fresh line): the timestamp counts.
    assert ledger.in_force(repo)[0][0][0] == stamped
    commit(repo, "Daily run", when=datetime(2026, 11, 2, 0, 0, 40, tzinfo=UTC))
    ((counts_from, _),), late = ledger.in_force(repo)
    assert counts_from == datetime(2026, 11, 2, 0, 0, 40, tzinfo=UTC) and late == 0
    (fill,) = report.live_results(repo, history)["s"].fills
    assert fill.time == datetime(2026, 11, 3, tzinfo=UTC) and fill.price == pytest.approx(300.15)


def test_normal_runs_and_one_commit_for_two_days(repo: Path) -> None:
    # Two ordinary runs, each committed a minute later: both count, in order, nothing is late.
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    decide(repo, at(DAY1 + timedelta(days=1)), "s", {})
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    counted, late = ledger.in_force(repo)
    assert [(t, r["weights"]) for t, r in counted] == [
        (at(DAY1, 22, 31), {"BTC": 1.0}),
        (at(DAY1 + timedelta(days=1), 22, 31), {}),
    ]
    assert late == 0
    # A sloppy local run: days 3 and 4 decided on time but committed together on day 4. Day 3's
    # line was never provably in force before day 4's replaced it, so only day 4's counts.
    decide(repo, at(DAY1 + timedelta(days=2)), "s", {"BTC": 0.5})
    decide(repo, at(DAY1 + timedelta(days=3)), "s", {"BTC": 0.25})
    decide(repo, at(DAY1 + timedelta(days=3)), "other", {})
    commit(repo, "two days at once", when=at(DAY1 + timedelta(days=3), 22, 31))
    counted, late = ledger.in_force(repo)
    assert [r["weights"] for _, r in counted if r["strategy"] == "s"] == [
        {"BTC": 1.0}, {}, {"BTC": 0.25},
    ]  # fmt: skip
    assert late == 1
    assert len(ledger.recorded_at(repo / ledger.DECISIONS)) == len(ledger.decisions(repo)) == 5


def test_outside_git_decisions_count_from_their_own_time(tmp_path: Path) -> None:
    decide(tmp_path, at(DAY1), "s", {"BTC": 1.0})
    assert ledger.in_force(tmp_path) == ([(at(DAY1), ledger.decisions(tmp_path)[0])], 0)
    assert ledger.in_force(tmp_path / "nothing-here") == ([], 0)


def _honest_two_days(repo: Path) -> Path:
    """Two honest daily commits: day 1 `s` goes all in on BTC, day 2 it holds."""
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    decide(repo, at(DAY1 + timedelta(days=1)), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    return repo / ledger.DECISIONS


def test_a_rewrite_hidden_behind_a_merge_is_caught(repo: Path) -> None:
    path = _honest_two_days(repo)
    honest_head = git(repo, "rev-parse", "HEAD")
    # BTC crashed, so the forger wants day 1 to say "stayed in cash". Build a parallel history
    # with the forged file, then merge the honest branch into it keeping the forged content.
    git(repo, "checkout", "-q", "--orphan", "forged")
    path.write_text(path.read_text().replace('"weights":{"BTC":1.0}', '"weights":{}'))
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    git(repo, "merge", "-q", "-s", "ours", "--allow-unrelated-histories", "-m", "sync", honest_head)
    # The result descends from the honest head, so pushing it is a plain fast-forward:
    # no force-push, and "block force pushes" on the branch would not stop it.
    git(repo, "merge-base", "--is-ancestor", honest_head, "HEAD")
    assert all(r["weights"] == {} for r in ledger.decisions(repo))  # the record now lies

    # Audit L2 (fixed): `git log -- file` skipped the honest side of that merge; the check now
    # compares every commit with each of its parents.
    with pytest.raises(ledger.LedgerTampered):
        ledger.check_append_only(path)


def test_honest_merges_and_a_deleted_working_file(repo: Path) -> None:
    path = _honest_two_days(repo)
    # A merge that brings in an unrelated side branch without touching the ledger is fine.
    git(repo, "checkout", "-q", "-b", "side")
    (repo / "note.txt").write_text("x")
    commit(repo, "side note", when=at(DAY1 + timedelta(days=1), 23, 0))
    git(repo, "checkout", "-q", "paper-trail")
    decide(repo, at(DAY1 + timedelta(days=2)), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 3", when=at(DAY1 + timedelta(days=2), 22, 31))
    git(repo, "merge", "-q", "--no-ff", "-m", "merge side", "side")
    assert ledger.check_append_only(path) == 3
    # Deleting the ledger from the working tree is a rewrite too.
    path.unlink()
    with pytest.raises(ledger.LedgerTampered):
        ledger.check_append_only(path)


def test_a_force_pushed_history_passes_the_check(repo: Path) -> None:
    """Audit L3, the limit of any check that only reads the branch: if the whole history is
    replaced (force-push, or delete + recreate), the new history is self-consistent and nothing
    inside it can show the old one existed. Only an outside witness can (GitHub's activity log,
    a branch ruleset). This test documents the limit; the guard is tested in
    test_audit_workflow.py."""
    path = _honest_two_days(repo)
    git(repo, "checkout", "-q", "--orphan", "rewritten")
    path.write_text(path.read_text().replace('"weights":{"BTC":1.0}', '"weights":{}'))
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    git(repo, "branch", "-q", "-M", "paper-trail")  # what `push --force` leaves on the remote
    assert ledger.check_append_only(path) == 1


def test_a_rewritten_bar_is_caught(repo: Path) -> None:
    """Audit L4 (fixed): stored bars are part of the record (the scoreboard is recomputed from
    them every run) but only the ledger files were checked for rewrites."""
    from grimstrade import data, run_daily

    data.append(repo, "BTC", btc([(100, 100), (100, 100), (100, 100)]))
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    before = report.score("s", report.live_results(repo, data.load_all(repo))["s"])

    # Lower the price `s` paid at the day-2 open from 100 to 50. One edited cell.
    bars = data.bars_path(repo, "BTC")
    lines = bars.read_text().splitlines(keepends=True)
    assert lines[2].startswith("2026-11-02,100.0,")
    lines[2] = lines[2].replace("2026-11-02,100.0,", "2026-11-02,50.0,")
    bars.write_text("".join(lines))
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    after = report.score("s", report.live_results(repo, data.load_all(repo))["s"])
    assert before.total_return < 0 and after.total_return > 0.9  # a loss became +99%

    def offline(url: str) -> bytes:
        raise OSError("offline")

    with pytest.raises(ledger.LedgerTampered, match="data/bars/BTC.csv"):
        run_daily.run(repo, at(DAY1 + timedelta(days=2)), offline)


def test_outside_a_git_checkout_the_check_silently_checks_nothing(tmp_path: Path) -> None:
    """Audit L6 (low): `--root` pointing at a plain folder (or at a gitignored `trail/` that is
    not a worktree) makes `check_append_only` return 0 without complaint, and the runner ignores
    the return value. A rewritten ledger there is never noticed."""
    decide(tmp_path, at(DAY1), "s", {"BTC": 1.0})
    path = tmp_path / ledger.DECISIONS
    path.write_text(path.read_text().replace('"BTC":1.0', '"BTC":0.5'))
    assert ledger.check_append_only(path) == 0


def test_a_decision_records_the_code_version(repo: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Audit L7 (first half fixed): a decision line did not say which code made it, so a strategy
    could change under the same name and keep one unbroken track record (and one try)."""
    monkeypatch.setenv("GITHUB_SHA", "8e26333a0000000000000000000000000000beef")
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    monkeypatch.delenv("GITHUB_SHA")
    decide(repo, at(DAY1 + timedelta(days=1)), "s", {"BTC": 1.0})  # a local run: unknown code
    first, second = ledger.decisions(repo)
    assert first["code"] == "8e26333a0000000000000000000000000000beef"
    assert "code" not in second


def test_a_strategy_changed_under_its_name_is_flagged(repo: Path) -> None:
    """Audit L7 (second half, fixed): a strategy's code or parameters could change under the same
    name and the scoreboard went on showing one unbroken record. Each decision now carries a
    fingerprint of the strategy's own code and the scoreboard says when it changed."""
    from grimstrade import report, run_daily
    from grimstrade.strategies import LIVE

    same = run_daily.fingerprint(LIVE["ts_momentum"])
    assert same == run_daily.fingerprint(LIVE["ts_momentum"]) and len(same) == 12
    assert same != run_daily.fingerprint(LIVE["xs_momentum"])  # another file, another fingerprint

    bars = btc([(100.0, 100.0)] * 5)
    seen: History = {"BTC": bars[:1]}
    decide(repo, at(DAY1), "s", {"BTC": 1.0})  # an old line, from before fingerprints
    for day, version in ((1, "aaaaaaaaaaaa"), (2, "aaaaaaaaaaaa")):
        when = at(DAY1 + timedelta(days=day))
        ledger.write_decision(repo, when, "s", {"BTC": 1.0}, seen, "t", version)
    assert report.code_changes(repo) == {}
    assert "Code changed" not in report.render(repo, {"BTC": bars})
    when = at(DAY1 + timedelta(days=3))
    ledger.write_decision(repo, when, "s", {"BTC": 0.5}, seen, "t", "bbbbbbbbbbbb")
    assert report.code_changes(repo) == {"s": 1}
    assert "**Code changed under the same name:** s (1x)" in report.render(repo, {"BTC": bars})
    # Second review: a line written by hand has no fingerprint; once a name has them, that
    # counts as a change too (it used to be skipped, so a hand-made decision went unflagged).
    decide(repo, at(DAY1 + timedelta(days=4)), "s", {"BTC": 1.0})
    assert report.code_changes(repo) == {"s": 2}


def test_a_lost_final_newline_does_not_glue_lines_together(tmp_path: Path) -> None:
    """Audit L9 (fixed; found by the independent reviewer): a ledger or bar file whose last line
    had lost its newline got the next line glued on ("}{"). Every later run then failed to parse
    it, and restoring the newline counted as rewriting history."""
    from grimstrade import data

    decide(tmp_path, at(DAY1), "s", {"BTC": 1.0})
    path = tmp_path / ledger.DECISIONS
    path.write_bytes(path.read_bytes().rstrip(b"\n"))
    before = path.read_bytes()
    decide(tmp_path, at(DAY1 + timedelta(days=1)), "s", {})
    assert path.read_bytes().startswith(before)  # still only an append
    assert [r["weights"] for r in ledger.decisions(tmp_path)] == [{"BTC": 1.0}, {}]

    data.append(tmp_path, "BTC", btc([(100, 100)]))
    bars = data.bars_path(tmp_path, "BTC")
    bars.write_bytes(bars.read_bytes().rstrip(b"\n"))
    data.append(tmp_path, "BTC", btc([(100, 100), (101, 101)]))
    assert [b.close for b in data.load(tmp_path, "BTC")] == [100.0, 101.0]
    # An empty bar file still gets its header.
    data.bars_path(tmp_path, "ETH").write_bytes(b"")
    data.append(tmp_path, "ETH", btc([(5, 5)]))
    assert [b.close for b in data.load(tmp_path, "ETH")] == [5.0]


def test_a_time_without_a_zone_is_refused() -> None:
    with pytest.raises(ValueError, match="time zone"):
        ledger.iso(datetime(2026, 11, 12, 22, 30))
    assert ledger.iso(datetime(2026, 11, 12, 22, 30, tzinfo=UTC)) == "2026-11-12T22:30:00Z"


# --- second independent review (2026-11-12): what the checks above still let through ---


def test_a_backdated_commit_merged_in_beside_the_record_is_refused(repo: Path) -> None:
    """Second review, high: one commit whose parent is the day-1 commit, dated day 1, holding the
    whole current ledger plus a hindsight line; then a merge with the real tip. The merged file
    is a pure append to both parents, so the append-only check passes, and every line in it
    counted from the forged date (the reviewer measured +98.7% for a record that made 0.0%).
    The daily job never merges, so a merge in the record is refused."""
    from grimstrade import run_daily

    path = _honest_two_days(repo)
    day1 = git(repo, "rev-list", "--max-parents=0", "HEAD")
    current = path.read_bytes()
    git(repo, "checkout", "-q", "-b", "forged", day1)
    path.write_bytes(current)
    decide(repo, at(DAY1, 22, 32), "s", {})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 33))
    git(repo, "checkout", "-q", "paper-trail")
    day4 = at(DAY1 + timedelta(days=3))
    git(repo, "merge", "-q", "--no-ff", "-X", "theirs", "-m", "merge", "forged", when=day4)
    assert path.read_bytes().startswith(current) and len(path.read_bytes()) > len(current)
    ledger.check_append_only(path)  # nothing to say: the file only grew
    with pytest.raises(ledger.LedgerTampered, match="is a merge"):
        run_daily.check_record(repo, day4 + timedelta(days=1))


def test_a_commit_dated_before_the_one_under_it_stops_the_run(repo: Path) -> None:
    """Second review: commit dates are written by whoever commits. One that runs backwards is a
    lie that shows from inside the record, so the run refuses (and does not only work around it,
    as `in_force` does for a report)."""
    from grimstrade import run_daily

    _honest_two_days(repo)
    now = at(DAY1 + timedelta(days=5))
    run_daily.check_record(repo, now)  # an honest history passes
    decide(repo, at(DAY1, 22, 32), "cheat", {"BTC": 1.0})
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 33))
    with pytest.raises(ledger.LedgerTampered, match="dated before the commit under it"):
        run_daily.check_record(repo, now)


def test_a_commit_dated_in_the_future_stops_the_run(repo: Path) -> None:
    """Second review: a commit dated 2099, touching anything at all, made every later decision
    count from 2099, i.e. never: each run's decision displaced the one before it, and only a
    growing "late decisions" number showed. (Past year 9999 every reader crashed.)"""
    from grimstrade import run_daily

    _honest_two_days(repo)
    (repo / "note.txt").write_text("x")
    commit(repo, "a note", when=datetime(2099, 1, 1, tzinfo=UTC))
    with pytest.raises(ledger.LedgerTampered, match="dated in the future"):
        run_daily.check_record(repo, at(DAY1 + timedelta(days=5)))


def test_a_record_file_swapped_for_a_symlink_is_refused(repo: Path) -> None:
    """Second review, high: the checks resolved links, so they vouched for the history of the
    link's target. One ordinary commit could swap the ledger or a bar file for another file that
    "only ever grew" (the reviewer turned -50% into +199%)."""
    path = _honest_two_days(repo)
    other = path.with_name("other.jsonl")
    other.write_text(path.read_text().replace('"BTC":1.0', '"BTC":0.5'))
    commit(repo, "a harmless new file", when=at(DAY1 + timedelta(days=2), 1, 0))
    path.unlink()
    path.symlink_to("other.jsonl")
    commit(repo, "Daily run day 3", when=at(DAY1 + timedelta(days=2), 22, 31))
    with pytest.raises(ledger.LedgerTampered, match="symbolic link"):
        ledger.check_append_only(path)
    with pytest.raises(ledger.LedgerTampered, match="symbolic link"):
        ledger.in_force(repo)
    # A linked folder is the same trick.
    (repo / "ledger").rename(repo / "real")
    (repo / "ledger").symlink_to("real")
    with pytest.raises(ledger.LedgerTampered, match="symbolic link"):
        ledger.check_append_only(repo / ledger.DECISIONS)


def test_a_shallow_clone_cannot_vouch_for_the_record(repo: Path, tmp_path: Path) -> None:
    """Second review: in a shallow clone git only has the newest commits. The check then vouched
    for history it could not see, and every old line was dated to the oldest commit present."""
    _honest_two_days(repo)
    decide(repo, at(DAY1 + timedelta(days=2)), "s", {})
    commit(repo, "Daily run day 3", when=at(DAY1 + timedelta(days=2), 22, 31))
    git(tmp_path, "clone", "-q", "--depth", "1", f"file://{repo}", "shallow")
    with pytest.raises(ledger.LedgerTampered, match="shallow"):
        ledger.check_append_only(tmp_path / "shallow" / ledger.DECISIONS)


def test_a_lost_newline_does_not_redate_the_last_decision(repo: Path) -> None:
    """Second review: lines were dated by where their newline sits. After a lost final newline
    the next run's newline completed the old line, which was then re-dated to that run: counted
    as late, and dropped in favour of the newer decision."""
    path = repo / ledger.DECISIONS
    decide(repo, at(DAY1), "s", {"BTC": 1.0})
    path.write_bytes(path.read_bytes().rstrip(b"\n"))
    commit(repo, "Daily run day 1", when=at(DAY1, 22, 31))
    decide(repo, at(DAY1 + timedelta(days=1)), "s", {})
    commit(repo, "Daily run day 2", when=at(DAY1 + timedelta(days=1), 22, 31))
    counted, late = ledger.in_force(repo)
    assert [t for t, _ in counted] == [at(DAY1, 22, 31), at(DAY1 + timedelta(days=1), 22, 31)]
    assert late == 0


def test_a_strategy_name_cannot_write_its_own_scoreboard_row(repo: Path) -> None:
    """Second review, high: names went into the tables as they are. A decision whose `strategy`
    holds "|" and a line break is a valid append and printed a typed-in row of numbers on every
    run. And a name that exists only in the decisions got a row without counting as a try."""
    name = "zz | 2026-05-01 | 190 | 31,400 | +214.0% | 4 of 4 |\n| fake"
    decide(repo, at(DAY1), name, {"BTC": 1.0})
    decide(repo, at(DAY1), "s", {})
    board = report.render(repo, {"BTC": btc([(100.0, 100.0)] * 3)}, repo)
    assert "+214.0%" not in board
    assert not any(line.startswith("| fake") for line in board.splitlines())
    assert ledger.total_tries(repo, repo) == 2


def test_a_nan_in_the_research_record_does_not_switch_off_its_spread(repo: Path) -> None:
    """Second review: one appended line with `"sharpe": NaN` made the spread of the tries'
    Sharpes NaN, and max(x, nan) is x: the deflated Sharpe lost a term (17.5% became 41.8%)."""
    path = repo / ledger.RESEARCH_FLOOR
    path.parent.mkdir(parents=True)
    path.write_text(
        '{"idea":"a","variant":"v1","sharpe":1.5,"seen":"2026-11-12T00:00:00Z"}\n'
        '{"idea":"a","variant":"v2","sharpe":NaN,"seen":"2026-11-12T00:00:00Z"}\n'
        '{"idea":"a","variant":"v3","sharpe":Infinity,"seen":"2026-11-12T00:00:00Z"}\n'
    )
    assert ledger.research_sharpes(repo, repo) == [1.5]
    assert ledger.research_tries(repo, repo) == 3  # still three tries
