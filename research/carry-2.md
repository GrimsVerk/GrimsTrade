# Carry 2: does short-1's premium carry hold on data it never saw?

Research run carry-2, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-carry-2.md`.
Branch `carry-2` (from `short-1`). Research only: fake money, public market-data endpoints only,
no change to the gym, the daily runner or the live strategies.

Question: short-1's one lead was a carry book on 30 surviving Binance perpetuals: long the third
with the lowest 7-day premium (or funding), short the third with the highest. Its direction was
chosen on the same data it was tested on. Does the same book, unchanged, earn on venues and coins
it never saw (other exchanges, Binance coins outside the 30, delisted contracts)?

## In plain words (results)

Not written yet: the card below was fixed before any new number was computed.

## Card (written 2026-11-13 ~08:30 UTC, before any new number)

This is a replication, not a search. Nothing below is tuned; every choice is short-1's
(`research/short-1.md`, card; code `research/lib/short1.py`) unless the new data forces a
substitute, and each substitute is fixed here.

### What was already seen (disclosure)

Short-1's tables for P30 and BTC/ETH (Binance, 2020-2025): `ls-premium` Sharpe 0.83 at 10 bps,
blend with `tsmom12` 1.25 vs 1.03 (p 0.096), not at 30 bps; `ls-funding` nearly the same book.
Breadth-1's long-only ICs on the same 30 pairs. Nothing on any other venue or coin. While
choosing venues, only endpoint availability was checked (does a public endpoint return funding
history and how far back), never a rate level or return.

### The books (sets the card is run on)

- **B-out: Binance USDT-M perpetuals outside short-1's 30**, every `*USDT` perpetual in Binance's
  public archive (`data.binance.vision`, which keeps delisted contracts), minus the 30 P30 coins.
  Quarterly contracts and non-USDT margins are excluded. Delisted coins stay in while they paid
  funding (this is the survivorship test).
- **B-all: all Binance USDT-M perpetuals** (B-out plus P30), reported, not a separate test.
- **Bybit: Bybit USDT perpetuals (linear)**, keyless v5 market endpoints. Live listings from
  `instruments-info`; delisted contracts are tried by name (every symbol in Binance's archive);
  whatever answers is kept.
- **Hyperliquid: Hyperliquid perpetuals** (USD-settled), keyless `info` endpoint, every coin in
  `meta` (it marks delisted coins but keeps them). History starts 2023-05, so with the 365-day
  rule it trades only from about 2024-05: a short test, reported with that caveat.
- **Pooled:** the daily returns of the venue books that exist on a day (B-out, Bybit,
  Hyperliquid), averaged with equal capital per venue (re-split daily at no cost, short-1's
  blend idealisation). Each venue ranks its own coins; coins are never ranked across venues
  (funding schedules and premium definitions differ).
- Not used: OKX (public funding history only covers the last 3 months), Bitget and dYdX (left
  out for the time budget, not for any result). Recorded in the download script.

### Prices, funding, premium (per venue)

- **Price:** the venue's own perpetual daily close (UTC day; short-1 used Binance spot as a
  stand-in, which is not available for most of these coins). Missing day: no return.
- **Volume:** the venue's own perpetual daily quote volume in USD (USDT).
- **Funding:** every funding event the venue publishes, booked exactly as short-1: return day
  `t` gets the events stamped in (00:00 of `t`, 00:00 of `t + 1`]; a position `w` earns
  `-w x rate`. Hyperliquid pays hourly; its rates are used as published.
- **Funding signal:** short-1's formula: per day, the mean rate of that day's events x 3, then the
  7-day mean (at least half the days present); `funding` = minus that, long low funding.
- **Premium signal:** the venue's premium index, short-1's formula: per day, the mean of the
  hourly premium closes (bars starting that day), then the 7-day mean; `premium` = minus that.
  Binance: `premiumIndexKlines` 1h (as short-1). Bybit: `premium-index-price-kline` 1h.
  Hyperliquid: the `premium` field of each hourly funding event (it is the hourly premium
  sample the rate is built from). A venue without premium history gets `ls-funding` only.

### Universe (as short-1)

A coin is tradable on day `t` if its perpetual paid funding within the two days up to `t`, it has
365 days of price history (here: its perp's own history), and its 30-day median daily quote
volume is at least 5M USD. Decisions start once 10 coins are tradable. Pre-filter for downloads
only: funding and premium are fetched only for symbols whose 30-day median volume ever reached
5M USD (a coin that never passes this cannot be tradable, so this changes nothing).

### Shapes and costs (as short-1)

- `ls-premium` (primary, short-1's lead) and `ls-funding`: weekly at Friday's close, rank the
  tradable coins with a finite signal, +0.5 of equity spread equally over the top third, -0.5 over
  the bottom third (gross 1, net 0). Weights drift until the next decision.
- Costs 10 bps a side on every unit of weight change (primary) and 30 bps (robustness), plus
  every funding event. Collateral earns 0.
- **Twin:** `tsmom12` long-only on the same venue's coins, 30 bps, no funding. Short-1's twin
  was on spot; spot bars do not exist here for most coins, so the perp close stands in for spot
  (the price gap is the small premium). `tsmom12` perp (10 bps + funding) and equal-weight perp
  are reported as baselines.
- **Blend:** 50% twin + 50% the `ls-` book, daily returns averaged (short-1's blend).
- Period: train only, decisions to 2025-11-09, no bar after 2025-11-10 loaded. Eras 2020-21 and
  2022-25 (short-1's), each year also shown.

### Pass bar for the replication (fixed now)

`ls-premium` **replicates** if all of these hold at 10 bps (short-1's cost):

1. **Pooled:** its Sharpe is above 0 with a one-sided stationary-bootstrap p < 0.10 (mean block
   20 days, 2,000 draws, against a zero series).
2. **Breadth of venues:** Sharpe above 0 on B-out AND on at least one of Bybit and Hyperliquid
   (Hyperliquid counts only with >= 1 year of decisions).
3. **Blend (short-1's bar 1) on the pooled set:** the pooled blend beats the pooled twin with
   p < 0.10.
4. **Eras:** pooled Sharpe above 0 in both eras with data.

Short-1's bar 5 (still ahead at 30 bps, blend p < 0.20) is reported for every set; passing 1-4
without it means "the carry is real but needs cheap execution". `ls-funding` is judged by the
same bars and reported next to it; because the two are nearly the same book, a pass of
`ls-funding` alone (without `ls-premium`) counts as a weak replication, not a pass.

**Held-out year** (2025-11-11 .. 2026-11-09): only if `ls-premium` replicates (1-4), once, on
the pooled set and on P30, at 10 and 30 bps; passes if the book's Sharpe is above 0 and the
blend is not behind the twin.

### Reported for every set

Sharpe, CAGR, max drawdown, worst week, per era and per year, funding per year, turnover,
correlation with the twin, blend Sharpe and p, the 30 bps rerun, the number of coins and
tradable coins per day, how many delisted coins ever entered the book, and the long and short
legs' Sharpe (short-1's legs diagnostic, kind `robustness`).

### Logging

Every run gets a row in `research/tries.md` when it runs (`variant` for `ls-premium` and
`ls-funding` per set, `baseline` for twins, `robustness` for 30 bps, B-all and legs).
Code: `scripts/fetch_carry2.py` (download), `research/lib/carry2.py` (books and run). Tables:
`research/results/carry-2.md`.

## Status

Card written. Next: download script, data, run.
