# hmm-regime: a two-state hidden Markov model as a risk switch

Card: `cards/hmm-regime.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hard | 0.89 (0.18) | +14.6% | 16.9% | 57.3% | 8.8 | 73% | 1.36 | 0.05 | 1.62 | 1.42 | 0.58 | +0.14 (p=0.03; +0.02..+0.27) | 4/5 |
| soft | 0.88 (0.18) | +14.1% | 16.5% | 59.2% | 8.2 | 73% | 1.38 | 0.05 | 1.62 | 1.37 | 0.58 | +0.14 (p=0.03; +0.02..+0.26) | 4/5 |
| vol-calm | 0.74 (0.18) | +11.1% | 15.8% | 54.8% | 3.4 | 61% | 1.22 | 0.09 | 1.46 | 1.17 | 0.39 | - | - |
| sma200 | 1.01 (0.18) | +15.9% | 15.8% | 44.4% | 4.3 | 70% | 1.14 | 0.14 | 1.58 | 1.53 | 0.75 | +0.27 (p=0.04; +0.02..+0.51) | 4/5 |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | +0.14 (p=0.07; -0.02..+0.28) | 4/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| hard | -57% | -3% | -15% | -28% | -10% | -39% | -35% |
| soft | -59% | -2% | -15% | -24% | -11% | -39% | -32% |
| vol-calm | -55% | -4% | -17% | -36% | -17% | -32% | -43% |
| sma200 | -33% | +2% | -14% | -12% | -4% | -23% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: hard +13.6%, soft +13.2%, vol-calm +10.5%, sma200 +14.7%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hard@etf | 0.46 (0.20) | +4.9% | 11.7% | 36.6% | 3.9 | 87% | 0.49 | 0.30 | 0.77 | 0.45 | +0.16 (p=0.04; +0.01..+0.30) | 4/4 |
| vol-calm@etf | 0.31 (0.20) | +2.6% | 9.9% | 36.6% | 1.9 | 69% | 0.48 | 0.11 | 0.20 | 0.24 | - | - |
| sma200@etf | 0.53 (0.20) | +4.3% | 8.6% | 16.8% | 3.9 | 65% | 0.67 | 0.36 | 0.66 | 0.31 | +0.22 (p=0.09; -0.03..+0.50) | 4/4 |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | +0.18 (p=0.08; -0.03..+0.38) | 3/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs vol-calm@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hard@coin | 0.63 (0.34) | +19.1% | 89.3% | 91.6% | 9.9 | 93% | 0.88 | 0.20 | -0.08 (p=0.82; -0.24..+0.06) | 1/2 |
| vol-calm@coin | 0.72 (0.34) | +29.6% | 83.5% | 91.6% | 4.9 | 85% | 0.81 | 0.59 | - | - |
| sma200@coin | 0.50 (0.34) | +11.3% | 73.1% | 89.8% | 6.1 | 46% | 0.59 | 0.38 | -0.22 (p=0.85; -0.57..+0.13) | 0/2 |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.01 (p=0.46; -0.15..+0.16) | 1/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs vol-calm@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hard@GSPC | 0.33 (0.18) | +2.6% | 8.8% | 45.9% | 8.9 | 65% | 0.10 | 0.63 | +0.09 (p=0.30; -0.19..+0.37) | 1/2 |
| vol-calm@GSPC | 0.24 (0.18) | +1.3% | 5.9% | 27.4% | 2.2 | 35% | 0.16 | 0.38 | - | - |
| sma200@GSPC | 0.74 (0.18) | +6.8% | 9.5% | 20.5% | 2.7 | 66% | 0.58 | 0.91 | +0.50 (p=0.01; +0.15..+0.85) | 2/2 |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.25 (p=0.12; -0.11..+0.61) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hard@N225 | 0.37 (0.13) | +3.8% | 12.0% | 44.7% | 12.0 | 64% | 0.66 | 0.67 | -0.01 | 0.10 | 0.06 | -0.01 | 0.31 | -0.04 (p=0.62; -0.25..+0.16) | 2/7 |
| vol-calm@N225 | 0.41 (0.13) | +3.1% | 8.3% | 36.6% | 1.9 | 39% | 0.38 | 0.91 | -0.65 | 0.46 | 0.06 | 0.39 | 0.56 | - | - |
| sma200@N225 | 0.41 (0.13) | +4.5% | 12.9% | 47.5% | 3.5 | 63% | 0.75 | 0.74 | 0.15 | 0.13 | 0.20 | -0.13 | 0.58 | -0.01 (p=0.51; -0.22..+0.20) | 4/7 |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.02 (p=0.54; -0.25..+0.20) | 5/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hard@FTSE | 0.31 (0.16) | +3.2% | 13.0% | 55.2% | 4.3 | 86% | 0.83 | 0.98 | -0.15 | -0.21 | -0.27 | 0.39 | +0.08 (p=0.26; -0.12..+0.26) | 4/6 |
| vol-calm@FTSE | 0.23 (0.16) | +1.8% | 9.6% | 40.0% | 2.2 | 56% | 0.45 | 0.55 | 0.36 | -0.38 | -0.11 | 0.38 | - | - |
| sma200@FTSE | 0.24 (0.16) | +2.0% | 10.9% | 43.0% | 4.6 | 68% | 0.50 | 0.71 | 0.21 | -0.24 | -0.15 | 0.04 | +0.01 (p=0.50; -0.19..+0.20) | 3/6 |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.15 (p=0.14; -0.07..+0.37) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| hard@GDAXI | 0.43 (0.17) | +5.4% | 14.7% | 48.5% | 6.2 | 75% | 0.73 | 1.38 | -0.03 | 0.26 | 0.16 | 0.33 | -0.09 (p=0.79; -0.29..+0.10) | 2/6 |
| vol-calm@GDAXI | 0.52 (0.17) | +5.6% | 11.9% | 33.0% | 1.6 | 57% | 0.65 | 0.65 | 0.46 | 0.56 | 0.29 | 0.68 | - | - |
| sma200@GDAXI | 0.55 (0.17) | +7.1% | 14.4% | 40.9% | 2.6 | 70% | 0.71 | 0.66 | 0.62 | 0.31 | 0.09 | 1.00 | +0.03 (p=0.43; -0.21..+0.26) | 4/6 |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | -0.06 (p=0.65; -0.30..+0.19) | 3/6 |

## Pass bar (primary variant `hard`)

- PASS: 1. Sharpe beats twin `vol-calm` with p < 0.10 (difference +0.14, p = 0.03)
- PASS: 2. Ahead of the twin in at least 4 of 5 eras (4 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (57.3% vs 54.8%)
- PASS: 4. Same sign out of universe in at least 2 of 3 sets (etf +0.16, coin -0.08, idx +0.01)
- PASS: 5. Beats equal weight on Sharpe (0.89 vs 0.88)

- FAIL: 6. (card's extra bar) Not behind twin B `sma200` on Sharpe on the six assets (0.89 vs 1.01)

**FAILS train** (passes the default bar against the volatility switch, fails the card's stricter bar).

## Verdict (2026-11-12)

Dead by the card's own bar, and the default bar flatters it. The hidden Markov model is a better
regime detector than a volatility threshold (+0.14 Sharpe, p = 0.03, ahead in 4 of 5 eras, also
ahead on the other ETFs). But that twin is worse than doing nothing (0.74 against 0.88 for equal
weight), so beating it proves little. Against what matters:

- Equal weight: 0.89 against 0.88. Nothing, for seven times the trading (8.8 turns a year).
- The 200-day average: 0.89 against 1.01, and a 57% maximum drawdown against 44%. The model sat
  through the dot-com bust (-57%): a slow grind down at moderate volatility looks "calm" to it.
- Out of universe it loses to the 200-day average on the old S&P 500 index (0.33 against 0.74)
  and the DAX, ties on the Nikkei, and wins only on the FTSE and the coins (where both lose to
  simply holding).

This answers the question survey part 4 left open: the published regime-switching results beat
buy-and-hold, but nobody compared them with a moving average. On our data the moving average is
better and simpler. Regimes defined by volatility alone miss the point; what protects is trend.
No held-out look was spent.
