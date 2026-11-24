# risk-menu-3: own-vol targeting without look-ahead, and when each item was under water

Written 2026-11-19, lane `risk-menu-3` (branch from `risk-menu-2`), **before any number of this
card is computed**. Descriptive only: **no new pick, nothing selectable, nothing proposed for
the book.** Research harness only; fake money.

## Why

`risk-menu` (PR #101) and `risk-menu-2` (PR #105) put own-volatility targeting of `tsmom12`
first on worst loss, worst 12 months and time under water, with the best Sharpe (1994-2025:
1.03 at 26% mean share, 1.08 at 70%, against `tsmom12` 0.94). Its size k (share =
min(1, k / sigma52)) was solved so the mean share **over the whole scored window** hits the
target: a mild look-ahead, since nobody in 1995 knew the 1994-2025 mean of sigma52. Question 1:
**how much do Sharpe, worst loss and worst 12 months move when k uses only data available at
each date?** Question 2 (open from risk-menu-2's next steps): **when was each item's longest
spell under water on 1994-2025?**

What had been seen when this was written: the tables of `results/risk-menu.md` (P) and
`results/risk-menu-2.md` (W), including each item's longest under-water length (not its dates).
No number of the expanding-window rule.

## The rule without look-ahead (fixed now)

- Same as risk-menu-2: `tsmom12` sleeve (gym costs), monthly reset on each 1st at 5 bps of the
  traded notional, drift in between, the rest in 13-week T-bills (`IRX`); sigma_d =
  `tsmom12`'s volatility over the 52 complete weeks before the previous day (`Sleeve.sigma`).
- **Expanding k**: on each 1st d, k_d solves mean over months m <= d (all months since the first
  finite sigma, d included) of min(1, k / sigma_m) = T, with T = 0.26 or 0.70. Every sigma_m is
  known at d. The share at d is min(1, k_d / sigma_d). sigma_d = 0: keep the drifted share.
- **Warm-up**: until 24 monthly sigmas exist (sigma needs about 13 months of `tsmom12`, so
  roughly the first three years from 1994-02), the share is the fixed target T, as risk-menu-2
  did before sigma existed. Assumption, stated: 24 months is a round minimum for a mean.
- T itself (26%: vol-timing's b1 mean share; 70%: risk-menu's middle size) is a menu choice made
  outside the data's risk path and is not re-fitted; the realised mean share will miss T and is
  reported.

## Windows and comparison

- W = 1994-02-01..2025-10-31 (risk-menu-2's window) and P = 2007-04..2025-10 (risk-menu's
  window). One series built from 1994-02; P is that series cut to P (k on P uses 1994+ data,
  which was available then). Nothing after 2025-10-31 is read; held-out year untouched.
- Against the re-fitted version: on W, `results/risk-menu-2.json` (vt-own 26% / 70%); on P,
  `results/risk-menu.json`. Report the change in Sharpe, worst loss, worst 12 months, plus
  growth, longest under water, realised mean share, and the range of k_d.
- **Correction rule**: if any of Sharpe (by >= 0.02), worst loss or worst 12 months (by >= 0.5
  points) moves, the menu's numbers are corrected in `research/risk-menu.md`, and any ranking
  that changes is said; otherwise the section says they hold.

## Under-water dates (question 2)

On W, for the 7 risk-menu-2 items plus the 2 expanding-k rows: the longest spell below an
earlier high (same definition as `underwater_years`), with the date of the high it started
from, the date of its lowest point, and the first day back at the old high (or "not back by
2025-10-31"), and its length in years.

## Expected before looking

Expanding k: early k is set from 1995-1997 sigmas, so the share path differs most in the late
1990s; Sharpe moves by a few hundredths, worst loss and worst 12 months by under a point; the
order on the menu holds. Under water: holding the six 2000-2011, `tsmom12` a spell ending
around 2000-2006 or 2018-2023.

## Output and logging

`research/results/risk-menu-3.md` (+ `.json`), script `research/lib/riskmenu3_run.py`, a short
section in `research/risk-menu.md`. Two `replication` rows in `research/tries.md` (risk-menu's
convention: one per newly built series): `vt-own-26-x@W94`, `vt-own-70-x@W94`, idea
`risk-menu-3`, not selectable. The P cut is the same series: no row. No `ledger/tries.jsonl`.

## Bars (quoted, not used: nothing is picked)

- Family: no strategy test, no family bar; the `tsmom12` lineage count stays as rp-1 left it.
- Project-wide (`origin/register-1:research/register/BAR.md`, rows through 2026-11-18 22:34):
  **2,904 tries, N 1,012, Bonferroni p <= 4.9e-5**; latest (`register-3`/`register-4`, rows
  through 2026-11-19 00:21): 3,118 tries, N 1,032. No item is judged against it.
