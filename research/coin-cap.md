# coin-cap: cap the combined coin weight inside tsmom12

Lane `coin-cap`, burst 1, 2026-11-18. Card (written and pushed before any number):
`cards/coin-cap.md`. Tables: `results/coin-cap.md`. Code: `lib/coin_cap.py`,
`lib/coin_cap_core.py`; test `tests/test_coin_cap.py`. Run once. Train years only, gym costs,
six live assets, 1994-02-01 .. 2025-11-09. The held-out year is unspent.

## Question

deep-1: 8 of `tsmom12`'s 10 worst drawdowns are coin tops. cointop-1: `stop-0.25` on the coin
slots cuts the worst loss from 36.5% to 28.9% for about 2 points less growth a year, "a smaller
coin position, not a better rule". Is a plain cap on the summed coin weight as good, cheaper?

## What was run

8 fixed cells (cap 10/15/20/25% x excess to cash / to the held non-coin slots pro rata), the
walk-forward stitch `cap-wf` (each year from 2016 the cell with the best growth over worst loss
on all earlier train days), all again at double costs; `tsmom12` and `stop-0.25` rerun unlogged
in the same script. 18 rows in `tries.md` (8 cells, `cap-wf`, 8 cells and `cap-wf` at 2x cost).

## Result

| | Sharpe | CAGR | Worst loss | Coin-crash windows summed | Crypto winter 2018 |
|---|---:|---:|---:|---:|---:|
| `tsmom12` | 1.05 | +17.8% | 36.5% | -156% | -22% |
| `stop-0.25` | 1.09 | +15.6% | 28.9% | -72% | -4% |
| `cap-wf` | 1.05 | +15.7% | 28.9% | -117% | -17% |
| `cap25-rest` | 1.07 | +16.9% | 28.9% | -129% | -17% |
| `cap20-rest` | 1.09 | +16.3% | 28.9% | -110% | -14% |
| `cap15-rest` | 1.06 | +14.6% | 28.9% | -84% | -10% |
| `cap10-rest` | 1.02 | +12.9% | 28.9% | -58% | -7% |

1. **Worst loss: a tie, and not a coin number.** Every cap from 10% to 25%, the stitch and
   the stop all have a worst loss of 28.9%. That is the 2000-02 dot-com fall (-28% in the
   stress table), years before there is a coin in the book. Any rule that takes roughly a
   quarter off the coin weight uncovers the same floor; no coin rule can go below it. So "worst
   loss 36.5% -> 28.9%" does not rank these rules at all.
2. **On worst loss alone the cap is cheaper.** `cap25` reaches the same 28.9% for 1.0 to 1.1
   points of CAGR a year against the stop's 2.2; `cap20` for 1.5 to 1.8. Four of eight cells
   (both 20% and both 25%) have the stop's worst loss and more growth, also at double costs.
3. **Inside the coin crashes the stop is better than any cap of the same cost.** Summed over
   deep-1's eight coin-crash windows the stop loses 72%; `cap20` (more growth than the stop)
   loses 110%, `cap15` (less growth than the stop) still loses 82 to 84%. A cap needs to go to
   10% (5 to 5.6 points of growth a year) to lose less than the stop there. So the stop is not
   only a smaller coin position: per point of growth given up it takes off about twice as much
   coin-crash loss as a cap does.
4. **Sharpe: nothing to tell apart.** All cells are within 0.05 of `tsmom12` (p 0.14 to 0.71);
   `cap-wf` against `stop-0.25` is -0.04 (p 0.69).
5. **Walk-forward picks the loosest caps**: `cap20-cash` for 2016-17, then `cap25` every year.
   Growth over worst loss on a sample where Bitcoin went up a thousandfold favours more coin.

## The bar, as the card set it (`cap-wf`)

- Bar 1 (worst loss no larger than the stop's): **tie**. 28.9% against 28.9%; the script prints
  FAIL because the stitched equity is rebuilt from returns and differs in the last float digit.
  All 8 fixed cells, which need no stitch, hold it. Read as held, with point 1 as the caveat.
- Bar 2 (CAGR above the stop's): holds by a hair, +15.69% against +15.61%. Not a finding.
- Bar 3 (Sharpe at least `tsmom12`'s and the stop's): **fails** (1.048 against 1.048 and 1.091).
- Bar 4 (bars 1 and 2 at double costs): same tie as bar 1; CAGR +15.57% against +15.27%.

Not all four hold, so the card's "a plain cap does the stop's job cheaper" is not claimed.

## Reading

A cap of 20 to 25% on the coins buys the same headline worst loss as the stop for about half
the growth cost, but only because the headline number stops measuring coins once it hits the
dot-com floor. Measured where the coins hurt, the stop does more per point of growth. Both are
risk choices with Sharpe differences inside noise; neither is a better rule than `tsmom12`.

Limits: one run on one history with two coins; the crash windows were drawn in hindsight by
deep-1; `stop-0.25` was chosen on the coin book, the cap grid here; the stitch leaves out one
switch trade a year; nine series were looked at.

## Changes after the card

None to the rule, grid, selection or bar. One reading note: bar 1 is reported as a tie (above).

## Next steps

- The right yardstick is missing: worst loss from 2013 on (coin years only) and time under
  water would rank cap against stop where the dot-com floor cannot hide the difference. One
  card, no new runs needed beyond rereading the saved equity curves in `research/data/runs/`.
- A cap and the stop together (cap 25% + `stop-0.25`) is the obvious combination; card first.
- Nothing here argues for spending the held-out year.
