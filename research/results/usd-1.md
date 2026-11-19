# USD 1: replication of `usd_13w` (table)

Script `lib/usd1.py`, card `research/usd-1.md`. Descriptive: no backtest, train bars
only, held-out year not loaded. `usd_13w` = the dollar index's (DXY) log change over the
last 91 days, known the day before the Friday. **S = minus the correlation** of `usd_13w`
with the coming `h` weeks' risk-adjusted return over all cells (every Friday, overlapping
windows): **S > 0 = same sign as slow-1 found** (dollar up, then worse returns). p = the
share of 2000 rotations of the weekly dollar series (one for all sets) with
S at least as large, one-sided. Null sd = the spread of S under those rotations; N eff =
1 / its variance (independent observations the S is worth); Detectable = 2.49 x null sd
(the true IC this test would catch four times in five). Non-overlap = S on every `h`-th
Friday, mean (min..max) over the `h` starting weeks. Basket S = the same correlation with
one number per Friday (the set's average). WF = slow-1's walk-forward IC (slope refitted
every two years; `pool` one slope, `per` a slope per asset), with the number of test
blocks whose fitted pooled slope has the card's sign (negative).

**Verdict at 13 weeks: echo only.** (a) pooled P > 0 with p < 0.05: yes. (b) S > 0 in at least 2 of 3 sets: yes. (c) `before`, the only set that shares no date with the screen, S > 0 with p < 0.05: no.

## Horizon 13 weeks (the bar)

| Set | From | To | Weeks | Cells | Assets | S | p | Null sd | N eff | Detectable | Non-overlap | Basket S (p) | WF pool | WF per | Blocks with the card's sign |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---|
| `before` | 1971-04-09 | 1999-10-01 | 1487 | 4306 | 4 | +0.013 | 0.438 | 0.063 | 249 | 0.158 | +0.013 (-0.02..+0.06) | +0.021 (0.414) | -0.097 | +0.013 | 8 of 12 |
| `markets` | 2000-01-07 | 2025-08-08 | 1336 | 22563 | 18 | +0.070 | 0.118 | 0.061 | 269 | 0.151 | +0.071 (+0.02..+0.15) | +0.088 (0.123) | +0.024 | +0.031 | 10 of 11 |
| `coins` | 2017-04-28 | 2025-08-08 | 433 | 30307 | 292 | +0.267 | 0.004 | 0.126 | 63 | 0.312 | +0.261 (-0.03..+0.41) | +0.319 (0.003) | +0.293 |  | 2 of 2 |
| **pooled** (sets count equally) | | | | | | P +1.16 | 0.025 | 0.63 | | | | | | | 3 of 3 sets S > 0 |
| `markets-resid` | 2000-01-07 | 2025-08-08 | 1336 | 22563 | 18 | -0.001 | 0.506 | 0.033 | 937 | 0.081 | +0.000 (-0.05..+0.04) | -0.010 (0.544) |  |  |  |
| `coins-resid` | 2017-04-28 | 2025-08-08 | 433 | 29531 | 214 | -0.087 | 0.826 | 0.084 | 141 | 0.210 | -0.090 (-0.24..+0.01) | -0.152 (0.854) |  |  |  |
| `six` (discovery sample, not a test) | 2000-01-07 | 2025-08-08 | 1336 | 5930 | 6 | +0.115 | 0.011 | 0.052 | 373 | 0.129 | +0.115 (+0.07..+0.14) | +0.160 (0.021) | +0.125 | +0.151 | 11 of 11 |

## Horizon 4 weeks (secondary, not in the bar)

| Set | From | To | Weeks | Cells | Assets | S | p | Null sd | N eff | Detectable | Non-overlap | Basket S (p) | WF pool | WF per | Blocks with the card's sign |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---|
| `before` | 1971-04-09 | 1999-12-03 | 1496 | 4342 | 4 | -0.013 | 0.637 | 0.042 | 577 | 0.103 | -0.013 (-0.03..-0.00) | -0.006 (0.551) | -0.051 | +0.014 | 7 of 12 |
| `markets` | 2000-01-07 | 2025-10-10 | 1345 | 22725 | 18 | +0.036 | 0.165 | 0.037 | 727 | 0.092 | +0.037 (+0.02..+0.06) | +0.039 (0.214) | -0.028 | -0.005 | 8 of 11 |
| `coins` | 2017-04-28 | 2025-10-10 | 442 | 31189 | 297 | +0.144 | 0.043 | 0.083 | 144 | 0.207 | +0.144 (+0.11..+0.16) | +0.155 (0.038) | +0.146 |  | 2 of 2 |
| **pooled** (sets count equally) | | | | | | P +0.80 | 0.120 | 0.62 | | | | | | | 2 of 3 sets S > 0 |
| `markets-resid` | 2000-01-07 | 2025-10-10 | 1345 | 22725 | 18 | +0.005 | 0.418 | 0.020 | 2411 | 0.051 | +0.005 (-0.00..+0.01) | +0.004 (0.476) |  |  |  |
| `coins-resid` | 2017-04-28 | 2025-10-10 | 442 | 30329 | 214 | -0.031 | 0.724 | 0.053 | 354 | 0.132 | -0.031 (-0.05..-0.02) | -0.077 (0.799) |  |  |  |
| `six` (discovery sample, not a test) | 2000-01-07 | 2025-10-10 | 1345 | 5984 | 6 | +0.053 | 0.051 | 0.033 | 945 | 0.081 | +0.053 (+0.04..+0.06) | +0.058 (0.119) | +0.026 | +0.045 | 9 of 11 |

`-resid` = the same set after taking out, per asset, the part of its return that the
screen's own assets explain (SPY for `markets`; the mean of BTC and ETH for `coins`).
S > 0 there means the dollar reaches those assets harder than it reached the screen's.
P = the mean over the three sets of S / null sd.

## S by era, 13 weeks (descriptive)

| Set | Era | Weeks | S |
|---|---|---:|---:|
| `before` | 1971-79 | 456 | -0.003 |
| `before` | 1980-89 | 522 | +0.116 |
| `before` | 1990-99 | 509 | -0.069 |
| `markets` | 2000-09 | 521 | +0.114 |
| `markets` | 2010-16 | 366 | +0.016 |
| `markets` | 2017-21 | 261 | +0.067 |
| `markets` | 2022-25 | 188 | +0.146 |
| `coins` | 2017-21 | 245 | +0.276 |
| `coins` | 2022-25 | 188 | +0.262 |
| `markets-resid` | 2000-09 | 521 | -0.004 |
| `markets-resid` | 2010-16 | 366 | +0.030 |
| `markets-resid` | 2017-21 | 261 | +0.035 |
| `markets-resid` | 2022-25 | 188 | -0.145 |
| `coins-resid` | 2017-21 | 245 | -0.053 |
| `coins-resid` | 2022-25 | 188 | -0.115 |

## S by era, 4 weeks (descriptive)

| Set | Era | Weeks | S |
|---|---|---:|---:|
| `before` | 1971-79 | 456 | +0.032 |
| `before` | 1980-89 | 522 | +0.051 |
| `before` | 1990-99 | 518 | -0.083 |
| `markets` | 2000-09 | 521 | +0.060 |
| `markets` | 2010-16 | 366 | +0.022 |
| `markets` | 2017-21 | 261 | -0.009 |
| `markets` | 2022-25 | 197 | +0.084 |
| `coins` | 2017-21 | 245 | +0.103 |
| `coins` | 2022-25 | 197 | +0.159 |
| `markets-resid` | 2000-09 | 521 | -0.000 |
| `markets-resid` | 2010-16 | 366 | +0.021 |
| `markets-resid` | 2017-21 | 261 | +0.023 |
| `markets-resid` | 2022-25 | 197 | -0.055 |
| `coins-resid` | 2017-21 | 245 | -0.054 |
| `coins-resid` | 2022-25 | 197 | -0.027 |

## S per asset, 13 weeks (descriptive)

| Set | Asset | S |
|---|---|---:|
| `before` | GSPC | +0.017 |
| `before` | N225 | +0.018 |
| `before` | FTSE | +0.101 |
| `before` | GDAXI | -0.159 |
| `markets` | IWM | +0.089 |
| `markets` | EFA | +0.066 |
| `markets` | EEM | +0.080 |
| `markets` | VNQ | +0.066 |
| `markets` | DBC | +0.255 |
| `markets` | SLV | +0.105 |
| `markets` | XLK | +0.109 |
| `markets` | XLF | -0.009 |
| `markets` | XLE | +0.123 |
| `markets` | XLV | +0.010 |
| `markets` | XLY | +0.060 |
| `markets` | XLP | -0.022 |
| `markets` | XLI | +0.060 |
| `markets` | XLB | +0.106 |
| `markets` | XLU | +0.023 |
| `markets` | N225 | +0.113 |
| `markets` | FTSE | +0.034 |
| `markets` | GDAXI | -0.008 |
| `coins` | ltc | +0.309 |
| `coins` | xrp | +0.242 |
| `coins` | bch | +0.420 |
| `coins` | etc | +0.212 |
| `coins` | xlm | +0.318 |
| `coins` | dash | +0.295 |
| `coins` | coins with S > 0 (of those with a year of cells) | 150 of 166 |
| `markets-resid` | IWM | +0.022 |
| `markets-resid` | EFA | -0.042 |
| `markets-resid` | EEM | +0.002 |
| `markets-resid` | VNQ | -0.006 |
| `markets-resid` | DBC | +0.230 |
| `markets-resid` | SLV | +0.081 |
| `markets-resid` | XLK | +0.052 |
| `markets-resid` | XLF | -0.171 |
| `markets-resid` | XLE | +0.081 |
| `markets-resid` | XLV | -0.088 |
| `markets-resid` | XLY | -0.048 |
| `markets-resid` | XLP | -0.116 |
| `markets-resid` | XLI | -0.063 |
| `markets-resid` | XLB | +0.048 |
| `markets-resid` | XLU | -0.033 |
| `markets-resid` | N225 | +0.064 |
| `markets-resid` | FTSE | -0.059 |
| `markets-resid` | GDAXI | -0.136 |
| `coins-resid` | ltc | -0.103 |
| `coins-resid` | xrp | +0.021 |
| `coins-resid` | bch | +0.124 |
| `coins-resid` | etc | -0.135 |
| `coins-resid` | xlm | +0.057 |
| `coins-resid` | dash | -0.015 |
| `coins-resid` | coins with S > 0 (of those with a year of cells) | 52 of 166 |
| `six` | BTC | +0.363 |
| `six` | ETH | +0.427 |
| `six` | SPY | +0.096 |
| `six` | QQQ | +0.109 |
| `six` | GLD | +0.031 |
| `six` | TLT | -0.034 |

## S per asset, 4 weeks (descriptive)

| Set | Asset | S |
|---|---|---:|
| `before` | GSPC | +0.002 |
| `before` | N225 | +0.013 |
| `before` | FTSE | -0.008 |
| `before` | GDAXI | -0.140 |
| `markets` | IWM | +0.037 |
| `markets` | EFA | +0.049 |
| `markets` | EEM | +0.085 |
| `markets` | VNQ | +0.050 |
| `markets` | DBC | +0.177 |
| `markets` | SLV | +0.087 |
| `markets` | XLK | +0.056 |
| `markets` | XLF | +0.001 |
| `markets` | XLE | +0.034 |
| `markets` | XLV | +0.009 |
| `markets` | XLY | +0.025 |
| `markets` | XLP | -0.013 |
| `markets` | XLI | +0.032 |
| `markets` | XLB | +0.061 |
| `markets` | XLU | +0.012 |
| `markets` | N225 | +0.038 |
| `markets` | FTSE | -0.012 |
| `markets` | GDAXI | -0.019 |
| `coins` | ltc | +0.134 |
| `coins` | xrp | -0.005 |
| `coins` | bch | +0.220 |
| `coins` | etc | +0.051 |
| `coins` | xlm | +0.081 |
| `coins` | dash | +0.167 |
| `coins` | coins with S > 0 (of those with a year of cells) | 153 of 170 |
| `markets-resid` | IWM | +0.003 |
| `markets-resid` | EFA | -0.009 |
| `markets-resid` | EEM | +0.053 |
| `markets-resid` | VNQ | +0.007 |
| `markets-resid` | DBC | +0.158 |
| `markets-resid` | SLV | +0.073 |
| `markets-resid` | XLK | +0.044 |
| `markets-resid` | XLF | -0.064 |
| `markets-resid` | XLE | +0.011 |
| `markets-resid` | XLV | -0.035 |
| `markets-resid` | XLY | -0.026 |
| `markets-resid` | XLP | -0.056 |
| `markets-resid` | XLI | -0.011 |
| `markets-resid` | XLB | +0.047 |
| `markets-resid` | XLU | -0.009 |
| `markets-resid` | N225 | +0.014 |
| `markets-resid` | FTSE | -0.062 |
| `markets-resid` | GDAXI | -0.080 |
| `coins-resid` | ltc | -0.070 |
| `coins-resid` | xrp | -0.156 |
| `coins-resid` | bch | +0.063 |
| `coins-resid` | etc | -0.151 |
| `coins-resid` | xlm | -0.092 |
| `coins-resid` | dash | +0.031 |
| `coins-resid` | coins with S > 0 (of those with a year of cells) | 70 of 170 |
| `six` | BTC | +0.211 |
| `six` | ETH | +0.195 |
| `six` | SPY | +0.041 |
| `six` | QQQ | +0.059 |
| `six` | GLD | +0.032 |
| `six` | TLT | -0.065 |

## Robustness (run with the same rotations; cannot change the verdict)

### 13 weeks

| Set | From | To | Weeks | Cells | Assets | S | p | Null sd | N eff | Detectable | Non-overlap | Basket S (p) | WF pool | WF per | Blocks with the card's sign |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---|
| coins: the protocol's six, gym bars | 2017-08-18 | 2025-08-08 | 417 | 2010 | 6 | +0.319 | 0.002 | 0.116 | 74 | 0.289 | +0.324 (+0.10..+0.47) | +0.365 (0.003) | +0.338 | +0.273 | 2 of 2 |
| before: from 1974 | 1974-01-04 | 1999-10-01 | 1344 | 4020 | 4 | +0.019 | 0.397 | 0.066 | 231 | 0.163 | +0.020 (-0.02..+0.07) | +0.033 (0.339) | -0.085 | +0.007 | 8 of 11 |
| markets: Fed broad index (2006+) | 2006-04-14 | 2025-08-08 | 1009 | 18064 | 18 | +0.023 | 0.359 | 0.071 | 200 | 0.176 | +0.026 (-0.03..+0.11) | +0.032 (0.353) | -0.060 | -0.019 | 8 of 8 |
| coins: Fed broad index (2006+) | 2017-04-28 | 2025-08-08 | 433 | 30307 | 292 | +0.222 | 0.029 | 0.120 | 69 | 0.299 | +0.220 (+0.00..+0.39) | +0.284 (0.018) | +0.203 |  | 2 of 2 |
| left out: IEF from 2000 | 2003-08-01 | 2025-08-08 | 1150 | 1150 | 1 | -0.044 | 0.660 | 0.090 | 123 | 0.224 | -0.042 (-0.14..+0.04) | -0.044 (0.660) | -0.052 |  | 1 of 9 |
| left out: LQD from 2000 | 2003-08-01 | 2025-08-08 | 1150 | 1150 | 1 | +0.002 | 0.487 | 0.096 | 108 | 0.239 | +0.006 (-0.09..+0.11) | +0.002 (0.487) | -0.098 |  | 5 of 9 |
| left out: GSPC from 2000 | 2000-01-07 | 2025-08-08 | 1336 | 1336 | 1 | +0.096 | 0.111 | 0.076 | 172 | 0.189 | +0.096 (+0.02..+0.20) | +0.096 (0.111) | +0.067 |  | 10 of 11 |

### 4 weeks

| Set | From | To | Weeks | Cells | Assets | S | p | Null sd | N eff | Detectable | Non-overlap | Basket S (p) | WF pool | WF per | Blocks with the card's sign |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---:|---:|---|
| coins: the protocol's six, gym bars | 2017-08-18 | 2025-10-10 | 426 | 2064 | 6 | +0.107 | 0.052 | 0.073 | 189 | 0.181 | +0.108 (+0.08..+0.14) | +0.108 (0.085) | +0.120 | +0.109 | 2 of 2 |
| before: from 1974 | 1974-01-04 | 1999-12-03 | 1353 | 4056 | 4 | -0.009 | 0.591 | 0.043 | 536 | 0.107 | -0.008 (-0.03..+0.00) | +0.004 (0.480) | -0.026 | +0.013 | 7 of 11 |
| markets: Fed broad index (2006+) | 2006-04-14 | 2025-10-10 | 1018 | 18226 | 18 | +0.018 | 0.305 | 0.043 | 539 | 0.107 | +0.018 (-0.00..+0.04) | +0.024 (0.310) | -0.032 | -0.020 | 8 of 8 |
| coins: Fed broad index (2006+) | 2017-04-28 | 2025-10-10 | 442 | 31189 | 297 | +0.130 | 0.058 | 0.080 | 157 | 0.198 | +0.129 (+0.09..+0.17) | +0.150 (0.051) | +0.146 |  | 2 of 2 |
| left out: IEF from 2000 | 2003-08-01 | 2025-10-10 | 1159 | 1159 | 1 | -0.062 | 0.844 | 0.060 | 281 | 0.148 | -0.062 (-0.09..-0.04) | -0.062 (0.844) | -0.016 |  | 1 of 9 |
| left out: LQD from 2000 | 2003-08-01 | 2025-10-10 | 1159 | 1159 | 1 | +0.015 | 0.402 | 0.061 | 273 | 0.150 | +0.016 (+0.01..+0.03) | +0.015 (0.402) | -0.020 |  | 8 of 9 |
| left out: GSPC from 2000 | 2000-01-07 | 2025-10-10 | 1345 | 1345 | 1 | +0.036 | 0.205 | 0.046 | 478 | 0.114 | +0.036 (+0.02..+0.07) | +0.036 (0.205) | -0.028 |  | 8 of 11 |

Fridays inside a Fed series' span with no value under the 21-day rule, carried forward: {'DTWEXBGS': 0}.
