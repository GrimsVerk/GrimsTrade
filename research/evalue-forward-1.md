# evalue-forward-1: does an anytime-valid sequential test let the forward record confirm an edge?

Lane `evalue-forward-1`, 2026-11-25 (UTC). Methods study, simulation only. Card:
[`cards/evalue-forward-1.md`](cards/evalue-forward-1.md) (pushed as `ad10934` before any
number). Script [`evalue1.py`](evalue1.py), full tables
[`results/evalue-forward-1.md`](results/evalue-forward-1.md) (45 s, numpy, deterministic; a
re-run gives identical bytes). Inputs: only the committed weekly returns store, train only,
cut at 2025-11-09. No backtest, no held-out year, no live record; no change to `src/` or the
forward registry.

## Answer (one screen)

- **No: a sequential e-value test does not change power-map-1's answer.** Where the test is
  valid (independent weekly differences, the Gaussian control), it reaches 80% rejection
  *later* than the fixed-horizon test, not sooner. For d +0.10 over `tsmom12` at rho 0.95 and
  the registry's alpha 0.025, the fixed test needs 78 years (simulated 77); the betting
  e-process (E1, ONS) has rejected in 3% of paths by 10 years, 11% by 20, 63% by 100 (median
  79 years). At power-map-1's alpha 0.05 the numbers are 62 years fixed against a median of 62
  sequential. Plausible edges (+0.05, +0.10) stay out of reach within 100 years at every rho.
- **Big edges stop earlier only on half the paths.** d +0.30 at rho 0.95, alpha 0.025: E1
  median 10.5 years, 80% by 16.1, against 9 years for the fixed test at 80% power. At the
  project bar (alpha 1.3e-6): median 36 years, 80% by 46, against 34 fixed. The usual rule of
  thumb holds here: the anytime-valid test's median stopping time is about the fixed test's
  80%-power horizon, and its 80% time is 1.3-1.8 times that horizon. Its gain is that the
  record may be looked at every week, not that it confirms sooner.
- **On the store's own dependence the e-processes are not valid.** Block-resampling the
  committed returns (52-week blocks, 163 donor series) keeps their serial dependence; the
  null "mean difference 0" then holds in the population but not week by week, and a test
  martingale needs the week-by-week (conditional) null. Result at nominal alpha 0.025 over
  100 years: E1 rejects 13.5-14.1% of null paths vs `tsmom12` (5.6 times the level) and 37%
  for `tsmom12` against zero; E2 (mixture SPRT) 4.0-4.5% and 11%. At the bar's 1.3e-6, E1
  rejected 3-12 null paths in 10,000 (about 230 to 900 times the level). With 1-week blocks
  (same fat tails, no dependence) every test keeps its level (E1 2.1%, E2 1.2%), so the cause
  is serial dependence, not fat tails: the difference series' 52-week variance ratio is median
  1.34 (p90 2.73), `tsmom12`'s own 3.3.
- **Side finding for the registry as it is:** its fixed-horizon verdict uses an iid standard
  error (PSR / t-test). On the same resampled null the t-test read once rejects 6.1-6.6% at 10
  years and 4.2-4.8% at 100 (nominal 2.5%), and 8% for a Sharpe-against-zero book at 10 years.
  The registry's `min_sample` and p-values are therefore optimistic by a factor of about 1.3-3
  in variance for trend-like books.
- **Weekly peeking at the fixed test is as bad as expected:** 59-63% false rejections by 100
  years at nominal 2.5% (43-45% even on iid Gaussian data). That is what the registry's
  read-once rule prevents, and it should keep it.

## Recommendation (for the lead; an engineering follow-up, nothing changed here)

1. **Do not adopt an e-process as the registry's verdict.** It cannot confirm a plausible edge
   (d <= +0.10) in useful time, it is no faster than the read-once test at 80% power, and on
   strategy returns with this much serial dependence its anytime guarantee does not hold
   (the card's adoption test failed on both counts: (a) false rejections 0.135 > 0.025, (b) no
   plausible edge reaches 80% within 20 years; the +0.30 median is 17% *later* than the fixed
   80% horizon on the valid Gaussian control).
2. **Fix the fixed-horizon verdict's standard error first** (cheap): a dependence-robust
   variance for `sharpe` and `mean` (Newey-West / Lo 2002 for the Sharpe ratio, or a block
   bootstrap with blocks of a year), and `min_sample` scaled by the train record's measured
   variance ratio. Without it the registry's alpha 0.025 is about 0.04-0.08 in practice.
3. **If continuous monitoring is wanted anyway** (a stop-early-for-harm or a large-edge alarm
   that is never the verdict): run the e-process on non-overlapping yearly (or at least
   quarterly) sums, not weekly differences, so the conditional-null assumption is closer to
   true. This lane did not validate that: with 52-week bootstrap blocks, yearly sums are
   independent by construction, so the simulation could not test it honestly.
4. power-map-1's recommendation 6 stands: the forward record is an implementation check and a
   description; it cannot rank books by edge within decades, sequentially or not.

## What was run (as the card fixed it)

- Statistic: weekly paired difference D = A - B, B = `tsmom12`, A scaled to B's volatility,
  in units of the train sd of D. Null: E[D | past] <= 0 each week.
- E1: one-sided betting e-process, ONS betting fraction in [0, 1/2] (Waudby-Smith and Ramdas
  2024; Shekhar and Ramdas 2023; Cutkosky and Orabona 2018), D clipped at 5 train sds.
  E2: one-sided half-normal mixture (tau 0.05 per week) of the self-normalised supermartingale
  exp(lambda S - lambda^2 V / 2) (Robbins 1970; de la Pena 1999). F: one-sided t-test read once
  at Y. P: the same t-test read every week. Reject when E >= 1/alpha (Ville's inequality;
  Ramdas, Grunwald, Vovk and Shafer 2023).
- Levels: 0.025 (the registry's per-rule alpha: forward data are fresh, so the train search's
  N does not apply; the per-family bar for a book registered alone), 0.05 (power-map-1's
  "registered alone" z 1.645), 1.3e-6 (BAR.md's z 4.70 at N 504).
- Scenarios: d in {0, +0.05, +0.10, +0.30}, rho in {0.77, 0.88, 0.95}; against zero S in
  {0, 0.5, 1.0}. 100 years of weekly steps; 10,000 paths per null cell, 2,000 otherwise; seed
  20261125. Fat tails: 52-week circular blocks of the primary `tsmom12` series paired with a
  donor's residual (163 C1 series with >= 20 years of overlap and rho 0.77-0.95; residual
  excess kurtosis median 17); Gaussian control iid normal.
- Added after the first results (section 5 of the results, not in the card): the same null
  with 1-week blocks, and the variance ratios, to tell fat tails from serial dependence.

## Selected numbers (alpha 0.025; full tables in the results file)

| Scenario | Fixed test: 80% years (formula / simulated) | E1 median years | E1 80% years | E1 share rejected by 20 y |
|---|---:|---:|---:|---:|
| Gaussian, rho 0.95, d +0.10 | 78 / 77 | 79 | >100 | 0.11 |
| Gaussian, rho 0.95, d +0.30 | 8.7 / 9 | 10.5 | 16.1 | 0.91 |
| Gaussian, rho 0.88, d +0.30 | 21 / 21 | 20.6 | 35.3 | 0.48 |
| Gaussian, rho 0.77, d +0.30 | 40 / 40 | 37.2 | 70.6 | 0.23 |
| Gaussian, own Sharpe 1.0 vs 0 | 7.8 / 9 | 9.9 | 14.9 | 0.93 |
| Resampled, rho 0.95, d +0.10 | 78 / 87 | 34 (invalid: null rejects 14%) | 97 | 0.32 |
| Resampled, rho 0.95, d +0.30 | 8.7 / 10 | 7.3 (invalid) | 11.5 | 0.96 |

Null, share ever rejected within 100 years at nominal 0.025: Gaussian E1 0.016-0.018, E2
0.011-0.013; resampled E1 0.135-0.141, E2 0.040-0.045, P 0.59-0.63; F read once at 10 years
0.061-0.066.

## Limits

- The block bootstrap treats the realised 1994-2025 path's year-to-year variation as noise
  around a zero mean. If part of it is a real, predictable regime, a test martingale on the
  conditional mean is the right null and the over-rejection is the test finding it; either way
  it is not evidence of an edge in the unconditional sense the bar asks about.
- Only two e-processes, each with one tuning (clip 5 sds, ONS; tau 0.05). Other betting rules
  (aGRAPA, mixtures over lambda) were not tried. A reason to expect no large gain: for an
  e-process tuned to the true edge, the time to reach 1/alpha is about 2 log(1/alpha) / snr^2,
  close to the fixed test's (z + 0.84)^2 / snr^2 (7.4 against 7.8 at alpha 0.025, 27 against
  31 at the bar), and a rule that must learn its bet pays extra.
- The mean-difference null equals the Sharpe-difference null only while the volatility ratio
  fixed at registration holds; volatility drift is not simulated.
- Donors are the store's C1 series (power-map-1's name rule); many are variants of a few
  families, so the 163 donors are fewer independent shapes than the count suggests.

Tries rows: one `note` row (`evalue-forward`), no selectable try.
