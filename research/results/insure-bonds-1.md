# insure-bonds-1: before scoring

## Before scoring (card): sources, splice, autocorrelation and the fall threshold

Consol splice (BoE M10, monthly changes of the spliced column matched to 1e-6 against the NBER 1852-1888, Klovland 1870-1914 and Capie-Webber columns): Klovland 1870-1914 1866-01..1914-07; none 1914-08..1915-01; Capie-Webber 1915-02..1926-12. Klovland matches 1866-01..1914-07; no NBER period in the window, C2 starts at 1865-12; norway: no data in N2 interpolated. Cached CSV against the workbook's spliced column: largest relative difference 0.0e+00.

norway: yields for 1909 months 1822-03 to 1984-12, 5 runs: 1822-03..1842-06 (244), 1842-11..1842-12 (2), 1845-11..1848-03 (29), 1848-10..1914-08 (791), 1914-10..1984-12 (843). Scored segments: 3, 1823-04..1842-06, 1849-11..1914-08, 1915-11..1984-12.

consols: yields for 733 months 1865-12 to 1926-12, 1 runs: 1865-12..1926-12 (733). Scored segments: 1, 1867-01..1926-12.

| Series | Source period | Timing (documented) | Months | Missing inside | Lag-1 acf (pairs) | Noise line | Lag-2 acf | Zero yield changes | Stale-suspect |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| norway | N1 quotations abroad 1822-01-1842-12 | end month | 246 | 4 | +0.133 (242) | 0.106 | +0.152 | 23.0% | yes |
| norway | N3 quotations abroad 1845-01-1914-12 | end month | 823 | 7 | -0.024 (817) | 0.058 | -0.170 | 18.4% | no |
| norway | N4 Oslo 1915-01-1939-12 | end month | 300 | 0 | +0.051 (298) | 0.095 | +0.059 | 8.7% | no |
| norway | N5 Oslo, occupation 1940-01-1945-12 | end month | 72 | 0 | -0.260 (70) | 0.197 | -0.160 | 12.7% | no |
| norway | N6 Oslo, regulated 1946-01-1984-12 | end month | 468 | 0 | -0.052 (466) | 0.076 | +0.066 | 15.4% | no |
| consols | C2 Klovland (Goschen-corrected) 1865-12-1914-07 | last Friday | 584 | 0 | +0.023 (582) | 0.068 | -0.054 | 2.6% | no |
| consols | C3 Capie-Webber 1914-08-1926-12 | end month / averages | 149 | 0 | -0.134 (147) | 0.136 | +0.155 | 9.5% | no |

Monthly log total returns (Norway: 10-year par bond; consols: perpetuity), demeaned per source period, pairs inside the period. Noise line 1.645/sqrt(pairs). Zero yield changes: months whose yield equals the month before. Stale-suspect: acf1 above the noise line or zero changes above 20% (card).

| Series | Falls at 25% | 20% | 15% | 10% | Threshold (largest with >= 8) |
|---|---:|---:|---:|---:|---:|
| norway | 0 | 0 | 0 | 2 | 10% |
| consols | 0 | 2 | 2 | 4 | 10% |

Confirmed falls of the total-return holding level, fall d and rise d, scored window (rule positions not read).

**Amendment A (card, after the counts above, before any rule position was read):** with 2 and 4 falls at 10%, both card verdicts are fixed as "Too few falls". The readings below are added, with the same tests, nulls and verdict table, reported next to (not instead of) the card's verdicts.

| Reading | Falls per rung | Threshold (largest with >= 8) |
|---|---|---:|
| Norway, 10-year par bond, extended ladder | 10.0%: 2, 7.5%: 7, 5.0%: 11 | 5.0% |
| Consols, perpetuity, extended ladder | 10.0%: 4, 7.5%: 5, 5.0%: 10 | 5.0% |
| Norway, perpetuity, card ladder | 25.0%: 2, 20.0%: 4, 15.0%: 9, 10.0%: 16 | 15.0% |

Norway with a perpetuity total return, lag-1 acf by period (AR-null input): N1 +0.109 (242), N3 -0.016 (817), N4 +0.032 (298), N5 -0.214 (70), N6 -0.021 (466).

