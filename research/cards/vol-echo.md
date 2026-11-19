# vol-echo: the day a shock leaves other people's volatility window

Field: signal processing (the "ghost" a boxcar filter produces when a spike leaves its window)
crossed with control theory (funds that steer exposure to a volatility target are feedback
controllers; their filter's memory makes part of their trading predictable). No paper is known
to me that tests this; the story is told by bank strategy desks.
Written 2026-11-17 23:20 UTC, run wide-1, before any test. Seen before writing: the earlier
runs' results (`dip-rsi2`, `vol-target`, `month-end-liquidity`).

## Claim

Volatility-control funds, risk-parity funds and many structured products size their stock
holdings as (target volatility) / (realised volatility over the last 1 or 3 months). A day with
a very large move raises that measure for exactly as long as it stays in the window. On the day
it drops out, measured volatility falls by a known amount and these funds must buy, whatever
the news. That date is known 21 (or 63) trading days ahead. Stocks should earn more than usual
on the roll-off day and the two days after.

## Why it might work

The buying is forced by a formula and its date is public arithmetic. It did not exist before
such funds became large (after 2008), which gives a placebo: the same rule on 1962-2009 should
show nothing.

## Why it might not

Many funds use exponentially weighted volatility, which has no ghost. A plausible flow moves
the index by perhaps 10 bps per event, which a few hundred events can barely show against
daily noise of 100 bps or more. Anyone can compute the date, so the effect may be traded
before it. The rule is in the market only a small part of the time.

## Rule (fixed)

For one asset, with r_k its daily close-to-close log returns and t the last closed bar:

- Window W_t = the last n returns r_(t-n+1) .. r_t. The return that leaves at the next close is
  r_(t-n+1). Its share of the window's variance: s_t = r_(t-n+1)^2 / (sum of r^2 over W_t).
- Trigger at t if s_t >= theta. Then R = t+1 is a roll-off day.
- Hold the asset for the sessions R, R+1, R+2 (bought at the open of R, sold at the open of
  R+3): the decision after the close of t is "in" if a trigger occurred at t, t-1 or t-2. Else
  cash. Daily decisions (an exception to the weekly rule, as in `month-end-liquidity`).

## Variants (all that will be run)

1. `echo21` (primary): n = 21, theta = 0.20 (one day that is a fifth of the month's variance:
   measured 21-day volatility falls by about 10% when it leaves).
2. `echo63`: n = 63, theta = 0.10 (measured 63-day volatility falls by about 5%).

Each on SPY and QQQ, alone.

## Twin and baselines

Twin `constant`: the same asset at a constant weight equal to the rule's average exposure.
Buy-and-hold shown. Reported: mean open-to-open return per day held and per day not held, with
a Welch t-test, before and after 2010-01-01 (the start of the volatility-control era).

## Out-of-universe

Two sets (`echo21` only): other stock ETFs (IWM, EFA, EEM) and the foreign indexes (Nikkei,
FTSE, DAX). Placebo, reported but not part of the bar: the S&P 500 index 1962-1993 and the
pre-2010 part of every series. If the placebo shows the same effect as 2010-2025, the mechanism
is not what earns it, whatever the Sharpe says.

## Pass bar (the shape of `month-end-liquidity`'s, since the rule is a single-asset timing rule)

1. `echo21` beats its `constant` twin on Sharpe with bootstrap p < 0.10 on SPY and QQQ both.
3. Max drawdown not more than 5 points worse than the twin's.
4. Same sign in both out-of-universe sets.
5. Sharpe above buy-and-hold of the same asset, SPY and QQQ.
6. From 2010-01-01: not behind the twin, SPY and QQQ.

(Bar 2, eras, is read from the tables.) Held-out year: once, `echo21` on SPY, only if all pass.

## Result

See `results/vol-echo.md` once tested.
