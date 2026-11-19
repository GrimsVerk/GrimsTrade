# Next steps

## Waiting for review: register-3 (branch `register-3`, draft PR #100 into `register-2`)

Card and results: `research/register-3.md`. Done:

1. The harness logs weeks, skew, excess kurtosis of every try it logs, next to the row, in
   `research/tries-shape.jsonl` (`grimstrade.tryshape`; hook in `research/lib/harness.py`
   `_log`). `grimstrade.register` and `research/register2.py` read it from every branch.
2. Correlation sample capped at 10 series per family: rho 0.52 (was 0.58), N_eff 490 (was 433)
   at the same data; the edge needed over `tsmom12` moves by 0.002 (+0.30 / +0.56 stays).
3. Regenerated with tonight's branches: 3,118 tries, N 1,032, N_eff 486, same edge over
   `tsmom12`. Cluster Sharpes now inverse-variance (min-variance broke on two twin series):
   against zero a 32-year rule needs 1.42 (was 1.23).

- [ ] Lead: `git cherry-pick 5937c52` onto the research base new lanes start from, so their
      tries carry their shape (0 rows logged so far).
- [ ] Next: scripts that append to `tries.md` without `harness.run` call `tryshape.log` too.
- [ ] Next: the correlation sample still needs return series (saved curves, one machine);
      a compact committed weekly-returns file per logged try would make it portable.

## Waiting for review: register-2 (branch `register-2`, draft PR #92 into `register-1`)

Measured inputs for the bar (card and results: `research/register-2.md`). Done:

1. `ledger.register_try` takes optional `weeks`, `skew`, `excess_kurtosis` (new lines only).
2. `research/register2.py all` (numpy; needs `research/data/` prices and, for saved curves,
   `research/register2.local.json`, see the `.example`) writes `research/register/moments.jsonl`
   (1,209 rows + 11 live with T, skew, excess kurtosis) and `trials.json` (effective trials).
3. `grimstrade.register` reads both: BAR.md shows the measured N (433 of 1,027, measured rho
   0.58; ONC finds 2 clusters) and a per-record-length bar table.

- [ ] Owner/lead: accept the measured bar (N 433: +0.30 close / +0.56 far over `tsmom12`).
- [ ] Next: lanes pass `weeks`/`skew`/`excess_kurtosis` when logging (a column in
      `research/tries.md` or the harness's `_log`), so the backfill stops depending on caches.
- [ ] Next: a correlation sample that covers more families (only 40% of selectable rows have
      returns; one family is a third of the sample).

## Waiting for review: register-1 (branch `register-1`, draft PR #79 into `dsr-1`, not merged)

From dsr-1's findings; no backtests, no tries. Done:

1. The scoreboard's N reads every local and remote branch except `paper-trail` (was: `main` and
   `research-*` only) plus the committed register: 2,830 research tries, 534 train Sharpes (was
   285 and 78). DECISIONS 2026-11-18 entry. Tests in `tests/test_stats.py` fail on the old code.
2. `research/register/tries.jsonl` (every distinct try on every pushed branch, only grows) and
   `research/register/BAR.md` (counts and the bar for a new pick). Regenerate:
   `git fetch origin && uv run python -m grimstrade.register`. Reproduces dsr-1's census exactly
   (2,811 / 947 / 124 at its snapshot). At generation: 2,904 tries, N for a new pick 1,012,
   edge needed over `tsmom12` +0.27 (close rule, rho 0.9) to +0.59 (far rule, independent).
3. PROPOSED convention in `docs/DESIGN.md` (Idea lab): every card quotes BAR.md's count and bar.

- [ ] Owner/lead: settle or reject the convention; then move it to DECISIONS.
- [ ] After merging to `main`: the night lead regenerates the register in one PR per night.
- [ ] Possible next: lanes log T, skew and kurtosis so BAR.md can give the bar per record length.

## Waiting for review: dsr-1 (branch `dsr-1`, draft PR #74 into `main`, not merged)

Project-wide multiple-testing check, no backtests. Write-up with verdict: `research/dsr-1.md`;
script: `research/dsr1.py` (`census`, `dsr`). Result: `tsmom12`'s profit survives any N, its
edge over equal weight fails at N = 1; no near-miss survives the project's search; none is worth
a held-out year.

- [x] Fix found: `ledger._RESEARCH_REFS` read only `main` and `research-*` branches (live N
      stopped at 307). Fixed in register-1 (PR #79).
- [ ] Owner/lead: decide on the project-wide register (built in register-1, PR #79, convention
      PROPOSED in `docs/DESIGN.md`) and have every card quote the global N.

## Waiting for review: honesty audit 1 (branch `audit-1`, PR #5, ready for review, not merged)

Adversarial audit of the record's honesty. Report with a half-screen summary, all findings
ranked, and a Status section: `docs/audits/honesty-2026-11.md`. Tests: `tests/test_audit_*.py`.

- [ ] Owner (needs admin): ruleset on `paper-trail` blocking force pushes and deletion (L3).
- [ ] Owner: decide what "graduation" means; six months cannot prove skill (S2).
- [ ] After merging: read the first daily run's log; the "Ask GitHub" step must say "GitHub's
      activity log agrees with the paper-trail history", not "rewrite check skipped" (the job's
      own token was never tried against the activity log).
- [ ] After merging: tell the research lane that the crypto fee is 60 bps now (was 25; G3,
      DECISIONS). Their logged Sharpes used the old fee; new backtests will be a little worse.
- [ ] After merging: bring `research-1`, `research-2` and `m1-wrapup` up to `main` or delete
      them, and never re-run an old Daily run: old workflow files have no guards (L13).
- [ ] Next audit pass: attack `ledger.py`, `run_daily.check_record` and the two scripts in
      `scripts/` again; three passes each found something.
- [ ] Build next from the audit: GitHub's arrival time for accepted commits, passed to the run
      directly, not through a file in the record (L14).
- [ ] Open findings to build next: credit dividends (G4); a second ETF source, Stooq is dead
      (D6, needs a key: owner's call); keep an unfilled buy pending (G2); crypto fee by volume
      tier (BACKLOG).

## M0 status: built, not yet proven live

Done: template scaffold, data ingest (BTC, ETH, SPY, QQQ, GLD, TLT, append-only CSV), gym
(next-open fills, fees, slippage, long-only, 10,000 USD), 4 benchmark strategies, append-only
ledger + tries counter + git-history integrity check, daily runner + `.github/workflows/daily.yml`,
scoreboard (`python -m grimstrade.report --root trail [--backtest]`), owner README, MIT license.

## To finish M0 (needs someone with GitHub access)

- [ ] Merge this branch to `main` (via PR), then run "Daily paper trading" once by hand
      (workflow_dispatch). Unverified live: Kraken/Coinbase/Yahoo/Stooq formats are from docs,
      tested only on fixtures (dev container can't reach them). Yahoo may 429 from Actions; Stooq is
      the fallback. Check the first run creates the `paper-trail` branch and pushes to it.
- [ ] Check the Actions settings allow GITHUB_TOKEN write (contents: write is requested).
- [ ] If the `protect-main` ruleset is ever widened to all branches, exempt `paper-trail`
      (the bot pushes there directly).

## Assumptions (see docs/DECISIONS.md)

- CSV + stdlib only (no parquet/pandas). Raw prices; dividends not credited yet.
- Bot commits to orphan branch `paper-trail` because `main` requires PRs.
- Costs: crypto 60 bps fee (was 25 until the audit, G3) + 5 bps slip; ETFs 0 fee + 2 bps slip; 1% rebalance band.
- Decisions at ~22:30 UTC see crypto bars through yesterday (today's still open) and ETFs through
  today. Fills show up a day later, once the fill bar has closed and been stored.
- A run with no new data since a strategy's last decision writes no new decision.
- Gymnasium env wrapper deferred (BACKLOG).

## M1: done (merged 2026-11-12, PR #3)

Brief: chief-of-staff/briefs/grimstrade-m1.md. The details are in PR #3 and docs/DECISIONS.md.

- Live in paper (they start at the next daily run, 22:30 UTC): `ts_momentum`, `xs_momentum`,
  `vol_target_spy`, `risk_parity`, `crypto_mean_reversion`, next to the four M0 yardsticks.
  Funding-rate carry is in BACKLOG.
- Scoreboard has a deflated Sharpe column (after 30 days). N counts the research lane's tries,
  each recorded by identity in `ledger/research_tries.jsonl` on paper-trail.
- `reports/weekly.md` (owner, plain language) and `reports/backtest.md` (hindsight, kept apart)
  are written every run.
- Reviews by Fable: DSR maths, each strategy against its paper, and the final PR review; all
  findings fixed and re-verified.
- Worth watching after the first M1 run (2026-11-12 22:30 UTC): the daily job is green, 9
  strategies in `ledger/tries.jsonl`, and `weekly.md` reads well.
- Merging `audit-1` may conflict in `ledger.py`/`gym.py` (M1 added the research-try functions,
  the `APPEND_ONLY` tuple and a finite-weights check in `validate`).

PR #3 merged (rebase) 2026-11-12 01:48 UTC; CI on main green; 114 tests pass. Owner: merge the
small docs PR that brings this section to main (branch `m1-wrapup`).
