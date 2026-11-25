# e4-indep-1: does `e4` beat `tsmom12` on stock data it has never seen?

Lane `e4-indep-1`, written 2026-11-25 21:10 UTC **before any `e4` or `tsmom12` number on the
tested series is computed**. Seen before writing: the spans and documentation of the files
below (first/last month, missing months, how each level was observed), and one power
calibration on already-scored data (US 1927-2025, standard errors only, section "Power").
Research only: fake money, keyless public data, no change to the gym, the daily runner or the
live strategies. Nothing after 2025-10-31 is read.

## Question

`e4` (a 1/3/6/12-month time-series momentum ensemble) is the only open lead: +0.063 Sharpe a
market over `tsmom12` on pooled-1's 41 stock markets (#142, SE 0.041, z 1.55); +0.010 on bonds
and currencies, -0.019 on commodity spot (#159); pooled over 62, +0.045 (z 1.43). #168 and #178
explain the lead descriptively (graded buy-back after the low, earlier partial exits). The
queue rule: do not retune it, test it again only on new independent data, pre-registered.
**On stock markets and periods where `e4` was never scored, is `e4`'s Sharpe higher than
`tsmom12`'s?** One pre-specified hypothesis, one direction.

## What was used before (every record that scored `e4`, from `tries.md`)

| Record | Series | Period |
|---|---|---|
| ensemble-tsmom (2026-11-12) | the six live assets; ETFs; coins; ^GSPC 1962-1993; ^N225, ^FTSE, ^GDAXI | 1962-2025 |
| crypto-alone | BTC, ETH | 2013-2025 |
| deep-1 | index atlas | 1962-2025 |
| pooled-1 (#142) | 41 stock markets: French US 10 industries (1927-07 on), 13 developed and 10 other country indices (1966 on), 8 ETFs | 1927-07..2025-10 |
| pooled-2 (#159) | 3 US bonds, 9 foreign bonds, 9 currencies, 7 PPI commodities + gold | 1927-04..2025-10 |
| e4-anatomy-1, reentry-reconcile-1, tick-tier-1 | re-scores of the pooled-1/pooled-2 series | same |

So every stock series scored for `e4` starts in **1927-07 or later**, and the markets are the
US, the 13 developed and 10 other countries listed in pooled-1 (no Nordic country, no
Ireland). Nothing before 1927 on any stock market. (JST annual data cannot carry the 1/3/6-month
legs; sector and style portfolios from 1926 are the same US market and years as the 10
industries: not independent.)

## Data (keyless, public)

**Primary pool P4 (deciding): four stock markets, every return before 1927-07.** No overlap in
time with any scored stock series, so no shared crash calendar with the 41 (1929, 1987, 2008
are all outside).

| Market | Series | Source | Observed | Gap g | Span (levels) |
|---|---|---|---|---:|---|
| US | S&P / Cowles composite price | Shiller `ie_data.xls` (cached) | monthly average | 1 | 1871-01..1927-06 (Aug-Nov 1914 closure carried flat by Shiller) |
| GB | Index of industrial shares (RES Memo 47) | NBER m11012a | end of month | 0 | 1867-07..1914-06 |
| GB | Industrial securities (LCES) | NBER m11012b | end of month to 1922, mid-month after | 0 | 1919-01..1924-12 |
| GB | Industrial stocks (LCES) | NBER m11012c | mid-month | 0 | 1925-01..1927-06 (too short: dropped by the rule below) |
| DE | Stock price index (Vierteljahrshefte, Sonderheft 36) | NBER m11023a | not stated | 1 | 1870-01..1913-12 |
| DE | Stock price index, 329 stocks | NBER m11023b | not stated | 1 | 1924-01..1927-06 (too short: dropped) |
| FR | Stock price index (Soc. de Statistique de Paris) | NBER m11024 | near end of month | 0 | 1899-01..1914-07 |
| FR | same series, 1919 on (Indices generaux) | NBER m11024 | not stated | 1 | 1919-01..1927-06 |

NBER Macrohistory, chapter XI, `data.nber.org/databases/macrohistory/rectdata/11/<id>.dat`
(fetched 2026-11-25, 0.2 MB, kept in the local cache only). Each run of consecutive months is a
**segment**; a segment counts if it has at least **48 scored months** (by the spans: GB
1925-27 and DE 1924-27 drop; all others count). Segments of one market are run separately
(each with its own 12-month warm-up) and their scored months concatenated into one return
series per market. Scored years from the spans: US 55.3, GB 50.8, DE 42.8, FR 21.8 (171).

**Secondary pool N5 (reported, not deciding): five stock markets never scored, but in years
that overlap the 41.** Kenneth R. French international country files (cached by data-long-4,
`F-F_International_Countries.zip`), `Mkt` = value-weight USD return with dividends, month end
(g = 0): Denmark 1989-, Finland 1988-, Ireland 1991-, Norway 1975-, Sweden 1975-, to 2025-10.
New markets, old calendar: their crashes are the 41's crashes, so this pool is weaker evidence
than P4 (pooled-1 measured a cross-market correlation of the differences of about 0.3).

## Rules (frozen code, unchanged)

pooled-2's monthly versions (`research/lib/pooled2_core.py`, `decide_monthly` and
`run_monthly`, frozen in `cards/pooled-2.md`), called as they are:

- `tsmom12`: position over the return of month t = 1 if level(t-1-g) / level(t-13-g) > 1, else 0.
- `e4`: position = share of the 1, 3, 6 and 12-month changes of level(t-1-g) that are > 0
  (0, 1/4, .., 1).
- Long or flat, cash earns 0, cost **2 bps** a side on the position change (pooled-1's index
  cost). Price returns (no dividends) for P4, both rules alike (only the US has dividends; a
  check uses them). `run_monthly` also builds `vt-own-70-x`; it is never read or reported here.
- g = 1 where the level is a monthly average or its observation date is not stated (a signal
  must not read a month the traded return already started in), 0 for documented end-of-month
  or mid-month point prices.

## Statistic

For each market, d = Sharpe(`e4`) - Sharpe(`tsmom12`) on its scored months (monthly mean / sd x
sqrt 12, cash 0, as pooled-2). **D = equal-weight mean of d over the pool's markets.** SE =
standard deviation of D over a **joint circular block bootstrap of calendar months** (12-month
blocks, the same draw for every market, each market's Sharpes recomputed on its own periods in
the draw; 2,000 draws, seed 0): `pooled2_core.cells` / `bootstrap` / `pooled`, as pooled-2,
the project's dependence-robust SE for this comparison. z = D / SE.

## Pre-registered rule (P4 decides; one-sided)

- **Confirmed** (independent replication): **z >= 1.645** (one-sided 5%).
- **Contradicted**: D + 1.645 SE < +0.063 (the one-sided 95% upper bound is below the size
  pooled-1 reported: that size does not carry to independent data).
- **Not confirmed, not contradicted**: neither (too little power to tell).

N5 gets the same three readings, reported, not deciding. Shown, not deciding: per-market d and
the count of d > 0; checks (g = 1 for every series; cost 50 bps a side; blocks of 6 and 24
months; US with Shiller's dividends; leave one market out; 1867-1897 vs 1898-1927); an
inverse-variance combination of P4 with pooled-1's 41 (D +0.063, SE 0.041; P4 is independent of
it in time).

## Bars (for context)

This is a confirmation test of one pre-specified hypothesis, not a selection: one-sided 1.645
is its level. It is **not** the bar for a new pick. `research/register/BAR.md` (rows through
2026-11-25 01:16): 4,126 distinct tries, N = 1,116 selectable + live, N_eff = 506 at measured
rho 0.55; a new pick needs **z >= 4.70** (DSR 0.95; Bonferroni p <= 9.9e-05), measured range
z 3.25 (ONC) .. 4.70. pooled-1's own family bar was z >= 2.50 (Bonferroni over its 8 rules).
`e4` already has 94 rows in `tries.md` (variant, robustness and note rows). A pass here leaves
`e4` an open lead with independent support; nothing goes live from this lane, the held-out year
stays unspent.

## Power (computed before this card, on already-scored data only)

`e4indep1.py power`: the same monthly code on Shiller US 1927-07..2025-10 (the US market and
years pooled-1 already scored; only standard errors printed, no difference looked at):
95.2 years scored, bootstrap SE of one market's d **0.059** (rho of `e4` and `tsmom12` monthly
returns 0.90; Jobson-Korkie-Memmel SE 0.046, so the bootstrap ratio k = 1.27, near
power-map-1's form SE = k sqrt(2 (1 - rho) / Y)). Scaled by sqrt(years) to each market and
pooled with a cross-market correlation c of the d's:

| Pool | c | Expected SE | Power at D +0.045 | +0.063 | +0.10 | MDE at 80% |
|---|---:|---:|---:|---:|---:|---:|
| P4 | 0.0 | 0.047 | 0.25 | 0.38 | 0.69 | 0.116 |
| P4 | **0.3** | **0.064** | 0.17 | **0.26** | 0.47 | 0.158 |
| P4 | 0.5 | 0.073 | 0.15 | 0.22 | 0.39 | 0.181 |
| N5 | 0.3 | 0.060 | 0.19 | 0.28 | 0.51 | 0.149 |

**Expected power is low: about one chance in four of passing if the true edge is the +0.063
pooled-1 saw, one in six at the pooled +0.045.** This is all the keyless independent stock
data found (pre-1927 monthly series exist only for these four markets in the NBER files; the
other candidates are annual, or the same market and years). The test is run because it is the
only clean one available, and its result is read against this power.

## What each outcome means

- **Confirmed**: independent support for `e4`'s edge on stocks; `e4` stays the open lead with
  one replication. Still far from the bar (z 4.70), still not a pick.
- **Not confirmed, not contradicted** (the likely outcome by power): no new information either
  way; the lead stays "open, unconfirmed" and the clean independent stock data are spent.
  A later test needs other data (none found keylessly).
- **Contradicted**: the +0.063 size does not carry to independent stock data; `e4` is
  downgraded from "open lead" to "no evidence of an edge" (pooled-1's lean was likely sample
  noise or specific to the post-1927 calendar). Not a retune trigger.
- A fail on P4 does not kill `e4` on the 41 (their D stands as measured); it says the lead did
  not replicate.

## Logged

One `variant` row per pool (P4 deciding, N5 secondary), a `robustness` row per market and per
check, a `note` row for the power calibration. Card not amended after numbers; any deviation is
written in the result file.
