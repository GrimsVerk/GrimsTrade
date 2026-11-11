# Design: grimstrade

## Summary

Every day after the US close a GitHub Actions job fetches daily bars, asks every live strategy for
target weights, appends those decisions to an append-only ledger and commits it **before** the
outcome exists. The gym fills each decision at the **next** bar's open with fees and slippage and
keeps score per strategy against the benchmarks.

## Core flows that must always work

- Daily run: fetch -> decide -> append ledger -> replay portfolios -> scoreboard -> commit.
- Ledger lines are never rewritten (a test and the runner both check git history).
- A decision never sees a bar that closed after it, and never fills at a price from before it.

## Parts (`src/grimstrade/`, each removable)

- `data.py`: `Bar`, universe, bar timing, CSV store (`data/bars/<SYM>.csv`, append-only).
  `sources.py`: keyless public fetchers (Kraken, Coinbase for crypto; Yahoo chart, Stooq for ETFs).
- `gym.py`: simulated broker. Event replay over bar opens/closes. Long-only, no leverage,
  fractional units, 10,000 USD start. `backtest()` makes historical decisions with the same rules.
- `strategies/`: one file per strategy, `decide(history) -> (weights, reason)`. `LIVE` lists the ones
  the runner calls.
- `ledger.py`: `ledger/decisions.jsonl` (one line per decision) and `ledger/tries.jsonl` (one line
  per strategy ever tried, for the deflated Sharpe).
- `report.py`: scoreboard (return, Sharpe, max drawdown, turnover) per strategy.
- `run_daily.py`: the entry point, `uv run python -m grimstrade.run_daily --root trail`.

## Timing rules (no look-ahead)

- Crypto daily bar `d` (UTC) opens `d 00:00` and closes `d+1 00:00`.
- ETF bar `d` is treated as open at `d 13:30 UTC` (earliest real open) and closed at `d 21:00 UTC`
  (latest real close), so both DST cases are conservative.
- A strategy at decision time `T` sees only bars with close <= `T`. Its order for each asset fills at
  the open of that asset's first bar with open > `T`. Crypto trades every day; ETFs only on bars
  that exist (weekends/holidays just have no bar).
- Ingest stores only bars that have closed (plus 15 min), and never changes stored rows.

## Where the record lives

The `paper-trail` branch (orphan, data only) holds `data/`, `ledger/`, `state/`, `reports/`. The
daily job checks it out into `trail/`, runs, and pushes it. Code changes go to `main` via PRs, so the
`main` PR rule never blocks the bot. Locally: `git worktree add trail paper-trail`.

## Costs (defaults in `gym.py`)

Crypto: 25 bps fee + 5 bps half-spread/slippage. ETFs: 0 fee + 2 bps. A trade smaller than 1% of
equity is skipped (rebalance band), except full exits.

## Benchmarks (what "making money" must beat)

Buy-and-hold BTC, buy-and-hold SPY, 60/40 SPY/TLT, equal weight of the universe.

## Strategy ladder

1. Baselines: the benchmarks through the gym (M0).
2. Classic: time-series momentum (Moskowitz, Ooi, Pedersen 2012), cross-sectional momentum
   (Jegadeesh & Titman 1993), volatility targeting, risk parity, crypto short-term mean reversion,
   crypto funding-rate carry.
3. ML: gradient boosting on engineered features, purged + embargoed CV (López de Prado).
4. Deep / GPU (5080): fine-tune a time-series foundation model (Chronos / TimesFM / Moirai class) in
   bf16; RL (PPO) in the gym for sizing and combining signals (experiment, raw-price RL overfits).
   NVFP4 mainly to run a ~30B local LLM for reading news.
5. LLM research desk: Claude sessions write theses with dated, checkable predictions, scored in the
   ledger (hit rate, Brier score).

## Idea lab

`research/ideas.md`: one line per idea with status (new / testing / live / dead + why); dead ideas
stay counted. Each idea gets a hypothesis card: claim, why, test, pass bar. Protocol: backtest on a
train period, check the held-out period once, forward-paper only if it passes. Mine first: Kelly /
fractional Kelly, random matrix theory, HMM regimes, Hawkes processes, fractional differentiation,
path signatures, optimal stopping, information theory, TDA; then econophysics and ecology. Sources:
arXiv q-fin, SSRN, JF/JFE classics, AQR and Man Group research.

## Graduation bar (before real money is even discussed)

At least 6 months of forward paper trading, beats the benchmarks after costs, deflated Sharpe
significant given the number of strategies tried, max drawdown the owner can stomach. Then the owner
decides.

## Milestones

- **M0** scaffold, data ingest for the starting universe, gym, ledger, daily runner, benchmarks live.
- **M1** classic strategies live in paper; deflated Sharpe; weekly one-screen scoreboard on the Desk.
- **M2** idea lab running; first token-burn research run.
- **M3** ML + GPU models (5080); LLM research desk with scored predictions.
