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

## fast-reentry-2: exposure controls and the "armed" re-entry (2026-11-18, PR #96)

Card `cards/fast-reentry-2.md` (pushed before any number), code `lib/fastreentry2.py` (one
run, 7 s), tables `results/fast-reentry-2.md`.

**Verdict by the card: "In between" again. Keeping `tsmom12`'s exits and changing only the
re-entry (`arm3-12`) gives almost the same result as `or3-12`: the insurance leaks through the
re-entry itself (bear-market rallies), not through the slower exit. The fast-reentry line
closes; the insure line has no pick left worth its bar.**

### (a) Is `or3-12`'s lower premium timing or exposure? (description)

insure-1's card 2 controls on the US 11 series, each rule against its own average position and
its own rotated positions (1,000 rotations):

| | Share avoided S | N, log pts | Premium P |
|---|---:|---:|---:|
| `tsmom12` / fixed 73% / rotations (median) | 0.50 / 0.29 / 0.27 | -0.3 / +2.5 / +1.3 | 1.07 / 1.63 / 1.82 |
| `or3-12` / fixed 83% / rotations | 0.35 / 0.18 / 0.17 | +1.2 / +1.6 / +0.8 | 0.97 / 1.61 / 1.85 |
| `arm3-12` / fixed 81% / rotations | 0.37 / 0.20 / 0.19 | +1.6 / +1.8 / +0.8 | 0.98 / 1.61 / 1.85 |

- **Timing, not just exposure**, for all three (S and P: p 0.000 against rotations; P well
  below fixed exposure). `or3-12`'s premium of 0.97 is not bought by its extra exposure alone:
  holding 83% costs 1.61. Its margin over its own controls is about `tsmom12`'s (premium 0.64
  below fixed vs 0.56; share +0.17 vs +0.21). Net of the rebound none beats simply holding its
  average position (N against rotations: p 0.82 / 0.41 / 0.33 in table order).

### (b) `arm3-12`: exit as `tsmom12`, re-enter when the 3-month return turns positive

| | US, 50 effective falls (decides) | 13 developed non-US, 19 falls |
|---|---|---|
| Rebound dB | **+7.7**, 40 of 49 | +9.2, 19 of 19 |
| Insurance dI | **-5.9**, 8 of 48 better | -3.9, 4 of 18 |
| **Net dN** | **+1.8** (28 of 50; sign p 0.24, bootstrap p 0.11) | +5.3 (13 of 19; p 0.084, 0.000) |
| Share avoided | 0.50 -> **0.37** (guard: drop 0.13 > 0.10, fails) | 0.49 -> 0.42 |
| Premium, full period / 2002-2025 | 1.07 -> 0.98 / 1.34 -> 1.31 | 1.11 -> 0.97 / 1.11 -> 0.98 |
| Mean position, flips a year | 73% -> 81%, 1.9 -> 2.9 | 66% -> 77%, 2.4 -> 3.8 |
| Worst loss (first series) | 38% -> 51% (US market) | 41% -> 41% (Japan) |

- **The exit was not the leak.** `arm3-12` leaves at every `tsmom12` exit (`or3-12` stayed in at
  369 of 1,030), yet it keeps only one more log point of the fall (dI -5.9 vs -6.9; share 0.37
  vs 0.35). Against `or3-12` directly: dN +0.4, 28 of 45 falls. The loss is in the re-entries:
  the four worst US clusters are again 1929-1933 (-16 to -29 log points), where every 3-month
  rally was bought and the next leg ridden down.
- **Where it helps**, as before: slow falls (US +4.1 per episode) and the long rebounds after
  1974 (+29) and the 1960s-70s falls; outside the US fast falls (+7.2, 17 of 23) and the 2008
  rebound. Non-US is consistent by bootstrap (p 0.000) but not by sign (0.084), and those falls
  overlap the US ones in time.
- **Bar.** Second pick in the insure line, family bar p < 0.025: not met on the deciding set
  (0.24 / 0.11). Project-wide bar (register-2: N 433 effective, Bonferroni p <= 1.2e-4): far.

### Should the line close?

**Yes, the re-entry line closes** (as the card set it: two pre-registered re-entry rules, both
in between). Any 3-month re-entry trades insurance for rebound almost one for one on US data
(dI about -6 to -7 against dB +8); the remaining +1.5 to +1.8 net is noise at 50 falls. **The
insure line has no further pick worth its bar** (a third pick would need p < 0.017 on an effect
two rules put at sign-test p 0.10-0.24): close it for new picks. Its standing description holds:
`tsmom12`'s insurance is timing, not just exposure, at a premium of about 1.3-1.5 since 2002,
and the late buy-back is the price of it. The held-out year stays unspent; nothing changes for
the live rule.

`tries.md`: 27 rows, idea `fast-reentry`: 1 `variant` (`arm3-12@insure-Mkt`), 26 `robustness`.
Part (a) added none.
