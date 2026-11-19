# contagion-catchup: buy the assets a shock has not reached yet

Field: epidemiology (an SIR-type infection spreading over a contact network) with the maths of
diffusion on a graph. Finance relatives: lead-lag and "network momentum" papers (Pu, Roberts,
Zohren 2023, from memory); none tested in this lab.
Written 2026-11-17 23:20 UTC, run wide-1, before any test. Seen before writing: breadth-1's
33-market table (own one-week momentum slightly negative, nothing passes) and rl-3's ceiling (a
weekly tilt on six assets needs IC 0.10).

## Claim

A price shock spreads between related assets like an infection between contacts: fast, but not
at once. In a week in which an asset's close relatives have moved and the asset itself has not
(it is "susceptible"), it catches up the week after. Assets that already moved with their
relatives are "recovered": nothing more to expect.

## Why it might work

Slow diffusion of information across related markets is documented for stocks and futures. The
21 ETFs used here close at the same minute, so a lead seen at the close is real, not an artefact
of clocks, and trading them costs 4 bps a round trip.

## Why it might not

These are among the most liquid instruments in the world; a one-week lag between them should
not exist. Half of the signal is "the asset's own week reverses", and our own tables say
one-week reversal is weak. Ranking by a weak signal concentrates the book in a third of the
assets.

## Book

The 21 US-listed ETFs in the cache: SPY, QQQ, TLT, GLD; IWM, EFA, EEM, IEF, LQD, VNQ, DBC, SLV;
XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLB, XLU. Total-return bars, gym costs (2 bps a side), next
open fills, through `gym.simulate`. An ETF is eligible after a year of bars. The test starts on
the first Friday with at least 10 eligible ETFs.

The six live assets are **not** the book: they hold only two pairs of relatives, and coin bars
close 21 hours before ETF bars at the decision, so "has not moved yet" would be a clock
artefact. A pass here would mean "the equity and bond slots could be tilted baskets", an owner's
decision; it would not change the six-asset rule by itself.

## Rule (fixed)

Every Friday, from closes visible at the decision, for each eligible ETF i:

- z_i = its log return over the last 7 calendar days divided by (its EWMA volatility, 60-bar
  half-life, annualised, times sqrt(7/365)), clipped to +-5 (the protocol's `z(7)`).
- w_ij = the correlation of the daily log returns of i and j over the last 252 trading days,
  set to 0 if negative; w_ii = 0.
- Infection pressure: lambda_i = sum_j w_ij z_j / sum_j w_ij (the correlation-weighted mean move
  of its relatives; 0 if it has none).
- Signal `catchup_i` = lambda_i - z_i: what the relatives did minus what the asset did.

Books (breadth-1's shapes, so the tables compare):

- `TS` (the twin): each eligible ETF has slot 1/N, held while its 365-day return is positive.
- `TOP-TS(signal)`: the k = round(N/3) eligible ETFs with the highest signal each have slot 1/k,
  held while their own 365-day return is positive, else that slot is cash.

## Variants (all that will be run)

1. `catchup` (primary): TOP-TS on `catchup`.
2. `nbr`: TOP-TS on lambda_i alone (the relatives' move, without subtracting the asset's own).

## Twin and baselines

Twin `TS`. Plain twin of the idea itself: `rev7`, TOP-TS on -z_i (plain one-week reversal, no
network). Also `EW` (equal weight of the eligible ETFs). Reported: the weekly rank IC of each
signal against the return from the next open to the open a week later (mean, t, both halves).

## Out-of-universe

One set applies: coins, which also close at one common time. BTC, ETH and the protocol's six
other coins (LTC, XRP, BCH, ETC, XLM, DASH) through the gym at 30 bps a side, from the first
Friday with at least 6 eligible coins. The four stock indexes are left out: they close hours
apart, so a "lag" between them is the clock, and Yahoo's index opens are stale.

## Pass bar (the card's own, because the book is not the six assets; each line at least as strict as the default)

1. `catchup` beats `TS` on Sharpe on the 21-ETF book, paired bootstrap p < 0.10.
2. Ahead of `TS` in at least 3 of the 4 eras with data (2000-09, 2010-16, 2017-21, 2022-25).
3. Max drawdown not more than 5 points worse than `TS`.
4. Same sign on the coin set after 30 bps costs.
5. Beats `EW` of the 21 ETFs on Sharpe.
6. Beats `rev7` on Sharpe (the network must add something to plain reversal).
7. Weekly rank IC of `catchup`: t >= 3 and positive in both halves of the sample.

Held-out year: once, `catchup` only, only if all bars pass.

## Result

See `results/contagion-catchup.md` once tested.
