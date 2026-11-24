# Data long 3: keyless long histories for rates, currencies and commodities

Lane `data-long-3`, 2026-11-24 (night). Branch `data-long-3`. Research only, fake money, keyless
public data, no raw vendor data committed. No strategy is tested here (that is the next lane,
with its own card).

Why: pooled-1 (PR #142) pooled near-miss trend variants over 41 stock markets; they share one
crash calendar (cross-market correlation of the differences about 0.3), so its power stalled
near +0.13 Sharpe per market. Only asset classes with their own calendar add independent
samples: long histories of rates, currencies and commodities. None was in the cache
(data-long-1/2 gave one US 10y bond rebuilt from Shiller and datahub gold, both monthly
averages).

## Plan (written and pushed before any derived number is computed)

Sources to try, in order (spans as documented, to be read from the files):

1. **ALFRED keyless CSV**, vintage 2025-11-10 (`alfredgraph.csv?id=<ID>&vintage_date=2025-11-10`):
   the series as known on 2025-11-10, so the files hold nothing from the held-out year and no
   later revision. Plain `fredgraph.csv` timed out from this machine tonight (HTTP/2 reset, then
   no answer), as on 2026-11-18; ALFRED answered.
   - US Treasury constant-maturity yields: daily `DGS1`, `DGS2`, `DGS5`, `DGS7`, `DGS10`,
     `DGS20`, `DGS30`; monthly averages `GS1`, `GS5`, `GS10`; bills `DTB3`, `TB3MS`.
   - FX spot (Fed H.10 noon buying rates, New York): `DEXJPUS`, `DEXUSUK`, `DEXSZUS`,
     `DEXCAUS`, `DEXGEUS` (to 2001) + `DEXUSEU` (from 1999), `DEXUSAL`, `DEXUSNZ`, `DEXSDUS`,
     `DEXNOUS`.
   - Foreign short and long rates (OECD Main Economic Indicators via FRED, monthly):
     `IR3TIB01<cc>M156N` (3-month interbank), `IRLTLT01<cc>M156N` (10y government) for the
     same currencies.
   - Commodities: `PPIACO` and PPI commodity groups (BLS), `WTISPLC` (WTI monthly),
     `DCOILWTICO` (WTI daily from 1986).
2. **World Bank Commodity Price Data ("Pink Sheet")**, `CMO-Historical-Data-Monthly.xlsx`,
   monthly nominal USD prices of about 70 commodities from 1960.
3. **Yahoo daily ETF closes** for validation only: `IEF`, `TLT`, `SHY` (already cached
   2026-11-12) and the CurrencyShares trusts `FXE`, `FXY`, `FXB`, `FXF`, `FXC`, `FXA` (to fetch,
   cut at 2025-11-10).

Derived series and how each will be validated (method fixed now):

- **Bond total return from a constant-maturity yield.** Each period, buy a par bond of maturity
  M at yield y(t-1) (coupon = y(t-1), semiannual), hold it for one period, then reprice it at
  y(t) with maturity M - dt; return = price change + accrued coupon. Exact pricing, not a
  duration approximation (the duration-convexity form is shown next to it as a check). Daily
  (dt = 1/365 by calendar days) and month-end (from the last daily yield of each month).
  Validation: daily and monthly returns of the 10y (and a 7y/10y blend) against `IEF`, 20y
  against `TLT`, 2y against `SHY`, 2002/2003 to 2025-10: correlation, tracking error a year,
  mean gap a year, and the worst drawdown of each. "Good enough for a monthly trend test" means
  a monthly correlation of 0.95 or more and a mean gap within 1 point a year (an ETF pays fees
  of 0.15% and holds a spread of maturities, so a small gap is expected). Stated now; reported
  whatever it shows.
- **FX excess return (carry included).** Long the foreign currency against USD for one month,
  funded in USD: r = S(t)/S(t-1) x (1 + i_f(t-1)/12) / (1 + i_us(t-1)/12) - 1, with S in USD
  per foreign unit, i_f the foreign 3-month rate, i_us the 3-month T-bill (monthly averages
  of the month before, known at the start of the month). Spot-only returns reported next to it.
  Validation: against the CurrencyShares trusts (spot plus the deposit rate they earn, minus a
  0.40% fee), 2005/2007 to 2025-10, monthly: correlation and mean gap a year.
- **Commodities:** spot price returns only (monthly averages). A futures investor earns spot
  plus roll yield plus collateral interest; the Pink Sheet has none of the last two. Reported
  against the cached S&P GSCI series if its kind (spot, excess or total return) can be read,
  as a sign of how far spot and investable returns drift apart; no claim that spot is
  investable.

Not done here: any trend rule or strategy statistic on these series.

## The answer on one screen (results, 2026-11-24)

**Long keyless histories now exist in the cache for 4 US Treasury maturities (daily from 1962/
1976/1977), 9 foreign 10-year government bonds (monthly averages, 1955-1989 on), 9 G10
currencies against USD with carry (daily spot from 1971) and 12 BLS commodity price indices
(monthly, 1913/1926/1947 on). The bond rebuild matches the real ETFs closely (monthly
correlation 0.97-0.99, mean gap within 0.6 points a year: the plan's bar is met), the currency
spot matches the CurrencyShares trusts (0.99), the carry is approximate (about 1 point a year
richer than the trusts). Commodities are spot prices: a futures fund on oil (USO) earned about
10 points a year less than spot oil did, 2006-2025, so commodity series answer "does the price
trend", not "what an investor earned".** Across classes monthly returns are close to
uncorrelated (mean -0.12 to +0.07); inside a class they are not (currencies +0.51, because all
are priced against the same dollar; bonds +0.52). No strategy was run.

Code: `lib/long_x_fetch.py` (fetch, cache only), `lib/long_x.py` (parsers and derivations, no
I/O; tests `tests/test_long_x.py`, offline, small in-code fixtures), `lib/long_x_build.py`
(validation, statistics, and `panel()`, the entry point for the next lane). Tables:
`results/data-long-3.md` (+ `.json`; statistics only, no prices or return series).

## Sources, terms, timing

Fetched 2026-11-24 with `uv run python -I research/lib/long_x_fetch.py` into
`<cache_root>/data-long-3/` (write-once, manifest line with URL, time, size, SHA-256; cache root
from the git-ignored `research/macro.local.json`). Nothing raw is committed. "Available" is the
conservative first day a value was public, as coded in `long_x.available()`; a signal must not
use a value before that day.

| Source (all keyless) | Series | Span in the cache (to 2025-10) | Freq | Available | Revised? | Terms |
|---|---|---|---|---|---|---|
| ALFRED, Fed H.15 | `DGS1/2/5/7/10/20/30`, `DTB3` | 1962-01 (2y 1976-06, 30y 1977-02 (no gap in the cached vintage: 2002-02..2006-02 has values), 20y gap 1987-1993), bills 1954 | daily | next business day | no (rare corrections) | US public domain |
| ALFRED, Fed H.15 | `GS1/2/5/7/10/20/30`, `TB3MS` | 1953-04 (bills 1934) | monthly average | first business day of next month | no | US public domain |
| ALFRED, Fed H.10 | `DEXJPUS`, `DEXUSUK`, `DEXSZUS`, `DEXCAUS`, `DEXUSAL`, `DEXUSNZ`, `DEXSDUS`, `DEXNOUS` (1971-01), `DEXUSEU` (1999-01) | 1971-01-04 | daily (noon New York buying rates) | the Monday after the week (H.10 is weekly) | no | US public domain |
| ALFRED, Fed H.10 | `EXGEUS` (mark per USD) | 1971-01..2001-12 | monthly average | as above | no | US public domain |
| ALFRED, OECD MEI | `IR3TIB01<cc>M156N` (3m interbank), `IRSTCI01<cc>M156N` (call money), `IRLTLT01<cc>M156N` (long-term government) | per country, 1955-2002 (table in results) | monthly average | about 2 months later (coded: start of m+3) | occasionally | OECD data, attribution (OECD terms; FRED marks them "copyright OECD"): do not commit |
| ALFRED, IMF IFS | `INTGST<cc>M193N` (T-bill), `INTDSR<cc>M193N` (discount) | 1950-1964 on, most end 2013-2021 | monthly | not coded (gap fillers before 1986 only) | occasionally | IMF terms, attribution: do not commit |
| ALFRED, BLS PPI | `PPIACO`, `WPU01`, `WPU012`, `WPU0121`, `WPU013`, `WPU051`, `WPU0531`, `WPU0561`, `WPU10`, `WPU101`, `WPU102`, `WPU1022` | 1913-01 / 1926-01 / 1947-01 (natgas 1967) to 2025-08 | monthly; the price of the Tuesday of the week with the 13th, not an average | about the 16th of the next month | yes, 4 months after first release | US public domain |
| ALFRED | `WTISPLC` (WTI, monthly average, 1946), `DCOILWTICO` (WTI daily, EIA, 1986) | | | | no | WTISPLC: third-party source on FRED (do not commit); EIA public domain |
| ALFRED, IMF PCPS | `POILWTIUSDM`, `PCOPPUSDM`, `PWHEAMTUSDM`, `PMAIZMTUSDM`, `PNGASUSUSDM` | 1990-01 | monthly average | | | IMF terms; cross-checks only |
| Yahoo chart API | `FXE`, `FXY`, `FXB`, `FXF`, `FXC`, `FXA` (new); `IEF`, `TLT`, `SHY`, `USO`, `^GSPC` (cache of 2026-11-12) | 2005-2007 on | daily | | | Yahoo terms, no redistribution; validation only |

Vintage: every ALFRED file is the vintage of 2025-11-10, the series as known that day. So no
observation from the held-out year is on disk, and no revision published later is used. For
PPI this means revised values (final), not the first releases a trader saw: a next lane that
wants first releases can fetch each month's vintage from ALFRED (not done here; revisions to
12-month commodity changes are expected to be small, not measured).

Not reachable or not available (2026-11-24, from this machine):
- `fred.stlouisfed.org/graph/fredgraph.csv`: HTTP/2 stream reset, then no answer over HTTP/1.1
  (as on 2026-11-18). ALFRED's graph CSV answered. The St. Louis Fed CDN also reset requests
  carrying browser-like or "research script" User-Agents; urllib's default agent was answered.
- World Bank "Pink Sheet" (`CMO-Historical-Data-Monthly.xlsx`, CC BY 4.0, monthly from 1960,
  about 70 commodities incl. gold, silver, copper, oil, grains): HTTP 403 to the script (a
  browser-only CDN check). Not fetched. `long_x.parse_pink` and `xlsx_rows` (stdlib only, tested
  on a generated workbook) read it if someone downloads it by hand in a browser into
  `<cache_root>/data-long-3/worldbank/<date>/`. It would add metals (copper, gold, silver) and
  softs from 1960 as monthly averages.
- Daily German mark (`DEXGEUS`, `DEXFRUS`): 404 on ALFRED, not in the Fed's H.10 data package;
  Bundesbank's API answers a JavaScript bot check; LBMA gold JSON: HTTP 403. Gold stays the
  datahub monthly series (data-long-2).

## Method of the derived returns

- **US Treasury bonds** (`UST2`, `UST5`, `UST10`, `UST30`): constant-maturity par bond rebuilt
  from the yield (Swinkels 2019; also Damodaran's method): buy a par bond of maturity M at
  y(t-1), hold it dt, reprice at y(t) with M - dt by the annuity formula with fractional
  periods, add the coupon accrued over dt. Daily (dt = calendar days / 365) or month-end (last
  daily yield of each month, dt = 1/12). The duration-convexity approximation differs from the
  exact repricing by a tracking error of 0.04% a year on monthly 10y returns: either is fine.
- **Foreign government bonds** (`GOV10-<cc>`): the same rebuild with M = 10 from the OECD
  monthly-average long rate, minus the local 3-month rate of the month before: a local-currency
  excess return, which is roughly what a currency-hedged holder earns. OECD's "long-term" rate
  is a 10-year benchmark for most countries, but definitions differ by country and period (not
  checked series by series).
- **Currencies** (`FX-<cur>`): long the currency against USD for a month, funded in USD:
  (S(t)/S(t-1)) x (1 + i_f/12) / (1 + i_us/12) - 1, S = month-end USD per unit, i_f and i_us the
  3-month rates (monthly averages of the month before). Foreign rate by priority: OECD 3-month
  interbank, OECD call money, IMF T-bill, IMF discount rate (spans per country in the results);
  US: OECD 3-month interbank from 1964-06, else `TB3MS`. The euro line is the mark before 1999,
  converted at 1.95583, and the mark is only a monthly average (EXGEUS): `FX-EUR` is flagged as
  averaged.
- **Commodities**: monthly price changes of the BLS PPI indices (point prices, mid-month) and of
  `WTISPLC` (monthly average). No roll yield, no collateral interest.

## Validation (method fixed in the plan above; tables in `results/data-long-3.md`)

Monthly, 2002-07 to 2025-10 (280 months), synthetic minus ETF:

| Pair | Corr | Tracking error a year | Mean gap a year | Worst loss, synthetic / ETF |
|---|---:|---:|---:|---|
| 10y vs IEF | 0.988 | 1.48% | -0.33% | 26.2% / 23.2% |
| 7y/10y blend vs IEF | 0.991 | 0.92% | -0.55% | 22.7% / 23.2% |
| 20y vs TLT | 0.986 | 2.62% | -0.16% | 42.4% / 47.6% |
| 20y/30y blend vs TLT | 0.993 | 1.58% | +0.11% | 45.9% / 47.6% |
| 2y vs SHY | 0.974 | 0.39% | -0.02% | 5.9% / 5.4% |

- The plan's bar (monthly correlation 0.95 or more, mean gap within 1 point a year) is met by
  all three planned pairs. Weekly (Friday weeks) the correlations are 0.96-0.98. The ETFs hold a
  spread of maturities, pay a 0.15% fee and close at 16:00 against H.15's mid-afternoon bid
  quotes; that explains the residual.
- Against Damodaran's annual T-bond return, 1963-2024: correlation 0.988, mean gap +0.33
  points, mean absolute gap 1.04 points, largest 6.6 points (25 of 62 years more than 1 point
  apart: Damodaran uses one annual coupon and a different year-end yield).
- **Averaging costs a lot at the monthly level.** Returns rebuilt from monthly-average yields
  (`GS10`, or OECD's US long rate, which is the same number) correlate only 0.73 with the
  month-end rebuild (tracking error 5.4% a year), although the long-run mean is the same (gap
  -0.04%). An average-based return at month m covers roughly mid m-1 to mid m: smoothed and half
  a month late. All `GOV10-*` series are of this kind: usable for 12-month trend with the
  one-month gap of data-long-2, not for month-by-month timing.
- **Currencies**: spot against the trusts 0.990-0.995 for all six (tracking error 1.0-1.5% a
  year). Adding the 3-month rate makes the synthetic richer than the trusts by +0.6 to +1.3
  points a year: the trusts' 0.40% fee and their deposit rate, which was below interbank (and
  zero when policy rates were negative). So spot is validated; carry is an upper estimate.
- **Commodities**: BLS crude-oil PPI correlates 0.89 with the WTI quote on or before the 13th
  and only 0.55 with the month-end quote, which confirms the PPI is a mid-month point price.
  Month-end WTI spot beat USO (a front-month futures fund) by **+10.0 points a year**,
  2006-2025 (contango, roll); worst loss 86% against 98%. PPI primary nonferrous and wheat
  correlate 0.75 and 0.81 with the IMF copper and wheat prices (different baskets).

Data checks: the largest monthly moves are real events (the 1976 Australian, 1984 New Zealand
and 1982 Swedish devaluations, the 2015 Swiss floor exit, 1973-74 oil and grain shocks, April
2020 oil). One to look at before use: `GOV10-NZ` loses 24.7% in 1984-08 (the OECD monthly average
jumps from 10.25% to 15.03% in the month after the July 1984 election and devaluation;
plausible, not checked against a second source).

## Coverage of the panel (`long_x_build.panel()`, monthly, to 2025-10)

| Class | Series | From | Months | Correlation with the S&P 500 | Averaged? |
|---|---|---|---:|---|---|
| US bonds | UST2, UST5, UST10, UST30 | 1976-07, 1962-02, 1962-02, 1977-03 | 584-765 | +0.06..+0.10 | no (daily also available) |
| US bond, long | UST10-avg (GS10) | 1953-05 | 870 | +0.12 | yes |
| Foreign bonds (excess) | GOV10 JP, GB, CH, CA, DE, AU, NZ, SE, NO | 1955-02 (CA) .. 1989-02 (JP) | 440-848 | -0.02..+0.15 | yes |
| Currencies (excess, with carry) | FX JPY, GBP, CHF, CAD, EUR, AUD, NZD, SEK, NOK | 1971-02 (CHF 1972-02, NZD 1974-01, NOK 1979-02) | 561-657 | 0.00..+0.41 (AUD, NZD, CAD highest) | EUR before 1999 only |
| Commodities (spot) | PPI all, farm, grains, wheat, livestock, coal, natgas, crude, metals, steel, nonferrous, primary nonferrous; WTI-avg | 1913-02 .. 1967-02 | 703-1,351 | -0.04..+0.12 | WTI-avg only |

Market-years, each series once: about 230 (four US bonds) + 480 (foreign bonds) + 480
(currencies) + 590 (the seven non-nested commodity indices of point 5 below; 580 more in the
nested aggregates), about 1,800 in all, against pooled-1's ~1,900 equity market-years.

Average pairwise correlation of monthly returns, 33 series, 1989-02 to 2025-08 (common months):
bonds with bonds +0.52, currencies with currencies +0.51, commodities with commodities +0.20;
between classes -0.12 (commodities, bonds) to +0.07. These are correlations of returns, not of
per-market strategy differences (pooled-1's 0.3); they say the classes have their own
calendars, and that inside the FX and bond classes the series share one factor each (the
dollar; world rates).

## Caveats

- Rebuilt bonds are constant-maturity par bonds: no fees, no bid-ask, no on/off-the-run spread.
  The ETF check covers 2002-2025 only; 1962-2001, including the 1979-1982 Volcker years, is
  checked only against Damodaran's annual returns.
- Carry uses monthly-average rates of the month before, not the rate locked at the start of
  the month, and interbank or call-money rates, not what a retail deposit earned. Japan before
  1985 uses the IMF T-bill rate (administered then), the UK before 1978 the IMF T-bill rate.
- Before 1973-03 the currencies were in the Smithsonian band, not floating; 1971-1973 returns
  are policy steps (e.g. `FX-CHF` +15.5% in 1973-02).
- PPI indices are US producer prices of physical goods, not exchange prices, and nested (grains
  is in farm products, steel and nonferrous are in metals). The PPI was revised (final values
  used, see Vintage).
- Commodity spot is not investable (USO gap above). A trend rule on spot measures price trend;
  its "returns" are not a futures investor's.
- Cash and the US short rate are monthly; the repo convention (cash earns 0) understates every
  rule that sits out in the 1970s-80s, when bills paid 5-15%.

## Ready for: e4 and vt-own-70-x on rates, currencies and commodities (next lane, own card)

pooled-1 left `e4` (+0.063, z 1.55) and `vt-own-70-x` (+0.022, z 1.37) open and said only
markets with their own crash calendar could add power. The panel above is that input. What the
next lane's card must settle before any number:

1. **Bar and comparator.** Quote the current `BAR.md` (at the time of writing 3,855 tries, N_eff 500, z >= 4.70) and pooled-1's own
   bar (Bonferroni z >= 2.50 over its 8 rules; here 2 rules, so z >= 1.96 one-sided at 0.025 or
   keep 2.50 to stay comparable: decide in the card). Twin `tsmom12` on the same series and
   months.
2. **Frequency.** US bonds and the eight non-EUR currencies have daily data: pooled-1's weekly
   engine (365-day lookbacks, Friday decisions, one-session fill) can run nearly unchanged on
   them from the daily series (`lx.bond_returns(alfred("DGS10"), 10.0)`, daily FX from
   `lx.usd_per_unit`, daily carry = monthly rate / 365 per calendar day). Foreign bonds, PPI
   commodities, `FX-EUR` before 1999 and `WTI-avg` are monthly only: a monthly version of each
   rule must be frozen in the card (e4 as 1/3/6/12-month signs; own-vol sigma from the last 36
   monthly returns, or state another choice) before the run.
3. **Gaps for averages and publication.** Averaged series (`averaged=True` in `panel()`) need
   the one-month gap between the last return a signal sees and the first it trades
   (data-long-2). PPI of month m (priced near the 13th) is public about the 16th of m+1: a
   position over the PPI change from m to m+1 can use PPI up to m-2: PPI of m-1 is public about the 16th of m, after the mid-month price that starts the m→m+1 change; check with `lx.available()`.
4. **Excess returns and cash.** Compare rules on returns over the US bill (bond total return
   minus bill; currencies are already excess; commodity spot has no collateral), with cash
   earning the bill, or keep cash at 0 for every series and say why. Without this, bonds' 5-7%
   yield in the 1970s-80s dominates every Sharpe.
5. **Which series count.** Drop nested and duplicate ones before the run: suggested pool of 9
   foreign + 3 US bonds (UST2, UST10, UST30: UST5 sits between), 9 currencies, 7 commodity
   indices (grains, livestock, coal, natgas, crude, steel, primary nonferrous; not PPI-all,
   farm, metals, nonferrous, wheat, WTI-avg), and gold from datahub (1971, averaged): 29
   markets. FX from 1973-03 (floating).
6. **Correlation.** Joint calendar-block bootstrap as pooled-1 (it keeps the within-class
   factors: the dollar for currencies, world rates for bonds). Report the pool alone and
   together with pooled-1's 41 equity markets.
7. **Costs.** 2 bps (pooled-1's index cost) is too low for commodities and some 1970s
   currencies; state a cost per class (e.g. 2 bps bonds, 3 bps currencies, 10 bps
   commodities) and a 2x check.
8. **What a pass means.** Spot commodities are not investable; carry is an upper estimate. A
   pass on this pool would say "the variant's edge over `tsmom12` exists outside equities", not
   that the paper book could earn it. The held-out year stays unspent.

## Logged

One `note` row in `research/tries.md` (idea `data-long-3`). No strategy, no variant, no
selectable try.
