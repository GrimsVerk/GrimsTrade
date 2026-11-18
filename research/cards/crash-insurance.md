# crash-insurance: is "trend = crash insurance" statistically solid, and what does it cost?

Lane insure-1, written 2026-11-18 22:45 UTC, **before any number of this lane was computed.**
Branch `insure-1` (from `trend-1926-fix`). Research only: fake money, files already in the data
cache, no change to the gym, the daily runner or the live strategies. No new rule: this is a
descriptive check of `tsmom12` exactly as trend-1926 ran it. The held-out year
(2025-11-11 .. 2026-11-09) is not touched: nothing after 2025-10-31 is parsed.

## Why

Tonight's lanes found that `tsmom12` has no provable edge over holding the same assets (dsr-1,
survey-5), and its remaining case is crash insurance: smaller losses in long bear markets
(eu-6, eu-7; trend-1926: "crash insurance, not an edge"). That claim rests on a handful of
episodes (2000-02, 2008, 2020, 2022 on the six assets; 1929-32 and 1973-74 in trend-1926). This
card asks whether the insurance is itself statistically solid across about 100 years of US
stocks, how many independent episodes back it, and what it costs per unit of loss avoided.

## What had been seen when this was written

- trend-1926 in full (both eras): over 1927-2001 the rule's Sharpe lead on the market is
  1929-1932 and 1973-1974 only; worst loss 38% against 84% (era 1) and 32% against 48% (era 2);
  the 22 of 28 market exits that were whipsaws; one spell (1929-11 to 1933-04, bought back 67%
  lower) did most of the work.
- trend-tune: on SPY and QQQ the rule hands back in the rebound much of what it saved in the
  fall; it buys back about seven months after a low, 23% above it.
- gsy-1: on 30 French industries 1928-2001, `tsmom12` sat in cash on 310 of 351 industry crash
  days (a 40% fall); its `tsmom12` book had a worst loss of 39% against 82% for equal weight.
- eu-6, eu-7: trend best in 6 of 6 crash windows on euro fund proxies (2000-02, 2008, 2022).
- General knowledge an agent cannot unlearn: the large US stock falls (1929-32, 1937-38, 1946,
  1962, 1968-70, 1973-74, 1987, 2000-02, 2007-09, 2020, 2022), and that a 12-month rule cannot
  leave a one- or two-month crash such as October 1987 or March 2020.
- From the files after 2001: nothing but their layout. No episode list, no drawdown, no rule
  return after 2001 was computed before this card.
- **Expectation, stated so it can be wrong:** insurance positive in most slow episodes and about
  zero or negative in fast ones; net of the rebound close to zero; the premium (cost outside
  falls per unit of loss avoided) somewhere near 1.

## Data

- **Primary set (11 series):** Ken French's daily market (`Mkt-RF + RF`) and the ten
  value-weighted industries (`10_Industry_Portfolios_daily_CSV.zip`), cache snapshot
  2026-11-12, the same files and loader as trend-1926. Loaded 1926-07-01 to 2025-10-31.
- **Robustness set (30 series):** the 30 value-weighted industries, daily
  (`30_Industry_Portfolios_daily_CSV.zip`, downloaded by gsy-1 to `french-gsy/2026-11-18/30d`),
  same span. Description only.
- Read with `python -I`, never committed.

## The rule series (reuse, no new replay)

- **1927-07-02 to 2001-12-30:** trend-1926's saved primary gym runs (`tsmom12@F-*` and
  `tsmom12@F62-*`, 2 bps a side, primary fill), read only. A session's rule return is the ratio
  of the equity on that session to the equity on the session before. trend-1926's replays are
  not redone.
- **Sessions no saved run covers** (the turn of 1961/1962 between the eras, and 2002-01-01 to
  2025-10-31): trend-tune's gym-free paper series (`trend_tune.paper`, 12-month lookback,
  Friday decisions, 2 bps a side) on the same bars, warm-up included. trend-1926-fix showed it
  agrees with the gym to 0.00001 a day except holiday-Friday weeks. Check reported: the episode
  table on 1927-2001 rebuilt from the paper series alone, largest difference in an episode's
  insurance.
- **30-industry set:** paper series only.
- **Holding:** the series' own total-return index.
- **Cash earns 0** (the gym's rule). **Second reading, fixed now:** cash earns French's daily
  T-bill return on days the paper series' position is 0 (`rule + (1 - position) x RF`), holding
  unchanged. A re-scoring, no new row.

## Crash episodes (mechanical, per series, non-overlapping)

- On each series' total-return index (session closes) from 1927-07-02 (the first decision) to
  2025-10-31.
- Zigzag with a 25% fall and a 25% rise: start at the first close as the running peak. While
  rising, track the highest close; when a close is 25% or more below it, that high is a
  confirmed **peak** and the series is falling. While falling, track the lowest close; when a
  close is 25% or more above it, that low is a confirmed **trough**, the episode is
  `[peak, trough]`, and the series is rising again from the trough.
- Only episodes with a confirmed trough count. An unfinished fall at the end is listed, not
  counted (its sessions count as calm).
- Depth = 1 - trough / peak. Length = calendar days from peak to trough.
- **Sensitivity (fixed now, description):** 20% fall / 20% rise, and 40% fall / 25% rise.

## Metrics

All in log points (100 x natural log), rule minus holding, over sessions after the start date
up to and including the end date.

- **Insurance** `I` of an episode: rule's log change minus holding's over `(peak, trough]`.
  Positive = loss avoided. **Share avoided** `S = I / |holding's log change|`.
- **Rebound** `B`: the same over `(trough, min(trough + 365 days, next episode's peak)]`: what
  the late return costs (expected negative).
- **Net** `N = I + B`.
- **Calm** `C`: the same summed over every other session from 1927-07-02 to 2025-10-31.
- Identity (checked in the script): total log difference over the whole span = sum `I` + sum
  `B` + `C`.
- **Premium** per series and pooled over the set: `P = -(sum B + C) / sum I`, the log growth given
  up outside falls per log point of loss avoided in falls. Below 1: the insurance paid for
  itself in growth; above 1: it cost more growth than it saved (it may still be worth having
  for the smaller worst loss, which is a preference, not a test). Also shown per year, and per
  era (1927-1961, 1962-2001, 2002-2025; episodes by their peak date, calm by its date).
- **Speed buckets** ("when does it fail"): fast (peak to trough at most 92 days), medium (93 to
  365), slow (over 365). Per bucket: count, mean `I`, share with `I > 0`, mean `S`, mean `N`.
  The market's episodes are listed one by one.

## Independence (effective episodes)

The 11 series fall together; an industry's fall inside a market fall is not new evidence.

- **Primary, market-anchored clusters:** each market episode is a cluster. An industry episode
  joins the market cluster whose `[peak, trough]` contains the industry episode's trough, else
  the one that contains its peak. Industry episodes that touch no market episode form their own
  clusters, linked when their `[peak, trough]` windows overlap (single linkage).
- **Conservative, linked clusters:** single linkage on overlapping `[peak, trough]` windows
  across all 11 series, market included (fewer, longer clusters).
- A cluster's value is the mean over its episodes (of `I`, `S`, `N`). The number of clusters is
  the number of effective episodes.

## Tests and pass rule (fixed now)

- **Sign test:** k clusters with value above 0 out of n (exact zeros dropped); one-sided
  binomial p = P(X >= k | n, 1/2).
- **Cluster bootstrap:** resample clusters with replacement, 10,000 draws, seed 0, mean of the
  cluster values; one-sided p = share of draws at or below 0; 90% range.

| Outcome | When (primary set, 25% episodes) |
|---|---|
| **Insurance real, and kept after the rebound** | `I`: sign test p < 0.05 and bootstrap p < 0.05, under both clusterings; and `N` the same under market-anchored clusters |
| **Insurance real, handed back in the rebound** | `I` passes as above; `N` does not |
| **Insurance not shown** | `I` fails under either clustering |

- Market alone (its own episodes, a dozen at most): sign test, description.
- The 30-industry set "agrees" if `I` passes there too (description, robustness).
- The T-bill reading and the 20% / 40% thresholds: description.
- **Bar.** This is not a pick: no rule is selected, so the bar for a new pick does not apply;
  it is quoted for scale. Base lane trend-1926 ran one pre-registered configuration with no
  family bar (edge only if p < 0.10 on market and book). Project-wide (`git show
  origin/register-1:research/register/BAR.md`, rows through 2026-11-18 22:34): **2,904 tries,
  N 1,012 for a new pick, Bonferroni p <= 4.9e-5.** The write-up says whether the sign-test p
  would clear it.

## `tries.md` rows

A new kind, defined in the header: `insure-check`, a descriptive re-score of an already logged
configuration (`tsmom12`) on a span or set it was not logged on; not selectable, not a strategy
try, not counted in any family. One row per rule series computed: 11 (the spliced 1927-2025
primary series, variant `tsmom12@insure-<series>`) and 30 (the 30 industries, paper series,
`tsmom12@insure30-<industry>`). Sharpe on all calendar days, 365 a year, cash at 0 (repo
convention). The T-bill reading and thresholds are re-scorings: no rows.

## What each answer means for the live rule

No outcome changes the live rule tonight. "Real and kept" would make crash insurance a solid,
counted reason for the stock slots' filter, with a price per unit. "Handed back" says the filter
changes the path (smaller worst loss, a preference) but not the wealth. "Not shown" says even the
insurance story rests on too few independent falls to call.
