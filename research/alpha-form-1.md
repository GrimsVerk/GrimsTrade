# alpha-form-1: the finished record re-scored in alpha form (does a rule add to `tsmom12`?)

Lane `alpha-form-1`, 2026-11-24 night. Branch `alpha-form-1` from `main` (`f7778a0`). A **lens
on finished tries, not new tries**: no backtest, no price bar, nothing after 2025-11-10. Inputs
are only the committed weekly returns store (`research/register/returns/`, card
`register-4.md`), the committed register (`research/register/tries.jsonl`) and the rows of
`research/tries.md` on this branch (to tell which stored series are selectable). This card was
written and pushed before any number below its "Results" heading was computed.

## Question

The bar (`research/register/BAR.md`) asks a new pick for a Sharpe edge over `tsmom12` at
z >= 4.69 (N_eff 486). `power-map-1.md` (PR #150) argues that this difference form is out of
reach for a rule not close to `tsmom12` (an uncorrelated rule needs a standalone Sharpe of
about 2.3 at 32 years), and that an **alpha form** (does the rule add to the best mix with
`tsmom12`?) is the one comparator where an honest pass is not absurd. Nobody has re-scored the
existing record that way. Question: under the alpha form, does any finished selectable try
pass, or come close, and does that change any conclusion in `research/SUMMARY.md`?

## Method (fixed before any number)

### Which series

- The store's rows, matched to register rows with `register2.match` (idea, variant, train
  period, start within 10 days, Sharpe to 0.0051; a row two different series fit is dropped
  as ambiguous). Register rows: the committed `tries.jsonl` plus the rows of this branch's
  `research/tries.md` not in it (the store already holds series of tries logged since the last
  regeneration; their `tries.md` rows are on `main`). Parsed with `grimstrade.register`.
- **Selectable** = a matched row of kind `variant` or `baseline`, period `train` (BAR.md's
  definition). Live strategies are not selectable tries and are left out (their series are
  the live books, scored by the forward record).
- One score per distinct series: series with identical weekly returns are scored once
  (harness copy preferred over a saved curve), under the first key in sorted order.
- Every series is cut at the last Friday before 2025-11-10 (train only).

### The comparator (`tsmom12`'s stored series)

As in the bar's own form and `power-map-1` (M5): the `tsmom12` of **the same universe**.
For a variant with an `@<universe>` suffix, the first that exists in the store, in this order:
`baselines/tsmom12@<u>`, `<idea>/tsmom12@<u>`, `<idea>/TS@<u>`; among several stored copies
with that key, the one with the longest overlap (harness copy on ties). Otherwise (no suffix,
or no same-universe `tsmom12` stored): the primary `baselines/tsmom12` (six assets, from
1994-02-01, harness copy). The table says which comparator each series met. A series that is
its own comparator (same key, or weekly correlation above 0.999) is not scored.

Sensitivity (reported, not the headline): every series against the primary six-asset
`tsmom12` (the book a new pick would actually join).

### The statistics

Over the common weeks (both finite), weekly simple returns as stored (no risk-free rate taken
off, like the register's Sharpes), r = rule, t = its `tsmom12`:

1. **Residual information ratio.** OLS r = a + b t + e. IR = a / sd(e) x sqrt(52.18).
   **z = a / SE(a)** with a Newey-West (Bartlett) SE, lag L = floor(4 (n/100)^(2/9)).
   For every series with NW z >= 3.0 and for the top 20, a check: a circular block bootstrap
   (52-week blocks, 2,000 draws, fixed seed 20261124) of a; **the larger of the two SEs
   decides a pass** (cautious). One-sided: only positive alpha counts.
2. **Best long-only mix.** w in [0, 1] on the rule, 1 - w on `tsmom12` (fully invested; Sharpe
   is scale-free, so no leverage is needed to read it): w* maximises the in-sample Sharpe
   (closed-form tangency weight, clipped to [0, 1]; the Sharpe is quasi-concave in w, so the
   clip is the constrained optimum). **Mix gain** = SR(mix) - SR(`tsmom12`), annual. Its SE: the
   same block bootstrap with w re-optimised in every draw. The gain is >= 0 by construction
   (w = 0 is allowed) and biased upward in sample, so it is reported as the **size** of what a
   rule adds; the test is z of step 1 (for one added asset the unconstrained version of this
   test is the alpha t: Gibbons, Ross and Shanken 1989).
3. For contrast only: the bar's own difference form for the same pair, z_d = (SR_r - SR_t) /
   SE_JK (Jobson-Korkie with Memmel's correction, as in `power-map-1` M1).

### Minimum overlap

**5 years** (261 common weeks). Shorter series are counted and listed as not scored.

### The bar (not lowered)

- **z >= 4.69**: the same N_eff 486 as BAR.md (measured rho 0.53, A.3, at most 10 per family).
  The alpha form is a different statistic on the **same** tries, so the trial count does not
  change. If anything it should go up: looking at the record through a second lens after the
  first is itself a choice. No allowance is made for that here; it would only raise the bar.
- **z >= 3.29** is reported beside it: the ONC (cluster-count) end of BAR's range, where the
  counting method decides (review-2, section 1b). A series between 3.29 and 4.69 is not a pass.
- A pass here would not be a pick: it would be a candidate for a pre-registered held-out
  test (`gate-null.md`), and the lens itself would need the lead's acceptance as a comparator.

### Families

BAR.md caps at most 10 series per family when it measures rho for N_eff; that cap is in the
4.69 already. Pass counts here are per series, uncapped (every stored selectable series is
one of the counted tries). Because large families (`trend-tune-surface` holds about 100
near-copies) can fill a top list, the results show the top 20 series uncapped **and** the best
series per family, the count of series at z >= 3.29 per family, and the top 20 with at most
10 per family (BAR's cap) if the cap changes the list.

### Outputs

- `research/alphaform1.py` (numpy, stdlib, `grimstrade.returnstore`, `register2`;
  deterministic), run as `uv run python research/alphaform1.py > research/results/alpha-form-1.md`.
- `tests/test_alphaform1.py`, synthetic series: a known alpha is recovered (IR and z near the
  planted values); a leveraged copy of `tsmom12` (2 x t) has IR about 0 and mix gain about 0;
  pure noise gives |z| small; the long-only weight is clipped.
- This file's results: the top 20 by z (family, overlap years, IR, z, mix gain), the pass
  counts at 4.69 and 3.29, which families concentrate the top, and a plain verdict on whether
  the lens changes any conclusion in `research/SUMMARY.md` (that file is not edited here).
- One `note` row in `research/tries.md` (a re-scoring, not a try; the selectable count is
  unchanged).

## Results (computed 2026-11-24 after the card, `acc7dd3`, was pushed)

Full tables: [`results/alpha-form-1.md`](results/alpha-form-1.md), generated by
`research/alphaform1.py` (3 s, deterministic: a second run gives the same bytes). Tests:
`tests/test_alphaform1.py` (a planted IR of 0.8 is recovered; `2 x tsmom12` has alpha 0 and mix
gain 0; a losing uncorrelated rule gets w* = 0; bootstrap SE near the NW SE on iid data).

### In plain words

- **Nothing passes in the alpha form either.** 341 distinct selectable series scored against
  their universe's `tsmom12`: **0 at z >= 4.69**, **2 at z >= 3.29**. The best is z 4.31.
- **The two that reach the 3.29 end are known artefacts, already explained in the record.**
  1. `fm-1 / fm-bolt-base-tilt` (z 4.31; NW alone 4.82, bootstrap 4.31; IR +0.99, mix gain
     +0.21): a Chronos-Bolt forecast tilt that `fm-1.md` showed is **memorisation** of price
     history seen in pretraining (IC about 0 on 2020-2025 and on inverted prices). Void.
  2. `diversifier-1 / merfx7` (z 4.14; NW 5.44; IR +0.96, but mix gain only +0.04, rho 0.995):
     6/7 `tsmom12` + 1/7 a merger-arb fund. `diversifier-1.md` showed this is the gym's
     **cash-earns-0 convention**: an always-held low-volatility slot earning about bills
     beats idle cash (above T-bills its Sharpe gain is +0.018, z 2.2).
  Under the card's cautious rule (the larger of NW and bootstrap SE) both are below 4.69; with
  the NW SE alone both would have been above it. That is how close the line is drawn, and why
  the card fixed the cautious rule in advance.
- **The rest of the top 20 is z 2.1-3.1, and most of it has a known non-skill reason:** plain
  holding beat trend on one equity fund in a bull window (`eu-1 hold@SXR8`, 2012-2025, z 3.14);
  bond-holding slots against a book whose cash earns 0 (`month-end-bonds last4@LQD` z 3.08,
  `auction-concession constant@IEF` z 2.35; the record's own twin test found `last4@LQD` no
  better than holding LQD at a constant 19%, -0.08, p 0.58); a coin calendar effect in two or
  three halving cycles (`halving-alone`, z 2.92, SUMMARY already names it); an in-sample tuning
  ceiling that "cannot be selected" (`trend-tune-surface hindsight-asset`, z 2.69, logged as a
  variant). The one plain rule near the top is the `sma200@GSPC` baseline against
  `tsmom12@GSPC` (S&P 500 index from 1962, 31 years, IR +0.60, z 3.07): a different trend
  rule on one index, below 3.29.
- **The record is close to what luck alone gives.** 28 series at z >= 2 (7.8 expected if all
  341 were independent nulls), 61 at z >= 1.645 (17.0). The excess is expected: the series are
  not independent (about 100 `trend-tune-surface` near-copies, rho with `tsmom12` 0.9+) and
  every bond-like or cash-like slot gets a positive alpha from the cash-0 convention. The 2 at
  z >= 3.29 against 0.17 expected are the two artefacts above.
- **Families.** No family concentrates the top: the top 20 hold 14 families, at most 3 from one
  (`trend-tune-surface`, 3 of its 97). BAR's cap (at most 10 per family) leaves the top 20
  unchanged. Families with a z >= 3.29 series: `fm-1` and `diversifier-1` only.
- **Size, not just z.** Median residual IR +0.14, median mix gain +0.010 Sharpe; p90 +0.09.
  The largest mix gains (+0.25 to +0.31) are single-asset holds over 13-17 years with bootstrap
  SEs of 0.09-0.16.
- **Sensitivity (all against the six-asset `tsmom12`):** 363 scored, 0 at 4.69, 2 at 3.29 (the
  same two), max z 4.33. The comparator choice changes nothing.
- **Contrast with the bar's own form on the same pairs:** z_d >= 3.29 for 3 series and >= 4.69
  for 1 (`merfx7`, 5.18 with the Jobson-Korkie SE, the nominal pass `diversifier-1` already
  explained away). The alpha form ranks uncorrelated slots higher (`last4@LQD`: z_d -1.75,
  alpha z 3.08), as power-map-1 said it would, but no uncorrelated series gets near 4.69.

### Top 20 (decision z)

| # | Series | Family | Comparator | Years | IR | z | Mix gain | Known reason |
|---:|---|---|---|---:|---:|---:|---:|---|
| 1 | `fm-bolt-base-tilt` | fm-1 | six-asset | 25.8 | +0.99 | 4.31 | +0.207 | pretraining memory (fm-1) |
| 2 | `merfx7` | diversifier-1 | six-asset | 31.8 | +0.96 | 4.14 | +0.042 | cash earns 0 (diversifier-1) |
| 3 | `hold@SXR8` | eu-1 | `tsmom12@SXR8` | 13.8 | +0.99 | 3.14 | +0.305 | holding one fund, 2012-2025 |
| 4 | `last4@LQD` | month-end-bonds | six-asset | 23.3 | +0.63 | 3.08 | +0.157 | bond slot vs cash 0; = its constant twin |
| 5 | `sma200@GSPC` | baselines | `tsmom12@GSPC` | 31.0 | +0.60 | 3.07 | +0.248 | baseline trend rule, one index |
| 6 | `halving-alone` | halving | six-asset | 31.8 | +0.86 | 2.92 | +0.249 | 2-3 coin cycles (errata-2) |
| 7 | `hindsight-asset` | trend-tune-surface | six-asset | 31.8 | +0.52 | 2.69 | +0.115 | in-sample ceiling, not selectable |
| 8 | `equal-weight@euw-2009` | eu-1 | `tsmom12@euw-2009` | 16.8 | +0.65 | 2.53 | +0.267 | holding, bull window |
| 9 | `even-gate` | fomc-cycle | six-asset | 31.8 | +0.68 | 2.39 | +0.195 | |
| 10 | `constant@IEF` | auction-concession | six-asset | 22.3 | +0.53 | 2.35 | +0.110 | bond slot vs cash 0 |
| 11 | `fm-bolt-small-tilt` | fm-1 | six-asset | 25.8 | +0.60 | 2.29 | +0.099 | pretraining memory |
| 12 | `L08-m` | trend-tune-surface | six-asset | 31.8 | +0.48 | 2.25 | +0.102 | |
| 13 | `flag100-sma@G30-disc` | gsy-runup | `tsmom12@G30-disc` | 73.5 | +0.39 | 2.23 | +0.021 | |
| 14 | `hold@F62-Shops` | trend-1926 | `tsmom12@F62-Shops` | 40.0 | +0.39 | 2.21 | +0.111 | holding |
| 15 | `equal-weight@euw-hh` | eu-2 | `tsmom12@euw-hh` | 13.8 | +0.67 | 2.20 | +0.297 | holding, bull window |
| 16 | `mag-match-c@idx` | turbulence | `tsmom12@idx` | 63.8 | +0.41 | 2.17 | +0.113 | |
| 17 | `hold@F62-Hlth` | trend-1926 | `tsmom12@F62-Hlth` | 40.0 | +0.34 | 2.17 | +0.075 | holding |
| 18 | `L08-w` | trend-tune-surface | six-asset | 31.8 | +0.45 | 2.16 | +0.093 | |
| 19 | `sma200@GDAXI` | baselines | `tsmom12@GDAXI` | 36.9 | +0.40 | 2.15 | +0.158 | baseline trend rule, one index |
| 20 | `ath-and` | ath | six-asset | 31.8 | +0.42 | 2.15 | +0.082 | |

"Six-asset": no same-universe `tsmom12` is stored, so the primary one was used (234 of 341
series; 107 met a same-universe one). Rho, beta, the NW and bootstrap z's, w* and the
bootstrap SE of the mix gain are in the results file.

### Not scored

58 distinct selectable series: 50 are their own comparator (the `tsmom12` baselines of each
universe), 1 has under 5 years of overlap, 7 correlate above 0.999 with their comparator. One
of those 7 shows the cash-0 artefact at its plainest: `short-sleeve bill10@bills` (90%
`tsmom12`, 10% T-bills) has a residual IR of +4.8, NW z 10.3, against `tsmom12` whose idle
cash earns 0. The 0.999 rule (fixed on the card) kept it out; had it been scored it would have
"passed" for no reason but the convention.

### Limits

- **Cash at 0.** The store holds raw strategy returns and no T-bill series, so alpha is not
  measured above bills (the card said so). This inflates the alpha of every bond-like or
  cash-like slot (`merfx7`, `last4@LQD`, `constant@IEF`, `bill10@bills`) and the excess of
  z >= 2 counts over luck. It cannot create a false negative for a rule that holds risky assets,
  so it does not weaken the "nothing passes" finding. An above-bills alpha would need a weekly
  bill-rate series added to the store (a strategy-like series: hold bills).
- **Coverage.** Only series that are in the store and match a selectable register row: 399
  distinct (454 register rows) of the 1,072 selectable train rows in the register used here. Tries without a saved
  curve (logged before register-4/5, or by scripts that save none) cannot be re-scored here.
  The scored set is the measured part of the record, not all of it.
- **In-sample.** Every number is a train-period, in-sample alpha of a finished try; the mix
  weight is optimised in sample. A pass would have been a candidate for one held-out test, not
  a pick.
- **The lens itself is a choice made after the record exists.** The card kept the bar at 4.69
  and did not add trials for the second look; a stricter count would only raise the bar.

### Does the alpha lens change any conclusion in `research/SUMMARY.md`?

**No.** SUMMARY's conclusions stand: no rule beats `tsmom12` at the bar; the largest leads are
explained (it names `halving-alone`; the alpha lens adds `fm-bolt-base-tilt` and `merfx7` as the
only series near the bar, and both are artefacts the record already explained); `tsmom12` is
crash insurance rather than an edge, and nothing in the record adds a significant, explained
alpha to it. The one sentence a rewrite could add: "Re-scored in alpha form (does a rule add to
the best mix with `tsmom12`?), 341 stored tries: 0 pass z 4.69; the 2 above 3.29 are the
Chronos memorisation (`fm-1`) and the cash-earns-0 slot (`diversifier-1`)." That makes
power-map-1's point concrete: the alpha form is the fairer comparator for uncorrelated rules,
but on the finished record it finds nothing the difference form missed. If the lead adopts it
for future cards, the cards should score above T-bills (the `diversifier-1` lesson), or every
bond-like slot will look like alpha.

Tries rows added by this lane: one `note` row (a re-scoring, no new try).
