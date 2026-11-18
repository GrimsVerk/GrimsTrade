# eu-1: does `tsmom12` keep its character on European UCITS ETFs, seen from euros?

Lane `eu-1` (WIDER), night of 2026-11-18. Research only, fake money. Branch `eu-1` from
`trend-tune`. Card: `cards/eu-1.md` (fixed before any strategy number).

**Why.** The owner lives in the Netherlands. US-domiciled ETFs (SPY, QQQ, GLD, TLT) have no EU
key information document (PRIIPs), so EU brokers do not sell them to retail clients: the live
book could not be copied by him. The question is whether the house rule, `tsmom12`, keeps its
character (Sharpe, worst loss, turnover, behaviour in crashes) on European-listed UCITS
ETFs/ETCs covering the same asset classes, measured in euros. A robustness check of a fixed rule
on a new universe, not a new selection.

## 1. Data

### Sources

- **UCITS ETFs/ETCs:** Yahoo's public chart API (the same keyless endpoint as `lib/fetch.py`),
  daily bars, raw and dividend-adjusted closes. Every line used is quoted in EUR (checked from
  the response's `currency` field).
- **USD per EUR:** the ECB euro reference rate (`data-api.ecb.europa.eu`, series
  `EXR/D.USD.EUR.SP00.A`, set around 14:15 CET), from 1999-01-04. FRED's graph CSV
  (`DEXUSEU`) timed out from this machine, so the ECB rate is the only one used. There is no
  euro before 1999, so nothing is converted before 1999-01-04.
- **US twins and coins in EUR:** the existing research cache (`lib/fetch.py`: Yahoo ETFs,
  Bitstamp/Coinbase coins in USD) divided by that day's rate (the last rate carried over ECB
  holidays). The same rate is applied to open, high, low and close: an approximation (the rate
  is fixed at 14:15 CET, US closes at 16:00 New York, coins at 00:00 UTC). Dutch crypto venues
  (e.g. Bitvavo) quote BTC and ETH in EUR directly; converted USD prices stand in for them.

Raw responses are saved under `<cache root>/eu-1/raw-<date>/` (cache root from the git-ignored
`research/macro.local.json`), read as data only (`json.loads`, `csv`) by
`uv run python -I research/lib/eu1_data.py build`, which writes the git-ignored CSVs in
`research/data/{bars,adj}/`. Nothing downloaded is committed.

Rerun on a fresh machine:

```sh
cp research/macro.local.json.example research/macro.local.json   # then set cache_root
uv run python research/lib/fetch.py                               # US ETFs and coins (USD)
uv run python -I research/lib/eu1_data.py fetch                   # UCITS lines + ECB rate
uv run python -I research/lib/eu1_data.py build                   # CSVs, EUR twins, splices
uv run --with numpy python research/lib/eu1_check.py              # sanity table
```

### The UCITS lines (Yahoo history; the fund's real launch is often earlier)

| Ours | Yahoo | Fund | Asset class | Twin of | Yahoo from | Used |
|---|---|---|---|---|---|---|
| IWDA | IWDA.AS | iShares Core MSCI World (Acc) | world equity | - | 2009-09-25 | wide set |
| SXR8 | SXR8.DE | iShares Core S&P 500 (Acc), EUR line of CSPX | US equity | SPY | 2010-11-01 (trimmed) | six, wide |
| SXRV | SXRV.DE | iShares Nasdaq 100 (Acc) | US tech equity | QQQ | 2010-11-01 (trimmed) | six |
| EXSA | EXSA.DE | iShares STOXX Europe 600 (DE) | European equity | - | 2008-01-02 | wide set |
| IQQE | IQQE.DE | iShares MSCI EM (Dist) | emerging equity | EEM | 2008-01-02 | wide set |
| IBGS | IBGS.AS | iShares Euro Govt Bond 1-3yr (Dist) | euro govts, short | - | 2008-01-02 | wide set |
| IBGL | IBGL.AS | iShares Euro Govt Bond 15-30yr (Dist) | euro govts, long | TLT (loosely) | 2008-01-02 | six, wide |
| 4GLD | 4GLD.DE | Xetra-Gold (physical ETC) | gold | GLD | 2009-11-13 | six, wide |
| EXXY | EXXY.DE | iShares Diversified Commodity Swap (DE) | broad commodities | DBC | 2008-01-02 | wide set |
| IS04 | IS04.DE | iShares $ Treasury 20+yr EUR Hedged (Dist) | US long Treasuries, hedged | TLT | 2015-04-01 | robustness |

Fetched but not used: EUNL (IWDA on Xetra), CSPX.AS (stale until 2011), EMIM/IS3N (Core MSCI EM
IMI, only from 2014; IQQE gives six more years), IBGM (7-10yr), VWRL (bad prints in June 2013),
EQQQ (Yahoo history unusable before 2009: 63% vol, a +53% day), MEUD (only from 2024 on
Yahoo), EXHE (behaves like a short bond fund, 2.9% vol: not the long one it was meant to be),
EWG2 (not on Yahoo). For a real book, EMIM is the cheaper EM fund and VWRL/IWDA the usual
world funds; they track the same indexes.

### Data problems found and how they were handled (before any strategy was run)

- SXR8 and SXRV: Yahoo's bars before 2010-11-01 are not EUR prices: both drop ~25% on
  2010-11-01 (the USD/EUR rate that day was ~1.39) on near-zero volume. Both start on
  2010-11-01 (`TRIM` in `eu1_data.py`). After that SXR8 tracks SPY in EUR to -0.2% a year
  (weekly correlation 0.90; the gap is the earlier European close) and SXRV tracks QQQ to -0.4%.
- Xetra lines repeat 2023-12-01's close on 2023-12-04..06 (zero volume): a Yahoo gap, kept as
  is (three days; a fill there would be at a stale open).
- Many lines have zero-volume days in their first years (thin Yahoo coverage), but no other
  stale runs or bad prints were found up to the train cut. Largest daily moves are all
  2020-03-12 or 2008 crash days.
- IBGL is not TLT: euro government bonds 15-30 years (Germany, France, Italy, Spain...), about
  10.6% vol against TLT-in-EUR's higher vol and a different rate cycle (weekly correlation with
  TLT in EUR 0.57). IS04 (US Treasuries 20+, hedged to EUR) is the closer twin but starts 2015;
  it is a robustness row.

Sanity table (coverage, gaps, largest move, buy-and-hold growth, tracking against the US twin
in EUR, all up to the train cut 2025-11-10): `results/eu-1-data.md`. Disclosure: this table
shows each line's buy-and-hold growth and volatility; it was seen before the card was written.
It contains no `tsmom12` or other strategy number.

### Splices (clearly marked `-S`)

The native UCITS histories start 2008-2010, so the native test covers 2012-2025. To see the
2000-02 and 2008 bear markets in euros, `<SYM>-S` series run the twin in EUR before the
listing's first Yahoo day, scaled to meet it there: SXR8-S (SPY before 2010-11-01), SXRV-S (QQQ),
4GLD-S (GLD before 2009-11-13), IBGL-S (TLT before 2008-01-02). Before 2008-2010 these are US
ETFs in euros, not European funds: for IBGL-S that means US Treasuries, not euro bonds. Splices
are robustness rows only; the verdict rests on the native window.
