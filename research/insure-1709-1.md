# insure-1709-1: does trend's crash insurance hold on UK monthly data 1709-1866?

Lane `insure-1709-1`, 2026-11-25 (UTC). Branch `insure-1709-1`. Research only: fake money,
keyless public data, no change to the gym, the daily runner or the live strategies. Card:
[`cards/insure-1709-1.md`](cards/insure-1709-1.md) (commit aab34a7, 22:11 UTC, before any
number on these series; its text says "~22:25", which is wrong: it was written 22:05-22:11).
Before-scoring table: commit 763d373 (22:14), before any rule position or episode. Tables:
[`results/insure-1709-1.md`](results/insure-1709-1.md). Code: `lib/insure1709.py`, tests
`tests/test_insure1709.py`. Data: Bank of England, "A millennium of macroeconomic data for the
UK" v3.1 (Open Government Licence v3), read locally; only statistics are committed.

## The answer on one screen

**The insurance holds out of sample, and its timing beats random dates and an AR(1) null. It
does not beat a block-bootstrap null. By the card that reads "Holds, timing not separable from
autocorrelation". On 158 years of monthly London share prices that no scored series covers
(1709-1866), monthly `tsmom12` lost less than holding in 7 of 7 falls of 25%+ (sign p 0.008)
and kept the gain after the rebound (7 of 7). It avoided 0.66 of each fall, against 0.41 for
the same average exposure held fixed and 0.38 at random dates (p_rot 0.000). Its timing gap
over random dates (+0.28) beats Gaussian AR(1) worlds with each source's own autocorrelation
(p 0.035). It does not beat a block bootstrap of the series' own returns (p 0.115), so the
card's decisive p_AR is 0.115. Seven falls is too few to separate the two. Consols (the
secondary series): 4 of 4 falls lost less, which is too few to test, and no timing (S 0.51
rule = 0.51 fixed).**

| Run (25% falls) | Falls | Lost less | S: rule / fixed / random (p_rot) | Gap G; p AR1 / BB | Premium: rule / fixed | Verdict |
|---|---:|---|---|---|---|---|
| **UK shares 1710-1866 (primary)** | 7 | **7 of 7** (p 0.008), N > 0 in 7 | **0.66** / 0.41 / 0.38 (0.000) | +0.28; **0.035 / 0.115** | 0.70 / 1.49 | **Holds, timing not separable from autocorrelation** |
| Consols 1754-1866 (secondary) | 4 | 4 of 4 (p 0.063), N > 0 in 3 | 0.51 / 0.51 / 0.49 (0.42) | +0.03; 0.50 / 0.55 | 0.42 / 0.84 | Too few falls |
| Shares, signal a month older (stale check) | 7 | 7 of 7 | 0.67 / 0.41 / 0.38 (0.000) | +0.28; not run | 0.92 / 1.48 | description |
| Shares, 20% / 20% | 11 | 11 of 11 (p 0.0005) | 0.67 / 0.41 / 0.38 (0.003) | +0.28 | 0.77 / 1.39 | description |
| Shares, Neal's 3 shares alone (1710-1811) | 5 | 5 of 5 (p 0.031) | 0.57 / 0.47 / 0.45 (0.173) | +0.13 | 0.72 / 1.10 | description |

(Rule: at each month-end, hold the index next month if its 12-month log change is above 0,
else cash at 0; 2 bps a side. Price indices, no dividends. S = share of the fall's log loss
avoided. p_rot: share of 1,000 common rotations of the positions with a mean S at least the
rule's. AR1/BB: share of 1,000 synthetic worlds whose gap G is at least the observed one.)

- **The falls.** South Sea 1720-22 (-74%), the Seven Years' War 1752-62 (-38%), the run-up to
  and the American war 1768-84 (-43%), the French wars 1792-97 (-40%) and 1802-03 (-30%), the
  late Napoleonic wars and post-war slump 1809-16 (-42%), and the railway bust 1846-48 (-28%).
  There is none in the 1825 crisis or in 1866 at 25% on this index. Five of the seven are
  slow war falls, which a 12-month rule handles best. Consols fall with shares in four of
  them, so the pooled set has 7 linked clusters, not 11.
- **Where it fails, as on daily data: the fast fall.** In the South Sea crash the rule was
  fully in at the June 1720 peak and lost 111 log points against holding's 133 (S 0.16). Every
  other fall: S 0.47-0.91.
- **Timing, controls first.** Lower exposure alone (a fixed 61%) avoids 0.41; random dates
  0.38 (5-95%: 0.21-0.57). The rule's 0.66 is above all 1,000 rotations. The premium order
  rule < fixed < random holds: 0.70 < 1.49 < 1.66 (p_P 0.006). A premium below 1 means the
  rule's price-only return finished ahead of holding: it gave back 0.70 of what it saved in
  falls, in the rebounds (-75 log points in total) and in calm years (-0.80 log points a year).
- **Autocorrelation, checked before scoring.** Monthly log returns of the share index are
  autocorrelated in all three source periods (lag 1): Neal +0.25, Gayer-Rostow-Schwartz +0.50,
  Acheson et al. +0.23, all far above the noise line (0.05-0.13). So by the card all three are
  "stale-suspect". Consols are not (+0.03). Zero-change months are rare (0-6%), so this is not
  a frozen-price index. Under Gaussian AR(1) worlds with these coefficients the rule's median
  gap is +0.15 (iid worlds: +0.08); the observed +0.28 is at their 96.5th percentile. The
  block bootstrap (mean block 3 months, each period's own returns: keeps lag 1-2 dependence,
  fat tails and some volatility clustering) has a similar median (+0.14) but a much wider
  spread (5-95%: -0.06 to +0.32). The observed gap is at its 88.5th percentile. Even the iid
  reference only gives p 0.019. With 7 falls the gap is noisy, and fat tails widen it further.
- **The stale check points away from stale prices.** If the timing came from prices that lag
  by a month (thin trading), deciding on a signal a month older should remove it. It does not:
  S 0.67 and the gap +0.28 are unchanged (premium 0.92 instead of 0.70). A one-month delay
  removes the lag-1 channel but not lag 2 (Neal +0.12, GRS +0.26), and the null for the delayed
  rule was not run (not on the card). So this is evidence against a lag-1 stale-price artefact,
  not a test.
- **What it adds to the SUMMARY claim.** Independent data, monthly, 1709-1866, a market and two
  centuries that no lane has scored: the insurance (lost less, kept net of the rebound) holds
  7 of 7, at the claimed strength (S 0.66 against "about half" since 1927). The timing beats
  random dates clearly and an AR(1) null narrowly. It falls short of a fat-tailed block-bootstrap
  null on 7 falls. Like the annual JST result, the timing evidence is "consistent with timing,
  not separable from the series' autocorrelation", but here the autocorrelation is weaker
  relative to the signal. Nothing changes for the live rule.

## How sure

- **Few, mostly dependent falls.** 7 falls in 158 years, one series. Five are war falls; the
  smallest possible sign-test p with 7 is 0.008. The project bar (`register/BAR.md`, rows
  through 2026-11-25 01:16: N 1,116, Bonferroni p <= 4.5e-05) is out of reach by design. This
  is a check of a descriptive claim, not a pick.
- **The splice differs from the card.** The card read the documentation as Neal to 1824 and
  then Acheson et al. Matching monthly changes (the card's rule) shows three sources instead:
  - Neal (3 shares: Bank of England, East India and South Sea Companies, unweighted, end month)
    1709-04 to 1811-02;
  - Gayer-Rostow-Schwartz without mines (63 companies, timing not stated) 1811-03 to 1825-03;
  - Acheson et al. (681 companies, cap-weighted, end month) from 1825-04.

  The cached CSV equals the workbook's spliced column exactly (1,893 months). The GRS period
  has a lag-1 acf of +0.50 and a lag-2 acf of +0.26, which looks like smoothing (an averaged or
  interpolated index); its sampling is not stated. Fall 6 (1809-11 to 1816-09, S 0.86) runs
  mostly through it. Without that fall, the rule still lost less in 6 of 6 (post hoc remark,
  not a test).
- **Neal alone is weaker on timing.** Scored on Neal's 3 shares alone (1710-1811), the rule
  lost less in 5 of 5 (p 0.031), but its S (0.57) is barely above fixed (0.47) and random
  (0.45; p_rot 0.173). The full-series timing leans on the 1809-16 and 1846-48 falls, where S
  is 0.86-0.91. The GRS and Acheson periods alone have one fall each.
- **Other indices over the same years (not independent).** Hayek (unweighted, 1821-1866): 3 of
  3, S 0.70 / 0.42 / 0.38 (p_rot 0.002). GRS with mines: 3 of 3, S 0.60 / 0.55 / 0.52 (0.34).
  GRS without mines: 3 of 3, S 0.67 / 0.49 / 0.47 (0.13). Acheson paid-up weighted: 2 of 2.
  Acheson unweighted: no 25% fall. The insurance always holds; the timing margin depends on
  the index.
- **Price-only, cash at 0.** No monthly dividends exist for these years. Holding forgoes no
  dividend in the comparison, and the rule earns nothing while out; the two omissions roughly
  offset. Check 1 (cash at the discount rate on prime paper, from 1718; 0 before) adds the
  interest but still no dividends. It is biased toward the rule (S 0.98, premium 0.12 for
  shares; -0.55 for consols, i.e. the rule beat holding outside falls too) and is shown only
  for completeness.
- **Consols.** Price = 1/yield, a perpetuity. The yield sources are Neal (end month) 1753-1823
  and then Odlyzko and the NBER (timing not stated). Four falls (the Seven Years' War, the
  American war, 1792-98, 1802-03); the rule lost less in all four, but the share avoided equals
  fixed exposure: no timing on consol prices. With coupon accrual (total return), S is 0.66
  against 0.29 fixed and 0.26 random (p_rot 0.016). That is a description only: the accrual
  changes the trend signal itself.
- **Monthly, not weekly.** The gym's rule decides weekly; this one decides at month-ends,
  which delays exits by up to a month. That biases against the rule in fast falls (1720).
- **Window.** Shares and consols stop at 1866-12. UK stocks were scored from 1867 (e4-indep-1:
  NBER GB industrial shares; data-wide-2's `SEEN`), JST from 1870. data-wide-2's fall counts on
  these series were not read by this lane.

## Logged

`tries.md`:
- 1 `note` row: the before-scoring autocorrelation table;
- 17 `insure-check` rows, idea `insure-1709-1`, variants `tsmom12m@insure-1709-*`: the
  two primary series and 15 checks. Sharpe = mean / sd of monthly rule returns x sqrt(12).

Rotations, AR worlds and the fixed control are re-scorings, so they get no rows. Downloads:
the BoE workbook, 27.5 MB, once, from bankofengland.co.uk (robots.txt checked; `/-/media/` is
not disallowed), into the local data cache. Only its header text and its M13 sheet were read.
The 6 MB monthly CSV was reused from jst-autocorr-2's cache.
