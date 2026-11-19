# Micro 1: do minute-bar features forecast the coming week? (screen, don't trade)

Research run micro-1, 2026-11-18. Branch `micro-1` (from `carry-2`). Descriptive only: no
backtest, no strategy, held-out year not loaded.

Question: every weekly input screened so far stays under a weekly IC of ~0.05 (`rl-3.md`,
`info-1.md`; volume-1, draft PR #41, found the same for own volume). The minute bars in the
raw-data cache (ingest 1 and 2) have never been used. Do realised volatility, jumps, or the
overnight/intraday split of the return, built from minute bars, reach a weekly IC of ~0.10?

## In plain words (results, 2026-11-18)

**No. None of the six minute-bar features forecasts the coming week. The largest in-sample IC
is +0.030 (`overnight13`), under half the family chance level (0.064) and under its own
single-test level (0.049). The best walk-forward IC is +0.048 and the best gain over the trend
inputs is +0.021 (both `intraday13`), against bars of 0.10 and +0.05. All six verdicts are
"no", so by the card the lane is closed: no re-run with other windows.** Descriptive only: no
backtest, held-out year not loaded. Table: `results/micro-1.md`.

- **What was measured.** Change and 52-week z-score of realised volatility (five-minute
  returns), the share of variance from jumps, signed jumps, and 13-week t-statistics of the
  overnight and the intraday return, each on the asset's own minute bars, used from the day
  after. 513 Fridays 2016-2025, about 2,950 asset-weeks (5.4 million BTC minute bars, 2.0
  million for SPY), the same target as info-1 and volume-1.
- **Honest reading of the numbers.**
  - The four volatility and jump features are new information (overlap with the trend inputs
    0.11-0.18) with no forecasting power: |IC| 0.000-0.018, walk-forward -0.05 to 0.00, and
    every one makes the trend forecast slightly worse (gain -0.004 to -0.036).
  - The overnight and intraday t-statistics are mostly the trend again (overlap 0.75 and
    0.62). `overnight13` has the largest IC (+0.030) and nothing out of sample (+0.007 at best).
  - `intraday13` is the only number near a bar: walk-forward +0.048 with a slope per asset,
    gain +0.021. Its in-sample IC is +0.012, a fifth of the family level, so it is not a
    "second look" by the card. The per-asset signs differ (coins +0.07 to +0.09, SPY and QQQ
    -0.06): trend in the coins, reversal in the stock ETFs. With 36 asset-candidate pairs and
    ~500 weeks each, numbers of that size are what chance gives. Shown, not judged.
- **How sure.** Less sure than volume-1, and only about large effects. Ten years gives a
  family chance level of 0.064 (volume-1: 0.048 on 26 years). A real IC of 0.10 would stand
  clear of it and nothing reaches half; a real IC of 0.03-0.05 cannot be told from zero on
  this history, and the walk-forward has three test blocks. Since rl-3's ceiling gives nothing
  below ~0.10 on this book, the conclusion that matters holds: nothing here is worth an RL run.
- **What it means.** Minute-bar volatility, jumps and the overnight/intraday split join
  prices, macro, on-chain, positioning, options and volume: no weekly input within reach of
  free data lifts this six-asset book above the 12-month trend.

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

### Disclosures (2026-11-18)

- Order, by commit: card (`a2a5b49`, stamped 11:09 UTC; the heading's "~11:10" was a guess),
  then code and tests (`e56545a`, pushed before the screen ran), then the one run with `--log`
  (six `screen` rows in `tries.md`). No dry run of the screen before it.
- The daily table was built after the card commit (it finished about when the code was
  committed, before the screen ran), by `micro1_days.py` as it stood before
  `ruff format` re-wrapped it (layout only; the committed file is the formatted one). Its log (minute bars and days per asset) was read before the
  screen ran: SPY/QQQ/GLD/TLT 2,478 days each, BTC 3,767, ETH 3,457. No other number was seen
  before the result table.
- `overnight` runs from the last close of the previous day **present in the table**; after a
  day dropped for too few bars it spans that day too. The card said "the previous session day".
- Coins sit on a calendar grid (a UTC day with no row is a missing day); for ETFs the rows are
  the session days, so a holiday is not a missing day.
- `rv_z52` starts 2016-01-29 and the others 2016-01-08 through BTC alone (its minute bars start
  2015-07-20); the ETFs join as their windows fill during 2016.
- The Alpaca minute bars were downloaded by ingest 1 with the owner's free key. Nothing was
  downloaded here. The bar and RL table caches (git-ignored) were copied read-only from the
  `volume-1` worktree, the local config file from `carry-3`'s.
- Not corrected, as the card said: ex-dividend drops in the ETFs' `overnight`.
- `ledger/tries.jsonl` has no rows: a screen is not a strategy (as info-1 and volume-1).

## Status (2026-11-18 ~11:16 UTC)

**Done:** card; `lib/micro1_days.py` (daily table from the minute bars, run with `python -I`);
`lib/micro1_ic.py` (features, family chance level, table; reuses `info1_ic.py` and
`info1_features.asof`); `tests/test_micro1.py`; table `results/micro-1.md`; six `screen` rows
in `tries.md`; this write-up; draft PR #46 (`micro-1` -> `carry-2`), not merged. Held-out year
untouched.

**Doing:** nothing half-finished. No process left running.

**Next:** nothing in this lane (closed by its own card). Minute bars could still matter at
their own horizon (the next day or the next hour), which is a different question from a weekly
input and needs its own card and cost model.

Reproduce: `.venv/bin/python -I research/lib/micro1_days.py <cache root>` (needs ingest 1's
`alpaca/1m-sip` and `coinbase/1m` folders), then `uv run python research/lib/micro1_ic.py`
(dry; `--log` writes tries rows: run once). Needs the bar cache (`research/lib/fetch.py`), RL
2's `tables2.pkl` (`rl2_data.py`) and `research/macro.local.json`.
