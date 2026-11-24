# Survey 7b: 2024-2026 literature on trend crashes, tail hedging, volatility management, signal blending and anomaly decay (2026-11-24, UTC)

Lane `survey-7` of the night lead (WIDER lane, research only, fake money). **Name collision:**
a branch `survey-7` and a file `research/survey-7.md` already exist from an earlier lane
(the `seasonal-20y` gate, PR #97, merged). Neither may be rewritten or deleted, so this lane
runs as **branch `survey-7b`, file `research/survey-7b.md`, ideas status "listed (survey-7b)"**
(default picked without the owner; nobody could be asked). Branch from `origin/main`
(`fac43c9`).

No test was run, no price or return was loaded, nothing after 2025-10-31 was looked at. No
card (none is needed without a test) and no `tries.md` row (a survey is not a try).

## Question and the filters used

Which work published in 2024-2026 on (a) time-series trend following and how it behaves in
crashes, (b) tail hedging and crisis alpha, (c) volatility management, (d) signal blending and
(e) replication and decay of anomalies is **not already covered** by `survey-2026-11.md`,
`survey-2.md` .. `survey-6.md` and `ideas.md`? For each new item: claim, data and sample,
out-of-sample status, whether it survived publication, whether it is testable here with
keyless data, the closest try we already have (and the risk that it is a filter or a
volatility dial in disguise). Each is scored on:

- **F1, not announced; F2, not driven by price** (`wide-11.md`, #109). F2 fails when the dose
  is a transform of the asset's own price; it passes with controls when the dose is something
  else that may react to price.
- **Power** (`power-map-1.md`, #150): can a true edge of a plausible size ever clear the bar
  (z >= 4.70; `research/register/BAR.md`)? Reference numbers from power-map-1: an edge over
  `tsmom12` on the six assets needs about +0.44 Sharpe at 80% power (plausible: at most +0.10);
  pooled over 13 developed markets +0.18; a long-short book on about 100 years, scored in the
  alpha form (does it add to `tsmom12`?), needs an IR of 0.51-0.60. Tonight's `xs-century-1`
  (#170, merged) built exactly that book: gross IR +0.88 (z 7.4), at the cheaper published
  momentum cost IR +0.51, z 4.44 (`results/xs-century-1.md`, R2), since 1994 IR +0.19. That near miss is the only place where the bar
  is within reach, and it shapes the ranking below.

**Already covered, so not listed again** (checked by grep of the five surveys, `ideas.md` and
`tries.md`): Moskowitz-Ooi-Pedersen; Hurst-Ooi-Pedersen; Babu et al.; Man's crisis-alpha and
speed notes; Daniel-Moskowitz; Moreira-Muir, Cederburg et al., Harvey et al. (vol targeting),
Liu-Tang-Zhou, Barroso-Detzel; Goulding-Harvey-Mazzoleni turning points (and their
"Breaking Bad Trends" follow-up, same mechanism); Moskowitz-Sabbatucci-Tamoni-Uhl nonlinear
TSMOM; Benhamou et al. CTA replication (arXiv 2507.15876); Zarattini-Antonacci; Pitkajarvi et
al.; McLean-Pontiff, Hou-Xue-Zhang, Jensen-Kelly-Pedersen, Harvey-Liu-Zhu; Baltussen et al.;
Koijen et al. carry; live tail-hedge funds (survey-6); the VIX-call overlay (`vix-call-1`,
#167, merged); PPUT under trend (`insure-4`); volume-weighted trend (`volume-1`).

## What is new, item by item

Access tags as in earlier surveys: `[full text]` (read), `[first pages]`, `[abstract]`,
`[secondary]` (a summary by someone else), `[search summary, unverified]`.

### (a) Trend following and its crash behaviour

**T1. Kurth, Eisler, Rej and Bouchaud, "Is Trend Still Your Friend? A Microstructural Account
of the Demise of Short-Term Trend-Following", arXiv 2607.01550, 2026-07.** `[full text, first
100k characters]`
- Claim: since about 2009, trend PnL collapsed on **small-tick** futures (tick size small
  relative to daily volatility; ranked monthly, lower half) and stayed intact on large-tick
  ones. Pre-2009 equal-risk Sharpe about 0.8 (small tick) and 1.4 (large tick); after, about 0
  and 1.0-1.2. Small-tick contracts are mostly equity indices and currencies; large-tick ones
  mostly bonds and commodities. Capacity, electronification and CTA crowding are rejected on
  timing or cross-section. Mechanism: trend trades used to feed their own trend through price
  impact; high-frequency market makers now pull liquidity ahead of predictable flow, which
  breaks the loop where the tick is small.
- Data: about 100 liquid futures, 1995-2025. Horizons tested 5-50 days (EWM up to 50-200);
  **no 6-12-month horizon**, and the text says the small-tick decay is "uniform across signal
  horizons" while slow signals are "approximately intact" in aggregate (not reconciled).
- Out of sample: none formal; the break date is chosen from the data. Survived publication:
  too new.
- Testable keyless: only at the asset-class level (our pooled stock-index, FX, bond and
  commodity series from `pooled-1`/`pooled-2`); we have no futures tick data, and all our ETFs
  are small-tick by their definition. A class split cannot separate tick from class, which the
  paper says matters.
- Closest try: `gap-2002-1` (#162: the insurance's net gain is not shown since 2002) and
  `insure-2`. It would be a **description** of whether stock-index trend lost its edge after
  2009, not a rule.
- F1 pass (structural); F2 pass (the classification is a contract property, fixed in advance;
  volatility enters only the ranking). Power: no pick is possible; as a descriptive split it
  can kill the class-level implication only.

**T2. Sepp and Lucic, "The Science and Practice of Trend-Following Systems", arXiv 2607.19497,
2026-07.** `[abstract]`
- Claim: every trend system's expected return is a kernel-weighted integral of the spectrum of
  volatility-normalised returns ("excess spectral mass at low frequencies"); positive skew of
  aggregated trend returns is structural, peaking near half the filter span; all trend systems
  are strongly correlated. Closed-form Sharpe and cost-optimal span.
- Data: Monte Carlo plus "liquid contracts", no sample stated. No out-of-sample test.
- Testable: yes as a diagnostic (variance ratios of our assets), but that is what
  `trend-where-it-pays` (dead) and `trend-tune` (flat plateau 6-12 months) already did in
  other words. **Overlap; no new mechanism.**
- F2 fail (a transform of the price path). Power: none.

**T3. Valeyre, "Breaking the Trend: How to Avoid Cherry-Picked Signals", arXiv 2504.10914,
2025-04 (v18, 2026-11).** `[abstract]`
- Claim: CTA-average trend returns match the Grebenkov-Serror theoretical Sharpe of a single
  EMA; one EMA suffices; baskets of indicators invite cherry-picking. No numbers in the
  abstract, no out-of-sample design.
- Consistent with `trend-tune` (plateau, `wf-*` dead) and `ensemble-tsmom`. **Confirms, adds
  no mechanism**; not listed in `ideas.md`.

**T4. Etienne, Ohana, Benhamou, Guez, Setrouk and Jacquot, "Revisiting the Structure of Trend
Premia: When Diversification Hides Redundancy", arXiv 2510.23150, 2025-10.** `[abstract]`
- Claim: the medium (125-day) trend layer is nearly a linear mix of short and long layers;
  dropping it improves Sharpe and drawdown efficiency ("barbell"); horizon weights per asset
  by Bayesian optimisation. Same team as Benhamou et al. (covered). No numbers or sample in the
  abstract; out-of-sample not described.
- Closest try: `e4` (1/3/6/12-month ensemble; +0.063 a stock market pooled, #142) and
  `e4-anatomy-1` (#168, merged: the lead is the rebound year plus smaller, smoother positions;
  the 6-month leg alone -0.001). A barbell is an `e4` variant chosen after seeing `e4`'s legs:
  **tuning risk, and the lead is a scale-down (vol dial) per `e4-anatomy-1`.**
- F2 fail. Power: the pooled lead needed is +0.18 against `e4`'s +0.063. Cannot reach.

**T5. Trend's 2024-2025 drawdown, practitioner record.** Korgaonkar (Man Group), "Trend
Following and Drawdowns: Is This Time Different?", 2025-06 `[full text]`; Kaminski and Wen
(AlphaSimplex), "Market Cycles and Managed Futures Drawdowns", 2025-06 `[secondary]`;
Cambridge Associates and trade-press notes `[search summary, unverified]`.
- Facts: SG Trend Index 12-month return -18.6% to 2025-04-30, the worst rolling 12 months in
  its 2000-2025 history (previous worst -16.0%, 2019-01); about -20% from 2024-05 to 2025-05.
  Cause named: policy-driven reversals (tariffs on and off); crowding rejected (flows vs
  performance correlation -0.1). After rolling 12-month losses over 10%, the next 12 months
  averaged +9.8% (Man); recoveries quicker after equity downturns (Kaminski-Wen). A rule that
  goes to cash after a 20% drawdown and re-enters on recovery lost 2.2% a year against staying
  invested (Man, 10,000 simulations).
- Mechanism implied: **"trend after its own drawdown"** (allocate more to trend after it
  lost). Data: the SG index is not keyless (survey-5); a live-fund proxy is (survey-5's
  managed-futures funds, 2010-2025: about 3 such drawdowns). Survived: no post-publication
  record. Closest try: `drawdown-control`, `fast-reentry*` (buy-back rules on the asset, all
  dead); this one acts on the strategy's own record.
- F2 fail (a transform of the strategy's price path). Power: 3-6 episodes in the keyless
  record: kill-only. For our book it changes nothing: `tsmom12` is never switched off, which
  is what Man's simulation favours.
- The 2025 episode is the V-shaped-reversal failure the repo already documents (fast crashes,
  late buy-back; #94, #96, #103). Worth knowing: it sits **inside our train window**, so any
  rule tuned on 2025 learns that one episode.

### (b) Tail hedging and crisis alpha

**H1. Noguer i Alonso and Al Fallouji, "Tail Risk Management with Puts and Trend Following: A
CVaR Framework for Crashes and Drawdowns", arXiv 2607.00883, 2026-07.** `[abstract]`
- Claim: in stylised Monte Carlo, fixed or grid-optimised mixes of a put sleeve and an EWMA
  trend sleeve have lower terminal CVaR than either alone; the best weight depends on the
  calibration. **Simulation only**, no market data.
- Closest tries: `insure-4` (PPUT while `tsmom12` is in: worse than `tsmom12`, z -1.67),
  `insure-3`, `vix-call-1` (#167: best fast-crash cover yet, pays only through 2020). **Covered;
  no new mechanism**, not listed.

**H2. Causley (One River), "Heretical Thinking: The Long Volatility Premium", 2025-10
(practitioner).** `[search summary, unverified]`
- Claim: a beta-neutral long-volatility overlay (puts with their equity delta hedged) improved
  return and cut drawdown over about 40 years. A commentary notes the result depends on how the
  puts' short-equity exposure is attributed and on the benchmark (stocks plus puts against
  stocks alone).
- Against it: survey-6's live tail-hedge composite (TAIL, VIXY, BTAL, SWAN), Sharpe -0.54 over
  2011-2025; MSCI and Man Institute analyses (older) find tail hedges lag simply holding less
  risk. Needs options or shorts (B6/B7) and a delta hedge.
- F1 pass (a premium claim); F2 pass. Power: an uncorrelated overlay on the six assets needs a
  standalone Sharpe near 2.3-2.55 in the difference form (power-map). **Dead (literature and
  live record)**; listed for completeness.

**H3. Research Affiliates, "Should Trend Follow Carry? Lessons from Bonds, Gold, and 2022",
2026-02.** `[secondary: Advisor Perspectives excerpt; page gated]`
- 83 futures and forwards 1989-2025: trend conditioned on carry beat plain trend by 1-2
  tracking errors over the full sample but lagged by about two tracking errors in 2020 and
  2022 (the carry filter forbade shorting bonds early in 2022); a naive carry filter never
  lets trend hold gold or silver. Conclusion: plain trend served crisis-alpha seekers better.
- **Confirms `ts-carry` (dead in survey-4) from outside**; no new line.

### (c) Volatility management

**V1. DeMiguel, Martin-Utrera and Uppal, "A Multifactor Perspective on Volatility-Managed
Portfolios", Journal of Finance 79(6), 2024, pp. 3859-3891, DOI 10.1111/jofi.13395 (open
access).** `[first pages of the published PDF]`
- Claim: a conditional mean-variance portfolio of nine equity factors whose weights fall with
  **market** volatility, and whose relative weights across factors are allowed to change with
  it, beats the unconditional multifactor portfolio **out of sample and net of costs**: Sharpe
  13% higher, significant at 1%. Three drivers: trading diversification (netting trades across
  factors; without it, four of nine managed factors have negative net mean), optimising with
  costs, and factor-specific timing (more value, momentum and betting-against-beta on average,
  less investment). Factor risk prices fall as market volatility rises. Answers Cederburg et
  al. and Barroso-Detzel (both covered: single-factor vol management fails out of sample and
  after costs).
- Data: US factors, 1977-01 .. 2020-12 (CRSP/Compustat-built, including HXZ ROE and IA).
- Out of sample: rolling estimation inside 1977-2020. Survived publication: only 2021-2025 is
  after the sample (5 years). **Pre-sample 1927-1976 is untouched by the paper** for the
  factors the Ken French library has back then (Mkt, SMB, HML, UMD).
- Testable keyless: partly. Ken French daily market (for market volatility) and monthly
  HML/UMD from 1926-27 are keyless (used by survey-6, `xs-century-1`). The paper's
  netting-of-trades cost saving needs stock-level holdings (not keyless), so a keyless test can
  only charge sleeve-level costs, which is harsher than the paper.
- Closest try: `xs-century-1` (#170: the unmanaged style book) and the own-vol line
  (`own-vol-target`, `own_vol_70`, `ownvol-anatomy-1` #172, still open). **Disguise risk high**: it is
  volatility sizing; the honest twin is each sleeve scaled by its own volatility (Moreira-Muir),
  and the paper's specific claim is that market-volatility conditioning with factor-specific
  slopes beats that.
- F1 pass (a risk-premium timing claim). F2 **pass with controls**: the dose is the market's
  volatility, not the sleeve's own price; control = the sleeve's own-vol twin. Power: **the only
  item that can reach the bar**, and only through `xs-century-1`'s book in the alpha form
  (needed IR 0.51-0.60 on about 97 years; the unmanaged book has IR +0.51 (z 4.44) at the cheaper cost
  (`results/xs-century-1.md`, R2); +13% of Sharpe would put it near 0.58, though carrying a
  +13% gain in a mean-variance portfolio's Sharpe over to an alpha-form IR against `tsmom12`
  is a loose analogy). Shorts are parked (B7), so any result is
  informational.

**V2. Reschenhofer and Zechner, "Volatility Managed Multi-Factor Portfolios", Journal of
Investment Management 23(3), 2025, pp. 72-106 (SSRN 4005163, 2022); with Neuhierl and Randl,
"Timing the Factor Zoo", working paper (AFA/AEA 2024).** `[search summary, unverified; JOIM
paywalled]`
- Claim: across 318 factors and 39 timing signals, past factor returns and factor volatility
  are the best single predictors; partial least squares over all signals dominates; median
  gain from timing a factor about 2% a year; a timed multifactor portfolio 8.6% a year above
  its naive timing (an earlier draft said 20%). Joint use of factor volatility and
  option-implied market volatility helps. Out of sample: "qualitatively similar" with all
  parameters estimated out of sample (the volatility paper); not checked for the zoo paper.
- Testable keyless: the Chen-Zimmermann open-source anomaly portfolios are public, but timing
  318 factors with 39 signals is a search the bar charges for. On `xs-century-1`'s four
  sleeves it reduces to factor momentum plus factor volatility.
- F2 **fail** for the factor-momentum part (the dose is the factor's own past return); the
  volatility part is V1 again. Power: on four sleeves the zoo's breadth is gone. Listed
  `factor-zoo-timing`, parked.

**V3. Xu, "Beyond Volatility Timing: The Hidden Power of Target Timing in Portfolio
Management", Journal of Portfolio Management 52(4), 2026, DOI 10.3905/jpm.2025.1.804.**
`[abstract via search summary; EBSCO page returned 403; author from one database record,
unconfirmed]`
- Claim: volatility-managed factor portfolios underperform partly because the volatility
  target, calibrated as in earlier studies, rises with factor volatility in real time, so
  exposure is not cut enough in factor crashes ("negative target timing"); a scheme with a
  positive target-timing effect improves on it. No numbers seen.
- Closest try: `own_vol_70`, `vol-target`, `risk-map`. **A volatility dial in disguise by
  construction.** F2 fail. Power: own-vol 70% leads `tsmom12` by +0.022 a market pooled (#142)
  against +0.18 needed. Listed `vol-target-timing`, dead on power.

**V4. Bongaerts, Kang and van Dijk, "Conditional Volatility Targeting", Financial Analysts
Journal 76(4), 2020, pp. 54-71.** `[abstract]` (older than 2024, but cited by the 2024-2026
work above and absent from our surveys)
- Claim: plain volatility targeting does not reliably help in global equity markets and can
  deepen drawdowns; adjusting exposure only in extreme high- and low-volatility states improves
  Sharpe and cuts drawdowns in major equity markets and momentum factors, with low turnover.
- Testable keyless: yes (pooled 41 markets). Closest try: `vol-calm` (baseline, worse than
  equal weight), `vol-shift` (new), `own-vol-target`. **Vol dial in disguise.** F2 fail.
  Power: as V3. Listed `vol-target-extremes`, dead on power.

### (d) Signal blending

No 2024-2026 paper on blending time-series signals (trend, carry, value) with an
out-of-sample record turned up beyond T4 (horizon blending) and H3 (trend filtered by carry).
The integrate-versus-mix literature (Fitzgibbons et al. 2017 and successors) is long-only
cross-sectional stock selection and does not apply to six assets. V1 is the one strong 2024
result whose gain comes from combining (trading diversification across factors), and it needs
stock-level trades to reproduce. **Nothing new listed.**

### (e) Replication and decay of anomalies

These update priors; they are not mechanisms.

**D1. Chen, Lopez-Lira and Zimmermann, "Does Peer-Reviewed Research Help Predict Stock
Returns?", arXiv 2212.10317 (v6, 2025-12).** `[search summary of abstract and NBER slides
2024]` Mining 29,000 accounting ratios for t > 2 gives cross-sectional predictability similar
to published research; about 50% survives after the original samples for both (published 53%,
mined 51%); mined signals reproduce the published decay pattern; risk-based predictors do
*worse* than mined benchmarks.

**D2. Chen and Welch, "What Useful Alphas?", arXiv 2607.06502, 2026-07.** `[abstract]` About
200 published long-short anomalies (Chen-Zimmermann data): median monthly return 48 bp to
2005, 19 bp after; on non-micro stocks 26 bp full period, **7 bp after 2005**, which modest
allowances for luck or costs remove.

**D3. Goncalves, Loudis and Ogden, "Out-of-Sample Alphas Post-Publication", working paper
2025-02 (AEA 2025).** `[search summary, unverified]` 177 anomalies: with maximum-Sharpe
weights estimated on pre-publication data, the post-publication alpha is about zero, also when
expected decay is built into the weights; the paper itself finds that combining many
anomalies with shrinkage still keeps a positive out-of-sample alpha.

**D4. Bowles, Reed, Ringgenberg and Thornock, "Anomaly Time", Journal of Finance 79(5), 2024,
pp. 3543-3579, DOI 10.1111/jofi.13372.** `[abstract]` Anomaly returns concentrate in the first
month after the underlying accounting information is released and decay soon after; June
rebalancing understates them; decay is faster as information processing speeds up. A stock
selection mechanism (`anomaly-time`): needs firm-level release dates and fundamentals, parked.

**D5. Cakici, Fieberg, Metko and Zaremba, "Do Anomalies Really Predict Market Returns? New Data
and New Evidence", Review of Finance 28(1), 2024, pp. 1-44.** `[abstract via RePEc]` 42
countries, up to 153 anomaly portfolios, 1990-2021, machine learning: **no robust market
predictability**; the US result rests on a few anomalies and on method choices. This kills the
2022 claim (Dong, Li, Rapach and Zhou, Journal of Finance 2022) that long-short anomaly
returns time the market: listed `anomaly-market-timing`, dead (literature).

**D6. "Lost in the Multiverse: Methodological Uncertainty in Studying Global Equity Returns",
Journal of Banking and Finance 190 (2026 per search; authors not confirmed).** `[search
summary, unverified]` 15 cross-country predictors, up to 13,824 implementations, out-of-sample
design selection: few cross-country premia are robust; developed-only samples show almost none;
small segmented markets strengthen results, liquid investable ones weaken them.

**What D1-D6 change here.** survey-6 used "published effects kept a median 28% (6 factors),
8% across families" live; D1 says 50% survives post-sample on paper, D2-D3 say near zero for
investable, out-of-sample-weighted portfolios after 2005. The gap is the investable filter and
the estimation of weights: **the paper-to-live haircut for anything we would actually trade
should stay at the pessimistic end (0-30% kept)**. D6 is a warning for pooled 13-market tests
of cross-country *premia* (not of `tsmom12`, which is a time-series rule applied per market).

## Sites that blocked or gated scripts

EBSCO (403), open.icm.edu.pl (403), Advisor Perspectives (membership gate), JOIM and FAJ
(paywall). The Journal of Finance PDF of V1 was opened from the LBS repository (open access).
SSRN was not opened directly (earlier surveys record 403); arXiv abstracts and one HTML full
text were readable. A second pass through a browser could read the JPM abstract (V3), the RA
piece (H3) and the JBF paper (D6); none of them would change a verdict.

## Scoreboard (new mechanisms only)

| # | Mechanism (`ideas.md` name) | Source | F1 | F2 | Closest try (disguise) | Keyless test | Can it reach the bar? | Verdict |
|---|---|---|---|---|---|---|---|---|
| 1 | `vm-style-book` | V1 (JF 2024), V2 | pass (premium timing) | pass with controls (market vol; control = own-vol twin) | `xs-century-1`, own-vol line (high: vol sizing) | partly: Ken French 1926-, sleeve-level costs only | **yes, just**: alpha form on ~97 years, needs IR 0.51-0.60; unmanaged book +0.51, z 4.44 (#170 R2) | **top 1** (informational: B7) |
| 2 | `tick-tier-trend` | T1 (arXiv 2026) | pass | pass | `gap-2002-1`, `insure-2` | class level only (pooled series) | no pick possible; descriptive, kill-only | **top 2** (descriptive) |
| 3 | `factor-zoo-timing` | V2 | pass | fail (factor momentum) | `xs-century-1`, `ensemble-tsmom` | yes (open anomaly data) but a 39 x 318 search | no on four sleeves | parked |
| 4 | `vol-target-timing` | V3 (JPM 2026) | pass | fail | `own_vol_70` (vol dial by construction) | yes | no (+0.022 seen, +0.18 needed pooled) | dead on power |
| 5 | `vol-target-extremes` | V4 (FAJ 2020) | pass | fail | `vol-calm`, `vol-shift`, own-vol | yes | no | dead on power |
| 6 | `trend-barbell` | T4 (arXiv 2025) | pass | fail | `e4`, `e4-anatomy-1` (tuning; scale-down) | yes | no (+0.063 seen, +0.18 needed) | dead on power |
| 7 | `trend-after-drawdown` | T5 (Man, AlphaSimplex 2025) | pass | fail | `drawdown-control`, `fast-reentry*` | live funds 2010-2025, ~3 episodes | no (kill-only) | parked |
| 8 | `spectral-trend` | T2 (arXiv 2026) | pass | fail | `trend-where-it-pays`, `trend-tune` | yes | no | dead (overlap) |
| 9 | `long-vol-premium` | H2 (practitioner 2025) | pass | pass | survey-6 tail funds, `vix-call-1`, `insure-4` | needs options/shorts (B6/B7) | no (standalone Sharpe ~2.3 needed) | dead (literature, live record) |
| 10 | `anomaly-market-timing` | D5 vs Dong et al. 2022 | pass | pass with controls | none | yes (open anomaly data) | no (single timing signal, C1/C4) | dead (literature) |
| 11 | `anomaly-time` | D4 (JF 2024) | pass (slow diffusion of released information, not a scheduled flow) | pass | none (stock selection) | no (firm-level dates and fundamentals) | not applicable to the six | parked |

Not listed (confirm earlier verdicts, no new mechanism): T3 single EMA (confirms
`trend-tune`), H1 put-plus-trend CVaR (covered by `insure-4`, `vix-call-1`), H3 trend filtered
by carry (confirms `ts-carry` dead), D1-D3 and D6 (priors).

**Count.** `SUMMARY.md` (night 4): 88 mechanisms listed, 19 tested by a strategy, 22 gates,
none passed. This lane adds **11 listed, 0 tested, 0 gates** (99 if nothing else lands
tonight; other lanes add their own, the lead unions). Project-wide bar unchanged: N_eff 500,
z >= 4.70 (`BAR.md`).

## Top 2 for a future lane (card sketches; not cards, nothing was run)

### 1. `vm-style-book`: does market-volatility conditioning of the century style book add to `tsmom12`?

- **Why this one.** It is the only new item whose plausible effect lands in the range where
  the bar can be cleared (power-map C2, alpha form), it has a published out-of-sample and
  net-of-cost claim (V1), and it leaves a 49-year pre-sample (1927-1976) the paper never saw.
- **Hypothesis.** `xs-century-1`'s book with each sleeve's weight conditioned on lagged market
  variance adds to `tsmom12` (alpha form) beyond the unmanaged book, net of costs.
- **Data.** `xs-century-1`'s sleeves and code unchanged (HML, UMD, 10 government bonds, 9
  currencies, rank-weighted, 10% vol per sleeve, equal weight per class); market variance =
  sum of squared daily Ken French Mkt returns over the previous month (keyless). Train only,
  nothing after 2025-10-31.
- **Rule (fixed before any number).** V1's construction in the simplest form: the asset set is
  augmented with managed copies f_k * (c / sigma^2_mkt,t-1) (c makes the managed copy's
  full-sample variance equal the original's, estimated on the expanding window only);
  mean-variance weights on the 2K sleeves from an expanding window (first 20 years burn-in),
  shrunk to equal risk by a fixed 50%, refitted each January; no other parameter.
- **Twins (disguise checks, fixed).** (i) the unmanaged book (`xs-century-1`); (ii) each sleeve
  scaled by its own lagged variance (Moreira-Muir); (iii) the whole book scaled by market
  variance with one slope. If (ii) or (iii) does as well, the gain is volatility sizing, not
  V1's mechanism.
- **Tests.** Primary: alpha-form t against `tsmom12` over 1948-2025 (after burn-in), at
  `xs-century-1`'s two cost levels plus each managed sleeve's own turnover cost. Secondary
  (descriptive): conditional minus unmanaged IR in 1948-1976 (pre-sample), 1977-2020 (the
  paper's), 2021-2025 (post).
- **Pass / kill.** Pass: alpha-form z >= 4.70 at the main cost **and** beats twins (ii) and
  (iii) by z >= 2 **and** conditional minus unmanaged > 0 in the pre-sample. Kill: conditional
  minus unmanaged IR <= 0 in 1948-1976, or the main-cost alpha-form z falls below
  `xs-century-1`'s.
- **Count.** A new family member selected after `xs-century-1`'s near miss: state that on the
  card, count it, and treat a pass as informational while shorts stay parked (B7).

### 2. `tick-tier-trend`: did trend on equity indices and currencies lose its edge after 2009 while bonds and commodities kept it?

- **Why this one.** T1 is the first 2024-2026 explanation of the post-2008 decline of trend
  that survives the obvious alternatives and predicts *where* it happened. Our book holds
  small-tick instruments (stock ETFs, coins); if the class-level prediction holds at the
  12-month horizon, the "insurance at a price" framing (#162) should expect a worse price
  from now on in stocks than in bonds and gold. Passes both filters; cheap (re-scores
  committed series).
- **Kind.** Descriptive, kill-only (no pick, no comparator change); a `note` row.
- **Data.** `pooled-1`/`pooled-2`'s committed per-market weekly series of `tsmom12` and buy and
  hold: stock indices and currencies (predicted small-tick) against government bonds and
  commodities (predicted large-tick); no new download.
- **Rule.** Statistic = difference in differences of (`tsmom12` Sharpe minus holding's Sharpe):
  [small-tick classes, 2009-2025 minus 1995-2008] minus [large-tick classes, same]; also for
  the 1- and 3-month legs of `e4` (closer to T1's horizons). SE by 52-week block bootstrap,
  markets resampled within class, fixed seed. Break date 2009-01 from the paper, not ours.
- **Reading.** Consistent if the statistic < 0 at z <= -2 for the short legs; killed at the
  class level if >= 0. Either way it cannot separate tick from class (T1 says class alone does
  not reproduce the split): written down before any number.

## Checks

Docs only. `uv sync && uv run ruff check . && uv run ruff format --check . && uv run mypy &&
uv run pytest` run before marking ready (see the PR).

## Sources (opened 2026-11-24, UTC)

- T1 <https://arxiv.org/abs/2607.01550>, <https://arxiv.org/html/2607.01550v1>
- T2 <https://arxiv.org/abs/2607.19497>
- T3 <https://arxiv.org/abs/2504.10914>
- T4 <https://arxiv.org/abs/2510.23150>
- T5 <https://www.man.com/insights/is-this-time-different>;
  <https://theideafarm.com/alternative-investment/trend-following/market-cycles-and-managed-futures-drawdowns/>;
  <https://www.cambridgeassociates.com/insight/does-trend-followings-recent-struggle-signal-that-the-strategy-is-structurally-broken/>
- H1 <https://arxiv.org/abs/2607.00883>
- H2 <https://alphaarchitect.com/the-long-volatility-premium-short-the-market-get-paid/>;
  <https://philippdubach.com/posts/long-volatility-premium/>
- H3 <https://www.researchaffiliates.com/content/dam/ra/publications/pdf/1107-should-trend-follow-carry-lessons-from-bonds-gold-and-2022.pdf>
  (not opened), <https://www.advisorperspectives.com/commentaries/2026/02/26/trend-follow-carry-lessons-bonds-gold-2022>
- V1 <https://ideas.repec.org/a/bla/jfinan/v79y2024i6p3859-3891.html>,
  <https://lbsresearch.london.edu/id/eprint/3716>
- V2 <https://joim.com/article/volatility-managed-multi-factor-portfolios>,
  <https://www.cxoadvisory.com/volatility-effects/comprehensive-equity-factor-timing/>
- V3 <https://www.ebsco.com/articles/business-and-management/8966f5b2-3315-56ea-b43c-c4992b13253a/beyond-volatility-timing-the-hidden-power-of-target-timing-in-portfolio-management> (403)
- V4 <https://ideas.repec.org/a/taf/ufajxx/v76y2020i4p54-71.html>
- D1 <https://arxiv.org/abs/2212.10317>
- D2 <https://arxiv.org/abs/2607.06502>
- D3 <https://finance-conference.wpcarey.asu.edu/sites/default/files/2025-02/Out-of-Sample_Alphas_%282025-02-12%29_with_link.pdf> (not opened)
- D4 <https://jacobslevycenter.wharton.upenn.edu/wp-content/uploads/2019/09/Anomaly-Time.pdf> (working paper; JF record via search)
- D5 <https://ideas.repec.org/a/oup/revfin/v28y2024i1p1-44..html>
- D6 <https://osuva.uwasa.fi/handle/11111/21104>
