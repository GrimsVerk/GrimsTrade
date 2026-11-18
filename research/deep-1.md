# deep-1: a failure atlas of the tested models, then one honest combination test

Status: **done** (2026-11-18). Branch `deep-1`. The card further down is as it was committed
before any number; what changed afterwards is listed under "Changes after the card".

## In plain words

**No combination of the models we already had beats the 12-month trend rule (`tsmom12`). The
reason is now clear: they are all the same six assets held at different sizes, so they lose in
the same weeks.**

- **What was done.** Part A: 52 return series (every card of runs 1 and 2, the macro cards, the
  benchmarks, the RL agents, the YouTube rules) were laid side by side and cut by era, asset,
  trend state, volatility, stress window and `tsmom12`'s ten deepest drawdowns. Part B: three
  ways of mixing 29 of those models with `tsmom12`, each choosing its mix from past data only,
  fixed before any number was seen.
- **Result.** All three mixes fail their pass mark. Sharpe (return per unit of risk) over
  1994-2025: 1.01, 1.02 and 1.08 against `tsmom12`'s 1.05. The best one is no better than
  simply averaging all the models (1.06).
- **The ceiling is low.** Even the best fixed mix chosen with full hindsight reaches only 1.22.
  There was little to find, and past data found about a sixth of it.
- **What is new.** Six failure modes, each with the asset and the years behind it (below). Two
  are worth a card of their own: the trend rule is slow out of a coin top (eight of its ten
  deepest drawdowns), and it misses the rebound (the slots it keeps empty earned 16-23% a year
  whenever more than a third of the book was still in trend).
- **Held-out year:** not spent. Nothing passed.

| Mix | How it chooses | Sharpe 1994-2025 | Since 2003 | Worst loss | Growth a year | Other markets ahead | Verdict |
|---|---|---:|---:|---:|---:|---:|---|
| `tsmom12` (the yardstick) | | 1.05 | 1.20 | 36.5% | 17.8% | | |
| `stack` | `tsmom12` plus the one model least like it in its losing weeks, sized by risk | 1.01 | 1.22 | 30.9% | 12.4% | 1 of 3 | fails 3 of 6 bars |
| `switch` | per trend state, the model that did best in that state so far | 1.02 | 1.05 | 34.7% | 14.9% | 1 of 3 | fails 4 of 6 |
| `meta` | a ridge regression weighs all 30 models | 1.08 | 1.27 | 32.3% | 14.7% | 2 of 3 | fails 2 of 6 (p = 0.27; ahead in 3 of 5 eras) |
| plain average of all models (added afterwards) | no choice at all | 1.06 | 1.29 | 39.7% | 14.5% | | reference, not a candidate |
| best fixed mix with hindsight | knows the whole period | 1.22 | 1.49 | | | | a ceiling, not a strategy |

Full tables: [`results/deep-1.md`](results/deep-1.md) (Part B),
[`results/deep-1-atlas.md`](results/deep-1-atlas.md) (Part A).

**Why each mix failed**

- `stack` picks what looked different, and that kept changing its mind: the Fed-hiking gate from
  2001 to 2014, then the 60/40 stock-and-bond book from 2015, in time for the bond crash of 2022
  (2022-25: Sharpe 0.50 against 0.88). A fifth of its book differs from
  `tsmom12`, so it is a real alternative; it is not a better one.
- `switch`, for the state "trends are up", kept choosing a gate that had dodged the last crash:
  the yield-curve gate (2000-07 and 2020-24) and the absorption ratio (2008-19). It dodged the
  dot-com bust (-2%), 2008 (+6%) and covid (+1%), and then sat out the 2023-24 rise (2022-25:
  Sharpe -0.32). Failure mode 6 below, reproduced out of sample.
- `meta` could not tell the models apart and spread itself over all of them (largest share 6-17%).
  It equals the plain average (+0.02, p = 0.23). Averaging thirty versions of "hold less when
  things look bad" smooths the ride a little (since 2003: 1.27-1.29 against 1.20, worst loss
  about 30% against 36.5%) and costs growth (17% a year against 21%). That is the same trade as
  `trend-vol`, `ensemble-tsmom` and `drawdown-control` before it: a choice of risk, not proof of
  skill.

**How sure**

- "No mix passes" is firm: two of the three are behind `tsmom12`, and the third is ahead by 0.03
  with a pass mark that needs about 0.15 or more.
- "There is no complement in this pool" is firm for these six assets: the hindsight ceiling
  (1.22) is arithmetic, not a forecast.
- "Averaging helps a little" is not proven: +0.08 since 2003 with p = 0.11, and it is the fourth
  rule of this family to land there. Each alone proves nothing; four in a row on the same data
  is still one bet.
- The three rules and their bar were fixed before any deep-1 number. The plain average and the
  hindsight ceiling were added after the result, and are labelled so.
- No look-ahead: a unit test with a scrambled future, and the three books' weights recomputed
  from history cut off at six days (`lib/deep1_combo.py check`), agree exactly.
- Tries: 3 `variant` rows, 9 out-of-universe and 18 component `robustness` rows, 1 `baseline`.

## Part A: where each model fails (written before Part B was run)

Tables: [`results/deep-1-atlas.md`](results/deep-1-atlas.md). 52 return series, every one a
configuration already in `tries.md`: 35 rebuilt with positions (all reproduce their logged Sharpe;
three boosting models differ by 0.01-0.02, see "Changes after the card"), 17 read from saved
equity curves. Nothing was selected. A drawdown = the fall from a high to the next low.

**The six failure modes that matter**

1. **The trend rule is slow out of a coin top.** Eight of `tsmom12`'s ten deepest drawdowns are
   Bitcoin and Ether (2013 twice, 2017 twice, 2018-20, 2021 twice, 2024-25); over the ten falls
   coins cost 166 points, stocks 55. A coin can halve in weeks while its 12-month return is still
   far above zero after a year in which it rose five-fold. The rules that lose least there are the
   ones that hold fewer coins when coins are wild (`trend-vol`: 84 points instead of 166; worst
   loss 26% against 36%) and the cycle clocks (`halving-and`, `ath-and`), which we do not believe.
   *Mitigation:* size or cap the coin slots by volatility (known: `trend-vol`, the crypto slot
   size), or a faster exit for coins only (that is the `trend-tune` lane's question).
2. **Stepping out means missing the rebound.** In the six months after the seven stress windows
   `tsmom12` made 0, -1, +29, 0, 0, +5 and +1%; equal weight made +15, +23, +47, +29, +7, +61 and
   +26%. Every trend clone, every macro gate and the rl-2 agents share this. Table 2b takes the
   gap apart: when at most a third of the book is in trend (13% of days, nine tenths of them in
   2000-09 and 2022-25) the empty slots lost 4% a year, so being out was right. When more of the
   book is in trend, the slots `tsmom12` leaves empty earned 16 to 23% a year, most of it coins
   coming back from a winter while stocks were fine. So an asset out of trend was bad news only
   when most of the book was out of trend with it. *Mitigation idea:* a breadth gate (keep an
   out-of-trend asset unless the book is broadly out of trend), or a faster way back in
   (`sma200` and `ensemble-tsmom` earn +1% a year in the "off" state where `tsmom12` loses 2%).
   Found after looking: it needs its own card and out-of-universe test before anyone believes it.
3. **The always-invested rules have one long bear market on a narrow book, and 2022.** Equal
   weight, `inverse-vol`, `kelly-shrunk`, `vol-target`, `hawkes`, `hmm` and `logit` all have
   the same worst drawdown: 2000-2002, 57-69%, on a book of SPY and QQQ. Since 2003 several are
   ahead of `tsmom12` (`kelly` 1.36, `inverse-vol` 1.32, `vol-target` 1.28 against 1.20). The
   bond-heavy ones then lost 26-27% in the 2022 rate shock, when bonds fell with stocks.
   *Mitigation:* a trend or volatility test on top, which is what `trend-vol` is; it is ahead of
   `tsmom12` in 70% of three-year windows and behind by 0.25 or more in 1%.
4. **The boosting models lost by not holding Bitcoin, and by sitting through the dot-com bust.**
   They held about half of `tsmom12`'s Bitcoin in 2013-2021 (8% of the book against 15%): Bitcoin
   gave `gbm` 2.6 points a year against `tsmom12`'s 6.9, which is most of the 5.7-point gap.
   For four of the six the worst three-year window starts in October 2012: Bitcoin joined the
   book in 2013 with no history a model could have learned from. In the dot-com bust they were
   about half invested (`tsmom12`: a quarter), having been trained on the S&P of 1962-99, where
   trend did not pay. In falls they were often better than `tsmom12` (covid -6 to -9% against
   -22%), and in 2022-25 four of them are ahead. *Mitigation:* none cheap; rl-2 already tried
   "only tilt the trend rule" and got the trend rule back.
5. **The free RL agents are a geared coin position.** Four of the five take 1.6 to 2.0 times
   `tsmom12`'s losing weeks and 1.6 to 1.9 times its winning weeks, and fell 60-87% in the coin
   winters. *Mitigation:* a coin cap, which rl-2 had; with it the agent copies `tsmom12`
   (correlation 1.00).
6. **Gates that leave early pay for the recession that did not come.** The macro gates beat
   `tsmom12` in 2000-09 (`curve-and` 0.57, `spread-and` 0.54, `hike-and` 0.52 against 0.19) and
   lose 2022-25 (`curve-and` -0.10, `walcl-and` -0.16, `real-and` 0.18 against 0.88): out of
   the market through the 2023-24 rise. *Mitigation:* none; each gate rests on three to five
   episodes. Part B's `switch` walked into exactly this.

**What the atlas says about combining.** Every six-asset rule shares `tsmom12`'s bad weeks: in
the weeks `tsmom12` lost, the correlations of the rules in Part B's pool run from 0.62 to 0.96
(only the 60/40 benchmark is lower, 0.44), and no rule keeps clearly more of the good weeks than
of the bad ones (the best, `halving-and` and `curve-and`: 0.08 more of `tsmom12`'s average good
week than of its average bad week). The models are the same six assets held at different sizes.
The two SPY-only timing rules are the exception (correlations 0.05 and 0.21) and are too small
to matter (2-6% a year). Part B confirmed it: past data could not pick a useful mix.

**How sure.** These are descriptions of one history. Failure modes 1, 3, 4 and 5 are arithmetic
(which asset lost what, when). Mode 2's breadth reading is the weakest: the "off" state is two
episodes (2000-03 and 2008-09) plus 2022, and it was seen after looking.

## Next lanes

1. **A breadth gate, as its own card (failure mode 2, the largest cost).** Rule fixed in advance:
   hold every eligible asset, except that an asset out of 12-month trend is dropped while at
   most a third of the book is in trend. Twins: `tsmom12` and equal weight, both. The six assets
   give three "off" episodes, so the verdict has to come from elsewhere: the 8 other ETFs, the
   four indexes from 1962, the 33-market pool and the wide books of `wide-1`, with a placebo
   (the same rule with the breadth series shifted by a year). It touches `tsmom12`'s exit, so
   agree the split with the `trend-tune` lane first.
2. **Coin tops on a book with enough coins (failure mode 1).** Six assets hold four coin
   tops; the Coin Metrics top-100 book of breadth-1 (dead coins included) holds hundreds. Card:
   does a volatility-capped slot, or a faster exit on coins only, lose less from a top than the
   12-month rule, coin by coin, after 30 bps costs? Twin: `tsmom12` on the same coins. Judge on
   the drop from each coin's own top and on Sharpe; then carry the one surviving setting back
   to BTC and ETH unchanged.
3. **A complement has to come from another source of return: test carry as the first one.**
   This pool has none (ceiling 1.22). The funding-carry book of short-1 and carry-2 earns from
   something else. Once carry-3 has its cost answer, run deep-1's `stack` rule unchanged on two
   sleeves, `tsmom12` and the carry book: first the atlas question (the carry book's correlation
   with `tsmom12` in its losing weeks, 2021-2025), then the walk-forward mix. Needs futures in
   the gym, so it stays a research result until the broker has them.

Not a lane, a note: more mixing rules on this pool are not worth a run. The ceiling says so.

---

## Card (fixed 2026-11-18, before any deep-1 number)

Branch `deep-1` from `carry-2`. Rules: `protocol.md`, all of it. Research only; six live assets
(SPY, QQQ, TLT, GLD, BTC, ETH), total-return prices, gym fills and costs, train period
1994-02-01 .. 2025-11-09.

### What had been seen when this card was written

Everything on `carry-2`, `summary-1`, `review-1`: every result table of runs 1-3, macro-1, rl-1
to rl-3, info-1, breadth-1, short-1, carry-2, and the review. In particular: `tsmom12` and equal
weight tie since 2003 (1.20 / 1.19); `ensemble-tsmom` and `drawdown-control` are ahead of
`tsmom12` since 2003 without proof; equal weight beats `tsmom12` in the year after a fall;
`inverse-vol` scores 0.85 over 1994-2025; the halving gate looks good and is not believed. One
unlogged timing run of the `tsmom12` baseline (Sharpe 1.05, the logged figure) was made to
measure how long a backtest takes. Nothing else was computed for this card.

### Question

Why does each tested model fail where it fails (which years, which assets, which state of the
market, which drawdown), and do the models' strengths cover each other's weaknesses well enough
that a combination, chosen with past data only, beats `tsmom12`?

**Out of scope** (lead's note, 2026-11-18): `tsmom12`'s own anatomy and tuning (lookbacks, exit
rules, walk-forward tuning) belong to the `trend-tune` lane. Here `tsmom12` is the yardstick:
its state and its drawdown episodes are the cuts the other models are laid against, and no
parameter of it is varied.

### Part A: the atlas (a description; no pass bar, nothing selectable)

**Models.** One daily return series per model on the six assets, train period.

- *Rebuilt from code with positions* (re-scores of configurations already in `tries.md`, so
  not logged again; each is checked against its logged Sharpe): the benchmarks and twins
  (`equal-weight`, `tsmom12`, `sma200`, `inverse-vol`, `vol-calm`, `bh-spy`, `bh-btc`,
  `sixty-forty`); the primary variant of every run-1 card (`kelly-shrunk` k0.2, `hmm-regime`
  hard, `fracdiff-momentum` d0.4, `drawdown-control` d1.0, `universal-portfolio` up,
  `absorption-ratio` six, `hawkes-clustering` down2, `vol-target` t40, `ensemble-tsmom` e4,
  `trend-vol` tv40, `trend-to-safe` safe); the primary variant of every run-2 card (`logit`,
  `gbm`, `meta-gbm`, `gbm-prop`, `gbm-pay`, `gbm-pool`, `gbm-wk`); the primary `-and` variant of
  every macro card (`hike-and`, `real-and`, `curve-and`, `m2-and`, `walcl-and`, `spread-and`,
  `halving-and`). The two single-asset timing cards (`month-end-liquidity`, `dip-rsi2`) are
  rebuilt on SPY alone and shown apart: they are not six-asset rules.
- *Read from saved out-of-sample equity curves, no positions* (the curves the runs wrote under
  their worktrees' git-ignored `research/data/runs/`; copied read-only to
  `<cache_root>/derived/deep-1/`): the five rl-1 ensembles and the four rl-2 ensembles
  (2000-01-07 on), and the primary variants of the ideas-1 rules. Regenerating RL positions
  needs the torch pipeline and is not worth it for agents that lost badly (rl-1) or copied
  `tsmom12` (rl-2). These series get every cut below except the per-asset one.

**Cuts** (all fixed here):

1. *Era*: the five protocol eras, plus 2003-2025 (the review's window) and the full period.
2. *Asset*: for models with positions, each asset's contribution to the daily return
   (yesterday's target weight times the asset's close-to-close return; the gap to the gym's
   return is shown as "costs and fills"). Reported over the full period and inside drawdowns.
3. *Trend state*, by `tsmom12`'s own position: `breadth` = share of eligible assets `tsmom12`
   holds at its decision in force. `off` if at most 1/3, `on` if at least 2/3, else `mixed`.
4. *Volatility state*: realised volatility of the equal-weight book over the 60 days to
   yesterday, cut into thirds of its whole train-period distribution (a description, so the
   full-sample cut-offs are allowed here; Part B never uses them).
5. *Stress windows*: the seven of the protocol, and the *rebound* after each: the 182 days
   that follow the window's last day.
6. *`tsmom12`'s ten deepest drawdown episodes* (high-water mark to the next new high; peak,
   trough, recovery): every model's return from peak to trough and over the 182 days after the
   trough, and which assets drove `tsmom12`'s loss.
7. *Correlation with `tsmom12`* on weekly returns (7-day blocks): overall, in the weeks
   `tsmom12` lost, and inside its drawdown episodes (peak to trough).
8. *Rolling three-year windows* (a new window every quarter): Sharpe minus `tsmom12`'s; share of
   windows ahead, worst, median, best.
9. Each model's own three deepest drawdowns: dates, depth, the asset that drove it.

Output: `results/deep-1-atlas.md` (compact tables) and, in this file, the three to six failure
modes that matter, each with a mitigation idea. Part A selects nothing and spends no tries; a
component run that is not yet in `tries.md` is logged as `robustness` under idea `deep-1`.

### Part B: three combination rules (fixed here, before Part A's numbers)

The rules are mechanical: every choice inside them is made by the rule itself from past data,
so nothing in Part A's tables can be used to pick a winner. They are the walk-forward test of
whether three of the atlas tables (correlation in losses, the trend-state table, the overall
return table) can be traded.

**Pool.** `tsmom12` plus 29 complements: every rebuilt six-asset model above except `bh-spy`
and `bh-btc` (single assets, not rules) and `halving-and` (its window was taken from folklore
that had seen the winters; macro-1 judged it "not believed"). The two SPY-only timing cards are
not in the pool.

**Machinery shared by the three rules.**

- A *sleeve* is a pool model: its own daily target weights, and the daily returns of its own
  gym replay (costs included) on the same universe from the same first day.
- The combined book's target weights on a day are the sleeve shares times each sleeve's target
  weights, summed per asset. It goes through `gym.simulate` like any strategy (one account, so
  trades between sleeves net out and every real trade pays the gym's costs).
- Sleeve shares are refitted on the first Friday of each calendar year (the protocol's
  schedule for fitted rules) from sleeve returns up to the day before, and held until the next
  refit. A decision on day `d` uses sleeve returns up to `d - 1` only (the gym's equity for day
  `d` includes the crypto close at midnight, after the 22:30 decision).
- Statistics use weekly returns: 7-day blocks counted back from the day before the refit,
  expanding window from each model's first day.
- A complement is *eligible* at a refit once it has 104 weekly returns since the first day it
  could act (the ML models' first fit day, `absorption-ratio` from 2002) with non-zero variance.
  Until the first refit at which `tsmom12` itself has 104 weeks, the book is `tsmom12`.
- Sharpe of weekly returns with zero variance counts as 0.

**B1 `stack`** (risk-based stacking with the complement least like `tsmom12` when it loses).
At each refit: among eligible complements with a positive Sharpe to date, pick the one whose
weekly returns have the lowest correlation with `tsmom12`'s over the weeks in which `tsmom12`
lost money (at least 26 such weeks; a complement with zero variance on them is skipped). The book
is two sleeves, `tsmom12` and that complement, with shares proportional to 1 / variance of each
sleeve's weekly returns over the last 156 weeks (all there are, if fewer), summing to 1. If no
complement qualifies, `tsmom12` alone.

**B2 `switch`** (a switch by trend state). The state on a Friday is the atlas's trend state
(`off`, `mixed`, `on`) from `tsmom12`'s decision that day. At each refit, for each state: the
model held in that state until the next refit is the one, among `tsmom12` and the eligible
complements, with the highest Sharpe over the past weeks that began in that state (a complement
needs 104 such weeks; ties and no data go to `tsmom12`). The book holds, each week, the full
target weights of the model assigned to that week's state.

**B3 `meta`** (a ridge meta-learner on the sleeves' returns). At each refit: ridge regression
of the constant 1 on the weekly returns of `tsmom12` and all eligible complements, no intercept
(Britten-Jones 1999: unpenalised, the coefficients are the mean-variance weights). Penalty
`lambda x T x v`, with `T` the number of weeks and `v` the average second moment of the
sleeves; `lambda` chosen from 0.1, 1, 10 at every fit by 5-fold cross-validation in time order
on those past weeks (squared error on the left-out block). Coefficients below zero are set to
zero and the rest scaled to sum to 1: those are the sleeve shares. All zero: `tsmom12` alone.

Three variants, no sweep. Each is logged as `variant` under ideas `deep-1-stack`,
`deep-1-switch`, `deep-1-meta` when it runs.

**Pass bar (each rule on its own; fixed now).** Twin: `tsmom12`.

1. Sharpe on the six assets, full train period, beats `tsmom12` with bootstrap p < 0.033
   (the protocol's 0.10 shared among three rules).
2. Ahead of `tsmom12` in at least 4 of the 5 eras.
3. Max drawdown not more than 5 points worse than `tsmom12`'s.
4. Out of universe: the Sharpe difference to `tsmom12` has the same sign in at least two of
   three sets: the 8 other ETFs, the 6 other coins, the four indexes as one portfolio from 1962.
   The rule is rerun unchanged on each set with the pool rebuilt there: every pool model that
   exists on the set, ML models refitted on the set's own history as the protocol says,
   `sixty-forty` dropped (it needs SPY and TLT), `absorption-ratio` switching off the set's risk
   assets (the card's list for ETFs; every coin; every index), macro gates as in the protocol.
5. Beats equal weight on Sharpe.
6. Not behind `tsmom12` on Sharpe over 2003-01-01 to the end of train, and not behind equal
   weight there (the review's window).

Also reported, not a bar: the average distance of the book's weights from `tsmom12`'s (a rule
that passes while holding `tsmom12` is not a finding), the sleeves chosen at every refit, and
the Sharpe of the best single pool model with hindsight (what perfect selection would have
given).

**Held-out year** (2025-11-11 .. 2026-11-09): once, for a rule that passes all six bars, and
for no other. The walk-forward simply continues into it; the sleeves' own held-out returns are
computed only inside that one run and logged as `robustness`. If nothing passes, the year stays
unspent.

**Look-ahead check.** A unit test (synthetic returns, scrambled future) proves the sleeve
shares at a refit do not change when later returns change; `lib/deep1_combo.py check` recomputes
the three books' weights on six days from history truncated at each day.

**What would count as what.** Pass: a combination candidate for the paper lane, with the
held-out look. Fail with the book far from `tsmom12`: the models' differences are real but not
predictable from their own past, which is the usual finding for strategy timing. Fail with the
book equal to `tsmom12`: the pool holds no complement at all.

### Changes after the card

- 2026-11-18, Part A. Re-scores against the logged Sharpe: 32 of 35 agree to two decimals. `gbm`
  0.80 (logged 0.81), `gbm-wk` 0.81 (0.82), `gbm-pay` 0.70 (0.68): scikit-learn's boosting does
  not reproduce to the last digit across runs or versions. Nothing rests on those digits.
- 2026-11-18, Part A. Two tables beyond the card's list were added to the atlas after the first
  tables were seen: 2b (what the slots `tsmom12` leaves empty earned, by trend state) and the
  "gain share minus loss share" column of table 5. Both are descriptions; neither feeds Part B.
- 2026-11-18, before any Part B number. Three details the card left open or got slightly wrong,
  settled while writing `lib/deep1_mix.py`: (1) the weekly returns run from one Friday decision
  to the next, so that a week has one trend state; at a refit the week still running is left out
  (the card said "7-day blocks counted back from the day before the refit": the same data less
  at most a week). (2) In `meta`, a sleeve that starts later than the others (`absorption`, the
  ML models outside the six assets) has its earlier weeks filled with the average return of the
  other sleeves that week, so that its arrival does not throw away everyone's earlier history.
  (3) `switch` compares Sharpe ratios of weekly returns inside a state; a sleeve that sat in
  cash through a state scores 0 there, which beats a sleeve that lost money.
- 2026-11-18, before any Part B number. Component runs that were not in `tries.md` (a card's
  rule on a set it had not been run on: 4 on the ETFs and coins, 14 on the four-index
  portfolio) were logged as `robustness` under idea `deep-1` when the sleeves were built.
- 2026-11-18, before any Part B number. The first run of `deep1_combo.py check` crashed on a
  model that does not exist yet on the check day (`absorption` in 1999); the check now gives such
  a model no returns and no weights, as the full run does. Then all six days agreed.
- 2026-11-18, after Part B. Two reference points were added to `results/deep-1.md` once the
  three results had been seen: `naive-1n` (equal shares in every eligible sleeve; one run on the
  six assets, logged as `baseline` under `deep-1-meta`) and the hindsight ceiling (an in-sample
  fit on the sleeves' saved returns, no backtest, no row). Neither is a candidate.
- 2026-11-18, after Part B. The atlas first counted a window from the first day's own return;
  the harness counts from the first day's close. The atlas was switched to the harness's
  convention so that the two result files agree (stress windows and eras move by one day; the
  largest change is the covid window, `tsmom12` -22% instead of -24%). The figures in Part A's
  text were updated; no finding changed.
- 2026-11-18. The ideas-1 series are the primary `-and` variant of six cards plus the two
  fear-and-greed rules; card 10 (`trend3`) runs on three assets and is left out.
