# Wide 30: five mechanisms from accounting, household finance, gambling economics, bankruptcy law and asset management, the top one gated

Research run wide-30, 2026-11-26 (night run, WIDER lane, short slot 08:34-08:50 UTC). Branch
`wide-30` (from `main`), PR into `main`. Research only: fake money, keyless public data, no
change to the gym, the daily runner or the live strategies. Train only: no bar or event after
2025-10-31 is used.

Fields already mined are left out (the headers of `wide-1` .. `wide-29`; wide-27 lists them in
full, wide-28 and wide-29 added theirs). Not redone: `patent-surge`, `strike-idleness`,
`crackdown-shock`, `approval-mood`, `margin-leverage`, Yale ICF, ParlGov, NBER, BLS, W36-W46.

**New fields tonight**: accounting (payout policy), household finance (consumer credit),
gambling economics, bankruptcy law, asset management (fund flows).

**Count carried in** from `main` after wide-29 = **113 / 29 / 44**. Family bar with this run's
gate: p < 0.10 / 114 = 0.00088.

Method as wide-21 .. wide-29 (wide-11 filters F1/F2, wide-10 points, keyless data, a duplicate
check; `research/gate-null.md` gates with gate-null-2's "both families" rule adopted by the
card). `[memory]` marks a literature fact not checked tonight.

## Step 1. What the record already holds near these fields

Searched `research/` and `docs/` on 2026-11-26 for: payout, Lamont, lottery, jackpot,
bankruptcy filing, merger, FDIC (W26 `failure-premium` exists: bank regulation, not redone).
Shiller's file is read by long-macro, insure-3 and eu-6/7 for D/P and E/P; **no lane formed
D/E**. No lottery, consumer-credit, bankruptcy-filing or fund-flow mechanism found.

## Step 2. Five mechanisms, scored before any return was read

**Timing and disclosure.** The candidates were scored 08:35-08:37 UTC in the lane's working
notes; only the card (`cards/wide-30.md`, commit 50f0613, 08:37:18 UTC) was pushed before the
run, so only the card proves that the choice and the rule came before any number. This table
was written after the run. Before the card: a FRED request for Q2 (no connection from the
script; nothing read) and the cache listing.

| # | Mechanism (field) | F1 | F2 | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| Q1 `payout-ratio` | D/E high = earnings temporarily low, a premium (accounting; Lamont 1998 `[memory]`) | pass (b) | with controls | 1 | 2 | 0 (published) | 1 (monthly 1871-2023) | 1 | 1 | -1 | **5** | 5% |
| Q2 `card-credit` | revolving credit growth as stretched households (household finance) | pass (b) | with controls | 1 | 1 | 0 | 1 | 1 | 1 | -1 | 4 | **data blocked** (FRED: no connection from the script; latest vintage revised) |
| Q3 `jackpot-speculation` | big lottery jackpots pull retail gamble demand from lottery stocks (gambling economics) | pass (a) | pass | 1 | 1 | 0 | **0** at index level (lottery-type stocks only) | 1 | 1 | 0 | - | filtered (reach, no keyless jackpot history) |
| Q4 `bankruptcy-filings` | business filing waves as distress premium (bankruptcy law) | pass (b) | with controls | 1 | 1 | 0 | 0 (quarterly PDF tables, no script-readable monthly series) | 1 | 1 | -1 | - | filtered (data) |
| Q5 `fund-flows` | equity fund outflows as forced selling (asset management) | pass (b) | fail without strong controls (flows chase returns) | 1 | 1 | 0 | 0 (ICI monthly data under terms, not keyless) | 0 | 1 | -1 | - | filtered (data, F2) |

**Picked by the rule.** Q1 scores highest (5) and its data are cached (Shiller, 2026-11-12),
dated with four months of slack for interpolated, late-reported earnings. **Gated: Q1 as W47
`payout-ratio`**, replication **R47** fixed in the same card (rows 1932-01 .. 1989-12). No
second gate.

## Step 3. W47 `payout-ratio` gate

Rule, data, both placebo families, gate, R47, shown cells, power and guess:
[`cards/wide-30.md`](cards/wide-30.md), pushed before any number (50f0613, 08:37:18 UTC).
Code: `research/lib/wide30.py` (pure functions tested offline in `tests/test_wide30.py`; it
reuses wide-28's row builder by re-indexing the dose to m' = m + 3, so every window matches the
card). Results: `research/results/payout-ratio.md`.

### Dry run (counts only, 2026-11-26 08:38 UTC)

Shiller's E ends **2023-06** in the cached file, so D/E is defined 1871-01 .. 2023-06 and the
gate has **390 rows (1991-01 .. 2023-06)**, not the card's "402 if all are"; every shift
defined. **Lag-1 acf 0.990**: the surrogate family gates. |end - start| **1.02 SD**: above one
SD, so **IAAFT** surrogates, as the card says.

## What came out (one real run, 2026-11-26 08:38 UTC)

### W47 `payout-ratio`: fails (t +0.80; ranks 18 and 20 of 41). Dead.

**After a high payout ratio the US market earned slightly more, not clearly: b +2.44% over
twelve months per unit of the dose (+0.65% per SD, SD 0.268), t +0.80, 390 months 1991-2023;
t ranks 18 of 41 among earlier-dose calendars and 20 of 41 among IAAFT surrogates. R47 not
run.** Held-out data untouched.

| Cell (US Mkt-RF, % over months m+5 .. m+16, per unit of H; controls c12, c1, rv; NW 12, unless named) | b | t | Rows |
|---|---:|---:|---:|
| **Gate** | **+2.437** | **+0.80** | **390** |
| Horizon 3 months (NW 3) | +1.087 | +0.84 | 390 |
| Horizon 6 months (NW 6) | +1.399 | +0.59 | 390 |
| No controls | +2.150 | +0.65 | 390 |
| Without rv | +2.511 | +0.82 | 390 |
| Rows 1991-01 .. 2007-12 | +0.497 | +0.05 | 204 |
| Rows 2008-01 .. 2023-06 | +1.163 | +0.56 | 186 |
| Without rows 2008-07 .. 2010-06 | -3.641 | -0.62 | 366 |

- **What sign there is comes from 2008-09.** Dropping the two years when E nearly vanished
  and D/E spiked turns b negative (t -0.62). Neither half is near 2.
- **The nulls.** Earlier-dose calendars: SD 1.61, 23% past |t| 2, 5/50/95% -1.51 / +0.56 /
  +3.31, a wave across k (k 33-47 above +2.4, peak +3.47). IAAFT surrogates: SD 2.00, 25% past
  2, 5/50/95% -2.90 / +0.63 / +2.77. The true t sits in the middle of both.
- **Not run**: the card's "with ln(D/P) as a further control" cell (needs a fifth regressor
  the reused builder lacks; short slot). The verdict does not hang on it: the gate fails on
  t and on both ranks.
- **Dating.** Shiller's monthly E interpolates quarterly S&P earnings; the four-month slack is
  meant to cover it. Not material to a fail.
  An October row uses the December quarter, whose 10-K deadline (60 days) falls at the end of
  m+4; a 5-month lag would be safer.
- My guess (b positive, t +0.5 .. +2.5, middle-to-high ranks; pass 5%) matched.

Label: **fail** (gate-null: b > 0 holds, t < 2, ranks 18 and 20).

## Family count and status

One mechanism added and closed (W47 `payout-ratio`, failed). The four others are parked (Q2,
data blocked) or filtered and are **not counted**; each has a `note` row in `tries.md` and a
line in `ideas.md`.

**Count:** carried in from `main` = 113 / 29 / 44; **after W47 = 114 mechanisms, 29 tested by a
strategy, none passed, 45 gates, three kill-only passes (W32, W36, W45), each killed by its
replication.** Gate id W47 (R47 not run). Family bar p < 0.10 / 114 = 0.00088. Published
effects tested after publication: one more (Lamont's payout ratio; fails here on 1991-2023,
four years of overlap with his sample).

**Data terms.** Robert Shiller's online data (`ie_data.xls`, public on his site, cached
2026-11-12 by another lane); Ken French Data Library factors (cached 2026-11-12). Only
statistics are committed. Nothing downloaded tonight.

Rows logged in `tries.md`: 1 `screen` (W47), 7 `robustness` (shown cells), 4 `note` (one per
candidate scored but not gated).

## Next

1. **Do not redo W47** with other windows, doses or horizons: the gate failed, and the only
   sign comes from the 2008-09 earnings collapse.
2. **Q2 `card-credit`** stays parked: the script had no connection to FRED tonight; a later
   lane with FRED access (and ALFRED vintages for the revisions) could reopen it.
