# dealer-backlog: idle cash into the long bond after auctions that dealers had to absorb

Field: queueing theory (a server of last resort with a measured backlog) with Grossman and
Miller's liquidity-provision model (whoever absorbs an order imbalance is paid by the
reversal that follows, more for a larger imbalance). It is W9, added to wide-1's list by
wide-5 (`wide-1.md`, last section) and picked there by a choice rule written before any
number. Written 2026-11-18, run wide-5, before any test or number of this card.

Seen before: every earlier result in `tries.md`, including `auction-concession` (wide-1: TLT
dips into long-bond auctions, -34 bps at closes over the five sessions to a 30-year auction,
-15 bps at our fills; it recovers after) and the post-auction yield path in
`results/wide-1-yields.md` (sessions A+1 .. A+5 on average). From the new download only the row
count and per-year counts of filled `primary_dealer_accepted` (none before 2008, all from
2009). No dealer share has been computed or printed by me or, as far as `tries.md` and
`ideas.md` show, by any earlier run.

## Claim

Primary dealers must bid in every Treasury auction (their agreement with the New York Fed).
When end investors stay away, the dealers are left holding a large part of the new bond. They
are a server with limited balance sheet: the bonds sit in their inventory at a price
concession and are sold down over the following days, and the price recovers as they are.
**The larger the dealers' share of an auction relative to its usual level, the more long
bonds earn in the five sessions after it.**

## Why it might work

- The obligation to bid is structural, not a habit; the backlog is measured and published at
  1 pm on auction day, before the close at which the rule decides.
- The dose varies auction to auction (the dealer share has ranged widely as foreign and
  direct bidders came and went), so a slope can be tested, and the non-positive surprises are
  a free placebo.
- About 270 auctions of 20- and 30-year bonds since 2008 for TLT and about 210 of 10-year notes
  for IEF; fills at 4 bps a round trip; idle cash goes to TLT.
- As I remember, not opened in this run: Fleming and Rosenberg (NY Fed Staff Report 299, 2007)
  find that dealers take on positions at auctions and are paid for the inventory risk by price
  appreciation in the following days; Lou, Yan and Zhang (2013) find the post-auction recovery
  on average. Neither, as far as I remember, sorts auctions by the published dealer share at
  our fills.

## Why it might not

- A high dealer share may mean bad news about demand that is not temporary: prices then keep
  falling (an overhang, the opposite sign).
- Hedge funds and dealers pre-position; the recovery may be over by the next open.
- The gain is capped: idle cash is about a quarter of the book for five sessions after about
  two long auctions a month. A real +20 bps per event is roughly +0.5% a year on the book,
  +0.03 Sharpe: **the bar of p < 0.00179 cannot be met by a gain that small**; the event study
  is where the mechanism can show.

## Data

- Prices: the six assets and the 8 other ETFs, as every run.
- The Treasury's auction file (fiscaldata.treasury.gov `accounting/od/auctions_query`, public,
  keyless), notes and bonds, downloaded 2026-11-18 to `<cache_root>/downloads/wide-5/
  treasury-auctions/` with `cusip, security_type, security_term, original_security_term,
  inflation_index_security, floating_rate, reopening, announcemt_date, auction_date,
  issue_date, maturity_date, int_rate, high_yield, offering_amt, total_accepted,
  comp_accepted, primary_dealer_accepted, direct_bidder_accepted, indirect_bidder_accepted,
  soma_accepted, bid_to_cover_ratio`. Parsed with `python -I` by `lib/wide5_auctions.py` into
  `<cache_root>/derived/wide-5/auctions.csv`; the parser prints only row counts and date
  ranges.

## Dose (fixed)

Nominal fixed-rate auctions only (no TIPS, no floaters), originals and reopenings.

- Groups by `original_security_term` (its leading number of years): **long** = 20 years or
  more (the 20- and 30-year bonds, for TLT); **ten** = 10 years (for IEF).
- Dealer share `s` = `primary_dealer_accepted` / `comp_accepted` (competitive awards; the Fed's
  add-ons and non-competitive bids are not in it). Auctions with either field missing are
  dropped.
- Surprise `u` = `s` minus the median `s` of the previous 12 auctions of the same group (at
  least 6 needed, else the auction has no dose). In percentage points.
- Auction day A = `auction_date`, mapped to the bond ETF's session on that date (dropped if
  there is none).

## Rule (fixed, no fitted parameter)

- Base: `tsmom12` on the six assets, decided weekly as always.
- Overlay, decided daily (as `auction-concession`): at a decision after the close of sessions
  A .. A+4 of a **long** auction with **u > 0**, the idle cash (1 minus the sum of the base
  weights) is added to TLT, if TLT is eligible. With next-open fills TLT then holds the extra
  weight from the open of A+1 to the open of A+6. Overlapping windows simply join.

## Variants (all that will be run)

1. `backlog` (only variant): as above.
2. Placebo, logged as `robustness`, never selectable: `backlog-neg`, the same overlay after
   long auctions with u <= 0.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, `backlog-neg`, and an event study (descriptive, no
`tries.md` row):

- For TLT on long auctions and IEF on ten-year auctions: the log return from the open of A+1
  to the open of A+6 (our fills), minus the average 5-session open-to-open log return of the
  same ETF from 2008-07-01 to the end of train. Also, for reference, close of A to close of
  A+5.
- Mean, t and count for u > 0 and u <= 0; the dose-response slope (OLS of the excess, in bps,
  on `u`, in percentage points; HC1 t); each for all years, 2008-07 to 2016 and 2017 to the end
  of train.

## Out-of-universe

The 8 other ETFs as a `tsmom12` book with the same overlay into IEF after ten-year auctions.
Coins and indexes: not applicable (no Treasury bond in them).

## Pass bar

The default in `protocol.md` for `backlog` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 56 = 0.00179**: the list of 46 plus W1-W10.
2. Eras counted from 2000-09 (before TLT exists the rule is its twin; before 2008-07 it is too,
   which is accepted), ahead in at least 3 of 4.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive, and positive on the ETF set (the only out-of-universe set that applies).
5. Beats equal weight on Sharpe.
6. (card) `backlog` beats its placebo `backlog-neg` on Sharpe.

Reading of the event study, fixed now: **the mechanism is supported** only if, for TLT at our
fills, (a) the dose-response slope is positive with t >= 2, (b) the mean after u > 0 is above
the mean after u <= 0, and (c) the slope is positive in both halves. Either way it is
evidence, not a pass.

Held-out year: once, `backlog` only, only if all bars pass.

## My guess before any number

Chance it passes: 2%. Difference to the twin: -0.01 to +0.02 Sharpe. TLT excess after u > 0:
-10 to +25 bps; slope t -1 to +2. If the sign comes out negative, that is the overhang story,
which this card does not trade.

## Result

See `results/dealer-backlog.md` once tested.
