# Data long 1: free long histories for the bond, gold and risky slots

Lane `data-long-1`, 2026-11-18. Research only: no data wired, no raw data committed.

Problem: the six-asset book's bond and gold slots start ~2002, so worst-loss questions (PR #43
trend-where, PR #37 trend-1926) rest on 2022 alone. Goal: free, keyless, account-free histories
that start before 2002, ideally before 1970.

"Verified" = the URL answered HTTP 200 from this machine on 2026-11-18 (curl, ~11:13 UTC), file
type and size checked. Spans and columns are from the source's own documentation; where a span is
marked (doc) it was not yet read from the file header.

## Table

| Source | URL | Series | Span | Freq | TR or price | Licence / terms | Verified |
|---|---|---|---|---|---|---|---|
| Damodaran, Historical Returns | https://pages.stern.nyu.edu/~adamodar/pc/datasets/histretSP.xls (page: .../New_Home_Page/datafile/histretSP.html) | S&P 500 TR, 3-mo T-bill, 10y US T-bond TR, Baa corp bond TR, real estate, **gold** | 1928-2025 (doc) | annual | total return (bonds), price (gold) | free to use, cite the source; no formal licence | yes (xls, 528 KB) |
| Shiller, Irrational Exuberance data | http://www.econ.yale.edu/~shiller/data/ie_data.xls (also shillerdata.com) | S&P price, dividend, CPI, GS10 long rate, CAPE, real total bond return | 1871-now (doc) | monthly | yield; file also carries a bond total-return index built from GS10 | free, academic; cite | yes (xls, 1.6 MB) |
| Jorda-Schularick-Taylor Macrohistory, R6 | https://www.macrohistory.net/app/download/9834512469/JSTdatasetR6.xlsx | `bond_tr`, `bill_rate`, `eq_tr`, `housing_tr`, `ltrate`, CPI, 18 countries incl. USA | 1870-2020 (doc) | annual | total return | CC BY-NC-SA 4.0 (non-commercial; fine for fake-money research, cite) | yes (xlsx, 1.1 MB) |
| NBER Macrohistory, ch. 13 | https://data.nber.org/databases/macrohistory/rectdata/13/m13033a.dat (index: nber.org/research/data/nber-macrohistory-database) | long-term US bond yields (ch. 13 interest rates), many series | ~1857-1960s (doc, series-dependent) | monthly | yield | public, cite NBER | yes (.dat, 13 KB) |
| Ken French Data Library | https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html | US equity factors, Rf (1-mo T-bill) | 1926-now | monthly/daily | total return (equity factors, bill) | free, cite; **no long bond or gold** | yes (html) |
| Fed H.15 (Data Download Program) | https://www.federalreserve.gov/datadownload/Choose.aspx?rel=H15 | constant-maturity Treasury yields (10y from 1962, 20y, 30y from 1977) | 1953/1962-now | daily/monthly | yield (rebuild TR from yield + duration) | US public domain | yes (html) |
| FRED csv (no key) | https://fred.stlouisfed.org/graph/fredgraph.csv?id=GS10 ; `LTGOVTBD` (long govt bond yield 1925-2000); `M1333BUSM156NNBR` (NBER long bond yield); `PPIACO` (all-commodity PPI 1913-); `IRLTLT01USM156N` | yields, commodity price index | 1913/1925-now (doc) | monthly | yield / price index | public domain mostly (check per series); the JSON **API** needs a free key (not signed up) | **no**: curl timed out (000) from here, 5 tries; retry or use browser |
| LBMA gold price | https://www.lbma.org.uk/prices-and-data/precious-metal-prices | LBMA Gold PM/AM | 1968-now | daily | price | page free to view; bulk/historic download is licensed via ICE/LBMA (paid, price on request) | page yes, data download not checked |
| World Gold Council Goldhub | https://www.gold.org/goldhub/data/gold-prices | gold price, many currencies | 1978-now daily, 1971 monthly-ish (doc) | daily | price | free with a **Goldhub account** (excluded: no accounts) | page yes |
| MeasuringWorth gold | https://www.measuringworth.com/datasets/gold/ | US/UK gold price | 1257-now (US from 1786) | annual | price | free for research, cite; no bulk API | yes (html form) |
| datahub.io core/gold-prices | https://datahub.io/core/gold-prices | monthly gold USD (from Bundesbank/World Bank) | 1833-now (doc) | monthly | price | ODC PDDL (public domain) | yes (html) |
| Bank of England "A millennium of macroeconomic data" | https://www.bankofengland.co.uk/statistics/research-datasets | UK consols yield, gilt yields, commodity prices, many UK series | 1200s-2016 | annual/monthly | yield / price | Open Government Licence | page yes |

Paid, listed only: Ibbotson/Morningstar SBBI long-term govt bond TR 1926-now (SBBI yearbook,
~USD 200-300/yr edition); Global Financial Data (subscription, price on request, thousands/yr);
LBMA/ICE historic bulk feed (licensed, price on request); Bloomberg/Refinitiv (enterprise).

## Risky (commodity / crypto-like) slot

Nothing crypto exists before 2009. Proxies with long free history:
- Gold itself (Damodaran 1928-, datahub 1833-): but the US gold price was fixed until 1971, so
  pre-1971 gold is near-flat and says nothing about drawdowns. Usable span for gold risk is 1971+.
- FRED `PPIACO` all-commodity price index 1913- (price, no roll/collateral return) once FRED is
  reachable; JST has no commodity series.
- Equity-like risky proxies with real drawdowns: Ken French small-cap / momentum deciles 1926-,
  JST `housing_tr` 1870-. These are a stress stand-in, not the same asset.

## Caveats

- Bond total return before 1953 rests on few, illiquid long issues; Damodaran's 10y TR is built
  from the yield with a constant-maturity bond formula, Shiller's likewise from GS10. Fine for
  annual worst-loss questions, not for daily trend signals.
- Annual series (Damodaran, JST) cap what a monthly trend rule can test; Shiller (monthly 1871-)
  is the only free monthly long-bond series confirmed reachable here.
- Gold pre-1971 is a fixed price: do not count 1934-1971 as "gold history" for risk.

## Recommendation: wire first

1. **Shiller `ie_data.xls`**: monthly 1871-now, GS10 yield plus a bond TR column. Gives the bond
   slot ~150 years monthly, including 1940-1981 (the long bond bear market, the real worst case,
   far worse than 2022 in real terms). One file, no key, reachable.
2. **Damodaran `histretSP.xls`**: annual 1928-now for 10y T-bond TR, T-bill, Baa and gold; a
   cross-check for (1) and the only one-file free gold+bond TR table. Use gold only from 1971.
3. **datahub gold-prices (monthly)** for a monthly gold slot 1971-now, PDDL licence.
4. JST R6 later, for non-US bond crashes (Germany 1923, Japan 1940s), if the owner wants
   out-of-sample countries; mind the NC licence.

Loader shape (for the next lane, not built): fetch into the gitignored cache only, parse with
`python -I` outside the repo first, record source URL + download date + sha256 in the cache index.
