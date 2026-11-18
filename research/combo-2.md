# combo-2: combo-1 with T-bill cash, a partner for the years stocks and bonds fall together

Research lane combo-2 (DEEPER), night 2026-11-18. Branch `combo-2` (from `combo-1`, #70),
draft PR #75 into `combo-1`. Research only: fake money, the price cache already on disk, no
change to the live rules. Costs: the protocol's, passed explicitly (25 bps fee + 5 bps slip on
crypto, 2 bps on ETFs), as in combo-1.

Starting point (combo-1, `combo-1.md`): four of six models are one de-risking bet; `blend-ws`
(`where-vol` + `stop-0.25`, equal risk) 1.13 against `tsmom12` 1.05 (p 0.059) is the closest
miss, behind in 2022-25 where both sleeves fail; nothing wins both the fast fall and the turn.

## Step 1 card: `combo-cash` (fixed 2026-11-18, before any number with interest)

**How the cash interest got here.** `origin/cash-interest` (#61, base `main`, the same `main`
commit `combo-1` started from) is merged into this branch with a merge commit (957fdd1), so the
gym code arrives unchanged: `gym.simulate(rates=...)` pays idle cash the 13-week T-bill rate
(`^IRX`), accrued every calendar day, a session's rate known from its close. The only conflict
was `next-steps.md` (both sections kept). Research plumbing: `harness.run(rates=...)` (default
nothing, so every earlier script is unchanged) and `harness.bill_rates()` (the cached
`research/data/bars/IRX.csv`, train cut at 2025-11-10). `combo1_map.py` was split into
`main` + `tables` so the same tables can be drawn for other series; its output is byte-identical
(checked: rerun leaves `results/combo-1-map.md` unchanged).

**What is rerun, exactly as carded, no new choices.**

- The failure map: the six gym models of combo-1's map (`tsmom12`, `trend-vol`, `where-vol`,
  `stop-0.25`, `inverse-vol`, `sixty-forty`) plus the equal-weight yardstick, rebuilt from their
  logged configurations through the harness with T-bill cash. Same five tables. The regime
  masks (trend state, chop, fast fall, slow bear, stock-bond sign, `tsmom12`'s ten deepest
  falls and the six months after) are combo-1's, computed from the series without interest, so
  the regime days do not move and only returns change. `band` (perpetual carry, out of the gym)
  stays as saved: its collateral sits in the perps venue, not in gym cash.
- Both blends (`blend-iv`, `blend-ws`) on all four sets (six, 8 ETFs, 6 coins, 4 indexes), with
  combo-1's equal-risk shares, yearly refit, sleeves and costs; the sleeves, the combined book,
  the `tsmom12` twin and equal weight all get T-bill cash. The pass bar is combo-1's six bars,
  family 72 (p < 0.0014).

**Sharpe convention.** Two readings, both reported: (a) the carded statistic, Sharpe against
0 (the protocol's convention, what `tries.md` logs), and (b) Sharpe above the T-bill rate the
gym paid, #61's scoreboard convention (rf from an all-cash book replayed in the same gym, so it
is aligned day for day). The verdict on the card is read on (a); (b) is reported so a merge of
#61 does not silently change it.

**What would count as "a conclusion changes".** Any of: a blend's pass/fail on any bar; the
order of the six models' full-train Sharpes; the sign of any cell of the map's regime table
(section 2) that combo-1's text relies on (the de-risking group's turn and chop losses, their
fast-fall gains, `where-vol`'s fast-fall and 2022 losses); the de-risking group's excess
correlations dropping below +0.5 or `where-vol` + `stop-0.25` leaving -0.1..+0.1.

**Tries.** Robustness rows only, idea `combo-2`: the six map models with cash (6) and the two
blends on four sets with cash (8). Sleeve rebuilds inside the blend runs are not logged again
(the same decisions as their rows). These rows do not count in the family bar (no new pick).

## Step 1 result: `combo-cash` (2026-11-18)

Tables: [`results/combo-2-cash.md`](results/combo-2-cash.md), from `lib/combo2_cash.py` (one
logged run, 22:23 UTC; 14 `robustness` rows in `tries.md`). Plumbing check: `tsmom12` rebuilt
without interest reproduces deep-1's atlas series exactly. Average bill rate 2.4% a year on
the six assets' span, 4.4% on the indexes' (from 1962).

**No verdict changes; both blends still fail the card. Cash interest lifts every cash-holding
book about equally, so most of combo-1's map survives unchanged. Four details move.**

| Six assets, 1994-2025 | Sharpe vs 0, before -> with cash | above T-bills | vs `tsmom12` (p), with cash | 2022-25 | Worst loss | Card |
|---|---:|---:|---:|---:|---:|---|
| `tsmom12` | 1.05 -> 1.08 | 0.93 | | 0.90 -> 0.97 | 36.5 -> 35.6% | |
| `blend-ws` | 1.13 -> 1.16 | 1.00 | +0.08 (0.051); above bills +0.06 (0.108) | 0.82 -> 0.91 | 28.9 -> 25.7% | fails 1, 2 (as before) |
| `blend-iv` | 1.07 -> 1.09 | 0.91 | +0.01 (0.450); above bills -0.02 (0.590) | 0.93 -> 0.97 | 44.4 -> 42.8% | fails 1, 2, 3, 4 (was 1, 3) |

What changed, against "what would count" in the card:

1. **`blend-iv` gets worse: it now fails four bars, not two.** Eras 3 of 5 (2022-25 is now a tie
   at 0.97, 2000-09 behind) and out of universe 1 of 3 (indexes -0.09, ETFs -0.01). The
   always-invested half earns no interest, the `tsmom12` it is compared with does: half of the
   blend gives up the cash yield. Dead either way.
2. **`blend-ws` is unchanged in substance:** +0.08 against 0 (p 0.051, bar 0.0014), +0.06 above
   T-bills (p 0.108); still behind `tsmom12` in 2022-25 (0.91 against 0.97); indexes now -0.01
   (was +0.00), so bar 4 rests on +0.02 ETFs and +0.04 coins. Worst loss 25.7% against 35.6%.
3. **Order of the map's Sharpes: `trend-vol` catches `tsmom12`** (1.076 each, against 0; was
   1.03 against 1.05): the most cash-heavy rule gains most. Above T-bills it is behind again
   (0.89 against 0.93), so this is the convention, not a new edge. `where-vol`'s lead shrinks
   (+0.015, was +0.02); `stop-0.25` keeps +0.05.
4. **2022-25 is less bad for the cash holders.** `tsmom12` 0.97 (was 0.90), `stop-0.25` 0.87
   (0.70); `where-vol` stays 0.86 (it held bonds, not cash). Above T-bills every book is lower
   (`tsmom12` 0.72, `where-vol` 0.64, `stop-0.25` 0.50).

Unchanged: every regime cell's sign that combo-1's text uses (de-risking group: turn -19 to
-32% a year, chop -7 to -21, fast falls +36 to +54 except `inverse-vol` at -41, as in combo-1's
table; `where-vol`: fast falls -10.3, 2022 rate
shock -13 points), every pair correlation within 0.02 (de-risking pairs +0.48..+0.94,
`where-vol` + `stop-0.25` -0.02). The one sign flip, `inverse-vol` in trend-off (+1.6 -> -0.7),
is a cell the text does not use: `tsmom12` sits in cash there and now earns on it.

**Reading.** combo-1's conclusions are robust to cash accounting. The rate matters for the
blends only through the half that holds no cash (`inverse-vol`), which falls further behind.
The 2022 gap is still there with cash: in 2022-25 `blend-ws` trails `tsmom12` with or without
interest, because its sleeves lost in assets (bonds, coins), not in cash.

## Step 2 card: `cofall-dbc`, one partner for the years stocks and bonds fall together (fixed 2026-11-18, before any number)

**What had been seen.** Step 1 above and everything combo-1 saw. No DBC series has been
computed on the six-asset book or in any gate in this lane; DBC has been in the protocol's
8-ETF out-of-universe set since run 1 (seen there only as one of eight assets). General market
history is known to the author (commodities rose in 2022 and in the 1970s, fell in 2008 and
2014-15): that is the hypothesis, not a result.

**The gap.** combo-1 and step 1: in the stock-bond-together regime (13% of days) every gym
model loses or ties, and in 2022-25 `tsmom12` and both blends lose to their own past; `tsmom12`
sits in cash there. The question is whether a long-only, gym-tradable partner earns in exactly
those weeks.

**Selection rule between the two named candidates (written before results).** Pick the one
whose return in the gate is not mechanically equal to what `tsmom12` already holds there. With
step 1's cash accounting, a T-bill slot the rule moves to when the stock and bond trends are
negative *is* the cash `tsmom12` already holds in those weeks (the gym now pays the bill rate
on it), so it cannot change a single return: it is degenerate, not a test. That leaves **DBC**
(a broad commodity futures ETF, research cache from 2006-02-06, total-return adjusted). The
T-bill stays in the rule as the fallback: when the gate is open and DBC is not trending, the
slot stays in cash at the bill rate.

**The rule (`cofall-dbc`).** Weekly, Friday, like `tsmom12`; only bars closed before the
decision.

1. On the six live assets: exactly `tsmom12` (each eligible asset an equal slot of 1/n, held
   when its 365-day return is positive). n counts only the six live assets; DBC never changes
   their slots.
2. Gate: SPY and TLT both eligible and both with a 365-day return of zero or below (both out
   of `tsmom12`).
3. When the gate is open, DBC is eligible (a year of bars, so from about 2007-02) and DBC's own
   365-day return is positive: hold DBC at one slot, 1/n (the size of the SPY or TLT slot it
   stands in for). It is paid from cash, which the gate guarantees (at least two slots empty),
   so no leverage. Otherwise no DBC.

No parameter exists to tune: the gate, the trend window and the slot size are `tsmom12`'s.
Gym: six assets plus DBC, protocol costs (DBC is an ETF: 2 bps), T-bill interest on cash for
both books (step 1's accounting). Twin: `tsmom12` with cash on the six assets. Look-ahead and
identity check: on every day the gate is closed, the book's targets equal the twin's.

**Pass bar (all must hold).** Family: combo-1's 72 plus this pick = **73, p < 0.10 / 73 =
0.00137** (stricter if another lane has added picks to the family by the verdict).

1. Full-train Sharpe beats the twin, paired stationary bootstrap (block 20, 2,000 draws),
   one-sided p < 0.00137, **both** against 0 and above T-bills.
2. Eras: ahead of the twin in 2022-25 and not behind it (by more than 0.01) in any other era.
   (Changed from combo-1's "4 of 5": the rule equals the twin until DBC is eligible in 2007, so
   1994-99 and most of 2000-09 are ties by construction.)
3. Worst loss not more than 5 points deeper than the twin's.
4. Mechanism: excess over the twin positive in the gate's own weeks and in the map's
   "stock-bond corr > 0" regime.
5. Beats equal weight (six assets, with cash) on Sharpe.
6. Since 2003 not behind the twin and not behind equal weight.

No out-of-universe set has a stock, a bond and a commodity partner that is not DBC itself, so
combo-1's bar 4 has no honest version here; the long-history evidence below replaces it as a
description, not a bar.

**Also reported, not bars.** Weeks the gate was open and DBC held; 2022 (the calendar year and
the 2022 rate-shock window) for the book and the twin; the map's regimes (fast fall, turn,
chop, stock-bond +).

**1970s-style co-falls (description only, if the data reach).** DBC starts in 2006. For
1962-2005 the cache has US stocks (Fama-French market and T-bill, monthly) and the 10-year
Treasury yield (FRED DGS10, daily from 1962); a 10-year bond's monthly return is approximated
from the yield (carry plus duration times the yield change, duration from the yield, par
bond). The commodity side needs a long series: the S&P GSCI is not free, so the proxy is
FRED's producer price index for all commodities (PPIACO, keyless graph CSV), a spot price
index without roll yield or collateral (it is not what DBC earns). Gold (monthly, cache) as a
second proxy. Same gate monthly (12-month stock and bond returns both at or below zero), same
DBC trend condition on the proxy. Reported: months open, the proxy's mean return in them
(plain and trend-gated) against the T-bill. Nothing here can pass or fail the card.

**How the bar reads.** The gate is open rarely (a few episodes since 2007), so bar 1 is almost
out of reach by construction: a pass would need a large effect in few weeks. The honest
evidence is bar 4 and the 2022 rows. A pass makes a candidate for a separate held-out card,
nothing more.

**Tries.** One `variant` row (idea `combo-2`, `cofall-dbc`), counted in the family (73). The
twin with cash is already logged in step 1 (`tsmom12 cash`), not again.

## Step 2 result: `cofall-dbc` fails (2026-11-18)

Tables: [`results/combo-2-cofall.md`](results/combo-2-cofall.md) (`lib/combo2_cofall.py`, one
logged run, 22:27 UTC, 1 `variant` row) and
[`results/combo-2-longrun.md`](results/combo-2-longrun.md) (`lib/combo2_longrun.py`,
description, no row). Checks passed: the fast path equals `gym.backtest` on four gate days, and
on every day the gate is closed the book's targets equal the twin's.

**The partner arrived late and stayed too long. `cofall-dbc` 1.07 against `tsmom12` 1.08
(-0.006, p 0.85; above T-bills the same), behind in 2022-25 (0.92 against 0.97), negative in its
own weeks (-2.3% a year). It fails bars 1, 2, 4 and 6.**

| Gate spell (SPY and TLT both out of trend) | Days | DBC weeks | Book minus twin | DBC in the spell |
|---|---:|---:|---:|---:|
| 2016-01-08 .. 2016-02-11 | 35 | 0 | 0.0 pts | -3.7% |
| 2018-12-14 .. 2019-01-31 | 49 | 0 | 0.0 pts | +1.8% |
| 2022-04-29 .. 2022-05-26 | 28 | 4 | +1.0 pts | +4.1% |
| 2022-06-03 .. 2023-05-04 | 336 | 38 | -4.0 pts | -23.8% |

Calendar 2022: twin -11.2%, book -12.9%. 2022-25: -4.5 points.

**Why.** The gate needs two 12-month trends to turn, and the stock trend turned last (end of
April 2022). By then commodities had run for two years; DBC peaked in June 2022 and fell 24%
over the rest of the spell while its own 12-month trend, also slow, stayed positive into late
2022. Three slow signals in a row: the co-fall is visible only after most of it, and the partner
that won it is past its peak. In 2008 the gate never opened (Treasuries rose), so the case it
was built for is one episode in the gym's history, and it went the wrong way.

**1970s-style evidence (description, 1962-2025, monthly).** The monthly gate (US stocks and a
10-year Treasury both down over 12 months) was open in only 35 of 767 months, in 12 short
spells; in the 1970s only 15 months (1966, 1969-70, 1973-08, 1974-11): high coupons kept the
bond's 12-month return positive through most of the inflation. In those months: T-bills +5.4%
a year, the S&P GSCI price index -24.9% (from 1985; with collateral and its own trend, -17.9%),
gold -2.7% (pegged until 1971, so the 1960s rows say nothing). No proxy earned in the gate
months; the bill did. The data do not reach a broad commodity return for the 1970s (the GSCI
history in the cache starts in 1985; FRED's commodity price index could not be fetched).

**Reading.** By the trend gate, "stocks and bonds fall together" is rare and is seen late;
the partner that would have helped (commodities, 2021-22) did its work before the gate opened.
The T-bill, which `tsmom12` already holds there and which now earns interest (step 1), is the
best of the long-only options measured. Family count: 73 picks, none passes.
