"""Honesty audit 2026-11: the daily workflow (.github/workflows/daily.yml).

The workflow can't run in tests, so these read its text. They are deliberately few and each
names the behaviour it stands for (see docs/audits/honesty-2026-11.md).
"""

from pathlib import Path

import pytest

DAILY = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "daily.yml"


@pytest.mark.xfail(
    strict=True,
    reason="audit L5: any failed fetch of paper-trail (deleted branch, or just a network blip) "
    "makes the job start a brand-new empty record instead of stopping",
)
def test_a_failed_fetch_does_not_start_a_new_record() -> None:
    text = DAILY.read_text()
    # Today: `if git fetch ...; then worktree add; else worktree add --orphan; fi`.
    # Needed: ask the remote whether the branch exists, and only then decide.
    assert "ls-remote" in text


@pytest.mark.xfail(
    strict=True,
    reason="audit L3: nothing asks GitHub whether paper-trail was force-pushed or deleted and "
    "recreated; the in-repo check cannot see that",
)
def test_the_job_checks_githubs_activity_log_for_a_rewritten_trail() -> None:
    assert "activity" in DAILY.read_text()


@pytest.mark.xfail(
    strict=True,
    reason="audit L8: workflow_dispatch can be started from any branch, so unmerged code "
    "(another gym, another strategy) can write into the one official record",
)
def test_the_job_only_runs_code_from_main() -> None:
    assert "github.ref == 'refs/heads/main'" in DAILY.read_text()
