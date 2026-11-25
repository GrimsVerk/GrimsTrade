# Card stale-checks-1: are the pre-1926 insurance results artefacts of averaged or stale prices?

Lane `stale-checks-1`, written 2026-11-25 ~23:10 UTC, **before any outcome number of the three
checks was computed** (no autocorrelation of the two US monthly series, no rule position,
episode, share avoided or p-value of any run below; no return of the AQR commodity aggregate).
Branch `stale-checks-1`. Research only: fake money, keyless data, no change to the gym, the
daily runner or the live strategies. All data are before 1966 (train).

## Question

The project's insurance finding (`tsmom12` loses less than holding in large falls; its share
avoided beats random dates) was checked on early data by insure-1870-1 (#186, annual JST
1871-1965) and insure-1709-1 (#212, BoE monthly 1709-1866). jst-autocorr-1/2 (#192, #204) found
that the early data's lag-1 autocorrelation can explain the timing statistic. survey-9 (PR #216)
names three artefact checks. Each asks whether the timing result rests on how early prices were
recorded (averaged within the period, or stale), rather than on information a trader had.

## What had been seen when this was written

- The write-ups and code of insure-1, insure-2, insure-1870-1, insure-1709-1, jst-autocorr-1,
  jst-autocorr-2, survey-9 (branch `origin/survey-9`), data-wide-2 (and their published numbers,
  e.g. insure-1870-1's decisive S 0.73 / fixed 0.51 / random 0.47, p_S 0.020; insure-1709-1's
  month-older check S 0.67 unchanged).
- Schwert (1990, NBER WP 2985; PDF cached by survey-9 from www.nber.org, robots allows): text
  only. It says Cowles 1871-1925 uses the average of the month's high and low (lag-1 acf about
  .25), and that for March 1885 to December 1925 his spliced series uses Dow Jones *end-of-month*
  price changes plus the Cowles dividend yield. One appendix page (1851-1886 rows of his monthly
  index) was OCR-tested for legibility (values looked at for the 1851-1886 rows only; no return
  or statistic computed).
- AQR "Commodities for the Long Run" file (cached by data-wide-2): column headers and the first
  four rows (1877-02..1877-05) only.
- MeasuringWorth's DJA page: no robots.txt (HTTP 404); footer: "Copyright MeasuringWorth. All
  rights reserved. This work may be used for non-profit educational purposes if proper credit is
  given. For other permission, please Contact Us." Nothing on scripted download. **Unclear, so
  MeasuringWorth is not used** (task rule). The point series comes from Schwert's appendix.

## (a) Averaged against point prices, US 1885-1925

- **Averaged series:** Shiller's monthly file (`ie_data.xls`, cached; read with
  `jstautocorr.shiller_monthly`): price P (Cowles before 1926: monthly averages) and dividend D.
  Monthly total return r_t = (P_t + D_t / 12) / P_{t-1} - 1.
- **Point series:** Schwert (1990) appendix "Monthly Index of Common Stock Returns, 1802-1987",
  OCR of the cached PDF (pages for 1884-1926), chained index; returns 1885-03..1925-12 are Dow
  Jones end-of-month price changes plus the Cowles dividend yield. OCR validation before any
  statistic: every row 12 values; a second OCR at another resolution must agree digit for digit,
  disagreements read off the page image by eye; any month with |log return| > 0.15 or a +x/-x
  reversal pair is checked against the image. Cached under `~/data/grimstrade/stale-checks-1/`,
  never committed.
- **Window:** return months 1885-03..1925-12 on both (490 months; the 12-month signal needs the
  first 12, so scored months start 1886-03 at the latest). Identical months on both series.
- **Rule and statistic:** insure-1709-1's monthly machinery unchanged (`insure1709.build_seg`,
  `evaluate`): monthly `tsmom12` (`trend_where_long.signals`: hold next month if the 12-month log
  change > 0), cash at 0 when out (same for both series), 2 bp a side; falls of 25%+ on each
  series' own total-return index (insure-1 zigzag, 25% down / 25% up); I, S, premium; fixed
  exposure; 1,000 common rotations (p_rot); gap G = S_rule - mean S_rotations; Gaussian AR(1)
  null with the series' own lag-1 acf (1,000 worlds; p_AR1).
- **Runs:** A1 Shiller, A2 Schwert/DJ (both lag 0), A3 Shiller with the signal one month older
  (lag 1), A4 Schwert/DJ lag 1, A5 (secondary) Shiller's signal traded on Schwert/DJ returns and
  scored on DJ's falls (does a signal built from averaged prices time the point-sampled falls?).
- **Before scoring (descriptive):** lag-1 and lag-2 acf of monthly log returns of both series on
  the same months; Working (1960) expected lag-1 acf of changes of an m-point average of a random
  walk, rho(m) = (m^2 - 1) / (2 (2 m^2 + 1)) (m = 25 trading days: 0.249; limit 0.25); and, since
  Cowles averages the month's high and low, the lag-1 acf of changes of the monthly midrange of a
  25-step Gaussian random walk (simulated, 200,000 months).
- **Decisive number:** dG = G(A1) - G(A2).
  - dG >= +0.10: **averaging inflates the timing statistic** (measured directly on this pair).
  - |dG| < 0.05: **no measurable averaging effect on the 12-month timing statistic**.
  - otherwise: **small, not separable from noise on so few falls**.
  - Secondary: if |G(A3) - G(A2)| < 0.05, a one-month delay removes what averaging adds (as
    Working predicts for lag-1 dependence only).
- Caveats fixed now: the Dow Jones average is 12-20 price-weighted stocks, Cowles hundreds
  value-weighted, so any difference is averaging *plus* composition. US 1885-1925 likely has
  only about 4-6 falls of 25%+: the verdict machinery's "Too few falls" (n < 5) may apply; dG is
  read as a description either way, not as a test.
- **Guess:** Shiller lag-1 acf about +0.25, DJ about +0.05; dG small (+0.00 to +0.08), because a
  12-month signal uses little of a lag-1 dependence; reading "small / no measurable".

## (b) A one-year-older signal on insure-1870-1 (annual JST)

- **Data and sample:** insure-1870-1's decisive configuration unchanged (JST R6 equity total
  return and bills; US to 1926, others to 1965; 25% falls on the nominal index; cash at bills;
  2 bp; anchored clusters with the US anchors; 1,000 rotations, seed 0).
- **Rules:** L1 (insure-1870-1's rule): hold in year t if eq(t-1) > bill(t-1). L2 (one year
  older): hold in year t if eq(t-2) > bill(t-2). To score both on the same years, every segment
  drops its first scored year (L2 has no signal there); both L1 and L2 are run on these trimmed
  segments with `insure1870.run`'s scoring unchanged (episodes, I tests, fixed, rotations, p_S,
  p_P, verdict). L1 on the untrimmed segments must reproduce #186 (S 0.73, p_S 0.020).
- **AR(1) benchmark (descriptive):** per-episode mean S gap (rule minus rotations) of L2 in
  1,000 Gaussian AR(1) worlds with each country's own observed acf (jst-autocorr-1's `simulate`
  set-up, signal lagged one more year), and in random-walk worlds (phi 0); same for L1.
- **What each outcome means (fixed now):**
  - L2 keeps p_S < 0.05 and its I tests pass: **timing does not rest on the last year alone**;
    a lag-1 artefact (averaging or one-year staleness) cannot be the whole timing result.
  - L2 p_S >= 0.10 while L1 (trimmed) p_S < 0.05: **timing rests on the last year's return**.
    This is what lag-1 autocorrelation (artefact or real) predicts; it does *not* separate an
    artefact from genuine one-year persistence, because a year-old signal is also a much worse
    real-world signal (survey-9: "a failure would be hard to read").
  - Otherwise (0.05 <= p_S(L2) < 0.10, or L1 trimmed itself fails): **in between / not read**.
  - The I count is reported but not decisive: any exposure below 100% loses less in a fall.
  - If L2's per-episode gap is inside the AR(1)-own worlds' 5-95% band, the year-older timing is
    what the measured autocorrelation alone produces.
- **Guess:** L2 S about 0.55-0.60 against random about 0.47, p_S about 0.10-0.20: "rests on the
  last year" (weakly), I tests still pass.

## (c) One-month delay on AQR's 1877-1912 commodity aggregate

- **Record check:** no record in `tries.md` or SUMMARY runs a trend test on the AQR aggregate
  (grep AQR/commodity/1877: only data-wide-2's data note). So "the existing trend test" is the
  project's standard monthly insurance statistic, run here for the first time on this series,
  with and without the delay. Noted as a new try.
- **Data:** AQR "Commodities for the Long Run" index-level file (monthly, cached by data-wide-2,
  parsed with `datawide2.read_xlsx_rows`), column 1: excess return of the equal-weight commodity
  futures portfolio. Return months 1877-02..1912-12 (data-wide-2's new-years window). Early
  prices are, by HOP/survey-9, from CBOT reports, high-low averages early on [not checked in this
  file].
- **Rule:** monthly `tsmom12` on the excess-return index (insure-1709-1 machinery), out = 0 excess
  return (collateral), 2 bp a side. C0: lag 0. C1: signal one month older (execution delayed a
  month). Falls 25%/25% on the excess-return index; C0/C1 also at 20%/20% (check).
- **Statistic:** as in (a): I tests, S rule/fixed/random, gap G, p_rot, premium, AR(1)-own and
  block-bootstrap nulls for G (1,000 worlds each); Sharpe of rule and of holding (descriptive);
  before scoring: lag-1/lag-2 acf of the monthly log excess returns.
- **What each outcome means (fixed now):** with r = G(C1) / G(C0) (only if G(C0) > 0.05):
  - r >= 0.75: **the timing survives a one-month delay** (not a pure averaging artefact).
  - r < 0.50: **the timing rests largely on one-month dependence** (what averaging predicts).
  - in between: **partly**.
  - G(C0) <= 0.05: **no timing to test**; the delay check is moot.
  - Few falls expected (about 3-6): verdict words "Too few falls" may apply; r is descriptive.
- **Guess:** lag-1 acf clearly positive (+0.1 to +0.3); G(C0) about +0.15; r about 0.6-0.9.

## Not done here

No new full records, no new data source beyond the cached files and Schwert's appendix OCR, no
Yale ICF data, no data.nber.org, no MeasuringWorth. No change to `insure1709`/`insure1870`
behaviour (at most an optional argument with the old default). No gate ids are taken.
