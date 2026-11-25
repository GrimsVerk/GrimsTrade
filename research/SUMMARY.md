# Research summary (2026-11-25, night 5)

The live rule is `tsmom12`: hold an asset only while its price is above where it was a year ago,
otherwise cash. "Sharpe" below means return per unit of risk (higher is better). Agents now merge
and run this repo; 8 pull requests are open (listed under "Still open").

## What we know now

- **The rule is crash insurance, not an edge.** It earns about what simply holding the same six
  assets earns (2010-2025: Sharpe 1.11 each, #74, #78). What it adds is smaller losses in long
  bear markets.
- **The insurance is real, and holds everywhere we looked.** The evidence is timing: it avoided
  0.50 of each fall, against 0.27 for the same exposure at random dates (#87). In 21 US market
  falls of 25% or more since 1927 it lost less than holding in 20 (50 episodes when industry-only
  falls are added, 37 under strict grouping). In 13 other developed markets since 1966: 17 of 18,
  not independent of the US falls (#90). It is cheaper than simply holding less in direction in
  every era and market, but statistically shown only for 1927-1961 and the developed-market
  price indices; since 2002 not shown (p 0.19). On the S&P 500 since 1986 it was far cheaper
  insurance than buying puts (#160).
- **But it has a price.** It buys back late, so the year after the low hands most of the gain
  back, and it trails holding in calm markets too, by about 2 points a year. Since 2002 the fall gain and the late buy-back about cancelled, so the calm drag is most of the cost: it left it about 1 point of
  growth a year behind holding on the broad US index (S&P 500 total return 0.7 with idle cash
  at bills, 1.0 with cash at 0; the French US market 1.1-1.4) and about 2 on single industries
  (mean of 10: 1.6-2.0; from about 1 ahead to 4 behind by industry) (#162). It fails in fast
  crashes of three months or less (1987, 2020). Faster buy-back rules did not fix this: early rallies look
  just like the bottom (#94, #96, #103).
- **Fast-crash cover can be bought, but it has not paid.** Puts while trend is in cost about 2.9
  points of growth a year against `tsmom12` (#165). VIX calls are the best cover tested for the
  falls trend misses (21.9 log points avoided per fall, against trend's 6.9), but over 2006-2025
  they were a net cost even with 2020 (Sharpe d -0.09 against `tsmom12`); 2020 is the only fall
  that comes near paying for them, and without it they cost about 4 points of growth a year
  (d -0.31, z -2.32) (#167). Buying them is a bet on the next fast crash from a calm level.
- **`e4`'s lead is a faster buy-back** (#168, descriptive). `e4` (an ensemble of 1/3/6/12-month
  signals) leads `tsmom12` mostly in the year after a market's low, where its faster legs buy
  back earlier (+0.092 Sharpe a stock market by the card's split; positive on all 39 stock
  markets with a 25% fall). Post hoc, against a `tsmom12` scaled to `e4`'s volatility, it gives
  part of that back in slow bear markets (it buys bear-market rallies) and in calm dips; fast
  crashes add little. Its smaller lead outside stocks is, by the card's rule, the risk part
  (part positions cut volatility, worth more where `tsmom12` earns more per unit of risk), not
  regime mix. This describes the known lead, it is not a test: `e4` stays "unsettled, leaning
  positive" (pooled +0.045, z 1.43; on bonds and currencies +0.010, z 0.33; #159).
- **Gaining in a crash needs shorts (bets on falls) across many markets.** That is how real
  trend funds gain in crashes (#83). Added to `tsmom12` without leverage, such a book gained in
  2008, 2020 and 2022, but cut Sharpe from 1.21 to 0.97 (#89). A risk choice, not an edge; the
  paper broker holds no shorts for now (answer B7).
- **Sizing by recent swings is the best-looking risk dial, but not a proven edge.** Re-run with
  no look-ahead, own-vol targeting kept Sharpe 0.97 (24% average share) and 1.04 (66%) against
  `tsmom12`'s 0.94 over 1994-2025. A lead of +0.03 to +0.10 is about one paired standard error
  (about 0.1) or less: noise (#110). Pooled over 41 other stock markets its 70% form leads by
  +0.022 a market, not shown (#142); on bonds and currencies it is -0.010 and killed: "equity-only
  at best" (#159). Where the lead comes from (#172, descriptive): not holding less and not the
  leverage effect, but risk removal. On stocks the sleeve earns about the same in volatile as in
  calm spells at twice the variance, so cutting then removes risk, not return (risk channel
  +0.024 a market); it gains in falls `tsmom12` is still in and pays some back in rebounds and
  calm markets. On the commodity currencies, whose trends pay while volatile, it loses (-0.123 a
  market, through the mean channel). It now trades as a paper book, `own_vol_70` (#135).
- **A broader `tsmom12` book is worse because the added markets trend poorly here, not because
  they co-move** (#143, #180, descriptive). The 29 added ETFs score 0.29 as a trend book against
  the six's 1.19; at their correlation with the six (0.38) they would need about 0.45 to help,
  so the best weight on them is zero. About two thirds of the fall at 35 assets is the coin
  share shrinking, one third the ETFs. Weighting by inverse volatility makes it worse.
- **Live funds agree: no family beat its plain index after fees.** 15 strategy families, 60
  real funds. The published effects kept about a quarter of their paper Sharpe after
  publication (median about 28% over six factors), and long-only funds built on them matched
  their index after fees (#91). Our own tests of published effects: 0 for 9 (tonight's two:
  the aviation-disaster mood effect #176, market-volatility management of style factors #179).
- **The bar for a new rule is measured, and rebuilds on any computer.** 4,095 tries logged
  (240 new since night 4), worth between 11 and 506 independent shots depending on how they are
  counted; the bar uses the cautious 506. A new rule must beat `tsmom12` at z >= 4.70, which is
  +0.31 to +0.56 Sharpe for rules correlated 0.77-0.93 with `tsmom12` (others use the z column
  in `BAR.md`) (#92, #100). The growth did not move it (night 4: 3,855 tries, N_eff 500,
  z 4.70). The weekly returns behind it are committed, so `BAR.md` regenerates from a clean
  checkout (#108, #111); the store keeps one series per live code version (#158, #166). The
  closest results stay below it: `halving-alone` +0.23 (z about 3.2-3.6, #137), about at the
  3.25 the bar would be if tries were counted by clusters, the coin rebalance band (z 2.76,
  #145) and the century long-short style book in alpha form (z 2.75, #170). Re-scored in alpha
  form, none of 341 stored series reaches the bar; the 2 above 3.29 are known artefacts (#154).
- **The bar is out of reach for every class we can test, and the one exception failed on
  costs** (#150, #170). With edges of the size the records show, no strategy class we can test
  has a realistic chance to clear the bar. Power depends on years of data, not on bar
  frequency. Forward paper scoring cannot confirm an edge: +0.10 over `tsmom12` by a book
  correlated 0.95 with it needs 72 years of record at 80% power even when registered alone
  (356 at the bar). The only case where a pass was not absurd, a long-short style book (value,
  momentum and carry in US stocks, 10 bond and 9 currency markets) on 97 years scored in alpha
  form against `tsmom12`, is now tested and comes closest: large gross edge in-sample (z 7.4, on
  the data HML and UMD were found on, so gross rows cannot decide); net of published trading
  costs it fails the bar (z 2.75, IR +0.31; momentum's cost decides). Since 1994 its alpha is
  insignificant (z 0.75), negative in the 2010s. Managing it by market volatility does not help
  (#179). It needs shorts in any case (B7).
- **Borrowed ideas: 95 mechanisms listed, 23 tested by a strategy, 25 gates, none passed** (many
  gates can only kill an idea, never pass one, by design: few independent episodes; #124).
  Tonight's wide-17 to wide-20 added 7 (#169, #171, #173, #176). New candidates must pass two
  filters first: not announced, not driven by price (#109). A literature survey listed 11 more
  from 2024-2026, none tested by it (#177).

## Tonight's verdicts (night 5)

- Century long-short style book against `tsmom12` in alpha form (#170): **fail.** Large gross
  edge in-sample (IR +0.88, z 7.4); net fails the bar (z 2.75 against 4.70). Even the cheaper
  published momentum cost stops at z 4.44 (a robustness row, which cannot turn a fail into a
  pass). What survives costs is bond carry, FX value and carry, and HML. A diversifier at best
  (mix gain +0.08 Sharpe in-sample, net), not an edge at the bar. Informational: needs shorts.
- Market-volatility management of that book (DeMiguel, Martin-Utrera and Uppal 2024; #179):
  **dead.** Out of the paper's window z 1.58 (full sample 2.40), below the unmanaged book's
  2.46 on the same months (kill K2). The paper's gain shows only inside its own 1977-2020
  window. Diagnostic after the run: before 1977 the fitted timing weight is 0 in every month,
  so there the managed book is the unmanaged one (the method found nothing to time, rather
  than timing and failing), and 1967-1976 was the paper's first estimation window.
- A VIX-call overlay on `tsmom12` (#167): **dead.** Best fast-crash cover tested, but a net
  cost even with 2020 (23 log points behind trend, d -0.09, z -0.42); without 2020 d -0.31
  (z -2.32). Both forms "rest on one crash" (kill 4).
- Hedge (multiplicative weights) across 16 existing books (#175): **killed.** 1.128 against
  `tsmom12`'s 1.052 (z +1.23) and behind the plain equal split of the same books (1.158,
  z -1.87). The regret guarantee is vacuous at 32 years, the textbook rate barely learns, and
  what it learns (weight towards the highest-swing books) costs Sharpe. Hedge between
  `tsmom12` and `own_vol_70` alone stays at 50/50 to 52/48: the equal split of the two. Post
  hoc, not a pick: the equal split's +0.106 (z 1.78) is flattered by three books chosen on
  this window.
- Where `e4`'s lead comes from (#168) and where own-vol's lead or loss comes from (#172), both
  descriptive re-scores: see "What we know now". Neither moves the verdicts on `e4` or own-vol.
- Why breadth lowers Sharpe (#180, descriptive): the added markets' low trend Sharpe, plus coin
  dilution; see "What we know now".
- Physics, signal processing and control ideas (#169): of 13 candidates 11 were already tested
  in other words; the two tested **fail**: `vclock12` (trend in variance time) -0.167
  (z -2.18), `huber52` (a robust trend estimate) -0.001 (z -0.01).
- Meteorology, actuarial and operations-research ideas (#173): two credibility rules **fail**:
  `cred-xs` +0.047 (z 0.95; its credibility factor came out 0, so it became a book-level
  switch), `cred-lr` -0.097 (z -1.06). One new descriptive idea, `rev-costloss` (now #182).
- Biology, ecology, epidemiology and climate (#171): two premium gates **fail**, temperature
  and disease-outbreak news (each rank 9 of 41 placebos, t +1.63 and +1.68). In both the
  reaction had the same sign as the forward return: a regime coincidence, not a premium.
- Economic history, psychology and sociology (#176): the aviation-disaster mood gate **fails**
  (t -0.59, rank 10 of 41; no reversal); a published effect not found post-sample.
- 2024-2026 literature (#177): 11 new mechanisms listed, none tested by the survey. Its top 1,
  `vm-style-book`, failed tonight (#179); its top 2, the post-2009 trend break by asset class,
  is #181 (open).
- Data (#174): keyless monthly consumer prices for 11 economies (from 1913-1954; annual back to
  1661 for one), country equity yields from 1975 and policy rates from 1946-1960. A real
  exchange rate can now replace the spot-reversal proxy for currency value (own card needed).
- Engineering (#166): the register stores the current live code versions (12 live series) and
  falls back to a series with the same code hash; the bar was regenerated (3,982 tries, N_eff
  504, z 4.70, before tonight's research lanes merged).

Also landed between the night-4 summary and tonight: the alpha-form re-score (#154, above), the
keyless long histories for rates, FX and commodities (#152), letting coin slots drift on about
90 other coins (#157: **not confirmed**, +0.033 net, z 1.80 against a bar of 2; the gain is
fewer trades, not drift), the register fixes (#158), `e4` and own-vol on non-equity markets
(#159), trend against puts (#160) and puts while trend is in (#165: worse than `tsmom12`,
z -1.67).

## Still open or running

- Held until after the 2026-11-25 daily run: one replay engine for the gym and the learning
  environment (#149), the daily run reconciling its own record (#153), the scoreboard's
  live-start-delay note (#155), daily-run robustness tests for misbehaving sources (#161).
- Tonight's lanes still open: why `e4` gains after the low when faster re-entry rules did not
  (#178), the post-2009 trend break by asset class (#181), the `tsmom12` exit scored as a crash
  warning by relative economic value (#182, draft), this summary (#183).
- Leads still open: `e4` (unsettled, leaning positive, from stocks; #159, #168); the halving
  window's one forward score (#137). `coin-drift-run` is closed: not confirmed (#157).
- Live: 11 books trade fake money daily; `own_vol_70` joins on its first run (#135). The record
  is days old: description only.

## Decisions

The owner ruled on 2026-11-24 that agents merge and run this repo. Every open question got its
recommended default as an agent call: see "Answers" in [`owner-decisions.md`](owner-decisions.md)
(for example: `tsmom12` is a risk choice, not an edge; no shorts or perpetual futures for now;
the three presets plus one own-vol 70% paper book). Any answer can be reversed by a later PR that
says why. The risk level stays a preference: [`risk-menu.md`](risk-menu.md) (#101, #105, #110)
is one "if you care most about X, pick Y" table. Example (2007-2025, no look-ahead): own-vol
target aimed at 70% held 61% on average, grew 13.8% a year with a worst loss of 15.7%, against
17.6% and 24.6% for a fixed 70%; holding the six grew most (27% a year) with a 47% worst loss.
None of the rows is a proven edge.

## Where to read more

- Crash insurance: #87, #90 (`research/insure-2.md`); its gap to holding per series since 2002:
  #162 (`research/gap-2002-1.md`); buy-back: #94, #96, #103; puts and VIX calls: #160, #165,
  #167 (`insure-3.md`, `insure-4.md`, `vix-call-1.md`).
- Risk levels: #101, #105, #110 (`research/risk-menu.md`); own-vol paper book: #135.
- Is the edge real? #74 (`research/dsr-1.md`), #78; live funds #91 (`research/survey-6.md`).
- The bar: #92, #100, #108, #111 (`research/register/BAR.md`); what could reach it: #150, #170.
- Tonight: `research/xs-century-1.md`, `vm-style-1.md`, `vix-call-1.md`, `hedge-books-1.md`,
  `e4-anatomy-1.md`, `ownvol-anatomy-1.md`, `breadth-anatomy-1.md`, `wide-17.md` to
  `wide-20.md`, `survey-7b.md`, `data-long-4.md`.
- Shorts: #83, #89. Coins: #69, #82. Euro books: #59, #62, #63, #68, #73, #77, #80, #85.
- Corrections after the independent review (#119): [`errata-2.md`](errata-2.md).
- Earlier runs (machine learning, macro, carry, papers): [`README.md`](README.md) and this
  file's git history.
