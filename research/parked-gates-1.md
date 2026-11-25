# parked-gates-1: two parked candidates gated (W32 `drought-inflation`, W33 `margin-susceptibles`)

Research run parked-gates-1, 2026-11-25 (night run, WIDER lane). Branch `parked-gates-1` (from
`main`), PR #188 into `main`. Research only: fake money, keyless public data, no change to the
gym, the daily runner or the live strategies. Train only: nothing dated after 2025-10-31 is read.

Rules, data, placebo families, gates, power and guesses: [`cards/parked-gates-1.md`](cards/parked-gates-1.md),
pushed (55ae2bb, 00:51:17 UTC; the card says "about 00:55", a slip) before any number. Script
`research/lib/parkedgates1.py` (pure functions `research/lib/parkedgates1_events.py`, tests
`tests/test_parkedgates1.py`), pushed (28aafa3, 00:53 UTC) before its first run.

## Step 1. Which parked candidates, and why

Six candidates passed the #109 filters tonight without a gate. The card's table picks by score,
then data: **Y4 `drought-inflation`** (score 4; NOAA nClimDiv PDSI, one keyless static file,
monthly from 1895, posted about the 5th-10th of the next month) and **Y5 `margin-susceptibles`**
(score 4). The others are not gateable tonight with keyless data, or not worth it:

- **FINRA margin statistics** (Y5's scored source) answer this script with 403, the policy class
  of BLS and SEC in data-wide-1; a browser User-Agent was not used. Y5 is gated on a substitute:
  the Federal Reserve's Financial Accounts (Z.1) via FRED's keyless graph CSV, broker-dealer
  receivables due from customers (margin loans and other receivables) over all-sector corporate
  equities at market value, quarterly (annual before 1952), about 10 weeks after the quarter.
- **P12 `strike-idleness`**: BLS refuses scripts that do not put a contact e-mail in the
  User-Agent (data-wide-1); this public repo sends none. Not gateable keyless.
- **P3 `panic-words`**: about 2,000 loc.gov API calls plus a pre-1963 index; the next in line.
- **P4 `mass-casualty-mood`**: list terms unclear; P1's mood channel just died as W31.
- **Y3 `monsoon-gold`** (3): W13's dead channel; fails the flow-size check.

Overlap (re-checked in `ideas.md`, `gate-null.md`, `tries.md`): W32 reuses W19's crop-yield
channel at its inflation end on bonds, with a new dose (wide-17 scored "not killed" 0 for that);
no gate or strategy has used margin debt or broker receivables.

## Step 2. Dry run (counts only, 2026-11-25 about 01:10 UTC)

- **W32**: PDSI 1,570 months read, 1895-01 .. 2025-10 (none later). Gate dose months 2002-07 ..
  2025-06: TLT 276 rows (IEF and SPY 276, GLD 249, DBC 234). Placebos keep 191-276 rows (later
  doses past 2025-10 drop rows, as carded).
- **W33**: receivables and market value 302 quarters each, 1945-12 .. 2025-09 (none later). Z.1
  is **annual before 1952** (the first quarters 1946-1951 other than Q4 are empty), so the
  40-quarter baseline first exists in 1961-12 (256 quarters of s; 768 decision months).
  Gate months 1965-01 .. 2025-09: 729 rows, all with s. Placebos keep 660-729 rows; SPY 392
  rows.

**Deviation found in the dry run, fixed before the real run.** The card wrote the gate window
as 1965-01 on the assumption that Z.1 is quarterly from 1945, and said that "gate months start
where every placebo has a dose, so all 41 fits use the same rows". With s starting 1961-12, the
placebos at k up to 103 lack rows before 1970-10, so both cannot hold. The gate runs on the
card's stated window (1965-01 .. 2025-09), with placebos dropping their missing rows (the W29
and W32 convention), and **one shown cell is added now, before any return**: the same gate and
its own 40 placebos on months 1970-10 .. 2025-09, where all 41 fits use the same rows.
