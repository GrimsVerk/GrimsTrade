# Tries

Every backtest variant run in the idea lab, one row each, appended by `lib/harness.py` the moment
it runs (also when the result is bad). The M1 lane counts these rows in the deflated Sharpe.
Never edit or delete a row.

- `period`: `train` or `heldout`. The held-out period is checked at most once per idea.
- `kind`: `variant` (a strategy configuration that could have been selected), `baseline`
  (benchmark or naive comparator), `robustness` (the same configuration on other data or costs,
  run after the choice was made).
- Sharpe: daily, 365 days/yr, zero risk-free rate (the repo's convention).

| UTC time | Idea | Variant | Kind | Period | From | To | Sharpe | Return | Max DD | Turnover/yr |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
| 2026-11-12 01:46 | baselines | bh-spy | baseline | train | 1994-02-01 | 2025-11-09 | 0.63 | +2395.7% | 55.2% | 0.01 |
| 2026-11-12 01:46 | baselines | bh-btc | baseline | train | 1994-02-01 | 2025-11-09 | 0.82 | +800978.6% | 84.9% | 0.00 |
| 2026-11-12 01:46 | baselines | sixty-forty | baseline | train | 1994-02-01 | 2025-11-09 | 0.76 | +1088.4% | 31.0% | 0.47 |
| 2026-11-12 01:46 | baselines | equal-weight | baseline | train | 1994-02-01 | 2025-11-09 | 0.88 | +20406.3% | 68.8% | 1.25 |
| 2026-11-12 01:46 | baselines | sma200 | baseline | train | 1994-02-01 | 2025-11-09 | 1.01 | +10675.0% | 44.4% | 4.33 |
| 2026-11-12 01:46 | baselines | tsmom12 | baseline | train | 1994-02-01 | 2025-11-09 | 1.05 | +18364.6% | 36.5% | 2.74 |
| 2026-11-12 01:46 | baselines | inverse-vol | baseline | train | 1994-02-01 | 2025-11-09 | 0.85 | +4028.4% | 61.1% | 0.73 |
| 2026-11-12 01:46 | baselines | vol-calm | baseline | train | 1994-02-01 | 2025-11-09 | 0.74 | +2716.4% | 54.8% | 3.38 |
| 2026-11-12 01:46 | baselines | equal-weight@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.48 | +352.5% | 43.1% | 0.32 |
| 2026-11-12 01:46 | baselines | sma200@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.53 | +181.0% | 16.8% | 3.92 |
| 2026-11-12 01:46 | baselines | tsmom12@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.60 | +227.0% | 16.5% | 2.93 |
| 2026-11-12 01:46 | baselines | inverse-vol@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.48 | +214.0% | 36.6% | 0.44 |
| 2026-11-12 01:46 | baselines | vol-calm@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.31 | +86.6% | 36.6% | 1.90 |
| 2026-11-12 01:46 | baselines | equal-weight@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.72 | +640.6% | 91.6% | 3.22 |
| 2026-11-12 01:46 | baselines | sma200@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.50 | +142.3% | 89.8% | 6.11 |
| 2026-11-12 01:46 | baselines | tsmom12@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.54 | +179.5% | 92.4% | 4.62 |
| 2026-11-12 01:46 | baselines | inverse-vol@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.73 | +717.0% | 91.7% | 3.49 |
| 2026-11-12 01:46 | baselines | vol-calm@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.72 | +744.5% | 91.6% | 4.93 |
| 2026-11-12 01:46 | baselines | equal-weight@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.62 | +10067.5% | 57.6% | 0.20 |
| 2026-11-12 01:46 | baselines | sma200@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.75 | +3763.2% | 23.5% | 3.73 |
| 2026-11-12 01:46 | baselines | tsmom12@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.72 | +4377.3% | 25.7% | 2.28 |
| 2026-11-12 01:46 | baselines | inverse-vol@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.60 | +7982.1% | 56.8% | 0.46 |
| 2026-11-12 01:46 | baselines | vol-calm@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.54 | +664.9% | 26.4% | 2.01 |
| 2026-11-12 01:46 | baselines | equal-weight@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.49 | +529.6% | 48.2% | 0.01 |
| 2026-11-12 01:46 | baselines | sma200@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.74 | +663.8% | 20.5% | 2.68 |
| 2026-11-12 01:46 | baselines | tsmom12@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.45 | +277.9% | 34.8% | 1.69 |
| 2026-11-12 01:46 | baselines | vol-calm@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.24 | +47.6% | 27.4% | 2.21 |
| 2026-11-12 01:46 | baselines | equal-weight@N225 | baseline | train | 1994-02-01 | 2025-11-09 | 0.24 | +149.6% | 68.9% | 0.04 |
| 2026-11-12 01:46 | baselines | sma200@N225 | baseline | train | 1994-02-01 | 2025-11-09 | 0.17 | +55.4% | 47.5% | 4.05 |
| 2026-11-12 01:46 | baselines | tsmom12@N225 | baseline | train | 1994-02-01 | 2025-11-09 | 0.37 | +289.6% | 44.2% | 2.44 |
| 2026-11-12 01:46 | baselines | vol-calm@N225 | baseline | train | 1994-02-01 | 2025-11-09 | 0.23 | +57.5% | 29.6% | 2.00 |
| 2026-11-12 01:46 | baselines | equal-weight@FTSE | baseline | train | 1994-02-01 | 2025-11-09 | 0.27 | +181.9% | 52.6% | 0.02 |
| 2026-11-12 01:46 | baselines | sma200@FTSE | baseline | train | 1994-02-01 | 2025-11-09 | 0.15 | +36.1% | 43.0% | 4.67 |
| 2026-11-12 01:46 | baselines | tsmom12@FTSE | baseline | train | 1994-02-01 | 2025-11-09 | 0.28 | +119.4% | 34.3% | 2.81 |
| 2026-11-12 01:46 | baselines | vol-calm@FTSE | baseline | train | 1994-02-01 | 2025-11-09 | 0.13 | +26.7% | 38.9% | 2.05 |
| 2026-11-12 01:46 | baselines | equal-weight@GDAXI | baseline | train | 1994-02-01 | 2025-11-09 | 0.45 | +995.7% | 72.7% | 0.01 |
| 2026-11-12 01:46 | baselines | sma200@GDAXI | baseline | train | 1994-02-01 | 2025-11-09 | 0.53 | +696.2% | 40.9% | 2.63 |
| 2026-11-12 01:46 | baselines | tsmom12@GDAXI | baseline | train | 1994-02-01 | 2025-11-09 | 0.37 | +319.2% | 58.9% | 1.79 |
| 2026-11-12 01:46 | baselines | vol-calm@GDAXI | baseline | train | 1994-02-01 | 2025-11-09 | 0.52 | +369.1% | 23.4% | 1.63 |
