# wide-18: `tsmom12` read in variance time (`vclock12`) and through a robust filter (`huber52`)

Lane wide-18, written 2026-11-24 about 23:45 UTC, **before any return of either rule below was
computed** (no dry run yet either). Candidates P1 and S1 of `research/wide-18.md`, step 1.

## What was seen before this card (disclosed)

Only the record: `tsmom12` 1.05 on the primary test; the trend-tune surface (6-12 months a flat
plateau, best of 98 settings +0.08, luck alone +0.17); `or3-12` / `arm3-12` (faster re-entry
leaks insurance through bear-market rallies); `e4` pooled +0.063 (not shown). No number of
either rule, on any data.

## Hypotheses

- **H1 (`vclock12`)**: market regimes turn over per unit of variance (information), not per
  calendar day. A trend window that holds a fixed amount of variance (one median year of the
  asset's own) re-enters faster after high-volatility crashes and exits no later in calm ones,
  and so beats the calendar window on Sharpe.
- **H2 (`huber52`)**: under fat tails a robust estimate of the year's drift flips less often on
  single jumps than the plain sum, so fewer whipsaws at the same insurance.

## Rules (frozen)

Both keep everything of `tsmom12` but the per-asset signal: `c.weekly(c.slots(signal))`, each
Friday an eligible asset (a year of bars) with signal true gets 1/n of the book (n = eligible
assets), else cash; gym costs, gym band, weights repeated daily, fills next open.

- **`vclock12` (variant)**: `lr` = the asset's daily log returns visible on the decision day,
  `B` = bars per year on its own clock (252 ETFs, 365 coins).
  1. Reference variance `V` = the median, over every window of `B` consecutive visible bars, of
     the window's sum of `lr^2` (the asset's median year of variance, expanding, causal).
  2. Window `k` = the smallest number of most recent bars whose `lr^2` sum reaches `V`, clipped
     to `[B // 4, 2 B]` and to the bars available.
  3. Signal: `sum(lr[-k:]) > 0`.
  If fewer than `B` returns are visible, the signal is `tsmom12`'s (365-day log return > 0).
- **`huber52` (variant)**: `w` = 5 bars (ETFs) or 7 (coins); `x` = the 52 log returns between
  closes `w` bars apart ending at the last visible close. `m` = median(x), `s` = 1.4826 x
  median(|x - m|); clip x to `[m - 1.345 s, m + 1.345 s]`; signal: mean(clipped x) > 0. With
  fewer than `52 w + 1` closes, or `s` = 0, the signal is `tsmom12`'s.
- No other setting is run. The clip constant (1.345, Huber's 95%-efficiency value), the median
  year and the window limits are stated, not tuned.

## Data, tests, costs

- Primary test: the six assets (SPY, QQQ, TLT, GLD, BTC, ETH), decisions 1994-02-01 ..
  **2025-10-31** (the lane's train cut; both books on the same window), total-return prices,
  gym costs. The held-out year is not loaded for decisions and not scored.
- Out of universe, signs only (`robustness` rows): `etf` (IWM, EFA, EEM, IEF, LQD, VNQ, DBC, SLV)
  and `idx` (S&P 500, Nikkei 225, FTSE 100, DAX price indexes, from 1962 or their first year).
- Comparator: `tsmom12`, re-scored with `log=False` on each set and window.

## Statistic and pass bar

- dSharpe = Sharpe(rule) - Sharpe(`tsmom12`), daily returns, 365 days, paired stationary
  bootstrap (20-day blocks, 2000 draws, seed 0; wide-16's `boot`). Two cash conventions on the
  six: cash at 0 (the protocol's, what `tries.md` logs) and above the 13-week bill.
- **Pass (each rule separately)**: z = dSharpe / SE >= **4.70** in both cash conventions on the
  primary test (`BAR.md`, N_eff 500), **and** dSharpe > 0 on `etf` and on `idx`. Anything else
  is a fail. The table also gives the correlation of daily returns with `tsmom12` and the edge
  4.70 x SE the rule would have needed at its own SE.
- Reported, not a pass: z >= 3.25 (the bar at the ONC end of the count) is called "the counting
  method decides".
- Power (stated before the run): both rules are `tsmom12` with a different reading of the same
  year; the trend-tune surface says such changes move Sharpe by a few hundredths with luck
  alone at +0.17 for the best of 98. Expected |dSharpe| under 0.06 at an SE of 0.03-0.06:
  z within about +-2. **Expected result: fail for both.**

## Logging

Each rule: one `variant` row (six, cash 0), robustness rows for `/bills`, `@etf`, `@idx`
(harness `tries.md` rows; train curves go to the returns store as the harness does). Script
`research/lib/wide18.py`, tests `tests/test_wide18.py`, results `research/results/wide-18.md`.
One dry run (`DRY=1`, last 120 days, nothing logged) is allowed before the real run; its output
is plumbing only.
