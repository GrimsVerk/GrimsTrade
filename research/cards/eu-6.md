# eu-6: should a small coin-free euro book run trend at all?

Field: choice between existing rules for a small euro book (no new signal, no tuning). Lane
`eu-6` (DEEPER), night of 2026-11-18, branch `eu-6` from `eu-5`. Written and pushed before any
number for the new runs below existed.

## Question

A euro investor in the Netherlands with a small coin-free book (EUR 5k-25k, fixed per-order fees
of EUR 1, 2 or 3) can run the house trend rule on the seven `euw` funds, or simply hold the seven
funds, or hold a plain stock/bond mix. Which is better, for which kind of investor? Trend's known
value is crash insurance (a smaller worst fall), not Sharpe. This card fixes, before any new
number, what is compared, how it is measured, and which rule wins under which preference.

## Seen before writing this (from eu-1 .. eu-5, train window W)

- `R` (`tsmom12` on `euw`, 1% band): Sharpe 0.617, max DD 13.0%, 30.1 orders/yr; crash windows
  2015-16 / 2018-Q4 / 2020 / 2022: -7.8 / -3.9 / -11.6 / +2.2%.
- `T` = `euw` + D2 (5/25 band, eu-5's pick): Sharpe 0.624, max DD 13.6%, 21.1 orders/yr; crash
  windows -8.2 / -4.2 / -12.2 / +1.7%. Minimum book (fee loss <= 0.10): ~4k / 7k / 11k at the
  EUR 1 / 2 / 3 tier. Fee runs at 3 tiers x 5k/10k/25k exist (eu-5).
- Equal weight of the seven, house 1% band (eu-3): Sharpe 0.77, max DD ~20%. With a 5% band
  (eu-2, fee runs only): Sharpe 0.81, max DD 19.6%, turnover 0.10/yr.
- Not seen: equal weight with the 5/25 band, any 60/40-style mix of these funds, time under
  water and worst 12 months of any `euw` rule, any `euw`-like book in 2000-02 or 2008.

## The three candidates (all that will be run; fixed now)

All on `euw` (SXR8 S&P 500, EXSA Europe 600, IQQE emerging markets, IBGS euro govts 1-3y, IBGL
euro govts 15-30y, 4GLD gold, EXXY commodities), EUR, total-return prices, eu-2's costs (ETF
slippage 0.05% a side), window W (decisions 2012-01-02 .. 2025-11-09), train only, cash at 0,
next-open fills, every rebalance through the gym with the band below.

- **T `trend`**: `tsmom12` + D2 (eu-5's saved runs, re-scored, no new row): each fund's 1/7
  slot held when its 365-day return is positive, else cash; Friday decisions; drift traded only
  when a slot is 25% off target (band min(5%, 25% x 1/7) = 3.57% of the book).
- **H `hold7`**: equal weight of the seven, the same 5/25 band (3.57% of the book). Weights sent
  every day (the house equal-weight baseline); a fund is traded only when it is 3.57 points off.
- **M `mix60`**: a fixed 60/40 mix of the funds, equal within each class: SXR8, EXSA, IQQE 20%
  each (60% stocks); IBGS, IBGL 20% each (40% euro government bonds); no gold, no commodities.
  The same 5/25 rule: band min(5%, 25% x 20%) = 5% of the book. Chosen as the plainest
  textbook 60/40 that uses only these funds; no other mix is run.
- References shown, no rows: `R` and equal weight with the house 1% band (eu-3's saved runs).

## Criteria a human cares about (computed for each candidate)

On W, no fixed fee unless stated:

1. **Sharpe** (with its SE, Mertens) and CAGR, vol.
2. **Worst loss**: max drawdown.
3. **Time under water**: the longest stretch, in months, from a peak until equity first gets back
   to it (an unrecovered stretch at the end counts to the last day).
4. **Worst 12 months**: the lowest return over any 365 calendar days.
5. **Crash windows**, total return inside each:
   - inside W: 2015-16, 2018-Q4, 2020 covid, 2022 rate shock (eu-1's windows);
   - **2008** (2007-10-09 .. 2009-03-09), US proxy: the three rules on `usw` (SPY, EFA, EEM, IEF,
     TLT, GLD, DBC; USD, the gym's costs; the US investor's analog: home-currency bonds) from
     2007-03-01, when all seven have a year of bars; T = `tsmom12` + 5/25 band, H = equal weight
     + 5/25 band, M = SPY, EFA, EEM, IEF, TLT 20% each + 5% band;
   - **2000-02** (dot-com bust), long monthly proxy (no daily ETF book exists before 2002):
     three US series, Shiller's S&P composite total return (price + dividends/12), Shiller's 10y
     Treasury total return, gold (datahub monthly, free market from 1971). T = each 1/3 slot held
     when its trailing 12-month return is positive, measured with a one-month lag (the series
     are monthly averages, so the lag keeps the signal clear of the month being traded); H =
     1/3 each, rebalanced monthly; M = 60% stocks / 40% bonds, monthly. No fees, cash at 0.
     Window = months 2000-03 .. 2002-10 (and the 2008 window again, 2007-10 .. 2009-03, as a
     second view). Only the crash windows of this proxy are judged; its full-period numbers
     (1972-2025) are shown, not judged (cash at 0 is harsh in 1972-2000, monthly averages
     smooth the falls).
6. **Fees**: each candidate at the EUR 1 / 2 / 3 tiers (eu-2's schedules; the EUR 1 and EUR 3
   tiers carry a EUR 2.50 yearly fee) on constant books of EUR 5k / 10k / 25k: Sharpe after
   fees, fee loss (own Sharpe at no fee minus Sharpe at the tier), orders a year, fixed fees a
   year (% of the book), max DD.
7. **Uncertainty**: paired stationary bootstrap of each Sharpe difference (T-H, T-M, H-M; mean
   block 20 days, 2,000 draws, seed 0): the difference, its bootstrap SE, 90% range, one-sided p.
8. **Descriptive only (no row, not judged)**: H scaled down to T's volatility with cash at 0
   (H's daily returns x vol(T)/vol(H), a hindsight constant), to show whether trend's smaller
   worst loss is more than holding less risk: its max DD and worst 12 months next to T's.

## Which wins under which preference (fixed now)

Each preference picks one winner among T, H, M; at a tie the rule with fewer orders a year at no
fee wins (simpler, cheaper).

- **P1 Sharpe** (best risk-adjusted return after fees, at the investor's tier and book): the
  highest Sharpe at that cell. A Sharpe lead counts as **real** only with paired bootstrap p <
  0.10 / 3 = 0.033 (three pairwise comparisons); otherwise the cell is a tie within noise.
- **P2 worst loss**: the lowest max DD; a lead under 2 points is a tie, then the better worst 12
  months decides.
- **P3 waiting**: the shortest longest-time-under-water; a lead under 3 months is a tie.
- **P4 crash insurance**: the most of the six crash windows (2000-02 proxy, 2008 proxy, 2015-16,
  2018-Q4, 2020, 2022) with the best return; a return within 1 point of the best also counts as
  best in that window.
- **P5 cost**: the fewest orders a year at no fee (and so the lowest fees at every tier).

**Is trend worth it for an investor?** Per (preference, tier, book): yes when T wins that
preference **and** T's fee loss at that tier and book is <= 0.10 Sharpe (eu-5's bar). For P2-P4
(fee-independent winners) the second condition gives the minimum book. The plain answer is
written for these investor kinds: Sharpe-seeker, worst-loss-averse, crash-insurance buyer,
cheapest/simplest; and EUR 5k / 10k / 25k at the three tiers.

## Rows and multiple testing (fixed now)

- `euw`: H and M, each at no fee and at 3 tiers x 3 books: **20 `baseline` rows** (idea `eu-6`).
  T at no fee and at the tiers: eu-5's saved runs, re-scored without new rows.
- `usw` from 2007-03-01: T (`robustness`), H, M (`baseline`): **3 rows**.
- Long monthly proxy 1972-2025: T (`robustness`), H, M (`baseline`): **3 rows**, written by hand
  in the same format (Sharpe annualised from monthly returns, sqrt(12); marked "monthly").
- **26 rows.** None is a selectable trend variant: these compare an existing rule with plain
  holding. The eu family stays at 10. The choice among T, H, M is its own family of three
  (the P1 bar above).
- Held-out year: untouched. Nothing here changes the live rule.
- Plumbing before any row (no number shown): T on `euw` here reproduces eu-5's saved D2 equity;
  H with the house 1% band reproduces eu-3's saved equal-weight equity; the fixed-mix decisions
  hold exactly the five weights on every day of W; the monthly proxy's three series cover
  1971-2025 without gaps.

## Result

`eu-6.md` and `results/eu-6.md` once run.
