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

**Doing**

- Survey parts 1 (trend), 2 (volatility, risk, Kelly), 4 (regimes, RMT, Hawkes, stopping),
  5 (overfitting, ML): reading agents write `notes/survey-parts/<n>-*.md`. If a part is missing,
  rerun its reader; then compile all six into `survey-2026-11.md`.
- Hypothesis cards in `cards/` (written and committed before any result is looked at).

**Next**

- Baselines and twins on the full history (`lib/baselines.py`, results in `results/`).
- Train-period tests of the cards, strongest first; one held-out check per idea that passes.
- Ranking in `ideas.md` and the summary above.

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
