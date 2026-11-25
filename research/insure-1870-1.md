# insure-1870-1: does trend's crash insurance hold on 1870-1965 annual data?

Lane `insure-1870-1`, 2026-11-25 (night of 2026-11-24). Branch `insure-1870-1`, PR #186.
Research only: fake money, keyless data already cached (JST Macrohistory R6, via data-long-4's
loader), no change to the gym, the daily runner or the live strategies. Card:
[`cards/insure-1870-1.md`](cards/insure-1870-1.md) (pushed before any number). Tables:
[`results/insure-1870-1.md`](results/insure-1870-1.md). Code: `lib/insure1870.py`, tests
`tests/test_insure1870.py`. Statistics only (JST is CC BY-NC-SA 4.0; cite Jorda, Schularick and
Taylor 2017); no raw data committed.

## The answer on one screen

**Yes, but narrowly on timing. On data the claim never saw (US 1873-1926, 15 other
countries 1871-1965, 1,264 country-years) the annual trend rule lost less than holding in 9 of
9 effective falls of 25%+ (9 of 10 under strict linking): all 31 multi-year falls and 1 of the
7 one-year falls. Those are 9 effective falls, but about 7 independent world events (with the
First World War and its aftermath merged, and the Second World War merged: 7 of 7, p 0.008).
The US contributes one fall, a tie: the rule missed 1907. "9 of 9" says nothing about timing,
since a fixed 62% exposure also scores 9 of 9 (38 of 38 episodes). The evidence for timing is
the share avoided, 0.73 against 0.51 fixed and 0.47 at random dates (p 0.020, 2 of 93
offsets), and the premium, 1.17 against 2.23 for simply holding less. By the card's rule:
"Holds" (narrowly on timing), at the claimed strength, handed back in the rebound, "timing, not
just exposure".**

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

- **The insurance holds out of sample.** The sign test gives p 0.002 on the 9 anchored
  clusters and p 0.011 on the 10 linked clusters; the cluster bootstrap gives p 0.000 for both.
  Mean insurance is +38 log points per fall. Every check passes the same way, and the premium
  order rule < fixed exposure < random timing holds in all seven runs (p_P 0.000 everywhere).
- **Losing less is not the evidence; timing is.** With bills earning a positive return, any
  exposure below 100% loses less in a fall. A fixed 62% equity share loses less in 9 of 9
  clusters and 38 of 38 episodes (the rule: 32 of 38), and 13 of 93 rotation offsets (14%) also
  score 9 of 9. What separates the rule from holding less is how much of each fall it avoids:
  S 0.73 against 0.51 fixed and 0.47 random (p 0.020: 2 of 93 offsets do as well), and what it
  pays for that: premium 1.17 against 2.23 fixed and 2.89 random. p_S is the weakest number of
  the result.
- **Same weakness as on daily data, seen more starkly.** Per episode the rule lost less in 32
  of 38 falls: all 31 multi-year falls and 1 of the 7 one-year falls (Germany 1924-25, where
  1924 had already lost to bills). The other 6 one-year falls (US 1907, Germany 1918,
  Netherlands 1941, Italy 1945 and 1947, Japan 1950) are ones where a once-a-year rule is fully
  in and loses exactly as much as holding (4 exact ties, 2 losing only the 2 bp entry cost).
  The anchored count (9 of 9) averages those into clusters with multi-year falls, so the
  cluster figure flatters a little; the per-episode 0.84 is the plainer number. On the full
  span: 76 of 99, 20 ties.
- **Handed back, partly.** Net of the year after the trough the mean is positive (+13 log
  points, bootstrap p 0.04), but only 6 of 9 clusters are above zero (sign p 0.25). By the
  card's rule that is "handed back in the rebound", as insure-2 found everywhere. The cause is
  built in: after a down trough year the annual rule always misses the whole first rebound year
  (B -8 to -91 log points after the one-year falls). Only the 40% falls keep it (7 of 8 net
  positive, p 0.035).
- **What it costs.** The premium is 1.17 (insure-1 on US 1927-1961: 0.85; since 1962 about
  1.35). Calm-year drag is about 1 log point a year with cash at bills and 2.3 with cash at 0
  (insure-2: about 2 since 2002, cash at 0). Holding less (a fixed 62% in equities) would have
  cost about twice as much per unit of loss avoided (2.23), random timing about 2.5 times (2.89).
- **US before 1927: no evidence.** On year-end closes the US index had one fall of 25%+ in
  1873-1926 (1906-07, -29%). The worst other years (1917 -24%, 1920 -18%, 1893 -15%) stay below
  25% at year end. The rule was fully in for 1907 (I = 0). Only 1 of the 9 anchored clusters
  (1906-08) has a US member, and that member is this tie. The out-of-sample support is non-US.
- **For the SUMMARY claim.** It can now cite out-of-sample support: 15 countries and 95 years
  the claim never saw agree at annual resolution on the insurance and on the premium order
  (cheaper than holding less). On timing (beating random dates) the support is narrow
  (p 0.020). Nothing changes for the live rule.

## How sure

- Card pushed before any number; one configuration decides; nothing tuned. Not a pick: the
  project bar (Bonferroni p <= 4.5e-05 at N 1,099) is quoted for scale; the decisive sign test
  (p 0.002) does not reach it, the full-span one (7.6e-06) does but overlaps the data the claim
  was built on.
- **Few independent falls.** There are 9 effective falls, and two of them (1917-1923 and
  1927-1935) hold 20 of the 38 episodes: the world wars, the post-war deflation and the
  Depression move all countries together. Merging WWI with its aftermath (1917-23 and 1924-26)
  and WWII (1936-41 and 1942-50) leaves 7 events, 7 of 7 insured (sign p 0.008). Strict linking
  gave 10 clusters against 9 anchored, so on this data "strict" was not the more conservative
  count the card expected (the US anchors are long and absorb more episodes).
- **Annual data biases this both ways (card, written before the numbers).** Intra-year falls
  that recover by December are invisible (1987-type, where trend fails on daily data): biases
  the share up. One decision a year means one-year falls are ties: biases it down. As predicted,
  the ties appeared (6 of 38 episodes), but clustering absorbed them, so the headline came out
  above the card's expectation (0.5-0.7 with ties against; got 1.00 per cluster, 0.84 per
  episode).
- **The placebo is coarse, and errs toward caution.** Rotations shift whole years: one
  common offset k of 1 to 93, each segment rotated by k mod its length. So there are only 93
  distinct nulls, and the smallest p it can give is about 0.011 (1 of 93). p_S 0.020 means 2 of
  the 93 offsets (84 and 85) reach the rule's share. In those two draws some segments are not
  really rotated. At offset 85, Australia and Japan 1949-65 and Portugal keep their own timing
  (shift 0), while France and Italy 1923-65 are shifted to L-1, i.e. they use the next year's
  position, which is decided by that year's own return: same-year look-ahead. Offset 84 does
  the same for Australia, Japan 1949-65 and Portugal (L-1) and Norway (0). The offsets that beat the rule
  therefore partly embed the rule's own timing or look-ahead, so the placebo errs toward caution.
  The cash-at-0 and hyperinflation checks give 0.020 and 0.036.
- **Data: year-end prices, but some early indices may be smoothed.** Jorda et al. (2019, "The
  Rate of Return on Everything, 1870-2015", QJE 134(3); NBER w24112 rev. May 2019, section on
  "Temporal aggregation and return averaging") state that "the equity prices used for return
  calculations, by the usual convention followed here, ... compare end-of-year prices of
  shares." So JST equity returns are year-end to year-end by convention, nominal, local
  currency. The per-country data appendix (where exceptions would be listed) could not be
  fetched (HTTP 403) and was not checked. A note on the data: the lag-1 autocorrelation of
  annual log returns (pairs of consecutive scored years within segments) is 0.19 in the
  decisive sample (0.19 over bills), against 0.04 after 1965. It is high in Norway 0.40,
  Germany 0.38, Portugal 0.36, Sweden 0.35 and Belgium 0.32, and low in the US (-0.06). Positive
  autocorrelation is what partly time-averaged or stale early indices would show; it helps a
  last-year rule and would bias S up. Sources are national, of mixed quality before 1914 (some
  indices thin or interpolated in early years and in wars). Bill returns are missing in several
  war years (segments split there). Germany's 1921-1922 hyperinflation years stay in the primary
  sample (check 5 drops them: same verdict).
- **Not the gym's rule.** Calendar-year decisions, excess over bills, cash earning bills; the
  weekly `tsmom12` (price above a year ago, cash at 0) is not replayed here.

## Logged

`tries.md`: 22 rows of kind `insure-check`, idea `insure-1870-1`: 16 per country
(`tsmom12a@insure-1870-<ISO>`, decisive sample; Sharpe = mean / sd of annual rule returns,
Turnover = flips a year, Max DD on year-end equity) and 6 pooled check rows. The placebo and
fixed controls are re-scorings (no rows).
