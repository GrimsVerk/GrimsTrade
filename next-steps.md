# Next steps

## combo-2 (DEEPER lane, night 2026-11-18, branch `combo-2`, draft PR #75 -> `combo-1`, never merged by agents)

Write-up `research/combo-2.md`. `origin/cash-interest` (#61) is merged into this branch (merge
commit 957fdd1, not cherry-picked); `harness.run(rates=...)` and `harness.bill_rates()` added
(default unchanged). Costs: protocol 25 + 5 bps crypto, 2 bps ETFs.

- DONE 2026-11-18. Step 1 `combo-cash`: combo-1's map and blends rerun with T-bill cash, 14
  `robustness` rows. No verdict changes: `blend-ws` 1.16 vs `tsmom12` 1.08 (p 0.051; above
  T-bills +0.06, p 0.108), still behind 2022-25; `blend-iv` now fails 4 bars. Map signs and pair
  correlations unchanged; `trend-vol` ties `tsmom12` against 0 (behind above T-bills).
- Step 2 `cofall-dbc` (DBC slot when SPY and TLT trends are both down; T-bill slot rejected as
  identical to cash with interest): 1.07 vs 1.08 (p 0.85), 2022 -1.7 points, fails; 1 `variant`
  row, family now 73. Long-run description 1962-2025: 35 co-fall months, T-bills beat every
  commodity proxy.
- Step 3 verdict: close the combo line; nothing worth a held-out year. Next: `stop-reentry`
  (combo-1's lane 1); owner decides #61.

## combo-1 (DEEPER lane, night 2026-11-18, branch `combo-1`, draft PR -> `main`, never merged by agents)

Task: failure map of the most credible models/overlays against `tsmom12` (where each loses:
eras, trend reversals, chop, crash speed, the 2022 rate shock), the complementarity story
(correlation of excess returns by regime), then at most 2 carded combinations chosen from the
map by a stated rule, train only, every try logged, then a verdict. Write-up `research/combo-1.md`.

- Base is `main`, which has no research stack: `research/` was copied unchanged from
  `origin/coin-cap-3` (it holds the deep-1 atlas code and series loader). `src/` stays `main`'s;
  main's gym charges 60 bps on crypto, the research protocol 25 + 5 bps, so every combo-1 replay
  passes the protocol costs explicitly (`lib/combo1_*.py`).
- Inputs not rebuilt (saved equity curves of finished lanes, copied read-only into
  `<cache_root>/derived/combo-1/inputs/`): `where-vol` (trend-where), `stop-0.25` (cointop-1);
  deep-1's sleeve series; carry-3's `band` train series.
- DONE 2026-11-18. Map: four of six models (`trend-vol`, `stop-0.25`, `inverse-vol`,
  `sixty-forty`) are one de-risking bet (excess correlations +0.5..+0.9; win falls, lose the
  turn); `where-vol` fails apart from them (0.00 with `stop-0.25`); `band` is the only one
  uncorrelated with `tsmom12` (out of gym). Card: two blends. `blend-ws` (`where-vol` +
  `stop-0.25`, equal risk) 1.13 vs 1.05 (p 0.059), worst loss 28.9%: closest miss so far, fails
  the family bar (p < 0.0014) and eras (behind 2022-25). `blend-iv` 1.07, worst loss 44.4%:
  fails. 8 rows in `research/tries.md`; held-out unspent. Next lanes (in `research/combo-1.md`):
  `stop-reentry` (coin stop + re-entry rule, 21 episodes), `combo-cash` (map and blends with
  T-bill cash), a long-only complement for the stock-bond-together regime (DBC, T-bill slot).

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
