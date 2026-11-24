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

## Results (2026-11-19)

Built as on the card: `src/grimstrade/returnstore.py` (stdlib), steps `export` and the store
reader in `research/register2.py` (`sources`, `to_store`, `fits` split out of `match`), a
coverage sentence in BAR.md (`register.stored`), `research/register/README.md`.
Tests: `tests/test_returnstore.py` (round trip with NaN/inf and a comma in a variant,
byte-stable gzip, stale family files removed, bad header refused; and, with numpy,
`register2` export then delete the caches: same series, same matches, a stray curve left out,
a second export changes no byte), one in `tests/test_register.py`.

### The store

| | |
|---|---:|
| Series | 1,178 (39 re-simulated baselines, 11 live, 1,128 saved curves that fit a register row) |
| Local curves not stored | 8 of 1,136 (fit no row; one has NaN returns) |
| Family files | 64 (largest `trend-1926` 0.89 MB) |
| Size | **3.9 MB** (budget 5 MB: no sampling needed) |
| Weekly returns stored | 1.84 million |

### Rounding to 1e-6 (the card's accepted side effect)

From the same register (register-3's 3,118 tries) and the same series, regenerated from the
store against register-3's files: `moments.jsonl` same 1,224 ids and sources; skew moved in
41 rows (at most 0.0001), excess kurtosis in 261 (at most 0.001, on a kurtosis of 95),
weekly Sharpe in 23 (0.0001); the live lines now come in name order. `trials.json`: every rho,
count, ONC result and shape figure identical; cluster Sharpe means and one variance move by
0.0001; only the unused minimum-variance cluster Sharpes move more (up to 0.019, the
ill-conditioned weights register-3 replaced). **BAR.md rendered from the same register is
byte-identical** to register-3's (N_eff 486, rho 0.53, +0.30 / +0.56 over `tsmom12`,
Bonferroni 1.0e-4); the only change is the new sentence naming the store.

The local-only run (no store, caches rounded and sorted the same way) and the store-plus-
caches run give byte-identical files, so canonical order changes nothing but the live lines'
order.

### Clean-checkout check

A fresh `git worktree` of commit 3ba1e4a (no `research/data/`, no `register2.local.json`):
`uv run --with numpy python research/register2.py estimate` wrote `trials.json` and
`moments.jsonl` byte-identical to the committed ones (`git status` clean), and BAR.md
rendered there from the committed register was byte-identical too (6 s for the estimate).

How BAR.md was rendered for these checks: `grimstrade.register` with the census of remote
branches switched off (the committed register, 89 branches as counted), so tries pushed
since register-3 do not mix in. The register itself was not regenerated here: the next
regeneration (`git fetch origin`, register, `export` of the new lanes' curves, `estimate`,
register) picks up tonight's newer branches.

Tries rows added by this lane: none.

## register-7 addendum: no named source branch, one series per try, a storage policy

Card written 2026-11-24, before any number below "register-7 results" was computed.
Engineering only: no new configuration is backtested, no try rows, no held-out data.
Prompted by summary-4 (PR #156): `register2.py all` read its harness from `origin/summary-2`,
which GitHub deleted after the merge, and `export` never replaces a stored row, so a re-run
of the baselines (price-cache drift) or of the live strategies (live code changed) became a
second series of the same try.

1. **Source tree.** `tree`, `baselines` and `all` take `--ref <commit>` (default `HEAD`: the
   current checkout's commit) instead of a fixed branch. The baselines' source tag stays
   `harness@<sha12>` of that commit. `trials.json`'s `harness_ref` names the harness commits
   of the stored baseline series instead of a branch name.
2. **Rule for re-runs (the store only grows; committed rows are never replaced or removed).**
   - Live strategies are versioned by code: `source = live@code-<c>-sim-<s>`, where `<c>` is
     the strategy's `code_hash` (`run_daily.fingerprint`, the field every ledger decision
     carries) and `<s>` the SHA-256 (12 hex) of the simulator's source (`gym.py`, `data.py`).
     A new code version is a new stored series; the old one stays as the record of what the
     old code did. A re-run with the same code (other prices, other machine) is not added:
     the stored series stays.
   - `estimate` uses one series per live strategy: the current code's version if stored;
     else its only stored version (with a warning when that is not the current code); with
     several stored versions and none current, the newest by tag kind (a versioned tag beats
     a pre-register-7 `live@<commit>` tag); two or more versioned tags and none current:
     the strategy is left out, with a warning (no order to pick by). So a live strategy
     counts once whatever the store holds.
   - Re-simulated baselines: a series is added only if no stored baseline series has the
     same idea, variant and start, or if it fits a register row that no stored series fits
     (a baseline logged by a changed harness). Drift re-runs are not added.
   - Saved curves: unchanged (identical rows once; different curves that fit the same row
     stay, and keep the row ambiguous).
3. **Storage policy.** A curve whose every fitting register row is of kind `robustness`
   (never selectable) is not stored by default: not by `export` (unless `export
   --robustness`) and not by the harness hook (`research/lib/harness.py`, `_store`). Its
   curve CSV is still saved locally. Stored rows stay. Over the budget, `export` no longer
   drops stored rows: it drops only new curves that fit no selectable row (by SHA-256 of
   idea/variant/start), and warns if the kept rows alone exceed the budget.
4. **Checks.** Offline tests for each rule. Byte-identity: the old `register2.py` with its
   source ref pinned to the commit the stored baselines came from (512ae2ce13e2) against the
   new one with `--ref 512ae2ce13e2`, same price caches: `tree` and `baselines` output
   byte-identical; `estimate` on the committed store: `moments.jsonl` byte-identical,
   `trials.json` identical except the `harness_ref` value. BAR.md is not regenerated here.
