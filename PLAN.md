# GrimsTrade plan

Written 2026-11-11 by the Chief of Staff (Verkmester). Agent-facing. The repo agent folds this into the template's files when it scaffolds the repo.

## Intent (owner 2026-11-11)

- A trading agent that makes decisions on **real, live market data** but trades **only fake money**, in our own simulated broker ("the gym").
- Success = it makes money in that world, measured honestly, against real prices as they arrive.
- Plus a research side: read the literature, borrow ideas from other fields (maths first), find data sources and trading ideas.
- The owner won't run it day to day. The Chief of Staff is responsible. Big research runs happen when the owner has weekly usage left near the reset.
- No real money. Ever moving to real money is the owner's call alone, and only after the graduation bar below.
- Hardware for training: owner's RTX 5080 (16 GB, Blackwell, supports NVFP4). Be ambitious; be smart about memory.

## Core idea: the forward-test ledger

Backtests flatter (look-ahead, overfitting, survivorship). The honest test is the future.

- Every decision is written to an **append-only ledger** and committed to git **before** its outcome exists. Git history is the tamper-evident timestamp.
- The simulator fills orders at the **next** price after the decision, with fees, spread and slippage. No peeking.
- Every strategy ever tried is counted, so results can be corrected for how many tries it took (deflated Sharpe ratio).

## Architecture (each part can be ripped out)

1. **data/**: ingest daily bars into parquet. Start: BTC, ETH, SPY, QQQ, GLD, TLT, plus a few more liquid crypto and ETFs. Sources (verify they're free and allowed at build time): crypto exchange public APIs (Binance/Kraken/Coinbase), Alpaca market data (free tier, also has a free paper-trading account), FRED for macro. No API keys in git: GitHub Actions secrets / gitignored local file.
2. **gym/**: simulated broker + portfolio. Gymnasium-compatible interface so RL agents plug in later. Fees, spread, slippage, no leverage at first, long-only at first. Starting virtual capital 10,000 USD.
3. **strategies/**: each strategy is one file with one function: data up to t in, target weights out.
4. **ledger/**: append-only JSONL, one line per decision (time, strategy, weights, prices seen, reason). Never rewritten.
5. **runner**: a scheduled GitHub Actions job (repo is public, so minutes are free), once a day after the US close: fetch data, run every live strategy, write the ledger, commit. Plain Python. **No Claude in the loop**, so it costs no usage and runs when the desktop is off.
6. **reports/**: scoreboard per strategy vs benchmarks: return, Sharpe, max drawdown, deflated Sharpe, turnover. Weekly one-screen summary for the owner (Desk row).

Start with daily bars: cheap, robust, enough signal to learn from. Intraday only once daily works.

## Benchmarks (what "making money" must beat)

Buy-and-hold BTC, buy-and-hold SPY, 60/40 SPY/TLT, equal-weight of the universe. Beating cash is not success; beating these after costs is.

## Strategy ladder (tried-and-tested first)

1. **Baselines** (week 1): the benchmarks themselves, run through the gym, to prove the plumbing.
2. **Classic, well-documented**: time-series momentum / trend following (Moskowitz, Ooi, Pedersen 2012), cross-sectional momentum (Jegadeesh & Titman 1993), volatility targeting, risk parity, short-term mean reversion in crypto, crypto funding-rate carry.
3. **Machine learning**: gradient boosting on engineered features, with purged + embargoed cross-validation (López de Prado, *Advances in Financial Machine Learning*).
4. **Deep / GPU (5080)**: fine-tune a time-series foundation model (Chronos / TimesFM / Moirai class, a few hundred M params: fits easily in bf16). RL (PPO etc.) in the gym, mainly for position sizing and combining signals; raw-price RL overfits badly, so treat it as an experiment. NVFP4 is mostly an inference win: use it to run a larger local LLM (~30B class) for reading news cheaply.
5. **LLM research desk**: Claude sessions read news, filings and papers and write **theses with explicit, dated, checkable predictions**. Those go in the ledger too and get scored (hit rate, Brier score), just like strategies.

## Idea lab (research side)

- `research/ideas.md`: one line per idea, with status (new / testing / live / dead + why). Dead ideas stay counted.
- Each idea becomes a hypothesis card: claim, why it should work, test, pass bar. Fixed protocol: backtest on train period, check on held-out period once, then forward-paper only if it passes.
- Maths and other fields to mine first: Kelly criterion and fractional Kelly (sizing), random matrix theory (cleaning covariance), hidden Markov / regime models, Hawkes processes (order flow, crypto), fractional differentiation, path signatures (rough path theory), optimal stopping, information theory (entropy of returns), topological data analysis. Physics (econophysics) and ecology (predator-prey, diversity) as second wave.
- Sources: arXiv q-fin, SSRN, Journal of Finance / JFE classics, AQR and Man Group public research.

## Token-burn runs

- Before a run: `omarchy-agent-usage-claude`; only spend weekly usage that would otherwise expire.
- Runs are `claude --bg` sessions (never `claude -p` / SDK loops, see chief-of-staff decisions). Typical run: pick ideas from `research/ideas.md`, test them, write results, promote winners to live paper.
- The daily runner never uses Claude.

## Graduation bar (before real money is even discussed)

At least 6 months of forward paper trading, beats the benchmarks after costs, deflated Sharpe significant given the number of strategies tried, max drawdown the owner can stomach. Then the owner decides. Agents never connect a real-money account.

## Milestones

- **M0** scaffold from grimsverk-template v2 (Python): data ingest for the starting universe, gym, ledger, daily Actions runner, benchmarks live.
- **M1** classic strategies live in paper; weekly scoreboard on the Desk.
- **M2** idea lab running; first token-burn research run.
- **M3** ML + GPU models (5080); LLM research desk with scored predictions.
