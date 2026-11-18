# Survey part 6: fractional differentiation, path signatures, TDA, information theory, econophysics, ecology

Scope: ideas borrowed from other fields, judged for one setup: BTC, ETH, SPY, QQQ, GLD, TLT; daily bars; long-only, no leverage; decide after the US close, fill at next open; costs 30 bps per crypto trade, 2 bps per ETF trade; about 9-10 years of joint history (roughly 2,300-2,500 ETF trading days).

Question: what held up out of sample and after costs, and what failed?

## How to read this file

Each entry carries a status tag:

- `[opened: full text]` - I read the body of the paper (HTML or extracted PDF text). Numbers come from the text.
- `[opened: abstract page]` - I opened the publisher/arXiv/repository page and read only the abstract. No numbers beyond the abstract.
- `[not opened: ...]` - cited from a search-result summary, a secondary source or memory. Treat as unverified.

Reading was cut short by a fetch limit near the end, so several planned sources (López de Prado's book text, Hosking, Gabaix, Taleb, Bandt & Pompe, Dimpfl & Peter, Urquhart) stayed unopened. They are marked.

Lines starting with "Own note:" are my reasoning, not a claim made by the source.

Counts: 27 sources opened (16 full or partial full text, 11 abstract page only), 9 not opened.

---

## A. Fractional differentiation

### A1. López de Prado (2018), Advances in Financial Machine Learning, ch. 5 "Fractionally Differentiated Features" `[not opened: from secondary documentation and memory]`
- Citation: M. López de Prado, *Advances in Financial Machine Learning*, Wiley, 2018. Book link not verified. Secondary description (appeared in search, page itself not opened): https://mlfinpy.readthedocs.io/en/latest/FractionalDifferentiated.html
- Claim: integer differencing (returns) makes a price series stationary but throws away memory; a fractional order d between 0 and 1 can pass a stationarity test while staying highly correlated with the price level. The fixed-width window variant (FFD) drops weights below a threshold so the same weight vector is used at every date. d is chosen as the smallest value at which the ADF statistic passes the 95% critical value.
- Numbers (from search summaries of library docs, unverified against the book): a worked example where ADF passes near d = 0.35; library default weight threshold 1e-5.
- Out-of-sample evidence in the source: none that I know of. The chapter argues the feature should help; it does not run an ablation with and without it.
- Own note: FFD is a fixed linear filter on log prices, so it equals a weighted sum of past returns with slowly decaying weights. A linear model given enough lagged returns already spans it. For a tree model it is one compact "distance from a long weighted average" feature, close in spirit to a price/moving-average ratio. The claim to test is therefore narrow: does it beat price/MA ratios and multi-horizon returns in the same model?
- Own note on window length (back-of-envelope, check numerically): weights decay like k^-(1+d)/|Γ(-d)|. For d = 0.4 the weight falls below 1e-5 only after roughly 1,500 lags, below 1e-4 after roughly 280 lags, below 1e-3 after roughly 55 lags. With 9-10 years of daily data, a 1e-5 threshold would eat most of the sample as warm-up. Use 1e-4 or 1e-3.

### A2. Hosking (1981), "Fractional differencing" `[not opened: from search summary of the abstract]`
- Citation: J. R. M. Hosking, Biometrika 68(1), 165-176, 1981. DOI from search result: https://doi.org/10.1093/biomet/68.1.165 (page not opened).
- Claim: generalises ARIMA to non-integer differencing order; the operator is an infinite binomial series in the lag operator; such processes show long-term persistence or anti-persistence.
- Relevance: the statistical origin (ARFIMA). It is a model of long memory, not evidence that long memory in prices is forecastable.

### A3. Stempień & Gajda (2025), "Comparative analysis of financial data differentiation techniques using LSTM neural network" `[opened: full text]`
- URL: https://arxiv.org/abs/2505.19243
- This is the closest thing I found to an independent out-of-sample test of fracdiff features in trading.
- Sample: S&P 500, WIG20, DAX, Nikkei 225, daily, 2014-01-01 to 2023-12-31. Train 2014-2020 (last two years as validation), test 2021-2023. Inputs: the differenced series plus technical indicators, fed to an LSTM.
- d chosen by the López de Prado ADF rule on the training part only: 0.46 (S&P 500), 0.12 (WIG20), 0.22 (DAX), 0.28 (Nikkei 225). Also tested: d from ARFIMA estimation, and a tempered variant (ARTFIMA).
- Claim: fracdiff inputs give lower forecast errors than log returns for most indices and better risk-adjusted trading results, especially for a portfolio of the four indices; "no single technique of fractional differentiation is universally superior".
- Numbers I read (Information Ratio = annualised return / annualised st. dev., test period, "transaction costs of 0.005%"). Long-only tables for the four indices, columns = log returns / López de Prado d / ARFIMA d / tempered / buy & hold (I did not confirm which table belongs to which index):
  - 0.58 / 0.68 / 0.62 / 0.15 / 0.50
  - 0.55 / 0.18 / 1.28 / 0.30 / 0.22
  - -0.38 / 0.41 / 1.08 / 0.19 / 0.39
  - 0.03 / 0.29 / 0.98 / -0.23 / 0.38
  - Portfolio long-only (my reading of the table order): 0.38 / 0.58 / 1.63 / 0.16 / 0.48.
- Critique: one 3-year test window, one path, no confidence intervals. Costs of 0.005% per trade are far below ours (2 bps ETF, 30 bps crypto). The López de Prado-d version beats buy & hold clearly in one of four index tables and is about level or worse in the others; the wins come from the ARFIMA-d variant, i.e. from a choice among four transforms made on the same test set. The tempered variant, the newest method, is the worst. This is weak support, not confirmation.
- For our setup: if tested, pick d on the training window only, per asset, by the ADF rule; expect d roughly 0.1-0.5; compare against log returns and a price/MA ratio in the same walk-forward model; charge real costs.

### A4. Gajda & Walasek (2020), "Fractional differentiation and its use in machine learning" `[not opened: from search summary]`
- University of Warsaw Working Paper 32/2020 (338). Listing seen in search: https://econpapers.repec.org/RePEc:war:wpaper:2020-32 (not opened).
- Claim per the summary: fracdiff series gave better RMSE/MAE than classical differencing in neural networks on four indices including WIG20 and S&P 500. Same research group as A3, so not an independent replication of it.

### A-summary: evidence gap
I searched for an ablation study (same model, with and without fracdiff features, clean walk-forward, realistic costs, multiple-testing control) and found none. I also found no formal published critique. The technique is widely repeated in tutorials and vendor documentation, which is not evidence.

---

## B. Path signatures / rough paths

Low-order facts used below (standard results; the lead-lag statements are confirmed in B2's text):
- Level 1 of the signature of a path over a window is the increment (the window return for a log-price path).
- Level 2 has a symmetric part (products of increments) and an antisymmetric part, the Lévy area. For two assets, the sign of the Lévy area says which one tended to move first within the window. For (time, price), the level-2 terms say whether the move came early or late in the window.
- After the lead-lag transform (pairing each series with a one-step-delayed copy), the Lévy area between a series' lead and its own lag equals its quadratic variation, i.e. realised variance.
- So a level-2 lead-lag signature of daily log prices contains: window returns, realised variances and covariances, and lead-lag areas. Most of it is features we already have under plainer names.

### B1. Chevyrev & Kormilitzin (2016), "A Primer on the Signature Method in Machine Learning" `[opened: abstract page]`
- URL: https://arxiv.org/abs/1603.03788
- Claim: tutorial on the signature as a feature set for sequential data; worked example is handwritten digit classification. No finance test in the abstract. The arXiv page notes it will appear in a Springer volume on signature methods in finance.
- Relevance: definitions only.

### B2. Gyurkó, Lyons, Kontkowski, Field (2013), "Extracting information from the signature of a financial data stream" `[opened: full text]`
- URL: https://arxiv.org/abs/1307.7244
- Sample: front-month WTI crude futures, level-one order book sampled by the minute in 30-minute buckets, 1 Jan 2011 to 1 Feb 2013; and FTSE 100 futures parent orders from two execution algorithms.
- Method: lead-lag transformed streams (time, price, spread, volumes), signature up to order 4, LASSO linear regression as a classifier; 75% of streams drawn at random for learning, 25% held out.
- Headline numbers: telling the 14:00-14:30 bucket from other buckets, out-of-sample correct classification 0.942-0.973, AUC 0.974-0.992 (Table 1). The 12:00-12:30 vs 12:30-13:00 pair is not distinguishable.
- The text states that with the lead-lag transform the signed area equals the quadratic variation of the mid price, and that a positive cross-area means a move in one series is followed by a same-direction move in the other.
- Critique: this is classification of intraday market states (the 14:30 pit close is an obvious regime), with a random split rather than a time-ordered one. No return forecast, no trading rule, no P&L. It says nothing about daily-bar trading.

### B3. Levin, Lyons, Ni (2013, rev. 2016), "Learning from the past, predicting the statistics for the future, learning an evolving system" `[opened: abstract page]`
- URL: https://arxiv.org/abs/1309.0260
- Claim: linear regression on truncated signatures of the past as a general nonparametric time-series method; on simulated AR and ARCH data it matched Gaussian-process regression accuracy at lower cost. The abstract mentions no real financial data.

### B4. Futter, Horvath, Wiese (2023), "Signature Trading: A Path-Dependent Extension of the Mean-Variance Framework with Exogenous Signals" `[opened: full text, experiment sections]`
- URL: https://arxiv.org/abs/2308.15135
- Claim: a strategy is a linear functional of the signature of the (lead-lag) market and signal path; the mean-variance optimal functional has a closed form given the expected signature; classical factor and momentum rules are special cases.
- Evidence in the passages I read: experiments are on simulated processes (a mean-reverting pair; an asset whose drift is a kernel-filtered Ornstein-Uhlenbeck signal). Real data appears as illustration: a SPY path from March-April 2020, and a MACD(10,20) rule on TLT in 2006. A signature functional reproduces a sigmoid-of-MACD position with figure labels R² = 66.1, 89.2, 89.6 as truncation order rises (text: order 3, "almost 90%"). Trade horizon in that example is 20 days.
- The paper says outright that fitting for out-of-sample robustness is left to the user, and that rolling refits "may lead to overfitting". I saw no out-of-sample Sharpe on market data and no transaction-cost treatment.
- For our setup: a framework, not evidence. The useful reading is the reverse one: an order-2 or order-3 signature rule is roughly a learned moving-average filter, so its upper bound at daily frequency is "a well-tuned trend rule".

### B5. Cuchiero & Möller (2023), "Signature Methods in Stochastic Portfolio Theory" `[opened: partial full text]`
- URL: https://arxiv.org/abs/2310.02322
- Claim: portfolios whose weights are linear in signature features of (ranked) market weights, fitted by log-wealth or mean-variance optimisation, beat the market portfolio out of sample "in almost all configurations", including with proportional transaction costs (1% and 5% are the levels named in the introduction).
- Design details I read: NASDAQ (ranked weights, 100 largest), SMI and S&P 500 (name-based); daily rebalancing; in-sample 2,000 days, out-of-sample 750 days; signature computed from 100 days before the investment period. I did not capture the headline return or Sharpe numbers (the results tables were outside the text I could read).
- Critique from the paper's own text: the universe is restricted to stocks that exist over the whole in- and out-of-sample period, which is survivorship bias, and the authors acknowledge it. Long-only is not imposed in the real-data runs as far as I could see. It is a large cross-section relative-value method, not a six-asset timing method.
- For our setup: little transfers. With six assets the "market weights" cross-section is too small.

### B-summary
I found no daily-frequency, time-ordered, after-cost test of signature features for return forecasting on a small multi-asset universe. The successful uses are intraday classification (B2), synthetic data (B3, B4) and large equity cross-sections with survivorship bias (B5).

---

## C. Topological data analysis (TDA)

### C1. Gidea & Katz (2018), "Topological data analysis of financial time series: Landscapes of crashes" `[opened: full text]`
- URL: https://arxiv.org/abs/1703.04385 (journal DOI on the page: 10.1016/j.physa.2017.09.028, Physica A)
- Sample: daily log returns of S&P 500, DJIA, NASDAQ, Russell 2000, 23 Dec 1987 to 8 Dec 2016 (7,301 trading days).
- Method: each window of w = 50 (also 100) days gives a cloud of w points in 4 dimensions; Rips filtration; 1-dimensional persistence (loops); persistence landscape; its L1 and L2 norms as a daily series. Then, following Guttal et al. (F2 below), variance, low-frequency spectral density and lag-1 autocorrelation of the norm series on a 500-day rolling window, examined over the 250 trading days before each crash.
- Headline numbers: low-frequency spectral density of the norm series rises over the 250 days before 10 Mar 2000 and 15 Sep 2008 with Kendall tau 0.89 and 1.00. Lag-1 autocorrelation shows no trend. For VIX on the same procedure: declining variability before 2000, tau 0.89 before Lehman.
- The critique is in the paper itself: in their Monte Carlo test with four white-noise series, the average L1 and L2 norms are linear in the noise variance, and the authors write that scaling the data by F multiplies the landscape area by F², "hence ... the values of the Lp-norms are proportional to the variance". They also state they do not claim the simulated models represent how crises occur.
- Other limits: two crash dates, both chosen in hindsight; no false-alarm count; no out-of-sample test; no trading rule.
- For our setup: replicating needs only w = 50, d = 6 assets, H1, L1 norm. The decisive check is whether the norm has any link to forward risk after controlling for average realised variance and mean pairwise correlation, or after standardising each asset by trailing volatility before building the cloud.

### C2. Gidea, Goldsmith, Katz, Roldan, Shmalo (2018/2020), "Topological recognition of critical transitions in time series of cryptocurrencies" `[opened: full text, method and results sections]`
- URL: https://arxiv.org/abs/1809.00695 (the arXiv page lists no journal reference; the published version is usually cited as Physica A, 2020, not verified here)
- Sample: Bitcoin, Ethereum, Litecoin, Ripple, daily, January 2016 to January 2018, one crash episode per coin (December 2017 - January 2018).
- Method: time-delay embedding of log returns with dimension 4, sliding window w = 50, L1 norm of the persistence landscape; then k-means with k = 18 on (log price, log return, L1 norm), each scaled to [0, 1]; clusters before the peak are identified by inspection.
- The authors state that the L1 norm also peaks at other times and "we cannot rely on the L1-norms alone to recognize approaching major crashes". k = 18 is larger than the elbow/silhouette/gap choices and was picked so that clusters span neither more than the 50-day window nor only a couple of days.
- Critique: one episode, cluster labels read off in hindsight, log price level is one of the clustering inputs (a cluster that means "price is at its high" will always precede a crash from the high), no out-of-sample test, no false-alarm analysis.
- For our setup: not testable as stated; the k-means step has no rule that could be fixed in advance.

### C3. Ismail, Md Noorani, Ismail, Abdul Razak (2022), "Early warning signals of financial crises using persistent homology and critical slowing down: evidence from different correlation tests" `[opened: full text]`
- URL: https://www.frontiersin.org/articles/10.3389/fams.2022.940133/full
- Sample and method: same four US indices, 22 Dec 1987 to 29 Dec 2017, window 50, L1 norm, then autocorrelation, variance and mean low-frequency power spectrum of the norm on a 500-point window, scored with Kendall, Spearman and Pearson trends.
- Result: only the power-spectrum indicator met their criteria. Their own scoring table (as summarised from the page) has more false alarms than hits, e.g. Kendall: 3 early warnings, 8 false alarms, 7 misses; Spearman: 4, 7, 7. Thresholds were set from the same two crises they are scored on.
- It does not compare against plain return variance and has no trading test. A replication of C1's procedure, not an independent validation of its usefulness.

### C4. "Shape of risk" practitioner note, Decimal Point Analytics (undated, no author named) `[opened: first half of page]`
- URL: https://decimalpointanalytics.com/ceo-desk/shape-of-risk.html
- Claim: in a live systematic equity programme (mid-cap universe, about seven years of daily data, rolling six-month correlation window, about 400 windows), persistent-homology signals from the correlation network were compared with the incumbent signal, cross-sectional return dispersion, as predictors of next-month realised downside variance.
- Numbers on the page (correlation with forward downside variance): cross-sectional dispersion +0.29; mean pairwise correlation -0.02; topological integration index -0.03; leading-eigenvalue share -0.01; loop persistence -0.04. The integration index is reported to match mean pairwise correlation at 0.99. The page says loop persistence failed a split-sample test but gives no split numbers and no after-cost results.
- Status: anonymous, not peer reviewed, not reproducible. I include it because it is the only source I found that ran the control everyone else skips (topology vs simple statistics), and it found nothing beyond the simple statistics.

### C5. Goel, Sharma, Kanniainen (2026), "Class of topological portfolios: Are they better than classical portfolios?" `[opened: abstract page]`
- URL: https://arxiv.org/abs/2601.03974
- Claim: choosing S&P 500 stocks to minimise a "topological risk" (Lp norm of persistence landscapes) beats seven portfolio optimisers, 1/N and the index over nearly a decade. The abstract mentions no transaction costs. Authors' own claim, no replication found; a stock-selection method that does not map onto six assets.

### C-summary
No out-of-sample, after-cost test of a TDA de-risking signal exists in what I found. The original authors show the norm scales with variance; the one source that controlled for simple statistics found no extra information.

---

## D. Information theory

### D1. Schreiber (2000), "Measuring information transfer" `[opened: abstract page]`
- URL: https://arxiv.org/abs/nlin/0001042 (Phys. Rev. Lett. 85, 461)
- Claim: transfer entropy, a directional measure that conditions on the target's own past, separates driving from responding systems where lagged mutual information cannot. Method paper; no finance.

### D2. Dimpfl & Peter (2013), "Using transfer entropy to measure information flows between financial markets" `[not opened: from search summary of the abstract]`
- Studies in Nonlinear Dynamics & Econometrics 17(1), 85-102. DOI from search: 10.1515/snde-2012-0044. Working-paper listing seen in search: https://econpapers.repec.org/RePEc:zbw:sfb649:sfb649dp2012-051 (not opened).
- Claim per the summary: transfer entropy with a bootstrap for inference, applied to CDS vs corporate bond markets and to VIX vs iTraxx, before, during and after the crisis. Descriptive information-flow results, not a trading test.

### D3. Jang, Yi, Kim, Ahn (2019), "Information flow between Bitcoin and other investment assets" `[opened: full text]`
- URL: https://www.mdpi.com/1099-4300/21/11/1116 (Entropy 21(11), 1116; text read through the Europe PMC copy of PMC7514459)
- Sample: Bitcoin, S&P 500, gold, USD/EUR; daily log returns; January 2014 to December 2018; 1,062 observations per series.
- Method: histogram transfer entropy (Freedman-Diaconis bins, lags 1 and 2) and symbolic transfer entropy on rise/fall patterns over 5-day windows; bootstrap significance. Granger tests at lag 1 for comparison.
- Results: histogram TE shows flow in both directions of similar size; symbolic TE shows flow mainly from the other assets to Bitcoin. Granger F-statistics: Bitcoin to gold 2.83 (10% level), gold to Bitcoin 0.04; Bitcoin and S&P 500 both directions at 10% (2.88 and 3.24); USD/EUR none. TE values are only in a figure.
- Critique: no forecast or trading test. Bitcoin's price is taken at 19:00 EST while the other series use their own closing times; a few hours of non-synchronous sampling is enough to manufacture a one-day "information flow". Results depend on bin and window choices.
- For our setup: the non-synchronous-close problem applies directly. Our crypto bars and ETF bars close at different times, and we fill at the next open. Any ETF-to-crypto lead measured on daily closes is mostly already in the crypto price by the time we can trade it.

### D4. Bandt & Pompe (2002), "Permutation entropy: a natural complexity measure for time series" `[from memory, unverified]`
- Phys. Rev. Lett. 88, 174102. Link not verified.
- Defines permutation entropy from the frequencies of ordinal patterns of length d in a series. Method paper.

### D5. Zunino, Zanin, Tabak, Pérez, Rosso (2009), "Forbidden patterns, permutation entropy and stock market inefficiency" `[opened: abstract page]`
- URL: https://ideas.repec.org/a/eee/phsmap/v388y2009i14p2854-2864.html (Physica A 388(14), 2854-2864)
- Claim: more forbidden ordinal patterns and lower normalised permutation entropy go with less efficient (less developed) stock markets. A ranking of markets, not a test that low-entropy periods can be traded.

### D6. Bariviera (2017), "The inefficiency of Bitcoin revisited: a dynamic approach" `[opened: full text]`
- URL: https://arxiv.org/abs/1709.08090 (Economics Letters 161, 1-4)
- Sample: daily Bitcoin prices, 18 Aug 2011 to 15 Feb 2017, 1,435 observations.
- Method: Hurst exponent by R/S and by detrended fluctuation analysis (block sizes 4 to 128), on a 500-observation sliding window stepped one day.
- Results: DFA Hurst exponent of returns above 0.5 before 2014 and near 0.5 afterwards (mean 0.57); R/S is biased towards finding long memory. Volatility (high-low range) has long memory throughout, DFA mean about 0.92. No trading test.
- For our setup: our sample starts after the persistent period this paper found. On its evidence BTC daily returns in our window have no long memory to exploit; volatility does, which supports volatility forecasting and volatility-scaled sizing, not direction.

### D7. Lo (2004), "The Adaptive Markets Hypothesis" `[opened: abstract page]`
- URL: https://web.mit.edu/~alo/www/Papers/JPM2004.html (Journal of Portfolio Management 30, 15-29)
- Claim: efficiency is not a fixed state; competition, adaptation and selection make predictability come and go. A framework. (A search summary says the paper illustrates this with 5-year rolling first-order autocorrelation of monthly S&P returns, 1871-2003; I did not read that part.)

### D8. Urquhart & McGroarty (2016); Urquhart, Gebka, Hudson (2015) `[not opened: from search summaries]`
- Listings seen in search: https://centaur.reading.ac.uk/79169 and https://centaur.reading.ac.uk/79166 (not opened).
- Claims per the summaries: on S&P 500, FTSE 100, Nikkei 225, Euro Stoxx 50 daily data 1990-2014, return predictability is significant in some periods and absent in others; the moving-average rule's predictive power fell in three developed markets after 1986. Consistent with adaptive markets; also consistent with "simple rules decay".

### D-summary
I searched for evidence that low-entropy or high-Hurst periods can be exploited by trend or reversal rules out of sample and found none: only descriptive efficiency rankings, plus blog-level anecdotes of failed Hurst regime switches. A 500-day window stepped daily over 10 years yields about five independent estimates, so "time-varying efficiency" plots have very few degrees of freedom.

---

## E. Econophysics

### E1. Filimonov & Sornette (2013), "A stable and robust calibration scheme of the log-periodic power law model" `[opened: abstract page]`
- URL: https://arxiv.org/abs/1108.0099 (Physica A 392(17), 3698-3707)
- Claim: rewriting the LPPL formula leaves three nonlinear parameters (critical time, exponent, log-frequency), with two of them slaved to the critical time; the cost function becomes smoother, usually with one minimum, so local search suffices. Tested on the Shanghai Composite, January 2007 to March 2008.
- Relevance: makes fitting stable. It is a numerical improvement and says nothing about predictive power.

### E2. Wheatley, Sornette, Huber, Reppen, Gantner (2019), "Are Bitcoin bubbles predictable? Combining a generalized Metcalfe's law and the LPPLS model" `[opened: full text]`
- URL: https://pmc.ncbi.nlm.nih.gov/articles/PMC6599809/ (Royal Society Open Science, DOI 10.1098/rsos.180538)
- Sample: 2,782 daily values, 17 July 2010 to 26 February 2018.
- Results: log market cap on log active addresses gives slope 1.69 (s.e. 0.0076), R² 0.95. Four main bubbles (peaks Aug 2012, Apr 2013, Nov 2013, Dec 2017). LPPLS critical-time estimates, with the true peak scaled to 1: 1.02, 1.05, 1.09, 1.01, with profile-likelihood intervals covering or just above 1. Fits using data up to 95% or 97.5% of a bubble's length still bracket the peak. In March 2018 they put fundamental value at about 22-44 billion USD against a market cap of 170 billion, "at least four times" overvalued, and predicted end-2018 values of 39-77 billion.
- Limits stated by the authors: full-bubble fits use hindsight (bubble start and end are known); only four bubbles, so false positives and misses cannot be assessed; the crash trigger is exogenous; active addresses are a poor user proxy; long-range extrapolation is "effectively meaningless"; R² may be spurious.
- Critique: no real-time forecast record. Bubble windows were chosen with knowledge of the peak. The Metcalfe valuation requires on-chain data we do not have in a daily-bar setup.

### E3. Brée & Joseph (2013), "Testing for financial crashes using the Log Periodic Power Law model" `[opened: full text, arXiv version]`
- URL: https://arxiv.org/abs/1002.1010 (International Review of Financial Analysis 30, 287-297)
- Sample: Hang Seng daily, 1970-2008; 11 crashes (peak with no higher value in the prior 262 weekdays, 25% drop within 60 weekdays).
- Results: fitted exponent and log-frequency fall inside the Johansen-Sornette ranges (0.15-0.51 and 4.8-7.92) for 7 of 11 pre-crash bubbles. The fit is erratic in the log-frequency, so minimum-error search is unreliable; bubble start dates in the earlier studies were moved by judgement; the minimum window of 131 weekdays matters. The price-must-rise condition implied by the proposed mechanism fails in many published cases; enforcing the positivity condition predicted crashes within a year in only 65 of 229 windows that were followed by crashes. The authors conclude the posited mechanism "must be incorrect" and that predictive success is partial. The 2007 crash was fitted well.
- For our setup: any LPPLS use must fix window-start rules and parameter filters before looking at outcomes, and must count windows that produced a "valid" fit with no crash afterwards.

### E4. Sornette et al. (2010), "The Financial Bubble Experiment: advanced diagnostics and forecasts of bubble terminations", volume II master document `[opened: full text]`
- URL: https://arxiv.org/abs/1005.5675
- What it is: the Financial Crisis Observatory's attempt at a clean record. Forecasts are published as hashes and revealed later, with a promise to report failures. This document lists forecast windows as of 12 May 2010 for palladium, platinum, NASDAQ and FTSE EPRA US (for example NASDAQ 20/80% window 5 July to 12 August 2010) plus three bubble candidates.
- Evidence: the document I opened contains no outcome assessment and no success rate; evaluation was deferred to a later document, and the authors say forecast-quality measures were still being developed. A search summary of the earlier batch describes mixed outcomes (two regime changes inside the window, one just before publication, one not). I found no independent scorecard of the Observatory's record. A vendor figure of "89% success" circulates in secondary sources; I could not trace it to a primary source and would not rely on it.

### E5. Gabaix (2009), "Power laws in economics and finance" `[not opened: from search summary]`
- NBER working paper 14299 (listing seen in search: https://www.nber.org/papers/w14299, not opened); later in Annual Review of Economics.
- Claim per the search summary of the underlying empirical work (Gopikrishnan et al.): return tails follow a power law with exponent about 3 (3.1 positive tail, 2.84 negative tail, measured from 2 to 100 standard deviations).
- Own note: with a tail exponent near 3, variance exists but the fourth moment does not. Sample variance converges slowly, sample kurtosis is meaningless, and Sharpe ratios from 9-10 years carry wider error bars than Gaussian formulas say.

### E6. Taleb (2020), Statistical Consequences of Fat Tails `[not opened: arXiv listing seen in search; content from memory, unverified]`
- Listing: https://arxiv.org/abs/2001.10488 (not opened).
- From memory: under fat tails the sample mean needs far more data to stabilise, tail estimates dominate outcomes, and any strategy with a non-zero chance of ruin should not be evaluated by expected value. On Kelly: the criterion maximises expected log growth and never bets into ruin, but it needs the true distribution; with fat tails and estimated parameters, full Kelly overbets, which argues for a fraction of Kelly.
- For our setup: no leverage and weights summing to at most 1 already cap the damage. The live risk is concentration in BTC/ETH after a good run, when estimated edge is highest.

### E-summary (Hurst and multifractality as regime indicators)
Beyond D6 I found no out-of-sample, after-cost study of a Hurst-based momentum/mean-reversion switch across several assets. Search results were vendor pages and anecdotes. The well-supported part is the critique: Hurst estimates from a few hundred points have wide confidence intervals and R/S is biased upward.

---

## F. Ecology and complex systems

### F1. Scheffer et al. (2009), "Early-warning signals for critical transitions" `[opened: abstract only, via Europe PMC]`
- Citation: Nature 461, 53-59. https://doi.org/10.1038/nature08227 (publisher page is behind a login).
- Claim: systems approaching a tipping point show generic early-warning signals; the abstract names financial markets as an example system. The specific indicators (rising lag-1 autocorrelation and variance, i.e. critical slowing down) are in the body, which I did not read.

### F2. Guttal, Raghavendra, Goel, Hoarau (2016), "Lack of critical slowing down suggests that financial meltdowns are not critical transitions, yet rising variability could signal systemic risk" `[opened: full text]`
- URL: https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0144198
- Sample: daily closes; Dow Jones for the 1929, 1987, 2000, 2008 crashes and across 115 years; S&P 500 and NASDAQ for 1987, 2000, 2008; DAX and FTSE for 2000 and 2008; a 2011-2015 check.
- Method: residuals after Gaussian-kernel detrending (bandwidth 25); lag-1 autocorrelation, variance and low-frequency power on a 500-day rolling window; trend measured by Kendall tau over the 250 days before the crash; tau above 0.9 counts as strong; three surrogate null models with 1,000 draws each.
- Results: lag-1 autocorrelation shows no or weak trend before any crash. Variance and low-frequency power rise strongly before all four Dow crashes, and those trends are unlikely under the nulls. Over the full Dow record 16 events pass the threshold: 5 before the four major crashes, 4 before minor crises, 7 with no crisis nearby. The authors note false alarms seem more frequent recently, and that the signal does not say when a crash will occur. No trading test.
- For our setup: this is the most careful test in the family, and its positive finding is "variance rises before crashes". That is a volatility signal. A 500-day window plus a 250-day trend window needs three years of warm-up; with 9-10 years of data and a base rate of 16 signals in 115 years, we would see one or two signals. It cannot be validated on our sample; a volatility-targeting rule captures the same information faster.

### F3. Diks, Hommes, Wang (2019), "Critical slowing down as an early warning signal for financial crises?" `[opened: full text of the 2015 working-paper version]`
- URL (working paper, opened): https://cendef.uva.nl/binaries/content/assets/subsites/amsterdam-school-of-economics/amsterdam-school-of-economics-research-institute/cendef/working-papers-2015/tipping.pdf ; published in Empirical Economics 57(4), 1201-1228, DOI 10.1007/s00181-018-1527-3 (publisher page not opened).
- Sample: daily S&P 500, NASDAQ, Hang Seng (Datastream, May 1986 to May 2011), TED spread, VIX. Windows of 80 to 500 days before each event; rolling window half the sample; detrending bandwidth 10 (20 as a check).
- Kendall tau for AR(1) / ACF(1) / variance (working-paper Table 2 and figures): 1987 S&P 500: 0.718 / 0.685 / 0.259. 2000 NASDAQ: 0.501 / 0.478 / 0.343. 2008 S&P 500: -0.503 / -0.470 / +0.354. 2008 TED spread: 0.699 / 0.705 / -0.441. 1997 Hang Seng: all three positive, between about 0.33 and 0.46. VIX 2008: 0.463 / 0.446 / -0.149 (variance not significant).
- Conclusion (published abstract): evidence for critical slowing down before Black Monday 1987; mixed or insignificant for the later crises.
- Critique: the analysed window ends at a crash date known in hindsight and is as short as 200 days; signs flip between series for the same crisis (2008). Together with F2, the autocorrelation half of the ecology toolkit does not carry over to markets.

### F4. Farmer (2002), "Market force, ecology and evolution" `[opened: abstract page]`
- URL: https://arxiv.org/abs/adap-org/9812005 (published in Industrial and Corporate Change, 2002, per the task brief; the arXiv page does not list it)
- Claim (model, not data): with a simple price-impact rule, value strategies need not push price to value; trend followers create short-term trends and longer oscillations; reinvested profits make capital dynamics equivalent to a population-biology model; patterns created by trend followers resist being arbitraged away longer than those created by value investors; progress to efficiency takes years to decades.

### F5. Scholl, Calinescu, Farmer (2021), "How market ecology explains market malfunction" `[opened: abstract page]`
- URL: https://arxiv.org/abs/2009.09454 (PNAS 118(26), DOI 10.1073/pnas.2015574118)
- Claim (toy model with value investors, trend followers, noise traders): a strategy's average return depends on how much wealth is invested in it; with realistic noise the market spends long periods away from efficiency.
- For our setup: no testable signal, since we cannot observe wealth by strategy. The practical reading is a prior: a rule's edge is a function of crowding and will drift, so judge rules on rolling out-of-sample windows and expect decay.

### F6. Calvo, Muñoz, Galla (2024), "Navigating uncertainty: risk-averse vs. risk-prone strategies in populations facing demographic and environmental stochasticity" `[opened: full text]`
- URL: https://arxiv.org/abs/2409.16127
- Used here as an opened source for the bet-hedging/Kelly link. The paper states that bet hedging trades arithmetic-mean fitness for geometric-mean fitness because reproduction is multiplicative, and that the Kelly criterion rests on the same idea. Its appendix gives geometric mean ≈ μ - σ²/(2μ) plus a skewness term: with zero or negative skew, cutting variance always raises long-run growth. Its own results are about fixation probability in finite populations (N = 50 and 100) under environmental switching, where the geometric-mean rule can fail.
- Kelly (1956), "A new interpretation of information rate", Bell System Technical Journal `[from memory, unverified; link not verified]`: the original log-growth result.
- For our setup: the transferable content is old and solid. Long-run growth is about mean minus half the variance, so reducing variance at equal mean raises compound return. Negative skew (crypto crashes, equity crashes) strengthens the case. Caveats from the biology literature match the finance ones: the result is asymptotic, and over finite horizons with absorbing states (ruin, or a drawdown that stops the project) more caution than Kelly is justified.

### F7. Eisler, Bartos, Kertész (2008), "Fluctuation scaling in complex systems: Taylor's law and beyond" `[opened: abstract page]`
- URL: https://arxiv.org/abs/0708.2053 (Advances in Physics 57, 89-142)
- Claim: across many systems, including the stock market, the standard deviation of an element's activity scales as a power of its mean activity, exponent usually between 1/2 and 1.
- For our setup: a descriptive law about activity (volume, trade counts), not a return forecast. No use for a six-asset daily strategy beyond a reminder that variability grows with scale.

---

## Verdict for this family

1. Overall: none of the six sub-fields has credible, independent, out-of-sample and after-cost trading evidence at daily frequency for a small multi-asset universe. What survives scrutiny reduces to three plain facts: variance rises before crashes and is persistent; lead-lag and realised variance are low-order statistics; long-run growth is mean minus half the variance.
2. Fractional differentiation: one test with a time-ordered hold-out (A3) and it is weak: a single 3-year window, costs of 0.005%, and the López de Prado-d version beats buy & hold clearly in one of four index tables. No ablation study exists. Worth one cheap test: FFD of log price per asset, d by the ADF rule on the training window only (expect 0.1-0.5), weight threshold 1e-4 (about 280 lags), compared against log returns and price/MA ratios in the same walk-forward model at our costs.
3. Fracdiff trap: it is a linear filter of past returns. If it "works", check that a 100-250 day price/MA ratio does not do the same. Never pick d on the full sample.
4. Signatures: no daily out-of-sample trading evidence. The best evidence is intraday classification with a random split (B2) and synthetic experiments (B4). Worth testing only at level 2: lead-lag signature over 20- and 60-day windows of the six log prices plus time, fed to a ridge model, against a baseline with the same information written plainly (window returns, realised variances and covariances, lagged cross-products).
5. Signature trap: feature count grows as channels to the power of the level (14 lead-lag channels give 196 level-2 terms and 2,744 level-3 terms) against about 2,400 daily observations. Level 3 and above will overfit.
6. TDA: no out-of-sample test. The original paper shows the landscape norm is proportional to variance for noise; the one controlled comparison found (C4, anonymous) reports it adds nothing beyond mean pairwise correlation. If tested: w = 50, six assets, H1, L1 norm, and require it to predict forward 20-day downside variance after controlling for average realised variance and 60-day mean pairwise correlation, with each asset standardised by trailing volatility first. Expect a null.
7. TDA trap: the norm is rolling variance in disguise. The crypto paper's k-means step (k = 18, clusters read in hindsight, price level as an input) is not a rule that can be fixed in advance.
8. Transfer entropy: descriptive only, and the BTC-vs-equities result depends on the estimator. The main trap for us is non-synchronous closes: crypto and ETF bars end at different times and we fill at the next open, so a measured daily lead from ETFs to crypto is largely untradeable. Any lead-lag test must use bars aligned to the US close and returns from next open.
9. Entropy and Hurst: time-varying efficiency is documented; exploitation is not. Bariviera finds BTC return persistence gone after 2014 (500-day DFA window), before our sample starts, while volatility stays strongly persistent. A 500-day window gives about five independent readings in ten years. Low priority; if tried, use it only as a gate on a trend rule and require it to beat the ungated rule out of sample.
10. LPPLS: fitting is now stable (E1) but prediction is unproven. Brée & Joseph find parameters in range for 7 of 11 Hang Seng crashes and reject the mechanism; Wheatley et al. admit hindsight bubble dating and too few bubbles to count false alarms; the Observatory's own experiment document has no scorecard. For BTC and ETH our sample holds perhaps three or four bubble peaks, which cannot validate a signal. If tested: confidence indicator = share of windows of 131-360 days whose fit passes pre-set filters (exponent 0.15-0.51, log-frequency 4.8-7.92), used only to cut crypto weight, and benchmarked against a simple overheating rule (for example price far above its 200-day average).
11. Power-law tails: tail exponent near 3 (not opened, widely reported) means variance estimates are noisy and kurtosis-based statistics are useless. Implication for sizing: use fractional Kelly or volatility targeting with a hard per-asset cap; do not size from a 9-year Sharpe ratio as if it were known.
12. Early-warning signals: the careful tests (F2, F3) reject rising autocorrelation as a market warning and keep rising variance, with 7 false alarms among 16 signals in 115 years of the Dow. The original parameters (500-day window, 250-day trend, tau above 0.9) need three years of warm-up and would fire once or twice in our sample. The usable version is ordinary volatility targeting on 20-60 day realised volatility.
13. Market ecology: models, not signals. Use as a prior that rule performance depends on crowding and decays; evaluate every rule on rolling out-of-sample windows.
14. Bet hedging / Kelly: the equivalence is real and old. It supports diversification across the six assets, holding cash when estimated edge is small, and variance reduction as a source of compound return. It gives no new signal.
15. Taylor's law: no application here.
16. Most worth testing, in order: (a) volatility-targeted, capped, fractional-Kelly sizing on top of whatever signals other survey parts support; (b) the level-2 lead-lag features against their plain-statistics baseline; (c) the fracdiff feature against price/MA ratios; (d) TDA norm and LPPLS indicator only as null-hypothesis checks against rolling variance and a simple overheating rule.
17. General rule for this family: every exotic indicator gets a plain twin (rolling variance, mean pairwise correlation, cross-sectional dispersion, price/MA ratio, 200-day trend filter). Adopt the exotic one only if it adds forecast value after the twin is in the model, on a time-ordered hold-out, at 30 bps crypto and 2 bps ETF costs.
18. Sample-size warning: crash-warning methods here were built on two to four events chosen in hindsight. Our sample has too few crashes to tell a real warning from luck, so de-risking rules should be judged on drawdown and turnover across the whole sample, not on whether they "called" 2020 or 2022.
