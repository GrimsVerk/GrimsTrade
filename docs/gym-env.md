# Gymnasium environment (`grimstrade.gym_env`)

An RL agent trains on the same simulator, costs and no-look-ahead rules as the classic
strategies. Ladder rung 4 in `DESIGN.md` (M3). Install the optional group: `uv sync --group rl`
(`dev` already includes it). The daily runner never imports this module (a test checks it).

```python
from grimstrade.gym_env import TradingEnv, load_train

td = load_train(root)  # bars, distributions, cash rates; nothing after 2025-11-10
env = TradingEnv(td.history, dividends=td.dividends, cash_rates=td.rates, weekday=4)
obs, info = env.reset(seed=0)
obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
```

## Rules

- **Simulator.** `Replay` is `gym.simulate`'s event loop, opened at each decision; it calls the
  gym's own `_execute`. Fills at each asset's next open with slippage, Kraken taker tiers for
  crypto, the 1% band, sells before buys, cash-limited buys that wait, distributions, cash
  interest: all as in `gym.py`. Test: `ts_momentum` and `equal_weight` driven through the env give
  `simulate`'s result (equity curve, fills, cash, positions, income); also for a window starting
  mid-history and for weekly decisions. Change `gym.simulate` and `Replay` together: the test
  will fail otherwise.
- **Decisions.** At 22:30 UTC (`gym.DECIDE_AT`), daily, or weekly on `weekday` (4 = Friday, the
  research protocol's rule). Between weekly decisions the same weights are re-submitted every
  day, as `common.weekly` research strategies are replayed, so the band rebalances drift.
- **Action.** A Box in [0, 1], one target weight per symbol (`env.symbols`, sorted). Clipped to
  [0, 1], zero for an asset with fewer than `min_bars` visible bars, then scaled down to sum to 1
  if above. The rest is cash. Long-only, no leverage, as the paper broker.
- **Observation** (float32), only from bars closed by the decision (`data.visible`) and the
  account's own fills so far: by default per symbol the last `lookback` (20) daily log
  close-to-close returns (zero-padded) and a has-data flag; then each symbol's weight and the
  cash weight, valued at the visible closes. `features=` replaces the market part with any
  function of the visible bars. Test: scrambling every bar not closed by T (keeping opens that
  already happened) changes no observation or reward up to T.
- **Reward.** Default `"log"`: log growth of equity from this decision to the next, after all
  costs (sums to the episode's log growth). `"simple"`, `"excess_log"` (above the cash rate), or
  any function of `StepInfo` (equity before/after, cash growth, turnover, fees).
  `turnover_penalty` subtracts that times turnover.
- **Episodes.** Decision days `start`..`end` (default: all bars). `episode_steps` picks a random
  window per reset from `np_random` (`reset(seed=...)` repeats it). `truncated` at the last step;
  `terminated` only if equity reaches 0. The last step runs to one period after the last decision;
  `info["result"]` then holds the full `gym.Result` (for `report.py`-style scoring).
- **Held-out year.** `TradingEnv` raises `HeldOutError` for any bar, distribution or cash rate
  after 2025-11-10 (`TRAIN_LAST_BAR`) or an `end` after it, unless `allow_held_out=True`;
  `load_train` drops them. Spending the held-out year follows `research/protocol.md`: once per
  card, after train.

## Lessons from rl-1 .. rl-6 built in, or left to the caller

- rl-1 (PPO on six assets, softmax action, log-return reward) learned to hold coins and traded
  7-10x equity a year. The env's turnover in `info` and `turnover_penalty` make cost visible; a
  random agent here makes ~1,450 fills a year on the six assets and loses 4-12% to costs.
- rl-2's residual frame (a bounded tilt on `tsmom12`, reward = active log return) is the
  harness that kept the agent from losing: build it on top with a `reward` function and an action
  wrapper; the env stays plain target weights.
- Weekly decisions (`weekday=4`) and masking of assets without history follow rl-1's env.
- rl-6's closing note: on this data no learner beat the plain rules; the limit was the number of
  independent bets, not the optimiser. This env makes honest experiments cheap (about 12,000
  steps a second on one CPU core, six assets); it does not make them likely to pass.

Not modelled (as in `gym.py`): shorting, perpetuals and funding, intraday bars, maker fees.
