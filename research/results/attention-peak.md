# attention-peak: leave a coin once its attention epidemic has peaked

Card: `cards/attention-peak.md`. Protocol: `protocol.md`.

Page-view series per coin (first day): BTC 2015-07-01, ETH 2015-07-01, LTC 2015-07-01, XRP 2015-07-01, BCH 2017-07-28, ETC 2016-07-25, XLM 2015-07-01, DASH 2015-07-01.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| peak | 1.02 (0.18) | +16.5% | 16.2% | 37.6% | 2.9 | 75% | 1.34 | 0.19 | 1.55 | 1.37 | 0.88 | -0.03 (p=0.74; -0.09..+0.03) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| peak | -28% | -4% | -22% | -14% | -6% | -17% | -20% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## Out spells

| Coin | First Friday out | Last Friday out | Fridays | Twin held it (Fridays) | Coin return, first out Friday to the Friday after the last (log) |
|---|---|---|---:|---:|---:|
| BTC | 2017-05-26 | 2017-06-16 | 4 | 4 | +16.9% |
| BTC | 2017-12-15 | 2018-01-19 | 6 | 6 | -47.0% |
| BTC | 2021-01-15 | 2021-02-05 | 4 | 4 | +25.5% |
| BTC | 2021-02-19 | 2021-03-19 | 5 | 5 | -1.6% |
| BTC | 2021-05-21 | 2021-06-11 | 4 | 4 | -4.1% |
| ETH | 2017-06-02 | 2017-06-09 | 2 | 2 | +46.7% |
| ETH | 2017-06-23 | 2017-09-22 | 14 | 14 | -11.4% |
| ETH | 2017-12-22 | 2017-12-22 | 1 | 1 | +9.3% |
| ETH | 2020-01-03 | 2020-01-31 | 5 | 3 | +50.9% |
| ETH | 2021-01-15 | 2021-04-30 | 16 | 16 | +109.3% |
| ETH | 2021-05-21 | 2021-06-11 | 4 | 4 | -8.6% |

## Out of universe: the 6 other coins

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| peak@coin | 0.33 (0.35) | +2.4% | 57.2% | 86.9% | 6.8 | 45% | -0.21 (p=0.85; -0.52..+0.11) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | - | - |

Out spells per other coin: LTC 10, XRP 13, BCH 5, ETC 5, XLM 10, DASH 5.

## Pass bar (only variant `peak`)

- FAIL: 1. `peak` beats twin `tsmom12` with p < 0.0022 (0.10 / 46) (difference -0.027, p = 0.7450)
- FAIL: 2. Ahead of the twin in both eras from 2017-21 (2 counted) (0 of 2)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (37.6% vs 36.5%)
- FAIL: 4. Positive, and positive on the one applicable out-of-universe set (coin set -0.210 (p = 0.85))
- PASS: 5. Beats equal weight on Sharpe (1.02 vs 0.88)

**FAILS train.**
