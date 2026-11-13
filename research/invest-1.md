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

## Results (2026-11-13; tables in `results/invest-1.md`, 33 rows in `tries.md`)

### In plain words

- **No slow signal passed.** None of the 8 variants beats 60/40 in both periods by the card's
  bar, and none adds to the trend rule out of sample. The answer to "which slow signals improve a
  long-horizon allocation over 60/40 and the trend rule" is: none that we can prove.
- **Valuation really does forecast the next decade, but that does not make money for an
  allocator.** Cheap stocks (high earnings yield, high excess CAPE yield) were followed by better
  10-year real returns since 1881 (R² 0.27-0.33). The overlapping-window t-values look huge
  (4-6), but there are only 14 non-overlapping decades, and on those the t-value is about 2.
  Turned into a tilt of 60/40, the CAPE signal earned nothing after 1990 (Sharpe 0.67 vs 0.67):
  US stocks looked expensive for most of 30 years and kept going up. The excess CAPE yield
  (which compares stocks with real bond yields) did better: +0.08 Sharpe before 1990 (p 0.002),
  +0.06 after (p 0.15), -0.01 on the ETFs 2003-2025. Right sign, too small to trust.
- **The trend rule is still the thing that holds up, and what it buys is safety, not return.**
  Monthly `tsmom12` beat 60/40 by +0.12 Sharpe before 1990 and +0.10 after (not significant on
  its own, p 0.17 and 0.22), but its worst fall was 19% against 63% (1927-89) and 8% against 29%
  (1990-2025). It gives up about 1 point of return a year for that.
- **Closest call:** the excess-CAPE-yield tilt inside the trend rule (`ecy-trend`) had the best
  Sharpe in both periods (0.62 and 0.82 against trend's 0.53 and 0.77). It beat the trend rule
  clearly before 1990 (p 0.002) but not after (p 0.13), and on the ETFs 2003-2025 it trailed it
  (0.94 vs 0.97). Parked, not dead: it is the one idea worth re-checking as data accrues.
- **Dead:** term spread, real-yield tilt, inflation switch (bonds to cash when inflation > 4%),
  dual momentum across stocks/bonds/cash, and the 10-month moving average (equal to its trend twin).
- **How sure:** the whole answer rests on about 10 independent decades of strategy returns (6.3
  train, 3.6 out of sample) and 14 non-overlapping decades of valuation history. That is enough
  to see that valuation forecasts the decade, and not enough to prove a tilt of +0.05-0.10
  Sharpe out of sample: at the same gain, `ecy-tilt` would need about 55 years of out-of-sample
  data instead of 36 to reach p < 0.10.

### Main numbers (excess Sharpe, monthly, 10 bps per side)

| Rule | Train 1927-89 | p vs 60/40 | OOS 1990-2025 | p vs 60/40 | ETF 2003-25 | Max DD train / OOS |
|---|---:|---:|---:|---:|---:|---:|
| `6040` | 0.41 | | 0.67 | | 0.76 | 63% / 29% |
| `bh-stocks` | 0.40 | 0.73 | 0.59 | 0.89 | 0.68 | 84% / 50% |
| `tsmom12-m` | 0.53 | 0.17 | 0.77 | 0.22 | 0.97 | 19% / 8% |
| `cape-tilt` | 0.43 | 0.27 | 0.67 | 0.52 | 0.71 | 61% / 22% |
| `ecy-tilt` | 0.49 | 0.002 | 0.73 | 0.15 | 0.75 | 57% / 31% |
| `term-tilt` | 0.38 | 0.92 | 0.57 | 0.97 | 0.60 | 63% / 35% |
| `real-tilt` | 0.46 | 0.19 | 0.64 | 0.69 | 0.68 | 49% / 38% |
| `infl-regime` | 0.41 | 0.44 | 0.69 | 0.34 | 0.80 | 63% / 33% |
| `6040-sma10` | 0.52 | 0.18 | 0.75 | 0.32 | 0.81 | 25% / 9% |
| `xmom` | 0.51 | 0.23 | 0.59 | 0.72 | 0.55 | 44% / 21% |
| `ecy-trend` | 0.62 | 0.04 | 0.82 | 0.16 | 0.94 | 19% / 10% |

Pass bars: `ecy-tilt` passes bar 1 (train), bar 3 (7 of 10 decades) and bar 4, fails bar 2
(OOS p 0.15). `ecy-trend` passes bars 1 and 4, fails 2 (p 0.16) and 3 (5 of 10 decades: behind
60/40 in the 1950s, 1960s and 2010s, when trend whipsawed). `cape-tilt` and `real-tilt` reach 6
decades but fail both p-values. Nothing passed, so no 30 bps robustness run was needed.

Eras (OOS, protocol): the CAPE and ECY tilts lost to 60/40 in 2022-25 (CAPE tilt -0.11, ECY
0.07, against 0.20: underweight stocks in a strong market, overweight bonds in the 2022 rate
shock), and every trend or momentum rule won 2000-09 (0.39-0.65 against 0.05).

### Long-horizon forecasts (next 10-year log real stock return, 1881-2013)

| Signal | Slope | R² | t (Newey-West) | t (Hansen-Hodrick) | Non-overlapping decades | t on those |
|---|---:|---:|---:|---:|---:|---:|
| earnings yield 1/CAPE | 8.3 | 0.27 | 5.9 | 6.2 | 14 | 2.0 |
| excess CAPE yield | 6.2 | 0.33 | 4.3 | 4.1 | 14 | 2.3 |
| term spread (from 1926) | 9.4 | 0.05 | 2.4 | 2.6 | 9 | 0.1 |
| real 10-year yield | -2.1 | 0.05 | -2.2 | -2.0 | 14 | -3.0 |
| inflation | 2.2 | 0.07 | 2.9 | 2.8 | 14 | 2.2 |

The overlapping-window corrections (Newey-West, Hansen-Hodrick) give t-values two to three times
the non-overlapping ones: with 14 real data points they are not to be believed at face value.
Only the two valuation signals keep the same sign at 1, 5 and 10 years and in both methods; the
term spread's non-overlapping slope even flips sign at 5 years. Real yields and inflation at 10
years carry the 1970s-80s story (high inflation, then a great decade) and not much else.

Where we are now: CAPE was 41 in October 2025 (45 at the 1999 peak; average ~17). History says
the next decade's real stock return is likely low; this run says an allocator could not have
turned that kind of warning into a better Sharpe after 1990.

### Deviations from the card (all noted before writing this section)

- Forecasts use the next h-year **real** stock return, not real excess (no T-bill rate before
  1926); Shiller's real total-return price is a monthly average, so a signal and its forward
  window overlap by half a month (negligible at 1-10 years).
- ETF check starts 2003-09 (the first month SPY and IEF both have 12 months of returns), not
  2003-01.
- Trend rules are their base (all held) for the first six months of train (1927-01..06), until
  12 months of French returns exist. The term-spread tilt is plain 60/40 until 1936-07 (120
  months of its own history).
- Shiller's earnings stop in 2023; the last value is carried forward (card), so valuation
  signals in 2024-25 move with price only.
- Stress windows were not computed (monthly data); the protocol eras are reported instead.
- The report was re-run once with `--no-log` to fix a display bug (real CAGR showed NaN because
  CPI for 2025-10 is not out); no strategy number changed and no row was logged twice.

## Sketch: the investing agent next to the trading agent (described, not built)

- **Own book.** A second fake-money account (say 10,000 USD) in the same gym, with its own
  strategy ids (`invest/<name>`) and its own ledger lines in the same append-only `ledger/`
  files, tagged by book. The trading agent's numbers and the investing agent's never mix, and
  the scoreboard shows the two books side by side.
- **Monthly decisions.** The daily runner already runs every day; an investing strategy decides
  only on the last trading day of a month (or quarter) and repeats its weights otherwise, like
  the weekly research strategies. Fills at the next open, same costs, same 1% band. A decision
  day with no new month-end close writes nothing.
- **Inputs.** Prices of SPY, IEF/TLT, GLD and cash (T-bill interest, which the investing book
  needs more than the trading book does: it may sit in cash for years). Valuation and CPI with
  the lags of this card, from a small monthly file the runner can read without keys (Shiller's
  sheet stopped in 2023, so a maintained source is needed first: FRED keyless CSV is blocked for
  our client; a monthly file committed by a person or an agent is the simple route).
- **Judged on years.** Its scoreboard shows rolling 1-, 3- and 10-year returns and drawdowns
  next to 60/40 and `tsmom12-m`, and says plainly that a year of paper results proves nothing at
  this horizon. The tries count and deflated Sharpe apply as for the trading agent.
- **What it would hold first.** On this run's evidence: `6040` and `tsmom12-m` monthly
  (SPY/IEF/cash) as the baselines, nothing else live. `ecy-trend` stays parked; the valuation
  numbers are shown as context ("expected 10-year return is low"), not traded.

## Status

Done 2026-11-13: card, data layer, as-of test, 8 variants + 3 baselines on train and OOS,
forecasts, ETF check, write-up. Held-out year (2025-11..2026-11) untouched. Draft PR #24
(`invest-1` -> `short-1`), not merged. Possible next steps (owner's choice): a maintained monthly
valuation source; a gold and international-stocks extension (needs keyless long gold history);
re-check `ecy-trend` on the held-out year only if a later card gives a reason.
