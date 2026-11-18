# Next steps

## Trend 1926 (done 2026-11-18, branch `trend-1926`, draft PR #37 -> `trend-tune`)

Does `tsmom12` beat holding on US stocks 1926-1961 (French daily market and 10 industries, cache
snapshot 2026-11-12), and were its days out rougher than its days in? Card fixed before any
number; write-up at the top of `research/trend-1926.md`; tables `research/results/trend-1926.md`;
96 rows in `research/tries.md` (24 baseline, 72 robustness). One run, nothing rerun.

- Result: ahead over 1927-07 to 1961-12 (market Sharpe 0.88 against 0.55, +0.33, p 0.02; book
  +0.45; 9 of 10 industries; worst loss 38% against 84%), but short of the card's "a property":
  about two thirds of the lead is 1929-1932 (without it +0.11, p 0.18; from 1933 +0.09, p 0.22),
  and in 1946-1961 the market trails (-0.09). Days out were rougher than days in on 10 of 10
  industries in 1927-1945 and on 1 of 10 in 1946-1961. Crash insurance, not an edge.
- Live rule: no change (fixed on the card). Held-out year not involved.
- Replay check: the gym and the gym-free paper series agree except on 2 days (market) and 6
  days (durables) of 9,731, all in weeks whose Friday was a holiday with a Saturday session;
  they pick a different decision day there. Explained, not a fill error.
- Doing: nothing. No process running.
- Next lanes (not started): `trend-where-it-pays` with 1946-1961 as its hard case;
  `fast-reentry` with this period as an out-of-universe set; French daily data 1962-1993 on its
  own card.
- Rerun: `uv run python -I research/lib/trend_1926.py` rebuilds the tables (needs
  `research/macro.local.json`); runs saved under the git-ignored `research/data/runs/trend-1926/`
  are re-scored without new `tries.md` rows (on a fresh machine they would be logged again).

For the owner:

- A risk choice, not a decision forced by this run: the trend filter on the stock slots is
  insurance against a multi-year collapse (worst loss halved in 1929-1932) that costs a little
  in calm bull markets.

## Trend tune (done 2026-11-18, branch `trend-tune`, draft PR #34 -> `carry-2`)

What earns `tsmom12` its money, where it bleeds, and whether walk-forward tuning of its lookback
beats the fixed 12 months. Card fixed before any number; write-up `research/trend-tune.md`;
tables `research/results/trend-tune-anatomy.md` and `research/results/trend-tune.md`; 129 rows
in `research/tries.md`.

- Tuning: no. Three walk-forward procedures (a lookback per asset, one for the book, per asset
  shrunk toward 12): 1.01, 1.02 and 1.05 Sharpe against 1.05 for fixed `tsmom12`; nothing out of
  universe. Perfect hindsight would have been worth +0.10, and the best lookback of one era says
  nothing about the next. 12 months stays. Held-out year unspent.
- Anatomy: the rule beats holding only on stocks (SPY +0.09, QQQ +0.11), by sitting out the
  roughest stretches of 2000-03, 2008-09 and 2022; on bonds, gold and coins the days out were no
  rougher than the days in, so it costs return there for no gain in Sharpe. It buys back seven
  months after a low, 23% above it, and hands back in the rebound what it saved in the fall; 82
  of 112 exits were whipsaws. Since 2003 it has behaved like holding 76% of everything. Settings
  (lookback 6-12 months, decision frequency, thresholds, bands) sit on a flat plateau.
- Doing: nothing. No process running.
- Next lanes (not started; rows in `research/ideas.md`): (1) `trend-1926`: the stock result on
  the US market and 10 industries 1926-1961 (French library, already cached); (2)
  `trend-where-it-pays`: keep the filter only on assets whose past days out were rougher than
  days in; (3) `fast-reentry`: held if the 3-month or the 12-month return is positive, tested
  only out of universe and on the held-out year.
- Rerun: `uv run python research/lib/trend_tune_anatomy.py` and
  `uv run python research/lib/trend_tune_b.py` rebuild the tables; runs already saved under the
  git-ignored `research/data/runs/` are re-scored without new `tries.md` rows (on a fresh
  machine they would be logged again: copy that folder or accept duplicate rows).

For the owner:

- Nothing to decide for the live rule: it stays at 12 months.
- Optional, for the M1 lane: a 2.5-5% rebalance band gave the same Sharpe with 15-25% less
  trading in the backtest (a cost saving, not an edge).
- A risk choice the next lane would inform: the trend filter on the bond, gold and coin slots
  has cost return without lifting Sharpe, but it did shrink their worst losses.

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
