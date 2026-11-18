# eu-2: amendments to the eu-1 card (small-account costs, currency hedge)

Field: robustness of the house rule for a Dutch retail investor (not a new rule, not a
selection). Lane `eu-2` (DEEPER), night of 2026-11-18, branch `eu-2` from `eu-1`. Everything in
`cards/eu-1.md` stays as written; these amendments add runs. Each amendment was committed and
pushed before any of its numbers existed. Seen before: everything in `eu-1.md` and
`results/eu-1.md` (all eu-1 strategy numbers).

## Amendment 1: fixed per-order fees at small book sizes (written ~22:10 UTC, before any run)

### Failure mode

eu-1 charged a Dutch broker as a percentage (0.10% fee + 0.05% slippage a side). Real Dutch
brokers charge a fixed amount per order. On a small book a fixed fee is a large share of each
order, and the house rule also places small drift trades (weekly decisions, 1% rebalance band):
a 1%-of-equity top-up on a EUR 5,000 book is a EUR 50 order, and a EUR 3 fee is 6% of it.

### Fee schedules (public pages, read 2026-11-18)

- DEGIRO NL, `degiro.nl/tarieven` ("Peildatum: 01.10.2025"): ETF core selection ("Kernselectie")
  EUR 0 commission + EUR 1 handling fee per order; other ETFs ("ETF Wereldwijd") EUR 2 + EUR 1
  = EUR 3 per order. Exchange connectivity fee: 0.25% of the portfolio, at most EUR 2.50 per
  calendar year per exchange outside Euronext Amsterdam/Brussels (here: Xetra).
- Trade Republic (operates in NL; its own fee page did not load, source: curvo.eu article of
  2026-09-18): EUR 1 per order when Trade Republic is the counterparty ("Best Price"), EUR 2 per
  order routed to an exchange of your choice ("Direct Price", since July 2026); savings plans
  free. No connectivity fee.

Which of our lines are in DEGIRO's core selection is not checked line by line, so EUR 1 and
EUR 3 bracket DEGIRO. Schedules (ETF orders; coins always pay 0.25% + 0.05%, a Dutch exchange's
percentage taker fee, as in eu-1):

| Schedule | Fixed fee per ETF order | Yearly fee | Slippage a side |
|---|---:|---:|---:|
| `slip` (reference, no fee) | 0 | 0 | 0.05% |
| `dg1` (DEGIRO core selection) | EUR 1 | EUR 2.50 (Xetra) | 0.05% |
| `tr2` (Trade Republic Direct Price) | EUR 2 | 0 | 0.05% |
| `dg3` (DEGIRO other ETFs) | EUR 3 | EUR 2.50 (Xetra) | 0.05% |

### Book size

EUR 5,000, 25,000 and 100,000, held constant: each fixed fee is charged as fee / book size of
the equity at that moment (as if the owner skims gains or tops up losses to keep the book at its
size). Otherwise a book compounding at 30% a year would be ten times its start size by 2021 and
the fee would vanish; a constant book answers "at this size, what does the fee cost".

### Mechanics

The gym is not changed. `lib/eu2.py` wraps the gym's order step in-process: after each batch of
fills it debits fee / book of the equity for every ETF fill, and once per calendar year (first
order day) the yearly fee / book. Cash may dip a few hundredths of a percent below zero until the
next order; this is accepted. With fee 0 the wrapper must reproduce the plain gym exactly (checked
in the script). Orders per year (ETF fills / years) are counted.

### Mitigation, fixed now: a 5% rebalance band

The gym skips a trade smaller than `band` x equity, except a full exit (house band 1%). The
mitigation is **band 5%**: drift top-ups below 5% of equity are skipped; entries and exits of a
whole slot (14-17% of equity) still go through. Robustness: band 2.5% for `tsmom12` at `dg3`.

### Runs (all, window W = decisions 2012-01-02 .. 2025-11-09, idea `eu-2`)

Books `eu6` (SXR8, SXRV, 4GLD, IBGL, BTC-EUR, ETH-EUR) and `euw` (SXR8, EXSA, IQQE, IBGS, IBGL,
4GLD, EXXY), as in eu-1. `tsmom12` rows are `robustness`, `equal-weight` rows `baseline`.

1. `slip`, bands 1% and 5%: `tsmom12` and `equal-weight` on both books (8 rows).
2. `dg1`, `tr2`, `dg3` x EUR 5k, 25k, 100k x bands 1% and 5%: `tsmom12` and `equal-weight` on
   both books (72 rows).
3. Band 2.5%, `dg3`, three sizes, `tsmom12` on both books (6 rows).

86 rows. Nothing is selected; no held-out data.

### What counts (per book, schedule, size, band)

- **Fee loss** = `tsmom12`'s Sharpe at `slip` minus its Sharpe under the schedule, same band.
- **Worth running** if (a) fee loss <= 0.10 and (b) `tsmom12` minus `equal-weight` Sharpe (both
  under the same schedule, size and band) is within 0.15 of the same gap at `slip` (eu-1's test 1).
- **Break-even book size** per book, schedule and band: the smallest book at which fee loss <=
  0.10, interpolated linearly in 1/size between the two tested sizes that bracket it (fee loss
  scales about as 1/size); "< 5k" or "> 100k" if outside the tested range.
- **The band works** if, at `dg3`, the 5% band at least halves the fee loss at every size, and
  at `slip` the 5% band moves `tsmom12`'s Sharpe by no more than 0.05 and its max drawdown by no
  more than 2 points against the 1% band (it must not change the rule's character).

## Amendment 2: EUR-hedged US equity

Written after the hedged lines' data check and before any run with them: see below once added.
