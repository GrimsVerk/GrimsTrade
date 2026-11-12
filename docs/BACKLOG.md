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
- Own reinforcement-learning trading agent (owner's main interest, 2026-11-12). Train it on the
  5080 in the gym; the classic strategies are the baselines it must beat, and their data is its
  training data. Daily bars are thin for RL (about 30 years of ETFs, 12 of crypto), so better
  data comes first (next item). Ladder rung 4 in `docs/DESIGN.md`.
- Data search lane (owner, 2026-11-12, "we really really need"): hunt for more and better data:
  longer history, more assets, intraday bars, order books, crypto funding, on-chain, macro, news,
  sentiment. Free and keyless first. Paid only if very, very cheap: list it with its price for the
  owner, who alone decides; agents never sign up or pay.
- Investing agent (owner, 2026-11-12): a second agent in this repo with a long horizon (months to
  decades), next to the trading agent (hours to days; minutes for crypto). Same gym, ledger and
  honesty rules; only the horizon differs.
- Where GPU models run (decide when M3 starts): small models are trained on the 5080 and their
  weights committed, so the Actions runner (no GPU) can use them. Big ones (a local news LLM)
  run on the owner's PC and write a dated signal file before the 22:30 UTC run; if the PC is
  off, those strategies skip that day. "No LLM in the runner" is about Claude and about not
  needing the desktop, not about models in general.
- Idea sources from the owner (2026-11-12), to read for hypotheses, never as truth:
  - YouTube channels, fetched with GrimsVerk/YT-Harvest (transcripts stay local, never in git;
    cite video + timestamp on each card): Andrei Jikh (@AndreiJikh), Bravos Research
    (@bravosresearch), Real Vision (UCGXWKlq1Oxr3ddEtmKhAkPg), Raoul Pal The Journey Man
    (UCVFSzL3VuZKP3cN9IXdLOtw), EC Krown (@ECKrown, @ECKrown4), EllioTrades
    (@elliotrades_official), George Gammon (@GeorgeGammon), Mark Tilbury (@marktilbury), MoneyZG
    (@MoneyZG), New Money (@NewMoneyYouTube), How Money Works (@HowMoneyWorks), Miles Deutscher
    Finance (@milesdeutscher1357; reviews FOSS trading repos).
  - FOSS trading repos (from Miles Deutscher's video yuckuVqd01k): TauricResearch/TradingAgents,
    ZhuLinsen/daily_stock_analysis, HKUDS/Vibe-Trading, anthropics/financial-services,
    freqtrade/freqtrade, Jakeschincariol/day-trader-skill, virattt/ai-hedge-fund,
    LuckyOne7777/LLM-Trading-Lab. Read code and docs for ideas; never run their code here.
