# insure-1870-1: does trend's crash insurance hold on 1870-1965 annual data?

Lane `insure-1870-1`, 2026-11-25 (night of 2026-11-24). Branch `insure-1870-1`, PR #186.
Research only: fake money, keyless data already cached (JST Macrohistory R6, via data-long-4's
loader), no change to the gym, the daily runner or the live strategies. Card:
[`cards/insure-1870-1.md`](cards/insure-1870-1.md) (pushed before any number). Tables:
[`results/insure-1870-1.md`](results/insure-1870-1.md). Code: `lib/insure1870.py`, tests
`tests/test_insure1870.py`. Statistics only (JST is CC BY-NC-SA 4.0; cite Jorda, Schularick and
Taylor 2017); no raw data committed.

## The answer on one screen

**Yes: on data the claim never saw (US 1873-1926, 15 other countries 1871-1965, 1,264
country-years) the annual trend rule lost less than holding in every one of 9 effective falls
of 25%+ (9 of 10 under strict linking), avoided 0.73 of each fall against 0.47 at random dates
(p 0.020), and bought that at a premium of 1.17 against 2.23 for simply holding less. By the
card's rule: "Holds", at the claimed strength, handed back in the rebound, "timing, not just
exposure". The failure mode is the same as on daily data: it insured all 32 multi-year falls
and none of the 6 one-year falls. The US alone adds almost nothing: before 1927 it has one
25% year-end fall (1907), and the rule sat through it.**

| Run (25% falls unless stated) | Episodes | Effective falls lost less (anchored; linked) | Share avoided: rule / fixed / random (p) | Premium: rule / fixed / random | Calm drag a year | Verdict |
|---|---:|---|---|---|---:|---|
| **Decisive: US to 1926, others to 1965** | 38 | **9 of 9; 9 of 10** | **0.73** / 0.51 / 0.47 (0.020) | **1.17** / 2.23 / 2.89 | -1.0 | **Holds** |
| Full span 1870-2020 (overlaps seen data) | 99 | 17 of 17; 14 of 14 | 0.70 / 0.56 / 0.50 (0.024) | 1.27 / 1.75 / 2.28 | -1.7 | Holds |
| Events on the real index | 51 | 11 of 11; 7 of 7 | 0.45 / 0.32 / 0.28 (0.000) | 1.19 / 2.35 / 3.17 | -1.1 | Holds |
| 20% fall / 20% rise | 48 | 14 of 15 | 0.73 / 0.53 / 0.48 (0.016) | 1.16 / 2.08 / 2.63 | -1.1 | Holds |
| 40% fall / 25% rise | 18 | 8 of 8 | 0.80 / 0.50 / 0.43 (0.014) | 1.26 / 2.93 / 4.04 | -0.9 | Holds (kept) |
| Cash at 0 when out | 38 | 9 of 9 | 0.60 / 0.41 / 0.38 (0.020) | 2.49 / 4.46 / 5.50 | -2.3 | Holds |
| Years with CPI > 50% dropped | 32 | 9 of 9 | 0.76 / 0.50 / 0.44 (0.036) | 1.12 / 2.31 / 2.84 | -1.1 | Holds |

(Rule: hold equities in year t if the equity total return of year t-1 beat the bill, else
bills; 2 bps a side. Share avoided can exceed 1: the rule earned bills while holding fell.
Calm drag: rule minus holding, log points per calm year. "Lost less": I > 0, ties counted
against. p: share of 1,000 common rotations of the positions with a share at least as large.)

- **The insurance holds out of sample.** Sign test on the 9 anchored clusters p 0.002, on 10
  linked clusters p 0.011, cluster bootstrap p 0.000 for both; mean insurance +38 log points
  per fall. Every check passes the same way, and the order rule < fixed exposure < random
  timing for the premium holds in all seven runs (p_P 0.000 everywhere).
- **Same weakness as on daily data, seen more starkly.** Per episode the rule lost less in 32
  of 38 falls; the 6 others are all one-year falls (US 1907, Germany 1918, Netherlands 1941,
  Italy 1945 and 1947, Japan 1950), where a once-a-year rule is fully in and loses exactly as
  much as holding (4 exact ties, 2 losing only the 2 bp entry cost). The anchored count (9 of 9)
  averages those into clusters with multi-year falls, so the cluster figure flatters a little;
  the per-episode 0.84 is the plainer number. On the full span: 76 of 99, 20 ties.
- **Handed back, partly.** Net of the year after the trough the mean is positive (+13 log
  points, bootstrap p 0.04), but only 6 of 9 clusters are above zero (sign p 0.25), so by the
  card's rule "handed back in the rebound", as insure-2 found everywhere. Built in: after a down
  trough year the annual rule always misses the whole first rebound year (B -8 to -91 log
  points after the one-year falls). Only the 40% falls keep it (7 of 8 net positive, p 0.035).
- **What it costs.** Premium 1.17 (insure-1 on US 1927-1961: 0.85; since 1962 about 1.35),
  calm-year drag about 1 log point a year with cash at bills and 2.3 with cash at 0
  (insure-2: about 2 since 2002, cash at 0). Holding less (fixed 62% in equities) would have
  cost about twice as much per unit of loss avoided (2.23), random timing about 2.5 times (2.89).
- **US before 1927: no evidence.** On year-end closes the US index had one fall of 25%+ in
  1873-1926 (1906-07, -29%); the worst other years (1917 -24%, 1920 -18%, 1893 -15%) stay below
  25% at year end. The rule
  was fully in for it (I = 0). The out-of-sample support is almost entirely non-US.
- **For the SUMMARY claim.** It can now cite out-of-sample support: 15 countries and 95 years
  the claim never saw, at annual resolution, agree on the insurance, on the timing (beats random
  dates) and on the premium order (cheaper than holding less). Nothing changes for the live rule.

## How sure

- Card pushed before any number; one configuration decides; nothing tuned. Not a pick: the
  project bar (Bonferroni p <= 4.5e-05 at N 1,099) is quoted for scale; the decisive sign test
  (p 0.002) does not reach it, the full-span one (7.6e-06) does but overlaps the data the claim
  was built on.
- **Few independent falls.** 9 effective falls, and two of them (1917-1923 and 1927-1935) hold
  20 of the 38 episodes: the world wars, the post-war deflation and the Depression move all
  countries together. Anchoring on US falls (insure-geo's method) and strict linking agree
  (9 and 10 clusters).
- **Annual data biases this both ways (card, written before the numbers).** Intra-year falls
  that recover by December are invisible (1987-type, where trend fails on daily data): biases
  the share up. One decision a year means one-year falls are ties: biases it down. As predicted,
  the ties appeared (6 of 38 episodes), but clustering absorbed them, so the headline came out
  above the card's expectation (0.5-0.7 with ties against; got 1.00 per cluster, 0.84 per
  episode).
- **The placebo is coarse.** Rotations shift whole years (offsets 1 to 93), so the null keeps
  the rule's spell lengths but has only 93 distinct offsets; p_S 0.020 is a granular estimate, the
  weakest number of the result. The cash-at-0 and hyperinflation checks give 0.020 and 0.036.
- **Data.** JST annual equity total returns are year-end to year-end, nominal, local currency,
  from national sources of mixed quality before 1914 (some indices thin or interpolated in
  early years and in wars); bill returns are missing in several war years (segments split
  there). Germany's 1921-1922 hyperinflation years stay in the primary sample (check 5 drops
  them: same verdict).
- **Not the gym's rule.** Calendar-year decisions, excess over bills, cash earning bills; the
  weekly `tsmom12` (price above a year ago, cash at 0) is not replayed here.

## Logged

`tries.md`: 22 rows of kind `insure-check`, idea `insure-1870-1`: 16 per country
(`tsmom12a@insure-1870-<ISO>`, decisive sample; Sharpe = mean / sd of annual rule returns,
Turnover = flips a year, Max DD on year-end equity) and 6 pooled check rows. The placebo and
fixed controls are re-scorings (no rows).
