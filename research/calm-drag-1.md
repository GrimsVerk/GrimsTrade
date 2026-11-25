# calm-drag-1: what the calm-market drag of `tsmom12` is made of

Lane `calm-drag-1` (DEEPER, descriptive), 2026-11-25 night (UTC). Card:
[`cards/calm-drag-1.md`](cards/calm-drag-1.md), pushed before any number. Code:
`lib/calmdrag1.py` (tests `tests/test_calmdrag1.py`). Tables:
[`results/calm-drag-1.md`](results/calm-drag-1.md). Research only, fake money, data already
in the cache (no download), nothing after 2025-10-31. No new rule, no tuning, nothing
selectable.

## Question

gap-2002-1 (#162) found that since 2002 the fall gain and the rebound lag of `tsmom12` about
cancel, so the calm drag C (rule minus holding on sessions outside every 25% fall and its
rebound year) is most of its cost. Nobody had split C: gap-2002-1, rev-costloss-1,
e4-anatomy-1, reentry-reconcile-1 and lagcost-1 were checked first (the last three split other
things: `e4` minus `tsmom12`, or execution lag; eu-4 counted whipsaw orders on a different
book). This lane splits C exactly into trading cost, the calm premium given up while out, the
timing of the calm exits, and the parts of each out-spell.

## The answer on one screen

- **Checks.** The split reproduces gap-2002-1's C to the hundredth (French US market 2002-2025
  -2.16, S&P 500 TR -1.65, mean of 10 industries -1.85) and every split adds up (largest
  residual 2e-15).
- **Costs are not it.** Trading cost on calm flips is 0.02-0.05 log points a year on every
  stock, bond and gold series (2 bps a side, about one calm flip a year).
- **It is not a late buy-back after real falls.** Out-spells that touch a fall or rebound
  contribute nothing to C (E-pre, E-mid, E-post are 0.00 everywhere, S&P -0.04): by the time
  the rebound year ends the rule is back in. This is mostly by construction: the rebound
  window (365 days) equals the rule's 12-month lookback, so at trough + 365 days the signal
  compares the price with the trough itself and is at or above it; that is also why the
  card's expectation of a sizeable E-post was wrong. All of C comes from out-spells that live
  entirely in calm markets: exits on dips that never became 25% falls.
- **Inside those spells the re-entry costs about twice what the exit saves** (1.7 times on
  GLD, 4.5 on QQQ). From exit to the spell's low the rule avoids +0.6 to +1.9 a year (G);
  from the low to re-entry it misses -2.2 to -4.2 (L). Nearly every such spell ends with the
  rule buying back above where it sold (W- is about all of C, W+ is +0.0 to +0.2). This is partly built in: a dip that kept falling
  would have become a 25% fall and left the calm label, so "calm-only spell" means, by
  hindsight, "false alarm".
- **Premium against timing depends on the era and the asset.**
  - US market 1927-2001: all premium, no bad timing (French market 1927-1961 P -0.97, T +0.01;
    1962-2001 P -1.15, T -0.03): the rule is out about 8-9% of calm time and gives up the calm
    equity premium for that time, no more.
  - US stocks since 2002: timing is half (S&P 500 TR 2002-2025 P -0.83, T -0.80; SPY since
    1994 P -0.77, T -0.72) to three quarters (French market P -0.47, T -1.66; QQQ P -0.40, T
    -1.66) of the out-time drag. The calm exits sat out better-than-average calm days: short
    dips followed by fast recoveries. The split is sensitive to the 25% cut-off (see How
    sure: 2022 is a fall on the French index and calm on the S&P).
  - Bonds and gold: mostly premium from long time out (TLT out 25% of calm time, P -1.68, T
    -0.56; GLD out 20%, P -2.45, T +1.05: gold's calm exits were well timed, but it is out so
    often that the premium outweighs it).
- **On stocks the drag is short whipsaws; on bonds and gold longer spells.** Spells of at most
  13 weeks carry -1.4 to -2.1 of the drag on SPY, QQQ, the S&P and the French market since
  2002, with a median calm spell of 4-8 calendar days (one or two Friday decisions: a flip
  around a 12-month return near zero, as eu-4 found on its book). TLT's drag is about half
  long spells (-1.05 of -2.25); GLD's a third (-0.43 of -1.40).
- **Coins: no calm drag to split.** Under the card's 25% zigzag BTC and ETH are almost never
  calm (2% and 0% of sessions) and the rule is never out in those sessions. A post-hoc look
  with a 50% zigzag (chosen after seeing that) gives the same picture: BTC never out in calm
  (C -0.07, all cost); ETH out 6% of its 11% calm time, and those exits paid (+1.27). The
  coins' trend cost, if any, lies in falls and rebounds, not here.

## Main table (cash 0, the gym's convention; log points a year, negative = costs the rule)

C = cost K + premium P + timing T. Out-spells: the calm drag minus cost splits into dip gain G
+ lag loss L (all from calm-only spells; edge spells are 0.00 on every row but S&P 1986-2025,
-0.04).

| Series | Window | Calm share | C | Cost K | Premium P | Timing T | Out share of calm | G (dip) | L (lag) | Spells <=13 wk | Spells >13 wk | Median spell, days |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| SPY | 1994-2025 | 0.78 | -1.51 | -0.02 | -0.77 | -0.72 | 0.066 | +1.38 | -2.86 | -1.41 | -0.07 | 4 |
| QQQ | 2000-2025 | 0.67 | -2.08 | -0.02 | -0.40 | -1.66 | 0.033 | +0.59 | -2.65 | -2.06 | +0.00 | 8 |
| GLD | 2005-2025 | 0.65 | -1.43 | -0.03 | -2.45 | +1.05 | 0.198 | +1.93 | -3.34 | -0.97 | -0.43 | 24 |
| TLT | 2003-2025 | 0.75 | -2.28 | -0.04 | -1.68 | -0.56 | 0.249 | +1.90 | -4.15 | -1.20 | -1.05 | 14 |
| BTC | 2013-2025 | 0.02 | +0.00 | +0.00 | +0.00 | +0.00 | 0.000 | - | - | - | - | - |
| ETH | 2017-2025 | 0.00 | +0.00 | +0.00 | +0.00 | +0.00 | 0.000 | - | - | - | - | - |
| French US market | 1927-2025 | 0.69 | -1.35 | -0.02 | -0.91 | -0.42 | 0.077 | +1.26 | -2.59 | -0.91 | -0.43 | 11 |
| French US market | 1927-1961 | 0.60 | -0.98 | -0.02 | -0.97 | +0.01 | 0.078 | +1.21 | -2.17 | -0.50 | -0.46 | 18 |
| French US market | 1962-2001 | 0.76 | -1.20 | -0.02 | -1.15 | -0.03 | 0.094 | +1.60 | -2.78 | -0.78 | -0.40 | 22 |
| French US market | 2002-2025 | 0.70 | -2.16 | -0.02 | -0.47 | -1.66 | 0.046 | +0.76 | -2.90 | -1.72 | -0.42 | 4 |
| S&P 500 TR | 1986-2025 | 0.80 | -1.12 | -0.02 | -0.76 | -0.35 | 0.063 | +1.34 | -2.41 | -1.00 | -0.07 | 4 |
| S&P 500 TR | 2002-2025 | 0.78 | -1.65 | -0.02 | -0.83 | -0.80 | 0.082 | +1.70 | -3.33 | -1.54 | -0.09 | 4 |
| Mean, 10 industries | 2002-2025 | 0.66 | -1.85 | -0.03 | -0.93 | -0.89 | 0.099 | +1.74 | -3.57 | -1.62 | -0.20 | 14 |

With idle cash at bills (the paper broker's convention) every C is 0.0-0.6 smaller (SPY
-1.37, TLT -1.95, S&P 1986-2025 -0.94; French 1962-2001 -0.62, the era of high bill rates),
and the shape is the same: the bills mostly shrink P. Per industry (results file): health,
staples and technology carry the largest drag (-3.9, -3.0, -3.0), and there it is mostly timing
(-2.6, -2.0, -2.1); shops and other the smallest (-0.9, -0.6).

## Which part could a future rule plausibly reduce without giving up the crash insurance?

Read from the table, not tested:

- **Costs: no.** At 0.02-0.05 a year there is nothing to save.
- **Late buy-back after real falls: no, it is not in the calm drag.** That cost sits in the
  rebound lag B (gap-2002-1), where faster buy-back rules have already failed (#94, #96, #103,
  #178).
- **The premium part: only by being out less, which is the insurance itself.** Each calm exit
  is, when it happens, the same signal as the first week of a real fall; calm-only spells are
  known to be false alarms only afterwards. On the long US record (1927-2001) the calm drag is
  almost all premium and no bad timing: the honest price of the exits, about 1 log point a
  year.
- **The one plausible target is the short whipsaw on stocks since 2002**: one- or two-Friday
  flips around a 12-month return near zero, -1.4 to -2.1 a year of the drag on the US stock
  series, half to three quarters of it as bad timing. But it is a weak lead: (1) it is concentrated in one era (the
  timing part is about zero in 1927-2001), so it may be the V-shaped dips of the 2010s rather
  than a property of the rule; (2) the obvious reducers (two-Friday confirmation, a dead zone
  around zero, holding only after four Fridays on) have been tried: they cut flips without
  improving Sharpe and made the worst drawdown deeper, because the same delay hits fast
  crashes (eu-4; trend-tune's "the later exits cost what the fewer whipsaws save"; trend-age
  dead). Any new attempt needs its own card, its own family bar and the project bar
  (N 1,116, z >= 4.93; BAR.md).
- **Bonds and gold**: their drag is mostly premium from being out a fifth to a quarter of calm
  time, and rev-costloss-1 (#182) found no crash-warning skill on gold or bonds. So the
  insurance there may not be worth its premium. That is a question about whether to trend-time
  those assets at all (a risk choice), not about a better exit.

## How sure

- One history per series; the six ETFs overlap 2005-2025 and the US series are the same
  market three ways (French, S&P, SPY), so they are not independent evidence. No standard
  errors are given: these are descriptions.
- The calm label is set by hindsight (whether a dip later reached 25%). So "the calm drag" is
  by construction the cost of the false alarms, and its split into whipsaw losses and saved
  dips (W- / W+) is close to tautological. G and L are exact, but they also condition on the
  dip having recovered.
- **The premium/timing split is sensitive to the 25% fall cut-off.** The 2021-11..2022-10
  drop is 25.6% on the French index (a fall) but under 25% on the S&P 500 TR (calm), so the
  S&P's 11-month out-spell 2022-06-06..2023-05-05 (231 sessions, plus a 20-session spell in
  May 2022) sits in its calm drag, while the French market's 2022-04-25..2023-05-05 spell sits
  in the fall and rebound parts. That is why the S&P's calm out share since 2002 is 0.082
  against the French market's 0.046, and why their P/T splits differ. One episode near the
  cut-off moves the split by tenths of a point a year.
- The premium P assumes the counterfactual of being out on random calm days with the same
  count; T is everything else. Both are exact parts of the same sum, not causal effects.
- **Deviations from the card, disclosed.** (1) The card split edge spells into before and
  after the fall; calm days between two episodes inside one spell were left out, so an E-mid
  column was added to keep the sum exact (it is 0.00 everywhere). (2) `insure1.infer_pos`
  keeps the old position on a flip day whose return is 0 or exactly the cost (both positions
  fit); the rebuild check caught this on 1-2 days each of nine French industries, and
  `repair()` now takes the position that reproduces the paper series' cost on that day. The
  paper series and C are unchanged by it (C reproduces gap-2002-1 exactly); gap-2002-1's bills
  series used the unrepaired positions on those days (checked: its gaps move by at most 0.001
  a year). (3) The S&P series
  opens already in the market, so its first position is taken from the second session. (4)
  The coin section with a 50% zigzag is post hoc, chosen after seeing that the coins have no
  calm sessions at 25%.
- The rebuild check of the French series at bills is circular (their bills series is built
  in `load_french` from the same repaired positions); the cash-0 check against the paper
  series carries the weight there. The S&P and the coins/ETFs at bills are checked the same
  way; their cash-0 checks are against the projects' own paper series.
- The window divisor Y counts from the first eligible session (or the window start); the
  2002-2025 rows use gap-2002-1's divisor exactly.
- Bar for scale (BAR.md, rows through 2026-11-25 01:16): 4,126 distinct tries, N for a new
  pick 1,116 (z >= 4.93; measured rho: N 506, z >= 4.70; Bonferroni p <= 4.5e-05). Not
  applicable: no test, no pick.
- `tries.md`: nine `note` rows (the six assets, the French US market, the S&P 500 TR, and the
  post-hoc coin diagnostic). Notes are not selectable; N for a new pick does not change.

## For the live rule

Nothing changes. For SUMMARY's "But it has a price" bullet (the lead's call): the calm drag is
not costs and not the late buy-back; it is the price of calm exits that turn out to be false
alarms, re-entered higher. On the long US record it is the calm premium given up for the time
out (about 1 point a year); on US stocks since 2002 it is mostly short one- or two-week
whipsaws, and half (S&P, SPY) to three quarters (French market, QQQ) of the out-time drag is
bad timing (they sat out fast recoveries); on bonds and gold it is long time out.
