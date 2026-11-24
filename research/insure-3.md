# insure-3: is trend cheaper or dearer crash insurance than buying puts?

Lane insure-3, 2026-11-24 (night). Branch `insure-3`, draft PR #160. Research only: fake
money, keyless public data, no change to the gym, the daily runner or the live strategies.
Card: [`cards/insure-3.md`](cards/insure-3.md) (pushed before any number). Tables:
[`results/insure-3.md`](results/insure-3.md). Code: `lib/fetch_insure3.py`, `lib/insure3.py`,
tests `tests/test_insure3.py`. Train data only (nothing after 2025-10-31 kept or parsed).

## The answer on one screen

**Over 1986-2025 on the S&P 500, trend was much cheaper insurance than buying puts, in total
and in slow bear markets. Puts were the better insurance in the two named fast crashes (1987,
2020), where trend failed. A 50/50 mix covers that weakness only partly: it lost less than
trend in both fast crashes, but its insurance cost more per fall avoided than trend's.**

| 1986-07..2025-10 | CAGR | Behind holding, pts a year | Sharpe above bills (SE) | Worst loss | Share of each 15% fall avoided | Insurance cost | Premium P |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hold S&P 500 (total return) | 11.1% | - | 0.50 (0.17) | 55% | - | - | - |
| `tsmom12` (cash at bills) | 10.8% | 0.37 | 0.58 (0.17) | 33% | 0.56 | **0.02** | **1.05** |
| PPUT (5% out-of-the-money monthly puts) | 8.0% | 3.14 | 0.41 (0.17) | 42% | 0.37 | **0.28** | **1.60** |
| 50/50 trend + PPUT, monthly rebalance | 9.5% | 1.68 | 0.54 (0.17) | 29% | 0.47 | 0.12 | 1.25 |

Insurance cost = points of CAGR a year behind holding, divided by the mean loss avoided per
fall (log points); lower is cheaper. Premium P (insure-1): log points given up outside the falls
per log point saved inside them; 1.0 = break even.

- **Which was cheaper: trend, by both measures.** Puts cost about 3.1 points of growth a year
  and avoided 11 log points per fall (0.37 of each fall); trend cost 0.4 points a year and
  avoided 17 (0.56). Per unit of loss avoided the puts were about 13 times dearer on the lead's
  measure (0.28 against 0.02) and 1.5 times on insure-1's premium (1.60 against 1.05). With cash
  at 0 (the gym's rule) trend's cost rises to 0.06 / 1.12, still far below the puts. The same
  order holds on every shorter window of the side table (2002-, 2006-, 2007-, 2008-: trend
  0.04-0.12, PPUT 0.20-0.24).
- **Which kind of crash.** In the two named fast crashes the puts won clearly: 1987 PPUT -11.0%
  against trend -33.0% (trend was fully in, same as holding), 2020 PPUT -11.8% against trend
  -19.8%. Puts also lost less in the four other falls where trend stayed in and lost what
  holding lost or nearly so: 1998 (-12% against -19%), 2010 (-8% against -16%), 2011 (-11%
  against -19%) and 2025 (-11% against -17%). Where trend got out partway (1990, 2018) it lost
  less than the puts. Trend won clearly in the slow bear markets and their later legs, where it
  was already out: 2000-02 (four falls, trend between -8% and +1%, PPUT
  -15% to -24%), 2007-09 (trend -14%, 0% and 0%; PPUT -31%, -12% and -23%) and 2022.
  By the card's cut, falls of 92 days or less (10 of 17) still favour trend on average (share
  avoided 0.52 against 0.41), because four of them are legs of slow bear markets in which trend
  was already in cash; the slower falls (7) favour it more (0.61 against 0.30).
- **Does a mix cover trend's fast-crash weakness? Partly** (card rule: "partly" when it loses
  less than trend in both 1987 and 2020 but costs more per fall avoided). 1987: mix -21.9%
  against trend -33.0%; 2020: -15.9% against -19.8%. Its insurance cost (0.12, premium 1.25)
  sits between trend's and the puts', not at or below trend's. What the mix does buy: the
  smallest worst loss of the four (29%, against 33% trend and 42% PPUT), because the two kinds
  of insurance fail in different crashes.
- **Sharpe.** Trend 0.58, mix 0.54, holding 0.50, PPUT 0.41, each with a standard error of
  about 0.17: the order is not resolved. Puts as published lose Sharpe against holding,
  consistent with the literature survey-6 quoted (Israelov 2019: PPUT alpha about -1.8% a year).

## Side table (descriptive, own windows)

| Index (from) | CAGR | Behind holding | Worst loss | 2020 crash | 2008 (Oct 2007 - Oct 2008) | Insurance cost (trend / PPUT on the same window) |
|---|---:|---:|---:|---:|---:|---|
| VXTH, S&P 500 + VIX calls (2006-03) | 10.3% | 0.70 | 43% | **+27.6%** | -29.4% | 0.06 (0.09 / 0.24) |
| PUT, put writing (2007-01) | 6.8% | 3.96 | 37% | -28.9% | -26.9% | 0.39 (0.09 / 0.23) |
| BXM, call writing (2002-03) | 5.8% | 4.14 | 40% | -30.2% | -29.1% | 0.47 (0.04 / 0.23) |
| CLL, 95-110 collar (2008-08) | 6.8% | 5.56 | 26% | -14.9% | (from 2008-08 only) | 0.39 (0.12 / 0.20) |

- **VXTH is the only option index whose cost comes near trend's** (0.06 against trend's 0.09 on
  2006-2025), and it is the opposite insurance: it gained 28% in March 2020 and paid nothing
  in the slow 2008 bear (-29%). VXTH and trend fail in different crashes, like PPUT and trend.
  Its rule (buy VIX calls when VIX is in a band) is set by CBOE with hindsight of its launch in
  2006; one fast crash carries its record.
- Put writing (PUT) and call writing (BXM) are not insurance: they sell it. They lost nearly as
  much as holding in the fast crashes and cost the most growth.
- CLL's window starts in 2008-08 and 44 sessions had no level (carried); the collar caps
  rallies, which is where its cost comes from.

## How sure

- **One history.** 17 falls of 15% or more in 39 years, two named fast crashes, one fall over a
  year (2007-08). The cost measures are ratios of small numbers: trend's gap to holding is only
  0.37 points a year here because the window opens near the 1987 crash and covers two deep bear
  markets trend sat out. Since 2010 (no deep bear market) trend trails holding by 3.2 points a
  year against 3.4 for PPUT (diagnostic re-score, no row): in a decade without a deep bear
  market the two cost about the same growth.
- **Gap to holding since 2002:** trend trails holding on the S&P 500 total return by 0.7 (cash
  at bills) to 1.0-1.1 (cash at 0) points a year. insure-2's 2.2 (SUMMARY's "about 2 points")
  is the mean over the French market and 10 value-weighted industries with cash at 0, not the
  market alone; industries whip trend around more. For the broad US index SUMMARY's figure
  looks about twice too high; not reconciled per series tonight (review of #160).
- **PPUT is an index, not a fund.** No fees, no bid-ask on the puts; a real put buyer pays
  more, so the puts' cost here is a lower bound. Trend carries 2 bps a side.
- **The trend rule is the record's** (`trend_tune.paper`): the tests check that its positions
  equal an independent restatement of the rule, and that changing every price after a Friday
  leaves the positions through the next Friday unchanged.
- **Disclosure:** the one run was made before the script and tests were pushed (the card was
  pushed first, as required; the step order slipped for the script). The tests were then
  written and passed without changing the script; the run was not repeated.
- **Data.** S&P 500 total return: Yahoo `^SP500TR` from 1988-01-04, before that (warm-up from
  1985 and the first 18 months) the cached `^GSPC` price plus Shiller's monthly dividends;
  the built series tracks the official one at daily correlation 0.9996 and 0.15 points a year
  less growth over 1988-2025. Bills: cached Yahoo `^IRX`. CBOE files: PPUT, PUT, BXM, CLL,
  VXTH loaded with a plain request (`cdn.cboe.com`, 307 redirect to `cdn-api.cboe.com`);
  `SPXTR` was refused (403), recorded and not retried.
- **Terms of use.** CBOE's terms (cboe.com/terms, section 2) allow one copy for "personal
  non-commercial use" and forbid copying, storing, distributing or creating a derivative work
  without written consent; cboe.com/use-of-content asks for a licence for any other use of
  Cboe content. So the raw index levels stay in the local data cache (git-ignored) and only
  summary statistics are committed here. Whether publishing summary statistics in a public repo
  is covered is a judgement call; survey-6 did the same. Yahoo data likewise stays in the cache.

## Count and bar

- `tries.md`: 10 rows, idea `insure-3` (hold and the five CBOE indices `baseline`; trend and
  mix, each with cash at bills and at 0, `robustness`). Sharpe there in the file's convention
  (daily calendar, zero rate). No selectable claim: nothing here is a pick.
- Bar for scale (BAR.md, rows through 2026-11-24 20:01): 3,855 tries, N 1,083 for a new pick,
  N_eff 500, z >= 4.70 (+0.31 over `tsmom12` for a close rule), Bonferroni p <= 1.0e-04. Not
  applicable: a description, no test.

## For the live rule

Nothing changes. The record can now say: trend's crash insurance was cheaper per unit of loss
avoided than the market price of index puts (as PPUT buys them) over 1986-2025, but puts (and
VIX calls) cover the fast crashes from a calm high that trend misses. Buying either is a risk
preference, not an edge; options are outside the paper broker in any case.

## Next (not started)

1. Reconcile the gap to holding since 2002 per series: insure-2's 2.2 points a year is the mean
   over the French market and 10 industries (cash at 0); here 0.7-1.1 on the S&P 500 total
   return. Then correct SUMMARY's "about 2 points" for the broad index if it holds.
2. Put protection only while trend is in the market (puts when exposed, nothing in cash): a
   new rule, needs its own card; the side table suggests it would target exactly trend's
   fast-crash gap. Would be a variant against the bar, and options cannot be paper-traded here.
