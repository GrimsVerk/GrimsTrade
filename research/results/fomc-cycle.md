# fomc-cycle: stock slots only in even weeks of the FOMC cycle

Card: `cards/fomc-cycle.md`. Survey and ranking: `survey-2.md`. Protocol: `protocol.md`.

Scheduled FOMC announcement days used: 256, 1994-02-04 .. 2025-12-10.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| even-gate | 1.22 (0.18) | +18.9% | 15.0% | 36.2% | 17.4 | 50% | 1.70 | 0.73 | 1.68 | 1.38 | 0.97 | +0.18 (p=0.03; +0.02..+0.33) | 4/5 |
| even-overlay | 0.96 (0.18) | +18.2% | 19.3% | 53.1% | 17.2 | 87% | 1.32 | 0.16 | 1.69 | 1.53 | 0.58 | -0.08 (p=0.90; -0.20..+0.03) | 2/5 |
| odd-gate | 0.65 (0.18) | +9.3% | 15.4% | 56.0% | 19.5 | 54% | 0.03 | -0.26 | 1.10 | 1.45 | 0.71 | -0.39 (p=1.00; -0.52..-0.29) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| even-gate | +7% | +6% | -12% | -5% | -7% | -23% | -13% |
| even-overlay | -51% | -9% | -23% | -22% | -4% | -23% | -31% |
| odd-gate | -33% | -4% | -20% | -16% | -11% | -23% | -22% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Sharpe minus the twin's from 2017-01-01 (after the published sample): `even-gate` -0.053, `even-overlay` -0.087, `odd-gate` -0.081.

## Event study (descriptive): mean daily log return in even and odd weeks, bps

Close = close-to-close (the paper's measure); open = next open to next open (what our fills earn), labelled by the session it starts on. Spread = even minus odd (Welch t).

| Asset | Period | close: n even / odd | even | odd | spread (t) | open: n even / odd | even | odd | spread (t) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 1994-2013 (first draft's sample) | 2323 / 2695 | +9.3 | -1.6 | +11.0 (+3.11) | 2323 / 2695 | +10.9 | -3.0 | +13.9 (+3.91) |
| SPY | 2014-2016 (authors' holdout) | 350 / 406 | +12.9 | -4.9 | +17.8 (+2.93) | 350 / 406 | +10.3 | -2.4 | +12.8 (+2.06) |
| SPY | 2017 to end of train (after publication) | 1039 / 1187 | +2.5 | +8.3 | -5.7 (-1.16) | 1039 / 1187 | +2.4 | +8.4 | -6.0 (-1.25) |
| QQQ | 1994-2013 (first draft's sample) | 1727 / 2000 | +10.2 | -5.8 | +16.0 (+2.49) | 1727 / 2000 | +11.5 | -7.0 | +18.5 (+2.81) |
| QQQ | 2014-2016 (authors' holdout) | 350 / 406 | +15.9 | -5.5 | +21.4 (+2.92) | 350 / 406 | +13.9 | -3.4 | +17.3 (+2.14) |
| QQQ | 2017 to end of train (after publication) | 1039 / 1187 | +6.8 | +8.4 | -1.5 (-0.25) | 1039 / 1187 | +6.6 | +8.6 | -2.1 (-0.34) |

## Out of universe

Other ETFs (gate on IWM, EFA, EEM):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| even-gate@etf | 0.67 (0.20) | +4.4% | 6.8% | 14.5% | 15.7 | 49% | +0.07 (p=0.28; -0.12..+0.25) | 2/4 |
| even-overlay@etf | 0.58 (0.20) | +7.3% | 13.7% | 25.9% | 20.4 | 81% | -0.02 (p=0.54; -0.24..+0.21) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | - | - |

Four indexes as one portfolio (gate on all four from 1994-02):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| even-gate@idx | 0.75 (0.13) | +5.3% | 7.3% | 25.7% | 30.4 | 52% | +0.03 (p=0.37; -0.11..+0.17) | 3/7 |
| even-overlay@idx | 0.71 (0.13) | +7.1% | 10.5% | 42.7% | 15.2 | 79% | -0.01 (p=0.57; -0.12..+0.09) | 2/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | - | - |

## Pass bar: `even-gate`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00164 (0.10 / 61) (difference +0.176, p = 0.0305)
- PASS: 2. Ahead of the twin in at least 4 of 5 eras (4 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (36.2% vs 36.5%)
- PASS: 4. Positive on the ETF and index sets (etf +0.066, idx +0.028)
- PASS: 5. Beats equal weight on Sharpe (1.22 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 2017-01-01 (-0.053)
- FAIL: 7. (card) SPY close-to-close spread from 2017 > 0 with t >= 2 (-5.7 bps a day, t -1.16)
- PASS: 8. (card) Beats the placebo `odd-gate` on Sharpe (1.224 vs 0.654)

**FAILS train.**

## Pass bar: `even-overlay`

- FAIL: 1. Beats twin `tsmom12` with p < 0.00164 (0.10 / 61) (difference -0.084, p = 0.8965)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (53.1% vs 36.5%)
- FAIL: 4. Positive on the ETF and index sets (etf -0.017, idx -0.011)
- PASS: 5. Beats equal weight on Sharpe (0.96 vs 0.88)
- FAIL: 6. (card) Not behind the twin from 2017-01-01 (-0.087)
- PASS: 8. (card) Beats the placebo `odd-gate` on Sharpe (0.964 vs 0.654)

**FAILS train.**
