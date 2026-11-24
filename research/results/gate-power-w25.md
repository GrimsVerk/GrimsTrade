# Gate power: W25 act-haven (lane gate-power)

Card: `research/gate-power.md` (pushed before this ran). Script `research/lib/gatepower_run.py`
(GATE=W25). 200 simulations per effect size; noise = the gate's real returns rotated against the dose calendar; planted effect f x sigma per unit-SD position (sigma per week: GLD 2.46%, TLT 1.89%).
Rebuild check: rebuilt t -1.02, stored -1.02, |fast-ols_dk| 0e+00. Rows 2168. Dose N_eff 27; episodes: n/a (continuous index).

## Detection rate by planted effect

IR = f x sqrt(52) x 1.30: the standalone information ratio of the timing rule trading all 2 gate asset(s) with equal risk (mean pairwise return correlation +0.18; x sqrt(n / (1 + (n - 1) rho))). Added = Sharpe gained over `tsmom12` (1.05) if that rule is mixed in uncorrelated, in the best mix.

| f | %/week per SD | IR | Added | t >= 2 only | Old rule | Corrected rule |
|---:|---:|---:|---:|---:|---:|---:|
| 0.00 | 0.000 | 0.00 | +0.000 | 6% | 4% | 5% |
| 0.02 | 0.043 | 0.19 | +0.017 | 20% | 10% | 15% |
| 0.04 | 0.087 | 0.38 | +0.065 | 56% | 26% | 38% |
| 0.06 | 0.130 | 0.56 | +0.142 | 80% | 57% | 64% |
| 0.08 | 0.174 | 0.75 | +0.242 | 96% | 82% | 90% |
| 0.10 | 0.217 | 0.94 | +0.360 | 100% | 94% | 96% |
| 0.15 | 0.326 | 1.41 | +0.709 | 100% | 100% | 100% |
| 0.20 | 0.434 | 1.88 | +1.105 | 100% | 100% | 100% |
| 0.30 | 0.651 | 2.82 | +1.961 | 100% | 100% | 100% |
| 0.40 | 0.869 | 3.76 | +2.856 | 100% | 100% | 100% |
| 0.60 | 1.303 | 5.64 | +4.691 | 100% | 100% | 100% |
| 0.80 | 1.737 | 7.53 | +6.548 | 100% | 100% | 100% |

## Minimum detectable effect, 80% power

| Rule | f | %/week per SD | IR | Added Sharpe |
|---|---:|---:|---:|---:|
| t >= 2 only (N(0,1) null) | 0.061 | 0.132 | 0.57 | +0.145 |
| Old rule (placebos as run) | 0.078 | 0.170 | 0.74 | +0.233 |
| Corrected rule (earlier doses k = +27..+183) | 0.072 | 0.157 | 0.68 | +0.201 |

## Null at f = 0 (all draws pooled)

True-dose t over 200 draws: SD 1.20, share |t| >= 2 10%.
Old placebos: SD 1.12, median +0.09, share |t| >= 2 9%.
Corrected placebos: SD 1.15, median +0.04, share |t| >= 2 10%.
False-pass rate (f = 0): old 4.5%, corrected 5.0%, t >= 2 only 6.5%.
