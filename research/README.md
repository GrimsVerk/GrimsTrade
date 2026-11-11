# Idea lab (M2)

## Plain-language summary

_Being written as the run goes; the final half-screen summary lands here before the hard stop._

Research run 1 started 2026-11-11 23:05 UTC. Nothing is concluded yet.

## Research run 1 (resume here)

Brief: `chief-of-staff/briefs/grimstrade-research-1.md`. Branch `research-1`. Hard stop
2026-11-12 08:40 UTC.

**Done**

- Skeleton: `ideas.md`, `tries.md`, `cards/`, `lib/`, `results/`, git-ignored `data/`.

**Doing**

- Literature survey (reading agents write `notes/survey-parts/*.md`; compiled into
  `survey-2026-11.md`).
- Price history cache and test harness (`lib/`).

**Next**

- Hypothesis cards (committed before any result is looked at).
- Train-period tests of the strongest cards; one held-out check per idea.
- Ranking and the summary above.

## Layout

- `ideas.md`: one line per idea with status. Dead ideas stay.
- `survey-2026-11.md`: what the literature says held up or failed, with links.
- `cards/<idea>.md`: hypothesis card: claim, why, test, pass bar. Written before results.
- `tries.md`: every backtest variant ever run, train or held-out. Appended by the harness.
- `results/`: what each test showed.
- `lib/`: research scripts. `data/`: price caches (git-ignored).

## Requests to the M1 lane (code in `src/`)

_None yet._
