# power-map-1: which kinds of strategy could ever pass the bar?

Lane `power-map-1`, 2026-11-24 night. Branch `power-map-1` from `main` (`f1d2da5`). Method
study: pure arithmetic and small simulations on the records' own standard errors and on the
committed weekly returns store (`research/register/returns/`). **No new strategy backtest, no
price bar loaded, nothing after 2025-11-10.** Card (this section) written and pushed before any
number below it was computed.

## Question

About 3,200 tries, none passed. The project-wide bar (`research/register/BAR.md`): a new pick
must beat `tsmom12` at **z >= 4.69** (N = 486 effectively independent trials, DSR 0.95), which
is +0.30 Sharpe for a rule close to `tsmom12` (SE 0.065) and +0.56 for a far one (SE 0.12) on
the primary test (six assets, 1994-02-01..2025-11-09, 1,657 weeks). `gate-power.md` and
`gate-null.md` show that most event-study gates could only kill. Before more nights go into
searches, map for each **kind** of strategy, with the history we can get keylessly, how big a
true edge must be to pass, and whether an edge that size is plausible.

## Method (fixed before any number)

### M1. Edge over `tsmom12` (the bar's own form)

Paired Sharpe difference d = SR_A - SR_B over Y years, B = `tsmom12`. For returns with
correlation rho (Jobson-Korkie with Memmel's correction, annualised, q periods a year):

    Var(d) = (1/Y) [2 - 2 rho + (SR_A^2 + SR_B^2 - 2 rho^2 SR_A SR_B) / (2 q)]

The second term is below 0.003 at weekly q and Sharpes near 1, so SE_d = k sqrt(2 (1 - rho) / Y).
Check against the record: SE 0.065 at 31.8 years gives rho 0.93, SE 0.12 gives rho 0.77, both as
`BAR.md` states; rho 0 gives 0.25, review-2's number. k is the ratio of a block-bootstrap SE
(52-week blocks, 2,000 draws, fixed seed) to the formula, **measured** on the committed series
(M5); k = 1 if the records give nothing better.

Minimum detectable edge (one-sided): MDE(z*, power) = (z* + Z^-1(power)) SE_d. Reported at
50% power (= the bar itself, z* SE) and **80% power** (z* + 0.84). z* = 4.69 (the bar); the
ONC end of the measured range, z* = 3.29, is shown beside it.

### M2. A different comparator: does A add to `tsmom12` (spanning / alpha test)?

Regress A's weekly excess returns on `tsmom12`'s; IR = alpha / residual SD, annualised;
t_alpha = IR sqrt(Y). MDE in IR: (z* + 0.84) k / sqrt(Y), independent of rho. Translated into
the Sharpe of the best mix of A and `tsmom12` (scale-free, so it holds without leverage):
sqrt(1.05^2 + IR^2) - 1.05. This is shown because the bar's difference form asks an
uncorrelated rule for a standalone Sharpe of about 2.2 at 32 years, while the alpha form asks
for what it adds. It is a proposal for the lead, not the bar.

### M3. Events and many bets

A strategy that makes E independent bets with per-bet Sharpe s (mean / SD of one bet's
return) has t = s sqrt(E), so the per-bet edge needed is (z* + 0.84) / sqrt(E), and its annual
IR is s sqrt(E / Y). Both views give the same annual IR bar as M2: **the bar in IR terms depends
on years of data, not on how many bars or bets there are**; more bets only lower the per-bet
edge needed (and raise the IR a given per-bet edge buys, the fundamental law IR = IC sqrt(B)).
Overlapping or clustered events count as their effective number (gate-power's
N_eff = N / (1 + 2 sum of autocorrelations)).

For crypto bets the per-bet edge is translated into basis points with the daily (or hourly)
return SD of BTC measured from the store's weekly BTC series (weekly SD / sqrt(7), and
/ sqrt(24) more for an hour, a random-walk scaling, stated as an approximation), and compared
with a round-trip cost of 10-30 bps (the cost range the coin lanes used).

### M4. Forward paper scoring

Years of forward record needed to confirm an edge d at 80% power:
Y = ((z* + 0.84) k sqrt(2 (1 - rho)) / d)^2 for an edge over `tsmom12`, and
Y = ((z* + 0.84) / S)^2 for a book's own Sharpe S against zero. z* for a forward test:
1.645 (one book registered before its record starts, no search on the forward data),
1.645 + E[max of 11] (the best of the 11 live books), and 4.69 (the bar). d in
{0.05, 0.10, 0.20, 0.30, 0.50}. For each live book: rho with `tsmom12` and the backtest d over
the live store's window (the 11 series in `returns/live.csv.gz`, from 1994-02-01), and the
forward years needed if that backtest d were the true edge (optimistic: backtest edges shrink).

### M5. Inputs measured from the committed store (no new backtest)

From `research/register/returns/*.csv.gz` (weekly strategy returns, train only), against the
primary `tsmom12` series (the six-asset `tsmom12` baseline from 1994-02-01; the live
`ts_momentum` series if that is what the store holds; the choice is printed):

- per stored series: overlap years with `tsmom12`, rho, the bootstrap SE of d and its ratio k
  to the formula;
- per class (families assigned by name before reading any number; list in the script):
  median rho and median overlap years, the median k;
- for the 13 developed markets (if the store holds `tsmom12@<market>` and a rule on the same
  market), the average correlation of the difference series across markets, giving the
  pooled effective years Y_eff = Y m / (1 + (m - 1) rho_d); otherwise a range rho_d 0.3-0.7.

### M6. Small simulation (checks the formulas, not strategies)

Pairs of weekly returns with Student-t(4) shocks (fat tails near the store's median excess
kurtosis), annual Sharpes 1.05 and 1.05 + d, correlation rho in {0, 0.5, 0.77, 0.93}, Y in
{6, 11, 32, 98}, 2,000 draws each, fixed seed: the Monte Carlo SD of d against the formula,
and the detection rate at the M1 MDE80 (should be about 80%). One frequency check: the same
Y sampled daily, weekly and monthly gives the same SE of the annual Sharpe (only years count).

### Classes and data (from the data records; years to 2025-11-09)

| Class | Data we can get keylessly | Years | Notes |
|---|---|---:|---|
| C1 slow trend / allocation | six ETFs/coins daily 1994-2025 (primary test); US stocks 1927-2025 (Yahoo ^GSPC, Ken French, Shiller); 13 developed markets 1966-2025 (price indices, insure-2) | 31.8 / 98 / 59.8 x 13 | the gym's own class |
| C2 cross-sectional, many assets | 34 ETFs (#106, about 2007-2025); coins top-N 2017-2025 (Binance); Ken French portfolios 1926-2025 (monthly, research only, not tradable in the gym) | about 18 / 8.3 / 99 | long-only in the gym (B7: no shorts) |
| C3 daily / intraday crypto, many bets | BTC daily since 2011-2014 (Bitstamp / Yahoo), 1-minute bars since 2017-08 (Binance) and 2015 (Coinbase); own intraday collectors since 2026-11-13 | 11-14 / 8.3 / 0 | 365-day markets |
| C4 event studies | FOMC since 1994 (8 a year), calendar effects (12 a year), weekly doses (gate-power), sparse episodes (10-40) | 31.8 or less | effective events, not rows |
| C5 carry with perps | funding since 2019-09 (Binance archive), Kraken 12 months | 6.2 | blocked: B6 (no perps), B7 (no shorts) |
| C6 forward-only paper scoring | the live record from 2026-11-11 | 0 so far | the only data no search has touched |

Plausibility is judged against the records, not new numbers: survey-6 (live, after fees: no
family beat its matched holding; style premia 0.50 and trend 0.17 above bills; published
effects kept a median 8% of the paper Sharpe), gate-power's yardstick (single timing signals
IR 0.2-0.5 in sample, 0.05-0.15 live), the project's own spread (primary-test SD 0.12; largest
edge seen +0.23), carry-3 (train +10.8% a year, held-out year -0.65) and rl-6 (246 weeks detect
only Sharpe >= 0.98). Where the records say nothing, the table says **unknown**.

### Outputs

- `research/powermap1.py` (numpy, stdlib, `returnstore`; deterministic), run as
  `uv run --with numpy python research/powermap1.py`; its printout goes into
  `research/results/power-map-1.md`.
- This file: the table (class, data, N_eff / Y_eff, edge needed, plausible?) and a ranked
  recommendation for future lanes.
- One `note` row in `research/tries.md` (no selectable try; the register count is unchanged
  except for that note).

## Results

(Filled in after the runs.)
