# risk-menu-2: the menu's risk columns on 1994-2025 (descriptive, no pick)

Card: `cards/risk-menu-2.md` (committed before any number). W = 1994-02-01..2025-10-31; items 1-7 of risk-menu (no wide book); definitions, costs and T-bill cash as risk-menu. Sharpe on daily excess returns over the 13-week T-bill (365-day convention); every other measure on the total-return curve. Own-vol target: k solved on W, fixed target share until `tsmom12` has 52 weeks. Before QQQ (1999-03) the six is SPY alone; before TLT (2002-07) 60/40 is 60% SPY and 40% bills. Nothing after 2025-10-31 read.

## 1. Return and risk on W

| Item | Sharpe W (SE) | Growth/yr | Vol | Worst loss | Worst 12 months | Longest under water | 2000-02 | 2008 | 2020 Q1 | 2022 | Mean share | Avg exposure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hold the six (equal weight) | 0.77 (0.18) | 18.3% | 21.7% | 68.8% | -53.6% | 11.1 y | -62.5% | -11.7% | +0.4% | -36.5% | - | 1.00 |
| 60/40 (SPY / TLT) | 0.58 (0.18) | 8.7% | 11.1% | 30.2% | -25.4% | 4.3 y | -19.8% | -12.0% | -3.5% | -23.0% | - | 0.88 |
| `tsmom12`, full size | 0.94 (0.18) | 18.5% | 17.0% | 35.6% | -29.2% | 5.7 y | -21.7% | -0.2% | -6.8% | -11.2% | 1.00 | 0.76 |
| `tsmom12` 70% + T-bills | 0.94 (0.18) | 13.8% | 11.9% | 24.6% | -20.6% | 4.7 y | -12.5% | +0.3% | -4.4% | -7.3% | 0.70 | 0.53 |
| `tsmom12` 26% + T-bills | 0.94 (0.18) | 6.7% | 4.4% | 8.1% | -6.8% | 2.4 y | +2.2% | +1.0% | -1.3% | -1.5% | 0.26 | 0.20 |
| Own-vol target, mean share 26% | 1.03 (0.18) | 6.0% | 3.3% | 5.4% | -2.7% | 1.3 y | +6.3% | +1.0% | -0.5% | +0.8% | 0.26 | 0.18 |
| Own-vol target, mean share 70% | 1.08 (0.18) | 12.9% | 9.4% | 16.9% | -8.1% | 3.3 y | -1.4% | +0.0% | -2.6% | -1.9% | 0.70 | 0.53 |

## 2. When the worst came

| Item | Worst loss: high | Worst loss: low | Worst 12 months: ending |
|---|---|---|---|
| Hold the six (equal weight) | 2000-03-24 | 2002-10-09 | 2001-09-22 |
| 60/40 (SPY / TLT) | 2007-12-06 | 2009-03-09 | 2022-11-09 |
| `tsmom12`, full size | 2018-01-13 | 2020-03-12 | 2019-01-13 |
| `tsmom12` 70% + T-bills | 2018-01-13 | 2020-03-12 | 2019-01-13 |
| `tsmom12` 26% + T-bills | 2020-02-14 | 2020-03-12 | 2019-01-13 |
| Own-vol target, mean share 26% | 2020-02-14 | 2020-03-12 | 2016-01-15 |
| Own-vol target, mean share 70% | 2020-02-14 | 2020-03-12 | 2008-11-01 |

## 3. Do the risk rankings hold? (W against risk-menu's P = 2007-04..2025-10)

Rank 1 = best (smallest worst loss, mildest worst 12 months, shortest time under water). Holds = same first item and Kendall's tau >= 0.7 (card).

### Worst loss: tau 1.00, first on W vt-own 26%, first on P vt-own 26%: **holds**

| Item | P | rank P | W | rank W |
|---|---:|---:|---:|---:|
| Hold the six (equal weight) | 47.0% | 7 | 68.8% | 7 |
| 60/40 (SPY / TLT) | 30.2% | 5 | 30.2% | 5 |
| `tsmom12`, full size | 35.6% | 6 | 35.6% | 6 |
| `tsmom12` 70% + T-bills | 24.6% | 4 | 24.6% | 4 |
| `tsmom12` 26% + T-bills | 8.1% | 2 | 8.1% | 2 |
| Own-vol target, mean share 26% | 6.3% | 1 | 5.4% | 1 |
| Own-vol target, mean share 70% | 18.2% | 3 | 16.9% | 3 |

### Worst 12 months: tau 1.00, first on W vt-own 26%, first on P vt-own 26%: **holds**

| Item | P | rank P | W | rank W |
|---|---:|---:|---:|---:|
| Hold the six (equal weight) | -44.9% | 7 | -53.6% | 7 |
| 60/40 (SPY / TLT) | -25.4% | 5 | -25.4% | 5 |
| `tsmom12`, full size | -29.2% | 6 | -29.2% | 6 |
| `tsmom12` 70% + T-bills | -20.6% | 4 | -20.6% | 4 |
| `tsmom12` 26% + T-bills | -6.8% | 2 | -6.8% | 2 |
| Own-vol target, mean share 26% | -3.2% | 1 | -2.7% | 1 |
| Own-vol target, mean share 70% | -8.4% | 3 | -8.1% | 3 |

### Longest under water: tau 0.52, first on W vt-own 26%, first on P vt-own 26%: **does not hold**

| Item | P | rank P | W | rank W |
|---|---:|---:|---:|---:|
| Hold the six (equal weight) | 2.3 y | 4 | 11.1 y | 7 |
| 60/40 (SPY / TLT) | 2.8 y | 7 | 4.3 y | 4 |
| `tsmom12`, full size | 2.6 y | 6 | 5.7 y | 6 |
| `tsmom12` 70% + T-bills | 2.6 y | 5 | 4.7 y | 5 |
| `tsmom12` 26% + T-bills | 2.1 y | 2 | 2.4 y | 2 |
| Own-vol target, mean share 26% | 1.3 y | 1 | 1.3 y | 1 |
| Own-vol target, mean share 70% | 2.2 y | 3 | 3.3 y | 3 |
