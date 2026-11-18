# Next steps

## Wide 7 (done 2026-11-18, branch `wide-7`, draft PR #81 -> `wide-6`)

Three event-study gates (rule, script and tests pushed before any number; one dry run with
counts only, then one run each), then two new mechanisms. **All three gates fail; no card, no
strategy, no `tries.md` row; held-out year untouched.** Write-up `research/wide-7.md`; tables
`research/results/wash-sale-echo.md`, `festival-gold.md`, `rmd-december.md`.

- W14 `wash-sale-echo` (tax law): 21 ETFs, return over days 31-45 after the third Friday of
  December on the November loss: -0.003 (t -0.07) 1994-2011, +0.023 (t 0.43) 2012-2024; coin
  placebo above the ETFs. Dead. Shown, not gating: a turn-of-year loser rebound after 2012 (t
  3.9 by year clusters, but a placebo window also reaches |t| 2.5-4: fragile).
- W13 `festival-gold` (anthropology): GLD 15 sessions before Dhanteras / Lunar New Year minus
  the month's mean: -1.9 bps a day (t -0.30), rank 10 of 15 shifts. Dead. Baur's autumn
  effect reversed after 2010.
- W12 `rmd-december` (demography): SPY late December in the RMD waiver years 2009 and 2020:
  -0.06% vs other years (p 0.51). Dead.
- New W16 `geomagnetic-storm` (heliophysics), W17 `fork-premium` (software release
  engineering) in `research/wide-1.md`, last section.

Count: 70 mechanisms, 16 tested by a strategy, none passed. The next strategy test is read at
p < 0.10 / 70 = 0.00143. Gates so far: 6, all failed.

- Doing: nothing. No process running.
- Next: (1) W16 `geomagnetic-storm` gate: the only queued entry whose post-sample years are
  inside train (2003-2025); needs the GFZ Kp/Ap file (check keyless access). (2) W15
  `cat-claims` gate (HURDAT2 landfalls, LQD vs TLT). (3) If the turn-of-year ETF loser
  rebound is wanted, pre-register it for the 2026 turn (tax year 2025 needs bars after train)
  rather than test it on the years that suggested it.
- Data: none added. A fresh worktree needs the price cache in `research/data/` (copy from
  another worktree or `research/lib/fetch.py`) and `research/macro.local.json`.

## Wide 6 (done 2026-11-18, branch `wide-6`, draft PR #76 -> `wide-5`)

Two event-study gates (ann-1's method: rule pushed before any number, no card unless the raw
effect exists in- and post-sample), then four new mechanisms for the queue. **Both gates fail;
no card, no strategy, no `tries.md` row; held-out year untouched.** Write-up
`research/wide-6.md`; tables `research/results/critical-slowing.md`, `research/results/lunar.md`.

- W11 `critical-slowing` (ecology/physics; Scheffer et al. 2009, Guttal et al. 2016, Diks,
  Hommes, Wang 2019): chance of a top-decile quarterly drawdown on a year's Kendall trend of
  rolling AC1 and variance, six assets pooled, volatility level controlled, Driscoll-Kraay t.
  AC1 t 1.4 (to 2015) and 0.1 (2016 on); variance -0.5 and 1.8 (raw, without the control,
  1.2 and 2.1). Only last month's volatility predicts (t 3.8). Dead by the gate.
- W3 `lunar` (Yuan, Zheng, Zhu 2006): SPY 2007-2025 new-moon minus full-moon days +1.6 bps a
  day (t 0.43), rank 12 of 29 phase shifts; the paper's years +3.1 (t 1.3) on the S&P 500.
  Dead by the gate (which could only see about 7 bps a day).
- New W12-W15 in `research/wide-1.md` (last section): `rmd-december` (demography),
  `festival-gold` (anthropology of lunisolar calendars), `wash-sale-echo` (tax law),
  `cat-claims` (catastrophe meteorology), each with a dose and the unseen years that can
  judge it.

Count (union of the wide and survey lines, which forked at wide-4 and each missed the other):
68 mechanisms, 16 tested, none passed. The next strategy test is read at p < 0.10 / 68 =
0.00147.

- Doing: nothing. No process running.
- Next: (1) W14 `wash-sale-echo` as an event-study gate (cached prices only; coins are the
  placebo). (2) W13 `festival-gold` gate on GLD (dates from `research/lib/wide6_rules.py`'s
  moon code, checked against a published table). (3) Merge the count: any lane branching from
  `wide-6` or `ann-1` should carry 68 / 16 forward.
- Data: none added. A fresh worktree needs the price cache in `research/data/` (copy from
  another worktree or `research/lib/fetch.py`) and `research/macro.local.json`.

## Wide 5 (done 2026-11-18, branch `wide-5`, draft PR #71 -> `wide-4`)

Two new mechanisms from queueing and control theory, picked by a written six-point choice
rule; choice note, cards, code and the step 3 questions were each pushed before any number.
**Both fail train; held-out year unspent.** Write-up `research/wide-5.md`; tables
`research/results/dealer-backlog.md`, `extension-dose.md`, `wide-5-deeper.md`; 6 rows in
`tries.md`.

- `dealer-backlog` (W9): idle cash into TLT for five sessions after 20/30-year auctions with
  an above-normal primary-dealer share: 1.02 vs 1.05 (-0.026, p 0.95). TLT after such
  auctions -13 bps vs +6 after the others; slope t -1.0 (wrong sign for the recovery story).
- `extension-dose` (W10): month-end TLT window only in high index-extension months: 1.06 vs
  1.05 (+0.013, p 0.19, 2 of 4 eras). Slope t 0.8; high-low gap +46 bps before 2014, -3
  after; the whole book gain is 2008-09. Not consistent with an index-buying flow.

Count: 56 mechanisms (46 listed + W1-W10), 14 tested, none passed. The next test is read at
p < 0.10 / 56 = 0.00179 (lower if more are added first).

- Doing: nothing. No process running.
- Next: (1) Treasury forced flows are now spent (four tested with doses or regimes, none
  supported); do not add another. (2) If a published calendar effect is wanted, W3 `lunar` is
  the only listed entry with post-sample years (2007-2025): an event study gate as ann-1 did,
  no strategy unless t >= 2 after publication. (3) Any idle-cash-into-TLT overlay should
  report its result without 2008-09 first: that is where these +0.01s come from.
- Data added (git-ignored cache): the auction file with dealer and competitive awards
  (`<cache_root>/downloads/wide-5/treasury-auctions/`), parsed to
  `derived/wide-5/auctions.csv` by `uv run python -I research/lib/wide5_auctions.py`.

## Wide 4 (done 2026-11-18, branch `wide-4`, draft PR #57 -> `wide-3`)

W2 `tax-drain` from the list, then five new mechanisms from unused fields and a test of the
best one. Fact check, choice note, cards and code were each pushed before any number. **Both
tested ideas fail train; held-out year unspent.** Write-up `research/wide-4.md`; tables
`research/results/tax-drain.md`, `research/results/coupon-dose.md`; 7 rows in `tries.md`.

- Fact (NY Fed, Santoro 2012): tax receipts sat in bank TT&L accounts with the Fed's account
  held near $5 billion until fall 2008; from 2008-12 the cash goes to the Fed. wide-3's date
  was right; the source adds that the drain only matters when reserves are scarce.
- `tax-drain` (W2, hydraulics): SPY, QQQ, TLT out for five sessions around each tax date
  from 2008-12-16: 1.03 vs 1.05 (-0.016, p 0.88). The drain is real (Treasury's Fed account
  +88 $bn over D-2 .. D+1 since 2008, t 13.7; +1 $bn before). Prices: right sign, right order
  by regime (SPY -62 bps while the Fed shrank reserves, t -1.3; ~0 before 2008), too weak.
- New W4-W8 in `research/wide-1.md` (last section): `coupon-dose` (pharmacokinetics),
  `tidal-trigger` (seismology), `payday-inflow` (actuarial science), `fatigue-damage`
  (materials fatigue), `snapshot-shrink` (metrology).
- `coupon-dose` (W4, picked): idle cash into TLT for four sessions when the Treasury's net
  payment on the 15th is positive: 1.04 vs 1.05 (-0.011, p 0.71). Positive-dose days +2 bps
  vs +18 on the others; wrong sign since 2014.

Count: 54 mechanisms (46 listed + W1-W8), 12 tested, none passed. The next test is read at
p < 0.10 / 54 = 0.00185.

- Doing: nothing. No process running.
- Next: W5 `tidal-trigger` is the only W entry with a prior above 1%, and it must be checked
  on a calendar not used to suggest it (forward, or the tax-date drain in future
  scarce-reserve years). Forced Treasury flows are now spent for this book. The `tax-drain`
  event study is worth re-running forward as a descriptive check, not as a trade.
- Data added (git-ignored cache): Daily Treasury Statement cash balances
  (`<cache_root>/treasury/dts-2026-11-18/`, parsed to `derived/wide-4/tga.csv`), the auction
  file with rates and amounts (`downloads/wide-4/treasury-auctions/`, parsed to
  `derived/wide-4/payments.csv`). FRED refuses automated downloads from this machine.

## Wide 3 (done 2026-11-18, branch `wide-3`, draft PR #54 -> `wide-2`)

Two more picks from wide-1's list, then three new mechanisms and a test of the best one. Choice
note, cards and code were each pushed before any number. **All three tested ideas fail train;
held-out year unspent.** Write-up `research/wide-3.md`; tables `research/results/`; 8 rows in
`tries.md`.

- `hedge-regime` (F2, stock-bond correlation as order parameter: keep TLT out of trend while
  it hedges): 1.05 vs 1.05 (+0.003, p 0.39); other ETFs -0.006. One sign flip (2023).
- `attention-peak` (P2, SIR on English-Wikipedia page views: leave a coin after its attention
  peak): 1.02 vs 1.05 (-0.03); other coins 0.33 vs 0.54. Caught 2017-12, wrong in 2021.
- `opex-pin` (new W1, option-expiry week, idle cash into stocks): 1.01 vs 1.05 (-0.04), behind
  its placebo week. SPY expiry week vs average week: -0.3 bps (t 0.0, 381 weeks).
- New, untested, with test plans in `research/wide-1.md` (last section): W2 `tax-drain`
  (reserve drain on tax dates, 1994-2007 as placebo), W3 `lunar` (lowest prior).

Count (corrected): wide-1's list has 46 entries; 10 cards now cover 11 of them plus one new
mechanism; 35 listed entries uncarded (wide-2's "39" counted cards, not entries). With the 3
new ones the family is 49; the next test is read at p < 0.10 / 49.

- Doing: nothing. No process running.
- Next: W2 `tax-drain` as an event study first (check when Treasury receipts moved from
  commercial-bank accounts to the Fed before writing its placebo). Of the 35 listed entries
  left, none has a better prior than the failures so far; the list looks exhausted for this
  book.

## Wide 2 (done 2026-11-18, branch `wide-2`, draft PR #47 -> `wide-1`)

One mechanism picked from the 42 that wide-1 listed and did not card: Q5, trend age (hazard
rate). Rule `age4`: hold a `tsmom12` slot only once the signal has been on for four Fridays.
**Fails train: 0.99 against 1.05 (difference -0.06, 90% range -0.11 to -0.01), behind in all
five eras; held-out year unspent.** Short spells are common (50 of 111 end within four weeks)
but cheap; the three missed weeks of lasting trends cost more. Write-up `research/wide-2.md`;
table `research/results/trend-age.md`; 7 rows in `tries.md`.

Second pick, same day: E6, patch-leaving (marginal value theorem). Rule `mvt`: the twin's
exposure, held only in the in-trend assets whose risk-scaled 12-month return is at least the
average. **Fails all five bars: 0.85 against 1.05 (difference -0.19, 90% range -0.36 to
-0.02), drawdown 53% against 37%, turnover 9.7 against 2.7; held-out year unspent.** Table
`research/results/patch-leaving.md`; 4 rows in `tries.md`. Both picks were read at
p < 0.10 / 42.

Third pick, same day: G2, crowded-trend (halve the book when at least three assets are eligible
and all are in trend). **Fails: 0.98 against 1.05 (difference -0.07, 90% range -0.16 to
+0.03), ahead in 1 of 5 eras; held-out year unspent.** Drawdown 29% against 37%, but 3 points
less return a year. Table `research/results/crowded-trend.md`; 4 rows in `tries.md`.

- Doing: nothing. No process running.
- Next: nothing from the three cards. 39 of wide-1's mechanisms stay uncarded; three price-only
  changes to the trend rule have now failed. wide-1's three lanes below stand as written.

## Wide 1 (done 2026-11-18, branch `wide-1`, draft PR #33 -> `carry-2`)

New hypotheses from ten other fields (ecology, epidemiology, signal processing, control,
information theory, game theory, physics, queueing, neuroscience, immunology). 46 mechanisms
sorted before any number; 33 collapse into ideas already killed; four got a card, each a bet on
someone else's mechanical trading. **All four fail their pre-set bar on train; held-out year
unspent.** Write-up `research/wide-1.md`; tables `research/results/`; 39 rows in `tries.md`.

- `auction-concession` (TLT out before 20/30-year Treasury auctions): book +0.01 over `tsmom12`
  (p 0.14). The dip is in TLT's closes (-34 bps, t 2.5) but half is lost at next-open fills;
  IEF goes the other way. Faint lead.
- `rebalance-pressure` (halve the month's stock/bond leader in the last five sessions): book
  -0.005. The raw spread has the predicted sign; not confirmed on 1962-2003 data.
- `contagion-catchup` (21 ETFs, hold those whose relatives moved and which did not): dead, 0.50
  vs 0.60. Relatives' moves do not spill over; plain one-week reversal is all there is.
- `vol-echo` (hold stocks when a shock leaves the 21-day volatility window): dead, SPY 0.25 vs
  0.63; the pre-2010 placebo looks the same.

Found after the tests (a hypothesis, not a result; `research/results/wide-1-yields.md`): long
bonds earned almost all their return in the last four sessions of each month (TLT +39 bps,
t 4.3, 2003-2025, both halves; +32 at next-open fills; from yields: nothing before 1990, +13
to +23 bps in 1990-2003).

Next lanes (each needs its own card; details at the top of `research/wide-1.md`):

1. `month-end-bonds`: idle cash into the long bond for the last four sessions of each month.
   Clean tests left: LQD (not looked at), TLT's first year, the held-out year once, forward paper.
2. A volume screen: the six assets' own trading volume has never been screened.
3. The month-end stock bounce after a bad month, with a mid-month placebo first.

### For the owner

- Nothing to change in the paper system.
- `month-end-bonds` would spend the held-out year on a pattern found by looking, not by a card.
  That is allowed only through a new card; whether to spend the year on it is your call.
- Flow effects of this size (15-40 bps per event) only pay with futures and modest leverage:
  the same broker gap the carry lead ran into.
- Two effects here are worth more at the close than at the next open (the auction dip keeps 45%
  at our fills, the month-end bond rally 83%). Whether the paper broker should be able to fill
  at the close is a design question.
- Paid data noted, nothing bought: token unlock schedules (price not checked).

## Carry 2 (done 2026-11-13, branch `carry-2`, draft PR #26 -> `short-1`)

Short-1's carry book, copied unchanged, on data it never saw: Binance perps outside the 30
(delisted included), Bybit, Hyperliquid (~550 coins, 2021-2025, 10 bps + every funding event).
Weak replication by the card: `ls-funding` passes all four bars (pooled Sharpe 0.69, p 0.04;
blend 0.37 vs twin 0.20, p 0.04; positive on every venue and era); `ls-premium`, the lead, does
not (pooled 0.44, p 0.15). Smaller than on short-1's 30 coins, a funding harvest with beta hedged
out, gone at 30 bps (turnover ~42x a year). Held-out year unspent (card: only if `ls-premium`
replicates). Write-up `research/carry-2.md`. Owner options: a cost card (real fills on small
perps, slower rebalance) or a held-out-only card for pooled `ls-funding`; neither matters while
the paper system stays long-only BTC/ETH on spot.

## Short 1 (done 2026-11-13, branch `short-1`, draft PR #23 -> `breadth-1`)

A short side on Binance USDT perps (30 pairs and BTC/ETH, 2020-2025, 10 bps + every funding
event): nothing passed. `tsmom12` that goes short in downtrends trails long-only (0.73 vs 1.03
spot on 30 coins; 0.76 vs 1.19 on BTC/ETH). Longs on perps paid ~12% a year in funding.
Dollar-neutral low-vol/size/turnover books lose (short legs of wild coins in the 2020-21 rally).
Near miss: a premium/funding carry book (short the most expensive perps), blend with `tsmom12`
1.25 vs 1.03 at 10 bps, but not at 30 bps. Held-out year unspent. Write-up `research/short-1.md`.
Owner options: a held-out-only carry card, or keep long-only BTC/ETH (recommended).

## Breadth 1 (done 2026-11-13, branch `breadth-1`, draft PR #22 -> `info-1`)

Wide books and hourly frequency, after 30 bps costs. One pass: in the wide Coin Metrics coin book
(top 100, dead coins included, 2019-2025), tilting toward low volume-to-market-cap coins inside
the trend rule lifted Sharpe from 0.72 to 1.06 (held-out year 0.61 against 0.31). It did not carry
over to the 30 liquid Binance pairs, and it stays below plain BTC `tsmom12` (~1.16), so it is
no case for widening the crypto slot. The 33-market pool and the hourly BTC/ETH rules add nothing
(hourly reversal is real, IC ~-0.08, but the costs are ten times the edge). Write-up
`research/breadth-1.md`. Open owner options: a short-side card on perpetuals with funding costs,
or a coin-book RL agent behind rl-3's gate. Neither matters while the paper system stays on
long-only BTC/ETH.

## Info 1 (done 2026-11-13, branch `info-1`, draft PR #21 -> `rl-3`)

23 new inputs (COT, Cboe options/vol and put/call, crypto funding/basis/DVOL, on-chain, Fear &
Greed, cross-asset) screened for weekly IC: none useful (best walk-forward gain over the trend
inputs +0.025; one candidate above chance in sample). Write-up `research/info-1.md`. Open
options for the owner: more independent bets (30 Binance perps, 33-market pool), a wider action
(short side), or a slower-horizon (4/13-week) screen as a new card.

## M0 status: built, not yet proven live

Done: template scaffold, data ingest (BTC, ETH, SPY, QQQ, GLD, TLT, append-only CSV), gym
(next-open fills, fees, slippage, long-only, 10,000 USD), 4 benchmark strategies, append-only
ledger + tries counter + git-history integrity check, daily runner + `.github/workflows/daily.yml`,
scoreboard (`python -m grimstrade.report --root trail [--backtest]`), owner README, MIT license.

## To finish M0 (needs someone with GitHub access)

- [ ] Merge this branch to `main` (via PR), then run "Daily paper trading" once by hand
      (workflow_dispatch). Unverified live: Kraken/Coinbase/Yahoo/Stooq formats are from docs,
      tested only on fixtures (dev container can't reach them). Yahoo may 429 from Actions; Stooq is
      the fallback. Check the first run creates the `paper-trail` branch and pushes to it.
- [ ] Check the Actions settings allow GITHUB_TOKEN write (contents: write is requested).
- [ ] If the `protect-main` ruleset is ever widened to all branches, exempt `paper-trail`
      (the bot pushes there directly).

## Assumptions (see docs/DECISIONS.md)

- CSV + stdlib only (no parquet/pandas). Raw prices; dividends not credited yet.
- Bot commits to orphan branch `paper-trail` because `main` requires PRs.
- Costs: crypto 25 bps fee + 5 bps slip; ETFs 0 fee + 2 bps slip; 1% rebalance band.
- Decisions at ~22:30 UTC see crypto bars through yesterday (today's still open) and ETFs through
  today. Fills show up a day later, once the fill bar has closed and been stored.
- A run with no new data since a strategy's last decision writes no new decision.
- Gymnasium env wrapper deferred (BACKLOG).

## M1 (next)

Classic strategies live in paper (time-series momentum, cross-sectional momentum, vol targeting,
risk parity, crypto mean reversion), each registered in `ledger/tries.jsonl`; deflated Sharpe in
the scoreboard; weekly one-screen summary for the owner.

## Macro 1 (research run, branch `macro-1`, started 2026-11-13 ~01:40 UTC)

Brief: `chief-of-staff/briefs/grimstrade-macro-1.md`. Question: does knowing the macro phase
(Fed policy, real rates, yield curve, money supply, credit spreads, the Bitcoin halving cycle)
add anything over `tsmom12`? Write-up: `research/macro-1.md`.

- Done: look-ahead-safe macro layer (`research/lib/macro.py`, ALFRED vintages; tests in
  `tests/test_macro_asof.py`), protocol section "Macro tests", six cards tested on train, all
  fail their bar (halving: passes on numbers but fails bar 2 and is not believed: three winters,
  folklore window). Feature skill table, write-up `research/macro-1.md`. Held-out year unused.
  Draft PR #16 (`macro-1` -> `research-3`), not merged.
- Doing: nothing.
- Next: macro features as regime inputs for the RL agent (list in `research/macro-1.md`). The
  owner may want to read the halving section before anyone trades a "four-year cycle".

## RL 1 (research run, branch `rl-1`, started 2026-11-13 ~01:50 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-1.md`. Question: can an RL agent (PPO, policy shared
across assets, prices + macro inputs) beat `tsmom12` out of sample? Plan and results:
`research/rl-1.md`; rules: `research/protocol.md` "Reinforcement-learning tests".

- Done: plan and protocol section before code; gym-exact batched simulator and environment
  with tests; 5 agents x 10 seeds x 13 walk-forward folds trained on the RTX 5080; evaluated
  through the real gym, 70 rows in `research/tries.md`; tables `research/results/rl-1.md`;
  write-up `research/rl-1.md`. Answer: no. All five fail (Sharpe 0.57-0.71 against
  `tsmom12` 0.99 out of sample 2000-2025, 0 of 50 seeds ahead). Held-out year unused.
  Draft PR #17 (`rl-1` -> `macro-1`), not merged.
- Doing: nothing. No process running.
- Next (not started): residual-policy rung (tsmom12 plus a bounded tilt, reward relative to
  tsmom12, coin cap); card and bar first. Details in `research/rl-1.md`, "What the next rung
  would need".

## RL 2 (research run, branch `rl-2`, started 2026-11-13 ~05:05 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-2.md`. Question: does an RL agent constrained to tilt
`tsmom12` (residual policy, active reward, early stopping, one variant pooled over 33 markets)
beat `tsmom12` out of sample? Plan and results: `research/rl-2.md`; rules: `research/protocol.md`
"Residual RL tests".

- Done: residual environment + tests (zero tilt == `tsmom12` exactly), trainer with purged
  validation and early stopping, on-chain inputs for coins (`research/lib/onchain.py`, as-of
  test), 4 variants x 10 seeds x 13 folds, evaluated through the gym, 56 rows in
  `research/tries.md`, tables `research/results/rl-2.md`, write-up. Answer: no. All four fail
  (Sharpe 0.96-0.98 against 0.99; active share 1.8-2.7%; at most 1 of 10 seeds ahead).
  Held-out year unused. Draft PR #18 (`rl-2` -> `rl-1`), not merged.
- Doing: nothing. No process running.
- Next (not started): planted-signal control of the residual pipeline (can it find a known
  weak signal?); then funding rates / basis for coins, which need shorting or futures in the gym.

## RL 3 (research run, branch `rl-3`, started 2026-11-13 ~05:30 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-3.md`. Question: is RL 2's null the inputs or the
learner? A known weak signal (IC 0.00-0.20) was planted into one input of RL 2's residual
environment, to see at what strength the same pipeline beats `tsmom12`. Card and results:
`research/rl-3.md`; rules: `research/protocol.md` "Planted-signal controls".

- Done: card before code, planted input with tests, 10 planted configurations + 4
  pre-registered diagnostics x 10 seeds x 13 folds, ceiling rules, a post-hoc supervised check,
  183 `control` rows in `research/tries.md`, tables `research/results/rl-3.md` and
  `research/results/rl-3-inputs.md`, write-up. Answer: the pipeline finds only 0.20 (capturing
  9-21% of its +0.45 ceiling) and misses 0.10 (worth +0.16). More budget or no early stopping
  does not help; least squares misses it too, so the cause is too many noisy inputs for the data.
  Real inputs: weekly IC at most ~0.05 alone and ~0 together, below the 0.10 at which even a
  perfect learner gains anything on this book. Both limits are real; the inputs bind first.
  Held-out year unused. Draft PR #19 (`rl-3` -> `rl-2`), not merged.
- Doing: nothing. No process running.
- Next (not started): (1) gate every learner change on "finds 0.10 in the planted control" (few
  inputs, shrinkage, pooled books); (2) screen new inputs (funding/basis, open interest,
  minute-bar features, VIX term structure) with a cheap weekly-IC table before any RL run.
