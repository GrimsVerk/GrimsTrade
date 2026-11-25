# hedge-books-1: Hedge (multiplicative weights) across the existing books

Research lane `hedge-books-1` (DEEPER), night 2026-11-24/25. Branch `hedge-books-1` from `main`
fac43c9, PR #175. Card [`cards/hedge-books-1.md`](cards/hedge-books-1.md) (ffa9f48, before any
number), script `lib/hedgebooks1.py` and tests (7d1ca3c, before the run), one run (117e812).
Tables: [`results/hedge-books-1.md`](results/hedge-books-1.md). Train only (no bar after
2025-10-31); held-out year untouched. Fake money, no change to the gym, runner or live books.

## In plain words

**No. An online allocator with a regret guarantee, run across 16 existing books, does not beat
`tsmom12` at the bar and does worse than simply splitting the money equally across the same
books.** Hedge (Freund and Schapire 1997, in Cesa-Bianchi and Lugosi's 2006 form with the
textbook rate) got Sharpe 1.13 against `tsmom12`'s 1.05 (z +1.23, the bar is 4.70) and against
1.16 for the equal split (z -1.87). The learning moved the weights only a little, and in the
wrong direction for Sharpe: towards Bitcoin buy-and-hold and cross-sectional momentum, the books
with the largest average weekly gain and the largest swings. A Hedge switch between `tsmom12`
and `own_vol_70` alone stayed at 50/50 to 52/48 for 32 years: it is the equal split of the two
(1.050 against 1.050). Both are killed by the card.

| 1994-02-01..2025-10-31, protocol costs | Sharpe | vs `tsmom12` d (SE) z | vs equal split z | corr `tsmom12` (weekly) | Growth/yr | Worst loss | Since 2003 | 2022-25 | Card |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `hedge16` (judged) | 1.128 | +0.076 (0.062) +1.23 | -1.87 | 0.94 | +18.3% | 33.5% | 1.30 | 0.85 | **kill** |
| `ew16` (equal split, baseline) | 1.158 | +0.106 (0.060) +1.78 | - | 0.95 | +17.1% | 33.0% | 1.36 | 0.90 | - |
| `hedge-pair` (`tsmom12` + `own_vol_70`) | 1.050 | -0.002 (0.003) -0.49 | +0.54 | 1.00 | +15.4% | 32.9% | 1.20 | 0.92 | **kill** |
| `tsmom12` | 1.052 | - | - | 1.00 | +17.9% | 37.0% | 1.20 | 0.92 | - |

At the gym's live costs (robustness) every number moves by at most 0.006 Sharpe; the verdicts
stay.

## Regret actually achieved

| | `hedge16` | `hedge-pair` |
|---|---:|---:|
| Rounds T, books K, rate eta = sqrt(8 ln K / T) | 1,656, 16, 0.116 | 1,656, 2, 0.058 |
| Loss regret against the best book (theorem's units) | 5.04 | 0.71 |
| Bound sqrt(T ln K / 2) | 47.9 | 24.0 |
| Spread of the books' total losses (best to worst) | 9.1 | 1.4 |
| Best book by loss, and by growth | `buy_hold_btc` | `tsmom12` |
| Log-wealth regret on the books' outcomes (total, per year) | 4.77, 0.150 | 0.70, 0.022 |
| Log-wealth regret of the traded book vs the best book by growth | 4.74 (`buy_hold_btc`) | 0.70 (`tsmom12`) |
| ... vs the best book by Sharpe | 1.21 (`halving-alone`) | -0.75 (`own_vol_70`: Hedge grew more) |

What this says:

1. **The guarantee is vacuous at this length.** The bound (47.9) is five times the whole spread
   between the best and the worst book over 32 years (9.1). Hedge kept its promise easily (5.0,
   a tenth of the bound), but a promise that loose allows anything from the best book to well
   below the average.
2. **The textbook rate barely learns.** eta times the books' loss spread is about 1.1, so the
   largest weight ever was 0.113 against 0.0625 at the start, and the effective number of books
   stayed at 15.8 of 16 on average (14.9 at the end). Hedge ended about halfway between the
   average and the best book in its own loss units.
3. **It learns the wrong target for this question.** Hedge's loss is linear in the week's return,
   so it rewards the highest average weekly gain, which here is the highest-swing books
   (`buy_hold_btc` final weight 0.111, `xs_momentum` 0.091; `crypto_mean_reversion` 0.039).
   Shifting weight to them adds growth (+18.3% a year against +17.1%) and costs Sharpe (1.128
   against 1.158). In log wealth it trails Bitcoin buy-and-hold by 0.15 a year, as expected
   from a near-uniform mix.
4. **The pair is a scale dial.** `own_vol_70` is `tsmom12` sized down by its own volatility;
   the two had nearly the same weekly gains, so Hedge's weight on `tsmom12` only moved from 0.500
   to 0.521. The result is about 85% of `tsmom12`'s size at the same Sharpe.

## Why the equal split looks better (post hoc, not a pick)

`ew16` is 1.158, +0.106 over `tsmom12` (z +1.78), worst loss 33.0% against 37.0%. This is a
baseline, not a candidate, and it was not chosen before the run as anything but a comparator. It
repeats deep-1's "plain average of all models" (1.06 against 1.05, its pool) and combo-1's
`blend-ws` reading: averaging many versions of "hold less when things look bad" plus some
always-invested books smooths the ride a little. Three of its 16 books were picked because they
did well in this very window (`halving-alone`, `where-vol`, `stop-0.25`), so its lead is
flattered, and z +1.78 is far below the 4.70 bar. Not worth a card on this evidence.

## Already tested before this lane

Cover's universal portfolio across the six assets (`universal-portfolio`, run 1: dead, stays at
its start mix); deep-1's three walk-forward mixes across 29 models (all fail); combo-1/2's
equal-risk pairs (fail). None was a regret-guaranteed allocator across books, so this lane is
the first; it adds the same answer from a different angle: across these books there is little
to learn (the books lose in the same weeks), and what an online learner can learn in 32 years
with a guaranteed rate is less still.

## Notes and assumptions

- Costs: the protocol's (25 bps fee + 5 bps slip on coins, 2 bps on ETFs) for every book,
  comparator and the combined account; the gym's live costs (Kraken taker tiers) as robustness.
  Cash at 0, dividend-adjusted prices. `tsmom12` here is the research yardstick (1.052 on this
  window, 1.048 at the gym's live costs); the live vol-scaled `ts_momentum` is 1.097 and is one of
  the 16 books.
- Check before use (card): the four research books rebuilt on their stored window match the
  store's Sharpe within 0.005 (`tsmom12` 1.0480 vs 1.0481, `halving-alone` 1.2848 vs 1.2826,
  `where-vol` 1.0711 vs 1.0743, `stop-0.25` 1.0908 vs 1.0909).
- The card's "written ~23:55 UTC" is a clock misread: it was committed at 23:47 UTC (ffa9f48),
  before the script (23:49) and the run (rows stamped 23:55). Text otherwise as committed.
- No look-ahead: weights from rounds ending at the end of Thursday are used from the Friday
  22:30 decision on; unit tests scramble later outcomes and check the day-to-round mapping
  (`tests/test_hedgebooks1.py`).

## Tries

24 rows under idea `hedge-books-1`: 2 `variant` (`hedge16`, `hedge-pair`), 3 `baseline`
(`ew16`, `ew-pair`, `book/tsmom12`), 19 `robustness` (the other 15 stand-alone books, and
`hedge16`, `ew16`, `hedge-pair` and `book/tsmom12` at the gym's live costs).
Family bar: `BAR.md` (2026-11-24 20:01), N_eff 500, z >= 4.70. Nothing passes.
