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
| 2026-11-12 01:49 | kelly-shrunk | k0.2 | variant | train | 1994-02-01 | 2025-11-09 | 0.86 | +3195.2% | 60.0% | 0.92 |
| 2026-11-12 01:49 | kelly-shrunk | k0.1 | variant | train | 1994-02-01 | 2025-11-09 | 1.10 | +3162.5% | 35.8% | 0.91 |
| 2026-11-12 01:49 | kelly-shrunk | k0.4 | variant | train | 1994-02-01 | 2025-11-09 | 0.84 | +3462.7% | 61.1% | 0.91 |
| 2026-11-12 01:49 | kelly-shrunk | k0.2@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.48 | +162.1% | 35.1% | 0.76 |
| 2026-11-12 01:49 | kelly-shrunk | k0.2@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.86 | +692.5% | 46.6% | 1.97 |
| 2026-11-12 01:49 | kelly-shrunk | k0.2@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.61 | +7775.3% | 56.6% | 0.63 |
| 2026-11-12 01:49 | baselines | tsmom12-k | baseline | train | 1994-02-01 | 2025-11-09 | 0.96 | +5517.2% | 31.6% | 2.48 |
| 2026-11-12 01:49 | baselines | sma200-k | baseline | train | 1994-02-01 | 2025-11-09 | 0.95 | +4188.8% | 32.7% | 4.06 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.4 | variant | train | 1994-02-01 | 2025-11-09 | 0.70 | +1800.0% | 43.4% | 7.72 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.3 | variant | train | 1994-02-01 | 2025-11-09 | 0.77 | +2702.7% | 45.6% | 4.85 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.5 | variant | train | 1994-02-01 | 2025-11-09 | 0.72 | +1895.0% | 37.0% | 11.42 |
| 2026-11-12 01:49 | baselines | tsmom12-k@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.57 | +177.0% | 16.5% | 2.66 |
| 2026-11-12 01:49 | baselines | sma200-k@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.56 | +163.7% | 16.8% | 3.67 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.4@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.44 | +117.2% | 22.3% | 8.38 |
| 2026-11-12 01:49 | baselines | tsmom12-k@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.41 | +94.1% | 62.8% | 3.92 |
| 2026-11-12 01:49 | baselines | sma200-k@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.34 | +52.3% | 72.0% | 4.84 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.4@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.31 | +30.8% | 79.9% | 9.96 |
| 2026-11-12 01:49 | baselines | tsmom12-k@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.46 | +297.5% | 34.8% | 1.65 |
| 2026-11-12 01:49 | baselines | sma200-k@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.74 | +666.2% | 20.5% | 2.66 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.4@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.63 | +523.1% | 27.2% | 6.66 |
| 2026-11-12 01:49 | baselines | tsmom12-k@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.56 | +4923.7% | 44.2% | 2.22 |
| 2026-11-12 01:49 | baselines | sma200-k@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.41 | +1284.5% | 47.5% | 3.52 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.4@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.50 | +3040.2% | 43.6% | 8.04 |
| 2026-11-12 01:49 | baselines | tsmom12-k@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.35 | +293.7% | 39.1% | 2.70 |
| 2026-11-12 01:49 | baselines | sma200-k@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.22 | +110.5% | 43.0% | 4.48 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.4@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.27 | +170.7% | 52.3% | 8.56 |
| 2026-11-12 01:49 | baselines | tsmom12-k@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.34 | +332.9% | 58.9% | 1.78 |
| 2026-11-12 01:49 | baselines | sma200-k@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.51 | +848.9% | 40.9% | 2.60 |
| 2026-11-12 01:49 | fracdiff-momentum | d0.4@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.25 | +159.5% | 48.2% | 8.79 |
| 2026-11-12 01:49 | drawdown-control | d1.0 | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +7419.0% | 37.2% | 3.54 |
| 2026-11-12 01:49 | drawdown-control | d1.5 | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +11209.7% | 48.1% | 2.60 |
| 2026-11-12 01:49 | drawdown-control | d1.0@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.47 | +121.5% | 17.4% | 2.98 |
| 2026-11-12 01:49 | drawdown-control | d1.0@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.67 | +597.4% | 79.4% | 3.57 |
| 2026-11-12 01:49 | drawdown-control | d1.0@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.58 | +265.3% | 15.5% | 3.86 |
| 2026-11-12 01:49 | baselines | sma200@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.41 | +1295.4% | 47.5% | 3.53 |
| 2026-11-12 01:49 | drawdown-control | d1.0@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.43 | +1041.3% | 38.2% | 3.45 |
| 2026-11-12 01:49 | baselines | sma200@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.24 | +126.8% | 43.0% | 4.55 |
| 2026-11-12 01:49 | drawdown-control | d1.0@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.32 | +179.0% | 27.7% | 3.83 |
| 2026-11-12 01:49 | baselines | sma200@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.55 | +1134.7% | 40.9% | 2.62 |
| 2026-11-12 01:49 | drawdown-control | d1.0@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.53 | +652.4% | 25.7% | 3.62 |
| 2026-11-12 01:49 | universal-portfolio | up | variant | train | 1994-02-01 | 2025-11-09 | 0.85 | +9073.6% | 51.7% | 1.34 |
| 2026-11-12 01:49 | universal-portfolio | up@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.51 | +266.9% | 39.2% | 0.20 |
| 2026-11-12 01:50 | universal-portfolio | up@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.68 | +548.1% | 82.1% | 2.45 |
| 2026-11-12 01:50 | universal-portfolio | up@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.54 | +2140.1% | 51.0% | 0.14 |
