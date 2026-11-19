# insure-2: is trend's crash insurance cheaper than holding less, per era and outside the US?

Lane insure-2, 2026-11-18 (night). Branch `insure-2` (from `insure-1`), draft PR #90. Research
only: fake money, keyless public data, no change to the gym, the daily runner or the live
strategies. Held-out year untouched (nothing after 2025-10-31 parsed). Tables:
`results/insure-2.md`. Code: `lib/insure2.py` (reuses `lib/insure1.py`; nothing replayed).

## The answer on one screen

**Trend's crash insurance is a robust property: across 98 years of US stocks and about 35 years
of 23 other markets it avoids about half of each 25%+ fall, and it buys that loss avoided more
cheaply than simply holding less. But it is not free and not an edge: the year after the low
hands most of it back, and since 2002 it has cost about 1.3-1.5 log points of growth per log
point of loss avoided, roughly 2 log points a year behind holding.**

| Where | Effective falls | Lost less than holding | Share of fall avoided | Premium: trend / hold less (fixed) / random timing | Verdict (cheaper than holding less?) |
|---|---:|---|---:|---|---|
| US 1927-1961 | 22 | 21 of 22 | 0.55 | 0.85 / 1.38 / 1.63 | yes (p 0.000) |
| US 1962-2001 | 15 | 15 of 15 | 0.47 | 1.38 / 2.15 / 2.60 | yes (p 0.013) |
| US 2002-2025 | 13 | 12 of 13 | 0.45 | 1.34 / 1.53 / 1.91 | in between (p 0.19) |
| 13 developed markets, 1966-2025 (price) | 19 | 17 of 18 | 0.49 | 1.11 / 1.33 / 1.52 | yes (p 0.009) |
| 3 regions, 1991-2025 (total return, USD) | 13 | 12 of 13 | 0.53 | 1.23 / 1.40 / 1.60 | in between (p 0.24) |
| 10 more markets, 1991-2025 (price) | 17 | 15 of 17 | 0.47 | 1.18 / 1.34 / 1.49 | in between (p 0.08) |

(p: share of 1,000 random-timing rotations whose premium is at least as low as trend's.)

- **Robust: the insurance itself.** In every era and every set trend lost less than holding in
  nearly every effective fall (92 of 98 counted above with a sign) and avoided 0.45-0.55 of the
  fall, against 0.26-0.36 for the same average exposure held fixed or at random dates. That
  "timing" part beats random timing in every era and set (share p 0.000-0.035).
- **Robust in direction, not always in strength: cheaper than holding less.** Trend's premium
  is below a fixed lower exposure and below random timing in all six rows. The rotation test
  passes in three (US 1927-61, US 1962-2001, 13 developed markets) and is "in between" in the
  three shortest or smallest (US since 2002, the total-return regions, the wider set). Nowhere
  is holding less the cheaper insurance.
- **Not robust: keeping it.** Net of the year after the low the insurance is a coin flip
  everywhere (US 16 of 50, non-US 7 of 19 effective falls positive): the rule buys back late.
  It pays only in long, deep bear markets (1929-32, 1973-74, Japan 1990-92, 2000-03, 2008) and
  loses in fast falls of three months or less (1987, 2020, August 2024: share avoided about a
  third, net about -15 log points, outside the US positive in 3 of 23).
- **What an investor should expect today.** Use the post-2002 numbers, total return: a premium
  of about **1.3-1.5** (US 1.34, non-US regions 1.49, wider set 1.37), i.e. for every 10 log
  points of a crash avoided, about 13-15 given up in rebounds and calm markets; in growth
  terms about **2 log points a year behind holding** (US 2.2, regions 2.7, wider 2.1), for a
  worst loss of about 35-55% instead of 50-85%. Holding less to get the same loss avoided would
  cost more (fixed 1.3-1.5, random 1.5-1.9: US 2002-2025, and the non-US sets over their whole
  spans; no post-2002 control split was computed outside the US). Whether that price is
  worth paying is a preference about drawdowns, not a test result.
- **For the live rule.** Nothing changes. The stock slots' trend filter is now a counted claim
  outside the US too: real insurance, cheaper than holding less, about 1.3-1.5 times as costly
  as it saves. Not a reason to expect higher growth than holding.
- **How sure.** Cards pushed before their numbers (`cards/insure-era.md`,
  `cards/insure-geo.md`). Not picks: no rule selected, nothing tuned; the project-wide bar
  (2,904 tries, N 1,012, Bonferroni p <= 4.9e-5) is quoted for scale only. The non-US
  insurance sign test (7.2e-5) narrowly misses it; with 1,000 rotations no control test can
  reach it. Per era and per set the effective counts are small (13-22). Price indices miss
  dividends, which flatters the level of the premium (not the comparison with the controls).
  The non-US sets overlap in time and share global falls (anchored on US falls), so they are
  not independent of each other or of the US after 1966.

## Step 1, insure-era: card 2's controls per era

Card `cards/insure-era.md` (pushed before its numbers). Same 11 US series, insure-1's 25%
episodes and clusters; the rule's paper series against a fixed exposure matched to the rule's
mean position in the era, and against the rule's own positions rotated to random dates within
the era (1,000 rotations).

| Era | Effective episodes | Share of fall avoided: rule / fixed / random (median) | Premium: rule / fixed / random (median) | p (share, premium) | Verdict |
|---|---:|---|---|---|---|
| 1927-1961 | 22 | 0.55 / 0.32 / 0.29 | **0.85** / 1.38 / 1.63 | 0.000, 0.000 | Timing, not just exposure |
| 1962-2001 | 15 | 0.47 / 0.26 / 0.25 | **1.38** / 2.15 / 2.60 | 0.002, 0.013 | Timing, not just exposure |
| 2002-2025 | 13 | 0.45 / 0.34 / 0.30 | **1.34** / 1.53 / 1.91 | 0.032, 0.191 | In between |
| **1962-2025** | 28 | 0.46 / 0.28 / 0.26 | **1.36** / 1.88 / 2.20 | 0.000, 0.020 | **Timing, not just exposure** |

- **Answer: yes, after 1962 trend is still cheaper insurance than holding less.** Holding less
  got dearer too after 1962 (fixed exposure 1.38 -> 1.88): the rise in trend's premium from 0.85
  to 1.36 is mostly the price of any crash insurance going up (after 1962 the falls paid out
  less: the rule's sum of loss avoided was 3,618 log points over 64 years against 4,768 over
  the 34 years before), not a decay of the timing. Trend still avoids about 0.46 of each fall against
  0.26-0.28 for the same exposure held at random or fixed.
- **But the margin narrows, and 2002-2025 alone does not pass.** Since 2002 the rule's premium
  (1.34) is only a little below a fixed 75% (1.53) and inside the random-timing range
  (p 0.19); its share avoided still beats random timing (p 0.03). 13 effective episodes is thin.
- Multiple tests (8 rotation p-values, Bonferroni 0.006): 1927-1961 both, 1962-2001 share
  (0.002), and 1962-2025 share (0.000) survive; the premium tests after 1962 (0.013, 0.020) do
  not. So "trend times falls better than chance" is solid in every era but the latest; "trend
  buys that cheaper than random timing" is solid only in 1927-1961, suggestive after.
- Net of the rebound, the rule is worse than both controls after 1962 (cluster N -3.8 log points
  against +1.5 fixed and +0.4 random; p 0.92): the late buy-back costs it more than it costs a
  passive lower exposure. Its advantage is entirely in calm markets (it is fully in when calm).
- Insurance itself (rule loses less than holding) stays near certain per era: 21 of 22, 15 of
  15, 12 of 13 effective episodes.
- The paper-series premium per era (0.85 / 1.38 / 1.34) matches insure-1's gym-splice numbers
  (0.86 / 1.38 / 1.34). No `tries.md` rows (re-scoring of logged positions).

## Step 2, insure-geo: outside the US

Card `cards/insure-geo.md` (pushed before its numbers). `tsmom12` exactly as in insure-1 (paper
series, Friday decisions, 2 bps a side, cash at 0) on 13 developed-market headline indices
(Yahoo daily closes, local currency, price indices except the DAX; first decisions 1966 to
1994), counted and judged the same way: 25% falls, clusters anchored on the US market's falls
(a cluster's value from its non-US episodes only), sign test and cluster bootstrap. Checks: the
same on Ken French's regional daily total returns in US dollars (Europe, Japan, Asia Pacific ex
Japan, from 1991) and on 10 more indices (Italy, New Zealand, Israel and seven emerging
markets).

| Set | Episodes / effective | Rule I > 0 (anchored; strict) | Share avoided | Net of rebound N | Premium: rule / fixed / random | p (share, premium) | Verdicts (card 1; card 2) |
|---|---:|---|---:|---:|---|---|---|
| **13 developed, price (decides)** | 109 / 19 | 17 of 18, p 7e-5; 14 of 15 | 0.49 | -0.9 (7 of 19 > 0) | **1.11** / 1.33 / 1.52 | 0.000, 0.009 | handed back; **timing, not just exposure** |
| 3 regions, total return, USD | 25 / 13 | 12 of 13, p 0.002; 10 of 11 | 0.53 | +0.4 | **1.23** / 1.40 / 1.60 | 0.035, 0.24 | handed back; in between |
| 10 more indices, price | 92 / 17 | 15 of 17, p 0.001; 13 of 15 | 0.47 | -0.3 | **1.18** / 1.34 / 1.49 | 0.009, 0.081 | handed back; in between |
| US, 1962-2025 (step 1) | 132 / 28 | 27 of 28 | 0.46 | -3.8 | **1.36** / 1.88 / 2.20 | 0.000, 0.020 | handed back; timing |

- **The insurance generalises.** Outside the US the rule lost less than holding in 17 of 18
  effective falls (sign test p 7e-5; strict grouping 14 of 15), avoiding about half of each
  fall (0.49), the same share as on US data. Net of the year after the low it is again a coin
  flip (mean -0.9 log points, 7 of 19 positive). Verdict by card 1's rule: **"insurance
  real, handed back in the rebound"**, in every set. The sign-test p (7.2e-5) narrowly misses
  the project-wide bar (4.9e-5); it is not a pick, quoted for scale.
- **Cheaper than holding less, again.** On the primary set the rule's premium (1.11) is below a
  fixed 66% exposure (1.33) and random timing (1.52, p 0.009), and its share avoided beats
  random timing (0.49 vs 0.34, p 0.000): card 2's verdict "timing, not just exposure". The
  order rule < fixed < random holds in every set; the rotation p-values are weaker on the
  shorter or smaller sets (premium p 0.24 on 3 regions, 0.08 on the wider 10), so those read
  "in between".
- **Price indices flatter the level, not the order.** Dividends are missing from the price
  indices, which lowers what the rule gives up while out. The total-return regions put the
  premium at 1.23 (2002-2025: 1.49) against 1.11 on prices (a different set, in US dollars, so
  not all of the gap is dividends). The fixed and random controls have the same mean exposure
  and miss the same dividends, so the comparison with them is fair; the price-index level is
  too low, by roughly 0.1-0.4.
- **Fast falls fail outside the US too:** 23 falls of three months or less (1987, 1989 Hong
  Kong, 2020, August 2024 in Japan): share avoided 0.35, net -15 log points, positive in 3 of
  23. Slow falls (over a year, 46): share 0.63, net +9.7, positive in 32 of 46.
- **By era:** price indices 1.12 before 2002 and 1.11 after; total-return regions 0.91 and
  1.49; wider set 0.98 and 1.37. Since 2002 the rule trailed holding by about 2-2.7 log points
  a year on the total-return regions and the wider set (2.2 on US data), and about 0.8 on the
  price indices.
- `tries.md`: 27 rows of kind `insure-check` (13 + 3 + 10 + Developed ex US), idea `insure-2`.
