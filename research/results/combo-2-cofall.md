# combo-2, step 2: `cofall-dbc`

Card: `combo-2.md`, "Step 2 card". Six live assets plus DBC, train period, total-return prices, protocol costs (25 + 5 bps crypto, 2 bps ETFs), T-bill interest on cash for every book. Sharpe on calendar days. p = paired stationary bootstrap, one-sided, against the `tsmom12` twin; bar p < 0.10 / 73 = 0.00137.

Gate open (SPY and TLT both out of trend): 448 of 11605 days (3.9%), 64 weeks; DBC held 294 days (42 weeks). First day DBC was held: 2022-04-29.

## Full train

| Book | Sharpe | vs twin | p | 90% range | Sharpe above bills | vs twin | p | Worst loss % | Growth %/yr |
|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| `cofall-dbc` | 1.07 | -0.006 | 0.845 | -0.016..+0.003 | 0.93 | -0.006 | 0.842 | 35.6 | +18.30 |
| `tsmom12` (twin) | 1.08 | | | | 0.93 | | | 35.6 | +18.40 |
| `equal-weight` | 0.88 | | | | 0.77 | | | 68.8 | +18.23 |

## Sharpe by era (against 0 / above bills)

| Book | all | 2003-25 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|
| `cofall-dbc` | 1.07 / 0.93 | 1.21 / 1.11 | 1.35 / 1.05 | 0.25 / 0.04 | 1.55 / 1.54 | 1.51 / 1.47 | 0.92 / 0.67 |
| `tsmom12` | 1.08 / 0.93 | 1.22 / 1.12 | 1.35 / 1.05 | 0.25 / 0.04 | 1.55 / 1.54 | 1.51 / 1.47 | 0.97 / 0.72 |
| `equal-weight` | 0.88 / 0.77 | 1.19 / 1.11 | 1.35 / 1.05 | 0.02 / -0.10 | 1.67 / 1.66 | 1.55 / 1.51 | 0.67 / 0.50 |

## Gate spells (SPY and TLT both out of trend)

Points of total return in the spell (book minus twin; decision days, holdings from the next open). DBC weeks = weeks the partner was held.

| Spell | Days | DBC weeks | Twin % | Book % | Book minus twin (points) | DBC own % |
|---|---:|---:|---:|---:|---:|---:|
| 2016-01-08 .. 2016-02-11 | 35 | 0 | -4.2 | -4.2 | +0.0 | -3.7 |
| 2018-12-14 .. 2019-01-31 | 49 | 0 | -1.4 | -1.4 | +0.0 | +1.8 |
| 2022-04-29 .. 2022-05-26 | 28 | 4 | -1.5 | -0.5 | +1.0 | +4.1 |
| 2022-06-03 .. 2023-05-04 | 336 | 38 | +1.9 | -2.0 | -4.0 | -23.8 |

## 2022

| Window | Twin % | Book % | Points |
|---|---:|---:|---:|
| calendar 2022 | -11.2 | -12.9 | -1.7 |
| 2022 rate shock | -12.6 | -13.9 | -1.2 |
| 2022-25 | +73.8 | +69.3 | -4.5 |

## Excess over the twin by regime (% a year)

| Book | gate open (own weeks) | trend off | trend mixed | trend on | chop (>=3 flips/13 wk) | fast fall (21-day, worst 5%) | slow bear (12-mo below 0) | stock-bond corr > 0 (1y) | tsmom12 top-10 falls (peak to low) | 6 months after those lows | tsmom12 losing weeks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `cofall-dbc` | -2.3 | -0.6 | +0.0 | -0.0 | -0.1 | -2.1 | -0.4 | -0.3 | +0.0 | -0.4 | -0.2 |
| *share of days* | *3.9%* | *13.3%* | *13.7%* | *72.9%* | *29.0%* | *5.0%* | *19.9%* | *13.3%* | *21.2%* | *14.6%* | *37.3%* |

## Pass bar

| Book | 1. p < 0.00137 (both) | 2. eras | 3. worst loss | 4. mechanism | 5. beats EW | 6. since 2003 | Verdict |
|---|---|---|---|---|---|---|---|
| `cofall-dbc` | vs 0 -0.006 p 0.845; above bills -0.006 p 0.842 FAIL | 2022-25 ahead False; none behind False FAIL | 35.6% vs 35.6% pass | gate -2.3, stock-bond+ -0.3 %/yr FAIL | 1.07 vs EW 0.88 pass | 1.21 vs 1.22 / EW 1.19 FAIL | fail |

