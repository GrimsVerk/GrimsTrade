# fast-reentry: does a quicker return after the low keep more of trend's crash insurance?

Lane fast-reentry, 2026-11-18 (night). Branch `fast-reentry` (from `insure-2`), draft PR #94.
Research only: fake money, files already in the data cache, no change to the gym, the daily
runner or the live strategies. Held-out year untouched (nothing after 2025-10-31 parsed). Card
(pushed before any number): `cards/fast-reentry.md`. Tables: `results/fast-reentry.md`. Code:
`lib/fastreentry.py` (reuses insure-1/insure-2's episodes and clusters; one run).

## The answer on one screen

**Verdict by the card: "In between". Returning sooner does win back much of the rebound, but
the rule tested pays for most of it in the fall itself. Net of the year after the low it is a
little better (+1.5 log points per US fall, not significant), and the lower premium comes mostly
from buying less insurance, not from cheaper insurance.**

Rule `or3-12`: hold if the 12-month OR the 3-month return is positive (trend-tune's "slow to
leave, quick to return" cell, taken as named). Against `tsmom12`, both as paper series, on the
same 25% falls:

| | US, 50 effective falls (decides) | 13 developed non-US, 19 falls |
|---|---|---|
| Rebound B (year after the low) | **+8.4** better, 41 of 49 falls | **+9.3**, 18 of 19 |
| Insurance I (peak -> trough) | **-6.9** worse, 8 of 48 better | -4.5, 2 of 18 |
| **Net N = I + B** | **+1.5** (30 of 50; sign p 0.10, bootstrap p 0.19) | +4.7 (12 of 19; p 0.18, 0.002) |
| Share of the fall avoided | 0.50 -> **0.35** | 0.49 -> 0.41 |
| Premium, full period | 1.07 -> 0.97 | 1.11 -> 0.97 |
| Premium 2002-2025 | 1.34 -> 1.33 | 1.11 -> 0.98 |
| Rule minus holding, log pts per series-year | -0.57 -> +0.18 | -0.83 -> +0.18 |
| Mean position / worst loss (first series) | 73% -> 83% / 38% -> 51% (US market) | 66% -> 79% / 41% -> 43% (Japan) |

- **Why the insurance shrinks.** The OR rule is not only quicker to return: it also stays in at
  36% of `tsmom12`'s exits (369 of 1,030 US, 203 of 574 non-US), because the 3-month return is
  often still positive when the 12-month one turns. And in multi-leg bear markets it buys the
  rallies and rides the next leg down: the largest losses against `tsmom12` are 1929-1933 (four
  clusters, -16 to -29 log points each) and 1992. The card's guard (share avoided at most 0.10
  below `tsmom12`) fails on US data (-0.15).
- **Where it helps.** Fast falls (three months or less), `tsmom12`'s weak spot: US +1.7 per
  episode (38 of 63), non-US **+7.4** (18 of 23; net -15.0 -> -7.6), and the long rebounds after
  1974, 1982 and 2009 (+12 to +36). Outside the US the net gain is consistent (bootstrap p
  0.002) but the sign test is not (12 of 19).
- **The premium.** It falls on every set (US 1.07 -> 0.97; total-return regions 1.23 -> 1.06),
  but the rule holds 10-13 points more stock and lost 51% instead of 38% on the US market. A
  lower premium on a smaller policy is not cheaper insurance; whether `or3-12` beats simply
  holding 83% (insure-1's card 2 controls) was not on the card and is not claimed. On US data
  since 2002, the "today" number, the premium did not move (1.34 -> 1.33).
- **For the live rule.** Nothing changes. The late buy-back is mostly the price of the
  insurance: a quicker return trades it for a smaller and leakier policy, as stop-reentry found
  on coins (PR #82). The insurance premium of about 1.3-1.5 since 2002 stands.

## Bar and how sure

- **Family count: a new pick in the insure line, the first** (insure-1/2 selected nothing):
  family bar p < 0.05. Not met on the deciding set (US sign test p 0.10, bootstrap 0.19).
  **Project-wide bar** (register-2, PR #92, `research/register/BAR.md`: 3,023 tries, N 433
  effective trials, Bonferroni p <= 1.2e-4): far from it. No live change could follow anyway:
  trend-tune saw this rule at +0.01 Sharpe over `tsmom12` on the six-asset primary test, against
  a needed +0.30.
- One rule, fixed before any number, run once (card, script and results are separate pushed
  commits). The rule was named by trend-tune from the six assets 1994-2025, not from these
  falls; these series overlap that window in time (US 1994-2025, non-US) but were not used to
  choose it.
- Both rules are paper series (insure-1's `tsmom12` premium 1.07 used the gym splice; the paper
  series gives the same 1.07 here). Non-US indices are price indices (premium level flattered,
  as insure-2 noted; the comparison between the two rules is not). Effective falls overlap in
  time across the US and non-US sets, so the two are not independent confirmations.
- `tries.md`: 27 rows, idea `fast-reentry`: 1 `variant` (`or3-12@insure-Mkt`), 26 `robustness`
  (10 US industries, 13 developed indices, 3 French regions).

## Next lanes (not started)

1. `or3-12` against insure-1's card 2 controls (fixed exposure at its 83%, rotated positions):
   is its lower premium timing or just more exposure? One re-scoring, no new rows.
2. The "armed" pure re-entry rule the card set aside (keep `tsmom12`'s exits; re-enter on a
   positive 3-month return only after it has been negative since the exit): isolates the
   re-entry from the slower exit that cost the insurance here. Second pick in the insure line
   (family bar 0.025); its own card first.
3. Nothing for the live rule; if (2) also lands "in between", close the fast-reentry line.
