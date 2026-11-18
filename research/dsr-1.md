# dsr-1: how much survives a project-wide multiple-testing correction?

Lane `dsr-1` (night 2026-11-18), branch `dsr-1` from `main`. Reads every branch's tries, runs no
backtest. Script: `research/dsr1.py` (stdlib, reads git objects only).

## 1. Census of every try on every branch (snapshot 2026-11-18 22:17 UTC)

How: `git fetch origin`, then `python research/dsr1.py census`. Every remote branch's
`research/tries.md` is read with `git show`. Branches share rows through their ancestry; a row
is the same try on two branches when its line is identical. A line that appears k times on one
branch (a re-run logged twice, 9-12 such lines) counts k times; across branches the count is the
largest k seen on any one branch. Lanes keep pushing tonight, so a later run gives larger
numbers; the method stays the same.

Headline: **2,811 distinct tries in 124 families** (the `Idea` column), from 57,590 lines summed
over 62 branch files. 558 are `variant` rows (a configuration that could have been picked),
400 `baseline`, 1,122 `robustness`, 508 `control` (planted-signal tests, never selectable),
214 `screen`, 9 `note`. Sharpe values are annualised (365 days, zero rate).

The three numbers the deflated Sharpe needs:

| Set | Rows | With Sharpe | Mean | Variance | SD |
|---|---:|---:|---:|---:|---:|
| Selectable (`variant`, train), any data or universe | 544 | 516 | 0.78 | 0.103 | 0.32 |
| Primary test (six assets, 1994-02-01..2025-11-09), variant + baseline | 256 | 256 | 0.95 | 0.014 | 0.12 |
| Primary test, `variant` only | 244 | 244 | 0.96 | 0.014 | 0.12 |

The spread on one test (SD 0.12) is less than half the spread across tests (0.32): most of the
project-wide spread is different data (coins, Europe, 1926, futures), not different rules.

Gaps:

- 408 rows have no Sharpe: 205 screens (forecast-skill scores, no backtest), 154 robustness rows
  (mostly `exit-window`, `reentry`, `usd-1`, which log other measures), 29 variants, 9 notes.
- Sharpe is not always on the same footing: some lanes use monthly data (`invest-1`, `oos`
  period) or other windows (RL from 2000, macro from 2003, coins from 2017, futures 2-6 years).
  A cross-test variance mixes record lengths; the repo's DSR rule (DECISIONS 2026-11-12) accepts
  that as the cautious direction.
- No lane logs skew, kurtosis or the record length T beyond the From/To dates; the DSR below
  takes T from the dates and treats skew and kurtosis as a sensitivity.
- `ledger/research_tries.jsonl` on `paper-trail` (the daily runner's copy) stopped at
  2026-11-13 with 307 entries; every one of its 267 variant entries is in the union. It is
  not a project-wide register any more. `ledger/tries.jsonl` there holds the 11 live
  strategies (no backtest Sharpe); they are counted in N below, not in the Sharpe spread.
- The lane column is a heuristic (the smallest branch file holding the row, ties to the oldest
  tip); family counts do not depend on it.

Full tables (by kind, by lane, all 124 families with their Sharpe variance) as the script
printed them:

<details><summary>Census tables</summary>

Remote branches read: 73; with a `research/tries.md`: 62. Data lines summed over branches: 57590; distinct tries after removing shared history: **2811**.

### By kind

| Kind | Rows | With Sharpe | Mean | Variance | SD | Range |
|---|---:|---:|---:|---:|---:|---|
| robustness | 1122 | 968 | 0.60 | 0.185 | 0.43 | -5.04 .. 1.51 |
| variant | 558 | 529 | 0.77 | 0.115 | 0.34 | -1.97 .. 1.49 |
| control | 508 | 503 | 0.62 | 0.291 | 0.54 | -1.26 .. 2.70 |
| baseline | 400 | 394 | 0.64 | 0.113 | 0.34 | -0.65 .. 1.49 |
| screen | 214 | 9 | 0.28 | 0.149 | 0.39 | -0.20 .. 0.79 |
| note | 9 | 0 | | | | |
| **all** | 2811 | 2403 | 0.65 | 0.184 | 0.43 | -5.04 .. 2.70 |

### Sharpe spread on the tests the deflated Sharpe needs

Annualised Sharpe (365 days, zero rate). Per-day variance = annual variance / 365.

| Set | Rows | With Sharpe | Mean | Variance | SD | Range |
|---|---:|---:|---:|---:|---:|---|
| selectable: `variant`, train, any data | 544 | 516 | 0.78 | 0.103 | 0.32 | -1.97 .. 1.49 |
| primary test: six assets, 1994-02-01..2025-11-09, variant+baseline | 256 | 256 | 0.95 | 0.014 | 0.12 | 0.58 .. 1.28 |
| primary test, `variant` only | 244 | 244 | 0.96 | 0.014 | 0.12 | 0.58 .. 1.28 |

### By lane (the branch that logged the row; approximate)

| Lane | Rows | Variants | Families | With Sharpe |
|---|---:|---:|---:|---:|
| research-1 | 216 | 27 | 17 | 216 |
| research-2 | 52 | 31 | 7 | 52 |
| research-3 | 20 | 20 | 1 | 20 |
| macro-1 | 61 | 13 | 7 | 61 |
| rl-1 | 70 | 5 | 1 | 70 |
| rl-2 | 56 | 4 | 1 | 56 |
| ideas-1 | 100 | 20 | 9 | 91 |
| rl-3 | 183 | 0 | 1 | 183 |
| info-1 | 23 | 0 | 1 | 0 |
| breadth-1 | 127 | 61 | 4 | 96 |
| short-1 | 46 | 10 | 2 | 46 |
| invest-1 | 33 | 16 | 1 | 33 |
| fm-1 | 21 | 3 | 1 | 3 |
| carry-2 | 66 | 8 | 6 | 66 |
| rl-4 | 148 | 8 | 5 | 148 |
| wide-1 | 39 | 10 | 4 | 39 |
| deep-1 | 31 | 3 | 4 | 31 |
| slow-1 | 108 | 0 | 2 | 0 |
| carry-3 | 147 | 25 | 6 | 130 |
| trend-tune | 129 | 101 | 3 | 129 |
| usd-1 | 26 | 0 | 1 | 0 |
| trend-1926 | 192 | 0 | 1 | 192 |
| cointop-1 | 35 | 15 | 5 | 35 |
| volume-1 | 12 | 0 | 2 | 0 |
| evo-1 | 166 | 0 | 2 | 166 |
| trend-where | 9 | 2 | 1 | 9 |
| rl-5 | 9 | 0 | 1 | 9 |
| month-end-bonds | 4 | 2 | 1 | 4 |
| micro-1 | 6 | 0 | 1 | 0 |
| wide-2 | 15 | 3 | 3 | 15 |
| coin-cap | 19 | 9 | 1 | 19 |
| research/exit-1-bt | 194 | 30 | 2 | 68 |
| research/exit-1-reentry | 32 | 14 | 1 | 0 |
| data-long-2 | 18 | 0 | 1 | 18 |
| coin-cap-2 | 4 | 2 | 1 | 4 |
| wide-3 | 8 | 3 | 3 | 8 |
| gsy-1 | 36 | 12 | 1 | 36 |
| coin-cap-3 | 6 | 2 | 1 | 6 |
| wide-4 | 7 | 2 | 2 | 7 |
| evo-2 | 39 | 0 | 1 | 39 |
| eu-1 | 44 | 0 | 1 | 44 |
| eu-2 | 96 | 0 | 1 | 96 |
| survey-2 | 7 | 2 | 1 | 7 |
| eu-3 | 81 | 60 | 1 | 81 |
| survey-3 | 9 | 3 | 1 | 9 |
| eu-4 | 24 | 20 | 1 | 24 |
| coin-cap-4 | 6 | 3 | 1 | 6 |
| wide-5 | 6 | 2 | 2 | 6 |
| survey-4 | 17 | 5 | 2 | 17 |
| combo-1 | 8 | 2 | 1 | 8 |

### By family (the `Idea` column), largest first

| Family | Rows | Variants | With Sharpe | Sharpe variance |
|---|---:|---:|---:|---:|
| trend-1926 | 192 | 0 | 192 | 0.030 |
| rl-3-control | 183 | 0 | 183 | 0.007 |
| evo-1-control | 154 | 0 | 154 | 0.052 |
| exit-window | 126 | 14 | 0 |  |
| baselines | 114 | 0 | 114 | 0.036 |
| rl-4-control | 112 | 0 | 112 | 0.017 |
| slow-1-screen | 104 | 0 | 0 |  |
| trend-tune-surface | 101 | 98 | 101 | 0.005 |
| eu-2 | 96 | 0 | 96 | 0.173 |
| eu-3 | 81 | 60 | 81 | 0.012 |
| rl-1 | 70 | 5 | 70 | 0.014 |
| exit-rules | 68 | 16 | 68 | 0.014 |
| rl-2 | 56 | 4 | 56 | 0.033 |
| breadth-1-hf | 52 | 8 | 24 | 0.051 |
| eu-1 | 44 | 0 | 44 | 0.139 |
| evo-2-control | 39 | 0 | 39 | 0.193 |
| short-1-P30 | 39 | 9 | 39 | 1.281 |
| carry-3-B-out | 36 | 6 | 32 | 0.176 |
| carry-3-Bybit | 36 | 6 | 32 | 0.097 |
| carry-3-Hyperliquid | 36 | 6 | 32 | 0.435 |
| gsy-runup | 36 | 12 | 36 | 0.031 |
| carry-3-pooled | 33 | 6 | 33 | 0.301 |
| invest-1 | 33 | 16 | 33 | 0.024 |
| reentry | 32 | 14 | 0 |  |
| breadth-1-binance | 31 | 21 | 29 | 0.073 |
| breadth-1-cm | 28 | 20 | 27 | 0.095 |
| trend-where | 27 | 2 | 27 | 0.043 |
| usd-1 | 26 | 0 | 0 |  |
| eu-4 | 24 | 20 | 24 | 0.062 |
| month-end-liquidity | 24 | 3 | 24 | 0.020 |
| info-1-screen | 23 | 0 | 0 |  |
| vol-echo | 22 | 4 | 22 | 0.059 |
| fm-1 | 21 | 3 | 3 | 0.008 |
| risk-map | 20 | 20 | 20 | 0.013 |
| trend-tune | 20 | 3 | 20 | 0.066 |
| coin-cap | 19 | 9 | 19 | 0.009 |
| deep-1 | 18 | 0 | 18 | 0.009 |
| dip-rsi2 | 18 | 2 | 18 | 0.017 |
| breadth-1-trad | 16 | 12 | 16 | 0.009 |
| cointop-1-cm | 16 | 12 | 16 | 0.038 |
| ath | 14 | 2 | 13 | 0.086 |
| carry-2-B-out | 13 | 2 | 13 | 0.041 |
| carry-2-Bybit | 13 | 2 | 13 | 0.053 |
| carry-2-Hyperliquid | 13 | 2 | 13 | 0.081 |
| absorption-ratio | 12 | 2 | 12 | 0.096 |
| crypto-alone | 12 | 0 | 12 | 0.074 |
| evo-1-smoke | 12 | 0 | 12 | 1.185 |
| ml-gbm | 12 | 9 | 12 | 0.027 |
| ts-carry | 11 | 3 | 11 | 0.135 |
| robustness | 10 | 0 | 10 | 0.007 |
| y10 | 10 | 4 | 9 | 0.076 |
| bbwp | 9 | 2 | 8 | 0.065 |
| carry-2-B-P30 | 9 | 0 | 9 | 0.102 |
| carry-2-B-all | 9 | 0 | 9 | 0.101 |
| carry-2-pooled | 9 | 2 | 9 | 0.066 |
| fracdiff-momentum | 9 | 3 | 9 | 0.042 |
| liquidity | 9 | 3 | 9 | 0.075 |
| ml-sizing | 9 | 6 | 9 | 0.039 |
| rl-4-perp-B-out | 9 | 2 | 9 | 0.176 |
| rl-4-perp-Bybit | 9 | 2 | 9 | 0.053 |
| rl-4-perp-Hyperliquid | 9 | 2 | 9 | 0.048 |
| rl-4-perp-pooled | 9 | 2 | 9 | 0.090 |
| rl-5-screen | 9 | 0 | 9 | 0.149 |
| srsi | 9 | 2 | 8 | 0.043 |
| trend3 | 9 | 2 | 8 | 0.095 |
| xtsmom | 9 | 3 | 9 | 0.044 |
| combo-1 | 8 | 2 | 8 | 0.048 |
| contagion-catchup | 8 | 2 | 8 | 0.027 |
| credit-spread | 8 | 2 | 8 | 0.051 |
| drawdown-control | 8 | 2 | 8 | 0.078 |
| fed-hiking | 8 | 2 | 8 | 0.071 |
| fng | 8 | 4 | 6 | 0.064 |
| gap | 8 | 2 | 7 | 0.076 |
| hmm-regime | 8 | 2 | 8 | 0.056 |
| oil | 8 | 2 | 7 | 0.106 |
| real-rate | 8 | 2 | 8 | 0.036 |
| trend-tune-anatomy | 8 | 0 | 8 | 0.027 |
| yield-curve | 8 | 2 | 8 | 0.088 |
| ensemble-tsmom | 7 | 1 | 7 | 0.064 |
| fomc-cycle | 7 | 2 | 7 | 0.050 |
| hawkes-clustering | 7 | 1 | 7 | 0.052 |
| ml-payoff | 7 | 4 | 7 | 0.039 |
| short-1-BTC-ETH | 7 | 1 | 7 | 0.023 |
| trend-age | 7 | 1 | 7 | 0.054 |
| trend-vol | 7 | 1 | 7 | 0.049 |
| auction-concession | 6 | 2 | 6 | 0.079 |
| coin-cap-3 | 6 | 2 | 6 | 0.008 |
| coin-cap-4 | 6 | 3 | 6 | 0.041 |
| cointop-1-breadth | 6 | 1 | 6 | 0.062 |
| cointop-1-fade | 6 | 1 | 6 | 0.063 |
| cointop-1-stop | 6 | 1 | 6 | 0.064 |
| halloween | 6 | 2 | 6 | 0.012 |
| kelly-shrunk | 6 | 3 | 6 | 0.047 |
| micro-1-screen | 6 | 0 | 0 |  |
| ml-filter | 6 | 3 | 6 | 0.086 |
| ml-linear | 6 | 3 | 6 | 0.142 |
| ml-pooled | 6 | 3 | 6 | 0.026 |
| ml-weekly | 6 | 3 | 6 | 0.073 |
| volume-1-coins-screen | 6 | 0 | 0 |  |
| volume-1-screen | 6 | 0 | 0 |  |
| carry-3-B-all | 5 | 0 | 1 |  |
| deep-1-meta | 5 | 1 | 5 | 0.059 |
| halving | 5 | 2 | 5 | 0.026 |
| vol-target | 5 | 2 | 5 | 0.031 |
| coin-cap-2 | 4 | 2 | 4 | 0.009 |
| crowded-trend | 4 | 1 | 4 | 0.048 |
| deep-1-stack | 4 | 1 | 4 | 0.065 |
| deep-1-switch | 4 | 1 | 4 | 0.051 |
| month-end-bonds | 4 | 2 | 4 | 0.032 |
| opex-pin | 4 | 1 | 4 | 0.079 |
| patch-leaving | 4 | 1 | 4 | 0.090 |
| slow-1-control | 4 | 0 | 0 |  |
| tax-drain | 4 | 1 | 4 | 0.051 |
| universal-portfolio | 4 | 1 | 4 | 0.024 |
| coupon-dose | 3 | 1 | 3 | 0.074 |
| crypto-slot-size | 3 | 3 | 3 | 0.035 |
| dealer-backlog | 3 | 1 | 3 | 0.063 |
| extension-dose | 3 | 1 | 3 | 0.063 |
| rebalance-pressure | 3 | 2 | 3 | 0.055 |
| attention-peak | 2 | 1 | 2 | 0.238 |
| hedge-regime | 2 | 1 | 2 | 0.106 |
| trend-to-safe | 2 | 1 | 2 | 0.058 |
| carry-3 | 1 | 1 | 0 |  |
| cointop-1 | 1 | 0 | 1 |  |

### Gaps

- Rows without a Sharpe: 408 (screen 205, robustness 154, variant 29, note 9, baseline 6, control 5).
- Families: 124. Periods: train 2754, heldout 23, oos 22, - 12.
- `ledger/research_tries.jsonl` on `paper-trail` (the daily runner's copy, last filled 2026-11-13): 307 entries; 267 name a variant and 0 of those are missing from the union (case ignored); 40 name only an idea (ideas-list entries, several never backtested). It stopped growing after research run 2: it is not a project-wide register.
- `ledger/tries.jsonl` on `paper-trail`: 11 live strategies (M0/M1 yardsticks and rules, no backtest Sharpe recorded there). Counted separately below, not in the rows.

</details>
