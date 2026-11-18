# trend-1926-era2: `tsmom12` on US stocks 1961-2001

Card: `trend-1926.md`.

<!-- tables below this line are written by lib/trend_1926.py -->

## 0. Data and checks

- Cache snapshot `french/2026-11-12`. 10319 sessions from 1961-01-03 to 2001-12-31; 0 of them Saturdays. Sessions a year: 252.
- Returns marked missing in the window: 0.
- First decision 1962-01-02; holding's first fill 1962-01-08.
- Replay check (the gym against trend-tune's paper series, which computes position x close-to-close return minus cost with no gym code): difference in total log growth from two weeks after the start, and the largest difference on any one day: F62-Mkt +0.0031 / 0.00990; F62-Durbl -0.0088 / 0.00600; F62-Utils +0.0274 / 0.01670.

## 1. (a) The whole period: the rule against holding

One series, the whole account. `Difference` is Sharpe of the rule minus Sharpe of holding; p is the one-sided bootstrap p-value that the rule is better (mean block 20 days; `p125` with a mean block of 125 days). Sharpe on calendar days, cash earns 0. `F-ind10` is the ten industries as one equal-slot book against equal weight.

| Series | Sharpe hold | Sharpe rule | Difference (p) | 90% range | p125 | Growth/yr hold | Growth/yr rule | Worst loss hold | Worst loss rule | Time in |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| F62-Mkt | 0.80 | 0.88 | +0.07 (0.26) | -0.12..+0.26 | 0.27 | 10.8% | 9.7% | 48% | 32% | 77% |
| F62-NoDur | 0.95 | 1.02 | +0.07 (0.29) | -0.13..+0.28 | - | 12.5% | 11.2% | 54% | 35% | 77% |
| F62-Durbl | 0.61 | 0.62 | +0.01 (0.44) | -0.17..+0.20 | - | 9.7% | 8.0% | 58% | 45% | 72% |
| F62-Manuf | 0.75 | 0.73 | -0.02 (0.56) | -0.22..+0.18 | - | 10.4% | 8.1% | 44% | 41% | 74% |
| F62-Enrgy | 0.75 | 0.68 | -0.07 (0.78) | -0.21..+0.07 | - | 12.2% | 9.5% | 52% | 34% | 81% |
| F62-HiTec | 0.55 | 0.57 | +0.03 (0.40) | -0.15..+0.21 | - | 10.2% | 8.8% | 74% | 44% | 73% |
| F62-Telcm | 0.70 | 0.73 | +0.02 (0.41) | -0.14..+0.19 | - | 10.2% | 8.7% | 55% | 27% | 75% |
| F62-Shops | 0.78 | 0.65 | -0.12 (0.85) | -0.33..+0.08 | - | 11.7% | 7.6% | 61% | 52% | 72% |
| F62-Hlth | 0.82 | 0.73 | -0.08 (0.79) | -0.26..+0.09 | - | 13.1% | 9.7% | 48% | 36% | 75% |
| F62-Utils | 0.93 | 0.96 | +0.04 (0.39) | -0.16..+0.24 | - | 9.6% | 8.2% | 46% | 23% | 77% |
| F62-Other | 0.82 | 0.84 | +0.02 (0.44) | -0.21..+0.23 | - | 11.6% | 9.5% | 56% | 35% | 76% |
| F62-ind10 | 0.91 | 0.97 | +0.05 (0.29) | -0.11..+0.23 | 0.31 | 11.7% | 9.5% | 47% | 31% | 75% |

Industries where the rule is ahead: 6 of 10.

## 2. (b) The mechanism: were the days out rougher than the days in?

Sessions are split by whether the rule held the asset (from the gym's fills). Volatility is that of the asset's daily log returns, annualised. `p` is the share of 2,000 rotations of the in/out sequence against the returns that give a ratio at least as large. `Asset while in / out`: log points a year of in-time and of out-time.

| Series | Time in | Volatility in | Volatility out | Ratio out/in | p | Of the 20 worst sessions, rule was out | Asset while in | Asset while out |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| F62-Mkt | 77% | 13% | 17% | 1.31 | 0.08 | 7 | +12.1 | +4.2 |
| F62-NoDur | 77% | 13% | 16% | 1.26 | 0.11 | 8 | +13.8 | +5.1 |
| F62-Durbl | 72% | 17% | 21% | 1.25 | 0.01 | 7 | +10.8 | +5.3 |
| F62-Manuf | 74% | 14% | 17% | 1.28 | 0.07 | 8 | +10.5 | +8.1 |
| F62-Enrgy | 81% | 17% | 20% | 1.18 | 0.14 | 3 | +11.3 | +12.4 |
| F62-HiTec | 73% | 20% | 26% | 1.30 | 0.09 | 9 | +11.7 | +4.4 |
| F62-Telcm | 75% | 15% | 18% | 1.25 | 0.03 | 6 | +11.2 | +5.4 |
| F62-Shops | 72% | 15% | 19% | 1.27 | 0.05 | 9 | +10.3 | +13.3 |
| F62-Hlth | 75% | 16% | 19% | 1.15 | 0.12 | 6 | +12.5 | +12.1 |
| F62-Utils | 77% | 10% | 13% | 1.32 | 0.04 | 4 | +10.2 | +5.8 |
| F62-Other | 76% | 13% | 18% | 1.39 | 0.01 | 8 | +11.9 | +8.0 |

## 3. (c) Two eras and (d) without the great crash

Windows: `whole` = 1962-01 to 2001-12; `1962-81` = 1962-01 to 1981-12; `1982-01` = 1982-01 to 2001-12; `x1` = without 1973-1974; `x2` = without 1987; `x3` = without 1973-1974 and 1987; `to1993` = 1962-01 to 1993-12.

Sharpe of the rule minus Sharpe of holding (p):

| Series | whole | 1962-81 | 1982-01 | x1 | x2 | x3 | to1993 |
|---|---:|---:|---:|---:|---:|---:|---:|
| F62-Mkt | +0.07 (0.26) | +0.13 (0.25) | +0.03 (0.37) | -0.03 (0.64) | +0.09 (0.23) | -0.02 (0.59) | +0.06 (0.36) |
| F62-NoDur | +0.07 (0.29) | +0.32 (0.10) | -0.09 (0.83) | -0.08 (0.78) | +0.13 (0.17) | -0.04 (0.65) | +0.06 (0.33) |
| F62-Durbl | +0.01 (0.44) | +0.16 (0.18) | -0.10 (0.74) | -0.11 (0.86) | +0.04 (0.40) | -0.10 (0.82) | +0.01 (0.49) |
| F62-Manuf | -0.02 (0.56) | +0.05 (0.40) | -0.09 (0.73) | -0.10 (0.81) | +0.03 (0.43) | -0.06 (0.69) | -0.01 (0.53) |
| F62-Enrgy | -0.07 (0.78) | +0.13 (0.17) | -0.21 (0.96) | -0.11 (0.90) | -0.05 (0.71) | -0.10 (0.85) | -0.00 (0.52) |
| F62-HiTec | +0.03 (0.40) | -0.03 (0.57) | +0.07 (0.31) | -0.04 (0.67) | +0.06 (0.32) | -0.02 (0.58) | -0.10 (0.76) |
| F62-Telcm | +0.02 (0.41) | -0.09 (0.69) | +0.09 (0.25) | +0.03 (0.38) | +0.04 (0.37) | +0.05 (0.32) | -0.07 (0.78) |
| F62-Shops | -0.12 (0.85) | +0.13 (0.30) | -0.29 (0.99) | -0.29 (0.99) | -0.12 (0.84) | -0.30 (1.00) | +0.00 (0.51) |
| F62-Hlth | -0.08 (0.79) | -0.09 (0.68) | -0.09 (0.83) | -0.17 (0.95) | -0.06 (0.72) | -0.15 (0.92) | -0.10 (0.76) |
| F62-Utils | +0.04 (0.39) | +0.17 (0.26) | -0.05 (0.70) | -0.05 (0.67) | +0.04 (0.38) | -0.06 (0.69) | +0.10 (0.28) |
| F62-Other | +0.02 (0.44) | +0.20 (0.19) | -0.11 (0.78) | -0.12 (0.85) | +0.02 (0.44) | -0.12 (0.84) | +0.12 (0.27) |
| F62-ind10 | +0.05 (0.29) | +0.19 (0.17) | -0.04 (0.65) | -0.06 (0.75) | +0.10 (0.17) | -0.02 (0.61) | +0.06 (0.32) |
| industries ahead | 6 of 10 | 7 of 10 | 2 of 10 | 1 of 10 | 7 of 10 | 1 of 10 | 5 of 10 |

Levels for the market and the book (Sharpe hold / rule; worst loss hold / rule):

| Series | whole | 1962-81 | 1982-01 | x1 | x2 | x3 | to1993 |
|---|---:|---:|---:|---:|---:|---:|---:|
| F62-Mkt | 0.80 / 0.88; 48% / 32% | 0.63 / 0.77; 48% / 19% | 0.95 / 0.98; 40% / 32% | 0.96 / 0.93; 40% / 32% | 0.85 / 0.94; 48% / 22% | 1.02 / 1.00; 40% / 22% | 0.81 / 0.87; 48% / 32% |
| F62-ind10 | 0.91 / 0.97; 47% / 31% | 0.71 / 0.89; 47% / 16% | 1.09 / 1.05; 32% / 31% | 1.08 / 1.02; 33% / 31% | 0.97 / 1.07; 47% / 16% | 1.16 / 1.14; 33% / 16% | 0.90 / 0.96; 47% / 31% |

Volatility ratio, sessions out over sessions in (rotation p):

| Series | whole | 1962-81 | 1982-01 | x1 | x2 | x3 | to1993 |
|---|---:|---:|---:|---:|---:|---:|---:|
| F62-Mkt | 1.31 (0.08) | 1.58 (0.01) | 1.21 (0.21) | 1.26 (0.09) | 1.38 (0.01) | 1.33 (0.01) | 1.34 (0.06) |
| F62-NoDur | 1.26 (0.11) | 1.69 (0.00) | 1.09 (0.21) | 1.21 (0.14) | 1.36 (0.01) | 1.31 (0.02) | 1.28 (0.17) |
| F62-Durbl | 1.25 (0.01) | 1.39 (0.01) | 1.18 (0.17) | 1.23 (0.03) | 1.32 (0.00) | 1.29 (0.00) | 1.18 (0.11) |
| F62-Manuf | 1.28 (0.07) | 1.47 (0.01) | 1.22 (0.20) | 1.20 (0.17) | 1.39 (0.00) | 1.31 (0.00) | 1.24 (0.19) |
| F62-Enrgy | 1.18 (0.14) | 1.26 (0.02) | 1.17 (0.16) | 1.16 (0.15) | 1.24 (0.00) | 1.22 (0.03) | 1.19 (0.15) |
| F62-HiTec | 1.30 (0.09) | 1.46 (0.01) | 1.26 (0.20) | 1.31 (0.08) | 1.34 (0.05) | 1.35 (0.04) | 1.23 (0.06) |
| F62-Telcm | 1.25 (0.03) | 1.41 (0.01) | 1.28 (0.11) | 1.25 (0.03) | 1.32 (0.00) | 1.33 (0.00) | 1.21 (0.14) |
| F62-Shops | 1.27 (0.05) | 1.48 (0.01) | 1.28 (0.10) | 1.22 (0.09) | 1.28 (0.00) | 1.22 (0.01) | 1.31 (0.03) |
| F62-Hlth | 1.15 (0.12) | 1.54 (0.03) | 0.95 (0.60) | 1.06 (0.31) | 1.21 (0.05) | 1.11 (0.14) | 1.20 (0.10) |
| F62-Utils | 1.32 (0.04) | 1.63 (0.02) | 1.28 (0.18) | 1.27 (0.07) | 1.40 (0.01) | 1.34 (0.01) | 1.40 (0.04) |
| F62-Other | 1.39 (0.01) | 1.59 (0.01) | 1.30 (0.09) | 1.38 (0.01) | 1.41 (0.00) | 1.39 (0.01) | 1.44 (0.02) |
| industries where present | 7 of 10 | 10 of 10 | 1 of 10 | 6 of 10 | 10 of 10 | 9 of 10 | 4 of 10 |

Market, by window: share of sessions in, volatility in and out:

| Series | whole | 1962-81 | 1982-01 | x1 | x2 | x3 | to1993 |
|---|---:|---:|---:|---:|---:|---:|---:|
| F62-Mkt | 77%; 13% / 17% | 72%; 10% / 16% | 81%; 15% / 18% | 80%; 13% / 16% | 76%; 12% / 17% | 80%; 12% / 16% | 75%; 12% / 16% |

## 4. Robustness: a later fill, higher costs, interest on cash

Sharpe of the rule minus Sharpe of its twin over the whole period (p). `late`: filled one session later. `10 bps`, `50 bps`: cost a side. `T-bill`: cash earns the T-bill return and both Sharpes are measured above it (a re-scoring of the primary runs).

| Series | Primary | late | 10 bps | 50 bps | T-bill | Sharpe above T-bills, hold / rule |
|---|---:|---:|---:|---:|---:|---:|
| F62-Mkt | +0.07 (0.26) | +0.05 (0.32) | +0.06 (0.29) | +0.02 (0.43) | +0.10 (0.17) | 0.39 / 0.49 |
| F62-NoDur | +0.07 (0.29) | +0.06 (0.31) | +0.06 (0.32) | +0.01 (0.49) | +0.09 (0.23) | 0.51 / 0.60 |
| F62-Durbl | +0.01 (0.44) | -0.05 (0.64) | +0.00 (0.48) | -0.05 (0.67) | +0.06 (0.31) | 0.28 / 0.34 |
| F62-Manuf | -0.02 (0.56) | -0.03 (0.58) | -0.03 (0.59) | -0.08 (0.74) | +0.01 (0.44) | 0.35 / 0.36 |
| F62-Enrgy | -0.07 (0.78) | -0.07 (0.78) | -0.08 (0.81) | -0.14 (0.94) | -0.04 (0.66) | 0.41 / 0.37 |
| F62-HiTec | +0.03 (0.40) | -0.02 (0.57) | +0.02 (0.44) | -0.04 (0.66) | +0.06 (0.29) | 0.28 / 0.34 |
| F62-Telcm | +0.02 (0.41) | -0.01 (0.52) | +0.01 (0.48) | -0.07 (0.75) | +0.05 (0.30) | 0.33 / 0.38 |
| F62-Shops | -0.12 (0.85) | -0.17 (0.91) | -0.14 (0.88) | -0.22 (0.96) | -0.09 (0.76) | 0.41 / 0.32 |
| F62-Hlth | -0.08 (0.79) | -0.11 (0.87) | -0.10 (0.83) | -0.17 (0.94) | -0.06 (0.70) | 0.47 / 0.41 |
| F62-Utils | +0.04 (0.39) | -0.02 (0.59) | +0.02 (0.44) | -0.06 (0.71) | +0.05 (0.34) | 0.37 / 0.42 |
| F62-Other | +0.02 (0.44) | -0.01 (0.53) | +0.01 (0.47) | -0.05 (0.63) | +0.04 (0.37) | 0.42 / 0.46 |
| F62-ind10 | +0.05 (0.29) | +0.01 (0.44) | +0.04 (0.34) | -0.04 (0.64) | +0.06 (0.25) | 0.47 / 0.53 |

Average T-bill return over the period: 6.0% a year.

## 5. Spells out (description)

A spell runs from an exit fill to the re-entry fill. A whipsaw is a spell bought back higher than it was sold. `Net` is the sum over spells of the price move avoided (positive: the rule gained by being out), in log points.

| Series | Spells | Whipsaws | Under 13 weeks: spells, net | 13 weeks or more: spells, net |
|---|---:|---:|---:|---:|
| F62-Mkt | 25 | 18 | 14, -35 | 11, -4 |
| F62-NoDur | 28 | 18 | 19, -26 | 9, -20 |
| F62-Durbl | 38 | 28 | 26, -65 | 12, +4 |
| F62-Manuf | 30 | 21 | 18, -72 | 12, -12 |
| F62-Enrgy | 43 | 32 | 35, -91 | 8, -3 |
| F62-HiTec | 51 | 41 | 41, -102 | 10, +55 |
| F62-Telcm | 46 | 35 | 34, -96 | 12, +41 |
| F62-Shops | 51 | 40 | 41, -112 | 10, -35 |
| F62-Hlth | 47 | 35 | 38, -111 | 9, -10 |
| F62-Utils | 34 | 26 | 25, -67 | 9, +15 |
| F62-Other | 31 | 23 | 21, -51 | 10, -24 |

The market's spells out of 13 weeks or more:

| Out | Back | Days | Price at re-entry against price at exit |
|---|---|---:|---:|
| 1962-05-14 | 1963-04-08 | 329 | +10% |
| 1966-08-22 | 1967-02-20 | 182 | +14% |
| 1969-06-16 | 1971-01-05 | 568 | -6% |
| 1973-04-09 | 1973-10-08 | 182 | +3% |
| 1973-10-29 | 1975-04-28 | 546 | -19% |
| 1977-12-12 | 1978-04-10 | 119 | -1% |
| 1981-12-21 | 1982-09-07 | 260 | +1% |
| 1984-04-24 | 1984-08-06 | 104 | +5% |
| 1988-01-11 | 1988-10-24 | 287 | +20% |
| 1990-08-06 | 1991-01-28 | 175 | -2% |
| 2000-11-20 | 2001-12-31 (still out) | 406 | -15% |

## 6. The card's outcome, applied mechanically

- market ahead over the whole period: yes
- market ahead in 1962-81: yes
- market ahead in 1982-01: yes
- market ahead in `x3`: no
- market ahead in `x1`: no
- book agrees in sign over the whole period: yes
- book agrees in sign in `x3`: yes
- mechanism present on the market, whole period: yes
- mechanism present on the market, `x1`: yes
- primary and `late` fills agree in sign on the market: yes
- mechanism on its own: market present in 1962-81 yes, in 1982-01 no; industries present 10 of 10 and 1 of 10.

**Outcome: Crashes only.**
