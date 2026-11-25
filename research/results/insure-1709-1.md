# insure-1709-1: crash insurance of monthly `tsmom12` on UK shares and consols, 1709-1866

Card: `cards/insure-1709-1.md`. Written by `lib/insure1709.py`. Log points = 100 x natural log, rule minus holding unless said otherwise. Cash earns 0 unless the row says otherwise. Price indices (no dividends, no coupons unless stated).

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

## UK shares (primary): 25% falls

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1720-06 | 1722-09 | 27 | 74% | -133 | -111 | +22 | +0.16 | -7 | +15 | Neal |
| 2 | 1752-12 | 1762-01 | 109 | 38% | -48 | -10 | +39 | +0.80 | -20 | +19 | Neal |
| 3 | 1768-05 | 1784-10 | 197 | 43% | -55 | -18 | +38 | +0.68 | -3 | +35 | Neal |
| 4 | 1792-03 | 1797-05 | 62 | 40% | -51 | -27 | +24 | +0.47 | -3 | +21 | Neal |
| 5 | 1802-04 | 1803-07 | 15 | 30% | -36 | -9 | +27 | +0.75 | -12 | +15 | Neal |
| 6 | 1809-11 | 1816-09 | 82 | 42% | -54 | -7 | +47 | +0.86 | -11 | +36 | Neal |
| 7 | 1846-08 | 1848-10 | 26 | 28% | -33 | -3 | +30 | +0.91 | -19 | +11 | Acheson et al. |

Unfinished fall at the end (peak): none.

| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (insurance) | 7 | 7 | 0.00781 | +32.3 | 0.000 |
| N = I + B (net of rebound) | 7 | 7 | 0.00781 | +21.8 | 0.000 |
| I with cash at the discount rate | 7 | 7 | 0.00781 | +48.5 | 0.000 |

| | Mean S (share avoided) | Pooled premium P |
|---|---:|---:|
| `tsmom12` monthly | +0.66 | 0.70 |
| Fixed exposure (x = 61%) | +0.41 | 1.49 |
| Random dates (1,000 rotations, median, 5-95%) | +0.38 (+0.21 to +0.57) | +1.66 (+0.91 to +3.53) |
| p: rotations at least as good | 0.000 | 0.006 |

Timing gap G = rule S minus mean rotation S: +0.278. Calm drag (rule minus holding per calm year): -0.80 log points. Premium from insure1's decomposition: 0.70.

| Null (1,000 worlds) | Median gap G (5-95%) | p: worlds with G >= observed | Worlds without a fall |
|---|---:|---:|---:|
| AR1: Gaussian AR(1), each source period's own mean, sd, lag-1 acf | +0.152 (+0.035 to +0.269) | 0.035 | 0 |
| BB: stationary block bootstrap of each period's returns, mean block 3 m | +0.139 (-0.061 to +0.321) | 0.115 | 0 |
| Reference: iid Gaussian (phi 0), the event definition alone | +0.081 (-0.103 to +0.233) | 0.019 | 0 |

Observed G +0.278; p_AR (larger of AR1 and BB) = 0.115.

**Verdict by the card (shares): Holds, timing not separable from autocorrelation** (at the claimed strength; kept; cheaper than holding less). Headline: lost less in 7 of 7 falls (ties against).

## Consols (secondary): 25% falls

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1754-08 | 1762-01 | 89 | 41% | -52 | -17 | +35 | +0.67 | -33 | +2 | Neal |
| 2 | 1763-03 | 1782-02 | 227 | 43% | -56 | -25 | +30 | +0.54 | -11 | +19 | Neal |
| 3 | 1792-03 | 1798-01 | 70 | 51% | -71 | -28 | +43 | +0.60 | -6 | +36 | Neal |
| 4 | 1802-04 | 1803-07 | 15 | 32% | -39 | -30 | +9 | +0.23 | -9 | -0 | Neal |

Unfinished fall at the end (peak): none.

| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (insurance) | 4 | 4 | 0.0625 | +29.2 | 0.000 |
| N = I + B (net of rebound) | 4 | 3 | 0.312 | +14.3 | 0.003 |
| I with cash at the discount rate | 4 | 4 | 0.0625 | +48.1 | 0.000 |

| | Mean S (share avoided) | Pooled premium P |
|---|---:|---:|
| `tsmom12` monthly | +0.51 | 0.42 |
| Fixed exposure (x = 51%) | +0.51 | 0.84 |
| Random dates (1,000 rotations, median, 5-95%) | +0.49 (+0.22 to +0.72) | +1.01 (+0.42 to +2.10) |
| p: rotations at least as good | 0.422 | 0.051 |

Timing gap G = rule S minus mean rotation S: +0.034. Calm drag (rule minus holding per calm year): +0.13 log points. Premium from insure1's decomposition: 0.42.

| Null (1,000 worlds) | Median gap G (5-95%) | p: worlds with G >= observed | Worlds without a fall |
|---|---:|---:|---:|
| AR1: Gaussian AR(1), each source period's own mean, sd, lag-1 acf | +0.034 (-0.184 to +0.216) | 0.500 | 0 |
| BB: stationary block bootstrap of each period's returns, mean block 3 m | +0.047 (-0.198 to +0.246) | 0.551 | 0 |
| Reference: iid Gaussian (phi 0), the event definition alone | +0.016 (-0.233 to +0.218) | 0.449 | 0 |

Observed G +0.034; p_AR (larger of AR1 and BB) = 0.551.

**Verdict by the card (consols): Too few falls** (at the claimed strength; handed back in the rebound; cheaper than holding less). Headline: lost less in 4 of 4 falls (ties against).

## Pooled description: shares and consols, linked clusters

| # | First peak | Last trough | Series | Mean I | Mean S | Mean N |
|---:|---|---|---|---:|---:|---:|
| 1 | 1720-06 | 1722-09 | shares | +22 | +0.16 | +15 |
| 2 | 1752-12 | 1762-01 | consols, shares | +37 | +0.74 | +11 |
| 3 | 1763-03 | 1784-10 | consols, shares | +34 | +0.61 | +27 |
| 4 | 1792-03 | 1798-01 | consols, shares | +33 | +0.54 | +29 |
| 5 | 1802-04 | 1803-07 | consols, shares | +18 | +0.49 | +7 |
| 6 | 1809-11 | 1816-09 | shares | +47 | +0.86 | +36 |
| 7 | 1846-08 | 1848-10 | shares | +30 | +0.91 | +11 |

Clusters with mean I > 0: 7 of 7 non-zero (sign p 0.00781), bootstrap p 0.000.

## Checks (description)

| Run | Falls | I > 0 (ties against) | Sign p / boot p | N > 0 | S rule / fixed / random (p_rot) | Gap G | P rule / fixed | Calm drag a year |
|---|---:|---|---|---|---|---:|---|---:|
| shares | 7 | 7 of 7 | 0.00781 / 0.000 | 7 of 7 | +0.66 / +0.41 / +0.38 (0.000) | +0.278 | 0.70 / 1.49 | -0.80 |
| shares, cash at the discount rate | 7 | 7 of 7 | 0.00781 / 0.000 | 7 of 7 | +0.98 / - / - | - | 0.12 / - | +0.14 |
| consols, cash at the discount rate | 4 | 4 of 4 | 0.0625 / 0.000 | 4 of 4 | +0.84 / - / - | - | -0.55 / - | +2.05 |
| shares, 20% fall / 20% rise | 11 | 11 of 11 | 0.000488 / 0.000 | 11 of 11 | +0.67 / +0.41 / +0.38 (0.003) | +0.278 | 0.77 / 1.39 | -1.35 |
| shares, 40% fall / 25% rise | 3 | 3 of 3 | 0.125 / 0.000 | 3 of 3 | +0.57 / +0.41 / +0.40 (0.138) | +0.179 | 0.37 / 1.81 | -0.15 |
| shares, Neal alone | 5 | 5 of 5 | 0.0312 / 0.000 | 5 of 5 | +0.57 / +0.47 / +0.45 (0.173) | +0.129 | 0.72 / 1.10 | -1.02 |
| shares, Gayer-Rostow-Schwartz excl. mines alone | 1 | 1 of 1 | 0.5 / 0.000 | 1 of 1 | +1.03 / +0.43 / +0.36 (0.012) | +0.665 | 0.33 / 1.88 | -0.03 |
| shares, Acheson et al. alone | 1 | 1 of 1 | 0.5 / 0.000 | 1 of 1 | +0.91 / +0.22 / +0.07 (0.000) | +0.718 | 1.81 / 6.22 | -0.94 |
| index: Acheson paid-up weighted | 2 | 2 of 2 | 0.25 / 0.000 | 1 of 2 | +0.66 / +0.37 / +0.33 (0.107) | +0.313 | 0.87 / 2.18 | -0.27 |
| index: Acheson unweighted | 0 | 0 of 0 | 1 / 1.000 | 0 of 0 | +nan / +nan / +nan (0.000) | +nan | inf / inf | -0.89 |
| index: GRS with mines | 3 | 3 of 3 | 0.125 / 0.000 | 3 of 3 | +0.60 / +0.55 / +0.52 (0.336) | +0.071 | 0.22 / 0.87 | +0.76 |
| index: GRS without mines | 3 | 3 of 3 | 0.125 / 0.000 | 2 of 3 | +0.67 / +0.49 / +0.47 (0.129) | +0.201 | 0.16 / 1.13 | +0.70 |
| index: Hayek | 3 | 3 of 3 | 0.125 / 0.000 | 3 of 3 | +0.70 / +0.42 / +0.38 (0.002) | +0.310 | 0.21 / 1.00 | -0.02 |
| shares, signal one month older (stale check) | 7 | 7 of 7 | 0.00781 / 0.000 | 7 of 7 | +0.67 / +0.41 / +0.38 (0.000) | +0.282 | 0.92 / 1.48 | -1.27 |
| consols, signal one month older | 4 | 4 of 4 | 0.0625 / 0.000 | 3 of 4 | +0.62 / +0.51 / +0.49 (0.187) | +0.139 | 0.59 / 0.84 | -0.20 |
| consols with coupon accrual | 4 | 4 of 4 | 0.0625 / 0.000 | 3 of 4 | +0.66 / +0.29 / +0.26 (0.016) | +0.382 | 2.32 / 3.59 | -1.52 |

p_rot: share of 1,000 rotations with mean S at least the rule's. Fixed exposure: the rule's mean position, no costs. Check 4's indices overlap the primary's calendar (not independent).

### Episodes: shares, Neal alone

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1720-06 | 1722-09 | 27 | 74% | -133 | -111 | +22 | +0.16 | -7 | +15 | Neal |
| 2 | 1752-12 | 1762-01 | 109 | 38% | -48 | -10 | +39 | +0.80 | -20 | +19 | Neal |
| 3 | 1768-05 | 1784-10 | 197 | 43% | -55 | -18 | +38 | +0.68 | -3 | +35 | Neal |
| 4 | 1792-03 | 1797-05 | 62 | 40% | -51 | -27 | +24 | +0.47 | -3 | +21 | Neal |
| 5 | 1802-04 | 1803-07 | 15 | 30% | -36 | -9 | +27 | +0.75 | -12 | +15 | Neal |

Unfinished fall at the end (peak): none.

### Episodes: shares, Gayer-Rostow-Schwartz excl. mines alone

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1812-03 | 1816-09 | 54 | 27% | -32 | +1 | +32 | +1.03 | -11 | +22 | Gayer-Rostow-Schwartz excl. mines |

Unfinished fall at the end (peak): none.

### Episodes: shares, Acheson et al. alone

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1846-08 | 1848-10 | 26 | 28% | -33 | -3 | +30 | +0.91 | -19 | +11 | Acheson et al. |

Unfinished fall at the end (peak): none.

### Episodes: shares, signal one month older (stale check)

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1720-06 | 1722-09 | 27 | 74% | -133 | -111 | +22 | +0.16 | -6 | +16 | Neal |
| 2 | 1752-12 | 1762-01 | 109 | 38% | -48 | -9 | +39 | +0.81 | -18 | +21 | Neal |
| 3 | 1768-05 | 1784-10 | 197 | 43% | -55 | -15 | +41 | +0.74 | -5 | +36 | Neal |
| 4 | 1792-03 | 1797-05 | 62 | 40% | -51 | -23 | +28 | +0.55 | -3 | +25 | Neal |
| 5 | 1802-04 | 1803-07 | 15 | 30% | -36 | -10 | +26 | +0.73 | -12 | +14 | Neal |
| 6 | 1809-11 | 1816-09 | 82 | 42% | -54 | -9 | +46 | +0.84 | -12 | +34 | Neal |
| 7 | 1846-08 | 1848-10 | 26 | 28% | -33 | -5 | +28 | +0.85 | -21 | +7 | Acheson et al. |

Unfinished fall at the end (peak): none.

