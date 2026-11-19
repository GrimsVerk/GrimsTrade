# combo-1, step 1: the failure map

Plan and reading: `combo-1.md`. Six live assets, train period (decisions 1994-02-01 .. 2025-11-09), total-return prices, protocol costs (30 bps crypto, 2 bps ETFs). Sharpe on calendar days. Excess = model's daily return minus `tsmom12`'s on the same day, annualised (x 365), in percent a year. Nothing here was run anew or selected: every series is a logged configuration read from saved output. `band` (perp funding carry) exists only from 2021-02-20; its cells cover its own span.

| Model | Why it is on the map |
|---|---|
| `trend-vol` | deep-1's best risk shape: trend with volatility-sized slots (run 1, tv40) |
| `where-vol` | trend-where: filter kept only where days out were rougher (1.07) |
| `stop-0.25` | cointop-1/coin-cap: 25% stop on the coin slots (1.09, worst loss 28.9%) |
| `inverse-vol` | always invested, risk-sized: the opposite of stepping out |
| `sixty-forty` | the lowest loss-week correlation with `tsmom12` in deep-1's pool (0.44) |
| `band` | carry-3: funding carry on perps, another source of return (2021-25 only) |

## 1. Sharpe by era

| Model | all | 2003-25 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | Growth %/yr | Worst loss % |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 1.05 | 1.20 | 1.34 | 0.19 | 1.55 | 1.50 | 0.90 | +17.8 | 36.5 |
| `trend-vol` | 1.03 | 1.22 | 1.35 | 0.24 | 1.63 | 1.48 | 0.97 | +13.3 | 25.7 |
| `where-vol` | 1.07 | 1.23 | 1.34 | 0.18 | 1.60 | 1.63 | 0.84 | +18.9 | 35.3 |
| `stop-0.25` | 1.09 | 1.33 | 1.34 | 0.19 | 1.56 | 1.91 | 0.70 | +15.6 | 28.9 |
| `inverse-vol` | 0.85 | 1.32 | 1.35 | 0.10 | 1.70 | 1.87 | 0.87 | +12.4 | 61.1 |
| `sixty-forty` | 0.76 | 0.85 | 1.35 | 0.19 | 1.39 | 1.33 | 0.31 | +8.1 | 31.0 |
| `band` | 0.79 | 0.79 | - | - | - | 0.83 | 0.91 | +10.8 | 17.2 |

## 2. Where each model loses to `tsmom12`: excess return by regime (% a year)

Negative = the model earns less than `tsmom12` in that regime. Regimes (descriptions on the whole sample): trend state = share of eligible assets `tsmom12` holds (off <= 1/3, on >= 2/3, deep-1's cut); chop = `tsmom12` changed at least 3 slots in the last 13 weeks; fast fall = the always-invested equal-weight book's 21-day return in its worst 5% of days; slow bear = that book's 12-month return below zero; stock-bond corr > 0 = SPY and TLT daily returns positively correlated over the past year (the 2022 kind of rate regime); `tsmom12`'s ten deepest falls (peak to low) and the six months after each low (the turn); `tsmom12`'s losing weeks.

| Model | trend off | trend mixed | trend on | chop (>=3 flips/13 wk) | fast fall (21-day, worst 5%) | slow bear (12-mo below 0) | stock-bond corr > 0 (1y) | tsmom12 top-10 falls (peak to low) | 6 months after those lows | tsmom12 losing weeks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `trend-vol` | +0.1 | -6.4 | -5.1 | -11.0 | +39.3 | +1.3 | -1.7 | +12.2 | -19.1 | +15.8 |
| `where-vol` | +2.5 | +3.0 | +0.3 | +1.7 | -10.2 | +2.6 | +6.3 | +1.5 | +1.6 | -1.0 |
| `stop-0.25` | -0.1 | -3.6 | -2.5 | -7.1 | +53.7 | +0.5 | -7.3 | +13.7 | -21.0 | +19.9 |
| `inverse-vol` | +1.6 | -4.8 | -6.3 | -11.7 | -40.1 | -0.4 | +2.0 | +18.1 | -22.0 | +28.3 |
| `sixty-forty` | +3.2 | -8.7 | -11.9 | -20.2 | +37.0 | +3.0 | -7.2 | +27.9 | -32.3 | +50.4 |
| `band` | -0.3 | +16.0 | -7.8 | -5.1 | +162.0 | +5.7 | -15.2 | +102.2 | -17.3 | +108.5 |
| *`tsmom12` own return* | *-1.8* | *+15.9* | *+21.8* | *+30.9* | *-128.8* | *-7.9* | *+17.6* | *-31.9* | *+48.3* | *-80.7* |
| *share of days* | *13%* | *14%* | *73%* | *29%* | *5%* | *20%* | *13%* | *21%* | *15%* | *37%* |

## 3. Stress windows: in the window / in the 6 months after (points, model minus `tsmom12`)

First column: `tsmom12`'s own total return in the window / after it. `-` = the model did not exist then.

| Window | `tsmom12` | `trend-vol` | `where-vol` | `stop-0.25` | `inverse-vol` | `sixty-forty` | `band` |
|---|---:|---:|---:|---:|---:|---:|---:|
| dot-com bust | -28 / +0 | +3 / +0 | +0 / +0 | +0 / +0 | -33 / +18 | -3 / +8 | - / - |
| 2008 crisis | -4 / -1 | +1 / -0 | +0 / +0 | +0 / +0 | -7 / +19 | -26 / +27 | - / - |
| covid crash | -22 / +31 | +6 / -10 | -0 / +5 | +13 / -13 | +8 / +3 | +5 / -3 | - / - |
| 2022 rate shock | -13 / -0 | +1 / +0 | -13 / +22 | +6 / +0 | -14 / +22 | -12 / +13 | +28 / -7 |
| crypto winter 2014 | -6 / +0 | +7 / -0 | +3 / -0 | +6 / +0 | +17 / +2 | +28 / -1 | - / - |
| crypto winter 2018 | -22 / +5 | +8 / -1 | +1 / +16 | +18 / -0 | +13 / +15 | +20 / +8 | - / - |
| crypto winter 2022 | -20 / +1 | +3 / +0 | -14 / +21 | +7 / +0 | -7 / +17 | -1 / +5 | +25 / +0 |

## 4. Does the model cover `tsmom12`'s losses? (weekly, 7-day blocks)

Corr = correlation of the model's weekly return with `tsmom12`'s (all weeks; weeks `tsmom12` lost). Ahead = share of `tsmom12`'s losing weeks in which the model lost less. Worst 10% = mean weekly return (%) in `tsmom12`'s worst tenth of weeks, model and `tsmom12` on the same weeks.

| Model | Corr, all | Corr, losing weeks | Ahead in losing weeks | Worst 10%: model | Worst 10%: `tsmom12` | Losing weeks |
|---|---:|---:|---:|---:|---:|---:|
| `trend-vol` | +0.92 | +0.88 | 56% | -2.86 | -3.74 | 619 |
| `where-vol` | +0.97 | +0.96 | 27% | -3.83 | -3.74 | 619 |
| `stop-0.25` | +0.87 | +0.78 | 32% | -2.66 | -3.74 | 619 |
| `inverse-vol` | +0.61 | +0.70 | 67% | -2.35 | -3.74 | 619 |
| `sixty-forty` | +0.46 | +0.44 | 78% | -1.34 | -3.74 | 619 |
| `band` | +0.05 | +0.01 | 78% | +0.36 | -3.90 | 101 |

## 5. Pairs: correlation of weekly excess returns (each minus `tsmom12`) by regime

Low or negative = the two models lose to `tsmom12` at different times, so a blend of them (or of either with `tsmom12`) could cover one with the other. `-` = fewer than 26 common weeks.

| Pair | all weeks | tsmom12 losing | chop | fast fall | slow bear | stock-bond + | turn (6 mo after low) |
|---|---:|---:|---:|---:|---:|---:|---:|
| `trend-vol` + `where-vol` | -0.00 | +0.00 | +0.00 | +0.05 | -0.01 | -0.07 | -0.06 |
| `trend-vol` + `stop-0.25` | +0.61 | +0.62 | +0.65 | +0.79 | +0.03 | +0.58 | +0.74 |
| `trend-vol` + `inverse-vol` | +0.66 | +0.77 | +0.82 | +0.42 | +0.07 | +0.65 | +0.87 |
| `trend-vol` + `sixty-forty` | +0.78 | +0.75 | +0.82 | +0.70 | +0.34 | +0.67 | +0.87 |
| `trend-vol` + `band` | +0.67 | +0.55 | +0.66 | - | -0.06 | +0.74 | +0.79 |
| `where-vol` + `stop-0.25` | -0.02 | +0.00 | -0.04 | +0.06 | -0.19 | -0.01 | -0.07 |
| `where-vol` + `inverse-vol` | +0.21 | +0.28 | +0.30 | +0.20 | +0.29 | +0.42 | +0.21 |
| `where-vol` + `sixty-forty` | +0.11 | +0.13 | +0.13 | +0.24 | +0.24 | +0.12 | +0.06 |
| `where-vol` + `band` | -0.18 | -0.12 | -0.31 | - | -0.09 | -0.19 | -0.29 |
| `stop-0.25` + `inverse-vol` | +0.48 | +0.67 | +0.59 | +0.40 | -0.07 | +0.57 | +0.68 |
| `stop-0.25` + `sixty-forty` | +0.57 | +0.61 | +0.61 | +0.55 | -0.06 | +0.64 | +0.69 |
| `stop-0.25` + `band` | +0.65 | +0.52 | +0.67 | - | -0.06 | +0.67 | +0.68 |
| `inverse-vol` + `sixty-forty` | +0.86 | +0.88 | +0.94 | +0.86 | +0.81 | +0.89 | +0.94 |
| `inverse-vol` + `band` | +0.54 | +0.46 | +0.36 | - | -0.01 | +0.56 | +0.56 |
| `sixty-forty` + `band` | +0.63 | +0.50 | +0.50 | - | +0.04 | +0.64 | +0.67 |
