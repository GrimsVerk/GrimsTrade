# Data wide 2: keyless sources that add independent episodes

Lane `data-wide-2`, 2026-11-25 (night, UTC). Branch `data-wide-2`. Data survey only: no
strategy, no backtest, no return statistic of any rule. Keyless public data only; no accounts,
keys or sign-ups; paid sources listed with their price only.

## Plan (written and pushed before any probe)

Goal: rank keyless public data sets by how many **new independent market-years** (and falls of
25% or more) they add to the project's tests, beyond what is already cached or scored:
Shiller US 1871-; NBER Macrohistory ch. XI (GB, DE, FR stocks; e4-indep-1); French country
files 1975-; JST R6 annual; data-long-3 (US bonds, 9 foreign 10y, 9 FX, PPI commodities,
Pink Sheet); data-long-4 (BIS CPI, policy rates); BoE "millennium" monthly sheet and Norges
Bank monthly stock index 1914-2001 (both cached by jst-autocorr-2 for description only);
crypto 1m bars from Binance, Bybit, Bitstamp, Bitfinex, Coinbase, Hyperliquid, Deribit.

Counting rule (fixed now): a market-year is independent when its series is a market (country,
asset or commodity) and a year that no scored series of the same asset class already covers.
A "fall" is a peak-to-trough decline of 25% or more in the monthly level, counted once per
episode (the level must recover to a new high, or the series end, before the next one counts).

Targets: monthly pre-1960 non-US stock, bond and commodity prices; emerging-market indices with
long free history; long monthly commodity spot or futures series; free bulk crypto intraday or
order-book archives. For each: URL, licence or terms, frequency, span, number of series,
whether a polite script fetch works, size. Fetch and cache only the top few that are clearly
allowed (total < 3 GB), with a loader in `research/lib/` and an offline test on a fixture.

## Probe log (in progress, 2026-11-25 UTC)

- 21:20 AQR "Commodities for the Long Run" (index level, monthly 1877-02 on): 200, keyless xlsx,
  aggregate portfolios only (equal-weight and long/short), no single commodities.
- 21:22 NBER Macrohistory chapter pages read (www.nber.org allows it). **data.nber.org's
  robots.txt is `Disallow: /` for every agent**: no scripted fetch of the .dat files from this
  lane (manual download only). FRED and ALFRED (which mirror many NBER series) reset the
  connection from this machine tonight (HTTP/2 reset, then time-outs).
- 21:25 Yale ICF (som.yale.edu, robots allow `/sites/default/files`, crawl delay 10 s, terms:
  academic research only, no redistribution, cite): St Petersburg and NYSE monthly indices,
  NYSE index 1815-1925, London IMM clean file fetched (10 MB zip).
- 21:28 OECD SDMX API: Cloudflare challenge (403) for a script; DBnomics mirror answers keyless.
- 21:30 Norges Bank HMS (robots allow, crawl delay 5 s), SNB historical series (allow),
  Riksbank (robots disallow `*.xls`: the stock and exchange-rate sheets are .xls, manual only).
