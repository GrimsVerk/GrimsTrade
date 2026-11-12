# Backlog: grimstrade

Ideas not started yet. Move one to `next-steps.md` when you start it; delete it when done.

- Gymnasium env wrapper around `gym.py` (for RL, M3).
- Credit dividends (ETF distributions) in the gym.
- Crypto fee by 30-day volume tier instead of one flat 60 bps (Kraken Pro taker: 0.80% from 0,
  0.60% from 2,500 USD, 0.38% from 10,000, 0.35% from 25,000; see DECISIONS, audit G3).
- More universe: a few more liquid crypto (SOL, ...) and ETFs (IWM, EFA, ...).
- Crypto funding-rate carry (long spot, short perpetual, collect funding). Needs a short-perp leg
  and funding cash flows in the gym first. Keyless source: Kraken Futures
  `https://futures.kraken.com/derivatives/api/v3/historical-funding-rates?symbol=PF_XBTUSD`
  (check the exact path when building; Binance/Bybit block US IPs, i.e. GitHub runners).
- A second daily run just after 00:00 UTC for crypto-only strategies, so a crypto signal fills
  ~22 hours sooner (see DECISIONS, execution timing). Changing the timing of a live strategy is a
  new try: register it under a new name.
- Alpaca free market data / FRED macro as extra sources (keys via Actions secrets).
