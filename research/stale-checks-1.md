# stale-checks-1: are the pre-1926 insurance results artefacts of averaged or stale prices?

Lane `stale-checks-1`, 2026-11-25 (UTC). Branch `stale-checks-1`. Research only: fake money,
keyless data, no change to the gym, the daily runner or the live strategies. Card:
[`cards/stale-checks-1.md`](cards/stale-checks-1.md) (commit 2bcd92b, 22:55 UTC, before any
outcome number; its text says "~23:10", which is wrong). Tables:
[`results/stale-checks-1.md`](results/stale-checks-1.md). Code: `lib/stalechecks1.py` (reuses
`insure1709`, `insure1870`, `jstautocorr`, `datawide2` unchanged; `insure1870.run` gained an
optional `segs` argument with the old default), tests `tests/test_stalechecks1.py`.

The three checks are the ones survey-9 (PR #216) proposes for the early-data insurance results
(insure-1870-1 #186, insure-1709-1 #212) after jst-autocorr-1/2 (#192, #204) found that early
autocorrelation can explain the timing statistic.

## The answer on one screen

**Averaging is real and about as large as averaging predicts (Working 1960: mean 0.249,
high-low midrange 0.302), but it barely moves the 12-month timing statistic. The annual JST timing disappears with a year-older signal. The early
commodity timing partly survives a one-month delay.** No part turns the insurance count around:
the rule lost less than holding in every 25% fall in (a) and (c). What is at stake is only the
timing evidence (beating random dates), and that is weak on all three samples, as before.

| Part | What was compared | Key numbers | Card reading |
|---|---|---|---|
| (a) US 1885-1925, monthly | Shiller (Cowles monthly averages) against Schwert's (1990) Dow Jones composite, month-end closes | lag-1 acf **+0.250** against **+0.015** (Working: 0.249); timing gap G **+0.435** against **+0.380**, 4 falls each | dG +0.055: **small, not separable from noise** |
| (b) JST annual 1871-1965 | signal from year t-1 (as #186) against t-2, same years | S 0.72 against random 0.45 (p_S 0.010) → **0.37 against 0.44 (p_S 0.732)**; anchored falls lost less 9 of 9 → 5 of 9 | **timing rests on the last year's return** |
| (c) AQR commodities 1877-1912, monthly | signal at month end against a month later | lag-1 acf +0.116; G **+0.186** (p_rot 0.061) → **+0.121** (p_rot 0.167); 6 of 6 falls lost less either way (with the 1877-02 return restored: +0.185 → +0.119) | ratio 0.65 (0.64 restored): **partly** |

## (a) Averaged against point prices, US 1885-1925

- **Point series.** MeasuringWorth's daily Dow Jones file was **not used**: no robots.txt
  (HTTP 404), and its terms say only that the work "may be used for non-profit educational
  purposes if proper credit is given. For other permission, please Contact Us"; nothing on
  scripted download, so unclear, and the task rule says skip. data.nber.org (Dow Jones in the
  Macrohistory files) is disallowed by robots.txt. Instead: Schwert (1990, NBER WP 2985, PDF on
  www.nber.org, cached by survey-9), whose appendix index uses the *end-of-month* price changes
  of his Dow Jones composite plus the Cowles dividend yield for March 1885 to December 1925 (his
  text, section 6.4). The composite is not the 12/20-stock industrial average: for 1885-1896 it
  is Dow Jones' single average, dominated by railroads with a few industrials; from 1897 Schwert
  combines the railroad (transportation) and industrial averages, weighting each by its number
  of stocks (his description of the Dow Jones data, before equation 2). The card's description ("12-20 price-weighted stocks") was wrong.
- **Transcription.** The appendix is a scan with no text layer. `lib/stalechecks1_ocr.py`
  rebuilds it: PDF pages 50-51 rendered at 300, 400 and 500 dpi (the 500 dpi one thresholded at
  60%, digit whitelist), whole-page tesseract (--psm 6) at each, plus a per-cell OCR of the 400
  dpi page (two thresholds, --psm 7); a cell takes the most common reading and is flagged unless
  3+ readings agree, no second value has 2+ readings, and the move from the previous month is at
  most 12% in logs. All 64 flagged cells and the full rows 1897-1899 (74 cells) were read off
  the page image by eye; they are committed as `results/stale-checks-1-ocr-corrections.csv`
  (year, month, value) and override the vote. Rerunning the script reproduces the lane's file
  byte for byte. sha256: `w2985.pdf`
  a509de9dc4079d969cc19251cae41208c7d7b1e6f09b580c2c7d8e2c19f94842;
  `schwert-appendix-1884-1926.csv`
  4ea58998266120ecda4a983599eadbebf5441c775684230d9a783d2484cf3a78. The CSV is cached at
  `<cache_root>/stale-checks-1/`, not committed; `stalechecks1.py` stops with a rebuild hint
  when it is missing. Three moves above 15% or sharp reversals remain (1893-07 -20%, 1907-10
  -15%, 1915-04/05); all are known panics and were checked on the image. A wrong fourth or
  fifth digit would add only a tiny negative autocorrelation.
- **Averaged series.** Shiller's monthly price and dividend (`ie_data.xls`, cached), total return
  `(P_t + D_t/12)/P_{t-1} - 1`. Before 1926 Shiller's prices are Cowles', which average the
  month's high and low (Schwert 1990).
- Same months on both: levels 1885-02..1925-12 (487 months), returns 1885-03..1925-12 (485
  returns). August-November 1914 (exchange closed; Schwert has no values) are dropped from both,
  a **deviation from the card**, which said 490 months and did not plan for the closure. So
  each series has two segments, and the 12-month signal restarts after the reopening: its first
  signal is at the end of 1915-12, so the second segment is scored from 1916-01 on, and the
  return from July to December 1914 is not scored.

**Autocorrelation, before scoring.** Shiller's monthly returns have lag-1 acf **+0.250**, the
Dow Jones month-end series **+0.015** (483 pairs; noise line 0.075). Working's formula for a
25-point average of a random walk gives 0.249 (limit 0.25). A simulated monthly high-low
midrange, which is Cowles' construction, gives +0.302, and the last close 0.000. So on these
years the averaged index's lag-1 autocorrelation is about what averaging alone produces, and
the point-sampled index has none. Averaging also lowers the measured volatility (11.4% against
15.0% a year; the Dow is also a narrower, price-weighted index). The two series' monthly returns
correlate 0.70.

**Timing.**

| Run | Falls | Lost less | S rule / fixed / random (p_rot) | Gap G | AR(1) p |
|---|---:|---|---|---:|---:|
| A1 Shiller, averaged | 4 | 4 of 4 | 0.73 / 0.32 / 0.29 (0.000) | **+0.435** | 0.150 |
| A2 Dow Jones, month-end | 4 | 4 of 4 | 0.70 / 0.35 / 0.30 (0.000) | **+0.380** | 0.106 |
| A3 Shiller, signal a month older | 4 | 4 of 4 | 0.63 / 0.32 / 0.29 (0.000) | +0.329 | - |
| A4 Dow Jones, signal a month older | 4 | 4 of 4 | 0.68 / 0.35 / 0.31 (0.006) | +0.361 | - |
| A5 Shiller's signal traded on Dow Jones | 4 | 4 of 4 | 0.71 / 0.32 / 0.27 (0.000) | +0.417 | - |

- **dG = +0.055** (card: at least +0.10 would be "averaging inflates"; below 0.05 "no
  measurable effect"): **small, not separable from noise.** Averaging puts +0.25 into the lag-1
  acf, but a 12-month signal uses little of a one-month dependence, so it moves the share avoided
  by about a seventh of the gap.
- **The two series do not see the same falls.** Averaging smooths depth: on Shiller 1892-93 is a
  25% fall, on the Dow 36%; the Dow has a 25% fall in 1895-96 that Shiller does not; Shiller has
  a 28% fall in 1916-17 that stays below 25% on the Dow. Each G is scored on its own series'
  falls.
- **A month-older signal (description):** Shiller's gap drops to +0.329, a little *below* the
  Dow's +0.380 (secondary card criterion |G(A3) - G(A2)| < 0.05: 0.051, just missed). The delay
  costs Shiller 0.106 of gap and the Dow 0.019 (+0.380 to +0.361): on these numbers a one-month
  delay takes out what averaging adds, and a bit more.
- **A5 is the tradable question,** since an average up to month end is known at month end:
  Shiller's averaged signal timed the Dow's own falls as well as the Dow's signal did (+0.417
  against +0.380). Here averaging did not mislead a 12-month rule.
- **US 1885-1925 alone shows timing beyond random dates on point prices** (p_rot 0.000), but not
  beyond an AR(1) world with its own (near-zero) acf (p 0.106): with an acf of 0.015 the AR(1)
  worlds are nearly iid, and their median gap is already +0.16, from the fall definition alone
  (insure-1709-1 saw the same: iid +0.08). Four falls are too few for the verdict machinery
  ("Too few falls", sign p 0.0625).

## (b) A one-year-older signal on insure-1870-1 (annual JST)

insure-1870-1's decisive configuration, unchanged (16 countries, US to 1926, others to 1965,
25% falls, cash at bills, anchored clusters, 1,000 rotations); reproduced first: S 0.73, random
0.47, p_S 0.020, 9 of 9. Each segment then drops its first scored year so that both signals
are scored on the same years.

| Signal | Anchored falls lost less | S rule / fixed / random | p_S | Premium rule / fixed / random | Verdict (#186 rule) |
|---|---|---|---:|---|---|
| L1: year t-1 (as #186) | 9 of 9 | 0.72 / 0.51 / 0.45 | 0.010 | 1.14 / 2.21 / 3.03 | Holds |
| L2: year t-2 | **5 of 9** | **0.37** / 0.50 / 0.44 | **0.732** | 3.17 / 2.22 / 3.01 | Does not hold |

- **By the card: the timing rests on the last year's return.** With the year-older signal the
  rule avoids, on average, *less* of a fall than random dates and than the same exposure held
  fixed (5 of 9 anchored clusters still lost less than holding), and its insurance tests fail.
  The premium is worse than holding less.
- Per episode (jst-autocorr-1's statistic) against Gaussian AR(1) worlds with each country's own
  acf: L1's gap +0.309 sits at p 0.045 (median of the worlds +0.206), close to jst-autocorr-1's
  98th percentile on the untrimmed sample;
  L2's gap +0.091 is inside the AR(1) worlds' 5-95% band (-0.040 to +0.167; median +0.060,
  p 0.321) and in random-walk
  worlds at p 0.100 (median +0.004). The per-episode and anchored statistics differ in sign for
  L2 (+0.09 against -0.07), because anchoring averages episodes into clusters.
- **What this does and does not say.** It is what lag-1 autocorrelation predicts, artefact or
  not. It does **not** separate an artefact from real one-year persistence: on annual data a
  year-older signal is a much worse signal in any world. A pass would have been informative; a
  fail on annual data is weak evidence (survey-9 said so before this ran). It does say the
  annual timing result has nothing beyond the last year's information, so it is not robust to
  any one-year staleness.

## (c) One-month delay on AQR's 1877-1912 commodity aggregate

No earlier record ran a trend test on this series (grep of tries.md and SUMMARY: only
data-wide-2's data note), so the project's monthly insurance statistic was run on it here for
the first time, with and without the delay. AQR "Commodities for the Long Run", excess return of
the equal-weight commodity futures portfolio (cached by data-wide-2), level months 1877-02 to
1912-12; rule out = zero excess return. **Disclosure:** `datawide2.parse_aqr_comlr` chains the
returns from the first one, so the first level is 1877-02 and the first return used is 1877-03,
not 1877-02 as the card's window implies. The review reran with the 1877-02 return restored
(base level at 1877-01), and this lane reproduced it: G +0.185 (C0) and +0.119 (C1), p_rot 0.061
and 0.160, ratio 0.64, still "partly". The tables keep the run as committed.

- **Before scoring:** lag-1 acf +0.116 (noise line 0.079), lag-2 -0.081. That is positive but
  half of what full averaging gives (0.25-0.30): consistent with partly averaged early prices or
  with non-synchronous closes across commodities; the file does not say which (survey-9 quotes
  HOP: early CBOT prices are high-low averages `[not checked for this file]`).
- C0 (signal at month end): 6 of 6 falls lost less (sign p 0.016), S 0.62 against fixed 0.45
  and random 0.43, **G +0.186**, p_rot 0.061 ("In between"), AR(1) p 0.106, block bootstrap p
  0.071.
- C1 (a month's delay): 6 of 6 lost less, S 0.54, **G +0.121**, p_rot 0.167, AR(1) p 0.126,
  bootstrap p 0.146. Ratio G(C1)/G(C0) **0.65: partly**. Sharpe falls from 0.21 to 0.09 (holding
  0.17).
- At 20% falls the gap is small even without delay (+0.080, p_rot 0.203) and gone with it
  (+0.013).
- Reading: on this aggregate the insurance (losing less) survives the delay, but the timing
  evidence was never significant at p_rot 0.05, and a third of it goes with a one-month delay.
  The early commodity series does not add timing evidence to the project's claim.

## How sure

- **Card before numbers.** All three readings are the card's, thresholds unchanged. The (a)
  verdict sits near a threshold: dG +0.055 is 0.005 above "no measurable effect"; the secondary
  criterion misses by 0.001. Neither changes the plain reading: averaging moves the 12-month gap
  by about 0.05, against gaps of 0.3-0.4.
- **Few falls.** (a) has 4 falls per series, (c) 6, (b) 9 anchored clusters (about 7
  independent events). None of the timing gaps in (a) or (c) beats an autocorrelation-preserving
  null at 0.05.
- **(a) mixes averaging with composition:** Schwert's Dow Jones composite is a few dozen
  price-weighted stocks (railroad-dominated to 1896, then the railroad and industrial averages
  weighted by their number of stocks; not the 12/20-stock industrial average the card named),
  Cowles hundreds, value-weighted. The acf difference matches Working's number so closely that
  averaging is the plain reading of the acf; for the timing gap the two cannot be separated.
- **OCR.** The Dow series is a transcription of a scanned table, corrected by eye where the
  readings disagreed. Gross errors would show as spikes and reversals; none remain beyond three
  real panics. A transcription error in the 3rd-5th digit would not move any number here.
- Nothing here is a pick or a gate; no gate ids taken.

## What changes in the project's claim

- The pre-1926 *monthly* US timing is not an averaging artefact: on Dow Jones month-end prices
  the gap is about the same (+0.38 against +0.44), though not beyond an AR(1) null (p 0.106, 4
  falls), and a signal from averaged prices times the point-sampled falls as well. Averaging inflates the lag-1 acf by +0.25, which matters for
  short signals, not much for `tsmom12`.
- The *annual* JST timing (#186) has nothing beyond the last year's return: a year-older signal
  loses it entirely. Together with #192/#204 this keeps "timing before 1966 not shown".
- The insurance count (losing less than holding) is unaffected wherever it was tested here,
  except with the year-older annual signal.

## Files and data

- `research/lib/stalechecks1.py`, `research/lib/stalechecks1_ocr.py` (rebuilds the
  transcription), `research/results/stale-checks-1-ocr-corrections.csv` (74 eye-read cells),
  `tests/test_stalechecks1.py`, `research/results/stale-checks-1.md`, card, 15 rows in
  `research/tries.md` (11 runs, 4 notes).
- New local data: the Schwert appendix transcription (`<cache_root>/stale-checks-1/`, 12 kB;
  OCR images in the lane's scratch directory). No new download: the PDF is survey-9's cache.
  MeasuringWorth: robots.txt and the DJA page read only (2 requests), no data fetched.
- Cite: Schwert, G. W. (1990), "Indexes of U.S. Stock Prices from 1802 to 1987", Journal of
  Business 63(3) (NBER WP 2985); Shiller's online data; Levine, Ooi, Richardson and Sasseville
  (2018), "Commodities for the Long Run", FAJ 74(2); Jorda, Schularick and Taylor (2017), JST
  Macrohistory Database (CC BY-NC-SA 4.0); Working, H. (1960), Econometrica 28(4).
