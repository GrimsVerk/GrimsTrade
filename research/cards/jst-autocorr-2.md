# Card jst-autocorr-2: where does the autocorrelation of early JST annual equity returns come from?

Lane `jst-autocorr-2`, written 2026-11-25 ~21:15 UTC, **before the source documentation was
re-read for this lane and before any number of this lane was computed**. Branch
`jst-autocorr-2`. Research only: fake money, keyless public data already cached, no change to
the gym, the daily runner or the live strategies. Train data only (JST R6 ends 2020).
Descriptive: nothing is selected or tuned; `note` rows in `tries.md` only.

## Question

insure-1870-1 (#186) found the annual trend rule's timing evidence on JST R6 1871-1965
(p_S 0.020). jst-autocorr-1 (#192) showed that a lag-1 autocorrelation of about 0.17-0.19 alone
produces most of that gap, and that the two sources it could check (US = Shiller Dec-Dec; Norway
1921-1965 = Klovland, latest bid of December) are year-end. The origin of the autocorrelation is
open. **Per country and source period: is the price timing year-end, averaged, interpolated or
unknown, and is the autocorrelation concentrated in (a) averaged/interpolated segments, (b)
war / exchange-closure / hyperinflation years, or (c) thin-market segments?** Output: which
country-periods of JST annual equity data are usable for timing tests.

## What had been seen when this was written

jst-autocorr-1's write-up, card and tables: its per-source-period lag-1 acf (e.g. Norway Oslo
microdata 1881-1920 +0.60, Germany Eube 1890-1913 +0.43, Denmark yearbook 1901-1922 +0.42,
Portugal +0.36, Sweden +0.35, Belgium +0.32; US Shiller -0.06; pooled decisive sample +0.17
over bills), its source-period boundaries (`SOURCES` in `research/lib/jstautocorr.py`) and its
reading that the appendix "says nothing per country about year-end vs averaged prices". Not
seen: any classification by this card's rule, any flag split, any permutation, any lag-2 acf,
anything on 1966-2020 per source period. The source boundaries were seen together with their
acf; this lane keeps them only where the documentation confirms them, and says where it changes
one.

Expectation, stated so it can be wrong: most early sources are stated as year-end or not stated
at all; few are averaged; the high-acf periods are thin single-exchange microdata, so (c) will
carry more than (a); war years add noise but not the bulk.

## Data

- JST Macrohistory R6 (`eq_tr`, `eq_capgain`, `bill_rate`, `cpi`), the copy cached by
  data-long-4, read-only, CC BY-NC-SA 4.0 (statistics only; cite Jorda, Schularick and Taylor
  2017; Jorda, Knoll, Kuvshinov, Schularick and Taylor 2019).
- Source documentation, the copies jst-autocorr-1 fetched from macrohistory.net (no new fetch of
  that site): `RORE_documentation.pdf` (the QJE 2019 data appendix), `JST_RORE_Documentation_R6`,
  `JST_documentationR6`, and the NBER w24112 / FRBSF 2017-25 working papers. Cited original
  sources (e.g. Le Bris-Hautcoeur, Waldenstrom, Eube, Ronge, Buelens, Moore, Nyberg-Vaihekoski,
  Fujino-Akiyama, Eichholtz et al., Brailsford et al., Grossman) are read only if a keyless
  public copy is found quickly; one fetch per URL, a block is recorded and never evaded.
- No new market data are planned. If a keyless monthly series for one of the unverified
  high-acf periods turns up, it is compared like jst-autocorr-1 (3) and reported as a
  description.

## (1) Classification rule (fixed now)

Unit: a **source period** = country x the years one equity price source covers in the
documentation (equity price / capital-gain series; dividends are not classified). Each source
period gets three labels, taken only from documentation text, never from the data:

- **Price timing:** `year-end` (stated: end-of-year, 31 December, last trading day / last
  quotation / last bid of the year or of December); `Dec-average` (stated: average of December
  prices or of the last month); `annual-average` (stated: average of the year, of monthly
  prices, or of the year's high and low); `interpolated` (stated: years filled by interpolation,
  apportioning, or a return that spans a closure / non-calendar interval); `unknown` (not
  stated, or only the paper-wide convention applies). The paper-wide sentence ("compare
  end-of-year prices") does **not** make a source `year-end`: it gives `unknown (convention
  year-end)`. A stated fact in a cited original source counts if the documentation names that
  source for that period.
- **Thin market:** `thin` if the documentation states the index or sample has fewer than 30
  shares, is a hand-collected selection from one exchange's price lists / yearbooks, or that
  quotations are missing or infrequent; `broad` if it states 30 or more shares or an official
  all-share/broad index; `unknown` otherwise.
- **Disruption years** (year-level, not source-level): 1914-1918 and 1939-1945 for every
  country (world wars, most exchanges closed or controlled for some months), plus any exchange
  closure, civil war or interpolated years the documentation names, plus hyperinflation years
  (CPI up more than 50% in the year, the `hyper_years` rule of insure-1870-1). A lag-1 pair is
  `disrupted` if either of its two years is.

## (2) Statistic

- Returns: annual log equity total return over bills, `log(1+eq_tr) - log(1+bill_rate)` (the
  rule compares the two); log total return reported alongside.
- Main sample: insure-1870-1's decisive sample (`insure1870.build(CONFIGS[0])`: US to 1926,
  others to 1965). A lag-1 pair is two consecutive scored years of one segment **and** of one
  source period; demeaned per source period (within the segment). Lag-2 pairs likewise.
- Per source period (table): years, pairs, lag-1 acf, its rough one-sided 5% noise line
  1.645/sqrt(pairs), lag-2 acf, and the three labels. Also for the 1966-2020 sources, as the
  reference era.
- Per flag F (price timing in {Dec-average, annual-average, interpolated} = "averaged"; thin;
  disrupted; and the union of the three): pooled lag-1 acf of flagged pairs, of the rest, the
  difference, and a permutation p (10,000 draws, seed 0): for source-level flags, the flag is
  shuffled across the decisive sample's source periods keeping the count; for the year-level
  disruption flag, each segment's flag vector is circularly shifted by an independent random
  offset. One-sided: flagged acf higher.
- Working's check (description): with averaging, lag-1 near 0.25 and lag-2 near 0; with stale
  prices or a real AR(1), lag-2 near lag-1 squared and positive. Reported per group, not tested.

## What counts as "explained" (fixed now)

Full-sample pooled acf A0 (decisive sample, over bills, this card's pairing). For each flag F,
with A_rest the acf of the pairs it does not flag and n_rest their count:

- **F explains it:** A_rest <= 1.645/sqrt(n_rest) (the rest is not distinguishable from zero)
  **and** permutation p <= 0.05.
- **F partly explains it:** not the above, but A_rest <= A0/2 or permutation p <= 0.05.
- **Not explained by F:** otherwise.
- If the union of all three flags does not explain it, the remaining autocorrelation is
  reported as "in documented-unflagged data, origin open (real or undocumented)".
- If fewer than 50 pairs carry a flag, F is "not decidable" (reported, no reading).

## Usability per source period (fixed now)

- **Not usable for timing tests:** price timing averaged or interpolated (those years), and
  disruption years (drop them, splitting the segment).
- **Usable only with an autocorrelation-preserving null** (AR(1)-matched or block bootstrap,
  never a rotation / random-date null): any source period whose lag-1 acf is above its noise
  line, whatever its labels; and every `thin` or `unknown`-timing period.
- **Usable:** documented `year-end`, not `thin`, acf at or below its noise line.
- Any pooled timing test on JST annual data, usable rows or not, should use an
  autocorrelation-preserving null; the rotation null of insure-1870-1 assumes acf 0.

## Bar and rows

Not a pick, no strategy try. The project bar (`register/BAR.md`, rows through 2026-11-25 01:16:
4,126 distinct tries, N 1,116 for a new pick) is quoted for scale only. One `note` row per
reading in `tries.md`, idea `jst-autocorr-2` (classification, each flag split, the
recommendation); no Sharpe.

## What each answer means

- **Averaging explains it:** the early JST timing evidence is an index artefact on those
  periods; drop them from any timing test.
- **Thin / disruption explains it:** the autocorrelation is stale-price or crisis-driven, not
  tradable at the stated dates; drop or AR-null those periods.
- **Nothing explains it:** either real annual momentum in early markets or undocumented
  construction; JST timing tests then need an AR-preserving null throughout, and the early
  timing evidence of #186 stays "consistent with autocorrelation of unknown origin".
- No outcome changes the live rule.
