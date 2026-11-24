# vol-timing: is ls-trend-2's control just volatility timing of `tsmom12`? (descriptive)

Written 2026-11-19, lane `vol-timing` (branch from `ls-trend-2`), before any number of this
card is computed. Descriptive only: **no new pick, nothing selectable, nothing proposed for the
book in this step.** Research harness only; fake money.

## Why

ls-trend-2 (PR #89) reported a side result: its control b1, "`tsmom12` + T-bills" with the
`tsmom12` share set each month by equal risk (trailing 52 weekly volatilities) against the wide
long-short book at gross 1 (mean share 0.26), had Sharpe 1.26 and max drawdown 5.6% in
P = 2007-04-01..2025-10-31, against `tsmom12` 1.21 and 38.3%. combo-1 mapped `trend-vol` among
four models making the same "hold less when it hurts" bet, which failed. diversifier-1: anything
that holds less money is scored above T-bills against a same-size T-bill slot.

## Series (all fixed here)

All as in `lstrend2_run.py` Part A: daily calendar excess returns over the 13-week T-bill, T-bill
interest on idle cash, Sharpe a year in the repo's convention (daily, 365). Windows P (main) and
L = 2010-02-01..2025-10-31. Nothing after 2025-10-31.

1. `tsmom12`: as logged (six assets), re-scored with bill interest (ls-trend-2's sleeve).
2. b1: ls-trend-2's control, reproduced (must match 1.26 / 5.6%).
3. const: k x `tsmom12`, k = b1's mean share in P, rest in bills (the same-size T-bill slot).
4. vt-own: `tsmom12` scaled at each month start by c / sigma52(`tsmom12`), sigma52 from the 52
   complete weeks before the previous month end (ls-trend-2's `Sleeve.sigma`), share capped at 1,
   rest in bills; c set so the mean share in P equals b1's. This drops the wide book's volatility
   from the split and keeps only `tsmom12`'s own (plain volatility targeting). The in-sample c
   only sets the size; it does not change Sharpe.
5. `trend-vol` (`tv40`, `rules.trend_vol(0.40)`, six assets, weekly, gym costs), re-scored with
   bill interest the same way.

## Measures

- Sharpe P and L, volatility, max drawdown of the excess curve and of the total-return curve,
  mean share; Sharpe difference to `tsmom12` with ls-trend-2's paired stationary bootstrap
  (mean block 20 days, 20,000 draws, seed 0), shown as description, not a test.
- Decomposition of b1's Sharpe gain over `tsmom12`: constant part S(const) - S(`tsmom12`), which
  is 0 by construction (Sharpe does not change with a constant scale; stated now), and
  time-varying part S(b1) - S(const); the latter split into own-volatility timing
  S(vt-own) - S(const) and the rest S(b1) - S(vt-own) (the wide book's volatility in the split).
- Weekly (Monday-Sunday) correlation of b1 with `trend-vol`, and of their overlays: the weekly
  residual of each series regressed on `tsmom12` (what each adds beyond a constant scale).

## What decides step 2 (fixed now)

The time-varying part is **material** if S(b1) - S(const) >= +0.05 in both P and L. It is
**covered by `trend-vol`** if the weekly overlay correlation of b1 with `trend-vol` is >= 0.5,
or if `trend-vol` shows the same Sharpe gain over `tsmom12` (within 0.03) in P. Material and not
covered: a proposed card (not run) for the next window, with the project-wide bar from
`register-2` BAR.md (at 2026-11-18 23:04: 3,023 tries, N 1,027, effective N 433, z >= 4.65, edge
over `tsmom12` +0.30 close rule / +0.56 far rule, Bonferroni p <= 1.2e-04). Otherwise:
"covered by trend-vol, no card" (or "not material, no card").

## Logging

Each series 3-5 gets one `replication` row in `research/tries.md` (descriptive, not selectable);
b1 and `tsmom12` are already logged by ls-trend-2 and are not logged again.
