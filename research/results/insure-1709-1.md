# insure-1709-1: results

Card: `cards/insure-1709-1.md`. Written by `lib/insure1709.py`. This first version holds only the card's
before-scoring table, committed before any rule position or episode was computed.

## Before scoring (card): sampling, splice and autocorrelation

Splice of the share index (M13, monthly changes matched to 1e-6): last month matching Neal: 1811-02; first matching Acheson: 1825-04. So Neal to 1811-02, Gayer-Rostow-Schwartz without mines (the only M13 column whose changes match in between) 1811-03 to 1825-03, Acheson et al. from 1825-04. Cached CSV against the workbook's spliced column: largest relative difference 0.0e+00 (1893 common months).

shares: 1893 months 1709-04 to 1866-12, 1 runs of consecutive months: 1709-04..1866-12 (1893).

consols: 1361 months 1753-08 to 1866-12, 1 runs of consecutive months: 1753-08..1866-12 (1361).

| Series | Source period | Timing (documented) | Thin | Months | Missing inside | Lag-1 acf (pairs) | Noise line | Lag-2 acf | Zero-change months | Stale-suspect |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| shares | Neal (3 shares, unweighted) 1709-04-1811-02 | end month | yes | 1223 | 0 | +0.253 (1221) | 0.047 | +0.117 | 0.0% | yes |
| shares | Gayer-Rostow-Schwartz excl. mines (63 companies) 1811-03-1825-03 | not stated | no | 169 | 0 | +0.498 (167) | 0.127 | +0.259 | 6.0% | yes |
| shares | Acheson et al. (681 companies, cap-weighted) 1825-04-1866-12 | end month | no | 501 | 0 | +0.232 (499) | 0.074 | +0.025 | 2.4% | yes |
| consols | Neal (3% consols) 1753-08-1822-12 | end month | no | 833 | 0 | +0.032 (831) | 0.057 | +0.007 | 4.2% | no |
| consols | Odlyzko / NBER 1823-01-1866-12 | not stated | no | 528 | 0 | +0.028 (526) | 0.072 | -0.014 | 1.1% | no |

Monthly log returns, demeaned per source period, pairs exactly 1 (2) months apart within the period. Noise line 1.645/sqrt(pairs). Stale-suspect: lag-1 acf above its noise line or more than 20% zero-change months (card).

