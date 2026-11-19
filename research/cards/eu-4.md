# eu-4: whipsaw reducers for the small coin-free EUR book

Field: execution of the house rule for a small euro book with fixed per-order fees (not a new
signal). Lane `eu-4` (DEEPER), night of 2026-11-18, branch `eu-4` from `eu-3`. Written and
pushed before any number for the rules below existed.

## Seen before writing this

- Everything in eu-1, eu-2, eu-3 (cards, write-ups, result tables), in particular eu-3's six
  order cutters V0-V5 on `euw` and their fee table.
- eu-4 step 1 (`results/eu-4-diag.md`, descriptive, the house rule only): `euw` places 30
  orders a year in thirds (entries, exits, drift); 83% of the ~20 flip orders a year sit in
  spells reversed within 4 weeks; 88 of 267 spells last one Friday; whipsaw spells are shallow
  (1-week spells: median peak |z| 0.05, 94% under 0.25); the weekly change of z has sd 0.21
  on every asset. z = 365-day log return / the asset's annualised EWMA vol (60-bar half-life).
- trend-tune (`results/trend-tune-anatomy.md`, "Entry and exit thresholds"): on the US six
  1994-2025, the 12-month rule with a no-trade band of half-width 0.25 in z around 0 had
  Sharpe 1.05 (same as the plain rule), worst loss 35% vs 36%, 1.7 vs 2.7 trades a year per
  asset. That grid also showed h = 0.5 at 1.01. No reducer has been run on `euw` or any EUR
  book.

## Failure mode

Fixed per-order fees make `tsmom12` on `euw` not worth running at EUR 5k at any tier and at
EUR 10k at the EUR 2-3 tiers (eu-3). Half of the fee drag is flips that the next flip reverses
within a month, around a 12-month return near zero. Question: does a pre-committed whipsaw
reducer that keeps the signal's character cut enough of those flips to move the minimum book?

## The two reducers (all that will be run; fixed now)

Both change only when a slot may switch state. Everything else is the house rule `R` exactly
as eu-3 ran it: Friday decisions on bars closed by 22:30 UTC, next-open fills, weights 1/7 per
held slot repeated every day (so drift is topped up on any day), 1% band, cash at 0,
total-return prices, EUR, ETF slippage 0.05% a side, window W (decisions 2012-01-02 ..
2025-11-09). Run as the eu-3 state machine over Fridays (`eu3.friday_weights` logic), from the
Friday 2011-12-30, where both start in the house rule's state (held = signal positive).

- **C1 `confirm2`** (confirmation). A slot switches only when the signal has had the new sign
  on this Friday *and* the Friday before. Otherwise it keeps its state. Removes every 1-Friday
  spell; every other flip comes one week later than in `R`.
- **C2 `dz25`** (dead zone). With z as above: a held slot is sold when z < -0.25; a cash slot
  is bought when z > +0.25; in between it keeps its state. 0.25 is about one week of z noise
  (0.21 measured in step 1, rounded up to the cell trend-tune already ran; no other value is
  run). Same sign convention as the signal (z > 0 iff the 12-month return > 0).

## Character test ("keeps the character"), against `R` at no fixed fee, on `euw`

All four must hold:

1. **Positions.** Correlation of the held state (1 held / 0 cash), pooled over all slot-Fridays
   of W, with `R`'s: >= 0.80. (Shown with it: the share of slot-Fridays that agree, and the
   correlation of the book's weekly exposure.) 0.80 is roughly "every flip a week late plus a
   few blips removed" at `R`'s ~20 flips and 67% exposure.
2. **Sharpe** within 0.05 of `R`'s (either direction; eu-3's bar).
3. **Max drawdown** within 2 points of `R`'s (either direction; eu-3's bar).
4. **Crash behaviour.** In the four crash windows inside W (2015-16, 2018-Q4, 2020 covid, 2022;
   eu-1's dates): the sign of (reducer minus equal weight) matches `R`'s in at least 3 of 4,
   **and** the reducer's return in each window is within 3 points of `R`'s.

**Robustness, other books** (logged as `robustness`; not selectable): the same reducers at no
fixed fee on `eu6` (the six with coins, in EUR, eu-2's costs) and on `usw` (US asset-class
ETFs in USD, the gym's costs), each against `R` on that book. A reducer counts as keeping the
character only if it also passes tests 1 and 2 on at least one of these two books; failing both
there marks it "fragile" and the verdict cannot use it.

## Family bar (multiple testing)

The family is "order cutters for `euw`": eu-3's V0-V5 plus C1 and C2, **8 selectable
variants**. `R` and equal weight are not selectable.

- A no-fee Sharpe difference to `R` is never read as a gain. It counts as real only with a
  paired bootstrap p < 0.10 / 8 = 0.0125, and even then it fails test 2 if it is over 0.05
  (a different rule, as eu-3 ruled for monthly decisions).
- If both reducers keep the character, the one with fewer orders a year at no fee is the pick
  (a mechanical count, not a Sharpe choice); the other is reported.
- Held-out year: untouched. A pass here is an implementation choice for small books, not an
  edge; using it in a live book would need its own card and the held-out look.

## Fees, books and "worth running"

Generic tiers: EUR 1, EUR 2, EUR 3 per ETF order (eu-2's three schedules unchanged, so the EUR
1 and EUR 3 tiers carry the same small yearly fee as in eu-2/eu-3), constant books of EUR 5k,
10k, 25k, fee / book debited per ETF fill (`eu2.fixed_fees`).

- **Worth running** (eu-3's strict reading): same character, **fee loss <= 0.10 Sharpe**
  with fee loss = max(own Sharpe at no fee, `R`'s) minus Sharpe under the tier, and Sharpe
  minus house equal weight's (same tier and book) within 0.15 of `R`'s gap at no fee.
- **Minimum book** per reducer and tier: the smallest book with fee loss <= 0.10, linear in
  1/size between tested sizes (eu-2's method); "<= 5k" / "> 25k" outside. Also shown: the
  mechanical prediction (fees per year / vol).
- **Success:** a reducer that keeps the character makes `euw` worth running at EUR 5k or 10k on
  a tier where neither `R` nor V0 is (eu-3: 5k at every tier, 10k at EUR 3; 10k at EUR 2 was on
  the line, V0 0.098 / R 0.104).

## Rows (fixed now)

- `euw`: C1 and C2, each at no fee and at 3 tiers x 3 books: **20 `variant` rows** (idea
  `eu-4`). `R` and equal weight on `euw` are eu-3's saved runs, re-scored without new rows.
- `eu6` and `usw` at no fee: C1, C2 (`robustness`) on each, **4 rows**; `R` and equal weight
  there are eu-2's / eu-1's saved runs, re-scored without new rows (if a saved run is missing,
  it is run and logged as `robustness` / `baseline`, and the count is given in the result).
- Plumbing check before any row: the state machine with no confirmation and h = 0 must give
  `R`'s weights exactly; no number is shown.

## Result

`eu-4.md` (sections 2-3) and `results/eu-4.md` once run.
