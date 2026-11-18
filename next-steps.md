# Next steps

## Coin cap 4 (done 2026-11-18, branch `coin-cap-4`, draft PR #69 -> `coin-cap-3`)

**One-screen verdict for a human: `research/coin-cap-verdict.md`.** If a coin risk control is
wanted, the weekly `stop-0.25` on the coin slots, as a risk preference: on the six assets in the
coin years worst loss 36.5% -> 17.7%, days 10%+ under water 39% -> 22%, about 2 points of growth
a year over the full train (6 in the coin years). Not proven: 15 of 21 episodes against a
family bar of 17 of 21 (m = 15 coin-cap picks, p < 0.0067).

- Step 1 (descriptive, `lib/coin_cap4_modes.py`, logs nothing; `results/coin-cap-4-modes.md`):
  the weekly stop loses (a) in the first leg of fast falls while still fully in (exit at -44%
  in the six lost episodes, -38% in the first week), (b) where its volatility band is wide at
  hot tops (2017 summer: -44% in price), (c) by re-entering bounces (two or more re-entries:
  mean edge -3%). BTC: three different causes in four losses.
- Step 2 (card "Fifth reading", `lib/coin_cap4.py`, **a plain run logs 6 tries rows**; `DRY=1`
  logs nothing; `results/coin-cap-4.md`): by the card, no candidate meets the family bar and a
  25% cap adds nothing to the stop. `pstop` (price band 25%, matched on time held) 16 of 21
  (p 0.013), fixes the 2017 summer only, is looser on BTC/ETH (six-asset coin-years worst loss
  25.2%); `cap25+stop` 17.9% against 17.7% for 2.6 points less growth. Time under water: a cap
  never shortens it; the stops shorten the coin-fall mean (267 -> 207-222 days) but not the
  six-asset longest stretch (about 1,000 days for every series).
- Rebuild data: `research/data/bars` and `adj` (git-ignored price cache, as other lanes) and
  `research/macro.local.json` (copy the `.example`).
- Doing: nothing. No process running. Held-out year unspent.
- To decide (not for an agent): whether to open the rule PR for weekly `stop-0.25` on the coin
  slots as a risk preference, and whether to spend the held-out year on that one rule.
- Next (not started, card first; none is needed for the decision above): a stop that waits
  after an exit before re-entry (failure mode c), counted as pick 16; a coin-size choice framed
  as risk budget (worst loss target) rather than a tested edge; nothing argues for more rules on
  fast crashes (no close-based rule can act inside two days).

## Coin cap 3 (done 2026-11-18, branch `coin-cap-3`, draft PR #56 -> `coin-cap-2`)

Does checking `stop-0.25` daily (same as-of timing, no look-ahead) fix the fast-crash losses of
the third reading without whipsaw cost eating the gain? Card section "Fourth reading" in
`research/cards/coin-cap.md` (pushed before any number); write-up "Fourth reading" in
`research/coin-cap.md`; tables `research/results/coin-cap-3.md`.

**Verdict (by the card): the daily check does not fix the fast crashes; the weekly stop stays
the recommendation.** Two variants, same 21 episodes. `stop-0.25-d` (daily exit and re-entry)
beats its matched cap in 18 of 21 episodes (p 0.0007, meets the bar corrected for all 13
coin-cap picks), mean edge +20.5% against the weekly +16.2%, but turns around only 3 of the 6
episodes the weekly stop trailed (2017 summer, 2021-05; not BTC 2013-04, BTC 2013-14, XRP
2020-11): bar 2 fails. `stop-0.25-dx` (Friday re-entry) is weaker (16 of 21, 2 of 6). The
daily check does not make deepest losses smaller (raw, the same on average); it keeps more
return (cheaper re-entries) despite 2.4x the switches and fees, an edge that mostly goes at
double costs (+15.9% against +15.4%). BTC (post-hoc): the weekly stop loses there because the
first leg is faster than any close-based rule (2013-04), because it re-enters a sharp rebound
before a second leg down (2013-12, 2017-12), and because the twin's own exit is early enough
that a cap of it is hard to beat (2021-11). Held-out year unspent.

- Rebuild: `research/lib/coin_cap3.py` (**a plain run logs 6 tries rows**; `DRY=1` is a
  plumbing run on random prices, logs nothing). Needs `GRIMSTRADE_DATA` or
  `research/macro.local.json` (copy the `.example`).
- Found: coin-cap-2's 4 tries rows cover 2015-09-23 .. 2025-11-09, not 2013-02-10 (a double
  slice in `coin_cap2.portfolio`, fixed in code; rows not edited; its bar did not use them).
- Doing: nothing. No process running.
- For the owner (update to coin-cap-2's item): the daily check does not change the rule-PR
  recommendation by the card; if a rule PR comes, it is still weekly `stop-0.25` on the coin
  slots, a risk choice. Two things to weigh first: (1) counted against all 13 coin-cap picks the
  weekly stop's episode edge is no longer significant (p 0.039 against 0.0077), so the case is
  weaker than coin-cap-2 read it; (2) the daily-checked stop is the only series that meets the
  corrected bar, but its gain is cost-matched return, not shallower losses, it is fee-sensitive,
  and on the six assets cointop-1's all-daily stop was worse than weekly (Sharpe 1.05 against
  1.09, worst loss 30.9% against 28.9%). Switching to daily would need its own card (and the
  held-out year, only if the owner asks).
- Next (not started, card first): a stop whose band does not loosen after a crash (price
  drawdown instead of volatility units) for the rebound re-entries; cap 25% together with
  `stop-0.25`; time under water.

## Coin cap 2 (done 2026-11-18, branch `coin-cap-2`, draft PR #53 -> `coin-cap`)

Does the stop's edge over a cap of the same cost hold across many independent coin falls, or is
it the one 2018-20 fall? Card section "Third reading" in `research/cards/coin-cap.md` (written
before any number); write-up "Third reading" in `research/coin-cap.md`; tables
`research/results/coin-cap-2.md` and (post-hoc, not in the bar)
`research/results/coin-cap-2-posthoc.md`.

**Verdict (by the card's bar): rule PR candidate, for the owner.** 445 coin falls (60% or more)
on 197 coins of breadth-1's book, 2013-2025, in 21 episodes (effective 7.6; 10 calendar years).
Against a cap of matched cost (0.663 of the slot: same mean return, about the same
volatility), the stop's deepest loss is smaller in 15 of 21 episodes (sign p 0.039), +16% of a
slot on average, +15% without the largest episode, and in 9 of 10 years. Not a one-episode
effect. Caveats for the owner: it loses in fast crashes (2013-04, 2017 summer, 2021-05: a
weekly stop cannot act inside days); on BTC alone it is behind a matched cap in 4 of 5 falls
(ETH: ahead in 6 of 6); pooled Sharpe is unchanged (0.46 vs 0.47), so this buys a shallower
worst loss for the same growth, not more return. Held-out year unspent.

- Rebuild: `research/lib/coin_cap2.py` (**a plain run logs 4 tries rows**; `DRY=1` is a
  plumbing run on random prices, logs nothing) and `research/lib/coin_cap2_posthoc.py` (logs
  nothing).
- Doing: nothing. No process running.
- For the owner: whether to open a rule PR putting `stop-0.25` on the coin slots of `tsmom12`
  (cointop-1 Part C: worst loss 36.5% -> 28.9%, about 2 points less growth a year; coin years
  17.7% against 21-27% for caps of similar cost). Before such a PR: decide whether the BTC
  result (1 of 5 falls) matters, and whether to spend the held-out year on it (the card spends
  it only if the owner asks). **Updated by coin-cap-3 above:** the daily check does not change
  this; counted against all coin-cap picks the weekly stop's episode edge is not significant.
- Next (not started, card first): a daily-read stop for the fast crashes is already known not to
  help Sharpe (cointop-1, daily rows); cap 25% together with `stop-0.25`; time under water.

## Coin cap (done 2026-11-18, branch `coin-cap`, draft PR #49 -> `cointop-1`)

Is a plain cap on the combined coin weight inside `tsmom12` as good as cointop-1's `stop-0.25`
at cutting the worst loss, at less cost in growth? Card `research/cards/coin-cap.md` (written
before any number); write-up `research/coin-cap.md`; tables `research/results/coin-cap.md`.
Every cap from 10% to 25%, the walk-forward stitch and the stop all have the same worst loss,
28.9%: the 2000-02 dot-com fall, not a coin number. On that number `cap25` is cheaper (1.0 to
1.1 points of CAGR a year against the stop's 2.2). Inside deep-1's coin-crash windows the stop
is better than any cap of the same cost (-72% summed against -110% for `cap20`). Sharpe is
inside noise everywhere. The card's bar is not met (Sharpe bar fails; worst loss is a tie).
Held-out year unspent.

Second reading (card section dated 11:18 UTC, `research/results/coin-cap-years.md`): on the coin
years only (2013-25) the tie breaks and the stop wins. Worst loss: stop 17.7%, `cap20` 21 to
23%, `cap25` and `cap-wf` 27.2%, `tsmom12` 36.5%. No cap with at least the stop's growth
matches it; a 15% cap to cash does (17.2%) for 3.8 points of CAGR a year more than the stop.
The gap is mostly the long 2018-20 fall, so it is close to one observation.

- Rebuild: `research/lib/coin_cap.py` (**a plain run logs 18 tries rows**) and
  `research/lib/coin_cap_years.py` (**logs 1 row**); do not rerun them with logging. `DRY=1`
  is a plumbing run that logs nothing.
- Doing: nothing. No process running.
- Next (not started, card first): cap 25% together with `stop-0.25`; time under water.

## Cointop 1 (done 2026-11-18, branch `cointop-1`, draft PR #40 -> `deep-1`)

`tsmom12` is slow out of coin tops. Coin tops studied on breadth-1's top-100 coin book; one
setting for each of three exit rules chosen there by a fixed procedure (BTC, ETH and the six
other test coins left out), then carried unchanged to BTC/ETH through the gym. No rule passes.
The coin book has 639 tops in about 19 separate months; the 12-month rule leaves a median 106
days after a top, at -52%. Chosen: `stop-0.25`, `fade-28`, `breadth-28`; none meets the coin
book's works-there bar (p 0.55, 0.103, 0.14) or beats its 26-weeks-late control. On the six
assets: Sharpe 1.09, 1.09, 1.08 against 1.05 (p about 0.3), worst loss 29-30% against 36.5%,
1 to 2 points less growth a year; nothing on the six other coins. A smaller coin position, not
a better rule. Held-out year unspent. Write-up `research/cointop-1.md`; tables
`research/results/cointop-1-coins.md` (Parts A, B), `research/results/cointop-1.md` (Part C).

- Rebuild: `research/lib/cointop1.py` (coin book) and `research/lib/cointop1_carry.py` (gym).
  **Both log tries rows on a plain run** (`cointop1.py` only with `--log`); do not rerun them
  with logging. `DRY=1` on the carry script is a plumbing run that logs nothing.
- Doing: nothing. No process running.
- Next lanes (not started): none needed from this one. A card for windows shorter than 28 days
  would be the only follow-up, and Part C says not to expect more than a risk choice from it.

### For the owner

- Nothing to decide. If a worst loss near 29% instead of 36.5% is wanted for 1 to 2 points less
  growth a year, `fade-28` on the coin slots is one more way to buy it (next to `trend-vol`
  and the presets in `research/risk-map.md`).

## Deep 1 (done 2026-11-18, branch `deep-1`, draft PR #36 -> `carry-2`)

Why does each tested model fail where it fails, and does a mix chosen from past data beat
`tsmom12`? No mix passes: `stack` 1.01, `switch` 1.02, `meta` 1.08 against 1.05 (1994-2025); the
best equals a plain average of all models (1.06), and even the best fixed mix with hindsight
reaches only 1.22. The models are the same six assets held at different sizes; they lose in the
same weeks. Failure atlas: 52 series, six failure modes (slow out of coin tops; missing the
rebound; one long bear market for always-invested rules; boosting models short of Bitcoin; RL as
a geared coin position; early-exit gates paying for 2023-24). Held-out year unspent. Write-up
`research/deep-1.md`; tables `research/results/deep-1-atlas.md`, `research/results/deep-1.md`.

- Rebuild: `research/lib/deep1_models.py <universe>` (series into `<cache_root>/derived/deep-1/`),
  `deep1_atlas.py`, `deep1_combo.py` (`check` = look-ahead check; a plain run reuses the cached
  replays and logs nothing twice).
- Next lanes (not started; detail in `research/deep-1.md`): a breadth-gate card judged on other
  universes (agree the split with `trend-tune` first); coin tops on the top-100 coin book; carry
  as the first real complement, with deep-1's `stack` rule unchanged, after carry-3.

### For the owner

- Nothing to decide. If you want a smoother ride, the plain average of all rules and `trend-vol`
  both give a worst loss near 30% instead of 36.5%, for about 3 points less growth a year. That
  is a choice of risk, like the presets in `research/risk-map.md`, not a better rule.

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
