# insure-1: is "trend = crash insurance" statistically solid, and what does it cost?

Lane insure-1, 2026-11-18 (night). Branch `insure-1` (from `trend-1926-fix`), draft PR #87.
Research only: fake money, files already in the data cache, no change to the gym, the daily
runner or the live strategies. Card (two parts, each pushed before its numbers):
`cards/crash-insurance.md`. Tables: `results/insure-1.md`. Code: `lib/insure1.py`. Held-out year
untouched (nothing after 2025-10-31 parsed).

## The answer on one screen

**Yes, the insurance is real, and it is timing, not just holding less. But it is not free: over
1927-2025 it cost about as much growth as it saved (a premium of about 1.07 log points given up
per log point of loss avoided), it was cheap only in the 1930s, and it mostly fails in fast
crashes.**

- **What was counted.** Every fall of 25% or more (zigzag: 25% down, then 25% up to close it)
  on the US market and 10 industries (French daily, 1927-07 to 2025-10): 270 episodes. They
  cluster, so they were grouped into **50 effective episodes** (each market fall plus the
  industry falls inside it; 37 under a stricter grouping). The market alone has 21.
- **Insurance (loss avoided from peak to trough).** `tsmom12` lost less than holding in 47 of
  48 effective episodes that are not ties (was 48 of 50 before #218: 2 are ties, the rule held
  through the fall; 47 of 50 with ties counted against; sign test p 2e-13, was 1e-12; 35 of 36
  under the strict grouping, was 36 of 37). On average it
  avoided half of the fall (mean share avoided 0.50). Market alone: 20 of 20 not tied (one tie: 20 of 21 with it counted against, as before #218).
- **Is it more than holding less?** A rule that sits in cash 25% of the time at random also
  loses less in a fall. Against exactly that (card 2): the rule's own positions shifted to
  random dates (same exposure, same spells) avoid 0.27 of the fall (90% of shifts 0.21-0.34),
  and a fixed 73% exposure avoids 0.29. The rule's 0.50 beat all 1,000 shifts. The timing is
  real.
- **What it costs.** The rule buys back late, so the year after the low hands most of it back.
  Net of that rebound, the effective episodes are a coin flip (15 of 48 not tied positive, was 16 of 50
  before #218; mean -0.3 log points; on the market alone 12 of 20, was 12 of 21, +5.9, p 0.06). Over the whole period, per log point of
  loss avoided in falls the rule gave up **1.07** in rebounds and calm markets (0.97 if cash
  earns T-bills). Holding less is far dearer insurance: **1.63** for a fixed 73% exposure,
  **1.8** for random timing (1.44 to 2.57). So trend is the cheapest of the three ways to lose
  less in a crash, at roughly break-even growth.
- **By era** (pooled 11 series): 0.86 in 1927-1961 (the insurance paid for itself), **1.38** in
  1962-2001 and **1.34** in 2002-2025 (it cost a third more than it saved).
- **When it fails.** Fast falls (peak to trough within 3 months, 63 episodes): it still avoids
  about half of the fall on average, but sells near the low and buys back higher: net of the
  rebound -6.6 log points, positive in only 12 of 63 (was 15 before #218). Market cases: September 1929 (avoided
  31%), spring 1940 (3%), 1987 (26%), March 2020 (44%), 2009's last leg (100% of the fall, then
  -48 in the rebound). Slow falls (over a year, 80 episodes): avoided two thirds, positive in 79
  of 80, still +10.5 net of the rebound (52 of 80). The insurance pays in long bear markets
  (1930-32, 1937-38, 1973-74, 2000-02, 2008) and is roughly a wash or a loss otherwise.
- **For the live rule.** Nothing changes. "Crash insurance" is now a counted claim: real across
  50 effective falls in 98 years, and cheaper than holding less. It is not an edge: in log
  growth it about breaks even with holding (worse since 1962), and its value is the smaller
  worst loss (market 38% against 84%), which is a preference.

## How it was counted (and the bar)

- One rule, exactly trend-1926's `tsmom12` (12-month return positive -> hold, else cash; Friday
  decisions; 2 bps a side). No new rule, nothing tuned, nothing selected.
- Rule returns 1927-2001: trend-1926's saved gym runs (not rerun), 77% of sessions; the turn of
  1961/62 and 2002-2025: trend-tune's gym-free paper series. Largest difference in one
  episode's insurance between the two sources on 1927-2001: 3.7 log points (holiday-Friday
  weeks, as trend-1926-fix found). The 30-industry robustness set is paper series only.
- `tries.md`: 41 rows of a new kind, `insure-check` (defined in its header: descriptive
  re-score of an existing configuration, not selectable, not counted in any family): 11 primary
  series and 30 industries. The T-bill reading, the 20% and 40% thresholds and card 2's controls
  are re-scorings: no rows.
- Bar. Not a pick, so the bar for a new pick does not apply. For scale: project-wide
  (`register-1`'s `BAR.md`, rows through 2026-11-18 22:34) **2,904 tries, N 1,012 for a new pick,
  Bonferroni p <= 4.9e-5**. Card 1's insurance sign tests (1.7e-13, 5.4e-10; market alone 9.5e-7; were 1.1e-12, 2.8e-10 and 1e-5 before #218)
  clear it, but that test is easy by construction (see card 2). Card 2's rotation test (0 of
  1,000) cannot reach 4.9e-5 with 1,000 rotations. The base lane trend-1926 had no family bar.

## Card 1 result: "insurance real, handed back in the rebound"

| Test (primary set, 25% episodes) | Clusters not tied | Above 0 | Sign-test p | Mean, log pts | Bootstrap p |
|---|---:|---:|---:|---:|---:|
| I (peak -> trough), market-anchored | 48 | 47 | 1.7e-13 | +25.1 | 0.000 |
| I, linked (strict) | 36 | 35 | 5.4e-10 | +19.8 | 0.000 |
| N = I + rebound, market-anchored | 48 | 15 | 1 | -0.3 | 0.56 |
| N, linked | 36 | 8 | 1 | -3.7 | 0.97 |
| N with cash at T-bills, market-anchored | 48 | 20 | 0.9 | +2.3 | 0.15 |
| Market alone, I | 20 | 20 | 9.5e-7 | +32.9 | 0.000 |
| Market alone, N | 20 | 12 | 0.25 | +5.9 | 0.06 |

Before #218 (ties counted as wins or losses at random) the rows read, as clusters / above 0 /
sign p: 50 / 48 / 1.1e-12; 37 / 36 / 2.8e-10; 50 / 16 / 1; 37 / 9 / 1; 50 / 20 / 0.94;
21 / 20 / 1e-5; 21 / 12 / 0.33. A tie is a cluster whose mean is below 1e-9 log points.

- Robust to the threshold: 20% falls (70 effective episodes) and 40% falls (23) give the same
  picture; at 40% the net is positive (+7.7, bootstrap p 0.03, sign test p 0.067, was 0.11 before #218): the deeper
  the fall, the more of the insurance survives the rebound. Premium 1.06 (20%), 1.11 (40%).
- 30 industries (961 industry episodes, 63 effective): I 58 of 60 not tied positive (was 58 of 62 before #218), N -0.5, premium
  1.06. The same answer.
- Per series the premium runs from 0.98 (telecoms) to 1.25 (energy); the market is 1.01.

## Card 2 result: "timing, not just exposure"

| | Share of the fall avoided | Net of rebound, log pts | Premium |
|---|---:|---:|---:|
| `tsmom12` | 0.50 | -0.3 | 1.07 |
| Fixed exposure 73% | 0.29 | +2.5 | 1.63 |
| Random timing, median (5-95%) | 0.27 (0.21-0.34) | +1.3 (-1.4 to +4.2) | 1.82 (1.44-2.57) |
| p (rotations at least as good) | 0.000 | 0.82 | 0.000 |

The rule's advantage is not in the episode itself net of the rebound (there it is no better than
random timing, p 0.82); it is that it stays invested in calm markets, so the same loss avoided
costs much less growth outside the falls.

## How sure

- Card 2 was added after card 1's numbers were seen, because card 1's test turned out to be
  easy by construction; it was written and pushed before its own numbers.
- Episodes are defined with hindsight (peak and trough), on holding's prices only, so they do
  not favour the rule; the rebound window charges the rule's late return to the insurance.
- 14 of the 50 effective episodes are 1929-1942; the market-anchored grouping counts five
  separate legs of 1929-1933 (the strict grouping: three). Even with that decade removed
  there are 36 effective episodes, 35 of them at or above zero on I and one below (durables,
  2023-12 to 2024-04), read from the cluster table, not a separate test.
- One country, one asset class, 98 years. The six live assets' crash record (2000-02, 2008,
  2020, 2022) is inside this sample on the market series.
- Cash at 0 is the gym's rule; with T-bills the premium is 0.97 (market 0.91).

## Next lanes (not started)

1. `insure-era`: card 2's controls per era (is trend still cheaper than holding less after
   1962, when its own premium rose to 1.35?). One re-scoring, no new rows.
2. `fast-reentry` on this episode set: the cost is the rebound (B about -28 log points per
   episode); a re-entry rule fixed on a card, judged on N across these 50 effective episodes.
3. The same count on non-US stocks (French international indices, or the Yahoo country indices
   1994-2025), to see whether 50 US episodes generalise.

2026-11-25 (eng-nits-1, #218): a value below 1e-9 log points (a rule in the market through a
whole fall or rebound) is now a tie, left out of the sign tests, instead of a win or a loss at
random; the counts above are marked "(was ... before #218)". No verdict changed. Also, `infer_pos` now dates a flip on a day the holding did not move on that day (it was one session late). `results/insure-1.md` was regenerated: card 2's random-timing N band moved from -1.44 to +4.19 to -1.42 to +4.18, and its p from 0.816 to 0.817 (0.82 above still holds). No verdict changed.
