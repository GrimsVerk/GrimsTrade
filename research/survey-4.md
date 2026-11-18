# Survey 4: effects that survived after publication (2026-11-18)

Lane `survey-4` of the night lead (research only, fake money). Branch `survey-4` from `ann-1`.
Question: survey-2, survey-3 and ann-1 tested three published effects (FOMC cycle, cross-asset
trend, announcement premium); all three replicate inside their papers' years and die after.
This survey takes the other angle: which effects have a **documented record after their
publication or before their original sample** in large replication studies, and which of those
fit this book (`tsmom12` on SPY, QQQ, TLT, GLD, BTC, ETH; weekly decisions on daily bars; next-open
fills; long only; ETFs about 4 bps a round trip, coins about 60)?

How it was made: web searches; abstracts through journal pages, RePEc and secondary write-ups;
three papers read as PDF text (`pdftotext` of the downloaded file, read as data). Every source is
tagged with how far it was read: `[full text]`, `[pages read]`, `[abstract]`, `[secondary]`,
`[search summary]`. Every citation below was checked on the web on 2026-11-18 (journal, volume,
pages). Numbers marked `[search summary]` were not seen in the paper itself.

This note (sources, candidates, pick rule) was written and pushed **before any number of this
lane was computed**. What I already knew about the data is stated where it matters (the rough
history of US interest rates and dividend yields is common knowledge, not a result of this lane).

## Sources

### How much survives, in general

- **R1. McLean and Pontiff, "Does Academic Research Destroy Stock Return Predictability?",
  Journal of Finance 71(1), 2016, DOI 10.1111/jofi.12365.** `[pages read]` (abstract and p. 1
  of the published PDF) <https://www.gwern.net/doc/economics/2016-mclean.pdf>
  - 97 cross-sectional stock predictors. "Portfolio returns are 26% lower out-of-sample and
    58% lower post-publication"; 32% attributed to publication-informed trading. Declines are
    larger for predictors with larger in-sample returns.
  - Here: the haircut to expect. Survey-2's three picks lost far more than 58% (all of it).
- **R2. Hou, Xue and Zhang, "Replicating Anomalies", Review of Financial Studies 33(5), 2020,
  pp. 2019-2133.** `[abstract]` <https://ideas.repec.org/a/oup/rfinst/v33y2020i5p2019-2133..html>
  - 452 stock anomalies; with NYSE breakpoints and value weights, 65% fail |t| >= 1.96, 82% fail
    |t| >= 2.78. Trading-friction anomalies fail worst (96%).
- **R3. Jensen, Kelly and Pedersen, "Is There a Replication Crisis in Finance?", Journal of
  Finance 78(5), 2023, pp. 2465-2518, DOI 10.1111/jofi.13249.** `[abstract]` + `[secondary]`
  <https://www.nber.org/system/files/working_papers/w28432/w28432.pdf>
  - 153 factors, 93 countries, Bayesian: most factors replicate (82% in the published version
    `[secondary]`); in 10 of 13 clusters more than 75% replicate; **seasonality, leverage and
    size are the exceptions**. Out-of-sample returns are lower but positive.
  - Here: all of R1-R3 are about the cross-section of single stocks. This book holds six
    assets, so they set expectations (decay, which families hold) rather than give rules.
- **R4. Harvey, Liu and Zhu, "... and the Cross-Section of Expected Returns", Review of
  Financial Studies 29(1), 2016, pp. 5-68.** `[abstract]` + `[secondary]`
  <https://www.nber.org/papers/w20592>
  - A new factor should clear t > 3.0 (p < 0.0027), not 2.0. The lineage's family bar (p <
    0.10 / number of mechanisms listed) is in the same spirit and, at 61+, stricter.

### Asset-class factors over two centuries (the core of this survey)

- **R5. Baltussen, Swinkels and van Vliet, "Global Factor Premiums", Journal of Financial
  Economics 142(3), 2021, pp. 1128-1154, DOI 10.1016/j.jfineco.2021.06.030.** `[full text]`
  (working-paper PDF hosted by a German trade magazine, read as text; tables I-V and the robustness
  table) <https://www.institutional-investment.de/uploads/media/Robeco_Study_Global-Factor-Premiums.pdf>
  - 24 premiums: six factors (trend, cross-sectional momentum, value, carry, return
    seasonality, betting-against-beta) in four asset classes (equity indexes, 10-year government
    bonds, commodities, currencies). Replication sample 1981-2011; "new sample" 1800-1980 plus
    2012-2016. Monthly, long-short, gross.
  - Definitions: trend and momentum = 12-1 month excess return; value = dividend yield
    (equities), real yield (bonds), 5-year reversal (commodities), PPP (currencies); **carry =
    the implied yield of each instrument** (equities: implied dividend yield minus the risk-free
    rate; bonds: slope plus roll-down); **seasonality = the asset's return in the same calendar
    month over the prior 20 years**; trend is time-series (long when positive), all others are
    cross-sectional within the asset class.
  - New sample (1800-1980, 2012-2016), Sharpe (t): equities trend 0.75 (11.0), carry 0.68
    (9.9), seasonality 0.60 (8.8), momentum 0.37, value 0.27, BAB 0.34; bonds trend 0.49 (7.2),
    carry 0.44 (6.5), seasonality 0.73 (10.7), momentum 0.31, value 0.28, BAB -0.02.
  - Replication 1981-2011, Sharpe (t): equities carry 0.87 (4.8), trend 0.62, seasonality
    0.36 (2.0); bonds carry 0.71 (3.9), trend 0.53, seasonality -0.09 (-0.5).
  - Footnote 8: only five premiums pass both the strict Bayesian test on the replication
    sample and the pre-sample test: **trend in equities, bonds and commodities; momentum in
    equities; carry in equities and bonds.**
  - Robustness (their Table VII as I read it): seasonality drops to about zero when its signal
    is lagged one month (multi-asset -0.07); carry and trend survive every variation.
- **R6. Koijen, Moskowitz, Pedersen and Vrugt, "Carry", Journal of Financial Economics
  127(2), 2018, pp. 197-225, DOI 10.1016/j.jfineco.2017.11.002.** `[full text]` (accepted
  manuscript, CBS research portal, read as text)
  <https://research-api.cbs.dk/ws/files/57294842/lasse_heje_pedersen_et_al_carry_acceptedmanuscript.pdf>
  - Carry = the return if prices stay the same. Equities: expected dividend yield minus the
    risk-free rate (from futures). Bonds: about (10-year yield minus the short rate) plus the
    roll-down. Samples end September 2012 (equity futures from 1988, bonds from 1983).
  - **Section 3.7, "Carry timing" (time series, per asset):** weight = sign(carry - C) with C =
    0 or C = the average carry of the asset class up to that date (fully out of sample). Table
    6, Sharpe: global equities 0.41 (C = 0) / 0.75 (C = mean); 10-year global bonds 0.65 / 0.69;
    US Treasuries 0.60 / 0.31. The authors note that with C = 0 the timing strategy is close to
    a passive long or short position in classes where carry rarely changes sign.
- **R7. Hurst, Ooi and Pedersen, "A Century of Evidence on Trend-Following Investing",
  Journal of Portfolio Management 44(1), 2017, pp. 15-29.** `[abstract]` + `[secondary]`
  <https://fairmodel.econ.yale.edu/ec439/hurst.pdf>
  - 67 markets back to 1880; trend positive in every decade, best in extreme stock years.
- **R8. Moskowitz, Ooi and Pedersen, "Time Series Momentum", Journal of Financial Economics
  104(2), 2012, pp. 228-250.** `[abstract]` 58 futures, 1985-2009; 1-12 month persistence,
  partial reversal later. **R9. Huang, Li, Wang and Zhou, "Time Series Momentum: Is It There?",
  Journal of Financial Economics 135(3), 2020, pp. 774-794.** `[abstract]` Asset by asset the
  predictive regressions are weak; the strategy's profit is close to one built on the historical
  mean. Here: R7-R9 are why `tsmom12` is the baseline; nothing new to card.

### Seasonal effects with an out-of-sample record

- **R10. Heston and Sadka, "Seasonality in the Cross-Section of Stock Returns", Journal of
  Financial Economics 87(2), 2008, pp. 418-445.** `[abstract]` Same-calendar-month returns
  repeat for up to 20 annual lags (NYSE/AMEX, 1963-2002 `[secondary]`).
- **R11. Keloharju, Linnainmaa and Nyberg, "Return Seasonalities", Journal of Finance 71(4),
  2016, pp. 1557-1590, DOI 10.1111/jofi.12398.** `[abstract]` Same-calendar-month strategy
  earns about 13% a year in stocks 1963-2011; similar seasonalities in anomalies, commodities and
  country indexes; the authors read them as common factors, not a separate anomaly. Their 2018
  follow-up (cited in R5) finds seasonal reversals that sum to zero over the year.
- **R12. Bouman and Jacobsen, "The Halloween Indicator, 'Sell in May and Go Away': Another
  Puzzle", American Economic Review 92(5), 2002, pp. 1618-1635.** `[secondary]` 37 markets,
  1970 to 1998 (sources say January or May 1970 to August or October 1998): November-April
  returns above May-October in 36 of 37.
- **R13. Andrade, Chhaochharia and Fuerst, "'Sell in May and Go Away' Just Won't Go Away",
  Financial Analysts Journal 69(4), 2013, pp. 94-105.** `[abstract]` + `[secondary]` The same
  37 countries on new data, November 1998 to April 2012: about 10 points a year higher in
  November-April than May-October, about as large as in the original sample; also in size,
  value, carry, volatility and credit premiums. **No effect in bond indexes** (32 countries),
  especially in the new data.
- **R14. Zhang and Jacobsen, "The Halloween Indicator, 'Sell in May and Go Away': Everywhere
  and All the Time", Journal of International Money and Finance 110, 2021.** `[abstract]` +
  `[secondary]` All index data worldwide (62,962 monthly observations; 108 or 114 markets,
  sources differ), UK back to the 1690s; the strategy beats the market in more than 80% of
  5-year windows `[secondary]`. End of sample not confirmed (2017 or so, unverified).

### Value and predictability

- **R15. Welch and Goyal, "A Comprehensive Look at the Empirical Performance of Equity
  Premium Prediction", Review of Financial Studies 21(4), 2008, pp. 1455-1508.** `[abstract]`
  No predictor, the dividend yield included, beat the historical mean out of sample for a
  real-time investor. Here: time-series value timing of SPY (high dividend yield = cheap) has a
  documented out-of-sample failure. R5's value premiums are cross-sectional and the weakest of
  its five surviving families.

### Crypto

- Liu and Tsyvinski, "Risks and Returns of Cryptocurrency", Review of Financial Studies 34(6),
  2021 `[search summary, unverified]`: 1-4 week time-series momentum in Bitcoin. Not a
  replication study; a weekly in-and-out at 60 bps costs about 31% a year (first survey);
  `breadth-1`'s weekly `mom_7` on coins was negative. Not a candidate.

## Candidates

Only mechanisms that the `wide-*` lineage (61 listed) has not tested. Each mapped to this book.

| # | Candidate | Sources | Survival record | Map to this book | Data (free, cached) |
|---:|---|---|---|---|---|
| A | `ts-carry`: keep a `tsmom12` slot of SPY, QQQ, TLT only while its carry is positive | R5, R6 | Passes R5's strict and pre-sample tests in equities and bonds (one of five such premiums); R6's own sample ends 2012-09, so 2012-10 .. 2025 is post-sample | Equity carry = the ETF's trailing 12-month dividend yield (from its own distributions) minus the 13-week T-bill yield; bond carry = 10-year Treasury yield minus the bill (R6's slope; roll-down left out). GLD, coins: no carry measurable on spot data, untouched | Yahoo dividend-adjusted vs raw closes, `^IRX`, FRED `DGS10` |
| B | `halloween`: stock slots only from November to April | R12, R13, R14 | The best-documented post-publication calendar record: new data 1998-2012 as large as the original (R13); 300 years of UK data (R14). Not in stocks' cross-section studies | SPY, QQQ trend slots held only in weeks starting November-April; TLT, GLD, coins untouched (R13: none in bonds) | prices only |
| C | `seasonal-20y`: keep a slot only in calendar months whose 20-year same-month average is not below the asset's 20-year average month | R5, R10, R11 | Strong in R5's new sample (equities 0.60, bonds 0.73) but fails its replication sample (equities Bayesian p 0.60, bonds -0.09) and dies with a one-month lag; R3 lists seasonality among the clusters that do not replicate | Needs 20 years of monthly history per asset: SPY via the S&P 500 index, QQQ via the Nasdaq Composite, TLT via the 10-year yield; GLD and coins have too little. Only cross-sectional forms are documented; the time-series form is my construction | `^GSPC`, `^IXIC`, `DGS10` |
| D | `ts-value`: keep the SPY/QQQ slot only while the dividend yield is above its own history's median (cheap); TLT while the real yield is | R5, R15 | R5: value is significant in the new sample but not in the replication; R15: dividend-yield timing fails out of sample | Same inputs as A plus CPI vintages | as A |

Collapsed into tested ideas (not candidates): cross-sectional momentum among the six (R5's
equity momentum) into `patch-leaving`; BAB into `inverse-vol`; trend variants from R7-R9 into
`ensemble-tsmom` and `trend-vol`; crypto weekly momentum into `breadth-1`; month-end and
pre-FOMC calendars into `month-end-liquidity` and `announcement-premium`.

**Family.** A-D are four mechanisms new to the lineage (`halloween` was parked by the first
survey, before the lineage started, and is counted now). Family: 61 + 4 = **65**; every test of
this lane is read at **p < 0.10 / 65 = 0.00154**.

## Pick rule (fixed before any number)

Score each candidate; the top two by score are carded and tested on train, in that order; ties
go to the larger documented time-series or long-only Sharpe.

1. Two points if a source finds it in an asset class this book holds both in a replication
   sample and in data outside it (R5 footnote 8, or R12 + R13 for Halloween); one point if only
   outside the original sample.
2. One point if a source documents a time-series (single-asset, long-or-flat-able) form.
3. One point if at least eight years of our train lie after the source's sample.
4. One point if all data are free and already cached.
5. Minus one if the documented record contains a published out-of-sample failure of the form
   we would trade (R15 for D; R3 and R5's lag test for C); else zero.

| Candidate | 1 | 2 | 3 | 4 | 5 | Score |
|---|---:|---:|---:|---:|---:|---:|
| A `ts-carry` | 2 | 1 (R6 Table 6) | 1 (2012-10 .. 2025) | 1 | 0 | **5** |
| B `halloween` | 2 (R12 1970-98, R13 1998-2012) | 1 (the rule is time-series) | 1 (2012-05 .. 2025) | 1 | 0 | **5** |
| C `seasonal-20y` | 1 | 0 | 1 | 1 | -1 | 2 |
| D `ts-value` | 1 | 0 | 1 | 1 | -1 | 2 |

A and B tie at 5; R6 documents a time-series Sharpe (0.41-0.75 equities, 0.60-0.69 bonds),
R13 a half-year spread but no Sharpe in what I could read: **A first, then B.** C and D are the
next two for a future lane if both fail.

## What I expect (before any number)

- `ts-carry`: US equity carry (dividend yield about 1-2% minus bills) was negative for most of
  1994-2001 and 2005-2008 and again from 2022, positive 2009-2021 when bills paid nothing. A gate
  on it takes SPY and QQQ out of the late-1990s and 2023-2025 rallies. Bond carry was negative
  only around 2000, 2006-07, 2019 and 2022-2024 (inverted curve). My guess: the primary loses to
  `tsmom12` by 0.05-0.15 Sharpe; the TLT leg alone helps a little (out in 2022). Prior that a
  variant passes: 2%.
- `halloween`: `tsmom12` already leaves stocks in 2001-02 and 2008; what remains is cutting
  every summer. Guess: within +-0.05 of the twin, p far from the family bar; the SPY
  winter-minus-summer spread positive but t < 2 after 1998. Prior: 1%.
