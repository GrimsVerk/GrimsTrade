# Card: trend-where-long (fixed 2026-11-18, before any number of this run)

Lane `data-long-2`, step 3. A robustness check of an existing rule, `where-vol` of lane
trend-where (PR #43, `research/trend-where.md` on branch `trend-where`), on monthly data before
2002. It is not a new selection: it cannot rescue `where-vol` (which failed its bar) and it picks
nothing.

## What had been seen when this was written

- `trend-where.md` in full: `where-vol` tied `tsmom12` on Sharpe 1994-2025 and its worst loss
  over the whole period was no deeper, but that rests on one episode (2022) in which it lost
  twice as much (-26% vs -13%), because it had dropped the filter on bonds (from 2009) and gold
  (from 2015). On 1926-1961 US industries it never dropped the filter.
- `research/data-long-2.md` sections 1-2 and the year-by-year cross-check table: annual returns
  of the Shiller bond, datahub gold and Damodaran series 1928-2024. So the big bond and gold
  years are known (bond bear 1965-1981, 1982 rally; gold 1979-80 spike and 1981-1985 and
  1996-1999 falls). No trend rule, no in/out split and no drawdown of any strategy on these data
  has been computed.

## Question

On long US bonds (1953-2001) and gold (1971-2001), does the walk-forward per-asset switch
`where-vol` drop the trend filter, and if so, does the worst loss get deeper than always-on
`tsmom12`'s? This is the "more than one episode" test that `trend-where.md` asked for.

## Data (section 2 of `data-long-2.md` fixes these choices)

- **Bond:** Shiller "Monthly Total Bond Returns" (`lib/long_bond.py`), only labels from 1953-04
  on (before that the yield is interpolated between Januaries: look-ahead inside the data).
  Label t is the return from month t to t+1, so it is re-dated to t+1: the return dated m runs
  from the month-(m-1) average yield to the month-m average yield and is known at the end of m.
- **Gold:** datahub monthly (`lib/long_gold.py`), returns dated m = price(m) / price(m-1), from
  1971-01 (`FREE_FROM`). Prices are monthly averages.
- **End:** the last return used is dated 2025-10. Held-out year (from 2025-11-11) not touched.
- Cash earns 0 (the repo's convention; it understates the growth of every rule that sits out,
  not the worst loss). Cost 2 bps a side on each change of weight (the gym's ETF slippage).

## The rule, translated to monthly bars (nothing else changed)

- **Signal:** at the end of month k, `tsmom12` is on if the 12 returns dated k-11..k compound
  to more than 1 (12-month log return > 0, as `trend_tune.signal`). Needs 12 returns (an asset
  is eligible after a year of bars, as `common.eligible`).
- **Gap:** that signal trades the return dated k+2, not k+1. Both series are monthly averages,
  so the return dated k+1 starts mid-month k, before the decision; trading it would let the
  signal see half of the return it trades. Same gap for `where-vol`, `tsmom12` and hold.
- **In and out:** a return is *in* if the signal that traded it was on, *out* if off, left out
  if no signal existed.
- **Refit:** at the end of each December, from returns dated up to that December and their
  in/out labels only (expanding window). The answer governs every decision made in the
  following calendar year (decision at end of month k uses the refit of the last December <= k).
- **Yes/no:** keep the filter (yes) if the standard deviation of the out returns is larger than
  that of the in returns; otherwise (no) the slot is simply held. Yes by default with under 5
  years of eligible returns or fewer than 60 out or 60 in returns (the trend-where minimums,
  read as counts of bars; on monthly bars that is 5 years of each).
- **Book:** equal slots among eligible assets; a slot is held if the answer is no, or yes and
  the signal is on; empty slots are cash. With every answer yes it is `tsmom12` exactly.

## Runs (each one row in `research/tries.md`, idea `trend-where`)

Books: `bond-m` (bond alone), `gold-m` (gold alone), `bondgold-m` (both, equal slots, from when
gold is eligible). Each run covers its data start to 2025-10; the row reports the window up to
2001-12 (the card's question); the write-up also gives 2002-2025.

1. `where-vol@<book>`: the rule above. `robustness` rows (3).
2. `tsmom12@<book>` and `hold@<book>`: twin and benchmark. `baseline` rows (6).
3. Two sensitivities, disclosed, not selectable (`robustness` rows):
   - `where-vol-min12@<book>`: minimums 12 out and 12 in months (a year of each) instead of 60,
     because 60 monthly bars is a far stricter wait than 60 daily bars (3).
   - `where-vol-lag0@<book>` and `tsmom12-lag0@<book>`: no gap month, to show how much the
     monthly averages flatter a trend rule (6).

Sharpe in these rows is monthly returns x sqrt(12) (not the repo's daily x sqrt(365)); noted in
each row's variant name by the `-m` book suffix. Run once.

## What is read off

1. **Worst loss** (max drawdown of monthly equity) of `where-vol`, `tsmom12`, hold, per book, to
   2001-12 and inside two windows fixed now: bond 1965-01 to 1981-09 (the yield peak), gold
   1980-01 to 2001-12 (peak to the end of the long bear). "No deeper" = within 5 points of
   `tsmom12`, the trend-where bar 2.
2. The yes/no per asset by year, and how many asset-years are no.
3. Sharpe and growth against `tsmom12`, with a paired stationary-bootstrap p (6-month blocks).

## Expected before looking

Unknown for bonds: in 1965-1981 out months (falling 12-month return, rising yields) may well be
rougher than in months, which keeps the filter (yes) and makes `where-vol` equal `tsmom12`. With
60-month minimums the gold answer cannot leave yes before ~1990 at the earliest, so the 1980-85
gold fall is met with the filter on by construction; only the min12 sensitivity can test it.
If answers turn no and the worst loss deepens by more than 5 points, the 2022 episode was not a
one-off: dropping the filter on bonds or gold buys depth of loss. If answers stay yes, the
question stays where `trend-where.md` left it, now on 50 more years.

## Assumptions

- Monthly averages and a 10y constant-maturity rebuild are not tradable prices; worst losses
  read shallower than on daily closes of a real fund. The comparison between rules is fair
  (same data, same gap), the levels are not.
- The 60-bar minimum is read as 60 bars, not as 60 trading days of calendar time; the min12
  sensitivity covers the other reading.
