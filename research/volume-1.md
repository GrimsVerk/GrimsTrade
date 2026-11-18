# Volume 1: does the six assets' own trading volume forecast? (screen, don't trade)

Research run volume-1, 2026-11-18. Branch `volume-1` (from `carry-2`). Descriptive only: no
backtest, no strategy, held-out year not loaded.

Question: every weekly input screened so far (prices, macro, on-chain, positioning, options,
cross-asset; `rl-3.md`, `info-1.md`) stays under a weekly IC of ~0.05. The six assets' own
trading volume, which sits in the bar cache already, has never been screened. Does any volume
feature reach the level where it is worth anything on this book (weekly IC ~0.10)?

## In plain words (results, 2026-11-18)

**No. None of the six volume features forecasts the coming week. The largest in-sample IC is
-0.021, under half the family chance level (0.048) and under every single-test chance level
(0.034-0.040). The best walk-forward IC is +0.017 and the best gain over the trend inputs is
+0.002, against bars of 0.10 and +0.05. All six verdicts are "no", so by the card the lane is
closed: no re-run with other windows.** Descriptive only: no backtest, held-out year not
loaded. Table: `results/volume-1.md`.

- **What was measured.** 4- and 13-week volume change, a 52-week abnormal-volume z-score, a
  13-week volume-weighted trend, up-day against down-day volume, and price-volume divergence,
  each on the asset's own bars, used from the day after the bar. 1,348 Fridays 2000-2025,
  about 5,850 asset-weeks, the same target as info-1 (the coming week's risk-adjusted return).
- **Honest reading of the numbers.**
  - The three pure volume features (`vol_chg4`, `vol_chg13`, `vol_z52`) are new information
    (overlap with the trend inputs 0.08-0.14) with no forecasting power: |IC| 0.009-0.012,
    walk-forward -0.02 to 0.00. Adding them to the trend inputs makes the forecast slightly
    worse (gain -0.006 to -0.022).
  - The volume-weighted trend is the trend again (overlap 0.82) and adds +0.002.
  - Price-volume divergence has the same sign for all six assets (-0.014 to -0.032: a move on
    rising volume is followed by a slightly weaker week), which is the only pattern in the
    table. Pooled it is -0.021, half the family level, walk-forward +0.017, gain +0.001. Too
    small to matter even if real: rl-3's ceiling gives nothing below 0.05.
  - Per asset, the coins show the largest numbers (`vol_z52` +0.078 for ETH, `vw_trend13`
    +0.071 for BTC). With 36 asset-candidate pairs and under 500 weeks per coin, that is chance-sized,
    and it does not carry into the walk-forward numbers. Shown, not judged (card).
- **How sure.** Sure. 1,348 weeks and a family chance level of 0.048: a real 0.10 would stand
  two chance levels clear, and nothing reaches a quarter of it. The one thing this cannot
  rule out is a coin-only volume effect, which needs more coins than two (the wide coin book;
  breadth-1 found a volume-to-market-cap tilt there, across coins, not through time).
- **What it means.** Own volume joins prices, macro, on-chain, positioning and options: no
  weekly input within reach of free data lifts this six-asset book above the 12-month trend.

## Card (written 2026-11-18 ~11:03 UTC, before any volume number was computed or printed)

Seen before: every earlier result in this repo (the info-1 table included: no candidate
useful, best walk-forward gain +0.025). Not seen: any statistic of the volume columns.

### Target, rows, period (same as `results/info-1.md`)

- Target `z` = `rl3_plant.week_z` on RL 2's `six` table: the log return the Friday decision
  holds (first open after Friday to the first open after the next Friday), over the asset's
  EWMA vol x sqrt(7/365), clipped to +-5.
- Rows: every Friday 2000-01-07 .. end of train (2025-11-09) and asset of the six that is
  eligible and has a finite target and a finite feature. Bars after the train cut are not
  loaded (`harness.load_history("train")`; the table stops there too).

### Data and as-of rule

- Volume = the `volume` column of the research bar cache (`research/data/bars`, the keyless
  public sources of `lib/fetch.py`: Yahoo for the ETFs, Bitstamp/Coinbase for the coins), in
  shares or coins. Returns inside the features come from the same bars' adjusted closes.
- A bar dated `x` is used from `x + 1` (info-1's market rule, `asof(..., lag=1)`): the Friday
  decision uses bars through Thursday, for ETFs and coins alike. Conservative: the gym would
  let the decision see Friday's ETF bar.
- A bar with volume <= 0 is missing. A window needs >= 80% of its bars present, else NaN.
- **BTC venue switch.** The BTC bars are Bitstamp to 2015-07-19 and Coinbase after, so the
  volume level jumps there. BTC volume before 2015-07-20 is not used at all.
- Every feature is a ratio or a z-score inside one asset's own history, so units (shares,
  coins) and the slow drift in volume levels drop out.
- A feature value older than 21 days at the decision is missing (info-1's rule).

### Candidates (6, fixed now; exact formulas)

`W` = bars per week: 5 for ETFs, 7 for coins. `V` = daily volume, `r` = daily log return of the
close, all windows trailing and ending at the bar itself.

1. `vol_chg4` = log(mean `V` over the last 4W bars / mean `V` over the 4W bars before them).
2. `vol_chg13` = the same with 13W.
3. `vol_z52` = abnormal volume: `x` = log(mean `V` over the last W bars); (`x` - mean of `x`
   over the last 52W bars) / their sd (>= 26W values).
4. `vw_trend13` = volume-weighted trend: sum(`V` x `r`) / sum(`V`) over the last 13W bars,
   divided by sd(`r`) over the same bars / sqrt(number of bars) (a t-statistic-like number).
5. `updown13` = `vw_trend13` minus the same number with equal weights (mean(`r`) in the
   numerator): positive when the up days had the larger volume.
6. `pv_div13` = price-volume divergence: sign(sum of `r` over the last 13W bars) x `vol_chg13`.
   Positive = the 13-week move came with rising volume; negative = with falling volume.

### Measures (per candidate; code reused from `lib/info1_ic.py`)

Coverage; in-sample pooled IC (Pearson), rank IC, IC per asset; walk-forward IC (OLS refitted
every two years 2000..2024 on Fridays before `y0 - 1`, per-asset slopes and pooled slope, a
block needs >= 104 training weeks); overlap with the seven trend inputs and the walk-forward
gain over them. All exactly as info-1's card, "Measures".

### Chance level and multiple-testing correction (fixed now)

- 500 circular shifts of >= 52 weeks (seed 0). **The same 500 shifts are applied to all six
  candidates.** Per candidate: the 95th percentile of |IC| over the shifts (single-test level,
  as info-1).
- **Family level (maxT):** for each shift, the largest |IC| among the six candidates; the 95th
  percentile of that maximum is the family chance level. A candidate counts as above chance
  only if its in-sample |IC| is above the **family** level. This is the correction for having
  six tries (Westfall-Young maxT; it keeps the candidates' correlation with each other).
- The per-asset table (36 numbers) is shown, not judged.

### What counts (fixed now; info-1's bar with the family level)

- **Useful**: in-sample |IC| above the family chance level, and walk-forward IC (per-asset or
  pooled, the better) >= 0.10 or walk-forward gain over the trend inputs >= +0.05.
- **Second look**: in-sample |IC| above the family chance level and walk-forward IC >= 0.05.
- Otherwise **no**. A "no" for all six closes the lane: no re-run with other windows.
- If one is useful: nothing is traded here. The next step would be its own card (rl-3's
  planted-signal gate on the real feature).

### Logging

One logged run. Every candidate gets one `screen` row in `tries.md` (descriptive, not
selectable). Table in `results/volume-1.md`. Nothing is downloaded: the bar cache is the one
`lib/fetch.py` built (git-ignored, copied read-only from another worktree, never committed).

### Disclosures (2026-11-18)

- The card's heading first said "~11:07 UTC", a guess; the card commit (`8aaf620`) is stamped
  11:03 UTC, and the heading now says so. Nothing else on the card changed after the run.
- Order, by commit: card (`8aaf620`), then code and tests (`4a4be0d`, pushed before the run),
  then the one run with `--log` (six `screen` rows in `tries.md`). No dry run and no coverage
  print before it; the first volume numbers seen were the result table.
- The bar and RL table caches (git-ignored) were copied read-only from the `slow-1` worktree.
  Nothing was downloaded.
- Not on the card, so not shown: info-1's "IC held" column.
- `ledger/tries.jsonl` has no rows: a screen is not a strategy (as info-1).

## Status (2026-11-18 ~11:10 UTC)

**Done:** card; `lib/volume1_ic.py` (features, family chance level, table; reuses
`info1_ic.py` and `info1_features.asof`); `tests/test_volume1_asof.py`; table
`results/volume-1.md`; six `screen` rows in `tries.md`; this write-up; draft PR #41 (`volume-1` ->
`carry-2`), not merged. Held-out year untouched.

**Doing:** nothing half-finished. No process left running.

**Next:** nothing in this lane (closed by its own card). If volume is tried again it should be
across many coins (the wide coin book), as its own card, not through time on six assets.

Reproduce: `uv run python research/lib/volume1_ic.py` (dry; `--log` writes tries rows: run
once). Needs the bar cache (`research/lib/fetch.py`) and RL 2's `tables2.pkl` (`rl2_data.py`).

## Card 2: volume across many coins (written 2026-11-18 ~11:16 UTC, before any number)

Asked for by the coordinator at ~11:15 UTC as a continuation of this lane. The card was
committed first as "card only, not run" (`c3c351d`), because the time looked too short; the
code and test then went in (`6f281fb`, pushed before the run) and the screen ran once
at ~11:19 UTC. The card text below is unchanged apart from this paragraph and the heading.

### Result of card 2 (2026-11-18)

**No. Across the top-100 coin book too, none of the six volume features passes. The largest
cross-sectional weekly rank IC is -0.020 (`vol_chg4`), under half the family chance level
(0.043) and under the card's 0.03 floor. All six verdicts are "no"; the lane closes.** 344
Fridays 2019-04-05 to 2025-11-09, about 89 coins a week, train only. Table:
`results/volume-1-coins.md`.

- The one pattern: coins whose volume has just jumped do slightly worse the next week
  (`vol_chg4` -0.020, t -2.3; `vol_z52` -0.019, t -1.8; negative in both eras). Both are
  just above their own single-test chance levels (0.017, 0.016) and well below the family
  level, which is what the correction is for: one of six looking like this is expected. The
  sign agrees with breadth-1's low-turnover tilt in this book, so it is not new information.
- The trend-like features (`vw_trend13`, `updown13`) have high chance levels (0.034, 0.043),
  which set the family level; they show nothing either.
- Deviations from the card, all disclosed: the first Friday is 2019-04-05, not 2019-01-04
  (the book's own start rule, 30 eligible coins, begins there); the rank correlation breaks
  ties by column order instead of averaging them (continuous inputs; ties are rare); the
  loader check is done: cointop-1 uses `breadth_books.cm_book()`, the one used here.
- No dry run before the logged run. The shared-cache pointer (`macro.local.json`,
  git-ignored) was copied from another worktree; the train-cut panel `cm-panel.npz` was read,
  the held-out panel was not.

### Card 2 as written

Seen before: the six-asset table above (all "no"); breadth-1's summary that a tilt toward low
volume-to-market-cap coins helped the trend rule in this same book, and that the book already
carries a `vol_growth` signal (7-day over 91-day volume). So volume in this book is not a
fully fresh look; that counts against any pass here. Not seen: any IC of the features below.

- **Book.** The Coin Metrics top-100 coin book, dead coins included
  (`breadth_books.cm_book(top_n=100)`, train cut, eligibility and all inputs lagged one day).
  To check before the run, not yet checked: that this is the panel cointop-1 cached; if
  cointop-1 uses another loader, use that one and say so here before running.
- **Volume** = `volume_reported_spot_usd_1d` (USD, reported by exchanges: inflated on some
  venues, which is one reason for ranks below). Price = `PriceUSD`.
- **Features.** The same six, same formulas, `W` = 7 (`volume1_ic.daily_features`).
- **Target.** The coming week's log return (decision Friday's usable price to the next
  Friday's) over the coin's 90-day vol x sqrt(7/365), clipped to +-5.
- **IC.** Cross-sectional: per Friday, the Spearman rank correlation across eligible coins
  with a finite feature and target (at least 20 coins); the IC is its mean over Fridays
  2019-01-04 .. 2025-11-09. Also shown: t-statistic of the weekly ICs, share of weeks
  positive, eras 2019-21 and 2022-25.
- **Chance and correction.** The feature panel circularly shifted in time by >= 52 weeks, 500
  shifts (seed 0), the same shifts for all six; family level = 95th percentile of the largest
  |mean IC| among the six (maxT), as above.
- **What counts.** Useful: |mean IC| above the family level, at least 0.03, and the same sign
  in both eras. Second look: above the family level only. Otherwise no, and the lane closes.
- **Logging.** One run; six `screen` rows in `tries.md` (idea `volume-1-coins-screen`); table
  `results/volume-1-coins.md`. A test first: the cross-sectional IC finds a planted rank
  signal and gives ~0 on noise; features unchanged when future rows are scrambled.
