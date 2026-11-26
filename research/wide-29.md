# Wide 29: six mechanisms from corporate finance, astronautics, brokerage regulation, tourism, pharmaceutical regulation and numismatics, scored before any price, the top one gated

Research run wide-29, 2026-11-26 (night run, WIDER lane, short slot 08:12-08:40 UTC). Branch
`wide-29` (from `main`), PR into `main`. Research only: fake money, keyless public data, no
change to the gym, the daily runner or the live strategies. Train only: no bar or event after
2025-10-31 is used.

Fields already mined are left out (the headers of `wide-1` .. `wide-28`; wide-27 lists them in
full, wide-28 added criminology, public-opinion research, emergency management, road safety,
entrepreneurship, cinema, musicology, trade law, religion, education, geodesy, media studies
and forensic statistics). Not redone: `patent-surge`, `strike-idleness`, `crackdown-shock`,
`approval-mood` (parked or another lane's), W36-W45.

**New fields tonight**: corporate finance (the new-issue market), astronautics, brokerage
regulation (household margin leverage), tourism, pharmaceutical regulation, numismatics
(currency operations).

**Count carried in** from `main` after wide-28 = **112 / 29 / 43**. Project-wide bar (`research/register/BAR.md` after summary-11): N_eff
510, z >= 4.70 against `tsmom12`, Bonferroni p <= 9.8e-5. Family bar with this run's gate:
p < 0.10 / 113 = 0.00088.

Method as wide-21 .. wide-28 (wide-11 filters F1/F2, wide-10 points, keyless data, a size
check, a duplicate check; `research/gate-null.md` gates with gate-null-2's "both families"
rule adopted by the card). `[memory]` marks a literature fact not checked tonight.

## Step 1. What the record already holds near these fields

Searched `research/` and `docs/` on 2026-11-26 for: IPO, Ritter, equity share, equity
issuance, margin debt, FINRA, hash rate, reverse repo. Found: margin debt only as a parked data
item (data-wide-1, parked-gates-1, survey-8); hash rate screened (info-1, slow-1, wide-15);
reverse repo in the macro/liquidity cards. **No IPO-market, launch, tourism, drug-approval
or coin-production mechanism.**

## Step 2. Six mechanisms, scored (2026-11-26, 08:13-08:15 UTC, before any price was read)

**Timing.** The card (`cards/wide-29.md`, commit b4b0821, 08:16:21 UTC) names Q1; this table
was written after the card and pushed after the real run (git dates both), so only the card's
commit proves the choice came before any number. **Disclosure**: before the card, the Ritter
file's layout and its 1960 rows (see the card), and finra.org's robots.txt request, which
returned a Cloudflare block page to the script (no page fetched).

- **Q1 `ipo-heat`** (corporate finance). Firms go public when their stock is dear (Ritter 1991;
  Loughran-Ritter 1995; Baker-Wurgler 2000; Lowry 2003 `[memory]`): a hot IPO market means low
  market returns afterwards.
- **Q2 `launch-cadence`** (astronautics). Orbital launch counts and failures as a tech-optimism
  gauge.
- **Q3 `margin-leverage`** (brokerage regulation). Household margin debt growth as leverage
  that unwinds in falls.
- **Q4 `tourism-arrivals`** (tourism). International arrivals as discretionary demand.
- **Q5 `drug-approvals`** (pharmaceutical regulation). FDA novel-drug approval waves.
- **Q6 `coin-hoarding`** (numismatics). Mint coin production / cash demand as precautionary
  hoarding.

| # | F1 | F2 | Cause | Dose | Post | Power | Unseen | Not killed | F2 cost | Score | Prior |
|---:|---|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---:|---:|
| Q1 `ipo-heat` | pass (b): a state | with controls: issuers wait for rallies | 1 (market timing by insiders) | 2 (graded count) | 0 (published; a part of the Baker-Wurgler index) | 1 (monthly 1960-2025: 405 gate months, 288 earlier ones for a replication) | 1 | 1 | -1 | **5** | 5% |
| Q2 `launch-cadence` | pass (a) | pass | **0** (no channel to index returns) | 1 | - | 1 | 1 | - | 0 | - | filtered (cause) |
| Q3 `margin-leverage` | pass (b) | **fail** without strong controls: margin debt is a price times leverage | 1 | 2 | 0 (published) | 1 | 0 | 1 | -1 | 4 | **data blocked**: finra.org answers scripts with a Cloudflare block |
| Q4 `tourism-arrivals` | pass (b) | pass | 0 (a late, noisy trace of demand) | 1 | 0 | 0 (no keyless monthly history found) | 1 | 1 | 0 | - | filtered (data, cause) |
| Q5 `drug-approvals` | pass (a) | pass | 1 (sector cash flows) | 1 | 0 | **0** at index level (one sector) | 1 | 1 | 0 | - | filtered (reach) |
| Q6 `coin-hoarding` | pass (b) | with controls | 0 (coin output follows Fed orders, not households, month to month `[memory]`) | 1 | 0 | 0 (no script-readable monthly series) | 1 | 1 | -1 | - | filtered (cause, data) |

**Size check (shown, not part of the rule).** Q1: twelve-month excess returns have an SD near
16%; 405 overlapping months of a dose with acf near 0.99 hold perhaps 10-20 independent
stretches, so only about 5% a year per SD of the dose would show.

**Picked by the rule.** Q1 scores highest (5) and its data are keyless (a 43 KB xlsx, robots.txt
allows it), dated as the market saw them (IPOs are public on their day; the rule waits to the
end of m+1). **Gated: Q1 as W46 `ipo-heat`**, replication **R46** fixed in the same card (rows
1966-01 .. 1989-12, outcomes ending before the gate's first). No second gate.

## Step 3. W46 `ipo-heat` gate

Rule, data, both placebo families, gate, R46, shown cells, power and guess: [`cards/wide-29.md`](cards/wide-29.md),
pushed before any number (b4b0821, 08:16:21 UTC; the card's header time was then corrected
08:20 -> 08:15, no rule text changed). Code: `research/lib/wide29.py` (pure functions tested
offline in `tests/test_wide29.py`; stdlib xlsx reader, since the repo has no openpyxl).
Results: `research/results/ipo-heat.md`.

### Dry run (counts only, 2026-11-26 08:17 UTC)

The file runs to 2026-10; the first dry run showed this, and before the real run the IPO
months were cut at 2025-10 (the project's train window; the card's text names only the return
window). IPO months 1960-01 .. 2025-10 (790); dose defined 1965-12 .. 2025-10 (719, no gaps).
**Gate rows 405 (1991-01 .. 2024-09)**, every shift defined. **Lag-1 acf of the dose 0.995**:
the surrogate family gates. |end - start| 0.32 SD: **phase** surrogates, as the card says.

## What came out (one real run, 2026-11-26 08:17 UTC)

### W46 `ipo-heat`: fails (t -1.09; ranks 10 and 14 of 41). Dead.

**After a hot IPO market the US market did earn a little less, but not clearly: b -3.45% over
twelve months per unit of the dose (-3.06% per SD, SD 0.886), t -1.09, 405 months 1991-2024;
-t ranks 10 of 41 among earlier-dose calendars and 14 of 41 among phase surrogates. R46 not
run.** Held-out data untouched.

| Cell (US Mkt-RF, % over months m+2 .. m+13, per unit of H; controls c12, c1, rv; NW 12, unless named) | b | t | Rows |
|---|---:|---:|---:|
| **Gate** | **-3.451** | **-1.09** | **405** |
| Horizon 3 months (NW 3) | -0.790 | -0.79 | 405 |
| Horizon 6 months (NW 6) | -1.802 | -0.93 | 405 |
| No controls | -2.643 | -0.78 | 405 |
| Without rv | -3.556 | -1.21 | 405 |
| Dose from the first-day return (column C) | -0.320 | -1.86 | 81 |
| Rows 1991-01 .. 2007-12 | +0.066 | +0.01 | 204 |
| Rows 2008-01 .. 2024-09 | -9.802 | -3.08 | 201 |
| Without rows 1998-01 .. 2001-12 | -4.645 | -1.67 | 357 |

- **All of it is in the second half.** 1991-2007, with the dot-com IPO peak and bust, gives
  t +0.01; 2008-2024 gives -3.08 (one long stretch: few IPOs after 2008 and the 2009-2013
  rally, the 2020-21 burst and the 2022 fall). Dropping the dot-com years makes the full
  sample slightly stronger (-1.67), the reverse of the textbook story's best episode.
- **The nulls.** Earlier-dose calendars: SD 1.38, 17% past |t| 2, 5/50/95% -2.88 / -0.09 /
  +1.27, a wave across k (k 83-93 near -3). Phase surrogates: SD 1.58, 25% past 2, 5/50/95%
  -2.66 / -0.42 / +2.36. The true t sits inside both.
- **The first-day-return cell** has only 81 rows: column C is blank in months without
  qualifying IPOs, and the twelve-month mean needs every month. Shown, not read.
- **Dating.** The net count is Ritter's later screen (SPACs, units, penny stocks and more
  excluded, CRSP-listed only): the market saw each IPO on its day but not this exact count.
  Not material to the verdict (fail).
- My guess (b negative, t -2.5 .. -0.5, middle-to-high ranks; pass 5%) was right.

Label: **fail** (gate-null: b < 0 holds, t > -2, ranks 10 and 14).

## Family count and status

One mechanism added and closed (W46 `ipo-heat`, failed). The five others are parked (Q3, data
blocked) or filtered and are **not counted**; each has a `note` row in `tries.md` and a line
in `ideas.md`.

**Count:** carried in from `main` = 112 / 29 / 43; **after W46 = 113 mechanisms, 29 tested by a
strategy, none passed, 44 gates, three kill-only passes (W32, W36, W45), each killed by its
replication.** Gate id W46 (R46 not run). Family bar p < 0.10 / 113 = 0.00088. Published
effects tested after publication: one (the IPO-volume part of Baker-Wurgler sentiment; fails
here on 1991-2024).

**Data terms.** Jay Ritter's IPO data (University of Florida, public on his site), one xlsx of
43 KB downloaded 2026-11-26 08:15 UTC (sha256 in the card), cached outside the repo. Ken French
Data Library factors (cached 2026-11-12). Only statistics are committed. finra.org was not
fetched (Cloudflare block to scripts).

Rows logged in `tries.md`: 1 `screen` (W46), 8 `robustness` (shown cells), 5 `note` (one per
candidate scored but not gated).

## Next

1. **Do not redo W46** with other windows, doses or horizons: the gate failed, and the only
   strong cell (2008-2024) is one long stretch picked after the fact.
2. **Q3 `margin-leverage`** stays parked: FINRA blocks scripts; a browser download by the owner
   would reopen it, and it is published (low prior).
