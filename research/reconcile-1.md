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

Run 2026-11-24 on `paper-trail` at `9e58ad6` (15 commits = 15 runs, 2026-11-11 22:00 to
2026-11-24 06:13 UTC; 145 ledger lines; 11 books):

    uv run python research/lib/reconcile1.py --work <scratch dir> --json <out.json>

(about 3 seconds; it clones the repo into the scratch dir and reads only the record branch).

### Answer

- **No class (c) mismatch: the runner and the gym agree with each other.** All 145 ledger lines
  are exactly what their strategy gives on the bars stored in that run's commit at the line's
  time. All 154 book snapshots (`state/portfolio.json` over the 15 runs: 4, 9, 9, then 11 books) are
  reproduced to the cent by the code that ran (its own gym, replayed in a subprocess on that
  commit's files, today's line uncommitted as at run time). Every live and backtest fill passes
  the gym-free check (open of a stored bar, after its decision, price, fee tier, cash sum).
- **No class (b) mismatch.** No bar was stored later than a run it should have reached (0 late
  bars), and the stored bars are never revised (the three rows of `data/revisions.jsonl` are
  2026-11-11 lows of SPY, QQQ, TLT, under 0.6 bp, and only logged). No ledger line was late
  (`ledger.in_force`: 0).
- **Live equals `gym.backtest` (22:30 decisions) every day for 9 of 11 books.** The two others,
  `risk_parity` and `xs_momentum`, differ on every day from their first fill, all class (a):
  max gap 51.37 and 43.99 USD (0.5% and 0.4% of equity), 37.51 and 27.26 USD at the end.
- **Class (d), outside the three asked for: the live scoreboard so far is not the gym on
  `main`.** Every scheduled run from 2026-11-13 to 2026-11-24 ran code `9b1c45e` (2026-11-12):
  `main` did not move until the landing of 2026-11-24 (#115), after the last run. So the record
  was scored with a flat 0.60% crypto fee, without the unpaid-buy rule (G2), distributions (G4)
  or cash interest. 46 of the 154 snapshots (the 4 books that hold crypto, from their first
  crypto fill) differ from today's gym; the next daily run (the first on new code) replays the
  record and these numbers move once, as DECISIONS says they will (fee tiers, 2026-11-18; G2,
  2026-11-17).

### Per book: live record against `gym.backtest`

Weights: one comparison per due day (the last ledger line due that day against the backtest's
22:30 decision). Days: UTC days both books mark (fills, end cash, end equity). Equity in USD on
2026-11-23's bars, both replayed by the gym on `main`.

| Book | Ledger lines | Weights: due days, matched, (a) | Days | Matched | (a) | (b) | (c) | Max equity gap (day) | Live / backtest equity | Fills live / bt | Fill-check problems |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `buy_hold_btc` | 14 | 13, 13, 0 | 13 | 13 | 0 | 0 | 0 | 0.00 | 8210.38 / 8210.38 | 1 / 1 | 0 |
| `buy_hold_spy` | 14 | 13, 13, 0 | 13 | 13 | 0 | 0 | 0 | 0.00 | 9577.78 / 9577.78 | 1 / 1 | 0 |
| `crypto_mean_reversion` | 13 | 13, 13, 0 | 12 | 12 | 0 | 0 | 0 | 0.00 | 10000.00 / 10000.00 | 0 / 0 | 0 |
| `equal_weight` | 14 | 13, 13, 0 | 13 | 13 | 0 | 0 | 0 | 0.00 | 9158.79 / 9158.79 | 13 / 13 | 0 |
| `preset_careful` | 12 | 12, 12, 0 | 11 | 11 | 0 | 0 | 0 | 0.00 | 9831.59 / 9831.59 | 4 / 4 | 0 |
| `preset_middle` | 12 | 12, 12, 0 | 11 | 11 | 0 | 0 | 0 | 0.00 | 9790.83 / 9790.83 | 2 / 2 | 0 |
| `risk_parity` | 13 | 13, 0, 13 | 12 | 0 | 12 | 0 | 0 | 51.37 (11-12) | 9561.46 / 9523.95 | 11 / 8 | 0 |
| `sixty_forty` | 14 | 13, 13, 0 | 13 | 13 | 0 | 0 | 0 | 0.00 | 9792.47 / 9792.47 | 4 / 4 | 0 |
| `ts_momentum` | 13 | 13, 13, 0 | 12 | 12 | 0 | 0 | 0 | 0.00 | 9857.53 / 9857.53 | 2 / 2 | 0 |
| `vol_target_spy` | 13 | 13, 13, 0 | 12 | 12 | 0 | 0 | 0 | 0.00 | 9810.27 / 9810.27 | 2 / 2 | 0 |
| `xs_momentum` | 13 | 13, 13, 0 | 12 | 0 | 12 | 0 | 0 | 43.99 (11-12) | 9372.51 / 9345.25 | 6 / 6 | 0 |

Days with no gap need no tolerance at all: there the two replays are equal to the last bit
(checked). Each book's `code_hash` is the same on all its lines.

### Where the (a) gaps come from

- **The start.** `risk_parity` and `xs_momentum` began with the run of 2026-11-12 01:51 UTC (a
  manual dispatch, due 2026-11-11), which started after the 00:00 crypto open. Their crypto
  legs filled at the open of 2026-11-13; the backtest, deciding 2026-11-11 22:30, bought crypto
  at the open of 2026-11-12 (BTC 73,965 against 71,406; ETH 2,055 against 2,018). The ETF legs
  filled at the same 2026-11-12 open in both. This one day is most of each gap (the max is on
  2026-11-12); later rebalances (11-16, 11-17, 11-20, 11-21) differ in size because the books'
  equity differs.
- **The extra crypto bar.** `risk_parity`'s weights use crypto volatility: every live line saw
  crypto bar D, the 22:30 decision of its due day did not, so the weights differ by 7e-6 to
  3.2e-4 on all 13 due days. `xs_momentum`'s cohort did not change (month-end rule), so its
  weights match.
- **Why the other books match exactly.** Their weights do not depend on the newest crypto bar
  (constant weights, ETF-only rules, or no position: `crypto_mean_reversion` stayed in cash),
  and the four benchmarks started with the on-time run of 2026-11-11 22:00, which fills like a
  22:30 backtest. With a new pending order at every open on both sides, the delayed and the
  22:30 schedules then give the same fills, unpaid-buy waits included (`equal_weight`, 11-16 and
  11-17).

So "live == gym" holds when the gym is given the live decision times; "live == `gym.backtest`"
holds for books whose decisions do not move with the newest crypto bar. For crypto-weighted
books, a live-vs-backtest gap of about half a percent after two weeks is schedule, and it is
mostly the one-day-late first crypto entry. The DECISIONS entry of 2026-11-24 says "in bars the
crypto lag is the same as in backtests"; true for the signal, but the fill is one calendar day
later, and a book's first crypto entry can be priced a day apart.

### The (d) gaps: what the next run will change

Snapshot of 2026-11-24 06:13 against the same record replayed by the gym on `main` (bars
through 2026-11-23; the trail has no `data/rates.csv` or `data/dividends.csv` yet, so no
interest or distributions on either side). Split by replaying with `main`'s gym and the old
flat 0.60% crypto fee:

| Book | Written (code `9b1c45e`) | `main`, flat 0.60% | `main` (fee tiers) | Fills written / `main` | Cause |
|---|---:|---:|---:|---:|---|
| `buy_hold_btc` | 8226.70 | 8226.70 | 8210.38 | 1 / 1 | first buy pays 0.80%, not 0.60% |
| `equal_weight` | 9176.72 | 9165.13 | 9158.79 | 9 / 13 | G2 top-ups (-11.59), tiers (-6.34) |
| `risk_parity` | 9558.25 | 9558.25 | 9561.46 | 7 / 11 | tiers: at 0.80% the 11-13 crypto buys fell just short of cash, G2 sold a little QQQ, SPY, GLD at that day's ETF open, a BTC top-up followed on 11-21 (+3.21, price luck) |
| `xs_momentum` | 9378.85 | 9375.61 | 9372.51 | 5 / 6 | G2 (-3.24), tiers (-3.10) |

The other seven books: written = `main` on every run. All 46 (d) rows are reproduced exactly by
the old code, so none is a bug. Who compares a research backtest (gym on `main`) with the
scoreboard as published up to 2026-11-24 is off by these amounts; after the next run the
scoreboard is on the same gym again.

The first new-code run also fetches distributions for the whole stored span. One with an
ex-date inside the live period (from 2026-11-12) would be paid into the past record too; the
next reconcile run will show it as (d).

### Minimal reproductions

No class (c) mismatch, so no bug reproduction. For the record:

- (a), `xs_momentum`: `gym.simulate` of the ledger's first line at its in-force time
  (2026-11-12 01:51:49) buys ETH at the 2026-11-13 00:00 open; the same weights at
  2026-11-11 22:30 buy it at the 2026-11-12 00:00 open (`gym.simulate`, `gym._execute`:
  "first bar that opens after T"). Working as designed (DESIGN, "Timing rules").
- (d): `research/lib/reconcile1.py` `old_snapshot()` (code `9b1c45e`) against `snapshot_of(
  report.live_results(...))` on the same commit; the split above swaps `gym.COSTS` for
  `{crypto: Costs(0.006, 0.0005), etf: Costs(0, 0.0002)}`.

### Limits

- Two weeks, 11 books, 13 due days: the check covers what happened, not what can. Untested on
  the record so far: a run that fails or skips a day, a source that stores a bar late, a
  distribution, cash interest, a strategy code change (none since 2026-11-12: `code_hash`
  constant per book). Rerun the script after the first runs on new code.
- Research backtests mostly use dividend-adjusted prices (`harness.run`, `adjusted=True` by
  default) while the live books trade raw prices with cash distributions; that gap is a
  documented choice and not measured here (no distribution fell in the live period).
- The fill check confirms each fill is legal; it does not re-derive which trades the band and
  the unpaid-buy rule should have made (that is the gym itself, compared under (c) and (a)).
