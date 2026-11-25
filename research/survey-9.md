# Survey 9: the long-history trend evidence next to the project's finding (2026-11-25, UTC)

Lane `survey-9` of the night lead (WIDER lane, literature only, fake money). Branch `survey-9`
from `origin/main` (`5feb0bb`). No test was run, no price or return was loaded and no statistic
was computed on any data. Papers were read with WebSearch, WebFetch and, for PDFs, `pdftotext`
(and `tesseract` for one scanned paper). PDFs cached under `~/data/grimstrade/survey-9/`
(20 MB, not committed).

**The project's finding this survey checks** (`SUMMARY.md` "What we know now"; records
`insure-2`, `gap-2002-1`, `insure-1870-1`, `jst-autocorr-1`/`-2`, `rev-costloss-1`,
`calm-drag-1`, `insure-1709-1`): `tsmom12` (long-only, unscaled, in or cash on the 12-month
sign) is crash insurance, not an edge. It earns about what holding the same assets earns
(2010-2025: Sharpe 1.11 each), loses less in slow falls of 25%+ (US since 1927: 20 of 21; 13
developed markets since 1966: 17 of 18; JST 1870-1965: 9 of 9; UK 1709-1866: 7 of 7), fails in
fast crashes (1987, 2020, South Sea 1720), and trails in calm markets (about 2 points a year;
since 2002 about 1 point behind on the S&P 500). Before 1966 its timing, beyond lower exposure
and random dates, is not separable from the early data's own autocorrelation (JST: an AR(1) of
0.19 gives most of the gap; UK 1709-1866: beats AR(1) worlds, p 0.035, not a block bootstrap,
p 0.115).

Read-depth labels: `[pages read]` = the relevant sections of the full text read tonight;
`[abstract]` = abstract or publisher page only; `[secondary]` = a third-party summary
(named); `[prior lane]` = read by an earlier lane, cited from its file and not re-read.

## The answer on one screen

- **No published long-history paper tests the project's rule against the project's
  comparison.** The famous century studies (Moskowitz-Ooi-Pedersen, Hurst-Ooi-Pedersen,
  Lempérière et al., Baltussen et al., Greyserman-Kaminski) test a *long-short,
  volatility-scaled* book on many futures or spot series, and score it against zero or against
  a 60/40 portfolio, not against holding the same assets in falls. Their "edge" lives in three
  things `tsmom12` does not have: shorts, volatility scaling and dozens of markets.
- **Where papers do compare with holding the same assets, they agree with the project.**
  Without volatility scaling, time-series momentum and buy-and-hold have about the same returns
  and alphas (Kim, Tse and Wald 2016). A rule that is long when an asset's *historical mean* is
  positive does as well as MOP's 12-month rule, and both earn mainly on their long legs (Huang,
  Li, Wang and Zhou 2020). Long-only timing of US stocks beats buy-and-hold only through a few
  bear markets (1930-31, 1973-74, 2001-02, 2007-08) and lost to it through 1975-1999
  (Zakamulin 2014); Faber's 10-month rule on the S&P 500 since 1901 kept about the return and
  cut the worst fall (-50% against -84%) but "does not widen the gap" over 1940-2000; long-only
  momentum "resembles a portfolio insurance strategy" (Zakamulin and Giner 2022).
- **The crisis evidence agrees in shape.** Trend gained in most slow bear markets (8 of 10
  worst 60/40 drawdowns since 1880, HOP; the 8 worst S&P drawdowns 1985-2018, Harvey et al.
  2019), misses fast crashes (1987, HOP), is weak for about four years after a crisis starts
  (Hutchinson and O'Brien 2014), and is hurt by turning points, the corrections and rebounds
  (Goulding, Harvey and Mazzoleni 2023/2024). The difference: long-short books *gain* in falls;
  long-only `tsmom12` only *loses less*. That is the short side (`#83`, `#89`), not a
  contradiction.
- **Stale or averaged early prices: the literature mostly does not ask.** Only MOP avoid the
  problem by design (liquid futures, mostly from 1985). HOP's early commodity prices are "an
  average of high and low prices" (1877 on); Working (1960) and Schwert (1990) show that such
  averaging alone puts about +0.25 into the lag-1 autocorrelation of monthly changes, which a
  trend rule harvests. Lempérière et al. call early index prices "clean, well-defined" and run
  no check. The one published check found is Baltussen et al.'s one-month signal delay (trend
  survives with a "limited" Sharpe reduction), which removes a pure averaging artefact but not
  longer-lag autocorrelation from thin or slow markets; the same paper argues data errors bias
  *towards* the null, which is wrong for averaging and staleness (they bias towards trend). On
  daily data, a one-day delay cut the best Brock-Lakonishok-LeBaron rule's mean return from
  17.2% to 7.8% a year and its Sharpe criterion lost significance (Sullivan, Timmermann and
  White 1999).
- **So the project's caution on pre-1966 timing is stricter than the literature, not at odds
  with it.** None of the century papers scores trend timing against an autocorrelation-matched
  null (AR(1) worlds, block bootstrap), as `insure-1709-1` did. MOP's own decomposition says
  time-series momentum profits *are* positive autocovariance, so "not separable from
  autocorrelation" is the expected reading if the early autocorrelation is real; the open
  question, unanswered in the literature too, is whether the early autocorrelation was real
  and tradable or a property of how the indices were built.
- **Power: the literature agrees the question cannot be settled on one market's history.**
  Zakamulin and Giner (2022): 80% power to show long-only momentum beats buy-and-hold needs
  about 250 years of monthly data; the project's `power-map-1` needs 72 years for +0.10 Sharpe
  against `tsmom12`.

## The table

| # | Source (read depth) | Data and span | Rule | Claim: edge or insurance | Controls for holding the same assets? | Stale or averaged early data addressed? | Against the project's records |
|---|---|---|---|---|---|---|---|
| 1 | Moskowitz, Ooi, Pedersen 2012, JFE 104 `[pages read]` | 58 liquid futures and forwards (24 commodities, 12 FX, 9 equity indices, 13 bonds), Jan 1965 to Dec 2009, monthly; Bloomberg/Datastream | sign of 12-month excess return, long-short, 40%/vol per asset | **edge**: diversified TSMOM alpha positive after passive long, smile (best in extreme quarters) | **partly**: regressions on each asset's passive long and a diversified passive long (Fig. 3); decomposition (Lo-MacKinlay/Lewellen): profits from positive auto-covariance, the mean-return part small | **yes, by design**: "we focus on the most liquid instruments to avoid returns being contaminated by illiquidity or stale price issues"; equity-microstructure staleness cited (Ahn et al. 2002) | Agrees the sample is clean; their edge needs shorts and vol scaling. Their decomposition (auto-covariance, not mean) is disputed by #9 |
| 2 | Hurst, Ooi, Pedersen 2017, JPM 44(1) `[pages read]` | 67 markets (29 commodities, 11 equity, 15 bonds, 12 FX), 1880-2016, monthly end-of-month; pre-futures: cash indices financed at local short rates (MSCI, Ibbotson, GFD, Yale ICF); commodities hand-transcribed from CBOT annual reports 1877-1951 | 1/3/12-month TSMOM equal-weighted, long-short, 10% ex ante vol, costs (6x today's before 1993) and 2/20 fees | **edge** (positive every decade) plus **insurance** (positive in 8 of 10 worst 60/40 drawdowns; average drawdown about 15 months; "may not perform well" in fast crashes such as 1987) | **no**: scored against zero and as a 20% sleeve of 60/40, not against holding the same markets | **no check**: early commodities use "the average of high and low prices before closing prices are available"; footnote 6: not "implementable back in the 1880s" | Agrees on slow falls and the fast-crash miss. Its early commodity data are averaged, the artefact `jst-autocorr-1` modelled; no lag or bootstrap check |
| 3 | Lempérière, Deremble, Seager, Potters, Bouchaud 2014, J. Investment Strategies (arXiv 1404.3274) `[pages read]` | 7 commodities, 7 bond, 7 index, 6 FX futures from 1960; spot back to 1800 (indices US from 1791, UK from 1693, commodities 1800, bonds from 1918, FX from 1973); all GFD; monthly closes | EMA trend (n = 5 months), sign, vol-normalised, long-short, no costs | **edge**: t 10.5 over two centuries, 9.8 after removing the beta to long-only; indices Sharpe 0.7 against 0.4 for the drift; 1800-1850 Sharpe 0.6 against drift 0.06; trend P&L only +15% correlated with long-only | **yes, linearly**: "de-biased" t-stat after regressing out the long-only P&L of the same series | **no check**: stocks and commodities "relatively easy to get clean, well-defined prices"; bonds before 1918 dropped as illiquid, Bretton Woods FX dropped | Disagrees most directly: a strong edge on the earliest index data, where the project found lag-1 autocorrelation +0.23 to +0.50 (UK monthly shares, `insure-1709-1`). A 5-month EMA is the signal most exposed to short-lag autocorrelation; whether GFD's early UK series is the same as the BoE one is not checked |
| 4 | Greyserman and Kaminski 2014, *Trend Following with Managed Futures* (Wiley) `[secondary]` (CFA Institute review; span from Geczy-Samonov's deck; risk.net review behind a script wall) | about 800 years, 1223-2013 (per Geczy-Samonov's citation), spot data | a long-short trend system on spot prices | **edge plus crisis alpha**: a search snippet of the risk.net review gives trend Sharpe about 1.16 against 0.47 for buy-and-hold `[not checked]`; the CFA reviewer also says the authors find "buying on dips and buy and hold are more productive than trying to chase returns with trend followers" `[not checked; contradicts the snippet]` | against buy-and-hold, details not read | the CFA reviewer: "the portfolio tested could not actually be mimicked in the marketplace"; HOP footnote 5: spot-based returns are "not implementable" (no roll) | Not usable as evidence either way at this reading depth |
| 5 | Geczy and Samonov 2016, FAJ 72(5) "Two Centuries of Price-Return Momentum"; 2017 SSRN "Two Centuries of Multi-Asset Momentum" `[abstract]` plus their 2017 Wharton deck `[pages read]` | US stocks 1801-1926 (hand-built) and 1927-; country equities, bonds, FX, commodities 1800-2014 from GFD; US sectors from Cowles' 68 industries | mainly cross-sectional 12-2 momentum; time-series momentum added in 2017 | **edge**, cross-sectional; time-series "worked but cross-sectional more significant" `[secondary: Alpha Architect, page blocked]` | no (cross-sectional) | not found; Cowles industry indices are monthly averages of high and low (Schwert 1990) | Not a test of the project's question |
| 6 | Baltussen, Swinkels, van Vliet 2021, JFE 142(3) "Global Factor Premiums" `[pages read]` (Robeco-hosted working paper) | 24 factors in equity indices, bonds, commodities, FX, Dec 1799 to Dec 2016; Bloomberg, Datastream, OECD, spliced with GFD, Dimson-Marsh-Staunton, JST, Siegel's website | MOP-style trend, long-short per asset class | **edge**: trend one of the strongest factors in the "new" 1800-1980 sample (Sharpe above 0.20 and t well above 3 in each asset class); factors "unrelated to market, downside, or macroeconomic risks" | no: against zero and in alpha regressions on the market | **one check**: "an additional monthly lag between signal measurement and factor strategy implementation" lowers trend's Sharpe by a "limited" amount; plus trimming and 10-year windows. Argues poor data "would be random" and bias towards the null | The lag check is the right fix for averaging and agrees with the project's own month-older check (`insure-1709-1`: S 0.67 unchanged). The "biased towards the null" argument does not hold for stale or averaged prices |
| 7 | Baltas and Kosowski 2013 (WP) and "Demystifying Time-Series Momentum Strategies" (SSRN 2140091) `[prior lane: ls-trend-1 L4, abstract]` | futures, from the 1970s-80s | TSMOM benchmarks, volatility estimators, trend t-stat signals | **edge**; explains CTA returns, no capacity limit found | no | not applicable (futures era) | Not long-history |
| 8 | Kim, Tse, Wald 2016, J. Financial Markets 30 `[abstract]`, `[secondary]` (Quantpedia; and Huang et al.'s summary) | MOP-type futures, from 1985 | MOP's rule with and without vol scaling | **neither, once unscaled**: the alpha comes mostly from volatility scaling; unscaled TSMOM and buy-and-hold have "similar cumulative returns", alphas not significantly different | **yes**: unscaled TSMOM against buy-and-hold of the same futures | not applicable | **Agrees** with "earns about what holding earns" (#74, #78) |
| 9 | Huang, Li, Wang, Zhou 2020, JFE 135 "Time-series momentum: Is it there?" `[pages read]` | MOP's 55 instruments, Jan 1985 to Dec 2015 | asset-by-asset and pooled predictive regressions; wild and pairs bootstraps; TSM against a "time series history" (TSH) rule (long if the historical mean is positive) | **little predictability**: 47 of 55 assets t < 1.65; pooled t 4.34 below bootstrap 5% critical values (12.53, 4.83); TSM and TSH "perform virtually the same", gains mainly from the long legs | **yes, in spirit**: TSH is a mean-based (holding-like) rule on the same assets; the TSM minus TSH alpha is never significant | bootstraps for size distortion; no early data | **Agrees**: the trend book's return is mostly being long assets with high means. Also agrees with the project's short-leg result (#89: shorts cut Sharpe) |
| 10 | Goyal and Jegadeesh 2018, RFS 31(5) `[prior lane: ls-trend-1 L8, abstract]` | stocks and futures | TS against cross-sectional strategies | time-series strategies carry a time-varying **net long** position; for stocks most of their lead is that net long investment | yes, via the net long split | not applicable | **Agrees** |
| 11 | Zakamulin 2014, J. Asset Management 15(4) "The real-life performance of market timing with moving average and time-series momentum rules" `[secondary]` (CXO Advisory) | S&P Composite, DJIA, long and intermediate Treasuries, 1926-2012, monthly; out of sample 1930-2012 | long-only SMA and "intrinsic momentum" (2-24 months), 0.5% one-way on stocks | **at best marginal**: 3 of 8 rule-index pairs beat buy-and-hold out of sample (S&P: SMA +10%, momentum +12% in Sharpe); stock timing underperformed buy-and-hold through 1975-1999; outperformance driven by 1930-31, 1973-74, 2001-02, 2007-08; in about 80% of exit-to-entry spells timing trailed holding | **yes**: long-only timing against holding the same index | not stated in the summary | **Agrees** closely: insurance in a few big bear markets, drag in between (`calm-drag-1`: calm-only false alarms are all of the drag) |
| 12 | Zakamulin and Giner 2022, IRFA 82 "Time series momentum in the US stock market" `[abstract]`, `[secondary]` (CXO Advisory) | S&P Composite total returns, monthly, Jan 1857 to Dec 2018; fits an AR(p) to excess returns | long-only and long-short TSMOM; analytic model | long-only beats buy-and-hold gross with about 30% higher monthly Sharpe; long-short not profitable; long-only returns "resemble a portfolio insurance strategy"; 80% power needs about 250 years | **yes**: long-only against holding the same index | **not that we could see**: before 1926 the S&P Composite monthly series is Cowles-based (monthly averages of high and low, Schwert 1990) if they used the usual splice `[not checked]`; they model short-term momentum as AR(p), the structure averaging produces | **Agrees** on "insurance", and on power. Their Sharpe gain is a risk reduction at similar return, which is the project's reading too. Their AR(p) short-term momentum on 1857-1925 is exactly where averaging bites |
| 13 | Faber 2007, updated 2013, "A Quantitative Approach to Tactical Asset Allocation" `[secondary]` (CXO Advisory; SSRN blocked) | S&P 500 1901-2012; 5 asset classes 1973-2012; monthly total returns | long-only 10-month SMA, cash at bills | S&P: 10.2% a year against 9.3%, volatility 12.0% against 17.9%, worst fall -50.3% against -83.5% (gross); 1940-2000 timing "does not widen the gap"; multi-asset gain "largely by avoiding most of the severe drawdown of 2008" | **yes** | not addressed; pre-1926 US data source not named | **Agrees**: same return, smaller worst fall, gain concentrated in big falls |
| 14 | Hutchinson and O'Brien 2014, "Is this time different? Trend following and financial crises" (UCC WP; J. Alternative Investments) `[pages read]` | 21 commodities, 13 bonds, 21 equity indices, FX from 9 rates, Jan 1921 to Jun 2013 (1940s excluded "due to concerns about data accuracy around World War II"); GFD before 1980; 6 global crises (1929, 1973, 1981, 1987, 2000, 2007) and 8 regional | long-short 12-month TSMOM, vol-scaled; 12.1% net, Sharpe 1.1 from 1925 | **weaker after crises**: in the years after a crisis starts, average returns are less than half of no-crisis returns, for about four years; markets lose their time-series predictability then | no (against no-crisis periods) | the WWII decade dropped; pre-1925 excluded for short vol histories | **Agrees** with the rebound give-back (`rev-costloss-1`, `#94`/`#96`/`#103`: "early rallies look like the bottom") |
| 15 | Hamill, Rattray, Van Hemert 2016, "Trend Following: Equity and Bond Crisis Alpha" (Man AHL) `[prior lane: ls-trend-1 L5, secondary]` | futures and forwards, 1960-2015 | long-short trend; variants with equity and bond positions restricted to be non-positive | **insurance via shorts**: best in the worst equity and bond environments; forbidding longs in equities and bonds enhanced crisis performance at a cost in average return | no | not applicable | **Agrees**: the crisis gain is the short side; long-only can only lose less |
| 16 | Harvey, Hoyle, Rattray, Sargaison, Taylor, Van Hemert 2019, JPM 45(5) "The Best of Strategies for the Worst of Times" `[pages read]` (abstract and set-up sections) | S&P 500 daily 1985-2018; 8 worst drawdowns, 3 recessions; futures strategies scaled to 10% vol | long-short futures TSMOM among other defensive strategies | **insurance with a positive mean**: time-series momentum among the most reliable crisis hedges in that window, with positive normal-time returns | no (against S&P drawdown and normal days) | not applicable | Agrees on slow falls; one 34-year window |
| 17 | Babu, Hoffman, Levine, Ooi, Schroeder, Stamelos 2020, JPM "You Can't Always Trend When You Want" `[secondary]` (AQR page, Alpha Architect summary) | 67 markets, futures data back to 1877 | HOP's strategy, decomposed into the size of market moves, conversion and diversification | the weak 2010s came mainly from small market moves, not from trend losing its ability to profit from them | no | not stated | **Agrees** with the calm drag: without big moves the insurance does not pay and the cost remains (`gap-2002-1`, `calm-drag-1`) |
| 18 | Goulding, Harvey, Mazzoleni 2023, JFE 149 "Momentum Turning Points"; 2024, FAJ 80(1) "Breaking Bad Trends" `[pages read]` (FAJ abstract, data) | multi-asset futures, 1990-2022 (FAJ) | monthly 1/12-month trend; dynamic speed after corrections and rebounds | turning points (corrections and rebounds) hurt standard trend; more breaks after 2009 explain weaker post-GFC returns | no | not applicable | **Agrees** with the late buy-back and the post-2002 cost (`gap-2002-1`, `#181`); the project already tested faster re-entry (`#94`, `#96`, `#103`, `#178`) |
| 19 | Dao, Nguyen, Deremble, Lempérière, Bouchaud, Potters 2016, J. Investment Strategies (arXiv 1607.02410) `[abstract]` | futures | single-asset trend as a long-volatility position | trend's P&L is the gap between long-term and short-term variance; it has the long-term variance exposure of a strangle portfolio | no | not applicable | **Agrees in mechanism**: insurance-like convexity, paid for in calm markets |
| 20 | Zarattini and Antonacci 2024, "A Century of Profitable Industry Trends" (SSRN/Concretum) `[secondary]` (CXO Advisory and search summaries); replication arXiv 2412.14361 `[abstract]` | 48 French-library US industries, 1926-2024 | long-only trend with channel breakouts and vol sizing across industries | **edge** claimed: 18.2% a year, Sharpe 1.39; the replication reports robustness problems in modern markets | benchmark not checked | not applicable (CRSP-based daily returns) | Disagrees on the face of it with `gap-2002-1` (10 industries 1.6-2.0 points a year behind holding since 2002), but it is a different, cross-industry, sized rule; numbers not checked |
| 21 | Kurth, Eisler, Rej, Bouchaud 2026 `[prior lane: survey-7b, tested as #181]` | futures, 1960s-2025 | trend by asset class | trend broke down after 2009 in stocks and FX, not in bonds | tested by the project against holding: the pattern shows, cause not separable from regime (#181) | not applicable | Already in the record |
| 22 | Brock, Lakonishok, LeBaron 1992; Sullivan, Timmermann, White 1999, JF 54(5) `[pages read]`; Fang, Jacobsen, Qin 2014, Rev. Financial Economics 23 `[abstract]`, `[secondary]` | DJIA daily 1897-1986 (BLL); 1897-1996 and S&P futures 1984-1996 (STW); DJIA 1987-2011 and 1885-1896 (FJQ) | moving-average and other daily rules, against cash or holding | **an in-sample edge that did not survive**: STW find the best rule significant 1897-1986 even after data snooping, but not 1987-1996 (p about 0.12) and not on S&P futures; FJQ find the 26 BLL rules dead both after 1986 and before 1897, an abrupt end that "probably" means bias | BLL/STW: against cash; FJQ: rule returns by signal | **STW, yes**: with a one-day signal delay (Ready 1997's slippage) the best mean-return rule fell from 17.2% to 7.8% a year, and the best Sharpe rule lost significance (p 0.26) | The clearest published case of a long-history "trend edge" shrinking once stale closes are lagged. Daily, not 12-month, so it says little about `tsmom12` itself |

### The stale-price and averaging literature the trend papers rely on (or skip)

| Source (read depth) | Finding | What it means for a 12-month trend rule on early data |
|---|---|---|
| Working 1960, Econometrica `[cited by Schwert, not opened]` | the change in an average of a random walk over a period has lag-1 autocorrelation of about +0.25 | any index built from monthly averages shows spurious short-lag trend; a one-period signal delay removes it |
| Schwert 1990, J. Business 63(3) (NBER WP 2985) `[pages read, OCR]` | Cowles 1871-1925 uses "the average of high and low prices in the month" (lag-1 about .25); Macaulay's railroads look averaged (.40); the monthly S&P composite after 1918 is "an average of the weekly values" and later of daily values; Smith and Cole 1802-1862 are point-sampled; his splice uses Dow Jones *end-of-month* prices for 1885-1925 and filters Cowles/Macaulay for averaging | the standard monthly US series before 1926 (Cowles, so Shiller's file) is averaged; `jst-autocorr-2` already notes that JST US is Shiller's December average (+0.01 acf); a monthly study on Shiller-type data before 1926 (#12, #13 possibly) inherits about +0.25 lag-1 acf |
| Lo and MacKinlay 1990; Boudoukh, Richardson, Whitelaw 1994 `[not opened; cited by MOP and Huang et al.]` | nonsynchronous trading makes index returns positively autocorrelated | thin early markets (few traded stocks) look trending at short lags |
| Ahn, Boudoukh, Richardson, Whitelaw 2002, RFS 15(2) `[abstract]` | 24 index futures in 15 countries: index returns positively autocorrelated, the matching futures about zero; the gap is largest at low volume | the autocorrelation trend earns on cash indices is partly not tradable; MOP cite this as their reason to use futures |
| Portnaya 2026, arXiv 2606.29591 `[abstract]` | SPY's lag-1 autocorrelation is a magnitude effect, "the fingerprint of bid-ask bounce and non-synchronous constituent staleness" | daily-horizon only; irrelevant to 12-month signals beyond confirming the mechanism today |

## Where the project's finding stands against the literature

1. **"It earns about what holding earns."** Supported by every paper that makes the same
   comparison (Kim-Tse-Wald, Huang et al., Goyal-Jegadeesh, Zakamulin, Faber, Zakamulin-Giner).
   Contradicted by none of them. The famous "century of trend" results do not contradict it
   either, because they answer a different question: a long-short, volatility-scaled book over
   dozens of markets, scored against zero. Lempérière et al. come closest (they remove the
   long-only beta of the same series) and still find a large edge, but with shorts and a
   5-month signal, on spot data with no stale-price check.
2. **"It is crash insurance: loses less in slow falls, fails in fast ones."** Agreed in shape by
   HOP, Harvey et al., Hamill et al., Zakamulin and Faber. The literature's books *gain* in
   falls because they go short; `tsmom12` cannot (B7). Nobody reports the project's exact
   statistic (share of each fall avoided against a fixed-exposure and a random-date control),
   so the 20-of-21 and 0.50-against-0.27 results have no published twin to compare numbers
   with.
3. **"It trails in calm markets and gives the gain back after the low."** Agreed by Hutchinson
   and O'Brien (weak for about four years after a crisis starts), Goulding et al. (turning
   points), Babu et al. (small moves in the 2010s), Zakamulin (trailed buy-and-hold through
   1975-1999) and Faber (no gain 1940-2000). The project's split (all calm drag from calm-only
   false alarms, `calm-drag-1`) is more detailed than anything found.
4. **"Before 1966 the timing is not separable from autocorrelation."** The literature neither
   confirms nor refutes this. It mostly does not ask: no century paper scores timing against an
   autocorrelation-matched null; one (Baltussen et al.) runs a one-month delay, which handles
   averaging but not genuine thin-market persistence; HOP and Zakamulin-Giner use or likely use
   averaged early series. Two facts point the same way as the project's caution: on daily US
   data a one-day delay halved the best rule's return (STW), and cash-index autocorrelation is
   absent in the matching futures (Ahn et al.). Two facts point the other way: MOP and HOP find
   trend in liquid futures after 1985, where staleness is small, and the effect has the same
   size as in the early data (HOP, Lempérière), which is harder to square with a pure artefact.
   Plain reading: the trend effect itself is well documented after 1960 on clean data; how much
   of its pre-1960 strength is the data's construction is unknown, in the literature and here.
5. **Power.** Zakamulin and Giner's 250 years for 80% power on one US index matches the
   project's `power-map-1`: no single-market history can settle "edge or insurance" for a
   long-only rule; only the cross-market count of falls (the project's approach) has enough
   independent episodes, and even it is limited by how correlated the falls are across
   markets.

What this survey does not show: that the literature's long-short edge is fake, or that
`tsmom12` has hidden edge. Several key sources were read only as abstracts or summaries (rows
4, 5, 8, 11, 12, 13, 17, 20); their numbers are quoted from those summaries and flagged.

## Checks the literature suggests on records the project already has (no new mechanism)

These are artefact checks on existing results, not new strategies, so no `tries.md` rows are
added. For the lead to pick from:

- **Averaging check on 1885-1925 US stocks, with data already cached.** Shiller's monthly file
  (Cowles-based before 1926, averaged; `data-long-4`) against the Dow Jones end-of-month index
  (point-sampled; MeasuringWorth, `data-long-1`), same years, same `insure-2` statistic. If the
  averaged series shows more timing than the point-sampled one, the averaging artefact is
  measured directly. Schwert's own splice (row above) is the published precedent for preferring
  the Dow Jones month-end series.
- **One-period delay on the JST annual records.** Baltussen et al.'s and STW's check, adapted:
  a signal one year older on `insure-1870-1`. A year's delay is a much bigger change on annual
  data than a month on monthly data, so a failure would be hard to read; a pass would say the
  timing does not rest on lag-1 alone. `insure-1709-1` already ran the monthly version (a month
  older: S 0.67, unchanged).
- **AQR's 1877-1912 commodity aggregate (`data-wide-2` #7).** If it is built from the CBOT
  transcriptions HOP describe (high-low averages early on; `[not checked]`), any trend result
  on it needs the one-month-delay control.

## Data sources named by the papers: keyless and not yet in `data-wide-2.md`

| Source | Named by | What | Keyless? | Note |
|---|---|---|---|---|
| Schwert's spliced US monthly returns 1802-1925 (appendix of NBER WP 2985) | Schwert 1990 | monthly index numbers; point-sampled 1802-1862 and 1885-1925 (Dow Jones month-end), Cowles/Macaulay 1863-1885 filtered for averaging | yes: `https://www.nber.org/system/files/working_papers/w2985/w2985.pdf` (www.nber.org robots.txt allows it) | scanned PDF, no text layer: needs OCR and a careful check of the digits; partly overlaps Yale ICF NYSE 1815-1925 (`data-wide-2` #3) |
| NBER Macrohistory m11025a, Cowles Commission and S&P common stock price index, 1871-1956 | Schwert 1990 (as Cowles); Baltussen et al. (JST, GFD splices) | monthly, averaged prices (the averaged twin for the check above) | the file exists keyless (`data.nber.org/databases/macrohistory/rectdata/11/m11025a.dat`), **but data.nber.org's robots.txt says `User-agent: * Disallow: /`**; a FRED mirror probably exists `[series id not checked]` | **flag for the lead:** `data-wide-2` #8 and #9 point scripts at `data.nber.org` rectdata, which that robots.txt disallows; use FRED or a manual download instead. This lane made two requests to it (robots.txt, then the file's first lines, not saved) before reading the robots file |
| Campbell, Grossman, Turner, British share market indices 1829-1929 (QUCEH WP 19-01; CEPR DP 13717) | found while checking the UK early indices | monthly UK share indices, 1829-1929 | `[not opened]`: both hosts sit behind a Cloudflare bot check | would cover 1866-1869, the gap between BoE's 1709-1866 index and the Yale IMM file (1869-1929) |
| Jeremy Siegel's website | Baltussen et al. | long US return series | `[not probed]` | |

Not new: AQR "Time Series Momentum: Factors, Monthly" (from 1985; already used by `survey-5`
and `ls-trend-1`), AQR "Commodities for the Long Run" (`data-wide-2` #7), Yale ICF (#1-#3),
JST, Shiller, French, MeasuringWorth. Paid or keyed, so excluded: GFD (used by HOP,
Lempérière, Geczy-Samonov, Hutchinson-O'Brien, Baltussen), Dimson-Marsh-Staunton, Bloomberg,
Datastream, MSCI, Commodity Systems Inc.

## Sites that blocked scripts (for the browser second pass)

- `core.ac.uk`, `papers.ssrn.com`, `www.quceh.org.uk`, `repec.cepr.org`: Cloudflare "Just a
  moment" challenge.
- `alphaarchitect.com`, `www.advisorperspectives.com`: HTTP 403 to the fetcher.
- `www.risk.net`: script wall ("a required part of this site couldn't load").
- `uia.brage.unit.no`: DNS failure; `cronfa.swan.ac.uk`: TLS error; `sites.google.com`: login
  redirect.
- `data.nber.org`: not blocked, but robots.txt disallows all agents (above).

Worth a browser pass, in order: the Zakamulin-Giner (2022) full text (data source and whether
the 1857-1925 values are averages), Greyserman-Kaminski's data chapter, Geczy-Samonov's 2017
time-series results, and the Campbell-Grossman-Turner indices.

## Files and downloads

- This file. No code, no results tables, no `tries.md` rows (no new testable mechanism).
- Cached PDFs and text under `~/data/grimstrade/survey-9/` (20 MB): HOP 2017, Lempérière 2014,
  Huang et al. 2020, Hutchinson-O'Brien 2014, Schwert 1990 (with OCR), Harvey et al. 2019,
  Goulding et al. 2024, Sullivan-Timmermann-White 1999, MOP 2012, Baltussen et al. (working
  paper), Geczy-Samonov deck.
