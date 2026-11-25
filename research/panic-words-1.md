# panic-words-1: W34 `panic-words` gated (wide-20's parked P3)

Research run panic-words-1, 2026-11-25 (night run, WIDER lane: linguistics and history). Branch
`panic-words-1` (from `main` aab87e6), PR #193 into `main`. Research only: keyless public data,
no change to the gym, the daily runner or the live strategies. Every month read is before 1965.

Rule, data, placebos and gate: [`cards/panic-words-1.md`](cards/panic-words-1.md), pushed
(68b64ce, 01:55:46 UTC; the card says "about 02:05", a slip) before any count of the word or any
return. Scripts `research/lib/fetch_panicwords1.py` and `research/lib/panicwords1.py` (pure
functions `research/lib/panicwords1_events.py`, tests `tests/test_panicwords1.py`), pushed
(bb8c2b2, 01:57:49 UTC) before their first run. Result file: `results/panic-words.md`; monthly
counts: `results/panic-words-counts.csv` (statistics of a CC-BY 4.0 dataset; cite Dell et al.
2023).

## Step 1. Overlap: not NVIX, not news-text-vol

Checked in `ideas.md`, `gate-null.md`, `tries.md`, `wide-15.md`, `wide-20.md`. Manela and
Moreira's NVIX (wide-15's X10 `news-text-vol`, filtered by F2) is a regression of VIX on Wall
Street Journal n-grams, fitted to option prices; P3 is a fixed one-word share in local papers,
never fitted to a price, with the opposite predicted sign (NVIX: higher later returns, a
disaster premium; P3: lower, a fear contagion). Distinct, so gated. Nearest literature: Garcia
(JF 2013), daily tone of New York Times columns; noted, not the same claim.

## Step 2. Data: loc.gov refused scripts; the same scans via American Stories

The loc.gov JSON API (Chronicling America's only interface since 2025) answered all six scripted
probes with HTTP 403 and a Cloudflare JavaScript challenge (`cf-mitigated: challenge`), with a
plain and a browser-like User-Agent, at under one request a minute. Its rate-limit page allows
20 a minute and warns of challenges under load. Not worked around (no browser, no solving).

Substitute: American Stories (Dell, Carlson, Bryan, Silcock, Arora, Shen, D'Amico-Wong, Le,
Querubin and Heldring 2023, arXiv 2308.12477; Hugging Face, CC-BY 4.0), article-level text re-OCRed from the same
public-domain scans, with the Library's publication date for each page. Measured download speed
(about 6 MB/s a stream) put 1880-1922 (about 230 GB) out of reach tonight, so the gate runs on
1925-1963 (about 34 GB, three streams, about an hour), where Ken French's daily US market gives
clean month-end total returns.

## Step 3. Dry run (counts only, 2026-11-25 02:42:36 UTC)

All 39 year files (1925-1963) downloaded and counted (`count` step, streamed, never extracted).
Articles a year run from 553,445 (1963) to 1,820,661 (1925), about 46,000-152,000 a month, from
43-94 titles a month; no month under the 2,000-article floor. Dose months 456
(1926-01 .. 1963-12); gate rows 438 (1927-07 .. 1963-12) as carded; placebos keep 353-431 rows;
common rows 353 (1934-08 on), as carded.

## What came out (one real run, 2026-11-25 02:42:40 UTC)

### W34 `panic-words`: fails its gate with the wrong sign. Dead.

**Gate (1927-07 .. 1963-12, 438 months): one unit more panic surprise (d, sd 0.256) goes with
+1.38% on the US market next month (+0.35% per sd; Newey-West t +1.19), with the dose month's
return, the past year's return and the dose month's realised volatility as controls. Predicted:
negative. Rank 37 of 41 (1 = most negative): fail on both conditions.**

Null width (40 earlier-dose calendars, k = 25-103 months, odd): placebo t SD 1.18, 10% with
|t| >= 2; 5/50/95% -2.03 / -0.10 / +1.47; extremes -2.80 (k 25) and +3.08 (k 39). Near normal,
slightly wide, centred (unlike W33's off-centre earlier-only family).

Shown cells (none gating), all positive or near zero, none near the predicted side:

| Cell | b (% per unit d) | t | rows |
|---|---:|---:|---:|
| (a) no controls | +1.28 | +1.04 | 438 |
| (b) "crash" dose, controls | +1.94 | +1.45 | 438 |
| (c) months m+1 .. m+3 | +0.14 | +0.06 | 438 |
| (d) common rows 1934-08 .. 1963-12 (own 40 placebos: rank 34 of 41, SD 1.18) | +1.10 | +1.06 | 353 |
| (e) 1927-07 .. 1945-12 | +2.99 | +1.21 | 222 |
| (e) 1946-01 .. 1963-12 | +0.19 | +0.21 | 216 |

(f) Feedback: d on the dose month's return, t -0.25; on the past year's, t -1.98 (more panic
words after a bad year, the F2 direction, weakly).

**Data check (descriptive, after the run).** The panic share is a sensible measure: median 8.8
articles per 10,000; the top months are 1933-03 (31.6, the bank holiday), 1932-10, 1929-11
(27.5; 1929-10 18.4), 1929-12 and the 1932 bank-failure months. It peaks in and just *after* the
falls, which is the F2 story the controls address; the month after a panic peak was, if
anything, better than average (the positive b), not worse.

**Reading.** Panic language in US newspapers 1927-1963 did not lead the market lower. If it
leads anything it is a rebound (the 1930s carry the positive sign: first half +2.99, second
half +0.19), which is the familiar reversal after crashes, not a narrative contagion. Kill-only
by design (about 6-10 episodes), so this fail kills the idea. **W34 `panic-words` is dead.**
Not run: 1880-1922 (230 GB of the same dataset, about 8 hours of download); a fail at the
gate needs no replication.

## Family count

From summary-6's count (#191, merged while this lane ran: 101 mechanisms, 29 tested by a
strategy, 28 gates; the card, written before the merge, quoted #191's earlier 101 / 28 / 28):
**102 mechanisms, 29 tested by a strategy, none passed; 29 gates, one kill-only pass (W32),
killed by its replication; every idea gated so far is dead.** Family bar for the next test: p < 0.10 / 102 = 0.00098. Parked candidates left:
P4 `mass-casualty-mood`, P12 `strike-idleness`, Y3 `monsoon-gold`.

## Cache left behind

`panic-words-1/americanstories/` (39 files, about 34 GB) and `panic-words-1/counts/` in the
shared data cache: kept so the counts can be rebuilt; safe to delete (the monthly counts are in
`results/panic-words-counts.csv`).
