# panic-words-1: W34 `panic-words` gate (wide-20's parked P3)

Lane panic-words-1, written 2026-11-25 about 02:05 UTC, **before any count of the word, any
return, slope or t below was computed**. Candidate P3 of `research/wide-20.md` step 2 (score 4,
parked for data). Method: `research/gate-null.md` (40 placebos, the rank decides, t >= 2 also
needed, kill-only label). Scripts: `research/lib/fetch_panicwords1.py` (raw bytes),
`research/lib/panicwords1.py` (counts and gate; pure functions in
`research/lib/panicwords1_events.py`, tests in `tests/test_panicwords1.py`), pushed before their
first run. One dry run (`DRY=1`, article and title counts only, no word counts), then one real
run.

**Train cut.** Nothing dated after 2025-10-31 is read; every dose and outcome month here is
before 1965.

## Overlap check (done first)

- **Not NVIX in disguise.** Manela and Moreira's NVIX (JFE 2017 `[memory]`) is a support-vector
  regression of VIX on Wall Street Journal front-page n-grams, fitted to option prices and then
  back-cast; wide-15 filtered it as `news-text-vol` (X10, F2: a transform of option prices).
  P3 is a fixed one-word dictionary share in local US newspapers, never fitted to any price, and
  it predicts the opposite sign (NVIX: high text uncertainty, *higher* later returns, a
  disaster-risk premium; P3: fear narrative spreads, *lower* next month). Distinct.
- Garcia (JF 2013 `[memory]`): New York Times financial columns 1905-2005, a word-list tone that
  predicts *daily* returns, reversed within days; wide-20 scored P3's post-sample point 0 for
  it. The monthly lead in local papers is a different claim but the same family; noted.
- No gate or strategy in `ideas.md`, `gate-null.md` or `tries.md` used newspaper word counts
  (W25 used a published geopolitical index: war words, not market words).

## Data (a substitute, and why)

**Planned source blocked.** The loc.gov JSON API (Chronicling America since 2025) answered all six
scripted probes on 2026-11-25 (01:49-01:52 UTC; collection search, general search, collections
list; browser-like and plain User-Agents) with HTTP 403 and `cf-mitigated: challenge` (a
Cloudflare JavaScript challenge). Not worked around: no browser, no challenge solving.

**Substitute.** American Stories (Dell et al. 2023, Hugging Face
`dell-research-harvard/AmericanStories`, CC-BY 4.0): article-level text re-OCRed from the same
public-domain Chronicling America scans, one `faro_<year>.tar.gz` a year, one JSON per page scan
with the Library's metadata (title, LCCN) and `edition.date` (the **publication date**; scans
were digitised decades later, and the digitisation date is never used). Fetched keyless into
the shared cache `panic-words-1/americanstories/`, never committed; only monthly counts are
written to the repo.

**Window.** 1880-1922 holds about 230 GB of these files (about 8 hours at the measured
8 MB/s), so the gate uses **1925-1963** (about 34 GB). That window also has a clean outcome: the
US market from Ken French's daily file (from 1926-07), compounded to calendar months, total
return, close to close. Before 1926 only Shiller's monthly *averages* exist, which leak the dose
month into the next month's return. Coverage after 1922 is thinner (fewer titles; the dry run
prints titles and articles per year).

## W34 `panic-words`

**Hypothesis** (wide-20 P3, narrative economics, Shiller 2019 `[memory]`). Fear narratives
spread like a contagion before they are acted on: when more of the press writes "panic", more
investors sell in the following weeks, so the US market earns less in the month after a rise in
panic language. Predicted sign of b: **negative**.

**Counts.** For each scan, publication month = `edition.date` (fallback: the date at the start of
the file name). Each entry of `full articles` with non-empty text is one article; its text is
headline + article, lower-cased, with line-end hyphens joined ("-\n" removed) and other line
breaks turned into spaces. N(m) = articles published in month m; n(m) = those matching
`\bpanic(?:s|ky|ked|king)?\b`. A month is valid if N(m) >= 2,000.

**Dose.** x(m) = ln((n(m) + 0.5) / N(m)); d(m) = x(m) minus the mean of x over months
m-12 .. m-1 (all 12 valid, else NaN): the surprise in panic language against its own past year
(OCR quality and the title mix drift over decades). "crash" is not in the primary dose: in this
era it is also a linen fabric in dry-goods ads and a road or air accident; it is a shown cell.

**Available on.** Papers published in month m are on the street in month m: d(m) is known at the
close of month m's last session.

**Outcome.** y(m) = ln of the compounded French US market total return (Mkt-RF + RF, daily file
`F-F_Research_Data_Factors_daily_CSV.zip`, cache snapshot `french/2026-11-12`) over calendar
month m+1 (close of m's last session to close of m+1's).

**Controls** (F2 passes only with controls: newspapers write "panic" after falls and in
turbulence). c1(m) = ln market return over month m (the dose month); c12(m) = ln return over
months m-12 .. m-1; v(m) = sqrt(sum of squared daily simple returns in month m).

**Statistic.** OLS y = a + b d + g1 c1 + g12 c12 + gv v, one row a dose month, t of b with
Newey-West (Bartlett) 3 lags over the month index (`wide11_events.ols_dk`, one row a period; the
same function for every cell). Gate dose months **1927-07 .. 1963-12** (c12 needs 12 French
months; about 438 rows).

**Placebo null (the decider).** The dose can answer prices, so earlier doses only (gate-null.md
step 1): d_k(m) = d(m - k), k = 25, 27, ..., 103 months (`parkedgates1_events.SHIFTS_W33`, odd,
never a multiple of 12, at least two years back so a placebo is not a lagged copy): **40
placebos**, controls and outcome unchanged. A row whose d_k is missing (before the dose starts,
1926-01) is dropped from that placebo only.

**Gate. Pass only if both hold:**
1. b < 0 with t <= -2.
2. The true t ranks among the 2 lowest of 41.

**Kill-only.** Panic language comes in a few episodes in 1927-1963 (1929, the bank panics of
1930-1933, 1937-1938, 1940, 1946, 1962 and smaller ones): about 6-10 independent episodes.
Smallest honest p 1/41 = 0.024, above the family bar (0.10 / 102 = 0.00098) and the register's
(Bonferroni over its N, about 1e-4). A fail kills the idea; a pass only says "not dead yet" and
needs a replication on other years (1880-1922 on Shiller-based outcomes with a one-month skip, or
other countries' papers) before any card.

**Shown (not gating).** (a) no controls; (b) "crash" (`\bcrash(?:es|ed|ing)?\b`) as the dose;
(c) the 3-month horizon (months m+1 .. m+3, NW 3 lags); (d) the gate and its own 40 placebos on
the common rows (dose months where every d_k exists, from 1934-08); (e) halves 1927-07 .. 1945-12
and 1946-01 .. 1963-12; (f) feedback: d(m) on c1(m) and c12(m) (F2's direction, descriptive);
(g) the null's width (SD, share |t| >= 2, 5/50/95%, extremes).

**Power, written before any number.** Monthly market sd about 6.5% in 1927-1963 (the 1930s
dominate); 438 rows; per sd of d the standard error of b is near 6.5% / sqrt(438) = 0.31%, so
t -2 needs about -0.6% a month per sd of panic surprise (about 7% a year): only a very large
effect passes.

**My guess before any number.** b of either sign, |t| < 1.5, middle rank; earlier-only null
possibly off-centre (W33). Chance of a pass: 2%.

## Disclosure (format probes before this card; no word count, return or statistic)

Six loc.gov JSON requests (all 403, challenge); the loc.gov rate-limit page (20 requests a
minute) and Chronicling America API page; the Hugging Face file listing (sizes by year) and
README of American Stories; the 1963 file downloaded once to measure speed and read one scan's
keys (`lccn`, `edition.date`, `full articles`, ...): an Evening Star page of 1963-12-15, 51,601
scans in the year. The fetch of 1925-1962 was started before this card (raw bytes only).

## Count

W34 enters the family as one mechanism and one gate: from #191's corrected count (101
mechanisms, 28 tested by a strategy, 28 gates; #191 open at writing, main's SUMMARY still says
95 / 23 / 25) to 102 mechanisms and 29 gates.
