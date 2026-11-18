# Critical slowing down: event-study gate (wide-6, W11)

Rule: `research/wide-6.md` (pushed before this ran). Script `research/lib/wide6_csd.py`.
Linear probability of a large forward drawdown (asset's top decile of the maximum
drawdown over the next quarter), pooled over SPY, QQQ, TLT, GLD, BTC, ETH with asset
intercepts; Driscoll-Kraay t (13 weekly lags). Slopes are per unit of Kendall tau
(range -1 to +1) and per unit of log volatility; base rate 0.10.

## Gate (with the two volatility controls)

| Period | obs | Fridays | tauAC1 slope (t) | tauVAR slope (t) | log sd21 (t) | log sdw (t) |
|---|---:|---:|---:|---:|---:|---:|
| in-sample (Fridays to 2015-12) | 3038 | 1091 | +0.039 (+1.44) | -0.019 (-0.53) | +0.195 (+3.81) | +0.078 (+1.10) |
| post-sample (2016-01 on) | 2887 | 502 | +0.003 (+0.12) | +0.040 (+1.82) | +0.038 (+0.97) | -0.003 (-0.05) |
| all | 5925 | 1593 | +0.019 (+0.96) | -0.005 (-0.24) | +0.107 (+3.06) | +0.101 (+2.09) |

Gate (slope > 0 and t >= 2.24 in both periods): tauAC1 **fail**, tauVAR **fail**.

## Shown: without the volatility controls (raw effect)

| Period | obs | Fridays | tauAC1 slope (t) | tauVAR slope (t) | log sd21 (t) | log sdw (t) |
|---|---:|---:|---:|---:|---:|---:|
| in-sample (Fridays to 2015-12) | 3038 | 1091 | +0.032 (+1.02) | +0.044 (+1.17) | - | - |
| post-sample (2016-01 on) | 2887 | 502 | +0.006 (+0.20) | +0.047 (+2.10) | - | - |
| all | 5925 | 1593 | +0.020 (+0.93) | +0.043 (+1.89) | - | - |

## Shown: continuous target (forward maximum drawdown, percent)

| Period | obs | Fridays | tauAC1 slope (t) | tauVAR slope (t) | log sd21 (t) | log sdw (t) |
|---|---:|---:|---:|---:|---:|---:|
| in-sample (Fridays to 2015-12) | 3038 | 1091 | +0.141 (+0.17) | +0.371 (+0.37) | +4.504 (+3.55) | +3.655 (+1.72) |
| post-sample (2016-01 on) | 2887 | 502 | +2.297 (+1.84) | +1.094 (+0.75) | +2.928 (+1.51) | +5.106 (+1.19) |
| all | 5925 | 1593 | +1.022 (+1.35) | +0.432 (+0.52) | +3.517 (+2.78) | +5.327 (+2.59) |

## Shown: per asset, each tau alone with the controls (Newey-West t)

| Asset | Period | obs | tauAC1 slope (t) | tauVAR slope (t) |
|---|---|---:|---:|---:|
| SPY | in-sample (Fridays to 2015-12) | 1091 | -0.039 (-1.06) | -0.015 (-0.35) |
| SPY | post-sample (2016-01 on) | 502 | +0.011 (+0.15) | +0.076 (+1.13) |
| QQQ | in-sample (Fridays to 2015-12) | 773 | +0.138 (+1.88) | +0.018 (+0.33) |
| QQQ | post-sample (2016-01 on) | 502 | +0.078 (+1.16) | -0.027 (-0.49) |
| TLT | in-sample (Fridays to 2015-12) | 595 | +0.065 (+1.66) | -0.013 (-0.28) |
| TLT | post-sample (2016-01 on) | 502 | -0.129 (-1.83) | +0.151 (+2.09) |
| GLD | in-sample (Fridays to 2015-12) | 475 | +0.153 (+1.73) | +0.029 (+0.36) |
| GLD | post-sample (2016-01 on) | 502 | +0.011 (+0.70) | +0.002 (+0.12) |
| BTC | in-sample (Fridays to 2015-12) | 104 | +0.049 (+0.29) | -0.606 (-1.92) |
| BTC | post-sample (2016-01 on) | 502 | +0.050 (+1.00) | +0.092 (+1.77) |
| ETH | in-sample (Fridays to 2015-12) | 0 | - | - |
| ETH | post-sample (2016-01 on) | 377 | -0.039 (-0.65) | -0.042 (-0.81) |

## Shown: S&P 500 index (GSPC) alone, Fridays 1962-2015 (the papers' years)

| Spec | obs | tauAC1 slope (t) | tauVAR slope (t) |
|---|---:|---:|---:|
| with vol controls | 2817 | -0.025 (-0.80) | +0.040 (+1.37) |
| without vol controls | 2817 | -0.028 (-0.91) | +0.068 (+2.59) |

## Shown: AC1 and variance of log price minus its trailing 25-bar mean (Guttal-style, causal)

| Period | obs | Fridays | tauAC1 slope (t) | tauVAR slope (t) | log sd21 (t) | log sdw (t) |
|---|---:|---:|---:|---:|---:|---:|
| in-sample (Fridays to 2015-12) | 3013 | 1086 | +0.044 (+1.09) | -0.000 (-0.01) | +0.189 (+3.60) | +0.059 (+0.85) |
| post-sample (2016-01 on) | 2884 | 502 | +0.008 (+0.24) | +0.028 (+1.07) | +0.043 (+1.12) | +0.016 (+0.27) |
| all | 5897 | 1588 | +0.029 (+1.09) | +0.001 (+0.03) | +0.107 (+3.03) | +0.091 (+2.01) |
