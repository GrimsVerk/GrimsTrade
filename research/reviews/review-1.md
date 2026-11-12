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

Taking out a rule's best stretch always hurts it. The point here is that it is the only such
stretch, and that it happened on a book the owner will never hold. The 2008 crisis is inside the
2003-2025 row: the trend rule lost 4% there against 20%, and gave that back in false alarms in
the years around it.

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

### 2. "Dead" mostly means "not proven": the pass bar rarely passes a real edge

**What the runs say.** Twenty ideas had a pass bar, none passed, all are listed as dead.

**What I found.** The bar is strict in the right direction and blunt in the other.

- A rule with no edge at all passes bars 1, 2 and 4 together about 4% of the time. So the lab is
  well protected against fooling itself, which is what the owner asked for.
- A rule with a real edge mostly fails too. Chance of passing those three bars, by simulation:

  | True Sharpe edge over the twin | Passes |
  |---:|---:|
  | 0 | 4% |
  | +0.10 | 24% |
  | +0.15 | 40% |
  | +0.20 | 57% |
  | +0.30 | 84% |

  Assumptions: the Sharpe difference to the twin is measured with a standard error of 0.115 over
  the 32 years (the typical value in the result tables), the five eras are independent, and the
  three out-of-universe sets have standard errors of 0.16, 0.18 and 0.10. An edge of +0.10 to
  +0.15 over the trend rule would be a very good find, and this bar would throw it out six to
  seven times in ten.
- `tsmom12` itself, tested as a card against equal weight, fails: it is ahead in 2 of 5 eras
  (`results/baselines.md`) where bar 2 asks for 4. The rule ranked first is "dead" by the lab's
  own bar.
- Two of the dead look better than the label once the two-asset years are set aside. Re-run,
  from 2003-09 (three assets or more):

  | Rule | Sharpe | Against `tsmom12` (p) | Against equal weight (p) | Worst loss | Growth a year |
  |---|---:|---:|---:|---:|---:|
  | equal weight | 1.18 | | | 47.0% | 24.4% |
  | `tsmom12` | 1.21 | | +0.03 (0.40) | 36.5% | 21.1% |
  | `sma200` | 1.21 | +0.00 (0.50) | +0.03 (0.40) | 31.0% | 20.1% |
  | `trend-vol` (tv40) | 1.24 | +0.03 (0.37) | +0.06 (0.34) | 22.0% | 14.2% |
  | `ensemble-tsmom` | 1.29 | +0.09 (0.13) | +0.12 (0.16) | 24.5% | 20.1% |
  | `drawdown-control` (d1.0) | 1.31 | +0.10 (0.10) | +0.13 (0.10) | 27.6% | 18.8% |

  None of this is proof: I looked at five rules in a window I chose after seeing finding 1. It
  does show the order among the trend-family rules is open, and that `tsmom12` is not the best
  of them on any measure in this window.

**What it changes.**

- "No new paper slot" is still the right call: a slot should need proof and nothing gave it.
- Read "dead" in `ideas.md` as "did not prove itself in a test that proves little either way".
  The list should not be used later as evidence that these ideas do not work.
- Which trend-family rule runs live (`tsmom12`, `ensemble-tsmom`, `drawdown-control`,
  `trend-vol`) is a choice of risk profile that the backtests cannot settle. The forward ledger
  can say more than another night of backtests.
