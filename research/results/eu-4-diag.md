# eu-4 step 1: where `euw` spends its order budget (descriptive)

Train period only, window W (decisions 2012-01-02 .. 2025-11-09), the house rule `tsmom12` on `euw` (SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY; 7 equal slots, Friday signal, weights repeated daily, 1% band), EUR, total-return prices, ETF slippage 0.05% a side, no fixed fee. This replays eu-3's `tsmom12@euw/slip` (no new `tries.md` row). Fee tiers are generic: EUR 1, 2 or 3 per ETF order on a constant book (eu-2's schedules; the EUR 1 and EUR 3 tiers also carry a EUR 2.50 yearly fee, the EUR 2 tier none). Book vol at no fee: 5.9%. Fee drag in Sharpe = fees per year / vol.

## 1. Orders by cause

A spell is the time between two signal flips of one slot, counted in Fridays. A **whipsaw** is a spell that the next flip closes within N weeks: an in-spell (bought, sold again) or an out-spell (sold, bought back); its two flips are two orders that cancel each other. Drift = top-ups and trims of held slots back to 1/7 once they stray by 1% of the book.

| Cause | Orders | Per year | Share | Fee/yr EUR 1 tier, 5k / 10k book | EUR 2 | EUR 3 | Sharpe drag at 10k (EUR 1 / 2 / 3) |
|---|---:|---:|---:|---|---|---|---|
| Start-up build (2012-01) | 4 | - | 1% | - | - | - | - |
| Signal flip in (entry) | 138 | 10.0 | 33% | EUR 10 (0.20% / 0.10%) | EUR 20 (0.40% / 0.20%) | EUR 30 (0.60% / 0.30%) | 0.017 / 0.034 / 0.051 |
| Signal flip out (exit) | 136 | 9.8 | 33% | EUR 10 (0.20% / 0.10%) | EUR 20 (0.39% / 0.20%) | EUR 29 (0.59% / 0.29%) | 0.017 / 0.034 / 0.050 |
| Drift top-up / trim | 139 | 10.0 | 33% | EUR 10 (0.20% / 0.10%) | EUR 20 (0.40% / 0.20%) | EUR 30 (0.60% / 0.30%) | 0.017 / 0.034 / 0.051 |
| All | 417 | 30.1 | 100% | EUR 30 (0.60% / 0.30%) | EUR 60 (1.20% / 0.60%) | EUR 90 (1.80% / 0.90%) | 0.051 / 0.103 / 0.154 |

(The yearly EUR 2.50 of two tiers is not an order and is left out of these columns; at 5k / 10k it is 0.05% / 0.025% of the book a year.)

Flip orders that sit in whipsaw spells (both orders of each short spell; a flip can close one spell and open the next, so each spell is charged its two flips once):

| N weeks | Short in-spells | Short out-spells | Orders in them / yr | Share of flip orders | Share of all orders | Fee/yr at 10k, EUR 1 / 2 / 3 | Sharpe drag at 10k (EUR 1 / 2 / 3) | Asset move inside (log pts/yr; in-spells / out-spells) |
|---:|---:|---:|---:|---:|---:|---|---|---|
| 4 | 67 | 83 | 16.4 | 83% | 54% | EUR 16 / EUR 33 / EUR 49 | 0.028 / 0.056 / 0.084 | -1.09 / +1.37 |
| 8 | 89 | 97 | 17.9 | 91% | 59% | EUR 18 / EUR 36 / EUR 54 | 0.031 / 0.061 / 0.092 | -1.65 / +1.70 |
| 13 | 93 | 109 | 18.5 | 94% | 62% | EUR 19 / EUR 37 / EUR 56 | 0.032 / 0.063 / 0.095 | -1.69 / +2.22 |
| 26 | 105 | 118 | 18.9 | 96% | 63% | EUR 19 / EUR 38 / EUR 57 | 0.032 / 0.065 / 0.097 | -1.71 / +2.53 |

Asset move inside = the asset's own log return from the opening to the closing flip, summed over spells, per year, divided by 7 (one slot's share of the book). For an in-spell a negative number is money lost while held; for an out-spell a positive number is the move missed while out. Fills are at the next open; these are Friday closes, so the size is approximate. These moves are selected by hindsight (a spell is a whipsaw *because* the asset turned), so they are not a cost any rule could avoid; they show only that whipsaws are not free of market loss either.

## 2. Which assets whipsaw

| Asset | Flips/yr | Spells | Median spell (wk) | Whipsaw spells <= 4 wk | <= 13 wk | Share of all <= 13 wk whipsaw | Drift orders/yr | Weekly noise of z (sd of weekly change) | Median |z| at a flip |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SXR8 | 2.0 | 27 | 3 | 17 | 18 | 9% | 2.4 | 0.22 | 0.11 |
| EXSA | 3.1 | 42 | 2 | 25 | 32 | 16% | 1.4 | 0.22 | 0.08 |
| IQQE | 3.2 | 44 | 4 | 22 | 31 | 15% | 1.3 | 0.20 | 0.10 |
| IBGS | 1.3 | 17 | 5 | 8 | 11 | 5% | 0.6 | 0.20 | 0.13 |
| IBGL | 3.4 | 46 | 3 | 28 | 36 | 18% | 1.3 | 0.22 | 0.11 |
| 4GLD | 2.7 | 37 | 4 | 23 | 29 | 14% | 1.9 | 0.21 | 0.10 |
| EXXY | 4.0 | 54 | 4 | 27 | 45 | 22% | 1.1 | 0.20 | 0.11 |

## 3. How short and how shallow are the whipsaws

Closed spells by length (Fridays), and the largest |z| reached inside each (z = 12-month log return / the asset's one-year EWMA vol, 60-bar half-life; the signal is the sign of z). A dead zone of half-width h (enter above +h, leave below -h) would have removed a spell whose |z| never got past h, other things equal; a confirmation rule (two Fridays in a row) removes every 1-Friday spell and delays the rest by a week.

| Length | Spells | In / out | Median peak \|z\| | Share with peak \|z\| < 0.25 | < 0.5 | Median move inside (log pts, in / out) |
|---|---:|---|---:|---:|---:|---|
| 1 week | 88 | 40 / 48 | 0.05 | 94% | 100% | -1.0 / +1.2 |
| 2 weeks | 23 | 11 / 12 | 0.14 | 83% | 100% | -1.8 / +1.2 |
| 3-4 weeks | 39 | 16 / 23 | 0.24 | 54% | 92% | -0.5 / +1.5 |
| 5-8 weeks | 36 | 22 / 14 | 0.43 | 11% | 69% | -2.9 / +2.7 |
| 9-13 weeks | 16 | 4 / 12 | 0.59 | 6% | 19% | -0.2 / +3.1 |
| 14-26 weeks | 21 | 12 / 9 | 0.91 | 0% | 5% | -0.8 / +0.5 |
| > 26 weeks | 44 | 27 / 17 | 1.88 | 0% | 2% | +6.0 / -0.2 |

All weekly z changes, pooled over the 7 assets: sd 0.21. Long spells (> 26 weeks) reach a median peak |z| of 1.88.
