# Honesty audit 1 (2026-11-12)

Auditor: lane C agent, branch `audit-1`. Scope: everything that could make the scoreboard say
something that is not true. Code audited: `main` at `8e26333`. Record audited: `paper-trail` at
`0d3bc31` (one daily run, 2026-11-11 22:00 UTC), read-only.

## Summary for the owner

(Being written as findings land; see Status at the end for what is done.)

## Findings, ranked by how much they could mislead

Severity: **high** = the scoreboard can show a result that never happened, and nothing warns;
**medium** = numbers are biased or a safeguard is weaker than the docs say; **low** = small or
unlikely, worth knowing. Each finding names its test in `tests/test_audit_*.py`.

### L1. A decision written after the outcome is accepted (high)

- **What:** the ledger check only proves that old lines were not changed. It does not prove a
  line was written when it says it was. Anyone who can push to `paper-trail` (the three agents all
  act as GrimsBot, which has write access) can append "on day 1 at 22:31 I bought BTC" on day 4,
  after BTC doubled. The gym fills it at the day-2 open and the scoreboard shows +100%.
- **Evidence:** `tests/test_audit_ledger.py::test_a_backdated_decision_is_not_credited`.
  `gym.simulate` sorts decisions by their own `time` field; `check_append_only` passes because
  the file only grew. Nothing compares a line's `time` with the commit that first carried it.
- **Proposed fix:** (1) in the runner, refuse a ledger where a decision's `time` is not within
  ~30 minutes before the commit that introduced it; (2) since commit dates can be forged too, use
  GitHub's own push log as the outside witness: `gh api repos/GrimsVerk/GrimsTrade/activity?ref=refs/heads/paper-trail`
  already lists every push with a server-side timestamp (checked 2026-11-12: it shows the branch
  creation by `github-actions[bot]` at 22:00:52Z, 3 s after the first decisions); (3) owner:
  a ruleset on `paper-trail` (see L2).

### L2. History can be rewritten with an ordinary push (high)

- **What:** `check_append_only` reads `git log -- <file>`. Git simplifies that log at merges: when
  a merge keeps one parent's version of the file, the other parent's history is skipped. So a
  forger builds a parallel history with a changed ledger, merges the honest branch into it keeping
  the forged file, and pushes. The result descends from the honest head, so it is a normal
  fast-forward push: no force-push needed, and a "block force pushes" rule would not stop it.
- **Evidence:** `tests/test_audit_ledger.py::test_a_rewrite_hidden_behind_a_merge_is_caught`
  (a losing all-in decision becomes "stayed in cash"; the check passes).
- **Proposed fix (small, in `ledger.py`):** walk every commit and compare the file with each of
  its parents' versions, instead of trusting the simplified log.

### L3. A force-push or delete-and-recreate of `paper-trail` leaves no trace in the repo (high)

- **What:** if the whole branch is replaced, the new history is self-consistent; no check that
  only reads the branch can know an older one existed. Today nothing stops it: the only ruleset
  (`protect-main`) covers the default branch only, and GrimsBot (all agents) has push rights.
- **Evidence:** `tests/test_audit_ledger.py::test_a_force_pushed_history_passes_the_check`;
  `gh api repos/GrimsVerk/GrimsTrade/rulesets` lists only `protect-main` with
  `include: ["~DEFAULT_BRANCH"]`.
- **Proposed fix:** (owner, needs admin) add a ruleset for `paper-trail`: block force pushes and
  deletion, no bypass. (Workflow, small) before running, ask GitHub's activity log for
  `force_push` / `branch_deletion` events on `paper-trail` and refuse to run if there are any:
  `tests/test_audit_workflow.py::test_the_job_checks_githubs_activity_log_for_a_rewritten_trail`.

### L4. Stored bars can be edited and nothing notices (high)

- **What:** the scoreboard is recomputed from `data/bars/*.csv` on every run, so the bars are as
  much "the record" as the decisions. AGENTS.md forbids rewriting them, but only the two ledger
  files are checked. Changing one cell (the open a strategy bought at) rewrites its whole result.
- **Evidence:** `tests/test_audit_ledger.py::test_a_rewritten_bar_is_caught`: one edited open
  turns a small loss into +99%, and the next run accepts it.
- **Proposed fix (small):** run the same append-only check over every file in `data/bars/`.

### L5. A failed fetch starts a brand-new record (medium)

- **What:** the workflow does `git fetch origin paper-trail || git worktree add --orphan`. If
  the branch was deleted, the bot silently starts a fresh record and the old one is gone from
  the scoreboard. If the fetch only failed for a moment (network), it also builds an orphan; the
  push is then rejected, so that day's decisions are lost.
- **Evidence:** `.github/workflows/daily.yml` lines 33-37;
  `tests/test_audit_workflow.py::test_a_failed_fetch_does_not_start_a_new_record`.
- **Proposed fix (small, workflow):** ask `git ls-remote` whether the branch exists; create the
  orphan only when the remote answers "no such branch" and the run was started by hand with an
  explicit "start a new record" input.

### L6. Outside a git checkout the check silently checks nothing (low)

- **What:** with `--root` on a plain folder, or on a `trail/` folder that is not a worktree
  (`/trail/` is gitignored in the code repo), `check_append_only` returns 0 and the runner ignores
  that. Mostly a trap for local runs.
- **Evidence:** `tests/test_audit_ledger.py::test_outside_a_git_checkout_the_check_silently_checks_nothing`.
- **Proposed fix:** the runner prints how many committed versions it verified and refuses a
  non-empty ledger with none.

### L7. A decision does not say which code made it (medium)

- **What:** strategy names key the ledger, but a strategy's code or parameters can change under
  the same name. The scoreboard then shows one unbroken track record, and `tries.jsonl` counts one
  try, for what were really two strategies. The daily job runs whatever is on `main` that day.
- **Evidence:** `tests/test_audit_ledger.py::test_a_decision_records_the_code_version`; the
  first real ledger lines have no code reference.
- **Proposed fix (small, `ledger.py`):** write the commit SHA of the code (`GITHUB_SHA`) into
  each decision line. Later: the scoreboard starts a new row when a strategy's code changes.

### L8. The daily job can be started from any branch (medium)

- **What:** `workflow_dispatch` runs the workflow file and code of whatever branch is chosen
  (`gh workflow run daily.yml --ref m1`). That code then writes to the one official record:
  unmerged strategies, a different gym, a different report.
- **Evidence:** `.github/workflows/daily.yml` has no branch condition;
  `tests/test_audit_workflow.py::test_the_job_only_runs_code_from_main`.
- **Proposed fix (small, workflow):** `if: github.ref == 'refs/heads/main'` on the job.

## Status

- **Done:** L1-L8 (ledger and workflow) demonstrated with tests.
- **Doing:** data, then gym, timing, statistics.
- **Next:** small fixes in `ledger.py`, `gym.py`, `sources.py`, the workflow; summary on top.
