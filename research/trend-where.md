# Trend where: keep the trend filter only where it buys calm

Research run trend-where, started 2026-11-18. Branch `trend-where` (from `trend-tune`). Research
only: fake money, the price cache already on disk, no change to the gym, the daily runner or the
live strategies. This is next lane 2 of `trend-tune.md`.

## In plain words (results, 2026-11-18)

**Dropping the trend filter where it buys no calm is a tie with keeping it everywhere: slightly
ahead, not provably so, and the worst loss over the whole period did not get deeper. Both
variants fail the bar; the live rule stays.** Held-out year not looked at. Tables:
`results/trend-where.md`; 8 rows in `tries.md`; one run.

Sharpe is return per unit of risk (higher is better). Six live assets, 1994-2025:

| | Sharpe | Growth a year | Worst loss | Loss in 2022 rate shock | Trades a year |
|---|---:|---:|---:|---:|---:|
| `where-vol` (filter kept where days out were more volatile) | 1.07 | +18.9% | 35.3% | -26% | 1.7 |
| `where-dd` (kept where days out fell deeper) | 1.05 | +18.4% | 35.7% | -27% | 2.4 |
| `tsmom12` (filter always on) | 1.05 | +17.8% | 36.5% | -13% | 2.7 |
| Equal weight (buy and hold) | 0.88 | +18.2% | 68.8% | -37% | 1.3 |

- **The yes/no finds the stocks by itself.** Looking only at the past each January,
  `where-vol` kept the filter on SPY and QQQ in every year and dropped it on bonds from 2009,
  gold from 2015, Bitcoin from 2019 and Ether from 2023. That is the full-sample answer of
  `trend-tune.md`, reached without hindsight.
- **On Sharpe it is a small gain that could be luck.** +0.03 against `tsmom12` (p = 0.27; the
  bar asked for p < 0.05), +0.03 since 2003. Out of universe: +0.05 on the 8 other ETFs
  (p = 0.08), +0.07 on the 6 other coins (p = 0.01), 0.00 on the 4 indexes (all stocks: every
  answer is yes at the last refit, so the rule is close to `tsmom12` there).
- **Worst loss: no deeper over the whole period, but twice as deep in 2022.** The book's worst
  loss is 35.3% against 36.5%, and the out-of-universe worst losses are within 2 points. But
  the answers only turned to no late (each asset keeps the filter for its first five years, and
  Bitcoin kept it through the 2014 and 2018 winters). The one bad stretch after bonds, gold and
  Bitcoin had all lost their filter is 2022: -26% against -13% in the rate shock, -33% against
  -20% in the crypto winter. So "same worst loss" rests on one episode, and in that episode the
  rule lost twice as much.
- **Reading "rougher" by depth of fall is worse than by volatility.** `where-dd` flips its
  answers (gold no in 2011, yes in 2016; bonds yes again in 2023), gains nothing on the six
  (+0.01) and is behind on the other ETFs (-0.07) and the indexes (-0.03).

### Pass bar

| Bar | `where-vol` | `where-dd` |
|---|---|---|
| 1. Sharpe beats `tsmom12`, p < 0.05 | FAIL (+0.03, p 0.27) | FAIL (+0.01, p 0.45) |
| 2. Worst loss within 5 points | pass (35.3% vs 36.5%) | pass (35.7% vs 36.5%) |
| 3. Since 2003: not behind, worst loss within 5 points | pass | pass |
| 4. Out of universe: Sharpe up and worst loss within 5 points, 2 of 3 sets | pass | FAIL |
| 5. Beats equal weight | pass | pass |

### What this means

1. **No change to the live rule.** Neither variant clears the bar.
2. **The filter on the bond, gold and coin slots is cheap insurance, not a drag worth
   removing.** Dropping it there was worth about +1 point of growth a year and a third less
   trading, with a Sharpe gain that cannot be told from zero, and it cost 13 points in 2022.
3. **The risk choice of `trend-tune.md` stands as it was put**, now with one table behind it.

### How sure

- The gap to `tsmom12` is measured with a standard error of about 0.04: +0.03 is inside the
  noise, and +0.10 would have been seen. Two tries, no selection between them.
- The worst-loss result is the weak part: the coin answers have been no only since 2019 (BTC)
  and 2023 (ETH), so the rule has held coins unfiltered through one winter.
- Card pushed before any number (commit `04c613a`). The no-look-ahead test removes every later
  bar and gets the same answers. Held-out year unspent.

### Next step

Run `where-vol`, unchanged, on the 1926-1961 US industries of lane `trend-1926` (data no run
here has tuned on, with 1929-32 and 1937 in it). It is the only place left where the worst-loss
question can be asked on more than one episode. No held-out look is earned.

## Follow-up result: on ten US industries 1926-1961 the switch never turns the filter off

**`where-vol` is `tsmom12` to the cent there: it answered yes for every industry at every one
of 34 yearly refits (0 of 340 industry-years no).** Tables: `results/trend-where-1926.md`; one
new row in `tries.md`; one run.

| Ten industries, one book, 1927-1961 | Sharpe | Growth a year | Worst loss | Worst loss 1929-32 |
|---|---:|---:|---:|---:|
| `where-vol` | 1.07 | +12.6% | 32.5% | 29.3% |
| `tsmom12` | 1.07 | +12.6% | 32.5% | 29.3% |
| Equal weight | 0.62 | +10.6% | 81.9% | 81.9% |

- **What it shows.** On stocks the yes/no is stable and unanimous: in all ten industries the
  days out were rougher than the days in (at the last refit 1.3 to 1.8 times as volatile), and
  that was already so at every earlier refit. This is the "days out are rougher on stocks"
  mechanism of `trend-tune.md` on 35 years no run here had tuned on. So the switch does no
  harm on stocks, because on stocks it does nothing.
- **What it does not show.** The open question was the worst loss on slots where the filter
  gets dropped (bonds, gold, coins). This data has no such slot, so that question is exactly
  where it was: one episode, 2022, in which the rule lost twice as much.
- The outcome is the one the follow-up card expected. Card pushed before the number (commit
  `966eddc`). Held-out year unspent.

**Next step now:** none worth a lane with the data on disk. The worst-loss question needs long
histories of non-stock assets (bonds and gold before 2002); if a keyless source for those is
found, `where-vol` runs on it unchanged.

## Follow-up card: `where-vol` on US industries 1926-1961 (fixed 2026-11-18, before any number)

**Seen when this was written:** everything above; the loader code of lane `trend-1926` (branch
`trend-1926`, draft PR #37), but not its write-up, tables or `tries.md` rows. No number of this
follow-up exists yet.

- **Data.** Ken French's 10 value-weighted industry portfolios, daily, 1926-07-01 to
  1961-12-31, as total-return bars built by `lib/trend_1926.py` (copied unchanged from
  `origin/trend-1926`; fills at the close the signal saw, 2 bps a side, cash earns 0: that
  lane's primary configuration). First decision 1927-07-02.
- **Rule.** `where-vol` exactly as on the card below: same code, same 5-year and 60-bar
  minimums, refit the first Friday of each year. Nothing is changed for this data (so "a year"
  of bars is 252 sessions although the exchange also traded on Saturdays until 1952).
- **Runs.** The ten industries as one equal-slot book: `where-vol`, with always-on `tsmom12`
  as twin and equal weight as benchmark (both are `trend-1926`'s own baselines, re-scored here
  without new rows). One new `robustness` row, idea `trend-where`, `where-vol@F-ind10`. Run once.
- **What is read off (a robustness check of a rule that already failed; it cannot rescue it).**
  1. Sharpe difference to `tsmom12` with the bootstrap p.
  2. Worst loss against `tsmom12`'s, whole period and inside 1929-09-03 to 1932-07-08 and
     1937-03-10 to 1938-03-31; "no deeper" means within 5 points.
  3. The yes/no per industry by year, and how many industry-years are no.
- **Expected before looking:** all ten are stocks, so the answers should be mostly yes and the
  book close to `tsmom12`. If so, the check says only that the switch does no harm on stocks,
  and the worst-loss question for non-stock slots stays open (no old bond, gold or coin data
  here). If many answers are no and the worst loss is deeper by more than 5 points, the switch
  is unsafe even on stocks.
- Held-out year not touched.

## Card (fixed 2026-11-18, before any number of this run)

### What had been seen when this was written

- Everything in `trend-tune.md` and its tables. In particular, in sample over the whole train
  period: `tsmom12`'s days out were rougher than its days in on SPY and QQQ only (SPY 29%
  against 16% volatility); on TLT, GLD, BTC and ETH they were not. The rule beat holding on
  Sharpe on the two stock funds only, but shrank the worst loss on others (TLT 33% against 48%).
- Deep-1 (draft PR #36): 8 of `tsmom12`'s 10 worst drawdowns are coin tops.
- So the full-sample answer to "where is the filter kept" is already known (stocks). What is not
  known is what a walk-forward yes/no, which only sees the past at each January, would have
  done, and what it costs in worst loss. No number of this run exists yet.

### The rule

- **In and out.** For an asset, each bar belongs to the `tsmom12` signal of the latest Friday
  strictly before the bar's date (the paper-series convention of `trend-tune.md`), computed only
  from bars visible at that Friday's decision. A bar is *in* if that signal was on, *out* if it
  was off. Bars before the asset was eligible (a year of bars) are left out.
- **Refit.** The first Friday of each calendar year, from bars visible at that decision only
  (expanding window). The answer holds until the next refit.
- **Yes/no, per asset.** The asset keeps its trend filter (yes) if its past out bars were
  rougher than its past in bars; otherwise (no) its slot is simply held. With under 5 years of
  eligible bars, or fewer than 60 out bars or 60 in bars, the answer is yes: the incumbent rule
  stays until there is evidence. No S&P 500 warm-up (SPY decides on its own history).
- **Two readings of "rougher", each one try:**
  1. `where-vol`: the standard deviation of close-to-close returns on out bars is larger than
     on in bars.
  2. `where-dd`: the worst peak-to-trough fall of the chained out-bar returns is deeper than
     that of the chained in-bar returns.
- **Trading.** Equal slots among eligible assets, Friday decisions, the gym's fills and costs. A
  slot is held if the asset's answer is no, or if its answer is yes and its `tsmom12` signal is
  on. With every answer yes the rule is `tsmom12` exactly; with every answer no it is equal
  weight exactly (a test proves both, and another proves the answers do not move when later
  bars are removed).

**Twin:** always-on `tsmom12`. **Benchmark:** equal weight (buy and hold). Idea name in
`tries.md`: `trend-where`. Two `variant` rows; out-of-universe runs are `robustness` rows.

**Out of universe.** Each variant refitted, unchanged, on each set's own history as one book:
the 8 other ETFs, the 6 other coins, the 4 indexes.

### Pass bar (each variant judged alone; all must hold; six assets, 1994-2025, train only)

1. Sharpe beats `tsmom12` with bootstrap p < 0.05 (the protocol's 0.10 shared between two).
2. **Worst loss:** max drawdown not more than 5 points worse than `tsmom12`'s.
3. Not behind `tsmom12` on Sharpe over 2003-01-01 to the end of train, and worst loss over that
   window not more than 5 points worse.
4. Out of universe: the Sharpe difference to `tsmom12` is positive in at least 2 of the 3 sets,
   and the worst loss is not more than 5 points worse than `tsmom12`'s in at least 2 of the 3.
5. Beats equal weight on Sharpe.

**Reported pass or fail:** the yes/no per asset by year, Sharpe, growth and worst loss of the
variant, `tsmom12` and equal weight side by side (the trade the owner is shown: return per unit
of risk against worst loss).

**Held-out year (2025-11-11 to 2026-11-09).** Not looked at in this run, pass or fail. A pass
on train would be a candidate for one held-out look in a later run.

**What each outcome would mean.** Fail on bar 2 or 4 with a Sharpe gain: dropping the filter
where it buys no calm raises return per unit of risk but deepens the worst loss; a risk choice
for the owner, not an edge. Fail on bar 1: the walk-forward answer cannot tell early enough
where the filter pays. Pass: a candidate revision of the live rule.

### Assumptions

- "Rougher" is read on the asset's own bars, not on the rule's equity. The 5-year and 60-bar
  minimums are set here and not tuned.
- Default yes (filter on) under thin evidence, because `tsmom12` is the incumbent.
