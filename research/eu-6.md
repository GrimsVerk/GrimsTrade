# eu-6: should a small coin-free euro book run trend at all?

Lane `eu-6` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-6` from `eu-5`. Card `cards/eu-6.md` (pushed before any number). Code `lib/eu6.py`
(`check`, then `run`; `lib/long_bond.py`, `lib/long_gold.py` copied unchanged from data-long-2);
table `results/eu-6.md`; 26 rows in `tries.md` (idea `eu-6`). Held-out year unspent.

## 1. What was compared

Three ways to run the seven `euw` funds (S&P 500, Europe 600, emerging markets, euro govts 1-3y
and 15-30y, gold, commodities) in EUR, 2012-2025, all with the 5/25 rebalance band:

- **T trend**: the house rule `tsmom12` (a fund is held only while its 12-month return is
  positive, else its slot is cash), eu-5's 5/25 band.
- **H hold7**: hold all seven, 1/7 each.
- **M mix60**: a plain 60/40 mix: three stock funds 20% each, the two euro bond funds 20% each.

No tuning; one try each. Crash years before the funds existed come from US proxies: 2008 from
the US asset-class book (`usw`, USD, from 2007), 2000-02 from a monthly US stocks / 10y
Treasuries / gold series (1972-2025).

## 2. Results (no fixed fee unless stated)

| | T trend | H hold7 | M mix60 |
|---|---:|---:|---:|
| Sharpe (SE) | 0.62 (0.27) | **0.78** (0.27) | 0.75 (0.27) |
| Yearly return (CAGR) / vol | +3.7% / 6.1% | +6.3% / 8.3% | +7.0% / 9.6% |
| Worst loss (max DD) | **13.6%** | 19.8% | 22.3% |
| Longest under water | 58 mo (2015-04 .. 2020-02) | **31 mo** (2015-04 .. 2017-11) | **31 mo** (2021-11 .. 2024-06) |
| Worst 12 months | -11.5% | **-11.4%** | -15.7% |
| 2000-02 (monthly US proxy) | **+8.8%** | -1.2% | -14.3% |
| 2008 (US proxy, USD) | **-0.7%** | -23.1% | -30.4% |
| 2015-16 / 2018-Q4 | **-8.2%** / -4.2% | -13.8% / **-3.4%** | -13.8% / -5.5% |
| 2020 covid / 2022 rates | **-12.2% / +1.7%** | -18.7% / -6.7% | -22.1% / -17.4% |
| Orders a year | 21.1 | 1.9 | **1.2** |
| Fee loss (Sharpe) at EUR 1 / 2 / 3, 10k book | 0.04 / 0.06 / 0.10 | <= 0.02 | <= 0.01 |

- **Sharpe differences are noise-sized.** T - H = -0.16 (bootstrap SE 0.14, 90% range -0.39 ..
  +0.06, p 0.12 that H is not better); T - M = -0.13 (SE 0.17); H - M = +0.03 (SE 0.10). None
  passes p < 0.033. On the US proxy from 2007 (which includes 2008) the order flips: T 0.64,
  H 0.63, M 0.54; on the monthly 1972-2025 proxy T 1.26, H 1.20, M 1.14 (cash at 0, monthly
  averages; shown, not judged). So "holding beats trend on Sharpe" is a 2012-2025 euro fact
  without 2008 in it, not a law.
- **Crash insurance is real and consistent.** T had the best return in all 6 windows (2018-Q4
  tied with H); 2008 -0.7% vs -23% / -30%; 2022 +1.7% vs -6.7% / -17.4%. The 60/40 mix is the
  worst in every crash: euro long bonds did not hedge stocks in 2022.
- **Part of the smaller worst loss is just holding less.** T is invested 67% of the time. H
  scaled down to T's vol (73% invested, 27% cash; a hindsight constant, descriptive) has Sharpe
  0.78, worst loss 14.8% (T 13.6%), worst 12 months -8.3% (T -11.5%), longest under water 31
  months (T 58). Trend's edge over "hold less" is in sharp falls (2008, 2022), not in max DD.
- **The cost of trend is waiting.** T spent almost five years (2015-04 .. 2020-02) below its
  peak: whipsaws in the sideways 2015-2019 markets. Fees add to it: 21 orders a year vs ~2.

## 3. Which wins under which preference (card's rules)

| Preference | Winner | Trend worth it? |
|---|---|---|
| P1 best Sharpe after fees | M (H ~ M tie, M has fewer orders); T third in every cell | no, at every tier and book |
| P2 smallest worst loss | T (13.6% vs 19.8 / 22.3%) | yes where T's fee loss <= 0.10: EUR 1 tier from 5k; EUR 2 and 3 from 10k |
| P3 shortest time under water | H ~ M tie (31 mo), M on fewer orders | no |
| P4 crash insurance | T (6 of 6 windows) | yes, same books as P2 |
| P5 cheapest / simplest | M (1.2 orders a year) | no |

## 4. The plain answer (one screen)

**For a small coin-free euro book, trend is insurance you pay for, not a better investment.**

- **Run trend if** you would sell in panic after a 20-30% fall, or need the money on a date
  that might land in a crash: on these funds it cut the worst loss from ~20-22% to ~14% and
  stayed near flat in 2008 (US proxy) and 2022, when holding lost 7-30%. And only if the book is
  big enough for the fees: **EUR 5k+ at a EUR 1 order tier, EUR 10k+ at EUR 2 or EUR 3**
  (below that, fees eat more than 0.10 Sharpe).
- **Don't run trend if** you can sit through falls and care about the long-run result: simply
  holding the seven funds (or a 60/40 mix) gave a higher Sharpe (0.78 / 0.75 vs 0.62), nearly
  twice the yearly return (6-7% vs 3.7%), shorter waits under water (31 vs 58 months), 2 orders
  a year instead of 21, and needs no weekly attention. Below EUR 10k at EUR 2-3 per order,
  trend is not worth it for anyone.
- **Middle way** (descriptive, not tested as a rule): holding the seven funds with about a
  quarter in cash matched trend's worst loss within ~1 point at the same Sharpe as full
  holding; it gives up trend's near-flat 2008/2022, but costs no orders.
- **Honest uncertainty.** Every Sharpe gap here is about one standard error (SE of the gap
  0.10-0.17 over 14 years). The data cannot say whether trend or holding has the higher Sharpe
  in the long run; on a proxy that includes 2008, trend was level or ahead. What the data do
  say firmly: trend's falls are smaller and its fee bill larger. Choose by which pain you mind
  more (big falls or long flat stretches and fees), not by Sharpe.

## Rows counted

26 rows (idea `eu-6`): H and M on `euw` at no fee and 3 tiers x 3 books (20 `baseline`); the
three rules on `usw` from 2007-03-01 (T `robustness`, H and M `baseline`); the three on the long
monthly proxy (same kinds; Sharpe annualised from monthly returns, marked `long-monthly`). T on
`euw` is eu-5's saved D2 runs, re-scored without new rows. No row is a selectable trend variant
(a comparison of an existing rule with plain holding), so the eu family stays at 10; the choice
among T, H, M is its own family of three (bar p < 0.033), and no Sharpe lead passed it.
