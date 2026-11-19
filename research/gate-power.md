# Gate power: could the event-study gates have found a real effect?

Lane `gate-power`, 2026-11-19. Branch `gate-power` from `wide-13` (`9369ba3`). Method study,
not a try at any effect. **Card written and pushed before any simulation ran.**

## Question

The project has run 19 event-study gates (wide-6..wide-13, survey-7, weather-1;
`research/gate-null.md`). All 19 failed. review-2 (`research/reviews/review-2.md`, PR #119)
found that the backward placebo shifts overlap the outcome window, that the 40-placebo scale
cannot be stretched to p 1e-4, and that designs with about 10 independent episodes "can only
kill". This lane measures the other half: **power**. If a gate shape could only detect an
effect far larger than any plausible one, its kill says little and further gates of that shape
are wasted spend.

## What this lane logs

No selectable try. No strategy, no backtest, no held-out data. Every planted effect is a
synthetic control on top of real returns, never a candidate. `research/tries.md` rows are for
backtest variants (and `control`/`screen` rows for named controls of a backtest); this study runs
no backtest, so it adds **no rows**. The register count is unchanged.

## Gates studied (real dose series, each gate's own code path)

| Gate | Shape | Dose | Outcome | Statistic | Placebos as run |
|---|---|---|---|---|---|
| W25 `act-haven` (wide-13) | dense weekly index, persistent | z of weekly GPR acts, Mondays 2005..2025-10 | GLD+TLT pooled, 4-week log return from M+9 to M+37 | Driscoll-Kraay t, 4 lags, asset intercepts | k = +-27..103 weeks (40) |
| W26 `failure-premium` (wide-13) | sparse events (about two episodes) | ln(1 + FDIC failed assets), Fridays 2000..2025-10 | XLF 4-week return from F+3 to F+31, four past-return controls | Newey-West t, 4 lags | k = +-27..103 weeks (40) |
| W22 `hedging-pressure` (wide-11) | persistent weekly z, short sample (2018-2025) | CFTC hedging-pressure z (156-week window) | GLD/TLT/SPY/QQQ 4-week return | Driscoll-Kraay t, 4 lags | k = +-27..103 weeks (40) |
| weather-1 `hdd-gas` | seasonal, 18 winters | HDD surprise, 7 days to Friday | UNG 5-session return from Friday+4 | HC1 t | 40 winter derangements (season swaps) |
| W19 `enso-commodity` (wide-9, the older one) | slow monthly cycle, about 8 ENSO swings | lagged ONI | DBC 6-month return, monthly 2014-01..2025-04 | Newey-West t, 6 lags | 40 earlier whole-year shifts (k = 2..41) |

Each gate is rebuilt by importing its own loader and fit (`wide13.py`/`wide13_events.py`,
`wide11_hp.py`/`wide11_events.py`, `weather1_hdd.py`/`weather1_events.py`,
`wide9_enso.py`/`wide9_events.py`). Before any planting, the script reproduces each gate's
stored true t (to 0.05) as a check that the rebuild is the gate. Bars: train only
(`load_history("train")`, cut at 2025-11-10); doses cut where the gate cut them. Downloads are
read from the existing caches with `python -I`; nothing is fetched.

## Method: planted-effect simulation

For each gate, simulation s = 1..200 at effect size f:

1. **Noise from the real asset.** Build the gate's weekly (W19: monthly) real log return series
   R on the gate's own clock (W25 Mondays from M+9, W26 Fridays from F+3, ...). Move it against
   the dose calendar by a random circular offset (not within 52 weeks, W19 12 months, of zero;
   the same 200 offsets for every f, so the curves are smooth). Multi-asset gates rotate all
   assets by the same offset. weather-1 permutes whole winters instead (keeps the season and
   within-winter order). This kills any real dose-return link and keeps the asset's own vol,
   fat tails and autocorrelation, and the dose's own persistence.
2. **Plant.** R'(w) = R_rot(w) + f x sigma_w x x(w), where sigma_w is the asset's weekly
   (W19: monthly) return SD on the gate sample and x(w) is the position a trader acting on the
   gate's claim would hold in week w: the mean of the standardized doses whose outcome window
   covers week w (h = 4 for the 4-week gates, 1 for weather-1, 6 months for W19), re-scaled to
   unit SD. So f is the effect in units of the asset's vol per unit-SD position.
3. **Gate.** Recompute the gate's outcome y from R' (sum over the outcome window), its controls
   from R' (W26), and its statistic for the true dose and for each placebo, with the gate's own
   fit function.
4. **Pass rules.**
   - **Old rule** (as run): b > 0, t >= 2, and rank 1-2 of 41 among the gate's own placebos.
   - **Corrected rule** (review-2 point 5a): the same, but placebos are earlier doses only:
     k = +27, +31, ..., +183 weeks (40 shifts, all doses before the true one, none sharing its
     outcome window), whole-year shifts (W19, already so), or season swaps (weather-1, already
     so). For W19 and weather-1 the two rules coincide.
   - weather-1 also keeps its own extra condition (both halves > 0) in its old rule; shown
     both with and without it.
5. **Grid.** f in {0, 0.02, 0.04, 0.06, 0.08, 0.10, 0.15, 0.20, 0.30, 0.40}, 200 simulations
   each. f = 0 measures the false-pass rate (size) of each rule. Fixed seed per gate.

**Effect size scales.** A position x with unit SD on an asset with weekly SD sigma_w earns
an expected f x sigma_w a week for about sigma_w of weekly risk, so the timing rule's
standalone information ratio is **IR = f x sqrt(52)** (W19: f x sqrt(12) for monthly f). Reported per gate:

- **MDE80**: the smallest f with 80% detection (linear interpolation on the grid), as %/week per
  unit-SD position (f x sigma_w) and as standalone IR.
- **Added Sharpe over `tsmom12`** if the timing rule were added uncorrelated to it in the best
  mix: sqrt(1.05^2 + IR^2) - 1.05.

**Yardsticks.**

- The register bar (`research/register/BAR.md`, branch `register-5`; review-2 section 1):
  +0.30..+0.56 Sharpe over `tsmom12` for rules correlated 0.77-0.93 with it. An uncorrelated
  overlay needs a standalone IR of sqrt(1.35^2 - 1.05^2) = **0.85** (for +0.30) to
  sqrt(1.61^2 - 1.05^2) = **1.22** (for +0.56); review-2 gives "about +1.2" for an uncorrelated
  rule.
- Plausible effect sizes: published single-signal timing effects of the kind these gates borrow
  are typically IR 0.2-0.5 in sample; review-2 (section 4c) finds published effects kept a
  median of about 28% after publication, so a realistic live size is **IR 0.05-0.15**. A gate
  whose MDE80 is above IR 0.5 cannot see even the in-sample paper size.

## Effective episodes

For each gate the script prints the effective number of independent dose observations,
N_eff = N / (1 + 2 sum of the dose's autocorrelations up to the first non-positive lag), and for
W26 the count of failure clusters (failure weeks within 26 weeks joined). The verdict relates
MDE80 to N_eff and to the outcome horizon, to give a rule a future card can apply before it runs.

## Outputs

- `research/lib/gatepower.py` (simulation, pure functions, tested), one runner per gate
  family under `research/lib/gatepower_*.py`.
- `research/results/gate-power.md`: per gate, detection rate by f for both rules, MDE80, N_eff,
  size at f = 0.
- This file: the verdict and a proposed design rule (text for the lead to adopt into
  `gate-null.md`; this lane does not edit that file).

## Expected cost

Single process, numpy only, light (< 1 GB). About 10 x 200 x 81 regressions per gate.

## Verdict

(Filled in after the runs.)
