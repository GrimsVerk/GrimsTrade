# rebalance-pressure: lean against the month-end trades of balanced funds

Field: control theory (other people's feedback controllers: a known setpoint, a known schedule,
a correction proportional to the error). Finance source: Harvey, Mazzoleni, Melone 2025, "The
Unintended Consequences of Rebalancing" (from memory, not re-read; their signals and windows are
not copied, the rule below is built from the mechanism).
Written 2026-11-17 23:20 UTC, run wide-1, before any test. Seen before writing: the earlier
runs' results, including `month-end-liquidity` (the unconditional turn-of-month window: dead,
faded since 2014, never in TLT).

## Claim

Pension and balanced funds hold a fixed stock/bond mix and restore it around month end. When
stocks have beaten bonds during the month they must sell stocks and buy bonds in the last
sessions, and the other way round. So in the last five sessions of a month the month's leader
lags the month's loser. `month-end-liquidity` tested "everything rises at month end". This is a
different claim: *which* of the two is pushed depends on the month so far.

## Why it might work

The flow is mechanical (a mandate, not a view), its sign is known from public prices, and its
size is proportional to the gap. Trading it costs about 4 bps a round trip in ETFs.

## Why it might not

It is known (published 2025, and discussed by banks for years), so others may trade ahead of the
window. Month-end effects faded in our own test. In a long-only book only half a slot moves, so
even a real effect is a few tenths of a percent a year.

## Rule (fixed)

- Base book: `tsmom12` on the six assets, decided weekly. Stocks = SPY and QQQ; bonds = TLT.
- T = the last trading day of the month (trading calendar: dates only, known in advance). M = T-5.
- At the close of M: g = (log return of SPY since the last close of the previous month) minus
  (the same for TLT). Both must be eligible.
- If |g| >= 2%, the tilt is on for the five sessions T-4 .. T (decisions after the closes of
  M .. T-1; daily decisions in this window, an exception to the weekly rule). The leader is the
  side that rose more.
- Tilt: every base weight on the leader's side is halved. The freed weight is split equally
  among the assets on the other side that the base book holds; if it holds none, the freed
  weight stays in cash. The rule never holds an asset `tsmom12` does not hold.
- The decision after the close of T returns to the base book (fill at the open of T+1).

## Variants (all that will be run)

1. `me` (primary): as above.
2. `me-rebound`: as above, and for the first three sessions of the new month (decisions after
   the closes of T, T+1, T+2) the opposite tilt: the side that was bought at month end is
   halved and the freed weight goes to the month's leader. Tests the mechanism's second
   prediction, that the price pressure reverses.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight. Reported next to the backtest: the open-to-open return
of SPY minus TLT over sessions T-4 .. T, signed against g, for the months the rule acted, with a
t-test, for 2003-2013 and 2014-2025 separately; the same for sessions T+1 .. T+3 signed with g.

## Out-of-universe

One set applies: the 8 other ETFs as a `tsmom12` book with stocks = IWM, EFA, EEM, VNQ and
bonds = IEF, LQD; g = mean month-to-date log return of the eligible stocks minus that of the
eligible bonds; DBC and SLV untouched. Coins and indexes have no bond leg.

## Pass bar

The default in `protocol.md` for `me` against `tsmom12`, read as follows: eras are counted from
2000-09 on (before TLT is eligible the rule is its twin), 3 of 4 needed; bar 4 is read on the
one applicable set. Plus, stricter:

6. The signed spread return in the window (the event study above) is positive in both halves,
   2003-2013 and 2014-2025.

Held-out year: once, `me` only, only if all bars pass.

## Result

See `results/rebalance-pressure.md` once tested.
