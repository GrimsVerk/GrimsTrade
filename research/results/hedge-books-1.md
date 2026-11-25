# hedge-books-1: Hedge across the existing books

Card: `research/cards/hedge-books-1.md`. From `research/lib/hedgebooks1.py`. Daily returns 1994-02-01..2025-10-31, 365-day Sharpe, cash at 0, dividend-adjusted prices. Rounds: 1656 weeks ending Thursdays 1994-02-03..2025-10-30. Paired stationary bootstrap (block 20 days, 2000 draws, seed 0).

## protocol costs (judged)

| Book | Sharpe | vs `tsmom12` d (SE) z | vs EW d (SE) z | corr wk `tsmom12` | CAGR | Worst loss | Since 2003 | 2022-25 | Turnover/yr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `hedge16` | 1.128 | +0.076 (0.062) +1.23 | -0.030 (0.016) -1.87 | 0.94 | +18.3% | 33.5% | 1.30 | 0.85 | 2.96 |
| `ew16` | 1.158 | +0.106 (0.060) +1.78 | - | 0.95 | +17.1% | 33.0% | 1.36 | 0.90 | 3.19 |
| `hedge-pair` | 1.050 | -0.002 (0.003) -0.49 | +0.000 (0.001) +0.54 | 1.00 | +15.4% | 32.9% | 1.20 | 0.92 | 2.34 |
| `ew-pair` | 1.050 | -0.002 (0.003) -0.60 | - | 1.00 | +15.3% | 32.8% | 1.20 | 0.92 | 2.31 |
| `tsmom12` | 1.052 | - | - | 1.00 | +17.9% | 37.0% | 1.20 | 0.92 | 2.80 |

Verdict by the card (pass: z vs `tsmom12` >= 4.70 and Sharpe above its EW twin):

- `hedge16`: z vs `tsmom12` +1.23 (bar 4.7), not above its EW twin (z -1.87): **KILL**
- `hedge-pair`: z vs `tsmom12` -0.49 (bar 4.7), above its EW twin (z +0.54): **KILL**

Stand-alone books (the experts):

| Book | Sharpe | CAGR | Worst loss | log wealth | Hedge16 mean w | final w |
|---|---:|---:|---:|---:|---:|---:|
| `buy_hold_btc` | 0.874 | +37.3% | 84.9% | 10.08 | 0.072 | 0.111 |
| `buy_hold_spy` | 0.631 | +10.7% | 55.2% | 3.22 | 0.061 | 0.054 |
| `sixty_forty` | 0.768 | +8.2% | 30.5% | 2.51 | 0.059 | 0.050 |
| `equal_weight` | 1.013 | +22.2% | 66.7% | 6.36 | 0.066 | 0.070 |
| `ts_momentum` | 1.097 | +14.0% | 28.4% | 4.15 | 0.062 | 0.057 |
| `xs_momentum` | 0.944 | +31.4% | 77.5% | 8.67 | 0.071 | 0.091 |
| `vol_target_spy` | 0.745 | +7.4% | 33.4% | 2.27 | 0.058 | 0.048 |
| `risk_parity` | 0.832 | +12.1% | 62.0% | 3.63 | 0.061 | 0.055 |
| `crypto_mean_reversion` | 0.128 | +0.8% | 51.7% | 0.25 | 0.052 | 0.039 |
| `preset_careful` | 0.961 | +9.3% | 22.0% | 2.84 | 0.060 | 0.051 |
| `preset_middle` | 1.036 | +14.2% | 30.9% | 4.23 | 0.062 | 0.058 |
| `own_vol_70` | 1.053 | +12.7% | 27.7% | 3.78 | 0.060 | 0.054 |
| `tsmom12` | 1.052 | +17.9% | 37.0% | 5.23 | 0.064 | 0.063 |
| `halving-alone` | 1.285 | +22.9% | 29.5% | 6.55 | 0.066 | 0.073 |
| `where-vol` | 1.075 | +18.9% | 35.4% | 5.51 | 0.064 | 0.065 |
| `stop-0.25` | 1.091 | +15.6% | 28.9% | 4.61 | 0.063 | 0.060 |

Hedge16: eta 0.1157; largest weight ever 0.113 (`buy_hold_btc`); effective number of books mean 15.8, final 14.9 (of 16). Hedge-pair: eta 0.0579; final weights `tsmom12` 0.521, `own_vol_70` 0.479; range of `tsmom12`'s weight 0.500..0.521.

Regret (card section 'Regret actually achieved'):

| Allocator | Loss regret | Bound sqrt(T ln K / 2) | Loss spread of the books | Best book (loss) | Log-wealth regret, game | per year | Best book (log wealth) | Log-wealth regret, gym vs best book by wealth | vs best by Sharpe |
|---|---:|---:|---:|---|---:|---:|---|---:|---:|
| `hedge16` | 5.04 | 47.91 | 9.14 | `buy_hold_btc` | 4.77 | 0.150 | `buy_hold_btc` | 4.74 (`buy_hold_btc`) | 1.21 (`halving-alone`) |
| `hedge-pair` | 0.71 | 23.96 | 1.44 | `tsmom12` | 0.70 | 0.022 | `tsmom12` | 0.70 (`tsmom12`) | -0.75 (`own_vol_70`) |

## gym live costs (robustness)

| Book | Sharpe | vs `tsmom12` d (SE) z | vs EW d (SE) z | corr wk `tsmom12` | CAGR | Worst loss | Since 2003 | 2022-25 | Turnover/yr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `hedge16` | 1.124 | +0.076 (0.062) +1.23 | -0.029 (0.016) -1.80 | 0.94 | +18.3% | 33.5% | 1.30 | 0.85 | 2.94 |
| `ew16` | 1.154 | +0.105 (0.060) +1.76 | - | 0.95 | +17.1% | 33.0% | 1.35 | 0.90 | 3.19 |
| `hedge-pair` | 1.045 | -0.003 (0.003) -1.10 | +0.001 (0.001) +0.88 | 1.00 | +15.3% | 33.2% | 1.19 | 0.92 | 2.33 |
| `ew-pair` | 1.044 | -0.004 (0.003) -1.35 | - | 1.00 | +15.2% | 33.1% | 1.19 | 0.91 | 2.31 |
| `tsmom12` | 1.048 | - | - | 1.00 | +17.8% | 37.4% | 1.20 | 0.92 | 2.81 |

Verdict by the card (pass: z vs `tsmom12` >= 4.70 and Sharpe above its EW twin):

- `hedge16`: z vs `tsmom12` +1.23 (bar 4.7), not above its EW twin (z -1.80): **KILL**
- `hedge-pair`: z vs `tsmom12` -1.10 (bar 4.7), above its EW twin (z +0.88): **KILL**

Stand-alone books (the experts):

| Book | Sharpe | CAGR | Worst loss | log wealth | Hedge16 mean w | final w |
|---|---:|---:|---:|---:|---:|---:|
| `buy_hold_btc` | 0.874 | +37.3% | 84.9% | 10.07 | 0.072 | 0.112 |
| `buy_hold_spy` | 0.631 | +10.7% | 55.2% | 3.22 | 0.061 | 0.055 |
| `sixty_forty` | 0.768 | +8.2% | 30.5% | 2.51 | 0.059 | 0.050 |
| `equal_weight` | 1.013 | +22.1% | 66.7% | 6.36 | 0.066 | 0.071 |
| `ts_momentum` | 1.091 | +13.9% | 28.4% | 4.13 | 0.062 | 0.058 |
| `xs_momentum` | 0.946 | +31.4% | 77.4% | 8.68 | 0.071 | 0.091 |
| `vol_target_spy` | 0.745 | +7.4% | 33.4% | 2.27 | 0.058 | 0.048 |
| `risk_parity` | 0.825 | +12.0% | 62.0% | 3.60 | 0.061 | 0.055 |
| `crypto_mean_reversion` | 0.048 | -0.5% | 58.3% | -0.15 | 0.052 | 0.037 |
| `preset_careful` | 0.956 | +9.3% | 22.0% | 2.82 | 0.061 | 0.051 |
| `preset_middle` | 1.029 | +14.1% | 30.9% | 4.20 | 0.062 | 0.058 |
| `own_vol_70` | 1.045 | +12.5% | 28.1% | 3.75 | 0.060 | 0.054 |
| `tsmom12` | 1.048 | +17.8% | 37.4% | 5.21 | 0.064 | 0.063 |
| `halving-alone` | 1.282 | +22.9% | 29.5% | 6.54 | 0.066 | 0.073 |
| `where-vol` | 1.072 | +18.9% | 35.4% | 5.49 | 0.064 | 0.065 |
| `stop-0.25` | 1.086 | +15.5% | 28.9% | 4.59 | 0.063 | 0.060 |

Hedge16: eta 0.1157; largest weight ever 0.113 (`buy_hold_btc`); effective number of books mean 15.8, final 14.9 (of 16). Hedge-pair: eta 0.0579; final weights `tsmom12` 0.521, `own_vol_70` 0.479; range of `tsmom12`'s weight 0.500..0.521.

Regret (card section 'Regret actually achieved'):

| Allocator | Loss regret | Bound sqrt(T ln K / 2) | Loss spread of the books | Best book (loss) | Log-wealth regret, game | per year | Best book (log wealth) | Log-wealth regret, gym vs best book by wealth | vs best by Sharpe |
|---|---:|---:|---:|---|---:|---:|---|---:|---:|
| `hedge16` | 5.06 | 47.91 | 9.51 | `buy_hold_btc` | 4.80 | 0.151 | `buy_hold_btc` | 4.75 (`buy_hold_btc`) | 1.21 (`halving-alone`) |
| `hedge-pair` | 0.71 | 23.96 | 1.45 | `tsmom12` | 0.70 | 0.022 | `tsmom12` | 0.70 (`tsmom12`) | 0.70 (`tsmom12`) |

