# insure-bonds-1: does trend's crash insurance hold on long government-bond histories?

Lane `insure-bonds-1`, 2026-11-25 (UTC). Branch `insure-bonds-1`. Research only: fake money,
keyless public data, no change to the gym, the daily runner or the live strategies. Card:
[`cards/insure-bonds-1.md`](cards/insure-bonds-1.md) (commit 422f648, 22:54 UTC, before any
number on these series). Before-scoring table and card amendment A: commit 3078c29 (22:59),
before any rule position, episode or outcome was read. (The amendment's heading time in the
card was corrected from "~23:15" to "22:56-22:59" in the run commit fb8f673, after the
results: a cosmetic edit of the time stamp only.) Tables:
[`results/insure-bonds-1.md`](results/insure-bonds-1.md). Code: `lib/insurebonds1.py` (reuses
`insure1709` and `insure1` unchanged), tests `tests/test_insurebonds1.py`. Data: Norges Bank
Historical Monetary Statistics (Klovland 2004 in Eitrheim, Klovland and Qvigstad 2004; short
rates: Eitrheim and Klovland 2007) and the Bank of England's "A millennium of macroeconomic
data" v3.1, read locally; only statistics are committed. Contains public sector information
licensed under the Open Government Licence v3.0.

## The answer on one screen

**The card's answer is "Too few falls" for both series: bond total-return indices rarely fall
10%. With the threshold lowered to 5% (amendment A, fixed before any outcome), the evidence is
split, and it adds no timing support. On UK consols 1867-1926 the rule lost less than holding in
9 of 10 falls and tied the tenth (sign p 0.002), but its share avoided is only "in between" random dates (p_rot
0.069; AR nulls p 0.07-0.10). On Norwegian government bonds 1823-1984 (the amendment's
primary) it does not hold: it lost less in 4 of 11 falls (sign p 0.34). Five of the 11 are
one-month falls, where the rule was in and lost the same as holding. In both series it handed
the saving back in the rebound (net N > 0 in 1 of 10 and 3 of 9 falls with N != 0).**

| Reading | Falls (size) | Lost less | S: rule / fixed / random (p_rot) | Gap G; p AR1 / BB | Premium rule / fixed | Verdict |
|---|---:|---|---|---|---|---|
| **Card: Norway, 10-year par bond, 1823-1984** | 2 (10%) | 1 of 2 | 0.39 / 0.15 / 0.00 (0.19) | +0.25; not run | 8.0 / 14.2 | **Too few falls** |
| **Card: consols, perpetuity, 1867-1926** | 4 (10%) | 4 of 4 (p 0.063) | 0.45 / 0.24 / 0.19 (0.14) | +0.23; not run | 2.3 / 3.0 | **Too few falls** |
| A1: Norway, par bond (amendment primary) | 11 (5%) | **4 of 11** (p 0.34) | 0.21 / 0.14 / 0.09 (0.16) | +0.09; 0.66 / 0.13 | 4.3 / 4.8 | **Does not hold** |
| A2: consols, perpetuity | 10 (5%) | **9 of 10**, 1 tie (p 0.002) | 0.42 / 0.24 / 0.20 (0.069) | +0.20; 0.073 / 0.097 | 1.9 / 2.3 | **In between** |
| A3: Norway, perpetuity | 9 (15%) | 5 of 9 (p 0.11) | 0.34 / 0.27 / 0.24 (0.22) | +0.09; 0.57 / 0.34 | 2.2 / 3.0 | Does not hold |

(Rule: at each month-end, hold the bond total-return index next month if its 12-month log
change is above 0, else cash at 0; 2 bps a side. S = share of the fall's log loss avoided.
Sign p: one-sided, ties dropped; "lost less" counts ties against. p_rot: share of 1,000 random
rotations of the positions with mean S at least the rule's. AR1/BB: share of 1,000 synthetic
worlds whose gap G is at least the observed one. "Premium" = what the rule gave back in
rebounds and calm years per unit saved in falls.)

- **Why so few falls.** A 10-year par bond rebuilt from Norway's yields fell 10% or more twice
  in 162 years (1939-40, and a one-month jump in 1979). The consol perpetuity, with about three
  times the duration, fell 10% four times in 60 years (the Boer War 1899-1901, 1914-17, 1918-19,
  1919-20). Coupons of 3-5% a year offset most yield rises. The card's ladder (25% down to 10%)
  was set for share-like falls and was too coarse for bonds. That is a design miss of the card,
  stated as such.
- **Where it works: slow yield rises.** Consols: every fall from 1884 to 1920 was a slow rise
  in yields (7-32 months), except 1918-19 (4 months) and a one-month fall in 1922 (a tie). The
  rule avoided 0.24-1.00 of each slow fall; 1918-19 only 0.04. Norway: the slow falls 1919-20 (S 0.67), 1939-40 (0.75)
  and 1954-56 (0.29) all lost less; so did the one-month fall of 1940-04..05 (S 1.00: the rule
  was already out at the invasion month, after the slow 1939-40 fall). With
  a perpetuity, Norway's slow falls 1949-51 and 1954-56 lost less with S 0.82-0.91.
- **Where it fails: one-month jumps.** Norway's 1946-1984 yields were administered and moved in
  steps. In 1969, 1974, 1977 and 1979 the yield jumped 1.2-2.0 points in one month and stayed
  there (for example 7.48% to 9.01% from 1977-11 to 1977-12), after months of almost no change.
  The 1931-09 fall (sterling left gold) was also a single month. A monthly 12-month rule is
  always in before such a jump: I = 0, a tie, counted against the rule. Five of A1's 11 falls
  are of this kind. The two other losses are 1825-26 (the rule lost 2 log points more) and
  1980-81 (0.02 log points more: about one trade's cost of 2 bps). This matches the equity record, where trend fails in fast falls (1720, 1987),
  but here the fast falls are half the sample.
- **Timing: not shown on any reading.** No reading has p_rot < 0.05. Consols come closest:
  S 0.42 against 0.24 for the same average exposure and 0.20 at random dates (p_rot 0.069). Its
  gap G = +0.20 is at the 93rd percentile of AR(1) worlds and the 90th of block-bootstrap
  worlds. Lag-1 autocorrelation is small in every source period except Norway's 1822-1842
  quotations abroad (+0.13, with 23% unchanged-yield months: "stale-suspect") and the 1940-45
  occupation (-0.26), and consols 1914-26 (-0.13). So the AR nulls hardly differ from the iid
  reference here. The AAFT surrogates (whole spectrum kept) give consols p 0.028, the only null
  below 0.05; it is description by the card, not decisive, and it is not a pass. Unlike the
  equity series, autocorrelation is not what keeps the bond timing from passing: the effect is
  small and the falls are few.
- **The insurance is handed back.** In both series most of the saving goes in the 12 months
  after the trough: N > 0 in 1 of the 10 Norwegian and 3 of the 9 consol falls where N != 0. The rule's premium
  is above 1 in every primary reading (1.9-8.0): with cash at 0 it trails holding over the
  whole span, partly because being out forgoes a 3-5% coupon. It is still cheaper than holding
  the same average exposure fixed (premium below the fixed one in all five readings).

## How sure

- **Few falls, and the threshold was moved.** The card's verdicts are "Too few falls", and
  they stand. The 5% readings come from amendment A, which was pushed after the fall counts
  (these depend only on the holding index) and before any rule position was read. That keeps
  them free of the outcome, but they are a second choice, and the amendment states it. With
  10-11 falls the sign test can reach p 0.001. No p here comes near the project bar
  (`research/register/BAR.md`, rows through 2026-11-25 22:31: N 1,123 for a new pick), and none
  needs to: this checks a descriptive claim. It is not a pick.
- **A 5% bond fall is not a crash.** It is a yield rise of roughly 0.7-1 point net of coupons.
  These readings ask whether the insurance shows in bond bear markets, not in crashes of the
  size behind the SUMMARY claim (25%+ equity falls).
- **The total returns are rebuilt, not observed.** Norway's are a constant-maturity 10-year par
  bond repriced monthly from A4's yield (data-long-3's method). The real loans of the 1800s were
  long amortising loans whose duration is not documented here. The perpetuity (check 2 and A3)
  is the long-duration bound. It gives more falls: 16 at 10%, where the rule lost less in 10
  and tied 6 (sign p 0.001 on the 10 non-zero), with S 0.42 against 0.26 fixed and 0.23 random (p_rot 0.051). That reading is
  "between" in timing too. It also counts the regulated-era jumps as falls, which the rule
  ties. Consols are a perpetuity in fact, but callable after Goschen's conversion. The pricing
  ignores the call, so it overstates price rises near par in the 1890s.
- **Price-only consols show no timing**, as insure-1709-1 found for 1754-1866. On price alone
  (1/y), at 5%, the rule lost less in 14 of 15 (one tie), but S 0.59 against 0.51 fixed and 0.50 random
  (p_rot 0.19). Total return adds the coupon to both sides, which changes the signal and the
  fall set (10 falls instead of 15).
- **The consol series has one splice inside the window.** The spliced BoE yield matches
  Klovland's Goschen-corrected series (last Friday of the month) from 1866-01 to 1914-07 and
  Capie and Webber's from 1915-02 ("mixture of end month and averages"). Neither matches during
  the 1914-08..1915-01 exchange closure. Six of the ten consol falls lie in the Klovland part.
- **Norway's data have gaps and a regime.** A4 has no monthly values for 1843-1844 (the
  documented interpolation concerns the annual averages, so check 6 is void), 1845-01..10,
  1848-04..09 and 1914-09. The 1845-1848 run is too short and is dropped, so 1845-1849 is not
  scored. 1822-1914 is almost free of falls: one 5% fall in 92 years (1825-26, where the rule
  lost more). All of A1's other falls are after 1919. A1 GOV (another construction, 1820-1920)
  has 2 falls at 5%. So the Norwegian reading is mostly 1919-1984, and half of that is the
  regulated era.
- **Cash at 0 vs a discount rate.** With cash at the central-bank discount rate when out, the
  rule's premium falls below 1 for consols (0.88) and Norway's perpetuity (0.72): cash earning
  interest makes being out nearly free. This check is biased toward the rule (holding then
  earns the coupon and the rule the bill rate) and is shown for completeness. The insurance
  counts barely change (A1 4 of 11, A2 9 of 10).
- **Stale check.** With the signal a month older, consols keep their timing and the gap even
  rises (S 0.49, p_rot 0.031, G +0.26; null not run, not on the card). So the consol timing is
  not a one-month stale-price effect. Norway: 5 of 11, S 0.21 unchanged.
- **Sub-periods.** Norway 1915-1984 alone: 4 of 10, S 0.27 / 0.15 / 0.10 (p_rot 0.092).
- **Overlaps.** Norway 1822-1866 shares the calendar with insure-1709-1's consols (price only).
  1871-1984 shares it with the US bond calendar (`SEEN` bond USA from 1871). Norway's own bond
  market is scored only from 1985 (data-long-3), so every Norwegian month here is new for that
  market. Consols 1867-1926 are new for UK government bonds (`SEEN` GBR from 1960; JST's annual
  UK bond returns from 1870 were unscored at the time of writing; see insure-jstbonds-1). The 1866 consol months only warm up the signal. The
  pooled description has one shared cluster (1919-20, both series).
- Not used: Hypotekbank (state mortgage bank) bonds 1851-1920; A3 maturities (overlap A4 from
  1921); SNB Swiss bond indices (cached; 1924-1954 is unscored for Switzerland but needs a
  yield-to-price splice in 1943); JST annual bond returns (annual; taken up by
  insure-jstbonds-1).

## What it adds to the SUMMARY claim

Proposed wording (for the summary lane): "On long government-bond histories the insurance shows
only where bond falls are slow: UK consols 1867-1926 lost less in 9 of 10 falls of 5%+ (one tie), with
timing between random and significant (p_rot 0.07). Norwegian bonds 1823-1984 lost less in only
4 of 11, because half their falls were one-month jumps of administered yields (#PR). Bond falls
of 10%+ are too rare in these data for the card's test." Nothing changes for the live rule.

## A bug found in the shared scoring code (for the lead)

When the rule is in throughout a fall (a one-month fall, no flip), `insure1.score`'s
cumulative sum of log differences leaves I at about 1e-14 instead of 0. `insure1.sign_test`
(drops only exact zeros) and `insure1709.Eval.k` (I > 0) then count that tie as a win or a
loss at random; the rebound B and so N = I + B carry the same noise. In this lane's first
run (fb8f673) it moved several rows: A2 10 of 10 (now 9 of 10), A3 6 of 9 (now 5 of 9), check 2
at 10% 13 of 16 (now 10 of 16), consols price-only 15 of 15 (now 14 of 15), the cash-rate rows,
and the pooled clusters 13 of 15 (now 12 of 14). The second fix (zeroing B and the cash-rate N
too, after the lead's review) moved N: A1 2 of 11 to 1 of 10 non-zero, A2 3 of 10 to 3 of 9,
Norway's cash-rate N 5 to 4 of 11. This lane zeroes |I|, |B|, |I_cash| and |N_cash| below 1e-9
in its own wrapper (`insurebonds1.evaluate`, tested), and every number above uses it;
`insure1` and `insure1709` are unchanged here. Earlier equity lanes **are** affected, per the
lead's review: insure-1 (#87) 48 of 50 becomes 47 of 50 with ties counted against (a 2010
durable-goods tie had counted as a win), insure-2 (#90) wider set 15 of 17 becomes 13 of 17. No
verdict changes; insure-1870-1 is unaffected (its difference is exactly 0). The shared fix and
the regeneration are in eng-nits-1 (#218).

## Logged

`tries.md`: 1 `note` row (the before-scoring table) and 19 `insure-check` rows, idea
`insure-bonds-1`, variants `tsmom12m@insure-bonds-*`: two card readings, three amendment
readings and 14 checks (the two card check 1 rows, `...-cash-discount-rate`, carry the Sharpe
with cash at the discount rate when out). In the run commit, checks 3, 5, 7 and 8 were run at
A1/A2's 5% instead of the card's 10% (at 10% they have 0-2 falls); check 2 stays at 10%. Sharpe = mean / sd of monthly rule returns x sqrt(12), cash at 0. Several
rows share one return series: the threshold only changes the episodes, not the rule, so the
Sharpe columns repeat. Rotations, null worlds and the fixed control are re-scorings and get no
rows. No gate id was taken. Download: Norges Bank `shortterm_ir.xlsx` (338 KB, once, robots.txt
read: crawl delay 5 s kept, generic User-Agent) into the local data cache. Everything else was
already cached (`bond_yields.xlsx` by data-wide-2, the BoE CSV and workbook by
jst-autocorr-2 and insure-1709-1).
