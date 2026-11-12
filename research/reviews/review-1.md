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
stocks, through two long bear markets, and nowhere else. The eight other ETFs in
`results/baselines.md` tell the same story: ahead in 2000-09 (0.81 against 0.41), level or
behind in two of the three eras since.

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
  | `kelly-shrunk` (k0.1, not the card's main setting) | 1.36 | +0.15 (0.23) | +0.18 (0.10) | 29.4% | 14.0% |

  None of this is proof: these are the five rules I looked at, in a window I chose after seeing
  finding 1. It does show the order among the cautious rules is open. In this window `tsmom12`
  has the lowest Sharpe and the largest worst loss of them, and the highest growth.

**What it changes.**

- "No new paper slot" is still the right call: a slot should need proof and nothing gave it.
- Read "dead" in `ideas.md` as "did not prove itself in a test that proves little either way".
  The list should not be used later as evidence that these ideas do not work.
- Which trend-family rule runs live (`tsmom12`, `ensemble-tsmom`, `drawdown-control`,
  `trend-vol`) is a choice of risk profile that the backtests cannot settle. The forward ledger
  can say more than another night of backtests.

### 3. Machine learning: "no skill found" holds; the Sharpe comparison says little

**What the runs say.** Every model lost to the trend rule (0.67 to 0.94 against 1.05); their
forecasts are a coin toss (AUC 0.48 to 0.51); a planted signal is found, so the test works.

**What I found.**

- The numbers reproduce. Re-run unlogged: `ml-linear/logit` 0.89, `ml-gbm/gbm` 0.81,
  `ml-sizing/gbm-low` 0.80; AUC 0.494 and 0.509 against 0.522 for the 12-month flag alone. All
  as reported.
- No look-ahead in the code as I read it: features come from the bars visible at the decision,
  labels from bars 28 days later, and a fit on day F uses only rows decided 35 days or more
  before F. The earlier code review checked the same by scrambling later bars.
- The gap to the trend rule is the dot-com bust again:

  | Model | Against `tsmom12`, 1994-2025 | Without the dot-com bust | From 2003-09 (p) |
  |---|---:|---:|---:|
  | `logit` | -0.16 | +0.01 | -0.03 (0.59) |
  | `gbm` | -0.24 | -0.12 | -0.10 (0.70) |
  | `gbm-low` | -0.25 | -0.11 | -0.08 (0.64) |

  In the bust the models were 79% (`logit`) and 52% (`gbm`) invested, the trend rule 26%. They
  had been trained on the S&P 500 of 1962 to 1999, where the trend rule did not beat holding
  (0.45 against 0.49 in `results/baselines.md`), so there was nothing to learn it from.
- The trend flag's own forecast skill sits in the early years: AUC 0.61 on the 593 forecasts
  before 2003 (SPY and QQQ only), 0.51 on the 5,621 since. The README's "the only signal in
  the features is the weak trend effect" is, since 2003, hardly a signal.
- The Sharpe bars could not have been passed. By the runs' own control
  (`results/ml-control.md`), a planted signal with a true correlation of about 0.12 with next
  month's return, as strong as the best published forecasts, ends at 0.80 to 0.90 Sharpe: no
  better than equal weight. So the Sharpe tables cannot tell "no signal" from "a real, ordinary
  signal". The result file says this; the README summary only half says it.
- That leaves the AUC. With about 1,500 independent asset-months its standard error is about
  0.015, so 0.49 to 0.51 is consistent with no skill and also with the trend flag's 0.52.

**What it changes.**

- "No ML slot" stands. No model showed skill, in any window.
- Read "coin toss" as: on 15 price features and six assets no skill could be seen, by a test
  that could only have seen a very large one. Run 2 is not evidence that ML cannot help with
  other information or a wider book. The README's own "Next" says the same; the plain-language
  summary should too.

### 4. The held-out year was not used for any test, but it was looked at

**What the runs say.** "The last 12 months of prices were never looked at, for any idea."

**What I found.**

- No held-out backtest was run. `tries.md` has no `heldout` row, and every backtest path loads
  prices through `load_history("train")`, which drops bars after 2025-11-10.
- But two figures in the repo were computed on the whole cache, held-out year included.
  `protocol.md` (Data) and the README (requests to the M1 lane) give TLT as "0.99x raw, 2.28x
  with coupons over 2002-2025" and SPY as "17x raw, 31x with dividends since 1993". On my fetch:

  | | Raw | With dividends |
  |---|---:|---:|
  | TLT, first bar to the train cut (2025-11-10) | 1.10x | 2.43x |
  | TLT, first bar to the end of the cache (2026-11-11) | 0.99x | 2.29x |
  | SPY, first bar to the train cut | 15.5x | 28.0x |
  | SPY, first bar to the end of the cache | 17.3x | 31.6x |

  The quoted figures are the full-cache ones. Anyone who reads them next to the train-period
  tables can work out that over the held-out year SPY rose about 11% and TLT fell about 10%.
  They are also mislabelled: they run to November 2026, not 2025.
- `protocol.md` already discloses one whole-cache print (the largest one-day moves, two of them
  in the held-out year). This is a second, undisclosed one, from the same early session.
- `idea_month_end_liquidity.py` reads every bar date in the cache, held-out year included, to
  count trading days to month end. Dates only, no prices; it does not matter for the result.
- To confirm the above I computed the same four ratios on the full cache. That is the only
  held-out number I looked at.

**What it changes.**

- No train result is affected.
- "Never looked at" is too strong. Whoever spends the held-out year should know that the
  direction of two of the six assets in it is written in the repo. The held-out pass mark
  ("not behind its twin") was weak before this; treat the forward paper ledger as the only
  clean test.
- The two figures should be recomputed to the train cut when the research files are next
  edited (TLT 1.10x and 2.43x, SPY 15.5x and 28.0x). The argument they support, that raw
  prices hide what bonds paid, stands either way.
- A limit no harness can fix: an agent's own memory of how markets moved in 2025-26 is not
  fenced off by a date cut.

### 5. Two fitted rules were graded on a default in the stretch that decided everything

**What the runs say.** `hmm-regime` is dead because it loses to the 200-day average (0.89 against
1.01) and "sat through the dot-com bust (-57%): a slow grind down at moderate volatility looks
calm to it". `hawkes-clustering` is "equal weight minus a few days".

**What I found.** Both rules, and their twin `vol-calm`, hold an asset by default until it has
1,000 bars and a yearly fit. First fitted model per asset: SPY 1998-01, QQQ 2004-01, TLT
2007-01, GLD 2009-01, BTC 2015-01, ETH 2020-01. So through the whole dot-com bust there was no
model for QQQ, the asset that lost 83%. Re-run: share of the bust in which each slot was held:

| Rule | SPY slot | QQQ slot |
|---|---:|---:|
| `hmm-regime` (hard) | 13% | 100% |
| `hawkes-clustering` | 85% | 100% |
| `vol-calm` (their twin) | 0% | 100% |
| `sma200` | 22% | 18% |
| `tsmom12` | 27% | 26% |

The hidden Markov model did not sleep through the bust: on SPY, where it existed, it was out
87% of the time. The 57% loss is the QQQ slot held by default. The stated cause of death is
wrong.

The verdict still holds on later data. `hmm-regime` (hard) against the 200-day average: -0.12
over 1994-2025, +0.04 without the bust, -0.05 from 2004 (p = 0.64), -0.18 from 2017-06. Against
equal weight it is within 0.02 in every window before 2017 and behind after. `hawkes-clustering`
is within 0.05 of equal weight in every window.

**What it changes.** No verdict. It answers the brief's question: I found no idea killed by a
bug, and one given the wrong reason. For later fitted rules: a rule that needs four years of
bars before it acts should be compared only from the day it acts, or borrow history the way
the ML tests did. Otherwise it is graded on its default.

### 6. The luck check: right arithmetic, and the conclusion survives its weak points

**What the runs say.** The best of 52 selectable variants beat equal weight by 0.22 Sharpe; luck
alone would give about 0.24; so no rule has shown an edge.

**What I found.**

- The formula (Bailey and López de Prado's expected maximum) is coded correctly. With 52 tries
  and a standard error of 0.11 I get 0.25.
- It treats the 52 tries as independent. They are not: 31 are ML models on the same features,
  and the top six rows of `results/deflation.md` are one bet, "hold less when markets are
  falling or wild", made six ways. With ten independent tries the luck figure would be 0.17,
  below the 0.22 seen. So as written the check leans towards "luck" more than the data force it
  to.
- That does not rescue the top six, because of finding 1: their +0.14 to +0.22 over equal
  weight is the dot-com bust on the two-asset book. Of the four I re-ran from 2003-09, the
  best three are +0.18, +0.13 and +0.12, each with p between 0.10 and 0.16 before any
  allowance for having been picked out of 52.
- Some choices have no row: the twins themselves (`tsmom12` +0.17, `sma200` +0.13) and the
  12-month lookback (9 months gives +0.25 and 15 months +0.01 in my re-run). Small next to 52.

**What it changes.** Nothing in the conclusion: no rule has shown an edge beyond luck. For the
M1 lane's deflated Sharpe, counting the 52 rows as independent errs on the safe side.

### 7. The out-of-universe sets are thin, and the coin set is tilted

**What the runs say.** Each idea is re-run on 8 other ETFs, 6 other coins and 4 stock indexes;
bar 4 asks for the right sign in two of the three.

**What I found.**

- **Coins.** The six are "among the largest in January 2018 and listed by Coinbase or Bitstamp
  with long history". In practice that means coins still trading on a major venue in November
  2026: all six have bars to 2026-11-11 in my fetch. Large coins of January 2018 that these
  venues never listed, or dropped, are missing (NEM, IOTA, NEO and Monero among them). A rule
  that sells what keeps falling earns its keep on exactly those. So the set flatters holding
  and understates trend rules (`tsmom12` 0.54 against 0.72 for holding the six). It is also
  short and noisy: it starts in 2017-08 with one coin, and its Sharpe ratios carry a standard
  error of 0.34.
- **Indexes.** The "next open" is often not a price anyone could trade. Share of days on which
  the open equals the previous close: S&P 500 index 64% to 92% in each decade from the 1960s to
  the 2000s; FTSE 95% to 100% from 2000 to 2025 (the protocol says "before about 2010"). There
  a fill is at the close the signal was computed from. For the Nikkei until the late 1980s and
  the DAX into the 1990s the open equals that day's own close, so the fill is one day late
  instead.
  Slow rules hardly notice. Fast ones do: `dip-rsi2`'s index results on the S&P and FTSE are in
  effect close-fill results.
- The DAX series (`^GDAXI`) includes dividends; the protocol calls all four "price indexes, no
  dividends".
- Bar 4 counts signs, and several of the differences are +0.00 to +0.03 (`trend-vol` on the
  indexes +0.00, `kelly-shrunk` on the ETFs -0.00, `vol-target` on the indexes +0.01). The sign
  of a number that small is a coin toss. This is part of why the bar is blunt (finding 2).

**What it changes.** No verdict: no idea failed on bar 4 alone. For later cards, count the coin
set as a weak vote that leans against anything that sells losers, and state the fill caveat for
the FTSE through 2025.

### 8. Smaller things

- `results/baselines.md` shows the Nikkei, FTSE and DAX alone from 1994-02-01. The code
  (`common.ctx`) and every idea test use each index's whole history (from 1966, 1985 and 1988),
  re-logged in `tries.md` at 02:00. The file is stale and would not reproduce. The change was
  made before the first idea test, so no result was chosen by it.
- The six assets were picked in 2026, knowing they had gone up (BTC about 21,000-fold, ETH about
  270-fold over their histories). That flatters every growth figure in the tables (18% to 31% a
  year), and it flatters holding more than it flatters a rule that sells losers. It cuts against
  finding 1's reading: the tie since 2003 means the edge is unproven, not that the rule is
  useless.
- Cash earns nothing in the gym. By the runs' own what-if (`results/cash-interest.md`) that
  costs the cautious rules 0.5% to 0.8% a year: also against the trend rule, and too small to
  reopen finding 1.
- ETF costs of 2 bps a side are too low for the 1990s. The rules trade their equity one to five
  times a year, so even ten times that cost moves nothing.
- `tsmom12` is ranked on a one-sided p of 0.08. Two-sided it is about 0.16.
