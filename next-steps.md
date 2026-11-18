# Next steps

## Evo 2 (IN PROGRESS 2026-11-18 from ~19:40 UTC, branch `evo-2` from `evo-1`)

Redesign of evo-1 after its planted control failed. Card: `research/cards/evo-2.md` (committed
before any evo-2 number): 8 inputs, fitness on six-asset days only, 12 nodes, one fixed greed
(500 x 10, penalty 0.02), plant calibrated per world to ceilings 0.8 (gate) and 0.5. Chain:
controls (noise 31-33 must be 0 of 3; plant 0.8 on 34-36 found in >= 2 of 3) -> 40 replays
(201-240) -> one real search on train -> verdict. Doing: implementing the card.

## Evo 1 (STOPPED 2026-11-18 ~19:35 UTC: the search fails its planted control; close or redesign, branch `evo-1`, draft PR #44 -> `carry-2`)

Question: can a genetic-programming search over trading rules find anything that beats `tsmom12`
once it is charged for its luck (walk-forward selection, a full-search replay test, out-of-universe
sets)? Card: `research/evo-1.md`; rules: `research/protocol.md` "Evolved-rule search tests".

- Done, burst 1: card, protocol section, `evo_stats.py` (Reality Check, SPA), `evo_gp.py`
  (grammar, GP), `evo_smoke.py` (toy world), `evo_feat.py` (the 72 inputs). Toy finding: an SPA
  over the rules a GP visited passes pure noise (p <= 0.006 in 4 of 4), so bar 3 became the
  **full-search replay test** (lead, 2026-11-18 ~11:15 UTC, on the card before any real number):
  pass only if none of 20 replay worlds is at or above the real score, or 40 worlds with at
  most one, chosen at the timing test.
- Done, burst 2 (2026-11-18 ~18:30-19:30 UTC), all in `research/lib/`, tests in `tests/`:
  - `evo_score.py`, the fast scorer (`test_evo_score.py`): within 0.04 Sharpe of `gym.simulate`
    on 16 fixed rules (measured 0.028), growth within 0.4 points, daily correlation > 0.995;
    models cash-limited weekend coin buys.
  - `evo_world.py` (shuffle / block-bootstrap worlds, zero log or zero mean simple return, the
    plant `H`) and `evo_wf.py` (walk-forward driver: 14 fits x 5 GP runs, candidates,
    `evo-top1` / `evo-ens10` / `evo-val`, gym replay; commands `timing`, `ceilings`, `control`,
    `baselines`, `replay`); `test_evo_wf.py`.
  - Timing (card, "Bar 3, replaced"): one walk-forward search ~0.04 CPU-hours; the whole plan
    ~2.1 CPU-hours with 40 replays. No halving.
  - Lead's decisions (card note, "Lead's decisions", committed before any replay): control
    worlds with zero mean simple return; 40 replays (seeds 101-140, at most one at or above);
    then the real search if the controls pass. Replay worlds stay zero log return (the note
    says why).
  - Controls, first run (zero log drift, superseded): planted found, noise 1 of 3, but equal
    weight earned 0.32-0.47 in noise (the holding premium).
  - **Controls after the fix** (27 rows, `research/results/evo-1.md`): **noise found in 0 of
    3; planted not found at any strength** (k=0.04: 0.10 / 0.19 / 0.27 against a ceiling of
    0.72). Diagnostic: at 12 of 14 fits the search's best in-sample fitness beats `H`'s own,
    i.e. it overfits past the true rule. By the card a real fail would read "too weak to
    tell".
- Lead's decision 2 (card note, before any tuning number): tune the greed on fresh synthetic
  worlds (grid A-F: node penalty 0.01/0.03/0.06 x 30/10/5 generations), pick by a rule written
  in advance, confirm on fresh worlds. Done 2026-11-18 ~19:22-19:29 UTC (94 `control` rows):
  no setting found the plant on tuning world 11; the rule picked D (0.01, 5 generations);
  **confirmation on worlds 21-23 failed** (noise 0 of 3, plant not found: -0.10 / -0.11 / 0.11
  against a ceiling of 0.24). So by the note: **no replay, no real search.** Tables in
  `research/results/evo-1.md`; reading at the top of `research/evo-1.md`.
- **Verdict: the search cannot find a planted rule at any tested greed** (ceiling 0.72 in world
  1, 0.22-0.24 in worlds 11 and 21). Doing: nothing. No process running. Held-out year
  untouched. No replay world, real-data search or real-data number of evo-1 exists.
- **Proposal for the lead: close the lane** (recommended), or redesign as a new card:
  - Close: on this data a free rule search over 72 inputs cannot tell even a planted 0.2-0.7
    Sharpe rule from its own luck; a real edge over `tsmom12` would be smaller still. Same
    lesson as rl-3 (too many noisy inputs for the data). Keep `evo_score.py` (a gym-exact
    weekly scorer, ~0.4 ms a rule) and `evo_world.py` for other lanes.
  - Redesign (only with a new card, the gate first): far fewer inputs (e.g. the 8 trend
    lookbacks and 2 volatility ones), fitness on the six-asset days only (now half the window
    is the index alone, where cross-asset inputs carry nothing), a plant calibrated per world
    to a fixed ceiling (the same k gave 0.22-0.72), and the planted world must be found before
    any replay. The replay and real-search code is ready: `evo_wf.py replays S 101 140`, then
    `evo_real.py S` (built and unit-tested, never run).
- Compute: CPU only; `evo_wf.py` uses 8 worker processes (a few hundred MB in all); run with
  `OMP_NUM_THREADS=1`. Scratch (JSON per world) under `<cache_root>/derived/evo-1/`.

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
