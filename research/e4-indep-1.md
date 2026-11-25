# e4-indep-1: `e4` against `tsmom12` on stock data it had never seen

Lane `e4-indep-1`, 2026-11-25 (night). Branch `e4-indep-1`. Research only: fake money, keyless
public data, no change to the gym, the daily runner or the live strategies; nothing after
2025-10-31 read. Card (pushed before any `e4` number on the tested data, not amended):
`cards/e4-indep-1.md` (commit 2f20007, 21:08 UTC; its header says 21:10, a typo). Tables:
`results/e4-indep-1.md` (+ `.json`), post hoc `results/e4-indep-1-posthoc.json` and
`results/e4-indep-1-freq41.json`. Code: `lib/e4indep1.py`, `lib/e4indep1_data.py`; tests
`tests/test_e4indep1.py`. Rules: pooled-2's frozen monthly `e4` and `tsmom12`, unchanged.

## The answer on one screen

**`e4`'s lead did not replicate on independent stock data. By the card's rule the result is
"contradicted".** On four stock markets before 1927-07 (US 1871-1927, GB 1867-1914 and
1919-1924, Germany 1870-1913, France 1899-1914 and 1919-1927; 171 market-years that overlap
no scored stock series in time), `e4` trails `tsmom12` by **D = -0.065 Sharpe a market (SE
0.041, z -1.59)**. The one-sided 95% upper bound is +0.002, below the +0.063 that pooled-1
found on 41 stock markets. `e4` wins in 1 of 4 markets (GB +0.096; US -0.054, DE -0.262,
FR -0.040).

- **It leans on Germany.** Without DE, D is +0.001 (SE 0.050). With dividends added (post
  hoc), D is -0.030 (SE 0.038). Its upper bound of +0.031 is still below +0.063, so the
  card's reading would not change. Without DE and with dividends, D is +0.019. So the data
  do not show that `e4` is *worse*. They show that an edge as large as the 41-market one is
  unlikely on these markets and years.
- **It is not only the monthly design.** Post hoc, the same monthly code on pooled-1's own 41
  markets gives +0.050 (no gap) and +0.023 (one-month gap), against pooled-1's weekly
  +0.063. A gap costs `e4` about 0.03 there. The pre-1927 pool (two of its four markets need
  the gap) is still about 0.07-0.09 below that, roughly 2 SE. Its one-sided upper bound
  (+0.002) is below both matched monthly-design figures (+0.050 with no gap, +0.023 with a
  one-month gap), not only below the weekly +0.063.
- **The secondary pool agrees with the 41, not with the pre-1927 pool.** Five markets never
  scored but in years that overlap the 41 (Denmark, Finland, Ireland, Norway, Sweden; French
  country files, 1975-2025) give **D = +0.067 (SE 0.057, z +1.18), 4 of 5 positive**. That is
  "not confirmed, not contradicted". The new markets that share the 41's crash calendar
  (1987, 2000-02, 2008, 2020) show the lead; the old calendar does not. N5 is not fully
  independent of the 41 either: pooled-1's EFA (one of its 8 ETFs) holds Nordic and Irish
  stocks. That fits a lead that
  belongs to the post-1975 calendar more than to stock markets in general. With 4 and 5
  markets this is a reading, not a finding.
- **Combined with the 41 (not deciding):** an inverse-variance mean of pooled-1 (+0.063, SE
  0.041) and the pre-1927 pool gives D -0.001, SE 0.029, z -0.04.

**What it means for the queue:** by the card, `e4` moves from "open lead" to "no evidence of
an edge on stocks in general": the +0.063 did not carry to nearly all the clean independent
stock data found keylessly (what is left: a small US-only pool before 1871, section 1). It is not a retune trigger. The 41's D stands as measured, and it is
not killed there. Expected power was low (0.26 at +0.063), so this test could not confirm
much. It still contradicted the pooled-1 size, and that is the informative direction.

## (1) What data had `e4` seen, and what is left

Every record that scored `e4` (from `tries.md`): ensemble-tsmom (six live assets, ETFs, coins,
^GSPC 1962-1993, ^N225, ^FTSE, ^GDAXI), crypto-alone, deep-1 (index atlas 1962-2025),
pooled-1 (41 stock markets from 1927-07: French US 10 industries, 13 developed and 10 other
country indices from 1966, 8 ETFs), pooled-2 (US and foreign bonds, G10 currencies, PPI
commodities from 1927-04, gold), and the re-scores e4-anatomy-1, reentry-reconcile-1 and
tick-tier-1 (the same series).

| Candidate (keyless) | Used? | Independent of the 41? | Verdict |
|---|---|---|---|
| Shiller / Cowles US monthly 1871-1926 | no | same market, earlier years: yes in time | **used (P4)** |
| NBER Macrohistory ch. XI: GB industrial shares 1867-1914, 1919-34; Germany 1870-1913, 1924-35; France 1899-1914, 1919-39 | no | before 1927-07: yes in time; GB/DE/FR after 1966 are in the 41 | **used (P4), cut at 1927-06** |
| NBER US railroad stocks m11005a 1857-1929 (m11005 from 1855) | no | from 1871 the same US market and years as Cowles; **1857-01..1870-12 (168 monthly levels, no gap, cached) overlaps neither Shiller nor the 41** | not used: missed when the card was written (review of #198). About 14 US years, so a US-only pool before 1871 is still unspent |
| Goetzmann-Ibbotson-Peng NYSE 1815-1925 (Yale ICF) | no | 1815-1870 would overlap nothing scored | **not checked** (probably keyless; not fetched or verified tonight) |
| NBER Frickey 1902-23, Dow-Jones 1897- | no | same US market and years as Cowles | not used (duplicate) |
| French international country files, 1975- | DK, FI, IE, NO, SE never | new markets, same years as the 41 | **used as secondary (N5)**; the other 16 countries are in the 41 |
| French US sector / style portfolios, 1926- | no | same market and years as the 10 industries | not independent |
| JST Macrohistory, annual 1870-2020 | yes (tsmom12 only, insure-1870-1) | annual: cannot carry the 1/3/6-month legs | not usable |
| data-long-3 commodities, PPI 1913-1926 | no (pooled-2 scored from 1927) | yes in time | not a test of the equity lead (commodities already -0.019); only aggregates exist before 1926 |
| data-long-4 equity yields, CPI, policy rates | no | n/a | not price series |

Download: NBER files, 0.2 MB (local cache `e4-indep-1/nber/`, not committed). Everything else
was already cached.

## (2) Card in short

D = equal-weight mean over markets of Sharpe(`e4`) - Sharpe(`tsmom12`), monthly returns, sqrt
12, cash 0, 2 bps a side. Signals read levels through month t-1-g, with g = 1 for monthly
averages or unstated observation dates (US, DE, FR 1919-) and g = 0 for end-of-month or
mid-month point prices (GB, FR 1899-1914). SE from pooled-2's joint circular 12-month block
bootstrap (2,000 draws, seed 0). Segments of one market run separately and are concatenated;
a segment counts with at least 48 scored months. The rule is one-sided: **confirmed** at z >=
1.645; **contradicted** when D + 1.645 SE < +0.063; otherwise not confirmed, not
contradicted. Expected SE was 0.064 (power 0.26 at +0.063, 0.17 at +0.045, MDE80 0.16), from
a calibration on already-scored US data. The realised SE (0.041) is smaller: the pre-1927 d's
are less correlated across markets than the c = 0.3 assumed.

## (3) Results

| Market | Scored years | `tsmom12` Sharpe | `e4` Sharpe | d |
|---|---:|---:|---:|---:|
| US (Shiller, g 1) | 55.3 | +0.412 | +0.358 | -0.054 |
| GB (NBER, g 0) | 50.8 | +0.394 | +0.490 | +0.096 |
| DE (NBER, g 1) | 42.8 | +0.541 | +0.280 | -0.262 |
| FR (NBER, g 0 / 1) | 21.8 | +0.355 | +0.314 | -0.040 |
| **P4 (deciding)** | 171 | | | **-0.065** (SE 0.041, z -1.59, upper +0.002): **contradicted** |
| DK | 35.8 | +0.709 | +0.699 | -0.010 |
| FI | 36.8 | +0.568 | +0.615 | +0.048 |
| IE | 33.8 | +0.458 | +0.566 | +0.108 |
| NO | 49.8 | +0.540 | +0.583 | +0.043 |
| SE | 49.8 | +0.590 | +0.735 | +0.146 |
| **N5 (secondary)** | 206 | | | **+0.067** (SE 0.057, z +1.18): not confirmed, not contradicted |

Checks named in the card (P4; not deciding):

| Check | D | SE | z | Upper (one-sided 95%) |
|---|---:|---:|---:|---:|
| g = 1 for every series | -0.124 | 0.039 | -3.15 | -0.059 |
| cost 50 bps a side | -0.177 | 0.047 | -3.78 | -0.100 |
| blocks 6 / 24 months | -0.065 / -0.065 | 0.040 / 0.040 | -1.63 / -1.63 | +0.000 / +0.001 |
| US with Shiller's dividends | -0.039 | 0.038 | -1.02 | +0.024 |
| without US / GB / DE / FR | -0.069 / -0.119 / +0.001 / -0.073 | 0.047 / 0.041 / 0.050 / 0.046 | | +0.008 / -0.051 / +0.083 / +0.002 |
| 1867-1897 | -0.175 | 0.056 | -3.15 | -0.084 |
| 1898-1927 | -0.039 | 0.057 | -0.69 | +0.055 |

Post hoc (not in the card, run after the result, reported, not deciding):

- **Dividends for all four** (US: Shiller; GB, DE, FR: JST R6 annual `eq_dp` / 12 added to each
  month of that year, GB 1867-1870 at the 1871 value; signals on the total-return level):
  D -0.030 (SE 0.038, z -0.81, upper +0.031); d US +0.051, GB +0.061, DE -0.180, FR -0.054;
  without DE +0.019. Price-only returns hurt `e4`: a steady dividend raises the Sharpe of a
  graded position more than that of an all-or-nothing one (mean grows with the average
  position, risk with its root mean square). The card's line "both rules alike" was wrong in
  direction, but the reading holds either way.
- **The monthly code on pooled-1's 41 markets** (month-end closes, already-scored data): D
  +0.050 at g 0 (SE 0.040; US10 +0.007, DEV13 +0.050, WIDE10 +0.091, ETF8 +0.055) and +0.023
  at g 1 (SE 0.036). The weekly-to-monthly move costs `e4` about 0.013. A one-month gap costs
  about 0.03 more. Neither closes the gap to P4.

## Caveats

- **Small and lopsided.** Four markets, one of them (DE) about 0.26 below the rest. Germany
  1870-1889 is an unweighted index of "representative stocks" and its observation date is not
  stated (g = 1). The early-period check (1867-1897, D -0.175) leans on that unweighted
  German index. The card counted DE as listed, and without it the pool reads zero, not
  positive.
- **France is a patched series.** m11024 chains several baskets in 1898-1914 (new bases or
  baskets in 1900, 1901, 1905 and 1908). Its compilers adjusted it so its annual averages
  match an annual series. The 1919-1927 segment holds a level-matched splice to the revised
  index in January 1926 (first computed 1922 on 194 securities; 288 securities from 1926).
  Levels are whole points: 65 of the 287 one-month changes through 1927-06 are exactly zero.
  The rules' strict `>` counts a zero change as "not up", so in France `e4`'s 1-month leg is
  pulled toward flat by rounding alone. France is a quarter of the pool's weight; without it D is -0.073 (upper bound
  +0.002), so the reading holds.
- **Old data.** Smoothed or stale old indices add positive autocorrelation to monthly
  returns. That should help `e4`'s fast legs, so smoothing is unlikely to explain the
  shortfall. The g = 1 check shows how much those legs depend on fresh data (-0.124 if every
  series waits a month).
- **The 1914 closures.** Shiller carries Aug-Nov 1914 flat; GB, DE and FR are cut at the
  closure (separate segments).
- **Costs.** At 50 bps a side, a level nearer 19th-century practice than 2 bps, `e4` loses
  clearly (it trades 2.3 times a year against 1.0 for `tsmom12` in the US). The card used
  pooled-1's 2 bps so the test reads like the original.
- **The N5 reading** rests on 5 markets that share the 41's crash calendar. Its agreement
  with the 41 is what a calendar-specific edge predicts. It is also what a real but small
  edge plus noise predicts.

## Logged

40 rows in `research/tries.md` (idea `e4-indep-1`, 2026-11-25 21:12 UTC). 2 `variant` rows
(P4, deciding; N5, secondary). 18 `robustness` rows (`tsmom12` and `e4` per market) and 11
for the card's checks. 5 post hoc dividend rows and 2 monthly-41 diagnostic rows, both marked
POST HOC. 2 `note` rows (the power calibration, the meta-combination).
