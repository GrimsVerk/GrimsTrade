# insure-2: crash insurance of `tsmom12` per era and outside the US

Written by `lib/insure2.py`. Log points = 100 x natural log; every number is rule minus holding unless said otherwise. Cash earns 0.

## Step 1, insure-era: card 2's controls per era

Card: `cards/insure-era.md`. Same 11 series, insure-1's 25% episodes, market-anchored clusters and calm mask, cash at 0, the rule as its paper series. Episodes by peak, clusters by first peak, calm by date. Fixed exposure: x = the rule's mean position in the window (whole-span x as second reading). Rotations: the 11-series block of the rule's positions rotated within the window, 1,000 per window, median (5-95%). p = share of rotations at least as good as the rule.

| Window | Clusters | Episodes | Rule S | Fixed S | Rotations S | p (S) | Rule P | Fixed P | Fixed P (whole-span x) | Rotations P | p (P) | Mean x | Verdict |
|---|---:|---:|---:|---:|---|---:|---:|---:|---:|---|---:|---:|---|
| 1927-1961 | 22 | 138 | 0.55 | 0.32 | +0.29 (+0.20 to +0.43) | 0.000 | 0.85 | 1.38 | 1.38 | +1.63 (+1.09 to +2.88) | 0.000 | 70% | Timing, not just exposure |
| 1962-2001 | 15 | 72 | 0.47 | 0.26 | +0.25 (+0.17 to +0.39) | 0.002 | 1.38 | 2.15 | 2.17 | +2.60 (+1.56 to +4.62) | 0.013 | 75% | Timing, not just exposure |
| 2002-2025 | 13 | 60 | 0.45 | 0.34 | +0.30 (+0.20 to +0.43) | 0.032 | 1.34 | 1.53 | 1.60 | +1.91 (+1.07 to +3.54) | 0.191 | 75% | In between |
| 1962-2025 | 28 | 132 | 0.46 | 0.28 | +0.26 (+0.17 to +0.36) | 0.000 | 1.36 | 1.88 | 1.90 | +2.20 (+1.45 to +3.87) | 0.020 | 75% | Timing, not just exposure |

Detail per window: the rule's sums (log points, paper series), the net N, and a sign test of the rule's cluster I (only with at least 10 clusters).

| Window | Sum I | Sum B | C | Rule N | Fixed N | Rotations N | p (N) | Rule I > 0 (sign test) | Clusters where rule S > fixed S |
|---|---:|---:|---:|---:|---:|---|---:|---|---|
| 1927-1961 | +4768 | -3872 | -204 | +4.2 | +3.9 | +2.6 (-1.9 to +8.2) | 0.260 | 21 of 22 (p 5.5e-06) | 16 of 22 |
| 1962-2001 | +1915 | -1957 | -692 | -2.3 | +2.8 | +2.0 (-2.7 to +6.4) | 0.935 | 15 of 15 (p 3.1e-05) | 12 of 15 |
| 2002-2025 | +1703 | -1784 | -492 | -5.5 | -0.3 | -1.7 (-7.4 to +2.5) | 0.912 | 12 of 13 (p 0.0017) | 8 of 13 |
| 1962-2025 | +3618 | -3741 | -1184 | -3.8 | +1.5 | +0.4 (-4.3 to +4.4) | 0.919 | 27 of 28 (p 1.1e-07) | 20 of 28 |

Fixed exposure's S is about 1 - x in every episode (it holds x of each fall); the last column counts clusters where the rule's S beats it.

**Headline by the card (1962-2025 window): Timing, not just exposure -> Yes.** Per era: 1927-1961 Timing, not just exposure; 1962-2001 Timing, not just exposure; 2002-2025 In between.

