# Next steps

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

## M1 (branch `m1`, brief: chief-of-staff/briefs/grimstrade-m1.md)

Goal: classic strategies live in paper, deflated Sharpe in the scoreboard, weekly one-screen
summary (`reports/weekly.md`), backtests reported apart from the forward record.

Done:
- Draft PR #3. `signals.py` (trailing return, realized/EWMA vol). `ts_momentum` live + tested.
  Strategies' try notes live in `strategies.NOTES`. `xs_momentum` (J&T 6/6, top third) live.
  `vol_target_spy` (10%, 1-month vol) and `risk_parity` (inverse vol, 3y window) live.
  `crypto_mean_reversion` (Connors RSI(2)) live. Parameters recorded in DECISIONS.
  Funding-rate carry -> BACKLOG (gym is long-only spot; carry needs a short perp leg).
  `stats.py` deflated Sharpe (matches the paper's example), column in scoreboard; try-count rule
  in DECISIONS (`ledger.research_tries`). Runner writes `reports/backtest.md` (two windows).

  `weekly.py` writes `reports/weekly.md` every run (plain language, tested). README points the
  owner at weekly.md and backtest.md.

Stopped 2026-11-11 ~23:20 UTC: usage limit reached. Resumed 2026-11-12 01:32 UTC: checks green (98 tests).

Fable reviews done 2026-11-12. DSR maths: correct (paper example reproduced). Fixed try-count
undercounting (disjoint ideas/variants, statuses like "rejected", blank lines in tables, bullets,
main not read; plus a never-shrinking high in `ledger/research_tries.jsonl`) and V[SR] now includes
research variants' Sharpes. Strategy faithfulness: no look-ahead. Fixed xs_momentum cohorts
re-picked the day after a weekday month end; DECISIONS now records daily re-deciding, the
one-day-late crypto fills (BACKLOG: 00:05 UTC run), vol_target as Harvey et al. style, RSI<10
as the looser variant. M1 strategies had not run yet on paper-trail, so these are not new tries.

Was doing (2026-11-12, new Fable rule in the brief): Fable subagent reviews of (a) the deflated-Sharpe
maths in `stats.py` and (b) each strategy's faithfulness to its paper; then fix findings; then a
Fable final review of PR #3.

Next (in order):
- Fable final review done: merge after fixes. Fixed: research tries recorded by identity (not a
  count) and reports read-only; weekly yardstick window off by one day; weekly wording no longer
  overclaims (strong needs beating every yardstick, nothing proven before 6 months); one broken
  strategy no longer stops the others or the reports; NaN weights rejected; runner tests isolated.
- Mark ready; try `gh pr merge --rebase --delete-branch`.
