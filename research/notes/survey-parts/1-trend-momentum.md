# Part 1: Trend and momentum

Survey date: 2026-11-12. Scope: trend and momentum in traditional assets (crypto trend is covered
elsewhere), judged for a long-only, unlevered, daily-bar book in BTC, ETH, SPY, QQQ, GLD, TLT with
next-open fills and costs of about 60 bps per crypto round trip and about 4 bps per ETF round trip.

How to read the entries:

- `[opened: full text]` means I read the paper itself (PDF text extracted and searched; for long papers I read the abstract, method and results sections, not every page).
- `[opened: abstract page]` means I read only the abstract or landing page; numbers are limited to what that page shows.
- `[opened: secondary summary]` means I read a third-party summary, not the paper.
- `[not opened]` means the entry rests on a search snippet or on another paper's description; treat as unverified.
- `[from memory, unverified]` marks anything I state from prior knowledge without having opened a source in this session.
- "Implication" lines are my inference for this setup, not claims made by the authors.

A recurring point: most of this literature studies LONG-SHORT, VOLATILITY-SCALED, LEVERED futures
portfolios across 50+ markets. Our book is long-only, unlevered and has six assets. Long-only trend
on a single asset is a "long or cash" switch, which keeps only part of the effect.

---

## A. Time-series momentum: the core papers and the critiques

### A1. Moskowitz, Ooi, Pedersen, "Time series momentum" `[opened: full text]`
Moskowitz, T.J., Ooi, Y.H., Pedersen, L.H. (2012). Journal of Financial Economics 104(2), 228-250. DOI 10.1016/j.jfineco.2011.11.003.
URL: https://pages.stern.nyu.edu/~lpederse/papers/TimeSeriesMomentum.pdf

- Sample: 58 liquid futures and forwards across equity indexes, currencies, commodities and government bonds (per the abstract; a search summary gives 24 commodities, 9 equity indexes, 13 bonds and 12 cross-currency pairs, which I did not check against the data table). Main evaluation January 1985 to December 2009; data back to 1965.
- Claim: "the past 12-month excess return of each instrument is a positive predictor of its future return." The effect "persists for about a year and then partially reverses over longer horizons." All 58 contracts show positive 12-month TSMOM returns and 52 are significant at 5%.
- Construction: TSMOM = sign of the past 12-month excess return, 1-month hold, each position scaled to 40% ex-ante annual volatility; the equal-weighted portfolio has about 12% annual volatility. This is long-short and implicitly levered.
- Key numbers: diversified portfolio Sharpe "greater than one", "roughly 2.5 times the Sharpe ratio for the equity market portfolio". Alpha about 1.58% per month (t = 7.99) against MSCI World and Fama-French SMB, HML, UMD; loads positively on UMD (cross-sectional momentum). Regressing each instrument's TSMOM on a constant long position gives positive alpha in 90% of cases, 26% significant.
- Extreme markets: coefficient on squared MSCI World return is 1.99 (t = 3.88): payoffs "similar to an option straddle on the market." Large gains in Q4 2008, "sharp losses when the crisis ends in March, April, and May of 2009."
- Costs / out-of-sample: returns are gross; no cost deduction in the main results. An out-of-sample check on 1966-1985 (asked for by the referee) gives "an annualized Sharpe ratio of 1.1".
- Implication (my inference): the evidence is strongest for the diversified long-short portfolio. For us the relevant fact is narrower: 12-month own-return sign has been a positive predictor for equity indexes, bonds and gold-like commodities. A long-or-cash version keeps the "avoid the down-trend" half, not the short-side gains that made Q4 2008 so profitable.

### A2. Hurst, Ooi, Pedersen, "A Century of Evidence on Trend-Following Investing" `[opened: full text]`
Hurst, B., Ooi, Y.H., Pedersen, L.H. (2017). Journal of Portfolio Management 44(1), Fall 2017. AQR.
URL: https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing (PDF: https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/AQR-JPM-Fall-2017.pdf)

- Sample: 67 markets (equity indexes, bond markets, commodities, currency pairs), January 1880 to December 2016, using hand-collected and spliced data before futures existed.
- Construction: equal-weighted blend of 1-, 3- and 12-month TSMOM signals, long or short every market, each position vol-scaled, portfolio targeted at 10% annual volatility, monthly rebalancing.
- Costs: transaction costs from current estimates by asset class, scaled up for history using Jones (2002); fees simulated as 2% management plus 20% performance with a high-water mark. The authors note costs "are estimated with a significant amount of uncertainty." The headline exhibit's numbers are in an image I could not extract, so I do not quote the return or Sharpe figures.
- Claims I could read: positive returns in every decade; average single-market Sharpe "approximately 0.4" (gross); each of the 1-, 3- and 12-month signals positive in each decade; the text states it had positive returns "on average, in major bear markets" (the 10 largest 60/40 drawdowns, which averaged about 15 months peak to trough); a 20% allocation from a 60/40 portfolio "reduced the maximum portfolio drawdown, lowered portfolio volatility, and increased portfolio returns"; worst drawdowns up to 25%. It "may not perform well in bear markets that occur very rapidly, such as the 1987 stock market crash."
- Post-2008: average cross-market correlations "increased meaningfully from late 2008 until the middle of 2014" ("risk-on/risk-off"), and high correlations are associated with low subsequent returns ("there are fewer truly different trends to bet on").
- Implication (my inference): the century evidence is a long-short, vol-targeted, many-market result. It supports trend as a real phenomenon but says little about a six-asset long-only book. The correlation finding matters for us: our six assets often move as one risk-on/risk-off block, which is exactly the regime where AQR reports weak trend returns.

### A3. Huang, Li, Wang, Zhou, "Time series momentum: Is it there?" `[opened: abstract page]`
Huang, D., Li, J., Wang, L., Zhou, G. (2020). Journal of Financial Economics 135(3), 774-794. DOI 10.1016/j.jfineco.2019.08.004.
URL: https://econpapers.repec.org/RePEc:eee:jfinec:v:135:y:2020:i:3:p:774-794 (full text at core.ac.uk and SMU repository returned 403 / empty)

- Sample: the Moskowitz-Ooi-Pedersen universe of 55 futures (per search summary; dates not verified).
- Claim (abstract): "asset-by-asset time series regressions reveal little evidence of TSM, both in- and out-of-sample." The pooled-regression t-statistic "is not statistically reliable as it is less than the critical values of parametric and nonparametric bootstraps." The TSM strategy "is profitable, but its performance is virtually the same as that of a similar strategy that is based on historical sample mean and does not require predictability."
- Mechanism (search summary, not verified in the paper): pooled regression without fixed effects biases the slope upward.
- Implication (my inference): much of TSMOM profit may be "be long the assets that have had positive average returns", not timing. For us that means a trend filter on SPY/QQQ/GLD/TLT must be judged against buy-and-hold of the same asset, not against zero. If it only matches buy-and-hold with more trades, it fails.

### A4. Kim, Tse, Wald, "Time series momentum and volatility scaling" `[opened: abstract page]` plus `[opened: secondary summary]`
Kim, A.Y., Tse, Y., Wald, J.K. (2016). Journal of Financial Markets 30, 103-124. DOI 10.1016/j.finmar.2016.05.003.
URL: https://econpapers.repec.org/RePEc:eee:finmar:v:30:y:2016:i:c:p:103-124 (summary: https://quantpedia.com/deconstructing-the-time-series-momentum-strategy/)

- Sample: 55 futures contracts, 1985-2013, including a replication of the 1985-2009 Moskowitz-Ooi-Pedersen period (per the Quantpedia summary).
- Claim (abstract): MOP's results "are largely driven by volatility-scaling returns (or the so-called risk parity approach to asset allocation) rather than by time series momentum." "Without scaling by volatility, time series momentum and a buy-and-hold strategy offer similar cumulative returns and their alphas are not significantly different."
- Numbers (secondary summary, not checked against the paper): monthly alpha 1.27% with volatility scaling versus 0.41% without; TSMOM beats buy-and-hold in 29 of 55 contracts unscaled, 31 of 55 scaled; outperformance concentrated before 2001; for 2009-2013 "the performance of TSMOM is worse than that of a buy-and-hold strategy."
- Costs: none mentioned in the summary.
- Implication (my inference): this is the most directly relevant critique for us. Our book cannot lever low-volatility assets (TLT, GLD) up to equal risk, so the volatility-scaling part of the "trend" return is largely out of reach. What remains, unscaled sign-of-past-return timing, looked roughly like buy-and-hold in their sample.

### A5. Goyal & Jegadeesh, "Cross-Sectional and Time-Series Tests of Return Predictability: What Is the Difference?" `[opened: abstract page]`
Goyal, A., Jegadeesh, N. (2018). Review of Financial Studies 31(5), 1784-1824. DOI 10.1093/rfs/hhx131.
URL: https://ideas.repec.org/a/oup/rfinst/v31y2018i5p1784-1824..html

- Sample: individual stocks and multiple international asset classes (dates not on the abstract page).
- Claim (abstract): CS strategies are zero-net-investment; "TS strategies take on a time-varying net long investment in risky assets." For individual stocks, the TS versus CS performance gap "is largely due to this time-varying net long investment." Across asset classes, "scaled CS strategies significantly outperform similarly scaled TS strategies."
- Costs / out-of-sample: not stated on the abstract page.
- Implication (my inference): part of what looks like TS momentum skill is simply being net long risky assets most of the time while they rose. For a long-only book this is the same warning as A3: the benchmark is buy-and-hold, and a trend filter's value is mainly in what it avoids (deep, slow bear markets), not in extra return.

---

## B. Simple long-only trend filters on a handful of asset classes

### B1. Faber, "A Quantitative Approach to Tactical Asset Allocation" `[opened: secondary summary]` (two summaries; SSRN page returned 403)
Faber, M.T. (2007). Journal of Wealth Management 9(4), Spring 2007 [from memory, unverified]; updated February 2013 as SSRN 962461. A ten-year retrospective appeared in the Journal of Portfolio Management in 2018 (per search snippet, not opened).
URL: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461 (not readable). Summaries read: https://www.cxoadvisory.com/technical-trading/long-term-outperformance-from-trends-defined-by-moving-averages (CXO, Aug 2013) and https://canadiancouchpotato.com/2013/12/30/the-failed-promise-of-market-timing/ (Dec 2013).

- Rule: hold each asset if its month-end price is above its 10-month simple moving average, else cash (T-bills); five equal-weighted asset classes (S&P 500, 10-year Treasuries, MSCI EAFE, GSCI, NAREIT); signals checked monthly; about 3-4 round trips per year for the five-asset model (CXO).
- In-sample (as reported by CXO, gross): S&P 500 alone 1901-2012, 10.2% versus 9.3% annualized, volatility 12.0% versus 17.9%, Sharpe 0.55 versus 0.32, worst drawdown -50.3% versus -83.5%. Five-asset portfolio 1973-2012: 10.5% versus 9.9%, volatility 7.0% versus 10.3%, Sharpe 0.73 versus 0.44, worst drawdown -9.5% versus -46.0%. Couch Potato gives the same five-asset numbers (10.48% versus 9.92%) and notes one losing year, -0.59% in 2008.
- Post-publication (2009-2012, from the paper's own 2013 table as quoted by Couch Potato): GTAA 12.77%, 3.65%, 2.49%, 1.26% versus buy-and-hold 18.74%, 14.04%, 2.81%, 11.57%. Annualized 4.95% versus 11.64%. Timing trailed buy-and-hold in five straight years through 2013. The live Cambria Global Tactical ETF (a different, 50-100 ETF implementation) returned 0.42% annualized over three years to December 2013 versus about 6.3-6.8% for buy-and-hold proxies.
- CXO caveats: results "gross of trading frictions", index data not tradable funds, possible data snooping in the 10-month window (though 3- to 12-month windows also beat buy-and-hold on Sharpe), outperformance "depended substantially on avoiding the 2008 crash", and for the S&P 500 the rule did not add to its edge over 1940-2000.
- 2018 retrospective `[not opened]`: a search snippet says the timing system beat stocks in 2008-2009 but trailed in six of the following eight years. Not verified.
- Implication (my inference): the 10-month SMA is a drawdown-reduction rule, not a return enhancer. Out of sample it delivered the drawdown cut in 2008 and then lagged badly in the 2009-2013 recovery. With our costs (4 bps ETF round trip) and 3-4 round trips a year the friction is trivial for SPY/QQQ/GLD/TLT. Judge it on maximum drawdown and Sharpe, and expect long stretches of lagging buy-and-hold.

### B2. Antonacci, dual momentum and Global Equity Momentum (GEM) `[opened: secondary summary]` (practitioner replication article; Antonacci's paper not opened)
Antonacci, G. (2012-2013). "Risk Premia Harvesting Through Dual Momentum", SSRN working paper; later a journal version (2017, per search snippet) and the book "Dual Momentum Investing" (2014) [from memory, unverified]. Replication read: ReSolve Asset Management, "Global Equity Momentum: A Craftsman's Perspective" (2019), reposted at https://hedgefundalpha.com/strategies/global-equity-momentum-a-craftsmans-perspective/ .

- Rules (per the ReSolve article): each month, if US stocks' 12-month return is above T-bills (absolute or time-series momentum), hold whichever of US or foreign stocks has the higher 12-month return (relative momentum); otherwise hold bonds. Original data 1974-2011, monthly (search snippets of the 2012 paper say data run January 1974 to December 2011).
- Claim (search snippets of the paper, not opened): combining absolute and relative momentum beats either alone; relative momentum adds return, absolute momentum "does far more to lessen volatility and drawdown." Reported returns are gross.
- Out-of-sample (ReSolve): extended back to 1950 and forward to 2018 and say GEM "has produced attractive absolute and risk-adjusted performance since 1950, both in- and out-of-sample." The page I read gives no CAGR, Sharpe or drawdown numbers.
- Parameter risk (ReSolve): they tested 18 x 18 = 324 lookback combinations of 1-18 months. A search snippet of the full report says the 12-month original looks like "random luck" relative to the alternatives and that the choice carries uncompensated specification risk; Newfound Research (snippet, not opened) reports lookback choice moving results by "hundreds, if not thousands, of basis points a year." Not verified from the full report.
- No live post-publication track record found in what I read.
- Implication (my inference): GEM is a three-asset monthly switch, very close to what our universe allows (SPY or QQQ versus TLT, with a T-bill gate). The absolute-momentum leg is just a 12-month trend filter; the relative leg with two or three assets is a coin-flip on which lookback you pick. Use an ensemble of lookbacks rather than the single 12-month number.

### B3. Zakamulin, "The real-life performance of market timing with moving average and time-series momentum rules" `[opened: abstract page]`
Zakamulin, V. (2014). Journal of Asset Management 15, 261-278 [volume/pages from memory, unverified]. DOI 10.1057/jam.2014.25.
URL: https://fitforthem.unipa.it/rep:6533b858fe1ef96bd12b5798

- Claim (abstract, paraphrased by the page): "the reported performance of market timing strategies usually contains a considerable data-mining bias" and ignores frictions; out-of-sample tests with realistic transaction costs show performance is "highly overstated."
- No numbers on the page I read.
- Implication (my inference): pick the moving-average length from the literature before looking at our data, and report results net of costs and against buy-and-hold.

### B4. Zakamulin, "Market Timing with Moving Averages: Anatomy and Performance of Trading Rules" `[opened: secondary summary]` (CXO Advisory)
Zakamulin, V. (working paper 2014, revised 2016; later the book "Market Timing with Moving Averages", Palgrave 2017 [from memory, unverified]).
URL: https://www.cxoadvisory.com/technical-trading/market-timing-with-moving-averages-over-the-very-long-run

- Sample: monthly S&P Composite and T-bill returns, January 1860 to December 2009. Six moving-average-type rules, re-optimized on rolling 20-year windows and tested out of sample. One-way cost 0.25%.
- Results (CXO, no exact return or Sharpe figures given): rules sat in cash "about a third of the time"; mean returns were lower than buy-and-hold but Sharpe ratios generally higher; simple momentum (sign of the past N-month return) was the best out-of-sample rule. Average (median) optimal lookback: 7 (5) months for momentum, 10 (11) for the SMA. Over 5- and 10-year horizons timing was about equally likely to beat or trail buy-and-hold.
- A companion summary (search snippet of an Alpha Architect page that returned 403) says there was no statistically significant outperformance in the second half of the sample. Not verified.
- Implication (my inference): the best case for long-or-cash trend on an equity index is "similar or lower return, lower risk, coin-flip relative performance over a decade." That is a risk-management tool with real costs of opportunity, not alpha.

---

## C. Post-2009 trend-following performance and explanations

### C1. Babu, Levine, Ooi, Schroeder, Stamelos, "You Can't Always Trend When You Want" `[opened: full text]`
Babu, A., Levine, A., Ooi, Y.H., Schroeder, S., Stamelos, E. (2020). Journal of Portfolio Management 46(4), March 2020. AQR.
URL: https://www.aqr.com/Insights/Research/Journal-Article/You-Cant-Always-Trend-When-You-Want (PDF: https://www.aqr.com/-/media/AQR/Documents/Journal-Articles/JPM-You-Cant-Always-Trend-When-You-Want.pdf)

- Sample: the Hurst-Ooi-Pedersen 67 markets (29 commodities, 11 equity indexes, 15 bond markets, 12 currency pairs), 1880-2018; recent period 2010-2018. Same 1/3/12-month TSMOM, 10% volatility target, net of estimated transaction costs, gross of fees.
- Live evidence quoted: SG Trend Index peaked 13 April 2015 and returned -19.7% from then to 31 December 2018. From 1 January 2010 to 31 December 2018 its annualized Sharpe was 0.05, versus 0.28 from its January 2000 inception to December 2018.
- Claim: the weak decade is "primarily due to muted moves across global markets", not lower "trend efficacy" (the slope from market move size to trend profit) and not lower diversification. "When large market moves occurred in the recent decade, trend following was able to benefit, as in 2014." Near-zero cash rates also cut total returns.
- Caveat: the authors run a large trend business; the decomposition is model-based and explains the past decade rather than predicting the next one.
- Implication (my inference): trend profits depend on large sustained moves. A long-only filter is hurt twice in a choppy decade: whipsaw costs plus missed rebounds. The useful part for us is that large moves in single assets (2008 equities, 2022 bonds) were still captured.

### C2. Man Group, "Gaining Momentum: Where Next for Trend-Following?" `[opened: full text]` (practitioner article)
Man Group (9 June 2022). Man Institute article, data to 31 May 2022.
URL: https://www.man.com/insights/gaining-momentum-trend

- Numbers (text): SG Trend Index +26% and Barclay BTOP50 +16% year-to-end-May 2022, both "best year-to-end-May returns since 2000"; Barclays Global Aggregate (USD hedged) -7.7% over the same period.
- Claim: in past crises trend made money on bonds through LONG bond positions; in 2022 the positive bond attribution came from SHORT bonds. The author calls 2022 "the first 'real world' opportunity" to test their bond crisis-alpha research. Simulations back to 1926 (chart only) are said to show trend doing well in inflationary periods.
- No analysis of long-only trend.
- Implication (my inference): the 2022 trend win came from being short bonds and long commodities. A long-only book in SPY/QQQ/TLT gets none of the short-side gain; at best it steps into cash. The long-or-cash version would have protected capital in 2022 but not profited.

### C3. Man Group, "Trend-Following: 2022 Review" `[opened: full text]` (practitioner discussion transcript)
Man Group (late 2022). Man Institute.
URL: https://www.man.com/insights/trend-following-2022-review

- Numbers (approximate, as spoken): world equities down "near 20%" and bonds down "a bit over 10%" in the first nine months of 2022. SG Trend and BTOP50 positive (exact figures only in a chart).
- Sector attribution for a roughly 80-market program: bond shorts and FX (mainly the US dollar trend from Q2) very profitable; commodities good in H1 and partly given back after July; equities the "least profitable" sector because of sharp bear-market rallies.
- Speed: faster trend signals "help for that crisis alpha feature" and were more defensive in equity sell-offs; no numbers given.
- Stock-bond correlation turned positive because inflation acted as "a common risk factor."
- Implication (my inference): in our universe the 2022 equity trend was choppy (several sharp rallies), so a long-or-cash filter on SPY/QQQ likely whipsawed several times. The cleaner long-only trend in 2022 was TLT staying below its trend all year (stay in cash) and the US dollar, which we do not hold.

### C4. Hamill, Rattray, Van Hemert, "Trend Following: Equity and Bond Crisis Alpha" `[opened: abstract page]` (Man Group overview page; full PDF not opened)
Hamill, C., Rattray, S., Van Hemert, O. (2016). Man Group / Oxford-Man working paper, September 2016 (SSRN, per search snippet).
URL: https://www.man.com/insights/trend-following-equity-and-bond-crisis-alpha (full paper link on that page: https://www.man.com/documents/download/CDWr8-fphNP-AYg1X-K2TYR, not opened)

- Sample: TSMOM in bonds, commodities, currencies and equity indexes, 1960-2015, monthly; pre-futures history proxied by cash returns financed at the short rate.
- Claims (overview): performance "consistently" good both before 1985 (bond bear market) and after (bond bull market), so not just a product of the 30-year bond rally. Returns positively skewed, more so for shorter-term strategies. Best in the worst equity AND worst bond environments ("equity smile" and a more pronounced "bond smile").
- Restriction test: barring LONG positions in equities or bonds improved crisis performance but cut average returns and weakened protection in the other asset class.
- No numbers on the overview page; costs not described there.
- Implication (my inference): the crisis protection of trend comes mostly from the ability to be short. Our long-only filter can only exit, so its crisis value is "not losing", and it gives up the convexity that made trend a hedge.

### C5. Man AHL, "The Need for Speed in Trend-Following Strategies" `[opened: full text]` (practitioner article; tables are in charts I could not read)
Man Group (January 2023). Man Institute.
URL: https://www.man.com/insights/need-for-speed-trend-following

- Sample: 50 most liquid futures and FX forwards, 1995-2022; equal risk across equity, fixed income, FX, commodities; five speeds of double exponentially weighted moving-average crossovers; each scaled to 10% volatility. Correlation between fastest and slowest speed: 0.17.
- Claims: Sharpe ratios "all significantly positive" and risk-adjusted returns "increase with slower speed"; after costs, faster speeds are "materially lower over the long-term." Skewness and crisis performance (worst S&P 500 quintile) are better for fast speeds; "The slowest trend speed cannot shift to a short position over a one- or three-month horizon." Costs are modelled for a USD 5bn book with Man's own execution; no bps figures in the text.
- Implication (my inference): there is a real trade-off. Slow signals (6-12 months) earn more over time; fast signals (weeks) protect better in sudden crashes but pay more costs and whipsaw. For crypto at 60 bps a round trip only slow signals are affordable; for ETFs at 4 bps a blend of speeds is affordable.

---

## D. Cross-sectional momentum across asset classes

### D1. Asness, Moskowitz, Pedersen, "Value and Momentum Everywhere" `[opened: full text]`
Asness, C.S., Moskowitz, T.J., Pedersen, L.H. (2013). Journal of Finance 68(3), 929-985. DOI 10.1111/jofi.12021.
URL: https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf

- Sample: eight markets: individual stocks in the US, UK, Europe, Japan, plus country equity index futures (from January 1978), currencies (from January 1979), government bonds (from January 1982), commodities (from January 1972); all to July 2011. Momentum = past 12-month return skipping the most recent month; tercile portfolios P1 (losers) to P3 (winners) and long-short P3-P1.
- Key numbers (Table I, Panel B, gross, long-short P3-P1 momentum): country indexes mean 8.7% a year, Sharpe 0.73 (t = 4.14); currencies 3.5%, Sharpe 0.34 (t = 1.90); FIXED INCOME 0.4%, Sharpe 0.06 (t = 0.35); commodities 12.4%, Sharpe 0.53 (t = 3.29); global non-stock asset classes 4.6%, Sharpe 0.63. Value and momentum are negatively correlated (about -0.60 on average for stock strategies); a 50/50 combination has Sharpe 1.42-1.59 across all asset classes.
- Long-only angle: the winner tercile P3 for country indexes had Sharpe 0.65 versus 0.14 for the loser tercile P1; for bonds P3 0.61 versus P1 0.64 (no spread).
- Costs: results gross; no transaction cost deduction in the table.
- Implication (my inference): cross-asset momentum worked in equity indexes and commodities, not in government bonds. For us, ranking SPY/QQQ/GLD/TLT/BTC/ETH by 12-1 month return is a cross-asset-class rank, not a within-class rank as in AMP, and it would mostly measure which asset class had the best year. AMP gives no evidence that this is profitable with six assets.

### D2. Daniel & Moskowitz, "Momentum Crashes" `[opened: abstract page]`
Daniel, K., Moskowitz, T.J. (2016). Journal of Financial Economics 122(2), 221-247. NBER WP 20439 (2014). DOI 10.1016/j.jfineco.2015.12.002.
URL: https://www.nber.org/papers/w20439

- Claim (abstract, as summarized by the page): momentum earns strong average returns across asset classes but has "infrequent, persistent" crashes. Crashes are partly forecastable: they occur in "panic" states, after market declines and in high volatility, coinciding with market rebounds, when past losers (high beta) jump. A dynamic strategy forecasting momentum's mean and variance "roughly doubles" the alpha and Sharpe of static momentum. Holds across periods, international equities and other asset classes.
- Costs / numbers: not on the abstract page. The famous examples (1932, 2009) I recall from the paper are `[from memory, unverified]`.
- Implication (my inference): crashes are a long-short problem (the short leg of past losers rallies). For a long-only rank-and-hold-winners rule, the analogous risk is a sharp rotation after a bear market bottom, when we sit in the defensive winner (TLT or cash) while equities rebound. This is the same "missed rebound" cost seen in Faber's 2009 record (B1).

### D3. Jegadeesh & Titman, "Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency" `[opened: abstract page]`
Jegadeesh, N., Titman, S. (1993). Journal of Finance 48(1), 65-91.
URL: https://ideas.repec.org/a/bla/jfinan/v48y1993i1p65-91.html

- Sample: US individual stocks (the 1965-1989 sample period is `[from memory, unverified]`; not on the abstract page).
- Claim (abstract): buying past winners and selling past losers generates "significant positive returns over three- to twelve-month holding periods"; not explained by systematic risk; part of the first-year abnormal return dissipates over the following two years.
- Costs: not on the abstract page.
- Implication (my inference): the founding result is about ranking hundreds of stocks within one asset class. It does not carry over to ranking six assets from four different classes.

### D4. Is cross-sectional ranking meaningful with six assets? (my inference, no single source)
- Every result above (D1-D3) sorts many assets into terciles or deciles within an asset class and holds a long-short spread. With six assets, "top 2 by 12-month return" is a concentrated asset-class bet whose result depends on a handful of regime switches per decade.
- AMP (D1) found no momentum in government bonds (Sharpe 0.06) and Goyal-Jegadeesh (A5) found that scaling matters when assets have "heterogeneous return distributions." BTC/ETH are several times as volatile as SPY and far more volatile than TLT (my rough estimate, not from a source); a raw return rank will pick crypto whenever crypto trends, so the "rotation" becomes mostly a crypto-or-not switch. Ranking on volatility-adjusted returns reduces that, but adds a parameter.
- The CXO test in E1 is the closest evidence: an eight-ETF universe gave only about 30 independent ranking periods in 12 years. Statistical power with six assets will be low.

---

## E. Trend and momentum in small ETF universes, after costs and whipsaw

### E1. CXO Advisory, "Simple Asset Class ETF Maximum Momentum Strategy" `[opened: full text]` (practitioner backtest, not peer reviewed)
CXO Advisory (about 2015).
URL: https://www.cxoadvisory.com/momentum-investing/simple-asset-class-etf-maximum-momentum-strategy/

- Universe: DBC, EEM, EFA, GLD, IWB, IWM, RWR, TLT plus 3-month T-bills; July 2002 to December 2014 (150 months), monthly rebalancing at month-end close, all-in on the single top asset.
- Results (gross): baseline "5-1" (top past-5-month return): 1.51% average monthly return, 5.50% monthly standard deviation, maximum drawdown -24%, 58 switches. A variant measured from the 105-day low: 1.63%, 5.70%, -40%, 55 switches. No buy-and-hold benchmark numbers in the text.
- Caveats stated: frictions and taxes ignored; about 30 independent five-month ranking intervals; only one full equity bear market; the difference between variants "not compelling."
- Implication (my inference): monthly top-1 rotation trades about 5 times a year, so at 4 bps per ETF round trip costs are negligible. The binding problem is sample size and parameter choice, not costs.

### E2. Fang, Jacobsen, Qin, "Predictability of the simple technical trading rules: An out-of-sample test" `[opened: abstract page]`
Fang, J., Jacobsen, B., Qin, Y. (2014). Review of Financial Economics 23(1), 30-45. DOI 10.1016/j.rfe.2013.05.004.
URL: https://ideas.repec.org/a/eee/revfin/v23y2014i1p30-45.html

- Sample: the moving-average and trading-range rules that Brock, Lakonishok and LeBaron (1992) found best on the Dow Jones (1897-1986), re-tested on fresh data 1987-2011 (and, per a search snippet, also on 1885-1896).
- Claim (abstract): "In a true out-of-sample test based on fresh data we find no evidence" of predictive power; the poor out-of-sample performance "most likely is not due to the market becoming more efficient" but to biases in the original testing.
- Costs: gross returns per search snippet; not verified.
- Implication (my inference): short-horizon daily moving-average crossovers on an equity index (Brock et al. used daily rules such as price versus 50-, 150- and 200-day averages, `[from memory, unverified]`) did not survive out of sample. Slow monthly-checked trend filters (B1, B4) are a different and better-supported object; do not confuse them with daily crossover trading.

---

## Verdict for this family

**Held up out of sample.** (1) Trend exists as a broad phenomenon: diversified long-short futures trend was positive in every decade since 1880 and in the 1966-1985 holdout (A1, A2), and did what it promised in the slow bear markets of 2008 and 2022 (C2, C3). (2) Slow, monthly-checked long-or-cash filters on equity indexes reduce volatility and maximum drawdown versus buy-and-hold, including out of sample in 2008 (B1, B4). (3) Slow signals beat fast ones after costs; fast ones only buy better crash protection (C5).

**Failed or weak.** (1) Trend as a return enhancer for a single asset: without volatility scaling, time-series momentum is about the same as buy-and-hold (A4), and much of its profit is "be long assets with positive average returns" (A3, A5). (2) Post-publication records: Faber's model returned 4.95% a year versus 11.64% for buy-and-hold over 2009-2012 (B1); the SG Trend Index had a Sharpe of 0.05 over 2010-2018 (C1). (3) Daily technical crossover rules on equity indexes failed on fresh data (E2), and optimized timing rules overstate performance (B3). (4) Cross-sectional momentum in government bonds was nil even in-sample (D1); dual-momentum lookback choice looks like luck (B2).

**Biggest caveats for our setup.**
- The headline literature is long-short, volatility-scaled and levered across 50-67 markets. Our book can neither short nor lever TLT and GLD up to equal risk, so the two biggest sources of the published returns (crisis shorts and volatility scaling) are out of reach (A4, C4).
- Six assets that often move together give few independent trends; AQR links high cross-market correlation to weak trend returns (A2).
- The cost of a long-or-cash filter is missed rebounds after bottoms (2009 in B1) and no protection in sudden crashes such as 1987 (A2), which can mean years behind buy-and-hold.
- Next-open fills barely matter for monthly signals, but checking a 200-day rule every day instead of at month-end will add whipsaw; test both.
- Judge every rule against same-asset buy-and-hold on Sharpe and maximum drawdown, not against zero.

**Testable ideas for our universe.**
1. Faber filter: each month-end, hold each of SPY, QQQ, GLD, TLT at equal weight if its close is above its 10-month (about 210-day) simple moving average, else cash; compare with equal-weight buy-and-hold on Sharpe and maximum drawdown.
2. Ensemble time-series momentum: for each asset, weight = share of the 1-, 3-, 6- and 12-month past returns that are positive (0, 0.25, ..., 1), rebalanced monthly, long-only, sum of weights at most 1.
3. Separate scaling from timing: run unlevered inverse-volatility weights (60-day volatility) across the four ETFs with and without idea 2's trend weight, to see whether any gain is timing or just risk balancing (A4).
4. GEM-style switch: hold SPY when its 12-month return is positive, otherwise TLT (or cash when TLT's 12-month return is also negative), averaged over 3-, 6-, 9- and 12-month lookbacks to avoid picking a lucky one.
5. Null check for cross-sectional ranking: monthly hold the top 2 of the 6 assets by 12-1 month volatility-adjusted return versus equal weight; expect no edge and treat a large edge as overfitting.
6. Whipsaw cost: the same 200-day SMA rule on SPY evaluated daily versus only at month-end, net of 4 bps per round trip, over 2000-2009, 2010-2019 and 2020-now separately.

**Source count.** 21 sources opened: 4 papers as full text (A1, A2, C1, D1), 4 practitioner articles read in full (C2, C3, C5, E1), 8 abstract or landing pages (A3, A4, A5, B3, C4, D2, D3, E2), and 5 secondary summaries (Quantpedia for A4; CXO and Canadian Couch Potato for B1; the ReSolve repost for B2; CXO for B4). Items tagged `[from memory, unverified]` or `[not opened]` are marked inline.
