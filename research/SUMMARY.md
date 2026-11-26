# Research summary (2026-11-25/26, night 6)

The live rule is `tsmom12`: hold an asset only while its price is above where it was a year ago,
otherwise cash. "Sharpe" below means return per unit of risk (higher is better). Agents now merge
and run this repo; open pull requests are listed under "Still open".

## What we know now

- **The rule is crash insurance, not an edge.** It earns about what simply holding the same six
  assets earns (2010-2025: Sharpe 1.11 each, #74, #78). What it adds is smaller losses in long
  bear markets.
- **On stocks the insurance is real, and since 1927 the evidence is timing; on older stock data the timing is not shown.** It avoided
  0.50 of each fall, against 0.27 for the same exposure at random dates (#87). In 21 US market
  falls of 25% or more since 1927 it lost less than holding in 20 (20 of 20 not tied; 1933, held
  throughout, is a tie; 50 episodes when industry-only falls are added, 37 under strict
  grouping). In 13 other developed markets since 1966: 17 of 19 effective falls (17 of 17 not
  tied; 2 ties where the rule held throughout, Hong Kong 1989 and Japan 2024; ties counted as
  ties since #218), not independent of the US falls (#90). It is cheaper than simply holding less
  in direction in every era and market, but statistically shown only for 1927-1961 and the
  developed-market price indices; since 2002 not shown (p 0.19). Out of sample on annual data
  for 1870-1965 it holds in slow falls only (#186); its timing statistic is consistent with the
  early annual data's autocorrelation, so the timing part there is not shown (#192). That
  autocorrelation is not documented averaging, and post hoc about half to two thirds of it is
  common across countries; its origin is open, so before 1966 any pooled timing test needs a
  null that keeps the autocorrelation (#204). Independent monthly UK data for 1709-1866 agree
  on the count (7 of 7), with the same autocorrelation caveat as the annual JST data (#212).
  The annual JST timing rests on last year's return: a year-older signal removes it (S 0.72 ->
  0.37, p 0.73); averaged prices barely move the 12-month timing on US 1885-1925 (#220).
  **On bonds and floating currencies no timing is shown: where the insurance holds, it is what
  holding less gives.** Norwegian bonds 1823-1984 do not hold (4 of 11 falls of 5%), UK
  consols 1867-1926 are in between (9 of 10; share 0.42 against 0.24 fixed, p_rot 0.069, not
  shown) (#219); JST bonds in 14 countries lost less in 9 of 12 falls of 10%, timing gap below
  the null medians (#225); floating currencies 1791-1970 lost less in 10 of 11 clusters, by
  exposure only (#222). The literature (#216) agrees where it compares with holding (about
  holding's return, smaller worst falls); the century studies score long-short books against
  zero, and Lempérière et al. (2014) is the strongest counter-evidence, with no stale-price
  check. On the S&P 500 since 1986 it was far cheaper
  insurance than buying puts (#160). Scored as a crash warning, the exit has real skill on US
  stocks since 1927 (hit rate 0.49, false-alarm rate 0.21; Peirce score +0.28 against -0.01
  for the same warnings at random dates) and none on gold, bonds or coins (#182).
- **But it has a price.** It buys back late, so the year after the low hands most of the gain
  back, and it trails holding in calm markets too, by about 2 points a year. Since 2002 the fall
  gain and the late buy-back about cancelled, so the calm drag is most of the cost: it left it
  about 1 point of growth a year behind holding on the broad US index (S&P 500 total return 0.7
  with idle cash at bills, 1.0 with cash at 0; the French US market 1.1-1.4) and about 2 on single
  industries (mean of 10: 1.6-2.0; from about 1 ahead to 4 behind by industry) (#162). That calm
  drag is false alarms (partly by construction: calm is defined by hindsight), not a slow buy-back
  after real falls: all of it comes from exits on dips that never became 25% falls, bought back
  higher, where the re-entry costs about twice what the exit saved; trading costs are 0.02-0.05
  points a year (#203, descriptive). On the US market 1927-2001 it is only the premium given up
  while out (8-9% of calm time); on US stocks since 2002 it is mostly one- or two-week whipsaws,
  and bad timing is half to three quarters of it; on bonds and gold it is long time out (TLT 25%,
  GLD 20% of calm time). Per asset, the net of fall gain, buy-back and calm drag (#214,
  descriptive, cash 0): about break-even on the long US stock record (French US market
  1927-2025 -0.10 a year, +0.66 with idle cash at bills), on QQQ positive only because its
  window starts at the 2000 peak (+1.06; since 2002 -1.48); not paid on bonds (TLT -1.48,
  30-year since 1978 -2.12), gold (GLD -2.33) or coins (BTC -3.72, ETH -3.55). The timed
  book's worst drawdown (37.4%, 2018-2020) is a coin drawdown, deeper than the untimed book
  over the same dates (27.1%). As a warning it pays only for someone whose protection costs
  about a tenth to a third of the loss it prevents; on the US market a plain holder sits at the
  top edge of that band, where it is worth about nothing (value +0.06 of a perfect warning; in money -0.01;
  pooled 11 series +0.01 / -0.04; SPY and QQQ +0.17 / +0.20, but -0.05 / +0.05 in money), and the
  largest block of false alarms is the rebound after the low (#182). It fails in fast crashes of
  three months or less (1987, 2020). Faster buy-back rules did not fix this: early rallies look
  just like the bottom (#94, #96, #103; per fall `e4` too, #178).
- **Fast-crash cover can be bought, but it has not paid.** Puts while trend is in cost about 2.9
  points of growth a year against `tsmom12` (#165). VIX calls are the best cover tested for the
  falls trend misses (21.9 log points avoided per fall, against trend's 6.9), but over 2006-2025
  they were a net cost even with 2020 (Sharpe d -0.09 against `tsmom12`); 2020 is the only fall
  that comes near paying for them, and without it they cost about 4 points of growth a year
  (d -0.31, z -2.32) (#167). Buying them is a bet on the next fast crash from a calm level.
- **`e4` is no longer an open lead: its stock-market lead did not carry to independent data**
  (#198). `e4` (an ensemble of 1/3/6/12-month signals) led `tsmom12` by +0.063 Sharpe a market
  on 41 stock markets (#142; with bonds and currencies pooled +0.045, z 1.43, #159). On four
  stock markets before 1927 (US, Britain, Germany, France; 171 market-years that overlap no
  scored series in time) it trails: -0.065 a market (SE 0.041, z -1.59), one-sided upper bound
  +0.002, ahead in 1 of 4. It leans on Germany (without it +0.001) and the test had little power
  (0.26), so it does not show that `e4` is worse; it shows that an edge as large as the
  41-market one is unlikely there. By its card `e4` is now "no evidence of an edge on stocks in
  general". Five Nordic and Irish markets since 1975 (not deciding; their years overlap the 41)
  give +0.067 (z 1.18): the lead may belong to the post-1975 crash calendar, a reading on 4 and
  5 markets, not a finding. Where the old lead came from stays as described (#168, #178): mostly
  the year after a market's low, where the faster legs buy back earlier; per fall that buy-back
  leaks like the old re-entry rules, and its partial exits pay for the bear-market rallies it
  buys and cost in calm markets.
- **Gaining in a crash needs shorts (bets on falls) across many markets.** That is how real
  trend funds gain in crashes (#83). Added to `tsmom12` without leverage, such a book gained in
  2008, 2020 and 2022, but cut Sharpe from 1.21 to 0.97 (#89). A risk choice, not an edge; the
  paper broker holds no shorts for now (answer B7).
- **Sizing by recent swings is the best-looking risk dial, but not a proven edge.** Re-run with
  no look-ahead, own-vol targeting kept Sharpe 0.97 (24% average share) and 1.04 (66%) against
  `tsmom12`'s 0.94 over 1994-2025. A lead of +0.03 to +0.10 is about one paired standard error
  (about 0.1) or less: noise (#110). Pooled over 41 other stock markets its 70% form leads by
  +0.022 a market, not shown (#142); on bonds and currencies it is -0.010 and killed: "equity-only
  at best" (#159). On independent pre-1927 stocks (US, GB, DE, FR; 171 market-years) it trails
  by 0.007 (SE 0.021, upper bound +0.028): not shown, not contradicted; combined with the 41,
  +0.012 (SE 0.013), not distinguishable from zero. The reading stays "equity-only at best,
  unconfirmed", and those data are now spent for own-vol (#231). Where the lead comes from (#172, descriptive): not holding less and not the
  leverage effect, but risk removal. On stocks the sleeve earns about the same in volatile as in
  calm spells at twice the variance, so cutting then removes risk, not return (risk channel
  +0.024 a market); it gains in falls `tsmom12` is still in and pays some back in rebounds and
  calm markets. On the commodity currencies, whose trends pay while volatile, it loses (-0.123 a
  market, through the mean channel). It now trades as a paper book, `own_vol_70` (#135).
- **A broader `tsmom12` book is worse mainly because the added markets trend poorly here**
  (#143, #180, descriptive). The 29 added ETFs score 0.29 as a trend book against the six's
  1.19; at their correlation with the six (0.38) they would need about 0.45 to help, so the best
  weight on them is zero. Co-movement is secondary, not absent: 0.66 with the six in crises, and
  against the four non-coin assets (rho 0.73) both causes count. About two thirds of the fall at
  35 assets is the coin share shrinking, one third the ETFs. Weighting by inverse volatility
  makes it worse.
- **Live funds agree: no family beat its plain index after fees.** 15 strategy families, 60
  real funds. The published effects kept about a quarter of their paper Sharpe after
  publication (median about 28% over six factors), and long-only funds built on them matched
  their index after fees (#91). Our own tests of published effects: 0 for 9 by night 5 (its
  last two: the aviation-disaster mood effect #176, market-volatility management of style
  factors #179). Night 6 adds eight that did not hold up: the industrial-electricity premium
  (Da, Huang and Yun 2017; passed its gate, died in replication, #202), real-rate currency value
  (Asness, Moskowitz and Pedersen 2013; no better than the proxy, #197), the crypto-theft
  channel (Liu and Tsyvinski 2021, Corbet et al. 2020; no effect, #205), the consumption cycle
  (Atanasov, Møller and Priestley 2020, Melone 2022; t -0.57 with a dose known at the time,
  #210), the post-quake drift (Scholtens and Voorhorst 2013, #215), the political-uncertainty
  premium after mid-term cabinet changes (Pastor and Veronesi, in the spirit of Bernhard and
  Leblang 2006; wrong sign, t -1.74, #221; the negative side, fixed in advance, also
  fails on unseen JST years 1921-1959, t -1.27, #229), drought under-reaction in food stocks (Hong, Li
  and Xu 2019, US industry form, t +0.07) and the sport-elimination mood effect (Edmans, Garcia
  and Norli 2007; t -0.95, far from the published fall, #223).
- **The bar for a new rule is measured, and rebuilds on any computer.** 4,492 tries logged
  (366 new since night 5; the register reads every pushed branch, open ones included), worth
  between 11 and 509 independent shots depending on how they are counted; the bar uses the
  cautious 509. A new rule must beat `tsmom12` at z >= 4.70, which is
  +0.31 to +0.56 Sharpe for rules correlated 0.77-0.93 with `tsmom12` (others use the z column
  in `BAR.md`) (#92, #100). The growth did not move it (night 5: 4,126 tries, N_eff 506,
  z 4.70). The weekly returns behind it are committed, so `BAR.md` regenerates from a clean
  checkout (#108, #111); the store keeps one series per live code version (#158, #166). The
  closest results stay below it: `halving-alone` +0.23 (z about 3.2-3.6, #137), about at the
  3.26 the bar would be if tries were counted by clusters, the coin rebalance band (z 2.76,
  #145) and the century long-short style book in alpha form (z 2.75, #170). Re-scored in alpha
  form, none of 341 stored series reaches the bar; the 2 above 3.29 are known artefacts (#154).
- **The bar is out of reach for every class we can test, and the one exception failed on costs**
  (#150, #170). With edges of the size the records show, no strategy class we can test has a
  realistic chance to clear the bar. Power depends on years of data, not on bar frequency.
  Forward paper scoring cannot confirm an edge: +0.10 over `tsmom12` by a book correlated 0.95
  with it needs 72 years of record at 80% power even when registered alone (356 at the bar). The
  only case where a pass was not absurd, a long-short style book (value and momentum in US
  stocks; value, momentum and carry in 10 bond and 9 currency markets) on 97 years scored in
  alpha form against `tsmom12`, is now tested: large gross edge in-sample (z 7.4, on the data
  HML and UMD were found on, so gross rows cannot decide); net of published trading costs it
  fails the bar (z 2.75, IR +0.31; momentum's cost decides). Since 1994 its alpha is
  insignificant (z 0.75), negative in the 2010s. Managing it by market volatility does not help
  (#179), and neither does the published real-rate currency value in place of the proxy (z 2.74,
  #197). It needs shorts in any case (B7).
- **Borrowed ideas: 112 mechanisms counted, 29 tested by a strategy, none passed; 43 gates, three
  kill-only passes, each killed by its own replication** (many gates can only kill an idea,
  never pass one, by design: few independent episodes; #124). The passes: W32
  `drought-inflation` (t -3.71, rank 1 of 41 on TLT 2002-2025; its replication R32 on the
  10-year yield 1962-2002 t -0.19, rank 21; #188) and W36 `grid-load-premium` (t -2.31, rank 1
  of 41 on the US market 1974-2025; R36 on 1926-1955 t -0.32, rank 13; #202) and W45
  `arms-fear` (US gun-check growth, t +3.50, rank 2 of 41 among both earlier-dose calendars and
  IAAFT surrogates, 2008-2023, leaning on few episodes; R45 on 2000-2008 t +0.54, rank 13;
  #230). All three are persistent monthly doses. W32 ranks 1 in every placebo family; W36 would
  have failed a phase-surrogate family (rank 3). Three passes in about 40 first gates is within
  what chance gives (#207), and replication caught all three. Night 6 added W36 with R36 (#202), W37 `hack-drift` (#205), W38
  `consumption-cycle` and W39 `bank-capital-premium` (#210), W40 `quake-drift` (#215), W41
  `cabinet-collapse` (#221), W43 `drought-food-margin` and the first gate of wide-8's W18
  `elimination-mood` (#223), W44 `revision-noise` (#226), W41n (W41's negative side, #229)
  and W45 with R45 (#230); all but W36 and W45 failed at the gate. W42 is unused. Every gate is
  listed in [`gate-null.md`](gate-null.md). A
  mechanism enters the count once it gets a gate or a strategy test; descriptive re-scores and
  listed-only ideas do not (#191), and #197 counts as part of the century style book's
  mechanism. Family bar for the next strategy test: p < 0.10 / 112 = 0.00089 (these counts
  checked against `gate-null.md` on main, after W45). New candidates must pass two filters
  first: not announced, not driven by price (#109). Two literature surveys listed 11 more each
  (#177, #201); survey-8's only two testable ones became W38 and W39.

## Tonight's verdicts (night 6)

- `e4` against `tsmom12` on independent pre-1927 stock data (#198): **contradicted**, by the
  card's rule (D -0.065 a market, z -1.59, upper bound +0.002 below pooled-1's +0.063;
  low power, 0.26). `e4` leaves the open leads; see "What we know now".
- Real-rate currency value (#197): **fail, both primaries** (alpha against `tsmom12` z 1.71;
  in #170's style book z 2.74; bar 4.70). By the kill rules: no more variants of currency value
  on this panel, no more sleeve swaps in #170's book.
- What the calm-market drag is made of (#203, descriptive): false alarms re-entered higher,
  not costs and not late buy-backs; see "What we know now". The short stock whipsaws are the
  only plausible lever, and a weak one (the obvious reducers already failed). The split depends
  on the 25% cut-off.
- Where the early JST autocorrelation comes from (#204, descriptive): **not documented
  averaging; origin open.** Rule from now on: before 1966 a pooled timing test needs a null
  that keeps the autocorrelation (AR(1)-matched or block bootstrap, never rotation or random
  dates); a single-source test may use a standard null only on the cleared rows (Switzerland
  1926-1959, Germany 1871-1889 and 1914-1959).
- wide-22 (#202): **W36 `grid-load-premium` passed its kill-only gate, then failed its
  replication: dead** (t -2.31, rank 1 of 41, 1974-2025; R36 on 1926-1955 t -0.32, rank 13;
  R36 had about 20% power). Post hoc, phase surrogates ranked W36 3rd (#207: they would have
  stopped it).
- wide-23 (#205): **W37 `hack-drift` fails** (ETH after crypto thefts: t +0.68, predicted
  negative, rank 38 of 41; weak kill, expected t only about -1.1).
- survey-8 (#201, literature): 11 listed; nine dead or parked before any data, the other two
  became W38 and W39.
- gate-null-2 (#207, simulation): **the shifted-calendar rank is too liberal for persistent
  doses, but the t >= 2 rule hides almost all of it** (the full gate rule passes a null 0.9-3.1%
  of the time, up to 5.5% with a slow premium). No verdict changes. Proposed, not adopted: for
  doses with lag-1 autocorrelation of 0.8 or more, a pass also needs rank 2 or better among 40
  phase surrogates (W43 and W44 applied it by pre-registration). The 0.8 line rests on one cell.
- rl-7 (#209): **not shown.** A policy gradient on past-price features scored on 56 unseen
  markets: D +0.016 Sharpe a market (z 0.46); it relearns trend. Learning from prices alone
  stays closed; reopen only with other inputs (carry, value, macro).
- data-wide-2 (#206, no rule run): pre-1927 bonds (2,946 new market-years) and stocks (1,620)
  are not used up. The largest pool (Yale ICF London Investor's Monthly Manual, 1869-1929) is
  for academic use only by its terms: an owner decision is needed before any rule runs on it.
- Bank of England UK shares 1709-1866 (#212): **holds; the timing is not separable from
  autocorrelation.** 7 of 7 falls of 25% (sign p 0.008); avoided 0.66 against 0.41 fixed and
  0.38 random; beats AR(1) worlds (p 0.035) but not a block bootstrap (p 0.115). Fails in the
  South Sea crash of 1720. On Consols 4 of 4 falls, no timing.
- jst-gates-1 (#210, kill-only): **W38 `consumption-cycle` and W39 `bank-capital-premium`
  fail** (W38 t -1.88, rank 3 of 21, and -0.57 with a dose known at the time; W39 t +0.17, wrong
  sign). W38's alternative dose form (t -2.71) is a shown cell, not to be retried.
- asset-ledger-1 (#214, descriptive): about paid for itself on the long US stock record, not on
  bonds, gold or coins; see "But it has a price". Dropping timing on those would be a new try,
  chosen with hindsight, and needs its own card and bar.
- wide-24 (#215): **W40 `quake-drift` fails** (t +0.38, predicted negative, rank 24 of 41;
  moderate kill).
- survey-9 (#216, literature only): **agrees where it makes the same comparison**; its two
  artefact checks were run in #220.
- Long government-bond histories (insure-bonds-1, #219, descriptive): **too few 10% falls for
  the card; at 5% (amendment fixed before outcomes) Norway 1823-1984 does not hold, consols
  1867-1926 are in between.** Norway lost less in 4 of 11 falls (sign p 0.34; five are one-month
  falls where the rule was in, four of them administered-yield steps after 1946). Consols 9 of
  10 with 1 tie (sign p 0.002), share avoided 0.42 against 0.24 fixed and 0.20 random (p_rot
  0.069; AR nulls 0.073 / 0.097). The saving is handed back in the rebound in every reading.
  Rebuilt total returns are approximations.
- JST annual government bonds (insure-jstbonds-1, #225): **holds only as lower exposure.** 1,352
  country-years in 14 countries, 1871-2020, that overlap no scored bond series: lost less in 9
  of 12 falls of 10% (sign p 0.011), but avoided 0.70 against 0.68 fixed and 0.65 random; the
  gap is below the AR(1) and block-bootstrap medians (p 0.58 / 0.68). The bonds have no lag-1
  autocorrelation (-0.009): there is no timing to explain away. 1994 caught it fully in.
- Floating currencies 1791-1970 (fx-peg-1, #222): a real-time peg filter (24-month band test;
  agreement with the regime chronology 0.841, under the card's 0.85, the gap almost all
  1946-1970). **Insurance: holds only as lower exposure** (10 of 11 clusters, sign p 0.001; S
  0.63 = fixed 0.63, random 0.61). **Premium: not separable from autocorrelation** (long/short
  +4.2% a year, t 4.7; AR(1) p 0.057, drift kept p 0.50). Price only, no carry.
- Artefact checks on the early insurance results (stale-checks-1, #220): **averaging is real
  but barely moves the 12-month timing; the annual JST timing rests on last year's return.**
  US 1885-1925: averaged Shiller against point Dow Jones prices, lag-1 acf +0.250 against
  +0.015, timing gap +0.435 against +0.380 (dG +0.055, 4 falls). JST 1871-1965 with a year-older
  signal: S 0.72 -> 0.37 (p 0.73), 9 of 9 -> 5 of 9. AQR commodities 1877-1912 with a one-month
  delay: gap +0.186 -> +0.121 (ratio 0.65, "partly"). Not shown: real or artefact; falls are few.
- wide-25 (#221): 14 mechanisms scored before any price. **W41 `cabinet-collapse` fails on its
  sign** (kill-only): a country's market after a mid-term cabinet start, 18 markets 1976-2022,
  171 event months, b -1.66% over six months (t -1.74, predicted > 0), rank 41 of 41. The
  negative side (12 months t -2.60) is post hoc, not shown.
- wide-26 (#223): 14 mechanisms scored before any price. **W43 `drought-food-margin` fails**
  (US food stocks after Corn Belt drought, 1960-2025: t +0.07, rank 22 of 41 shifted and 23 of 41
  phase surrogates). **W18 `elimination-mood` closed dead** (74 knockout eliminations
  2006-2024: next-session b -0.081%, t -0.95, rank 6; the published 0.4-0.5% fall is 3.8-4.9 SE
  away). Three crop-weather channels are now dead (W19, W32/R32, W43).
- wide-27 (#226): 13 mechanisms scored before any price. **W44 `revision-noise` fails**
  (kill-only, both placebo families): payroll revision noise (Philadelphia Fed vintages) and the
  US market over three months, 1990-2025: t +0.24 (predicted > 0), rank 23 of 41 shifted and 19
  of 41 phase surrogates. The top-scored `patent-surge` is parked on data.
- w41-neg-1 (#229, kill-only): **W41's negative side is dead on independent years** (annual
  JST 1921-1959, b < 0 fixed in advance: b -2.9% a year, t -1.27, rank 5 of 21 earlier-dose
  calendars, AR bootstrap p 0.140). The postwar half (t -3.23) is post hoc, not a lead. Power
  about 26% against W41's -3.1%: a weak kill against a small drift.
- wide-28 (#230): 13 mechanisms scored before any price. **W45 `arms-fear` passed its kill-only
  gate, then failed its replication: dead** (FBI NICS gun-check growth and the US market two to
  four months on: t +3.50, rank 2 of 41 in both families; without the pandemic months t +1.95;
  R45 2000-2008 t +0.54, rank 13). `approval-mood` is parked: its only keyless source
  disallows AI agents in robots.txt.
- ownvol-indep-1 (#231): **own-vol on independent pre-1927 stocks: not shown, not
  contradicted** (D -0.007, SE 0.021, upper bound +0.028, below #110's +0.06; +0.010 with US
  dividends; five new markets 1975-2025 +0.010). See "What we know now".
- Data fix (eng-nits-1, #218): `infer_pos` dated a flip on a flat day one session late (78 of
  8,427 flips), and rounding-sized insurance values counted as wins or losses; ties now count
  as ties. Counts regenerated (US market 20 of 20 not tied, 13 developed 17 of 17); no verdict
  changed.
- Data fix (dw2-dates-1, #224): data-wide-2's parser dropped small Excel date serials, so the
  Norges Bank exchange rates started in 1927 instead of 1914, and a one-month spike in the
  BoE $/£ (1857-10) made a false 48% fall; both fixed. Only data-wide-2's counts move (currencies
  379 new market-years, 4 falls); no verdict changed.
- Engineering. The daily check rebuilds cash with the gym's own functions (#196). The daily
  runner fixes #161's findings (#199: source fallback, conflicting bars refused, fetch caps);
  #218 adds a test that an `IncompleteRead` falls back to the next source and documents that a
  Kraken hole repeats as a problem line for about four runs. The forward registry measures
  `lrv` at freeze, sizes lines with an upper value of it (expected power 0.80 in all ten weekly
  cells), and measures skew and kurtosis for Sharpe lines (#200, #208); dependence slower than
  a year still needs a larger `lrv` set by hand. mypy is clean on main again (#228, test
  annotations only). Nothing live changes.
- `BAR.md` as last regenerated (summary-10, in the order `research/register/README.md` states):
  4,492 tries, N 1,123, N_eff 509, z 4.70 (rows through 2026-11-25 23:32 UTC); the rows of
  #229-#231 are not yet in it.

Night 5's verdicts, in short (records and this file's git history have the detail): the century
long-short style book fails net of costs (#170, z 2.75); managing it by market volatility is
dead (#179); a VIX-call overlay is dead (#167); Hedge across 16 books is killed (#175); the
candidates from physics and control (#169), meteorology and actuarial work (#173), biology and
climate (#171) and history and psychology (#176) all fail; the post-2009 trend break is
inconclusive (#181); an Omori re-entry clock was not run, being a vol-calm re-entry in other
words (#187); on 1870-1965 annual data the 9-of-9 insurance count holds but the timing is not
shown (#186, #192); an e-value test does not change the forward registry's answer (#184); a
dependence-robust standard error for its verdict is adopted as an improvement, not a fix
(#189); `coin-drift-run` is killed on six unseen coins (#190); W32 passed then died in R32 and
W33 fails (#188); W34 `panic-words` and W35 `solar-max-recession` fail (#193, #194); keyless
consumer prices for 11 economies arrived (#174, used by #197); the register stores the current
live code versions (#166).

## Still open or running

- Daily run: the 2026-11-25 run passed (its snapshot matches the gym on `main` for all 12
  books). The next one is the first with #196 and #199 (fetch caps, source fallback).
- Open research PRs: none at the time of writing (#231 merged: own-vol not shown on
  independent stocks).
- Leads still open: the halving window's one forward score (#137). `e4` is closed as a lead
  (#198); `coin-drift-run` is dead (#157, #190).
- Live: 12 books trade fake money daily, `own_vol_70` included (#135). The record is days old:
  description only.

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
  #162 (`research/gap-2002-1.md`); what the calm drag is made of: #203 (`calm-drag-1.md`);
  buy-back: #94, #96, #103; puts and VIX calls: #160, #165, #167 (`insure-3.md`, `insure-4.md`,
  `vix-call-1.md`); the early annual data's autocorrelation: #192, #204 (`jst-autocorr-1.md`,
  `jst-autocorr-2.md`).
- Risk levels: #101, #105, #110 (`research/risk-menu.md`); own-vol paper book: #135.
- Is the edge real? #74 (`research/dsr-1.md`), #78; live funds #91 (`research/survey-6.md`).
- The bar: #92, #100, #108, #111 (`research/register/BAR.md`); what could reach it: #150, #170.
- Tonight: `research/e4-indep-1.md`, `fx-value-real-1.md`, `calm-drag-1.md`,
  `jst-autocorr-2.md`, `wide-22.md`, `wide-23.md`, `survey-8.md`, `registry-moments-1.md`,
  `gate-null-2.md`, `data-wide-2.md`, `rl-7.md`, `insure-1709-1.md`, `jst-gates-1.md`,
  `asset-ledger-1.md`, `wide-24.md`, `survey-9.md`, `insure-bonds-1.md`, `stale-checks-1.md`,
  `fx-peg-1.md`, `insure-jstbonds-1.md`, `wide-25.md`, `wide-26.md`, `wide-27.md`;
  engineering in `docs/DECISIONS.md` and `docs/forward-registry.md`.
- Night 5: `research/xs-century-1.md`, `vm-style-1.md`, `vix-call-1.md`, `hedge-books-1.md`,
  `e4-anatomy-1.md`, `reentry-reconcile-1.md`, `ownvol-anatomy-1.md`, `rev-costloss-1.md`,
  `tick-tier-1.md`, `omori-1.md`, `insure-1870-1.md`, `evalue-forward-1.md`,
  `breadth-anatomy-1.md`, `wide-17.md` to `wide-20.md`, `survey-7b.md`, `data-long-4.md`,
  `parked-gates-1.md`, `forward-se-1.md`, `coin-drift-2.md`, `jst-autocorr-1.md`,
  `panic-words-1.md`, `wide-21.md`.
- Shorts: #83, #89. Coins: #69, #82. Euro books: #59, #62, #63, #68, #73, #77, #80, #85.
- Corrections after the independent review (#119): [`errata-2.md`](errata-2.md).
- Earlier runs (machine learning, macro, carry, papers): [`README.md`](README.md) and this
  file's git history.
