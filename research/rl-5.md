# RL 5: lasso on perp inputs screened by return spread

Research run rl-5, 2026-11-18. Branch `rl-5` (from `rl-4`). Research only: no strategy is
added to the paper system. No RL is trained in this run (rl-4: no RL variant passes the planted
gate); the learner is rl-4's gate-passing lasso, unchanged.

Question: rl-4 screened perp inputs by rank IC, and the input that won (`vol`, rank IC 0.10) paid
nothing in return. If inputs are screened by what a third-against-third book on them **earns**
(the weekly return spread), does any input survive a multiple-testing correction, and does the
fixed lasso on the survivors beat the funding carry book (`ls-funding`, pooled Sharpe 0.57)?

Words. **Spread**: the coming week's return of the top third of coins by an input minus the
bottom third. **Holm correction**: with N inputs tested, the smallest p-value must be below
0.10 / N, the next below 0.10 / (N - 1), and so on; it keeps the chance of one false pass in the
whole table at 10%. **Net**: after 10 bps a side on every change of weight; funding is already
inside the return.

## Card (written 2026-11-18 ~11:08 UTC, before any rl-5 code or number)

### What was already seen (disclosure)

All of rl-4 (`research/rl-4.md`), on this same data and these same years: gross spreads, sign
picked after the fact, no costs (`results/rl-4-perp-why.md`): `funding` +0.40% a week (t 2.1),
`premium` +0.40% (t 2.0), `mom_12_1` -0.09% (t -0.3), `vol` +0.05% (t 0.2). carry-2: `ls-funding`
pooled Sharpe 0.69 on its days, 0.57 on rl-4's days; `ls-premium` 0.44; both near zero at
30 bps. So four of the nine inputs below have been seen gross, and a t of 2.1 cannot pass a Holm
correction over nine (it needs about 2.5 at best). That is known now and is the point of the
correction: the screen is expected to be hard. The five new inputs have not been scored on these
sets. The held-out year (2025-11-11 .. 2026-11-09) has never been loaded for this and is not
touched in this run, whatever the result (carry-3 spent it for the carry band).

### Data, book, costs (rl-4 part 2 / carry-2, unchanged)

carry-2's three sets (Binance perps outside short-1's 30, Bybit, Hyperliquid), carry-2's tradable
rule, weekly decisions at Friday's close, **train years only: decisions to 2025-11-09**. Return
of a week = total return of a long position (price change minus funding paid), in plain percent.
Loaded through `rl4_perp.load()` unchanged.

### Candidate inputs (nine, fixed now)

All known at Friday's close, per coin. The first four are rl-4's.

1. `funding`: mean funding rate of the last 7 days.
2. `premium`: mean perp premium over spot of the last 7 days.
3. `mom_12_1`: log return from 365 to 30 days ago.
4. `vol`: log of the 30-day volatility of daily returns.
5. `rev_1w`: log return of the last 7 days (short-term reversal or continuation).
6. `mom_1m`: log return of the last 30 days.
7. `fund_30`: mean daily funding paid over the last 30 days (a slower carry).
8. `max_30`: the largest daily log return of the last 30 days (the "lottery" coins).
9. `log_qv`: log of the 30-day median daily dollar volume (size / liquidity).

### The screen (fixed now, run once)

For each input and each venue-week with at least 10 tradable coins that have the input: coins are
sorted by the input; the book is +0.5 of equity equal-weighted in the top third and -0.5 in the
bottom third (carry-2's book). Gross week = 0.5 x (mean return top third - mean return bottom
third). Cost = 10 bps x the sum of absolute weight changes against that venue's previous
decision (the first week pays for the whole book; drift inside the week is ignored). **Pooled
week** = the mean over the venues that have a book that Friday (equal capital per venue), so one
number per week.

- **Sign:** not set in advance. `s` = the sign of the mean pooled gross week over all train
  weeks. Net week = `s` x gross - cost.
- **Statistic:** t of the mean pooled net week (mean / standard error, plain, no autocorrelation
  correction). p = two-sided because the sign was picked from the same data: 2 x (1 - Phi(t)),
  and 1 if t <= 0.
- **Multiple testing:** Holm step-down over all nine p-values, family-wise level 0.10.
- **An input passes** if (a) it is rejected by Holm at 0.10 and (b) its mean net week, with the
  pooled sign `s`, is above 0 on at least two of the three venues.

Reported, not a bar: gross spread and its t, the annualised Sharpe of the pooled net weeks
(mean / sd x sqrt(52)), turnover, per-venue numbers, the unadjusted p.

This screen uses every train week at once, so anything it passes is selected in sample; a book
built on the survivors and judged on the same weeks is flattered. That is disclosed here and
again in the write-up; the only clean test would be a held-out year, which this run does not have.

### The learner (only if at least one input passes; run once)

`ls-ml5`: rl-4's `ls-ml-ret` exactly (lasso, penalty by purged CV on rl-4's grid with the 14-day
gap, yearly refits 2021-2025, first model at 1,000 rows, one model for all venues, inputs as
centred ranks, target the week's return as a z-score across the venue's coins, book = top third
long, bottom third short by forecast, 10 bps a side plus every funding event), on the passing
inputs only. The return target is used because rl-4 showed the book is paid in returns, not
ranks. If no input passes, nothing is trained and the answer is "no input clears the screen".

**Bars (pooled, 10 bps + funding, fixed now):**

1. Pooled Sharpe **above 0.57** (`ls-funding` on the same days; the number is recomputed in the
   same run and that one is used).
2. Sharpe difference to `ls-funding` above 0 with a paired stationary-bootstrap p < 0.10
   (rl-4's bar 2).
3. Sharpe above 0 on Binance-outside-30 and on at least one of Bybit and Hyperliquid.

A pass is a candidate for a later card, not a strategy, and is marked "selected in sample".

### Tries and code

One `screen` row per input in `tries.md` (idea `rl-5-screen`), although `screen` rows are not
strategy tries: the net pooled weeks are a small backtest, so they are counted in the open.
`ls-ml5`, if run: one `variant` row per set (idea `rl-5-perp-<set>`). Code
`research/lib/rl5_screen.py` (reuses `rl4_perp`), test `tests/test_rl5.py` on made-up data,
table `results/rl-5-screen.md`.
