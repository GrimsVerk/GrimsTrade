# reconcile-1: does the live paper record match the gym?

Lane `reconcile-1`, 2026-11-24. Descriptive engineering check, not a strategy try: no card,
no held-out data, no Sharpe. Research results assume "live == gym"; this checks it for the 11
paper books on branch `paper-trail` (read only; nothing there was changed).

## Written before any number was computed

### What is compared

For each live book and each daily run on `paper-trail` (one commit = one run):

1. **Weights.** The weights in `ledger/decisions.jsonl` against the book's strategy (current
   `main` code) re-run at the run's own decision time (the line's `time`), on the bars that were
   stored on `paper-trail` *in that run's commit* (`visible_history` at that time). Then the same
   on the bars stored at the newest commit, and at the time a backtest would decide
   (`gym.DECIDE_AT` = 22:30 UTC on the day the run was due).
2. **Snapshot.** `state/portfolio.json` of each commit (cash, positions, equity, fill count, as
   the runner wrote them) against a replay of that commit's ledger on that commit's bars,
   (i) with the gym of the code that ran (the `code` commit in the ledger line; earlier lines:
   the newest `main` commit before the run) and (ii) with the gym on `main` now.
3. **Day by day, live against backtest.** The live book (`report.live_results`: the ledger's
   decisions from the time each counts, `ledger.in_force`, replayed by `gym.simulate`) against
   `gym.backtest` over the same days (one decision a day at 22:30 UTC, the book's strategy, the
   same bars, same start cash, same costs), per UTC day: target weights in force, fills (symbol,
   price, quantity, fee), cash and equity at the end of the day.
4. **Fills on their own.** Each live fill checked against the bars without the gym: it is at an
   open of a stored bar of its asset, after the decision that caused it, at open x (1 +/- slip),
   with a fee of the tier rate x traded value; and each day's cash change equals the fills' cash
   flows.

The run due on day D is the one that starts between 12:00 UTC on D and 12:00 UTC on D+1 (the
2026-11-24 entry in `docs/DECISIONS.md`: scheduled 22:30 D, started 02:01-06:13 UTC on D+1).

### Tolerance (floating point only)

- Values both sides compute in full precision (weights, quantities, prices, fees, cash,
  equity): equal when `|a - b| <= 1e-9 * max(1, |a|, |b|)`.
- Values the runner wrote rounded to cents (`cash`, `equity` in `state/portfolio.json`): equal
  when `|a - b| <= 0.005 + 1e-9 * |b|`. Positions there are full floats: the first rule.
- Fill counts and the set of symbols filled on a day: exact.

Nothing else is forgiven: a gap of one cent beyond rounding is a mismatch and gets a class.

### Classes of mismatch

- **(a) schedule**: explained by the delayed schedule (DECISIONS 2026-11-24). The live
  decision ran at its real time instead of 22:30 on its due day: it saw one crypto bar more,
  filled crypto a day later or ETF buys later because the cash came from a crypto sale.
  Test: the mismatch is gone when the backtest decides at the live run's own times on the same
  bars (everything else equal).
- **(b) data**: a bar or other input the live run did not have (stored later, or stored for a
  day before the decision but after the run) or that a source revised (`data/revisions.jsonl`).
  Test: the mismatch is gone when the replay uses only the bars stored in that run's commit.
- **(c) bug**: in the runner or the gym: the ledger's weights are not what the strategy gives
  on the bars the run had, a snapshot is not what the code that ran computes from its own
  record, or a fill breaks the timing, price, fee or cash rules. Each gets a minimal
  reproduction and the code location.
- **(d) rule change** (added because it is neither of the three): the gym's rules changed on
  `main` after the run (fee tiers, unpaid buys, distributions, cash interest), so the snapshot
  the runner wrote and the record replayed today differ. Not a bug; it means the scoreboard's
  past numbers move when new code first runs.

A day that mismatches for several reasons gets the worst: (c) before (b) before (d) before (a).

## Results

(pending)
