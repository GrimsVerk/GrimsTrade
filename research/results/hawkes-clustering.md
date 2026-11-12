# hawkes-clustering: self-exciting crash days

Card: `cards/hawkes-clustering.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| down2 | 0.87 (0.18) | +16.4% | 19.7% | 69.3% | 9.1 | 84% | 1.37 | 0.02 | 1.40 | 1.64 | 0.66 | +0.12 (p=0.09; -0.03..+0.28) | 3/5 |
| vol-calm | 0.74 (0.18) | +11.1% | 15.8% | 54.8% | 3.4 | 61% | 1.22 | 0.09 | 1.46 | 1.17 | 0.39 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | +0.14 (p=0.07; -0.02..+0.28) | 4/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| down2 | -68% | -2% | -13% | -29% | -14% | -39% | -34% |
| vol-calm | -55% | -4% | -17% | -36% | -17% | -32% | -43% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: down2 +15.2%, vol-calm +10.5%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| down2@etf | 0.49 (0.20) | +5.3% | 12.0% | 36.6% | 6.2 | 79% | 0.54 | 0.28 | 1.05 | 0.28 | +0.18 (p=0.05; -0.00..+0.37) | 4/4 |
| vol-calm@etf | 0.31 (0.20) | +2.6% | 9.9% | 36.6% | 1.9 | 69% | 0.48 | 0.11 | 0.20 | 0.24 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | +0.18 (p=0.08; -0.03..+0.38) | 3/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs vol-calm@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| down2@coin | 0.64 (0.34) | +20.5% | 88.2% | 91.6% | 9.5 | 90% | 0.96 | 0.06 | -0.08 (p=0.78; -0.26..+0.09) | 1/2 |
| vol-calm@coin | 0.72 (0.34) | +29.6% | 83.5% | 91.6% | 4.9 | 85% | 0.81 | 0.59 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.01 (p=0.46; -0.15..+0.16) | 1/2 |

## Out of universe: GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs vol-calm@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| down2@GSPC | 0.67 (0.18) | +7.2% | 11.4% | 40.8% | 6.4 | 82% | 0.38 | 0.99 | +0.42 (p=0.02; +0.08..+0.76) | 2/2 |
| vol-calm@GSPC | 0.24 (0.18) | +1.3% | 5.9% | 27.4% | 2.2 | 35% | 0.16 | 0.38 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.25 (p=0.12; -0.11..+0.61) | 2/2 |

## Out of universe: N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| down2@N225 | 0.40 (0.13) | +5.0% | 15.3% | 73.8% | 6.7 | 77% | 0.76 | 0.60 | 0.30 | -0.09 | 0.25 | 0.52 | 0.55 | -0.02 (p=0.54; -0.25..+0.21) | 4/7 |
| vol-calm@N225 | 0.41 (0.13) | +3.1% | 8.3% | 36.6% | 1.9 | 39% | 0.38 | 0.91 | -0.65 | 0.46 | 0.06 | 0.39 | 0.56 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.02 (p=0.54; -0.25..+0.20) | 5/7 |

## Out of universe: FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| down2@FTSE | 0.27 (0.16) | +2.8% | 13.3% | 53.0% | 6.7 | 79% | 0.84 | 0.82 | -0.17 | -0.05 | 0.10 | -0.02 | +0.04 (p=0.38; -0.18..+0.24) | 4/6 |
| vol-calm@FTSE | 0.23 (0.16) | +1.8% | 9.6% | 40.0% | 2.2 | 56% | 0.45 | 0.55 | 0.36 | -0.38 | -0.11 | 0.38 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.15 (p=0.14; -0.07..+0.37) | 5/6 |

## Out of universe: GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-calm@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| down2@GDAXI | 0.25 (0.17) | +2.8% | 16.4% | 59.8% | 6.4 | 72% | 0.50 | 0.93 | 0.06 | 0.09 | 0.18 | -0.12 | -0.27 (p=0.97; -0.54..-0.03) | 1/6 |
| vol-calm@GDAXI | 0.52 (0.17) | +5.6% | 11.9% | 33.0% | 1.6 | 57% | 0.65 | 0.65 | 0.46 | 0.56 | 0.29 | 0.68 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | -0.06 (p=0.65; -0.30..+0.19) | 3/6 |

## Pass bar (primary variant `down2`)

- PASS: 1. Sharpe beats twin `vol-calm` with p < 0.10 (difference +0.12, p = 0.09)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (3 of 5)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (69.3% vs 54.8%)
- PASS: 4. Same sign out of universe in at least 2 of 3 sets (etf +0.18, coin -0.08, idx +0.05)
- FAIL: 5. Beats equal weight on Sharpe (0.87 vs 0.88)

**FAILS train.**

## Verdict (2026-11-12)

Dead. Fitted note: mu was tied to the observed event rate and (memory, branching ratio) chosen by
likelihood on a grid, with the exact discrete-time branching ratio in place of the card's
continuous-time alpha/beta. The fitted self-excitation is weak (branching ratio 0.1-0.4, memory
of 1-8 days), so the rule steps aside for a few days after a large down day and is back in.
Result: equal weight with a few missed days. Sharpe 0.87 against 0.88, the same 69% drawdown,
seven times the turnover. It beats the volatility switch only because that switch is out of the
market far more. As the survey said, at daily bars a Hawkes process is a risk model, not a signal.
