# Survey 8: 2017-2026 literature on intermediaries, rebalancing flows, macro and text indices, cross-asset lead-lag and real-time data (2026-11-25, UTC)

Lane `survey-8` of the night lead (WIDER lane, research only, fake money). Branch `survey-8`
from `origin/main` (`d84fe39`). Format, filters and power yardstick as in `survey-7b.md`.

No test was run, no price or return was loaded, no statistic was computed on any data. One
header row of the cached JST R6 file was read to list its column names (no values). Each
mechanism listed gets a `note` row in `tries.md` (the brief asks for it; survey-7b wrote none),
with kind `note`, no Sharpe, so it is not selectable and does not move N in `BAR.md`.

## Question and the filters used

Which work on asset-allocation-level return predictors **outside** what `survey-2026-11.md`,
`survey-2.md` .. `survey-7.md`, `survey-7b.md` and `ideas.md` cover is worth listing? Topics
from the brief: (a) intermediary and dealer balance sheets, (b) flows and fund-rebalancing
pressure, (c) macro-uncertainty and text indices published with a lag, (d) cross-asset
lead-lag, (e) carry and term structure beyond `carry-2`/`carry-3`, (f) real-time-data vintages,
(g) ML on macro data with an out-of-sample asset-class Sharpe, (h) replications. The focus is
2022-2026; older papers appear where the 2022-2026 work tests or extends them, or where the
mechanism had no entry here at all (the consumption line, 2020, is one).

Each item is scored on:

- **F1, not announced; F2, not driven by price** (`wide-11.md`, #109). F2 fails when the dose
  is a transform of the asset's own price; it passes "with controls" when the dose is something
  else that may react to price.
- **Power** (`power-map-1.md`, #150; `research/register/BAR.md`). A strategy pick needs
  z >= 4.70 against `tsmom12` (N_eff 506): about +0.44 Sharpe at 80% power on the six assets,
  +0.18 pooled over 13 developed markets; plausible edges are at most +0.10. A single macro
  timing signal is class C1/C4 there: **dead on power as a pick, whatever the paper says.**
  The only form in which a macro predictor can say anything is a **gate** (event study or
  predictive regression, judged against its own placebos, `gate-null.md`) at the family bar
  **p < 0.10 / 103 = 0.00097** (one-sided z about 3.10; 103 mechanisms per `SUMMARY.md`,
  night 5 and the morning merges; listing alone does not add to the count, #191).
- **Unseen data.** survey-7b's lesson stands: a published effect keeps 0-30% of its paper size
  once investable and out of sample. A gate only means something on data the source papers
  never used (pre-sample, post-sample or other countries).

**Already covered, so not listed again** (grep of the surveys, `ideas.md`, `tries.md`,
`gate-null.md`, `data-wide-1.md`, `wide-*.md` on 2026-11-25): Pitkajarvi-Suominen-Vaittinen
cross-asset momentum (bond-to-stock lead-lag; `xtsmom` dead, survey-3); Goyal-Welch-Zafirov
2024 (survey-2026-11 item 14); Kelly-Malamud-Zhou and Nagel's reply (survey-2026-11 items 22,
23); Etula et al. "dash for cash" (survey-2026-11 E3); Greenwood-Vayanos duration supply
(wide-12 D4); Cieslak-Morse-Vissing-Jorgensen (`fomc-cycle`); GPR index (W25); foreign official
custody flows (W23); COT hedging pressure (W22); Z.1 margin receivables (W33); ICI fund flows,
ETF shares outstanding, FINRA margin debt (filtered F2 by `data-wide-1.md`); EPU daily
(`data-wide-1.md` row 5, scored 3, "heavily studied, fails unseen"); news-implied volatility
(wide-15 X10, filtered); the Fed balance sheet, M2, credit spread, curve inversion, real rate,
oil, 10-year yield gates (`macro-1`, `yt-1`, all dead); `ts-carry` (stock and bond carry, dead);
`rebalance-pressure` (month-end stock/bond leader, dead); `dealer-backlog` (auction dealer
share, dead); `vix`, `vrp`, `usd_13w` (screened in `info-1`/`slow-1`; `usd-1`).

## What is new, item by item

Access tags as in survey-7b: `[full text]`, `[first pages]`, `[abstract]`, `[secondary]`,
`[search summary, unverified]`, `[memory]`.

### (a) Intermediaries and dealers

**I1. Baron and Muir, "Intermediaries and Asset Prices: International Evidence since 1870",
Review of Financial Studies 35(5), 2022, pp. 2144-2189, DOI 10.1093/rfs/hhab077.** `[abstract;
discussant slides with the main table (Manela, 2019)]`
- Claim: balance-sheet growth of banks and securities firms predicts **lower** returns on
  stocks, bonds, currencies and housing; stronger at short horizons, outside crises too, and
  where intermediaries hold more of the asset. Working-paper table (US, UK, Japan, 1870-2016,
  annual): bank asset growth on 1-3-year real stock returns -0.01 to -0.06, t -0.6 to -4.3
  depending on clustering; R2 0.4-12%; 263-377 country-years.
- Data: hand-collected bank and broker balance sheets; not keyless. The nearest keyless dose is
  JST bank credit (`tloans`), which is I3's dose, not this one.
- Out of sample: none formal in the slides; the long sample is used for power. Post-sample in
  any public file: 2017-2020 (JST R6 ends 2020).
- Folded into I3 (same mechanism family, same data region); no own row.

**I2. Haddad and Muir, "Do Intermediaries Matter for Aggregate Asset Prices?", Journal of
Finance 76(6), 2021, pp. 2719-2761.** `[abstract, research brief]`
- Claim: intermediary health (He-Kelly-Manela capital ratio, Adrian-Etula-Muir leverage)
  predicts returns more where households are less active: CDS, MBS, FX, commodities, credit.
  Equities are the class where it should matter least.
- What it changes here: it is the authors' own reason to expect **little** from an intermediary
  signal on SPY, QQQ or a stock index. It lowers the prior of I4, I5 and I6 on our assets.

**I3. Davis and Taylor, "The Leverage Factor: Credit Cycles and Asset Returns", Management
Science 68(10), 2022, pp. 7350-7361, DOI 10.1287/mnsc.2022.4508 (NBER w26435).** `[full text,
working paper]` With Baron and Xiong, "Credit Expansion and Neglected Crash Risk", QJE 132(2),
2017 `[abstract]`, and I1.
- Claim: the three-year change in bank loans to GDP (JST) predicts lower real equity returns:
  above-median credit growth 6.8% a year against 11.5% below median (14 countries, 1950-2015);
  -300 to -400 bp a year per unit in local projections; bonds barely affected. Out-of-sample
  recursive stock/bond/bill allocation, 1970-2015, 14 countries: Sharpe 0.78 for the leverage
  signal alone, 0.94 with momentum and value against 0.83 without it (+0.11), 60/40 0.45.
- Data: JST R6 (`tloans`, `gdp`, `eq_tr`, `bond_tr`), cached locally (CC BY-NC-SA, hand
  download, `data-long-4.md`); BIS credit-to-GDP after 2020 (keyless).
- Seen data: 1950-2015 by Davis-Taylor; 1870-1913 in their binned table; 1920-2012 by Baron and
  Xiong (bank and market equity). **Unseen: 2016-2025 only**, about 10 years x 14 markets that
  move together.
- F1 pass (b, a premium); F2 pass with controls (GDP in the ratio falls in recessions; credit is
  not a price). Closest try: none (W33 is margin receivables times this month's fall, monthly).
- Power: on 2016-2025 a gate has roughly 10 annual observations per market with cross-market
  correlation near 0.6, so 15-25 effective years: **kill-only at best, dead on power.** As a
  pick (stock weight tilt) it is C1: dead on power.

**I4. Adrian, Etula and Muir, "Financial Intermediaries and the Cross-Section of Asset
Returns", Journal of Finance 69(6), 2014; Adrian, Moench and Shin, NY Fed Staff Reports 422
(2010) and 625 ("Dynamic Leverage Asset Pricing").** `[search summary, unverified]`
- Claim: broker-dealer leverage from the Fed's Financial Accounts prices the cross-section
  (AEM); the **level** of broker-dealer leverage predicts low future returns on stocks,
  Treasuries and corporate bonds, also out of sample (AMS).
- Data: Z.1 security brokers and dealers, total assets and liabilities, quarterly from 1952,
  keyless via FRED's graph CSV (as W33 did); published about ten weeks after the quarter and
  revised (real-time vintages: ALFRED, partly).
- Post-sample: about 2013-2025 (about 50 quarters). Pre-sample: 1952-1967 for AEM's 1968 start.
- F1 pass (b); F2 with controls (dealer assets are marked to market). Haddad-Muir (I2): weak in
  equities. Power: one quarterly series, about 30 unseen years: **dead on power.**

**I5. He, Kelly and Manela, "Intermediary Asset Pricing: New Evidence from Many Asset Classes",
JFE 126(1), 2017.** `[abstract]` (older; its data are the reference input of I2)
- The capital ratio is primary dealers' **market** equity over market equity plus book debt;
  the authors keep an updated series on their site (keyless per earlier visits `[memory]`, not
  opened tonight). Shocks are priced across asset classes; as a time-series predictor it is a
  transform of bank-holding-company share prices, which fall with SPY.
- F2: **fails in practice** (a price of a sector of the asset itself); with controls at most.
  Post-sample 2013-2025, quarterly. **Dead on power and filter.**

**I6. Du, Hebert and Li, "Intermediary Balance Sheets and the Treasury Yield Curve", JFE 150,
2023, 103722 (NBER w30222).** `[full text, working paper, searched]`
- Claim: dealers switched from net short to net long Treasuries after 2008; yields sit near the
  "net long" bound since; dealer positions move **opposite the term spread** (they add when the
  curve is flat). The paper does not test dealer positions as a return predictor.
- As a TLT dose (NY Fed primary-dealer positions, weekly, keyless), it is the term spread with
  a minus sign: **duplicate** of `yield-curve` (dead) and `ts-carry`'s TLT leg. Dead (overlap).

### (b) Flows and fund-rebalancing pressure

**R1. Harvey, Mazzoleni and Melone, "The Unintended Consequences of Rebalancing", NBER w33554,
2025 (version 2026-01-14; AFA 2026).** `[full text, first pages and method section]`
- Claim: two signals of balanced-fund rebalancing, 1997-09 .. 2023-03, daily. *Threshold*:
  the drift of a 60/40 book from its target since the last rebalance, averaged over bands
  0-2.5%; *Calendar*: the same drift on the last business days of the month. When stocks are
  overweight, equity returns are about 16-17 bp lower and bond returns 2-4 bp higher **over the
  next day**; the pressure reverts almost fully within two weeks; strongest near quarter-ends;
  significant only since the early 2000s; also in international equity. A long-short S&P 500
  versus 10-year note futures book on both signals: Sharpe above 1, 1997-2023 (in sample).
- F1: the Calendar signal **fails** (month-end dates are public; it is the month-end family
  again). F2: the Threshold signal **fails** (by construction a function of trailing SPY-minus-TLT
  returns; the paper itself shows it loads on 1-20-day equity returns).
- Closest tries: `rebalance-pressure` (dead: the month's leader halved in the last five
  sessions, -0.005), `month-end-liquidity`, `month-end-bonds` (dead, not replicated).
- Horizon: one day, gone in two weeks; our book decides on Friday closes with next-open fills,
  so it cannot hold the effect. **Dead (filters and overlap)**; a daily-lane idea at most, and
  front-run by the funds' own desks per the paper's interviews.

### (c) Macro uncertainty and text indices published with a lag

**X1. Bybee, Kelly, Manela and Xiu, "Business News and Business Cycles", Journal of Finance
79(5), 2024, pp. 3105-3147 (NBER w29344).** `[full text, working paper, searched]`
- 180 topics from 800,000 WSJ articles, 1984-2017. News attention **explains** 25% of the
  variation of contemporaneous market returns (out-of-sample R2 17.8% in an expanding window is
  also a contemporaneous fit). No predictive return claim beyond the VAR for macro series.
- **Not a predictor; not listed.**

Not listed either: the SF Fed daily news-sentiment index (keyless, daily from 1980; its
published validation is against consumer surveys, no return claim found); trade-policy
uncertainty (Caldara et al. 2020, same newspaper-count design as the GPR gate W25, dead);
the Jurado-Ludvigson-Ng macro-uncertainty index `[memory]` (estimated with full-sample
parameters, so a vintage is not what was known; its financial half is price-based, F2).

### (d) Cross-asset lead-lag

**L1. Huang and Kilic, "Gold, Platinum, and Expected Stock Returns", JFE 132(3), 2019;
follow-ups 2020-2024.** `[abstract]` Xu, Li and Singh, International Journal of Managerial
Finance 2021 `[abstract]`: the **change** of the gold-to-platinum ratio (not its level) predicts
returns in 17 developed markets and the world index, out of sample. Pacific-Basin Finance
Journal 62, 2020 `[abstract]`: confirms the US, fails in China. Pham and Rudolf `[abstract]`:
stronger for cyclical industries; one-month out-of-sample forecast weak.
- F1 pass (b). F2: pass with controls for SPY (other assets' prices, which react to the same
  news); **fails for GLD** (its own price is in the ratio).
- Data: platinum prices back to the 1970s are LBMA (licensed) or the World Bank Pink Sheet (403
  to scripts, `next-steps.md` item 8); keyless continuous futures cover only recent decades
  (to verify). Post-sample after Huang-Kilic (data to about 2018): about 7 years.
- One global dose for all markets, so pooling does not add independent years. **Dead on power.**

**L2. Jeanneret and Sokolovski, "Commodity Prices and Currencies", working paper 2023-09;
"Looking Under the Hood of Commodity Currency Predictability", Management Science (2025, DOI
10.1287/mnsc.2024.07249; authorship not confirmed).** `[abstract, search summary]`
- Claim: monthly changes in a country's commodity export prices predict its currency, out of
  sample against the random walk; concentrated at short horizons and in a few thinly traded
  (mostly emerging) currencies: slow information diffusion, not a premium.
- Not on the six assets; data-long-4's nine developed currencies are the liquid ones where the
  paper finds little. A cross-section of currencies needs shorts (B7). **Parked** (not
  applicable; informational at most).

**L3. Kelly, Malamud and Pedersen, "Principal Portfolios", Journal of Finance 78(1), 2023,
pp. 347-387.** `[abstract]`
- Uses every asset's signal (momentum, carry, value) to predict every other asset's return; the
  antisymmetric part ("principal alpha portfolios") earns out-of-sample alpha across datasets.
- F2 fails (price signals); on six assets it is a lead-lag search of the kind `xtsmom`,
  `contagion-catchup`, `transfer-entropy` and `spillover` already killed (non-synchronous closes
  of coins and ETFs). **Dead (overlap).**

### (e) Carry and term structure beyond carry-2 / carry-3

No 2022-2026 time-series carry or term-structure predictor for the six assets turned up that
is not `ts-carry` (stock and bond carry, dead), the curve gates (dead), the VIX term structure
(`vix_term` in `info-1`) or crypto funding (`carry-2`/`carry-3`, held-out fail). Du-Hebert-Li
(I6) is the one new term-structure paper, and it reduces to the term spread. Commodity basis
and currency carry need assets the gym does not hold. **Nothing new listed.**

### (f) Real-time data vintages and (g) ML on macro data

**M1. Atanasov, Moller and Priestley, "Consumption Fluctuations and Expected Returns", Journal
of Finance 75(3), 2020, pp. 1677-1713, DOI 10.1111/jofi.12870** `[abstract, search summary]`;
**Melone, "Consumption Disconnect Redux", working paper 2022-06** `[full text, first 800
lines]`; Moller and Rangvid, "End-of-the-Year Economic Growth and Time-Varying Expected
Returns", JFE 115(1), 2015 `[search result title]`.
- Claim: when consumption is low against its own trend (marginal utility high), expected stock
  returns are high. AMP: "cyclical consumption" (a Hamilton-filter residual of log
  consumption), US post-war, slope negative in every country of an international sample, and
  it subsumes many standard predictors. Melone: the "consumption gap" (consumption below the
  level warranted by productivity expectations), US 1967-2020, R2 3.9% (quarter) to 12.1%
  (year) in sample, significant out of sample (Campbell-Thompson R2), a mean-variance timer
  worth 2.39% a year in certainty equivalent; **with real-time vintages 1997-2020** (second lag,
  Philadelphia Fed real-time data) the in-sample R2 is 6% (quarter) to almost 20% (year) and
  the out-of-sample test holds. In Melone's table AMP's measure has R2 2.4% (quarterly).
- Why it is new here: no file in `research/` mentions consumption as a predictor (grep
  2026-11-25); `cay` was never tested.
- F1 pass (b, a premium). F2 **pass with controls**: consumption answers wealth, so a crash
  lowers consumption and raises the predictor just before a rebound; controls are the market's
  own trailing 1- and 3-year returns and the dividend yield, and the feedback is shown.
- Keyless data: JST R6 `rconsbarro` (Barro-Ursua real consumption per capita), 17 countries
  from 1870, cached locally (`data-long-4`; coverage per country to be checked by the card
  before any return is read); Philadelphia Fed Real-Time Data Set (real consumption vintages
  from 1965, keyless xlsx; part of it is already cached under `philly-rtdsm/`).
- **Unseen data: 1870-1946 in every JST country** (all three papers are post-war; one related
  long-run paper, Pozzi, tests the consumption-income ratio 1870-2015 for four countries and
  finds it inconclusive `[abstract]`), and the US after 2020 (Melone) or 2017 (AMP).
- Power: see the card sketch. As a pick: C1, dead. As a gate on 1870-1946: within reach **only
  if most of the published size survives** (needs a pooled annual R2 of about 6%; Melone's
  in-sample 12% at one year is the ceiling, the 0-30% haircut puts it at 0-4%). Top 1.

**M2. Bianchi, Buchner and Tamoni, "Bond Risk Premiums with Machine Learning", RFS 34(2), 2021,
pp. 1046-1089; corrigendum with Hoogteijling, RFS 34(2), 2021, pp. 1090-1103.** `[abstract,
search summary]`
- Claim: neural networks on 128 FRED-MD series plus forward rates predict bond excess returns
  out of sample. The corrigendum: the original used data not available in real time; with
  real-time macro data the out-of-sample gain shrinks, and only the neural net stays significant.
- Data: FRED-MD vintages (monthly since 1999, keyless) `[memory]`. Target: TLT, a single timing
  signal. Closest tries: `ml-linear`, `ml-gbm` and the other `ml-*` (dead), `slow-1` (49
  inputs at 4 and 13 weeks, none passes), `y10`, `yield-curve`.
- F2 fails for the forward-rate inputs (bond prices), passes for macro. **Dead on power**, and
  the corrigendum is itself the replication: half the paper result was look-ahead.

**What M1-M2 and I3 say about real-time data and ML on macro.** The two cleanest asset-class
out-of-sample numbers found tonight are Davis-Taylor's +0.11 Sharpe (credit added to momentum
and value in a 14-country stock/bond book, 1970-2015, annual) and Melone's real-time 1997-2020
test. Both are in-sample to their authors' choice of predictor. Bianchi et al.'s corrigendum
is the warning: a revised-data macro predictor can lose most of its out-of-sample gain once
vintages are used, so any card here must use vintages or the second lag, as Melone does.

## Sites that blocked or gated scripts

- `repec.cepr.org` (CEPR discussion-paper PDFs): 403 to a plain script fetch; the NBER copy of
  the same paper opened.
- `biopen.bi.no` (AMP's open-access copy): DNS lookup failed from this machine.
- `www.wu.ac.at` (Jeanneret-Sokolovski PDF): TLS error on a plain script fetch.
- The fetch tool returns binary PDF for EDHEC, Manela's slides and NBER; text came from a
  local `pdftotext` of the saved file.
- Paywalled: RFS, JF, Management Science, QJE, JFE publisher pages. SSRN not tried (earlier
  surveys record 403).
- A browser pass could read AMP's international table (M1) and the Management Science
  commodity-currency paper (L2); neither would change a verdict here.

## Scoreboard (new mechanisms only)

| # | Mechanism (`ideas.md` name) | Source | F1 | F2 | Closest try (disguise) | Keyless data | Unseen data | Can it reach the bar? | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `consumption-cycle` | M1 (JF 2020; WP 2022; JFE 2015) | pass (premium) | pass with controls (wealth feedback) | none (no consumption predictor tried) | JST `rconsbarro` 1870- (cached); Philly Fed real-time vintages | **1870-1946, 17 countries**; US after 2020 | gate: only if ~all of the paper size survives; pick: no | **top 1** (gate) |
| 2 | `bank-capital-premium` | I2, I5 theory; JST `lev` (Jorda et al. 2021 used it for crises only) | pass (premium) | pass with controls (loan losses follow falls) | none; W33 is margin receivables | JST `lev` 1870- (cached) | no return test on this dose found (Baron-Muir used asset growth) | gate: weak (slow, trending dose; Haddad-Muir expect little in equities); pick: no | **top 2** (gate, likely kill-only) |
| 3 | `credit-boom-leverage` | I3 (MS 2022), Baron-Xiong (QJE 2017), I1 (RFS 2022) | pass | pass with controls | none | JST `tloans`/`gdp`; BIS credit-to-GDP | 2016-2025 only | no (15-25 effective years) | parked (kill-only) |
| 4 | `dealer-leverage` | I4 (JF 2014; NY Fed SR 422/625) | pass | with controls (assets marked to market) | W33 (same Z.1 table, other dose) | Z.1 via FRED, quarterly 1952- | 1952-1967, 2013-2025 | no (one quarterly series) | dead on power |
| 5 | `intermediary-capital-ratio` | I5 (JFE 2017), I2 (JF 2021) | pass | **fail** (dealers' market equity) | `credit-spread` (dead) | authors' site `[memory]` | 2013-2025 | no | dead (filter, power) |
| 6 | `dealer-treasury-position` | I6 (JFE 2023) | pass | with controls | `yield-curve`, `ts-carry` (the term spread with a minus sign) | NY Fed dealer positions, weekly | 2023- | no | dead (overlap) |
| 7 | `rebalance-threshold` | R1 (NBER 2025/2026) | calendar part **fails** | threshold part **fails** | `rebalance-pressure`, `month-end-*` (dead) | SPY, TLT daily | 2023- | no (one-day effect, weekly book) | dead (filters, overlap) |
| 8 | `gold-platinum` | L1 (JFE 2019; IJMF 2021) | pass | pass with controls (SPY); fail (GLD) | `oil` (dead) | platinum history not keyless before recent decades | about 2019-2025 | no (one global dose) | dead on power |
| 9 | `commodity-currency` | L2 (WP 2023; MS 2025) | pass | pass with controls | none | commodity export prices (IMF); FX from data-long-4 | post-2021 | not applicable to the six; B7 | parked |
| 10 | `ml-macro-bonds` | M2 (RFS 2021 + corrigendum) | pass | fail (forward rates) / pass (macro) | `ml-*`, `slow-1`, `y10` (dead) | FRED-MD vintages `[memory]` | post-2016 | no (single TLT signal) | dead on power |
| 11 | `principal-portfolios` | L3 (JF 2023) | pass | fail | `xtsmom`, `contagion-catchup`, `transfer-entropy`, `spillover` (dead) | yes | - | no | dead (overlap) |

Not listed (no new mechanism or not a predictor): X1 business-news attention (contemporaneous),
SF Fed news sentiment (no return claim), trade-policy uncertainty (design of W25), JLN
uncertainty (look-ahead in construction), Baron-Muir asset growth (folded into row 3; data not
keyless), Haddad-Muir (a prior, not a dose).

**Count.** `SUMMARY.md`: 103 mechanisms, 29 tested by a strategy, 30 gates, none passed. This
lane adds **11 listed, 0 tested, 0 gates**; by the #191 rule a listing does not enter the count,
so the family bar for the next test stays **p < 0.10 / 103 = 0.00097**, and a card that runs
row 1 or 2 would make it 104 (0.10 / 104 = 0.00096). Project bar unchanged: N_eff 506,
z >= 4.70 (`BAR.md`).

**The honest summary.** Ten of the eleven are dead or parked before any data: they fail a
filter, duplicate a dead try, do not apply to the six assets, or have under 30 unseen years for
a single slow signal. The only two that can say anything are annual gates on the JST panel
before 1947, and both are long shots: row 1 needs the published effect to survive almost
whole on data from a different century, row 2 has a dose that trends for decades and an
authors' own prior (I2) that equities are where intermediaries matter least.

## Top 2 for a future lane (card sketches; not cards, nothing was run)

### 1. `consumption-cycle`: does consumption below its own trend predict higher stock returns in 1870-1946?

- **Why this one.** A premium mechanism (F1 pass) whose dose is not a price (F2 with controls),
  with three published papers that all used post-war data, so the JST panel before 1947 is
  unseen by every source; the dose is in a file we already hold; and the real-time result
  (Melone) answers the vintage objection for the post-war US.
- **Hypothesis (sign fixed).** Lower cyclical consumption at the end of year t predicts higher
  real equity total return in year t+1 (and t+1..t+3), pooled across JST countries.
- **Data.** JST R6 `rconsbarro` (real consumption per capita), `eq_tr`, `bill_rate`, `cpi`,
  `eq_dp`, 1870-1946; countries with at least 40 consumption years (listed by the card from
  coverage counts before any return is read). Train only; JST ends 2020, nothing after
  2025-10-31 exists in it. Cite Jorda, Schularick and Taylor (2017); CC BY-NC-SA; nothing
  committed but derived statistics.
- **Dose (fixed before any number).** AMP's construction in annual form: cc_t = c_t minus the
  fitted value of a regression of c_t on c_{t-2} and c_{t-3} (Hamilton filter, h = 2 years,
  two lags), estimated by expanding window per country (first 20 years burn-in), so the dose
  is known at t. Second form, reported only: the 5-year deviation of log consumption from its
  trailing 10-year mean.
- **Statistic.** Pooled regression of the next year's real excess equity return on the
  standardised dose (per-country expanding z), with country fixed effects; controls: the
  market's own trailing 1- and 3-year real returns and `eq_dp` (wealth feedback, F2). SE:
  Driscoll-Kraay, 2 lags. Null: 40 placebo calendars (dose shifted by k = 5..44 years within
  country, both ways, `gate-null.md` step 1), and the earlier-dose half reported separately.
- **Pass / kill (fixed).** Gate W-next. Pass: one-sided p < 0.00096 (family bar at 104) **and**
  rank 1 of 41 against placebos **and** the sign holds in both halves (1870-1913, 1920-1946)
  with the wars (1914-1919, 1939-1945) dropped. Kill: t >= 0 (wrong sign) or rank worse than
  10 of 41. Between: inconclusive. Replication (if pass): US 2021-2025 on Philadelphia Fed
  vintages with Melone's second lag, sign only (five years: kill-only).
- **Power, stated before any number.** About 15 countries x 65 usable years = 975
  country-years; cross-country correlation of annual returns about 0.4 gives roughly 160
  effective years. t is about sqrt(R2 x 160): R2 2% -> 1.8, 4% -> 2.5, 6% -> 3.1 (the bar),
  12% (Melone's in-sample ceiling) -> 4.4. With the 0-30% haircut a pass is unlikely; a clean
  kill (t >= 0) is the likely informative outcome. The `jst-autocorr-1` caveat applies (early
  annual returns have a lag-1 autocorrelation near 0.19 of unknown origin): the controls
  include the lagged return, and the placebo null absorbs the rest.
- **What it cannot do.** Change the book: even a pass is a fact about 1870-1946 stock markets;
  as a stock-weight tilt on the six it is class C1 (needs +0.44, plausible +0.10).

### 2. `bank-capital-premium`: does thin bank capital predict higher stock returns, 1870-2020?

- **Why this one.** The intermediary-asset-pricing prediction (He-Krishnamurthy; HKM) tested on
  a **book** capital ratio, which is less price-driven than HKM's market ratio, on a long panel
  where, as far as this search found, nobody has run it as a return predictor (Jorda, Richter,
  Schularick and Taylor, Review of Economic Studies 88(1), 2021, used it for crisis risk and
  found little; Baron-Muir used asset growth). The dose is already cached.
- **Hypothesis (sign fixed).** A banking sector capital ratio below its own trailing trend at
  the end of year t predicts higher real equity (and government bond) excess returns in t+1.
- **Data.** JST R6 `lev` (capital to assets), `eq_tr`, `bond_tr`, `bill_rate`, `cpi`,
  `crisisJST`; all years with `lev`; post-war and pre-war halves reported.
- **Dose (fixed).** lev_t minus its trailing 10-year mean (the level trends down from the 19th
  century into the 1950s; the detrending is the only parameter), per-country expanding z.
- **Statistic, null, pass/kill.** As in sketch 1, with the systemic-crisis dummy (`crisisJST`)
  as an extra control so the dose is not a crisis flag in disguise (Muir 2017 `[memory]`:
  premia rise in financial crises). Pass at p < 0.00096 and rank 1 of 41 and the sign in both
  halves; kill at the wrong sign or rank worse than 10.
- **Power, before any number.** The dose moves slowly (book capital changes over years), so a
  10-year detrended series has perhaps 10-15 independent swings per country over 150 years;
  Haddad-Muir (I2) expect little in equities. **Likely kill-only**; listed second because it is
  the one intermediary dose with long, keyless, unseen data, not because it is likely to pass.

## Checks

Docs only (this file, `ideas.md` rows, `tries.md` note rows). `uv sync && uv run ruff check .
&& uv run ruff format --check . && uv run mypy && uv run pytest` run before the PR (see the PR).
Downloads: six paper PDFs (about 7 MB) into a scratch folder outside the repo; no market data.

## Sources (opened or searched 2026-11-25, UTC)

- I1 <https://ideas.repec.org/a/oup/rfinst/v35y2022i5p2144-2189..html>;
  <http://asaf.manela.org/discussions/Manela_Discussion_of_BM_2019.pdf> (discussion slides)
- I2 <https://nber.org/papers/w28692>;
  <https://anderson-review.ucla.edu/when-financial-intermediaries-sneeze-these-assets-catch-a-cold/>
- I3 <https://www.nber.org/papers/w26435> (PDF read);
  <https://econpapers.repec.org/RePEc:inm:ormnsc:v:68:y:2022:i:10:p:7350-7361>;
  Baron-Xiong <https://www.nber.org/papers/w22695>
- I4 <https://www.newyorkfed.org/research/staff_reports/sr464.pdf>,
  <https://www.newyorkfed.org/research/staff_reports/sr422.pdf>,
  <https://www.newyorkfed.org/research/staff_reports/sr625.pdf> (not opened)
- I5 <https://bfi.uchicago.edu/wp-content/uploads/jfepublishedversion.pdf> (not opened)
- I6 <https://nber.org/papers/w30222> (PDF read)
- R1 <https://www.nber.org/papers/w33554>;
  <https://www.edhec.edu/sites/default/files/2026-03/Scientific%20paper.%20ssrn-5122748.pdf>
  (PDF read)
- X1 <https://www.nber.org/papers/w29344> (PDF read)
- SF Fed news sentiment <https://www.frbsf.org/research-and-insights/data-and-indicators/daily-news-sentiment-index/>
- L1 <https://www.emerald.com/insight/content/doi/10.1108/IJMF-06-2020-0328/full/html>;
  <https://ideas.repec.org/a/eee/pacfin/v62y2020ics0927538x20301104.html>
- L2 <https://pubsonline.informs.org/doi/10.1287/mnsc.2024.07249>;
  <https://www.wu.ac.at/fileadmin/wu/d/ri/isk/VSFX_2021/Papers/20230910_Commodity_Prices_and_Currencies_Jeanneret_Sokolovski_SSRNlink.pdf>
  (TLS error)
- L3 <https://ideas.repec.org/a/bla/jfinan/v78y2023i1p347-387.html>
- M1 <https://econpapers.repec.org/RePEc:bla:jfinan:v:75:y:2020:i:3:p:1677-1713>;
  <https://acfr.aut.ac.nz/__data/assets/pdf_file/0003/689016/Melone-Consumption-Disconnect-Redux.pdf>
  (PDF read); Pozzi <https://personal.eur.nl:443/pozzi/returns.pdf> (not opened);
  Engsted-Hyde-Moller <https://ideas.repec.org/a/eee/jimfin/v29y2010i7p1237-1255.html>
- M2 <https://repub.eur.nl/pub/134902>; <https://wrap.warwick.ac.uk/151797>
- Bank capital <https://www.nber.org/papers/w23287> (not opened)
