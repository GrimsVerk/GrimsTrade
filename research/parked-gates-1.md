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

## Step 2. Dry run (counts only, 2026-11-25 about 01:02 UTC)

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

## What came out (one real run, 2026-11-25 01:06:13 UTC; R32 at 01:10:32 UTC)

### W32 `drought-inflation`: passes its kill-only gate, then fails its replication. Dead.

**Gate (2002-2025): one more PDSI unit of US drought goes with -0.78% on TLT over the next
quarter (months m+2..m+4; t -3.71, 276 dose months 2002-07 .. 2025-06), rank 1 of 41 shifted
calendars (empirical one-sided p 0.024). The first gate in this record to pass.** Kill-only by
design (about 6-10 drought episodes), so by `gate-null.md` step 7 it only said "not dead yet".

| Cut (TLT, months m+2..m+4, unless named) | b, % per PDSI unit | t | Rows |
|---|---:|---:|---:|
| **Gate: D = -PDSI** | **-0.784** | **-3.71** | 276 |
| IEF instead | -0.325 | -3.02 | 276 |
| GLD instead (predicted > 0) | -0.390 | -1.32 | 249 |
| DBC instead (predicted > 0) | +0.688 | +1.72 | 234 |
| SPY instead | +0.220 | +0.96 | 276 |
| 1-month horizon / 6-month horizon | -0.268 / -1.525 | -2.98 / -4.84 | 276 / 273 |
| Growing-season dose months only (May-Sep) | -0.462 | -1.35 | 115 |
| 3-month change of PDSI as dose | -0.155 | -0.60 | 276 |
| Reaction: TLT over month m+1 (release month) | -0.208 | -2.15 | 276 |

- **Null width: SD of placebo t 0.94, 0% with |t| >= 2**, quantiles 5/50/95% -1.37 / +0.08 /
  +1.71, extremes -1.76 / +1.95: narrower than W29's 1.47 for a persistent monthly dose.
- Already suspicious in the shown cells: the release-month cell has the same sign (the dose
  moves with bond prices at once, not only later), the change of drought (the news) shows
  nothing (t -0.60), the growing season (when drought hits crops) is weaker than the year, and
  gold has the wrong sign. That reads as "drier years coincided with falling bonds", not as a
  crop-to-inflation channel.

**Replication R32** (card `cards/parked-gates-1b.md`, pushed after the W32 result and before
any number of it; the card says "about 01:15", it was committed at 01:07:23 UTC, a slip): the
same dose on the 10-year yield over the 40 years before TLT, dose months 1962-01 .. 2002-03,
483 rows, no outcome month shared with W32.

| Cut (DGS10 change, end of m+1 to end of m+4) | b, bp per PDSI unit (food CPI: % per unit) | t | Rows |
|---|---:|---:|---:|
| **R32 gate: 1962-01 .. 2002-03** (predicted > 0) | **-0.32** | **-0.19** | 483 |
| Same design, 2002-07 .. 2025-06 (W32's years) | +4.36 | +3.01 | 276 |
| Same design, 1962-01 .. 2025-06 | +0.91 | +0.73 | 762 |
| Growing season, 1962-2002 | +1.84 | +0.76 | 200 |
| Reaction, month m+1, 1962-2002 | +0.11 | +0.18 | 483 |
| Mechanism: food CPI log change m+1..m+4, 1962-2025 (predicted > 0) | -0.045 | -1.68 | 761 |
| Mechanism: same, 1962-2002 | -0.063 | -1.82 | 483 |

- **R32 fails: rank 21 of 41** (p 0.51), placebo SD 1.19, 8% with |t| >= 2, quantiles -1.96 /
  -0.21 / +1.59, extremes -2.35 / +2.55. The yield version of the W32 design agrees with TLT on
  2002-2025 (t +3.01), so the outcome change is not the reason; the 40 earlier years, with
  droughts in 1963-64, 1976-77, 1980-81, 1988-89 and 1999-2002, show nothing.
- **The mechanism's first link is absent.** Drought does not predict higher food prices over the
  next quarter; the slope is slightly negative in both spans (t -1.68, -1.82).
- **Post hoc (descriptive, picked after W32): no single 2002-2025 episode carries W32.** Without
  2002-03, 2006-08, 2011-13 or 2020-23 the TLT slope stays at -0.65 .. -0.84 (t -3.12 .. -3.84);
  without the outcome windows touching the 2022 bond crash, -0.66 (t -3.34). The 2002-2025
  relation is broad within the period, which fits a slow common trend (drier decades, falling
  then rising bond prices) better than a shock channel; nothing here separates the two, and
  the replication is the test that decides.

Verdict, as the R32 card fixed it before the number: **dead, a one-period result.** No card for
a strategy. Held-out year untouched.

### W33 `margin-susceptibles`: fails. Dead.

**The interaction of this month's fall with the susceptible stock (broker margin and other
customer receivables over equity market value, detrended) has no slope on next month's S&P 500
return: b3 +0.017 (t +0.05, 729 months 1965-01 .. 2025-09), rank 41 of 41.** Dead by the gate.

| Cut (GSPC month m+1, b3 = F x s) | b3 | t | Rows |
|---|---:|---:|---:|
| **Gate, with controls** | **+0.017** | **+0.05** | 729 |
| Without controls | +0.074 | +0.23 | 729 |
| Binary trigger 1[r < -5%] x s | +0.021 | +0.83 | 729 |
| Stricter release lag (quarter end <= m - 6) | +0.134 | +0.35 | 729 |
| SPY instead (from 1993) | -0.130 | -0.17 | 380 |
| 1965-1994 / 1995-2025 | -0.308 / -0.159 | -0.71 / -0.21 | 360 / 369 |
| Main effects: b1 (F) / b2 (s) | +0.014 / -0.009 | +0.16 / -1.23 | 729 |
| Same rows for all 41 fits (1970-10 .. 2025-09, added after the dry run) | +0.001 | +0.00 | 660 (rank 41 of 41) |

- No cut comes near: the forced-selling cascade is not visible at monthly resolution with this
  proxy (70 months with a fall below -5% since 1965). The proxy is coarse (quarterly, includes
  non-margin receivables), and margin calls act within days, so the kill is of this monthly
  form, not of every margin story.
- **The null is not centred: all 40 earlier-dose placebo t are positive** (SD 0.58, 30% with
  |t| >= 2, quantiles +1.11 / +1.70 / +3.06, extremes +0.66 / +3.27; the same on the
  same-rows sample, SD 0.59). An s from 2-8 years earlier, interacted with this month's fall,
  leans positive everywhere; not explained tonight (a guess: the detrended ratio is high in old
  bull eras whose falls reversed). It does not touch the verdict: the true t is below 2 and
  below every placebo. It is a reminder that an earlier-only placebo family can be biased, so
  the rank, not the t against 0, is the reference (`gate-null.md` step 4).

Labels: W32, R32 and W33 are all **kill-only** (smallest p 1/41 = 0.024 each, above the family
bar 0.10 / 97 = 0.00103 and the register's 9.9e-5).

My guesses, written before the numbers: W32 "|t| < 1.5, pass 1%" was wrong (t -3.71, pass);
R32 "b positive but t below 2, pass 15%" was right on the verdict, wrong on the sign; W33 "|t| <
1.5, middle rank, placebo SD 1.0-1.3" was right on t, wrong on rank (last) and on the width
(0.58, off-centre).

## Family count and status

Two mechanisms added and closed: W32 `drought-inflation` (passed its kill-only gate, killed by
its replication R32) and W33 `margin-susceptibles` (failed). The four other parked candidates
(P3, P4, P12, Y3) stay parked, not counted.

**Count: 97 mechanisms (95 carried in from wide-20 + W32 + W33), 23 tested by a strategy, none
passed; 28 gates (25 + W32, W33 and the replication R32): one kill-only pass (W32), killed by
its own replication; every idea gated so far is dead.** Family bar for the next strategy test:
p < 0.10 / 97 = 0.00103, and the register's (3,982 tries, N 1,099, N_eff 504: z >= 4.70,
Bonferroni p <= 9.9e-5).

Rows logged in `tries.md`: 3 `screen` rows (`drought-inflation` W32, `drought-inflation` R32,
`margin-susceptibles` W33).

## Next

1. **The kill-only procedure did its job once.** W32 is the first gate pass in 28; the
   replication step 7 asks for killed it on an independent 40-year period, and its mechanism
   link (drought -> food prices) is absent. A future pass should get the same treatment
   (independent period or market, carded before the number) before anyone writes "lead".
2. **Persistent climate doses line up with slow bond and stock regimes** (W29 temperature,
   W32 drought): a 20-year sample of a monthly persistent dose has few independent swings
   even when the placebo null looks narrow (W32's placebo SD 0.94). For such doses a card
   could require the change of the dose (the news) to carry the effect too, or a second period,
   fixed before any number.
3. **Next parked candidate: P3 `panic-words`** (about 2,000 loc.gov calls, monthly 1880-1963).
   P12 `strike-idleness` needs a BLS route that does not ask for a contact e-mail; FINRA's
   margin page refuses scripts as well.
