# W43 `drought-food-margin`: results

Rule: [`cards/wide-26.md`](../cards/wide-26.md) (pushed before any number). Code:
`research/lib/wide26.py`, `research/lib/wide26_events.py`. Outcome: French 49-industry
value-weighted Food minus its 60-month beta times Mkt-RF, summed over months m+2..m+4,
percent; dose D = -PDSI of the Corn Belt (nClimDiv 361) in month m.

### W43 gate (dose months 1960-01 .. 2025-07)

- b +0.009% per PDSI unit, Newey-West t +0.07, 786 dose months.
- Shifted calendars: rank 22 of 41 (lowest = 1); null SD 1.10, 8% past |t| 2, 5/50/95% -1.68 / +0.03 / +1.52, extremes -2.28 / +2.02.
- Phase surrogates (seed 26): rank 23 of 41; null SD 1.25, 15% past |t| 2, 5/50/95% -2.13 / -0.07 / +2.06, extremes -2.97 / +2.65.
- Dose lag-1 autocorrelation (1895-2025): 0.940; 'both families' rule applies.
- **Verdict: FAIL.**

R43 not run (the card runs it only after a pass).

## Shown cells (not gating; beta-adjusted Food, NW 3, gate rows, unless named)

| Cell | b, % per unit | t | Rows |
|---|---:|---:|---:|
| **Gate** | **+0.009** | **+0.07** | **786** |
| Raw Food minus market (no beta) | -0.044 | -0.33 | 786 |
| W32's dose: contiguous-US PDSI (code 110) | +0.053 | +0.41 | 786 |
| Drying: PDSI(m-3) - PDSI(m), Corn Belt | -0.008 | -0.04 | 786 |
| 12-month horizon (m+2 .. m+13), NW 12 | +0.086 | +0.20 | 777 |
| Growing-season dose months only (Jun-Sep) | -0.121 | -0.49 | 261 |
| Restaurants (Meals), beta-adjusted | +0.006 | +0.04 | 786 |
| Farms (Agric), beta-adjusted, no sign predicted | +0.103 | +0.61 | 786 |
| Equal-weighted Food, beta-adjusted | -0.122 | -1.19 | 786 |
| The market itself (Mkt-RF, m+2 .. m+4) | +0.246 | +1.59 | 786 |
| After Hong-Li-Xu: dose months 2016-01 on | -0.327 | -2.02 | 114 |

## The ten driest dose months in the gate rows

| Dose month | D (-PDSI) | y, % |
|---|---:|---:|
| 1964-02 | +5.64 | -1.40 |
| 1964-03 | +5.32 | -0.51 |
| 1977-02 | +5.29 | +0.69 |
| 1977-05 | +5.09 | +3.67 |
| 1977-06 | +5.06 | -0.75 |
| 1964-01 | +5.03 | -2.75 |
| 1977-03 | +4.92 | +3.41 |
| 1977-04 | +4.87 | +3.02 |
| 1977-07 | +4.80 | -2.09 |
| 2012-11 | +4.61 | +14.60 |
