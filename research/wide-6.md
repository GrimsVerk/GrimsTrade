# Wide 6: two event-study gates (critical slowing down, lunar) and four new mechanisms

Research run wide-6, 2026-11-18. Branch `wide-6` (from `wide-5`), draft PR into `wide-5`.
Research only: fake money, public data, no change to the gym, the daily runner or the live
strategies.

Method, taken from ann-1: a cheap **event-study gate** first (does the raw effect exist in
our data, in the years its literature used and in the years after?). Only a gate that passes
gets a card and a train test. A gate is descriptive: like ann-1's, it gets no `tries.md` row
and does not count as a tested mechanism, so a failure does not spend the family's bar.

## Family count (corrected before anything else)

wide-5 counts 56 mechanisms, 14 tested; ann-1 counts 61, 14 tested. Both are right on their
own branch and both are short: the two lines forked at wide-4 (54 mechanisms, 12 tested).
survey-2 added 7 mechanisms and tested 1, survey-3 tested 1 more; wide-5 added 2 and tested 2.
The union is **63 mechanisms (54 + 7 + 2), 16 tested, none passed**, and the next strategy
test is read at **p < 0.10 / 63 = 0.00159** (lower again once this run adds its own). This run
uses the union.

## Step 1. Critical slowing down (W11 `critical-slowing`)

### The idea, from ecology and physics

Near a tipping point (a fold bifurcation) a system recovers ever more slowly from small
shocks. In a time series that shows as rising lag-1 autocorrelation (AC1) and rising variance
before the shift. Scheffer et al. (2009) set this out as a generic early-warning signal for
lakes, climate, fisheries and also, as a hope, markets. If a market crash were such a
transition, rising AC1 and variance in daily returns would warn of it, and a `tsmom12` slot
could be left before the trend rule leaves it.

Our survey (`survey-2026-11.md`, part 6) already read this literature and marked the idea
"dead (literature)" in `ideas.md`: rising AC1 is rejected, rising variance "reduces to
volatility targeting". That was never checked on our own assets. This gate checks it, and asks
the one question that matters for us: **does a rise in AC1 or variance say anything about a
coming large drawdown beyond what the current level of volatility already says?**

### Literature check

Tags as in ann-1: `[pages read]`, `[page read]`, `[abstract]`, `[page read: model summary]` =
the full text was fetched and read through a summarising tool, numbers quoted from that
summary; `[record]` = bibliographic record only (Crossref).

- **Scheffer, Bascompte, Brock, Brovkin, Carpenter, Dakos, Held, van Nes, Rietkerk, Sugihara
  (2009)**, "Early-warning signals for critical transitions", Nature 461(7260), pp. 53-59, DOI
  10.1038/nature08227. `[record]` (Crossref; the survey read the abstract via Europe PMC). The
  generic signals: slower recovery, rising AC1, rising variance, skewness, flickering.
- **Dakos et al. (2012)**, "Methods for detecting early warnings of critical transitions in
  time series illustrated using simulated ecological data", PLoS ONE 7(7), e41010, DOI
  10.1371/journal.pone.0041010. `[record]` The standard recipe: a rolling window (often half
  the series), the indicator's trend measured by Kendall's tau.
- **Guttal, Raghavendra, Goel, Hoarau (2016)**, "Lack of critical slowing down suggests that
  financial meltdowns are not critical transitions, yet rising variability could signal
  systemic risk", PLoS ONE 11(1), e0144198, DOI 10.1371/journal.pone.0144198. `[page read:
  model summary]`
  - Dow Jones (about 115 years: crashes 1929, 1987, 2000, 2008), S&P 500 and NASDAQ (1987,
    2000, 2008), DAX and FTSE (2000, 2008). Detrended log prices (Gaussian kernel, bandwidth
    25), rolling window 500 days, Kendall tau over the last 250 days before each crash; AC1,
    variance, low-frequency power; three null models with 1,000 surrogates each; over 1.25
    million parameter combinations scanned.
  - AC1: no or weak trends before any crash (never above tau 0.9 for the Dow); trends no
    larger than in the surrogates. Variance and low-frequency power: strong rises before all
    crashes; on the Dow, 16 strong variance/power signals in 115 years: 5 before the four
    major crashes, 4 before minor crises, 7 false alarms.
  - Out of sample in the paper itself (2011-09 to 2015-09): no significant trends in the Dow,
    S&P 500 or FTSE; strong rises in NASDAQ and DAX ("mixed early warning signals").
  - Not done in the paper: a test of whether rising variance adds anything to the level of
    volatility. The authors note variance of detrended prices and return volatility can
    disagree.
- **Diks, Hommes, Wang (2019)**, "Critical slowing down as an early warning signal for
  financial crises?", Empirical Economics 57(4), pp. 1201-1228, DOI
  10.1007/s00181-018-1527-3; working paper CeNDEF 15-04 (2015). `[abstract]` (EconPapers
  record; the full text linked by the survey now returns 404). Four crises: 1987, the 1997
  Asian crisis, 2000, 2008. Evidence of slowing down before Black Monday 1987 only; mixed and
  not significant for the other three. Notes that financial series are near unit root.
- **Ismail et al. (2022)**, Frontiers in Applied Mathematics and Statistics, DOI
  10.3389/fams.2022.940133: read in full by the survey (persistent homology plus critical
  slowing down); not reread here.

What the record says before our numbers: AC1 does not rise before crashes (two independent
groups, one exception: 1987); variance does, with many false alarms, and nobody has shown it
adds to plain volatility. Post-sample years for the gate: **2016 on** (Guttal et al. published
2016-01 with data to 2015-09; Diks et al.'s crises end in 2008).

### Decision rule (fixed and pushed before any number)

Nothing below may change after the script's first run.

**Series.** The six live assets (SPY, QQQ, TLT, GLD, BTC, ETH), dividend-adjusted closes from
the research cache, train bars only (to 2025-11-10). Daily log returns r. Each asset on its
own clock: w = 252 bars for ETFs, 365 for coins (one year); horizon H = 63 bars for ETFs,
91 for coins (a quarter).

**Sample.** One observation per asset per Friday (the last bar on or before the Friday), once
the asset has 2w + 1 bars, and only while the full forward window (H bars) is inside train.

**Indicators at t** (bars up to t only):

- `ac1`: lag-1 autocorrelation of r over the last w bars, computed for every bar; **tauAC1**
  = Kendall's tau between time and the last w daily values of `ac1` (Dakos et al.'s trend
  measure; Guttal et al.'s 250-day trend window).
- `var`: variance of r over the last w bars; **tauVAR** = Kendall's tau of its last w daily
  values.
- Controls (plain volatility clustering): log of the standard deviation of r over the last
  21 bars, and over the last w bars.

**Target.** The forward maximum drawdown FDD(t): the largest fall in log close from a running
peak, over bars t .. t+H (the peak may be the close at t). **Large** = FDD at or above the
asset's 90th percentile of FDD over its sampled Fridays in train (an asset-relative cut, so
coins and bonds count alike). L(t) = 1 if large, else 0.

**Regression.** Linear probability, pooled over the six assets with an asset intercept each:

L = a(asset) + b1 tauAC1 + b2 tauVAR + c1 log sd21 + c2 log sdw + e

Standard errors: Driscoll-Kraay (the score summed over assets each Friday, then Newey-West
with Bartlett weights and 13 weekly lags, which covers the overlap of the 91-bar coin window).

**Periods.** In-sample: Fridays to 2015-12-31. Post-sample: Fridays from 2016-01-01 whose
forward window ends inside train.

**Gate.** For each indicator separately: b > 0 with t >= 2.24 (one-sided 1.25%: 2.5% split
over the two indicators) **in both periods**. If either indicator passes, a card is written
(a `tsmom12` overlay that leaves an in-trend slot while that indicator's tau is high), tested
on train with rows in `tries.md` and the family bar. If neither passes, `critical-slowing` is
recorded as dead by the gate: no card, no strategy, no `tries.md` row.

**Shown, not gating.** The same regression without the two volatility controls (the raw
effect); per asset, the slope on each tau alone with the controls (Newey-West t); the
continuous FDD target in place of L; the S&P 500 index (GSPC) alone for 1962-2015, the long
in-sample history of the papers; a literature-faithful variant whose AC1 and variance are
taken on the log price minus its trailing 25-bar mean (a causal stand-in for Guttal et al.'s
two-sided kernel detrending, which looks ahead) in place of returns.

**My guess before any number.** tauAC1: slope near zero, |t| < 1.5 in both periods (the
literature). tauVAR: positive without controls (rising variance means high variance now,
and volatility clusters), near zero or negative once the level of volatility is in, because
volatility also mean-reverts. Chance the gate passes: 3%.
