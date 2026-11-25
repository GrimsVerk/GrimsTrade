# rl-7: a small learned policy against `tsmom12` on ~50,000 market-months

Lane `rl-7`, 2026-11-25 (night). Branch `rl-7`. Research only: fake money, files already in
the local cache (nothing downloaded), no change to the gym, the daily runner or the live
strategies; nothing after 2025-10 read, project held-out year untouched. Card (pushed before
any number, not amended): `cards/rl-7.md` (commit b5a59d3, 21:54 UTC). Tables:
`results/rl-7.md` (+ `rl-7-gate.json`, `rl-7-final.json`). Code: `lib/rl7_data.py`,
`lib/rl7.py`; tests `tests/test_rl7.py` (offline, made-up data). Compute: seconds on one CPU.

## The answer on one screen

**No. The learned policy does not beat `tsmom12` out of sample in a way this test can see.**
On 56 markets it never trained on, 1990-2025 (20,962 market-months), the policy-gradient
learner `pg-lin` is ahead by **D = +0.016 Sharpe a market (SE 0.034, z 0.46)**, ahead in 32
of 56 markets. That is far from the project bar (z 4.70) and from the family bar (z 1.96). By
the card it is **"not shown"**: the one-sided 95% upper bound is +0.072, so an edge of +0.05 to
+0.07 a market cannot be ruled out, but nothing near a pick is possible on this evidence.

- **The gate worked, and it changes what the RL line's failure means.** `pg-lin` (a linear
  sigmoid policy trained by exact-gradient ascent on a mean-variance reward: the
  contextual-bandit form of policy gradient) passes rl-4-style planted gate on all four bars.
  It finds a planted monthly IC of 0.05 (lift +0.014, z 1.91, 90% of its ceiling) and 0.10
  (+0.047, z 3.37), and pure noise costs it nothing (+0.000). PPO failed the same kind of gate
  in rl-3/rl-4. So at this data size the learner is not the limit.
- **`lasso-sign` fails the gate**, and not because the lasso cannot find the input (it finds
  0.10, z 2.15). Its long-or-flat sign rule rarely changes position on a weak signal: the
  forecast is almost always above zero (mean position 0.76-0.90). Even its told-the-answer
  ceiling gains nothing at 0.05 (-0.002). The sign rule throws a weak forecast away. By the
  card it was not run on held-out data.
- **What `pg-lin` learned** (fitted on 23 markets x 9,149 months before 1990): mostly trend.
  The largest weights are on the 12-month sign and return (`up12` +0.31, `m12` +0.19) and on
  the last month (`up1` +0.20, `m1` +0.14), then the 6-month sign (+0.11). It is a graded
  blend of 12-month trend and one-month continuation, close to `e4` in spirit. It holds a much
  smaller position (mean 0.13 against `tsmom12`'s 0.64) and moves it less (0.50 against 1.18 a
  year). Its +0.016 is the size of edge `e4`-like graded rules have shown here before (+0.01
  to +0.06), not a new kind of edge.
- **The secondary cells agree it is noise around zero.** On the train markets after 1990,
  +0.006 (z 0.24). On the held-out markets before 1990, -0.024 (z -0.77). Out of fold on the
  training cell, -0.028 (z -1.17). By class in the primary cell: equity +0.027 (24/39),
  commodities +0.054 (3/4), rates -0.018 (3/8), currencies -0.047 (2/5). Signs do not agree
  across cells or classes.

**How sure.** The gate is the strongest part: one fixed noise draw at every strength, the
realised planted ICs came out on target (0.057, 0.107), and the ceiling is close to the learner.
The final run was done once, after the gate rows were pushed (commit 3e6bc01, 21:57:33 UTC;
the final ran at about 21:58). The test's power is low, as the card said. The gate itself
measures it: a planted monthly IC of 0.05 beyond the price features is worth only about +0.014
Sharpe a market, and 0.10 about +0.05. With a held-out SE of 0.034, z 4.70 needs D of about
+0.16. That is a signal several times stronger than a monthly IC of 0.10, which no past-price
feature is known to carry.

## What this means for the RL line

- **More data rescued the learner, not the strategy.** With ~100x the market-months of
  rl-1..rl-6, a policy-gradient learner now passes the planted gate that PPO failed. Pointed at
  real past-price features, though, it relearns trend and lands within noise of `tsmom12`. The
  limit is the inputs: monthly past prices carry about one trend signal, and `tsmom12` already
  has it.
- **The RL line stays closed for price-only inputs.** Do not retune `pg-lin` (risk aversion,
  penalty, features) on these data. Every series the project has is now in either its
  training cell or one of its held-out cells.
- **If the line is reopened, change the inputs, not the learner.** Inputs whose own calendar
  differs from trend (carry, value, macro: data-long-3/4 have them for 9-11 economies) are the
  candidates. `pg-lin` and this gate are the ready pipeline. Such a card must name the input
  set first and count every input it tried.

## Disclosures

- All held-out series had been scored before by pooled-1/pooled-2/e4-indep-1 for `tsmom12`,
  `e4` and own-vol, so 12-month trend's behaviour there was known in outline. No learner had
  been fitted on them. The feature list (standard trend inputs) was fixed on the card and not
  tuned.
- The loader labels the 8 ETFs `equity` (pooled-1's convention), so the class slice counts
  IEF/LQD and DBC/SLV under equity. This does not change the verdict: z < 1.96 in every slice.
- Cash earns 0 on the series that are not already excess returns (stocks, commodity spot),
  as in pooled-1/e4-indep-1. Sharpe does not depend on scale, so `pg-lin`'s small position
  is not a handicap. But matching `tsmom12`'s risk would need about 5x leverage, which the
  paper broker does not allow.
- The gate rows in `tries.md` are stamped 21:58 by hand. The gate ran at 21:56-21:57 and was
  pushed at 21:57:33, before the final run. The order shows in the commit times.
- After the final run, only formatting changed in `rl7.py` (ruff). The gate was re-run once
  after that change, as a check that it reproduces: the output was identical. The final run
  was not repeated.

## Tries

25 rows in `tries.md`. Idea `rl-7-control`: 15 `control` rows (the `tsmom12` training-cell
reference, and per learner the strengths none/0.00/0.05/0.10 plus the ceiling at 0.00/0.05/0.10).
Idea `rl-7`: 1 `variant` (`pg-lin` on the primary cell), 1 `baseline` (`tsmom12` on the primary
cell), and 8 `robustness` rows (4 class slices, plus each rule on the two secondary cells).
Nothing was trained beyond the configurations the card lists.
