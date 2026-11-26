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
  From rl-5 (2026-11-18) a `screen` row of idea `rl-5-screen` is one input's pooled
  third-against-third book after 10 bps (weekly, Sharpe with sqrt(52), turnover = weight changes
  a year), sign picked in sample; numbers in `results/rl-5-screen.md`.
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
- `search` (added 2026-11-18, evo-1): one row for a whole automated rule search; the Variant
  cell states how many rules it evaluated (they are not logged one by one). Counts as that many
  tries for any deflation (`protocol.md`, "Evolved-rule search tests").
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
| 2026-11-17 22:58 | rl-4-control | ols3-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +4633.2% | 38.6% | 2.96 |
| 2026-11-17 22:58 | rl-4-control | ols3-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4364.8% | 39.0% | 9.07 |
| 2026-11-17 22:58 | rl-4-control | ols3-0.10 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +5859.6% | 38.9% | 13.58 |
| 2026-11-17 22:58 | rl-4-control | ols3-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15348.6% | 35.5% | 17.04 |
| 2026-11-17 22:58 | rl-4-control | ridge28-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5295.6% | 34.9% | 2.77 |
| 2026-11-17 22:58 | rl-4-control | ridge28-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4979.5% | 33.6% | 3.86 |
| 2026-11-17 22:58 | rl-4-control | ridge28-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4525.5% | 38.0% | 8.77 |
| 2026-11-17 22:58 | rl-4-control | ridge28-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.25 | +12569.1% | 35.3% | 14.92 |
| 2026-11-17 22:58 | rl-4-control | lasso28-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5255.0% | 37.0% | 2.77 |
| 2026-11-17 22:58 | rl-4-control | lasso28-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4674.8% | 36.2% | 6.40 |
| 2026-11-17 22:58 | rl-4-control | lasso28-0.10 | control | train | 2000-01-07 | 2025-11-09 | 1.06 | +6071.7% | 32.8% | 12.48 |
| 2026-11-17 22:58 | rl-4-control | lasso28-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.35 | +16401.2% | 24.9% | 16.76 |
| 2026-11-17 22:58 | rl-4-control | ols28-pool-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +2879.3% | 31.3% | 6.32 |
| 2026-11-17 22:58 | rl-4-control | ols28-pool-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +3396.3% | 31.8% | 8.69 |
| 2026-11-17 22:58 | rl-4-control | ols28-pool-0.10 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +4723.5% | 31.1% | 11.85 |
| 2026-11-17 22:58 | rl-4-control | ols28-pool-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.32 | +13815.5% | 26.3% | 15.51 |
| 2026-11-17 22:58 | rl-4-control | ols28-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.88 | +2727.1% | 42.0% | 4.92 |
| 2026-11-17 22:58 | rl-4-control | ols28-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.90 | +2879.4% | 40.8% | 7.48 |
| 2026-11-17 22:58 | rl-4-control | ols28-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +3953.6% | 39.4% | 10.84 |
| 2026-11-17 22:58 | rl-4-control | ols28-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.25 | +10922.9% | 35.3% | 14.80 |
| 2026-11-17 23:09 | rl-4-perp-B-out | ls-ml, perp 10 bps + funding | variant | train | 2022-01-08 | 2025-11-09 | -0.55 | -36.1% | 47.7% | 21.48 |
| 2026-11-17 23:09 | rl-4-perp-B-out | ls-ml, perp 30 bps + funding | robustness | train | 2022-01-08 | 2025-11-09 | -0.83 | -47.5% | 55.6% | 21.48 |
| 2026-11-17 23:09 | rl-4-perp-B-out | ls-funding, perp 10 bps + funding | baseline | train | 2022-01-08 | 2025-11-09 | 0.37 | +14.2% | 24.2% | 42.45 |
| 2026-11-17 23:09 | rl-4-perp-B-out | ls-funding, perp 30 bps + funding | robustness | train | 2022-01-08 | 2025-11-09 | -0.46 | -19.5% | 34.7% | 42.45 |
| 2026-11-17 23:09 | rl-4-perp-B-out | ls-equal, perp 10 bps + funding | baseline | train | 2022-01-08 | 2025-11-09 | -0.38 | -20.4% | 36.0% | 35.82 |
| 2026-11-17 23:09 | rl-4-perp-B-out | ls-equal, perp 30 bps + funding | robustness | train | 2022-01-08 | 2025-11-09 | -0.95 | -41.1% | 51.5% | 35.82 |
| 2026-11-17 23:09 | rl-4-perp-B-out | tsmom12 twin, perp close as spot, 30 bps | baseline | train | 2022-01-08 | 2025-11-09 | -0.30 | -43.2% | 52.7% | 4.00 |
| 2026-11-17 23:09 | rl-4-perp-Bybit | ls-ml, perp 10 bps + funding | variant | train | 2022-05-14 | 2025-11-09 | -0.00 | -7.1% | 35.7% | 23.04 |
| 2026-11-17 23:09 | rl-4-perp-Bybit | ls-ml, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | -0.26 | -23.0% | 40.8% | 23.04 |
| 2026-11-17 23:09 | rl-4-perp-Bybit | ls-funding, perp 10 bps + funding | baseline | train | 2022-05-14 | 2025-11-09 | 0.31 | +12.9% | 19.5% | 46.16 |
| 2026-11-17 23:09 | rl-4-perp-Bybit | ls-funding, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | -0.35 | -19.6% | 29.5% | 46.16 |
| 2026-11-17 23:09 | rl-4-perp-Bybit | ls-equal, perp 10 bps + funding | baseline | train | 2022-05-14 | 2025-11-09 | 0.19 | +6.4% | 25.6% | 37.20 |
| 2026-11-17 23:09 | rl-4-perp-Bybit | ls-equal, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | -0.26 | -19.7% | 30.6% | 37.20 |
| 2026-11-17 23:09 | rl-4-perp-Bybit | tsmom12 twin, perp close as spot, 30 bps | baseline | train | 2022-05-14 | 2025-11-09 | 0.20 | +1.3% | 51.3% | 5.64 |
| 2026-11-17 23:09 | rl-4-perp-Hyperliquid | ls-ml, perp 10 bps + funding | variant | train | 2023-06-10 | 2025-11-09 | 0.49 | +27.2% | 33.5% | 25.08 |
| 2026-11-17 23:09 | rl-4-perp-Hyperliquid | ls-ml, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | 0.29 | +11.0% | 33.6% | 25.08 |
| 2026-11-17 23:09 | rl-4-perp-Hyperliquid | ls-funding, perp 10 bps + funding | baseline | train | 2023-06-10 | 2025-11-09 | 0.47 | +23.6% | 27.1% | 44.28 |
| 2026-11-17 23:09 | rl-4-perp-Hyperliquid | ls-funding, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | 0.10 | -1.5% | 27.3% | 44.28 |
| 2026-11-17 23:09 | rl-4-perp-Hyperliquid | ls-equal, perp 10 bps + funding | baseline | train | 2023-06-10 | 2025-11-09 | 0.43 | +20.4% | 33.8% | 40.34 |
| 2026-11-17 23:09 | rl-4-perp-Hyperliquid | ls-equal, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | 0.09 | -2.2% | 37.1% | 40.34 |
| 2026-11-17 23:09 | rl-4-perp-Hyperliquid | tsmom12 twin, perp close as spot, 30 bps | baseline | train | 2023-06-10 | 2025-11-09 | 0.52 | +37.6% | 51.3% | 11.32 |
| 2026-11-17 23:09 | rl-4-perp-pooled | ls-ml, equal capital per venue | variant | train | 2022-01-08 | 2025-11-09 | 0.03 | -4.0% | 31.6% | nan |
| 2026-11-17 23:09 | rl-4-perp-pooled | ls-ml @30, equal capital per venue | robustness | train | 2022-01-08 | 2025-11-09 | -0.27 | -21.8% | 39.6% | nan |
| 2026-11-17 23:09 | rl-4-perp-pooled | ls-funding, equal capital per venue | baseline | train | 2022-01-08 | 2025-11-09 | 0.57 | +24.4% | 19.1% | nan |
| 2026-11-17 23:09 | rl-4-perp-pooled | ls-funding @30, equal capital per venue | robustness | train | 2022-01-08 | 2025-11-09 | -0.27 | -13.1% | 28.6% | nan |
| 2026-11-17 23:09 | rl-4-perp-pooled | ls-equal, equal capital per venue | baseline | train | 2022-01-08 | 2025-11-09 | 0.06 | -0.5% | 27.4% | nan |
| 2026-11-17 23:09 | rl-4-perp-pooled | ls-equal @30, equal capital per venue | robustness | train | 2022-01-08 | 2025-11-09 | -0.51 | -26.9% | 38.8% | nan |
| 2026-11-17 23:09 | rl-4-perp-pooled | tsmom12 twin, equal capital per venue | baseline | train | 2022-01-08 | 2025-11-09 | 0.01 | -22.7% | 49.6% | nan |
| 2026-11-17 23:11 | rl-4-perp-B-out | ls-ml-ret, perp 10 bps + funding | variant | train | 2022-01-08 | 2025-11-09 | 0.00 | +0.0% | 0.0% | 0.00 |
| 2026-11-17 23:11 | rl-4-perp-B-out | ls-ml-ret, perp 30 bps + funding | robustness | train | 2022-01-08 | 2025-11-09 | 0.00 | +0.0% | 0.0% | 0.00 |
| 2026-11-17 23:11 | rl-4-perp-Bybit | ls-ml-ret, perp 10 bps + funding | variant | train | 2022-05-14 | 2025-11-09 | 0.00 | +0.0% | 0.0% | 0.00 |
| 2026-11-17 23:11 | rl-4-perp-Bybit | ls-ml-ret, perp 30 bps + funding | robustness | train | 2022-05-14 | 2025-11-09 | 0.00 | +0.0% | 0.0% | 0.00 |
| 2026-11-17 23:11 | rl-4-perp-Hyperliquid | ls-ml-ret, perp 10 bps + funding | variant | train | 2023-06-10 | 2025-11-09 | 0.00 | +0.0% | 0.0% | 0.00 |
| 2026-11-17 23:11 | rl-4-perp-Hyperliquid | ls-ml-ret, perp 30 bps + funding | robustness | train | 2023-06-10 | 2025-11-09 | 0.00 | +0.0% | 0.0% | 0.00 |
| 2026-11-17 23:11 | rl-4-perp-pooled | ls-ml-ret, equal capital per venue | variant | train | 2022-01-08 | 2025-11-09 | 0.00 | +0.0% | 0.0% | nan |
| 2026-11-17 23:11 | rl-4-perp-pooled | ls-ml-ret @30, equal capital per venue | robustness | train | 2022-01-08 | 2025-11-09 | 0.00 | +0.0% | 0.0% | nan |
| 2026-11-17 23:12 | rl-4-control | ols1-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +5395.5% | 36.5% | 2.79 |
| 2026-11-17 23:12 | rl-4-control | ols1-0.05 | control | train | 2000-01-07 | 2025-11-09 | 1.02 | +4982.8% | 32.1% | 10.53 |
| 2026-11-17 23:12 | rl-4-control | ols1-0.10 | control | train | 2000-01-07 | 2025-11-09 | 1.13 | +7125.5% | 29.6% | 14.63 |
| 2026-11-17 23:12 | rl-4-control | ols1-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.42 | +19509.5% | 22.2% | 17.35 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3521.3% | 35.1% | 3.17 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3888.7% | 35.5% | 2.98 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4720.5% | 35.4% | 3.04 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3494.0% | 35.6% | 2.98 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4268.1% | 34.9% | 3.04 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +3636.0% | 35.1% | 3.21 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4084.9% | 35.4% | 2.97 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4435.5% | 35.1% | 3.02 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4696.1% | 35.4% | 3.03 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +4476.5% | 35.0% | 3.23 |
| 2026-11-18 01:31 | rl-4-control | ppo3-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4096.8% | 35.0% | 3.02 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +3514.4% | 34.9% | 3.59 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4109.0% | 35.0% | 3.26 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4158.4% | 35.7% | 3.56 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +3650.2% | 35.5% | 3.19 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4286.0% | 35.5% | 3.35 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3923.0% | 35.2% | 3.67 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3850.6% | 35.0% | 3.72 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4562.6% | 35.3% | 3.61 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.92 | +3421.9% | 35.0% | 3.30 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4073.2% | 35.7% | 3.76 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +3909.3% | 35.8% | 3.42 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +3964.3% | 35.3% | 4.49 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4587.7% | 34.9% | 5.78 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4180.0% | 35.7% | 4.59 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4126.9% | 35.0% | 4.11 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4518.0% | 35.0% | 4.36 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4497.6% | 35.3% | 5.65 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4268.6% | 35.2% | 4.96 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s7 | control | train | 2000-01-07 | 2025-11-09 | 1.00 | +4997.7% | 35.8% | 5.21 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.99 | +4791.6% | 35.3% | 5.37 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4606.8% | 35.5% | 4.65 |
| 2026-11-18 01:32 | rl-4-control | ppo3-0.10 | control | train | 2000-01-07 | 2025-11-09 | 0.98 | +4444.6% | 34.9% | 4.75 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s0 | control | train | 2000-01-07 | 2025-11-09 | 1.15 | +8007.7% | 32.9% | 10.94 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s1 | control | train | 2000-01-07 | 2025-11-09 | 1.14 | +8354.2% | 34.7% | 10.39 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s2 | control | train | 2000-01-07 | 2025-11-09 | 1.14 | +8419.9% | 32.8% | 10.17 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s3 | control | train | 2000-01-07 | 2025-11-09 | 1.15 | +9095.5% | 34.4% | 10.59 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s4 | control | train | 2000-01-07 | 2025-11-09 | 1.14 | +8232.9% | 32.9% | 10.84 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s5 | control | train | 2000-01-07 | 2025-11-09 | 1.11 | +7919.8% | 37.0% | 10.82 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s6 | control | train | 2000-01-07 | 2025-11-09 | 1.14 | +7883.1% | 34.5% | 10.70 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s7 | control | train | 2000-01-07 | 2025-11-09 | 1.17 | +9520.6% | 32.8% | 9.96 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s8 | control | train | 2000-01-07 | 2025-11-09 | 1.17 | +9480.0% | 32.8% | 10.67 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20-s9 | control | train | 2000-01-07 | 2025-11-09 | 1.15 | +8545.1% | 32.8% | 10.72 |
| 2026-11-18 01:33 | rl-4-control | ppo3-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.15 | +8561.1% | 33.6% | 10.51 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4388.3% | 41.5% | 3.08 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +4406.2% | 43.6% | 3.11 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +4376.5% | 43.4% | 3.08 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.93 | +4397.4% | 43.7% | 3.09 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4533.1% | 42.7% | 3.09 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4494.5% | 43.0% | 3.09 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4407.5% | 42.2% | 3.09 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4481.7% | 42.0% | 3.09 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4606.3% | 43.2% | 3.06 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4414.5% | 42.4% | 3.09 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.00 | control | train | 2000-01-07 | 2025-11-09 | 0.94 | +4464.0% | 42.8% | 3.09 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s0 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4876.8% | 42.4% | 8.31 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s1 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +4688.1% | 43.9% | 8.52 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s2 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +4791.0% | 43.7% | 8.21 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s3 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4979.4% | 43.8% | 8.24 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s4 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4825.8% | 42.9% | 8.23 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s5 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4901.6% | 42.7% | 8.32 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s6 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4872.8% | 42.5% | 8.22 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s7 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4884.1% | 42.4% | 8.29 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s8 | control | train | 2000-01-07 | 2025-11-09 | 0.95 | +4820.7% | 43.2% | 8.44 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05-s9 | control | train | 2000-01-07 | 2025-11-09 | 0.97 | +5042.3% | 42.5% | 8.37 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.05 | control | train | 2000-01-07 | 2025-11-09 | 0.96 | +4905.4% | 42.9% | 8.30 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s0 | control | train | 2000-01-07 | 2025-11-09 | 1.03 | +6316.6% | 41.9% | 13.11 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s1 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6423.5% | 42.4% | 13.16 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s2 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6383.9% | 41.7% | 13.08 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s3 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6434.9% | 41.7% | 12.98 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s4 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6431.6% | 42.3% | 13.14 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s5 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6601.7% | 41.9% | 13.10 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s6 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6412.3% | 42.3% | 13.01 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s7 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6461.0% | 41.8% | 13.14 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s8 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6430.5% | 41.7% | 13.04 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10-s9 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6391.9% | 41.9% | 13.02 |
| 2026-11-18 01:49 | rl-4-control | ppo3-warm-0.10 | control | train | 2000-01-07 | 2025-11-09 | 1.04 | +6409.1% | 42.0% | 13.08 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s0 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15855.4% | 37.3% | 16.86 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s1 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15919.2% | 37.9% | 16.88 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s2 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15742.1% | 37.9% | 16.86 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s3 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15838.5% | 37.7% | 16.85 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s4 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15839.3% | 38.1% | 16.88 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s5 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15938.5% | 37.5% | 16.85 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s6 | control | train | 2000-01-07 | 2025-11-09 | 1.29 | +15640.8% | 38.1% | 16.85 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s7 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15866.3% | 37.3% | 16.86 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s8 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15857.8% | 37.8% | 16.88 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20-s9 | control | train | 2000-01-07 | 2025-11-09 | 1.29 | +15737.8% | 37.9% | 16.86 |
| 2026-11-18 01:50 | rl-4-control | ppo3-warm-0.20 | control | train | 2000-01-07 | 2025-11-09 | 1.30 | +15834.8% | 37.7% | 16.87 |
| 2026-11-18 11:08 | rl-5-screen | funding | screen | train | 2021-02-19 | 2025-10-31 | 0.73 | +51.0% | 20.3% | 39.24 |
| 2026-11-18 11:08 | rl-5-screen | premium | screen | train | 2021-02-19 | 2025-10-31 | 0.49 | +32.9% | 23.9% | 38.04 |
| 2026-11-18 11:08 | rl-5-screen | mom_12_1 | screen | train | 2021-02-19 | 2025-10-31 | 0.10 | -0.3% | 23.3% | 14.93 |
| 2026-11-18 11:08 | rl-5-screen | vol | screen | train | 2021-02-19 | 2025-10-31 | -0.01 | -9.7% | 38.8% | 20.61 |
| 2026-11-18 11:08 | rl-5-screen | rev_1w | screen | train | 2021-02-19 | 2025-10-31 | -0.17 | -17.9% | 41.7% | 62.19 |
| 2026-11-18 11:08 | rl-5-screen | mom_1m | screen | train | 2021-02-19 | 2025-10-31 | -0.20 | -21.8% | 41.7% | 32.38 |
| 2026-11-18 11:08 | rl-5-screen | fund_30 | screen | train | 2021-02-19 | 2025-10-31 | 0.64 | +43.4% | 13.3% | 20.95 |
| 2026-11-18 11:08 | rl-5-screen | max_30 | screen | train | 2021-02-19 | 2025-10-31 | 0.18 | +8.2% | 35.8% | 24.65 |
| 2026-11-18 11:08 | rl-5-screen | log_qv | screen | train | 2021-02-19 | 2025-10-31 | 0.79 | +63.9% | 24.5% | 15.67 |
| 2026-11-18 11:05 | volume-1-screen | vol_chg4 (IC +0.011, chance 0.036, family 0.048, WF -0.010, gain -0.022) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:05 | volume-1-screen | vol_chg13 (IC -0.009, chance 0.034, family 0.048, WF +0.002, gain -0.006) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:05 | volume-1-screen | vol_z52 (IC +0.012, chance 0.037, family 0.048, WF +0.001, gain -0.007) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:05 | volume-1-screen | vw_trend13 (IC +0.003, chance 0.038, family 0.048, WF +0.012, gain +0.002) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:05 | volume-1-screen | updown13 (IC -0.003, chance 0.037, family 0.048, WF +0.001, gain -0.017) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:05 | volume-1-screen | pv_div13 (IC -0.021, chance 0.040, family 0.048, WF +0.017, gain +0.001) | screen | train | 2000-01-07 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:19 | volume-1-coins-screen | vol_chg4 (xs rank IC -0.020, t -2.3, chance 0.017, family 0.043, no) | screen | train | 2019-04-05 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:19 | volume-1-coins-screen | vol_chg13 (xs rank IC +0.003, t +0.2, chance 0.013, family 0.043, no) | screen | train | 2019-04-05 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:19 | volume-1-coins-screen | vol_z52 (xs rank IC -0.019, t -1.8, chance 0.016, family 0.043, no) | screen | train | 2019-04-05 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:19 | volume-1-coins-screen | vw_trend13 (xs rank IC -0.010, t -0.9, chance 0.034, family 0.043, no) | screen | train | 2019-04-05 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:19 | volume-1-coins-screen | updown13 (xs rank IC -0.019, t -1.7, chance 0.043, family 0.043, no) | screen | train | 2019-04-05 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:19 | volume-1-coins-screen | pv_div13 (xs rank IC +0.007, t +0.7, chance 0.024, family 0.043, no) | screen | train | 2019-04-05 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:07 | evo-1-smoke | toy noise seed 1, GP 200x15 (2274 rules; fit Sharpe 1.49; SPA p 0.002; no market data, Sharpe = best rule on unseen toy days) | control | - | - | - | 0.19 | - | - | - |
| 2026-11-18 11:07 | evo-1-smoke | toy noise seed 2, GP 200x15 (2257 rules; fit Sharpe 1.52; SPA p 0.004) | control | - | - | - | 0.39 | - | - | - |
| 2026-11-18 11:07 | evo-1-smoke | toy noise seed 3, GP 200x15 (2243 rules; fit Sharpe 1.36; SPA p 0.006) | control | - | - | - | -0.06 | - | - | - |
| 2026-11-18 11:07 | evo-1-smoke | toy plant k=0.05 seed 1, GP 200x15 (2101 rules; SPA p 0.090; H itself 1.33) | control | - | - | - | -0.19 | - | - | - |
| 2026-11-18 11:07 | evo-1-smoke | toy plant k=0.1 seed 1, GP 200x15 (2063 rules; SPA p 0.896; H itself 2.49) | control | - | - | - | -0.37 | - | - | - |
| 2026-11-18 11:07 | evo-1-smoke | toy plant k=0.2 seed 1, GP 200x15 (2053 rules; SPA p 0.000; H itself 4.74) | control | - | - | - | 1.16 | - | - | - |
| 2026-11-18 11:08 | evo-1-smoke | toy noise seed 1, 2000 random rules, no evolution (1983 rules; fit Sharpe 0.73; SPA p 0.552) | control | - | - | - | 0.12 | - | - | - |
| 2026-11-18 11:08 | evo-1-smoke | toy noise seed 2, 2000 random rules, no evolution (1986 rules; fit Sharpe 0.75; SPA p 0.476) | control | - | - | - | 0.04 | - | - | - |
| 2026-11-18 11:08 | evo-1-smoke | toy noise seed 3, 2000 random rules, no evolution (1972 rules; fit Sharpe 0.83; SPA p 0.232) | control | - | - | - | -0.07 | - | - | - |
| 2026-11-18 11:08 | evo-1-smoke | toy noise seed 1, GP 500x30 (10076 rules; fit Sharpe 1.88; SPA p 0.000) | control | - | - | - | -0.66 | - | - | - |
| 2026-11-18 11:08 | evo-1-smoke | toy plant k=0.1 seed 1, GP 500x30 (10274 rules; SPA p 0.000; H itself 2.49; weights corr to H 0.99) | control | - | - | - | 2.52 | - | - | - |
| 2026-11-18 11:08 | evo-1-smoke | toy plant k=0.2 seed 1, GP 500x30 (10013 rules; SPA p 0.000; H itself 4.74; weights corr to H 0.62) | control | - | - | - | 2.70 | - | - | - |
| 2026-11-18 19:05 | evo-1-control | shuffle 1 plant k=0.01: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.32 | +94.5% | 36.8% | 8.04 |
| 2026-11-18 19:05 | evo-1-control | shuffle 1 plant k=0.02: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.45 | +161.4% | 26.2% | 7.89 |
| 2026-11-18 19:05 | evo-1-control | shuffle 1 plant k=0.04: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.82 | +493.9% | 13.1% | 7.16 |
| 2026-11-18 19:06 | evo-1-control | shuffle 1: evo-top1, walk-forward 2000-2025 (629008 evaluations, 629008 formulas, 365727 behaviours; bootstrap p vs cash 0.418; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.04 | -13.2% | 51.6% | 18.44 |
| 2026-11-18 19:06 | evo-1-control | shuffle 1: evo-ens10, walk-forward 2000-2025 (629008 evaluations, 629008 formulas, 365727 behaviours; bootstrap p vs cash 0.491; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.01 | -14.2% | 58.1% | 14.73 |
| 2026-11-18 19:06 | evo-1-control | shuffle 1: evo-val, walk-forward 2000-2025 (629008 evaluations, 629008 formulas, 365727 behaviours; bootstrap p vs cash 0.197; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.18 | +44.5% | 51.8% | 10.16 |
| 2026-11-18 19:06 | evo-1-control | shuffle 1 plant k=0.04: evo-top1, walk-forward 2000-2025 (640606 evaluations, 640606 formulas, 357131 behaviours; bootstrap p vs cash 0.009; weights corr to H 0.47; ceiling 0.82; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.46 | +205.1% | 32.1% | 14.71 |
| 2026-11-18 19:06 | evo-1-control | shuffle 1 plant k=0.04: evo-ens10, walk-forward 2000-2025 (640606 evaluations, 640606 formulas, 357131 behaviours; bootstrap p vs cash 0.002; weights corr to H 0.56; ceiling 0.82; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.51 | +208.6% | 31.2% | 13.84 |
| 2026-11-18 19:06 | evo-1-control | shuffle 1 plant k=0.04: evo-val, walk-forward 2000-2025 (640606 evaluations, 640606 formulas, 357131 behaviours; bootstrap p vs cash 0.117; weights corr to H 0.35; ceiling 0.82; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.24 | +57.1% | 35.2% | 12.80 |
| 2026-11-18 19:07 | evo-1-control | shuffle 2: evo-top1, walk-forward 2000-2025 (595023 evaluations, 595023 formulas, 360638 behaviours; bootstrap p vs cash 0.636; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.07 | -83.7% | 95.6% | 32.03 |
| 2026-11-18 19:07 | evo-1-control | shuffle 2: evo-ens10, walk-forward 2000-2025 (595023 evaluations, 595023 formulas, 360638 behaviours; bootstrap p vs cash 0.240; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.12 | -1.1% | 66.4% | 20.95 |
| 2026-11-18 19:07 | evo-1-control | shuffle 2: evo-val, walk-forward 2000-2025 (595023 evaluations, 595023 formulas, 360638 behaviours; bootstrap p vs cash 0.476; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.01 | -80.6% | 88.8% | 22.37 |
| 2026-11-18 19:07 | evo-1-control | shuffle 3: evo-top1, walk-forward 2000-2025 (602432 evaluations, 602432 formulas, 333639 behaviours; bootstrap p vs cash 0.122; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.24 | +44.0% | 89.7% | 21.46 |
| 2026-11-18 19:07 | evo-1-control | shuffle 3: evo-ens10, walk-forward 2000-2025 (602432 evaluations, 602432 formulas, 333639 behaviours; bootstrap p vs cash 0.051; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.31 | +244.5% | 75.7% | 18.05 |
| 2026-11-18 19:07 | evo-1-control | shuffle 3: evo-val, walk-forward 2000-2025 (602432 evaluations, 602432 formulas, 333639 behaviours; bootstrap p vs cash 0.024; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.37 | +488.4% | 75.6% | 23.15 |
| 2026-11-18 19:07 | evo-1-control | shuffle 1 plant k=0.02: evo-top1, walk-forward 2000-2025 (625432 evaluations, 625432 formulas, 352931 behaviours; bootstrap p vs cash 0.074; weights corr to H 0.26; ceiling 0.45; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.26 | +47.8% | 31.0% | 9.28 |
| 2026-11-18 19:07 | evo-1-control | shuffle 1 plant k=0.02: evo-ens10, walk-forward 2000-2025 (625432 evaluations, 625432 formulas, 352931 behaviours; bootstrap p vs cash 0.099; weights corr to H 0.44; ceiling 0.45; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.23 | +37.7% | 35.3% | 9.92 |
| 2026-11-18 19:07 | evo-1-control | shuffle 1 plant k=0.02: evo-val, walk-forward 2000-2025 (625432 evaluations, 625432 formulas, 352931 behaviours; bootstrap p vs cash 0.018; weights corr to H 0.39; ceiling 0.45; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.42 | +149.6% | 38.0% | 13.14 |
| 2026-11-18 19:08 | evo-1-control | shuffle 1 plant k=0.01: evo-top1, walk-forward 2000-2025 (637867 evaluations, 637867 formulas, 371586 behaviours; bootstrap p vs cash 0.641; weights corr to H 0.19; ceiling 0.32; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.06 | -36.7% | 65.0% | 14.49 |
| 2026-11-18 19:08 | evo-1-control | shuffle 1 plant k=0.01: evo-ens10, walk-forward 2000-2025 (637867 evaluations, 637867 formulas, 371586 behaviours; bootstrap p vs cash 0.579; weights corr to H 0.32; ceiling 0.32; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.03 | -15.8% | 50.1% | 11.02 |
| 2026-11-18 19:08 | evo-1-control | shuffle 1 plant k=0.01: evo-val, walk-forward 2000-2025 (637867 evaluations, 637867 formulas, 371586 behaviours; bootstrap p vs cash 0.503; weights corr to H 0.25; ceiling 0.32; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.00 | -11.2% | 62.8% | 12.09 |
| 2026-11-18 19:08 | evo-1-control | shuffle 1: equal weight, no search (world context; p vs cash 0.057) | control | train | 2000-01-07 | 2025-11-09 | 0.32 | +173.2% | 64.5% | 1.52 |
| 2026-11-18 19:08 | evo-1-control | shuffle 1: tsmom12, no search (world context; p vs cash 0.262) | control | train | 2000-01-07 | 2025-11-09 | 0.13 | +24.2% | 62.1% | 3.88 |
| 2026-11-18 19:08 | evo-1-control | shuffle 2: equal weight, no search (world context; p vs cash 0.013) | control | train | 2000-01-07 | 2025-11-09 | 0.41 | +305.8% | 32.9% | 1.55 |
| 2026-11-18 19:08 | evo-1-control | shuffle 2: tsmom12, no search (world context; p vs cash 0.394) | control | train | 2000-01-07 | 2025-11-09 | 0.05 | -3.3% | 45.3% | 4.10 |
| 2026-11-18 19:08 | evo-1-control | shuffle 3: equal weight, no search (world context; p vs cash 0.007) | control | train | 2000-01-07 | 2025-11-09 | 0.47 | +423.7% | 45.1% | 1.66 |
| 2026-11-18 19:08 | evo-1-control | shuffle 3: tsmom12, no search (world context; p vs cash 0.008) | control | train | 2000-01-07 | 2025-11-09 | 0.46 | +261.5% | 42.4% | 3.51 |
| 2026-11-18 19:09 | evo-1-control | shuffle 1 plant k=0.01: equal weight, no search (world context; p vs cash 0.174) | control | train | 2000-01-07 | 2025-11-09 | 0.19 | +59.3% | 73.7% | 1.44 |
| 2026-11-18 19:09 | evo-1-control | shuffle 1 plant k=0.01: tsmom12, no search (world context; p vs cash 0.382) | control | train | 2000-01-07 | 2025-11-09 | 0.06 | +1.1% | 62.0% | 3.68 |
| 2026-11-18 19:09 | evo-1-control | shuffle 1 plant k=0.02: equal weight, no search (world context; p vs cash 0.399) | control | train | 2000-01-07 | 2025-11-09 | 0.06 | -11.3% | 80.8% | 1.36 |
| 2026-11-18 19:09 | evo-1-control | shuffle 1 plant k=0.02: tsmom12, no search (world context; p vs cash 0.377) | control | train | 2000-01-07 | 2025-11-09 | 0.06 | +1.9% | 63.4% | 3.42 |
| 2026-11-18 19:09 | evo-1-control | shuffle 1 plant k=0.04: equal weight, no search (world context; p vs cash 0.904) | control | train | 2000-01-07 | 2025-11-09 | -0.26 | -77.8% | 90.8% | 1.21 |
| 2026-11-18 19:09 | evo-1-control | shuffle 1 plant k=0.04: tsmom12, no search (world context; p vs cash 0.707) | control | train | 2000-01-07 | 2025-11-09 | -0.10 | -31.2% | 64.3% | 2.82 |
| 2026-11-18 19:14 | evo-1-control | shuffle 1 zero-mean plant k=0.01: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.08 | +8.5% | 48.9% | 7.52 |
| 2026-11-18 19:14 | evo-1-control | shuffle 1 zero-mean plant k=0.02: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.30 | +77.3% | 34.5% | 7.20 |
| 2026-11-18 19:14 | evo-1-control | shuffle 1 zero-mean plant k=0.04: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.72 | +325.1% | 19.2% | 6.49 |
| 2026-11-18 19:14 | evo-1-control | shuffle 1 zero-mean: equal weight, no search (world context; p vs cash 0.708) | control | train | 2000-01-07 | 2025-11-09 | -0.10 | -55.2% | 80.4% | 1.23 |
| 2026-11-18 19:14 | evo-1-control | shuffle 1 zero-mean: evo-top1, walk-forward 2000-2025 (636572 evaluations, 636572 formulas, 370285 behaviours; bootstrap p vs cash 0.929; vs equal weight -0.19, p 0.813; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.29 | -70.4% | 76.1% | 16.34 |
| 2026-11-18 19:14 | evo-1-control | shuffle 1 zero-mean: evo-ens10, walk-forward 2000-2025 (636572 evaluations, 636572 formulas, 370285 behaviours; bootstrap p vs cash 0.831; vs equal weight -0.09, p 0.669; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.19 | -37.6% | 47.7% | 11.29 |
| 2026-11-18 19:15 | evo-1-control | shuffle 1 zero-mean: evo-val, walk-forward 2000-2025 (636572 evaluations, 636572 formulas, 370285 behaviours; bootstrap p vs cash 0.132; vs equal weight +0.32, p 0.052; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.22 | +50.3% | 30.6% | 11.59 |
| 2026-11-18 19:15 | evo-1-control | shuffle 2 zero-mean: equal weight, no search (world context; p vs cash 0.505) | control | train | 2000-01-07 | 2025-11-09 | -0.01 | -30.9% | 56.0% | 1.31 |
| 2026-11-18 19:15 | evo-1-control | shuffle 2 zero-mean: evo-top1, walk-forward 2000-2025 (627612 evaluations, 627612 formulas, 388622 behaviours; bootstrap p vs cash 0.542; vs equal weight -0.03, p 0.542; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.03 | -75.9% | 94.1% | 33.18 |
| 2026-11-18 19:15 | evo-1-control | shuffle 2 zero-mean: evo-ens10, walk-forward 2000-2025 (627612 evaluations, 627612 formulas, 388622 behaviours; bootstrap p vs cash 0.632; vs equal weight -0.08, p 0.653; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.09 | -51.1% | 72.1% | 20.51 |
| 2026-11-18 19:15 | evo-1-control | shuffle 2 zero-mean: evo-val, walk-forward 2000-2025 (627612 evaluations, 627612 formulas, 388622 behaviours; bootstrap p vs cash 0.908; vs equal weight -0.26, p 0.896; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.26 | -84.0% | 88.7% | 26.91 |
| 2026-11-18 19:15 | evo-1-control | shuffle 3 zero-mean: equal weight, no search (world context; p vs cash 0.391) | control | train | 2000-01-07 | 2025-11-09 | 0.05 | -12.0% | 70.1% | 1.44 |
| 2026-11-18 19:15 | evo-1-control | shuffle 3 zero-mean: evo-top1, walk-forward 2000-2025 (620940 evaluations, 620940 formulas, 350194 behaviours; bootstrap p vs cash 0.968; vs equal weight -0.39, p 0.986; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.34 | -98.6% | 98.9% | 25.87 |
| 2026-11-18 19:15 | evo-1-control | shuffle 3 zero-mean: evo-ens10, walk-forward 2000-2025 (620940 evaluations, 620940 formulas, 350194 behaviours; bootstrap p vs cash 0.772; vs equal weight -0.19, p 0.890; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.14 | -87.9% | 94.9% | 20.05 |
| 2026-11-18 19:15 | evo-1-control | shuffle 3 zero-mean: evo-val, walk-forward 2000-2025 (620940 evaluations, 620940 formulas, 350194 behaviours; bootstrap p vs cash 0.880; vs equal weight -0.26, p 0.945; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.21 | -93.1% | 95.6% | 20.77 |
| 2026-11-18 19:15 | evo-1-control | shuffle 1 zero-mean plant k=0.04: equal weight, no search (world context; p vs cash 1.000) | control | train | 2000-01-07 | 2025-11-09 | -0.75 | -97.3% | 97.7% | 1.12 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.04: evo-top1, walk-forward 2000-2025 (640955 evaluations, 640955 formulas, 350250 behaviours; bootstrap p vs cash 0.317; vs equal weight +0.85, p 0.000; weights corr to H 0.32; ceiling 0.72; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.10 | +12.7% | 58.6% | 12.31 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.04: evo-ens10, walk-forward 2000-2025 (640955 evaluations, 640955 formulas, 350250 behaviours; bootstrap p vs cash 0.178; vs equal weight +0.94, p 0.000; weights corr to H 0.48; ceiling 0.72; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.19 | +31.6% | 40.3% | 9.93 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.04: evo-val, walk-forward 2000-2025 (640955 evaluations, 640955 formulas, 350250 behaviours; bootstrap p vs cash 0.073; vs equal weight +1.02, p 0.000; weights corr to H 0.39; ceiling 0.72; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.27 | +68.7% | 22.5% | 11.71 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.02: equal weight, no search (world context; p vs cash 0.981) | control | train | 2000-01-07 | 2025-11-09 | -0.41 | -88.4% | 91.7% | 1.14 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.02: evo-top1, walk-forward 2000-2025 (637756 evaluations, 637756 formulas, 352995 behaviours; bootstrap p vs cash 0.926; vs equal weight +0.14, p 0.273; weights corr to H 0.31; ceiling 0.30; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.28 | -52.3% | 66.5% | 9.40 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.02: evo-ens10, walk-forward 2000-2025 (637756 evaluations, 637756 formulas, 352995 behaviours; bootstrap p vs cash 0.653; vs equal weight +0.33, p 0.068; weights corr to H 0.47; ceiling 0.30; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.09 | -20.4% | 46.0% | 10.96 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.02: evo-val, walk-forward 2000-2025 (637756 evaluations, 637756 formulas, 352995 behaviours; bootstrap p vs cash 0.602; vs equal weight +0.36, p 0.068; weights corr to H 0.26; ceiling 0.30; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.05 | -26.5% | 47.2% | 12.05 |
| 2026-11-18 19:16 | evo-1-control | shuffle 1 zero-mean plant k=0.01: equal weight, no search (world context; p vs cash 0.899) | control | train | 2000-01-07 | 2025-11-09 | -0.24 | -75.7% | 86.0% | 1.20 |
| 2026-11-18 19:17 | evo-1-control | shuffle 1 zero-mean plant k=0.01: evo-top1, walk-forward 2000-2025 (644920 evaluations, 644920 formulas, 371664 behaviours; bootstrap p vs cash 0.448; vs equal weight +0.26, p 0.113; weights corr to H 0.27; ceiling 0.08; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.02 | -7.4% | 45.4% | 15.23 |
| 2026-11-18 19:17 | evo-1-control | shuffle 1 zero-mean plant k=0.01: evo-ens10, walk-forward 2000-2025 (644920 evaluations, 644920 formulas, 371664 behaviours; bootstrap p vs cash 0.697; vs equal weight +0.13, p 0.251; weights corr to H 0.37; ceiling 0.08; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.11 | -23.2% | 49.0% | 11.38 |
| 2026-11-18 19:17 | evo-1-control | shuffle 1 zero-mean plant k=0.01: evo-val, walk-forward 2000-2025 (644920 evaluations, 644920 formulas, 371664 behaviours; bootstrap p vs cash 0.510; vs equal weight +0.24, p 0.122; weights corr to H 0.25; ceiling 0.08; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.00 | -8.6% | 30.7% | 9.77 |
| 2026-11-18 19:22 | evo-1-control | shuffle 11 zero-mean plant k=0.04: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.22 | +42.7% | 32.8% | 6.82 |
| 2026-11-18 19:22 | evo-1-control | shuffle 11 zero-mean: equal weight, no search (world context; p vs cash 0.586) | control | train | 2000-01-07 | 2025-11-09 | -0.04 | -40.2% | 74.0% | 1.24 |
| 2026-11-18 19:23 | evo-1-control | shuffle 11 zero-mean [setting A: penalty 0.01, 30 generations]: evo-top1, walk-forward 2000-2025 (646146 evaluations, 646146 formulas, 403278 behaviours; bootstrap p vs cash 0.646; vs equal weight -0.04, p 0.573; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.08 | -29.3% | 48.0% | 23.99 |
| 2026-11-18 19:23 | evo-1-control | shuffle 11 zero-mean [setting A: penalty 0.01, 30 generations]: evo-ens10, walk-forward 2000-2025 (646146 evaluations, 646146 formulas, 403278 behaviours; bootstrap p vs cash 0.568; vs equal weight -0.00, p 0.498; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.04 | -13.7% | 37.1% | 19.56 |
| 2026-11-18 19:23 | evo-1-control | shuffle 11 zero-mean [setting A: penalty 0.01, 30 generations]: evo-val, walk-forward 2000-2025 (646146 evaluations, 646146 formulas, 403278 behaviours; bootstrap p vs cash 0.212; vs equal weight +0.19, p 0.183; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.16 | +34.8% | 48.2% | 21.01 |
| 2026-11-18 19:23 | evo-1-control | shuffle 12 zero-mean: equal weight, no search (world context; p vs cash 0.441) | control | train | 2000-01-07 | 2025-11-09 | 0.01 | -26.3% | 68.5% | 1.23 |
| 2026-11-18 19:23 | evo-1-control | shuffle 12 zero-mean [setting A: penalty 0.01, 30 generations]: evo-top1, walk-forward 2000-2025 (652911 evaluations, 652911 formulas, 382817 behaviours; bootstrap p vs cash 0.501; vs equal weight -0.02, p 0.545; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.00 | -32.2% | 64.7% | 17.58 |
| 2026-11-18 19:23 | evo-1-control | shuffle 12 zero-mean [setting A: penalty 0.01, 30 generations]: evo-ens10, walk-forward 2000-2025 (652911 evaluations, 652911 formulas, 382817 behaviours; bootstrap p vs cash 0.756; vs equal weight -0.15, p 0.786; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.14 | -52.5% | 72.6% | 17.64 |
| 2026-11-18 19:23 | evo-1-control | shuffle 12 zero-mean [setting A: penalty 0.01, 30 generations]: evo-val, walk-forward 2000-2025 (652911 evaluations, 652911 formulas, 382817 behaviours; bootstrap p vs cash 0.520; vs equal weight -0.02, p 0.558; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.01 | -30.7% | 57.3% | 22.63 |
| 2026-11-18 19:23 | evo-1-control | shuffle 13 zero-mean: equal weight, no search (world context; p vs cash 0.479) | control | train | 2000-01-07 | 2025-11-09 | 0.00 | -30.1% | 60.8% | 1.33 |
| 2026-11-18 19:23 | evo-1-control | shuffle 13 zero-mean [setting A: penalty 0.01, 30 generations]: evo-top1, walk-forward 2000-2025 (620348 evaluations, 620348 formulas, 365393 behaviours; bootstrap p vs cash 0.345; vs equal weight +0.07, p 0.370; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.07 | -21.2% | 74.5% | 24.66 |
| 2026-11-18 19:23 | evo-1-control | shuffle 13 zero-mean [setting A: penalty 0.01, 30 generations]: evo-ens10, walk-forward 2000-2025 (620348 evaluations, 620348 formulas, 365393 behaviours; bootstrap p vs cash 0.807; vs equal weight -0.17, p 0.854; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.16 | -69.0% | 82.9% | 18.24 |
| 2026-11-18 19:23 | evo-1-control | shuffle 13 zero-mean [setting A: penalty 0.01, 30 generations]: evo-val, walk-forward 2000-2025 (620348 evaluations, 620348 formulas, 365393 behaviours; bootstrap p vs cash 0.059; vs equal weight +0.33, p 0.066; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.33 | +301.9% | 58.6% | 24.54 |
| 2026-11-18 19:24 | evo-1-control | shuffle 11 zero-mean plant k=0.04: equal weight, no search (world context; p vs cash 1.000) | control | train | 2000-01-07 | 2025-11-09 | -0.72 | -96.7% | 97.2% | 1.11 |
| 2026-11-18 19:24 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting A: penalty 0.01, 30 generations]: evo-top1, walk-forward 2000-2025 (642779 evaluations, 642779 formulas, 357037 behaviours; bootstrap p vs cash 0.659; vs equal weight +0.63, p 0.004; weights corr to H 0.32; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.09 | -28.5% | 51.8% | 17.74 |
| 2026-11-18 19:24 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting A: penalty 0.01, 30 generations]: evo-ens10, walk-forward 2000-2025 (642779 evaluations, 642779 formulas, 357037 behaviours; bootstrap p vs cash 0.312; vs equal weight +0.81, p 0.000; weights corr to H 0.51; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.09 | +10.6% | 23.4% | 13.26 |
| 2026-11-18 19:24 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting A: penalty 0.01, 30 generations]: evo-val, walk-forward 2000-2025 (642779 evaluations, 642779 formulas, 357037 behaviours; bootstrap p vs cash 0.328; vs equal weight +0.81, p 0.001; weights corr to H 0.25; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.09 | +10.0% | 19.2% | 8.20 |
| 2026-11-18 19:24 | evo-1-control | shuffle 11 zero-mean [setting B: penalty 0.03, 30 generations]: evo-top1, walk-forward 2000-2025 (316445 evaluations, 316445 formulas, 187980 behaviours; bootstrap p vs cash 0.625; vs equal weight -0.03, p 0.545; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.07 | -20.8% | 36.1% | 17.22 |
| 2026-11-18 19:24 | evo-1-control | shuffle 11 zero-mean [setting B: penalty 0.03, 30 generations]: evo-ens10, walk-forward 2000-2025 (316445 evaluations, 316445 formulas, 187980 behaviours; bootstrap p vs cash 0.768; vs equal weight -0.11, p 0.716; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.14 | -24.7% | 35.5% | 13.19 |
| 2026-11-18 19:24 | evo-1-control | shuffle 11 zero-mean [setting B: penalty 0.03, 30 generations]: evo-val, walk-forward 2000-2025 (316445 evaluations, 316445 formulas, 187980 behaviours; bootstrap p vs cash 0.678; vs equal weight -0.06, p 0.604; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.10 | -10.9% | 29.7% | 7.35 |
| 2026-11-18 19:24 | evo-1-control | shuffle 12 zero-mean [setting B: penalty 0.03, 30 generations]: evo-top1, walk-forward 2000-2025 (400330 evaluations, 400330 formulas, 224859 behaviours; bootstrap p vs cash 0.805; vs equal weight -0.17, p 0.826; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.16 | -82.1% | 93.9% | 20.00 |
| 2026-11-18 19:24 | evo-1-control | shuffle 12 zero-mean [setting B: penalty 0.03, 30 generations]: evo-ens10, walk-forward 2000-2025 (400330 evaluations, 400330 formulas, 224859 behaviours; bootstrap p vs cash 0.918; vs equal weight -0.29, p 0.963; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.28 | -75.3% | 88.7% | 15.55 |
| 2026-11-18 19:24 | evo-1-control | shuffle 12 zero-mean [setting B: penalty 0.03, 30 generations]: evo-val, walk-forward 2000-2025 (400330 evaluations, 400330 formulas, 224859 behaviours; bootstrap p vs cash 0.902; vs equal weight -0.27, p 0.894; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.25 | -90.7% | 96.0% | 16.77 |
| 2026-11-18 19:25 | evo-1-control | shuffle 13 zero-mean [setting B: penalty 0.03, 30 generations]: evo-top1, walk-forward 2000-2025 (309514 evaluations, 309514 formulas, 172252 behaviours; bootstrap p vs cash 0.277; vs equal weight +0.09, p 0.309; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.10 | -5.6% | 74.9% | 19.43 |
| 2026-11-18 19:25 | evo-1-control | shuffle 13 zero-mean [setting B: penalty 0.03, 30 generations]: evo-ens10, walk-forward 2000-2025 (309514 evaluations, 309514 formulas, 172252 behaviours; bootstrap p vs cash 0.447; vs equal weight +0.02, p 0.458; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.02 | -24.2% | 66.5% | 15.50 |
| 2026-11-18 19:25 | evo-1-control | shuffle 13 zero-mean [setting B: penalty 0.03, 30 generations]: evo-val, walk-forward 2000-2025 (309514 evaluations, 309514 formulas, 172252 behaviours; bootstrap p vs cash 0.345; vs equal weight +0.07, p 0.348; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.08 | -26.4% | 91.2% | 12.10 |
| 2026-11-18 19:25 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting B: penalty 0.03, 30 generations]: evo-top1, walk-forward 2000-2025 (425950 evaluations, 425950 formulas, 244128 behaviours; bootstrap p vs cash 0.641; vs equal weight +0.65, p 0.001; weights corr to H 0.46; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.07 | -7.2% | 22.9% | 7.10 |
| 2026-11-18 19:25 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting B: penalty 0.03, 30 generations]: evo-ens10, walk-forward 2000-2025 (425950 evaluations, 425950 formulas, 244128 behaviours; bootstrap p vs cash 0.335; vs equal weight +0.80, p 0.000; weights corr to H 0.61; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.09 | +7.4% | 20.5% | 7.89 |
| 2026-11-18 19:25 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting B: penalty 0.03, 30 generations]: evo-val, walk-forward 2000-2025 (425950 evaluations, 425950 formulas, 244128 behaviours; bootstrap p vs cash 0.827; vs equal weight +0.54, p 0.011; weights corr to H 0.30; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.18 | -24.4% | 32.6% | 6.42 |
| 2026-11-18 19:25 | evo-1-control | shuffle 11 zero-mean [setting C: penalty 0.06, 30 generations]: evo-top1, walk-forward 2000-2025 (191568 evaluations, 191568 formulas, 123580 behaviours; bootstrap p vs cash 0.454; vs equal weight +0.06, p 0.402; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.02 | -1.4% | 25.6% | 11.76 |
| 2026-11-18 19:25 | evo-1-control | shuffle 11 zero-mean [setting C: penalty 0.06, 30 generations]: evo-ens10, walk-forward 2000-2025 (191568 evaluations, 191568 formulas, 123580 behaviours; bootstrap p vs cash 0.457; vs equal weight +0.05, p 0.372; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.01 | -1.1% | 20.8% | 7.93 |
| 2026-11-18 19:25 | evo-1-control | shuffle 11 zero-mean [setting C: penalty 0.06, 30 generations]: evo-val, walk-forward 2000-2025 (191568 evaluations, 191568 formulas, 123580 behaviours; bootstrap p vs cash 0.097; vs equal weight +0.28, p 0.106; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.25 | +66.5% | 20.7% | 7.97 |
| 2026-11-18 19:25 | evo-1-control | shuffle 12 zero-mean [setting C: penalty 0.06, 30 generations]: evo-top1, walk-forward 2000-2025 (221399 evaluations, 221399 formulas, 130636 behaviours; bootstrap p vs cash 0.894; vs equal weight -0.26, p 0.910; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.24 | -95.7% | 98.3% | 13.57 |
| 2026-11-18 19:25 | evo-1-control | shuffle 12 zero-mean [setting C: penalty 0.06, 30 generations]: evo-ens10, walk-forward 2000-2025 (221399 evaluations, 221399 formulas, 130636 behaviours; bootstrap p vs cash 0.791; vs equal weight -0.18, p 0.916; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.17 | -59.5% | 79.8% | 12.26 |
| 2026-11-18 19:25 | evo-1-control | shuffle 12 zero-mean [setting C: penalty 0.06, 30 generations]: evo-val, walk-forward 2000-2025 (221399 evaluations, 221399 formulas, 130636 behaviours; bootstrap p vs cash 0.963; vs equal weight -0.35, p 0.957; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.34 | -94.3% | 96.8% | 9.47 |
| 2026-11-18 19:26 | evo-1-control | shuffle 13 zero-mean [setting C: penalty 0.06, 30 generations]: evo-top1, walk-forward 2000-2025 (200679 evaluations, 200679 formulas, 124273 behaviours; bootstrap p vs cash 0.211; vs equal weight +0.14, p 0.200; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.15 | +13.9% | 70.9% | 17.69 |
| 2026-11-18 19:26 | evo-1-control | shuffle 13 zero-mean [setting C: penalty 0.06, 30 generations]: evo-ens10, walk-forward 2000-2025 (200679 evaluations, 200679 formulas, 124273 behaviours; bootstrap p vs cash 0.572; vs equal weight -0.05, p 0.638; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.05 | -46.8% | 71.0% | 11.49 |
| 2026-11-18 19:26 | evo-1-control | shuffle 13 zero-mean [setting C: penalty 0.06, 30 generations]: evo-val, walk-forward 2000-2025 (200679 evaluations, 200679 formulas, 124273 behaviours; bootstrap p vs cash 0.070; vs equal weight +0.29, p 0.072; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.29 | +178.5% | 72.0% | 12.17 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting C: penalty 0.06, 30 generations]: evo-top1, walk-forward 2000-2025 (290680 evaluations, 290680 formulas, 175316 behaviours; bootstrap p vs cash 0.486; vs equal weight +0.72, p 0.000; weights corr to H 0.52; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.01 | -1.2% | 22.4% | 6.92 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting C: penalty 0.06, 30 generations]: evo-ens10, walk-forward 2000-2025 (290680 evaluations, 290680 formulas, 175316 behaviours; bootstrap p vs cash 0.516; vs equal weight +0.71, p 0.000; weights corr to H 0.61; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.01 | -2.8% | 24.0% | 6.66 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting C: penalty 0.06, 30 generations]: evo-val, walk-forward 2000-2025 (290680 evaluations, 290680 formulas, 175316 behaviours; bootstrap p vs cash 0.737; vs equal weight +0.58, p 0.007; weights corr to H 0.29; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.14 | -22.7% | 40.8% | 7.89 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (148732 evaluations, 148732 formulas, 106058 behaviours; bootstrap p vs cash 0.359; vs equal weight +0.10, p 0.321; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.06 | +4.3% | 41.0% | 15.44 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (148732 evaluations, 148732 formulas, 106058 behaviours; bootstrap p vs cash 0.300; vs equal weight +0.13, p 0.220; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.09 | +9.7% | 23.6% | 9.41 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (148732 evaluations, 148732 formulas, 106058 behaviours; bootstrap p vs cash 0.833; vs equal weight -0.13, p 0.741; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.16 | -48.1% | 73.6% | 11.32 |
| 2026-11-18 19:26 | evo-1-control | shuffle 12 zero-mean [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (148327 evaluations, 148327 formulas, 104468 behaviours; bootstrap p vs cash 0.820; vs equal weight -0.19, p 0.824; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.18 | -64.4% | 79.6% | 16.71 |
| 2026-11-18 19:26 | evo-1-control | shuffle 12 zero-mean [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (148327 evaluations, 148327 formulas, 104468 behaviours; bootstrap p vs cash 0.962; vs equal weight -0.34, p 0.985; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.33 | -84.0% | 89.6% | 11.87 |
| 2026-11-18 19:26 | evo-1-control | shuffle 12 zero-mean [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (148327 evaluations, 148327 formulas, 104468 behaviours; bootstrap p vs cash 0.661; vs equal weight -0.10, p 0.688; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.09 | -60.9% | 82.8% | 17.02 |
| 2026-11-18 19:26 | evo-1-control | shuffle 13 zero-mean [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (141668 evaluations, 141668 formulas, 99394 behaviours; bootstrap p vs cash 0.549; vs equal weight -0.03, p 0.569; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.02 | -72.1% | 93.2% | 16.83 |
| 2026-11-18 19:26 | evo-1-control | shuffle 13 zero-mean [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (141668 evaluations, 141668 formulas, 99394 behaviours; bootstrap p vs cash 0.599; vs equal weight -0.06, p 0.681; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.06 | -48.6% | 69.8% | 12.58 |
| 2026-11-18 19:26 | evo-1-control | shuffle 13 zero-mean [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (141668 evaluations, 141668 formulas, 99394 behaviours; bootstrap p vs cash 0.284; vs equal weight +0.10, p 0.294; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.10 | -21.1% | 81.2% | 11.67 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (164953 evaluations, 164953 formulas, 120990 behaviours; bootstrap p vs cash 0.678; vs equal weight +0.63, p 0.002; weights corr to H 0.38; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.09 | -18.0% | 35.5% | 8.71 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (164953 evaluations, 164953 formulas, 120990 behaviours; bootstrap p vs cash 0.500; vs equal weight +0.71, p 0.000; weights corr to H 0.54; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.00 | -2.6% | 22.4% | 7.15 |
| 2026-11-18 19:26 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (164953 evaluations, 164953 formulas, 120990 behaviours; bootstrap p vs cash 0.178; vs equal weight +0.92, p 0.000; weights corr to H 0.36; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.20 | +45.4% | 45.5% | 8.21 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean [setting E: penalty 0.03, 10 generations]: evo-top1, walk-forward 2000-2025 (159920 evaluations, 159920 formulas, 105936 behaviours; bootstrap p vs cash 0.872; vs equal weight -0.20, p 0.821; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.23 | -42.1% | 48.3% | 17.09 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean [setting E: penalty 0.03, 10 generations]: evo-ens10, walk-forward 2000-2025 (159920 evaluations, 159920 formulas, 105936 behaviours; bootstrap p vs cash 0.510; vs equal weight +0.02, p 0.469; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.02 | -5.8% | 26.2% | 9.53 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean [setting E: penalty 0.03, 10 generations]: evo-val, walk-forward 2000-2025 (159920 evaluations, 159920 formulas, 105936 behaviours; bootstrap p vs cash 0.425; vs equal weight +0.07, p 0.362; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.03 | -1.7% | 45.6% | 10.50 |
| 2026-11-18 19:27 | evo-1-control | shuffle 12 zero-mean [setting E: penalty 0.03, 10 generations]: evo-top1, walk-forward 2000-2025 (171875 evaluations, 171875 formulas, 109689 behaviours; bootstrap p vs cash 0.807; vs equal weight -0.19, p 0.846; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.18 | -88.6% | 96.8% | 22.86 |
| 2026-11-18 19:27 | evo-1-control | shuffle 12 zero-mean [setting E: penalty 0.03, 10 generations]: evo-ens10, walk-forward 2000-2025 (171875 evaluations, 171875 formulas, 109689 behaviours; bootstrap p vs cash 0.745; vs equal weight -0.15, p 0.855; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.14 | -54.5% | 79.6% | 13.41 |
| 2026-11-18 19:27 | evo-1-control | shuffle 12 zero-mean [setting E: penalty 0.03, 10 generations]: evo-val, walk-forward 2000-2025 (171875 evaluations, 171875 formulas, 109689 behaviours; bootstrap p vs cash 0.926; vs equal weight -0.31, p 0.927; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.29 | -91.2% | 94.7% | 10.83 |
| 2026-11-18 19:27 | evo-1-control | shuffle 13 zero-mean [setting E: penalty 0.03, 10 generations]: evo-top1, walk-forward 2000-2025 (158721 evaluations, 158721 formulas, 100150 behaviours; bootstrap p vs cash 0.282; vs equal weight +0.10, p 0.298; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.10 | -23.5% | 82.2% | 16.07 |
| 2026-11-18 19:27 | evo-1-control | shuffle 13 zero-mean [setting E: penalty 0.03, 10 generations]: evo-ens10, walk-forward 2000-2025 (158721 evaluations, 158721 formulas, 100150 behaviours; bootstrap p vs cash 0.653; vs equal weight -0.09, p 0.740; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.09 | -58.4% | 76.7% | 13.21 |
| 2026-11-18 19:27 | evo-1-control | shuffle 13 zero-mean [setting E: penalty 0.03, 10 generations]: evo-val, walk-forward 2000-2025 (158721 evaluations, 158721 formulas, 100150 behaviours; bootstrap p vs cash 0.228; vs equal weight +0.14, p 0.227; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.15 | +20.9% | 75.4% | 14.81 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting E: penalty 0.03, 10 generations]: evo-top1, walk-forward 2000-2025 (228501 evaluations, 228501 formulas, 152471 behaviours; bootstrap p vs cash 0.671; vs equal weight +0.62, p 0.003; weights corr to H 0.42; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.10 | -12.7% | 25.1% | 7.46 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting E: penalty 0.03, 10 generations]: evo-ens10, walk-forward 2000-2025 (228501 evaluations, 228501 formulas, 152471 behaviours; bootstrap p vs cash 0.606; vs equal weight +0.66, p 0.000; weights corr to H 0.59; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.06 | -6.9% | 19.9% | 6.52 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting E: penalty 0.03, 10 generations]: evo-val, walk-forward 2000-2025 (228501 evaluations, 228501 formulas, 152471 behaviours; bootstrap p vs cash 0.286; vs equal weight +0.83, p 0.001; weights corr to H 0.35; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.11 | +13.0% | 21.2% | 5.86 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean [setting F: penalty 0.06, 10 generations]: evo-top1, walk-forward 2000-2025 (114052 evaluations, 114052 formulas, 77253 behaviours; bootstrap p vs cash 0.670; vs equal weight -0.06, p 0.609; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.10 | -26.2% | 43.9% | 14.62 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean [setting F: penalty 0.06, 10 generations]: evo-ens10, walk-forward 2000-2025 (114052 evaluations, 114052 formulas, 77253 behaviours; bootstrap p vs cash 0.579; vs equal weight -0.01, p 0.503; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.04 | -8.5% | 26.4% | 8.29 |
| 2026-11-18 19:27 | evo-1-control | shuffle 11 zero-mean [setting F: penalty 0.06, 10 generations]: evo-val, walk-forward 2000-2025 (114052 evaluations, 114052 formulas, 77253 behaviours; bootstrap p vs cash 0.567; vs equal weight +0.01, p 0.500; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.03 | -22.7% | 52.4% | 10.56 |
| 2026-11-18 19:27 | evo-1-control | shuffle 12 zero-mean [setting F: penalty 0.06, 10 generations]: evo-top1, walk-forward 2000-2025 (126018 evaluations, 126018 formulas, 80133 behaviours; bootstrap p vs cash 0.855; vs equal weight -0.22, p 0.865; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.20 | -93.4% | 97.5% | 13.64 |
| 2026-11-18 19:27 | evo-1-control | shuffle 12 zero-mean [setting F: penalty 0.06, 10 generations]: evo-ens10, walk-forward 2000-2025 (126018 evaluations, 126018 formulas, 80133 behaviours; bootstrap p vs cash 0.775; vs equal weight -0.17, p 0.902; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.16 | -59.1% | 76.3% | 10.99 |
| 2026-11-18 19:27 | evo-1-control | shuffle 12 zero-mean [setting F: penalty 0.06, 10 generations]: evo-val, walk-forward 2000-2025 (126018 evaluations, 126018 formulas, 80133 behaviours; bootstrap p vs cash 0.827; vs equal weight -0.20, p 0.837; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.19 | -86.6% | 93.4% | 12.02 |
| 2026-11-18 19:28 | evo-1-control | shuffle 13 zero-mean [setting F: penalty 0.06, 10 generations]: evo-top1, walk-forward 2000-2025 (118610 evaluations, 118610 formulas, 78158 behaviours; bootstrap p vs cash 0.490; vs equal weight +0.00, p 0.518; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.00 | -52.7% | 79.6% | 15.61 |
| 2026-11-18 19:28 | evo-1-control | shuffle 13 zero-mean [setting F: penalty 0.06, 10 generations]: evo-ens10, walk-forward 2000-2025 (118610 evaluations, 118610 formulas, 78158 behaviours; bootstrap p vs cash 0.517; vs equal weight -0.01, p 0.548; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.01 | -28.7% | 53.8% | 10.59 |
| 2026-11-18 19:28 | evo-1-control | shuffle 13 zero-mean [setting F: penalty 0.06, 10 generations]: evo-val, walk-forward 2000-2025 (118610 evaluations, 118610 formulas, 78158 behaviours; bootstrap p vs cash 0.079; vs equal weight +0.31, p 0.096; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.31 | +184.3% | 69.0% | 10.14 |
| 2026-11-18 19:28 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting F: penalty 0.06, 10 generations]: evo-top1, walk-forward 2000-2025 (176040 evaluations, 176040 formulas, 116035 behaviours; bootstrap p vs cash 0.275; vs equal weight +0.83, p 0.000; weights corr to H 0.58; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.11 | +10.7% | 17.8% | 5.84 |
| 2026-11-18 19:28 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting F: penalty 0.06, 10 generations]: evo-ens10, walk-forward 2000-2025 (176040 evaluations, 176040 formulas, 116035 behaviours; bootstrap p vs cash 0.584; vs equal weight +0.67, p 0.000; weights corr to H 0.59; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.04 | -6.3% | 25.0% | 6.40 |
| 2026-11-18 19:28 | evo-1-control | shuffle 11 zero-mean plant k=0.04 [setting F: penalty 0.06, 10 generations]: evo-val, walk-forward 2000-2025 (176040 evaluations, 176040 formulas, 116035 behaviours; bootstrap p vs cash 0.610; vs equal weight +0.66, p 0.001; weights corr to H 0.34; ceiling 0.22; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.06 | -16.2% | 32.9% | 8.89 |
| 2026-11-18 19:28 | evo-1-control | shuffle 21 zero-mean plant k=0.04: ceiling, H itself through the gym, no search | control | train | 2000-01-07 | 2025-11-09 | 0.24 | +51.6% | 31.6% | 6.63 |
| 2026-11-18 19:28 | evo-1-control | shuffle 21 zero-mean: equal weight, no search (world context; p vs cash 0.417) | control | train | 2000-01-07 | 2025-11-09 | 0.03 | -19.5% | 61.0% | 1.48 |
| 2026-11-18 19:28 | evo-1-control | shuffle 21 zero-mean [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (138468 evaluations, 138468 formulas, 98022 behaviours; bootstrap p vs cash 0.843; vs equal weight -0.23, p 0.868; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.19 | -79.9% | 84.4% | 15.78 |
| 2026-11-18 19:28 | evo-1-control | shuffle 21 zero-mean [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (138468 evaluations, 138468 formulas, 98022 behaviours; bootstrap p vs cash 0.694; vs equal weight -0.15, p 0.873; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.12 | -58.3% | 66.8% | 14.43 |
| 2026-11-18 19:28 | evo-1-control | shuffle 21 zero-mean [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (138468 evaluations, 138468 formulas, 98022 behaviours; bootstrap p vs cash 0.904; vs equal weight -0.27, p 0.908; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.24 | -88.7% | 92.5% | 18.03 |
| 2026-11-18 19:28 | evo-1-control | shuffle 22 zero-mean: equal weight, no search (world context; p vs cash 0.594) | control | train | 2000-01-07 | 2025-11-09 | -0.06 | -45.6% | 73.6% | 1.21 |
| 2026-11-18 19:28 | evo-1-control | shuffle 22 zero-mean [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (144939 evaluations, 144939 formulas, 102098 behaviours; bootstrap p vs cash 0.290; vs equal weight +0.14, p 0.236; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.09 | -0.1% | 47.9% | 21.29 |
| 2026-11-18 19:28 | evo-1-control | shuffle 22 zero-mean [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (144939 evaluations, 144939 formulas, 102098 behaviours; bootstrap p vs cash 0.210; vs equal weight +0.20, p 0.072; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.14 | +26.8% | 29.1% | 11.60 |
| 2026-11-18 19:28 | evo-1-control | shuffle 22 zero-mean [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (144939 evaluations, 144939 formulas, 102098 behaviours; bootstrap p vs cash 0.611; vs equal weight -0.00, p 0.496; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.06 | -47.6% | 78.0% | 14.89 |
| 2026-11-18 19:28 | evo-1-control | shuffle 23 zero-mean: equal weight, no search (world context; p vs cash 0.470) | control | train | 2000-01-07 | 2025-11-09 | 0.02 | -24.8% | 70.3% | 1.28 |
| 2026-11-18 19:29 | evo-1-control | shuffle 23 zero-mean [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (138633 evaluations, 138633 formulas, 97315 behaviours; bootstrap p vs cash 0.987; vs equal weight -0.45, p 0.982; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.44 | -89.0% | 90.1% | 16.08 |
| 2026-11-18 19:29 | evo-1-control | shuffle 23 zero-mean [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (138633 evaluations, 138633 formulas, 97315 behaviours; bootstrap p vs cash 0.709; vs equal weight -0.11, p 0.769; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.09 | -45.7% | 64.6% | 14.12 |
| 2026-11-18 19:29 | evo-1-control | shuffle 23 zero-mean [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (138633 evaluations, 138633 formulas, 97315 behaviours; bootstrap p vs cash 0.881; vs equal weight -0.21, p 0.847; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.19 | -78.3% | 84.0% | 17.10 |
| 2026-11-18 19:29 | evo-1-control | shuffle 21 zero-mean plant k=0.04: equal weight, no search (world context; p vs cash 0.997) | control | train | 2000-01-07 | 2025-11-09 | -0.56 | -93.8% | 95.2% | 1.26 |
| 2026-11-18 19:29 | evo-1-control | shuffle 21 zero-mean plant k=0.04 [setting D: penalty 0.01, 5 generations]: evo-top1, walk-forward 2000-2025 (163850 evaluations, 163850 formulas, 120164 behaviours; bootstrap p vs cash 0.684; vs equal weight +0.46, p 0.024; weights corr to H 0.35; ceiling 0.24; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.10 | -20.2% | 41.2% | 7.77 |
| 2026-11-18 19:29 | evo-1-control | shuffle 21 zero-mean plant k=0.04 [setting D: penalty 0.01, 5 generations]: evo-ens10, walk-forward 2000-2025 (163850 evaluations, 163850 formulas, 120164 behaviours; bootstrap p vs cash 0.715; vs equal weight +0.45, p 0.006; weights corr to H 0.56; ceiling 0.24; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.11 | -20.4% | 40.2% | 7.83 |
| 2026-11-18 19:29 | evo-1-control | shuffle 21 zero-mean plant k=0.04 [setting D: penalty 0.01, 5 generations]: evo-val, walk-forward 2000-2025 (163850 evaluations, 163850 formulas, 120164 behaviours; bootstrap p vs cash 0.288; vs equal weight +0.66, p 0.001; weights corr to H 0.27; ceiling 0.24; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.11 | +13.7% | 28.2% | 9.05 |
| 2026-11-18 19:40 | evo-2-control | shuffle 34 zero-mean plant k=0.0378906: ceiling, H itself through the gym, no search (k calibrated to a fast-scorer ceiling of 0.8: fast 0.790) | control | train | 2000-01-07 | 2025-11-09 | 0.78 | +382.3% | 20.8% | 6.95 |
| 2026-11-18 19:40 | evo-2-control | shuffle 34 zero-mean plant k=0.0175: ceiling, H itself through the gym, no search (k calibrated to a fast-scorer ceiling of 0.5: fast 0.494) | control | train | 2000-01-07 | 2025-11-09 | 0.49 | +168.9% | 16.9% | 7.99 |
| 2026-11-18 19:41 | evo-2-control | shuffle 35 zero-mean plant k=0.05875: ceiling, H itself through the gym, no search (k calibrated to a fast-scorer ceiling of 0.8: fast 0.800) | control | train | 2000-01-07 | 2025-11-09 | 0.80 | +403.0% | 21.7% | 6.15 |
| 2026-11-18 19:41 | evo-2-control | shuffle 35 zero-mean plant k=0.03: ceiling, H itself through the gym, no search (k calibrated to a fast-scorer ceiling of 0.5: fast 0.502) | control | train | 2000-01-07 | 2025-11-09 | 0.49 | +178.0% | 25.0% | 7.14 |
| 2026-11-18 19:41 | evo-2-control | shuffle 36 zero-mean plant k=0.0725: ceiling, H itself through the gym, no search (k calibrated to a fast-scorer ceiling of 0.8: fast 0.797) | control | train | 2000-01-07 | 2025-11-09 | 0.80 | +325.8% | 16.3% | 5.78 |
| 2026-11-18 19:41 | evo-2-control | shuffle 36 zero-mean plant k=0.0425: ceiling, H itself through the gym, no search (k calibrated to a fast-scorer ceiling of 0.5: fast 0.503) | control | train | 2000-01-07 | 2025-11-09 | 0.50 | +157.1% | 22.8% | 6.79 |
| 2026-11-18 19:42 | evo-2-control | shuffle 31 zero-mean: equal weight, no search (world context; p vs cash 0.514) | control | train | 2000-01-07 | 2025-11-09 | -0.01 | -32.7% | 59.0% | 1.37 |
| 2026-11-18 19:42 | evo-2-control | shuffle 31 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (224492 evaluations, 224492 formulas, 124271 behaviours; bootstrap p vs cash 0.705; vs equal weight -0.10, p 0.675; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.11 | -69.0% | 86.6% | 24.55 |
| 2026-11-18 19:42 | evo-2-control | shuffle 31 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (224492 evaluations, 224492 formulas, 124271 behaviours; bootstrap p vs cash 0.734; vs equal weight -0.14, p 0.749; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.15 | -50.3% | 68.3% | 18.22 |
| 2026-11-18 19:42 | evo-2-control | shuffle 31 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (224492 evaluations, 224492 formulas, 124271 behaviours; bootstrap p vs cash 0.824; vs equal weight -0.20, p 0.800; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.21 | -85.4% | 95.3% | 18.08 |
| 2026-11-18 19:42 | evo-2-control | shuffle 32 zero-mean: equal weight, no search (world context; p vs cash 0.680) | control | train | 2000-01-07 | 2025-11-09 | -0.10 | -54.7% | 69.4% | 1.31 |
| 2026-11-18 19:42 | evo-2-control | shuffle 32 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (203930 evaluations, 203930 formulas, 107452 behaviours; bootstrap p vs cash 0.922; vs equal weight -0.16, p 0.765; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.26 | -53.9% | 65.5% | 7.20 |
| 2026-11-18 19:42 | evo-2-control | shuffle 32 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (203930 evaluations, 203930 formulas, 107452 behaviours; bootstrap p vs cash 0.937; vs equal weight -0.17, p 0.821; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.26 | -39.2% | 46.7% | 7.21 |
| 2026-11-18 19:42 | evo-2-control | shuffle 32 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (203930 evaluations, 203930 formulas, 107452 behaviours; bootstrap p vs cash 0.975; vs equal weight -0.27, p 0.910; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.37 | -63.5% | 64.4% | 9.61 |
| 2026-11-18 19:42 | evo-2-control | shuffle 33 zero-mean: equal weight, no search (world context; p vs cash 0.629) | control | train | 2000-01-07 | 2025-11-09 | -0.06 | -46.3% | 57.3% | 1.33 |
| 2026-11-18 19:42 | evo-2-control | shuffle 33 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (223651 evaluations, 223651 formulas, 118191 behaviours; bootstrap p vs cash 0.269; vs equal weight +0.17, p 0.196; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.11 | -10.0% | 60.4% | 14.89 |
| 2026-11-18 19:42 | evo-2-control | shuffle 33 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (223651 evaluations, 223651 formulas, 118191 behaviours; bootstrap p vs cash 0.402; vs equal weight +0.11, p 0.257; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.05 | -15.1% | 50.1% | 14.67 |
| 2026-11-18 19:42 | evo-2-control | shuffle 33 zero-mean [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (223651 evaluations, 223651 formulas, 118191 behaviours; bootstrap p vs cash 0.308; vs equal weight +0.17, p 0.229; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.10 | -26.4% | 84.7% | 19.76 |
| 2026-11-18 19:43 | evo-2-control | shuffle 34 zero-mean plant k=0.0378906: equal weight, no search (world context; p vs cash 0.986) | control | train | 2000-01-07 | 2025-11-09 | -0.48 | -91.4% | 95.9% | 1.07 |
| 2026-11-18 19:43 | evo-2-control | shuffle 34 zero-mean plant k=0.0378906 [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (239093 evaluations, 239093 formulas, 127536 behaviours; bootstrap p vs cash 0.632; vs equal weight +0.42, p 0.030; weights corr to H 0.47; ceiling 0.78; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.07 | -56.0% | 85.9% | 10.62 |
| 2026-11-18 19:43 | evo-2-control | shuffle 34 zero-mean plant k=0.0378906 [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (239093 evaluations, 239093 formulas, 127536 behaviours; bootstrap p vs cash 0.064; vs equal weight +0.77, p 0.000; weights corr to H 0.65; ceiling 0.78; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.29 | +112.7% | 39.7% | 11.26 |
| 2026-11-18 19:43 | evo-2-control | shuffle 34 zero-mean plant k=0.0378906 [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (239093 evaluations, 239093 formulas, 127536 behaviours; bootstrap p vs cash 0.021; vs equal weight +0.87, p 0.000; weights corr to H 0.45; ceiling 0.78; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.39 | +282.5% | 48.7% | 12.51 |
| 2026-11-18 19:43 | evo-2-control | shuffle 35 zero-mean plant k=0.05875: equal weight, no search (world context; p vs cash 1.000) | control | train | 2000-01-07 | 2025-11-09 | -0.84 | -98.1% | 98.2% | 1.20 |
| 2026-11-18 19:43 | evo-2-control | shuffle 35 zero-mean plant k=0.05875 [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (242287 evaluations, 242287 formulas, 127882 behaviours; bootstrap p vs cash 0.039; vs equal weight +1.20, p 0.000; weights corr to H 0.49; ceiling 0.80; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.37 | +312.6% | 62.6% | 24.67 |
| 2026-11-18 19:43 | evo-2-control | shuffle 35 zero-mean plant k=0.05875 [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (242287 evaluations, 242287 formulas, 127882 behaviours; bootstrap p vs cash 0.079; vs equal weight +1.11, p 0.000; weights corr to H 0.60; ceiling 0.80; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.28 | +134.5% | 59.2% | 17.73 |
| 2026-11-18 19:43 | evo-2-control | shuffle 35 zero-mean plant k=0.05875 [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (242287 evaluations, 242287 formulas, 127882 behaviours; bootstrap p vs cash 0.203; vs equal weight +1.00, p 0.000; weights corr to H 0.45; ceiling 0.80; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.17 | +29.7% | 89.3% | 21.82 |
| 2026-11-18 19:43 | evo-2-control | shuffle 36 zero-mean plant k=0.0725: equal weight, no search (world context; p vs cash 1.000) | control | train | 2000-01-07 | 2025-11-09 | -1.26 | -99.7% | 99.7% | 1.24 |
| 2026-11-18 19:43 | evo-2-control | shuffle 36 zero-mean plant k=0.0725 [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (242249 evaluations, 242249 formulas, 131495 behaviours; bootstrap p vs cash 0.002; vs equal weight +1.95, p 0.000; weights corr to H 0.51; ceiling 0.80; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.69 | +826.7% | 43.4% | 10.53 |
| 2026-11-18 19:43 | evo-2-control | shuffle 36 zero-mean plant k=0.0725 [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (242249 evaluations, 242249 formulas, 131495 behaviours; bootstrap p vs cash 0.000; vs equal weight +2.07, p 0.000; weights corr to H 0.76; ceiling 0.80; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.81 | +936.3% | 32.2% | 13.54 |
| 2026-11-18 19:43 | evo-2-control | shuffle 36 zero-mean plant k=0.0725 [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (242249 evaluations, 242249 formulas, 131495 behaviours; bootstrap p vs cash 0.059; vs equal weight +1.59, p 0.000; weights corr to H 0.50; ceiling 0.80; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.33 | +185.0% | 46.7% | 12.83 |
| 2026-11-18 19:43 | evo-2-control | shuffle 34 zero-mean plant k=0.0175 [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (231766 evaluations, 231766 formulas, 122279 behaviours; bootstrap p vs cash 0.056; vs equal weight +0.47, p 0.024; weights corr to H 0.27; ceiling 0.49; FOUND) | control | train | 2000-01-07 | 2025-11-09 | 0.32 | +171.4% | 50.5% | 12.37 |
| 2026-11-18 19:43 | evo-2-control | shuffle 34 zero-mean plant k=0.0175 [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (231766 evaluations, 231766 formulas, 122279 behaviours; bootstrap p vs cash 0.653; vs equal weight +0.08, p 0.347; weights corr to H 0.37; ceiling 0.49; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.08 | -57.9% | 81.7% | 12.42 |
| 2026-11-18 19:43 | evo-2-control | shuffle 34 zero-mean plant k=0.0175 [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (231766 evaluations, 231766 formulas, 122279 behaviours; bootstrap p vs cash 0.977; vs equal weight -0.26, p 0.887; weights corr to H 0.26; ceiling 0.49; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.42 | -86.8% | 92.1% | 10.87 |
| 2026-11-18 19:43 | evo-2-control | shuffle 35 zero-mean plant k=0.03 [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (238447 evaluations, 238447 formulas, 129403 behaviours; bootstrap p vs cash 0.101; vs equal weight +0.57, p 0.004; weights corr to H 0.24; ceiling 0.49; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.24 | +105.9% | 73.2% | 23.12 |
| 2026-11-18 19:43 | evo-2-control | shuffle 35 zero-mean plant k=0.03 [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (238447 evaluations, 238447 formulas, 129403 behaviours; bootstrap p vs cash 0.340; vs equal weight +0.42, p 0.009; weights corr to H 0.35; ceiling 0.49; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.09 | -10.1% | 76.8% | 19.43 |
| 2026-11-18 19:43 | evo-2-control | shuffle 35 zero-mean plant k=0.03 [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (238447 evaluations, 238447 formulas, 129403 behaviours; bootstrap p vs cash 0.581; vs equal weight +0.28, p 0.102; weights corr to H 0.18; ceiling 0.49; not found) | control | train | 2000-01-07 | 2025-11-09 | -0.05 | -55.6% | 70.0% | 19.24 |
| 2026-11-18 19:43 | evo-2-control | shuffle 36 zero-mean plant k=0.0425 [setting evo-2: penalty 0.02, 10 generations]: evo-top1, walk-forward 2000-2025 (229792 evaluations, 229792 formulas, 124853 behaviours; bootstrap p vs cash 0.127; vs equal weight +0.90, p 0.000; weights corr to H 0.36; ceiling 0.50; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.23 | +56.3% | 35.1% | 12.32 |
| 2026-11-18 19:43 | evo-2-control | shuffle 36 zero-mean plant k=0.0425 [setting evo-2: penalty 0.02, 10 generations]: evo-ens10, walk-forward 2000-2025 (229792 evaluations, 229792 formulas, 124853 behaviours; bootstrap p vs cash 0.277; vs equal weight +0.79, p 0.000; weights corr to H 0.51; ceiling 0.50; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.12 | +19.7% | 39.0% | 11.16 |
| 2026-11-18 19:43 | evo-2-control | shuffle 36 zero-mean plant k=0.0425 [setting evo-2: penalty 0.02, 10 generations]: evo-val, walk-forward 2000-2025 (229792 evaluations, 229792 formulas, 124853 behaviours; bootstrap p vs cash 0.460; vs equal weight +0.69, p 0.002; weights corr to H 0.40; ceiling 0.50; not found) | control | train | 2000-01-07 | 2025-11-09 | 0.02 | -19.3% | 43.3% | 15.09 |
| 2026-11-18 11:12 | micro-1-screen | rv_chg (IC -0.004, chance 0.048, family 0.064, WF -0.023, gain -0.036) | screen | train | 2016-01-08 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:12 | micro-1-screen | rv_z52 (IC -0.000, chance 0.048, family 0.064, WF -0.002, gain -0.009) | screen | train | 2016-01-29 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:12 | micro-1-screen | jump4 (IC +0.002, chance 0.052, family 0.064, WF -0.005, gain -0.010) | screen | train | 2016-01-08 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:12 | micro-1-screen | sjump4 (IC -0.018, chance 0.043, family 0.064, WF -0.001, gain -0.004) | screen | train | 2016-01-08 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:12 | micro-1-screen | overnight13 (IC +0.030, chance 0.049, family 0.064, WF +0.007, gain -0.009) | screen | train | 2016-01-08 | 2025-11-09 | - | - | - | - |
| 2026-11-18 11:12 | micro-1-screen | intraday13 (IC +0.012, chance 0.057, family 0.064, WF +0.048, gain +0.021) | screen | train | 2016-01-08 | 2025-11-09 | - | - | - | - |
| 2026-11-18 18:52 | reentry | now@^GSPC sample A 10y (R vs now; share>1 0.00, mean 1.000, 1 episodes) | baseline | train | 1928-01 | 2016-10 | n/a | +0.0% | +0.0% | n/a |
| 2026-11-18 18:52 | reentry | dca12@^GSPC sample A 10y (R vs now; share>1 0.33, mean 0.983, 1 episodes) | variant | train | 1928-01 | 2016-10 | n/a | -3.4% | -13.0% | n/a |
| 2026-11-18 18:52 | reentry | dd20@^GSPC sample A 10y (R vs now; share>1 0.30, mean 0.941, 1 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.0% | -43.5% | n/a |
| 2026-11-18 18:52 | reentry | dd30@^GSPC sample A 10y (R vs now; share>1 0.29, mean 0.888, 1 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.0% | -66.7% | n/a |
| 2026-11-18 18:52 | reentry | dd20-sma10@^GSPC sample A 10y (R vs now; share>1 0.33, mean 0.987, 1 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.0% | -48.1% | n/a |
| 2026-11-18 18:52 | reentry | cape-median@^GSPC sample A 10y (R vs now; share>1 0.28, mean 0.906, 1 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.0% | -66.1% | n/a |
| 2026-11-18 18:52 | reentry | staged-24@^GSPC sample A 10y (R vs now; share>1 0.25, mean 0.963, 1 episodes) | variant | train | 1928-01 | 2016-10 | n/a | -1.0% | -26.4% | n/a |
| 2026-11-18 18:52 | reentry | dd30-24@^GSPC sample A 10y (R vs now; share>1 0.23, mean 0.962, 1 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.0% | -27.7% | n/a |
| 2026-11-18 18:52 | reentry | now@^GSPC sample B 10y (R vs now; share>1 0.00, mean 1.000, 8 episodes) | baseline | train | 1928-01 | 2016-10 | n/a | +0.0% | +0.0% | n/a |
| 2026-11-18 18:52 | reentry | dca12@^GSPC sample B 10y (R vs now; share>1 0.31, mean 0.988, 8 episodes) | variant | train | 1928-01 | 2016-10 | n/a | -2.8% | -10.1% | n/a |
| 2026-11-18 18:52 | reentry | dd20@^GSPC sample B 10y (R vs now; share>1 0.43, mean 0.938, 8 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.0% | -48.0% | n/a |
| 2026-11-18 18:52 | reentry | dd30@^GSPC sample B 10y (R vs now; share>1 0.51, mean 0.953, 8 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.9% | -65.3% | n/a |
| 2026-11-18 18:52 | reentry | dd20-sma10@^GSPC sample B 10y (R vs now; share>1 0.43, mean 1.008, 8 episodes) | variant | train | 1928-01 | 2016-10 | n/a | +0.0% | -48.6% | n/a |
| 2026-11-18 18:52 | reentry | cape-median@^GSPC sample B 10y (R vs now; share>1 0.48, mean 0.923, 8 episodes) | variant | train | 1928-01 | 2016-10 | n/a | -3.9% | -65.3% | n/a |
| 2026-11-18 18:52 | reentry | staged-24@^GSPC sample B 10y (R vs now; share>1 0.35, mean 0.967, 8 episodes) | variant | train | 1928-01 | 2016-10 | n/a | -7.6% | -27.8% | n/a |
| 2026-11-18 18:52 | reentry | dd30-24@^GSPC sample B 10y (R vs now; share>1 0.31, mean 0.968, 8 episodes) | variant | train | 1928-01 | 2016-10 | n/a | -9.2% | -27.8% | n/a |
| 2026-11-18 18:52 | reentry | now@^IXIC sample A 10y (R vs now; share>1 0.00, mean 1.000, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | +0.0% | +0.0% | n/a |
| 2026-11-18 18:52 | reentry | dca12@^IXIC sample A 10y (R vs now; share>1 0.35, mean 0.990, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | -4.5% | -14.3% | n/a |
| 2026-11-18 18:52 | reentry | dd20@^IXIC sample A 10y (R vs now; share>1 0.26, mean 0.946, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | +0.0% | -40.1% | n/a |
| 2026-11-18 18:52 | reentry | dd30@^IXIC sample A 10y (R vs now; share>1 0.26, mean 0.870, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | +0.0% | -69.9% | n/a |
| 2026-11-18 18:52 | reentry | dd20-sma10@^IXIC sample A 10y (R vs now; share>1 0.28, mean 0.909, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | +0.0% | -48.3% | n/a |
| 2026-11-18 18:52 | reentry | cape-median@^IXIC sample A 10y (R vs now; share>1 0.31, mean 0.886, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | -9.0% | -75.2% | n/a |
| 2026-11-18 18:52 | reentry | staged-24@^IXIC sample A 10y (R vs now; share>1 0.21, mean 0.949, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | +0.0% | -27.6% | n/a |
| 2026-11-18 18:52 | reentry | dd30-24@^IXIC sample A 10y (R vs now; share>1 0.20, mean 0.956, 1 episodes) | robustness | train | 1981-02 | 2016-10 | n/a | +0.0% | -31.5% | n/a |
| 2026-11-18 18:52 | reentry | now@^IXIC sample B 10y (R vs now; share>1 0.00, mean 1.000, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | +0.0% | +0.0% | n/a |
| 2026-11-18 18:52 | reentry | dca12@^IXIC sample B 10y (R vs now; share>1 0.35, mean 0.993, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | -4.1% | -14.1% | n/a |
| 2026-11-18 18:52 | reentry | dd20@^IXIC sample B 10y (R vs now; share>1 0.08, mean 0.859, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | +0.0% | -41.1% | n/a |
| 2026-11-18 18:52 | reentry | dd30@^IXIC sample B 10y (R vs now; share>1 0.04, mean 0.700, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | -31.0% | -70.9% | n/a |
| 2026-11-18 18:52 | reentry | dd20-sma10@^IXIC sample B 10y (R vs now; share>1 0.13, mean 0.831, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | -9.4% | -49.4% | n/a |
| 2026-11-18 18:52 | reentry | cape-median@^IXIC sample B 10y (R vs now; share>1 0.45, mean 1.021, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | -11.3% | -72.0% | n/a |
| 2026-11-18 18:52 | reentry | staged-24@^IXIC sample B 10y (R vs now; share>1 0.05, mean 0.889, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | -10.9% | -31.5% | n/a |
| 2026-11-18 18:52 | reentry | dd30-24@^IXIC sample B 10y (R vs now; share>1 0.04, mean 0.867, 3 episodes) | robustness | train | 1991-12 | 2016-10 | n/a | -11.0% | -35.7% | n/a |
| 2026-11-18 18:52 | exit-window | now@GSPC (mean R-1 all starts; MaxDD col = worst R) | baseline | train | 1929-01-03 | 2025-09-30 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:52 | exit-window | fallback@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.66% | 42.7% | n/a |
| 2026-11-18 18:52 | exit-window | staged5@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.30% | 21.9% | n/a |
| 2026-11-18 18:52 | exit-window | staged-half@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.33% | 21.3% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma200@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.54% | 28.4% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma50@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.33% | 20.5% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail5@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.60% | 26.3% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail8@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.65% | 29.6% | n/a |
| 2026-11-18 18:52 | exit-window | trig-vix@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1990-03-13 | 2025-09-30 | n/a | +0.57% | 19.8% | n/a |
| 2026-11-18 18:52 | exit-window | limit3@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.18% | 42.7% | n/a |
| 2026-11-18 18:52 | exit-window | limit5@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.40% | 42.7% | n/a |
| 2026-11-18 18:52 | exit-window | bracket@GSPC (mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.17% | 26.3% | n/a |
| 2026-11-18 18:52 | exit-window | now@IXIC (mean R-1 all starts; MaxDD col = worst R) | baseline | train | 1972-02-03 | 2025-09-30 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:52 | exit-window | fallback@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +1.05% | 34.0% | n/a |
| 2026-11-18 18:52 | exit-window | staged5@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.47% | 22.0% | n/a |
| 2026-11-18 18:52 | exit-window | staged-half@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.53% | 17.0% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma200@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.85% | 28.7% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma50@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.75% | 12.3% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail5@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.97% | 22.4% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail8@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +1.08% | 25.5% | n/a |
| 2026-11-18 18:52 | exit-window | trig-vix@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1990-03-13 | 2025-09-30 | n/a | +0.90% | 28.7% | n/a |
| 2026-11-18 18:52 | exit-window | limit3@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.19% | 34.0% | n/a |
| 2026-11-18 18:52 | exit-window | limit5@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.55% | 34.0% | n/a |
| 2026-11-18 18:52 | exit-window | bracket@IXIC (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.17% | 22.4% | n/a |
| 2026-11-18 18:52 | exit-window | now@OSEBX (mean R-1 all starts; MaxDD col = worst R) | baseline | train | 2014-03-17 | 2025-09-29 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:52 | exit-window | fallback@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.94% | 32.6% | n/a |
| 2026-11-18 18:52 | exit-window | staged5@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.43% | 16.7% | n/a |
| 2026-11-18 18:52 | exit-window | staged-half@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.47% | 16.3% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma200@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.29% | 10.6% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma50@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.03% | 8.8% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail5@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.84% | 14.3% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail8@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.83% | 18.1% | n/a |
| 2026-11-18 18:52 | exit-window | trig-vix@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.23% | 13.1% | n/a |
| 2026-11-18 18:52 | exit-window | limit3@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.50% | 32.6% | n/a |
| 2026-11-18 18:52 | exit-window | limit5@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.73% | 32.6% | n/a |
| 2026-11-18 18:52 | exit-window | bracket@OSEBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.41% | 14.3% | n/a |
| 2026-11-18 18:52 | exit-window | now@OBX (mean R-1 all starts; MaxDD col = worst R) | baseline | train | 2005-09-26 | 2025-09-29 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:52 | exit-window | fallback@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.99% | 40.1% | n/a |
| 2026-11-18 18:52 | exit-window | staged5@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.45% | 21.9% | n/a |
| 2026-11-18 18:52 | exit-window | staged-half@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.49% | 20.0% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma200@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.55% | 20.0% | n/a |
| 2026-11-18 18:52 | exit-window | trig-sma50@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.19% | 13.1% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail5@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.82% | 17.2% | n/a |
| 2026-11-18 18:52 | exit-window | trig-trail8@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.91% | 18.3% | n/a |
| 2026-11-18 18:52 | exit-window | trig-vix@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.60% | 22.5% | n/a |
| 2026-11-18 18:52 | exit-window | limit3@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.41% | 40.1% | n/a |
| 2026-11-18 18:52 | exit-window | limit5@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.72% | 40.1% | n/a |
| 2026-11-18 18:52 | exit-window | bracket@OBX (mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.26% | 17.2% | n/a |
| 2026-11-18 18:54 | exit-rules | buyhold@GSPC (index, cash 0, trade next close) | baseline | train | 1927-12-30 | 2025-11-07 | 0.42 | +38001.9% | 86.2% | 0.00 |
| 2026-11-18 18:54 | exit-rules | sma10m@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.54 | +41544.1% | 53.8% | 1.47 |
| 2026-11-18 18:54 | exit-rules | sma200d@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.62 | +80543.8% | 53.7% | 5.99 |
| 2026-11-18 18:54 | exit-rules | tsmom12@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.51 | +32338.2% | 54.2% | 0.96 |
| 2026-11-18 18:54 | exit-rules | dd8@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.52 | +39043.3% | 56.3% | 3.15 |
| 2026-11-18 18:54 | exit-rules | dd10@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.52 | +48087.4% | 57.0% | 2.29 |
| 2026-11-18 18:54 | exit-rules | vix30@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.35 | +7801.9% | 86.2% | 0.49 |
| 2026-11-18 18:54 | exit-rules | vixts@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.38 | +15243.1% | 86.2% | 1.10 |
| 2026-11-18 18:54 | exit-rules | baa@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.37 | +11354.4% | 86.2% | 0.61 |
| 2026-11-18 18:54 | exit-rules | hyglqd@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.36 | +10407.3% | 86.2% | 2.06 |
| 2026-11-18 18:54 | exit-rules | cape30@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.44 | +39187.8% | 83.0% | 0.27 |
| 2026-11-18 18:54 | exit-rules | capepct@GSPC (index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.38 | +14059.1% | 79.9% | 0.31 |
| 2026-11-18 18:54 | exit-rules | buyhold@IXIC (index, cash 0, trade next close) | baseline | train | 1971-02-05 | 2025-11-07 | 0.59 | +22904.5% | 77.9% | 0.00 |
| 2026-11-18 18:54 | exit-rules | sma10m@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.68 | +12545.6% | 52.1% | 1.53 |
| 2026-11-18 18:54 | exit-rules | sma200d@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.78 | +18209.2% | 56.7% | 5.52 |
| 2026-11-18 18:54 | exit-rules | tsmom12@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.67 | +16421.7% | 53.4% | 0.80 |
| 2026-11-18 18:54 | exit-rules | dd8@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.87 | +46265.3% | 39.0% | 3.58 |
| 2026-11-18 18:54 | exit-rules | dd10@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.80 | +34778.1% | 50.3% | 2.78 |
| 2026-11-18 18:54 | exit-rules | vix30@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.50 | +2924.2% | 68.6% | 0.88 |
| 2026-11-18 18:54 | exit-rules | vixts@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.51 | +5511.5% | 77.9% | 1.97 |
| 2026-11-18 18:54 | exit-rules | baa@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.53 | +4437.9% | 67.2% | 1.10 |
| 2026-11-18 18:54 | exit-rules | hyglqd@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.47 | +3669.7% | 77.9% | 3.69 |
| 2026-11-18 18:54 | exit-rules | cape30@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.71 | +20221.6% | 59.9% | 0.44 |
| 2026-11-18 18:54 | exit-rules | capepct@IXIC (index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.61 | +7621.4% | 59.9% | 0.33 |
| 2026-11-18 18:56 | exit-window | now@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:56 | exit-window | fallback@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +1.43% | 23.3% | n/a |
| 2026-11-18 18:56 | exit-window | staged5@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.63% | 15.6% | n/a |
| 2026-11-18 18:56 | exit-window | staged-half@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.71% | 11.6% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma200@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.77% | 8.7% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma50@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.13% | 6.9% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail5@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.90% | 12.4% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail8@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +1.10% | 14.6% | n/a |
| 2026-11-18 18:56 | exit-window | trig-vix@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-23 | 2025-05-14 | n/a | +0.64% | 13.4% | n/a |
| 2026-11-18 18:56 | exit-window | limit3@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.75% | 23.3% | n/a |
| 2026-11-18 18:56 | exit-window | limit5@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +1.09% | 23.3% | n/a |
| 2026-11-18 18:56 | exit-window | bracket@GSPC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.39% | 12.4% | n/a |
| 2026-11-18 18:56 | exit-window | now@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:56 | exit-window | fallback@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +1.68% | 23.3% | n/a |
| 2026-11-18 18:56 | exit-window | staged5@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.77% | 15.6% | n/a |
| 2026-11-18 18:56 | exit-window | staged-half@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.84% | 11.6% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma200@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.71% | 8.7% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma50@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.16% | 6.9% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail5@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.97% | 12.4% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail8@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +1.27% | 14.6% | n/a |
| 2026-11-18 18:56 | exit-window | trig-vix@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.91% | 10.6% | n/a |
| 2026-11-18 18:56 | exit-window | limit3@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.92% | 23.3% | n/a |
| 2026-11-18 18:56 | exit-window | limit5@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +1.33% | 23.3% | n/a |
| 2026-11-18 18:56 | exit-window | bracket@GSPC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1996-03-08 | 2025-05-09 | n/a | +0.46% | 12.4% | n/a |
| 2026-11-18 18:56 | exit-window | now@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:56 | exit-window | fallback@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +2.04% | 27.5% | n/a |
| 2026-11-18 18:56 | exit-window | staged5@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +0.68% | 15.3% | n/a |
| 2026-11-18 18:56 | exit-window | staged-half@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +1.02% | 13.8% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma200@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +1.85% | 27.5% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma50@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +0.18% | 9.3% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail5@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +1.31% | 11.6% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail8@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +1.89% | 18.2% | n/a |
| 2026-11-18 18:56 | exit-window | trig-vix@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +1.77% | 27.5% | n/a |
| 2026-11-18 18:56 | exit-window | limit3@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +0.64% | 23.9% | n/a |
| 2026-11-18 18:56 | exit-window | limit5@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +1.15% | 23.9% | n/a |
| 2026-11-18 18:56 | exit-window | bracket@IXIC now-like (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-17 | n/a | +0.19% | 11.6% | n/a |
| 2026-11-18 18:56 | exit-window | now@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +0.00% | -0.0% | n/a |
| 2026-11-18 18:56 | exit-window | fallback@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +1.89% | 27.5% | n/a |
| 2026-11-18 18:56 | exit-window | staged5@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +0.68% | 15.3% | n/a |
| 2026-11-18 18:56 | exit-window | staged-half@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +0.95% | 13.8% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma200@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +1.93% | 27.5% | n/a |
| 2026-11-18 18:56 | exit-window | trig-sma50@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +0.04% | 9.3% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail5@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +1.10% | 11.6% | n/a |
| 2026-11-18 18:56 | exit-window | trig-trail8@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +1.87% | 18.2% | n/a |
| 2026-11-18 18:56 | exit-window | trig-vix@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +1.94% | 27.5% | n/a |
| 2026-11-18 18:56 | exit-window | limit3@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +0.45% | 23.9% | n/a |
| 2026-11-18 18:56 | exit-window | limit5@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +0.84% | 23.9% | n/a |
| 2026-11-18 18:56 | exit-window | bracket@IXIC now-like-vix (post hoc sample; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-31 | 2025-03-17 | n/a | +0.13% | 11.6% | n/a |
| 2026-11-18 19:02 | exit-window | staged3@GSPC (amendment; mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.33% | 22.2% | n/a |
| 2026-11-18 19:02 | exit-window | staged5-sma200@GSPC (amendment; mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.26% | 16.4% | n/a |
| 2026-11-18 19:02 | exit-window | staged-half-sma200@GSPC (amendment; mean R-1 all starts; MaxDD col = worst R) | variant | train | 1929-01-03 | 2025-09-30 | n/a | +0.27% | 14.2% | n/a |
| 2026-11-18 19:02 | exit-window | staged3@IXIC (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.52% | 20.0% | n/a |
| 2026-11-18 19:02 | exit-window | staged5-sma200@IXIC (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.40% | 17.5% | n/a |
| 2026-11-18 19:02 | exit-window | staged-half-sma200@IXIC (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 1972-02-03 | 2025-09-30 | n/a | +0.42% | 14.3% | n/a |
| 2026-11-18 19:02 | exit-window | staged3@OBX (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.49% | 23.8% | n/a |
| 2026-11-18 19:02 | exit-window | staged5-sma200@OBX (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.27% | 10.6% | n/a |
| 2026-11-18 19:02 | exit-window | staged-half-sma200@OBX (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2005-09-26 | 2025-09-29 | n/a | +0.27% | 10.0% | n/a |
| 2026-11-18 19:02 | exit-window | staged3@OSEBX (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.47% | 17.1% | n/a |
| 2026-11-18 19:02 | exit-window | staged5-sma200@OSEBX (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.15% | 8.5% | n/a |
| 2026-11-18 19:02 | exit-window | staged-half-sma200@OSEBX (amendment; mean R-1 all starts; MaxDD col = worst R) | robustness | train | 2014-03-17 | 2025-09-29 | n/a | +0.15% | 5.3% | n/a |
| 2026-11-18 19:02 | exit-rules | sma200d-b2@GSPC (amendment; index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.59 | +68497.71% | 52.8% | 2.55 |
| 2026-11-18 19:02 | exit-rules | sma200d-c2@GSPC (amendment; index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.59 | +64027.32% | 52.0% | 3.35 |
| 2026-11-18 19:02 | exit-rules | kl3m10@GSPC (amendment; index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.46 | +22306.81% | 67.8% | 1.31 |
| 2026-11-18 19:02 | exit-rules | rv2@GSPC (amendment; index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.42 | +22426.68% | 85.4% | 1.14 |
| 2026-11-18 19:02 | exit-rules | sma200d-rv@GSPC (amendment; index, cash 0, trade next close) | variant | train | 1927-12-30 | 2025-11-07 | 0.55 | +65637.17% | 52.0% | 1.90 |
| 2026-11-18 19:02 | exit-rules | sma200d-b2@IXIC (amendment; index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.75 | +16507.88% | 55.9% | 2.70 |
| 2026-11-18 19:02 | exit-rules | sma200d-c2@IXIC (amendment; index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.75 | +15932.71% | 49.2% | 3.58 |
| 2026-11-18 19:02 | exit-rules | kl3m10@IXIC (amendment; index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.65 | +11168.67% | 55.2% | 1.57 |
| 2026-11-18 19:02 | exit-rules | rv2@IXIC (amendment; index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.62 | +15711.17% | 79.7% | 1.17 |
| 2026-11-18 19:02 | exit-rules | sma200d-rv@IXIC (amendment; index, cash 0, trade next close) | robustness | train | 1971-02-05 | 2025-11-07 | 0.73 | +19444.86% | 70.4% | 2.16 |
| 2026-11-18 19:02 | exit-rules | buyhold@OBX (amendment; index, cash 0, trade next close) | baseline | train | 2004-09-27 | 2025-11-07 | 0.55 | +723.02% | 64.8% | 0.00 |
| 2026-11-18 19:02 | exit-rules | sma10m@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.49 | +300.47% | 43.2% | 1.80 |
| 2026-11-18 19:02 | exit-rules | sma200d@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.49 | +277.81% | 31.0% | 9.19 |
| 2026-11-18 19:02 | exit-rules | tsmom12@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.56 | +399.02% | 28.1% | 0.95 |
| 2026-11-18 19:02 | exit-rules | dd8@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.51 | +334.12% | 32.8% | 3.79 |
| 2026-11-18 19:02 | exit-rules | dd10@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.56 | +447.07% | 36.9% | 2.56 |
| 2026-11-18 19:02 | exit-rules | vix30@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.31 | +115.17% | 62.1% | 1.61 |
| 2026-11-18 19:02 | exit-rules | vixts@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.51 | +289.87% | 36.0% | 5.12 |
| 2026-11-18 19:02 | exit-rules | baa@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.65 | +524.32% | 37.9% | 1.33 |
| 2026-11-18 19:02 | exit-rules | hyglqd@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.48 | +241.91% | 46.6% | 13.93 |
| 2026-11-18 19:02 | exit-rules | cape30@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.48 | +426.27% | 64.8% | 0.85 |
| 2026-11-18 19:02 | exit-rules | capepct@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.43 | +312.60% | 64.8% | 0.66 |
| 2026-11-18 19:02 | exit-rules | sma200d-b2@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.50 | +301.10% | 34.5% | 4.26 |
| 2026-11-18 19:02 | exit-rules | sma200d-c2@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.51 | +308.42% | 28.8% | 4.83 |
| 2026-11-18 19:02 | exit-rules | kl3m10@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.69 | +835.43% | 31.6% | 1.23 |
| 2026-11-18 19:02 | exit-rules | rv2@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.62 | +667.02% | 39.3% | 0.95 |
| 2026-11-18 19:02 | exit-rules | sma200d-rv@OBX (amendment; index, cash 0, trade next close) | robustness | train | 2004-09-27 | 2025-11-07 | 0.51 | +350.11% | 46.2% | 2.65 |
| 2026-11-18 19:02 | exit-rules | buyhold@OSEBX (amendment; index, cash 0, trade next close) | baseline | train | 2013-03-05 | 2025-11-07 | 0.67 | +233.84% | 32.8% | 0.00 |
| 2026-11-18 19:02 | exit-rules | sma10m@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.52 | +108.58% | 25.9% | 1.89 |
| 2026-11-18 19:02 | exit-rules | sma200d@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.39 | +65.58% | 31.0% | 9.47 |
| 2026-11-18 19:02 | exit-rules | tsmom12@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.51 | +106.96% | 26.1% | 1.42 |
| 2026-11-18 19:02 | exit-rules | dd8@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.53 | +118.92% | 22.3% | 2.21 |
| 2026-11-18 19:02 | exit-rules | dd10@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.55 | +133.44% | 31.7% | 1.42 |
| 2026-11-18 19:02 | exit-rules | vix30@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.39 | +72.28% | 27.4% | 1.74 |
| 2026-11-18 19:02 | exit-rules | vixts@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.35 | +55.64% | 33.8% | 6.00 |
| 2026-11-18 19:02 | exit-rules | baa@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.52 | +115.39% | 38.1% | 1.42 |
| 2026-11-18 19:02 | exit-rules | hyglqd@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.48 | +73.84% | 19.0% | 15.46 |
| 2026-11-18 19:02 | exit-rules | cape30@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.66 | +138.84% | 22.1% | 1.42 |
| 2026-11-18 19:02 | exit-rules | capepct@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.50 | +91.08% | 22.1% | 0.95 |
| 2026-11-18 19:02 | exit-rules | sma200d-b2@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.42 | +76.37% | 29.0% | 3.63 |
| 2026-11-18 19:02 | exit-rules | sma200d-c2@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.45 | +82.29% | 27.6% | 4.10 |
| 2026-11-18 19:02 | exit-rules | kl3m10@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.53 | +127.60% | 31.5% | 0.79 |
| 2026-11-18 19:02 | exit-rules | rv2@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.57 | +143.64% | 31.5% | 1.10 |
| 2026-11-18 19:02 | exit-rules | sma200d-rv@OSEBX (amendment; index, cash 0, trade next close) | robustness | train | 2013-03-05 | 2025-11-07 | 0.48 | +98.70% | 28.1% | 2.84 |
| 2026-11-18 19:31 | exit-window | fallback@GSPC now-like-below200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1965-06-09 | 2025-05-09 | n/a | +1.30% | 11.0% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half@GSPC now-like-below200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1965-06-09 | 2025-05-09 | n/a | +0.65% | 5.5% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half-sma200@GSPC now-like-below200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1965-06-09 | 2025-05-09 | n/a | +0.06% | 2.4% | n/a |
| 2026-11-18 19:31 | exit-window | fallback@GSPC now-like-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +1.48% | 23.3% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half@GSPC now-like-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.74% | 11.6% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half-sma200@GSPC now-like-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1961-06-15 | 2025-05-14 | n/a | +0.53% | 4.4% | n/a |
| 2026-11-18 19:31 | exit-window | fallback@IXIC now-like-below200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-29 | 2025-03-17 | n/a | -1.89% | 16.1% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half@IXIC now-like-below200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-29 | 2025-03-17 | n/a | -0.94% | 8.0% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half-sma200@IXIC now-like-below200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1994-03-29 | 2025-03-17 | n/a | -0.26% | 2.2% | n/a |
| 2026-11-18 19:31 | exit-window | fallback@IXIC now-like-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-05 | n/a | +2.51% | 27.5% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half@IXIC now-like-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-05 | n/a | +1.25% | 13.8% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half-sma200@IXIC now-like-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 1993-04-02 | 2025-03-05 | n/a | +1.06% | 13.8% | n/a |
| 2026-11-18 19:31 | exit-window | fallback@OSEBX late-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 2015-03-19 | 2025-09-29 | n/a | +0.16% | 14.0% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half@OSEBX late-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 2015-03-19 | 2025-09-29 | n/a | +0.08% | 7.0% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half-sma200@OSEBX late-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 2015-03-19 | 2025-09-29 | n/a | +0.01% | 5.0% | n/a |
| 2026-11-18 19:31 | exit-window | fallback@OBX late-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 2006-10-26 | 2025-09-29 | n/a | +0.37% | 20.5% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half@OBX late-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 2006-10-26 | 2025-09-29 | n/a | +0.18% | 10.3% | n/a |
| 2026-11-18 19:31 | exit-window | staged-half-sma200@OBX late-above200 (post hoc review-1 cut; mean R-1; MaxDD col = worst R) | robustness | train | 2006-10-26 | 2025-09-29 | n/a | +0.18% | 5.7% | n/a |
| 2026-11-18 18:58 | trend-where | where-vol@bond-m | robustness | train | 1954-06-01 | 2001-12-31 | 0.82 | +678.9% | 25.6% | 1.01 |
| 2026-11-18 18:58 | trend-where | tsmom12@bond-m | baseline | train | 1954-06-01 | 2001-12-31 | 0.82 | +678.9% | 25.6% | 1.01 |
| 2026-11-18 18:58 | trend-where | hold@bond-m | baseline | train | 1954-06-01 | 2001-12-31 | 0.99 | +1845.6% | 15.2% | 0.00 |
| 2026-11-18 18:58 | trend-where | where-vol-min12@bond-m | robustness | train | 1954-06-01 | 2001-12-31 | 0.82 | +678.9% | 25.6% | 1.01 |
| 2026-11-18 18:58 | trend-where | where-vol-lag0@bond-m | robustness | train | 1954-06-01 | 2001-12-31 | 0.97 | +1032.7% | 20.5% | 1.01 |
| 2026-11-18 18:58 | trend-where | tsmom12-lag0@bond-m | robustness | train | 1954-06-01 | 2001-12-31 | 0.97 | +1032.7% | 20.5% | 1.01 |
| 2026-11-18 18:58 | trend-where | where-vol@gold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.47 | +718.1% | 51.7% | 0.27 |
| 2026-11-18 18:58 | trend-where | tsmom12@gold-m | baseline | train | 1972-02-01 | 2001-12-31 | 0.51 | +800.3% | 42.6% | 1.20 |
| 2026-11-18 18:58 | trend-where | hold@gold-m | baseline | train | 1972-02-01 | 2001-12-31 | 0.39 | +499.9% | 62.1% | 0.00 |
| 2026-11-18 18:58 | trend-where | where-vol-min12@gold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.41 | +541.8% | 62.1% | 0.13 |
| 2026-11-18 18:58 | trend-where | where-vol-lag0@gold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.53 | +1042.5% | 47.3% | 0.27 |
| 2026-11-18 18:58 | trend-where | tsmom12-lag0@gold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.59 | +1257.7% | 32.5% | 1.20 |
| 2026-11-18 18:58 | trend-where | where-vol@bondgold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.79 | +718.2% | 21.6% | 0.60 |
| 2026-11-18 18:58 | trend-where | tsmom12@bondgold-m | baseline | train | 1972-02-01 | 2001-12-31 | 0.85 | +745.7% | 21.6% | 1.07 |
| 2026-11-18 18:58 | trend-where | hold@bondgold-m | baseline | train | 1972-02-01 | 2001-12-31 | 0.79 | +891.2% | 28.1% | 0.00 |
| 2026-11-18 18:58 | trend-where | where-vol-min12@bondgold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.71 | +636.1% | 34.9% | 0.53 |
| 2026-11-18 18:58 | trend-where | where-vol-lag0@bondgold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.90 | +985.3% | 14.6% | 0.60 |
| 2026-11-18 18:58 | trend-where | tsmom12-lag0@bondgold-m | robustness | train | 1972-02-01 | 2001-12-31 | 0.97 | +1067.7% | 14.6% | 1.07 |
| 2026-11-18 22:15 | combo-1 | blend-iv | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +8605.5% | 44.4% | 1.44 |
| 2026-11-18 22:15 | combo-1 | blend-ws | variant | train | 1994-02-01 | 2025-11-09 | 1.13 | +15262.9% | 28.9% | 3.02 |
| 2026-11-18 22:15 | combo-1 | blend-iv@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.61 | +237.0% | 21.9% | 1.73 |
| 2026-11-18 22:15 | combo-1 | blend-ws@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.62 | +247.8% | 16.8% | 2.66 |
| 2026-11-18 22:15 | combo-1 | blend-iv@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.65 | +454.3% | 90.9% | 4.04 |
| 2026-11-18 22:15 | combo-1 | blend-ws@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.56 | +287.6% | 76.0% | 4.56 |
| 2026-11-18 22:15 | combo-1 | blend-iv@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.69 | +5371.8% | 33.0% | 1.49 |
| 2026-11-18 22:15 | combo-1 | blend-ws@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.72 | +4483.0% | 25.7% | 2.27 |
| 2026-11-18 22:23 | combo-2 | tsmom12 cash | robustness | train | 1994-02-01 | 2025-11-09 | 1.08 | +21395.9% | 35.6% | 2.74 |
| 2026-11-18 22:23 | combo-2 | trend-vol cash | robustness | train | 1994-02-01 | 2025-11-09 | 1.08 | +6086.1% | 22.2% | 2.94 |
| 2026-11-18 22:23 | combo-2 | where-vol cash | robustness | train | 1994-02-01 | 2025-11-09 | 1.09 | +26783.0% | 34.9% | 1.71 |
| 2026-11-18 22:23 | combo-2 | stop-0.25 cash | robustness | train | 1994-02-01 | 2025-11-09 | 1.13 | +11897.6% | 25.7% | 3.85 |
| 2026-11-18 22:23 | combo-2 | inverse-vol cash | robustness | train | 1994-02-01 | 2025-11-09 | 0.85 | +4071.6% | 61.1% | 0.73 |
| 2026-11-18 22:23 | combo-2 | sixty-forty cash | robustness | train | 1994-02-01 | 2025-11-09 | 0.80 | +1295.3% | 30.2% | 0.47 |
| 2026-11-18 22:23 | combo-2 | blend-iv cash | robustness | train | 1994-02-01 | 2025-11-09 | 1.09 | +9252.5% | 42.8% | 1.43 |
| 2026-11-18 22:23 | combo-2 | blend-ws cash | robustness | train | 1994-02-01 | 2025-11-09 | 1.16 | +17676.0% | 25.7% | 3.01 |
| 2026-11-18 22:23 | combo-2 | blend-iv cash@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.65 | +261.7% | 21.8% | 1.73 |
| 2026-11-18 22:23 | combo-2 | blend-ws cash@etf | robustness | train | 2001-05-27 | 2025-11-09 | 0.67 | +288.2% | 16.7% | 2.65 |
| 2026-11-18 22:23 | combo-2 | blend-iv cash@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.66 | +487.0% | 90.8% | 4.05 |
| 2026-11-18 22:23 | combo-2 | blend-ws cash@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.59 | +345.9% | 75.2% | 4.57 |
| 2026-11-18 22:23 | combo-2 | blend-iv cash@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.76 | +8241.7% | 32.5% | 1.50 |
| 2026-11-18 22:23 | combo-2 | blend-ws cash@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.85 | +9251.6% | 25.6% | 2.28 |
| 2026-11-18 22:27 | combo-2 | cofall-dbc | variant | train | 1994-02-01 | 2025-11-09 | 1.07 | +20836.7% | 35.6% | 2.83 |
| 2026-11-19 02:42 | hdd-gas | UNG next-week on HDD surprise (slope -0.036 pp/10DD, t -0.29, rank 19/41, gate fail) | screen | train | 2007-11-02 | 2025-03-28 | - | - | - | - |
| 2026-11-19 03:15 | cpc-revision | UNG next-session open-to-close on CPC 6-10/8-14 outlook revision (slope -0.076 pp/0.10, t -0.68, rank 36/41, gate fail) | screen | train | 2012-11-01 | 2025-03-31 | - | - | - | - |
| 2026-11-19 03:04 | act-haven | GLD+TLT 4-week return on GPR acts z, from available-on date (b -0.137%/z, t -1.02, rank 21/41, gate fail) | screen | train | 2005-01-03 | 2025-10-06 | - | - | - | - |
| 2026-11-19 03:04 | failure-premium | XLF 4-week return on ln(1 + FDIC failed assets) with past-return controls (b -0.059%/unit, t -0.48, rank 21/41, gate fail) | screen | train | 2000-01-07 | 2025-10-03 | - | - | - | - |
| 2026-11-24 19:50 | pooled-1 | e4@pooled-41 (pooled dSharpe vs tsmom12 +0.063, SE 0.041, z +1.55; weekly Sharpe; still open; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.54 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | or3-12@pooled-41 (pooled dSharpe vs tsmom12 +0.018, SE 0.040, z +0.47; weekly Sharpe; still open; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.50 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | arm3-12@pooled-41 (pooled dSharpe vs tsmom12 +0.015, SE 0.038, z +0.39; weekly Sharpe; still open; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.49 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@pooled-41 (pooled dSharpe vs tsmom12 +0.022, SE 0.016, z +1.37; weekly Sharpe; still open; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.50 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@pooled-41 (pooled dSharpe vs tsmom12 -0.012, SE 0.029, z -0.43; weekly Sharpe; still open; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.47 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | tv40@pooled-41 (pooled dSharpe vs tsmom12 +0.002, SE 0.002, z +0.68; weekly Sharpe; killed; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.48 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | fade-28@pooled-41 (pooled dSharpe vs tsmom12 -0.062, SE 0.042, z -1.48; weekly Sharpe; killed; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.42 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@pooled-41 (pooled dSharpe vs tsmom12 -0.066, SE 0.050, z -1.33; weekly Sharpe; still open; -) | variant | train | 1927-07-05 | 2025-10-31 | 0.41 | - | - | - |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.83 | +539793.5% | 33.8% | 1.78 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.82 | +148864.2% | 39.2% | 4.93 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.83 | +1026886.9% | 56.8% | 2.29 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.84 | +1053678.3% | 56.8% | 2.57 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.88 | +39227.2% | 27.4% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.88 | +915.4% | 12.9% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.83 | +519481.1% | 35.2% | 1.80 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.72 | +26631.8% | 28.7% | 8.90 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-NoDur | robustness | train | 1927-07-05 | 2025-10-31 | 0.60 | +8803.8% | 34.2% | 5.94 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.56 | +507191.5% | 73.6% | 2.37 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.68 | +1341125.0% | 48.6% | 5.12 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.60 | +2652162.2% | 74.4% | 3.10 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.59 | +1838806.1% | 71.4% | 3.61 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.62 | +77787.2% | 53.6% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.59 | +1574.4% | 22.2% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.55 | +309381.7% | 69.6% | 2.51 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.58 | +101186.5% | 39.8% | 8.36 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Durbl | robustness | train | 1927-07-05 | 2025-10-31 | 0.54 | +42028.8% | 34.4% | 5.40 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.70 | +608703.1% | 50.7% | 1.78 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.73 | +272046.0% | 42.4% | 4.78 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.70 | +1492687.3% | 63.4% | 2.45 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.71 | +1654091.1% | 63.4% | 2.72 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.77 | +128189.6% | 44.6% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.75 | +2177.5% | 17.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.70 | +534023.3% | 50.4% | 1.82 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.63 | +40157.5% | 28.3% | 8.33 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Manuf | robustness | train | 1927-07-05 | 2025-10-31 | 0.49 | +6581.7% | 42.0% | 5.99 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.56 | +223854.9% | 56.0% | 2.55 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.58 | +116392.3% | 43.9% | 5.24 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.55 | +347637.7% | 63.7% | 3.00 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.54 | +282802.5% | 60.8% | 3.75 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.57 | +24821.1% | 50.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.54 | +860.3% | 26.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.56 | +205220.7% | 55.8% | 2.61 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.49 | +19050.9% | 36.7% | 8.81 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Enrgy | robustness | train | 1927-07-05 | 2025-10-31 | 0.44 | +7278.1% | 39.6% | 5.77 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.66 | +1760289.9% | 56.2% | 2.02 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.65 | +433855.0% | 57.8% | 5.07 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.64 | +2772498.1% | 66.7% | 2.74 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.62 | +1883566.3% | 66.7% | 3.24 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.69 | +183753.2% | 53.9% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.63 | +1817.0% | 27.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.66 | +1435313.4% | 54.8% | 2.08 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.64 | +141427.8% | 46.6% | 8.41 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-HiTec | robustness | train | 1927-07-05 | 2025-10-31 | 0.55 | +34915.6% | 44.9% | 5.58 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.75 | +312547.1% | 32.7% | 1.84 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.75 | +119301.5% | 41.5% | 4.83 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.73 | +413870.6% | 55.5% | 2.37 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.71 | +334037.7% | 54.6% | 2.80 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.80 | +22227.2% | 23.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.74 | +592.6% | 10.9% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +317009.9% | 31.3% | 1.87 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.61 | +19106.9% | 40.5% | 8.89 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Telcm | robustness | train | 1927-07-05 | 2025-10-31 | 0.70 | +28593.2% | 33.6% | 5.09 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +962239.9% | 53.8% | 1.74 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.78 | +361712.4% | 45.5% | 4.88 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +2324612.2% | 59.3% | 2.41 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +2198540.2% | 59.3% | 2.76 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.87 | +163032.9% | 36.3% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.87 | +2180.6% | 13.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.75 | +878292.1% | 53.9% | 1.77 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +125337.0% | 40.7% | 8.11 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Shops | robustness | train | 1927-07-05 | 2025-10-31 | 0.73 | +58131.0% | 34.5% | 5.28 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.72 | +702197.9% | 42.1% | 2.04 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.75 | +258702.6% | 44.7% | 5.01 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.65 | +480499.4% | 61.0% | 2.78 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.65 | +439381.2% | 61.0% | 3.22 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.78 | +45828.7% | 29.1% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.64 | +399.1% | 19.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.72 | +632448.8% | 42.7% | 2.08 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.64 | +40377.9% | 47.8% | 8.68 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Hlth | robustness | train | 1927-07-05 | 2025-10-31 | 0.64 | +24771.9% | 48.4% | 5.48 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.74 | +399121.2% | 56.0% | 1.78 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.77 | +240232.1% | 57.9% | 4.44 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.65 | +279751.0% | 74.9% | 2.15 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.66 | +322335.5% | 74.6% | 2.51 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.82 | +97712.5% | 41.9% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +1217.8% | 21.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +414678.8% | 45.6% | 1.80 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.88 | +290077.2% | 29.4% | 8.13 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Utils | robustness | train | 1927-07-05 | 2025-10-31 | 0.66 | +20500.8% | 31.9% | 5.38 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.66 | +306701.5% | 49.7% | 1.74 |
| 2026-11-24 19:50 | pooled-1 | e4@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.73 | +285146.7% | 37.0% | 4.51 |
| 2026-11-24 19:50 | pooled-1 | or3-12@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.68 | +1137004.8% | 58.4% | 2.35 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.70 | +1404945.9% | 55.3% | 2.67 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.75 | +67932.2% | 43.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.76 | +1406.9% | 15.9% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.67 | +301387.8% | 50.0% | 1.76 |
| 2026-11-24 19:50 | pooled-1 | fade-28@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.66 | +51928.6% | 35.3% | 7.71 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@US10-US-Other | robustness | train | 1927-07-05 | 2025-10-31 | 0.57 | +12501.7% | 40.8% | 5.08 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.56 | +4526.5% | 46.5% | 2.23 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.52 | +2055.7% | 37.7% | 5.35 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.59 | +8906.1% | 47.5% | 3.00 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.61 | +9391.4% | 49.2% | 3.46 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.55 | +1175.1% | 34.6% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.44 | +118.4% | 15.2% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.56 | +4381.2% | 46.5% | 2.28 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.50 | +1325.0% | 49.1% | 8.38 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Japan | robustness | train | 1966-01-25 | 2025-10-31 | 0.33 | +366.1% | 39.0% | 5.10 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.42 | +525.9% | 38.6% | 2.05 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.58 | +788.7% | 22.3% | 5.10 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.57 | +1582.0% | 36.8% | 2.80 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.56 | +1504.3% | 38.3% | 3.07 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.48 | +331.5% | 27.8% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.47 | +71.9% | 8.8% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.41 | +512.0% | 38.6% | 2.06 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.44 | +314.2% | 29.2% | 7.48 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Canada | robustness | train | 1980-07-08 | 2025-10-31 | 0.44 | +301.8% | 21.5% | 5.72 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.34 | +289.8% | 40.0% | 2.62 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.24 | +116.4% | 44.1% | 6.06 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.31 | +264.9% | 40.1% | 3.55 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.28 | +215.3% | 41.1% | 4.14 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.39 | +258.6% | 29.6% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.44 | +88.9% | 11.8% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.35 | +309.5% | 37.0% | 2.62 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.16 | +49.9% | 53.6% | 9.38 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-UK | robustness | train | 1985-01-08 | 2025-10-31 | 0.17 | +56.0% | 39.3% | 6.35 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.32 | +237.1% | 53.5% | 2.56 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.46 | +384.4% | 33.5% | 5.37 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.44 | +579.8% | 44.3% | 3.01 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.43 | +529.3% | 44.3% | 3.71 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.38 | +218.3% | 42.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.37 | +61.4% | 20.5% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.33 | +247.5% | 52.2% | 2.56 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.32 | +140.1% | 36.2% | 9.28 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Australia | robustness | train | 1985-08-20 | 2025-10-31 | 0.32 | +131.9% | 39.2% | 5.70 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.39 | +619.3% | 45.3% | 2.51 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.43 | +577.3% | 40.5% | 5.38 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.46 | +1245.9% | 42.9% | 3.68 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.44 | +1093.4% | 43.3% | 4.15 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.45 | +502.5% | 36.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.41 | +105.6% | 17.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.40 | +653.3% | 45.1% | 2.63 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.33 | +252.0% | 37.3% | 7.86 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-HongKong | robustness | train | 1988-01-12 | 2025-10-31 | 0.25 | +128.0% | 31.3% | 4.68 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.40 | +518.0% | 56.4% | 1.82 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.55 | +802.0% | 30.6% | 5.08 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.47 | +956.7% | 52.6% | 2.69 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.48 | +990.7% | 53.3% | 3.01 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.45 | +338.9% | 43.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.44 | +82.7% | 16.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.40 | +512.7% | 56.4% | 1.84 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.41 | +305.0% | 32.8% | 8.50 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Germany | robustness | train | 1989-01-03 | 2025-10-31 | 0.40 | +283.6% | 29.8% | 6.00 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.29 | +162.6% | 46.8% | 2.64 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.45 | +349.2% | 37.9% | 5.18 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.50 | +770.6% | 46.9% | 3.29 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.50 | +722.0% | 45.9% | 3.78 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.34 | +137.2% | 33.1% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.24 | +30.1% | 23.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.29 | +162.1% | 46.9% | 2.64 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.18 | +54.1% | 40.7% | 7.15 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Singapore | robustness | train | 1989-01-17 | 2025-10-31 | 0.41 | +188.4% | 28.0% | 3.67 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.30 | +211.4% | 45.9% | 2.11 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.27 | +135.8% | 33.8% | 5.72 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.23 | +128.4% | 41.1% | 3.55 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.24 | +136.7% | 47.2% | 3.96 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.31 | +138.6% | 31.9% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.26 | +33.5% | 13.8% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.30 | +206.6% | 45.9% | 2.13 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.20 | +67.1% | 44.5% | 8.57 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-France | robustness | train | 1991-03-12 | 2025-10-31 | 0.16 | +44.6% | 41.9% | 5.80 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.41 | +325.0% | 42.0% | 3.09 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.42 | +246.9% | 36.4% | 5.66 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.34 | +247.7% | 53.3% | 4.04 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.35 | +265.1% | 50.0% | 4.80 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.47 | +237.7% | 28.4% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.46 | +58.2% | 13.2% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.41 | +325.8% | 42.0% | 3.09 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.33 | +134.1% | 39.7% | 9.63 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Switzerland | robustness | train | 1991-11-19 | 2025-10-31 | 0.38 | +165.6% | 39.4% | 5.18 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.40 | +280.3% | 39.1% | 2.42 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.44 | +278.8% | 34.2% | 5.56 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.46 | +494.9% | 42.8% | 3.49 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.48 | +505.9% | 37.8% | 3.91 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.37 | +145.5% | 34.3% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.27 | +35.6% | 17.2% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.40 | +280.0% | 39.1% | 2.42 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.33 | +135.8% | 37.2% | 8.20 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Belgium | robustness | train | 1992-04-22 | 2025-10-31 | 0.37 | +144.6% | 23.0% | 4.92 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.49 | +521.5% | 37.0% | 2.22 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.46 | +336.8% | 23.0% | 5.23 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.41 | +397.4% | 44.7% | 2.97 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.40 | +370.7% | 44.7% | 3.59 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.48 | +234.6% | 20.4% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.43 | +47.1% | 6.7% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.49 | +521.4% | 35.9% | 2.22 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.28 | +111.9% | 45.1% | 8.77 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Netherlands | robustness | train | 1993-10-19 | 2025-10-31 | 0.35 | +149.3% | 35.7% | 5.90 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.29 | +162.6% | 60.9% | 2.35 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.45 | +340.0% | 34.8% | 5.15 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.50 | +745.0% | 44.3% | 3.10 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.48 | +653.1% | 42.7% | 3.60 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.28 | +95.9% | 39.2% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.17 | +18.7% | 15.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.29 | +163.6% | 61.1% | 2.38 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.32 | +141.9% | 43.1% | 7.80 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Austria | robustness | train | 1993-11-23 | 2025-10-31 | 0.36 | +159.8% | 43.9% | 4.04 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.45 | +427.6% | 55.6% | 1.95 |
| 2026-11-24 19:50 | pooled-1 | e4@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.41 | +255.2% | 52.8% | 5.55 |
| 2026-11-24 19:50 | pooled-1 | or3-12@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.35 | +278.1% | 61.2% | 4.38 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.34 | +255.8% | 62.3% | 4.63 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.45 | +243.1% | 45.0% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.41 | +66.9% | 18.8% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.45 | +421.6% | 55.7% | 1.94 |
| 2026-11-24 19:50 | pooled-1 | fade-28@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.36 | +167.2% | 48.7% | 7.90 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@DEV13-Spain | robustness | train | 1994-07-19 | 2025-10-31 | 0.37 | +163.8% | 29.5% | 4.95 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | 0.10 | +12.0% | 63.8% | 2.05 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | 0.23 | +68.4% | 34.3% | 5.44 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | 0.12 | +15.7% | 60.7% | 3.32 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | 0.08 | +0.1% | 64.0% | 3.91 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | 0.13 | +23.4% | 42.3% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | 0.10 | +9.1% | 19.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | 0.10 | +12.2% | 63.5% | 2.03 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | -0.10 | -33.0% | 54.7% | 7.98 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Italy | robustness | train | 1999-01-05 | 2025-10-31 | -0.02 | -16.9% | 38.3% | 5.33 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.85 | +454.4% | 29.6% | 1.06 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.95 | +389.3% | 20.4% | 4.15 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.83 | +469.0% | 29.6% | 1.51 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.83 | +471.8% | 29.6% | 1.61 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.81 | +199.9% | 16.8% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.71 | +45.5% | 7.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.84 | +442.9% | 29.6% | 1.06 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.95 | +314.2% | 11.0% | 8.12 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-NewZealand | robustness | train | 2004-01-13 | 2025-10-31 | 0.61 | +131.2% | 19.4% | 6.19 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.53 | +774.4% | 30.7% | 1.84 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.66 | +943.3% | 27.3% | 5.01 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.54 | +954.6% | 41.5% | 2.90 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.54 | +969.2% | 41.0% | 3.40 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.52 | +398.2% | 22.9% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.52 | +115.4% | 13.7% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.54 | +783.0% | 30.7% | 1.86 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.59 | +541.2% | 24.3% | 7.64 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Israel | robustness | train | 1993-10-12 | 2025-10-30 | 0.54 | +390.4% | 22.2% | 5.34 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.46 | +508.9% | 47.0% | 2.98 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.50 | +493.4% | 36.4% | 5.70 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.36 | +310.6% | 63.5% | 4.13 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.36 | +309.2% | 63.5% | 4.85 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.49 | +415.0% | 44.6% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.49 | +106.8% | 20.3% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.47 | +501.0% | 46.6% | 3.11 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.45 | +304.7% | 29.9% | 8.16 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Korea | robustness | train | 1998-01-06 | 2025-10-31 | 0.39 | +206.6% | 34.9% | 5.28 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.31 | +152.7% | 52.4% | 2.75 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.38 | +187.5% | 34.9% | 5.17 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.43 | +370.9% | 47.5% | 3.26 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.39 | +286.0% | 53.5% | 4.00 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.29 | +106.4% | 38.8% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.29 | +41.2% | 13.3% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.30 | +147.3% | 52.3% | 2.78 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.15 | +32.1% | 42.3% | 8.76 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Taiwan | robustness | train | 1998-07-21 | 2025-10-31 | 0.19 | +44.6% | 31.5% | 5.68 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.59 | +824.9% | 46.2% | 2.24 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.76 | +1208.4% | 28.6% | 4.93 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.68 | +1699.2% | 42.1% | 2.38 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.61 | +1044.4% | 42.1% | 3.26 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.63 | +513.5% | 34.6% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.48 | +67.5% | 18.3% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.61 | +891.4% | 46.0% | 2.31 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.62 | +538.8% | 37.5% | 8.47 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-India | robustness | train | 1998-07-21 | 2025-10-31 | 0.53 | +316.8% | 28.2% | 5.54 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.55 | +2250.1% | 61.2% | 3.08 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.70 | +3773.7% | 45.5% | 5.27 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.60 | +4247.3% | 61.2% | 3.40 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.63 | +4785.1% | 61.2% | 4.23 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.57 | +1288.9% | 47.0% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.56 | +210.0% | 20.1% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.52 | +1389.0% | 54.4% | 3.31 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.47 | +807.0% | 49.6% | 8.80 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Brazil | robustness | train | 1994-05-10 | 2025-10-31 | 0.55 | +1041.0% | 53.0% | 4.92 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.47 | +764.3% | 50.5% | 3.25 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.52 | +706.8% | 35.9% | 5.57 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.53 | +1387.2% | 44.5% | 3.80 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.55 | +1419.7% | 42.7% | 4.41 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.49 | +485.6% | 47.1% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.46 | +108.7% | 24.2% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.47 | +757.7% | 50.5% | 3.32 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.40 | +319.6% | 45.4% | 8.81 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Mexico | robustness | train | 1992-12-01 | 2025-10-31 | 0.29 | +135.7% | 45.4% | 5.92 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.15 | +35.5% | 48.9% | 2.85 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.37 | +147.1% | 26.5% | 5.03 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.19 | +60.2% | 50.6% | 4.18 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.15 | +39.2% | 53.3% | 4.70 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.22 | +47.9% | 27.4% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.26 | +24.6% | 10.6% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.15 | +35.7% | 48.9% | 2.86 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.16 | +33.5% | 37.9% | 7.38 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Malaysia | robustness | train | 1994-12-13 | 2025-10-31 | 0.43 | +130.8% | 15.6% | 3.30 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.46 | +696.7% | 59.4% | 2.35 |
| 2026-11-24 19:50 | pooled-1 | e4@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.76 | +2532.2% | 32.1% | 4.62 |
| 2026-11-24 19:50 | pooled-1 | or3-12@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.59 | +2164.6% | 68.1% | 3.10 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.56 | +1710.6% | 71.1% | 3.51 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.49 | +430.6% | 41.3% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.44 | +85.3% | 16.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.47 | +716.0% | 57.6% | 2.39 |
| 2026-11-24 19:50 | pooled-1 | fade-28@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.51 | +508.4% | 36.4% | 8.20 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@WIDE10-Indonesia | robustness | train | 1991-04-30 | 2025-10-31 | 0.57 | +570.1% | 28.4% | 3.80 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.36 | +194.8% | 31.6% | 2.83 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.41 | +202.6% | 30.2% | 5.98 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.36 | +225.2% | 44.4% | 3.48 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.34 | +186.4% | 44.4% | 4.22 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.33 | +102.7% | 25.0% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.25 | +25.1% | 12.5% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.37 | +195.7% | 31.4% | 2.86 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.17 | +38.4% | 30.3% | 9.30 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-IWM | robustness | train | 2001-06-05 | 2025-10-31 | 0.10 | +11.9% | 29.5% | 5.78 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.32 | +109.9% | 44.1% | 2.89 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.52 | +210.8% | 23.4% | 5.14 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.35 | +152.6% | 43.8% | 3.33 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.38 | +174.9% | 43.1% | 4.28 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.32 | +76.8% | 35.6% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.35 | +31.4% | 13.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.33 | +116.4% | 44.1% | 2.91 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.27 | +62.5% | 22.6% | 8.59 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-EFA | robustness | train | 2002-09-04 | 2025-10-31 | 0.33 | +82.3% | 25.1% | 5.14 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.44 | +248.1% | 47.1% | 2.65 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.43 | +192.3% | 32.1% | 5.71 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.51 | +413.8% | 43.4% | 3.20 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.46 | +314.8% | 48.4% | 3.86 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.40 | +142.1% | 42.9% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.40 | +53.8% | 17.5% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.44 | +247.1% | 45.6% | 2.72 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.12 | +17.7% | 46.4% | 9.15 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-EEM | robustness | train | 2004-04-20 | 2025-10-31 | 0.35 | +109.0% | 35.9% | 5.53 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.67 | +116.6% | 10.4% | 1.93 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.59 | +78.0% | 8.1% | 5.40 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.59 | +105.5% | 12.5% | 3.10 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.62 | +113.6% | 11.5% | 3.37 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.66 | +66.1% | 7.9% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.59 | +20.8% | 4.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.67 | +116.6% | 10.4% | 1.93 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.45 | +51.6% | 9.1% | 8.77 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-IEF | robustness | train | 2003-08-05 | 2025-10-31 | 0.40 | +38.7% | 11.2% | 5.35 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.45 | +89.2% | 21.8% | 2.38 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.61 | +96.3% | 15.9% | 5.13 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.49 | +105.8% | 21.8% | 2.47 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.49 | +106.5% | 21.8% | 2.92 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.44 | +48.3% | 14.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.43 | +16.4% | 6.4% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.45 | +87.0% | 21.8% | 2.38 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.45 | +54.5% | 13.0% | 9.13 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-LQD | robustness | train | 2003-08-05 | 2025-10-31 | 0.39 | +42.3% | 12.9% | 5.62 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.38 | +155.6% | 39.1% | 2.59 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.31 | +94.0% | 34.9% | 5.74 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.25 | +81.3% | 50.9% | 3.34 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.23 | +63.4% | 53.1% | 4.04 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.36 | +105.3% | 27.8% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.35 | +38.4% | 11.9% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.38 | +153.9% | 39.1% | 2.65 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.17 | +29.8% | 28.1% | 9.66 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-VNQ | robustness | train | 2005-10-04 | 2025-10-31 | 0.21 | +40.7% | 35.5% | 5.38 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.15 | +24.8% | 51.3% | 3.58 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.35 | +91.8% | 37.4% | 5.90 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.25 | +65.0% | 51.7% | 4.44 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.29 | +85.3% | 47.8% | 5.18 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.13 | +15.3% | 41.0% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.12 | +7.0% | 22.0% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.16 | +26.3% | 50.6% | 3.60 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.20 | +36.0% | 42.4% | 7.64 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-DBC | robustness | train | 2007-02-13 | 2025-10-31 | 0.40 | +93.2% | 26.8% | 4.22 |
| 2026-11-24 19:50 | pooled-1 | tsmom12@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.34 | +169.1% | 61.0% | 3.08 |
| 2026-11-24 19:50 | pooled-1 | e4@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.22 | +55.6% | 70.7% | 6.44 |
| 2026-11-24 19:50 | pooled-1 | or3-12@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.25 | +71.4% | 78.6% | 4.49 |
| 2026-11-24 19:50 | pooled-1 | arm3-12@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.30 | +119.8% | 73.0% | 5.36 |
| 2026-11-24 19:50 | pooled-1 | vt-own-70-x@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.25 | +65.3% | 49.7% | - |
| 2026-11-24 19:50 | pooled-1 | vt-own-26-x@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.33 | +36.9% | 16.8% | - |
| 2026-11-24 19:50 | pooled-1 | tv40@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.35 | +172.9% | 60.7% | 3.43 |
| 2026-11-24 19:50 | pooled-1 | fade-28@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.25 | +74.9% | 60.3% | 8.06 |
| 2026-11-24 19:50 | pooled-1 | stop-0.25@ETF8-SLV | robustness | train | 2007-05-08 | 2025-10-31 | 0.37 | +144.5% | 52.3% | 3.79 |
| 2026-11-24 19:38 | reconcile-1 | live paper record vs gym, 11 books, 2026-11-11..24: 0 bugs (c), 0 data (b); 9 books equal gym.backtest daily, risk_parity/xs_momentum differ by schedule (a, max 0.5%); scoreboard so far on old code 9b1c45e (d, moves once at next run) | note | - | 2026-11-11 | 2026-11-24 | - | - | - | - |
| 2026-11-24 19:35 | breadth-book-1 | six@2008 | baseline | train | 2008-01-02 | 2025-11-09 | 1.23 | +4272.3% | 37.6% | 2.87 |
| 2026-11-24 19:35 | breadth-book-1 | four@2008 | baseline | train | 2008-01-02 | 2025-11-09 | 0.92 | +280.0% | 15.7% | 2.44 |
| 2026-11-24 19:35 | breadth-book-1 | E-6@2008 | variant | train | 2008-01-02 | 2025-11-09 | 0.73 | +154.8% | 12.5% | 2.58 |
| 2026-11-24 19:35 | breadth-book-1 | E-12@2008 | variant | train | 2008-01-02 | 2025-11-09 | 0.53 | +76.2% | 10.1% | 2.73 |
| 2026-11-24 19:35 | breadth-book-1 | E-20@2008 | variant | train | 2008-01-02 | 2025-11-09 | 0.46 | +74.9% | 15.3% | 2.85 |
| 2026-11-24 19:35 | breadth-book-1 | E-all@2008 | variant | train | 2008-01-02 | 2025-11-09 | 0.48 | +96.1% | 17.8% | 2.69 |
| 2026-11-24 19:35 | breadth-book-1 | L-12@2008 | variant | train | 2008-01-02 | 2025-11-09 | 1.04 | +550.3% | 24.9% | 2.87 |
| 2026-11-24 19:35 | breadth-book-1 | L-20@2008 | variant | train | 2008-01-02 | 2025-11-09 | 0.93 | +294.9% | 20.6% | 2.84 |
| 2026-11-24 19:35 | breadth-book-1 | L-all@2008 | variant | train | 2008-01-02 | 2025-11-09 | 0.75 | +215.7% | 20.7% | 2.67 |
| 2026-11-24 19:35 | breadth-book-1 | six-live-form@2008/ts_momentum | robustness | train | 2008-01-02 | 2025-11-09 | 1.39 | +1371.6% | 20.0% | 4.51 |
| 2026-11-24 19:35 | breadth-book-1 | L-all-live-form@2008/ts_momentum | robustness | train | 2008-01-02 | 2025-11-09 | 0.68 | +164.1% | 15.7% | 5.64 |
| 2026-11-24 19:35 | breadth-book-1 | C-2@2020 | baseline | train | 2020-01-01 | 2025-11-09 | 1.17 | +1814.1% | 57.4% | 2.29 |
| 2026-11-24 19:35 | breadth-book-1 | C-5@2020 | variant | train | 2020-01-01 | 2025-11-09 | 0.91 | +733.7% | 62.7% | 4.44 |
| 2026-11-24 19:35 | breadth-book-1 | C-10@2020 | variant | train | 2020-01-01 | 2025-11-09 | 0.78 | +400.8% | 60.7% | 4.42 |
| 2026-11-24 19:35 | breadth-book-1 | six@2020 | baseline | train | 2020-01-01 | 2025-11-09 | 1.28 | +355.0% | 28.8% | 2.76 |
| 2026-11-24 19:35 | breadth-book-1 | LC-all@2020 | variant | train | 2020-01-01 | 2025-11-09 | 0.84 | +107.3% | 25.8% | 2.93 |
| 2026-11-24 19:35 | breadth-book-1 | LC-all-live-form@2020/ts_momentum | robustness | train | 2020-01-01 | 2025-11-09 | 1.03 | +73.1% | 15.2% | 5.40 |
| 2026-11-24 19:35 | breadth-book-1 | six-live-form@2020/ts_momentum | robustness | train | 2020-01-01 | 2025-11-09 | 1.36 | +196.5% | 20.0% | 4.20 |
| 2026-11-24 19:35 | breadth-book-1 | L-all@2020 | robustness | train | 2020-01-01 | 2025-11-09 | 0.84 | +60.7% | 18.9% | 2.77 |
| 2026-11-24 19:29 | congress-workload | SPY 4-week return on Anscombe roll-call count (session dummy, past-return controls) (b -0.009%/unit, t -0.19, rank 25/41, gate fail) | screen | train | 1994-02-04 | 2025-10-03 | - | - | - | - |
| 2026-11-24 19:29 | refund-runoff | QQQ+IWM+BTC+ETH 4-week return on Nash-cascade runoff of the IRS individual-refund surprise (b +0.281%/unit, t +1.44, rank 7/41, gate fail) | screen | train | 2008-01-04 | 2025-10-03 | - | - | - | - |
| 2026-11-24 19:18 | turbulence | turb | variant | train | 1994-02-01 | 2025-11-09 | 0.95 | +6489.3% | 40.6% | 8.76 |
| 2026-11-24 19:18 | turbulence | corr | variant | train | 1994-02-01 | 2025-11-09 | 0.97 | +10393.3% | 31.4% | 11.48 |
| 2026-11-24 19:18 | turbulence | mag | baseline | train | 1994-02-01 | 2025-11-09 | 1.00 | +8214.7% | 45.0% | 8.51 |
| 2026-11-24 19:18 | turbulence | mag-match | baseline | train | 1994-02-01 | 2025-11-09 | 0.99 | +8131.5% | 45.0% | 8.35 |
| 2026-11-24 19:18 | turbulence | mag-match-c | baseline | train | 1994-02-01 | 2025-11-09 | 1.05 | +11449.5% | 38.9% | 6.63 |
| 2026-11-24 19:18 | turbulence | turb-q75 | robustness | train | 1994-02-01 | 2025-11-09 | 0.89 | +3121.9% | 47.0% | 13.90 |
| 2026-11-24 19:18 | turbulence | mag-match-q75 | baseline | train | 1994-02-01 | 2025-11-09 | 0.90 | +3347.3% | 48.7% | 15.38 |
| 2026-11-24 19:18 | turbulence | turb@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.83 | +4444.8% | 22.1% | 8.45 |
| 2026-11-24 19:18 | turbulence | corr@idx | robustness | train | 1962-01-02 | 2025-11-09 | 0.62 | +2101.7% | 25.7% | 17.55 |
| 2026-11-24 19:18 | turbulence | mag@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.84 | +4662.0% | 20.8% | 8.14 |
| 2026-11-24 19:18 | turbulence | mag-match@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.82 | +4350.3% | 20.8% | 8.13 |
| 2026-11-24 19:18 | turbulence | mag-match-c@idx | baseline | train | 1962-01-02 | 2025-11-09 | 0.86 | +5126.9% | 20.7% | 8.34 |
| 2026-11-24 19:22 | halving-2 | bh@LZ | baseline | train | 2014-04-02 | 2025-11-09 | 0.74 | +1695.7% | 93.0% | 4.49 |
| 2026-11-24 19:22 | halving-2 | tsmom12@LZ | baseline | train | 2014-04-02 | 2025-11-09 | 0.62 | +765.7% | 92.0% | 5.61 |
| 2026-11-24 19:22 | halving-2 | alone-own@LZ | robustness | train | 2014-04-02 | 2025-11-09 | 0.45 | +61.2% | 95.7% | 3.00 |
| 2026-11-24 19:22 | halving-2 | alone-btc@LZ | robustness | train | 2014-04-02 | 2025-11-09 | 1.23 | +323508.0% | 76.9% | 4.50 |
| 2026-11-24 19:22 | halving-2 | and-own@LZ | robustness | train | 2014-04-02 | 2025-11-09 | 0.13 | -62.4% | 96.7% | 4.59 |
| 2026-11-24 19:22 | halving-2 | bh@LTC | baseline | train | 2014-04-02 | 2025-11-09 | 0.68 | +821.4% | 93.6% | 0.01 |
| 2026-11-24 19:22 | halving-2 | tsmom12@LTC | baseline | train | 2014-04-02 | 2025-11-09 | 0.39 | -9.4% | 97.0% | 2.39 |
| 2026-11-24 19:22 | halving-2 | alone-own@LTC | robustness | train | 2014-04-02 | 2025-11-09 | 0.25 | -73.3% | 96.8% | 0.90 |
| 2026-11-24 19:22 | halving-2 | alone-btc@LTC | robustness | train | 2014-04-02 | 2025-11-09 | 1.14 | +162327.4% | 78.3% | 0.59 |
| 2026-11-24 19:22 | halving-2 | bh@ZEC | baseline | train | 2017-10-30 | 2025-11-09 | 0.63 | +114.4% | 97.6% | 0.31 |
| 2026-11-24 19:22 | halving-2 | tsmom12@ZEC | baseline | train | 2017-10-30 | 2025-11-09 | 0.71 | +601.7% | 91.2% | 1.90 |
| 2026-11-24 19:22 | halving-2 | alone-own@ZEC | robustness | train | 2017-10-30 | 2025-11-09 | 0.75 | +622.4% | 96.8% | 0.41 |
| 2026-11-24 19:22 | halving-2 | alone-btc@ZEC | robustness | train | 2017-10-30 | 2025-11-09 | 1.03 | +7015.6% | 78.6% | 1.65 |
| 2026-11-24 19:22 | halving-2 | bh@BCH | baseline | train | 2018-08-02 | 2025-11-09 | 0.45 | -30.1% | 94.2% | 0.30 |
| 2026-11-24 19:22 | halving-2 | tsmom12@BCH | baseline | train | 2018-08-02 | 2025-11-09 | 0.44 | +47.0% | 74.9% | 1.89 |
| 2026-11-24 19:22 | halving-2 | alone-own@BCH | robustness | train | 2018-08-02 | 2025-11-09 | 0.68 | +349.9% | 89.6% | 0.72 |
| 2026-11-24 19:22 | halving-2 | alone-btc@BCH | robustness | train | 2018-08-02 | 2025-11-09 | 0.92 | +2369.9% | 73.8% | 0.58 |
| 2026-11-24 19:22 | halving-2 | bh@BSV | baseline | train | 2019-11-16 | 2025-11-09 | 0.30 | -79.4% | 95.3% | 0.21 |
| 2026-11-24 19:22 | halving-2 | tsmom12@BSV | baseline | train | 2019-11-16 | 2025-11-09 | 0.28 | -48.6% | 83.3% | 2.93 |
| 2026-11-24 19:22 | halving-2 | alone-own@BSV | robustness | train | 2019-11-16 | 2025-11-09 | 0.42 | -40.5% | 84.0% | 0.54 |
| 2026-11-24 19:22 | halving-2 | alone-btc@BSV | robustness | train | 2019-11-16 | 2025-11-09 | 0.45 | -27.5% | 82.3% | 0.50 |
| 2026-11-24 19:22 | halving-2 | bh@ETC | baseline | train | 2017-07-26 | 2025-11-09 | 0.55 | +11.7% | 91.9% | 0.09 |
| 2026-11-24 19:22 | halving-2 | tsmom12@ETC | baseline | train | 2017-07-26 | 2025-11-09 | 0.44 | +8.2% | 90.9% | 2.54 |
| 2026-11-24 19:22 | halving-2 | alone-own@ETC | robustness | train | 2017-07-26 | 2025-11-09 | 0.58 | +125.7% | 91.9% | 0.96 |
| 2026-11-24 19:22 | halving-2 | alone-btc@ETC | robustness | train | 2017-07-26 | 2025-11-09 | 0.86 | +2251.4% | 73.1% | 0.60 |
| 2026-11-24 19:22 | halving-2 | bh@BTC | baseline | train | 2011-07-19 | 2025-11-09 | 1.19 | +760764.5% | 85.0% | 0.00 |
| 2026-11-24 19:22 | halving-2 | tsmom12@BTC | baseline | train | 2011-07-19 | 2025-11-09 | 1.10 | +227428.8% | 85.0% | 0.41 |
| 2026-11-24 19:22 | halving-2 | alone-own@BTC | robustness | train | 2011-07-19 | 2025-11-09 | 1.57 | +30148673.5% | 85.0% | 0.67 |
| 2026-11-24 19:22 | halving-2 | S1 alone-own@LZ own-calendar placebos (Sharpe 0.45, rank 40/41, null SD 0.14, fail) | screen | train | 2014-04-02 | 2025-11-09 | - | - | - | - |
| 2026-11-24 19:22 | halving-2 | S2 alone-btc@LZ BTC-calendar placebos (Sharpe 1.23, rank 1/41, null SD 0.22) | screen | train | 2014-04-02 | 2025-11-09 | - | - | - | - |
| 2026-11-24 19:22 | halving-2 | C2 LZ alt/BTC own window minus outside (+0.402/yr, rank 32/41 most negative; gate fail: BTC-beta) | screen | train | 2014-04-02 | 2025-11-09 | - | - | - | - |
| 2026-11-24 19:22 | halving-2 | BTC alone-own placebos (rank 1/41, shown) | screen | train | 2011-07-19 | 2025-11-09 | - | - | - | - |
| 2026-11-24 19:45 | buy_hold_btc | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.87 | +2294348.3% | 84.9% | 0.00 |
| 2026-11-24 19:45 | buy_hold_btc | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.87 | +2294348.3% | 84.9% | 0.00 |
| 2026-11-24 19:45 | buy_hold_spy | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.63 | +2395.7% | 55.2% | 0.01 |
| 2026-11-24 19:45 | buy_hold_spy | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.63 | +2395.7% | 55.2% | 0.01 |
| 2026-11-24 19:45 | sixty_forty | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.77 | +1123.3% | 30.5% | 0.47 |
| 2026-11-24 19:45 | sixty_forty | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.77 | +1123.3% | 30.5% | 0.47 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +56379.0% | 66.7% | 1.52 |
| 2026-11-24 19:45 | equal_weight | lag-e1-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +56630.0% | 66.7% | 1.54 |
| 2026-11-24 19:45 | equal_weight | lag-e2-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +55763.4% | 66.8% | 1.52 |
| 2026-11-24 19:45 | equal_weight | lag-e5-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.00 | +54598.4% | 66.7% | 1.50 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +56620.6% | 66.7% | 1.52 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +55674.8% | 66.7% | 1.52 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +55452.6% | 66.7% | 1.53 |
| 2026-11-24 19:45 | equal_weight | lag-e1-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +56796.9% | 66.7% | 1.52 |
| 2026-11-24 19:45 | equal_weight | lag-e2-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 1.00 | +54467.4% | 66.8% | 1.52 |
| 2026-11-24 19:45 | equal_weight | lag-e5-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +54614.4% | 66.7% | 1.55 |
| 2026-11-24 19:45 | equal_weight | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +56071.5% | 66.7% | 1.51 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.09 | +5936.8% | 28.4% | 4.31 |
| 2026-11-24 19:45 | ts_momentum | lag-e1-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.12 | +6657.7% | 24.7% | 4.33 |
| 2026-11-24 19:45 | ts_momentum | lag-e2-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.10 | +6190.5% | 25.9% | 4.33 |
| 2026-11-24 19:45 | ts_momentum | lag-e5-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.13 | +7391.7% | 24.6% | 4.34 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 1.09 | +6033.2% | 28.4% | 4.36 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 1.07 | +5715.5% | 28.4% | 4.40 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.07 | +5682.9% | 28.4% | 4.39 |
| 2026-11-24 19:45 | ts_momentum | lag-e1-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 1.11 | +6728.3% | 24.7% | 4.39 |
| 2026-11-24 19:45 | ts_momentum | lag-e2-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 1.08 | +5928.8% | 25.9% | 4.41 |
| 2026-11-24 19:45 | ts_momentum | lag-e5-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.11 | +7127.2% | 24.6% | 4.42 |
| 2026-11-24 19:45 | ts_momentum | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 1.09 | +6028.4% | 28.4% | 4.36 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +570422.0% | 77.6% | 3.66 |
| 2026-11-24 19:45 | xs_momentum | lag-e1-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +574505.0% | 77.7% | 3.78 |
| 2026-11-24 19:45 | xs_momentum | lag-e2-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +559237.6% | 77.7% | 3.79 |
| 2026-11-24 19:45 | xs_momentum | lag-e5-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.93 | +526798.8% | 77.6% | 4.03 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +574511.0% | 77.4% | 3.63 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +537465.7% | 77.8% | 3.63 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 0.93 | +498023.7% | 77.9% | 3.63 |
| 2026-11-24 19:45 | xs_momentum | lag-e1-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +582610.5% | 77.3% | 3.64 |
| 2026-11-24 19:45 | xs_momentum | lag-e2-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +536789.2% | 77.7% | 3.71 |
| 2026-11-24 19:45 | xs_momentum | lag-e5-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 0.92 | +456221.4% | 78.1% | 3.76 |
| 2026-11-24 19:45 | xs_momentum | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.94 | +564160.9% | 77.4% | 3.58 |
| 2026-11-24 19:45 | vol_target_spy | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.74 | +862.9% | 33.4% | 3.93 |
| 2026-11-24 19:45 | vol_target_spy | lag-e1-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.73 | +834.4% | 33.2% | 3.96 |
| 2026-11-24 19:45 | vol_target_spy | lag-e2-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.73 | +849.9% | 34.4% | 3.96 |
| 2026-11-24 19:45 | vol_target_spy | lag-e5-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.73 | +906.6% | 33.0% | 3.96 |
| 2026-11-24 19:45 | vol_target_spy | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.74 | +862.9% | 33.4% | 3.93 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3619.2% | 62.0% | 0.58 |
| 2026-11-24 19:45 | risk_parity | lag-e1-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3601.0% | 62.0% | 0.58 |
| 2026-11-24 19:45 | risk_parity | lag-e2-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3614.4% | 62.1% | 0.61 |
| 2026-11-24 19:45 | risk_parity | lag-e5-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3712.7% | 62.1% | 0.60 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 0.82 | +3566.8% | 62.0% | 0.58 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3649.8% | 62.0% | 0.59 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 0.82 | +3571.3% | 62.0% | 0.57 |
| 2026-11-24 19:45 | risk_parity | lag-e1-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3701.1% | 62.0% | 0.59 |
| 2026-11-24 19:45 | risk_parity | lag-e2-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 0.82 | +3575.6% | 62.1% | 0.59 |
| 2026-11-24 19:45 | risk_parity | lag-e5-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3757.7% | 62.1% | 0.62 |
| 2026-11-24 19:45 | risk_parity | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.83 | +3605.3% | 62.0% | 0.57 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.09 | +6.2% | 39.5% | 6.71 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 0.04 | -16.2% | 58.3% | 6.28 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c2 | robustness | train | 1994-02-01 | 2025-11-09 | -0.05 | -41.6% | 52.4% | 5.16 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 0.27 | +136.6% | 28.7% | 8.67 |
| 2026-11-24 19:45 | crypto_mean_reversion | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.04 | -16.2% | 58.3% | 6.28 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.95 | +1547.3% | 22.0% | 4.76 |
| 2026-11-24 19:45 | preset_careful | lag-e1-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.00 | +1863.7% | 16.5% | 4.81 |
| 2026-11-24 19:45 | preset_careful | lag-e2-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 0.96 | +1677.6% | 17.6% | 4.81 |
| 2026-11-24 19:45 | preset_careful | lag-e5-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +2014.0% | 17.2% | 4.83 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 0.95 | +1578.6% | 22.0% | 4.77 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 0.95 | +1553.1% | 22.0% | 4.77 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 0.96 | +1579.6% | 22.0% | 4.78 |
| 2026-11-24 19:45 | preset_careful | lag-e1-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +1897.3% | 16.5% | 4.81 |
| 2026-11-24 19:45 | preset_careful | lag-e2-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 0.96 | +1685.8% | 17.6% | 4.80 |
| 2026-11-24 19:45 | preset_careful | lag-e5-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +2022.4% | 17.2% | 4.83 |
| 2026-11-24 19:45 | preset_careful | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 0.95 | +1577.9% | 22.0% | 4.77 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.02 | +6244.7% | 30.9% | 4.90 |
| 2026-11-24 19:45 | preset_middle | lag-e1-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.05 | +7291.7% | 27.4% | 4.92 |
| 2026-11-24 19:45 | preset_middle | lag-e2-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.03 | +6659.6% | 28.1% | 4.92 |
| 2026-11-24 19:45 | preset_middle | lag-e5-c0 | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +7770.8% | 27.7% | 4.90 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 1.03 | +6520.8% | 30.9% | 4.89 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 1.01 | +5963.8% | 30.9% | 4.90 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.00 | +5881.1% | 30.9% | 4.91 |
| 2026-11-24 19:45 | preset_middle | lag-e1-c1 | robustness | train | 1994-02-01 | 2025-11-09 | 1.06 | +7608.1% | 27.4% | 4.91 |
| 2026-11-24 19:45 | preset_middle | lag-e2-c2 | robustness | train | 1994-02-01 | 2025-11-09 | 1.02 | +6386.4% | 28.1% | 4.93 |
| 2026-11-24 19:45 | preset_middle | lag-e5-c5 | robustness | train | 1994-02-01 | 2025-11-09 | 1.04 | +7252.3% | 27.7% | 4.91 |
| 2026-11-24 19:45 | preset_middle | sched-0300 | robustness | train | 1994-02-01 | 2025-11-09 | 1.03 | +6521.7% | 30.9% | 4.88 |
| 2026-11-24 19:45 | buy_hold_btc | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.31 | +1975195.7% | 84.9% | 0.00 |
| 2026-11-24 19:45 | buy_hold_btc | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.31 | +2131456.4% | 84.9% | 0.00 |
| 2026-11-24 19:45 | buy_hold_spy | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.91 | +580.8% | 33.7% | 0.02 |
| 2026-11-24 19:45 | buy_hold_spy | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.91 | +580.8% | 33.7% | 0.02 |
| 2026-11-24 19:45 | sixty_forty | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.93 | +256.9% | 27.3% | 0.49 |
| 2026-11-24 19:45 | sixty_forty | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.93 | +256.9% | 27.3% | 0.49 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +10186.9% | 47.7% | 1.55 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +10232.6% | 47.8% | 1.55 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.44 | +10173.8% | 47.7% | 1.53 |
| 2026-11-24 19:45 | equal_weight | lag-e0-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +10200.0% | 47.6% | 1.57 |
| 2026-11-24 19:45 | equal_weight | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +10352.0% | 47.7% | 1.54 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.57 | +1042.2% | 20.1% | 4.45 |
| 2026-11-24 19:45 | ts_momentum | lag-e1-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.59 | +1085.5% | 21.9% | 4.47 |
| 2026-11-24 19:45 | ts_momentum | lag-e2-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.56 | +1030.5% | 21.3% | 4.46 |
| 2026-11-24 19:45 | ts_momentum | lag-e5-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.57 | +1090.2% | 21.5% | 4.46 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.55 | +1054.3% | 20.0% | 4.51 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.51 | +994.5% | 19.9% | 4.56 |
| 2026-11-24 19:45 | ts_momentum | lag-e0-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.50 | +990.5% | 20.3% | 4.55 |
| 2026-11-24 19:45 | ts_momentum | lag-e1-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.57 | +1088.2% | 20.0% | 4.52 |
| 2026-11-24 19:45 | ts_momentum | lag-e2-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.50 | +980.9% | 20.6% | 4.56 |
| 2026-11-24 19:45 | ts_momentum | lag-e5-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.50 | +1045.5% | 20.6% | 4.56 |
| 2026-11-24 19:45 | ts_momentum | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.55 | +1053.8% | 20.0% | 4.51 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.29 | +121944.4% | 77.7% | 3.65 |
| 2026-11-24 19:45 | xs_momentum | lag-e1-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.29 | +122910.3% | 77.6% | 3.75 |
| 2026-11-24 19:45 | xs_momentum | lag-e2-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.29 | +122770.0% | 77.6% | 3.79 |
| 2026-11-24 19:45 | xs_momentum | lag-e5-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.29 | +122590.6% | 77.5% | 4.03 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.29 | +123228.8% | 77.4% | 3.61 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.28 | +115184.6% | 77.9% | 3.64 |
| 2026-11-24 19:45 | xs_momentum | lag-e0-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.27 | +106096.0% | 78.1% | 3.63 |
| 2026-11-24 19:45 | xs_momentum | lag-e2-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.28 | +115685.3% | 77.9% | 3.70 |
| 2026-11-24 19:45 | xs_momentum | lag-e5-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.27 | +106309.4% | 77.9% | 3.76 |
| 2026-11-24 19:45 | xs_momentum | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.29 | +120494.3% | 77.5% | 3.60 |
| 2026-11-24 19:45 | vol_target_spy | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.00 | +280.1% | 13.3% | 3.87 |
| 2026-11-24 19:45 | vol_target_spy | lag-e1-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.94 | +257.3% | 12.9% | 3.89 |
| 2026-11-24 19:45 | vol_target_spy | lag-e2-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.96 | +274.3% | 14.1% | 3.90 |
| 2026-11-24 19:45 | vol_target_spy | lag-e5-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.93 | +275.0% | 15.5% | 3.89 |
| 2026-11-24 19:45 | vol_target_spy | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.00 | +280.1% | 13.3% | 3.87 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.43 | +760.7% | 29.9% | 0.60 |
| 2026-11-24 19:45 | risk_parity | lag-e1-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.41 | +741.3% | 29.5% | 0.60 |
| 2026-11-24 19:45 | risk_parity | lag-e2-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.43 | +756.1% | 29.8% | 0.63 |
| 2026-11-24 19:45 | risk_parity | lag-e5-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.41 | +745.4% | 29.9% | 0.60 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +748.3% | 29.8% | 0.59 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +746.9% | 29.8% | 0.60 |
| 2026-11-24 19:45 | risk_parity | lag-e0-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.41 | +739.6% | 30.0% | 0.58 |
| 2026-11-24 19:45 | risk_parity | lag-e1-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +758.0% | 29.9% | 0.61 |
| 2026-11-24 19:45 | risk_parity | lag-e2-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.43 | +759.4% | 29.6% | 0.61 |
| 2026-11-24 19:45 | risk_parity | lag-e5-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +743.9% | 29.7% | 0.62 |
| 2026-11-24 19:45 | risk_parity | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +751.7% | 30.0% | 0.58 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.14 | +6.2% | 39.5% | 15.11 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.07 | -16.2% | 58.3% | 14.58 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | -0.07 | -41.6% | 52.4% | 13.99 |
| 2026-11-24 19:45 | crypto_mean_reversion | lag-e0-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.41 | +136.6% | 28.7% | 16.20 |
| 2026-11-24 19:45 | crypto_mean_reversion | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 0.07 | -16.2% | 58.3% | 14.59 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.25 | +236.3% | 12.4% | 5.01 |
| 2026-11-24 19:45 | preset_careful | lag-e1-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.28 | +247.7% | 10.7% | 5.05 |
| 2026-11-24 19:45 | preset_careful | lag-e2-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.23 | +232.5% | 10.7% | 5.04 |
| 2026-11-24 19:45 | preset_careful | lag-e5-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.22 | +246.2% | 12.4% | 5.06 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.27 | +242.8% | 12.2% | 5.02 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.26 | +238.3% | 12.2% | 5.01 |
| 2026-11-24 19:45 | preset_careful | lag-e0-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.27 | +243.1% | 12.2% | 5.03 |
| 2026-11-24 19:45 | preset_careful | lag-e1-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.29 | +253.9% | 10.7% | 5.05 |
| 2026-11-24 19:45 | preset_careful | lag-e2-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.23 | +233.9% | 10.7% | 5.02 |
| 2026-11-24 19:45 | preset_careful | lag-e5-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.22 | +247.6% | 12.2% | 5.06 |
| 2026-11-24 19:45 | preset_careful | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.27 | +242.6% | 12.2% | 5.02 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.41 | +1156.9% | 23.7% | 5.11 |
| 2026-11-24 19:45 | preset_middle | lag-e1-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.42 | +1218.7% | 25.3% | 5.12 |
| 2026-11-24 19:45 | preset_middle | lag-e2-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.40 | +1149.3% | 24.8% | 5.13 |
| 2026-11-24 19:45 | preset_middle | lag-e5-c0@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.41 | +1224.1% | 25.3% | 5.11 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.43 | +1212.1% | 23.9% | 5.10 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.38 | +1098.4% | 24.5% | 5.13 |
| 2026-11-24 19:45 | preset_middle | lag-e0-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.37 | +1082.9% | 23.8% | 5.13 |
| 2026-11-24 19:45 | preset_middle | lag-e1-c1@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.45 | +1285.6% | 24.2% | 5.11 |
| 2026-11-24 19:45 | preset_middle | lag-e2-c2@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.36 | +1085.5% | 26.5% | 5.15 |
| 2026-11-24 19:45 | preset_middle | lag-e5-c5@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.38 | +1143.2% | 25.9% | 5.13 |
| 2026-11-24 19:45 | preset_middle | sched-0300@coin | robustness | train | 2012-01-02 | 2025-11-09 | 1.43 | +1214.0% | 24.0% | 5.09 |
| 2026-11-24 19:48 | cost-band | band05 | variant | train | 1994-02-01 | 2025-11-09 | 1.09 | +22368.9% | 32.5% | 2.06 |
| 2026-11-24 19:48 | cost-band | band05/bills | robustness | train | 1994-02-01 | 2025-11-09 | 1.13 | +26578.8% | 31.1% | 2.04 |
| 2026-11-24 19:48 | cost-band | band02 | variant | train | 1994-02-01 | 2025-11-09 | 1.06 | +19426.3% | 36.1% | 2.44 |
| 2026-11-24 19:48 | cost-band | band02/bills | robustness | train | 1994-02-01 | 2025-11-09 | 1.09 | +22485.7% | 35.2% | 2.43 |
| 2026-11-24 19:48 | cost-band | band05@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.56 | +234.6% | 91.7% | 3.27 |
| 2026-11-24 19:48 | cost-band | band02@coin | robustness | train | 2017-08-18 | 2025-11-09 | 0.53 | +165.3% | 92.5% | 4.09 |
| 2026-11-24 19:52 | cost-band | ceiling: `tsmom12` with coin fills free (not tradable; step 1b, `lib/wide16_ceiling.py`): +0.0103, SE 0.0017, z 6.0; drift costs only +0.0085, z 10.0 | note | train | 1994-02-01 | 2025-11-09 | - | - | - | - |
| 2026-11-24 19:52 | cost-band | post hoc split (`lib/wide16_posthoc.py`, not a try): band05 +0.049 = drift bet +0.054 (coin fills free) + fees/tiers -0.005; coin share while held 0.274 vs 0.273 | note | train | 1994-02-01 | 2025-11-09 | - | - | - | - |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-overlay@US-ind10 | robustness | train | 1945-07-25 | 2025-11-09 | 0.83 | +5654.2% | 19.1% | 5.31 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-alone@US-ind10 | robustness | train | 1945-07-25 | 2025-11-09 | 0.73 | +16610.6% | 35.3% | 5.47 |
| 2026-11-24 19:48 | seasonal-20y | tsmom12@US-ind10 | robustness | train | 1945-07-25 | 2025-11-09 | 0.98 | +190644.3% | 30.1% | 2.73 |
| 2026-11-24 19:48 | seasonal-20y | hold@US-ind10 | robustness | train | 1945-07-25 | 2025-11-09 | 0.86 | +843652.9% | 52.4% | 0.20 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-overlay@US-Mkt | robustness | train | 1945-07-25 | 2025-11-09 | 0.48 | +1982.7% | 31.0% | 4.60 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-alone@US-Mkt | robustness | train | 1945-07-25 | 2025-11-09 | 0.48 | +4762.1% | 39.3% | 4.99 |
| 2026-11-24 19:48 | seasonal-20y | tsmom12@US-Mkt | robustness | train | 1945-07-25 | 2025-11-09 | 0.86 | +185980.7% | 32.3% | 1.25 |
| 2026-11-24 19:48 | seasonal-20y | hold@US-Mkt | robustness | train | 1945-07-25 | 2025-11-09 | 0.78 | +584882.4% | 54.6% | 0.00 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-overlay@US-NoDur | robustness | train | 1945-07-25 | 2025-11-09 | 0.67 | +5000.0% | 36.0% | 5.74 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-alone@US-NoDur | robustness | train | 1945-07-25 | 2025-11-09 | 0.65 | +11233.7% | 43.0% | 5.27 |
| 2026-11-24 19:48 | seasonal-20y | tsmom12@US-NoDur | robustness | train | 1945-07-25 | 2025-11-09 | 0.90 | +144248.0% | 35.5% | 3.03 |
| 2026-11-24 19:48 | seasonal-20y | hold@US-NoDur | robustness | train | 1945-07-25 | 2025-11-09 | 0.89 | +582613.7% | 54.0% | 0.00 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-overlay@US-Durbl | robustness | train | 1945-07-25 | 2025-11-09 | 0.56 | +11704.6% | 48.4% | 4.80 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-alone@US-Durbl | robustness | train | 1945-07-25 | 2025-11-09 | 0.44 | +11499.3% | 67.6% | 5.15 |
| 2026-11-24 19:48 | seasonal-20y | tsmom12@US-Durbl | robustness | train | 1945-07-25 | 2025-11-09 | 0.56 | +77320.9% | 72.5% | 3.32 |
| 2026-11-24 19:48 | seasonal-20y | hold@US-Durbl | robustness | train | 1945-07-25 | 2025-11-09 | 0.57 | +503970.9% | 78.5% | 0.00 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-overlay@US-Manuf | robustness | train | 1945-07-25 | 2025-11-09 | 0.60 | +4767.2% | 34.9% | 4.81 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-alone@US-Manuf | robustness | train | 1945-07-25 | 2025-11-09 | 0.61 | +17885.5% | 46.2% | 5.00 |
| 2026-11-24 19:48 | seasonal-20y | tsmom12@US-Manuf | robustness | train | 1945-07-25 | 2025-11-09 | 0.76 | +101259.6% | 41.0% | 2.28 |
| 2026-11-24 19:48 | seasonal-20y | hold@US-Manuf | robustness | train | 1945-07-25 | 2025-11-09 | 0.74 | +559070.7% | 58.5% | 0.00 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-overlay@US-Enrgy | robustness | train | 1945-07-25 | 2025-11-09 | 0.41 | +2220.8% | 54.8% | 5.61 |
| 2026-11-24 19:48 | seasonal-20y | seasonal-20y-alone@US-Enrgy | robustness | train | 1945-07-25 | 2025-11-09 | 0.47 | +10285.9% | 63.0% | 5.37 |
| 2026-11-24 19:48 | seasonal-20y | tsmom12@US-Enrgy | robustness | train | 1945-07-25 | 2025-11-09 | 0.65 | +136518.7% | 44.0% | 3.24 |
| 2026-11-24 19:48 | seasonal-20y | hold@US-Enrgy | robustness | train | 1945-07-25 | 2025-11-09 | 0.64 | +769953.3% | 72.1% | 0.00 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@US-HiTec | robustness | train | 1945-07-25 | 2025-11-09 | 0.49 | +5839.4% | 36.0% | 5.16 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@US-HiTec | robustness | train | 1945-07-25 | 2025-11-09 | 0.52 | +22922.1% | 65.2% | 5.41 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@US-HiTec | robustness | train | 1945-07-25 | 2025-11-09 | 0.69 | +337743.9% | 44.0% | 1.57 |
| 2026-11-24 19:49 | seasonal-20y | hold@US-HiTec | robustness | train | 1945-07-25 | 2025-11-09 | 0.66 | +1371734.8% | 82.2% | 0.00 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@US-Telcm | robustness | train | 1945-07-25 | 2025-11-09 | 0.58 | +3441.7% | 29.8% | 4.49 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@US-Telcm | robustness | train | 1945-07-25 | 2025-11-09 | 0.45 | +3928.4% | 66.0% | 5.08 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@US-Telcm | robustness | train | 1945-07-25 | 2025-11-09 | 0.75 | +71279.2% | 30.8% | 2.46 |
| 2026-11-24 19:49 | seasonal-20y | hold@US-Telcm | robustness | train | 1945-07-25 | 2025-11-09 | 0.62 | +107068.4% | 73.7% | 0.00 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@US-Shops | robustness | train | 1945-07-25 | 2025-11-09 | 0.57 | +4415.8% | 37.9% | 5.27 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@US-Shops | robustness | train | 1945-07-25 | 2025-11-09 | 0.55 | +10539.8% | 65.6% | 5.32 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@US-Shops | robustness | train | 1945-07-25 | 2025-11-09 | 0.80 | +164085.4% | 52.4% | 1.13 |
| 2026-11-24 19:49 | seasonal-20y | hold@US-Shops | robustness | train | 1945-07-25 | 2025-11-09 | 0.80 | +1005184.3% | 60.9% | 0.00 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@US-Hlth | robustness | train | 1945-07-25 | 2025-11-09 | 0.51 | +3395.6% | 38.6% | 5.34 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@US-Hlth | robustness | train | 1945-07-25 | 2025-11-09 | 0.58 | +12908.1% | 37.7% | 5.12 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@US-Hlth | robustness | train | 1945-07-25 | 2025-11-09 | 0.79 | +222954.1% | 36.2% | 2.68 |
| 2026-11-24 19:49 | seasonal-20y | hold@US-Hlth | robustness | train | 1945-07-25 | 2025-11-09 | 0.83 | +1776031.5% | 48.2% | 0.00 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@US-Utils | robustness | train | 1945-07-25 | 2025-11-09 | 0.67 | +3519.9% | 22.5% | 6.20 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@US-Utils | robustness | train | 1945-07-25 | 2025-11-09 | 0.64 | +10432.4% | 35.5% | 6.55 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@US-Utils | robustness | train | 1945-07-25 | 2025-11-09 | 0.92 | +107501.9% | 30.3% | 2.26 |
| 2026-11-24 19:49 | seasonal-20y | hold@US-Utils | robustness | train | 1945-07-25 | 2025-11-09 | 0.82 | +306809.5% | 45.7% | 0.00 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@US-Other | robustness | train | 1945-07-25 | 2025-11-09 | 0.59 | +4459.2% | 42.0% | 5.01 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@US-Other | robustness | train | 1945-07-25 | 2025-11-09 | 0.55 | +14015.2% | 59.1% | 5.45 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@US-Other | robustness | train | 1945-07-25 | 2025-11-09 | 0.76 | +93858.2% | 34.7% | 2.16 |
| 2026-11-24 19:49 | seasonal-20y | hold@US-Other | robustness | train | 1945-07-25 | 2025-11-09 | 0.66 | +314648.9% | 72.0% | 0.00 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@US-ind10-late | robustness | train | 1945-07-25 | 2025-11-09 | 0.75 | +4050.8% | 25.2% | 5.29 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@US-ind10-late | robustness | train | 1945-07-25 | 2025-11-09 | 0.70 | +13896.6% | 35.6% | 5.46 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@US-ind10-late | robustness | train | 1945-07-25 | 2025-11-09 | 0.94 | +143864.7% | 30.7% | 2.71 |
| 2026-11-24 19:49 | seasonal-20y | hold@US-ind10-late | robustness | train | 1945-07-25 | 2025-11-09 | 0.86 | +859593.2% | 52.3% | 0.20 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo13 | robustness | train | 1984-01-25 | 2025-11-09 | 0.47 | +219.9% | 33.9% | 4.49 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo13 | robustness | train | 1984-01-25 | 2025-11-09 | 0.25 | +150.4% | 62.4% | 5.42 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo13 | robustness | train | 1984-01-25 | 2025-11-09 | 0.48 | +521.1% | 41.6% | 2.44 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo13 | robustness | train | 1984-01-25 | 2025-11-09 | 0.31 | +407.2% | 72.2% | 0.20 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Japan | robustness | train | 1984-01-25 | 2025-11-09 | 0.45 | +377.5% | 38.4% | 3.83 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Japan | robustness | train | 1984-01-25 | 2025-11-09 | 0.16 | +66.5% | 74.7% | 4.65 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Japan | robustness | train | 1984-01-25 | 2025-11-09 | 0.49 | +1061.8% | 40.8% | 2.26 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Japan | robustness | train | 1984-01-25 | 2025-11-09 | 0.29 | +417.1% | 81.9% | 0.01 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Canada | robustness | train | 1998-06-24 | 2025-11-09 | 0.22 | +52.4% | 34.9% | 4.74 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Canada | robustness | train | 1998-06-24 | 2025-11-09 | 0.21 | +73.2% | 45.3% | 5.32 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Canada | robustness | train | 1998-06-24 | 2025-11-09 | 0.32 | +130.4% | 34.1% | 2.57 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Canada | robustness | train | 1998-06-24 | 2025-11-09 | 0.39 | +309.7% | 50.0% | 0.02 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-UK | robustness | train | 2003-01-25 | 2025-11-09 | 0.24 | +44.5% | 22.4% | 6.17 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-UK | robustness | train | 2003-01-25 | 2025-11-09 | 0.35 | +135.2% | 33.7% | 6.43 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-UK | robustness | train | 2003-01-25 | 2025-11-09 | 0.21 | +45.7% | 34.3% | 3.05 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-UK | robustness | train | 2003-01-25 | 2025-11-09 | 0.34 | +172.3% | 47.8% | 0.02 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Australia | robustness | train | 2003-08-25 | 2025-11-09 | 0.34 | +59.1% | 24.1% | 6.40 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Australia | robustness | train | 2003-08-25 | 2025-11-09 | 0.40 | +129.2% | 38.0% | 7.74 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Australia | robustness | train | 2003-08-25 | 2025-11-09 | 0.38 | +112.4% | 30.1% | 2.66 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Australia | robustness | train | 2003-08-25 | 2025-11-09 | 0.38 | +186.5% | 54.6% | 0.03 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-HongKong | robustness | train | 2005-12-25 | 2025-11-09 | 0.22 | +39.9% | 30.8% | 5.90 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-HongKong | robustness | train | 2005-12-25 | 2025-11-09 | 0.33 | +130.8% | 41.3% | 7.48 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-HongKong | robustness | train | 2005-12-25 | 2025-11-09 | 0.25 | +70.7% | 44.9% | 2.97 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-HongKong | robustness | train | 2005-12-25 | 2025-11-09 | 0.24 | +74.1% | 65.2% | 0.03 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Germany | robustness | train | 2006-12-25 | 2025-11-09 | 0.15 | +21.7% | 36.0% | 5.34 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Germany | robustness | train | 2006-12-25 | 2025-11-09 | 0.38 | +151.9% | 47.6% | 6.00 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Germany | robustness | train | 2006-12-25 | 2025-11-09 | 0.22 | +48.0% | 51.9% | 2.05 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Germany | robustness | train | 2006-12-25 | 2025-11-09 | 0.43 | +263.1% | 54.8% | 0.03 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Singapore | robustness | train | 2006-12-25 | 2025-11-09 | 0.40 | +63.7% | 26.0% | 4.98 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Singapore | robustness | train | 2006-12-25 | 2025-11-09 | 0.36 | +101.1% | 45.2% | 6.23 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Singapore | robustness | train | 2006-12-25 | 2025-11-09 | 0.22 | +36.3% | 26.0% | 2.95 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Singapore | robustness | train | 2006-12-25 | 2025-11-09 | 0.21 | +48.3% | 62.4% | 0.05 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-France | robustness | train | 2009-03-25 | 2025-11-09 | 0.14 | +16.9% | 20.3% | 5.35 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-France | robustness | train | 2009-03-25 | 2025-11-09 | 0.34 | +89.9% | 38.6% | 5.45 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-France | robustness | train | 2009-03-25 | 2025-11-09 | 0.04 | -6.5% | 35.8% | 2.81 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-France | robustness | train | 2009-03-25 | 2025-11-09 | 0.41 | +174.4% | 38.6% | 0.03 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Switzerland | robustness | train | 2009-11-24 | 2025-11-09 | -0.01 | -5.6% | 28.7% | 5.62 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Switzerland | robustness | train | 2009-11-24 | 2025-11-09 | 0.30 | +50.3% | 20.4% | 5.34 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Switzerland | robustness | train | 2009-11-24 | 2025-11-09 | 0.02 | -6.2% | 36.9% | 4.41 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Switzerland | robustness | train | 2009-11-24 | 2025-11-09 | 0.34 | +88.2% | 31.2% | 0.04 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Belgium | robustness | train | 2010-04-24 | 2025-11-09 | 0.20 | +19.5% | 14.6% | 4.14 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Belgium | robustness | train | 2010-04-24 | 2025-11-09 | 0.23 | +36.7% | 37.6% | 5.92 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Belgium | robustness | train | 2010-04-24 | 2025-11-09 | 0.21 | +32.9% | 36.5% | 2.15 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Belgium | robustness | train | 2010-04-24 | 2025-11-09 | 0.32 | +91.4% | 39.8% | 0.05 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Netherlands | robustness | train | 2011-10-25 | 2025-11-09 | 0.61 | +95.7% | 14.1% | 5.72 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Netherlands | robustness | train | 2011-10-25 | 2025-11-09 | 0.63 | +167.1% | 27.5% | 5.93 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Netherlands | robustness | train | 2011-10-25 | 2025-11-09 | 0.32 | +56.4% | 28.7% | 2.82 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Netherlands | robustness | train | 2011-10-25 | 2025-11-09 | 0.58 | +221.6% | 35.8% | 0.04 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Austria | robustness | train | 2011-11-24 | 2025-11-09 | 0.02 | -2.9% | 33.7% | 3.87 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Austria | robustness | train | 2011-11-24 | 2025-11-09 | 0.32 | +66.4% | 50.7% | 4.62 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Austria | robustness | train | 2011-11-24 | 2025-11-09 | 0.15 | +16.1% | 38.8% | 2.57 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Austria | robustness | train | 2011-11-24 | 2025-11-09 | 0.44 | +159.2% | 55.8% | 0.05 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay@geo-Spain | robustness | train | 2012-07-25 | 2025-11-09 | 0.20 | +20.3% | 29.0% | 4.71 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone@geo-Spain | robustness | train | 2012-07-25 | 2025-11-09 | 0.11 | +8.1% | 43.8% | 6.07 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12@geo-Spain | robustness | train | 2012-07-25 | 2025-11-09 | 0.30 | +48.1% | 36.5% | 2.21 |
| 2026-11-24 19:49 | seasonal-20y | hold@geo-Spain | robustness | train | 2012-07-25 | 2025-11-09 | 0.43 | +137.3% | 48.5% | 0.05 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-overlay | variant | train | 1994-02-01 | 2025-11-09 | 0.87 | +4608.3% | 41.9% | 4.31 |
| 2026-11-24 19:49 | seasonal-20y | seasonal-20y-alone | variant | train | 1994-02-01 | 2025-11-09 | 0.81 | +7486.9% | 50.8% | 4.53 |
| 2026-11-24 19:49 | seasonal-20y | tsmom12 | baseline | train | 1994-02-01 | 2025-11-09 | 1.04 | +18044.5% | 37.4% | 2.81 |
| 2026-11-24 19:49 | seasonal-20y | hold | baseline | train | 1994-02-01 | 2025-11-09 | 0.88 | +20054.9% | 68.8% | 1.46 |
| 2026-11-24 20:17 | alpha-form | stored record re-scored in alpha form (residual IR on the same universe's `tsmom12`, NW/bootstrap z, best long-only mix): 341 distinct selectable series, 0 at z >= 4.69, 2 at >= 3.29 (fm-bolt-base-tilt 4.31: pretraining memory; merfx7 4.14: cash earns 0); median mix gain +0.010; a lens, no new try (research/alpha-form-1.md) | note | - | - | - | - | - | - | - |
| 2026-11-24 20:01 | power-map | power map of strategy classes vs the bar (z 4.69): edge needed at 80% power C1 six assets +0.51, US 1927 +0.29, 13 markets pooled (Y_eff 191) +0.21, C2 +0.79 (ETFs/coins), +0.34 (Ken French at the long-only rho 0.84; long-short near rho 0: +0.85), C3 daily +0.72, C4 +0.43, C5 +3.03; alpha form IR 0.43-2.40; chance a top-plausible edge passes <= 0.02 where known; forward d +0.10 needs 72+ years; no backtest (research/power-map-1.md) | note | - | - | - | - | - | - | - |
| 2026-11-24 20:30 | coin-drift-run | k06@cm (cointop-1 coin book, band 0.06 of the slot) | baseline | train | 2019-04-07 | 2025-11-10 | 0.69 | +337.3% | 63.9% | 7.61 |
| 2026-11-24 20:30 | coin-drift-run | band05@cm (band 0.30 of the slot) | robustness | train | 2019-04-07 | 2025-11-10 | 0.72 | +373.9% | 60.6% | 5.03 |
| 2026-11-24 20:30 | coin-drift-run | band02@cm (band 0.12 of the slot) | robustness | train | 2019-04-07 | 2025-11-10 | 0.70 | +351.2% | 62.9% | 6.40 |
| 2026-11-24 20:30 | coin-drift-run | k06@cm placebo P1 (median of 40 shuffles; mean Sharpe 0.66) | control | train | 2019-04-07 | 2025-11-10 | 0.66 | +286.1% | 62.2% | 7.49 |
| 2026-11-24 20:30 | coin-drift-run | band02@cm placebo P1 (median of 40 shuffles; mean Sharpe 0.67) | control | train | 2019-04-07 | 2025-11-10 | 0.67 | +298.3% | 62.4% | 6.51 |
| 2026-11-24 20:30 | coin-drift-run | band05@cm placebo P1 (median of 40 shuffles; mean Sharpe 0.68) | control | train | 2019-04-07 | 2025-11-10 | 0.69 | +309.5% | 61.0% | 5.10 |
| 2026-11-24 20:30 | coin-drift-run | k06@cm placebo P2 (median of 40 shuffles; mean Sharpe 0.47) | control | train | 2019-04-07 | 2025-11-10 | 0.56 | +180.4% | 58.0% | 8.78 |
| 2026-11-24 20:30 | coin-drift-run | band02@cm placebo P2 (median of 40 shuffles; mean Sharpe 0.49) | control | train | 2019-04-07 | 2025-11-10 | 0.58 | +196.3% | 56.9% | 7.41 |
| 2026-11-24 20:30 | coin-drift-run | band05@cm placebo P2 (median of 40 shuffles; mean Sharpe 0.50) | control | train | 2019-04-07 | 2025-11-10 | 0.59 | +202.1% | 57.7% | 5.33 |
| 2026-11-24 20:32 | coin-drift-run | costs-at-zero split (same run, not a try): band05@cm net +0.033 (z 1.80) = drift with all coin costs zero +0.014 (z 0.71) + fees and tiers +0.019; band02@cm +0.011 = +0.005 + 0.006; excess over placebo P1 +0.009 (z 0.83) / +0.002 (z 0.62), over P2 +0.009 (z 0.54) / -0.001 (z -0.35); Turnover/yr in this idea's rows = traded value x equity a year, both sides | note | train | 2019-04-07 | 2025-11-10 | - | - | - | - |
| 2026-11-24 20:25 | data-long-3 | data lane: keyless long rates/FX/commodity panel cached (US bonds 1962-, 9 foreign 10y 1955-89-, 9 FX with carry 1971-, 12 PPI commodity indices 1913-47-); bonds vs IEF/TLT/SHY corr 0.97-0.99, FX spot vs trusts 0.99, spot oil vs USO +10 pts/yr; no strategy run (research/data-long-3.md) | note | train | 1913-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-24 20:57 | insure-3 | hold-spx-tr@insure3 | baseline | train | 1986-06-30 | 2025-10-31 | 0.67 | +6242.2% | 55.3% | - |
| 2026-11-24 20:57 | insure-3 | tsmom12-spx-tr-bills@insure3 | robustness | train | 1986-06-30 | 2025-10-31 | 0.80 | +5457.0% | 33.0% | 1.12 |
| 2026-11-24 20:57 | insure-3 | tsmom12-spx-tr-cash0@insure3 | robustness | train | 1986-06-30 | 2025-10-31 | 0.76 | +4452.0% | 34.3% | 1.12 |
| 2026-11-24 20:57 | insure-3 | cboe-pput@insure3 | baseline | train | 1986-06-30 | 2025-10-31 | 0.63 | +1952.2% | 42.0% | 12.00 |
| 2026-11-24 20:57 | insure-3 | mix50-tsmom12-pput-bills@insure3 | robustness | train | 1986-06-30 | 2025-10-31 | 0.77 | +3388.5% | 28.6% | - |
| 2026-11-24 20:57 | insure-3 | mix50-tsmom12-pput-cash0@insure3 | robustness | train | 1986-06-30 | 2025-10-31 | 0.75 | +3057.1% | 29.1% | - |
| 2026-11-24 20:57 | insure-3 | cboe-put@insure3 | baseline | train | 2007-01-31 | 2025-10-31 | 0.54 | +245.6% | 37.1% | 12.00 |
| 2026-11-24 20:57 | insure-3 | cboe-bxm@insure3 | baseline | train | 2002-03-28 | 2025-10-31 | 0.48 | +278.2% | 40.1% | 12.00 |
| 2026-11-24 20:57 | insure-3 | cboe-cll@insure3 | baseline | train | 2008-08-29 | 2025-10-31 | 0.58 | +210.6% | 25.5% | 12.00 |
| 2026-11-24 20:57 | insure-3 | cboe-vxth@insure3 | baseline | train | 2006-03-31 | 2025-10-31 | 0.67 | +580.8% | 43.3% | 12.00 |
| 2026-11-24 20:57 | pooled-2 | e4@pooled2-nonequity-21 (pooled dSharpe vs tsmom12 +0.010, SE 0.030, z +0.33; still open) | variant | train | 1956-03-01 | 2025-10-31 | 0.30 | - | - | - |
| 2026-11-24 20:57 | pooled-2 | e4@pooled2-com-8 (pooled dSharpe vs tsmom12 -0.019, SE 0.022, z -0.86; killed (shown, not judged)) | variant | train | 1927-04-01 | 2025-10-01 | 0.34 | - | - | - |
| 2026-11-24 20:57 | pooled-2 | e4@pooled2-combined-62 (pooled dSharpe vs tsmom12 +0.045, SE 0.032, z +1.43; unsettled, leaning positive) | variant | train | 1927-07-08 | 2025-10-31 | 0.46 | - | - | - |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@pooled2-nonequity-21 (pooled dSharpe vs tsmom12 -0.010, SE 0.017, z -0.57; killed) | variant | train | 1956-03-01 | 2025-10-31 | 0.28 | - | - | - |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@pooled2-com-8 (pooled dSharpe vs tsmom12 +0.056, SE 0.026, z +2.15; still open (shown, not judged)) | variant | train | 1927-04-01 | 2025-10-01 | 0.42 | - | - | - |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@pooled2-combined-62 (pooled dSharpe vs tsmom12 +0.011, SE 0.012, z +0.89; equity-only at best) | variant | train | 1927-07-08 | 2025-10-31 | 0.42 | - | - | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@USB3-UST2 | robustness | train | 1977-06-10 | 2025-10-31 | 0.61 | +64.8% | 5.7% | 2.46 |
| 2026-11-24 20:57 | pooled-2 | e4@USB3-UST2 | robustness | train | 1977-06-10 | 2025-10-31 | 0.63 | +59.8% | 5.1% | 4.81 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@USB3-UST2 | robustness | train | 1977-06-10 | 2025-10-31 | 0.60 | +42.9% | 4.0% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@USB3-UST10 | robustness | train | 1963-01-18 | 2025-10-31 | 0.41 | +272.1% | 16.4% | 2.18 |
| 2026-11-24 20:57 | pooled-2 | e4@USB3-UST10 | robustness | train | 1963-01-18 | 2025-10-31 | 0.36 | +177.8% | 14.9% | 5.30 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@USB3-UST10 | robustness | train | 1963-01-18 | 2025-10-31 | 0.39 | +96.1% | 11.4% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@USB3-UST30 | robustness | train | 1978-03-03 | 2025-10-31 | 0.31 | +262.2% | 37.4% | 2.35 |
| 2026-11-24 20:57 | pooled-2 | e4@USB3-UST30 | robustness | train | 1978-03-03 | 2025-10-31 | 0.34 | +269.0% | 29.2% | 5.46 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@USB3-UST30 | robustness | train | 1978-03-03 | 2025-10-31 | 0.40 | +204.3% | 25.9% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-JP | robustness | train | 1990-03-01 | 2025-09-01 | 0.45 | +70.7% | 10.5% | 1.18 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-JP | robustness | train | 1990-03-01 | 2025-09-01 | 0.32 | +41.1% | 10.0% | 2.26 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-JP | robustness | train | 1990-03-01 | 2025-09-01 | 0.43 | +51.6% | 10.0% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-GB | robustness | train | 1961-03-01 | 2025-09-01 | 0.16 | +52.7% | 29.5% | 1.11 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-GB | robustness | train | 1961-03-01 | 2025-09-01 | 0.11 | +25.8% | 26.3% | 2.34 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-GB | robustness | train | 1961-03-01 | 2025-09-01 | 0.23 | +53.8% | 16.0% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-CH | robustness | train | 1973-03-01 | 2025-08-01 | 0.53 | +188.9% | 12.5% | 1.05 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-CH | robustness | train | 1973-03-01 | 2025-08-01 | 0.56 | +176.3% | 12.1% | 2.48 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-CH | robustness | train | 1973-03-01 | 2025-08-01 | 0.53 | +117.7% | 9.9% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-CA | robustness | train | 1956-03-01 | 2025-09-01 | 0.30 | +115.0% | 17.5% | 0.92 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-CA | robustness | train | 1956-03-01 | 2025-09-01 | 0.20 | +56.1% | 20.3% | 2.30 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-CA | robustness | train | 1956-03-01 | 2025-09-01 | 0.27 | +50.3% | 12.2% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-DE | robustness | train | 1957-07-01 | 2025-09-01 | 0.58 | +273.1% | 14.6% | 0.82 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-DE | robustness | train | 1957-07-01 | 2025-09-01 | 0.63 | +280.1% | 14.7% | 2.00 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-DE | robustness | train | 1957-07-01 | 2025-09-01 | 0.62 | +138.8% | 7.4% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-AU | robustness | train | 1970-09-01 | 2025-09-01 | 0.21 | +67.1% | 23.1% | 1.18 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-AU | robustness | train | 1970-09-01 | 2025-09-01 | 0.22 | +60.9% | 19.9% | 2.29 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-AU | robustness | train | 1970-09-01 | 2025-09-01 | 0.27 | +51.3% | 11.6% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-NZ | robustness | train | 1980-12-01 | 2025-09-01 | 0.06 | +9.1% | 40.9% | 1.16 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-NZ | robustness | train | 1980-12-01 | 2025-09-01 | 0.11 | +21.1% | 35.3% | 2.50 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-NZ | robustness | train | 1980-12-01 | 2025-09-01 | 0.10 | +18.5% | 29.7% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-SE | robustness | train | 1988-02-01 | 2025-09-01 | 0.36 | +87.3% | 21.9% | 1.01 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-SE | robustness | train | 1988-02-01 | 2025-09-01 | 0.56 | +133.8% | 13.3% | 2.04 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-SE | robustness | train | 1988-02-01 | 2025-09-01 | 0.40 | +69.1% | 13.5% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@GOV9-GOV10-NO | robustness | train | 1986-03-01 | 2025-09-01 | 0.31 | +63.7% | 16.3% | 1.06 |
| 2026-11-24 20:57 | pooled-2 | e4@GOV9-GOV10-NO | robustness | train | 1986-03-01 | 2025-09-01 | 0.38 | +73.2% | 12.0% | 2.38 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@GOV9-GOV10-NO | robustness | train | 1986-03-01 | 2025-09-01 | 0.31 | +44.2% | 11.9% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-JPY | robustness | train | 1974-03-22 | 2025-10-31 | 0.24 | +117.5% | 34.6% | 2.17 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-JPY | robustness | train | 1974-03-22 | 2025-10-31 | 0.19 | +70.6% | 36.9% | 5.01 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-JPY | robustness | train | 1974-03-22 | 2025-10-31 | 0.21 | +50.9% | 19.1% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-GBP | robustness | train | 1974-03-22 | 2025-10-31 | 0.18 | +59.9% | 39.1% | 2.54 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-GBP | robustness | train | 1974-03-22 | 2025-10-31 | 0.24 | +87.8% | 22.1% | 5.25 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-GBP | robustness | train | 1974-03-22 | 2025-10-31 | 0.15 | +32.8% | 34.4% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-CHF | robustness | train | 1974-03-22 | 2025-10-31 | 0.21 | +99.9% | 36.9% | 2.34 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-CHF | robustness | train | 1974-03-22 | 2025-10-31 | 0.21 | +86.7% | 36.9% | 5.44 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-CHF | robustness | train | 1974-03-22 | 2025-10-31 | 0.27 | +84.3% | 28.8% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-CAD | robustness | train | 1974-03-22 | 2025-10-31 | 0.08 | +15.0% | 30.5% | 3.02 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-CAD | robustness | train | 1974-03-22 | 2025-10-31 | 0.08 | +13.6% | 24.8% | 5.67 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-CAD | robustness | train | 1974-03-22 | 2025-10-31 | -0.11 | -12.1% | 18.3% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-AUD | robustness | train | 1974-03-22 | 2025-10-31 | 0.20 | +86.3% | 37.8% | 2.13 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-AUD | robustness | train | 1974-03-22 | 2025-10-31 | 0.19 | +71.2% | 34.9% | 5.04 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-AUD | robustness | train | 1974-03-22 | 2025-10-31 | 0.09 | +16.0% | 25.4% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-NZD | robustness | train | 1975-01-17 | 2025-10-31 | 0.42 | +358.8% | 27.7% | 2.32 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-NZD | robustness | train | 1975-01-17 | 2025-10-31 | 0.41 | +278.7% | 32.6% | 5.27 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-NZD | robustness | train | 1975-01-17 | 2025-10-31 | 0.31 | +81.0% | 19.3% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-SEK | robustness | train | 1974-03-22 | 2025-10-31 | 0.13 | +40.8% | 35.4% | 2.42 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-SEK | robustness | train | 1974-03-22 | 2025-10-31 | 0.16 | +48.1% | 37.4% | 5.26 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-SEK | robustness | train | 1974-03-22 | 2025-10-31 | 0.14 | +31.4% | 24.4% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-NOK | robustness | train | 1980-02-15 | 2025-10-31 | 0.21 | +80.4% | 31.5% | 3.13 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-NOK | robustness | train | 1980-02-15 | 2025-10-31 | 0.23 | +80.3% | 33.7% | 5.69 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-NOK | robustness | train | 1980-02-15 | 2025-10-31 | 0.13 | +24.7% | 26.5% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@FX9-FX-EUR | robustness | train | 1974-05-01 | 2025-10-01 | 0.07 | +13.5% | 49.6% | 1.18 |
| 2026-11-24 20:57 | pooled-2 | e4@FX9-FX-EUR | robustness | train | 1974-05-01 | 2025-10-01 | 0.12 | +31.9% | 28.9% | 2.26 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@FX9-FX-EUR | robustness | train | 1974-05-01 | 2025-10-01 | 0.10 | +18.7% | 38.7% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-PPI-grains | robustness | train | 1927-04-01 | 2025-08-01 | 0.16 | +314.4% | 59.3% | 1.26 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-PPI-grains | robustness | train | 1927-04-01 | 2025-08-01 | 0.12 | +120.7% | 57.4% | 2.57 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-PPI-grains | robustness | train | 1927-04-01 | 2025-08-01 | 0.18 | +260.6% | 34.6% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-PPI-livestock | robustness | train | 1947-03-01 | 2025-08-01 | 0.16 | +154.7% | 56.5% | 1.18 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-PPI-livestock | robustness | train | 1947-03-01 | 2025-08-01 | -0.05 | -52.5% | 75.7% | 2.57 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-PPI-livestock | robustness | train | 1947-03-01 | 2025-08-01 | 0.14 | +79.2% | 36.0% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-PPI-coal | robustness | train | 1927-04-01 | 2025-08-01 | 0.62 | +2516.9% | 16.0% | 1.18 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-PPI-coal | robustness | train | 1927-04-01 | 2025-08-01 | 0.53 | +1287.7% | 14.7% | 2.41 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-PPI-coal | robustness | train | 1927-04-01 | 2025-08-01 | 0.62 | +424.2% | 7.4% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-PPI-natgas | robustness | train | 1968-04-01 | 2025-08-01 | 0.19 | +107.0% | 93.8% | 1.34 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-PPI-natgas | robustness | train | 1968-04-01 | 2025-08-01 | 0.28 | +945.5% | 75.0% | 2.45 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-PPI-natgas | robustness | train | 1968-04-01 | 2025-08-01 | 0.20 | +196.0% | 50.5% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-PPI-crude | robustness | train | 1948-04-01 | 2025-08-01 | 0.10 | +1.1% | 91.5% | 1.03 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-PPI-crude | robustness | train | 1948-04-01 | 2025-08-01 | 0.17 | +191.0% | 77.2% | 1.91 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-PPI-crude | robustness | train | 1948-04-01 | 2025-08-01 | 0.14 | +64.0% | 48.7% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-PPI-steel | robustness | train | 1927-04-01 | 2025-08-01 | 0.64 | +2633.8% | 37.1% | 0.70 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-PPI-steel | robustness | train | 1927-04-01 | 2025-08-01 | 0.66 | +2088.8% | 32.2% | 1.81 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-PPI-steel | robustness | train | 1927-04-01 | 2025-08-01 | 0.88 | +660.3% | 9.2% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-PPI-prim-nonferrous | robustness | train | 1948-04-01 | 2025-08-01 | 0.40 | +1226.6% | 46.3% | 0.89 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-PPI-prim-nonferrous | robustness | train | 1948-04-01 | 2025-08-01 | 0.47 | +1513.7% | 31.3% | 2.05 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-PPI-prim-nonferrous | robustness | train | 1948-04-01 | 2025-08-01 | 0.56 | +740.6% | 19.9% | - |
| 2026-11-24 20:57 | pooled-2 | tsmom12@COM8-GOLD | robustness | train | 1972-03-01 | 2025-10-01 | 0.63 | +8907.1% | 44.1% | 1.32 |
| 2026-11-24 20:57 | pooled-2 | e4@COM8-GOLD | robustness | train | 1972-03-01 | 2025-10-01 | 0.57 | +2882.0% | 49.8% | 2.28 |
| 2026-11-24 20:57 | pooled-2 | vt-own-70-x@COM8-GOLD | robustness | train | 1972-03-01 | 2025-10-01 | 0.65 | +2921.7% | 38.9% | - |
| 2026-11-24 21:27 | gap-2002-1 | re-score (not a try): tsmom12 minus holding 2002-01..2025-10, log pts a year, cash 0 / bills: S&P 500 TR -1.00 / -0.70, French US market -1.41 / -1.08, mean of 10 industries -2.02 / -1.60 (Telcm +0.72 to Hlth -3.92), 11-series mean -1.96 / -1.55 (insure-2's -2.19 by peak reproduced); by date fall +7.4, rebound lag -7.5, calm drag -1.9 (11-series mean, cash 0); S&P +4.9 / -4.3 / -1.7 (research/gap-2002-1.md) | note | train | 2002-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-24 21:47 | insure-4 | tsmom12-pput-bills@insure4 | variant | train | 1986-06-30 | 2025-10-31 | 0.75 | +1847.8% | 18.6% | 10.92 |
| 2026-11-24 21:47 | insure-4 | tsmom12-pput-bills-cost10@insure4 | robustness | train | 1986-06-30 | 2025-10-31 | 0.75 | +1780.3% | 18.9% | 10.92 |
| 2026-11-24 21:47 | insure-4 | tsmom12-pput-cash0@insure4 | robustness | train | 1986-06-30 | 2025-10-31 | 0.71 | +1495.5% | 22.8% | 10.92 |
| 2026-11-24 23:31 | wide-18 | vclock12 | variant | train | 1994-02-01 | 2025-10-31 | 0.88 | +6123.2% | 48.3% | 3.32 |
| 2026-11-24 23:31 | wide-18 | vclock12/bills | robustness | train | 1994-02-01 | 2025-10-31 | 0.91 | +7410.6% | 47.5% | 3.30 |
| 2026-11-24 23:31 | wide-18 | huber52 | variant | train | 1994-02-01 | 2025-10-31 | 1.04 | +20286.7% | 40.1% | 3.68 |
| 2026-11-24 23:31 | wide-18 | huber52/bills | robustness | train | 1994-02-01 | 2025-10-31 | 1.07 | +23383.1% | 36.5% | 3.66 |
| 2026-11-24 23:31 | wide-18 | vclock12@etf | robustness | train | 2001-05-27 | 2025-10-31 | 0.56 | +227.1% | 23.3% | 2.87 |
| 2026-11-24 23:31 | wide-18 | huber52@etf | robustness | train | 2001-05-27 | 2025-10-31 | 0.56 | +251.1% | 27.5% | 3.29 |
| 2026-11-24 23:31 | wide-18 | vclock12@idx | robustness | train | 1962-01-02 | 2025-10-31 | 0.68 | +3839.4% | 39.6% | 2.77 |
| 2026-11-24 23:31 | wide-18 | huber52@idx | robustness | train | 1962-01-02 | 2025-10-31 | 0.62 | +3436.0% | 34.7% | 2.44 |
| 2026-11-24 23:32 | wide-18 | hann12: tapered FIR trend filter (killed in step 1: sma200 / e4 / trend-tune overlap; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | kalman-llt: local-linear-trend Kalman slope (killed: per-asset lookback, wf-asset; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | cusum-exit: CUSUM / SPRT drift-change exit (killed: changepoint-momentum, coin-fast-exit, drawdown-control; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | pd-trend: derivative action on the 12-month return (killed: turning-points, e4, fast-reentry; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | gain-schedule: volatility-scheduled lookback (merged into vclock12; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | perm-entropy: permutation-entropy / Lempel-Ziv gate (killed: hurst-entropy-gate parked; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | ib-soft: rate-distortion soft slot (killed: kelly-shrunk, ml-sizing; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | mst-length: correlation-network MST length trigger (killed: absorption-ratio, turbulence; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | spillover: Diebold-Yilmaz connectedness (killed: absorption-ratio, transfer-entropy; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | centrality-tilt: weight peripheral assets (killed: multi-signal BAB wrong sign; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | tail-index: Hill exponent crash warning (killed: critical-slowing, volatility in disguise; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | irreversibility: Zumbach time-reversal asymmetry for sizing (killed: a volatility target; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:32 | wide-18 | post hoc (not a try): vclock12 window by asset (lib/wide18_posthoc.py); median 1.22-1.30 y on BTC, ETH, QQQ, GLD, 0.92-0.94 on SPY, TLT | note | train | 1994-02-01 | 2025-10-31 | - | - | - | - |
| 2026-11-24 23:32 | vix-call-1 | tsmom12+vxth-leg@vixcall1 | variant | train | 2006-03-31 | 2025-10-31 | 0.63 | +369.0% | 27.4% | 13.63 |
| 2026-11-24 23:32 | vix-call-1 | tsmom12-in-vxth-bills@vixcall1 | variant | train | 2006-03-31 | 2025-10-31 | 0.74 | +357.9% | 18.7% | 11.56 |
| 2026-11-24 23:32 | vix-call-1 | tsmom12+vxth-leg-x2@vixcall1 | robustness | train | 2006-03-31 | 2025-10-31 | 0.34 | +182.2% | 43.5% | 13.63 |
| 2026-11-24 23:32 | vix-call-1 | tsmom12+vxth-leg-cost50@vixcall1 | robustness | train | 2006-03-31 | 2025-10-31 | 0.59 | +325.2% | 28.1% | 13.63 |
| 2026-11-24 23:32 | vix-call-1 | tsmom12-cash0+vxth-leg@vixcall1 | robustness | train | 2006-03-31 | 2025-10-31 | 0.61 | +344.9% | 29.9% | 13.63 |
| 2026-11-24 23:32 | vix-call-1 | tsmom12-delever-matched@vixcall1 | control | train | 2006-03-31 | 2025-10-31 | 0.74 | +369.0% | 22.3% | 1.63 |
| 2026-11-24 23:32 | vix-call-1 | mix-tsmom12-pput-matched@vixcall1 | control | train | 2006-03-31 | 2025-10-31 | 0.65 | +377.6% | 42.0% | 13.63 |
| 2026-11-24 23:34 | xs-century-1 | tsmom12@us-mkt-monthly (comparator, above bills, monthly x sqrt12) | baseline | train | 1928-07-01 | 2025-10-31 | 0.55 | +49427.7% | 44.3% | - |
| 2026-11-24 23:34 | xs-century-1 | book (primary): alpha vs tsmom12 IR +0.31 z +2.75 (monthly excess x sqrt12) | variant | train | 1928-07-01 | 2025-10-31 | 0.40 | +501.1% | 29.3% | - |
| 2026-11-24 23:34 | xs-century-1 | R1 gross: alpha vs tsmom12 IR +0.88 z +7.39 (monthly excess x sqrt12) | robustness | train | 1928-07-01 | 2025-10-31 | 0.96 | +9139.5% | 18.8% | - |
| 2026-11-24 23:34 | xs-century-1 | R2 UMD cost 0.34%/mo: alpha vs tsmom12 IR +0.51 z +4.44 (monthly excess x sqrt12) | robustness | train | 1928-07-01 | 2025-10-31 | 0.59 | +1440.5% | 24.6% | - |
| 2026-11-24 23:34 | xs-century-1 | R3 bond/FX costs x2: alpha vs tsmom12 IR +0.25 z +2.22 (monthly excess x sqrt12) | robustness | train | 1928-07-01 | 2025-10-31 | 0.34 | +353.6% | 34.5% | - |
| 2026-11-24 23:34 | xs-century-1 | R4 + commodity spot: alpha vs tsmom12 IR +0.31 z +2.61 (monthly excess x sqrt12) | robustness | train | 1928-07-01 | 2025-10-31 | 0.39 | +366.3% | 25.1% | - |
| 2026-11-24 23:34 | xs-century-1 | R5 1994-01..2025-10: alpha vs tsmom12 IR +0.19 z +0.75 (monthly excess x sqrt12) | robustness | train | 1994-01-01 | 2025-10-31 | 0.20 | +21.1% | 29.3% | - |
| 2026-11-24 23:34 | xs-century-1 | R6 vs six-asset tsmom12: alpha vs tsmom12 IR +0.22 z +0.84 (monthly excess x sqrt12) | robustness | train | 1994-03-01 | 2025-10-31 | 0.20 | +21.6% | 29.3% | - |
| 2026-11-24 23:34 | xs-century-1 | R7 bonds + FX only: alpha vs tsmom12 IR +0.43 z +2.63 (monthly excess x sqrt12) | robustness | train | 1962-04-01 | 2025-10-31 | 0.45 | +274.8% | 23.2% | - |
| 2026-11-24 23:37 | e4-anatomy-1 | re-score (not a try): e4 minus tsmom12 Sharpe per market split by regime and leg (pooled-1/pooled-2 series and code; d reproduced to 6e-16). Card split, 25% zigzag: equity D +0.063 = risk part +0.087 + return part -0.024 (rebound +0.092, fast +0.022, slow +0.003, whipsaw +0.018, calm -0.159); bonds+FX +0.010 = +0.035 - 0.025. Post hoc vs vol-matched tsmom12: equity rebound +0.117 (SE 0.041, 39 of 41 markets > 0), slow bear -0.037, calm -0.043, fast +0.009. Equity-vs-other gap +0.053 = risk part +0.052 (card reading B), not regime mix (research/e4-anatomy-1.md) | note | train | 1927-04-01 | 2025-10-31 | - | - | - | - |
| 2026-11-24 23:35 | temperature-premium | SPY next-but-one month return on GISTEMP 12-month anomaly minus prior decade (b +3.25%/deg C, t +1.63, rank 9/41, gate fail) | screen | train | 1993-02-01 | 2025-10-31 | - | - | - | - |
| 2026-11-24 23:35 | outbreak-premium | SPY 4-week return on detrended Anscombe count of WHO Disease Outbreak News reports (b +0.065%/unit, t +1.68, rank 9/41, gate fail) | screen | train | 2005-01-07 | 2025-10-31 | - | - | - | - |
| 2026-11-24 23:47 | outbreak-premium | review check: W30 gate fit without the 6 weeks with >= 60 WHO items (re-dated archive weeks) (b +0.159%/unit, t +1.11, rank 12/41, placebo SD 1.64) | screen | train | 2005-01-07 | 2025-10-31 | - | - | - | - |
| 2026-11-24 23:47 | outbreak-premium | review check: W30 gate fit on Fridays 2005-01..2019-12 only, before the re-dated years (b +0.082%/unit, t +0.48, rank 21/41, placebo SD 1.16) | screen | train | 2005-01-07 | 2020-01-27 | - | - | - | - |
| 2026-11-24 23:45 | wide-19 | cred-xs | variant | train | 1994-02-01 | 2025-10-31 | 1.09 | +29621.4% | 39.9% | 1.83 |
| 2026-11-24 23:45 | wide-19 | cred-xs/bills | robustness | train | 1994-02-01 | 2025-10-31 | 1.11 | +33497.4% | 38.8% | 1.82 |
| 2026-11-24 23:45 | wide-19 | cred-lr | variant | train | 1994-02-01 | 2025-10-31 | 0.95 | +20355.6% | 48.6% | 1.72 |
| 2026-11-24 23:45 | wide-19 | cred-lr/bills | robustness | train | 1994-02-01 | 2025-10-31 | 0.96 | +21459.4% | 47.5% | 1.73 |
| 2026-11-24 23:45 | wide-19 | cred-xs@etf | robustness | train | 2001-05-27 | 2025-10-31 | 0.62 | +325.1% | 23.6% | 2.12 |
| 2026-11-24 23:45 | wide-19 | cred-lr@etf | robustness | train | 2001-05-27 | 2025-10-31 | 0.53 | +284.1% | 36.2% | 0.96 |
| 2026-11-24 23:45 | wide-19 | cred-xs@idx | robustness | train | 1962-01-02 | 2025-10-31 | 0.70 | +4868.1% | 26.0% | 2.13 |
| 2026-11-24 23:45 | wide-19 | cred-lr@idx | robustness | train | 1962-01-02 | 2025-10-31 | 0.65 | +7530.4% | 51.9% | 0.89 |
| 2026-11-24 23:50 | wide-19 | brier-verify: Brier skill / Murphy decomposition of the in/out signal (killed in step 1: multi-signal / info-1 IC, insure-1; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | rev-costloss: relative economic value of the exit (new, descriptive; a reframing of insure-1; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | mos-calibrate: logistic MOS soft slot (killed: kelly-shrunk, ml-linear, ml-sizing; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | damped-persistence: persistence/climatology blend (killed: combo-1 blend-iv, bet-hedge-seedbank; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | bma-lookbacks: BMA / lagged ensemble of lookbacks (killed: e4, wf-pooled, tranching; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | xl-layer: reinsurance layer / aggregate stop-loss (killed: drawdown-control, cppi-floor, stop-0.25; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | bonus-malus: exposure ladder by monthly outcome (killed: ensemble-tsmom, slew-limit, arm3-12; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | cred-forward: credibility of the forward record, Esscher/Wang premium (killed: power-map-1, insure-4; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | stop-reentry: optimal-stopping re-entry, real-options band (killed: fast-reentry, bear-legs, eu-4 dz25; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | robust-lookback: worst-case lookback set, minimax regret, newsvendor size (killed: ensemble-tsmom, wf-pooled, ib-soft; not run) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:50 | wide-19 | post hoc (not a try): Z at 2025-10-31 with the noise term corrected for correlation, V (1 - rho): six 0.00, etf 0.03, idx 0.16 (lib/wide19_posthoc.py) | note | train | 1994-02-01 | 2025-10-31 | - | - | - | - |
| 2026-11-24 23:55 | hedge-books-1 | book/buy_hold_btc | robustness | train | 1994-02-01 | 2025-10-31 | 0.87 | +2384778.8% | 84.9% | 0.00 |
| 2026-11-24 23:55 | hedge-books-1 | book/buy_hold_spy | robustness | train | 1994-02-01 | 2025-10-31 | 0.63 | +2398.0% | 55.2% | 0.01 |
| 2026-11-24 23:55 | hedge-books-1 | book/sixty_forty | robustness | train | 1994-02-01 | 2025-10-31 | 0.77 | +1126.1% | 30.5% | 0.47 |
| 2026-11-24 23:55 | hedge-books-1 | book/equal_weight | robustness | train | 1994-02-01 | 2025-10-31 | 1.01 | +57602.8% | 66.7% | 1.51 |
| 2026-11-24 23:55 | hedge-books-1 | book/ts_momentum | robustness | train | 1994-02-01 | 2025-10-31 | 1.10 | +6236.9% | 28.4% | 4.38 |
| 2026-11-24 23:55 | hedge-books-1 | book/xs_momentum | robustness | train | 1994-02-01 | 2025-10-31 | 0.94 | +582644.9% | 77.5% | 3.57 |
| 2026-11-24 23:55 | hedge-books-1 | book/vol_target_spy | robustness | train | 1994-02-01 | 2025-10-31 | 0.74 | +864.0% | 33.4% | 3.94 |
| 2026-11-24 23:55 | hedge-books-1 | book/risk_parity | robustness | train | 1994-02-01 | 2025-10-31 | 0.83 | +3688.5% | 62.0% | 0.58 |
| 2026-11-24 23:55 | hedge-books-1 | book/crypto_mean_reversion | robustness | train | 1994-02-01 | 2025-10-31 | 0.13 | +28.1% | 51.7% | 7.05 |
| 2026-11-24 23:55 | hedge-books-1 | book/preset_careful | robustness | train | 1994-02-01 | 2025-10-31 | 0.96 | +1606.2% | 22.0% | 4.78 |
| 2026-11-24 23:55 | hedge-books-1 | book/preset_middle | robustness | train | 1994-02-01 | 2025-10-31 | 1.04 | +6760.6% | 30.9% | 4.91 |
| 2026-11-24 23:55 | hedge-books-1 | book/own_vol_70 | robustness | train | 1994-02-01 | 2025-10-31 | 1.05 | +4300.6% | 27.7% | 1.86 |
| 2026-11-24 23:55 | hedge-books-1 | book/tsmom12 | baseline | train | 1994-02-01 | 2025-10-31 | 1.05 | +18641.3% | 37.0% | 2.80 |
| 2026-11-24 23:55 | hedge-books-1 | book/halving-alone | robustness | train | 1994-02-01 | 2025-10-31 | 1.29 | +70158.9% | 29.5% | 2.57 |
| 2026-11-24 23:55 | hedge-books-1 | book/where-vol | robustness | train | 1994-02-01 | 2025-10-31 | 1.07 | +24569.7% | 35.4% | 1.89 |
| 2026-11-24 23:55 | hedge-books-1 | book/stop-0.25 | robustness | train | 1994-02-01 | 2025-10-31 | 1.09 | +9925.7% | 28.9% | 3.84 |
| 2026-11-24 23:55 | hedge-books-1 | hedge16 | variant | train | 1994-02-01 | 2025-10-31 | 1.13 | +20836.8% | 33.5% | 2.96 |
| 2026-11-24 23:55 | hedge-books-1 | ew16 | baseline | train | 1994-02-01 | 2025-10-31 | 1.16 | +15095.3% | 33.0% | 3.19 |
| 2026-11-24 23:55 | hedge-books-1 | hedge-pair | variant | train | 1994-02-01 | 2025-10-31 | 1.05 | +9239.2% | 32.9% | 2.34 |
| 2026-11-24 23:55 | hedge-books-1 | ew-pair | baseline | train | 1994-02-01 | 2025-10-31 | 1.05 | +9073.0% | 32.8% | 2.31 |
| 2026-11-24 23:55 | hedge-books-1 | book/tsmom12/gymcost | robustness | train | 1994-02-01 | 2025-10-31 | 1.05 | +18290.3% | 37.4% | 2.81 |
| 2026-11-24 23:55 | hedge-books-1 | hedge16/gymcost | robustness | train | 1994-02-01 | 2025-10-31 | 1.12 | +20488.7% | 33.5% | 2.94 |
| 2026-11-24 23:55 | hedge-books-1 | ew16/gymcost | robustness | train | 1994-02-01 | 2025-10-31 | 1.15 | +14775.1% | 33.0% | 3.19 |
| 2026-11-24 23:55 | hedge-books-1 | hedge-pair/gymcost | robustness | train | 1994-02-01 | 2025-10-31 | 1.05 | +9021.0% | 33.2% | 2.33 |
| 2026-11-24 23:50 | air-disaster-mood | SPY daily return on log2(deaths/25) of Wikidata aviation accidents >= 50 deaths, days 0-1, HC1 (b -0.038%/day/unit, t -0.59, rank 10/41, gate fail) | screen | train | 2008-01-02 | 2025-10-31 | - | - | - | - |
| 2026-11-24 23:55 | jackpot-substitution | wide-20 candidate, scored before any price, no number computed: P2, score 5, parked: no keyless jackpot history | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | panic-words | wide-20 candidate, scored before any price, no number computed: P3, score 4, parked: about 2,000 Chronicling America calls | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | mass-casualty-mood | wide-20 candidate, scored before any price, no number computed: P4, score 4, parked: P1's channel, data terms unclear | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | my-ratio | wide-20 candidate, scored before any price, no number computed: P5, filtered (F1: age structure known decades ahead) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | conception-lead | wide-20 candidate, scored before any price, no number computed: P6, filtered (F1: births read as news) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | dst-sleep | wide-20 candidate, scored before any price, no number computed: P7, filtered (F1: scheduled dates, no dose) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | sad-onset | wide-20 candidate, scored before any price, no number computed: P8, filtered (F1: fixed calendar, no dose) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | experience-weighted | wide-20 candidate, scored before any price, no number computed: P9, filtered (F2: weighted past returns) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | consumer-sentiment | wide-20 candidate, scored before any price, no number computed: P10, filtered (F1 and F2) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | skyscraper-index | wide-20 candidate, scored before any price, no number computed: P11, score 0, dead (literature) | note | train | - | - | - | - | - | - |
| 2026-11-24 23:55 | strike-idleness | wide-20 candidate, scored before any price, no number computed: P12, score 4, parked: BLS refuses scripts | note | train | - | - | - | - | - | - |
| 2026-11-24 23:47 | ownvol-anatomy-1 | re-score (not a try): vt-own-70-x minus tsmom12 split into exposure E (fixed-share twin), mean channel M and risk channel R; equity 41 d +0.022 = E +0.001 + M -0.003 + R +0.024; judged 21 d -0.010 = E +0.000 + M -0.015 + R +0.005; FX9 d -0.052 = E +0.000 + M -0.056 + R +0.004; COM8 d +0.056 = E -0.001 + M -0.018 + R +0.075; six d +0.101 = E +0.003 + M -0.153 + R +0.251 (research/ownvol-anatomy-1.md) | note | train | 1913-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 00:07 | breadth-anatomy-1 | re-score (not a try): why breadth-book-1's wider tsmom12 books score lower (same bars, rule, universes; Sharpe above bills 2008-01..2025-10). Gap L-12/L-20/L-all - six -0.23/-0.36/-0.54 = ETF breadth with coins at the six's weight (K - six) -0.17/-0.17/-0.17 (z -2.6 to -3.2) + coin dilution -0.06/-0.19/-0.37 (coin share 26/54/68%). Coin-free: four 0.82 vs four+6/14/29 added 0.38/0.36/0.37. Added sleeves' own tsmom12 Sharpe mean 0.17 (six 0.65; FX -0.31, intl eq 0.04, cmdty 0.06); A-29 book 0.29 vs rho 0.38 x 1.19 = 0.45: marginal test fails, best weight 0 (vs four: rho 0.73). Crisis rho(A-29, six) 0.66 vs 0.37. Inverse-vol widens the gap (-0.81). 2008-09 gap -0.19, 2010-25 -0.54 (research/breadth-anatomy-1.md) | note | train | 2008-01-02 | 2025-10-31 | - | - | - | - |
| 2026-11-25 00:03 | vm-style-1 | tsmom12@us-mkt-monthly (comparator, above bills, monthly x sqrt12) | baseline | train | 1938-07-01 | 2025-10-31 | 0.57 | +23363.4% | 31.0% | - |
| 2026-11-25 00:03 | vm-style-1 | xs-century-1 book (unmanaged, same months): alpha vs tsmom12 full IR +0.35 z +2.92; out-of-paper IR +0.38 z +2.46 (monthly excess x sqrt12) | baseline | train | 1938-07-01 | 2025-10-31 | 0.43 | +450.1% | 29.3% | - |
| 2026-11-25 00:03 | vm-style-1 | CMV (primary: theta = a + b / market vol): alpha vs tsmom12 full IR +0.31 z +2.40; out-of-paper IR +0.28 z +1.58 (monthly excess x sqrt12) | variant | train | 1938-07-01 | 2025-10-31 | 0.34 | +2953.9% | 69.0% | - |
| 2026-11-25 00:03 | vm-style-1 | UMV (control: b = 0): alpha vs tsmom12 full IR +0.29 z +2.29; out-of-paper IR +0.28 z +1.56 (monthly excess x sqrt12) | variant | train | 1938-07-01 | 2025-10-31 | 0.32 | +2240.3% | 66.5% | - |
| 2026-11-25 00:03 | vm-style-1 | own-vol twin (theta = a + b / own vol): alpha vs tsmom12 full IR +0.27 z +2.08; out-of-paper IR +0.27 z +1.51 (monthly excess x sqrt12) | variant | train | 1938-07-01 | 2025-10-31 | 0.28 | +1327.3% | 74.7% | - |
| 2026-11-25 00:03 | vm-style-1 | R1 CMV gross: alpha vs tsmom12 full IR +1.00 z +8.00; out-of-paper IR +0.99 z +5.40 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 1.06 | +364976050745.5% | 52.9% | - |
| 2026-11-25 00:03 | vm-style-1 | R1 UMV gross: alpha vs tsmom12 full IR +0.90 z +7.17; out-of-paper IR +0.99 z +5.84 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 0.95 | +7177729375.7% | 63.5% | - |
| 2026-11-25 00:03 | vm-style-1 | R2 CMV UMD 0.34%/mo: alpha vs tsmom12 full IR +0.46 z +3.65; out-of-paper IR +0.48 z +2.87 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 0.51 | +72263.4% | 73.7% | - |
| 2026-11-25 00:03 | vm-style-1 | R2 UMV UMD 0.34%/mo: alpha vs tsmom12 full IR +0.45 z +3.59; out-of-paper IR +0.48 z +2.85 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 0.50 | +56336.9% | 71.6% | - |
| 2026-11-25 00:03 | vm-style-1 | R3a CMV kappa US 0.25%: alpha vs tsmom12 full IR +0.32 z +2.46; out-of-paper IR +0.29 z +1.59 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 0.35 | +3452.6% | 69.9% | - |
| 2026-11-25 00:03 | vm-style-1 | R3b CMV kappa US 1.0%: alpha vs tsmom12 full IR +0.27 z +2.09; out-of-paper IR +0.24 z +1.35 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 0.30 | +1736.0% | 70.9% | - |
| 2026-11-25 00:03 | vm-style-1 | R4 CMV market variance (1 / sigma^2): alpha vs tsmom12 full IR +0.28 z +2.23; out-of-paper IR +0.27 z +1.53 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 0.32 | +2324.6% | 68.9% | - |
| 2026-11-25 00:03 | vm-style-1 | CMV sample out-of-paper: alpha vs tsmom12 IR +0.28 z +1.58; CMV-UMV Sharpe +0.00 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 2025-10-31 | 0.38 | +354.1% | 36.4% | - |
| 2026-11-25 00:03 | vm-style-1 | CMV sample in-paper 1977-2020: alpha vs tsmom12 IR +0.33 z +1.85; CMV-UMV Sharpe +0.03 (monthly excess x sqrt12) | robustness | train | 1977-01-01 | 2020-12-31 | 0.33 | +572.5% | 60.0% | - |
| 2026-11-25 00:03 | vm-style-1 | CMV sample pre 1939-1976: alpha vs tsmom12 IR +0.39 z +2.10; CMV-UMV Sharpe +0.00 (monthly excess x sqrt12) | robustness | train | 1938-07-01 | 1976-12-31 | 0.48 | +478.3% | 36.4% | - |
| 2026-11-25 00:03 | vm-style-1 | CMV sample post 2021-2025: alpha vs tsmom12 IR -0.53 z -1.32; CMV-UMV Sharpe +0.02 (monthly excess x sqrt12) | robustness | train | 2021-01-01 | 2025-10-31 | -0.41 | -21.5% | 25.7% | - |
| 2026-11-25 00:43 | evalue-forward | anytime-valid sequential test for the forward record (betting e-process ONS, mixture SPRT) vs fixed horizon: on iid data no faster (d +0.10 rho 0.95 alpha 0.025: fixed 78 y, E1 median 79 y, 11% by 20 y; d +0.30 median 10.5 y vs fixed 9 y); on the store's block-resampled null E1 rejects 13.5-14.1% at nominal 2.5% (serial dependence, 52-week variance ratio median 1.34), fixed iid t-test 4.2-6.6%; do not adopt; simulation only (research/evalue-forward-1.md) | note | - | - | - | - | - | - | - |
| 2026-11-25 00:04 | reentry-reconcile-1 | re-score (not a try): e4, or3-12, arm3-12 minus tsmom12 on pooled-1's 41 equity markets (d reproduced exactly), e4's gap split into buy-back ((1-h12)h) and trims (h12(h-1)). Card split, 25% zigzag: e4 buy-back rebound +0.134 = or3-12's +0.134, slow bear -0.065; trims slow bear +0.069, rebound -0.042, calm -0.157. Per 25% fall (491, log pts): e4 dI +1.88 dB +3.54 (K 1.53); e4 buy-back alone -4.35 / +6.32 (K 0.31); or3-12 -6.48 / +8.43 (K 0.23); arm3-12 -5.75 / +7.78 (K 0.26). per fall, in log points, e4's buy-back leaks like the old rules and its trims pay for the bear rallies; in Sharpe the graded, smaller buy-back matters about as much (e4-re +0.045 of e4's +0.063) (research/reentry-reconcile-1.md) | note | train | 1927-07-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 00:04 | reentry-reconcile-1 | diagnostic sleeves (not tries, not selectable; a later card on any counts these 10): e4-re (h12 + (1-h12) e4) D +0.045, e4-trim (h12 e4) +0.014, or3-12 x 0.25/0.5/0.75/w* (w* 0.735) +0.015/+0.022/+0.023/+0.023, arm3-12 x 0.25/0.5/0.75/w* (w* 0.914) +0.012/+0.018/+0.019/+0.017, Sharpe per market vs tsmom12 on 41 equity markets; e4-re minus size-matched sleeves +0.022 / +0.028 (paired SE 0.010 / 0.014) | note | train | 1927-07-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 00:24 | rev-costloss-1 | re-score (not a try): tsmom12 exit as a binary crash warning (out = warn), event = 10% fall below the Friday close within 13 weeks; US market 1927-2025 H 0.49 F 0.21 Peirce +0.28 (random dates -0.01, p 0.000), V > 0 for C/L 0.105-0.290, holder's C/L 0.27, V there +0.06, money V -0.01; 11 French series Peirce +0.23; SPY +0.32, QQQ +0.28, GLD -0.00, TLT +0.06, BTC -0.04, ETH -0.03; grid 5/10/20% x 4/13/26 weeks in research/results/rev-costloss-1.md | note | train | 1927-07-08 | 2025-10-31 | - | - | - | - |
| 2026-11-25 00:07 | tick-tier-1 | re-score (not a try): tsmom12/e4 Sharpe above bills 1995-2008 vs 2009-2025-10 by asset class on pooled-1/pooled-2 series (65 eligible); tsmom12 class means EQ +0.42->+0.22 / FX +0.36->-0.20 / BD +0.52->+0.28 / CM +0.28->+0.28; contrast C = (dEQ+dFX)/2 - dBD: tsmom12 -0.14 (SE 0.36), timing part -0.77 (SE 0.23), e4 +0.10 (SE 0.40), e4 timing -0.53 (SE 0.19); reading: inconclusive (research/tick-tier-1.md) | note | train | 1995-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 00:50 | omori-1 | omori-clock: exit as tsmom12, re-enter when an Omori fit K/(t+c)^p of post-peak large-move counts gives an expected rate below a fraction of the pre-crash rate (killed in step 1: a volatility-calm re-entry in other words; bear-legs volatility / vol ratio / duration AUC 0.47-0.54, arm3-12, vol-calm, hawkes-clustering overlap; not run) | note | train | - | - | - | - | - | - |
| 2026-11-25 01:06 | drought-inflation | W32: TLT log return months m+2..m+4 on -PDSI (contiguous US, NOAA nClimDiv), NW 3 lags (b -0.784%/unit, t -3.71, rank 1/41, kill-only gate PASS; killed by replication R32) | screen | train | 2002-07-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 01:06 | margin-susceptibles | W33: GSPC month m+1 on min(r(m),0) x detrended ln(Z.1 broker customer receivables / equities market value), controls, NW 3 lags (b3 +0.017, t +0.05, rank 41/41, gate fail) | screen | train | 1964-12-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 01:10 | drought-inflation | R32 replication of W32: 10-year yield change end m+1..end m+4 on -PDSI, dose months 1962-01..2002-03, NW 3 lags (b -0.32 bp/unit, t -0.19, rank 21/41, gate fail: W32 dead) | screen | train | 1962-02-28 | 2002-07-31 | - | - | - | - |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-AUS | insure-check | train | 1871-12-31 | 1965-12-31 | 1.03 | +282094.5% | 8.2% | 0.32 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-BEL | insure-check | train | 1871-12-31 | 1965-12-31 | 0.47 | +27669.8% | 31.7% | 0.39 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-CHE | insure-check | train | 1901-12-31 | 1965-12-31 | 0.68 | +8843.8% | 17.7% | 0.38 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-DEU | insure-check | train | 1871-12-31 | 1965-12-31 | 0.16 | +6290934.2% | 26.6% | 0.38 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-DNK | insure-check | train | 1876-12-31 | 1965-12-31 | 0.88 | +56652.3% | 8.3% | 0.38 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-ESP | insure-check | train | 1901-12-31 | 1965-12-31 | 0.67 | +10290.2% | 29.1% | 0.36 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-FIN | insure-check | train | 1897-12-31 | 1965-12-31 | 0.53 | +47295.9% | 18.8% | 0.49 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-FRA | insure-check | train | 1871-12-31 | 1965-12-31 | 0.45 | +28853.8% | 30.0% | 0.40 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-GBR | insure-check | train | 1872-12-31 | 1965-12-31 | 0.62 | +16428.4% | 21.3% | 0.35 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-ITA | insure-check | train | 1886-12-31 | 1965-12-31 | 0.48 | +93796.2% | 58.8% | 0.28 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-JPN | insure-check | train | 1887-12-31 | 1965-12-31 | 0.49 | +150889.5% | 39.1% | 0.46 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-NLD | insure-check | train | 1901-12-31 | 1965-12-31 | 0.39 | +1990.8% | 28.9% | 0.49 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-NOR | insure-check | train | 1882-12-31 | 1965-12-31 | 0.71 | +11196.4% | 19.0% | 0.33 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-PRT | insure-check | train | 1881-12-31 | 1965-12-31 | 0.66 | +53036.7% | 13.3% | 0.33 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-SWE | insure-check | train | 1872-12-31 | 1965-12-31 | 0.85 | +182344.6% | 19.8% | 0.32 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-USA | insure-check | train | 1873-12-31 | 1926-12-31 | 0.43 | +1078.0% | 28.8% | 0.52 |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-check-full: Check 1: full span 1870-2020; Holds; I > 0 in 17 of 17 anchored falls, S 0.70 vs random 0.50 (p 0.024), P 1.27 | insure-check | train | 1871-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-check-real: Check 2: events on the real index; Holds; I > 0 in 11 of 11 anchored falls, S 0.45 vs random 0.28 (p 0.000), P 1.19 | insure-check | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-check-t20: Check 3a: 20% fall / 20% rise; Holds; I > 0 in 14 of 15 anchored falls, S 0.73 vs random 0.48 (p 0.016), P 1.16 | insure-check | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-check-t40: Check 3b: 40% fall / 25% rise; Holds; I > 0 in 8 of 8 anchored falls, S 0.80 vs random 0.43 (p 0.014), P 1.26 | insure-check | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-check-cash0: Check 4: cash at 0 when out; Holds; I > 0 in 9 of 9 anchored falls, S 0.60 vs random 0.38 (p 0.020), P 2.49 | insure-check | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 00:44 | insure-1870-1 | tsmom12a@insure-1870-check-nohyper: Check 5: years with CPI > 50% dropped; Holds; I > 0 in 9 of 9 anchored falls, S 0.76 vs random 0.44 (p 0.036), P 1.12 | insure-check | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 01:16 | coin-drift-run | tsmom12@cd2 (band 0.01; coin-drift-2's six coins to 2019-03) | baseline | train | 2015-01-25 | 2019-03-30 | 1.93 | +27485.5% | 77.5% | 8.39 |
| 2026-11-25 01:16 | coin-drift-run | band05@cd2 (band 0.05 of equity) | robustness | train | 2015-01-25 | 2019-03-30 | 1.92 | +23114.2% | 75.0% | 3.34 |
| 2026-11-25 01:16 | coin-drift-run | coin-drift-2 split (same run, not a try): band05@cd2 net -0.014 (z -0.50); above bills +0.011 (z 0.40); coin fills free -0.019 (z -0.69); reading: killed: no support on unseen data | note | train | 2015-01-25 | 2019-03-31 | - | - | - | - |
| 2026-11-25 01:07 | forward-se | forward registry verdict SE (engineering, not a try): one-year Bartlett HAC with fixed-b Student-t p (b = (L + 1) / n), min_sample with lrv; null rejection at nominal 0.025 on 52-week block-resampled store paths, vs tsmom12 10 y 0.061-0.064 -> 0.043-0.058, 100 y 0.046-0.047 -> 0.031-0.036, tsmom12 vs 0 0.081/0.083 -> 0.010/0.023, Gaussian 0.024-0.027 kept; card kill condition met (3 cells > 0.040), adopted by the night lead as a deviation; remainder is skew of yearly sums (research/forward-se-1.md) | note | - | - | - | - | - | - | - |
| 2026-11-25 02:05 | jst-autocorr-1 | descriptive note on insure-1870-1 (not a try): per-episode S 0.80 vs 0.47 random (gap +0.32) on JST 1871-1965; AR(1) phi 0.19 alone gives median gap +0.20 (observed at 98th pct), full annual averaging +0.24 (94th pct; card reading 'smoothing could explain it', narrowly); random walk +0.06; checked sources are year-end (JST US = Shiller Dec-Dec, JST Norway 1921-65 = Klovland Dec-Dec month-end, acf +0.23); origin of the 0.17-0.19 acf open (research/jst-autocorr-1.md) | note | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 02:42 | panic-words | W34: US market (French daily, compounded) month m+1 on detrended ln share of newspaper articles with "panic" (American Stories, 1926-1963), controls c1, c12, realised vol, NW 3 lags (b +1.38%/unit, t +1.19, rank 37/41, gate fail: dead) | screen | train | 1927-07-31 | 1964-01-31 | - | - | - | - |
| 2026-11-25 02:12 | solar-max-recession | W34: Shiller S&P 500 total return P(m+1)..P(m+2) on trailing 12-month mean SILSO sunspot number / 100, dose months 1871-01..2023-07, NW 12 (b -0.162%/month/unit, t -0.87, rank 3/41, gate fail) | screen | train | 1871-01-31 | 2023-09-30 | - | - | - | - |
| 2026-11-25 02:14 | volcanic-veil | wide-21 candidate, scored before any price, no number computed: S2, score 4, parked: six eruptions since 1871, food channel dead (W32/R32) | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | river-freight | wide-21 candidate, scored before any price, no number computed: S3, score 5, parked: fails its size check, inflation channel dead (W32/R32) | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | pdo-regime | wide-21 candidate, scored before any price, no number computed: S4, score 3, parked: four or five regimes, ENSO and drought channels dead | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | amo-hurricane | wide-21 candidate, scored before any price, no number computed: S5, filtered: duplicate of dead channels (W15, W32) | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | cosmic-ray-cloud | wide-21 candidate, scored before any price, no number computed: S6, filtered: duplicate of W16 (Forbush decreases coincide with storms) | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | eclipse-omen | wide-21 candidate, scored before any price, no number computed: S7, filtered F1: scheduled, no dose | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | hurst-flood | wide-21 candidate, scored before any price, no number computed: S8, filtered F2 (price statistic), dead in the literature (Lo 1991) | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | kaiser-felicity | wide-21 candidate, scored before any price, no number computed: S9, filtered F2: volatility and prior highs are prices | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | stress-corrosion-calm | wide-21 candidate, scored before any price, no number computed: S10, filtered F1/F2: low volatility is a price, credit a published statistic | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | paris-law-credit | wide-21 candidate, scored before any price, no number computed: S11, filtered F1: quarterly credit statistics are public news | note | train | - | - | - | - | - | - |
| 2026-11-25 02:14 | chemical-accident-mood | wide-21 candidate, scored before any price, no number computed: S12, filtered: mood-shock class dead (W31) | note | train | - | - | - | - | - | - |
| 2026-11-25 09:20 | solar-max-recession | renumber at merge (not a try): wide-21's W34 = W35 (panic-words-1 merged first and keeps W34); the replication R34 = R35; the row above stays as written | note | - | - | - | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | power calibration (not a try): pooled2_core monthly code on Shiller US 1927-07..2025-10 (already-scored market and years), SE of one market's d 0.059 (12-month blocks), rho 0.90; expected P4 SE 0.064 at c 0.3, power 0.26 at D +0.063, 0.17 at +0.045 (only SEs printed) | note | train | 1927-07-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4 (P4 pre-1927 stock markets US/GB/DE/FR, monthly, never scored, DECIDING; pooled dSharpe vs tsmom12 -0.065, SE 0.041, z -1.59, one-sided 95% upper +0.002, d>0 in 1/4; contradicted (one-sided 95% upper bound below the 41-market +0.063)) | variant | train | 1868-08-01 | 1927-06-01 | 0.36 | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-P4-US | robustness | train | 1872-03-01 | 1927-06-01 | 0.41 | +387.8% | 29.3% | 0.96 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-US | robustness | train | 1872-03-01 | 1927-06-01 | 0.36 | +232.5% | 34.7% | 2.31 |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-P4-GB | robustness | train | 1868-08-01 | 1924-12-01 | 0.39 | +126.5% | 31.0% | 1.08 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-GB | robustness | train | 1868-08-01 | 1924-12-01 | 0.49 | +164.7% | 25.6% | 2.42 |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-P4-DE | robustness | train | 1871-03-01 | 1913-12-01 | 0.54 | +375.1% | 23.9% | 1.21 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-DE | robustness | train | 1871-03-01 | 1913-12-01 | 0.28 | +98.6% | 31.8% | 2.41 |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-P4-FR | robustness | train | 1900-02-01 | 1927-06-01 | 0.35 | +94.0% | 32.1% | 1.15 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-FR | robustness | train | 1900-02-01 | 1927-06-01 | 0.31 | +66.8% | 26.1% | 2.48 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-gap-1-everywhere (pooled dSharpe vs tsmom12 -0.124, SE 0.039, z -3.15, one-sided 95% upper -0.059, d>0 in 0/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-cost-50-bps (pooled dSharpe vs tsmom12 -0.177, SE 0.047, z -3.78, one-sided 95% upper -0.100, d>0 in 0/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-blocks-6 (pooled dSharpe vs tsmom12 -0.065, SE 0.040, z -1.63, one-sided 95% upper +0.000, d>0 in 1/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-blocks-24 (pooled dSharpe vs tsmom12 -0.065, SE 0.040, z -1.63, one-sided 95% upper +0.001, d>0 in 1/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-US-with-dividends (pooled dSharpe vs tsmom12 -0.039, SE 0.038, z -1.02, one-sided 95% upper +0.024, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-without-US (pooled dSharpe vs tsmom12 -0.069, SE 0.047, z -1.47, one-sided 95% upper +0.008, d>0 in 1/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-without-GB (pooled dSharpe vs tsmom12 -0.119, SE 0.041, z -2.88, one-sided 95% upper -0.051, d>0 in 0/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-without-DE (pooled dSharpe vs tsmom12 +0.001, SE 0.050, z +0.01, one-sided 95% upper +0.083, d>0 in 1/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-without-FR (pooled dSharpe vs tsmom12 -0.073, SE 0.046, z -1.60, one-sided 95% upper +0.002, d>0 in 1/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-1867-1897 (pooled dSharpe vs tsmom12 -0.175, SE 0.056, z -3.15, one-sided 95% upper -0.084, d>0 in 0/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-check-1898-1927 (pooled dSharpe vs tsmom12 -0.039, SE 0.057, z -0.69, one-sided 95% upper +0.055, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-N5 (N5 DK/FI/IE/NO/SE French country files 1975-2025, new markets but years overlap the 41, secondary; pooled dSharpe vs tsmom12 +0.067, SE 0.057, z +1.18, one-sided 95% upper +0.160, d>0 in 4/5; not confirmed, not contradicted (too little power to tell)) | variant | train | 1976-01-01 | 2025-10-01 | 0.64 | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-N5-DK | robustness | train | 1990-01-01 | 2025-10-01 | 0.71 | +2566.0% | 31.0% | 0.95 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-N5-DK | robustness | train | 1990-01-01 | 2025-10-01 | 0.70 | +1560.6% | 26.8% | 2.62 |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-N5-FI | robustness | train | 1989-01-01 | 2025-10-01 | 0.57 | +2584.1% | 41.8% | 1.28 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-N5-FI | robustness | train | 1989-01-01 | 2025-10-01 | 0.62 | +2651.7% | 36.0% | 2.58 |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-N5-IE | robustness | train | 1992-01-01 | 2025-10-01 | 0.46 | +707.4% | 55.3% | 1.33 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-N5-IE | robustness | train | 1992-01-01 | 2025-10-01 | 0.57 | +1106.9% | 32.6% | 2.57 |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-N5-NO | robustness | train | 1976-01-01 | 2025-10-01 | 0.54 | +6956.6% | 39.9% | 1.10 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-N5-NO | robustness | train | 1976-01-01 | 2025-10-01 | 0.58 | +6044.1% | 33.4% | 2.66 |
| 2026-11-25 21:12 | e4-indep-1 | tsmom12@indep-N5-SE | robustness | train | 1976-01-01 | 2025-10-01 | 0.59 | +8609.9% | 44.7% | 1.30 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-N5-SE | robustness | train | 1976-01-01 | 2025-10-01 | 0.74 | +15615.5% | 29.0% | 2.57 |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-posthoc-dividends-all-four (POST HOC, JST eq_dp/12 for GB/DE/FR, Shiller dividends US; pooled dSharpe vs tsmom12 -0.030, SE 0.038, z -0.81, one-sided 95% upper +0.031, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-posthoc-dividends-without-US (POST HOC, JST eq_dp/12 for GB/DE/FR, Shiller dividends US; pooled dSharpe vs tsmom12 -0.058, SE 0.044, z -1.32, one-sided 95% upper +0.014, d>0 in 1/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-posthoc-dividends-without-GB (POST HOC, JST eq_dp/12 for GB/DE/FR, Shiller dividends US; pooled dSharpe vs tsmom12 -0.061, SE 0.038, z -1.62, one-sided 95% upper +0.001, d>0 in 1/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-posthoc-dividends-without-DE (POST HOC, JST eq_dp/12 for GB/DE/FR, Shiller dividends US; pooled dSharpe vs tsmom12 +0.019, SE 0.044, z +0.44, one-sided 95% upper +0.092, d>0 in 2/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@indep-P4-posthoc-dividends-without-FR (POST HOC, JST eq_dp/12 for GB/DE/FR, Shiller dividends US; pooled dSharpe vs tsmom12 -0.023, SE 0.041, z -0.56, one-sided 95% upper +0.044, d>0 in 2/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@monthly-41-gap0 (POST HOC diagnostic on already-scored data: card's monthly code on pooled-1's 41 month-end levels; pooled dSharpe vs tsmom12 +0.050, SE 0.040, z +1.25, one-sided 95% upper +0.116, d>0 in 29/41; by group DEV13 +0.050, ETF8 +0.055, US10 +0.007, WIDE10 +0.091) | robustness | train | 1927-07-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | e4@monthly-41-gap1 (POST HOC diagnostic on already-scored data: card's monthly code on pooled-1's 41 month-end levels; pooled dSharpe vs tsmom12 +0.023, SE 0.036, z +0.65, one-sided 95% upper +0.082, d>0 in 24/41; by group DEV13 +0.036, ETF8 +0.006, US10 -0.014, WIDE10 +0.058) | robustness | train | 1927-07-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:12 | e4-indep-1 | meta (not a try): inverse-variance of pooled-1's 41 (+0.063, SE 0.041) and P4: D -0.001, SE 0.029, z -0.04 (research/e4-indep-1.md) | note | train | 1867-08-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:05 | fx-value-real-1 | sleeve real-rate value (primary 1): alpha vs tsmom12 IR +0.28 z +1.71 (monthly excess x sqrt12) | variant | train | 1980-09-01 | 2025-10-31 | 0.33 | +266.7% | 36.8% | - |
| 2026-11-25 21:05 | fx-value-real-1 | book with real-rate FX value (primary 2): alpha vs tsmom12 IR +0.31 z +2.74 (monthly excess x sqrt12) | variant | train | 1928-07-01 | 2025-10-31 | 0.40 | +489.1% | 30.1% | - |
| 2026-11-25 21:05 | fx-value-real-1 | S1 sleeve gross: alpha vs tsmom12 IR +0.31 z +1.91 (monthly excess x sqrt12) | robustness | train | 1980-09-01 | 2025-10-31 | 0.36 | +329.4% | 35.7% | - |
| 2026-11-25 21:05 | fx-value-real-1 | S2 sleeve FX cost x2: alpha vs tsmom12 IR +0.24 z +1.50 (monthly excess x sqrt12) | robustness | train | 1980-09-01 | 2025-10-31 | 0.29 | +213.1% | 41.6% | - |
| 2026-11-25 21:05 | fx-value-real-1 | S3 sleeve point-to-point 60m: alpha vs tsmom12 IR +0.26 z +1.63 (monthly excess x sqrt12) | robustness | train | 1980-04-01 | 2025-10-31 | 0.31 | +235.5% | 36.6% | - |
| 2026-11-25 21:05 | fx-value-real-1 | S4 sleeve 1994-01..2025-10: alpha vs tsmom12 IR +0.11 z +0.57 (monthly excess x sqrt12) | robustness | train | 1994-01-01 | 2025-10-31 | 0.14 | +36.0% | 36.8% | - |
| 2026-11-25 21:05 | fx-value-real-1 | S5 sleeve vs six-asset tsmom12: alpha vs tsmom12 IR +0.10 z +0.52 (monthly excess x sqrt12) | robustness | train | 1994-03-01 | 2025-10-31 | 0.14 | +35.4% | 36.8% | - |
| 2026-11-25 21:05 | fx-value-real-1 | B1 book gross: alpha vs tsmom12 IR +0.89 z +7.38 (monthly excess x sqrt12) | robustness | train | 1928-07-01 | 2025-10-31 | 0.97 | +8974.2% | 18.8% | - |
| 2026-11-25 21:05 | fx-value-real-1 | B2 book UMD cost 0.34%/mo: alpha vs tsmom12 IR +0.51 z +4.43 (monthly excess x sqrt12) | robustness | train | 1928-07-01 | 2025-10-31 | 0.60 | +1409.8% | 25.5% | - |
| 2026-11-25 21:05 | fx-value-real-1 | B3 bonds + FX only: alpha vs tsmom12 IR +0.44 z +2.65 (monthly excess x sqrt12) | robustness | train | 1962-04-01 | 2025-10-31 | 0.46 | +264.4% | 23.2% | - |
| 2026-11-25 21:05 | fx-value-real-1 | C1 proxy sleeve (spot reversal, #170): alpha vs tsmom12 IR +0.30 z +1.89 (monthly excess x sqrt12) | control | train | 1980-09-01 | 2025-10-31 | 0.37 | +349.1% | 30.9% | - |
| 2026-11-25 21:17 | consumption-cycle | survey-8 listing, scored before any price, no number computed: top 1; F1 pass, F2 with controls; unseen JST 1880-1947; kill-only gate (smallest p 0.048; pick is C1, dead on power) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | bank-capital-premium | survey-8 listing, scored before any price, no number computed: top 2; F1 pass, F2 with controls; JST lev, no return test found; kill-only gate (smallest p 0.024) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | credit-boom-leverage | survey-8 listing, scored before any price, no number computed: parked; F1 contested (wide-21 S11 paris-law-credit filtered F1); JST data used by sources, unseen 2016-2025 only; kill-only at best | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | dealer-leverage | survey-8 listing, scored before any price, no number computed: dead on power; one quarterly Z.1 series, ~30 unseen years | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | intermediary-capital-ratio | survey-8 listing, scored before any price, no number computed: filtered F2 (dealers' market equity) and dead on power | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | dealer-treasury-position | survey-8 listing, scored before any price, no number computed: dead (overlap): the term spread with a minus sign (yield-curve, ts-carry) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | rebalance-threshold | survey-8 listing, scored before any price, no number computed: filtered F1 (calendar part) and F2 (threshold part); overlap with rebalance-pressure | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | gold-platinum | survey-8 listing, scored before any price, no number computed: dead on power; F2 fails for GLD; long platinum history not keyless | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | commodity-currency | survey-8 listing, scored before any price, no number computed: parked; not on the six assets, needs shorts (B7) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | ml-macro-bonds | survey-8 listing, scored before any price, no number computed: dead on power; single TLT timing signal; corrigendum shows look-ahead | note | train | - | - | - | - | - | - |
| 2026-11-25 21:17 | principal-portfolios | survey-8 listing, scored before any price, no number computed: filtered F2 (price signals); overlap with xtsmom, contagion-catchup | note | train | - | - | - | - | - | - |
| 2026-11-25 21:18 | registry-lrv | forward registry lrv measured at freeze (engineering, not a try): Bartlett one-year ratio over variance, divided by fixed-b c, floored at 1, recorded as lrv_train; freeze refuses mean/sharpe lines without it or below it; synthetic AR(1) tests only, no store data read (docs/DECISIONS.md) | note | - | - | - | - | - | - | - |
| 2026-11-25 21:13 | grid-load-premium | W36 (provisional id): French Mkt-RF of month m+3 on 100 ln(U(m)/U(m-12)), U = EIA industrial electricity sales (MER T7.6 ESICPUS), usage months 1974-01..2025-07, NW 3 (b -0.098%/month/point, t -2.31, rank 1/41, post-sample 2011-2025 b -0.225 t -2.53: kill-only gate PASS; killed by replication R36) | screen | train | 1974-04-30 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:15 | grid-load-premium | R36 replication of W36 (`cards/wide-22b.md`): Mkt-RF of month m+3 on yoy growth of NBER electric power production (FRED M01128 to 1938, M0128A from 1939, spliced on growth), usage months 1926-04..1955-12, NW 3 (b -0.027%/month/point, t -0.32, rank 13/41, gate fail: W36 dead) | screen | train | 1926-07-31 | 1956-03-31 | - | - | - | - |
| 2026-11-25 21:15 | grid-load-premium | post hoc, after W36 and R36 (not a rule): W36 regression on 2011-2025 without usage months 2020-2021 (b -0.233, t -1.27, 151 rows); 1974-2025 without 2020-2021 (b -0.084, t -1.82); 1993-2025 (b -0.073, t -1.02); 1993-2010 (b -0.009, t -0.08) | robustness | train | 1974-04-30 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:10 | storage-premium | wide-22 candidate, scored before any price, no number computed: E2, score 5, parked: about five storage-deficit episodes on UNG (power 0), F2 cost (injections answer the futures spread) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | blackout-cascade | wide-22 candidate, scored before any price, no number computed: E3, filtered: mood-shock class dead (W31); size far below an index move | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | kingman-bottleneck | wide-22 candidate, scored before any price, no number computed: Q1, filtered F1 / duplicate: capacity utilisation is a scheduled release; as a premium it is E1's output-gap channel | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | expansion-hazard | wide-22 candidate, scored before any price, no number computed: R1, dead (literature): no positive duration dependence in post-war US expansions (Diebold-Rudebusch 1990, Rudebusch 2016) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | epidemic-threshold | wide-22 candidate, scored before any price, no number computed: N1, filtered F2: the contagion graph is built from return correlations (duplicate of the dead absorption ratio) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | rate-distortion-attention | wide-22 candidate, scored before any price, no number computed: I1, parked: news-pressure data not keyless; documented effect is on retail volume, not index returns | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | debt-ceiling-attrition | wide-22 candidate, scored before any price, no number computed: G1, filtered F1: X-dates are published; four standoffs | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | auction-winners-curse | wide-22 candidate, scored before any price, no number computed: G2, filtered F1: auction sizes announced a week ahead (and finance literature) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | freight-gauge | wide-22 candidate, scored before any price, no number computed: T1, parked as a duplicate of E1 (same output-gap premium, another meter); shares W36's verdict | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | prime-age-inflow | wide-22 candidate, scored before any price, no number computed: D1, filtered F1: age structure known decades ahead (duplicate of wide-20 P5 my-ratio) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | frost-crop | wide-22 candidate, scored before any price, no number computed: H1, filtered: food-price channel dead (W32/R32); size tiny | note | train | - | - | - | - | - | - |
| 2026-11-25 21:10 | habituation | wide-22 candidate, scored before any price, no number computed: B1, filtered F2: the dose is the market's own reaction to past shocks | note | train | - | - | - | - | - | - |
| 2026-11-25 21:58 | rl-7-control | tsmom12@rl7-trainingcell (reference for the gate; 23 train markets x before 1990, mean per-market Sharpe) | control | train | 1870-08-01 | 1989-12-01 | 0.49 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | lasso-sign@none (planted gate, out of fold; vs tsmom12 D -0.038, SE 0.039) | control | train | 1870-08-01 | 1989-12-01 | 0.46 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | lasso-sign@0.00 (planted gate, out of fold; vs tsmom12 D -0.039, SE 0.039) | control | train | 1870-08-01 | 1989-12-01 | 0.45 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | lasso-sign-ceil@0.00 (planted gate, out of fold; vs tsmom12 D -0.009, SE 0.013) | control | train | 1870-08-01 | 1989-12-01 | 0.48 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | lasso-sign@0.05 (planted gate, out of fold; vs tsmom12 D -0.032, SE 0.036; lift over @0.00 +0.007, z +0.58) | control | train | 1870-08-01 | 1989-12-01 | 0.46 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | lasso-sign-ceil@0.05 (planted gate, out of fold; vs tsmom12 D -0.010, SE 0.032; lift over @0.00 -0.002, z -0.06) | control | train | 1870-08-01 | 1989-12-01 | 0.48 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | lasso-sign@0.10 (planted gate, out of fold; vs tsmom12 D +0.009, SE 0.031; lift over @0.00 +0.048, z +2.15; gate fails (G3, G4 met)) | control | train | 1870-08-01 | 1989-12-01 | 0.50 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | lasso-sign-ceil@0.10 (planted gate, out of fold; vs tsmom12 D +0.020, SE 0.034; lift over @0.00 +0.028, z +0.95) | control | train | 1870-08-01 | 1989-12-01 | 0.51 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | pg-lin@none (planted gate, out of fold; vs tsmom12 D -0.028, SE 0.024) | control | train | 1870-08-01 | 1989-12-01 | 0.47 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | pg-lin@0.00 (planted gate, out of fold; vs tsmom12 D -0.028, SE 0.024) | control | train | 1870-08-01 | 1989-12-01 | 0.47 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | pg-lin-ceil@0.00 (planted gate, out of fold; vs tsmom12 D -0.026, SE 0.028) | control | train | 1870-08-01 | 1989-12-01 | 0.47 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | pg-lin@0.05 (planted gate, out of fold; vs tsmom12 D -0.014, SE 0.028; lift over @0.00 +0.014, z +1.91) | control | train | 1870-08-01 | 1989-12-01 | 0.48 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | pg-lin-ceil@0.05 (planted gate, out of fold; vs tsmom12 D -0.011, SE 0.031; lift over @0.00 +0.015, z +1.83) | control | train | 1870-08-01 | 1989-12-01 | 0.48 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | pg-lin@0.10 (planted gate, out of fold; vs tsmom12 D +0.019, SE 0.032; lift over @0.00 +0.047, z +3.37; gate PASSES (G1, G2, G3, G4 met)) | control | train | 1870-08-01 | 1989-12-01 | 0.51 | - | - | - |
| 2026-11-25 21:58 | rl-7-control | pg-lin-ceil@0.10 (planted gate, out of fold; vs tsmom12 D +0.027, SE 0.035; lift over @0.00 +0.053, z +3.39) | control | train | 1870-08-01 | 1989-12-01 | 0.52 | - | - | - |
| 2026-11-25 21:58 | rl-7 | tsmom12@rl7-primary-56 (comparator, mean per-market Sharpe; primary: holdout markets x 1990-01..2025-10) | baseline | train | 1990-01-01 | 2025-10-01 | 0.40 | - | - | - |
| 2026-11-25 21:58 | rl-7 | pg-lin@rl7-primary-56 (primary: holdout markets x 1990-01..2025-10; frozen fit on the training cell; pooled dSharpe vs tsmom12 +0.016, SE 0.034, z +0.46, d>0 in 32/56; one-sided 95% upper +0.072; not shown) | variant | train | 1990-01-01 | 2025-10-01 | 0.42 | - | - | - |
| 2026-11-25 21:58 | rl-7 | pg-lin@rl7-primary-equity (class slice of the primary cell; dSharpe +0.027, SE 0.044, d>0 in 24/39) | robustness | train | 1990-01-01 | 2025-10-01 | - | - | - | - |
| 2026-11-25 21:58 | rl-7 | pg-lin@rl7-primary-rates (class slice of the primary cell; dSharpe -0.018, SE 0.048, d>0 in 3/8) | robustness | train | 1990-01-01 | 2025-10-01 | - | - | - | - |
| 2026-11-25 21:58 | rl-7 | pg-lin@rl7-primary-fx (class slice of the primary cell; dSharpe -0.047, SE 0.047, d>0 in 2/5) | robustness | train | 1990-01-01 | 2025-10-01 | - | - | - | - |
| 2026-11-25 21:58 | rl-7 | pg-lin@rl7-primary-commodity (class slice of the primary cell; dSharpe +0.054, SE 0.045, d>0 in 3/4) | robustness | train | 1990-01-01 | 2025-10-01 | - | - | - | - |
| 2026-11-25 21:58 | rl-7 | tsmom12@rl7-trainmkts-post1990 (comparator, mean per-market Sharpe; train markets x 1990-01..2025-10) | robustness | train | 1990-01-01 | 2025-10-01 | 0.38 | - | - | - |
| 2026-11-25 21:58 | rl-7 | pg-lin@rl7-trainmkts-post1990 (train markets x 1990-01..2025-10; frozen fit on the training cell; pooled dSharpe vs tsmom12 +0.006, SE 0.026, z +0.24, d>0 in 11/19) | robustness | train | 1990-01-01 | 2025-10-01 | 0.39 | - | - | - |
| 2026-11-25 21:58 | rl-7 | tsmom12@rl7-holdmkts-pre1990 (comparator, mean per-market Sharpe; holdout markets x before 1990) | robustness | train | 1929-04-01 | 1989-12-01 | 0.52 | - | - | - |
| 2026-11-25 21:58 | rl-7 | pg-lin@rl7-holdmkts-pre1990 (holdout markets x before 1990; frozen fit on the training cell; pooled dSharpe vs tsmom12 -0.024, SE 0.031, z -0.77, d>0 in 10/24) | robustness | train | 1929-04-01 | 1989-12-01 | 0.50 | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): tsmom12 calm drag (outside 25% zigzag falls + rebound year) split exactly, cash 0, log pts a year: SPY C -1.51 = cost -0.02 + premium -0.77 + timing -0.72; all from calm-only out-spells (edge 0.00); dip gain +1.38, lag loss -2.86; spells <=13 wk -1.41; out 6.6% of calm time (research/calm-drag-1.md) | note | train | 1994-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): QQQ calm drag C -2.08 = cost -0.02 + premium -0.40 + timing -1.66; calm-only spells only; G +0.59, L -2.65; <=13 wk -2.06; out 3.3% of calm time (research/calm-drag-1.md) | note | train | 2000-03-13 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): GLD calm drag C -1.43 = cost -0.03 + premium -2.45 + timing +1.05; calm-only spells only; G +1.93, L -3.34; <=13 wk -0.97, longer -0.43; out 19.8% of calm time (research/calm-drag-1.md) | note | train | 2005-11-21 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): TLT calm drag C -2.28 = cost -0.04 + premium -1.68 + timing -0.56; calm-only spells only; G +1.90, L -4.15; <=13 wk -1.20, longer -1.05; out 24.9% of calm time (research/calm-drag-1.md) | note | train | 2003-08-04 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): BTC under the 25% zigzag 2% of sessions calm, rule never out in them: calm drag 0.00, nothing to split (research/calm-drag-1.md) | note | train | 2013-01-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): ETH under the 25% zigzag 0% of sessions calm: calm drag 0.00, nothing to split (research/calm-drag-1.md) | note | train | 2017-05-27 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): French US market calm drag 1927-2025 C -1.35 = cost -0.02 + premium -0.91 + timing -0.42; eras P/T 1927-61 -0.97/+0.01, 1962-2001 -1.15/-0.03, 2002-25 -0.47/-1.66 (C -2.16 = gap-2002-1); edge spells 0.00; G +1.26, L -2.59; mean of 10 industries 2002-25 C -1.85, P -0.93, T -0.89 (research/calm-drag-1.md) | note | train | 1927-07-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | re-score (not a try): S&P 500 TR calm drag 1986-2025 C -1.12 = cost -0.02 + premium -0.76 + timing -0.35; 2002-25 C -1.65 (= gap-2002-1), P -0.83, T -0.80, <=13 wk -1.54; edge spells -0.04; G +1.34, L -2.41 (research/calm-drag-1.md) | note | train | 1986-07-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:22 | calm-drag-1 | post-hoc diagnostic (not on the card, not a try): coins with a 50% / 50% zigzag; BTC calm 33% of sessions, never out, C -0.07 (cost); ETH calm 11%, out 6.4% of it, C +1.27 (premium -1.31, timing +2.98): no coin calm drag (research/calm-drag-1.md) | note | train | 2013-01-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:28 | jst-autocorr-2 | descriptive note (not a try): pooled lag-1 acf over bills +0.138 (1218 pairs) on insure-1870-1's decisive sample, source-period pairing (research/jst-autocorr-2.md) | note | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 21:28 | jst-autocorr-2 | flag split 'averaged / interpolated' (descriptive): acf flagged -0.00 (138 pairs) vs rest +0.15 (1080), permutation p 0.836: not explained by this flag | note | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 21:28 | jst-autocorr-2 | flag split 'thin' (descriptive): acf flagged +0.26 (275 pairs) vs rest +0.12 (943), permutation p 0.190: not explained by this flag | note | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 21:28 | jst-autocorr-2 | flag split 'disrupted (war, closure, hyperinflation)' (descriptive): acf flagged +0.06 (205 pairs) vs rest +0.18 (1013), permutation p 0.754: not explained by this flag | note | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 21:28 | jst-autocorr-2 | flag split 'union of the three' (descriptive): acf flagged +0.08 (520 pairs) vs rest +0.19 (698), permutation p 0.763: not explained by this flag | note | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 21:28 | jst-autocorr-2 | usability per JST source period (descriptive, card rule), scored years 1871-2020: AR-preserving null only (acf above noise line) 291; AR-preserving null only (labels unknown) 1308; AR-preserving null only (thin) 191; not usable (averaged / interpolated) 271; too short to judge: AR-preserving null only 28; usable 91 | note | train | 1871-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 21:32 | crackdown-shock | wide-23 candidate, scored before any price, no number computed: C2, score 5, parked: no keyless event list of unscheduled crypto enforcement (Auer-Claessens list in a paper appendix; a list from memory is hindsight-picked) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | court-ruling-shock | wide-23 candidate, scored before any price, no number computed: C3, filtered: power 0 (fewer than ten unscheduled crypto court rulings) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | scotus-business | wide-23 candidate, scored before any price, no number computed: C4, score 5 with cause 0, parked: Supreme Court decisions hit single firms, index reach near zero; opinion days announced | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | news-novelty | wide-23 candidate, scored before any price, no number computed: C5, score 4, parked: KL novelty of newspaper text; narrative-news channel died in W34 on the same corpus and years | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | cloud-outage | wide-23 candidate, scored before any price, no number computed: C6, filtered: four or five economy-wide outages; one-day productivity / mood class dead (W31, wide-22 E3) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | fee-congestion | wide-23 candidate, scored before any price, no number computed: C7, filtered F2: blockchain fees and congestion follow price and volume | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | flu-absenteeism | wide-23 candidate, scored before any price, no number computed: C8, score 5 with cause 0, parked: ILI above seasonal norm as a labour shock; size about 0.1% of GDP; outbreak channel dead (W30) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | estate-liquidation | wide-23 candidate, scored before any price, no number computed: C9, filtered: size (excess estates tens of USD bn sold over a year) and power (one episode) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | crime-cycle | wide-23 candidate, scored before any price, no number computed: C10, filtered F1: crime statistics are lagged published news; monthly national counts need an API key | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | fireball-omen | wide-23 candidate, scored before any price, no number computed: C11, filtered: no channel (bolides go unnoticed; mood class dead, W31) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | soil-moisture | wide-23 candidate, scored before any price, no number computed: C12, filtered: food-price channel dead (W32/R32); grains not a live asset | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | creep-rupture | wide-23 candidate, scored before any price, no number computed: C13, filtered F2: time spent at high valuation is a price statistic (cape-tilt dead) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:32 | prediction-error | wide-23 candidate, scored before any price, no number computed: C14, filtered F1: surprises are scheduled macro releases (finance literature) | note | train | - | - | - | - | - | - |
| 2026-11-25 21:35 | hack-drift | W37 (provisional id): ETH ln C(d+8)/C(d+1) on D(d) = sum log2(USD/5m) of DefiLlama non-CEX thefts >= USD 10 m dated d, controls r7 r30, NW 7, days 2016-06-21..2025-10-23 (b +0.278%/unit, t +0.68, rank 38/41 earlier-dose calendars; phase-surrogate rank 27, random-day rank 30: gate FAIL, wrong sign; R37 not run) | screen | train | 2016-06-22 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:57 | hack-drift | post hoc after W37, on review of PR #205 (not a rule, not a gate): W37 design without events not public at their listed date; without LuBian (USD 3.5 bn, listed 2020-12-28, public 2025-08): b -0.003%/unit, t -0.01, rank 31/41 (placebo SD 1.02; phase rank 20, random-day rank 27); without LuBian and Mirror (USD 90 m, discovered 2022-05-17): b -0.023, t -0.06, rank 31; shown cells without LuBian all abs(t) < 1.4 | note | train | 2016-06-22 | 2025-10-31 | - | - | - | - |
| 2026-11-25 21:44 | registry-moments | forward registry (engineering, not a try): lrv sized with an upper 0.65 fixed-b chi-square value of the train estimate (expected power 0.70-0.77 -> 0.81-0.84 on weekly AR(1) records, 5/10 y); sharpe lines measure skew and kurtosis on the train record, plan k below measured refused; synthetic records only, no store data read (research/registry-moments-1.md) | note | - | - | - | - | - | - | - |
| 2026-11-25 21:44 | gate-null-2 | methodology, synthetic null (not a try): P(rank <= 2 of 41) of shifted-calendar placebos 5.4-19% at dose phi 0.8-0.99 (nominal 4.9); phase surrogates 4.0-6.0%; full gate rule (t >= 2) 0.9-3.1% in every family (`gate-null-2.md`) | note | - | - | - | - | - | - | - |
| 2026-11-25 21:44 | gate-null-2 | methodology, synthetic power (not a try): R^2 1%, T 600: shift 53-68%, phase 53-67%, 'both' 46-65% (cost 2-3 points at phi <= 0.95, 5-8 at 0.98-0.99) | note | - | - | - | - | - | - | - |
| 2026-11-25 21:44 | gate-null-2 | descriptive re-score of 19 gates on main (W20-W35, R32, weather-1/2) under phase and IAAFT surrogates: no verdict changes; W32 rank 1 in all families; W33/W35 nulls centred | note | - | - | - | - | - | - | - |
| 2026-11-25 21:44 | gate-null-2 | proposed rule (not adopted): dose acf1 >= 0.8 -> pass needs rank <= 2 in shifted calendars and in 40 phase surrogates, plus t >= 2 | note | - | - | - | - | - | - | - |
| 2026-11-25 21:46 | data-wide-2 | data lane (not a try): keyless sources ranked by new independent market-years vs scored coverage (JST equity included); cached Yale ICF London IMM 1869-1929 (77 sovereign bond markets, 2,463 new pre-1927 bond years, 82 falls 25%+; stock indices 50 countries, file truncated; Yale terms academic only: owner decision needed before rule tests), St Petersburg 1865-1917, NYSE 1815-1925, Norges Bank bonds 1820-/FX 1819-, SNB 1924-, AQR commodity futures 1877-; manual download only (robots or blocks): NBER ch. IV commodities, DBnomics (IFS FX, OECD shares), Riksbank, FRED, OECD, Stooq; no rule run (research/data-wide-2.md) | note | - | - | - | - | - | - | - |
| 2026-11-25 22:15 | insure-1709-1 | before scoring (card), BoE monthly 1709-1866, monthly log returns: lag-1 acf shares Neal 1709-04..1811-02 +0.253 (1221 pairs), GRS excl. mines 1811-03..1825-03 +0.498 (167), Acheson cap-weighted 1825-04..1866-12 +0.232 (499), all above noise line (stale-suspect); consols Neal 1753-1822 +0.032, Odlyzko/NBER 1823-1866 +0.028; splice found Neal/GRS/Acheson (card expected Neal/Acheson) | note | train | 1709-04-30 | 1866-12-31 | - | - | - | - |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-shares | insure-check | train | 1710-05-31 | 1866-12-31 | 0.29 | +2540.2% | 67.6% | 0.96 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-consols | insure-check | train | 1754-09-30 | 1866-12-31 | 0.11 | +70.1% | 34.9% | 1.53 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-shares-20%/20% | insure-check | train | 1710-05-31 | 1866-12-31 | 0.29 | +2540.2% | 67.6% | 0.96 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-shares-40%/25% | insure-check | train | 1710-05-31 | 1866-12-31 | 0.29 | +2540.2% | 67.6% | 0.96 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-shares-Neal-alone | insure-check | train | 1710-05-31 | 1811-02-28 | 0.16 | +212.4% | 67.6% | 1.16 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-shares-Gayer-Rostow-Schwartz-excl.-mines-alone | insure-check | train | 1812-04-30 | 1825-03-31 | 0.95 | +66.2% | 9.3% | 0.46 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-shares-Acheson-et-al.-alone | insure-check | train | 1826-05-31 | 1866-12-31 | 0.80 | +408.7% | 14.2% | 0.69 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-index-Acheson-paid-up-weighted | insure-check | train | 1826-04-30 | 1866-12-31 | 0.52 | +216.1% | 19.4% | 1.28 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-index-Acheson-unweighted | insure-check | train | 1826-04-30 | 1866-12-31 | 0.75 | +444.0% | 18.2% | 0.83 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-index-GRS-with-mines | insure-check | train | 1812-03-31 | 1850-12-31 | 0.19 | +112.4% | 65.4% | 0.85 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-index-GRS-without-mines | insure-check | train | 1812-03-31 | 1850-12-31 | 0.39 | +107.1% | 22.4% | 0.95 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-index-Hayek | insure-check | train | 1821-02-28 | 1866-12-31 | 0.34 | +185.1% | 39.3% | 0.89 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-shares-lag-1 | insure-check | train | 1710-06-30 | 1866-12-31 | 0.25 | +1485.3% | 67.9% | 0.96 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-consols-lag-1 | insure-check | train | 1754-10-31 | 1866-12-31 | 0.09 | +53.0% | 35.1% | 1.52 |
| 2026-11-25 22:17 | insure-1709-1 | tsmom12m@insure-1709-check-consols-total-return | insure-check | train | 1754-09-30 | 1866-12-31 | 0.44 | +1839.3% | 22.0% | 1.10 |
| 2026-11-25 22:18 | insure-1709-1 | tsmom12m@insure-1709-check-shares-cash-discount-rate | insure-check | train | 1710-05-31 | 1866-12-31 | 0.47 | +26971.5% | 67.2% | 0.96 |
| 2026-11-25 22:18 | insure-1709-1 | tsmom12m@insure-1709-check-consols-cash-discount-rate | insure-check | train | 1754-09-30 | 1866-12-31 | 0.47 | +1616.7% | 25.5% | 1.53 |
| 2026-11-25 22:04 | consumption-cycle | W38 (provisional id), jst-gates-1 (`cards/jst-gates-1.md`): next-year JST log equity return over bills on the Hamilton consumption cycle (ln rconsbarro, h 2, lags 2-3, expanding), country dummies, trailing 1/3-year returns and eq_dp as controls, DK 2, 14 countries, 355 rows, outcomes 1904-1913, 1920-1938, 1947 minus the jst-autocorr-2 drop list (b -0.0236 per sd, t -1.88, shift rank 3/21, bootstrap p 0.045, halves -0.030 / -0.027, without suspect periods -0.023; phase rank 4/41 shown): kill-only gate FAIL (not a clean kill; not supported); no replication | screen | train | 1904-12-31 | 1947-12-31 | - | - | - | - |
| 2026-11-25 22:04 | consumption-cycle | shown after W38 (not gating): no controls t -2.47; dose of year t-1 t -0.57; second form c(t) minus mean c(t-10..t-1) t -2.71, shift rank 1/21 (shown only, not the card's dose); common rows t -1.84, rank 3; feedback z(t) on y(t-1) t +3.40, on y(t) t -0.19; 10 of 14 countries with a negative own slope | robustness | train | 1904-12-31 | 1947-12-31 | - | - | - | - |
| 2026-11-25 22:04 | bank-capital-premium | W39 (provisional id), jst-gates-1: next-year JST log equity return over bills on lev minus its trailing 10-year mean, controls as W38 plus crisisJST, DK 2, 16 countries, 1285 rows, outcomes 1925-2020 without 1939-1946 minus the drop list (b +0.0023 per sd, t +0.17, shift rank 19/41, bootstrap p 0.580, halves -0.012 / +0.022; phase rank 28/41 shown): kill-only gate KILL (clean, wrong sign); no replication | screen | train | 1925-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 22:04 | bank-capital-premium | shown after W39 (not gating): no controls t -0.30; dose of year t-1 t +0.78; without suspect periods t +0.21; common rows t +0.81, rank 28; no crisis control t +0.17; government bond excess return t +2.38 (sign reported only); 9 of 16 countries with a negative own slope | robustness | train | 1925-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 22:05 | jst-gates-1 | note (not a try): the first run's phase surrogates replaced each country's phases with shared random ones (perfect phase alignment across countries, not Prichard-Theiler); fixed to add the shared random phase to each country's own phases. Shown diagnostic only: W38 phase rank 8 -> 4 of 41, W39 24 -> 28; deciding numbers unchanged | note | train | - | - | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): SPY tsmom12 minus holding, cash 0, log pts a year: fall gain I +4.15, buy-back B -3.22, calm C -1.51, net N -0.57 (bills -0.20); since 2002 N -1.38; 3 falls of 25% (research/asset-ledger-1.md) | note | train | 1994-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): QQQ I +12.06, B -8.92, C -2.08, N +1.06 (bills +1.52), all from 2000-2002; since 2002 N -1.48 (research/asset-ledger-1.md) | note | train | 2000-03-13 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): TLT I +1.96, B -1.16, C -2.28, N -1.48 (bills -0.70); 2 falls (research/asset-ledger-1.md) | note | train | 2003-08-04 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): GLD I +1.64, B -2.53, C -1.43, N -2.33 (bills -2.09); 2 falls (research/asset-ledger-1.md) | note | train | 2005-11-21 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): BTC I +26.93, B -30.64, C 0.00, N -3.72 (bills -3.29); trading cost -1.00 a year of it; 33 falls (research/asset-ledger-1.md) | note | train | 2013-01-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): ETH I +63.60, B -67.16, C 0.00, N -3.55 (bills -2.53); trading cost -1.91 a year of it; 23 falls (research/asset-ledger-1.md) | note | train | 2017-05-27 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): French US market (SPY proxy) I +7.03, B -5.78, C -1.35, N -0.10 (bills +0.66); since 2002 N -1.41 (= gap-2002-1); 21 falls (research/asset-ledger-1.md) | note | train | 1927-07-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): S&P 500 TR (SPY proxy) I +3.39, B -3.11, C -1.12, N -0.84 (bills -0.34); since 2002 N -1.00 (= gap-2002-1) (research/asset-ledger-1.md) | note | train | 1986-07-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): French HiTec (loose QQQ proxy) I +10.25, B -9.26, C -1.39, N -0.40 (bills +0.46); since 2002 N -2.97 (research/asset-ledger-1.md) | note | train | 1927-07-05 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): 30y Treasury rebuild DGS30 (TLT proxy, insure-1 paper rule) I +1.66, B -1.54, C -2.24, N -2.12 (bills -0.67); since 2002 N -2.49 (research/asset-ledger-1.md) | note | train | 1978-02-27 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): gold monthly averages (GLD proxy, trend-where-long monthly tsmom12) I +3.08, B -1.89, C -0.96, N +0.22; 2005-2025 N -1.43 vs GLD -2.33 (averaging flatters) (research/asset-ledger-1.md) | note | train | 1972-02-01 | 2025-10-01 | - | - | - | - |
| 2026-11-25 22:31 | asset-ledger-1 | re-score (not a try): six-asset gym books, worst drawdown split by asset (cash 0): equal-weight 68.8% 2000-03..2002-10 (QQQ 74%, SPY 26%); tsmom12 37.4% 2018-01..2020-03 (BTC 34%, ETH 73%, TLT/GLD -11%), equal-weight over those dates 27.1% (research/asset-ledger-1.md) | note | train | 1994-02-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:03 | fx-peg-1 | before scoring (card), 23 FX markets 1791-1970 as quoted (BoE $/GBP; Norges Bank A1 end month, A2 monthly averages): lag-1 acf of monthly log changes end-month sources -0.09..+0.40, A2 averages -0.01..+0.60 (Mark +0.60, USD +0.41, CAD +0.43); peg filter (trailing 24m, 1% band, 80%) float share 0.00-0.57 by market; agreement with chronology (hand-coded pre-1946, IRR fine codes 1946-70) 0.841 on 10,862 market-months, kappa +0.65 (filter peg/chronology float 1,520, filter float/chronology peg 212): below the card's 0.85, so the verdict carries 'filter disagrees with the chronology'; data-wide-2's parser drops A2 1914-1927 (Excel serials < 10,000), read here | note | train | - | - | - | - | - | - |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-filtered | insure-check | train | 1793-02-28 | 1953-12-31 | 0.25 | +19208.3% | 45.3% | 1.02 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-unfiltered | insure-check | train | 1792-02-29 | 1970-12-31 | 0.15 | +133191.5% | 57.7% | 1.43 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-pegonly | insure-check | train | 1792-02-29 | 1970-12-31 | 0.08 | +612.7% | 66.7% | 1.57 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-falls-10/10 | insure-check | train | 1793-02-28 | 1953-12-31 | 0.25 | +19208.3% | 45.3% | 1.02 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-falls-25/25 | insure-check | train | 1793-02-28 | 1953-12-31 | 0.25 | +19208.3% | 45.3% | 1.02 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-window-12 | insure-check | train | 1792-02-29 | 1953-04-30 | 0.28 | +34467.4% | 46.4% | 1.00 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-window-60 | insure-check | train | 1796-02-29 | 1941-10-31 | 0.21 | +3368.8% | 45.3% | 1.04 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-band-2% | insure-check | train | 1795-07-31 | 1950-10-31 | 0.32 | +20559.2% | 44.7% | 0.96 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-end-month-only | insure-check | train | 1793-02-28 | 1942-05-31 | 0.26 | +623.6% | 45.3% | 1.26 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-nok-only | insure-check | train | 1821-05-31 | 1953-12-31 | 0.27 | +8634.1% | 33.7% | 0.91 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-boe-only | insure-check | train | 1793-02-28 | 1942-05-31 | 0.19 | +121.1% | 45.3% | 1.37 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-cost-25bps | insure-check | train | 1793-02-28 | 1953-12-31 | 0.22 | +9264.3% | 48.1% | 1.02 |
| 2026-11-25 23:07 | fx-peg-1 | tsmom12m@fx-peg-1-check-stale-lag1 | insure-check | train | 1793-02-28 | 1953-12-31 | 0.18 | +3031.7% | 56.2% | 1.01 |
| 2026-11-25 23:12 | fx-peg-1 | post hoc (not on the card), description: filter vs chronology agreement split at 1946: hand-coded list 1791-1945 0.930 on 6,983 market-months (kappa +0.86), IRR 1946-1970 0.679 on 3,879 (kappa +0.05; all 1,247 disagreements IRR float / filter peg: IRR codes the krone 12 in 1946-54, parallel-market basis); peg-only book: 1 confirmed 15% fall, 19 unfinished (devaluations never rebound 15%); 22 unfinished falls in the primary book, rule S median 0.88 | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | quake-supply-spillover | wide-24 candidate, scored before any price, no number computed: Q2, score 6 but power 0, parked: a handful of hub quakes; input-output weights not keyless by script; first link is Q1 quake-drift | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | aftershock-renewal | wide-24 candidate, scored before any price, no number computed: Q3, filtered F1: after the mainshock the Omori decay is a public deterministic clock; omori-1 killed the market form | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | elimination-mood | wide-24 candidate (wide-8's W18, never gated), scored before any price, no number computed: Q4, score 4, parked: mood class dead (W31); one-day dip not a trade at the book's horizon; keyless match list now exists | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | olympic-host | wide-24 candidate, scored before any price, no number computed: Q5, filtered: power 0 (about 15 awards in markets with data) | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | canal-closure | wide-24 candidate, scored before any price, no number computed: Q6, filtered: power 0 (four or five closures) | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | cable-cut | wide-24 candidate, scored before any price, no number computed: Q7, filtered: no index-level channel or size (traffic reroutes within hours) | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | fraud-revelation | wide-24 candidate, scored before any price, no number computed: Q8, score 5, parked (data): SEC servers ask for a contact e-mail; keyless DOJ list starts 2009 (one bust); F2 with controls | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | livestock-epidemic | wide-24 candidate, scored before any price, no number computed: Q9, filtered: food-price channel dead (W32/R32); few outbreaks | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | refugee-wave | wide-24 candidate, scored before any price, no number computed: Q10, filtered F1 and size: inflows counted with lags; Mariel shows no wage effect | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | supply-pressure | wide-24 candidate, scored before any price, no number computed: Q11, filtered: GSCPI power 0 (three episodes since 1997); inflation-risk channel dead (W32/R32) | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | export-ban | wide-24 candidate, scored before any price, no number computed: Q12, filtered: power 0, single-sector reach | note | train | - | - | - | - | - | - |
| 2026-11-25 22:29 | disaster-evt | wide-24 candidate, scored before any price, no number computed: Q13, filtered: duplicate of the disaster-probability premium (W30 dead); EM-DAT needs registration | note | train | - | - | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 (provisional id): hit country's index excess over the other 24 cached markets, ln C(s0+21)/C(s0+1), on D = sum log2(1 + S) of declustered M >= 6 shallow quakes (S = % of the country's place population within 40 km x 10^(0.45(M-6.5))), controls r2 r20, market dummies, DK 30, 25 markets, 168,901 rows, 79 (event, market) pairs (b +0.093%/unit, t +0.38, rank 24/41 shifted calendars both ways, step 23 days; random-day surrogate rank 28; dose acf1 +0.008, gate-null-2 'both' rule not triggered: gate FAIL; R40 not run) | screen | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: reaction r2 on D, no controls, DK 5 (b -0.380%/unit, t -1.39) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: 60-session horizon, DK 90 (b -0.137, t -0.36) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: own return, no world subtraction (b +0.144, t +0.53) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: binary dose, 1 per event with S >= 1% (b +0.444, t +0.61) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: fixed radius 100 km (b -0.005, t -0.03) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: M >= 6.5 only (b -0.088, t -0.33) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: Japan only, N225, 6,800 rows (b -0.290, t -0.77) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: without Tohoku 2011-03-11 (b +0.282, t +1.19) | robustness | train | 1998-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 22:34 | quake-drift | W40 shown: rows from 2012-01-01, after Scholtens-Voorhorst's sample, 85,219 rows (b +0.131, t +0.22) | robustness | train | 2012-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:00 | coup-shock | wide-25 candidate, scored before any price, no number computed: P2, filtered: power 0 (no coups in the cached markets since 1975 beyond a handful; Thailand, Turkey not cached) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | leader-death | wide-25 candidate, scored before any price, no number computed: P3, filtered: power 0 (a handful of natural deaths in office in the 21 French markets since 1975; Jones-Olken design) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | fragmentation-premium | wide-25 candidate, scored before any price, no number computed: P4, score 4 (tie with P1), parked: persistent dose that changes at elections (few swings per country); same Pastor-Veronesi premium as W27 (dead); F2 with controls | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | smog-cognition | wide-25 candidate, scored before any price, no number computed: P5, filtered: same-day mood/cognition dip (Heyes-Neidell-Saberian 2016), dead class (W31, W16) and not a trade at the book's weekly horizon | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | dev-activity | wide-25 candidate, scored before any price, no number computed: P6, score 4 (tie with P1), parked: cause 0 (commits to Bitcoin Core / go-ethereum have no monthly link to coin demand); F2 with controls (developers follow prices) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | cve-disclosure | wide-25 candidate, scored before any price, no number computed: P7, filtered: power 0 (a few dozen NVD entries, a handful critical); security news does not move ETH at index level (W37) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | sanctions-designation | wide-25 candidate, scored before any price, no number computed: P8, not scored: duplicate of wide-23 C2 crackdown-shock (a subset); noted as a data lead (OFAC SDN list, if per-entry dates are keyless) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | night-lights | wide-25 candidate, scored before any price, no number computed: P9, filtered (data): NASA Earthdata and the EOG archive need a login | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | process-accident | wide-25 candidate, scored before any price, no number computed: P10, filtered: no reach to a live asset (product prices and single firms) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | rail-carloads | wide-25 candidate, scored before any price, no number computed: P11, filtered F1 and data: scheduled weekly release read as news; history not keyless by script; duplicate of wide-22 T1 freight gauge | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | recall-wave | wide-25 candidate, scored before any price, no number computed: P12, filtered: no reach (single firms) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | beige-book-tone | wide-25 candidate, scored before any price, no number computed: P13, score 3, parked: scheduled release; cause 0 (macro summary priced on release); narrative-text channel dead (W34); F2 with controls | note | train | - | - | - | - | - | - |
| 2026-11-25 23:00 | quantum-threat | wide-25 candidate, scored before any price, no number computed: P14, filtered: power 0 (a handful of milestone papers); no break within any trading horizon | note | train | - | - | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41, wide-25: country's French USD market return minus the mean of the other 20 French markets over months m+1..m+6 on D = 1 in a month with a ParlGov mid-term cabinet start (new cabinet, same election date as the previous), controls own excess 1/3/12 months, country dummies, DK 6, 18 countries, 9,300 country-months 1976-01..2022-12, 171 event months (b -1.663% per event month, t -1.74, rank 41/41 from the top (the lowest t) among earlier-dose calendars k = 25..103 months odd; null SD 1.24, 8% past 2, 5/50/95% -1.26/+0.14/+2.26; random-month surrogates SD 1.10, rank 39; dose acf1 -0.007): kill-only gate FAIL (wrong sign); R41 not run | screen | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: reaction e(m-1)+e(m), no controls, DK 2 (b +0.086, t +0.15) | robustness | train | 1976-01-31 | 2022-12-31 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: horizon 3 months, DK 3 (b -1.119, t -1.86) | robustness | train | 1976-01-31 | 2023-03-31 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: horizon 12 months, DK 12 (b -3.120, t -2.60; wrong side of the one-sided gate, noted only) | robustness | train | 1976-01-31 | 2023-12-31 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: local-currency returns (b -1.197, t -1.44) | robustness | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: without Italy and Japan, 8,172 rows (b -1.323, t -1.13) | robustness | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: rows m >= 2001-01, after Bernhard-Leblang's samples, 4,752 rows (b -0.888, t -1.08) | robustness | train | 2001-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: non-caretaker events only (b -1.647, t -1.60) | robustness | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: caretaker events only, 17 events (b -1.726, t -0.85) | robustness | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: without the 13 post-election formations (previous cabinet a caretaker from election day; cell added after the card, before any number) (b -1.773, t -1.77) | robustness | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: count dose (b -1.663, t -1.74) | robustness | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:05 | cabinet-collapse | W41 shown: no controls (b -1.683, t -1.74) | robustness | train | 1976-01-31 | 2023-06-30 | - | - | - | - |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-A1: A1 Shiller (averaged), lag 0; I > 0 in 4 of 4, S 0.73 vs random 0.29 (p_rot 0.000), G +0.435 | insure-check | train | 1886-03-31 | 1925-12-31 | 0.77 | +1037.0% | 20.1% | 0.94 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-A2: A2 Schwert / Dow Jones (month-end), lag 0; I > 0 in 4 of 4, S 0.70 vs random 0.30 (p_rot 0.000), G +0.380 | insure-check | train | 1886-03-31 | 1925-12-31 | 0.52 | +637.0% | 27.6% | 1.04 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-A3: A3 Shiller, signal a month older; I > 0 in 4 of 4, S 0.63 vs random 0.29 (p_rot 0.000), G +0.329 | insure-check | train | 1886-04-30 | 1925-12-31 | 0.59 | +540.7% | 21.1% | 0.94 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-A4: A4 Schwert / Dow Jones, signal a month older; I > 0 in 4 of 4, S 0.68 vs random 0.31 (p_rot 0.006), G +0.361 | insure-check | train | 1886-04-30 | 1925-12-31 | 0.42 | +354.5% | 33.8% | 1.05 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-A5: A5 Shiller's signal traded on Dow Jones; I > 0 in 4 of 4, S 0.71 vs random 0.27 (p_rot 0.000), G +0.417 | insure-check | train | 1886-03-31 | 1925-12-31 | 0.53 | +672.4% | 31.5% | 0.94 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-C0: C0 AQR commodities, lag 0; I > 0 in 6 of 6, S 0.62 vs random 0.43 (p_rot 0.061), G +0.186 | insure-check | train | 1878-03-31 | 1912-12-31 | 0.21 | +99.3% | 54.2% | 1.49 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-C1: C1 AQR commodities, one-month delay; I > 0 in 6 of 6, S 0.54 vs random 0.42 (p_rot 0.167), G +0.121 | insure-check | train | 1878-04-30 | 1912-12-31 | 0.09 | +11.6% | 70.9% | 1.47 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-C0-20: C0 at 20% / 20%; I > 0 in 8 of 8, S 0.51 vs random 0.42 (p_rot 0.203), G +0.080 | insure-check | train | 1878-03-31 | 1912-12-31 | 0.21 | +99.3% | 54.2% | 1.49 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12m@stale-checks-1-C1-20: C1 at 20% / 20%; I > 0 in 6 of 8, S 0.44 vs random 0.41 (p_rot 0.425), G +0.013 | insure-check | train | 1878-04-30 | 1912-12-31 | 0.09 | +11.6% | 70.9% | 1.47 |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12a@stale-checks-1-L1: insure-1870-1 decisive sample, first year dropped, signal t-1; Holds; I > 0 in 9 of 9 anchored falls, S 0.72 vs random 0.45 (p 0.010), P 1.14 | insure-check | train | 1872-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 23:04 | stale-checks-1 | tsmom12a@stale-checks-1-L2: insure-1870-1 decisive sample, first year dropped, signal t-2; Does not hold; I > 0 in 5 of 9 anchored falls, S 0.37 vs random 0.44 (p 0.732), P 3.17 | insure-check | train | 1872-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 23:04 | stale-checks-1 | before scoring (descriptive, not a try): US monthly 1885-03..1925-12 (Aug-Nov 1914 dropped), lag-1 acf of log total returns: Shiller (Cowles averages) +0.250, Schwert appendix / Dow Jones month-end +0.015 (483 pairs, noise line 0.075); Working (1960) rho(25) 0.249, simulated monthly high-low midrange +0.302; monthly return correlation 0.697 | note | train | 1885-03-31 | 1925-12-31 | - | - | - | - |
| 2026-11-25 23:04 | stale-checks-1 | (a) verdict (card): dG = G(Shiller) - G(Dow Jones) = +0.435 - 0.380 = +0.055: small, not separable from noise on 4 falls each; averaging is as large as Working predicts in the acf but moves the 12-month timing gap little; Dow Jones gap +0.38 at AR(1) p 0.106 (research/stale-checks-1.md) | note | train | 1886-03-31 | 1925-12-31 | - | - | - | - |
| 2026-11-25 23:04 | stale-checks-1 | (b) verdict (card): one-year-older signal on insure-1870-1 loses the timing (S 0.37 vs random 0.44, p_S 0.732; 5 of 9 anchored falls) while the same trimmed sample with the usual signal keeps it (0.72 vs 0.45, p 0.010): timing rests on the last year's return; per-episode gap of the older signal +0.091 sits inside AR(1)-own-phi worlds (p 0.321); artefact and real persistence not separated | note | train | 1872-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 23:04 | stale-checks-1 | (c) verdict (card): AQR EW commodity excess return 1877-1912, lag-1 acf +0.116 (noise 0.079); gap G +0.186 (p_rot 0.061; AR1 0.106, BB 0.071) falls to +0.121 with a one-month delay (p_rot 0.167): ratio 0.65, partly; 6 of 6 falls lost less either way; first trend test on this series (no earlier record used it) | note | train | 1878-03-31 | 1912-12-31 | - | - | - | - |
| 2026-11-25 23:01 | insure-bonds-1 | before scoring (card), monthly log total returns: norway lag-1 acf N1 +0.13, N3 -0.02, N4 +0.05, N5 -0.26, N6 -0.05; falls 25/20/15/10% 0/0/0/2, threshold 10%; consols lag-1 acf C2 +0.02, C3 -0.13; falls 25/20/15/10% 0/2/2/4, threshold 10% (research/results/insure-bonds-1.md) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-norway | insure-check | train | 1823-04-30 | 1984-12-31 | 1.43 | +46475.3% | 18.8% | 0.27 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-consols | insure-check | train | 1867-01-31 | 1926-12-31 | 0.46 | +219.6% | 34.3% | 1.07 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-norway-5pct | insure-check | train | 1823-04-30 | 1984-12-31 | 1.43 | +46475.3% | 18.8% | 0.27 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-consols-5pct | insure-check | train | 1867-01-31 | 1926-12-31 | 0.46 | +219.6% | 34.3% | 1.07 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-norway-perpetuity-15pct | insure-check | train | 1823-04-30 | 1984-12-31 | 0.61 | +20720.4% | 35.3% | 0.76 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-perpetuity | insure-check | train | 1823-04-30 | 1984-12-31 | 0.61 | +20720.4% | 35.3% | 0.76 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-consols-price-only | insure-check | train | 1867-01-31 | 1926-12-31 | 0.04 | +4.1% | 29.3% | 1.65 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-15.0% | insure-check | train | 1823-04-30 | 1984-12-31 | 1.43 | +46475.3% | 18.8% | 0.27 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-7.5% | insure-check | train | 1823-04-30 | 1984-12-31 | 1.43 | +46475.3% | 18.8% | 0.27 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-consols-15.0% | insure-check | train | 1867-01-31 | 1926-12-31 | 0.46 | +219.6% | 34.3% | 1.07 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-consols-7.5% | insure-check | train | 1867-01-31 | 1926-12-31 | 0.46 | +219.6% | 34.3% | 1.07 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-1822-1914 | insure-check | train | 1823-04-30 | 1914-08-31 | 2.09 | +3005.2% | 8.0% | 0.12 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-1915-1984 | insure-check | train | 1915-11-30 | 1984-12-31 | 1.10 | +1399.9% | 18.8% | 0.46 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-A1-GOV-1820-1920 | insure-check | train | 1823-04-30 | 1920-12-31 | 2.04 | +3458.8% | 8.0% | 0.15 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-lag-1 | insure-check | train | 1823-05-31 | 1984-12-31 | 1.43 | +49976.7% | 13.9% | 0.27 |
| 2026-11-25 23:01 | insure-bonds-1 | tsmom12m@insure-bonds-check-consols-lag-1 | insure-check | train | 1867-02-28 | 1926-12-31 | 0.57 | +336.7% | 21.6% | 1.07 |
| 2026-11-25 23:21 | insure-bonds-1 | tsmom12m@insure-bonds-check-norway-cash-discount-rate | insure-check | train | 1823-04-30 | 1984-12-31 | 1.57 | +83779.3% | 11.1% | 0.27 |
| 2026-11-25 23:21 | insure-bonds-1 | tsmom12m@insure-bonds-check-consols-cash-discount-rate | insure-check | train | 1867-01-31 | 1926-12-31 | 0.67 | +451.5% | 25.2% | 1.07 |
| 2026-11-25 23:27 | fx-peg-1 | correction (review of #222), description: the 23:03 note row's '23 FX markets' is 18 markets in 23 market-source rows; the post-hoc split is 0.931 (not 0.930) before 1946; unfinished-falls S median is 0.87 (not 0.88, read from rounded values); BoE M15 has a one-month spike 1857-10 (4.876, 8.924, 4.843 $/GBP): GBP-in-USD lag-1 acf -0.092 with it, +0.321 without the two changes, and a spurious 48% fall 1857-10..1861-01 in the unfiltered and peg-only books; the primary book never scores 1857, no verdict changes | note | train | - | - | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 (provisional id): French 49-industry VW Food excess minus 60-month beta x Mkt-RF, summed over months m+2..m+4, on D = -PDSI of the Corn Belt (nClimDiv 361) in month m, NW 3, 786 dose months 1960-01..2025-06 (b +0.009%/unit, t +0.07, rank 22/41 shifted calendars k = +-13..89 step 4, rank 23/41 phase surrogates seed 26; dose acf1 0.940, gate-null-2 'both' rule applied: gate FAIL; R43 not run) | screen | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: raw Food minus market, no beta (b -0.044, t -0.33) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: W32's dose, contiguous-US PDSI code 110 (b +0.053, t +0.41) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: drying PDSI(m-3)-PDSI(m), Corn Belt (b -0.008, t -0.04) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: 12-month horizon m+2..m+13, NW 12, 777 rows (b +0.086, t +0.20) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: growing-season dose months Jun-Sep only, 261 rows (b -0.121, t -0.49) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: restaurants (Meals) beta-adjusted (b +0.006, t +0.04) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: farms (Agric) beta-adjusted, no sign predicted (b +0.103, t +0.61) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: equal-weighted Food beta-adjusted (b -0.122, t -1.19) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: the market itself, Mkt-RF m+2..m+4 (b +0.246, t +1.59) | robustness | train | 1960-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:13 | drought-food-margin | W43 shown: dose months 2016-01 on, after Hong-Li-Xu's sample, 114 rows (b -0.327, t -2.02; post hoc placebo ranks 5/41 shifted, 2/41 surrogates; null SD 1.49 / 1.47; one drought episode 2022-10..2024-03): noted only | robustness | train | 2016-03-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:08 | heat-yield | wide-26 candidate, scored before any price, no number computed: H2, score 6 but same channel as H1 (processor input costs) with a meter needing daily station data (GHCN-daily, several GB): parked, joins H1's fate | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | snowpack-hydro | wide-26 candidate, scored before any price, no number computed: H3, score 4, filtered: regulated power-cost adjustment clauses pass most replacement-power cost to customers; one water year a year; firm prices not cached | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | reservoir-power | wide-26 candidate, scored before any price, no number computed: H4, filtered: power 0 (a handful of dry-year crises in Brazil and New Zealand; Nordic weight small) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | ndvi-crop | wide-26 candidate, scored before any price, no number computed: H5, filtered: duplicate of H1's channel; the yield news is scheduled (USDA reports); MODIS/VIIRS need an Earthdata login | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | ozone-yield | wide-26 candidate, scored before any price, no number computed: H6, filtered: size inside H1's noise; no keyless national ozone-season series by script | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | crop-pest | wide-26 candidate, scored before any price, no number computed: H7, filtered: power 0 (a handful of single-crop outbreaks) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | sst-fishery | wide-26 candidate, scored before any price, no number computed: H8, filtered: anchovy link is ENSO (W19 dead); salmon farmers trade in Oslo, not cached | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | wind-drought | wide-26 candidate, scored before any price, no number computed: H9, filtered: power 0 (about 15 annual doses), owners' prices not cached | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | solar-curtailment | wide-26 candidate, scored before any price, no number computed: H10, filtered: no listed reach; CAISO data from 2014 | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | rhine-low-water | wide-26 candidate, scored before any price, no number computed: H11, filtered: duplicate of wide-21 S3 river-freight (size); five or six low-water seasons; gauge history not keyless by script | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | wildfire-liability | wide-26 candidate, scored before any price, no number computed: H12, filtered: power 0 (a handful of utility fires, single firms) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | sea-level-flooding | wide-26 candidate, scored before any price, no number computed: H13, filtered: a smooth trend, no swinging dose; power 0 | note | train | - | - | - | - | - | - |
| 2026-11-25 23:08 | livestock-heat | wide-26 candidate, scored before any price, no number computed: H14, parked: same channel as H1; no national heat-stress series by script | note | train | - | - | - | - | - | - |
| 2026-11-25 23:17 | elimination-mood | W18 (wide-8's id, first gate; record-closing check, cards/wide-26b.md): losing country's index next-session log return minus the other cached markets, on D = 1 per knockout elimination (first knockout loss incl. penalties, World Cup and Euro finals, martj42 results), market dummies, DK 5, 25 markets, 122,576 rows, 74 eliminations (b -0.081%, t -0.95, rank 6/41 shifted calendars 23k days both ways; dose acf1 -0.001: gate FAIL; R18 not run) | screen | train | 2006-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:17 | elimination-mood | W18 shown: round weight, match number - 3 (b -0.032%, t -0.87) | robustness | train | 2006-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:17 | elimination-mood | W18 shown: group-stage exits (b -0.031%, t -0.26) | robustness | train | 2006-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:17 | elimination-mood | W18 shown: knockout wins as placebo dose (b -0.093%, t -1.09) | robustness | train | 2006-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:17 | elimination-mood | W18 shown: own return, no world subtraction (b -0.048%, t -0.34) | robustness | train | 2006-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:17 | elimination-mood | W18 shown: World Cup only (b -0.152%, t -1.73) | robustness | train | 2006-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:17 | elimination-mood | W18 shown: two sessions s0-1 to s0+1 (b -0.092%, t -0.61) | robustness | train | 2006-01-01 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-AUS | insure-check | train | 1901-12-31 | 1968-12-31 | 0.86 | +326.9% | 10.2% | 0.54 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-BEL | insure-check | train | 1871-12-31 | 2020-12-31 | 0.83 | +100629.1% | 15.7% | 0.39 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-CHE | insure-check | train | 1901-12-31 | 1938-12-31 | 1.31 | +300.9% | 0.6% | 0.28 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-DEU | insure-check | train | 1871-12-31 | 1938-12-31 | 1.32 | +1157.5% | 12.4% | 0.30 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-DNK | insure-check | train | 1876-12-31 | 2020-12-31 | 1.05 | +79300.5% | 11.0% | 0.44 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-ESP | insure-check | train | 1901-12-31 | 2017-12-31 | 1.07 | +57040.6% | 12.5% | 0.28 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-FIN | insure-check | train | 1871-12-31 | 2020-12-31 | 1.03 | +597691.9% | 11.8% | 0.35 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-FRA | insure-check | train | 1871-12-31 | 2020-12-31 | 0.86 | +98599.7% | 12.4% | 0.42 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-GBR | insure-check | train | 1928-12-31 | 1959-12-31 | 0.11 | +15.1% | 30.2% | 0.54 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-ITA | insure-check | train | 1886-12-31 | 2020-12-31 | 1.05 | +284100.5% | 12.2% | 0.40 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-JPN | insure-check | train | 1882-12-31 | 1988-12-31 | 1.38 | +30056.5% | 6.5% | 0.29 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-NLD | insure-check | train | 1871-12-31 | 2020-12-31 | 1.09 | +51205.7% | 9.9% | 0.39 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-PRT | insure-check | train | 1881-12-31 | 2020-12-31 | 0.99 | +733411.7% | 12.4% | 0.34 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-SWE | insure-check | train | 1872-12-31 | 1985-12-31 | 1.01 | +15045.7% | 10.7% | 0.41 |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-overlap: Check 1: overlapping years kept (all 16 countries); d 10.0%; Holds only as lower exposure; I > 0 in 11 of 15 anchored falls, S 0.87 vs fixed 0.70, G +0.003 (p AR 0.708, BB 0.879), P 2.96 | insure-check | train | 1871-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-disrupted: Check 2: disrupted years kept; d 10.0%; Holds only as lower exposure; I > 0 in 12 of 14 anchored falls, S 0.91 vs fixed 0.64, G +0.105 (p AR 0.543, BB 0.713), P 1.57 | insure-check | train | 1871-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-real: Check 3: events on the real index; d 10.0%; Does not hold; I > 0 in 11 of 14 anchored falls, S 0.43 vs fixed 0.40, G +0.054 (p AR 0.059, BB 0.247), P 1.54 | insure-check | train | 1872-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-cash0: Check 4: cash at 0 when out; d 10.0%; Holds only as lower exposure; I > 0 in 9 of 12 anchored falls, S 0.50 vs fixed 0.39, G +0.002 (p AR 0.502, BB 0.644), P 17.55 | insure-check | train | 1871-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-larger: Check 5a: next larger fall threshold; d 15.0%; Too few falls; I > 0 in 4 of 4 anchored falls, S 0.86 vs fixed 0.59, G +0.237 (p AR 0.209, BB 0.413), P 3.63 | insure-check | train | 1871-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-smaller: Check 5b: next smaller fall threshold; d 7.5%; Holds only as lower exposure; I > 0 in 15 of 21 anchored falls, S 0.82 vs fixed 0.74, G +0.151 (p AR 0.052, BB 0.105), P 1.82 | insure-check | train | 1871-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-pre: Check 6a: primary, scored years to 1965; d 10.0%; Too few falls; I > 0 in 6 of 8 anchored falls, S 0.70 vs fixed 0.59, G +0.102 (p AR 0.495, BB 0.216), P 1.49 | insure-check | train | 1871-12-31 | 1965-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-post: Check 6b: primary, scored years 1966-2020; d 10.0%; Too few falls; I > 0 in 3 of 4 anchored falls, S 1.34 vs fixed 0.87, G -0.051 (p AR 0.627, BB 0.925), P 4.34 | insure-check | train | 1966-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-primary-L1: primary: L1 signal year t-1 (trimmed); d 10.0%; Holds only as lower exposure; I > 0 in 9 of 11 anchored falls, S 0.97 vs fixed 0.71, G +0.000 (p AR 0.754, BB 0.878), P 2.63 | insure-check | train | 1872-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-primary-L2: primary: L2 signal year t-2 (trimmed); d 10.0%; Does not hold; I > 0 in 8 of 11 anchored falls, S 0.65 vs fixed 0.72, G +0.107 (p AR 0.122, BB 0.220), P 3.21 | insure-check | train | 1872-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-overlap-L1: overlap: L1 signal year t-1 (trimmed); d 10.0%; Holds only as lower exposure; I > 0 in 11 of 14 anchored falls, S 0.92 vs fixed 0.72, G -0.023 (p AR 0.833, BB 0.953), P 3.26 | insure-check | train | 1872-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:22 | insure-jstbonds-1 | tsmom12a@insure-jstbonds-overlap-L2: overlap: L2 signal year t-2 (trimmed); d 10.0%; Holds only as lower exposure; I > 0 in 10 of 14 anchored falls, S 0.62 vs fixed 0.73, G +0.002 (p AR 0.505, BB 0.471), P 4.05 | insure-check | train | 1872-12-31 | 2020-12-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44, wide-27: US French Mkt-RF over months v+1..v+3 on D(v) = ln of the 12-month mean of first + second payroll revisions (Philadelphia Fed monthly vintages, vintage v as of mid-month v) minus its trailing 120-month mean; controls real-time payroll growth g12, ln real-time volatility of monthly changes s12, market c12 and c1; NW 3; 427 months 1990-01..2025-07 (b +0.473% per unit of D, SD of D 0.35, t +0.24, rank 23/41 among earlier-dose calendars k = 25..103 odd (null SD 1.03, 5% past 2, 5/50/95% -0.93/+0.53/+1.89) and 19/41 among 40 phase surrogates (gating by gate-null-2's proposed rule, adopted; SD 0.96, 3% past 2); dose acf1 0.969): kill-only gate FAIL; R44 not run | screen | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: horizon 1 month, NW 0 (b +0.244, t +0.26) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: horizon 6 months, NW 6 (b +1.372, t +0.38) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: horizon 12 months, NW 12 (b -0.224, t -0.04) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: no controls (b +1.531, t +0.95) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: without s12 (b +0.873, t +0.61) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: first revision only (b +0.579, t +0.30) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: dose in levels (ln R12, no trailing mean) (b +0.350, t +0.17) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: rows 1990-01..2007-12 (b +6.942, t +1.30) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:32 | revision-noise | W44 shown: rows 2008-01..2025-07 (b -1.598, t -0.66) | robustness | train | 1990-01-31 | 2025-10-31 | - | - | - | - |
| 2026-11-25 23:28 | patent-surge | wide-27 candidate, scored before any price, no number computed: O1, scored 6 but parked: data (USPTO PTMT country tables 404 to a script, ALFRED/FRED copies unreachable tonight, PatentsView bulk over 1 GB); data lead | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | grant-backlog | wide-27 candidate, scored before any price, no number computed: O2, filtered: cause 0 and power 0 (one US pendency series) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | retraction-wave | wide-27 candidate, scored before any price, no number computed: O3, filtered: no reach (single papers, single firms) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | standard-freeze | wide-27 candidate, scored before any price, no number computed: O4, filtered: F1 fail (release freezes scheduled years ahead), duplicate of release engineering (wide-9) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | data-blackout | wide-27 candidate, scored before any price, no number computed: O5, filtered: power 0 (three or four data-stopping appropriation lapses in train) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | fed-research-tone | wide-27 candidate, scored before any price, no number computed: O7, scored 4, parked: cause 0, no keyless dated corpus scored by script | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | spectrum-auction | wide-27 candidate, scored before any price, no number computed: O8, filtered: power 0 (about ten large auctions, one sector), auction calendar announced | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | route-network | wide-27 candidate, scored before any price, no number computed: O9, filtered: data (route data paid), timetables filed ahead | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | postal-disruption | wide-27 candidate, scored before any price, no number computed: O10, filtered: power 0 and no index-level reach | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | method-change | wide-27 candidate, scored before any price, no number computed: O11, filtered: F1 fail (methodology changes announced ahead), duplicate of metrology | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | benchmark-revision | wide-27 candidate, scored before any price, no number computed: O12, folded into O6 (same channel; benchmark dates scheduled) | note | train | - | - | - | - | - | - |
| 2026-11-25 23:28 | wiki-attention | wide-27 candidate, scored before any price, no number computed: O13, filtered: F2 fail (attention follows prices), duplicate of attention-peak | note | train | - | - | - | - | - | - |
| 2026-11-26 00:02 | cabinet-drift | W41n, w41-neg-1 (`cards/w41-neg-1.md`, sign b < 0 fixed from W41's post-hoc negative side): next-year JST log equity return over bills minus the cross-country mean on D = 1 in a year with a ParlGov mid-term cabinet start (wide-25's event rule), controls own demeaned excess 1/3 years, country dummies, DK 2, 13 countries with rows (JST R6 has no CAN, IRL), 305 rows, 97 event rows, outcomes 1921-1959 without 1939-1946 minus the jst-autocorr-2 drop list (b -2.895% per event year, t -1.27, shift rank 5/21 from the bottom, k 2..21 (SD 1.22); AR-preserving bootstrap p 0.140, 199 paths (SD 1.18); halves -0.805 / -8.006; dose acf1 +0.178): kill-only gate DEAD (gate not met) | screen | train | 1921-12-31 | 1959-12-31 | - | - | - | - |
| 2026-11-26 00:02 | cabinet-drift | W41n shown: outcomes 1921-1938 (b -0.805, t -0.27, 178 rows) | robustness | train | 1921-12-31 | 1938-12-31 | - | - | - | - |
| 2026-11-26 00:02 | cabinet-drift | W41n shown: outcomes 1947-1959 (b -8.006, t -3.23, 127 rows; post hoc, not a lead) | robustness | train | 1947-12-31 | 1959-12-31 | - | - | - | - |
| 2026-11-26 00:02 | cabinet-drift | W41n shown: no controls (b -3.051, t -1.40) | robustness | train | 1921-12-31 | 1959-12-31 | - | - | - | - |
| 2026-11-26 00:02 | cabinet-drift | W41n shown: without France (b -2.119, t -0.82, 283 rows) | robustness | train | 1921-12-31 | 1959-12-31 | - | - | - | - |
| 2026-11-26 00:02 | cabinet-drift | W41n shown: without wide-25's post-election formations (b -3.024, t -1.35) | robustness | train | 1921-12-31 | 1959-12-31 | - | - | - | - |
| 2026-11-26 00:02 | cabinet-drift | W41n shown: count dose (b -3.017, t -1.40) | robustness | train | 1921-12-31 | 1959-12-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45, wide-28: US French Mkt-RF over months m+2..m+4 on D(m) = y/y log growth of three months of FBI NICS sales checks (handgun + long_gun + multiple, all states; BuzzFeed CSV 1998-11..2023-09; row m enters at the end of m+1); controls market c12, c1 and ln realised variance rv; NW 3; 182 months 2008-08..2023-09 (b +10.177% per unit of D, SD of D 0.179, t +3.50, rank 2/41 among earlier-dose calendars k = 25..103 odd (null SD 1.95, 40% past 2, 5/50/95% -2.34/+0.30/+3.19) and 2/41 among 40 IAAFT surrogates (end mismatch 4.46 SD; SD 1.52, 23% past 2); dose acf1 0.935): kill-only gate PASS; killed by R45 | screen | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | R45, replication of W45 (card wide-28): same rule on rows 2000-01..2008-05 (b +4.947, t +0.54, 101 rows, rank 13/41 among the gate's IAAFT surrogates; 17/41 among phase surrogates, the family the card's R45 text names, run 00:10): FAIL, W45 dead | screen | train | 2000-01-31 | 2008-09-30 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: horizon 1 month, NW 0 (b +3.403, t +1.86) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: horizon 6 months, NW 6 (b +19.487, t +4.03) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: horizon 12 months, NW 12 (b +29.877, t +3.90) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: no controls (b +10.659, t +4.13) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: without rv (b +10.753, t +4.16) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: one-month dose ln(S(m)/S(m-12)) (b +7.457, t +3.05) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: dose from totals (b +13.096, t +3.76) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: rows 2008-08..2015-12 (b +6.121, t +1.16) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: rows 2016-01..2023-09 (b +13.111, t +3.21) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:08 | arms-fear | W45 shown: without rows 2020-02..2021-06 (b +7.919, t +1.95) | robustness | train | 2008-08-31 | 2025-10-31 | - | - | - | - |
| 2026-11-26 00:05 | approval-mood | wide-28 candidate, scored before any price, no number computed: P2, scored 4, parked: the keyless approval history (presidency.ucsb.edu) disallows AI agents in robots.txt; not fetched | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | declaration-politics | wide-28 candidate, scored before any price, no number computed: P3, filtered: cause 0, duplicate of catastrophe meteorology (disaster counts) | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | road-deaths | wide-28 candidate, scored before any price, no number computed: P4, scored 4, parked: cause 0 (late, noisy trace of activity) | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | firm-births | wide-28 candidate, scored before any price, no number computed: P5, filtered: dating (Census BFS published only since 2018, earlier months back-filled), power | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | box-office | wide-28 candidate, scored before any price, no number computed: P6, filtered: data (weekly grosses not keyless to a script), cause 0 | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | chart-valence | wide-28 candidate, scored before any price, no number computed: P7, filtered: data (valence needs a keyed streaming API), published (Edmans et al. 2022) | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | trade-remedy | wide-28 candidate, scored before any price, no number computed: P8, filtered: no index-level reach, power 0, event studies published | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | conclave | wide-28 candidate, scored before any price, no number computed: P9, filtered: power 0 (a handful of events since 1958) | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | exam-season | wide-28 candidate, scored before any price, no number computed: P10, filtered: F1 fail (calendars set years ahead), duplicate of the calendar field | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | earth-rotation | wide-28 candidate, scored before any price, no number computed: P11, filtered: cause 0 | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | newspaper-strike | wide-28 candidate, scored before any price, no number computed: P12, filtered: power 0 (few strikes), published (Peress 2014; volume, not returns) | note | train | - | - | - | - | - | - |
| 2026-11-26 00:05 | benford-drift | wide-28 candidate, scored before any price, no number computed: P13, filtered: cause 0, power 0 | note | train | - | - | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4 (P4 pre-1927 stock markets US/GB/DE/FR, monthly, never scored for own-vol, DECIDING; pooled dSharpe vs tsmom12 -0.007, SE 0.021, z -0.34, one-sided 95% upper +0.028, d>0 in 2/4; not confirmed, not contradicted (too little power to tell); upper bound below #110's +0.06) | variant | train | 1868-08-01 | 1927-06-01 | 0.42 | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-P4-US | robustness | train | 1872-03-01 | 1927-06-01 | 0.41 | +387.8% | 29.3% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-US | robustness | train | 1872-03-01 | 1927-06-01 | 0.33 | +103.3% | 21.4% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-P4-GB | robustness | train | 1868-08-01 | 1924-12-01 | 0.39 | +126.5% | 31.0% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-GB | robustness | train | 1868-08-01 | 1924-12-01 | 0.44 | +99.2% | 22.4% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-P4-DE | robustness | train | 1871-03-01 | 1913-12-01 | 0.54 | +375.1% | 23.9% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-DE | robustness | train | 1871-03-01 | 1913-12-01 | 0.53 | +235.5% | 21.0% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-P4-FR | robustness | train | 1900-02-01 | 1927-06-01 | 0.35 | +94.0% | 32.1% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-FR | robustness | train | 1900-02-01 | 1927-06-01 | 0.37 | +64.3% | 23.5% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-without-US (pooled dSharpe vs tsmom12 +0.018, SE 0.020, z +0.91, one-sided 95% upper +0.051, d>0 in 2/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-without-GB (pooled dSharpe vs tsmom12 -0.026, SE 0.025, z -1.04, one-sided 95% upper +0.015, d>0 in 1/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-without-DE (pooled dSharpe vs tsmom12 -0.007, SE 0.024, z -0.27, one-sided 95% upper +0.033, d>0 in 2/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-without-FR (pooled dSharpe vs tsmom12 -0.015, SE 0.028, z -0.53, one-sided 95% upper +0.031, d>0 in 1/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-sized-months-only (pooled dSharpe vs tsmom12 +0.001, SE 0.028, z +0.05, one-sided 95% upper +0.047, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-gap-1-everywhere (pooled dSharpe vs tsmom12 -0.009, SE 0.021, z -0.45, one-sided 95% upper +0.025, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-cost-50-bps (pooled dSharpe vs tsmom12 -0.010, SE 0.021, z -0.46, one-sided 95% upper +0.025, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-blocks-6 (pooled dSharpe vs tsmom12 -0.007, SE 0.024, z -0.30, one-sided 95% upper +0.032, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-blocks-24 (pooled dSharpe vs tsmom12 -0.007, SE 0.021, z -0.34, one-sided 95% upper +0.027, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-US-with-dividends (pooled dSharpe vs tsmom12 +0.010, SE 0.018, z +0.60, one-sided 95% upper +0.039, d>0 in 2/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-1867-1897 (pooled dSharpe vs tsmom12 -0.078, SE 0.051, z -1.54, one-sided 95% upper +0.005, d>0 in 0/3) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-P4-check-1898-1927 (pooled dSharpe vs tsmom12 +0.024, SE 0.016, z +1.48, one-sided 95% upper +0.051, d>0 in 3/4) | robustness | train | 1868-08-01 | 1927-06-30 | - | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-N5 (N5 DK/FI/IE/NO/SE French country files 1975-2025, new markets but years overlap the 41, secondary; pooled dSharpe vs tsmom12 +0.010, SE 0.026, z +0.39, one-sided 95% upper +0.052, d>0 in 4/5; not confirmed, not contradicted (too little power to tell); upper bound below #110's +0.06) | variant | train | 1976-01-01 | 2025-10-01 | 0.58 | - | - | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-N5-DK | robustness | train | 1990-01-01 | 2025-10-01 | 0.71 | +2566.0% | 31.0% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-N5-DK | robustness | train | 1990-01-01 | 2025-10-01 | 0.74 | +1138.4% | 19.0% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-N5-FI | robustness | train | 1989-01-01 | 2025-10-01 | 0.57 | +2584.1% | 41.8% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-N5-FI | robustness | train | 1989-01-01 | 2025-10-01 | 0.54 | +875.5% | 35.2% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-N5-IE | robustness | train | 1992-01-01 | 2025-10-01 | 0.46 | +707.4% | 55.3% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-N5-IE | robustness | train | 1992-01-01 | 2025-10-01 | 0.50 | +392.7% | 39.4% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-N5-NO | robustness | train | 1976-01-01 | 2025-10-01 | 0.54 | +6956.6% | 39.9% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-N5-NO | robustness | train | 1976-01-01 | 2025-10-01 | 0.54 | +3015.1% | 33.3% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | tsmom12@indep-N5-SE | robustness | train | 1976-01-01 | 2025-10-01 | 0.59 | +8609.9% | 44.7% | - |
| 2026-11-26 00:10 | ownvol-indep-1 | own_vol_70@indep-N5-SE | robustness | train | 1976-01-01 | 2025-10-01 | 0.60 | +2901.6% | 32.2% | - |
