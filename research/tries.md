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
- `live-check` (added 2026-11-18, survey-5): a descriptive re-score of an already logged
  configuration over a live-fund window (variant tagged `@live-L`, 2010-02 to 2025-10), set
  against live funds; not selectable, not a strategy try, not counted in the family
  (`cards/live-check.md`, numbers in `results/live-check.md`). Survey-6 extends it:
  `<family>@live-fund` rows are equal-weight composites of live funds of a strategy family
  over their own months (From/To), Sharpe = monthly return above the T-bill (not the daily
  convention), Return and Max DD of the total return, turnover `-`
  (`cards/live-families.md`, numbers in `results/live-families.md`).
- `replication` (added 2026-11-18, ls-trend-1): a descriptive replication of a published effect
  built outside the live book's constraints (here shorts and leverage the paper broker cannot
  hold), tagged `@live-L` (2010-02 to 2025-10, Sharpe on excess returns); not selectable, not a
  strategy try, not counted in the family (`cards/ls-trend.md`, numbers in
  `results/ls-trend.md`).

- `insure-check` (added 2026-11-18, insure-1): a descriptive re-score of an already logged
  configuration (`tsmom12`) on a span or set it was not logged on (trend-1926's saved gym runs
  spliced with the gym-free paper series to 1927-2025; the 30 French industries, paper series);
  not selectable, not a strategy try, not counted in any family (`cards/crash-insurance.md`,
  numbers in `results/insure-1.md`). Turnover/yr there = position flips a year. insure-2 adds
  27 such rows on non-US stock indices (paper series; `cards/insure-geo.md`, `results/insure-2.md`).
- Sharpe: daily, 365 days/yr, zero risk-free rate (the repo's convention).
- `invest-1` rows (added 2026-11-13): monthly decisions; Sharpe is of monthly returns in excess
  of T-bills x sqrt(12); period `train` = 1927-01..1989-12, `oos` = 1990-01..2025-10 (both fixed
  on the card in `invest-1.md`, neither is the protocol's held-out year); Return is total, not
  per year; Turnover/yr = sum of |weight changes| in stocks and bonds per year.

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
| 2026-11-13 07:59 | breadth-1-cm | weekly turnover TOP-TS, 100 bps a side | robustness | train | 2019-04-07 | 2025-11-09 | 0.93 | +828.3% | 59.8% | 7.60 |
| 2026-11-13 07:59 | breadth-1-cm | weekly turnover TOP-TS, top 50 coins | robustness | train | 2019-04-07 | 2025-11-09 | 1.04 | +1317.1% | 55.4% | 7.66 |
| 2026-11-13 07:59 | breadth-1-cm | weekly turnover placebo, 100 random fixed scores (95th pct of TOP-TS - TS +0.10) | control | train | 2019-04-05 | 2025-11-09 | - | - | - | - |
| 2026-11-13 07:59 | breadth-1-cm | weekly turnover TS held-out | baseline | heldout | 2025-11-16 | 2026-11-09 | 0.31 | +2.1% | 5.0% | 2.21 |
| 2026-11-13 07:59 | breadth-1-cm | weekly turnover TOP-TS held-out | variant | heldout | 2025-11-16 | 2026-11-09 | 0.61 | +5.1% | 6.1% | 2.21 |
| 2026-11-13 08:07 | short-1-P30 | tsmom12 spot, spot 30 bps | baseline | train | 2020-02-15 | 2025-11-09 | 1.03 | +1201.3% | 62.2% | 3.30 |
| 2026-11-13 08:07 | short-1-P30 | tsmom12 perp, perp 10 bps + funding | baseline | train | 2020-02-15 | 2025-11-09 | 0.88 | +665.0% | 62.2% | 3.30 |
| 2026-11-13 08:07 | short-1-P30 | tsmom12 perp, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | 0.86 | +619.7% | 62.3% | 3.30 |
| 2026-11-13 08:07 | short-1-P30 | EW perp, perp 10 bps + funding | baseline | train | 2020-02-15 | 2025-11-09 | 0.80 | +498.0% | 81.9% | 1.48 |
| 2026-11-13 08:07 | short-1-P30 | EW perp, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | 0.79 | +469.3% | 82.1% | 1.48 |
| 2026-11-13 08:07 | short-1-P30 | tsmom12-ls, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | 0.73 | +343.3% | 62.2% | 6.81 |
| 2026-11-13 08:07 | short-1-P30 | tsmom12-ls, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | 0.69 | +290.0% | 62.5% | 6.81 |
| 2026-11-13 08:07 | short-1-P30 | ls-low_vol, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | -0.43 | -72.3% | 81.2% | 9.70 |
| 2026-11-13 08:07 | short-1-P30 | ls-low_vol, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | -0.52 | -76.8% | 82.9% | 9.70 |
| 2026-11-13 08:07 | short-1-P30 | ls-size, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | -0.62 | -84.6% | 90.0% | 5.15 |
| 2026-11-13 08:07 | short-1-P30 | ls-size, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | -0.68 | -86.4% | 90.8% | 5.15 |
| 2026-11-13 08:07 | short-1-P30 | ls-turnover, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | -0.54 | -73.2% | 87.0% | 9.99 |
| 2026-11-13 08:07 | short-1-P30 | ls-turnover, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | -0.63 | -77.6% | 88.3% | 9.99 |
| 2026-11-13 08:07 | short-1-P30 | ls-funding, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | 0.78 | +195.2% | 47.5% | 38.60 |
| 2026-11-13 08:07 | short-1-P30 | ls-funding, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | 0.49 | +82.2% | 52.0% | 38.60 |
| 2026-11-13 08:07 | short-1-P30 | ls-premium, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | 0.83 | +229.5% | 49.2% | 39.64 |
| 2026-11-13 08:07 | short-1-P30 | ls-premium, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | 0.54 | +100.9% | 53.6% | 39.64 |
| 2026-11-13 08:07 | short-1-P30 | ls-trend, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | 0.24 | +16.5% | 51.3% | 11.00 |
| 2026-11-13 08:07 | short-1-P30 | ls-trend, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | 0.13 | -3.2% | 55.3% | 11.00 |
| 2026-11-13 08:07 | short-1-P30 | ls-combo, perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | -0.34 | -64.6% | 79.0% | 16.97 |
| 2026-11-13 08:07 | short-1-P30 | ls-combo, perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | -0.47 | -72.6% | 81.7% | 16.97 |
| 2026-11-13 08:07 | short-1-P30 | ls-rev_1 (daily), perp 10 bps + funding | variant | train | 2020-02-15 | 2025-11-09 | -1.97 | -98.2% | 98.2% | 483.24 |
| 2026-11-13 08:07 | short-1-P30 | ls-rev_1 (daily), perp 30 bps + funding | robustness | train | 2020-02-15 | 2025-11-09 | -5.04 | -100.0% | 100.0% | 483.24 |
| 2026-11-13 08:07 | short-1-BTC-ETH | tsmom12 spot, spot 30 bps | baseline | train | 2020-01-04 | 2025-11-09 | 1.19 | +1958.5% | 57.9% | 1.62 |
| 2026-11-13 08:07 | short-1-BTC-ETH | tsmom12 perp, perp 10 bps + funding | baseline | train | 2020-01-04 | 2025-11-09 | 0.98 | +906.2% | 59.2% | 1.62 |
| 2026-11-13 08:07 | short-1-BTC-ETH | tsmom12 perp, perp 30 bps + funding | robustness | train | 2020-01-04 | 2025-11-09 | 0.97 | +875.3% | 59.2% | 1.62 |
| 2026-11-13 08:07 | short-1-BTC-ETH | EW perp, perp 10 bps + funding | baseline | train | 2020-01-04 | 2025-11-09 | 0.92 | +901.0% | 77.3% | 0.00 |
| 2026-11-13 08:07 | short-1-BTC-ETH | EW perp, perp 30 bps + funding | robustness | train | 2020-01-04 | 2025-11-09 | 0.92 | +884.4% | 77.4% | 0.00 |
| 2026-11-13 08:07 | short-1-BTC-ETH | tsmom12-ls, perp 10 bps + funding | variant | train | 2020-01-04 | 2025-11-09 | 0.76 | +404.3% | 62.9% | 3.24 |
| 2026-11-13 08:07 | short-1-BTC-ETH | tsmom12-ls, perp 30 bps + funding | robustness | train | 2020-01-04 | 2025-11-09 | 0.74 | +368.6% | 63.4% | 3.24 |
| 2026-11-13 08:08 | short-1-P30 | ls-low_vol long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | 0.83 | +278.1% | 45.1% | 4.47 |
| 2026-11-13 08:08 | short-1-P30 | ls-low_vol short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.86 | -97.2% | 98.2% | 5.23 |
| 2026-11-13 08:08 | short-1-P30 | ls-size long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | 0.62 | +152.0% | 53.8% | 2.14 |
| 2026-11-13 08:08 | short-1-P30 | ls-size short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.86 | -97.5% | 98.6% | 3.01 |
| 2026-11-13 08:08 | short-1-P30 | ls-turnover long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | 0.71 | +206.8% | 53.4% | 4.92 |
| 2026-11-13 08:08 | short-1-P30 | ls-turnover short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.85 | -96.2% | 97.9% | 5.07 |
| 2026-11-13 08:08 | short-1-P30 | ls-funding long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | 0.91 | +505.8% | 55.0% | 17.41 |
| 2026-11-13 08:08 | short-1-P30 | ls-funding short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.41 | -78.5% | 87.5% | 21.18 |
| 2026-11-13 08:08 | short-1-P30 | ls-premium long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | 1.02 | +720.8% | 55.3% | 18.37 |
| 2026-11-13 08:08 | short-1-P30 | ls-premium short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.47 | -82.1% | 88.7% | 21.27 |
| 2026-11-13 08:08 | short-1-P30 | ls-trend long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | 0.88 | +414.2% | 55.1% | 5.26 |
| 2026-11-13 08:08 | short-1-P30 | ls-trend short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.68 | -91.4% | 95.3% | 5.74 |
| 2026-11-13 08:08 | short-1-P30 | ls-combo long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | 0.76 | +230.9% | 48.0% | 8.01 |
| 2026-11-13 08:08 | short-1-P30 | ls-combo short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.74 | -95.8% | 97.4% | 8.95 |
| 2026-11-13 08:08 | short-1-P30 | ls-rev_1 (daily) long leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -0.01 | -49.5% | 77.7% | 243.76 |
| 2026-11-13 08:08 | short-1-P30 | ls-rev_1 (daily) short leg alone (diagnostic) | robustness | train | 2020-02-15 | 2025-11-09 | -1.47 | -98.6% | 99.0% | 239.48 |
| 2026-11-13 08:17 | invest-1 | 6040 | baseline | train | 1927-01 | 1989-12 | 0.41 | +14628.4% | 63.0% | 0.23 |
| 2026-11-13 08:17 | invest-1 | 6040 | baseline | oos | 1990-01 | 2025-10 | 0.67 | +2028.4% | 28.8% | 0.22 |
| 2026-11-13 08:17 | invest-1 | bh-stocks | baseline | train | 1927-01 | 1989-12 | 0.40 | +38532.5% | 83.7% | 0.00 |
| 2026-11-13 08:17 | invest-1 | bh-stocks | baseline | oos | 1990-01 | 2025-10 | 0.59 | +4022.9% | 50.3% | 0.00 |
| 2026-11-13 08:17 | invest-1 | tsmom12-m | baseline | train | 1927-01 | 1989-12 | 0.53 | +9429.0% | 19.1% | 0.95 |
| 2026-11-13 08:17 | invest-1 | tsmom12-m | baseline | oos | 1990-01 | 2025-10 | 0.77 | +1428.2% | 7.6% | 0.94 |
| 2026-11-13 08:17 | invest-1 | cape-tilt | variant | train | 1927-01 | 1989-12 | 0.43 | +22785.1% | 60.7% | 0.54 |
| 2026-11-13 08:17 | invest-1 | cape-tilt | variant | oos | 1990-01 | 2025-10 | 0.67 | +1232.7% | 22.2% | 0.34 |
| 2026-11-13 08:17 | invest-1 | ecy-tilt | variant | train | 1927-01 | 1989-12 | 0.49 | +34921.3% | 56.6% | 0.48 |
| 2026-11-13 08:17 | invest-1 | ecy-tilt | variant | oos | 1990-01 | 2025-10 | 0.73 | +2107.9% | 30.7% | 0.54 |
| 2026-11-13 08:17 | invest-1 | term-tilt | variant | train | 1927-01 | 1989-12 | 0.38 | +10865.4% | 63.0% | 1.40 |
| 2026-11-13 08:17 | invest-1 | term-tilt | variant | oos | 1990-01 | 2025-10 | 0.57 | +1442.9% | 34.6% | 1.06 |
| 2026-11-13 08:17 | invest-1 | real-tilt | variant | train | 1927-01 | 1989-12 | 0.46 | +18935.0% | 49.3% | 0.48 |
| 2026-11-13 08:17 | invest-1 | real-tilt | variant | oos | 1990-01 | 2025-10 | 0.64 | +2261.5% | 37.8% | 0.57 |
| 2026-11-13 08:17 | invest-1 | infl-regime | variant | train | 1927-01 | 1989-12 | 0.41 | +13926.2% | 63.0% | 0.34 |
| 2026-11-13 08:17 | invest-1 | infl-regime | variant | oos | 1990-01 | 2025-10 | 0.69 | +2051.7% | 32.7% | 0.35 |
| 2026-11-13 08:17 | invest-1 | 6040-sma10 | variant | train | 1927-01 | 1989-12 | 0.52 | +11432.5% | 24.7% | 1.38 |
| 2026-11-13 08:17 | invest-1 | 6040-sma10 | variant | oos | 1990-01 | 2025-10 | 0.75 | +1436.2% | 9.1% | 1.66 |
| 2026-11-13 08:17 | invest-1 | xmom | variant | train | 1927-01 | 1989-12 | 0.51 | +33056.3% | 43.5% | 2.10 |
| 2026-11-13 08:17 | invest-1 | xmom | variant | oos | 1990-01 | 2025-10 | 0.59 | +2182.9% | 20.6% | 2.57 |
| 2026-11-13 08:17 | invest-1 | ecy-trend | variant | train | 1927-01 | 1989-12 | 0.62 | +22702.7% | 19.4% | 1.14 |
| 2026-11-13 08:17 | invest-1 | ecy-trend | variant | oos | 1990-01 | 2025-10 | 0.82 | +1633.1% | 9.7% | 1.19 |
| 2026-11-13 08:17 | invest-1 | 6040 (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.76 | +486.7% | 29.5% | 0.21 |
| 2026-11-13 08:17 | invest-1 | bh-stocks (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.68 | +915.8% | 50.8% | 0.00 |
| 2026-11-13 08:17 | invest-1 | tsmom12-m (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.97 | +357.2% | 6.8% | 0.99 |
| 2026-11-13 08:17 | invest-1 | cape-tilt (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.71 | +300.8% | 22.9% | 0.35 |
| 2026-11-13 08:17 | invest-1 | ecy-tilt (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.75 | +481.6% | 31.5% | 0.51 |
| 2026-11-13 08:17 | invest-1 | term-tilt (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.60 | +352.0% | 35.1% | 0.75 |
| 2026-11-13 08:17 | invest-1 | real-tilt (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.68 | +540.8% | 38.4% | 0.56 |
| 2026-11-13 08:17 | invest-1 | infl-regime (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.80 | +508.2% | 32.6% | 0.40 |
| 2026-11-13 08:17 | invest-1 | 6040-sma10 (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.81 | +318.7% | 15.3% | 1.84 |
| 2026-11-13 08:17 | invest-1 | xmom (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.55 | +553.9% | 28.2% | 3.88 |
| 2026-11-13 08:17 | invest-1 | ecy-trend (ETF) | robustness | oos | 2003-09 | 2025-10 | 0.94 | +409.7% | 9.6% | 1.23 |
| 2026-11-13 08:29 | fm-1 | fm-bolt-small-tilt | variant | train | 2000-01-07 | 2025-11-09 | 1.09 | +7326.7% | 34.1% | 7.60 |
| 2026-11-13 08:29 | fm-1 | fm-bolt-small weekly IC +0.105 (post-release +0.105), WF gain +0.057 | screen | train | 2000-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-small daily IC +0.034 (post-release -0.032) | screen | train | 2000-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-small hourly btc-binance-1h IC -0.0054 (post-release -0.0251, partial -0.0057) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-small hourly btc-binance-24h IC +0.0129 (post-release +0.0076, partial +0.0083) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-small hourly eth-binance-1h IC +0.0110 (post-release +0.0279, partial +0.0109) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-small hourly eth-binance-24h IC +0.0305 (post-release +0.0475, partial +0.0288) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-base-tilt | variant | train | 2000-01-07 | 2025-11-09 | 1.17 | +10210.2% | 29.6% | 8.10 |
| 2026-11-13 08:29 | fm-1 | fm-bolt-base weekly IC +0.148 (post-release +0.164), WF gain +0.110 | screen | train | 2000-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-base daily IC +0.040 (post-release -0.005) | screen | train | 2000-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-base hourly btc-binance-1h IC -0.0159 (post-release -0.0379, partial -0.0141) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-base hourly btc-binance-24h IC +0.0052 (post-release -0.0439, partial -0.0007) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-base hourly eth-binance-1h IC -0.0066 (post-release +0.0128, partial -0.0055) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-bolt-base hourly eth-binance-24h IC +0.0341 (post-release +0.0297, partial +0.0317) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-chronos2-tilt | variant | train | 2000-01-07 | 2025-11-09 | 0.99 | +4478.0% | 34.9% | 9.78 |
| 2026-11-13 08:29 | fm-1 | fm-chronos2 weekly IC +0.020 (post-release +0.303), WF gain -0.008 | screen | train | 2000-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-chronos2 daily IC -0.012 (post-release -0.064) | screen | train | 2000-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-chronos2 hourly btc-binance-1h IC -0.0285 (post-release +0.1273, partial -0.0290) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-chronos2 hourly btc-binance-24h IC +0.0123 (post-release -0.0060, partial +0.0127) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-chronos2 hourly eth-binance-1h IC -0.0195 (post-release +0.1392, partial -0.0182) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 08:29 | fm-1 | fm-chronos2 hourly eth-binance-24h IC -0.0138 (post-release +0.1293, partial -0.0151) | screen | train | 2023-01 | 2025-11 | - | - | - | - |
| 2026-11-13 05:48 | bbwp | bbwp-and | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +11791.1% | 35.4% | 3.03 |
| 2026-11-13 05:48 | gap | gap-and | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +9117.6% | 36.5% | 2.57 |
| 2026-11-13 05:48 | bbwp | bbwp-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.82 | +11865.0% | 68.8% | 2.47 |
| 2026-11-13 05:48 | gap | gap-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.78 | +6409.0% | 68.8% | 2.44 |
| 2026-11-13 05:49 | gap | gap-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.46 | +88.0% | 16.5% | 2.57 |
| 2026-11-13 05:49 | bbwp | bbwp-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.61 | +223.8% | 16.7% | 2.98 |
| 2026-11-13 05:49 | gap | gap-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.31 | +121.5% | 34.8% | 2.05 |
| 2026-11-13 05:49 | bbwp | bbwp-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.52 | +170.1% | 92.4% | 4.83 |
| 2026-11-13 05:49 | bbwp | bbwp-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.32 | +137.4% | 34.8% | 2.06 |
| 2026-11-13 05:49 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 05:49 | gap | gap-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.47 | +1340.3% | 40.0% | 1.63 |
| 2026-11-13 05:49 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 05:49 | bbwp | bbwp-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.49 | +2546.3% | 44.2% | 2.49 |
| 2026-11-13 05:49 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 05:49 | gap | gap-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.29 | +154.5% | 39.1% | 1.75 |
| 2026-11-13 05:49 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 05:49 | bbwp | bbwp-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.27 | +175.3% | 39.1% | 2.88 |
| 2026-11-13 05:49 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 05:49 | gap | gap-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.20 | +90.3% | 53.5% | 1.39 |
| 2026-11-13 05:49 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 05:49 | bbwp | bbwp-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.37 | +384.6% | 55.6% | 1.91 |
| 2026-11-13 05:49 | oil | oil-and | variant | train | 1994-02-01 | 2025-11-09 | 1.10 | +16247.2% | 36.5% | 2.68 |
| 2026-11-13 05:49 | oil | oil-alone | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +18971.7% | 56.3% | 2.37 |
| 2026-11-13 05:49 | srsi | srsi-and | variant | train | 1994-02-01 | 2025-11-09 | 0.82 | +2710.9% | 28.9% | 2.33 |
| 2026-11-13 05:49 | srsi | srsi-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.69 | +3167.2% | 68.8% | 2.18 |
| 2026-11-13 05:49 | oil | oil-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.63 | +197.4% | 16.6% | 2.72 |
| 2026-11-13 05:49 | srsi | srsi-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.44 | +83.9% | 11.6% | 2.18 |
| 2026-11-13 05:49 | oil | oil-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.31 | +126.8% | 34.8% | 2.01 |
| 2026-11-13 05:49 | srsi | srsi-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.56 | +254.0% | 90.7% | 3.69 |
| 2026-11-13 05:49 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 05:49 | srsi | srsi-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.24 | +64.4% | 34.8% | 1.44 |
| 2026-11-13 05:49 | oil | oil-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.53 | +3121.1% | 40.2% | 1.86 |
| 2026-11-13 05:49 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 05:49 | srsi | srsi-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.28 | +277.5% | 35.5% | 1.53 |
| 2026-11-13 05:49 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 05:49 | oil | oil-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.31 | +191.2% | 40.7% | 2.47 |
| 2026-11-13 05:49 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 05:49 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 05:49 | srsi | srsi-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.35 | +200.3% | 32.2% | 2.03 |
| 2026-11-13 05:49 | oil | oil-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.39 | +367.7% | 57.7% | 1.56 |
| 2026-11-13 05:49 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 05:49 | srsi | srsi-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.33 | +214.6% | 23.6% | 1.31 |
| 2026-11-13 05:49 | y10 | y10chg-and | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +14768.8% | 36.5% | 3.18 |
| 2026-11-13 05:49 | y10 | y10lvl40-and | variant | train | 1994-02-01 | 2025-11-09 | 0.98 | +5338.2% | 36.5% | 2.93 |
| 2026-11-13 05:49 | y10 | y10lvl47-and | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +8460.8% | 36.5% | 2.93 |
| 2026-11-13 05:49 | y10 | y10lvl55-and | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +9474.5% | 36.5% | 2.74 |
| 2026-11-13 05:49 | ath | ath-and | variant | train | 1994-02-01 | 2025-11-09 | 1.13 | +12883.1% | 28.9% | 2.78 |
| 2026-11-13 05:49 | ath | ath-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.96 | +18340.6% | 68.8% | 2.30 |
| 2026-11-13 05:49 | ath | ath-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.62 | +190.4% | 16.5% | 2.83 |
| 2026-11-13 05:49 | y10 | y10chg-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.59 | +214.7% | 16.5% | 3.31 |
| 2026-11-13 05:49 | ath | ath-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.62 | +437.8% | 90.1% | 4.44 |
| 2026-11-13 05:49 | y10 | y10chg-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.63 | +441.5% | 29.4% | 2.55 |
| 2026-11-13 05:49 | ath | ath-and@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.48 | +274.7% | 34.8% | 1.76 |
| 2026-11-13 05:49 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 05:49 | y10 | y10chg-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.57 | +4558.5% | 45.1% | 3.18 |
| 2026-11-13 05:49 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 05:49 | ath | ath-and@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.45 | +1791.4% | 44.2% | 2.24 |
| 2026-11-13 05:49 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 05:49 | y10 | y10chg-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.42 | +423.0% | 35.1% | 3.71 |
| 2026-11-13 05:49 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 05:49 | ath | ath-and@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.41 | +403.4% | 39.1% | 2.18 |
| 2026-11-13 05:49 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 05:49 | y10 | y10chg-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.37 | +413.2% | 61.0% | 2.56 |
| 2026-11-13 05:49 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 05:49 | ath | ath-and@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.53 | +895.2% | 44.6% | 1.37 |
| 2026-11-13 05:49 | baselines | tsmom12@trend3 | baseline | train | 1994-02-01 | 2025-11-09 | 1.11 | +47314.1% | 34.7% | 2.67 |
| 2026-11-13 05:49 | trend3 | trend3-sma200@trend3 | variant | train | 1994-02-01 | 2025-11-09 | 1.10 | +31013.6% | 34.7% | 4.09 |
| 2026-11-13 05:49 | fng | fng-buyfear | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +14005.8% | 47.8% | 3.01 |
| 2026-11-13 05:49 | fng | fng-sellgreed | variant | train | 1994-02-01 | 2025-11-09 | 0.67 | +1443.8% | 34.1% | 2.93 |
| 2026-11-13 05:49 | fng | fng-buyfear@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.44 | +9.1% | 94.0% | 4.94 |
| 2026-11-13 05:49 | trend3 | trend3-10m@trend3 | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +30256.0% | 30.0% | 3.89 |
| 2026-11-13 05:49 | baselines | tsmom12@etf | baseline | train | 2001-05-27 | 2025-11-09 | 0.60 | +227.0% | 16.5% | 2.93 |
| 2026-11-13 05:49 | trend3 | trend3-sma200@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.53 | +181.0% | 16.8% | 3.92 |
| 2026-11-13 05:49 | baselines | tsmom12@coin | baseline | train | 2017-08-18 | 2025-11-09 | 0.54 | +179.5% | 92.4% | 4.62 |
| 2026-11-13 05:49 | trend3 | trend3-sma200@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.50 | +142.3% | 89.8% | 6.11 |
| 2026-11-13 05:49 | baselines | tsmom12@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.45 | +277.9% | 34.8% | 1.69 |
| 2026-11-13 05:49 | trend3 | trend3-sma200@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.74 | +663.8% | 20.5% | 2.68 |
| 2026-11-13 05:49 | baselines | tsmom12@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-13 05:49 | trend3 | trend3-sma200@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.41 | +1295.4% | 47.5% | 3.53 |
| 2026-11-13 05:49 | baselines | tsmom12@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.37 | +349.4% | 39.1% | 2.70 |
| 2026-11-13 05:49 | trend3 | trend3-sma200@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.24 | +126.8% | 43.0% | 4.55 |
| 2026-11-13 05:49 | baselines | tsmom12@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.40 | +495.8% | 58.9% | 1.78 |
| 2026-11-13 05:49 | trend3 | trend3-sma200@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.55 | +1134.7% | 40.9% | 2.62 |
| 2026-11-13 05:50 | fng | fng-buyfear | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +14005.8% | 47.8% | 3.01 |
| 2026-11-13 05:50 | fng | fng-sellgreed | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +9959.2% | 38.7% | 3.90 |
| 2026-11-13 05:50 | fng | fng-buyfear@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.44 | +9.1% | 94.0% | 4.94 |
| 2026-11-13 05:50 | ath | ath-and-d70 | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +8333.7% | 28.9% | 2.74 |
| 2026-11-13 05:50 | ath | ath-and-d130 | robustness | train | 1994-02-01 | 2025-11-09 | 1.10 | +12569.9% | 28.9% | 2.72 |
| 2026-11-13 05:51 | ath | ath-and-short | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +11580.4% | 31.3% | 2.95 |
| 2026-11-13 05:51 | ath | ath-and-coins | robustness | train | 1994-02-01 | 2025-11-09 | 1.13 | +14864.2% | 28.9% | 2.59 |
| 2026-11-13 05:51 | ath | ath-and-stocks | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +16209.3% | 35.8% | 2.97 |
| 2026-11-13 05:51 | bbwp | source video 1 (#1); dead: -0.04 vs tsmom12, 0/5 eras | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | srsi | source video 1 (#2); dead: -0.23 vs tsmom12, out ~half the time | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | ath | source video 1 (#3); dead, nearest miss: +0.08 p=0.18, gain all from coins (4 BTC episodes) | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | gap | source video 2, video 3 (#7); dead: -0.09 vs tsmom12 | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | oil | source video 3 (#8); dead: +0.05 p=0.20, 3/5 eras, mixed out of universe | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | y10 | source video 3 (#9); dead: change -0.04, levels -0.07..-0.01 | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | trend3 | source video 2 (#10); dead: equals its twin (-0.01), it is sma200 | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | fng | source video 4 (#12, stand-in); dead: buy fear -0.10, sell greed -0.08 | note | train | - | - | - | - | - | - |
| 2026-11-13 05:51 | fng | fng-sellgreed rows at 2026-11-13 05:49-05:50 had a bug (no data before 2018 dropped coins); superseded by the rerun | note | train | - | - | - | - | - | - |
| 2026-11-13 09:45 | carry-2-B-out | tsmom12 twin, perp close as spot, 30 bps | baseline | train | 2021-02-20 | 2025-11-09 | 0.07 | -48.3% | 76.1% | 4.16 |
| 2026-11-13 09:45 | carry-2-B-out | tsmom12 perp, perp 10 bps + funding | baseline | train | 2021-02-20 | 2025-11-09 | -0.02 | -59.3% | 78.3% | 4.16 |
| 2026-11-13 09:45 | carry-2-B-out | tsmom12 perp, perp 30 bps + funding | robustness | train | 2021-02-20 | 2025-11-09 | -0.03 | -61.3% | 79.3% | 4.16 |
| 2026-11-13 09:45 | carry-2-B-out | EW perp, perp 10 bps + funding | baseline | train | 2021-02-20 | 2025-11-09 | 0.04 | -84.6% | 92.8% | 3.58 |
| 2026-11-13 09:45 | carry-2-B-out | EW perp, perp 30 bps + funding | robustness | train | 2021-02-20 | 2025-11-09 | 0.02 | -85.5% | 93.2% | 3.58 |
| 2026-11-13 09:45 | carry-2-B-out | ls-premium, perp 10 bps + funding | variant | train | 2021-02-20 | 2025-11-09 | 0.17 | +7.0% | 28.7% | 41.80 |
| 2026-11-13 09:45 | carry-2-B-out | ls-premium, perp 30 bps + funding | robustness | train | 2021-02-20 | 2025-11-09 | -0.36 | -30.0% | 47.3% | 41.80 |
| 2026-11-13 09:45 | carry-2-B-out | ls-premium long leg alone (diagnostic) | robustness | train | 2021-02-20 | 2025-11-09 | -0.01 | -40.0% | 62.0% | 19.97 |
| 2026-11-13 09:45 | carry-2-B-out | ls-premium short leg alone (diagnostic) | robustness | train | 2021-02-20 | 2025-11-09 | 0.12 | -19.5% | 57.7% | 21.83 |
| 2026-11-13 09:45 | carry-2-B-out | ls-funding, perp 10 bps + funding | variant | train | 2021-02-20 | 2025-11-09 | 0.57 | +43.0% | 24.2% | 42.08 |
| 2026-11-13 09:45 | carry-2-B-out | ls-funding, perp 30 bps + funding | robustness | train | 2021-02-20 | 2025-11-09 | -0.02 | -6.6% | 34.7% | 42.08 |
| 2026-11-13 09:45 | carry-2-B-out | ls-funding long leg alone (diagnostic) | robustness | train | 2021-02-20 | 2025-11-09 | 0.08 | -27.0% | 59.5% | 19.49 |
| 2026-11-13 09:45 | carry-2-B-out | ls-funding short leg alone (diagnostic) | robustness | train | 2021-02-20 | 2025-11-09 | 0.16 | -12.5% | 57.3% | 22.59 |
| 2026-11-13 09:45 | carry-2-Bybit | tsmom12 twin, perp close as spot, 30 bps | baseline | train | 2022-05-14 | 2025-11-09 | 0.20 | +1.3% | 51.3% | 5.64 |
| 2026-11-13 09:45 | carry-2-Bybit | tsmom12 perp, perp 10 bps + funding | baseline | train | 2022-05-14 | 2025-11-09 | 0.16 | -4.7% | 52.8% | 5.64 |
| 2026-11-13 09:45 | carry-2-Bybit | tsmom12 perp, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | 0.12 | -8.8% | 53.2% | 5.64 |
| 2026-11-13 09:45 | carry-2-Bybit | EW perp, perp 10 bps + funding | baseline | train | 2022-05-14 | 2025-11-09 | 0.13 | -51.6% | 72.8% | 7.62 |
| 2026-11-13 09:45 | carry-2-Bybit | EW perp, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | 0.10 | -54.6% | 73.6% | 7.62 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-premium, perp 10 bps + funding | variant | train | 2022-05-14 | 2025-11-09 | 0.73 | +41.4% | 19.5% | 42.66 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-premium, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | 0.13 | +3.1% | 23.8% | 42.66 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-premium long leg alone (diagnostic) | robustness | train | 2022-05-14 | 2025-11-09 | 0.18 | -1.2% | 41.0% | 21.30 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-premium short leg alone (diagnostic) | robustness | train | 2022-05-14 | 2025-11-09 | 0.14 | -7.8% | 53.1% | 21.36 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-funding, perp 10 bps + funding | variant | train | 2022-05-14 | 2025-11-09 | 0.31 | +12.9% | 19.5% | 46.16 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-funding, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | -0.35 | -19.6% | 29.5% | 46.16 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-funding long leg alone (diagnostic) | robustness | train | 2022-05-14 | 2025-11-09 | 0.11 | -10.3% | 44.5% | 22.06 |
| 2026-11-13 09:45 | carry-2-Bybit | ls-funding short leg alone (diagnostic) | robustness | train | 2022-05-14 | 2025-11-09 | 0.04 | -19.2% | 53.5% | 24.10 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | tsmom12 twin, perp close as spot, 30 bps | baseline | train | 2023-06-10 | 2025-11-09 | 0.52 | +37.6% | 51.3% | 11.32 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | tsmom12 perp, perp 10 bps + funding | baseline | train | 2023-06-10 | 2025-11-09 | 0.30 | +3.4% | 53.6% | 11.32 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | tsmom12 perp, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | 0.26 | -2.4% | 54.3% | 11.32 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | EW perp, perp 10 bps + funding | baseline | train | 2023-06-10 | 2025-11-09 | -0.07 | -56.3% | 67.3% | 13.04 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | EW perp, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | -0.11 | -59.2% | 69.0% | 13.04 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-premium, perp 10 bps + funding | variant | train | 2023-06-10 | 2025-11-09 | 0.28 | +10.0% | 31.8% | 44.02 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-premium, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | -0.09 | -12.2% | 36.6% | 44.02 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-premium long leg alone (diagnostic) | robustness | train | 2023-06-10 | 2025-11-09 | 0.43 | +25.0% | 41.3% | 22.20 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-premium short leg alone (diagnostic) | robustness | train | 2023-06-10 | 2025-11-09 | -0.18 | -33.1% | 55.2% | 21.82 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-funding, perp 10 bps + funding | variant | train | 2023-06-10 | 2025-11-09 | 0.47 | +23.6% | 27.1% | 44.28 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-funding, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | 0.10 | -1.5% | 27.3% | 44.28 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-funding long leg alone (diagnostic) | robustness | train | 2023-06-10 | 2025-11-09 | 0.59 | +43.6% | 33.4% | 21.93 |
| 2026-11-13 09:45 | carry-2-Hyperliquid | ls-funding short leg alone (diagnostic) | robustness | train | 2023-06-10 | 2025-11-09 | -0.21 | -35.6% | 54.9% | 22.35 |
| 2026-11-13 09:45 | carry-2-pooled | EW perp, equal capital per venue | baseline | train | 2021-02-20 | 2025-11-09 | -0.02 | -86.6% | 93.7% | nan |
| 2026-11-13 09:45 | carry-2-pooled | EW perp @30, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | -0.04 | -87.6% | 94.2% | nan |
| 2026-11-13 09:45 | carry-2-pooled | ls-funding, equal capital per venue | variant | train | 2021-02-20 | 2025-11-09 | 0.69 | +55.8% | 19.1% | nan |
| 2026-11-13 09:45 | carry-2-pooled | ls-funding @30, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.09 | +0.8% | 28.6% | nan |
| 2026-11-13 09:45 | carry-2-pooled | ls-premium, equal capital per venue | variant | train | 2021-02-20 | 2025-11-09 | 0.44 | +30.9% | 26.5% | nan |
| 2026-11-13 09:45 | carry-2-pooled | ls-premium @30, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | -0.12 | -14.3% | 33.2% | nan |
| 2026-11-13 09:45 | carry-2-pooled | tsmom12 perp, equal capital per venue | baseline | train | 2021-02-20 | 2025-11-09 | 0.09 | -49.0% | 75.1% | nan |
| 2026-11-13 09:45 | carry-2-pooled | tsmom12 perp @30, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.06 | -52.2% | 76.1% | nan |
| 2026-11-13 09:45 | carry-2-pooled | tsmom12 twin, equal capital per venue | baseline | train | 2021-02-20 | 2025-11-09 | 0.20 | -29.6% | 71.6% | nan |
| 2026-11-13 09:45 | carry-2-B-all | tsmom12 twin (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.42 | +41.7% | 67.9% | 4.05 |
| 2026-11-13 09:45 | carry-2-B-all | tsmom12 perp (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.30 | +1.8% | 71.3% | 4.05 |
| 2026-11-13 09:45 | carry-2-B-all | tsmom12 perp @30 (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.28 | -3.3% | 72.2% | 4.05 |
| 2026-11-13 09:45 | carry-2-B-all | EW perp (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.26 | -54.8% | 89.5% | 3.23 |
| 2026-11-13 09:45 | carry-2-B-all | EW perp @30 (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.25 | -57.2% | 90.0% | 3.23 |
| 2026-11-13 09:45 | carry-2-B-all | ls-premium (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.81 | +83.0% | 22.4% | 39.78 |
| 2026-11-13 09:45 | carry-2-B-all | ls-premium @30 (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.32 | +21.1% | 35.9% | 39.78 |
| 2026-11-13 09:45 | carry-2-B-all | ls-funding (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 1.17 | +143.0% | 19.8% | 41.19 |
| 2026-11-13 09:45 | carry-2-B-all | ls-funding @30 (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 0.64 | +58.6% | 26.4% | 41.19 |
| 2026-11-13 09:45 | carry-2-B-P30 | tsmom12 twin (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 0.71 | +210.6% | 62.7% | 2.90 |
| 2026-11-13 09:45 | carry-2-B-P30 | tsmom12 perp (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 0.57 | +112.7% | 62.6% | 2.90 |
| 2026-11-13 09:45 | carry-2-B-P30 | tsmom12 perp @30 (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 0.55 | +103.4% | 62.7% | 2.90 |
| 2026-11-13 09:45 | carry-2-B-P30 | EW perp (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 0.47 | +31.0% | 84.0% | 0.80 |
| 2026-11-13 09:45 | carry-2-B-P30 | EW perp @30 (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 0.46 | +26.6% | 84.2% | 0.80 |
| 2026-11-13 09:45 | carry-2-B-P30 | ls-premium (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 1.38 | +284.1% | 15.5% | 38.44 |
| 2026-11-13 09:45 | carry-2-B-P30 | ls-premium @30 (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 1.00 | +158.3% | 29.2% | 38.44 |
| 2026-11-13 09:45 | carry-2-B-P30 | ls-funding (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 1.10 | +176.1% | 16.4% | 38.16 |
| 2026-11-13 09:45 | carry-2-B-P30 | ls-funding @30 (robustness set) | robustness | train | 2021-02-06 | 2025-11-09 | 0.71 | +86.0% | 29.6% | 38.16 |
| 2026-11-18 01:32 | carry-3-B-out | tsmom12 twin | baseline | train | 2021-02-20 | 2025-11-09 | 0.07 | -48.3% | 76.1% | 5.38 |
| 2026-11-18 01:32 | carry-3-B-out | w1 | variant | train | 2021-02-20 | 2025-11-09 | 0.72 | +58.6% | 22.6% | 43.72 |
| 2026-11-18 01:32 | carry-3-B-out | w2 | variant | train | 2021-02-20 | 2025-11-09 | 0.97 | +80.8% | 15.0% | 25.60 |
| 2026-11-18 01:32 | carry-3-B-out | w4 | variant | train | 2021-02-20 | 2025-11-09 | 0.58 | +36.3% | 11.8% | 11.74 |
| 2026-11-18 01:32 | carry-3-B-out | band | variant | train | 2021-02-20 | 2025-11-09 | 0.72 | +54.8% | 17.2% | 29.33 |
| 2026-11-18 01:32 | carry-3-B-out | f30 | variant | train | 2021-02-20 | 2025-11-09 | 0.10 | +1.9% | 23.7% | 21.73 |
| 2026-11-18 01:32 | carry-3-B-out | w1 nocost | robustness | train | 2021-02-20 | 2025-11-09 | 0.87 | +77.0% | 21.0% | 45.06 |
| 2026-11-18 01:32 | carry-3-B-out | w2 nocost | robustness | train | 2021-02-20 | 2025-11-09 | 1.00 | +84.0% | 14.9% | 26.83 |
| 2026-11-18 01:32 | carry-3-B-out | w4 nocost | robustness | train | 2021-02-20 | 2025-11-09 | 0.54 | +33.7% | 13.1% | 15.66 |
| 2026-11-18 01:32 | carry-3-B-out | band nocost | robustness | train | 2021-02-20 | 2025-11-09 | 0.85 | +68.3% | 17.1% | 29.54 |
| 2026-11-18 01:32 | carry-3-B-out | f30 nocost | robustness | train | 2021-02-20 | 2025-11-09 | 0.16 | +6.5% | 22.4% | 23.39 |
| 2026-11-18 01:32 | carry-3-B-out | w1 flat10 | robustness | train | 2021-02-20 | 2025-11-09 | 0.57 | +43.0% | 24.2% | 45.06 |
| 2026-11-18 01:32 | carry-3-B-out | w2 phase 1 | robustness | train | 2021-02-20 | 2025-11-09 | 0.55 | +43.3% | 22.8% | 25.77 |
| 2026-11-18 01:32 | carry-3-B-out | w2 phase 2 | robustness | train | 2021-02-20 | 2025-11-09 | 1.13 | +121.3% | 11.8% | 25.43 |
| 2026-11-18 01:32 | carry-3-B-out | w4 phase 1 | robustness | train | 2021-02-20 | 2025-11-09 | 0.20 | +9.6% | 32.5% | 11.85 |
| 2026-11-18 01:32 | carry-3-B-out | w4 phase 2 | robustness | train | 2021-02-20 | 2025-11-09 | 1.00 | +107.7% | 18.4% | 12.33 |
| 2026-11-18 01:32 | carry-3-B-out | w4 phase 3 | robustness | train | 2021-02-20 | 2025-11-09 | 0.27 | +16.9% | 32.1% | 11.36 |
| 2026-11-18 01:32 | carry-3-B-out | w4 phase 4 | robustness | train | 2021-02-20 | 2025-11-09 | 0.22 | +11.4% | 21.2% | 11.41 |
| 2026-11-18 01:32 | carry-3-B-out | band flat10 | robustness | train | 2021-02-20 | 2025-11-09 | 0.64 | +46.4% | 17.2% | 29.54 |
| 2026-11-18 01:32 | carry-3-B-out | band flat30 | robustness | train | 2021-02-20 | 2025-11-09 | 0.22 | +10.7% | 22.8% | 29.54 |
| 2026-11-18 01:32 | carry-3-B-out | band x2 | robustness | train | 2021-02-20 | 2025-11-09 | 0.67 | +49.9% | 17.2% | 29.33 |
| 2026-11-18 01:32 | carry-3-B-out | band A100k | robustness | train | 2021-02-20 | 2025-11-09 | 0.64 | +46.4% | 17.3% | 29.54 |
| 2026-11-18 01:32 | carry-3-B-out | band A1M | robustness | train | 2021-02-20 | 2025-11-09 | 0.47 | +30.2% | 17.5% | 29.54 |
| 2026-11-18 01:32 | carry-3-B-out | band maker | robustness | train | 2021-02-20 | 2025-11-09 | 0.79 | +61.8% | 17.2% | 29.33 |
| 2026-11-18 01:32 | carry-3-B-out | band top50 | robustness | train | 2021-02-20 | 2025-11-09 | 0.68 | +58.4% | 21.9% | 30.79 |
| 2026-11-18 01:32 | carry-3-B-out | band long leg | robustness | train | 2021-02-20 | 2025-11-09 | 0.13 | -18.2% | 55.8% | 14.04 |
| 2026-11-18 01:32 | carry-3-B-out | band short leg | robustness | train | 2021-02-20 | 2025-11-09 | 0.16 | -12.3% | 56.0% | 15.64 |
| 2026-11-18 01:32 | carry-3-Bybit | tsmom12 twin | baseline | train | 2022-05-14 | 2025-11-09 | 0.20 | +1.3% | 51.3% | 6.20 |
| 2026-11-18 01:32 | carry-3-Bybit | w1 | variant | train | 2022-05-14 | 2025-11-09 | 0.39 | +17.3% | 19.3% | 47.65 |
| 2026-11-18 01:32 | carry-3-Bybit | w2 | variant | train | 2022-05-14 | 2025-11-09 | 0.39 | +15.7% | 15.8% | 27.98 |
| 2026-11-18 01:32 | carry-3-Bybit | w4 | variant | train | 2022-05-14 | 2025-11-09 | -0.07 | -4.9% | 18.4% | 16.35 |
| 2026-11-18 01:32 | carry-3-Bybit | band | variant | train | 2022-05-14 | 2025-11-09 | 0.45 | +19.3% | 17.0% | 33.32 |
| 2026-11-18 01:32 | carry-3-Bybit | f30 | variant | train | 2022-05-14 | 2025-11-09 | 0.37 | +16.4% | 26.3% | 26.45 |
| 2026-11-18 01:32 | carry-3-Bybit | w1 nocost | robustness | train | 2022-05-14 | 2025-11-09 | 0.64 | +33.8% | 18.0% | 48.45 |
| 2026-11-18 01:32 | carry-3-Bybit | w2 nocost | robustness | train | 2022-05-14 | 2025-11-09 | 0.60 | +27.3% | 14.7% | 28.82 |
| 2026-11-18 01:32 | carry-3-Bybit | w4 nocost | robustness | train | 2022-05-14 | 2025-11-09 | 0.07 | +0.7% | 18.0% | 17.28 |
| 2026-11-18 01:32 | carry-3-Bybit | band nocost | robustness | train | 2022-05-14 | 2025-11-09 | 0.63 | +30.0% | 15.2% | 33.34 |
| 2026-11-18 01:32 | carry-3-Bybit | f30 nocost | robustness | train | 2022-05-14 | 2025-11-09 | 0.47 | +22.3% | 24.3% | 27.42 |
| 2026-11-18 01:32 | carry-3-Bybit | w1 flat10 | robustness | train | 2022-05-14 | 2025-11-09 | 0.31 | +12.9% | 19.5% | 48.45 |
| 2026-11-18 01:32 | carry-3-Bybit | w2 phase 1 | robustness | train | 2022-05-14 | 2025-11-09 | 0.47 | +22.2% | 23.4% | 27.86 |
| 2026-11-18 01:32 | carry-3-Bybit | w2 phase 2 | robustness | train | 2022-05-14 | 2025-11-09 | 0.21 | +7.6% | 19.7% | 28.11 |
| 2026-11-18 01:32 | carry-3-Bybit | w4 phase 1 | robustness | train | 2022-05-14 | 2025-11-09 | 0.18 | +5.4% | 18.3% | 16.54 |
| 2026-11-18 01:32 | carry-3-Bybit | w4 phase 2 | robustness | train | 2022-05-14 | 2025-11-09 | 0.38 | +17.7% | 20.5% | 16.38 |
| 2026-11-18 01:32 | carry-3-Bybit | w4 phase 3 | robustness | train | 2022-05-14 | 2025-11-09 | -0.34 | -20.4% | 30.9% | 16.10 |
| 2026-11-18 01:32 | carry-3-Bybit | w4 phase 4 | robustness | train | 2022-05-14 | 2025-11-09 | -0.39 | -22.7% | 39.4% | 16.40 |
| 2026-11-18 01:32 | carry-3-Bybit | band flat10 | robustness | train | 2022-05-14 | 2025-11-09 | 0.38 | +15.7% | 17.6% | 33.34 |
| 2026-11-18 01:32 | carry-3-Bybit | band flat30 | robustness | train | 2022-05-14 | 2025-11-09 | -0.12 | -8.4% | 25.0% | 33.34 |
| 2026-11-18 01:32 | carry-3-Bybit | band x2 | robustness | train | 2022-05-14 | 2025-11-09 | 0.38 | +15.7% | 18.0% | 33.32 |
| 2026-11-18 01:32 | carry-3-Bybit | band A100k | robustness | train | 2022-05-14 | 2025-11-09 | 0.35 | +14.1% | 18.2% | 33.34 |
| 2026-11-18 01:32 | carry-3-Bybit | band A1M | robustness | train | 2022-05-14 | 2025-11-09 | 0.11 | +1.9% | 22.1% | 33.34 |
| 2026-11-18 01:32 | carry-3-Bybit | band maker | robustness | train | 2022-05-14 | 2025-11-09 | 0.54 | +24.5% | 15.7% | 33.32 |
| 2026-11-18 01:32 | carry-3-Bybit | band top50 | robustness | train | 2022-05-14 | 2025-11-09 | 0.29 | +11.7% | 17.1% | 34.36 |
| 2026-11-18 01:32 | carry-3-Bybit | band long leg | robustness | train | 2022-05-14 | 2025-11-09 | 0.19 | +0.1% | 41.4% | 15.89 |
| 2026-11-18 01:32 | carry-3-Bybit | band short leg | robustness | train | 2022-05-14 | 2025-11-09 | 0.01 | -22.2% | 55.9% | 17.71 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | tsmom12 twin | baseline | train | 2023-06-10 | 2025-11-09 | 0.52 | +37.6% | 51.3% | 11.91 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w1 | variant | train | 2023-06-10 | 2025-11-09 | 0.50 | +25.7% | 27.1% | 46.53 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w2 | variant | train | 2023-06-10 | 2025-11-09 | 0.66 | +34.2% | 33.0% | 27.88 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w4 | variant | train | 2023-06-10 | 2025-11-09 | 0.51 | +24.1% | 37.3% | 16.56 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band | variant | train | 2023-06-10 | 2025-11-09 | 0.61 | +31.9% | 26.9% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | f30 | variant | train | 2023-06-10 | 2025-11-09 | 0.30 | +10.9% | 34.8% | 29.24 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w1 nocost | robustness | train | 2023-06-10 | 2025-11-09 | 0.66 | +38.4% | 26.9% | 46.61 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w2 nocost | robustness | train | 2023-06-10 | 2025-11-09 | 0.75 | +41.3% | 33.0% | 27.96 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w4 nocost | robustness | train | 2023-06-10 | 2025-11-09 | 0.58 | +28.7% | 37.2% | 16.64 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band nocost | robustness | train | 2023-06-10 | 2025-11-09 | 0.74 | +42.1% | 26.7% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | f30 nocost | robustness | train | 2023-06-10 | 2025-11-09 | 0.39 | +17.5% | 33.9% | 29.34 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w1 flat10 | robustness | train | 2023-06-10 | 2025-11-09 | 0.47 | +23.6% | 27.1% | 46.61 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w2 phase 1 | robustness | train | 2023-06-10 | 2025-11-09 | -0.02 | -8.5% | 31.1% | 27.63 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w2 phase 2 | robustness | train | 2023-06-10 | 2025-11-09 | 1.10 | +88.3% | 38.6% | 28.13 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w4 phase 1 | robustness | train | 2023-06-10 | 2025-11-09 | 0.15 | +0.2% | 39.1% | 16.46 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w4 phase 2 | robustness | train | 2023-06-10 | 2025-11-09 | 1.01 | +88.5% | 46.7% | 17.36 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w4 phase 3 | robustness | train | 2023-06-10 | 2025-11-09 | 0.13 | -1.3% | 35.9% | 16.84 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | w4 phase 4 | robustness | train | 2023-06-10 | 2025-11-09 | 0.25 | +7.6% | 38.6% | 15.59 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band flat10 | robustness | train | 2023-06-10 | 2025-11-09 | 0.58 | +30.1% | 26.9% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band flat30 | robustness | train | 2023-06-10 | 2025-11-09 | 0.27 | +9.2% | 27.1% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band x2 | robustness | train | 2023-06-10 | 2025-11-09 | 0.55 | +27.4% | 27.0% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band A100k | robustness | train | 2023-06-10 | 2025-11-09 | 0.50 | +23.9% | 27.0% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band A1M | robustness | train | 2023-06-10 | 2025-11-09 | 0.15 | +1.7% | 27.5% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band maker | robustness | train | 2023-06-10 | 2025-11-09 | 0.67 | +36.8% | 26.8% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band top50 | robustness | train | 2023-06-10 | 2025-11-09 | 0.61 | +31.9% | 26.9% | 36.12 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band long leg | robustness | train | 2023-06-10 | 2025-11-09 | 0.57 | +40.9% | 34.1% | 18.26 |
| 2026-11-18 01:32 | carry-3-Hyperliquid | band short leg | robustness | train | 2023-06-10 | 2025-11-09 | -0.13 | -29.0% | 52.5% | 18.58 |
| 2026-11-18 01:32 | carry-3-pooled | tsmom12 twin, equal capital per venue | baseline | train | 2021-02-20 | 2025-11-09 | 0.20 | -29.6% | 71.6% | 6.82 |
| 2026-11-18 01:32 | carry-3-pooled | w1, equal capital per venue | variant | train | 2021-02-20 | 2025-11-09 | 0.78 | +65.9% | 18.0% | 45.32 |
| 2026-11-18 01:32 | carry-3-pooled | w2, equal capital per venue | variant | train | 2021-02-20 | 2025-11-09 | 1.01 | +86.1% | 15.0% | 26.87 |
| 2026-11-18 01:32 | carry-3-pooled | w4, equal capital per venue | variant | train | 2021-02-20 | 2025-11-09 | 0.69 | +44.7% | 16.3% | 14.73 |
| 2026-11-18 01:32 | carry-3-pooled | band, equal capital per venue | variant | train | 2021-02-20 | 2025-11-09 | 0.79 | +62.4% | 17.2% | 31.69 |
| 2026-11-18 01:32 | carry-3-pooled | f30, equal capital per venue | variant | train | 2021-02-20 | 2025-11-09 | 0.29 | +15.8% | 18.7% | 24.88 |
| 2026-11-18 01:32 | carry-3-pooled | w1 nocost, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.99 | +93.7% | 17.5% | 46.04 |
| 2026-11-18 01:32 | carry-3-pooled | w2 nocost, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 1.13 | +101.0% | 14.9% | 27.57 |
| 2026-11-18 01:32 | carry-3-pooled | w4 nocost, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.75 | +50.1% | 14.5% | 16.34 |
| 2026-11-18 01:32 | carry-3-pooled | band nocost, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.96 | +81.1% | 17.1% | 31.77 |
| 2026-11-18 01:32 | carry-3-pooled | f30 nocost, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.39 | +24.3% | 16.7% | 25.77 |
| 2026-11-18 01:32 | carry-3-pooled | w1 flat10, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.69 | +55.8% | 19.1% | 46.04 |
| 2026-11-18 01:32 | carry-3-pooled | w2 phase 1, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.56 | +42.8% | 23.4% | 27.07 |
| 2026-11-18 01:32 | carry-3-pooled | w2 phase 2, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 1.22 | +136.6% | 14.6% | 26.67 |
| 2026-11-18 01:32 | carry-3-pooled | w4 phase 1, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.45 | +34.8% | 23.6% | 15.02 |
| 2026-11-18 01:32 | carry-3-pooled | w4 phase 2, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 1.29 | +156.7% | 21.5% | 14.92 |
| 2026-11-18 01:32 | carry-3-pooled | w4 phase 3, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.19 | +8.8% | 32.1% | 14.61 |
| 2026-11-18 01:32 | carry-3-pooled | w4 phase 4, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.11 | +2.4% | 27.0% | 14.37 |
| 2026-11-18 01:32 | carry-3-pooled | band flat10, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.73 | +55.8% | 17.2% | 31.77 |
| 2026-11-18 01:32 | carry-3-pooled | band flat30, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.28 | +15.4% | 21.8% | 31.77 |
| 2026-11-18 01:32 | carry-3-pooled | band x2, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.73 | +55.6% | 17.2% | 31.69 |
| 2026-11-18 01:32 | carry-3-pooled | band A100k, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.69 | +51.6% | 17.3% | 31.77 |
| 2026-11-18 01:32 | carry-3-pooled | band A1M, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.41 | +25.5% | 19.9% | 31.77 |
| 2026-11-18 01:32 | carry-3-pooled | band maker, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.87 | +71.4% | 17.2% | 31.69 |
| 2026-11-18 01:32 | carry-3-pooled | band top50, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.75 | +60.7% | 17.2% | 32.66 |
| 2026-11-18 01:32 | carry-3-pooled | band long leg, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.14 | -13.4% | 58.0% | 15.41 |
| 2026-11-18 01:32 | carry-3-pooled | band short leg, equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 0.16 | -11.1% | 55.9% | 16.82 |
| 2026-11-18 01:32 | carry-3-pooled | band (B-all for B-out), equal capital per venue | robustness | train | 2021-02-20 | 2025-11-09 | 1.07 | +107.7% | 15.9% | 31.32 |
| 2026-11-18 01:32 | carry-3-B-all | band (robustness set) | robustness | train | 2021-01-23 | 2025-11-09 | 1.15 | +120.7% | 15.9% | 28.18 |
| 2026-11-18 01:32 | carry-3-B-out | weekly cross-sectional IC, 7-day funding vs next week's price: -0.011 (t -1.1, 245 weeks) | robustness | train | 2021-02-20 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-B-out | weekly cross-sectional IC, 7-day funding vs next week's price + funding: +0.009 (t +0.9, 245 weeks) | robustness | train | 2021-02-20 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-B-out | weekly cross-sectional IC, 30-day funding vs next week's price: -0.018 (t -1.9, 245 weeks) | robustness | train | 2021-02-20 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-B-out | weekly cross-sectional IC, 30-day funding vs next week's price + funding: +0.000 (t +0.0, 245 weeks) | robustness | train | 2021-02-20 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Bybit | weekly cross-sectional IC, 7-day funding vs next week's price: +0.007 (t +0.5, 181 weeks) | robustness | train | 2022-05-14 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Bybit | weekly cross-sectional IC, 7-day funding vs next week's price + funding: +0.027 (t +1.8, 181 weeks) | robustness | train | 2022-05-14 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Bybit | weekly cross-sectional IC, 30-day funding vs next week's price: -0.002 (t -0.1, 181 weeks) | robustness | train | 2022-05-14 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Bybit | weekly cross-sectional IC, 30-day funding vs next week's price + funding: +0.017 (t +1.1, 181 weeks) | robustness | train | 2022-05-14 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Hyperliquid | weekly cross-sectional IC, 7-day funding vs next week's price: +0.024 (t +0.7, 73 weeks) | robustness | train | 2023-06-10 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Hyperliquid | weekly cross-sectional IC, 7-day funding vs next week's price + funding: +0.045 (t +1.4, 73 weeks) | robustness | train | 2023-06-10 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Hyperliquid | weekly cross-sectional IC, 30-day funding vs next week's price: +0.022 (t +0.7, 73 weeks) | robustness | train | 2023-06-10 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-Hyperliquid | weekly cross-sectional IC, 30-day funding vs next week's price + funding: +0.041 (t +1.3, 73 weeks) | robustness | train | 2023-06-10 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-B-all | weekly cross-sectional IC, 7-day funding vs next week's price: +0.003 (t +0.3, 249 weeks) | robustness | train | 2021-01-23 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-B-all | weekly cross-sectional IC, 7-day funding vs next week's price + funding: +0.023 (t +2.5, 249 weeks) | robustness | train | 2021-01-23 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-B-all | weekly cross-sectional IC, 30-day funding vs next week's price: -0.004 (t -0.5, 249 weeks) | robustness | train | 2021-01-23 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:32 | carry-3-B-all | weekly cross-sectional IC, 30-day funding vs next week's price + funding: +0.014 (t +1.5, 249 weeks) | robustness | train | 2021-01-23 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:01 | carry-3 | claim: the one held-out run of carry-3 starts | variant | heldout | 2025-11-11 | 2026-11-09 | - | - | - | - |
| 2026-11-18 11:01 | carry-3-B-out | tsmom12 twin | baseline | heldout | 2025-11-11 | 2026-11-10 | -0.17 | -2.5% | 9.0% | 2.84 |
| 2026-11-18 11:01 | carry-3-B-out | band | variant | heldout | 2025-11-11 | 2026-11-10 | -0.29 | -5.8% | 22.1% | 27.15 |
| 2026-11-18 11:01 | carry-3-B-out | band nocost | robustness | heldout | 2025-11-11 | 2026-11-10 | -0.18 | -4.1% | 21.2% | 27.26 |
| 2026-11-18 11:01 | carry-3-B-out | band flat10 | robustness | heldout | 2025-11-11 | 2026-11-10 | -0.35 | -6.7% | 22.3% | 27.26 |
| 2026-11-18 11:01 | carry-3-B-out | band x2 | robustness | heldout | 2025-11-11 | 2026-11-10 | -0.34 | -6.5% | 22.4% | 27.15 |
| 2026-11-18 11:01 | carry-3-Bybit | tsmom12 twin | baseline | heldout | 2025-11-11 | 2026-11-10 | -0.65 | -8.4% | 11.1% | 2.76 |
| 2026-11-18 11:01 | carry-3-Bybit | band | variant | heldout | 2025-11-11 | 2026-11-10 | 0.51 | +7.0% | 15.3% | 30.18 |
| 2026-11-18 11:01 | carry-3-Bybit | band nocost | robustness | heldout | 2025-11-11 | 2026-11-10 | 0.67 | +9.7% | 14.6% | 30.18 |
| 2026-11-18 11:01 | carry-3-Bybit | band flat10 | robustness | heldout | 2025-11-11 | 2026-11-10 | 0.48 | +6.4% | 15.4% | 30.18 |
| 2026-11-18 11:01 | carry-3-Bybit | band x2 | robustness | heldout | 2025-11-11 | 2026-11-10 | 0.46 | +6.1% | 15.5% | 30.18 |
| 2026-11-18 11:01 | carry-3-Hyperliquid | tsmom12 twin | baseline | heldout | 2025-11-11 | 2026-11-10 | 0.15 | +1.0% | 18.1% | 4.44 |
| 2026-11-18 11:01 | carry-3-Hyperliquid | band | variant | heldout | 2025-11-11 | 2026-11-10 | -1.33 | -24.8% | 31.3% | 31.82 |
| 2026-11-18 11:01 | carry-3-Hyperliquid | band nocost | robustness | heldout | 2025-11-11 | 2026-11-10 | -1.21 | -23.1% | 29.9% | 31.82 |
| 2026-11-18 11:01 | carry-3-Hyperliquid | band flat10 | robustness | heldout | 2025-11-11 | 2026-11-10 | -1.37 | -25.5% | 31.9% | 31.82 |
| 2026-11-18 11:01 | carry-3-Hyperliquid | band x2 | robustness | heldout | 2025-11-11 | 2026-11-10 | -1.38 | -25.5% | 31.9% | 31.82 |
| 2026-11-18 11:01 | carry-3-pooled | tsmom12 twin, equal capital per venue | baseline | heldout | 2025-11-11 | 2026-11-10 | -0.21 | -3.1% | 9.6% | 3.35 |
| 2026-11-18 11:01 | carry-3-pooled | band, equal capital per venue | variant | heldout | 2025-11-11 | 2026-11-10 | -0.65 | -8.1% | 18.2% | 29.72 |
| 2026-11-18 11:01 | carry-3-pooled | band nocost, equal capital per venue | robustness | heldout | 2025-11-11 | 2026-11-10 | -0.47 | -6.1% | 17.6% | 29.75 |
| 2026-11-18 11:01 | carry-3-pooled | band flat10, equal capital per venue | robustness | heldout | 2025-11-11 | 2026-11-10 | -0.72 | -8.8% | 18.3% | 29.75 |
| 2026-11-18 11:01 | carry-3-pooled | band x2, equal capital per venue | robustness | heldout | 2025-11-11 | 2026-11-10 | -0.72 | -8.9% | 18.3% | 29.72 |
| 2026-11-17 23:25 | vol-echo | echo21@SPY | variant | train | 1994-02-01 | 2025-11-09 | 0.25 | +56.0% | 23.4% | 20.77 |
| 2026-11-17 23:25 | vol-echo | constant@SPY | baseline | train | 1994-02-01 | 2025-11-09 | 0.63 | +66.5% | 9.6% | 0.05 |
| 2026-11-17 23:25 | auction-concession | six | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +19941.1% | 35.9% | 4.23 |
| 2026-11-17 23:25 | vol-echo | echo21@QQQ | variant | train | 2000-03-10 | 2025-11-09 | 0.13 | +20.8% | 38.6% | 20.32 |
| 2026-11-17 23:25 | vol-echo | constant@QQQ | baseline | train | 2000-03-10 | 2025-11-09 | 0.41 | +46.3% | 19.1% | 0.09 |
| 2026-11-17 23:25 | auction-concession | tlt@TLT | variant | train | 2003-07-31 | 2025-11-09 | 0.50 | +242.4% | 44.1% | 25.35 |
| 2026-11-17 23:25 | auction-concession | constant@TLT | baseline | train | 2003-07-31 | 2025-11-09 | 0.33 | +97.2% | 39.7% | 0.07 |
| 2026-11-17 23:25 | vol-echo | echo21@IWM | robustness | train | 2001-05-27 | 2025-11-09 | 0.04 | -0.0% | 35.7% | 17.67 |
| 2026-11-17 23:25 | vol-echo | constant@IWM | baseline | train | 2001-05-27 | 2025-11-09 | 0.43 | +33.3% | 8.8% | 0.05 |
| 2026-11-17 23:25 | auction-concession | six@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.57 | +207.8% | 16.9% | 6.11 |
| 2026-11-17 23:25 | vol-echo | echo21@EFA | robustness | train | 2002-08-28 | 2025-11-09 | -0.01 | -8.9% | 27.8% | 21.09 |
| 2026-11-17 23:25 | vol-echo | constant@EFA | baseline | train | 2002-08-28 | 2025-11-09 | 0.45 | +33.5% | 10.8% | 0.06 |
| 2026-11-17 23:25 | auction-concession | tlt@IEF | robustness | train | 2003-07-31 | 2025-11-09 | 0.26 | +34.5% | 22.7% | 41.34 |
| 2026-11-17 23:25 | auction-concession | constant@IEF | baseline | train | 2003-07-31 | 2025-11-09 | 0.55 | +69.4% | 16.2% | 0.05 |
| 2026-11-17 23:25 | vol-echo | echo21@EEM | robustness | train | 2004-04-14 | 2025-11-09 | -0.09 | -24.6% | 36.8% | 19.07 |
| 2026-11-17 23:25 | vol-echo | constant@EEM | baseline | train | 2004-04-14 | 2025-11-09 | 0.36 | +30.7% | 11.9% | 0.07 |
| 2026-11-17 23:25 | vol-echo | echo21@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.24 | +118.8% | 40.6% | 19.26 |
| 2026-11-17 23:25 | vol-echo | constant@N225 | baseline | train | 1966-01-06 | 2025-11-09 | 0.40 | +84.8% | 16.2% | 0.05 |
| 2026-11-17 23:25 | vol-echo | echo21@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.38 | +116.4% | 18.0% | 19.26 |
| 2026-11-17 23:25 | vol-echo | constant@FTSE | baseline | train | 1985-01-03 | 2025-11-09 | 0.39 | +40.6% | 8.1% | 0.04 |
| 2026-11-17 23:25 | vol-echo | echo21@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.27 | +85.2% | 20.9% | 21.04 |
| 2026-11-17 23:25 | vol-echo | constant@GDAXI | baseline | train | 1988-12-30 | 2025-11-09 | 0.47 | +64.7% | 14.7% | 0.06 |
| 2026-11-17 23:25 | vol-echo | echo21@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.42 | +71.6% | 14.6% | 18.61 |
| 2026-11-17 23:25 | vol-echo | constant@GSPC | baseline | train | 1962-01-02 | 1993-01-27 | 0.51 | +29.9% | 7.2% | 0.03 |
| 2026-11-17 23:25 | vol-echo | echo63@SPY | variant | train | 1994-02-01 | 2025-11-09 | -0.22 | -27.8% | 43.0% | 10.79 |
| 2026-11-17 23:25 | vol-echo | constant@SPY | baseline | train | 1994-02-01 | 2025-11-09 | 0.63 | +32.3% | 5.2% | 0.02 |
| 2026-11-17 23:25 | vol-echo | echo63@QQQ | variant | train | 2000-03-10 | 2025-11-09 | -0.17 | -25.7% | 39.0% | 10.48 |
| 2026-11-17 23:25 | vol-echo | constant@QQQ | baseline | train | 2000-03-10 | 2025-11-09 | 0.41 | +21.7% | 9.7% | 0.03 |
| 2026-11-17 23:25 | rebalance-pressure | me | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +17811.8% | 37.3% | 5.41 |
| 2026-11-17 23:26 | rebalance-pressure | me-rebound | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +17026.1% | 39.8% | 6.97 |
| 2026-11-17 23:26 | contagion-catchup | TS@etf21 | baseline | train | 1999-12-22 | 2025-11-09 | 0.60 | +284.3% | 20.8% | 2.67 |
| 2026-11-17 23:26 | contagion-catchup | EW@etf21 | baseline | train | 1999-12-22 | 2025-11-09 | 0.55 | +549.2% | 41.5% | 0.17 |
| 2026-11-17 23:26 | contagion-catchup | rev7@etf21 | baseline | train | 1999-12-22 | 2025-11-09 | 0.53 | +268.2% | 20.6% | 48.04 |
| 2026-11-17 23:26 | contagion-catchup | catchup@etf21 | variant | train | 1999-12-22 | 2025-11-09 | 0.50 | +232.7% | 21.4% | 47.91 |
| 2026-11-17 23:26 | contagion-catchup | nbr@etf21 | variant | train | 1999-12-22 | 2025-11-09 | 0.33 | +101.0% | 36.8% | 49.42 |
| 2026-11-17 23:26 | rebalance-pressure | me@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.63 | +242.7% | 15.8% | 6.89 |
| 2026-11-17 23:26 | contagion-catchup | TS@coin8 | baseline | train | 2019-08-08 | 2025-11-09 | 0.74 | +401.7% | 64.3% | 4.19 |
| 2026-11-17 23:26 | contagion-catchup | EW@coin8 | baseline | train | 2019-08-08 | 2025-11-09 | 0.81 | +659.8% | 83.4% | 2.49 |
| 2026-11-17 23:26 | contagion-catchup | catchup@coin8 | robustness | train | 2019-08-08 | 2025-11-09 | 0.38 | +14.9% | 70.2% | 46.05 |
| 2026-11-18 11:10 | month-end-bonds | last4@LQD | variant | train | 2002-07-31 | 2025-11-09 | 0.52 | +65.4% | 11.6% | 23.96 |
| 2026-11-18 11:10 | month-end-bonds | last4@TLT-y1 | variant | train | 2002-07-31 | 2003-07-29 | 0.22 | +1.1% | 4.9% | 22.05 |
| 2026-11-18 11:10 | month-end-bonds | constant@LQD | baseline | train | 2002-07-31 | 2025-11-09 | 0.60 | +24.4% | 5.2% | 0.03 |
| 2026-11-18 11:10 | month-end-bonds | hold@LQD | baseline | train | 2002-07-31 | 2025-11-09 | 0.59 | +190.0% | 25.0% | 0.02 |
| 2026-11-18 11:13 | trend-age | age4 | variant | train | 1994-02-01 | 2025-11-09 | 0.99 | +12259.5% | 37.9% | 1.93 |
| 2026-11-18 11:13 | trend-age | age4@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.60 | +206.1% | 17.0% | 1.65 |
| 2026-11-18 11:13 | trend-age | age4@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.37 | +13.7% | 90.8% | 3.44 |
| 2026-11-18 11:13 | trend-age | age4@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.41 | +225.9% | 33.2% | 1.10 |
| 2026-11-18 11:13 | trend-age | age4@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.53 | +3554.2% | 45.0% | 1.46 |
| 2026-11-18 11:13 | trend-age | age4@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.28 | +179.5% | 40.4% | 1.50 |
| 2026-11-18 11:13 | trend-age | age4@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.47 | +773.7% | 55.2% | 0.97 |
| 2026-11-18 11:16 | patch-leaving | mvt | variant | train | 1994-02-01 | 2025-11-09 | 0.85 | +22498.4% | 53.2% | 9.69 |
| 2026-11-18 11:16 | patch-leaving | mvt@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.54 | +218.3% | 20.1% | 8.70 |
| 2026-11-18 11:17 | patch-leaving | mvt@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.14 | -78.6% | 97.4% | 9.95 |
| 2026-11-18 11:17 | patch-leaving | mvt@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.66 | +5694.5% | 33.3% | 9.16 |
| 2026-11-18 11:19 | crowded-trend | crowd | variant | train | 1994-02-01 | 2025-11-09 | 0.98 | +7879.3% | 28.9% | 3.30 |
| 2026-11-18 11:19 | crowded-trend | crowd@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.47 | +122.0% | 16.2% | 3.85 |
| 2026-11-18 11:19 | crowded-trend | crowd@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.59 | +349.3% | 91.5% | 4.95 |
| 2026-11-18 11:19 | crowded-trend | crowd@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.71 | +1932.4% | 24.6% | 2.88 |
| 2026-11-18 19:08 | hedge-regime | hedge | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +18562.6% | 35.8% | 2.57 |
| 2026-11-18 19:08 | hedge-regime | hedge@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.59 | +223.1% | 16.5% | 2.85 |
| 2026-11-18 19:11 | attention-peak | peak | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +12638.8% | 37.6% | 2.91 |
| 2026-11-18 19:11 | attention-peak | peak@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.33 | +21.8% | 86.9% | 6.77 |
| 2026-11-18 19:16 | opex-pin | pin | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +19229.9% | 40.6% | 9.41 |
| 2026-11-18 19:16 | opex-pin | pin-after | robustness | train | 1994-02-01 | 2025-11-09 | 1.03 | +21200.1% | 35.3% | 9.37 |
| 2026-11-18 19:16 | opex-pin | pin@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.46 | +207.5% | 28.8% | 10.53 |
| 2026-11-18 19:16 | opex-pin | pin@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.64 | +4060.7% | 36.3% | 8.66 |
| 2026-11-18 19:28 | tax-drain | drain | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +16594.3% | 37.9% | 5.74 |
| 2026-11-18 19:28 | tax-drain | drain-ttl | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +16177.2% | 36.5% | 3.02 |
| 2026-11-18 19:28 | tax-drain | drain@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.59 | +212.7% | 17.0% | 5.52 |
| 2026-11-18 19:28 | tax-drain | drain@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.72 | +4188.6% | 26.7% | 3.41 |
| 2026-11-18 19:39 | coupon-dose | dose | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +17793.6% | 36.3% | 6.34 |
| 2026-11-18 19:39 | coupon-dose | dose-neg | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +17447.2% | 36.8% | 5.86 |
| 2026-11-18 19:39 | coupon-dose | dose@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.57 | +209.4% | 18.5% | 6.89 |
| 2026-11-18 20:12 | fomc-cycle | even-gate | variant | train | 1994-02-01 | 2025-11-09 | 1.22 | +24221.9% | 36.2% | 17.38 |
| 2026-11-18 20:12 | fomc-cycle | even-overlay | variant | train | 1994-02-01 | 2025-11-09 | 0.96 | +20181.7% | 53.1% | 17.21 |
| 2026-11-18 20:12 | fomc-cycle | odd-gate | robustness | train | 1994-02-01 | 2025-11-09 | 0.65 | +1573.6% | 56.0% | 19.48 |
| 2026-11-18 20:12 | fomc-cycle | even-gate@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.67 | +183.9% | 14.5% | 15.67 |
| 2026-11-18 20:12 | fomc-cycle | even-overlay@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.58 | +458.1% | 25.9% | 20.38 |
| 2026-11-18 20:12 | fomc-cycle | even-gate@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.75 | +2625.4% | 25.7% | 30.43 |
| 2026-11-18 20:12 | fomc-cycle | even-overlay@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.71 | +8053.7% | 42.7% | 15.17 |
| 2026-11-18 20:21 | xtsmom | xtsmom | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +13381.0% | 35.3% | 3.47 |
| 2026-11-18 20:21 | xtsmom | xtsmom-b6 | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +12010.0% | 34.5% | 3.86 |
| 2026-11-18 20:21 | xtsmom | xtsmom-full | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +11269.4% | 39.0% | 3.08 |
| 2026-11-18 20:21 | xtsmom | xtsmom-tlt | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +15980.7% | 34.5% | 3.57 |
| 2026-11-18 20:21 | xtsmom | xtsmom@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.66 | +225.0% | 16.5% | 3.39 |
| 2026-11-18 20:21 | xtsmom | xtsmom-b6@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.51 | +135.3% | 15.5% | 3.78 |
| 2026-11-18 20:21 | xtsmom | xtsmom-full@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.59 | +185.2% | 18.2% | 3.46 |
| 2026-11-18 20:21 | xtsmom | xtsmom@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.86 | +4363.4% | 23.9% | 3.06 |
| 2026-11-18 20:21 | xtsmom | xtsmom-b6@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.83 | +3224.1% | 22.0% | 4.17 |
| 2026-11-18 22:13 | ts-carry | carry | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +5073.4% | 41.4% | 2.57 |
| 2026-11-18 22:13 | ts-carry | carry-mean | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +18364.7% | 36.5% | 2.74 |
| 2026-11-18 22:13 | ts-carry | carry-bond | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +18324.5% | 38.8% | 2.76 |
| 2026-11-18 22:13 | ts-carry | carry-equity | robustness | train | 1994-02-01 | 2025-11-09 | 0.97 | +5114.2% | 39.4% | 2.59 |
| 2026-11-18 22:13 | ts-carry | carry@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.48 | +109.7% | 16.3% | 2.63 |
| 2026-11-18 22:13 | ts-carry | carry-mean@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.60 | +227.0% | 16.5% | 2.93 |
| 2026-11-18 22:13 | ts-carry | carry@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | -0.10 | -3.9% | 9.9% | 0.26 |
| 2026-11-18 22:13 | ts-carry | carry-mean@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.45 | +277.9% | 34.8% | 1.69 |
| 2026-11-18 22:14 | ts-carry | carry-mean | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +7824.5% | 39.8% | 2.19 |
| 2026-11-18 22:14 | ts-carry | carry-mean@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.48 | +113.9% | 13.9% | 2.65 |
| 2026-11-18 22:14 | ts-carry | carry-mean@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.46 | +102.3% | 15.8% | 1.75 |
| 2026-11-18 22:15 | halloween | halloween | variant | train | 1994-02-01 | 2025-11-09 | 0.96 | +6878.8% | 38.8% | 3.16 |
| 2026-11-18 22:15 | halloween | halloween-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +7159.9% | 49.4% | 3.01 |
| 2026-11-18 22:15 | halloween | halloween@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.69 | +198.8% | 16.5% | 2.74 |
| 2026-11-18 22:15 | halloween | halloween-alone@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.68 | +300.4% | 22.5% | 2.56 |
| 2026-11-18 22:15 | halloween | halloween@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.85 | +2137.7% | 22.9% | 2.51 |
| 2026-11-18 22:15 | halloween | halloween-alone@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.85 | +9224.4% | 33.1% | 2.11 |
| 2026-11-18 22:28 | survey-5 | tsmom12@live-L | live-check | train | 2010-02-01 | 2025-10-31 | 1.36 | +4708.5% | 36.5% | 2.74 |
| 2026-11-18 22:28 | survey-5 | tsmom12-c00@live-L | live-check | train | 2010-02-01 | 2025-10-31 | 1.07 | +294.4% | 15.8% | 2.16 |
| 2026-11-18 22:28 | survey-5 | where-vol@live-L | live-check | train | 2010-02-01 | 2025-10-31 | 1.40 | +6314.8% | 35.3% | 1.71 |
| 2026-11-18 22:28 | survey-5 | sixty-forty@live-L | live-check | train | 2010-02-01 | 2025-10-31 | 1.01 | +375.4% | 27.3% | 0.47 |
| 2026-11-18 22:45 | ls-trend-1 | wide-LS@live-L | replication | train | 2010-02-01 | 2025-10-31 | 0.15 | +20.6% | 30.1% | 11.96 |
| 2026-11-18 22:45 | ls-trend-1 | wide-LO@live-L | replication | train | 2010-02-01 | 2025-10-31 | 0.24 | +42.4% | 27.7% | 6.57 |
| 2026-11-18 22:45 | ls-trend-1 | narrow-LS@live-L | replication | train | 2010-02-01 | 2025-10-31 | 0.58 | +500.2% | 47.9% | 8.85 |
| 2026-11-18 22:45 | ls-trend-1 | narrow-LO@live-L | replication | train | 2010-02-01 | 2025-10-31 | 0.93 | +1618.7% | 38.1% | 5.24 |
| 2026-11-18 22:56 | ls-trend-2 | blend-er@L07 | variant | train | 2007-04-01 | 2025-10-31 | 0.97 | +158.0% | 8.8% | 3.26 |
| 2026-11-18 22:56 | ls-trend-2 | blend-er@L | robustness | train | 2010-02-01 | 2025-10-31 | 1.13 | +136.0% | 7.6% | 3.26 |
| 2026-11-18 22:56 | ls-trend-2 | blend-er@F | robustness | train | 1995-03-01 | 2025-10-31 | 0.79 | +542.5% | 19.7% | 3.26 |
| 2026-11-18 22:56 | ls-trend-2 | blend-er-cost2@L07 | robustness | train | 2007-04-01 | 2025-10-31 | 0.83 | +124.0% | 9.0% | 3.26 |
| 2026-11-18 22:56 | ls-trend-2 | tsmom12-split-bills@L07 | baseline | train | 2007-04-01 | 2025-10-31 | 1.26 | +130.9% | 5.6% | 0.71 |
| 2026-11-18 22:56 | ls-trend-2 | wide-LS-g1@L07 | replication | train | 2007-04-01 | 2025-10-31 | 0.14 | +11.8% | 16.2% | 2.82 |
| 2026-11-18 22:57 | ls-trend-2 | hop-wide-LS@live-L | replication | train | 2010-02-01 | 2025-10-31 | -0.09 | -28.9% | 45.9% | 28.55 |
| 2026-11-18 22:57 | ls-trend-2 | hop-wide-LS-g1@live-L | replication | train | 2010-02-01 | 2025-10-31 | -0.04 | -4.6% | 17.9% | 10.05 |
| 2026-11-18 22:57 | ls-trend-2 | gspc-12m@1961 | replication | train | 1961-01-01 | 2025-10-31 | 0.22 | +6.6% | 95.0% | 9.24 |
| 2026-11-18 22:57 | ls-trend-2 | gspc-hop@1961 | replication | train | 1961-01-01 | 2025-10-31 | 0.21 | +180.6% | 86.9% | 20.20 |
| 2026-11-18 23:54 | vol-timing | const-tsmom12@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.21 | +186.1% | 10.8% | 0.71 |
| 2026-11-18 23:54 | vol-timing | vt-own-tsmom12@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.34 | +159.9% | 6.4% | 0.71 |
| 2026-11-18 23:54 | vol-timing | tv40-ex@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.21 | +1121.0% | 24.0% | 2.91 |
| 2026-11-19 00:16 | risk-menu | tsmom12-70@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.22 | +1462.6% | 27.7% | 2.00 |
| 2026-11-19 00:16 | risk-menu | tsmom12-26@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.22 | +192.5% | 10.7% | 0.79 |
| 2026-11-19 00:16 | risk-menu | vt-own-26@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.34 | +158.7% | 6.4% | 0.91 |
| 2026-11-19 00:16 | risk-menu | vt-own-70@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.33 | +1109.2% | 18.2% | 2.18 |
| 2026-11-19 00:16 | risk-menu | split-90-10@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.21 | +3109.4% | 34.7% | 2.82 |
| 2026-11-19 00:16 | risk-menu | split-70-30@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.21 | +1518.1% | 27.2% | 2.94 |
| 2026-11-19 00:16 | risk-menu | split-50-50@L07 | replication | train | 2007-04-01 | 2025-10-31 | 1.18 | +688.8% | 19.3% | 3.00 |
| 2026-11-19 00:24 | risk-menu-2 | tsmom12-70@W94 | replication | train | 1994-02-01 | 2025-10-31 | 0.94 | +2715.8% | 27.7% | 1.92 |
| 2026-11-19 00:24 | risk-menu-2 | tsmom12-26@W94 | replication | train | 1994-02-01 | 2025-10-31 | 0.94 | +268.0% | 10.7% | 0.72 |
| 2026-11-19 00:24 | risk-menu-2 | vt-own-26@W94 | replication | train | 1994-02-01 | 2025-10-31 | 1.03 | +191.0% | 6.4% | 0.71 |
| 2026-11-19 00:24 | risk-menu-2 | vt-own-70@W94 | replication | train | 1994-02-01 | 2025-10-31 | 1.08 | +2090.5% | 17.0% | 1.92 |
| 2026-11-19 00:30 | risk-menu-3 | vt-own-26-x@W94 | replication | train | 1994-02-01 | 2025-10-31 | 0.97 | +159.0% | 7.6% | 0.66 |
| 2026-11-19 00:30 | risk-menu-3 | vt-own-70-x@W94 | replication | train | 1994-02-01 | 2025-10-31 | 1.04 | +1509.2% | 15.8% | 1.81 |
| 2026-11-19 00:02 | short-sleeve | short10@bills | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +13498.6% | 32.8% | 2.60 |
| 2026-11-19 00:02 | short-sleeve | bill10@bills | baseline | train | 1994-02-01 | 2025-11-09 | 1.09 | +14008.2% | 32.1% | 2.46 |
| 2026-11-18 22:51 | rp-1 | where-rp | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +4066.6% | 24.5% | 1.38 |
| 2026-11-18 22:51 | rp-1 | where-rp@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.68 | +178.3% | 14.2% | 2.30 |
| 2026-11-18 22:51 | rp-1 | where-rp@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.61 | +349.8% | 91.8% | 3.95 |
| 2026-11-18 22:51 | rp-1 | where-rp@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.71 | +4000.8% | 29.5% | 2.43 |
| 2026-11-18 23:10 | survey-6 | value@live-fund | live-check | train | 1992-11-01 | 2025-10-31 | 0.53 | +2296.9% | 59.1% | - |
| 2026-11-18 23:10 | survey-6 | momentum@live-fund | live-check | train | 2007-04-01 | 2025-10-31 | 0.58 | +530.9% | 55.7% | - |
| 2026-11-18 23:10 | survey-6 | quality@live-fund | live-check | train | 2010-07-01 | 2025-10-31 | 1.00 | +758.3% | 26.0% | - |
| 2026-11-18 23:10 | survey-6 | low-vol@live-fund | live-check | train | 2011-06-01 | 2025-10-31 | 0.70 | +221.9% | 18.3% | - |
| 2026-11-18 23:10 | survey-6 | multi-factor@live-fund | live-check | train | 2005-10-01 | 2025-10-31 | 0.59 | +632.6% | 53.0% | - |
| 2026-11-18 23:10 | survey-6 | dividend@live-fund | live-check | train | 2003-01-01 | 2025-10-31 | 0.67 | +789.2% | 47.5% | - |
| 2026-11-18 23:10 | survey-6 | style-premia@live-fund | live-check | train | 2013-11-01 | 2025-10-31 | 0.50 | +120.0% | 34.9% | - |
| 2026-11-18 23:10 | survey-6 | fx-carry@live-fund | live-check | train | 2009-07-01 | 2025-10-31 | -0.03 | +13.6% | 26.3% | - |
| 2026-11-18 23:10 | survey-6 | merger-arb@live-fund | live-check | train | 1989-02-01 | 2025-10-31 | 0.40 | +504.1% | 11.5% | - |
| 2026-11-18 23:10 | survey-6 | option-writing@live-fund | live-check | train | 1988-01-01 | 2025-10-31 | 0.43 | +962.1% | 32.0% | - |
| 2026-11-18 23:10 | survey-6 | tail-hedge@live-fund | live-check | train | 2011-02-01 | 2025-10-31 | -0.54 | -95.7% | 97.4% | - |
| 2026-11-18 23:10 | survey-6 | gold-miners@live-fund | live-check | train | 2004-12-01 | 2025-10-31 | 0.32 | +318.9% | 77.6% | - |
| 2026-11-18 23:10 | survey-6 | defensive-sectors@live-fund | live-check | train | 1999-01-01 | 2025-10-31 | 0.57 | +708.2% | 33.6% | - |
| 2026-11-18 23:10 | survey-6 | trend@live-fund | live-check | train | 2007-03-01 | 2025-10-31 | 0.17 | +58.9% | 19.6% | - |
| 2026-11-18 23:10 | survey-6 | risk-parity@live-fund | live-check | train | 2009-07-01 | 2025-10-31 | 0.63 | +184.8% | 20.4% | - |
| 2026-11-18 23:18 | diversifier-1 | merfx7 | variant | train | 1994-02-01 | 2025-11-09 | 1.09 | +11421.5% | 30.8% | 2.36 |
| 2026-11-18 23:18 | diversifier-1 | mna7@mna | robustness | train | 2010-11-17 | 2025-11-09 | 1.37 | +2606.7% | 31.5% | 2.46 |
| 2026-11-19 00:21 | multi-signal-screen | value (IC wk -0.018 [-0.055..+0.020], mo -0.023, partial -0.008, placebo B p 0.49, corr tsmom12 -0.501) | screen | train | 2008-02-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | carry (IC wk -0.023 [-0.055..+0.011], mo -0.041, partial -0.029, placebo B p 0.63, corr tsmom12 -0.062) | screen | train | 2003-08-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | xsmom (IC wk +0.043 [+0.010..+0.077], mo +0.039, partial +0.035, placebo B p 0.04, corr tsmom12 +0.760) | screen | train | 2003-08-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | lowvol (IC wk -0.059 [-0.093..-0.026], mo -0.081, partial -0.050, placebo B p 0.07, corr tsmom12 +0.113) | screen | train | 2003-08-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | bab (IC wk -0.055 [-0.088..-0.021], mo -0.124, partial -0.028, placebo B p 0.19, corr tsmom12 -0.261) | screen | train | 2005-07-29 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | tsmom12 (IC wk +0.014 [-0.028..+0.056], mo +0.007, placebo B p 0.51, corr tsmom12 +1.000) | screen | train | 2003-10-10 | 2025-10-03 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | value@etf (IC wk -0.029 [-0.068..+0.012], mo -0.043, partial -0.013, placebo B p 0.43, corr tsmom12 -0.558) | screen | train | 2008-02-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | carry@etf (IC wk -0.026 [-0.062..+0.007], mo -0.053, partial -0.034, placebo B p 0.61, corr tsmom12 -0.102) | screen | train | 2003-08-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | xsmom@etf (IC wk +0.052 [+0.015..+0.088], mo +0.065, partial +0.035, placebo B p 0.00, corr tsmom12 +0.796) | screen | train | 2003-08-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | lowvol@etf (IC wk -0.047 [-0.083..-0.011], mo -0.091, partial -0.044, placebo B p 0.09, corr tsmom12 +0.172) | screen | train | 2003-08-01 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | bab@etf (IC wk -0.076 [-0.113..-0.038], mo -0.182, partial -0.050, placebo B p 0.00, corr tsmom12 -0.355) | screen | train | 2005-07-29 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:21 | multi-signal-screen | tsmom12@etf (IC wk +0.030 [-0.018..+0.076], mo +0.056, placebo B p 0.04, corr tsmom12 +1.000) | screen | train | 2003-10-10 | 2025-10-03 | - | - | - | - |
| 2026-11-19 00:30 | breadth-screen | value@wide34 (within-class IC wk +0.005 [-0.015..+0.023], mo -0.007, partial -0.000, placebo B p 0.74, corr tsmom12 -0.370) | screen | train | 2001-09-21 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:30 | breadth-screen | carry@wide34 (within-class IC wk -0.012 [-0.029..+0.006], mo -0.027, partial -0.007, placebo B p 0.27, corr tsmom12 +0.026) | screen | train | 1997-03-21 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:30 | breadth-screen | xsmom@wide34 (within-class IC wk -0.005 [-0.022..+0.013], mo -0.011, partial -0.004, placebo B p 0.70, corr tsmom12 +0.716) | screen | train | 1997-03-21 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:30 | breadth-screen | lowvol@wide34 (within-class IC wk -0.017 [-0.033..-0.000], mo -0.019, partial -0.020, placebo B p 0.15, corr tsmom12 +0.234) | screen | train | 1997-03-14 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:30 | breadth-screen | bab@wide34 (within-class IC wk +0.003 [-0.016..+0.023], mo -0.008, partial -0.001, placebo B p 0.81, corr tsmom12 -0.033) | screen | train | 1999-03-12 | 2025-10-31 | - | - | - | - |
| 2026-11-19 00:30 | breadth-screen | tsmom12@wide34 (within-class IC wk -0.005 [-0.028..+0.018], mo -0.028, placebo B p 0.72, corr tsmom12 +1.000) | screen | train | 1997-03-21 | 2025-10-31 | - | - | - | - |
| 2026-11-18 22:12 | dealer-backlog | backlog | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +16070.0% | 35.0% | 6.12 |
| 2026-11-18 22:12 | dealer-backlog | backlog-neg | robustness | train | 1994-02-01 | 2025-11-09 | 1.03 | +17264.7% | 37.0% | 8.59 |
| 2026-11-18 22:12 | dealer-backlog | backlog@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.59 | +226.2% | 19.2% | 5.95 |
| 2026-11-18 22:12 | extension-dose | ext-high | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +19956.0% | 35.8% | 5.96 |
| 2026-11-18 22:12 | extension-dose | ext-low | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +19461.1% | 36.1% | 6.01 |
| 2026-11-18 22:12 | extension-dose | ext-high@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.62 | +244.1% | 16.4% | 6.88 |
| 2026-11-18 01:32 | trend-tune-anatomy | equal-weight@SPY | baseline | train | 1994-02-01 | 2025-11-09 | 0.63 | +2395.7% | 55.2% | 0.01 |
| 2026-11-18 01:32 | trend-tune-anatomy | tsmom12@SPY | baseline | train | 1994-02-01 | 2025-11-09 | 0.72 | +1723.3% | 31.2% | 1.52 |
| 2026-11-18 01:32 | trend-tune-anatomy | equal-weight@QQQ | baseline | train | 2000-03-10 | 2025-11-09 | 0.41 | +569.8% | 83.0% | 0.03 |
| 2026-11-18 01:32 | trend-tune-anatomy | tsmom12@QQQ | baseline | train | 2000-03-10 | 2025-11-09 | 0.53 | +709.7% | 40.7% | 1.14 |
| 2026-11-18 01:32 | trend-tune-anatomy | equal-weight@TLT | baseline | train | 2003-07-31 | 2025-11-09 | 0.33 | +127.6% | 48.4% | 0.02 |
| 2026-11-18 01:32 | trend-tune-anatomy | tsmom12@TLT | baseline | train | 2003-07-31 | 2025-11-09 | 0.27 | +74.8% | 33.0% | 2.25 |
| 2026-11-18 01:32 | trend-tune-anatomy | equal-weight@GLD | baseline | train | 2005-11-19 | 2025-11-09 | 0.66 | +677.0% | 45.6% | 0.02 |
| 2026-11-18 01:32 | trend-tune-anatomy | tsmom12@GLD | baseline | train | 2005-11-19 | 2025-11-09 | 0.58 | +366.4% | 34.5% | 2.66 |
| 2026-11-18 01:32 | trend-tune-surface | L03-d | variant | train | 1994-02-01 | 2025-11-09 | 0.99 | +8341.9% | 44.1% | 12.04 |
| 2026-11-18 01:32 | trend-tune-surface | L03-w | variant | train | 1994-02-01 | 2025-11-09 | 0.96 | +7613.9% | 49.9% | 5.37 |
| 2026-11-18 01:32 | trend-tune-surface | L03-m | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +11051.5% | 31.5% | 3.37 |
| 2026-11-18 01:32 | trend-tune-surface | L04-d | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +9072.6% | 53.4% | 9.97 |
| 2026-11-18 01:32 | trend-tune-surface | L04-w | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +8501.1% | 48.9% | 4.99 |
| 2026-11-18 01:32 | trend-tune-surface | L04-m | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +11865.7% | 41.8% | 3.02 |
| 2026-11-18 01:32 | trend-tune-surface | L05-d | variant | train | 1994-02-01 | 2025-11-09 | 0.99 | +9860.6% | 50.3% | 8.18 |
| 2026-11-18 01:32 | trend-tune-surface | L05-w | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +12379.6% | 36.9% | 4.42 |
| 2026-11-18 01:32 | trend-tune-surface | L05-m | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +13447.1% | 29.3% | 2.95 |
| 2026-11-18 01:32 | trend-tune-surface | L06-d | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +12745.8% | 38.5% | 9.14 |
| 2026-11-18 01:32 | trend-tune-surface | L06-w | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +11880.7% | 37.5% | 4.47 |
| 2026-11-18 01:32 | trend-tune-surface | L06-m | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +14534.0% | 32.7% | 2.62 |
| 2026-11-18 01:32 | trend-tune-surface | L07-d | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +12498.1% | 34.0% | 8.18 |
| 2026-11-18 01:32 | trend-tune-surface | L07-w | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +15759.7% | 29.0% | 3.66 |
| 2026-11-18 01:32 | trend-tune-surface | L07-m | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +16285.6% | 32.4% | 2.51 |
| 2026-11-18 01:32 | trend-tune-surface | L08-d | variant | train | 1994-02-01 | 2025-11-09 | 1.10 | +20920.0% | 32.3% | 7.53 |
| 2026-11-18 01:32 | trend-tune-surface | L08-w | variant | train | 1994-02-01 | 2025-11-09 | 1.13 | +24085.3% | 28.1% | 4.00 |
| 2026-11-18 01:32 | trend-tune-surface | L08-m | variant | train | 1994-02-01 | 2025-11-09 | 1.14 | +27335.2% | 32.3% | 2.31 |
| 2026-11-18 01:32 | trend-tune-surface | L09-d | variant | train | 1994-02-01 | 2025-11-09 | 1.10 | +20738.2% | 29.8% | 6.98 |
| 2026-11-18 01:32 | trend-tune-surface | L09-w | variant | train | 1994-02-01 | 2025-11-09 | 1.09 | +19870.4% | 32.6% | 3.87 |
| 2026-11-18 01:32 | trend-tune-surface | L09-m | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +20176.3% | 34.9% | 2.37 |
| 2026-11-18 01:32 | trend-tune-surface | L10-d | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +13519.4% | 39.1% | 6.38 |
| 2026-11-18 01:32 | trend-tune-surface | L10-w | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +16029.7% | 35.3% | 3.40 |
| 2026-11-18 01:32 | trend-tune-surface | L10-m | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +15466.1% | 40.5% | 2.25 |
| 2026-11-18 01:32 | trend-tune-surface | L11-d | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +20003.7% | 31.6% | 5.88 |
| 2026-11-18 01:32 | trend-tune-surface | L11-w | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +18575.2% | 33.1% | 3.08 |
| 2026-11-18 01:32 | trend-tune-surface | L11-m | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +19535.5% | 33.5% | 2.02 |
| 2026-11-18 01:32 | trend-tune-surface | L12-d | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +19463.0% | 35.8% | 4.89 |
| 2026-11-18 01:32 | trend-tune-surface | L12-m | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +14632.7% | 41.1% | 1.93 |
| 2026-11-18 01:32 | trend-tune-surface | L13-d | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +15595.3% | 34.1% | 5.36 |
| 2026-11-18 01:32 | trend-tune-surface | L13-w | variant | train | 1994-02-01 | 2025-11-09 | 0.99 | +14512.9% | 35.9% | 2.86 |
| 2026-11-18 01:32 | trend-tune-surface | L13-m | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +17234.4% | 39.0% | 1.92 |
| 2026-11-18 01:32 | trend-tune-surface | L14-d | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +16224.4% | 40.2% | 5.59 |
| 2026-11-18 01:32 | trend-tune-surface | L14-w | variant | train | 1994-02-01 | 2025-11-09 | 0.98 | +14637.6% | 40.8% | 2.92 |
| 2026-11-18 01:32 | trend-tune-surface | L14-m | variant | train | 1994-02-01 | 2025-11-09 | 0.96 | +13783.7% | 42.7% | 1.86 |
| 2026-11-18 01:32 | trend-tune-surface | L15-d | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +12108.5% | 46.4% | 5.07 |
| 2026-11-18 01:32 | trend-tune-surface | L15-w | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +12700.2% | 45.5% | 2.80 |
| 2026-11-18 01:32 | trend-tune-surface | L15-m | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +12638.9% | 45.2% | 1.82 |
| 2026-11-18 01:32 | trend-tune-surface | L16-d | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +11533.4% | 44.5% | 4.94 |
| 2026-11-18 01:32 | trend-tune-surface | L16-w | variant | train | 1994-02-01 | 2025-11-09 | 0.93 | +11217.8% | 52.9% | 2.90 |
| 2026-11-18 01:32 | trend-tune-surface | L16-m | variant | train | 1994-02-01 | 2025-11-09 | 0.90 | +10044.8% | 46.3% | 2.06 |
| 2026-11-18 01:32 | trend-tune-surface | L18-d | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +8845.2% | 49.4% | 5.71 |
| 2026-11-18 01:32 | trend-tune-surface | L18-w | variant | train | 1994-02-01 | 2025-11-09 | 0.93 | +11818.9% | 46.0% | 2.87 |
| 2026-11-18 01:32 | trend-tune-surface | L18-m | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +10676.1% | 46.5% | 1.94 |
| 2026-11-18 01:32 | trend-tune-surface | L20-d | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +10531.7% | 48.6% | 5.24 |
| 2026-11-18 01:32 | trend-tune-surface | L20-w | variant | train | 1994-02-01 | 2025-11-09 | 0.93 | +12557.5% | 48.4% | 2.85 |
| 2026-11-18 01:32 | trend-tune-surface | L20-m | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +13082.5% | 47.9% | 2.00 |
| 2026-11-18 01:32 | trend-tune-surface | L22-d | variant | train | 1994-02-01 | 2025-11-09 | 0.92 | +11552.4% | 47.5% | 3.99 |
| 2026-11-18 01:32 | trend-tune-surface | L22-w | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +10864.4% | 47.3% | 2.45 |
| 2026-11-18 01:32 | trend-tune-surface | L22-m | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +9255.7% | 47.8% | 1.89 |
| 2026-11-18 01:32 | trend-tune-surface | L24-d | variant | train | 1994-02-01 | 2025-11-09 | 0.87 | +9479.9% | 47.3% | 3.90 |
| 2026-11-18 01:32 | trend-tune-surface | L24-w | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +9574.1% | 47.0% | 2.43 |
| 2026-11-18 01:32 | trend-tune-surface | L24-m | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +11605.6% | 47.6% | 1.75 |
| 2026-11-18 01:32 | trend-tune-surface | and-03-06 | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +4271.7% | 46.0% | 5.28 |
| 2026-11-18 01:32 | trend-tune-surface | and-03-09 | variant | train | 1994-02-01 | 2025-11-09 | 0.98 | +6124.9% | 39.4% | 5.09 |
| 2026-11-18 01:32 | trend-tune-surface | and-03-12 | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +5049.5% | 38.9% | 4.46 |
| 2026-11-18 01:32 | trend-tune-surface | and-03-18 | variant | train | 1994-02-01 | 2025-11-09 | 0.96 | +4832.6% | 37.6% | 4.61 |
| 2026-11-18 01:32 | trend-tune-surface | or-03-06 | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +20767.9% | 42.0% | 4.32 |
| 2026-11-18 01:32 | trend-tune-surface | and-06-09 | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +12326.0% | 29.2% | 4.13 |
| 2026-11-18 01:32 | trend-tune-surface | and-06-12 | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +10208.5% | 31.1% | 3.51 |
| 2026-11-18 01:32 | trend-tune-surface | and-06-18 | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +8986.4% | 28.4% | 3.93 |
| 2026-11-18 01:32 | trend-tune-surface | or-03-09 | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +24273.8% | 36.9% | 3.97 |
| 2026-11-18 01:32 | trend-tune-surface | or-06-09 | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +18683.4% | 37.6% | 3.91 |
| 2026-11-18 01:32 | trend-tune-surface | and-09-12 | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +14340.1% | 32.7% | 3.35 |
| 2026-11-18 01:32 | trend-tune-surface | and-09-18 | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +11165.5% | 35.5% | 3.69 |
| 2026-11-18 01:32 | trend-tune-surface | or-03-12 | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +27089.4% | 41.7% | 3.57 |
| 2026-11-18 01:32 | trend-tune-surface | or-06-12 | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +21322.0% | 44.2% | 3.70 |
| 2026-11-18 01:32 | trend-tune-surface | or-09-12 | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +25718.1% | 36.6% | 3.18 |
| 2026-11-18 01:32 | trend-tune-surface | and-12-18 | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +14043.3% | 34.0% | 2.73 |
| 2026-11-18 01:32 | trend-tune-surface | or-03-18 | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +18293.7% | 51.4% | 3.57 |
| 2026-11-18 01:32 | trend-tune-surface | or-06-18 | variant | train | 1994-02-01 | 2025-11-09 | 0.94 | +15316.9% | 54.0% | 3.25 |
| 2026-11-18 01:32 | trend-tune-surface | or-09-18 | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +21035.7% | 45.8% | 2.85 |
| 2026-11-18 01:32 | trend-tune-surface | or-12-18 | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +15442.1% | 45.4% | 2.72 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c-0.25-h0.00 | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +15472.7% | 40.4% | 4.58 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c-0.25-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +17182.9% | 49.1% | 2.33 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c-0.25-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 0.99 | +15237.4% | 48.9% | 1.99 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c+0.00-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 0.99 | +11092.6% | 36.3% | 2.58 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c+0.00-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +15272.0% | 32.7% | 2.11 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c+0.25-h0.00 | variant | train | 1994-02-01 | 2025-11-09 | 0.93 | +6298.6% | 42.8% | 3.99 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c+0.25-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +9051.5% | 32.4% | 2.41 |
| 2026-11-18 01:32 | trend-tune-surface | z06-c+0.25-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +7821.6% | 35.5% | 1.94 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c-0.25-h0.00 | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +25893.9% | 38.0% | 3.13 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c-0.25-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 1.03 | +21699.8% | 42.1% | 1.77 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c-0.25-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +19166.8% | 44.3% | 1.43 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c+0.00-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +20212.8% | 34.9% | 1.70 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c+0.00-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +17911.3% | 45.0% | 1.52 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c+0.25-h0.00 | variant | train | 1994-02-01 | 2025-11-09 | 0.98 | +11055.0% | 38.5% | 3.10 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c+0.25-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 0.98 | +11845.4% | 40.2% | 1.77 |
| 2026-11-18 01:32 | trend-tune-surface | z12-c+0.25-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +12321.3% | 41.9% | 1.55 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c-0.25-h0.00 | variant | train | 1994-02-01 | 2025-11-09 | 0.89 | +10681.5% | 45.9% | 2.84 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c-0.25-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 0.92 | +12568.8% | 48.1% | 1.57 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c-0.25-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +10696.8% | 52.8% | 1.42 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c+0.00-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 0.91 | +10713.6% | 45.6% | 1.66 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c+0.00-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 0.90 | +10969.6% | 48.1% | 1.40 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c+0.25-h0.00 | variant | train | 1994-02-01 | 2025-11-09 | 0.84 | +5884.3% | 46.9% | 2.90 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c+0.25-h0.25 | variant | train | 1994-02-01 | 2025-11-09 | 0.86 | +7359.0% | 45.8% | 1.67 |
| 2026-11-18 01:32 | trend-tune-surface | z18-c+0.25-h0.50 | variant | train | 1994-02-01 | 2025-11-09 | 0.88 | +8615.9% | 44.9% | 1.47 |
| 2026-11-18 01:32 | trend-tune-surface | tsmom12-band0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +17268.3% | 38.0% | 4.39 |
| 2026-11-18 01:32 | trend-tune-surface | tsmom12-band2.5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.07 | +20095.0% | 36.2% | 2.26 |
| 2026-11-18 01:32 | trend-tune-surface | tsmom12-band5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.07 | +20462.0% | 36.9% | 2.01 |
| 2026-11-18 01:32 | trend-tune-surface | hindsight-asset | variant | train | 1994-02-01 | 2025-11-09 | 1.15 | +26940.8% | 28.8% | 3.53 |
| 2026-11-18 01:36 | trend-tune | wf-asset | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +11602.4% | 35.0% | 3.89 |
| 2026-11-18 01:36 | trend-tune | wf-pooled | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +12311.9% | 37.5% | 4.31 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +18364.7% | 36.5% | 2.74 |
| 2026-11-18 01:36 | trend-tune | wf-asset@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.57 | +198.0% | 18.7% | 3.57 |
| 2026-11-18 01:36 | trend-tune | wf-asset@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.52 | +159.6% | 92.4% | 4.85 |
| 2026-11-18 01:36 | trend-tune | wf-asset@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.46 | +239.7% | 25.3% | 3.75 |
| 2026-11-18 01:36 | trend-tune | wf-asset@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.37 | +1136.1% | 53.3% | 3.39 |
| 2026-11-18 01:36 | trend-tune | wf-asset@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.27 | +165.3% | 50.5% | 3.32 |
| 2026-11-18 01:36 | trend-tune | wf-asset@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.61 | +1596.8% | 30.5% | 2.90 |
| 2026-11-18 01:36 | trend-tune | wf-pooled@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.54 | +188.0% | 16.5% | 3.36 |
| 2026-11-18 01:36 | trend-tune | wf-pooled@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.52 | +151.7% | 92.4% | 5.55 |
| 2026-11-18 01:36 | trend-tune | wf-pooled@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.73 | +3226.0% | 29.5% | 4.67 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.60 | +221.0% | 17.1% | 3.14 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.53 | +180.4% | 93.0% | 5.06 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk@GSPC | robustness | train | 1962-01-02 | 1993-01-27 | 0.33 | +146.0% | 33.2% | 3.95 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk@N225 | robustness | train | 1966-01-06 | 2025-11-09 | 0.55 | +4760.5% | 44.2% | 2.23 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk@FTSE | robustness | train | 1985-01-03 | 2025-11-09 | 0.34 | +282.4% | 39.1% | 2.86 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk@GDAXI | robustness | train | 1988-12-30 | 2025-11-09 | 0.41 | +553.4% | 54.6% | 3.09 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk-raw | robustness | train | 1994-02-01 | 2025-11-09 | 0.96 | +11127.8% | 38.4% | 3.31 |
| 2026-11-18 01:36 | trend-tune | wf-shrunk-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +17327.2% | 37.1% | 2.74 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Mkt | baseline | train | 1927-07-02 | 1961-12-28 | 0.55 | +2107.4% | 84.1% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Mkt | baseline | train | 1927-07-02 | 1961-12-28 | 0.88 | +4102.5% | 38.2% | 2.13 |
| 2026-11-18 11:01 | trend-1926 | hold@F-NoDur | baseline | train | 1927-07-02 | 1961-12-28 | 0.67 | +1975.3% | 67.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-NoDur | baseline | train | 1927-07-02 | 1961-12-28 | 1.05 | +2896.3% | 31.5% | 1.30 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Durbl | baseline | train | 1927-07-02 | 1961-12-28 | 0.51 | +4205.8% | 90.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Durbl | baseline | train | 1927-07-02 | 1961-12-28 | 0.80 | +10988.2% | 52.9% | 1.46 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Manuf | baseline | train | 1927-07-02 | 1961-12-28 | 0.53 | +2765.9% | 88.9% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Manuf | baseline | train | 1927-07-02 | 1961-12-28 | 0.85 | +6098.2% | 49.4% | 1.60 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Enrgy | baseline | train | 1927-07-02 | 1961-12-28 | 0.55 | +2669.6% | 78.7% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Enrgy | baseline | train | 1927-07-02 | 1961-12-28 | 0.55 | +1177.2% | 57.0% | 2.05 |
| 2026-11-18 11:01 | trend-1926 | hold@F-HiTec | baseline | train | 1927-07-02 | 1961-12-28 | 0.55 | +4554.6% | 91.2% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-HiTec | baseline | train | 1927-07-02 | 1961-12-28 | 0.83 | +10366.1% | 56.9% | 0.63 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Telcm | baseline | train | 1927-07-02 | 1961-12-28 | 0.66 | +2232.7% | 70.3% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Telcm | baseline | train | 1927-07-02 | 1961-12-28 | 0.97 | +3749.3% | 32.7% | 0.54 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Shops | baseline | train | 1927-07-02 | 1961-12-28 | 0.59 | +2621.2% | 84.7% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Shops | baseline | train | 1927-07-02 | 1961-12-28 | 1.06 | +7330.9% | 33.8% | 1.01 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Hlth | baseline | train | 1927-07-02 | 1961-12-28 | 0.66 | +4121.5% | 75.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Hlth | baseline | train | 1927-07-02 | 1961-12-28 | 1.14 | +10065.1% | 38.5% | 1.01 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Utils | baseline | train | 1927-07-02 | 1961-12-28 | 0.46 | +1509.0% | 87.6% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Utils | baseline | train | 1927-07-02 | 1961-12-28 | 0.81 | +4332.5% | 56.0% | 1.11 |
| 2026-11-18 11:01 | trend-1926 | hold@F-Other | baseline | train | 1927-07-02 | 1961-12-28 | 0.40 | +816.0% | 90.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-Other | baseline | train | 1927-07-02 | 1961-12-28 | 0.74 | +2638.1% | 48.1% | 1.63 |
| 2026-11-18 11:01 | trend-1926 | equal-weight@F-ind10 | baseline | train | 1927-07-02 | 1961-12-28 | 0.62 | +3163.0% | 81.9% | 0.10 |
| 2026-11-18 11:01 | trend-1926 | tsmom12@F-ind10 | baseline | train | 1927-07-02 | 1961-12-28 | 1.07 | +5912.9% | 32.5% | 1.30 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Mkt | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +2088.8% | 84.1% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Mkt | robustness | train | 1927-07-02 | 1961-12-28 | 0.83 | +3324.5% | 38.1% | 2.08 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-NoDur | robustness | train | 1927-07-02 | 1961-12-28 | 0.67 | +1953.4% | 67.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-NoDur | robustness | train | 1927-07-02 | 1961-12-28 | 1.00 | +2450.5% | 37.7% | 1.31 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Durbl | robustness | train | 1927-07-02 | 1961-12-28 | 0.51 | +4142.2% | 90.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Durbl | robustness | train | 1927-07-02 | 1961-12-28 | 0.77 | +9308.1% | 54.8% | 1.48 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Manuf | robustness | train | 1927-07-02 | 1961-12-28 | 0.53 | +2737.5% | 88.9% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Manuf | robustness | train | 1927-07-02 | 1961-12-28 | 0.81 | +4908.7% | 50.7% | 1.60 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Enrgy | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +2663.0% | 78.7% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Enrgy | robustness | train | 1927-07-02 | 1961-12-28 | 0.54 | +1085.4% | 56.2% | 2.05 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-HiTec | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +4440.6% | 91.2% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-HiTec | robustness | train | 1927-07-02 | 1961-12-28 | 0.81 | +9454.2% | 56.2% | 0.64 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Telcm | robustness | train | 1927-07-02 | 1961-12-28 | 0.66 | +2230.4% | 70.3% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Telcm | robustness | train | 1927-07-02 | 1961-12-28 | 0.95 | +3382.6% | 32.7% | 0.55 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Shops | robustness | train | 1927-07-02 | 1961-12-28 | 0.59 | +2613.8% | 84.7% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Shops | robustness | train | 1927-07-02 | 1961-12-28 | 1.05 | +7002.6% | 36.1% | 1.02 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Hlth | robustness | train | 1927-07-02 | 1961-12-28 | 0.66 | +4069.0% | 75.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Hlth | robustness | train | 1927-07-02 | 1961-12-28 | 1.09 | +8165.9% | 42.1% | 1.01 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Utils | robustness | train | 1927-07-02 | 1961-12-28 | 0.46 | +1494.9% | 87.6% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Utils | robustness | train | 1927-07-02 | 1961-12-28 | 0.78 | +3721.4% | 56.0% | 1.12 |
| 2026-11-18 11:01 | trend-1926 | hold-late@F-Other | robustness | train | 1927-07-02 | 1961-12-28 | 0.39 | +809.9% | 90.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-Other | robustness | train | 1927-07-02 | 1961-12-28 | 0.72 | +2372.6% | 49.8% | 1.64 |
| 2026-11-18 11:01 | trend-1926 | equal-weight-late@F-ind10 | robustness | train | 1927-07-02 | 1961-12-28 | 0.62 | +3077.5% | 81.9% | 0.10 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-late@F-ind10 | robustness | train | 1927-07-02 | 1961-12-28 | 1.04 | +5159.7% | 33.8% | 1.31 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Mkt | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +2105.7% | 84.1% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Mkt | robustness | train | 1927-07-02 | 1961-12-28 | 0.87 | +3915.2% | 38.6% | 2.13 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-NoDur | robustness | train | 1927-07-02 | 1961-12-28 | 0.67 | +1973.7% | 67.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-NoDur | robustness | train | 1927-07-02 | 1961-12-28 | 1.04 | +2767.3% | 31.9% | 1.31 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Durbl | robustness | train | 1927-07-02 | 1961-12-28 | 0.51 | +4202.4% | 90.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Durbl | robustness | train | 1927-07-02 | 1961-12-28 | 0.79 | +10375.9% | 53.4% | 1.46 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Manuf | robustness | train | 1927-07-02 | 1961-12-28 | 0.53 | +2763.6% | 88.9% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Manuf | robustness | train | 1927-07-02 | 1961-12-28 | 0.84 | +5803.0% | 49.9% | 1.60 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Enrgy | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +2667.4% | 78.7% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Enrgy | robustness | train | 1927-07-02 | 1961-12-28 | 0.54 | +1085.6% | 57.7% | 2.06 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-HiTec | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +4550.9% | 91.2% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-HiTec | robustness | train | 1927-07-02 | 1961-12-28 | 0.82 | +9996.0% | 57.3% | 0.64 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Telcm | robustness | train | 1927-07-02 | 1961-12-28 | 0.66 | +2230.8% | 70.3% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Telcm | robustness | train | 1927-07-02 | 1961-12-28 | 0.97 | +3631.1% | 32.7% | 0.55 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Shops | robustness | train | 1927-07-02 | 1961-12-28 | 0.59 | +2619.0% | 84.7% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Shops | robustness | train | 1927-07-02 | 1961-12-28 | 1.05 | +7079.6% | 34.2% | 1.02 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Hlth | robustness | train | 1927-07-02 | 1961-12-28 | 0.66 | +4118.2% | 75.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Hlth | robustness | train | 1927-07-02 | 1961-12-28 | 1.13 | +9721.4% | 38.6% | 1.01 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Utils | robustness | train | 1927-07-02 | 1961-12-28 | 0.46 | +1507.7% | 87.6% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Utils | robustness | train | 1927-07-02 | 1961-12-28 | 0.81 | +4141.7% | 56.0% | 1.12 |
| 2026-11-18 11:01 | trend-1926 | hold-10bps@F-Other | robustness | train | 1927-07-02 | 1961-12-28 | 0.39 | +815.2% | 90.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-Other | robustness | train | 1927-07-02 | 1961-12-28 | 0.73 | +2503.5% | 48.7% | 1.63 |
| 2026-11-18 11:01 | trend-1926 | equal-weight-10bps@F-ind10 | robustness | train | 1927-07-02 | 1961-12-28 | 0.62 | +3123.6% | 81.9% | 0.10 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-10bps@F-ind10 | robustness | train | 1927-07-02 | 1961-12-28 | 1.06 | +5604.3% | 33.0% | 1.30 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Mkt | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +2096.9% | 84.1% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Mkt | robustness | train | 1927-07-02 | 1961-12-28 | 0.82 | +3096.6% | 40.7% | 2.09 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-NoDur | robustness | train | 1927-07-02 | 1961-12-28 | 0.67 | +1965.4% | 67.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-NoDur | robustness | train | 1927-07-02 | 1961-12-28 | 0.97 | +2201.1% | 33.8% | 1.32 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Durbl | robustness | train | 1927-07-02 | 1961-12-28 | 0.51 | +4185.3% | 90.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Durbl | robustness | train | 1927-07-02 | 1961-12-28 | 0.75 | +7786.0% | 56.7% | 1.49 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Manuf | robustness | train | 1927-07-02 | 1961-12-28 | 0.53 | +2752.2% | 88.9% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Manuf | robustness | train | 1927-07-02 | 1961-12-28 | 0.79 | +4524.9% | 52.4% | 1.60 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Enrgy | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +2656.4% | 78.7% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Enrgy | robustness | train | 1927-07-02 | 1961-12-28 | 0.47 | +717.3% | 61.0% | 2.11 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-HiTec | robustness | train | 1927-07-02 | 1961-12-28 | 0.55 | +4532.4% | 91.2% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-HiTec | robustness | train | 1927-07-02 | 1961-12-28 | 0.79 | +8333.0% | 59.3% | 0.65 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Telcm | robustness | train | 1927-07-02 | 1961-12-28 | 0.65 | +2221.5% | 70.3% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Telcm | robustness | train | 1927-07-02 | 1961-12-28 | 0.93 | +3092.2% | 32.7% | 0.57 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Shops | robustness | train | 1927-07-02 | 1961-12-28 | 0.59 | +2608.2% | 84.7% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Shops | robustness | train | 1927-07-02 | 1961-12-28 | 1.01 | +5945.1% | 36.2% | 1.03 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Hlth | robustness | train | 1927-07-02 | 1961-12-28 | 0.66 | +4101.4% | 75.6% | 0.00 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Hlth | robustness | train | 1927-07-02 | 1961-12-28 | 1.09 | +8169.5% | 39.1% | 1.01 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Utils | robustness | train | 1927-07-02 | 1961-12-28 | 0.46 | +1501.3% | 87.6% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Utils | robustness | train | 1927-07-02 | 1961-12-28 | 0.76 | +3304.1% | 56.0% | 1.13 |
| 2026-11-18 11:01 | trend-1926 | hold-50bps@F-Other | robustness | train | 1927-07-02 | 1961-12-28 | 0.39 | +811.6% | 90.5% | 0.01 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-Other | robustness | train | 1927-07-02 | 1961-12-28 | 0.68 | +1923.6% | 51.5% | 1.64 |
| 2026-11-18 11:01 | trend-1926 | equal-weight-50bps@F-ind10 | robustness | train | 1927-07-02 | 1961-12-28 | 0.62 | +3011.1% | 81.9% | 0.10 |
| 2026-11-18 11:01 | trend-1926 | tsmom12-50bps@F-ind10 | robustness | train | 1927-07-02 | 1961-12-28 | 1.00 | +4394.5% | 35.5% | 1.32 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Mkt | baseline | train | 1962-01-02 | 2001-12-30 | 0.80 | +5977.3% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Mkt | baseline | train | 1962-01-02 | 2001-12-30 | 0.88 | +3961.1% | 32.3% | 0.82 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-NoDur | baseline | train | 1962-01-02 | 2001-12-30 | 0.95 | +11083.6% | 54.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-NoDur | baseline | train | 1962-01-02 | 2001-12-30 | 1.02 | +6877.7% | 35.5% | 1.79 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Durbl | baseline | train | 1962-01-02 | 2001-12-30 | 0.61 | +3968.2% | 58.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Durbl | baseline | train | 1962-01-02 | 2001-12-30 | 0.62 | +2089.2% | 45.4% | 2.03 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Manuf | baseline | train | 1962-01-02 | 2001-12-30 | 0.75 | +5084.1% | 44.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Manuf | baseline | train | 1962-01-02 | 2001-12-30 | 0.73 | +2129.9% | 41.0% | 2.00 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Enrgy | baseline | train | 1962-01-02 | 2001-12-30 | 0.75 | +9776.1% | 51.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Enrgy | baseline | train | 1962-01-02 | 2001-12-30 | 0.68 | +3689.3% | 34.0% | 2.59 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-HiTec | baseline | train | 1962-01-02 | 2001-12-30 | 0.55 | +4693.6% | 73.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-HiTec | baseline | train | 1962-01-02 | 2001-12-30 | 0.57 | +2809.9% | 44.0% | 1.49 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Telcm | baseline | train | 1962-01-02 | 2001-12-30 | 0.70 | +4821.7% | 55.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Telcm | baseline | train | 1962-01-02 | 2001-12-30 | 0.73 | +2686.3% | 27.0% | 1.92 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Shops | baseline | train | 1962-01-02 | 2001-12-30 | 0.78 | +8316.8% | 60.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Shops | baseline | train | 1962-01-02 | 2001-12-30 | 0.65 | +1806.5% | 52.4% | 3.08 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Hlth | baseline | train | 1962-01-02 | 2001-12-30 | 0.82 | +13868.4% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Hlth | baseline | train | 1962-01-02 | 2001-12-30 | 0.73 | +3969.7% | 36.2% | 1.83 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Utils | baseline | train | 1962-01-02 | 2001-12-30 | 0.93 | +3840.6% | 45.7% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Utils | baseline | train | 1962-01-02 | 2001-12-30 | 0.96 | +2201.5% | 22.8% | 1.88 |
| 2026-11-18 11:18 | trend-1926 | hold@F62-Other | baseline | train | 1962-01-02 | 2001-12-30 | 0.82 | +7963.4% | 56.4% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-Other | baseline | train | 1962-01-02 | 2001-12-30 | 0.84 | +3662.0% | 34.7% | 2.63 |
| 2026-11-18 11:18 | trend-1926 | equal-weight@F62-ind10 | baseline | train | 1962-01-02 | 2001-12-30 | 0.91 | +8401.2% | 46.7% | 0.16 |
| 2026-11-18 11:18 | trend-1926 | tsmom12@F62-ind10 | baseline | train | 1962-01-02 | 2001-12-30 | 0.97 | +3710.0% | 30.6% | 2.38 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Mkt | robustness | train | 1962-01-02 | 2001-12-30 | 0.81 | +6022.6% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Mkt | robustness | train | 1962-01-02 | 2001-12-30 | 0.86 | +3658.6% | 32.3% | 0.83 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-NoDur | robustness | train | 1962-01-02 | 2001-12-30 | 0.95 | +11142.0% | 54.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-NoDur | robustness | train | 1962-01-02 | 2001-12-30 | 1.01 | +6833.3% | 33.8% | 1.80 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Durbl | robustness | train | 1962-01-02 | 2001-12-30 | 0.61 | +3960.1% | 58.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Durbl | robustness | train | 1962-01-02 | 2001-12-30 | 0.56 | +1485.0% | 46.0% | 2.00 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Manuf | robustness | train | 1962-01-02 | 2001-12-30 | 0.75 | +5121.2% | 44.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Manuf | robustness | train | 1962-01-02 | 2001-12-30 | 0.72 | +2103.6% | 38.9% | 2.02 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Enrgy | robustness | train | 1962-01-02 | 2001-12-30 | 0.75 | +9875.9% | 51.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Enrgy | robustness | train | 1962-01-02 | 2001-12-30 | 0.68 | +3677.6% | 33.9% | 2.60 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-HiTec | robustness | train | 1962-01-02 | 2001-12-30 | 0.55 | +4726.9% | 73.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-HiTec | robustness | train | 1962-01-02 | 2001-12-30 | 0.53 | +2055.6% | 48.8% | 1.60 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Telcm | robustness | train | 1962-01-02 | 2001-12-30 | 0.71 | +4877.0% | 55.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Telcm | robustness | train | 1962-01-02 | 2001-12-30 | 0.70 | +2343.3% | 31.3% | 1.94 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Shops | robustness | train | 1962-01-02 | 2001-12-30 | 0.78 | +8455.4% | 60.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Shops | robustness | train | 1962-01-02 | 2001-12-30 | 0.61 | +1499.5% | 54.5% | 3.07 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Hlth | robustness | train | 1962-01-02 | 2001-12-30 | 0.82 | +13875.4% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Hlth | robustness | train | 1962-01-02 | 2001-12-30 | 0.70 | +3390.4% | 37.0% | 1.83 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Utils | robustness | train | 1962-01-02 | 2001-12-30 | 0.93 | +3868.4% | 45.7% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Utils | robustness | train | 1962-01-02 | 2001-12-30 | 0.90 | +1885.3% | 20.7% | 1.89 |
| 2026-11-18 11:18 | trend-1926 | hold-late@F62-Other | robustness | train | 1962-01-02 | 2001-12-30 | 0.82 | +7996.6% | 56.4% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-Other | robustness | train | 1962-01-02 | 2001-12-30 | 0.81 | +3280.3% | 35.4% | 2.62 |
| 2026-11-18 11:18 | trend-1926 | equal-weight-late@F62-ind10 | robustness | train | 1962-01-02 | 2001-12-30 | 0.91 | +8362.5% | 47.0% | 0.16 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-late@F62-ind10 | robustness | train | 1962-01-02 | 2001-12-30 | 0.93 | +3210.6% | 31.5% | 2.38 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Mkt | robustness | train | 1962-01-02 | 2001-12-30 | 0.80 | +5972.4% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Mkt | robustness | train | 1962-01-02 | 2001-12-30 | 0.87 | +3801.9% | 32.3% | 0.83 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-NoDur | robustness | train | 1962-01-02 | 2001-12-30 | 0.95 | +11074.6% | 54.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-NoDur | robustness | train | 1962-01-02 | 2001-12-30 | 1.01 | +6572.0% | 35.7% | 1.79 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Durbl | robustness | train | 1962-01-02 | 2001-12-30 | 0.61 | +3964.9% | 58.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Durbl | robustness | train | 1962-01-02 | 2001-12-30 | 0.61 | +1958.4% | 45.8% | 2.03 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Manuf | robustness | train | 1962-01-02 | 2001-12-30 | 0.75 | +5079.9% | 44.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Manuf | robustness | train | 1962-01-02 | 2001-12-30 | 0.72 | +2025.4% | 41.2% | 1.99 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Enrgy | robustness | train | 1962-01-02 | 2001-12-30 | 0.75 | +9768.2% | 51.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Enrgy | robustness | train | 1962-01-02 | 2001-12-30 | 0.67 | +3437.4% | 34.6% | 2.58 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-HiTec | robustness | train | 1962-01-02 | 2001-12-30 | 0.55 | +4689.8% | 73.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-HiTec | robustness | train | 1962-01-02 | 2001-12-30 | 0.56 | +2581.9% | 45.1% | 1.51 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Telcm | robustness | train | 1962-01-02 | 2001-12-30 | 0.70 | +4817.8% | 55.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Telcm | robustness | train | 1962-01-02 | 2001-12-30 | 0.71 | +2488.6% | 28.3% | 1.93 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Shops | robustness | train | 1962-01-02 | 2001-12-30 | 0.78 | +8310.1% | 60.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Shops | robustness | train | 1962-01-02 | 2001-12-30 | 0.64 | +1655.7% | 53.3% | 3.05 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Hlth | robustness | train | 1962-01-02 | 2001-12-30 | 0.82 | +13857.2% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Hlth | robustness | train | 1962-01-02 | 2001-12-30 | 0.72 | +3674.9% | 36.4% | 1.84 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Utils | robustness | train | 1962-01-02 | 2001-12-30 | 0.93 | +3837.5% | 45.7% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Utils | robustness | train | 1962-01-02 | 2001-12-30 | 0.95 | +2079.7% | 23.1% | 1.87 |
| 2026-11-18 11:18 | trend-1926 | hold-10bps@F62-Other | robustness | train | 1962-01-02 | 2001-12-30 | 0.82 | +7957.0% | 56.4% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-Other | robustness | train | 1962-01-02 | 2001-12-30 | 0.83 | +3479.9% | 35.6% | 2.61 |
| 2026-11-18 11:18 | trend-1926 | equal-weight-10bps@F62-ind10 | robustness | train | 1962-01-02 | 2001-12-30 | 0.91 | +8424.3% | 46.8% | 0.18 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-10bps@F62-ind10 | robustness | train | 1962-01-02 | 2001-12-30 | 0.95 | +3484.0% | 30.8% | 2.37 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Mkt | robustness | train | 1962-01-02 | 2001-12-30 | 0.80 | +5948.2% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Mkt | robustness | train | 1962-01-02 | 2001-12-30 | 0.82 | +3094.6% | 32.3% | 0.84 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-NoDur | robustness | train | 1962-01-02 | 2001-12-30 | 0.95 | +11030.1% | 54.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-NoDur | robustness | train | 1962-01-02 | 2001-12-30 | 0.96 | +5233.0% | 36.7% | 1.76 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Durbl | robustness | train | 1962-01-02 | 2001-12-30 | 0.61 | +3948.8% | 58.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Durbl | robustness | train | 1962-01-02 | 2001-12-30 | 0.56 | +1412.8% | 47.9% | 2.01 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Manuf | robustness | train | 1962-01-02 | 2001-12-30 | 0.75 | +5059.3% | 44.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Manuf | robustness | train | 1962-01-02 | 2001-12-30 | 0.66 | +1571.9% | 42.2% | 1.95 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Enrgy | robustness | train | 1962-01-02 | 2001-12-30 | 0.75 | +9729.0% | 51.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Enrgy | robustness | train | 1962-01-02 | 2001-12-30 | 0.61 | +2407.7% | 37.7% | 2.55 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-HiTec | robustness | train | 1962-01-02 | 2001-12-30 | 0.55 | +4670.7% | 73.5% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-HiTec | robustness | train | 1962-01-02 | 2001-12-30 | 0.50 | +1683.4% | 50.3% | 1.61 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Telcm | robustness | train | 1962-01-02 | 2001-12-30 | 0.70 | +4798.2% | 55.0% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Telcm | robustness | train | 1962-01-02 | 2001-12-30 | 0.64 | +1691.6% | 36.3% | 1.95 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Shops | robustness | train | 1962-01-02 | 2001-12-30 | 0.78 | +8276.6% | 60.9% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Shops | robustness | train | 1962-01-02 | 2001-12-30 | 0.55 | +1062.8% | 57.2% | 2.95 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Hlth | robustness | train | 1962-01-02 | 2001-12-30 | 0.81 | +13801.7% | 48.2% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Hlth | robustness | train | 1962-01-02 | 2001-12-30 | 0.65 | +2491.8% | 39.4% | 1.85 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Utils | robustness | train | 1962-01-02 | 2001-12-30 | 0.93 | +3821.8% | 45.7% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Utils | robustness | train | 1962-01-02 | 2001-12-30 | 0.87 | +1560.6% | 24.3% | 1.85 |
| 2026-11-18 11:18 | trend-1926 | hold-50bps@F62-Other | robustness | train | 1962-01-02 | 2001-12-30 | 0.82 | +7924.9% | 56.4% | 0.00 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-Other | robustness | train | 1962-01-02 | 2001-12-30 | 0.78 | +2693.6% | 40.1% | 2.53 |
| 2026-11-18 11:18 | trend-1926 | equal-weight-50bps@F62-ind10 | robustness | train | 1962-01-02 | 2001-12-30 | 0.91 | +8089.3% | 46.9% | 0.16 |
| 2026-11-18 11:18 | trend-1926 | tsmom12-50bps@F62-ind10 | robustness | train | 1962-01-02 | 2001-12-30 | 0.87 | +2472.9% | 32.4% | 2.33 |
| 2026-11-18 19:18 | gsy-runup | tsmom12@G30-disc | baseline | train | 1928-07-02 | 2001-12-30 | 0.98 | +165635.5% | 39.0% | 2.37 |
| 2026-11-18 19:18 | gsy-runup | equal-weight@G30-disc | baseline | train | 1928-07-02 | 2001-12-30 | 0.73 | +198914.5% | 82.4% | 0.11 |
| 2026-11-18 19:18 | gsy-runup | flag100-cash@G30-disc | variant | train | 1928-07-02 | 2001-12-30 | 1.02 | +133838.8% | 33.5% | 2.35 |
| 2026-11-18 19:18 | gsy-runup | flag150-cash@G30-disc | variant | train | 1928-07-02 | 2001-12-30 | 1.00 | +154205.6% | 35.8% | 2.36 |
| 2026-11-18 19:18 | gsy-runup | flag100-sma@G30-disc | variant | train | 1928-07-02 | 2001-12-30 | 1.01 | +181321.7% | 36.5% | 2.40 |
| 2026-11-18 19:18 | gsy-runup | flag150-sma@G30-disc | variant | train | 1928-07-02 | 2001-12-30 | 0.99 | +171936.9% | 37.8% | 2.38 |
| 2026-11-18 19:18 | gsy-runup | flag100-vol@G30-disc | variant | train | 1928-07-02 | 2001-12-30 | 1.01 | +157830.8% | 36.4% | 2.42 |
| 2026-11-18 19:18 | gsy-runup | flag150-vol@G30-disc | variant | train | 1928-07-02 | 2001-12-30 | 0.99 | +162844.9% | 37.7% | 2.39 |
| 2026-11-18 19:18 | gsy-runup | tsmom12@G30-check | baseline | train | 2002-01-02 | 2025-11-09 | 0.73 | +564.6% | 21.0% | 2.59 |
| 2026-11-18 19:18 | gsy-runup | equal-weight@G30-check | baseline | train | 2002-01-02 | 2025-11-09 | 0.62 | +973.5% | 55.1% | 0.11 |
| 2026-11-18 19:18 | gsy-runup | flag100-cash@G30-check | variant | train | 2002-01-02 | 2025-11-09 | 0.73 | +472.8% | 20.0% | 2.41 |
| 2026-11-18 19:18 | gsy-runup | flag150-cash@G30-check | variant | train | 2002-01-02 | 2025-11-09 | 0.73 | +512.1% | 20.0% | 2.43 |
| 2026-11-18 19:18 | gsy-runup | flag100-sma@G30-check | variant | train | 2002-01-02 | 2025-11-09 | 0.75 | +561.9% | 20.0% | 2.70 |
| 2026-11-18 19:18 | gsy-runup | flag150-sma@G30-check | variant | train | 2002-01-02 | 2025-11-09 | 0.75 | +574.7% | 20.0% | 2.65 |
| 2026-11-18 19:18 | gsy-runup | flag100-vol@G30-check | variant | train | 2002-01-02 | 2025-11-09 | 0.75 | +539.8% | 20.4% | 2.60 |
| 2026-11-18 19:18 | gsy-runup | flag150-vol@G30-check | variant | train | 2002-01-02 | 2025-11-09 | 0.73 | +540.4% | 20.4% | 2.57 |
| 2026-11-18 19:18 | gsy-runup | tsmom12@G10-disc | baseline | train | 1928-07-02 | 2001-12-30 | 0.99 | +168228.2% | 32.5% | 2.36 |
| 2026-11-18 19:18 | gsy-runup | equal-weight@G10-disc | baseline | train | 1928-07-02 | 2001-12-30 | 0.72 | +196508.5% | 82.0% | 0.16 |
| 2026-11-18 19:18 | gsy-runup | flag100-cash@G10-disc | robustness | train | 1928-07-02 | 2001-12-30 | 1.02 | +157027.7% | 30.6% | 2.34 |
| 2026-11-18 19:18 | gsy-runup | flag150-cash@G10-disc | robustness | train | 1928-07-02 | 2001-12-30 | 1.00 | +163720.0% | 32.5% | 2.36 |
| 2026-11-18 19:18 | gsy-runup | flag100-sma@G10-disc | robustness | train | 1928-07-02 | 2001-12-30 | 1.01 | +166041.9% | 31.5% | 2.40 |
| 2026-11-18 19:18 | gsy-runup | flag150-sma@G10-disc | robustness | train | 1928-07-02 | 2001-12-30 | 1.00 | +168806.2% | 32.5% | 2.40 |
| 2026-11-18 19:18 | gsy-runup | flag100-vol@G10-disc | robustness | train | 1928-07-02 | 2001-12-30 | 1.01 | +160321.7% | 31.1% | 2.36 |
| 2026-11-18 19:18 | gsy-runup | flag150-vol@G10-disc | robustness | train | 1928-07-02 | 2001-12-30 | 0.99 | +166074.3% | 32.4% | 2.36 |
| 2026-11-18 19:18 | gsy-runup | tsmom12@G10-check | baseline | train | 2002-01-02 | 2025-11-09 | 0.72 | +503.5% | 23.6% | 2.76 |
| 2026-11-18 19:18 | gsy-runup | equal-weight@G10-check | baseline | train | 2002-01-02 | 2025-11-09 | 0.62 | +917.8% | 52.4% | 0.20 |
| 2026-11-18 19:18 | gsy-runup | flag100-cash@G10-check | robustness | train | 2002-01-02 | 2025-11-09 | 0.74 | +478.2% | 23.6% | 2.44 |
| 2026-11-18 19:18 | gsy-runup | flag150-cash@G10-check | robustness | train | 2002-01-02 | 2025-11-09 | 0.76 | +526.0% | 23.6% | 2.48 |
| 2026-11-18 19:18 | gsy-runup | flag100-sma@G10-check | robustness | train | 2002-01-02 | 2025-11-09 | 0.74 | +517.5% | 23.6% | 2.78 |
| 2026-11-18 19:18 | gsy-runup | flag150-sma@G10-check | robustness | train | 2002-01-02 | 2025-11-09 | 0.75 | +537.7% | 23.6% | 2.76 |
| 2026-11-18 19:18 | gsy-runup | flag100-vol@G10-check | robustness | train | 2002-01-02 | 2025-11-09 | 0.74 | +513.7% | 23.6% | 2.71 |
| 2026-11-18 19:18 | gsy-runup | flag150-vol@G10-check | robustness | train | 2002-01-02 | 2025-11-09 | 0.75 | +539.7% | 23.6% | 2.71 |
| 2026-11-18 19:21 | gsy-runup | tsmom12@ETF4-train | baseline | train | 1999-12-23 | 2025-11-09 | 0.50 | +300.5% | 24.9% | 3.01 |
| 2026-11-18 19:21 | gsy-runup | equal-weight@ETF4-train | baseline | train | 1999-12-23 | 2025-11-09 | 0.50 | +738.2% | 56.7% | 0.39 |
| 2026-11-18 19:21 | gsy-runup | flag100-sma@ETF4-train | robustness | train | 1999-12-23 | 2025-11-09 | 0.45 | +247.8% | 24.9% | 3.20 |
| 2026-11-18 19:21 | gsy-runup | flag100-vol@ETF4-train | robustness | train | 1999-12-23 | 2025-11-09 | 0.48 | +270.0% | 24.9% | 2.95 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Mkt | insure-check | train | 1927-07-02 | 2025-10-31 | 0.82 | +1202861.5% | 38.2% | 1.40 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-NoDur | insure-check | train | 1927-07-02 | 2025-10-31 | 0.87 | +600276.0% | 35.5% | 1.77 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Durbl | insure-check | train | 1927-07-02 | 2025-10-31 | 0.60 | +1108597.3% | 72.5% | 2.36 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Manuf | insure-check | train | 1927-07-02 | 2025-10-31 | 0.74 | +845637.1% | 49.4% | 1.77 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Enrgy | insure-check | train | 1927-07-02 | 2025-10-31 | 0.57 | +231174.0% | 57.0% | 2.55 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-HiTec | insure-check | train | 1927-07-02 | 2025-10-31 | 0.67 | +2644856.0% | 56.9% | 2.01 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Telcm | insure-check | train | 1927-07-02 | 2025-10-31 | 0.76 | +446328.0% | 32.7% | 1.83 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Shops | insure-check | train | 1927-07-02 | 2025-10-31 | 0.81 | +1384864.3% | 52.4% | 1.73 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Hlth | insure-check | train | 1927-07-02 | 2025-10-31 | 0.78 | +1068443.5% | 38.5% | 2.03 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Utils | insure-check | train | 1927-07-02 | 2025-10-31 | 0.78 | +541036.3% | 56.0% | 1.77 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure-Other | insure-check | train | 1927-07-02 | 2025-10-31 | 0.73 | +510119.9% | 48.1% | 1.73 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Food | insure-check | train | 1927-07-02 | 2025-10-31 | 0.82 | +528569.4% | 36.1% | 1.74 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Beer | insure-check | train | 1927-07-02 | 2025-10-31 | 0.61 | +881019.0% | 67.8% | 2.23 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Smoke | insure-check | train | 1927-07-02 | 2025-10-31 | 0.69 | +917498.3% | 51.4% | 2.48 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Games | insure-check | train | 1927-07-02 | 2025-10-31 | 0.59 | +1016849.6% | 57.3% | 2.07 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Books | insure-check | train | 1927-07-02 | 2025-10-31 | 0.69 | +1311500.2% | 45.2% | 1.91 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Hshld | insure-check | train | 1927-07-02 | 2025-10-31 | 0.64 | +236720.3% | 42.7% | 2.21 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Clths | insure-check | train | 1927-07-02 | 2025-10-31 | 0.64 | +184951.2% | 46.5% | 2.27 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Hlth | insure-check | train | 1927-07-02 | 2025-10-31 | 0.78 | +1108305.7% | 38.5% | 2.03 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Chems | insure-check | train | 1927-07-02 | 2025-10-31 | 0.56 | +120707.8% | 59.6% | 2.47 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Txtls | insure-check | train | 1927-07-02 | 2025-10-31 | 0.56 | +123659.1% | 59.4% | 1.90 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Cnstr | insure-check | train | 1927-07-02 | 2025-10-31 | 0.59 | +173008.1% | 61.8% | 2.36 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Steel | insure-check | train | 1927-07-02 | 2025-10-31 | 0.47 | +99832.9% | 76.7% | 2.62 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-FabPr | insure-check | train | 1927-07-02 | 2025-10-31 | 0.66 | +715688.5% | 60.7% | 1.99 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-ElcEq | insure-check | train | 1927-07-02 | 2025-10-31 | 0.63 | +1318608.6% | 59.6% | 1.99 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Autos | insure-check | train | 1927-07-02 | 2025-10-31 | 0.58 | +1031972.7% | 69.4% | 2.50 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Carry | insure-check | train | 1927-07-02 | 2025-10-31 | 0.68 | +1780214.2% | 45.6% | 1.85 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Mines | insure-check | train | 1927-07-02 | 2025-10-31 | 0.45 | +62420.2% | 63.0% | 2.46 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Coal | insure-check | train | 1927-07-02 | 2025-10-31 | 0.41 | +91226.1% | 85.3% | 2.38 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Oil | insure-check | train | 1927-07-02 | 2025-10-31 | 0.58 | +284878.3% | 57.7% | 2.47 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Util | insure-check | train | 1927-07-02 | 2025-10-31 | 0.78 | +526398.9% | 56.0% | 1.77 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Telcm | insure-check | train | 1927-07-02 | 2025-10-31 | 0.76 | +450017.8% | 32.7% | 1.83 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Servs | insure-check | train | 1927-07-02 | 2025-10-31 | 0.45 | +1026331.0% | 91.7% | 1.56 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-BusEq | insure-check | train | 1927-07-02 | 2025-10-31 | 0.70 | +3428047.4% | 49.8% | 2.36 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Paper | insure-check | train | 1927-07-02 | 2025-10-31 | 0.62 | +171532.0% | 48.3% | 2.29 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Trans | insure-check | train | 1927-07-02 | 2025-10-31 | 0.52 | +68510.5% | 55.2% | 2.52 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Whlsl | insure-check | train | 1927-07-02 | 2025-10-31 | 0.66 | +1084716.2% | 53.6% | 2.04 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Rtail | insure-check | train | 1927-07-02 | 2025-10-31 | 0.77 | +1198842.3% | 66.5% | 1.81 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Meals | insure-check | train | 1927-07-02 | 2025-10-31 | 0.71 | +1565555.2% | 48.1% | 1.78 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Fin | insure-check | train | 1927-07-02 | 2025-10-31 | 0.72 | +744261.3% | 48.6% | 2.05 |
| 2026-11-18 22:49 | insure-1 | tsmom12@insure30-Other | insure-check | train | 1927-07-02 | 2025-10-31 | 0.57 | +128598.1% | 57.9% | 2.38 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Japan | insure-check | train | 1966-01-21 | 2025-10-31 | 0.57 | +5522.2% | 40.8% | 2.22 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Canada | insure-check | train | 1980-07-04 | 2025-10-31 | 0.43 | +521.5% | 34.2% | 2.05 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-UK | insure-check | train | 1984-12-28 | 2025-10-31 | 0.38 | +366.0% | 37.6% | 2.62 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Australia | insure-check | train | 1985-08-16 | 2025-10-31 | 0.37 | +323.6% | 54.0% | 2.56 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-HongKong | insure-check | train | 1988-01-08 | 2025-10-31 | 0.37 | +529.5% | 46.5% | 2.51 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Germany | insure-check | train | 1988-12-29 | 2025-10-31 | 0.42 | +563.2% | 51.9% | 1.82 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Singapore | insure-check | train | 1989-01-13 | 2025-10-31 | 0.33 | +206.3% | 47.0% | 2.63 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-France | insure-check | train | 1991-03-08 | 2025-10-31 | 0.38 | +345.6% | 39.8% | 2.11 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Switzerland | insure-check | train | 1991-11-15 | 2025-10-31 | 0.41 | +309.6% | 38.4% | 3.09 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Belgium | insure-check | train | 1992-04-16 | 2025-10-31 | 0.43 | +323.3% | 37.5% | 2.41 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Netherlands | insure-check | train | 1993-10-08 | 2025-10-31 | 0.50 | +559.1% | 36.3% | 2.21 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Austria | insure-check | train | 1993-11-19 | 2025-10-31 | 0.35 | +240.0% | 49.9% | 2.35 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Spain | insure-check | train | 1994-07-15 | 2025-10-31 | 0.47 | +454.9% | 53.7% | 1.95 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-FF-Europe | insure-check | train | 1991-06-21 | 2025-10-31 | 0.50 | +553.7% | 39.0% | 2.30 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-FF-Japan | insure-check | train | 1991-06-21 | 2025-10-31 | 0.31 | +224.2% | 38.6% | 3.11 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-FF-AsiaPacExJapan | insure-check | train | 1991-06-21 | 2025-10-31 | 0.56 | +653.2% | 39.2% | 2.65 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Italy | insure-check | train | 1998-12-18 | 2025-10-31 | 0.14 | +28.5% | 62.3% | 2.05 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-NewZealand | insure-check | train | 2004-01-09 | 2025-10-31 | 0.95 | +485.9% | 25.1% | 1.05 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Israel | insure-check | train | 1993-10-01 | 2025-10-30 | 0.58 | +908.3% | 30.4% | 1.84 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Korea | insure-check | train | 1997-12-26 | 2025-10-31 | 0.48 | +586.6% | 41.8% | 2.98 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Taiwan | insure-check | train | 1998-07-17 | 2025-10-31 | 0.36 | +225.4% | 50.1% | 2.75 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-India | insure-check | train | 1998-07-17 | 2025-10-31 | 0.66 | +1229.8% | 40.7% | 2.23 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Brazil | insure-check | train | 1994-05-06 | 2025-10-31 | 0.57 | +2809.9% | 61.2% | 3.08 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Mexico | insure-check | train | 1992-11-27 | 2025-10-31 | 0.50 | +838.5% | 49.9% | 3.25 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Malaysia | insure-check | train | 1994-12-09 | 2025-10-31 | 0.24 | +76.0% | 45.7% | 2.85 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-Indonesia | insure-check | train | 1991-04-26 | 2025-10-31 | 0.51 | +849.5% | 53.2% | 2.34 |
| 2026-11-18 23:04 | insure-2 | tsmom12@insure-geo-FF-DevExUS | insure-check | train | 1991-06-21 | 2025-10-31 | 0.49 | +390.7% | 36.0% | 2.53 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Mkt | variant | train | 1927-07-02 | 2025-10-31 | 0.82 | +2864104.0% | 50.7% | 2.13 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-NoDur | robustness | train | 1927-07-02 | 2025-10-31 | 0.90 | +1545677.9% | 50.7% | 2.28 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Durbl | robustness | train | 1927-07-02 | 2025-10-31 | 0.63 | +5592185.4% | 75.0% | 3.09 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Manuf | robustness | train | 1927-07-02 | 2025-10-31 | 0.75 | +2462135.9% | 55.9% | 2.44 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Enrgy | robustness | train | 1927-07-02 | 2025-10-31 | 0.57 | +440719.1% | 61.1% | 3.00 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-HiTec | robustness | train | 1927-07-02 | 2025-10-31 | 0.66 | +4524121.2% | 61.6% | 2.72 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Telcm | robustness | train | 1927-07-02 | 2025-10-31 | 0.74 | +721895.8% | 50.6% | 2.36 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Shops | robustness | train | 1927-07-02 | 2025-10-31 | 0.83 | +4049260.1% | 52.0% | 2.40 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Hlth | robustness | train | 1927-07-02 | 2025-10-31 | 0.70 | +846827.7% | 52.6% | 2.76 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Utils | robustness | train | 1927-07-02 | 2025-10-31 | 0.70 | +454232.3% | 69.6% | 2.13 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-Other | robustness | train | 1927-07-02 | 2025-10-31 | 0.74 | +2106804.4% | 53.8% | 2.34 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Japan | robustness | train | 1966-01-21 | 2025-10-31 | 0.60 | +11065.0% | 42.6% | 2.99 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Canada | robustness | train | 1980-07-04 | 2025-10-31 | 0.57 | +1488.7% | 32.6% | 2.80 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-UK | robustness | train | 1984-12-28 | 2025-10-31 | 0.32 | +291.0% | 37.9% | 3.55 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Australia | robustness | train | 1985-08-16 | 2025-10-31 | 0.47 | +682.4% | 44.3% | 3.01 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-HongKong | robustness | train | 1988-01-08 | 2025-10-31 | 0.47 | +1435.4% | 44.4% | 3.67 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Germany | robustness | train | 1988-12-29 | 2025-10-31 | 0.47 | +959.3% | 50.0% | 2.69 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Singapore | robustness | train | 1989-01-13 | 2025-10-31 | 0.53 | +834.2% | 50.2% | 3.29 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-France | robustness | train | 1991-03-08 | 2025-10-31 | 0.31 | +257.8% | 39.5% | 3.55 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Switzerland | robustness | train | 1991-11-15 | 2025-10-31 | 0.30 | +182.8% | 52.9% | 4.03 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Belgium | robustness | train | 1992-04-16 | 2025-10-31 | 0.50 | +550.8% | 36.6% | 3.49 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Netherlands | robustness | train | 1993-10-08 | 2025-10-31 | 0.46 | +528.6% | 41.9% | 2.96 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Austria | robustness | train | 1993-11-19 | 2025-10-31 | 0.54 | +846.2% | 39.5% | 3.10 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-Spain | robustness | train | 1994-07-15 | 2025-10-31 | 0.35 | +287.6% | 63.6% | 4.37 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-FF-Europe | robustness | train | 1991-06-21 | 2025-10-31 | 0.56 | +954.7% | 35.5% | 3.05 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-FF-Japan | robustness | train | 1991-06-21 | 2025-10-31 | 0.30 | +237.8% | 44.0% | 4.16 |
| 2026-11-18 23:14 | fast-reentry | or3-12@insure-geo-FF-AsiaPacExJapan | robustness | train | 1991-06-21 | 2025-10-31 | 0.70 | +1577.6% | 42.2% | 3.40 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Mkt | variant | train | 1927-07-02 | 2025-10-31 | 0.83 | +3095797.2% | 50.7% | 2.40 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-NoDur | robustness | train | 1927-07-02 | 2025-10-31 | 0.91 | +1705190.2% | 48.9% | 2.56 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Durbl | robustness | train | 1927-07-02 | 2025-10-31 | 0.62 | +4320923.1% | 72.0% | 3.60 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Manuf | robustness | train | 1927-07-02 | 2025-10-31 | 0.76 | +2705034.3% | 55.9% | 2.70 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Enrgy | robustness | train | 1927-07-02 | 2025-10-31 | 0.56 | +340852.8% | 60.0% | 3.75 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-HiTec | robustness | train | 1927-07-02 | 2025-10-31 | 0.65 | +3349156.2% | 61.6% | 3.23 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Telcm | robustness | train | 1927-07-02 | 2025-10-31 | 0.73 | +591762.3% | 50.1% | 2.78 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Shops | robustness | train | 1927-07-02 | 2025-10-31 | 0.84 | +4241546.5% | 52.0% | 2.74 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Hlth | robustness | train | 1927-07-02 | 2025-10-31 | 0.71 | +773558.7% | 52.6% | 3.21 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Utils | robustness | train | 1927-07-02 | 2025-10-31 | 0.72 | +546093.8% | 68.4% | 2.50 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-Other | robustness | train | 1927-07-02 | 2025-10-31 | 0.77 | +2792413.0% | 50.9% | 2.66 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Japan | robustness | train | 1966-01-21 | 2025-10-31 | 0.63 | +14051.1% | 41.2% | 3.46 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Canada | robustness | train | 1980-07-04 | 2025-10-31 | 0.58 | +1527.3% | 32.6% | 3.06 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-UK | robustness | train | 1984-12-28 | 2025-10-31 | 0.31 | +265.2% | 39.6% | 4.13 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Australia | robustness | train | 1985-08-16 | 2025-10-31 | 0.46 | +625.4% | 44.3% | 3.70 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-HongKong | robustness | train | 1988-01-08 | 2025-10-31 | 0.46 | +1263.0% | 45.7% | 4.15 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Germany | robustness | train | 1988-12-29 | 2025-10-31 | 0.49 | +1047.4% | 48.6% | 3.01 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Singapore | robustness | train | 1989-01-13 | 2025-10-31 | 0.54 | +840.4% | 47.1% | 3.77 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-France | robustness | train | 1991-03-08 | 2025-10-31 | 0.32 | +262.2% | 45.5% | 3.95 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Switzerland | robustness | train | 1991-11-15 | 2025-10-31 | 0.31 | +198.3% | 50.0% | 4.80 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Belgium | robustness | train | 1992-04-16 | 2025-10-31 | 0.52 | +584.7% | 34.4% | 3.90 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Netherlands | robustness | train | 1993-10-08 | 2025-10-31 | 0.44 | +474.8% | 41.9% | 3.58 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Austria | robustness | train | 1993-11-19 | 2025-10-31 | 0.51 | +706.8% | 37.5% | 3.60 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-Spain | robustness | train | 1994-07-15 | 2025-10-31 | 0.35 | +269.1% | 64.0% | 4.63 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-FF-Europe | robustness | train | 1991-06-21 | 2025-10-31 | 0.54 | +820.3% | 37.8% | 3.75 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-FF-Japan | robustness | train | 1991-06-21 | 2025-10-31 | 0.33 | +303.4% | 45.2% | 4.86 |
| 2026-11-18 23:20 | fast-reentry | arm3-12@insure-geo-FF-AsiaPacExJapan | robustness | train | 1991-06-21 | 2025-10-31 | 0.70 | +1514.9% | 42.2% | 3.98 |
| 2026-11-18 11:07 | trend-where | where-vol | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +24412.0% | 35.3% | 1.71 |
| 2026-11-18 11:07 | trend-where | where-dd | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +21300.2% | 35.7% | 2.41 |
| 2026-11-18 11:07 | trend-where | where-vol@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.65 | +273.8% | 16.8% | 2.38 |
| 2026-11-18 11:07 | trend-where | where-dd@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.53 | +185.1% | 19.5% | 2.61 |
| 2026-11-18 11:07 | trend-where | where-vol@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.61 | +326.9% | 92.4% | 3.77 |
| 2026-11-18 11:07 | trend-where | where-dd@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.59 | +297.6% | 92.4% | 3.80 |
| 2026-11-18 11:07 | trend-where | where-vol@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.72 | +4653.9% | 27.4% | 2.25 |
| 2026-11-18 11:07 | trend-where | where-dd@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.69 | +4293.4% | 30.3% | 2.16 |
| 2026-11-18 11:11 | trend-where | where-vol@F-ind10 | robustness | train | 1927-07-02 | 1961-12-28 | 1.07 | +5912.9% | 32.5% | 1.30 |
| 2026-11-18 19:53 | eu-1 | tsmom12@us6 | robustness | train | 2012-01-02 | 2025-11-09 | 1.37 | +3489.5% | 36.5% | 2.81 |
| 2026-11-18 19:53 | eu-1 | equal-weight@us6 | baseline | train | 2012-01-02 | 2025-11-09 | 1.32 | +5323.5% | 47.0% | 1.29 |
| 2026-11-18 19:53 | eu-1 | tsmom12@us6-eur | robustness | train | 2012-01-02 | 2025-11-09 | 1.39 | +4463.3% | 31.3% | 3.06 |
| 2026-11-18 19:53 | eu-1 | equal-weight@us6-eur | baseline | train | 2012-01-02 | 2025-11-09 | 1.31 | +5914.5% | 42.8% | 1.27 |
| 2026-11-18 19:53 | eu-1 | tsmom12@eu6 | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +4353.7% | 31.0% | 3.13 |
| 2026-11-18 19:53 | eu-1 | equal-weight@eu6 | baseline | train | 2012-01-02 | 2025-11-09 | 1.38 | +5989.6% | 43.0% | 1.24 |
| 2026-11-18 19:53 | eu-1 | tsmom12@usw | robustness | train | 2012-01-02 | 2025-11-09 | 0.63 | +62.7% | 11.1% | 3.02 |
| 2026-11-18 19:53 | eu-1 | equal-weight@usw | baseline | train | 2012-01-02 | 2025-11-09 | 0.67 | +119.1% | 18.7% | 0.24 |
| 2026-11-18 19:53 | eu-1 | tsmom12@usw-eur | robustness | train | 2012-01-02 | 2025-11-09 | 0.54 | +69.8% | 13.8% | 3.04 |
| 2026-11-18 19:53 | eu-1 | equal-weight@usw-eur | baseline | train | 2012-01-02 | 2025-11-09 | 0.64 | +146.2% | 19.1% | 0.23 |
| 2026-11-18 19:53 | eu-1 | tsmom12@euw | robustness | train | 2012-01-02 | 2025-11-09 | 0.56 | +54.2% | 14.3% | 2.92 |
| 2026-11-18 19:53 | eu-1 | equal-weight@euw | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +134.7% | 19.8% | 0.21 |
| 2026-11-18 19:53 | eu-1 | hold-IWDA | baseline | train | 2012-01-02 | 2025-11-09 | 0.86 | +425.8% | 33.6% | 0.03 |
| 2026-11-18 19:53 | eu-1 | hold-SPY | baseline | train | 2012-01-02 | 2025-11-09 | 0.91 | +580.8% | 33.7% | 0.02 |
| 2026-11-18 19:53 | eu-1 | tsmom12@eu6/gym | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +4551.8% | 31.0% | 3.13 |
| 2026-11-18 19:53 | eu-1 | tsmom12@eu6/harsh | robustness | train | 2012-01-02 | 2025-11-09 | 1.41 | +4046.2% | 31.4% | 3.13 |
| 2026-11-18 19:53 | eu-1 | tsmom12@euw/gym | robustness | train | 2012-01-02 | 2025-11-09 | 0.63 | +62.6% | 12.7% | 2.92 |
| 2026-11-18 19:53 | eu-1 | tsmom12@euw/harsh | robustness | train | 2012-01-02 | 2025-11-09 | 0.44 | +39.3% | 18.1% | 2.92 |
| 2026-11-18 19:53 | eu-1 | tsmom12@eu6-is04 | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +5225.0% | 30.2% | 2.89 |
| 2026-11-18 19:53 | eu-1 | equal-weight@eu6-is04 | baseline | train | 2012-01-02 | 2025-11-09 | 1.39 | +7505.8% | 42.7% | 1.28 |
| 2026-11-18 19:53 | eu-1 | tsmom12@SXR8 | robustness | train | 2012-01-02 | 2025-11-09 | 0.70 | +261.4% | 29.2% | 2.03 |
| 2026-11-18 19:53 | eu-1 | hold@SXR8 | baseline | train | 2012-01-02 | 2025-11-09 | 0.97 | +629.6% | 33.8% | 0.02 |
| 2026-11-18 19:53 | eu-1 | tsmom12@SPY | robustness | train | 2012-01-02 | 2025-11-09 | 0.79 | +298.8% | 31.2% | 1.83 |
| 2026-11-18 19:53 | eu-1 | hold@SPY | baseline | train | 2012-01-02 | 2025-11-09 | 0.91 | +580.8% | 33.7% | 0.02 |
| 2026-11-18 19:53 | eu-1 | tsmom12@SXRV | robustness | train | 2012-01-02 | 2025-11-09 | 0.93 | +711.6% | 30.6% | 1.05 |
| 2026-11-18 19:53 | eu-1 | hold@SXRV | baseline | train | 2012-01-02 | 2025-11-09 | 1.06 | +1225.9% | 31.3% | 0.01 |
| 2026-11-18 19:53 | eu-1 | tsmom12@QQQ | robustness | train | 2012-01-02 | 2025-11-09 | 0.90 | +647.1% | 29.6% | 1.02 |
| 2026-11-18 19:53 | eu-1 | hold@QQQ | baseline | train | 2012-01-02 | 2025-11-09 | 0.99 | +1135.1% | 35.1% | 0.02 |
| 2026-11-18 19:53 | eu-1 | tsmom12@4GLD | robustness | train | 2012-01-02 | 2025-11-09 | 0.60 | +142.4% | 21.4% | 2.57 |
| 2026-11-18 19:53 | eu-1 | hold@4GLD | baseline | train | 2012-01-02 | 2025-11-09 | 0.62 | +189.2% | 36.8% | 0.06 |
| 2026-11-18 19:53 | eu-1 | tsmom12@GLD | robustness | train | 2012-01-02 | 2025-11-09 | 0.48 | +98.4% | 29.2% | 2.92 |
| 2026-11-18 19:53 | eu-1 | hold@GLD | baseline | train | 2012-01-02 | 2025-11-09 | 0.50 | +144.4% | 42.1% | 0.07 |
| 2026-11-18 19:53 | eu-1 | tsmom12@IBGL | robustness | train | 2012-01-02 | 2025-11-09 | 0.33 | +36.8% | 21.6% | 3.56 |
| 2026-11-18 19:53 | eu-1 | hold@IBGL | baseline | train | 2012-01-02 | 2025-11-09 | 0.27 | +38.0% | 43.7% | 0.05 |
| 2026-11-18 19:53 | eu-1 | tsmom12@TLT | robustness | train | 2012-01-02 | 2025-11-09 | 0.02 | -4.1% | 33.0% | 2.53 |
| 2026-11-18 19:53 | eu-1 | hold@TLT | baseline | train | 2012-01-02 | 2025-11-09 | 0.11 | +8.7% | 48.4% | 0.06 |
| 2026-11-18 19:53 | eu-1 | tsmom12@euw-2009 | robustness | train | 2009-01-02 | 2025-11-09 | 0.55 | +69.6% | 14.3% | 2.76 |
| 2026-11-18 19:53 | eu-1 | equal-weight@euw-2009 | baseline | train | 2009-01-02 | 2025-11-09 | 0.78 | +200.7% | 19.8% | 0.23 |
| 2026-11-18 19:53 | eu-1 | tsmom12@usw-2009 | robustness | train | 2009-01-02 | 2025-11-09 | 0.59 | +86.7% | 11.1% | 2.89 |
| 2026-11-18 19:53 | eu-1 | equal-weight@usw-2009 | baseline | train | 2009-01-02 | 2025-11-09 | 0.72 | +211.6% | 18.8% | 0.23 |
| 2026-11-18 19:53 | eu-1 | tsmom12@eu6-S-2000 | robustness | train | 2000-01-03 | 2025-11-09 | 0.94 | +4675.6% | 38.9% | 3.14 |
| 2026-11-18 19:53 | eu-1 | equal-weight@eu6-S-2000 | baseline | train | 2000-01-03 | 2025-11-09 | 0.76 | +4673.5% | 70.5% | 1.22 |
| 2026-11-18 19:53 | eu-1 | tsmom12@us6-2000 | robustness | train | 2000-01-03 | 2025-11-09 | 0.99 | +5494.7% | 36.5% | 2.77 |
| 2026-11-18 19:53 | eu-1 | equal-weight@us6-2000 | baseline | train | 2000-01-03 | 2025-11-09 | 0.82 | +6073.2% | 68.8% | 1.27 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/slip-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +4502.3% | 31.0% | 3.12 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/slip-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.38 | +6049.8% | 42.9% | 1.24 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/slip-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.51 | +5219.9% | 27.9% | 2.30 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/slip-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.46 | +7323.0% | 39.7% | 0.40 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/dg1-5k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.41 | +3982.5% | 31.9% | 3.12 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/dg1-5k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.33 | +5116.6% | 44.2% | 1.21 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/dg1-5k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.49 | +5063.3% | 28.0% | 2.31 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/dg1-5k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.47 | +7830.6% | 39.5% | 0.41 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/dg1-25k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +4378.1% | 31.0% | 3.12 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/dg1-25k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.37 | +5812.1% | 43.1% | 1.21 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/dg1-25k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.50 | +5161.8% | 27.9% | 2.30 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/dg1-25k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.46 | +7300.8% | 39.7% | 0.40 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/dg1-100k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +4469.6% | 31.0% | 3.13 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/dg1-100k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.38 | +6002.2% | 43.0% | 1.24 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/dg1-100k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.51 | +5204.3% | 27.9% | 2.30 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/dg1-100k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.46 | +7315.1% | 39.7% | 0.40 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/tr2-5k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.37 | +3558.8% | 32.9% | 3.13 |
| 2026-11-18 20:05 | eu-2 | equal-weight@eu6/tr2-5k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.29 | +4491.6% | 44.3% | 1.24 |
| 2026-11-18 20:05 | eu-2 | tsmom12@eu6/tr2-5k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.47 | +4919.5% | 30.6% | 2.31 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/tr2-5k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.49 | +8530.2% | 37.6% | 0.43 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/tr2-25k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.43 | +4282.0% | 31.1% | 3.12 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/tr2-25k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.36 | +5696.9% | 43.3% | 1.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/tr2-25k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.50 | +5212.8% | 27.9% | 2.30 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/tr2-25k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.46 | +7297.1% | 39.7% | 0.40 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/tr2-100k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +4443.9% | 31.0% | 3.13 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/tr2-100k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.38 | +5964.7% | 43.0% | 1.24 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/tr2-100k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.51 | +5196.9% | 27.9% | 2.30 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/tr2-100k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.46 | +7314.1% | 39.7% | 0.40 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-5k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.33 | +3160.9% | 34.2% | 3.16 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/dg3-5k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.25 | +3940.7% | 45.2% | 1.24 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-5k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +4674.6% | 30.6% | 2.31 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/dg3-5k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.49 | +8244.6% | 38.0% | 0.42 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-25k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +4182.8% | 31.3% | 3.12 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/dg3-25k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.35 | +5426.0% | 43.4% | 1.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-25k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.50 | +5171.2% | 27.9% | 2.30 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/dg3-25k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.46 | +7265.4% | 39.8% | 0.40 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-100k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +4410.2% | 31.0% | 3.12 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/dg3-100k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 1.37 | +5910.2% | 43.1% | 1.24 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-100k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.50 | +5176.9% | 27.9% | 2.30 |
| 2026-11-18 20:06 | eu-2 | equal-weight@eu6/dg3-100k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 1.49 | +7864.8% | 37.9% | 0.42 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-5k-b2.5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +4333.4% | 30.6% | 2.64 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-25k-b2.5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.48 | +4853.9% | 30.8% | 2.62 |
| 2026-11-18 20:06 | eu-2 | tsmom12@eu6/dg3-100k-b2.5 | robustness | train | 2012-01-02 | 2025-11-09 | 1.49 | +5027.6% | 30.8% | 2.63 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/slip-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.62 | +60.9% | 13.0% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/slip-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +133.2% | 19.8% | 0.20 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/slip-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.61 | +64.7% | 14.9% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/slip-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.81 | +139.9% | 19.6% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg1-5k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.50 | +46.7% | 15.9% | 2.91 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg1-5k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.73 | +123.6% | 20.0% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg1-5k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.54 | +54.9% | 17.0% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg1-5k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.80 | +136.5% | 19.7% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg1-25k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.59 | +57.9% | 13.4% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg1-25k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.76 | +131.6% | 19.8% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg1-25k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.59 | +62.6% | 15.3% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg1-25k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.81 | +139.2% | 19.7% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg1-100k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.61 | +60.1% | 13.1% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg1-100k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +135.2% | 19.8% | 0.22 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg1-100k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.60 | +64.1% | 15.0% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg1-100k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.81 | +139.6% | 19.6% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/tr2-5k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.41 | +36.3% | 18.5% | 2.91 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/tr2-5k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.70 | +116.2% | 20.2% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/tr2-5k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.48 | +47.9% | 18.8% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/tr2-5k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.80 | +137.8% | 19.7% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/tr2-25k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.57 | +55.4% | 14.0% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/tr2-25k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +130.5% | 19.9% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/tr2-25k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.58 | +61.1% | 15.5% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/tr2-25k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.81 | +139.4% | 19.7% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/tr2-100k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.61 | +59.4% | 13.2% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/tr2-100k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +133.6% | 19.8% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/tr2-100k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.60 | +63.7% | 15.1% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/tr2-100k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.81 | +139.6% | 19.6% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-5k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.29 | +23.7% | 21.5% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg3-5k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.66 | +105.2% | 20.3% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-5k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.42 | +39.6% | 20.4% | 2.76 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg3-5k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.79 | +134.0% | 19.8% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-25k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.55 | +52.4% | 14.6% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg3-25k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +128.6% | 19.9% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-25k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.57 | +59.0% | 16.0% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg3-25k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.80 | +138.7% | 19.7% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-100k-b1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.60 | +58.7% | 13.3% | 2.92 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg3-100k-b1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.76 | +132.2% | 19.8% | 0.21 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-100k-b5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.60 | +63.2% | 15.2% | 2.77 |
| 2026-11-18 20:06 | eu-2 | equal-weight@euw/dg3-100k-b5 | baseline | train | 2012-01-02 | 2025-11-09 | 0.81 | +139.5% | 19.6% | 0.10 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-5k-b2.5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.39 | +34.7% | 20.0% | 2.80 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-25k-b2.5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.57 | +56.9% | 15.1% | 2.81 |
| 2026-11-18 20:06 | eu-2 | tsmom12@euw/dg3-100k-b2.5 | robustness | train | 2012-01-02 | 2025-11-09 | 0.61 | +61.3% | 14.4% | 2.81 |
| 2026-11-18 20:11 | eu-2 | tsmom12@euw-h | robustness | train | 2012-01-02 | 2025-11-09 | 0.53 | +47.3% | 14.3% | 2.92 |
| 2026-11-18 20:11 | eu-2 | equal-weight@euw-h | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +123.2% | 19.8% | 0.21 |
| 2026-11-18 20:11 | eu-2 | tsmom12@euw-hh | robustness | train | 2012-01-02 | 2025-11-09 | 0.43 | +35.5% | 16.5% | 2.95 |
| 2026-11-18 20:11 | eu-2 | equal-weight@euw-hh | baseline | train | 2012-01-02 | 2025-11-09 | 0.70 | +110.4% | 19.8% | 0.22 |
| 2026-11-18 20:11 | eu-2 | tsmom12@eu6-h | robustness | train | 2012-01-02 | 2025-11-09 | 1.43 | +4148.5% | 32.1% | 3.07 |
| 2026-11-18 20:11 | eu-2 | equal-weight@eu6-h | baseline | train | 2012-01-02 | 2025-11-09 | 1.36 | +5607.3% | 44.0% | 1.25 |
| 2026-11-18 20:11 | eu-2 | tsmom12@IUSEL | robustness | train | 2012-01-02 | 2025-11-09 | 0.62 | +169.6% | 30.6% | 2.02 |
| 2026-11-18 20:11 | eu-2 | hold@IUSEL | baseline | train | 2012-01-02 | 2025-11-09 | 0.82 | +399.0% | 34.8% | 0.03 |
| 2026-11-18 20:11 | eu-2 | tsmom12@XAD1 | robustness | train | 2012-01-02 | 2025-11-09 | 0.27 | +40.1% | 40.9% | 3.00 |
| 2026-11-18 20:11 | eu-2 | hold@XAD1 | baseline | train | 2012-01-02 | 2025-11-09 | 0.37 | +84.2% | 44.0% | 0.08 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.62 | +60.9% | 13.0% | 2.92 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/dg1-5k | robustness | train | 2012-01-02 | 2025-11-09 | 0.50 | +46.7% | 15.9% | 2.91 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/dg1-10k | robustness | train | 2012-01-02 | 2025-11-09 | 0.56 | +53.4% | 14.4% | 2.92 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/dg1-25k | robustness | train | 2012-01-02 | 2025-11-09 | 0.59 | +57.9% | 13.4% | 2.92 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/tr2-5k | robustness | train | 2012-01-02 | 2025-11-09 | 0.41 | +36.3% | 18.5% | 2.91 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/tr2-10k | robustness | train | 2012-01-02 | 2025-11-09 | 0.51 | +48.0% | 15.7% | 2.92 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/tr2-25k | robustness | train | 2012-01-02 | 2025-11-09 | 0.57 | +55.4% | 14.0% | 2.92 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/dg3-5k | robustness | train | 2012-01-02 | 2025-11-09 | 0.29 | +23.7% | 21.5% | 2.92 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/dg3-10k | robustness | train | 2012-01-02 | 2025-11-09 | 0.46 | +41.3% | 17.2% | 2.92 |
| 2026-11-18 20:20 | eu-3 | tsmom12@euw/dg3-25k | robustness | train | 2012-01-02 | 2025-11-09 | 0.55 | +52.4% | 14.6% | 2.92 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/slip | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +133.2% | 19.8% | 0.20 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/dg1-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.73 | +123.6% | 20.0% | 0.21 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/dg1-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +128.9% | 19.9% | 0.21 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/dg1-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.76 | +131.6% | 19.8% | 0.21 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/tr2-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.70 | +116.2% | 20.2% | 0.21 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/tr2-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.73 | +125.1% | 20.1% | 0.21 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/tr2-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +130.5% | 19.9% | 0.21 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/dg3-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.66 | +105.2% | 20.3% | 0.21 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/dg3-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.71 | +119.7% | 20.1% | 0.22 |
| 2026-11-18 20:20 | eu-3 | equal-weight@euw/dg3-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +128.6% | 19.9% | 0.21 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.63 | +62.6% | 13.2% | 4.12 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/dg1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.53 | +49.1% | 15.7% | 4.12 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/dg1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +55.5% | 14.3% | 4.12 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/dg1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +60.0% | 13.6% | 4.12 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/tr2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.44 | +39.4% | 18.2% | 4.11 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/tr2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.53 | +50.4% | 15.5% | 4.12 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/tr2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +57.3% | 14.0% | 4.12 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/dg3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.33 | +27.3% | 21.1% | 4.11 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/dg3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.48 | +44.3% | 16.9% | 4.11 |
| 2026-11-18 20:20 | eu-3 | V0-w-fri@euw/dg3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.57 | +54.8% | 14.5% | 4.12 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.75 | +84.2% | 13.6% | 1.90 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/dg1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.70 | +75.1% | 14.2% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/dg1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.73 | +79.8% | 13.6% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/dg1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.74 | +82.4% | 13.6% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/tr2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.65 | +69.3% | 15.4% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/tr2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.71 | +77.0% | 14.0% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/tr2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.74 | +81.3% | 13.6% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/dg3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +60.8% | 17.2% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/dg3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.68 | +72.1% | 14.8% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V1-m@euw/dg3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.72 | +79.5% | 13.6% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.65 | +62.3% | 15.5% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/dg1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.56 | +51.6% | 17.8% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/dg1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +56.6% | 16.8% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/dg1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.63 | +60.0% | 16.0% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/tr2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.48 | +43.3% | 20.0% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/tr2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.57 | +52.9% | 17.6% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/tr2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +58.3% | 16.4% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/dg3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.40 | +33.6% | 22.4% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/dg3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.53 | +47.7% | 18.7% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V2-m-in@euw/dg3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +56.1% | 16.9% | 2.96 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.70 | +74.1% | 12.6% | 3.41 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/dg1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +61.0% | 13.8% | 3.40 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/dg1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.65 | +67.3% | 12.7% | 3.40 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/dg1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.68 | +71.2% | 12.7% | 3.41 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/tr2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.53 | +51.8% | 16.1% | 3.40 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/tr2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +62.3% | 13.8% | 3.39 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/tr2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.66 | +69.1% | 12.7% | 3.40 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/dg3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.44 | +40.4% | 18.7% | 3.39 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/dg3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.57 | +56.3% | 15.0% | 3.40 |
| 2026-11-18 20:20 | eu-3 | V3-hold4w@euw/dg3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.64 | +66.6% | 12.8% | 3.40 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.71 | +87.4% | 16.6% | 3.68 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/dg1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.64 | +75.8% | 16.6% | 3.67 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/dg1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.67 | +81.4% | 16.6% | 3.67 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/dg1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.69 | +85.0% | 16.6% | 3.68 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/tr2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +67.5% | 16.8% | 3.67 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/tr2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.65 | +77.4% | 16.6% | 3.67 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/tr2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.68 | +83.3% | 16.6% | 3.68 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/dg3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.51 | +56.5% | 18.9% | 3.68 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/dg3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +71.6% | 16.7% | 3.67 |
| 2026-11-18 20:20 | eu-3 | V4-c4@euw/dg3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.67 | +80.9% | 16.6% | 3.67 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.77 | +103.6% | 17.0% | 1.92 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/dg1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.74 | +95.6% | 17.0% | 1.92 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/dg1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.75 | +99.5% | 17.0% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/dg1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.77 | +101.9% | 17.0% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/tr2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.71 | +91.5% | 17.1% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/tr2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.74 | +97.3% | 17.0% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/tr2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.76 | +101.1% | 17.0% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/dg3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.67 | +83.8% | 17.1% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/dg3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.72 | +93.5% | 17.1% | 1.91 |
| 2026-11-18 20:20 | eu-3 | V5-c4-m@euw/dg3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.75 | +99.4% | 17.0% | 1.91 |
| 2026-11-18 20:20 | eu-3 | ew-c4@euw/slip | baseline | train | 2012-01-02 | 2025-11-09 | 0.90 | +170.9% | 19.9% | 0.25 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.62 | +62.8% | 16.3% | 1.52 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.64 | +67.2% | 15.4% | 1.11 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@eu6/slip | robustness | train | 2012-01-02 | 2025-11-09 | 1.40 | +4045.4% | 32.6% | 2.38 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@eu6/slip | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +4598.8% | 31.7% | 1.84 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@usw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.61 | +62.5% | 12.2% | 1.88 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@usw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.56 | +57.3% | 14.3% | 1.22 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.54 | +52.2% | 18.3% | 1.52 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +57.8% | 17.2% | 1.53 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +60.8% | 16.6% | 1.53 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.48 | +45.2% | 19.8% | 1.53 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.54 | +53.5% | 18.1% | 1.52 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +59.4% | 16.9% | 1.53 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.41 | +36.7% | 21.6% | 1.52 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.51 | +48.7% | 19.0% | 1.53 |
| 2026-11-18 22:09 | eu-4 | C1-confirm2@euw/eur3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.57 | +57.0% | 17.4% | 1.53 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +58.4% | 16.5% | 1.10 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +62.8% | 15.9% | 1.10 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.63 | +65.2% | 15.5% | 1.10 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.53 | +52.7% | 17.7% | 1.10 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +59.6% | 16.5% | 1.10 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.62 | +64.2% | 15.6% | 1.10 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.47 | +44.7% | 19.5% | 1.11 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.56 | +55.6% | 17.1% | 1.10 |
| 2026-11-18 22:09 | eu-4 | C2-dz25@euw/eur3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +62.5% | 16.0% | 1.10 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +60.9% | 13.7% | 4.10 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.62 | +64.7% | 13.6% | 2.79 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@eu6/slip | robustness | train | 2012-01-02 | 2025-11-09 | 1.18 | +19716.3% | 64.7% | 2.50 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@eu6/slip | robustness | train | 2012-01-02 | 2025-11-09 | 1.48 | +4912.3% | 30.5% | 2.36 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@usw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.64 | +64.6% | 10.7% | 4.33 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@usw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.66 | +69.3% | 10.9% | 2.91 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.51 | +48.5% | 16.3% | 4.10 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.56 | +54.6% | 14.9% | 4.10 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +58.4% | 14.1% | 4.11 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.44 | +40.3% | 18.6% | 4.09 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.52 | +49.9% | 16.1% | 4.10 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.57 | +56.4% | 14.6% | 4.10 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.35 | +29.7% | 21.4% | 4.08 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.48 | +44.3% | 17.4% | 4.09 |
| 2026-11-18 22:18 | eu-5 | D1-flipreb@euw/eur3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.55 | +53.9% | 15.1% | 4.10 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.55 | +55.0% | 15.3% | 2.78 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +59.3% | 14.5% | 2.79 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +62.5% | 14.0% | 2.79 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.49 | +47.9% | 17.3% | 2.78 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.56 | +56.4% | 15.1% | 2.79 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +60.9% | 14.2% | 2.79 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.42 | +38.2% | 19.5% | 2.77 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.53 | +51.6% | 16.4% | 2.78 |
| 2026-11-18 22:18 | eu-5 | D2-band25r@euw/eur3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +58.8% | 14.6% | 2.79 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/slip | baseline | train | 2012-01-02 | 2025-11-09 | 0.78 | +134.2% | 19.8% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/slip | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +156.7% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | trend525@usw-2007 | robustness | train | 2007-03-01 | 2025-11-09 | 0.64 | +124.0% | 10.9% | 2.69 |
| 2026-11-18 22:27 | eu-6 | hold7@usw-2007 | baseline | train | 2007-03-01 | 2025-11-09 | 0.63 | +225.2% | 32.0% | 0.13 |
| 2026-11-18 22:27 | eu-6 | mix60@usw-2007 | baseline | train | 2007-03-01 | 2025-11-09 | 0.54 | +193.2% | 32.0% | 0.08 |
| 2026-11-18 22:27 | eu-6 | t-proxy@long-monthly | robustness | train | 1972-02-01 | 2025-09-01 | 1.26 | +6483.1% | 12.5% | 1.12 |
| 2026-11-18 22:27 | eu-6 | h-proxy@long-monthly | baseline | train | 1972-02-01 | 2025-09-01 | 1.20 | +11192.4% | 20.8% | 0.27 |
| 2026-11-18 22:27 | eu-6 | m-proxy@long-monthly | baseline | train | 1972-02-01 | 2025-09-01 | 1.14 | +12155.1% | 27.0% | 0.19 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur1-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.76 | +129.7% | 20.0% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur1-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +153.7% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur1-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +132.3% | 19.9% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur1-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +155.0% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur1-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.78 | +133.6% | 19.8% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur1-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +156.0% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur2-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.76 | +130.3% | 20.0% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur2-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +155.2% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur2-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +132.6% | 19.8% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur2-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +155.7% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur2-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +131.8% | 20.0% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur2-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +156.3% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur3-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +126.6% | 20.1% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur3-5k | baseline | train | 2012-01-02 | 2025-11-09 | 0.74 | +151.6% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur3-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.76 | +130.1% | 20.0% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur3-10k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +154.4% | 22.3% | 0.09 |
| 2026-11-18 22:27 | eu-6 | hold7@euw/eur3-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.77 | +132.8% | 19.9% | 0.10 |
| 2026-11-18 22:27 | eu-6 | mix60@euw/eur3-25k | baseline | train | 2012-01-02 | 2025-11-09 | 0.75 | +155.6% | 22.3% | 0.09 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +71.8% | 16.1% | 1.21 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.79 | +83.7% | 13.8% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@usw-2007 | robustness | train | 2007-03-01 | 2025-11-09 | 0.67 | +151.9% | 14.1% | 1.21 |
| 2026-11-18 22:34 | eu-7 | hold7cash@usw-2007 | robustness | train | 2007-03-01 | 2025-11-09 | 0.60 | +119.0% | 22.1% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks-proxy@long-monthly | robustness | train | 1972-02-01 | 2025-09-01 | 1.24 | +8764.3% | 19.4% | 0.44 |
| 2026-11-18 22:34 | eu-7 | hold7cash-proxy@long-monthly | robustness | train | 1972-02-01 | 2025-09-01 | 1.20 | +2363.1% | 14.3% | 0.19 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.57 | +66.0% | 16.0% | 1.20 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.76 | +78.6% | 13.7% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +68.7% | 16.1% | 1.20 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.77 | +79.7% | 13.7% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +70.6% | 16.1% | 1.21 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.78 | +82.5% | 13.7% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.55 | +63.0% | 16.5% | 1.23 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.76 | +79.1% | 13.8% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +67.6% | 16.0% | 1.20 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.77 | +80.1% | 13.7% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +70.2% | 16.1% | 1.21 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.78 | +82.6% | 13.7% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.51 | +56.3% | 16.4% | 1.22 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.75 | +76.8% | 13.9% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.56 | +64.3% | 16.4% | 1.24 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.76 | +78.9% | 13.8% | 0.08 |
| 2026-11-18 22:34 | eu-7 | trendstocks@euw/eur3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.59 | +68.7% | 16.1% | 1.20 |
| 2026-11-18 22:34 | eu-7 | hold7cash@euw/eur3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.78 | +82.2% | 13.7% | 0.08 |
| 2026-11-18 22:44 | eu-8 | trend525-estr@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.64 | +67.4% | 14.0% | 2.79 |
| 2026-11-18 22:44 | eu-8 | hold7cash-estr@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.82 | +87.7% | 13.8% | 0.08 |
| 2026-11-18 22:44 | eu-8 | hold7-estr@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.78 | +134.6% | 19.8% | 0.10 |
| 2026-11-18 22:44 | eu-8 | mix60-estr@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.75 | +157.3% | 22.3% | 0.09 |
| 2026-11-18 22:44 | eu-8 | trend525-estr0@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.66 | +69.2% | 13.6% | 2.79 |
| 2026-11-18 22:44 | eu-8 | hold7cash-estr0@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.83 | +89.6% | 13.8% | 0.08 |
| 2026-11-18 22:44 | eu-8 | hold7-estr0@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.78 | +134.8% | 19.8% | 0.10 |
| 2026-11-18 22:44 | eu-8 | mix60-estr0@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.76 | +157.5% | 22.3% | 0.09 |
| 2026-11-18 22:44 | eu-8 | trend525-irx@usw-2007 | robustness | train | 2007-03-01 | 2025-11-09 | 0.70 | +144.0% | 10.9% | 2.69 |
| 2026-11-18 22:44 | eu-8 | hold7cash-irx@usw-2007 | robustness | train | 2007-03-01 | 2025-11-09 | 0.66 | +139.9% | 21.9% | 0.08 |
| 2026-11-18 22:44 | eu-8 | hold7-irx@usw-2007 | robustness | train | 2007-03-01 | 2025-11-09 | 0.63 | +227.4% | 31.9% | 0.13 |
| 2026-11-18 22:44 | eu-8 | mix60-irx@usw-2007 | robustness | train | 2007-03-01 | 2025-11-09 | 0.55 | +196.4% | 32.0% | 0.08 |
| 2026-11-18 22:44 | eu-8 | trend525-irx-proxy@long-monthly | robustness | train | 1972-02-01 | 2025-09-01 | 1.47 | +13037.9% | 11.7% | 1.11 |
| 2026-11-18 22:44 | eu-8 | hold7cash-irx-proxy@long-monthly | robustness | train | 1972-02-01 | 2025-09-01 | 1.48 | +5249.6% | 11.6% | 0.19 |
| 2026-11-18 22:44 | eu-8 | hold7-irx-proxy@long-monthly | robustness | train | 1972-02-01 | 2025-09-01 | 1.20 | +11192.4% | 20.8% | 0.27 |
| 2026-11-18 22:44 | eu-8 | mix60-irx-proxy@long-monthly | robustness | train | 1972-02-01 | 2025-09-01 | 1.14 | +12155.1% | 27.0% | 0.19 |
| 2026-11-18 22:48 | eu-8 | trendsl@usw-2007-2011 | robustness | train | 2007-03-01 | 2011-12-31 | 0.77 | +40.4% | 10.8% | 1.22 |
| 2026-11-18 22:48 | eu-8 | trendsl-proxy@long-monthly-1994-2011 | robustness | train | 1994-01-01 | 2011-12-01 | 1.46 | +316.5% | 6.7% | 0.52 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/slip | variant | train | 2012-01-02 | 2025-11-09 | 0.63 | +73.7% | 15.9% | 1.68 |
| 2026-11-18 22:48 | eu-8 | trendsl-estr@euw/slip | robustness | train | 2012-01-02 | 2025-11-09 | 0.64 | +75.7% | 15.9% | 1.68 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur1-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +65.6% | 16.1% | 1.69 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur1-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +69.9% | 15.9% | 1.69 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur1-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.62 | +71.9% | 15.9% | 1.70 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur2-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.54 | +61.1% | 16.4% | 1.70 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur2-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.58 | +67.5% | 15.9% | 1.68 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur2-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.61 | +71.1% | 15.9% | 1.69 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur3-5k | variant | train | 2012-01-02 | 2025-11-09 | 0.48 | +52.5% | 17.0% | 1.70 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur3-10k | variant | train | 2012-01-02 | 2025-11-09 | 0.56 | +63.7% | 16.4% | 1.70 |
| 2026-11-18 22:48 | eu-8 | trendsl@euw/eur3-25k | variant | train | 2012-01-02 | 2025-11-09 | 0.60 | +69.8% | 15.9% | 1.69 |
| 2026-11-17 23:27 | slow-1-screen | cot_spec h=4w (IC +0.016, chance 0.045, WF -0.019, z +0.17 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_spec_chg4 h=4w (IC -0.013, chance 0.044, WF +0.012, z +0.48 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_spec_z3y h=4w (IC -0.034, chance 0.058, WF +0.045, z +1.66 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_lev h=4w (IC +0.047, chance 0.073, WF -0.006, z -0.15 vs 3.40, no) | screen | train | 2006-06-23 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_am h=4w (IC -0.033, chance 0.059, WF -0.009, z +0.24 vs 3.40, no) | screen | train | 2006-06-23 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | fund_bn h=4w (IC -0.044, chance 0.180, WF +0.117, z +0.79 vs 3.40, no) | screen | train | 2020-01-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | prem_bn h=4w (IC -0.022, chance 0.222, WF +0.003, z -0.05 vs 3.40, no) | screen | train | 2020-01-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | fund_drb h=4w (IC -0.010, chance 0.139, WF +0.025, z +0.45 vs 3.40, no) | screen | train | 2019-05-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dvol_rv h=4w (IC -0.024, chance 0.167, WF +nan, z nan vs 3.40, no) | screen | train | 2021-03-26 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | puell h=4w (IC +0.069, chance 0.136, WF +0.002, z -0.05 vs 3.40, no) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | hash_growth h=4w (IC -0.013, chance 0.162, WF +0.190, z +1.53 vs 3.40, near) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | tx_growth h=4w (IC +0.114, chance 0.159, WF +0.070, z +0.85 vs 3.40, no) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | fng h=4w (IC +0.143, chance 0.224, WF +0.143, z +0.99 vs 3.40, no) | screen | train | 2018-02-09 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vix_term h=4w (IC +0.046, chance 0.058, WF +0.050, z +1.42 vs 3.40, no) | screen | train | 2009-09-25 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vix_term6 h=4w (IC +0.010, chance 0.072, WF +0.039, z +1.20 vs 3.40, no) | screen | train | 2008-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | skew_z h=4w (IC +0.011, chance 0.070, WF +0.012, z +0.12 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vvix_vix h=4w (IC +0.009, chance 0.056, WF +0.012, z +0.95 vs 3.40, no) | screen | train | 2006-03-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vrp h=4w (IC +0.014, chance 0.055, WF +0.010, z +0.43 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | pc_total h=4w (IC +0.015, chance 0.077, WF +0.018, z +0.50 vs 3.40, no) | screen | train | 2006-11-17 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | pc_equity h=4w (IC +0.028, chance 0.077, WF +0.072, z +1.30 vs 3.40, no) | screen | train | 2006-11-17 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | usd_13w h=4w (IC -0.053, chance 0.070, WF +0.045, z +1.30 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | oil_13w h=4w (IC -0.005, chance 0.059, WF +0.043, z +1.57 vs 3.40, no) | screen | train | 2000-11-24 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | hy_ief_13w h=4w (IC -0.011, chance 0.082, WF +0.048, z +1.16 vs 3.40, no) | screen | train | 2007-07-13 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z7 h=4w (IC +0.018, chance 0.038, WF +0.040, z +2.50 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z30 h=4w (IC +0.027, chance 0.063, WF +0.050, z +2.05 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z91 h=4w (IC +0.046, chance 0.070, WF +0.052, z +1.84 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z182 h=4w (IC +0.051, chance 0.075, WF +0.053, z +1.91 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z365 h=4w (IC +0.062, chance 0.078, WF +0.046, z +1.17 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | up_12m h=4w (IC +0.052, chance 0.071, WF +0.026, z +1.05 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | sma_gap h=4w (IC +0.062, chance 0.079, WF +0.065, z +2.19 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | log_vol h=4w (IC -0.015, chance 0.081, WF +0.013, z +0.67 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vol_shock h=4w (IC +0.008, chance 0.062, WF +0.013, z +0.68 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dd_1y h=4w (IC +0.059, chance 0.073, WF +0.052, z +1.66 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | since_high h=4w (IC -0.076, chance 0.072, WF +0.052, z +1.65 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | breadth h=4w (IC +0.059, chance 0.073, WF +0.026, z +0.92 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | univ_mom_1m h=4w (IC +0.021, chance 0.072, WF +0.005, z +0.21 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | univ_vol_shock h=4w (IC -0.014, chance 0.062, WF +0.028, z +1.22 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | rank_12m h=4w (IC +0.029, chance 0.056, WF +0.020, z +1.19 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | halving h=4w (IC -0.104, chance 0.211, WF -0.005, z -0.57 vs 3.40, no) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dff30 h=4w (IC +0.007, chance 0.066, WF +0.056, z +2.15 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dff_chg182 h=4w (IC +0.030, chance 0.081, WF +0.020, z +0.75 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | real_ff h=4w (IC +0.080, chance 0.068, WF -0.047, z -0.92 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | curve h=4w (IC +0.015, chance 0.068, WF -0.006, z +0.02 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | baa20 h=4w (IC -0.010, chance 0.072, WF +0.012, z +0.44 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | real_m2 h=4w (IC +0.013, chance 0.084, WF +0.008, z +0.40 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | unrate_rise h=4w (IC +0.028, chance 0.064, WF +0.004, z +0.33 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cpi_yoy h=4w (IC -0.089, chance 0.060, WF +0.038, z +2.18 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dgs10 h=4w (IC -0.030, chance 0.052, WF +0.022, z +1.05 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vix h=4w (IC +0.011, chance 0.068, WF +0.002, z +0.32 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_spec h=13w (IC +0.030, chance 0.069, WF -0.051, z -0.21 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_spec_chg4 h=13w (IC -0.041, chance 0.041, WF +0.035, z +1.97 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_spec_z3y h=13w (IC -0.054, chance 0.100, WF +0.057, z +1.27 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_lev h=13w (IC +0.068, chance 0.115, WF +0.025, z +0.43 vs 3.40, no) | screen | train | 2006-06-23 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cot_am h=13w (IC -0.029, chance 0.094, WF -0.012, z -0.09 vs 3.40, no) | screen | train | 2006-06-23 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | fund_bn h=13w (IC -0.012, chance 0.281, WF -0.188, z -0.90 vs 3.40, no) | screen | train | 2020-01-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | prem_bn h=13w (IC +0.014, chance 0.323, WF -0.133, z -0.65 vs 3.40, no) | screen | train | 2020-01-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | fund_drb h=13w (IC -0.027, chance 0.206, WF +0.186, z +1.28 vs 3.40, no) | screen | train | 2019-05-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dvol_rv h=13w (IC -0.047, chance 0.182, WF +nan, z nan vs 3.40, no) | screen | train | 2021-03-26 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | puell h=13w (IC +0.054, chance 0.239, WF -0.029, z -0.42 vs 3.40, no) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | hash_growth h=13w (IC -0.043, chance 0.280, WF +0.262, z +1.32 vs 3.40, no) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | tx_growth h=13w (IC +0.158, chance 0.236, WF +0.158, z +1.19 vs 3.40, no) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | fng h=13w (IC +0.172, chance 0.318, WF +0.157, z +0.74 vs 3.40, no) | screen | train | 2018-02-09 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vix_term h=13w (IC +0.067, chance 0.078, WF +0.072, z +1.43 vs 3.40, no) | screen | train | 2009-09-25 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vix_term6 h=13w (IC +0.021, chance 0.102, WF +0.066, z +1.53 vs 3.40, no) | screen | train | 2008-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | skew_z h=13w (IC +0.021, chance 0.114, WF -0.036, z -1.17 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vvix_vix h=13w (IC +0.025, chance 0.097, WF -0.018, z +0.09 vs 3.40, no) | screen | train | 2006-03-10 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vrp h=13w (IC +0.018, chance 0.064, WF +0.016, z +0.54 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | pc_total h=13w (IC +0.005, chance 0.115, WF +0.039, z +0.66 vs 3.40, no) | screen | train | 2006-11-17 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | pc_equity h=13w (IC -0.004, chance 0.110, WF +0.030, z +0.55 vs 3.40, no) | screen | train | 2006-11-17 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | usd_13w h=13w (IC -0.115, chance 0.111, WF +0.151, z +2.82 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | oil_13w h=13w (IC -0.045, chance 0.087, WF +0.022, z +0.57 vs 3.40, no) | screen | train | 2000-11-24 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | hy_ief_13w h=13w (IC +0.013, chance 0.127, WF +0.038, z +0.43 vs 3.40, no) | screen | train | 2007-07-13 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z7 h=13w (IC +0.015, chance 0.038, WF +0.046, z +2.52 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z30 h=13w (IC +0.048, chance 0.073, WF +0.070, z +2.10 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z91 h=13w (IC +0.067, chance 0.110, WF +0.068, z +1.55 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z182 h=13w (IC +0.101, chance 0.118, WF +0.078, z +1.60 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | z365 h=13w (IC +0.076, chance 0.132, WF +0.046, z +0.48 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | up_12m h=13w (IC +0.081, chance 0.126, WF +0.046, z +0.79 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | sma_gap h=13w (IC +0.106, chance 0.123, WF +0.093, z +1.79 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | log_vol h=13w (IC -0.034, chance 0.133, WF +0.015, z +0.60 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vol_shock h=13w (IC -0.020, chance 0.090, WF -0.004, z +0.11 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dd_1y h=13w (IC +0.093, chance 0.128, WF +0.083, z +1.58 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | since_high h=13w (IC -0.108, chance 0.126, WF +0.064, z +1.14 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | breadth h=13w (IC +0.079, chance 0.127, WF +0.022, z +0.47 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | univ_mom_1m h=13w (IC +0.048, chance 0.071, WF +0.036, z +1.21 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | univ_vol_shock h=13w (IC -0.028, chance 0.089, WF +0.055, z +1.59 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | rank_12m h=13w (IC +0.046, chance 0.095, WF +0.017, z +0.82 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | halving h=13w (IC -0.143, chance 0.327, WF +0.048, z -0.34 vs 3.40, no) | screen | train | 2013-01-04 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dff30 h=13w (IC +0.029, chance 0.119, WF +0.059, z +1.67 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dff_chg182 h=13w (IC +0.079, chance 0.147, WF +0.065, z +1.38 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | real_ff h=13w (IC +0.146, chance 0.120, WF -0.089, z -1.01 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | curve h=13w (IC +0.005, chance 0.117, WF +0.003, z +0.22 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | baa20 h=13w (IC -0.029, chance 0.129, WF +0.037, z +0.97 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | real_m2 h=13w (IC +0.003, chance 0.145, WF +0.006, z +0.33 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | unrate_rise h=13w (IC +0.037, chance 0.121, WF +0.011, z +0.47 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | cpi_yoy h=13w (IC -0.146, chance 0.102, WF +0.058, z +1.95 vs 3.40, near) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | dgs10 h=13w (IC -0.035, chance 0.083, WF +0.015, z +0.89 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | vix h=13w (IC -0.013, chance 0.110, WF +0.004, z +0.38 vs 3.40, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | combined slow4 h=4w (gain +0.028 over up_12m +0.025, z +1.25 vs 2.09, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | combined all-sign h=4w (gain -0.013 over up_12m +0.025, z +0.12 vs 2.09, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | combined all-ridge h=4w (gain -0.005 over up_12m +0.025, z +0.46 vs 2.09, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | combined slow4 h=13w (gain +0.013 over up_12m +0.028, z +0.55 vs 2.09, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | combined all-sign h=13w (gain -0.011 over up_12m +0.028, z +0.37 vs 2.09, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-screen | combined all-ridge h=13w (gain -0.001 over up_12m +0.028, z +0.52 vs 2.09, no) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-control | plant10-fast h=4w (planted IC +0.100, WF +0.090, z +4.50 vs 3.40) | control | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-control | plant10-slow h=4w (planted IC +0.100, WF +0.097, z +4.15 vs 3.40) | control | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-control | plant10-fast h=13w (planted IC +0.100, WF +0.093, z +2.73 vs 3.40) | control | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:27 | slow-1-control | plant10-slow h=13w (planted IC +0.100, WF +0.075, z +1.73 vs 3.40) | control | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | before h=13w (S +0.013, p 0.438, null sd 0.063, 4306 cells, 1487 weeks) | screen | train | 1971-04-09 | 1999-10-01 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | markets h=13w (S +0.070, p 0.118, null sd 0.061, 22563 cells, 1336 weeks) | screen | train | 2000-01-07 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins h=13w (S +0.267, p 0.004, null sd 0.126, 30307 cells, 433 weeks) | screen | train | 2017-04-28 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | before h=4w (S -0.013, p 0.637, null sd 0.042, 4342 cells, 1496 weeks) | screen | train | 1971-04-09 | 1999-12-03 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | markets h=4w (S +0.036, p 0.165, null sd 0.037, 22725 cells, 1345 weeks) | screen | train | 2000-01-07 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins h=4w (S +0.144, p 0.043, null sd 0.083, 31189 cells, 442 weeks) | screen | train | 2017-04-28 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | markets-resid h=13w (S -0.001, p 0.506, null sd 0.033, 22563 cells, 1336 weeks) | screen | train | 2000-01-07 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins-resid h=13w (S -0.087, p 0.826, null sd 0.084, 29531 cells, 433 weeks) | screen | train | 2017-04-28 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | markets-resid h=4w (S +0.005, p 0.418, null sd 0.020, 22725 cells, 1345 weeks) | screen | train | 2000-01-07 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins-resid h=4w (S -0.031, p 0.724, null sd 0.053, 30329 cells, 442 weeks) | screen | train | 2017-04-28 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins: the protocol's six, gym bars h=13w (S +0.319, p 0.002, null sd 0.116, 2010 cells, 417 weeks) | robustness | train | 2017-08-18 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | before: from 1974 h=13w (S +0.019, p 0.397, null sd 0.066, 4020 cells, 1344 weeks) | robustness | train | 1974-01-04 | 1999-10-01 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | markets: Fed broad index (2006+) h=13w (S +0.023, p 0.359, null sd 0.071, 18064 cells, 1009 weeks) | robustness | train | 2006-04-14 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins: Fed broad index (2006+) h=13w (S +0.222, p 0.029, null sd 0.120, 30307 cells, 433 weeks) | robustness | train | 2017-04-28 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | left out: IEF from 2000 h=13w (S -0.044, p 0.660, null sd 0.090, 1150 cells, 1150 weeks) | robustness | train | 2003-08-01 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | left out: LQD from 2000 h=13w (S +0.002, p 0.487, null sd 0.096, 1150 cells, 1150 weeks) | robustness | train | 2003-08-01 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | left out: GSPC from 2000 h=13w (S +0.096, p 0.111, null sd 0.076, 1336 cells, 1336 weeks) | robustness | train | 2000-01-07 | 2025-08-08 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins: the protocol's six, gym bars h=4w (S +0.107, p 0.052, null sd 0.073, 2064 cells, 426 weeks) | robustness | train | 2017-08-18 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | before: from 1974 h=4w (S -0.009, p 0.591, null sd 0.043, 4056 cells, 1353 weeks) | robustness | train | 1974-01-04 | 1999-12-03 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | markets: Fed broad index (2006+) h=4w (S +0.018, p 0.305, null sd 0.043, 18226 cells, 1018 weeks) | robustness | train | 2006-04-14 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | coins: Fed broad index (2006+) h=4w (S +0.130, p 0.058, null sd 0.080, 31189 cells, 442 weeks) | robustness | train | 2017-04-28 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | left out: IEF from 2000 h=4w (S -0.062, p 0.844, null sd 0.060, 1159 cells, 1159 weeks) | robustness | train | 2003-08-01 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | left out: LQD from 2000 h=4w (S +0.015, p 0.402, null sd 0.061, 1159 cells, 1159 weeks) | robustness | train | 2003-08-01 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | left out: GSPC from 2000 h=4w (S +0.036, p 0.205, null sd 0.046, 1345 cells, 1345 weeks) | robustness | train | 2000-01-07 | 2025-10-10 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | pooled before+markets+coins h=13w (P +1.16, p 0.025, 3 of 3 sets S > 0) | screen | train | 1971-01-01 | 2025-11-09 | - | - | - | - |
| 2026-11-18 01:49 | usd-1 | pooled before+markets+coins h=4w (P +0.80, p 0.120, 2 of 3 sets S > 0) | screen | train | 1971-01-01 | 2025-11-09 | - | - | - | - |
| 2026-11-17 23:26 | deep-1 | liquidity/walcl-and@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.51 | +150.4% | 17.0% | 2.55 |
| 2026-11-17 23:26 | deep-1 | absorption-ratio/six@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.64 | +379.4% | 90.0% | 3.88 |
| 2026-11-17 23:26 | deep-1 | trend-to-safe/safe@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.54 | +179.5% | 92.4% | 4.62 |
| 2026-11-17 23:26 | deep-1 | liquidity/walcl-and@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.53 | +216.5% | 69.5% | 1.92 |
| 2026-11-17 23:26 | deep-1 | hmm-regime/hard@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.57 | +1585.4% | 37.8% | 7.82 |
| 2026-11-17 23:26 | deep-1 | fracdiff-momentum/d0.4@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.67 | +2829.0% | 34.6% | 8.23 |
| 2026-11-17 23:26 | deep-1 | drawdown-control/d1.0@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.71 | +1840.1% | 21.9% | 3.42 |
| 2026-11-17 23:26 | deep-1 | absorption-ratio/six@idx | robustness | train | 2002-01-01 | 2025-11-09 | 0.40 | +138.7% | 34.5% | 1.38 |
| 2026-11-17 23:26 | deep-1 | hawkes-clustering/down2@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.60 | +2955.0% | 57.7% | 6.68 |
| 2026-11-17 23:26 | deep-1 | ensemble-tsmom/e4@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.77 | +2977.8% | 23.4% | 5.43 |
| 2026-11-17 23:26 | deep-1 | trend-vol/tv40@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.72 | +4379.0% | 25.3% | 2.30 |
| 2026-11-17 23:26 | deep-1 | trend-to-safe/safe@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.72 | +4377.3% | 25.7% | 2.28 |
| 2026-11-17 23:27 | deep-1 | fed-hiking/hike-and@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.65 | +1425.0% | 23.9% | 2.08 |
| 2026-11-17 23:27 | deep-1 | real-rate/real-and@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.63 | +1690.9% | 26.0% | 2.47 |
| 2026-11-17 23:27 | deep-1 | yield-curve/curve-and@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.69 | +2040.2% | 25.7% | 1.64 |
| 2026-11-17 23:27 | deep-1 | liquidity/m2-and@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.59 | +1638.0% | 28.5% | 2.08 |
| 2026-11-17 23:27 | deep-1 | liquidity/walcl-and@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.66 | +2602.2% | 25.7% | 2.12 |
| 2026-11-17 23:27 | deep-1 | credit-spread/spread-and@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.70 | +3161.0% | 27.2% | 2.14 |
| 2026-11-18 01:34 | deep-1-stack | stack | variant | train | 1994-02-01 | 2025-11-09 | 1.01 | +4061.1% | 30.9% | 1.21 |
| 2026-11-18 01:34 | deep-1-switch | switch | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +8204.3% | 34.7% | 3.15 |
| 2026-11-18 01:34 | deep-1-meta | meta | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +7647.5% | 32.3% | 2.26 |
| 2026-11-18 01:34 | deep-1-stack | stack@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.52 | +180.5% | 17.3% | 3.91 |
| 2026-11-18 01:34 | deep-1-switch | switch@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.56 | +154.8% | 16.8% | 6.00 |
| 2026-11-18 01:34 | deep-1-meta | meta@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.59 | +189.8% | 16.7% | 2.13 |
| 2026-11-18 01:34 | deep-1-stack | stack@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.44 | +67.1% | 92.4% | 7.49 |
| 2026-11-18 01:34 | deep-1-switch | switch@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.54 | +192.1% | 92.4% | 5.57 |
| 2026-11-18 01:34 | deep-1-meta | meta@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.59 | +310.5% | 91.9% | 3.89 |
| 2026-11-18 01:34 | deep-1-stack | stack@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.73 | +2099.3% | 24.0% | 2.17 |
| 2026-11-18 01:34 | deep-1-switch | switch@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.63 | +1617.6% | 22.9% | 3.73 |
| 2026-11-18 01:34 | deep-1-meta | meta@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.75 | +2859.9% | 23.3% | 2.98 |
| 2026-11-18 01:35 | deep-1-meta | naive-1n | baseline | train | 1994-02-01 | 2025-11-09 | 1.06 | +7367.4% | 39.7% | 2.49 |
| 2026-11-18 11:02 | cointop-1-cm | stop-0.25 on the coin book (pooled single-coin 0.42, vs TS -0.01 p 0.55) | variant | train | 2019-04-07 | 2025-11-09 | 1.00 | +350.3% | 37.0% | 3.28 |
| 2026-11-18 11:02 | cointop-1-cm | stop-0.5 on the coin book (pooled single-coin 0.38, vs TS -0.06 p 0.72) | variant | train | 2019-04-07 | 2025-11-09 | 0.72 | +290.5% | 59.5% | 3.80 |
| 2026-11-18 11:02 | cointop-1-cm | stop-0.75 on the coin book (pooled single-coin 0.38, vs TS -0.06 p 0.83) | variant | train | 2019-04-07 | 2025-11-09 | 0.67 | +280.0% | 64.1% | 4.16 |
| 2026-11-18 11:02 | cointop-1-cm | stop-1 on the coin book (pooled single-coin 0.41, vs TS -0.03 p 0.86) | variant | train | 2019-04-07 | 2025-11-09 | 0.68 | +320.1% | 64.4% | 4.10 |
| 2026-11-18 11:02 | cointop-1-cm | fade-28 on the coin book (pooled single-coin 0.58, vs TS +0.14 p 0.10) | variant | train | 2019-04-07 | 2025-11-09 | 1.23 | +1026.1% | 35.9% | 7.07 |
| 2026-11-18 11:02 | cointop-1-cm | fade-56 on the coin book (pooled single-coin 0.47, vs TS +0.03 p 0.42) | variant | train | 2019-04-07 | 2025-11-09 | 0.84 | +441.6% | 46.8% | 5.35 |
| 2026-11-18 11:02 | cointop-1-cm | fade-91 on the coin book (pooled single-coin 0.43, vs TS -0.00 p 0.51) | variant | train | 2019-04-07 | 2025-11-09 | 0.79 | +397.5% | 53.8% | 4.70 |
| 2026-11-18 11:02 | cointop-1-cm | fade-182 on the coin book (pooled single-coin 0.33, vs TS -0.11 p 0.96) | variant | train | 2019-04-07 | 2025-11-09 | 0.57 | +181.0% | 67.4% | 4.29 |
| 2026-11-18 11:02 | cointop-1-cm | breadth-28 on the coin book (pooled single-coin 0.61, vs TS +0.18 p 0.14) | variant | train | 2019-04-07 | 2025-11-09 | 1.12 | +951.6% | 42.7% | 6.81 |
| 2026-11-18 11:02 | cointop-1-cm | breadth-56 on the coin book (pooled single-coin 0.44, vs TS +0.01 p 0.50) | variant | train | 2019-04-07 | 2025-11-09 | 0.73 | +343.2% | 62.8% | 5.24 |
| 2026-11-18 11:02 | cointop-1-cm | breadth-91 on the coin book (pooled single-coin 0.44, vs TS +0.00 p 0.49) | variant | train | 2019-04-07 | 2025-11-09 | 0.72 | +339.7% | 63.1% | 3.95 |
| 2026-11-18 11:02 | cointop-1-cm | breadth-182 on the coin book (pooled single-coin 0.33, vs TS -0.10 p 0.86) | variant | train | 2019-04-07 | 2025-11-09 | 0.50 | +121.2% | 75.5% | 3.71 |
| 2026-11-18 11:02 | cointop-1-cm | TS twin on the selection set (pooled single-coin 0.44) | baseline | train | 2019-04-07 | 2025-11-09 | 0.72 | +391.2% | 64.5% | 4.04 |
| 2026-11-18 11:02 | cointop-1-cm | stop-0.25 control: condition read 26 weeks late (pooled 0.44) | control | train | 2019-04-07 | 2025-11-09 | 0.99 | +268.8% | 32.3% | 3.10 |
| 2026-11-18 11:02 | cointop-1-cm | fade-28 control: condition read 26 weeks late (pooled 0.44) | control | train | 2019-04-07 | 2025-11-09 | 0.87 | +369.9% | 45.5% | 6.39 |
| 2026-11-18 11:02 | cointop-1-cm | breadth-28 control: condition read 26 weeks late (pooled 0.46) | control | train | 2019-04-07 | 2025-11-09 | 0.74 | +294.2% | 53.7% | 5.77 |
| 2026-11-18 11:08 | cointop-1-stop | stop-0.25 | variant | train | 1994-02-01 | 2025-11-09 | 1.09 | +9967.0% | 28.9% | 3.81 |
| 2026-11-18 11:08 | cointop-1-fade | fade-28 | variant | train | 1994-02-01 | 2025-11-09 | 1.09 | +12344.2% | 28.9% | 4.76 |
| 2026-11-18 11:08 | cointop-1-breadth | breadth-28 | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +14344.8% | 29.9% | 4.30 |
| 2026-11-18 11:08 | cointop-1-stop | stop-0.25@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.51 | +211.8% | 64.3% | 4.28 |
| 2026-11-18 11:08 | cointop-1-fade | fade-28@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.55 | +273.2% | 81.7% | 9.05 |
| 2026-11-18 11:08 | cointop-1-breadth | breadth-28@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.51 | +197.3% | 91.6% | 7.35 |
| 2026-11-18 11:08 | cointop-1-stop | stop-0.25@BTC | robustness | train | 2013-01-01 | 2025-11-09 | 1.25 | +79142.5% | 67.6% | 6.20 |
| 2026-11-18 11:08 | cointop-1-fade | fade-28@BTC | robustness | train | 2013-01-01 | 2025-11-09 | 1.28 | +150817.0% | 77.0% | 10.14 |
| 2026-11-18 11:08 | cointop-1-breadth | breadth-28@BTC | robustness | train | 2013-01-01 | 2025-11-09 | 1.23 | +186942.5% | 78.1% | 8.37 |
| 2026-11-18 11:08 | cointop-1-stop | stop-0.25@ETH | robustness | train | 2017-05-19 | 2025-11-09 | 0.95 | +2085.5% | 62.2% | 6.51 |
| 2026-11-18 11:08 | cointop-1-fade | fade-28@ETH | robustness | train | 2017-05-19 | 2025-11-09 | 0.91 | +2159.3% | 76.9% | 9.58 |
| 2026-11-18 11:08 | cointop-1-breadth | breadth-28@ETH | robustness | train | 2017-05-19 | 2025-11-09 | 0.94 | +2595.0% | 82.3% | 8.19 |
| 2026-11-18 11:08 | cointop-1-stop | stop-0.25-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.07 | +9061.6% | 29.0% | 3.79 |
| 2026-11-18 11:08 | cointop-1-fade | fade-28-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +10808.9% | 29.0% | 4.72 |
| 2026-11-18 11:08 | cointop-1-breadth | breadth-28-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +12994.4% | 30.2% | 4.26 |
| 2026-11-18 11:08 | cointop-1 | tsmom12-daily | baseline | train | 1994-02-01 | 2025-11-09 | 1.06 | +19463.0% | 35.8% | 4.89 |
| 2026-11-18 11:08 | cointop-1-stop | stop-0.25-daily | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +7587.0% | 30.9% | 7.96 |
| 2026-11-18 11:08 | cointop-1-fade | fade-28-daily | robustness | train | 1994-02-01 | 2025-11-09 | 1.11 | +12690.9% | 30.9% | 10.52 |
| 2026-11-18 11:08 | cointop-1-breadth | breadth-28-daily | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +12568.5% | 33.1% | 8.98 |
| 2026-11-18 11:15 | coin-cap | cap10-cash | variant | train | 1994-02-01 | 2025-11-09 | 1.00 | +3803.8% | 28.9% | 2.04 |
| 2026-11-18 11:15 | coin-cap | cap10-rest | variant | train | 1994-02-01 | 2025-11-09 | 1.02 | +4578.9% | 28.9% | 2.72 |
| 2026-11-18 11:15 | coin-cap | cap15-cash | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +6701.1% | 28.9% | 2.30 |
| 2026-11-18 11:15 | coin-cap | cap15-rest | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +7565.2% | 28.9% | 2.82 |
| 2026-11-18 11:15 | coin-cap | cap20-cash | variant | train | 1994-02-01 | 2025-11-09 | 1.08 | +11223.2% | 28.9% | 2.49 |
| 2026-11-18 11:15 | coin-cap | cap20-rest | variant | train | 1994-02-01 | 2025-11-09 | 1.09 | +12163.3% | 28.9% | 2.89 |
| 2026-11-18 11:15 | coin-cap | cap25-cash | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +13608.9% | 28.9% | 2.61 |
| 2026-11-18 11:15 | coin-cap | cap25-rest | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +14041.1% | 28.9% | 2.83 |
| 2026-11-18 11:15 | coin-cap | cap-wf | variant | train | 1994-02-01 | 2025-11-09 | 1.05 | +10189.5% | 28.9% | 2.30 |
| 2026-11-18 11:15 | coin-cap | cap10-cash-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 0.99 | +3679.2% | 29.0% | 2.05 |
| 2026-11-18 11:15 | coin-cap | cap10-rest-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +4422.7% | 29.0% | 2.72 |
| 2026-11-18 11:15 | coin-cap | cap15-cash-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +6415.8% | 29.0% | 2.30 |
| 2026-11-18 11:15 | coin-cap | cap15-rest-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +7234.4% | 29.0% | 2.82 |
| 2026-11-18 11:15 | coin-cap | cap20-cash-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.07 | +10615.8% | 29.0% | 2.49 |
| 2026-11-18 11:15 | coin-cap | cap20-rest-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.08 | +11525.2% | 29.0% | 2.90 |
| 2026-11-18 11:15 | coin-cap | cap25-cash-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +12774.3% | 29.0% | 2.61 |
| 2026-11-18 11:15 | coin-cap | cap25-rest-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +13342.9% | 29.0% | 2.83 |
| 2026-11-18 11:15 | coin-cap | cap-wf-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +9867.8% | 29.0% | 2.30 |
| 2026-11-18 11:19 | coin-cap | cap-wf coin years reread | robustness | train | 2013-01-01 | 2025-11-09 | 1.44 | +1796.6% | 27.2% | 2.30 |
| 2026-11-18 19:07 | coin-cap-2 | TS twin, extended coin book (all coins, 2013 on) | baseline | train | 2013-02-10 | 2025-11-09 | 1.14 | +21116.3% | 83.2% | 4.38 |
| 2026-11-18 19:07 | coin-cap-2 | stop-0.25, extended coin book | robustness | train | 2013-02-10 | 2025-11-09 | 1.34 | +9685.3% | 37.0% | 5.23 |
| 2026-11-18 19:07 | coin-cap-2 | cap matched cost f*=0.663, extended coin book | variant | train | 2013-02-10 | 2025-11-09 | 1.15 | +6037.3% | 66.4% | 2.90 |
| 2026-11-18 19:07 | coin-cap-2 | cap matched time f_time=0.311, extended coin book | variant | train | 2013-02-10 | 2025-11-09 | 1.17 | +818.0% | 37.5% | 1.36 |
| 2026-11-18 19:19 | coin-cap-3 | stop-0.25-d, extended coin book | variant | train | 2013-02-10 | 2025-11-09 | 1.41 | +123002.3% | 65.8% | 9.60 |
| 2026-11-18 19:19 | coin-cap-3 | stop-0.25-dx, extended coin book | variant | train | 2013-02-10 | 2025-11-09 | 1.46 | +129969.1% | 68.6% | 6.08 |
| 2026-11-18 19:19 | coin-cap-3 | stop-0.25-d, extended coin book, 2x cost | robustness | train | 2013-02-10 | 2025-11-09 | 1.34 | +78935.0% | 67.3% | 9.60 |
| 2026-11-18 19:19 | coin-cap-3 | stop-0.25-dx, extended coin book, 2x cost | robustness | train | 2013-02-10 | 2025-11-09 | 1.41 | +96112.4% | 70.0% | 6.08 |
| 2026-11-18 19:19 | coin-cap-3 | stop-0.25 weekly, extended coin book, 2x cost | robustness | train | 2013-02-10 | 2025-11-09 | 1.32 | +90470.3% | 68.6% | 4.16 |
| 2026-11-18 19:19 | coin-cap-3 | TS twin, extended coin book, 2x cost | baseline | train | 2013-02-10 | 2025-11-09 | 1.21 | +258381.9% | 83.8% | 3.48 |
| 2026-11-18 22:11 | coin-cap-4 | cap25+stop | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +7620.3% | 28.9% | 3.60 |
| 2026-11-18 22:11 | coin-cap-4 | pstop-0.25 | variant | train | 1994-02-01 | 2025-11-09 | 1.12 | +12968.8% | 28.9% | 3.18 |
| 2026-11-18 22:11 | coin-cap-4 | cap25+stop-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +6960.5% | 29.0% | 3.58 |
| 2026-11-18 22:11 | coin-cap-4 | pstop-0.25-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.10 | +12082.3% | 29.0% | 3.19 |
| 2026-11-18 22:11 | coin-cap-4 | pstop-0.25, extended coin book | variant | train | 2013-02-10 | 2025-11-09 | 1.49 | +190837.6% | 64.1% | 3.55 |
| 2026-11-18 22:11 | coin-cap-4 | pstop-0.25, extended coin book, 2x cost | robustness | train | 2013-02-10 | 2025-11-09 | 1.46 | +163343.9% | 64.1% | 3.55 |
| 2026-11-18 22:41 | stop-reentry | stop-cool-13 | variant | train | 1994-02-01 | 2025-11-09 | 1.04 | +5969.5% | 28.9% | 2.79 |
| 2026-11-18 22:41 | stop-reentry | stop-cool-13-2xcost | robustness | train | 1994-02-01 | 2025-11-09 | 1.03 | +5623.9% | 29.0% | 2.79 |
| 2026-11-18 22:41 | stop-reentry | stop-cool-13, extended coin book | variant | train | 2013-02-10 | 2025-11-09 | 1.41 | +98643.5% | 65.9% | 2.83 |
| 2026-11-18 22:41 | stop-reentry | stop-cool-13, extended coin book, 2x cost | robustness | train | 2013-02-10 | 2025-11-09 | 1.39 | +86869.4% | 66.1% | 2.83 |
