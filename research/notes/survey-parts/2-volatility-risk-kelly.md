# Part 2: Volatility timing, risk-based allocation, Kelly sizing

Survey date: 2026-11-12. Scope: what the literature says for a long-only, unlevered (weights sum to at
most 1, rest in cash at 0%), daily-bar book in BTC, ETH, SPY, QQQ, GLD, TLT with next-open fills and
costs of about 60 bps per crypto round trip and about 4 bps per ETF round trip.

How to read the entries:

- `[opened: full text]` means I read the paper itself (PDF text), at least the parts cited.
- `[opened: abstract page]` means I read only the abstract or landing page; numbers are limited to what that page shows.
- `[opened: secondary summary]` means I read a third-party summary, not the paper.
- `[not opened]` means the entry rests on a search snippet or on another paper's description; treat as unverified.
- `[from memory, unverified]` marks anything I state from prior knowledge without opening a source in this session.
- "Implication" lines are my inference for this setup, not claims made by the authors.

---

## A. Volatility-managed portfolios and volatility targeting

### A1. Moreira & Muir, "Volatility-Managed Portfolios" `[opened: abstract page]`
Moreira, A., Muir, T. (2017). Journal of Finance 72(4), 1611-1644. NBER Working Paper 22208 (2016).
URL: https://www.nber.org/papers/w22208

- Sample (per abstract): equity factors (market, value, momentum, profitability, return on equity, investment) and the currency carry trade. The abstract page gives no dates or numbers.
- Claim: portfolios that take less risk when recent volatility is high "produce large alphas, increase factor Sharpe ratios, and produce large utility gains for mean-variance investors". Mechanism: changes in volatility are not offset by proportional changes in expected returns. The strategy takes less risk in recessions and crises yet still earns high average returns.
- Design `[from memory, unverified]`: weight = c / (last month's realized variance from daily returns), rebalanced monthly; the scaled portfolio is levered well above 1 in calm periods. The paper reportedly has a robustness check with a leverage cap; I did not verify its numbers.
- Costs and out-of-sample: the abstract says nothing on costs. The headline alpha is from a full-sample spanning regression, which Cederburg et al. (A2) show is not a tradable out-of-sample strategy.
- Implication (my inference): the original result relies on levering up in calm periods. Our cap at 100% removes that half, so the paper by itself does not tell us whether de-risking alone pays.

### A2. Cederburg, O'Doherty, Wang & Yan, "On the performance of volatility-managed portfolios" `[opened: full text]`
Cederburg, S., O'Doherty, M. S., Wang, F., Yan, X. (2020). Journal of Financial Economics 138(1), 95-117. DOI 10.1016/j.jfineco.2020.04.015.
URL: https://www.lehigh.edu/~xuy219/research/COWY.pdf

- Sample: 103 US equity strategies (the nine Moreira-Muir factors plus 94 anomaly portfolios), monthly, market factor from 1926.
- Direct comparison: "In the more comprehensive sample of 103 equity portfolios, the volatility-managed versions outperform in 53 cases, whereas the original versions outperform in 50 cases." Only eight show significant Sharpe gains from volatility management, "concentrated among momentum-related strategies".
- Spanning-regression alphas are real in-sample (market factor alpha 4.63% a year), but the implied combination strategy cannot be built in real time. Out of sample, the market combination strategy underperforms the plain market: Sharpe 0.42 versus 0.46, certainty equivalent 1.56% versus 1.75% a year. The in-sample gain for the scaled market "is concentrated in the period surrounding the Great Depression".
- Leverage: base case caps total absolute weight at 5. They also test caps of 1.0 and 1.5 and no cap; "the performance of the combination strategies does not systematically improve for these cases". In all specifications more than half of the Sharpe and CER differences are negative.
- Cause: "structural instability in the underlying spanning regressions". No transaction costs are needed to reach the negative verdict.
- Implication (my inference): for the plain market portfolio, monthly inverse-variance scaling is not a reliable improvement out of sample, and a leverage cap of 1 does not rescue it. Any gain we find on SPY/QQQ should be treated as likely noise unless it is large and stable across subperiods.

### A3. Harvey, Hoyle, Korgaonkar, Rattray, Sargaison & Van Hemert, "The Impact of Volatility Targeting" `[opened: full text]`
Harvey, C. R., Hoyle, E., Korgaonkar, R., Rattray, S., Sargaison, M., Van Hemert, O. (2018). Journal of Portfolio Management, Fall 2018 (Man Group / Duke).
URL: https://people.duke.edu/~charvey/Research/Published_Papers/P135_The_impact_of.pdf

- Sample: more than 60 assets with daily data, US equities from 1927 (Equities All U.S. 1927-2017), US bonds from 1963, 50 futures and forwards plus credit 1988-2017, 60-40 and risk parity portfolios 1988-2017.
- Method: target 10% annualized volatility using exponentially weighted realized volatility (half-lives tested from 10 to 90 days; 20 days is the default in figures), computed from squared returns with zero mean. Exposure is not capped: it scales up in calm periods. Costs: 1.0 bp per unit of notional traded for equities, 0.5 bp bonds and credit, 1.0 bp gold.
- Claims with numbers: US equities Sharpe "improves from 0.40 (unscaled) to between 0.48 and 0.51 (volatility scaled)", not sensitive to the estimator; regression intercept 0.64 bp per day, t = 3.05. Gross and net Sharpe are equal at two decimals (0.4831 versus 0.4766 for the 10-day half-life). For "bonds, currencies, and commodities, volatility scaling has a negligible effect on realized Sharpe ratios". For US bonds 1963-2017, scaling lowered the Sharpe because the 1960-1980 bond bear market had low volatility.
- Tails: volatility targeting "consistently reduces the likelihood of extreme returns (and the volatility of volatility)" across all assets, and reduces maximum drawdowns for 60-40 and risk parity portfolios. It cuts both tails.
- Mechanism: the leverage effect (volatility rises when prices fall) in equities and credit makes volatility scaling act like a partial time-series momentum overlay.
- Out-of-sample: volatility estimates are causal (ex ante), so the scaled series is tradable; there is no fitted parameter beyond the half-life. But full-sample target scaling is used for display.
- Implication (my inference): the robust, cheap benefit is tail and drawdown control, not Sharpe. Sharpe gains exist only for risk assets (SPY, QQQ, and probably BTC/ETH, which show a leverage effect at times) and none are expected for TLT or GLD. With a cap of 1, we keep the de-risking half; whether the Sharpe gain survives without the lever-up half is not shown here and must be tested.

### A4. Liu, Tang & Zhou, "Volatility-Managed Portfolio: Does It Really Work?" `[opened: abstract page]`
Liu, F., Tang, X., Zhou, G. (2019). Journal of Portfolio Management 46(1), 38-51.
URL: https://profiles.wustl.edu/en/publications/volatility-managed-portfolio-does-it-really-work/

- Claim (abstract, paraphrased by the fetch tool): the usual application of volatility timing to the stock market has look-ahead bias. A search snippet from another version says Moreira and Muir "calibrated the weight parameter based on the unconditional volatility over the entire sample period" `[not opened: snippet only]`.
- After the bias is corrected (fixed-window and rolling-window estimation, per snippet), the strategy is "very difficult to implement" because maximum drawdowns are about 68% to 93% in almost all cases. It beats the market only during the financial crisis. Three alternative volatility-timing rules also fail to beat the market.
- No cost figures on the page.
- Implication (my inference): the 68-93% drawdowns come from levering up in calm markets right before crashes. A long-only cap of 1 removes that failure mode by construction, but it also removes most of the claimed upside. The look-ahead point matters for us: any target volatility must be set from past data only, or replaced by a parameter-free rule (for example, inverse-volatility weights across assets, which need no target).

### A5. Barroso & Detzel, "Do limits to arbitrage explain the benefits of volatility-managed portfolios?" `[opened: abstract page]`
Barroso, P., Detzel, A. (2021). Journal of Financial Economics 140(3), 744-767. DOI 10.1016/j.jfineco.2021.02.009.
URL: https://econpapers.repec.org/RePEc:eee:jfinec:v:140:y:2021:i:3:p:744-767

- Claim: "after transaction costs, volatility management of asset-pricing factors besides the market return generally produces zero abnormal returns and significantly reduces Sharpe ratios", even with six cost-mitigation strategies.
- Exception: "abnormal returns of the volatility-managed market portfolio are robust to transaction costs", concentrated in easily arbitraged stocks. But "the managed market strategy only provides superior performance when sentiment is high".
- Sample dates and numbers not on the abstract page.
- Implication (my inference): costs kill volatility management for high-turnover long-short factors, not for a cheap index. For SPY/QQQ at 4 bps a round trip, cost is not the binding problem; instability (A2, A4) is. For BTC/ETH at 60 bps, frequent exposure changes from daily volatility estimates could cost real money, so changes should be banded or done weekly.

---

## B. Risk parity and naive diversification

### B1. Asness, Frazzini & Pedersen, "Leverage Aversion and Risk Parity" `[opened: full text]`
Asness, C. S., Frazzini, A., Pedersen, L. H. (2012). Financial Analysts Journal 68(1), 47-59.
URL: https://www.aqr.com/-/media/AQR/Documents/Insights/Journal-Article/Leverage-Aversion-and-Risk-Parity.pdf

- Samples: "long sample" US stocks and bonds 1926-2010; "broad sample" global stocks, US bonds, credit, commodities 1973-2010; "global sample" stocks and bonds in 11 countries 1986-2010. Monthly.
- Method: each month, weight of each asset class = inverse of its volatility from three years of monthly excess returns up to t-1; then scaled by a constant to match the ex post volatility of the value-weighted market (that constant is a full-sample, look-ahead choice for the levered version).
- Numbers, long sample (Table 2): stocks Sharpe 0.35, bonds 0.47, value-weighted portfolio 0.25, 60/40 0.40, unlevered RP 0.52 (excess return 2.20% a year at 4.25% volatility), levered RP 0.53 (7.99% at 15.08% volatility). RP alpha t-statistic 4.30.
- Direct statement on unlevered investors: "the value-weighted market portfolio and the 60/40 portfolio have earned higher average returns than the unlevered RP portfolio. Therefore, an investor who cannot or will not use leverage may rationally prefer to hold the market portfolio, the 60/40 portfolio, or even all stocks despite all these portfolios having lower Sharpe ratios than RP."
- Costs: levered RP returns do not include financing spreads or deleveraging costs (authors say so). The authors argue 1926-2010 was not biased toward bonds (yields round-tripped). Later evidence: see B4 on 2022.
- Implication (my inference): risk parity's edge is a higher Sharpe ratio that only becomes a higher return with leverage. Unlevered and with cash at 0%, inverse-volatility weighting across our six assets will be dominated by TLT and GLD and will have low absolute return. Its value for us is lower drawdown, not higher growth. With BTC/ETH at four to five times the volatility of SPY, inverse-volatility gives crypto tiny weights.

### B2. DeMiguel, Garlappi & Uppal, "Optimal Versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy?" `[opened: abstract page]`
DeMiguel, V., Garlappi, L., Uppal, R. (2009). Review of Financial Studies 22(5), 1915-1953.
URL: https://ideas.repec.org/a/oup/rfinst/v22y2009i5p1915-1953.html

- Sample: 14 mean-variance models (including shrinkage and constrained versions) on seven empirical datasets.
- Claim: none is consistently better than 1/N on Sharpe ratio, certainty-equivalent return, or turnover. Calibrated to US equities, the estimation window needed for sample-based mean-variance to beat 1/N is about 3,000 months for 25 assets and about 6,000 months for 50 assets.
- Out-of-sample: rolling-window, out-of-sample by design. Turnover is reported, which is the cost proxy.
- Later replications `[from memory, unverified]`: Kritzman, Page and Turkington (2010) argued that optimization with long-run (not rolling sample) expected returns beats 1/N; Kirby and Ostdiek (2012) showed that volatility-timing rules (weights proportional to inverse variance, no means) can beat 1/N after costs. I did not open either.
- Implication (my inference): with six assets and a few years of crypto data, any rule that uses estimated expected returns will be swamped by noise. Use rules that need only volatilities (or nothing): 1/N, inverse-volatility, or fixed weights. 1/N across our six assets puts one third in crypto, which is a much riskier portfolio than 1/N across equity sectors; "naive" here means "crypto-heavy".

### B3. Maillard, Roncalli & Teiletche, "The Properties of Equally Weighted Risk Contribution Portfolios" `[not opened]`
Maillard, S., Roncalli, T., Teiletche, J. (2010). Journal of Portfolio Management 36(4), 60-70 (pages per a Springer reference list; another listing says 60-71).
URL: no page opened (EconBiz record returned an access-denied page).

- Claim, from secondary descriptions in search results only: the equal-risk-contribution (ERC) portfolio sets each asset's contribution to portfolio variance equal; it sits between 1/N and minimum variance, with volatility ordered minimum variance < ERC < 1/N.
- `[from memory, unverified]`: when all pairwise correlations are equal, ERC reduces to inverse-volatility weights. That is the case that makes inverse volatility a cheap stand-in for full ERC.
- Implication (my inference): with six assets, ERC versus inverse-volatility differs mainly through the BTC-ETH correlation (high) and the SPY-QQQ correlation (high). ERC would treat each pair as close to one risk unit and give each member less than inverse-volatility does. Both are parameter-light and testable; the difference is worth a single comparison, not a search.

### B4. Western Asset, "When Diversification Fails, and Recovers" `[opened: practitioner article]`
Western Asset Management blog, 2022-11-29.
URL: https://www.westernasset.com/us/en/research/blog/when-diversification-fails-and-recovers-2022-11-29.cfm

- Claim: in 2022 bonds fell nearly as much as stocks. A 60/40 of S&P 500 and the Bloomberg US Aggregate was down close to 20% year to date, "on course to be the deepest annual drawdown for this portfolio since 2008". Simultaneous 12-month declines in stocks and bonds happened in only four quarters since 1973 (2%).
- Cause given: high and persistent inflation plus aggressive central-bank tightening (1994 cited as the other such regime).
- Other 2022 reports seen only in search snippets `[not opened]`: the RPAR Risk Parity ETF fell more than 32% from its November 2021 high (Bloomberg via BNN); AQR's multi-asset fund returned -10.5% in 2022 (CAIA). An unverified site claimed about -22% for Bridgewater All Weather; I could not confirm it.
- Implication (my inference): risk parity assumes the bond leg hedges the equity leg. In an inflation shock that fails, and levered risk parity suffers most. Unlevered, our risk-parity book would have lost less than levered funds, but TLT (long duration, about -30% in 2022 `[from memory, unverified]`) would have been its largest weight among the ETFs. Any risk-parity test must include 2022 and report it separately; a backtest that starts in 2010 and ends in 2021 is the bond bull market only.

---

## C. Covariance estimation and minimum variance for small portfolios

### C1. Lopez de Prado, "Building Diversified Portfolios that Outperform Out-of-Sample" `[opened: full text]`
Lopez de Prado, M. (2016). Journal of Portfolio Management 42(4), 59-69. DOI 10.3905/jpm.2016.42.4.059. SSRN 2708678.
URL: https://papers.ssrn.com/abstract=2708678 (PDF read from a mirror: https://www.smallake.kr/wp-content/uploads/2020/04/SSRN-id2708678.pdf)

- Method: hierarchical risk parity (HRP): cluster assets by correlation distance, reorder the covariance matrix, then split weight top-down by inverse variance within clusters. No matrix inversion.
- Evidence is a Monte Carlo, not real data: 10 simulated Gaussian series with added random shocks and random correlation, 520 daily observations, 260-day lookback, monthly rebalance, 10,000 repetitions, long-only (0 <= w <= 1).
- Numbers: out-of-sample variance CLA (minimum variance) 0.1157, IVP (inverse variance) 0.0928, HRP 0.0671. CLA has "72.47% greater variance than HRP's"; IVP 38.24% greater. Mean returns are zero by construction, so this is a risk comparison only.
- Later checks `[not opened: search snippet]`: a 2016 Quantopian walk-forward test on 20 ETFs reportedly found HRP below inverse-variance on return and below minimum variance on volatility. I did not read it.
- Implication (my inference): HRP's advantage comes from many assets with cluster structure. With six assets the "tree" is close to trivial (crypto pair, equity pair, GLD, TLT), so HRP will look like a cluster-aware inverse-variance rule. Worth one test against plain inverse-variance; the simulation is not evidence that it adds return.

### C2. Jagannathan & Ma, "Risk Reduction in Large Portfolios: Why Imposing the Wrong Constraints Helps" `[opened: abstract page]`
Jagannathan, R., Ma, T. (2003). Journal of Finance 58(4), 1651-1684. NBER Working Paper 8922 (2002).
URL: https://www.nber.org/papers/w8922

- Claim: a no-short-sale constraint is equivalent to shrinking the large elements of the sample covariance matrix, which reduces estimated portfolio risk even when the true optimum has short positions.
- With the long-only constraint, minimum-variance portfolios from the monthly sample covariance matrix perform about as well as those from factor models, shrinkage estimators, or daily data. Daily data helps when minimizing tracking error.
- Sample details are not on the abstract page.
- Implication (my inference): our long-only constraint already does much of the work of a shrinkage estimator. Fancy covariance estimation is low priority for six assets; a plain rolling sample covariance with weights floored at zero is a fair baseline.

### C3. Ledoit & Wolf, "Honey, I Shrunk the Sample Covariance Matrix" `[not opened]`
Ledoit, O., Wolf, M. (2004). Journal of Portfolio Management 30(4), 110-119. DOI 10.3905/jpm.2004.110. Working paper: UPF Economics WP 691 (2003).
URL: https://econ-papers.upf.edu/en/onepaper.php?id=691 (listed in search; not opened. The author's own PDF failed with a certificate error.)

- Claim, from the search-result rendering of the abstract only: shrink the sample covariance toward a structured target with an optimal shrinkage intensity; on real stock data this lowered tracking error and raised the realized information ratio of an active manager.
- `[from memory, unverified]`: the paper's setting is hundreds of stocks with a few years of monthly data, where the sample matrix is close to singular. Clarke, de Silva and Thorley (2006, JPM, "Minimum-Variance Portfolios in the U.S. Equity Market") reported that long-only minimum variance on large US stocks had lower volatility than the market with similar or higher return over 1968-2005. Not opened.
- Implication (my inference): with six assets and hundreds of daily observations, the sample covariance is well conditioned and shrinkage changes little. Its main use for us would be stabilizing the crypto-versus-ETF correlation, which shifts by regime.

---

## D. Kelly criterion, fractional Kelly, and estimation error

### D1. Kelly (1956) and Thorp, background `[from memory, unverified]`
Kelly, J. L. (1956). "A New Interpretation of Information Rate." Bell System Technical Journal 35(4), 917-926. Thorp, E. O., various, including "The Kelly Criterion in Blackjack, Sports Betting, and the Stock Market" (2006, Handbook of Asset and Liability Management). Not opened.

- Content from memory: maximizing expected log wealth maximizes the long-run growth rate. For a single asset with lognormal returns, the Kelly fraction is approximately (mu - r) / sigma^2 (excess drift over variance).
- Worked example, my arithmetic, not from a source: SPY with an assumed 6% excess drift and 16% volatility gives f = 0.06 / 0.0256, about 2.3, far above our cap of 1. BTC with an assumed 40% drift and 70% volatility gives about 0.8. The inputs are guesses; the point is that Kelly for equity indices usually asks for leverage, so under a cap of 1 the cap binds and Kelly gives no information, while for crypto the answer depends almost entirely on the drift guess.
- Implication (my inference): Kelly is useful to us mainly as an upper bound and as a reason never to exceed the cap, not as a sizing formula with estimated means.

### D2. MacLean, Thorp & Ziemba, "Good and bad properties of the Kelly criterion" `[opened: full text]`
MacLean, L. C., Thorp, E. O., Ziemba, W. T. (2010 draft). Published as "Long-term capital growth: the good and bad properties of the Kelly and fractional Kelly capital growth criteria", Quantitative Finance 10(7), 681-687 (2010); also chapter 39 of "The Kelly Capital Growth Investment Criterion" (World Scientific, 2011).
URL: https://www.stat.berkeley.edu/~aldous/157/Papers/Good_Bad_Kelly.pdf

- Good: Kelly maximizes the limiting exponential growth rate. "The main disadvantage of the Kelly criterion is that its suggested wagers may be very large. Hence, the Kelly criterion can be very risky in the short term."
- Overbetting: in continuous time "the growth rate becomes zero plus the risk free rate when one bets exactly twice the Kelly wager"; "it never pays to bet more than the Kelly strategy because then risk increases (lower security) and growth decreases".
- Estimation: citing Chopra and Ziemba (1993), errors in means versus variances versus covariances were "about 20:2:1 in importance" (cash-equivalent loss, at moderate risk aversion). Closing advice: "Given the extreme sensitivity of E log calculations to errors in mean estimates, these estimates must be accurate and to be on the safe side, the size of the wagers should be reduced."
- Slow dominance: with mu 20% versus 10% and both sigma 10%, A beats B with 95% confidence in five years; if A's sigma is 20%, it takes 157 years.
- Practice note: "practitioners who wish to protect capital above all, sharply reduce risk as their drawdown increases."
- Implication (my inference): our biggest error source would be the expected-return input, not volatility. Any Kelly-style rule should use volatility (which we estimate well) and a fixed, conservative edge assumption, or be replaced by fractional rules. Because overbetting by 2x drives growth to zero and our crypto drift is very uncertain, half-Kelly or less is the honest default if Kelly is used at all.

### D3. Baker & McHale, "Optimal Betting Under Parameter Uncertainty: Improving the Kelly Criterion" `[opened: abstract page]`
Baker, R. D., McHale, I. G. (2013). Decision Analysis 10(3), 189-199. DOI 10.1287/deca.2013.0271.
URL: https://econpapers.repec.org/RePEc:inm:ordeca:v:10:y:2013:i:3:p:189-199

- Claim (abstract, paraphrased): Kelly treats an estimated win probability as known. Because estimated inputs do worse out of sample, bets should be shrunk. Several shrinkage-factor estimates are compared; in simulations and on tennis betting data the shrunken versions beat raw Kelly. A "back of envelope" shrinkage correction is offered.
- No numbers on the abstract page; setting is a two-outcome bet, not a continuous portfolio.
- Implication (my inference): this formalizes "fractional Kelly because of estimation error". The shrinkage factor grows with the uncertainty of the edge, and for crypto drift estimated from a decade of data that uncertainty is large, which argues for small fractions.

### D4. Busseti, Ryu & Boyd, "Risk-Constrained Kelly Gambling" `[opened: abstract page]`
Busseti, E., Ryu, E. K., Boyd, S. (2016). arXiv:1603.06183 (published in Journal of Investing 25(3), 2016 `[from memory, unverified]`).
URL: https://arxiv.org/abs/1603.06183

- Claim: Kelly with a constraint that caps the probability of a wealth drawdown below a set level. A bound on drawdown probability turns this into a convex problem; Monte Carlo shows the bound is reasonably close to actual drawdown risk. One risk-aversion parameter trades growth for drawdown risk. Simulations show it beats fractional Kelly at the same drawdown risk or the same growth rate. A quadratic approximation is close to Markowitz mean-variance.
- Out-of-sample: simulations with known distributions, so estimation error is not addressed.
- Implication (my inference): useful as a reminder that "cap drawdown probability" and "fractional Kelly" are close cousins of mean-variance. It does not solve our real problem, which is unknown means.

### D5. Grossman & Zhou, "Optimal Investment Strategies for Controlling Drawdowns" `[from memory, unverified]`
Grossman, S. J., Zhou, Z. (1993). Mathematical Finance 3(3), 241-276. Not opened.

- Content from memory: if wealth must never fall below a fraction alpha of its running maximum, the optimal policy invests a constant-proportion (Merton-like) fraction of the cushion, wealth minus alpha times the peak, so exposure shrinks toward zero as the drawdown approaches the limit.
- Implication (my inference): this is the formal version of "cut risk as drawdown grows" (D2). A simple testable form: exposure = min(1, k x (1 - drawdown / D_max)) with D_max fixed in advance. It sells after losses and buys after recoveries, so it behaves like trend-following and will be whipsawed in choppy markets; costs matter for crypto.

---

## E. Rebalancing premium and "volatility harvesting"

### E1. Fernholz & Shay (1982); Shannon's demon; Luenberger's volatility pumping `[from memory, unverified]`
Fernholz, R., Shay, B. (1982). "Stochastic Portfolio Theory and Stock Market Equilibrium." Journal of Finance 37(2), 615-624. Luenberger, D. (1997). Investment Science, chapter on volatility pumping. Not opened; the quotes below are as reproduced in E2.

- The claim as summarized and quoted by E2: a constant-weight cash-stock portfolio "will buy on a downtick and sell on an uptick", so if the risky asset and cash have equal expected growth (both normalized to zero), a 50/50 rebalanced mix has expected growth sigma^2/8. Luenberger: "The pumping effect is obviously most dramatic when the original variance is high... you will likely begin to enjoy volatility, seeking it out".
- My arithmetic, not from a source: for BTC with annual volatility around 70%, sigma^2/8 is about 6% a year, which is why BTC/cash rebalancing looks attractive on paper.

### E2. Cuthbertson, Hayley, Motson & Nitzsche, "What Does Rebalancing Really Achieve?" `[opened: full text]`
Cuthbertson, K., Hayley, S., Motson, N., Nitzsche, D. (2016). International Journal of Finance & Economics 21(3), 224-240. DOI 10.1002/ijfe.1545. Accepted version dated 2016-02-04.
URL: https://openaccess.city.ac.uk/id/eprint/13733/1/What%20Does%20Rebalancing%20Really%20Achieve%204-Feb-2016.pdf

- Method: analytics plus simulation with IID returns (the case least favorable to buy-and-hold). No empirical backtest.
- Claim 1: "in the absence of mean reversion in relative asset prices the greater expected growth of rebalanced strategies is entirely explained by their lower portfolio volatilities rather than... being due to the rebalancing trades themselves being profitable." Unrebalanced portfolios also earn "excess growth" while they stay diversified.
- Claim 2 (one risky asset plus cash): rebalanced and buy-and-hold portfolios start with equal expected growth; over finite horizons "expected portfolio final wealth for an unrebalanced portfolio is greater than for a rebalanced portfolio". Rebalancing wins on paths that mean-revert and loses when the risky asset "makes large cumulative moves in either direction (i.e. tends instead to trend)".
- Claim 3: "Rebalancing will be profitable in markets which tend to mean-revert, and loss-making in markets which tend to show momentum." Following the volatility-pumping argument leads to "insufficient diversification and excessive transactions costs".
- Implication (my inference): a fixed BTC/cash or BTC/GLD mix rebalanced often is a bet on mean reversion in the BTC/cash ratio, and in effect short a trend (the payoff is like selling volatility on large moves). Part 3 of this survey found BTC trends at weekly horizons. So frequent rebalancing of a BTC mix should not be expected to add return; rebalance for risk control only, rarely or with wide bands, since every rebalance costs about 30 bps per side in crypto.

---

## F. Crypto in a multi-asset portfolio

### F1. Platanakis & Urquhart, "Should investors include Bitcoin in their portfolios? A portfolio theory approach" `[opened: abstract page]`
Platanakis, E., Urquhart, A. (2020). The British Accounting Review 52(4), 100837. DOI 10.1016/j.bar.2019.100837. SSRN 3215321.
URL: https://ideas.repec.org/a/eee/bracre/v52y2020i4s0890838919300605.html (the CORE full-text PDF returned 403)

- Sample: traditional stock and bond benchmark portfolio plus Bitcoin, data up to June 2018 (start date not on the page). Eight asset-allocation strategies tested out of sample (which eight is not on the page).
- Claim: "the benefits of Bitcoin are quite considerable with substantially higher risk-adjusted returns"; robust to rolling windows, "the incorporation of transaction costs", a commodity portfolio, alternative indices, short selling, and higher-moment optimizers. Conclusion: "investors should include Bitcoin in their portfolio."
- Caveat (mine): the sample ends June 2018, so it includes the 2013 and 2017 BTC run-ups and only the start of the 2018 bear market. Out of sample in the rolling-window sense, but not out of sample in time relative to BTC's bubble phase. No numbers checked.
- Implication (my inference): academic support for "some BTC improves a stock-bond portfolio" exists but rests on a sample dominated by BTC's early growth. Treat the size of the benefit as unknown going forward.

### F2. Howard (FTSE Russell), "Risk-friendly ways to consider a Bitcoin allocation" `[opened: full text, practitioner note]`
Howard, M. (November 2020). FTSE Russell Education note.
URL: https://www.lseg.com/content/dam/ftse-russell/en_us/documents/research/ftse_russell-education_risk_friendly_ways_to_consider_a_bitcoin_allocation_0.pdf

- Sample: 2014-12-31 to 2020-09-30, hypothetical index data; Russell 1000 as the equity leg. No transaction costs mentioned.
- Numbers (Exhibit 1): Russell 1000 return 10.71% a year, volatility 18.49%, return/risk 0.58, max drawdown -34.58%. Bitcoin 80.59%, 72.86%, 1.11, -83.00%. Bitcoin 50% / cash 50% rebalanced daily: 43.75%, 36.43%, 1.20, -55.22%. Bitcoin 25% target volatility: 38.49%, 24.39%, 1.58, -42.07%, with "around 45% allocated to Bitcoin and 55% allocated to cash" on average. Russell 1000 + 2.5% BTC, quarterly rebalanced: 13.31%, 18.46%, 0.72, -34.54%. With 5% BTC: 15.87%, 18.72%, 0.85, -34.63%.
- The author notes the target-volatility version "essentially represents an all or nothing exposure to the digital asset".
- Correlation: average 12-month rolling BTC/Russell 1000 correlation 0.06 since 2015; about 0.26 since the start of 2020.
- Implication (my inference): in this window, volatility targeting BTC raised return per unit risk from 1.11 to 1.58 and cut the drawdown from 83% to 42%, without leverage (BTC weight below 100% by construction at a 25% target). That is the de-risk-only case that matters for us. But it is one bull-dominated sample, no costs, daily rebalancing, and an index provider's marketing-adjacent note. It must be retested with 60 bps round trips, next-open fills, and 2021-2025 data.

### F3. Goodall & Abou Zeid (Man Group), "Crypto: Too Hot to Handle?" `[opened: practitioner article]`
Goodall, R., Abou Zeid, T. (2025-03-21). Man Group Insights.
URL: https://www.man.com/insights/crypto-too-hot-to-handle

- Sample: BTC 2012-09-01 to 2024-12-31 for the volatility-scaling exhibits.
- Claims: BTC volatility range fell from "20-130%" in the 2010s to "closer to 30-60%" in the 2020s; drawdowns could reach "up to 50%" at current volatility versus "roughly 70%" when volatility was near 130%. Scaling BTC ex ante to 30% volatility adds "around 40 Sharpe points in each instance", regardless of the volatility-estimate half-life; vol of vol and expected shortfall also improve (figures only in a chart I could not read). For a 1% BTC sleeve in a 60/40, the unscaled sleeve's share of portfolio risk "oscillates between 0 and 6%"; the scaled one stays in a tight range. BTC-equity correlation has risen since 2020.
- Costs and leverage: not stated in the text. Scaling to 30% volatility when BTC runs at 30-60% means exposure mostly at or below 1, so it is close to our de-risk-only case, but at times of 20% BTC volatility it would lever.
- Implication (my inference): two independent practitioner sources (F2, F3) agree that volatility-scaling BTC improves risk-adjusted returns, and Harvey et al. (A3) give the mechanism (a leverage effect acting like momentum). Crypto is the one asset in our universe where de-risk-only volatility timing has a plausible case. It is also where costs are highest, so exposure changes need bands.

---

## Verdict for this family

**Held up.** (1) Volatility targeting reliably cuts tail losses, vol of vol and drawdowns across assets (A3), and the scaled series uses only past data. (2) Simple beats optimized: 1/N and volatility-only rules match or beat mean-variance out of sample (B2), and a long-only constraint already does most of what covariance shrinkage does (C2). (3) Risk parity has a higher Sharpe than 60/40 over 1926-2010 (B1: 0.52 unlevered versus 0.40). (4) Kelly's core lessons are robust: never bet above Kelly, errors in means dominate (about 20:2:1 versus variances and covariances), so shrink bets (D2, D3). (5) Volatility-scaling BTC improved risk-adjusted returns in two practitioner samples (F2, F3).

**Failed or weaker than claimed.** Moreira-Muir alphas do not become real-time gains: out of sample the scaled market lost to the plain market (Sharpe 0.42 versus 0.46), and leverage caps of 1.0 or 1.5 did not fix it (A2). With the look-ahead removed and leverage allowed, drawdowns reached 68-93% (A4). After costs, volatility management of factors other than the market earns nothing (A5). Sharpe gains from volatility scaling are absent for bonds, currencies and commodities, and negative for US bonds 1963-2017 (A3). Unlevered risk parity earns a low absolute return (2.20% a year excess in B1), and the stock-bond hedge failed in 2022 (B4). "Rebalancing premium" and volatility pumping are mostly diversification, and rebalancing loses on trending paths (E2).

**Biggest caveats for our setup.** Our cap at 100% removes the lever-up half that produces most published volatility-timing gains; only the de-risk half is left, and its evidence is mostly about tails, not return. Cash earns 0 here, so every de-risked dollar gives up the full risk premium. Crypto evidence is from short, bull-dominated samples with no costs (F1, F2). Daily volatility estimates move weights daily: at 60 bps a crypto round trip, unbanded rebalancing can eat the benefit. Kelly with estimated crypto drift is close to meaningless; SPY Kelly almost always exceeds 1, so the cap binds.

**Testable ideas for our universe (fix parameters before looking at our data).**
1. Inverse-volatility weights across all six assets (60-day realized volatility, monthly rebalance, weights sum to 1), against 1/N and buy-and-hold SPY, with 2022 reported separately.
2. BTC and ETH de-risk-only targeting: weight = min(1, 40% / 20-day realized volatility), traded only when the target weight moves by more than 10 percentage points.
3. The same min(1, target / realized volatility) rule on SPY and QQQ, target = trailing 5-year median volatility from past data only; judge it on drawdown and Sharpe, not total return.
4. A fixed 5% BTC sleeve in an equal-weight SPY/GLD/TLT core, rebalanced quarterly versus never, to measure whether rebalancing adds anything after costs.
5. Equal risk contribution (or HRP) versus plain inverse volatility on the same six assets: a single comparison to see whether accounting for the BTC-ETH and SPY-QQQ correlations matters.

**Source count.** 17 sources opened (7 as full text, one of them a practitioner note; 8 as abstract or landing pages; 2 as practitioner web articles); 5 entries rest on memory or search snippets only and are tagged `[not opened]` or `[from memory, unverified]`.
