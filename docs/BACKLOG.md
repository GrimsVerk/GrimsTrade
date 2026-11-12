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
- Macro and cycle research lane (owner idea, 2026-11-12). Investors watch slow, years-long forces;
  test whether knowing which phase we are in helps the agent. Not yet tested by any research run
  (runs 1-3 only used prices; run 2 named FRED rates and credit spreads as the next kind of
  information). Candidates, each a card with its pass bar fixed first:
  - Fed policy: hiking vs cutting, level and direction of the fed funds rate (FRED `FEDFUNDS`,
    `DFF`), real rates, yield curve (`T10Y2Y`). Cheap money tends to lift asset prices.
  - Money supply / liquidity: M2 growth (`M2SL`), Fed balance sheet (`WALCL`), "money printing".
  - Bitcoin's ~4-year cycle around the halvings (2012, 2016, 2020, 2024): phase since the last
    halving as a signal. Warning: only ~3 full cycles of data, so very easy to fool ourselves;
    out-of-sample check is hard. Treat any result with deep suspicion.
  - Credit spreads (`BAA10Y`, high-yield OAS) as a risk-off warning.
  Honesty traps: macro data is published late and revised (use release dates / ALFRED vintages,
  never today's revised numbers, or it is look-ahead); few cycles means few independent tests.
  Bar to beat: the 12-month trend rule, which already reacts to these cycles with a lag. FRED
  csv downloads (`fredgraph.csv?id=...`) are keyless.
