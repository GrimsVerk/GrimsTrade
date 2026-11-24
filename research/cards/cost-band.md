# cost-band: a cost-sized tolerance band for rebalancing `tsmom12`'s held slots

Lane wide-16, written 2026-11-24 (about 20:20 UTC), **before any return of the rule below was
computed**. Field: stochastic control with proportional costs (the no-trade region; Magill and
Constantinides 1976, Davis and Norman 1990; width by the cube-root law, Rogers 2001, Janecek
and Shreve 2004 `[memory]`), read through Shannon's demon (rebalancing a volatile slot pumps,
letting it drift lets winners run). Candidate C1 (+ B4) of `wide-16.md`, step 1.

## What was seen before this card (disclosed)

Step 1b of `wide-16.md` (`lib/wide16_ceiling.py`, baseline only, no rule): `tsmom12` replayed
with the gym's costs reproduces Sharpe 1.045. From 2015 its coin fills are 1.7 entries, 1.5
exits and **76 drift top-ups or trims a year**; the drift fills trade 1.06 x equity a year and
cost 0.38% (fee) + 0.05% (slip) of equity a year, against 0.22% for all entries and exits.
Ceilings (not tradable): all coin costs at zero gives +0.0103 Sharpe (paired SE 0.0017, z 6.0)
on 1994-2025; adding back only the drift fills' costs gives +0.0085 (SE 0.0008, z 10.0).
These numbers chose this rule over no rule; they do not set its band (the band is the
formula below, with constants fixed from the gym's fee table).

## Hypothesis

`tsmom12` re-balances every held slot to 1/n whenever it is one point of equity away (the
gym's 1% band). On coin slots (daily vol about 4%, so a 1/6 slot drifts about 0.7 points a
day) that is a top-up or trim every few days at about 0.85% a trade. A tolerance band sized by
the cost of a correction should keep almost all of the book's exposure and risk while paying a
fraction of those costs, and so raise Sharpe by close to the drift cost.

## Rule (frozen)

- Signal, slots and decision days: `tsmom12` unchanged (`c.weekly(c.slots(c.tsmom_signal))`:
  each Friday an eligible asset whose 365-day log return is above zero gets 1/n, n = eligible
  assets; weights repeated daily).
- The only change: the gym's rebalance band (`gym.simulate(band=...)`, "skip a trade smaller
  than this share of equity, except a full exit"). Entries and full exits always trade. A
  held slot is traded back to 1/n only once it is `b` of equity away. One band for every slot
  (the gym has one band; for ETF slots the wider band costs only tracking, their fee is 2 bps).
- **`band05` (primary)**: b = 0.05, the cube-root law's half-width for a coin slot,
  h = (3 lambda w^2 (1 - w)^2 / (2 gamma))^(1/3) with lambda = 0.0085 (the gym's zero-volume
  coin taker fee 0.80% + slip 0.05%), w = 1/6, gamma = 2: h = 0.0497, rounded to 0.05.
  (The theory trades back to the band's edge; the gym's weight interface can only trade back
  to the target, so this is the standard "tolerance band, reset to target" form. Stated, not
  tuned.)
- **`band02` (secondary)**: b = 0.02, one doubling of today's band: the smallest step, the
  least tracking error.
- No other band is run. The held-out year is not touched.

## Data, tests, costs

- Primary test: the six assets, decisions 1994-02-01 .. 2025-11-09, total-return prices,
  gym costs (`gym.COSTS`, Kraken tiers on coins, 2 bps on ETFs). No bar after 2025-11-10.
- Out of universe (already used by earlier lanes): `coin` (LTC, XRP, BCH, ETC, XLM, DASH,
  from 2017-08-18), where every slot is a coin. Both variants as `robustness` rows.
- Comparator: `tsmom12` (baseline, logged; re-scored with `log=False` on each set).

## Statistic and pass bar

- dSharpe = Sharpe(rule) - Sharpe(`tsmom12`), daily returns, 365 days, two cash conventions:
  (a) the protocol's (cash earns 0, what `tries.md` logs) and (b) idle cash earns the 13-week
  bill (`harness.bill_rates()`), Sharpe above the bill. (b) is required because a rule that
  holds different cash can win on (a) by convention alone (diversifier-1).
- SE: paired stationary bootstrap of the difference (2,000 draws, mean block 20 days, seed 0;
  `stats._stationary_indices`, as diversifier-1). z = dSharpe / SE.
- **Pass (train) = all of:** (1) the project bar, `research/register/BAR.md`: **z >= 4.69**
  on the primary test (N_eff 486; DSR 0.95; it implies Bonferroni p <= 1.0e-4, z 3.71) in
  **both** cash conventions; (2) dSharpe > 0 on `coin`; (3) max drawdown on the primary test
  not more than 1 point worse than `tsmom12` (it is meant to be the same book). Two variants
  are tried; each is judged on its own and the 2 tries go into the count (N moves by 2: the
  bar stays 4.69 to two decimals).
- Reported, not scored: per-era dSharpe, coin drift fills a year and their cost, turnover,
  the tracking error of the daily return difference, its correlation with `tsmom12`.

## Power (written before the run)

- The bar is reachable: removing the drift costs with no tracking error would give z about
  10 (step 1b). So this design, unlike a 40-placebo gate, can pass.
- What it takes. With a saving of a share s of the drift cost (dSharpe about 0.0085 s), the
  difference's SE must stay below 0.0085 s / 4.69 = 0.0018 s. With book vol about 16% and 31.8
  years, that is a tracking error of at most about **0.16 s % a year** averaged over the whole
  test (about 0.3 s % a year in the coin years).
- What to expect. A slot drifting inside +-b of its size with coin vol about 70% gives a
  tracking error of the order b/sqrt(3) x 70% per coin while held: about 1% a year at b =
  0.02 and 2% at b = 0.05 in the coin years, five to ten times what the bar allows. Expected
  z: about 0.5-1.5. **Expected outcome: fail.** The saving is real but small (at most +0.0085
  Sharpe); the drift it leaves is a short-horizon coin bet (winners kept, losers not topped
  up) whose noise is far larger than the fee it saves. A pass would need that drift bet itself
  to earn a high, steady return (coin short-term momentum), not the fee.
- Detectable edge at the expected SE (about 0.01-0.02 if the tracking error is 1-2% a year):
  +0.05 to +0.09 Sharpe at z 4.69; the plausible effect is +0.005 to +0.01.

## Look-ahead and checks

- The rule adds no signal code: its weights are `tsmom12`'s, so its decisions are identical to
  the logged baseline's (tested on synthetic bars: same weights; a bar planted after day k
  changes no decision up to k; the train loader never returns a bar after 2025-11-10).
- The gym's band semantics are tested on synthetic bars: a 1/2 slot that drifts 3 points is
  topped up at b = 0.01, untouched at b = 0.05; a full exit always trades.
- One dry run (`DRY=1`, last 120 days, nothing logged), then one real run.

## Disclosure added with the script (before the real run)

The dry run (`DRY=1`, the last 120 days of train, 2025-07..11, nothing logged) was meant to
print counts only, but the script's pass-bar lines printed that window's numbers: dSharpe z
-1.6 / -1.5 for `band05` / `band02` on the six, coin dSharpe +0.027 / +0.003. A 120-day window
says nothing about a 32-year test; nothing in the card was changed after seeing it.
