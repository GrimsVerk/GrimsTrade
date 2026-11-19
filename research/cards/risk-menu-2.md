# risk-menu-2: the menu's risk columns on 1994-2025 (descriptive, no pick)

Written 2026-11-19, lane `risk-menu-2` (branch from `risk-menu`), **before any number of this
card is computed**. Descriptive only: **no new pick, nothing selectable, nothing proposed for
the book.** Research harness only; fake money.

## Why

`risk-menu` (PR #101) put eleven risk dials on one footing, but only on P = 2007-04..2025-10,
because the wide long-short book needs 52 weeks of 34 ETFs. Its rankings by worst loss, worst 12
months and time under water therefore never saw 2000-2002, the bear market that review-1 found
drives `tsmom12`'s lead over holding. The question here: **do those three rankings hold with
2000-2002 included?**

What had been seen when this was written: the risk-menu tables on P (own-vol target 26% first on
all three: 6.3% / -3.2% / 1.3 y; hold the six last on worst loss and worst 12 months), the
2026-11-12 risk map's 1994-2025 worst-drop column (cash at 0, other rule forms), rp-1's
1994-2025 table. No number of any menu item on 1994-2025 with T-bill cash.

## Items (fixed now: 7 of the 11)

Every item that does not need the wide long-short book, with risk-menu's definitions unchanged:

1. **Hold the six** (equal weight in what is eligible), 2. **60/40** (SPY / TLT),
3. **`tsmom12`** full size, 4. **`tsmom12` 70%** + T-bills, 5. **`tsmom12` 26%** + T-bills,
6. **own-vol target, mean share 26%**, 7. **own-vol target, mean share 70%**.

Left out: the equal-risk blend and the three fixed splits (items 8-11: they need the wide book).

## Footing

- Window W = **1994-02-01..2025-10-31**: the gym's train start (SPY's first day plus a year of
  warm-up) to risk-menu's last day. Nothing after 2025-10-31 is read; the held-out year is
  untouched.
- Same as risk-menu: daily calendar returns, idle cash at the 13-week T-bill (`IRX`), gym costs
  for gym-run rules, 5 bps on the traded notional of each monthly share reset, drift between
  resets. Mixes start in bills on 1994-02-01 and reset on each 1st from then on.
- Own-vol target: share min(1, k / sigma52) from the 52 complete weeks of `tsmom12` before the
  previous month end, as risk-menu. Until `tsmom12` has 52 weeks of history (about its first
  13 months) the share is the fixed target (0.26 / 0.70), noted as an assumption. k is re-solved
  so the mean share **over W** hits the target (the in-sample k sets only the size).
- What the early years hold (by the existing rules, not changed): before QQQ (1999-03) the six
  means SPY alone; before TLT (2002-07) 60/40 is 60% SPY and 40% cash at bills; gold from 2004,
  Bitcoin from 2013, Ether from 2017.

## Measures

On W, on the total-return curve unless stated: Sharpe above T-bills (with `stats.sharpe_se`, as
context only), growth a year, volatility, **worst loss** (max drawdown), **worst 12 months**
(lowest 365-day return), **longest under water** (years below an earlier high, to recovery or to
the end), crash windows **2000-2002** (2000-01-01..2002-12-31, new), 2008, 2020 Q1, 2022, and
average gross exposure. No bootstrap, no orders column (risk-menu has them on P).

## The comparison (fixed now)

For each of the three risk measures, the order of the 7 items on W next to their order on P
(from `results/risk-menu.json`), with Kendall's tau between the two orders. Read as: a ranking
**holds** if the same item comes first on both windows and tau >= 0.7; otherwise it says what
moved. Ties (equal to the shown decimal) count as ties. One history each: no standard error.

## Expected before looking

Worst loss and worst 12 months: hold the six falls far deeper (2000-2002 hits SPY and QQQ with
no bonds yet), so `tsmom12` forms gain against holding; own-vol 26% stays first. Time under
water: the order may move most, since 2000-2002 gives holding a long wait (risk map: 11 years
for SPY + QQQ at cash 0).

## Output

`research/results/risk-menu-2.md` (+ `.json`), and a short section in `research/risk-menu.md`
answering the question. Script `research/lib/riskmenu2_run.py`.

## Logging

One `replication` row in `research/tries.md` per newly built series on the new window, as
risk-menu's convention: items 4-7 (4 rows, tag `@W94`, idea `risk-menu-2`, not selectable).
Items 1-3 are re-scores of logged baselines: no row. No `ledger/tries.jsonl` line.

## Bars (quoted, not used: nothing is picked)

- Family: no strategy test, no family bar; the `tsmom12` lineage count stays as rp-1 left it.
- Project-wide (`origin/register-1:research/register/BAR.md`, rows through 2026-11-18 22:34):
  **2,904 tries, N 1,012, Bonferroni p <= 4.9e-5**; latest (`register-3`, rows through 23:04):
  3,023 tries, N 1,027, effective N 433, edge over `tsmom12` +0.30 (close rule). No item is
  judged against it.
