# eu-8: cash interest, idea C, and which rule fits which investor

Lane `eu-8` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-8` from `eu-7`. Card `cards/eu-8.md` (each step pushed before its numbers). Code
`lib/eu8.py` (`fetch`, `check`, `cash`, ...); tables `results/eu-8-cash.md`. Held-out year unspent.

## 1. Step 1: does interest on idle cash change anything? (No.)

eu-6 and eu-7 kept idle cash at 0. Here the same runs are re-scored with cash earning a euro
money-market rate, from the ECB Data Portal (keyless): EONIA monthly averages before 2019-10,
the daily euro short-term rate (EUR STR) after, ACT/360, on the gym's actual end-of-day cash.
The `usw` 2008 proxy and the long monthly proxy get the US 13-week T-bill rate (IRX). How:
`lib/cash_interest.py` (on the base since 2026-11-12, US-only) re-scored target cash; `eu8.py`
re-implements the same idea for the euro rate and the gym's actual cash, so `origin/cash-interest`
(#61, a gym change) was not needed.

**Why so little moves:** over 2012-2025 the euro rate averaged only +0.5% a year (below zero
from 2015 to mid-2022, about 3-4% only in 2023-24). T holds 31% cash, B 33%, so they gain about
0.1-0.2% a year.

| (no fixed fee, `euw` 2012-2025) | T trend | B hold7 + 33% cash | H hold7 | M 60/40 |
|---|---:|---:|---:|---:|
| Sharpe above the rate (cash 0: Sharpe vs 0) | 0.57 (0.62) | 0.73 (0.79) | 0.72 (0.78) | 0.71 (0.75) |
| CAGR, rate as is (cash 0) | +3.8% (+3.7%) | +4.6% (+4.5%) | +6.3% (+6.3%) | +7.1% (+7.0%) |
| Worst loss | 14.0% (13.6%) | 13.8% | 19.8% | 22.3% |
| 2008 on the US proxy with T-bill interest | -0.3% (-0.7%) | -15.0% (-15.7%) | -23.0% | -30.4% |

All eight conclusions the card listed **hold** (`results/eu-8-cash.md` section 5): the Sharpe
order B ~ H > M > T (no gap real; B - T +0.17, p 0.10), B smallest worst loss, H shortest time
under water, T best in crashes (5 of 6 among T/B/H), trend's return cost (H - T CAGR +2.6 vs
+2.7 points), B's 2008-proxy worst loss twice T's (21.9% vs 10.9%). Flooring the euro rate at 0
(a cash account that never charges) changes no number by more than 0.04 Sharpe.

The one place interest matters is the **long US proxy 1972-2025**, where T-bills paid about 4% a year on
average: T's Sharpe above the T-bill rate is 0.78 vs 0.62 for both H and B (cash at 0: 1.26 vs
1.20), and T's CAGR rises from 8.1% to 9.5%, above H's 9.2%. So in a world of normal positive
rates trend's cash is not dead money and trend's long-run cost largely disappears; in the euro
2012-2025 window it was. That is a statement about the rate regime, not a new test: it widens
K8 ("trend at least as good as holding on the long proxy") rather than changing it.

Rows: 16 `robustness` (idea `eu-8`): T, B, H, M on `euw` with the rate as is and floored (8),
on `usw` 2007- with IRX (4), on the long monthly proxy with IRX (4). The tries.md Sharpe column
is against 0; the result file gives the excess Sharpe. The eu family stays at 12.
