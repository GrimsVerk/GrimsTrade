# diversifier-1: a held merger-arbitrage slot next to `tsmom12`

Field: allocation, risk (survey-6, "positive and uncorrelated" families). Written 2026-11-18
23:20 UTC, lane diversifier-1 (base `survey-6`), **before any daily return of the book below
was computed**. Seen before: survey-6's monthly live-fund numbers (`results/live-families.md`):
MERFX Sharpe above bills 0.44 (1989-2025), MNA 0.30 (2009-2025), the merger-arb composite
+14% in 2000-02 and -3% in 2008-09. That is why this family is asked about at all: the pick
of the family is itself made on those numbers, and is counted below.

## Question

Does adding one live, keyless-priced merger-arbitrage holding as a **held seventh slot** make
the paper book (`tsmom12` on SPY, QQQ, TLT, GLD, BTC, ETH) a better **risk** choice (worst
loss, crash windows, time under water)? And is there any Sharpe evidence for it?

A pass on risk alone is **a preference, not an edge**: it would be an owner's choice of
drawdown shape, not a forward claim, and it does not pass the project bar.

## Instrument choice rule (fixed now)

- Family: the survey-6 family that is (a) positive after fees live, (b) uncorrelated with
  stocks, and (c) buyable as a plain fund or ETF with the longest keyless daily history.
  Style premia fails (c) for most investors (QSPIX: mutual fund, 2013, high minimum); trend's
  longest live funds are shorter and `tsmom12` already is a trend rule. **Merger arbitrage.**
- Primary instrument: **MERFX** (The Merger Fund), the longest live merger-arb record with a
  keyless daily NAV (from 1989-01-31), so the whole train window and all named crash windows
  are covered. NAV is after the fund's fees.
- Robustness (same configuration, other data, after the choice): **MNA** (the merger-arb ETF,
  from 2009-11-17), from its first eligible day (a year of bars), against `tsmom12` on the same
  days. This is the vehicle most investors would actually buy.

## Rule (fixed; one selectable variant)

- The primary variant is **`merfx7`**: each Friday, weights =
  6/7 x (`tsmom12`'s weights on the six) + **1/7 in the diversifier, always held** (once it has a
  year of bars, as every asset). The diversifier is never timed. The rest of `tsmom12`'s cash
  stays cash (cash earns 0, as in the protocol).
- Slot size 1/7 fixed a priori: "one more equal slot" when all six are live. No other size
  is run.
- Robustness: `mna7@mna` (the same rule with MNA), from MNA's first eligible day.

## Data, period, costs

- Train only: decisions 1994-02-01 .. 2025-11-09; no bar after 2025-11-10 is loaded. The
  held-out year is not looked at.
- MERFX and MNA daily bars from the Yahoo chart API (`lib/fetch.yahoo_all`, keyless),
  dividend-adjusted (total return), git-ignored. MERFX is a mutual fund: its "open" is the
  day's NAV, so a Friday order fills at the next business day's NAV (realistic for a fund).
- Costs: `grimstrade.gym.simulate` unchanged (2 bps a side for the ETF-class slots, 30 bps in
  crypto, 1% band). MERFX sales loads (not in NAV) are not modelled: kind to the book, stated.

## Comparator and metrics

Comparator: `tsmom12` (baseline, already logged; re-scored with `log=False`). Also shown:
equal weight (the protocol's pass condition 5).

Sharpe (daily, 365 days, zero risk-free rate, `stats.sharpe`), difference to `tsmom12` with the
paired stationary bootstrap (one-sided p, 90% range) and its z = d / SE (SE = bootstrap
standard deviation of the difference).

Risk metrics: max drawdown; worst calendar year; total return in the 2008 crisis
(2007-10-09..2009-03-09), the covid crash (2020-02-19..2020-03-23) and calendar 2020-Q1, the 2022
rate shock (2022-01-03..2022-10-12) and calendar 2022 (dot-com bust shown, not scored); time
under water = longest peak-to-recovery stretch in calendar days, and share of days below a
prior peak. Correlation of the diversifier's daily returns with SPY and with `tsmom12`.

## Bars

- **Family bar** (protocol pass bar, one variant): Sharpe beats `tsmom12` with bootstrap
  p < 0.10, ahead in at least 4 of 5 eras, max drawdown not more than 5 points worse, and beats
  equal weight. Out-of-universe condition: none applies (no second set of "six assets plus a
  merger-arb fund"); stated as a limit, so even a family pass is not a train pass.
- **Project bar** (`research/register/BAR.md` on `origin/register-2`, rows through
  2026-11-18 23:04): 3,023 tries, N 1,027 for a new pick, measured rho 0.58 -> **N 433
  effective; z >= 4.65 (DSR 0.95), edge over `tsmom12` +0.30 (close rule, SE 0.065);
  Bonferroni p <= 1.2e-4 (z 3.68)**. This rule is closer to `tsmom12` than the "close rule"
  (6/7 of the book is identical), so its own bootstrap SE is used with the z column.
- **Risk preference** (fixed now; all three needed): (a) smaller max drawdown than `tsmom12`,
  (b) a smaller loss (or larger gain) in at least 2 of the 3 named crash windows (2008 crisis,
  covid crash, 2022 rate shock), (c) longest time under water not longer. Met = "preferred on
  risk" (a preference, not an edge); not met = "no risk case".

## Count

`merfx7` is one `variant` row (a pick: counted in the family and project-wide).
`mna7@mna` is one `robustness` row. `tsmom12` and equal weight are re-scored, not logged.

## Result

`results/diversifier-1.md` and the verdict in `research/diversifier-1.md`, once run.
