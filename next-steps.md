# Next steps

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
- Costs: crypto 25 bps fee + 5 bps slip; ETFs 0 fee + 2 bps slip; 1% rebalance band.
- Decisions at ~22:30 UTC see crypto bars through yesterday (today's still open) and ETFs through
  today. Fills show up a day later, once the fill bar has closed and been stored.
- A run with no new data since a strategy's last decision writes no new decision.
- Gymnasium env wrapper deferred (BACKLOG).

## M1 (next)

Classic strategies live in paper (time-series momentum, cross-sectional momentum, vol targeting,
risk parity, crypto mean reversion), each registered in `ledger/tries.jsonl`; deflated Sharpe in
the scoreboard; weekly one-screen summary for the owner.

## Macro 1 (research run, branch `macro-1`, started 2026-11-13 ~01:40 UTC)

Brief: `chief-of-staff/briefs/grimstrade-macro-1.md`. Question: does knowing the macro phase
(Fed policy, real rates, yield curve, money supply, credit spreads, the Bitcoin halving cycle)
add anything over `tsmom12`? Write-up: `research/macro-1.md`.

- Done: look-ahead-safe macro layer (`research/lib/macro.py`, ALFRED vintages; tests in
  `tests/test_macro_asof.py`), protocol section "Macro tests", six cards tested on train, all
  fail their bar (halving: passes on numbers but fails bar 2 and is not believed: three winters,
  folklore window). Feature skill table, write-up `research/macro-1.md`. Held-out year unused.
  Draft PR #16 (`macro-1` -> `research-3`), not merged.
- Doing: nothing.
- Next: macro features as regime inputs for the RL agent (list in `research/macro-1.md`). The
  owner may want to read the halving section before anyone trades a "four-year cycle".

## RL 1 (research run, branch `rl-1`, started 2026-11-13 ~01:50 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-1.md`. Question: can an RL agent (PPO, policy shared
across assets, prices + macro inputs) beat `tsmom12` out of sample? Plan and results:
`research/rl-1.md`; rules: `research/protocol.md` "Reinforcement-learning tests".

- Done: plan and protocol section before code; gym-exact batched simulator and environment
  with tests; 5 agents x 10 seeds x 13 walk-forward folds trained on the RTX 5080; evaluated
  through the real gym, 70 rows in `research/tries.md`; tables `research/results/rl-1.md`;
  write-up `research/rl-1.md`. Answer: no. All five fail (Sharpe 0.57-0.71 against
  `tsmom12` 0.99 out of sample 2000-2025, 0 of 50 seeds ahead). Held-out year unused.
  Draft PR #17 (`rl-1` -> `macro-1`), not merged.
- Doing: nothing. No process running.
- Next (not started): residual-policy rung (tsmom12 plus a bounded tilt, reward relative to
  tsmom12, coin cap); card and bar first. Details in `research/rl-1.md`, "What the next rung
  would need".

## RL 2 (research run, branch `rl-2`, started 2026-11-13 ~05:05 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-2.md`. Question: does an RL agent constrained to tilt
`tsmom12` (residual policy, active reward, early stopping, one variant pooled over 33 markets)
beat `tsmom12` out of sample? Plan and results: `research/rl-2.md`; rules: `research/protocol.md`
"Residual RL tests".

- Done: residual environment + tests (zero tilt == `tsmom12` exactly), trainer with purged
  validation and early stopping, on-chain inputs for coins (`research/lib/onchain.py`, as-of
  test), 4 variants x 10 seeds x 13 folds, evaluated through the gym, 56 rows in
  `research/tries.md`, tables `research/results/rl-2.md`, write-up. Answer: no. All four fail
  (Sharpe 0.96-0.98 against 0.99; active share 1.8-2.7%; at most 1 of 10 seeds ahead).
  Held-out year unused. Draft PR #18 (`rl-2` -> `rl-1`), not merged.
- Doing: nothing. No process running.
- Next (not started): planted-signal control of the residual pipeline (can it find a known
  weak signal?); then funding rates / basis for coins, which need shorting or futures in the gym.

## Ideas 1 (research run, branch `ideas-1`, started 2026-11-13 ~06:00 UTC)

Brief: `chief-of-staff/briefs/grimstrade-ideas-1.md`. Test eight YouTube rules (harvest 1) by the
protocol: cards in `research/cards/yt-1.md` (fixed before any test), runner
`research/lib/idea_yt.py`, write-up `research/ideas-1.md`. Status: cards written; testing next.
