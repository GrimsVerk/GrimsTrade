# yt-1: eight rules from trading YouTube (harvest 1), one card each

Written 2026-11-13 ~05:45 UTC (commit 8ac6754; the time first written here, 06:10, was a slip, corrected after the tests), run ideas-1, **before any test of these rules and before any of
their indicators was computed or plotted**. Brief: `chief-of-staff/briefs/grimstrade-ideas-1.md`.
Source list (our own words, video ids): `yt-harvest-1/docs/ideas/grimstrade-ideas.md`, items
#1, #2, #3, #7, #8, #9, #10, #12. Seen before: every result of runs 1-3, macro-1, rl-1 and rl-2
(nothing has beaten `tsmom12`; macro gates on top of it all failed; the halving window "worked"
in-sample only), and the public history of the episodes the videos name.

Items not carded: #4 (monthly RSI against a hand-drawn line) and #5 (diminishing cycle returns,
3 points) are vague; #6 (halving cycle) was carded and tested in macro-1 (`cards/halving.md`);
#11 (debasement hurdle) is an allocation claim, not in this batch's list; the hype list has no
rules. #12 as stated (loud critics) has no data; it is tested through the stand-in the note
names, the crypto Fear & Greed index.

## Shared rules (all eight cards)

Everything in `protocol.md` applies, the macro as-of rule included. Weekly decisions on Friday.

**Gate shape.** A card defines when an asset is *hostile*. `<card>-and` (primary unless the card
says otherwise): the asset's `tsmom12` slot is held only while it is not hostile. `<card>-alone`:
the asset's equal-weight slot is held while it is not hostile, no trend test (does the signal
carry information on its own?). Reported, not judged.

**Which assets a gate acts on.** As in macro-1, safe assets (TLT, GLD, IEF, LQD) keep their
`tsmom12` slot, except where a card names one. "Stocks" means every asset that is not a coin, not
a safe asset and not a commodity fund (DBC, SLV): SPY, QQQ, IWM, EFA, EEM, VNQ and the four
indexes. A gate never acts on an asset the card does not name; such assets keep `tsmom12`.

**Causality.** Price signals of an asset are computed from that asset's bars visible at the
decision only (the harness view). "Weekly close" = the last visible daily close of each ISO week;
"monthly close" = the last close of each *completed* calendar month (a month counts as completed
from the first bar of the next month). Macro and sentiment series are used from the day after
they became public (`lib/macro.py`); `UMCSENT` from its ALFRED vintages (first vintage
1998-07-31; older months count as public 45 days after the 1st of the month, later than the real
release). Fear & Greed's value for day `x` (UTC) is used from `x + 1`.

**Twin.** `tsmom12` for every card (card 10 also shows `sma200`). Also shown: equal weight.

**Pass bar.** The default in `protocol.md`, plus bar 6 from "Macro tests" for every card: the
primary must not be behind `tsmom12` on Sharpe over 2003-01-01..end of train.

**Episodes.** Every result counts its hostile spells 1994-2025 (runs of hostile days, gaps under
30 days merged, spells under 30 days dropped; `macro.spells`). For per-asset price gates the
count is given for BTC and SPY. That count is the number of independent tests.

**Out-of-universe** as in `protocol.md`: the 8 other ETFs, the 6 other coins, the indexes one at
a time (S&P 500 1962-1993, Nikkei, FTSE, DAX). Cards say which sets apply.

## 1. `bbwp`: weekly Bollinger Band Width Percentile tops (video FAIAELKdn7g)

**Claim.** When the weekly band width percentile goes above ~95 a major top comes within 0-2
months: cut exposure.

**Rule (fixed).** On weekly closes: band width `BBW = 4 x std(last 20 closes) / mean(last 20
closes)` (Bollinger 20, 2; population std). `BBWP` = share of the previous BBW values (the last
252 weeks, at least 104 needed) that are below the current one, x 100. Signal week: `BBWP >= 95`
and the weekly close above its 20-week mean (the expansion is upward: a top, not a crash). The
asset is hostile for 56 days (8 weeks, "0-2 months") after the last signal week. Gate acts on
every non-safe asset (stocks, commodity funds, coins), each on its own price.

**Why it might not work.** A wide band after a rally is also what the middle of a strong bull
run looks like (2017, 2020-21); 8 weeks out may miss the best weeks. Few cycle tops per asset.

**Variants.** `bbwp-and` (primary), `bbwp-alone`. The mirror case (low BBWP flags a breakout of
unknown direction) cannot be traded long-only; it is noted as an RL input only.

**Out of universe:** all three sets.

## 2. `srsi`: monthly stochastic RSI leaving overbought (video FAIAELKdn7g)

**Rule (fixed).** On monthly closes: RSI(14) with Wilder smoothing; `stoch = (RSI - min14) /
(max14 - min14) x 100` over the last 14 RSI values; `K` = 3-month mean of `stoch`, `D` not used.
Signal month: `K` was above 80 the month before and is at or below 80 now. Hostile for 365 days
from the first bar after the signal month (when the month is complete): the claim is a cycle top,
and cycle bears last about a year. Gate acts on every non-safe asset.

**Why it might not work.** About 4 BTC events; on stocks the monthly K leaves 80 many times in
long bull markets (1995-99, 2013-19) and a year out would be costly.

**Variants.** `srsi-and` (primary), `srsi-alone`. **Out of universe:** all three sets.

## 3. `ath`: the clock after breaking the old all-time high (video FAIAELKdn7g)

**Rule (fixed).** On weekly closes, track the all-time high (highest weekly close so far). A
cycle is armed when the weekly close falls at least 50% (coins) or 20% (everything else: the
usual bear-market line) below that high. The breakout is the first weekly close above that high
after it was armed. The asset is hostile from day 100 to day 464 after the breakout ("raise exits
past ~100 days", then a year of bear). Gate acts on every non-safe asset.

**Why it might not work.** n = 4 for BTC, and the 42-231 day range in the claim is wider than
the window's start; stocks often run for years after a new high (1995, 2013).

**Variants.** `ath-and` (primary), `ath-alone`. **Out of universe:** all three sets.

## 7. `gap`: stocks near highs while consumers are gloomy (videos YXFvwJQBzJc, f353QO5Dgus)

**Rule (fixed).** Sentiment is low when the latest `UMCSENT` value in the vintage current the day
before is at or below the 25th percentile of the previous 240 observations in that vintage (at
least 120 needed). A stock is near its high when its close is at least 95% of its highest close
over the last 252 bars. A stock is hostile for 182 days ("6-24 months", shortest end) after any
visible bar on which both held (sentiment taken as of the day after that bar's date). Gate acts
on stocks only.

**Why it might not work.** Low sentiment with high prices described 2023-24, a strong market;
sentiment is driven by inflation and gas prices, not by future earnings.

**Variants.** `gap-and` (primary), `gap-alone`. **Out of universe:** ETFs and indexes (not coins).

## 8. `oil`: oil supply shock regime (video f353QO5Dgus)

**Rule (fixed).** WTI spot (`DCOILWTICO`, daily from 1986, used from the day after). Shock on day
`d` when the latest price is at least 1.5x the price 182 days earlier, or at least 2x the price
365 days earlier (a base at or below 0 gives no shock). Stocks are hostile on a shock day and for
182 days after the last one. Gate acts on stocks only. The "favour energy" half is not tested
(long-only equal slots; no energy asset in the six).

**Why it might not work.** Few shocks since 1994 (1999-2000, 2005, 2008, 2021-22); rebounds from
crashes (1999, 2009, 2020-21) also double the price and are bullish.

**Variants.** `oil-and` (primary), `oil-alone`. **Out of universe:** ETFs and indexes (the S&P
500 test covers 1987-1993 only, including 1990).

## 9. `y10`: 10-year yield stress (video f353QO5Dgus)

**Rule (fixed).** 10-year Treasury yield (`DGS10`, used from the day after). Gate acts on stocks
and on TLT (the claim: underweight long bonds and equities). Four variants, as the note asks
(a range of levels and the 3-month change):

1. `y10chg-and` (primary): hostile while the yield is more than 0.75 points above its value 91
   days earlier.
2. `y10lvl40-and`, 3. `y10lvl47-and`, 4. `y10lvl55-and`: hostile while the yield is above 4.0%,
   4.7% (the video's range) or 5.5%.

**Why it might not work.** Yields were above 4.7% for most of 1994-2007, good years; the level
has no fixed meaning across decades.

**Out of universe:** ETFs and indexes (S&P 500 1962-1993 has the 1970s-80s yield cycle).

## 10. `trend3`: long SPY, GLD, BTC above the long average (video YXFvwJQBzJc)

**Rule (fixed).** Universe SPY, GLD, BTC, equal slots (one third each once eligible). 1.
`trend3-sma200` (primary): slot held above the 200-trading-day average (`sma200`'s rule). 2.
`trend3-10m`: slot held when the close is above the mean of the last 10 monthly closes. Twin:
`tsmom12` on the same three assets; equal weight of the three shown.

**Expectation, stated before the test:** this is the `sma200` twin itself on a smaller book.
`sma200` is already behind `tsmom12` on the six assets (1.01 vs 1.05). It cannot be "a new idea";
it is reported to show the owner how the video's rule compares with ours.

**Out of universe:** read from the logged `sma200` vs `tsmom12` baselines on each set.

## 12. `fng`: crypto Fear & Greed contrarian (video Fnx513JS5Vg, stand-in)

**Rule (fixed).** Alternative.me Crypto Fear & Greed index, daily from 2018-02-01. Coins only.
1. `fng-buyfear` (primary): a coin's slot is held when `tsmom12` holds it OR the index was at or
   below 24 ("extreme fear") on any day of the last 30. 2. `fng-sellgreed`: the `tsmom12` slot
   is dropped while the latest index value is 75 or above ("extreme greed").

**Bar 2 note.** Before 2018 the rule equals `tsmom12`, so it can be ahead in at most 2 eras
(2017-21, 2022-25): it cannot meet bar 2 (as with `halving`). The verdict keeps the default bar;
the result also says whether it is ahead in both eras with data, for information only.

**Out of universe:** the coin set only (same index; not an independent check).

## Results

`results/<card>.md` once tested; summary in `ideas-1.md`.
