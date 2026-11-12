# Idea lab (M2)

## Plain-language summary

_Being written as the run goes; the final half-screen summary lands here before the hard stop._

Research run 1 started 2026-11-11 23:05 UTC (cut off by the usage limit at about 23:15, resumed
2026-11-12 01:32). Nothing is concluded yet.

## Research run 1 (resume here)

Brief: `chief-of-staff/briefs/grimstrade-research-1.md`. Branch `research-1`. Hard stop
2026-11-12 08:40 UTC.

**Done**

- Skeleton: `ideas.md`, `tries.md`, `cards/`, `lib/`, `results/`, git-ignored `data/`.
- Harness (`lib/harness.py`, `lib/common.py`, `lib/stats.py`): runs a strategy through the real
  gym, logs every try, refuses a second held-out look. Checked against `gym.backtest`.
- Long history in the cache (`lib/fetch.py`): SPY 1993, QQQ 1999, TLT 2002, GLD 2004, BTC 2012,
  ETH 2016, plus the out-of-universe sets (8 ETFs, 6 coins, 4 foreign/old indexes, 9 sectors).
- `protocol.md`: periods, eras, twins, out-of-universe sets and the pass bar, fixed before any
  test.
- Survey parts 3 (crypto, reversal, calendar) and 6 (exotic maths, econophysics, ecology) in
  `notes/survey-parts/`.

- All six survey parts in `notes/survey-parts/` (1 trend, 2 volatility/risk/Kelly, 3 crypto and
  calendar, 4 regimes/RMT/Hawkes/stopping, 5 overfitting and ML, 6 exotic maths).
- Nine hypothesis cards in `cards/`, committed before any test (commit 6ad40cc).
- `ideas.md`: every idea with its status.
- Baselines and plain twins on all universes: `results/baselines.md` (39 logged tries).

**Doing**

- Idea tests, one script per idea in `lib/` (`test_<idea>.py`), one result file per idea in
  `results/`. An idea is done when `results/<idea>.md` exists and its line in `ideas.md` no longer
  says `testing`. Check a script with `DRY=1` first (120 days, nothing logged), then run it once.

**Next**

- Compile the six survey parts into `survey-2026-11.md` (verdict per family, links).
- One held-out check per idea that passed train (the harness refuses a second look).
- Ranking in `ideas.md` and the plain-language summary at the top of this file.

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
