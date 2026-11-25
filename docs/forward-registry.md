# Forward registry: judge a rule only on what happens after it is frozen

Lane `forward-1`, 2026-11-18. Research only, fake money. Proposed, not adopted: the owner decides
(`docs/DECISIONS.md`, entry of 2026-11-18). Code `src/grimstrade/forward.py`, tests
`tests/test_forward.py`, proposals `research/forward/candidates.jsonl` (written by
`research/forward/propose.py`).

## Why

- Published effects vanish after publication. Tonight's lanes went 0 for 3: `fomc-cycle`
  (survey-2), `xtsmom` (survey-3) and the FOMC announcement premium (ann-1) each held in their
  papers' years and not after.
- Held-out years are scarce. carry-3 spent its year (2025-11..2026-11); the next year nobody has
  seen starts after 2026-11-10 and is complete only from 2027-11.
- Several candidates can only be judged on data that does not exist yet: carry-3 `band`, the
  `fomc-bond-drift` effect (its paper's sample covers all our train years), the coin
  `stop-0.25` (PRs #53/#56) and monthly vs weekly decisions for small EUR books (eu-3, #63).

The future is the one sample no one can have looked at. A forward registry uses it honestly:
freeze the rule, write down the test and the sample it needs, then score only what comes after.

## Data model

`research/forward/registry.jsonl`, one JSON line per frozen rule, append-only (git history is
checked with `ledger.check_append_only`, the same check the paper-trail ledger gets):

| Field | Meaning |
|---|---|
| `id` | rule id with a version, `carry-3-band@1`. Never frozen twice; a changed rule is `@2` |
| `code`, `code_ref` | sha256 of each file that defines the rule, and the commit they were read from |
| `params`, `data` | the rule's parameters; its data source, universe and mode (`replayable` or `live`) |
| `rule_hash` | sha256 over `code`, `params` and `data` (canonical JSON): the rule's fingerprint |
| `metric` | `sharpe` (per-period values, annualised), `mean` (per-event values) or `win_rate` (share of events above 0, against 1/2) |
| `effect`, `sd`, `skew`, `kurtosis` | the effect assumed true, used for power (and the noise, for `mean`); skew and kurtosis enter only the `sharpe` sample |
| `moments_train` | `sharpe` only: skew and kurtosis measured on the train record (n, skew, kurtosis, sha256 of the values); `freeze` refuses a line without it or with a smaller Mertens k |
| `lrv`, `lrv_train`, `se` | long-run variance ratio used for the sample (`mean`, `sharpe`), its measurement on the train record (`freeze` refuses a line without one), and the standard-error rule |
| `per_year` | observations a year (52 weekly bars, 8 FOMC meetings, ...) |
| `alpha`, `power` | one-sided significance level and power, fixed in advance |
| `min_sample`, `years_needed` | the sample the effect needs at that alpha and power (the calculator's numbers; `freeze` refuses others) |
| `source`, `note` | where the candidate came from, caveats |
| `frozen_at` | UTC time written by `freeze`; `read` refuses a line without a valid one (`MissingFreezeTime`): a proposal pasted in by hand is not frozen |

Observations, one file per rule (`research/forward/obs/<id>.jsonl`), one line per bar or event:
`{"start", "end", "value", "rule_hash"}`. The rule's own forward adapter writes them. These
files are append-only too: `read_obs` runs the same `ledger.check_append_only` history check as
the registry, so an observation committed once and later changed or removed (a loss dropped, a
value edited) raises `LedgerTampered` and nothing is scored.

## Rules of scoring (all enforced by `forward.py`, all tested)

1. **Freeze time is the commit.** A rule counts as frozen from the later of its `frozen_at` and
   the first commit on HEAD's first-parent chain that holds its line (`ledger.recorded_at` with
   `first_parent`): on `main` that is the merge, not a side commit whose date its author chose
   (the registry lives on a branch with merges; the decisions ledger has none). An uncommitted
   line is not frozen: `score` raises `NotFrozen`. Commit dates can be forged by whoever
   pushes; GitHub's push log stays the outside
   witness, as for the ledger (audit L1).
2. **Only bars that start after the freeze.** An observation whose holding period (or event
   window) starts before the freeze time is refused with `LookAhead`, not dropped: a pre-freeze
   bar in a forward file means backtest was mixed in, and the whole file is suspect. "Starts
   after", not "closes after": a bar that opened before the freeze was partly known.
3. **No re-freeze without a new id.** `freeze` refuses a known id (`AlreadyFrozen`); a file whose
   committed lines were ever changed stops everything (`LedgerTampered`); a line edited before
   its commit fails its own `rule_hash` (`HashMismatch`). The same history check runs on each
   observation file (`read_obs`).
4. **Same code or no score.** Every observation carries the `rule_hash` of the code that made it;
   another hash is refused (`HashMismatch`). `check_code` re-hashes the frozen files on disk or at
   a commit and names every file that changed.
5. **The verdict is read once.** It uses exactly the first `min_sample` observations: before
   that the score says `waiting` (numbers shown are interim, not a verdict); after it, later
   observations are shown but never change `pass` or `fail`. No looking until the p-value
   happens to dip under alpha.
6. Overlapping observations are refused (each bar counts once).

### Power and minimum sample

Since 2026-11-25 (lane forward-se-1, `docs/DECISIONS.md`) the `sharpe` and `mean` verdicts use
a dependence-robust test, because weekly strategy returns are serially dependent and an iid
standard error rejected a true null 4-9% of the time at nominal 2.5% (evalue-forward-1):

- Statistic: T = mean / sqrt(w / n), w the Bartlett (Newey-West) long-run variance with
  L = min(round(per_year) - 1, n // 4) lags (one year of observations; 51 for weekly bars),
  scaled by n / (n - 1) so that L = 0 is the ordinary t-test (`forward.hac_t`).
- p = P(t_nu > T sqrt(c)), b = (L + 1) / n (Kiefer and Vogelsang's bandwidth M = L + 1),
  c = 1 - b + b^2 / 3, nu = 1.5 / b: a Student-t approximation to the fixed-b distribution
  (Kiefer and Vogelsang 2005). Its 97.5% critical value is within 1% of theirs and its 95% one
  within 1.2% for b <= 0.1; at b = 0.25 it is conservative. For `sharpe` the same T (Lo 2002 at the null Sharpe 0); the
  estimate shown is the annualised sample Sharpe.
- min_sample: the smallest n with n >= lrv * base(cv(n)), cv(n) the test's critical value at n:
  `sharpe` base = 1 + (1 - skew sr + (kurtosis - 1)/4 sr^2) ((cv + z(power)) / sr)^2, sr per
  period (Mertens' variance under the alternative); `mean` base = ((cv + z(power)) sd /
  effect)^2. `lrv` (plan field, at least 1, default 1) is the long-run variance ratio assumed
  true (`tsmom12`'s is 2.14; left at 1, a trend-like book is under-powered: 0.65 instead of
  0.80). Since lane `registry-lrv-1` it is measured at every freeze (`forward.measure_lrv`):
  the rule's values on its train record, in the unit of its forward observations, Bartlett
  long-run variance at the verdict's lag rule (`lag(n, per_year)`) over the sample variance,
  divided by the fixed-b mean factor c = 1 - b + b^2 / 3 (b = (L + 1) / n; without it five
  years of weekly train values would read about 20% low), floored at 1. The record must hold a
  full year of lags (n >= 4 (round(per_year) - 1): 204 weekly values, 28 events at 8 a year).
  `entry(..., train=values)` records the measurement under `lrv_train` (n, lags, raw ratio, c,
  floored lrv, sha256 of the values) and sets `lrv` = max(the plan's, measured); `freeze(...,
  train=values)` re-measures and refuses (`LrvNotMeasured`) a `mean` or `sharpe` line without
  `train`, with a `lrv_train` that is not this record's, or with a `lrv` below it. A caller may
  set a larger `lrv` (dependence longer than a year, which a one-year window cannot see), never
  a smaller one. Lines without `lrv` (none frozen) read as 1. `win_rate` does not use `lrv`.
- **The measured lrv is an upper value, not the estimate** (lane `registry-moments-1`). Five
  years of weekly values measure a true lrv of 3 with sd about 1.4, so a line sized with the
  point estimate gets an expected power of 0.70-0.77 instead of 0.80 whenever it is dependent.
  `measure_lrv` keeps the estimate as `point` and sets `lrv` = max(1, `lrv_upper(point, nu)`):
  point nu / chi2_nu(1 - 0.65), nu = 1.5 / b the verdict's own fixed-b degrees of freedom
  (Wilson-Hilferty quantile). 1.35 times the estimate at five years of weekly values, 1.21 at
  ten. The level 0.65 (`LRV_LEVEL`) is the smallest on a 0.05 grid at which the expected power
  over the measurement noise reaches 0.80 in every AR(1) cell (phi 0 to 0.6, five and ten years
  of weekly values, 4,000 records each, `research/registrymoments1.py`, tables in
  `research/results/registry-moments-1.md`): 0.809-0.838 in the dependent cells (phi 0.2 to
  0.6), against 0.703-0.771 for the point estimate; 0.869-0.883 with no dependence. Cost: a line with no dependence waits on average 1.45 times (five years of
  train) or 1.28 times (ten) the sample it needs, up from 1.20 / 1.14. Not fixed by it: 8 events
  a year with strong dependence (0.77 at phi 0.5) and dependence slower than a year (0.57: the
  one-year window does not see it; the caller must set a larger `lrv`).
- **Skew and kurtosis are measured too** (`sharpe` only). `measure_moments` takes the train
  record's population skew and raw kurtosis (`stats.moments`); `entry` compares Mertens' k =
  1 - skew sr + (kurtosis - 1)/4 sr^2 at the plan's own per-period Sharpe (`k_factor`) for the
  plan's pair and the measured pair, and takes the measured pair when the plan's k is smaller
  (more optimistic). A caller may assume a larger k (a worse tail than the record shows), never
  a smaller one; `freeze` refuses (`MomentsNotMeasured`) a `sharpe` line without
  `moments_train`, with one from other values, or with a k below the measured one. No upper
  value here: on a crash-prone weekly record (skew -1, kurtosis 6.5) the measured k has sd
  0.02-0.10 around a true 1.08-1.27 (Sharpe 0.5-1.5), so it moves the sample by a few percent
  where lrv moves it by a third. `mean` (its sample uses `sd`, not the moments) and `win_rate`
  measure no moments; lines without the fields read skew 0, kurtosis 3.
- Measured level (research/forward-se-1.md): on 52-week block-resampled store nulls it rejects
  4.3-5.8% at 10 years and 3.1-3.6% at 100 years for a difference against `tsmom12` (was
  6.1-6.4% / 4.6-4.7%), 1.0% / 2.3% for `tsmom12` against zero (was 8.1% / 8.3%; the upper test
  is very conservative there: 0.9% above +cv, 11.7% below -cv at 10 years). What remains at 10
  years is the skewness of yearly sums, which no standard error removes: read a 10-year verdict
  against `tsmom12` as about a 5%-level test. The card's kill condition was met (3 cells
  > 0.040); the night lead adopted the rule anyway as an improvement over the iid test, a
  deviation from the card, reversible by the owner.
- `win_rate`: exact binomial sign test; the first n at which the exact power reaches the target
  (exact power saw-tooths in n).

## Relation to `tries.jsonl` and the deflated Sharpe

- **The search already happened.** Each candidate was found on train data and is counted there
  (`research/tries.md`, unioned into `ledger/research_tries.jsonl`). Freezing an already counted
  variant is not a new try, as a held-out run of a counted variant is not (DECISIONS,
  2026-11-12). A rule frozen without a research row first gets one.
- **Forward data are fresh**, so the train search's selection bias does not reach them. What
  remains is the multiplicity of the registry itself: alpha is set per rule at freeze so that
  the batch shares 0.10 one-sided (Bonferroni: four rules at 0.025 each). The registry counts
  every rule ever frozen, dead ones included; a deflated Sharpe on forward records uses that
  count as N, not the research lane's thousands.
- **Live strategies** stay on the paper trail with `ledger/tries.jsonl`, the scoreboard and the
  graduation bar. The registry does not replace the paper trail; it is for rules that cannot or
  should not run in the gym yet (perps with a short leg, event effects, EUR books, rule changes
  the owner has not taken).

## Where it runs

A separate offline command, never the daily runner:

```sh
uv run python -m grimstrade.forward table [research/forward/candidates.jsonl]   # sample needed
uv run python -m grimstrade.forward score [--registry ...] [--obs ...] [--ref <commit>]
```

This lane does not schedule it and does not touch `.github/workflows/` or `run_daily`. If the
owner wants it scheduled later: a weekly job (or a local timer) that runs each rule's adapter,
appends its new observations, commits, and prints the score table. For `live` rules (carry: the
perp venues drop delisted coins from later downloads) the adapter must run and commit every week;
`replayable` rules (FOMC, coin falls, EUR ETFs) can be recomputed at any time from the frozen
code. Not built yet: a check that a `live` rule's observations were committed within a few days
of their bar (`ledger.recorded_at` on the observation file gives it cheaply).

## Before anything is frozen

None of the four research scripts can produce forward observations as they stand: each stops at
`TRAIN_END`/`HELD_END` on purpose (ann-1: "no bar after 2025-11-09 is read"). Each needs a small
adapter that runs the unchanged rule on bars after the freeze and writes observations. The adapter
is part of the rule: its files join `code`, so the hashes in `candidates.jsonl` (the research
code as it stands, at the commits named) will change at freeze. That is why the file is a
proposal.

## The four candidates (proposals, NOT frozen by the owner)

Alpha 0.025 one-sided each (0.10 over the four), power 80%. "Years" = `min_sample` / per year.
The alpha 0.10 columns are for comparison with rl-6's ~7 years (a single test at p < 0.10).

| Id | Metric (value) | Effect assumed | Per year | n needed | Years | n at 0.10 | Years at 0.10 |
|---|---|---:|---:|---:|---:|---:|---:|
| `carry-3-band@1` | Sharpe of the book's weekly return after costs and funding | 0.79 (train) | 52 | 659 | **12.7** | 379 | 7.3 |
| `fomc-bond-drift@1` | mean TLT day-0 excess return per scheduled FOMC meeting, bps (sd 107) | 12 bps (papers) | 8 | 625 | **78.1** | 359 | 44.9 |
| `coin-stop-0.25@1` | share of coin-fall episodes where the stop's deepest loss beats a matched cap | 15/21 = 0.714 | 1.6 | 42 | **26.2** | 26 | 16.2 |
| `eu-monthly-vs-weekly@1` | Sharpe of weekly return, monthly clock minus weekly rule (euw, no fee) | 0.50 | 52 | 1638 | **31.5** | 941 | 18.1 |

Where the effects come from (details in each line's `source` and `note`):

- **carry-3 `band`**: train 2021-02..2025-11 pooled Sharpe 0.79 (p 0.025, carry-3, PR #31);
  held-out year -0.65 (failed). 0.79 is the optimistic number: if the truth is half of it,
  four times the years.
- **fomc-bond-drift**: the papers' ~12 bps a meeting (survey-2 S3: Pan and Peng 2025;
  Hillenbrand, RFS 2025). sd 107 bps is implied by ann-1's TLT cell (+26.5 bps, t 2.3, 87
  meetings). At ann-1's in-sample 26.5 bps it would still need 128 meetings, ~16 years; that
  cell is 1 of ~70 and in the papers' own sample.
- **coin `stop-0.25`**: 15 of 21 episodes 2013-2025 (coin-cap-2, PR #53); not significant
  against all 13 coin-cap picks (coin-cap-3, PR #56). 21 episodes in ~13 years is 1.6 a year,
  but only 7.6 are effectively independent in 10 years: by that count ~55 years.
- **eu monthly vs weekly**: +0.14 Sharpe at no fee, one-sided bootstrap p 0.03 over ~14 years
  (eu-3, PR #63), the best of six variants; on the US six 1994-2025 monthly was worse. 0.50 is
  the annual signal-to-noise that p implies (1.88 / sqrt(14)), probably inflated.

### What the table says

- **Only carry-3 `band` can be judged forward within a working life of the project**, and even
  it needs ~13 years at the batch's alpha (~7 at a lone p < 0.10) if the train Sharpe were the
  truth. Its held-out year says the truth is probably lower. Freezing it is cheap (an adapter and
  a weekly snapshot of the perp lists) and it is the only clean second look this idea can get.
- **The other three cannot be settled forward in useful time** (26 to 78 years). Freezing them
  costs little and keeps them honest, but their owner decisions should not wait on it:
  - coin `stop-0.25` is a risk choice (shallower worst loss, same Sharpe), decide it as one;
  - a monthly clock's fee saving for a small EUR book is mechanical (fees per year / volatility,
    eu-3) and needs no test; only its edge would, and that edge is likely luck;
  - `fomc-bond-drift` stays a descriptive forward check at most, as survey-3 said.
- The registry's main use is therefore as a **filter on what is worth waiting for**: write the
  bar and the years at freeze, and anything that needs decades is decided on other grounds now,
  instead of being "pending more data" for ever.

## Owner decision

Freeze these and schedule the scorer? Concretely: (1) adopt the registry rules above
(DECISIONS entry); (2) which of the four to freeze (recommendation: `carry-3-band@1` for a
verdict, the other three as descriptive records only, or not at all); (3) a lane to write the
adapters and freeze; (4) whether a weekly job runs the scorer (it needs an owner-made schedule;
this lane added none).
