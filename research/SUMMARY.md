# Research summary (2026-11-19, night 3)

The live rule is `tsmom12`: hold an asset only while its price is above where it was a year ago,
otherwise cash. "Sharpe" below means return per unit of risk (higher is better). To decide on
the ~100 open pull requests, start with [`pr-map.md`](pr-map.md) (#113).

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
  back: since 2002 about 2 points of growth a year behind holding. It fails in fast crashes of
  three months or less (1987, 2020). Faster buy-back rules did not fix this: early rallies look
  just like the bottom (#94, #96, #103).
- **Gaining in a crash needs shorts (bets on falls) across many markets.** That is how real
  trend funds gain in crashes (#83). Added to `tsmom12` without leverage, such a book gained in
  2008, 2020 and 2022, but cut Sharpe from 1.21 to 0.97 (#89). A risk choice, not an edge; the
  paper broker cannot hold shorts today.
- **Sizing by recent swings is the best-looking risk dial, but not a proven edge.** Re-run with
  no look-ahead, own-vol targeting kept Sharpe 0.97 (24% average share) and 1.04 (66%) against
  `tsmom12`'s 0.94 over 1994-2025. A lead of +0.03 to +0.10 is about one paired standard error
  (about 0.1) or less: noise. The menu order did not change (#110).
- **Live funds agree: no family beat its plain index after fees.** 15 strategy families, 60
  real funds. The published effects kept about a quarter of their paper Sharpe after
  publication (median about 28% over six factors), and long-only funds built on them matched
  their index after fees (#91). Our own tests of published effects: 0 for 5.
- **The bar for a new rule is measured, and now rebuilds on any computer.** 3,130 tries logged,
  worth between 12 and 486 independent shots depending on how they are counted; the bar uses the
  cautious 486. A new rule must beat `tsmom12` at z >= 4.69, which is +0.30 to +0.56 Sharpe for
  rules correlated 0.77-0.93 with `tsmom12` (others use the z column in `BAR.md`) (#92, #100).
  The weekly returns behind it are committed, so `BAR.md` regenerates from a clean checkout
  (#108, #111). The largest lead seen on the main test is +0.23 (`halving-alone`, a secondary
  variant whose edge sits in two or three coin cycles; z about 3.2-3.6): below the bar of 4.69,
  but at the 3.29 the bar would be if tries were counted by clusters.
- **Borrowed ideas: 80 listed, 19 tested, none passed** (several gates could only kill an idea,
  never pass one, by design: few independent episodes; #124). New candidates must now pass two
  filters first: not announced, not driven by price (#109). Tonight's gates failed too: foreign
  central banks' Treasury selling (#112: wrong sign, rank 34 of 41) and weather surprises for
  natural gas (#116: no signal; the lane reads it as the market pricing the forecast, untested). Style signals (value, carry, momentum,
  low risk) are flat on a 34-fund set too (#106).
- **Closed:** learning agents, futures carry, evolved rules, blends, volatility timing as an edge
  (#98), short sleeves (#99), euro-book variants (#85), style signals on keyless funds (#106).
  Coins: a 25% stop is a risk preference, not a proven rule (#69, #82).

## Still open or running

- Night 3: inflation-disagreement gate (#112), keyless data for the new filters (#114), the
  engineering integration preview (#115, review aid, not for merge), this PR map (#113).
- Live: 11 books trade fake money daily. The record is days old: description only.

## Decisions only you can make

**The main one: pick your risk level** from the risk menu, `research/risk-menu.md` (#101, #105,
#110), a single "if you care most about X, pick Y" table. Example (2007-2025, no look-ahead):
own-vol target (size set by recent swings) aimed at 70% held 61% on average, grew 13.8% a year
with a worst loss of 15.7%, against 17.6% and 24.6% for a fixed 70%: 3.8 points of growth a year
for 8.9 points less worst loss; holding the six grew most (27% a year) with a 47% worst loss. None of the rows is a proven edge.

Then, in "For the owner" in [`next-steps.md`](../next-steps.md) (numbered O1-O18 in
[`pr-map.md`](pr-map.md) section 5):

1. Treat `tsmom12` as a risk choice, not an edge (#74, #78)?
2. Accept the measured bar (#92) and the project-wide tries register (#79)?
3. Let the paper broker hold shorts (#83), or perpetual futures (#109, the last candidate)?
4. Coin stop as a risk preference (#69)? Euro paper book with the order-saving band (#59, #73)?
5. Merge the engineering PRs in the order of `pr-map.md` section 3 (#27, #13, #29, #30, #32,
   then interest on cash #61); land the 90 research PRs as one archive (section 4)?

## Where to read more

- Crash insurance: #87, #90 (`research/insure-2.md`); buy-back: #94, #96, #103.
- Risk levels: #101, #105, #110 (`research/risk-menu.md`).
- Is the edge real? #74 (`research/dsr-1.md`), #78; live funds #91 (`research/survey-6.md`).
- The bar: #92, #100, #108, #111 (`research/register/BAR.md`).
- Shorts: #83, #89. Coins: #69, #82. Euro books: #59, #62, #63, #68, #73, #77, #80, #85.
- Corrections after the independent review (#119): [`errata-2.md`](errata-2.md).
- Earlier runs (machine learning, macro, carry, papers): [`README.md`](README.md) and this
  file's git history.
