# Gate null: judge every gate against its own placebos, not N(0, 1)

Method note, wide-9, 2026-11-19. Applies to every event-study gate from now on (and to any
card whose statistic comes from a few clustered events). Written after wide-8 measured the
problem and wide-9's two gates measured it again.

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
| 4-week return of GLD/TLT on GPR acts z from its available-on date, Driscoll-Kraay 4 lags, 2,166 rows (wide-13, W25) | 40 calendars moved k = 27-103 weeks (earlier-dose half only, per review-2: 20) | 1.11 (0.97) | 12% (5%) | index shares slow regimes with safe havens: centred below zero (median -0.96; earlier-only -0.26) |
| 4-week return of XLF on ln(1 + FDIC failed assets), four price controls, Newey-West 4 lags, 1,344 weeks (wide-13, W26) | 40 calendars moved k = 27-103 weeks (earlier-dose half only: 20) | 1.63 (0.48) | 25% (0%) | failures follow XLF at 52 weeks (t -3.87): later-dose shifts carry the whole negative tail (to -4.37), review-2 point (1); about two episodes, kill-only |

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
7. **After a gate passes, for a card.** The card's p must beat the family bar (p < 0.00139)
   and the register's (p <= 4.9e-5 at 2,904 tries); a rank among 40 placebos cannot reach
   either (it bottoms at 0.024). The card's test therefore reads its t against the placebo
   distribution's scale: z = (t - median of placebo t) / SD of placebo t, read against N(0, 1)
   at the bar, and states both z and the plain t. If the placebo t look far from normal (heavy
   tails: the wide-8 null reached +8.9 among 153, W19's -5.93 among 40), the card instead uses a block bootstrap
   by event cluster (year or episode) for its p, and says so in the card before the run.

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
