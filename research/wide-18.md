# Wide 18: physics, signal processing, control, information theory and network science for `tsmom12`

Research run wide-18, 2026-11-24 (night lane of the WIDER line). Branch `wide-18` (from `main`),
PR into `main`. Research only: fake money, the price cache on disk, no change to the gym, the
daily runner or the live strategies. Train only: every run here ends on 2025-10-31 (the lane's
cut, stricter than the protocol's 2025-11-09); the held-out year is unread. A sister lane
(wide-17) takes biology, ecology and epidemiology; this one stays out of those fields.

Question: do methods from physics, signal processing, control theory, information theory or
network science give a better trend estimate, a regime or crash timer, or a sizing rule for the
live `tsmom12` (or predict the six assets' returns)?

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-24 20:01): **3,855 tries,
N 1,083; measured rho 0.54 gives N_eff 500: a new rule needs z >= 4.70 against `tsmom12` on the
primary test (edge +0.31 for a close rule, SE 0.065; +0.56 for a far one, SE 0.12); Bonferroni
p <= 1.0e-4.** At the ONC end of the count (11 trials) it would be z >= 3.25.

## Step 1. Candidates, checked against the record (written before any number)

Records read: `ideas.md` (all tables), `tries.md` idea list, `SUMMARY.md`, `wide-15.md`,
`wide-16.md`, `multi-signal.md`, `trend-tune.md`, `pooled-1.md` (`e4`), `fast-reentry.md`
(`or3-12`, `arm3-12`), `bear-legs.md`. "Closest try" names the record a candidate would mostly
repeat; "corr" is the expected correlation of its daily returns with `tsmom12` (a guess before
any run: high correlation means a small paired SE, so a reachable bar in Sharpe units, but also
little room for a gain). Most candidates are filters on the same price path, so most are
`tsmom12` with a different weighting of the past.

| # | Candidate | Field (source) | Why it should work | Why it probably won't | Closest try | Corr | Verdict |
|---:|---|---|---|---|---|---:|---|
| P1 | **`vclock12`: trend measured in intrinsic (variance) time.** The lookback is not 12 calendar months but the stretch of recent bars that holds one median year of the asset's variance: short in turbulent markets, long in calm ones | Physics: subordinated Brownian motion and trading time (Mandelbrot and Taylor 1967; Clark 1973); intrinsic-time event clocks (Glattfelder, Dupuis, Olsen 2011) `[memory]` | If regimes turn over per unit of information (variance), not per calendar day, a calendar window is too long after a crash (the rule's known leak: it buys back about seven months late, `trend-tune`) and too short in a slow calm top. The variance clock shortens the window exactly when the market is moving fast | A shorter window in high volatility is a fast re-entry rule by another name, and `or3-12` / `arm3-12` failed because bear-market rallies are high-volatility too (`bear-legs`: 74% of falls hold a 10% rally before the low). The longer window in calm markets makes exits later at calm tops (2007), which costs insurance | `fast-reentry` (`or3-12`), `wf-asset`, trend-tune surface (6-12 months a plateau) | 0.85-0.92 | **Test** (pick 1) |
| S1 | **`huber52`: a robust trend estimate.** Sign of a Huber M-estimate (one-step, clipped at 1.345 robust sd around the median) of the last 52 weekly log returns, instead of the plain sum | Signal processing / robust statistics: limiters and M-estimators for impulsive noise (Huber 1964) `[memory]` | Weekly returns have excess kurtosis near 9 (`BAR.md` shape table); the plain mean is an inefficient drift estimate under fat tails, and one jump (a covid rebound week, a coin pump) can flip `tsmom12`. A clipped mean has lower variance, so fewer false flips | The sign of the drift, not its size, is what `tsmom12` uses, and over a year the sign is rarely decided by one week; where it is, the jump may be the information (a crash *is* the trend). Clipping also biases: up for negatively skewed stocks (stay in longer in a crash), down for positively skewed coins (more cash in coin runs) | `tsmom12` itself; `fracdiff-momentum` (another weighting, dead) | 0.90-0.97 | **Test** (pick 2) |
| S2 | `hann12`: a tapered (Hann-window) FIR trend filter instead of the box that a 12-month return is | Signal processing: window design, sidelobe leakage (Harris 1978); trend rules as weighted returns (Levine and Pedersen 2016) `[memory]` | A box filter's sidelobes pass fast wiggles, which become whipsaws; a taper suppresses them | The triangular taper is the moving-average rule already (`sma200`: 1.01 vs 1.05), and `e4` is a stepped taper; the trend-tune surface is flat across shapes | `sma200`, `ensemble-tsmom` / `e4`, trend-tune | 0.9 | **Kill**: tested in other words |
| S3 | `kalman-llt`: slope of a local-linear-trend Kalman filter with the gain set by the measured signal-to-noise per asset | Signal processing / estimation (Kalman 1960; Harvey 1989) `[memory]` | The optimal linear trend estimate if the model holds; the gain adapts per asset | Steady state is a double exponential average whose length is set by q/r per asset: a per-asset lookback, which walk-forward tuning already failed (`wf-asset` -0.04) | `wf-asset`, `wf-shrunk`, trend-tune | 0.9 | **Kill**: per-asset lookback, tested |
| S4 | `cusum-exit`: Page's CUSUM / Wald's SPRT on returns to detect a drift change and exit early | Signal processing / sequential detection (Page 1954; Wald 1945) `[memory]` | Fastest detector of a mean shift for a given false-alarm rate | A faster exit trades insurance for whipsaw; `changepoint-momentum` (literature, gone above 2 bps), `stop-0.25` and `fade-28` (coin-fast-exit) and `drawdown-control` all tested this trade | `changepoint-momentum`, `coin-fast-exit`, `drawdown-control` | 0.85 | **Kill**: tested |
| C1 | `pd-trend`: derivative action (PD control): exit when the 12-month return is positive but has fallen by more than x vol over three months | Control theory (PID) | A rising error signal is caught before it crosses zero | Momentum of momentum is a blend of a fast and a slow lookback (`turning-points`, `e4`), and `fast-reentry` is the same blend on the way back | `turning-points`, `e4`, `fast-reentry` | 0.9 | **Kill**: tested in other words |
| C2 | `gain-schedule`: a lookback scheduled on the volatility regime (short when volatility is high) | Control theory (gain scheduling) | Same reason as P1 | It is P1 without the principle (a hand-set map from volatility to lookback, two free constants) | P1 | 0.9 | **Merged into P1** |
| I1 | `perm-entropy`: trust the trend only while the permutation entropy (or Lempel-Ziv complexity) of the weekly sign sequence is low | Information theory (Bandt and Pompe 2002; Lempel and Ziv 1976) `[memory]` | Low entropy = a predictable stretch, where a trend rule should pay | `hurst-entropy-gate` was parked for this reason (time-varying efficiency documented, not exploitable; about five independent readings in ten years); with 52 weekly signs the entropy estimate is noise | `hurst-entropy-gate`, `hmm-regime` | 0.8 | **Kill**: parked record |
| I2 | `ib-soft`: soft position = P(drift > 0 given the 12-month t-statistic), the rate-distortion answer to quantising a noisy signal to on/off | Information theory (rate-distortion, information bottleneck) | On/off throws away how sure the signal is | A soft slot is `kelly-shrunk` (posterior-proportional = inverse-vol), `ml-sizing` (worse) and wide-16's B2 | `kelly-shrunk`, `ml-sizing`, `ensemble-tsmom` | 0.9 | **Kill**: tested |
| N1 | `mst-length`: length of the correlation network's minimum spanning tree (it shrinks in crashes) as a risk-off trigger | Network science / econophysics (Mantegna 1999; Onnela et al. 2003) `[memory]` | Networks tighten before and in crashes | With six assets the tree has five edges and is the mean correlation; `absorption-ratio` (dead) and `turbulence`'s correlation part (dead, misses crashes) tested that signal | `absorption-ratio`, `turbulence` | 0.7 | **Kill**: tested |
| N2 | `spillover`: Diebold-Yilmaz connectedness (VAR variance decomposition) as a regime signal | Network science / econometrics (Diebold and Yilmaz 2012; Billio et al. 2012) `[memory]` | Connectedness rises in crises | Same signal as N1 plus a lead-lag part that hits the non-synchronous closes of coins and ETFs (`transfer-entropy` killed for this) | `absorption-ratio`, `transfer-entropy` | 0.7 | **Kill**: tested |
| N3 | `centrality-tilt`: weight in-trend slots toward the network's peripheral assets (low eigenvector centrality earns more) | Network science (Pozzi, Di Matteo, Aste 2013) `[memory]` | Peripheral assets diversify; the paper finds they earn more per unit of risk | With six assets centrality is the loading on the first principal component, i.e. beta: `multi-signal`'s BAB had the wrong sign here (IC -0.055) | `multi-signal` BAB, `where-rp` | 0.8 | **Kill**: tested, wrong sign |
| P2 | `tail-index`: a falling Hill tail exponent as a crash warning | Econophysics (Lux 1996; Gabaix et al. 2003) `[memory]` | Fatter tails before a crash | Like rising variance, it is mostly the level of volatility (`critical-slowing`: recent volatility the only predictor); a Hill estimate on a year of daily data has a standard error near a third of itself | `critical-slowing`, `turbulence` | 0.8 | **Kill**: volatility in disguise |
| P3 | `irreversibility`: time-reversal asymmetry (past trends predict future volatility, the Zumbach effect) for sizing | Statistical physics (Zumbach 2009) `[memory]` | A measurable arrow of time in returns | It forecasts volatility, not return: any use for sizing is a volatility target (`own-vol-target`, risk-menu) | `own-vol-target`, `vol-target` | 0.9 | **Kill**: a volatility target |

`[memory]`: cited from memory, not re-read for this run.

**What survives.** Of 14 candidates (12 distinct after merging C2 into P1), 10 are tested
records in other words: smoother or tapered filters, per-asset lookbacks, faster exits,
momentum of momentum, soft slots, correlation-network regime signals and volatility forecasts.
The two that survive (P1, S1) change only how `tsmom12` reads the past year, not what it holds
or when it decides, so both are close rules with small paired SEs, which is the only design
where the bar is reachable (wide-16, `power-map-1`). Both are expected to fail.

## Step 2. The test (card `cards/wide-18.md`, pushed before any number)

See the card. Two variants, both against `tsmom12` on the primary test, both cash conventions;
out-of-universe signs on the 8 ETFs and the four price indexes.

Order: candidates and card 7890c6d (23:29 UTC; the card says "about 23:45", a slip: it was
written about 23:28), script and tests 030543d (23:31), one dry run (last 120 days, nothing
logged, plumbing only), then the one real run (23:31).

## Step 3. Result (one real run, 2026-11-24 23:31 UTC): both fail; neither is even ahead

Tables: [`results/wide-18.md`](results/wide-18.md) (`uv run --with numpy python
research/lib/wide18.py`).

| Primary test, 1994-02-01 .. 2025-10-31 | Sharpe | dSharpe vs `tsmom12` | Paired SE | z | corr | Edge it needed (4.70 SE) | Max DD | Slot flips/yr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 1.044 | - | - | - | - | - | 37.4% | 7.2 |
| `vclock12` | 0.878 | -0.167 | 0.076 | **-2.18** | 0.92 | +0.36 | 48.3% | 9.6 |
| `vclock12`, above bills | 0.765 | -0.166 | 0.076 | -2.18 | | | | |
| `huber52` | 1.044 | -0.001 | 0.038 | **-0.01** | 0.97 | +0.18 | 40.1% | 8.8 |
| `huber52`, above bills | 0.931 | -0.000 | 0.038 | -0.00 | | | | |

| Out of universe (signs) | `vclock12` dSharpe (z) | `huber52` dSharpe (z) |
|---|---:|---:|
| 8 ETFs, 2001-2025 | -0.036 (-0.37) | -0.037 (-0.46) |
| 4 price indexes, 1962-2025 | -0.043 (-0.61) | -0.103 (-1.84) |

**Verdict: both fail the card's bar** (z >= 4.70 in both cash conventions and positive on both
other sets): both are behind or level on every set. Nothing goes to the paper book.

- **`vclock12` is worse, and worst where it was meant to help.** Era differences on the six:
  1994-99 -0.33, 2000-09 +0.15, 2010-16 -0.18, 2017-21 -0.16, 2022-25 -0.61. It helped only in
  the slow 2000s bear markets and on the indexes before 1994 (+0.16, +0.09), and lost the 2022
  fall (the window was long after calm years, so the exit came late) and both the 1990s and
  2010s bull runs (more flips: 9.6 a year against 7.2). Post hoc (`lib/wide18_posthoc.py`, not
  a try): the variance of coins, QQQ and gold fell over the record, so the expanding "median
  year" was a loud year and their windows sat above a year most of the time (median 1.22-1.30
  years; at the two-year cap 10-24% of Fridays); on SPY and TLT the median window was 0.92-0.94
  years. The physical premise (regimes turn over per unit of variance) needs a stationary
  variance scale, and these assets do not have one. A rolling reference would fix that and add
  a free parameter; it was not run.
- **`huber52` is `tsmom12`**: correlation 0.97, the same Sharpe to three decimals on the six,
  slightly worse worst loss (40% vs 37%) and more flips (8.8 vs 7.2). On the indexes it is
  clearly worse (-0.10, z -1.84): clipping the big weeks keeps the rule in through crashes
  that come as a few large down weeks. The jumps are part of the trend, not noise around it.
- **The power statement held**: both |z| stayed within 2.2 and both were expected fails. The
  close rule (`huber52`, corr 0.97) has an SE of 0.038, so the bar in Sharpe units was +0.18:
  lower than the BAR.md close-rule figure (+0.31), still far above anything a re-weighting of
  the same year has shown (trend-tune: best of 98 settings +0.08).

## What this says about the fields

- **Most ideas from these fields are filters on the same price path** and so map onto tested
  records: 10 of 12 distinct candidates were killed in step 1 without a run. The two that were
  new (a variance clock, a robust estimator) changed how the year is read, not what is held,
  and neither helped. Network ideas need breadth the six do not have (a six-node network is
  its mean correlation).
- **Physics' clock change needs a stationary scale.** If a later lane wants the variance clock,
  the honest next form is a rolling reference (e.g. the median year of the last ten), carded
  fresh, and judged on the pooled 41 markets (pooled-1's design), not the six.

## Count

This run adds **2 mechanisms tested by a strategy (`vclock12`, `huber52`; 2 variants, 6
robustness rows) and 12 killed as overlaps (note rows in `tries.md`, not counted as tries,
as wide-16 did), none passed**. On wide-16's count: 90 mechanisms, 21 strategy tests, 22
gates, none passed (not counting wide-17's, which runs in parallel).
