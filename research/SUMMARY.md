# Research summary (2026-11-24, night 4)

The live rule is `tsmom12`: hold an asset only while its price is above where it was a year ago,
otherwise cash. "Sharpe" below means return per unit of risk (higher is better). Agents now merge
and run this repo; 7 pull requests are open (listed under "Still open").

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
  price indices; since 2002 not shown (p 0.19).
- **But it has a price.** It buys back late, so the year after the low hands most of the gain
  back: since 2002 about 2 points of growth a year behind holding as the mean over the US market and 10 industries (insure-2), about 0.7-1.1 on the S&P 500 total return (insure-3). It fails in fast crashes of
  three months or less (1987, 2020). Faster buy-back rules did not fix this: early rallies look
  just like the bottom (#94, #96, #103).
- **Gaining in a crash needs shorts (bets on falls) across many markets.** That is how real
  trend funds gain in crashes (#83). Added to `tsmom12` without leverage, such a book gained in
  2008, 2020 and 2022, but cut Sharpe from 1.21 to 0.97 (#89). A risk choice, not an edge; the
  paper broker holds no shorts for now (answer B7).
- **Sizing by recent swings is the best-looking risk dial, but not a proven edge.** Re-run with
  no look-ahead, own-vol targeting kept Sharpe 0.97 (24% average share) and 1.04 (66%) against
  `tsmom12`'s 0.94 over 1994-2025. A lead of +0.03 to +0.10 is about one paired standard error
  (about 0.1) or less: noise (#110). Pooled over 41 other markets its 70% form leads by +0.022 a
  market, not shown (#142). It now trades as a paper book, `own_vol_70` (#135).
- **Live funds agree: no family beat its plain index after fees.** 15 strategy families, 60
  real funds. The published effects kept about a quarter of their paper Sharpe after
  publication (median about 28% over six factors), and long-only funds built on them matched
  their index after fees (#91). Our own tests of published effects: 0 for 7 (tonight's two:
  turbulence #134, seasonality #148).
- **The bar for a new rule is measured, and rebuilds on any computer.** 3,855 tries logged
  (725 new since the count of 19 November, 660 of them robustness checks), worth between 11 and
  500 independent shots depending on how they are counted; the bar uses the cautious 500. A new
  rule must beat `tsmom12` at z >= 4.70, which is +0.31 to +0.56 Sharpe for rules correlated
  0.77-0.93 with `tsmom12` (others use the z column in `BAR.md`) (#92, #100). The growth moved
  it by 0.01 (was 3,130 tries, N_eff 486, z 4.69, +0.30). The weekly returns behind it are
  committed, so `BAR.md` regenerates from a clean checkout (#108, #111). The closest results
  stay below it: `halving-alone` +0.23 (z about 3.2-3.6, #137), about at the 3.25 the bar would
  be if tries were counted by clusters, and the coin rebalance band (z 2.76, #145).
- **The bar is out of reach for every class we can test** (#150). With edges of the size the
  records show, no strategy class we can test has a realistic chance to clear the bar. Power
  depends on years of data, not on bar frequency. Forward paper scoring cannot confirm an edge:
  +0.10 over `tsmom12` by a book correlated 0.95 with it needs 72 years of record at 80% power
  even when registered alone (356 at the bar). The only case where a pass is not absurd: a
  long-short style book on about 100 years of data, scored under an alpha comparator (does it
  add to `tsmom12`?), which needs shorts, data the gym cannot trade and a comparator change the
  project has not adopted.
- **Borrowed ideas: 88 mechanisms listed, 19 tested by a strategy, 22 gates, none passed** (many
  gates can only kill an idea, never pass one, by design: few independent episodes; #124). New
  candidates must pass two filters first: not announced, not driven by price (#109).

## Tonight's verdicts (night 4)

- Halving rule on other halving coins (#137): **BTC-beta.** A coin's own halving dates make it
  worse (Litecoin + Zcash: rank 40 of 41 placebos); only BTC's calendar works, which is the same
  three coin winters again. `halving-alone` stays at +0.23 (z about 3.2-3.6), now read as a
  BTC-cycle coincidence. Only its forward window, inside the held-out year, is left to score.
- Financial turbulence as a crash overlay (#134): **dead.** A volatility trigger in disguise:
  -0.04 Sharpe against a plain-volatility twin that is out of the market just as often (p 0.84).
- Near-miss trend variants pooled over 41 markets (#142): **none passes** (best z 1.55 against
  2.50 for 8 rules). Two stay open, leaning positive: `e4`, an ensemble of 1/3/6/12-month
  signals (+0.063 a market), and the own-vol 70% form (+0.022).
- More markets in the `tsmom12` book (#143): **lower Sharpe.** 12, 20 and 35 assets give 0.96,
  0.83 and 0.65 against the six's 1.19 (z -2.3 to -2.6); the smaller worst loss is only a
  smaller coin share.
- Same-calendar-month seasonality (#148): **dead.** Absent in US industries since 1945, in 13
  developed markets and on the six assets; as an overlay 0.88 against `tsmom12`'s 1.06 (z -2.76).
- Two gates from unused fields (#139), legislative workload and tax-refund flows: **both fail**
  (ranks 25 and 7 of 41).
- A cost-sized rebalance band for coin slots (#145): **fails** (+0.049 Sharpe, z 2.76 against
  4.69). Post hoc the gain is not the fee but letting coin slots run in rallies
  (`coin-drift-run`, new, weak).
- Execution lag (#144): barely matters for ten of the 11 books (all under 0.075 Sharpe); an
  earlier crypto-only run is not worth building. Its rule 2 triggered on `buy_hold_btc` (+0.92
  CAGR points a year from a one-day-later first coin entry), so the scoreboard carries a
  live-start-delay note (#155).
- Live record against the gym (#141): **live equals the gym** for 9 of 11 books every day; the
  other 2 differ only by the schedule (at most 0.5%). No bugs, no data errors. Every run so far
  used the code from before tonight's merges, so the next run moves four coin books once (3 to
  18 USD each).
- Engineering, landed: forward registry hardening and the delayed daily schedule recorded in
  DECISIONS (#133), a Treasury bill-rate fallback (#138), a Gymnasium environment around the
  gym (#140), the daily job without the dev tools (#147).

## Still open or running

- Re-scoring the stored record in alpha form against `tsmom12` (#154): 341 stored series, 0
  reach the bar of 4.70; the 2 above 3.29 are known artefacts (`fm-1` memorisation, `merfx7`
  with cash at 0).
- Held until after the 2026-11-25 daily run: one replay engine for the gym and the learning
  environment (#149), the daily run reconciling its own record (#153), the scoreboard's
  live-start-delay note (#155).
- Work in progress: keyless long histories for rates, FX and commodities (#152), the night
  lead's notes (#146), this summary (#156).
- Lane `register-7` is fixing `register2.py`'s dead source-branch reference and its rule for
  duplicate live series (the store keeps old copies when the live code changes).
- Leads still open: `e4` and own-vol 70% pooled (#142); `coin-drift-run` (#145, post hoc); the
  halving window's one forward score (#137).
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

- Crash insurance: #87, #90 (`research/insure-2.md`); buy-back: #94, #96, #103.
- Risk levels: #101, #105, #110 (`research/risk-menu.md`); own-vol paper book: #135.
- Is the edge real? #74 (`research/dsr-1.md`), #78; live funds #91 (`research/survey-6.md`).
- The bar: #92, #100, #108, #111 (`research/register/BAR.md`); what could reach it: #150.
- Tonight: `research/halving-2.md`, `turbulence-1.md`, `pooled-1.md`, `breadth-book-1.md`,
  `seasonal-1.md`, `wide-15.md`, `wide-16.md`, `lagcost-1.md`, `reconcile-1.md`.
- Shorts: #83, #89. Coins: #69, #82. Euro books: #59, #62, #63, #68, #73, #77, #80, #85.
- Corrections after the independent review (#119): [`errata-2.md`](errata-2.md).
- Earlier runs (machine learning, macro, carry, papers): [`README.md`](README.md) and this
  file's git history.
