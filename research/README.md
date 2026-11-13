# Idea lab (M2)

## Plain-language summary

Three research runs, night of 2026-11-12. **Neither the clever maths (run 1) nor machine
learning (run 2) beat the simple 12-month trend rule. Nothing new has earned a paper slot. What
is left is a choice of risk, and run 3 lays it out: [`risk-map.md`](risk-map.md).**

Run 3, the risk map:

- **Done:** the rules from runs 1 and 2 at 20 settings (hold everything, the trend rule, the
  trend rule with three volatility caps; crypto at 0%, 5%, 10% or a sixth per coin), each
  logged as a try. No new ideas, nothing tuned, held-out year untouched.
- **Result:** one chart of growth per year against worst drop, a table, and three presets.
  Since 2003, with 10,000 at the high: Careful fell to 8,820 at worst and grew 9% a year;
  Middle fell to 7,730 and grew 15%; Bold fell to 5,300 and grew 25%.
- **What it means:** every step up in growth came with a deeper drop. The size of the crypto
  slots moves an account most, the trend rule next, the volatility cap after that. None of
  them is skill.
- **Read with run 1:** an independent review (`reviews/review-1.md` on branch `review-1`)
  found that the trend rule's lead over holding everything, quoted below as Sharpe 1.05
  against 0.88 and a worst loss of 37% against 69%, comes from 2000-2002, when the book held
  only SPY and QQQ. Since 2003 the two tie on Sharpe (1.20 against 1.19); the trend rule gives
  a worst loss of 37% against 47% and costs about 4 points of growth a year. Run 3 reproduces
  those figures and shows 2003-2025 next to 1994-2025 throughout.

Run 2, machine learning:

- **Done:** seven ideas written down with their pass mark before testing; 31 model versions,
  52 backtests, all logged. Linear models, gradient boosting and a small decision tree on 15
  simple features (trend, volatility, drawdown, what the other assets are doing), tested so
  that no model ever saw its own future.
- **Result:** every version lost to the trend rule (Sharpe 0.67 to 0.94 against 1.05), and all
  but four lost to simply holding everything (0.88); those four beat it by 0.06 at most.
- **Why:** the models cannot tell good months from bad ones; their ranking is a coin toss.
  The only signal in the features is the weak trend effect the simple rule already uses, and
  fitting a model on top lost it rather than sharpened it. Boosting did not beat the plain
  linear model. A model filtering the trend rule's trades made the rule worse. Training on
  the size of gains instead of their direction, on 33 markets instead of six (five times the
  data), or to forecast a week ahead instead of a month, changed nothing.
- **The test is not broken:** a fake signal planted in the data is found, and a second agent
  that did not write the code hunted for errors and found none that changes a result. The
  fake signal has to be at least twice as strong as the best published forecasts before it
  beats the trend rule: six assets decided once a month are too few bets for forecasting to
  pay.
- **What it means:** no ML slot in paper trading on price features. The trend rule does not
  win by forecasting either: it is right less often than "always up". It wins by sitting out
  the large losses.

Run 1, ideas from the literature (unchanged):

- 14 ideas from about 150 papers (`survey-2026-11.md`), 216 backtests. None of the 13 with a
  pass mark passed: Kelly sizing, hidden Markov regimes, Hawkes processes and the rest each
  equal a simpler rule or lose to it.
- **What holds up:** the 12-month trend rule earned about what holding everything earned since
  1994 (17.8% a year against 18.2%) with a worst loss of 37% instead of 69%. The M1 lane
  already runs it.
- **The real choice is how much risk:** a volatility cap on that rule (`trend-vol`) takes the
  worst loss to 26% and growth to 13% a year; and the size of the crypto slots moves the worst
  loss more than any rule (5% per coin: 31%; a sixth per coin: 47%).
- **For the M1 lane:** the gym ignores dividends, which makes bonds look worthless (requests at
  the bottom).

Both runs:

- **Luck check:** the best of the 52 versions tried beat "hold everything" by 0.22 Sharpe; luck
  alone would give about 0.24. No new rule has shown an edge.
- **Still clean:** the last 12 months of prices were never looked at, for any idea.

Macro run (macro-1, 2026-11-13; [`macro-1.md`](macro-1.md)): **no macro phase beat the trend
rule in a way we can trust.** Fed hikes, real rates, the yield curve, money supply, the Fed's
balance sheet and credit spreads, each as a gate on `tsmom12`: all six cards fail, all behind
the trend rule since 2003. The Bitcoin halving cycle looks good (+0.15 Sharpe) but rests on three
winters and a window taken from folklore that saw them. Macro features are kept as regime inputs
for the RL agent, built look-ahead safe in `lib/macro.py`.

## Ranking after run 2

For forward paper trading (M3), best first. Run 2 changed nothing here: no ML model comes
close to a slot. None of the ideas passed its pre-set bar; the order is by what the tests
support.

1. `tsmom12` (12-month trend). Already M1's. Sharpe 1.05 against 0.88 for equal weight over
   1994-2025 (p = 0.08), worst loss 37% against 69%; holds on raw prices and at double costs
   (`results/robustness.md`). Keep it live: it is the bar.
2. `trend-vol` (trend with a volatility cap). Same Sharpe as `tsmom12`, worst loss 26%, growth
   13.3% a year against 17.8%. A paper slot only if the owner wants the low-drawdown profile.
3. `ensemble-tsmom` (trend at four horizons). +0.05 over `tsmom12`, right sign in every other
   market set, not significant. No separate slot; a possible revision of M1's rule later.
4. `sma200`, `drawdown-control`, `vol-target`, `trend-to-safe`: the same protection in other
   clothes. No slot.

Separate from the ranking, a decision for the owner: the size of the crypto slots
(`results/crypto-slot-size.md`). It moves the worst loss more than any rule above.

Dead in run 2, machine learning (Sharpe on the six assets 1994-2025; `tsmom12` 1.05, equal
weight 0.88; details in `results/ml-*.md`):

- `ml-linear` (0.84-0.89): found nothing and became equal weight.
- `ml-gbm` (0.72-0.86 over nine settings): found nothing and traded on the noise, at three
  to four times the trend rule's turnover. Boosting did not beat the linear model.
- `ml-filter` (0.73-0.94): a model grading the trend rule's trades took positions off at
  random.
- `ml-sizing` (0.68-0.82): letting the position follow the forecast followed the noise more
  closely.
- `ml-payoff` (0.67-0.77): trained on the size of gains, the models were worse at exactly that
  than "always up".
- `ml-pooled` (0.68-0.92): 33 markets and five times the rows gave the same coin toss.
- `ml-weekly` (0.82-0.89): forecasting a week ahead, four times the bets, the same coin toss.
- Forecast skill for all of them: AUC 0.48 to 0.51 (0.50 is a coin toss), below the single
  12-month flag at 0.52 and below most trend features left alone (0.52 to 0.54,
  `results/ml-feature-skill.md`). `results/ml-control.md` shows a planted signal is found, and
  that it takes a correlation of 0.2 to 0.3 with next month's return to beat `tsmom12` on
  this book.

Dead in run 1, with the one-line reason (details in `ideas.md` and `results/`):

- `fracdiff-momentum`: a fast trend rule; worse than 12-month momentum everywhere.
- `hmm-regime`: beats a volatility switch, loses to the 200-day average; slept through 2000-2002.
- `kelly-shrunk`: the no-leverage cap turns it into inverse-volatility weights.
- `universal-portfolio`: 30 years is far too short for its guarantee; it stays where it starts.
- `hawkes-clustering`: daily crash clustering is too weak to trade.
- `absorption-ratio`: worked until its paper came out in 2010, not since.
- `month-end-liquidity`: real for decades (t of 3 to 4 on old indexes), faded since 2014.
- `dip-rsi2`: real but tiny (in the market 5% of the time) and halved since publication.
- Killed by reading alone: topological data analysis, transfer entropy, critical slowing down,
  change-point momentum, daily crypto reversal, pre-FOMC drift, return forecasts from
  time-series foundation models.

## Research run 3: the risk map (finished)

Brief: `chief-of-staff/briefs/grimstrade-research-3.md`. Branch `research-3` (from
`research-2`), draft PR #9. Hard stop 2026-11-12 08:40 UTC. Started 07:13 UTC.

**Done**

- `cards/risk-map.md`, written before any run: a description, no pass bar.
- `lib/risk_map.py`: `run` backtests the 20 variants and logs them (idea `risk-map` in
  `tries.md`); with no argument it rebuilds every table and the chart from the saved equity
  curves, logging nothing; `check` proves no look-ahead (same weights from truncated history
  on six days, all 20 variants).
- `risk-map.md` and `risk-map.svg` for the owner; `results/risk-map.md` with every variant
  over 1994-2025, 2003-2025 and 2013-2025, the dates of each worst drop, Sharpe, and the
  average share held in crypto and in cash.
- Checks against earlier work: `hold-c17`, `tsmom12-c17` and `tv40-c17` give the Sharpe and
  worst loss logged in runs 1-2 (0.88, 1.05, 1.03); the 2003-2025 slice gives the review's
  figures (1.20 against 1.19, 36.5% against 47.0%, 20.7% against 24.9% a year); the 2013
  slice of `hold-c00/c05/c10` gives the worst losses in `results/crypto-slot-size.md`.

**Assumptions**

- Total-return data: the harness already used dividend-adjusted ETF prices from Yahoo's
  keyless chart API (`data/adj/`), so nothing new was fetched.
- "Since 2003" is a slice of the 1994 run from 2003-01-01, not a fresh account. It matches
  the review's separate run to the decimals quoted.
- "A sixth per coin" is the equal slot the earlier runs used (1/n of the eligible assets), so
  it was a fifth in Bitcoin from 2013 to 2017.
- Volatility caps of 60%, 40% and 20% a year. 40% is the `trend-vol` card's setting; the
  other two were picked before any run to bracket it, not tuned.
- Presets: Careful `tv20-c05`, Middle `tsmom12-c10`, Bold `hold-c17`, picked to span the
  chart, not for Sharpe. The paper lane's `ts_momentum` (equal slots, 40% volatility cap) is
  nearest to `tv40-c17`, which lands beside Middle. Its volatility estimate and daily
  decisions differ from the menu's, so that is a neighbour, not a replay.

**Doing**

- Nothing half-finished.

**Next (nothing here is started)**

- The owner picks a preset (Desk question). The M1 lane then needs a crypto slot size, which
  its `ts_momentum` does not have today (every asset gets an equal slot).
- The run-1 summary and ranking below still carry the 1994-2025 headline; the review's
  correction is noted at the top, not yet worked through `ideas.md` and the ranking.

## Research run 2 (finished)

Brief: `chief-of-staff/briefs/grimstrade-research-2.md`. Branch `research-2` (from `research-1`),
draft PR #7. Question: does machine learning on simple features beat `tsmom12` after costs?
Answer: no. Hard stop 2026-11-12 08:40 UTC. Started 02:08 UTC, cut off by the usage limit at
02:32, resumed 06:32.

**Done**

- ML test rules in `protocol.md` ("Machine-learning tests" and the four sections after it),
  each written before the test that uses it.
- `lib/ml.py` (features, purged walk-forward fits, sizing, payoff weights, pooled rows),
  `lib/mltest.py` (the card test), `lib/lookahead_check_ml.py` (passes for every model kind:
  cached models give the same weights as models refitted on history truncated by the gym,
  pooled rows are the same when built from truncated history, and forecasts do not move by a
  bit when every later bar is scrambled).
- Seven cards, all tested, all dead, each `results/ml-*.md` ending in a dated verdict:
  `ml-linear`, `ml-gbm` (9 settings), `ml-filter` (carded before any model was fitted);
  `ml-sizing`, `ml-payoff`, `ml-pooled`, `ml-weekly` (each carded after the ones before it had
  failed, and saying so). `ml-weekly` runs with `ML_HORIZON=7` in front of the command.
- `results/ml-control.md` (`lib/control_ml.py`): planted signals of correlation 0 to 0.30. The
  machinery finds them; 0.20 ties `tsmom12`, 0.30 beats it.
- `results/deflation.md` refreshed (52 selectable variants; +0.24 from luck, +0.22 seen).
- Dividends (brief, item 4): nothing to add. The research harness has used dividend-adjusted
  prices for every ETF since run 1 (`data/adj/`), so every ML test already credits them;
  `results/robustness.md` has the raw-price view. The request to the M1 lane stands.
- Independent code review of `lib/ml.py` and the harness by a subagent: no bug that could
  change a verdict ("Code review" below). It led to `results/ml-feature-skill.md`
  (`lib/feature_skill.py`, no backtest): single features scored without a model.
- Summary and ranking above; `ideas.md` statuses.
- The held-out year is untouched: nothing passed its train bar.

**Doing**

- Nothing half-finished: every file on the branch is complete as it stands.

**Next (a later run; nothing here is started)**

- More models on the same price features are not worth another night. What would be different
  in kind: other information (interest rates and credit spreads from FRED, keyless; funding
  rates need perpetual futures, which the gym does not have), or a much wider book to rank
  (30 or more ETFs, long only), where a weak forecast has more bets to work on.

**Code review (2026-11-12, by an agent that did not write the code).** It recomputed features
and labels from the raw price files (same to 1e-14), scrambled every bar after a fit day (rows,
chosen settings and forecasts unchanged to the bit) and read the purge arithmetic, cache keys
and weights. No leak, no misalignment. What it did find, none of it able to change a verdict:

- The results said "the features hold no signal" when only the models had been scored.
  Corrected in `results/ml-control.md`, `ml-gbm.md`, `ml-payoff.md`, `ml-pooled.md`; the
  measurement is `results/ml-feature-skill.md`.
- The planted control signals are about 0.02 stronger than their labels (chance of the noise
  draw). Noted in the control's reading.
- The S&P 500 warm-up rows, and SPY's rows until QQQ joins in 2000, have cross-asset features
  that only repeat the asset's own (one asset in the set). Early models cannot learn those
  four features. Pushes towards a null; `ml-pooled`, which has no warm-up rows, was null too.
- On market-holiday Fridays before crypto exists the weekly decision slips to Monday (32 of
  1,658 Fridays on the six assets), for the models and the twins alike.
- The 0.05 floor of the confidence ratio is in the wrong units for the `raw` target. Only
  `gbm-raw` uses it, with the hold-or-not rule, where the floor plays no part. Fix before
  using `raw` with another position rule.
- Labels run from the Friday close, one bar before the earliest fill, so the skill tables
  slightly flatter what could be traded. Works against a false null.
- With payoff weights the scaler in the linear pipeline is fitted unweighted. Cosmetic.

**Run 2 in one paragraph:** machine learning on 15 simple features did not beat `tsmom12`.
Linear models found nothing and became equal weight (0.89 Sharpe against 1.05); boosting found
nothing and traded on the noise (0.72-0.86 over nine settings); a model filtering the trend
rule made it worse (0.73-0.94); sharper position rules, payoff-weighted training, five times
the training data and a one-week horizon did not help (0.67-0.92). The models' forecast skill
is nil (AUC 0.48-0.51, below the single 12-month flag at 0.52 and below the trend features
left alone). A planted signal is detected, and it has to reach a correlation of 0.2 to 0.3
before it beats `tsmom12`: six assets decided monthly are too few bets for return forecasting
to pay.

Run any card with `uv run --with numpy --with scikit-learn python research/lib/idea_ml_<x>.py`
(`DRY=1` first for a plumbing check: a real run appends tries).

## Research run 1 (finished)

Brief: `chief-of-staff/briefs/grimstrade-research-1.md`. Branch `research-1`, draft PR #4. Hard
stop 2026-11-12 08:40 UTC. Started 2026-11-11 23:05 UTC, cut off by the usage limit at about
23:15, resumed 01:32.

**Done**

- Harness, long price history, `protocol.md` (fixed before any test), baselines and twins.
- `survey-2026-11.md` (verdict per family, 165 source entries with links) from the six parts in
  `notes/survey-parts/`.
- Nine cards (committed before any test, 6ad40cc), then three more (e8197ba) and two more
  (8b46f31), each saying what had been seen by then. All fourteen tested and judged:
  `results/<idea>.md` each end with a dated verdict; `ideas.md` has every status.
- `results/robustness.md`: front-runners on raw prices and at double costs.
- `results/cash-interest.md`: what-if with T-bill interest on cash (adds 0.5-0.8% a year to the
  cautious rules, changes no ranking).
- `results/deflation.md`: the best edge seen against what luck alone would give (0.22 vs 0.20).
- `results/crypto-alone.md`: the plain and run-2 rules on BTC alone and ETH alone (trend does
  not beat holding there; it shrinks the winters; the size of the slot matters more).
- The summary and ranking above.

**Doing**

- Nothing half-finished: every file on the branch is complete as it stands.

**Next (a later run; nothing here is started)**

- Cards still in `ideas.md` under "New": `vol-shift`, `turbulence`. Write the card first, test
  with `lib/testkit.py`, `DRY=1` before the real run (a real run logs tries).
- The held-out year (2025-11-11 to 2026-11-09) has not been looked at for any idea. The harness
  allows one look per idea; spend it only on an idea that passes its train bar.
- If the M1 lane credits dividends or pays interest on cash, rerun `lib/baselines.py` and
  `lib/robustness.py`: rules that hold cash will look better than they do here.

## Layout

- `risk-map.md`, `risk-map.svg`: the owner's page on how much risk and how much crypto.
- `ideas.md`: one line per idea with status. Dead ideas stay.
- `survey-2026-11.md`: what the literature says held up or failed, with links.
- `cards/<idea>.md`: hypothesis card: claim, why, test, pass bar. Written before results.
- `protocol.md`: the test rules, fixed before any test.
- `tries.md`: every backtest variant ever run, train or held-out. Appended by the harness.
- `results/`: what each test showed, one file per idea, ending in a dated verdict.
- `lib/`: research scripts. `data/`: price caches (git-ignored).

## Requests to the M1 lane (code in `src/`)

- **Count the idea lab's tries in the deflated Sharpe.** `research/tries.md` has one row per
  backtest; the rows with kind `variant` (52 on the six assets so far, plus the timing rules run
  per asset) are the ones that could have been selected. `lib/deflation.py` shows one way to
  read them.
- **Credit dividends in the gym** (already in `docs/BACKLOG.md`; this makes it urgent). Raw TLT is
  0.99x over 2002-2025; with coupons it is 2.28x. SPY: 17x raw, 31x with dividends since 1993. The
  live scoreboard will understate every bond holder and flatter every rule that avoids bonds.
- **Pay interest on cash** (for example the 3-month T-bill rate), or add a cash-like ETF (BIL/SHV)
  to the universe. Smaller than it sounds: `results/cash-interest.md` puts it at 0.5-0.8% a year
  for rules that hold a quarter of the book in cash, with no change in ranking. Truthful
  accounting, low priority.
- `report.score` annualises with 365 days over the equity rows it gets. If a strategy's history
  ever holds no crypto, the gym reports only trading days and the Sharpe is overstated by about
  20% (sqrt(365/252)). Harmless today (crypto is always in the history); the research harness
  fills calendar days itself.
