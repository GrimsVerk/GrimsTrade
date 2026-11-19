# exit-rules: how to sell a stock position inside a 6-week window, and classic exit rules

Field: market timing / trend following (Faber 2007 "A quantitative approach to tactical asset
allocation"; Moskowitz, Ooi & Pedersen 2012 time-series momentum; Campbell & Shiller on CAPE;
Kaminski & Lo 2014 on stop-loss rules).
Written 2026-11-18 ~19:30 UTC, lane `bt` of the exit-plan-2026 run, before any number below was
computed. Seen before: the repo's earlier results (trend rules, `sma200`/`tsmom12`, the
`credit-spread` card), the last row of Shiller's file (CAPE about 39 in Nov 2026, printed while
checking the column layout), and public market history (the episodes named below).

Research only, fake money. The investor sells a small stock portfolio by 31 Dec 2026,
whatever happens. The question is not "should the investor be in stocks" but "how to sell
inside the window".

## Data (all cached, keyless)

- S&P 500 price index `^GSPC`, daily closes from 1927-12-30 (Yahoo cache 2026-11-12, refreshed
  into the job's tmp dir for Part C). Price index: no dividends (about 0.1% over 6 weeks;
  ignored, the same for every rule).
- Nasdaq Composite `^IXIC` from 1971-02-05 (tech-bubble angle).
- Oslo: `OSEBX.OL` / `^OSEAX` / `OBX.OL` from Yahoo if the chart endpoint serves them
  (robustness line only).
- VIX (CBOE file, 1990-01-02 on), VIX3M (CBOE file from 2009-09-18; Yahoo `^VIX3M` if longer).
- Credit: FRED `BAA10Y` (Moody's Baa minus 10y Treasury, daily from 1986, cache 2026-11-13);
  HYG/LQD price ratio (Yahoo, from 2007-04).
- CAPE: rebuilt from Shiller's `ie_data.xls` (monthly real price and real earnings), with
  earnings shifted 3 months (publication lag): CAPE(m) = real price(m) / mean real earnings of
  months m-3-119 .. m-3. A month's CAPE is used from the first trading day of the next month.

## Periods

All backtests (Parts A and B) use the repo's train period: decisions up to 2025-11-09, and a
Part A window must end by then too. The held-out year (2025-11-11 .. 2026-11-09) is not used for
any backtest. Part C (current readings) uses the latest data and is description, not a test.

## Part A: the decision at hand (sell within ~28 trading days)

Calendar: from 2026-11-18, the 18 Dec 2026 close is trading day 22 at Oslo Børs (day 21 in New
York) and 30 Dec (Oslo's last trading day of 2026) is day 28. So: start day 0 = every trading day
in the sample; fallback day F = 22; last possible day N = 28. Price P0 = close of day 0. A
signal seen at the close of day t is executed at the close of day t+1 (the investor checks in the
evening and sells the next day). Limit sales: if the close of day t >= limit, the sale is booked
at the limit price on day t (conservative: a real limit would fill intraday at the limit).
Outcome R = realised average sale price / P0.

Strategies (all that will be run; 11 variants plus the baseline):

0. `now` (baseline): sell everything at P0, R = 1.
1. `fallback`: do nothing, sell everything at day 22.
2. `staged5`: five equal tranches at days 0, 5, 10, 15, 20 (weekly).
3. `staged-half`: half at day 0, half at day 22.
4. `trig-sma200`: sell all the day after the first close below the 200-day average (day 0..21);
   else at day 22. If already below at day 0, this sells on day 1.
5. `trig-sma50`: the same with the 50-day average.
6. `trig-trail5`: sell all the day after the close falls 5% below the highest close since day 0
   (P0 included); else day 22.
7. `trig-trail8`: the same at 8%.
8. `trig-vix`: sell all the day after VIX closes above 1.3 x its 50-day average; else day 22
   (VIX from 1990).
9. `limit3`: limit 3% above P0 (filled on the first close at or above it), else day 22.
10. `limit5`: limit 5% above P0, else day 22.
11. `bracket`: limit 3% above P0 or trailing stop 5% (as 6), whichever first, else day 22.

Metrics of R - 1 across start dates: mean, median, 5th and 95th percentile, P(R < 0.95),
P(R < 0.90), P(R > 1). Overlapping windows: about N/28 independent windows; the effective count
is shown next to each sample.

Samples (states at day 0, fixed now, no look-ahead):

- `all`: every start date.
- `cape-hi`: lagged CAPE at or above the 90th percentile of its own history up to that month
  (expanding window from 1881).
- `runup`: index within 5% of its all-time high (since the series began) and up at least 25%
  over the last 504 trading days. Chosen so that November 2026 fits it: the point is analogs of
  now.
- `lowvix`: VIX close below 16 (1990 on).
- `late` (the main "late-bubble" sample): `cape-hi` and `runup` both true.
- Ex post scenario `crash-window` (not a selectable state; it uses the future): windows in which
  the index fell 10% or more below P0 at some close in days 1..28. Shows how each strategy does
  if the pop does come inside the window.

Pass/answer: there is no pass bar; this is a description of distributions. A strategy "beats
selling now" for the investor only if its 5th percentile is no worse than -5% AND its median is
above 0 in the `late` sample, and the conclusion holds on `^IXIC` too. Differences in mean
smaller than 0.5 points are called "the same".

Robustness (logged as `robustness`, after the choice): the same table on `^IXIC` and on the Oslo
index if available, and `all` split 1928-1989 / 1990-2025.

## Part B: classic exit rules on crash episodes

S&P 500 daily, 1928 (each rule starts when its inputs exist) to 2025-11-09. Long or cash (cash
earns 0, as in the protocol; this biases against timing). Decision at close of day t, trade at
the close of day t+1 (index opens before about 1962 are not real). Monthly rules decide at the
last close of the month.

Rules (all that will be run; 11 variants; buy-and-hold is the baseline):

1. `sma10m`: out when the month-end close is below the 10-month average of month-end closes.
2. `sma200d`: out when the daily close is below the 200-day average.
3. `tsmom12`: out when the month-end close is below the close 12 months earlier.
4. `dd8`: out when the close is 8% or more below its highest close of the last 252 days; back in
   when the close is above its 50-day average.
5. `dd10`: the same at 10%.
6. `vix30`: out when VIX closes above 30; back in when it closes below 20 (1990 on).
7. `vixts`: out when VIX / VIX3M closes above 1.0; back in when it closes below 0.9 (VIX3M
   start on).
8. `baa`: out when the 20-day mean of `BAA10Y` is more than 0.5 points above its lowest value of
   the last 365 calendar days (the repo's `credit-spread` rule); back in when it is not (1986 on).
9. `hyglqd`: out when HYG/LQD closes below its 200-day average (2008 on).
10. `cape30`: out when lagged CAPE is above 30.
11. `capepct`: out when lagged CAPE is at or above the 95th percentile of its own expanding
   history.

Episodes (peak and trough found from the closes inside these windows): 1929 (1929-01 ..
1932-12), 1937 (1937-01 .. 1938-12), 1973-74 (1972-06 .. 1974-12), 1987 (1987-06 .. 1987-12),
2000-02 (2000-01 .. 2002-12), 2007-09 (2007-06 .. 2009-06), 2020 (2020-01 .. 2020-06), 2022
(2021-11 .. 2022-12); Nasdaq 2000-02 as an extra line.

Metrics per rule and episode: date of the first exit signal on or after 60 trading days before
the peak and the lag in trading days after the peak; share of the peak-to-trough fall avoided
((exit price - trough) / (peak - trough), using the first exit; 0 if no exit before the trough);
the rule's return from peak to trough vs buy-and-hold's (re-entries included). Full sample:
annual return, max drawdown, round trips per year, whipsaws (round trips where the re-entry
price is above the exit price) and their average cost, share of exits that were false alarms
(the index did not fall 10% below the exit price before the rule re-entered).

Interpretation rule: eight episodes are eight observations, not thousands. A rule is "useful in
crashes" only if it avoided at least a third of the fall in at least 6 of 8 episodes; it is
"cheap in normal times" if its whipsaw cost is under 1% a year. Neither is a pass that makes it
a trading strategy; it is input to the playbook.

## Part C: current readings

Latest close (Yahoo refresh) of: S&P 500 and Nasdaq vs their 200-day and 10-month averages,
drawdown from the all-time high, VIX and VIX/VIX3M, HYG/LQD vs its 200-day average, BAA10Y
(latest cached), CAPE (Shiller, lagged and unlagged), Oslo index if available. Which Part B rules
are "out" today.

## Counting

Every strategy x index run is a row in `tries.md` (kind `variant` on `^GSPC`, `robustness` on
other indexes and sub-periods). The total number of variants and the number of sample cuts are
stated in the result: 11 Part A variants x 5 samples and 11 Part B rules x 8 episodes are many
comparisons on few independent episodes.

## Result

`research/exit-plan-2026/lanes/bt.md`.

## Amendment 2026-11-18 (~20:30 UTC), before running these; Parts A-C results already seen

Added from the `lit` lane's suggested tests (`lanes/lit.md` section 16). Because Parts A-C have
been seen, these are post-hoc additions. Each one is counted as a variant, and none of them can
overturn the card's verdicts above. Suggestions that only duplicate what is above are skipped:
lit 1, 7 and 8, and lit 3's "-X% from the 52-week high" stop, which is `dd8`/`dd10`.

Part A, 3 new variants. Same windows, F = 22, signal at close t, sale at close t+1:

- `staged3`: thirds on days 0, 11 and 22.
- `staged5-sma200`: the `staged5` tranches. After the first close below the 200-day average
  (days 0..21), everything still unsold goes the next day.
- `staged-half-sma200`: half on day 0. The other half goes the day after the first close
  below the 200-day average, else on day 22.

Part B, 5 new variants. Same engine as Part B above:

- `sma200d-b2`: out when the close is more than 2% below the 200-day average; back in when it
  closes above it.
- `sma200d-c2`: out after 2 closes in a row below the 200-day average; back in after 2 closes
  in a row above it.
- `kl3m10` (Kaminski-Lo style): out when the 63-day return is below -10%; back in when the
  63-day return is above 0.
- `rv2`: out when the 21-day realised volatility is above 2 x its 252-day median; back in
  below 1.25 x.
- `sma200d-rv` (vol as confirmer): out when the close is below the 200-day average AND
  21-day volatility is above 1.5 x its 252-day median; back in when the close is above the
  average.

Robustness (`robustness` rows):

- All Part B rules on OBX (2004 on) and OSEBX (2013 on): the 2007-09, 2018 Q4, 2020 and 2022
  episodes where the data cover them.
- An added 2018 Q4 episode (2018-09-01 .. 2018-12-31) for the S&P 500 and the Nasdaq.

Screen (descriptive, not a variant): Greenwood-Shleifer-You flags for US tech, using Ken French's
10-industry daily `HiTec` portfolio (cache 2026-11-12) and the Nasdaq/XLK for months after it
ends:

- 2-year raw return, and 2-year return net of the market (French `Mkt`).
- Acceleration: R(t-24,t) - R(t-24,t-12).
- 1-year change in 63-day volatility.
- The months since 1926 when the 2-year raw return was at least 100%.

Skipped:

- lit 5, HY OAS (`BAMLH0A0HYM2`): not cached, and FRED timed out from this machine. The Baa
  spread above stands in for it.
- lit 9, GSADF: needs R `exuber`, which is not available here.

## Amendment 2, 2026-11-18 (written about 19:40 UTC), review round 1; before running these

Post hoc: Parts A-C and amendment 1 have been seen, and the reviewer has seen that the card's
`late` state no longer fits the US indexes (S&P 500 -6.1%, Nasdaq -11.9% from their highs at the
17 Nov close). Everything below is `robustness` in `tries.md`, is labelled post hoc, and decides
nothing; it only splits samples already shown by today's state at day 0.

Correction of times written above (the text above is left as it was). The card's first version
says "~19:30 UTC" and amendment 1 says "~20:30 UTC". Those were not UTC. The git commits are the
record: the card was committed at 18:50 UTC (19:50 CET) and amendment 1 at 19:01 UTC
(20:01 CET). Both were still committed before the runs they cover (Part A rows in
`tries.md` from 18:53 UTC, amendment rows 19:02 UTC).

Part A, new sample cuts (same windows, F = 22, train period, same strategies `fallback`,
`staged-half`, `staged-half-sma200`, with `now` = 0 as the baseline):

- `now-like-below200`: `now-like` (as defined in `bt_window_now.py`) AND the day-0 close below
  its 200-day average. S&P 500 and Nasdaq. This is the US state at the 17 Nov close.
- `now-like-above200`: `now-like` AND the day-0 close at or above its 200-day average (the rest
  of `now-like`). S&P 500 and Nasdaq.
- `late-above200`: `late` AND the day-0 close at or above its 200-day average. OSEBX and OBX
  (their `late` uses the US CAPE, so it equals `runup` over their history). This is the Oslo
  state today.

Same metrics as Part A (mean, median, p05, p95, P<-5%, P<-10%, P>0, start days, spells).
18 rows (3 strategies x 6 index-cuts), kind `robustness`, script `bt_review1.py`.

Part C additions (description only, no test):

- `URTH` (iShares MSCI World ETF, USD, Yahoo) as the reading for a global index fund: close vs
  its 200-day average, from its high, 24-month return.
- For each holding type (Oslo ~ OSEBX/OBX; global fund ~ S&P 500 and URTH; US/tech ~ Nasdaq):
  the 200-day state, the date of the last cross of the 200-day line, and which day-0 sample
  conditions (`runup`, `late`, `now-like`) hold today.
- `sma10m` is printed as the decision in force (last completed month end) and separately as the
  live value, so the script agrees with the text.
- `bt_now.py --fetch <dir>` refetches the public Yahoo series first; a US bar of today's New
  York date is dropped until 16:10 New York time (Oslo: 16:30 Oslo time) unless `--us-last`
  is given.

Correction to amendment 2 itself (19:33 UTC, before running): it was written and committed at
19:30 UTC, not "about 19:40", and the first Part A rows in `tries.md` are from
18:52 UTC, not 18:53.
