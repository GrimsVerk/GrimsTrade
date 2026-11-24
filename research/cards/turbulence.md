# turbulence: does an unusual pattern of co-movement add anything to a plain volatility trigger, as a crash overlay on `tsmom12`?

Lane `turbulence-1`, written 2026-11-24, **before any number of this lane was computed** (no
turbulence value, trigger share, backtest or crash loss on any data). Research harness only;
fake money; train data only (the harness never loads a bar after 2025-11-10).

## Why

`tsmom12` (the live rule: hold an asset while its 12-month return is positive, else cash) fails
in fast crashes of three months or less (1987, 2020): the 12-month return is still positive
when the fall starts, so it rides the fall down and then buys back late (`SUMMARY.md`;
`fast-reentry.md`, #94 #96 #103). Faster buy-back rules did not fix it. `ideas.md` lists
`turbulence` as `new`, to be tested only against a volatility trigger, because wide-1 put it in
the gate family with `absorption-ratio`, which lost to its plain volatility twin after
publication (`results/absorption-ratio.md`).

Financial turbulence (Kritzman and Li 2010, "Skulls, Financial Turbulence, and Risk
Management", Financial Analysts Journal 66(5)) is the Mahalanobis distance of today's
cross-asset return vector from its trailing mean, under its trailing covariance. It is large
when returns are large (magnitude) **or** when assets move against their usual correlations
(say, bonds and stocks falling together). Kinlaw and Turkington (2014, "Correlation Surprise",
Journal of Asset Management 14) split it: magnitude surprise = the same distance with the
correlations set to zero; correlation surprise = turbulence / magnitude surprise.

**The question:** in the first weeks of a fast crash, while `tsmom12` is still in, does stepping
out on turbulence lose less than stepping out on a plain volatility trigger that is out of the
market just as often? Only the correlation part can make the two differ.

## Signal (fixed now)

On the test universe's business-day grid (`Panel.grid`: one row per day of the grid symbol, each
asset's last close visible at that day's 22:30 UTC decision; SPY for the six assets, the S&P 500
index for `idx`):

- r_i = log return of each asset into grid row i.
- Assets at row i: those with a return on every row i-252..i (a full year of window plus today).
  n_i of them; nothing if n_i = 0.
- Window: mean mu and covariance S of the 252 rows i-252..i-1 (today's return is **not** in its
  own window). Shrinkage, fixed: S_s = 0.9 S + 0.1 diag(S) (correlations shrunk by a tenth,
  variances unchanged; keeps S_s invertible for 2-6 assets).
- Daily turbulence d_i = (r_i - mu)' S_s^-1 (r_i - mu) / n_i (divided by n_i so the scale does
  not jump when an asset joins; about 1 on an ordinary day).
- Daily magnitude surprise m_i = sum_j (r_ij - mu_j)^2 / S_jj / n_i (the same with correlations
  set to zero: a plain, cross-asset volatility measure).
- Smoothing: T_i = mean of d over rows i-4..i (one week), M_i = the same for m. Correlation
  surprise C_i = T_i / M_i; defined only when n_i >= 2 on all five rows (with one asset C = 1 and
  carries nothing).
- Trigger: X_i > q_i, where q_i = the p-th percentile of X over the previous 756 rows
  (i-756..i-1, the current row excluded), needing at least 252 earlier values; off before that.
  Primary p = 90.

## Overlay (fixed now)

- Base: `tsmom12` exactly as logged (`baselines.py`: `weekly(slots(tsmom_signal))`, Friday
  decisions, equal slots of the eligible assets, cash for slots with a non-positive 12-month
  return).
- Every day (not only Fridays): if the trigger is on at the decision, the **risk slots** that
  `tsmom12` holds go to cash: SPY, QQQ, BTC, ETH on the six assets (GLD and TLT keep their
  slots, as in `absorption-ratio`); all four indexes on `idx`. When the trigger is off,
  `tsmom12`'s weights again. Decisions see only closes before 22:30 UTC; fills at the next open
  (the gym, unchanged); gym costs; cash earns 0 (the protocol's convention).
- The overlay can only remove exposure: it cannot buy back sooner than `tsmom12`. It aims at the
  fall, not at the late buy-back.

## Rules run (all of them; every one is a row in `tries.md`)

Six assets, 1994-02-01..2025-11-09 (the primary test; the trigger needs about a year of T, so it
is off until about 1995-02):

| Name | Signal | p | Kind |
|---|---|---:|---|
| `turb` | T | 90 | variant (primary) |
| `corr` | C (correlation part alone) | 90 | variant |
| `mag` | M (the plain volatility twin, same percentile) | 90 | baseline |
| `mag-match` | M, p chosen so its trigger is on on the same share of decision days as `turb`'s | p* | baseline (control) |
| `mag-match-c` | M, p matched to `corr`'s share | p** | baseline (control) |
| `turb-q75` | T | 75 (Kritzman and Li's top-quartile convention) | robustness |
| `mag-match-q75` | M matched to `turb-q75`'s share | | baseline (control) |

Out of universe, `idx` (S&P 500 index, Nikkei 225, FTSE 100, DAX as one equal-slot portfolio,
1962-01-02..2025-11-09, the set `baselines.py` and deep-1 already ran; covers 1987): `turb`,
`corr`, `mag`, `mag-match`, `mag-match-c` as `robustness` / `baseline` rows. `tsmom12` and equal
weight are re-scored from the logged baselines (`log=False`, already counted).

The matched twins are controls, not rules anyone could have run: p* is set on the whole train
window (bisection on the share of decision days with the trigger on). That is what isolates the
co-movement information: same overlay, same assets, same smoothing, same time out of the
market; only the correlations differ.

## Look-ahead tests (in `tests/`, offline, before the real run)

1. Truncation: the signal arrays computed on a panel cut at row k equal the full arrays on rows
   <= k (synthetic data).
2. A shock planted at row k changes nothing before row k.
3. The overlay through `harness.check_against_gym` on synthetic data (the fast path equals the
   gym's own visible-history path, which rebuilds the signal from the visible bars only).
4. Mahalanobis algebra: with an identity covariance d = m; with two perfectly ordinary
   correlated assets moving against their correlation, d > m.

## Pass bar (fixed now)

**Selectable (could replace or change the live rule):** both of
1. the protocol default bar (`protocol.md`) for `turb` (or `corr`) against its matched twin
   (`mag-match` / `mag-match-c`): Sharpe beats it with bootstrap p < 0.10; ahead in at least 4 of
   the 5 eras; max drawdown at most 5 points worse; same sign of the Sharpe difference on `idx`
   (the only out-of-universe set run, so "at least two of three" is read as "the one run"); beats
   equal weight; **and**
2. the project-wide bar (`register/BAR.md`, rows through 2026-11-19 00:30: 3,130 distinct
   tries, N 1,032 for a new pick, **N 486 effective trials; DSR 0.95 needs z >= 4.69, an edge
   over `tsmom12` of +0.30 (close rule) to +0.56 (far rule) on the primary test; Bonferroni
   p <= 1.0e-4**). z = Sharpe difference to `tsmom12` / its paired stationary-bootstrap SD (mean
   block 20 days, 2,000 draws, seed 0, `stats._stationary_indices`).

**Descriptive: does co-movement add anything?** Reported, not a pass:
- Sharpe difference `turb` - `mag-match` and `corr` - `mag-match-c` on both sets, with the
  bootstrap p and z.
- Fast crashes: peak-to-trough of the S&P 500 index close inside fixed windows (peak = the
  highest close before the window's lowest close): 1987 (1987-08-01..12-31, `idx` only), 1998
  (1998-07-01..10-31; on the six only SPY exists, so turbulence there is magnitude only), 2011
  (2011-04-01..12-31), 2015 (2015-07-01..10-31), 2018-Q4 (2018-09-01..12-31), 2020
  (2020-02-01..04-30). For each rule: return peak -> trough (the fall), trough -> 91 days later
  (the rebound) and the two combined; `tsmom12`, `turb`, `corr`, the twins. Plus the slow
  stress windows of `harness.STRESS`. Six episodes, clustered in time across the two sets:
  **kill-only** in the sense of `gate-null.md` step 7. Reading: "turbulence helps in fast
  crashes" only if `turb` loses less than `mag-match` in the fall in at least 5 of the 6
  episodes (pooling both sets, `idx` deciding where both have it) and the combined fall +
  rebound is not worse on average; even then it says "not dead", not "proven".
- Trigger shares, the correlation of T, M and C, how often each trigger fires inside each fast
  crash and on which day relative to the peak.

## Prior (stated now)

Low. About 5% that `turb` beats `mag-match` at p < 0.10 on the six assets with the same sign on
`idx`; well under 1% that anything clears the project bar (+0.30 Sharpe over `tsmom12`). Why:

- The gate family failed: `absorption-ratio` (eigenvalue concentration, another co-movement
  signal) lost to its plain volatility twin after 2010.
- The six assets are thin: one asset until 1999 (turbulence is then pure magnitude), two until
  2003, four from 2005-06, crypto from 2013-2018. The correlation part has little to work with,
  and crypto's own jumps will set it off without any US-market stress.
- In a fast crash the first big down day moves everything; the magnitude part fires the same
  day. Correlation surprise is most distinctive when bonds stop hedging (2022), a slow fall
  `tsmom12` already handles.
- Volatility timing of `tsmom12` was already found to be a risk dial, not an edge (#98, #110).

## What each answer means

- Passes both bars: the held-out year is looked at once, then a paper book. Not expected.
- `turb` (or `corr`) ahead of its matched twin but far below the project bar: co-movement holds
  some information, worth one line in `ideas.md`; nothing changes for the live rule.
- Not ahead of the matched twin: turbulence is volatility in disguise for this use; the
  `turbulence` line closes as dead, and the fast-crash failure stays the price of `tsmom12`.

Code: `research/lib/turbulence1.py`; results `research/results/turbulence-1.md`; write-up
`research/turbulence-1.md`.
