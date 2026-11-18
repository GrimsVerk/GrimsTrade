# trend-1926: `tsmom12` on US stocks 1926-1961

Card and write-up: `trend-1926.md`. One run of the pre-registered evaluation, 2026-11-18.

Findings:

- Whole period: the rule is ahead on the market (0.88 against 0.55, +0.33, p 0.02), on the
  ten-industry book (+0.45, p below 0.01) and on 9 of 10 industries; worst loss 38% against 84%.
- The days out were rougher than the days in (market ratio 1.68, p 0.02; 10 of 10 industries).
- 1927-1945 carries it (+0.44). In 1946-1961 the market is behind (-0.09) and the mechanism is
  present on 1 of 10 industries.
- Without 1929-1932 the market's difference is +0.11 (p 0.18); from 1933 it is +0.09 (p 0.22):
  positive in sign, not clear of zero. The book keeps +0.21 and +0.19 (p 0.03 and 0.05).
- One spell out (1929-11 to 1933-04, bought back 67% lower) is the whole price gain; the other
  27 spells net to a loss in price.
- Outcome by the card: not "a property" (the market trails after the war), not "one crash
  again" (`d1` and `d3` stay positive). Crash insurance, not an edge.

<!-- tables below this line are written by lib/trend_1926.py -->

## 0. Data and checks

- Cache snapshot `french/2026-11-12`. 10043 sessions from 1926-07-01 to 1961-12-29; 1158 of them Saturdays. Sessions a year: 294 before 1952, 254 from 1952.
- Returns marked missing in the window: 0.
- First decision 1927-07-02; holding's first fill 1927-07-05.
- Replay check (the gym against trend-tune's paper series, which computes position x close-to-close return minus cost with no gym code): difference in total log growth from two weeks after the start, and the largest difference on any one day: F-Mkt +0.0019 / 0.00210; F-Durbl +0.0109 / 0.01510; F-Utils -0.0000 / 0.00001.

## 1. (a) The whole period: the rule against holding

One series, the whole account. `Difference` is Sharpe of the rule minus Sharpe of holding; p is the one-sided bootstrap p-value that the rule is better (mean block 20 days; `p125` with a mean block of 125 days). Sharpe on calendar days, cash earns 0. `F-ind10` is the ten industries as one equal-slot book against equal weight.

| Series | Sharpe hold | Sharpe rule | Difference (p) | 90% range | p125 | Growth/yr hold | Growth/yr rule | Worst loss hold | Worst loss rule | Time in |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| F-Mkt | 0.55 | 0.88 | +0.33 (0.02) | +0.06..+0.60 | 0.02 | 9.4% | 11.4% | 84% | 38% | 70% |
| F-NoDur | 0.67 | 1.05 | +0.38 (0.01) | +0.11..+0.68 | - | 9.2% | 10.4% | 68% | 32% | 71% |
| F-Durbl | 0.51 | 0.80 | +0.29 (0.03) | +0.03..+0.54 | - | 11.5% | 14.6% | 91% | 53% | 67% |
| F-Manuf | 0.53 | 0.85 | +0.31 (0.02) | +0.06..+0.57 | - | 10.2% | 12.7% | 89% | 49% | 68% |
| F-Enrgy | 0.55 | 0.55 | -0.00 (0.51) | -0.24..+0.23 | - | 10.1% | 7.7% | 79% | 57% | 67% |
| F-HiTec | 0.55 | 0.83 | +0.28 (0.03) | +0.03..+0.53 | - | 11.8% | 14.4% | 91% | 57% | 73% |
| F-Telcm | 0.66 | 0.97 | +0.32 (0.01) | +0.09..+0.57 | - | 9.6% | 11.2% | 70% | 33% | 76% |
| F-Shops | 0.59 | 1.06 | +0.47 (0.00) | +0.19..+0.75 | - | 10.0% | 13.3% | 85% | 34% | 71% |
| F-Hlth | 0.66 | 1.14 | +0.48 (0.00) | +0.20..+0.76 | - | 11.5% | 14.3% | 76% | 38% | 70% |
| F-Utils | 0.46 | 0.81 | +0.35 (0.02) | +0.07..+0.64 | - | 8.4% | 11.6% | 88% | 56% | 70% |
| F-Other | 0.40 | 0.74 | +0.35 (0.03) | +0.05..+0.64 | - | 6.6% | 10.1% | 90% | 48% | 65% |
| F-ind10 | 0.62 | 1.07 | +0.45 (0.00) | +0.19..+0.72 | 0.00 | 10.6% | 12.6% | 82% | 33% | 70% |

Industries where the rule is ahead: 9 of 10.

## 2. (b) The mechanism: were the days out rougher than the days in?

Sessions are split by whether the rule held the asset (from the gym's fills). Volatility is that of the asset's daily log returns, annualised. `p` is the share of 2,000 rotations of the in/out sequence against the returns that give a ratio at least as large. `Asset while in / out`: log points a year of in-time and of out-time.

| Series | Time in | Volatility in | Volatility out | Ratio out/in | p | Of the 20 worst sessions, rule was out | Asset while in | Asset while out |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F-Mkt | 70% | 16% | 27% | 1.68 | 0.02 | 8 | +15.5 | -6.4 |
| F-NoDur | 71% | 12% | 20% | 1.73 | 0.02 | 10 | +13.9 | -3.8 |
| F-Durbl | 67% | 24% | 39% | 1.64 | 0.01 | 12 | +20.6 | -8.3 |
| F-Manuf | 68% | 19% | 30% | 1.60 | 0.02 | 9 | +17.7 | -7.0 |
| F-Enrgy | 67% | 19% | 26% | 1.34 | 0.05 | 6 | +11.2 | +6.6 |
| F-HiTec | 73% | 22% | 37% | 1.74 | 0.04 | 9 | +18.4 | -8.9 |
| F-Telcm | 76% | 13% | 22% | 1.65 | 0.01 | 9 | +14.0 | -6.1 |
| F-Shops | 71% | 15% | 27% | 1.84 | 0.00 | 13 | +17.6 | -10.2 |
| F-Hlth | 70% | 15% | 27% | 1.81 | 0.00 | 17 | +19.2 | -8.5 |
| F-Utils | 70% | 18% | 32% | 1.81 | 0.06 | 8 | +15.8 | -9.8 |
| F-Other | 65% | 18% | 30% | 1.66 | 0.02 | 11 | +14.9 | -9.0 |

## 3. (c) Two eras and (d) without the great crash

Windows: `whole` = 1927-07 to 1961-12; `1927-45` = 1927-07 to 1945-12; `1946-61` = 1946-01 to 1961-12; `d1` = without 1929-1932; `d2` = without 1929-09-03 to 1932-07-08; `d3` = 1933-01 to 1961-12.

Sharpe of the rule minus Sharpe of holding (p):

| Series | whole | 1927-45 | 1946-61 | d1 | d2 | d3 |
|---|---:|---:|---:|---:|---:|---:|
| F-Mkt | +0.33 (0.02) | +0.44 (0.03) | -0.09 (0.74) | +0.11 (0.18) | +0.09 (0.27) | +0.09 (0.22) |
| F-NoDur | +0.38 (0.01) | +0.41 (0.03) | +0.12 (0.20) | +0.22 (0.04) | +0.14 (0.17) | +0.22 (0.04) |
| F-Durbl | +0.29 (0.03) | +0.37 (0.04) | +0.01 (0.48) | +0.06 (0.30) | +0.02 (0.46) | +0.04 (0.37) |
| F-Manuf | +0.31 (0.02) | +0.40 (0.03) | -0.02 (0.56) | +0.10 (0.21) | +0.10 (0.23) | +0.08 (0.27) |
| F-Enrgy | -0.00 (0.51) | -0.03 (0.55) | -0.12 (0.84) | -0.14 (0.91) | -0.20 (0.96) | -0.13 (0.90) |
| F-HiTec | +0.28 (0.03) | +0.29 (0.08) | +0.01 (0.47) | +0.05 (0.30) | +0.06 (0.33) | +0.04 (0.35) |
| F-Telcm | +0.32 (0.01) | +0.35 (0.03) | +0.05 (0.29) | +0.17 (0.04) | +0.15 (0.12) | +0.17 (0.06) |
| F-Shops | +0.47 (0.00) | +0.54 (0.01) | +0.08 (0.29) | +0.17 (0.07) | +0.13 (0.20) | +0.16 (0.12) |
| F-Hlth | +0.48 (0.00) | +0.51 (0.01) | +0.13 (0.15) | +0.16 (0.06) | +0.16 (0.12) | +0.16 (0.07) |
| F-Utils | +0.35 (0.02) | +0.34 (0.06) | +0.03 (0.41) | +0.32 (0.02) | +0.27 (0.07) | +0.30 (0.04) |
| F-Other | +0.35 (0.03) | +0.44 (0.04) | +0.03 (0.43) | +0.14 (0.16) | +0.09 (0.29) | +0.13 (0.17) |
| F-ind10 | +0.45 (0.00) | +0.47 (0.02) | +0.15 (0.09) | +0.21 (0.03) | +0.18 (0.10) | +0.19 (0.05) |
| industries ahead | 9 of 10 | 9 of 10 | 8 of 10 | 9 of 10 | 9 of 10 | 9 of 10 |

Levels for the market and the book (Sharpe hold / rule; worst loss hold / rule):

| Series | whole | 1927-45 | 1946-61 | d1 | d2 | d3 |
|---|---:|---:|---:|---:|---:|---:|
| F-Mkt | 0.55 / 0.88; 84% / 38% | 0.35 / 0.79; 84% / 38% | 1.20 / 1.11; 28% / 28% | 0.93 / 1.04; 51% / 38% | 0.97 / 1.06; 51% / 38% | 0.86 / 0.96; 51% / 38% |
| F-ind10 | 0.62 / 1.07; 82% / 33% | 0.41 / 0.89; 82% / 33% | 1.36 / 1.50; 28% / 23% | 1.03 / 1.24; 47% / 33% | 1.06 / 1.25; 47% / 33% | 0.95 / 1.14; 47% / 33% |

Volatility ratio, sessions out over sessions in (rotation p):

| Series | whole | 1927-45 | 1946-61 | d1 | d2 | d3 |
|---|---:|---:|---:|---:|---:|---:|
| F-Mkt | 1.68 (0.02) | 1.53 (0.03) | 1.22 (0.14) | 1.38 (0.08) | 1.59 (0.01) | 1.37 (0.08) |
| F-NoDur | 1.73 (0.02) | 1.62 (0.04) | 1.28 (0.16) | 1.41 (0.09) | 1.56 (0.04) | 1.40 (0.09) |
| F-Durbl | 1.64 (0.01) | 1.61 (0.02) | 1.15 (0.12) | 1.33 (0.05) | 1.51 (0.02) | 1.32 (0.04) |
| F-Manuf | 1.60 (0.02) | 1.54 (0.03) | 1.11 (0.22) | 1.32 (0.09) | 1.57 (0.01) | 1.31 (0.09) |
| F-Enrgy | 1.34 (0.05) | 1.27 (0.09) | 0.97 (0.54) | 1.14 (0.22) | 1.20 (0.11) | 1.16 (0.21) |
| F-HiTec | 1.74 (0.04) | 1.48 (0.05) | 1.21 (0.10) | 1.38 (0.16) | 1.63 (0.08) | 1.38 (0.15) |
| F-Telcm | 1.65 (0.01) | 1.51 (0.03) | 0.80 (0.45) | 1.40 (0.09) | 1.64 (0.05) | 1.40 (0.08) |
| F-Shops | 1.84 (0.00) | 1.74 (0.01) | 1.06 (0.24) | 1.38 (0.14) | 1.55 (0.03) | 1.39 (0.13) |
| F-Hlth | 1.81 (0.00) | 1.98 (0.00) | 0.83 (0.89) | 1.05 (0.28) | 1.32 (0.16) | 1.05 (0.31) |
| F-Utils | 1.81 (0.06) | 1.38 (0.09) | 1.27 (0.13) | 1.87 (0.01) | 1.97 (0.00) | 1.87 (0.01) |
| F-Other | 1.66 (0.02) | 1.63 (0.05) | 1.14 (0.24) | 1.31 (0.08) | 1.55 (0.01) | 1.28 (0.08) |
| industries where present | 10 of 10 | 10 of 10 | 1 of 10 | 6 of 10 | 8 of 10 | 6 of 10 |

Market, by window: share of sessions in, volatility in and out:

| Series | whole | 1927-45 | 1946-61 | d1 | d2 | d3 |
|---|---:|---:|---:|---:|---:|---:|
| F-Mkt | 70%; 16% / 27% | 61%; 20% / 31% | 82%; 11% / 13% | 77%; 15% / 21% | 76%; 15% / 24% | 76%; 15% / 21% |

## 4. Robustness: a later fill, higher costs, interest on cash

Sharpe of the rule minus Sharpe of its twin over the whole period (p). `late`: filled one session later. `10 bps`, `50 bps`: cost a side. `T-bill`: cash earns the T-bill return and both Sharpes are measured above it (a re-scoring of the primary runs).

| Series | Primary | late | 10 bps | 50 bps | T-bill | Sharpe above T-bills, hold / rule |
|---|---:|---:|---:|---:|---:|---:|
| F-Mkt | +0.33 (0.02) | +0.28 (0.04) | +0.32 (0.03) | +0.27 (0.05) | +0.32 (0.03) | 0.50 / 0.82 |
| F-NoDur | +0.38 (0.01) | +0.33 (0.02) | +0.37 (0.01) | +0.30 (0.04) | +0.36 (0.01) | 0.60 / 0.97 |
| F-Durbl | +0.29 (0.03) | +0.26 (0.05) | +0.28 (0.04) | +0.24 (0.07) | +0.28 (0.03) | 0.48 / 0.76 |
| F-Manuf | +0.31 (0.02) | +0.27 (0.04) | +0.30 (0.03) | +0.26 (0.05) | +0.31 (0.03) | 0.49 / 0.80 |
| F-Enrgy | -0.00 (0.51) | -0.02 (0.55) | -0.02 (0.55) | -0.08 (0.73) | +0.00 (0.50) | 0.51 / 0.51 |
| F-HiTec | +0.28 (0.03) | +0.26 (0.04) | +0.27 (0.04) | +0.24 (0.05) | +0.26 (0.04) | 0.51 / 0.78 |
| F-Telcm | +0.32 (0.01) | +0.29 (0.02) | +0.31 (0.01) | +0.27 (0.03) | +0.30 (0.01) | 0.59 / 0.89 |
| F-Shops | +0.47 (0.00) | +0.46 (0.00) | +0.46 (0.00) | +0.42 (0.01) | +0.46 (0.00) | 0.54 / 1.00 |
| F-Hlth | +0.48 (0.00) | +0.43 (0.01) | +0.47 (0.00) | +0.43 (0.00) | +0.47 (0.00) | 0.61 / 1.08 |
| F-Utils | +0.35 (0.02) | +0.32 (0.03) | +0.34 (0.02) | +0.30 (0.04) | +0.33 (0.02) | 0.42 / 0.75 |
| F-Other | +0.35 (0.03) | +0.33 (0.04) | +0.34 (0.03) | +0.29 (0.06) | +0.34 (0.03) | 0.35 / 0.69 |
| F-ind10 | +0.45 (0.00) | +0.42 (0.00) | +0.44 (0.00) | +0.39 (0.01) | +0.44 (0.00) | 0.57 / 1.01 |

Average T-bill return over the period: 1.0% a year.

## 5. Spells out (description)

A spell runs from an exit fill to the re-entry fill. A whipsaw is a spell bought back higher than it was sold. `Net` is the sum over spells of the price move avoided (positive: the rule gained by being out), in log points.

| Series | Spells | Whipsaws | Under 13 weeks: spells, net | 13 weeks or more: spells, net |
|---|---:|---:|---:|---:|
| F-Mkt | 28 | 22 | 19, -36 | 9, +102 |
| F-NoDur | 27 | 14 | 17, -4 | 10, +42 |
| F-Durbl | 35 | 23 | 25, -96 | 10, +192 |
| F-Manuf | 30 | 21 | 20, -48 | 10, +126 |
| F-Enrgy | 46 | 33 | 35, -66 | 11, -5 |
| F-HiTec | 22 | 17 | 15, -76 | 7, +157 |
| F-Telcm | 19 | 9 | 10, -4 | 9, +55 |
| F-Shops | 21 | 11 | 11, -12 | 10, +113 |
| F-Hlth | 21 | 12 | 11, -27 | 10, +116 |
| F-Utils | 27 | 16 | 18, -22 | 9, +125 |
| F-Other | 31 | 22 | 17, -44 | 14, +154 |

The market's spells out of 13 weeks or more:

| Out | Back | Days | Price at re-entry against price at exit |
|---|---|---:|---:|
| 1929-11-11 | 1933-04-08 | 1244 | -67% |
| 1934-06-30 | 1934-10-20 | 112 | -6% |
| 1935-01-12 | 1935-05-11 | 119 | +6% |
| 1937-09-11 | 1938-10-08 | 392 | -5% |
| 1940-09-07 | 1941-05-24 | 259 | -7% |
| 1941-10-18 | 1942-10-17 | 364 | +1% |
| 1946-10-05 | 1947-09-15 | 345 | +3% |
| 1949-04-23 | 1949-08-15 | 114 | +6% |
| 1957-09-23 | 1958-07-28 | 308 | +11% |

## 6. The card's outcome, applied mechanically

- market ahead over the whole period: yes
- market ahead in 1927-45: yes
- market ahead in 1946-61: no
- market ahead in `d1`: yes
- market ahead in `d3`: yes
- book agrees in sign over the whole period: yes
- book agrees in sign in `d1`: yes
- mechanism present on the market, whole period: yes
- mechanism present on the market, `d3`: yes
- primary and `late` fills agree in sign on the market: yes
- mechanism on its own: market present in 1927-45 yes, in 1946-61 no; industries present 10 of 10 and 1 of 10.

**Outcome: Something remains, but short of the card's conditions for a property.**
