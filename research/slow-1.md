# Slow 1: do our inputs forecast at 4 and 13 weeks, where they failed at 1 week?

Research run slow-1, 2026-11-18. Branch `slow-1` (from `carry-2`). Follows info-1's "levers
left" #3: "COT and valuation-type inputs (Puell, VRP) are documented at monthly-to-quarterly
horizons. A 4-week or 13-week target is a new card, not a re-read of this table."

Question: info-1 and rl-3 measured 50 inputs against **next week's** return and found nothing
(best walk-forward gain +0.025, bar 0.10). Do the same inputs forecast the next **4 weeks** or
the next **13 weeks** of our six assets well enough to tilt `tsmom12`?

Not a repeat of invest-1. invest-1 asked whether valuation, yields and inflation improve a
monthly stock/bond/cash allocation over 60/40, 1927-2025, at 1- to 10-year horizons. slow-1 is
the trading book: our six assets (BTC, ETH, SPY, QQQ, GLD, TLT), weekly decisions, `tsmom12` as
the twin, 2000-2025, positioning / options / crypto / on-chain / macro inputs, horizons of one
month and one quarter.

## In plain words

(Results go here. Nothing has been computed when this card is committed.)

## Card (written 2026-11-18, before any slow-horizon number was computed)

What had been seen when this was written: the published weekly tables (`results/info-1.md`,
`results/rl-3-inputs.md`) and one plumbing print of the RL table's shape and dates (1,658
Fridays 1994-02-04 .. 2025-11-07, bars to 2025-11-10; no target, no IC).

### Targets

`z_h` for `h` = 4 and 13 weeks, on RL 2's `six` table: the log return from the first open after
Friday `i` to the first open after Friday `i + h`, divided by the asset's EWMA volatility at
Friday `i` x sqrt(7h / 365), clipped to +-5. For `h` = 1 this is `rl3_plant.week_z` exactly (a
test proves it). A cell needs the asset eligible at Friday `i` (a year of bars) and the closing
open inside the train bars (so the last 13-week row is a Friday in early August 2025). Bars after
2025-11-10 are not in the table: the held-out year is not loaded.

**Overlap.** Rows are every Friday, so consecutive `h`-week targets overlap in `h - 1` of their
`h` weeks. The point estimates use all Fridays. **No standard error here is 1/sqrt(rows).**
Every chance level comes from a circular-shift null (below), which keeps the overlap in the
target, the persistence of the input and the co-movement of the six assets. As a cross-check
each IC is also computed on non-overlapping rows (every `h`-th Friday), for each of the `h`
possible starting weeks: the table shows their mean and their min..max.

### Rows and period

Fridays 2000-01-07 .. end of train, the six assets, every cell with a finite target and a
finite input. Same as `results/info-1.md` apart from the horizon.

### Inputs (49; no new data)

- **info-1's 23**, formulas and as-of rules unchanged (`lib/info1_features.py`, card
  `research/info-1.md`): `cot_spec`, `cot_spec_chg4`, `cot_spec_z3y`, `cot_lev`, `cot_am`,
  `fund_bn`, `prem_bn`, `fund_drb`, `dvol_rv`, `puell`, `hash_growth`, `tx_growth`, `fng`,
  `vix_term`, `vix_term6`, `skew_z`, `vvix_vix`, `vrp`, `pc_total`, `pc_equity`, `usd_13w`,
  `oil_13w`, `hy_ief_13w`.
- **rl-3's real inputs, 26 of its 27** (`results/rl-3-inputs.md`): the 15 price features of
  `ml.py` (`z7`, `z30`, `z91`, `z182`, `z365`, `up_12m`, `sma_gap`, `log_vol`, `vol_shock`,
  `dd_1y`, `since_high`, `breadth`, `univ_mom_1m`, `univ_vol_shock`, `rank_12m`), `halving`
  (coins only; missing for the other four), and the 10 macro inputs (`dff30`, `dff_chg182`,
  `real_ff`, `curve`, `baa20`, `real_m2`, `unrate_rise`, `cpi_yoy`, `dgs10`, `vix`). The 27th,
  `coin`, is a constant per asset, not a forecast: left out.
- The seven **trend inputs** (`z7`, `z30`, `z91`, `z182`, `z365`, `up_12m`, `sma_gap`) are what
  `tsmom12` already has. They are measured and counted in the correction, but a trend input over
  the bar is not new information and triggers no trading card (run 2 traded them: `ml-linear`,
  `ensemble-tsmom`, `fracdiff-momentum`).
- No transformations are added for the slow horizons (no smoothing, no extra lags): each one
  would be another test.

### Measures (per input and horizon)

1. **Coverage**: first date, weeks, cells.
2. **In-sample IC**: Pearson correlation of the input with `z_h` over all cells; Spearman (rank)
   IC; IC inside the cells `tsmom12` holds; IC per asset (descriptive table).
3. **Non-overlapping IC**: as above (mean and min..max over the `h` starting weeks).
4. **Walk-forward IC** (info-1's scheme, unchanged): ordinary least squares refitted every two
   years (2000, 2002, ..., 2024) on Fridays of years before `y0 - 1`, predicting `y0 .. y0 + 1`;
   inputs standardised on the training rows; a block is skipped with fewer than 104 training
   weeks. Two models: a slope per asset (`per`) and one pooled slope (`pool`). IC = correlation
   of all out-of-sample predictions with `z_h`. The year's gap is also the purge: the last
   training target ends at most 13 weeks into year `y0 - 1`, nine months before the test block.
5. **Walk-forward gain over the trend inputs**: walk-forward IC of the seven trend inputs plus
   the input (per-asset slopes) minus that of the trend inputs alone, same rows. Not defined for
   the trend inputs themselves.
6. **Chance (circular-shift null)**: the input's weekly series is rotated in time by a random
   offset inside its own span (first to last Friday it has data; offset at least 52 weeks from
   either end), the same rotation for all six assets, and measures 2 and 4 are recomputed. 1,000
   rotations, seed 0. One random number per rotation sets the offset of every input (as a
   share of its span), so inputs with the same span are rotated together and the dependence
   between the tests is kept. Different from info-1 in one point: info-1 rotated over the whole
   table, which leaves short inputs with few usable rotations; rotating inside the span keeps
   the coverage. An input with a span under 157 weeks has no chance level and cannot survive.
7. **Effective sample size**: 1 / (variance of the null in-sample IC). This is the number of
   independent observations a plain correlation with the same chance spread would have. Shown
   next to the cells and next to weeks / `h`.
8. **Smallest detectable IC**: null mean + (critical value + 0.84) x null sd of the walk-forward
   IC: the true walk-forward IC this screen would flag four times out of five.

### Multiple testing

The family is 49 inputs x 2 horizons x 2 slope models = **196 walk-forward ICs**. Correction:
single-step maxT (Westfall-Young) on the same 1,000 rotations. Each null walk-forward IC is
studentised with its own null mean and sd; the critical value `c` is the 95th percentile, over
rotations, of the largest studentised value in the family. One-sided: a negative walk-forward IC
(the sign flipped between training and test) is useless whatever its size. So across all 196
tests together the chance of one false "survives" is 5%.

### The bar (fixed now)

- **An input survives** if, at a horizon, its walk-forward IC (`per` or `pool`) is **>= 0.10**
  and its studentised value is **>= `c`**. A trend input over the bar is reported as "trend
  (already in `tsmom12`)" and does not count.
- **Near**: walk-forward IC >= 0.05 and above its own single-test 95% level. Named in the
  write-up, no trading card.
- **A combined forecast survives** if it beats `tsmom12`'s own state: see below.

What 0.10 means at a slow horizon, so nobody over-reads a pass: a forecast is worth roughly
IC x sqrt(independent bets a year). A 4-week IC of 0.10 gives 13 bets a year against 52, so it
is worth about what a weekly IC of 0.05 is (0.10 / sqrt(4)); a 13-week IC of 0.10 about a weekly
0.03. rl-3's ceiling put a weekly 0.10 at +0.16 Sharpe and a weekly 0.05 at +0.03. The table
shows this "weekly-equivalent IC" (IC / sqrt(h)). The 0.10 bar is therefore the door to a
trading card, not a claim of value: the trading card decides.

### Combined forecasts (3, fixed now)

`tsmom12`'s own state = the walk-forward forecast from `up_12m` alone, a slope per asset (model
`B`). Each combined forecast adds inputs to `B`; its score is the **gain** = walk-forward IC of
the combined model minus that of `B`, on all cells from 2000, same blocks. Missing inputs are 0
after standardising on the training rows (neutral).

- `slow4`: `B` + a slope per asset on the four inputs the literature places at monthly-to-
  quarterly horizons: `cot_spec_z3y` (positioning extreme), `vrp` (variance risk premium),
  `puell` (coins), `curve` (term spread).
- `all-sign`: `B` + one column: the mean over the 42 non-trend inputs of sign x standardised
  input, the sign being that of the input's pooled IC on the training rows. Nothing but signs is
  fitted, plus one slope.
- `all-ridge`: `B` + ridge regression on the 42 non-trend inputs (pooled slopes), penalty =
  number of training rows (it halves the slope of an input that is uncorrelated with the rest);
  `B`'s slopes are not penalised. The penalty is fixed here, not tuned.

Null: all 42 non-trend inputs rotated together over the whole 2000-2025 window (offset >= 52
weeks), `B` untouched, 500 rotations, seed 0; maxT over the 3 x 2 = 6 gains. **Survives** if
gain >= +0.05 (info-1's gain bar) and studentised gain >= the 6-test critical value.

### Controls (not strategies, not in the family)

- **Reproduction**: the script is first run at `h` = 1. Its IC, rank IC and walk-forward columns
  must match `results/info-1.md` and `results/rl-3-inputs.md` to three decimals. These numbers
  are already public; nothing is logged for them.
- **Planted input** (kind `control`, idea `slow-1-control`): a synthetic input whose in-sample
  IC with `z_h` is exactly 0.10, with two kinds of noise: `fast` (noise with the target's own
  `h`-week overlap) and `slow` (noise with a 26-week half-life, like a valuation or positioning
  series). Run through the same measures and judged against the same `c`. It answers: could this
  screen have seen a true 0.10 at this horizon at all? `fast` is the best case.

### If something survives

A trading card is added to this file and committed before any of its numbers. Outline, fixed
now: the survivor's walk-forward forecast tilts `tsmom12` through rl-2's residual action (at most
half a slot per asset, coins never above their `tsmom12` weight, long only), score = forecast /
its training sd; the tilt is re-decided every `h` weeks (the slow rebalance) while `tsmom12`
itself stays weekly; at most two variants; twin `tsmom12`; the protocol's default pass bar plus
"not behind `tsmom12` since 2003". Train only. The held-out year (2025-11-11 .. 2026-11-09) is
looked at once, and only for a rule that passed train.

If nothing survives: no trading card, no backtest. The write-up names the closest inputs and
shows the effective sample sizes.

### Logging

Every input x horizon gets a row in `tries.md` (kind `screen`, idea `slow-1-screen`: a
descriptive row, not a backtest, not selectable), 98 rows; the six combined-forecast scores
likewise (`screen`); the four planted inputs as `control`. Table: `results/slow-1.md`. Script
`lib/slow1_ic.py`; derived arrays under `<cache_root>/derived/slow-1/`. No downloads.

## Disclosures

- 2026-11-18, before the logged run. Reproduction at `h` = 1 (`slow1_ic.py --check`): the
  script's weekly IC, rank IC, IC held, walk-forward (per, pooled, trend) and gain match
  `results/info-1.md` for all 23 inputs (largest difference 0.0005, the rounding), and its weekly
  IC matches `results/rl-3-inputs.md` for 25 of the 26 rl-3 inputs. The 26th, `halving`, differs
  by design: rl-3 pooled it over all six assets with zeros off coins, this card measures it on
  coins only.
- Details the card left open, fixed in the code before the run: a combined-forecast input with
  fewer than 104 finite training cells in a block is 0 in that block; the ridge penalty is the
  number of training rows for every input, read literally, so an input with partial coverage is
  shrunk by more than half; `halving` off coins is missing, and rl-3's price inputs are missing
  where the asset is not eligible (so a rotation cannot move a placeholder zero into a live
  cell). The family counts only walk-forward ICs that exist (an input too short for a
  walk-forward block, like `dvol_rv` at 1 week, drops out), so it may be smaller than 196.
- A timing print at `h` = 1 (20 rotations of three inputs, three combined-forecast rotations;
  seconds only, no statistic) was run to size the job. No `h` = 4 or 13 number had been computed
  when the run was launched.

## Status (2026-11-18, paused by the lead at the usage limit)

**Done:** card; code and tests; weekly reproduction; the logged run (once, `--run --log`: 98
input rows + 6 combined rows of kind `screen`, 4 `control` rows in `tries.md`); table
`results/slow-1.md` with a post-hoc section. Held-out year not loaded.

**Result in one line (write-up still to come):** nothing survives. Family of 192, critical
z 3.40. Closest: `usd_13w` at 13 weeks, walk-forward IC +0.151, z 2.82, family-adjusted p 0.23;
it comes from BTC and ETH in 2017-2025 and is zero on the four ETFs. No combined forecast beats
`up_12m` (best gain +0.028, z 1.25). No trading card, no backtest.

**Next:** the plain-words write-up at the top of this file, the `next-steps.md` section, the
PR text. No process running.
