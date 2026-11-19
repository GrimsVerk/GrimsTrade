# dsr-1: how much survives a project-wide multiple-testing correction?

Lane `dsr-1` (night 2026-11-18), branch `dsr-1` from `main`. Reads every branch's tries, runs no
backtest. Script: `research/dsr1.py` (stdlib, reads git objects only).

## Verdict in plain words (one screen)

**Is `tsmom12`'s edge credible after everything the project tried? Its profit is; its edge is
not.**

- The trend rule makes money: Sharpe 1.05 over 32 years is far beyond luck, however many of the
  project's 2,811 tries are counted. But holding all six assets passes the same test. That part
  is the market's return, not the rule's skill.
- The edge over simply holding (+0.17 Sharpe, p 0.08) was not proven even before the search
  began: it fails at N = 1 and comes from 2000-2002 alone (review-1). Corrected for the eight
  baselines it was ranked against, the luck-adjusted edge is -0.01; for the 89 trials before
  it went live, -0.13; for today's 947 selectable tries, -0.22. Since 2003 it is zero.
- So `tsmom12` stays what review-1 called it: insurance (a 37% worst loss instead of 47-69%,
  for about 4 points of growth a year). Keep it live as the bar and as a risk choice; do not
  read its scoreboard rank as skill.

**Which near-misses are worth a held-out year? None, by the rule fixed before the numbers.**
The five best across the project (`gsy-runup`, `halving-and`, quiet coins, funding carry,
coin `stop-0.25`) all fall below 0.95 even at their own family's size, and to 0.07-0.44 at the
project's size. Two had their year spent already (quiet coins passed it, carry failed it). The
closest unspent ones are `gsy-runup` (+0.03 Sharpe, gone after 2002) and `halving-and` (three
crypto winters, a folklore window). One year is about a third of a Sharpe standard error: it
cannot lift any of them over the bar, so spending it would only use up clean data. If the
owner wants the coin stop as a risk preference (coin-cap's advice), that is a choice of risk,
not a finding, and needs no held-out year.

**What a new idea now has to clear.** On the primary test, against `tsmom12`, with today's
947 selectable tries counted as 96 independent ones (rho 0.9): z >= 4.2, about **+0.27 Sharpe**
for a rule close to `tsmom12` (SE 0.065) and +0.50 for a far one (SE 0.12). With all 947 as
independent: +0.32 / +0.59. Nothing the project has seen comes near; the largest edges over
`tsmom12` on the primary test were +0.18 (`fomc-cycle`, reversed after publication) and +0.15
(`halving-and`).

**Found on the way: the live scoreboard undercounts N.** `grimstrade.ledger` reads tries from
`main` and `research-*` branches only (`_RESEARCH_REFS`). Lanes since 2026-11-13 are named
otherwise (`carry-2`, `wide-1`, `eu-4`, ...), so `ledger/research_tries.jsonl` on `paper-trail`
stopped at 307 entries; the project has 2,811 rows, 947 of them selectable. The scoreboard's
deflated Sharpe is too kind by that much. Undercounting is the direction DECISIONS calls
dishonest.

### Proposal: one project-wide tries register

- **Where:** `research/register/` on `main`. `tries.jsonl`: one line per try, the union of
  every branch, keyed by a hash of the tries.md line plus its occurrence number (the dedupe
  this lane used), with branch, family, kind, period, test (from, to, universe), Sharpe and,
  new, the record length T, skew, kurtosis, the comparator and the one-sided p against it.
  `BAR.md`: generated, the global N (raw and at rho 0.9), the Sharpe spread per test, and the
  edge a new idea must clear on each test (the table above).
- **How it grows without lanes merging each other:** lanes keep appending to their own
  `research/tries.md` as now. Each card quotes the global N from
  `python research/dsr1.py census` run over all remote branches at card time (seconds, no
  data). The night lead regenerates `research/register/` in one PR per night;
  `.gitattributes` marks `tries.jsonl` `merge=union`, so the PRs never conflict.
- **Tamper evidence:** widen `_RESEARCH_REFS` in `grimstrade/ledger.py` to every remote branch
  (`refs/remotes/*/*`, minus `paper-trail`), so the daily runner again appends every try it
  sees to `ledger/research_tries.jsonl` on `paper-trail` and the live scoreboard's N is the
  project's N. A deleted branch then cannot hide a try, as DECISIONS 2026-11-12 intended.
- **Bars become global:** a card's family bar stays (it is the lane's own question), and every
  result also reports its DSR at the global N. "Passed its family bar" without the global
  number is not a lead.

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

## 2. Card: deflated Sharpe and Bonferroni/Holm (fixed 2026-11-18 ~22:40 UTC, before any number below is computed)

No new strategy test: every input is a number already logged in a tries row or written in a
lane's write-up. Nothing touches the held-out year.

### Formula, checked against the paper

Bailey and López de Prado (2014), "The Deflated Sharpe Ratio", JPM 40(5), eq. (1)-(2), read
from the authors' PDF tonight:

- Expected best of N independent trials whose Sharpes have mean `E` and variance `V`:
  `E + sqrt(V) * ((1 - g) * Z^-1(1 - 1/N) + g * Z^-1(1 - 1/(N e)))`, `g` = 0.5772 (Euler).
- `DSR = Z( (SR - SR0) * sqrt(T - 1) / sqrt(1 - skew * SR + (kurt - 1) / 4 * SR^2) )`, with
  `SR0` the expression above with `E = 0` (the null: no trial has skill), per-period Sharpes,
  raw kurtosis (3 for a normal).
- Dependent trials (appendix A.3, eq. 9): M correlated trials count as `N = rho + (1 - rho) M`
  independent ones, `rho` the average correlation.

The repo already implements eq. (2) in `src/grimstrade/stats.py`. Check run before the card:
it reproduces the paper's worked example exactly (N = 100, V = 1/2, T = 1,250, skew -3,
kurtosis 10, SR 2.5 a year: DSR 0.9004; 0.9505 at N = 46; with normal returns it passes 0.95
up to N = 88, as the paper says). This lane reuses that code, unchanged.

### (a) `tsmom12`

Inputs: Sharpe 1.05 on the primary test (six assets, decisions 1994-02-01..2025-11-09, daily on
all calendar days: T = the calendar days in that window); against equal weight +0.17, p = 0.08,
SE about 0.12 (review-1, paired bootstrap, reproduced there); since 2003 +0.00 (p = 0.49).

Three tests, all reported:

1. **Absolute, as in the paper.** `DSR(SR = 1.05)`, null "no trial has skill" (`E` = 0).
2. **Against the project's own trials.** `SR0` = `E` + the luck term, with `E` the mean Sharpe of
   the trials on the same test (eq. 1 with its mean, as in the paper's appendix code). This asks
   "is `tsmom12` better than the best of N rules drawn from what this project typically finds",
   the question that matters for a long-only book whose trials all carry the market's Sharpe.
3. **Edge over equal weight.** In difference form: `Z((d - SE * maxZ(N)) / SE)`, d = +0.17,
   SE = 0.12 (bootstrap, so fat tails and serial dependence are already in it). Also d = +0.00
   for 2003-2025.

`V` (variance of trial Sharpes): (i) the primary test's spread from the census (variant +
baseline rows on that test); (ii) the cautious project-wide spread (selectable rows on any data,
the rule in DECISIONS 2026-11-12); never below 1/T. Skew and kurtosis are not logged anywhere:
normal (0, 3) is the main case; skew -1 with kurtosis 30 is the stress case, shown beside it.

**N, the trials made before `tsmom12` was chosen.** Reconstructed from the tries' UTC times and
git history; the assumption is that a row's time is when it ran (the harness writes it then):

- **N1, as the bar:** the protocol named `tsmom12` the plain twin before any test (commit times,
  2026-11-12), copying a published rule (Moskowitz, Ooi, Pedersen 2012) with the literature's
  12-month lookback. It then ranked first among the baselines of the first harness run on the
  primary test. N1 = the baseline rows on the primary test at that first run's minute.
- **N2, as the live rule (preset Middle):** the risk-map card (research-3, committed
  2026-11-12 08:15 +0100 = 07:15 UTC) picked the presets after runs 1 and 2. N2 = selectable rows
  (variant + baseline) on the primary test logged before 07:15 UTC that day, plus the risk map's
  20 menu rows, plus the 11 live strategies on `paper-trail` (tried, so they count; the
  repo's "overcounting is the cautious direction").
- **N3, if chosen today:** every selectable row (variant + baseline, train) anywhere in the
  project, plus the 11 live strategies. **M4, upper bound:** every row with a Sharpe of any kind.
- Effective N: the trial correlations need return series this lane does not have. Each N is
  shown raw and at `rho` = 0.5 and 0.9 (eq. 9). Also reported: the **break-even N**, the largest
  number of independent trials at which each test still gives DSR >= 0.95.

Bonferroni/Holm for `tsmom12`: p-values are `1 - PSR(0)` (absolute) and 0.08 (edge). Bonferroni
at family size m: reject if `p * m < 0.05`. Holm's first step is Bonferroni, so for the single
best hypothesis in a family the two agree; reported as the largest m at which each p survives
(`0.05 / p`).

### (b) The five best near-misses across the project

**Which five (rule fixed now, before collecting them):** candidates are ideas the lanes' own
write-ups (`research/*.md` on every branch) call a lead, a near miss, or parked, plus ideas that
passed a family bar but were not adopted. From those, the five with the smallest one-sided
p-value the lane reported against the comparator its card named (twin, `tsmom12`, equal weight
or Bitcoin). Ties or missing p: the larger reported Sharpe difference. An idea counts once, at
the variant its lane called primary (not its best variant, unless the card made it so).

For each: the edge `d` and its SE as the lane reported them (SE = d / Z^-1(1 - p) when only p
is given); `Z((d - SE * maxZ(N)) / SE)` at two N's: **N_family** (the selectable rows of its
own family, the bar the lane used) and **N_project** (N3 above); plus Bonferroni/Holm as for
`tsmom12`, with m = N_family, m = the number of candidates found, and m = N_project. Also the
absolute DSR of its own Sharpe at N_project where its test is long enough.

**Held-out year, rule fixed now.** A near-miss is worth a held-out year only if its held-out
year is still unspent (no `heldout` row for that family) and its edge DSR is >= 0.95 at
N_family and >= 0.50 at N_project. Passing 0.95 at N_project would make it a find on its own;
below 0.50 at N_project the held-out year (one year, about a third of a Sharpe-SE) cannot
change the verdict, so it would be spent for nothing.

**Tries rows.** The repo logs a row per configuration run through the harness (protocol,
"Counting tries"); this lane runs none, and `research/tries.md` does not exist on `main`.
No rows are added; the analysis is this file plus `research/dsr1.py`.

**Disclosed before the numbers:** the census numbers in section 1 (spreads 0.12 and 0.32), the
inputs quoted above from review-1 and `results/deflation.md` (research-2: 52 variants, luck
alone gives +0.24 over equal weight against +0.22 seen), and the lane's own rough mental guess
while planning that the absolute DSR could land near 0.5 under the widest spread. Every
scenario on this card is reported whatever it shows.

### Card note, 2026-11-18 ~23:05 UTC: the five near-misses found by the rule (inputs only, before any DSR is computed)

Searched every branch's `research/*.md` (315 distinct files) for "lead", "near miss",
"parked", "passes" and reported p-values. Candidates and the p each lane reported against its
own card's comparator (one-sided):

| Candidate | Lane | Status in the write-ups | p | In the five? |
|---|---|---|---:|---|
| `gsy-runup` flag100-sma (run-up exit on `tsmom12`, 30 French industries 1928-2001) | gsy-1 | "weak pass on the letter; not a candidate" | 0.001 | yes |
| `halving-and` (coins out 18-30 months after a halving) | macro-1 | parked, "not believed" | ~0.005 (90% range +0.06..+0.25) | yes |
| quiet coins: `turnover` TOP-TS on a 100-coin book | breadth-1 | passed its bar, lead; held-out year spent | printed 0.00 (< 0.005) | yes |
| funding carry `band` | carry-3 (short-1, carry-2) | passed train, failed held-out | 0.025 | yes |
| coin `stop-0.25` | coin-cap 1-4 | "a risk preference, not a proven rule" | 0.039 (sign test) | yes |
| `blend-ws` (`where-vol` + `stop-0.25`) | combo-1 | "closest miss the repo has had" | 0.059 | no (6th) |
| Fed-hiking gate on the S&P 500 1962-93 | macro-1 | "keep watching" | 0.06 (out of universe; primary lost) | no |
| `ath` | ideas-1 | nearest miss | 0.18 | no |
| `auction-concession` (book) | wide-1 | faint lead on TLT alone | 0.14 (TLT alone 0.05, a side test) | no |
| `where-vol` | trend-where | small gain, could be luck | 0.27 | no |

Left out by the rule: `fomc-cycle` (p 0.03, but dead: reversed after publication), `usd-1`
(a forecast replication that failed, no backtest), the evo-1/2 planted worlds (controls),
`fm-1` (memorised prices). The carry idea counts once, at carry-3's primary `band` (short-1's
`ls-premium`, p 0.096, is the same idea).

Clarifications (method, not results): (1) where a lane printed a 90% range, SE = width / 3.29
(as research-2's `lib/deflation.py` does); else SE = d / z(p). (2) A printed "0.00" is taken
as 0.005, the largest value it can mean (cautious). (3) The difference-form DSR is
`Z(z - maxZ(N))` with z = d / SE, so a sign test (coin-cap) enters through its p alone.
(4) N_family = the larger of the family's `variant` rows in the census and the lane's own
family count: gsy-1 12, macro-1 13 (six macro cards), breadth-1 61, carry-3 25, coin-cap 16
(the lane counts 15 rules). (5) Rows logged after the census snapshot (22:17 UTC) are left out
so the numbers reproduce. Script: `python research/dsr1.py dsr`.

### Results (computed 2026-11-18 ~23:15 UTC, after the card and the candidate note above were pushed)

`uv run python research/dsr1.py dsr`, unedited output:

Rows up to 2026-11-18 22:17 UTC: 2811. T for the primary test = 11,605 calendar days. Luck floor 1/T = 0.0315 a year (variance of an annual Sharpe).

| Trial count | N | at rho 0.5 | at rho 0.9 |
|---|---:|---:|---:|
| N1 bar (first harness run) | 8 | 4.5 | 1.7 |
| N2 live preset (risk map) | 89 | 45 | 9.8 |
| N3 if chosen today | 947 | 474 | 96 |
| M4 every row with a Sharpe | 2,414 | 1,208 | 242 |

Variance of trial Sharpes (annual): primary test 0.0142 (mean 0.95, 256 rows); project-wide selectable variants 0.1032 (mean 0.78). The primary-test spread is below the luck floor 0.0315, so the floor is used there.

#### (a1) `tsmom12`, absolute (paper's null: no trial has skill)

| N | V | SR0 (annual) | DSR normal | DSR stress (skew -1, kurt 30) |
|---|---|---:|---:|---:|
| N1 bar (first harness run): 8.0 | primary | 0.26 | 1.0000 | 1.0000 |
| N1 bar (first harness run): 8.0 | project | 0.47 | 0.9995 | 0.9992 |
| N1 bar (first harness run) (rho 0.9): 1.7 | primary | 0.06 | 1.0000 | 1.0000 |
| N1 bar (first harness run) (rho 0.9): 1.7 | project | 0.12 | 1.0000 | 1.0000 |
| N2 live preset (risk map): 89 | primary | 0.44 | 0.9997 | 0.9995 |
| N2 live preset (risk map): 89 | project | 0.80 | 0.9207 | 0.9130 |
| N2 live preset (risk map) (rho 0.9): 9.8 | primary | 0.28 | 1.0000 | 1.0000 |
| N2 live preset (risk map) (rho 0.9): 9.8 | project | 0.50 | 0.9990 | 0.9985 |
| N3 if chosen today: 947 | primary | 0.57 | 0.9963 | 0.9951 |
| N3 if chosen today: 947 | project | 1.04 | 0.5205 | 0.5197 |
| N3 if chosen today (rho 0.9): 96 | primary | 0.45 | 0.9997 | 0.9995 |
| N3 if chosen today (rho 0.9): 96 | project | 0.81 | 0.9136 | 0.9057 |
| M4 every row with a Sharpe: 2,414 | primary | 0.62 | 0.9923 | 0.9902 |
| M4 every row with a Sharpe: 2,414 | project | 1.12 | 0.3387 | 0.3441 |
| M4 every row with a Sharpe (rho 0.9): 242 | primary | 0.50 | 0.9990 | 0.9986 |
| M4 every row with a Sharpe (rho 0.9): 242 | project | 0.91 | 0.7873 | 0.7790 |

For comparison, equal weight (Sharpe 0.88, a rule nobody searched for) in the same test: V project, N3 if chosen today: 0.182; N1, V primary: 0.9998. The absolute test cannot tell a trend rule from holding the market.

Break-even N (largest number of independent trials with DSR >= 0.95): V primary: 58,940; V project: 62.

#### (a2) `tsmom12` against the project's own trials (eq. 1 with their mean)

| N | Mean and V of the trials | SR0 (annual) | DSR normal | DSR stress |
|---|---|---:|---:|---:|
| N1 bar (first harness run): 8.0 | primary (0.95) | 1.21 | 0.180 | 0.189 |
| N1 bar (first harness run): 8.0 | project (0.78) | 1.25 | 0.132 | 0.140 |
| N1 bar (first harness run) (rho 0.9): 1.7 | primary (0.95) | 1.02 | 0.573 | 0.571 |
| N1 bar (first harness run) (rho 0.9): 1.7 | project (0.78) | 0.89 | 0.809 | 0.800 |
| N2 live preset (risk map): 89 | primary (0.95) | 1.40 | 0.026 | 0.030 |
| N2 live preset (risk map): 89 | project (0.78) | 1.58 | 0.001 | 0.002 |
| N2 live preset (risk map) (rho 0.9): 9.8 | primary (0.95) | 1.23 | 0.154 | 0.163 |
| N2 live preset (risk map) (rho 0.9): 9.8 | project (0.78) | 1.28 | 0.095 | 0.103 |
| N3 if chosen today: 947 | primary (0.95) | 1.53 | 0.004 | 0.005 |
| N3 if chosen today: 947 | project (0.78) | 1.82 | 0.000 | 0.000 |
| N3 if chosen today (rho 0.9): 96 | primary (0.95) | 1.40 | 0.024 | 0.029 |
| N3 if chosen today (rho 0.9): 96 | project (0.78) | 1.59 | 0.001 | 0.002 |
| M4 every row with a Sharpe: 2,414 | primary (0.95) | 1.57 | 0.002 | 0.002 |
| M4 every row with a Sharpe: 2,414 | project (0.78) | 1.90 | 0.000 | 0.000 |
| M4 every row with a Sharpe (rho 0.9): 242 | primary (0.95) | 1.46 | 0.011 | 0.014 |
| M4 every row with a Sharpe (rho 0.9): 242 | project (0.78) | 1.69 | 0.000 | 0.000 |

Break-even N: primary (0.95): none (fails at N = 1); project (0.78): none (fails at N = 1).

#### (a3) `tsmom12`'s edge over equal weight (difference form)

| Window | d | z | N | DSR | Edge left after luck (d - SE maxZ) |
|---|---:|---:|---|---:|---:|
| `tsmom12` vs equal weight | +0.17 | 1.41 | N1 bar (first harness run): 8 | 0.478 | -0.01 |
| `tsmom12` vs equal weight | +0.17 | 1.41 | N2 live preset (risk map): 89 | 0.139 | -0.13 |
| `tsmom12` vs equal weight | +0.17 | 1.41 | N3 if chosen today: 947 | 0.033 | -0.22 |
| `tsmom12` vs equal weight | +0.17 | 1.41 | M4 every row with a Sharpe: 2,414 | 0.018 | -0.25 |
| `tsmom12` vs equal weight, 2003-2025 | +0.00 | 0.03 | N1 bar (first harness run): 8 | 0.076 | - |
| `tsmom12` vs equal weight, 2003-2025 | +0.00 | 0.03 | N2 live preset (risk map): 89 | 0.007 | - |
| `tsmom12` vs equal weight, 2003-2025 | +0.00 | 0.03 | N3 if chosen today: 947 | 0.001 | - |
| `tsmom12` vs equal weight, 2003-2025 | +0.00 | 0.03 | M4 every row with a Sharpe: 2,414 | 0.000 | - |
| | | | break-even N (1994-2025) | none (fails at N = 1) | |

#### (b) The five near-misses

| Near-miss | Lane | Against | d | p | z | N_family | DSR at N_family | DSR at N3 = 947 | at N3, rho 0.9 | Absolute DSR at N3 (V project) | Held-out year |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `gsy-runup` flag100-sma | gsy-1 | `tsmom12`, 30 French industries 1928-2001 | +0.027 | 0.0010 | 3.09 | 12 | 0.923 | 0.441 | 0.718 | 0.396 | unspent |
| `halving-and` | macro-1 | `tsmom12`, six assets | +0.15 | 0.0050 | 2.60 | 13 | 0.814 | 0.260 | 0.533 | 0.815 | unspent |
| quiet coins (`turnover` TOP-TS) | breadth-1 | `tsmom12` on the same coin book | +0.34 | 0.0050 | 2.58 | 61 | 0.589 | 0.253 | 0.524 | 0.310 | spent (passed: 0.61 vs 0.31) |
| funding carry `band` | carry-3 | zero (pooled Sharpe > 0) | +0.79 | 0.0250 | 1.96 | 25 | 0.485 | 0.100 | 0.290 | 0.064 | spent (failed: -0.65) |
| coin `stop-0.25` | coin-cap 1-4 | a coin cap of the same cost (sign test, 21 episodes) | +0.714 | 0.0392 | 1.76 | 16 | 0.484 | 0.069 | 0.225 | 0.609 | unspent |

#### Bonferroni and Holm (one-sided p, alpha 0.05)

| Hypothesis | p | Survives Bonferroni up to m = | Holm-adjusted, m = 6 | Bonferroni at N_family | Holm-adjusted at m = N3 = 947 |
|---|---:|---:|---:|---:|---:|
| `tsmom12` vs equal weight | 0.0800 | 0.6 | 0.080 | 0.640 (m = 8) | 1.000 |
| `gsy-runup` flag100-sma | 0.0010 | 50 | 0.006 | 0.012 (m = 12) | 0.947 |
| `halving-and` | 0.0050 | 10 | 0.025 | 0.065 (m = 13) | 1.000 |
| quiet coins (`turnover` TOP-TS) | 0.0050 | 10 | 0.025 | 0.305 (m = 61) | 1.000 |
| funding carry `band` | 0.0250 | 2.0 | 0.075 | 0.625 (m = 25) | 1.000 |
| coin `stop-0.25` | 0.0392 | 1.3 | 0.078 | 0.627 (m = 16) | 1.000 |

`tsmom12` absolute (Sharpe > 0): p = 1.7e-09, survives Bonferroni up to m = 30,292,480.

Card's held-out rule (unspent, DSR >= 0.95 at N_family and >= 0.50 at N3):

- `gsy-runup` flag100-sma: no
- `halving-and`: no
- quiet coins (`turnover` TOP-TS): no
- funding carry `band`: no
- coin `stop-0.25`: no

### What the numbers say

- **The trials on the primary test are mostly copies of one another.** Their Sharpe spread
  (variance 0.014) is below what luck alone gives one rule over 32 years (0.0315). That is
  only possible if they move together: most are `tsmom12` with something added. So the raw
  counts overstate the independent trials, and the rho 0.9 rows are the realistic ones for the
  primary test. The project-wide spread (0.103) mixes tests of different data and lengths and
  is the cautious upper end, as DECISIONS 2026-11-12 intends.
- **`tsmom12` makes money: that survives everything.** Sharpe 1.05 over 11,605 days is > 0 with
  p = 1.7e-9 (Bonferroni would allow 30 million tests). The absolute DSR stays >= 0.95 up to
  58,940 independent trials at the primary test's spread; only with the project-wide spread and
  more than 62 independent trials does it drop (0.52 at N3 = 947 raw, 0.91 at rho 0.9). But
  equal weight, which nobody searched for, passes the same test (0.9998 at N1): this test
  rewards holding risky assets, not the trend rule.
- **`tsmom12`'s edge over holding does not survive, and never did.** Alone it was +0.17,
  p = 0.08: below 0.95 already at N = 1 (0.92). At the eight baselines it was ranked first
  among, DSR 0.48 and the edge left after luck is -0.01; at the live pick (N2 = 89) 0.14; if
  picked today (947) 0.03. Since 2003 the edge is zero (review-1). Against the project's own
  trials (test 2) it is not outstanding at any N (DSR 0.18 at N1, 0.02-0.15 at N2).
- **No near-miss survives the project's search.** At its own family's size the best is
  `gsy-runup` (DSR 0.92; Bonferroni at m = 12 gives 0.012, Holm in the family of six 0.006),
  but its edge is +0.027 Sharpe, from 1928-2001, and fades after 2002 (p 0.2). At N3 = 947
  every near-miss is between 0.07 and 0.44 (0.23-0.72 at rho 0.9); Holm at m = 947 adjusts
  every p to >= 0.95. By the card's rule **none is worth a held-out year**: the two whose
  year is unspent and that come closest (`gsy-runup`, `halving-and`) fail 0.95 at their own
  family size.
- **Sensitivity.** Skew -1 and kurtosis 30 move the absolute DSR by less than 0.01 (daily
  Sharpe is small, so the higher moments hardly enter); the verdicts rest on N and V.

Tries rows: none added (no configuration was run; the repo logs harness runs, see the card).
