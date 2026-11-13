# Invest 1: what can a long-horizon allocator honestly know?

Brief: `chief-of-staff/briefs/grimstrade-invest-1.md`. The first research run for the owner's
investing agent (`docs/BACKLOG.md`, "Investing agent"): months-to-decades horizon, same honesty
rules as the trading agent. Question: do slow signals (valuation, yields, inflation, trend,
cross-asset momentum) improve a stock/bond/cash allocation over 60/40 and over the 12-month trend
rule, and how many independent decades does any answer rest on?

## Card (fixed 2026-11-13 ~08:30 UTC, before any number was computed)

### Data (raw cache, read with `python -I`, never committed)

Monthly, decisions at each month end `t`, the new weights earn month `t+1`.

- **Stocks:** US market total return, Ken French `Mkt-RF + RF` (CRSP value-weighted,
  month-end to month-end), 1926-07 onward.
- **Bonds:** a constant-maturity 10-year par Treasury, return computed from yields:
  `r = y(t-1)/12 + price change of a 10-year par bond (coupon y(t-1)) repriced at y(t) with
  9 11/12 years left`. Yields: Shiller's `GS10` before 1962 (monthly *averages*: smooths bond
  returns by about half a month; train period only), FRED `DGS10` last daily value of each
  month from 1962 (month-end, clean).
- **Cash:** French `RF` (1-month T-bill), earned on whatever is not in stocks or bonds.
- **Gold:** no keyless monthly gold history before 2000 in the cache (and the price was fixed
  until 1971), so gold is not in the main test. It enters only the ETF check (GLD, 2005+).
- **Valuation:** Shiller `ie_data.xls` (P, E, CPI from 1871; ends 2023-09). After that, P is the
  monthly average of `^GSPC` daily closes (Shiller's own definition of P), and E stays at its
  last known value (stale earnings: the 10-year average moves little in two years; disclosed).
- **CPI:** Shiller's CPI to 1946-12, FRED `CPIAUCSL` (latest values, rarely revised) from 1947.

The cache holds data into 2026. Nothing after 2025-10 is loaded: the protocol's held-out year
(2025-11-11 .. 2026-11-09) is not touched by this run.

### Publication lags (the as-of rule)

At the decision at the end of month `t`:

- Prices, yields and the T-bill rate of month `t` are known (market data).
- CPI is used through month `t-2` (released mid-month after; one extra month of margin for the
  older history).
- Shiller's E is used through month `t-6`. His monthly E is interpolated between quarter ends,
  so the value for month `m` depends on a quarter end up to two months later, and S&P reports
  roughly three months after a quarter. Six months covers both.
- A test (`tests/test_invest1_asof.py`) proves that scrambling every input after the lagged
  month leaves each signal unchanged.

### Signals (all computed from as-of data only)

- `ey` = 1 / CAPE, CAPE = (P(t) / CPI(t-2)) / mean of real E over the 120 months ending `t-6`.
- `ecy` = excess CAPE yield = `ey` - (y(t) - 10-year annualised CPI inflation to `t-2`)
  (Shiller's definition with our lags).
- `term` = y(t) - 12 x RF(t) (10-year yield minus the T-bill rate).
- `real` = y(t) - CPI inflation over the 12 months to `t-2`.
- `infl` = CPI inflation over the 12 months to `t-2`.
- `mom12(asset)` = total return over the last 12 months (to `t`).
- `sma10(asset)` = total-return index above its average of the last 10 month ends.

A percentile `p` is the share of all earlier months (from the first month the signal exists)
whose value is below the current one: expanding, never fitted on the future. Before a signal has
120 months of its own history, `p` = 0.5 (the rule is its base allocation).

### Baselines (rows of kind `baseline`)

- `6040`: 60% stocks, 40% bonds, rebalanced monthly.
- `bh-stocks`: 100% stocks.
- `tsmom12-m`: the trend twin, monthly: stocks and bonds each get half; a half is held while its
  12-month total return is positive, else it sits in cash (the repo's `tsmom12`, monthly).

### Variants (rows of kind `variant`; 8, fixed here)

Tilts move the stock share around 60% (between 30% and 90%), the rest in bonds:

1. `cape-tilt`: stocks = 0.6 + 0.6 x (p(`ey`) - 0.5). Cheap stocks (high earnings yield): more.
2. `ecy-tilt`: the same with p(`ecy`).
3. `term-tilt`: the same with p(`term`) (steep curve: more stocks).
4. `real-tilt`: stocks = 0.6 - 0.6 x (p(`real`) - 0.5) (high real yields: bonds are cheap, more
   bonds).
5. `infl-regime`: 60/40, but the bond 40% sits in cash while `infl` > 4%.
6. `6040-sma10`: 60/40 with a 10-month moving-average filter on each sleeve (out to cash).
7. `xmom`: cross-asset (dual) momentum: all in the one of stocks or bonds with the higher
   `mom12`, if that beats cash's 12-month return; else all cash.
8. `ecy-trend`: `ecy-tilt` weights, with each sleeve in cash while its `mom12` is negative
   (valuation plus the trend rule).

### Costs

10 bps per side on every change in stock or bond weight (index funds in the old decades cost
more; 30 bps is run as `robustness` for any variant that passes). Cash trades free.

### Periods

- **Train:** decisions 1926-12 .. 1989-11 (returns 1927-01 .. 1989-12), ~6.3 decades.
- **Out of sample:** returns 1990-01 .. 2025-10, ~3.6 decades. CAPE was published (Campbell and
  Shiller 1988) before this window began, so for valuation it is a true post-publication test.
  It is not virgin for the trend rule: earlier runs saw `tsmom12` win on 1994-2025 ETF data.
- **Eras** inside the OOS window (protocol): 1994-99, 2000-09, 2010-16, 2017-21, 2022-25.
- **Decades:** 1927-39, 1940s, 1950s, 1960s, 1970s, 1980s, 1990s, 2000s, 2010s, 2020-25 (10).

### Metrics

Sharpe of monthly returns **in excess of cash** (RF), x sqrt(12) (over these decades cash paid
up to 15%; zero-rate Sharpe would flatter anything that holds cash). Also CAGR, real CAGR (CPI),
max drawdown on month ends, turnover, and the worst rolling 10-year real return.

### Pass bars

A variant **beats 60/40** only if all hold:

1. Train: excess Sharpe above `6040`, paired stationary block bootstrap of monthly returns (mean
   block 24 months: positions persist for years; 2,000 draws, seed 0), one-sided p < 0.10.
2. Out of sample: the same test, p < 0.10.
3. Ahead of `6040` on excess Sharpe in at least 6 of the 10 decades.
4. Max drawdown not more than 5 points worse than `6040`'s, in each period.

A variant **adds to the trend rule** only if, in addition, it beats `tsmom12-m` on excess Sharpe
with p < 0.10 in both periods.

With 8 variants and two independent periods each at p < 0.10, the chance that at least one pure
noise variant passes both is about 8 x 0.01 = 8%: a single pass is evidence, not proof.

### Long-horizon forecasts (descriptive, not selectable, no `tries.md` rows)

For each slow signal, the slope of the next 1-, 5- and 10-year real excess stock return on the
signal (1881-2015 with Shiller's real total-return price where French is missing; 1927-2015
otherwise), with three standard errors: Newey-West (lags 1.5 x horizon), Hansen-Hodrick
(lags = horizon - 1), and a non-overlapping regression (one point per horizon window, so 10-year
results rest on ~9-13 points). The honest count of independent observations is the number of
non-overlapping windows, and it is reported next to every number.

### ETF check (robustness)

Baselines and every variant re-run on SPY / IEF (2003-01 .. 2025-10, Yahoo adjusted closes,
month ends; cash = French RF), with GLD as a third risk asset in `xmom` from 2005-12. Same
signals. Kind `robustness`.

## Results

(Filled after the runs.)
