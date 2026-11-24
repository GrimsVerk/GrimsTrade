# eu-2 results, amendment 2: EUR-hedged US equity

Train period only, window W (decisions 2012-01-02 .. 2025-11-09). Total-return prices; EUR books at percentage costs (`retail`: ETFs 0.10% + 0.05%), US books at the gym's, coins 0.25% + 0.05%; house band 1%. Sharpe on calendar days, zero risk-free rate. `IUSEL` = IUSE, iShares S&P 500 EUR Hedged (London EUR line); `XAD1` = Xtrackers Physical Gold EUR Hedged. Rows from eu-1 are re-scored from its saved runs (no new rows). Card: `cards/eu-2.md`.

## 1. Coin-free asset classes: does hedging remove the currency drag?

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@usw | 0.63 (0.27) | +3.6% | 5.9% | 11.1% | 3.0 | 61% | 0.20 | 0.82 | 0.81 |
| equal-weight@usw | 0.67 (0.27) | +5.8% | 9.1% | 18.7% | 0.2 | 100% | 0.23 | 1.05 | 0.68 |
| tsmom12@usw-eur | 0.54 (0.27) | +3.9% | 7.7% | 13.8% | 3.0 | 64% | 0.64 | 0.42 | 0.54 |
| equal-weight@usw-eur | 0.64 (0.27) | +6.7% | 11.1% | 19.1% | 0.2 | 100% | 0.58 | 0.78 | 0.55 |
| tsmom12@euw | 0.56 (0.27) | +3.2% | 5.9% | 14.3% | 2.9 | 67% | 0.66 | 0.33 | 0.74 |
| equal-weight@euw | 0.77 (0.27) | +6.3% | 8.5% | 19.8% | 0.2 | 100% | 0.67 | 0.82 | 0.84 |
| tsmom12@euw-h | 0.53 (0.27) | +2.8% | 5.5% | 14.3% | 2.9 | 66% | 0.61 | 0.27 | 0.78 |
| equal-weight@euw-h | 0.75 (0.27) | +6.0% | 8.2% | 19.8% | 0.2 | 100% | 0.61 | 0.83 | 0.81 |
| tsmom12@euw-hh | 0.43 (0.27) | +2.2% | 5.4% | 16.5% | 2.9 | 63% | 0.46 | 0.24 | 0.65 |
| equal-weight@euw-hh | 0.70 (0.27) | +5.5% | 8.2% | 19.8% | 0.2 | 100% | 0.53 | 0.81 | 0.76 |

| Book | tsmom12 - EW Sharpe | Change vs euw |
|---|---:|---:|
| usw | -0.04 | +0.17 |
| usw-eur | -0.10 | +0.10 |
| euw | -0.21 | +0.00 |
| euw-h | -0.21 | -0.01 |
| euw-hh | -0.27 | -0.06 |

- `euw-h`: gap change -0.01 (card: >= +0.06 removes, >= +0.03 in part): **no**
- `euw-hh`: gap change -0.06 (card: >= +0.06 removes, >= +0.03 in part): **no**

## 2. The live six with a hedged S&P 500 slot

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@us6 | 1.37 (0.28) | +29.5% | 20.5% | 36.5% | 2.8 | 72% | 1.64 | 1.50 | 0.88 |
| equal-weight@us6 | 1.32 (0.28) | +33.4% | 24.1% | 47.0% | 1.3 | 100% | 1.73 | 1.55 | 0.67 |
| tsmom12@eu6 | 1.44 (0.28) | +31.5% | 20.5% | 31.0% | 3.1 | 78% | 1.89 | 1.48 | 0.84 |
| equal-weight@eu6 | 1.38 (0.28) | +34.5% | 23.5% | 43.0% | 1.2 | 100% | 1.90 | 1.51 | 0.68 |
| tsmom12@eu6-h | 1.43 (0.28) | +31.0% | 20.3% | 32.1% | 3.1 | 77% | 1.89 | 1.46 | 0.87 |
| equal-weight@eu6-h | 1.36 (0.28) | +33.9% | 23.4% | 44.0% | 1.2 | 100% | 1.90 | 1.51 | 0.67 |

## 3. eu-1's character tests on the hedged books

### eu6-h vs us6: **holds**

| Test | EUR book | US book | Pass |
|---|---:|---:|---|
| 1. Sharpe tsmom12 - EW (within 0.15) | +0.07 | +0.05 | yes |
| 2. tsmom12 max DD (<= US + 5 pts, < EUR EW 44.0%) | 32.1% | 36.5% | yes |
| 3. tsmom12 turnover/yr (0.67x-1.5x; ratio 1.09) | 3.07 | 2.81 | yes |
| 4. crash sign of tsmom12 - EW matches (>= 3 of 4) | 4 of 4 | | yes |

### euw-h vs usw: **holds in part**

| Test | EUR book | US book | Pass |
|---|---:|---:|---|
| 1. Sharpe tsmom12 - EW (within 0.15) | -0.21 | -0.04 | **no** |
| 2. tsmom12 max DD (<= US + 5 pts, < EUR EW 19.8%) | 14.3% | 11.1% | yes |
| 3. tsmom12 turnover/yr (0.67x-1.5x; ratio 0.97) | 2.92 | 3.02 | yes |
| 4. crash sign of tsmom12 - EW matches (>= 3 of 4) | 4 of 4 | | yes |

## 4. Single slots: the filter against holding

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|
| tsmom12@IUSEL | 0.62 (0.28) | +7.4% | 12.8% | 30.6% | 2.0 | 84% |
| hold@IUSEL | 0.82 (0.27) | +12.3% | 15.5% | 34.8% | 0.0 | 100% |
| tsmom12@SXR8 | 0.70 (0.27) | +9.7% | 14.8% | 29.2% | 2.0 | 91% |
| hold@SXR8 | 0.97 (0.27) | +15.4% | 16.2% | 33.8% | 0.0 | 100% |
| tsmom12@SPY | 0.79 (0.28) | +10.5% | 13.9% | 31.2% | 1.8 | 88% |
| hold@SPY | 0.91 (0.27) | +14.8% | 16.7% | 33.7% | 0.0 | 100% |
| tsmom12@XAD1 | 0.27 (0.27) | +2.5% | 11.3% | 40.9% | 3.0 | 53% |
| hold@XAD1 | 0.37 (0.27) | +4.5% | 15.1% | 44.0% | 0.1 | 100% |
| tsmom12@4GLD | 0.60 (0.27) | +6.6% | 11.8% | 21.4% | 2.6 | 70% |
| hold@4GLD | 0.62 (0.27) | +8.0% | 14.0% | 36.8% | 0.1 | 100% |
| tsmom12@GLD | 0.48 (0.27) | +5.1% | 11.9% | 29.2% | 2.9 | 59% |
| hold@GLD | 0.50 (0.27) | +6.7% | 15.3% | 42.1% | 0.1 | 100% |

| Slot | tsmom12 - hold Sharpe |
|---|---:|
| IUSEL | -0.20 |
| SXR8 | -0.27 |
| SPY | -0.12 |
| XAD1 | -0.10 |
| 4GLD | -0.02 |
| GLD | -0.02 |

US slot behaves as in USD (IUSE's gap within 0.05 of SPY's): **no** (-0.20 vs -0.12; SXR8 -0.27).

Crash windows (total return inside each):

| Run | 2011 euro crisis | 2015-16 | 2018-Q4 | 2020 covid | 2022 rate shock |
|---|---:|---:|---:|---:|---:|
| tsmom12@euw | - | -8.0% | -4.1% | -11.7% | +2.1% |
| equal-weight@euw | - | -14.5% | -3.2% | -18.8% | -7.1% |
| tsmom12@euw-h | - | -7.4% | -3.9% | -12.0% | +1.2% |
| equal-weight@euw-h | - | -14.1% | -4.0% | -18.8% | -9.3% |
| tsmom12@euw-hh | - | -6.3% | -4.1% | -12.2% | -2.1% |
| equal-weight@euw-hh | - | -14.1% | -4.6% | -19.0% | -11.7% |
| tsmom12@IUSEL | - | -5.4% | -10.8% | -29.5% | -15.0% |
| hold@IUSEL | - | -14.0% | -18.4% | -34.8% | -25.7% |
| tsmom12@SXR8 | - | -12.2% | -12.5% | -27.1% | -10.9% |
| hold@SXR8 | - | -15.7% | -12.5% | -33.8% | -11.4% |
| tsmom12@SPY | - | -8.8% | -11.3% | -28.7% | -13.3% |
| hold@SPY | - | -13.0% | -19.3% | -33.7% | -24.5% |
| tsmom12@XAD1 | - | +0.0% | +0.0% | -4.0% | -13.6% |
| hold@XAD1 | - | +3.3% | +3.5% | -4.0% | -9.1% |
| tsmom12@4GLD | - | -7.5% | +1.8% | -3.3% | +7.9% |
| hold@4GLD | - | +2.1% | +7.6% | -3.3% | +7.9% |
| tsmom12@GLD | - | +0.0% | +0.0% | -3.6% | -8.5% |
| hold@GLD | - | +2.9% | +5.0% | -3.6% | -7.3% |

## Verdicts

- `euw-h`: currency drag no
- `euw-hh`: currency drag no
- US slot as in USD: no
