# Lane lit: what the literature says about late-stage bubbles, tops and leaving them

Lane `lit`, exit research run, 2026-11-18. Research only. Status: first full draft (verification pass on remaining "from memory" items possible).

Decision this serves: a euro-based investor with a small stock portfolio wants to be fully out of
stocks by a fixed date (worked example: 31 Dec 2026, about 6 weeks away), avoid a bad sell day,
park crash-safe, and buy back after a possible bubble pop. Tax is out of scope.

Marking: "(verified)" = I opened the paper/page in this session and the number is from it.
"(from memory, well-known)" = standard citation I am sure of but did not reopen. "(unverified)" =
I could not confirm; do not lean on it.

## Bottom line (read this first)

1. **Nobody in the literature can date a top, and 6 weeks is noise.** The best predictors
   (valuation, sentiment, credit) work at 1-10 years and mostly fail out of sample even there
   (Goyal-Welch 2008, Goyal-Welch-Zafirov 2024). Over 6 weeks the expected drift is ~0.6-0.8% of
   the portfolio against a typical swing of ~5.4-6.8%. Plan to cap regret, not to forecast.
2. **Bubble features raise crash odds a lot, but the top comes later.** After a 100% (150%)
   two-year industry run-up, the chance of a 40% drawdown within 2 years was 53% (80%); rising
   volatility, issuance, acceleration and young-firm leadership raise it further. But in run-ups
   that did crash, prices kept rising ~6 months and ~30% after the signal (Greenwood-Shleifer-You).
   Whole markets crash after booms far less often (Goetzmann 2015).
3. **What works for exits is reacting, not predicting.** Trend rules (10-month SMA, 12-month
   momentum) got out of most slow bear markets for 130+ years (positive in 8 of the 10 worst
   60/40 drawdowns since 1880) at the cost of frequent whipsaws, and fail in 1987-style crashes.
   Stop-losses help only when markets trend (Kaminski-Lo). Volatility spikes are a reasonable
   confirmer (Moreira-Muir), weak out of sample alone.
4. **For an investor who must be out by a fixed date the whipsaw cost nearly vanishes**: the
   sale happens by 31 Dec anyway, so a trigger only moves the date earlier. Literature-consistent plan: staged selling (a part now,
   a part on a trend/drawdown trigger, the rest on a fixed fallback date), park in cash-like
   assets, and treat CAPE, concentration, LPPL, put/call and VIX-curve "top" calls as not
   actionable. Ranked shortlist: section 15. Rules for bt: section 16.

## 1. Greenwood, Shleifer & You (2019), "Bubbles for Fama"

**Claim.** A big industry run-up does not predict low *average* returns, but it sharply raises the
*probability of a crash*, and some features of the run-up separate the run-ups that crash from the
ones that keep going.

**Evidence (verified, NBER WP 23191, Feb 2017 version; the JFE version keeps the headline
numbers).**
- Sample: US industries 1928-2014 (40 episodes where the industry rose >100% over 2 years, both
  raw and net of market); out-of-sample check on international sectors 1985/87-2013/14 (107
  episodes).
- Crash = a 40% drawdown at any point in the next 24 months.
- Unconditional 2-year crash probability per industry-month: 14% (11% after 1970); international
  24%.
- Crash probability after a run-up of 50% / 100% / 150% (raw and net of market, 2 years): about
  20% / 53% / 80% in US industries (15 episodes at 150%); international 36% / 50% / 67% (51
  episodes at 150%).
- But average returns after a 100% run-up are about market-like: holding all run-up industries
  returned +7% after 1 year, 0% after 2 years, +5% after 4 years (compounded).
- **Timing is the hard part.** In the 21 US run-ups that did crash, prices on average *peaked 6
  months after* the run-up was first flagged, rising another *30%* in between. "At a horizon of
  one-year, it is virtually impossible to generate outperformance."
- Features of run-ups that crash (Table 4/5): bigger 1-year *increase* in volatility, more
  equity issuance (share of firms issuing >=5% new shares in the past year), *acceleration*
  (2-year return minus first-year return: how much of the rise came recently), a
  disproportionate rise of *young* firms (age tilt), rising market CAPE. Level of turnover is high
  in run-ups that crash *and* in those that do not: turnover does not help. Sales growth
  (fundamentals) does not help in the US.
- Exit strategies (Table 8, one characteristic at a time, sell to risk-free, never buy back):
  selling on volatility above the crash-episode mean flagged 20 candidates (60% crashed) and beat
  passive by 0 / 8 / 12 percentage points at 1 / 2 / 4 years. Volatility, firm age and
  acceleration each gave >=10 points over 2 years. Issuance flagged 13, of which 9 crashed, but
  missed 13 other crashes. Moving to cash beat moving to the broad market, because industry
  bubbles tend to coincide with broad rallies: "When an industry bubble is called correctly, it is
  best to avoid the stock market altogether." Industry bubbles also negatively predict the
  *market* return at 2 years (Internet Appendix).
- Caveat by the authors: only 40 US episodes; thresholds set at in-sample means (some
  look-ahead); results are at 2-4 year horizons.

**Out-of-sample record.** The international sample (built after the US one) confirms the crash
probability pattern and the value of volatility and issuance; outperformance is smaller.

**Use for a 6-week decision.** Low for timing, useful as a *risk flag*. It says (a) the risk of a
deep drawdown after a big, accelerating, issuance-heavy, young-firm run-up is very high, (b) the
peak typically comes months after the signal, so a 6-week window will on average still be in the
"still rising" phase, and (c) the crash risk argues for moving to cash, not to the broad index. It
does *not* give a sell date.

**Citation.** Greenwood, R., Shleifer, A., You, Y. (2019). Bubbles for Fama. *Journal of Financial
Economics* 131(1), 20-43. https://doi.org/10.1016/j.jfineco.2018.09.002 ; NBER WP 23191:
https://www.nber.org/papers/w23191

Related, the counterweight: **Goetzmann (2015), "Bubble investing: learning from history"**
(verified, NBER abstract). On a broad panel of world stock *markets* since the early 1900s, the
probability of a crash after a boom is "only slightly higher" than unconditionally; after a market
*doubled*, the chance it gave back all of the gain was about 10%. "Not all booms are bad."
GSY's high crash probabilities are for *industries* up >100% *net of the market*; for whole
national markets the base rate is far lower. Citation: Goetzmann, W. N. (2015). NBER WP 21693.
https://www.nber.org/papers/w21693

## 2. Riding the bubble and leaving it

**Brunnermeier & Nagel (2004), "Hedge funds and the technology bubble".**
- Claim (verified, abstract via LBS repository and JF listing): hedge funds did *not* lean against
  the Nasdaq bubble; they were heavily overweight tech, captured the upturn, and by cutting
  positions in stocks that were about to fall avoided much of the downturn. Consistent with
  "riding the bubble" when sentiment is predictable and arbitrage is limited.
- Detail (partly verified, from search snippets of the paper, not reopened): hedge-fund tech
  exposure peaked around **September 1999, about 6 months before the March 2000 top**; the
  exit was gradual, stock by stock, not one sell date. (From memory, well-known, in the paper:
  Tiger (Robertson) refused to ride and closed in March 2000 right at the top; Soros's Quantum
  re-bought tech late and lost heavily in spring 2000.) Lesson: even the best-informed did not
  call the day; the winners scaled out over months.
- Data: 13F holdings, 1998-2000. Sample is one bubble: no out-of-sample record as a rule.
- Use for 6 weeks: supports *staged* exit and "sell into strength while the trend is still up"
  over waiting for a clean top signal.
- Citation: Brunnermeier, M. K., Nagel, S. (2004). *Journal of Finance* 59(5), 2013-2040.
  https://doi.org/10.1111/j.1540-6261.2004.00690.x

**Abreu & Brunnermeier (2003), "Bubbles and crashes"** (from memory, well-known).
- Theory: rational arbitrageurs learn *at different times* that prices are too high and cannot
  coordinate a joint exit; each wants to ride as long as possible and get out just before the
  others. The bubble survives long after "everyone knows", and the crash needs either enough
  sellers or a synchronising event; **minor news can trigger a large crash**.
- Implication: there is no reliable public "top" signal by construction; once a top is obvious,
  it is already in the price. Exits are a race, so rules must be fast and pre-committed.
- Citation: Abreu, D., Brunnermeier, M. K. (2003). *Econometrica* 71(1), 173-204.
  https://doi.org/10.1111/1468-0262.00393

**Temin & Voth (2004), "Riding the South Sea bubble"** (from memory, well-known): Hoare's Bank
knowingly bought into the 1720 bubble and sold out at a profit, the same "ride and exit" pattern.
*American Economic Review* 94(5), 1654-1668. https://doi.org/10.1257/0002828043052268

## 3. Valuation: CAPE and the dividend/earnings yield

**Claim.** High valuations predict low returns over 5-10+ years; over months they predict almost
nothing.

**Evidence.**
- Campbell & Shiller (1988, 1998) (from memory, well-known): the price/10-year average earnings
  ratio (CAPE) and the dividend yield forecast real returns at 10-year horizons with large R²;
  short horizons small. Campbell & Shiller presented this to the Fed Board on 3 Dec 1996; two days
  later came Greenspan's "irrational exuberance" speech.
- The cost of being early (verified, quoted in GSY 2017 from Fama 2014): after Shiller "called"
  the bubble in Dec 1996, prices *doubled*; "at its low, in 2003, US stock price index was higher
  than when Shiller first called the bubble". So on price alone, a seller in Dec 1996 had to buy
  back *higher* even at the exact 2002 low; only cash interest over ~6 years (about 5%/yr then,
  from memory) made the early call pay, and only with near-perfect re-entry.
- Size of the one-year link (from memory, well-known, Cochrane 2011 presidential address, Table
  1, annual US data 1947-2009): dividend yield regression R² about 0.09 at 1 year, rising to
  about 0.3 at 5 years. Secondary sources give CAPE one-year R² anywhere from about 0.05 to 0.27
  depending on sample (unverified; search snippets only). At 6 weeks the R² is a fraction of the
  annual one.
- **Out-of-sample: Goyal & Welch (2008)** (from memory, well-known): the classic predictors
  (dividend/earnings yields, book-to-market, term and default spreads, inflation, issuance...)
  mostly *fail to beat the historical mean* out of sample, and were unstable even before the
  1990s bubble. **Goyal, Welch & Zafirov (2024)** (verified, abstract): re-test of 29 newer
  variables from 26 papers plus the original 17, data to end-2021: more than a third lose
  significance even in-sample; of those still significant in-sample, about half predict poorly
  out-of-sample; only "a few" still work reasonably in and out of sample.
- **Campbell & Thompson (2008)** (verified, NBER abstract): with sensible restrictions (sign of
  the coefficient, no negative premium forecasts) many predictors do beat the historical mean
  out of sample, but the gain is "small"; monthly out-of-sample R² is well under 1% (from memory,
  well-known magnitude). A good predictor can also look bad for a long stretch.

**Use for 6 weeks.** Practically none as a trigger. CAPE is historically very high in late 2026
(bt lane / data lanes have the reading), which is a reason for a *lower long-run expected
return* and a reason an investor may want less equity, not a reason to expect a fall before 31 Dec.
No defensible CAPE sell threshold exists for a 6-week horizon.

**Citations.**
- Campbell, J. Y., Shiller, R. J. (1988). Stock prices, earnings, and expected dividends. *Journal
  of Finance* 43(3), 661-676. https://doi.org/10.1111/j.1540-6261.1988.tb04598.x
- Campbell, J. Y., Shiller, R. J. (1998). Valuation ratios and the long-run stock market outlook.
  *Journal of Portfolio Management* 24(2), 11-26. https://doi.org/10.3905/jpm.24.2.11
- Goyal, A., Welch, I. (2008). A comprehensive look at the empirical performance of equity premium
  prediction. *Review of Financial Studies* 21(4), 1455-1508. https://doi.org/10.1093/rfs/hhm014
- Goyal, A., Welch, I., Zafirov, A. (2024). A comprehensive 2022 look at the empirical performance
  of equity premium prediction. *Review of Financial Studies* 37(11), 3490-3557.
  https://doi.org/10.1093/rfs/hhae044
- Campbell, J. Y., Thompson, S. B. (2008). Predicting excess stock returns out of sample: can
  anything beat the historical average? *Review of Financial Studies* 21(4), 1509-1531.
  https://doi.org/10.1093/rfs/hhm055 ; NBER WP 11468: https://www.nber.org/papers/w11468
- Cochrane, J. H. (2011). Presidential address: Discount rates. *Journal of Finance* 66(4),
  1047-1108. https://doi.org/10.1111/j.1540-6261.2011.01671.x

## 4. How predictable is a ~6-week window?

**Claim.** Barely at all. Every predictor above has its best R² at multi-year horizons; at 1
month the best out-of-sample R² values in the literature are around or below 1%.

**What that means in euros (my arithmetic, standard assumptions, not from a paper).** With equity
volatility of ~16-20% a year, the standard deviation of a 6-week return is about
16-20% x sqrt(6/52) = **5.4-6.8%**; the expected 6-week return at a 5-7% annual equity premium
is about **+0.6-0.8%**. So the typical swing is roughly **5.4-6.8% of the portfolio** either way
versus an expected drift of about **0.6-0.8%**. A signal with a 1% R² shifts the expected value by
a tiny fraction of a percent. The sell date will mostly be luck; the plan should cap regret, not chase a forecast.

**Implication.** Rules that *cut tail exposure* (trend breaks, drawdown stops) are defensible
because they act *after* the market reveals a regime; rules that claim to *predict* a top
inside 6 weeks are not.

## 5. Breadth and narrow leadership (concentration)

**Claim (popular).** Rallies led by a few mega-caps with weak breadth precede tops.

**Evidence.**
- **Kritzman & Turkington, "The Fallacy of Concentration"** (verified via a detailed Quantpedia
  summary; SSRN 5436695, 2025; paper itself not opened): US, 49 Ken French industries, Jul 1926
  - Jun 2025, concentration measured as effective number of stocks; in panel regressions
  concentration explains "virtually none" of the variation in future returns; a rule that
  invests less when concentration is high *lowered* returns and *raised* risk versus buy-and-hold
  at the same average exposure. They note the S&P 500 is the most concentrated since at least
  1998.
- Practitioner studies (CFA Institute blog, Hartford, Schroders) find that high top-10
  concentration preceded *equal-weight beating cap-weight* over the next 5 years (e.g. 88% of
  5-year windows after the most concentrated periods, 1964-2024: secondary, unverified). That is a
  *relative* (which stocks) result over years, not a market-timing signal.
- Advance/decline divergences, "% of stocks above the 200-day", the "Hindenburg Omen": I found
  **no peer-reviewed out-of-sample support** for these as market-top timers (absence of
  evidence after a short search, not proof).

**Use for 6 weeks.** Not a trigger. If anything, concentration argues for *what* to hold after
re-entry (equal-weight/broad), not *when* to sell.

**Citation.** Kritzman, M., Turkington, D. (2025). The fallacy of concentration. SSRN 5436695.
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5436695 ; summary:
https://quantpedia.com/the-fallacy-of-concentration-risk/

## 6. Credit spreads

**Gilchrist & Zakrajšek (2012): the excess bond premium (EBP).**
- Claim (partly verified via NBER Reporter 2018 and a Fed FEDS Note summary; AER paper from
  memory): splitting corporate bond spreads into expected default and a residual "excess bond
  premium" (the price of bearing credit risk), the EBP is a strong *leading indicator of
  recessions* and of economic activity; post-1985 it captures most of the variation in recession
  probabilities and flagged the 2007-09 recession well. The Fed publishes the EBP monthly.
- Stock-return timing: the papers are about the real economy; I did **not** find evidence of a
  stock-market sell threshold on EBP (unverified for equity timing).
- Citation: Gilchrist, S., Zakrajšek, E. (2012). Credit spreads and business cycle fluctuations.
  *American Economic Review* 102(4), 1692-1720. https://doi.org/10.1257/aer.102.4.1692 ; data
  and note: https://www.federalreserve.gov/econresdata/notes/feds-notes/2016/recession-risk-and-the-excess-bond-premium-20160408.html

**López-Salido, Stein & Zakrajšek (2017): credit-market sentiment.**
- Claim (verified via working-paper abstract; QJE version from memory): *very low* credit spreads
  and frothy issuance (elevated credit-market sentiment) in year t-2 predict a widening of spreads
  and weaker activity in years t and t+1, through predictable mean reversion. US data from 1929.
  Note: tight spreads are the *warning*, widening spreads are the *event*.
- Citation: López-Salido, D., Stein, J. C., Zakrajšek, E. (2017). Credit-market sentiment and the
  business cycle. *Quarterly Journal of Economics* 132(3), 1373-1426.
  https://doi.org/10.1093/qje/qjx014

**Use for 6 weeks.** Medium as a *confirming* stress signal: a quick rise in high-yield spreads
or the EBP alongside a price break makes "regime change" more likely than "noise". No
literature-backed numeric threshold for selling stocks; any number (e.g. HY OAS +100 bp in 1-3
months) is a heuristic that bt must test.

## 7. Sentiment indices

- **Baker & Wurgler (2006, 2007)** (from memory, well-known): when their sentiment index (closed-end
  fund discount, turnover, IPO count and first-day returns, equity share in issuance, dividend
  premium) is high, *subsequent* returns are low for speculative stocks (young, small,
  unprofitable, high-volatility, non-payers) relative to safe ones. That is a cross-section
  result at 1-year-ish horizons, not a market-day signal. JF 61(4), 1645-1680,
  https://doi.org/10.1111/j.1540-6261.2006.00885.x ; JEP 21(2), 129-152,
  https://doi.org/10.1257/jep.21.2.129
- **Huang, Jiang, Tu & Zhou (2015), "Investor sentiment aligned"** (partly verified via abstract
  listings): a PLS-cleaned version of the same proxies predicts the *aggregate* monthly market
  return in and out of sample, 1965-2010, with R² several times Baker-Wurgler's; exact OOS R²
  not verified (secondary sources conflict). *RFS* 28(3), 791-837.
  https://doi.org/10.1093/rfs/hhu080 . Even if R² is a few percent monthly, see section 4.
- **AAII bull-bear survey** (from memory): Fisher & Statman (2000) find individual-investor
  sentiment is a *contrarian* indicator for subsequent S&P 500 returns; the effect is modest and
  noisy. *Financial Analysts Journal* 56(2), 16-23. https://doi.org/10.2469/faj.v56.n2.2340
- **Put/call ratio**: the robust academic result (Pan & Poteshman 2006, RFS 19(3), 871-908,
  https://doi.org/10.1093/rfs/hhj024, from memory) is for *individual stocks* using non-public
  open-buy volume; I found no solid evidence that the public index put/call ratio times the
  market (unverified/absent).
- IPO and issuance waves: covered by lane reentry.

**Use for 6 weeks.** Low. Euphoric readings raise long-run risk, especially for speculative/AI
names, but give no date. No defensible threshold.

## 8. Trend-following exits

**Faber (2007), 10-month SMA.**
- Rule: at each month end, hold the index if price > its 10-month simple moving average, else
  cash (verified, rule from Faber's own page; he notes the result is broadly stable for 3 to 12+
  month averages and that 10 months is close to a 200-day average).
- Evidence (unverified, from secondary summaries of the 2013 update; paper not opened): S&P 500
  1901-2012, compounded return 10.18%/yr timing vs 9.32% buy-and-hold, invested ~70% of the
  time, fewer than one round trip a year, the 1930s drawdown cut from ~84% to ~42%, much lower
  volatility. The gain comes from sidestepping a few long bear markets (1929-32, 1973-74,
  2000-02, 2008-09); in-sample, no costs or taxes.
- Citation: Faber, M. T. (2007). A quantitative approach to tactical asset allocation. *Journal
  of Wealth Management* 9(4), 69-79. https://doi.org/10.3905/jwm.2007.674809 ; SSRN 962461:
  https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461

**Moskowitz, Ooi & Pedersen (2012), time-series momentum.** (Verified, abstract via JFE/SSRN
listings.) Significant time-series momentum in each of 58 liquid futures (equity indices,
currencies, commodities, bonds); a diversified portfolio earns abnormal returns with little factor
exposure and does best in *extreme* markets. Returns persist "for one to 12 months" and then
partially reverse over longer horizons (verified, abstract from the full text). The standard
signal is the sign of the past 12-month excess return. *JFE* 104(2),
228-250. https://doi.org/10.1016/j.jfineco.2011.11.003

**Hurst, Ooi & Pedersen (2017), a century of trend following.** (Verified, full text opened.)
- 67 markets, Jan 1880 - Dec 2016; 1-, 3- and 12-month signals, 10% vol target.
- Positive returns in every decade; average Sharpe per market about 0.4; low correlation with
  stocks and bonds; the decades before 1985 are out-of-sample relative to MOP 2012.
- In the **10 largest 60/40 drawdowns since 1880, trend following was positive in 8 of 10**.
- Why: the average peak-to-trough length of those drawdowns was **about 15 months**, so trend
  signals have time to flip. It "may not perform well in bear markets that occur very rapidly,
  such as the 1987 stock market crash". Its own worst periods are sharp reversals.
- Lagging the signal one month hurts, especially for short lookbacks: speed of execution matters.
- *Journal of Portfolio Management* 44(1), 15-29. https://doi.org/10.3905/jpm.2017.44.1.015 ;
  AQR copy: https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing

**Whipsaw and the honest out-of-sample record: Zakamulin (2014).** (Partly verified: abstract
via Springer/RePEc; numbers from a CXO summary of the 2013 version.) Reported MA/momentum
timing performance is "suspiciously" strong; with out-of-sample parameter choice and realistic
costs it is much lower. S&P 500, 1930-2012, 0.5% costs: Sharpe gain of only about 7-12% over
buy-and-hold; in about **80% of the out-of-market spells the timer underperformed buy-and-hold**
(whipsaw); all of the benefit comes from a few severe bear markets. *Journal of Asset
Management* 15(4), 261-278. https://doi.org/10.1057/jam.2014.25

**Use for 6 weeks.** The best-supported *exit* tool, with known costs: it will not sell the top
and will often sell before a rebound (whipsaw), but it reliably gets out of the slow, deep bear
markets that bubble bursts usually are (2000-02 took 31 months; 2007-09 17 months). For an
investor who must be out by a fixed date the whipsaw cost is small, because the sale happens before
31 Dec anyway: a trend break simply moves the sell date earlier. Within a 6-week window, the monthly rule only checks twice (30
Nov, 31 Dec), so a daily variant (close below 200-day average) is the practical form; its
threshold has less academic backing than the monthly 10-month rule.

## 9. Volatility regimes

**Moreira & Muir (2017), volatility-managed portfolios.** (Verified, NBER abstract.) Scaling
exposure by the inverse of last month's realized variance raises Sharpe ratios and gives large
alphas for the market and many factors, because volatility rises without a matching rise in
expected returns: take less risk in crises. *Journal of Finance* 72(4), 1611-1644.
https://doi.org/10.1111/jofi.12513 ; NBER WP 22208: https://www.nber.org/papers/w22208

**Out-of-sample critique: Cederburg, O'Doherty, Wang & Yan (2020).** (Partly verified via
abstract listings/summaries.) Across 103 equity strategies, real-time implementable versions do
*not* reliably beat the unmanaged ones; out-of-sample they had lower Sharpe ratios and certainty
equivalents for most strategies, because the in-sample regressions are unstable. *JFE* 138(1),
95-117. https://doi.org/10.1016/j.jfineco.2020.04.015

**VIX term structure.** Johnson (2017) (verified, abstract listing): the slope of the VIX term
structure carries information about the *variance risk premium*, i.e. returns on variance swaps,
VIX futures and straddles, not reliably about the S&P 500 itself. An inverted VIX curve
(front > back) marks stress *already under way*. *JFQA* 52(6), 2461-2490.
https://doi.org/10.1017/S0022109017000825 . I found no peer-reviewed evidence that inversion is a
good *equity sell* signal (unverified/absent); historically high-VIX periods are often followed
by *above*-average equity returns, which cuts against selling into a spike.

**Use for 6 weeks.** Medium as a *risk-reduction* signal combined with trend: a jump in realized
volatility after a long calm is exactly the GSY "volatility increase" feature and the Moreira-Muir
"cut risk" condition. No defensible universal number; any threshold (e.g. 21-day realized vol
above 2x its 1-year median, or VIX > 30) is a heuristic for bt to test.

## 10. LPPL (Sornette) bubble prediction

- Claim: a bubble shows super-exponential growth with accelerating log-periodic oscillations;
  fitting the log-periodic power law gives a "critical time" t_c, the most probable end of the
  bubble (from memory, well-known: Johansen, Ledoit & Sornette 2000, *IJTAF* 3(2), 219-255,
  https://doi.org/10.1142/S0219024900000115). ETH Zurich's Financial Crisis Observatory publishes
  LPPLS "confidence" indicators.
- Record: proponents report real-time successes (Shanghai 2015, Sornette et al., *Journal of
  Investment Strategies*, 2015) and claim low false-positive rates on synthetic data. Critics:
  Bree & Joseph (verified, arXiv abstract): on 11 Hang Seng crashes 1970-2008 only 7 fits had
  parameters in the ranges proposed *after the fact*, and the claimed mechanism holds for only
  about half of previously reported bubbles. A 2025 *IRFA* paper (unverified details) argues
  published false-positive rates are understated. Sornette's own papers note t_c is a most
  probable time and a bubble can end without a crash. **No systematic, public, out-of-sample hit
  and false-alarm record** for live FCO calls that I could find.
- Use for 6 weeks: low. Fits are unstable (small changes in window move t_c by months). Do not
  put LPPL in the playbook; at most a curiosity.
- Citation (critique): Bree, D. S., Joseph, N. L. (2013). Testing for financial crashes using the
  log periodic power law model. *International Review of Financial Analysis* 30, 287-297
  (journal details from memory). arXiv: https://arxiv.org/abs/1002.1010

## 11. PSY / GSADF real-time bubble detection

- Claim (verified via abstract listings): Phillips, Shi & Yu (2015) generalise the recursive
  right-tailed unit-root test (sup ADF) to GSADF with flexible windows and a *real-time*
  date-stamping procedure (backward SADF). On the S&P 500 price/dividend ratio, Jan 1871 - Dec
  2010, it picks up the known episodes (incl. the 1990s) better than earlier methods.
  Phillips, Wu & Yu (2011) (from memory) date the start of Nasdaq explosiveness to the mid-1990s,
  years before the 2000 top.
- Out-of-sample/usability: it is a test that the price is *explosive*, i.e. a bubble is
  *forming*; it is good at dating the start, says nothing about *when* it ends, and the end is
  dated only once the explosive statistic falls back below its critical value, i.e. after prices
  have already turned. Monthly data and choice of fundamentals (dividends, earnings) matter.
- Use for 6 weeks: low as a top-timer; possible as an *exit-when-explosiveness-ends* rule, which
  in practice behaves like a trend rule. Tools exist (R `psymonitor`, `exuber`).
- Citations: Phillips, P. C. B., Shi, S., Yu, J. (2015). Testing for multiple bubbles: historical
  episodes of exuberance and collapse in the S&P 500. *International Economic Review* 56(4),
  1043-1078. https://doi.org/10.1111/iere.12132 ; Phillips, P. C. B., Wu, Y., Yu, J. (2011).
  Explosive behavior in the 1990s Nasdaq: when did exuberance escalate asset values?
  *International Economic Review* 52(1), 201-226. https://doi.org/10.1111/j.1468-2354.2010.00625.x

## 12. Stop-loss rules: Kaminski & Lo

- Claim (verified via RePEc abstracts of both versions): a simple 0/1 stop-loss rule (exit after
  cumulative losses pass a threshold, re-enter later) **always lowers expected return if prices
  are a random walk**; it can **add value when returns have momentum** or regime switches
  ("flight to quality" episodes).
- Evidence: working paper (2008): US equities with long-term US government bonds as the
  stop-out asset, monthly Jan 1950 - Dec 2004: certain rules added **50-100 bp per month during
  stop-out periods**. Published version (2014): daily index futures; at longer sampling
  frequencies some rules raise expected return while substantially cutting volatility.
- Caveat: the 1950-2004 stop-out asset (long Treasuries) had a strong flight-to-quality behaviour
  that may not hold (2022 showed stocks and bonds falling together). The gain is per stop-out
  month, not per year of holding.
- Use for 6 weeks: medium. Supports a pre-committed drawdown trigger as one exit leg; the exact
  threshold is not pinned down by the paper in a way I could verify (they test a grid).
- Citation: Kaminski, K. M., Lo, A. W. (2014). When do stop-loss rules stop losses? *Journal of
  Financial Markets* 18, 234-254. https://doi.org/10.1016/j.finmar.2013.07.001 ; WP:
  https://ideas.repec.org/p/hhs/sifrwp/0063.html

## 13. Market timing overall

- **Newsletters: Graham & Harvey (1996)** (verified via abstract listings): 237 newsletter
  strategies, 1980-1992; no evidence they raised equity weights before rises or cut them before
  falls. A 1997 *FAJ* follow-up (326 letters, 1983-95) agrees for the group. *JFE* 42(3),
  397-421. https://doi.org/10.1016/0304-405X(96)00878-1 ; NBER WP 4890:
  https://www.nber.org/papers/w4890
- **Investors' actual timing: Dichev (2007)** (abstract verified, numbers from a secondary
  summary): dollar-weighted (actual investor) returns trail buy-and-hold by about 1.3%/yr on
  NYSE/AMEX 1926-2002, **5.3%/yr on Nasdaq 1973-2002** (money poured in near the 2000 top), and
  1.5%/yr internationally. *AER* 97(1), 386-401. https://doi.org/10.1257/aer.97.1.386
- **Dalbar QAIB caveat** (from memory): Dalbar's widely quoted "investor return gap" of several
  percent a year uses a method critics consider flawed (it compares a lump sum with periodic
  flows), overstating the gap; Morningstar's "Mind the Gap" fund-flow estimates are about 1%/yr
  (unverified exact value). Use Dichev/Morningstar, not Dalbar.
- **Shiller 1996**: see section 3: a correct long-run call, years early.
- Overall: the literature supports *rules that reduce exposure after a regime change* (trend,
  volatility) much more than *forecasting tops*. Discretionary timing has a poor record.

## 14. Lump sum vs staged selling and buying

- **Constantinides (1979)** (verified as cited in Vanguard 2023): dollar-cost averaging is
  dominated by a policy that decides each period on the information then available; a fixed
  staging schedule is suboptimal. *JFQA* 14(2), 443-450. https://doi.org/10.2307/2330513
- **Vanguard (2023), Finlay & Zorn, "Cost averaging: invest now or temporarily hold your cash?"**
  (verified, full text opened): MSCI World and US bonds 1976-2022 (plus other markets): lump-sum
  investing beat a 3-month cost-averaging plan **68%** of the time (65% for all-equity even with
  T-bill interest on the waiting cash); 60/40 average ending value USD 109,360 lump sum vs
  107,453 staged (+1.8%); longer staging = bigger shortfall. Staging wins in the worst 5th
  percentile (crashes) and lowers regret; "investors with higher loss aversion would be better
  off with CA". https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf
- **Applied to a forced sale by a fixed date (my reading).** The same logic runs in reverse for *selling*: because
  stocks have a positive expected premium, staying invested longer is better *on average*, and
  selling all now is the "de-risk now" choice. Over 6 weeks the expected cost of selling early is
  tiny (section 4: about 0.6-0.8% of the portfolio), while the spread of outcomes is about 10x larger.
  So: (a) selling in 2-3 tranches (e.g. one now, one on a trigger, rest by the fallback date)
  costs almost nothing in expectation and cuts the regret of "sold the day before a +5% week" or
  "waited into the crash"; (b) on re-entry, Vanguard's evidence favours buying back in one go
  or over a short window (<=3 months) once the plan says so, rather than a long DCA, unless loss
  aversion dominates.

## 15. Ranked shortlist for the fast-exit playbook

Ranking = strength of evidence x usability inside 6 weeks.

| Rank | Indicator | Threshold the literature supports | Evidence quality |
|---|---|---|---|
| 1 | Trend break on the index you hold (or S&P 500 / MSCI World / OSEBX) | Monthly: month-end close < 10-month SMA (Faber). Daily practical form: close < 200-day SMA (no paper pins a band; 1-3% band and/or 2-day confirmation is a heuristic to cut whipsaw). 12-month return < 0 (MOP) is the slower version. | Strong long-run (HOP 1880-2016, 8 of 10 big drawdowns positive), but most exits are whipsaws (~80% of out-spells, Zakamulin); misses 1987-style crashes. |
| 2 | Drawdown stop | Kaminski-Lo: stop-loss adds value only under momentum/regime switching; no single verified threshold. Heuristic: -8 to -10% from the recent high on the index you hold. | Medium; theory clear, threshold not pinned down. |
| 3 | Volatility spike after calm | Moreira-Muir: cut exposure when realized variance is high. No universal number; heuristic: 21-day realized vol > ~2x its 1-year median, or VIX > 30, *together with* rank 1 or 2. | Medium in-sample, weak out-of-sample (Cederburg et al.). Use as a confirmer, not alone. |
| 4 | Credit stress | HY spread or EBP rising quickly (EBP: GZ 2012; LSZ 2017). No equity-sell threshold in the literature. | Medium for recessions; untested here for 6-week equity exits. |
| 5 | GSY run-up features (AI/semis industry) | Industry 2-yr return > 100% raw *and* net of market; plus rising 1-yr volatility, issuance, acceleration, young-firm tilt. Means: elevated crash risk *within 2 years*; the peak came ~6 months (+30%) later on average. | Good (40 US + 107 intl episodes), but a background risk flag, not a date. |

**No defensible threshold / not supported for a 6-week decision:**
- CAPE or any valuation level (good at 10 years, near-useless at 6 weeks; Goyal-Welch OOS failure).
- Market concentration / narrow breadth (Kritzman-Turkington: no predictive power; acting on it
  lowered returns). A/D-line divergences, Hindenburg Omen: no peer-reviewed support found.
- LPPL / "critical time" forecasts (unstable fits, no public live hit-rate).
- PSY/GSADF as a *top* timer (dates the start, not the end).
- Put/call ratio, AAII bull-bear spread (weak, noisy contrarian at best).
- VIX term-structure inversion as a sell signal (it measures stress already present; high VIX
  periods often precede good returns).
- Seasonality (Nov-Apr "Halloween" strength; Bouman & Jacobsen 2002, *AER* 92(5), 1618-1635,
  https://doi.org/10.1257/000282802762024683, from memory): if anything, a weak reason *not* to
  rush; too weak to plan around.
- Newsletter or pundit "top" calls (Graham-Harvey: no timing skill).

**What the literature says about the decision as a whole.** Nobody can date the top; the best
evidence supports (1) a pre-committed exit on a regime break (trend/drawdown, confirmed by
volatility or credit), (2) staged selling to cap regret, since 6-week returns are mostly noise,
and (3) a firm fallback date. Bubble features raise the odds of a large fall over 1-2 years, but
the median path after such signals still rose for months (GSY: +30% over ~6 months; Shiller 1996:
prices doubled). Holding cash rather than the broad index after an industry-bubble call was the
better parking choice in GSY.

## 16. For bt lane (suggested tests)

1. **Monthly 10-month SMA** (Faber) and **12-month TSMOM** on S&P 500 TR, MSCI World (EUR),
   OSEBX, Nasdaq-100: entry/exit dates in 1987, 2000-02, 2007-09, 2018 Q4, 2020, 2022; count
   whipsaws.
2. **Daily 200-day SMA** with bands 0/1/2/3% and 1-/2-day confirmation: same episodes, plus
   whipsaw count per year.
3. **Kaminski-Lo stop**: exit if cumulative return over the last J months < -gamma (gamma 5-15%,
   J 1-6), re-enter when it recovers by delta; also the simple "-X% from 52-week high" stop.
4. **Vol trigger**: 21-day realized vol > k x 252-day median (k 1.5-2.5); alone and as a
   confirmer of 1-3.
5. **Credit confirmer**: ICE BofA US HY OAS (FRED `BAMLH0A0HYM2`) change over 1-3 months
   > +50/+100/+150 bp; EBP from the Fed's FEDS Notes CSV.
6. **GSY flags** for the AI-exposed industry (semis / tech hardware / software, Ken French 49
   industries or SOX): 2-year raw and net-of-market return vs 100%; acceleration (R(t-24,t) -
   R(t-24,t-12)); 1-year change in volatility; report the current reading.
7. **The investor's real question**, for each rule: draw many random 6-week windows ending on a
   forced-sale date (31 Dec analogue). Compare the sale price under "rule, else fallback date"
   vs "sell all on day 1" vs "3 equal tranches" vs "sell all on the fallback date": mean,
   median, 5th percentile, and probability of beating day-1. Expect means to be within ~1% of
   each other and the tails to differ; that is the trade-off to show the investor.
8. **"Sell when up" rule**: limit-sell at +3%/+5% above the starting price, else fallback date.
   (Momentum/52-week-high literature suggests new highs are not followed by below-average
   returns; test, don't assume.)
9. Optional: GSADF/BSADF on S&P 500 and Nasdaq-100 price/dividend (R `exuber`), exit when BSADF
   falls back below its 95% critical value after an explosive spell: compare with rule 1.

## 17. Not verified in this session (do not lean on these without a check)

- Faber 10-month SMA performance numbers (secondary summaries only; SSRN blocked).
- Kaminski-Lo exact thresholds/lookbacks that produced the 50-100 bp/month (abstract only).
- Brunnermeier-Nagel: "tech exposure peaked Sept 1999" (search snippet), Tiger/Quantum details
  (memory).
- Zakamulin's "80% of out-spells underperform" and 7-12% Sharpe gain (CXO summary).
- Dichev's 1.3% / 5.3% / 1.5% gaps (secondary summary); Dalbar critique and Morningstar ~1%
  (memory).
- Huang-Jiang-Tu-Zhou out-of-sample R² (sources conflict); Fisher-Statman AAII result (memory).
- CAPE one-year R² range; Cochrane 2011 R² values (memory).
- Concentration paper read through a summary, not the SSRN text; practitioner 88% figure.
- LPPL 2025 IRFA false-positive critique (search snippet); Bree-Joseph journal details (memory).
- Publisher pages (Wiley, Elsevier, SSRN, MIT DSpace) refused automated fetches; all DOIs above
  were checked to resolve (HTTP 302 at doi.org), which confirms they exist, not every detail.
