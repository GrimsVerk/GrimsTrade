# combo-2, step 1: combo-1 rerun with T-bill cash

## A. The failure map with T-bill cash

Card: `combo-2.md`, step 1. combo-1's map with idle cash earning the 13-week T-bill rate (gym PR #61): the six gym models rebuilt from their logged configurations at protocol costs (25 + 5 bps crypto, 2 bps ETFs), regime masks unchanged from combo-1 (computed without interest). Sharpe on calendar days, against 0 (the carded statistic); Sharpe above T-bills in the extra table at the end. Excess = model's daily return minus `tsmom12`'s (both with interest), annualised, % a year. `band` (perp funding carry) exists only from 2021-02-20; its cells cover its own span.

| Model | Why it is on the map |
|---|---|
| `trend-vol` | deep-1's best risk shape: trend with volatility-sized slots (run 1, tv40) |
| `where-vol` | trend-where: filter kept only where days out were rougher (1.07) |
| `stop-0.25` | cointop-1/coin-cap: 25% stop on the coin slots (1.09, worst loss 28.9%) |
| `inverse-vol` | always invested, risk-sized: the opposite of stepping out |
| `sixty-forty` | the lowest loss-week correlation with `tsmom12` in deep-1's pool (0.44) |
| `band` | carry-3: funding carry on perps, another source of return (2021-25 only) |

### 1. Sharpe by era

| Model | all | 2003-25 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | Growth %/yr | Worst loss % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 1.08 | 1.22 | 1.35 | 0.25 | 1.55 | 1.51 | 0.99 | +18.4 | 35.6 |
| `trend-vol` | 1.08 | 1.26 | 1.35 | 0.31 | 1.63 | 1.51 | 1.09 | +13.9 | 22.2 |
| `where-vol` | 1.09 | 1.23 | 1.35 | 0.24 | 1.60 | 1.63 | 0.86 | +19.2 | 34.9 |
| `stop-0.25` | 1.13 | 1.37 | 1.35 | 0.25 | 1.56 | 1.94 | 0.87 | +16.2 | 25.7 |
| `inverse-vol` | 0.85 | 1.33 | 1.35 | 0.10 | 1.70 | 1.87 | 0.88 | +12.5 | 61.1 |
| `sixty-forty` | 0.80 | 0.85 | 1.55 | 0.23 | 1.39 | 1.33 | 0.31 | +8.6 | 30.2 |
| `band` | 0.79 | 0.79 | - | - | - | 0.83 | 0.91 | +10.8 | 17.2 |

### 2. Where each model loses to `tsmom12`: excess return by regime (% a year)

Negative = the model earns less than `tsmom12` in that regime. Regimes (descriptions on the whole sample): trend state = share of eligible assets `tsmom12` holds (off <= 1/3, on >= 2/3, deep-1's cut); chop = `tsmom12` changed at least 3 slots in the last 13 weeks; fast fall = the always-invested equal-weight book's 21-day return in its worst 5% of days; slow bear = that book's 12-month return below zero; stock-bond corr > 0 = SPY and TLT daily returns positively correlated over the past year (the 2022 kind of rate regime); `tsmom12`'s ten deepest falls (peak to low) and the six months after each low (the turn); `tsmom12`'s losing weeks.

| Model | trend off | trend mixed | trend on | chop (>=3 flips/13 wk) | fast fall (21-day, worst 5%) | slow bear (12-mo below 0) | stock-bond corr > 0 (1y) | tsmom12 top-10 falls (peak to low) | 6 months after those lows | tsmom12 losing weeks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `trend-vol` | +0.1 | -6.4 | -5.1 | -10.9 | +39.4 | +1.3 | -1.6 | +12.3 | -19.0 | +15.8 |
| `where-vol` | +2.1 | +2.8 | +0.2 | +1.3 | -10.3 | +2.2 | +5.5 | +1.3 | +1.4 | -1.2 |
| `stop-0.25` | -0.1 | -3.5 | -2.4 | -6.9 | +53.7 | +0.5 | -6.9 | +13.9 | -21.0 | +20.0 |
| `inverse-vol` | -0.7 | -5.1 | -6.4 | -12.2 | -41.4 | -2.0 | +0.9 | +17.0 | -22.2 | +28.0 |
| `sixty-forty` | +1.4 | -9.1 | -11.5 | -20.6 | +36.2 | +1.9 | -8.3 | +27.3 | -32.3 | +50.5 |
| `band` | -3.5 | +14.1 | -8.4 | -6.6 | +161.1 | +2.6 | -16.6 | +101.8 | -17.9 | +107.5 |
| *`tsmom12` own return* | *+0.6* | *+16.3* | *+22.0* | *+31.4* | *-127.5* | *-6.2* | *+18.7* | *-30.7* | *+48.6* | *-80.3* |
| *share of days* | *13%* | *14%* | *73%* | *29%* | *5%* | *20%* | *13%* | *21%* | *15%* | *37%* |

### 3. Stress windows: in the window / in the 6 months after (points, model minus `tsmom12`)

First column: `tsmom12`'s own total return in the window / after it. `-` = the model did not exist then.

| Window | `tsmom12` | `trend-vol` | `where-vol` | `stop-0.25` | `inverse-vol` | `sixty-forty` | `band` |
|---|---:|---:|---:|---:|---:|---:|---:|
| dot-com bust | -24 / +1 | +4 / -0 | +0 / +0 | +0 / +0 | -37 / +18 | -5 / +7 | - / - |
| 2008 crisis | -3 / -1 | +1 / +0 | +0 / +0 | +0 / +0 | -7 / +19 | -27 / +27 | - / - |
| covid crash | -22 / +31 | +6 / -10 | -0 / +5 | +13 / -13 | +8 / +3 | +5 / -3 | - / - |
| 2022 rate shock | -13 / +2 | +1 / +0 | -13 / +21 | +6 / +0 | -14 / +20 | -13 / +11 | +27 / -9 |
| crypto winter 2014 | -6 / +0 | +7 / -0 | +3 / -0 | +6 / +0 | +17 / +2 | +28 / -1 | - / - |
| crypto winter 2018 | -22 / +6 | +8 / -1 | +0 / +16 | +18 / -0 | +13 / +14 | +19 / +7 | - / - |
| crypto winter 2022 | -18 / +3 | +4 / +0 | -15 / +20 | +7 / +0 | -8 / +15 | -2 / +3 | +24 / -2 |

### 4. Does the model cover `tsmom12`'s losses? (weekly, 7-day blocks)

Corr = correlation of the model's weekly return with `tsmom12`'s (all weeks; weeks `tsmom12` lost). Ahead = share of `tsmom12`'s losing weeks in which the model lost less. Worst 10% = mean weekly return (%) in `tsmom12`'s worst tenth of weeks, model and `tsmom12` on the same weeks.

| Model | Corr, all | Corr, losing weeks | Ahead in losing weeks | Worst 10%: model | Worst 10%: `tsmom12` | Losing weeks |
|---|---:|---:|---:|---:|---:|---:|
| `trend-vol` | +0.92 | +0.88 | 55% | -2.86 | -3.74 | 617 |
| `where-vol` | +0.97 | +0.96 | 27% | -3.83 | -3.74 | 617 |
| `stop-0.25` | +0.87 | +0.78 | 32% | -2.66 | -3.74 | 617 |
| `inverse-vol` | +0.61 | +0.70 | 67% | -2.35 | -3.74 | 617 |
| `sixty-forty` | +0.46 | +0.44 | 79% | -1.32 | -3.74 | 617 |
| `band` | +0.05 | +0.01 | 79% | +0.36 | -3.88 | 99 |

### 5. Pairs: correlation of weekly excess returns (each minus `tsmom12`) by regime

Low or negative = the two models lose to `tsmom12` at different times, so a blend of them (or of either with `tsmom12`) could cover one with the other. `-` = fewer than 26 common weeks.

| Pair | all weeks | tsmom12 losing | chop | fast fall | slow bear | stock-bond + | turn (6 mo after low) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `trend-vol` + `where-vol` | +0.00 | +0.00 | +0.01 | +0.05 | -0.01 | -0.07 | -0.06 |
| `trend-vol` + `stop-0.25` | +0.61 | +0.62 | +0.65 | +0.79 | +0.03 | +0.58 | +0.74 |
| `trend-vol` + `inverse-vol` | +0.66 | +0.77 | +0.82 | +0.42 | +0.07 | +0.65 | +0.87 |
| `trend-vol` + `sixty-forty` | +0.78 | +0.75 | +0.82 | +0.70 | +0.34 | +0.67 | +0.87 |
| `trend-vol` + `band` | +0.67 | +0.55 | +0.65 | - | -0.06 | +0.74 | +0.79 |
| `where-vol` + `stop-0.25` | -0.02 | -0.00 | -0.04 | +0.06 | -0.20 | -0.01 | -0.06 |
| `where-vol` + `inverse-vol` | +0.21 | +0.27 | +0.30 | +0.20 | +0.29 | +0.42 | +0.21 |
| `where-vol` + `sixty-forty` | +0.11 | +0.13 | +0.13 | +0.23 | +0.24 | +0.12 | +0.06 |
| `where-vol` + `band` | -0.18 | -0.10 | -0.32 | - | -0.10 | -0.19 | -0.29 |
| `stop-0.25` + `inverse-vol` | +0.48 | +0.67 | +0.59 | +0.40 | -0.07 | +0.58 | +0.68 |
| `stop-0.25` + `sixty-forty` | +0.57 | +0.61 | +0.61 | +0.55 | -0.07 | +0.64 | +0.69 |
| `stop-0.25` + `band` | +0.65 | +0.52 | +0.67 | - | -0.05 | +0.67 | +0.68 |
| `inverse-vol` + `sixty-forty` | +0.86 | +0.88 | +0.94 | +0.86 | +0.81 | +0.89 | +0.94 |
| `inverse-vol` + `band` | +0.54 | +0.47 | +0.36 | - | -0.01 | +0.56 | +0.56 |
| `sixty-forty` + `band` | +0.63 | +0.50 | +0.50 | - | +0.04 | +0.64 | +0.67 |

### 6. Sharpe above T-bills by era (gym models, #61's convention)

| Model | all | 2003-25 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 0.93 | 1.12 | 1.05 | 0.04 | 1.54 | 1.47 | 0.72 |
| `trend-vol` | 0.89 | 1.12 | 1.05 | 0.08 | 1.62 | 1.43 | 0.76 |
| `where-vol` | 0.95 | 1.14 | 1.05 | 0.03 | 1.59 | 1.59 | 0.64 |
| `stop-0.25` | 0.96 | 1.24 | 1.05 | 0.04 | 1.56 | 1.87 | 0.50 |
| `inverse-vol` | 0.69 | 1.18 | 1.05 | -0.04 | 1.69 | 1.78 | 0.59 |
| `sixty-forty` | 0.58 | 0.70 | 1.06 | 0.02 | 1.38 | 1.23 | 0.01 |
| `equal-weight` | 0.77 | 1.11 | 1.05 | -0.10 | 1.66 | 1.51 | 0.50 |

## B. The two blends with T-bill cash

combo-1's card unchanged (equal-risk shares refitted yearly, protocol costs); every book (sleeves, blend, `tsmom12` twin, equal weight) earns the T-bill rate on idle cash. p = paired stationary bootstrap, one-sided; bar p < 0.0014 (family 72). Left: Sharpe against 0 (the card); right: above T-bills.

### Six live assets, from 1994-02-01 (average bill rate 2.4%)

| Book | Sharpe | vs `tsmom12` | p | Sharpe above bills | vs `tsmom12` | p | Worst loss % | Growth %/yr | Mean shares |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `blend-iv` | 1.09 | +0.01 | 0.450 | 0.91 | -0.02 | 0.590 | 42.8 | +15.3 | 0.47 / 0.53 |
| `blend-ws` | 1.16 | +0.08 | 0.051 | 1.00 | +0.06 | 0.108 | 25.7 | +17.7 | 0.47 / 0.53 |
| `tsmom12` | 1.08 | | | 0.93 | | | 35.6 | +18.4 | |
| `equal-weight` | 0.88 | | | 0.77 | | | 68.8 | +18.2 | |

### 8 other ETFs, from 2001-05-27 (average bill rate 1.7%)

| Book | Sharpe | vs `tsmom12` | p | Sharpe above bills | vs `tsmom12` | p | Worst loss % | Growth %/yr | Mean shares |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `blend-iv` | 0.65 | -0.01 | 0.514 | 0.46 | -0.01 | 0.515 | 21.8 | +5.4 | 0.55 / 0.45 |
| `blend-ws` | 0.67 | +0.02 | 0.150 | 0.49 | +0.02 | 0.124 | 16.7 | +5.7 | 0.49 / 0.51 |
| `tsmom12` | 0.66 | | | 0.47 | | | 16.5 | +5.5 | |
| `equal-weight` | 0.48 | | | 0.37 | | | 43.1 | +6.4 | |

### 6 other coins, from 2017-08-18 (average bill rate 2.5%)

| Book | Sharpe | vs `tsmom12` | p | Sharpe above bills | vs `tsmom12` | p | Worst loss % | Growth %/yr | Mean shares |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `blend-iv` | 0.66 | +0.11 | 0.085 | 0.63 | +0.11 | 0.081 | 90.8 | +24.0 | 0.54 / 0.46 |
| `blend-ws` | 0.59 | +0.04 | 0.406 | 0.54 | +0.02 | 0.452 | 75.2 | +19.9 | 0.41 / 0.59 |
| `tsmom12` | 0.55 | | | 0.52 | | | 92.2 | +14.7 | |
| `equal-weight` | 0.72 | | | 0.70 | | | 91.6 | +27.5 | |

### 4 indexes as one portfolio, from 1962-01-02 (average bill rate 4.4%)

| Book | Sharpe | vs `tsmom12` | p | Sharpe above bills | vs `tsmom12` | p | Worst loss % | Growth %/yr | Mean shares |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `blend-iv` | 0.76 | -0.09 | 0.953 | 0.31 | -0.04 | 0.802 | 32.5 | +7.2 | 0.59 / 0.41 |
| `blend-ws` | 0.85 | -0.01 | 0.661 | 0.35 | -0.00 | 0.592 | 25.6 | +7.4 | 0.49 / 0.51 |
| `tsmom12` | 0.85 | | | 0.35 | | | 25.6 | +7.4 | |
| `equal-weight` | 0.62 | | | 0.28 | | | 57.7 | +7.5 | |

### Sharpe by era (six assets, against 0)

| Book | all | 2003-25 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `blend-iv` | 1.09 | 1.43 | 1.35 | 0.17 | 1.85 | 1.85 | 0.97 |
| `blend-ws` | 1.16 | 1.38 | 1.35 | 0.25 | 1.66 | 1.88 | 0.91 |
| `tsmom12` | 1.08 | 1.22 | 1.35 | 0.25 | 1.55 | 1.51 | 0.97 |
| `equal-weight` | 0.88 | 1.19 | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 |

### Sharpe by era (six assets, above T-bills)

| Book | all | 2003-25 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `blend-iv` | 0.91 | 1.30 | 1.05 | -0.02 | 1.84 | 1.79 | 0.68 |
| `blend-ws` | 1.00 | 1.26 | 1.05 | 0.04 | 1.66 | 1.82 | 0.61 |
| `tsmom12` | 0.93 | 1.12 | 1.05 | 0.04 | 1.54 | 1.47 | 0.72 |
| `equal-weight` | 0.77 | 1.11 | 1.05 | -0.10 | 1.66 | 1.51 | 0.50 |

### Excess over `tsmom12` by the map's regimes (% a year, six assets, with cash)

| Book | trend off | trend mixed | trend on | chop (>=3 flips/13 wk) | fast fall (21-day, worst 5%) | slow bear (12-mo below 0) | stock-bond corr > 0 (1y) | tsmom12 top-10 falls (peak to low) | 6 months after those lows | tsmom12 losing weeks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `blend-iv` | -0.4 | -1.6 | -3.9 | -7.1 | -12.2 | -1.0 | +0.4 | +11.3 | -13.2 | +17.2 |
| `blend-ws` | +0.9 | -0.4 | -1.4 | -3.4 | +27.3 | +1.4 | -2.2 | +8.4 | -11.7 | +10.8 |

### Pass bar, Sharpe against 0 (the card)

| Blend | 1. p < 0.0014 | 2. eras | 3. worst loss | 4. out of universe | 5. beats EW | 6. since 2003 | Verdict |
|---|---|---|---|---|---|---|---|
| `blend-iv` | +0.01, p 0.450 FAIL | 3 of 5 FAIL | 42.8% vs 35.6% FAIL | etf -0.01, coin +0.11, idx -0.09 FAIL | 1.09 vs EW 0.88 pass | 1.43 vs 1.22 / EW 1.19 pass | fail |
| `blend-ws` | +0.08, p 0.051 FAIL | 2 of 5 FAIL | 25.7% vs 35.6% pass | etf +0.02, coin +0.04, idx -0.01 pass | 1.16 vs EW 0.88 pass | 1.37 vs 1.22 / EW 1.19 pass | fail |

### Pass bar, Sharpe above T-bills (#61's convention)

| Blend | 1. p < 0.0014 | 2. eras | 3. worst loss | 4. out of universe | 5. beats EW | 6. since 2003 | Verdict |
|---|---|---|---|---|---|---|---|
| `blend-iv` | -0.02, p 0.590 FAIL | 3 of 5 FAIL | 47.9% vs 38.3% FAIL | etf -0.01, coin +0.11, idx -0.04 FAIL | 0.91 vs EW 0.77 pass | 1.29 vs 1.12 / EW 1.11 pass | fail |
| `blend-ws` | +0.06, p 0.108 FAIL | 2 of 5 FAIL | 31.6% vs 38.3% pass | etf +0.02, coin +0.02, idx -0.00 pass | 1.00 vs EW 0.77 pass | 1.26 vs 1.12 / EW 1.11 pass | fail |

