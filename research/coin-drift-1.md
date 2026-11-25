# coin-drift-1: letting held coin slots drift, checked on ~90 other coins

Research lane coin-drift-1, 2026-11-24. Branch `coin-drift-1` (from `main`), draft PR #157.
Research only: fake money, cached data, no change to the gym, the daily runner or the live
strategies. Train only: no bar after 2025-11-10 was loaded; the held-out year is unread.
Card: [`cards/coin-drift-run.md`](cards/coin-drift-run.md) (commit d8613f5, 20:24 UTC, before
any number). Tables: [`results/coin-drift-run.md`](results/coin-drift-run.md)
(`uv run python -I research/lib/coindrift1.py`; core `lib/coindrift1_core.py`, tests
`tests/test_coindrift1.py`).

Project-wide bar (`register/BAR.md`): **N_eff 486, z >= 4.69 against `tsmom12` on the primary
test.** This lane is a mechanism check (bar z >= 2 on a coin book the live strategies do not
trade), not a pick, and cannot make one.

## Question

wide-16 (#145) found after the fact that widening the gym's rebalance band from 0.01 to 0.05
helped `tsmom12` (+0.049 Sharpe, z 2.76) not through fees but because held coin slots were left
to run above 1/n in the 2017 and 2020-21 rallies (+0.054 with coin fills free). That was seen
on BTC and ETH, the data that suggested it. Does the same band, frozen, earn the same kind of
gain on cointop-1's coin book (about 90 coins a week, with BTC, ETH and wide-16's six other
coins removed), and is it more than what a book with no trend to ride would earn from trading
less?

## Design (from the card)

- cointop-1's selection set and twin: each Friday a universe coin with a positive 365-day
  return gets 1/(coins in the universe), the rest cash; 292 coins pass through the universe,
  median 92 a week; returns 2019-04-07 .. 2025-11-10 (6.6 years).
- Traded daily as the gym trades, with the gym's costs (Kraken taker tiers on the book's 30-day
  coin volume, 0.05% slip, 10,000 USD start). The band is carried as a share of the slot, as it
  acted on wide-16's 1/6 coin slot (a 1.1% slot cannot take a 0.05-of-equity band: the gym would
  never buy it): `k06` (0.01 x 6, the comparator), `band02` (k 0.12), `band05` (k 0.30,
  primary).
- Placebos, 40 shuffles each, same code: **P1** shuffles coins' returns across coins in 7-day
  blocks (keeps each day's cross-section, so the coin market's own trend stays); **P2** does the
  same to returns net of the market and also puts the market's weeks in a random order (no
  trend anywhere).
- Pass: M1 z >= 2 net of costs in both cash conventions; M2 excess over P1 z >= 2. M2b (excess
  over P2) decides the reading if M2 fails.

## Result: the mechanism is not confirmed

| `band05` against `k06` (cash 0 unless stated) | dSharpe | SE | z |
|---|---:|---:|---:|
| net of costs (M1) | +0.033 | 0.018 | **1.80** |
| net, above bills (M1) | +0.032 | 0.018 | 1.78 |
| all coin costs zero (the drift part) | +0.014 | 0.019 | 0.71 |
| excess over P1 (M2) | +0.009 | 0.010 | **0.83** |
| excess over P2 (M2b) | +0.009 | 0.017 | 0.54 |

| `band02` against `k06` | dSharpe | SE | z |
|---|---:|---:|---:|
| net of costs (M1) | +0.011 | 0.004 | **2.45** |
| net, above bills | +0.010 | 0.004 | 2.42 |
| all coin costs zero | +0.005 | 0.005 | 1.08 |
| excess over P1 (M2) | +0.002 | 0.003 | **0.62** |
| excess over P2 (M2b) | -0.001 | 0.004 | -0.35 |

- **`band05` fails M1** (z 1.80 < 2) and is no better than its placebos: on books with no coin
  trend of their own (P1) the same band gains +0.024 on average (SD 0.009, 5% quantile
  +0.010, lowest +0.002), and with no trend at all (P2) +0.024 too. The real +0.033 ranks 6th of 41 in
  P1 (p 0.15) and 13th of 41 in P2 (p 0.32). **Reading: not confirmed.**
- **`band02` passes M1** (z 2.45) **but is entirely a placebo effect**: P1 gains +0.009, P2
  +0.012, against the real +0.011 (rank 13 and 24 of 41). **Reading: fewer trades, not
  drift.**
- **Where the net gain comes from.** About 60% of `band05`'s +0.033 is fees: the wide band trades
  5.0 x equity a year instead of 7.6 and pays 2.3% + 0.25% slip instead of 3.05% + 0.38%, even
  though the dearer tier raises the fee per traded dollar from 0.40% to 0.46% (the same tier
  effect wide-16 saw). The rest (+0.014 with costs at zero) is not distinguishable from zero,
  and the placebos show that trading a ~90-slot coin book less pays about +0.02 Sharpe whether
  or not any coin trends (fees saved, minus a slightly more concentrated book).
- **By year** (`band05` minus `k06`, net / costs zero): 2019 +0.06 / +0.04, 2020 +0.08 / +0.02,
  2021 +0.08 / +0.06, 2022 -0.03 / -0.06, 2023-25 near 0. What drift gain there is sits in the
  2020-21 run, the same episode that carried wide-16, and is partly given back in 2022.
- Other numbers: tracking error of the pair 3.9% a year (corr 0.9991), higher than the card's
  1-3% guess, which is why the SE (0.018) sits at the top of the card's 0.01-0.03 range. Coin
  share while held 0.475 against 0.495; worst loss 60.6% against 63.9%.

## Power, after the fact

The test could see an effect of about +0.036 at z 2 (SE 0.018). The drift part measured here
is +0.014 (95% about -0.02 .. +0.05); wide-16's +0.054 on BTC and ETH sits about 2 SE above it
(a loose comparison: different books and slot sizes). And the book holds about three coin
bull episodes, two of them the same years as wide-16's. So this is **not confirmed**, not
**disproven**: a small own-coin drift premium (+0.01 to +0.02 Sharpe on a coin book) is
compatible with these numbers; one as large as wide-16's post-hoc +0.054 is unlikely.

## What it means

- **For `coin-drift-run`** (`ideas.md`): the only independent coin history found no support
  for the story. On ~90 coins the gain from a wide band is what a no-trend book also earns,
  mostly fees; the drift part is +0.014, z 0.7. wide-16's six-asset number stays what it was,
  a post-hoc observation in two bull runs, now without the mechanism it was explained by.
  Status: **not confirmed (tested)**. A further test would need new episodes (the forward paper
  trail) and would be underpowered for years.
- **For the live band** (the gym's 0.01): no change. `cost-band` failed the project bar on the
  primary test (z 2.76 against 4.69), and this lane removes the one reason to think its gain
  would repeat. The fee saving a wide band brings is real on a book that is all coins (here
  about +0.02 Sharpe), but on the live six-asset books wide-16 measured fees and tiers at about
  zero (-0.005), because fewer fills mean a dearer tier.

## Changes after the card (disclosed)

- **The first real run read no bill rates.** This worktree had no `research/data/bars/IRX.csv`
  (a gitignored cache), so `harness.bill_rates()` returned nothing and the above-bills column
  equalled cash 0. The cache file was copied from another checkout (the same Yahoo `^IRX`
  series; `bill_rates` reads train sessions only), the script now asserts the series is not
  empty, and it was rerun once without logging. Only the above-bills column changed (`band05`
  z 1.80 -> 1.78, `band02` 2.45 -> 2.42); every other number is identical. The tries rows come
  from the first run and do not contain the bills reading.
- The card said one `control` row per placebo kind and band would be "the mean of the 40
  shuffles"; a mean of 40 accounts has no single return path, so each row is the upper-median
  shuffle by Sharpe (index 20 of 40), with the 40-shuffle mean Sharpe in the Variant text.
- The look-ahead test of the placebo prices covers P1 only: P2 moves whole weeks of the market
  in time by design. Its rule still reads only placebo prices before each decision (tested on
  `trend_up` for any price matrix).
- The rows' `To` is 2025-11-10, the last train bar (the day the last return is earned), not the
  last decision 2025-11-09. Turnover/yr in these rows is traded value over equity a year (both
  sides), not weight changes.
- The card was written "about 20:30 UTC"; its commit is 20:24 UTC.

## Rows in `tries.md` (idea `coin-drift-run`)

`k06@cm` (`baseline`); `band05@cm`, `band02@cm` (`robustness`); six `control` rows (P1 and P2
at each band); one `note` row (the costs-at-zero split and the placebo excesses). None is
selectable except the baseline, a benchmark.
