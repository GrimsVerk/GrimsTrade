# ownvol-anatomy-1: where does own-vol's lead (or loss) over `tsmom12` come from?

Lane `ownvol-anatomy-1`, written 2026-11-24 **before any number of this card is computed** (no
decomposition below has been run on any series; what had been seen: the published tables of
risk-menu-3 (#110), pooled-1 (#142) and pooled-2 (#159), and the sibling card
`cards/e4-anatomy-1.md`, whose regime definitions this card reuses). Before writing, one
plumbing call re-ran #110's six-asset book to check the data are in place: `vt-own 70% x`
1.035 against `tsmom12` 0.933 (#110 printed 1.036 / 0.937; the gap is later code in the bill
rate, not this lane). Research only: fake money, files already in the data cache (read-only),
no change to the gym, the daily runner, the live strategies or the `own_vol_70` paper book.
Train data only: the loaders of pooled-1, pooled-2 and risk-menu-3 stop at 2025-10-31; the
held-out year is untouched.

## What this is (and is not)

A **descriptive re-score** of finished tries, with their own code and series: no new rule,
own-vol is not retuned (target 0.70, 52-week / 36-month sigma, monthly reset, 24-sigma warm-up
all as frozen), nothing is selected, and it is not a new test of own-vol. The numbers explain the
D that pooled-1, pooled-2 and #110 already reported; they cannot make it significant. Logged as
one `note` row in `tries.md` (as gap-2002-1 did).

## Question

Own-vol targeting (`vt-own-70-x`: the `tsmom12` sleeve x min(1, k / sigma), k for a mean share
of 0.70) leads `tsmom12` by +0.10 Sharpe on the six (#110, one paired SE), by D = +0.022 a market
on 41 stock markets (pooled-1), and trails by -0.010 on 21 bond and currency series (pooled-2,
judged; currencies -0.052, driven by CAD, AUD, NZD, NOK), with +0.056 on 8 commodity spot series
(shown). **Where does that come from:** (a) volatility timing (less exposure in high-volatility
spells), split into a risk channel and a mean channel; (b) the average-exposure difference (is
the lead just holding less?); (c) which market regime; (d) why stocks and commodities gain but
currencies lose.

## Series and rules (unchanged)

- **Equity 41**: `pooled1.load_all()`, `pooled1_core.run_market` (weekly decisions, fill one
  session late, 2 bps a side, cash 0, own-vol reset cost 5 bps), weekly Sharpe (sqrt 52).
- **Non-equity 29**: `pooled2.load_nonequity()`, the costs, lags and engines of
  `pooled2.run_specs` (weekly engine with publication lags and sigma skip 1 on US bonds and 8
  currencies; monthly engine, 36-month sigma, on GOV9, FX-EUR, PPI and gold), excess over the
  bill, Sharpe at the series' frequency. Groups and pools as pooled-2: judged = USB3 + GOV9 +
  FX9 (21); COM8 shown apart. FX9 is also shown split into commodity currencies (CAD, AUD, NZD,
  NOK) and the other five (JPY, GBP, CHF, SEK, EUR).
- **The six**: risk-menu-3's book, `riskmenu3_run.vt_expanding(s1, 0.70, held)` against the
  `tsmom12` sleeve `s1`, window W = 1994-02-01..2025-10-31, daily excess returns over bills on
  calendar days, Sharpe with sqrt 365 (`stats.sharpe`). One series: decomposed, not pooled.
- **Reproduction check (must hold, else stop and report)**: this lane's per-series d equals
  pooled-1's and pooled-2's d for every series to 1e-9 (pools: equity +0.0217, judged -0.0100,
  COM8 +0.0560); the six's d equals the plumbing call above (1.035 - 0.933) to 1e-9.

Own-vol's share v_t on each session (period) is the share the book holds over that return: set
at the monthly reset, drifting in between, as in `own_vol` / `own_vol_weekly` /
`own_vol_monthly` / `riskmenu_run.mix`. This lane replays those loops to record v_t; a test
checks the replay gives the frozen code's returns exactly.

## The fixed-share twin (part b)

F: the same machinery as own-vol (monthly resets on the same days, drift in between, the same
reset cost per traded notional), but the reset share is always one number s_bar, own-vol's
average share **while `tsmom12` is invested**: s_bar = sum_t v_t g_t / sum_t g_t over the scored
sessions (g_t = `tsmom12`'s gross position, 0 or 1; on the six its gross exposure). So F holds
the market, on average, as much as own-vol does, at a constant share. s_bar uses the whole
sample: a descriptive twin, not a rule. Because Sharpe is scale-free with cash at 0 (equities) or
at the bill (excess returns), F's Sharpe equals `tsmom12`'s up to drift between resets and reset
costs: E (below) is expected to be about zero by construction. That is part of the answer to
(b), so it is reported, not assumed. Total growth, volatility and worst loss of `tsmom12`, F and
own-vol are shown per pool too (holding less matters there, not in Sharpe).

## Decomposition (exact identities, fixed now)

Per series, with period returns o (own-vol), f (F), s (`tsmom12`) of the scored span, T periods,
means mu and population standard deviations sd (ddof 0, as pooled-1/2's Sharpe) at the period
frequency, annualised by sqrt(P) (P = 52, 12, or 365 on the six):

    d = SR_o - SR_s = E + M + R
    E = SR_f - SR_s                                   exposure (holding less, at a fixed share)
    M = (mu_o - mu_f) / sd_o * sqrt(P)                timing, mean channel
    R = mu_f * (1 / sd_o - 1 / sd_f) * sqrt(P)        timing, risk channel

- **M, the mean channel**: own-vol earns more (M > 0) or less than the same average share held
  fixed. M > 0 means the sleeve earns less per unit of exposure when own-vol holds little (high
  recent volatility) than when it holds much: the leverage / volatility-feedback effect. M < 0
  means high-volatility spells are the ones that pay (rebounds, early trends) and own-vol misses
  them.
- **R, the risk channel**: own-vol's swings are smaller (R > 0, if mu_f > 0) than the fixed
  twin's at the same mean: cutting exposure when volatility is high removes more variance than
  return. It is positive when volatility clusters (recent volatility predicts the next month's).
- **Timing = M + R.**
- **Split by period, exactly**: every term is a sum of one term per period,
  E = sum_t e_t (with e_t = (f_t - s_t) / (T sd_f) sqrt(P) - SR_s [(f_t - mu_f)^2 -
  (s_t - mu_s)^2] / (T sd_f (sd_f + sd_s))), M = sum_t (o_t - f_t) / (T sd_o) sqrt(P),
  R = sum_t -SR_f [(o_t - mu_o)^2 - (f_t - mu_f)^2] / (T sd_o (sd_o + sd_f)), so any partition
  of the periods splits E, M and R exactly. Pool numbers are equal-weight means over series, so
  they add up to the pool's D exactly.

## Partitions (each period gets one label in each)

1. **Regimes (part c), the sibling card's definitions** (`cards/e4-anatomy-1.md`, from insure-1
   and insure-2): labels on every session (month) of the series' own traded level (equities: the
   level pooled-1 trades; bonds and currencies: the excess-return level pooled-2 trades; monthly
   series: the cumulated monthly excess returns; the six: the equal-weight hold-the-six excess
   level `c.equal_weight`, as risk-menu-3 builds it), over the series' whole loaded history; a
   scored period takes the label of its last session.
   - **Fall**: zigzag 25% down / 25% up (`insure1.zigzag`, `PRIMARY`), sessions (peak, trough].
     **Fast crash**: trough - peak <= 92 days. **Slow bear**: > 92 days (medium 93-365 and long
     > 365 kept in the json). An unfinished fall at the end is calm.
   - **Rebound**: (trough, the earlier of trough + 365 days and the next peak].
   - **Whipsaw**: outside falls and rebounds, `tsmom12`'s position changes at least twice among
     the decisions within 13 weeks on either side (monthly: 3 months; the six: the book's
     gross exposure changes direction twice among the weekly decisions within 13 weeks).
   - **Calm**: everything else. Priority fall > rebound > whipsaw > calm.
   - Readings: **A** (primary) 25% / 25%; **B** down = up = 1.5 x the series' annualised
     volatility of its level (fairer for bonds and currencies, where 25% falls are rare); **C**
     insure-3's 15% / 15%.
2. **Volatility state (part a)**: own-vol's share on the period's first session. "Out": `tsmom12`
   holds nothing all period. "Warm-up": before the first sized reset (share = target). Otherwise
   terciles of the share among the series' own in-market, post-warm-up periods: **low share**
   (high recent volatility), **mid**, **high share** (calm, often capped at 1).
3. **Trend phase (part d)**: "entry": the first 26 weeks (6 months) after a `tsmom12` entry
   (position 0 -> 1); "held": other in-market periods; "out". This tests pooled-2's untested
   guess that on commodity currencies the sleeve is cut again just as the trend re-enters.

## Volatility and return by class (part d)

Per series, at its frequency (h = 4 weeks or 3 months):

- **Leverage correlation L**: the correlation of the traded level's period return r_t with the
  change in its realised volatility, RV(t+1..t+h) - RV(t-h+1..t), RV = sqrt(mean of squared
  period returns), over all periods of the scored span. L < 0: falls raise volatility (stocks);
  L > 0: rises raise it.
- **Sleeve mean and variance by share tercile**: the `tsmom12` sleeve's annualised mean and
  variance in the low- and high-share terciles. Own-vol's mean channel gains when mean / variance
  is higher in the high-share (calm) tercile than in the low-share one.
- **Volatility persistence**: the correlation of the sleeve's sigma at a reset (the one own-vol
  uses) with the sleeve's realised volatility over the next month, on in-market months. This is
  what the risk channel lives on.

Shown per group and pool as equal-weight means over series.

## Readings (fixed now)

- **(b)** "The lead is holding less" if |E| >= half of |D| in the pool; otherwise "not holding
  less".
- **(a)** A channel (M or R) "carries" the pool's D if it has D's sign, is at least half of |D|
  and is above 2 SE; "within noise" otherwise. Both, one, or neither are named.
- **(c)** A regime "carries" if its M + R term is above 2 SE and above half of |D|; otherwise the
  regime split is described, not called.
- **(d)** The gap D_equity - D_FX9 (and equity - judged 21, equity - COM8, shown) is split into
  the differences of E, M and R. "Currencies lose through the mean channel" if the M difference
  is at least half of the gap; "through the risk channel" if the R difference is; "mixed"
  otherwise. The regime and trend-phase rows of M say where.
- On the six, the same split with no SE (one series; #110's paired SE of the lead is about 0.1).

## Uncertainty (description, not a test)

SE of each pool-level term (E, M, R, and each label's share of them) from a joint circular
bootstrap of 12-month blocks on one monthly calendar (pooled-2's calendar, 2,000 draws, seed 0),
with each series' means and standard deviations held at their full-sample values (a
linearisation: it measures how much the split moves with the calendar, not a test of own-vol).
A series enters a draw only with at least 12 months of periods in it.

## Expectation, stated so it can be wrong

E about zero everywhere (|E| < 0.005). On stocks most of D is the risk channel (volatility
clusters, so cutting exposure in volatile spells removes risk), with a small or negative mean
channel: own-vol loses in rebounds and in the entry phase (the sigma still carries the crash)
and gains in slow bears it is still invested in. Fast crashes about zero (sigma lags the crash,
and `tsmom12` is often out by the time the share is cut). On currencies the risk channel is
small (weaker volatility clustering) and the mean channel negative, concentrated in the entry
phase and in the low-share tercile of the commodity currencies. Leverage correlation L negative
for stocks, near zero for currencies (positive for JPY and CHF).

## Output and rows

- `research/lib/ownvolanatomy_core.py` (decomposition, partitions, bootstrap; numpy only) and
  `research/lib/ownvolanatomy.py` (data, run) write `results/ownvol-anatomy-1.md` (+ `.json`);
  write-up `research/ownvol-anatomy-1.md`.
- Tests `tests/test_ownvolanatomy.py` (offline, synthetic series): the replayed share gives the
  frozen own-vol returns exactly; E + M + R = d exactly and the per-period terms add up to each
  term; labels cover every period once; a constant-share own-vol gives M = R = 0.
- One `tries.md` row of kind `note`, one `ideas.md` line. Bar for scale (BAR.md): z >= 4.70,
  N 500. Not applicable: no test, no pick.
