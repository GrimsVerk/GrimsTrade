# Volume 1: does the six assets' own trading volume forecast? (screen, don't trade)

Research run volume-1, 2026-11-18. Branch `volume-1` (from `carry-2`). Descriptive only: no
backtest, no strategy, held-out year not loaded.

Question: every weekly input screened so far (prices, macro, on-chain, positioning, options,
cross-asset; `rl-3.md`, `info-1.md`) stays under a weekly IC of ~0.05. The six assets' own
trading volume, which sits in the bar cache already, has never been screened. Does any volume
feature reach the level where it is worth anything on this book (weekly IC ~0.10)?

## In plain words (results)

Not run yet. This section is filled in after the one logged run.

## Card (written 2026-11-18 ~11:07 UTC, before any volume number was computed or printed)

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
