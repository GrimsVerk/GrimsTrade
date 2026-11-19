# Wash-sale echo: event-study gate (wide-7, W14)

Rule: `research/wide-7.md` (pushed before this ran). Script
`research/lib/wide7_washsale.py`.
Slope b of a window's log return on the November YTD loss L = max(0, -YTD), year fixed
effects, t clustered by year (no small-sample correction). Echo = calendar days
S+31..S+45 after the third Friday of December S; turn of year = 31 Dec..10 Jan; late
placebo = S+46..S+60.

## Gate

| Test | b (t) | Needed |
|---|---:|---|
| ETF echo, tax years 1993-2011 | -0.003 (-0.07) | b > 0, t >= 2 |
| ETF echo, tax years 2012-2024 | +0.023 (+0.43) | b > 0, t >= 2 |
| Coin echo b below ETF echo b (all years) | +0.049 vs +0.006 | yes |

**Gate: fail.**

## Shown

| Sample | Asset-years (with a loss, years) | Echo | Turn of year | Late placebo | Echo on YTD | Echo, no year effects |
|---|---|---:|---:|---:|---:|---:|
| ETF in-sample 1993-2011 | 227 (66, 18) | -0.003 (-0.07) | +0.043 (+0.98) | -0.154 (-4.09) | -0.017 (-0.57) | -0.044 (-1.77) |
| ETF post-sample 2012-2024 | 273 (73, 13) | +0.023 (+0.43) | +0.089 (+3.91) | +0.112 (+2.48) | +0.008 (+0.24) | +0.018 (+0.45) |
| ETF all 1993-2024 | 500 (139, 31) | +0.006 (+0.17) | +0.059 (+1.75) | -0.061 (-1.16) | -0.005 (-0.22) | -0.034 (-1.31) |
| Coins 2013-2018 | 12 (6, 6) | +0.016 (+181289773322726.09) | -0.046 (-209781925382886.25) | +0.062 (+244477388554256.00) | +0.013 (+0.76) | +0.032 (+0.88) |
| Coins 2019-2024 | 46 (12, 6) | +0.088 (+7.09) | -0.135 (-3.60) | -0.080 (-1.24) | +0.053 (+1.32) | +0.139 (+2.66) |
| Coins all | 58 (18, 12) | +0.049 (+2.01) | -0.086 (-3.20) | -0.002 (-0.05) | +0.044 (+1.38) | +0.056 (+1.33) |

Echo on YTD: the slope on the signed YTD return (a positive slope on a loss is a
negative slope on YTD).

## Mean echo return of losers minus non-losers, by tax year (ETFs, bps)

| Tax year | Losers | Others | Losers minus others |
|---|---:|---:|---:|
| 1999 | 2 | 8 | +580 |
| 2000 | 6 | 5 | +237 |
| 2001 | 10 | 2 | -807 |
| 2002 | 12 | 1 | -191 |
| 2004 | 1 | 16 | -189 |
| 2005 | 1 | 18 | -144 |
| 2007 | 4 | 17 | +822 |
| 2008 | 19 | 2 | +292 |
| 2009 | 2 | 19 | +492 |
| 2010 | 2 | 19 | -11 |
| 2011 | 6 | 15 | +85 |
| 2013 | 7 | 14 | +407 |
| 2014 | 5 | 16 | +12 |
| 2015 | 10 | 11 | +45 |
| 2016 | 2 | 19 | -130 |
| 2017 | 1 | 20 | -273 |
| 2018 | 12 | 9 | -76 |
| 2020 | 5 | 16 | -272 |
| 2021 | 6 | 15 | +179 |
| 2022 | 17 | 4 | +229 |
| 2023 | 7 | 14 | -147 |
| 2024 | 1 | 20 | +96 |
