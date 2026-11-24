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

## Results (computed 2026-11-24 after the card, `ebc7a82`, was pushed)

Full tables: [`results/power-map-1.md`](results/power-map-1.md), generated by
`research/powermap1.py` (20 s, numpy). All inputs are the committed weekly store (train only)
and numbers quoted from the records.

### In plain words (one screen)

- **No kind of strategy we can test has a realistic chance of passing the bar.** For every
  class where the records give a plausible size, a true edge at the top of that range would
  clear z 4.69 with a probability between about 2e-5 and 0.02 in the bar's difference form,
  and at most 0.026 (1 in 38, Ken French portfolios) in the alpha form (table below). For
  high-frequency crypto and perp carry the size is unknown; even an assumed residual IR of 1.5
  would pass only 11-24% of the time. The search did not fail for
  lack of ideas: with this data, the bar cannot be reached by edges of the size that exist.
- **Power depends on years of data, not on how many bars** (iid simulation, given return
  process). Daily, weekly and monthly sampling of the same 32 years give the same SE of the
  annual Sharpe at a true Sharpe of 1.0 (0.176 / 0.176 / 0.179 in the simulation, against
  0.177 / 0.178 / 0.180 from the formula). Minute bars only help a strategy whose true Sharpe is high because it makes
  many bets; they do not lower the bar.
- **The two levers that move the numbers are more years and a different comparator.** Pooling
  13 developed markets 1966-2025 gives about 191 effective years (the difference series of a
  rule against each market's `tsmom12` correlate only 0.26 across markets), which brings the
  edge needed for a trend-like rule down to +0.18 (from +0.44 on the six assets at the
  store's median correlation 0.88). Still about twice the largest plausible edge (+0.10).
  For a rule uncorrelated with `tsmom12`, at 32 years and 80% power, the bar's difference
  form asks a standalone Sharpe of 2.55; an alpha (spanning) test asks a residual IR of 1.06,
  which is +0.44 on the best mix (at 50% power: 2.3 against IR 0.90, +0.33).
- **The only combination where an honest pass is not absurd:** a long-short, multi-asset
  style book (the one live family with a positive, uncorrelated record, survey-6: Sharpe 0.50
  over 12 years) tested on about 100 years of data under the alpha form, where the bar is
  IR 0.51 (50% power) to 0.60 (80%). That needs shorts (B7), a comparator change, and data
  that is not tradable in the gym (Ken French portfolios). Its live 0.50 sits at the bar at
  50% power, before any decay.
- **Forward paper scoring cannot confirm an edge in any useful time.** An edge of +0.10 over
  `tsmom12` by a book correlated 0.95 with it needs 72 years of forward record at 80% power
  even if registered alone (z 1.645), 356 years at the bar. Every live book's backtest edge
  over `tsmom12` is negative (-0.08 to -1.13), so there is no edge to confirm. A book's own
  Sharpe of 1.0 against zero takes 7 years at z 1.645. The live record is an implementation
  check and a description, not a test of edge.
- **The bar barely moves with more tries.** z needed: 4.69 at N 486, 4.90 at 1,000, 5.09 at
  2,000, 5.33 at 5,000. Tries are not the binding constraint; years of independent data are.

### The map

Edge over `tsmom12` in annual Sharpe. SE of d = k sqrt(2 (1 - rho) / Y), with k = 1.08 (the
median ratio of the 52-week block-bootstrap SE to the formula over 800 stored series; p75
1.27). rho: the store's median for the class against the `tsmom12` of the same universe.
"Plausible" is the record's evidence, not a new estimate. "Chance" is the probability that a
true edge at the **top** of the plausible range clears z 4.69 (difference form; alpha form).

| Class | Data (keyless) | Y_eff | rho | Edge needed, z 4.69: 50% / 80% power | Alpha form: IR needed, 80% | Plausible true size | Chance to pass | Honest pass possible? |
|---|---|---:|---:|---|---:|---|---|---|
| C1 slow trend, six assets | daily 1994-2025 | 32 | 0.88 | +0.44 / +0.51 (bar's close rule, rho 0.93: +0.30) | 1.06 | d 0 to +0.10 (project's max on the primary test +0.23; spread SD 0.12); live trend 0.17 above bills | 1.5e-4; 4.7e-5 | **no** |
| C1 slow trend, US 1927-2025 | S&P / Ken French | 98 | 0.88 | +0.25 / +0.29 | 0.60 | same | 2.5e-3; 4.6e-4 | **no** |
| C1 slow trend, 13 markets pooled | 1966-2025 | 191 | 0.88 | +0.18 / +0.21 | 0.43 | same | 0.02; 2.8e-3 | **no** (closest; tests "works across markets", not "better on our six") |
| C2 cross-sectional, ETFs / coins | about 2007-2025 | 18 | 0.84 | +0.67 / +0.79 | 1.41 | IR 0 to 0.30; survey-6: momentum funds live IR -0.03, long-only factor funds matched their index | 3.4e-5; 2.2e-4 | **no** |
| C2 cross-sectional, 1927- | Ken French portfolios (research only), at the long-only class rho 0.84; a long-short book near rho 0 needs about +0.85 at 80% power in the difference form | 98 | 0.84 | +0.29 / +0.34 | 0.60 | IR up to 0.30 post-publication (UMD 0.26); style premia live 0.50 | 1.2e-3; 0.03 (at IR 0.50: about 0.45) | **only here, and only in the alpha form; needs B7** |
| C3 crypto, daily bets | BTC daily 2014-2025 | 11 | 0.92 | +0.61 / +0.72 | 1.78 | **unknown**; the project's coin lanes found no edge that survived (cointop-1, rl-6, halving-2 z <= 3.1) | 8.5e-3; 0.06 at an assumed IR 1.0 | **unlikely**; needs a net 40 bps a day per bet |
| C3 crypto, hourly bets | Binance 1-minute 2017-08..2025-11 (own collectors: days) | 8 | 0.1 (assumed) | +2.37 / +2.79 | 2.08 | **unknown**; costs of 10-30 bps a round trip are 5-16x the net edge an hourly bet needs | 2.1e-5; 0.24 at an assumed IR 1.5 | **unknown, cost-bound** |
| C4 event studies | events 1994-2025 | 32 | 0.92 | +0.36 / +0.43 | 1.06 | IR 0.05-0.15 live (gate-power yardstick); 0 of 19 gates; FOMC drift gone after publication (ann-1) | 2.6e-5; 4.7e-5 | **no** (sparse designs kill-only) |
| C5 perp carry | funding 2019-09..2025-11 | 6 | 0.2 (assumed) | +2.57 / +3.03 | 2.40 | carry-3: train +10.8% a year, held-out year -0.65 | 7.9e-5; 0.11 at an assumed IR 1.5 | **no**, and blocked (B6/B7) |
| C6 forward paper scoring | live record since 2026-11-11 | 0 | 0.23-0.95 | see below | - | all 11 books' backtest d < 0 | - | **no edge to confirm**; years per the table below |

Bets per class (M3): the per-bet Sharpe needed at z 4.69 and 80% power is 0.37 for FOMC days
(254 since 1994), 0.31 for a monthly effect since 1994, 0.17 for a monthly effect since 1927,
1.3-1.4 for 18-20 sparse or seasonal episodes (a mean event return above one SD: kill-only),
0.093 for daily BTC bets (39.5 bps net a day at a 4.2% daily SD) and 0.022 for hourly bets
(1.9 bps net an hour, against 10-30 bps of cost per round trip). Whatever the count, the
annual IR is 1.06 at 32 years, 1.78 at 11, 2.08 at 8.

Forward years (M4), 80% power, edge d over `tsmom12`:

| Book's rho with `tsmom12` | z | d +0.10 | +0.20 | +0.30 | +0.50 |
|---|---|---:|---:|---:|---:|
| 0.95 (presets, trend variants) | 1.645 (registered alone) | 72 | 18 | 8 | 3 |
| 0.95 | 3.27 (best of 11 live) | 196 | 49 | 22 | 8 |
| 0.95 | 4.69 (the bar) | 356 | 89 | 40 | 14 |
| 0.77 | 1.645 | 331 | 83 | 37 | 13 |
| 0.00 | 1.645 | 1,437 | 359 | 160 | 57 |

Against zero, a book's own Sharpe S at z 1.645: S 0.5 needs 29 years, 1.0 needs 7, 2.0 needs
1.8. The live books' backtest correlation with `tsmom12` (1994-2025) runs from 0.23
(`crypto_mean_reversion`) to 0.95 (`preset_middle`), their d from -0.08 (`equal_weight`) to
-1.13.

Checks (M6; 1,000 draws per cell, 400 at 98 years, not the card's 2,000): with Student-t(4) shocks the Monte Carlo SD of d is 1.02-1.19 times the formula
(fatter tails, shorter samples: more); the store's own k is 1.08 (median). Detection at the
formula's MDE80 came out 76-81%. So the tables are roughly right and, if anything, slightly
kind.

What the store also shows (descriptive, not candidates): the largest edges over the same
universe's `tsmom12` among logged tries are +0.30 (z 3.3, plain holding beats trend on a euro
S&P 500 fund 2012-2025), +0.71 (z 2.9, `halving-2` on Litecoin) and +0.19 (z 1.6,
`fomc-cycle`). None near z 4.69: these largest-d series have z from 0.2 to 3.3.

### Ranked recommendation for future lanes

1. **Accept the "risk choice" framing as the end state for the six-asset book.** With the
   data we can get, no Sharpe edge of a size the literature and live funds support can pass
   z 4.69. Lanes that pick between risk levels, drawdowns and crash behaviour (the risk menu)
   answer questions the data can answer; Sharpe-edge searches on the six assets do not.
   Stop new C1 and C4 edge searches on the six assets: chance to pass below 1 in 5,000 each.
2. **If an edge search continues at all: pool long history, pre-register, and use the alpha
   form.** The only places where the bar comes within reach of plausible sizes are pooled
   13-market trend tests (Y_eff about 191: edge +0.18 needed against at most +0.10 plausible,
   about a 2% chance) and long-short style tests on about 100 years under an alpha
   comparator (IR 0.51-0.60 needed; live style premia 0.50). Both answer "does this work
   across markets", not "is it better on our six", and the second needs shorts (B7). The
   comparator is the lead's call: the alpha form does not lower z, it stops asking an
   uncorrelated overlay for a standalone Sharpe of 2.3.
3. **High-frequency crypto: only as a cost study first.** The bar needs a net 40 bps a day
   (daily bets) or a net 1.9 bps an hour after 10-30 bps of costs; whether any keyless
   strategy has that is unknown, and the project's coin lanes found nothing. A lane here
   should first measure the realistic cost per round trip on a paper venue; if costs are
   above about 10 bps, hourly bets cannot pass.
4. **Event studies: run only with a power check first.** Before a card, compute the per-event
   Sharpe needed (table M3). A design with 254 independent events (FOMC days since 1994)
   needs a per-event Sharpe of 0.37, one with 200 needs 0.42, and 18-20 episodes need more
   than 1.3 (kill-only); that matches gate-power's partial result.
   A rule for cards: if a true effect at the top of the plausible range has under 5% chance
   to pass, label the test kill-only or skip it.
5. **Perp carry: closed** (blocked by B6/B7, 6 years of funding, needs an alpha IR of 2.4).
6. **Forward scoring: keep it, for what it can do.** It checks the implementation and
   describes risk; it cannot rank the books by edge within decades. Do not read the
   scoreboard order as evidence of edge, and do not spend held-out data on forward
   "confirmation" of edges below +0.30.

### Limits

- rho for 1-minute crypto (0.1) and perp carry (0.2) is assumed; the store holds no such
  series. The plausible ranges are judgments from the records named in the table; where the
  records say nothing, the table says unknown.
- Y_eff for 13 markets uses the cross-market correlation of difference series measured on
  four markets (FTSE, DAX, S&P 500, Nikkei; 19 rules, 110 pairs); the other nine may correlate
  more. It also assumes the same rule and the same edge in every market.
- The bootstrap SE uses 52-week blocks; slow rules whose difference returns persist for years
  would need longer blocks and would make k larger, so the edges needed would be larger.
- Event-count rows assume independent events; overlapping windows reduce them further.

Tries rows: one `note` row (`power-map`), no selectable try.
