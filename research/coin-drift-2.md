# coin-drift-2: wide-16's `band05@coin`, unchanged, on six coins and years it never saw

Research lane coin-drift-2, 2026-11-25 (UTC). Branch `coin-drift-2` (from `main`), PR #190.
Research only: fake money, cached keyless data, no change to the gym, the daily runner or the
live strategies. Train only: no bar after 2019-03-31 enters the book; the held-out year is
unread. Card: [`cards/coin-drift-2.md`](cards/coin-drift-2.md) (commit 552d0c5, 01:14 UTC,
before any number). Tables: [`results/coin-drift-2.md`](results/coin-drift-2.md)
(`uv run python -I research/lib/coindrift2.py --log`; tests `tests/test_coindrift2.py`).

Project-wide bar (`register/BAR.md`): **N_eff 506, z >= 4.70 against `tsmom12` on the primary
test.** This lane cannot make a pick; its own bar for "a real small effect" was z >= 2.5.

## Question

`coin-drift-run` is wide-16's post-hoc reading of `cost-band`: a 0.05 rebalance band beat the
gym's 0.01 (+0.049 Sharpe, z 2.76) because held coin slots were left to run in the 2017 and
2020-21 rallies (+0.054 with coin fills free). coin-drift-1 found no support on ~90 coins from
2019-04 (+0.033, z 1.80, no better than no-trend placebos). Does the rule, unchanged, help on
multi-coin data that neither test traded?

## Which data was unseen (the card's search)

BTC before 2012 and ETH before 2016-05 are one-coin windows (no drift between slots); wide-16's
six other coins before 2017-08 overlap the chosen book's years and were held back as a possible
second test. What is left is the coins other than BTC, ETH and those six, **before 2019-04**
(coin-drift-1's first return day is 2019-04-07). The card took wide-16's own set rule ("large
caps of January 2018"): the six largest eligible coins in breadth-1's book A on 2018-01-01
without BTC, ETH, wide-16's six and USDT: **XEM, XMR, ZEC, DOGE, DCR, REP**. Coin Metrics
prices, bars cut after 2019-03-31, returns 2015-01-25 .. 2019-03-31 (4.2 years). The rule is
`tsmom12` through the gym with band 0.05 against band 0.01, gym costs: wide-16's `run_set("coin")`
on other coins.

## Result: killed by the card

| `band05` minus `tsmom12` (band 0.01) | dSharpe | SE | z |
|---|---:|---:|---:|
| net, cash 0 (**scored**) | **-0.014** | 0.028 | **-0.50** |
| net, idle cash at bills (reported) | +0.011 | 0.028 | +0.40 |
| coin fills free in both (the drift part) | **-0.019** | 0.028 | -0.69 |

| Window | `tsmom12` Sharpe | dSharpe net | dSharpe, fills free |
|---|---:|---:|---:|
| 2015 | -0.59 | -0.010 | -0.031 |
| 2016 | 2.81 | -0.065 | -0.081 |
| 2017 | 4.21 | -0.068 | -0.068 |
| 2018 | -0.82 | +0.049 | +0.044 |
| after the pick (2018-01-01 ..) | -0.74 | +0.044 | +0.039 |

- **Reading (card): z < 1 and dSharpe < 0, so `coin-drift-run` is killed.** On the only
  multi-coin history neither wide-16 nor coin-drift-1 traded, the wide band is slightly worse.
- **The story fails where it should be strongest.** In the 2016 and 2017 coin rallies (book
  Sharpe 2.8 and 4.2) letting slots drift *lost* 0.07 a year, with or without costs; the small
  gain is in the 2018 bust. That is the reverse of wide-16's post-hoc reading (gain in the
  rallies).
- **Fees are saved and do not help.** `band05` trades 53 coin fills a year instead of 404 and
  pays 1.5% + 0.2% slip of equity a year instead of 2.35% + 0.4%. Fees and tiers add about
  +0.005 Sharpe; the drift part itself is -0.019, so the net is -0.014.
- **Noise.** Tracking error of the pair 6.7% a year (corr 0.9976), SE 0.028: the test could
  see about +0.07 at z 2.5, as the card said (it expected "not confirmed"). The point estimate
  is below zero, so the result is not just "underpowered": a drift premium of wide-16's size
  (+0.054 costs free) sits 2.6 SE above the -0.019 measured here (a loose comparison: other
  coins and slot counts).
- The above-bills line is positive while cash 0 is negative: with a 0.05 band the trade dates
  depend on the account's path, and a little interest on idle cash moves them. That the sign
  flips on so small a change says the same as the SE: there is no stable effect here.
- Both books: Sharpe 1.93 / 1.92, growth 284% / 268% a year, worst loss 77.5% / 75.0% (a
  thinly traded book in the 2015-18 coin boom and bust; one or two coins until 2016-04).
- **Survivorship.** For 2015-2017 the coins were picked by their January 2018 cap, which is
  look-ahead in the universe. It inflates both books' Sharpe (1.93) and, if anything, favours
  `band05` (winners drift up), so the kill is conservative.
- **The only look-ahead-free slice** (2018-01-01 on, 453 days, mostly a bust spent in cash) is
  dSharpe +0.044 net / +0.039 costs-free, with no SE: too short to read, and not a reason to
  revive the idea.

## What it means

- `coin-drift-run` (`ideas.md`): **dead.** Two tests on data that did not suggest it: ~90 coins
  2019-25 (+0.033, z 1.80, all of it fewer trades) and six coins 2015-19 (-0.014, z -0.50, the
  drift part negative, worst in the rallies). wide-16's +0.049 on the six assets stays a
  post-hoc observation of two BTC/ETH runs with no mechanism behind it.
- No case for changing the gym's 0.01 band or the live books.
- Not run, and now not worth running: wide-16's six coins before 2017-08 (same years as this
  book, thinner still).

## Changes after the card (disclosed)

- None to the rule, data or bars. The card said returns "to the last bar - 1 day (2019-03-30)";
  that is the last decision day (`end`), and the account's returns run to the last bar,
  2019-03-31, as in wide-16 (the `tries.md` rows show `To` 2019-03-30 for the two books and
  2019-03-31 for the note).
- The per-year table has no 2019 row: both books held only cash in 2019-01 .. 03 (all six
  coins below their 365-day price), so the script skips a window with no variance.

- After the logged run the pure parts (coin pick, bar builder) moved to
  `lib/coindrift2_core.py`, because importing `harness` from a test registered research
  symbols and broke five daily-runner tests in the full suite. The script was rerun once
  without logging: `results/coin-drift-2.md` is byte-identical.

## Rows in `tries.md` (idea `coin-drift-run`)

`tsmom12@cd2` (`baseline`), `band05@cd2` (`robustness`), one `note` row (the costs-free and
bills readings and the verdict).
