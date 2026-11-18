# combo-1: where the credible models fail, and whether two that fail apart beat `tsmom12`

Research lane combo-1 (DEEPER), night 2026-11-18. Branch `combo-1` (from `main`; `research/`
copied unchanged from `coin-cap-3`), draft PR #70 into `main`. Research only: fake money, saved
outputs and the price cache already on disk, no change to the gym, the runner or the live rules.

Owner direction: study the existing models, why each fails where it does, and combine models
whose strengths cover each other's weaknesses. deep-1 (#36) already did this for the 52 models
of runs 1-2, macro-1, rl-1/2 and ideas-1 ("they are the same six assets held at different
sizes, so they lose in the same weeks"; three walk-forward mixes all failed; hindsight ceiling
1.22). This lane does not redo that. It adds the lanes that finished after deep-1 (trend-where,
cointop-1/coin-cap, carry-3) and new cuts deep-1 did not make (chop, crash speed, the
stock-bond rate regime, excess-return correlation between models by regime).

## Step 1: the failure map (2026-11-18)

Tables: [`results/combo-1-map.md`](results/combo-1-map.md), from `lib/combo1_map.py`. No
backtest was run and nothing was selected: every series is a configuration already logged in a
lane's `tries.md`, read from saved output. Each reproduces its logged Sharpe (`tsmom12` 1.05,
`where-vol` 1.07, `stop-0.25` 1.09, `band` 0.79).

**Which models, and why these six.** The most credible near-misses of every line that is not
dead by a wide margin, plus the two opposites deep-1 named:

- `trend-vol` (run 1, tv40): trend with slots sized by volatility; deep-1's best risk shape.
- `where-vol` (trend-where): the filter kept only where the days out were rougher (1.07).
- `stop-0.25` (cointop-1, coin-cap 1-3): a 25% stop on the coin slots (1.09, worst loss 28.9%).
- `inverse-vol` (protocol twin): always invested, risk-sized: the opposite of stepping out.
- `sixty-forty` (benchmark): the lowest loss-week correlation with `tsmom12` in deep-1's pool.
- `band` (carry-3): funding carry on perpetuals, the only other source of return (2021-25,
  failed its held-out year).

Left off, with the reason: the gsy-1 crash flags (no six-asset series; their gain is pre-2002
and fades after), `fomc-cycle` and the other calendar effects (reversed after publication),
the ML/RL/macro models (deep-1's atlas covers them; nothing new since).

### The map: where each one loses to `tsmom12`

Sharpe 1994-2025 (since 2003); excess = the model's return minus `tsmom12`'s, % a year, in each
regime (thresholds in the results file). "Turn" = the six months after each of `tsmom12`'s ten
deepest lows. Stress-window figures are points of total return, model minus `tsmom12`.

| Model | Sharpe (2003-) | Loses to `tsmom12` where | Wins where | Corr. with `tsmom12` in its losing weeks |
|---|---|---|---|---:|
| `tsmom12` | 1.05 (1.20) | (yardstick: -129%/yr in fast falls, -32%/yr into its top-10 falls) | turns +48%/yr, trend-on +22%/yr | |
| `trend-vol` | 1.03 (1.22) | chop -11, trend on -5, **turn -19**, covid rebound -10 pts | fast falls +39, top-10 falls +12, crypto winters +3..+8 pts | 0.88 |
| `where-vol` | 1.07 (1.23) | **fast falls -10, 2022 rate shock -13 pts, crypto winter 2022 -14 pts**, era 2022-25 0.84 vs 0.90 | chop +2, trend mixed +3, stock-bond+ +6, turns after 2022 +21 pts | 0.96 |
| `stop-0.25` | 1.09 (1.33) | **chop -7, stock-bond+ -7, turn -21**, covid rebound -13 pts, era 2022-25 0.70 vs 0.90 | fast falls +54, crypto winters +6..+18 pts, covid crash +13 pts | 0.78 |
| `inverse-vol` | 0.85 (1.32) | **slow bears on a narrow book: dot-com -33 pts**, 2008 -7, 2022 -14 pts, fast falls -40, chop -12 | turns: +15..+22 pts after five of seven windows, crypto winters 2014/2018 | 0.70 |
| `sixty-forty` | 0.76 (0.85) | trend on -12, chop -20, **turn -32**, 2008 -26 pts, 2022 -12 pts | `tsmom12`'s losing weeks +50, crypto winters 2014 and 2018 +28 and +20 pts | 0.44 |
| `band` (2021-25) | 0.79 | trend on -8, stock-bond+ -15, turn -17; held-out year -0.65 | 2022 rate shock +28, crypto winter 2022 +25 pts; worst 10% of `tsmom12` weeks +0.36% vs -3.90% | 0.01 |

### Why each fails where it does

1. **`trend-vol`, `stop-0.25`, `inverse-vol` and `sixty-forty` are one bet: less exposure when
   it hurts.** Their excess returns over `tsmom12` correlate +0.48 to +0.88 with each other in
   every regime except slow bears. Each is ahead in the fast falls and in `tsmom12`'s losing
   weeks and gives it back in the turn (-19 to -32% a year in the six months after each low),
   in chop and while trends are on. That is the price of holding less: they are risk levels,
   not complements (deep-1's finding, now regime by regime). `stop-0.25` is the sharpest
   version: it buys the fast coin crash (+54% a year in fast falls) and pays in the turn
   (re-entry late) and in chop (stopped out, then the trend resumes).
2. **`where-vol` fails in the opposite place.** It holds bonds (from 2009), gold (2015) and
   coins (2019/2023) without the filter, so it loses when those fall together and fast: the
   2022 rate shock (-13 points), the 2022 crypto winter (-14), fast falls in general (-10% a
   year). It wins back in chop and in the turns (no late re-entry on those slots). Its excess
   is uncorrelated with the de-risking group (-0.02 to +0.29; with `stop-0.25`: 0.00 overall,
   0.00 in `tsmom12`'s losing weeks, -0.19 in slow bears).
3. **`inverse-vol` fails in long bears on a narrow book** (2000-02: a book of SPY and QQQ;
   -33 points) and in 2022 (bonds fell with stocks), and wins every turn: the slots `tsmom12`
   leaves empty earn the rebound (deep-1 failure mode 2).
4. **`band` is the only model uncorrelated with `tsmom12` itself** (0.05 overall, 0.01 in its
   losing weeks; positive in its worst weeks). It also loses in the turn and in the 2022 kind of
   rate regime. But it has 4.7 years, is not in the gym (perpetuals, shorts), and in its one
   held-out year it lost together with `tsmom12` (carry-3: -0.65 vs BTC/ETH `tsmom12` -1.49;
   the 50/50 blend was worse than `tsmom12` alone).

**The complementarity story in one line.** Inside the gym's six assets there is one pair that
fails at different times and is ahead of `tsmom12` on its own: `where-vol` (loses in fast joint
falls of bonds/gold/coins, wins chop and turns) and `stop-0.25` (wins fast coin falls, loses
chop and turns), excess correlation 0.00. Everything else either is the same de-risking bet as
the other (pairs +0.5 to +0.9) or is out of the gym (`band`). Nothing on the map wins both the
fast fall and the turn: whatever buys the fall pays for it in the six months after the low.
