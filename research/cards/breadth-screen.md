# breadth-screen: do the five multi-signal signals get their published signs back on 34 ETFs?

Written 2026-11-19 00:30 UTC, lane breadth-screen (base `multi-signal`), **before any signal, IC
or return in this card was computed** on the wide set. What was seen before writing:
multi-signal's card, script, results and write-up (the six-asset numbers), ls-trend-1's fetch
script and card (the ticker list and its four classes), and for the 35 cached CSVs only their
header, first and last date and row count. No price of the wide set was summarised. This is a
**descriptive screen, not a strategy test**: no backtest, no pick, no strategy try, held-out year
not loaded.

Bars to quote (lane rules). Project-wide (register-1, `research/register/BAR.md` on
`origin/register-1`, rows through 2026-11-18 22:34): **2,904 tries, N 1,012 for a new pick,
Bonferroni p <= 4.9e-5 (z 3.89); DSR 0.95 edge over `tsmom12` +0.32 Sharpe for a close rule,
+0.59 for a far one; against zero a new rule needs an annual Sharpe of 1.32 over 32 years.**
Trend family: 65 mechanisms, 16 tested, next test at p < 0.00154 (survey-5). Neither applies to
the rows of this screen (not picks); both apply to any rule or wide book a later lane builds
from it.

## Why

multi-signal (PR #104): on the six assets only cross-sectional momentum had a positive weekly IC
(+0.043; +0.035 beyond `tsmom12`, rank correlation 0.76 with it); value and carry sat inside
chance; low-vol and BAB had the wrong sign. Its diagnosis: breadth (4-5 assets a week, one or
two per class), where the papers rank 10-40 markets inside each class. Question here: with the
widest keyless universe already cached, ranked within asset class as the papers do, do the
published signs come back (value, carry, momentum positive; low-vol and low-beta positive), and
is anything large enough to matter for a future wide book? Prior, stated now: momentum positive
and small; value and carry modestly positive; BAB positive within class (FP's within-class
result is their strongest); none large on weekly ranks of ETFs.

## Universe (chosen now, before computing)

**ls-trend-1's wide set of 34 ETFs** (cached by `lstrend1_fetch.py` in
`<cache_root>/derived/ls-trend-1/`, Yahoo close and adjusted close), not the ~16
out-of-universe markets: it is wider and already split into the four classes of the papers.
QQQ (also in that folder, ls-trend-1's narrow set only) is left out, as in ls-trend-1's wide set.

- equity (9): SPY, EWA, EWG, EWP, EWQ, EWI, EWJ, EWN, EWU
- bonds (4): SHY, IEI, IEF, TLT
- commodities (15): GLD, SLV, PPLT, PALL, CPER, DBB, USO, BNO, UGA, UNG, CORN, WEAT, SOYB,
  CANE, DBA
- currencies (6): FXE, FXY, FXB, FXA, FXC, FXF

Train only: no bar after 2025-11-10 (`harness.TRAIN_LAST_BAR`) is read. Every ETF trades on US
days, so `sigma_i` uses 252 bars a year. First bars run from 1993 (SPY) to 2011 (CANE, CPER,
SOYB, WEAT): the class cross-section grows over time (this is stated, not fixed).

## Signals: multi-signal's five, unchanged

Exactly as in `cards/multi-signal.md` (formulas, windows, minimum bars, the `/ sigma_i` scaling,
the FRED `DGS3MO`/`DGS10` lag of one day): `value` (AMP: ln mean close 5.5..4.5 years ago minus
ln close, / sigma), `carry` (Koijen et al., / sigma), `xsmom` (AMP MOM2-12, / sigma), `lowvol`
(-sigma), `bab` (FP, -beta to SPY, 252-day vol, 5-year 3-day correlation). Reference `tsmom12`
(365-day log return > 0) and `z365`.

Carry applies the card's rule for each kind of asset to the new members:

- equity funds: the SPY/QQQ rule, trailing 365-day distribution yield (log adjusted minus log
  close return) minus `DGS3MO`.
- Treasury funds: the TLT rule, constant-maturity yield minus `DGS3MO`, at the cached maturity
  nearest the fund: SHY `DGS2`, IEI the 5-year point interpolated linearly between `DGS2` and
  `DGS10` (DGS5 is not cached), IEF and TLT `DGS10` (TLT as in the card; `DGS30` has a gap
  2002-2006). IEF and TLT share a numerator, so they differ only by `sigma`. Roll-down left out
  (as in the card).
- currency funds: the SPY/QQQ rule (trailing distribution yield minus `DGS3MO`): the trusts pay
  the foreign deposit rate, so this is foreign minus US short rate (Koijen et al.'s FX carry),
  floored at zero distributions when the foreign rate was at or below the fee.
- commodity funds: **no carry**. The card's GLD rule (minus the bill, lease rate 0) gives every
  commodity fund the same numerator, so it would rank only `sigma`; the futures basis (Koijen et
  al.'s commodity carry) is not in the cached data. Carry is ranked in three classes.

## Ranking within class (the papers' way)

- Each Friday, within each class with **at least 3** qualifying ETFs: Spearman rank IC (average
  ranks for ties) of score and target. **Weekly IC = mean over the classes that qualify** that
  week (equal weight per class; AMP and Koijen et al. combine classes with equal risk). A week
  counts when at least one class qualifies. IC = mean over weeks.
- **Beyond `tsmom12` (partial IC)**: within each class, score ranks regressed (OLS, intercept) on
  the `tsmom12` indicator; correlation of the residual with the target ranks; mean over classes,
  then weeks.
- Targets, horizons, eras, bootstrap: unchanged (log total return to the last close on or before
  t + 7 / t + 28 days; raw primary, return / sigma secondary; stationary block bootstrap of the
  weekly series, mean block 13 weeks, 5,000 draws, fixed seed, 95% and 99.5%; eras 2000-09,
  2010-16, 2017-21, 2022-25).
- **Placebo A**: 2,000 draws, each week the scores permuted among that week's ETFs **within each
  class**; 95th percentile of |mean IC| and two-sided p.
- **Placebo B**: fixed relabels **within class** (asset i gets asset pi(i)'s whole score series,
  pi permuting only inside each class). The full set is too large (9! x 4! x 15! x 6!), so
  **2,000 random within-class relabels**, fixed seed; p = share with |IC| >= |observed|.
- Link to `tsmom12`: mean within-class weekly Spearman of score with the indicator and `z365`.

Secondary (descriptive, not in the bar; 4 extra looks): (a) `value`, `carry`, `xsmom` without
the `/ sigma` scaling (the papers' raw within-class ranks; multi-signal scaled only because it
had no within-class ranking); (b) `bab` against each class's own market (FP's construction: the
equal-weight average daily log return of the class's ETFs alive that day); (c) every signal
pooled across all 34 with no class split (the six-asset way, for comparison); (d) the IC in
each class alone.

## Worth a card later? (bar fixed now)

10 primary looks (5 signals x 2 horizons): Bonferroni's 99.5% interval, as in multi-signal.

1. Partial IC beyond `tsmom12`, raw next-week target: 99.5% interval above 0, month same sign.
2. Outside both placebos: |IC| above placebo A's 95th percentile and placebo B p < 0.05.
3. Same sign in at least 3 of the 4 eras with data, and in at least half of the classes with
   data (this replaces multi-signal's four-ETF check, which has no meaning here).
4. Size, two readings, both reported:
   - multi-signal's own bar: partial weekly IC >= 0.10;
   - **wide-book reading**: annualised IC information ratio of the partial weekly IC (mean / sd
     x sqrt(52)) >= **0.59**, BAR.md's edge for a far rule at N 1,012. The IC-IR is roughly the
     Sharpe of a rank-weighted long-short book before costs, borrow and leverage, so it is an
     upper bound; a long-only, no-short paper book collects less.

"Brings the published sign back" (the question asked): the primary weekly IC has the paper's
sign (positive for all five, since every score is oriented so higher = expected better) with
the 95% interval excluding 0. Positive but inside the 95% interval = "sign back, not
distinguishable from 0".

Expected before computing: `xsmom` positive; `value`, `carry` weakly positive; `bab` and
`lowvol` sign unclear; nothing passes 4.

## Logging

Script `research/lib/breadth_screen.py`, pushed before its run. Run once with `--log`: one
`screen` row per primary signal plus `tsmom12` (6 rows, idea `breadth-screen`, variants tagged
`@wide34`), numbers in the variant text and in `results/breadth-screen.md`. Screen rows are not
selectable and not strategy tries.
