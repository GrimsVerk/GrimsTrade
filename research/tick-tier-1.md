# tick-tier-1: did 12-month trend break after 2009 on stock indices and currencies but not on bonds?

Lane `tick-tier-1`, 2026-11-25 (night). Branch `tick-tier-1`, PR #181. Descriptive re-score,
kill-only: no new rule, nothing selected, a `note` row in `tries.md`. Card (pushed before any
number, not amended): `cards/tick-tier-1.md`. Tables: `results/tick-tier-1.md` (+ `.json`).
Code: `lib/ticktier1.py` (pooled-1's and pooled-2's loaders and rules, unchanged); tests
`tests/test_ticktier1.py`. One real run; two post hoc reading aids, marked as such. Train data
only (to 2025-10-31).

## The paper, checked

Kurth, Eisler, Rej and Bouchaud, arXiv 2607.01550 (2026-07), read from the abstract and the
HTML full text. About 100 futures, 1995-2025; signals EWM 5/20 to 50/200 days (no 6-12-month
signal); break "approximately 2008/9", Table 1 splits at 2009. Tick size = monthly average of
tick / daily volatility, ranked into halves. Small-tick: mostly equity indices and currencies;
large-tick: bonds ("almost pure"), most commodities (whose smaller-tick half degraded too).
Small-tick equal-risk Sharpe about 0.8 before and about 0 after; large-tick about 1.4 and
1.0-1.2. They say asset class alone does not reproduce the split. The survey's summary
(`survey-7b`, PR #177) matches the paper on all of these points.

## The answer on one screen

**By the card's deciding statistic, inconclusive. `tsmom12`'s own Sharpe above bills fell after
2009 in stocks, currencies and bonds alike (stocks 0.42 to 0.22, currencies 0.36 to -0.20, bonds
0.52 to 0.28, commodities 0.28 to 0.28). Small-tick classes minus bonds: C = -0.14 (SE 0.36,
z -0.38). `e4`: +0.10, "not seen". But the paper's pattern shows up clearly in the timing part
(the rule's Sharpe minus holding's): C = -0.77 (SE 0.23, z -3.40), `e4` -0.53 (z -2.87). Against
holding, the rule lost ground after 2009 on 33 of 34 stock series and 8 of 9 currencies, and on
none of 14 bond series. Part of that bond result is one episode (2022) (post hoc). Holding stocks got
better after 2009 and holding bonds got worse, so this is consistent with the paper at the
class level but cannot tell its mechanism from a change of regime.**

Sharpe above the US bill (cash at the bill), per series at its own frequency. Pre 1995-01..2008-12,
post 2009-01..2025-10. 65 of 70 series have five years in each window (34 stock, 9 FX, 14
bond, 8 commodity). Delta = post minus pre. SE from a joint 12-month block bootstrap drawn
separately inside each window.

| | Stocks (EQ, 34) | Currencies (FX, 9) | Bonds (BD, 14) | Commodities (CM, 8) | C = (dEQ + dFX)/2 - dBD | Reading (card) |
|---|---|---|---|---|---|---|
| `tsmom12` pre -> post | 0.42 -> 0.22 (-0.20, SE 0.24) | 0.36 -> -0.20 (-0.56, SE 0.25) | 0.52 -> 0.28 (-0.24, SE 0.30) | 0.28 -> 0.28 (-0.00) | **-0.14 (SE 0.36, z -0.38)** | **inconclusive** |
| `e4` | 0.41 -> 0.32 (-0.10) | 0.25 -> -0.13 (-0.39) | 0.57 -> 0.22 (-0.35) | 0.31 -> 0.31 (+0.01) | +0.10 (SE 0.40, z +0.26) | not seen at class level |
| holding | 0.17 -> 0.51 (+0.34) | 0.05 -> -0.05 (-0.11) | 0.66 -> 0.14 (-0.52) | 0.34 -> 0.39 (+0.05) | +0.63 (SE 0.47) | - |
| `tsmom12` minus holding | -0.54 | -0.45 | +0.28 | -0.05 | **-0.77 (SE 0.23, z -3.40)** | consistent (class level) |
| `e4` minus holding | -0.44 | -0.28 | +0.17 | -0.04 | -0.53 (SE 0.19, z -2.87) | consistent (class level) |

Every check gives the same picture (table in `results/`): with the break at 2010 the rule's C is
-0.25 (z -0.71) and the timing C -0.59 (z -2.79). Blocks of 3 or 24 months, equity cash at 0, and
pooled-1's 41 kept together all leave the rule's C between -0.08 and -0.16 and the timing C
between -0.75 and -0.78 (z -3.4 to -3.7). The commodity-inclusive C_4 is -0.26 (z -1.35) for the
rule and -0.61 (z -3.64) for timing. The full-sample `tsmom12` Sharpe of all 70 series
reproduces the logged pooled-1/pooled-2 rows exactly (2 decimals).

## What drives it

- **Currencies are the clean case.** `tsmom12` lost Sharpe on all 9 currencies (mean -0.56),
  while holding them barely changed (-0.11). Long-only currency trend went from about 0.36 to
  below zero. This matches the sign of the paper's small-tick result, here at the 12-month
  horizon (class is not tick).
- **Stocks: the rule held up, holding got better.** The rule's own Sharpe fell on 25 of 34 stock
  series (most of the foreign indices, for example France 0.61 to -0.13, Mexico 0.70 to -0.09;
  US industries only 5 of 10). Holding's Sharpe rose on almost all of them (mean +0.34): a long
  bull market with short falls (2011, 2020, 2022), where a 12-month filter steps out late and
  buys back late. So against holding the rule lost ground on 33 of 34 series (mean -0.54).
- **Bonds: the reverse.** The rule's Sharpe fell (-0.24), but holding's fell more (-0.52, the
  2022 rate shock and a decade of low yields), so against holding it gained on all 14.
- **Post hoc (not on the card): without 2022** (post window cut at 2021-12) the bond timing
  Delta is 0.00 (SE 0.09) instead of +0.28, while stocks (-0.57) and currencies (-0.48) stay.
  The timing C is then -0.53 (SE 0.20, z -2.6). So the stock and currency side does not depend on
  2022; the bond side's gain does.
- **Post hoc: is the stock timing drop just the higher drift?** No. On i.i.d. walks that keep
  each stock series' own drift and volatility in each era but have no trend (50 reps), holding's
  Delta is +0.23, and the timing Delta is only -0.03 (5-95%: -0.09..+0.03) against the real
  -0.54. What is left is either trend decay or the path: 1995-2008 held two long bear markets
  (2000-02, 2007-09), where a 12-month rule earns its keep, and 2009-2025 held none of that
  length. An i.i.d. null cannot separate those two (`results/tick-tier-1-posthoc.md`).
- Commodities (spot PPI and gold, not judged in pooled-2) show nothing either way (-0.00,
  timing -0.05). Gold alone rose (0.63 to 0.82).

## How sure

- Descriptive, one pre-registered split at the paper's own date. The deciding number on the card
  (the rule's own C) is inconclusive, as the card's power note expected (realised SE 0.36). The
  timing part clears its z of -2.0 easily and in every check. The card stated before the run that
  it reads only "trend, not drift" as a qualifier. That is reported here as a second reading, not
  promoted to the answer.
- Class is not tick. The paper says class alone does not reproduce its split, and we have no tick
  data. This is the class-level implication only. Horizon: 12 months (`e4`: 1-12 months), not the
  paper's 5-50 days. Long-only, not long-short futures.
- One break, one post-2009 path. Stocks had an unusually calm bull market and bonds their worst
  drawdown in decades in the post window. A microstructure story and a regime story predict the
  same signs here. The 2022-free cut shows the bond side rests on one episode.
- Series are rebuilt, not traded: price indices without dividends for most foreign stock
  markets (this lowers holding's level, not the change), constant-maturity bonds, monthly-average
  foreign yields, carry-inclusive interbank FX, spot PPI. They are the same in both windows.

## For the live six-asset book

The book holds SPY and QQQ (stock indices, small-tick class), TLT (bonds, large-tick), GLD
(gold; the paper does not place it by name) and BTC/ETH (not in the paper; their futures' tick
is tiny relative to volatility, so they would be small-tick if the definition carries over; not
tested here).

- What it says: since 2009, the 12-month rule's crash insurance has cost much more against
  holding on stock indices than before, and it has been worth more on bonds. This fits
  `gap-2002-1` (#162: about 1 point a year behind holding on the US index since 2002, the calm
  drag being most of the cost) and `insure-2`'s "not shown since 2002". Since 2009 the
  insurance has cost more against holding on SPY/QQQ, and the TLT slot is where the rule earned
  its keep (mostly 2022). By the card's pre-stated mapping (deciding reading inconclusive), this
  gives no forecast for the stock slot.
- What it does not say: nothing here is a rule or an edge, so nothing changes live. The rule's
  own Sharpe fell about as much on bonds as on stocks. Whether the stock-slot gap is
  microstructure or just a calm bull market cannot be decided from 17 years.

## Logged

Order of commits: the write-up commit preceded the post hoc results commit by two minutes; the
numbers quoted here are from the scratch run of the same code, and the committed post hoc
results (`results/tick-tier-1-posthoc.md`) reproduce them.

`tries.md`: one `note` row, idea `tick-tier-1` (re-score, not a try). `ideas.md`: a
`tick-tier-trend` line.
