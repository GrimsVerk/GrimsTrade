# eu-1: does `tsmom12` keep its character on European UCITS ETFs, seen from euros?

Lane `eu-1` (WIDER), night of 2026-11-18. Research only, fake money. Branch `eu-1` from
`trend-tune`. Card: `cards/eu-1.md` (fixed before any strategy number).

**Why.** For a retail investor in the Netherlands: US-domiciled ETFs (SPY, QQQ, GLD, TLT) have no EU
key information document (PRIIPs), so EU brokers do not sell them to retail clients: the live
book could not be copied by such an investor. The question is whether the house rule, `tsmom12`, keeps its
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

## 2. What was run

Card `cards/eu-1.md`, unchanged: `tsmom12` exactly as the house runs it (365-day return > 0
holds the equal slot, Fridays, next-open fills, cash at 0, total-return prices), on six books,
in window W = decisions 2012-01-02 .. 2025-11-09 (train end; the held-out year is untouched):
the live six in USD (`us6`), the same six converted to EUR (`us6-eur`), their UCITS copies in
EUR (`eu6`: SXR8, SXRV, 4GLD, IBGL, BTC and ETH in EUR), and a coin-free asset-class set in the
same three versions (`usw`: SPY, EFA, EEM, IEF, TLT, GLD, DBC; `euw`: SXR8, EXSA, IQQE, IBGS,
IBGL, 4GLD, EXXY). EUR books pay Dutch broker costs (ETFs 0.10% fee + 0.05% slippage a side);
US books the gym's. Plus costs, a hedged-Treasury bond slot, single slots, and two longer
windows. 44 rows in `tries.md` (idea `eu-1`), all `robustness` or `baseline`. Full tables:
`results/eu-1.md`; rerun `uv run --with numpy python research/lib/eu1.py`.

## 3. Results (window W, 2012-2025, each book in its own currency)

| Book | `tsmom12` Sharpe | EW Sharpe | `tsmom12` max DD | EW max DD | `tsmom12` turnover/yr |
|---|---:|---:|---:|---:|---:|
| us6 (USD, gym costs) | 1.37 | 1.32 | 36.5% | 47.0% | 2.8 |
| us6-eur (currency only) | 1.39 | 1.31 | 31.3% | 42.8% | 3.1 |
| **eu6 (UCITS, EUR, Dutch costs)** | **1.44** | 1.38 | **31.0%** | 43.0% | **3.1** |
| usw (USD, gym costs) | 0.63 | 0.67 | 11.1% | 18.7% | 3.0 |
| usw-eur (currency only) | 0.54 | 0.64 | 13.8% | 19.1% | 3.0 |
| **euw (UCITS, EUR, Dutch costs)** | **0.56** | 0.77 | **14.3%** | 19.8% | **2.9** |

Standard errors of every Sharpe here are about 0.27: no difference in this table is
statistically meaningful on 14 years. The tests are about character, not about winning.

**The card's tests.** Pair A (`eu6` vs `us6`): all four pass, **holds**. Sharpe gap to equal
weight +0.06 against +0.05; max drawdown 31.0% against 36.5%; turnover 3.1 against 2.8 (1.11x);
the crash pattern matches in 4 of 4 windows. Pair B (`euw` vs `usw`): **holds in part**.
Drawdown (14.3% vs 11.1%, still well under equal weight's 19.8%), turnover (0.96x) and crash
pattern (3 of 4) pass; return per risk fails: `tsmom12` trails equal weight by 0.21 in EUR
against 0.04 in USD.

**Where pair B's gap comes from.** About half is the currency: the same US funds in EUR already
trail by 0.10 (`usw-eur`). Most of the rest is cost: at the gym's costs `euw` scores 0.63 (gap
-0.14), at harsh costs 0.44. A 6%-vol book earning 3% a year notices 0.15% a side on ~3 round
trips a year; the coin books (20% vol) barely do (`eu6` 1.45 gym, 1.44 Dutch, 1.41 harsh).

**Slot by slot (section 5 of the results).** On the equity slots the filter costs more in EUR
than in USD: SXR8 0.70 filtered vs 0.97 held (SPY: 0.79 vs 0.91). The clearest case is 2022:
the dollar rose, so the S&P 500 held in EUR fell only 11% (SPY in USD 25%) and the filter saved
almost nothing (-10.9% vs -11.4%). In 2015-16, 2018-Q4 and 2020 the euro view made little
difference to the falls; the rest of the gap is whipsaw cost and noise (SE ~0.27). On euro long bonds the filter did its job:
IBGL 0.33 filtered vs 0.27 held, max drawdown 22% vs 44%, 2022 0% vs -34% (it was out). On
Xetra-Gold it cut the drawdown from 37% to 21% for the same Sharpe. Swapping IBGL for the
EUR-hedged long Treasury fund IS04 changes nothing (1.42 vs 1.44).

## 4. Crash behaviour in EUR (total return inside each window)

| Window | `tsmom12` eu6 | EW eu6 | `tsmom12` us6 (USD) | `tsmom12` euw | EW euw | `tsmom12` usw (USD) |
|---|---:|---:|---:|---:|---:|---:|
| 2011 euro crisis (2011-05-02..10-03) | +0.3% (spliced) | +4.4% | +0.3% | -4.9% (from 2009) | -5.5% | -6.2% |
| 2015-16 (2015-05-21..2016-02-11) | -1.0% | +6.5% | -7.8% | -8.0% | -14.5% | -1.1% |
| 2018-Q4 (2018-09-20..12-24) | -4.8% | -14.3% | -5.9% | -4.1% | -3.2% | -3.6% |
| 2020 covid (2020-02-19..03-23) | -23.8% | -24.6% | -21.8% | -11.7% | -18.8% | -8.3% |
| 2022 rate shock (2022-01-03..10-12) | -10.9% | -29.1% | -13.5% | +2.1% | -7.1% | -2.5% |

The same shape as in USD: the rule is out of the slow bear markets (2018-Q4, 2022: it was out of
euro long bonds before they fell 34%) and too slow for the covid crash, which it rode down with
everyone. In 2015-16 the coin books' equal weight gained (coins rose) while the rule was partly
out. On the spliced 2000-2025 six (US ETFs in EUR before 2008-10), the rule lost 30% in the
dot-com bust against 69% for equal weight and +1% against -17% in 2008, as the US six did.

## Verdict

**Character holds.** From a euro investor's view, the house rule on European UCITS funds
behaves like it does on the US book: about the same Sharpe (1.44 vs 1.37 on the six, 2012-2025),
a smaller worst loss than holding everything (31% vs 43%), about three round trips a year, out
of the slow bear markets and caught by the fast one. The live book can be copied with SXR8 (or
CSPX), SXRV, Xetra-Gold (4GLD) and IBGL, plus BTC and ETH in EUR.

One difference to know: in euros the filter on US stocks earned less (in 2022 the rising dollar
had already cushioned a euro holder's fall); and on a coin-free, low-volatility book Dutch broker
costs take a visible bite (-0.07 Sharpe). Neither changes the worst-loss role.

Caveats: Yahoo's UCITS histories start 2008-2010 (window W has no 2008); the coins dominate the
six's Sharpe; IBGL is euro government bonds, not Treasuries (IS04 gives the same result); US
fund numbers are gross of the 15% US dividend withholding a Dutch holder of a US fund would pay,
while Irish UCITS funds already carry their (lower) withholding in the price; the USD/EUR rate is
the ECB's 14:15 CET fix applied to all of a day's prices.

Held-out year: unspent (nothing was selected).
