# Research summary (2026-11-18, after night 2)

The live rule is `tsmom12`: hold an asset only while its price is above where it was a year ago,
otherwise cash. "Sharpe" below means return per unit of risk (higher is better).

## What we know now

- **The live rule earns about what simply holding the same assets earns.** Over 1994-2025 its
  Sharpe is 1.05 against 0.88 for holding all six, but that lead (p 0.08, not proven) comes from
  before 2010. From 2010 to 2025 the two tie: 1.11 against 1.11 (#74, #78).
- **What it buys is crash insurance, not an edge.** It loses less in long bear markets: 2008 -2%
  against -13% for holding, 2022 -13% against -38%. It cannot gain from a fall, as real trend
  funds do. A small euro book of seven funds shows the same: smaller worst loss (13.6% against
  19.8%), but lower Sharpe (0.62 against 0.78) and longer under water (58 against 31 months,
  #77). Using trend on fewer funds loses the insurance (#80).
- **Published effects fade once published: 0 for 5 in our tests** (#60, #64, #65, #72). Live
  trend funds kept about a fifth of the published trend effect (paper Sharpe 1.41, live 0.29,
  #78).
- **Any new "winner" now faces a very high bar.** The project has logged 2,904 tries. With that
  many shots, a new rule must beat `tsmom12` by +0.27 to +0.59 Sharpe to count (#79). The
  largest lead ever seen on the main test was +0.18, and it reversed after publication. Tonight's
  closest miss, a blend of two existing rules (1.13 against 1.05, p 0.059), fails (#70, #75).
- **Closed:** learning agents (#52), futures carry (failed its locked test year, #31), evolved
  rules (#58), blends (#75), the coin line (#69). Of 68 ideas borrowed from other fields, 16
  were tested and none passed (#76).
- **Coins:** the best coin rule, a 25% stop, cuts the worst loss in coin years from 36.5% to
  17.7% for about 2 points of growth a year: a risk choice, not a proven rule (#69).
- **A live test cannot settle it.** Telling the rule apart from holding would take about 107
  years of live data (#78).

## Still open or running

- `ls-trend-1`: would also betting on falls give the crash gains real trend funds get?
- `stop-reentry`: one fixed rule for buying coins back after the stop.
- `eu-8`: the euro book with interest on idle cash; trend on stocks plus long bonds.
- `wide-7`: three more borrowed ideas (tax-loss selling, festival gold demand, December pension
  withdrawals).
- Live: 11 books trade fake money daily. The record is days old: description only, no verdict.

## Decisions only you can make

Full list: "For the owner" in [`next-steps.md`](../next-steps.md). The main ones:

1. Treat `tsmom12` as a risk choice (smaller losses), not an edge (#74, #78)?
2. Adopt the project-wide tries register and its bar (#79)?
3. Add the coin stop as a risk preference (#69)? If yes, spend the locked test year on it only.
4. Add a euro paper book, with the rebalance band that cuts its orders by a third (#59, #73)?
5. Merge the engineering pull requests (interest on cash #61; #29, #30, #32)?

## Where to read more

- Is the rule's edge real? #74 (`research/dsr-1.md`), #78 (`research/survey-5.md`).
- The bar for new ideas: #79 (`research/register/BAR.md`).
- Coins: #69 (`research/coin-cap-verdict.md`). Blends: #70, #75.
- Euro investor: #59, #62, #63, #68, #73, #77, #80.
- Earlier runs (machine learning, macro, carry, papers): [`README.md`](README.md) and this
  file's git history.
