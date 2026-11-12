# crypto-slot-size: how big should the crypto slots be?

Card: `cards/crypto-slot-size.md`. Six live assets, decisions from 2013-01-01.

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2010-16 | 2017-21 | 2022-25 | dSharpe vs equal-weight (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| c05 | 1.36 (0.29) | +18.0% | 12.8% | 30.5% | 0.5 | 100% | 1.54 | 1.77 | 0.82 | +0.02 (p=0.45; -0.22..+0.27) | 2/3 |
| c10 | 1.39 (0.29) | +24.9% | 17.1% | 37.3% | 0.9 | 100% | 1.85 | 1.70 | 0.74 | +0.05 (p=0.23; -0.06..+0.17) | 3/3 |
| c00 | 1.05 (0.28) | +11.1% | 10.6% | 25.2% | 0.4 | 100% | 0.82 | 1.46 | 0.80 | -0.29 (p=0.85; -0.75..+0.17) | 1/3 |
| equal-weight | 1.34 (0.29) | +35.3% | 24.9% | 47.0% | 1.3 | 100% | 1.82 | 1.55 | 0.67 | - | - |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| c05 | - | - | -16% | -27% | +7% | -14% | -27% |
| c10 | - | - | -19% | -32% | -0% | -27% | -34% |
| c00 | - | - | -14% | -24% | +17% | -1% | -19% |
| equal-weight | - | - | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: c05 +16.5%, c10 +22.2%, c00 +10.5%, equal-weight +30.2%

## Reading (2026-11-12)

Descriptive, as the card said. Since 2013 the Sharpe ratio barely depends on the size of the
crypto slots once there is any crypto at all: 1.36 at 5% per coin, 1.39 at 10%, 1.34 at 1/6.
None of these differences is close to significant. Holding no crypto is lower (1.05), also not
significantly (the gap is about one standard error).

What the size sets is the scale of everything:

| Per coin | Growth a year | Worst loss | Crypto winter 2018 | Crypto winter 2022 |
|---|---:|---:|---:|---:|
| 0% | +11.1% | 25% | -1% | -19% |
| 5% | +18.0% | 31% | -14% | -27% |
| 10% | +24.9% | 37% | -27% | -34% |
| 1/6 (equal weight) | +35.3% | 47% | -42% | -42% |

This is one decade in which Bitcoin rose about a thousandfold; the growth column will not repeat.
The worst-loss column is the more durable information. The size of the crypto slot is the single
biggest risk setting in the live universe, bigger than any rule tested in this run, and it is a
decision for the owner, not something a backtest can optimise.
