# rl-7: can a small learned policy beat `tsmom12` on ~50,000 market-months?

Lane `rl-7`, card written 2026-11-25 21:55 UTC **before any learner, gate or rule number is
computed on any of the data below**. Seen before writing: the spans and month counts of the
series (`uv run python research/lib/rl7_data.py`, no returns or statistics printed), and every
earlier record named below. Research only: fake money, files already in the local cache, no
change to the gym, the daily runner or the live strategies. Nothing after 2025-10 is read; the
project's held-out year (from 2025-11-11) is not touched. Every period in `tries.md` is `train`
in the project's sense; "holdout" below means this card's held-out cell inside those years.

## Question

The RL line (rl-1 .. rl-6) closed on daily ETF/crypto/perp data: too few independent bets, and
no RL variant passed rl-4's planted-signal gate (the lasso did, narrowly). The project now has
long monthly histories. **With about 50,000 market-months across stocks, bonds, currencies and
commodities, does a small learned policy on past-price features beat `tsmom12` out of sample,
pooled across markets it was not trained on, in years after its training data end?** One
direction (learner better), two pre-registered learners.

## What was seen before (disclosure)

- Every series below was used by earlier lanes. pooled-1 (#142) and pooled-2 (#159) scored
  `tsmom12`, `e4` (the 1/3/6/12-month ensemble) and own-vol targeting on the 41 stock markets
  and the 29 non-equity series (1927-2025); e4-indep-1 (#198) scored `tsmom12` and `e4` on the
  pre-1927 markets and the five Nordic/Irish markets. So the post-1990 behaviour of 12-month
  trend and of the 1/3/6/12-month signs on these markets is known in outline (`e4` +0.063 on
  stocks, about 0 elsewhere). The feature list below includes those signs because they are
  the standard trend inputs, not because of those results; it was not tuned on anything.
- No learner of any kind has been fitted on these monthly series before.
- rl-4: a lasso on 28 inputs passed its planted gate on weekly data (45% of the ceiling at
  IC 0.10); PPO failed. rl-5/rl-6 closed the perp line on power grounds.

## Data (`research/lib/rl7_data.py`, all from the local cache)

80 monthly series, 49,566 market-months of returns before the warm-up:

| Group | Series | Kind of return | Signal gap g | Cost a side |
|---|---|---|---:|---:|
| US10 | French US 10 industries, month-end, 1926-08.. | total return, cash 0 (pooled-1) | 0 | 2 bps |
| DEV13, WIDE10 | 23 country indices (Yahoo, as pooled-1), 1965-2003 starts | price, local currency, cash 0 | 0 | 2 bps |
| ETF8 | IWM EFA EEM IEF LQD VNQ DBC SLV, 2000-2006 starts | total return, cash 0 | 0 | 2 bps |
| USB3 | US 2/10/30-year Treasury rebuilds (data-long-3), month-end | excess of the 3-month bill | 1 | 2 bps |
| GOV9 | 9 foreign 10-year bonds (monthly averages), 1955-1989 starts | excess of the local 3-month rate | 1 | 2 bps |
| FX9 | 9 G10 currencies against USD, 1973.. | excess (carry included) | 1 | 3 bps |
| COM8 | 7 BLS PPI commodity indices 1926-1967.., gold 1971.. | spot change, cash 0 | 2 (gold 1) | 10 bps |
| P4 | US (Shiller) 1871-1927, GB, DE, FR before 1927-07 (NBER) | price, cash 0 | 1 (GB 0) | 2 bps |
| N5 | DK FI IE NO SE (French country files) 1975-1991.. | total return, USD | 0 | 2 bps |

Gaps and costs are the earlier lanes' (daily-derived US bonds and currencies get g = 1
because H.15/H.10 values are public a day to a week late; DE and FR pre-1927 use g = 1 on all
their segments). Each run of consecutive months is a segment with its own warm-up.

## Features (fixed now; past prices only)

For the return of month t of a segment, with s = t - g and L the log level after each return
(the signal sees returns through month t - 1 - g, exactly as pooled-2's monthly `tsmom12`):

- `m1, m3, m6, m12, m24`: (L[s] - L[s-k]) / (sigma36 x sqrt k), k = 1, 3, 6, 12, 24 months
- `up1, up3, up6, up12`: 1 if L[s] > L[s-k], else 0 (`up12` is `tsmom12`'s own signal)
- `dvol`: ln(sigma12 / sigma36), recent against longer volatility
- `drift`: (L[s] - L[0]) / (s x sigma36), the segment's own average past return in risk units

sigma12 / sigma36: standard deviation (ddof 1) of the last 12 / 36 monthly log returns
through s - 1. A month is eligible when s >= 36. `tsmom12` and the learners are compared on
exactly the same eligible months. Features are standardised with the mean and standard
deviation of the rows a model is fitted on. Target: y = r_t / sigma36 (the month's return in
risk units), clipped to [-5, 5] for fitting only.

## Learners (fixed now; no other is run)

1. **`lasso-sign`** (the learner that passed rl-4's gate): lasso of y on the 11 features with
   an intercept; penalty from the grid alpha in {0.0005, 0.001, 0.002, 0.005, 0.01, 0.02,
   0.05} (scikit-learn's `Lasso`, standardised inputs), chosen by the lowest mean squared
   error in a purged 5-fold time CV inside the rows it is fitted on (5 contiguous blocks of
   calendar months with equal row counts; fit rows whose month is within 36 months of the
   validation block are dropped). Policy: hold 1 if the forecast > 0, else 0 (the same
   long-or-flat action as `tsmom12`).
2. **`pg-lin`** (the learned-policy / RL-style learner): a linear-sigmoid policy p =
   sigmoid(w . x + b) in [0, 1], trained by gradient ascent on the mean monthly reward
   p y - (1/2) (p y)^2 (mean-variance in risk units, risk aversion 1) minus (0.01/2) |w|^2.
   Full batch, Adam (learning rate 0.05, betas 0.9/0.999), 500 steps, start w = 0, b = 0, no
   seed (deterministic), no early stopping. Actions do not move prices, so this is the
   contextual-bandit form of policy gradient with the exact gradient instead of a sampled one
   (no REINFORCE variance; the reason PPO failed in rl-3/rl-4 was that variance at this
   signal size). No MLP: with this signal-to-noise the extra width is more to overfit, and
   rl-4 found the inputs, not the optimiser, to be the limit.

Net return of any rule in a month: p_t r_t - cost x |p_t - p_(t-1)| (p before a market's first
scored month = 0). Both learners are fitted **once** on the training cell and then frozen (no
refit schedule: every training target is before every held-out decision).

## Split (fixed now; seed 707)

- A series is **spanning** if it has at least 60 eligible months before 1990-01 and at least
  60 from 1990-01. Within each group, the spanning series (sorted by name) are permuted with
  `numpy.random.default_rng(707)` per group in the table order above; the first floor(n/2) are
  **train markets**, the rest **holdout markets**. Series with fewer than 60 eligible months
  from 1990 are train markets (P4); series with fewer than 60 before 1990 are holdout markets
  (most country indices, the ETFs, three GOV, three N5).
- **Training cell:** train markets x months before 1990-01. Nothing else is used to fit,
  choose penalties or run the gate.
- **Primary holdout (the only judged cell):** holdout markets x 1990-01..2025-10.
- Reported, not judged, from the same single run: train markets x 1990-01.. (new years only)
  and holdout markets x before 1990 (new markets, same years).

## Planted-signal gate first (rl-4's design, adapted; training cell only)

Planted input `peek_s = s x yz + sqrt(1 - s^2) x e`, where yz is y (unclipped) standardised
over the training cell and e is one N(0, 1) draw per row (seed 7070, row order fixed), the
same draw at every strength. Strengths: **none** (no `peek` column), **0.00** (pure noise),
**0.05** (main rung; a monthly IC of 0.05 is about the size of a real monthly trend edge),
**0.10**. Each learner (with `peek` as a 12th input) is run by a purged 5-fold time CV over
the training cell (folds and purge as above; the lasso's penalty CV nested inside each fold's
fit rows), giving out-of-fold positions for every training-cell row.

- Lift L(s): pooled paired Sharpe difference, learner at s minus the same learner at 0.00
  (same noise draw), per market over its training-cell months, equal-weight mean over the
  train markets, SE from pooled-2's joint circular 12-month block bootstrap (2,000 draws,
  seed 0); one-sided p from z.
- Ceiling L*(s): the same lift for the same learner told the inputs: features `up12` and
  `peek` only (for the lasso: plain least squares, alpha 0).
- **A learner passes the gate if all hold:** (G1) L(0.05) > 0 with p < 0.10; (G2) L(0.05) >=
  L*(0.05) / 3, with L*(0.05) > 0; (G3) L(0.10) > 0 with p < 0.10; (G4) planted noise costs at
  most 0.025 and does not "help": the paired difference learner at 0.00 minus learner at none
  is >= -0.025 and not > 0 at p < 0.10.
- Reported, not gated: the realised IC of `peek`, the lasso's coefficients and penalties per
  fold, D of each run against `tsmom12` on the training cell (out of fold).
- **If neither learner passes, nothing is run on held-out data**; the write-up says why. Only a
  passing learner goes to the final run.

## The final run (once, after the gate rows are pushed)

Each passing learner is fitted on the whole training cell (11 features, no `peek`), frozen,
and applied to every eligible month of every series. **Statistic:** D = equal-weight mean over
the primary-holdout markets of Sharpe(learner) - Sharpe(`tsmom12`), monthly net returns,
annualised with sqrt 12, cash 0 (excess series are already excess), same months; SE from the
joint circular 12-month block bootstrap of calendar months (2,000 draws, seed 0; pooled-2's
`bootstrap`), z = D / SE.

**Bars and readings (fixed now):**

- **Pick candidate:** z >= **4.70** (the project bar, `register/BAR.md` rows through
  2026-11-25 01:16: 4,126 tries, N = 1,116, 506 effective trials at rho 0.55; Bonferroni
  p <= 9.9e-05) **and** D > 0 in at least 3 of the 4 asset classes (equity, rates, fx,
  commodity) of the primary cell. Even then it would only earn a held-out-year test, not a
  live slot.
- **Positive, below the bar:** 1.96 <= z < 4.70 (one-sided 5% Bonferroni over the 2 learners,
  the family bar): a lead to test again on new data, not a pick.
- **Killed:** the one-sided 95% upper bound D + 1.645 SE < +0.05 (no edge of 0.05 a market).
- Otherwise: **not shown** (the test cannot tell).

**Expected outcome, stated now:** a pass is very unlikely. The best pooled per-market edge any
rule has shown over `tsmom12` here is +0.063 (`e4`, z 1.55); pooled-2's SE for a rule close to
`tsmom12` was about 0.03, and a learner's rule is farther from `tsmom12` (larger SE, perhaps
0.05). z 4.70 needs an edge of roughly +0.15 to +0.25 Sharpe a market, three to four times the
best seen. **What a fail means:** with about 100x the market-months of rl-1..rl-6, a small
learner on past prices does not beat a fixed 12-month trend rule out of sample; adding data
does not rescue learned price-only policies, so the RL line stays closed for price-only
inputs. If the gate fails, it means that even the training cell (tens of market-decades) is not enough for the
pipeline to find a monthly IC of 0.05: a learned policy could not be told apart from noise at
the edge sizes that matter.

## Tries and compute

- Idea `rl-7-control` (kind `control`, not selectable) for every gate run: per learner the
  strengths none/0.00/0.05/0.10 (4) and the ceiling at 0.00/0.05/0.10 (3): 14 rows, plus one
  `tsmom12` training-cell reference row.
- Idea `rl-7`: one `variant` row per learner that reaches the final run (primary cell), one
  `baseline` row for `tsmom12` on the primary cell, `robustness` rows for the two secondary
  cells and the per-class figures.
- numpy and scikit-learn on the CPU, one process, well under 2.5 GB and a few minutes. No GPU.
- Code: `research/lib/rl7_data.py`, `research/lib/rl7.py`; tests `tests/test_rl7.py` (offline,
  made-up data). Write-up: `research/rl-7.md`, tables `research/results/rl-7.md` (+ `.json`).
