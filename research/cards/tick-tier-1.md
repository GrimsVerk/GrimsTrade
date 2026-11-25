# tick-tier-1: did 12-month trend break after 2009 on stock indices and currencies but not on bonds?

Lane `tick-tier-1`, written 2026-11-25 **before any number of this card is computed** (no
window split of any series below has been run in this lane). Descriptive re-score, kill-only:
no new rule, nothing selected, no comparator change, a `note` row in `tries.md` (as
`gap-2002-1` and `e4-anatomy-1` did). Research only: fake money, files already in the data
cache (read-only), no change to the gym, the daily runner or the live strategies. Train data
only: nothing after 2025-10-31 is parsed (pooled-1's and pooled-2's loaders); the held-out year
is untouched.

## The claim being checked (read from the paper, not from the survey)

Kurth, Eisler, Rej and Bouchaud, "Is Trend Still Your Friend? A Microstructural Account of the
Demise of Short-Term Trend-Following", arXiv 2607.01550 (v1, 2026-07-02). Read for this card
(abstract and HTML full text):

- About 100 liquid futures, 1995-2025. Signals EWM-tau minus EWM-4tau, tau = 5, 10, 20, 50
  days (the slowest is about 50/200 days); **no 6-12-month signal is tested**.
- Break: "approximately 2008/9"; their Table 1 splits at **2009** (1995-2009 against
  2009-2025). No formal break-date test; other sections mention 2010 and 2011.
- Tick size: each month, the average daily ratio of the tick to the daily volatility; products
  ranked monthly and split into halves (lower half small-tick). Equity indices and currencies
  cluster in the small-tick half; bonds ("an almost pure large tick sector") and most
  commodities in the large-tick half. The commodity universe is split: its smaller-tick half
  degraded too.
- Result: equal-risk portfolio Sharpe of small-tick contracts about 0.8 before and about 0
  after; large-tick about 1.4 before and 1.0-1.2 after. Whole universe at tau = 50: 0.70
  before, 0.40 after (SE about 0.25). They state that **no decomposition by asset class**
  reproduces the split (tiers within a class still split), so a class-level test is weaker
  than their tick test by their own account.

What our data can do: the cache has no futures and no tick sizes, only the asset class of each
series. So this lane checks the **class-level implication at the 12-month horizon**: if the
paper's mechanism also reaches slow trend, `tsmom12` should have lost more Sharpe after 2009 on
stock indices and currencies than on government bonds. A null here does not refute the paper
(other horizon, other instruments, class is not tick); a clear negative is only "consistent".

## Data and rules (frozen code, nothing new fitted)

- Series: pooled-1's 41 (`pooled1.load_all`, `pooled1_core.run_market`, 2 bps, weekly) and
  pooled-2's 29 (`pooled2.load_nonequity`, `pooled2.run_specs`, its costs, lags and frequencies).
- Rules: `tsmom12` and `e4` exactly as there (positions, lags, costs unchanged). Also `hold`
  (the series itself, always invested, no cost) as the reference for the timing part.
- Returns above bills, cash at the bill: pooled-2's series already are (bonds and FX in excess
  of the US bill or funded at the US rate; commodities spot with cash 0, as pooled-2). pooled-1's
  are total or price returns with cash at 0, so here each session's return is reduced by
  position x the US 3-month bill (`DTB3`, last value on or before the previous session,
  calendar days / 365; `hold`: minus the full bill). The US bill is used for local-currency
  indices too (a convention, not a hedge); check: pooled-1's own cash at 0.

## Classes (by asset, fixed now)

| Class | Paper's tier | Series |
|---|---|---|
| EQ | small | US10 industries (10), DEV13 indices (13), WIDE10 indices (10), ETFs IWM, EFA, EEM, VNQ (4) = 37 |
| FX | small | FX9: JPY, GBP, CHF, CAD, AUD, NZD, SEK, NOK (weekly), EUR (monthly) = 9 |
| BD | large | USB3 (UST2, UST10, UST30), GOV9 (9 foreign 10-year), ETFs IEF, LQD = 14 |
| CM | large, split | COM8 (7 PPI spot series, gold), ETFs DBC, SLV = 10 |

pooled-1's 41 "equity markets" include four non-equity ETFs (IEF, LQD bonds; DBC, SLV
commodities); they go to their asset class. Check: pooled-1's grouping as it was (all 41 in EQ,
pooled-2's 29 as above).

## Windows and statistic

- Pre: periods ending 1995-01-01 .. 2008-12-31 (the paper's sample start to its break). Post:
  2009-01-01 .. 2025-10-31. A period belongs to the month it ends in (pooled-2's monthly
  calendar). A series counts only with at least 5 years of scored periods in **each** window
  (260 weeks or 60 months); the eligible set is fixed from the real data and kept in every draw.
- Per series m and rule r: S_pre, S_post = Sharpe above bills in the window, annualised at the
  series' frequency (sqrt 52 or sqrt 12), as pooled-2. Delta_m = S_post - S_pre.
- Per class K: Delta_K = equal-weight mean of Delta_m over its eligible series; also the class
  mean levels S_pre, S_post (to set beside the paper's 0.8 -> 0 and 1.4 -> 1.0-1.2).
- **Primary contrast** C = (Delta_EQ + Delta_FX) / 2 - Delta_BD (small-tick classes, class-
  balanced, minus the pure large-tick class). Shown, not deciding: C_4 = (Delta_EQ + Delta_FX)
  / 2 - (Delta_BD + Delta_CM) / 2 (commodities are spot PPI, not judged in pooled-2, and split
  in the paper).
- **Timing part** (the survey's sketch): the same C on Delta_m(r) - Delta_m(hold), i.e. on the
  rule's Sharpe minus holding's. A long-only `tsmom12` carries the market's drift; if stocks
  simply rose more after 2009, its Sharpe rises with no change in trend. The timing part
  removes that.
- SE: joint circular block bootstrap of calendar months as in pooled-2 (12-month blocks, the
  same months for every series, so the dollar, world-rates and crash calendars stay), drawn
  **separately inside each window** (the break date stays where it is). 2,000 draws, seed 0.
  In a draw a series' window Sharpe needs one year of periods (pooled-2's minimum); class means
  over the fixed eligible set, nan-skipping. SE = standard deviation of the draws, z = C / SE.

## Readings (per rule; `tsmom12` decides the answer, `e4` is reported with the same rules)

1. **"Consistent with the paper (class level)"**: C <= -2.0 SE (z <= -2.0), AND Delta_EQ < 0
   AND Delta_FX < 0. Qualified as "trend, not drift" if the timing part also has z <= -2.0,
   otherwise "in the rule's Sharpe only, not in its timing".
2. **"Not seen at the class level (killed for 12-month trend on our series)"**: C >= 0.
3. **"Inconclusive"**: anything else (C < 0 with z > -2.0, or z <= -2.0 with Delta_EQ or
   Delta_FX >= 0).

Same three readings on the timing part, reported beside. Pre-stated: whatever the reading, this
cannot separate tick from class, and it is about 12-month (and `e4`'s 1-12-month) trend, not the
paper's 5-50-day signals.

## Power (before the numbers)

A single series' Sharpe over 14 or 17 years has SE about 0.27 / 0.24, so Delta_m about 0.36.
With within-class correlation of Delta about 0.5 (stocks, bonds) and 0.3 (FX), the class means
have SE about 0.25 (EQ), 0.22 (FX), 0.26 (BD), so SE(C) about 0.3. z <= -2 then needs C about
-0.6 or lower. The paper's tier gap is about -0.5 (-0.8 against -0.3) for equal-risk
portfolios of many contracts at fast horizons; per-series Sharpes are lower (0.3-0.5 for
`tsmom12` in pooled-1/2), and at tau = 50 their whole-universe drop is -0.3. **Expected by
construction: "inconclusive" unless the effect is large; the lane can kill the class-level
implication (C >= 0) but is unlikely to confirm it.** The realised SE is reported.

## Checks (reported, not deciding)

- Break at 2010-01 instead of 2009-01 (the paper's other dates).
- Blocks of 3 and 24 months.
- Equity cash at 0 (pooled-1's own convention, no bill subtracted).
- pooled-1's grouping as is (41 in EQ).
- Market-weighted contrast: mean Delta over EQ+FX series minus mean over BD series.
- Plumbing: the eligible set and the point Deltas reproduce from the per-period returns; pooled-1
  and pooled-2 full-sample `tsmom12` Sharpes reproduce their published robustness rows (cash-0
  equity rows; pooled-2 rows as logged).

## What it would mean for the live six-asset book

The book (`tsmom12` on SPY, QQQ, TLT, GLD, BTC, ETH) holds two stock indices (EQ, small-tick in
the paper's terms), one long Treasury (BD, large-tick), gold (CM; the paper does not place gold
by name; commodity futures are mostly large-tick) and two coins (not in the paper; CME bitcoin
futures have a tick that is tiny against daily volatility, so they would be small-tick if the
definition carried over; not tested). Pre-stated readings:

- Consistent: expect the insurance (#87, #162) to be worth less on SPY/QQQ (and plausibly the
  coins) than on TLT/GLD from now on; the "price of the insurance" in stocks is the part to watch.
  No live change from this lane (descriptive; the live rule is a risk choice, not an edge).
- Killed or inconclusive: no reason from our data to expect a class-specific decline of
  12-month trend; nothing changes.

## Output and logging

- `research/tick-tier-1.md` (answer), `research/results/tick-tier-1.md` (+ `.json`), code
  `research/lib/ticktier1.py` (reuses `pooled1_core`, `pooled2_core`, `pooled1`, `pooled2`),
  tests `tests/test_ticktier1.py` (window split and bootstrap on synthetic data, offline).
- `research/tries.md`: one `note` row (re-score, not a try). `research/ideas.md`: a
  `tick-tier-trend` line.
