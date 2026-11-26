# ownvol-indep-1: does `own_vol_70` beat `tsmom12` on stock data it has never seen?

Lane `ownvol-indep-1`, written 2026-11-26 00:25 UTC **before any own-vol return on any series
is computed in this lane** (no calibration run either: the power section uses only published
SEs). Seen before writing: the segment spans of e4-indep-1's data (first/last month, gap,
scored months; no rule run) and e4-indep-1's published `e4` and `tsmom12` numbers (#198).
e4-indep-1's code ran `pooled2_core.run_monthly`, which also builds `vt-own-70-x`, but it never
read, printed or stored it (`RULES2`; grep of `results/e4-indep-1*.json` and `.md` for "own":
0 hits). Research only: fake money, cached keyless data, no change to the gym, the daily runner,
the scoreboard, the workflows, the live strategies or the `own_vol_70` paper book. Nothing after
2025-10-31 is read.

## Question

`own_vol_70` (the `tsmom12` sleeve sized by its own volatility for a 70% mean share) is the
best-looking risk dial, not a proven edge: +0.03..+0.10 Sharpe over `tsmom12` on the six live
assets 1994-2025 (risk-menu-3, #110, about 1 SE; +0.06 the usual figure), +0.022 a market
pooled over pooled-1's 41 stock markets (#142, SE 0.016, z 1.37, not shown), killed on bonds
and currencies (#159: -0.010, upper +0.024) and so read as **"equity-only at best"**.
ownvol-anatomy-1 (#172) found the stock lean is risk removal (risk channel +0.024 a market).
It has never been scored on independent data (checked: no `own` row in `tries.md` on pre-1927
or Nordic series; e4-indep-1's rows are `e4` and `tsmom12` only). **On stock markets and
periods where own-vol was never scored, is own-vol's Sharpe higher than `tsmom12`'s?** One
pre-specified hypothesis, one direction. Kill-only: a pass is not a pick.

## Data (e4-indep-1's, unchanged)

`e4indep1.PRIMARY` and `e4indep1.SECONDARY`, loaded with `e4indep1.load_segs` and its segment
rule (a segment counts with at least 48 scored months; segments of a market run separately,
each with its own warm-up, scored months concatenated). Gaps g as in e4-indep-1's card (1 for
monthly averages or unstated observation dates, 0 for point prices).

- **P4 (deciding):** US (Shiller, 1871-1927, g 1), GB (NBER m11012a 1867-1914 and m11012b
  1919-1924, g 0), DE (NBER m11023a 1870-1913, g 1), FR (NBER m11024 1899-1914 g 0,
  1919-1927 g 1). Price returns. 171 scored market-years, all before 1927-07: no overlap in
  time with any series own-vol was scored on (#110 from 1994, #142 from 1927-07, #159 from
  1927-04).
- **N5 (secondary, shown, not deciding):** Denmark, Finland, Ireland, Norway, Sweden (French
  country files, USD, with dividends, g 0, 1975/1988-2025-10). Never scored for own-vol, but
  same calendar as the 41.

## Rules (frozen code, unchanged)

`pooled2_core.run_monthly`, as frozen in `cards/pooled-2.md` and called by e4-indep-1:

- `tsmom12`: position over month t = 1 if level(t-1-g) / level(t-13-g) > 1, else 0; 2 bps a
  side.
- `own_vol_70` = **`vt-own-70-x`, monthly form**: the `tsmom12` sleeve (net of its 2 bps) x
  min(1, k / sigma), sigma = sd (ddof 1) x sqrt 12 of the last 36 monthly sleeve returns
  (through t-1-g, only months after the segment's first scored month), k = `solve_k` over all
  sigmas seen so far for a mean share of 0.70, monthly reset, 24 sigmas at the 0.70 share
  before sizing starts, share drifts within the month, 5 bps on the traded notional at a reset.
- **Deviation from the live rule (stated, not tested):** the live `own_vol_70` uses a 52-week
  sigma from daily data, resets monthly, same target, cap, k rule, warm-up count and reset cost.
  These data are monthly only, so sigma is from 36 monthly returns (pooled-2's frozen monthly
  form, used there on 10 monthly markets). No other change.
- **Warm-up dilution (a property of the frozen code, kept):** sizing starts after 36 + 24
  months (+ g) from a segment's first scored month; before that own-vol is the sleeve at a
  fixed 0.70, so d is about 0 there. From the spans, the sized share of scored months is US
  0.91, GB 0.81 (its 1919-1924 segment is all warm-up), DE 0.88, FR 0.55; mean 0.79 (about
  0.94 on the 41, weekly code). An edge of a given size on sized months shows up as about 0.84
  of that size in D.

## Statistic

d = Sharpe(own-vol) - Sharpe(`tsmom12`) per market on its scored months (monthly mean / sd x
sqrt 12, cash 0). **D = equal-weight mean of d over P4's four markets.** SE: the joint circular
block bootstrap of calendar months (12-month blocks, 2,000 draws, seed 0), `pooled2_core.cells`
/ `bootstrap` / `pooled`, exactly as e4-indep-1 and pooled-2. z = D / SE.

## Pre-registered rule (P4 decides; one-sided)

- **Confirmed** (independent replication of the stock lean): **z >= 1.645**.
- **Contradicted**: **D + 1.645 SE < +0.022** (the one-sided 95% upper bound is below the
  41-market size, #142).
- **Not confirmed, not contradicted**: neither.
- Shown with the reading, not deciding: whether the upper bound is also below +0.06 (#110's
  usual size).

N5 gets the same three readings, reported, not deciding.

**What each outcome does to "equity-only at best":**

- Confirmed: the stock lean has one independent replication; the reading becomes "a small
  stock-market edge, replicated once". Still far from the bar (z >= 4.70), not a pick, no live
  change.
- Contradicted: the 41's +0.022 does not carry to independent stock data. "Equity-only at
  best" becomes **"no Sharpe edge shown on any asset class; a risk dial only"** (lower swings
  and drawdowns at a lower mean, no Sharpe claim). The 41's D stands as measured. Not a retune
  trigger. The paper book is not changed by this lane (the owner's / lead's call).
- Neither: the reading stays "equity-only at best, unconfirmed", and these independent data are
  spent for own-vol.

## Shown cells (not deciding)

Per market d (US, GB, DE, FR) and the count of d > 0; **without each market, Germany named**
(e4-indep-1's pool leaned on Germany); **sized months only** (each segment's first 60 + g
scored months dropped, the warm-up); g = 1 for every series; cost 50 bps a side (sleeve) with
the reset cost unchanged; blocks of 6 and 24 months; US with Shiller's dividends; 1867-1897 vs
1898-1927; N5 and its per-market d; per market the Sharpe, max drawdown and average share
(the risk-dial description); an inverse-variance combination of P4 with the 41 (+0.022, SE
0.016; P4 is independent of it in time).

## Bars (for context)

A confirmation test of one pre-specified hypothesis, not a selection: one-sided 1.645 is its
level, not the bar for a new pick. `research/register/BAR.md` (rows through 2026-11-25 23:32):
4,492 distinct tries, N = 1,123 selectable + live, N_eff = 509 at measured rho 0.55; a new
pick needs **z >= 4.70** (DSR 0.95; Bonferroni p <= 9.8e-05). Nothing goes live from this lane;
the held-out year stays unspent.

## Power (from published SEs only; no own-vol return computed)

On the 41 the own-vol d had 0.39 times `e4`'s SE (0.016 against 0.041, #142). Applied to
e4-indep-1 on the same P4 data: to its realised `e4` SE (0.041) gives **expected SE 0.016**;
to its pre-registered expected SE (0.064, c 0.3) gives 0.025. (Warm-up months add no variance
to d, so the dilution shrinks the SE as well; ignored, cautious.)

| Expected SE | Power at D +0.022 (#142) | at +0.018 (+0.022 diluted) | at +0.06 (#110) | at +0.05 (diluted) | MDE at 80% | P(contradicted) if true D = 0 |
|---:|---:|---:|---:|---:|---:|---:|
| 0.016 | 0.39 | 0.31 | 0.98 | 0.93 | 0.040 | 0.39 |
| 0.025 | 0.22 | 0.18 | 0.77 | 0.64 | 0.062 | 0.22 |

**Low power at the 41's size** (one chance in three to five of confirming it if true, and only
one in four to five of contradicting it if the true edge is zero), **good power at #110's
size**. The likely outcome is "neither"; an edge as large as +0.06 would very likely show.

## Logged

One `variant` row per pool (P4 deciding, N5 secondary), a `robustness` row per market and rule
and per check, in `tries.md`'s format. Card not amended after numbers; any deviation goes in
`research/ownvol-indep-1.md`.
