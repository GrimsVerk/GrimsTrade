# RMD December: event-study gate (wide-7, W12)

Rule: `research/wide-7.md` (pushed before this ran). Script `research/lib/wide7_rmd.py`.
Excess = log return over the last ten December sessions minus ten times the year's
mean daily log return on its other sessions. D = mean over the RMD waiver years (2009,
2020) minus mean over the other years, in %; p = exact one-sided permutation over all
pairs of years.

## Gate

| Test | D, % (p) | Needed |
|---|---:|---|
| SPY excess, Decembers 1993-2024 | -0.06 (0.505) | D > 0, p <= 0.05 |
| TLT excess, Decembers 2002-2024 | -0.18 | D > 0 |

**Gate: fail.**

## Shown

| Series | Years | Last ten, excess | Last ten, raw | First ten, excess (placebo) | 2009 excess (rank) | 2020 excess (rank) |
|---|---|---:|---:|---:|---:|---:|
| SPY | 1994-2024 | -0.06 (0.51) | +0.37 (0.41) | +1.07 (0.31) | -0.48 (20 of 31) | +0.79 (11 of 31) |
| TLT | 2003-2024 | -0.18 (0.59) | -0.49 (0.67) | -3.37 (0.89) | -0.67 (15 of 22) | -0.35 (12 of 22) |
| GSPC | 1975-2024 | -0.31 (0.57) | +0.08 (0.47) | +1.02 (0.33) | -0.32 (35 of 50) | +0.91 (19 of 50) |
