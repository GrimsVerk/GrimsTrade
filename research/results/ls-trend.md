# ls-trend: long-short TSMOM on a wider ETF set against live trend funds

Card: `cards/ls-trend.md` (committed before any number). Descriptive replication, nothing selected, nothing after 2025-10 read. Monthly returns **above the 13-week T-bill**. Rule of Moskowitz, Ooi, Pedersen 2012: sign of the 12-month excess return, 40% / ex ante vol per asset, equal weight across the assets alive, monthly, one day later than the paper; costs 5 bps a side, borrow 1.0% a year on shorts, leverage financed at the bill. Wide = 34 ETFs (9 equity, 4 Treasury, 15 commodity, 6 currency); narrow = SPY, QQQ, GLD, TLT (`tsmom12-c00`'s assets). LS = long-short, LO = long-only (short signals to cash). L = 2010-02..2025-10, L07 = 2007-04..2025-10.

## 1. Sharpe, risk, leverage, costs

| Series | First month | Sharpe L | Sharpe L07 | Vol L07 | Worst year (L07) | Mean gross | Mean net | Turnover/yr | Costs/yr | Borrow/yr |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wide-LS | 1994-03 | 0.15 | 0.21 | 16.5% | -18.5% (2016) | 3.69 | +0.81 | 12.0 | 0.60% | 1.40% |
| wide-LO | 1994-03 | 0.24 | 0.28 | 12.7% | -14.7% (2018) | 2.39 | +2.39 | 6.6 | 0.33% | 0.00% |
| narrow-LS | 1994-03 | 0.63 | 0.60 | 21.9% | -27.5% (2018) | 2.61 | +1.34 | 8.9 | 0.44% | 0.62% |
| narrow-LO | 1994-03 | 1.03 | 0.99 | 19.0% | -20.8% (2022) | 2.25 | +2.25 | 5.2 | 0.26% | 0.00% |
| TC (trend funds) | 2007-03 | 0.19 | 0.17 | 8.4% | - | - | - | - | - | - |
| AQR TSMOM factor | 1985-01 | 0.35 | 0.37 | 13.5% | - | - | - | - | - | - |
| RYMFX | 2007-03 | -0.05 | -0.02 | 8.9% | - | - | - | - | - | - |
| AQMIX | 2010-02 | 0.29 | 0.29 | 10.0% | - | - | - | - | - | - |
| tsmom12 | 1994-02 | 1.11 | 1.02 | 22.5% | - | - | - | - | - | - |
| tsmom12-c00 | 1994-02 | 1.02 | 0.89 | 8.2% | - | - | - | - | - | - |
| SPY | 1993-02 | 0.92 | 0.65 | 15.6% | - | - | - | - | - | - |

## 2. Correlation of monthly excess returns in L (n in brackets; funds need 36)

| Cell | TC (trend funds) | AQR TSMOM factor | SPY | tsmom12 | tsmom12-c00 | RYMFX | AQMIX | ASFYX | WTMF | PQTIX | ABYIX | DBMF | KMLM | CTA | RYMFX in L07 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wide-LS | 0.61 (189) | 0.81 (189) | -0.17 (189) | 0.08 (189) | 0.08 (189) | 0.50 (189) | 0.64 (189) | 0.56 (182) | 0.31 (177) | 0.50 (141) | 0.59 (135) | 0.50 (77) | 0.60 (58) | 0.30 (43) | 0.51 (223) |
| wide-LO | 0.35 (189) | 0.38 (189) | 0.46 (189) | 0.31 (189) | 0.56 (189) | 0.31 (189) | 0.27 (189) | 0.38 (182) | 0.36 (177) | 0.16 (141) | 0.23 (135) | 0.17 (77) | 0.10 (58) | -0.33 (43) | 0.31 (223) |
| narrow-LS | 0.39 (189) | 0.39 (189) | 0.38 (189) | 0.37 (189) | 0.72 (189) | 0.44 (189) | 0.34 (189) | 0.43 (182) | 0.17 (177) | 0.21 (141) | 0.38 (135) | 0.42 (77) | 0.08 (58) | 0.08 (43) | 0.41 (223) |
| narrow-LO | 0.26 (189) | 0.27 (189) | 0.60 (189) | 0.44 (189) | 0.88 (189) | 0.35 (189) | 0.16 (189) | 0.33 (182) | 0.23 (177) | 0.09 (141) | 0.23 (135) | 0.10 (77) | -0.35 (58) | -0.41 (43) | 0.31 (223) |

wide-LS with wide-LO in L: 0.53 (189 months).

narrow-LS with narrow-LO in L: 0.85 (189 months).

wide-LS with narrow-LS in L: 0.42 (189 months).

## 3. Crash windows (compounded monthly excess return)

Raw, and at 10% volatility (x 10% / the series' own monthly vol in L07, or over its own life to 2025-10 if shorter; a display scaling, ex post).

| Series | Vol used | 2008 | 2020-02..03 | 2022 | 2008 at 10% vol | 2020-02..03 at 10% vol | 2022 at 10% vol |
|---|---:|---:|---:|---:|---:|---:|---:|
| wide-LS | 16.5% | +34.9% | +24.6% | +12.8% | +21.2% | +15.0% | +7.8% |
| wide-LO | 12.7% | +1.1% | -4.7% | -2.8% | +0.8% | -3.7% | -2.2% |
| narrow-LS | 21.9% | +23.7% | -10.9% | -4.1% | +10.8% | -5.0% | -1.9% |
| narrow-LO | 19.0% | +7.2% | -10.9% | -20.8% | +3.8% | -5.7% | -10.9% |
| TC (trend funds) | 8.4% | +7.1% | +3.6% | +17.6% | +8.4% | +4.3% | +21.0% |
| AQR TSMOM factor | 13.5% | +24.6% | +10.5% | +24.7% | +18.3% | +7.8% | +18.4% |
| RYMFX | 8.9% | +7.1% | -0.5% | +12.5% | +8.0% | -0.6% | +14.1% |
| AQMIX | 10.0% | - | +5.0% | +32.8% | - | +5.0% | +32.8% |
| tsmom12 | 22.5% | -1.6% | -14.1% | -12.9% | -0.7% | -6.2% | -5.7% |
| tsmom12-c00 | 8.2% | -1.6% | -9.0% | -11.1% | -1.9% | -10.9% | -13.5% |
| SPY | 15.6% | -37.7% | -19.5% | -19.8% | -24.2% | -12.6% | -12.7% |
| AQR commodities | 16.2% | +9.4% | +20.5% | +18.6% | +5.8% | +12.7% | +11.5% |
| AQR equity | 26.3% | +43.6% | -46.2% | -38.7% | +16.6% | -17.6% | -14.7% |
| AQR bonds | 28.6% | +32.6% | +23.2% | +129.8% | +11.4% | +8.1% | +45.5% |
| AQR currencies | 18.5% | +23.4% | +27.1% | +8.9% | +12.7% | +14.6% | +4.8% |
| ASFYX | 12.4% | - | +6.8% | +33.0% | - | +5.5% | +26.6% |
| PQTIX | 9.7% | - | +8.7% | +9.4% | - | +8.9% | +9.7% |
| ABYIX | 8.6% | - | +5.3% | +14.8% | - | +6.1% | +17.1% |
| DBMF | 11.4% | - | -1.0% | +19.2% | - | -0.9% | +16.9% |

## 4. Where the crash gains came from (additive daily contributions, % of capital, raw scale; costs not included in the legs)

### wide-LS

| Window | Class | Long legs | Short legs | Total | Share of window total |
|---|---|---:|---:|---:|---:|
| 2008 | equity | -4.6% | +22.2% | +17.6% | 51% |
| 2008 | bonds | +10.9% | +0.0% | +10.9% | 31% |
| 2008 | commodities | -3.6% | +4.2% | +0.5% | 2% |
| 2008 | currencies | -0.2% | +5.8% | +5.6% | 16% |
| 2008 | all | +2.4% | +32.2% | +34.6% | 100% |
| 2008 | **short legs' share of the gain** | | | | **93%** (long 7%) |
| 2020-02..03 | equity | -8.2% | +7.7% | -0.5% | -2% |
| 2020-02..03 | bonds | +6.0% | +0.0% | +6.0% | 25% |
| 2020-02..03 | commodities | -2.0% | +16.4% | +14.4% | 61% |
| 2020-02..03 | currencies | -0.1% | +3.8% | +3.7% | 16% |
| 2020-02..03 | all | -4.3% | +28.0% | +23.7% | 100% |
| 2020-02..03 | **short legs' share of the gain** | | | | **118%** (long -18%) |
| 2022 | equity | -6.5% | +1.0% | -5.5% | -39% |
| 2022 | bonds | +0.0% | +11.0% | +11.0% | 77% |
| 2022 | commodities | +6.0% | -2.4% | +3.6% | 26% |
| 2022 | currencies | -1.6% | +6.8% | +5.1% | 36% |
| 2022 | all | -2.2% | +16.4% | +14.3% | 100% |
| 2022 | **short legs' share of the gain** | | | | **115%** (long -15%) |

### narrow-LS

| Window | Class | Long legs | Short legs | Total | Share of window total |
|---|---|---:|---:|---:|---:|
| 2008 | equity | -10.7% | +21.8% | +11.1% | 39% |
| 2008 | bonds | +18.4% | +0.0% | +18.4% | 64% |
| 2008 | commodities | +1.1% | -1.8% | -0.7% | -2% |
| 2008 | currencies | +0.0% | +0.0% | +0.0% | 0% |
| 2008 | all | +8.8% | +20.0% | +28.8% | 100% |
| 2008 | **short legs' share of the gain** | | | | **70%** (long 30%) |
| 2020-02..03 | equity | -17.0% | +0.0% | -17.0% | - |
| 2020-02..03 | bonds | +10.4% | +0.0% | +10.4% | - |
| 2020-02..03 | commodities | -0.2% | +0.0% | -0.2% | - |
| 2020-02..03 | currencies | +0.0% | +0.0% | +0.0% | - |
| 2020-02..03 | all | -6.8% | +0.0% | -6.8% | - |
| 2022 | equity | -16.9% | +7.3% | -9.6% | -1057% |
| 2022 | bonds | +0.0% | +20.3% | +20.3% | 2228% |
| 2022 | commodities | -4.9% | -4.9% | -9.8% | -1071% |
| 2022 | currencies | +0.0% | +0.0% | +0.0% | 0% |
| 2022 | all | -21.8% | +22.7% | +0.9% | 100% |
| 2022 | **short legs' share of the gain** | | | | **2493%** (long -2393%) |

### AQR TSMOM factor by asset class (sum of monthly returns in the window)

| Window | equity | bonds | commodities | currencies | all |
|---|---:|---:|---:|---:|---:|
| 2008 | +43.7% | +31.9% | +11.9% | +24.2% | +23.9% |
| 2020-02..03 | -53.3% | +22.1% | +20.3% | +25.7% | +10.4% |
| 2022 | -45.4% | +93.3% | +18.7% | +10.0% | +23.7% |

(The factor's class columns are each scaled on their own, so they do not add to `all`; read the signs and the order.)

## 5. The 2 x 2: short effect and universe effect

Crash returns at 10% vol; correlation with TC in L.

| Effect | 2008 | 2020-02..03 | 2022 | Corr. with TC |
|---|---:|---:|---:|---:|
| short effect, wide (wide-LS - wide-LO) | +20.4% | +18.6% | +9.9% | +0.26 |
| short effect, narrow (narrow-LS - narrow-LO) | +7.0% | +0.7% | +9.1% | +0.13 |
| universe effect, LS (wide-LS - narrow-LS) | +10.4% | +19.9% | +9.6% | +0.21 |
| universe effect, LO (wide-LO - narrow-LO) | -3.0% | +2.0% | +8.7% | +0.08 |

## 6. Card's reading rule

- wide-LS: 2008 +34.9%, 2022 +12.8%, corr. with TC 0.61 -> reproduces the funds' crash behaviour.
- wide-LO: 2008 +1.1%, 2022 -2.8%, corr. with TC 0.35 -> does not reproduce the funds' crash behaviour.
- narrow-LS: 2008 +23.7%, 2022 -4.1%, corr. with TC 0.39 -> does not reproduce the funds' crash behaviour.
- narrow-LO: 2008 +7.2%, 2022 -20.8%, corr. with TC 0.26 -> does not reproduce the funds' crash behaviour.
