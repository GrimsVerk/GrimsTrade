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

## Status

- **Done:** L1 demonstrated.
- **Doing:** remaining ledger findings (history rewrite through a merge, force-push, bars not
  checked, branch deletion), then data, gym, timing, statistics.
- **Next:** small fixes in `ledger.py`, `gym.py`, `sources.py`, the workflow; summary on top.
