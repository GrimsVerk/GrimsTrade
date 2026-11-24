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

### The published backtests, as printed (in-sample)

Checked 2026-11-19 against the paper text where it says `[paper]` (journal print, or the
authors' draft or accepted manuscript where noted; volume, issue and pages checked against
Crossref). "Computed" = monthly mean / sd x sqrt 12 from the printed table (excess returns
for long-short factors). No post-publication numbers were read.

| Family | Paper | Sample | Printed result | Sharpe (paper) |
|---|---|---|---|---|
| value | Fama and French, "Common risk factors in the returns on stocks and bonds", JFE 33(1), 1993, 3-56 `[paper]` | 1963-07..1991-12 | HML 0.40%/month, sd 2.54, t 2.91 (Table 2) | **0.55** computed (market 0.33) |
| momentum | Jegadeesh and Titman, "Returns to buying winners and selling losers", JF 48(1), 1993, 65-91 `[paper]` | 1965-01..1989-12 | 12/3 winners minus losers 1.31%/month, t 3.74; 6/6 0.95%, t 3.07 (Table I; equal weight, deciles) | not printed (no sd) |
| momentum | Carhart, "On persistence in mutual fund performance", JF 52(1), 1997, 57-82 `[paper]` | 1963-07..1993-12 | PR1YR 0.82%/month, sd 3.49, t 4.46 (Table II) | **0.81** computed |
| quality | Fama and French, "A five-factor asset pricing model", JFE 116(1), 2015, 1-22 `[paper]` | 1963-07..2013-12 | RMW 0.25%/month, sd 2.14, t 2.92; CMA 0.33, sd 2.01, t 4.07 (Table 4, 2x3) | **RMW 0.40**, CMA 0.57 computed |
| quality | Novy-Marx, "The other side of value", JFE 108(1), 2013, 1-28 (author's 2012 version) `[paper]` | 1963-07..2010-12 | gross profitability high minus low 0.31%/month, t 2.49, sd 2.94 | 0.37 computed |
| quality | Asness, Frazzini and Pedersen, "Quality minus junk", Review of Accounting Studies 24(1), 2019, 34-112 `[paper]`; working paper Oct 2013 `[paper]` | WP: US 1956-06..2012-12; journal: US 1957-07..2016-12 | US QMJ 0.40%/month, t 4.38 (WP); 0.29%/month, t 3.62 (journal) | **0.58** (WP) / 0.47 (journal), stated |
| low-vol | Frazzini and Pedersen, "Betting against beta", JFE 111(1), 2014, 1-25 (authors' 2013 draft) `[paper]` | 1926-01..2012-03 | US BAB 0.70%/month, t 7.12, vol 10.7% | **0.78** stated |
| low-vol | Baker, Bradley and Wurgler, "Benchmarks as limits to arbitrage", FAJ 67(1), 2011, 40-54 `[paper]` | 1968-01..2008-12 | lowest-volatility quintile of the top 1,000 stocks, long-only | 0.38 stated (min-variance 0.47; large stocks 0.27) |
| multi-factor | Asness, Moskowitz and Pedersen, "Value and momentum everywhere", JF 68(3), 2013, 929-985 `[paper]` | 1972-01..2011-07 | 50/50 value + momentum, all asset classes, 6.8%/yr, sd 4.3% | **1.59** stated |
| dividend | none found with an in-sample Sharpe. McQueen, Shields and Thorley, FAJ 53(4), 1997 (Dow-10, 1946-1995): beats the Dow statistically, not after risk, costs and taxes `[secondary]` | | Koijen et al. (below): equity dividend-yield carry, long-short, Sharpe 0.36 `[paper]` | (0.36, long-short) |
| FX carry | Koijen, Moskowitz, Pedersen and Vrugt, "Carry", JFE 127(2), 2018, 197-225 (accepted manuscript) `[paper]` | currencies 1983-11..2012-09 | currency carry 5.29%/yr, sd 7.80% | **0.68** stated |
| FX carry | Lustig, Roussanov and Verdelhan, "Common risk factors in currency markets", RFS 24(11), 2011, 3731-3777 `[paper]` | 1983-11..2009-12 | HML_FX net of bid-ask 4.54%/yr, sd 9.05% | 0.50 stated (0.95 before bid-ask) |
| merger arb | Mitchell and Pulvino, "Characteristics of risk and return in risk arbitrage", JF 56(6), 2001, 2135-2175 `[paper]` | 1963-1998 (4,750 deals) | index-manager series after costs 10.64%/yr, sd 7.74%; returns like selling index puts; beta 0.49 in down markets | **0.57** stated (CRSP market 0.40) |
| option writing | Whaley, "Return and risk of CBOE Buy Write Monthly Index", Journal of Derivatives 10(2), 2002, 35-42 `[secondary]`: text not read | 1988-06..2001-12 | BXM 1.12%/month, sd 2.66; S&P 500 1.19%, sd 4.10 `[secondary, a search snippet: unverified]` | not found; ~0.9 vs ~0.65 if bills ~5%/yr (rough, unverified) |
| option writing | Ennis Knupp + Associates, "Evaluating the performance characteristics of the CBOE S&P 500 PutWrite Index", Dec 2008, for CBOE `[paper]` | 1986-06..2008-10 (index launched 2007; mostly backfill) | PUT 10.32%/yr, sd 9.91%; S&P 500 8.77%, sd 15.39% | **0.63** vs S&P 0.30 stated (gap +0.33) |
| risk parity | Asness, Frazzini and Pedersen, "Leverage aversion and risk parity", FAJ 68(1), 2012, 47-59 `[paper]` | 1926-01..2010-06 | risk parity 7.99%/yr excess, vol 15.08%; 60/40 4.65%, vol 11.68% | **0.53** vs 60/40 0.40 stated (gap +0.13) |
| trend | Moskowitz, Ooi and Pedersen 2012 via AQR's TSMOM factor (survey-5) | 1985-01..2009-12 | | **1.41** (survey-5, today's data) |
| tail hedge | Israelov, "Pathetic protection", Journal of Alternative Investments 21(3), 2019, 6-33 `[secondary]` | 1986-07..2016-05 | CBOE PPUT (5% OTM puts on the S&P 500): alpha -1.8%/yr, beta 0.74; a plain stock/cash mix of equal return had ~60% higher Sharpe | no positive edge claimed: insurance has a cost |
| gold miners, defensive sectors | no published long-short backtest used | | | - |

Paper series computed by code (card): HML, Mom (UMD), RMW, CMA from Ken French; BAB and QMJ
from AQR. Their in-sample Sharpe from today's data need not equal the printed one (the
libraries are rebuilt; French's Mom is value-weighted, not Jegadeesh-Titman's deciles).

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

## Step 2: the live check by family (card dda9386, script db6eba0, run 2026-11-19)

Card: [`cards/live-families.md`](cards/live-families.md), pushed before any number. Tables:
[`results/live-families.md`](results/live-families.md). Monthly returns above the 13-week
T-bill, each family over its own live months to 2025-10 (held-out year unread), every fund
after its fees. **Logged as:** 15 `live-check` rows in `tries.md` (`<family>@live-fund`, header
extended): descriptive, not selectable, not strategy tries. No `ledger/tries.jsonl` row.

**One slip in the card, declared:** it gives the Bonferroni level for 15 composites as
t >= 2.94; the right number for one-sided 0.05/15 is **2.71** (the code's). No family reaches
either, so no reading changes.

### What the numbers say (card's reading rules applied)

| Family | Live years | Sharpe | Plain holding, same months | Gap | Alpha t | Reading | Worst crash vs VFINX |
|---|---:|---:|---:|---:|---:|---|---|
| value | 33 | 0.53 | 0.55 | -0.02 | 0.1 | matched its holding | GFC -57% (-51%) |
| momentum | 18.6 | 0.58 | 0.64 | -0.06 | -0.1 | matched | GFC -56% (-51%) |
| quality | 15.3 | 1.00 | 0.97 | +0.03 | 0.9 | matched | 2022 -18% (-18%) |
| low-vol | 14.4 | 0.70 | 0.69 | +0.01 | 0.7 | matched (max DD 18% vs 25%) | 2020 -18% (-20%) |
| multi-factor | 20 | 0.59 | 0.65 | -0.05 | -1.6 | matched | GFC -52% (-51%) |
| dividend | 22.8 | 0.67 | 0.71 | -0.04 | 0.2 | matched | GFC -46% (-51%) |
| defensive sectors | 26.8 | 0.57 | 0.48 | +0.08 | 1.5 | matched (max DD 34% vs 51%) | GFC -33% (-51%) |
| option writing | 37.8 | 0.43 | 0.63 | -0.20 | -1.0 | **lagged** | GFC -31% (-51%) |
| gold miners (vs gold) | 20.8 | 0.32 | 0.59 | -0.27 | -1.2 | **lagged** | GFC -41% (-51%) |
| risk parity (vs 60/40) | 16.3 | 0.63 | 0.92 | -0.30 | -1.0 | **lagged** | 2022 -16% (-18%) |
| merger arb (vs bonds) | 36.8 | 0.40 | 0.55 | -0.15 | 2.2 | lagged bonds on Sharpe; alpha t 2.2 | 2000-02 **+14%**, GFC -3% |
| tail hedge | 14.7 | -0.54 | - | - | -1.6 | **cost** (TAIL -0.77, VIXY -0.74, BTAL -0.24) | 2020 **+46%** (-20%) |
| style premia, long-short (bills) | 12 | 0.50 | 0 | +0.50 | 1.7 | paid little; **risk tool** | 2022 **+28%** (-18%) |
| trend (bills) | 18.7 | 0.17 | 0 | +0.17 | 0.7 | paid little; **risk tool** | GFC **+13%**, 2022 **+20%** |
| FX carry (CEW, bills) | 16.3 | -0.03 | 0 | -0.03 | -0.1 | did not pay | 2020 -9% |

1. **No long-only equity factor family beat its plain index after fees.** Value, momentum,
   quality, low-vol, multi-factor, dividend: gaps -0.06 to +0.03, alpha t -1.6 to 0.9, over
   14-33 live years. Of their 26 member funds, none has alpha t above 1.5. The long-only factor
   fund **is the index**: correlation 0.86-0.99, beta 0.65-1.04. Low-vol and dividend bought
   shallower drawdowns at the same Sharpe, not a higher one.
2. **Strategies that sell insurance lagged their holding live.** Option writing lagged the
   S&P 500 by 0.20 Sharpe over 38 years (PBP, XYLD, QYLD -0.31 to -0.42); the paper indexes
   themselves (no fees) lagged too: BXM -0.17 since 2002, PUT -0.10 since 2007. The PUT
   study's in-sample gap was +0.33. So the loss is the effect, not the fees.
3. **Strategies that buy insurance cost a lot live.** The tail-hedge funds lost 0.5-0.8
   Sharpe a year (VIXY a mean of -47% a year, a 100% drawdown) and paid off in one window (2020, +46%).
   An 80/20 mix with the market lost 0.13 Sharpe for a 5-point shallower drawdown. Not a risk
   tool by the card's rule.
4. **The only families with a positive live Sharpe and low correlation to stocks:** AQR's
   long-short style premia (0.50, t 1.7, 12 years; corr -0.01; +28% in 2022), merger
   arbitrage (0.40 over 37 years, t about 2.4 against bills; corr 0.39; +14% in 2000-02, -3%
   in 2008-09) and trend (0.17, corr -0.13, gained in all three crashes it lived through).
   Style premia and trend pass the card's risk-tool rule; merger arb misses only on
   correlation (0.39 > 0.3), and its 80/20 mix cut the market's drawdown by 8 points at +0.01
   Sharpe.
5. **Nothing reaches t 2.71** (Bonferroni over 15 families), let alone the project-wide bar
   (z 3.89). Merger arb's alpha t 2.2 against bonds is the highest.

### Paper to live: how much of each published backtest is left

Printed in-sample Sharpe (card) against the live counterpart fixed by the card. The code's
version from today's data is in brackets where it has one.

| Family | Paper Sharpe | Paper factor after publication (today's data) | Live counterpart | Kept | Reading |
|---|---:|---:|---:|---:|---|
| value | HML 0.55 (0.52) | 0.12 (1994-2025) | IR 0.02 | **4%** | decayed to nothing |
| momentum | PR1YR 0.81 (UMD 0.80) | 0.26 (1994-2025) | IR -0.03 | **<0** | decayed to nothing |
| quality | QMJ 0.58 (0.56) / RMW 0.40 (0.41) | QMJ -0.03 (2020-25), RMW 0.45 (2016-25) | IR 0.25 | **43% / 63%** | kept part / most (t 0.9: not shown to be real) |
| low-vol | BAB 0.78 (0.70) | 0.42 (2015-2025) | IR 0.20 | **26%** | kept part |
| multi-factor | 1.59 (value + momentum everywhere) | - | style premia Sharpe 0.50; long-only IR -0.37 | **31% / <0** | kept part (long-short) / nothing (long-only) |
| dividend | (D/P carry 0.36) | - | IR 0.03 | 8% | decayed to nothing |
| FX carry | 0.68 | - | -0.03 (CEW, long-only EM basket) | <0 | nothing (weak proxy: no G10 long-short fund survives) |
| merger arb | 0.57 (after costs) | - | 0.40 | **70%** | kept most |
| option writing | PUT gap +0.33 | BXM gap -0.17, PUT gap -0.10 (indexes) | gap -0.20 | <0 | reversed |
| risk parity | gap to 60/40 +0.13 | - | gap -0.30 | <0 | reversed |
| trend | 1.41 | 0.35 (survey-5) | 0.17 (composite; AQMIX 0.29) | **12% (21%)** | decayed to nothing (nearly) |

The pattern: **the more a premium was a famous stock-selection anomaly, the less is left**
(value, momentum, dividend: 0-8%); the ones that kept most are premia for bearing a real,
ugly risk that few want (merger arb's deal-break risk, 70%; low beta's leverage constraint,
26%) or long-short multi-asset books (style premia, 31%). Of the 11 families with a number, the
median kept 8%, and 4 of 11 went below zero; McLean-Pontiff's 58% decay for stock anomalies looks optimistic for
what an investor in a fund actually got.

## Step 3: plain ranking for a human (one screen)

**Paid live, net of fees, more than the plain thing you would otherwise hold: none.** No
family beat its matched holding with t >= 2 over its live life.

**Paid something, and low correlation with stocks (worth knowing as diversifiers):**
1. Long-short multi-asset style premia (value, momentum, carry, defensive): Sharpe 0.50, 12
   years, +28% in 2022. Kept about a third of the paper. Only one manager's two funds.
2. Merger arbitrage: Sharpe 0.40 for 37 years, small drawdowns (11%), gained in 2000-02,
   flat in 2008-09. Kept 70% of the paper, the best of any family. Not more Sharpe than a
   bond index over the same years, but a different risk.
3. Trend following: Sharpe 0.17, gained in every crash it lived through. Insurance that
   roughly pays for itself.

**Paid exactly like their index (a holding, not an edge):** value, momentum, quality,
low-vol, multi-factor, dividend, defensive sectors. Low-vol, dividend and defensive sectors
bought shallower drawdowns (low-vol 18% vs 25%, dividend 47% vs 51%, defensive sectors 34%
vs 51%) at about the same Sharpe: risk choices.

**Lagged or cost money:** option writing (-0.20 vs the S&P 500), risk parity (-0.30 vs a
60/40 index fund), gold miners (-0.27 vs gold), FX carry (0), tail hedges (-0.54 a year).

**Decayed to nothing:** value, momentum, dividend, trend (kept 0-12% of the paper Sharpe);
option writing and risk parity reversed sign.

### What this means for our six-asset weekly book (SPY, QQQ, TLT, GLD, BTC, ETH)

Most families do not map onto six assets at all (stock selection, deals, options). What does
map, and what the live record says about it:

- **Holding the six is the bar, and the live record says it is hard to beat:** every
  long-only tilt matched its index. Survey-5 found the same for `tsmom12` (Sharpe 1.11 =
  holding 1.11 in 2010-2025).
- **What paid live with low correlation is long-short and multi-asset** (style premia,
  trend), and it paid mainly in crashes. Our long-only trend rule cannot gain from a fall;
  short-1 found shorting coins on perps lost.

**Directions to study next (2-3), judged on crash behaviour, not Sharpe:**

1. **A trend-as-insurance sleeve, judged as insurance** (the risk-tool measures of this
   card: crash windows, the 80/20 mix's drawdown and Sharpe change). Question: does a
   small sleeve that is short SPY/QQQ in a 12-month downtrend (ETFs, not perps; no coins
   short) do for the six what the live trend funds did for a stock book (2008 +13%, 2022
   +20%) at a cost we can afford? Prior: low (short-1, survey-5), but it is the only
   family whose live record is "gains in crashes, roughly free".
2. **Cross-asset "defensive" weights within the six**, as a risk choice, not an edge:
   low-vol, dividend and defensive sectors all bought 4-17 points shallower drawdowns at
   about the same Sharpe live. The six-asset analogue is inverse-volatility or capped-coin
   weights; `risk-map.md` already maps the drawdown choices, so this is a write-up for the
   owner rather than a new test.
3. **A multi-asset style-premia check on the six (value = 5-year reversal, carry = TLT
   term spread and coin funding, momentum = 12-month, defensive = low vol), long-short
   across the six, descriptive first** (an information-coefficient screen like info-1, not a
   strategy). The only family with a positive, uncorrelated live record that our data can
   express. Prior very low: six assets is a tiny cross-section, and anything built must meet
   the project-wide bar (N 1,012, z 3.89).

**Not worth our time, on the live record:** long-only factor tilts of any kind, option
writing / covered calls, tail-risk ETFs and long volatility, gold miners instead of gold,
FX carry, more published return effects tested for a Sharpe edge.

## Caveats

- **Survivors only** (AQR's momentum funds were merged away in 2026, DBV liquidated in
  2023): the live record is, if anything, better than the families'.
- **Different windows.** Each family is measured over its own live years, so families are
  not compared over the same markets (value from 1992, style premia from 2013). The gap to
  the matched holding is over the same months, which is the fair comparison.
- **Matched holdings are a choice.** Merger arb against a bond index (similar volatility);
  gold miners against gold; risk parity against a 60/40 index fund; style premia, trend,
  carry and tail hedges against bills. Another choice moves the gaps, not the "matched its
  holding" readings of the equity families, whose correlations with their index are 0.86+.
- **Tail-hedge composite mixes** three bills-matched funds and SWAN (matched to a 60/40
  fund); its composite "gap" is not meaningful, its members are.
- **Fees are today's.** NAVs net whatever was paid; A-share sales loads (MERFX, GATEX,
  INIVX) are not in NAV, so an investor who paid them got less.
- **Paper numbers**: Whaley's BXM figures come from a search snippet (unverified); the
  card's option-writing paper number is the PUT study's (read), whose window includes 16
  months after launch.
