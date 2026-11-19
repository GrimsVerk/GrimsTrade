# register-4: a committed weekly-returns store, so the bar regenerates on any checkout

Card written 2026-11-19, before any result below the "Results" heading was computed.
Base: register-3 (PR #100). Its `research/register/BAR.md` (3,118 tries, N 1,032, N_eff 486,
+0.30 / +0.56 over `tsmom12`) rests on `research/register/trials.json` and `moments.jsonl`,
which `research/register2.py estimate` builds from return series that exist only on one
machine (re-simulated baselines and live strategies need the gitignored price caches; the
saved equity curves sit in other lanes' gitignored `research/data/runs/`, listed in the
gitignored `research/register2.local.json`). Nobody else can rebuild the bar.

Engineering only: no new configuration is backtested, no try rows, no held-out data.

## 1. The store (format fixed now)

- `research/register/returns/<family>.csv.gz`, one file per family (the register's `Idea`;
  the live strategies are `live`). Gzip with a zero timestamp and no file name, so the same
  series give the same bytes on every machine.
- One CSV row per series: `source,idea,variant,start,sharpe,first_friday,micro_returns`.
  `source`, `idea`, `variant`, `start` and `sharpe` (the harness's daily Sharpe, full
  precision, used to match the series to its register row) are the fields of
  `register2.Series`. The weekly returns (Friday to Friday, consecutive Fridays from
  `first_friday`) are stored as integers in millionths (returns rounded to 1e-6), space
  separated; `nan` / `inf` / `-inf` kept as such.
- Only strategy returns: no prices, no raw market data.
- What goes in: every re-simulated baseline series, every live strategy series, and every
  saved curve that fits at least one register row by `register2.match`'s rule (idea, variant,
  train period, start within 10 days, Sharpe to 0.0051), ambiguous fits included (so a row
  stays ambiguous). Identical rows are stored once. Rows sorted by
  (source, idea, variant, start, sharpe, returns) inside a file.
- Size budget: under 5 MB for the whole directory. If the export is bigger, it keeps every
  series that fits a selectable row (variant or baseline, train) or is live or a baseline,
  then adds the others by SHA-256 of `idea/variant/start` until the budget, and reports it.

## 2. Reading it

- A stdlib module (`grimstrade.returnstore`: read, write, merge) so the tests run without
  numpy and `grimstrade.register` can report the store's coverage in BAR.md.
- `research/register2.py estimate` loads the store first, then adds local series not already
  in it (the gitignored intermediates in `research/data/register2/`), all rounded to 1e-6, and
  sorts every source list canonically, so a machine with local curves and a clean checkout
  compute from the same inputs. A new step `export` writes the store from both; `all` runs it
  before `estimate`.
- Expected side effect, accepted now: rounding to 1e-6 can move fourth decimals in
  `trials.json` and `moments.jsonl` (once); every figure BAR.md prints must stay the same.

## 3. Checks

- Fixture test (offline): write a store, read it back, merge with local series, byte-stable
  output; `register2`'s matching reads it like the local files.
- Real check: in a fresh worktree of this branch with no `research/data/` and no local json,
  `register2.py estimate` must write `trials.json` and `moments.jsonl` byte-identical to the
  committed ones, and BAR.md rendered from register-3's committed register must keep every
  number of register-3's BAR.md.
- `research/register/README.md`: how a lane adds its returns.

Tries rows added by this lane: none planned.

## Results

(not yet)
