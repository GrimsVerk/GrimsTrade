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

DRYRUN

RESULT
