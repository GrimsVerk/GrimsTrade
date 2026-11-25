# pooled-2: do `e4` and `vt-own-70-x` beat `tsmom12` outside equities?

Lane `pooled-2`, written 2026-11-24 **before any number of this card is computed** (no rule has
been run on any series below in this lane; only spans were read, from `data-long-3.md`).
Research only: fake money, files already in the data cache (read-only), no change to the gym,
the daily runner or the live strategies. Train data only: nothing after 2025-10-31 is parsed
(`long_x.LAST`; the held-out year from 2025-11-11 is untouched).

## Question

pooled-1 (#142) left two of eight near-miss variants "open, leaning positive" on 41 stock
markets: `e4` (D +0.063, z 1.55) and `vt-own-70-x` (D +0.022, z 1.37). Its power stalled
because stock markets share one crash calendar. **On markets with their own calendars (US and
foreign government bonds, G10 currencies; commodities shown apart), is either variant better
than plain 12-month trend on the same series?** This is the out-of-sample test pooled-1 asked
for: the rules were chosen on the six live assets and pooled-1 looked at stocks; none of them
has been run on these series.

## Rules, frozen (pooled-1's code, `lib/pooled1_core.py`)

- `tsmom12` (twin): held (position 1) while the 365-day return > 0, else cash (0).
- `e4`: position = share of the 30/91/182/365-day returns that are > 0 (0, 1/4, .. 1).
- `vt-own-70-x`: the `tsmom12` sleeve x min(1, k / sigma), k solved over all sigmas seen so far
  for a mean share of 0.70 (`solve_k`), monthly reset, 24 sigmas at the target share before
  sizing starts, drifting share between resets, 5 bps on the traded notional at a reset.
- Long or flat, as frozen: no short positions (a currency is held only while it trends up
  against the dollar).

Weekly versions (daily data) call `pooled1_core` directly: `up`, `trailing_logret`, `held`,
`returns`, `weekly`, `fridays`, `solve_k`. Two changes, both for publication lags (point 3
below) and tested to reduce to pooled-1's code when the lag is zero: the signal at Friday F reads
the last session whose value was public by F (not the session of F), and own-vol's sigma skips
the most recent complete week. Monthly versions (frozen now, for monthly-only series):

- `tsmom12`: level after the last usable month / level 12 months earlier > 1.
- `e4`: share of the 1, 3, 6 and 12-month changes of that level that are > 0.
- `vt-own-70-x`: sigma = standard deviation (ddof 1) x sqrt(12) of the last 36 monthly `tsmom12`
  sleeve returns that are usable (the same gap as the signal), only months after the series'
  first scored month; reset every month; same k, target, warm-up count (24 sigmas) and reset
  cost as the weekly version; share drifts within the month as in `own_vol`.

## The eight points from data-long-3's "Ready for" list, settled

**1. Bar and comparator.** The twin is `tsmom12` on the same series and periods. Two rules are
tested; Bonferroni over 2 would be z >= 1.96, but **this card keeps pooled-1's z >= 2.50** so the
two lanes read on one scale and the combined reading (below) has one bar. The project bar
(`research/register/BAR.md`, rows through 2026-11-24 20:01: 3,855 distinct tries, N = 500
effective trials at measured rho 0.54, DSR 0.95 needs **z >= 4.70**, Bonferroni p <= 1.0e-4) is
the bar for "selectable candidate". Verdicts per variant, on the judged pool (point 8):

- **"Real small edge (outside equities)"**: z >= 2.50, AND D > 0 in at least 2 of the 3 judged
  groups (US bonds, foreign bonds, currencies), AND D > 0 on the periods before 1994-02-01
  (markets with at least 5 years scored there; outside the primary test's window, which holds TLT
  and GLD).
- **"Selectable candidate"**: the above with z >= 4.70. Even then nothing goes live from this lane
  (own card on the primary test, held-out year).
- **"Killed (outside equities)"**: the upper end of the 95% interval below +0.03, or z <= -2.50.
- **"Still open"**: neither.

**2. Frequency.** Weekly, pooled-1's engine, where daily data exist: US bonds (`DGS*`, H.15) and
the eight non-EUR currencies (H.10). Decisions each calendar Friday, fill at the close of the
next session, earning from the session after (pooled-1: one session late). Weekly Sharpe
(sqrt 52). Monthly elsewhere (foreign bonds, `FX-EUR`, commodities, gold), monthly Sharpe
(sqrt 12), with the frozen monthly rules above.

**3. Gaps for averages and publication.** Weekly: the signal at Friday F uses only sessions
whose `long_x.available()` date is on or before F: H.15 yields (`h15-daily`, next business day;
the signal reads Thursday's yield) and H.10 rates (`h10-daily`, the Monday after the week; the
signal reads the previous week). Own-vol's sigma skips the last complete week for the same
reason (a one-week-staler sigma). Monthly, the position over the return dated t (a month) uses
levels through the return dated t-1-g:

| Series | Kind | g | Why |
|---|---|---:|---|
| `GOV10-*` (OECD monthly-average long rates) | averaged | 1 | data-long-2's one-month gap: the return of month t is built from the averages of t-1 and t, so the signal stops at t-2; the average of a month is computable from that month's market yields at its end. OECD publishes about 2 months later (`oecd-monthly`, start of m+3): a strict-publication check with g = 3 is reported, not deciding. |
| `FX-EUR` (mark monthly average before 1999, month-end euro after) | averaged | 1 | as above, applied to the whole series |
| gold (datahub monthly, an average) | averaged | 1 | as above |
| PPI commodities (point price near the 13th) | ppi | 2 | the return of month t runs from the price of t-1 to that of t; the decision must precede the t-1 pricing day (about the 7th-13th); PPI of month m is public about the 17th of m+1 (`available("ppi")`), so the last usable level is m = t-3 |

Carry inside FX returns (foreign and US 3-month rates, monthly averages of the month before)
and the bill inside bond excess returns are part of the return earned, not of the signal's
information: a deposit or bill rate is known when it is struck. The OECD release lag of those
rates is a dataset lag. Check (reported, not deciding): FX signals on the spot-only index.

**4. Excess returns and cash.** Every rule is compared on returns in excess of the US bill, with
cash earning the bill (excess 0 when out), so the 5-15% bill rates of the 1970s-80s do not
dominate any Sharpe. Signals are read from the same excess-return level (as time-series momentum
is usually defined). US bonds: daily rebuilt total return (`long_x.bond_returns`) minus `DTB3`
(last value on or before the start of each step, calendar days / 365). Foreign bonds: the
panel's local excess over the local 3-month rate (a hedged return). Currencies: the panel's
carry-inclusive return, funded at the US 3-month rate (daily: spot change x (1 + i_f x days /
36,500) / (1 + i_us x days / 36,500), rates of the month before the step's end, as the monthly
panel). Commodities and gold: spot price change, cash 0 (no bill subtracted: spot has no
collateral; a futures position's excess return would be spot plus roll yield, unknown here).

**5. Which series count (29; no nested or duplicate series).**

| Group | Series | Data | Freq | Span (first; last 2025-10) |
|---|---|---|---|---|
| USB3 | UST2, UST10, UST30 (UST5 sits between: left out) | ALFRED `DGS2/10/30` daily, excess over `DTB3` | weekly | 1976-06, 1962-01, 1977-02 (the tail after the last gap over 14 days) |
| GOV9 | GOV10 JP, GB, CH, CA, DE, AU, NZ, SE, NO | `panel()`, averaged | monthly | 1955-02 (CA) .. 1989-02 (JP) |
| FX9 | JPY, GBP, CHF, CAD, AUD, NZD, SEK, NOK (daily H.10) and EUR (`panel()`, monthly) | carry-inclusive excess | weekly (8), monthly (EUR) | from 1973-03-01 (floating) or the first month both rates exist |
| COM8 (shown, not judged) | PPI grains, livestock, coal, natgas, crude, steel, primary nonferrous; gold (datahub, from 1971-01) | spot | monthly | 1913/1926/1947/1967 on; gold 1971 |

Left out: UST5, UST10-avg (duplicates of UST10), UST20 (gap 1987-1993), PPI all / farm / metals /
nonferrous / wheat (aggregates of included ones), WTI-avg (same oil as PPI crude). Judged pool =
USB3 + GOV9 + FX9 = **21 markets**.

**6. Correlation.** Joint circular block bootstrap on one monthly calendar (all markets): each
weekly market's weeks go to the month of their Friday, and the per-month sums (count, sum, sum of
squares) of each rule's returns are the units; blocks of **12 months**, the same draw for every
market (this keeps the within-class factors, the dollar and world rates, and the cross-class
calendar). Each market's Sharpes are recomputed on its own periods in the draw (at least one
year of periods), D recomputed. 2,000 draws, seed 0; SE = standard deviation of the draws;
z = D / SE; 95% interval D +- 1.96 SE (percentile shown). Checks, not deciding: blocks of 3 and
24 months. Sets reported: judged pool (21), each group, COM8 alone, all 29, and the combined
sets below.

**7. Costs.** Per side, share of the position changed: bonds **2 bps**, currencies **3 bps**,
commodities and gold **10 bps**. Own-vol reset: 5 bps (frozen), 10 bps on commodities. Check
(reported, not deciding): every cost doubled.

**8. What a pass means.** The verdict is on the judged pool, bonds + currencies (21). Commodities
are spot prices (not investable: spot oil beat a front-month fund by 10 points a year) and are
shown separately as "does the price trend", not as an earnable edge. Carry is an upper estimate
(about 1 point a year richer than the trusts); it moves both rules alike, the difference little.
A pass says "the variant's edge over `tsmom12` exists outside equities on rebuilt bond and
currency returns", not that the paper book could earn it; the held-out year stays unspent and
nothing goes live from this lane.

## Combined reading with pooled-1 (pre-stated)

pooled-1's 41 equity markets are re-run with pooled-1's code unchanged (`pooled1.load_all`,
`pooled1_core.run_market`, 2 bps, weekly) and put on the same monthly calendar; its point D must
equal pooled-1's published D (check: `e4` +0.063, `vt-own-70-x` +0.022).

- **Combined pool**: equal-weight mean of d over 41 equity + 21 judged = **62 markets**, SE from
  the same joint bootstrap (one calendar, 1927-2025). Also shown: the class-balanced mean
  (D_equity + D_nonequity) / 2 with its bootstrap SE (not deciding).
- Readings, in order:
  1. **"Real small edge across asset classes"**: combined z >= 2.50, AND D > 0 in both pools,
     AND combined D > 0 before 1994. With z >= 4.70: "selectable candidate" (still own card).
  2. **"Equity-only at best"**: the non-equity verdict is "killed".
  3. **"Lean not confirmed"**: non-equity D <= 0 (not killed): pooled-1's lean is downgraded to
     "no evidence".
  4. **"Unsettled, leaning positive"**: non-equity D > 0 but reading 1 not met.
- Pre-stated expectation of power (not a result): if the non-equity SE is about 0.04 and the two
  pools' differences are uncorrelated, the combined SE is about 0.03 for `e4`; an `e4` edge of
  +0.063 everywhere would then give z about 2.1. **The combined test reaches 2.50 for `e4` only if
  the non-equity edge is clearly larger than the equity one.** Likely outcome by construction:
  readings 3 or 4.

## Power (before the numbers)

Prior single-market paired SE for a close rule: about 0.08 over 35 years (pooled-1's card),
about 0.067 over the judged pool's average of roughly 50 years. SE(D) = 0.067 x sqrt((1 + 20 rho)
/ 21):

| rho of d between markets | SE of D | Edge found 80% of the time at z 2.50 | at z 4.70 |
|---:|---:|---:|---:|
| 0 | 0.015 | +0.05 | +0.08 |
| 0.1 | 0.025 | +0.08 | +0.14 |
| 0.3 | 0.039 | +0.13 | +0.22 |
| 0.5 | 0.049 | +0.16 | +0.27 |

`vt-own-70-x` had about 0.4 times the price rules' SE in pooled-1: roughly +0.02 to +0.07 at
z 2.50. Within FX (the dollar) and within bonds (world rates) the differences are likely
correlated (returns: +0.5), so the 0.3-0.5 rows are the realistic ones. The result reports the
realised SE and the edge found at 80%.

## Controls and checks

- Look-ahead tests (`tests/test_pooled2.py`): weekly decisions and own-vol shares unchanged when
  every later bar is removed or changed; with publication lag the signal never reads a session
  whose `available()` date is after the Friday; monthly decisions unchanged when later months are
  removed and never read a month inside the gap; with zero lag the weekly engine equals
  `pooled1_core.decide` / `own_vol` exactly; a variant identical to its twin gives D = 0 in every
  draw; month-cell sums give the same Sharpe as the returns themselves.
- **Plumbing run on random walks** (each series replaced by an i.i.d. normal walk, zero drift in
  excess terms, volatility 8% bonds, 10% currencies, 25% commodities, on its own dates; seed
  12345): D near 0 and z inside about +-2. Reported, then one real run.
- **Drift-matched null** (pooled-1's amendment 1, as a reading aid): 100 replications of i.i.d.
  normal walks with each series' own mean and standard deviation of (daily or monthly) log
  excess returns, seed 1000 + replication; null mean and 5/95% quantiles of D; "beyond drift"
  = D - null mean; pooled-1's reading rule ("exposure, not timing" for a pass not above the null's
  95% quantile).
- Checks reported, not deciding: blocks 3 / 24 months, costs x2, FX signals on spot only, GOV10
  with g = 3, each group alone, the correlation of d between markets (mean pairwise, over
  draws).

## Output and logging

- `research/pooled-2.md` (verdicts), `research/results/pooled-2.md` (+ `.json`), plumbing
  `research/results/pooled-2-plumbing.md`; code `research/lib/pooled2_core.py` (engines,
  bootstrap; numpy only) and `research/lib/pooled2.py` (data, run).
- `research/tries.md`: one `variant` row per variant and pooled test (`<v>@pooled2-nonequity-21`,
  `<v>@pooled2-com-8`, `<v>@pooled2-combined-62`; Sharpe cell = mean per-market Sharpe) and one
  `robustness` row per market and rule (`tsmom12`, `e4`, `vt-own-70-x` x 29 series).
  `research/ideas.md`: the `ensemble-tsmom` and `own-vol-target` lines.
