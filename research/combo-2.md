# combo-2: combo-1 with T-bill cash, a partner for the years stocks and bonds fall together

Research lane combo-2 (DEEPER), night 2026-11-18. Branch `combo-2` (from `combo-1`, #70),
draft PR #75 into `combo-1`. Research only: fake money, the price cache already on disk, no
change to the live rules. Costs: the protocol's, passed explicitly (25 bps fee + 5 bps slip on
crypto, 2 bps on ETFs), as in combo-1.

Starting point (combo-1, `combo-1.md`): four of six models are one de-risking bet; `blend-ws`
(`where-vol` + `stop-0.25`, equal risk) 1.13 against `tsmom12` 1.05 (p 0.059) is the closest
miss, behind in 2022-25 where both sleeves fail; nothing wins both the fast fall and the turn.

## Step 1 card: `combo-cash` (fixed 2026-11-18, before any number with interest)

**How the cash interest got here.** `origin/cash-interest` (#61, base `main`, the same `main`
commit `combo-1` started from) is merged into this branch with a merge commit (957fdd1), so the
gym code arrives unchanged: `gym.simulate(rates=...)` pays idle cash the 13-week T-bill rate
(`^IRX`), accrued every calendar day, a session's rate known from its close. The only conflict
was `next-steps.md` (both sections kept). Research plumbing: `harness.run(rates=...)` (default
nothing, so every earlier script is unchanged) and `harness.bill_rates()` (the cached
`research/data/bars/IRX.csv`, train cut at 2025-11-10). `combo1_map.py` was split into
`main` + `tables` so the same tables can be drawn for other series; its output is byte-identical
(checked: rerun leaves `results/combo-1-map.md` unchanged).

**What is rerun, exactly as carded, no new choices.**

- The failure map: the six gym models of combo-1's map (`tsmom12`, `trend-vol`, `where-vol`,
  `stop-0.25`, `inverse-vol`, `sixty-forty`) plus the equal-weight yardstick, rebuilt from their
  logged configurations through the harness with T-bill cash. Same five tables. The regime
  masks (trend state, chop, fast fall, slow bear, stock-bond sign, `tsmom12`'s ten deepest
  falls and the six months after) are combo-1's, computed from the series without interest, so
  the regime days do not move and only returns change. `band` (perpetual carry, out of the gym)
  stays as saved: its collateral sits in the perps venue, not in gym cash.
- Both blends (`blend-iv`, `blend-ws`) on all four sets (six, 8 ETFs, 6 coins, 4 indexes), with
  combo-1's equal-risk shares, yearly refit, sleeves and costs; the sleeves, the combined book,
  the `tsmom12` twin and equal weight all get T-bill cash. The pass bar is combo-1's six bars,
  family 72 (p < 0.0014).

**Sharpe convention.** Two readings, both reported: (a) the carded statistic, Sharpe against
0 (the protocol's convention, what `tries.md` logs), and (b) Sharpe above the T-bill rate the
gym paid, #61's scoreboard convention (rf from an all-cash book replayed in the same gym, so it
is aligned day for day). The verdict on the card is read on (a); (b) is reported so a merge of
#61 does not silently change it.

**What would count as "a conclusion changes".** Any of: a blend's pass/fail on any bar; the
order of the six models' full-train Sharpes; the sign of any cell of the map's regime table
(section 2) that combo-1's text relies on (the de-risking group's turn and chop losses, their
fast-fall gains, `where-vol`'s fast-fall and 2022 losses); the de-risking group's excess
correlations dropping below +0.5 or `where-vol` + `stop-0.25` leaving -0.1..+0.1.

**Tries.** Robustness rows only, idea `combo-2`: the six map models with cash (6) and the two
blends on four sets with cash (8). Sleeve rebuilds inside the blend runs are not logged again
(the same decisions as their rows). These rows do not count in the family bar (no new pick).

## Step 1 result: `combo-cash` (2026-11-18)

Tables: [`results/combo-2-cash.md`](results/combo-2-cash.md), from `lib/combo2_cash.py` (one
logged run, 22:23 UTC; 14 `robustness` rows in `tries.md`). Plumbing check: `tsmom12` rebuilt
without interest reproduces deep-1's atlas series exactly. Average bill rate 2.4% a year on
the six assets' span, 4.4% on the indexes' (from 1962).

**No verdict changes; both blends still fail the card. Cash interest lifts every cash-holding
book about equally, so most of combo-1's map survives unchanged. Four details move.**

| Six assets, 1994-2025 | Sharpe vs 0, before -> with cash | above T-bills | vs `tsmom12` (p), with cash | 2022-25 | Worst loss | Card |
|---|---:|---:|---:|---:|---:|---|
| `tsmom12` | 1.05 -> 1.08 | 0.93 | | 0.90 -> 0.97 | 36.5 -> 35.6% | |
| `blend-ws` | 1.13 -> 1.16 | 1.00 | +0.08 (0.051); above bills +0.06 (0.108) | 0.82 -> 0.91 | 28.9 -> 25.7% | fails 1, 2 (as before) |
| `blend-iv` | 1.07 -> 1.09 | 0.91 | +0.01 (0.450); above bills -0.02 (0.590) | 0.93 -> 0.97 | 44.4 -> 42.8% | fails 1, 2, 3, 4 (was 1, 3) |

What changed, against "what would count" in the card:

1. **`blend-iv` gets worse: it now fails four bars, not two.** Eras 3 of 5 (2022-25 is now a tie
   at 0.97, 2000-09 behind) and out of universe 1 of 3 (indexes -0.09, ETFs -0.01). The
   always-invested half earns no interest, the `tsmom12` it is compared with does: half of the
   blend gives up the cash yield. Dead either way.
2. **`blend-ws` is unchanged in substance:** +0.08 against 0 (p 0.051, bar 0.0014), +0.06 above
   T-bills (p 0.108); still behind `tsmom12` in 2022-25 (0.91 against 0.97); indexes now -0.01
   (was +0.00), so bar 4 rests on +0.02 ETFs and +0.04 coins. Worst loss 25.7% against 35.6%.
3. **Order of the map's Sharpes: `trend-vol` catches `tsmom12`** (1.076 each, against 0; was
   1.03 against 1.05): the most cash-heavy rule gains most. Above T-bills it is behind again
   (0.89 against 0.93), so this is the convention, not a new edge. `where-vol`'s lead shrinks
   (+0.015, was +0.02); `stop-0.25` keeps +0.05.
4. **2022-25 is less bad for the cash holders.** `tsmom12` 0.97 (was 0.90), `stop-0.25` 0.87
   (0.70); `where-vol` stays 0.86 (it held bonds, not cash). Above T-bills every book is lower
   (`tsmom12` 0.72, `where-vol` 0.64, `stop-0.25` 0.50).

Unchanged: every regime cell's sign that combo-1's text uses (de-risking group: turn -19 to
-32% a year, chop -7 to -21, fast falls +36 to +54; `where-vol`: fast falls -10.3, 2022 rate
shock -13 points), every pair correlation within 0.02 (de-risking pairs +0.48..+0.94,
`where-vol` + `stop-0.25` -0.02). The one sign flip, `inverse-vol` in trend-off (+1.6 -> -0.7),
is a cell the text does not use: `tsmom12` sits in cash there and now earns on it.

**Reading.** combo-1's conclusions are robust to cash accounting. The rate matters for the
blends only through the half that holds no cash (`inverse-vol`), which falls further behind.
The 2022 gap is still there with cash: in 2022-25 `blend-ws` trails `tsmom12` with or without
interest, because its sleeves lost in assets (bonds, coins), not in cash.
