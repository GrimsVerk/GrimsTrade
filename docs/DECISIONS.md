# Decisions: grimstrade

Settled decisions and why, newest first. Don't relitigate; update an entry if the owner changes it.

- 2026-11-12: Counting tries for the deflated Sharpe (N). N = strategies in `ledger/tries.jsonl`
  (benchmarks included; live strategies count before their first run) + the research lane's
  tries. Research tries = distinct (idea, variant) rows of `research/tries.md` (columns: date |
  idea | variant | period), unioned over the code checkout and every local/remote `research-*`
  branch; a held-out check of a variant already counted is not a new try. If `research/ideas.md`
  shows more ideas with status testing/live/dead than that, the ideas count is used instead.
  Dead tries stay counted forever. Why: overcounting only makes us more cautious; undercounting
  is the dishonest direction. `ledger.research_tries` implements it.
- 2026-11-12: Deflated Sharpe inputs. Per-day Sharpe, skew and kurtosis of each strategy's daily
  equity returns; the variance of Sharpes across trials is the larger of 1/T (pure luck over T
  days) and the sample variance of the Sharpes on the same table. Shown only after 30 days. The
  backtest report is deflated with the same N.

- 2026-11-12: M1 classic strategies use the papers' standard parameters, never tuned on our data
  (every tuning run would be a hidden try). Where the paper doesn't fit a 6-asset, long-only,
  unlevered gym, the textbook default was picked once, here:
  - `ts_momentum` (MOP 2012): 12-month return sign, 40% vol target, EWMA vol with 60-day center
    of mass, 1/N per asset; negative signal = cash (no shorts); per-asset size capped at 1/N.
  - `xs_momentum` (J&T 1993): J=6/K=6, month-end formation, no skip week; winners = top third
    (a decile of 6 assets is empty); losers not shorted.
  - `vol_target_spy`: SPY only (the market portfolio of Moreira & Muir), 10% target (Harvey et
    al. 2018), 21-trading-day realized vol, capped at 100%.
  - `risk_parity` (AFP 2012): inverse vol over the whole universe, 3-year window of daily
    returns, an asset joins after 1 year of history; unlevered (the paper levers).
  - `crypto_mean_reversion`: Connors RSI(2) < 10, close above 200-day SMA, exit when close above
    5-day SMA; BTC and ETH, half each.
  - Vol is annualised per asset class: 365 bars/yr crypto, 252 ETFs (MOP use 261; the
    difference is under 2%). The Sharpe convention (365 days) is unchanged.
- 2026-11-12: Funding-rate carry is not built in M1. A keyless source exists (Kraken Futures
  `historicalfundingrates`), but carry needs a short perpetual leg and the gym is long-only spot.
  In BACKLOG.

- 2026-11-11: Daily bot writes to the `paper-trail` branch, not `main`. Why: `main` requires PRs;
  a data-only branch keeps the record's history clean and CI quiet.
- 2026-11-11: Bars and ledger are CSV/JSONL, stdlib only. Why: diff-able in git (the tamper
  evidence), no dependencies to break the unattended runner.
- 2026-11-11: Prices are raw (not dividend-adjusted); dividends are not credited yet. Why: adjusted
  history changes retroactively, which breaks append-only data. Understates SPY/TLT a little.
- 2026-11-11: Sharpe uses 365 calendar days and a zero risk-free rate. Why: crypto trades every day;
  one convention for all strategies.
- 2026-11-11: No real-money broker, ever, without the owner's explicit decision. No keys in git.
- 2026-11-11: License is MIT. Why: owner's ruling.
