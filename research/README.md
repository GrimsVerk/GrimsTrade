# Idea lab (M2)

## Plain-language summary

Research run 1, night of 2026-11-12. In one sentence: **the clever maths lost to the simple
rules, and the simple rules do not earn more than holding everything; they lose less.**

- **What was done.** About 150 papers and articles read in six families (`survey-2026-11.md`).
  Twelve ideas written down as hypothesis cards, each with its rule and its pass mark fixed
  *before* its test. Each tested on up to 32 years of prices (63 for old stock indexes), then on
  markets it was not designed on (other funds, other coins, Japan, UK, Germany). 199 backtests,
  every one logged in `tries.md`.
- **Result: none of the twelve passed its mark.** Kelly sizing, hidden Markov regimes,
  fractional differencing, Hawkes crash clustering, the absorption ratio, Cover's universal
  portfolio, drawdown control, the month-end effect, dip buying: each equals a simpler rule or
  loses to it. Two were real effects that faded after they were published. That is the honest
  answer, not a failure of the run: it tells us where not to spend the next months.
- **What does hold up.** A slow trend rule (hold an asset only while its 12-month return is
  positive) earned about what holding everything earned since 1994 (17.8% a year against 18.2%)
  and its worst loss was 37% instead of 69%. The evidence is thin (about 1 chance in 10 that it
  is luck) and weaker on other markets. The M1 lane already runs this rule; it is the one to beat.
- **The real choice is how much risk, not which trick.** Holding everything, trend, and trend
  with a volatility cap give roughly the same return per unit of risk. They differ in the size of
  the ride: worst loss 69%, 37% and 26%; growth 18%, 18% and 13% a year. If the owner's limit is
  the worst loss, the third (`trend-vol`) is worth a paper slot. It did not pass as an "edge" and
  is not labelled one.
- **How much could be luck.** Of the 17 rule versions that could have been picked, the best beat
  "hold everything" by 0.22 Sharpe. If none of them had any edge, the best would still be
  expected to show about 0.19 (`results/deflation.md`). So no new rule here has shown an edge.
- **What to expect.** Published edges usually keep a quarter to a half of their backtest size. A
  realistic goal for the paper system is the benchmarks' return with much smaller losses.
- **The untouched year.** The last 12 months of prices were never used, for any idea. They are
  still a clean test for whatever comes next.
- **Two things the gym gets wrong** (requests to the M1 lane, below): it ignores dividends, which
  makes bonds look worthless, and cash earns nothing, which punishes every rule that steps aside.

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
4. `sma200`, `drawdown-control`, `vol-target`: the same protection in other clothes. No slot.

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
- Nine cards (committed before any test, 6ad40cc), then three more (e8197ba, after the first
  nine; each says what had been seen). All twelve tested and judged: `results/<idea>.md` each end
  with a dated verdict; `ideas.md` has every status.
- `results/robustness.md`: front-runners on raw prices and at double costs.
- `results/deflation.md`: the best edge seen against what luck alone would give (0.22 vs 0.19).
- The summary and ranking above.

**Doing**

- Nothing half-finished: every file on the branch is complete as it stands.

**Next (a later run; nothing here is started)**

- Cards still in `ideas.md` under "New": `vol-shift`, `hmm-switch-to-bonds`, `turbulence`,
  `fixed-btc-sleeve`. Write the card first, test with `lib/testkit.py`, `DRY=1` before the real
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
  to the universe. With cash at 0, rules that step aside are punished and "always invested" wins by
  construction when rates are high.
- `report.score` annualises with 365 days over the equity rows it gets. If a strategy's history
  ever holds no crypto, the gym reports only trading days and the Sharpe is overstated by about
  20% (sqrt(365/252)). Harmless today (crypto is always in the history); the research harness
  fills calendar days itself.
