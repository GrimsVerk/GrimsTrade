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
