# Test protocol (fixed 2026-11-12, before any idea was tested)

The rules every idea test follows. Changing a rule after seeing a result is not allowed; a new
rule gets a new dated section at the bottom and applies only to later tests.

## Data

- Longest keyless history: SPY from 1993-01-29, QQQ 1999-03-10, TLT 2002-07-30, GLD 2004-11-18
  (Yahoo); BTC from 2012-01-01 (Bitstamp to 2015-07-19, Coinbase after); ETH from 2016-05-18
  (Coinbase). Fetched by `lib/fetch.py` into git-ignored `data/`.
- **Total-return prices are the primary data.** ETF bars are dividend-adjusted. Reason: raw TLT is
  flat over 23 years (0.99x) while its holders earned 2.28x with coupons; raw prices would make
  any rule that avoids bonds look clever for the wrong reason. The live paper system still trades
  raw prices, so every finalist is also run on raw prices (`robustness`), and crediting dividends
  is a request to the M1 lane (see README).
- Cash earns 0 (the gym's rule). This is harsh on rules that sit in cash in the 1990s and 2000s,
  when cash paid 3-6%. It is kept because it is what the gym does; it biases against timing rules.
- Fills, fees and slippage come from `grimstrade.gym.simulate`, unchanged: next open, 30 bps a
  side in crypto, 2 bps a side in ETFs, 1% rebalance band.

## Periods

- **Train:** decisions 1994-02-01 .. 2025-11-09. Bars after 2025-11-10 are not loaded.
- **Held-out:** decisions 2025-11-11 .. 2026-11-09. Checked at most once per idea, only for an
  idea that passed on train, and logged in `tries.md`. The harness refuses a second look.
- **Eras** (reported separately, always): 1994-99, 2000-09, 2010-16, 2017-21, 2022-25.
- **Stress windows** (total return inside each): dot-com bust 2000-03-24..2002-10-09, 2008 crisis
  2007-10-09..2009-03-09, covid crash 2020-02-19..2020-03-23, 2022 rate shock
  2022-01-03..2022-10-12, crypto winters 2013-12-04..2015-01-14, 2017-12-17..2018-12-15,
  2021-11-10..2022-11-21.

## Conventions shared by every strategy and baseline

- An asset can be held once it has one year of bars (252 ETF bars, 365 crypto bars).
- Signals are re-decided weekly, on Friday's close; the same weights are repeated on other days.
- Sharpe: daily returns on all calendar days, 365 days a year, zero risk-free rate (the repo's
  convention). Standard errors by Mertens (2002). Differences between two strategies: paired
  stationary bootstrap (mean block 20 days, 2,000 draws), one-sided p-value.
- Anything with fitted parameters is walk-forward: fitted only on bars before the decision,
  refitted on a fixed schedule written on the card.

## Baselines and plain twins

Benchmarks (from `docs/DESIGN.md`): buy-and-hold BTC, buy-and-hold SPY, 60/40 SPY/TLT, equal
weight of the eligible assets. Plain twins that an exotic idea has to beat to justify itself:

- `sma200`: each asset's equal slot is held when its close is above its 200-trading-day average,
  else cash.
- `tsmom12`: the slot is held when the asset's 365-day return is positive, else cash.
- `inverse-vol`: weights proportional to 1 / (60-day-half-life EWMA volatility), summing to 1.

Every card names its twin. An idea that only matches its twin is dead: the twin is simpler.

## Out-of-universe sets (chosen before any test)

An idea built on our six assets is also run, unchanged, on assets it was not designed on:

- **Other ETFs:** IWM, EFA, EEM, IEF, LQD, VNQ, DBC, SLV (small caps, foreign and emerging
  stocks, mid-term Treasuries, corporate bonds, real estate, commodities, silver).
- **Other coins:** LTC, XRP, BCH, ETC, XLM, DASH: coins that were among the largest in January
  2018 and that Coinbase or Bitstamp list with long history. Picked from an old ranking on
  purpose: picking today's large coins would only test the winners.
- **Other markets (price indexes, local currency, no dividends):** S&P 500 index 1962-1993 (the
  30 years before SPY existed), Nikkei 225 from 1965, FTSE 100 from 1984, DAX from 1988. Caveat:
  Yahoo's index "open" before about 2010 is often the previous close, so a next-open fill there
  is a fill at the signal's own close (slightly kind; the same for strategy and twin).

How the sets are run: rules that act on one asset at a time run on a set as an equal-slot
portfolio (ETFs, coins) and on each index alone (the S&P 500 index cut at 1993-01-28). Rules that
build a portfolio (kelly-shrunk, universal-portfolio) run the four indexes as one portfolio with
the S&P 500 index kept to 2025; after 1993 that leg overlaps SPY and is flagged.

## Pass bar (default; a card may be stricter, never looser)

An idea **passes train** only if all of these hold:

1. Sharpe on the six assets, full train period, beats its plain twin with bootstrap p < 0.10.
2. It is ahead of the twin in at least 3 of the eras both have data for (4 if all 5 exist).
3. Max drawdown is not more than 5 points worse than the twin's.
4. Out-of-universe: the Sharpe difference to the twin has the same sign in at least two of the
   three out-of-universe sets (as far as the idea applies to them; the card says which).
5. It beats the equal-weight benchmark on Sharpe (otherwise there is no reason to run it).

Only then is the held-out year looked at, once. Held-out passes if the idea is not behind its twin
there (12 months cannot prove anything; it can only fail to contradict). Pass on both makes the
idea an M3 paper candidate. Everything else is dead or parked, with the reason in `ideas.md`.

## Counting tries

Every configuration run through the harness appends a row to `tries.md` at the moment it runs:
`variant` (could have been selected), `baseline`, or `robustness` (same configuration on other
data, costs or prices, after the choice was made). Cards fix the variants in advance; the number
of variants per idea is kept small because each one raises the bar the deflated Sharpe sets.

## Disclosures

- 2026-11-12: while smoke-testing the harness, one unlogged run of the `sma200` twin on 2017-2025
  raw prices was seen (Sharpe 1.38). It is a baseline, not an idea, and is re-run and logged under
  this protocol.
- 2026-11-12: a data sanity print covered the whole cache and showed the largest one-day moves
  per symbol, two of which fall in the held-out year (GLD and SLV, 2026-01-30). No strategy
  result was involved. Sanity scripts now stop at the train cut.
