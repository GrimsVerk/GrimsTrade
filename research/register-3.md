# register-3: the harness logs each try's shape; a family-balanced correlation sample

Card written 2026-11-19, before any number below the "Results" heading was computed.
Base: register-2 (PR #92). Its `research/register/BAR.md` (3,023 tries, N 1,027) counts the
1,027 selectable and live tries as N_eff = 433 independent ones (A.3 with a measured average
correlation of 0.58 over 294 return series), but one family (a trend-tuning surface) is 97 of
those 294 series, and the record length, skew and kurtosis of a try exist only where a local
equity curve could be found (410 of 1,016 selectable rows).

## 1. The harness logs record length, skew and excess kurtosis (no new tries)

- `grimstrade.tryshape` (stdlib only, so it runs on every branch's `src/`): from the harness's
  calendar-day equity curve, weekly simple returns Friday to Friday (the rule of
  `research/register2.py`), T = their number, population skew and excess kurtosis, and the
  annualised weekly Sharpe.
- `research/lib/harness.py`'s `_log` (the standard path: `harness.run(..., log=True)`) appends,
  after its `research/tries.md` row, one line to `research/tries-shape.jsonl`: the exact row
  text plus weeks, skew, excess kurtosis, weekly Sharpe. Append-only, like `tries.md`; a run
  with fewer than two weekly returns or no variation writes no shape line.
- The register joins a shape line to every register try whose line is that row text (a row
  logged twice is one configuration run twice: same shape). `research/register2.py` takes it
  as a source of moments (source `logged`), ahead of re-simulation and saved curves, because it
  is computed from the row's own run when it was logged.
- The harness exists only on research branches (all at the same blob, `0ca675d`). This branch
  carries it unchanged in one commit and the hook in the next, so the hook commit cherry-picks
  cleanly onto any research branch (instructions in the results).
- Tests offline and deterministic: the shape of a synthetic curve against values computed by
  hand; the append-only file; the register's join; the harness's `_log` end to end when numpy
  is available (skipped otherwise; numpy is not a dev dependency).

## 2. A family-balanced correlation sample (rule fixed now)

- Family: the register's `Idea` column (the 11 live strategies are one family, `live`).
- Window and filter as register-2 (every weekly return 2012-01-06..2025-11-07 present, one
  series per distinct return path). Then the cap: **at most 10 series per family**. Within a
  family the series are sorted by the SHA-256 of `idea/variant/start` and the first 10 kept:
  a fixed pseudo-random pick that does not look at returns or Sharpe.
- On the capped sample: average pairwise correlation (A.3), ONC (same code, seed and
  settings), eigenvalue participation ratio, cluster Sharpe variance; the 1994-2025 window as
  a check with the same cap.
- Decision rule: BAR.md's measured A.3 row uses the capped sample's rho; the uncapped
  register-2 figure stays as a comparison row. The bar for a new pick stays the more cautious
  (larger N) of A.3 and ONC scaled (now K of the capped sample, scaled by K N / M), never
  above N. Reported: how far N_eff and the close/far edges move from 433 / +0.30 / +0.56.
- Sensitivities, reported, not used for the bar: caps of 1 (one per family, same pick), 5 and
  20; and the uncapped sample with each pair weighted so that every family counts by its share
  of the register's selectable rows (a post-stratified average).

## 3. Regenerate with tonight's branches

`git fetch origin`, `uv run python -m grimstrade.register`, then
`uv run --with numpy python research/register2.py all` with the saved curves of tonight's new
lanes added to the local list, then the register again (BAR.md reads the new
`trials.json`). A short note of what changed: tries, N, rows with a shape, sample, N_eff, bar.

Tries rows added by this lane: none planned (no new configuration is backtested).

## Results (2026-11-19)

### 1. Shape logged by the harness

Built as on the card: `src/grimstrade/tryshape.py`, the hook in `research/lib/harness.py`
(`_log`, three lines), `register.logged_shapes`, source `logged` in `research/register2.py`.
Tests: `tests/test_tryshape.py` (hand values for a two-point series, append-only file, the
harness's `_log` end to end with numpy: `uv run --with numpy pytest`), two in
`tests/test_register.py`. The hook commit (`33f3b4a`) was cherry-picked onto `summary-2` in a
scratch checkout: applies cleanly, its tests pass. No lane has logged a shape yet (0 rows):
it starts when the research base carries that commit.

### 2. Family-capped sample (same register and series as register-2: N 1,027)

The uncapped sample has 294 series from 57 families; the five largest hold 97, 27, 20, 12 and
12. Capped at 10 per family: 175 series.

| Sample (2012-2025 window) | Series | rho | N_eff (A.3) | ONC K | Close edge | Far edge |
|---|---:|---:|---:|---:|---:|---:|
| uncapped (register-2) | 294 | 0.58 | 433 | 2 | +0.30 | +0.56 |
| **at most 10 per family** | 175 | **0.52** | **490** | 2 | **+0.30** | **+0.56** |
| at most 5 | 140 | 0.56 | 450 | 2 | +0.30 | +0.56 |
| at most 20 | 210 | 0.52 | 495 | 2 | +0.31 | +0.56 |
| one per family | 57 | 0.69 | 320 | 2 | +0.30 | +0.55 |
| uncapped, pairs weighted by register share | 294 | 0.49 | 524 | - | +0.31 | +0.57 |

(Edges at three decimals: 433 gives z 4.654, +0.303 / +0.559; 490 gives z 4.691, +0.305 /
+0.563; Bonferroni p from 1.2e-4 to 1.0e-4.) Check window 1994-2025, capped: 115 series, rho
0.68, 2 clusters. ONC still finds 2 clusters (112 and 63); scaled, 11.7 trials: A.3 stays the
cautious estimate and sets the bar.

Finding: capping raises N_eff from 433 to 490 (+13%), not lowers it. register-2's note guessed
the big family lowered the average; it was the other way round: the 97 trend-tuning series
correlate highly with each other, so their many within-family pairs pushed the average up.
Weighting every family by its share of the register gives 0.49 (N 524). The edge needed over
`tsmom12` moves by 0.002-0.004: E[max] grows with log N, so any N between 320 and 524 gives
+0.30 (close) / +0.55-0.57 (far). The bar is settled by its order of magnitude, not by the
sample. Only one per family moves rho much (0.69), and that pick lands mostly in the larger
(non-crypto) cluster (48 of 57).
