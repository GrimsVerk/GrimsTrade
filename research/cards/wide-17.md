# wide-17: two premium gates from climate and epidemiology (W29 `temperature-premium`, W30 `outbreak-premium`)

Lane wide-17, written 2026-11-24 about 23:55 UTC, **before any return, slope or t of either
rule below was computed**. Candidates Y1 and Y2 of `research/wide-17.md` step 2 (both scored
6). Seen before this card: only the format probes disclosed in step 2 (GISTEMP header and 1880-
1881 rows; WHO DON's three oldest titles and the item count). Method: `research/gate-null.md`.
Script `research/lib/wide17.py` (pure functions in `research/lib/wide17_events.py`, tests in
`tests/test_wide17.py`), pushed before its first run. One dry run (`DRY=1`, counts only), then
one real run.

**Train cut.** Nothing dated after **2025-10-31** is read: price bars, temperature months and
outbreak reports alike (`LAST = 2025-10-31`; every exit bar must be on or before it).

## W29 `temperature-premium`

**Hypothesis.** A warm global-temperature shock is priced long-run risk: SPY earns more in the
months after it (predicted sign of b: positive).

**Data.** NASA GISTEMP v4, `GLB.Ts+dSST.csv` (global land-ocean anomaly, monthly from 1880,
keyless, public domain), one snapshot fetched 2026-11-24 into the shared cache
`wide-17/gistemp/2026-11-24/`. This is today's vintage: past months are revised slightly when
stations and methods change (typically a few hundredths of a degree `[memory]`); real-time
vintages are not used. Months after 2025-10 are never read.

**Dose.** A(m) = anomaly of month m (deg C). d(m) = mean of A over m-11..m minus mean of A over
m-131..m-12 (the last year against the ten years before it). NaN if any month is missing.

**Available on (no look-ahead).** GISTEMP posts month m around the 10th-15th of month m+1.
The outcome for dose month m is SPY's log return over calendar month m+2: from the close of the
last bar on or before the last day of m+1 to the close of the last bar on or before the last
day of m+2 (dividend-adjusted closes, `harness.load_history("train")`). The row is dropped if
either bar is missing, if the entry bar is not in month m+1 or the exit bar not in month m+2,
or if the exit bar is after 2025-10-31.

**Statistic.** OLS y = a + b d, one row a month, t of b with Newey-West (Bartlett) 3 lags over
the month index (`wide11_events.ols_dk` with one row per period: the same code path for every
cell). No controls (F2 passes outright).

**Placebo null (the decider).** Temperature does not answer stock prices, so shifts both ways
are allowed: d_k(m) = d(m - k months), k in +-{13, 17, 21, ..., 89} (step 4, never a multiple
of 12): **40 placebos**; a row with a missing d_k is dropped from that placebo only.

**Gate. Pass only if both hold** (outcome months 1993-02 .. 2025-10):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41.

**Kill-only.** d swings with ENSO and decadal variability: about 8-10 independent swings in 32
years. The smallest p this design can show is 1/41 = 0.024, above the family bar (0.0011) and
the register's (1.0e-4). A fail kills the idea; a pass only says "not dead yet".

**Shown (not gating).** QQQ, TLT, GLD instead of SPY; BTC and ETH pooled (asset intercepts,
Driscoll-Kraay 3 lags, from their first cached month); the 12-month horizon (exit at the end of
m+13, NW 12 lags); the monthly innovation A(m) - mean of A over m-120..m-1 as the dose;
outcome months 2013-01 .. 2025-10 (after the literature's samples); the reaction cell (SPY over
month m+1, the release month: the premium story predicts a negative slope there); the null's
width.

**Power, written before any number.** SPY's monthly sd is about 4.3%; if d's sd is about
0.08 deg C, with 393 months the standard error of b is about 4.3% / (0.08 x sqrt(393)), near
2.7% per deg C. t 2 needs b near 5.5% per deg C a month, about 0.45% a month per sd of d
(5% a year per sd): only a very large premium passes.

**My guess before any number.** b of either sign, |t| < 1.5, rank in the middle; placebo t sd
1.2-1.8 (a persistent dose with few swings). Chance of a pass: 1%.

## W30 `outbreak-premium`

**Hypothesis.** A burst of WHO outbreak reports raises the perceived chance of a pandemic, a
rare disaster; SPY earns a higher premium over the next 4 weeks (predicted sign of b: positive).

**Data.** WHO Disease Outbreak News API (`https://www.who.int/api/news/diseaseoutbreaknews`,
OData, keyless), fields `PublicationDate` and `Title`, every item, fetched 2026-11-24 into the
shared cache `wide-17/who-don/2026-11-24/` (untrusted download, read with `python -I`; only
counts are committed). Items dated after 2025-10-31 are never read. The API starts in 2004-01;
the 1996-2003 archive is not in it and is not used.

**Dose.** Weeks run Saturday F - 6 .. Friday F (UTC publication date). n(F) = reports in the
week; z(F) = 2 sqrt(n(F) + 3/8) (Anscombe); x(F) = z(F) minus the mean of z over the 52 weeks
F - 7 .. F - 364 (WHO's reporting volume drifts over the years). NaN without 52 earlier weeks
(first dose Friday 2005-01-07).

**Available on (no look-ahead).** Reports are public on their publication day. Entry at the
close of SPY's first bar dated >= F + 3 (the Monday after), exit at the close of the first bar
dated >= F + 31. y(F) = ln(exit / entry), dividend-adjusted closes. The row is dropped if a bar
is missing, the exit bar is dated after F + 38 or after 2025-10-31.

**Statistic.** OLS y = a + b x, one row a week, t of b with Newey-West 4 lags over the week
index (`ols_dk`, one row per week). No controls (F2 passes outright).

**Placebo null (the decider).** WHO reporting does not answer asset prices, so shifts both
ways are allowed: x_k(F) = x(F - 7k days), k in +-{27, 31, ..., 103} (`wide13_events.SHIFTS`,
the wide-11/13/15 family): **40 placebos**; rows with a missing x_k dropped from that placebo.

**Gate. Pass only if both hold** (Fridays 2005-01-07 .. 2025-09-26):
1. b > 0 with t >= 2.
2. The true t ranks among the 2 highest of 41.

**Kill-only.** Report bursts cluster in perhaps 10-20 outbreaks (H5N1 2004-2008, H1N1 2009,
MERS 2013-2015, Ebola 2014-2016, Zika 2016, and smaller ones); smallest p 1/41 = 0.024 >
0.0011.

**Shown (not gating).** QQQ, GLD, TLT instead of SPY; XLV (health care, Donadelli et al.'s
sector; signal-input ETF in the cache); BTC and ETH pooled (DK 4 lags); the raw Anscombe count
z instead of x; the 1-week horizon (exit at the first bar >= F + 10, 1 lag); Fridays from
2015-01-02 (after Donadelli et al.'s sample); with SPY's past 4/13/26/52-week returns as
controls; the reaction cell (SPY's return over the dose week itself, last bar <= F - 7 to last
bar <= F: the premium story predicts a negative slope); the null's width.

**Power, written before any number.** SPY's 4-week sd about 4.5%; about 1,080 weeks
overlapping by 3 (about 270 effective); if x's sd is about 1 unit, the standard error of b is
about 4.5% / sqrt(270), near 0.27% per unit. t 2 needs about 0.55% per 4 weeks per sd of
outbreak activity (7% a year): only a large premium passes.

**My guess before any number.** b near zero, |t| < 1.5, middle rank; placebo t sd 1.0-1.3
(a weekly count with little persistence once detrended). Chance of a pass: 0.5%.

## Both gates

**On a pass:** "not dead yet" only; no strategy card in this run. A design with more
independent episodes (temperature: other countries' markets and the 1926-1992 French data;
outbreaks: the pre-2004 archive and other markets) would be needed before any card.
**On a fail:** dead, one `screen` row each in `tries.md`, a line in `ideas.md`.

The count after this run (if both gates run): 90 mechanisms, 19 tested by a strategy, 24 gates.
