# seasonal-1: `seasonal-20y` (same-calendar-month seasonality) on long histories

Lane `seasonal-1`, 2026-11-24, branch `seasonal-1`, PR #148. Research only: fake money, cached
keyless public prices, train data only (nothing after 2025-11-10 parsed). Card
`cards/seasonal-20y.md` (pushed before any number, commit 968d07b); script
`lib/seasonal1.py` with rules in `lib/seasonal1_rules.py` and look-ahead tests in
`tests/test_seasonal1.py` (pushed before the run, 8aad519); tables `results/seasonal-1.md`.
One dry run (counts only), then one real run; nothing tuned or rerun. 112 rows in `tries.md`
(2 variant, 2 baseline, 108 robustness).

## In plain words

**Dead for this book. Holding an asset only in calendar months that were better than its
average month over the past 20 years lost to plain holding, and as an overlay it lost to
`tsmom12`, in the US since 1945, in 13 developed markets and on the six-asset test.** Not a
pick (primary overlay z -2.76 against the bar's +4.69). By the card's labels: *absent* on every
book and every single series.

| Test (decides in bold) | Weeks | Standalone - hold: diff (z) | Overlay - `tsmom12`: diff (z) |
|---|---:|---|---|
| **US ten-industry book, 1945-08 .. 2025-11** | 4,189 | **-0.13 (-1.89)** | -0.17 (-2.21) |
| US book, before 1981 / from 1981 | 1,848 / 2,341 | -0.11 (-0.98) / -0.13 (-1.53) | -0.24 (-1.89) / -0.14 (-1.41) |
| US book, before 2008 / from 2008 | 3,257 / 932 | -0.08 (-0.99) / -0.17 (-1.41) | -0.17 (-1.88) / -0.18 (-1.26) |
| US market alone | 4,189 | -0.30 (-3.62) | -0.38 (-4.50) |
| US book, fill one session later | 4,189 | -0.16 (-2.32) | -0.20 (-2.71) |
| 13 developed markets, 1984-02 .. 2025-11 | 2,180 | -0.07 (-0.62) | -0.03 (-0.30) |
| 13 markets, before 2008 / from 2008 | 1,248 / 932 | -0.13 (-0.81) / +0.02 (+0.19) | -0.14 (-0.82) / +0.14 (+1.06) |
| **Primary six assets, 1994-02 .. 2025-11** | 1,657 | -0.07 (-0.86) | **-0.18 (-2.76)** |
| Six, before 2008 / from 2008 | 725 / 932 | -0.21 (-1.25) / -0.05 (-0.82) | -0.37 (-2.34) / -0.10 (-1.96) |

Sharpe differences on weekly returns, annualised; z = difference / paired bootstrap SE.
Primary six: overlay 0.88 against `tsmom12` 1.06; standalone 0.84 against holding 0.91.
Single series: the standalone rule is behind holding on 10 of 10 US industries (z -1.4 to -2.9)
and on 8 of 13 markets (best: Singapore +0.15, z 0.93); the overlay is behind `tsmom12` on 10 of
10 industries and 9 of 13 markets.

## What it means

1. **No "strong before 1981".** R5 reports the signal strong in its pre-1981 sample; on US
   industries 1945-1980 it is behind holding (-0.11, z -0.98). The card's *early only* reading
   did not happen. Before 1981 and after it, before 2008 and after it, the sign is the same.
2. **Most of the loss is the price of switching in and out, not a wrong signal.** With cash at 0,
   holding an asset a random half of the months keeps about sqrt(0.5) = 71% of its Sharpe, so a
   timing rule with no information loses about 0.2-0.3 of Sharpe against holding. The placebo
   rows show exactly that: the same rule with the "same month" replaced by off-cycle months
   (lags 12 j + s, s = 1 .. 10) loses -0.15 to -0.29 (mean -0.21, sd 0.045) on the US book.
3. **Against those placebos the true annual lag ranks first of 11** (-0.13 against a mean of
   -0.21; empirical p = 1/11 = 0.09, about 1.8 placebo sds). So there is a trace of the
   published same-month pattern in US industries, of the size the papers' critics expect: it
   recovers about a third of what random switching costs and never pays for being out of the
   market half the time. The placebo set was on the card as shown, not deciding; 11 overlapping
   lags are not 11 independent draws, so the trace is weak.
4. **The calendar it learns is the familiar one** (checked after the run, as a bug check): on the
   US market the season is on in 0% of Septembers, 98% of Decembers, 81% of Novembers, 68% of
   Januaries, 20% of Februaries. Those months' 20-year means are noisy (standard error about 1%
   a month), and the next month does not follow them reliably enough.
5. **For the live rule: nothing changes.** As an overlay it removes half of `tsmom12`'s exposure
   (76% to 37% on the US book, 76% to 47% on the six) and loses Sharpe everywhere but in the
   13 markets after 2008 (+0.14, z 1.06), one era seen after the fact.

## How sure

- The bar was written before the run; the verdict does not lean on it. The rule is behind
  holding in every era of the longest data set, so no reading of the counts turns it into a pass.
- The data sets are not independent of each other (US industries are one market seen ten ways;
  the 13 markets share global months; SPY's proxy is the US market), so "absent everywhere" is
  a few independent looks, not 28.
- The primary test's season comes from proxies: `^GSPC` (price, no dividends) for SPY, `^IXIC`
  for QQQ, `^TNX` turned into a bond return (carry minus duration 17 times the yield change) for
  TLT. GLD, BTC and ETH keep their slots unfiltered (no 20-year month-end series in the cache).
- The 13 markets are price indices in local currency, and their Yahoo histories start late or
  with gaps, so the 20-year signal starts in 1984 (Japan) to 2012 (Spain); the book is Japan
  alone until 1998. No pre-1981 weeks there or on the six.
- The cross-sectional form the papers document (rank assets against each other) was tested by
  `survey-7` on 23 ETFs and also failed; neither test reaches the stock-level evidence of
  Heston-Sadka and KLN, which needs individual stocks.

## Deviations and disclosures

- The card said the US test starts "about 1946-07". By the card's own rule (19 of 20 same-month
  returns, 228 of 240 months) the first holding month is 1945-08; the run used the rule, not the
  estimate.
- Holding month = the month of the next weekday after the latest close; when a series still has
  a session in the old month (Saturday sessions before 1953) the switch waits for it. That guard
  uses the session calendar, not prices; written in `seasonal1_rules.Season.state`, tested.
- The per-month on-shares in point 4 were computed after the run, as a sign check of the code;
  no rule was changed.
- The paired Sharpe difference against a fully invested comparator has a negative null for any
  timing rule (point 2); the card did not say so. It does not change the verdict (the
  card's question is whether the rule beats holding, and it does not; against the placebos it
  leaves only the weak trace of point 3), but the next calendar card should compare with a
  placebo or a constant-exposure twin, not with zero.

## Next

Nothing on this idea. If anyone revisits calendar seasonality, the only open form is the
stock-level cross-section (Heston-Sadka), which this book cannot hold.
