# absorption-ratio: market tightness from sector eigenvalues

Card: `cards/absorption-ratio.md`. All runs start 2002-01-01.

Share of weeks-days with the signal on (shift > 1): absorption ratio 29%, volatility twin 17%; correlation of the two shifts 0.30.

## The six live assets

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-shift (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| six | 1.02 (0.21) | +17.7% | 17.5% | 45.5% | 1.8 | 81% | 0.93 | 1.46 | 1.42 | 0.41 | -0.15 (p=0.86; -0.38..+0.07) | 1/4 |
| vol-shift | 1.17 (0.21) | +21.6% | 18.1% | 37.1% | 2.7 | 90% | 0.46 | 1.58 | 1.80 | 0.86 | - | - |
| equal-weight | 1.04 (0.21) | +21.9% | 21.1% | 47.0% | 1.3 | 100% | 0.39 | 1.67 | 1.55 | 0.67 | -0.12 (p=0.86; -0.30..+0.06) | 1/4 |

Sharpe, rule vs twin, before and after publication: 2002-2010: 0.97 vs 0.56; 2011-2025: 1.13 vs 1.44

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| six | - | +7% | -6% | -37% | -17% | -41% | -42% |
| vol-shift | - | -10% | -5% | -22% | -11% | -26% | -30% |
| equal-weight | - | -20% | -22% | -37% | -17% | -42% | -42% |

## SPY alone

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-shift@SPY (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| spy@SPY | 0.54 (0.21) | +6.4% | 13.1% | 25.4% | 1.3 | 71% | 0.44 | 0.64 | 0.64 | 0.47 | -0.08 (p=0.69; -0.33..+0.16) | 2/4 |
| vol-shift@SPY | 0.62 (0.21) | +8.1% | 14.3% | 44.0% | 2.5 | 83% | 0.25 | 0.58 | 1.28 | 0.84 | - | - |
| equal-weight@SPY | 0.58 (0.20) | +9.7% | 19.1% | 55.2% | 0.0 | 100% | 0.18 | 0.85 | 0.99 | 0.68 | -0.04 (p=0.59; -0.25..+0.17) | 1/4 |

Sharpe, rule vs twin, before and after publication: 2002-2010: 0.41 vs 0.34; 2011-2025: 0.60 vs 0.84

## Out of universe: 8 other ETFs

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-shift@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| six@etf | 0.46 (0.21) | +4.0% | 9.7% | 20.7% | 1.1 | 77% | 0.70 | 0.20 | 0.56 | 0.38 | -0.12 (p=0.79; -0.37..+0.13) | 1/4 |
| vol-shift@etf | 0.58 (0.20) | +6.2% | 11.7% | 32.1% | 2.1 | 87% | 0.62 | 0.31 | 0.98 | 0.59 | - | - |
| equal-weight@etf | 0.51 (0.21) | +6.7% | 14.9% | 43.1% | 0.3 | 100% | 0.46 | 0.46 | 0.76 | 0.52 | -0.07 (p=0.69; -0.27..+0.14) | 1/4 |

Sharpe, rule vs twin, before and after publication: 2002-2010: 0.67 vs 0.72; 2011-2025: 0.33 vs 0.47

## Out of universe: N225 alone

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-shift@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| six@N225 | 0.34 (0.21) | +4.3% | 17.0% | 40.6% | 1.3 | 71% | 0.12 | 0.43 | 0.20 | 0.61 | -0.12 (p=0.80; -0.34..+0.10) | 1/4 |
| vol-shift@N225 | 0.45 (0.21) | +6.9% | 18.5% | 48.2% | 2.6 | 83% | 0.39 | 0.30 | 0.59 | 0.77 | - | - |
| equal-weight@N225 | 0.40 (0.21) | +6.8% | 22.6% | 61.4% | 0.0 | 100% | 0.12 | 0.49 | 0.54 | 0.79 | -0.05 (p=0.65; -0.22..+0.12) | 2/4 |

Sharpe, rule vs twin, before and after publication: 2002-2010: 0.09 vs 0.36; 2011-2025: 0.45 vs 0.51

## Out of universe: FTSE alone

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-shift@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| six@FTSE | 0.13 (0.20) | +0.8% | 12.1% | 41.2% | 1.3 | 71% | 0.22 | 0.02 | -0.12 | 0.48 | -0.03 (p=0.59; -0.25..+0.18) | 2/4 |
| vol-shift@FTSE | 0.16 (0.20) | +1.3% | 13.9% | 43.6% | 2.7 | 83% | 0.16 | -0.03 | 0.09 | 0.80 | - | - |
| equal-weight@FTSE | 0.24 (0.21) | +2.7% | 17.8% | 47.8% | 0.0 | 100% | 0.13 | 0.33 | 0.12 | 0.64 | +0.08 (p=0.22; -0.10..+0.26) | 2/4 |

Sharpe, rule vs twin, before and after publication: 2002-2010: 0.15 vs 0.20; 2011-2025: 0.12 vs 0.13

## Out of universe: GDAXI alone

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs vol-shift@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| six@GDAXI | 0.33 (0.21) | +3.9% | 15.0% | 44.0% | 1.3 | 71% | 0.43 | 0.34 | -0.07 | 0.59 | -0.08 (p=0.68; -0.36..+0.17) | 1/4 |
| vol-shift@GDAXI | 0.41 (0.20) | +5.9% | 17.9% | 49.1% | 2.6 | 83% | 0.30 | 0.35 | 0.51 | 0.87 | - | - |
| equal-weight@GDAXI | 0.40 (0.20) | +6.6% | 22.2% | 59.7% | 0.0 | 100% | 0.20 | 0.55 | 0.43 | 0.70 | -0.01 (p=0.53; -0.19..+0.18) | 1/4 |

Sharpe, rule vs twin, before and after publication: 2002-2010: 0.40 vs 0.34; 2011-2025: 0.30 vs 0.48

## Pass bar (primary variant `six`)

- FAIL: 1. Sharpe beats twin `vol-shift` with p < 0.10 (difference -0.15, p = 0.86)
- FAIL: 2. Ahead of the twin in at least 3 of 4 eras (1 of 4)
- FAIL: 3. Max drawdown not more than 5 points worse than the twin's (45.5% vs 37.1%)
- FAIL: 4. Same sign out of universe in both applicable sets (etf -0.12, idx -0.08)
- FAIL: 5. Beats equal weight on Sharpe (1.02 vs 1.04)
- FAIL: 6. (card) Not behind the twin after publication, 2011-2025 (-0.32)

**FAILS train.**
