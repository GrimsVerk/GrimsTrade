# reentry-reconcile-1: why does `e4` gain in the year after the low when faster re-entry rules did not?

Lane `reentry-reconcile-1`, written 2026-11-25 **before any number of this card is computed**
(nothing below has been run on any series). Seen before: the published write-ups and tables of
e4-anatomy-1 (#168), pooled-1 (#142: D per group for `e4`, `or3-12`, `arm3-12`), fast-reentry
and fast-reentry-2 (#94, #96), bear-legs (#103), and the text of ownvol-anatomy-1 (#172, for
context only; none of its code is used). Research only: fake money, files already in the data
cache (read-only), no change to the gym, the daily runner or the live strategies. Train data
only: pooled-1's loaders stop at 2025-10-31; the held-out year is untouched.

## What this is (and is not)

A **descriptive reconciliation** of finished tries on their own series and code: no new rule,
`e4` not retuned, nothing selected. The re-entry rules are not re-opened (their line stays
closed). The diagnostic sleeves below are mechanism checks, labelled diagnostic: none is a
candidate, none is scored against the bar, and a later card that wants any of them as a rule
must count them (10 configurations, listed on the `tries.md` note row).

## The puzzle

- e4-anatomy-1: on pooled-1's 41 stock markets `e4` leads `tsmom12` by D = +0.063 Sharpe a
  market; by its card split (25% zigzag) the rebound year after a low gives +0.092, positive
  on all 39 markets with a 25% fall; the faster legs buy back earlier.
- fast-reentry / fast-reentry-2 / bear-legs (US French market + 10 industries since 1927, 13
  developed indices): `or3-12` and `arm3-12` win the rebound (+8 log points per US fall) but
  give most of it back inside the falls (-6 to -7), net +1.5 to +1.8, not shown; "early rallies
  look just like the bottom". pooled-1: on the same 41 markets they lead by +0.018 and +0.015,
  below the drift-only null of their extra exposure.

**Question: why do both hold?** Candidates (fixed now): (a) `e4`'s legs re-enter with only a
part of the slot, so false rallies cost less than an all-in re-entry; (b) sample: the earlier
tests were US (and developed) falls, `e4`'s gain is on 41 markets; (c) the definitions or the
metric differ (rebound window, gross rebound term against net of the fall, Sharpe against log
points); (d) the rules differ in exits or in the signals (`e4` also trims while `tsmom12` is
in; 1/3/6-month legs against one 3-month leg).

## Series and rules (unchanged)

- Series: `pooled1.load_all()` (41 equity markets: 10 US industries since 1927, 13 developed
  and 10 other indices, 8 ETFs), pooled-1's engine (`pooled1_core.decide`, `held`, `returns`:
  Friday decisions, fill one session late, 2 bps a side, cash 0, weekly Sharpe with sqrt 52).
  Group EQ-US10 is also shown alone: it is the closest to fast-reentry's US set.
- Logged rules re-scored: `tsmom12` (h12), `e4`, `or3-12`, `arm3-12`, positions straight from
  `pooled1_core.decide`. **Check (must hold, else stop and report):** per-market D of the three
  against `tsmom12` equals pooled-1's (`results/pooled-1.json`) to 1e-9.
- **Diagnostic sleeves** (positions built from the same decision series, held and costed by the
  same engine):
  - `e4-re` = h12 + (1 - h12) x e4: `e4`'s buy-back only (full while `tsmom12` is in);
  - `e4-trim` = h12 x e4: `e4`'s trims only (out whenever `tsmom12` is out);
  - `or3-12 x w`, `arm3-12 x w` = h12 + w x (h - h12) for w in {0.25, 0.5, 0.75}: the same
    re-entry at part size (w = 1 is the rule itself);
  - `or3-12 x w*`, `arm3-12 x w*`: size-matched, w* = (mean re-entry size of `e4-re`) / (mean
    re-entry size of the rule), each size the equal-weight mean over the 41 markets of the
    market's mean (1 - h12) x position over its scored weeks.

## Measures (all fixed now)

1. **Regime anatomy** of `e4`, `or3-12`, `arm3-12` against `tsmom12`, with e4-anatomy-1's code
   and definitions unchanged (`e4anatomy_core.fall_labels`, `whipsaw`, `parts`): d = return
   part + risk part, return part split by regime (fast crash, slow bear, rebound, whipsaw,
   calm). Readings: A (25% zigzag, primary), B (1.5 x the series' volatility), and the
   volatility-matched split (VA: against `tsmom12` scaled to the rule's own volatility, labels
   A), which e4-anatomy-1 added post hoc and this card fixes in advance. Mean position gap by
   regime.
2. **Component split.** Since h12 is 0 or 1, every rule's position gap splits exactly:
   h - h12 = (1 - h12) x h [**buy-back component**: held while `tsmom12` is out] + h12 x (h - 1)
   [**trim component**: held less while `tsmom12` is in]. The return part splits the same way
   before costs (daily component x market return, summed to weeks; cost and compounding residual
   reported apart). By regime, with each component's mean size. Efficiency of the buy-back
   component: its rebound term divided by minus its slow-bear term (gain per unit of
   bear-rally cost; undefined if the slow-bear term is >= 0, then reported as "no cost").
3. **Episode metric in the earlier lanes' units.** On every 25% / 25% zigzag fall of each
   market's traded level (daily, insure-1's zigzag as `e4anatomy_core.zigzag`; fall = (peak,
   trough], rebound = (trough, min(trough + 365 days, next peak)]), per rule: dI = log growth of
   the rule minus `tsmom12` over the fall, dB over the rebound, dN = dI + dB, in log points,
   net of costs. Equal weight per episode (no clustering: a description, not fast-reentry's
   test). Pool means over all episodes, per group, share with dN > 0. **Kept share K = mean dN
   / mean dB** (how much of the rebound gain survives the fall). Also by component in simple
   points before costs.
4. **Pooled D and paired SE** for every rule and diagnostic against `tsmom12`, and for the
   differences D(`e4`) - D(x) and D(`e4-re`) - D(x): pooled-1's joint circular block bootstrap
   (`pooled1_core.bootstrap`, 52-week blocks, 2,000 draws, seed 0), same draws for all.

## How each explanation is judged (fixed now)

First, **is there a conflict at all?** "No conflict" if on the 41 markets `e4` shows the same
shape as the 3-month rules in measure 3 (mean dB > 0 and mean dI < 0) **and** K(`e4`) <=
K(best 3-month rule) + 0.10; then e4-anatomy's rebound term is a gross gain like theirs and the
lead must come from elsewhere (risk part, calm, trims), which measures 1, 2 and 4 then locate.

- **(a) part size.** Return terms scale linearly in w, so size alone cannot change the ratio
  of rebound gain to bear-rally cost; only the risk part is non-linear. **Supported** if for
  both `or3-12` and `arm3-12` the best of the sleeves w in {0.25, 0.5, 0.75, w*} beats w = 1
  by >= 0.02 in D, **and** the size-matched w* sleeve comes within 0.02 of D(`e4-re`).
  **Partly** if only the first holds. **Rejected** otherwise.
- **(b) sample.** **Rejected** if on the 41 markets both 3-month rules show the earlier
  pattern (mean dB > 0, mean dI < 0, K <= 0.5) and D(`e4`) - D(rule) >= 0.02 for both.
  **Supported** if instead K > 0.5 for both on the 41 markets, or D(rule) is within 0.02 of
  D(`e4`), i.e. the earlier result does not carry over to this sample. Otherwise "mixed".
  EQ-US10 alone shown as the bridge (not judged; 10 series).
- **(c) definitions / metric.** The definitions are the same if the rebound window and the
  zigzag in measure 3 are those of e4-anatomy-1 and insure-1 (they are, by construction:
  checked by a test on a constructed path). **(c) carries** if "no conflict" holds above (the
  two lanes measure different things: a gross rebound term inside a Sharpe split against a net
  fall-plus-rebound sum). **Does not** if K(`e4`) > K(best 3-month rule) + 0.10.
- **(d) exits and signals.**
  - **Exit (trims) carries** if D(`e4-trim`) >= 0.5 x D(`e4`), or the trim component's
    return terms in falls (fast + slow, reading A) are larger than minus the buy-back
    component's slow-bear term (the trims pay for the bear rallies bought).
  - **Signals carry** if D(`e4-re`) exceeds both size-matched w* sleeves by >= 0.02 **and**
    the efficiency of `e4`'s buy-back component (measure 2) is higher than both 3-month
    rules'.
  - Otherwise "(d) does not carry".

Each verdict is printed with the paired SE of the differences it uses; a difference under 2
paired SE is reported as "within noise" next to the verdict (the verdict letter is kept). More
than one explanation can hold.

## Expectation, stated so it can be wrong

No real conflict: `e4` also gains in rebounds and loses in slow bears, and keeps about as much
of its rebound gain as the 3-month rules in log points (c). Its Sharpe lead over them comes
mostly from the trims and the lower volatility of part positions (risk part, d-exit), not from
a better buy-back signal. (a) at most partly (part size helps only through the risk part);
(b) rejected (pooled-1 already put the 3-month rules at +0.015 to +0.018 on the same 41).

## Output and rows

- `research/lib/reconcile_reentry.py` (runner) and `research/lib/reconcile_reentry_core.py`
  (numpy, no data access) write `results/reentry-reconcile-1.md` (+ `.json`). Tests
  `tests/test_reconcile_reentry.py` (offline, synthetic): components add up to the position gap
  and to the return part before costs, w = 1 sleeves equal the rule, episode windows match
  `e4anatomy_core.fall_labels` on a constructed path, dN = dI + dB.
- `tries.md`: one `note` row for the re-score of the three logged rules and one `note` row for
  the 10 diagnostic sleeves (not tries, not selectable). One `ideas.md` line. Bar for scale
  (BAR.md): z >= 4.70, N 500. Not applicable: no test, no pick.
