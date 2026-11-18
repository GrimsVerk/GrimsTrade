# live-check: our backtests against live funds of their family

Card: `cards/live-check.md` (committed before any number). Descriptive, nothing selected, held-out year unread (no month after 2025-10). All figures are monthly returns **above the 13-week T-bill**; our rules earn the bill on cash (`cash_interest.rescored`). Sharpe = monthly mean / sd x sqrt 12. Live funds: net asset value with distributions (after fees and real costs). TC = equal weight of the trend funds alive each month (RYMFX, AQMIX, ASFYX, WTMF, PQTIX, ABYIX, DBMF, KMLM, CTA); RC = the same for ABRZX, AQRIX, RPAR.

## 1. Sharpe by window

L = 2010-02..2025-10 (the live window), L07 = 2007-04..2025-10 (RYMFX's), P = 1985-01..2009-12 for the AQR factor (the paper's sample) and 1994-02..2009-12 for ours.

| Series | Months in L | Sharpe L | Sharpe L07 | Sharpe P | Own life | Sharpe own life |
|---|---:|---:|---:|---:|---|---:|
| tsmom12 | 189 | 1.11 | 1.02 | 0.55 | 1994-02 .. 2025-10 | 0.86 |
| tsmom12-c00 | 189 | 1.02 | 0.89 | 0.55 | 1994-02 .. 2025-10 | 0.72 |
| where-vol | 189 | 1.14 | 1.04 | 0.55 | 1994-02 .. 2025-10 | 0.87 |
| sixty-forty | 189 | 0.93 | 0.72 | 0.40 | 1994-02 .. 2025-10 | 0.66 |
| TC (trend funds) | 189 | 0.19 | 0.17 | 0.25 | 2007-03 .. 2025-10 | 0.17 |
| RC (risk-parity funds) | 189 | 0.60 | - | - | 2009-07 .. 2025-10 | 0.63 |
| AQR TSMOM factor (paper) | 189 | 0.35 | 0.37 | 1.41 | 1985-01 .. 2025-10 | 0.95 |
| RYMFX | 189 | -0.05 | -0.02 | 0.25 | 2007-03 .. 2025-10 | -0.02 |
| AQMIX | 189 | 0.29 | - | - | 2010-02 .. 2025-10 | 0.29 |
| ASFYX | 182 | 0.17 | - | - | 2010-09 .. 2025-10 | 0.17 |
| WTMF | 177 | -0.11 | - | - | 2011-02 .. 2025-10 | -0.11 |
| PQTIX | 141 | 0.25 | - | - | 2014-02 .. 2025-10 | 0.25 |
| ABYIX | 135 | 0.28 | - | - | 2014-08 .. 2025-10 | 0.28 |
| DBMF | 77 | 0.49 | - | - | 2019-06 .. 2025-10 | 0.49 |
| KMLM | 58 | 0.07 | - | - | 2021-01 .. 2025-10 | 0.07 |
| CTA | 43 | 0.40 | - | - | 2022-04 .. 2025-10 | 0.40 |
| ABRZX | 189 | 0.53 | - | - | 2009-07 .. 2025-10 | 0.57 |
| AQRIX | 181 | 0.63 | - | - | 2010-10 .. 2025-10 | 0.63 |
| RPAR | 70 | 0.14 | - | - | 2020-01 .. 2025-10 | 0.14 |
| LFMIX | 174 | 0.16 | - | - | 2011-05 .. 2025-10 | 0.16 |
| SPLV | 173 | 0.74 | - | - | 2011-06 .. 2025-10 | 0.74 |
| USMV | 168 | 0.90 | - | - | 2011-11 .. 2025-10 | 0.90 |
| QSPIX | 144 | 0.46 | - | - | 2013-11 .. 2025-10 | 0.46 |
| QRPIX | 97 | 0.37 | - | - | 2017-10 .. 2025-10 | 0.37 |
| SPY | 189 | 0.92 | 0.65 | 0.31 | 1993-02 .. 2025-10 | 0.60 |
| hold-c17 | 189 | 1.11 | 1.03 | 0.26 | 1994-02 .. 2025-10 | 0.74 |

## 2. Correlation of monthly excess returns (months in common within L)

Rows: ours. Funds need 36 months in common; n in brackets.

| Ours | TC (trend funds) | RC (risk-parity funds) | AQR TSMOM factor (paper) | SPY | RYMFX | AQMIX | ASFYX | WTMF | PQTIX | ABYIX | DBMF | KMLM | CTA | ABRZX | AQRIX | RPAR | LFMIX | SPLV | USMV | QSPIX | QRPIX |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 | 0.17 (189) | 0.36 (189) | 0.09 (189) | 0.40 (189) | 0.21 (189) | 0.10 (189) | 0.20 (182) | 0.20 (177) | 0.08 (141) | 0.14 (135) | 0.13 (77) | -0.12 (58) | -0.13 (43) | 0.36 (189) | 0.35 (181) | 0.43 (70) | 0.22 (174) | 0.35 (173) | 0.38 (168) | -0.01 (144) | -0.04 (97) |
| tsmom12-c00 | 0.17 (189) | 0.68 (189) | 0.12 (189) | 0.72 (189) | 0.25 (189) | 0.05 (189) | 0.25 (182) | 0.21 (177) | 0.01 (141) | 0.13 (135) | 0.06 (77) | -0.30 (58) | -0.29 (43) | 0.66 (189) | 0.63 (181) | 0.67 (70) | 0.23 (174) | 0.61 (173) | 0.68 (168) | -0.11 (144) | -0.03 (97) |
| where-vol | 0.12 (189) | 0.43 (189) | 0.06 (189) | 0.44 (189) | 0.18 (189) | 0.03 (189) | 0.15 (182) | 0.24 (177) | 0.03 (141) | 0.08 (135) | -0.00 (77) | -0.21 (58) | -0.35 (43) | 0.42 (189) | 0.40 (181) | 0.56 (70) | 0.17 (174) | 0.37 (173) | 0.40 (168) | -0.06 (144) | -0.12 (97) |
| sixty-forty | -0.09 (189) | 0.85 (189) | -0.08 (189) | 0.83 (189) | 0.04 (189) | -0.22 (189) | -0.00 (182) | 0.21 (177) | -0.21 (141) | -0.10 (135) | -0.30 (77) | -0.53 (58) | -0.49 (43) | 0.80 (189) | 0.77 (181) | 0.93 (70) | 0.03 (174) | 0.74 (173) | 0.83 (168) | -0.15 (144) | -0.17 (97) |

Live against paper: TC with the AQR factor 0.71 (189 months); AQMIX with the AQR factor 0.76 (189). TC with SPY -0.06; RC with SPY 0.76.

## 3. Crash years (calendar-year excess return; 2020-02..03 two-month return)

| Series | 2008 | 2020 | 2020-02..03 | 2022 |
|---|---:|---:|---:|---:|
| tsmom12 | -1.6% | +72.4% | -14.1% | -12.9% |
| tsmom12-c00 | -1.6% | +19.8% | -9.0% | -11.1% |
| where-vol | -1.6% | +79.0% | -14.1% | -27.4% |
| sixty-forty | -13.2% | +20.6% | -6.5% | -24.5% |
| TC (trend funds) | +7.1% | +4.6% | +3.6% | +17.6% |
| RC (risk-parity funds) | - | +9.9% | -9.4% | -17.8% |
| AQR TSMOM factor (paper) | +24.6% | -6.7% | +10.5% | +24.7% |
| RYMFX | +7.1% | +1.8% | -0.5% | +12.5% |
| AQMIX | - | -0.8% | +5.0% | +32.8% |
| ASFYX | - | +13.2% | +6.8% | +33.0% |
| WTMF | - | +0.1% | +1.5% | -8.4% |
| PQTIX | - | +8.6% | +8.7% | +9.4% |
| ABYIX | - | +7.6% | +5.3% | +14.8% |
| DBMF | - | +1.4% | -1.0% | +19.2% |
| KMLM | - | - | - | +21.8% |
| CTA | - | - | - | - |
| ABRZX | - | +8.8% | -10.8% | -16.7% |
| AQRIX | - | +2.3% | -10.8% | -12.3% |
| RPAR | - | +19.0% | -6.6% | -24.4% |
| LFMIX | - | +5.3% | -3.1% | +13.2% |
| SPLV | - | -1.7% | -21.5% | -6.7% |
| USMV | - | +5.3% | -19.2% | -11.2% |
| QSPIX | - | -22.2% | -7.0% | +28.2% |
| QRPIX | - | -21.3% | -7.5% | +22.8% |
| SPY | -37.7% | +17.9% | -19.5% | -19.8% |
| hold-c17 | -12.9% | +111.0% | -11.8% | -37.7% |

## 4. Haircut, trend family

| Step | From | To | Sharpe from | Sharpe to | Kept |
|---|---|---|---:|---:|---:|
| (a) post-sample decay of the published portfolio | AQR factor, P | AQR factor, L | 1.41 | 0.35 | 25% |
| (b) implementation and fees | AQR factor, L | AQMIX, L | 0.35 | 0.29 | 83% |
| (b') same, the fund panel | AQR factor, L | TC, L | 0.35 | 0.19 | 54% |
| **(c) total: h = 1 - kept** | AQR factor, P | AQMIX, L | 1.41 | 0.29 | 20% (h = 80%) |
| (d) our split | `tsmom12`, 1994-2009 | `tsmom12`, L | 0.55 | 1.11 | 201% |
| (d) our split | `tsmom12-c00`, 1994-2009 | `tsmom12-c00`, L | 0.55 | 1.02 | 184% |

## 5. Sharpe gap in L (ours minus its live family)

- `tsmom12` 1.11 vs TC 0.19 on the same 189 months: +0.92.
- `tsmom12-c00` 1.02 vs TC 0.19 on the same 189 months: +0.83.
- `where-vol` 1.14 vs RC 0.60 on the same 189 months: +0.54.
- `sixty-forty` 0.93 vs RC 0.60 on the same 189 months: +0.34.

## 6. For step 3: expected live Sharpe of `tsmom12` and forward length

`tsmom12` backtest 1994-2025: Sharpe 1.05 (repo convention: daily, 365, zero rate). Weekly returns: Sharpe 1.03, skew +0.33, kurtosis 12.6. Weekly `tsmom12` minus `hold-c17`: Sharpe -0.10, skew +0.20, kurtosis 19.9.

Weeks needed (forward-1's `sharpe` formula, power 0.8, one-sided), in years of 52 weeks:

| Haircut h | Expected live Sharpe | Years, Sharpe > 0, a 0.025 | a 0.10 | Expected lead over holding (Sharpe of difference) | Years, lead > 0, a 0.025 | a 0.10 |
|---|---:|---:|---:|---:|---:|---:|
| none (the backtest) | 1.05 | 7.3 | 4.2 | -0.10 | 19230769 | 19230769 |
| measured (c), 80% | 0.21 | 170.2 | 97.8 | -0.02 | 19230769 | 19230769 |
| Harvey-Liu ceiling (H2), 25% | 0.79 | 12.7 | 7.3 | -0.07 | 19230769 | 19230769 |
| bank-strategy median (H1), 73% | 0.28 | 97.2 | 55.8 | -0.03 | 19230769 | 19230769 |
