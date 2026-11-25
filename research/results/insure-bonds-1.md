# insure-bonds-1: crash insurance of monthly `tsmom12` on Norwegian government bonds 1822-1984 and UK consols 1867-1926

Card: `cards/insure-bonds-1.md`. Written by `lib/insurebonds1.py`. Log points = 100 x natural log, rule minus holding unless said otherwise. Total returns rebuilt from yields (Norway: 10-year par bond; consols: perpetuity). Cash earns 0 unless the row says otherwise.

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

## Card: Norway (primary), falls of 10.0% (rise 10.0%)

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1939-02 | 1940-05 | 15 | 13% | -14 | -3 | +11 | +0.78 | -12 | -2 | N4 Oslo |
| 2 | 1979-11 | 1979-12 | 1 | 11% | -12 | -12 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |

Unfinished fall at the end (peak): none.

| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (insurance) | 1 | 1 | 0.5 | +5.3 | 0.245 |
| N = I + B (net of rebound) | 2 | 0 | 1 | -5.7 | 1.000 |
| I with cash at the discount rate | 1 | 1 | 0.5 | +6.9 | 0.245 |

| | Mean S (share avoided) | Pooled premium P |
|---|---:|---:|
| `tsmom12` monthly | +0.39 | 8.03 |
| Fixed exposure (x = 97%, 99%, 86%) | +0.15 | 14.24 |
| Random dates (1,000 rotations, median, 5-95%) | +0.00 (+0.00 to +0.50) | +6.74 (+3.47 to +43.49) |
| p: rotations at least as good | 0.188 | 0.245 |

Timing gap G = rule S minus mean rotation S: +0.252. Calm drag (rule minus holding per calm year): -0.42 log points. Premium from insure1's decomposition: 8.03.

Nulls not run: fewer than 5 falls with I != 0 (the verdict is fixed).

**Verdict (card, Norway (primary)): Too few falls** (weaker than claimed; handed back in the rebound; cheaper than holding less). Headline: lost less in 1 of 2 falls (ties against).

## Card: UK consols, falls of 10.0% (rise 10.0%)

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1899-03 | 1901-11 | 32 | 11% | -12 | -3 | +9 | +0.74 | -4 | +5 | C2 Klovland |
| 2 | 1914-06 | 1917-01 | 31 | 22% | -25 | -8 | +18 | +0.70 | -12 | +6 | C2 Klovland |
| 3 | 1918-10 | 1919-02 | 4 | 14% | -16 | -15 | +1 | +0.04 | -16 | -16 | C3 Capie-Webber |
| 4 | 1919-08 | 1920-11 | 15 | 20% | -23 | -15 | +8 | +0.33 | -16 | -9 | C3 Capie-Webber |

Unfinished fall at the end (peak): none.

| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (insurance) | 4 | 4 | 0.0625 | +8.7 | 0.000 |
| N = I + B (net of rebound) | 4 | 2 | 0.688 | -3.3 | 0.701 |
| I with cash at the discount rate | 4 | 4 | 0.0625 | +14.8 | 0.000 |

| | Mean S (share avoided) | Pooled premium P |
|---|---:|---:|
| `tsmom12` monthly | +0.45 | 2.28 |
| Fixed exposure (x = 76%) | +0.24 | 2.96 |
| Random dates (1,000 rotations, median, 5-95%) | +0.19 (+0.00 to +0.56) | +3.50 (+1.31 to +28.68) |
| p: rotations at least as good | 0.142 | 0.259 |

Timing gap G = rule S minus mean rotation S: +0.232. Calm drag (rule minus holding per calm year): -0.63 log points. Premium from insure1's decomposition: 2.28.

Nulls not run: fewer than 5 falls with I != 0 (the verdict is fixed).

**Verdict (card, UK consols): Too few falls** (at the claimed strength; handed back in the rebound; cheaper than holding less). Headline: lost less in 4 of 4 falls (ties against).

## Amendment A1: Norway, 10-year par bond, extended ladder, falls of 5.0% (rise 5.0%)

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1825-09 | 1826-03 | 6 | 6% | -6 | -8 | -2 | -0.36 | -7 | -9 | N1 quotations abroad |
| 2 | 1919-09 | 1920-07 | 10 | 8% | -8 | -3 | +5 | +0.67 | -8 | -2 | N4 Oslo |
| 3 | 1931-08 | 1931-09 | 1 | 5% | -5 | -5 | +0 | +0.00 | +0 | +0 | N4 Oslo |
| 4 | 1939-02 | 1940-02 | 12 | 11% | -12 | -3 | +9 | +0.75 | -6 | +3 | N4 Oslo |
| 5 | 1940-04 | 1940-05 | 1 | 7% | -7 | +0 | +7 | +1.00 | -12 | -5 | N5 Oslo, occupation |
| 6 | 1954-10 | 1956-07 | 21 | 9% | -10 | -7 | +3 | +0.29 | -5 | -2 | N6 Oslo, regulated |
| 7 | 1969-08 | 1969-09 | 1 | 8% | -9 | -9 | +0 | +0.00 | -8 | -8 | N6 Oslo, regulated |
| 8 | 1974-03 | 1974-04 | 1 | 9% | -9 | -9 | +0 | +0.00 | -7 | -7 | N6 Oslo, regulated |
| 9 | 1977-11 | 1977-12 | 1 | 9% | -10 | -10 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |
| 10 | 1979-11 | 1979-12 | 1 | 11% | -12 | -12 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |
| 11 | 1980-12 | 1981-05 | 5 | 7% | -7 | -7 | -0 | -0.00 | -7 | -7 | N6 Oslo, regulated |

Unfinished fall at the end (peak): none.

| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (insurance) | 6 | 4 | 0.344 | +2.0 | 0.014 |
| N = I + B (net of rebound) | 11 | 2 | 0.994 | -5.1 | 1.000 |
| I with cash at the discount rate | 6 | 4 | 0.344 | +2.8 | 0.006 |

| | Mean S (share avoided) | Pooled premium P |
|---|---:|---:|
| `tsmom12` monthly | +0.21 | 4.32 |
| Fixed exposure (x = 97%, 99%, 86%) | +0.14 | 4.78 |
| Random dates (1,000 rotations, median, 5-95%) | +0.09 (+0.00 to +0.27) | +6.03 (+2.12 to +34.80) |
| p: rotations at least as good | 0.164 | 0.321 |

Timing gap G = rule S minus mean rotation S: +0.090. Calm drag (rule minus holding per calm year): -0.13 log points. Premium from insure1's decomposition: 4.32.

| Null (1,000 worlds) | Median gap G (5-95%) | p: worlds with G >= observed | Worlds without a fall |
|---|---:|---:|---:|
| AR1: Gaussian AR(1), each source period's own mean, sd, lag-1 acf | +0.139 (-0.066 to +0.354) | 0.659 | 4 |
| BB: stationary block bootstrap of each period's returns, mean block 3 m | -0.011 (-0.114 to +0.146) | 0.132 | 1 |
| Reference: iid Gaussian (phi 0) | +0.125 (-0.042 to +0.333) | 0.641 | 1 |
| Description: AAFT phase-randomised surrogates (whole spectrum, own values) | +0.107 (-0.050 to +0.307) | 0.566 | 0 |

Observed G +0.090; p_AR (larger of AR1 and BB) = 0.659.

**Verdict (amendment a1, Norway, 10-year par bond, extended ladder): Does not hold** (weaker than claimed; handed back in the rebound; cheaper than holding less). Headline: lost less in 4 of 11 falls (ties against).

## Amendment A2: Consols, perpetuity, extended ladder, falls of 5.0% (rise 5.0%)

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1884-08 | 1885-03 | 7 | 8% | -8 | -6 | +2 | +0.24 | -9 | -7 | C2 Klovland |
| 2 | 1899-03 | 1901-11 | 32 | 11% | -12 | -3 | +9 | +0.74 | -4 | +5 | C2 Klovland |
| 3 | 1902-05 | 1904-02 | 21 | 7% | -7 | -5 | +2 | +0.31 | -6 | -3 | C2 Klovland |
| 4 | 1906-04 | 1907-08 | 16 | 6% | -6 | -2 | +4 | +0.61 | -7 | -3 | C2 Klovland |
| 5 | 1911-03 | 1912-10 | 19 | 6% | -6 | -4 | +2 | +0.37 | -3 | -0 | C2 Klovland |
| 6 | 1914-06 | 1916-04 | 22 | 18% | -19 | -8 | +12 | +0.60 | -7 | +5 | C2 Klovland |
| 7 | 1916-06 | 1917-01 | 7 | 12% | -13 | -0 | +13 | +1.00 | -12 | +1 | C3 Capie-Webber |
| 8 | 1918-10 | 1919-02 | 4 | 14% | -16 | -15 | +1 | +0.04 | -16 | -16 | C3 Capie-Webber |
| 9 | 1919-08 | 1920-11 | 15 | 20% | -23 | -15 | +8 | +0.33 | -16 | -9 | C3 Capie-Webber |
| 10 | 1922-11 | 1922-12 | 1 | 6% | -6 | -6 | +0 | +0.00 | -0 | -0 | C3 Capie-Webber |

Unfinished fall at the end (peak): none.

| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (insurance) | 10 | 10 | 0.000977 | +5.2 | 0.000 |
| N = I + B (net of rebound) | 10 | 3 | 0.945 | -2.7 | 0.927 |
| I with cash at the discount rate | 10 | 10 | 0.000977 | +8.5 | 0.000 |

| | Mean S (share avoided) | Pooled premium P |
|---|---:|---:|
| `tsmom12` monthly | +0.42 | 1.86 |
| Fixed exposure (x = 76%) | +0.24 | 2.29 |
| Random dates (1,000 rotations, median, 5-95%) | +0.20 (+0.05 to +0.45) | +2.68 (+1.25 to +14.14) |
| p: rotations at least as good | 0.069 | 0.243 |

Timing gap G = rule S minus mean rotation S: +0.200. Calm drag (rule minus holding per calm year): -0.44 log points. Premium from insure1's decomposition: 1.86.

| Null (1,000 worlds) | Median gap G (5-95%) | p: worlds with G >= observed | Worlds without a fall |
|---|---:|---:|---:|
| AR1: Gaussian AR(1), each source period's own mean, sd, lag-1 acf | +0.048 (-0.106 to +0.218) | 0.073 | 0 |
| BB: stationary block bootstrap of each period's returns, mean block 3 m | +0.054 (-0.096 to +0.251) | 0.097 | 0 |
| Reference: iid Gaussian (phi 0) | +0.060 (-0.086 to +0.234) | 0.094 | 0 |
| Description: AAFT phase-randomised surrogates (whole spectrum, own values) | -0.001 (-0.149 to +0.169) | 0.028 | 0 |

Observed G +0.200; p_AR (larger of AR1 and BB) = 0.097.

**Verdict (amendment a2, Consols, perpetuity, extended ladder): In between** (at the claimed strength; handed back in the rebound; cheaper than holding less). Headline: lost less in 10 of 10 falls (ties against).

## Amendment A3: Norway, perpetuity, card ladder, falls of 15.0% (rise 15.0%)

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1825-07 | 1826-03 | 8 | 17% | -19 | -16 | +3 | +0.14 | -17 | -14 | N1 quotations abroad |
| 2 | 1919-09 | 1920-07 | 10 | 20% | -23 | -6 | +17 | +0.73 | -21 | -5 | N4 Oslo |
| 3 | 1938-10 | 1940-05 | 19 | 37% | -46 | -10 | +36 | +0.78 | -31 | +4 | N4 Oslo |
| 4 | 1949-11 | 1951-11 | 24 | 23% | -26 | -5 | +21 | +0.82 | -7 | +14 | N6 Oslo, regulated |
| 5 | 1954-06 | 1956-07 | 25 | 36% | -45 | -4 | +41 | +0.91 | -16 | +25 | N6 Oslo, regulated |
| 6 | 1969-08 | 1969-09 | 1 | 19% | -21 | -21 | +0 | +0.00 | -11 | -11 | N6 Oslo, regulated |
| 7 | 1974-03 | 1974-04 | 1 | 17% | -18 | -18 | +0 | +0.00 | -6 | -6 | N6 Oslo, regulated |
| 8 | 1977-11 | 1977-12 | 1 | 16% | -18 | -18 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |
| 9 | 1979-11 | 1981-12 | 25 | 19% | -21 | -28 | -7 | -0.33 | -6 | -13 | N6 Oslo, regulated |

Unfinished fall at the end (peak): none.

| Test | Falls with value != 0 (n) | Above 0 (k) | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (insurance) | 7 | 6 | 0.0625 | +12.3 | 0.006 |
| N = I + B (net of rebound) | 9 | 3 | 0.91 | -1.7 | 0.664 |
| I with cash at the discount rate | 7 | 7 | 0.00781 | +16.0 | 0.000 |

| | Mean S (share avoided) | Pooled premium P |
|---|---:|---:|
| `tsmom12` monthly | +0.34 | 2.22 |
| Fixed exposure (x = 90%, 81%, 72%) | +0.27 | 2.99 |
| Random dates (1,000 rotations, median, 5-95%) | +0.24 (+0.06 to +0.48) | +3.59 (+1.65 to +10.69) |
| p: rotations at least as good | 0.217 | 0.177 |

Timing gap G = rule S minus mean rotation S: +0.087. Calm drag (rule minus holding per calm year): -0.89 log points. Premium from insure1's decomposition: 2.22.

| Null (1,000 worlds) | Median gap G (5-95%) | p: worlds with G >= observed | Worlds without a fall |
|---|---:|---:|---:|
| AR1: Gaussian AR(1), each source period's own mean, sd, lag-1 acf | +0.106 (-0.096 to +0.298) | 0.566 | 0 |
| BB: stationary block bootstrap of each period's returns, mean block 3 m | +0.031 (-0.158 to +0.250) | 0.335 | 0 |
| Reference: iid Gaussian (phi 0) | +0.106 (-0.102 to +0.292) | 0.565 | 0 |
| Description: AAFT phase-randomised surrogates (whole spectrum, own values) | +0.150 (-0.023 to +0.339) | 0.710 | 0 |

Observed G +0.087; p_AR (larger of AR1 and BB) = 0.566.

**Verdict (amendment a3, Norway, perpetuity, card ladder): Does not hold** (weaker than claimed; handed back in the rebound; cheaper than holding less). Headline: lost less in 6 of 9 falls (ties against).

## Pooled description: Norway and consols at 5% (A1 + A2), linked clusters

| # | First peak | Last trough | Series | Mean I | Mean S | Mean N |
|---:|---|---|---|---:|---:|---:|
| 1 | 1825-09 | 1826-03 | norway | -2 | -0.36 | -9 |
| 2 | 1884-08 | 1885-03 | consols | +2 | +0.24 | -7 |
| 3 | 1899-03 | 1901-11 | consols | +9 | +0.74 | +5 |
| 4 | 1902-05 | 1904-02 | consols | +2 | +0.31 | -3 |
| 5 | 1906-04 | 1907-08 | consols | +4 | +0.61 | -3 |
| 6 | 1911-03 | 1912-10 | consols | +2 | +0.37 | -0 |
| 7 | 1914-06 | 1916-04 | consols | +12 | +0.60 | +5 |
| 8 | 1916-06 | 1917-01 | consols | +13 | +1.00 | +1 |
| 9 | 1918-10 | 1919-02 | consols | +1 | +0.04 | -16 |
| 10 | 1919-08 | 1920-11 | consols, norway | +7 | +0.50 | -5 |
| 11 | 1922-11 | 1922-12 | consols | +0 | +0.00 | -0 |
| 12 | 1931-08 | 1931-09 | norway | +0 | +0.00 | +0 |
| 13 | 1939-02 | 1940-02 | norway | +9 | +0.75 | +3 |
| 14 | 1940-04 | 1940-05 | norway | +7 | +1.00 | -5 |
| 15 | 1954-10 | 1956-07 | norway | +3 | +0.29 | -2 |
| 16 | 1969-08 | 1969-09 | norway | +0 | +0.00 | -8 |
| 17 | 1974-03 | 1974-04 | norway | +0 | +0.00 | -7 |
| 18 | 1977-11 | 1977-12 | norway | +0 | +0.00 | -10 |
| 19 | 1979-11 | 1979-12 | norway | +0 | +0.00 | -10 |
| 20 | 1980-12 | 1981-05 | norway | -0 | -0.00 | -7 |

Clusters with mean I > 0: 13 of 15 non-zero (sign p 0.00369), bootstrap p 0.000.

## Checks (description)

| Run | Falls | I > 0 (ties against) | Sign p / boot p | N > 0 | S rule / fixed / random (p_rot) | Gap G | P rule / fixed | Calm drag a year |
|---|---:|---|---|---|---|---:|---|---:|
| norway | 2 | 1 of 2 | 0.5 / 0.245 | 0 of 2 | +0.39 / +0.15 / +0.00 (0.188) | +0.252 | 8.03 / 14.24 | -0.42 |
| consols | 4 | 4 of 4 | 0.0625 / 0.000 | 2 of 4 | +0.45 / +0.24 / +0.19 (0.142) | +0.232 | 2.28 / 2.96 | -0.63 |
| norway | 11 | 4 of 11 | 0.344 / 0.014 | 2 of 11 | +0.21 / +0.14 / +0.09 (0.164) | +0.090 | 4.32 / 4.78 | -0.13 |
| consols | 10 | 10 of 10 | 0.000977 / 0.000 | 3 of 10 | +0.42 / +0.24 / +0.20 (0.069) | +0.200 | 1.86 / 2.29 | -0.44 |
| norway | 9 | 6 of 9 | 0.0625 / 0.006 | 3 of 9 | +0.34 / +0.27 / +0.24 (0.217) | +0.087 | 2.22 / 2.99 | -0.89 |
| norway, cash at the discount rate | 2 | 1 of 2 | 0.5 / 0.245 | 1 of 2 | +0.51 / - / - | - | 2.11 / - | -0.11 |
| consols, cash at the discount rate | 4 | 4 of 4 | 0.0625 / 0.000 | 2 of 4 | +0.79 / - / - | - | 0.83 / - | -0.16 |
| norway, cash at the discount rate | 11 | 4 of 11 | 0.344 / 0.006 | 5 of 11 | +0.30 / - / - | - | 1.50 / - | -0.06 |
| consols, cash at the discount rate | 10 | 10 of 10 | 0.000977 / 0.000 | 6 of 10 | +0.73 / - / - | - | 0.88 / - | -0.28 |
| norway, cash at the discount rate | 9 | 7 of 9 | 0.00781 / 0.000 | 5 of 9 | +0.48 / - / - | - | 0.72 / - | -0.08 |
| Norway, perpetuity total return, 10% | 16 | 13 of 16 | 0.000122 / 0.000 | 5 of 16 | +0.42 / +0.26 / +0.23 (0.051) | +0.174 | 1.83 / 2.47 | -0.82 |
| consols, price only (1/y), 5% | 15 | 15 of 15 | 3.05e-05 / 0.000 | 10 of 15 | +0.59 / +0.51 / +0.50 (0.193) | +0.098 | 0.72 / 0.81 | -0.44 |
| norway, falls of 15.0% | 0 | 0 of 0 | 1 / 1.000 | 0 of 0 | +nan / +nan / +nan (0.000) | +nan | inf / inf | -0.48 |
| norway, falls of 7.5% | 7 | 3 of 7 | 0.125 / 0.019 | 0 of 7 | +0.25 / +0.15 / +0.14 (0.145) | +0.114 | 4.94 / 5.79 | -0.24 |
| consols, falls of 15.0% | 2 | 2 of 2 | 0.25 / 0.000 | 1 of 2 | +0.52 / +0.25 / +0.13 (0.122) | +0.302 | 2.76 / 4.08 | -0.78 |
| consols, falls of 7.5% | 5 | 5 of 5 | 0.0312 / 0.000 | 2 of 5 | +0.41 / +0.24 / +0.20 (0.093) | +0.188 | 2.21 / 2.78 | -0.51 |
| Norway 1822-1914 alone, 5% | 1 | 0 of 1 | 1 / 1.000 | 0 of 1 | -0.36 / +0.03 / +0.00 (1.000) | -0.381 | inf / 27.46 | -0.12 |
| Norway 1915-1984 alone, 5% | 10 | 4 of 10 | 0.188 / 0.006 | 2 of 10 | +0.27 / +0.15 / +0.10 (0.092) | +0.137 | 3.24 / 4.51 | -0.14 |
| Norway A1 GOV 1820-1920 (overlapping), 5% | 2 | 1 of 2 | 0.75 / 0.243 | 0 of 2 | +0.15 / +0.08 / +0.00 (0.184) | +0.079 | 7.59 / 6.06 | -0.12 |
| norway, signal one month older (stale check), 5% | 11 | 6 of 11 | 0.0156 / 0.000 | 0 of 10 | +0.21 / +0.14 / +0.10 (0.187) | +0.081 | 4.51 / 4.78 | -0.08 |
| consols, signal one month older (stale check), 5% | 10 | 7 of 10 | 0.0352 / 0.000 | 4 of 10 | +0.49 / +0.24 / +0.21 (0.031) | +0.264 | 1.22 / 2.29 | -0.22 |

p_rot: share of 1,000 rotations with mean S at least the rule's. Fixed exposure: the rule's mean position, no costs. The first rows are the card and amendment readings, then the same with cash at the discount rate (Norges Bank's for Norway, the BoE prime-paper rate for consols), then the checks at the threshold in their label.

### Episodes: Norway, perpetuity total return, 10%

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1825-07 | 1826-03 | 8 | 17% | -19 | -16 | +3 | +0.14 | -17 | -14 | N1 quotations abroad |
| 2 | 1853-08 | 1854-02 | 6 | 14% | -15 | -15 | +0 | +0.00 | -14 | -14 | N3 quotations abroad |
| 3 | 1857-06 | 1857-11 | 5 | 15% | -16 | -10 | +6 | +0.35 | -13 | -8 | N3 quotations abroad |
| 4 | 1898-06 | 1900-05 | 23 | 11% | -12 | -1 | +11 | +0.93 | -2 | +9 | N3 quotations abroad |
| 5 | 1919-09 | 1920-07 | 10 | 20% | -23 | -6 | +17 | +0.73 | -21 | -5 | N4 Oslo |
| 6 | 1922-08 | 1923-10 | 14 | 14% | -15 | -4 | +11 | +0.71 | -3 | +8 | N4 Oslo |
| 7 | 1931-05 | 1931-09 | 4 | 13% | -14 | -14 | +0 | +0.00 | -14 | -14 | N4 Oslo |
| 8 | 1938-10 | 1940-02 | 16 | 33% | -41 | -10 | +30 | +0.75 | -13 | +18 | N4 Oslo |
| 9 | 1940-04 | 1940-05 | 1 | 16% | -18 | +0 | +18 | +1.00 | -31 | -13 | N5 Oslo, occupation |
| 10 | 1949-11 | 1951-11 | 24 | 23% | -26 | -5 | +21 | +0.82 | -7 | +14 | N6 Oslo, regulated |
| 11 | 1954-06 | 1956-07 | 25 | 36% | -45 | -4 | +41 | +0.91 | -16 | +25 | N6 Oslo, regulated |
| 12 | 1969-08 | 1969-09 | 1 | 19% | -21 | -21 | +0 | +0.00 | -11 | -11 | N6 Oslo, regulated |
| 13 | 1974-03 | 1974-04 | 1 | 17% | -18 | -18 | +0 | +0.00 | -6 | -6 | N6 Oslo, regulated |
| 14 | 1977-11 | 1977-12 | 1 | 16% | -18 | -18 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |
| 15 | 1979-11 | 1979-12 | 1 | 17% | -19 | -19 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |
| 16 | 1980-12 | 1981-12 | 12 | 12% | -13 | -8 | +5 | +0.35 | -6 | -1 | N6 Oslo, regulated |

Unfinished fall at the end (peak): none.

### Episodes: norway, falls of 15.0%

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|

Unfinished fall at the end (peak): none.

### Episodes: Norway 1822-1914 alone, 5%

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1825-09 | 1826-03 | 6 | 6% | -6 | -8 | -2 | -0.36 | -7 | -9 | N1 quotations abroad |

Unfinished fall at the end (peak): none.

### Episodes: Norway 1915-1984 alone, 5%

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1919-09 | 1920-07 | 10 | 8% | -8 | -3 | +5 | +0.67 | -8 | -2 | N4 Oslo |
| 2 | 1931-08 | 1931-09 | 1 | 5% | -5 | -5 | +0 | +0.00 | +0 | +0 | N4 Oslo |
| 3 | 1939-02 | 1940-02 | 12 | 11% | -12 | -3 | +9 | +0.75 | -6 | +3 | N4 Oslo |
| 4 | 1940-04 | 1940-05 | 1 | 7% | -7 | +0 | +7 | +1.00 | -12 | -5 | N5 Oslo, occupation |
| 5 | 1954-10 | 1956-07 | 21 | 9% | -10 | -7 | +3 | +0.29 | -5 | -2 | N6 Oslo, regulated |
| 6 | 1969-08 | 1969-09 | 1 | 8% | -9 | -9 | +0 | +0.00 | -8 | -8 | N6 Oslo, regulated |
| 7 | 1974-03 | 1974-04 | 1 | 9% | -9 | -9 | +0 | +0.00 | -7 | -7 | N6 Oslo, regulated |
| 8 | 1977-11 | 1977-12 | 1 | 9% | -10 | -10 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |
| 9 | 1979-11 | 1979-12 | 1 | 11% | -12 | -12 | +0 | +0.00 | -10 | -10 | N6 Oslo, regulated |
| 10 | 1980-12 | 1981-05 | 5 | 7% | -7 | -7 | -0 | -0.00 | -7 | -7 | N6 Oslo, regulated |

Unfinished fall at the end (peak): none.

### Episodes: norway, signal one month older (stale check), 5%

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1825-09 | 1826-03 | 6 | 6% | -6 | -6 | +1 | +0.10 | -4 | -4 | N1 quotations abroad |
| 2 | 1919-09 | 1920-07 | 10 | 8% | -8 | -8 | +0 | +0.00 | -11 | -11 | N4 Oslo |
| 3 | 1931-08 | 1931-09 | 1 | 5% | -5 | -5 | +0 | +0.00 | +0 | +0 | N4 Oslo |
| 4 | 1939-02 | 1940-02 | 12 | 11% | -12 | -7 | +5 | +0.41 | -6 | -1 | N4 Oslo |
| 5 | 1940-04 | 1940-05 | 1 | 7% | -7 | +0 | +7 | +1.00 | -14 | -6 | N5 Oslo, occupation |
| 6 | 1954-10 | 1956-07 | 21 | 9% | -10 | -7 | +3 | +0.32 | -6 | -3 | N6 Oslo, regulated |
| 7 | 1969-08 | 1969-09 | 1 | 8% | -9 | -9 | +0 | +0.00 | -5 | -5 | N6 Oslo, regulated |
| 8 | 1974-03 | 1974-04 | 1 | 9% | -9 | -9 | +0 | +0.00 | -6 | -6 | N6 Oslo, regulated |
| 9 | 1977-11 | 1977-12 | 1 | 9% | -10 | -10 | +0 | +0.00 | -9 | -9 | N6 Oslo, regulated |
| 10 | 1979-11 | 1979-12 | 1 | 11% | -12 | -12 | +0 | +0.00 | -7 | -7 | N6 Oslo, regulated |
| 11 | 1980-12 | 1981-05 | 5 | 7% | -7 | -4 | +3 | +0.44 | -6 | -3 | N6 Oslo, regulated |

Unfinished fall at the end (peak): none.

### Episodes: consols, signal one month older (stale check), 5%

| # | Peak | Trough | Months | Depth | Holding, log pts | Rule, log pts | I | S | B (12 m) | N | Source at peak |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 1884-08 | 1885-03 | 7 | 8% | -8 | -8 | +0 | +0.00 | -7 | -7 | C2 Klovland |
| 2 | 1899-03 | 1901-11 | 32 | 11% | -12 | -3 | +9 | +0.77 | -5 | +5 | C2 Klovland |
| 3 | 1902-05 | 1904-02 | 21 | 7% | -7 | -2 | +5 | +0.71 | -7 | -2 | C2 Klovland |
| 4 | 1906-04 | 1907-08 | 16 | 6% | -6 | -2 | +4 | +0.64 | -8 | -4 | C2 Klovland |
| 5 | 1911-03 | 1912-10 | 19 | 6% | -6 | -3 | +4 | +0.61 | -4 | -0 | C2 Klovland |
| 6 | 1914-06 | 1916-04 | 22 | 18% | -19 | -8 | +12 | +0.60 | -7 | +5 | C2 Klovland |
| 7 | 1916-06 | 1917-01 | 7 | 12% | -13 | -0 | +13 | +1.00 | -10 | +3 | C3 Capie-Webber |
| 8 | 1918-10 | 1919-02 | 4 | 14% | -16 | -16 | +0 | +0.00 | -13 | -13 | C3 Capie-Webber |
| 9 | 1919-08 | 1920-11 | 15 | 20% | -23 | -10 | +13 | +0.56 | -4 | +9 | C3 Capie-Webber |
| 10 | 1922-11 | 1922-12 | 1 | 6% | -6 | -6 | -0 | -0.00 | -0 | -0 | C3 Capie-Webber |

Unfinished fall at the end (peak): none.

