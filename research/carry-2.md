# Carry 2: does short-1's premium carry hold on data it never saw?

Research run carry-2, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-carry-2.md`.
Branch `carry-2` (from `short-1`). Research only: fake money, public market-data endpoints only,
no change to the gym, the daily runner or the live strategies.

Question: short-1's one lead was a carry book on 30 surviving Binance perpetuals: long the third
with the lowest 7-day premium (or funding), short the third with the highest. Its direction was
chosen on the same data it was tested on. Does the same book, unchanged, earn on venues and coins
it never saw (other exchanges, Binance coins outside the 30, delisted contracts)?

## In plain words (results, 2026-11-13)

**Partly. The carry shows up on every venue and coin set it never saw, but it is smaller than
on short-1's 30 coins, it is only clear in the funding version, and it does not survive
30 bps a side.** By the card's own words that is a *weak replication*: `ls-funding` passes all
four bars, `ls-premium` (the primary, short-1's lead) passes two of four. The held-out year
stays unspent (the card allows it only if `ls-premium` replicates). Tables:
`results/carry-2.md`; 66 rows in `tries.md`.

| Set (10 bps + funding) | Years | Coins held | `ls-premium` Sharpe (p>0) | `ls-funding` Sharpe (p>0) | Twin `tsmom12` |
|---|---:|---:|---:|---:|---:|
| short-1 P30 (spot closes, in-sample) | 5.7 | 30 | 0.83 | 0.78 | 1.03 |
| **Pooled new data** (equal capital per venue) | 4.7 | ~550 | 0.44 (0.15) | **0.69 (0.04)** | 0.20 |
| Binance outside the 30, delisted included | 4.7 | 273 | 0.17 (0.35) | 0.57 (0.07) | 0.07 |
| Bybit (live contracts only) | 3.5 | 215 | 0.73 (0.08) | 0.31 (0.26) | 0.20 |
| Hyperliquid (from 2024-06 in effect) | 2.4 | 58 | 0.28 (0.32) | 0.47 (0.21) | 0.52 |
| Pooled at 30 bps | 4.7 | | -0.12 | 0.09 | |

- **The sign holds everywhere.** Both books are positive on all three new sets at 10 bps, in
  both eras of the pooled set, and nearly uncorrelated with the long-only trend (-0.1 to -0.3).
  The pooled funding book made 9.8% a year with a 19% max drawdown and a -10% worst week; half
  of equity in it lifted the pooled twin from 0.20 to 0.37 (p 0.04) and cut its drawdown from 72%
  to 41%.
- **But it is weaker than the lead.** On Binance's other 273 coins the premium book is close to
  nothing (0.17); the funding book is 0.57. The premium book's best venue is Bybit (0.73), the
  funding book's is Binance. Short-1's 30 large coins are where carry works best: rerun on their
  perp closes (robustness) they give 1.38 / 1.10, and all 588 Binance coins together 0.81 / 1.17.
  So the effect is real but concentrated in larger, more liquid coins, and short-1's sample was
  a flattering one.
- **Costs decide it.** The book turns over ~42 times a year. At 30 bps a side (a retail account)
  every new set is at or below zero. It needs execution at about 10 bps a side or less (maker
  orders or a fee tier), or a slower rule, which would be a new card.
- **Where the money comes from.** On Binance's other coins both legs lose on price (the long
  third of cheap-funding coins fell ~10% a year, the short third rose a little less than the
  market), and the book's gain is the funding it collects, ~9% of equity a year (the short leg
  receives ~7%). It is a funding harvest with the market beta hedged out, not a price signal.
- **Survivorship.** 16 of the 273 Binance coins it held were delisted later in train, and 4 of
  58 on Hyperliquid; they are in the numbers. Bybit served no delisted contracts, so that set is
  survivors only (which, as short-1 noted, hurts a short book more than it helps).
- **How sure.** Fairly sure the funding carry exists beyond short-1's coins at low cost: positive
  on every set, pooled p 0.04, hundreds of coins, three venues, delisted coins included. Not sure
  of its size: two signals were scored on three sets (the pass is the better of two nearly equal
  books), the venues are not independent (the same coins, the same 2021-2025 market, one bull run
  and one winter), Bybit has 3.5 years and Hyperliquid 2.4. Sure that it does not pay at 30 bps.

### What this means

1. **Nothing to change in the paper system.** The long-only BTC/ETH trend on spot (Sharpe 1.19
   in short-1) is still far ahead of anything here; the twin on these wide coin sets is poor
   (0.07-0.52), so the blend gains are gains over a bad long-only book.
2. **A carry sleeve is plausible only with cheap execution.** If the owner ever wants one, the
   next card should be about costs, not signals: what a 10 bps fill really costs on the 100-odd
   smallest of these perps (spread, depth), and whether a slower rebalance (every two or four
   weeks, fixed before any number) keeps the funding while cutting turnover. The funding version,
   not the premium version, is the one with out-of-venue evidence.
3. **The held-out year** (2025-11 .. 2026-11) is still clean for both books. A new card may spend
   it once on pooled `ls-funding` at 10 bps; this card's rule did not allow it.

### What the gym would need if it held (described, not built)

Short-1's list (signed weights with a gross limit, funding as a cash flow every event, margin and
liquidation), plus: a wide perp universe per venue (100+ coins) with point-in-time listing and
delisting; the perp's own closes rather than spot (on the 30 coins the perp closes add ~0.5
Sharpe to the premium book, because the book earns the premium's convergence); funding and
premium feeds per venue (Binance archive, Bybit v5, Hyperliquid info are all keyless);
a cost model by coin size (the 10 vs 30 bps gap is the whole result); and a scoreboard that
shows funding received next to price P&L. Fake money only: nothing would place an order.

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

### Disclosures (2026-11-13)

- The card was committed and pushed (commit "carry-2: card") before the download script existed;
  its "~08:30 UTC" stamp is approximate (the commit time is the record).
- One logged run (`carry2.py --log --legs`), no rerun, nothing tuned, bars unchanged.
- Added beyond the card's list, as robustness only: `B-P30 (perp closes)`, short-1's 30 coins on
  their perp closes, to show what the price substitution does.
- Hyperliquid funding was fetched only from each coin's day 350 (its rate limit allows ~30 pages
  a minute); the card cannot use earlier funding (365-day rule), so no number changes. Its
  volume is coin volume x daily close.
- Bybit: delisted Binance names were tried; Bybit answered for none, so Bybit is live contracts
  only. Four new 2025 listings hit the rate limit once and were refetched.
- Binance's archive has perp klines from 2020-01, so B-out trades from 2021-02. Binance's
  monthly 2025-11 files hold held-out days; the panels drop every bar after 2025-11-10 on load,
  and no held-out number was computed.
- Pooled funding and turnover are not pooled (shown per venue).
- The daily close is the last trade of the UTC day; for small coins it carries some bid-ask
  bounce, which a weekly book mostly averages out. Not measured.

## Status (2026-11-13 ~10:00 UTC)

**Done:** card; `scripts/fetch_carry2.py` (Binance archive 588 perps after the volume
pre-filter, Bybit 392, Hyperliquid 58; manifest lines in the cache); `research/lib/carry2.py`
and `carry2_panel.py` (test `tests/test_carry2.py`); the logged run; `results/carry-2.md`; this
write-up. Draft PR `carry-2` -> `short-1`.

**Doing:** nothing. No process left running.

**Next (owner's choice, not started):** a cost card (real fill costs on small perps, a slower
rebalance fixed in advance), and/or a held-out-only card for pooled `ls-funding`. Neither
matters for the paper system while it stays long-only BTC/ETH on spot.

Reproduce: `uv run python -I scripts/fetch_carry2.py binance|bybit|hyperliquid` (resumable),
then `uv run python -I research/lib/carry2.py` (add `--log --legs` to write `tries.md` rows:
done once already). Cache root from `research/macro.local.json`; panels under
`<cache_root>/derived/carry-2/`.
