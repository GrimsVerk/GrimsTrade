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

## Power result (written 2026-11-18, after the power script; no book mean was looked at)

**In one line: a slower carry cannot be detected on these years. Both rules of the plan fail, so
by the plan no slow-carry card is written and nothing is run.** Table:
`results/rl-6-power.md`.

| Book (pooled, 246 weeks, 2021-02 .. 2025-11) | Weekly sd | Turnover/yr | MDE/week, p < 0.10 | MDE/week, p < 0.10/8 | As annual Sharpe, p < 0.10/8 |
|---|---:|---:|---:|---:|---:|
| `w1` weekly, 7-day funding | 1.83% (2.19% with autocorrelation) | 39x | 0.30% | 0.43% | 1.42 |
| `m4-f7` every 4 weeks, 7-day funding | 1.26% | 14x | 0.17% | 0.25% | 1.42 |
| `m4-f28` every 4 weeks, 28-day funding | 1.50% | 13x | 0.20% | 0.30% | 1.42 |
| `m4-f56` every 4 weeks, 56-day funding | 1.60% | 10x | 0.22% | 0.32% | 1.42 |

- **Rule 1 fails (absolute).** On 4.7 years the smallest Sharpe a test finds 80% of the time is
  **0.98 at p < 0.10 and 1.42 at the honest p < 0.10 / 8**, whatever the rebalance speed: a
  Sharpe's error depends on the number of years, not on how often the book trades. The best
  carry number ever seen here is 0.79 (carry-3 `band`, train). In money: a monthly book must
  earn about 0.17-0.22% a week (9-11% a year) to be found at p < 0.10, and 0.25-0.32% a week
  (13-16% a year) at p < 0.10 / 8. Per 4-week month that is about 1.0-1.3%.
- **Rule 2 fails (paired), by a factor of eight.** A slow book saves, for certain, 0.04% a week
  at 8 bps a side (25 fewer turns a year). The smallest gap to `w1` a paired test can see at
  p < 0.10 / 8 is 0.31% a week (`m4-f7`) to 0.53% (`m4-f56`). Even at the gym's 30 bps the
  saving (0.14-0.17% a week) is below the 0.21-0.36% a test needs at plain p < 0.10. So the one
  thing a slow book is for cannot be told apart from the signal it gives up: the slow books are
  as different from `w1` week to week (sd of the difference 1.6-2.7%) as `w1` is from zero.
- **Years needed** (80% power): a true Sharpe 0.79 needs 7.2 years at p < 0.10 and 15.2 years
  at p < 0.10 / 8; a true 0.5 needs 18 and 38 years. The perp cross-section has 4.7 train years
  (5.7 with the spent held-out year).
- One true fact the table does show: the four phase books of a monthly carry average out to a
  calmer book (weekly sd 1.26% against 1.83%) at a third of the turnover. That is
  diversification across rebalance dates, not edge.

### How much of carry-2's and carry-3's loss was cost, how much price

From the published tables (carry-2 `results/carry-2.md`, carry-3 `research/carry-3.md` on its
branch). Price = result - funding + costs: an approximation (compounding ignored, not a scored
number), as carry-3 itself uses it.

| Where it lost | Result/yr | Funding/yr | Costs/yr | Price/yr (approx.) | What did the damage |
|---|---:|---:|---:|---:|---|
| carry-2 `ls-funding` pooled, 10 bps (train) | +9.8% | ~+9% | ~-4.2% (42x x 10 bps) | ~+5% | nothing; it earned |
| same at 30 bps (Sharpe 0.09) | ~+1.4% | ~+9% | ~-12.6% | ~+5% | **cost, all of it** |
| carry-3 `w1`, realistic ~8 bps (train) | +11.3% | +8.9% | -3.5% | ~+5.9% | nothing |
| carry-3 `w4`, every 4 weeks (train) | +8.1% | +5.9% | -1.0% | ~+3.2% | saves 2.5 points of cost, loses 3.0 of funding and 2.7 of price |
| carry-3 `f30`, 30-day funding (train) | +3.2% | +8.4% | -2.0% | ~-3.2% | **price**: keeps the funding, gives it back |
| carry-3 `band`, **held-out year** (Sharpe -0.65) | -8.1% | +16.2% | -2.3% | ~-22% | **price**; with no cost at all still -6.1% (Sharpe -0.47) |

- **carry-2's failure was cost.** At 30 bps a side and 42x turnover the book pays ~12.6% a year
  against ~9% of funding. That is what a slower book would fix, and carry-3 then showed the
  real cost on these venues is ~8 bps, not 30 bps, so at the real cost turnover is no longer the
  problem (costs 2.5% a year).
- **carry-3's failure was price.** On the held-out year costs were 2.3 of the 8.1 points lost;
  the book's price move took ~22 points (most likely the short leg; carry-3 did not score legs on that year), more than the 16 points of funding it collected. A
  slower book would have saved about half of those 2.3 points (`w4` trades half as much) and
  would have held the same losing shorts longer.
- **Slower signals already cost more than they save on train.** carry-3's `w4` and `f30` (seen
  before this run) both end below `w1` and `band`; funding carries information for one to two
  weeks and fades within a month.

### Disclosures

- The plan and the decision rule were committed and pushed (commit b0058b2) before the script
  was run. The script ran twice: the second run only renamed one column header
  (`sd of difference` to `sd_eff of difference`); the numbers are identical.
- The script computes each book's weekly returns in memory but prints only demeaned summaries;
  no mean, Sharpe or p-value of a book was printed, written or looked at. Because no book was
  scored, **no row is added to `tries.md`** (a row is for a scored configuration); the four noise
  books are listed here instead.
- `m4-*` books hold weights flat between rebalances (no drift) and are gross of costs; that is
  enough for a noise estimate and is not carry-3's engine.
- MDE uses a normal approximation with an autocorrelation guard (the larger of the weekly sd and
  the sd of 4-week sums / 2); a stationary bootstrap would be a little wider, not narrower.
- Held-out year not loaded. No RL, no torch.

## Step 2: skipped

By the plan's rule, no `research/cards/slow-carry.md` and no train run. Two further reasons that
were known before the power run and point the same way: carry-3 already scored the two obvious
slow carries on these train years (`w4`, `f30`), so a new run would be a re-look at seen data;
and there is no held-out year left to confirm anything a train run found.

## Closing note: the RL / perp line, rl-1 .. rl-6

**Verdict: closed.** Six runs, one answer: on the data this repo has, no learner, and no input
fed to a learner, beats the plain rules, and the reason is the number of independent bets, not
the optimizer.

| Run | Question | Answer |
|---|---|---|
| rl-1 | PPO on six assets, prices + macro, against `tsmom12` | No: 0.57-0.71 vs 0.99, 0 of 50 seeds ahead |
| rl-2 | Residual RL tilting `tsmom12` | No: 0.96-0.98 vs 0.99, active share ~2% |
| rl-3 | Planted signal: what can the pipeline find? | Finds IC 0.20, misses 0.10; real inputs ~0.05; inputs bind first |
| rl-4 | Cheap learner fixes behind a gate; then the perp cross-section | Lasso passes the gate, no RL variant does; lasso perp book 0.03 vs `ls-funding` 0.57 |
| rl-5 | Perp inputs screened by return spread | None of nine passes Holm (best p 0.087); 246 weeks detect only ~0.3%/week |
| rl-6 | A slower carry, to make cost matter less | Not detectable: Sharpe 1.42 needed at the honest bar on 4.7 years; cost was not the held-out loss |

What was learned:

1. **The learners were never the binding limit.** rl-3 and rl-4 show a gated learner can find a
   weekly IC of 0.10 on a few inputs; the real inputs, on six assets or ~550 perps, carry IC
   0.00-0.05 against price. The one thing that pays, funding, is a cash flow, not a forecast
   (carry-3: IC ~0.02 against price + funding, zero against price).
2. **Five years of weekly data are too few.** ~250 weeks, coins that move together, venues that
   share the same market: the honest number of independent bets is a few hundred, and that
   bounds detectable Sharpe near 1.0 (p < 0.10) or 1.4 after counting tries.
3. **Cost was solved, price was not.** Realistic fees (~8 bps) made turnover a 2-3% a year issue;
   the held-out loss came from the short leg's price, which no rebalance speed fixes.
4. **The protocol held.** Every card was fixed before its numbers; the only held-out year used
   was spent once (carry-3) and failed. Nothing in this line reached the paper system.

What would need to change to reopen it (any one, stated as a trigger, not a plan):

- **Forward data on one fixed rule.** Record carry-3 `band`'s weekly decisions from now on
  (carry-3 option 3, no gym change) and score them unseen. One pre-registered rule pays only
  p < 0.10, so a true 0.79 needs ~7 years of forward data; a first look after 1-2 years can only
  kill it, not confirm it. Cheapest way back in.
- **Longer perp history with a fresh held-out period.** The perp cross-section starts in 2020
  (Binance archive) and trades from 2021 under the 365-day rule. From 2027-11 one new unseen year
  exists; a held-out-only card on `band` could spend it. Older single-contract funding (BitMEX
  since 2016, a handful of coins) adds years but not breadth.
- **A new input with t >= 3 on its own.** An RL or ML rung on perps reopens only if a
  pre-registered screen finds an input that clears Holm with room to spare on train, and carries
  to another venue; and only with a learner that already passed the planted gate (rl-4's lasso).
  Order-book or intraday data would be the candidates; breadth-1 found hourly edges eaten by cost.
- **A much wider, longer cross-section** (spot coins with dead ones, 2017+, or the 33-market pool
  with decades) for learner work in general: more independent bets is the only lever rl-3 named.

### Status

Done 2026-11-18. Nothing running. No row added to `tries.md`. Draft PR #52 (`rl-6` -> `rl-5`),
not merged.
