# Idea lab (M2)

## Plain-language summary

Research run 1, night of 2026-11-12. In one sentence: **the clever maths lost to the simple
rules, and the simple rules are only a little better than just holding everything.**

- **What was done.** About 150 papers and articles read in six families (`survey-2026-11.md`).
  Nine ideas written down as hypothesis cards, each with its rule and its pass mark fixed *before*
  any test. Each tested on up to 32 years of prices (63 for old stock indexes), then on markets
  it was not designed on (other funds, other coins, Japan, UK, Germany). 158 backtests, all logged.
- **Result: none of the nine passed.** Kelly sizing, hidden Markov regimes, fractional
  differencing, Hawkes crash clustering, the absorption ratio, Cover's universal portfolio,
  drawdown control, the month-end effect and dip buying: each either equals a simpler rule or
  loses to it. Two were real effects that faded after they were published. Nothing goes to paper
  trading from this run, and that is the honest answer, not a failure of the run.
- **What does hold up.** A slow trend rule (hold an asset only while it is above its 200-day
  average, or up over 12 months) earned about the same as holding everything since 1994 and lost
  about half as much in the bad years (worst loss 37-44% against 69%). The statistical evidence is
  thin (roughly 1 chance in 10 that it is luck) and it is weaker on other markets. The M1 lane
  already runs these rules; this run says they are the ones to beat.
- **One lead worth a card next time.** Sizing crypto by its volatility kept the same growth with
  half the swings on six other coins. Suggestive, not proven.
- **What to expect.** The best edge seen in 32 years is small, and published edges usually keep a
  quarter to a half of their backtest size. A realistic goal for the paper system is the
  benchmarks' return with smaller losses, not a higher return.
- **The untouched year.** The last 12 months of prices were never used. They are still available
  as a clean test for whatever run 2 proposes.
- **Two things the gym gets wrong** (requests to the M1 lane, below): it ignores dividends, which
  makes bonds look worthless, and cash earns nothing, which punishes every rule that steps aside.

## Ranking after run 1

Candidates for forward paper trading (M3), best first:

1. `tsmom12` and `sma200` (plain trend). Already M1's. Sharpe 1.05 and 1.01 against 0.88 for equal
   weight over 1994-2025, drawdown roughly halved. Keep them live; they are the bar.
2. `vol-target-crypto`: not tested as its own card yet. First card of run 2.
3. `vol-shift` and `drawdown-control`: smoother or cheaper versions of the same protection. Only
   worth a paper slot if run 2 shows they add something to trend.

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
- All six survey parts in `notes/survey-parts/`.
- Nine hypothesis cards, committed before any test (commit 6ad40cc); all nine tested and judged:
  `results/<idea>.md` each end with a dated verdict; `ideas.md` has every status.
- The summary and ranking above.

**Doing**

- `survey-2026-11.md`: compiling the six parts (verdict per family, key links). If this file is
  missing or stops mid-way, finish it from the "Verdict for this family" sections of the parts.

**Next (only if usage is left before the hard stop)**

- Run 2 cards, written before testing, in this order: `vol-target-crypto`, `vol-shift`,
  `ensemble-tsmom`, `hmm-switch-to-bonds`, `turbulence`, `fixed-btc-sleeve` (see `ideas.md`,
  section "New"). Note on the cards for the first two that their idea came out of run 1's train
  results. Test with `lib/testkit.py` exactly like run 1.
- The held-out year has not been looked at for any idea. Spend it only on an idea that passes.

## Layout

- `ideas.md`: one line per idea with status. Dead ideas stay.
- `survey-2026-11.md`: what the literature says held up or failed, with links.
- `cards/<idea>.md`: hypothesis card: claim, why, test, pass bar. Written before results.
- `protocol.md`: the test rules, fixed before any test.
- `tries.md`: every backtest variant ever run, train or held-out. Appended by the harness.
- `results/`: what each test showed.
- `lib/`: research scripts. `data/`: price caches (git-ignored).

## Requests to the M1 lane (code in `src/`)

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
