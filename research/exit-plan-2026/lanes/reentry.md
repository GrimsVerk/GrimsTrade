# Lane `reentry`: buying back in after a pop, and IPO waves as a top signal

Lane notes for the exit-plan-2026 report (night lead, 2026-11-18). Research only, not advice.
Numbers marked "our data" come from the scripts in `../scripts/reentry_*.py` run on cached free
data (Yahoo daily `^GSPC` from 1927-12 and `^IXIC` from 1971-02, price only; Shiller `ie_data.xls`;
Ken French T-bill; FRED `BAA10Y`), full output in `reentry-describe.txt` and `reentry-rules.txt`.
The one rule test follows the card `research/cards/reentry.md` (committed before any
number); its 32 rows are in `research/tries.md` (idea `reentry`). Facts from the web carry a link;
anything I could not check is marked (unverified).

## Bottom line

1. **No re-entry rule beat simply buying back at once**, even when we look only at months with
   high valuations like now. 7 rules were tested on the S&P 500 from 1928 and none passed the
   pass bar set on the card. The wait-for-a-crash rules win big when the sale happens near the
   real top (1929, 1968, 1972, 1987, 2000, 2007: mostly 1.3-1.6x the wealth of buying back at
   once, after 10 years). They mostly lose when the sale is 2-3 years early (1996-12 and
   1997-12: 0.64-0.97x). Sold 15 months early (1998-12), they still won. There is no reliable
   way to know in advance which of the two cases you are in.
2. **What a plan can do is cap regret, not add return.** Spreading the purchase over 12 months
   cost about 3% of 10-year wealth in the typical month, and its worst tenth of outcomes was
   0.90x. Waiting for a crash with no deadline had a worst tenth of 0.33-0.52x: the cash sat out
   a market that never fell far enough. Adding a deadline (fully back in within 24 months)
   lifted that worst tenth to 0.72x.
3. **A hot IPO market is a weak top signal.** IPO waves do come in late bull markets and IPOs
   almost vanish in busts. But the lead time ranges from 0 to more than 3 years, and most hot
   years were not followed by a bear market within 2 years (7 of the 11 years since 1980 with
   at least 300 IPOs). 2026 is a record year in dollars ($149bn, driven by SpaceX's $75bn IPO,
   the largest ever). By number of deals it is not a hot year: 123 IPOs, against 397 in 2021.
   A dead IPO market at a bottom lags the market low by 1-2 years, so it is useless as a buy
   signal.

## Part 1: re-entry

### How long busts lasted

S&P 500 bear markets, daily closes, price only (no dividends) (our data, `reentry-describe.txt`):

| Peak | Trough | Fall | Peak to trough | Trough back to old peak |
|---|---|---:|---:|---:|
| 1929-09-16 | 1932-06-01 | -86% | 32 months | 268 months (1954-09) |
| 1956-08 | 1957-10 | -22% | 15 | 11 |
| 1961-12 | 1962-06 | -28% | 6 | 14 |
| 1966-02 | 1966-10 | -22% | 8 | 7 |
| 1968-11 | 1970-05 | -36% | 18 | 21 |
| 1973-01 | 1974-10 | -48% | 21 | 69 (1980-07) |
| 1980-11 | 1982-08 | -27% | 20 | 3 |
| 1987-08 | 1987-12 | -34% | 3 | 20 |
| 2000-03-24 | 2002-10-09 | -49% | 31 | 56 (2007-05) |
| 2007-10-09 | 2009-03-09 | -57% | 17 | 49 (2013-03) |
| 2020-02 | 2020-03 | -34% | 1 | 5 |
| 2022-01 | 2022-10 | -25% | 9 | 15 |

- **Nasdaq after 2000:** -78% (2000-03-10 to 2002-10-09). The old peak was not regained until
  2015-04-23, **15.1 years** later, price only (our data).
- **1929:** price-only recovery took 25 years. Counting dividends and the 1930s deflation, a
  buyer at the peak was back to even by about late 1936
  ([Hulbert, via History News Network](https://www.historynewsnetwork.org/article/79770)).
  1936-37 was itself a top, followed by another bear market.
- **Japan:** the Nikkei 225 closed at a record 38,915.87 on 1989-12-29 and did not close above it
  until 2024-02-22 (39,098.68), **34 years** later
  ([Boston Globe/AP](https://www.bostonglobe.com/2024/02/22/business/japans-nikkei-stock-index-breaks-its-1989-record-surges-an-all-time-high/),
  [Bloomberg](https://www.bloomberg.com/news/articles/2024-02-22/japan-s-nikkei-hits-intraday-high-surging-past-1989-record)).
- The long recoveries (1929, 1973, Nasdaq 2000, Japan 1990) all came after busts that began from
  very high valuations or real bubbles. That is the scenario studied here (valuations are very
  high now), so the short recoveries of 2020 and 2022 are not a fair guide.

### Buying at -20%, -30%, -40%

Bought at the first close at each depth below the all-time high. S&P 500 (12 bear markets
1929-2022), price only (our data):

| Bought at | n | Median further fall | Fell >=10% more | 1y later (median, % positive) | 3y | 5y |
|---|---:|---:|---:|---|---|---|
| -20% | 12 | -9% | 42% | +20%, 67% | +36%, 83% | +34%, 82% |
| -30% | 7 | -25% | 57% | +12%, 57% | +20%, 86% | +27%, 86% |
| -40% | 4 | -20% | 100% | +14%, 75% | +33%, 75% | +62%, 75% |

- The exceptions are the busts after bubbles. Buying at -40% in November 1929 still lost 51%
  over 5 years, after a further 77% fall. On the Nasdaq, buying in 2000 at -20%, -30% or -40%
  meant a further fall of 63-70% and a loss of 27-47% after 5 years.
- On the Nasdaq (13 bear markets since 1971), buying at -20% gave a median 5-year return of
  +101% (91% positive). Only two Nasdaq bear markets ever reached -40% (1973-74 and 2000-02).

### Signals for the bottom (our data unless linked)

- **Trend (10-month average, 200-day average).** After the low, the first month-end close above
  the 10-month average came a median of **3.9 months later, 20% above the low** (S&P,
  12 bears, range 0.6-6.9 months). The 200-day average gave 3.5 months and 18%. On the Nasdaq:
  2.1 months and 25%. The commonly quoted "about 7 months" is true only of the slow cases (1958,
  1987-88, 2002-03). The ~20% above the low holds. Trend rules rarely gave false buy signals
  inside a bear market once it was down 20%: one on the S&P and three on the Nasdaq, all in
  2000-02. Background:
  [Faber, A Quantitative Approach to Tactical Asset Allocation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461).
- **VIX peak.** In the 4 S&P bear markets since 1990, the VIX peaked **7-219 days before the
  low**, at prices 7-17% above it (2008: VIX 80.9 on 2008-11-20, low on 2009-03-09; 2020: VIX
  82.7 on 03-16, low on 03-23). A VIX spike marks panic, not the exact low.
- **Credit spread (Baa minus 10-year Treasury).** It peaked on the very day of the low in 2002
  and 2020, and 43-103 days before it in 1987, 2008 and 2022. It is close, but a peak is only
  known after the fact.
- **The Fed's first rate cut is not a buy signal.** From the close on the day of the first cut
  of each easing cycle, the S&P later fell a further **42%** (2001-01-03) and **56%**
  (2007-09-18). After the 1998, 2019 and 2024 first cuts the further fall was 9-25%.
- **CAPE back to its median.** Measured with earnings lagged 3 months, the CAPE was last at or
  below its long-run median (now 18.1) from 2008-11 to 2009-06. It is now **39.7**, the 97th
  percentile since 1928. Only 1998-12 to 2000-10 was higher. Since late 2016 the CAPE has been in
  its historical top fifth in 99% of months. Waiting for "cheap" has meant waiting a decade or
  more.

### Lump sum vs spreading purchases over time

- Vanguard 2012 (US, UK, Australia) found that investing a lump sum at once beat spreading it
  over 12 months about **two-thirds** of the time
  ([Vanguard 2012, copy](https://militarymoneymanual.com/wp-content/uploads/2021/08/Dollar-Cost-Averaging-Just-Means-Taking-Risk-Later-Vanguard.pdf)).
  Vanguard 2023 found the lump sum ahead **68%** of the time (1976-2022). It also found that
  spreading purchases still beat holding cash and is a reasonable choice for an investor who
  fears regret
  ([Vanguard 2023](https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf)).
- Our data agrees. A 12-month spread lost to buying at once in 67% of start months since 1928,
  with a median cost of 3.4% of 10-year wealth.
- The behavioural case: the realistic alternative to a fixed schedule is often not a lump sum
  but staying in cash, and staying in cash is what hurt most in our test.

### The risk that the pop comes late or never

- **Shiller and Greenspan, 1996.** Greenspan's "irrational exuberance" speech was on 1996-12-05
  ([Federal Reserve](https://www.federalreserve.gov/boarddocs/speeches/1996/19961205.htm)).
  Shiller had warned the Fed Board days before (unverified date: 1996-12-03 per his own
  accounts). The S&P closed at 744 that day and then doubled to 1,527 by March 2000. Even the
  2002 low (777) was above the 1996 level. It first closed below 744 in 2008-09 (low 676.53 on
  2009-03-09) (our data).
- **Grantham.** GMO was early on both the Japan and the dot-com bubbles ("two to three years too
  early", in Grantham's own account). Its assets fell from $31bn (1998) to $20bn (2001) as
  clients left before being proven right
  ([Institutional Investor](https://www.institutionalinvestor.com/article/b1hjlb0qs4c807/GMO-Is-Feeling-Pain-Reminiscent-of-the-Late-1990s),
  [top1000funds](https://www.top1000funds.com/2012/04/gmo%E2%80%99s-grantham-bets-against-irrational-markets/)).
  In January 2021 he again called a bubble
  ([GMO, Waiting for the Last Dance](https://www.gmo.com/globalassets/articles/viewpoints/2021/waiting-for-the-last-dance_1-2021.pdf)).
  The S&P fell 25% in 2022 and then passed its old high in January 2024 (our data).
- **Selling 1-3 years early, from our test.** Selling in 1996-12 or 1997-12 and waiting for a
  -20% drop or for a cheap CAPE left the investor with 0.64-0.97x the wealth of buying back at
  once. Waiting for a cheap CAPE never got back in at all within 10 years.

### Rules test (card `research/cards/reentry.md`)

Setup: sell at month `t`; cash earns T-bills; each rule decides at month-end closes using only
data known then. We compare the rule's wealth after 10 years with buying back at once (ratio
R; above 1 means the rule did better). The sample "B" holds the months when the CAPE was in its
own top fifth up to that date (the situation in late 2026). That is 390 start months, but only
**8 separate episodes**, so every number below rests on a few independent cases. S&P 500
total return, 1928-2016 starts (our data, `reentry-rules.txt`).

| Rule | B median R | B share R>1 | B worst tenth | All-months mean R | B before 1972 (median, share) | B from 1972 | Passes |
|---|---:|---:|---:|---:|---|---|---|
| `dca12` (12 monthly tranches) | 0.97 | 31% | 0.90 | 0.98 | 0.98, 39% | 0.97, 27% | no |
| `dd20` (all in at -20%) | 1.00 | 43% | 0.52 | 0.94 | 1.07, 65% | 1.00, 31% | no |
| `dd30` (all in at -30%) | 1.01 | 51% | 0.35 | 0.89 | 1.09, 64% | 1.00, 44% | no |
| `dd20-sma10` (-20%, then trend up) | 1.00 | 43% | 0.51 | 0.99 | 1.09, 62% | 0.96, 32% | no |
| `cape-median` | 0.96 | 48% | 0.35 | 0.91 | 1.02, 53% | 0.80, 45% | no |
| `staged-24` (1/3 at -20/-30/-40%, rest at 24 months) | 0.92 | 35% | 0.72 | 0.96 | 1.00, 48% | 0.90, 28% | no |
| `dd30-24` (-30% or 24 months) | 0.91 | 31% | 0.72 | 0.96 | 0.96, 39% | 0.88, 26% | no |

- The pass bar required, in sample B, a median R above 1 with R above 1 in at least 55% of
  months, in both halves. Before 1972 the plain drawdown rules passed (they won about 64% of
  the time). From 1972 on, none did, mostly because of the 1990s.
- On the Nasdaq (robustness, from 1981), the drawdown rules won in only 4-13% of high-CAPE
  months.
- Sold exactly at the named tops, every waiting rule won: 1929-08 1.3-3.3x, 1968-11
  1.1-1.6x, 1972-12 1.1-1.7x, 1987-08 1.2-1.4x, 2000-03 1.1-1.7x, 2007-10 1.1-1.7x. Sold
  15 months early (1998-12), they won as well (1.0-1.5x). Sold 2-3 years early (1996-12,
  1997-12), they mostly lost (0.64-0.97x; only `dd30` from 1997-12 won, at 1.07x). Sold in
  1937-02, the rules bought back at once, because the market was still far below its 1929
  high.
- Limits: price data ends 2026-11-12; Shiller's dividends are smoothed; fills are at the
  month-end close; there are no taxes or fees, and no currency effect for a euro investor.

### A re-entry rule set the evidence supports

The evidence gives no rule that adds return. A plan can only limit two regrets: buying back
just before the crash, and never buying back. Taken together:

1. **Set a hard deadline now:** fully back in stocks by **31 Dec 2028** (24 months after the
   sale), whatever has happened. Open-ended waiting was the costliest choice in every sample.
2. **Before the deadline, buy in thirds on falls of the S&P 500 (or the index you will own) from
   its all-time high:** 1/3 at -20%, 1/3 at -30%, 1/3 at -40% (`staged-24`). Average cost vs
   buying at once: about 3-4% of 10-year wealth (mean R 0.96-0.97). In high-valuation months the median cost was about 8%. Worst tenth: 0.72x. In a
   real 1968-, 1973-, 2000- or 2008-style bust it gave 1.4-1.6x.
3. **The simpler alternative:** 12 equal monthly purchases from January 2027 (`dca12`). Median
   cost about 3%, worst tenth 0.90x. This is the better choice if you care more about not
   missing a rally than about catching a crash.
4. **Use VIX above about 45, a peak in credit spreads, or a 200-day-average cross after a -30%
   fall only to bring forward a tranche that is already due.** Never use them as a reason to
   wait longer. The Fed's first cut and "CAPE back to median" are not buy signals.
5. **Write the rule down now** and follow it mechanically. The 1929 and 2000 cases show that a
   -20% fall can become -50% to -80%, and the 1996 case shows that the fall can arrive only
   after the market has doubled.

Honest uncertainty: 8 high-valuation episodes since 1928, and only 3 since 1972. Rule 2 is
insurance against regret, not an edge.

**Review round 2 (2026-11-18): the default is swapped.** Points 2 and 3 above compared
`staged-24` on all-months and high-CAPE numbers with `dca12` on high-CAPE numbers only. Read
in the same sample B (10-year horizon, `reentry-rules.txt`): `dca12` median 0.97, worst tenth
0.90, mean 0.99, share above 1 31%; `staged-24` median 0.92, worst tenth 0.72, mean 0.97, share
above 1 35%. From 1972: 0.97 / 0.90 against 0.90 / 0.68. Nasdaq sample B: 0.96 / 0.86 / 35%
against 0.89 / 0.69 / 5%. At the named tops before real busts (1929-08, 1968-11, 1972-12,
2000-03, 2007-10) `staged-24` gave 1.40-1.61 against 1.09-1.34; sold early (1996-12, 1997-12)
0.64-0.71 against 0.88-0.93. So in the sample that fits today `dca12` was better on the median
and the bad tail, and `staged-24` is a bet that a real bust comes. The report (section 8.2) now
makes `dca12` the default and keeps `staged-24` as that bet. No new test: the same table, read
side by side; the choice of default was made after seeing it.

## Part 2: IPO waves and sentiment as top signals

### Ritter's counts

Operating-company IPOs on NYSE and Nasdaq; Ritter excludes SPACs, ADRs, offers under $5 and
similar. From [Ritter, IPO Statistics (2026-11-05 edition), Table 1](https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf);
[data page](https://site.warrington.ufl.edu/ritter/ipo-data/):

| Year | IPOs | Mean first-day return | Proceeds | What followed |
|---|---:|---:|---:|---|
| 1983 | 451 | 9.9% | $8.9bn | Nasdaq -31% (1983-06 to 1984-07). The S&P had no 20% bear market |
| 1986 | 393 | 6.1% | $13.4bn | 1987 crash: S&P peak 1987-08, -34% |
| 1993 | 510 | 12.7% | $31.4bn | No bear market until 2000 |
| 1996 | **677** (record count) | 17.2% | $42.1bn | The S&P doubled before its 2000 peak |
| 1999 | 476 | **71.2%** | $64.7bn | Peak 2000-03 |
| 2000 | 380 | 56.3% | $64.8bn | -49% (S&P), -78% (Nasdaq) |
| 2001-03 | 80, 66, 63 | 14.0%, 9.1%, 11.7% | | Bust and low |
| 2007 | 159 | 14.0% | $35.7bn | Peak 2007-10 with no IPO wave beforehand (a miss) |
| 2008-09 | 21, 41 | 5.7%, 9.8% | | Low 2009-03 |
| 2014 | 206 | 15.5% | $42.2bn | No bear market until 2020 (Covid) |
| 2020 | 165 (+248 SPACs) | 41.6% | $61.9bn | |
| 2021 | 311 (+613 SPACs) | 32.1% | **$119.4bn** | 2022: S&P -25%, Nasdaq -36% |
| 2022-23 | 38, 54 | 48.9%, 11.9% | $7.0bn, $11.9bn | Low 2022-10 |
| 2025 | 90 (+144 SPACs) | 29.3% | $39.0bn | |

SPAC counts are from Ritter's Table 15b in the same file.

- **Do IPO waves peak near tops?** Loosely. Take the 11 years since 1980 with at least 300 IPOs
  (1983, 1986, 1992-1997, 1999, 2000, 2021). An S&P bear market began within 24 months of the
  year's end after 4 of them (1986, 1999, 2000, 2021) and not after 7. So **7 of 11 were false
  alarms**; 1997 came close, followed by a 19% fall in 1998. (I chose the 300 threshold after
  seeing the table: this is a description, not a tested rule.)
- **Lead time:** from 0 (2000, 2021) to 39 months (1996 to the 2000 peak) by deal count. Deal
  counts peaked 3 years early in the 1990s.
- **First-day returns did better.** The years with a mean first-day return of 30% or more
  (1999, 2000, 2020, 2021) all came less than 2 years before or during a top. The exception was
  2022's 48.9%, from 38 deals in a falling market. Four or five episodes cannot prove anything.
- Ibbotson and Jaffe described "hot issue" markets in 1975: periods when first-day returns are
  high and persist from month to month
  ([JF 1975](https://doi.org/10.1111/j.1540-6261.1975.tb01019.x)).
- Lowry 2003 found that IPO volume is driven mostly by firms' need for capital and by investor
  sentiment, with high-volume periods followed by poor returns on the new issues
  ([JFE 2003](https://doi.org/10.1016/S0304-405X(02)00230-X); paraphrase from memory,
  (unverified) wording).
- Pastor and Veronesi 2005 give a rational account. IPO waves follow strong market returns and
  are followed by weaker ones because firms go public when expected returns fall, so a wave
  does not prove a bubble
  ([abstract](https://ideas.repec.org/a/bla/jfinan/v60y2005i4p1713-1757.html)).

### Equity issuance and sentiment

- **Baker and Wurgler 2000.** The equity share of new issues (equity / (equity + debt)) predicted
  US market returns from 1928 to 1997, in both halves of the sample. When it was in its bottom
  quartile, the next year's value-weighted return averaged 14%. In its top quartile, the next
  year's return averaged -6% (the minus sign is garbled in the PDF text; the reading follows the
  paper's widely quoted result)
  ([paper](https://pages.stern.nyu.edu/~jwurgler/papers/equityshare.pdf)).
  Butler, Grullon and Weston (2005) attribute the effect to "pseudo market timing", a
  small-sample bias
  ([JF 2005](https://ideas.repec.org/a/bla/jfinan/v60y2005i2p963-986.html)). Baker, Taliaferro
  and Wurgler answer that the bias explains only about 1% of it
  ([paper](https://pages.stern.nyu.edu/%7Ejwurgler/papers/wurgler_baker_taliaferro.pdf)).
  How well it predicted out of sample after 1997 is (unverified) here. Goyal and Welch (2008)
  include it among predictors that mostly fail out of sample; its exact score there was not
  checked.
- **Baker-Wurgler sentiment index (2006 JF, 2007 JEP).** It combines IPO count, first-day
  returns, the equity share, turnover, the closed-end fund discount and the dividend premium.
  It mainly predicts the cross-section: after high sentiment, speculative, young and
  unprofitable stocks do worst ([JEP 2007](https://doi.org/10.1257/jep.21.2.129)). Its record
  for timing the whole market is weak. Huang, Jiang, Tu and Zhou (2015) build an "aligned" index
  with in-sample R² more than 5 times and out-of-sample R² more than 10 times those of
  Baker-Wurgler (via summaries; (unverified) exact numbers)
  ([RFS 2015](https://ideas.repec.org/a/oup/rfinst/v28y2015i3p791-837..html)).
- **Greenwood, Shleifer and You 2019, "Bubbles for Fama".** When an industry beats the market by
  100% over 2 years, the chance of a crash (a 40% fall within 2 years) is about 53%, against
  about 20% after a 50% run-up (NBER version). Issuance, volatility, turnover and an
  accelerating price path raise that chance further. But average returns after such run-ups
  roughly match the market, so a run-up alone gives no edge
  ([NBER w23191](https://www.nber.org/system/files/working_papers/w23191/w23191.pdf),
  [JFE 2019](https://econpapers.repec.org/RePEc:eee:jfinec:v:131:y:2019:i:1:p:20-43)). This is
  the closest academic support for the common idea that hot issuance marks a bubble, and it is
  about industries (AI), not the whole index.
- **The IPO stocks themselves:** Loughran and Ritter (1995) found that IPO firms of 1970-1990
  returned about 5% a year over 5 years, against 12% for similar non-issuers
  ([JF 1995](https://doi.org/10.1111/j.1540-6261.1995.tb05166.x)). Ritter's 1980-2024 update:
  the average 3-year return from the first close was 20.5 points below the market, about
  -5.5% a year (Table 16, same file). Buying the hot AI IPOs is a separate, bad bet.

### 2025-2026

- **2025:** 90 IPOs by Ritter's count, $39.0bn raised, mean first-day return 29.3%, the highest
  since 2022 (Ritter, above). Renaissance Capital, which counts more widely, had 202 IPOs.
- **2026 to date:** 123 IPOs, $149.0bn raised (+314% on 2025), number of deals -36%
  (Renaissance stats page, read 2026-11-18,
  [link](https://www.renaissancecapital.com/IPO-Center/Stats?market=us)). That beats 2021's
  record $142.4bn from 397 IPOs
  ([Renaissance 2021 review](https://www.renaissancecapital.com/IPO-Center/News/89606/Renaissance-Capitals-2021-US-IPO-Market-Review)).
  As of 8 September, $146bn had been raised, $71bn excluding SpaceX
  ([Renaissance Fall 2026 preview](https://www.renaissancecapital.com/review/US_Fall_Preview_2026_Public.pdf)).
- **The big deals:**
  - **SpaceX** (merged with xAI in 2026): priced 2026-06-11 at $135, raising about $75bn at about
    a $1.77tn valuation, the largest IPO ever. The previous record was Saudi Aramco's $25.6bn in
    2019
    ([Business Recorder/Reuters](https://www.brecorder.com/news/amp/40425123),
    [TechRepublic](https://techrepublic.com/article/news-spacex-ipo-price-valuation/)).
  - **SK hynix:** a $26.5bn Nasdaq ADR in July (secondary sources; (unverified)).
  - **Cerebras:** 2026-05-14, $5.55bn, the largest US AI-chip IPO
    ([Dealroom](https://dealroom.co/news/128936-cerebras-raises-5-55b-in-biggest-us-ipo-of-2026/)).
  - **Anthropic:** Nasdaq lists ANT as starting to trade on **2026-11-19**
    ([Nasdaq Trader notice, 2026-11-11](https://nasdaqtrader.com/TraderNews.aspx?id=DTN2026-28)).
    Reported range $70-78 for 825m shares (about $58-64bn, around a $1tn valuation; secondary
    sources, (unverified) until priced). Its listing comes after a sharp tech sell-off the day
    after the US midterms
    ([investingLive/WSJ](https://investinglive.com/stock-market-update/wsj-anthropic-targets-nasdaq-debut-next-week-under-ticker-ant-despite-tech-selloff/)).
  - **OpenAI:** an IPO is talked about but (unverified).
- **Is it extreme?** In dollars, yes: a record, carried by a few mega-deals. In number of deals,
  no: 123 is a third of 2021's count and a fifth of 1996's. Relative to the size of the market,
  probably not: 2026 proceeds may be about 0.2% of US market value against about 0.4% in 2000
  ((unverified), rough market-value estimates). The 1999-2000 signature (hundreds of small,
  unprofitable firms doubling on day one) is not what 2026 looks like. 2026 looks more like a
  handful of giant private companies cashing in, which fits Pastor and Veronesi's rational
  story and Greenwood, Shleifer and You's "issuance in a hot industry" warning equally well.
- Market context, our data: the Nasdaq was 8.2% below its 2026-10-06 high on 2026-11-12, and the
  S&P 500 2.9% below.

### "Almost no IPOs at bottoms": true, but useless for timing

True: 2002-03 had 66 and 63 IPOs, 2008-09 had 21 and 41, 2022-23 had 38 and 54 (Ritter). But
the IPO count stays low for 1-2 years after the market's low. 2003 had 63 IPOs while the S&P
rose 26%. 2009 had 41 while it rose about 65% from the March low. 2023 had 54, and the S&P
passed its old high in January 2024 with 2024 still at only 73. By the time IPOs come back, the
market is already well off its low. A shut IPO window tells you a bust has happened; it does
not tell you when to buy.

### Verdict on IPOs and sentiment as a top signal

- **Lead time:** 0-3+ years.
- **False alarms:** about 2 of every 3 hot years by deal count (1983, 1993, 1996 and 2014 are the
  clear ones; 1992-95 and 1997 too). Some tops had no wave at all (2007).
- **Use:** a "late cycle" warning that justifies not adding money and setting the re-entry plan
  above. It is not a sell date, and it is not a reason to stay in cash for years.
- The commonly heard claim that IPO waves come near tops and not at bottoms is broadly right
  about bottoms and only loosely right about tops.

## Could not verify

Baker-Wurgler out-of-sample record after 1997 (and its Goyal-Welch score); Lowry 2003 exact
wording; Huang et al. exact R²; the SK hynix ADR size; Anthropic's final price and size (not
priced at time of writing); OpenAI IPO timing; market-value ratios for 2000 vs 2026; the date of
Shiller's 1996 Fed briefing.
