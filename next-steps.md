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

## M1 (branch `m1`, brief: chief-of-staff/briefs/grimstrade-m1.md)

Goal: classic strategies live in paper, deflated Sharpe in the scoreboard, weekly one-screen
summary (`reports/weekly.md`), backtests reported apart from the forward record.

Done:
- (nothing yet)

Doing:
- Shared signal helpers + time-series momentum.

Next (in order):
- Cross-sectional momentum, volatility targeting, risk parity, crypto mean reversion.
- Funding-rate carry -> BACKLOG (gym is long-only spot; carry needs a short perp leg).
- Deflated Sharpe in the scoreboard; tries = ledger/tries.jsonl + research lane's tries.
- Backtest report (`reports/backtest.md`), weekly summary (`reports/weekly.md`).
- Mark PR ready, try `gh pr merge --rebase --delete-branch`.
