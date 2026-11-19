# Survey 5: live track records as post-sample evidence (2026-11-18)

Lane `survey-5` of the night lead (research only, fake money). Branch `survey-5` from `survey-4`.

Why: published effects are 0 for 5 in this book after publication (survey-2, survey-3, ann-1,
survey-4's `ts-carry` and `halloween`). Survey-4's advice was to prefer forward or live evidence
over more backtests of published effects. The live rule `tsmom12` (Sharpe 1.05 in our 1994-2025
backtest) is itself a published effect (Moskowitz, Ooi, Pedersen 2012). Its forward record in
this repo is days old. But funds have traded the same family with real money since 2007-2010.
Their net asset values are a **live** record: not chosen in hindsight, after fees and real
costs, and mostly after the papers. This survey collects those records, then asks how much a
backtest of this family loses when it goes live (step 2), and what that means for the Sharpe
to expect from `tsmom12` and for how long a forward test needs (step 3).

How the list was made: Yahoo's keyless chart API (the same endpoint `lib/fetch.py` uses), AQR's
public data library, web searches for inception dates and fees. Only each fund's name, type and
first and last bar were read in this step (`lib/survey5_fetch.py` prints nothing else). **No
return of any fund was computed before the card in step 2.** One slip to declare: opening the
AQR workbook to read its layout printed the first four monthly rows of 1985 (four numbers,
outside every window used below).

Tags as in survey-4: `[data]` = seen in the downloaded file; `[issuer]` = the fund company's
own page via a search summary; `[secondary]` = an aggregator or a write-up; `[not checked]`.

## Live return series (all keyless, daily, net of fees)

Prices are Yahoo's adjusted close (distributions reinvested): for a mutual fund that is the
daily NAV, so every series is **after the fund's fees and its real trading costs**. First bar
is Yahoo's first bar `[data]`; inception and fees are from the sources tagged. Downloaded
2026-11-18 into the git-ignored cache (`<cache_root>/downloads/survey-5/yahoo/`, parsed to
`<cache_root>/derived/survey-5/<TICKER>.csv`) by
`python -I research/lib/survey5_fetch.py <cache_root>`.

### Trend following / managed futures (the family of `tsmom12`)

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| RYMFX | Guggenheim Managed Futures Strategy (P) | mutual fund | 2007-02-22 | 2007-03-02 `[issuer]`; tracked the S&P Diversified Trends Indicator until 2011-07, a DTI-based rule until 2013-01, a multi-strategy book since `[issuer]`. The only one live through 2008. | 1.83% net `[issuer]` |
| AQMIX | AQR Managed Futures Strategy (I) | mutual fund | 2010-01-05 | 2010-01-05 `[issuer]`. Same manager and method family as the AQR TSMOM factor below. | 1.26% "adjusted" (2.72% with short-sale and borrowing costs) `[issuer]` |
| ASFYX | Virtus AlphaSimplex Managed Futures Strategy (I) | mutual fund | 2010-08-03 | 2010-07-30 `[secondary]` (Schwab) | 1.45% net `[secondary]` |
| WTMF | WisdomTree Managed Futures Strategy | ETF | 2011-01-05 | 2011-01 `[data]`; the method changed over its life `[not checked]` | ~0.65% `[secondary]` |
| LFMIX | LoCorr Macro Strategies (I) | mutual fund | 2011-04-06 | multi-manager, trend-heavy `[not checked]`; reported alone, not in the composite | `[not checked]` |
| PQTIX | PIMCO TRENDS Managed Futures Strategy (I) | mutual fund | 2014-01-06 | Yahoo's history starts here `[data]` | ~1.5% (another share class) `[secondary]` |
| ABYIX | Abbey Capital Futures Strategy (I) | mutual fund | 2014-07-03 | multi-CTA `[not checked]` | `[not checked]` |
| DBMF | iMGP DBi Managed Futures Strategy | ETF | 2019-05-08 | replicates the SG CTA index's positions from its returns `[not checked]` | 0.85% `[secondary]` |
| KMLM | KraneShares Mount Lucas Managed Futures Index Strategy | ETF | 2020-12-02 | tracks the KFA MLM Index (index history to 1988 only on request) `[secondary]` | 0.90% `[secondary]` |
| CTA | Simplify Managed Futures Strategy | ETF | 2022-03-08 | | ~0.75% (2023 figure) `[secondary]` |

### Risk parity / balanced risk (the family of `sixty-forty` and `where-vol`)

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| ABRZX | Invesco Balanced-Risk Allocation (A) | mutual fund | 2009-06-03 | NAV series; the A share's sales load is not in NAV | `[not checked]` |
| AQRIX | AQR Multi-Asset (I), formerly AQR Risk Parity (renamed 2019-01-30 `[issuer]`) | mutual fund | 2010-09-30 | | 1.05% (0.83% adjusted) `[issuer]` |
| RPAR | RPAR Risk Parity | ETF | 2019-12-13 | | `[not checked]` (about 0.5%) |

### Defensive / low volatility (context: the equity sleeve)

| Ticker | Fund | Type | First bar `[data]` | Fee a year |
|---|---|---|---|---|
| SPLV | Invesco S&P 500 Low Volatility | ETF | 2011-05-05 | `[not checked]` (about 0.25%) |
| USMV | iShares MSCI USA Min Vol Factor | ETF | 2011-10-20 | `[not checked]` (about 0.15%) |

### Carry and multi-style premia (the family of survey-4's `ts-carry`)

| Ticker | Fund | Type | First bar `[data]` | Inception, notes | Fee a year |
|---|---|---|---|---|---|
| QSPIX | AQR Style Premia Alternative (I) | mutual fund | 2013-10-30 | 2013-10-30 `[issuer]`; long-short value, momentum, carry, defensive across asset classes | 1.53% adjusted (6.13% with short-sale and borrowing costs) `[issuer]` |
| QRPIX | AQR Alternative Risk Premia (I) | mutual fund | 2017-09-19 | | `[not checked]` |
| DBV | Invesco DB G10 Currency Harvest (FX carry) | ETF | - | **Yahoo returns 404: delisted, no keyless history.** The one pure carry ETF is gone. | - |

## The published backtest to set against the live record

- **AQR, "Time Series Momentum: Factors, Monthly"**, keyless xlsx from the AQR data library
  (<https://www.aqr.com/Insights/Datasets/Time-Series-Momentum-Factors-Monthly>), cached at
  `<cache_root>/downloads/survey-5/aqr/tsmom.xlsx`. `[data]` Monthly excess returns from
  1985-01 of the long/short 12-month TSMOM factor of Moskowitz, Ooi and Pedersen, "Time Series
  Momentum", Journal of Financial Economics 104(2), 2012, pp. 228-250 (citation printed in the
  file), "an updated and extended version of the paper data", rebuilt in full at each update.
  It is a **paper portfolio**: no fees, no costs stated. The paper's sample ends 2009, so the
  factor's 2010-2025 months are its post-sample years, and AQMIX (same manager, live, net)
  covers the same years.

## Tried and not usable keyless

- **SG CTA Index, SG Trend Index** (the industry's trend benchmark): the old direct feeds
  (`cib.societegenerale.com/fileadmin/indices_feeds/CTA_Historical.xls`, `Trend_Index_...`)
  answer with a bot wall (Incapsula), not data. DBMF is the keyless live proxy.
- **KFA MLM Index** (live since 1988): history only on request from the ETF sponsor
  `[search summary]`. KMLM is the live proxy since 2020.
- **BarclayHedge CTA Index**: not tried; its data pages need an account `[not checked]`.

## What this list cannot show

- **Survivorship.** Yahoo serves only funds still listed. Closed managed-futures and carry funds
  (DBV above; others not searched) are missing, so this panel's live record is if anything
  **better** than the family's.
- **Selection by me.** The tickers are the large, well-known funds of each family I could name
  before looking at any return. Their performance was not known to this lane when picked; I
  knew in general that managed futures had a poor 2010s and a strong 2022 (common knowledge,
  stated here so it can be discounted).
- **Different products.** Funds are long/short futures books at a 10-15% volatility target;
  `tsmom12` is long-only on six assets including two coins. Correlation, not equality, is the
  question.

## Literature on backtest-to-live haircuts (for step 2)

- **H1. Suhonen, Lennkh and Perez, "Quantifying Backtest Overfitting in Alternative Beta
  Strategies", Journal of Portfolio Management 43(2), Winter 2017.** `[secondary]` (CXO
  Advisory, mathinvestor.org, Alpha Architect write-ups; the paper itself not read; SSRN
  working paper March 2016). 215 bank "alternative beta" indices from 15 banks, backtests
  averaging 10.7 years, live periods 4.6 years: median Sharpe **1.20 backtest, 0.31 live, a
  73% haircut**; at least 50% in every asset class; worst in event-driven, value and **carry**,
  mildest in volatility and **trend** strategies; more complex strategies lose about 30% more.
  Only 18 of 215 matched their backtest live.
- **H2. Harvey and Liu, "Backtesting", Journal of Portfolio Management 42(1), Fall 2015,
  pp. 13-28.** `[secondary]` (PDF on the author's page, not read here). The flat 50% haircut
  is wrong: the multiple-testing haircut is non-linear, above 50% for Sharpe below ~0.4 and at
  most ~25% above 1.0 (for their example number of tests).
- **H3. Hurst, Ooi and Pedersen, "A Century of Evidence on Trend-Following Investing", Journal
  of Portfolio Management 44(1), Fall 2017, pp. 15-29.** `[pages read]` (text layer of the
  PDF; the exhibits are images and were not read). 67 markets, 1880-2016, 1/3/12-month TSMOM
  at 10% volatility; subtracts estimated costs and a **2% management and 20% performance fee**
  to mimic a fund; argues that TSMOM "captures well the performance of the managed futures
  indices and manager returns". Net Sharpe 0.76 for the full period is `[secondary]`.
- **H4. Wiecki, Campbell, Lent and Stauth, "All that Glitters Is Not Gold: Comparing Backtest
  and Out-of-Sample Performance on a Large Cohort of Trading Algorithms", SSRN 2745220, 2016
  (journal version `[not checked]`).** `[secondary]` 888 Quantopian equity algorithms: backtest Sharpe barely
  predicts live Sharpe (linear R² very low; 0.17 with a non-linear model); the more a strategy
  was backtested, the larger the gap.
- Already in survey-4 (R1): McLean and Pontiff 2016, 26% lower out of sample and 58% lower
  after publication for 97 stock anomalies.

## Step 2: the live check (card 045422c, script d9f5846, run 2026-11-18)

Card: [`cards/live-check.md`](cards/live-check.md), pushed before any number. Tables:
[`results/live-check.md`](results/live-check.md). Everything is a monthly return above the
13-week T-bill; our rules earn the bill on cash. Window L = 2010-02 to 2025-10; nothing after
2025-10 was read (held-out year unspent). The four re-scores reproduce their logged Sharpe
(`tsmom12` 1.05, `tsmom12-c00` 0.79, `where-vol` 1.07, `sixty-forty` 0.76, `hold-c17` 0.88).

**Logged as:** 4 rows of the new kind `live-check` in `tries.md` (`<rule>@live-L`, defined in
its header: descriptive re-score, not selectable, not counted). No strategy picked; the
family stays 65 mechanisms, 16 tested; no `ledger/tries.jsonl` row.

### What the numbers say (card's reading rules applied)

| | Corr. with family (L) | Reading | Sharpe in L | Family's Sharpe in L | Gap |
|---|---:|---|---:|---:|---:|
| `tsmom12` vs trend funds (TC) | 0.17 | does not move with it | 1.11 | 0.19 | +0.92 |
| `tsmom12-c00` (no coins) vs TC | 0.17 | does not | 1.02 | 0.19 | +0.83 |
| `where-vol` vs risk-parity funds (RC) | 0.43 | partly | 1.14 | 0.60 | +0.54 |
| `sixty-forty` vs RC | 0.85 | moves with it | 0.93 | 0.60 | +0.34 |

1. **`tsmom12` is not a trend fund.** Its monthly returns correlate 0.17 with the nine live
   trend funds, 0.09 with AQR's paper TSMOM factor, but 0.40 with SPY (without coins 0.72) and
   0.36 / 0.68 with the risk-parity funds. The funds are long/short and market-neutral on
   average (TC with SPY -0.06); our rule is long-only with a trend exit. The card's coin
   rule: the gap to TC is not the coins (`tsmom12-c00` is +0.83 ahead too). It is beta: in L,
   holding the same six assets (`hold-c17`) also has Sharpe 1.11, SPY 0.92. **In the live
   window `tsmom12` had exactly the Sharpe of holding everything (1.11 vs 1.11).** Its lead
   over holding is all from 1994-2009 (0.55 vs 0.26 above bills).
2. **Crash years: the funds gained, ours lost less than holding.** 2008: TC (RYMFX only)
   +7.1%, AQR factor +24.6%, `tsmom12` -1.6%, holding -12.9%, SPY -37.7%. 2020-02..03: TC
   +3.6%, `tsmom12` -14.1%, holding -11.8%. 2022: TC +17.6% (AQMIX +32.8%), `tsmom12` -12.9%,
   `where-vol` -27.4%, holding -37.7%. Our rule cuts losses by stepping out; it cannot gain
   from a fall, which is where live trend funds earn most of their keep.
3. **The haircut, trend family (the clean same-manager pair).** AQR's paper TSMOM factor:
   Sharpe **1.41** in the paper's sample (1985-2009) and **0.35** in L (25% kept). AQR's live
   fund AQMIX: **0.29** in L, 83% of the paper factor in the same months (fees and real
   costs), correlation 0.76 with it. **Total: h = 1 - 0.29 / 1.41 = 80%.** The fund panel
   (survivors only, so flattering) has 0.19, 54% of the factor. Most of the loss is the
   effect itself fading after its sample, not implementation. That is at the pessimistic end
   of the literature: H1's median bank strategy loses 73% (trend among the mildest), H2 caps
   the haircut at about 25% for Sharpe above 1, McLean-Pontiff 58% for stock anomalies.
4. **Our own split agrees for the part that is trend.** `tsmom12`'s lead over holding was
   +0.29 Sharpe in 1994-2009 and +0.00 in L: the trend edge kept nothing in our own data
   after 2009, the same story as the paper factor (25% kept) and the funds.
5. **`sixty-forty` and `where-vol`.** `sixty-forty` moves with the live risk-parity funds
   (0.85) and beats them by 0.34: a plain SPY/TLT mix over a decade when stocks and long
   bonds both did well, against funds with fees and commodity sleeves (RPAR 0.14, AQRIX 0.63).
   `where-vol` only partly (0.43); in 2022 it lost -27.4% against RC's -17.8%.
6. Context, not a candidate: the low-volatility ETFs (SPLV 0.74, USMV 0.90 in L) and AQR's
   multi-style funds (QSPIX 0.46, QRPIX 0.37; -22% in 2020, +23-28% in 2022). The one pure
   carry ETF (DBV) is delisted, so the carry family's live record is not keyless here.

Caveats: TC is survivors only; RYMFX changed method twice; the AQR factor is rebuilt at each
update ("AQR reconstructs the full history"), so its 1985-2009 numbers are today's version of
the paper data, not the 2012 printout; monthly Sharpe above bills is not the repo's daily
zero-rate Sharpe (`tsmom12` 1.05 there is 0.86 here over 1994-2025).

## Step 3: what to expect from `tsmom12` live, in plain words

**The card's rule** (backtest Sharpe 1.05 x (1 - h)) gives an expected live Sharpe of
**0.21** at the measured haircut (80%), 0.28 at the bank-strategy median (73%), 0.79 at
Harvey-Liu's ceiling (25%). Forward length with forward-1's formula (power 0.8, weekly,
skew +0.33, kurtosis 12.6 from the backtest; `docs/forward-registry.md` on `forward-1`,
PR #67): to show **Sharpe above 0** takes 7.3 years if the backtest were true, 12.7 at 0.79,
97 at 0.28 and **170 years at 0.21** (one-sided alpha 0.025, forward-1's per-rule level;
4.2 / 7.3 / 56 / 98 at alpha 0.10).

**But the haircut belongs on the trend edge, not on the whole Sharpe.** Most of `tsmom12`'s
Sharpe is the market return of the assets it holds; in L that part did not shrink at all.
The honest plain statement for a reader:

> Expect `tsmom12` to earn about what holding the same assets earns, with smaller losses in
> long bear markets. Do not expect it to beat holding on risk-adjusted return: its 0.17
> Sharpe lead in the 1994-2025 backtest was 0.00 to 0.04 in 2010-2025, and live trend
> funds kept only about a fifth of the published trend effect. What it does buy is a shallower worst year
> (2022: -13% against -38% for holding everything; 2008: -2% against -13%), not a higher
> Sharpe. And no forward test can tell us within a lifetime whether the Sharpe edge is real:
> a 0.17 lead with weekly correlation 0.80 needs **107 years** to show at alpha 0.025 (62 at
> 0.10); at the measured haircut, thousands. Showing merely "Sharpe above 0" takes 7 years
> if the backtest is right and over a century if the live funds are a guide.

(The Sharpe-gap power is an addition after the first run, marked in the results file: the
card's own lead measure, the mean weekly return difference, is below 0, because `tsmom12`
earns slightly less than holding at lower risk.)

What this means for the forward registry: like forward-1's `stop-0.25`, `tsmom12` against
holding is a **risk choice** (shallower worst loss), to be decided as one, not something to
wait for a forward verdict on. Its forward record is still worth keeping as a descriptive
check that the rule runs as built.

## Count and next

Family unchanged: 65 mechanisms, 16 tested, none passed; next test at p < 0.00154. Published
effects 0 for 5 after publication in this book, and the live funds of the one effect we run
show the same decay (paper 1.41, live 0.29).
