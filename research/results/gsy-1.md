# gsy-1: GSY run-up flag as an exit overlay on `tsmom12`

Card: `cards/gsy-runup.md`, step 3. Written by `lib/gsy.py runs`. Replication: `results/gsy-1-replication.md`.

## Step 3. The card's variants against `tsmom12`

Equal-slot books of the 30 (`G30`, primary) and 10 (`G10`, robustness) French industries, daily, value-weighted. `disc` = decisions 1928-07-02 to 2001-12-30; `check` = 2002-01-02 to 2025-11-09. Sharpe on calendar days, cash 0, 2 bps a side. `dSharpe` = variant minus `tsmom12` on the same days; p one-sided bootstrap (block 20 days; `p125` block 125). Crashes: falls of 40% or more from a running peak in an industry's daily index, crash day in the period; `out` = slot in cash on the crash day; `by overlay` = out while `tsmom12` held. `exit->X`: median calendar days from the exit to the crash day; `peak->exit`: median days from the peak to the exit (negative = out before the peak). Alarms: spells where the overlay held cash while `tsmom12` held; `false` = no 40% crash in that industry within 730 days of the spell's start (crashes from the full 1926-2025 data); `given up` = sum of the price moves over those spells, log points (positive = the overlay missed a rise).

Flag episodes in the period (independent bets), 100% / 150%: G30-disc 51 / 18; G30-check 17 / 12; G10-disc 6 / 2; G10-check 5 / 3.

Equal weight (holding) against `tsmom12`, Sharpe hold / `tsmom12`, worst loss hold / `tsmom12`: G30-disc 0.73 / 0.98, 82% / 39%; G30-check 0.62 / 0.73, 55% / 21%; G10-disc 0.72 / 0.99, 82% / 33%; G10-check 0.62 / 0.72, 52% / 24%.

### G30, disc

| Variant | Sharpe | dSharpe (p; p125) | d 1928-64 | d 1965-01 | Worst loss (tsmom12) | Growth/yr | Time in | Crashes out / n | by overlay | exit->X | peak->exit | Alarms: spells, false | given up |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 | 0.98 | - | - | - | 39% (39%) | 10.6% | 70% | 310 / 351 | - | 241 | 58 | - | - |
| flag100-cash | 1.02 | +0.04 (0.01; 0.02) | +0.05 | +0.04 | 33% (39%) | 10.3% | 66% | 322 / 351 | 12 | 313 | -24 | 171, 110 | +604 |
| flag150-cash | 1.00 | +0.02 (0.03; 0.04) | +0.03 | +0.00 | 36% (39%) | 10.5% | 69% | 318 / 351 | 8 | 277 | 47 | 62, 37 | +191 |
| flag100-sma | 1.01 | +0.03 (0.00; 0.00) | +0.04 | +0.01 | 37% (39%) | 10.7% | 69% | 318 / 351 | 8 | 237 | 57 | 188, 91 | -249 |
| flag150-sma | 0.99 | +0.01 (0.02; 0.03) | +0.02 | +0.00 | 38% (39%) | 10.7% | 70% | 315 / 351 | 5 | 237 | 58 | 62, 23 | -122 |
| flag100-vol | 1.01 | +0.03 (0.01; 0.01) | +0.03 | +0.03 | 36% (39%) | 10.5% | 68% | 318 / 351 | 8 | 250 | 53 | 193, 101 | +109 |
| flag150-vol | 0.99 | +0.01 (0.04; 0.04) | +0.01 | +0.01 | 38% (39%) | 10.6% | 70% | 315 / 351 | 5 | 248 | 56 | 68, 26 | +29 |

### G30, check

| Variant | Sharpe | dSharpe (p; p125) | d 2015-25 | Worst loss (tsmom12) | Growth/yr | Time in | Crashes out / n | by overlay | exit->X | peak->exit | Alarms: spells, false | given up |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 | 0.73 | - | - | 21% (21%) | 8.3% | 72% | 110 / 117 | - | 140 | 94 | - | - |
| flag100-cash | 0.73 | +0.00 (0.46; 0.47) | +0.00 | 20% (21%) | 7.6% | 66% | 115 / 117 | 5 | 178 | 43 | 90, 52 | +245 |
| flag150-cash | 0.73 | +0.00 (0.45; 0.47) | +0.01 | 20% (21%) | 7.9% | 68% | 112 / 117 | 2 | 174 | 58 | 70, 37 | +137 |
| flag100-sma | 0.75 | +0.02 (0.20; 0.23) | -0.01 | 20% (21%) | 8.2% | 71% | 114 / 117 | 4 | 137 | 92 | 113, 59 | -33 |
| flag150-sma | 0.75 | +0.02 (0.18; 0.22) | -0.00 | 20% (21%) | 8.3% | 71% | 112 / 117 | 2 | 139 | 94 | 78, 34 | -74 |
| flag100-vol | 0.75 | +0.02 (0.26; 0.25) | +0.02 | 20% (21%) | 8.1% | 70% | 115 / 117 | 5 | 174 | 70 | 83, 50 | -25 |
| flag150-vol | 0.73 | +0.00 (0.45; 0.45) | +0.02 | 20% (21%) | 8.1% | 71% | 112 / 117 | 2 | 157 | 92 | 49, 22 | +42 |

### G10, disc

| Variant | Sharpe | dSharpe (p; p125) | d 1928-64 | d 1965-01 | Worst loss (tsmom12) | Growth/yr | Time in | Crashes out / n | by overlay | exit->X | peak->exit | Alarms: spells, false | given up |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 | 0.99 | - | - | - | 33% (33%) | 10.6% | 73% | 74 / 78 | - | 297 | 66 | - | - |
| flag100-cash | 1.02 | +0.03 (0.13; 0.09) | +0.04 | +0.01 | 31% (33%) | 10.5% | 71% | 77 / 78 | 3 | 357 | 21 | 22, 7 | +40 |
| flag150-cash | 1.00 | +0.00 (0.26; 0.26) | -0.00 | +0.01 | 33% (33%) | 10.6% | 72% | 75 / 78 | 1 | 304 | 62 | 8, 5 | +20 |
| flag100-sma | 1.01 | +0.01 (0.16; 0.12) | +0.02 | +0.00 | 32% (33%) | 10.6% | 72% | 76 / 78 | 2 | 288 | 66 | 27, 5 | -3 |
| flag150-sma | 1.00 | +0.00 (0.23; 0.24) | +0.00 | +0.00 | 33% (33%) | 10.6% | 73% | 75 / 78 | 1 | 290 | 67 | 8, 3 | -6 |
| flag100-vol | 1.01 | +0.02 (0.28; 0.24) | +0.02 | +0.01 | 31% (33%) | 10.6% | 72% | 76 / 78 | 2 | 310 | 58 | 28, 8 | +26 |
| flag150-vol | 0.99 | +0.00 (0.43; 0.46) | -0.01 | +0.01 | 32% (33%) | 10.6% | 73% | 74 / 78 | 0 | 306 | 64 | 9, 4 | +5 |

### G10, check

| Variant | Sharpe | dSharpe (p; p125) | d 2015-25 | Worst loss (tsmom12) | Growth/yr | Time in | Crashes out / n | by overlay | exit->X | peak->exit | Alarms: spells, false | given up |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| tsmom12 | 0.72 | - | - | 24% (24%) | 7.8% | 74% | 24 / 26 | - | 109 | 142 | - | - |
| flag100-cash | 0.74 | +0.03 (0.24; 0.23) | +0.03 | 24% (24%) | 7.6% | 70% | 26 / 26 | 2 | 158 | 119 | 28, 16 | +11 |
| flag150-cash | 0.76 | +0.04 (0.10; 0.07) | +0.05 | 24% (24%) | 8.0% | 72% | 25 / 26 | 1 | 168 | 130 | 24, 13 | -63 |
| flag100-sma | 0.74 | +0.02 (0.11; 0.10) | +0.03 | 24% (24%) | 7.9% | 74% | 26 / 26 | 2 | 109 | 142 | 35, 21 | -30 |
| flag150-sma | 0.75 | +0.03 (0.04; 0.03) | +0.05 | 24% (24%) | 8.1% | 74% | 25 / 26 | 1 | 134 | 150 | 29, 16 | -62 |
| flag100-vol | 0.74 | +0.02 (0.18; 0.17) | +0.05 | 24% (24%) | 7.9% | 73% | 26 / 26 | 2 | 126 | 119 | 18, 10 | -34 |
| flag150-vol | 0.75 | +0.03 (0.06; 0.02) | +0.05 | 24% (24%) | 8.1% | 74% | 25 / 26 | 1 | 142 | 130 | 12, 8 | -69 |

### The card's pass bar, applied mechanically

Route S: `G30` discovery dSharpe > 0 with p < 0.0083, check dSharpe > 0, `G10` discovery dSharpe > 0. Route W: worst loss at least 5 points smaller than `tsmom12`'s and dSharpe >= -0.05 in discovery and check, and a larger share of crashes out than `tsmom12` in both.

| Variant | Route S | Route W | Verdict |
|---|---|---|---|
| flag100-cash | no | no | dead |
| flag150-cash | no | no | dead |
| flag100-sma | yes | no | passes |
| flag150-sma | no | no | dead |
| flag100-vol | yes | no | passes |
| flag150-vol | no | no | dead |
