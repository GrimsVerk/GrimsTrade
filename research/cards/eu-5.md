# eu-5: drift-only order cutters for the small coin-free EUR book

Field: execution of the house rule for a small euro book with fixed per-order fees (not a new
signal). Lane `eu-5` (DEEPER), night of 2026-11-18, branch `eu-5` from `eu-4`. Written and
pushed before any number for the two rules below existed.

## Seen before writing this

- Everything in eu-1 .. eu-4 (cards, write-ups, result tables).
- eu-4 step 1 (`results/eu-4-diag.md`): `euw` places 30.1 orders a year in thirds: 10.0
  entries, 9.8 exits, 10.0 drift top-ups or trims (held slots back to 1/7 once off by 1% of the
  book). eu-4's two signal-side reducers (C1 confirm-two-Fridays, C2 dead zone +-0.25 z) cut
  orders to 20 / 17 a year but deepened max drawdown by 3.3 / 2.4 points (later exits in
  covid 2020) and failed the character test.
- eu-3 V0 (trades on Fridays only, signal unchanged): drift 10.0 -> 7.9 orders a year, keeps
  the character; in the family.
- **eu-2's 5% band, exactly what it did** (`cards/eu-2.md`, "Mitigation"; the brief calls it
  eu-3's, it was eu-2's). It raised the gym's rebalance band from 1% to 5% of equity: any trade
  smaller than 5% of the book was skipped, except a full exit. On `euw` every entry is a whole
  1/7 slot (14.3% of the book), so in practice it cut only drift trades (held slots were
  topped up or trimmed only once 5 points, i.e. 35% of their target, away). Results seen: on
  `euw` at no fee orders 30 -> 21 a year, Sharpe -0.01, max DD +1.9 points, crash windows
  -8.9 / -4.2 / -12.5 / +2.1% vs R's -7.8 / -3.9 / -11.6 / +2.2%; the EUR 3 tier's fee loss
  fell ~40% (break-even 16k -> 10k). A 2.5% band (fee runs only) gave 22 orders a year. It
  **failed eu-2's card** for two reasons: (a) eu-2 required it to at least halve the fee loss
  at every size, and on `euw` it cut it by ~40%; (b) on `eu6` (coins) it changed the rule
  (Sharpe +0.06, max DD -3.1 points at no fee: it stopped trimming winning coins). So "changed
  the rule" was a verdict on the coin book, not on `euw`. It was never judged by eu-4's
  character test (positions, crash windows, robustness on two books) and is not in the
  selectable family.

## Failure mode

Fixed per-order fees make `tsmom12` on `euw` not worth running at EUR 5k at any tier and at
EUR 10k at the EUR 3 tier (EUR 2 on the line) (eu-3, eu-4). A third of the orders are drift
top-ups that do not come from the signal. Question: does a pre-committed rule that leaves the
signal (and so every entry and exit) untouched and only trades drift less often keep the
character and move the minimum book?

## The two drift cutters (all that will be run; fixed now)

Both leave the held set exactly as `R`'s on every Friday (same signal, same entries and exits,
same days). Everything else is the house rule `R` as eu-3/eu-4 ran it: Friday decisions on bars
closed by 22:30 UTC, next-open fills, 1/n per held slot (n = live slots), cash at 0,
total-return prices, EUR, ETF slippage 0.05% a side, window W (decisions 2012-01-02 ..
2025-11-09), the eu-3 state machine over Fridays from 2011-12-30.

- **D1 `flipreb`** (rebalance only at flips). `R` sends its weights every day, so drift is
  topped up on any day it passes the 1% band. D1 sends a decision only on an **event day**: the
  first decision day of W and every day whose applied Friday held set (or n) differs from the
  previous day's. On an event day it sends `R`'s full target with the house 1% band, so the
  flipping slot goes in or out and every other held slot more than 1% of the book off target
  is topped up or trimmed at the same open. On every other day it sends nothing: held slots
  drift freely. (An entry short of cash is filled as far as cash allows, as in the gym, and
  topped up at the next event.)
- **D2 `band25r`** (5/25 band). `R`'s daily decisions, but a top-up or trim is placed only
  when the slot is off target by more than X of its target. **X is fixed by a stated outside
  rule, not by our data:** the "5/25" rebalancing rule of thumb from the asset-allocation
  literature (rebalance an asset class when it is off by 5 percentage points absolute or 25%
  of its target, whichever is smaller). With targets 1/7 (`euw`, `usw`) that is 25% of target
  = **3.57% of the book**; with 1/6 (`eu6`) 4.17%. Implemented as the gym band min(0.05,
  0.25/n): entries (a whole slot) and full exits always pass. No other X is run.
- **How D2 differs from eu-2's failed band.** Same mechanism (a wider gym band), so its result
  on `euw` is expected near eu-2's 2.5% and 5% bands; this card does not pretend otherwise. What
  differs: X comes from a rule stated in advance and tied to the target (25%, i.e. 3.57%, not a
  round 5% = 35% of target); it is judged on eu-4's character test and robustness books, and
  counted in the family; and success is the minimum book, not "halves the fee loss". D1 is a
  different mechanism (when, not how far).

## Character test ("keeps the character"), against `R` at no fixed fee, on `euw`

eu-4's four tests. All four must hold:

1. **Positions.** eu-4's held-state correlation is 1.00 here by construction (shown). What these
   rules can move is the size of a held slot, so test 1 is: the correlation of the realised
   end-of-day slot weights (position value / equity), pooled over all slot-days of W, with
   `R`'s **>= 0.80**. Shown with it: the mean absolute weight gap per slot-day.
2. **Sharpe** within 0.05 of `R`'s (either direction).
3. **Max drawdown** within 2 points of `R`'s (either direction).
4. **Crash behaviour (incl. 2020).** In the four crash windows inside W (2015-16, 2018-Q4,
   2020 covid, 2022): the sign of (rule minus equal weight) matches `R`'s in at least 3 of 4,
   **and** the rule's return in each window is within 3 points of `R`'s.

**Robustness, other books** (logged as `robustness`; not selectable): D1 and D2 at no fixed fee
on `eu6` (the six with coins, EUR, eu-2's costs) and on `usw` (US asset-class ETFs, USD, the
gym's costs), each against `R` on that book. A rule keeps the character only if it also passes
tests 1 and 2 on at least one of these two books; failing both marks it "fragile".

## Family bar (multiple testing)

The family "order cutters for `euw`" is eu-3's V0-V5, eu-4's C1, C2, and D1, D2: **10
selectable variants**. `R` and equal weight are not selectable.

- A no-fee Sharpe difference to `R` counts as real only with a paired bootstrap p < 0.10 / 10
  = **0.01**, and even then it fails test 2 if it is over 0.05.
- If both keep the character, the one with fewer orders a year at no fee is the pick (a
  mechanical count); the other is reported.
- Held-out year: untouched. A pass is an implementation choice for small books, not an edge.

## Fees, books and "worth running" (eu-4's, unchanged)

Generic tiers EUR 1, 2, 3 per ETF order (eu-2's schedules; the EUR 1 and EUR 3 tiers also carry
a EUR 2.50 yearly fee), constant books of EUR 5k, 10k, 25k.

- **Worth running:** keeps the character, fee loss <= 0.10 Sharpe (loss = max(own Sharpe at no
  fee, `R`'s) minus Sharpe under the tier), and Sharpe minus equal weight's (same tier and
  book) within 0.15 of `R`'s gap at no fee.
- **Minimum book** per rule and tier: smallest book with loss <= 0.10, linear in 1/size between
  tested sizes; also the mechanical value (orders x fee + yearly fee) / (0.10 x vol).
- **Success:** a rule that keeps the character makes `euw` worth running at a (tier, 5k or 10k)
  cell where neither `R` nor V0 is (eu-4's grid: 5k at every tier, 10k at EUR 3). If so, eu-3's
  verdict changes for that cell; otherwise it stands.

## Rows (fixed now)

- `euw`: D1 and D2, each at no fee and at 3 tiers x 3 books: **20 `variant` rows** (idea
  `eu-5`). `R`, V0 and equal weight are eu-3's saved runs, re-scored without new rows.
- `eu6` and `usw` at no fee: D1, D2 (`robustness`), **4 rows**; `R` there is eu-2's / eu-1's
  saved run, re-scored.
- Plumbing check before any row (no number shown): D1 with every day an event reproduces `R`'s
  decisions exactly; D2's code path with band 1% reproduces `R`'s equity; the realised-weight
  replay (fills x closes + cash) matches the gym's equity on every day.

## Result

`eu-5.md` and `results/eu-5.md` once run.
