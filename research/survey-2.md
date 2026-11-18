# Survey 2: 2023-2026 research for this book (2026-11-18)

Lane `survey-2` of the night lead. Question: what has research from 2023 to 2026 (and older
papers whose out-of-sample record was only written up since) found that this book could use,
and that the repo has not already listed, carded or killed? The book: `tsmom12` on SPY, QQQ,
TLT, GLD, BTC, ETH; weekly decisions on daily bars; fills at the next open; ETFs about 4 bps a
round trip, coins about 60.

How it was made: web searches (SSRN pages refuse automated reading, as in the first survey;
abstracts were read through journal pages, RePEc, search summaries and secondary write-ups), one
paper read in full for its first seven pages. Every entry is tagged with how far it was read:
`[full text]`, `[pages read]`, `[abstract]`, `[secondary]` (a write-up by someone else),
`[search summary, unverified]` (only a search engine's summary of the page: numbers there are
not checked). Numbers are quoted as the source gives them. "Overlap" says what the repo already
tested or listed (`research/ideas.md`, `research/wide-1.md`, cards).

Checked against: `ideas.md`, `wide-1.md` (54 mechanisms incl. W1-W8), the 40 cards, and the
other night lanes' branches (no branch mentions the FOMC cycle, cross-asset momentum or the
announcement premium; `month-end-bonds` and `volume-1` have their own lanes).

## Sources

### Monetary-policy calendar (new family for this repo)

- **S1. Cieslak, Morse, Vissing-Jorgensen, "Stock Returns over the FOMC Cycle", Journal of
  Finance 74(5), 2019.** `[pages read]` (2015 working-paper draft, pp. 1-7)
  <http://www.stern.nyu.edu/sites/default/files/assets/documents/cycle_paper_cieslak_morse_vissingjorgensen.pdf>
  - Claim: since 1994 the US equity premium was earned entirely in "even weeks" of FOMC cycle
    time. Day 0 = scheduled announcement day (second day of a two-day meeting); days are
    weekdays (weekends omitted, holidays counted as zero return). Week 0 = days -1..3, week 2 =
    9..13, week 4 = 19..23, week 6 = 29..33; odd weeks -6..-2, 4..8, 14..18, 24..28.
  - Size (1994-2013, about 160 meetings): average 5-day excess return 0.57% in week 0, 0.30%
    week 2, 0.42% week 4, 0.61% week 6; about 0, -0.17%, -0.17%, -0.12% in weeks -1, 1, 3, 5.
    Daily regression: +13.6 bps a day in week 0 and +10 bps a day in weeks 2/4/6 over odd weeks,
    both significant at 1%. Pattern in each of 1994-2000, 2001-07, 2008-13; also 1982-93 (week 1
    higher there); MSCI world ex-US and emerging markets (EM +18 bps a day in weeks 2/4/6,
    t 4.75). Not in 10-year Treasuries.
  - Out of sample: the published version reports the pattern held in 2014-2016, after the
    first draft `[search summary, unverified]`. About half of the even-week return is mean
    reversion after market declines ("Fed put") `[search summary, unverified]`.
  - Follow-ups: Yun and Kwon, Finance Research Letters 2023, 1994-2020: low-risk anomaly
    returns drop in even weeks `[search summary, unverified]`
    <https://strathprints.strath.ac.uk/88240/>; Ortu, Reggiani, Severino, "Persistence-based
    capital allocation along the FOMC cycle", Quarterly Journal of Finance 15(1), 2025 (CIRANO
    2024s-02): a strategy on the 2- and 6-week cycles "largely outperforms" the even-week one
    `[abstract]` <https://cirano.qc.ca/en/summaries/2024s-02>. No independent test after 2016
    found.
  - Here: implementable. The FOMC calendar is published about a year ahead (federalreserve.gov,
    free; downloaded). A gate on the SPY/QQQ slots, toggled about weekly, at 4 bps.
  - Overlap: `pre-fomc-drift` (dead, literature) is the first day of week 0 only; `opex-pin`
    (idle cash into stocks in one calendar week a month) failed. Not in any list.
- **S2. Ai, Bansal, Guo, "Macroeconomic Announcement Premium", NBER WP 31923, 2023.**
  `[abstract]` <https://www.nber.org/papers/w31923>
  - A survey. From 2020-01 to 2023-08 the average announcement premium was 16.33 bps per
    announcement, against 10.68 over the full sample `[search summary, unverified]`.
  - Against it: "Is There a Macro-Announcement Premium?", Management Science, 2025, DOI
    10.1287/mnsc.2024.06960 `[abstract]`
    <https://pubsonline.informs.org/doi/10.1287/mnsc.2024.06960>: volatility barely falls after
    announcements; the average announcement return is mostly monetary-policy surprises and
    small-sample luck; the premium is estimated to be small. A blog summary says it is not
    clearly present on employment and inflation days `[secondary]`.
  - Here: FOMC days fit next-open fills (2 pm announcement); CPI and payrolls come at 8:30, so
    the slot must be bought at the open of the day before. Needs 30 years of BLS release dates.
  - Overlap: S1's week 0; `pre-fomc-drift`.
- **S3. Pan and Peng, "The Pre-FOMC Drift and the Secular Decline in Long-Term Interest
  Rates", AFA 2025 draft, AEA 2026.** `[search summary, unverified]`
  <https://en.saif.sjtu.edu.cn/junpan/FOMC_new.pdf>
  - Long Treasuries rise the day before FOMC announcements: 10-year yield -0.68 bps on day -1
    (significant), from the Tokyo open of day -2 to the London close of day -1. Lucca and Moench
    had found no bond drift.
  - With Hillenbrand, "The Fed and the Secular Decline in Interest Rates", Review of Financial
    Studies 2025 `[abstract]` <https://papers.ssrn.com/abstract=3550593>: the fall in yields since
    1989 happened almost entirely in three-day windows around FOMC meetings; yields fall when
    the Fed cuts or lowers its long-run dot.
  - Here: idle cash into TLT around meetings; same dates as S1. Size: 0.68 bps of 10-year yield
    is about 12 bps on TLT a meeting. Hillenbrand's half is a cutting-cycle story: in a hiking
    cycle the same windows should go the other way.
  - Overlap: three Treasury-calendar cards failed (`auction-concession`, `tax-drain`,
    `coupon-dose`).
- **S4. Walker, Lou, Pinter, Üslü, "Why do government bond yields drift when news is on its
  way?", Bank Underground, 2025-02-13** (BoE working paper 2022). `[full text]` (the blog)
  <https://bankunderground.co.uk/2025/02/13/why-do-government-bond-yields-drift-when-news-is-on-its-way/>
  - UK gilts since 1997: daily yield changes in the two days before scheduled news (MPC, CPI,
    labour data) are 0.5 bps higher than outside (1.1 bps when gilt issuance came first),
    adding up to +2 points of yield; dealers sell new bonds before news. US yields rise before
    FOMC meetings when Treasury issuance came first (no bps given).
  - Overlap: `auction-concession` (faint lead on TLT, 2020-25). Opposite sign to S3 for US
    windows after issuance. Low.

### Trend and cross-asset timing

- **S5. Pitkäjärvi, Suominen, Vaittinen, "Cross-asset signals and time series momentum",
  Journal of Financial Economics 136(1), 2020.** `[secondary]`
  <https://www.cxoadvisory.com/equity-premium/cross-asset-class-intrinsic-momentum>
  <https://research.vu.nl/en/publications/cross-asset-signals-and-time-series-momentum/>
  - 20 countries, 1980-2015, monthly. Stocks: long when the past 12-month stock and bond
    returns are both positive. Bonds: long when the bond return is positive and the stock
    return negative. Sharpe 45% above plain TSMOM (abstract). CXO: gross, indexes, lags and
    tests on the same data, a bond bull market; gains modest in the US, UK, Canada, none in
    Japan.
  - Out of sample: none found; 2016-2025 is after the sample.
  - Here: no new data. SPY/QQQ slots held only while TLT's 12-month return is also positive.
    Weakness visible without a test: 2023-24, stocks rose while TLT's 12-month return was
    negative.
  - Overlap: macro gates on risk assets ("leaving early": `credit-spread`, `yield-curve`),
    `trend-to-safe`, `hedge-regime`. The ML features had no bond-trend input for stocks.
- **S6. Goulding, Harvey, Mazzoleni, "Momentum turning points", Journal of Financial Economics
  149(3), 2023.** `[secondary]` <https://www.cxoadvisory.com/momentum-investing/handling-reversals-in-price-trend-direction/>
  <https://econpapers.repec.org/RePEc:eee:jfinec:v:149:y:2023:i:3:p:378-406>
  - Slow (12-month) and fast (1-2 month) TSMOM define bull, correction, bear, rebound; the
    blend weight per state is learned. US stocks 1969-2018: gross Sharpe 0.52 against 0.51 for
    the static blend. Not better in Japan.
  - Overlap: `ensemble-tsmom` (+0.05, p 0.21), `trend-age`. Low.
- **S7. Moskowitz, Sabbatucci, Tamoni, Uhl, "Nonlinear Time Series Momentum", SSRN 5933974,
  2025-12.** `[search summary, unverified]` (SSRN 403) <https://papers.ssrn.com/abstract=5933974>
  - Machine learning on past returns finds nonlinear patterns; out-of-sample gains over TSMOM
    claimed as significant.
  - Overlap: run 2's seven ML cards (incl. pooled over 33 markets): AUC 0.50. Low fit.
- **S8. Benhamou et al., "Re-evaluating Short- and Long-Term Trend Factors in CTA
  Replication", arXiv 2507.15876, 2025.** `[abstract]` <https://arxiv.org/abs/2507.15876>
  - Bayesian decomposition of CTA returns into short trend, long trend and beta; a search
    summary says a short-term trend sleeve beat multi-month breakouts 2010-2025 after costs
    `[search summary, unverified]`. Futures, levered. Overlap: fast trend loses here after costs
    (`fracdiff-momentum`, `ensemble-tsmom`). Low.
- **S9. Zarattini and Antonacci, "A Century of Profitable Industry Trends", 2024, and the
  critique "Refining and Robust Backtesting of A Century of Profitable Industry Trends", arXiv
  2412.14361.** `[abstract]` <https://arxiv.org/html/2412.14361v1>
  - Long-only trend on 48 US industries; the critique finds no robust validation. Industries,
    not this book.

### Crypto

- **S10. Han, Kang, Ryu, "Time-Series and Cross-Sectional Momentum in the Cryptocurrency
  Market: A Comprehensive Analysis under Realistic Assumptions".** `[search summary,
  unverified]` (venue and year not checked)
  - With costs and daily price swings (liquidations) many momentum books die; TSMOM evidence
    strong, cross-sectional weak. Supports the coin slots as they are; nothing new.
- **S11. Arain and Snudden, 2025: real-time daily crypto forecasts, 2021-10 to 2024-02.**
  `[search summary, unverified]` Most predictors that are statistically significant earn no
  trading profit. Agrees with info-1 (IC ~0).
- **S12. Yae and Tian, working paper 2021: Bitcoin's stochastic correlation with stocks.**
  `[search summary, unverified]` <https://acfr.aut.ac.nz/__data/assets/pdf_file/0009/576990/George-Tian-NZ_2021.pdf>
  Daily out-of-sample R-squared up to 2.33%; "well-known in-sample predictors fail out of
  sample". Daily horizon cannot pay 60 bps. Low.
- **S13. Spot bitcoin ETF flows: Mazur and Polyzos, Journal of Alternative Investments 2025;
  DWF Labs (industry) 2026.** `[search summary, unverified]`
  <https://zuscholars.zu.ac.ae/works/7267>. Flows track price levels (R-squared 0.95); DWF:
  flows follow the last five days (correlation 0.54), not the next five (0.03). Two years of
  data. Not a signal.
- **S14. Stablecoin supply: arXiv 2603.23480 (2026), Artemis (industry).** `[search summary,
  unverified]` <https://arxiv.org/html/2603.23480v1>. Volatility and volume, or cross-section of
  layer-one coins; no tested Bitcoin-return result. Overlap: `stablecoin-resource` (parked).

### Regimes, flows, overlays

- **S15. Shu, Yu, Mulvey, statistical jump models, arXiv 2402.05272 (2024) and 2406.09578.**
  Already in the first survey; `hmm-regime` lost to the 200-day average. No new OOS record
  found.
- **S16. Harvey, Mazzoleni, Melone, "The Unintended Consequences of Rebalancing", NBER WP
  33554, 2025.** `[secondary]` <https://www.nber.org/papers/w33554>. Month-end and quarter-end
  pension rebalancing is front-run; cost about 8 bps a year ($16 bn). Overlap:
  `rebalance-pressure` (tested: book -0.005; raw spread right sign). Literature now supports
  the mechanism; the trade still does not fit a long-only trend book.
- **S17. Hartley and Schwarz, "Predictable End-of-Month Treasury Returns", Wharton working
  paper 2019; NY Fed Liberty Street, 2024-09, on month-end Treasury liquidity.** `[search
  summary, unverified]` <https://rodneywhitecenter.wharton.upenn.edu/wp-content/uploads/2019/12/17-19.Schwarz.pdf>.
  Coupon Treasuries earn their excess return in the last days of the month, tied to index
  rebalancing. This is the paper wide-1 remembered for `month-end-bonds`: the pattern was in
  print before our post hoc look. That idea has its own lane (`month-end-bonds` branch).
- **S18. Gupta et al., Forecasting 2024: climate risk predicts real gold returns, annual
  1258-2023.** `[search summary, unverified]` Annual; nothing for weekly decisions.
- **S19. "AdaptiveTrend", arXiv 2602.11708 (2026): crypto trend on 150+ perpetual pairs, OOS
  2022-2024.** `[search summary, unverified]` Needs perps and shorts (`short-1`, `carry-2`).

## Candidates and ranking (written 2026-11-18, before any number of this lane)

Only mechanisms the repo has not listed. Prior = my guess that a card on it passes the
protocol's train bar here, from three things: the out-of-sample record (independent, post
publication), the fit to this book (weekly, long-only, next-open fills, costs), and free data.

| Rank | Candidate | Source | OOS record | Fit here | Data | Prior |
|---:|---|---|---|---|---|---:|
| 1 | `fomc-cycle`: hold the SPY/QQQ trend slots only in even FOMC-cycle weeks | S1 | Three sub-periods, 1982-93, other countries, authors' 2014-16 holdout, follow-ups to 2020; nothing independent after 2016 | High: a weekly calendar known a year ahead, stock ETFs at 4 bps, claimed size (10 bps a day) far above costs | FOMC dates, free (downloaded) | 5% |
| 2 | `xtsmom`: SPY/QQQ slots only while TLT's 12-month return is also positive | S5 | In sample only; modest in the US | High: no new data | none | 3% |
| 3 | `fomc-bond-drift`: idle cash into TLT around FOMC days | S3 | None independent; half of it is the 1989-2020 fall in yields | Medium: ~12 bps a meeting, eight a year | FOMC dates | 2% |
| 4 | `announcement-premium`: idle cash into stocks on FOMC, CPI, payroll days | S2 | Disputed (bigger 2020-23 vs "small", MS 2025) | Medium: 8:30 releases need a day-early fill | BLS dates, work | 2% |
| 5 | `turning-points`: state-dependent slow/fast blend | S6 | 0.52 vs 0.51, gross | Medium | none | 1% |
| 6 | `nonlinear-tsmom`: ML on past returns | S7 | Claimed, unverified | Low: ML failed seven times here | none | 1% |
| 7 | `crypto-corr`: BTC timed by its correlation with stocks | S12 | Daily R-squared 2% | Low: daily horizon vs 60 bps | none | <1% |

Not candidates (collapse into tested or listed ideas): S4 into `auction-concession`; S8 into
the fast-trend failures; S10, S11 confirm nulls; S13 too short; S14 into `stablecoin-resource`;
S15 into `hmm-regime`; S16 into `rebalance-pressure`; S17 into `month-end-bonds`; S9, S18,
S19 do not fit the book.

**Pick: `fomc-cycle`.** It has the best out-of-sample record of the new ones and the cleanest
fit (the cycle is weekly and the calendar is fixed a year ahead). It is also the one whose
claimed effect is large enough that our 32 years can see it, and our train holds nine years
(2017-2025) after the published sample (1994-2016): a post-publication test of a published
rule, which is what the first survey said this lab should prefer. What speaks against it: the
lab's calendar overlays are 0 for 5, published effects decay (McLean-Pontiff), and half of the
effect is said to be bounces after declines (dip buying: real, small here). My guess before any
number: the even-minus-odd spread is positive since 2017 but well under the paper's 10 bps a
day, and the gate does not beat `tsmom12` at the family bar.

**How the bar is counted.** This lane continues the `wide-*` lineage, which reads each new pick
against every mechanism listed so far (46, then 49, then 54). This list adds 7 candidates, so
the family is 54 + 7 = 61 and the pick is read at p < 0.10 / 61 = 0.00164. That is the bar of
the lineage; counting every card the lab has run since 2026-11-12 (well over 100 configurations
in `tries.md`) would be stricter still, and is noted next to the result. Because 1994-2016 is
the paper's own sample, the card adds two bars on 2017-2025 alone.
