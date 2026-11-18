# Survey 6: which strategy families paid investors live? (2026-11-19)

Lane `survey-6` of the night lead (research only, fake money). Branch `survey-6` from
`survey-5`, draft PR #91.

Why: survey-5 found that live trend funds earned Sharpe 0.19-0.29 above bills in 2010-2025
against 1.41 for the published paper factor in its own sample (h = 80%), and that `tsmom12`
earned exactly what holding the six assets earned. Published effects are 0 for 5 after
publication in this book. So: before choosing the next direction, look at **which strategy
families have actually paid investors, live and net of fees, since their funds launched**,
and how much of each family's published backtest survived. Live records are not chosen in
hindsight by us, pay real costs, and mostly run after the papers.

How the list was made: names of the large, long-running funds of each family I could name
before looking at any return (knowledge, not a screen), checked on Yahoo's keyless chart API
(`lib/survey6_fetch.py`, which prints each series' name, type and first and last bar only),
Ken French's and AQR's public data libraries, CBOE's public index files, and web searches for
inception dates, fees and mandate changes. **No return of any fund, holding, factor or index
was computed before the card.** One slip to declare: checking the layout of the Fama-French
five-factor file printed its first monthly row (1963-07: six numbers, inside RMW's and CMA's
paper sample; not a statistic of any window).

Tags as in survey-4/5: `[data]` = seen in the downloaded file; `[issuer]` = the fund
company's own page (via a search summary or the page); `[secondary]` = an aggregator or a
write-up; `[not checked]`.

## Live return series (keyless, daily, net of fees)

Yahoo's adjusted close (distributions reinvested): for a mutual fund that is the daily NAV, so
every series is **after the fund's fees and its real trading costs** (sales loads of A shares
are not in NAV and are ignored). First bar `[data]`. Downloaded 2026-11-18/19 into the
git-ignored cache (`<cache_root>/downloads/survey-6/`, parsed to
`<cache_root>/derived/survey-6/<TICKER>.csv`) by
`python -I research/lib/survey6_fetch.py <cache_root>`. Trend and risk-parity series are
survey-5's (`<cache_root>/derived/survey-5/`), reused unchanged.

Inception and fee tags from the issuers' pages and filings where found (2026-11-19 search;
fees are today's, not those paid over the whole life; the NAV already nets whatever was paid).
"Cut" = months used, where a fund only became the family later or stopped being it.

### Value

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| DFLVX | DFA US Large Cap Value (I) | mutual fund | 1993-02-18 | 1993-02-19 `[issuer]`; benchmark Russell 1000 Value | 0.22% net `[issuer]` |
| DFSVX | DFA US Small Cap Value (I) | mutual fund | 1993-02-26 | 1993-03-02 `[issuer]` | 0.27% net `[issuer]` |
| DFIVX | DFA International Value (I) | mutual fund | 1994-02-15 | 1994-02-15 `[issuer]` | 0.28% net `[issuer]` |
| VIVAX | Vanguard Value Index (Investor) | mutual fund | 1992-10-30 | 1992-11-02 `[issuer]`; S&P/Barra Value to 2003-05, MSCI US Prime Value to 2013-04, CRSP (renamed Morningstar 2026-07) since `[issuer]` | 0.17% `[issuer]` |
| IWD | iShares Russell 1000 Value | ETF | 2000-05-26 | 2000-05-22 `[issuer]` | 0.18% `[issuer]` |
| IWN | iShares Russell 2000 Value | ETF | 2000-07-28 | 2000-07-24 `[issuer]` | 0.24% `[issuer]` |
| VTV | Vanguard Value ETF | ETF | 2004-01-30 | 2004-01-26 `[issuer]`; index history as VIVAX | 0.03% `[issuer]` |
| RPV | Invesco S&P 500 Pure Value | ETF | 2006-03-07 | 2006-03-01 `[secondary]`; Rydex, then Guggenheim, Invesco since 2018-04 | 0.35% `[secondary]` |

### Momentum

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| PDP | Invesco Dorsey Wright Momentum | ETF | 2007-03-01 | 2007-03-01 `[secondary]`; Dorsey Wright Technical Leaders index (relative strength), renamed only 2023 `[issuer]` | 0.62% `[secondary]` |
| MTUM | iShares MSCI USA Momentum Factor | ETF | 2013-04-18 | 2013-04-16 `[issuer]`; index to the "SR Variant" (staggered rebalance) about 2020-12 `[secondary]` | 0.15% `[issuer]` |

### Quality

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| SPHQ | Invesco S&P 500 Quality | ETF | 2005-12-06 | 2005-12-06 `[secondary]`; **was a Value Line "Timeliness" fund until 2010-06-30** `[issuer: SEC 497]`, S&P quality rankings to about 2016-03, S&P 500 Quality index since `[secondary]`. **Cut: from 2010-07.** | 0.15% `[secondary]` |
| QUAL | iShares MSCI USA Quality Factor | ETF | 2013-07-18 | 2013-07-16 `[issuer]` | 0.15% `[issuer]` |

### Low and minimum volatility

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| SPLV | Invesco S&P 500 Low Volatility | ETF | 2011-05-05 | 2011-05-05 `[secondary]` | 0.25% `[secondary]` |
| USMV | iShares MSCI USA Min Vol Factor | ETF | 2011-10-20 | 2011-10-18 `[issuer]` | 0.15% `[issuer]` |
| ACWV | iShares MSCI Global Min Vol Factor | ETF | 2011-10-20 | 2011-10-18 `[issuer]` | 0.20% `[issuer]` |
| EEMV | iShares MSCI EM Min Vol Factor | ETF | 2011-10-20 | 2011-10-18 `[issuer]` | 0.25% `[issuer]` |

### Multi-factor

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| DFEOX | DFA US Core Equity 1 (I) | mutual fund | 2005-09-16 | 2005-09-15 `[issuer]`; market with size, value, profitability tilts | 0.15% `[secondary]` |
| DFQTX | DFA US Core Equity 2 (I) | mutual fund | 2005-09-16 | 2005-09-15 `[issuer]`; stronger tilts | 0.18% net `[issuer]` |
| LRGF | iShares U.S. Equity Factor | ETF | 2015-04-30 | 2015-04-28 `[issuer]`; MSCI multi-factor to 2022-05, STOXX factor index since 2022-06 `[issuer]` | 0.08% (0.20% before 2022) `[issuer]` |
| GSLC | Goldman Sachs ActiveBeta US Large Cap | ETF | 2015-09-21 | 2015-09-17 `[issuer]` | 0.09% `[secondary]` |

### Long-short style premia (survey-5's, reused)

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| QSPIX | AQR Style Premia Alternative (I) | mutual fund | 2013-10-30 | 2013-10-30 `[issuer]`; long-short value, momentum, carry, defensive across asset classes | 1.53% (6.13% with short dividends and borrowing) `[issuer]` |
| QRPIX | AQR Alternative Risk Premia (I) | mutual fund | 2017-09-19 | survey-5 | `[not checked]` |

### Dividend

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| DVY | iShares Select Dividend | ETF | 2003-11-07 | 2003-11-03 `[issuer]` | 0.38% `[issuer]` |
| SDY | SPDR S&P Dividend | ETF | 2005-11-15 | 2005-11-08 `[issuer]`; High Yield Dividend Aristocrats | 0.35% `[issuer]` |
| VIG | Vanguard Dividend Appreciation | ETF | 2006-05-02 | 2006-04-21 `[issuer]`; Dividend Achievers to 2021-09, S&P US Dividend Growers since `[issuer]` | 0.04% `[issuer]` |
| VYM | Vanguard High Dividend Yield | ETF | 2006-11-16 | 2006-11-10 `[issuer]` | 0.04% `[issuer]` |
| SCHD | Schwab US Dividend Equity | ETF | 2011-10-20 | 2011-10-20 `[issuer]` | 0.06% `[issuer]` |
| VDIGX | Vanguard Dividend Growth (Investor) | mutual fund (active) | 1992-05-15 | 1992-05-15 `[issuer]`; **a utilities income fund until 2002-12-06** `[issuer]`. **Cut: from 2003-01.** | 0.20% `[issuer]` |

### FX carry

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| CEW | WisdomTree Emerging Currency Strategy | ETF | 2009-06-02 | 2009-05-06 `[issuer]`; T-bills plus short EM currency forwards, so it earns EM short rates (carry) plus spot moves against USD `[issuer]`; long-only basket, not a G10 long-short carry trade | 0.55% `[issuer]` |

### Merger arbitrage

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| MERFX | The Merger Fund (A, the old Investor class) | mutual fund | 1989-01-31 | 1989 `[issuer]`; strategy unchanged | 1.55% net; A share 5.5% max load (not in NAV) `[issuer]` |
| ARBFX | Arbitrage Fund (R) | mutual fund | 2000-09-18 | 2000-09-18 `[secondary]`; dropped its 80% merger-arbitrage policy 2026-08 (after our window) `[secondary/SEC]` | about 1.71% `[secondary]` |
| MNA | NYLI (formerly IQ) Merger Arbitrage | ETF | 2009-11-17 | 2009-11-17 `[issuer]`; index-based | 0.77% `[issuer]` |

### Option writing

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| GATEX | Gateway Fund (A) | mutual fund | 1980-01-02 | 1977-12-07 `[issuer]`; single-stock calls at launch, **S&P 500 index calls sold plus index puts bought "since 1988"** `[issuer]`. **Cut: from 1988-01.** | 0.94% net; 5.75% max load (not in NAV) `[issuer]` |
| PBP | Invesco S&P 500 BuyWrite | ETF | 2007-12-27 | 2007-12-20 `[secondary]`; tracks CBOE BXM | 0.29% `[secondary]` |
| XYLD | Global X S&P 500 Covered Call | ETF | 2013-06-24 | 2013-06-21 `[issuer]`; Recon/Horizons until 2018 | 0.60% `[issuer]` |
| QYLD | Global X Nasdaq 100 Covered Call | ETF | 2013-12-12 | 2013-12-11 `[issuer]` | 0.60% `[issuer]` |

### Tail hedges

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| TAIL | Cambria Tail Risk | ETF | 2017-04-06 | 2017-04-06 `[issuer]`; Treasuries plus OTM S&P 500 puts | 0.59% `[issuer]` |
| VIXY | ProShares VIX Short-Term Futures | ETF | 2011-01-04 | 2011-01-03 `[issuer]`; long 1-2 month VIX futures | 0.85% `[issuer]` |
| BTAL | AGF US Market Neutral Anti-Beta | ETF | 2011-09-13 | 2011-09-13 `[secondary]`; long low beta, short high beta; index until 2022-02, rules-based active since `[secondary]` | 1.40% net incl. short costs `[issuer]` |
| SWAN | Amplify BlackSwan Growth & Treasury Core | ETF | 2018-11-06 | 2018-11-06 `[secondary]`; ~90% Treasuries + ~10% SPY LEAP calls | 0.49% `[secondary]` |

### Gold miners

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| INIVX | VanEck International Investors Gold (A) | mutual fund | 1980-01-02 | 1956-02-10 `[issuer]` | 1.31%; 5.75% load (not in NAV) `[issuer]` |
| FSAGX | Fidelity Select Gold | mutual fund | 1985-12-16 | 1985-12-16 `[secondary]`; may hold up to 25% bullion `[secondary]` | about 0.64% `[secondary]` |
| VGPMX | Vanguard Precious Metals and Mining (Investor) | mutual fund | 1984-05-23 | 1984-05-23 `[issuer]`; **became Global Capital Cycles 2018-09-26** `[issuer]`. **Cut: to 2018-08.** | 0.42% (today's fund) `[issuer]` |
| GDX | VanEck Gold Miners | ETF | 2006-05-22 | 2006-05-16 `[issuer]` | 0.51% `[issuer]` |
| GDXJ | VanEck Junior Gold Miners | ETF | 2009-11-11 | 2009-11-10 `[issuer]`; rules widened 2017 `[secondary]` | 0.52% `[issuer]` |

### Defensive sectors

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| XLP / XLU / XLV | Select Sector SPDR: staples / utilities / health care | ETF | 1998-12-22 | 1998-12-16 `[issuer]` | 0.08% `[issuer]` |
| SECT | Main Sector Rotation | ETF (active, fund of ETFs) | 2017-09-06 | 2017-09-05 `[secondary]`; rotates sector ETFs on value and momentum | about 0.7% `[secondary]` |

### Trend and risk parity

Survey-5's lists, unchanged: trend RYMFX, AQMIX, ASFYX, WTMF, PQTIX, ABYIX, DBMF, KMLM, CTA;
risk parity ABRZX, AQRIX, RPAR (fees and dates in `survey-5.md`).

## Plain holdings to match against

| Ticker | Holding | First bar `[data]` | Used for |
|---|---|---|---|
| VFINX | Vanguard 500 Index (Investor) | 1980-01-02 | US large-cap families; the market column and the 80/20 mix |
| NAESX | Vanguard Small Cap Index (Investor) | 1980-01-02 | DFSVX |
| VTSMX | Vanguard Total Stock Market Index (Investor) | 1992-04-27 | PDP, DFA core funds |
| VGTSX | Vanguard Total International Stock Index (Investor) | 1996-04-29 | DFIVX |
| IWB / IWM | iShares Russell 1000 / 2000 | 2000-05 | IWD / IWN |
| ACWI / EEM | iShares MSCI ACWI / Emerging Markets | 2008-03 / 2003-04 | ACWV / EEMV |
| QQQ | Invesco QQQ | 1999-03-10 | QYLD |
| SPY | SPDR S&P 500 | 1993-01-29 | sector ETFs (same sponsor family, same index) |
| VBMFX | Vanguard Total Bond Market Index (Investor) | 1986-12-11 | merger arbitrage (similar risk) |
| VBINX | Vanguard Balanced Index (Investor), 60/40 | 1992-09-28 | risk parity, SWAN |
| GLD | SPDR Gold Shares | 2004-11-18 | gold miners |
| bills | 13-week T-bill (the repo's `IRX` series) | 1960 | market-neutral families |

Index mutual funds rather than ETFs where the fund family is older (VFINX vs SPY), so the
matched holding is itself live and net of its (small) fee.

## Published paper series (keyless)

| Series | Source | First month `[data]` | Notes |
|---|---|---|---|
| Mkt-RF, SMB, HML, RF | Ken French library, `F-F_Research_Data_Factors_CSV.zip` | 1926-07 | file built from the 2026-09 CRSP database `[data]` |
| RMW, CMA | Ken French, `F-F_Research_Data_5_Factors_2x3_CSV.zip` | 1963-07 | |
| Mom (UMD) | Ken French, `F-F_Momentum_Factor_CSV.zip` | 1927-01 | |
| BAB (US and 23 countries) | AQR, "Betting Against Beta: Equity Factors, Monthly" | 1930-12 | "updated and extended version" of Frazzini-Pedersen 2014; "AQR reconstructs the full history each time" `[data]` |
| QMJ (US and 23 countries) | AQR, "Quality Minus Junk: Factors, Monthly" | 1957-07 | same caveat `[data]` |
| BXM, PUT | CBOE, `cdn.cboe.com/api/global/us_indices/daily_prices/<n>_History.csv` | BXM 2002-03-22, PUT daily 2007-02 | PUT's file has only 7 scattered points before 2007 `[data]`, so its backfilled years are not usable |
| TSMOM | AQR (survey-5) | 1985-01 | reused through survey-5's result, not recomputed |

Paper citations and their printed in-sample numbers: being verified (next commit).

## Tried and not usable keyless

- **AQR's momentum funds** (AMOMX, ASMOX, AIMOX, the only long-running live momentum funds by
  the authors of the factor): Yahoo returns meta data but no prices. They were merged into AQR's multi-style funds about 2026-05-04 (AQR: single-style funds
  no longer viable alone) `[issuer: SEC 497/N-14]`; Yahoo keeps no history of merged funds.
- **DBV** (Invesco DB G10 Currency Harvest, the one pure FX-carry ETF): 404, delisted (as in
  survey-5). Last traded 2023-03-03, liquidated about 2023-03-10 `[issuer: SEC]`.
- **HFRI / Credit Suisse / Eurekahedge** hedge-fund indexes (merger arbitrage, tail risk):
  need accounts or are not keyless `[not checked]`; the live funds stand in.
- **Gold before 2004-11**: no keyless daily gold price on the same endpoint before GLD, so the
  old gold-miner funds (INIVX 1980, FSAGX 1985, VGPMX 1984) are matched to gold only from
  2004-12.

## What this list cannot show

- **Survivorship.** Yahoo serves only funds still listed. The AQR momentum funds and DBV are
  gone (above); other closed value, dividend, covered-call and tail funds were not searched.
  Each family's live record here is if anything **better** than the family's.
- **Selection by me.** Picked by name, before any return was computed in this lane; I know in
  general how some families fared (the card states what).
- **Long-only funds against long-short papers.** A long-only value or momentum fund holds the
  market plus a tilt. Its comparable "live Sharpe" of the effect is the information ratio of
  its return against its matched holding, not its own Sharpe; the card fixes that measure.
- **Index changes.** Several ETFs changed index or method during their lives (table notes);
  they are kept as one series, since an investor holding them lived through the change.
