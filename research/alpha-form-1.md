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

## Results

(Not computed yet.)
