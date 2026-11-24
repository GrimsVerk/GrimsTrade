# Wide 19: meteorology, actuarial science and operations research for `tsmom12`

Research run wide-19, 2026-11-24/25 (night lane of the WIDER line). Branch `wide-19` (from
`main`), PR into `main`. Research only: fake money, the price cache on disk, no change to the
gym, the daily runner or the live strategies. Train only: every run here ends on 2025-10-31 (the
lane's cut, stricter than the protocol's 2025-11-09); the held-out year is unread. Sister lanes
tonight: wide-17 (biology, ecology, epidemiology, climate) and wide-18 (physics, signal
processing, control, information theory, networks; PR #169). This lane stays out of their
fields.

Question: do methods from weather forecasting (ensembles, calibration and verification, model
output statistics, skill against persistence and climatology), actuarial science (credibility
theory, experience rating, reinsurance layers, ruin theory) or operations research (inventory
policies, optimal stopping, robust optimisation) tell `tsmom12` when to be in, how much to hold
or how to blend signals better, or improve the project's honest evaluation of it?

Project-wide bar (`research/register/BAR.md`, rows through 2026-11-24 20:01): **3,855 tries,
N 1,083; measured rho 0.54 gives N_eff 500: a new rule needs z >= 4.70 against `tsmom12` on the
primary test (edge +0.31 for a close rule, SE 0.065; +0.56 for a far one, SE 0.12); Bonferroni
p <= 1.0e-4.** At the ONC end of the count (11 trials) it would be z >= 3.25.

## Step 1. Candidates, checked against the record (written 2026-11-24 about 23:45 UTC, before any number)

Records read: `ideas.md` (all tables), the `tries.md` idea list, `SUMMARY.md`, `BAR.md`,
`wide-15.md`, `wide-16.md` (which already killed `s-S-inventory`, `cppi-floor` (ruin / floor),
`tranching`, `slew-limit`, `leaky-bucket` and `derating` as overlaps: not repeated here),
`wide-18.md` and its results (branch `origin/wide-18`), `multi-signal.md`, `trend-tune.md`,
`insure-2.md`, `insure-4.md`, `pooled-1.md` (`e4`), `fast-reentry.md`, `bear-legs.md`, and
wide-17's candidate table (branch `origin/wide-17`) to stay out of its fields. "Corr" is the
expected correlation of the rule's daily returns with `tsmom12` (a guess before any run; a high
correlation means a small paired SE and a reachable bar in Sharpe units, but little room for a
gain). Sources marked `[memory]` are cited from memory, not re-read for this run.

| # | Candidate | Field (source) | What it would change | Why it should work | Why it probably won't | Closest try | Corr | Verdict |
|---:|---|---|---|---|---|---|---:|---|
| M1 | `brier-verify`: score `tsmom12`'s in/out as a probability forecast of the next four weeks' sign; Brier skill score against climatology (always up) and persistence (last month's sign), Murphy's decomposition into reliability and resolution | Forecast verification (Brier 1950; Murphy 1973) `[memory]` | Evaluation only | A proper score says whether the signal has resolution (separates good from bad months) at all, apart from the Sharpe of a book | The weekly IC of `tsmom12`'s signal is already measured at +0.014 (`multi-signal`, info-1): resolution about zero by another name. The rule's value is in the tail (a fall avoided), which a sign score dilutes | `multi-signal` / info-1 IC; insure-1 (fall share avoided vs random timing) | n/a | **Kill**: measured in other words |
| M2 | `rev-costloss`: relative economic value (the static cost-loss model): for a user who pays C to protect against a loss L, value of the exit signal as a function of C/L, against random timing and against `sma200` | Forecast verification (Richardson 2000; Murphy 1977) `[memory]` | Evaluation only | Turns "crash insurance" into a curve: for which users (which C/L) is the trend exit worth its false alarms. The peak value is the Peirce skill score (hit rate minus false-alarm rate) | The ingredients (share of falls avoided, exposure, random-timing null) are insure-1/2's; a fixed loss L per event ignores the size of the fall, which insure-1 measures directly | insure-1, insure-2 | n/a | **New** (descriptive; a reframing of insure-1, not run tonight) |
| M3 | `mos-calibrate`: model output statistics: a walk-forward logistic map from the 12-month return (in risk units) to P(next month up), slot = calibrated probability | Weather post-processing (Glahn and Lowry 1972) `[memory]` | A soft slot | Raw model output is biased and overconfident; MOS fixes both | A calibrated probability is a soft slot: `kelly-shrunk` (= inverse-vol), `ml-linear` (AUC 0.49), `ml-sizing` (worse), wide-18's `ib-soft` | `kelly-shrunk`, `ml-linear`, `ml-sizing` | 0.9 | **Kill**: tested |
| M4 | `damped-persistence`: the optimal blend of persistence and climatology for an AR(1) anomaly: slot = p + rho (signal - p), with p the long-run share of up months and rho the signal's lag correlation | Statistical forecasting (persistence vs climatology skill; Murphy 1992) `[memory]` | A fixed blend of trend and hold | It is the minimum-MSE forecast when skill is weak | A constant blend of `tsmom12` and holding: `combo-1` `blend-iv` (p 0.39), wide-16's `bet-hedge-seedbank`, insure-2's fixed-exposure controls (trend is the cheaper insurance) | `combo-1`, `deep-1-meta`, `bet-hedge-seedbank` | 0.9+ | **Kill**: tested |
| M5 | `bma-lookbacks`: ensemble post-processing by Bayesian model averaging: weight the 1/3/6/12-month signals by their past verification likelihood; also the lagged-average ensemble (average of the last k Fridays' signals) | Ensemble forecasting (Raftery et al. 2005; Hoffman and Kalnay 1983) `[memory]` | Soft blend of lookbacks | Members with past skill get more weight; lagged members reduce noise | BMA sits between equal weights (`e4`, +0.063 pooled, not shown) and a walk-forward hard pick (`wf-pooled`, -0.03); the lagged ensemble is `tranching` / `trend-age` (dead) | `e4`, `wf-pooled`, `tranching` | 0.9 | **Kill**: between two tested ends |
| A1 | **`cred-xs`: Buhlmann-Straub credibility across the book.** Each asset's 12-month drift (in risk units) is shrunk toward the book's average drift with the credibility factor Z = a / (a + v): v the sampling variance of a year's drift, a the measured between-asset variance of true drifts. Hold while the credibility estimate is positive | Actuarial credibility theory (Buhlmann 1967; Buhlmann and Straub 1970; Boor 1992 on the complement) `[memory]` | When to be in: an asset slightly out of trend is held while the book's trend is strong, and dropped early when the book's trend is weak | A year of one asset's drift is a noisy estimate (v about 1/52 in weekly risk units); credibility is the minimum-MSE linear estimate, and the book's average is a less noisy complement. Z comes from the data, not from a free parameter | The six are four classes and highly correlated within classes (SPY/QQQ, BTC/ETH), so the collective is mostly "are stocks and coins up"; Buhlmann assumes independent risks. Holding a falling asset because the others rise gives back insurance; xtsmom (gate stocks on bonds) tied | `breadth-gate` (new, untested: keep an out-of-trend asset while the book is broadly in trend); `xtsmom` (dead); `crowded-trend` (the opposite direction, dead) | 0.85-0.95 | **Test** (pick 1) |
| A2 | **`cred-lr`: credibility toward the asset's own long-run drift.** Same Z = a / (a + v), but a is the measured variance over time of the asset's true one-year drift and the complement is its own long-run mean drift (expanding). Hold while Z x + (1 - Z) mu > 0 | Actuarial credibility theory (Buhlmann 1967: experience vs manual rate) `[memory]` | When to be in: a data-chosen negative threshold per asset | The textbook actuarial answer to "how much weight does one year of experience get": if a year of drift is mostly noise, Z is small and the rule leans to the long-run rate (holding) | Holding lost to `tsmom12` on the primary test (equal weight 0.88 vs 1.05); the insurance is in tails, not in the mean, and a mean model cannot see it. Fixed thresholds on the trend-tune surface were flat | trend-tune thresholds (fixed, flat plateau); `combo-1` (blend with hold) | 0.6-0.95 | **Test** (pick 2): Z is estimated, which no record did; the value of Z is itself an honest-evaluation number |
| A3 | `xl-layer`: reinsurance layering: an aggregate stop-loss on the book's calendar-year loss (cash once the year's loss passes an attachment point) or a retention kept in every slot | Reinsurance (excess-of-loss, aggregate stop-loss) | Exits by loss size | Insure only the expensive tail | A stop on the book's loss is `drawdown-control` (+0.07, p 0.14) and `cppi-floor`; a per-slot stop is `stop-0.25`; a retention is a blend with hold | `drawdown-control`, `cppi-floor`, `coin-fast-exit` | 0.85 | **Kill**: tested |
| A4 | `bonus-malus`: experience rating as a Markov ladder of exposure classes (up one class after a good month, down two after a bad one) | Motor insurance (Lemaire 1995) `[memory]` | A slow, path-dependent soft slot | Rewards a persistent record, punishes losses fast | A discrete soft trend on monthly returns: `e4` / `ensemble-tsmom`, `slew-limit`, `trend-age`; asymmetric up/down steps are `arm3-12`'s fast exit / slow entry in other words | `ensemble-tsmom`, `slew-limit`, `fast-reentry-2` | 0.9 | **Kill**: tested |
| A5 | `cred-forward`: credibility of the forward paper record against the backtest (Z = T / (T + k) with k from the variance ratio), and the Esscher / Wang premium of the insurance against its measured price | Credibility for evaluation; premium principles (Buhlmann 1980; Wang 2000) `[memory]` | Evaluation only | Says how many years of live record it takes before it outweighs the backtest | The same arithmetic as `power-map-1` (#150: +0.10 needs 72 years at 80% power); the premium was priced with real puts in insure-4 (PPUT 2.9 points a year dearer than trend), better than a model premium | `power-map-1`, insure-4 | n/a | **Kill**: measured in other words |
| O1 | `stop-reentry`: optimal stopping for re-entry after an exit (secretary-type rules, the odds algorithm) and the real-options entry/exit band (enter above z_H, exit below z_L) | Operations research (Bruss 2000; Dixit 1989) `[memory]` | When to buy back | Re-entry is the rule's known leak (it buys back late) | The re-entry line is closed: `or3-12`, `arm3-12` and `bear-legs` (bear-market rallies look like the bottom); a hysteresis band is eu-4's `dz25` (deeper covid drawdown) and `cost-band` | `fast-reentry`, `fast-reentry-2`, `bear-legs`, eu-4 `dz25` | 0.85 | **Kill**: tested |
| O2 | `robust-lookback`: robust optimisation: hold only if the trend is positive at every lookback in an uncertainty set (6/9/12 months, the worst case), or minimax-regret choice of lookback across eras; a newsvendor critical-fractile slot size | Robust optimisation (Ben-Tal and Nemirovski 1998; Goldfarb and Iyengar 2003); inventory theory `[memory]` | When to be in; slot size | Robust to the unknowable lookback | "All lookbacks agree" is k-of-n voting with k = n (wide-16's R1, `ensemble-tsmom`); minimax lookback choice is walk-forward tuning (`wf-pooled`, -0.03); a fractile size is a soft slot (`ib-soft`, `kelly-shrunk`). The lookback plateau (6-12 months) leaves no ambiguity worth hedging | `ensemble-tsmom`, `wf-pooled`, trend-tune | 0.9 | **Kill**: tested |

Also killed in passing (no row of their own): analogue forecasting (Lorenz 1969, nearest past
states: a nearest-neighbour model, run 2's ML cards), Thompson-sampling bandits over sleeves
(`deep-1-switch`: picks the last crash's winner), the (s, S) policy and the ruin floor (wide-16).

**What survives.** Of 12 candidates, 9 are tested or measured records in other words (soft
slots, blends with holding, lookback ensembles, stops and floors, re-entry rules, and three
evaluations the project already made with other tools); one evaluation (M2) is new but
descriptive and is left for later. The two that survive are both credibility estimates (A1,
A2): they change only *when* `tsmom12` is in, they have no free parameter (the weight on the
asset's own year is estimated from the data each Friday), and they shrink toward two different
complements, the book now (A1) or the asset's long-run rate (A2). Both are expected to fail.

## Step 2. The test (card `cards/wide-19.md`, pushed before any number)

See the card. Two variants, both against `tsmom12` on the primary test, both cash conventions;
out-of-universe signs on the 8 ETFs and the four price indexes.

Order: candidates and card f1cf2a4 (23:43 UTC; the card says "about 23:50", a slip: it was
pushed at 23:43), script and tests 68cf51b (23:45), one dry run (last 120 days, nothing logged;
it showed end-of-window Z values of 0.00 for `cred-xs` and 0.02-0.16 for `cred-lr` on the two
other sets, plumbing only, after the card), then the one real run (23:45).

## Step 3. Result (one real run, 2026-11-24 23:45 UTC): both fail

Tables: [`results/wide-19.md`](results/wide-19.md) (`uv run --with numpy python
research/lib/wide19.py`).

| Primary test, 1994-02-01 .. 2025-10-31 | Sharpe | dSharpe vs `tsmom12` | Paired SE | z | corr | Edge it needed (4.70 SE) | Max DD | Slot flips/yr | Z (median) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `tsmom12` | 1.044 | - | - | - | - | - | 37.4% | 7.2 | (1) |
| `cred-xs` | 1.091 | +0.047 | 0.049 | **+0.95** | 0.95 | +0.23 | 39.9% | 3.7 | 0.00 |
| `cred-xs`, above bills | 0.977 | +0.046 | 0.049 | +0.94 | | | | | |
| `cred-lr` | 0.948 | -0.097 | 0.091 | **-1.06** | 0.88 | +0.43 | 48.6% | 2.4 | 0.19 |
| `cred-lr`, above bills | 0.833 | -0.098 | 0.091 | -1.07 | | | | | |

| Out of universe (signs) | `cred-xs` dSharpe (z) | `cred-lr` dSharpe (z) |
|---|---:|---:|
| 8 ETFs, 2001-2025 | +0.026 (+0.28) | -0.070 (-0.54) |
| 4 price indexes, 1962-2025 | -0.024 (-0.44) | -0.065 (-0.82) |

**Verdict: both fail the card's bar** (z >= 4.70 in both cash conventions and positive on both
other sets). Nothing goes to the paper book.

- **The data give a year of one asset's drift almost no credibility.** For `cred-xs` the
  estimated between-asset variance of true drifts was at or below zero on most Fridays (Z median 0.00 in all three sets; the
  cross-sectional spread of one-year drifts, 0.78 V on the six, 0.71 V on the ETFs and 0.59 V
  on the indexes at the end, is smaller than the sampling noise V = 1/52 alone), so Z = 0 and
  the rule became a book-level switch: every eligible asset in while the book's average drift
  is positive. That book is +0.047 on the six (z 0.95; eras -0.02, +0.09, +0.14, -0.01, +0.09),
  half the flips, more exposure (0.82 vs 0.76) and a deeper worst loss (40% vs 37%); +0.026 on
  the ETFs, -0.024 on the indexes. A tie, on the side of `breadth-gate`'s untested hint.
- **`cred-lr` leans to holding and loses where holding loses.** Its Z (median 0.19 on the six,
  0.01 on the ETFs, 0.24 on the indexes) moves the estimate only a fifth of the way from the
  asset's long-run rate to the year's drift, so it held through most falls: 2000-09 -0.21 and
  2022-25 -0.23 on the six, 2000-09 -0.58 on the indexes, worst loss 49-52%. It led only in the
  2010s bull markets.
- **Post hoc (not a try, `lib/wide19_posthoc.py`).** Buhlmann's estimator assumes independent
  risks; with correlated assets the noise part of the cross-sectional variance is V (1 - rho),
  not V, so Z = 0 is biased low. Corrected at the last Friday (mean pairwise rho of weekly
  returns 0.15 / 0.33 / 0.60), Z is 0.00 on the six, 0.03 on the ETFs and 0.16 on the indexes:
  the conclusion stands. The 1994-99 era (SPY alone, so Z plays no part) differs by -0.022:
  the 52-week Friday grid is 364 days, not `tsmom12`'s 365, a small timing difference, not the
  method.
- **The power statement held**: |z| stayed within 1.1; both expected fails.

## What this says about the fields

- **Most ideas from forecasting, insurance and OR are tested records in other words**: 9 of 12
  candidates (calibrated soft slots, persistence/climatology blends, lookback ensembles,
  reinsurance stops, experience-rating ladders, re-entry stopping rules, robust lookback sets,
  and evaluations the project already ran as IC tables, insure-1 and power-map-1).
- **Credibility theory's honest-evaluation answer**: as an estimate of an asset's drift, one
  year of its own returns earns a credibility of 0 to about 0.2, both against the book and
  against its own history. That fits the project's reading that `tsmom12` is not a drift
  forecast but crash insurance (insure-1/2): it pays in the tails, which a mean-squared-error
  method cannot see. Shrinking the drift toward a complement therefore either changes little
  (the book switch) or gives the insurance back (toward holding).
- **Left open**: M2 `rev-costloss` (relative economic value of the exit for each cost/loss
  ratio) as a descriptive reframing of insure-1; `cred-xs` as a book-level switch is a tie that
  a pooled design (pooled-1's 41 markets) could judge, if a later lane wants it.

## Count

This run adds **2 mechanisms tested by a strategy (`cred-xs`, `cred-lr`; 2 variants, 6
robustness rows), 1 new descriptive idea (`rev-costloss`) and 9 killed as overlaps (note rows
in `tries.md`, not counted as tries, as wide-16/18 did), none passed**. On wide-18's count: 92
mechanisms, 23 strategy tests, 22 gates, none passed (not counting wide-17's, which runs in
parallel).
