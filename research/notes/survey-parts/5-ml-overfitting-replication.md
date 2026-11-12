# Part 5: Backtest overfitting, replication, machine learning

Survey date: 2026-11-12. Scope: what the literature says for a long-only, unlevered, daily-bar
book in BTC, ETH, SPY, QQQ, GLD, TLT with next-open fills and costs of about 60 bps per crypto
round trip and about 4 bps per ETF round trip. This part covers (A) backtest overfitting and the
replication record of published strategies, and (B) machine learning and deep learning for return
prediction on a handful of daily series.

How to read the entries:

- `[opened: full text]` means I read the paper itself (PDF text), at least the sections cited.
- `[opened: abstract page]` means I read only the abstract or landing page; numbers are limited to what that page shows.
- `[opened: secondary summary]` means I read a third-party summary, not the paper.
- `[not opened]` means the entry rests on a search snippet or on another paper's description; treat as unverified.
- `[from memory, unverified]` marks anything I state from prior knowledge without checking it in this session.
- "Implication" lines are my inference for this setup, not claims made by the authors.

---

## A1. Multiple testing and backtest overfitting

### 1. Harvey, Liu & Zhu, "... and the Cross-Section of Expected Returns" `[opened: abstract page]`
Harvey, C. R., Liu, Y., Zhu, H. (2014). NBER Working Paper 20592; published in Review of Financial Studies 29(1), 2016, 5-68.
URL: https://www.nber.org/papers/w20592

- Sample: the published factor literature from the first empirical tests in 1967 onward ("hundreds of papers and hundreds of factors", per the page). The SSRN page (abstract_id 2249314) was not opened.
- Claim: with that much data mining, the usual t > 2.0 cutoff is no longer adequate. Their multiple-testing framework, which allows for correlated tests and unpublished tests, gives a rising historical series of cutoffs. A newly discovered factor should clear a t-ratio above 3.0. "Most claimed research findings in financial economics are likely false."
- Costs / out of sample: not a trading study; the point is statistical significance after accounting for the number of tests.
- Implication (my inference): a t-stat of 2 on our own backtest means little if we tried more than a few variants. Our bar for "real" should be at least t > 3 on the full sample, and higher if the count of tries in `ledger/tries.jsonl` is large. With 6 assets and daily data since about 2004 (ETFs) or 2015 (ETH), a t of 3 needs a Sharpe of roughly 3 / sqrt(years), so about 0.7 over 20 years or 1.3 over 5 years (my arithmetic, assuming t is about Sharpe times sqrt(years)).

### 2. Bailey & Lopez de Prado, "The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting and Non-Normality" `[opened: full text]`
Bailey, D. H., Lopez de Prado, M. (2014). Journal of Portfolio Management 40(5), 94-107 (the PDF says "Forthcoming, 2014"; volume and pages are from memory, unverified).
URL: https://www.davidhbailey.com/dhbpapers/deflated-sharpe.pdf

- Method: the expected maximum Sharpe ratio across N independent trials grows with N and with the variance of the trial Sharpes. The DSR is the probability that the true Sharpe is above zero once the observed Sharpe is measured against that expected maximum instead of against zero, with a correction for skewness, kurtosis and sample length T. Appendix A.3 explains how to estimate the number of effectively independent trials when M correlated trials were run.
- Worked example: a Treasury auction-cycle seasonality strategy. Many configurations give an annualized Sharpe of 2 and the best gives 2.5 over 5 years of daily data (T = 1250). With the reported number of trials, trial-Sharpe variance and non-normal returns, the investor finds "only a 90% chance that the true SR associated with this strategy is greater than zero", so it fails at 95%. Had the analyst stopped after N = 46 trials, DSR would have been 0.9505 and passed. With normal returns it would have passed up to N = 88. (The exact N, variance, skewness and kurtosis values sit in equation images that did not extract; from memory they are N = 100, variance 1/2, skewness -3, kurtosis 10, unverified.)
- Advice in the paper: plan multiple testing in advance; "Investment theory, not computational power, should motivate what experiments are worth conducting." It suggests an optimal-stopping rule: sample about 37% (1/e) of the theoretically justified configurations, then stop at the first later one that beats all of them.
- Implication (my inference): a backtest Sharpe of 2.5 on 5 years of daily data can be noise if you ran 100 variants with fat-tailed returns. We should log every variant (we already do in `tries.jsonl`), estimate the effective number of independent trials, and report DSR next to every Sharpe. Negative skew (typical of short-volatility and mean-reversion rules) makes things worse.

### 3. Bailey, Borwein, Lopez de Prado & Zhu, "The Probability of Backtest Overfitting" `[opened: full text]`
Bailey, D. H., Borwein, J. M., Lopez de Prado, M., Zhu, Q. J. (2015 revised version). Published in Journal of Computational Finance 20(4), 2017 (venue from memory, unverified).
URL: https://www.davidhbailey.com/dhbpapers/backtest-prob.pdf

- Method: combinatorially symmetric cross-validation (CSCV). Split the matrix of trial returns into S blocks, form every half/half combination, pick the best configuration in the in-sample half and record its rank in the out-of-sample half. PBO is the share of splits in which the in-sample winner falls below the median out of sample. The abstract says standard holdout "tend[s] to be unreliable and inaccurate in the context of investment backtests".
- Synthetic overfit example: every in-sample Sharpe is positive (range 1 to 3), "about 78% of the SR OOS are negative", PBO 74%. "The higher the SR IS, the lower the SR OOS." A real strategy (unnamed) shows PBO 0.04% with only 3% negative OOS Sharpes.
- Seasonal example on a pure random walk: 1,000 daily prices (about 4 years); searching 8,800 combinations of entry day, holding period, stop-loss and side gives an optimal annualized Sharpe of 1.27 and a probabilistic Sharpe statistic of 2.83 ("less than 1% probability that the true Sharpe ratio is below 0"). CSCV finds about 53% of OOS Sharpes negative and PBO 55%. With a real monthly effect planted (first 5 days of each month shifted by a quarter of a standard deviation), the best Sharpe is 1.54 and PBO falls to 13%.
- Implication (my inference): this is exactly our risk. A calendar or entry-day rule tuned on 4 years of a single asset can show Sharpe 1.3 with "p < 1%" on pure noise. Running CSCV over all variants we try for a rule family is cheap and tells us whether the selection process works, not just whether the winner looks good.

### 4. Harvey & Liu, "Backtesting" `[opened: full text]`
Harvey, C. R., Liu, Y. (2015). Journal of Portfolio Management, Fall 2015 (pages 13 onward in that issue).
URL: https://people.duke.edu/~charvey/Research/Published_Papers/P120_Backtesting.PDF

- Starting point: "A common practice in evaluating backtests of trading strategies is to discount the reported Sharpe ratios by 50%." They replace the rule of thumb with a multiple-testing haircut (Bonferroni, Holm, BHY), using the factor-population model from Harvey, Liu & Zhu.
- Key finding: the haircut is nonlinear. "The haircut is almost always more than and sometimes much larger than 50% when the annualized Sharpe ratio is less than 0.4. On the other hand, when the Sharpe ratio is greater than 1.0, the haircut is at most 25%." So "50% is too lenient for relatively small Sharpe ratios (< 0.4) and too harsh for large ones (> 1.0)." This holds for the parameter grid in their exhibits; it is not universal.
- Examples: with 50 trials, the haircut is "almost 50%" for the weakest published strategy they show (an E/P sort) but only 7.9% for the strongest (betting against beta). Worked program example: 120 monthly observations (10 years), annualized Sharpe 1.0, monthly autocorrelation 0.1 (autocorrelation-corrected Sharpe 0.912), 100 tests with average correlation 0.4: under BHY the adjusted Sharpe is 0.438, a haircut of 52.0%.
- Caveat they state: high observed Sharpes can come from negatively skewed, option-like returns; the method does not handle that.
- Implication (my inference): for the kind of Sharpe we can plausibly see on a long-only 6-asset book (0.3 to 0.8 above buy-and-hold is generous), the haircut after even modest searching is likely 50% or more, and a marginal improvement of 0.1 to 0.2 in Sharpe over buy-and-hold should be treated as zero unless it was pre-registered.

### 5. Arnott, Harvey & Markowitz, "A Backtesting Protocol in the Era of Machine Learning" `[opened: full text]`
Arnott, R., Harvey, C. R., Markowitz, H. (2019). Journal of Financial Data Science 1(1), 64-74. DOI 10.3905/jfds.2019.1.064. SSRN 3275654.
URL: https://papers.ssrn.com/abstract=3275654 (I read a third-party copy of the SSRN PDF: https://www.smallake.kr/wp-content/uploads/2023/04/SSRN-id3275654.pdf)

- Opening example: a long-short NYSE strategy built from letters of ticker symbols, found on 1963-1988 and "validated out of sample with even stronger results over the years 1989 through 2015", nearly 6% alpha a year, turnover under 10% a year. It is pure data mining across thousands of letter combinations. Lesson: a single chronological holdout can be passed by a false strategy when you search hard enough.
- Data limits: "about 55 years of high-quality equity data (or less than 700 monthly observations) ... far too small for most machine learning applications, and impossibly small for advanced approaches such as deep learning."
- Seven-point protocol (Exhibit 2): (1) research motivation: economic foundation stated before the research; (2) multiple testing: keep track of all models and variables tried, successful and not, and do not stop as soon as a good model appears; (3) data and sample choice: transformations, outlier rules and winsorization chosen in advance, results robust to small changes; (4) cross-validation: "true out-of-sample tests are only possible in live trading", no out-of-sample "iterations", costs included; (5) model dynamics: structural change, crowding, minimal tweaking of a live model; (6) complexity: avoid the curse of dimensionality, simplest practicable specification, interpret the model; (7) research culture: reward good science, accept "that most tests will fail".
- Implication (my inference): this checklist maps directly onto a small lab. Our forward paper ledger is the only true out-of-sample test. Any rule changed after seeing paper results starts a new trial with a new ledger entry. With 6 assets and at most about 20 years of daily ETF data (about 11 years for BTC with usable volume, under 10 for ETH), deep models have no data to learn from.

### 6. Bailey, Borwein, Lopez de Prado & Zhu, "Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance" `[not opened]`
Bailey, D. H., Borwein, J. M., Lopez de Prado, M., Zhu, Q. J. (2014). Notices of the American Mathematical Society 61(5), 458-471.
URL tried: https://www.ams.org/notices/201405/rnoti-p458.pdf (HTTP 403); author-site copy not found.

- `[from memory, unverified]`: the paper introduces the minimum backtest length (MinBTL). Its headline example, as I remember it: with 5 years of daily data, a researcher should try no more than about 45 independent configurations, or the best one is expected to show an in-sample annualized Sharpe of 1 even when every configuration has a true Sharpe of zero. It also argues that overfitting in the presence of memory (serial correlation) produces negative out-of-sample performance, not just zero. I could not open the paper to check these numbers.
- Implication (my inference): if the memory is right, 5 years of data supports only a few dozen honest tries per rule family. Our crypto history is barely long enough for that.

---

## A2. Out-of-sample decay and the replication record

### 7. McLean & Pontiff, "Does Academic Research Destroy Stock Return Predictability?" `[opened: full text]`
McLean, R. D., Pontiff, J. (2016). Journal of Finance 71(1), February 2016.
URL: https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12365 (publisher page returned 403; I read the journal PDF at https://www.gwern.net/doc/economics/2016-mclean.pdf)

- Sample: 97 variables shown in published papers to predict cross-sectional US stock returns; long-short extreme-quintile portfolios, compared in-sample, out-of-sample but before publication, and after publication.
- Claim (abstract): "Portfolio returns are 26% lower out-of-sample and 58% lower post-publication." The 26% is "an upper bound estimate of data mining effects"; the difference, 32%, is attributed to publication-informed trading. They reject both "predictability disappears entirely" and "no change".
- Which decay more: "Post-publication declines are greater for predictors with higher in-sample returns" and higher in-sample t-statistics. The decay "is larger for predictors that can be constructed with only price and trading data". Post-publication returns are lower where arbitrage is cheap (liquid, low idiosyncratic risk stocks).
- Costs: not netted; these are gross long-short returns.
- Implication (my inference): price-only signals in liquid instruments, which is all we have (SPY, QQQ, GLD, TLT, BTC, ETH), are the category that decays most. Expect a published effect to be at least halved, and more if its in-sample Sharpe was striking.

### 8. Hou, Xue & Zhang, "Replicating Anomalies" `[opened: abstract page]`
Hou, K., Xue, C., Zhang, L. (2017). NBER Working Paper 23394; published in Review of Financial Studies 33(5), 2020, 2019-2133.
URL: https://www.nber.org/papers/w23394

- Sample: a library of 447 anomaly variables in US stocks, rebuilt with NYSE breakpoints and value-weighted returns to limit microcap influence.
- Claim: 286 of 447 (64%) are insignificant at the 5% level, including 95 of 102 liquidity variables (93%). With a t cutoff of 3, 380 (85%) are insignificant. Of the 161 that survive, many are much smaller than originally reported, and the q-factor model leaves 115 of those alphas insignificant (150 with t < 3).
- Costs: not in the abstract.
- Implication (my inference): most published effects depended on microcaps and equal weighting. Our universe is the opposite extreme: six of the most liquid instruments in the world. Anything that relied on illiquidity or small size should be assumed absent.

### 9. Jensen, Kelly & Pedersen, "Is There a Replication Crisis in Finance?" `[opened: abstract page]`
Jensen, T. I., Kelly, B. T., Pedersen, L. H. (2021). NBER Working Paper 28432; published in Journal of Finance 78(5), 2023, 2465-2518.
URL: https://www.nber.org/papers/w28432

- Sample: a large set of published equity factors (the abstract gives no count; from memory it is 153, unverified), US plus a new dataset covering 93 countries.
- Claim: with a Bayesian model of factor replication, "most" factors replicate, group into 13 themes, stay significant in the tangency portfolio, and work out of sample internationally. They argue the large number of factors strengthens the evidence rather than weakening it.
- Contrast with entry 8: the difference is mainly method (Bayesian shrinkage across related factors, and a different standard for "replicates"). Both are cross-sectional, long-short equity results, gross of costs.
- Implication (my inference): the replication debate is about cross-sectional stock factors, which we cannot trade. The positive reading (factors are real but smaller) still says nothing about timing six assets. For us the relevant lesson is that themes with economic motivation and many independent confirmations (for example time-series momentum, covered in other parts) are more credible than single-paper effects.

### 10. Suhonen, Lennkh & Perez, "Quantifying Backtest Overfitting in Alternative Beta Strategies" `[opened: secondary summary]`
Suhonen, A., Lennkh, M., Perez, F. (2017). Journal of Portfolio Management 43(2), Winter 2017 (volume and issue from memory, unverified; the season and journal are from the search summary).
URL read: https://www.cxoadvisory.com/big-ideas/live-performance-of-alternative-beta-products/ (summary of the March 2016 working paper)

- Sample: 215 investable "alternative beta" (bank risk-premia index) strategies from 15 investment banks, 5 asset classes, 11 strategy types, daily USD returns January 1990 to early March 2015, split at each product's live date.
- Claim: median annualized Sharpe 1.20 in the backtest versus 0.31 live, a 73% decline. Deterioration was at least 50% for every asset class. Only 18 of 215 had a live Sharpe at or above the backtest; 65 of 215 had a negative live Sharpe. The most complex strategies deteriorated about 30% more than the simplest. The authors conclude a 50% haircut is not conservative enough.
- Costs: these are bank indices, typically net of index fees (my understanding, not checked in the summary).
- Implication (my inference): this is the closest real-money analogue to our case: systematic rules on liquid futures and indices, designed by professionals, then run live. Plan on keeping roughly a quarter of a backtest Sharpe, and less for complex rules.

### 11. Wiecki, Campbell, Lent & Stauth, "All that glitters is not gold: Comparing backtest and out-of-sample performance on a large cohort of trading algorithms" `[opened: full text]`
Wiecki, T., Campbell, A., Lent, J., Stauth, J. (2016). Quantopian working paper, SSRN 2745220; later in Journal of Investing (per search summary, not checked).
URL read: https://c.mql5.com/forextsd/forum/208/All%20that%20Glitters%20Is%20Not%20Gold%20-%20Comparing%20Backtest%20and%20Out-of-Sample%20Performance%20on%20a%20Large%20Cohort%20o.pdf (third-party copy of the SSRN PDF)

- Sample: 888 algorithms written on Quantopian, backtested 2010 to mid-2015, with at least 6 months of out-of-sample (paper) performance, June 2015 to February 2016. US equities.
- Claim: backtest Sharpe "offer[s] little value in predicting out of sample performance (R² < 0.025)". IS versus OOS Sharpe: Pearson R² = 0.02; the Sharpe over the last in-sample year did a bit better (R² = 0.05). Volatility and drawdown carry over well (R² = 0.67 and 0.34). The more backtesting an author did, the larger the Sharpe shortfall (significant but small effect, Spearman R² = 0.017). "The higher the IS Sharpe ratio, the lower the OOS Sharpe ratio, and the larger the shortfall" (figure caption). A nonlinear classifier on many backtest features reached R² = 0.17 on hold-out data.
- Caveats they state: the IS period was a calm bull market and the OOS period a flat-to-bear market, so part of the gap is regime.
- Implication (my inference): risk carries over from backtest to live; return does not. We should size positions on backtest volatility and drawdown, but treat the backtest return as close to uninformative. Counting backtest runs per strategy (which our ledger does) is justified by their finding that more runs mean a bigger shortfall.

