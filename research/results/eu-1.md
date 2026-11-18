# eu-1 results: `tsmom12` on European UCITS ETFs in EUR

Train period only. Total-return prices. Sharpe on calendar days, zero risk-free rate, each book in its own currency. Costs: `gym` (ETFs 0 + 2 bps), `nl` (Dutch broker, ETFs 0.10% + 0.05%), `harsh` (ETFs 0.25% + 0.15%); coins 0.25% + 0.05% throughout. Card: `cards/eu-1.md`. Era columns are Sharpe ratios.

## 1. Window W, 2012-01-02 .. 2025-11-09

### The live six: US in USD, US in EUR, UCITS in EUR

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@us6 | 1.37 (0.28) | +29.5% | 20.5% | 36.5% | 2.8 | 72% | 1.64 | 1.50 | 0.88 |
| equal-weight@us6 | 1.32 (0.28) | +33.4% | 24.1% | 47.0% | 1.3 | 100% | 1.73 | 1.55 | 0.67 |
| tsmom12@us6-eur | 1.39 (0.28) | +31.7% | 21.4% | 31.3% | 3.1 | 75% | 1.83 | 1.46 | 0.78 |
| equal-weight@us6-eur | 1.31 (0.27) | +34.4% | 25.0% | 42.8% | 1.3 | 100% | 1.79 | 1.48 | 0.63 |
| tsmom12@eu6 | 1.44 (0.28) | +31.5% | 20.5% | 31.0% | 3.1 | 78% | 1.89 | 1.48 | 0.84 |
| equal-weight@eu6 | 1.38 (0.28) | +34.5% | 23.5% | 43.0% | 1.2 | 100% | 1.90 | 1.51 | 0.68 |

### Asset classes, no coins: US in USD, US in EUR, UCITS in EUR

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@usw | 0.63 (0.27) | +3.6% | 5.9% | 11.1% | 3.0 | 61% | 0.20 | 0.82 | 0.81 |
| equal-weight@usw | 0.67 (0.27) | +5.8% | 9.1% | 18.7% | 0.2 | 100% | 0.23 | 1.05 | 0.68 |
| tsmom12@usw-eur | 0.54 (0.27) | +3.9% | 7.7% | 13.8% | 3.0 | 64% | 0.64 | 0.42 | 0.54 |
| equal-weight@usw-eur | 0.64 (0.27) | +6.7% | 11.1% | 19.1% | 0.2 | 100% | 0.58 | 0.78 | 0.55 |
| tsmom12@euw | 0.56 (0.27) | +3.2% | 5.9% | 14.3% | 2.9 | 67% | 0.66 | 0.33 | 0.74 |
| equal-weight@euw | 0.77 (0.27) | +6.3% | 8.5% | 19.8% | 0.2 | 100% | 0.67 | 0.82 | 0.84 |

Buy and hold, for scale:

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hold-IWDA | 0.86 (0.27) | +12.7% | 15.4% | 33.6% | 0.0 | 100% | 0.99 | 0.87 | 0.67 |
| hold-SPY | 0.91 (0.27) | +14.8% | 16.7% | 33.7% | 0.0 | 100% | 1.10 | 0.99 | 0.68 |

## 2. The card's tests

### Pair A: eu6 vs us6: **holds**

| Test | EUR book | US book | Pass |
|---|---:|---:|---|
| 1. Sharpe tsmom12 - EW (within 0.15) | +0.06 | +0.05 | yes |
| 2. tsmom12 max DD (<= US + 5 pts, < EUR EW 43.0%) | 31.0% | 36.5% | yes |
| 3. tsmom12 turnover/yr (0.67x-1.5x; ratio 1.11) | 3.13 | 2.81 | yes |
| 4. crash sign of tsmom12 - EW matches (>= 3 of 4) | 4 of 4 | | yes |

### Pair B: euw vs usw: **holds in part**

| Test | EUR book | US book | Pass |
|---|---:|---:|---|
| 1. Sharpe tsmom12 - EW (within 0.15) | -0.21 | -0.04 | **no** |
| 2. tsmom12 max DD (<= US + 5 pts, < EUR EW 19.8%) | 14.3% | 11.1% | yes |
| 3. tsmom12 turnover/yr (0.67x-1.5x; ratio 0.96) | 2.92 | 3.02 | yes |
| 4. crash sign of tsmom12 - EW matches (>= 3 of 4) | 3 of 4 | | yes |

## 3. Crash windows (total return inside each, own currency)

| Run | 2011 euro crisis | 2015-16 | 2018-Q4 | 2020 covid | 2022 rate shock |
|---|---:|---:|---:|---:|---:|
| tsmom12@us6 | - | -7.8% | -5.9% | -21.8% | -13.5% |
| equal-weight@us6 | - | +9.8% | -17.4% | -22.3% | -36.7% |
| tsmom12@us6-eur | - | -0.4% | -5.3% | -22.0% | -12.5% |
| equal-weight@us6-eur | - | +8.0% | -14.3% | -22.0% | -26.0% |
| tsmom12@eu6 | - | -1.0% | -4.8% | -23.8% | -10.9% |
| equal-weight@eu6 | - | +6.5% | -14.3% | -24.6% | -29.1% |
| tsmom12@usw | - | -1.1% | -3.6% | -8.3% | -2.5% |
| equal-weight@usw | - | -11.8% | -7.2% | -16.2% | -16.5% |
| tsmom12@usw-eur | - | -6.5% | -5.0% | -8.4% | +0.3% |
| equal-weight@usw-eur | - | -13.4% | -4.4% | -16.1% | -2.4% |
| tsmom12@euw | - | -8.0% | -4.1% | -11.7% | +2.1% |
| equal-weight@euw | - | -14.5% | -3.2% | -18.8% | -7.1% |
| hold-IWDA | - | -20.3% | -14.4% | -33.6% | -13.3% |
| hold-SPY | - | -13.0% | -19.3% | -33.7% | -24.5% |

## 4. Costs and the bond slot

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|
| tsmom12@eu6 | 1.44 (0.28) | +31.5% | 20.5% | 31.0% | 3.1 | 78% |
| tsmom12@euw | 0.56 (0.27) | +3.2% | 5.9% | 14.3% | 2.9 | 67% |
| tsmom12@eu6/gym | 1.45 (0.28) | +31.9% | 20.5% | 31.0% | 3.1 | 78% |
| tsmom12@eu6/harsh | 1.41 (0.28) | +30.8% | 20.5% | 31.4% | 3.1 | 78% |
| tsmom12@euw/gym | 0.63 (0.27) | +3.6% | 5.8% | 12.7% | 2.9 | 67% |
| tsmom12@euw/harsh | 0.44 (0.27) | +2.4% | 5.9% | 18.1% | 2.9 | 67% |

IS04 (US Treasuries 20+, EUR-hedged; joins 2016) in place of IBGL:

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@eu6 | 1.44 (0.28) | +31.5% | 20.5% | 31.0% | 3.1 | 78% | 1.89 | 1.48 | 0.84 |
| tsmom12@eu6-is04 | 1.42 (0.28) | +33.2% | 21.9% | 30.2% | 2.9 | 76% | 1.75 | 1.49 | 0.78 |
| equal-weight@eu6-is04 | 1.39 (0.28) | +36.7% | 24.8% | 42.7% | 1.3 | 100% | 1.76 | 1.53 | 0.68 |
| equal-weight@eu6 | 1.38 (0.28) | +34.5% | 23.5% | 43.0% | 1.2 | 100% | 1.90 | 1.51 | 0.68 |

## 5. Single assets: the filter against holding, slot by slot

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|
| tsmom12@SXR8 | 0.70 (0.27) | +9.7% | 14.8% | 29.2% | 2.0 | 91% |
| hold@SXR8 | 0.97 (0.27) | +15.4% | 16.2% | 33.8% | 0.0 | 100% |
| tsmom12@SPY | 0.79 (0.28) | +10.5% | 13.9% | 31.2% | 1.8 | 88% |
| hold@SPY | 0.91 (0.27) | +14.8% | 16.7% | 33.7% | 0.0 | 100% |
| tsmom12@SXRV | 0.93 (0.27) | +16.3% | 18.1% | 30.6% | 1.1 | 90% |
| hold@SXRV | 1.06 (0.27) | +20.5% | 19.4% | 31.3% | 0.0 | 100% |
| tsmom12@QQQ | 0.90 (0.27) | +15.6% | 18.0% | 29.6% | 1.0 | 90% |
| hold@QQQ | 0.99 (0.27) | +19.9% | 20.5% | 35.1% | 0.0 | 100% |
| tsmom12@4GLD | 0.60 (0.27) | +6.6% | 11.8% | 21.4% | 2.6 | 70% |
| hold@4GLD | 0.62 (0.27) | +8.0% | 14.0% | 36.8% | 0.1 | 100% |
| tsmom12@GLD | 0.48 (0.27) | +5.1% | 11.9% | 29.2% | 2.9 | 59% |
| hold@GLD | 0.50 (0.27) | +6.7% | 15.3% | 42.1% | 0.1 | 100% |
| tsmom12@IBGL | 0.33 (0.27) | +2.3% | 7.7% | 21.6% | 3.6 | 68% |
| hold@IBGL | 0.27 (0.27) | +2.3% | 10.8% | 43.7% | 0.0 | 100% |
| tsmom12@TLT | 0.02 (0.27) | -0.3% | 10.6% | 33.0% | 2.5 | 51% |
| hold@TLT | 0.11 (0.27) | +0.6% | 14.6% | 48.4% | 0.1 | 100% |

| Run | 2011 euro crisis | 2015-16 | 2018-Q4 | 2020 covid | 2022 rate shock |
|---|---:|---:|---:|---:|---:|
| tsmom12@SXR8 | - | -12.2% | -12.5% | -27.1% | -10.9% |
| hold@SXR8 | - | -15.7% | -12.5% | -33.8% | -11.4% |
| tsmom12@SPY | - | -8.8% | -11.3% | -28.7% | -13.3% |
| hold@SPY | - | -13.0% | -19.3% | -33.7% | -24.5% |
| tsmom12@SXRV | - | -10.7% | -15.4% | -28.4% | -26.7% |
| hold@SXRV | - | -15.2% | -15.4% | -28.4% | -23.0% |
| tsmom12@QQQ | - | -12.3% | -20.6% | -27.7% | -19.3% |
| hold@QQQ | - | -12.0% | -22.0% | -27.9% | -34.3% |
| tsmom12@4GLD | - | -7.5% | +1.8% | -3.3% | +7.9% |
| hold@4GLD | - | +2.1% | +7.6% | -3.3% | +7.9% |
| tsmom12@GLD | - | +0.0% | +0.0% | -3.6% | -8.5% |
| hold@GLD | - | +2.9% | +5.0% | -3.6% | -7.3% |
| tsmom12@IBGL | - | +4.6% | -2.9% | -3.2% | +0.0% |
| hold@IBGL | - | +4.7% | +2.0% | -3.2% | -34.2% |
| tsmom12@TLT | - | +2.2% | +0.0% | +14.2% | -5.5% |
| hold@TLT | - | +13.2% | +4.5% | +14.2% | -29.3% |

## 6. Longer windows (robustness only)

### Asset classes from 2009-01-02 (native UCITS histories)

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@euw-2009 | 0.55 (0.25) | +3.2% | 6.1% | 14.3% | 2.8 | 66% | 0.83 | 0.56 | 0.33 | 0.74 |
| equal-weight@euw-2009 | 0.78 (0.25) | +6.7% | 8.9% | 19.8% | 0.2 | 100% | 1.21 | 0.63 | 0.82 | 0.85 |
| tsmom12@usw-2009 | 0.59 (0.25) | +3.8% | 6.6% | 11.1% | 2.9 | 63% | 0.33 | 0.37 | 0.82 | 0.81 |
| equal-weight@usw-2009 | 0.72 (0.25) | +7.0% | 10.1% | 18.8% | 0.2 | 100% | 1.10 | 0.46 | 1.04 | 0.67 |

| Run | 2011 euro crisis | 2015-16 | 2018-Q4 | 2020 covid | 2022 rate shock |
|---|---:|---:|---:|---:|---:|
| tsmom12@euw-2009 | -4.9% | -8.0% | -4.1% | -11.7% | +2.1% |
| equal-weight@euw-2009 | -5.5% | -14.5% | -3.1% | -18.8% | -7.0% |
| tsmom12@usw-2009 | -6.2% | -1.1% | -3.6% | -8.3% | -2.5% |
| equal-weight@usw-2009 | -7.1% | -11.7% | -7.2% | -16.3% | -16.6% |

### The six from 2000-01-03, spliced (`-S`: US ETFs in EUR before 2008-2010)

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@eu6-S-2000 | 0.94 (0.20) | +16.1% | 17.5% | 38.9% | 3.1 | 68% | -0.06 | 1.73 | 1.48 | 0.84 |
| equal-weight@eu6-S-2000 | 0.76 (0.20) | +16.1% | 23.2% | 70.5% | 1.2 | 100% | -0.09 | 1.78 | 1.51 | 0.68 |
| tsmom12@us6-2000 | 0.99 (0.20) | +16.8% | 17.2% | 36.5% | 2.8 | 70% | 0.21 | 1.55 | 1.50 | 0.88 |
| equal-weight@us6-2000 | 0.82 (0.20) | +17.3% | 22.7% | 68.8% | 1.3 | 100% | 0.03 | 1.67 | 1.55 | 0.67 |

Crash windows, plus the house's own 2000-02 and 2008 stress windows:

| Run | 2011 euro crisis | 2015-16 | 2018-Q4 | 2020 covid | 2022 rate shock |
|---|---:|---:|---:|---:|---:|
| tsmom12@eu6-S-2000 | +0.3% | -1.0% | -4.8% | -23.8% | -10.9% |
| equal-weight@eu6-S-2000 | +4.4% | +6.5% | -14.3% | -24.6% | -29.1% |
| tsmom12@us6-2000 | +0.3% | -7.8% | -5.9% | -21.8% | -13.5% |
| equal-weight@us6-2000 | +1.6% | +9.8% | -17.4% | -22.3% | -36.7% |

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| tsmom12@eu6-S-2000 | -30% | +1% | -24% | -11% | +6% | -22% | -17% |
| equal-weight@eu6-S-2000 | -69% | -17% | -25% | -29% | -6% | -39% | -37% |
| tsmom12@us6-2000 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight@us6-2000 | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## Verdicts

- Pair A: eu6 vs us6: **holds**
- Pair B: euw vs usw: **holds in part**
