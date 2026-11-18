# Trend where: keep the trend filter only where it buys calm

Research run trend-where, started 2026-11-18. Branch `trend-where` (from `trend-tune`). Research
only: fake money, the price cache already on disk, no change to the gym, the daily runner or the
live strategies. This is next lane 2 of `trend-tune.md`.

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
