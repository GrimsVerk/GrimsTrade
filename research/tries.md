# Tries

Every backtest variant run in the idea lab, one row each, appended by `lib/harness.py` the moment
it runs (also when the result is bad). The M1 lane counts these rows in the deflated Sharpe.
Never edit or delete a row.

- `period`: `train` or `heldout`. The held-out period is checked at most once per idea.
- `kind`: `variant` (a strategy configuration that could have been selected), `baseline`
  (benchmark or naive comparator), `robustness` (the same configuration on other data or costs,
  run after the choice was made).
- `control` (added 2026-11-13, rl-3): a planted-signal control experiment, never a strategy, not
  selectable and not counted as a strategy try (`protocol.md`, "Planted-signal controls").
- `screen` (added 2026-11-13, info-1): a descriptive weekly IC row for one candidate input, no
  backtest, not selectable and not counted as a strategy try; numbers in `results/info-1.md`.
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
| 2026-11-12 01:52 | hmm-regime | hard | variant | train | 1994-02-01 | 2025-11-09 | 0.89 | +7501.8% | 57.3% | 8.81 |
| 2026-11-12 01:52 | hmm-regime | soft | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +6589.8% | 59.2% | 8.21 |
| 2026-11-12 01:53 | hmm-regime | hard@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.46 | +220.4% | 36.6% | 3.88 |
| 2026-11-12 01:53 | hmm-regime | hard@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.63 | +320.6% | 91.6% | 9.88 |
| 2026-11-12 01:53 | hmm-regime | hard@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.33 | +118.9% | 45.9% | 8.95 |
| 2026-11-12 01:53 | baselines | vol-calm@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.41 | +529.8% | 36.6% | 1.87 |
| 2026-11-12 01:53 | baselines | sma200@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.41 | +1295.4% | 47.5% | 3.53 |
| 2026-11-12 01:53 | hmm-regime | hard@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.37 | +836.9% | 44.7% | 11.98 |
| 2026-11-12 01:53 | baselines | vol-calm@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.23 | +104.2% | 40.0% | 2.16 |
| 2026-11-12 01:53 | baselines | sma200@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.24 | +126.8% | 43.0% | 4.55 |
| 2026-11-12 01:53 | hmm-regime | hard@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.31 | +263.6% | 55.2% | 4.33 |
| 2026-11-12 01:53 | baselines | vol-calm@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.52 | +658.4% | 33.0% | 1.59 |
| 2026-11-12 01:53 | baselines | sma200@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.55 | +1134.7% | 40.9% | 2.62 |
| 2026-11-12 01:53 | hmm-regime | hard@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.43 | +587.7% | 48.5% | 6.17 |
| 2026-11-12 01:53 | hawkes-clustering | down2 | variant | train | 1994-02-01 | 2025-11-09 | 0.87 | +12305.9% | 69.3% | 9.07 |
| 2026-11-12 01:53 | hawkes-clustering | down2@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.49 | +255.7% | 36.6% | 6.19 |
| 2026-11-12 01:53 | hawkes-clustering | down2@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.64 | +365.6% | 91.6% | 9.54 |
| 2026-11-12 01:53 | hawkes-clustering | down2@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.67 | +767.9% | 40.8% | 6.35 |
| 2026-11-12 01:53 | baselines | vol-calm@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.41 | +529.8% | 36.6% | 1.87 |
| 2026-11-12 01:53 | hawkes-clustering | down2@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.40 | +1768.2% | 73.8% | 6.70 |
| 2026-11-12 01:53 | baselines | vol-calm@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.23 | +104.2% | 40.0% | 2.16 |
| 2026-11-12 01:53 | hawkes-clustering | down2@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.27 | +210.4% | 53.0% | 6.67 |
| 2026-11-12 01:53 | baselines | vol-calm@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.52 | +658.4% | 33.0% | 1.59 |
| 2026-11-12 01:53 | hawkes-clustering | down2@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.25 | +179.6% | 59.8% | 6.37 |
| 2026-11-12 01:55 | absorption-ratio | six | variant | train | 2002-01-01 | 2025-11-09 | 1.02 | +4806.5% | 45.5% | 1.82 |
| 2026-11-12 01:55 | absorption-ratio | vol-shift | baseline | train | 2002-01-01 | 2025-11-09 | 1.17 | +10494.3% | 37.1% | 2.70 |
| 2026-11-12 01:55 | absorption-ratio | spy@SPY | variant | train | 2002-01-01 | 2025-11-09 | 0.54 | +339.3% | 25.4% | 1.26 |
| 2026-11-12 01:55 | absorption-ratio | vol-shift@SPY | baseline | train | 2002-01-01 | 2025-11-09 | 0.62 | +545.4% | 44.0% | 2.55 |
| 2026-11-12 01:55 | absorption-ratio | six@etf | robustness | train | 2002-01-01 | 2025-11-09 | 0.46 | +157.3% | 20.7% | 1.13 |
| 2026-11-12 01:55 | absorption-ratio | vol-shift@etf | baseline | train | 2002-01-01 | 2025-11-09 | 0.58 | +323.4% | 32.1% | 2.10 |
| 2026-11-12 01:55 | absorption-ratio | six@N225 | robustness | train | 2002-01-01 | 2025-11-09 | 0.34 | +175.6% | 40.6% | 1.27 |
| 2026-11-12 01:55 | absorption-ratio | vol-shift@N225 | baseline | train | 2002-01-01 | 2025-11-09 | 0.45 | +390.0% | 48.2% | 2.58 |
| 2026-11-12 01:55 | absorption-ratio | six@FTSE | robustness | train | 2002-01-01 | 2025-11-09 | 0.13 | +22.2% | 41.2% | 1.28 |
| 2026-11-12 01:55 | absorption-ratio | vol-shift@FTSE | baseline | train | 2002-01-01 | 2025-11-09 | 0.16 | +35.9% | 43.6% | 2.67 |
| 2026-11-12 01:55 | absorption-ratio | six@GDAXI | robustness | train | 2002-01-01 | 2025-11-09 | 0.33 | +149.3% | 44.0% | 1.32 |
| 2026-11-12 01:55 | absorption-ratio | vol-shift@GDAXI | baseline | train | 2002-01-01 | 2025-11-09 | 0.41 | +296.6% | 49.1% | 2.58 |
| 2026-11-12 01:56 | month-end-liquidity | window@SPY | variant | train | 1994-02-01 | 2025-11-09 | 0.56 | +459.0% | 18.9% | 24.01 |
| 2026-11-12 01:56 | month-end-liquidity | constant@SPY | baseline | train | 1994-02-01 | 2025-11-09 | 0.63 | +234.8% | 22.0% | 0.14 |
| 2026-11-12 01:56 | month-end-liquidity | window@QQQ | variant | train | 2000-03-10 | 2025-11-09 | 0.34 | +187.2% | 46.9% | 23.99 |
| 2026-11-12 01:56 | month-end-liquidity | constant@QQQ | baseline | train | 2000-03-10 | 2025-11-09 | 0.41 | +131.8% | 40.4% | 0.24 |
| 2026-11-12 01:56 | month-end-liquidity | window@TLT | variant | train | 2003-07-31 | 2025-11-09 | 0.15 | +21.5% | 25.7% | 24.02 |
| 2026-11-12 01:56 | month-end-liquidity | constant@TLT | baseline | train | 2003-07-31 | 2025-11-09 | 0.32 | +38.7% | 19.3% | 0.10 |
| 2026-11-12 01:56 | month-end-liquidity | window@IWM | robustness | train | 2001-05-27 | 2025-11-09 | 0.41 | +214.0% | 25.1% | 24.00 |
| 2026-11-12 01:56 | month-end-liquidity | constant@IWM | baseline | train | 2001-05-27 | 2025-11-09 | 0.44 | +121.1% | 23.2% | 0.21 |
| 2026-11-12 01:56 | month-end-liquidity | window@EFA | robustness | train | 2002-08-28 | 2025-11-09 | 0.41 | +160.1% | 26.4% | 24.00 |
| 2026-11-12 01:56 | month-end-liquidity | constant@EFA | baseline | train | 2002-08-28 | 2025-11-09 | 0.44 | +92.0% | 25.6% | 0.15 |
| 2026-11-12 01:56 | month-end-liquidity | window@EEM | robustness | train | 2004-04-14 | 2025-11-09 | 0.59 | +459.2% | 34.2% | 24.00 |
| 2026-11-12 01:56 | month-end-liquidity | constant@EEM | baseline | train | 2004-04-14 | 2025-11-09 | 0.37 | +90.4% | 28.2% | 0.22 |
| 2026-11-12 01:56 | month-end-liquidity | window@IEF | robustness | train | 2003-07-31 | 2025-11-09 | 0.42 | +42.4% | 11.4% | 24.03 |
| 2026-11-12 01:56 | month-end-liquidity | constant@IEF | baseline | train | 2003-07-31 | 2025-11-09 | 0.55 | +31.9% | 8.6% | 0.04 |
| 2026-11-12 01:56 | month-end-liquidity | window@LQD | robustness | train | 2003-07-31 | 2025-11-09 | 0.51 | +70.2% | 11.6% | 24.03 |
| 2026-11-12 01:56 | month-end-liquidity | constant@LQD | baseline | train | 2003-07-31 | 2025-11-09 | 0.56 | +40.9% | 9.1% | 0.04 |
| 2026-11-12 01:56 | month-end-liquidity | window@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.81 | +568.1% | 28.4% | 24.00 |
| 2026-11-12 01:56 | month-end-liquidity | constant@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.50 | +101.4% | 19.3% | 0.11 |
| 2026-11-12 01:56 | month-end-liquidity | window@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.50 | +2088.5% | 38.9% | 23.99 |
| 2026-11-12 01:56 | month-end-liquidity | constant@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.40 | +350.7% | 38.5% | 0.17 |
| 2026-11-12 01:56 | month-end-liquidity | window@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.72 | +1296.6% | 20.7% | 24.00 |
| 2026-11-12 01:56 | month-end-liquidity | constant@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.38 | +133.3% | 21.2% | 0.12 |
| 2026-11-12 01:56 | month-end-liquidity | window@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.64 | +1321.9% | 33.0% | 24.00 |
| 2026-11-12 01:56 | month-end-liquidity | constant@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.47 | +225.9% | 33.2% | 0.18 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@SPY | variant | train | 1994-02-01 | 2025-11-09 | 0.50 | +106.6% | 11.8% | 7.88 |
| 2026-11-12 01:56 | dip-rsi2 | constant@SPY | baseline | train | 1994-02-01 | 2025-11-09 | 0.65 | +20.2% | 3.3% | 0.01 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@QQQ | variant | train | 2000-03-10 | 2025-11-09 | 0.32 | +60.4% | 16.5% | 7.96 |
| 2026-11-12 01:56 | dip-rsi2 | constant@QQQ | baseline | train | 2000-03-10 | 2025-11-09 | 0.42 | +14.9% | 7.0% | 0.02 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@IWM | robustness | train | 2001-05-27 | 2025-11-09 | 0.41 | +58.0% | 15.0% | 7.90 |
| 2026-11-12 01:56 | dip-rsi2 | constant@IWM | baseline | train | 2001-05-27 | 2025-11-09 | 0.44 | +14.1% | 3.9% | 0.01 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@EFA | robustness | train | 2002-08-28 | 2025-11-09 | 0.35 | +35.4% | 9.4% | 6.98 |
| 2026-11-12 01:56 | dip-rsi2 | constant@EFA | baseline | train | 2002-08-28 | 2025-11-09 | 0.43 | +10.2% | 4.0% | 0.01 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@EEM | robustness | train | 2004-04-14 | 2025-11-09 | 0.19 | +19.0% | 11.2% | 6.87 |
| 2026-11-12 01:56 | dip-rsi2 | constant@EEM | baseline | train | 2004-04-14 | 2025-11-09 | 0.35 | +9.1% | 3.8% | 0.01 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.19 | +18.0% | 22.0% | 10.31 |
| 2026-11-12 01:56 | dip-rsi2 | constant@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.52 | +17.0% | 4.2% | 0.01 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.19 | +54.5% | 18.8% | 7.01 |
| 2026-11-12 01:56 | dip-rsi2 | constant@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.42 | +27.1% | 5.6% | 0.01 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.20 | +29.7% | 12.4% | 7.14 |
| 2026-11-12 01:56 | dip-rsi2 | constant@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.39 | +13.8% | 3.3% | 0.01 |
| 2026-11-12 01:56 | dip-rsi2 | rsi2@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.26 | +51.1% | 17.1% | 7.27 |
| 2026-11-12 01:56 | dip-rsi2 | constant@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.48 | +20.1% | 5.3% | 0.01 |
| 2026-11-12 02:00 | vol-target | t40 | variant | train | 1994-02-01 | 2025-11-09 | 0.87 | +6723.0% | 66.5% | 1.94 |
| 2026-11-12 02:00 | vol-target | t25 | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +4459.8% | 57.8% | 1.70 |
| 2026-11-12 02:00 | vol-target | t40@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.52 | +352.1% | 36.8% | 0.43 |
| 2026-11-12 02:00 | vol-target | t40@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.80 | +758.7% | 57.9% | 5.56 |
| 2026-11-12 02:00 | vol-target | t40@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.62 | +9100.7% | 58.3% | 0.32 |
| 2026-11-12 02:00 | ensemble-tsmom | e4 | variant | train | 1994-02-01 | 2025-11-09 | 1.10 | +11319.4% | 35.8% | 5.28 |
| 2026-11-12 02:00 | ensemble-tsmom | e4@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.62 | +196.8% | 15.8% | 5.63 |
| 2026-11-12 02:00 | ensemble-tsmom | e4@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.68 | +621.6% | 83.1% | 7.59 |
| 2026-11-12 02:00 | ensemble-tsmom | e4@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.55 | +285.2% | 23.4% | 5.32 |
| 2026-11-12 02:00 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-12 02:00 | baselines | sma200@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.41 | +1295.4% | 47.5% | 3.53 |
| 2026-11-12 02:00 | ensemble-tsmom | e4@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.53 | +2502.5% | 34.3% | 5.56 |
| 2026-11-12 02:00 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-12 02:00 | baselines | sma200@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.24 | +126.8% | 43.0% | 4.55 |
| 2026-11-12 02:00 | ensemble-tsmom | e4@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.25 | +125.2% | 42.3% | 6.03 |
| 2026-11-12 02:00 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-12 02:00 | baselines | sma200@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.55 | +1134.7% | 40.9% | 2.62 |
| 2026-11-12 02:00 | ensemble-tsmom | e4@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.57 | +917.5% | 28.7% | 5.14 |
| 2026-11-12 02:00 | trend-vol | tv40 | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +5131.6% | 25.7% | 2.91 |
| 2026-11-12 02:00 | trend-vol | tv40@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.61 | +228.1% | 16.5% | 2.97 |
| 2026-11-12 02:00 | trend-vol | tv40@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.64 | +248.9% | 59.0% | 4.61 |
| 2026-11-12 02:00 | trend-vol | tv40@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.46 | +284.6% | 33.6% | 1.69 |
| 2026-11-12 02:00 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-12 02:00 | trend-vol | tv40@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.55 | +4550.7% | 44.2% | 2.30 |
| 2026-11-12 02:00 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-12 02:00 | trend-vol | tv40@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.38 | +372.2% | 36.0% | 2.71 |
| 2026-11-12 02:00 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-12 02:00 | trend-vol | tv40@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.40 | +490.7% | 58.9% | 1.78 |
| 2026-11-12 02:01 | robustness | equal-weight-raw | robustness | train | 1994-02-01 | 2025-11-09 | 0.82 | +13224.7% | 69.3% | 1.28 |
| 2026-11-12 02:01 | robustness | tsmom12-raw | robustness | train | 1994-02-01 | 2025-11-09 | 0.95 | +10638.4% | 37.7% | 2.73 |
| 2026-11-12 02:01 | robustness | sma200-raw | robustness | train | 1994-02-01 | 2025-11-09 | 0.96 | +8005.7% | 45.4% | 4.21 |
| 2026-11-12 02:01 | robustness | ensemble-tsmom-raw | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +8122.7% | 35.8% | 5.32 |
| 2026-11-12 02:01 | robustness | trend-vol-raw | robustness | train | 1994-02-01 | 2025-11-09 | 0.91 | +2988.5% | 23.6% | 3.03 |
| 2026-11-12 02:01 | robustness | equal-weight-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 0.88 | +19557.5% | 68.8% | 1.27 |
| 2026-11-12 02:01 | robustness | tsmom12-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +17327.1% | 37.1% | 2.74 |
| 2026-11-12 02:01 | robustness | sma200-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 0.99 | +9763.3% | 44.6% | 4.32 |
| 2026-11-12 02:01 | robustness | ensemble-tsmom-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.08 | +10192.6% | 36.0% | 5.29 |
| 2026-11-12 02:01 | robustness | trend-vol-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.02 | +4792.1% | 25.7% | 2.91 |
| 2026-11-12 02:03 | crypto-alone | equal-weight@BTC | baseline | train | 2013-01-01 | 2025-11-09 | 1.29 | +800978.6% | 84.9% | 0.00 |
| 2026-11-12 02:03 | crypto-alone | sma200@BTC | baseline | train | 2013-01-01 | 2025-11-09 | 1.38 | +876037.1% | 71.0% | 2.23 |
| 2026-11-12 02:03 | crypto-alone | tsmom12@BTC | baseline | train | 2013-01-01 | 2025-11-09 | 1.30 | +541657.3% | 80.5% | 0.41 |
| 2026-11-12 02:03 | crypto-alone | e4@BTC | robustness | train | 2013-01-01 | 2025-11-09 | 1.43 | +766603.9% | 70.3% | 4.92 |
| 2026-11-12 02:03 | crypto-alone | t40@BTC | robustness | train | 2013-01-01 | 2025-11-09 | 1.24 | +39226.2% | 68.5% | 4.62 |
| 2026-11-12 02:03 | crypto-alone | tv40@BTC | robustness | train | 2013-01-01 | 2025-11-09 | 1.26 | +21340.8% | 54.3% | 3.98 |
| 2026-11-12 02:03 | crypto-alone | equal-weight@ETH | baseline | train | 2017-05-19 | 2025-11-09 | 0.86 | +2071.1% | 94.0% | 0.01 |
| 2026-11-12 02:03 | crypto-alone | sma200@ETH | baseline | train | 2017-05-19 | 2025-11-09 | 0.74 | +894.8% | 93.4% | 2.62 |
| 2026-11-12 02:03 | crypto-alone | tsmom12@ETH | baseline | train | 2017-05-19 | 2025-11-09 | 0.83 | +1691.2% | 91.8% | 1.45 |
| 2026-11-12 02:03 | crypto-alone | e4@ETH | robustness | train | 2017-05-19 | 2025-11-09 | 0.93 | +2753.6% | 83.3% | 5.41 |
| 2026-11-12 02:03 | crypto-alone | t40@ETH | robustness | train | 2017-05-19 | 2025-11-09 | 0.82 | +906.6% | 72.0% | 5.78 |
| 2026-11-12 02:03 | crypto-alone | tv40@ETH | robustness | train | 2017-05-19 | 2025-11-09 | 0.71 | +420.5% | 69.4% | 5.01 |
| 2026-11-12 02:06 | trend-to-safe | safe | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +19117.7% | 32.9% | 5.55 |
| 2026-11-12 02:06 | trend-to-safe | safe@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.68 | +326.7% | 22.0% | 5.58 |
| 2026-11-12 02:06 | crypto-slot-size | c05 | variant | train | 2013-01-01 | 2025-11-09 | 1.36 | +737.1% | 30.5% | 0.54 |
| 2026-11-12 02:06 | crypto-slot-size | c10 | variant | train | 2013-01-01 | 2025-11-09 | 1.39 | +1642.9% | 37.3% | 0.88 |
| 2026-11-12 02:06 | crypto-slot-size | c00 | variant | train | 2013-01-01 | 2025-11-09 | 1.05 | +288.5% | 25.2% | 0.36 |
| 2026-11-12 02:17 | ml-linear | logit | variant | train | 1994-02-01 | 2025-11-09 | 0.89 | +9686.7% | 58.5% | 3.48 |
| 2026-11-12 02:17 | ml-linear | logit-hard | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +19826.6% | 68.8% | 1.31 |
| 2026-11-12 02:17 | ml-linear | ridge | variant | train | 1994-02-01 | 2025-11-09 | 0.84 | +9436.9% | 60.6% | 2.13 |
| 2026-11-12 02:17 | ml-linear | logit@etf | robustness | train | 2007-01-05 | 2025-11-09 | 0.37 | +115.4% | 42.5% | 1.46 |
| 2026-11-12 02:17 | ml-linear | logit@coin | robustness | train | 2023-01-06 | 2025-11-09 | -0.06 | -0.7% | 4.2% | 0.84 |
| 2026-11-12 02:17 | ml-linear | logit@idx | robustness | train | 1974-01-04 | 2025-11-09 | 0.62 | +2441.0% | 36.4% | 2.97 |
| 2026-11-12 02:18 | ml-gbm | gbm | variant | train | 1994-02-01 | 2025-11-09 | 0.81 | +3338.5% | 46.0% | 9.62 |
| 2026-11-12 02:18 | ml-gbm | gbm-hard | variant | train | 1994-02-01 | 2025-11-09 | 0.72 | +3397.3% | 53.1% | 6.82 |
| 2026-11-12 02:18 | ml-gbm | gbm-reg | variant | train | 1994-02-01 | 2025-11-09 | 0.78 | +3829.1% | 46.9% | 7.95 |
| 2026-11-12 02:18 | ml-gbm | gbm-cv | variant | train | 1994-02-01 | 2025-11-09 | 0.79 | +4979.0% | 58.2% | 4.22 |
| 2026-11-12 02:18 | ml-gbm | gbm-d1 | variant | train | 1994-02-01 | 2025-11-09 | 0.72 | +2650.0% | 53.3% | 4.69 |
| 2026-11-12 02:19 | ml-gbm | gbm-d6 | variant | train | 1994-02-01 | 2025-11-09 | 0.78 | +2705.3% | 45.6% | 11.76 |
| 2026-11-12 02:19 | ml-gbm | gbm-n25 | variant | train | 1994-02-01 | 2025-11-09 | 0.75 | +3165.3% | 49.4% | 6.41 |
| 2026-11-12 02:19 | ml-gbm | gbm-n400 | variant | train | 1994-02-01 | 2025-11-09 | 0.76 | +2462.0% | 52.8% | 12.77 |
| 2026-11-12 02:19 | ml-gbm | gbm-leaf20 | variant | train | 1994-02-01 | 2025-11-09 | 0.86 | +4099.9% | 47.3% | 9.39 |
| 2026-11-12 02:19 | ml-gbm | gbm@etf | robustness | train | 2007-01-05 | 2025-11-09 | 0.23 | +45.1% | 34.0% | 10.39 |
| 2026-11-12 02:19 | ml-gbm | gbm@coin | robustness | train | 2023-01-06 | 2025-11-09 | 0.78 | +95.9% | 35.1% | 11.46 |
| 2026-11-12 02:19 | ml-gbm | gbm@idx | robustness | train | 1974-01-04 | 2025-11-09 | 0.59 | +1403.2% | 41.1% | 9.23 |
| 2026-11-12 02:20 | ml-filter | meta-gbm | variant | train | 1994-02-01 | 2025-11-09 | 0.73 | +1302.2% | 28.3% | 8.03 |
| 2026-11-12 02:20 | ml-filter | meta-logit | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +5283.8% | 29.4% | 3.40 |
| 2026-11-12 02:20 | ml-filter | and-gbm | variant | train | 1994-02-01 | 2025-11-09 | 0.86 | +2662.5% | 29.6% | 7.01 |
| 2026-11-12 02:20 | ml-filter | meta-gbm@etf | robustness | train | 2007-01-05 | 2025-11-09 | 0.38 | +56.2% | 17.2% | 8.20 |
| 2026-11-12 02:20 | ml-filter | meta-gbm@coin | robustness | train | 2023-01-06 | 2025-11-09 | 0.17 | +2.8% | 39.6% | 10.59 |
| 2026-11-12 02:20 | ml-filter | meta-gbm@idx | robustness | train | 1974-01-04 | 2025-11-09 | 0.62 | +872.8% | 21.7% | 8.10 |
| 2026-11-12 02:27 | ml-sizing | gbm-prop | variant | train | 1994-02-01 | 2025-11-09 | 0.75 | +1209.2% | 36.6% | 9.17 |
| 2026-11-12 02:27 | ml-sizing | logit-prop | variant | train | 1994-02-01 | 2025-11-09 | 0.75 | +1198.7% | 46.2% | 2.51 |
| 2026-11-12 02:27 | ml-sizing | gbm-low | variant | train | 1994-02-01 | 2025-11-09 | 0.80 | +3612.7% | 52.6% | 9.68 |
| 2026-11-12 02:27 | ml-sizing | logit-low | variant | train | 1994-02-01 | 2025-11-09 | 0.82 | +3678.6% | 37.7% | 6.60 |
| 2026-11-12 02:27 | ml-sizing | gbm-reg-prop | variant | train | 1994-02-01 | 2025-11-09 | 0.68 | +1430.3% | 45.0% | 8.41 |
| 2026-11-12 02:27 | ml-sizing | ridge-prop | variant | train | 1994-02-01 | 2025-11-09 | 0.82 | +1406.4% | 39.7% | 1.39 |
| 2026-11-12 02:27 | ml-sizing | gbm-prop@etf | robustness | train | 2007-01-05 | 2025-11-09 | 0.19 | +24.5% | 24.1% | 9.81 |
| 2026-11-12 02:27 | ml-sizing | gbm-prop@coin | robustness | train | 2023-01-06 | 2025-11-09 | 0.76 | +83.4% | 32.8% | 11.44 |
| 2026-11-12 02:27 | ml-sizing | gbm-prop@idx | robustness | train | 1974-01-04 | 2025-11-09 | 0.61 | +773.3% | 26.9% | 9.34 |
| 2026-11-12 06:34 | ml-payoff | gbm-pay | variant | train | 1994-02-01 | 2025-11-09 | 0.68 | +2382.6% | 55.0% | 6.52 |
| 2026-11-12 06:34 | ml-payoff | logit-pay | variant | train | 1994-02-01 | 2025-11-09 | 0.77 | +5962.7% | 52.7% | 2.30 |
| 2026-11-12 06:34 | ml-payoff | tree-pay | variant | train | 1994-02-01 | 2025-11-09 | 0.67 | +2784.1% | 58.7% | 3.21 |
| 2026-11-12 06:34 | ml-payoff | gbm-raw | variant | train | 1994-02-01 | 2025-11-09 | 0.74 | +3348.9% | 55.7% | 5.65 |
| 2026-11-12 06:34 | ml-payoff | gbm-pay@etf | robustness | train | 2007-01-05 | 2025-11-09 | 0.21 | +40.8% | 38.9% | 11.65 |
| 2026-11-12 06:34 | ml-payoff | gbm-pay@coin | robustness | train | 2023-01-06 | 2025-11-09 | 0.77 | +102.8% | 41.6% | 10.07 |
| 2026-11-12 06:34 | ml-payoff | gbm-pay@idx | robustness | train | 1974-01-04 | 2025-11-09 | 0.61 | +2222.5% | 43.8% | 7.05 |
| 2026-11-12 06:38 | ml-pooled | gbm-pool | variant | train | 1994-02-01 | 2025-11-09 | 0.70 | +1994.0% | 50.0% | 6.85 |
| 2026-11-12 06:38 | ml-pooled | logit-pool | variant | train | 1994-02-01 | 2025-11-09 | 0.92 | +6540.6% | 37.3% | 3.08 |
| 2026-11-12 06:38 | ml-pooled | gbm-pool-low | variant | train | 1994-02-01 | 2025-11-09 | 0.68 | +2197.0% | 45.4% | 7.34 |
| 2026-11-12 06:39 | ml-pooled | gbm-pool@etf | robustness | train | 2007-01-05 | 2025-11-09 | 0.48 | +118.5% | 18.3% | 6.79 |
| 2026-11-12 06:39 | ml-pooled | gbm-pool@coin | robustness | train | 2023-01-06 | 2025-11-09 | 0.50 | +35.9% | 32.1% | 11.17 |
| 2026-11-12 06:39 | ml-pooled | gbm-pool@idx | robustness | train | 1974-01-04 | 2025-11-09 | 0.62 | +1787.1% | 47.6% | 7.75 |
| 2026-11-12 06:46 | ml-weekly | gbm-wk | variant | train | 1994-02-01 | 2025-11-09 | 0.82 | +4057.7% | 45.7% | 11.76 |
| 2026-11-12 06:46 | ml-weekly | logit-wk | variant | train | 1994-02-01 | 2025-11-09 | 0.89 | +9744.1% | 57.1% | 2.14 |
| 2026-11-12 06:46 | ml-weekly | gbm-wk-low | variant | train | 1994-02-01 | 2025-11-09 | 0.83 | +6376.1% | 54.7% | 9.13 |
| 2026-11-12 06:46 | ml-weekly | gbm-wk@etf | robustness | train | 2007-01-05 | 2025-11-09 | 0.24 | +45.9% | 37.4% | 14.58 |
| 2026-11-12 06:46 | ml-weekly | gbm-wk@coin | robustness | train | 2023-01-06 | 2025-11-09 | 1.01 | +111.5% | 23.1% | 18.32 |
| 2026-11-12 06:46 | ml-weekly | gbm-wk@idx | robustness | train | 1974-01-04 | 2025-11-09 | 0.67 | +1988.7% | 31.5% | 12.42 |
| 2026-11-12 07:15 | risk-map | hold-c00 | variant | train | 1994-02-01 | 2025-11-09 | 0.62 | +1536.2% | 68.8% | 0.40 |
| 2026-11-12 07:15 | risk-map | hold-c05 | variant | train | 1994-02-01 | 2025-11-09 | 0.75 | +3464.4% | 68.8% | 0.53 |
| 2026-11-12 07:15 | risk-map | hold-c10 | variant | train | 1994-02-01 | 2025-11-09 | 0.83 | +7242.7% | 68.8% | 0.83 |
| 2026-11-12 07:15 | risk-map | hold-c17 | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +20406.3% | 68.8% | 1.25 |
| 2026-11-12 07:15 | risk-map | tsmom12-c00 | variant | train | 1994-02-01 | 2025-11-09 | 0.79 | +1442.4% | 28.9% | 2.16 |
| 2026-11-12 07:15 | risk-map | tsmom12-c05 | variant | train | 1994-02-01 | 2025-11-09 | 0.96 | +3224.6% | 28.9% | 2.29 |
| 2026-11-12 07:15 | risk-map | tsmom12-c10 | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +6451.9% | 28.9% | 2.50 |
| 2026-11-12 07:15 | risk-map | tsmom12-c17 | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +18364.6% | 36.5% | 2.74 |
| 2026-11-12 07:15 | risk-map | tv60-c00 | variant | train | 1994-02-01 | 2025-11-09 | 0.80 | +1433.3% | 28.8% | 2.16 |
| 2026-11-12 07:15 | risk-map | tv60-c05 | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +2426.2% | 28.8% | 2.28 |
| 2026-11-12 07:15 | risk-map | tv60-c10 | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +3841.3% | 28.8% | 2.53 |
| 2026-11-12 07:15 | risk-map | tv60-c17 | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +7724.8% | 29.8% | 2.96 |
| 2026-11-12 07:15 | risk-map | tv40-c00 | variant | train | 1994-02-01 | 2025-11-09 | 0.83 | +1481.2% | 25.7% | 2.18 |
| 2026-11-12 07:15 | risk-map | tv40-c05 | variant | train | 1994-02-01 | 2025-11-09 | 0.92 | +2185.6% | 25.7% | 2.28 |
| 2026-11-12 07:15 | risk-map | tv40-c10 | variant | train | 1994-02-01 | 2025-11-09 | 0.98 | +3057.9% | 25.7% | 2.52 |
| 2026-11-12 07:15 | risk-map | tv40-c17 | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +5131.6% | 25.7% | 2.91 |
| 2026-11-12 07:15 | risk-map | tv20-c00 | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +1408.5% | 17.9% | 2.47 |
| 2026-11-12 07:15 | risk-map | tv20-c05 | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +1692.5% | 17.9% | 2.44 |
| 2026-11-12 07:15 | risk-map | tv20-c10 | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +1976.1% | 17.9% | 2.47 |
| 2026-11-12 07:15 | risk-map | tv20-c17 | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +2562.0% | 17.9% | 2.56 |
| 2026-11-13 01:44 | yield-curve | curve-and | variant | train | 1994-02-01 | 2025-11-09 | 1.13 | +10254.6% | 29.9% | 2.13 |
| 2026-11-13 01:44 | real-rate | real-and | variant | train | 1994-02-01 | 2025-11-09 | 0.87 | +5014.9% | 33.0% | 2.83 |
| 2026-11-13 01:44 | fed-hiking | hike-and | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +6850.2% | 28.8% | 2.66 |
| 2026-11-13 01:44 | liquidity | m2-and | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +9230.7% | 36.5% | 2.55 |
| 2026-11-13 01:44 | halving | halving-and | variant | train | 1994-02-01 | 2025-11-09 | 1.20 | +31818.9% | 28.9% | 2.67 |
| 2026-11-13 01:44 | credit-spread | spread-and | variant | train | 1994-02-01 | 2025-11-09 | 0.99 | +8477.1% | 38.8% | 2.89 |
| 2026-11-13 01:44 | yield-curve | curve-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +10475.8% | 47.8% | 2.02 |
| 2026-11-13 01:44 | credit-spread | spread-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.80 | +5453.8% | 60.3% | 3.00 |
| 2026-11-13 01:44 | halving | halving-alone | variant | train | 1994-02-01 | 2025-11-09 | 1.28 | +69253.1% | 29.7% | 2.46 |
| 2026-11-13 01:44 | real-rate | real-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.58 | +1989.2% | 68.8% | 2.66 |
| 2026-11-13 01:44 | fed-hiking | hike-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.85 | +8109.0% | 59.4% | 2.29 |
| 2026-11-13 01:44 | liquidity | m2-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.79 | +8918.0% | 68.8% | 2.16 |
| 2026-11-13 01:44 | liquidity | walcl-and | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +5799.8% | 28.9% | 2.26 |
| 2026-11-13 01:44 | halving | halving-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.86 | +1942.9% | 69.5% | 4.29 |
| 2026-11-13 01:44 | yield-curve | curve-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.55 | +139.4% | 16.3% | 2.21 |
| 2026-11-13 01:44 | real-rate | real-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.49 | +132.2% | 17.5% | 2.81 |
| 2026-11-13 01:44 | fed-hiking | hike-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.49 | +139.6% | 16.6% | 2.63 |
| 2026-11-13 01:44 | credit-spread | spread-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.56 | +174.7% | 16.6% | 2.69 |
| 2026-11-13 01:44 | liquidity | m2-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.55 | +175.5% | 16.5% | 2.75 |
| 2026-11-13 01:44 | yield-curve | curve-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.47 | +113.3% | 89.6% | 2.51 |
| 2026-11-13 01:44 | real-rate | real-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.60 | +341.2% | 87.4% | 4.10 |
| 2026-11-13 01:44 | fed-hiking | hike-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.68 | +622.0% | 71.6% | 3.99 |
| 2026-11-13 01:44 | credit-spread | spread-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.48 | +96.7% | 91.5% | 4.61 |
| 2026-11-13 01:44 | yield-curve | curve-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.27 | +90.3% | 34.8% | 1.61 |
| 2026-11-13 01:44 | liquidity | m2-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.54 | +195.2% | 92.4% | 3.72 |
| 2026-11-13 01:44 | real-rate | real-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.49 | +287.6% | 33.2% | 2.34 |
| 2026-11-13 01:44 | fed-hiking | hike-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.72 | +386.6% | 14.2% | 2.14 |
| 2026-11-13 01:44 | credit-spread | spread-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.41 | +227.6% | 34.8% | 2.19 |
| 2026-11-13 01:44 | liquidity | m2-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.28 | +96.8% | 33.6% | 1.94 |
| 2026-11-13 01:44 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 01:44 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 01:44 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 01:44 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 01:44 | yield-curve | curve-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.54 | +2872.5% | 38.0% | 1.50 |
| 2026-11-13 01:44 | real-rate | real-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.45 | +1333.8% | 40.0% | 2.47 |
| 2026-11-13 01:44 | fed-hiking | hike-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.39 | +747.5% | 49.0% | 2.03 |
| 2026-11-13 01:44 | credit-spread | spread-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.56 | +4217.6% | 47.4% | 2.10 |
| 2026-11-13 01:44 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 01:44 | liquidity | m2-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.52 | +2686.2% | 42.4% | 1.82 |
| 2026-11-13 01:44 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 01:44 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 01:44 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 01:44 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 01:44 | yield-curve | curve-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.36 | +242.4% | 42.0% | 1.88 |
| 2026-11-13 01:44 | real-rate | real-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.30 | +183.3% | 39.1% | 2.59 |
| 2026-11-13 01:44 | fed-hiking | hike-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.34 | +216.7% | 25.9% | 2.20 |
| 2026-11-13 01:44 | credit-spread | spread-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.29 | +180.0% | 37.8% | 2.41 |
| 2026-11-13 01:44 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 01:44 | liquidity | m2-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.31 | +197.5% | 42.3% | 2.37 |
| 2026-11-13 01:44 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 01:44 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 01:44 | yield-curve | curve-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.51 | +557.4% | 34.8% | 1.33 |
| 2026-11-13 01:44 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 01:44 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 01:44 | fed-hiking | hike-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.28 | +177.3% | 52.0% | 1.67 |
| 2026-11-13 01:44 | real-rate | real-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.27 | +162.8% | 53.3% | 2.26 |
| 2026-11-13 01:44 | credit-spread | spread-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.46 | +595.0% | 49.4% | 1.73 |
| 2026-11-13 01:44 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 01:44 | liquidity | m2-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.24 | +133.3% | 57.6% | 1.87 |
| 2026-11-13 01:45 | halving | halving-and-m12-24 | robustness | train | 1994-02-01 | 2025-11-09 | 1.12 | +13849.3% | 28.9% | 2.46 |
| 2026-11-13 01:45 | halving | halving-and-m24-36 | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +18007.7% | 39.0% | 2.71 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.52 | +2668.9% | 82.9% | 7.47 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.56 | +4022.2% | 80.4% | 9.34 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.59 | +4506.2% | 80.5% | 7.72 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.69 | +12260.0% | 82.9% | 8.02 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.63 | +7072.7% | 78.0% | 6.86 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.61 | +7211.8% | 83.5% | 7.59 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.65 | +9942.1% | 78.7% | 7.37 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.68 | +15977.3% | 81.1% | 7.94 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.58 | +4609.3% | 80.7% | 8.31 |
| 2026-11-13 05:03 | rl-1 | ppo-lin-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.61 | +6459.8% | 76.5% | 7.79 |
| 2026-11-13 05:03 | rl-1 | ppo-lin | variant | train | 2000-01-07 | 2025-11-09 | 0.63 | +7506.0% | 77.3% | 7.02 |
| 2026-11-13 05:03 | rl-1 | ppo-lin@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.51 | +240.9% | 29.0% | 7.87 |
| 2026-11-13 05:03 | rl-1 | ppo-lin@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.60 | +206.7% | 92.1% | 8.44 |
| 2026-11-13 05:03 | rl-1 | ppo-lin@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.37 | +157.2% | 41.6% | 5.45 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.55 | +3730.1% | 86.3% | 9.23 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.58 | +5067.0% | 81.7% | 9.77 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.65 | +8868.0% | 72.5% | 10.17 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.69 | +12889.3% | 79.0% | 8.35 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.64 | +9646.2% | 81.2% | 7.33 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.62 | +8142.6% | 78.0% | 8.18 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.65 | +10598.8% | 80.0% | 9.20 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.64 | +11101.8% | 81.7% | 8.82 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.67 | +14484.1% | 80.9% | 9.64 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.75 | +26613.8% | 79.2% | 6.48 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp | variant | train | 2000-01-07 | 2025-11-09 | 0.66 | +11510.3% | 79.6% | 6.91 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.49 | +301.1% | 39.9% | 15.26 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.64 | +340.2% | 91.6% | 8.03 |
| 2026-11-13 05:03 | rl-1 | ppo-mlp@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.31 | +134.0% | 51.2% | 13.63 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.48 | +616.0% | 66.8% | 7.37 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.37 | +420.3% | 85.0% | 10.27 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.53 | +960.6% | 69.1% | 7.25 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.51 | +777.3% | 60.8% | 9.51 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.46 | +619.7% | 57.2% | 8.50 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.45 | +748.0% | 77.3% | 10.55 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.53 | +1200.1% | 65.8% | 9.53 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.58 | +1508.9% | 59.2% | 8.65 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.49 | +1097.5% | 81.7% | 7.25 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.70 | +3081.8% | 65.5% | 6.95 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd | variant | train | 2000-01-07 | 2025-11-09 | 0.57 | +1219.8% | 60.4% | 7.13 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.39 | +100.2% | 23.3% | 10.94 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.56 | +224.8% | 65.6% | 4.50 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-dd@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.14 | +23.1% | 34.6% | 8.58 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.70 | +17165.6% | 86.7% | 10.08 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.67 | +14758.2% | 83.9% | 8.86 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.69 | +16664.8% | 75.9% | 9.54 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.72 | +19844.0% | 82.5% | 9.39 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.67 | +13576.8% | 81.8% | 7.03 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.64 | +11044.1% | 83.1% | 8.23 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.65 | +12458.8% | 83.8% | 11.47 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.67 | +15266.5% | 81.9% | 10.27 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.69 | +19640.0% | 81.0% | 8.90 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.78 | +38135.0% | 80.3% | 6.52 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px | variant | train | 2000-01-07 | 2025-11-09 | 0.71 | +19730.4% | 82.3% | 6.74 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.52 | +321.1% | 40.6% | 17.11 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.64 | +305.9% | 91.4% | 8.14 |
| 2026-11-13 05:04 | rl-1 | ppo-mlp-px@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.38 | +184.8% | 38.2% | 13.95 |
| 2026-11-13 05:04 | rl-1 | es-lin-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.51 | +2555.1% | 90.8% | 10.95 |
| 2026-11-13 05:04 | rl-1 | es-lin-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.64 | +11976.5% | 82.8% | 13.41 |
| 2026-11-13 05:04 | rl-1 | es-lin-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.56 | +5481.9% | 86.9% | 10.07 |
| 2026-11-13 05:04 | rl-1 | es-lin-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.56 | +5409.7% | 87.7% | 12.20 |
| 2026-11-13 05:04 | rl-1 | es-lin-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.53 | +3311.6% | 85.7% | 10.77 |
| 2026-11-13 05:04 | rl-1 | es-lin-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.54 | +3881.9% | 85.5% | 8.56 |
| 2026-11-13 05:04 | rl-1 | es-lin-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.57 | +6311.3% | 87.9% | 10.85 |
| 2026-11-13 05:04 | rl-1 | es-lin-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.56 | +5207.3% | 87.5% | 10.20 |
| 2026-11-13 05:04 | rl-1 | es-lin-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.59 | +7802.4% | 86.9% | 11.54 |
| 2026-11-13 05:04 | rl-1 | es-lin-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.51 | +2717.4% | 88.8% | 10.24 |
| 2026-11-13 05:04 | rl-1 | es-lin | variant | train | 2000-01-07 | 2025-11-09 | 0.57 | +5864.3% | 86.5% | 9.86 |
| 2026-11-13 05:04 | rl-1 | es-lin@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.41 | +209.8% | 37.9% | 19.27 |
| 2026-11-13 05:04 | rl-1 | es-lin@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.61 | +181.7% | 92.2% | 14.36 |
| 2026-11-13 05:04 | rl-1 | es-lin@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.26 | +106.8% | 52.9% | 14.49 |
| 2026-11-13 05:29 | rl-2 | res-lin-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.97 | +4831.8% | 35.1% | 2.98 |
| 2026-11-13 05:29 | rl-2 | res-lin-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.99 | +5334.8% | 35.6% | 3.14 |
| 2026-11-13 05:29 | rl-2 | res-lin-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.99 | +5167.8% | 34.7% | 2.97 |
| 2026-11-13 05:29 | rl-2 | res-lin-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +4976.0% | 35.7% | 2.95 |
| 2026-11-13 05:29 | rl-2 | res-lin-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.97 | +4901.2% | 35.7% | 2.92 |
| 2026-11-13 05:29 | rl-2 | res-lin-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.99 | +5158.5% | 35.4% | 2.97 |
| 2026-11-13 05:29 | rl-2 | res-lin-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +4944.4% | 35.7% | 3.00 |
| 2026-11-13 05:29 | rl-2 | res-lin-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +5001.2% | 35.5% | 2.97 |
| 2026-11-13 05:29 | rl-2 | res-lin-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +5077.1% | 35.1% | 2.95 |
| 2026-11-13 05:29 | rl-2 | res-lin-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +5003.6% | 35.8% | 2.93 |
| 2026-11-13 05:29 | rl-2 | res-lin | variant | train | 2000-01-07 | 2025-11-09 | 0.98 | +5053.0% | 35.7% | 2.95 |
| 2026-11-13 05:29 | rl-2 | res-lin@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.59 | +241.0% | 20.7% | 3.18 |
| 2026-11-13 05:29 | rl-2 | res-lin@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.54 | +178.4% | 92.4% | 4.61 |
| 2026-11-13 05:29 | rl-2 | res-lin@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.49 | +200.7% | 26.7% | 2.67 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.93 | +3573.2% | 35.0% | 3.17 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.95 | +3953.3% | 35.2% | 3.37 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +4973.2% | 35.2% | 3.41 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.99 | +5281.7% | 35.0% | 3.22 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.99 | +5073.7% | 35.3% | 3.22 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +4924.0% | 35.7% | 3.15 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.97 | +4747.2% | 36.0% | 3.16 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.93 | +3516.9% | 35.3% | 3.13 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.96 | +4242.9% | 34.9% | 3.51 |
| 2026-11-13 05:30 | rl-2 | res-mlp-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.96 | +4403.6% | 36.0% | 3.31 |
| 2026-11-13 05:30 | rl-2 | res-mlp | variant | train | 2000-01-07 | 2025-11-09 | 0.97 | +4498.8% | 35.3% | 3.10 |
| 2026-11-13 05:30 | rl-2 | res-mlp@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.59 | +233.3% | 21.7% | 3.42 |
| 2026-11-13 05:30 | rl-2 | res-mlp@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.53 | +177.8% | 92.4% | 4.62 |
| 2026-11-13 05:30 | rl-2 | res-mlp@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.48 | +190.8% | 27.4% | 2.88 |
| 2026-11-13 05:30 | rl-2 | res-pool-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.96 | +4459.1% | 37.0% | 3.16 |
| 2026-11-13 05:30 | rl-2 | res-pool-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.97 | +4587.2% | 35.8% | 3.13 |
| 2026-11-13 05:30 | rl-2 | res-pool-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.97 | +4584.8% | 36.5% | 3.20 |
| 2026-11-13 05:30 | rl-2 | res-pool-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +4744.8% | 35.6% | 3.13 |
| 2026-11-13 05:30 | rl-2 | res-pool-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.96 | +4267.2% | 36.4% | 3.33 |
| 2026-11-13 05:30 | rl-2 | res-pool-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.96 | +4425.8% | 35.5% | 3.16 |
| 2026-11-13 05:30 | rl-2 | res-pool-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 1.00 | +5080.2% | 33.8% | 3.21 |
| 2026-11-13 05:30 | rl-2 | res-pool-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.93 | +3445.3% | 35.7% | 3.31 |
| 2026-11-13 05:30 | rl-2 | res-pool-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +4555.2% | 34.7% | 3.12 |
| 2026-11-13 05:30 | rl-2 | res-pool-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.94 | +3946.9% | 36.0% | 3.21 |
| 2026-11-13 05:30 | rl-2 | res-pool | variant | train | 2000-01-07 | 2025-11-09 | 0.97 | +4379.2% | 36.4% | 3.04 |
| 2026-11-13 05:30 | rl-2 | res-pool@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.59 | +233.4% | 20.3% | 3.36 |
| 2026-11-13 05:31 | rl-2 | res-pool@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.54 | +188.3% | 92.3% | 4.40 |
| 2026-11-13 05:31 | rl-2 | res-pool@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.47 | +181.3% | 26.9% | 2.82 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s0 | robustness | train | 2000-01-07 | 2025-11-09 | 0.93 | +3509.0% | 35.1% | 3.15 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s1 | robustness | train | 2000-01-07 | 2025-11-09 | 0.91 | +3286.5% | 36.1% | 3.32 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s2 | robustness | train | 2000-01-07 | 2025-11-09 | 0.94 | +3746.3% | 35.4% | 3.10 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s3 | robustness | train | 2000-01-07 | 2025-11-09 | 0.98 | +4945.6% | 35.3% | 2.93 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s4 | robustness | train | 2000-01-07 | 2025-11-09 | 0.97 | +4683.8% | 36.0% | 3.16 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s5 | robustness | train | 2000-01-07 | 2025-11-09 | 0.93 | +3583.0% | 36.2% | 3.36 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s6 | robustness | train | 2000-01-07 | 2025-11-09 | 0.99 | +5172.0% | 35.2% | 3.11 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s7 | robustness | train | 2000-01-07 | 2025-11-09 | 0.99 | +5124.4% | 34.8% | 3.22 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s8 | robustness | train | 2000-01-07 | 2025-11-09 | 0.92 | +3326.3% | 35.8% | 3.38 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain-s9 | robustness | train | 2000-01-07 | 2025-11-09 | 0.97 | +4618.0% | 36.7% | 3.53 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain | variant | train | 2000-01-07 | 2025-11-09 | 0.96 | +4204.9% | 35.7% | 3.12 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain@etf | robustness | train | 2001-06-01 | 2025-11-09 | 0.59 | +236.3% | 22.4% | 3.48 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.52 | +160.7% | 92.4% | 4.60 |
| 2026-11-13 05:39 | rl-2 | res-mlp-chain@idx | robustness | train | 2000-01-07 | 2025-11-09 | 0.48 | +193.0% | 28.7% | 2.84 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.00-k0.5 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3718.5% | 33.5% | 10.51 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.00-k1.0 | control | train | 2000-01-07 | 2025-11-09 | 0.91 | +2913.1% | 37.1% | 14.70 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.00-k2.0 | control | train | 2000-01-07 | 2025-11-09 | 0.86 | +2231.4% | 41.7% | 17.62 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.00-k4.0 | control | train | 2000-01-07 | 2025-11-09 | 0.84 | +1940.9% | 45.3% | 18.90 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.00-ksign | control | train | 2000-01-07 | 2025-11-09 | 0.84 | +1853.1% | 46.6% | 19.56 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.02-k0.5 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4183.3% | 33.1% | 10.52 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.02-k1.0 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3497.2% | 35.7% | 14.68 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.02-k2.0 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +2797.8% | 40.3% | 17.59 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.02-k4.0 | control | train | 2000-01-07 | 2025-11-09 | 0.90 | +2474.6% | 44.2% | 18.85 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.02-ksign | control | train | 2000-01-07 | 2025-11-09 | 0.89 | +2228.9% | 44.8% | 19.50 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.05-k0.5 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +4994.2% | 32.1% | 10.49 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.05-k1.0 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +4523.6% | 33.5% | 14.65 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.05-k2.0 | control | train | 2000-01-07 | 2025-11-09 | 1.00 | +3841.1% | 37.9% | 17.55 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.05-k4.0 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +3491.6% | 42.2% | 18.82 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.05-ksign | control | train | 2000-01-07 | 2025-11-09 | 1.01 | +3533.7% | 43.9% | 19.43 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.10-k0.5 | control | train | 2000-01-07 | 2025-11-09 | 1.09 | +6842.9% | 30.2% | 10.47 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.10-k1.0 | control | train | 2000-01-07 | 2025-11-09 | 1.13 | +7147.1% | 29.2% | 14.61 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.10-k2.0 | control | train | 2000-01-07 | 2025-11-09 | 1.14 | +6746.1% | 33.0% | 17.48 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.10-k4.0 | control | train | 2000-01-07 | 2025-11-09 | 1.14 | +6389.2% | 37.4% | 18.74 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.10-ksign | control | train | 2000-01-07 | 2025-11-09 | 1.14 | +6037.0% | 44.9% | 19.50 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.20-k0.5 | control | train | 2000-01-07 | 2025-11-09 | 1.25 | +12608.4% | 25.9% | 10.42 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.20-k1.0 | control | train | 2000-01-07 | 2025-11-09 | 1.36 | +17064.5% | 22.5% | 14.50 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.20-k2.0 | control | train | 2000-01-07 | 2025-11-09 | 1.42 | +19437.4% | 22.2% | 17.34 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.20-k4.0 | control | train | 2000-01-07 | 2025-11-09 | 1.43 | +19181.7% | 24.7% | 18.58 |
| 2026-11-13 05:50 | rl-3-control | ceiling-0.20-ksign | control | train | 2000-01-07 | 2025-11-09 | 1.43 | +17470.0% | 29.0% | 19.33 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5031.9% | 35.4% | 2.92 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5107.5% | 35.6% | 2.93 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4904.0% | 35.9% | 2.97 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5090.6% | 35.3% | 2.96 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5056.4% | 34.8% | 2.94 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5079.3% | 35.8% | 3.01 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4850.7% | 35.6% | 2.97 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4865.7% | 35.5% | 2.99 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4775.2% | 36.3% | 2.90 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4916.6% | 35.5% | 2.98 |
| 2026-11-13 06:30 | rl-3-control | plant-lin-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4967.1% | 35.8% | 2.94 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4973.0% | 36.5% | 2.94 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5103.7% | 35.4% | 2.98 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5050.1% | 35.1% | 3.04 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5130.5% | 35.3% | 2.97 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5149.6% | 34.9% | 2.99 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5149.6% | 36.1% | 3.02 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4895.5% | 35.5% | 2.97 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4828.1% | 35.3% | 3.00 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4827.8% | 36.0% | 2.91 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4984.4% | 35.7% | 3.02 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.02 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5025.7% | 35.8% | 2.94 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5082.4% | 36.0% | 3.00 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5108.9% | 35.5% | 3.01 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5017.8% | 35.3% | 3.13 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5154.1% | 35.2% | 3.05 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5132.3% | 35.1% | 3.17 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5154.9% | 35.4% | 3.07 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4845.7% | 36.0% | 3.05 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5002.6% | 35.3% | 3.30 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4897.0% | 35.8% | 3.02 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5134.8% | 35.8% | 3.19 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5096.9% | 35.3% | 3.04 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5147.3% | 35.9% | 3.21 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4822.9% | 35.7% | 3.20 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5332.0% | 35.4% | 3.38 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s3 | control | train | 2000-01-07 | 2025-11-09 | 1.00 | +5457.0% | 34.8% | 3.38 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5032.9% | 34.6% | 3.27 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5327.2% | 35.2% | 3.27 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5186.9% | 35.8% | 3.51 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5070.5% | 35.6% | 3.57 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5233.9% | 35.8% | 3.77 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10-s9 | control | train | 2000-01-07 | 2025-11-09 | 1.00 | +5367.6% | 35.6% | 3.48 |
| 2026-11-13 06:31 | rl-3-control | plant-lin-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5102.4% | 36.1% | 3.29 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s0 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +6067.1% | 36.0% | 4.23 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s1 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +5613.2% | 35.2% | 4.19 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s2 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +6298.9% | 35.4% | 4.56 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s3 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +6176.3% | 36.1% | 4.45 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s4 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +6107.4% | 35.2% | 4.67 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s5 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6561.0% | 35.5% | 4.31 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s6 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6683.5% | 35.7% | 4.41 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s7 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +5786.5% | 36.0% | 4.28 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s8 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +6057.9% | 34.8% | 4.67 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20-s9 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +6418.7% | 35.9% | 4.65 |
| 2026-11-13 06:32 | rl-3-control | plant-lin-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +6129.4% | 35.8% | 4.34 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4578.4% | 35.4% | 3.56 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s1 | control | train | 2000-01-07 | 2025-11-09 | 1.00 | +5545.1% | 34.8% | 3.51 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5100.8% | 35.6% | 3.14 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4733.6% | 36.1% | 3.16 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +3284.2% | 35.7% | 3.10 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +3374.9% | 35.2% | 3.23 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +4053.3% | 35.5% | 3.40 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4843.3% | 34.6% | 3.05 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5023.6% | 36.4% | 3.24 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4262.6% | 35.6% | 3.30 |
| 2026-11-13 06:32 | rl-3-control | plant-mlp-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4488.9% | 35.8% | 3.11 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4441.2% | 35.5% | 3.78 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4932.7% | 35.4% | 3.48 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +5131.7% | 35.9% | 3.20 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4709.1% | 36.2% | 3.18 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.91 | +3163.9% | 36.2% | 3.17 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3554.5% | 35.1% | 3.55 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4400.5% | 35.5% | 3.49 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4869.3% | 34.7% | 3.10 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +3400.0% | 36.1% | 3.34 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4684.8% | 34.8% | 3.38 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.02 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4316.1% | 36.0% | 3.20 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4606.7% | 36.4% | 4.13 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4760.7% | 34.7% | 3.99 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4993.2% | 35.8% | 3.55 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4234.1% | 34.9% | 3.42 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.91 | +3229.9% | 35.4% | 3.35 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3589.7% | 35.2% | 4.09 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4778.0% | 34.9% | 3.82 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5053.1% | 34.6% | 3.21 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +3414.0% | 36.1% | 3.23 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4608.1% | 34.9% | 4.01 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4337.5% | 35.2% | 3.44 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +3820.3% | 36.3% | 5.62 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4869.2% | 35.0% | 5.10 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s2 | control | train | 2000-01-07 | 2025-11-09 | 1.00 | +5537.4% | 35.4% | 4.56 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4499.4% | 35.1% | 4.25 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3456.5% | 36.1% | 3.86 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4792.5% | 35.8% | 4.97 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4400.3% | 34.9% | 4.69 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3846.3% | 34.3% | 4.00 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +3881.4% | 36.4% | 4.64 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4289.7% | 35.2% | 5.53 |
| 2026-11-13 06:33 | rl-3-control | plant-mlp-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4389.7% | 35.6% | 4.52 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s0 | control | train | 2000-01-07 | 2025-11-09 | 1.05 | +5852.3% | 33.9% | 8.83 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s1 | control | train | 2000-01-07 | 2025-11-09 | 1.09 | +7414.4% | 34.7% | 8.93 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s2 | control | train | 2000-01-07 | 2025-11-09 | 1.09 | +7721.2% | 33.6% | 7.85 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s3 | control | train | 2000-01-07 | 2025-11-09 | 1.06 | +6731.1% | 36.1% | 9.27 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s4 | control | train | 2000-01-07 | 2025-11-09 | 1.08 | +6365.4% | 34.6% | 8.85 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s5 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +5380.5% | 34.6% | 9.15 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s6 | control | train | 2000-01-07 | 2025-11-09 | 1.05 | +5648.6% | 34.8% | 8.88 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s7 | control | train | 2000-01-07 | 2025-11-09 | 1.07 | +6708.3% | 34.6% | 8.00 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s8 | control | train | 2000-01-07 | 2025-11-09 | 1.09 | +6982.4% | 33.1% | 7.43 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20-s9 | control | train | 2000-01-07 | 2025-11-09 | 1.10 | +7319.8% | 33.2% | 9.04 |
| 2026-11-13 06:34 | rl-3-control | plant-mlp-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.08 | +6850.6% | 33.8% | 8.50 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +4067.6% | 35.0% | 4.82 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +4984.5% | 34.7% | 4.90 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5157.8% | 36.2% | 4.23 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +3264.6% | 35.0% | 4.21 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.90 | +2804.3% | 32.9% | 3.93 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3633.7% | 35.2% | 5.11 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +3830.6% | 34.4% | 4.68 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4658.7% | 34.1% | 3.27 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.91 | +3011.8% | 33.3% | 4.71 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.90 | +2969.9% | 34.9% | 4.68 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3941.5% | 34.7% | 4.24 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3696.3% | 34.7% | 8.13 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3851.6% | 34.6% | 6.78 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4535.0% | 34.6% | 4.95 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +3703.8% | 36.3% | 5.04 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +2985.2% | 31.1% | 5.61 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3492.0% | 35.5% | 6.69 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3447.0% | 36.0% | 4.95 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3552.1% | 35.0% | 4.62 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +3675.4% | 30.4% | 7.84 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +3683.6% | 31.3% | 6.34 |
| 2026-11-13 07:29 | rl-3-control | diag-long-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +3843.3% | 33.9% | 5.82 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3910.2% | 42.2% | 4.92 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4669.7% | 44.3% | 4.68 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4900.7% | 44.6% | 4.56 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +4807.2% | 43.0% | 4.60 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3659.8% | 39.2% | 4.70 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3955.3% | 41.2% | 4.76 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3945.2% | 38.8% | 4.51 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.91 | +3506.4% | 43.1% | 4.29 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +3743.6% | 41.0% | 4.52 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +4266.7% | 43.0% | 4.85 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4119.7% | 41.3% | 4.41 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4271.2% | 43.2% | 6.74 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4877.2% | 46.8% | 6.54 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s2 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +5740.6% | 45.1% | 6.10 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s3 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +5548.6% | 39.5% | 6.30 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4002.4% | 41.4% | 6.27 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4394.3% | 41.8% | 6.48 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +4550.7% | 39.7% | 5.96 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4214.7% | 42.6% | 5.65 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +4574.3% | 40.5% | 6.06 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4342.3% | 43.1% | 6.58 |
| 2026-11-13 07:30 | rl-3-control | diag-noes-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +4675.5% | 41.8% | 6.07 |
| 2026-11-13 07:31 | rl-3-control | sup-ols-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.87 | +2673.8% | 45.5% | 5.56 |
| 2026-11-13 07:31 | rl-3-control | sup-ols-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.87 | +2749.2% | 45.6% | 7.02 |
| 2026-11-13 07:31 | rl-3-control | sup-ols-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.91 | +3245.2% | 45.1% | 8.98 |
| 2026-11-13 07:31 | rl-3-control | sup-ols-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.08 | +6989.5% | 44.1% | 11.32 |
| 2026-11-13 07:43 | info-1-screen | cot_spec (IC +0.003, chance 0.032, WF -0.007, gain -0.018) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | cot_spec_chg4 (IC -0.035, chance 0.033, WF +0.034, gain +0.012) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | cot_spec_z3y (IC -0.024, chance 0.028, WF +0.026, gain +0.007) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | cot_lev (IC +0.026, chance 0.061, WF -0.001, gain -0.005) | screen | train | 2006-06-23 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | cot_am (IC -0.020, chance 0.044, WF -0.007, gain -0.018) | screen | train | 2006-06-23 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | fund_bn (IC -0.005, chance 0.251, WF -0.015, gain +0.025) | screen | train | 2020-01-10 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | prem_bn (IC +0.034, chance 0.218, WF +0.046, gain +0.006) | screen | train | 2020-01-10 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | fund_drb (IC +0.009, chance 0.245, WF +0.059, gain -0.002) | screen | train | 2019-05-10 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | dvol_rv (IC -0.002, chance 0.236, WF +nan, gain +nan) | screen | train | 2021-03-26 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | puell (IC +0.056, chance 0.218, WF +0.015, gain +0.012) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | hash_growth (IC -0.003, chance 0.230, WF +0.106, gain +0.009) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | tx_growth (IC +0.065, chance 0.225, WF +0.037, gain +0.001) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | fng (IC +0.083, chance 0.285, WF +0.083, gain +0.015) | screen | train | 2018-02-09 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | vix_term (IC +0.012, chance 0.046, WF +0.033, gain +0.012) | screen | train | 2009-09-25 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | vix_term6 (IC -0.007, chance 0.049, WF +0.028, gain -0.019) | screen | train | 2008-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | skew_z (IC +0.023, chance 0.035, WF +0.007, gain -0.004) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | vvix_vix (IC +0.014, chance 0.052, WF +0.018, gain -0.020) | screen | train | 2006-03-10 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | vrp (IC -0.002, chance 0.034, WF -0.007, gain -0.011) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | pc_total (IC +0.022, chance 0.068, WF +0.033, gain +0.025) | screen | train | 2006-11-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | pc_equity (IC +0.025, chance 0.072, WF +0.038, gain +0.020) | screen | train | 2006-11-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | usd_13w (IC -0.019, chance 0.033, WF +0.003, gain -0.005) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | oil_13w (IC -0.008, chance 0.036, WF +0.021, gain +0.009) | screen | train | 2000-11-24 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:43 | info-1-screen | hy_ief_13w (IC -0.015, chance 0.050, WF +0.015, gain -0.002) | screen | train | 2007-07-13 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:55 | breadth-1-binance | weekly EW baseline | baseline | train | 2020-02-01 | 2025-11-09 | 0.91 | +916.1% | 81.5% | 1.82 |
| 2026-11-13 07:55 | breadth-1-binance | weekly TS baseline | baseline | train | 2020-02-01 | 2025-11-09 | 1.05 | +1314.5% | 62.2% | 3.41 |
| 2026-11-13 07:55 | breadth-1-binance | weekly mom_7 TOP-TS (IC -0.028 t -1.6, vs TS -0.30 p 0.96) no | variant | train | 2020-02-01 | 2025-11-09 | 0.75 | +372.7% | 74.4% | 43.07 |
| 2026-11-13 07:55 | breadth-1-binance | weekly mom_28 TOP-TS (IC +0.006 t +0.3, vs TS +0.06 p 0.36) no | variant | train | 2020-02-01 | 2025-11-09 | 1.11 | +2767.6% | 66.2% | 22.42 |
| 2026-11-13 07:55 | breadth-1-binance | weekly mom_91 TOP-TS (IC +0.003 t +0.2, vs TS -0.02 p 0.57) no | variant | train | 2020-02-01 | 2025-11-09 | 1.03 | +1975.3% | 69.5% | 13.26 |
| 2026-11-13 07:55 | breadth-1-binance | weekly mom_365 TOP-TS (IC +0.023 t +1.3, vs TS +0.02 p 0.45) no | variant | train | 2020-02-01 | 2025-11-09 | 1.07 | +1991.1% | 66.9% | 8.60 |
| 2026-11-13 07:55 | breadth-1-binance | weekly size TOP-TS (IC -0.075 t -4.5, vs TS +0.08 p 0.35) no | variant | train | 2020-02-01 | 2025-11-09 | 1.13 | +2831.3% | 64.0% | 5.25 |
| 2026-11-13 07:55 | breadth-1-binance | weekly turnover TOP-TS (IC +0.076 t +4.2, vs TS -0.03 p 0.57) no | variant | train | 2020-02-01 | 2025-11-09 | 1.01 | +1022.3% | 57.2% | 7.51 |
| 2026-11-13 07:55 | breadth-1-binance | weekly vol_growth TOP-TS (IC +0.001 t +0.1, vs TS -0.25 p 0.94) no | variant | train | 2020-02-01 | 2025-11-09 | 0.80 | +493.2% | 75.5% | 25.15 |
| 2026-11-13 07:55 | breadth-1-binance | weekly low_vol TOP-TS (IC +0.100 t +5.1, vs TS -0.02 p 0.52) weak-but-real | variant | train | 2020-02-01 | 2025-11-09 | 1.03 | +1033.2% | 61.1% | 7.60 |
| 2026-11-13 07:55 | breadth-1-binance | weekly EW baseline | baseline | train | 2020-02-15 | 2025-11-09 | 0.84 | +638.1% | 81.1% | 1.78 |
| 2026-11-13 07:55 | breadth-1-binance | weekly TS baseline | baseline | train | 2020-02-15 | 2025-11-09 | 0.99 | +1024.2% | 62.2% | 3.35 |
| 2026-11-13 07:55 | breadth-1-binance | weekly funding TOP-TS (IC +0.043 t +2.8, vs TS -0.15 p 0.81) no | variant | train | 2020-02-15 | 2025-11-09 | 0.84 | +766.5% | 69.3% | 24.29 |
| 2026-11-13 07:55 | breadth-1-binance | weekly premium TOP-TS (IC +0.030 t +2.0, vs TS -0.03 p 0.60) no | variant | train | 2020-02-15 | 2025-11-09 | 0.94 | +1256.5% | 72.0% | 24.88 |
| 2026-11-13 07:55 | breadth-1-trad | weekly EW baseline | baseline | train | 1999-12-28 | 2025-11-09 | 0.69 | +1617.5% | 44.0% | 0.07 |
| 2026-11-13 07:55 | breadth-1-trad | weekly TS baseline | baseline | train | 1999-12-28 | 2025-11-09 | 0.77 | +757.1% | 27.6% | 2.45 |
| 2026-11-13 07:55 | breadth-1-trad | weekly mom_7 TOP-TS (IC -0.003 t -0.3, vs TS -0.19 p 0.94) no | variant | train | 1999-12-28 | 2025-11-09 | 0.58 | +627.7% | 35.1% | 49.78 |
| 2026-11-13 07:55 | breadth-1-binance | daily EW baseline | baseline | train | 2020-01-31 | 2025-11-09 | 0.89 | +826.0% | 81.3% | 2.30 |
| 2026-11-13 07:55 | breadth-1-binance | daily TS baseline | baseline | train | 2020-01-31 | 2025-11-09 | 1.00 | +1058.1% | 61.6% | 7.91 |
| 2026-11-13 07:55 | breadth-1-binance | daily mom_7 TOP-TS (IC -0.028 t -4.1, vs TS -0.15 p 0.84) no | variant | train | 2020-01-31 | 2025-11-09 | 0.85 | +632.0% | 71.0% | 106.18 |
| 2026-11-13 07:55 | breadth-1-binance | daily mom_28 TOP-TS (IC -0.014 t -2.1, vs TS -0.01 p 0.55) no | variant | train | 2020-01-31 | 2025-11-09 | 0.98 | +1194.3% | 70.8% | 58.98 |
| 2026-11-13 07:55 | breadth-1-trad | weekly mom_28 TOP-TS (IC -0.008 t -0.9, vs TS -0.05 p 0.66) no | variant | train | 1999-12-28 | 2025-11-09 | 0.72 | +1227.2% | 35.2% | 25.81 |
| 2026-11-13 07:55 | breadth-1-binance | daily mom_91 TOP-TS (IC -0.004 t -0.6, vs TS -0.13 p 0.82) no | variant | train | 2020-01-31 | 2025-11-09 | 0.87 | +836.9% | 69.6% | 36.92 |
| 2026-11-13 07:55 | breadth-1-binance | daily mom_365 TOP-TS (IC +0.009 t +1.3, vs TS -0.04 p 0.59) no | variant | train | 2020-01-31 | 2025-11-09 | 0.95 | +1115.6% | 68.8% | 22.74 |
| 2026-11-13 07:55 | breadth-1-trad | weekly mom_91 TOP-TS (IC +0.002 t +0.2, vs TS -0.25 p 0.97) no | variant | train | 1999-12-28 | 2025-11-09 | 0.52 | +557.4% | 52.4% | 16.62 |
| 2026-11-13 07:55 | breadth-1-binance | daily rev_1 TOP-TS (IC +0.019 t +2.8, vs TS -1.41 p 1.00) no | variant | train | 2020-01-31 | 2025-11-09 | -0.41 | -96.0% | 98.3% | 286.58 |
| 2026-11-13 07:55 | breadth-1-binance | daily size TOP-TS (IC -0.050 t -7.6, vs TS -0.02 p 0.57) no | variant | train | 2020-01-31 | 2025-11-09 | 0.98 | +1360.7% | 62.1% | 10.77 |
| 2026-11-13 07:55 | breadth-1-binance | daily turnover TOP-TS (IC +0.057 t +8.5, vs TS +0.03 p 0.46) weak-but-real | variant | train | 2020-01-31 | 2025-11-09 | 1.03 | +1112.7% | 57.8% | 15.23 |
| 2026-11-13 07:55 | breadth-1-trad | weekly mom_365 TOP-TS (IC +0.025 t +2.6, vs TS -0.03 p 0.59) no | variant | train | 1999-12-28 | 2025-11-09 | 0.74 | +1472.1% | 42.8% | 10.36 |
| 2026-11-13 07:55 | breadth-1-binance | daily vol_growth TOP-TS (IC -0.016 t -2.7, vs TS -0.21 p 0.89) no | variant | train | 2020-01-31 | 2025-11-09 | 0.79 | +474.3% | 73.7% | 44.56 |
| 2026-11-13 07:55 | breadth-1-binance | daily low_vol TOP-TS (IC +0.069 t +8.9, vs TS -0.01 p 0.54) weak-but-real | variant | train | 2020-01-31 | 2025-11-09 | 0.99 | +827.6% | 59.3% | 14.53 |
| 2026-11-13 07:55 | breadth-1-trad | weekly low_vol TOP-TS (IC -0.021 t -1.9, vs TS -0.08 p 0.69) no | variant | train | 1999-12-28 | 2025-11-09 | 0.68 | +203.3% | 17.2% | 5.14 |
| 2026-11-13 07:55 | breadth-1-cm | weekly EW baseline | baseline | train | 2019-04-07 | 2025-11-09 | 0.64 | +223.1% | 85.3% | 2.88 |
| 2026-11-13 07:55 | breadth-1-cm | weekly TS baseline | baseline | train | 2019-04-07 | 2025-11-09 | 0.72 | +383.9% | 64.4% | 3.91 |
| 2026-11-13 07:55 | breadth-1-cm | weekly mom_7 TOP-TS (IC -0.023 t -2.3, vs TS -0.02 p 0.58) no | variant | train | 2019-04-07 | 2025-11-09 | 0.69 | +360.5% | 75.7% | 36.79 |
| 2026-11-13 07:55 | breadth-1-binance | daily EW baseline | baseline | train | 2020-02-14 | 2025-11-09 | 0.84 | +622.6% | 81.2% | 2.26 |
| 2026-11-13 07:55 | breadth-1-binance | daily TS baseline | baseline | train | 2020-02-14 | 2025-11-09 | 0.95 | +870.9% | 61.6% | 7.92 |
| 2026-11-13 07:55 | breadth-1-binance | daily funding TOP-TS (IC +0.027 t +4.8, vs TS -0.04 p 0.60) weak-but-real | variant | train | 2020-02-14 | 2025-11-09 | 0.91 | +1131.6% | 69.5% | 49.23 |
| 2026-11-13 07:55 | breadth-1-binance | daily premium TOP-TS (IC +0.025 t +4.5, vs TS -0.04 p 0.63) weak-but-real | variant | train | 2020-02-14 | 2025-11-09 | 0.89 | +994.9% | 75.4% | 48.99 |
| 2026-11-13 07:55 | breadth-1-cm | weekly mom_28 TOP-TS (IC -0.013 t -1.2, vs TS +0.26 p 0.01) no | variant | train | 2019-04-07 | 2025-11-09 | 0.98 | +1412.5% | 66.6% | 19.14 |
| 2026-11-13 07:55 | breadth-1-trad | weekly high_52w TOP-TS (IC +0.010 t +0.9, vs TS +0.04 p 0.38) no | variant | train | 1999-12-28 | 2025-11-09 | 0.81 | +791.2% | 30.4% | 21.14 |
| 2026-11-13 07:55 | breadth-1-cm | weekly mom_91 TOP-TS (IC -0.014 t -1.2, vs TS -0.00 p 0.52) no | variant | train | 2019-04-07 | 2025-11-09 | 0.72 | +422.4% | 67.3% | 12.30 |
| 2026-11-13 07:55 | breadth-1-cm | weekly mom_365 TOP-TS (IC +0.006 t +0.5, vs TS -0.08 p 0.69) no | variant | train | 2019-04-07 | 2025-11-09 | 0.64 | +252.5% | 81.1% | 8.71 |
| 2026-11-13 07:55 | breadth-1-trad | daily EW baseline | baseline | train | 1999-12-24 | 2025-11-09 | 0.70 | +1634.4% | 43.5% | 0.10 |
| 2026-11-13 07:55 | breadth-1-trad | daily TS baseline | baseline | train | 1999-12-24 | 2025-11-09 | 0.82 | +885.8% | 27.3% | 4.90 |
| 2026-11-13 07:55 | breadth-1-trad | daily mom_7 TOP-TS (IC -0.007 t -1.6, vs TS -0.26 p 0.99) no | variant | train | 1999-12-24 | 2025-11-09 | 0.56 | +580.0% | 42.0% | 101.01 |
| 2026-11-13 07:55 | breadth-1-cm | weekly size TOP-TS (IC -0.049 t -4.3, vs TS -0.02 p 0.59) no | variant | train | 2019-04-07 | 2025-11-09 | 0.69 | +342.8% | 69.2% | 7.19 |
| 2026-11-13 07:55 | breadth-1-cm | weekly turnover TOP-TS (IC +0.060 t +5.1, vs TS +0.34 p 0.00) PASS | variant | train | 2019-04-07 | 2025-11-09 | 1.06 | +1329.9% | 54.3% | 7.60 |
| 2026-11-13 07:55 | breadth-1-trad | daily mom_28 TOP-TS (IC +0.002 t +0.3, vs TS -0.02 p 0.55) no | variant | train | 1999-12-24 | 2025-11-09 | 0.80 | +1743.3% | 33.3% | 54.63 |
| 2026-11-13 07:55 | breadth-1-cm | weekly vol_growth TOP-TS (IC -0.021 t -2.3, vs TS +0.07 p 0.29) no | variant | train | 2019-04-07 | 2025-11-09 | 0.79 | +576.9% | 67.0% | 22.62 |
| 2026-11-13 07:55 | breadth-1-cm | weekly low_vol TOP-TS (IC +0.082 t +6.1, vs TS +0.04 p 0.38) weak-but-real | variant | train | 2019-04-07 | 2025-11-09 | 0.75 | +401.8% | 60.1% | 7.44 |
| 2026-11-13 07:55 | breadth-1-cm | weekly addr_growth TOP-TS (IC +0.011 t +1.0, vs TS +0.13 p 0.17) no | variant | train | 2019-04-07 | 2025-11-09 | 0.90 | +992.5% | 65.8% | 9.52 |
| 2026-11-13 07:55 | breadth-1-trad | daily mom_91 TOP-TS (IC +0.009 t +2.0, vs TS -0.23 p 0.97) no | variant | train | 1999-12-24 | 2025-11-09 | 0.59 | +726.6% | 43.4% | 36.20 |
| 2026-11-13 07:55 | breadth-1-cm | daily EW baseline | baseline | train | 2019-04-02 | 2025-11-09 | 0.66 | +262.7% | 85.7% | 4.04 |
| 2026-11-13 07:55 | breadth-1-cm | daily TS baseline | baseline | train | 2019-04-02 | 2025-11-09 | 0.76 | +458.7% | 64.7% | 8.94 |
| 2026-11-13 07:55 | breadth-1-cm | daily mom_7 TOP-TS (IC -0.017 t -4.2, vs TS -0.25 p 0.99) no | variant | train | 2019-04-02 | 2025-11-09 | 0.51 | +129.2% | 85.3% | 91.42 |
| 2026-11-13 07:55 | breadth-1-trad | daily mom_365 TOP-TS (IC +0.017 t +3.9, vs TS -0.07 p 0.69) no | variant | train | 1999-12-24 | 2025-11-09 | 0.75 | +1620.0% | 45.4% | 22.74 |
| 2026-11-13 07:55 | breadth-1-cm | daily mom_28 TOP-TS (IC -0.016 t -3.8, vs TS +0.08 p 0.26) no | variant | train | 2019-04-02 | 2025-11-09 | 0.83 | +719.3% | 68.2% | 49.53 |
| 2026-11-13 07:55 | breadth-1-cm | daily mom_91 TOP-TS (IC -0.014 t -3.6, vs TS +0.01 p 0.44) no | variant | train | 2019-04-02 | 2025-11-09 | 0.77 | +569.5% | 68.4% | 30.85 |
| 2026-11-13 07:55 | breadth-1-trad | daily low_vol TOP-TS (IC -0.019 t -3.6, vs TS -0.19 p 0.87) no | variant | train | 1999-12-24 | 2025-11-09 | 0.63 | +174.9% | 18.8% | 9.33 |
| 2026-11-13 07:55 | breadth-1-cm | daily mom_365 TOP-TS (IC -0.002 t -0.6, vs TS -0.14 p 0.78) no | variant | train | 2019-04-02 | 2025-11-09 | 0.62 | +234.1% | 81.7% | 22.57 |
| 2026-11-13 07:55 | breadth-1-trad | daily high_52w TOP-TS (IC +0.005 t +1.0, vs TS -0.04 p 0.61) no | variant | train | 1999-12-24 | 2025-11-09 | 0.78 | +682.1% | 30.7% | 48.33 |
| 2026-11-13 07:55 | breadth-1-cm | daily rev_1 TOP-TS (IC +0.009 t +2.4, vs TS -1.33 p 1.00) no | variant | train | 2019-04-02 | 2025-11-09 | -0.57 | -96.4% | 98.8% | 246.10 |
| 2026-11-13 07:55 | breadth-1-cm | daily size TOP-TS (IC -0.031 t -8.4, vs TS +0.03 p 0.42) no | variant | train | 2019-04-02 | 2025-11-09 | 0.79 | +527.0% | 66.7% | 13.90 |
| 2026-11-13 07:55 | breadth-1-cm | daily turnover TOP-TS (IC +0.039 t +9.1, vs TS +0.31 p 0.00) PASS | variant | train | 2019-04-02 | 2025-11-09 | 1.07 | +1367.5% | 56.2% | 15.60 |
| 2026-11-13 07:55 | breadth-1-cm | daily vol_growth TOP-TS (IC -0.024 t -7.0, vs TS -0.05 p 0.70) no | variant | train | 2019-04-02 | 2025-11-09 | 0.71 | +397.2% | 72.8% | 39.05 |
| 2026-11-13 07:55 | breadth-1-cm | daily low_vol TOP-TS (IC +0.057 t +11.5, vs TS -0.03 p 0.59) weak-but-real | variant | train | 2019-04-02 | 2025-11-09 | 0.73 | +364.5% | 60.8% | 16.93 |
| 2026-11-13 07:55 | breadth-1-cm | daily addr_growth TOP-TS (IC -0.000 t -0.1, vs TS +0.09 p 0.24) no | variant | train | 2019-04-02 | 2025-11-09 | 0.91 | +1031.8% | 61.3% | 19.03 |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp r_1h (IC 1h -0.0869, 24h -0.024) | screen | train | 2011-08-18 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp r_4h (IC 1h -0.0688, 24h -0.031) | screen | train | 2011-08-18 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp r_24h (IC 1h -0.0153, 24h -0.027) | screen | train | 2011-08-18 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp r_168h (IC 1h +0.0145, 24h +0.035) | screen | train | 2011-08-18 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp vol_shock (IC 1h +0.0147, 24h +0.030) | screen | train | 2011-08-18 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp volu_shock (IC 1h +0.0219, 24h +0.050) | screen | train | 2011-08-18 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp hour_mean (IC 1h +0.0002, 24h -0.014) | screen | train | 2011-08-18 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance r_1h (IC 1h -0.0716, 24h -0.023) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance r_4h (IC 1h -0.0606, 24h -0.040) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance r_24h (IC 1h -0.0242, 24h -0.055) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance r_168h (IC 1h +0.0088, 24h +0.003) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance vol_shock (IC 1h +0.0099, 24h +0.041) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance volu_shock (IC 1h +0.0145, 24h +0.030) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance hour_mean (IC 1h +0.0095, 24h +0.001) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp r_1h (IC 1h -0.0628, 24h -0.039) | screen | train | 2017-08-16 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp r_4h (IC 1h -0.0492, 24h -0.047) | screen | train | 2017-08-16 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp r_24h (IC 1h -0.0261, 24h -0.079) | screen | train | 2017-08-16 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp r_168h (IC 1h +0.0088, 24h +0.006) | screen | train | 2017-08-16 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp vol_shock (IC 1h +0.0154, 24h +0.052) | screen | train | 2017-08-16 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp volu_shock (IC 1h +0.0130, 24h +0.032) | screen | train | 2017-08-16 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp hour_mean (IC 1h +0.0067, 24h +0.053) | screen | train | 2017-08-16 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance r_1h (IC 1h -0.0593, 24h -0.045) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance r_4h (IC 1h -0.0506, 24h -0.049) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance r_24h (IC 1h -0.0252, 24h -0.075) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance r_168h (IC 1h +0.0089, 24h +0.006) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance vol_shock (IC 1h +0.0159, 24h +0.053) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance volu_shock (IC 1h +0.0170, 24h +0.038) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance hour_mean (IC 1h +0.0089, 24h +0.053) | screen | train | 2017-08-17 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp buy-hold | baseline | train | 2014-01-01 | 2025-11-09 | 0.95 | +14025.6% | 83.3% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp tsmom12 daily | baseline | train | 2014-01-01 | 2025-11-09 | 0.99 | +14354.8% | 80.9% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp hf-band 30bps (vs ts -0.14 p 0.80) | variant | train | 2014-01-01 | 2025-11-09 | 0.85 | +5650.5% | 87.0% | 19.55 |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp hf-band-ts 30bps (vs ts -0.07 p 0.79) | variant | train | 2014-01-01 | 2025-11-09 | 0.92 | +7110.7% | 87.0% | 19.55 |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance buy-hold | baseline | train | 2020-01-01 | 2025-11-09 | 1.05 | +1354.8% | 76.5% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance tsmom12 daily | baseline | train | 2020-01-01 | 2025-11-09 | 1.16 | +1679.2% | 55.1% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance hf-band 30bps (vs ts -0.26 p 0.83) | variant | train | 2020-01-01 | 2025-11-09 | 0.91 | +661.7% | 74.9% | 15.18 |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance hf-band-ts 30bps (vs ts -0.04 p 0.63) | variant | train | 2020-01-01 | 2025-11-09 | 1.12 | +1062.3% | 45.2% | 15.18 |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp buy-hold | baseline | train | 2020-01-01 | 2025-11-09 | 1.10 | +2681.8% | 79.3% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp tsmom12 daily | baseline | train | 2020-01-01 | 2025-11-09 | 0.92 | +896.7% | 72.4% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp hf-band 30bps (vs ts -0.53 p 0.97) | variant | train | 2020-01-01 | 2025-11-09 | 0.38 | +4.0% | 82.4% | 54.41 |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp hf-band-ts 30bps (vs ts -0.41 p 0.99) | variant | train | 2020-01-01 | 2025-11-09 | 0.50 | +95.1% | 68.3% | 54.41 |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance buy-hold | baseline | train | 2020-01-01 | 2025-11-09 | 1.10 | +2672.3% | 79.3% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance tsmom12 daily | baseline | train | 2020-01-01 | 2025-11-09 | 0.93 | +954.8% | 70.8% | 0.00 |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance hf-band 30bps (vs ts -0.34 p 0.85) | variant | train | 2020-01-01 | 2025-11-09 | 0.59 | +174.1% | 82.4% | 41.45 |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance hf-band-ts 30bps (vs ts -0.31 p 0.93) | variant | train | 2020-01-01 | 2025-11-09 | 0.62 | +204.7% | 62.0% | 41.45 |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp hf-band 10bps (vs ts -0.08 p 0.69) | robustness | train | 2014-01-01 | 2025-11-09 | 0.92 | +9072.7% | 85.8% | 19.55 |
| 2026-11-13 07:57 | breadth-1-hf | btc-bitstamp hf-band-ts 10bps (vs ts -0.02 p 0.61) | robustness | train | 2014-01-01 | 2025-11-09 | 0.98 | +10687.3% | 85.5% | 19.55 |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance hf-band 10bps (vs ts -0.21 p 0.79) | robustness | train | 2020-01-01 | 2025-11-09 | 0.96 | +810.4% | 73.5% | 15.18 |
| 2026-11-13 07:57 | breadth-1-hf | btc-binance hf-band-ts 10bps (vs ts +0.00 p 0.53) | robustness | train | 2020-01-01 | 2025-11-09 | 1.18 | +1267.2% | 44.1% | 15.18 |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp hf-band 10bps (vs ts -0.40 p 0.93) | robustness | train | 2020-01-01 | 2025-11-09 | 0.53 | +97.1% | 76.8% | 54.41 |
| 2026-11-13 07:57 | breadth-1-hf | eth-bitstamp hf-band-ts 10bps (vs ts -0.30 p 0.96) | robustness | train | 2020-01-01 | 2025-11-09 | 0.63 | +212.5% | 65.8% | 54.41 |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance hf-band 10bps (vs ts -0.23 p 0.77) | robustness | train | 2020-01-01 | 2025-11-09 | 0.71 | +346.0% | 78.4% | 41.45 |
| 2026-11-13 07:57 | breadth-1-hf | eth-binance hf-band-ts 10bps (vs ts -0.22 p 0.85) | robustness | train | 2020-01-01 | 2025-11-09 | 0.73 | +339.7% | 59.2% | 41.45 |
| 2026-11-13 07:57 | breadth-1-binance | hourly rev_1h (IC +0.0612 t +29.7, break-even 0.58) | screen | train | 2020-01-01 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:57 | breadth-1-binance | hourly mom_24h (IC -0.0366 t -17.1, break-even 0.20) | screen | train | 2020-01-01 | 2025-11-09 | - | - | - | - |
