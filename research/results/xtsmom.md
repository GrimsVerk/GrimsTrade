# xtsmom: stock slots only while bonds also trend up

Card: `cards/xtsmom.md`. Survey: `survey-2.md` (S5), `survey-3.md`. Protocol: `protocol.md`. No-look-ahead check against `gym.backtest` on 1999-10-01, 2008-10-10, 2018-12-21, 2023-06-02: passed.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| xtsmom | 1.05 (0.18) | +16.7% | 15.9% | 35.3% | 3.5 | 62% | 1.19 | 0.36 | 1.50 | 1.42 | 0.86 | +0.00 (p=0.49; -0.09..+0.10) | 1/5 |
| xtsmom-b6 | 1.02 (0.18) | +16.3% | 16.0% | 34.5% | 3.9 | 58% | 1.26 | 0.21 | 1.46 | 1.42 | 1.01 | -0.03 (p=0.67; -0.11..+0.06) | 2/5 |
| xtsmom-full | 1.01 (0.18) | +16.1% | 16.1% | 39.0% | 3.1 | 53% | 1.19 | 0.28 | 1.37 | 1.39 | 0.92 | -0.04 (p=0.76; -0.14..+0.06) | 2/5 |
| xtsmom-tlt | 1.04 (0.18) | +17.3% | 16.7% | 34.5% | 3.6 | 68% | 1.34 | 0.24 | 1.52 | 1.43 | 0.90 | -0.01 (p=0.59; -0.05..+0.04) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| xtsmom | -17% | -4% | -22% | -8% | -10% | -22% | -16% |
| xtsmom-b6 | -20% | -4% | -20% | -10% | -6% | -21% | -16% |
| xtsmom-full | -17% | -6% | -22% | -7% | -13% | -21% | -15% |
| xtsmom-tlt | -28% | -4% | -22% | -9% | -9% | -21% | -16% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## In the paper's years and after: Sharpe minus the twin's, by window

| Run | 1962-1979 (before the sample) | 1980-1993 (in sample) | 1994-2015 (in sample) | 2016 (maybe in sample) | 2017 to end of train (after) |
|---|---:|---:|---:|---:|---:|
| xtsmom (six) | - | - | +0.047 | +0.046 | -0.059 |
| xtsmom-b6 (six) | - | - | -0.028 | -0.095 | -0.013 |
| xtsmom-full (six) | - | - | -0.034 | +0.252 | -0.062 |
| xtsmom-tlt (six, robustness) | - | - | +0.002 | +0.291 | -0.038 |
| xtsmom (ETFs) | - | - | +0.083 | -0.153 | +0.038 |
| xtsmom-b6 (ETFs) | - | - | -0.110 | -0.172 | -0.028 |
| xtsmom-full (ETFs) | - | - | -0.016 | -0.033 | +0.008 |
| xtsmom (indexes) | +0.043 | +0.594 | +0.083 | -0.515 | -0.179 |
| xtsmom-b6 (indexes) | +0.101 | +0.459 | -0.044 | -0.589 | +0.055 |

(`-`: the run has no days, or fewer than 200, in that window.)

## Event study (descriptive): own trend up, split by the bond signal, bps a day

Mean daily log return on days the asset's own 365-day return is positive, by the 10-year bond's trailing return as of the day before (up / down); spread = up minus down (Welch t). SPY: next open to next open (what a decision after day d holds). S&P 500 index: close to close (its early opens are unreliable).

| Asset | Window | n up / down | up | down | spread (t) |
|---|---|---:|---:|---:|---:|
| **bond look-back 12m** | | | | | |
| GSPC (close) | 1962-1979 (before the sample) | 2464 / 278 | +2.0 | -1.3 | +3.3 (+0.73) |
| GSPC (close) | 1980-1993 (in sample) | 2202 / 354 | +6.6 | -14.8 | +21.5 (+2.21) |
| SPY (open) | 1994-2015 (in sample) | 3386 / 1027 | +4.8 | +5.0 | -0.2 (-0.06) |
| SPY (open) | 2016 (maybe in sample) | 171 / 14 | +2.8 | +2.0 | +0.8 (+0.07) |
| SPY (open) | 2017 to end of train (after) | 900 / 1008 | +5.0 | +4.5 | +0.4 (+0.10) |
| **bond look-back 6m** | | | | | |
| GSPC (close) | 1962-1979 (before the sample) | 2112 / 630 | +2.2 | -0.3 | +2.5 (+0.85) |
| GSPC (close) | 1980-1993 (in sample) | 2009 / 547 | +5.6 | -3.5 | +9.1 (+1.42) |
| SPY (open) | 1994-2015 (in sample) | 2803 / 1610 | +5.2 | +4.3 | +0.9 (+0.31) |
| SPY (open) | 2016 (maybe in sample) | 149 / 36 | +0.5 | +12.1 | -11.6 (-1.31) |
| SPY (open) | 2017 to end of train (after) | 1081 / 827 | +6.8 | +2.0 | +4.9 (+1.06) |

## Pass bar: `xtsmom`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00164 (0.10 / 61) (difference +0.002, p = 0.4925)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (1 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (35.3% vs 36.5%)
- PASS: 4. Positive on the ETF and index sets (etf +0.062, idx +0.137)
- PASS: 5. Beats equal weight on Sharpe (1.05 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 2017-01-01 (-0.059)
- FAIL: 7. (card) SPY up-trend days 2017 to end of train (after): bond-up minus bond-down > 0, t >= 2 (+0.4 bps a day, t +0.10)

**FAILS train.**

## Pass bar: `xtsmom-b6`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00164 (0.10 / 61) (difference -0.026, p = 0.6735)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (34.5% vs 36.5%)
- FAIL: 4. Positive on the ETF and index sets (etf -0.085, idx +0.109)
- PASS: 5. Beats equal weight on Sharpe (1.02 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 2017-01-01 (-0.013)
- FAIL: 7. (card) SPY up-trend days 2017 to end of train (after): bond-up minus bond-down > 0, t >= 2 (+4.9 bps a day, t +1.06)

**FAILS train.**

## Pass bar: `xtsmom-full`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00164 (0.10 / 61) (difference -0.041, p = 0.7645)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (39.0% vs 36.5%)
- FAIL: 4. Positive on the ETF and index sets (etf -0.008, idx +0.137)
- PASS: 5. Beats equal weight on Sharpe (1.01 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 2017-01-01 (-0.062)

**FAILS train.**
