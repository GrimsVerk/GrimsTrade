# combo-1, step 2: the two carded blends

Card: `combo-1.md`, "Step 2: card". Train period, total-return prices, protocol costs (25 + 5 bps crypto, 2 bps ETFs). Sharpe on calendar days. p = paired stationary bootstrap, one-sided, against `tsmom12`; bar p < 0.10 / 72 = 0.0014.

## Six live assets, from 1994-02-01

| Book | Sharpe | vs `tsmom12` | p | Worst loss % | Growth %/yr | Turnover | Mean shares (sleeve 1 / 2) | Distance from `tsmom12` |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `blend-iv` | 1.07 | +0.02 | 0.385 | 44.4 | +15.1 | 1.44 | 0.47 / 0.53 | 12% |
| `blend-ws` | 1.13 | +0.08 | 0.059 | 28.9 | +17.2 | 3.02 | 0.47 / 0.53 | 3% |
| `tsmom12` | 1.05 | | | 36.5 | +17.8 | 2.74 | | |
| `equal-weight` | 0.88 | | | 68.8 | +18.2 | 1.25 | | |

### Sharpe by era (six assets)

| Book | all | 2003-25 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `blend-iv` | 1.07 | 1.42 | 1.35 | 0.14 | 1.85 | 1.85 | 0.93 |
| `blend-ws` | 1.13 | 1.35 | 1.34 | 0.19 | 1.66 | 1.86 | 0.82 |
| `tsmom12` | 1.05 | 1.20 | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 |
| `equal-weight` | 0.88 | 1.19 | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 |

### Excess over `tsmom12` by the map's regimes (% a year, six assets)

| Book | trend off | trend mixed | trend on | chop (>=3 flips/13 wk) | fast fall (21-day, worst 5%) | slow bear (12-mo below 0) | stock-bond corr > 0 (1y) | tsmom12 top-10 falls (peak to low) | 6 months after those lows | tsmom12 losing weeks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `blend-iv` | +0.9 | -1.4 | -3.8 | -6.8 | -11.4 | -0.1 | +1.0 | +11.8 | -13.1 | +17.4 |
| `blend-ws` | +1.1 | -0.3 | -1.4 | -3.4 | +27.1 | +1.5 | -2.1 | +8.5 | -11.6 | +10.8 |

## 8 other ETFs, from 2001-05-27

| Book | Sharpe | vs `tsmom12` | p | Worst loss % | Growth %/yr | Turnover | Mean shares (sleeve 1 / 2) | Distance from `tsmom12` |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `blend-iv` | 0.61 | +0.01 | 0.422 | 21.9 | +5.1 | 1.73 | 0.55 / 0.45 | 15% |
| `blend-ws` | 0.62 | +0.02 | 0.073 | 16.8 | +5.2 | 2.66 | 0.49 / 0.51 | 2% |
| `tsmom12` | 0.60 | | | 16.5 | +5.0 | 2.93 | | |
| `equal-weight` | 0.48 | | | 43.1 | +6.4 | 0.32 | | |

## 6 other coins, from 2017-08-18

| Book | Sharpe | vs `tsmom12` | p | Worst loss % | Growth %/yr | Turnover | Mean shares (sleeve 1 / 2) | Distance from `tsmom12` |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `blend-iv` | 0.65 | +0.12 | 0.066 | 90.9 | +23.1 | 4.04 | 0.54 / 0.46 | 12% |
| `blend-ws` | 0.56 | +0.02 | 0.458 | 76.0 | +17.9 | 4.56 | 0.41 / 0.59 | 13% |
| `tsmom12` | 0.54 | | | 92.4 | +13.3 | 4.62 | | |
| `equal-weight` | 0.72 | | | 91.6 | +27.5 | 3.22 | | |

## 4 indexes as one portfolio, from 1962-01-02

| Book | Sharpe | vs `tsmom12` | p | Worst loss % | Growth %/yr | Turnover | Mean shares (sleeve 1 / 2) | Distance from `tsmom12` |
|---|---:|---:|---:|---:|---:|---:|---|---:|
| `blend-iv` | 0.69 | -0.03 | 0.688 | 33.0 | +6.5 | 1.49 | 0.59 / 0.41 | 8% |
| `blend-ws` | 0.72 | +0.00 | 0.449 | 25.7 | +6.2 | 2.27 | 0.49 / 0.51 | 0% |
| `tsmom12` | 0.72 | | | 25.7 | +6.1 | 2.28 | | |
| `equal-weight` | 0.62 | | | 57.6 | +7.5 | 0.20 | | |

## Pass bar

| Blend | 1. p < 0.0014 | 2. eras | 3. worst loss | 4. out of universe | 5. beats EW | 6. since 2003 | Verdict |
|---|---|---|---|---|---|---|---|
| `blend-iv` | +0.02, p 0.385 FAIL | 4 of 5 pass | 44.4% vs 36.5% FAIL | etf +0.01, coin +0.12, idx -0.03 pass | 1.07 vs EW 0.88 pass | 1.41 vs 1.19 / EW 1.19 pass | fail |
| `blend-ws` | +0.08, p 0.059 FAIL | 2 of 5 FAIL | 28.9% vs 36.5% pass | etf +0.02, coin +0.02, idx +0.00 pass | 1.13 vs EW 0.88 pass | 1.34 vs 1.19 / EW 1.19 pass | fail |
