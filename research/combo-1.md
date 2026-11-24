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

## Step 2: card (fixed 2026-11-18, after the map, before any combination number)

**What had been seen.** Everything on the map above (full-train tables, which is why the train
test below is partly circular: see "How the bar reads"), deep-1's atlas and Part B, every
finished lane's write-up. No blend of any kind has been computed in this lane.

**Selection rules (stated, applied to the map, no weights fitted).** Gym-tradable means a
long-only six-asset book with target weights (so `band` is out: perpetuals and shorts, 2021-25
only, held-out year spent). Two combinations, no more:

- **A `blend-iv` (cover `tsmom12`'s losses).** Rule: `tsmom12` plus the gym-tradable model with
  the lowest correlation with `tsmom12` in `tsmom12`'s losing weeks, among those that exist on
  all three out-of-universe sets (bar 4 needs them; `sixty-forty`, 0.44, needs SPY and TLT and
  exists on none). Applied: `inverse-vol` 0.70 < `stop-0.25` 0.78 < `trend-vol` 0.88 <
  `where-vol` 0.96, so **`tsmom12` + `inverse-vol`**. Mechanism: `inverse-vol` wins the turns
  `tsmom12` misses and loses the slow bears `tsmom12` sits out.
- **B `blend-ws` (two overlays that fail apart).** Rule: among gym-tradable models ahead of
  `tsmom12` on full-train Sharpe, the pair whose excess returns (each minus `tsmom12`) have the
  lowest correlation in `tsmom12`'s losing weeks. Qualify: `where-vol` 1.07, `stop-0.25` 1.09
  (`trend-vol` 1.03, `inverse-vol` 0.85, `sixty-forty` 0.76 do not). One pair, correlation
  0.00: **`where-vol` + `stop-0.25`**. Mechanism: `where-vol` loses fast joint falls and wins
  chop and turns; `stop-0.25` the reverse, on the coin slots.

**Machinery (both, the same).** Each sleeve is the logged configuration rebuilt through the
harness (`where-vol`: trend-where's `Where("vol")`; `stop-0.25`: cointop-1's `rule(stop_ok)`;
`tsmom12` and `inverse-vol`: the protocol's), checked against its logged Sharpe. Sleeve shares
are equal risk: proportional to 1 / standard deviation of the sleeve's weekly returns (7-day
blocks, its own gym replay) over the last 156 weeks before the refit (all there are if fewer;
equal shares until 26 weeks exist), refitted on the first Friday of each calendar year from
returns up to the day before, held to the next refit (deep-1's schedule). The combined target
weights are the shares times the sleeves' target weights, summed per asset, replayed through
`gym.simulate` as one account at the protocol's costs (25 bps fee + 5 bps slip on crypto, 2 bps
on ETFs; `main`'s gym default of 60 bps is not used, so every number compares with the logged
ones). No other parameter exists: no sweep, no fixed-capital alternative, no other pair.

**Pass bar (each on its own; twin `tsmom12` rebuilt the same way).**

1. Sharpe on the six assets, full train, beats `tsmom12` with paired stationary bootstrap
   (block 20 days, 2,000 draws) one-sided **p < 0.10 / 72 = 0.0014**. Family: the `wide-*`
   lineage's 61, survey-4's 4, wide-5's W9-W10 (2), deep-1's three combination rules and these
   two (72). If a lane has added more by the verdict, the stricter bar is used.
2. Ahead of `tsmom12` in at least 4 of the 5 eras.
3. Worst loss not more than 5 points deeper than `tsmom12`'s.
4. Out of universe: Sharpe difference to `tsmom12` positive in at least 2 of 3 sets (8 other
   ETFs, 6 other coins, 4 indexes as one portfolio), the rule rerun unchanged with the sleeves
   rebuilt there (`stop-0.25` acts on coins only, so on ETFs and indexes it equals `tsmom12`).
5. Beats equal weight on Sharpe.
6. Since 2003 not behind `tsmom12` and not behind equal weight.

Also reported, not bars: average sleeve shares, the book's distance from `tsmom12`'s weights,
the six regimes of the map for each blend.

**How the bar reads.** The pairs were picked on the full-train map, so bars 1-3, 5 and 6 are
in-sample for the choice; bar 4 is the honest part (where-vol's and stop's OOU runs exist, but
no blend was ever computed there). A pass makes a candidate for a separate held-out card (the
held-out year is not touched in this lane), nothing more.

**Tries.** Each blend on the six assets: `variant` under idea `combo-1` (2 rows). Each blend
out of universe: `robustness` (6 rows). Sleeve rebuilds that reproduce a logged configuration
are not logged again; a sleeve configuration that has no row yet is logged as `robustness`.

## Step 3: verdict (2026-11-18)

Tables: [`results/combo-1.md`](results/combo-1.md), from `lib/combo1_blend.py` (one logged run,
2026-11-18 22:15 UTC; 8 rows in `tries.md`: 2 `variant`, 6 `robustness`). The sleeves
reproduce their logged Sharpe; the look-ahead check (scrambled future returns leave a refit's
shares unchanged) passed. Held-out year untouched.

**Neither blend beats `tsmom12` honestly. `blend-ws` (`where-vol` + `stop-0.25`, equal risk) is
the closest miss the repo has had: Sharpe 1.13 against 1.05 (p = 0.059), worst loss 28.9%
against 36.5%, above both of its own sleeves (1.07, 1.09). It fails the family bar (p < 0.0014
needs about +0.15) and the era bar (ahead in 2 of 5: ties in 1994-99 and 2000-09, behind in
2022-25).**

| Six assets, 1994-2025 | Sharpe | vs `tsmom12` (p) | Since 2003 | 2022-25 | Worst loss | Growth/yr | Bars passed |
|---|---:|---:|---:|---:|---:|---:|---|
| `blend-ws` = `where-vol` + `stop-0.25` | 1.13 | +0.08 (0.059) | 1.35 | 0.82 | 28.9% | +17.2% | 3, 4, 5, 6; fails 1, 2 |
| `blend-iv` = `tsmom12` + `inverse-vol` | 1.07 | +0.02 (0.385) | 1.42 | 0.93 | 44.4% | +15.1% | 2, 4, 5, 6; fails 1, 3 |
| `tsmom12` | 1.05 | | 1.20 | 0.88 | 36.5% | +17.8% | |
| equal weight | 0.88 | | 1.19 | 0.67 | 68.8% | +18.2% | |

Out of universe (Sharpe minus `tsmom12`): `blend-ws` +0.02 on the ETFs, +0.02 on the coins,
+0.00 on the indexes; `blend-iv` +0.01, +0.12, -0.03.

**What it says.**

1. **Complementarity is real but small.** Two overlays whose excess returns are uncorrelated
   (0.00) blend into something better than either: +0.08 Sharpe and the stop's shallower worst
   loss kept at almost no growth cost (17.2% against 17.8% a year). That is the diversification
   arithmetic of two weak, independent edges (each about +0.03), not a new edge. With
   uncorrelated excess the blend's information ratio rises by about the square root of two;
   it would need edges about twice as large to clear the bar.
2. **The blend fails exactly where the map said both sleeves are weak at once: 2022-25.**
   `where-vol` lost the 2022 rate shock and crypto winter (unfiltered bonds, gold, coins);
   `stop-0.25` lost the 2023-24 turn (late re-entry). Different months, same era: the blend is
   behind there (0.82 against 0.88). By the map's regimes it still loses in the turn (-11.6% a
   year in the six months after `tsmom12`'s lows) and gains in fast falls (+27%).
3. **Out of universe there is almost nothing to carry.** The stop acts on coins only, and
   `where-vol` equals `tsmom12` on the indexes, so on two of the three sets `blend-ws` is half
   of a near-copy (distance from `tsmom12` 0-2%). Its "pass" on bar 4 is +0.02, +0.02, +0.00:
   positive, not evidence.
4. **`blend-iv` is the risk dial again.** Half in an always-invested book wins the turns and
   the post-2003 years (1.42 against 1.20) and pays in the long bear on a narrow book: worst
   loss 44.4% (2000-02). Same verdict as deep-1's average and `inverse-vol` itself.
5. **The pick was made on the full-train map**, so bars 1-3, 5 and 6 are in-sample for the
   choice; p = 0.059 overstates the evidence, not understates it.
6. **Not judgeable forward either.** Its excess over `tsmom12` has an information ratio of
   about 0.28 a year (t 1.56 over 31.8 years); detecting that at 80% power (alpha 0.025) takes
   about a century of forward data.

**Status:** both dead by the card. The held-out year stays unspent. No change to the live rule.

### What the failure map says about the next lane

The map's hard fact: **nothing on it wins both the fast fall and the turn.** Every model that
loses less in a fall gives it back in the six months after the low (-17 to -32% a year), and
the one model that wins the turn (`where-vol`) loses the fast joint fall. Blending two of them
averages the two failures; it cannot remove them. So the next lanes worth running attack one
failure directly, each with its own card:

1. **`stop-reentry` (D, from coin-cap-3):** keep the coin stop's fall protection and fix its
   turn loss (-21% a year after lows): a re-entry rule for a stopped coin (e.g. back in at a
   new 4-week high), judged on coin-cap-2's 21 coin-crash episodes on 197 coins, twin
   `stop-0.25`, then carried unchanged to BTC/ETH.
2. **`combo-cash` (D, cheap):** rerun this map and both blends with T-bill interest on idle
   cash (`cash-interest`, #61). Every de-risking model, `tsmom12` included, sits in cash in
   its winning regimes, and in 2022-25 cash paid 0-5%: the de-risking sleeves gain against
   `where-vol` and `inverse-vol`, so the ranking of the failures may move. Robustness rows only.
3. **A complement for the stock-bond-together regime (W):** in the 2022 kind of year (stocks
   and bonds positively correlated, 13% of days) every gym-tradable model loses; only the
   out-of-gym carry book won. A long-only candidate needs another return source available in
   the gym (commodities, short-dated Treasuries/T-bills as a slot): card a `tsmom12` slot set
   that adds DBC and a T-bill ETF, judged on that regime first.
