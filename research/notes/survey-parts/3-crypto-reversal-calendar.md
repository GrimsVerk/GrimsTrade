# Part 3: Crypto-specific effects, short-term mean reversion, calendar anomalies

Survey date: 2026-11-12. Scope: what the literature says for a long-only, unlevered, daily-bar
book in BTC, ETH, SPY, QQQ, GLD, TLT with next-open fills and costs of about 60 bps per crypto
round trip and about 4 bps per ETF round trip.

How to read the entries:

- `[opened: full text]` means I read the paper itself (PDF text).
- `[opened: abstract page]` means I read only the abstract or landing page; numbers are limited to what that page shows.
- `[opened: secondary summary]` means I read a third-party summary, not the paper.
- `[not opened]` means the entry rests on a search snippet or on another paper's description; treat as unverified.
- "Implication" lines are my inference for this setup, not claims made by the authors.

---

## A. Crypto: momentum versus reversal at daily and weekly horizons

### A1. Liu & Tsyvinski, "Risks and Returns of Cryptocurrency" `[opened: full text of NBER WP]`
Liu, Y., Tsyvinski, A. (2018). NBER Working Paper 24877. Published in Review of Financial Studies 34(6), 2021, 2689-2727.
URL: https://www.nber.org/papers/w24877 (PDF: https://www.nber.org/system/files/working_papers/w24877/w24877.pdf)

- Sample: BTC 2011-01-01 to 2018-05-31, XRP from 2013-08, ETH from 2015-08-07 to 2018-05-31. Daily, weekly, monthly.
- Claim: time-series MOMENTUM, not reversal, at daily and weekly horizons. A one-standard-deviation rise in today's BTC return (5.55%) predicts +0.33% the next day. A one-standard-deviation rise in this week's return (16.64%) predicts +3.16% next week, and the effect persists to 4 weeks. Weekly quintiles: top quintile 11.22% per week next week (Sharpe 0.45) versus bottom quintile 2.60% (Sharpe 0.19). "For Ethereum, the momentum effect is less significant than for Bitcoin and Ripple."
- Attention: a one-standard-deviation rise in Google searches for "Bitcoin" predicts +2.3% over the 2-week-ahead return; Twitter count +2.50% at 1 week; the "Bitcoin hack" search ratio predicts -2.75% the following week.
- Valuation: a price-to-"dividend" ratio built from BTC price over wallet-user count "has no predictive power". Realized volatility does not predict BTC or ETH returns.
- Day of week: no Monday effect; Saturday is lower (BTC 0.33% on Saturdays versus 0.52% daily average).
- Out-of-sample: only an internal check (first two years set the quintile cutoffs). No costs. The sample ends May 2018 and is dominated by the 2011-2017 run-up.
- Implication: the daily effect goes the wrong way for a reversal rule and is too small for us in either direction. 0.33% per one-sigma move is below a 60 bps round trip. Weekly momentum was large in-sample but see A3-A5 for decay.

### A2. Shen, Urquhart & Wang, "A three-factor pricing model for cryptocurrencies" `[opened: abstract page]`
Shen, D., Urquhart, A., Wang, P. (2020). Finance Research Letters 34. DOI 10.1016/j.frl.2019.07.021.
URL: https://ideas.repec.org/a/eee/finlet/v34y2020ics1544612319304519.html

- Sample: more than 1,700 coins, April 2013 to March 2019. Weekly sorts (per search summary of the working paper; not read directly).
- Claim: market, size and REVERSAL factors price the cross-section. "Reversal returns also increase from larger to smaller cryptocurrencies."
- Critique `[not opened]`: Jia, Goodell & Shen (2022, Finance Research Letters 45) reportedly find momentum rather than reversal in a more recent sample (https://ideas.repec.org/a/eee/finlet/v45y2022ics1544612321002208.html, link from search, page not read).
- Implication: the reversal premium is a small-coin, cross-sectional, long-short result. It says nothing positive about BTC or ETH.

### A3. Bianchi, Babiak & Dickerson, "Trading volume and liquidity provision in cryptocurrency markets" `[opened: full text of working paper]`
Bianchi, D., Babiak, M., Dickerson, A. (2022). Sveriges Riksbank WP 413; published in Journal of Banking & Finance 142, 106547.
URL: https://www.riksbank.se/globalassets/media/rapporter/working-papers/2022/no.-413-trading-volume-and-liquidity-provision-in-cryptocurreny-markets.pdf

- Sample: USD pairs on multiple centralised exchanges, 2017-03-01 to 2022-03-01, daily rebalancing.
- Claim: daily short-term reversal profits (a proxy for liquidity provision) sit in low-volume, small, volatile pairs. Equal-weighted reversal: 1.26% per day on low-volume pairs versus 0.54% on high-volume pairs. Value-weighted: 0.65% (low volume) versus -0.19% (p = 0.251) on high-volume pairs.
- Direct statement: "for larger, more liquid, and less volatile assets the reversal strategy returns tend to be close to zero and are not statistically significant."
- After costs (30 bps long side, 40 bps short side): equal-weighted reversal survives (1.68% per day reported); "for the value-weighted sorts, none of the strategies generate positive and statistically significant returns." The authors also say the paper is not a trading recipe: returns assume fills at the closing price.
- Implication: this is the clearest evidence against daily mean reversion in BTC/ETH. The effect is a small-coin liquidity premium, it needs a short leg, and it vanishes when value-weighted and costed.

### A4. Dobrynskaya, "Cryptocurrency Momentum and Reversal" `[opened: abstract page]`
Dobrynskaya, V. (2023). Journal of Alternative Investments 26(1), 65-76. DOI 10.3905/jai.2023.1.189. SSRN id 3913263 (SSRN page returned 403, not read).
URL: https://publications.hse.ru/en/view/811744977

- Sample: 2,000 largest coins, 2014-2020. Cross-sectional sorts, horizons 1 week to 2 years.
- Claim: momentum up to about 2-4 weeks, significant reversal beyond about 1 month; the reversal is driven by "past loser" coins.
- No cost numbers on the page. Cross-sectional and long-short.

### A5. Dobrynskaya & Dubrovskiy, "Cryptocurrencies Meet Equities: Risk Factors and Asset Pricing Relationships" `[opened: full text of working paper, first sections]`
HSE Working Paper WP BRP 86/FE/2022.
URL: https://wp.hse.ru/data/2022/02/24/1749596434/86FE2022.pdf

- Sample: 2,000 coins above $1m capitalisation, 2014-01-06 to 2020-11-01, weekly.
- Claim: "Momentum premium has vanished in the recent years," attributed to extraordinary performance of several past-loser coins. Equity market risk, especially equity downside risk, is priced in crypto and "appears to be more important than cryptocurrency market risk."
- Implication: two points for us. Cross-sectional crypto momentum decayed after the early samples. Crypto carries equity downside risk, so BTC/ETH do not diversify SPY/QQQ when it matters.

### A6. Grobys & Sapkota, "Cryptocurrencies and momentum" `[opened: abstract page]`
Economics Letters 180 (2019), 6-10. DOI 10.1016/j.econlet.2019.03.028.
URL: https://ideas.repec.org/a/eee/ecolet/v180y2019icp6-10.html

- 143 coins, 2014-2018. "Our findings do not indicate any evidence of significant momentum payoffs."

### A7. Tzouvanas, Kizys & Tsend-Ayush, "Momentum trading in cryptocurrencies: Short-term returns and diversification benefits" `[opened: abstract page]`
Economics Letters 191 (2020). DOI 10.1016/j.econlet.2019.108728.
URL: https://ideas.repec.org/a/eee/ecolet/v191y2020ics0165176519303647.html

- Twelve coins, about three years of daily data, J/K portfolios. Momentum "highly significant for short-term portfolios" and gone at longer horizons. No cost numbers on the page.
- A6 and A7 together: results flip with universe and horizon. That instability is itself the finding.

### A8. Fieberg, Liedtke, Poddig, Walker & Zaremba, "A Trend Factor for the Cross Section of Cryptocurrency Returns" `[opened: full text]`
Journal of Financial and Quantitative Analysis 60(7), 2025, 3116-3153. Open access. DOI 10.1017/S0022109024000747.
URL: https://doi.org/10.1017/S0022109024000747

- Sample: more than 3,000 coins, April 2015 to May 2022, weekly. 28 technical signals aggregated by machine learning into "CTREND".
- Headline: long-short quintile spread 3.87% per week gross (t = 5.19). Largest 100 coins: 3.40% gross.
- After costs (30/40, 40/50, 50/60 bps long/short): full sample 2.90% to 2.35% per week; largest 100 coins 2.45% to 1.90%, all significant. Weekly turnover about 68%. Break-even cost 1.41% (1.25% for the largest 100).
- Long leg alone, largest 100 coins: 3.78% gross, 3.11-3.38% net per week (t about 3.6-3.9). The low-trend quintile earns about zero, so in this paper the long side carries the result.
- Caveats: one bull-heavy sample; the authors test 55,296 design variants and report robustness, which is reassuring on specification but not on time; no post-2022 evidence here.
- Implication: the strongest after-cost crypto result in this family is TREND, not reversal, and it is cross-sectional across 100+ coins. With two coins we cannot run it. What transfers is the direction: use trend as a long-or-cash filter on BTC/ETH, at weekly rather than daily turnover.

### A9. Fieberg, Liedtke & Zaremba, "Cryptocurrency anomalies and economic constraints" `[opened: abstract page]`
International Review of Financial Analysis 94 (2024), 103218. DOI 10.1016/j.irfa.2024.103218.
URL: https://ideas.repec.org/a/eee/finana/v94y2024ics1057521924001509.html

- Claim: size and volume anomalies come from "micro-cap coins of negligible economic importance." Momentum survives in larger coins but "incurs substantial trading costs and extracts alphas largely from short positions." Abnormal returns occur mainly in bull markets and fade over time.
- The authors' own protocol: focus on long positions, charge costs, emphasise recent years. That is the right template for our tests.
- Note the tension with A8 on which leg carries the profit. Unresolved here.

### A10. Wen, Bouri, Xu & Zhao, "Intraday return predictability in the cryptocurrency markets: Momentum, reversal, or both" `[opened: abstract page]`
North American Journal of Economics and Finance 62 (2022). DOI 10.1016/j.najef.2022.101733.
URL: https://ideas.repec.org/a/eee/ecofin/v62y2022ics1062940822000833.html

- BTC high-frequency data, 2013-03-03 to 2020-05-31; similar patterns reported for ETH, LTC, XRP. Both intraday momentum and intraday reversal exist; patterns shift with jumps, FOMC releases, liquidity and COVID.
- No cost statement on the page. Intraday, so outside a once-a-day decision model.

### A11. Padysak & Vojtko (Quantpedia), "Revisiting Trend-following and Mean-reversion Strategies in Bitcoin" `[opened: practitioner article]`
Follow-up to "Seasonality, Trend-following, and Mean reversion in Bitcoin" (2022, SSRN; original not opened).
URL: https://quantpedia.com/?p=35597

- Rules: MAX = long BTC when the daily price is at its 10-50 day high; MIN = long when at its 10-50 day low. Gemini daily prices from Oct 2015. In-sample Nov 2015 to Feb 2022; out-of-sample 2022-02-04 to 2024-08-20.
- Out-of-sample: MAX (trend) "remains alive and well"; a 20-day high did better than 10-day. MIN (dip-buying) produced low or negative returns over the 2.5 years. No significant day-of-week pattern in either.
- Limits: performance tables are images I could not read, so no numbers here. No transaction costs. Not peer reviewed.
- Implication: the one explicit out-of-sample check of BTC dip-buying on daily bars that I found failed, before costs.

---

## B. Crypto seasonality, halving, on-chain, attention

### B1. Caporale & Plastun, "The Day of the Week Effect in the Crypto Currency Market" `[opened: abstract page]`
DIW Discussion Paper 1694 (2017); later in Finance Research Letters (2019).
URL: https://www.diw.de/de/diw_01.c.567282.de/publikationen/diskussionspapiere/2017_1694/the_day_of_the_week_effect_in_the_crypto_currency_market.html

- BTC, LTC, XRP, Dash. Only BTC shows an anomaly: Monday returns "significantly higher than those on the other days of the week." Sample period not stated on the page. A search summary says most simulated trading results were not different from random; I did not verify that in the paper.

### B2. Baur, Cahill, Godfrey & Liu, "Bitcoin time-of-day, day-of-week and month-of-year effects in returns and trading volume" `[opened: abstract page]`
Finance Research Letters 31 (2019), 78-92. DOI 10.1016/j.frl.2019.04.023.
URL: https://econpapers.repec.org/RePEc:eee:finlet:v:31:y:2019:i:c:p:78-92

- More than 15 million observations from seven exchanges. Time-specific return anomalies exist but do not persist over time. Volume patterns are stable: lower activity in local evenings and on weekends.

### B3. Kaiser, "Seasonality in cryptocurrencies" `[opened: abstract page]`
Finance Research Letters 31 (2019). DOI 10.1016/j.frl.2018.11.007.
URL: https://ideas.repec.org/a/eee/finlet/v31y2019ics1544612318304513.html

- Ten coins. No consistent or robust calendar effects in returns; weak-form efficiency not rejected. Robust patterns only in volume, volatility and spreads (lower on weekends, in January, in summer). The January 2018 sell-off alone flips monthly results.
- Implication for B1-B3 plus A1 and A11: crypto day-of-week results disagree with each other (Monday high in one, Saturday low in another, nothing in three). A weekly in-and-out trade costs about 52 x 0.6% = 31% a year in our cost model (my arithmetic). Not worth testing.

### B4. Halving cycle `[opened: two abstract pages]`
- Veloso, Gatsios, Magnani & Lima (2025), "Is Bitcoin's Market Maturing? Cumulative Abnormal Returns and Volatility in the 2024 Halving and Past Cycles," Journal of Risk and Financial Management 18(5), 242. URL: https://ideas.repec.org/a/gam/jjrfmx/v18y2025i5p242-d1647669.html. Event study on the 2012, 2016, 2020, 2024 halvings; concludes that returns and volatility around halvings are declining.
- Virtonen (2025), "Estimating the Impact of the Bitcoin Halving on Its Price Using Synthetic Control," arXiv:2511.05512. URL: https://arxiv.org/abs/2511.05512v1. Finds evidence of a positive effect about three months after the 2024 halving; fails to get a significant, robust estimate for 2020. Preprint.
- Implication: four events, all pre-announced, mixed causal evidence. There is no sample to validate a rule on. Do not trade it.

### B5. On-chain valuation and network factors
- Liu & Tsyvinski (A1) `[opened]`: price-to-wallet-users ratio does not predict BTC returns.
- Cong, Li & Wang, "Tokenomics: Dynamic Adoption and Valuation," NBER WP 27222 (2020); Review of Financial Studies 34(3), 2021, 1105-1155 `[opened: abstract page]`. URL: https://www.nber.org/papers/w27222. Theory paper: token value comes from users' transactional demand, with feedback between adoption and price. It makes no return-predictability claim.
- Liu, Tsyvinski & Wu, "Common Risk Factors in Cryptocurrency," NBER WP 25882 (2019); Journal of Finance 77(2), 2022, 1133-1177 `[opened: abstract page]`. URL: https://www.nber.org/papers/w25882. Market, size and momentum explain the cross-section; nine long-short strategies are subsumed by those three factors. Cross-sectional, so not usable with two coins.
- Grobys, Näsman & Sandretto (2026), "Using on-chain data to predict Bitcoin cycles," Research in International Business and Finance 89, DOI 10.1016/j.ribaf.2026.103486 `[not opened: repository blocked automated access; from search snippet]`. Reportedly finds MVRV Z-score rules beat buy-and-hold and NUPL rules. Link not verified by reading; repository handle from search: https://osuva.uwasa.fi/handle/11111/20453.
- Implication: I found no opened source showing MVRV, NVT or active addresses predicting BTC out of sample after costs. MVRV-type rules fire a handful of times per cycle, so any backtest has very few independent trades. Low priority; needs an extra data feed.

### B6. Investor attention
- Covered in A1: Google and Twitter attention predicted 1-2 week BTC returns in 2011-2018. I did not open any post-2018 replication. Treat as unverified out of sample.

---

## C. Bitcoin versus equities and gold

### C1. Klein, Pham Thu & Walther, "Bitcoin is not the New Gold: A comparison of volatility, correlation, and portfolio performance" `[opened: abstract page]`
International Review of Financial Analysis 59 (2018), 105-116. DOI 10.1016/j.irfa.2018.07.010.
URL: https://econpapers.repec.org/RePEc:eee:finana:v:59:y:2018:i:c:p:105-116

- BEKK-GARCH correlations. Gold acts as flight-to-quality in distress; Bitcoin "behaves as the exact opposite and it positively correlates with downward markets." No stable hedging benefit found.

### C2. Iyer, "Cryptic Connections: Spillovers between Crypto and Equity Markets" `[opened: IMF landing page]`
IMF Global Financial Stability Note 2022/01, January 2022.
URL: https://www.imf.org/en/Publications/global-financial-stability-notes/Issues/2022/01/10/Cryptic-Connections-511776

- Since the start of COVID-19, BTC volatility spillovers to the S&P 500 and MSCI EM rose by about 12-16 percentage points and return spillovers by about 8-10 points. BTC explains about 14-18% of equity volatility variation and 8-10% of equity return variation.
- Implication for C1, C2 and A5: treat BTC/ETH as high-beta risk assets, not as digital gold. In a six-asset long-only book the real diversifiers are GLD, TLT and cash. Size crypto by volatility and expect it to fall with QQQ in stress.

### C3. Crypto carry (funding rate / basis): not available to us `[opened: BIS landing page]`
Schmeling, Schrimpf & Todorov, "Crypto carry," BIS Working Paper 1087 (April 2023, revised 2025).
URL: https://www.bis.org/publ/work1087.htm

- Carry on BTC and ETH futures averages above 10% a year and can reach 60% a year. It is earned by "going long in the spot market, while selling short in the futures contract," and is exposed to margin spikes and liquidation.
- Implication: it needs a short futures or perp leg. Our mandate has none, so the trade is out of scope. The one usable idea, that very high carry warns of crashes, would need a futures data feed.

---

## D. ETF short-term mean reversion

### D1. Baltussen, van Bekkum & Da, "Indexing and Stock Market Serial Dependence Around the World" `[opened: full text of accepted manuscript]`
Journal of Financial Economics 132(1), 2019, 26-48. DOI 10.1016/j.jfineco.2018.07.016.
URL: https://personal.eur.nl/vanbekkum/2018%20JFE%20BaltussenVanBekkumDa.pdf

- Sample: 20 major stock indexes in 15 countries, plus their futures and ETFs.
- Claim: daily index AR(1) hovered around +0.05 from 1951, fell from the 1980s, turned negative in the 2000s. Before 1999 it was positive for all 20 indexes; after 1999 it is negative for 16 of 20, significantly so for 7. Weekly AR(1) is negative for all 20 after 1999. The shift is tied to index products.
- Economic size: a strategy trading against multi-day autocorrelation (MAC(5)) earns an annualised Sharpe of 0.63 on all indexes and 0.67 on the S&P 500 after 2 March 1999, with similar figures for futures and ETFs. Before costs, long-short.
- Authors' own caveat: it "requires frequent rebalancing" and "perhaps is not exploitable to many investors after accounting for transaction costs."
- Implication: this is the best academic support for SPY/QQQ dip-buying, and it is a post-1999 regime, not a law. We pay only about 2 bps a side, so costs are not the obstacle. The obstacles are that we can only run the long half, that cash earns 0, and that we fill at the next open rather than the close.

### D2. Connors' RSI(2) and short-term rules `[opened: secondary review]` and Zarattini (Concretum), "Opportunity-set bias in mean-reversion trading systems" `[opened: practitioner article]`
URLs: https://www.cxoadvisory.com/technical-trading/a-few-notes-on-short-term-trading-strategies-that-work and https://concretumgroup.com/opportunity-set-bias-in-mean-reversion-trading-systems/

- CXO Advisory review of Connors & Alvarez (2008): backtests use daily data 1995-2007; no data-snooping correction, no held-out sample, no cost sensitivity, little on drawdowns or subperiods.
- Concretum: S&P 500 constituents, 1996 to Nov 2025. Entry RSI(2) < 5 and close below the 5-day average, buy next open; exit next open after first close above the 5-day average, or after 5 days. 114,189 trades, mean 45 bps per trade, 64% hit rate. About 3.1% of days hold 50% of all trades. In 10,000 simulations capped at five trades a day, none matched the full-sample mean. No costs modelled. Single stocks, not index ETFs.
- I found no rigorous source on post-2008 decay of RSI(2) on SPY itself. Blog claims go both ways and I do not cite them.
- Implication: the edge clusters in sell-offs. With two equity ETFs we do not have the capacity problem, but we do have the same state dependence: the trades come in bunches exactly when SPY and QQQ fall together.

### D3. AQR, "Hold the Dip" `[opened: full text]`
Cao, Chong & Villalon, AQR Alternative Thinking 2025 Issue 4.
URL: https://www.aqr.com/Insights/Research/Alternative-Thinking/Hold-the-Dip

- 196 buy-the-dip variants on the S&P 500 (4 depths x 7 lengths x 7 holding periods), in cash otherwise, 1965-01-01 to 2025-09-30.
- Average Sharpe is 0.04 below buy-and-hold (about 16% worse); over 60% of variants underperform. From October 1989 (total-return data) the gap is 0.27 (47% worse). Average alpha to equities 0.5% a year; only 16 of 196 variants are significant.
- Reason given: buy-the-dip is "usually positioned opposite momentum." The authors exclude high-frequency variants as cost-sensitive stat-arb, so this does not test a 2-day RSI rule directly.
- Implication: sets the benchmark. A dip rule on SPY must beat buy-and-hold on Sharpe, not just make money. With cash at 0 the bar is higher still.

---

## E. Calendar anomalies in equities and bonds

### E1. McConnell & Xu, "Equity Returns at the Turn of the Month" `[opened: abstract page]`
Financial Analysts Journal 64(2), 2008, 49-64. DOI 10.2469/faj.v64.n2.11.
URL: https://rpc.cfainstitute.org/research/financial-analysts-journal/2008/equity-returns-at-the-turn-of-the-month

- US equities 1926-2005: investors earned no reward for market risk except at turns of the month. Holds outside small caps, outside year-ends, and in 31 of 35 countries. Not explained by volume or fund flows. (A search summary gives 0.15% average daily value-weighted return over the four-day window; I did not see this on the page.)
- Lakonishok & Smidt (1988), "Are Seasonal Anomalies Real? A Ninety-Year Perspective," Review of Financial Studies 1(4), 403-425, DOI 10.1093/rfs/1.4.403 `[not opened: from search snippet]`: 90 years of Dow data, persistent anomalies at the turn of the week, month, year and around holidays. Link not verified.

### E2. Han, Han & Tian, "The disappearing turn-of-month effect" `[opened: abstract page]`
Finance Research Letters 71 (2025). DOI 10.1016/j.frl.2024.106461.
URL: https://ideas.repec.org/a/eee/finlet/v71y2025ics1544612324014909.html

- The turn-of-month effect "disappears entirely after 2001." Explanation offered: the sharp fall in transaction costs after 2001 let arbitrageurs trade against it and removed the reason to bunch trades at month-end. No magnitudes on the page.

### E3. Etula, Rinne, Suominen & Vaittinen, "Dash for Cash: Monthly Market Impact of Institutional Liquidity Needs" `[opened: full text, selected sections]`
Review of Financial Studies 33(1), 2020, 75-111. DOI 10.1093/rfs/hhz054. Open access copy:
URL: https://acris.aalto.fi/ws/portalfiles/portal/40965155/hhz054.pdf

- Mechanism: institutions need cash at month-end; with T+3 settlement they had to sell stocks by T-4, Treasuries (T+1) by T-2. Prices dip, then recover.
- Numbers (CRSP value-weighted, since the 1995 settlement rule, sample to Dec 2013): holding-period return -17 bps over T-8..T-4 and +77 bps over T-3..T+3. Abnormal: -37 bps for T-8..T-4, +25 bps for T-3..T-1, +48 bps for T-3..T+3. Reversals in all 23 equity markets surveyed, significant in 20. Effects are two to three times larger when month-end is a Friday. Treasury yields stay elevated until about T-2.
- Caveats: sample ends 2013; US equity settlement moved to T+2 in September 2017 (stated in the paper), which shifts the dates; E2 says the plain turn-of-month effect is gone after 2001. These two papers are not obviously consistent and I did not resolve it.
- Implication: cheap to test on SPY, QQQ and TLT (about 4 bps a round trip, one round trip a month). Expect a weak or dead result post-2014.

### E4. Lucca & Moench, "The Pre-FOMC Announcement Drift" `[opened: full text of staff report]` and Kurov, Wolfe & Gilbert, "The disappearing pre-FOMC announcement drift" `[opened: abstract page]`
Lucca & Moench: NY Fed Staff Report 512 (2011, rev. 2013); Journal of Finance 70(1), 2015, 329-371. URL: https://www.newyorkfed.org/research/staff_reports/sr512.html
Kurov et al.: Finance Research Letters 40 (2021), DOI 10.1016/j.frl.2020.101781. URL: https://ideas.repec.org/a/eee/finlet/v40y2021ics1544612320315956.html

- Original: Sept 1994 to March 2011, the S&P 500 rose on average 49 bps in the 24 hours before scheduled FOMC announcements (2 pm to 2 pm, t above 4.5). That is about 80% of annual realised excess returns; holding only that window gave a Sharpe above 1.1. 1980-1993: 20 bps on meeting days. No effect in Treasuries.
- Follow-up: extending to December 2019, the drift "essentially disappeared after 2015," at meetings with and without press conferences.
- Fill problem: the window is 2 pm to 2 pm. With next-open fills the closest we get is open-to-open across two sessions, which adds about a day of unrelated noise.
- Implication: a textbook post-publication decay. Do not build on it. At most run it as a known-dead control.

### E5. Jacobsen & Zhang, "The Halloween Indicator, 'Sell in May and Go Away': an even bigger puzzle" `[opened: full text of working paper]`
SSRN id 2154873 working paper (hosted copy). A later version was published as "The Halloween indicator, 'Sell in May and Go Away': Everywhere and all the time" (2021; journal page not opened).
URL: https://a.storyblok.com/f/331657/x/44b806eeba/ssrn-id2154873.pdf
Original: Bouman & Jacobsen (2002), American Economic Review `[not opened: described in this paper]`; winter beats summer in 36 of 37 countries.

- All available index history, 65 countries pooled: summer (May-Oct) excess return -1.17% (t = 3.36) versus winter 4.89% (t = 14.52); November-April returns 4.5% higher (t = 11.42).
- Out-of-sample for the 37 original countries, Sept 1998 to 2011: positive point estimate in all 37, significant in 15; average coefficient 8.9% versus 8.2% in-sample. The winter-only strategy beat buy-and-hold on raw return in 31 of 37 markets and on Sharpe in 36 of 37.
- Caveats: same author as the original; the skeptics (Maberly & Pierce 2003/2004; Dichtl & Drobetz 2014) were not opened; the out-of-sample window ends 2011 and I verified nothing after that; index data exclude dividends in places.
- Implication: two trades a year, so cost and fill timing are irrelevant. But it is one observation a year: 15 years of post-2011 data cannot confirm or reject it. Being in cash at 0 for six months is expensive if the effect is merely weak.

### E6. Overnight versus intraday returns
- Cliff, Cooper & Gulen, "Return Differences between Trading and Non-trading Hours: Like Night and Day" (2008, SSRN 1004081) `[opened: secondary summary only]`. URL of summary: https://www.cxoadvisory.com/calendar-effects/buy-at-the-close-and-sell-at-the-open. 1993-2006: the US equity premium accrued overnight. Overnight-minus-daytime spread per day: 0.068% SPY, 0.061% DIA, 0.18% QQQQ; daytime returns negative for 12 of 14 high-volume ETFs. Costs not assessed. The same page notes a 2022 follow-up finding the gap weakened over the prior 5-10 years (not opened).
- Lou, Polk & Skouras, "A tug of war: Overnight versus intraday expected returns," Journal of Financial Economics 134(1), 2019 `[opened: abstract page of the LSE working-paper record]`. URL: https://researchonline.lse.ac.uk/id/eprint/119010. Momentum profits accrue almost entirely overnight; most other anomalies earn their returns intraday and give some back overnight. Cross-section of stocks.
- Bondarenko & Muravyev, "Market Return Around the Clock: A Puzzle," Journal of Financial and Quantitative Analysis 58(3), 2023, 939-967 `[opened: abstract page]`. URL: https://econpapers.repec.org/RePEc:cup:jfinqa:v:58:y:2023:i:3:p:939-967_1. In E-mini S&P futures, "4 hours around European open account for the entire average market return" (Sharpe 1.6, said to survive costs); the other 20 hours average about zero.
- Implication: we buy at an open and sell at an open, so every position holds equal numbers of day sessions and nights. We can neither harvest the overnight premium nor be hurt by missing it on a multi-day hold. The cost shows up elsewhere: a signal computed at the close and filled at the next open skips the first night. If the first night carries much of a short-term bounce, close-fill backtests of dip rules overstate what we get. This must be measured, not assumed.

---

## Verdict for this family

**Held up.** (1) The sign change in index autocorrelation: daily and weekly S&P 500 serial dependence has been negative since about 2000 (D1), which supports short-horizon dip-buying in SPY/QQQ in principle. (2) Crypto trend over reversal: where costs and large coins are checked (A3, A8, A11), trend survives and reversal does not. (3) BTC as a risk asset, not digital gold (C1, C2, A5). (4) Halloween survived one out-of-sample window to 2011 (E5), with no verification after that.

**Failed or decayed.** Daily mean reversion in BTC/ETH: not real for large liquid pairs even before our 60 bps (A3), opposite sign in A1, failed out of sample in A11. Crypto day-of-week and time-of-day effects: inconsistent across studies, not persistent (B1-B3). Pre-FOMC drift: gone after 2015 (E4). Plain turn-of-month: reported gone after 2001 (E2). Generic buy-the-dip on the S&P 500: worse Sharpe than buy-and-hold across 196 variants (D3). Cross-sectional crypto momentum and reversal factors: unstable across samples, driven by small coins or short legs, and not runnable with two coins anyway (A2, A4-A7, A9). Halving and on-chain rules: too few events to validate (B4, B5). Crypto carry and the overnight premium: real, but need instruments or fills we do not have (C3, E6).

**Most worth testing here, with concrete parameters.**
1. SPY/QQQ short-term dip rule, long-or-cash: entry RSI(2) < 5 and close below the 5-day average; exit on first close above the 5-day average or after 5 days; fills at next open; 2 bps a side. Optional filter: only when close is above the 200-day average. Report 1995-2007, 2008-2016, 2017-now separately, and compare Sharpe with buy-and-hold and with the same rule filled at the close.
2. Month-end liquidity window on SPY, QQQ, TLT: long from the open of T-3 to the open of T+4 (T = last trading day), flat or underweight over T-8..T-4. For TLT also try entry at the open of T-1. Split at 2001, 2013 and September 2017.
3. BTC/ETH: no daily reversal rule. If anything, a slow long-or-cash trend filter (price at a 10-20 day high, or weekly momentum), judged after 60 bps a round trip and against buy-and-hold. This overlaps the trend family.
4. Halloween tilt as a low-priority overlay: SPY/QQQ November-April, TLT/GLD rather than cash May-October. Two trades a year; accept that it cannot be validated statistically.

**Main traps.**
- Fill mismatch: almost every paper uses close-to-close returns. Our next-open fill skips the first overnight, which is where short-term bounces and the pre-FOMC window partly live.
- Long-short results quoted as if long-only. Check which leg earns the money; papers disagree (A8 versus A9).
- Sample era: crypto results from 2013-2018 are dominated by two bull runs; equity mean reversion is a post-1999 regime that can end the way positive autocorrelation did.
- Multiple testing: 196 dip variants in D3 yield 16 "significant" ones by construction of chance. Fix parameters from the literature before looking at our data.
- Cash earns 0: any rule that sits out of the market must beat buy-and-hold on Sharpe, not just be profitable.
- Clustering: dip signals in SPY, QQQ and crypto fire together in sell-offs, so they are one bet, not several.
- Turnover arithmetic in crypto: 60 bps a round trip means a weekly in-and-out costs about 31% a year. Only slow signals can work.

**Source count.** 33 sources opened (9 as full text, 21 as abstract or landing pages, 3 as practitioner articles) plus 1 read only through a secondary summary; 4 cited without opening and marked as such.
