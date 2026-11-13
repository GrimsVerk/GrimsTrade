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

- Done: plan, protocol section.
- Doing: environment (`research/lib/rl_env.py`) with gym-equivalence and look-ahead tests.
- Next: agents (`research/lib/rl_train.py`), walk-forward runs, write-up.
