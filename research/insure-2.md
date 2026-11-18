# insure-2: is trend's crash insurance cheaper than holding less, per era and outside the US?

Lane insure-2, 2026-11-18 (night). Branch `insure-2` (from `insure-1`), draft PR #90. Research
only: fake money, keyless public data, no change to the gym, the daily runner or the live
strategies. Held-out year untouched (nothing after 2025-10-31 parsed). Tables:
`results/insure-2.md`. Code: `lib/insure2.py` (reuses `lib/insure1.py`; nothing replayed).

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
