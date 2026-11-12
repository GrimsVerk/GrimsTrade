# trend-to-safe: bonds or gold instead of cash when a risk asset is out of trend

Card: `cards/trend-to-safe.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| safe | 1.02 (0.18) | +18.0% | 17.7% | 32.9% | 5.5 | 86% | 1.34 | 0.15 | 1.58 | 1.55 | 0.80 | -0.03 (p=0.77; -0.09..+0.03) | 2/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| safe | -28% | -2% | -20% | -22% | -1% | -23% | -27% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: safe +16.5%, tsmom12 +16.4%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| safe@etf | 0.68 (0.20) | +6.1% | 9.3% | 22.0% | 5.6 | 85% | 0.85 | 0.59 | 0.57 | 0.60 | +0.08 (p=0.06; -0.00..+0.18) | 4/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

## Pass bar (primary variant `safe`)

- FAIL: 1. Sharpe beats twin `tsmom12` with p < 0.10 (difference -0.03, p = 0.77)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (32.9% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 1 of 1 sets (etf +0.08)
- PASS: 5. Beats equal weight on Sharpe (1.02 vs 0.88)

**FAILS train.**

## Verdict (2026-11-12)

Fails. On the six assets it is 12-month trend again (1.02 against 1.05), ahead in 2 of 5 eras, and
behind in 2022-25 (0.80 against 0.88; -22% in the 2022 rate shock against -13%), which the card
made a condition. The safe asset's own trend test did not keep it out of trouble in 2022: gold
and long bonds were "in trend" at the wrong moments.

On the other ETFs, where the safe assets are mid-term Treasuries and corporate bonds, it did help
(0.68 against 0.60, p = 0.06, ahead in all four eras). Calmer safe assets make a better parking
place than 20-year bonds and gold. That is a hint about which safe asset, not a pass: one set,
found after the fact. If the universe ever gets a mid-term bond fund (IEF), this is worth a
fresh card.
