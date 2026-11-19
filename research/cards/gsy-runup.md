# gsy-runup: step aside after an industry doubles ("Bubbles for Fama")

Field: empirical asset pricing, bubbles and crashes (Greenwood, Shleifer & You 2019, "Bubbles
for Fama", Journal of Financial Economics 131(1)).
Written 2026-11-18, lane gsy-1, **before any number of this lane was computed.** Branch `gsy-1`
(from `trend-1926`). Research only: fake money, public data, no change to the gym, the daily
runner or the live strategies. The held-out year (2025-11-11 .. 2026-11-09) is not touched.

## Claim (from the paper, as relayed by tonight's literature lane; not re-read here)

In US industries 1928-2014 (Fama-French 48), after an industry's value-weighted return over two
years exceeds 100%, both raw and net of the market, the chance of a crash (a 40% drawdown)
within the next two years is about 53%, and about 80% after a 150% run-up. Rising volatility,
share issuance, acceleration of the run-up and a high share of young firms raise it. Prices kept
rising for about 6 months (about 30%) after the first signal on average, and moving to cash
after the signal beat moving to the broad index.

**Hypothesis for GrimsTrade:** a GSY run-up flag used as an exit overlay on the `tsmom12` trend
book improves its worst loss or its Sharpe, out of sample.

## Why it might work

`tsmom12` leaves only after a year of gains has been given back, so in a bubble that bursts it
sells late (trend-tune: it buys back 23% above the low and sells well below the top). A flag
that fires during the run-up could step aside before the fall, and GSY say the run-up alone
carries information about the crash.

## Why it might not

- GSY's own numbers say half the flags are false alarms at 100%, and that prices rise ~30% after
  the first signal: selling on the flag gives up that rise.
- `tsmom12` already exits real crashes, only later. An overlay can add only the fall between the
  peak and `tsmom12`'s own exit, and it pays with every false alarm.
- Few events: an industry doubling (raw and net of market) in two years is rare, more so with
  30 or 10 broad industries than with 48. The book's worst loss is mostly a market-wide fall,
  which an industry flag cannot see; the book effect will be small.
- GSY's sample includes the years tested here (see "Overlap").

## What had been seen when this was written

- `trend-1926.md` and its tables: `tsmom12` against holding on Ken French's daily market and 10
  industries, 1927-1961 and 1962-2001 (so `tsmom12` on the 10-industry daily series is not new
  data for the twin; no overlay or run-up statistic was ever computed).
- `trend-tune.md`: `tsmom12` sells late and buys back late; 82 of 112 exits whipsaws.
- The GSY headline numbers above, from the literature lane (the paper itself was not re-read).
- General knowledge an agent cannot unlearn: the tech bubble of 1998-2000 and its crash, the
  energy run-up to 2008, the 1929 crash, the 2020-2021 run in technology.
- From the French 30- and 49-industry files: nothing yet (they are downloaded for this lane).

## Data

- Ken French data library, value-weighted industry portfolios, dividends included (CRSP):
  - `49_Industry_Portfolios_CSV.zip` (monthly): replication only (closest to GSY's 48).
  - `30_Industry_Portfolios_CSV.zip`, `10_Industry_Portfolios_CSV.zip` (monthly): replication.
  - `30_Industry_Portfolios_daily_CSV.zip`: **primary book**.
  - `10_Industry_Portfolios_daily_CSV.zip` (already cached, snapshot 2026-11-12): robustness.
  - Market: `Mkt-RF + RF` from `F-F_Research_Data_Factors_daily_CSV.zip` (daily, cached) and
    `F-F_Research_Data_Factors_CSV.zip` (monthly, cached).
- New files go to a fresh snapshot folder under the cache root (the git-ignored
  `research/macro.local.json`), outside the repo; read as data with `python -I`, never
  executed, never committed. A value marked missing (-99.99 / -999) means no bar that day.
- **Nothing after 2025-11-09 is used** (train end). The French files end before the held-out
  year anyway; the cut is also in the code.

## The flag (fixed)

On the daily total-return index of each industry, on each session close `t`:

- `R2(t)` = return over the last 730 calendar days (the close on or before `t - 730`).
- `M2(t)` = the same for the market.
- **Run-up at `t`** if `R2(t) >= T` and `R2(t) - M2(t) >= T`, with `T` = 1.00 (100%) or 1.50
  (150%). Thresholds are the paper's; no other value is tried.
- **Flag active** on a decision day if a run-up held on any session in the last 730 calendar
  days up to the last visible close (the paper's two-year crash window, counted from the latest
  run-up session, so a run-up that keeps going keeps the flag on).

Computed only from closes visible at the decision; arrays are built causally (entry `i` uses
bars `<= i`), as `common.vol_series` does.

## Variants (all that will be run; 6)

The base is `tsmom12` exactly as the protocol's twin: each industry has an equal slot, held
while its 365-day return is positive, else cash; Friday decisions; 1% band. Each variant holds
the slot only if `tsmom12` holds it **and** the exit condition below is false:

| Variant | Exit condition |
|---|---|
| `flag100-cash`, `flag150-cash` | flag active (the paper's "move to cash") |
| `flag100-sma`, `flag150-sma` | flag active **and** close below its mean over the last 290 calendar days (~200 sessions / 10 months; calendar days because of Saturday sessions before 1952) |
| `flag100-vol`, `flag150-vol` | flag active **and** volatility rising: stdev of daily log returns over the last 182 calendar days above that of the 182 calendar days before |

Nothing else is tried (no other threshold, window, or combination). Issuance and young-firm
share are not in the French files and are not used.

## Universes and periods

- **Primary book:** the 30 French industries, daily, as one equal-slot book (`G30-*` symbols).
- **Discovery: decisions 1928-07-02 .. 2001-12-31** (the flag needs two years of history; data
  start 1926-07-01).
- **Check: decisions 2002-01-02 .. 2025-11-09** (history before 2002 is visible to the signals,
  as it would have been).
- **Overlap, said plainly:** GSY's US sample is 1928-2014. Discovery is entirely inside it, and
  so is 2002-2014 of the check. Only 2015-2025 is outside their sample; that window is reported
  next to the check but is short (few or no flags). So this is mainly a test of whether GSY's
  finding works **as an overlay on our trend rule**, not an out-of-sample test of GSY.
- **Robustness:** the 10 French industries (daily, `G10-*`), same two periods. If a variant
  passes: the repo's ETF sector set XLK, XLE, XLF, XLV (Yahoo, dividend-adjusted, train period
  only, market = SPY) as a second robustness, rows `robustness`.
- Engine: `grimstrade.gym.simulate` via `lib/harness.py`, unchanged; fills as trend-1926's
  primary (open = previous close: the fill is at the close the signal saw), 2 bps a side.
  Cash earns 0. Sharpe on calendar days, 365 a year.

## Step 2: replication (descriptive, no strategy, before the variants)

On monthly value-weighted returns, 49 industries, months 1928-07 .. 2014-12 (GSY's period):

- Episode = the first month an industry's 24-month return is `>= T` raw and net of market
  (24-month market return subtracted); the same industry starts no new episode while it had a
  run-up month in the previous 24 months.
- Crash = within months `t+1 .. t+24`, a peak-to-trough fall of at least 40% in the industry's
  total-return index, the peak counted from month `t` on. Also shown: the stricter "falls 40%
  below the level of month `t`".
- Reported: episodes, crash share, both thresholds; the same on 30 and 10 industries; and split
  1928-2001 / 2002-2025. The unconditional crash share (all industry-months) for comparison.
- The setup "works" if the 49-industry, 100% crash share is within 15 points of 53% and the
  150% share is higher than the 100% share. If not, the definitions are re-read against the
  paper and the gap is written down; the card's variants are run unchanged either way.

## Metrics (per variant, per period, against `tsmom12` on the same book and days)

- Sharpe and its difference to `tsmom12` (paired stationary bootstrap, mean block 20 days,
  2,000 draws, seed 0, one-sided p); also block 125 days.
- Worst loss (max drawdown) of the book; growth a year; time in.
- **Crashes:** every fall of 40% or more from a running peak in an industry's daily index
  within the period (crash day `X` = the first close 40% below the peak; one crash per peak).
  **% of crashes avoided** = share of crashes where the slot was in cash on day `X` (decision in
  force), for the variant and for `tsmom12`; and how many of the variant's were avoided only by
  the overlay.
- **Days early:** for crashes avoided, calendar days from the exit to `X` (median), and from
  the peak to the exit (negative = out before the peak).
- **False alarms:** overlay-caused spells out (variant in cash while `tsmom12` holds) after
  which the industry has no 40% crash within 730 days of the spell's start; count and share;
  and the price move given up in all overlay spells (log points).
- Number of flag episodes in the period (the number of independent bets the result rests on).

## Pass bar (fixed; 6 variants, two routes, so 12 tests)

A variant **passes** if either route holds on the primary book:

- **Route S (Sharpe):** discovery Sharpe difference to `tsmom12` positive with p < 0.10 / 12
  = 0.008 (Bonferroni over 6 variants x 2 routes); **and** the check-period difference is
  positive; **and** the 10-industry book's discovery difference is positive.
- **Route W (worst loss):** worst loss at least 5 points smaller than `tsmom12`'s in discovery
  **and** in the check period; Sharpe no more than 0.05 below `tsmom12` in either period; and a
  larger share of crashes avoided than `tsmom12` in both periods.

Failing both routes: dead. Passing: a candidate for its own card on the six live assets under
the default protocol bar (held-out year once, there), never a live change from this lane.

Expectation, stated so it can be wrong: `-cash` loses Sharpe (it sells run-ups that keep
rising, and stays out through rebounds); `-sma` and `-vol` sit close to `tsmom12`; nothing
passes because the events are few and `tsmom12` already exits the big crashes.

## `tries.md` rows (idea `gsy-runup`)

- `tsmom12` and equal weight on each book and period: `baseline` (8 rows).
- The 6 variants on the 30-industry book, discovery and check: `variant` (12 rows; one variant
  = one configuration seen on two periods).
- The 6 variants on the 10-industry book, two periods: `robustness` (12 rows).
- ETF sector set, only if something passes: `robustness`.
- The replication is descriptive: no rows.

## Result

See `research/gsy-1.md` and `research/results/gsy-1.md` once run.
