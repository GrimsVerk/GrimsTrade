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

- Sample: 58 liquid futures and forwards (24 commodities, 9 developed equity indexes, 13 developed government bonds, 9 currency forwards per the paper's data section; also 12 cross-currency pairs). Main evaluation January 1985 to December 2009; data back to 1965.
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

