# GSY 1: does a "Bubbles for Fama" run-up flag improve `tsmom12`?

Research lane gsy-1, 2026-11-18. Branch `gsy-1` (from `trend-1926`). Research only: fake money,
public data (Ken French library, cached Yahoo bars), no change to the gym, the daily runner or
the live strategies. Card, fixed before any number: `cards/gsy-runup.md`. Tables:
`results/gsy-1-replication.md` (step 2) and `results/gsy-1.md` (step 3). 36 rows in `tries.md`
(idea `gsy-runup`: 12 variant, 10 baseline, 14 robustness). Held-out year untouched.

## In plain words

**The warning is real; as an exit on top of the trend rule it adds almost nothing.** After an
industry doubles in two years (raw and net of the market), it crashes (falls 40% from a peak)
within two years 38% of the time against 15% for any industry-month (1928-2014, 49
industries), and 51% after a 150% rise. That is GSY's direction, at a lower level than their
53% / ~80%. But `tsmom12` already sits in cash on 88% of industry crash days (310 of 351 in
1928-2001), so the flag can add only a handful (5-12 more), and it pays with many false alarms.
Two variants pass the card's bar by its letter, by +0.03 Sharpe; out of GSY's era and on sector
ETFs the gain is not there. **Verdict: weak pass on the letter, no case for the live rule.**

## Step 2: replication (descriptive, `results/gsy-1-replication.md`)

| Data | Run-up | Episodes | Crash within 2 years | Base rate (any month) |
|---|---|---:|---:|---:|
| 49 industries, 1928-2014 (GSY's window) | 100% | 104 | 38% | 15% |
| same | 150% | 51 | 51% | 15% |
| 49 industries, 2002-2023 signals | 100% / 150% | 30 / 17 | 27% / 35% | 12% |
| 49 industries, 2015-2023 (outside GSY's sample) | 100% / 150% | 10 / 5 | 30% / 40% | 8% |
| 30 industries, 1928-2014 | 100% / 150% | 50 / 17 | 34% / 47% | 12% |

- By the card's test the setup "works": 38.5% is within 15 points of 53% (just), and 150% is
  above 100%. The level is lower than GSY's and our count of episodes is probably higher than
  theirs (their count was not relayed; we did not re-read the paper). 20 of our 104 are
  1933-1935 rebounds from the depression low, and only 2 of those crashed. A filter added after
  seeing the table (industries with at least 10 firms, which GSY may have used) gives 40% (53
  episodes) and 62% (21): nearer at 150%, not at 100%. Recorded as a re-reading, not the card's
  definition.
- The median return over the next 6 months is +3% after a 100% run-up and -6% after 150%: in
  our data the "keeps rising ~30% for six months" is not the typical case.
- Since 2002 the warning is weaker (27% at 100%), but so is the base rate (12%); the ratio
  stays about 2-3x.

## Step 3: the overlay (`results/gsy-1.md`)

The base is `tsmom12` on an equal-slot book of the 30 French industries (primary) or the 10
(robustness), daily, 2 bps a side, Friday decisions, through the unchanged gym. Each variant also
holds cash while the run-up flag is active (two years from the last run-up day), alone (`-cash`),
or only when the close is also below its 290-day mean (`-sma`) or volatility is rising (`-vol`).

| Variant | 30 ind. 1928-2001: dSharpe (p) | worst loss (`tsmom12` 39%) | 30 ind. 2002-2025: dSharpe (p) | 10 ind. 1928-2001 | ETF sectors 2000-2025 | Card |
|---|---:|---:|---:|---:|---:|---|
| flag100-cash | +0.043 (0.013) | 33% | +0.004 (0.46) | +0.027 | - | dead |
| flag150-cash | +0.020 (0.033) | 36% | +0.004 (0.45) | +0.005 | - | dead |
| flag100-sma | +0.027 (0.001) | 37% | +0.018 (0.20) | +0.012 | -0.04 | **passes (route S)** |
| flag150-sma | +0.012 (0.021) | 38% | +0.017 (0.18) | +0.003 | - | dead |
| flag100-vol | +0.030 (0.007) | 36% | +0.015 (0.26) | +0.017 | -0.02 | **passes (route S)** |
| flag150-vol | +0.011 (0.036) | 38% | +0.003 (0.45) | +0.001 | - | dead |

`tsmom12` itself: 0.98 Sharpe in 1928-2001 (equal weight 0.73, worst loss 82%), 0.73 in
2002-2025 (equal weight 0.62). Route S needed p < 0.0083 (0.10 over 12 tests) in discovery, a
positive difference after 2002, and a positive one on the 10-industry book. Route W (worst loss
5 points better in both periods) failed for every variant: after 2002 the book's worst loss
moves from 21% to 20% at best.

**What the plain verdicts mean.**

- `flag100-sma` and `flag100-vol` pass by the card's letter. The gain is about +0.03 Sharpe
  (1.01 against 0.98) and 2-3 points of worst loss in 1928-2001; after 2002 it is +0.02 and
  cannot be told from zero (p 0.20 and 0.26). The very small discovery p-values come from two
  books that differ on a few percent of days, so the bootstrap is tight around a tiny effect;
  small and steady, not large.
- On the four sector ETFs (2 flag episodes in 26 years) both are behind `tsmom12` (-0.04,
  -0.02). Too few events to count against them, but no support either.
- The `-cash` variants (the paper's "move to cash") gain in 1928-2001 although the rises they
  sit out add up to 1.9 and 6.0 log units of price (150% and 100%); after 2002 they are level
  with `tsmom12`.
- Mechanism: the flag adds 5-12 crashes avoided out of 351 (1928-2001) and 2-5 of 117
  (2002-2025). False alarms (no 40% crash within two years) are 37-64% of the overlay's
  spells, near what the replication's crash rate predicts. Only `flag100-cash` is out before
  the peak (median exit 24 days before it, against 58 days after for `tsmom12`); `-sma` and
  `-vol` leave at about the same point as `tsmom12` (they need the price to turn first, and
  then mostly duplicate the trend rule).

**How sure.**

- Overlap with GSY: discovery (1928-2001) is entirely inside their sample, and so is 2002-2014.
  Only 2015-2025 is outside it, and there the variants are +0.00 to +0.02.
- Disclosure: before the full run a `DRY=1` plumbing run printed the same table for only the
  last 500 days of each period (2000-2001 and 2024-2025). Nothing was changed after it; all six
  variants were run as fixed on the card.
- After the full run the script was run once more to print p-values to three decimals (the
  saved runs re-scored, no new rows) and, as the card fixed, to add the ETF set for the
  variants that passed.
- Crash counting restarts the peak after each crash, so a fall of 64% counts twice; the same for
  every rule.

## What it means

- For the live rule: nothing. The pass is +0.03 Sharpe on a 30-industry book, not seen after
  2002 or on sector ETFs. On the six live assets a 100%-in-two-years flag would fire mostly on
  BTC and ETH, where doubling is ordinary, so it is not even the same signal there.
- By the card, a pass makes a candidate for its own six-asset card under the default bar. The
  recommendation is not to spend one: the expected gain is below what that bar can detect.
- What is real and may be useful elsewhere: a run-up is a 2-3x higher chance of a 40% crash.
  That is a risk-description fact (for the owner's risk map or for sizing a concentrated
  position), not a timing edge on top of a trend filter.
