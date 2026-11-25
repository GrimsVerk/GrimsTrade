# insure-jstbonds-1: does trend's crash insurance hold on JST annual government-bond returns?

Lane `insure-jstbonds-1`, 2026-11-25 (UTC). Branch `insure-jstbonds-1`. Research only: fake
money, keyless data already cached (JST Macrohistory R6, data-long-4's copy), no change to the
gym, the daily runner or the live strategies. Card:
[`cards/insure-jstbonds-1.md`](cards/insure-jstbonds-1.md) (commit c6bffee, before any number);
amendment A with the holding-index fall counts and the chosen threshold (commit 31b8124, before
any rule position, insurance or share was read). Tables:
[`results/insure-jstbonds-1.md`](results/insure-jstbonds-1.md). Code: `lib/insurejstbonds1.py`
(reuses `insure1870`, `insure1`, `jstautocorr`, `jstautocorr2` unchanged), tests
`tests/test_insurejstbonds1.py`. Statistics only: JST R6 is CC BY-NC-SA 4.0 (recorded in
data-long-1 and data-long-4: non-commercial use with citation; cite Jorda, Schularick and
Taylor 2017 and Jorda, Knoll, Kuvshinov, Schularick and Taylor 2019); no raw data committed.

Suggested by insure-bonds-1 (PR #219) as "the natural next bond insurance check". No earlier
record scored JST `bond_tr` for insurance (jst-gates-1 used it as a regression outcome only).
R6 has bond returns for 16 countries, not 17: Canada and Ireland have none.

## The answer on one screen

**By the card: "Holds only as lower exposure" (weaker than claimed; handed back in the rebound;
cheaper than holding less, narrowly).** On 1,352 non-overlapping country-years (14 countries,
1871-2020, war, closure and hyperinflation years dropped) the annual rule lost less than holding
in 9 of 12 effective bond falls of 10%+ (anchored and linked clusters are the same here; sign p
0.011 on the 10 non-ties, bootstrap p 0.000). It shows **no timing**: per fall it avoided 0.70 of
the loss against 0.68 for the same exposure held fixed and 0.65 at random dates. That gap
(+0.04) is *below* the median gap of AR(1) worlds (+0.06; p 0.58) and of block-bootstrap worlds
(+0.09; p 0.68). The year-older signal control cannot be read, because the rule itself shows no
timing to remove. The kill reading on the card applies: **the JST bond data do not support
trend's timing on bonds.** Together with #182, #214 and insure-bonds-1, the bond line reads "lost
less in slow falls, as any lower exposure does; no timing evidence".

| Run (d = 10% unless stated) | Episodes | Anchored clusters lost less | Per episode: lost less / ties / n | S per episode: rule / fixed / random | Gap G | p AR(1) / BB | Premium rule / fixed | Verdict |
|---|---:|---|---|---|---:|---|---|---|
| **Primary: non-overlapping, undisrupted** | 23 | **9 of 12** | 13 / 4 / 23 | **0.70** / 0.68 / 0.65 | **+0.043** | **0.584 / 0.677** | 2.38 / 2.70 | **Holds only as lower exposure** |
| Check 1: overlapping years kept (16 countries) | 33 | 11 of 15 | 16 / 11 / 33 | 0.66 / 0.68 / 0.66 | +0.003 | 0.708 / 0.879 | 2.96 / 3.15 | Holds only as lower exposure |
| Check 2: disrupted years kept | 34 | 12 of 14 | 22 / 5 / 34 | 0.71 / 0.64 / 0.61 | +0.105 | 0.543 / 0.713 | 1.57 / 2.14 | Holds only as lower exposure |
| Check 3: events on the real index | 62 | 11 of 14 | 42 / 7 / 62 | 0.39 / 0.34 / 0.33 | +0.054 | 0.059 / 0.247 | 1.54 / 1.76 | Does not hold (linked 7 of 9, p 0.09) |
| Check 4: cash at 0 when out | 23 | 9 of 12 | 13 / 4 / 23 | (S anchored 0.50 / 0.39 / 0.36) | +0.002 | 0.502 / 0.644 | 17.6 / 17.5 | Holds only as lower exposure |
| Check 5a: d = 15% | 6 | 4 of 4 | 5 / 0 / 6 | | +0.237 | 0.209 / 0.413 | 3.63 / 4.99 | Too few falls |
| Check 5b: d = 7.5% | 44 | 15 of 21 | 25 / 8 / 44 | 0.89 / 0.77 / 0.74 | +0.151 | 0.052 / 0.105 | 1.82 / 2.05 | Holds only as lower exposure |
| Check 6a: primary, to 1965 | 15 | 6 of 8 | 10 / 3 / 15 | 0.70 (anch.) | +0.102 | 0.495 / 0.216 | 1.49 / 1.94 | Too few falls |
| Check 6b: primary, 1966-2020 | 8 | 3 of 4 | 3 / 1 / 8 | 1.34 (anch.) | -0.051 | 0.627 / 0.925 | 4.34 / 4.00 | Too few falls |
| Control: L1, signal t-1 (trimmed primary) | 20 | 9 of 11 | 11 / 3 / 20 | 0.69 / 0.71 / 0.69 | +0.000 | 0.754 / 0.878 | 2.63 / 2.94 | Holds only as lower exposure |
| Control: L2, signal t-2 (same years) | 20 | 8 of 11 | 14 / 1 / 20 | 0.78 / 0.72 / 0.68 | +0.107 | 0.122 / 0.220 | 3.21 / 2.97 | Does not hold |

(Rule: hold bonds in year t if `bond_tr` of year t-1 beat the bill, else bills; 2 bps a side.
Falls: zigzag 10% down / 10% up on each segment's year-end nominal total-return index. S = share
of the fall's log loss avoided; above 1 when bills earned while bonds fell. Gap G =
jst-autocorr-1's per-episode statistic (rule S minus mean S over rotations); p AR(1) / BB = share
of 1,000 worlds with at least the observed G; the card decides on the larger. "Lost less" counts
ties and the 2 bp entry cost against the rule. Premium = what the rule gave back in rebounds and
calm years per unit saved in falls. Full tables, every episode and the anchored clusters are in
the results file.)

- **Why d = 10%.** On the holding indices alone (amendment A), the primary has 2, 4 and 6
  bond falls at 25%, 20% and 15%, then 23 at 10% (12 anchored and 12 linked clusters, the first
  rung with at least 10 of each). Annual bond falls of crash size are almost absent: the two 25%
  falls are Portugal 1889-92 and 2009-11. A 10% fall of a bond index is a yield rise of a few
  points, not a crash.
- **Where it works: slow falls.** Of the 13 multi-year falls the rule lost less in 12 (I +5 to
  +55 log points; S 0.48-2.34). The one exception is the UK 1946-52 (-0.9). Examples: Portugal
  1889-92 (+55), France 1968-70 (+30), Spain 1976-79 (+36), Portugal 2009-11 (+39; but it lost
  59 in the rebound year).
- **Where it fails: one-year falls.** 10 of the 23 falls lasted one year. In 9 of them the rule
  was fully in, because the year before had been a good bond year: 4 exact ties and 5 that lost
  the 2 bp cost of re-entering in the fall year (Germany 1930-31 and Denmark, Spain, France and
  Italy 1993-94). The 1994 bond crash shows on year-end data as a one-year fall in 9 countries
  (with the overlaps), and the rule was in for every one. Only Finland 1947-48 (+19) was already
  out. This is the fast-fall failure of the equity record (1987, 2020), and here it is close to
  half the sample.
- **No timing, and not because of autocorrelation.** Unlike the early equity data, annual bond
  excess returns in the primary have no lag-1 autocorrelation (pooled -0.009; per country
  -0.21 to +0.17). So the AR(1) worlds are nearly iid, and their median gap of +0.06 comes from
  the fall definition alone, as stale-checks-1 and insure-1709-1 found. The rule's +0.04 sits
  below it. Per fall the rule avoids about what the same average exposure (59% in bonds)
  avoids: 0.70 against 0.68. On data this flat, a fixed 59% bond / 41% bill mix avoids two
  thirds of a 10% fall, because bills earn while bonds fall.
- **The anchored statistic looks better, and the card says why it does not decide.** Mean S
  over the 12 anchored clusters is 0.91 against 0.68 fixed and 0.61 at random dates (rotation p
  0.081). The difference from the per-episode figure is the 1993-94 cluster: its five falls (one exact tie, four that lost the 2 bp
  entry cost) count once as a cluster but five times per episode. Rotations are description only on this sample
  (pooled, starting before 1966, #204's rule), and the decisive AR-preserving nulls are run on
  the per-episode gap.
- **Check 2 shows what a rotation null would have claimed.** With the war and hyperinflation
  years kept, the rotation p falls to 0.010, but the AR and block-bootstrap nulls give 0.54 and
  0.71: the observed gap (+0.105) equals the AR worlds' median (+0.112).
- **Handed back.** Net of the year after the trough, 7 of 12 clusters are above zero (sign p
  0.39). The calm drag is small (-0.36 log points a year with cash at bills). The premium (2.38)
  is slightly below holding less (2.70), so it is narrowly "cheaper than holding less". With
  cash at 0 that goes (17.6 against 17.5; calm drag -2.5 a year): with cash at 0, being out of
  bonds forgoes the coupon, as insure-bonds-1 found.
- **The year-older signal control (stale-checks-1 (b)).** On the trimmed primary the t-1 rule
  shows no timing (G +0.000, p 0.75 / 0.88), so the card's reading is "in between / not read":
  there is nothing for a year-older signal to remove. With the t-2 signal the insurance count
  itself fails (8 of 11, sign p 0.11), and its anchored S (0.65) is below fixed exposure
  (0.72). Its per-episode gap is larger (+0.107, p 0.12 / 0.22) only because a two-year-old
  signal is out in a few one-year falls by chance (1 tie against 3). That is not timing. Same on
  check 1: L1 G -0.023, L2 +0.002.
- **With and without overlapping country-years.** The overlaps are all US and Norwegian years,
  UK 1867-1926 and 1960 on, Australia 1969 on, Switzerland 1955 on, Germany 1956 on, Japan 1989
  on and Sweden 1986 on (`datawide2.SEEN` plus insure-bonds-1). Adding them (check 1: 1,998
  country-years, 16 countries) adds 10 falls: 3 slow ones that lost less (US 1966-69, UK 1959-61
  and 1971-74), the 1993-94 ties in four more countries, and the one-year ties US 2008-09, US
  2012-13 and Australia 1972-73. Lost less 11 of 15 (sign p 0.003); timing G +0.003, p 0.71 /
  0.88. Same verdict.
- **Per country (description).** Twelve of the 14 primary countries have 1-4 falls each;
  Switzerland (to 1954) and Japan (to 1988) have none. Netherlands (1 fall, AR p 0.042) and
  Portugal (3, p 0.079) are the only countries below 0.10. With 12 countries tested that is
  about what chance gives. No country verdict.

## How sure

- **Card before numbers, threshold from holding counts only.** One configuration decides;
  nothing tuned. The threshold rule was on the card before any count, and d was pushed before
  any rule position was read. Checks 5a and 6 read "Too few falls", as amendment A expected for
  5a.
- **Few falls.** 12 effective falls (10 non-ties) in the primary, and most clusters hold one
  country. The insurance sign test (p 0.011) is robust across checks except check 3 (real
  index: linked p 0.09). The timing reading is not close: no decisive null p is below 0.5 in the
  primary or check 1. The closest any reading comes is check 5b (7.5%: p 0.052 / 0.105), still
  above the card's 0.10 on the larger p.
- **The nulls are too narrow (stated on the card).** Neither keeps the cross-country
  co-movement of falls. That errs toward "timing shown", so it does not weaken a "no timing"
  reading. The block bootstrap's median gap (+0.09) is above the AR(1)'s (+0.06) because it keeps
  fat tails and each segment's drift.
- **The tie rule.** insure-bonds-1's bug (I about 1e-14 when the rule stays in) is handled by
  setting |I| < 1e-9 to 0 (tested). A fall where the rule re-enters in the fall year loses
  exactly the 2 bp entry cost. Like insure-1870-1, it counts as a loss, not a tie. Counted as
  ties instead, the primary sign test would be 9 of 9 non-zero anchored clusters, which is no
  change to the verdict.
- **Annual data hide the fast falls.** A fall that recovers within a calendar year never shows
  (most of 1994's intra-year fall, for example). On annual data a one-year fall is a tie by
  construction. The card stated both biases before the numbers. They push the headline share
  down (9 of 12 = 0.75, "weaker than claimed") and the share among multi-year falls up.
- **Disrupted-year rule borrowed from equities.** jst-autocorr-2's war, closure and
  hyperinflation spans were written for share markets and are applied to bonds unchanged
  (card). Keeping them (check 2) gives the same verdict.
- **Not the gym's rule.** Calendar-year decisions on the excess over bills, cash earning bills.
  The weekly `tsmom12` (price above a year ago, cash at 0) is not replayed. Check 4 gives the
  cash-at-0 reading.
- Not a pick. The project bar (`research/register/BAR.md`, N_eff 509, z 4.70) is quoted for
  scale only. No gate id was taken.

## What it adds to the SUMMARY claim

Proposed wording (for the summary lane): "On JST annual government-bond returns (14 countries,
1871-2020, years no record had scored), the annual trend rule lost less than holding in 9 of 12
bond falls of 10%+. The 12 of 13 slow falls account for that. In one-year falls such as 1994 it
was fully in. It shows no timing: per fall it avoided 0.70 of the loss against 0.68 for the same
exposure held fixed, below what AR(1) and block-bootstrap worlds give (p 0.58 / 0.68). On bonds
the insurance is what holding less gives (#PR)." Nothing changes for the live rule.

## Logged

`tries.md`: 26 rows of kind `insure-check`, idea `insure-jstbonds-1`: 14 per-country rows for
the primary countries (`tsmom12a@insure-jstbonds-<ISO>`; annual Sharpe = mean / sd of the rule's
annual returns, total return, worst year-end drawdown, flips a year), 8 check rows and 4
year-older-control rows (L1 and L2 on the primary and on check 1). Rotations, null worlds
and the fixed control are re-scorings and get no rows. No download: everything was in the
local cache.
