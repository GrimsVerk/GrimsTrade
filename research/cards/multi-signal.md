# multi-signal: do value, carry, cross-sectional momentum or low risk rank our six assets?

Written 2026-11-19 00:20 UTC, lane multi-signal (base `survey-6`), **before any signal, IC or
return in this card was computed**. What was seen before writing: the three papers below (read
as text), survey-6's write-up, `info-1.md`, `rl-3.md`, and the coverage of the cached data
(file lists and one CSV header; no values summarised). This is a **descriptive screen, not a
strategy test**: no backtest, no pick, no strategy try, held-out year not loaded.

Bars to quote (lane rules). Project-wide (register-1, `research/register/BAR.md` on
`origin/register-1`, rows through 2026-11-18 22:34): **2,904 tries, N 1,012 for a new pick,
Bonferroni p <= 4.9e-5 (z 3.89); DSR 0.95 edge over `tsmom12` +0.32 Sharpe for a close rule,
+0.59 for a far one.** Our trend family: 65 mechanisms, 16 tested, next test at p < 0.00154
(survey-5). Neither applies to the rows of this screen (not picks); both apply to any rule a
later lane builds from it.

## Why

Survey-6: live long-only value, carry, momentum and low-vol funds tracked their indexes; the only
positive live family was long-short style premia (Sharpe 0.50, t 1.7), i.e. the same four
signals used cross-sectionally across many markets. Our book uses only time-series momentum
(`tsmom12`). Question: in our six-asset universe, does any of the four carry rank information
(which asset will do better than the others next week or month) beyond `tsmom12`? Prior, stated
now: very low. Breadth is six assets in four classes, AMP and Koijen et al. rank within classes
of 10-40 markets, and info-1 / rl-3 found no weekly input above IC ~0.05 on this book.

## Sources (verified as text, 2026-11-19)

- **AMP.** Asness, Moskowitz and Pedersen, "Value and momentum everywhere", Journal of Finance
  68(3), June 2013, 929-985. p. 936-937: momentum for all asset classes = "the past 12-month
  cumulative raw return on the asset ..., skipping the most recent month's return, MOM2-12".
  Value: commodities "the log of the spot price 5 years ago (actually, the average spot price from
  4.5 to 5.5 years ago), divided by the most recent spot price"; bonds "the 5-year change in the
  yields of 10-year bonds ..., which is similar to the negative of the past 5-year return"; country
  equities BE/ME; for stocks the negative past 5-year return correlates 0.83-0.86 with BE/ME
  portfolios (p. 938). Factors weight by cross-sectional rank (eq. 1).
- **Koijen et al.** Koijen, Moskowitz, Pedersen and Vrugt, "Carry", Journal of Financial
  Economics 127(2), 2018, 197-225 (accepted manuscript, CBS portal; also R6 in `survey-4.md`).
  Carry = the return if prices stay the same: equities expected dividend yield minus the local
  risk-free rate; bonds about the 10-year yield minus the short rate plus roll-down; commodities
  the expected convenience yield in excess of the risk-free rate (the futures basis). The global
  carry factor weights asset classes by the inverse of their return volatility.
- **FP.** Frazzini and Pedersen, "Betting against beta", Journal of Financial Economics 111(1),
  2014, 1-25 (authors' draft of 2013-05-10, p. 16): beta = correlation x sigma_i / sigma_m, with
  "a 1-year rolling standard deviation for volatilities and a 5-year horizon for the
  correlation", 1-day log returns for volatility, overlapping 3-day log returns for correlation,
  at least 120 and 750 trading days; shrunk 0.6 x beta + 0.4 x 1, which "does not affect how
  securities are sorted". Each class's beta is against that class's own market (robustness: a
  multi-asset global market portfolio).

## Universe, dates, data (fixed now)

- Six assets SPY, QQQ, TLT, GLD, BTC, ETH; total-return (dividend-adjusted) closes from the
  research cache; train only (no bar after 2025-11-10). Robustness set: the four ETFs alone.
- Decisions: every Friday close from 1994-02-04 whose forward window ends by 2025-11-10. An asset
  counts once it has a year of bars (protocol) and the signal and target exist. A week counts
  when at least 3 assets qualify.
- `sigma_i`: annualised standard deviation of daily log returns over the last 365 calendar days
  (at least 120 bars; 252 or 365 bars a year by asset clock).
- External inputs (keyless; FRED's public `fredgraph.csv` serves the same series as the cached
  copy): 3-month T-bill `DGS3MO` and 10-year Treasury `DGS10`, the value for day x used from
  x + 1. Crypto funding: Binance USDT-margined perpetual funding (`data.binance.vision`, cached),
  from 2020-01. BitMEX (from 2016) refused a plain client (403); not worked around.

## Signals (higher score = expected to do better than the others)

1. **`value`** (AMP's commodity measure, used for all six; AMP say it is similar to their bond
   measure and close to BE/ME for stocks, and BE/ME is not keyless):
   `V = ln(mean adjusted close over [t - 5.5y, t - 4.5y]) - ln(close_t)`; score `V / sigma_i`.
   Needs 5.5 years of bars: three assets qualify only from 2008-01.
2. **`carry`** (Koijen et al., return if prices stay the same, per year, above cash):
   SPY, QQQ: trailing 365-day distribution yield (log adjusted minus log raw return over 365
   days) minus `DGS3MO` (backward-looking proxy for the futures-implied yield); TLT: `DGS10`
   minus `DGS3MO` (roll-down left out); GLD: minus `DGS3MO` (lease rate taken as 0); BTC, ETH:
   minus the mean Binance perpetual funding rate of the last 7 days, annualised (the perp basis
   is the coin's convenience yield minus financing). Score `carry / sigma_i` (inverse-vol, as the
   global carry factor weights classes). Coins enter from 2020-01-08.
3. **`xsmom`** (AMP MOM2-12): `ln(close at t - 30d) - ln(close at t - 365d)`; score `/ sigma_i`.
4. **`lowvol`**: `-sigma_i` (the simplest low-risk signal).
5. **`bab`** (FP): `-beta_i` against SPY as the market (the closest single market for this book;
   neither FP's per-class markets nor their global portfolio exist here), on SPY's trading days
   (coin closes on those days): sigma from the last 252 daily log returns (>= 120), correlation
   from overlapping 3-day log returns over the last 5 years (>= 750). Shrinkage skipped: it does
   not change ranks. SPY's beta is 1 by construction.

Reference: `tsmom12` = 1 if the 365-day log return is > 0, else 0 (the live rule's signal);
`z365` = that return / sigma_i (its continuous strength).

## Targets and measures

- Targets: log total return from the Friday close to the asset's last close on or before
  t + 7 days (**week**) and t + 28 days (**month**, overlapping). Primary: raw return (as the
  brief asks). Secondary: return / sigma_i (risk-adjusted).
- **Rank IC**: each week, Spearman correlation (average ranks for ties) of score and target across
  the qualifying assets; IC = mean over weeks. With n <= 6 a single week's IC has SE ~0.45.
- **CI**: stationary block bootstrap of the weekly IC series, mean block 13 weeks, 5,000 draws,
  fixed seed; 95% and 99.5% percentile intervals.
- **Placebo A (shuffled labels)**: 2,000 draws, each week the scores are permuted among that
  week's assets; report the 95th percentile of |mean IC| and the two-sided p.
- **Placebo B (fixed relabel)**: every non-identity permutation of the six assets (719; 23 for the
  ETF set): asset i gets asset pi(i)'s score series for all weeks. Keeps each series' time
  structure; asks whether the signal beats an arbitrary fixed mapping (a near-static signal like
  `lowvol` can score well only because one asset, say a coin, earned more on average). p = share
  of permutations with |IC| >= |observed|.
- **Link to `tsmom12`**: mean weekly Spearman of score with the `tsmom12` indicator (weeks where it
  is not constant) and with `z365`.
- **Beyond `tsmom12` (partial IC)**: each week, score ranks regressed (OLS, intercept) on the
  `tsmom12` indicator; correlation of the residual with the target ranks; mean over weeks, same
  CI. Reference: `tsmom12`'s and `z365`'s own rank IC.
- Eras (protocol): 2000-09, 2010-16, 2017-21, 2022-25 (1994-99 has at most two assets).

## Worth a card later? (bar fixed now)

A signal is worth a strategy card only if **all** hold (10 primary looks: 5 signals x 2 horizons,
so the interval is Bonferroni's 99.5%):

1. Partial IC beyond `tsmom12`, raw next-week target: > 0 with the 99.5% block-bootstrap interval
   above 0, and the same sign at the month horizon.
2. Outside both placebos: |IC| above placebo A's 95th percentile and placebo B p < 0.05.
3. Same sign on the four-ETF set, and in at least 3 of the 4 eras with data.
4. Size: partial weekly IC >= 0.10. rl-3's ceiling: a rule told a clean signal gains +0.03
   Sharpe at IC 0.05 and +0.16 at 0.10, while a new pick must show +0.32 (close) to +0.59 (far)
   over `tsmom12` at N 1,012. Below 0.10 nothing on this book is worth a test.

Expected before computing: nothing passes 4; the fundamental law's IR ~ IC x sqrt(breadth)
gives little with six correlated, slowly changing scores.

## Logging

Script `research/lib/multisignal_ic.py`, pushed before its run. Run once with `--log`: one
`screen` row per signal per universe in `tries.md` (idea `multi-signal-screen`; 5 signals +
the `tsmom12` reference, x six and four-ETF sets = 12 rows), numbers in the variant text and in
`results/multi-signal.md`. Screen rows are not selectable and are not strategy tries.
