# wide-19: `tsmom12` with credibility-weighted drifts (`cred-xs`, `cred-lr`)

Lane wide-19, written 2026-11-24 about 23:50 UTC, **before any return of either rule below was
computed** (no dry run yet either). Candidates A1 and A2 of `research/wide-19.md`, step 1.

## What was seen before this card (disclosed)

Only the record: `tsmom12` 1.05 on the primary test, equal weight (holding) 0.88; the trend-tune
surface (6-12 months a flat plateau, any threshold, best of 98 settings +0.08, luck alone +0.17);
`xtsmom` (gate stocks on the bond trend) tied; `crowded-trend` (halve the book when all are in
trend) -0.07; `breadth-gate` noted but never tested; wide-18's `huber52` (the same 52 weekly
returns, robust mean) equal to `tsmom12`. The asset start dates of the six (SPY 1993, QQQ 1999,
TLT 2002, GLD 2004, BTC 2012, ETH 2016), so until QQQ is eligible (2000-03) the book is SPY
alone. No number of either rule and no value of Z, on any data.

## Hypotheses

- **H1 (`cred-xs`)**: a year of one asset's drift is a noisy estimate of its current drift; the
  book's average drift is a less noisy complement. Buhlmann-Straub credibility (the minimum-MSE
  linear estimate) beats the asset's own sign on Sharpe.
- **H2 (`cred-lr`)**: the same, with the asset's own long-run drift as the complement (the
  actuary's "manual rate"): the data decide how far the rule moves from the year's sign toward
  holding.

## Rules (frozen)

Both keep everything of `tsmom12` but the per-asset signal: `c.weekly(c.slots(signal))`, each
Friday an eligible asset (a year of bars) with signal true gets 1/n of the book (n = eligible
assets), else cash; gym costs, gym band, weights repeated daily, fills next open.

Common inputs on decision Friday `d` (only bars visible on `d`):
1. Friday grid `tau_k = d - 7k`. An asset's weekly close at `tau` is its last close dated on or
   before `tau`; weekly log returns between consecutive grid closes, from the first grid date
   with a close.
2. `x(s, tau)` = mean / sample sd (ddof 1) of the 52 weekly log returns ending at `tau` (a
   year's drift in risk units; its sign is the sign of the 52-week log return, so with Z = 1
   the rule is `tsmom12` up to 364 vs 365 days). Undefined with fewer than 52 returns or sd 0.
3. `v = 1/52`: the sampling variance of `x` when the true drift is constant (Buhlmann's
   expected process variance in these units). Stated, not estimated.
4. `Z = a / (a + v)`, with `a` floored at 0. If `a` cannot be estimated (below), `Z = 1`.

- **`cred-xs` (variant)**: at each grid Friday `tau <= d` with at least two assets having
  `x(s, tau)`, the cross-sectional sample variance (ddof 1) `S2(tau)` of those `x`.
  `a` = mean over those Fridays of `S2(tau) - v` (Buhlmann's estimator of the variance of
  hypothetical means; needs at least 52 such Fridays, else `Z = 1`). Collective
  `xbar(d)` = mean of `x(s, d)` over the assets that have one. Signal:
  `Z x(s, d) + (1 - Z) xbar(d) > 0`.
- **`cred-lr` (variant)**: `mu(s, d)` = mean / sample sd of all of the asset's visible weekly
  log returns (expanding). `a` = mean over the pool of (asset `s`, Friday `tau <= d`) with
  `x(s, tau)` defined, taken only from assets with at least 156 weekly returns, of
  `(x(s, tau) - mu(s, d))^2 - v` (needs at least 52 pool points, else `Z = 1`). One `Z` for all
  assets. Signal: `Z x(s, d) + (1 - Z) mu(s, d) > 0`.
- In both, an asset without `x(s, d)` gets `tsmom12`'s signal (365-day log return > 0). No
  other setting is run. Nothing is tuned: v is theory, a and Z are estimated each Friday.

## Data, tests, costs

- Primary test: the six assets (SPY, QQQ, TLT, GLD, BTC, ETH), decisions 1994-02-01 ..
  **2025-10-31** (the lane's train cut; both books on the same window), total-return prices,
  gym costs. The held-out year is not loaded for decisions and not scored.
- Out of universe, signs only (`robustness` rows): `etf` (IWM, EFA, EEM, IEF, LQD, VNQ, DBC, SLV)
  and `idx` (S&P 500, Nikkei 225, FTSE 100, DAX price indexes, from 1962 or their first year).
  Both sets are wider cross-sections than the six, where credibility should do best.
- Comparator: `tsmom12`, re-scored with `log=False` on each set and window.

## Statistic and pass bar

- dSharpe = Sharpe(rule) - Sharpe(`tsmom12`), daily returns, 365 days, paired stationary
  bootstrap (20-day blocks, 2000 draws, seed 0; wide-16's `boot`). Two cash conventions on the
  six: cash at 0 (the protocol's, what `tries.md` logs) and above the 13-week bill.
- **Pass (each rule separately)**: z = dSharpe / SE >= **4.70** in both cash conventions on the
  primary test (`BAR.md`, N_eff 500; the SE is the rule's own paired SE, so the bar in Sharpe
  units follows its correlation with `tsmom12`), **and** dSharpe > 0 on `etf` and on `idx`.
  Anything else is a fail. The table gives the correlation of daily returns with `tsmom12`, the
  edge 4.70 x SE the rule would have needed, and Z at the end of each set and its median over
  the decisions.
- Reported, not a pass: z >= 3.25 (the bar at the ONC end of the count) is called "the counting
  method decides".
- Power (stated before the run): I do not know Z. If Z is near 1, both rules are `tsmom12`
  (dSharpe about 0). If Z is near 0, `cred-xs` is a book-level switch (all eligible assets in or
  out on the average drift) and `cred-lr` is close to holding, which lost 0.17 to `tsmom12` on
  this test. Expected |dSharpe| under 0.15 at an SE of 0.03-0.08: z within about +-2.5.
  **Expected result: fail for both**; the estimated Z is reported either way, as the data's
  answer to "how much is one year of an asset's own trend worth".

## Logging

Each rule: one `variant` row (six, cash 0), robustness rows for `/bills`, `@etf`, `@idx`
(harness `tries.md` rows; train curves go to the returns store as the harness does). The ten
killed candidates of step 1 get `note` rows. Script `research/lib/wide19.py`, tests
`tests/test_wide19.py`, results `research/results/wide-19.md`. One dry run (`DRY=1`, last 120
days, nothing logged) is allowed before the real run; its output is plumbing only.
