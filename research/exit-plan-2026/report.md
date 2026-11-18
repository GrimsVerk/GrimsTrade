# Selling a stock portfolio by a fixed date: exit plan, parking and re-entry

Report of the exit-plan-2026 research run, written 2026-11-18 and revised after review round 1
(`review-log.md`).

The scenario: a euro-based retail investor living in the Netherlands, with a small stock
portfolio (index funds and shares), wants to be fully out of stocks by a fixed date (the worked
example uses 31 Dec 2026), avoid a bad sell date, park the cash safely in euros against a crash
(short run included), and buy back in later. The rules are applied per holding type: a US or
global index fund, a tech or Nasdaq fund, a share or fund on a smaller non-euro market (Oslo
Børs is the tested example), and single shares.

This is research help, not financial advice. It lays out evidence, options and rules you can
choose to follow. You place every order yourself. The market readings are an example from the
Wed 18 Nov 2026 US and Oslo closes (refreshed 22:12 UTC that day, after the VIX close); every rule is written so that you
apply it to the readings on the day you act (section 5 says how to refresh them). "(unverified)"
marks anything no source in this run confirmed. Section 11 maps every part to the lane note,
script and logged test behind it.

## 1. Summary

> **The playbook in five steps** (details and a checklist in section 6)
>
> 1. **Your start day (e.g. Thu 19 Nov):** for each holding, look at the last close of the index
>    it follows (table 5.2). Below its 200-day average: sell all of that holding. Above: sell
>    half. (At the 18 Nov closes the US and tech indexes were below, the S&P by only 0.31%,
>    and Oslo was above. Check again the evening before.)
> 2. **The rest:** sell on the trading day after the index first closes below its 200-day
>    average, or on the fallback day, whichever comes first. Shares: fallback
>    **Fri 18 Dec**, last safe day **Mon 21 Dec**. Funds: fallback **Fri 11 Dec**, order in
>    before the fund's cut-off; last safe Tue 15 or Wed 16 Dec for a fund whose cash reaches
>    your broker within 2-6 business days of the order. A slow fund (cash at the broker within
>    5-10 business days): fallback **Fri 4 Dec**, last safe Wed 9 Dec (section 6.2, step 3).
> 3. **Each time cash lands:** if it settled in another currency, convert it to euros the same
>    day and move it to your Dutch account. Do not hold the other currency while you wait.
> 4. **Park it in euro cash:** a Dutch savings account under the deposit guarantee, or a euro
>    overnight-rate or 0-1 year government-bond ETF at the Dutch broker you will buy back with.
>    Not gold, Berkshire, long bonds or anything in dollars.
> 5. **Buy back** in 12 equal monthly buys, January to December 2027. In the past high-valuation
>    months that fit today this had a better typical result and a milder bad tail than waiting
>    for falls. Only as a bet that a real bust comes: a third each time a month-end close of the
>    S&P 500 is 20%, 30% and 40% below its high (about 6,255, 5,473 and 4,691), the rest by
>    **Fri 29 Dec 2028**; it paid 1.4-1.6 times in real busts and cost more otherwise (section 8.2).

What the evidence says, in short:

- **Nobody can date a top.** The warning signs in the literature (valuation, industry run-ups,
  issuance, sentiment, credit) work over years; only trend rules act within weeks, and only after
  the turn (section 2). No investor with a documented record timed a top to the month; those who
  did well scaled out (section 3). Over six weeks the expected gain is about 0.6-0.8% of the
  amount, against a typical swing of about 5.4-6.8%.
- **Selling in two steps passed our pre-set test (the 200-day speed-up added later is post
  hoc); how firm that is depends on the holding.**
  Oslo holdings fit the test's own sample: half now and half later cut the chance of ending more
  than 5% worse than "sell all now" from 9% (waiting to the fallback) to 1% (only 10 separate
  spells, 2013-2025). US and tech holdings
  fit only a sample defined after seeing today's data: there staging cut it from 11% to 2%
  (S&P 500) and from 16% to 5% (Nasdaq). Selling a US/tech holding in full gives up about
  0.7-1.4% of expected drift against plain staging, a fraction of a percent against the tested
  200-day rule, and buys a certain price (section 6.1).
- **"Sell only at a higher price" is the risky choice.** It gets the higher price about two
  times in three, but when a fall comes it ends up selling low (-8 to -9% on average).
- **Where things stood at the 18 Nov closes (refresh before acting):** S&P 500 0.31% below its
  200-day average (second close below; 6.3% below its 6 Oct high), Nasdaq 2.9% below (11.5% off
  its high), MSCI World ETF 1.0% below, Oslo's OSEBX 3.2% above. VIX 24.6 with a slightly
  inverted VIX curve; credit calm; CAPE 39.4, near its record.
- **Euro cash lost at most about 0.5%** in any crash measured (an overnight-rate ETF in 2020,
  from negative rates); every other candidate lost far more in some crash. Gold fell 22% (in
  dollars) within the Lehman weeks of 2008; Berkshire fell 54% in 2007-09 (in dollars); long euro
  bonds lost 32% in 2022; Oslo's OBX lost 62% in 2007-09, more than the S&P's 52% (both in
  euros; but OBX lost less in 2022 and 2025).
- **No re-entry rule beat buying back at once** over 10 years. Waiting won when the sale was near
  the real top and lost when it was 2-3 years early. A plan can cap regret, not add return; the
  deadline is its most important part.
- **A big IPO year is a weak top signal:** after 7 of the 11 hot IPO years since 1980, no bear
  market began within two years. 2026 is a record by dollars (SpaceX), not by number of deals.

## 2. What the research literature says

The literature comes first. This section covers three questions in turn: how to spot a late-stage bubble, how to leave one, and where to wait. Section 4 then shows how the playbook follows from it. Details and full citations are in `lanes/lit.md` (lit), `lanes/haven.md` (haven) and `lanes/bt.md` (bt, our backtests). "(unverified)" means the figure was read only from a summary or from memory in this run (lit §17; section 10.5). Some papers are cited from memory in lit and were not reopened: Campbell-Shiller, Goyal-Welch 2008, Baker-Wurgler 2006, Abreu-Brunnermeier, Fisher-Statman and Pan-Poteshman. They are standard results.

### 2.1 Recognising a late-stage bubble

One finding runs through all of it. The indicators that predict anything do so over 1-10 years, and most lose their edge out of sample. [Goyal-Welch (2008)](https://doi.org/10.1093/rfs/hhm014) found that the classic predictors mostly fail to beat the historical average. [Goyal-Welch-Zafirov (2024)](https://doi.org/10.1093/rfs/hhae044) re-tested them with data to 2021: of the predictors still significant in sample, about half predict poorly out of sample. Over six weeks the expected gain is about 0.6-0.8% of the amount, against a typical swing of about 5.4-6.8% (lit §4; our arithmetic). So for each indicator we ask two things: does it raise the risk, and does it give a date?

| Indicator | What the research finds | Horizon | Evidence quality | Out-of-sample record; our own test | Usable in 6 weeks? |
|---|---|---|---|---|---|
| **Valuation (CAPE, dividend yield)** | A high CAPE predicts low real returns. The one-year link is small: R² about 0.09 at 1 year and 0.3 at 5 years for the dividend yield (Cochrane 2011, unverified) ([Campbell-Shiller 1998](https://doi.org/10.3905/jpm.24.2.11); lit §3) | 5-10+ years | Strong at 10 years, weak at 1 year | Mostly fails out of sample (Goyal-Welch). With sign restrictions there is a small gain ([Campbell-Thompson 2008](https://doi.org/10.1093/rfs/hhm055)). **Ours:** the CAPE exit rules avoided a third of the fall in only 1-2 of 8 crashes; they were out from June 1997 and missed the +100% that followed (bt Part B) | **No.** CAPE says "expensive" (39.4 for Nov 2026, 98th percentile), not "when" |
| **Industry run-up (Greenwood-Shleifer-You)** | US industries 1928-2014, after a two-year rise of 100% or 150%, raw and net of the market: P(40% fall within 2 years) was 53% and about 80%, against a 14% base rate. The odds rise further with rising volatility, share issuance, acceleration and young firms. Turnover and sales growth do not help. In the 21 run-ups that crashed, the peak came on average 6 months and +30% after the flag ([GSY 2019](https://doi.org/10.1016/j.jfineco.2018.09.002); [NBER w23191](https://www.nber.org/papers/w23191); lit §1) | 2 years | Good: 40 US and 107 international episodes. The thresholds are in-sample means | International sample: 50% after 100%, 67% after 150%. **Ours** (`lanes/gsy-replication.md`, lane gsy-1; 49 Ken French industries 1928-2014): 38% after a 100% run-up (104 run-ups) and 51% after 150% (51), against 15% for any industry-month. Since 2002: 27% and 35% against 12%. Our definition gives more episodes than GSY's 40, and 19 of ours are 1933-35 rebounds, so the levels differ. The direction holds: odds 2-3 times the base rate. The median next 6 months was +3% after 100% and -6% after 150%, across all run-ups, crashed or not. As an overlay on a trend rule the flag added about +0.03 Sharpe and did not cut the worst loss materially, because the trend rule was already out for 88% of industry crashes (310 of 351, 1928-2001) (gsy-1 write-up, `research/gsy-1.md` on branch `gsy-1`, commit 35d155f) | **As a risk flag, not a date.** `^SOX` +99.5% over 2 years on 17 Nov, at the flag on the raw return; GSY's flag also needs +100% net of the market, which was not computed for SOX. Broad US tech (`HiTec`) +62% raw (bt amendment) |
| **Same, whole markets (Goetzmann)** | In national markets since the early 1900s, a crash after a boom is "only slightly" more likely than otherwise. After a market doubled, there was about a 10% chance it gave back the whole gain ([Goetzmann 2015](https://www.nber.org/papers/w21693), abstract) | Years | Medium: broad panel, abstract read | n/a | The counterweight to GSY: GSY's high odds are for industries, not whole markets |
| **Issuance and IPO waves** (a commonly cited signal; details in section 9.1) | In GSY, issuance flagged 13 run-ups, of which 9 crashed, but it missed 13 other crashes. The equity share of new issues predicted market returns 1928-1997 ([Baker-Wurgler 2000](https://pages.stern.nyu.edu/~jwurgler/papers/equityshare.pdf); later record unverified). Firms go public after strong returns, so a wave does not prove a bubble ([Pastor-Veronesi 2005](https://ideas.repec.org/a/bla/jfinan/v60y2005i4p1713-1757.html)) | 1-2 years | Medium | **Ours:** of 11 hot IPO years since 1980, a bear market began within two years after 4. The threshold was chosen after seeing the table (section 9.1) | **No** |
| **Breadth and concentration** | Across 49 US industries 1926-2025, concentration explains "virtually none" of future returns. A rule that held less when concentration was high lowered returns and raised risk ([Kritzman-Turkington 2025](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5436695), read via a [summary](https://quantpedia.com/the-fallacy-of-concentration-risk/), unverified at source). Practitioner studies find that high top-10 concentration preceded equal-weight beating cap-weight over 5 years (unverified). Advance/decline divergences, "% above the 200-day" and the Hindenburg Omen: no peer-reviewed support found (a short search; absence, not proof) (lit §5) | 5 years, and only for which stocks do better | Weak as a timer | Acting on concentration lost in their test. Not tested by us | **No.** At most a reason to buy back broad or equal-weight |
| **Sentiment indices** | When the Baker-Wurgler index is high, speculative stocks later do worse than safe ones. That is a cross-section result at about 1 year ([BW 2006](https://doi.org/10.1111/j.1540-6261.2006.00885.x); [BW 2007](https://doi.org/10.1257/jep.21.2.129)). A cleaned version predicts the monthly market return in and out of sample, 1965-2010 ([Huang-Jiang-Tu-Zhou 2015](https://doi.org/10.1093/rfs/hhu080); out-of-sample R² unverified). The AAII bull-bear survey is a modest, noisy contrarian signal ([Fisher-Statman 2000](https://doi.org/10.2469/faj.v56.n2.2340), unverified). For put/call, the robust result is for single stocks using non-public volume ([Pan-Poteshman 2006](https://doi.org/10.1093/rfs/hhj024)); for the index put/call ratio no solid evidence was found (lit §7) | Months to 1 year | Medium (Baker-Wurgler) to weak (AAII, put/call) | Even a few percent of monthly R² moves the expected six-week return by only a small fraction of a percent (lit §4). Not tested by us | **No.** No defensible threshold |
| **Credit spreads** | The excess bond premium leads recessions ([Gilchrist-Zakrajšek 2012](https://doi.org/10.1257/aer.102.4.1692)). Very tight spreads two years earlier predict widening and weaker activity ([López-Salido-Stein-Zakrajšek 2017](https://doi.org/10.1093/qje/qjx014)). Tight spreads are the warning; widening is the event. The literature gives no stock-sell threshold (lit §6) | 1-2 years (for the economy) | Medium for recessions; none for stock timing | **Ours:** the Baa-spread rule caught 2000 and 2007 but was late in 1987 and 2020. 87-95% of the credit rules' exits were false alarms (bt Part B) | **Only as a confirmer.** Calm on 10 Nov: Baa spread 1.51 |
| **Volatility, VIX** | Cutting exposure when recent variance is high raised Sharpe ratios in sample ([Moreira-Muir 2017](https://doi.org/10.1111/jofi.12513)). Across 103 strategies, real-time versions mostly did not beat the unmanaged ones ([Cederburg et al. 2020](https://doi.org/10.1016/j.jfineco.2020.04.015)). The VIX curve's slope predicts returns on volatility products, not on the S&P ([Johnson 2017](https://doi.org/10.1017/S0022109017000825)). An inverted curve marks stress already under way, and high VIX was often followed by above-average returns (lit §9) | Weeks to months | Medium in sample, weak out of sample | **Ours:** VIX above 30 caught 2007-09, 2020 and 2022 (data from 1990). A volatility spike alone protected poorly. The VIX trigger failed the six-week bar (bt Parts A, B, amendment) | **Only as a confirmer.** On 18 Nov: VIX 24.6, curve just inverted (section 5.1) |
| **Trend and momentum** | 12-month time-series momentum works in each of 58 futures; it persists 1-12 months and then partly reverses ([Moskowitz-Ooi-Pedersen 2012](https://doi.org/10.1016/j.jfineco.2011.11.003)). Trend following was positive in 8 of the 10 worst 60/40 drawdowns since 1880 ([Hurst-Ooi-Pedersen 2017](https://doi.org/10.3905/jpm.2017.44.1.015)). It fails in sudden crashes like 1987 (lit §8) | Reacts after the turn | Strong over the long run: the data before 1985 are out of sample relative to the 2012 paper | The honest out-of-sample gain is small, and most exits are whipsaws (section 2.2). **Ours:** the 200-day rule avoided at least a third of the fall in all 8 big crashes; 89% of its exits were false alarms (bt Part B) | **Yes.** It is the one reaction rule (sections 2.2, 2.3) |
| **LPPL (Sornette)** | Fits a "critical time" to super-exponential price growth ([Johansen-Ledoit-Sornette 2000](https://doi.org/10.1142/S0219024900000115)) | Weeks to months (claimed) | Weak | On 11 Hang Seng crashes, only 7 fits had parameters in the ranges proposed after the fact ([Bree-Joseph](https://arxiv.org/abs/1002.1010)). No public record of live hits and false alarms was found (lit §10). Not tested by us | **No.** The fits are unstable |
| **PSY / GSADF** | A real-time test of whether prices are explosive. It dates the start of the 1990s Nasdaq episode years before 2000 ([Phillips-Shi-Yu 2015](https://doi.org/10.1111/iere.12132); [Phillips-Wu-Yu 2011](https://doi.org/10.1111/j.1468-2354.2010.00625.x)) | Dates the start; dates the end only after prices turn | Medium as a bubble detector | Used as an exit it behaves like a trend rule (lit §11). Not tested by us (no tool) | **No** as a top timer |

**What the table says.** Everything that warns of a bubble works over years, and nothing names a date. Trend is the only indicator with a long out-of-sample record that acts within weeks, and it acts after the turn, not before. Theory agrees. In Abreu-Brunnermeier (2003), informed traders cannot coordinate their exit, so a bubble outlives "everyone knows" and minor news can set off the crash. By construction there is no public top signal ([Econometrica](https://doi.org/10.1111/1468-0262.00393); lit §2).

### 2.2 Leaving a bubble

- **Trend following.** Faber's rule: hold the index while its month-end close is above its 10-month average, otherwise hold cash. He reports similar results for 3 to 12+ month averages and notes that 10 months is close to the 200-day average ([Faber 2007](https://doi.org/10.3905/jwm.2007.674809)). His reported results for 1901-2012: 10.18% a year against 9.32% for buy-and-hold, with the 1930s fall cut from about 84% to 42% (unverified, secondary summaries). Hurst-Ooi-Pedersen covered 67 markets, 1880-2016. The 10 worst 60/40 drawdowns lasted about 15 months on average, which gives the signal time to flip. Acting one month late hurts ([AQR copy](https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing); lit §8).
- **The honest record: whipsaws.** Zakamulin (2014) chose parameters out of sample and charged 0.5% costs. On the S&P 500 1930-2012, the Sharpe gain shrank to about 7-12%, and in about 80% of the spells out of the market the timer did worse than buy-and-hold (unverified, CXO summary). All of the benefit came from a few severe bear markets ([JAM](https://doi.org/10.1057/jam.2014.25)). **Ours:** over 98 years the trend rules ended level with buy-and-hold on return, with about a third less maximum drawdown. Their cost in normal years was 1.2-3.5% a year: insurance with a premium (bt Part B). For a sale that must happen by a fixed date anyway, the whipsaw cost nearly vanishes: a trigger only moves the date earlier (lit §8).
- **Stop-losses.** If prices are a random walk, a stop-loss always lowers expected return. It adds value only when returns have momentum or regimes switch. In the working paper, rules added 50-100 bp per stop-out month in 1950-2004, with long Treasuries as the place to wait. The exact thresholds are unverified ([Kaminski-Lo 2014](https://doi.org/10.1016/j.finmar.2013.07.001); lit §12). **Ours:** 8% and 10% drawdown stops protected in all 8 crashes but bought back too early in long bear markets. A Kaminski-Lo-style rule did clearly worse than the trend rules. A 5% trailing stop failed the six-week bar (bt Part B, amendment, Part A).
- **Volatility management.** It helps in sample (Moreira-Muir) and is weak in real time (Cederburg et al.). **Ours:** using volatility as a confirmer for the 200-day rule cut trades but let 2000-02 through (-42%) (bt amendment).
- **Timing overall.** 237 newsletter strategies (1980-1992) showed no ability to raise stock weights before rises or cut them before falls ([Graham-Harvey 1996](https://doi.org/10.1016/0304-405X(96)00878-1)). Investors' actual (dollar-weighted) returns trailed buy-and-hold by about 1.3% a year on NYSE/AMEX 1926-2002, and by 5.3% a year on Nasdaq 1973-2002 ([Dichev 2007](https://doi.org/10.1257/aer.97.1.386); numbers unverified). The literature backs rules that cut exposure after a regime change, not forecasts of tops (lit §13).
- **Riding and scaling out.** Hedge funds rode the tech bubble and cut their positions stock by stock. Their tech exposure peaked around September 1999, about six months before the top (detail unverified) ([Brunnermeier-Nagel 2004](https://doi.org/10.1111/j.1540-6261.2004.00690.x); lit §2).
- **Selling at once or in stages.** Lump-sum investing beat a 3-month cost-averaging plan 68% of the time (1976-2022). Staging won in the worst 5% of cases and lowered regret: "investors with higher loss aversion would be better off with CA" ([Vanguard 2023](https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf)). A fixed schedule is beaten by a policy that acts on new information ([Constantinides 1979](https://doi.org/10.2307/2330513)). Turned round for selling: over six weeks, staging costs little in expectation and caps regret either way (lit §14).

### 2.3 The ranked shortlist, and where each threshold comes from

Ranking = strength of evidence × usability within six weeks (lit §15).

| Rank | Indicator and threshold | Threshold from | What our tests found | In the playbook? |
|---|---|---|---|---|
| 1 | **Trend break on the holding's own index.** Month-end close below the 10-month average (Faber). Daily form: close below the 200-day average. Slower form: 12-month return below 0 (MOP) | 10-month and 12-month: **literature**. 200-day daily: **heuristic** close to Faber; no paper pins it. 2% band or 2-day confirmation: **heuristic** | 200-day: avoided at least a third of the fall in 8 of 8 crashes; held to the trough it lost 11-19%, against 25-86% for buy-and-hold. The band or 2-day versions halve the trades but were late in 1987 (-33% vs -16%). 12-month momentum missed 1987 and 2020 (bt Part B, amendment) | **Yes:** the speed-up trigger, on the first close below |
| 2 | **Drawdown stop**, -8% to -10% from the recent high | **Heuristic.** Kaminski-Lo give the condition, not the number | Protected in 8 of 8 crashes but bought back too early in long bears. A trailing stop failed the six-week bar | No |
| 3 | **Volatility spike after calm**: 21-day realized volatility above about 2x its 1-year median, or VIX above 30, together with rank 1 or 2 | **Heuristic.** Moreira-Muir give the direction | The VIX trigger failed the six-week bar; volatility alone protected poorly | No for selling. For re-entry, VIX above about 45 brings a tranche forward |
| 4 | **Credit stress**: high-yield spread or the excess bond premium rising quickly | **No literature threshold.** bt used Baa spread 0.5 above its 1-year low, and HYG/LQD below its 200-day average (heuristics) | Late in 1987 and 2020; 87-95% false alarms | No for selling. For re-entry, a spread peak can bring a tranche forward |
| 5 | **GSY flag on the AI industry**: two-year return above 100%, raw and net of the market, plus rising volatility, issuance, acceleration and young firms | **Literature** (in-sample means) | Replication: 38% and 51% against 15% (`lanes/gsy-replication.md`). As a trend overlay it added little (gsy-1) | As background only: a reason to have a plan and to wait in cash rather than the broad market. Not a trigger |

**Not supported for a six-week decision** (lit §15): CAPE or any valuation level; concentration and breadth; LPPL; GSADF as a top timer; put/call and AAII; VIX-curve inversion; seasonality (the "Halloween" effect: [Bouman-Jacobsen 2002](https://doi.org/10.1257/000282802762024683), from memory, unverified; if anything a weak reason not to rush); newsletter and pundit calls.

**So the playbook's working trigger is not a paper's number.** The 200-day daily line is a heuristic close to Faber's 10-month rule. Our backtests tested it on 8 crashes, with the card's bar fixed before the results. Combining it with staged selling was added after the first results were seen (post hoc).

### 2.4 Havens in the literature (details and our crash table: section 7)

- **Gold is a haven only briefly.** It is a haven for stocks "only for 15 trading days after an extreme shock", and neither a hedge nor a haven for bonds ([Baur-Lucey 2010, WP](https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp198.pdf)). Over 1979-2009 it was a hedge and haven for the US and major European markets, but not for Australia, Canada, Japan or the BRICs ([Baur-McDermott 2010](https://econpapers.repec.org/RePEc:eee:jbfina:v:34:y:2010:i:8:p:1886-1898)). **Ours:** gold fell 22% in dollars inside the Lehman weeks and 12% in March 2020 (haven).
- **Haven currencies.** CHF and JPY gain against the dollar over hours to days when US stocks fall (1993-2008) ([Ranaldo-Söderlind 2010](https://econpapers.repec.org/RePEc:oup:revfin:v:14:y:2010:i:3:p:385-407)). **Ours:** JPY nevertheless fell 21.5% against the dollar in 2022.
- **Flight to quality, and when it fails.** In the March 2020 "dash for cash", even government bonds were sold ([FSB 2020](https://www.fsb.org/2020/11/holistic-review-of-the-march-market-turmoil/)). Stocks and bonds fall together when inflation uncertainty dominates ([Brixton et al. 2023](https://www.aqr.com/insights/research/journal-article/a-changing-stock-bond-correlation)). **Ours:** long Bunds lost 32% in 2022.
- **Money funds can break.** The Reserve Primary Fund fell to 97 cents on 16 Sep 2008 ([SEC](https://www.sec.gov/litigation/litreleases/2009/lr21025.htm)). Between 11 and 25 March 2020, euro-area LVNAV funds had outflows of about EUR 85bn (16% of assets), while public-debt funds had inflows ([ECB](https://www.ecb.europa.eu/pub/financial-stability/macroprudential-bulletin/html/ecb.mpbu202104_2~a205b46756.en.html)).
- **Trend following as "crisis alpha"** (Hurst-Ooi-Pedersen; [Neville et al. 2021](https://www.man.com/maninstitute/best-strategies-for-inflationary-times)). Both come from firms that sell trend products. It is a strategy with losing years, not a parking place.
- **Upshot:** every haven in the literature is conditional on the kind of crash. In our crash table, euro cash is the only holding that lost at most about 0.5% in every crash (section 7).

## 3. What investors with proven records did

"Action" means documented in a filing, an annual letter, reported fund returns, or press at the time. "Talk" means forecasts, memos and interviews. Sources for every row are in `lanes/inv.md` (inv §1-12). Numbers marked (unverified) rest on one weak source.

| Investor | Documented action (dated) | Result | Talk | Verdict |
|---|---|---|---|---|
| **Buffett / Berkshire** | 1969: wound up his partnership, "not attuned to this market" ([letter](https://gurufocus.com/news/6620/warren-buffett-partnership-letter-in-may-1969)). 1998-2000: no tech. 2008: put $14.5bn into crisis deals. 2020: sold the airlines and did not spend the cash. 2024-25: net seller; cash about $382bn at 30 Sep 2025 ([Fortune](https://fortune.com/2025/11/01/warren-buffett-stocks-net-selling-berkshire-hathaway-q3-earnings-investment-portfolio-cash/)) | 1999: -19.9% vs S&P +21.0%. 2000-02: about +30% vs -38%. 2008: -31.8% vs -37.0% ([2024 letter](https://www.berkshirehathaway.com/letters/2024ltr.pdf)). BRK-B -53.9% peak to trough 2007-09 | "Neither Charlie ... nor I can predict" ([2008 letter](https://www.berkshirehathaway.com/letters/2008ltr.pdf)). "Buy American. I Am." (16 Oct 2008), 28.5% before the S&P low | **Action-backed** |
| **Grantham / GMO** | Underweight US growth and tech from about 1997-98; defensive into 2008 | Right in the end, but GMO's assets fell from about $31bn to $20bn (1998-2001) ([Institutional Investor](https://www.institutionalinvestor.com/article/b1hjlb0qs4c807/GMO-Is-Feeling-Pain-Reminiscent-of-the-Late-1990s)) | "Superbubble", 5 Jan 2021: the S&P was 97% higher by 17 Nov 2026. "Slim to none" chance the AI bubble does not burst, Jan 2026 ([ThinkAdvisor](https://www.thinkadvisor.com/amp/2026/01/20/jeremy-grantham-slim-to-none-chance-ai-bubble-wont-burst/)) | **Mixed** |
| **Marks / Oaktree** | "bubble.com" memo, 3 Jan 2000 (a view; Oaktree held no tech). 2008: a $10.9bn distressed fund, investing about $600m a week in the last 15 weeks of 2008 ([Oaktree](https://www.oaktreecapital.com/insights/insight-commentary/education/commemorating-25-years-of-mastering-the-market-cycle)) | Strong after 2008 (numbers unverified) | Dec 2025: neither all-in nor all-out, "a moderate position" ([memo](https://www.oaktreecapital.com/docs/default-source/memos/is-it-a-bubble.pdf)) | **Action-backed** |
| **Druckenmiller** | Mar 2000: bought about $6bn of tech near the top. 2024: sold Nvidia ([Quartr](https://quartr.com/insights/investment-strategy/stanley-druckenmiller-breaking-the-bank); [Fortune](https://fortune.com/2024/10/18/billionaire-investor-druckenmiller-sold-nvidia-regrets-huang-musk-ellison/)) | Lost about $3bn and left Soros in April 2000 (sizes differ, unverified). Sold Nvidia "too early" | On Nvidia: "It was a big mistake" | **Mixed** |
| **Klarman / Baupost** | Reopened to new money in early 2008 and invested about $4bn in the crash; often 30-50% in cash ([Fool](https://www.fool.com/investing/general/2010/11/11/klarman-finds-opportunities-scarce.aspx)) | 2008 about -7% to -13% (unverified) | Cash is "a residual of our bottom-up search" ([letter quote](https://www.distressed-debt-investing.com/2009/12/wisdom-from-seth-klarman-part-6.html?m=1)) | **Action-backed** (letters private) |
| **Templeton** | 1999-2000: shorted about 84 dot-com stocks, each timed to the end of its IPO lockup ([Investing.com](https://m.investing.com/analysis/when-the-unicorns-become-horses-again--tech-bubble-repeats-200470464?ampMode=1)). The mechanism is backed by [Ofek-Richardson](https://www.nber.org/papers/w8630) | Large profit (about $90m often quoted, unverified) | "Bull markets ... die on euphoria" | **Action-backed** (book source) |
| **Robertson / Tiger** | Refused tech; announced on 30 Mar 2000 that Tiger would close, 20 days after the Nasdaq peak ([CNN](https://money.cnn.com/2000/03/30/mutualfunds/q_funds_tiger/)) | Assets fell from about $22bn to $6bn before the top; proved right only after closing | Said he no longer understood the market | **Mixed** |
| **Burry** | 2005-08: CDS on subprime mortgage bonds. 2023: index puts. 30 Sep 2025: puts on Nvidia and Palantir ([Fortune](https://fortune.com/2025/11/04/big-short-investor-michael-burry-nvidia-palantir-puts-alex-karp/)) | About +489% net, Nov 2000 to Jun 2008 (page unverified). 2023 puts likely lost. 2025 profit or loss unknown | Repeated crash calls 2015-2023 | **Mixed** |
| **Hussman** | Fund hedged most of the time since about 2009 ([Zacks](https://zacks.com/funds/mutual-fund/quote/HSGFX/performance)) | -1.5% to -4.4% a year over 10 years; assets from $5.2bn to $0.34bn | Repeated forecasts of large losses | **Talk + costly action** |
| **Dalio / Bridgewater** | Pure Alpha +9.4% in 2008. Jan 2020: "cash is trash" ([Fortune](https://fortune.com/2020/09/15/the-losses-continue-to-pile-up-for-hedge-fund-king-ray-dalio/)) | Pure Alpha II about -20% by Mar 2020 | "We should have made money ... the way we did in 2008" | **Mixed** |
| **Shiller 1996** | Fed briefing (3 Dec 1996, date unverified); Greenspan's speech on 5 Dec, with the S&P at 744.38 ([Fed](https://www.federalreserve.gov/boarddocs/speeches/1996/19961205.htm)) | S&P +105% to Mar 2000; the 2002 trough (776.76) was still above the warning-day level | Right about long-run returns, 3+ years early | **Talk only** |
| **Timer studies** | 237 newsletters 1980-92 ([Graham-Harvey](https://www.nber.org/papers/w4890)). Hulbert data 1980-2001 ([CXO](https://www.cxoadvisory.com/investing-expertise/classic-papers-the-value-of-investment-newsletters/)) | No timing skill as a group. The top timers of 2000-02 were average in 2007-09. The best timers cut volatility rather than adding return | n/a | **No repeatable skill** |

**Lessons** (inv, cross-investor lessons):

1. **Nobody with a documented record timed a top to the month.** Buffett was more than a year early, Grantham 2-3 years, Shiller 3+ years. Robertson quit 20 days before he would have been proved right. Those who were right say they cannot time it (Buffett, Marks, Klarman).
2. **Being early is expensive and can end you first.** Tiger closed; GMO lost about a third of its assets; Hussman's fund shrank by more than 90%. A plan must survive the pop coming late.
3. **The winners scale; they do not flip.** Buffett built cash over years, Marks turns a "risk dial", Klarman's cash is a residual, and hedge funds cut tech stock by stock (section 2.2).
4. **Re-entry is where the money was made**, with rules set in advance. They were early there too: Buffett's op-ed came 28.5% before the low, and Oaktree started buying in September 2008. Several who called the top missed the re-entry (Grantham, Hussman).
5. **Chasing, and valuation-only calls, hurt even the best.** Druckenmiller bought the 2000 top and sold Nvidia too early on valuation.
6. **Shocks are not forecastable**, even by the largest macro firm (Dalio 2020). Crash safety must come from the asset you hold (cash), not from a call. The one clean bubble trade, Templeton's, used a dated mechanical trigger, not general bubble talk.

## 4. How the playbook follows

| Playbook step (summary, section 1) | From the literature (section 2) | From the investors (section 3) | From our own backtests | How clean |
|---|---|---|---|---|
| **1. On your start day, sell half of each holding; sell all of a holding whose index already closed below its 200-day average** | Six-week returns are mostly noise (2.1). Staging costs little and caps regret (Vanguard, 2.2) | Scale, don't flip (lesson 3) | "Half now, half at the fallback" passed the six-week bar (bt Part A). Per holding: Oslo fits the card's `late` sample; US and tech holdings fit only the post-hoc `now-like` sample, where staging also held up (section 6.1) | Bar fixed before any number. But `late` was defined to fit Nov 2026, its windows come from only about 20 separate spells, and the US/tech evidence is post hoc |
| **2. Sell the rest on the trading day after the first close below the 200-day average, else at the fallback** | Trend is the only reaction rule with a long out-of-sample record (Faber, Moskowitz-Ooi-Pedersen, Hurst-Ooi-Pedersen). Its whipsaw cost (Zakamulin) does not matter for a forced sale. The 200-day daily line is a heuristic (2.3) | React, don't predict (lessons 1, 6). Pre-commit, because exits are a race (Abreu-Brunnermeier) | Avoided a third or more of the fall in 8 of 8 crashes (bt Part B). Added to staging, it cut the mean loss when a 10% fall came in the window from -5.0% to -1.4% (S&P, all start days with a 10%+ fall in the window, `crash-window`) | **Post hoc:** the combination was added after the first results (bt amendment). 8 crashes are 8 observations |
| **Fallback 18 Dec for shares, 11 Dec for funds (4 Dec for slow funds); last safe 21 Dec (shares), 15-16 Dec (funds with cash at the broker within 2-6 business days), 9 Dec (within 5-10)** | None: this is the calendar | A plan must work if the pop comes late (lesson 2) | Settlement, fund cut-offs and the holiday calendar (park sections 4 and 7). The fallback day is the forced sale in the test | A fact, not a market signal. Fund dates rest on a platform's "normally" figures |
| **3. Move the money to euros the same day** | None | None | Currency risk of a smaller non-euro market: the krone (NOK) fell about 20% against the euro in late 2008 and 18.5% in one month in 2020. OBX lost 62% in 2007-09, more than the S&P's 52% (both in euros; haven, park) | Descriptive |
| **4. Park in euro cash** | Havens are conditional on the kind of crash; money funds can break (2.4) | Crash safety from the asset (lesson 6). Berkshire fell 54% in 2007-09 | In our table of 10 crashes, euro cash lost at most about 0.5% (negative-rate years); every other candidate lost more in some crash (haven) | Descriptive, nothing fitted |
| **5. Buy back in 12 monthly buys through 2027; as a bet on a real bust only, in thirds at -20%, -30% and -40%, all in by 29 Dec 2028** | A lump sum usually wins; spreading lowers regret (Vanguard). The literature gives no threshold | Re-enter with rules set in advance, and expect to be early (lesson 4). A fixed end date avoids the Grantham/Hussman failure | No re-entry rule beat buying back at once. In the high-valuation months that fit today, 12 monthly buys had the better median (0.97 vs 0.92 times buying at once) and the milder worst tenth (0.90 vs 0.72); the thirds won only in real busts (1.4-1.6 times) (section 8.2) | Both rules and levels fixed on the reentry card before any number; which one is the default was chosen after seeing them (review round 2). 8 high-valuation episodes, only 3 since 1972 |

**Left out on purpose:** CAPE, breadth and concentration, sentiment indices, LPPL, GSADF and IPO counts as sell triggers. The literature gives them no date (sections 2.1, 2.3), and our tests agree for CAPE, VIX and credit. VIX and credit appear only as a way to bring a re-entry tranche forward.

**Ours, not the literature's:** the choice of two tranches, the 200-day daily form, the fallback mechanics and the re-entry levels all come from our own backtests. Fixed in advance: the six-week bar, the 8-crash rule test and the re-entry card. Chosen after seeing results: the "half now plus 200-day" combination, the `now-like` sample, the choice of 12 monthly buys over the thirds as the default re-entry, the 300-IPO threshold and the 10-firm filter in the GSY replication (section 10.2). Commonly heard ideas (an IPO wave as a top signal, Berkshire, a savings account, bonds) are assessed after this evidence, in section 9.

## 5. Where the indicators stand now

### 5.1 The readings (bt lane, Part C): an example to refresh

US and Oslo data to the close of Wed 18 Nov 2026 (refetched 22:12 UTC, after the 16:15 New York VIX close; the stock close is
16:00 New York, 22:00 CET), Baa spread to 10 Nov (cached; FRED not reachable from this machine), Shiller CAPE for Nov 2026 (price = 12 Nov close). Source:
`lanes/bt.md` Part C and "Review round 1 fixes", script `bt_now.py`. These numbers move every
day; the rules in section 6 use the reading on your own start day, and these are the example.

> **To refresh before acting:** run
> `uv run --with xlrd --with pandas python -I research/exit-plan-2026/scripts/bt_now.py --fetch <dir>`
> (see its header; `<dir>` is a scratch folder outside the repo). It prints this table, the
> 200-day state of each holding type with the date of the last cross, and which tested sample
> the state matches. Without the script, any charting site that draws a 200-day simple moving
> average on the index shows the same state.

| | S&P 500 | Nasdaq Composite | OSEBX | OBX |
|---|---:|---:|---:|---:|
| Close | 7,323.63 | 24,429.88 | 2,073.85 | 1,980.71 |
| vs 200-day average | **-0.31%** (7,347) | **-2.9%** (25,152) | +3.2% (2,010) | +1.9% (1,943) |
| 200-day trigger at that close | **fired** (below since 17 Nov, 2 closes) | **fired** (below since 13 Nov) | not fired | not fired |
| vs 50-day average | -4.3% | -6.9% | -1.0% | -1.4% |
| From all-time high | -6.3% (high 6 Oct) | -11.5% (6 Oct) | -3.3% (30 Oct) | -3.8% (30 Oct) |
| Oct month-end vs 10-month average (Faber) | +3.8% (in) | +1.8% (in) | +7.2% | +6.6% |
| 12-month / 24-month return | +10.7% / +24.3% | +8.9% / +30.0% | +30.8% / +43.8% | +31.5% / +46.4% |

(The 17 Nov readings used in the first draft and in the round-1 review: S&P 7,340.53, 0.05%
below its line; Nasdaq 3.3% below; VIX 25.46, VIX/VIX3M 1.019. States did not change.)

Other readings (same dates):

- **Volatility:** VIX 24.56 on 18 Nov, 1.38 times its 50-day mean, 92nd percentile of the past
  year. VIX/VIX3M = 1.011, so the VIX curve is just inverted (1.10 on 5 Nov, 0.91-0.94 on
  11-13 Nov, 1.02 on 17 Nov). The S&P fell 4.36% on Thu 5 Nov (bt, Yahoo `^GSPC`); AP reported the Nasdaq -5.5%
  that day ([AP via Boston.com](https://www.boston.com/news/national-news/2026/11/05/a-brutal-sell-off-for-ai-stocks-sends-wall-street-reeling-and-the-sp-500-tumbles-4-4/)).
- **Credit:** calm. HYG/LQD is 0.50% above its 200-day average (18 Nov). The Baa minus 10-year spread was
  1.51 on 10 Nov; the tested credit rule would turn hostile only above about 1.95.
- **Valuation:** Shiller CAPE 39.37 for Nov 2026, the 98.3rd percentile of all months since
  1881; only 1999-2000 was higher (peak 44.2 in Dec 1999). On how this differs from the 39.7 and
  39.8 quoted elsewhere, see section 10.1.
- **AI stocks:** Nvidia closed at 155.46 on 17 Nov, 35.0% below its 6 Oct close of 239.24
  (152.12 on 18 Nov). The semiconductor index `^SOX` was up 99.5% over two years on 17 Nov, at
  the Greenwood-Shleifer-You 100% flag on the raw return (the flag also needs +100% net of the
  market, which was not computed for SOX), but already 34% below its 22 Jun 2026 high. XLK (US
  tech) was 19% below its 6 Oct high. Broad US tech (Ken French `HiTec`) was up 62% over two
  years at end-Sep 2026 (+25% net of the market): below the flag, which it touched only in single
  months of 2024-25 (bt amendment).
- **Trend-rule states on the S&P 500 at the 18 Nov close:** out: 200-day rule (by 0.31%), VIX
  curve, both CAPE rules. In: 12-month momentum, 8% and 10% drawdown stops (the 8% stop needs a
  close below about 7,193), VIX above 30, both credit rules. The 10-month rule is in: that is the
  decision made at the Fri 30 Oct month-end close (+3.8%), in force until the next check at the
  Mon 30 Nov close. Its live value on 18 Nov was -0.26%, so it would turn out if the month ended
  at that level (bt review fixes, point 4a). On the Nasdaq the drawdown stops have been out since
  2 Nov.

### 5.2 Which reading applies to what you hold

This report assumes no particular holdings. Each holding follows the index of the market it
tracks, and each holding is a separate sale, so apply the trigger per holding, to the state on
your start day:

| If the holding is ... | Watch this index | State at the 18 Nov closes (example) |
|---|---|---|
| Shares on Oslo Børs, or a fund tracking Oslo or the Nordics | OSEBX (broad); OBX for the 25 largest | Not fired. OSEBX must close below about 2,010, OBX below about 1,943 |
| A US or global index fund, or US large-company shares | S&P 500 (for a global fund also check the MSCI World ETF `URTH`) | **Fired** (0.31% below; first close below 17 Nov); `URTH` 1.0% below its line |
| A tech, Nasdaq or AI fund, or tech shares | Nasdaq Composite | **Fired** (2.9% below) |
| A single company share | The index of its home market, as above | A stock's own 200-day line was not tested |

Caveats: global (MSCI World) funds were not tested; the S&P 500 (about 70% of MSCI World) is
the nearest tested index, and `URTH` is shown for information only. If the two sit on different
sides of their 200-day lines, the S&P 500 governs, because it is the index the rule was tested
on; `URTH` matches no tested sample (its high, 13 Aug, is older than the 63 trading days
`now-like` allows). At the 18 Nov closes both were below, so the question did not arise. The 200-day average moves a
little every day, so the levels above are from 18 Nov.

### 5.3 What this means

- **The US market is in a correction, not (yet) a crash.** Stress is visible in volatility and
  the VIX curve; credit has not confirmed it. Nobody can say from these readings whether this is
  the start of the pop (lit section 4; inv lessons 1 and 7).
- **History does not say "a pull-back means more to come".** In past months like now (expensive
  market, index 4-12% below a recent high), the next six weeks were on average slightly up
  (holding to the fallback date: mean +1.4%), but one window in ten ended more than 5% worse
  (bt, `now-like` sample; defined after seeing today's readings, so descriptive only).
- **CAPE says long-run returns are likely low; it says nothing about the next six weeks.** As an
  exit rule it was out years early and missed whole bull markets (bt Part B; lit section 3).
- **Holdings on a smaller non-euro market carry a second risk: the currency.** For Oslo, the
  krone (NOK) lost about 20% against the euro in late 2008 and 18.5% in one month in 2020
  (Norges Bank fixings, park section 5). In euros, Oslo's OBX fell more than the S&P in the deep crashes (2007-09: -62% against -52%, own
  maximum drawdown -70%; Lehman leg -54% against -32%; 2020 -42% against -34%) and less in the
  smaller ones (2022: -9.0% against -13.1%; Aug 2024 -6.6% against -9.1%; 2025 -8.5% against
  -22.7%) (haven, corrected in review round 1). In the deep crashes, stock falls and krone falls
  came together.

## 6. The exit playbook

### 6.1 Why this design

The bt lane tested 11 ways to sell inside the window on S&P 500 data from 1928 to 2025 (Nasdaq,
OBX and OSEBX as robustness), plus 3 variants added later. The window starts on day 0 and ends
with a forced sale on the fallback day (trading day 22 = Fri 18 Dec 2026 counted at Oslo from
18 Nov; from a later start day the window is a day or two shorter). Main sample `late`:
expensive market (CAPE top 10%), index within 5% of its high, up 25% or more over two years. The
card's bar, fixed before any number: a way of selling "beats selling everything now" only if,
in `late`, its 5th percentile is no worse than -5% and its median is above 0, on both the S&P and
the Nasdaq.

S&P 500 in the card's (pre-registered) `late` sample, result versus selling everything on day 0
(R-1 in %; `lanes/bt.md` Part A):

| Way of selling | Median (`late`) | 5th pct (`late`) | Chance >5% worse (`late`) | Mean if a 10% fall comes in the window (all start days) | Passes the bar |
|---|---:|---:|---:|---:|---|
| Sell everything now | 0 | 0 | 0% | 0 | (baseline) |
| Hold, sell everything on 18 Dec | +1.06 | -5.69 | 7.1% | -10.05 | no |
| **Half now, half on 18 Dec** | +0.53 | -2.85 | 0.4% | -5.03 | **yes** |
| Five weekly fifths | +0.48 | -3.05 | 0.6% | -5.12 | **yes** |
| Thirds (post hoc) | +0.5 | -3.0 | n/a | -5.33 | yes |
| **Half now, rest on 18 Dec or the day after a 200-day break** (post hoc) | +0.5 | -2.8 | n/a | **-1.40** | yes |
| Everything on a 200-day break, else 18 Dec | +0.99 | -5.57 | 7.4% | -2.81 | no |
| Limit +3% above today, else 18 Dec | +1.36 | -5.68 | 6.9% | -8.38 | no |
| Limit +5%, else 18 Dec | +1.07 | -5.69 | 7.1% | -9.20 | no |
| 5% trailing stop, else 18 Dec | +0.96 | -5.66 | 8.1% | -5.91 | no |
| VIX spike (above 1.3 x its 50-day mean), else 18 Dec (VIX data: 1990 on only) | +0.77 | -6.10 | 8.6% | -5.83 | no |
| Below the 50-day average, else 18 Dec | -0.13 | -4.06 | 3.0% | -2.04 | no (median below 0) |

**Which sample fits each holding today** (bt "Review round 1 fixes", point 1). `late` needs the
index within 5% of its high. At the 18 Nov closes Oslo still fits it; the S&P (-6.3%) and the
Nasdaq (-11.5%) do not. For them the nearest sample is `now-like` (CAPE top 10%, index 4-12%
below a high set within the last 63 trading days), defined after seeing today's readings
(post hoc, card amendment 2). Oslo's `late` sample uses the US CAPE (there is no Oslo CAPE), so
for OSEBX it is the same as the `runup` sample. R-1 in % against "sell all now" (which is 0 in
every column); train period, windows ending by Nov 2025:

| Holding type (proxy index) | Sample that fits (status) | Way of selling | Mean | Median | 5th pct | Chance >5% worse |
|---|---|---|---:|---:|---:|---:|
| Oslo shares, Oslo or Nordic fund (OSEBX) | `late` (card sample; Oslo a robustness index; 10 spells, 2013-2025) | half now, half at the fallback | +0.08 | +0.21 | -3.25 | 1.0% |
| | | half now, rest on a 200-day break | +0.01 | +0.16 | -3.26 | 0.0% |
| | | hold to the fallback | +0.16 | +0.43 | -6.51 | 9.3% |
| Global fund, US shares (S&P 500) | `now-like` (post hoc; 44 spells) | half now, half at the fallback | +0.71 | +1.13 | -3.82 | 1.7% |
| | | half now, rest on a 200-day break | +0.39 | +0.15 | -2.41 | 0.0% |
| | | hold to the fallback | +1.43 | +2.25 | -7.64 | 10.7% |
| Tech fund or tech shares (Nasdaq) | `now-like` (post hoc; 35 spells) | half now, half at the fallback | +1.02 | +1.40 | -5.00 | 5.0% |
| | | half now, rest on a 200-day break | +0.92 | +1.15 | -4.78 | 4.6% |
| | | hold to the fallback | +2.04 | +2.81 | -10.00 | 15.7% |

Notes: OBX (2004-2025) gives the same picture as OSEBX (staged 5th percentile -3.5, hold -6.9).
The Nasdaq at -11.5% (18 Nov close) sits near the edge of the `now-like` band; a further fall
of about 0.6% puts it outside every tested sample. The sub-samples that start below the 200-day line, as the US did on
17 Nov, have only 14 (S&P) and 7 (Nasdaq) separate spells: too few to read. So the evidence for
Oslo holdings is the card's own sample; for US and tech holdings it is post hoc, and on the
Nasdaq staging only just meets the -5% line.

**What selling a US/tech holding in full costs** (bt review fixes, point 2; post-hoc `now-like`
sample, in % of the holding). Against plain staging: S&P about 0.7% by the mean, 1.1% by the
median; Nasdaq 1.0% and 1.4%. It buys a certain price instead of a spread whose worst 1 in 20 is
3.8-5.0% lower. Against the tested 200-day rule in a below-the-line start the difference is a
fraction of a percent (+0.06% S&P, -0.26% Nasdaq, in the 14- and 7-spell sub-samples), because
that rule sells the second half the next day anyway (step 1 below).

How to read it:

- **Staging buys a smaller worst case, not money.** In `late` its average gain over selling now
  is 0.3-0.4 points on the S&P, 0.1 on OSEBX. What it removes is the
  7-9% chance of a more-than-5% loss from waiting. Five steps are no better than two (the medians
  and tails are within 0.2 points).
- **The 200-day speed-up keeps staging's typical result and cuts the crash case.** In `late`, it
  had the same median as plain staging and a mean 0.03 points lower; when a 10% fall came inside
  the window (all start days, `crash-window`), the loss fell from -5.0% to -1.4% (S&P), -4.9% to -1.9% (Nasdaq), -4.7% to -2.4%
  (OSEBX). It was added after the first results were seen (bt amendment), so its numbers are
  less clean than the card's original variants.
- **Why the 200-day line and not another trigger.** Over 1928-2025 the 200-day rule avoided at
  least a third of the fall in all 8 big crashes (1929, 1937, 1973-74, 1987, 2000-02, 2007-09,
  2020, 2022); held to the trough it lost 11-19% where buy-and-hold lost 25-86% (bt Part B). Its
  known cost, many false alarms (89% of its exits) and whipsaws, does not matter for a one-off
  sale you must make anyway (lit sections 8 and 15). Trailing stops and VIX triggers rarely fire
  in time inside six weeks and failed the bar; the 50-day line sells on ordinary dips; CAPE
  rules exit years early. Selling everything on a 200-day break alone (no first half) failed the
  bar in `late` (5th percentile -5.57), because it waits fully while the index is above the line.
- **Why not wait for a better price.** The limit strategies fill about two times in three, but
  if the fall comes they sell low on the fallback date. Their worst cases are no better than
  doing nothing (bt bottom line 2).
- **What the literature and the investors add:** see section 4.
- **Alternative B: sell everything now.** It is the lowest-risk choice and fully defensible. It
  gives up the small expected drift (about 0.1-0.2% for Oslo holdings, about 0.7-1.4% for
  US/tech in the post-hoc sample) and saves one commission. The playbook stages because the goal
  is to avoid a bad sale day and ideally sell higher: the half you keep is the chance to sell
  higher, without a limit order.

### 6.2 The rules, step by step

**Step 0. Prepare (this week).**

- List each holding, the index it follows (table 5.2), whether it is a share or a fund, and
  where it is held: the dates in step 3 differ by type and platform.
- An exchange-traded fund (ETF) counts as a share here: it trades on the exchange, settles like
  a share (T+2) and has no fund cut-off, so it follows the share rows in step 3, not the fund
  rows. Only funds you buy and sell through the fund manager (no exchange price during the
  day) take the slower fund path.
- Funds: note each fund's order cut-off time (brokers usually show it in the order window;
  e.g. 09:00, 11:00 or 13:00). An order after the cut-off goes the next business day.
- Broker: check where and how fast it pays out the proceeds, and whether any optional
  withdrawal delay is switched on. Note your commission (section 6.3).
- Commissions, fund cut-offs and settlement times vary by broker: check yours. If proceeds
  settle in another currency, set up the route to convert them to euros now; a first transfer
  can be slowed by checks, and a small test transfer early on shows how long each hop really
  takes (park section 4).
- Have the Dutch receiving account ready: a savings account, or the Dutch broker account you
  will buy back with (section 7).

**Step 1. First sale (your start day, e.g. Thu 19 Nov).** On the evening before, refresh the
readings (section 5.1). Then, for each holding:

- **Its index's last close was below its 200-day average:** sell all of that holding.
- **It was above:** sell half (by value). The rest follows step 2.
- **Example with the 18 Nov readings:** US, global and tech holdings: all (the S&P was below
  by only 0.31%, the Nasdaq by 2.9%); Oslo holdings: half. If the S&P has closed back above its
  line by the evening before your start day, the trigger has not fired for US and global
  holdings: sell half and treat the rest under step 2.

What was tested, exactly (bt review fixes, point 3): the rule sells half at the close of day 0
(your start day), and the rest at the close of the next trading day after the first close below
the 200-day average from day 0 on; if no close from day 0 to day 21 is below, the rest goes on
day 22. Closes before day 0 are not looked at. So "sell all on day 0 because the index is
already below" is not literally the tested rule: it moves half the position one day earlier,
which made a difference of a fraction of a percent in the past (post-hoc sub-samples). Once
fired, the rule stays fired: a close back above the line after that changes nothing. It acts on
the first close below, even by a hair; a version that waits for two closes below was tested only
over years (bt amendment, Part B), not in the six-week test. A US index closes at 22:00 CET,
after the European markets, so you act on it the next European trading day; that is the test's
one-day lag, but the price differs (not modelled). For a fund, "sell now" means: order in before that day's cut-off.

**Step 2. Watch (each trading evening, about two minutes, until the day before your fallback:
Thu 17 Dec for shares, Thu 10 Dec for funds).**

For each holding still unsold: did its index close below its 200-day average today?

- Yes: sell the rest of that holding on the next trading day (a fund: before its next cut-off).
- No: do nothing. Do not move the date to wait for more.
- After everything is sold, the index's moves no longer matter for the sale. Do not buy back
  because it climbs back above its line: buying back follows section 8.

**Step 3. Fallback: sell everything still held** (park section 7.3). "Last safe" means the worst
case still reaches your Dutch account by Wed 30 Dec, with Thu 31 Dec spare. The fallback is the
plan; the last-safe day is for a missed fallback.

| Holding (by when the cash is at the broker) | Fallback | Last safe day (fund: order in before the cut-off) | Worst-case cash in NL if sold on the fallback / last-safe day |
|---|---|---|---|
| Shares, cash at the broker 2 trading days after the sale (T+2, Oslo Børs calendar) | **Fri 18 Dec** | **Mon 21 Dec** | Tue 29 Dec / Wed 30 Dec |
| US shares (cash at the broker T+1) | **Fri 18 Dec** | **Mon 21 Dec** | as T+2 shares or a day earlier |
| Nordic fund, cash at the broker within 2-5 business days of the order | **Fri 11 Dec** | **Wed 16 Dec** | Wed 23 Dec / Wed 30 Dec |
| Non-Nordic or global fund, cash at the broker within 2-6 business days of the order | **Fri 11 Dec** | **Tue 15 Dec** | Mon 28 Dec / Wed 30 Dec |
| Any fund, cash at the broker within 5-10 business days of the order (slow platform) | **Fri 4 Dec** | **Wed 9 Dec** | Wed 23 Dec / Wed 30 Dec |

Assumptions (park section 7.3; every row uses the same chain, `report_checks.py`): "2-5",
"2-6" and "5-10" days mean the cash is at your broker within that many business days, counted
from the day the order goes to the fund manager; platforms quoting such figures call them
"normal" and do not guarantee a date; after that, the broker pays out within 2 bank days at worst; converting and moving the
money to a Dutch account takes 1 day; fund days skip 24, 25 and 31 Dec (and 28 Dec for global
funds). A fund may be allowed by its rules to take up to two weeks to pay a redemption, which is
why the fallback, not the last-safe day, is the plan. Commissions, fund cut-offs and settlement
times vary by broker: check yours, and if unsure, use the slower row. If your platform's figure
is the day the cash reaches your bank account (not the broker), drop the 2 payout days: the
dates above then have that much spare. For a 5-10 day fund, step 2 ends Thu 3 Dec; a 5-10 day
global fund that skips 28 Dec has the same dates, because its tenth day falls before Christmas.

Shares sold later than 21 Dec: Tue 22 Dec settles Mon 28 Dec (no spare day); Mon 28 Dec is the
last sale that certainly settles in 2026 (Wed 30 Dec), with the cash likely in January; Wed 30
Dec is the last Oslo trading day and settles Mon 4 Jan 2027.

Calendar: Oslo Børs is closed on Thu 24 and Thu 31 Dec. Funds on the Oslo calendar (dealing
calendars read from three fund companies) do not deal on 24, 25 or 31 Dec, and global funds also not on Mon 28 Dec (some also not on Thu 26 Nov, US
Thanksgiving). Whether VPS (the Oslo settlement system) settles share trades on 31 Dec is
unverified. Other exchanges have their own holiday calendars (sources, section 11.2). Source:
park sections 3.4 and 7.1.

**Step 4. Move the money (after each sale).**

1. Shares: two trading days after the sale, the cash settles at the broker (US shares: one).
   Funds: the cash reaches the broker after the fund's settlement time (2-5, 2-6 or up to 10
   business days after the order).
2. Pay it out, or move it, to the account where you will park it (section 7). Check your
   broker's payout rules and times.
3. If the proceeds settled in another currency, convert them to euros the same day. Low-cost
   transfer services charge well under 1%; bank markups can be higher (unverified).
4. Do not hold the other currency to wait for a better rate. The risk you are guarding against,
   a crash, is the moment the currency of a smaller market tends to fall hardest (section 5.3).

US shares: the proceeds are in dollars; convert them to euros too. A broker's automatic
conversion often costs more than a manual one; check yours (park section 7.4).

**Step 5. Park the euros** (section 7).

### 6.3 Costs and how many tranches

- **Commissions vary by broker: check yours.** Each holding sold on each date is one trade. On a
  small portfolio a minimum or fixed commission per trade matters more than the percentage rate:
  a fixed fee of EUR 3 per trade (DEGIRO's EUR 2 + 1 on Euronext Amsterdam, section 8.2) is 0.3%
  of a EUR 1,000 order and 0.03% of a EUR 10,000 order. Some brokers offer cheaper commission
  classes for small orders; switching may take time.
- **So: two tranches.** Staging's expected gain is small (0.1-0.4 points, section 6.1) and its
  risk benefit comes with two steps; where each trade costs a tenth of a percent or more of the
  order, more than 2-3 trades in total eats the gain.
- **Several holdings.** To keep the trade count down, sell whole holdings rather than half of
  each: with four holdings of similar size, two now and two later is 4 trades instead of 8.
  This works like staging only if the holdings move roughly together (same market). That is
  reasoning, not a tested rule.
- **US shares** may carry a higher minimum commission than home-market shares, plus a currency
  conversion fee (automatic conversion often costs more than manual; park section 7.4).
- **Funds.** Some platforms sell funds without commission (some funds charge), in which case the
  tranche count costs nothing for funds. Funds do not settle T+2: see step 3.
- **Order type for thin Oslo stocks** (reasoning, not a tested result; park section 7.5): use a
  limit order, never a market order. Check the order book first: if your quantity fits within
  the volume at the best bid, a limit at the best bid sells at once; if not, sell in two or three
  slices during the day, or place the limit one or two ticks below the bid and accept the spread
  as the cost. On the fallback day do not set a limit far above the bid: an unfilled order means
  no sale. At some brokers, "Fill and Kill" and "Fill or Kill" orders do not work in the opening
  or closing auction.
- **Currency.** Converting non-euro proceeds costs from well under 1% at a low-cost transfer
  service to perhaps 1-2% as a bank markup (unverified). Both are small against the moves of a
  smaller market's currency: EUR/NOK ranged 10.31-11.00 between Aug and Nov 2026 (6.7%). Convert
  non-euro proceeds promptly.
- **Total:** commissions plus conversion depend on your broker and currency route; add them up
  for your own holdings before choosing more than two tranches.

### 6.4 The checklist (one screen)

```
PREP (this week)
[ ] Each holding -> its index (Oslo = OSEBX | US/global = S&P 500 | tech = Nasdaq),
    share/ETF or fund (an ETF follows the share dates), and platform. Funds: note the cut-off
[ ] Broker: payout route and times known, any withdrawal delay off, commission noted
[ ] Non-euro proceeds: conversion route to euros ready; Dutch account ready; optional test transfer

SELL
[ ] Evening before your start day: refresh readings (bt_now.py --fetch, or a 200-day chart)
[ ] Start day (e.g. Thu 19 Nov), per holding: index closed below its 200-day average?
        yes -> sell ALL of it      no -> sell HALF
        (18 Nov example: US, global, tech below -> all; Oslo above -> half)
[ ] Each evening until the day before the fallback: index closed below its 200-day average?
        yes -> sell the rest the next trading day (fund: before its cut-off)
[ ] Fallback, sell everything left:
        shares Fri 18 Dec (missed it: Mon 21 Dec is the last safe day)
        funds  Fri 11 Dec (last safe, cash at broker in 2-5/2-6 days: Nordic Wed 16 Dec,
               global Tue 15 Dec; cash at broker in 5-10 days: fallback Fri 4 Dec,
               last safe Wed 9 Dec)
[ ] Thin Oslo stock: limit order at or just below the best bid, never a market order

MOVE (after each sale)
[ ] Cash at the broker (shares +2 trading days; funds +2-6, slow ones up to +10 business days)
    -> pay out / move to your Dutch account
[ ] Same day: non-euro proceeds -> EUR. No waiting for a better rate.

PARK
[ ] EUR savings account (deposit guarantee) or EUR overnight / 0-1y govt ETF at your Dutch broker

DON'T
[ ] no "only at a higher price" limit orders   [ ] no buying back because the index bounces
[ ] no gold, Berkshire, long bonds or dollars as the safe part
```

## 7. Where to park the money

The goal is crash safety, including the first days of a crash. The haven lane measured how each
candidate behaved in 10 crashes (1929-2025), for a dollar and a euro holder; the park lane
collected the Dutch products, guarantees and costs.

### 7.1 The options

"Worst in past crashes" = the largest fall seen in the euro view (1999 on) or the dollar view
where no euro data exist (`lanes/haven-table.md`). Yields read 2026-11-15/18 (park section 2).

| Option | Yield now | Worst in past crashes | Main risks | Cost | Minimum | Back into stocks |
|---|---|---|---|---|---|---|
| **Dutch instant-access savings** (ING / Rabo / ABN / ASN / Triodos) | 1.10 / 1.52 / 1.25 / 1.30 / 1.16% (Keuze.nl, 15 Nov) | Never down in any crash (3-month Euribor cash: at worst -0.1% over 2022 from negative rates) | Bank failure: covered to EUR 100k, but up to 7 working days without access; inflation | 0 | 0 | SEPA to the broker: same day to 1 bank day |
| bunq savings | 3.11% promo for 6 months, then 1.55% (Keuze.nl) | Same | Same; promo ends | 0 | 0 | Same |
| **Broker cash at the ECB rate** (e.g. Trade Republic) | 2.50%; 4% promo for new customers on the first EUR 20k until 1 Mar 2027 | Cash: never down | Held at partner banks; which guarantee covers which part is unverified | 0 | 0 | Instant inside the broker |
| **EUR overnight-rate ETF** (Xtrackers XEON, Amundi CSH) | Tracks the overnight rate; XEON 1-year +2.11% | XEON: -0.5% at worst (2020, negative rates) | Synthetic: swap banks (loss capped at 10% of value by UCITS, DWS aims under 5%); not a deposit; broker failure (securities held apart; EUR 20k scheme) | TER 0.10%/yr + broker fee | 1 share (about EUR 150, unverified) | Sell in seconds; cash usable at once at most brokers; settles T+2 |
| **iShares EUR Govt Bond 0-1yr** (IEGE, Euronext Amsterdam) | 1-year +2.03%; worst fall in the last year -0.07% | -4.91% since launch, from the negative-rate years | Tiny rate risk; holds the bonds itself (no swap) | TER 0.07% + DEGIRO EUR 2 + 1 | 1 share | Same |
| Euro govt bonds 1-3 years (ETF DBXP / IBGS) | IBGS 1-year +0.77% | DBXP -3.1% (2020), -4.6% (2022); IBGS 2022 -4.29%, -6.10% since launch | Rate risk; the ECB is raising rates (next meeting 17 Dec, markets price a hike, forecast) | TER 0.10% + broker fee | 1 share | Same |
| Fixed-term deposit | ABN 1y 2.25%; Santander 1y up to 2.90% | Never down | Money locked: you cannot buy the dip | 0 | EUR 1,000 typical | Only at maturity |
| Gold ETC (iShares Physical Gold, Xetra-Gold) | n/a | In euros: -16% (Lehman weeks), -12.6% (2020), -11.6% (2022); in dollars -22% (Sep-Nov 2008), -11.8% (9-18 Mar 2020) | Liquidity selling in the crash itself; dollar; 15-20% yearly swings | TER 0.12% (Xetra-Gold 0.36%/yr) + fee | 1 unit | T+2 |
| CHF (Swiss franc) | about 0% interest | Ended up against the euro in all 7 euro-era crashes, but -9% along the way in 2007-09 | A currency bet; central-bank jumps | not researched | not researched | Must convert back |
| Berkshire Hathaway B | n/a (stock, about USD 572 on 6 Nov) | In euros -43.6% (2007-09), -30% (2020) | A stock; dollar; succession | DEGIRO round trip: 0.5% plus EUR 4 (EUR 1 + 1 per trade, 0.25% FX each way) | 1 share | US T+1, then FX back |
| Long euro govt bonds (10y+) | n/a | -32.6% (2022), -10.3% in March 2020 | Inflation, rising rates, dash for cash | ETF fee | 1 share | T+2 |
| US T-bills / dollars | n/a | In euros -15.3% (2000-02), -13.3% (2007-09) | The dollar can fall with US stocks (2025) | FX each way | | |

### 7.2 Guarantees, and what can still go wrong

- **Deposit guarantee:** EUR 100,000 per person per bank, paid within 7 working days. When
  Amsterdam Trade Bank failed on Fri 22 Apr 2022, compensation was available within 7 working
  days and 95% was paid within a month (De Nederlandsche Bank). It covers savings and current accounts, not
  securities.
- **Investor compensation:** up to EUR 20,000 if a Dutch broker fails and your securities or cash
  cannot be returned. Client securities are held apart from the broker's own assets. Market
  losses are never covered (Rijksoverheid, De Nederlandsche Bank).
- **Money funds can break in a crash.** The Reserve Primary Fund fell to 97 cents on 16 Sep 2008
  and held back redemptions (SEC). In March 2020, euro-area funds holding company paper (LVNAV)
  had outflows of about EUR 85bn (16% of assets) in two weeks, while government-only funds had
  inflows (ECB Macroprudential Bulletin 12). Prefer a deposit, a government-only fund, or an
  overnight product backed by several large banks over a "prime" money fund.

### 7.3 What the evidence supports

1. **First choice: euro cash.** A Dutch savings account under the guarantee, or a euro
   overnight-rate or 0-1 year government ETF. Euro cash lost at most about 0.5% in any crash
   window measured, including the first days: a savings account at a rate of zero or more cannot
   fall; the overnight-rate ETF XEON lost 0.5% at worst in 2020 and 3-month Euribor cash 0.2% at
   worst in 2022, both from negative rates (haven).
   The 0-1 year ETF IEGE was not in the crash table; it has lost 4.9% in total since launch,
   over the negative-rate years rather than in one crash, and 0.07% at worst in the last year.
   Cash also keeps the full amount ready for buying back.
2. **Practical pick:** if you will buy back through a Dutch broker, holding XEON/CSH or IEGE in
   that account lets you switch in seconds; IEGE avoids the swap. If you want no product risk at
   all, a savings account costs about one bank day to move.
3. **The yield gap is small.** Six months at 2.5% versus 1.1% is 1.25% versus 0.55% of the
   amount parked (rate x 0.5).
4. **Not parking:** gold, long bonds, dollars, JPY and Berkshire are bets on the kind of crash.
   CHF was the best-behaved non-cash asset for a euro holder, but it is a currency position.
   Money held in any other non-euro currency is not parking either.

## 8. Buying back in

### 8.1 What the evidence says

- **Busts after real bubbles last long.** S&P 500, price only: 1929 -86% over 32 months; 1973-74
  -48% over 21 months, 69 months back to the old peak; 2000-02 -49% over 31 months, 56 months
  back; 2007-09 -57% over 17 months, 49 months back. The Nasdaq needed 15.1 years to regain its
  2000 peak; Japan's Nikkei 34 years (1989 to 2024). The quick recoveries of 2020 and 2022 came
  after busts from lower valuations and are not a fair guide (reentry Part 1).
- **Buying at -20%, -30%, -40% from the high** (12 S&P bear markets 1929-2022): after a buy at
  -20%, the market fell 10% or more further in 42% of cases; 5 years later it was up a median
  34%. In bubble busts the losses kept going: a buy at -40% in Nov 1929 still lost 51% over five
  years, and Nasdaq buys at -20/-30/-40% in 2000 fell another 63-70%.
- **Bottom signals are late or early, never exact.** The first month-end close above the
  10-month average came a median 3.9 months after the low, about 20% above it. VIX peaked 7-219
  days before the low (2008: 80.9 on 20 Nov 2008, low on 9 Mar 2009). The credit spread peaked on
  the day of the low in 2002 and 2020, but 43-103 days before it in 1987, 2008 and 2022.
- **The Fed's first rate cut is not a buy signal:** after the first cut on 3 Jan 2001 the S&P
  fell a further 42%; after 18 Sep 2007, a further 56%.
- **Waiting for "cheap" means waiting a decade.** Lagged CAPE was last at or below its long-run
  median (now 18.1) in Nov 2008 - Jun 2009.
- **No re-entry rule beat buying back at once** (card `research/cards/reentry.md`, fixed
  before any number; 7 rules, S&P 500 total return, 10-year horizon, sales in high-CAPE months
  1928-2016: 390 months but only 8 separate episodes). Sold exactly at the named tops (1929,
  1937, 1968, 1972, 1987, 2000, 2007), no waiting rule lost: 1.0-3.3 times the wealth of buying
  back at once (in Feb 1937 most rules tied at 1.0, because the market was still far below its
  1929 high and they bought back at once). Sold 2-3 years early (Dec 1996, Dec 1997), they mostly
  lost (0.64-0.97 times). Waiting with no deadline had a worst tenth of 0.33-0.52 times; a
  24-month deadline lifted it to 0.72.
- **Lump sum versus spreading:** a lump sum beat spreading over time about two times in three
  (Vanguard 2012 and 2023: 68%, 1976-2022). Spreading still beat staying in cash, and staying in
  cash hurt most in our test.
- **The investors:** the money was made by deploying into panic with rules made in advance, and
  they were early there too. Buffett's "Buy American. I Am." op-ed of 16 Oct 2008 came 28.5%
  before the S&P low; Oaktree invested about USD 600m a week in the last 15 weeks of 2008 (inv).
  Those who called the top and had no re-entry rule stayed out through years of gains
  (Grantham, Hussman).

### 8.2 A re-entry rule set the evidence supports

No rule adds return. A plan can only limit two regrets: buying back just before the crash, and
never buying back.

Both rules below come from the reentry card (fixed before any number) and were tested the same
way: sale in a month, cash earns T-bills, decisions at month-end closes, wealth after 10 years
against buying back at once (R; above 1 = better than buying back at once). Side by side, in the
same samples (`lanes/reentry-rules.txt`, S&P 500 total return, 1928-2016 starts):

| R after 10 years vs buying back at once | `dca12`: 12 equal monthly buys | `staged-24`: thirds at -20/-30/-40%, rest at 24 months |
|---|---:|---:|
| High-valuation months (sample B, the one that fits Nov 2026; 390 months, 8 episodes): median | **0.97** | 0.92 |
| same: worst tenth (the regret measure) | **0.90** | 0.72 |
| same: share of months with R above 1 | 31% | 35% |
| same: mean | 0.99 | 0.97 |
| Sample B from 1972 (249 months, 3 episodes): median / worst tenth | 0.97 / 0.90 | 0.90 / 0.68 |
| Sold at a top before a real bust (Aug 1929, Nov 1968, Dec 1972, Mar 2000, Oct 2007) | 1.09-1.34 | **1.40-1.61** |
| Sold 2-3 years early (Dec 1996, Dec 1997) | 0.88-0.93 | 0.64-0.71 |
| All months (sample A, 1,066 months): mean | 0.98 | 0.96 |
| Nasdaq, high-valuation months (robustness, 3 episodes): median / worst tenth / share above 1 | 0.96 / 0.86 / 35% | 0.89 / 0.69 / 5% |

So in the sample that fits today, the 12 monthly buys did better on the median and clearly
better in the bad tail. The thirds won only when a real bust followed the sale, and by a lot.
Neither rule beat buying back at once; both are ways to limit regret.

1. **Default: 12 equal monthly buys** (`dca12`), the first in January 2027 and the last in
   December 2027, whatever the market does. In the test the first twelfth was bought at the
   close of the sale month; starting one month later is a small shift that was not tested.
   Its own end date is the deadline: fully back in stocks after 12 months.
2. **Alternative, a bet that a real bust comes:** buy in thirds (`staged-24`): one third at the
   first month-end close of the S&P 500 20% below its all-time high, one third at 30%, one third
   at 40%, decided at month-end closes as tested; whatever is left goes in by the deadline, 24
   months after the sale: 31 Dec 2028 is a Sunday, so **Fri 29 Dec 2028** (2028 exchange
   holidays not checked). From the 6 Oct 2026 closing high of about 7,819 the levels are about
   **6,255 / 5,473 / 4,691** (`report_checks.py`); if the index makes a new high first, the
   levels move up. On 18 Nov it was 6.3% below its high. Choose this only if you accept the bet:
   a belief that the AI boom is a bubble that will burst within two years is such a bet. In the
   test it cost more than the monthly buys in the typical high-valuation month and in the worst
   tenth, and it paid off only in the five real busts.
3. **Signals may only bring purchases forward, never delay them:** VIX above about 45, a peak in
   credit spreads, or a close above the 200-day average after a 30% fall can bring forward a
   third that is due or the remaining monthly buys (an add-on that was not tested). The Fed's
   first cut and "CAPE back to its median" are not buy signals.
4. **Write the rule down now** and follow it mechanically. A -20% fall can become -50% to -80%
   (1929, 2000), and a fall can arrive only after the market has doubled (1996).

Notes: the thresholds were tested on the S&P 500 in dollars. If you buy a global or European
fund in euros, the S&P levels are a proxy (not tested in euros), and a dollar fund adds
currency risk (section 7). Buying costs at DEGIRO on Euronext Amsterdam: EUR 2 + 1 per trade,
so three buys about EUR 9 and twelve about EUR 36 in total, whatever the amount; ETFs in its
"core selection" cost EUR 1 per trade (which ETFs are included is unverified).

## 9. Commonly heard ideas, assessed

These ideas are often heard in markets like this one. They are assessed after the evidence
above, against the same literature and data.

### 9.1 A big IPO wave as a top signal

- **Partly true, weak as a timer.** IPO waves come in late bull markets and IPOs almost vanish in
  busts. Of the 11 years since 1980 with at least 300 IPOs (Ritter's count), a bear market began
  within two years after 4 (1986, 1999, 2000, 2021) and not after 7. Measured from the end of
  the year when deal counts peaked to the next market top, the lead time ranged from 0 (2000,
  2021) to 39 months (the record count of 1996 to the March 2000 top); 1996 is not one of the
  four years above, because the top came more than two years later. 2007's top came with no
  wave. The 300 threshold was
  chosen after seeing the table: a description, not a tested rule (reentry Part 2).
- **First-day returns did a little better:** every year with a mean first-day return of 30% or
  more (1999, 2000, 2020, 2021) came less than two years before or during a top; 2022 (48.9% on
  38 deals in a falling market) was the exception. 2025's 29.3% sits just under the line. Four or
  five episodes prove nothing.
- **The research behind it:** issuance in a hot industry raises crash odds (Greenwood-Shleifer-
  You 2019); the equity share of new issues predicted market returns 1928-1997 (Baker-Wurgler
  2000; its later out-of-sample record unverified). Pastor-Veronesi (2005) give a rational
  reading: firms go public after strong returns, so a wave does not prove a bubble (section 2.1).
- **"Almost no IPOs at bottoms": true, but useless for buying.** IPO counts stay low for 1-2
  years after the low (2003: 63 IPOs while the S&P rose 26%; 2009: 41).
- **2026:** 123 IPOs and USD 149bn raised to 18 Nov (Renaissance Capital): a record in dollars,
  above 2021's USD 142.4bn from 397 IPOs. SpaceX (merged with xAI) raised about USD 75bn on 11 Jun
  2026, the largest IPO ever. By number of deals 2026 is not hot: a third of 2021, a fifth of
  1996. It looks like a few giant private firms cashing in, not hundreds of small unprofitable
  ones doubling on day one.
- **Anthropic:** Nasdaq lists ANT to start trading on Thu 19 Nov 2026 (Nasdaq Trader notice of
  11 Nov). Its reported range of USD 70-78 for 825m shares is unverified until priced. One big
  listing is a data point in the record-dollars story above, not a separate signal.
- **Buying hot IPOs is a separate, poor bet:** IPO firms trailed the market by about 5.5% a year
  over three years (Ritter, 1980-2024; Loughran-Ritter 1995).
- **Verdict:** a late-cycle warning that supports having an exit and a re-entry plan. It is not a
  sell date and not a reason to stay in cash for years.

### 9.2 Berkshire Hathaway as a defensive holding

- **Lower-beta stock, not a crash haven.** Beta to the S&P 0.66 (2000-2025), 0.81 (2016-2025). In
  the slow tech bust it shone: calendar 2000-02 about +30% against the S&P's -38% (Berkshire 2024
  letter). In liquidity crashes it fell nearly as far: -54% vs -57% (2007-09) and -29% vs -34%
  (Feb-Mar 2020); -18.5% on Black Monday 1987; -10.9% on day one of the worst 2008 leg (inv,
  haven).
- **For a euro holder it adds the dollar:** -43.6% at worst in euros in 2007-09. Costs at DEGIRO
  0.5% of the amount plus EUR 4 per round trip (EUR 1 + 1 per trade, 0.25% FX each way); one share about USD 572 (6 Nov 2026).
- **Changes:** Buffett stepped down as CEO at the end of 2025; Greg Abel is CEO from 1 Jan 2026,
  and Buffett stays chairman (AP, 28 Feb 2026, in inv). Berkshire turned net buyer in Q2 2026.
  Cash about USD 357-377bn at end-Q3 2026, depending on the measure. A blog claim that Howard
  Buffett now chairs the board (TIKR, in park) is not confirmed by any other source (section 10.1).
- **Verdict:** if you want some lower-AI stock exposure while waiting, it is a reasonable one, but
  count it as stock, not as the safe part (2026 to 17 Nov: BRK-B +16.7%, S&P +7.2%).

### 9.3 A savings account until the bubble pops

- **Supported:** euro cash lost at most about 0.5% in any crash measured, less than any other
  candidate (section 7), and it keeps the money ready for buying back.
- **The risk is the pop coming late or never.** After the Shiller/Greenspan warning of Dec 1996
  the S&P doubled, and even the 2002 low (777) was above the warning-day close (744). After
  Grantham's "superbubble" call of 5 Jan 2021 the S&P was 97% higher by 17 Nov 2026. That is why
  the re-entry plan has a deadline.
- Inflation is a small cost over months (cash lost about 5% in real terms over 1973-74).

### 9.4 Bonds with a small amount

- **Reachable:** bond ETFs need one share; Dutch state bonds can be bought through a broker "for
  any euro amount" (DSTA), though retail bond quotes may be thin (unverified).
- **Short euro government bonds** are fine for months: a 0-1 year ETF behaves like cash; 1-3 years
  fell at worst 3-5% (2020, 2022). With the ECB raising rates, 0-1 years beats 1-3 years for
  parking.
- **Long bonds are a bet on the kind of crash:** they won big in deflationary busts (US 10-year
  +40% over 2000-02, +22% over 2007-09) and lost big in the inflationary one (long Bunds -32%,
  US 30-year -30% in 2022).
- Holding a single bond only makes sense if it matures inside your waiting window.

### 9.5 Side topics, as they came up

- **Nvidia:** -35.0% from 6 Oct to 17 Nov (confirmed in bt). Company-specific news was not
  researched. While parked in euro cash, the plan holds no AI, data-centre or hyperscaler
  stocks anyway.
- **What the investors say about AI now (talk, not timing):** Grantham (Jan 2026): "slim to none"
  chance the AI bubble does not burst. Marks (Dec 2025): neither all-in nor all-out, "a moderate
  position". Burry held puts on Nvidia and Palantir at 30 Sep 2025; his profit or loss cannot be
  seen.

## 10. What the evidence cannot settle

### 10.1 Contradictions between lanes, reconciled

| Topic | Lane A | Lane B | Resolution |
|---|---|---|---|
| CAPE now | 39.37 (bt: Shiller's own figure, Nov 2026, price 12 Nov, unlagged; 98.3rd pct since 1881) | 39.8 (bt, earnings lagged 3 months); 39.7 (reentry, earnings lagged 3 months and CPI 1 month; 97th pct of lagged values since 1928) | Same data, different lag and base period. The report quotes 39.4 (Shiller) for "now". All say near-record. |
| Berkshire 2007-09 | -53.9% (inv: BRK-B, its own peak 10 Dec 2007 to 5 Mar 2009) | -51.5% own fall, -40.3% S&P peak to S&P trough (haven: BRK-A, S&P window from 9 Oct 2007) | Different share class and window. The report uses -54% (own peak to trough). Same message. |
| Berkshire 2020 | -29.4% (inv, BRK-B) | -30.2% (haven, BRK-A) | Share class. |
| Oslo in 2008 | -65% (bt: OBX in NOK, 22 May - 21 Nov 2008) | -61.7% (haven: OBX in EUR over the S&P's 2007-09 window; own max drawdown -69.6%) | Different window and currency. The euro figure is the one that matters to a euro investor. haven's first figures (-69.2%, -80.5%) came from a currency-conversion bug, fixed in review round 1. |
| Gold in the Lehman weeks | -22% (haven, dollars, gold futures own fall) | -16% (haven, euros) | Currency. |
| Short euro govt bonds | -3.1% / -4.6% (haven: DBXP, 2020/2022 own falls) | -4.29% (2022) and -6.10% since launch (park: IBGS) | Different products and windows. Both say: a few percent at worst. |
| Trend following in big drawdowns | Positive in 8 of 10 (lit, full text of Hurst-Ooi-Pedersen) | "8 or 9" (haven, summary) | Use 8 of 10. |
| Spare day | bt: 30 Dec as a spare day | park: a 30 Dec sale settles Mon 4 Jan 2027 | 30 Dec is not a spare day for cash in 2026; Mon 21 Dec is the spare for shares, Tue 15 / Wed 16 Dec for funds with cash at the broker within 2-6 business days, Wed 9 Dec within 5-10. |
| Drawdown and volatility exits | lit ranks a drawdown stop 2nd and VIX/credit as confirmers | bt: trailing stops and the VIX trigger failed the six-week bar (they rarely fire in time) | Not used for the sale. Over years, drawdown stops do protect (bt Part B). VIX/credit are kept only to bring a re-entry tranche forward. |
| S&P distance from its high | -2.9% on 12 Nov (reentry) | -6.1% on 17 Nov (bt) | Different dates. inv's "-9.1% in 2026" is another measure: the deepest fall within calendar 2026 (its script). |
| Berkshire chair | Buffett stays chairman, Abel CEO from 1 Jan 2026 (inv: AP via NY1, 28 Feb 2026; also the reviewer) | Howard Buffett now chair (park: one TIKR blog post) | **Resolved for the sourced date:** Buffett was chairman at 28 Feb 2026 (AP). The TIKR claim has no second source (unverified). It does not change the verdict. |
| Shiller's Fed briefing | 3 Dec 1996 (inv, from his book, page unverified) | date unverified (reentry) | Treat the date as unverified. Greenspan's speech, 5 Dec 1996, is sourced. |

### 10.2 Few episodes and choices made after seeing results

- **Few independent cases.** Exit rules: 8 crashes since 1929. The six-week test: the `late`
  sample has 2,739 start days, about 98 windows from only 20 separate spells (OSEBX: 10 spells).
  Re-entry: 8 high-valuation episodes since 1928, only 3 since 1972. Read the tables as a few
  dozen observations at most.
- **Post hoc (chosen after results were seen):** the headline combination "half now, rest on the
  fallback or a 200-day break" (bt amendment); the `now-like` sample, the only one that fits US
  and tech holdings now, and its below-the-200-day split (card amendment 2); the 300-IPO
  threshold; the 10-firm filter in the GSY replication. The `late` sample was itself defined to
  fit November 2026 (stated on the card). The re-entry default (12 monthly buys rather than the
  thirds) was picked from the card's results in review round 2: both rules were on the card,
  the choice between them was made after seeing the table.
- **Card timestamps:** the exit-rules card's stated times ("~19:30" and "~20:30 UTC") were wrong;
  the commits are 18:50 and 19:01 UTC. A dated correction is on the card (amendment 2), with the
  old text left as it was. The order card-before-numbers holds in git.
- **Many comparisons:** six-week test, 15 strategies x up to 14 sample cuts (plus 18 post-hoc
  robustness rows in review round 1); crash test, 16 rules x 9 episodes. Some favourable cells
  are luck.

### 10.3 What the tests did not cover

- Currency moves (e.g. NOK/EUR for Oslo) in the exit backtests; fees and spreads; dividends (price indexes, about 0.1%
  over six weeks); interest on cash in the exit tests (cash earns 0).
- Global (MSCI World) funds and single stocks. Oslo indexes have short histories (OBX from 2004,
  OSEBX from 2013). Both lanes treat OBX/OSEBX as total-return indexes; that was not verified.
- The intraday timing of a real sale: the test books the index close of the day after a signal,
  while an Oslo sale or a fund's cut-off prices earlier in the day.
- Funds' shorter window. The test's forced sale is on trading day 22 (Fri 18 Dec). The fund
  fallback, Fri 11 Dec, is trading day 17 from 18 Nov (16 from a 19 Nov start), and the slow-fund
  fallback, Fri 4 Dec, is day 12. No window of those lengths was run, so for funds the six-week
  statistics in section 6.1 apply only roughly (a shorter wait usually means a narrower spread
  of outcomes and less of the small expected drift; not tested).
- The VIX trigger's `late` statistics cover 1990 on only (VIX data); on the S&P that is 2,340 of
  2,739 `late` start days.
- The high-yield credit spread and the GSADF bubble test (data or tools not available). The Oslo
  versions of the VIX and credit rules are invalid (a calendar bug, flagged in bt and in
  `tries.md`).

### 10.4 Practical items not verified

Broker payout times and commission classes (they vary by broker: check yours); whether a fund
platform's "2-5" / "2-6" / "5-10" days count from the order day (assumed) or the trade date, and whether
fund cash is withdrawable the day it shows; other fund platforms' settlement wording and payout
times; whether VPS settles share trades on Thu 31 Dec (Oslo Børs and the funds are closed);
current bid-ask spreads of Oslo small caps and the closing-auction times; banks' FX markup on
transfers; which guarantee covers Trade Republic cash at each partner bank; which ETFs are in
DEGIRO's core selection; XEON's swap basket; IBKR, Saxo and Dutch bank broker fees; the price
of one XEON share; Anthropic's final price and size; the SK hynix ADR size; OpenAI IPO timing.

### 10.5 Literature figures read only from summaries or memory

Faber's 10-month performance numbers; Zakamulin's "80% of out-of-market spells underperform";
Dichev's return gaps; Huang-Jiang-Tu-Zhou out-of-sample R²; Kaminski-Lo thresholds;
Brunnermeier-Nagel's "tech exposure peaked Sept 1999"; Baker-Wurgler's post-1997 record;
Kritzman-Turkington (read via a summary) and the practitioner concentration studies;
Fisher-Statman on the AAII survey; Cochrane's R² figures; Bouman-Jacobsen (from memory);
Campbell-Shiller, Goyal-Welch 2008, Baker-Wurgler 2006, Abreu-Brunnermeier and Pan-Poteshman
(cited from memory, standard results); Burry's +489% (source page unverified); the
Druckenmiller 2000 trade size; Templeton's profit; Oaktree's and Baupost's 2008 numbers.

### 10.6 The big unknown

Whether the current US correction is the start of the pop. No reading in section 5 can settle
it, and the literature says none can (lit section 4; Abreu-Brunnermeier 2003). The playbook is
built to give an acceptable result either way, not to call it. Whether trade date or settlement
date counts for a given deadline is outside this research; selling by the last-safe day for
each holding (section 6.2, step 3) puts both in 2026.

## 11. Sources and map to the work

### 11.1 Map: report section to lane notes, scripts and logged tests

| Report section | Lane notes | Scripts (`scripts/`) | Card / logged tests |
|---|---|---|---|
| 2 Literature | `lanes/lit.md`; `lanes/haven.md` (literature part); `lanes/gsy-replication.md` (copy from branch `gsy-1`, commit 35d155f); drafted in `lanes/report-sections-ABC.md` (section A) | `bt_amend.py` (GSY screen) | gsy-1: card `cards/gsy-runup.md` and `research/gsy-1.md` on branch `gsy-1`; own crash tests: as for 6 |
| 3 Investors | `lanes/inv.md`; drafted in `lanes/report-sections-ABC.md` (section B) | `inv_drawdowns.py`, `inv_burry_check.py` | Not logged |
| 4 How the playbook follows | sections 2-3 and the lanes behind 6-8; drafted in `lanes/report-sections-ABC.md` (section C) | as for 6-8 | as for 6-8 |
| 5 Readings | `lanes/bt.md` Part C, amendment (GSY screen, checks), "Review round 1 fixes" points 1, 4, 5 | `bt_fetch.sh`, `bt_data.py`, `bt_now.py` (`--fetch`) | Descriptive, not logged |
| 6 Exit playbook | `lanes/bt.md` Part A, amendment and "Review round 1 fixes"; `lanes/lit.md` sections 4, 8, 14, 15; `lanes/inv.md` lessons; `lanes/park.md` sections 3-5 and 7 | `bt_window.py`, `bt_window_now.py`, `bt_amend.py`, `bt_review1.py`, `bt_tables.py`, `report_checks.py` | `research/cards/exit-rules.md` (amendments 1 and 2); `research/tries.md` idea `exit-window` |
| 6.1 Crash rules over years | `lanes/bt.md` Part B and amendment | `bt_rules.py`, `bt_amend.py`, `bt_sanity.py` | `research/tries.md` idea `exit-rules` |
| 7 Parking | `lanes/haven.md` (incl. the round 1 correction), `lanes/haven-table.md`, `lanes/park.md` sections 1-2 | `haven_crash_table.py` | Descriptive, not logged |
| 8 Re-entry | `lanes/reentry.md` Part 1, `lanes/reentry-describe.txt`, `lanes/reentry-rules.txt`; `lanes/inv.md` | `reentry_data.py`, `reentry_describe.py`, `reentry_rules.py` | `research/cards/reentry.md`; `research/tries.md` idea `reentry` |
| 9 Common ideas | `lanes/reentry.md` Part 2; `lanes/inv.md` section 1; `lanes/haven.md`; `lanes/park.md` | `inv_drawdowns.py`, `inv_burry_check.py` | Not logged |
| Dates, fees, levels | this report; `lanes/park.md` section 7 | `report_checks.py` | n/a |

Logged tests: 208 rows dated 2026-11-18 in `research/tries.md`, of which 176 come from bt (ideas
`exit-window` and `exit-rules`; 3 Oslo rows invalid, calendar bug) and 32 from reentry (idea
`reentry`), plus 18 post-hoc `robustness` rows from bt in review round 1 (`bt_review1.py`). The
gsy-1 rows are logged on its own branch. Result tables as CSV: `lanes/bt-data/`.

### 11.2 Sources

**Data**

- Yahoo Finance chart API, daily closes (`^GSPC`, `^IXIC`, `OSEBX.OL`, `OBX.OL`, `^VIX`, `^VIX3M`,
  `^SOX`, HYG, LQD, XLK, NVDA, BRK-A, BRK-B, GC=F, SHY, IEF, TLT, GLD, EXX6.DE, EUNH.DE, DBXP.DE,
  XEON.DE), fetched 2026-11-12/18.
- CBOE VIX history: https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv
- FRED: https://fred.stlouisfed.org/ (BAA10Y, DGS2, DGS10, DGS30, DEXSZUS, DEXJPUS, DEXUSEU,
  DEXNOUS, ECBDFR)
- Shiller data (`ie_data.xls`): https://shillerdata.com/
- Ken French data library (daily factors, T-bill, HiTec):
  https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- ECB 3-month Euribor: https://data-api.ecb.europa.eu/service/data/FM/M.U2.EUR.RT.MM.EURIBOR3MD_.HSTA?format=csvdata
- World Bank Pink Sheet (gold, monthly): https://thedocs.worldbank.org/en/doc/74e8be41ceb20fa0da750cda2f6b9e4e-0050012026/related/CMO-Historical-Data-Monthly.xlsx
- Norges Bank exchange rates: https://data.norges-bank.no/api/data/EXR/B.EUR.NOK.SP?format=csv&locale=en
- Ritter, IPO Statistics (2026-11-05 edition): https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf ;
  data page https://site.warrington.ufl.edu/ritter/ipo-data/

**Literature: bubbles, prediction, timing**

- Greenwood, Shleifer, You (2019), Bubbles for Fama, JFE 131(1): https://doi.org/10.1016/j.jfineco.2018.09.002 ; NBER w23191: https://www.nber.org/papers/w23191
- Goetzmann (2015), Bubble investing, NBER w21693: https://www.nber.org/papers/w21693
- Brunnermeier, Nagel (2004), Hedge funds and the technology bubble, JF 59(5): https://doi.org/10.1111/j.1540-6261.2004.00690.x
- Abreu, Brunnermeier (2003), Bubbles and crashes, Econometrica 71(1): https://doi.org/10.1111/1468-0262.00393
- Temin, Voth (2004), Riding the South Sea bubble, AER 94(5): https://doi.org/10.1257/0002828043052268
- Campbell, Shiller (1988), JF 43(3): https://doi.org/10.1111/j.1540-6261.1988.tb04598.x ; (1998), JPM 24(2): https://doi.org/10.3905/jpm.24.2.11
- Goyal, Welch (2008), RFS 21(4): https://doi.org/10.1093/rfs/hhm014
- Goyal, Welch, Zafirov (2024), RFS 37(11): https://doi.org/10.1093/rfs/hhae044
- Campbell, Thompson (2008), RFS 21(4): https://doi.org/10.1093/rfs/hhm055
- Cochrane (2011), Discount rates, JF 66(4): https://doi.org/10.1111/j.1540-6261.2011.01671.x
- Kritzman, Turkington (2025), The fallacy of concentration, SSRN 5436695: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5436695 ; summary https://quantpedia.com/the-fallacy-of-concentration-risk/
- Gilchrist, Zakrajšek (2012), AER 102(4): https://doi.org/10.1257/aer.102.4.1692 ; Fed note: https://www.federalreserve.gov/econresdata/notes/feds-notes/2016/recession-risk-and-the-excess-bond-premium-20160408.html
- López-Salido, Stein, Zakrajšek (2017), QJE 132(3): https://doi.org/10.1093/qje/qjx014
- Baker, Wurgler (2000), equity share: https://pages.stern.nyu.edu/~jwurgler/papers/equityshare.pdf ; (2006), JF 61(4): https://doi.org/10.1111/j.1540-6261.2006.00885.x ; (2007), JEP 21(2): https://doi.org/10.1257/jep.21.2.129
- Baker, Taliaferro, Wurgler: https://pages.stern.nyu.edu/%7Ejwurgler/papers/wurgler_baker_taliaferro.pdf
- Butler, Grullon, Weston (2005), JF: https://ideas.repec.org/a/bla/jfinan/v60y2005i2p963-986.html
- Huang, Jiang, Tu, Zhou (2015), RFS 28(3): https://doi.org/10.1093/rfs/hhu080
- Fisher, Statman (2000), FAJ 56(2): https://doi.org/10.2469/faj.v56.n2.2340
- Pan, Poteshman (2006), RFS 19(3): https://doi.org/10.1093/rfs/hhj024
- Faber (2007), JWM 9(4): https://doi.org/10.3905/jwm.2007.674809 ; SSRN 962461: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=962461
- Moskowitz, Ooi, Pedersen (2012), JFE 104(2): https://doi.org/10.1016/j.jfineco.2011.11.003
- Hurst, Ooi, Pedersen (2017), JPM 44(1): https://doi.org/10.3905/jpm.2017.44.1.015 ; AQR: https://www.aqr.com/Insights/Research/Journal-Article/A-Century-of-Evidence-on-Trend-Following-Investing
- Zakamulin (2014), JAM 15(4): https://doi.org/10.1057/jam.2014.25
- Moreira, Muir (2017), JF 72(4): https://doi.org/10.1111/jofi.12513
- Cederburg, O'Doherty, Wang, Yan (2020), JFE 138(1): https://doi.org/10.1016/j.jfineco.2020.04.015
- Johnson (2017), VIX term structure, JFQA 52(6): https://doi.org/10.1017/S0022109017000825
- Johansen, Ledoit, Sornette (2000), IJTAF 3(2): https://doi.org/10.1142/S0219024900000115 ; Bree, Joseph: https://arxiv.org/abs/1002.1010
- Phillips, Shi, Yu (2015), IER 56(4): https://doi.org/10.1111/iere.12132 ; Phillips, Wu, Yu (2011), IER 52(1): https://doi.org/10.1111/j.1468-2354.2010.00625.x
- Kaminski, Lo (2014), JFM 18: https://doi.org/10.1016/j.finmar.2013.07.001 ; WP: https://ideas.repec.org/p/hhs/sifrwp/0063.html
- Graham, Harvey (1996), JFE 42(3): https://doi.org/10.1016/0304-405X(96)00878-1 ; NBER w4890: https://www.nber.org/papers/w4890
- Dichev (2007), AER 97(1): https://doi.org/10.1257/aer.97.1.386
- Constantinides (1979), JFQA 14(2): https://doi.org/10.2307/2330513
- Vanguard (2023), Cost averaging: https://corporate.vanguard.com/content/dam/corp/research/pdf/cost_averaging_invest_now_or_temporarily_hold_your_cash.pdf ; Vanguard (2012), copy: https://militarymoneymanual.com/wp-content/uploads/2021/08/Dollar-Cost-Averaging-Just-Means-Taking-Risk-Later-Vanguard.pdf
- Bouman, Jacobsen (2002), AER 92(5): https://doi.org/10.1257/000282802762024683
- Ofek, Richardson (2003), DotCom mania, NBER w8630: https://www.nber.org/papers/w8630
- Our GSY replication (Ken French industries): `lanes/gsy-replication.md`, copied from branch
  `gsy-1`, commit 35d155f (`research/results/gsy-1-replication.md`; overlay results in
  `research/gsy-1.md` on that branch)

**Literature: IPOs**

- Ibbotson, Jaffe (1975), JF: https://doi.org/10.1111/j.1540-6261.1975.tb01019.x
- Lowry (2003), JFE: https://doi.org/10.1016/S0304-405X(02)00230-X
- Pastor, Veronesi (2005), JF: https://ideas.repec.org/a/bla/jfinan/v60y2005i4p1713-1757.html
- Loughran, Ritter (1995), JF: https://doi.org/10.1111/j.1540-6261.1995.tb05166.x

**Literature and official sources: havens and safety**

- Baur, Lucey (2010), Financial Review 45(2): https://econpapers.repec.org/RePEc:bla:finrev:v:45:y:2010:i:2:p:217-229 ; WP: https://www.tcd.ie/triss/assets/PDFs/iiis/iiisdp198.pdf
- Baur, McDermott (2010), JBF 34(8): https://econpapers.repec.org/RePEc:eee:jbfina:v:34:y:2010:i:8:p:1886-1898
- Ranaldo, Söderlind (2010), Review of Finance 14(3): https://econpapers.repec.org/RePEc:oup:revfin:v:14:y:2010:i:3:p:385-407
- FSB (2020), Holistic review of the March market turmoil: https://www.fsb.org/2020/11/holistic-review-of-the-march-market-turmoil/
- NY Fed Liberty Street (2022): https://libertystreeteconomics.newyorkfed.org/2022/09/how-can-safe-asset-markets-be-fragile/
- Brixton et al. (2023), A changing stock-bond correlation: https://www.aqr.com/insights/research/journal-article/a-changing-stock-bond-correlation
- Neville et al. (2021), Man Institute: https://www.man.com/maninstitute/best-strategies-for-inflationary-times
- Reserve Primary Fund: https://www.investmentnews.com/mutual-funds/huge-money-market-fund-breaks-the-buck/17433 ; SEC LR-21025: https://www.sec.gov/litigation/litreleases/2009/lr21025.htm ; Crane Data: https://www.cranedata.com/archives/all-articles/2488
- EU MMF Regulation 2017/1131: https://eur-lex.europa.eu/eli/reg/2017/1131/oj
- ECB Macroprudential Bulletin 12 (2021): https://www.ecb.europa.eu/pub/financial-stability/macroprudential-bulletin/html/ecb.mpbu202104_2~a205b46756.en.html
- Gold Reserve Act: https://www.federalreservehistory.org/essays/gold-reserve-act

**Investors**

- Berkshire letters: 2024 https://www.berkshirehathaway.com/letters/2024ltr.pdf ; 2008 https://www.berkshirehathaway.com/letters/2008ltr.pdf ; 1986 https://www.berkshirehathaway.com/letters/1986.html
- Buffett partnership 1969: https://gurufocus.com/news/6620/warren-buffett-partnership-letter-in-may-1969 ; https://novelinvestor.com/notes/buffett-partnership-letters-by-warren-buffett/
- Inc. on BRK 1998-2000: https://www.inc.com/phil-rosen/berkshire-hathaway-warren-buffett-warning-sign-stock-market/91436294
- Buffett op-ed 2008: https://www.nytimes.com/2008/10/17/opinion/17buffett.html ; https://domain-b.com/investments/world_markets/20081020_warren_buffett.html
- Fortune 2025-11-01 (Berkshire cash): https://fortune.com/2025/11/01/warren-buffett-stocks-net-selling-berkshire-hathaway-q3-earnings-investment-portfolio-cash/
- AP via NY1, 2026-02-28 (Abel letter): https://ny1.com/nyc/all-boroughs/ap-top-news/2026/02/28/warren-buffetts-successor-greg-abel-publishes-his-first-letter-to-berkshire-hathaway-shareholders ; Irish Times: https://www.irishtimes.com/business/2026/02/28/greg-abel-tells-berkshire-hathaway-investors-its-cash-pile-is-not-a-retreat-from-deal-making/
- Berkshire 2026 buying: https://investinglive.com/Education/berkshire-s-cash-pile-starts-moving-under-greg-abel-learn-the-lessons-behind-the-news/ ; https://247wallst.com/investing/2026/08/08/berkshire-hathaway-just-did-something-it-hasnt-done-in-more-than-3-years/ ; Kiplinger: https://www.kiplinger.com/investing/stocks/stocks-berkshire-hathaway-bought-sold-q3-2026 ; AP via NY1 2026-11-07: https://ny1.com/nyc/all-boroughs/ap-top-news/2026/11/07/berkshire-hathaway-buys-back-96-billion-of-its-own-stock-but-its-profits-declined
- TIKR on Berkshire's chair (not confirmed by a second source, section 10.1): https://www.tikr.com/blog/berkshire-stock-holds-near-505-as-howard-buffett-takes-the-chair-heres-what-changes
- GMO / Grantham: https://www.outlookbusiness.com/perspective/looking-at-bubbles-the-statistical-way-936 ; https://www.advisorperspectives.com/articles/2015/06/29/grantham-stocks-will-continue-upward-until-the-election ; https://www.institutionalinvestor.com/article/b1hjlb0qs4c807/GMO-Is-Feeling-Pain-Reminiscent-of-the-Late-1990s ; https://moneyweek.com/investments/jeremy-grantham-on-long-term-investing-in-a-short-term-market ; https://www.gmo.com/americas/research-library/3q-2019-gmo-quarterly-letter ; https://www.gmo.com/globalassets/articles/viewpoints/2021/waiting-for-the-last-dance_1-2021.pdf ; https://www.gmo.com/globalassets/articles/viewpoints/2022/gmo_let-the-wild-rumpus-begin_1-22.pdf ; https://www.gmo.com/americas/research-library/valuing-ai-extreme-bubble-new-golden-era-or-both/ ; https://www.thinkadvisor.com/amp/2026/01/20/jeremy-grantham-slim-to-none-chance-ai-bubble-wont-burst/ ; https://www.top1000funds.com/2012/04/gmo%E2%80%99s-grantham-bets-against-irrational-markets/
- Marks / Oaktree: https://www.oaktreecapital.com/insights/memos ; https://www.oaktreecapital.com/docs/default-source/memos/is-it-a-bubble.pdf ; https://www.oaktreecapital.com/insights/insight-commentary/education/commemorating-25-years-of-mastering-the-market-cycle ; https://www.institutionalinvestor.com/article/b150qfyrndkrzm/howard-marks-the-distressed-debt-king ; https://businessinsider.in/howard-marks-made-billions-piling-into-the-market-at-the-depths-of-the-financial-crisis-heres-why-hes-continuing-to-buy-now-and-what-it-would-take-for-him-to-stop/articleshow/66148612.cms
- Druckenmiller: https://quartr.com/insights/investment-strategy/stanley-druckenmiller-breaking-the-bank ; https://www.wsws.org/en/articles/2000/05/soro-m05.pdf ; https://moneyweek.com/441992/the-worlds-greatest-investors-stanley-druckenmiller ; https://fortune.com/2024/10/18/billionaire-investor-druckenmiller-sold-nvidia-regrets-huang-musk-ellison/ ; https://fool.com/investing/2026/05/24/why-billionaire-stanley-druckenmiller-dumped-nvidi/
- Klarman: https://www.distressed-debt-investing.com/2009/12/wisdom-from-seth-klarman-part-6.html?m=1 ; https://www.fool.com/investing/general/2010/11/11/klarman-finds-opportunities-scarce.aspx ; https://en.wikipedia.org/wiki/Seth_Klarman
- Templeton: https://m.investing.com/analysis/when-the-unicorns-become-horses-again--tech-bubble-repeats-200470464?ampMode=1 ; https://www.redwheel.com/at/de/professional/?p=1694
- Robertson: https://money.cnn.com/2000/03/30/mutualfunds/q_funds_tiger/ ; https://www.theglobeandmail.com/report-on-business/wizard-of-wall-street-hangs-up-his-hat/article25459132/ ; https://www.investmentnews.com/alternatives/hedge-fund-guru-julian-robertson-dies-at-90/225681 ; https://hedgefundalpha.com/investor-letters/archives-julian-robertson-closing-letter-investors/
- Burry: https://www.etf.com/sections/news/michael-burry-makes-new-bet-against-blackrocks-soxx ; https://www.fool.com/investing/2023/08/16/big-short-michael-burry-16-billion-against-stock ; https://marketrebellion.com/news/no-michael-burry-didnt-risk-93-of-his-portfolio-on-put-options ; https://fortune.com/2025/11/04/big-short-investor-michael-burry-nvidia-palantir-puts-alex-karp/ ; https://techstrong.ai/features/tech-investor-michael-burry-alleges-accounting-irregularities-at-hyperscalers-in-pursuit-of-ai-boom/ ; https://www.cp24.com/news/money/2025/11/13/investor-michael-burry-of-big-short-fame-deregisters-scion-asset-management/ ; https://www.hedgeweek.com/burry-still-active-in-markets-after-scion-de-registration/
- Hussman: https://finance.yahoo.com/quote/HSGFX/performance?p=HSGFX ; https://zacks.com/funds/mutual-fund/quote/HSGFX/performance ; https://www.investmentnews.com/mutual-funds/john-hussman/24069
- Dalio: https://www.institutionalinvestor.com/article/b1jsw5lw26ncfq/In-Disappointing-Year-Bridgewater-s-Flagship-Fund-Returns-0-5 ; https://fortune.com/2020/09/15/the-losses-continue-to-pile-up-for-hedge-fund-king-ray-dalio/ ; https://businessinsider.in/finance/news/ray-dalio-was-blindsided-by-the-coronavirus-market-rout-and-now-his-flagship-fund-is-down-20-this-year/amp_articleshow/74658093.cms
- Greenspan speech, 5 Dec 1996: https://www.federalreserve.gov/boarddocs/speeches/1996/19961205.htm
- Newsletter timers: https://scholars.duke.edu/publication/774086 ; https://www.cxoadvisory.com/investing-expertise/classic-papers-the-value-of-investment-newsletters/ ; https://blog.validea.com/?p=11804

**Market events 2026**

- AP via Boston.com, 5 Nov 2026 sell-off: https://www.boston.com/news/national-news/2026/11/05/a-brutal-sell-off-for-ai-stocks-sends-wall-street-reeling-and-the-sp-500-tumbles-4-4/
- Renaissance Capital IPO stats: https://www.renaissancecapital.com/IPO-Center/Stats?market=us ; 2021 review: https://www.renaissancecapital.com/IPO-Center/News/89606/Renaissance-Capitals-2021-US-IPO-Market-Review ; Fall 2026 preview: https://www.renaissancecapital.com/review/US_Fall_Preview_2026_Public.pdf
- SpaceX IPO: https://www.brecorder.com/news/amp/40425123 ; https://techrepublic.com/article/news-spacex-ipo-price-valuation/
- Cerebras IPO: https://dealroom.co/news/128936-cerebras-raises-5-55b-in-biggest-us-ipo-of-2026/
- Anthropic listing, Nasdaq Trader notice: https://nasdaqtrader.com/TraderNews.aspx?id=DTN2026-28 ; investingLive/WSJ: https://investinglive.com/stock-market-update/wsj-anthropic-targets-nasdaq-debut-next-week-under-ticker-ant-despite-tech-selloff/
- 1929 recovery with dividends (Hulbert): https://www.historynewsnetwork.org/article/79770
- Nikkei record 2024: https://www.bostonglobe.com/2024/02/22/business/japans-nikkei-stock-index-breaks-its-1989-record-surges-an-all-time-high/ ; https://www.bloomberg.com/news/articles/2024-02-22/japan-s-nikkei-hits-intraday-high-surging-past-1989-record

**Practical: rates, products, guarantees, selling and moving money**

- ECB rate: https://fred.stlouisfed.org/graph/?id=ECBDFR ; https://www.lovguiden.dk/en/det-offentlige/den-europaeiske-centralbank/2026-10-29-ecb-holder-renten-uaendret-paa-250-trods-inflation-paa-38 ; https://www.scotiabank.com/ca/en/about/economics/economics-publications/post.other-publications.international-economics.europe-.ecb--october-29-2026-.html ; Raisin NL: https://www.raisin.com/nl-nl/nieuws/spaarrente-verwachting-november-2026/
- Savings rates: Keuze.nl, read 2026-11-15 (exact page not recorded in the park note); fixed-term: https://dutchreview.com/financial/best-dutch-fixed-term-deposit-savings-accounts/
- Trade Republic: https://www.geld.nl/sparen/expert/nieuws/trade-republic-4-procent-actierente ; https://dutchreview.com/financial/trade-republic-savings-rate-new-customers/
- ETFs (justETF): XEON https://www.justetf.com/en/etf-profile.html?isin=LU0290358497 ; Amundi CSH https://www.justetf.com/en/etf-profile.html?isin=FR0010510800 ; IEGE https://www.justetf.com/en/etf-profile.html?isin=IE00B3FH7618 ; ERNE https://www.justetf.com/en/etf-profile.html?isin=IE00BCRY6557 ; IBGS https://www.justetf.com/en/etf-profile.html?isin=IE00B14X4Q57 ; iShares Physical Gold https://www.justetf.com/en/etf-profile.html?isin=IE00B4ND3602
- XEON mechanics: https://www.trackinsight.com/en/fund/XEON ; https://etf.dws.com/en-ch/knowledge/focus-topics/overnight-etfs-an-alternative-to-easy-access-savings-accounts/
- Xetra-Gold costs: https://www.xetra-gold.com/en/gold-news/gold-etcs-the-most-important-cost-models
- Berkshire B quote: https://www.foxbusiness.com/quote?stockTicker=BRK.B
- Dutch deposit guarantee: https://www.dnb.nl/en/reliable-financial-sector/dutch-deposit-guarantee/faq-dutch-deposit-guarantee/ ; ATB payout: https://www.dnb.nl/nieuws-voor-de-sector/nederlandse-depositogarantie-2024/dnb-publiceert-factsheet-over-verloop-dgs-uitkering-amsterdam-trade-bank/ ; DSB: https://www.nhnieuws.nl/nieuws/682/geen-garantie-speciale-depositos
- SNS Reaal 2013: https://www.allenovery.com/en-gb/global/news-and-insights/european-finance-litigation-review/northern-europe/expropriation-of-sns-reaal-first-application-of-the-dutch-intervention-act ; https://radar.avrotros.nl/artikel/staat-nationaliseert-sns-voor-37-miljard-11769 ; https://www.consumentenbond.nl/nieuws/2013/zorgen-nationalisatie-sns ; https://www.government.nl/latest/news/2023/04/21/ministry-of-finance-to-pay-compensation-to-holders-of-expropriated-sns-securities-and-assets ; https://www.accountant.nl/nieuws/2024/4/staat-betaalt-900-miljoen-aan-onteigende-sns-reaal-beleggers/
- Investor compensation: https://www.rijksoverheid.nl/vraag-en-antwoord/financiele-sector/wat-gebeurt-er-met-mijn-tegoeden-als-mijn-beleggingsonderneming-failliet-gaat ; https://www.dnb.nl/voor-de-sector/open-boek-toezicht-sectoren/banken/resolutie/beleggerscompensatiestelsel-bcs/
- Dutch state bonds: https://english.dsta.nl/subjects/purchasing-government-bonds
- DEGIRO fees: https://www.degiro.nl/tarieven ; core selection: https://www.debelegger.nl/post/degiro-schrapt-kernselectie-buiten-tradegate-dit-veranderd-er-voor-beleggers ; https://financer.nl/review/degiro-kernselectie/
- Fund dealing calendars 2026 (Oslo calendar): dealing calendars read from three fund companies (`lanes/park.md` section 7.1)
- NYSE holidays 2026-2028: https://ir.theice.com/press/news-details/2025/NYSE-Group-Announces-2026-2027-and-2028-Holiday-and-Early-Closings-Calendar/default.aspx
- ESMA T+1 (Oct 2027): https://esma.europa.eu/press-news/esma-news/one-year-go-t1-settlement-regulatory-framework-complete-now-lets-make-it
- Holiday calendars: Euronext https://live.euronext.com/resources/trading-hours-holidays ; Norges Bank settlement days https://www.norges-bank.no/tema/Norges-Banks-oppgjorssystem/Oppgjorsdager/ ; ECB TARGET https://www.ecb.europa.eu/ecb/contacts/working-hours/html/index.en.html ; Euronext Clearing https://www.euronext.com/sites/default/files/2025-11/2026_holidays_calendar_for_euronext_clearing_services_2.pdf
- The krone (NOK) in March 2020, as currency-risk evidence: Norges Bank staff memo https://www.norges-bank.no/link/d6c761672e1242db9ecac5658bd0b78d.aspx?ft=.pdf
