# reentry-reconcile-1: why does `e4` gain after the low when faster re-entry rules did not?

Lane `reentry-reconcile-1`, 2026-11-25 (night). Branch `reentry-reconcile-1`, PR #178.
Research only: fake money, files already in the data cache (read-only), no change to the gym,
the daily runner or the live strategies. Train data only: pooled-1's loaders stop at
2025-10-31. A **descriptive reconciliation** of finished tries (e4-anatomy-1 #168, pooled-1
#142, fast-reentry #94 / #96, bear-legs #103) on pooled-1's 41 stock markets and code: no new
rule, `e4` not retuned, nothing selected, the re-entry line stays closed. Card (pushed before
any number, not amended): `cards/reentry-reconcile-1.md`. Tables:
`results/reentry-reconcile-1.md` (+ `.json`). Code: `lib/reconcile_reentry.py`,
`lib/reconcile_reentry_core.py`; tests `tests/test_reconcile_reentry.py`. One run, 8 s.

## The answer on one screen

**Both hold, because `e4` does not buy back better. It also sells sooner.** Split `e4`'s
position gap to `tsmom12` exactly into a **buy-back part** (what it holds while `tsmom12` is
out) and a **trim part** (what it holds less while `tsmom12` is in):

- **`e4`'s buy-back part behaves like the old re-entry rules.** Per 25% fall on the same 41
  markets it gains +6.3 log points in the year after the low and gives back 4.4 inside the
  fall. It keeps 31% of its rebound gain; `or3-12` keeps 23% and `arm3-12` 26%. The old
  finding holds for `e4`'s legs too: early rallies look like the bottom. In e4-anatomy's
  Sharpe split the buy-back's rebound term is +0.134, exactly `or3-12`'s.
- **The trim part is what the re-entry rules lack.** The 1/3/6-month legs also cut the
  position before `tsmom12` exits. That gains +5.6 points per fall and pays for the bear-market
  rallies the buy-back buys. In slow bears the trims give +0.069 Sharpe and the buy-back
  costs -0.065, so e4-anatomy's slow-bear term nets to +0.003. Its rebound term (+0.092) is
  the buy-back's +0.134 minus the trims' -0.042: the trims hold back early in rebounds too.
  The trims cost in calm markets (-0.157) and are paid back by lower volatility (risk part
  +0.087; the 3-month rules' risk part is -0.040 to -0.046 because they hold more).
- **A smaller edge is the graded buy-back.** `e4-re` is `e4` with its trims removed. It beats
  `or3-12` and `arm3-12` scaled to the same mean buy-back size by +0.022 and +0.028 Sharpe
  (paired SE 0.010 and 0.014). The reason: a buy-back on one leg is a quarter slot, and it
  grows only as more legs agree. Per fall this still keeps only 31% of the rebound gain,
  against 25% for the size-matched `or3-12`.

The card's explanations, judged by its rules:

| | Verdict | Why |
|---|---|---|
| (a) part size | **rejected** | Size scales the rebound gain and the bear-rally cost by the same factor (K 0.23-0.32 at every w, 1 included). The best sleeves move D by +0.005 at most: `or3-12` +0.018 to +0.023, `arm3-12` +0.015 to +0.019. |
| (b) sample | **rejected** | On the 41 markets the 3-month rules repeat the US result: dB +8.4 / dI -6.5 (`or3-12`) against fast-reentry's US +8.4 / -6.9; K 0.23 and 0.26. |
| (c) definitions / metric | **does not carry** | Same zigzag and rebound window by construction. Per fall `e4` keeps 1.53 times its rebound gain (dN +5.4 against dB +3.5): that is its trims, not a different measure. |
| (d) exits | **carries** | Trim terms in falls +0.098 against the buy-back's slow-bear cost -0.065. |
| (d) signals | **carry, small** | `e4-re` beats the size-matched sleeves by +0.022 / +0.028 (beyond 2 paired SE). Rebound gain per unit of slow-bear cost: 2.05 against 1.81 / 1.89. |

**So the summary line "faster buy-back rules did not fix this: early rallies look just like
the bottom" stays true, `e4` included.** `e4` does not fix the late buy-back. It offsets the
cost of an earlier, leaky buy-back with earlier, partial exits. In Sharpe terms neither half
does much alone (`e4-re` +0.045, `e4-trim` +0.014). Together they make `e4`'s +0.063, still
not shown (z 1.55, pooled-1). The lead over the 3-month rules is +0.044 / +0.048 with paired SE
0.025 / 0.026: within noise.

## Numbers behind it

Equity 41, Sharpe points per market against `tsmom12`, card split, 25% zigzag (reading A):

| Rule | D | Risk part | Return part | Fast | Slow bear | Rebound | Whipsaw | Calm |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `e4` | +0.063 | +0.087 | -0.024 | +0.022 | +0.003 | +0.092 | +0.018 | -0.159 |
| of which buy-back | | | +0.080 | -0.008 | -0.065 | +0.134 | +0.018 | +0.002 |
| of which trims | | | -0.101 | +0.030 | +0.069 | -0.042 | +0.000 | -0.157 |
| `or3-12` (all buy-back) | +0.018 | -0.046 | +0.064 | -0.009 | -0.074 | +0.134 | +0.015 | -0.001 |
| `arm3-12` (all buy-back) | +0.015 | -0.040 | +0.055 | -0.010 | -0.066 | +0.124 | +0.007 | -0.000 |
| `e4-re` (diagnostic) | +0.045 | -0.019 | +0.064 | -0.007 | -0.054 | +0.109 | +0.014 | +0.001 |
| `e4-trim` (diagnostic) | +0.014 | +0.123 | -0.109 | +0.032 | +0.074 | -0.045 | -0.000 | -0.171 |

(The `e4` component rows leave out its cost term, -0.005, and compounding residual, +0.002.)
Mean buy-back position in rebounds: `e4` 0.24, `or3-12` 0.33, `arm3-12` 0.29. Mean trim in
falls: `e4` -0.15 to -0.18.

Per 25% fall (491 falls over 41 markets, equal weight, log points net of costs):

| Rule | dI (fall) | dB (rebound) | dN | K = dN / dB | dN > 0 | US10: dI / dB |
|---|---:|---:|---:|---:|---:|---|
| `e4` | +1.88 | +3.54 | +5.42 | 1.53 | 68% | +0.88 / +3.11 |
| `e4-re` (buy-back only) | -4.35 | +6.32 | +1.97 | 0.31 | 56% | -5.08 / +5.92 |
| `e4-trim` (trims only) | +6.23 | -2.79 | +3.44 | n/a | 62% | +5.95 / -2.81 |
| `or3-12` | -6.48 | +8.43 | +1.95 | 0.23 | 50% | -7.49 / +8.35 |
| `arm3-12` | -5.75 | +7.78 | +2.03 | 0.26 | 49% | -6.57 / +7.64 |
| `or3-12 x w*` (size-matched, 0.735) | -4.71 | +6.31 | +1.60 | 0.25 | 50% | -5.44 / +6.24 |

The trims gain most in fast falls (+8.5 points per fall before costs, 114 falls): `e4` holds
less during a 1987 or 2020 than `tsmom12`, which is still fully in. In Sharpe terms this is
small (+0.022), because fast falls are 1% of the time.

## How sure

- The rules are pooled-1's own code. Per-market d of `e4`, `or3-12` and `arm3-12` reproduces
  pooled-1 exactly (worst 0.0). The regimes, the zigzag and the split are e4-anatomy-1's
  functions, unchanged. The component split is exact: tests check it adds up to the position
  gap and, with costs and compounding, to the return gap.
- The per-fall numbers leave out calm markets, where the trims cost most (-0.157 Sharpe).
  So K flatters `e4`. fast-reentry's premium counted calm spans; this table does not. That is
  why `e4`'s Sharpe lead (+0.063) is far smaller than its per-fall lead suggests.
- 491 falls on 41 markets overlap heavily in time (the markets share one crash calendar,
  pooled-1). They are not 491 independent cases. No test is made; the SEs are pooled-1's joint
  52-week block bootstrap (2,000 draws, seed 0), a description.
- Regimes are labelled with hindsight (the zigzag needs the later recovery). A rule cannot use
  them.
- The "signals" edge (+0.022 / +0.028) passes the card's rule and is beyond 2 paired SE. It is
  still small, from one sample whose markets fall together, and it does not change K much
  (0.31 against 0.25).
- The diagnostic sleeves (`e4-re`, `e4-trim`, `or3-12 x w`, `arm3-12 x w`, w in 0.25, 0.5,
  0.75, w*) are mechanism checks, not candidates. A later card that wants any of them as a
  rule must count these 10 configurations (note row in `tries.md`).

## The card's expectation, scored

- "No real conflict, K about equal": **wrong** by the card's letter. `e4` keeps far more per
  fall (K 1.53). The reason is its trims; its buy-back alone is like the old rules (0.31).
- "The lead over the 3-month rules is mostly the trims and lower volatility, not a better
  buy-back signal": **mostly right**. The trims carry most of it, but a smaller graded-buy-back
  edge passes the card's rule too.
- "(a) at most partly": **rejected**, weaker than expected. "(b) rejected": **right**.

## For the live rule and the summary

Nothing changes. `tsmom12` stays the rule. `e4` stays "unsettled, leaning positive". The
re-entry line stays closed: this lane re-opens nothing. The held-out year is unspent.

A suggested reading for `SUMMARY.md` (the lead decides): "`e4` does not fix the late buy-back
either: its buy-back part gives back about 70% of its rebound gain inside falls, like the
3-month rules. Its lead comes from also selling sooner (partial exits while `tsmom12` is still
in), which pays for the bear-market rallies it buys (#178)."

## Logged

`tries.md`: two `note` rows, as e4-anatomy-1 did. One is the re-score of three logged rules
(not a new try). The other lists the 10 diagnostic sleeves (not tries, not selectable). One
`ideas.md` line. Bar for scale (BAR.md): z >= 4.70, N 500. Not applicable: no test, no pick.
