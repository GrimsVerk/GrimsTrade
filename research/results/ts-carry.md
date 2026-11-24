# ts-carry: stock and bond trend slots only while carry is positive

Card: `cards/ts-carry.md`. Survey: `survey-4.md` (pick A). Protocol: `protocol.md`. No-look-ahead check against `gym.backtest` on 1999-10-01, 2008-10-10, 2018-12-21, 2023-06-02: passed.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| carry | 0.97 (0.18) | +13.2% | 13.8% | 41.4% | 2.6 | 41% | - | 0.66 | 1.55 | 1.43 | 0.78 | -0.08 (p=0.78; -0.24..+0.09) | 1/4 |
| carry-mean | 1.02 (0.18) | +14.7% | 14.5% | 39.8% | 2.2 | 43% | 0.61 | 0.65 | 1.58 | 1.47 | 0.75 | -0.03 (p=0.62; -0.19..+0.15) | 2/5 |
| carry-bond | 1.05 (0.18) | +17.8% | 17.1% | 38.8% | 2.8 | 75% | 1.34 | 0.19 | 1.55 | 1.47 | 0.94 | -0.00 (p=0.56; -0.01..+0.01) | 1/5 |
| carry-equity | 0.97 (0.18) | +13.2% | 13.8% | 39.4% | 2.6 | 42% | - | 0.66 | 1.55 | 1.45 | 0.73 | -0.08 (p=0.78; -0.24..+0.09) | 1/4 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| carry | +0% | +6% | -21% | -12% | -6% | -23% | -18% |
| carry-mean | +15% | -4% | -22% | -13% | -6% | -21% | -19% |
| carry-bond | -28% | -4% | -24% | -13% | -6% | -22% | -20% |
| carry-equity | +0% | +6% | -19% | -12% | -6% | -23% | -18% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Share of `tsmom12`'s held days that each run holds in cash instead:

- `carry`: SPY 54%, QQQ 53%, TLT 9%
- `carry-mean`: SPY 42%, QQQ 32%, TLT 65%
- `carry-bond`: SPY 0%, QQQ 0%, TLT 9%
- `carry-equity`: SPY 54%, QQQ 53%, TLT 0%

Sharpe above T-bills with T-bill interest on cash (`cash_interest.rescored`; no row):

- `carry`: 0.94 (gym: 0.97)
- `carry-mean`: 0.99 (gym: 1.02)
- `carry-bond`: 0.93 (gym: 1.05)
- `carry-equity`: 0.93 (gym: 0.97)
- `tsmom12`: 0.93 (gym: 1.05)
- `equal-weight`: 0.77 (gym: 0.88)

## Out of universe

Other ETFs:

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| carry@etf | 0.48 (0.21) | +3.1% | 6.7% | 16.3% | 2.6 | 47% | 0.70 | 0.44 | 0.44 | 0.40 | -0.12 (p=0.86; -0.30..+0.07) | 1/4 |
| carry-mean@etf | 0.48 (0.20) | +3.2% | 7.0% | 13.9% | 2.7 | 35% | 0.54 | 0.51 | 0.44 | 0.39 | -0.12 (p=0.88; -0.29..+0.05) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |

S&P 500 index alone, 1962-1993 (Shiller dividends, 3-month lag):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| carry@GSPC | -0.10 (0.18) | -0.1% | 1.2% | 9.9% | 0.3 | 2% | -0.55 (p=0.99; -0.96..-0.15) | 0/2 |
| carry-mean@GSPC | 0.46 (0.19) | +2.3% | 5.2% | 15.8% | 1.8 | 15% | +0.02 (p=0.46; -0.31..+0.33) | 1/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | - | - |

## Before, in and after the paper's sample: Sharpe minus the twin's

| Run | 1994 - 2012-09 (in sample) | 2012-10 to end of train (after) |
|---|---:|---:|
| carry | -0.031 | -0.052 |
| carry-mean | -0.003 | -0.020 |
| carry-bond | -0.001 | -0.003 |
| carry-equity | -0.030 | -0.051 |

## Event study (descriptive): own trend up, split by carry, bps a day

Mean daily log return on days the asset's own 365-day return is positive, by carry above / not above the cut-off as of that day; spread = above minus not above (Welch t). ETFs: next open to next open (what a decision after day d holds). S&P 500 index: close to close.

| Asset | Window | n above / not | above | not | spread (t) |
|---|---|---:|---:|---:|---:|
| **cut-off 0** | | | | | |
| SPY (open) | 1994 - 2012-09 (in sample) | 1049 / 2565 | +4.4 | +5.1 | -0.7 (-0.19) |
| SPY (open) | 2012-10 to end of train (after) | 1953 / 939 | +4.1 | +5.3 | -1.2 (-0.32) |
| TLT (open) | 1994 - 2012-09 (in sample) | 1839 / 159 | +3.0 | +2.1 | +1.0 (+0.23) |
| TLT (open) | 2012-10 to end of train (after) | 1400 / 189 | -0.6 | -3.9 | +3.2 (+0.43) |
| GSPC (close) | 1962-1987 (before the sample) | 141 / 4274 | -4.7 | +2.3 | -7.0 (-1.66) |
| GSPC (close) | 1988-1993 (in sample) | 33 / 933 | +8.5 | +4.0 | +4.5 (+0.37) |
| **cut-off running mean** | | | | | |
| SPY (open) | 1994 - 2012-09 (in sample) | 1503 / 2111 | +3.9 | +5.7 | -1.7 (-0.51) |
| SPY (open) | 2012-10 to end of train (after) | 2240 / 652 | +3.7 | +7.2 | -3.5 (-0.88) |
| TLT (open) | 1994 - 2012-09 (in sample) | 971 / 1027 | +3.9 | +2.0 | +1.9 (+0.47) |
| TLT (open) | 2012-10 to end of train (after) | 258 / 1331 | +8.2 | -2.8 | +11.0 (+1.93) |
| GSPC (close) | 1962-1987 (before the sample) | 671 / 3744 | +6.2 | +1.3 | +4.9 (+1.39) |
| GSPC (close) | 1988-1993 (in sample) | 497 / 469 | +3.1 | +5.2 | -2.1 (-0.40) |

## Pass bar: `carry`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00154 (0.10 / 65) (difference -0.078, p = 0.7800)
- FAIL: 2. Ahead of the twin in at least 4 of 4 eras (1 of 4)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (41.4% vs 36.5%)
- FAIL: 4. Positive on the ETF set and the S&P 500 index (etf -0.117, S&P 500 -0.546)
- PASS: 5. Beats equal weight on Sharpe (0.97 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 2012-10-01 (-0.052)
- FAIL: 7. (card) After 2012-10: SPY and TLT carry spreads > 0, one with t >= 2 (SPY -1.2 bps (t -0.32), TLT +3.2 bps (t +0.43))

**FAILS train.**

## Pass bar: `carry-mean`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00154 (0.10 / 65) (difference -0.026, p = 0.6205)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (39.8% vs 36.5%)
- FAIL: 4. Positive on the ETF set and the S&P 500 index (etf -0.120, S&P 500 +0.016)
- PASS: 5. Beats equal weight on Sharpe (1.02 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 2012-10-01 (-0.020)
- FAIL: 7. (card) After 2012-10: SPY and TLT carry spreads > 0, one with t >= 2 (SPY -3.5 bps (t -0.88), TLT +11.0 bps (t +1.93))

**FAILS train.**
