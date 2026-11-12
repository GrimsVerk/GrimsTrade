# Idea lab (M2)

## Plain-language summary

Research run 1, night of 2026-11-12. **The clever maths lost to the simple rules, and the simple
rules do not earn more than holding everything: they lose less.**

- **Done:** about 150 papers read (`survey-2026-11.md`); 14 ideas written down with their pass
  mark fixed before testing; each tested on up to 32 years of prices and on markets it was not
  built on. 216 backtests, all logged.
- **None of the 13 with a pass mark passed** (the 14th only describes a choice). Kelly sizing,
  hidden Markov regimes, Hawkes processes and the rest each equal a simpler rule or lose to it.
  Two were real effects that faded once published.
- **What holds up:** a slow trend rule (hold an asset only while it is up over 12 months) earned
  about what holding everything earned since 1994 (17.8% a year against 18.2%) with a worst loss
  of 37% instead of 69%. The M1 lane already runs it. It is the rule to beat.
- **The real choice is how much risk.** Adding a volatility cap to that rule (`trend-vol`) takes
  the worst loss to 26% and growth to 13% a year. Worth a paper slot only if the owner wants the
  smaller losses; it is a risk setting, not an edge.
- **Luck check:** the best new rule beat "hold everything" by 0.22 Sharpe; luck alone across the
  21 versions tried would give about 0.20. No new rule has shown an edge.
- **Crypto:** trend rules did not beat simply holding Bitcoin or Ether, and still lost 70% at
  worst. The size of the crypto slot is the biggest risk setting there is: 5% per coin meant a
  worst loss of 31% since 2013, a sixth per coin 47% (`results/crypto-slot-size.md`).
- **Still clean:** the last 12 months of prices were never looked at, for any idea.
- **For the M1 lane:** the gym ignores dividends, which makes bonds look worthless (requests at
  the bottom). That it pays nothing on cash turned out to matter little (about 0.6% a year).

## Ranking after run 1

For forward paper trading (M3), best first. None passed the pre-set bar; the order is by what the
tests support.

1. `tsmom12` (12-month trend). Already M1's. Sharpe 1.05 against 0.88 for equal weight over
   1994-2025 (p = 0.08), worst loss 37% against 69%; holds on raw prices and at double costs
   (`results/robustness.md`). Keep it live: it is the bar.
2. `trend-vol` (trend with a volatility cap). Same Sharpe as `tsmom12`, worst loss 26%, growth
   13.3% a year against 17.8%. A paper slot only if the owner wants the low-drawdown profile.
3. `ensemble-tsmom` (trend at four horizons). +0.05 over `tsmom12`, right sign in every other
   market set, not significant. No separate slot; a possible revision of M1's rule later.
4. `sma200`, `drawdown-control`, `vol-target`, `trend-to-safe`: the same protection in other
   clothes. No slot.

Separate from the ranking, a decision for the owner: the size of the crypto slots
(`results/crypto-slot-size.md`). It moves the worst loss more than any rule above.

Dead, with the one-line reason (details in `ideas.md` and `results/`):

- `fracdiff-momentum`: a fast trend rule; worse than 12-month momentum everywhere.
- `hmm-regime`: beats a volatility switch, loses to the 200-day average; slept through 2000-2002.
- `kelly-shrunk`: the no-leverage cap turns it into inverse-volatility weights.
- `universal-portfolio`: 30 years is far too short for its guarantee; it stays where it starts.
- `hawkes-clustering`: daily crash clustering is too weak to trade.
- `absorption-ratio`: worked until its paper came out in 2010, not since.
- `month-end-liquidity`: real for decades (t of 3 to 4 on old indexes), faded since 2014.
- `dip-rsi2`: real but tiny (in the market 5% of the time) and halved since publication.
- Killed by reading alone: topological data analysis, transfer entropy, critical slowing down,
  change-point momentum, daily crypto reversal, pre-FOMC drift, return forecasts from
  time-series foundation models.

## Research run 1 (resume here)

Brief: `chief-of-staff/briefs/grimstrade-research-1.md`. Branch `research-1`, draft PR #4. Hard
stop 2026-11-12 08:40 UTC. Started 2026-11-11 23:05 UTC, cut off by the usage limit at about
23:15, resumed 01:32.

**Done**

- Harness, long price history, `protocol.md` (fixed before any test), baselines and twins.
- `survey-2026-11.md` (verdict per family, 165 source entries with links) from the six parts in
  `notes/survey-parts/`.
- Nine cards (committed before any test, 6ad40cc), then three more (e8197ba) and two more
  (8b46f31), each saying what had been seen by then. All fourteen tested and judged: `results/<idea>.md` each end
  with a dated verdict; `ideas.md` has every status.
- `results/robustness.md`: front-runners on raw prices and at double costs.
- `results/cash-interest.md`: what-if with T-bill interest on cash (adds 0.5-0.8% a year to the
  cautious rules, changes no ranking).
- `results/deflation.md`: the best edge seen against what luck alone would give (0.22 vs 0.20).
- `results/crypto-alone.md`: the plain and run-2 rules on BTC alone and ETH alone (trend does
  not beat holding there; it shrinks the winters; the size of the slot matters more).
- The summary and ranking above.

**Doing**

- Nothing half-finished: every file on the branch is complete as it stands.

**Next (a later run; nothing here is started)**

- Cards still in `ideas.md` under "New": `vol-shift`, `turbulence`. Write the card first, test with `lib/testkit.py`, `DRY=1` before the real
  run (a real run logs tries).
- The held-out year (2025-11-11 to 2026-11-09) has not been looked at for any idea. The harness
  allows one look per idea; spend it only on an idea that passes its train bar.
- If the M1 lane credits dividends or pays interest on cash, rerun `lib/baselines.py` and
  `lib/robustness.py`: rules that hold cash will look better than they do here.

## Layout

- `ideas.md`: one line per idea with status. Dead ideas stay.
- `survey-2026-11.md`: what the literature says held up or failed, with links.
- `cards/<idea>.md`: hypothesis card: claim, why, test, pass bar. Written before results.
- `protocol.md`: the test rules, fixed before any test.
- `tries.md`: every backtest variant ever run, train or held-out. Appended by the harness.
- `results/`: what each test showed, one file per idea, ending in a dated verdict.
- `lib/`: research scripts. `data/`: price caches (git-ignored).

## Requests to the M1 lane (code in `src/`)

- **Count the idea lab's tries in the deflated Sharpe.** `research/tries.md` has one row per
  backtest; the rows with kind `variant` (17 on the six assets so far, plus the timing rules run
  per asset) are the ones that could have been selected. `lib/deflation.py` shows one way to
  read them.
- **Credit dividends in the gym** (already in `docs/BACKLOG.md`; this makes it urgent). Raw TLT is
  0.99x over 2002-2025; with coupons it is 2.28x. SPY: 17x raw, 31x with dividends since 1993. The
  live scoreboard will understate every bond holder and flatter every rule that avoids bonds.
- **Pay interest on cash** (for example the 3-month T-bill rate), or add a cash-like ETF (BIL/SHV)
  to the universe. Smaller than it sounds: `results/cash-interest.md` puts it at 0.5-0.8% a year
  for rules that hold a quarter of the book in cash, with no change in ranking. Truthful
  accounting, low priority.
- `report.score` annualises with 365 days over the equity rows it gets. If a strategy's history
  ever holds no crypto, the gym reports only trading days and the Sharpe is overstated by about
  20% (sqrt(365/252)). Harmless today (crypto is always in the history); the research harness
  fills calendar days itself.
