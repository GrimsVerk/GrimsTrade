# month-end-bonds: hold the bond for the last four sessions of the month

Card: `cards/month-end-bonds.md` (written before any number). Train bars only; the held-out year was not loaded. One run each of `last4@LQD` and `last4@TLT-y1`. Twin `constant` holds LQD at a constant 19%; `hold` is buy-and-hold.

## LQD, 2002-07-31 to 2025-11-09 (gym: next-open fills, 2 bps a side)

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure | 2000-09 | 2010-16 | 2017-21 | 2022-25 | dSharpe vs constant@LQD (p; 90% range) | Eras ahead |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| last4@LQD | 0.52 (0.22) | +2.2% | 4.3% | 11.6% | 24.0 | 18% | 0.37 | 1.19 | 0.60 | 0.56 | -0.08 (p=0.58; -0.42..+0.36) | 2/4 |
| constant@LQD | 0.60 (0.21) | +0.9% | 1.6% | 5.2% | 0.0 | 19% | 0.66 | 1.02 | 0.69 | -0.01 | - | - |
| hold@LQD | 0.59 (0.21) | +4.7% | 8.4% | 25.0% | 0.0 | 100% | 0.64 | 1.02 | 0.67 | -0.02 | -0.01 (p=0.97; -0.02..-0.00) | 1/4 |

## LQD: the window, month by month

| Period | Months | Window, gross: bps (t) | Average session, bps | Net excess: bps (t) | Share of months up, gross |
|---|---:|---:|---:|---:|---:|
| all | 279 | +22.5 (+4.12) | +1.99 | +10.5 (+1.93) | 67% |
| to 2013 | 137 | +26.5 (+2.93) | +2.63 | +12.0 (+1.33) | 67% |
| from 2014 | 142 | +18.6 (+2.97) | +1.38 | +9.1 (+1.45) | 68% |
| first year (to 2003-07-30) | 11 | +53.2 (+1.72) | +5.06 | +28.9 (+0.94) | 64% |
| 2003-07-31 on | 268 | +21.2 (+3.83) | +1.85 | +9.8 (+1.77) | 68% |

Window = bought at the open of T-3, sold at the open of T+1 (T = last session of the month). Net excess = window return minus 4 bps of cost minus four average sessions of the same period. "First year" is a row of the same run, not a separate try.

Correlation of LQD's window return with TLT's in the same 279 months: +0.57 (no bar; how much of the LQD result is the same Treasury move).

## TLT, first year only (bars 2002-07-30 to 2003-07-30)

| Variant | Sharpe (SE) | CAGR | Vol | Max DD | Turnover/yr | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|
| last4@TLT-y1 | 0.22 (1.01) | +1.1% | 5.5% | 4.9% | 22.0 | 17% |

| Period | Months | Window, gross: bps (t) | Average session, bps | Net excess: bps (t) | Share of months up, gross |
|---|---:|---:|---:|---:|---:|
| first year | 11 | +14.8 (+0.30) | +3.14 | -1.8 (-0.04) | 64% |

## Pass bar: `last4@LQD`

- FAIL: 1. LQD: net excess over all months positive with t >= 2.0 (+10.5 bps, t +1.93, 279 months)
- PASS: 2. LQD: net excess positive in both halves (to 2013 +12.0 bps, from 2014 +9.1 bps)
- FAIL: 3. LQD: gym Sharpe above the twin with p < 0.10 (difference -0.076, p = 0.58)
- FAIL: 4. LQD: gym Sharpe above buy-and-hold (0.52 vs 0.59)

**FAILS train.**

## TLT's first year (can only fail to contradict)

- CONTRADICTED: net excess -1.8 bps a month (t -0.04, 11 months).
