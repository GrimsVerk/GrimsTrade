# vm-style-1: does market-volatility management (DMU 2024) make the century style book add to `tsmom12`?

Lane `vm-style-1`, 2026-11-25 (night). Branch `vm-style-1` from `main` (`fe627bb`), PR #179.
Research only: fake money, cached keyless data (read-only), no change to the gym, the daily
runner or the live strategies. Nothing after 2025-10-31 parsed; held-out year untouched.
Card (pushed before any number, `d7791bd`, not amended): [`cards/vm-style-1.md`](cards/vm-style-1.md).
Code pushed before the run (`2630295`): `lib/vm_style.py` (pure parts; tests
`tests/test_vm_style.py`), `lib/vm_style_run.py` (one run, 12 s). Tables:
[`results/vm-style-1.md`](results/vm-style-1.md). Shorts are research-only (B7) and Ken French
portfolios are not tradable in the gym, so the verdict is informational.

## The answer on one screen

**Fail, by the card's rules: out-of-paper z 1.58, full-sample z 2.40, against a bar of 4.70.
Kill rule K2 is hit: the managed book adds less to `tsmom12` than the unmanaged
`xs-century-1` book on the same months (z 2.46 out of paper). Market-volatility management of
the style book is dead.** Outside the paper's 1977-2020 window the conditioning does nothing:
the rule's net Sharpe is 0.38 against 0.37 for its own unconditional twin (+1%, t 1.2), and
0.00 apart in 1938-07..1976-12.

- **The method, verified in the paper** (DeMiguel, Martin-Utrera and Uppal, JF 79(6) 2024,
  section I.B-C): weights theta_k,t = a_k + b_k / sigma_t, with sigma_t the SD of the daily
  market returns in month t (volatility, not variance: the paper says so to cut costs); (a, b) >= 0
  from a mean-variance problem with costs in the objective, gamma 5, expanding window, first
  window 120 months, re-estimated monthly. The paper's comparator is the same problem with b = 0
  (UMV): out of sample 1977-2020, net Sharpe 1.06 vs 0.94 (+13%).
- **Here**: the eight sleeves of `xs-century-1` (HML, UMD, bond value / momentum / carry, FX
  value / momentum / carry), unchanged and at its costs, as DMU's factors; scaling trades charged
  per sleeve (0.50% per unit for US stocks, 5 bps for bonds and FX; no netting across sleeves,
  which the paper credits for much of its gain). Out of sample 1938-07 .. 2025-10.

| Out-of-sample book (net) | Sharpe, full | Sharpe, out of paper | alpha IR vs `tsmom12`, out of paper | z, out of paper (decides) | z, full |
|---|---:|---:|---:|---:|---:|
| **CMV** (DMU, market vol) | 0.34 | 0.38 | +0.28 | **1.58** | 2.40 |
| UMV (b = 0, the paper's comparator) | 0.32 | 0.37 | +0.28 | 1.56 | 2.29 |
| Own-vol twin (each sleeve by its own vol) | 0.28 | 0.36 | +0.27 | 1.51 | 2.08 |
| `xs-century-1` book (equal weights, unmanaged) | 0.43 | 0.53 | +0.38 | 2.46 | 2.92 |

Out of paper = 1938-07..1976-12 plus 2021-01..2025-10 (520 months, 43 years). Kill rules: K1
(CMV <= UMV) not hit, by 0.01 of Sharpe; K2 hit; K3 (own-vol twin >= CMV) not hit, by 0.02.

## What it means

1. **The paper's gain shows up inside its own window and nowhere else.** CMV over UMV: +9%
   net Sharpe in 1977-2020 (the paper's +13% is on nine equity factors with netting), +0% in
   1938-07..1976-12, and the two are equal to two decimals in every decade from the 1940s to the
   1970s: before 1977 the optimiser, with costs in its objective, finds no market-volatility
   timing worth paying for and sets b to 0 (in all 462 months; review note 2). Gross (R1) the same pattern: CMV over UMV
   +12% on the full sample, 0% out of paper (both 1.09). This is the outcome the pre/post
   split was built to catch; it is consistent with the conditioning being fitted to 1977-2020.
2. **The optimiser costs more than the timing earns.** Both mean-variance books (CMV, UMV) lose
   to `xs-century-1`'s plain equal-weight book (net Sharpe 0.34 / 0.32 against 0.43, full),
   most likely because estimated means tilt the weights (the largest mean weights are on HML,
   bond carry and FX value) and the books run at about 15% volatility on about 8 units of gross
   notional, so every re-estimate is a costly trade. Gross they look strong (CMV full z 8.0, UMV out of paper 5.8), net they do not:
   the same story as `xs-century-1` (costs decide), with an added layer of estimation error.
3. **It is not vol sizing in disguise either, because there is nothing to disguise.** The own-vol
   twin is no better (0.36 out of paper, 0.28 full) and the variance form (R4, 1 / sigma^2)
   is a little worse than the volatility form. All three conditional variants sit within 0.02
   of Sharpe of the unconditional one out of paper.
4. **Nothing changes for the book.** Shorts stay parked (B7). With `xs-century-1` (z 2.75)
   and this (z 1.58 out of paper) the long-short style family has now failed twice in the
   alpha form; the only rows above the bar are gross.

## How sure

- One run of the pre-registered evaluation; card not amended; code and tests pushed first. The
  tests check realised volatility per month, the one-month lag of the conditioner, the exact
  NNLS solution of the constrained mean-variance problem (KKT), no look-ahead in the walk,
  recovery of a planted Moreira-Muir effect, the cost of scaling trades, and the entry of a
  late sleeve after 120 months. The run asserts that the sleeves equal `xs-century-1`'s.
- **Robust to every cost setting the card named.** Out-of-paper z: 1.35 to 1.59 at US scaling
  costs 1.0% to 0.25% (R3), 2.87 with the cheaper published momentum cost (R2; UMV 2.85), 1.53
  with variance (R4). Only gross rows clear 4.70 (R1: 5.40; UMV gross 5.84), and gross rows cannot
  decide.
- **Deviations from the paper (all stated on the card).** Sleeves instead of stock portfolios:
  no netting of trades across sleeves (the paper's "trading diversification", which it says
  turns four of nine managed factors from negative to positive net mean), so costs here are
  harsher than the paper's main case. US scaling cost 0.50% per unit traded, one number for
  1938-2025 (from Jones 2002 as recalled, not re-read). No MKT factor (not in the book). Unequal
  histories: a sleeve enters after 120 months and the window restarts at the latest entrant's
  first month (the paper has one common window). The own-vol twin uses six monthly returns for
  bond and FX sleeves (no daily data).
- **What the netting caveat can and cannot change.** Netting lowers costs, so it could lift the
  absolute numbers; it cannot create a gross timing gain where there is none: gross, CMV and
  UMV are equal out of paper (1.09 each).
- **Trial count.** 16 rows logged: 3 `variant` (CMV, UMV, own-vol twin), 2 `baseline` (the
  comparator, the unmanaged book on the same months), 11 `robustness` (R1-R4 and the sample
  splits). The bar was not lowered for the comparator or for this being the second try in the
  family after a near miss.

## Review notes (added after the run, 2026-11-25 UTC; card unchanged)

1. **Not all 520 "out-of-paper" months are free of the paper's data.** DMU's sample starts in
   1967-01 and 1967-01..1976-12 was their first estimation window, so 120 of the 520 months
   (1967-1976) are data the paper fitted on, though not data it scored. The cleanly unseen
   part is 1938-07..1966-12 (342 months) and 2021-01..2025-10 (58 months). The card's split is
   kept as fixed; this narrows how much it can claim.
2. **The fitted b is 0 in every one of the 462 months 1938-07..1976-12** (checked after the run:
   CMV's weights equal UMV's to 1e-9 in all 462 months; a diagnostic of the same run, not a new
   try). In 1977-2020 b is 0 in 44 of 528 months, in 2021-2025 in 2 of 58. So the out-of-paper
   CMV-vs-UMV comparison (K1, rule 3) rests on the 58 months from 2021 alone. Before 1977 the
   managed book *is* the unmanaged one, so "+0% in 1938-1976" says the method found nothing to
   time there, not that timing was tried and failed. The fail and K2 do not depend on this: they
   come from the alpha z against `tsmom12` and against the unmanaged book.
3. **Labels.** Out of sample starts in 1938-07, so the sample called "pre 1939-1976" in
   `results/vm-style-1.md` and in the `tries.md` rows (left as generated; rows are never edited)
   covers 1938-07..1976-12 (462 months). The write-up and `ideas.md` use the corrected label.

## Logged

`research/tries.md`: 16 rows, idea `vm-style-1`. Sharpe there is of monthly excess returns x
sqrt(12), stated in each Variant cell. No `ledger/tries.jsonl` line, because the gym cannot hold
shorts (as in `xs-century-1`).

Source: DeMiguel, V., A. Martin-Utrera and R. Uppal (2024), "A Multifactor Perspective on
Volatility-Managed Portfolios", Journal of Finance 79(6), 3859-3891, DOI 10.1111/jofi.13395
(open-access copy at LBS Research Online).
