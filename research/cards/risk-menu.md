# risk-menu: the risk dials side by side (descriptive, no pick)

Written 2026-11-19, lane `risk-menu` (branch from `vol-timing`), **before any number of this
card is computed**. Descriptive only: **no new pick, nothing selectable, nothing proposed for
the book.** Research harness only; fake money.

## Why

Tonight's lanes found no provable edge for `tsmom12` over holding (dsr-1, survey-5) and read its
value as crash insurance (insure-1, insure-2). Several ways to set the risk level now exist, each
studied on its own footing: a smaller fixed share of `tsmom12` with the rest in T-bills (rp-1:
about 70% matches `where-rp`'s worst loss), own-volatility targeting of `tsmom12` (vol-timing),
blends with the wide long-short trend book (ls-trend-2: the equal-risk blend, and a menu of fixed
splits as its next item 2), plain holding of the six, and 60/40. A human choosing a risk level
needs them on one footing: same window, same costs, cash earning T-bills, the same measures.

What had been seen when this was written: the vol-timing and ls-trend-2 tables (P window:
`tsmom12` Sharpe 1.21, worst loss 35.6% total; b1 1.26 / 5.6%; vt-own at mean share 0.26 1.34 /
6.3%; the equal-risk blend 0.97 / 8.8% with crash windows +8.9% / +2.2% / +2.0%), rp-1's
1994-2025 table, the 2026-11-12 risk map (2003-2025, cash at 0). No number of a fixed split, of
`tsmom12` at 0.70, of vt-own at 0.70, or of holding / 60/40 on the P window with bill interest.

## Footing (all items)

- Window P = 2007-04-01..2025-10-31 (the first month both `tsmom12` and the wide book have 52
  weeks of history, as ls-trend-2). Second window L = 2010-02-01..2025-10-31 for Sharpe only.
  Nothing after 2025-10-31 is read; the held-out year is untouched.
- Daily calendar returns; idle cash earns the 13-week T-bill (`IRX`, as `cash_interest.py`).
- Costs at the repo's standard per piece: the gym's costs for gym-run rules (2 bps ETFs, 25 + 5
  bps crypto, 1% band); the wide book 5 bps a side and 1% a year borrow on shorts
  (ls-trend-1/2); 5 bps on the traded notional of every monthly share reset.
- Monthly reset: on the 1st of each month the share goes back to its target; between resets it
  drifts with returns (as ls-trend-2's blend and vol-timing's vt-own).

## Menu (fixed now; 11 items)

Plain holding (gym runs, weekly Friday decisions, re-scored with bill interest):

1. **Hold the six**: equal weight in SPY, QQQ, TLT, GLD, BTC, ETH as each becomes eligible
   (logged baseline `equal-weight`).
2. **60/40**: 60% SPY, 40% TLT (logged baseline `sixty-forty`).

`tsmom12` sizes (rest in T-bills):

3. **`tsmom12`** at full size (logged baseline; ls-trend-2's sleeve).
4. **`tsmom12` 70%**: fixed share 0.70 (rp-1's `where-rp` match).
5. **`tsmom12` 26%**: fixed share 0.26 (vol-timing's same-size slot, here with monthly reset).

Own-volatility targeting of `tsmom12` (vol-timing's vt-own: share min(1, k / sigma52), sigma52
from the 52 complete weeks before the previous month end; k solved so the mean share in P hits
the target; the in-sample k sets only the size):

6. **vt-own 26%**: mean share 0.26 (vol-timing's), now with reset costs.
7. **vt-own 70%**: mean share 0.70 (the cap at 1 will bind often).

Blends with the wide long-short book at gross 1 (`wide-LS-g1`, ls-trend-2):

8. **Equal-risk blend** (ls-trend-2's `blend-er`, reproduced: must match Sharpe 0.97).
9. **Split 90/10**, 10. **Split 70/30**, 11. **Split 50/50**: fixed capital shares
   `tsmom12` / `wide-LS-g1`, reset monthly (ls-trend-2 next item 2's "90/10 to 50/50").

ls-trend-2's control b1 is not on the menu: vol-timing showed it is own-volatility timing with
extra noise (item 6 is its cleaner form). `where-rp` is not re-run: rp-1 itself says item 4 is
the plain way to its risk level.

## Measures (what a human chooses on)

All on P, on the total-return curve (what the account shows, bills included) unless stated.

- **Sharpe above T-bills** (daily excess, 365-day convention), with its standard error
  (`stats.sharpe_se`, Mertens), and the paired stationary bootstrap difference against hold-the-
  six and against `tsmom12` (mean block 20 days, 2,000 draws, seed 0; 5%..95% range), as
  description, not a test. Sharpe L beside it.
- **Growth a year** (CAGR) and volatility.
- **Worst loss**: maximum drawdown.
- **Worst 12 months**: lowest return over any 365-day window.
- **Time under water**: longest stretch below an earlier high (to recovery, or to the end).
- **Crash windows**: calendar 2008, 2020 Q1 (Jan-Mar), calendar 2022.
- **Average exposure**: mean gross invested share (sum of absolute weights; for blends both
  sleeves, so shorts count).
- **Orders a year**: gym fills for gym-run rules (exact). For mixes: `tsmom12`'s fills (a
  smaller share trades the same tickets), plus one order per held `tsmom12` asset at each
  monthly reset that moves the share by at least 1 point of the book, plus, for blends, the wide
  book's resized positions (one order per position held, monthly). Approximate; marked so.
  Turnover a year beside it.

## The output (fixed now)

`research/risk-menu.md`, one screen: a table "if you care most about X, pick Y" with one line
per measure above (Sharpe, growth, worst loss, worst 12 months, time under water, each crash
window, fewest orders). For Sharpe the line also names every item whose bootstrap 5%..95% range
against the best overlaps 0 ("not told apart"). Risk measures come from one history and carry no
standard error; the page says so. It ends with the reminder that no item is a proven edge
(project-wide bar below). A risk map SVG (`research/risk-menu.svg`): worst loss (x) against
growth a year (y), one labelled dot per item, no external fonts.

## Bars (quoted, not used: nothing is picked)

- Family: no strategy test, so no family bar applies; the combo / `tsmom12` lineage count stays
  as rp-1 left it (74, none passed, next at p < 0.10 / 75).
- Project-wide (`origin/register-1:research/register/BAR.md`, rows through 2026-11-18 22:34):
  **2,904 tries, N 1,012, Bonferroni p <= 4.9e-5**, edge over `tsmom12` +0.32 for a close rule;
  latest `register-3` (rows through 23:04): 3,023 tries, N 1,027, effective N 433, edge +0.30.
  No menu item is judged against it; a Sharpe gap smaller than that is no evidence of skill.

## Expected before looking

Fixed shares keep `tsmom12`'s Sharpe and scale its losses; vt-own keeps vol-timing's small
Sharpe gain; blends cost Sharpe in proportion to the wide share and buy crash gains; holding the
six grows fastest with the deepest loss (BTC, ETH); 60/40 has the lowest Sharpe. All Sharpe
gaps will sit inside about two standard errors (SE about 0.25 on 18.6 years).

## Logging

One `replication` row in `research/tries.md` (idea `risk-menu`, tag `@L07`, not selectable)
per newly built series: items 4, 5, 6, 7, 9, 10, 11 (7 rows). Items 1, 2, 3, 8 are re-scores of
logged configurations and get no row. No `ledger/tries.jsonl` line (no strategy tried).
