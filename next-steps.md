# Next steps

## Health 1 (branch `health-1`, draft PR, not merged): live check of the daily runs, 2026-11-17

Checked runs 2026-11-12 to 2026-11-17 (logs, `paper-trail` ledger, bars, replayed fills).

- Healthy: all 11 live strategies (9 + presets Careful, Middle) decided on every run with new
  data; no duplicates, no NaN or invalid weights. Bars: BTC/ETH every day to 2026-11-16, ETFs
  every session to 2026-11-16 (only market holidays missing). Kraken + Yahoo every run, no Stooq
  fallback, no 429, no problems recorded; 3 revisions under 1 bp. Every decision's orders filled
  at the first open after it; equity matches the bars.
- Fixed here: `reports/weekly.md` showed the presets by code name (`weekly.PLAIN` lacked them).
  Test: `test_every_live_strategy_has_a_plain_name`.
- Watch: the 22:30 UTC cron fires at 02:00-04:40 UTC (GitHub delay). No look-ahead, but the
  crypto bar of the run's own day opened before the decision, so crypto orders fill about 22 h
  later (next day's 00:00 open) instead of 1.5 h; backtests still decide at 22:30 (`DECIDE_AT`).
  Decide whether to accept this or move the run (DECISIONS) before comparing live and backtest.
- Watch: fully invested `equal_weight` (Bold) cannot top up crypto at 00:00 (no cash; ETF sells
  happen at 13:30 and each ETF is inside the 1% band), so it drifts until an ETF leaves the band.
  Same family as audit G2 (keep an unfilled buy pending).
- `next-steps.md` on `main` still lists audit-1 (PR #5) as waiting for review; it is merged.

## G2: an unpaid buy waits for cash (branch `g2-pending-buy`, draft PR #29, not merged)

Fix for audit G2 and the 2026-11-17 health-check symptom (fully invested `equal_weight` could
not top up crypto). Rule and why: `docs/DECISIONS.md` (2026-11-17, audit G2). Code:
`gym._execute`. Tests: `tests/test_audit_gym.py` (the G2 test is no longer xfail; the drifting
case runs at 22:30 and at the late-cron 03:00).

- [ ] After merging: the first run replays every score with the new rule. Expect `equal_weight`
      and `xs_momentum` to move by a couple of dollars and their backtests a little (DECISIONS).
      No ledger line or bar changes.

### For the owner

- The rule changes the live gym: merging is your call. Nothing else needs you.

## G4: ETF dividends paid as cash (branch `g4-dividends`, draft PR #30, not merged)

Fix for audit G4 (dividends half; cash still earns nothing). Rule and why: `docs/DECISIONS.md`
(2026-11-17, audit G4). Code: `data.py` (dividend store), `sources.yahoo_dividends`,
`run_daily._dividends` and `check_record`, `gym.simulate(dividends=...)`. Tests:
`tests/test_dividends.py` (offline, fixture `tests/fixtures/yahoo_dividends.json`, hand-made in
Yahoo's format).

- [ ] After merging: the first daily run creates `data/dividends.csv` on `paper-trail` with
      every stored ETF's payouts since its first stored bar (on 2026-11-17: SPY 8, QQQ 8, TLT 23,
      GLD none). Check the log shows `+N dividends (yahoo)` and no "dividends not fetched".
- [ ] After merging: backtests move up once (60/40 about +4.9% over the stored span); tell the
      research lane their fund baselines were missing dividends.

### For the owner

- The rule changes the live gym and the daily runner (one more Yahoo request per ETF per run):
  merging is your call.

## Crypto fee by 30-day volume tier (branch `fee-tiers`, draft PR #32, not merged)

Replaces the flat 0.60% crypto fee with Kraken Pro's taker schedule by each strategy's own
30-day crypto volume. Schedule, date read and why: `docs/DECISIONS.md` (2026-11-18). Code:
`gym.Costs.fee_at`, `gym.KRAKEN_TAKER`, `gym._execute`. Tests: `tests/test_audit_gym.py`
(the two fee tests), `tests/test_gym.py`.

- [ ] After merging: the first run replays every score with the tiers (`buy_hold_btc` live
      about -0.2%; `crypto_mean_reversion` backtest about +3.8%). Tell the research lane: a
      backtest's crypto fee is now 0.38-0.80% by how much it trades, not a flat 0.60%.
- [ ] Re-read kraken.com/pro/fees now and then; a change needs a new DECISIONS entry.

### For the owner

- Changes the live gym's costs: merging is your call. If you would trade crypto elsewhere,
  that venue's schedule goes in `gym.KRAKEN_TAKER`'s place.

## Cash interest (branch `cash-interest`, draft PR #61, not merged)

Idle cash earns the 13-week T-bill rate (Yahoo `^IRX`), accrued daily, in the live record from
the first run with this code and in backtests over all stored rates; Sharpe is measured above
that rate. Rule and why: `docs/DECISIONS.md` (2026-11-18, cash interest). Code: `rates.py` (store,
knowledge times), `gym.simulate(rates=...)`, `report.py` plumbing, `run_daily._rates`. Tests:
`tests/test_cash_interest.py` (offline, fixture rates). Train-period effect (PR #61): CAGR
`tsmom12` +17.64% -> +18.19%, `sixty_forty` +8.09% -> +8.63%; Sharpe above T-bills is lower for
every book (convention change, not a loss).

- [ ] After merging: the first daily run creates `data/rates.csv` on `paper-trail` with `^IRX`
      closes since the first stored bar. Check the log shows `rates: +N (yahoo ^IRX)` and no
      "rates not fetched".
- [ ] Rebase notes: PRs #29 (G2), #30 (G4) and #32 (fee tiers) touch the same `simulate`
      signature and `report.py` lines; conflicts are mechanical (keep both parameters). G4's
      `weekly.md` sentence "cash earns no interest" must then say cash earns the T-bill rate.

### For the owner

- Merging is your call: it changes every score once (interest on cash, Sharpe above the cash
  rate). Open questions in PR #61: a broker spread below the T-bill rate; should the research
  harness also measure Sharpe above T-bills; a second rate source (US Treasury CSV).

## forward-1 (done 2026-11-18 night, branch `forward-1` from `main`, draft PR #67 -> `main`)

WIDER lane (new method): a forward-only shadow registry. Each candidate rule is frozen (hash of
code + parameters + data source) with its metric, bar and minimum sample written at freeze, and
scored only on bars that start after the freeze. Research only; no change to the daily runner,
its schedule or workflows. Design `docs/forward-registry.md`; code `src/grimstrade/forward.py`
(`python -m grimstrade.forward table|score`); tests `tests/test_forward.py` (freeze,
append-only, refusal of pre-freeze bars, hash mismatch, power calculator, verdict read once);
proposals `research/forward/candidates.jsonl` (made by `research/forward/propose.py`; NOT
frozen); DECISIONS entry 2026-11-18 marked PROPOSED.

- Years needed at 80% power, alpha 0.025 each (0.10 over the four): `carry-3-band@1` 12.7
  (7.3 at a lone 0.10; train Sharpe 0.79 assumed, held-out was -0.65); `fomc-bond-drift@1` 78
  (papers' 12 bps a meeting); `coin-stop-0.25@1` 26 (15/21 episodes; ~55 counting only
  independent episodes); `eu-monthly-vs-weekly@1` 32 (signal-to-noise 0.50 from eu-3's p 0.03).
- Finding: only carry can be judged forward in useful time; the other three need decades, so
  their decisions should be taken on other grounds now (stop = risk choice; monthly clock's fee
  saving is mechanical; FOMC drift descriptive only).
- Before any freeze: each rule needs a forward adapter (the research scripts stop at
  `TRAIN_END`/`HELD_END` on purpose); the adapter's files join the hash, so the proposal hashes
  change at freeze. Carry also needs weekly snapshots of the perp lists (delisted coins vanish
  from later downloads).
- Doing: nothing. No process running.
- [ ] **Owner decision: freeze these and schedule the scorer?** (1) adopt the registry rules
      (DECISIONS 2026-11-18); (2) which to freeze (recommended: `carry-3-band@1` for a verdict;
      the other three descriptive only, or not at all); (3) a lane to write the adapters and
      freeze; (4) whether a weekly job (owner-made schedule) runs `forward score`.

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
      (D6, needs a key: owner's call); crypto fee by volume tier (BACKLOG). G2: branch
      `g2-pending-buy`.

- [ ] Open findings to build next: dividends (G4: branch `g4-dividends`); a second ETF source, Stooq is dead
      (D6, needs a key: owner's call); keep an unfilled buy pending (G2); crypto fee by volume
      tier (branch `fee-tiers`).

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

- CSV + stdlib only (no parquet/pandas). Raw prices; dividends paid as cash on the ex-date (G4).
- Bot commits to orphan branch `paper-trail` because `main` requires PRs.
- Costs: crypto Kraken Pro taker fee by 30-day volume, 0.38-0.80% (flat 60 bps after audit G3, 25 before) + 5 bps slip; ETFs 0 fee + 2 bps slip; 1% rebalance band.
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
