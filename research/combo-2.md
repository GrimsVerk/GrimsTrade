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

## Results

Filled in below as each step finishes.
