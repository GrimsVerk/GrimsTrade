# registry-moments-1: results (`research/registrymoments1.py`)

Seed 20261125, 4000 records per cell, plan power 0.8, alpha 0.025.
Vectorised vs `forward.measure_lrv`: largest relative gap 5.6e-16.

## 1. Sizing: lowest expected power over the 10 weekly AR(1) cells, by level

| Level | Lowest expected power | Its cell | Highest (true lrv 1) |
|---|---:|---|---:|
| point estimate | 0.703 | weekly 5 y, phi 0.60 | 0.845 |
| 0.50 | 0.737 | weekly 5 y, phi 0.60 | 0.855 |
| 0.55 | 0.761 | weekly 5 y, phi 0.60 | 0.864 |
| 0.60 | 0.785 | weekly 5 y, phi 0.60 | 0.873 |
| 0.65 | 0.809 | weekly 5 y, phi 0.60 | 0.883 |
| 0.70 | 0.833 | weekly 5 y, phi 0.60 | 0.895 |
| 0.75 | 0.854 | weekly 10 y, phi 0.60 | 0.907 |
| 0.80 | 0.874 | weekly 10 y, phi 0.60 | 0.922 |
| 0.85 | 0.896 | weekly 10 y, phi 0.60 | 0.938 |
| 0.90 | 0.921 | weekly 10 y, phi 0.60 | 0.956 |

**Chosen level: 0.65** (`forward.LRV_LEVEL` = 0.65).

## 2. Sizing cells: point estimate vs the chosen level

| Cell | True lrv | Rule | Median used | Mean used | P(used < true) | Expected power | P(power < 0.75) | Mean used / true |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| weekly 5 y, phi 0.00 | 1.00 | point | 1.00 | 1.20 | 0.00 | 0.845 | 0.00 | 1.20 |
| weekly 5 y, phi 0.00 | 1.00 | 0.65 | 1.21 | 1.45 | 0.00 | 0.883 | 0.00 | 1.45 |
| weekly 5 y, phi 0.20 | 1.50 | point | 1.34 | 1.56 | 0.59 | 0.761 | 0.50 | 1.04 |
| weekly 5 y, phi 0.20 | 1.50 | 0.65 | 1.81 | 2.04 | 0.36 | 0.838 | 0.29 | 1.36 |
| weekly 5 y, phi 0.33 | 2.00 | point | 1.78 | 1.99 | 0.60 | 0.731 | 0.51 | 1.00 |
| weekly 5 y, phi 0.33 | 2.00 | 0.65 | 2.41 | 2.67 | 0.35 | 0.824 | 0.28 | 1.33 |
| weekly 5 y, phi 0.50 | 3.00 | point | 2.58 | 2.90 | 0.61 | 0.712 | 0.53 | 0.97 |
| weekly 5 y, phi 0.50 | 3.00 | 0.65 | 3.50 | 3.92 | 0.39 | 0.816 | 0.30 | 1.31 |
| weekly 5 y, phi 0.60 | 4.00 | point | 3.43 | 3.77 | 0.62 | 0.703 | 0.54 | 0.94 |
| weekly 5 y, phi 0.60 | 4.00 | 0.65 | 4.65 | 5.10 | 0.39 | 0.809 | 0.32 | 1.27 |
| weekly 10 y, phi 0.00 | 1.00 | point | 1.00 | 1.14 | 0.00 | 0.838 | 0.00 | 1.14 |
| weekly 10 y, phi 0.00 | 1.00 | 0.65 | 1.15 | 1.28 | 0.00 | 0.869 | 0.00 | 1.28 |
| weekly 10 y, phi 0.20 | 1.50 | point | 1.42 | 1.52 | 0.56 | 0.771 | 0.44 | 1.02 |
| weekly 10 y, phi 0.20 | 1.50 | 0.65 | 1.71 | 1.82 | 0.35 | 0.831 | 0.26 | 1.21 |
| weekly 10 y, phi 0.33 | 2.00 | point | 1.86 | 1.98 | 0.58 | 0.755 | 0.45 | 0.99 |
| weekly 10 y, phi 0.33 | 2.00 | 0.65 | 2.25 | 2.39 | 0.37 | 0.824 | 0.25 | 1.20 |
| weekly 10 y, phi 0.50 | 3.00 | point | 2.78 | 2.91 | 0.59 | 0.746 | 0.47 | 0.97 |
| weekly 10 y, phi 0.50 | 3.00 | 0.65 | 3.36 | 3.53 | 0.38 | 0.818 | 0.27 | 1.18 |
| weekly 10 y, phi 0.60 | 4.00 | point | 3.67 | 3.84 | 0.60 | 0.742 | 0.47 | 0.96 |
| weekly 10 y, phi 0.60 | 4.00 | 0.65 | 4.44 | 4.65 | 0.39 | 0.815 | 0.28 | 1.16 |

## 3. Other records (not used for sizing)

| Cell | True lrv | Rule | Median used | Mean used | P(used < true) | Expected power | P(power < 0.75) | Mean used / true |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| 8 a year, 5 y, phi 0.00 | 1.00 | point | 1.00 | 1.21 | 0.00 | 0.848 | 0.00 | 1.21 |
| 8 a year, 5 y, phi 0.00 | 1.00 | 0.65 | 1.28 | 1.48 | 0.00 | 0.890 | 0.00 | 1.48 |
| 8 a year, 5 y, phi 0.33 | 2.00 | point | 1.65 | 1.80 | 0.66 | 0.706 | 0.57 | 0.90 |
| 8 a year, 5 y, phi 0.33 | 2.00 | 0.65 | 2.23 | 2.41 | 0.40 | 0.809 | 0.32 | 1.20 |
| 8 a year, 5 y, phi 0.50 | 3.00 | point | 2.29 | 2.41 | 0.75 | 0.658 | 0.65 | 0.80 |
| 8 a year, 5 y, phi 0.50 | 3.00 | 0.65 | 3.09 | 3.25 | 0.47 | 0.774 | 0.38 | 1.08 |
| 8 a year, 10 y, phi 0.00 | 1.00 | point | 1.00 | 1.13 | 0.00 | 0.838 | 0.00 | 1.13 |
| 8 a year, 10 y, phi 0.00 | 1.00 | 0.65 | 1.17 | 1.28 | 0.00 | 0.870 | 0.00 | 1.28 |
| 8 a year, 10 y, phi 0.33 | 2.00 | point | 1.74 | 1.80 | 0.67 | 0.725 | 0.54 | 0.90 |
| 8 a year, 10 y, phi 0.33 | 2.00 | 0.65 | 2.11 | 2.18 | 0.44 | 0.800 | 0.31 | 1.09 |
| 8 a year, 10 y, phi 0.50 | 3.00 | point | 2.41 | 2.44 | 0.79 | 0.683 | 0.65 | 0.81 |
| 8 a year, 10 y, phi 0.50 | 3.00 | 0.65 | 2.91 | 2.96 | 0.54 | 0.765 | 0.40 | 0.99 |
| weekly 5 y, phi 0.50, t(4) shocks | 3.00 | point | 2.61 | 2.89 | 0.61 | 0.711 | 0.52 | 0.96 |
| weekly 5 y, phi 0.50, t(4) shocks | 3.00 | 0.65 | 3.53 | 3.90 | 0.37 | 0.814 | 0.30 | 1.30 |
| weekly 5 y, slow (phi 0.98 part) | 3.00 | point | 1.32 | 1.61 | 0.94 | 0.478 | 0.91 | 0.54 |
| weekly 5 y, slow (phi 0.98 part) | 3.00 | 0.65 | 1.78 | 2.09 | 0.83 | 0.575 | 0.76 | 0.70 |
| weekly 10 y, slow (phi 0.98 part) | 3.00 | point | 1.49 | 1.63 | 0.97 | 0.496 | 0.93 | 0.54 |
| weekly 10 y, slow (phi 0.98 part) | 3.00 | 0.65 | 1.81 | 1.95 | 0.90 | 0.568 | 0.84 | 0.65 |

## 4. Power approximation vs a Monte Carlo of the verdict's test

AR(1) phi 0.5 (true lrv 3) forward records with a true mean `effect`; the sample is
sized with lrv U (`forward.min_events_mean`); rejections of `forward`'s fixed-b HAC
test at alpha 0.025, 2,000 records per row.

| Sized with lrv | n | Approximate power | Monte Carlo power |
|---:|---:|---:|---:|
| 1.5 | 1271 | 0.496 | 0.512 |
| 3 | 2449 | 0.800 | 0.798 |
| 4.5 | 3627 | 0.931 | 0.942 |

## 5. Measured Mertens factor k on skewed, fat-tailed weekly records

Returns: N(0, 1) with probability 0.95, N(-2.5, 2^2) with 0.05 (a crash state),
iid; k = 1 - skew sr + (kurtosis - 1) / 4 sr^2 at the plan's per-week Sharpe sr.
Truth from 4,000,000 draws. The default plan (skew 0, kurtosis 3) is k0.

| Annual Sharpe | Years | True k | k0 | Median measured k | sd | P(measured < true) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.5 | 5 | 1.076 | 1.002 | 1.069 | 0.030 | 0.59 |
| 0.5 | 10 | 1.076 | 1.002 | 1.072 | 0.022 | 0.56 |
| 0.79 | 5 | 1.126 | 1.006 | 1.115 | 0.049 | 0.58 |
| 0.79 | 10 | 1.126 | 1.006 | 1.119 | 0.036 | 0.57 |
| 1.5 | 5 | 1.267 | 1.022 | 1.240 | 0.101 | 0.60 |
| 1.5 | 10 | 1.267 | 1.022 | 1.252 | 0.077 | 0.58 |

Population skew -1.00, kurtosis 6.54.
