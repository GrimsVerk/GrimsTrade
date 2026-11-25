# Gate null: judge every gate against its own placebos, not N(0, 1)

Method note, wide-9, 2026-11-19. Applies to every event-study gate from now on (and to any
card whose statistic comes from a few clustered events). Written after wide-8 measured the
problem and wide-9's two gates measured it again.
Amended 2026-11-19 by `gate-null-2` (placebo rule in step 1, new step 7, kill-only label):
see "Method change" at the end.

## The problem, in numbers

A gate reads a t from an event study. ann-1 and wide-6/7 read it against a standard normal
(t >= 2 means about 2.5% one-sided). That is only right when the events are independent and
the standard error sees all of the dependence. In this project's designs it often does not:
events cluster in a few years or episodes, a dose (a loss, an index) is autocorrelated, and
the funds or days in one window move together. The spread of the same statistic over placebo
versions of the design (same code, same data, events moved where no story predicts anything)
shows how wide the real null is:

| Design (run) | Placebos | SD of placebo t | Share with \|t\| >= 2 | Why |
|---|---:|---:|---:|---|
| Cross-section of 21 ETFs, 10-day return on 11-month loss, one window (wide-8, turn-of-year) | 153 placebo windows | **2.18** | **35%** | funds in one window move together; few independent bets |
| Monthly 6-month DBC return on lagged ONI, Newey-West 6 lags (wide-9, W19) | 40 year-shifted ONI calendars | **1.74** | **20%** | ENSO episodes last a year; ~8 independent swings in 12 years |
| SPY daily return, six sessions after severe geomagnetic storms, NW 5 lags (wide-8, W16) | 30 shifted Ap calendars | 1.48 * | 20% * | 19 storm days in about a dozen episodes |
| SPY new- minus full-moon days (wide-6, W3) | 28 phase shifts | 1.34 * | 11% * | adjacent shifts overlap; a smooth wave, not independent draws |
| GLD festival runs minus their month's mean (wide-7, W13) | 14 weekly shifts | 0.59 * | 0% * | few placebos |
| ETH minus BTC, ten days into and after 15 upgrades, one-sample t (wide-9, W17) | 40 calendars moved by k x 30 days | **1.05** | **2%** | non-overlapping, roughly independent events: the normal null is right |
| TLT open-to-close on the day's Fed purchase dose, HC1, 2,983 days (wide-10, W20) | 40 calendars moved k trading days | 0.99 | 2% | daily, nearly independent days: normal null about right |
| BTC/ETH next-week return on weekly stablecoin issuance, HC1, 339 weeks (wide-10, W21) | 40 calendars moved k weeks | 1.24 | **28%** | persistent dose, high in bull markets: shifted doses share the regime (median +0.85) |
| 4-week return of GLD/TLT/SPY/QQQ on hedging-pressure z, Driscoll-Kraay 4 lags, 1,484 rows (wide-11, W22) | 40 calendars moved k = 27-103 weeks | 1.13 | 8% | persistent dose that follows price at 6-12 months: future-dose shifts lean positive (95% +2.22, max +3.41) |
| 4-week return of TLT/IEF on foreign official custody-flow z, four price controls, Driscoll-Kraay 4 lags, 1,644 rows (wide-12, W23) | 40 calendars moved k = 27-103 weeks | 1.19 | 10% | persistent dose, symmetric null (5/95% -2.07/+1.89): same family as W22, same width |
| Next-quarter return of TLT/IEF on SPF 10-year inflation-dispersion z, Driscoll-Kraay 1 lag, 124 rows (wide-12, W24) | 40 calendars moved k = 7-45 quarters | 0.90 | 0% | non-overlapping quarters, short placebo samples (36-124 rows): narrower than normal |
| 4-week return of GLD/TLT on GPR acts z from its available-on date, Driscoll-Kraay 4 lags, 2,166 rows (wide-13, W25) | 40 calendars moved k = 27-103 weeks (earlier-dose half only, per review-2: 20) | 1.11 (0.97) | 12% (5%) | index shares slow regimes with safe havens: centred below zero (median -0.96; earlier-only -0.26) |
| 4-week return of XLF on ln(1 + FDIC failed assets), four price controls, Newey-West 4 lags, 1,344 weeks (wide-13, W26) | 40 calendars moved k = 27-103 weeks (earlier-dose half only: 20) | 1.63 (0.48) | 25% (0%) | failures follow XLF at 52 weeks (t -3.87): later-dose shifts carry the whole negative tail (to -4.37), review-2 point (1); about two episodes, kill-only |
| 4-week return of SPY on Anscombe roll-call count, session dummy and four price controls, Newey-West 4 lags, 1,653 weeks (wide-15, W27) | 40 earlier-dose calendars, k = 27-105 weeks (odd) | 1.08 | 5% | weekly count with no price feedback found (t <= 1.01): near normal |
| 4-week return of QQQ/IWM/BTC/ETH on the runoff of the IRS refund surprise, Driscoll-Kraay 4 lags, 2,999 rows (wide-15, W28) | 40 calendars moved k = 27-103 weeks, both ways | **1.92** | **32%** | dose large only about 15 weeks a year, four co-moving assets: about one independent draw per season (about 18) |
| SPY next-but-one month return on GISTEMP 12-month anomaly minus prior decade, Newey-West 3 lags, 393 months (wide-17, W29) | 40 calendars moved k = 13-89 months, both ways | 1.47 | 22% | persistent dose with a few ENSO-paced swings; far shifts carry the upper tail (to +3.11) |
| SPY 4-week return on detrended Anscombe count of WHO outbreak reports, Newey-West 4 lags, 1,082 weeks (wide-17, W30) | 40 calendars moved k = 27-103 weeks, both ways | **1.64** | **22%** | one website re-dating week (2021-06-11, 814 items, x about 23 sd) dominates; 2005-2019 alone SD 1.16, 7% (wide-17 erratum) |
| SPY daily return on log2(deaths / 25) of aviation accidents (>= 50 deaths), days 0-1, HC1, 4,488 days (wide-20, W31) | 40 calendars moved 23k days, wrapped, both ways | 0.91 | 2% | 34 unscheduled, nearly independent events on daily returns: about normal, slightly narrow |

\* Pseudo-t: the stored placebo effects divided by the true cell's standard error (effect / t,
from rounded stored values, good to about 5%). These gates stored effects, not placebo t.
Not recoverable from stored output: W15 `cat-claims` (true slope +0.01, t 0.09: the implied
standard error is too imprecise); W14 `wash-sale-echo` and W12 `rmd-december` (no shifted
calendars; W12 used a permutation p, which is already an empirical null).

So: **clustered or autocorrelated designs overstate t by 1.5-2x** (35% of placebos past
|t| 2 instead of 5%); independent-event designs do not. Which one a gate is cannot be told in
advance with confidence, so every gate measures it.

## The procedure (every gate from wide-9 on)

1. **Placebo family in the rule, before any number.** Pick one way to move the events where
   the mechanism predicts nothing, and write it into the rule:
   - shifted calendars: the whole event calendar moved by k x a step that is not a multiple of
     the mechanism's own clock (61 days for storms: not a multiple of the 27-day solar
     rotation; 30 days for scheduled upgrades);
   - whole-year shifts when a seasonal cycle must be kept (ONI moved by k years, hurricane days
     moved to the same date k years away);
   - placebo windows: the same construction anchored at other months (wide-8's turn of year);
   - permutation of the event years when there are only a handful (W12).
   Leave out placebos that share part of the true events (W19 dropped k = 1: ENSO episodes
   span two calendar years).
   **No placebo may use information from the outcome window** (rule added 2026-11-19, see
   "Method change" below). A placebo dose, including any window it is built on (a z-score's
   lookback, a moving sum), must end before the outcome it is paired with starts. For a dose
   that can respond to prices (positioning, flows, issuance, failures, anything F2 can find),
   this rules out backward shifts (a later dose, negative k): use only earlier doses, far
   enough back that the placebo is not a lagged copy of the true dose, or whole-year shifts
   that keep the dose before the outcome. Shifts in both directions stay allowed only for doses
   that prices cannot move (calendars, weather, solar activity, scheduled dates).
2. **At least 20 placebos, 40 by default.** The smallest one-sided p is 1 / (1 + N).
3. **Same statistic, same code path.** The placebo t is computed by the very function that
   computes the true t (a `shift` argument, not a copy).
4. **The rank decides.** Pass needs the true statistic among the 2 highest (or lowest, by the
   predicted sign) of 1 + N: empirical one-sided p = rank / (1 + N), about 0.05 at N = 40.
   Keep t >= 2 as an extra necessary condition; it costs nothing.
5. **Report the null's width every time.** Every gate result prints the placebo t's standard
   deviation, the share with |t| >= 2, the 5/50/95% quantiles and the extremes, next to the
   true t. That is the design diagnostic the next reader needs.
6. **Shown cells inherit the null.** A shown cell with |t| 2.5-3.5 in a design whose placebo
   SD is near 2 is ordinary, and is written as "noted only", never as a lead. A shown cell that
   looks like a lead needs its own placebo before anyone writes "lead" (wide-8 did this for the
   turn-of-year cell: t 3.9 in the pooled table, rank 6 of 154 in the one-window null).
7. **State the smallest honest p, and label kill-only gates** (replaces the old step 7,
   2026-11-19). The card's p must beat the family bar (p < 0.00139) and the register's
   (p <= 4.9e-5 at 2,904 tries). A rank among 40 placebos bottoms at 0.024, and reading t
   against the placebos' median and SD at N(0, 1) (the old step 7) extrapolates a 40-draw
   scale about four SDs into a tail this method has measured as heavy (W19's -5.93 among 40,
   the wide-8 null's +8.9 among 153): that p is not valid. A block bootstrap by event cluster
   cannot reach 1e-4 honestly either when there are only 8-20 independent episodes. So each
   gate writes into its rule, before any number: the number of independent episodes (years,
   swings, crises) and the smallest p its design can honestly reach (at best about
   1 / (number of distinct placebo or bootstrap outcomes), and never below what the episode
   count supports). If that p is above the card bar, the gate is labelled **kill-only**: a
   fail kills the idea; a pass only says "not dead yet" and needs a new design with more
   independent episodes (other markets, other periods, more events) before any card. **A
   clustered design with about 10 independent episodes is kill-only.**

## Earlier verdicts re-read under the placebo null

All from the stored outputs (`research/results/*.md`, the write-ups); nothing rerun.

| Gate (run) | Gate statistic as stored | Null used then | Under a placebo null | Verdict |
|---|---|---|---|---|
| FOMC pre-announcement drift (ann-1) | SPY day 0 minus other days 2015-2025: -0.8 bps (Welch t -0.06) | N(0, 1) | negative sign: no placebo can make it pass | dead, unchanged |
| `critical-slowing` (wide-6) | slopes: tauAC1 +0.039 (t 1.44) in-sample, +0.003 (0.12) after; tauVAR -0.019 (-0.53), +0.040 (1.82); needed t >= 2.24 in both periods | N(0, 1) (Driscoll-Kraay) | each indicator misses in at least one period by sign or t below 1.5; a wider null only raises the bar | dead, unchanged |
| `lunar` W3 (wide-6) | +1.6 bps a day (t 0.43) | 28 phase shifts (rank 12 of 29) | already placebo-ranked | dead, unchanged |
| `rmd-december` W12 (wide-7) | excess -0.06% (wrong sign) | permutation p 0.51 | already empirical | dead, unchanged |
| `festival-gold` W13 (wide-7) | -1.9 bps a day (t -0.30) | 15 weekly shifts (rank 10) | already placebo-ranked | dead, unchanged |
| `wash-sale-echo` W14 (wide-7) | echo slope -0.003 (t -0.07) / +0.023 (t 0.43) | N(0, 1), year-clustered | t far below any bar | dead, unchanged |
| `geomagnetic-storm` W16 (wide-8) | +18.2 bps (t +2.46), wrong sign | 30 shifted calendars (rank 29 of 31) | already placebo-ranked | dead, unchanged |
| `cat-claims` W15 (wide-8) | +0.01 per category (t 0.09) | 22 shifted calendars (rank 8 of 23) | already placebo-ranked | dead, unchanged |
| `enso-commodity` W19 (wide-9) | -2.5 points per degree (t -0.92) | 40 placebos (rank 32 of 41) | this procedure | dead |
| `fork-premium` W17 (wide-9) | +0.7% (t 0.23) | 40 placebos (rank 19 of 41) | this procedure | dead |

**No verdict changes.** Every gate failed with its main statistic of the wrong sign or with
|t| < 1.5, and a placebo null at least as wide as N(0, 1) (the only exception measured, W13's
0.59 from 14 placebos, was already rank-judged) can only make a pass harder. The re-reading
changes the weight of the **shown** cells, not the verdicts:

- wide-7's turn-of-year cell (t 3.9): already re-read by wide-8 (rank 6 of 154); kept only as a
  forward test with 8% power.
- ann-1's TLT on FOMC days after 2015 (+26.5 bps, t 2.3, one of about 70 cells, in-sample for
  its own paper) and BTC (t 2.1 with a sign flip): independent daily events, so the normal null
  may be roughly right there, but one of 70 cells at t 2.3 is what chance gives. Noted only, as
  ann-1 said.
- wide-6's raw rising-variance effect (S&P 500 t 2.6, Driscoll-Kraay on overlapping 21-day
  windows, the clustered kind): would need its own placebo; it also vanishes with a volatility
  control. Noted only.
- wide-8's W15 TLT cell (t -3.0, season-clustered landfalls) and wide-9's W19 SLV (t 3.25) and
  GLD (t 2.61): clustered designs, no placebo computed; inside the range of the measured nulls
  (wide-8 95%/2%: +3.33/-4.26; W19 extremes -5.93/+2.84). Noted only.

None of the earlier gates was near a pass, so nothing here asks for a rerun. If a later lane
wants the table above to carry placebo t for W14, W15 and the shown cells, each is one cheap
rerun with a `shift` argument added; that is optional, not a correction.

## Method change, 2026-11-19 (lane `gate-null-2`, from review-2)

The independent review `review-2` (`research/reviews/review-2.md` on branch `review-2`, section
5) found two faults in this note, both fixed above:

1. **Backward shifts look into the outcome.** W22 (wide-11) moved a price-responsive dose (the
   hedging-pressure z, 156-week window) both ways. For negative k the placebo dose is z from
   27-103 weeks *later*, whose window contains the outcome weeks, and hedgers add to their net
   short after rallies. The placebo t are lopsided: the 20 backward shifts average **+0.74**
   (the ten nearest, k = -27..-63, all at least +0.83), the 20 forward shifts **-0.39** (none
   above +0.65), and all three placebos with t >= 2 are backward (k = -27: +2.52, -31: +3.41,
   -55: +2.20) (review-2, 5b). Such a null is too wide on the side a true effect would need,
   so it would fail a real effect. Step 1 now forbids it.
2. **Step 7 was invalid** (extrapolating 40 placebos to p 1e-4). Replaced by "state the
   smallest honest p; kill-only when it is above the card bar".

Old gates are not re-run. The table lists every gate verdict so far, whether its placebos used
backward shifts of a dose that prices can move, and whether the verdict could flip.

| Gate (run, branch) | Placebos | Backward shift of a price-responsive dose? | True statistic | Could the verdict flip? |
|---|---|---|---|---|
| ann-1 FOMC drift | none, N(0, 1) | no | t -0.06 | no: wrong side |
| `critical-slowing` (wide-6) | none, N(0, 1) | no | t < 1.5 or wrong sign in a period | no |
| W3 `lunar` (wide-6) | phase shifts, both ways | no: a calendar | t +0.43 | no: t < 2 |
| W12 `rmd-december` (wide-7) | permutation of years | no | wrong sign | no |
| W13 `festival-gold` (wide-7) | weekly shifts | no: a calendar | t -0.30 | no |
| W14 `wash-sale-echo` (wide-7) | none (year-clustered N(0, 1)) | no | t -0.07 / +0.43 | no |
| W15 `cat-claims` (wide-8) | k = -11..11 shifts | no: landfalls | t +0.09 | no |
| W16 `geomagnetic-storm` (wide-8) | k x 61 days, both ways | no: solar activity | t +2.46, wrong sign | no |
| W17 `fork-premium` (wide-9) | k x 30 days, both ways | no: scheduled upgrades | t +0.23 | no |
| W19 `enso-commodity` (wide-9) | k = 2..41 years, earlier only | no | t -0.92 | no |
| W20 Fed purchase dose (wide-10) | k = 3..27 days, both ways | judged no: purchases follow a schedule announced ahead | t +0.37, rank 11 | no: t < 2 |
| W21 stablecoin issuance (wide-10) | k = 3..22 weeks, both ways | **yes**: issuance runs high in bull markets (placebo median +0.85) | t +1.06, rank 17 | no: t < 2 |
| W22 hedging pressure (wide-11) | k = 27..103 weeks, both ways | **yes** (above) | t +0.49 | no: t < 2 |
| W23 custody flow (wide-12) | as W22 | **yes**: holdings follow TLT's same-week return | t -1.20, wrong sign | no |
| W24 inflation dispersion (wide-12) | k = 7..45 quarters, both ways | possible (survey dispersion may follow yields) | t -0.75, wrong sign | no |
| W25 `act-haven` (wide-13) | k = 27..103 weeks; earlier half also reported | yes, weakly (26-52-week link) | t -1.02, wrong sign | no |
| W26 `failure-premium` (wide-13) | k = 27..103 weeks; earlier half also reported | **yes**: failures follow XLF (t -3.87) | t -0.48, wrong sign | no |
| weather-1 (#116) | 40 derangements of winters | no: weather | t -0.29, rank 19 | no |
| W27 `congress-workload` (wide-15) | k = 27..105 weeks, earlier only | not used (earlier only, as step 1 asks) | t -0.19, wrong sign, rank 25 | no |
| W28 `refund-runoff` (wide-15) | k = 27..103 weeks, both ways | no: refunds do not answer prices (feedback t -1.20 .. +1.08) | t +1.44, rank 7 | no: t < 2 |
| W29 `temperature-premium` (wide-17) | k = 13..89 months, both ways | no: temperature does not answer prices | t +1.63, rank 9 | no: t < 2 |
| W30 `outbreak-premium` (wide-17) | k = 27..103 weeks, both ways | no: WHO reporting does not answer prices | t +1.68, rank 9 | no: t < 2 |
| W31 `air-disaster-mood` (wide-20) | 23k days wrapped, k = ±1..20, both ways | no: accidents do not answer prices | t -0.59, rank 10 | no: t > -2 |

W23-W26 rows sit on branches made after this one (`wide-12`, `wide-13`); the facts are read
from their write-ups. weather-2 (#117) uses winter derangements (allowed) but its "bar, if the
gate passes" section leans on the old step 7; with 13 winters it is kill-only.

**No verdict can flip, and dead ideas stay dead.** A gate passes only if the true t is at least
2 with the predicted sign *and* ranks among the top 2 of 41. Removing contaminated placebos can
only narrow the null on the side that matters, so it could turn a fail into a pass only where
the true t cleared 2 with the right sign and the rank alone failed. No gate is in that position:
every one failed on its own t (wrong sign or t < 2). Where a null is widened instead (stricter
placebos, kill-only labels), passing only gets harder. The clustered gates above (few episodes:
W15, W16, W19, W21-W26, weather-1) would be kill-only by the new step 7, so the count "19 tested, none passed" is weaker evidence against
borrowed ideas than it sounds, because several gates had little power by design (review-2, 5d).
