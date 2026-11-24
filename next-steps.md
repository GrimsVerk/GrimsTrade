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

## Night lead 2026-11-24 (in flight; this section is rewritten at handoff)

Merged tonight, each after a fresh review agent: #136 (ruff exclude for a one-off script),
#133 (forward registry hardening; delayed schedule in DECISIONS), #138 (Treasury bill-rate
fallback), #137 (halving-2: `halving-alone` does not transfer to other halving coins; BTC-beta),
#134 (turbulence-1: dead, the volatility part does all the work), #135 (`own_vol_70` paper book),
#140 (Gymnasium env wrapper, `docs/gym-env.md`), #139 (wide-15: two gates, both fail; 87
mechanisms, 22 gates). Under review: #141 (reconcile-1: live record == gym), #143
(breadth-book-1: more markets lowered `tsmom12`'s Sharpe). Running: `pooled-1`, `lagcost-1`,
`wide-16`, `daily-nodev-1`, `seasonal-1`.

## Lane queue (each from `main`)

1. After the first daily run on new main (tonight ~02:00-06:00 UTC): rerun
   `research/lib/reconcile1.py` (from #141) and check the one-time replay change it predicts.
2. Regenerate `research/register/BAR.md` with tonight's tries rows (register + register2), then
   refresh `research/SUMMARY.md` with tonight's verdicts.
3. `Replay` in `src/grimstrade/gym_env.py` copies `gym.simulate`'s loop: rewrite `simulate` as
   `Replay` + a decision loop so there is one copy (touches the runner path: needs a daily dry
   run). Add a test for the no-event-day interest catch-up.
