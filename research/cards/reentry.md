# reentry: when to buy back in after selling into a suspected bubble

Written 2026-11-18 ~18:45 UTC (committed at 18:49 UTC; the time first written here, 19:20, was a mistake), lane `reentry` of the exit-1 run, before any number of
this test was computed. Seen before: public history of US bear markets (1929, 1973-74, 2000-02,
2007-09, 2020, 2022), the published claims that a 10-month-SMA re-entry comes late, and the
header and last rows of Shiller's `ie_data.xls` (CAPE 39.4 on 2026-11-12). No backtest of any
rule below has been run on these data by this lane.

This is not a trading-gym idea (one asset, one-off decision, monthly), so it does not use
`lib/harness.py`. It follows the protocol's spirit: rules fixed here, every variant logged in
`tries.md`, no look-ahead, no tuning after seeing results.

## Question

Someone sells US stocks at month `t` because they think stocks are in a bubble and holds cash. Which
rule for buying back in leaves them richest 5 and 10 years later, compared with buying back
immediately (= never having sold)? Especially when valuations are high, as now.

## Data (all cached, keyless)

- Prices: `^GSPC` daily closes (Yahoo, 1927-12 on), month-end close = last close of the month.
- Dividends: Shiller `D` (annual dividend, monthly series); one month's dividend = D/12 paid on
  the month-end price. Total return month `m` = (C_m + D_m/12) / C_{m-1}.
- Cash: Ken French monthly `RF` (1-month T-bill), from 1926-07. Cash earns RF (not 0: the
  question is about years in cash, and 0 would make waiting look much worse than it was).
- Valuation: CAPE_m = (C_m / CPI_{m-1}) / mean over k = 3..122 of (E_{m-k} / CPI_{m-k}). Earnings
  lagged 3 months (reporting delay), CPI 1 month. Shiller's own CAPE column is not used (it has
  no lag).
- Robustness: `^IXIC` (Nasdaq Composite, price only, 1971-02 on) with the same rules, no
  dividends; cash RF.

## Decisions and fills

The investor decides at each month-end close using only closes up to and including that day and
the lagged CAPE; they trade at that same close (index data; the protocol's caveat on index fills
applies, the same for every rule). All-time high = highest daily close since 1927-12-30 up to the
decision day.

## Rules (all that will be run)

Wealth starts at 1 in cash at the end of month `t`. Cash earns RF until invested; once invested,
money stays invested to the horizon (no second exit).

0. `now` (baseline): all in at `t`.
1. `dca12`: 1/12 at `t` and at each of the next 11 month-ends.
2. `dd20`: all in at the first month-end close at or after `t` that is at least 20% below the
   all-time high. No deadline.
3. `dd30`: the same at 30%. No deadline.
4. `dd20-sma10`: wait until a month-end close at least 20% below the all-time high has occurred
   (at or after `t`), then all in at the first later-or-same month-end close above its own
   10-month average of month-end closes. No deadline.
5. `cape-median`: all in at the first month-end at or after `t` whose CAPE is at or below the
   median of all CAPE values from 1928-01 up to that month (expanding, no look-ahead). No
   deadline.
6. `staged-24`: one third at the first month-end with drawdown at least 20%, one third at 30%,
   one third at 40%; whatever is still in cash goes in at `t` + 24 months.
7. `dd30-24`: all in at the first month-end with drawdown at least 30%, or at `t` + 24 months,
   whichever comes first.

## Samples

- A, all months: decisions 1928-01 .. last month with a full horizon.
- B, high valuation (the case studied here): decisions in A whose CAPE is in the top 20% of all CAPE
  values from 1928-01 up to that month (expanding percentile, no look-ahead).
- Named tops (shown, not part of the bar): 1929-08, 1937-02, 1968-11, 1972-12, 1987-08,
  2000-03, 2007-10, 2021-12; and early exits: 1996-12 (Shiller's "irrational exuberance" talk
  month), 1997-12, 1998-12, 2005-12, 2019-12. Nasdaq: 2000-02, 1998-12.

## Metrics

Ratio R = wealth of the rule / wealth of `now` at `t` + 60 and `t` + 120 months. Per sample:
median R, mean R, share of months with R > 1, 10th percentile of R, share of months still not
fully invested at the horizon. Monthly starts overlap heavily: B has only a handful of
independent episodes (counted as runs of B months with gaps under 12 months merged), and that
count is reported with every number.

## Pass bar (fixed)

A rule "beats buying back immediately" only if, at the 10-year horizon:

1. in sample B, median R > 1.00 and the share of months with R > 1 is at least 55%;
2. 1 holds in both halves of B (decisions before 1972-01 and from 1972-01);
3. in sample A, mean R is at least 0.97 (it does not cost much when the bubble call is wrong).

The same on `^IXIC` (B defined with the S&P 500 CAPE, decisions from 1981-02 so the 10-month
average and ATH have history) is robustness only and cannot rescue a failed rule.

## Logging

Each rule is one row per sample in `tries.md` at run time: kind `variant` (rules 1-7) or
`baseline` (rule 0) on `^GSPC`, `robustness` on `^IXIC`; period `train`; From/To = first and last
decision month; Sharpe column "n/a"; Return column = median R - 1 at 10 years in that sample;
Max DD column = 10th percentile of R - 1; Turnover column "n/a". The held-out-year rule of the
protocol does not apply (no strategy is selected for the gym).

## Twin

`now` (buying back at once). A re-entry rule that cannot beat it in high-valuation months has
no case.

## Result (added 2026-11-18 after the run)

Run once (tries rows 2026-11-18 18:52). No rule passed: in sample B at 10 years no rule had
median R > 1 with share >= 55% in both halves (pre-1972 the drawdown rules passed, from 1972 none
did). Numbers and discussion: moved out of the public repo.
