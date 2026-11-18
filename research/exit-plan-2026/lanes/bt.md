# Lane bt: backtests of exit rules, and where the indicators stand now

Lane `bt` of the exit-plan-2026 run, 2026-11-18. Research only, fake money. Card (written and
pushed before any number): `research/cards/exit-rules.md`. Scripts:
`research/exit-plan-2026/scripts/bt_*.py`. Result tables as CSV: `lanes/bt-data/`. Every run is
a row in `research/tries.md` (ideas `exit-window` and `exit-rules`, 2026-11-18).

## Bottom line for the investor

1. **Selling in steps beats both "sell everything now" and "wait for a better price" for this
   situation, but the gain is small.** In past states like late 2026 (expensive market by
   CAPE, index near its high after a big two-year rise), selling in 5 weekly tranches or
   half now / half in mid-December gained on average +0.3 to +0.4% over selling everything on
   day 0. What staging really buys is a smaller worst case. Waiting and selling everything in
   mid-December was more than 5% worse than day 0 in 7% of cases. Staging cut that to under 1%.
2. **"Wait for a higher price" (a limit 3-5% above today) is the risky choice.** It gets the
   higher price in about two out of three windows. But when a fall does come inside the
   window, it ends up selling low on the fallback date: on average -8 to -9% in those
   windows, against -5% for staging. Its worst cases are no better than doing nothing.
3. **No trigger reliably beats staging inside a 6-week window.** The 50-day-average trigger
   cuts the bad tail but has a median just below 0 (it sells on ordinary dips). The 200-day
   and trailing-stop triggers rarely fire within 22 days of a calm high, so they behave like
   waiting until the fallback date. Triggers help only if a real fall starts inside the window.
4. **Over years, the classic trend rules work as crash insurance, not as profit.** The 200-day
   and 10-month averages got out of all 8 big falls since 1929 with between -6% and -28% instead
   of -25% to -86%. Over 1928-2025 they ended level with buy-and-hold on return, with a max
   drawdown of 54% instead of 86%. They cost 2-3.5% a year in normal years, and 70-90% of
   their exits were false alarms. CAPE only says the market is expensive, not when it will
   fall: as an exit rule it was out years early and missed whole bull markets.
4b. **Best combination tested (post hoc, in the amendment): stage, and speed up on a 200-day
   break.** Sell half now; sell the rest on 18 Dec, or the day after the index closes below
   its 200-day average, whichever comes first. In calm states this kept staging's median. If
   a 10% fall came inside the window, the average loss dropped from about -5% to -1.4%.
5. **Today (17 Nov 2026 close) a correction is already under way in the US.** The S&P 500 is
   6.1% below its 6 Oct high and sits exactly on its 200-day average (-0.05%). The Nasdaq is
   11.9% below its high and under its 200-day line. VIX is 25.5 and the VIX curve is inverted
   (VIX/VIX3M 1.02). Credit is calm (HYG/LQD above its 200-day line, Baa spread near its
   1-year low). CAPE is 39.4, the 98th percentile of all months since 1881. Oslo (OSEBX) is
   only 3.3% below its 30 Oct high and 3.2% above its 200-day line.

## Data and dates (exact)

| Series | Source | Range used |
|---|---|---|
| S&P 500 price index `^GSPC` | Yahoo chart cache 2026-11-12, refreshed 2026-11-18 | 1927-12-30 .. 2025-11-07 (tests); .. 2026-11-17 (readings) |
| Nasdaq Composite `^IXIC` | Yahoo, same | 1971-02-05 .. 2025-11-07; .. 2026-11-17 |
| OSEBX `OSEBX.OL`, OBX `OBX.OL` | Yahoo (refresh 2026-11-18) | OSEBX 2013-03-05 .., OBX 2004-09-27 .. (`^OSEAX` not served) |
| VIX | CBOE `VIX_History.csv` (2026-11-12) + Yahoo `^VIX` after | 1990-01-02 .. |
| VIX3M | Yahoo `^VIX3M` + CBOE file | 2006-07-17 .. |
| HYG/LQD | Yahoo | 2007-04-11 .. |
| Baa - 10y spread | FRED `BAA10Y` cache 2026-11-13 | 1986-01-02 .. 2026-11-10 |
| CAPE | Shiller `ie_data.xls` (shillerdata.com, cached 2026-11-12) | 1871 .. 2026-11 |

- Tests use only the repo's train period: decisions and Part A windows end by 2025-11-09. The
  held-out year was not used. Part C (readings) uses the latest data, as a description only.
- Prices are index levels without dividends, and cash earns 0 (protocol). Over a 6-week window
  the dividend is about 0.1%. Over decades it biases against buy-and-hold (it misses about
  2-4% a year of dividends) and against the timing rules (they miss T-bill interest). For the
  S&P, the two roughly offset.
- CAPE is rebuilt with earnings lagged 3 months: real price(m) / mean real earnings of months
  m-122..m-3. A month's value is used from the 1st of the next month.
- Execution: a signal at the close of day t trades at the close of day t+1. Index opens before
  about 1962 are not real prices, so closes are used throughout. Limit sales are booked at
  the limit price on the first close at or above it.
- Oslo indexes: OSEBX and OBX are, as far as I know, total-return indexes (dividends
  reinvested). This was not verified here. Their history is short: 2004/2013 on, so about
  10-15 "late" spells.
- Not modelled: currency moves for a euro investor in non-euro assets (e.g. NOK/EUR for Oslo
  holdings), fund pricing, spreads, fees.

## Part A: the decision at hand (sell inside ~28 trading days)

Set-up (card): day 0 = any trading day; P0 = its close. Fallback = trading day 22 (the 18 Dec
2026 close at Oslo, counted from 18 Nov); the last day is 28 (30 Dec). The outcome is
R = average sale price / P0. "now" sells everything at P0 (R = 1).

The 11 strategies:

- `fallback`: hold, then sell everything on day 22.
- `staged5`: 5 weekly tranches, on days 0, 5, 10, 15 and 20.
- `staged-half`: half on day 0, half on day 22.
- `trig-sma200` / `trig-sma50`: sell everything the day after the first close below the
  200-day / 50-day average, else on day 22.
- `trig-trail5` / `trig-trail8`: sell everything after a close 5% / 8% below the highest close
  since day 0, else on day 22.
- `trig-vix`: sell everything after VIX closes above 1.3 x its 50-day average, else on day 22.
- `limit3` / `limit5`: sell at +3% / +5% above P0 if reached, else on day 22.
- `bracket`: +3% limit or the 5% trailing stop, whichever comes first, else on day 22.

Samples (states at day 0, fixed on the card):

- `late` = lagged CAPE in the top 10% of its history so far, AND index within 5% of its
  all-time high, AND up at least 25% over 2 years. This was chosen to match November 2026 as
  it looked before the current pull-back.
- `crash-window` (uses the future, so it is a scenario, not a state): windows where the index
  fell at least 10% below P0 at some close.
- `now-like` (post hoc, defined after the Part C readings, logged as `robustness`): CAPE top
  10%, index 4-12% below a high set within the last 63 days, and up at least 15% over 2 years.

How many independent windows: "all" S&P = ~868 non-overlapping windows. `late` = 2,739 start
days = ~98 windows, but from only 20 separate spells, and those cluster in 1929, the 1960s,
1996-2000 and 2017-2025. Treat the conditional results as a few dozen observations, not
thousands.

**S&P 500, all start days 1929-2025** (R-1 in %; P in % of start days; `trig-vix` 1990 on only:
8,954 of 24,301 days)

| strategy | mean | median | p05 | p95 | P<-5% | P<-10% | P>0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| now | +0.00 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | 0.0 |
| fallback | +0.66 | +1.06 | -7.75 | +7.82 | 10.8 | 3.1 | 60.1 |
| staged5 | +0.30 | +0.48 | -4.09 | +4.12 | 3.4 | 0.6 | 59.1 |
| staged-half | +0.33 | +0.53 | -3.88 | +3.91 | 3.1 | 0.6 | 60.1 |
| trig-sma200 | +0.54 | +0.32 | -4.67 | +6.03 | 4.4 | 0.6 | 56.0 |
| trig-sma50 | +0.33 | +0.00 | -3.87 | +5.50 | 2.4 | 0.1 | 49.7 |
| trig-trail5 | +0.60 | +0.76 | -6.23 | +7.48 | 11.0 | 0.5 | 56.5 |
| trig-trail8 | +0.65 | +1.00 | -7.86 | +7.62 | 12.5 | 1.6 | 59.3 |
| trig-vix | +0.57 | +0.78 | -6.31 | +6.66 | 8.2 | 1.0 | 58.3 |
| limit3 | +0.18 | +2.01 | -7.28 | +3.00 | 9.7 | 2.7 | 64.9 |
| limit5 | +0.40 | +1.24 | -7.58 | +5.00 | 10.4 | 2.9 | 61.4 |
| bracket | +0.17 | +1.71 | -6.19 | +3.00 | 10.7 | 0.5 | 61.9 |

**S&P 500, `late` sample** (2,739 start days, ~98 windows, 20 spells; the `trig-vix` row covers
1990 on only, 2,340 of the 2,739 days, because VIX starts in 1990)

| strategy | mean | median | p05 | p95 | P<-5% | P<-10% | P>0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| now | +0.00 | +0.00 | +0.00 | +0.00 | 0.0 | 0.0 | 0.0 |
| fallback | +0.71 | +1.06 | -5.69 | +5.83 | 7.1 | 0.4 | 63.5 |
| staged5 | +0.31 | +0.48 | -3.05 | +3.13 | 0.6 | 0.0 | 61.6 |
| staged-half | +0.36 | +0.53 | -2.85 | +2.91 | 0.4 | 0.1 | 63.5 |
| trig-sma200 | +0.67 | +0.99 | -5.57 | +5.81 | 7.4 | 0.3 | 62.0 |
| trig-sma50 | +0.12 | -0.13 | -4.06 | +5.31 | 3.0 | 0.0 | 48.1 |
| trig-trail5 | +0.57 | +0.96 | -5.66 | +5.81 | 8.1 | 0.3 | 61.3 |
| trig-trail8 | +0.66 | +1.06 | -6.38 | +5.83 | 8.8 | 0.5 | 63.5 |
| trig-vix | +0.45 | +0.77 | -6.10 | +6.05 | 8.6 | 0.2 | 57.7 |
| limit3 | +0.45 | +1.36 | -5.68 | +3.00 | 6.9 | 0.4 | 65.8 |
| limit5 | +0.64 | +1.07 | -5.69 | +5.00 | 7.1 | 0.4 | 63.6 |
| bracket | +0.33 | +1.28 | -5.59 | +3.00 | 7.9 | 0.3 | 63.9 |

**S&P 500, `now-like` sample (post hoc)** (703 start days, ~25 windows, 44 spells; `trig-vix`
605 days, 1990 on)

| strategy | mean | median | p05 | p95 | P<-5% | P<-10% | P>0 |
|---|---:|---:|---:|---:|---:|---:|---:|
| fallback | +1.43 | +2.25 | -7.64 | +8.88 | 10.7 | 1.7 | 65.6 |
| staged5 | +0.63 | +0.71 | -3.97 | +4.97 | 2.7 | 0.4 | 62.7 |
| staged-half | +0.71 | +1.13 | -3.82 | +4.44 | 1.7 | 0.3 | 65.6 |
| trig-sma200 | +0.77 | +0.30 | -4.83 | +7.60 | 3.8 | 0.0 | 54.3 |
| trig-sma50 | +0.13 | +0.11 | -2.73 | +2.70 | 0.1 | 0.0 | 54.8 |
| trig-trail5 | +0.90 | +1.34 | -6.46 | +8.88 | 10.4 | 2.7 | 57.3 |
| trig-trail8 | +1.10 | +2.20 | -9.45 | +8.88 | 14.7 | 4.1 | 64.7 |
| trig-vix | +0.64 | +0.72 | -8.84 | +8.67 | 12.1 | 3.0 | 57.4 |
| limit3 | +0.75 | +3.00 | -7.40 | +3.00 | 9.4 | 1.4 | 72.4 |
| limit5 | +1.09 | +2.52 | -7.61 | +5.00 | 10.2 | 1.6 | 66.6 |
| bracket | +0.39 | +3.00 | -6.29 | +3.00 | 10.0 | 2.7 | 67.6 |

After a fresh 4-12% pull-back in an expensive market, the next month was on average slightly
up (dips were bought; mean +1.4% for waiting). The bad tail was just as fat: 1 in 10 windows
was more than 5% worse. In this sample the index is often already below its 50-day average on
day 0, so `trig-sma50` sells at once and behaves like "now".

**If a fall of 10%+ does come inside the window** (S&P `crash-window`, ex post scenario, ~62
windows)

| strategy | mean | median | p05 | P<-5% | P<-10% |
|---|---:|---:|---:|---:|---:|
| now | 0.00 | 0.00 | 0.00 | 0.0 | 0.0 |
| fallback | -10.05 | -9.12 | -23.69 | 81.7 | 42.9 |
| staged5 | -5.12 | -4.70 | -12.08 | 45.6 | 8.5 |
| staged-half | -5.03 | -4.56 | -11.85 | 42.9 | 8.0 |
| trig-sma200 | -2.81 | -1.47 | -11.85 | 25.1 | 7.8 |
| trig-sma50 | -2.04 | -1.54 | -7.76 | 15.7 | 1.6 |
| trig-trail5 | -5.91 | -5.76 | -10.98 | 62.8 | 7.7 |
| trig-trail8 | -8.05 | -8.08 | -13.09 | 85.5 | 23.0 |
| trig-vix | -5.83 | -6.24 | -11.77 | 61.0 | 15.7 |
| limit3 | -8.38 | -8.41 | -23.20 | 71.0 | 38.0 |
| limit5 | -9.20 | -8.85 | -23.55 | 77.6 | 40.7 |
| bracket | -5.06 | -5.64 | -10.71 | 60.3 | 7.1 |

**Robustness: 5th percentile / median of R-1 (%)**

| index/sample | fallback | staged5 | staged-half | trig-sma50 | bracket |
|---|---:|---:|---:|---:|---:|
| GSPC all | -7.8 / +1.1 | -4.1 / +0.5 | -3.9 / +0.5 | -3.9 / +0.0 | -6.2 / +1.7 |
| GSPC all-1928-1989 | -8.4 / +0.9 | -4.4 / +0.4 | -4.2 / +0.5 | -3.9 / -0.0 | -6.3 / +1.6 |
| GSPC all-1990-2025 | -6.8 / +1.3 | -3.7 / +0.6 | -3.4 / +0.6 | -3.8 / +0.1 | -5.9 / +1.8 |
| GSPC cape-hi | -7.2 / +1.0 | -3.9 / +0.4 | -3.6 / +0.5 | -3.7 / +0.0 | -6.1 / +1.4 |
| GSPC runup | -6.0 / +0.8 | -3.2 / +0.3 | -3.0 / +0.4 | -4.2 / -0.3 | -5.8 / +1.1 |
| GSPC lowvix | -4.2 / +1.0 | -2.3 / +0.5 | -2.1 / +0.5 | -3.4 / +0.0 | -4.6 / +1.1 |
| GSPC late | -5.7 / +1.1 | -3.0 / +0.5 | -2.8 / +0.5 | -4.1 / -0.1 | -5.6 / +1.3 |
| GSPC late-1990-2025 | -5.9 / +1.2 | -3.2 / +0.6 | -2.9 / +0.6 | -4.3 / -0.0 | -5.7 / +1.6 |
| IXIC all | -9.5 / +1.5 | -5.1 / +0.7 | -4.7 / +0.8 | -4.6 / +0.2 | -6.7 / +3.0 |
| IXIC late | -8.1 / +1.6 | -4.3 / +1.0 | -4.1 / +0.8 | -6.4 / +0.8 | -6.7 / +3.0 |
| IXIC now-like (post hoc) | -10.0 / +2.8 | -5.3 / +1.1 | -5.0 / +1.4 | -4.3 / -0.0 | -7.1 / +3.0 |
| OBX all | -8.8 / +1.3 | -4.6 / +0.6 | -4.4 / +0.7 | -5.1 / -0.1 | -6.4 / +2.8 |
| OBX late | -6.9 / +0.5 | -4.0 / +0.3 | -3.5 / +0.3 | -5.5 / -0.5 | -6.0 / +0.9 |
| OSEBX all | -6.1 / +1.1 | -3.3 / +0.5 | -3.0 / +0.5 | -3.9 / -0.1 | -5.5 / +1.5 |
| OSEBX late (= runup here) | -6.5 / +0.4 | -3.9 / +0.2 | -3.3 / +0.2 | -5.1 / -0.5 | -5.9 / +0.6 |

**Verdict against the card's bar** (beats selling now only if p05 >= -5% AND median > 0 in
`late`, on both the S&P and the Nasdaq):

- `staged5` and `staged-half` pass. The S&P is -3.1/+0.5 and -2.9/+0.5; the Nasdaq is
  -4.3/+1.0 and -4.1/+0.8. Both also hold on OBX/OSEBX.
- Every other strategy fails. `trig-sma50` has a median below 0. All the others have a 5th
  percentile below -5%, though several only just (-5.6 to -5.7 on the S&P).
- The pass is about risk, not money: the mean gain over "now" is 0.3-0.6 points.

Plain language: there is no timing edge to find inside six weeks. Expected drift is +0.5 to
+1% a month, smaller than one bad day. The choice is between a certain price today and a
spread of outcomes around a slightly higher average. Staging keeps most of that small upside
and removes most of the regret risk.

## Part B: classic exit rules on crash episodes

S&P 500 1928-2025, long or cash. 11 rules; buy-and-hold is the baseline.

- `sma10m`: out when the month-end close is below its 10-month average.
- `sma200d`: out when the daily close is below its 200-day average.
- `tsmom12`: out when the month-end close is below the close 12 months earlier.
- `dd8` / `dd10`: out when the close is 8% / 10% below the high since the later of 252 days
  ago and the last re-entry; back in above the 50-day average.
- `vix30`: out when VIX closes above 30, back in below 20.
- `vixts`: out when VIX/VIX3M closes above 1.0, back in below 0.9.
- `baa`: out when the 20-day mean of the Baa spread is 0.5 points above its 1-year low.
- `hyglqd`: out when HYG/LQD is below its 200-day average.
- `cape30`: out when lagged CAPE is above 30.
- `capepct`: out when lagged CAPE is in the top 5% of its history.

Rules whose data start later (VIX 1990, Baa 1986, VIX3M 2006, HYG 2007) are invested before
their data exist. That is why they show "-" and the full fall in early episodes: this is
missing data, not evidence.

The episodes (S&P 500 closes, peak to trough):

- 1929: 1929-09-16 .. 1932-06-01, -86%
- 1937: 1937-03-10 .. 1938-03-31, -54%
- 1973-74: 1973-01-11 .. 1974-10-03, -48%
- 1987: 1987-08-25 .. 1987-12-04, -34%
- 2000-02: 2000-03-24 .. 2002-10-09, -49%
- 2007-09: 2007-10-09 .. 2009-03-09, -57%
- 2020: 2020-02-19 .. 2020-03-23, -34%
- 2022: 2022-01-03 .. 2022-10-12, -25%

**Return of the rule from peak to trough, in %, re-entries included** (buy-and-hold = the fall)

| rule | 1929 | 1937 | 1973-74 | 1987 | 2000-02 | 2007-09 | 2020 | 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| buyhold | -86 | -54 | -48 | -34 | -49 | -57 | -34 | -25 |
| sma10m | -28 | -12 | -8 | -24 | -11 | -6 | -9 | -18 |
| sma200d | -19 | -17 | -12 | -16 | -14 | -11 | -11 | -15 |
| tsmom12 | -34 | -27 | -13 | -31 | -14 | -11 | -34 | -13 |
| dd8 | -35 | -18 | -34 | -7 | -40 | -31 | -13 | -22 |
| dd10 | -49 | -27 | -34 | -16 | -38 | -40 | -13 | -19 |
| vix30 | (-86) | (-54) | (-48) | (-34) | -41 | -26 | -13 | -32 |
| vixts | (-86) | (-54) | (-48) | (-34) | (-49) | -17 | -8 | -25 |
| baa | (-86) | (-54) | (-48) | -28 | -45 | -8 | -29 | -23 |
| hyglqd | (-86) | (-54) | (-48) | (-34) | (-49) | -20 | +0 | -28 |
| cape30 | -79 | -54 | -48 | -34 | -23 | -57 | +0 | -3 |
| capepct | -77 | -54 | -48 | -34 | -18 | -57 | +0 | -14 |

(Brackets = no data yet for that rule.)

**Share of the fall avoided by the first exit** ((exit price - trough) / (peak - trough))

| rule | 1929 | 1937 | 1973-74 | 1987 | 2000-02 | 2007-09 | 2020 | 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sma10m | 0.67 | 0.78 | 0.84 | 0.28 | 0.88 | 0.90 | 0.74 | 0.60 |
| sma200d | 0.78 | 0.75 | 0.78 | 0.52 | 0.77 | 0.89 | 0.62 | 0.68 |
| tsmom12 | 0.60 | 0.51 | 0.77 | 0.07 | 0.72 | 0.81 | 0.00 | 0.47 |
| dd8 | 0.88 | 0.83 | 0.80 | 0.80 | 0.77 | 0.82 | 0.62 | 0.68 |
| dd10 | 0.95 | 0.78 | 0.77 | 0.52 | 0.83 | 0.85 | 0.62 | 0.53 |
| vix30 | - | - | - | - | 0.83 | 0.83 | 0.62 | 0.82 |
| vixts | - | - | - | - | 0.00 | 0.92 | 0.90 | 0.82 |
| baa | - | - | - | 0.17 | 0.95 | 0.91 | 0.14 | 0.64 |
| hyglqd | - | - | - | - | - | 0.74 | 0.34 | 0.67 |
| cape30 | 0.92 | 0.00 | 0.00 | 0.00 | 0.09 | 0.00 | 0.74 | 0.00 |
| capepct | 0.61 | 0.00 | 0.00 | 0.00 | -0.33 | 0.00 | 0.74 | 0.00 |

**Lag of the first exit, trading days after the peak** (negative = before the peak)

| rule | 1929 | 1937 | 1973-74 | 1987 | 2000-02 | 2007-09 | 2020 | 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| sma10m | 34 | 37 | 33 | 48 | 132 | 38 | 8 | 39 |
| sma200d | 28 | 32 | -57 | 37 | -23 | -45 | 7 | 14 |
| tsmom12 | 51 | 143 | 75 | 68 | 175 | 79 | - | 82 |
| dd8 | 14 | 20 | 48 | 34 | -23 | -38 | 7 | 14 |
| dd10 | 15 | 33 | 74 | 37 | 16 | 34 | 7 | 35 |
| vix30 | - | - | - | - | 16 | -37 | 7 | -21 |
| vixts | - | - | - | - | - | -73 | -15 | -21 |
| baa | - | - | - | 59 | 8 | -18 | 20 | 50 |
| hyglqd | - | - | - | - | - | 74 | -300 | -60 |
| cape30 | -30 | - | - | - | -709 | - | -52 | -336 |
| capepct | -257 | - | - | - | -1215 | - | -52 | -336 |

A negative lag means the rule was already out at the peak, often after an earlier exit and
re-entry. Read it together with the peak-to-trough return.

**Full sample** (S&P 500 1927-12-30 .. 2025-11-07; Nasdaq 1971-02-05 .. 2025-11-07). Columns:

- annual return, max DD, time invested, false alarms and normal-year cost are in %.
- Sharpe: calendar days, zero risk-free rate (repo convention).
- Whipsaws are round trips where the rule bought back higher than it sold, with their average
  cost.
- False alarm: the index never fell 10% below the exit price before the rule bought back.
- Normal-year cost: the mean yearly gap to buy-and-hold in calendar years outside the episode
  windows (80 S&P years, 42 Nasdaq years).

| index | rule | ann. return | max DD | Sharpe | invested | trips/yr | whipsaws | avg whipsaw cost | false alarm | normal-year cost |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| GSPC | buyhold | 6.3 | 86.2 | 0.42 | 100 | 0 | 0 | - | - | 0 |
| GSPC | sma10m | 6.4 | 53.8 | 0.54 | 68 | 0.74 | 54 | 6.1 | 71 | -3.5 |
| GSPC | sma200d | 7.1 | 53.7 | 0.62 | 68 | 2.99 | 213 | 1.9 | 89 | -2.7 |
| GSPC | tsmom12 | 6.1 | 54.2 | 0.51 | 70 | 0.48 | 35 | 6.2 | 70 | -3.2 |
| GSPC | dd8 | 6.3 | 56.3 | 0.52 | 82 | 1.57 | 110 | 3.8 | 77 | -2.9 |
| GSPC | dd10 | 6.5 | 57.0 | 0.52 | 87 | 1.14 | 76 | 3.9 | 74 | -2.1 |
| GSPC | vix30 | 4.6 | 86.2 | 0.35 | 91 | 0.25 | 22 | 8.5 | 67 | -1.4 |
| GSPC | vixts | 5.3 | 86.2 | 0.38 | 94 | 0.55 | 45 | 3.3 | 87 | -1.2 |
| GSPC | baa | 5.0 | 86.2 | 0.37 | 90 | 0.31 | 20 | 10.9 | 87 | -1.4 |
| GSPC | hyglqd | 4.9 | 86.2 | 0.36 | 91 | 1.03 | 66 | 3.0 | 95 | -1.7 |
| GSPC | cape30 | 6.3 | 83.0 | 0.44 | 89 | 0.13 | 5 | 6.5 | 85 | -1.3 |
| GSPC | capepct | 5.2 | 79.9 | 0.38 | 82 | 0.15 | 8 | 15.8 | 80 | -2.5 |
| IXIC | buyhold | 10.4 | 77.9 | 0.59 | 100 | 0 | 0 | - | - | 0 |
| IXIC | sma10m | 9.2 | 52.1 | 0.68 | 71 | 0.77 | 32 | 8.6 | 74 | -6.6 |
| IXIC | sma200d | 10.0 | 56.7 | 0.78 | 71 | 2.76 | 114 | 2.6 | 86 | -6.3 |
| IXIC | tsmom12 | 9.8 | 53.4 | 0.67 | 77 | 0.40 | 17 | 7.9 | 59 | -5.2 |
| IXIC | dd8 | 11.9 | 39.0 | 0.87 | 80 | 1.79 | 63 | 3.9 | 76 | -3.3 |
| IXIC | dd10 | 11.3 | 50.3 | 0.80 | 83 | 1.39 | 48 | 4.5 | 71 | -3.7 |
| IXIC | vix30 | 6.4 | 68.6 | 0.50 | 85 | 0.44 | 23 | 12.0 | 63 | -4.2 |
| IXIC | vixts | 7.6 | 77.9 | 0.51 | 90 | 0.99 | 46 | 4.1 | 87 | -3.0 |
| IXIC | baa | 7.2 | 67.2 | 0.53 | 81 | 0.55 | 20 | 17.3 | 77 | -4.3 |
| IXIC | hyglqd | 6.9 | 77.9 | 0.47 | 83 | 1.84 | 69 | 3.9 | 93 | -4.2 |
| IXIC | cape30 | 10.2 | 59.9 | 0.71 | 80 | 0.22 | 2 | 4.0 | 75 | -4.7 |
| IXIC | capepct | 8.3 | 59.9 | 0.61 | 75 | 0.16 | 6 | 15.1 | 78 | -6.8 |

**Nasdaq 2000-03-10 .. 2002-10-09 (-78%)**: the rule's peak-to-trough return and the share
avoided by the first exit:

| rule | return | avoided |
|---|---:|---:|
| sma10m | -50% | 0.63 |
| sma200d | -51% | 0.62 |
| tsmom12 | -53% | 0.39 |
| dd8 | -38% | 0.70 |
| dd10 | -49% | 0.88 |
| vix30 | -68% | 0.62 |
| baa | -66% | 0.78 |
| vixts, hyglqd | -78% | no data |
| cape30 | -14% | out from June 1997, missing +100% first |
| capepct | -18% | out from June 1997, missing +100% first |

In the tech bust, every price rule still lost about half: the Nasdaq kept bouncing above its
averages, and each bounce bought back in.

**Verdicts against the card's bars:**

- "Useful in crashes" (avoided at least a third of the fall in at least 6 of 8 episodes):
  - Pass: `sma200d` (8/8), `dd8` (8/8), `dd10` (8/8), `sma10m` (7/8, it missed 1987),
    `tsmom12` (6/8, it missed 1987 and 2020).
  - VIX, credit and HYG rules cannot pass: no data for 3-5 of the episodes. Where data exist,
    `vix30`/`vixts` caught 2007-09, 2020 and 2022. `baa` caught 2000 and 2007 but was late in
    1987 and 2020.
  - CAPE rules fail (1-2 of 8). They exit years early and do not get back in.
- By the peak-to-trough return, which includes re-entries, the slow trend rules (`sma10m`,
  `sma200d`) protect best: -6% to -28%. The drawdown stops buy back too early in long bears
  (2000-02 -40%, 2007-09 -31/-40%).
- "Cheap in normal times" (whipsaw cost under 1% a year): no rule passes. Normal-year cost is
  1.2-3.5% a year on the S&P and 3-7% on the Nasdaq. False alarms are 70-95% of exits.
- Over 98 years the trend rules end level with buy-and-hold on return, with about a third less
  max drawdown. That is insurance with a premium, as in Faber (2007). It is not a free lunch.
- Eight episodes are eight observations. Without the repo's earlier results, the S&P full-sample
  Sharpe gaps (0.42 vs 0.54-0.62) would not be significant on their own either.

## Part C: current readings

Data: US to the 2026-11-17 close (the 18 Nov bar was intraday when fetched), Oslo to the
2026-11-18 close, Baa spread to 2026-11-10, Shiller to Nov 2026 (price = 12 Nov close).

| | S&P 500 | Nasdaq Comp | OSEBX | OBX |
|---|---:|---:|---:|---:|
| close | 7,340.53 | 24,328.38 | 2,073.85 | 1,980.71 |
| vs 50-day avg | -4.1% (7,655) | -7.4% (26,268) | -1.0% (2,095) | -1.4% (2,008) |
| vs 200-day avg | **-0.05%** (7,345) | -3.3% (25,146) | +3.2% (2,010) | +1.9% (1,943) |
| Oct month-end vs 10-month avg (Faber) | +3.8% (in) | +1.8% (in) | +7.2% | +6.6% |
| today vs live 10-month avg | -0.05% (7,344) | -3.0% (25,071) | +2.1% (2,032) | +0.9% (1,963) |
| from all-time high | -6.1% (high 6 Oct) | -11.9% (6 Oct) | -3.3% (30 Oct) | -3.8% (30 Oct) |
| 12-month return | +10.0% | +7.1% | +30.8% | +31.5% |
| 24-month return | +25.0% | +30.2% | +43.8% | +46.4% |

- VIX 25.46 (17 Nov), 1.44 x its 50-day mean (17.7), so `trig-vix` (>1.3x) is on. It is in
  the 94th percentile of the past year.
- VIX3M 24.98, so VIX/VIX3M = 1.019: the curve is inverted and `vixts` is out. It was 1.10 on
  5 Nov, 0.91-0.94 on 11-13 Nov, then 0.995 and 1.019.
- HYG/LQD is 0.88% above its 200-day average (in) and 0.3% below its 50-day.
- Baa - 10y spread: 1.51 (10 Nov). Its 20-day mean is 1.485, and the 1-year low of that mean
  is 1.446, so the `baa` rule turns hostile only above 1.95. Credit shows no stress.
- CAPE (Shiller, unlagged) is 39.37 for Nov 2026: the 98.3rd percentile of all months since
  1881. The only higher readings were 1999-2000 (max 44.2, Dec 1999). Lagged CAPE is 39.8.
- Part B rule states on the S&P 500 at the 17 Nov close:
  - Out: `sma200d` (by 0.05%, first close below), `vixts`, `cape30`, `capepct`.
  - In: `sma10m` (the decision in force, made at the 30 Oct close; next decision at the 30 Nov
    close; it is at the line now: the live value is -0.05%, "out" if the month ended today), `tsmom12`, `dd8`
    (needs a close below about 7,194, 8% under the 6 Oct high of about 7,819), `dd10`, `vix30` (needs VIX
    above 30), `baa`, `hyglqd`.
- On the Nasdaq, `dd8`/`dd10` are also out (since 2 Nov).
- The card's `late` state is no longer true for the S&P: it is more than 5% below its high. The
  post hoc `now-like` sample above is the closer analog.

## Practical reading for the playbook (this lane's view; the lead merges)

- **Base plan (passes the card's bar):** sell in steps. Either half now and half by 18 Dec,
  or one fifth each week from now to mid-December. Sell everything that is left by 18 Dec
  (day 22), leaving 30 Dec as a spare day.
- **Speed-up trigger (tested in the amendment below, post hoc):** if the index behind a holding
  closes below its 200-day average, sell everything still unsold the next day. Tested as
  `staged-half-sma200` / `staged5-sma200`, this keeps staging's small upside. If a fall comes
  inside the window, the loss drops from about -5% to about -1.5% (S&P `crash-window` mean).
  The 200-day line is also the trend rule that worked across all 8 crashes (Part B). Its
  whipsaws in normal times do not matter for a one-off sale.
- **Where that trigger stands today:** the S&P 500 closed 0.05% below its 200-day line on
  17 Nov (7,340.53 vs 7,344.53), so for US holdings it has just fired, by a hair. The
  Nasdaq is 3.3% below its line. OSEBX is 3.2% above its line (about 2,010) and OBX 1.9% above
  (about 1,943), so for Oslo holdings it has not fired.
- **Avoid:** a "sell only at a higher price" limit without a stop. If the fall comes, it sells
  low on the fallback date.
- **Do not wait for CAPE:** it has been "too high" since 2017.

## Amendment: tests suggested by the lit lane (card amendment 2026-11-18, post hoc)

Written on the card before these ran, but after Parts A-C had been seen. The variants are
counted, and they do not change the verdicts above. Script: `scripts/bt_amend.py`. CSVs:
`bt-data/amend-*.csv`.

**Part A, 3 new variants** (R-1 in %, p05 / median / mean; `crash-window` = mean)

| index | sample | staged3 | staged5-sma200 | staged-half-sma200 | (staged-half, for reference) |
|---|---|---:|---:|---:|---:|
| GSPC | all | -4.2 / +0.5 / +0.33 | -2.7 / +0.2 / +0.26 | -2.3 / +0.2 / +0.27 | -3.9 / +0.5 / +0.33 |
| GSPC | late | -3.0 / +0.5 / +0.35 | -3.1 / +0.5 / +0.29 | -2.8 / +0.5 / +0.33 | -2.9 / +0.5 / +0.36 |
| GSPC | now-like (post hoc) | -4.1 / +1.0 / +0.69 | -2.9 / +0.2 / +0.37 | -2.4 / +0.2 / +0.39 | -3.8 / +1.1 / +0.71 |
| GSPC | crash-window, mean | -5.33 | -1.60 | -1.40 | -5.03 |
| IXIC | late | -4.2 / +0.9 / +0.67 | -4.2 / +1.0 / +0.63 | -4.0 / +0.8 / +0.65 | -4.1 / +0.8 / +0.64 |
| IXIC | now-like (post hoc) | -5.6 / +1.4 / +0.84 | -4.8 / +0.9 / +0.68 | -4.8 / +1.2 / +0.92 | -5.0 / +1.4 / +1.02 |
| IXIC | crash-window, mean | -5.21 | -2.01 | -1.85 | -4.91 |
| OBX | late | -4.0 / +0.3 / +0.18 | -3.8 / +0.3 / +0.16 | -3.5 / +0.2 / +0.18 | -3.5 / +0.3 / +0.18 |
| OBX | crash-window, mean | -5.37 | -2.37 | -2.14 | -5.02 |
| OSEBX | late | -3.6 / +0.2 / +0.08 | -3.7 / +0.2 / +0.02 | -3.3 / +0.2 / +0.01 | -3.3 / +0.2 / +0.08 |
| OSEBX | crash-window, mean | -5.13 | -2.69 | -2.44 | -4.69 |

- All three new variants meet the card's bar in `late` on the S&P and the Nasdaq.
- Adding the 200-day speed-up to staging costs almost nothing in calm states: the same
  `late` median, mean about 0.02-0.03 points lower. When a 10% fall comes inside the window,
  it cuts the loss by about 3.5 points (S&P -1.4% vs -5.0%).
- This is the best trade-off between tail and upside among everything tested. But the
  combination was added after the first results, so its numbers are less clean than those of
  the card's original variants.
- `staged3` (thirds) behaves like `staged-half`.

**Part B, 5 new rules** (S&P 500 1928-2025; return from peak to trough in %)

| rule | 1929 | 1937 | 1973-74 | 1987 | 2000-02 | 2007-09 | 2018Q4 | 2020 | 2022 | ann. return | max DD | trips/yr | normal-year cost |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| buyhold | -86 | -54 | -48 | -34 | -49 | -57 | -20 | -34 | -25 | 6.3 | 86.2 | 0 | 0 |
| sma200d (Part B) | -19 | -17 | -12 | -16 | -14 | -11 | -8 | -11 | -15 | 7.1 | 53.7 | 2.99 | -2.7 |
| sma200d-b2 | -21 | -15 | -19 | -33 | -12 | -14 | -10 | -20 | -13 | 6.9 | 52.8 | 1.28 | -2.5 |
| sma200d-c2 | -19 | -15 | -14 | -33 | -11 | -11 | -9 | -9 | -16 | 6.8 | 52.0 | 1.68 | -2.8 |
| kl3m10 | -62 | -46 | -33 | -30 | -36 | -25 | -13 | -15 | -23 | 5.7 | 67.8 | 0.65 | -2.2 |
| rv2 | -85 | -41 | -43 | -30 | -45 | -32 | -4 | -13 | -25 | 5.7 | 85.4 | 0.57 | -1.5 |
| sma200d-rv | -35 | -26 | -21 | -16 | -42 | -20 | -8 | -11 | -18 | 6.9 | 52.0 | 0.95 | -1.9 |

- A 2% band or a 2-day confirmation on the 200-day rule halves the trips per year (3.0 to
  1.3-1.7) for about the same protection. The exception is 1987, where the band made the rule
  too late (-33% vs -16%).
- Kaminski-Lo-style (`kl3m10`) and a volatility spike alone (`rv2`) are clearly worse
  protection than the trend rules. Using volatility as a confirmer (`sma200d-rv`) cuts trades
  but let 2000-02 through (-42%).
- On the Nasdaq the picture is the same: the band and 2-day versions are -44% to -51% in
  2000-02, like the plain rule's -51%.
- 2018 Q4 (S&P -20%, Nasdaq -23%; original rules, added episode):
  - `sma200d`: -8% (S&P) and -16% (Nasdaq).
  - `vixts`: -7% and -9%.
  - `sma10m`: -21% and -8%.
  - `tsmom12` and `vix30` never got out.

**Oslo robustness** (OBX from 2004, OSEBX from 2013; return from peak to trough in %)

Episodes:

- OBX 2008: 2008-05-22 .. 2008-11-21, -65%.
- 2018 Q4: 2018-09-25 .. 2018-12-27, -18% (OBX) and -17% (OSEBX).
- 2020: 2020-01-17 .. 2020-03-16/23, -32% (OBX) and -33% (OSEBX).
- 2022: 2022-08-25 / 05-31 .. 2022-09-29, -15% (OBX) and -16% (OSEBX).

| rule | OBX 2008 | OBX 2018Q4 | OBX 2020 | OBX 2022 | OSEBX 2018Q4 | OSEBX 2020 | OSEBX 2022 |
|---|---:|---:|---:|---:|---:|---:|---:|
| buyhold | -65 | -18 | -32 | -15 | -17 | -33 | -16 |
| sma10m | -22 | -8 | -12 | -15 | -8 | -12 | -21 |
| sma200d | -15 | -12 | -6 | -11 | -11 | -11 | -17 |
| sma200d-c2 | -14 | -10 | -7 | -11 | -10 | -12 | -13 |
| tsmom12 | -13 | -18 | -12 | -15 | -17 | -12 | -16 |
| dd8 | -23 | -8 | -13 | -8 | -8 | -12 | -15 |
| baa | 0 | -13 | -32 | -6 | -13 | -33 | -11 |

- The trend rules protect Oslo in the big falls (2008, 2020) as they do the S&P. In shallow
  falls (2022, -15%) they gain little or lose more through whipsaws.
- Over the whole sample, every exit rule lagged buy-and-hold on Oslo: OBX 10.5% a year,
  `sma200d` 6.5%; OSEBX 10.0% vs 4.1%. These are short samples, but they show the insurance
  premium again.
- Calendar bug, not interpreted: `vix30`, `vixts` and `hyglqd` on the Oslo calendar re-enter
  on every US holiday, because a missing US value counts as "back in" (trips per year 2.5-7.7
  vs 0.3-1.0 on the S&P). Their Oslo rows in `tries.md` and `bt-data/amend-rules-full.csv` are
  invalid. On the S&P/Nasdaq calendar the effect is nil or tiny: VIX and US index days match.

**Greenwood-Shleifer-You screen** (descriptive, Ken French `HiTec` value-weighted, CRSP to
2026-09-30)

| month end | 2-year return | net of market | acceleration | 1-year change in vol |
|---|---:|---:|---:|---:|
| 2026-04 | +67% | +20% | +55% | -0.19 |
| 2026-05 | +73% | +25% | +59% | -0.22 |
| 2026-06 | +53% | +10% | +37% | -0.15 |
| 2026-07 | +54% | +14% | +29% | +0.08 |
| 2026-08 | +60% | +19% | +35% | +0.10 |
| 2026-09 | +62% | +25% | +32% | +0.05 |

- Months since 1926 with a 2-year HiTec return of at least 100% (GSY's flag):
  - Sustained spells: 1928-10..1929-10, 1936-07..1937-05, 1955, and 1999-01..2000-10 (the
    peak was +219% in Aug 2000).
  - Single months: 1997-01, 2011-02, 2020-12, 2021-08..10, 2024-09, 2024-12, 2025-10.
- Broad US tech in 2026 is up a lot but is not at 1999-2000 levels on this measure. It
  touched the flag in 2024-25.
- The narrower AI names are hotter. On 17 Nov 2026 the semiconductor index `^SOX` was +99.5%
  over 2 years, right at the flag, but already 34% below its 22 Jun 2026 high. XLK was 19%
  below its 6 Oct high.

**Checks requested by the lead (from the inv lane):**

- S&P 500 on 2026-11-05: confirmed, -4.36% that day (close-to-close, Yahoo `^GSPC`).
- Nvidia: confirmed, -35.0% from its 2026-10-06 close (239.24) to the 2026-11-17 close
  (155.46). It closed at 152.12 on 18 Nov, 36.4% below the high. Source: Yahoo `NVDA`,
  split-adjusted, fetched 2026-11-18.

## Review round 1 fixes (2026-11-18, card amendment 2)

The reviewer found that the card's `late` sample no longer fits the US indexes (S&P 500 -6.1%,
Nasdaq -11.9% from their 6 Oct highs at the 17 Nov close). Card amendment 2 (committed 19:30
UTC, before the run) added three post-hoc cuts by the day-0 state: `now-like` split
by the 200-day line for the S&P and the Nasdaq, and `late-above200` for OSEBX/OBX. Script
`scripts/bt_review1.py`, CSV `bt-data/review1-window.csv`, 18 `robustness` rows in `tries.md`
(19:31 UTC). All numbers below are train period (windows end by 2025-11-09).

### 1. Per holding type: which sample fits today, and the four ways to sell

R-1 in % against "sell everything on day 0" (so "sell all now" is 0 in every column). P = share
of start days more than 5% / 10% worse than day 0. "Card" = sample fixed on the card before any
number; "post hoc" = defined after seeing today's data. `staged-half-sma200` is itself a post-hoc
variant (amendment 1) in every row.

| Holding type (proxy index) | Sample that fits today (17/18 Nov) | Status | Way of selling | mean | median | p5 | P >5% worse | P >10% worse |
|---|---|---|---|---:|---:|---:|---:|---:|
| Oslo-listed shares or a Nordic fund (OSEBX) | `late`: -3.3% from 30 Oct high, +46% over 504 days, US CAPE top 10%; +3.2% above its 200-day line. 795 start days, ~28 windows, 10 spells, 2013-2025 | card sample, Oslo = robustness index | sell all now | 0 | 0 | 0 | 0 | 0 |
| | | | staged-half | +0.08 | +0.21 | -3.25 | 1.0% | 0.0% |
| | | | staged-half-sma200 | +0.01 | +0.16 | -3.26 | 0.0% | 0.0% |
| | | | hold to fallback | +0.16 | +0.43 | -6.51 | 9.3% | 1.0% |
| (cross-check: OBX, 2004-2025) | `late`, 1,256 days, 14 spells | as above | staged-half | +0.18 | +0.26 | -3.45 | 2.0% | 0.1% |
| | | | staged-half-sma200 | +0.18 | +0.23 | -3.54 | 1.0% | 0.0% |
| | | | hold to fallback | +0.37 | +0.51 | -6.91 | 9.6% | 2.0% |
| Global index fund (S&P 500 as proxy) | `now-like`: -6.1% from 6 Oct high (not within 5%, so not `late`), high within 63 days, +22.7% over 504 days, CAPE top 10%. 703 days, ~25 windows, 44 spells | post hoc | sell all now | 0 | 0 | 0 | 0 | 0 |
| | | | staged-half | +0.71 | +1.13 | -3.82 | 1.7% | 0.3% |
| | | | staged-half-sma200 | +0.39 | +0.15 | -2.41 | 0.0% | 0.0% |
| | | | hold to fallback | +1.43 | +2.25 | -7.64 | 10.7% | 1.7% |
| (today's sub-cut) | `now-like-below200`: closed 0.05% below its 200-day line on 17 Nov. 214 days, ~7.6 windows, 14 spells | post hoc | staged-half | +0.65 | +0.78 | -3.91 | 1.9% | 0.0% |
| | | | staged-half-sma200 (= half day 0, half day 1) | +0.06 | +0.06 | -0.97 | 0.0% | 0.0% |
| | | | hold to fallback | +1.30 | +1.56 | -7.82 | 11.7% | 1.9% |
| US/tech stocks or tech fund (Nasdaq Composite) | `now-like`: -11.9% from 6 Oct high (inside the 4-12% band, near its edge), +26% over 504 days. 694 days, ~25 windows, 35 spells | post hoc | sell all now | 0 | 0 | 0 | 0 | 0 |
| | | | staged-half | +1.02 | +1.40 | -5.00 | 5.0% | 1.2% |
| | | | staged-half-sma200 | +0.92 | +1.15 | -4.78 | 4.6% | 1.6% |
| | | | hold to fallback | +2.04 | +2.81 | -10.00 | 15.7% | 5.0% |
| (today's sub-cut) | `now-like-below200`: 3.3% below its 200-day line since 13 Nov. Only 73 days, ~2.6 windows, 7 spells | post hoc | staged-half | -0.94 | -1.15 | -5.18 | 5.5% | 0.0% |
| | | | staged-half-sma200 (= half day 0, half day 1) | -0.26 | -0.19 | -1.80 | 0.0% | 0.0% |
| | | | hold to fallback | -1.89 | -2.29 | -10.36 | 30.1% | 5.5% |

For reference, the card's `late` sample, which no longer fits the US (card sample): S&P
staged-half +0.36 / +0.53 / -2.85 / 0.4% / 0.1%, staged-half-sma200 +0.33 / +0.49 / -2.79 / 0.3%
/ 0.0%, fallback +0.71 / +1.06 / -5.69 / 7.1% / 0.4%; Nasdaq staged-half +0.64 / +0.82 / -4.05 /
2.8% / 0.7%, staged-half-sma200 +0.65 / +0.82 / -3.97 / 2.0% / 0.3%, fallback +1.27 / +1.65 /
-8.09 / 12.6% / 2.8%.

Notes:

- Every OSEBX `late` start day was above its 200-day line, so `late-above200` = `late` there.
- No backtest for a global fund itself. The S&P 500 stands in (it is about 70% of MSCI World).
  The MSCI World ETF `URTH` (USD) is in the readings: 0.46% below its 200-day line on 17 Nov,
  6.0% below its 13 Aug high. Its high is older than 63 trading days, so it is not `now-like`.
- The Nasdaq is at -11.85%, just inside the band: a further fall of 0.2% puts it outside
  `now-like` (no tested sample then fits; `crash-window` is the nearest scenario).
- The Nasdaq below-200 cut is 7 spells; its negative means are noise-sized, not a finding.

### 2. What "sell all US/tech now" costs in expected drift, and what it buys

In the post-hoc `now-like` sample, against staged-half (mean / median of R-1):

| Index | staged-half mean | median | what selling all now removes |
|---|---:|---:|---|
| S&P 500 | +0.71% | +1.13% | p5 -3.82%; 1.7% chance of >5% worse, 0.3% of >10% worse |
| Nasdaq | +1.02% | +1.40% | p5 -5.00%; 5.0% chance of >5% worse, 1.2% of >10% worse |

So the reviewer's estimate of about 0.7-1.4% of the amount sold is right: 0.71-1.02% by the
mean, 1.13-1.40% by the median. It buys a certain price instead of a spread whose worst 1 in 20
is about 3.8-5.0% below it.

Against the tested rule in today's state the cost is nil. Today the US indexes are below their
200-day lines, and in that state `staged-half-sma200` sells the second half on day 1 (point 3).
In `now-like-below200` it gave +0.06% (S&P) and -0.26% (Nasdaq) against "sell all now". Over
the whole `now-like` sample (above and below the line) it gave +0.39% / +0.92%. Waiting for
18 Dec in `now-like-below200` had a mean of +1.30% for the S&P but -1.89% for the Nasdaq
(7 spells). The direction of drift after a break of the 200-day line is not settled by this
data.

### 3. The tested rule, exactly (code: `bt_amend.outcomes_new`)

`staged-half-sma200`, with day 0 = the day of the first sale, F = 22:

1. Sell half at the close of day 0, whatever the state.
2. After each close of days 0 to 21, check: close < 200-day simple average (the mean of the last
   200 closes, that day's close included)?
3. The first time it is, sell the other half at the close of the next trading day.
4. If no close from day 0 to day 21 is below, sell the other half at the close of day 22.

What follows from the code:

- Closes before day 0 are not looked at. A break on 17 Nov counts only if the day-0 close is
  still below the line. Then the rule sells half on day 0 and half on day 1.
- So "sell all on day 0 because the index is already below" is not literally the tested rule.
  It moves half the position one day earlier. In the post-hoc `now-like-below200` cut the
  difference is the table's +0.06% (S&P) / -0.26% (Nasdaq) mean, a fraction of a percent.
- If the index has crossed back above its line by the day-0 close, the trigger has not fired.
  The rule then waits: the other half goes the day after the next close below, else on day 22.
- Once fired, it stays fired. A close back above the line after the trigger changes nothing:
  the half is sold the next day anyway. There is no re-entry.
- The rule never sells everything on day 0. "Sell all at once if the line breaks before
  anything is sold" (report step 2) is the card's `trig-sma200` for the part not yet sold.
  `trig-sma200` failed the bar in `late` (p5 -5.57) because it waits while the index is above
  the line. In a below-the-line start it sells everything on day 1.
- Calendar: the backtest uses one calendar. For a US index the close comes at 22:00 CET, after
  European markets (Oslo included) have closed, so an investor selling in Europe can act on
  day t's US close at the earliest on day t+1. That is the same one-day lag the test assumes,
  but the price differs: the test books the index close of day t+1, while a European sale (or a
  fund's NAV cut-off) prices earlier in the day.
  Not modelled.

Suggested wording for the report's Step 1 (US, global or tech holdings): "If the holding's index
closed below its 200-day average on the evening before your first sale, sell all of it now. The
tested rule sells half on the first day and the rest the next day if the line is still broken.
Selling all at once moves half of it one day earlier, which made a difference of a fraction of a
percent in the past. If the index has closed back above its line by then, the trigger has not fired: sell
half and treat the rest under Step 2."

### 4. Smaller items

- (a) `bt_now.py` printed `sma10m: False` for the S&P while the text says "in". The old script
  treated the last day of the series (17 Nov) as a month end, so it printed the live value
  (-0.05%, out if the month ended that day). The decision in force is the one made at the
  30 Oct close (+3.8%, in). Fixed: it now prints both, for `sma10m` and `tsmom12`. The
  backtests are not affected: only the last day of a series is open to this, and the train
  period ends after 9 Nov 2025 with no trade possible after it.
- (b) The `trig-vix` rows cover 1990 on only. In the S&P samples that is `late` 2,340 of 2,739
  start days, `all` 8,954 of 24,301, `now-like` 605 of 703 and `crash-window` 554 of 1,735. The
  Nasdaq samples are fully covered. Noted in the table captions above.
- (c) The card's times were wrong: "~19:30 UTC" and "~20:30 UTC" were in fact 18:50 and 19:01
  UTC by the commits. A dated correction note is on the card (amendment 2); the old text is left
  as it was.

### 5. Final refresh: one command

```sh
uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_now.py --fetch <scratch>/bt-dl
```

It refetches the public Yahoo series (S&P, Nasdaq, VIX, VIX3M, HYG, LQD, OSEBX, OBX, URTH) into
the scratch dir, which must be outside the repo and is never committed. It drops any US bar of
today's New York date before 16:10 New York time, and Oslo likewise before 16:30. It prints:

- the Part C table;
- for each holding type, the 200-day state, the date of the last cross and which sample fits;
- VIX, credit, CAPE and the Part B rule states, with monthly rules shown both as the decision
  in force and live.

The cache root comes from `GRIMSTRADE_DATA` / `BT_CACHE` or the gitignored
`research/macro.local.json`. The Baa spread is not refetched (FRED was unreachable).

## Honesty notes

- Variants: 30 selectable configurations, plus 2 baselines.
  - Card: 11 in Part A and 11 in Part B.
  - Amendment: 3 in Part A and 5 in Part B.
- `tries.md` has 194 rows from this lane:
  - Part A: 48 rows (12 x 4 indexes).
  - Part B: 24 rows (12 x 2 indexes).
  - Post hoc `now-like` samples: 48 rows (12 x 2 samples x 2 indexes, kind `robustness`).
  - Amendment: 56 rows (Part A 3 x 4 indexes; Part B 5 x 2 US indexes + 17 x 2 Oslo
    indexes, Oslo as `robustness`). Three Oslo rule rows are invalid because of the calendar
    bug noted in the amendment.
  - Review round 1 (amendment 2): 18 rows (3 strategies x 6 index-cuts, post hoc,
    `robustness`).
- Comparisons: Part A has 15 strategies x up to 14 sample cuts; Part B has 16 rules x 9
  episodes. With this many cuts, some favourable cells are luck.
- Unlogged runs:
  - A first `bt_window.py` run crashed before printing any number.
  - `bt_rules.py` was run a second time, without `--log`, after fixing a bug that skipped the
    1929 episode. The configurations were the same and the full-sample numbers identical; only
    the episode table gained the 1929 column.
  - `bt_sanity.py` printed only date ranges.
- Post hoc: the `now-like` sample was defined after seeing the current readings. It is
  labelled and logged as robustness and decides nothing. The card's `late` sample was also
  chosen to fit November 2026, which the card says.
- Not done:
  - Currency risk for non-euro holdings (e.g. NOK/EUR for Oslo).
  - Single stocks: no specific holdings were tested.
  - HY OAS: not cached, and FRED is unreachable from this machine.
  - GSADF: no R `exuber` here.
  - Re-running the Oslo VIX/credit rules with the calendar fixed.

## Reproduce

```sh
# scratch dir for downloads (never committed); cache root has yahoo-1d/, cboe/, fred/, shiller/
bash research/exit-plan-2026/scripts/bt_fetch.sh <tmp>/bt-dl
export BT_CACHE=<cache root> BT_FRESH=<tmp>/bt-dl
uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_window.py <out>
uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_window_now.py <out>
uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_rules.py <out>
uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_amend.py <out>
uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_review1.py <out>
# Part C, refetching first (or --us-last YYYY-MM-DD to cut the US data by hand):
uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_now.py --fetch <tmp>/bt-dl
uv run --with pandas python -I research/exit-plan-2026/scripts/bt_tables.py
```

(Add `--log` to `bt_window.py`, `bt_window_now.py`, `bt_rules.py`, `bt_amend.py` and `bt_review1.py` only for a logged rerun; it appends rows to `tries.md`.)
