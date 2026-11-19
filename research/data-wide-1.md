# Data wide 1: keyless sources that could carry F1/F2 doses

Research run data-wide-1, 2026-11-19. Branch `data-wide-1` (from `wide-11`), draft PR into
`wide-11`. Data survey only: no candidate written, no gate, no backtest, no return statistic,
no correlation with any price. Weather and climate data are out of scope (another lane).

**Status: skeleton, being filled.**

## Why

wide-11's filters ask for a dose that is **F1 not announced** (an unscheduled flow, or a
premium) and **F2 not price-driven** (the dose does not follow the asset's own prices at any
horizon up to a year). Most sources the project has read so far fail one of them: schedules
(Treasury auctions, Fed purchase schedules, index lists) fail F1; positioning, issuance and
attention (COT, stablecoin supply, pageviews) fail F2. This run looks for public keyless
series whose dose is set by something outside markets.

## Already in the project (not repeated)

From `docs/data-sources.md` on branch `data-search-1` and the wide/survey lanes: exchange
bars, funding and open interest, FRED/ALFRED, Treasury yield curve and auctions
(fiscaldata), NY Fed operations, CFTC COT, Cboe put/call, Ken French, Shiller, Coin Metrics,
blockchain.com hash rate, Fear & Greed, GDELT events (30 files probed), GFZ Kp/Ap, NHC
hurricane tracks, CPC ENSO, Wikimedia pageviews, DefiLlama stablecoins.

## Inventory

(filled below)

## Verified downloads

(filled below)

## Loaders

(filled below)

## For wide-13 (ideas only, nothing tested)

(filled below)
