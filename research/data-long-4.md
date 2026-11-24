# Data long 4: keyless long histories of consumer prices, equity yields and policy rates

Lane `data-long-4`, 2026-11-24 (night). Branch `data-long-4`. Research only, keyless public
data, no raw data committed. No strategy is tested here (no card, no `tries.md` row: nothing
here is a return series).

Why: xs-century-1 (PR #170) had to proxy currency value by 5-year spot reversal because no
consumer-price data was cached, and left out equity-index value and carry across countries
because no country dividend or earnings yields were cached. data-long-3 covers bonds and
currencies of 11 economies (US, JP, GB, CH, CA, DE/euro area, AU, NZ, SE, NO); this lane adds
the price levels, equity yields and policy rates of the same economies.

## Plan (written and pushed before any derived number is computed)

Sources (probed 2026-11-24; spans as the probes showed, to be confirmed from the files):

1. **BIS long consumer prices** (`WS_LONG_CPI`, index 2010 = 100), SDMX csv, keyless: monthly
   for all 11 economies from 1913-1949 (euro area 1990), annual from 1661 (GB), 1830 (SE), 1865
   (NO). AU and NZ "monthly" are quarterly values repeated over the quarter. The query's
   `endPeriod` keeps later months off the disk (monthly to 2025-09: October 2025 prints came
   out after 2025-11-10).
2. **BIS central-bank policy rates** (`WS_CBPOL`), monthly, from 1946 (GB, CH, SE, JP) to 1986
   (NO). Short rates are already cached (data-long-3: OECD 3-month interbank and call money,
   IMF T-bill and discount rates from 1950-1964); the policy rate fills the earlier years and
   is a check.
3. **Jorda-Schularick-Taylor Macrohistory Database R6** (annual 1870-2020, 18 countries, not
   NZ): CPI, short rate, long rate, equity dividend-price ratio (`eq_dp`), equity total and
   capital-gain returns, bill and bond returns. The pre-1913 and pre-1950 annual layer.
4. **Kenneth R. French international country files** with and without dividends (monthly from
   1975: GB, JP, CH, CA, DE, AU, NZ, SE, NO and 12 more): the value-weight market return in
   local currency with and without dividends, and annual value-weight averages of B/M, E/P,
   CE/P and dividend yield per country.
5. **ALFRED vintage 2025-11-10**: US CPI `CPIAUCNS` (BLS, 1913), OECD MEI CPI
   (`<ISO3>CPIALLMINMEI`, 1914-1955 on; ends 2021-2025) as a cross-check of BIS, OECD MEI share
   price indices `SPASTT01<cc>M661N` (monthly averages, 1950s on).
6. US dividend and earnings yields: Shiller's monthly file (already cached, 1871 on; no new
   fetch).

Derived series and checks (method fixed now):

- **Monthly CPI per economy** = BIS monthly index; AU and NZ flagged quarterly. Check: 12-month
  inflation from BIS against OECD MEI over their common months (correlation, mean absolute
  gap in points); same for US against `CPIAUCNS`.
- **Monthly trailing dividend yield per country (1976 on)** from French's two files: price
  index P from the return without dividends, the month's dividend D(t) = (r_with - r_without)
  x P(t-1), yield = sum of the last 12 D / P(t). Check: against French's own annual Yld
  (whichever month-end matches it best, reported with the lag) and against JST `eq_dp` over
  1976-2020 (correlation of levels, mean gap).
- **Annual earnings yield and B/M per country (1975 on)**: French's annual averages, as
  published; JST has no earnings.
- **Policy rate**: BIS monthly; check against the cached OECD 3-month rate (correlation of
  levels, mean gap) where both exist.
- `available()` timing for each kind (conservative): BIS monthly CPI of month m from the 1st of
  m+2; quarterly CPI from the 1st of the second month after the quarter; policy rate at the
  end of its month; French monthly dividends at the end of the month; French annual ratios of
  year t from 1 July of year t (accounting data of fiscal t-1; French forms the portfolios at
  the end of each December); JST annual values of year t from 1 July of t+1.

Terms: none of these licences clearly allows redistribution in an MIT repo (BIS: non-commercial
redistribution; JST: CC BY-NC-SA 4.0; French and OECD: no redistribution grant; BLS CPI is
public domain but is kept with the rest for one convention). Only code and statistics are
committed. Nothing after 2025-10-31 is parsed.

Not done here: any value, carry or inflation signal, rule or strategy statistic.

## The answer on one screen (results, 2026-11-24)

**Consumer prices now exist in the cache, monthly and unbroken, for all 11 economies of
data-long-3: from 1913-1926 for US, GB, CA, CH, NO, AU, NZ (AU and NZ quarterly), 1946 JP,
1949 DE, 1954 SE (quarterly 1918-1954), 1990 euro area; annual back to 1661 (GB), 1830 (SE),
1865 (NO), all to 2025-09.** So xs-century-1's currency value can use a real exchange rate
(spot x CPI ratio) for all nine currencies from 1971 instead of the spot-reversal proxy. **Country
equity yields exist monthly from 1975 for 9 of the 11** (JP, GB, CH, CA, DE, AU, SE, NO; NZ from
1988; US from Shiller since 1871), as a trailing dividend yield derived from French's returns
with and without dividends, plus annual value-weight E/P, B/M, cash-flow yield and dividend
yield from 1975; JST adds an annual dividend-price ratio back to 1870-1900 for 8 of them (no
Canada, no NZ). There is no keyless monthly earnings yield outside the US. **Policy rates** add
1946-1960 starts for US, GB, CH, SE, JP, DE, CA (short rates were already cached from 1955-1964).
The cross-checks pass where a second source exists (below); the weak spot is the derived
dividend yield against JST for DE, AU and NO (correlation 0.55).

Code: `lib/long_macro_fetch.py` (fetch, cache only), `lib/long_macro.py` (parsers and
derivations, no I/O; tests `tests/test_long_macro.py`, offline, small in-code fixtures),
`lib/long_macro_build.py` (coverage, checks, and the loaders `cpi`, `policy_rate`,
`dividend_yield`, `french_ratios`, `jst`, `us_yields`, `real_fx_series` for the next lane).
Tables: `results/data-long-4.md` (+ `.json`; statistics only, no levels).

## Coverage

| Series | Areas | Start | End | Freq | Source | Licence / terms | Gaps and notes |
|---|---|---|---|---|---|---|---|
| CPI, all items (index 2010 = 100) | US, GB, CA, CH, NO | 1913-01, 1915-01, 1914-01, 1921-01, 1926-02 | 2025-09 | monthly | BIS long CPI (`WS_LONG_CPI`) | BIS: non-commercial redistribution, cite BIS; not committed | NO one missing month (1926-01) |
| | JP, DE, SE, XM | 1946-08, 1949-01, 1954-06, 1990-01 | 2025-09 | monthly | BIS | as above | SE quarterly 1918-03..1954-03 |
| | AU, NZ | 1922-04, 1925-07 | 2025-Q3 | quarterly (repeated over the quarter's months) | BIS | as above | use `lm.quarter_ends` and `cpi-quarterly` timing |
| CPI, annual | GB, SE, NO, others | 1661, 1830, 1865, 1913-1946 | 2024 | annual | BIS | as above | |
| CPI, cross-check | 10 (no XM) | 1914-1955 | 2021-06 (JP) .. 2025-04 | monthly (AU, NZ quarterly) | OECD MEI via ALFRED, vintage 2025-11-10 | OECD terms, not committed | OECD stopped these; BIS is the series to use |
| CPI, US | US | 1913-01 | 2025-09 | monthly | BLS `CPIAUCNS` via ALFRED | public domain (kept in the cache like the rest) | identical to BIS US |
| Policy rate | GB, CH, SE, JP | 1946-01 | 2025-10 | monthly | BIS `WS_CBPOL` | BIS, not committed | JP missing 1999-03..2000-07, 2001-04..2006-02, 2013-05..2016-08 (quantity targets) |
| | DE | 1948-07 | 1998-12 | monthly | BIS | | then XM from 1999-01 |
| | US, CA, AU, NZ, NO | 1954-07, 1960-07, 1976-04, 1985-01, 1986-03 | 2025-10 | monthly | BIS | | |
| Dividend yield, trailing 12 months (derived) | JP, GB, CH, DE, AU, SE, NO; CA; NZ | 1975-12; 1977-12; 1988-12 | 2025-10 | monthly | Kenneth R. French international country files, with and without dividends | free for research; no redistribution grant; not committed | value-weight market of French's sample (all firms, local currency) |
| B/M, E/P, CE/P, D/P (value-weight averages) | same 9 | 1975 (CA 1977, NZ 1988) | 2025 (row t = December t-1) | annual | French | as above | |
| US D/P, E/P | US | 1871-01 | 2023-06 | monthly | Shiller `ie_data.xls` (cache of 2026-11-12) | not committed (earlier lanes) | the cached file stops at 2023-06 for D and E; a fresh download would extend it |
| JST R6: CPI, short and long rate, eq_dp, equity and bond returns | US, JP, GB, CH, CA, DE, AU, SE, NO (no NZ) | 1870 (eq_dp CH 1900, JP 1886, NO 1880; CA none) | 2020 | annual | Jorda-Schularick-Taylor Macrohistory Database R6 | CC BY-NC-SA 4.0; not committed | hand download (see fetch); cite Jorda, Schularick and Taylor (2017) |
| Share price index | 11 (EZ, NO from 1986) | 1950-1967 | 2025-09 | monthly average | OECD MEI `SPASTT01<cc>M661N` via ALFRED | OECD terms; not committed | price only, averaged |
| Real exchange rate input | 9 currencies | 1971-01 | 2025-09 | monthly | data-long-3 month-end spot x BIS CPI | derived, not committed | EUR before 1999 = mark (monthly average) with German CPI |

Not used, but open-licence fallbacks if BIS ever goes away: national statistics offices (UK ONS
under the Open Government Licence, Statistics Canada under the Open Government Licence - Canada,
Statistics Norway CC BY 4.0, Statistics Sweden CC0, ABS CC BY 4.0) publish their own CPI with
keyless APIs. Their raw data could be committed with attribution; BIS gives all 11 in one
query, so they were not fetched.

## Checks (method fixed in the plan; tables in `results/data-long-4.md`)

- **CPI.** BIS 12-month inflation against OECD MEI over 300-1,300 common months: correlation
  0.991-1.000, mean absolute gap 0.00-0.12 points except GB (0.51) and NO (0.20); the source of the UK gap
  (which index each splices in which years) was not examined. US: identical to BLS `CPIAUCNS`. Against JST's annual CPI:
  0.96-1.00 except DE (0.89; BIS annual DE starts 1924, after the hyperinflation; the
  residual years were not examined).
- **Policy rates** against the cached OECD 3-month rate: correlation 0.93-0.998, mean gap
  -0.5 to +0.1 points (policy below the 3-month rate, as expected), except DE 1960-1998 (0.88,
  -1.0 points: BIS's German series is the discount rate to 1978, the Lombard rate 1979-1984
  and the repo rate from 1985, so it is a different instrument in the early years).
- **Derived dividend yield.** French's annual Yld of row t matches the derived yield at
  December t-1 (correlation 0.87-0.99; at December t only 0.18-0.86), which fixes the timing:
  row t is formed at the end of December t-1 and is coded as public on 1 July of t. Mean gap
  +0.03 to +0.27 points (French averages ratios, the derived yield sums dividends over the end
  price). Against JST `eq_dp` (December of the same year), 1975-2020: JP 0.89, GB 0.92, SE 0.82,
  CH 0.74, DE, AU and NO 0.54-0.55. JST's US `eq_dp` is Shiller's December D/P (correlation
  1.000). The low three look like sample differences (JST takes its yields from published
  national indices, French computes them on his own firm sample), not a timing error, since
  the December t-1 alignment is worse for all of them; not examined further. The level
  differences are small (mean gaps within 0.55 points). A value or carry signal from French's
  yields should be checked against JST's on 1975-2020 before use.

## Caveats

- BIS CPI is today's vintage (rebased, occasionally revised), not what a trader saw; NSA CPI
  is rarely revised, so the effect is expected to be small (not measured). The query keeps
  nothing after 2025-09 on disk.
- AU and NZ CPI are quarterly: a monthly signal must use the quarter's value only from its
  `cpi-quarterly` availability date.
- French's sample is his own selection of firms (few in some countries in 1975-1985, e.g. NZ
  from 1988), in local currency; it is not an investable index.
- The French files on disk run to 2025-12; the parser cuts at 2025-10 and keeps the annual row
  2025 (December 2024 data).
- JST stops in 2020 and has no New Zealand.
- No earnings yield outside the US at monthly frequency; annual E/P from 1975 only.

## For the next lane (xs-century-2 or similar, own card)

- Currency value: `real_fx_series(cur)` (ln real exchange rate) for 9 currencies from 1971;
  the card fixes the lookback (AMP 2013 use the 5-year change) and the CPI lag
  (`lm.available("cpi-monthly")`: CPI of month m from the 1st of m+2).
- Equity value and carry across countries: `dividend_yield(cc)` monthly from 1975 (9 markets)
  plus US from Shiller; `french_ratios(cc)` for B/M or E/P annually; JST `eq_dp` for a
  1900-1975 annual extension. The equity returns themselves: French's country market returns
  (in the same files) or the OECD share price indices (price only, averaged).
- Inflation-adjusted bonds or real carry: BIS CPI with the cached long and short rates.

## Logged

No `tries.md` row (no return series computed). One line in `research/ideas.md`.
