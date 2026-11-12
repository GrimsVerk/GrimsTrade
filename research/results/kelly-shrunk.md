# kelly-shrunk: fractional Kelly under an equal-Sharpe prior

Card: `cards/kelly-shrunk.md`. Protocol: `protocol.md`.

## The six live assets, train period

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs inverse-vol (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| k0.2 | 0.86 (0.18) | +11.6% | 13.9% | 60.0% | 0.9 | 98% | 1.33 | 0.07 | 1.79 | 1.90 | 0.88 | +0.01 (p=0.34; -0.03..+0.05) | 3/5 |
| k0.1 | 1.10 (0.18) | +11.6% | 10.5% | 35.8% | 0.9 | 89% | 1.40 | 0.32 | 1.79 | 1.90 | 0.88 | +0.25 (p=0.00; +0.14..+0.35) | 5/5 |
| k0.4 | 0.84 (0.18) | +11.9% | 14.7% | 61.1% | 0.9 | 100% | 1.35 | 0.08 | 1.79 | 1.90 | 0.88 | -0.01 (p=0.73; -0.05..+0.02) | 3/5 |
| inverse-vol | 0.85 (0.18) | +12.4% | 15.1% | 61.1% | 0.7 | 100% | 1.35 | 0.10 | 1.69 | 1.87 | 0.87 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | +0.03 (p=0.37; -0.12..+0.19) | 0/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| k0.2 | -60% | -5% | -12% | -26% | +13% | -8% | -26% |
| k0.1 | -36% | -5% | -12% | -26% | +13% | -8% | -26% |
| k0.4 | -61% | -5% | -12% | -26% | +13% | -8% | -26% |
| inverse-vol | -61% | -10% | -14% | -27% | +11% | -9% | -27% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

Annualised log growth: k0.2 +11.0%, k0.1 +11.0%, k0.4 +11.2%, inverse-vol +11.7%, equal-weight +16.7%

## Out of universe: etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs inverse-vol@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| k0.2@etf | 0.48 (0.20) | +4.0% | 9.1% | 35.1% | 0.8 | 99% | 0.41 | 0.77 | 0.83 | 0.23 | -0.00 (p=0.51; -0.08..+0.08) | 2/4 |
| inverse-vol@etf | 0.48 (0.20) | +4.8% | 11.0% | 36.6% | 0.4 | 100% | 0.35 | 0.68 | 0.87 | 0.35 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | +0.00 (p=0.51; -0.10..+0.10) | 2/4 |

## Out of universe: coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs inverse-vol@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| k0.2@coin | 0.86 (0.34) | +28.6% | 37.0% | 46.6% | 2.0 | 43% | 0.96 | 0.77 | +0.13 (p=0.21; -0.12..+0.38) | 2/2 |
| inverse-vol@coin | 0.73 (0.34) | +29.1% | 94.9% | 91.7% | 3.5 | 100% | 0.89 | 0.49 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | -0.01 (p=0.73; -0.04..+0.02) | 0/2 |

## Out of universe: idx, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs inverse-vol@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| k0.2@idx | 0.61 (0.13) | +7.1% | 12.5% | 56.6% | 0.6 | 100% | 0.59 | 1.04 | 1.15 | -0.10 | 0.66 | 0.69 | 1.00 | +0.01 (p=0.30; -0.01..+0.02) | 3/7 |
| inverse-vol@idx | 0.60 (0.13) | +7.1% | 12.7% | 56.8% | 0.5 | 100% | 0.59 | 1.04 | 1.18 | -0.07 | 0.63 | 0.65 | 0.96 | - | - |
| equal-weight@idx | 0.62 (0.13) | +7.5% | 13.1% | 57.6% | 0.2 | 100% | 0.71 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | +0.01 (p=0.16; -0.01..+0.04) | 3/7 |

## Pass bar (primary variant `k0.2`)

- FAIL: 1. Sharpe beats twin `inverse-vol` with p < 0.10 (difference +0.01, p = 0.34)
- FAIL: 2. Ahead of the twin in at least 4 of 5 eras (3 of 5)
- PASS: 3. Max drawdown not more than 5 points worse than the twin's (60.0% vs 61.1%)
- PASS: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.00, coin +0.13, idx +0.01)
- FAIL: 5. Beats equal weight on Sharpe (0.86 vs 0.88)

**FAILS train.**
## Verdict (2026-11-12)

Dead as carded. The primary variant is inverse-vol to within noise on the six assets (+0.01), the
other ETFs (0.00) and the indexes (+0.01). The reason is the one the card feared: with a
no-leverage cap the Kelly fractions add to more than 1 almost always and are scaled back to 1, and
the correlation correction that is left is worth nothing measurable.

Two things to keep, neither of which is a pass:

- The quarter-Kelly sensitivity `k0.1` shows +0.25 Sharpe over the twin (p = 0.00). It all comes
  from one episode: 2000-2002, when the universe was SPY and QQQ at 25-40% volatility and the
  smaller fraction left a third of the book in cash (-36% instead of -60%). From 2010 on the three
  variants are identical. Choosing it now would be picking a parameter after seeing the result on
  the strength of one event; it is not selected.
- On the six other coins the absolute Kelly scale did what the theory says: the same growth
  (+28.6% a year versus +29.1%) at 37% volatility instead of 95%, and a 47% maximum drawdown
  instead of 92%. The Sharpe gain (+0.13, p = 0.21) is not significant on eight years. This is the
  practical lesson: for crypto, size by volatility on an absolute scale. It goes into `ideas.md`
  as `vol-target-crypto` for a fresh card; it was not carded in advance and is not a result.
