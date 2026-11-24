# trend-tune, Part B: walk-forward tuning of the lookback against fixed `tsmom12`

Card: `trend-tune.md` (Part B). Run 2026-11-18. 20 rows in `tries.md` under idea `trend-tune`
(3 variants, 17 robustness). Tables below are written by `lib/trend_tune_b.py`.

## Verdict (2026-11-18)

**All three procedures fail. Tuning the lookback honestly does not beat leaving it at 12
months; it is slightly worse.** Held-out year not looked at.

| Procedure | Sharpe 1994-2025 | Against `tsmom12` (p) | Since 2003 | Eras ahead | Out of universe (ETFs / coins / indexes) | Bars passed |
|---|---:|---:|---:|---:|---|---:|
| `wf-asset` (a lookback per asset) | 1.01 | -0.04 (0.78) | -0.01 | 1 of 5 | -0.03 / -0.01 / -0.01 | 2 of 7 |
| `wf-pooled` (one lookback, re-chosen yearly) | 1.02 | -0.03 (0.63) | -0.01 | 2 of 5 | -0.06 / -0.02 / +0.01 | 2 of 7 |
| `wf-shrunk` (per asset, shrunk toward 12) | 1.05 | 0.00 | 0.00 | 0 of 5 | -0.00 / -0.00 / -0.03 | 3 of 7 |
| `tsmom12` (fixed) | 1.05 | | | | | |

- `wf-asset` and `wf-pooled` did move (weights 6% and 8% of the book away from `tsmom12` on
  average, mostly to 6 and 9 months) and paid for it with 45% to 60% more trading and no gain.
- `wf-shrunk` never left 12 months on the six assets: the evidence for any other lookback was
  never strong enough once shrunk. It is `tsmom12` to the cent. Where it did move (other ETFs,
  coins, indexes, raw prices) it changed nothing (-0.03 to +0.01).
- Out of universe the differences are small and of both signs; single indexes swing from
  -0.18 (Nikkei, p 0.99) to +0.22 (DAX, p 0.02) for the same procedure, which is what noise
  looks like.
- This is the result Part A predicted: with all of train in view, the best lookbacks are
  worth +0.10 (`results/trend-tune-anatomy.md`, hindsight ceiling), and the best lookback of
  one era says nothing about the next. A tuner that can only look back has nothing to learn.
- How sure: the test measures the difference to `tsmom12` with a standard error of 0.05 to
  0.08, so it would have seen a gain of 0.15 and would probably have missed one of 0.05. What
  it rules out is that tuning the lookback is a large, easy win. Fairly sure of that: three
  procedures, six assets and 18 other markets all say the same.
- The robustness section below is for `wf-shrunk`, as the card requires (largest train
  difference, here zero), so on total-return prices it is the twin against itself.

<!-- tables below this line are written by lib/trend_tune_b.py -->

Train period only (decisions to 2025-11-09), total-return prices, the gym's fills and costs. Each procedure picks lookbacks from 3, 6, 9, 12, 15, 18, 24 months on the first Friday of every year, from bars visible at that moment only, then trades like `tsmom12`. Twin: fixed `tsmom12`.

## The six live assets, 1994-2025

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-asset | 1.01 (0.18) | +16.2% | 16.2% | 35.0% | 3.9 | 72% | 1.22 | 0.24 | 1.45 | 1.45 | 0.88 | -0.04 (p=0.78; -0.13..+0.05) | 1/5 |
| wf-pooled | 1.02 (0.18) | +16.4% | 16.1% | 37.5% | 4.3 | 71% | 1.22 | 0.22 | 1.59 | 1.48 | 0.72 | -0.03 (p=0.63; -0.17..+0.11) | 2/5 |
| wf-shrunk | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | +0.00 (p=1.00; +0.00..+0.00) | 0/5 |
| tsmom12 | 1.05 (0.18) | +17.8% | 17.1% | 36.5% | 2.7 | 76% | 1.34 | 0.19 | 1.55 | 1.50 | 0.88 | - | - |
| equal-weight | 0.88 (0.18) | +18.2% | 21.7% | 68.8% | 1.3 | 100% | 1.35 | 0.02 | 1.67 | 1.55 | 0.67 | -0.17 (p=0.92; -0.36..+0.03) | 3/5 |

Total return inside each stress window:

| Variant | dot-com bust | 2008 crisis | covid crash | 2022 rate shock | crypto winter 2014 | crypto winter 2018 | crypto winter 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| wf-asset | -26% | -2% | -15% | -16% | -6% | -24% | -23% |
| wf-pooled | -25% | +0% | -17% | -15% | -1% | -16% | -22% |
| wf-shrunk | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| tsmom12 | -28% | -4% | -22% | -13% | -6% | -22% | -20% |
| equal-weight | -69% | -20% | -22% | -37% | -17% | -42% | -42% |

## The same runs from 2003 (the review's window)

| Variant | Sharpe | Against `tsmom12` (p) | Growth/yr | Worst loss |
|---|---:|---:|---:|---:|
| wf-asset | 1.18 | -0.01 (0.60) | +19.7% | 34.8% |
| wf-pooled | 1.19 | -0.01 (0.54) | +19.9% | 31.0% |
| wf-shrunk | 1.20 | +0.00 (1.00) | +20.7% | 36.5% |
| tsmom12 | 1.20 | - | +20.7% | 36.5% |
| equal-weight | 1.19 | -0.00 (0.51) | +24.9% | 47.0% |

## What each procedure chose

A row is shown when the choice changed; `-` means the asset was not in the book yet; 12 is `tsmom12`'s own setting.

### `wf-asset`

| Refit (first Friday of) | SPY | QQQ | TLT | GLD | BTC | ETH |
|---|---:|---:|---:|---:|---:|---:|
| 1994 | 6 | - | - | - | - | - |
| 2000 | 6 | 12 | - | - | - | - |
| 2003 | 6 | 12 | 12 | - | - | - |
| 2005 | 6 | 12 | 12 | 12 | - | - |
| 2006 | 6 | 9 | 12 | 12 | - | - |
| 2009 | 6 | 9 | 24 | 12 | - | - |
| 2010 | 6 | 9 | 3 | 12 | - | - |
| 2011 | 9 | 9 | 3 | 24 | - | - |
| 2012 | 9 | 9 | 3 | 24 | 12 | - |
| 2013 | 9 | 9 | 3 | 15 | 12 | - |
| 2014 | 9 | 9 | 24 | 15 | 12 | - |
| 2015 | 6 | 9 | 3 | 15 | 12 | - |
| 2016 | 9 | 9 | 3 | 15 | 12 | - |
| 2017 | 6 | 9 | 3 | 18 | 12 | 12 |
| 2019 | 6 | 9 | 3 | 18 | 6 | 12 |
| 2020 | 6 | 9 | 3 | 24 | 6 | 12 |
| 2021 | 9 | 9 | 3 | 18 | 6 | 12 |
| 2022 | 9 | 9 | 3 | 24 | 6 | 12 |
| 2023 | 9 | 9 | 18 | 18 | 9 | 3 |

Average distance from `tsmom12`'s weights (active share): 6.4% of the book. Trades a year: 3.9 against 2.7.

### `wf-pooled`

| Refit (first Friday of) | SPY | QQQ | TLT | GLD | BTC | ETH |
|---|---:|---:|---:|---:|---:|---:|
| 1994 | 6 | - | - | - | - | - |
| 2000 | 6 | 6 | - | - | - | - |
| 2003 | 6 | 6 | 6 | - | - | - |
| 2005 | 9 | 9 | 9 | 9 | - | - |
| 2012 | 9 | 9 | 9 | 9 | 9 | - |
| 2015 | 6 | 6 | 6 | 6 | 6 | - |
| 2016 | 9 | 9 | 9 | 9 | 9 | - |
| 2017 | 6 | 6 | 6 | 6 | 6 | 6 |
| 2025 | 9 | 9 | 9 | 9 | 9 | 9 |

Average distance from `tsmom12`'s weights (active share): 8.4% of the book. Trades a year: 4.3 against 2.7.

### `wf-shrunk`

| Refit (first Friday of) | SPY | QQQ | TLT | GLD | BTC | ETH |
|---|---:|---:|---:|---:|---:|---:|
| 1994 | 12 | - | - | - | - | - |
| 2000 | 12 | 12 | - | - | - | - |
| 2003 | 12 | 12 | 12 | - | - | - |
| 2005 | 12 | 12 | 12 | 12 | - | - |
| 2012 | 12 | 12 | 12 | 12 | 12 | - |
| 2017 | 12 | 12 | 12 | 12 | 12 | 12 |

Average distance from `tsmom12`'s weights (active share): 0.0% of the book. Trades a year: 2.7 against 2.7.

## Out of universe

#### `wf-asset` on etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-asset@etf | 0.57 (0.20) | +4.6% | 8.5% | 18.7% | 3.6 | 65% | 0.87 | 0.43 | 0.35 | 0.29 | -0.03 (p=0.75; -0.11..+0.05) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

Lookbacks in force at the end: IWM 9, EFA 6, EEM 9, IEF 9, LQD 24, VNQ 6, DBC 3, SLV 9.

#### `wf-asset` on coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-asset@coin | 0.52 (0.34) | +12.3% | 77.1% | 92.4% | 4.8 | 53% | 0.64 | 0.35 | -0.01 (p=0.73; -0.05..+0.02) | 0/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

Lookbacks in force at the end: LTC 3, XRP 6, BCH 3, ETC 12, XLM 12, DASH 12.

#### `wf-asset` on GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-asset@GSPC | 0.46 (0.18) | +4.0% | 9.4% | 25.3% | 3.7 | 64% | 0.28 | 0.65 | +0.02 (p=0.47; -0.21..+0.21) | 2/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

Lookbacks in force at the end: GSPC 6.

#### `wf-asset` on N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-asset@N225 | 0.37 (0.13) | +4.3% | 14.0% | 53.3% | 3.4 | 65% | 0.59 | 0.59 | -0.07 | 0.19 | 0.12 | 0.25 | 0.81 | -0.18 (p=0.99; -0.29..-0.07) | 0/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

Lookbacks in force at the end: N225 12.

#### `wf-asset` on FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-asset@FTSE | 0.27 (0.16) | +2.4% | 11.5% | 50.5% | 3.3 | 67% | 0.57 | 0.93 | 0.05 | -0.07 | -0.39 | 0.20 | -0.10 (p=0.94; -0.22..+0.01) | 2/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

Lookbacks in force at the end: FTSE 12.

#### `wf-asset` on GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-asset@GDAXI | 0.61 (0.17) | +8.0% | 14.2% | 30.5% | 2.9 | 67% | 0.62 | 0.90 | 0.68 | 0.30 | 0.24 | 0.99 | +0.22 (p=0.02; +0.05..+0.40) | 4/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

Lookbacks in force at the end: GDAXI 6.

#### `wf-pooled` on etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-pooled@etf | 0.54 (0.20) | +4.4% | 8.7% | 16.5% | 3.4 | 65% | 0.81 | 0.44 | 0.44 | 0.16 | -0.06 (p=0.97; -0.12..-0.01) | 0/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

Lookbacks in force at the end: IWM 9, EFA 9, EEM 9, IEF 9, LQD 9, VNQ 9, DBC 9, SLV 9.

#### `wf-pooled` on coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-pooled@coin | 0.52 (0.34) | +11.9% | 77.7% | 92.4% | 5.5 | 54% | 0.64 | 0.33 | -0.02 (p=0.61; -0.10..+0.07) | 0/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

Lookbacks in force at the end: LTC 3, XRP 3, BCH 3, ETC 3, XLM 3, DASH 3.

#### `wf-pooled` on idx, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@idx (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-pooled@idx | 0.73 (0.13) | +5.6% | 8.0% | 29.5% | 4.7 | 66% | 0.92 | 1.01 | 1.17 | 0.42 | 0.30 | 0.21 | 0.82 | +0.01 (p=0.47; -0.14..+0.15) | 4/7 |
| tsmom12@idx | 0.72 (0.13) | +6.1% | 8.8% | 25.7% | 2.3 | 70% | 0.76 | 0.97 | 1.10 | 0.52 | 0.37 | 0.33 | 0.79 | - | - |
| equal-weight@idx | 0.62 (0.13) | +7.5% | 13.1% | 57.6% | 0.2 | 100% | 0.71 | 0.97 | 1.11 | -0.05 | 0.66 | 0.62 | 0.95 | -0.10 (p=0.84; -0.27..+0.07) | 5/7 |

Lookbacks in force at the end: GSPC 6, N225 6, FTSE 6, GDAXI 6.

#### `wf-shrunk` on etf, from 2001-05-27

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@etf (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk@etf | 0.60 (0.20) | +4.9% | 8.6% | 17.1% | 3.1 | 65% | 0.81 | 0.41 | 0.42 | 0.65 | -0.00 (p=0.57; -0.04..+0.03) | 1/4 |
| tsmom12@etf | 0.60 (0.20) | +5.0% | 8.7% | 16.5% | 2.9 | 65% | 0.81 | 0.44 | 0.44 | 0.59 | - | - |
| equal-weight@etf | 0.48 (0.20) | +6.4% | 15.1% | 43.1% | 0.3 | 100% | 0.41 | 0.46 | 0.76 | 0.52 | -0.12 (p=0.76; -0.39..+0.15) | 2/4 |

Lookbacks in force at the end: IWM 12, EFA 6, EEM 12, IEF 12, LQD 12, VNQ 12, DBC 3, SLV 12.

#### `wf-shrunk` on coin, from 2017-08-18

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2017-21 | 2022-25 | dSharpe vs tsmom12@coin (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk@coin | 0.53 (0.34) | +13.3% | 76.4% | 93.0% | 5.1 | 55% | 0.64 | 0.38 | -0.00 (p=0.54; -0.05..+0.05) | 1/2 |
| tsmom12@coin | 0.54 (0.34) | +13.3% | 77.4% | 92.4% | 4.6 | 55% | 0.64 | 0.40 | - | - |
| equal-weight@coin | 0.72 (0.34) | +27.5% | 95.4% | 91.6% | 3.2 | 100% | 0.89 | 0.47 | +0.19 (p=0.12; -0.06..+0.46) | 2/2 |

Lookbacks in force at the end: LTC 3, XRP 12, BCH 12, ETC 12, XLM 12, DASH 12.

#### `wf-shrunk` on GSPC, from 1962-01-02

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | dSharpe vs tsmom12@GSPC (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk@GSPC | 0.33 (0.19) | +2.9% | 10.6% | 33.2% | 3.9 | 64% | 0.14 | 0.49 | -0.12 (p=0.90; -0.28..+0.03) | 0/2 |
| tsmom12@GSPC | 0.45 (0.19) | +4.4% | 11.0% | 34.8% | 1.7 | 69% | 0.26 | 0.62 | - | - |
| equal-weight@GSPC | 0.49 (0.18) | +6.1% | 14.1% | 48.2% | 0.0 | 100% | 0.26 | 0.74 | +0.05 (p=0.38; -0.18..+0.25) | 2/2 |

Lookbacks in force at the end: GSPC 12.

#### `wf-shrunk` on N225, from 1966-01-06

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1962-79 | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@N225 (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | +0.00 (p=1.00; +0.00..+0.00) | 0/7 |
| tsmom12@N225 | 0.55 (0.13) | +6.7% | 13.5% | 44.2% | 2.2 | 65% | 0.77 | 0.72 | 0.35 | 0.33 | 0.24 | 0.54 | 0.81 | - | - |
| equal-weight@N225 | 0.40 (0.13) | +6.1% | 20.1% | 81.9% | 0.0 | 100% | 0.81 | 0.47 | 0.17 | -0.10 | 0.49 | 0.54 | 0.79 | -0.15 (p=0.94; -0.31..+0.01) | 3/7 |

Lookbacks in force at the end: N225 12.

#### `wf-shrunk` on FTSE, from 1985-01-03

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@FTSE (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk@FTSE | 0.34 (0.16) | +3.3% | 11.8% | 39.1% | 2.9 | 72% | 0.51 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | -0.03 (p=0.93; -0.08..+0.01) | 3/6 |
| tsmom12@FTSE | 0.37 (0.16) | +3.7% | 11.8% | 39.1% | 2.7 | 71% | 0.64 | 0.72 | 0.36 | -0.07 | -0.02 | 0.20 | - | - |
| equal-weight@FTSE | 0.39 (0.16) | +5.3% | 17.1% | 52.6% | 0.0 | 100% | 0.82 | 0.86 | -0.01 | 0.33 | 0.12 | 0.64 | +0.01 (p=0.43; -0.18..+0.20) | 5/6 |

Lookbacks in force at the end: FTSE 12.

#### `wf-shrunk` on GDAXI, from 1988-12-30

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1980-93 | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12@GDAXI (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk@GDAXI | 0.41 (0.17) | +5.2% | 15.1% | 54.6% | 3.1 | 68% | 0.62 | 0.68 | 0.49 | 0.25 | -0.52 | 0.99 | +0.02 (p=0.40; -0.09..+0.13) | 2/6 |
| tsmom12@GDAXI | 0.40 (0.17) | +5.0% | 15.1% | 58.9% | 1.8 | 69% | 0.62 | 0.68 | 0.46 | 0.42 | -0.47 | 0.44 | - | - |
| equal-weight@GDAXI | 0.47 (0.17) | +8.1% | 21.8% | 72.7% | 0.0 | 100% | 0.63 | 1.01 | 0.08 | 0.55 | 0.43 | 0.70 | +0.07 (p=0.30; -0.14..+0.28) | 5/6 |

Lookbacks in force at the end: GDAXI 6.

## Pass bar (each procedure judged alone)

### `wf-asset`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.033 (difference -0.04, p = 0.78)
- FAIL: 2. Ahead of `tsmom12` in at least 4 of 5 eras (1 of 5)
- PASS: 3. Max drawdown not more than 5 points worse (35.0% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.03, coin -0.01, idx -0.01)
- PASS: 5. Beats equal weight on Sharpe (1.01 vs 0.88)
- FAIL: 6. Not behind `tsmom12` since 2003 (difference -0.01)
- FAIL: 7. Deflation: the difference beats the best of 3 unskilled tries (-0.04 against +0.05 for 3 tries and +0.10 for 21; standard error of the difference 0.05)

**FAILS train.**

### `wf-pooled`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.033 (difference -0.03, p = 0.63)
- FAIL: 2. Ahead of `tsmom12` in at least 4 of 5 eras (2 of 5)
- PASS: 3. Max drawdown not more than 5 points worse (37.5% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.06, coin -0.02, idx +0.01)
- PASS: 5. Beats equal weight on Sharpe (1.02 vs 0.88)
- FAIL: 6. Not behind `tsmom12` since 2003 (difference -0.01)
- FAIL: 7. Deflation: the difference beats the best of 3 unskilled tries (-0.03 against +0.07 for 3 tries and +0.16 for 21; standard error of the difference 0.08)

**FAILS train.**

### `wf-shrunk`

- FAIL: 1. Sharpe beats `tsmom12` with p < 0.033 (difference +0.00, p = 1.00)
- FAIL: 2. Ahead of `tsmom12` in at least 4 of 5 eras (0 of 5)
- PASS: 3. Max drawdown not more than 5 points worse (36.5% vs 36.5%)
- FAIL: 4. Same sign out of universe in at least 2 of 3 sets (etf -0.00, coin -0.00, idx -0.03)
- PASS: 5. Beats equal weight on Sharpe (1.05 vs 0.88)
- PASS: 6. Not behind `tsmom12` since 2003 (difference +0.00)
- FAIL: 7. Deflation: the difference beats the best of 3 unskilled tries (+0.00 against +0.00 for 3 tries and +0.00 for 21; standard error of the difference 0.00)

**FAILS train.**

## Robustness of the procedure with the largest train difference (`wf-shrunk`)

Raw prices (no dividends, what the live scoreboard shows):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12-raw (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk-raw | 0.96 (0.18) | +16.0% | 17.0% | 38.4% | 3.3 | 72% | 1.12 | 0.10 | 1.46 | 1.45 | 0.86 | +0.01 (p=0.23; -0.01..+0.03) | 1/5 |
| tsmom12-raw | 0.95 (0.18) | +15.8% | 17.0% | 37.7% | 2.7 | 72% | 1.12 | 0.10 | 1.40 | 1.45 | 0.88 | - | - |

Double costs (120 bps a round trip in coins, 8 bps in ETFs):

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs tsmom12-2xcost (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| wf-shrunk-2xcost | 1.04 (0.18) | +17.6% | 17.1% | 37.1% | 2.7 | 76% | 1.34 | 0.19 | 1.53 | 1.48 | 0.87 | +0.00 (p=1.00; +0.00..+0.00) | 0/5 |
| tsmom12-2xcost | 1.04 (0.18) | +17.6% | 17.1% | 37.1% | 2.7 | 76% | 1.34 | 0.19 | 1.53 | 1.48 | 0.87 | - | - |

## Held-out year

Not looked at: no procedure passed train.
