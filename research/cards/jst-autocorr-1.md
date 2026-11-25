# Card jst-autocorr-1: is insure-1870-1's timing result an artefact of smoothed early indices?

Lane `jst-autocorr-1`, written 2026-11-25 ~01:55 UTC, **before any number of this lane was
computed** and before the JST source documentation was read. Branch `jst-autocorr-1`. Research
only: fake money, keyless public data, no change to the gym, the daily runner or the live
strategies. Train data only (JST R6 ends 2020, Shiller's file is cut at 2025-10). Descriptive:
nothing is selected or tuned; one `note` row in `tries.md`.

## Question

insure-1870-1 (#186) found the annual trend rule's insurance "holds, narrowly on timing" on JST
R6, US 1873-1926 and 15 countries 1871-1965: share avoided S 0.73 (mean over anchored
clusters) against 0.51 at fixed exposure and 0.47 at random dates (p 0.020). Its caveat: the
lag-1 autocorrelation of annual log returns is 0.19 in that sample (0.04 after 1965; Norway
0.40, Germany 0.38, Portugal 0.36, Sweden 0.35, Belgium 0.32, US -0.06). If some early indices
are annual or December **averages** of prices, or stale/interpolated, measured returns are
positively autocorrelated (Working 1960: the first difference of non-overlapping averages of a
random walk has lag-1 autocorrelation that tends to 0.25), and a "last year beat bills" rule
then scores well on the *measured* index without any timing an investor could have had.
**Is S 0.73 explainable by smoothing alone?**

## What had been seen when this was written

insure-1870-1's write-up, card and results (all numbers above). Nothing else of this lane: no
source classification, no autocorrelation or S on any subsample, no simulation, no Shiller
comparison.

Expectation, stated so it can be wrong: the S gap (rule minus random) shrinks on documented
year-end country-periods but stays positive; an AR(1) of 0.19 inflates S by a few hundredths,
not by the full 0.26 gap.

## Data

- JST Macrohistory R6 (`eq_tr`, `bill_rate`, `cpi`), the copy cached by data-long-4, read-only,
  CC BY-NC-SA 4.0 (statistics only; cite Jorda, Schularick and Taylor 2017; Jorda, Knoll,
  Kuvshinov, Schularick and Taylor 2019). Sample and segments exactly as insure-1870-1's
  decisive sample (`insure1870.build(CONFIGS[0])`).
- Source documentation: the JST "Rate of Return on Everything" data appendix (per-country
  equity sources). Tried in this order, each fetched once, a block is recorded and never
  evaded: macrohistory.net documentation page and PDFs, the NBER w24112 PDF, the FRBSF working
  paper 2017-25 PDF, other public mirrors (journal supplementary data, RePEc listings).
- Independent US series: Shiller's monthly `ie_data.xls` (cached 2026-11-12; P = monthly
  average of daily closes, Cowles before 1926; D annual dividends spread monthly). Other keyless
  long annual or monthly national series (e.g. central-bank historical monetary statistics for
  Sweden or Norway) if they can be fetched keyless within the lane; skipped otherwise, and said
  so.

## (1) Classification

Each country-period of the decisive sample gets one label from the documentation text:
**year-end** (the source is stated to use end-of-year / December 31 / last-trading-day prices),
**averaged** (annual average, December average, average of monthly or high-low prices, or
interpolated), **unknown** (not stated, or the documentation could not be read). No label is
taken from the data. A year's label is the label of the country-period holding it.

## (2) Subsample comparison (description)

For each label group: lag-1 autocorrelation of annual log total returns (pairs of consecutive
scored years of one segment, both in the group; pooled Pearson after demeaning per segment),
and of log returns over bills; per-episode share avoided S of the rule, of fixed exposure and
the mean over the 1,000 rotations of insure-1870-1 (same seed), for episodes whose (peak,
trough] years all carry that label (mixed episodes reported apart). Also the per-episode S on
the whole decisive sample, so the groups compare with it rather than with the cluster mean.

## (3) Independent series

US 1872-1926 (and 1927-1965): lag-1 autocorrelation of Shiller December-to-December log total
returns, of Shiller annual-average-price returns (to show what averaging does), and of JST US,
same years. Same for any other keyless series found.

## (4) Simulation: S under smoothing alone

Same segments (lengths, actual bill series, 2 bps a side, the rule and episode code of
insure-1870-1, 25% zigzag). Per segment the measured log excess return over bills has the
segment's own mean and standard deviation, Gaussian.

- **A (AR(1)):** x_t = m + phi (x_{t-1} - m) + e_t with unconditional sd matched; phi in
  {0, 0.10, 0.19, 0.30} common to all segments, plus one run with each country's own observed
  phi from the decisive sample.
- **B (time averaging):** a monthly Gaussian random walk; the measured year value is the mean
  of the 12 month-end levels (lag-1 autocorrelation about 0.24), scaled so the measured sd
  matches; scored on the measured index (what JST would show) and, as a description, with the
  same signal scored against the true year-end returns.
- 1,000 simulated worlds per scenario, seed 0; per world: per-episode mean S of the rule, of
  fixed exposure, and the mean over 50 rotations (common offset, as insure-1870-1).

**Reading (fixed now).** Observed values: per-episode S of the rule and the gap rule minus
random on the actual decisive sample. "Smoothing could explain it" if the observed gap lies
below the 95th percentile of the phi = 0.19 scenario (A) **or** of scenario B; "smoothing alone
does not explain it" if it is above the 95th percentile of both. Reported next to the phi = 0
null (what insure-1870-1's rotation test assumes). For (2): "survives on year-end data" if the
year-end group's gap is at least half the full-sample gap; "gone on year-end data" if at or
below 0; in between otherwise; "not decidable" if the year-end group has fewer than 5 episodes.

## Bar and rows

Not a pick, no strategy try. The project bar (`register/BAR.md`, rows through 2026-11-25
00:50: 4,119 tries, N 1,115) is quoted for scale only. One `note` row in `tries.md`, idea
`jst-autocorr-1`; ideas.md gets one line.

## What each answer means

- **Smoothing could explain it:** insure-1870-1's timing evidence (p_S 0.020) should be read as
  "not distinguishable from an index-construction artefact"; the insurance-vs-exposure finding
  (premium order) needs its own check; the SUMMARY claim cites the early data for losing less,
  not for timing.
- **Not explained:** the early-data timing evidence stands, with the smoothing caveat reduced
  to the size measured here.
- No outcome changes the live rule.
