# Research summary (2026-11-19, end of night 2)

The live rule is `tsmom12`: hold an asset only while its price is above where it was a year ago,
otherwise cash. "Sharpe" below means return per unit of risk (higher is better).

## What we know now

- **The rule is crash insurance, not an edge.** It earns about what simply holding the same six
  assets earns (2010-2025: Sharpe 1.11 each, #74, #78). What it adds is smaller losses in long
  bear markets.
- **The insurance is real, and holds everywhere we looked.** In 50 independent US falls of 25%
  or more since 1927 it lost less than holding in 48, avoiding about half of each (#87). In 13
  other developed markets since 1966: 17 of 18 (#90). It is cheaper than simply holding less.
- **But it has a price.** It buys back late, so the year after the low hands most of the gain
  back: since 2002 about 2 points of growth a year behind holding. It fails in fast crashes of
  three months or less (1987, 2020). Faster buy-back rules did not fix this: early rallies look
  just like the bottom (#94, #96, #103).
- **Gaining in a crash needs shorts (bets on falls) across many markets.** That is how real
  trend funds gain in crashes (#83). Added to `tsmom12` without leverage, such a book gained in
  2008, 2020 and 2022, but cut Sharpe from 1.21 to 0.97 (#89). A risk choice, not an edge; the
  paper broker cannot hold shorts today.
- **Live funds agree: no family beat its plain index after fees.** 15 strategy families, 60
  real funds; published backtests kept a median 8% of their paper result (#91). Our own tests
  of published effects: 0 for 5.
- **The bar for a new rule is now measured.** 3,118 tries logged, worth about 486 independent
  shots. A new rule must beat `tsmom12` by +0.30 to +0.56 Sharpe to count (#92, #100). The
  largest lead ever seen on the main test was +0.18, and it faded.
- **Closed:** learning agents, futures carry, evolved rules, blends, volatility timing as an edge
  (#98), short sleeves (#99), euro-book variants (#85), borrowed ideas (78 listed, 18 tested,
  none passed). Coins: a 25% stop is a risk preference, not a proven rule (#69, #82).

## Still open or running

- `wide-11` (more borrowed ideas), `breadth-screen` (style signals on a wide fund set),
  `register-4` (lets the bar be recomputed on any computer).
- Live: 11 books trade fake money daily. The record is days old: description only.

## Decisions only you can make

**The main one: pick your risk level** from the risk menu, `research/risk-menu.md` (#101), a
single "if you care most about X, pick Y" table. Example (2007-2025): own-vol target (size set
by recent swings) at 70% had a worst loss of 18% against 25% for a fixed 70%; holding the six
grew most (27% a year) with a 47% worst loss. None of the rows is a proven edge.

Then, in "For the owner" in [`next-steps.md`](../next-steps.md):

1. Treat `tsmom12` as a risk choice, not an edge (#74, #78)?
2. Accept the measured bar (#92) and the project-wide tries register (#79)?
3. Let the paper broker hold shorts, so a crash-gaining book can be tested live (#83)?
4. Coin stop as a risk preference (#69)? Euro paper book with the order-saving band (#59, #73)?
5. Merge the engineering pull requests (interest on cash #61; #29, #30, #32)?

## Where to read more

- Crash insurance: #87, #90 (`research/insure-2.md`); buy-back: #94, #96, #103.
- Risk levels: #101, #105 (`research/risk-menu.md`).
- Is the edge real? #74 (`research/dsr-1.md`), #78; live funds #91 (`research/survey-6.md`).
- The bar: #92, #100 (`research/register/BAR.md`).
- Shorts: #83, #89. Coins: #69, #82. Euro investor: #59, #62, #63, #68, #73, #77, #80, #85.
- Earlier runs (machine learning, macro, carry, papers): [`README.md`](README.md) and this
  file's git history.
