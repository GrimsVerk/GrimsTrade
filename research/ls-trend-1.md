# ls-trend-1: is the missing crisis alpha the missing short side and the narrow universe?

Lane `ls-trend-1` of the night run, 2026-11-18. Branch `ls-trend-1` from `survey-5` (draft PR
into `survey-5`). Research harness only: the live runner and the paper broker are not changed.
Fake money only.

Why: survey-5 (`survey-5.md`, `results/live-check.md`) found that `tsmom12` is not a trend fund.
Its monthly returns correlate 0.17 with nine live trend funds (TC) and 0.40 with SPY; in the
live window its Sharpe above bills equals holding the same assets (1.11 vs 1.11). In the crash
years live trend funds gained (+7% in 2008, +4% in 2020-02..03, +18% in 2022) while `tsmom12`
lost (-2%, -14%, -13%). `tsmom12` differs from the funds in two ways at once: it is long-only
(in or out), and it trades six assets (four without coins) where the funds trade 50-100+
futures in four asset classes. This lane asks which of the two matters.

Tags as in survey-4/5: `[pages read]` = text of the paper read here; `[abstract]` = abstract or
publisher page only; `[secondary]` = a write-up or search summary; `[not checked]`.

## Step 1: literature (what the sources say about where crash-year gains come from)

### Sources, with what was checked

- **L1. Moskowitz, Ooi, Pedersen, "Time Series Momentum", Journal of Financial Economics
  104(2), 2012, pp. 228-250, doi 10.1016/j.jfineco.2011.11.003.** `[pages read]` (text layer of
  the journal PDF, cached at `<cache_root>/downloads/ls-trend-1/papers/mop2012.*`). 58 futures
  and forwards (24 commodities, 12 cross-currency pairs from nine currencies, nine equity
  indexes, 13 government bonds), 1985-2009. Each position long or short by the sign of the
  past 12-month excess return, sized to 40% ex ante volatility (`40% / sigma_{t-1}`, sigma an
  exponentially weighted daily variance with centre of mass 60 days, annualised with 261),
  equal weight across the instruments alive (eq. 5 and the portfolio formula in Section 4.1;
  about 12% portfolio volatility). On 2008 (Section 4.3): profits "are large in October,
  November, and December of 2008 ... when commodity and equity prices dropped sharply, bond
  prices rose, and currency rates moved dramatically"; third-quarter losses had "caused the
  TSMOM strategy to be short in many contracts, setting up large profits" in the fourth
  quarter; losses again when the crisis ended (March-May 2009). The "smile": returns largest
  in the biggest up and down S&P 500 quarters; positive coefficient on the squared market
  return (Table 3 Panel C). TSMOM beats a passive long position at the same volatility
  (Fig. 3), and adds return over passive long for most instruments. **No numeric long/short
  split of the 2008 gain is given.**
- **L2. Hurst, Ooi, Pedersen, "A Century of Evidence on Trend-Following Investing", Journal of
  Portfolio Management 44(1), Fall 2017, pp. 15-29.** `[pages read]` (text layer; exhibits are
  images, not read; cached by survey-5). 67 markets, 1880-2016, 1/3/12-month signals, "always
  holds either a long or short position in every market", 10% ex ante volatility, costs and
  2/20 fees subtracted. Positive in 8 of the 10 largest 60/40 drawdowns. Why: bear markets
  have mostly unfolded over months (average 10 worst 60/40 drawdowns about 15 months),
  "giving trend followers an opportunity to position themselves short after the initial market
  decline and profit from continued market declines"; fast crashes (1987) are not caught.
  **The mechanism named is the short side; no numeric split.**
- **L3. Hurst, Ooi, Pedersen, "Demystifying Managed Futures", Journal of Investment Management
  11(3), 2013, pp. 42-58 (pages `[not checked]`).** `[pages read]` (authors' pre-print). TSMOM on
  58 markets explains CTA and managed-futures index returns and drives the largest managers'
  alphas to about zero. Same mechanism in words: in prolonged bear markets "time series
  momentum takes short positions as markets begin to decline and thus profits as markets
  fall"; the strategy "always holds a long or a short position".
- **L4. Baltas and Kosowski, "Momentum Strategies in Futures Markets and Trend-Following
  Funds"**, working paper (first version 2011-12, EFMA 2012 Barcelona; EDHEC publication July
  2013; no journal version found). `[abstract]` (the EFMA PDF is behind a bot check). TSMOM
  benchmarks at several frequencies have high explanatory power for CTA index returns; no
  capacity constraint found. Their companion paper (Baltas and Kosowski, "Demystifying
  Time-Series Momentum Strategies: Volatility Estimators, Trading Rules and Pairwise
  Correlations", SSRN 2140091) is on construction choices `[abstract]`. **Neither, as far as
  read, splits crash-year returns by leg.**
- **L5. Hamill, Rattray, Van Hemert, "Trend Following: Equity and Bond Crisis Alpha", Man
  AHL / Oxford-Man working paper, August 2016 (SSRN 2831926; a chapter in Harvey, Rattray, Van
  Hemert, *Strategic Risk Management*, Wiley 2021).** `[secondary]` (Man Institute summary page;
  the paper itself not read). Bonds, commodities, currencies and equity indexes, 1960-2015.
  Performance best in the worst equity **and** the worst bond environments (an "equity smile"
  and a stronger "bond smile"); trend worked before 1985 (bond bear market) as well as after.
  **Restricting the equity and bond positions to be non-positive (no long equities or bonds)
  enhanced crisis performance**, at the cost of lower average returns and worse results in the
  other asset's sell-off. That is the closest the literature comes to "the crisis gain is in
  the short side" for equities and bonds, and it says the short legs help in crises and cost
  in normal times.
- **L6. NBIM Discussion Note 1-2014, "Momentum in Futures Markets".** `[pages read]` (text
  layer; Chart 5 is an image). 47 futures from 1978. Over the full sample, "most of the
  positive portfolio performance is due to the long signals, while the value-added from the
  short signals is only apparent in currencies and commodities" (Section 3.5). Not by crash
  year.
- **L7. Kim, Tse, Wald, "Time Series Momentum and Volatility Scaling", Journal of Financial
  Markets 30, 2016, pp. 103-124.** `[abstract]` and `[secondary]`. Without volatility scaling,
  TSMOM and buy-and-hold have similar returns and alphas; the paper's edge comes mostly from
  the scaling. (Relevant here because `tsmom12` is unscaled in/out.)
- **L8. Goyal and Jegadeesh, "Cross-Sectional and Time-Series Tests of Return Predictability:
  What Is the Difference?", Review of Financial Studies 31(5), 2018, pp. 1784-1824.**
  `[abstract]`. Time-series strategies carry a time-varying **net long** position; for stocks
  most of their lead over cross-sectional strategies is that net long investment.
- **L9. Huang, Li, Wang, Zhou, "Time-Series Momentum: Is It There?", Journal of Financial
  Economics 135(3), 2020, pp. 774-794 (pages `[not checked]`).** `[secondary]`. The asset-level
  predictability behind TSMOM is weak; much of the portfolio's return is explained by
  holding assets with high past mean returns.
- **L10. Fidelity Investments, "Trend-following crisis alpha: does it come from beta timing or
  market selection?"** (practitioner note, 2026). `[secondary]` (web page; the PDF did not
  load). Splits a simple trend model into **beta timing** (long or short an asset class and how
  much) and **relative value** inside a class: beta timing carries over 76% of the risk (a
  companion note: about 78% of the excess return) and is more negatively correlated with
  equities in down months. A sponsor's own numbers.
- **Year reviews (practitioner, for 2008 and 2022 by asset class).** Mount Lucas, "Managed
  Futures - 2022 Review" (blog, 2023-01-30) `[pages read]`: "In 2008 the right Managed
  Futures positions were short commodity markets, long bonds and long the USD"; in 2022 "the
  short side of bond markets" and "the long side of commodity markets" (first half), the USD
  up against the major currencies (second half). SG Trend Indicator 2022 attribution (fixed
  income, currencies and energy gave the bulk) `[secondary]` via a search summary, source page
  not opened. WisdomTree (2026 blog) says managed futures' 2022 return was "driven almost
  entirely by short positions in bonds and equities" `[pages read]`, with no numbers.

### What share of trend funds' crash-year gains came from shorts, by asset class

**No source read gives a numeric long/short share for any crash year.** The decompositions that
exist are by asset class (sector attribution charts, as images) or by beta timing vs relative
value (L10), and the one leg split found (L6) is over the full sample, where the **long** legs
carry most of the return. What the sources do say, by year and class:

| Crash | Equities | Bonds | Commodities | Currencies | Sources |
|---|---|---|---|---|---|
| 2008 (Q4 mostly) | **short** gained (after Q3 losses set the shorts up) | **long** gained (bonds rose) | **short** gained (after the mid-year top; long first half) | long USD (and long yen) gained | L1 Section 4.3, Mount Lucas |
| 2020-02..03 | too fast to be short in time (L2's 1987 point); a loss or flat | **long** gained (trend was long bonds into the crash) | short energy gained `[not checked]` | mixed `[not checked]` | L2 (mechanism); no year review read |
| 2022 | **short** helped (WisdomTree) | **short** gained (yields rose all year; the largest single source) | **long** gained (energy, grains, first half) | long USD gained (yen fell) | Mount Lucas, SG via summary, WisdomTree |

Plain reading of the sources:

1. **Crisis alpha is beta timing that may be either sign**, not "the short side" alone. In
   2008 a big part was **long** bonds and long USD; in 2022 a big part was **long**
   commodities and long USD. The shorts that mattered were equities and commodities in 2008
   and bonds in 2022. So the missing pieces in `tsmom12` are (a) the short side (2008 equity
   and commodity shorts, 2022 bond shorts) **and** (b) assets it does not hold at all
   (currencies, energy, grains; it holds only gold among commodities).
2. **The short legs pay in crises and cost in normal times** (L5's restriction result, L6's
   full-sample split). So adding shorts should raise crash-year returns and correlation with
   the funds, and may lower the long-run mean.
3. **Fast crashes are not caught** (L2): 2020-02..03 is the year where a 12-month long-short
   rule should do least, and the funds' +4% there came mostly from shorter signals and bonds.
4. **Volatility scaling is part of the effect** (L7): a faithful replication must scale like
   L1, not hold equal weights in or out.

This is the hypothesis step 2 checks on ETFs: a long-short, volatility-scaled TSMOM on a wider
ETF universe should move with the live funds (correlation >= 0.5) and gain in 2008 and 2022;
long-only on the same universe should not; the four-asset narrow set should fall in between or
fail even long-short (too few classes). Step 2's card fixes all of this before any number.

Not read, would sharpen the answer: the Hamill et al. paper itself (its tables of
non-positive restrictions), Greyserman and Kaminski, *Trend Following with Managed Futures: The
Search for Crisis Alpha* (Wiley 2014), and the SG Trend Indicator's sector attribution files
(the SG site sits behind a bot wall, `survey-5.md`).
