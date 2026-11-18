# RL 6: can a slower carry be detected, and closing the RL/perp line

Research run rl-6, 2026-11-18. Branch `rl-6` (from `rl-5`). Research only: fake money, train
years only (decisions to 2025-11-09), no RL or torch, nothing added to the paper system.

Question from rl-5: close the RL lane, or try a slower funding carry (rebalanced monthly, or on
funding averaged over 4-8 weeks) so that cost matters less? Before any card, a power analysis:
on the perp history there is, what is the smallest edge such a book could show, and how much of
carry-2's and carry-3's losses was cost and how much was price?

Words. **Edge**: the true mean return of a book per week. **MDE** (minimum detectable edge): the
smallest true edge a test finds 80% of the time. **sd**: the standard deviation of the book's
weekly return. **Turnover**: the sum of weight changes a year, in multiples of the account.

## Plan (written 2026-11-18, before the power script was run)

### What was already seen (disclosure)

Everything in carry-2, carry-3 and rl-4/rl-5 on these train years. In particular carry-3 already
scored two slow shapes on train (`research/carry-3.md` on branch `carry-3`): `w4` (four phase
books, each rebalanced every 4 weeks; pooled Sharpe 0.69, 15x turnover, negative on Bybit) and
`f30` (30-day funding signal; 0.29), next to `band` 0.79 and `w2` 1.01; and carry-3's one
held-out run (`band`, pooled -0.65). So the *means* of the obvious slow carries are known; a new
slow-carry run on the same years would be a re-look, not a test.

### What the script measures (no strategy numbers)

`research/lib/rl6_power.py` builds four carry-shaped books on carry-2's three venues: `w1`
(weekly on 7-day funding), and `m4-f7`, `m4-f28`, `m4-f56` (every 4 weeks, four phase books
averaged, on 7-, 28- and 56-day funding). It prints only their noise (weekly sd,
autocorrelation, sd of 4-week sums), their mechanical turnover, the paired sd of each slow book
minus `w1`, and from these the MDE. Means, Sharpes and p-values of the books are never printed
(each series is demeaned before it is summarised). The cost and price split of carry-2 and
carry-3 is taken from their published tables, not recomputed.

### The bar a slow carry would face (fixed now)

The carry cards' bar is a one-sided p < 0.10. A slow carry would be at least the 8th shape scored
on this data (carry-2 two, carry-3 five), so its honest bar is p < 0.10 / 8 (Bonferroni).

### Decision rule (fixed now)

A slower carry counts as **detectable** on these years, and step 2 (card, then train runs) goes
ahead, only if both hold:

1. **Absolute:** the MDE at p < 0.10 / 8, as an annual Sharpe, is at most 0.79 (carry-3 `band`'s
   train Sharpe, the most optimistic carry number seen).
2. **Paired:** the smallest gap between a slow book and `w1` that a paired test can find at
   p < 0.10 / 8 is no larger than the cost the slow book saves for certain at 8 bps a side
   (carry-3's measured realistic cost). Otherwise the one thing a slow book is for, the cost
   saving, cannot be told apart from the signal it loses.

If either fails: no card, no run; the closing note for the RL/perp line follows.
