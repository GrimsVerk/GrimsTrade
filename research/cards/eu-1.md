# eu-1: `tsmom12` on European UCITS ETFs/ETCs, from a euro investor's view

Field: robustness of the house rule on a new universe (not a new rule, not a selection).
Written 2026-11-18 ~21:30 UTC, lane eu-1, after the data note (`eu-1.md`, section 1) and before
any strategy was run on the new data. Seen before: everything in `trend-tune.md` (the rule's
anatomy on the US six, the out-of-universe sets) and the data sanity table
(`results/eu-1-data.md`: buy-and-hold growth, vol and tracking of each UCITS line; no strategy
number).

## Claim to check

`tsmom12` (each eligible asset holds its equal slot when its 365-day return is positive, else
that slot is cash; decided on Fridays) keeps its character when the US-listed ETFs are replaced
by European-listed UCITS funds covering the same asset classes and everything is measured in
euros, with a European retail broker's costs.

## Why it might not

- Currency: a euro investor holding unhedged US funds carries the dollar. USD/EUR moves 8-10% a
  year and has tended to rise in US equity sell-offs (2008, 2020, 2022), which cushions a euro
  holder's falls and changes what the 12-month trend sees.
- Euro government bonds are not US Treasuries: different rate cycle (2011-12 euro crisis
  spreads, negative yields 2015-21, a deeper 2022 fall at the long end).
- Costs are higher than the gym's US ETF assumption (2 bps, no fee).
- Shorter histories: the native window is 2012-2025, which misses 2000-02 and 2008.

## Rule (fixed, no tuning)

`c.weekly(c.slots(c.tsmom_signal))` from `lib/common.py`, unchanged: 365-day lookback, equal
slots over eligible assets (a year of bars), weekly Friday decisions, next-open fills, cash at 0,
1% rebalance band, total-return (dividend-adjusted) prices. Nothing is fitted or chosen.

## Universes

Window **W**: decisions 2012-01-02 .. 2025-11-09 (train end). 2012-01-02 is the first Monday by
which every native UCITS line has a year of clean bars (SXR8/SXRV start 2010-11-01). Coins join
when they have a year of bars (BTC 2013, ETH 2017), the same in every coin book.

| Book | Members | Currency | Costs |
|---|---|---|---|
| `us6` | SPY, QQQ, GLD, TLT, BTC, ETH (the live six) | USD | gym |
| `us6-eur` | the same six converted to EUR | EUR | gym |
| `eu6` | SXR8, SXRV, 4GLD, IBGL, BTC-EUR, ETH-EUR | EUR | retail |
| `usw` | SPY, EFA, EEM, IEF, TLT, GLD, DBC (US asset classes) | USD | gym |
| `usw-eur` | the same seven in EUR | EUR | gym |
| `euw` | SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY (1:1 with `usw`) | EUR | retail |

Pairs judged: **A** = `eu6` vs `us6` (can the live book be copied), **B** = `euw` vs `usw`
(the asset classes, no coins). `us6-eur` and `usw-eur` split the change into currency and
instrument; they are descriptive.

## Costs (fixed)

- **retail**: UCITS ETFs/ETCs 0.10% fee + 0.05% slippage a side. Basis: DEGIRO charges
  about EUR 1 (core selection) to EUR 4 (other ETFs on Xetra/Euronext) per order; on the
  EUR 1,000-5,000 orders a EUR 10,000-50,000 book places that is 0.02-0.4%, 0.10% in the middle.
  Half-spreads of these liquid iShares lines and Xetra-Gold are a few basis points. Coins in EUR:
  the gym's crypto costs (0.25% + 0.05%), about a European exchange's taker fee.
- **gym**: the house costs (ETFs 0 + 0.02%, coins 0.25% + 0.05%).
- **harsh** (robustness): ETFs 0.25% + 0.15%.
- No taxes: none is modelled in any book, so the comparison is like for like.

## Runs (all that will be run; every one a row in `tries.md`, idea `eu-1`)

On W:

1. `tsmom12` and `equal-weight` on each of the six books (12 rows; `tsmom12` rows are
   `robustness`, `equal-weight` rows `baseline`).
2. Buy-and-hold IWDA (world equity, EUR, retail costs) and buy-and-hold SPY (USD, gym):
   `baseline`, 2 rows.
3. Costs: `tsmom12` on `eu6` and `euw` at gym and at harsh costs (4 rows).
4. `eu6` with IS04 (US Treasuries 20+, EUR-hedged, from 2015) in place of IBGL: `tsmom12` and
   `equal-weight` (2 rows; IS04 joins in 2016).
5. Single assets, the four ETF slots of the six: `tsmom12` and buy-and-hold on SXR8, SXRV, 4GLD,
   IBGL (retail) and SPY, QQQ, GLD, TLT (USD, gym): 16 rows, descriptive.

Longer windows, robustness only:

6. `euw` native from its first possible decision (2009-01-02, members join as they reach a year):
   `tsmom12` and `equal-weight`, and the same two on `usw` (USD, gym) from the same day
   (4 rows).
7. Splices, decisions 2000-01-03 .. 2025-11-09 (the ECB rate starts 1999): `eu6-S` (SXR8-S,
   SXRV-S, 4GLD-S, IBGL-S, BTC-EUR, ETH-EUR; retail costs) and `us6` in USD on the same window:
   `tsmom12` and `equal-weight` each (4 rows). Before 2008-2010 `-S` series are US ETFs in
   euros.

## Crash windows (fixed; peak to trough of US/world equities, US dates)

| Window | From | To |
|---|---|---|
| 2011 euro crisis | 2011-05-02 | 2011-10-03 |
| 2015-16 China / oil | 2015-05-21 | 2016-02-11 |
| 2018-Q4 | 2018-09-20 | 2018-12-24 |
| 2020 covid | 2020-02-19 | 2020-03-23 |
| 2022 rate shock | 2022-01-03 | 2022-10-12 |

Total return of each book inside each window (in its own currency). 2011 lies before W starts:
it is read from run 6 (`euw` from 2009) and run 7 (splices from 2000) and the matching US runs.

## What counts as "character holds" (per pair A and B, on W)

1. **Return per risk:** `tsmom12`'s Sharpe minus `equal-weight`'s Sharpe on the EUR book is
   within 0.15 of the same difference on the US book.
2. **Worst loss:** `tsmom12`'s max drawdown on the EUR book is at most 5 points worse than on the
   US book, and smaller than the EUR book's `equal-weight` drawdown.
3. **Turnover:** `tsmom12`'s turnover on the EUR book is between 0.67x and 1.5x the US book's.
4. **Crashes:** in the four crash windows inside W, the sign of (`tsmom12` minus `equal-weight`)
   on the EUR book matches the US book's in at least 3 of 4.

Verdict per pair: **holds** if all four pass; **holds in part** if 2 and 4 pass but 1 or 3
fails; **breaks** otherwise. Absolute Sharpe ratios are reported but are not a criterion (the
EUR book has a different asset mix and currency). No held-out year is used: nothing is selected.

## Result

See `eu-1.md` (sections 2-4) and `results/eu-1.md` once run.
