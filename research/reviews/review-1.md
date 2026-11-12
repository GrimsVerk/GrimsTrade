# Review 1 of research runs 1 and 2

Reviewer: an agent that wrote none of the code. Branch `review-1`, made from `research-2` at
`0343bcb`. Written 2026-11-12, 06:50 to 08:30 UTC. Status: **in progress**; the verdict below is
provisional until this line says final.

## Verdict (provisional)

Being written. First finding is below; the verdict is filled in as the checks finish.

## How the review was done

- All prices fetched again from the public sources with `lib/fetch.py` (2026-11-12 06:50 UTC),
  into this worktree's own git-ignored cache. Nothing was copied from the research worktree.
- Every number below marked "re-run" comes from scripts I wrote against `lib/harness.py` with
  `log=False`, so `tries.md` is untouched. No held-out backtest was run.
- Nothing in the repo was changed except this file.

## Findings, ranked by impact

### 1. The trend rule's lead over "hold everything" is one episode on a two-asset book

**What the runs say.** `tsmom12` has Sharpe 1.05 against 0.88 for equal weight over 1994-2025
(p = 0.08), with a worst loss of 37% instead of 69%. That is the bar every idea was measured
against, and the reason the README ranks `tsmom12` first.

**What I found.** The numbers reproduce exactly on my own fetch (1.05, 0.88, p = 0.07 to 0.08,
36.5% and 68.8%). But the lead comes entirely from the dot-com bust, and in those years the
"six-asset" book held two assets. An asset joins the book after a year of bars, so the book is:

| From | Assets in the book |
|---|---|
| 1994-02 | SPY |
| 2000-03 | SPY, QQQ (QQQ joins in the month of the Nasdaq peak) |
| 2003-07 | SPY, QQQ, TLT |
| 2005-11 | SPY, QQQ, TLT, GLD |
| 2013-01 | the four ETFs and BTC |
| 2017-05 | all six |

Equal weight's 69% loss is a half-SPY, half-QQQ book in 2000-2002. No six-asset book ever lost
that. Re-run, same harness, same costs, total-return prices:

| Window | `tsmom12` Sharpe | Equal weight Sharpe | Difference (p) | Worst loss, trend / equal | Growth a year, trend / equal |
|---|---:|---:|---:|---:|---:|
| 1994-2025, as in the runs | 1.05 | 0.88 | +0.17 (0.08) | 36.5% / 68.8% | 17.8% / 18.2% |
| The same without the dot-com bust (2000-03-24 to 2002-10-09 removed) | 1.21 | 1.22 | -0.01 (0.56) | | 20.8% / 24.8% |
| 2003-2025 | 1.20 | 1.19 | +0.00 (0.49) | 36.5% / 47.0% | 20.7% / 24.9% |
| 2010-2025 | 1.34 | 1.30 | +0.04 (0.40) | 36.5% / 47.0% | 27.4% / 31.1% |
| 2017-06 to 2025 (all six assets held) | 1.15 | 1.12 | +0.03 (0.45) | 36.5% / 47.0% | 26.5% / 31.5% |

Asset by asset, each over its own history, the trend rule against holding that asset: SPY +0.09
(p = 0.27), QQQ +0.11 (p = 0.21), GLD -0.08, TLT -0.06, BTC +0.01, ETH -0.02. It helped on
stocks, through two long bear markets, and nowhere else.

The rule itself is not fragile in the usual ways: any decision weekday gives 1.04 to 1.05, and
lookbacks of 9 to 12 months give 1.03 to 1.13. Lookbacks of 15 months and more give 0.82 to
0.89, no better than equal weight.

**What it changes.**

- "Nothing beat `tsmom12`" stays true. But `tsmom12` has not beaten holding everything on any
  book that looks like the live one. The honest headline is: nothing, the trend rule included,
  has shown an edge over equal weight since the book had more than two assets.
- What the trend rule does deliver since 2003 is a smaller worst loss (37% against 47%) paid for
  with about 4 to 5 points of growth a year. That is the same trade the README already describes
  for `trend-vol`; it is a choice about risk, not evidence of skill.
- The live scoreboard should not be expected to show `tsmom12` ahead of equal weight on Sharpe.
  If it does not, that is the backtest's own forecast, not a failure.
- Later tests should report the window from 2003 (or from 2005, four assets) next to 1994-2025,
  and judge against equal weight as well as `tsmom12`. Every "difference to equal weight" in
  `results/deflation.md` carries the same dot-com episode.
