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
| `effect`, `sd`, `skew`, `kurtosis` | the effect assumed true, used for power (and the noise, for `mean`) |
| `per_year` | observations a year (52 weekly bars, 8 FOMC meetings, ...) |
| `alpha`, `power` | one-sided significance level and power, fixed in advance |
| `min_sample`, `years_needed` | the sample the effect needs at that alpha and power (the calculator's numbers; `freeze` refuses others) |
| `source`, `note` | where the candidate came from, caveats |
| `frozen_at` | UTC time written by `freeze` |

Observations, one file per rule (`research/forward/obs/<id>.jsonl`), one line per bar or event:
`{"start", "end", "value", "rule_hash"}`. The rule's own forward adapter writes them.

## Rules of scoring (all enforced by `forward.py`, all tested)

1. **Freeze time is the commit.** A rule counts as frozen from the later of its `frozen_at` and
   the commit that first holds its line (`ledger.recorded_at`), exactly as decisions count from
   their commit (`ledger.in_force`). An uncommitted line is not frozen: `score` raises
   `NotFrozen`. Commit dates can be forged by whoever pushes; GitHub's push log stays the outside
   witness, as for the ledger (audit L1).
2. **Only bars that start after the freeze.** An observation whose holding period (or event
   window) starts before the freeze time is refused with `LookAhead`, not dropped: a pre-freeze
   bar in a forward file means backtest was mixed in, and the whole file is suspect. "Starts
   after", not "closes after": a bar that opened before the freeze was partly known.
3. **No re-freeze without a new id.** `freeze` refuses a known id (`AlreadyFrozen`); a file whose
   committed lines were ever changed stops everything (`LedgerTampered`); a line edited before
   its commit fails its own `rule_hash` (`HashMismatch`).
4. **Same code or no score.** Every observation carries the `rule_hash` of the code that made it;
   another hash is refused (`HashMismatch`). `check_code` re-hashes the frozen files on disk or at
   a commit and names every file that changed.
5. **The verdict is read once.** It uses exactly the first `min_sample` observations: before
   that the score says `waiting` (numbers shown are interim, not a verdict); after it, later
   observations are shown but never change `pass` or `fail`. No looking until the p-value
   happens to dip under alpha.
6. Overlapping observations are refused (each bar counts once).

### Power and minimum sample

- `sharpe`: n = 1 + (1 - skew sr + (kurtosis - 1)/4 sr^2) ((z(1-alpha) + z(power)) / sr)^2 with
  sr the per-period Sharpe: the variance `stats.probabilistic_sharpe` already uses (Mertens), so
  the test and its power calculation agree. Verdict p = 1 - PSR(0).
- `mean`: n = ((z(1-alpha) + z(power)) sd / effect)^2 (normal approximation to the t-test).
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
