# attention-peak: leave a coin once its attention epidemic has peaked

Field: epidemiology (SIR: an epidemic turns when new infections fall). It is mechanism P2 of
`wide-1.md` step 1 ("attention is the infection: a mania ends when new infections peak"),
which wide-1 parked: "three manias, all coins at once. Data is free (Wikimedia, from 2015-07)".
Written 2026-11-18, pushed 19:06 UTC (commit f25b507), run wide-3, before any test or number of this card, and before
any page-view number was downloaded or seen. Seen before: every earlier result in `tries.md`,
the coin price history in general terms (tops in 2017-12 and 2021, as public knowledge).

## Claim

A coin mania is an epidemic of attention. Price is carried by newly "infected" buyers; the
number of people reading about the coin for the first time is a proxy for them. Once attention
has surged and then turned down from its peak, the pool of new buyers is used up, and the price
has nothing left to carry it. Leaving the coin at that point beats `tsmom12`, which leaves only
once the 365-day return turns negative, often a year after the top.

## Why it might work

The data is outside price (no earlier rule here read it), public the next day, and the
mechanism predicts the timing (after the peak of attention), not just the level.

## Why it might not

- Few episodes: 2017-12, 2021 (two peaks), maybe 2024. Three or four exits decide the result,
  so a pass could be luck, as with the halving.
- Attention also surges in crashes (2020-03, 2022-05 and 2022-11 as far as I remember); the
  rule then exits after the fall, when the trend rule may already be out or the bottom is in.
- English Wikipedia is one audience among many, and its share of crypto attention may have
  fallen over time.

## Data (fixed before download)

- Wikimedia REST API, per-article page views, `en.wikipedia`, `all-access`, agent `user`,
  daily, 2015-07-01 to 2025-11-10 (the train cut; nothing later is requested). One request per
  title, no key; a generic user agent with no personal details. Script
  `lib/wide3_pageviews.py`, output in the git-ignored `research/data/pageviews/`.
- Titles: `Bitcoin` (BTC), `Ethereum` (ETH). Other coins: `Litecoin` (LTC),
  `Ripple_(payment_protocol)` plus `XRP_Ledger` (XRP; the article was renamed, the two are
  summed), `Bitcoin_Cash` (BCH), `Ethereum_Classic` (ETC), `Stellar_(payment_network)` (XLM),
  `Dash_(cryptocurrency)` (DASH). A title the API has no data for contributes nothing; a coin
  with no data at all is its twin, disclosed in the result.
- As of: the views of day D are used only by decisions after day D (decision on a Friday F
  uses views up to F-1).

## Rule (fixed, no fitted parameter)

- Weekly decisions on Friday's close. Base weights are `tsmom12`'s; ETFs are never touched.
- For each coin, with v = daily views up to F-1:
  - `surge`: the mean of the last 28 days is at least 3 times the median of the 365 days before
    those 28 (days F-393 .. F-29).
  - `past peak`: the mean of the last 7 days is below the highest 7-day mean ending on any day
    of the last 56 days.
  - **Out** if `surge` and `past peak`: the coin's slot is cash this week (not given to others).
    Otherwise the twin's weight. Less than 393 days of views: the twin's weight.
- Reading: during a rising epidemic the last week is the highest, so the coin is held; after the
  peak it is out until the 28-day mean falls back below 3 times the base (the epidemic is over)
  or attention makes a new 7-day high (a second wave).

## Variants (all that will be run)

1. `peak` (only variant): as above.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight; every out spell per coin (first and last Friday, the
coin's return over the spell, and whether the twin held it).

## Out-of-universe

Coins only: the 6 other coins as a book. ETFs and indexes have no coin: not applicable.

## Pass bar

The default in `protocol.md` for `peak` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 46 = 0.0022** (`wide-3.md`, step 1).
2. Eras counted from 2017-21 (the rule can first act in 2016-07, so the earlier eras are ties
   by construction): ahead in both, 2 of 2.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive, and positive on the one applicable out-of-universe set (other coins).
5. Beats equal weight on Sharpe.

Held-out year: once, `peak` only, only if all bars pass.

## My guess before any number

Chance it passes: 3%. Difference to the twin: -0.10 to +0.15 Sharpe.

## Result

See `results/attention-peak.md` once tested.
