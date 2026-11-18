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
