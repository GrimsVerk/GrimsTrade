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
