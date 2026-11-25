# Card rev-costloss-1: the `tsmom12` exit scored as a crash warning (relative economic value)

Lane rev-costloss-1, 2026-11-25 00:30 UTC (night). Written and pushed before any number of
this card was computed. Descriptive only: no new rule, nothing selected, nothing tuned. Train
data only (no session after 2025-10-31 is used). Idea `rev-costloss` (wide-19's M2, #173).

## What has been seen before this card

insure-1/insure-2's published tables (share of each 25% fall avoided 0.50 against 0.27 at
random dates; fast falls of three months or less: share about a third, net about -15 log
points; slow falls over a year: share 0.63) and gap-2002-1's split (2002-2025, 11 French
series, cash 0: fall gain +7.4, rebound lag -7.5, calm drag -1.9 log points a year; S&P 500
total return +4.9 / -4.3 / -1.7). No hit rate, false-alarm rate or value curve of the exit has
been computed by anyone in the project.

## Question

Read the rule's exit as a binary forecast, the way meteorology scores a warning: for which
cost/loss ratios C/L is "`tsmom12` is out" a valuable crash warning at all, and does that
match the calm-drag against crash-gain trade-off measured in insure-2 and gap-2002-1?

## Data (existing loaders, nothing fetched)

- **US, long history (primary):** the French daily US market, 1927-07-02 .. 2025-10-31, and
  the 10 value-weighted industries, exactly gap-2002-1's `french()` (insure-1's `build`, the
  rule's paper series, Friday decisions, 2 bps a side, total-return index as holding).
  Reported for the market alone, and pooled over the 11 series (contingency tables summed).
  Eras as insure-2: 1927-1961, 1962-2001, 2002-2025 (by forecast date).
- **The six:** SPY, QQQ, TLT, GLD, BTC, ETH, adjusted train bars
  (`harness.load_history("train")`), the rule's paper series per asset alone
  (`trend_tune.paper`, as insure-1 builds it; positions read back with `insure1.infer_pos` at
  the asset's one-way cost, checked to reproduce the paper returns). Per asset, and pooled.

## Forecast and event (fixed here)

- **Forecast unit:** each Friday decision f on which the asset is eligible. Warning W = 1 when
  the rule's position for the sessions after f (to the next Friday) is 0 ("out"), else 0.
- **Event E(X, N):** the asset's total-return close falls at least X below its close at f at
  some session in (f, f + 7N days]: min(close) / close(f) <= 1 - X. Only Fridays with the whole
  window inside the data (f + 7N days <= the last session, at most 2025-10-31) count.
- **Grid, all reported, none selected:** X in {5%, 10%, 20%} x N in {4, 13, 26} weeks.
  **Primary: X = 10%, N = 13 weeks** (a 10% fall within a quarter). For the coins most cells
  have base rates near 1, so their readings are thin; reported, not dropped.
- **Contingency table:** hits a (W=1, E=1), false alarms b (W=1, E=0), misses c (W=0, E=1),
  correct rejections d. Base rate s = (a+c)/n, hit rate H = a/(a+c), false-alarm rate
  F = b/(b+d), Peirce skill score PSS = H - F.

## Relative economic value (Richardson 2000, QJRMS 126; static cost-loss model, Murphy 1977)

A user protects at cost C or risks a loss L if the event comes unprotected; alpha = C/L in
(0, 1). Mean expense per forecast, in units of L:

- climatology (always or never protect, whichever is cheaper): E_clim = min(alpha, s)
- perfect forecast: E_perf = s alpha
- the warning: E_fc = alpha (H s + F (1 - s)) + (1 - H) s
- **V(alpha) = (E_clim - E_fc) / (E_clim - E_perf)**; V = 1 perfect, V = 0 no better than
  climatology, V < 0 worse. Maximum at alpha = s, where V = PSS.

Reported: V on alpha in {0.02, 0.05, 0.10, 0.15, 0.20, 0.30, 0.40, 0.50, 0.60, 0.80}, V_max =
PSS, and the range of alpha with V > 0 (on a grid of step 0.005).

## Bridges to what the project already measured

1. **Random timing:** the weekly warning sequence rotated by k weeks (k uniform on
   [52, n - 52]; for the 11 pooled series one k for all, as insure-1), 1,000 rotations, seed 0:
   same exposure and spell lengths, random dates. Reported: median and 5-95% of PSS and of V
   at the primary alpha points, and p = share of rotations with PSS >= the rule's.
2. **A holder's own cost/loss ratio.** With r the asset's simple return over the week after
   f (the sessions the warning acts on): protecting when nothing comes costs the forgone
   return, C = mean(r | E=0); an unprotected event costs L = mean(r | E=0) - mean(r | E=1)
   more than a quiet week. alpha_hold = C / L. Reported with V(alpha_hold).
3. **Money value (the same ratio in returns, cash at 0, no costs):**
   V_money = (sum r_rule - sum r_hold) / (sum r_perfect - sum r_hold), with r_rule = (1 - W) r,
   r_hold = r, r_perfect = (1 - E) r (out exactly in event weeks), log returns summed per
   week. Its sign is the sign of the rule's weekly gap to holding.
4. **Where the false alarms and the misses sit:** each forecast Friday is labelled by insure-1's
   25% / 25% zigzag on the same index: fall (peak, trough], rebound (trough, min(trough + 365
   days, next peak)], calm. Shares of b (false alarms) and c (misses) per part; and H for event
   weeks inside falls split by fall speed (peak -> trough <= 92 days fast, 93-365 medium,
   > 365 slow, insure-1's classes).

## What readings would mean (stated before the numbers)

- PSS > 0 and above the rotations' 95%: the exit has real skill as a warning, the REV form of
  insure-1's "0.50 against 0.27". PSS inside the rotations: no skill as a binary warning
  (would contradict insure-1; then the 25% fall definition and the 10%/13-week one differ).
- The V > 0 range of alpha: the users for whom the warning beats climatology. Expected
  (stated so it can be wrong): on the US market a PSS of about 0.2-0.35 and V > 0 for alpha
  from a few percent up to about 0.5; nobody with alpha above roughly 0.6 gains.
- alpha_hold inside the V > 0 range with V(alpha_hold) clearly positive while V_money is about
  0 or negative: the binary score flatters the exit, because it counts a missed 10% fall the
  same as a missed 40% one and scores rebound weeks spent out as cheap false alarms; the gap
  numbers (rebound lag + calm drag about cancel the fall gain) are the money truth.
  V(alpha_hold) about 0 and V_money about 0: the two framings agree that for a plain holder the
  warning is worth about nothing, matching gap-2002-1.
- Most false alarms in rebound parts: the late buy-back is the warning's main cost (REV form
  of insure-2's "handed back"). Most in calm parts: the calm drag is.
- H lower for fast falls than slow: the known weakness (1987, 2020) in warning terms.

## Rows and bar

- One `tries.md` row of kind `note` (a re-score of a logged configuration, as gap-2002-1): no
  strategy try, not selectable, nothing for `ledger/tries.jsonl`.
- Bar for scale only (BAR.md): N 504, z >= 4.70, Bonferroni p <= 9.9e-05 for a new pick. Not
  applicable: no pick. A rotation p is descriptive (1,000 rotations cannot reach 1e-4).
- Code `research/lib/revcostloss1.py`, tables `research/results/rev-costloss-1.md`, write-up
  `research/rev-costloss-1.md`, tests `tests/test_revcostloss1.py` (formulas, offline).
