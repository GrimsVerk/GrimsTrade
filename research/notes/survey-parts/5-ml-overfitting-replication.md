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

---

## A3. Technical trading rules, data snooping, return predictors

### 12. Sullivan, Timmermann & White, "Data-Snooping, Technical Trading Rule Performance, and the Bootstrap" `[not opened]`
Sullivan, R., Timmermann, A., White, H. (1999). Journal of Finance 54(5).
URL tried: https://onlinelibrary.wiley.com/doi/abs/10.1111/0022-1082.00163 (HTTP 403).

- What I know comes from entry 13, which reuses their universe: 7,846 technical rules (filters, moving averages, support and resistance, channel breakouts, on-balance volume) on daily Dow Jones prices, tested with White's Reality Check bootstrap so that the best rule is judged against the whole search.
- Entry 13 says that "as reported in, e.g., STW ... the rules did poorly in more recent periods." `[from memory, unverified]`: STW found the best rule significant on 1897-1986 even after the Reality Check, but not in the 1987-1996 out-of-sample decade.
- Implication (my inference): the canonical data-snooping-controlled test of technical rules on a US index found the edge gone by the late 1980s.

### 13. Bajgrowicz & Scaillet, "Technical trading revisited: False discoveries, persistence tests, and transaction costs" `[opened: full text]`
Bajgrowicz, P., Scaillet, O. (2012). Journal of Financial Economics 106(3), 473-491. DOI 10.1016/j.jfineco.2012.06.001.
URL read: https://bashtage.github.io/kevinsheppard.com/files/teaching/mfe/advanced-econometrics/Bajgrowicz_Scaillet.pdf (copy of the journal PDF)

- Sample: daily Dow Jones Industrial Average, 1897 to 2011, the same 7,846 rules as STW, split into six subperiods. Data snooping controlled with the false discovery rate (FDR), which admits more true rules than the Reality Check.
- Claim (abstract): "even with the more powerful FDR technique, an investor would never have been able to select ex ante the future best-performing rules. Moreover, even in-sample, the performance is completely offset by the introduction of low transaction costs."
- Costs: one-way costs of 16, 35 and 70 bps are enough to remove all detected outperformers in the three subperiods covering 1897-1962. "In the three most recent sample periods (1962-2011), we do not detect any positive performance ... already under zero transaction costs." In 1962-1986 most rules with positive in-sample performance "require costs below 10 basis points to break even."
- Rule horizon: without costs the best 1939-1962 rule uses a 2-day window; with 12.5 bps one-way costs the best rule needs 250 days of data. Costs push the survivors toward slow, long-window rules.
- Implication (my inference): fast technical rules on a liquid US index have had no edge since the 1960s, even before costs. If any technical rule is worth testing on SPY/QQQ, it is a slow one (around 200-250 days), and it should be judged as a risk filter against buy-and-hold, not as alpha.

### 14. Goyal, Welch & Zafirov, "A Comprehensive 2022 Look at the Empirical Performance of Equity Premium Prediction" `[opened: abstract page]`
Goyal, A., Welch, I., Zafirov, A. (2024). Review of Financial Studies 37(11), 3490-3557. Working paper SFI 21-85 (2021).
URL: https://ideas.repec.org/a/oup/rfinst/v37y2024i11p3490-3557..html

- Sample: 29 variables from 26 papers published after Goyal and Welch (2008), plus the original 17, for predicting the US equity premium, with data to the end of 2021.
- Claim (abstract): "More than one-third of these new variables no longer have empirical significance even in-sample. Of those that do, half have poor out-of-sample performance. A small number of variables still perform reasonably well both in-sample and out-of-sample." The abstract does not name the survivors.
- Background `[from memory, unverified]`: Welch and Goyal (2008, RFS) found that the classic predictors (dividend yield, earnings yield, term spread and others) mostly failed to beat the historical mean out of sample.
- Implication (my inference): market timing of SPY with macro or valuation variables has a poor record. A daily-bar system should not expect to time the equity premium; the default should be to hold the asset and use rules mainly to manage risk.

### 15. Hudson & Urquhart, "Technical trading and cryptocurrencies" `[not opened]`
Hudson, R., Urquhart, A. (2021). Annals of Operations Research 297, 191-220. DOI 10.1007/s10479-019-03357-1.
URL tried: https://centaur.reading.ac.uk/85715 (bot-protection page, access denied).

- From the search summary only: almost 15,000 technical rules from five classes, on two Bitcoin markets and three other cryptocurrencies. They report significant predictability and profitability in every class and coin, robust to multiple-hypothesis (data-snooping) procedures, with higher risk-adjusted returns than buy-and-hold. I could not check the sample period, costs, or whether there is a true out-of-sample period.
- Implication (my inference): unlike the Dow, crypto technical rules have at least survived data-snooping corrections in-sample. That is a weaker claim than out-of-sample profit after 60 bps.

### 16. Deprez & Frommel, "Are simple technical trading rules profitable in bitcoin markets?" `[opened: abstract page]`
Deprez, N., Frommel, M. (2024). International Review of Economics & Finance 93(PB), 858-874. DOI 10.1016/j.iref.2024.05.003.
URL: https://ideas.repec.org/a/eee/reveco/v93y2024ipbp858-874.html

- Sample: Bitcoin; 75,360 simple technical rules in 6 classes, daily and intraday. Dates not on the abstract page.
- Method (abstract): select the best rules after transaction costs with a multiple-hypothesis procedure, combine the selected rules into portfolios, then evaluate out of sample.
- Claim: "especially risk-return wise, simple technical trading rules can outperform a buy-and-hold strategy in the bitcoin market out-of-sample." No cost level, Sharpe or return figures on the page.
- Implication (my inference): this is the most directly relevant design (costs, snooping control, out-of-sample) and it comes out positive for Bitcoin, mainly on risk-adjusted terms. That fits the common finding that trend filters on BTC mostly cut drawdowns. Their cost assumption is unknown to me and may be below our 60 bps.

### 17. Detzel, Liu, Strauss, Zhou & Zhu, "Learning and predictability via technical analysis: Evidence from bitcoin and stocks with hard-to-value fundamentals" `[opened: abstract page]`
Detzel, A., Liu, H., Strauss, J., Zhou, G., Zhu, Y. (2021). Financial Management 50(1), 107-137. DOI 10.1111/fima.12310.
URL: https://ideas.repec.org/a/bla/finmgt/v50y2021i1p107-137.html

- Claim (abstract): "ratios of prices to their moving averages forecast daily Bitcoin returns in and out of sample. Trading strategies based on these ratios generate an economically significant alpha and Sharpe ratio gains relative to a buy-and-hold position." Similar results for small-cap, young-firm, low-coverage stocks and NASDAQ stocks in the dotcom era. They give an equilibrium model where learning about hard-to-value fundamentals makes moving averages informative.
- Costs and numbers: not on the abstract page. A CXO Advisory summary of the January 2018 working paper (seen only as a search snippet, `[not opened]`) mentions 5- to 100-day moving averages and gross annualized returns of roughly 203% to 216%, gross of costs.
- Implication (my inference): there is a stated economic reason (hard-to-value assets, learning) for trend rules to work in BTC and not in SPY. That is the kind of prior the AHM protocol (entry 5) asks for. It also predicts that the effect weakens as Bitcoin matures, so later data should be weighted more.

---

## B1. Machine learning for return prediction

### 18. Gu, Kelly & Xiu, "Empirical Asset Pricing via Machine Learning" `[opened: abstract page]`
Gu, S., Kelly, B., Xiu, D. (2018, revised 2019). NBER Working Paper 25398; published in Review of Financial Studies 33(5), 2020.
URL: https://www.nber.org/papers/w25398

- Sample `[from memory, unverified]`: about 30,000 US stocks, 1957-2016, monthly, about 900 predictors (94 firm characteristics interacted with macro variables), with an out-of-sample period starting in 1987.
- Claim (abstract page, paraphrased by the fetch tool): ML forecasts give large economic gains, "in some cases" doubling the performance of leading regression strategies. Trees and neural networks do best, through nonlinear interactions. All methods agree on a small set of dominant signals: variations on momentum, liquidity and volatility. The page shows no Sharpe or R² figures. `[from memory, unverified]`: the monthly out-of-sample R² for individual stocks is well under 1% (about 0.4% for the best neural net).
- Critique (entry 20, Israel, Kelly & Moskowitz, one of whom is a co-author here): the benchmark is OLS with only size, value and momentum, and all results are gross of trading costs.
- Implication (my inference): the gains come from thousands of stocks in the cross-section. With six assets there is no cross-section to learn from, and the dominant signals (momentum, volatility) are ones we can code directly with two or three parameters.

### 19. Avramov, Cheng & Metzker, "Machine Learning vs. Economic Restrictions: Evidence from Stock Return Predictability" `[opened: abstract page]`
Avramov, D., Cheng, S., Metzker, L. (2023). Management Science 69(5), 2587-2619. DOI 10.1287/mnsc.2022.4449.
URL: https://econpapers.repec.org/RePEc:inm:ormnsc:v:69:y:2023:i:5:p:2587-2619

- Claim (abstract): deep learning signals "extract profitability from difficult-to-arbitrage stocks". Excluding microcaps, distressed stocks, or high-volatility episodes considerably weakens profitability. "Machine learning-based performance further deteriorates in the presence of reasonable trading costs", due to high turnover and extreme positions. On the positive side, ML identifies mispriced stocks consistent with most anomalies, and deep learning signals stay profitable on the long side, in recent years, with low downside risk.
- Implication (my inference): the ML premium in equities lives where we are not (microcaps, distressed names, crisis periods) and is eaten by turnover. For six liquid instruments, the ML edge reported in the cross-section should be assumed to be zero.

### 20. Israel, Kelly & Moskowitz, "Can Machines 'Learn' Finance?" `[opened: full text]`
Israel, R., Kelly, B., Moskowitz, T. J. (2020). Journal of Investment Management 18(2), 23-36. AQR version.
URL read: https://www.aqr.com/-/media/AQR/Documents/Alternative-Thinking/AQR-Alternative-Thinking-2Q19-Can-Machines-Learn-Finance.pdf

- Small data: for macro instruments (currencies, government bonds, commodity futures) "a few decades of data, or a few hundred observations per asset" at monthly frequency. "This is 'tiny' data as it can only support a model with a handful of parameters if one hopes to achieve a degree of model stability." The number of independent observations of the target, not the number of predictors, limits the model.
- Correlation shrinks the effective sample: 71% average pairwise correlation among the Fama-French 100 portfolios; 3 principal components explain at least 80% of their covariance over 1927-2019.
- Low signal-to-noise is enforced by competition: informed traders trade until little predictability remains. In-sample CAPE regressions on the US market (1926-2018): R² 0.5% at 1 month (1,115 observations), 7.7% at 12 months (93), 28.3% at 36 months (31), 29.6% at 60 months (19 independent observations). Longer horizons have more signal but far fewer observations.
- On Gu, Kelly & Xiu: gains are "economically and statistically significant, but the gains are by no means revolutionary"; the benchmark is a 3-predictor OLS and results are gross of costs. Higher-frequency prediction runs into trading costs that open "a large gap between what a statistical prediction model says and what can actually be implemented".
- Their suggestion: ML is better suited to areas with stronger signal-to-noise (risk management, transaction cost modelling, factor construction) than to return prediction.
- Implication (my inference): for six daily series this is decisive. Daily data adds observations but not independent signal, and costs grow with frequency. A model with more than a handful of parameters per asset will mostly fit noise. If we use ML at all, use it for volatility and risk forecasts, where signal-to-noise is high.

### 21. Lim, Zohren & Roberts, "Enhancing Time Series Momentum Strategies Using Deep Neural Networks" `[opened: abstract page]`
Lim, B., Zohren, S., Roberts, S. (2019). Journal of Financial Data Science, Fall 2019. arXiv 1904.04912.
URL: https://arxiv.org/abs/1904.04912

- Sample: backtest on 88 continuous futures contracts; dates not on the abstract page (`[from memory, unverified]`: roughly 1990s to 2015, with testing from the mid-1990s).
- Claim: an LSTM trained to maximize Sharpe directly (deep momentum network) "improved traditional methods by more than two times in the absence of transactions costs". It keeps outperforming only with costs up to about 2-3 basis points.
- Implication (my inference): the edge is fragile to costs even on futures. At 60 bps per crypto round trip, or even 4 bps per ETF round trip, a net-of-cost advantage over plain time-series momentum is unlikely. A deep model also has far more parameters than six daily series can support (entry 20).

### 22. Kelly, Malamud & Zhou, "The Virtue of Complexity in Return Prediction" `[opened: abstract page]`
Kelly, B. T., Malamud, S., Zhou, K. (2022, revised 2022). NBER Working Paper 30217; published in Journal of Finance 79(1), 2024, 459-503. DOI 10.1111/jofi.13298.
URL: https://www.nber.org/papers/w30217

- Claim (abstract): "we theoretically prove that simple models severely understate return predictability compared to 'complex' models" in which parameters exceed observations; "Our findings establish the rationale for modeling expected returns through machine learning." The empirical application is US stock market timing (abstract page gives no Sharpe or sample numbers). `[from memory, unverified]`: the application uses about 15 predictors from Welch and Goyal, expanded into thousands of random Fourier features, trained on rolling 12-month windows, monthly.

### 23. Nagel, "Seemingly Virtuous Complexity in Return Prediction" `[opened: abstract page]`
Nagel, S. (2025). NBER Working Paper 34104, August 2025.
URL: https://www.nber.org/papers/w34104

- Claim (abstract): the random Fourier features approach "appears to yield a successful out-of-sample stock market index timing strategy even when trained in rolling windows as small as T = 12 months with P in the thousands." But when P is much larger than T, the forecast "becomes a weighted average of the T training sample returns". In short windows it "reduces to a recency-weighted average of the T return observations in the training data, essentially a momentum strategy", and since similarity falls as predictor volatility rises, "the result is a volatility-timed momentum strategy." The performance comes from the fact that "a volatility-timed momentum strategy happened to perform well in historical data." On artificial data with reversals instead of momentum, "the RFF approach still constructs the same volatility-timed momentum strategy, which then performs poorly."
- Other critics named in the brief (Buncic 2025; Cartea et al.) were not opened.
- Implication (my inference): the strongest recent "complexity" result for timing an index is, underneath, a volatility-scaled 12-month momentum rule. We can test that rule directly with two parameters. This is a general warning: before trusting any ML timing model, check whether a simple trend or volatility rule replicates its returns.

---

## B2. Time-series foundation models on financial returns

### 24. Rahimikia, Ni & Wang, "Re(Visiting) Time Series Foundation Models in Finance" `[opened: full text, first ~80% of the HTML]`
Rahimikia, E., Ni, H., Wang, W. (2025). arXiv 2511.18578, November 2025.
URL: https://arxiv.org/html/2511.18578v1

- Sample: daily firm-level excess returns in 94 countries from 1990, about two billion observations; expanding-window out-of-sample test 2001-2023 (US test set: 10,171 securities). Context windows of 5, 21, 252 and 512 trading days.
- Models: Chronos (tiny to large), TimesFM (8M to 500M), and twelve more TSFM architectures said to behave similarly; benchmarks are linear models, tree ensembles (XGBoost, CatBoost, LightGBM) and neural nets. R² is measured against a zero forecast.
- Claim: "Off-the-shelf TSFMs perform poorly." Zero-shot out-of-sample R²: Chronos-large -1.37% (window 512, direction accuracy just above 51%), TimesFM-500M -2.80% (accuracy just below 50%). Every model, including the benchmarks, has negative R² against a zero forecast (OLS about -0.47%, CatBoost about -0.10%). Fine-tuning mostly made TSFMs worse. Pre-training from scratch on financial data helps (Chronos-small R² -0.59% at window 512). "Generic time series pre-training does not directly transfer to financial domains."
- Portfolios: daily-rebalanced, equal-weighted long-short decile sorts across thousands of stocks, before transaction costs (stated for CatBoost; I did not reach the cost section for the TSFM portfolios). CatBoost US Sharpe 6.79; zero-shot TimesFM-500M annual return -1.47%. Such Sharpes come from daily cross-sectional sorts over thousands of small stocks and would not survive costs (my inference).
- Implication (my inference): on daily returns, no model in this large study beat a zero forecast in R². A foundation model run zero-shot on six daily series has no reason to do better. For our book, the honest benchmark is "predict zero, hold the asset" and none of these models clears it.

### 25. Noguer i Alonso & Pereira Franklin, "Pretrained Time-Series Foundation Models for Financial Return Forecasting" `[opened: abstract page]`
Noguer i Alonso, M., Pereira Franklin, R. (2026). arXiv 2606.27100, June 2026.
URL: https://arxiv.org/abs/2606.27100

- Sample: five liquid US stocks (AAPL, AMZN, GOOG, JPM, META), rolling-origin evaluation; frequency not on the abstract page.
- Models: TimeGPT, TimesFM-2.5, Moirai-2.0, Chronos, Chronos-2 versus train-from-scratch nets (N-BEATS, N-HiTS, PatchTST, iTransformer, KAN) and a random walk.
- Claim: pretrained models win 8 of 10 task-level rankings against the scratch-trained nets, but "gains over the random-walk benchmark are small and sparse." A one-sided Diebold-Mariano test shows superiority over the random walk only for Chronos on AMZN and Moirai-2.0 on GOOG, i.e. 2 cases in a grid of models and stocks. No trading test, no costs.
- Implication (my inference): two significant cells out of a grid is about what chance produces. On a handful of liquid series (our setup), TSFMs do not beat a naive forecast in a way that could pay 4 to 60 bps per round trip.

