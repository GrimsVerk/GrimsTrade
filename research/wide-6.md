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

### What came out (one run, 2026-11-18; table `results/critical-slowing.md`)

**The gate fails for both indicators. `critical-slowing` is dead by the gate: no card, no
strategy, no `tries.md` row.**

Linear probability of a top-decile forward drawdown (base rate 0.10), slope per unit of
Kendall tau, Driscoll-Kraay t, with the two volatility controls:

| Period | obs | tauAC1 slope (t) | tauVAR slope (t) | log sd21 (t) |
|---|---:|---:|---:|---:|
| In-sample (to 2015) | 3,038 | +0.039 (1.44) | -0.019 (-0.53) | +0.195 (3.81) |
| Post-sample (2016 on) | 2,887 | +0.003 (0.12) | +0.040 (1.82) | +0.038 (0.97) |

- **AC1 does not rise before large drawdowns**, in our six assets or in the S&P 500 index
  over 1962-2015 (-0.025, t -0.8). A tau of +1 (a full year of steadily rising AC1) would add
  4 points to a 10% chance in-sample and nothing after 2015. As the papers found.
- **Rising variance carries no information beyond the level of volatility.** Without the
  controls it has a raw effect (S&P 500 1962-2015 t 2.6; six assets after 2016 t 2.1; in-sample
  t 1.2). With last month's volatility in the regression, it drops to t -0.5 in-sample and 1.8
  after 2016. The one predictor that works is plain recent volatility (t 3.8 in-sample), which
  `tsmom12`'s siblings `vol-target` and `trend-vol` already use. This is the survey's "reduces
  to volatility targeting", now measured.
- Per asset nothing reaches the bar: the largest cells are TLT's tauVAR after 2016 (+0.15,
  t 2.1, against -0.01 before) and QQQ's tauAC1 in-sample (t 1.9, then 1.2), out of 22 cells.
  The Guttal-style variant (log price minus its trailing 25-bar mean) gives the same picture
  (tauAC1 t 1.1 and 0.2). The continuous drawdown target likewise (all |t| < 1.9).
- **Compared with my guess:** AC1 near zero with |t| < 1.5: yes (1.4, 0.1). Variance positive
  raw and near zero with controls: yes. 3% chance of a pass: no pass.

Disclosures: one dry run (`DRY=1`) printed only sample counts per asset and period. The first
full run crashed before any statistic (a NaN at bar 0 poisoned the rolling sums of the
volatility controls); the fix (bar 0 return set to 0, the detrended series' first 24 values
set to 0, none inside any window used) was checked by counting non-finite values, then run.
The fix was meant to be pushed before the run; a lint error stopped that commit and the run
went ahead, so the fix is in the commit after the run. The code that ran is the code pushed
there (the only later change is a ruff-required ternary). Family count unchanged by a gate:
63 mechanisms, 16 tested (W11 makes it 64; see the count at the end).

## Step 2. W3 `lunar`: the same gate

### Literature check

- **Yuan, Zheng, Zhu (2006)**, "Are investors moonstruck? Lunar phases and stock returns",
  Journal of Empirical Finance 13(1), pp. 1-23, DOI 10.1016/j.jempfin.2005.06.001 (Crossref).
  `[pages read]` pp. 1-14 of the authors' accepted version
  (<https://personal.lse.ac.uk/yuan/papers/lunar.pdf>).
  - 48 countries, January 1973 to July 2001 (Datastream). A full-moon period is the full-moon
    day plus N days either side (N = 7: the 15-day window; N = 3: the 7-day window); new-moon
    periods likewise.
  - Equal-weighted global portfolio: new-moon minus full-moon periods 40.3 bps per lunar cycle
    (15-day window) and 27.5 bps (7-day), both significant at 5%; value-weighted 30.4 bps
    (10%) and 25.9 bps (5%): 3% to 5% a year. Daily differences 2.8 to 4.9 bps. Pooled over
    countries: about 4 bps a day (15-day window); larger in emerging markets (11.3 bps on the
    7-day window), **2.4 bps a day for the G-7** (both windows). In the US stronger for NASDAQ
    and small stocks.
  - No difference in volatility or volume; not explained by macro announcements or other
    calendar effects. The cause offered is mood.
- **Dichev and Janes (2003)**, "Lunar cycle effects in stock returns", Journal of Private
  Equity 6(4), pp. 8-29, DOI 10.3905/jpe.2003.320053 (Crossref; working paper SSRN 281665,
  2001). `[search summary, unverified]` (the SSRN page refused the fetch): returns in the 15
  days around new moons about double those around full moons, for all major US indexes over
  about 100 years and nearly all major indexes of 24 other countries over about 30 years; no
  effect in volatility or volume.

Post-sample years: Yuan et al.'s data end in 2001-07; the journal version appeared in 2006.
The gate window is **2007-01 to the end of train (2025-11-10)**, as `next-steps.md` proposed.

**Power, written before any number.** SPY's daily standard deviation since 2007 is about
1.2%; with about 2,300 trading days in each of the two periods, the standard error of the
difference is about 3.5 bps a day. The published G-7 size (2.4 bps) would show up at t of
about 0.7; the gate's t >= 2 needs about 7 bps a day, three times the published size for big
markets. So a failed gate cannot say the effect is gone; it can only say it is not large. For
this book that is the question that matters: an idle-cash overlay on half the days at 2.4
bps a day is a few hundredths of Sharpe.

### Decision rule (fixed and pushed before any number)

**Gate statistic.** SPY's dividend-adjusted close-to-close daily log return, mean over
trading days in new-moon periods minus mean over trading days in full-moon periods, 15-day
window (Yuan et al.'s N = 7; a day belongs to the period of the nearer of the two phases
within 7 calendar days, UTC dates), Welch t. Phases from the mean lunation (29.530589 days
from the new moon of 2000-01-06 18:14 UTC; off the true phase by up to about a day, which
moves a window edge by at most one day).

**Gate window.** 2007-01-01 to 2025-11-10 (train's last bar). No later bar is read.

**Rule.** Pass only if the difference is positive with t >= 2 **and** the true phase ranks in
the top 3 of the 29 phase shifts (the event dates moved by 0, 1, ..., 28 days; the same
statistic for each). On a pass, a card (idle cash into SPY and QQQ in new-moon periods, the
weekly harness, rows in `tries.md`, family bar). Otherwise W3 is dead by the gate, with no
card and no row.

**Shown, not gating.** The same statistic for the S&P 500 index (GSPC, no dividends) in
1962-1972 (before the paper's sample), 1973 to 2001-07 (its sample), 2001-08 to 2006
(after the sample, before the journal), 2007-2016 and 2017-2025; SPY in 1993 to 2001-07;
QQQ, N225, FTSE, GDAXI and BTC in the gate window; the 7-day window (N = 3) for SPY and GSPC.

**My guess before any number.** SPY gate difference between -3 and +4 bps, |t| < 1.2; the
paper's own years on GSPC positive at about t 1 to 2 (the US is a G-7 market). Chance of a
pass: 2%.

### What came out (one run, 2026-11-18; table `results/lunar.md`)

**The gate fails: SPY new-moon minus full-moon days +1.6 bps a day (t 0.43) over 2007-2025,
rank 12 of 29 phase shifts. W3 `lunar` is dead by the gate: no card, no strategy, no
`tries.md` row.**

| Series, years | New minus full, bps a day (t) | Rank of 29 |
|---|---:|---:|
| SPY 2007-01..2025-11 (gate) | +1.6 (0.43) | 12 |
| S&P 500 index 1973..2001-07 (paper's years) | +3.1 (1.28) | 5 |
| SPY 1993..2001-07 (paper's years) | +7.3 (1.54) | 3 |
| S&P 500 index 1962-1972 (before) | +0.7 (0.28) | 9 |
| S&P 500 index 2001-08..2006 (after sample, before journal) | -2.4 (-0.43) | 22 |
| S&P 500 index 2007-2016 / 2017-2025 | +2.5 (0.46) / +0.4 (0.07) | 11 / 14 |
| QQQ, N225, FTSE, GDAXI 2007-2025 | +0.5 to +2.5 (0.1 to 0.6) | 10 to 14 |
| BTC 2014-2025 | +10.3 (0.92) | 1 |

- In the paper's own years the US shows the paper's sign at the paper's size for a G-7
  market (+3 bps, t 1.3) and SPY a larger one (+7 bps, t 1.5, rank 3). After publication
  every stock series stays positive but small (+0.4 to +2.7 bps, all t below 0.6, ranks in
  the middle of the 29 shifts). The true phase is not special among the shifts: the largest
  shifted differences are 6 to 8 bps, at event dates moved by 19 to 25 days.
- BTC ranks first of 29 with +10 bps a day, t 0.9: one coin, one series, not the gate, and
  a coin's daily noise makes 10 bps a coin toss.
- Read as power, not proof of absence: the gate could only see about 7 bps a day. What it
  rules out is an effect large enough to pay in this book; a 1-2 bps a day mood tilt may be
  there and would be worth a few hundredths of Sharpe as an idle-cash overlay.
- **Compared with my guess:** SPY between -3 and +4 bps with |t| < 1.2: yes (+1.6, 0.43).
  Paper's years on GSPC positive at t 1 to 2: yes (1.28). 2% chance of a pass: no pass.

Disclosures: one dry run (`DRY=1`) printed only the gate's day counts (4,745 days: 2,342 new,
2,328 full, 75 in neither); a second check printed only each shown series' first and last
day and day count. Then one run. Index series carry no dividends (immaterial for a
difference of two daily means).
