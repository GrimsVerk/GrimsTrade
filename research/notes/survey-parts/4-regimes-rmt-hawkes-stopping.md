# Part 4: Regime models, random matrix theory, Hawkes processes, optimal stopping

Survey date: 2026-11-12. Scope: what the literature says for a long-only, unlevered, daily-bar
book in BTC, ETH, SPY, QQQ, GLD, TLT with next-open fills and costs of about 60 bps per crypto
round trip and about 4 bps per ETF round trip.

How to read the entries:

- `[opened: full text]` means I read the paper itself (PDF or HTML text).
- `[opened: abstract page]` means I read only the abstract or landing page; numbers are limited to what that page shows.
- `[opened: secondary summary]` means I read a third-party summary, not the paper.
- `[not opened]` means the entry rests on a search snippet or on another paper's description; treat as unverified.
- `[from memory, unverified]` marks anything I state from prior knowledge without having read it in this session.
- "Implication" lines are my inference for this setup, not claims made by the authors.

---

## A. Regime switching, hidden Markov models and jump models for allocation

### A1. Shu, Yu & Mulvey, "Downside risk reduction using regime-switching signals: a statistical jump model approach" `[opened: full text]`
Shu, Y., Yu, C., Mulvey, J. M. (2024). Journal of Asset Management 25(5), 493-507. DOI 10.1057/s41260-024-00376-x. arXiv 2402.05272 (v3, Sept 2024).
URL: https://arxiv.org/html/2402.05272v3

- Sample: daily total returns of the S&P 500, DAX and Nikkei 225, 1970-2023; each index tested on its own (index or cash, a 0/1 strategy). Out-of-sample test 1990-2023.
- Method: two-state statistical jump model (JM) on three exponentially smoothed features (downside deviation with 10-day halflife; Sortino ratio with 20-day and 60-day halflives), refit every six months on a 3,000-day window. Benchmark: two-state Gaussian HMM on returns, refit daily, Viterbi path smoothed by a rolling mean. The JM jump penalty (and the HMM smoothing window) is re-selected monthly by maximising validation-period Sharpe on a rolling 12-year train / 8-year validation scheme.
- Costs and delay: 10 bps one way; signal from day t applied on day t+2 (one-day delay). Robustness with 5- and 10-day delays.
- Out-of-sample 1990-2023 (Table 4): S&P 500 buy-and-hold CAGR 10.2%, vol 18.2%, Sharpe 0.48, max drawdown -55.2%; HMM 8.5% / 11.3% / 0.54 / -28.9%; JM 11.2% / 13.1% / 0.68 / -26.6%. DAX: B&H Sharpe 0.30, HMM 0.35, JM 0.44. Nikkei: B&H 0.12, HMM 0.19, JM 0.31. Returns include the risk-free rate earned in cash.
- No moving-average or plain volatility-filter benchmark. The authors say the signals lag by about half a month at crash onsets and ends, and that the JM "did not necessarily improve strategy returns" in the 2020 rebound. Performance falls with longer delays.
- Caveat (my reading): the hyperparameter is chosen by in-sample Sharpe each month, which is legitimate walk-forward but still a tuning loop; and cash earned T-bill rates that were high in the 1990s.
- Implication (my inference): the best recent evidence that a regime filter cuts drawdown roughly in half on equity indexes after costs and a one-day delay. The Sharpe gain over buy-and-hold is real in their table, but the paper never tests whether a 10-month moving average or a volatility-target rule does as well, which is the question that matters for us. The features (smoothed downside deviation and Sortino) are themselves close to trend-plus-volatility filters.

### A2. Bulla, Mergner, Bulla, Sesboue & Chesneau, "Markov-switching asset allocation: do profitable strategies exist?" `[opened: full text]`
Bulla, J., Mergner, S., Bulla, I., Sesboue, A., Chesneau, C. (2011). Journal of Asset Management 12(5), 310-321. DOI 10.1057/jam.2010.27. Working paper MPRA 21154 (2010).
URL: https://mpra.ub.uni-muenchen.de/21154/1/MPRA_paper_21154.pdf

- Sample: daily returns of DAX, DJIA, S&P 500 (from January 1976), NASDAQ 100 (from October 1985), Nikkei 225 (from January 1983), to about 2009. Two assets: the index or a risk-free asset fixed at 3% a year.
- Method: two-state Gaussian HMM on daily returns, rolling 2,000-day window, Viterbi path, one-step-ahead state prediction, then a median filter over 6 days (k = 6) to cut switching. The filter cut switches by about 50-65% (S&P 500: 134 to 46 over 5,834 forecast days).
- Costs: 10 bps one way. Out-of-sample (Table 5): S&P 500 index mean 8.37%, SD 16.5%, Sharpe 0.390; strategy 8.56%, 10.3%, 0.577. DJIA 0.417 to 0.646. NASDAQ 0.272 to 0.464 (SD 32.0% to 14.0%). DAX 0.292 to 0.437. Nikkei index -4.30%, strategy -2.28%. Abstract: volatility down 41% on average; excess return 18.5 bp (S&P 500) to 201.6 bp (Nikkei) a year.
- In-sample results were far stronger (S&P 500 Sharpe 0.91 to 0.95); the out-of-sample edge is mostly volatility reduction, the return edge is small.
- The paper itself reviews earlier failures: Bauer et al. (2004) found much of the excess return disappears after costs; Hess (2006) found regime forecasts had no advantage after costs; Dacco and Satchell (1999) showed a few wrong regime calls erase the advantage (all cited by Bulla et al., not opened by me).
- Caveat: the 3% fixed cash rate flatters the strategy when real cash yielded less; no moving-average benchmark; the median filter length was chosen by the authors ("produces good results for all indices").
- Implication (my inference): on US large-cap indexes, an HMM risk-off switch gave almost the same return as buy-and-hold with about 40% less volatility. That is a risk tool, not an alpha source. For SPY/QQQ at 4 bps a round trip, costs are not the binding constraint; the comparison with a simple trend or volatility filter is.

### A3. Nystrup, Hansson, Madsen & Lindstrom, "Regime-based versus static asset allocation: letting the data speak" `[opened: abstract page]`
Nystrup, P., Hansson, B. W., Madsen, H., Lindstrom, E. (2015). Journal of Portfolio Management 42(1), 103-109. DOI 10.3905/jpm.2015.42.1.103.
URL: https://lup.lub.lu.se/record/8165472

- Sample: a global stock index and a global government bond index (dates not on the page).
- Claim (abstract): a regime-switching model with time-varying parameters; "a static portfolio may not be optimal even when the investor has no forecasting skill."
- The full text (Paper C of Nystrup's 2018 DTU PhD thesis, https://orbit.dtu.dk/files/152802375/phd465_Nystrup_P.pdf) returned HTTP 403 to my fetches, so I could not check numbers, costs or the out-of-sample design. The thesis abstract says two regimes in stock returns are enough to "profitably adjust allocations" in single- and multi-asset settings and that regime-based allocation adds value versus rebalancing to a static benchmark.
- Related, not opened: Nystrup, Hansen, Larsen, Madsen, Lindstrom (2017/2018), "Dynamic allocation or diversification: a regime-based approach to multiple assets", Journal of Portfolio Management; per search snippet, regime-based allocation "is profitable, even when compared to a diversified benchmark portfolio." Numbers unverified.
- Implication (my inference): this group's work is the most relevant to a stock/bond/gold mix, but I could not verify its numbers. It supports a two-state equity regime driving a shift between SPY/QQQ and TLT/GLD rather than to cash.

### A4. Shu, Yu & Mulvey, "Dynamic asset allocation with asset-specific regime forecasts" `[opened: full text, first ~100k characters of HTML]`
Shu, Y., Yu, C., Mulvey, J. M. (2025). Annals of Operations Research 346(1), 285-318. arXiv 2406.09578 (June 2024).
URL: https://arxiv.org/html/2406.09578v1

- Sample: 12 daily total-return indexes (US large, mid, small cap; EAFE; EM; aggregate bonds; Treasuries; high yield; corporates; REITs; commodities; gold), 1991-2023. Out-of-sample test 2007-2023. Refit every six months on an 11-year lookback; jump penalty re-tuned on a rolling five-year validation window.
- Method: a statistical jump model labels each asset's bull/bear regimes, a gradient-boosted tree classifier (XGBoost) forecasts them, and the forecasts feed expected returns into minimum-variance, mean-variance and equal-weight portfolios. Costs 5 bps one way. Trading delay not stated in the part I read.
- Results 2007-2023 (Table 6, excess of a 1.1% risk-free rate): 60/40 Sharpe 0.57, max drawdown -31.5%. Equal weight 1/12: Sharpe 0.51, MDD -37.5%, turnover 0.81; equal weight with regime forecasts: Sharpe 0.91, MDD -17.6%, turnover 11.70. Min-variance 0.70 to 1.12 (MDD -19.3% to -7.1%). Mean-variance 0.37 to 1.02 (turnover 3.40 to 9.12).
- No trend or moving-average benchmark. The authors say forecasts "are not perfect" and cite late bearish calls (2015-2016 large-cap selloff).
- Caveat (my reading): turnover rises by an order of magnitude (0.81 to 11.70 for equal weight). At 5 bps one way that is cheap; at our 30 bps one way on crypto it would cost about 7% a year if applied to crypto at that turnover. One test window (2007-2023) starting just before the GFC, which is the most favourable possible start for a risk-off signal. Many design choices (features, classifier, penalty grid) in a paper from the same group that proposed the method.
- Implication (my inference): the strongest claim in this family for a multi-asset book, and the asset mix (equities, Treasuries, gold) overlaps ours. But it is a single-author-group result, not independently replicated, starting in 2007, and with no trend-filter control. Worth a replication on SPY/QQQ/TLT/GLD only with a per-asset 10-month moving average as the control.

### A5. Hidden Markov models for Bitcoin: Koki, Leonardos & Piliouras, "A peek into the unobservable: hidden states and Bayesian inference for the Bitcoin and Ether price series" `[opened: abstract page]`
Koki, C., Leonardos, S., Piliouras, G. (2019, revised 2021). arXiv 1909.10957. (A related version by the same authors on Bitcoin, Ether and Ripple appeared in Research in International Business and Finance, per search snippet; not opened.)
URL: https://arxiv.org/abs/1909.10957

- Sample: Bitcoin and Ether prices with blockchain covariates (dates not on the abstract page).
- Claim: a non-homogeneous HMM finds two alternating Bitcoin states (described as fundamental-trader and noise-trader driven) with different autocorrelation and drivers; a search snippet for the related paper says a four-state NHHM gave the best one-step-ahead forecasts among competing models.
- No trading strategy, no costs, no economic out-of-sample test on the abstract page.
- My search for a costed, out-of-sample HMM trading backtest on Bitcoin found only statistical forecasting papers and unreviewed preprints. I found nothing rigorous.
- Implication (my inference): there is no credible evidence that an HMM risk switch adds value on BTC/ETH after 60 bps round trips. Any test here is new ground and must beat a plain trend filter on BTC, which is the known baseline.

### A6. Background models `[from memory, unverified]`
- Hamilton (1989, Econometrica), "A new approach to the economic analysis of nonstationary time series and the business cycle": the two-state Markov-switching model, applied to US GNP growth. Not a trading paper.
- Ang & Bekaert (2002, Review of Financial Studies; 2004, Financial Analysts Journal): regime-switching international equity allocation; their 2004 result is that the value comes mainly from switching to cash or bonds in the high-volatility, low-return regime. Bulla et al. (A2) quote both papers to this effect, and note Ang and Bekaert left out transaction costs.
- Guidolin & Timmermann (2007, Journal of Economic Dynamics and Control), "Asset allocation under multivariate regime switching": four regimes (crash, slow growth, bull, recovery) in US stocks and bonds, monthly; they report out-of-sample gains for a regime-aware investor. I did not open it and cannot quote numbers.
- Nystrup, Madsen, Lindstrom (2018, Journal of Forecasting?), "Greedy online classification of persistent market states" (with Kolm?): online jump-model classification. Authorship and venue not verified; not opened.

---

## B. Change-point detection in trading

### B1. Wood, Roberts & Zohren, "Slow momentum with fast reversion: a trading strategy using deep learning and changepoint detection" `[opened: full text]`
Wood, K., Roberts, S., Zohren, S. (2022). Journal of Financial Data Science, Winter 2022. arXiv 2105.13727 (v3, Dec 2021).
URL: https://arxiv.org/abs/2105.13727 (PDF https://arxiv.org/pdf/2105.13727v3)

- Sample: 50 liquid continuous futures (commodities, equities, fixed income, FX), Pinnacle CLC data, 1990-2020, daily. Expanding-window walk-forward: train/validate on 1990-1995, test 1995-2000, then expand by five years, re-tune and test the next five years. Results averaged over test windows 1995-2020.
- Method: a Gaussian-process online changepoint detector (lookback 10 to 252 days) feeds a changepoint location and severity score into an LSTM "Deep Momentum Network" that sizes long/short positions with a Sharpe-ratio loss. Long-short, volatility-scaled.
- Claim (Exhibit 3, raw signal, before costs): Long Only Sharpe 0.44; MACD 0.77; TSMOM 0.94; LSTM without CPD 1.62; LSTM with CPD 2.04 (21-day lookback), 2.08 (63-day), 2.16 (lookback re-tuned). "The addition of the CPD module leads to an improvement in Sharpe ratio of one-third"; in 2015-2020 the average improvement is 70% for the 21-day lookback.
- Costs (Appendix C): the main results ignore costs. With costs added, "Our strategy outperforms classical strategies for transaction costs of up to 2 basis points, at which point it rapidly deteriorates, due to the fast reverting component." Longer CPD windows become better as costs rise.
- Implication (my inference): the headline Sharpe is pre-cost and long-short on 50 futures. The authors' own cost test kills the advantage over classical trend above about 2 bps per trade. Our crypto costs are about 15 times that. The CPD gain comes from fast reversion trades, exactly what our costs and next-open fills punish. Not usable here; the only salvageable idea is a slow (63-252 day) changepoint flag as a trend-exit signal, which is close to a moving-average rule anyway.

### B2. Adams & MacKay, "Bayesian online changepoint detection" `[opened: abstract page]`
Adams, R. P., MacKay, D. J. C. (2007). arXiv 0710.3742 (technical report, University of Cambridge).
URL: https://arxiv.org/abs/0710.3742

- Method: exact online inference of the "run length" (time since the last changepoint) by message passing, assuming parameters before and after a change are independent. It needs a hazard rate (prior expected regime length) and a conjugate model for each segment.
- No trading test on the abstract page. `[from memory, unverified]`: one of the paper's demonstration datasets is daily Dow Jones returns, segmented by volatility; this is a descriptive fit, not a strategy.
- Implication (my inference): BOCPD is a building block, not a strategy. For a daily long-only book it would amount to a volatility-regime detector with two free choices (hazard rate and prior), and it has no published costed out-of-sample record that I found. Its natural use here is as a de-risking trigger, tested against a plain rolling-volatility threshold.

### B3. Simpler change-point rules `[not opened]`
- I did not find a costed out-of-sample study of CUSUM or Page-Hinkley style detectors as stand-alone daily trading rules on indexes or BTC within my source budget. The classical CUSUM is closely related to a drawdown-from-peak rule (both trigger when cumulative evidence against the current regime exceeds a threshold), so the stop-loss literature in section E is the nearest evidence. That link is my inference.

---

## C. Random matrix theory, correlation cleaning, and market-mode indicators

### C1. Bun, Bouchaud & Potters, "Cleaning large correlation matrices: tools from random matrix theory" `[opened: abstract page]`
Bun, J., Bouchaud, J.-P., Potters, M. (2017). Physics Reports 666, 1-109. DOI 10.1016/j.physrep.2016.10.005. arXiv 1610.08104.
URL: https://arxiv.org/abs/1610.08104

- Content (abstract): a review of RMT tools (Marchenko-Pastur equation, free probability, eigenvector statistics) leading to "rotationally invariant estimators" (RIE) for large correlation matrices with no prior structure; the authors report RIE beats earlier methods in financial applications. The abstract page does not state the N/T regime or the test design.
- Background `[from memory, unverified]`: Laloux, Cizeau, Bouchaud, Potters (1999, Physical Review Letters) and Plerou et al. (2002, Physical Review E) found that for several hundred US stocks with a few years of daily data, most eigenvalues of the sample correlation matrix fall inside the Marchenko-Pastur noise band, with only a market mode and a few sector modes standing out. Ledoit and Wolf's nonlinear shrinkage (2012 onward, Annals of Statistics) targets the same large-N problem.
- Arithmetic for our case (my own calculation, not from the sources): the Marchenko-Pastur noise band for a pure-noise correlation matrix runs from (1 - sqrt(q))^2 to (1 + sqrt(q))^2 with q = N/T. With N = 6 and T = 252 daily bars, q = 0.024, so the band is about 0.72 to 1.33. With T = 60, q = 0.1 and the band is about 0.47 to 1.73. The asymptotic theory assumes both N and T large; at N = 6 it is at best a rough guide.
- Implication (my inference): RMT cleaning is decoration for a 6-asset book. Estimation noise in a 6x6 correlation matrix with a year of daily data is small next to the non-stationarity of the true correlations (stock-bond correlation flipped sign around 2000 and again around 2022). Simple shrinkage toward a constant correlation, or no optimisation at all (equal weight or inverse volatility), is the practical answer. The real risk for us is regime change in correlations, not finite-sample noise.

### C2. Kritzman, Li, Page & Rigobon, "Principal components as a measure of systemic risk" `[opened: secondary summary]` and `[from memory, unverified]` for details
Kritzman, M., Li, Y., Page, S., Rigobon, R. (2011). Journal of Portfolio Management 37(4), 112-126. SSRN 1633027 (SSRN returned 403; the scispace PDF copy came back empty).
Secondary summary read: Portfolio Optimizer blog, "The absorption ratio: measuring financial risk, part 2". URL: https://portfoliooptimizer.io/blog/the-absorption-ratio-measuring-financial-risk/

- Definition: the absorption ratio (AR) is the share of total variance explained by a fixed number of principal components of a set of asset returns. A high AR means markets are tightly coupled and shocks spread widely.
- Original claims `[from memory, unverified]`: the authors used US industry returns with a rolling window and roughly one fifth of the eigenvectors, reported that most major US drawdowns were preceded by AR spikes, and showed a stock/bond switching rule based on a standardised AR shift beating a static mix. I could not open the paper to verify numbers, costs or out-of-sample design.
- Secondary replication (Portfolio Optimizer blog): nine Sector SPDR ETFs, weekly, October 2000 to March 2022, 52-week covariance, one eigenvector. The AR spikes during crashes and stays high, but tends to fall rather than rise before crashes, contradicting the early-warning claim. A rule scaling SPY versus cash by how elevated the AR is gave Sharpe about 0.85 versus about 0.54 for buy-and-hold, with roughly 50% average exposure and max weekly drawdown about 15% versus 55%. The scaling method is not disclosed, there are no costs, and it is a single in-sample backtest. The author notes the strategy "struggles when the absorption ratio is choppy, like around 2005 and 2015."
- Related `[from memory, unverified]`: Kritzman and Li (2010, Financial Analysts Journal), "Skulls, financial turbulence, and risk management", define turbulence as the Mahalanobis distance of today's return vector from its historical mean and covariance; turbulent periods are persistent and have worse returns. I did not open it and found no independent costed out-of-sample test within my budget.
- Implication (my inference): with 6 assets of different classes, the first principal component is not a "market mode" in the RMT sense; it mixes equity beta and crypto beta, and the AR would mostly track whether BTC/ETH and SPY/QQQ are moving together. The replication suggests the AR is a coincident volatility-and-correlation gauge, not a leading indicator. It may add little beyond realised volatility. A Mahalanobis turbulence score on our 6 assets is cheap to compute and worth one test as a de-risking trigger, but the prior should be that it duplicates a volatility filter.

