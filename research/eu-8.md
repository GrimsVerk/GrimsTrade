# eu-8: cash interest, idea C, and which rule fits which investor

Lane `eu-8` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-8` from `eu-7`. Card `cards/eu-8.md` (each step pushed before its numbers). Code
`lib/eu8.py` (`fetch`, `check`, `cash`) and `lib/eu8c.py` (`check`, `run`); tables
`results/eu-8-cash.md` (step 1) and `results/eu-8-c.md` (step 2); 29 rows in `tries.md` (idea
`eu-8`). eu family now 13 (bar p < 0.0077). Held-out year unspent.

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

## 2. Step 2: idea C, trend on stocks and the long-bond fund only (fails, narrowly)

eu-7 found that trend's 2022 protection came from its bond slots. Idea C filters the three stock
funds and the long euro bond fund (IBGL) with `tsmom12` and holds short bonds, gold and
commodities at 1/7 always. Post-hoc, so carded before any number and **judged first on US
proxies 1994-2011** (the monthly stocks / 10y Treasuries / gold proxy, and the `usw` ETFs
2007-03 .. 2011-12 with no later bar loaded), then on EUR 2012-2025 with eu-7's test.

| | T trend | C stocks + long bonds | B hold7 + 33% cash | H hold7 |
|---|---:|---:|---:|---:|
| US monthly 1994-2011: Sharpe / max DD | 1.51 / 6.7% | 1.46 / 6.7% | 1.27 / 11.8% | 1.27 / 17.3% |
| US `usw` 2007-2011: Sharpe / max DD / orders a year | 0.64 / 10.0% / 16 | 0.77 / 10.8% / 11 | 0.53 / 22.1% / 6 | 0.54 / 32.0% / 6 |
| EUR 2012-2025: Sharpe (SE 0.27) | 0.62 | 0.63 | 0.79 | 0.78 |
| EUR: worst loss / longest under water | 13.6% / 58 mo | 15.9% / 57 mo | 13.8% / 31 mo | 19.8% / 31 mo |
| EUR: orders a year | 21.1 | 13.4 | 2.3 | 1.9 |
| Crash windows 2000-02 / 2008 (proxies) | +8.8 / -0.7% | +11.4 / -0.8% | -0.7 / -15.7% | -1.2 / -23.1% |
| 2015-16 / 2018-Q4 / 2020 / 2022 | -8.2 / -4.2 / -12.2 / +1.7% | -11.2 / -2.6 / -14.2 / +1.2% | -10.0 / -2.5 / -13.0 / -4.3% | -13.8 / -3.4 / -18.7 / -6.7% |

- **Stage 1 (US): keeps the insurance, but gains only 1 of 3** (37% fewer orders; Sharpe -0.05,
  under water 1 month shorter, both short of the bar). Fails.
- **Stage 2 (EUR): fails the insurance test by 0.2 points** (worst loss 15.9% vs T's 13.6%,
  2 points allowed), though it is within 3 points of T in 5 of 6 windows and keeps 2022 (+1.2% vs
  +1.7%); gains 1 of 3 (37% fewer orders; Sharpe +0.00, p 0.49; under water -1 month). Fails.
- So the held-out year stays unspent. C is the closest of the three partial-trend rules (A, B,
  C) to "T with fewer orders": same Sharpe, same crash record except commodity-heavy falls
  (2015-16, 2020, where holding commodities cost 2-3 points), at 13 instead of 21 orders a year.
  Under eu-7's mechanical tie rule (most windows best, then fewer orders) it even takes P4 from T
  (4 windows each). That is a tie-break, not a test pass; it is reported, not promoted.
- Cash interest (rate (a)) does not change this: C 0.57 excess Sharpe, T 0.57.

## 3. Which rule fits which investor (one screen; replaces eu-7 section 3)

Small coin-free euro book of the seven UCITS funds, 5/25 band, 2012-2025 plus US proxies for
2000-02 and 2008. All Sharpe gaps are about one standard error: no rule is *better*, they differ
in which pain they spare you. Cash interest at the euro money-market rate changes none of this.

| If you mainly want... | Use | What you get (EUR 2012-2025) | What it costs |
|---|---|---|---|
| the best long-run result, and can sit through a 20-30% fall | **H** hold the seven (or M 60/40) | Sharpe 0.78, +6.3% a year, back to the peak within 31 months, 2 orders a year | worst loss 20% (M 22%); -23% in a 2008-type crash (M -30%) |
| a smaller worst fall, without trading | **B** hold the seven, a third in cash | worst loss 14%, worst 12 months -8%, 31 months, 2 orders a year, H's Sharpe | +4.5% a year; not insurance: about -16% in a 2008-type crash |
| insurance against a sharp crash in any asset (stocks 2008, bonds 2022) | **T** trend on all seven | 2008 about 0%, 2022 +2%, best in 4-5 of 6 crash windows, worst loss 14% | +3.7% a year, 58 months below a peak, 21 orders a year; book EUR 5k+ at EUR 1 per order, 10k+ at EUR 2-3 |
| the same insurance with fewer orders, accepting a slightly deeper fall | **C** trend on stocks + long bonds (did not pass its card; a choice, not a finding) | T's Sharpe; as good as T or within 1 point in 4 of 6 crash windows (2022 +1%); 13 orders a year | worst loss 16%, 57 months below a peak; 2015-16 and 2020 2-3 points worse than T |
| the least effort | **H** | 2 orders a year, no weekly check | as H above |

- A book under EUR 10k paying EUR 2-3 per order: H or B only (trend's fees eat over 0.10 Sharpe).
- Rule A (trend on stocks only, eu-7) is not listed: C matches or beats it on everything but
  orders (13 vs 10 a year) and, unlike A, kept 2022.

## 4. Should the eu line stop here? Yes.

- The question "which rule for a small euro book, for which investor" is answered, and the answer
  survived two checks this lane (cash interest, a third partial-trend rule). The remaining choice
  is the investor's preference, not a research question.
- Every further Sharpe comparison would be a coin flip on the same 14 years (pair SEs 0.07-0.17,
  family bar now p < 0.0077, project-wide bar p <= 4.9e-5): more variants would only spend
  multiple-testing budget. Three attempts (A, B, C) to keep trend's insurance at a lower cost
  failed their cards.
- What could still add information is not another variant but more history or the future: a
  longer euro-proxy history (pre-2012, e.g. from index data) to sharpen the T vs H gap, or a
  forward paper-trade of the one rule the investor picks. Neither needs the held-out year now.
