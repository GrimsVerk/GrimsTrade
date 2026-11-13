# FM 1: Chronos zero-shot forecasts, tables (train period only)

Scripts `lib/fm1_forecast.py` (GPU) and `lib/fm1_eval.py` (numpy); card `research/fm-1.md`.
Raw numbers in `research/data/fm/eval-<model>.json` and `check-<model>.json` (git-ignored).
IC = Pearson correlation of the vol-scaled forecast with the target, pooled over assets.

## Models run

| Model | Revision (HF commit) | GPU s (week / day / hour) | Peak GPU | Peak RAM |
|---|---|---|---:|---:|
| `amazon/chronos-bolt-small` | `772f3d25d38aec6d914c8949dab4462e2d46f5d8` | 5.9 / 1.3 / 2.0 | 245 MB | 2.5 GB |
| `amazon/chronos-bolt-base` | `5d9f166d69f47aef3401367a7b842e78fe97b121` | 1.2 / 3.6 / 5.6 | 759 MB | 2.5 GB |
| `amazon/chronos-2` | `29ec3766d36d6f73f0696f85560a422f50e8498c` | 2.1 / 7.6 / 11.9 | 676 MB | 2.2 GB |

bf16 on the RTX 5080, context 512 bars, batch 256. Memorisation checks: a few seconds each.

## Weekly, six assets (`week_z`, Fridays 2000-01-07 .. 2025-11-07)

| Model | IC | after release (cells) | chance | WF IC | WF trend | gain over trend | gate Sharpe (tsmom12 0.988) | diff, p | diff 2020-25, p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| bolt-small | +0.105 | +0.105 (280) | 0.039 | +0.088 | +0.024 | +0.057 | 1.089 | +0.100, 0.02 | +0.039, 0.31 |
| bolt-base | +0.148 | +0.164 (280) | 0.043 | +0.135 | +0.024 | +0.110 | 1.172 | +0.184, 0.0005 | -0.097, 0.87 |
| chronos-2 | +0.020 | +0.303 (12) | 0.038 | -0.000 | +0.024 | -0.008 | 0.988 | -0.000, 0.51 | -0.008, 0.54 |

Gate eras (2000-09 / 2010-16 / 2017-21 / 2022-25), tsmom12 0.19 / 1.55 / 1.50 / 0.88:
bolt-small 0.33 / 1.82 / 1.54 / 0.89; bolt-base 0.53 / 1.92 / 1.52 / 0.83; chronos-2 0.14 / 1.63 /
1.49 / 0.89. Max drawdown 34% / 30% / 35% (tsmom12 36%).

## Memorisation checks (weekly IC by period; added after the first results, see write-up)

`inv` = the same six assets fed 1 / price, forecast sign flipped back. A model that reads
patterns should score about the same; a model that recognises the series should not.

| Book | Model | to 2009 | 2010-19 | 2020-25 | after release |
|---|---|---:|---:|---:|---:|
| six | bolt-small | +0.166 | +0.110 | +0.014 | +0.105 |
| six inv | bolt-small | +0.003 | -0.009 | -0.039 | +0.136 |
| six | bolt-base | +0.229 | +0.175 | -0.004 | +0.164 |
| six inv | bolt-base | +0.024 | +0.030 | -0.046 | +0.146 |
| six | chronos-2 | +0.026 | +0.039 | -0.014 | - |
| six inv | chronos-2 | -0.002 | +0.068 | -0.024 | - |
| 8 other ETFs | bolt-small / base / c2 | +0.201 / +0.277 / +0.044 | +0.133 / +0.187 / -0.008 | -0.025 / -0.012 / -0.036 | +0.160 / +0.183 / - |
| 4 indexes 1994+ | bolt-small / base / c2 | +0.190 / +0.285 / +0.009 | +0.206 / +0.324 / -0.057 | -0.031 / -0.012 / -0.022 | +0.156 / +0.098 / - |
| 9 sectors | bolt-small / base / c2 | +0.188 / +0.282 / +0.029 | +0.165 / +0.244 / -0.021 | -0.022 / +0.019 / +0.008 | +0.092 / +0.138 / - |
| 6 other coins | bolt-small / base / c2 | - | -0.130 / -0.047 / -0.022 | -0.035 / -0.041 / -0.044 | -0.081 / +0.009 / - |
| S&P 500 index 1964-1993 | bolt-small / base / c2 | +0.005 / +0.013 / +0.068 | - | - | - |

(The "six" row for bolt-small here is pooled over all six by period; per asset, bolt-small SPY
+0.224 / +0.195 / -0.037, QQQ +0.217 / +0.150 / -0.034, and fed 1 / price SPY +0.017 / -0.071 /
-0.057. Bolt-base SPY +0.290 / +0.301 / +0.054, inverted +0.060 / -0.029 / -0.085.)

## Daily, six assets (next close-to-close return / vol, 2000-2025)

| Model | IC | after release (cells) | partial given 4 trend inputs |
|---|---:|---:|---:|
| bolt-small | +0.034 | -0.032 (1,628) | +0.030 |
| bolt-base | +0.040 | -0.005 (1,628) | +0.037 |
| chronos-2 | -0.012 | -0.064 (102) | -0.018 |

## Hourly BTC/ETH (Binance, 2023-01-01 .. 2025-11-09)

IC of the forecast; `r_1h` = IC of the last hour's return (breadth-1's reversal) on the same rows;
partial = given `r_1h`, `r_24h`, `r_168h`. After release: Bolt ~8,250 hours, Chronos-2 ~500.

| Model | Series | IC | after release | r_1h IC | partial | partial after release |
|---|---|---:|---:|---:|---:|---:|
| bolt-small | BTC 1h | -0.005 | -0.025 | -0.023 | -0.006 | -0.021 |
| bolt-small | BTC 24h | +0.013 | +0.008 | -0.012 | +0.008 | -0.008 |
| bolt-small | ETH 1h | +0.011 | +0.028 | -0.007 | +0.011 | +0.030 |
| bolt-small | ETH 24h | +0.031 | +0.048 | -0.015 | +0.029 | +0.045 |
| bolt-base | BTC 1h | -0.016 | -0.038 | -0.023 | -0.014 | -0.025 |
| bolt-base | BTC 24h | +0.005 | -0.044 | -0.012 | -0.001 | -0.052 |
| bolt-base | ETH 1h | -0.007 | +0.013 | -0.007 | -0.006 | +0.017 |
| bolt-base | ETH 24h | +0.034 | +0.030 | -0.015 | +0.032 | +0.028 |
| chronos-2 | BTC 1h | -0.029 | +0.127 | -0.023 | -0.029 | +0.133 |
| chronos-2 | BTC 24h | +0.012 | -0.006 | -0.012 | +0.013 | +0.018 |
| chronos-2 | ETH 1h | -0.020 | +0.139 | -0.007 | -0.018 | +0.141 |
| chronos-2 | ETH 24h | -0.014 | +0.129 | -0.015 | -0.015 | +0.131 |

Standard errors: 1 h about 0.011 (Bolt, after release) and 0.045 (Chronos-2); 24 h overlaps, so
about 0.054 and 0.22.
