# Next steps

Running log of what is in flight on GrimsTrade. Lane logs before 2026-11-24 stay on their own
branches; the leads' night log is on branch `summary-1` (closed PR #28, branch kept).

## Rules since 2026-11-24 (owner: "agents merge")

- Every lane branches from current `main` and opens a PR to `main`. No lane on an unmerged lane.
- The GrimsTrade lead merges (rebase; a merge commit for long-diverged branches) when the checks
  pass and a fresh review agent finds no required fix. Changes to the daily runner, scoreboard or
  workflows also need a passing dry run of the daily job
  (`uv run python -m grimstrade.run_daily --root <copy of paper-trail>`, then `--intraday <dir>`).
- Research records land when the result is written, negative ones too.
- Never: push to `main` or `paper-trail`, rewrite `main`, delete a lane branch (the tries
  register counts branches).
- Public repo: no personal detail about the owner in files, commits or PR texts.

## Landing lead 1 (2026-11-24): clear the PR backlog

- DONE #115: engineering PRs #13 #27 #29 #30 #32 #61 #67 #14 #15 landed in one merge
  (`docs/integrate-1.md`; 291 tests; daily dry run passed).
- DONE #118: research archive (all research lanes; `docs/research-archive-1.md`); 81 contained
  research PRs closed or marked merged with "landed via #118".
- DONE #129: scoreboard footnote says Sharpe is above the cash rate.
- DONE #126: register chain (#79 #92 #100 #108 #111 + register-6) in one merge, with three
  review fixes (non-UTF-8 branch files cannot stop the daily run; try-shape logging only warns;
  `research/tries-shape.jsonl` merges by union). The returns store keeps buy-and-hold weekly
  series (weekly returns derived from Yahoo/exchange prices back to 1994): accepted as derived
  statistics, not bars (lead's call, `returnstore.py`).
- Owner decisions brief (`research/owner-decisions.md`): every item answered by its default as
  an agent call (section "Answers"); no owner question left.

## Lane queue (each from `main`)

1. Second bill-rate source (US Treasury keyless CSV) when Yahoo `^IRX` fails (BACKLOG; A2c).
2. One own-vol 70% paper book next to the presets, no-look-ahead form (owner-decisions C2).
3. Record the delayed schedule in DECISIONS (runs fire 02:00-04:40 UTC, not 22:30; D1).
4. Forward registry: obs files get the append-only check; `read()` requires `frozen_at`
   (review notes on #67).
