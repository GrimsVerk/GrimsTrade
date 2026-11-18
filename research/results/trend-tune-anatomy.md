# trend-tune, Part A: anatomy of `tsmom12`

Card: `trend-tune.md` (Part A). Run 2026-11-18. A description of one rule on train data: nothing
here was selected, and nothing here is a test. 109 rows in `tries.md` (8 baselines, 98 surface
cells logged as `variant` to be conservative, 3 robustness). Tables below are written by
`lib/trend_tune_anatomy.py`; the section numbers match the card.

## Findings in plain words

A "log point" is one hundredth of a log return; for small numbers read it as a percent.

1. **It only ever beat holding on stocks, and only in the two long bear markets of 2000-2009**
   (section 1). Alone on each asset: SPY +0.09 Sharpe, QQQ +0.11, both unproven (p 0.26 and
   0.20); gold -0.08, bonds -0.06, Bitcoin +0.01, Ether -0.02. Since 2003 it is not ahead of
   holding by more than +0.01 on any of the six.
2. **It does not win by dodging losses. It wins, where it wins, by dodging wild days**
   (section 2). On five of the six assets the price *rose* on balance while the rule was out
   (only QQQ fell). What differs is the kind of days it sat out. On stocks the out-days were
   almost twice as rough as the in-days (SPY 29% volatility against 16%, QQQ 40% against 21%)
   and 12 of the 20 worst days fell while it was out. On bonds, gold and coins the out-days
   were no rougher than the in-days (TLT 14% against 15%, GLD 16% against 19%, BTC 65% against
   83%, ETH 86% against 94%), so there the rule gave up return and bought no calm. Stocks fall
   slowly and violently at the same time; coin crashes come out of uptrends (the rule was in
   for 74% of Bitcoin's crash time, and out on only 3 of its 20 worst days).
3. **What it saves in a bear market it hands back in the rebound, almost one for one**
   (section 5). Averaged over the six assets: +13.6 log points a year gained inside bear
   windows, -14.4 lost in the 12 months after each low, -0.6 in the rest. It sells at a median
   of 21% below the high and buys back 23% above the low, about seven months late. The years
   after a fall are where it trails equal weight most: 2003 (-22 points), 2009 (-20), 2019
   (-34), 2020 (-39), 2023 (-29).
4. **The bleed is whipsaw in short spells, not fees** (section 4). Of 112 spells out, 82 were
   whipsaws (the rule bought back higher than it sold). The 84 spells shorter than 13 weeks
   cost a net 339 log points summed over the six slots; the 22 spells longer than 26 weeks
   earned 247, and one of them (QQQ, November 2000 to June 2003, -58% while out) is 87 of
   that. Trading costs are small next to this: 0.03 to 0.06 log points a year on the ETFs, 0.3
   to 0.6 on the coins, against whipsaw costs of 2 to 12.
5. **In the book, since 2003, every asset contributed less under the rule than under plain
   holding** (section 6): 4.0 points a year in all (SPY -0.9, QQQ -1.2, TLT -0.3, GLD -0.6, BTC
   -0.5, ETH -0.7). The rule was behind equal weight in 17 of 23 calendar years. The dot-com
   bust is the one large entry on the other side (+28 points a year for two and a half years,
   on a book of two stock funds).
6. **Since 2003 the rule has behaved like "hold three quarters of everything"** (section 3).
   A constant 76% holding (the rule's own average) had the same Sharpe (1.19 against 1.20) and
   about the same worst loss (38% against 36%); the rule grew 2 points a year faster with 1.5
   points more volatility. Over 1994-2025 the worst loss differs a lot (57% against 36%): that
   is the dot-com bust again.
7. **The settings sit on a broad plateau; there is nothing to pick** (section 7). Lookbacks
   of 6 to 12 months give 1.02 to 1.13; shorter or longer is worse (0.96 at 3 months, 0.88 at
   24), in both windows. Deciding daily, weekly or monthly makes no difference (monthly halves
   the trading). Two lookbacks together, entry and exit thresholds and no-trade bands add at
   most 0.03 to the plain rule; a band cuts trading by 40% at the same Sharpe. No cell is a
   spike. The best cell (8 months) is +0.08 ahead, and 98 cells with no edge would show +0.17
   by luck alone. Twelve months is on the slow edge of the plateau, not at its centre.
8. **Perfect hindsight is worth +0.10** (section 7, hindsight ceiling). Giving each asset the
   lookback that turned out best over all of train (SPY 9, QQQ 9, TLT 18, GLD 18, BTC 9, ETH 3
   months) lifts Sharpe from 1.05 to 1.15. No honest tuner can beat a tuner that has seen the
   answers, so +0.10 is the ceiling for Part B, and the pass bar can only just see +0.10.
9. **The best lookback does not persist** (section 8). From one era to the next the ranking
   of lookbacks is unrelated (rank correlation -0.01 over 18 steps); last era's best lookback
   ranks 4.2 of 7 in the next (chance: 4) and beats 12 months in 7 of 18 steps.

**What part of the rule earns the money:** a few long absences from falling stock markets
(2000-2003, 2008-2009, 2022), which removed the most violent stretches. **Where it bleeds:**
late re-entry after every low, and dozens of short out-and-back-in trips at a higher price,
on every asset; on bonds, gold and coins there is no offsetting gain.

Reading notes: bear windows chain inside one long fall (QQQ 2000-2002 is six windows), so a
"bought back at" figure can be below an earlier low; the bucket sums are exact all the same.
Per-asset Sharpe differences are differences of two noisy numbers (standard error about 0.1).

<!-- tables below this line are written by lib/trend_tune_anatomy.py -->

Train period only (decisions to 2025-11-09), total-return prices, the gym's fills and costs. `tsmom12`: each asset's equal slot is held while its 365-day return is positive, else cash; decided on Fridays. Everything here is in sample and descriptive.

## 1. Each asset on its own: the rule against holding

One asset, all of the account, from the day it has a year of bars. `hold` buys once; the rule is `tsmom12` on that asset alone. p is the paired bootstrap's one-sided p-value that the rule's Sharpe is higher.

| Asset | From | Sharpe hold | Sharpe rule | Difference (p) | Growth/yr hold | Growth/yr rule | Worst loss hold | Worst loss rule | Time in |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 1994-02-01 | 0.63 | 0.72 | +0.09 (0.26) | +10.6% | +9.6% | 55% | 31% | 81% |
| QQQ | 2000-03-10 | 0.41 | 0.53 | +0.11 (0.20) | +7.7% | +8.5% | 83% | 41% | 79% |
| TLT | 2003-07-31 | 0.33 | 0.27 | -0.06 (0.69) | +3.8% | +2.5% | 48% | 33% | 64% |
| GLD | 2005-11-19 | 0.66 | 0.58 | -0.08 (0.76) | +10.8% | +8.0% | 46% | 34% | 69% |
| BTC | 2013-01-01 | 1.29 | 1.30 | +0.01 (0.48) | +101.1% | +95.1% | 85% | 81% | 76% |
| ETH | 2017-05-19 | 0.86 | 0.83 | -0.02 (0.54) | +43.7% | +40.5% | 94% | 92% | 63% |

Sharpe of the rule minus Sharpe of holding, by era (blank: under 250 days):

| Asset | 1994-99 | 2000-09 | 2010-16 | 2017-21 | 2022-25 | 2003-2025 |
|---|---:|---:|---:|---:|---:|---:|
| SPY | -0.00 | +0.19 | -0.23 | -0.16 | -0.04 | -0.02 |
| QQQ | - | +0.10 | -0.10 | -0.18 | -0.03 | -0.08 |
| TLT | - | -0.04 | -0.18 | -0.22 | -0.34 | -0.06 |
| GLD | - | -0.27 | +0.16 | -0.23 | -0.20 | -0.08 |
| BTC | - | - | -0.05 | -0.09 | +0.38 | +0.01 |
| ETH | - | - | - | -0.06 | -0.01 | -0.02 |

## 2. In and out: what the asset did while the rule held it and while it did not

Log points are sums of log returns (x100); a year's worth is shown. The asset's return is split at every fill: the overnight gap belongs to the position held before the open. `Asset while in` and `Asset while out` are annualised over the time spent in that state, so they compare the two kinds of days directly.

| Asset | Time in | Asset while in (log pts/yr of in-time) | Asset while out (log pts/yr of out-time) | Volatility in | Volatility out | Of the 20 worst days, rule was out |
|---|---:|---:|---:|---:|---:|---:|
| SPY | 81% | +11.3 | +5.0 | 16% | 29% | 12 |
| QQQ | 79% | +10.4 | -3.6 | 21% | 40% | 12 |
| TLT | 64% | +4.0 | +3.2 | 15% | 14% | 4 |
| GLD | 69% | +11.2 | +8.1 | 19% | 16% | 4 |
| BTC | 76% | +88.5 | +11.3 | 83% | 65% | 3 |
| ETH | 63% | +54.9 | +4.5 | 94% | 86% | 9 |

The identity, per year of the asset's history (log points a year): the rule's growth = holding's growth - what the asset did while the rule was out - costs.

| Asset | Years | Holding | Asset while rule was out | Costs and slippage | Rule |
|---|---:|---:|---:|---:|---:|
| SPY | 31.7 | +10.1 | +1.0 | -0.03 | +9.1 |
| QQQ | 25.6 | +7.4 | -0.8 | -0.03 | +8.2 |
| TLT | 22.2 | +3.7 | +1.1 | -0.04 | +2.5 |
| GLD | 19.9 | +10.3 | +2.5 | -0.06 | +7.7 |
| BTC | 12.8 | +70.0 | +2.7 | -0.33 | +66.9 |
| ETH | 8.5 | +36.4 | +1.6 | -0.64 | +34.1 |

A negative `Asset while rule was out` means the asset fell on balance while the rule was out (the rule gained by being out); a positive one means it rose (the rule missed it).

## 3. Being invested against stepping aside

`Constant` holds the rule's own average share of the asset all the time (the rest in cash at 0%), so it has the Sharpe of plain holding. The growth gap between the rule and `constant` is what choosing *when* to hold added or cost; the gaps in volatility and worst loss are what stepping aside bought.

| What | Average share held | Growth/yr constant | Growth/yr rule | Timing gap | Volatility constant | Volatility rule | Worst loss constant | Worst loss rule | Sharpe constant | Sharpe rule |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY alone | 81% | +8.8% | +9.6% | +0.7% | 15.3% | 14.1% | 47% | 31% | 0.63 | 0.72 |
| QQQ alone | 79% | +6.6% | +8.5% | +1.9% | 20.9% | 18.9% | 74% | 41% | 0.41 | 0.53 |
| TLT alone | 64% | +2.6% | +2.5% | -0.1% | 9.3% | 11.8% | 34% | 33% | 0.33 | 0.27 |
| GLD alone | 69% | +7.7% | +8.0% | +0.3% | 12.4% | 15.3% | 33% | 34% | 0.66 | 0.58 |
| BTC alone | 76% | +80.2% | +95.1% | +14.9% | 59.3% | 71.3% | 74% | 81% | 1.29 | 1.30 |
| ETH alone | 63% | +38.6% | +40.5% | +1.9% | 57.4% | 74.4% | 81% | 92% | 0.86 | 0.83 |
| Six-asset book, 1994-2025 | 76% | +14.0% | +17.8% | +3.8% | 16.4% | 17.1% | 57% | 36% | 0.88 | 1.05 |
| Six-asset book, 2003-2025 | 76% | +18.7% | +20.7% | +2.0% | 15.4% | 16.9% | 38% | 36% | 1.19 | 1.20 |

## 4. Out-spells, flips and whipsaw

A spell runs from the exit fill to the re-entry fill. It *saved* if the asset was cheaper at re-entry and was a *whipsaw* if it was dearer. Log points a year of the asset's history, on the asset's own slot (not the book). `Net` = saved - whipsaw - costs = the rule's growth minus holding's.

| Asset | Fills/yr | Spells | Saved spells | Whipsaws | Saved (log pts/yr) | Whipsaw cost (log pts/yr) | Costs (log pts/yr) | Net (log pts/yr) | Median spell (days) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 1.5 | 24 | 5 | 19 | +1.2 | -2.2 | -0.03 | -1.0 | 8 |
| QQQ | 1.5 | 19 | 4 | 15 | +3.8 | -3.0 | -0.03 | +0.7 | 21 |
| TLT | 2.3 | 25 | 8 | 17 | +1.3 | -2.4 | -0.04 | -1.2 | 42 |
| GLD | 2.9 | 28 | 7 | 21 | +1.6 | -4.1 | -0.06 | -2.6 | 28 |
| BTC | 1.2 | 7 | 2 | 5 | +3.6 | -6.4 | -0.33 | -3.0 | 35 |
| ETH | 2.2 | 9 | 4 | 5 | +10.2 | -11.8 | -0.64 | -2.3 | 49 |

Spells by length, all six assets (net = saved minus whipsaw, in log points; summed over the assets' slots, not annualised):

| Length | Spells | Whipsaws | Net log points | Per asset: spells (net) |
|---|---:|---:|---:|---|
| under 4 weeks | 57 | 44 | -127 | SPY 16 (-36), QQQ 10 (-43), TLT 12 (-6), GLD 14 (-26), BTC 2 (-0), ETH 3 (-15) |
| 4-13 weeks | 27 | 24 | -212 | SPY 4 (-28), QQQ 6 (-33), TLT 4 (-15), GLD 8 (-41), BTC 2 (-51), ETH 3 (-44) |
| 13-26 weeks | 6 | 5 | -44 | TLT 3 (-16), GLD 2 (-2), ETH 1 (-26) |
| over 26 weeks | 22 | 9 | +247 | SPY 4 (+33), QQQ 3 (+96), TLT 6 (+11), GLD 4 (+19), BTC 3 (+16), ETH 2 (+72) |

The ten spells that saved most:

| Asset | Out | Back in | Days | Asset's move while out |
|---|---|---|---:|---:|
| QQQ | 2000-11-20 | 2003-06-09 | 931 | -58% |
| BTC | 2022-02-05 | 2023-06-17 | 497 | -37% |
| ETH | 2018-08-18 | 2019-09-21 | 399 | -31% |
| ETH | 2022-05-07 | 2023-06-03 | 392 | -29% |
| GLD | 2013-01-28 | 2014-06-23 | 511 | -21% |
| TLT | 2022-03-28 | 2024-01-02 | 645 | -20% |
| SPY | 2000-11-13 | 2002-03-18 | 490 | -12% |
| SPY | 2008-01-22 | 2009-10-12 | 629 | -12% |
| ETH | 2023-08-12 | 2023-08-26 | 14 | -11% |
| QQQ | 2008-09-02 | 2009-09-21 | 384 | -9% |

The ten costliest whipsaws:

| Asset | Out | Back in | Days | Asset's move while out |
|---|---|---|---:|---:|
| ETH | 2019-12-28 | 2020-01-18 | 21 | +34% |
| BTC | 2015-11-14 | 2015-12-12 | 28 | +34% |
| ETH | 2025-02-15 | 2025-07-19 | 154 | +30% |
| ETH | 2020-03-14 | 2020-04-18 | 35 | +26% |
| BTC | 2018-11-03 | 2019-05-25 | 203 | +26% |
| BTC | 2020-06-27 | 2020-08-01 | 35 | +24% |
| ETH | 2020-05-16 | 2020-07-18 | 63 | +19% |
| SPY | 2020-03-16 | 2020-04-20 | 35 | +18% |
| GLD | 2009-01-12 | 2009-02-17 | 36 | +17% |
| QQQ | 2025-04-07 | 2025-04-14 | 7 | +14% |

## 5. Bear markets, rebounds and the rest

Bear window: a fall of at least 20% (ETFs) or 50% (coins) from the highest close since the last bear low, to the lowest close after it. Rebound: the 365 days after that low. Log points summed inside each bucket; `Rule - hold` is what the rule gained or lost there against holding, before costs.

| Asset | Bucket | Windows | Years | Holding (log pts) | Rule (log pts) | Rule - hold | Rule - hold per year of history | Time in |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| SPY | bear | 6 | 4.0 | -254 | -85 | +168 | +5.3 | 34% |
| SPY | rebound | 6 | 4.6 | +198 | +42 | -156 | -4.9 | 39% |
| SPY | the rest | - | 23.2 | +378 | +335 | -43 | -1.3 | 97% |
| QQQ | bear | 13 | 3.8 | -581 | -221 | +360 | +14.0 | 41% |
| QQQ | rebound | 13 | 6.7 | +487 | +181 | -307 | -12.0 | 59% |
| QQQ | the rest | - | 15.1 | +284 | +251 | -33 | -1.3 | 97% |
| TLT | bear | 3 | 4.7 | -120 | -64 | +56 | +2.5 | 39% |
| TLT | rebound | 3 | 3.0 | +46 | +8 | -38 | -1.7 | 33% |
| TLT | the rest | - | 14.5 | +157 | +113 | -43 | -1.9 | 79% |
| GLD | bear | 5 | 7.1 | -166 | -132 | +34 | +1.7 | 45% |
| GLD | rebound | 5 | 4.1 | +102 | +34 | -67 | -3.4 | 79% |
| GLD | the rest | - | 8.7 | +269 | +253 | -16 | -0.8 | 85% |
| BTC | bear | 10 | 4.1 | -1061 | -823 | +238 | +18.5 | 74% |
| BTC | rebound | 10 | 4.5 | +1174 | +901 | -273 | -21.2 | 55% |
| BTC | the rest | - | 4.2 | +787 | +787 | +0 | +0.0 | 100% |
| ETH | bear | 8 | 3.4 | -995 | -659 | +335 | +39.6 | 71% |
| ETH | rebound | 8 | 4.2 | +1042 | +679 | -363 | -42.9 | 50% |
| ETH | the rest | - | 0.9 | +261 | +275 | +14 | +1.7 | 94% |
| all six | bear | | | -3176 | -1986 | +1191 | +13.6 (average) | |
| all six | rebound | | | +3048 | +1844 | -1204 | -14.4 (average) | |
| all six | the rest | | | +2135 | +2013 | -122 | -0.6 (average) | |

Every bear window: how far below the high the rule sold, and how far above the low it bought back. `Held` and `rule` are the returns inside the window (high to low).

| Asset | High | Low | Held | Rule | Sold at (from the high) | Bought back at (from the low) | Days from low to buy-back |
|---|---|---|---:|---:|---|---|---:|
| SPY | 2000-03-24 | 2001-09-21 | -36% | -11% | -11% on 2000-11-13 | +21% on 2002-03-18 | 178 |
| SPY | 2002-03-19 | 2002-07-23 | -32% | -5% | -5% on 2002-04-08 | +27% on 2003-06-23 | 335 |
| SPY | 2007-10-09 | 2008-11-20 | -51% | -18% | -18% on 2008-01-22 | +47% on 2009-10-12 | 326 |
| SPY | 2009-01-06 | 2009-03-09 | -27% | +0% | was out at the high | +61% on 2009-10-12 | 217 |
| SPY | 2020-02-19 | 2020-03-23 | -34% | -29% | -29% on 2020-03-16 | +27% on 2020-04-20 | 28 |
| SPY | 2022-01-03 | 2022-10-12 | -24% | -13% | -13% on 2022-05-02 | +17% on 2023-05-08 | 208 |
| QQQ | 2000-03-27 | 2000-05-23 | -36% | -36% | held through the low | was in at the low | - |
| QQQ | 2000-09-01 | 2001-01-02 | -48% | -31% | -31% on 2000-11-20 | -44% on 2003-06-09 | 888 |
| QQQ | 2001-01-23 | 2001-04-04 | -50% | +0% | was out at the high | -12% on 2003-06-09 | 796 |
| QQQ | 2001-05-21 | 2001-09-21 | -45% | +0% | was out at the high | +6% on 2003-06-09 | 626 |
| QQQ | 2001-12-06 | 2002-08-05 | -50% | +0% | was out at the high | +40% on 2003-06-09 | 308 |
| QQQ | 2002-08-22 | 2002-10-09 | -23% | +0% | was out at the high | +50% on 2003-06-09 | 243 |
| QQQ | 2007-10-31 | 2008-03-10 | -25% | -20% | -20% on 2008-02-11 | +6% on 2008-03-31 | 21 |
| QQQ | 2008-06-05 | 2008-11-20 | -49% | -9% | -6% on 2008-06-23 | +66% on 2009-09-21 | 305 |
| QQQ | 2018-08-29 | 2018-12-24 | -23% | -21% | -21% on 2018-12-24 | +14% on 2019-01-22 | 29 |
| QQQ | 2020-02-19 | 2020-03-16 | -29% | -29% | held through the low | was in at the low | - |
| QQQ | 2021-12-27 | 2022-06-16 | -33% | -20% | -20% on 2022-04-25 | +20% on 2023-05-08 | 326 |
| QQQ | 2022-08-15 | 2022-11-03 | -22% | +0% | was out at the high | +24% on 2023-05-08 | 186 |
| QQQ | 2025-02-19 | 2025-04-08 | -23% | -24% | -24% on 2025-04-07 | +12% on 2025-04-14 | 6 |
| TLT | 2008-12-30 | 2009-06-10 | -27% | -27% | held through the low | was in at the low | - |
| TLT | 2012-07-25 | 2013-08-21 | -21% | -10% | -11% on 2013-02-04 | +14% on 2014-06-02 | 285 |
| TLT | 2020-08-04 | 2023-10-19 | -48% | -21% | -16% on 2021-02-22 | +20% on 2024-01-02 | 75 |
| GLD | 2006-05-12 | 2006-06-14 | -22% | -22% | held through the low | was in at the low | - |
| GLD | 2008-03-17 | 2008-09-11 | -26% | -26% | held through the low | was in at the low | - |
| GLD | 2008-10-09 | 2008-11-12 | -22% | -21% | -21% on 2008-10-27 | +10% on 2008-12-01 | 19 |
| GLD | 2011-08-22 | 2015-12-17 | -46% | -26% | -16% on 2012-07-16 | +15% on 2016-02-16 | 61 |
| GLD | 2020-08-06 | 2022-09-26 | -22% | -21% | -13% on 2021-07-12 | +10% on 2022-12-05 | 70 |
| BTC | 2013-04-09 | 2013-04-16 | -70% | -70% | held through the low | was in at the low | - |
| BTC | 2013-04-24 | 2013-07-06 | -55% | -55% | held through the low | was in at the low | - |
| BTC | 2013-12-04 | 2013-12-18 | -54% | -54% | held through the low | was in at the low | - |
| BTC | 2014-01-06 | 2014-04-10 | -60% | -60% | held through the low | was in at the low | - |
| BTC | 2014-06-03 | 2015-01-14 | -74% | -48% | -48% on 2014-11-22 | +118% on 2015-11-07 | 297 |
| BTC | 2017-12-16 | 2018-02-05 | -65% | -65% | held through the low | was in at the low | - |
| BTC | 2018-03-04 | 2018-12-15 | -72% | -45% | -45% on 2018-11-03 | +151% on 2019-05-25 | 161 |
| BTC | 2019-06-26 | 2020-03-12 | -62% | -62% | held through the low | was in at the low | - |
| BTC | 2021-04-13 | 2021-07-20 | -53% | -53% | held through the low | was in at the low | - |
| BTC | 2021-11-08 | 2022-11-21 | -77% | -38% | -38% on 2022-02-05 | +67% on 2023-06-17 | 208 |
| ETH | 2017-06-12 | 2017-07-16 | -61% | -61% | held through the low | was in at the low | - |
| ETH | 2018-01-13 | 2018-04-06 | -73% | -73% | held through the low | was in at the low | - |
| ETH | 2018-05-05 | 2018-12-14 | -90% | -61% | -61% on 2018-08-18 | +163% on 2019-09-21 | 281 |
| ETH | 2019-06-26 | 2019-12-17 | -64% | -46% | was out at the high | was in at the low | - |
| ETH | 2020-02-14 | 2020-03-12 | -61% | -61% | held through the low | was in at the low | - |
| ETH | 2021-05-11 | 2021-07-20 | -57% | -57% | held through the low | was in at the low | - |
| ETH | 2021-11-08 | 2022-06-18 | -79% | -44% | -44% on 2022-05-07 | +92% on 2023-06-03 | 350 |
| ETH | 2024-03-11 | 2025-04-08 | -64% | -33% | -33% on 2025-02-15 | +141% on 2025-07-19 | 102 |

Across the 45 bear windows: the rule sold at a median of -21% from the high (22 sales inside a window) and bought back at a median of +23% above the low, 212 days after it (28 buy-backs).

## 6. The six-asset book: where the return comes from

Both books replayed through the gym with every fill kept. An asset's contribution on a day is its change in value minus the cash put into it, over the book's equity the day before; the six add up to the book's daily return to the cent. Shown as the sum of daily returns per year of the window (percent a year; these add across assets, growth rates do not).

`tsmom12`:

| Window | SPY | QQQ | TLT | GLD | BTC | ETH | Book |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1994-2025 | +5.1% | +1.4% | +0.6% | +1.1% | +6.9% | +2.7% | +17.9% |
| 2003-2025 | +1.8% | +2.6% | +0.9% | +1.6% | +9.6% | +3.7% | +20.3% |
| 1994-99 | +21.9% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +21.9% |
| 2000-09 | +0.3% | -0.4% | +1.1% | +1.5% | +0.0% | +0.0% | +2.4% |
| 2010-16 | +2.0% | +3.2% | +1.2% | +0.9% | +15.7% | +0.0% | +23.0% |
| 2017-21 | +2.2% | +3.7% | +0.6% | +1.0% | +16.9% | +15.1% | +39.7% |
| 2022-25 | +1.4% | +1.7% | -0.9% | +2.8% | +6.7% | +2.5% | +14.2% |
| dot-com bust | -2.9% | -7.6% | +0.0% | +0.0% | +0.0% | +0.0% | -10.5% |

Equal weight (hold everything):

| Window | SPY | QQQ | TLT | GLD | BTC | ETH | Book |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1994-2025 | +5.3% | +1.0% | +0.8% | +1.6% | +7.3% | +3.2% | +19.1% |
| 2003-2025 | +2.7% | +3.8% | +1.2% | +2.2% | +10.1% | +4.4% | +24.3% |
| 1994-99 | +22.0% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | +22.0% |
| 2000-09 | -0.4% | -2.6% | +1.2% | +2.3% | +0.0% | +0.0% | +0.5% |
| 2010-16 | +2.9% | +3.5% | +1.9% | +0.6% | +16.6% | +0.0% | +25.5% |
| 2017-21 | +3.0% | +4.5% | +1.3% | +1.7% | +18.5% | +17.2% | +46.2% |
| 2022-25 | +2.0% | +2.5% | -1.4% | +3.7% | +5.7% | +3.6% | +16.1% |
| dot-com bust | -11.2% | -27.5% | +0.0% | +0.0% | +0.0% | +0.0% | -38.7% |

`tsmom12` minus equal weight (positive: the rule earned more from that asset):

| Window | SPY | QQQ | TLT | GLD | BTC | ETH | Book |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1994-2025 | -0.2% | +0.4% | -0.2% | -0.4% | -0.3% | -0.5% | -1.2% |
| 2003-2025 | -0.9% | -1.2% | -0.3% | -0.6% | -0.5% | -0.7% | -4.0% |
| 1994-99 | -0.1% | +0.0% | +0.0% | +0.0% | +0.0% | +0.0% | -0.1% |
| 2000-09 | +0.7% | +2.2% | -0.1% | -0.8% | +0.0% | +0.0% | +1.9% |
| 2010-16 | -0.9% | -0.3% | -0.7% | +0.3% | -0.9% | +0.0% | -2.4% |
| 2017-21 | -0.8% | -0.8% | -0.7% | -0.6% | -1.6% | -2.1% | -6.5% |
| 2022-25 | -0.6% | -0.7% | +0.5% | -0.9% | +1.0% | -1.2% | -2.0% |
| dot-com bust | +8.2% | +19.9% | +0.0% | +0.0% | +0.0% | +0.0% | +28.2% |

Sharpe, growth and worst loss of the two books in the same windows:

| Window | Sharpe rule | Sharpe equal weight | Growth/yr rule | Growth/yr equal weight | Worst loss rule | Worst loss equal weight | Average share held by the rule |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1994-2025 | 1.05 | 0.88 | +17.8% | +18.2% | 36% | 69% | 76% |
| 2003-2025 | 1.20 | 1.19 | +20.7% | +24.9% | 36% | 47% | 76% |
| 1994-99 | 1.34 | 1.35 | +22.8% | +23.0% | 19% | 19% | 99% |
| 2000-09 | 0.19 | 0.02 | +1.6% | -2.0% | 29% | 69% | 63% |
| 2010-16 | 1.55 | 1.67 | +24.5% | +27.5% | 17% | 20% | 81% |
| 2017-21 | 1.50 | 1.55 | +43.4% | +51.7% | 36% | 47% | 77% |
| 2022-25 | 0.88 | 0.67 | +13.5% | +14.0% | 16% | 40% | 62% |
| dot-com bust | -0.58 | -1.07 | -11.9% | -36.7% | 28% | 69% | 26% |

Calendar years since 2003, the rule's return minus equal weight's, with the asset that moved the gap most (its contribution to the rule minus to equal weight):

| Year | Rule | Equal weight | Gap | Largest part of the gap |
|---|---:|---:|---:|---|
| 2003 | +13.2% | +35.0% | -21.8% | QQQ -11.2% |
| 2004 | +8.4% | +10.4% | -2.0% | TLT -0.9% |
| 2005 | +5.4% | +6.8% | -1.4% | QQQ -1.4% |
| 2006 | +6.2% | +12.1% | -5.9% | QQQ -3.4% |
| 2007 | +17.4% | +16.4% | +1.0% | GLD +0.5% |
| 2008 | -0.7% | -11.7% | +11.0% | QQQ +7.8% |
| 2009 | -0.7% | +18.8% | -19.5% | QQQ -9.4% |
| 2010 | +17.6% | +19.0% | -1.4% | TLT -1.2% |
| 2011 | +9.3% | +13.4% | -4.1% | SPY -2.4% |
| 2012 | +6.4% | +11.2% | -4.8% | GLD -2.9% |
| 2013 | +201.3% | +166.1% | +35.2% | GLD +6.1% |
| 2014 | -1.8% | -1.2% | -0.5% | TLT -2.5% |
| 2015 | -1.5% | +9.1% | -10.6% | BTC -12.6% |
| 2016 | +16.4% | +27.4% | -11.0% | QQQ -2.8% |
| 2017 | +155.8% | +148.5% | +7.4% | ETH +4.9% |
| 2018 | -19.7% | -32.7% | +13.1% | ETH +10.9% |
| 2019 | +4.3% | +37.9% | -33.5% | ETH -13.9% |
| 2020 | +72.9% | +111.7% | -38.8% | ETH -13.4% |
| 2021 | +64.4% | +65.2% | -0.8% | ETH +1.0% |
| 2022 | -12.8% | -36.5% | +23.7% | BTC +12.6% |
| 2023 | +23.4% | +52.8% | -29.4% | BTC -8.7% |
| 2024 | +38.8% | +39.5% | -0.7% | TLT -0.5% |
| 2025 | +10.2% | +23.4% | -13.2% | ETH -6.4% |

The rule finished behind equal weight in 17 of 23 years and ahead in 6.

## 7. Sensitivity surface (train, IN SAMPLE: a description, nothing is selected)

Every cell is a rule on the six assets, 1994-2025, through the gym, and a row in `tries.md`. Sharpe ratios. `tsmom12` is the 12-month, weekly, no-threshold cell: 1.05 over 1994-2025 and 1.20 over 2003-2025.

### Lookback (months) by decision frequency

Sharpe 1994-2025:

| | daily | weekly | monthly |
|---|---:|---:|---:|
| 3 | 0.99 | 0.96 | 1.00 |
| 4 | 1.00 | 0.97 | 1.01 |
| 5 | 0.99 | 1.03 | 1.02 |
| 6 | 1.04 | 1.02 | 1.05 |
| 7 | 1.02 | 1.06 | 1.05 |
| 8 | 1.10 | 1.13 | 1.14 |
| 9 | 1.10 | 1.09 | 1.08 |
| 10 | 1.00 | 1.03 | 1.01 |
| 11 | 1.07 | 1.05 | 1.05 |
| 12 | 1.06 | 1.05 | 1.00 |
| 13 | 1.00 | 0.99 | 1.02 |
| 14 | 1.00 | 0.98 | 0.96 |
| 15 | 0.94 | 0.95 | 0.95 |
| 16 | 0.94 | 0.93 | 0.90 |
| 18 | 0.88 | 0.93 | 0.91 |
| 20 | 0.91 | 0.93 | 0.94 |
| 22 | 0.92 | 0.91 | 0.88 |
| 24 | 0.87 | 0.88 | 0.91 |

Sharpe 2003-2025:

| | daily | weekly | monthly |
|---|---:|---:|---:|
| 3 | 1.23 | 1.21 | 1.17 |
| 4 | 1.30 | 1.24 | 1.24 |
| 5 | 1.23 | 1.23 | 1.16 |
| 6 | 1.21 | 1.18 | 1.19 |
| 7 | 1.23 | 1.26 | 1.22 |
| 8 | 1.31 | 1.32 | 1.32 |
| 9 | 1.28 | 1.24 | 1.19 |
| 10 | 1.14 | 1.17 | 1.10 |
| 11 | 1.22 | 1.20 | 1.20 |
| 12 | 1.23 | 1.20 | 1.12 |
| 13 | 1.16 | 1.13 | 1.15 |
| 14 | 1.17 | 1.12 | 1.10 |
| 15 | 1.09 | 1.09 | 1.09 |
| 16 | 1.11 | 1.06 | 1.06 |
| 18 | 1.04 | 1.10 | 1.06 |
| 20 | 1.08 | 1.09 | 1.10 |
| 22 | 1.08 | 1.06 | 1.02 |
| 24 | 1.04 | 1.04 | 1.07 |

Worst loss 1994-2025:

| | daily | weekly | monthly |
|---|---:|---:|---:|
| 3 | 44% | 50% | 32% |
| 4 | 53% | 49% | 42% |
| 5 | 50% | 37% | 29% |
| 6 | 38% | 37% | 33% |
| 7 | 34% | 29% | 32% |
| 8 | 32% | 28% | 32% |
| 9 | 30% | 33% | 35% |
| 10 | 39% | 35% | 41% |
| 11 | 32% | 33% | 33% |
| 12 | 36% | 36% | 41% |
| 13 | 34% | 36% | 39% |
| 14 | 40% | 41% | 43% |
| 15 | 46% | 45% | 45% |
| 16 | 44% | 53% | 46% |
| 18 | 49% | 46% | 46% |
| 20 | 49% | 48% | 48% |
| 22 | 47% | 47% | 48% |
| 24 | 47% | 47% | 48% |

Trades a year (turnover):

| | daily | weekly | monthly |
|---|---:|---:|---:|
| 3 | 12.0 | 5.4 | 3.4 |
| 4 | 10.0 | 5.0 | 3.0 |
| 5 | 8.2 | 4.4 | 2.9 |
| 6 | 9.1 | 4.5 | 2.6 |
| 7 | 8.2 | 3.7 | 2.5 |
| 8 | 7.5 | 4.0 | 2.3 |
| 9 | 7.0 | 3.9 | 2.4 |
| 10 | 6.4 | 3.4 | 2.2 |
| 11 | 5.9 | 3.1 | 2.0 |
| 12 | 4.9 | 2.7 | 1.9 |
| 13 | 5.4 | 2.9 | 1.9 |
| 14 | 5.6 | 2.9 | 1.9 |
| 15 | 5.1 | 2.8 | 1.8 |
| 16 | 4.9 | 2.9 | 2.1 |
| 18 | 5.7 | 2.9 | 1.9 |
| 20 | 5.2 | 2.8 | 2.0 |
| 22 | 4.0 | 2.5 | 1.9 |
| 24 | 3.9 | 2.4 | 1.8 |

Sharpe 1994-2025 minus the average of the cell's grid neighbours (a spike is above +0.10):

| | daily | weekly | monthly |
|---|---:|---:|---:|
| 3 | +0.02 | -0.03 | +0.02 |
| 4 | +0.01 | -0.02 | +0.01 |
| 5 | -0.03 | +0.03 | -0.01 |
| 6 | +0.03 | -0.03 | +0.02 |
| 7 | -0.05 | +0.00 | -0.03 |
| 8 | +0.02 | +0.03 | +0.05 |
| 9 | +0.04 | +0.00 | +0.00 |
| 10 | -0.07 | -0.01 | -0.05 |
| 11 | +0.03 | +0.00 | +0.03 |
| 12 | +0.02 | +0.02 | -0.04 |
| 13 | -0.01 | -0.02 | +0.04 |
| 14 | +0.03 | +0.00 | -0.02 |
| 15 | -0.02 | -0.00 | +0.01 |
| 16 | +0.02 | -0.00 | -0.03 |
| 18 | -0.04 | +0.02 | -0.01 |
| 20 | -0.01 | +0.01 | +0.03 |
| 22 | +0.02 | +0.01 | -0.04 |
| 24 | -0.02 | -0.02 | +0.03 |

### Two lookbacks together (weekly)

Above the diagonal (row < column): AND, held only if both are positive (the fast one takes you out, both must agree to get back in). Below the diagonal: OR, held if either is positive (slow to leave, quick to return). On the diagonal: the single lookback.

Sharpe 1994-2025:

| | 3 | 6 | 9 | 12 | 18 |
|---|---:|---:|---:|---:|---:|
| 3 | 0.96 | 0.91 | 0.98 | 0.94 | 0.96 |
| 6 | 1.06 | 1.02 | 1.06 | 1.02 | 1.02 |
| 9 | 1.06 | 1.04 | 1.09 | 1.05 | 1.01 |
| 12 | 1.06 | 1.05 | 1.08 | 1.05 | 1.03 |
| 18 | 0.95 | 0.94 | 1.01 | 0.95 | 0.93 |

Sharpe 2003-2025:

| | 3 | 6 | 9 | 12 | 18 |
|---|---:|---:|---:|---:|---:|
| 3 | 1.21 | 1.09 | 1.20 | 1.11 | 1.14 |
| 6 | 1.29 | 1.18 | 1.24 | 1.15 | 1.15 |
| 9 | 1.25 | 1.17 | 1.24 | 1.18 | 1.14 |
| 12 | 1.28 | 1.23 | 1.25 | 1.20 | 1.17 |
| 18 | 1.17 | 1.13 | 1.19 | 1.13 | 1.10 |

Worst loss 1994-2025:

| | 3 | 6 | 9 | 12 | 18 |
|---|---:|---:|---:|---:|---:|
| 3 | 50% | 46% | 39% | 39% | 38% |
| 6 | 42% | 37% | 29% | 31% | 28% |
| 9 | 37% | 38% | 33% | 33% | 36% |
| 12 | 42% | 44% | 37% | 36% | 34% |
| 18 | 51% | 54% | 46% | 45% | 46% |

Trades a year:

| | 3 | 6 | 9 | 12 | 18 |
|---|---:|---:|---:|---:|---:|
| 3 | 5.4 | 5.3 | 5.1 | 4.5 | 4.6 |
| 6 | 4.3 | 4.5 | 4.1 | 3.5 | 3.9 |
| 9 | 4.0 | 3.9 | 3.9 | 3.3 | 3.7 |
| 12 | 3.6 | 3.7 | 3.2 | 2.7 | 2.7 |
| 18 | 3.6 | 3.3 | 2.8 | 2.7 | 2.9 |

### Entry and exit thresholds on the trend's z-score (weekly)

z = the L-month return in units of the asset's own volatility. Enter above c + h, leave below c - h. Rows: centre c (negative = lenient, stays in through small losses; positive = strict). Columns: half-width h of the no-trade band. c = 0, h = 0 is the plain rule.

6-month lookback, Sharpe 1994-2025 / 2003-2025 (worst loss; trades a year):

| | h = 0.00 | h = 0.25 | h = 0.50 |
|---|---:|---:|---:|
| c = -0.25 | 1.02 / 1.25 (40%; 4.6) | 1.03 / 1.27 (49%; 2.3) | 0.99 / 1.18 (49%; 2.0) |
| c = +0.00 | 1.02 / 1.18 (37%; 4.5) | 0.99 / 1.18 (36%; 2.6) | 1.04 / 1.23 (33%; 2.1) |
| c = +0.25 | 0.93 / 1.13 (43%; 4.0) | 1.00 / 1.16 (32%; 2.4) | 0.97 / 1.17 (35%; 1.9) |

12-month lookback, Sharpe 1994-2025 / 2003-2025 (worst loss; trades a year):

| | h = 0.00 | h = 0.25 | h = 0.50 |
|---|---:|---:|---:|
| c = -0.25 | 1.08 / 1.27 (38%; 3.1) | 1.03 / 1.21 (42%; 1.8) | 1.01 / 1.18 (44%; 1.4) |
| c = +0.00 | 1.05 / 1.20 (36%; 2.7) | 1.05 / 1.21 (35%; 1.7) | 1.01 / 1.17 (45%; 1.5) |
| c = +0.25 | 0.98 / 1.15 (39%; 3.1) | 0.98 / 1.11 (40%; 1.8) | 0.97 / 1.10 (42%; 1.5) |

18-month lookback, Sharpe 1994-2025 / 2003-2025 (worst loss; trades a year):

| | h = 0.00 | h = 0.25 | h = 0.50 |
|---|---:|---:|---:|
| c = -0.25 | 0.89 / 1.05 (46%; 2.8) | 0.92 / 1.12 (48%; 1.6) | 0.88 / 1.09 (53%; 1.4) |
| c = +0.00 | 0.93 / 1.10 (46%; 2.9) | 0.91 / 1.07 (46%; 1.7) | 0.90 / 1.09 (48%; 1.4) |
| c = +0.25 | 0.84 / 0.91 (47%; 2.9) | 0.86 / 0.97 (46%; 1.7) | 0.88 / 1.04 (45%; 1.5) |

### The gym's rebalance band, `tsmom12` unchanged otherwise

| Band | Sharpe 1994-2025 | Sharpe 2003-2025 | Growth/yr | Worst loss | Trades a year |
|---|---:|---:|---:|---:|---:|
| 0.0% | 1.04 | 1.18 | +17.6% | 38% | 4.4 |
| 1.0% (the gym's rule) | 1.05 | 1.20 | +17.8% | 36% | 2.7 |
| 2.5% | 1.07 | 1.22 | +18.2% | 36% | 2.3 |
| 5.0% | 1.07 | 1.23 | +18.2% | 37% | 2.0 |

### Hindsight ceiling (the best lookbacks chosen with all of train in view)

The tuner's own score (paper series, full train) picks, with hindsight: SPY 9, QQQ 9, TLT 18, GLD 18, BTC 9, ETH 3 months per asset; 9 months for the pool. Run as fixed rules:

| Rule | Sharpe 1994-2025 | Sharpe 2003-2025 | Against `tsmom12` (p) | Worst loss |
|---|---:|---:|---:|---:|
| hindsight per asset (9, 9, 18, 18, 9, 3) | 1.15 | 1.33 | +0.10 (0.05) | 29% |
| hindsight pooled (9 months; the `L09-w` cell) | 1.09 | 1.24 | +0.04 (0.26) | 33% |

Paper-series Sharpe by lookback over all of train (what the tuner sees at the end; SPY includes the S&P 500 index 1962-1993):

| | 3 | 6 | 9 | 12 | 15 | 18 | 24 | Best |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 0.57 | 0.64 | 0.65 | 0.62 | 0.55 | 0.57 | 0.53 | 9 |
| QQQ | 0.40 | 0.53 | 0.59 | 0.53 | 0.49 | 0.39 | 0.35 | 9 |
| TLT | 0.35 | 0.23 | 0.16 | 0.25 | 0.20 | 0.37 | 0.36 | 18 |
| GLD | 0.62 | 0.65 | 0.53 | 0.59 | 0.69 | 0.71 | 0.70 | 18 |
| BTC | 1.29 | 1.37 | 1.40 | 1.30 | 1.16 | 1.10 | 1.09 | 9 |
| ETH | 0.96 | 0.75 | 0.82 | 0.83 | 0.71 | 0.73 | 0.58 | 3 |
| pool | 0.79 | 0.84 | 0.85 | 0.80 | 0.72 | 0.69 | 0.65 | 9 |

### Reading the surface

- Cells logged besides `tsmom12`: 98. Ahead of `tsmom12` on Sharpe over 1994-2025: 21; over 2003-2025: 33.
- If none of the 98 cells had any edge over `tsmom12`, the best would still be expected to show about +0.17 (expected maximum, standard error of a difference about 0.07 among the top cells; the cells are far from independent, so this overstates luck).
- The eight best cells by Sharpe 1994-2025 (in sample):

| Cell | Sharpe 1994-2025 | Against `tsmom12` | Sharpe 2003-2025 | Against `tsmom12` 2003-2025 | Worst loss | Trades a year |
|---|---:|---:|---:|---:|---:|---:|
| hindsight-asset | 1.15 | +0.10 | 1.33 | +0.13 | 29% | 3.5 |
| L08-m | 1.14 | +0.09 | 1.32 | +0.12 | 32% | 2.3 |
| L08-w | 1.13 | +0.08 | 1.32 | +0.12 | 28% | 4.0 |
| L08-d | 1.10 | +0.05 | 1.31 | +0.11 | 32% | 7.5 |
| L09-d | 1.10 | +0.05 | 1.28 | +0.08 | 30% | 7.0 |
| L09-w | 1.09 | +0.04 | 1.24 | +0.04 | 33% | 3.9 |
| or-09-12 | 1.08 | +0.04 | 1.25 | +0.06 | 37% | 3.2 |
| z12-c-0.25-h0.00 | 1.08 | +0.03 | 1.27 | +0.07 | 38% | 3.1 |

- Spikes in the lookback-by-frequency map (a cell more than 0.10 above its neighbours): none.

## 8. Does the best lookback persist from one era to the next?

From the paper series the tuner scores on (gym-free, costs charged; no `tries.md` rows). Sharpe of each grid lookback in each era, for eras with at least two years of that asset. `Rank corr.` is the Spearman rank correlation of the seven lookbacks with the previous era (+1: same order, 0: unrelated). `Last best, now` is the rank (1 = best of 7) that the previous era's best lookback has in this era; 4 is what chance gives.

| Asset | Era | 3 | 6 | 9 | 12 | 15 | 18 | 24 | Best | Rank corr. | Last best, now | Last best minus 12 months, now |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 1962-79 | 0.52 | 0.41 | 0.37 | 0.26 | 0.17 | 0.13 | -0.09 | 3 | - | - | - |
| SPY | 1980-93 | 0.59 | 0.78 | 0.64 | 0.62 | 0.56 | 0.52 | 0.64 | 6 | +0.21 | 5 (3 months) | -0.03 |
| SPY | 1994-99 | 1.20 | 1.23 | 1.24 | 1.34 | 1.35 | 1.35 | 1.35 | 15 | -0.21 | 6 (6 months) | -0.11 |
| SPY | 2000-09 | -0.10 | 0.32 | 0.50 | 0.32 | 0.14 | 0.22 | 0.07 | 9 | -0.18 | 5 (15 months) | -0.18 |
| SPY | 2010-16 | 0.40 | 0.55 | 0.57 | 0.57 | 0.74 | 0.74 | 0.90 | 24 | -0.14 | 4 (9 months) | +0.01 |
| SPY | 2017-21 | 1.22 | 0.66 | 0.86 | 0.97 | 0.88 | 1.03 | 0.79 | 3 | -0.29 | 6 (24 months) | -0.18 |
| SPY | 2022-25 | 0.87 | 0.87 | 0.76 | 0.73 | 0.37 | 0.57 | 0.57 | 3 | +0.14 | 1 (3 months) | +0.15 |
| QQQ | 2000-09 | -0.04 | 0.14 | 0.29 | -0.00 | -0.12 | -0.19 | -0.29 | 9 | - | - | - |
| QQQ | 2010-16 | 0.30 | 0.63 | 0.62 | 0.84 | 0.88 | 0.90 | 0.91 | 24 | -0.79 | 6 (9 months) | -0.22 |
| QQQ | 2017-21 | 1.14 | 1.01 | 0.96 | 1.07 | 1.23 | 1.10 | 1.23 | 15 | +0.57 | 1 (24 months) | +0.16 |
| QQQ | 2022-25 | 0.77 | 0.83 | 0.86 | 0.69 | 0.48 | 0.31 | 0.17 | 9 | -0.82 | 5 (15 months) | -0.22 |
| TLT | 2000-09 | 0.53 | 0.06 | 0.19 | 0.49 | 0.36 | 0.41 | 0.52 | 3 | - | - | - |
| TLT | 2010-16 | 0.61 | 0.44 | 0.31 | 0.32 | 0.24 | 0.46 | 0.37 | 3 | +0.43 | 1 (3 months) | +0.29 |
| TLT | 2017-21 | 0.31 | 0.55 | 0.40 | 0.30 | 0.19 | 0.45 | 0.52 | 6 | +0.46 | 5 (3 months) | +0.01 |
| TLT | 2022-25 | -0.53 | -0.64 | -0.88 | -0.85 | -0.38 | -0.35 | -0.76 | 18 | -0.07 | 4 (6 months) | +0.22 |
| GLD | 2000-09 | 0.74 | 0.74 | 0.69 | 0.66 | 0.88 | 0.87 | 0.92 | 24 | - | - | - |
| GLD | 2010-16 | 0.15 | 0.38 | 0.21 | 0.24 | 0.39 | 0.43 | 0.21 | 18 | +0.39 | 5 (24 months) | -0.02 |
| GLD | 2017-21 | 0.61 | 0.37 | 0.36 | 0.59 | 0.42 | 0.50 | 0.72 | 24 | -0.25 | 4 (18 months) | -0.09 |
| GLD | 2022-25 | 1.29 | 1.32 | 1.09 | 1.18 | 1.32 | 1.33 | 1.24 | 18 | +0.00 | 5 (24 months) | +0.07 |
| BTC | 2010-16 | 1.60 | 1.85 | 1.90 | 1.59 | 1.43 | 1.51 | 1.42 | 9 | - | - | - |
| BTC | 2017-21 | 1.33 | 1.31 | 1.23 | 1.27 | 1.15 | 1.12 | 1.31 | 3 | +0.29 | 5 (9 months) | -0.03 |
| BTC | 2022-25 | 0.81 | 0.70 | 1.04 | 1.06 | 0.84 | 0.37 | 0.14 | 12 | -0.11 | 4 (3 months) | -0.25 |
| ETH | 2017-21 | 1.38 | 1.17 | 1.21 | 1.11 | 1.10 | 1.08 | 1.01 | 3 | - | - | - |
| ETH | 2022-25 | 0.13 | -0.12 | 0.12 | 0.33 | -0.01 | 0.19 | -0.13 | 12 | +0.25 | 3 (3 months) | -0.20 |
| pool | 1962-79 | 0.52 | 0.41 | 0.37 | 0.26 | 0.17 | 0.13 | -0.09 | 3 | - | - | - |
| pool | 1980-93 | 0.59 | 0.79 | 0.64 | 0.62 | 0.56 | 0.52 | 0.64 | 6 | +0.21 | 5 (3 months) | -0.03 |
| pool | 1994-99 | 1.20 | 1.23 | 1.24 | 1.34 | 1.35 | 1.35 | 1.35 | 15 | -0.21 | 6 (6 months) | -0.11 |
| pool | 2000-09 | -0.07 | 0.16 | 0.38 | 0.22 | 0.10 | 0.06 | -0.00 | 9 | -0.14 | 4 (15 months) | -0.12 |
| pool | 2010-16 | 1.39 | 1.65 | 1.65 | 1.51 | 1.47 | 1.59 | 1.49 | 9 | +0.75 | 1 (9 months) | +0.14 |
| pool | 2017-21 | 1.71 | 1.55 | 1.54 | 1.52 | 1.44 | 1.48 | 1.54 | 3 | -0.07 | 4 (9 months) | +0.01 |
| pool | 2022-25 | 0.77 | 0.65 | 0.84 | 0.94 | 0.62 | 0.51 | 0.22 | 12 | +0.14 | 3 (3 months) | -0.17 |

Over the 18 era-to-era steps of the six assets: average rank correlation -0.01; the previous era's best lookback ranked 4.2 of 7 on average in the next era, was the best again in 3 steps, and beat the 12-month rule in 7 of them (average Sharpe difference to 12 months -0.04).
