# Micro 1: do minute-bar features forecast the coming week? (screen, don't trade)

Research run micro-1, 2026-11-18. Branch `micro-1` (from `carry-2`). Descriptive only: no
backtest, no strategy, held-out year not loaded.

Question: every weekly input screened so far stays under a weekly IC of ~0.05 (`rl-3.md`,
`info-1.md`; volume-1, draft PR #41, found the same for own volume). The minute bars in the
raw-data cache (ingest 1 and 2) have never been used. Do realised volatility, jumps, or the
overnight/intraday split of the return, built from minute bars, reach a weekly IC of ~0.10?

## Card (written 2026-11-18 ~11:10 UTC, before any minute-bar number was computed or printed)

Seen before: every earlier result in this repo, volume-1's card and result included. Seen of
the minute data: the folder listing (file names, counts, sizes) and the first 600 bytes of one
SPY file and 300 bytes of one BTC file, to learn the format. Not seen: any statistic.

### History length (disclosure, from the folder listing)

| Asset | Source (cache path) | First file | Train years |
| --- | --- | --- | ---: |
| SPY, QQQ, GLD, TLT | Alpaca 1m SIP, raw prices (`alpaca/1m-sip/<SYM>/<YYYY-MM>.json`) | 2016-01 | ~9.9 |
| BTC | Coinbase 1m (`coinbase/1m/BTC-USD/<year>/`) | 2015 (from 2015-07-20) | ~10.3 |
| ETH | Coinbase 1m (`coinbase/1m/ETH-USD/<year>/`) | 2016 (from 2016-05-18) | ~9.5 |

**About 10 years, against 26 for volume-1 and info-1**: ~510 Fridays and ~3,000 asset-weeks
at most, under half of volume-1's 5,850. The chance levels will be wider for it (expected
single-test level ~0.05, family ~0.07), so a true IC of 0.05 cannot be told from zero here; a
true 0.10 still can. The walk-forward has three test blocks only (2020-21, 2022-23, 2024-25).
Files dated after the train cut (2025-11-09) exist in the cache; days after the cut are dropped
when the daily table is built and never reach a statistic.

### Target, rows, period

- Target `z` = `rl3_plant.week_z` on RL 2's `six` table (as info-1 and volume-1).
- Rows: every Friday 2016-01-08 .. end of train (2025-11-09) and asset of the six that is
  eligible and has a finite target and a finite feature.

### Data and as-of rule

- Session = 09:30-16:00 New York time (daylight saving from the tz database; the offset of
  12:00 UTC that day). Five-minute returns: log differences of the sequence [open of the first
  bar in the window, last close in each five-minute bin that has a bar]. A day needs >= 30
  five-minute returns, else it is missing.
- ETFs: window = the session; day = the New York date. `RV` = sum of squared five-minute
  returns, `BV` = (pi/2) x sum |r_i| |r_(i-1)| x n/(n-1) (bipower variation), `RS+`/`RS-` =
  the sums of squared positive/negative returns. `intraday` = log(last session close / first
  session open); `overnight` = log(first session open / the previous session day's last close).
- Coins: `RV`, `BV`, `RS+`, `RS-` on the whole UTC day (288 bins); `intraday` and `overnight`
  split at the same New York session (inside 09:30-16:00 against the rest of the day).
- Alpaca prices are raw: an ex-dividend drop sits in `overnight`. None of the four ETFs split
  in the period. Not corrected.
- A day dated `x` is used from `x + 1` (`info1_features.asof(..., lag=1)`): the Friday decision
  uses days through Thursday. A value older than 21 days is missing. A window needs >= 80% of
  its days present, else NaN.

### Candidates (6, fixed now)

`W` = days per week: 5 for ETFs, 7 for coins. Windows trailing, ending at the day itself.

1. `rv_chg` = log(mean `RV` over the last W days / mean `RV` over the last 13W days).
2. `rv_z52` = `x` = log(mean `RV` over the last W days); (`x` - mean of `x` over the last 52W
   days) / their sd (>= 26W values).
3. `jump4` = 1 - sum(`BV`) / sum(`RV`) over the last 4W days (share of variance from jumps).
4. `sjump4` = (sum `RS+` - sum `RS-`) / sum `RV` over the last 4W days (signed jumps).
5. `overnight13` = mean(`overnight`) / sd(`overnight`) x sqrt(n) over the last 13W days.
6. `intraday13` = the same for `intraday`.

### Measures, chance level, bars (as volume-1's card)

- Per candidate: coverage; in-sample pooled IC (Pearson), rank IC, IC per asset (shown, not
  judged); walk-forward IC (OLS refitted every two years on Fridays before `y0 - 1`, per-asset
  slopes and pooled slope, a block needs >= 104 training weeks); overlap with the seven trend
  inputs and the walk-forward gain over them. Code reused from `lib/info1_ic.py`.
- Chance: 500 circular shifts of >= 52 weeks inside the 2016-2025 window (seed 0), the same
  shifts for all six. Single-test level = 95th percentile of |IC|. **Family level (maxT)** =
  95th percentile over the shifts of the largest |IC| among the six. A candidate is above
  chance only above the family level.
- **Useful**: in-sample |IC| above the family level, and walk-forward IC (per-asset or pooled,
  the better) >= 0.10 or gain over the trend inputs >= +0.05. **Second look**: above the family
  level and walk-forward IC >= 0.05. Otherwise **no**. A "no" for all six closes the lane: no
  re-run with other windows.
- If one is useful: nothing is traded here; the next step would be its own card.

### Logging

One logged run. Every candidate gets one `screen` row in `tries.md`. Table in
`results/micro-1.md`. Nothing is downloaded. The raw minute files are read by one script run
with `python -I` (`lib/micro1_days.py`, standard library and numpy only), which writes a daily
table under the cache root (`derived/micro-1/`, never committed); the screen reads that table.
