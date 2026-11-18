# auction-concession: step aside while dealers make room for a Treasury auction

Field: queueing and inventory theory (a server with limited capacity facing a large batch on a
published date), the same thing ecologists call predator satiation. Finance source: Lou, Yan,
Zhang 2013, "Anticipated and Repeated Shocks in Liquid Markets" (2-, 5- and 10-year notes,
1980-2008; from memory, not re-read for this card).
Written 2026-11-17 23:20 UTC, run wide-1, before any test. Seen before writing: the auction
calendar only (dates and terms of every note and bond auction since 1979, no prices), and the
earlier runs' results (`month-end-liquidity`: no turn-of-month effect in TLT).

## Claim

Long Treasury prices dip in the trading days before an auction of long bonds and recover after
it, because the dealers who must absorb the new supply sell or hedge beforehand. A TLT holder who
is out for the five sessions that end with the auction day does better than one who stays in.

## Why it might work

The seller (the Treasury) does not care about the price, the date and size are published a week
ahead, and the buyers' balance sheets are limited. The cause is forced, not a habit. Published
size: yields about 2-3 bps higher into the auction; on TLT's duration (~17 years) that is
roughly 40 bps of price a month, against a normal five-day drift of under 10 bps.

## Why it might not

Published in 2013 on data to 2008; anyone can trade it with futures at almost no cost, so it
may be gone. Our evidence is for notes; 30-year bonds were not auctioned at all between 2001 and
2006. We fill at the open of the day after the auction and so miss the first hours of any
recovery. In the gym the rule only removes exposure: if the dip is smaller than TLT's normal
drift it loses.

## Data

`https://api.fiscaldata.treasury.gov/.../accounting/od/auctions_query` (public, keyless),
snapshot of 2026-11-17 under `<cache_root>/downloads/wide-1/treasury-auctions/`, parsed with
`python -I` by `lib/wide1_auctions.py` into `<cache_root>/derived/wide-1/auctions.csv`.
Qualifying auctions: nominal, fixed-rate (no TIPS, no floaters), new issues and reopenings alike.

- For TLT (20+ year Treasuries): bonds with an original term of 19 years or more (the 30-year
  and, from 2020, the 20-year).
- For IEF (7-10 year Treasuries): notes with an original term of 6 years 11 months to 10 years
  (the 7- and 10-year).

As-of rule: an auction exists for the rule only from its announcement date (announcement date
<= decision date). The trading calendar (dates only) is taken as known in advance.

## Rule (fixed)

A = the auction date. The asset's slot is **out for the five sessions A-4 .. A** and in
otherwise. That is: a decision after the close of any of the sessions A-5 .. A-1, with the
auction already announced, holds nothing in that asset; the decision after the close of A buys
back (fill at the open of A+1). Windows of several auctions simply add up. Decisions are daily
for this gate (an exception to the weekly rule, as in `month-end-liquidity`: the card needs
exact days).

## Variants (all that will be run)

1. `six` (primary): the `tsmom12` book on the six assets, decided weekly as always, where TLT's
   slot is additionally empty during the out sessions.
2. `tlt`: TLT alone, held except during the out sessions.

## Twin and baselines

`six`: twin `tsmom12`. `tlt`: twin `constant` (TLT at a constant weight equal to the rule's
average exposure: same risk, no timing); buy-and-hold TLT shown. Also reported: mean
open-to-open return per out session and per in session with a Welch t-test, before and after
2013-01-01.

## Out-of-universe

One set applies (no auctions for stocks, coins or indexes): the 8 other ETFs as a `tsmom12`
book with IEF's slot gated by the 7- and 10-year auctions, and IEF alone against its `constant`
twin. Both logged as `robustness`.

## Pass bar

The default in `protocol.md` for `six` against `tsmom12`, read as follows: eras are counted from
2000-09 on (before TLT exists the rule is its twin), 3 of 4 needed; bar 4 needs the ETF-set
book and IEF alone to both have the sign of the main difference. Plus, stricter:

6. `tlt` beats its `constant` twin on Sharpe with bootstrap p < 0.10.
7. From 2013-01-01 (after publication): `six` not behind `tsmom12`, `tlt` not behind `constant`.

Held-out year: once, `six` only, only if all bars pass.

## Result

See `results/auction-concession.md` once tested.
