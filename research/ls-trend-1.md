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

## Step 2: the replication (card 9722e86, script f1e8931, run 2026-11-18)

Card: [`cards/ls-trend.md`](cards/ls-trend.md), pushed before any number. Tables:
[`results/ls-trend.md`](results/ls-trend.md). Moskowitz-Ooi-Pedersen's rule unchanged (sign of
the 12-month excess return, 40% / ex ante vol per asset, equal weight across the assets
alive, monthly), one day later than the paper, 5 bps a side, 1% a year borrow on shorts,
leverage financed at the bill. Wide = 34 ETFs (9 country equity, 4 Treasury, 15 commodity,
6 currency); narrow = SPY, QQQ, GLD, TLT. Nothing after 2025-10 read.

One disclosure: the script was first run once with logging switched off (a plumbing check),
then run again to log; both runs printed identical tables (the code did not change between
them).

**Logged as:** 4 rows of the new kind `replication` in `tries.md` (`<cell>@live-L`, defined
in its header: descriptive, not selectable, not counted). No `ledger/tries.jsonl` row. Family
unchanged: **68 mechanisms, 16 tested** (wide-6's reconciled count), next strategy test at
**p < 0.10 / 68 = 0.00147**. Long-short TSMOM is the same mechanism as `tsmom12`
(time-series momentum), so it adds no family member.

### What the numbers say (card's reading rules applied)

| Cell | 2008 | 2020-02..03 | 2022 | Corr. with TC (L) | Corr. with AQR factor | Corr. with SPY | Sharpe L | Reading |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| **wide-LS** | **+34.9%** | **+24.6%** | **+12.8%** | **0.61** | 0.81 | -0.17 | 0.15 | **reproduces** |
| wide-LO | +1.1% | -4.7% | -2.8% | 0.35 | 0.38 | 0.46 | 0.24 | does not |
| narrow-LS | +23.7% | -10.9% | -4.1% | 0.39 | 0.39 | 0.38 | 0.63 | does not |
| narrow-LO | +7.2% | -10.9% | -20.8% | 0.26 | 0.27 | 0.60 | 1.03 | does not |
| TC (live funds) | +7.1% | +3.6% | +17.6% | - | 0.71 | -0.06 | 0.19 | |
| AQR factor (paper) | +24.6% | +10.5% | +24.7% | 0.71 | - | - | 0.35 | |
| `tsmom12` | -1.6% | -14.1% | -12.9% | 0.17 | 0.09 | 0.40 | 1.11 | |

(Raw returns above the bill; wide-LS runs at 16.5% volatility, TC at 8.4%. At 10% volatility
wide-LS is +21% / +15% / +8% against TC's +8% / +4% / +21%.)

1. **Yes: long-short on the wide set looks like the live funds.** It gained in all three crash
   windows, correlates 0.61 with the nine-fund composite, 0.81 with AQR's paper factor, 0.64
   with AQMIX, and -0.17 with SPY. `tsmom12` correlates 0.08 with it. That is a faithful
   enough replication of the family from 34 keyless ETFs.
2. **Both missing pieces matter, and neither is enough alone.** By the card's rule the short
   side is a missing piece (wide-LO fails) and so is the universe (narrow-LS fails). The 2 x 2,
   crash returns at 10% volatility: adding shorts to the wide set adds +20% / +19% / +10%
   (2008 / 2020 / 2022) and +0.26 correlation with TC; on the narrow set only +7% / +1% / +9%
   and +0.13. Widening adds +10% / +20% / +10% when short is allowed, but almost nothing
   long-only (-3% / +2% / +9%). Shorts need many markets to short; many markets need shorts to
   pay in a crash.
3. **The crash gains are mostly short legs** (wide-LS, additive daily P&L): 2008 +34.6% total,
   **93% from shorts** (equity shorts +22.2%, currency shorts i.e. long USD +5.8%, commodity
   shorts +4.2%; long bonds +10.9% was the one big long). 2020-02..03 +23.7%: commodity shorts
   +16.4% (oil, gas), equity shorts +7.7%, long bonds +6.0%, equity longs -8.2%. 2022 +14.3%:
   **bond shorts +11.0%**, currency shorts (long USD) +6.8%, commodity longs +6.0%, equity
   longs -6.5%. Short legs gave 93%, 118% and 115% of the three crash gains (above 100% where
   the long legs lost). The literature's picture (step 1) holds: 2008 short equities plus long
   bonds and long USD, 2022 short bonds plus long commodities and long USD. 2020 differs from
   my expectation (I expected flat; L2 said too fast): the ETF book was already short oil and
   gas from 2019's downtrend, and after February's fall it shorted the European indexes.
4. **The narrow set cannot do it.** narrow-LS made 2008 (+23.7%: short SPY/QQQ +21.8%, long
   TLT +18.4%) but lost in 2022: its one bond short (TLT +20.3%) was eaten by its equity longs
   early in the year and the GLD position (-9.8%). With four assets, two of them equity, there
   is no USD leg, no energy, and no second bond.
5. **The price of the crisis alpha is the Sharpe.** In L wide-LS has Sharpe 0.15 (TC 0.19,
   AQR factor 0.35), against 1.03 for narrow-LO and 1.11 for `tsmom12`; worst calendar year
   -18.5% (2016). It needs 3.7x gross leverage on average (SHY at 40% / ~2% vol), turns over
   12x a year, and pays 0.60% a year in costs plus 1.40% in borrow. The funds' crisis alpha is
   real and reproducible, and so is their decade of near-zero returns: the long bull market
   that made `tsmom12` look good is exactly what long-short trend gives away.

Caveats: the ETF set has no non-US bonds and few currencies; several commodity ETFs only
exist from 2010-11; leverage above 1x is financed at the bill in the model; SHY's tiny
volatility makes it the largest position by notional; one day of delay against the paper.
The narrow-LS 2022 leg shares in the results table are meaningless (total +0.9%, near zero).

## Step 3: the plain answer, and what a forward test would take (proposal only)

**Does long-short reproduce the live funds' crash behaviour? Yes, and only when it is also
wide.** The same 12-month rule that `tsmom12` uses, run long-short and volatility-scaled over
34 ETFs in four asset classes, gained +35% in 2008, +25% in 2020-02..03 and +13% in 2022 and
moved with the live trend funds (correlation 0.61; 0.81 with AQR's paper factor). Long-only on
the same 34 ETFs did not (+1%, -5%, -3%; correlation 0.35), and long-short on `tsmom12`'s four
non-coin assets did not either (+24%, -11%, -4%; 0.39). So the missing crisis alpha is the
missing short side **and** the narrow universe together: in the crash windows 93-118% of the
gain came from short legs (equities in 2008, oil and gas in 2020, bonds in 2022, the dollar in
all three), and those shorts need markets `tsmom12` does not hold.

**What it costs.** The funds' other half came with it: Sharpe above bills 0.15 in 2010-2025
(funds 0.19), against 1.11 for `tsmom12` and 1.03 for the same rule long-only on four assets.
Long-short trend gives away the long bull market in exchange for gains in long bear markets.
Its monthly correlation with `tsmom12` is 0.08. That makes it a possible **diversifier** next
to `tsmom12`, not a replacement. Whether a blend helps is a new question with its own card. A
forward test would not settle "Sharpe above 0" within a lifetime: at 0.15 it takes about 350
years by forward-1's formula (normal returns, weekly, alpha 0.025, power 0.8); at the AQR
factor's 0.35, 64 years. Crash behaviour can only be judged when crashes come, about three in
18 years.

### Proposal (not built; nothing here changes the live runner or the paper broker)

What the paper broker would need before this could be tested forward, in order of size:

1. **Instruments.** About 30 more daily ETF series in `grimstrade.data` (the card's list,
   keyless Yahoo like the six already there): 8 country equity, 3 more Treasury, about 14
   commodity, 6 currency. The ingest is the existing code path. Smaller first cut: one ETF per
   sub-market, about 16 (SPY, EWJ, EWG, EWU; SHY, IEF, TLT; GLD, SLV, USO, UNG, DBB, DBA; FXE,
   FXY, FXA).
2. **Shorts in the gym** (`gym.py` rejects weights below 0 today): negative weights; short
   proceeds earn the bill (the gym pays 0 on cash today; `cash_interest.py` is the research
   what-if); a borrow fee accrued daily per symbol (start at the card's 1% a year flat, with a
   table for hard-to-borrow funds such as UNG and USO); dividends debited to the short side
   (the gym uses adjusted prices, so this is a check, not new code).
3. **Leverage, or a rescaled version.** The paper's sizing needs 3.7x gross on average (SHY
   alone is the largest notional). Either (a) allow gross above 1 with financing at bill plus a
   spread and a margin rule that forces a cut, or (b) **scale the whole book to gross <= 1**,
   which keeps every correlation and Sharpe the same before costs and divides the returns by
   about 3.7 (2008 about +9%, 2022 about +3.5%). (b) is much less work and stays inside "no
   leverage". A third route, **inverse ETFs** for the short side inside today's long-only gym,
   exists only for a few markets (SPY, TLT, the dollar) and loses to daily reset in choppy
   markets; not recommended as the main route.
4. **Costs to state before any forward run:** 5 bps a side, 1% borrow, about 12x turnover a
   year (0.6% + 1.4% a year at full leverage; a quarter of that at gross 1).
5. **How it would be judged.** Not on Sharpe (350 years). Two descriptive checks that can be
   read in a few years: monthly correlation with a live trend-fund composite (expected 0.5-0.7;
   SE about 0.1 after three years), and the sign of its return in the next equity or bond bear
   market. Logged in the forward registry as a **descriptive shadow**, not as a book rule,
   unless a separate card (the blend question) first passes the family bar
   (p < 0.10 / 68 = 0.00147).

## Count and next

Family unchanged: 68 mechanisms, 16 tested, none passed; long-short TSMOM is the same
mechanism as `tsmom12`. Four `replication` rows in `tries.md`; held-out year unspent.

Next, each a card before numbers:
1. **Blend:** `tsmom12` plus wide-LS at gross 1 (correlation 0.08), judged on worst year and
   on the Sharpe gap to `tsmom12` at the family bar. The best-founded use of this lane's result.
2. **Unlevered and smaller:** wide-LS scaled to gross <= 1 on the 16-ETF first cut, to see how
   much of the crash behaviour survives the paper broker's limits (descriptive).
3. **Signal speed for fast crashes:** Hurst-Ooi-Pedersen's 1/3/12-month blend on the same
   ETFs, the paper's own specification (no tuning), to check 2020-type crashes.
