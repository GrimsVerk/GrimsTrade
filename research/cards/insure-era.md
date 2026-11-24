# insure-era: is trend still cheaper insurance than holding less after 1962?

Lane insure-2, step 1, written 2026-11-18 22:58 UTC, **before any number of this step was
computed.** Branch `insure-2` (from `insure-1`). Research only: fake money, files already in the
data cache, no change to the gym, the daily runner or the live strategies. No new rule and no
new data: a per-era re-scoring of insure-1's card 2 (`cards/crash-insurance.md`). The held-out
year (2025-11-11 .. 2026-11-09) is not touched: nothing after 2025-10-31 is parsed.

## Why

insure-1 found that over 1927-2025 `tsmom12` buys loss avoided in 25% falls more cheaply than
holding less: premium 1.07 against 1.63 for a fixed 73% exposure and 1.82 for its own positions
rotated to random dates. But its own premium rose from 0.86 (1927-1961) to 1.38 (1962-2001) and
1.34 (2002-2025). The whole-period controls may be carried by the 1930s. The question that
matters for an investor today: **after 1962, is trend still cheaper than simply holding less?**

## What had been seen when this was written

- All of `results/insure-1.md` and `insure-1.md`: card 1 (episodes, clusters, premium by era
  with the gym splice: 0.86 / 1.38 / 1.34, T-bill 0.84 / 1.04 / 1.28) and card 2 over the whole
  span (rule S 0.50, P 1.07; fixed 73% S 0.29, P 1.63; rotations S 0.27, P 1.82; p 0.000 on
  both).
- The era split of the episodes by peak (138 / 72 / 60 episodes).
- Not computed: any control (fixed exposure, rotations) per era; the rule's paper-series premium
  per era; cluster counts per era.
- **Expectation, stated so it can be wrong:** after 1962 the rule still avoids a clearly larger
  share of each fall than random timing, and its premium is still below the fixed-exposure
  premium, but the gap is much narrower than over the whole span, and against the rotations the
  premium test may not reach p < 0.05 in one or both later eras.

## Data and series (all reused, nothing replayed)

- insure-1's primary set: French daily market and 10 value-weighted industries (cache snapshot
  2026-11-12), 1927-07-02 to 2025-10-31, loaded by `insure1.load_primary` (which reads
  trend-1926's saved gym runs; card 2 uses only the paper series built alongside).
- Episodes: card 1's 25% / 25% zigzag episodes, rebound windows, market-anchored clusters and
  calm mask, exactly as `insure1.score` and `insure1.market_anchored` build them.
- Rule: its paper series (as card 2, so rule and controls are built alike). Cash earns 0.

## Windows

| Window | Dates (calm counted on these dates) |
|---|---|
| 1927-1961 | 1927-07-02 .. 1961-12-31 |
| 1962-2001 | 1962-01-01 .. 2001-12-31 |
| 2002-2025 | 2002-01-01 .. 2025-10-31 |
| **1962-2025 (headline)** | 1962-01-01 .. 2025-10-31 |

- An episode belongs to the window that holds its peak (card 1's era rule); its `I` and `B`
  count there even when the rebound runs past the window's end.
- A market-anchored cluster belongs to the window that holds its first peak. Mean cluster `S`
  and `N` in a window are over those clusters.
- Premium in a window: `P = -(sum B + C) / sum I` over the window's episodes and the window's
  calm sessions (sessions outside every episode's `(peak, rebound end]`, as in card 1).

## Controls per window

- **Fixed exposure:** per series, `x` = the rule's mean paper position over the window's
  sessions (primary: exposure matched in that window); return `x * r`, no costs. Second reading:
  card 2's whole-span `x`.
- **Random timing (rotations within the window):** the rule's own paper positions on the
  sessions from the window's start to the later of its end and its last episode's rebound end,
  the whole 11-series block rotated together by one random offset `k` (circular within that
  span, `k` uniform in [365, n - 365] sessions), return `pos * r - 0.0002 * flips` (the wrap
  counts as a flip if it is one). Same exposure, spells and cross-series links in the window,
  timing broken. 1,000 rotations per window, seed 0 (one generator per window, fixed order).
  Sessions outside that span keep the rule's own positions (they enter no statistic of the
  window).

## Statistics and pass rule (fixed now, per window, same as card 2)

Mean cluster `S`, mean cluster `N`, pooled `P`, for the rule, the fixed exposure, and the
rotations (median, 5-95%), with p = share of rotations at least as good (S at least as large,
P at or below).

| Outcome | When |
|---|---|
| **Timing, not just exposure** | rule `S` above rotations with p < 0.05 **and** rule `P` below rotations with p < 0.05, **and** rule `P` below `P_fix` |
| **Exposure, not timing** | neither p below 0.10 |
| **In between** | otherwise |

- **Headline answer** ("still cheaper than holding less after 1962"): the 1962-2025 window's
  outcome. "Yes" needs "Timing, not just exposure" there; the two later eras are shown as
  detail. "Partly" for "In between"; "No" for "Exposure, not timing" **or** rule `P` at or above
  `P_fix` in 1962-2025.
- Four windows x two rotation tests = eight p-values; the write-up also says which survive
  Bonferroni at 0.05 / 8 = 0.006 (with 1,000 rotations the smallest reportable p is 0.001,
  shown as 0.000 = none of the 1,000).
- Few clusters per era: the write-up gives the cluster count of each window and does not run a
  sign test on fewer than 10 clusters.

## Bar and rows

- Not a pick: no rule is selected, so the bar for a new pick does not apply; quoted for scale.
  Base lane insure-1: no family bar (descriptive, kind `insure-check`). Project-wide (`git show
  origin/register-1:research/register/BAR.md`, rows through 2026-11-18 22:34): **2,904 tries,
  N 1,012 for a new pick, Bonferroni p <= 4.9e-5**; 1,000 rotations cannot reach it.
- No new `tries.md` rows: the controls and the per-era split are re-scorings of positions
  insure-1 already logged (card 2's rule), as insure-1 did for card 2.

## What each answer means

- **Yes:** trend's crash insurance is a real, cheaper-than-holding-less property in the modern
  era too; the rising premium is the price of insurance in general, not a decay of timing.
- **Partly / No:** after 1962 trend's insurance is closer to "hold less"; an investor who wants
  a smaller worst loss could get much of it by holding less, without a rule.
- No outcome changes the live rule tonight.
