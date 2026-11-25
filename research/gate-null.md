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
| Same-month spread (top fifth minus bottom fifth of 20-year same-month averages), 23 assets, Friday clock, 106 months 2017-2025 (survey-7, `seasonal-20y`) | 40 month-index shifts off the annual cycle (lags 13 months or more) | 0.79 | 2% | non-overlapping monthly spreads: about normal; median +0.58 (every placebo lag carries the assets' long-run mean) |
| TLT open-to-close on the day's Fed purchase dose, HC1, 2,983 days (wide-10, W20) | 40 calendars moved k trading days | 0.99 | 2% | daily, nearly independent days: normal null about right |
| BTC/ETH next-week return on weekly stablecoin issuance, HC1, 339 weeks (wide-10, W21) | 40 calendars moved k weeks | 1.24 | **28%** | persistent dose, high in bull markets: shifted doses share the regime (median +0.85) |
| 4-week return of GLD/TLT/SPY/QQQ on hedging-pressure z, Driscoll-Kraay 4 lags, 1,484 rows (wide-11, W22) | 40 calendars moved k = 27-103 weeks | 1.13 | 8% | persistent dose that follows price at 6-12 months: future-dose shifts lean positive (95% +2.22, max +3.41) |
| 4-week return of TLT/IEF on foreign official custody-flow z, four price controls, Driscoll-Kraay 4 lags, 1,644 rows (wide-12, W23) | 40 calendars moved k = 27-103 weeks | 1.19 | 10% | persistent dose, symmetric null (5/95% -2.07/+1.89): same family as W22, same width |
| Next-quarter return of TLT/IEF on SPF 10-year inflation-dispersion z, Driscoll-Kraay 1 lag, 124 rows (wide-12, W24) | 40 calendars moved k = 7-45 quarters | 0.90 | 0% | non-overlapping quarters, short placebo samples (36-124 rows): narrower than normal |
| UNG next-week return on the gas-weighted 7-day HDD surprise, HC1, 389 weeks, winters 2007-08..2024-25 (weather-1, `hdd-gas`) | 40 winter derangements | 1.12 | 10% | non-overlapping weeks, whole-winter permutation: close to N(0, 1), slightly wide |
| 4-week return of GLD/TLT on GPR acts z from its available-on date, Driscoll-Kraay 4 lags, 2,166 rows (wide-13, W25) | 40 calendars moved k = 27-103 weeks (earlier-dose half only, per review-2: 20) | 1.11 (0.97) | 12% (5%) | index shares slow regimes with safe havens: centred below zero (median -0.96; earlier-only -0.26) |
| 4-week return of XLF on ln(1 + FDIC failed assets), four price controls, Newey-West 4 lags, 1,344 weeks (wide-13, W26) | 40 calendars moved k = 27-103 weeks (earlier-dose half only: 20) | 1.63 (0.48) | 25% (0%) | failures follow XLF at 52 weeks (t -3.87): later-dose shifts carry the whole negative tail (to -4.37), review-2 point (1); about two episodes, kill-only |
| UNG open-to-close on the change of a gas-weighted CPC 6-10/8-14 day cold-outlook index, HC1, 1,327 sessions, 13 winters (weather-2, `cpc-revision`) | 40 winter derangements | 0.95 | 10% | centred above zero (median +0.78): calendar structure shared across winters; 13 winters, kill-only |
| 4-week return of SPY on Anscombe roll-call count, session dummy and four price controls, Newey-West 4 lags, 1,653 weeks (wide-15, W27) | 40 earlier-dose calendars, k = 27-105 weeks (odd) | 1.08 | 5% | weekly count with no price feedback found (t <= 1.01): near normal |
| 4-week return of QQQ/IWM/BTC/ETH on the runoff of the IRS refund surprise, Driscoll-Kraay 4 lags, 2,999 rows (wide-15, W28) | 40 calendars moved k = 27-103 weeks, both ways | **1.92** | **32%** | dose large only about 15 weeks a year, four co-moving assets: about one independent draw per season (about 18) |
| SPY next-but-one month return on GISTEMP 12-month anomaly minus prior decade, Newey-West 3 lags, 393 months (wide-17, W29) | 40 calendars moved k = 13-89 months, both ways | 1.47 | 22% | persistent dose with a few ENSO-paced swings; far shifts carry the upper tail (to +3.11) |
| SPY 4-week return on detrended Anscombe count of WHO outbreak reports, Newey-West 4 lags, 1,082 weeks (wide-17, W30) | 40 calendars moved k = 27-103 weeks, both ways | **1.64** | **22%** | one website re-dating week (2021-06-11, 814 items, x about 23 sd) dominates; 2005-2019 alone SD 1.16, 7% (wide-17 erratum) |
| SPY daily return on log2(deaths / 25) of aviation accidents (>= 50 deaths), days 0-1, HC1, 4,488 days (wide-20, W31) | 40 calendars moved 23k days, wrapped, both ways | 0.91 | 2% | 34 unscheduled, nearly independent events on daily returns: about normal, slightly narrow |
| TLT next-quarter return on -PDSI (contiguous US drought), Newey-West 3 lags, 276 months (parked-gates-1, W32) | 40 calendars moved k = 13-89 months, both ways | 0.94 | 0% | persistent dose, but placebo t stay inside -1.76 / +1.95; the true t -3.71 ranked 1 (the first pass), then failed its replication R32 |
| 10-year yield change over the next quarter on -PDSI, Newey-West 3 lags, 483 months 1962-2002 (parked-gates-1, R32) | 40 calendars moved k = 13-89 months, both ways | 1.19 | 8% | same dose, 40 other years: wider than W32's |
| GSPC next month on this month's fall x detrended ln(broker customer receivables / equity value), four controls, Newey-West 3 lags, 729 months (parked-gates-1, W33) | 40 earlier-dose calendars, k = 25-103 months (odd) | 0.58 | **30%** | **off-centre**: all 40 placebo t positive (median +1.70, 95% +3.06): an earlier-only family can be biased; the rank is the reference |
| US market (French daily) next month on detrended ln share of newspaper articles with "panic", three price controls, Newey-West 3 lags, 438 months 1927-1963 (panic-words-1, W34) | 40 earlier-dose calendars, k = 25-103 months (odd) | 1.18 | 10% | earlier-only family, centred this time (median -0.10, 5/95% -2.03/+1.47); panic peaks cluster in 1929-1933 |
| Shiller S&P 500 next month (monthly averages) on trailing 12-month mean sunspot number, Newey-West 12 lags, 1,831 months 1871-2023 (wide-21, W35) | 40 calendars moved k = 19-95 months, both ways | 1.16 | 25% | **off-centre** (median +1.25, 95% +2.83, max +3.11): a cyclic dose shifted 4-8 years becomes its own anti-phase, so the family repeats one weak pattern with the opposite sign; about 14 cycles |
| French Mkt-RF of month m+3 on year-on-year growth of EIA industrial electricity sales, Newey-West 3 lags, 619 months 1974-2025 (wide-22, W36) | 40 earlier-dose calendars, k = 25-103 months (odd) | 0.91 | 2% | persistent macro dose, centred (median -0.44, 5/95% -1.38/+1.40); 40 phase-randomised surrogates (shown) are wider: SD 1.10, 10%, smallest -2.62, and rank the true t 3, not 1 |
| Same on yoy growth of NBER utility electricity production (spliced), 357 months 1926-1955 (wide-22, R36) | 40 earlier-dose calendars, k = 25-103 months (odd) | 0.55 | 0% | narrower than N(0, 1) (5/95% -1.36/+0.60, extremes -1.78/+0.66); phase surrogates SD 1.10 |
| ETH 7-day return from the end of day d+1 on log2(USD stolen / 5 m) of DefiLlama non-exchange thefts >= USD 10 m on day d, controls r7 r30, Newey-West 7 lags, 3,412 days 2016-2025 (wide-23, W37) | 40 earlier-dose calendars, k = 23-920 days (step 23) | 1.02 | 5% | 109 nearly independent event days: about normal, slightly left (median -0.60, 5/95% -1.85/+1.19, min -3.61); phase surrogates SD 1.13 (10%), random-day surrogates SD 1.08 (8%); without the one event not public at its date (LuBian, post hoc) placebo SD 1.02, random-day 0.94 |
| JST next-year log equity return over bills on the Hamilton consumption cycle, country dummies and three controls, Driscoll-Kraay 2 lags, 355 country-years 1904-1947, 14 countries (jst-gates-1, W38) | 20 earlier-dose calendars, k = 4-23 years | 1.06 | 5% | centred (median -0.10, 5/95% -2.00/+1.39, extremes -2.29/+1.82); the returns-side AR bootstrap (SD 1.32, median +0.34) and phase surrogates with shared phases (SD 1.49) are wider |
| Same design on JST `lev` minus its trailing 10-year mean, plus a crisis control, 1,285 country-years 1925-2020, 16 countries (jst-gates-1, W39) | 40 earlier-dose calendars, k = 5-44 years | 1.09 | 12% | **off-centre** (median +0.23, 95% +2.16, max +2.37: k = 20-29 sit near +2, as W33); bootstrap SD 1.09 and phase SD 0.89 are centred |
| Hit country's index minus the other 24 cached markets, 20 sessions from the close of s0+1, on log2(1 + % of the country's place population within a magnitude radius) of declustered M >= 6 shallow quakes, controls r2 r20, market dummies, Driscoll-Kraay 30 days, 168,901 rows, 25 markets, 1998-2025 (wide-24, W40) | 40 calendars moved 23k days, k = +-1..20, both ways | 1.09 | 5% | 79 nearly independent (event, market) pairs, dose acf1 +0.008: about normal (median +0.15, 5/95% -1.95/+1.30, extremes -2.29/+1.80); random-day surrogates SD 1.28 (5%), one draw at +4.77 |
| Country's French USD market minus the other 20 over the six months after a ParlGov mid-term cabinet start (binary monthly dose), own excess 1/3/12-month controls, country dummies, Driscoll-Kraay 6 lags, 9,300 country-months 1976-2022, 18 countries, 171 event months (wide-25, W41) | 40 earlier-dose calendars, k = 25-103 months (odd) | 1.24 | 8% | upper side wide (median +0.14, 95% +2.26, max +3.39): shifts of 31-53 months lean positive, perhaps the 3-5 year election clock; random-month surrogates (shown) centred, SD 1.10, 5% |
| US food industry (French 49 VW Food) minus 60-month beta x market, months m+2..m+4, on -PDSI of the Corn Belt (nClimDiv 361), Newey-West 3 lags, 786 months 1960-2025 (wide-26, W43, provisional id) | 40 calendars moved k = 13-89 months, both ways; 40 phase surrogates (both families: dose acf1 0.94) | 1.10 | 8% | persistent physical dose, centred (median +0.03, 5/95% -1.68/+1.52, extremes -2.28/+2.02); phase surrogates wider: SD 1.25, 15%, extremes -2.97/+2.65 |
| Losing country's index next-session return minus the other cached markets on 1 per World Cup / Euro knockout elimination, market dummies, Driscoll-Kraay 5 days, 122,576 rows, 25 markets, 2006-2025 (wide-26, W18, record-closing) | 40 calendars moved 23k days, k = +-1..20, both ways | 0.87 | 0% | 74 sparse one-day events, dose acf1 -0.001: narrower than normal (median -0.20, 5/95% -1.20/+1.37, extremes -1.77/+2.00) |

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
| `seasonal-20y` (survey-7) | 40 month-index shifts off the annual cycle, lags 13 months or more | no: earlier lags only | t +0.19, rank 31 | no: t < 2 |
| W20 Fed purchase dose (wide-10) | k = 3..27 days, both ways | judged no: purchases follow a schedule announced ahead | t +0.37, rank 11 | no: t < 2 |
| W21 stablecoin issuance (wide-10) | k = 3..22 weeks, both ways | **yes**: issuance runs high in bull markets (placebo median +0.85) | t +1.06, rank 17 | no: t < 2 |
| W22 hedging pressure (wide-11) | k = 27..103 weeks, both ways | **yes** (above) | t +0.49 | no: t < 2 |
| W23 custody flow (wide-12) | as W22 | **yes**: holdings follow TLT's same-week return | t -1.20, wrong sign | no |
| W24 inflation dispersion (wide-12) | k = 7..45 quarters, both ways | possible (survey dispersion may follow yields) | t -0.75, wrong sign | no |
| W25 `act-haven` (wide-13) | k = 27..103 weeks; earlier half also reported | yes, weakly (26-52-week link) | t -1.02, wrong sign | no |
| W26 `failure-premium` (wide-13) | k = 27..103 weeks; earlier half also reported | **yes**: failures follow XLF (t -3.87) | t -0.48, wrong sign | no |
| weather-1 `hdd-gas` (#116) | 40 derangements of winters | no: weather | t -0.29, rank 19 | no |
| weather-2 `cpc-revision` (#117) | 40 derangements of 13 winters | no: weather forecasts | t -0.68, wrong sign, rank 36 | no |
| W27 `congress-workload` (wide-15) | k = 27..105 weeks, earlier only | not used (earlier only, as step 1 asks) | t -0.19, wrong sign, rank 25 | no |
| W28 `refund-runoff` (wide-15) | k = 27..103 weeks, both ways | no: refunds do not answer prices (feedback t -1.20 .. +1.08) | t +1.44, rank 7 | no: t < 2 |
| W29 `temperature-premium` (wide-17) | k = 13..89 months, both ways | no: temperature does not answer prices | t +1.63, rank 9 | no: t < 2 |
| W30 `outbreak-premium` (wide-17) | k = 27..103 weeks, both ways | no: WHO reporting does not answer prices | t +1.68, rank 9 | no: t < 2 |
| W31 `air-disaster-mood` (wide-20) | 23k days wrapped, k = ±1..20, both ways | no: accidents do not answer prices | t -0.59, rank 10 | no: t > -2 |
| W32 `drought-inflation` (parked-gates-1) | k = 13..89 months, both ways | no: drought does not answer prices | t -3.71, rank 1: **pass (kill-only)** | killed by its replication R32 (1962-2002: t -0.19, rank 21) |
| R32, replication of W32 (parked-gates-1, `cards/parked-gates-1b.md`) | k = 13..89 months, both ways | no: drought does not answer prices | 10-year yield 1962-2002: t -0.19 (predicted > 0), rank 21 | no: t < 2; W32 dead |
| W33 `margin-susceptibles` (parked-gates-1) | k = 25..103 months, earlier only | not used (earlier only, as step 1 asks) | t +0.05, rank 41 | no: t < 2 |
| W34 `panic-words` (panic-words-1) | k = 25..103 months, earlier only | not used (earlier only, as step 1 asks) | t +1.19 (predicted < 0), rank 37 | no: wrong sign |
| W35 `solar-max-recession` (wide-21) | k = +-19..95 months (step 4), both ways | no: the sun does not answer prices | t -0.87, rank 3 | no: t > -2 |
| W36 `grid-load-premium` (wide-22) | k = 25..103 months, earlier only | not used (earlier only, as step 1 asks) | t -2.31, rank 1, post-sample b < 0: **pass (kill-only)** | killed by its replication R36 (1926-1955: t -0.32, rank 13) |
| R36, replication of W36 (wide-22, `cards/wide-22b.md`) | k = 25..103 months, earlier only | not used | t -0.32 (predicted < 0), rank 13 | no: t > -2; W36 dead (low power: see `wide-22.md`) |
| W37 `hack-drift` (wide-23) | k = 23..920 days, earlier only | not used (earlier only, as step 1 asks: the loot scales with prices) | t +0.68 (predicted < 0), rank 38; post hoc without LuBian (USD 3.5 bn, not public at its listed date) t -0.01, rank 31 | no: t near 0 (the positive sign is one event) |
| W38 `consumption-cycle` (jst-gates-1) | k = 4..23 years, earlier only | not used (earlier only, as step 1 asks) | t -1.88, rank 3 of 21 | no: fails t and rank; the predicted sign shows only for the same-year dose, which a real-time reader could not have had (dose of year t-1: t -0.57) |
| W39 `bank-capital-premium` (jst-gates-1) | k = 5..44 years, earlier only | not used | t +0.17 (predicted < 0), rank 19 | no: wrong sign |
| W40 `quake-drift` (wide-24) | k = +-23..460 days, both ways | no: earthquakes do not answer prices | t +0.38 (predicted < 0), rank 24; random-day rank 28 | no: wrong sign |
| W41 `cabinet-collapse` (wide-25) | k = 25..103 months, earlier only | not used (earlier only, as step 1 asks: governments fall after bad markets) | t -1.74 (predicted > 0), rank 41 of 41; random-month rank 39 | no: wrong sign |
| W43 `drought-food-margin` (wide-26) | k = +-13..89 months, both ways, plus 40 phase surrogates | no: drought does not answer stock prices | t +0.07 (predicted < 0), rank 22; surrogate rank 23 | no: wrong sign |
| W18 `elimination-mood` (wide-26, record-closing) | k = +-23..460 days, both ways | no: match results do not answer prices | t -0.95, rank 6 | no: t > -2 |

W23-W26 rows sit on branches made after this one (`wide-12`, `wide-13`); the facts are read
from their write-ups. weather-2 (#117) uses winter derangements (allowed) but its "bar, if the
gate passes" section leans on the old step 7; with 13 winters it is kill-only.

The table holds all **33 gates** of the family count (`parked-gates-1.md`, "Family count";
family after summary-6's correction: 101 mechanisms, 29 tested by a strategy, 28 gates;
panic-words-1 adds W34, wide-21 adds W35, wide-22 adds W36 and its replication R36, wide-23
adds W37: **105 mechanisms, 29 tested by a strategy, 33 gates, family bar p < 0.10 / 105 =
0.00095**):
the 11 through survey-7 (ann-1, wide-6 x 2, wide-7 x 3, wide-8 x 2, wide-9 x 2, survey-7), W20-W26,
weather-1 and weather-2, W27-W37 and the replications R32 and R36 (summary-6 added the
`seasonal-20y`, weather-2 and R32 rows from their write-ups, 2026-11-25). Two passed (W32 and
W36, both kill-only), and each was killed by its replication (R32, R36).

**No verdict can flip, and dead ideas stay dead.** A gate passes only if the true t is at least
2 with the predicted sign *and* ranks among the top 2 of 41. Removing contaminated placebos can
only narrow the null on the side that matters, so it could turn a fail into a pass only where
the true t cleared 2 with the right sign and the rank alone failed. No gate is in that position:
every one failed on its own t (wrong sign or t < 2), except W32 (parked-gates-1) and W36
(wide-22), which passed outright and were killed by their replications R32 and R36. Where a null is widened instead (stricter
placebos, kill-only labels), passing only gets harder. The clustered gates above (few episodes:
W15, W16, W19, W21-W26, weather-1) would be kill-only by the new step 7, so the count "19 tested, none passed" (19 gates then; 33 now, two kill-only passes, both killed by replication) is weaker evidence against
borrowed ideas than it sounds, because several gates had little power by design (review-2, 5d).

## First pass, and what the procedure did with it (parked-gates-1, 2026-11-25)

W32 `drought-inflation` was the first gate in this record to pass (TLT on -PDSI, t -3.71, rank 1
of 41, 2002-2025). Step 7 labels such a pass "not dead yet" and asks for a new design with more
independent episodes. That design (R32, `cards/parked-gates-1b.md`) was carded after the W32
number and before its own: the same dose on the 10-year yield over 1962-2002, the 40 years
before TLT. It failed (t -0.19, rank 21 of 41), and the mechanism's first link (drought, then
higher food prices) was absent in both periods. So a persistent monthly dose passed one
20-year period on a narrow-looking null (placebo SD 0.94) and showed nothing in the 40 years
before: a narrow placebo null does not make a 20-year sample of a slow dose rich in independent
episodes. Keep the replication step for every future pass.

**Count after W34 (panic-words-1, 2026-11-25).** One mechanism and one gate added to the count
above (summary-6, #191: 101 mechanisms, 29 tested by a strategy, 28 gates): **102 mechanisms, 29
tested by a strategy, 29 gates**; W34 failed (wrong sign), so still one kill-only pass (W32,
killed by R32) and every gated idea dead. Family bar p < 0.10 / 102 = 0.00098.

**Count after W35 (wide-21, 2026-11-25; renumbered from W34 at merge, its card says W34
(provisional)).** One more mechanism and gate: **103 mechanisms, 29 tested by a strategy, 30
gates**; W35 failed (t -0.87 > -2), so still one kill-only pass (W32, killed by R32) and every
gated idea dead. Family bar p < 0.10 / 103 = 0.00097.

**Count after W36 (wide-22, 2026-11-25; ids provisional, parallel lanes may take W36).** One
more mechanism and two more gates (W36 and its replication R36, counted as R32 was): **104
mechanisms, 29 tested by a strategy, 32 gates, two kill-only passes (W32, W36), each killed by
its replication (R32, R36)**; every gated idea dead. Family bar p < 0.10 / 104 = 0.00096.
Both passes were persistent monthly macro doses on a narrow placebo null (SD 0.91-0.94); for
W36 a phase-randomised surrogate family (shown, not gating) was wider (SD 1.10) and ranked the
true t 3 of 41, a miss. Suggestion for the lead (not adopted): for persistent macro doses,
require the rank in both families.
#197 `fx-value-real-1` (merged 2026-11-25) is treated as part of #170's style-book mechanism (a
better currency-value definition for the same book), not a new mechanism, so 104 / 29 stands.

**Count after W37 (wide-23, 2026-11-25).** One more mechanism and gate after W36/R36:
**105 mechanisms, 29 tested by a strategy, 33 gates, two kill-only passes (W32, W36), each
killed by its replication (R32, R36)**; W37 failed (t +0.68, rank 38; post hoc t -0.01 without
its one event that was not public at its listed date, so no effect rather than a wrong sign),
so every gated idea is dead. Family bar p < 0.10 / 105 = 0.00095. In this one event gate the
phase-randomised and random-day surrogate families (shown) agreed with the earlier-dose
placebos on width (SD 1.13 and 1.08 against 1.02; without LuBian random-day 0.94) and on the
verdict (ranks 27 and 30). One gate does not say when the families disagree; gate-null-2
(PR #207, open) studies exactly that.

**Count after W38 and W39 (jst-gates-1, 2026-11-25; carded as provisional ids while #205 was
unmerged; #205 then landed with W37, so W38/W39 stand).** Two more mechanisms and two more
gates, no replication (neither gate passed): **107 mechanisms, 29 tested by a strategy, 35
gates, still two kill-only passes (W32, W36), each killed by its replication**. Family bar p <
0.10 / 107 = 0.00093. W38 is a pooled annual JST gate before 1966; W39 spans both sides of it.
Per jst-autocorr-2, the shift family keeps the returns' own and common autocorrelation (the
outcome is the real one) but not a shifted dose's same-year link to returns, so the card added
a returns-side AR(1) bootstrap under H0 (a pass condition) and phase surrogates with shared
phases (shown). W38 (`consumption-cycle`) fails: t -1.88 and rank 3 of 21. That t holds only
for the same-year dose, which a reader at the start of year t+1 could not have had (annual
consumption is published after the year, and these values are later reconstructions); the
dose of year t-1 gives t -0.57 (lags 2 and 3: -0.04, -0.10). A full pass would still only
have been kill-only (p >= 0.048 against 0.00093). W39 (`bank-capital-premium`, t +0.17) fails
on its sign.

**Count after W40 (wide-24, 2026-11-25; carded as a provisional id while #210 held W38/W39;
#210 landed during the lane, so W40 is the next free id and stands).** One more mechanism and
gate after W38/W39: **108 mechanisms, 29 tested by a strategy, 36 gates, two kill-only passes
(W32, W36), each killed by its replication (R32, R36)**; W40 failed (t +0.38, predicted
negative, rank 24 of 41), so every gated idea is dead. Family bar p < 0.10 / 108 = 0.00093.
W40's dose is a sparse event series (pooled lag-1 acf +0.008), so gate-null-2's proposed "both
families" rule (acf >= 0.8) did not apply; the random-day surrogates (shown) agreed with the
shifted calendars on the verdict (rank 28), as in W37.

## Cyclic doses need another placebo family (wide-21, 2026-11-25)

W35 (`solar-max-recession`) moved a dose with its own cycle (the sunspot cycle, about 132
months) by k = +-19..95 months. Shifts of 4-8 years turn the dose into its own anti-phase, so
those placebos repeat the true pattern with the opposite sign: placebo t median +1.25, 95%
+2.83, max +3.11, against a true t of -0.87 that still ranked 3 of 41. The family measured one
weak cyclic pattern 40 times, not 40 nulls; only the t condition (step 4) kept the rank from
deciding. For the next dose with its own clock (a cycle, a season of variable length), write
into the rule a family that keeps the phase relation random rather than systematic: a
phase-randomised surrogate of the dose (same spectrum, random phases; Theiler et al. 1992
`[memory]`) or a permutation of whole cycles, and keep t >= 2 as a necessary condition.


## Proposed rule, not adopted: a second placebo family for persistent doses (gate-null-2, 2026-11-25)

**PROPOSED, for the lead to adopt or reject; no verdict above changes.** `gate-null-2.md`
simulated known nulls. For a dose with lag-1 autocorrelation phi >= 0.8, the shifted-calendar
rank alone is too liberal: P(rank <= 2 of 41) is 5.4-19% against 4.9%, because neighbouring
shifts are near-copies. At phi 0.8 it is 5.4-7.5%, three of four cells under the 7.3% mis-size
line; it is 7.5-10.7% at 0.9 and 13-19% at 0.98-0.99. The t >= 2 condition keeps the full
gate's false passes at 1-3% with GARCH-t or real returns; with a slow premium in returns they
reach 5.5%. Phase-randomised surrogates stay at 4.0-6.0%.

Proposed: for a dose with lag-1 autocorrelation >= 0.8 at its own step, or with its own cycle,
the rule also names 40 phase-randomised surrogates of the dose (IAAFT if skewed or mostly
zeros). For a near-unit-root dose, detrend or end-match the dose first, or use IAAFT. A pass
then needs t >= 2 and rank <= 2 in both families. The cost is 2-3 points of power at phi
0.9-0.95 and 5-8 at 0.98-0.99.

**Caveats, from the write-up.**

- The 0.8 threshold rests on one cell (7.5% against the 7.3% line, about 0.3 SE).
- "Both" was chosen over the surrogate family alone by a margin within noise. The paired power
  gap at R^2 1%, T 600 is 4.79 points (SE 0.17), 1.2 SE under the card's 5-point line. That
  averages phi 0.9-0.99, an averaging the card did not fix; with phi 0.8 the gap is 4.4, and at
  phi 0.98-0.99 alone it is 5-8 points.
- The card's rule governs, so the recommendation stands, adopted by a margin within noise.

Re-scored on main, no verdict changes: W32 ranks 1 in every family, and the other gates fail
their own t. Surrogates centre the off-centre nulls of W33 and W35. W36 (wide-22, #202; not
re-scored here) had phase rank 3 in its own write-up, so it would have failed "both".

## Count after W41 (wide-25, 2026-11-25)

W41 `cabinet-collapse` (comparative politics: a political-uncertainty premium after mid-term
cabinet starts, 18 developed markets 1976-2022) fails on its sign (t -1.74, predicted > 0;
rank 41 of 41). Count after wide-24's #215 (W40), merged before this one: **109 mechanisms, 29 tested by a
strategy, none passed; 37 gates, two kill-only passes (W32, W36), each killed by its
replication; family bar p < 0.10 / 109 = 0.00092.** The dose is a sparse event series (pooled
lag-1 acf -0.007), so gate-null-2's proposed "both families" rule does not apply; the two
families agree. An event calendar tied to a 3-5 year election clock made the earlier-dose
shifts of 31-53 months lean positive (max +3.39): a political gate should report a
random-month family next to the shifts, as W41 did.

## Count after W43 and W18 (wide-26, 2026-11-25)

W43 `drought-food-margin` (agronomy: Corn Belt drought as an input-cost shock to US food
stocks; a provisional id, W42 is unused, so the lead may renumber) fails on its t (+0.07,
predicted < 0; rank 22 of 41 shifted, 23 of 41 phase surrogates). W18 `elimination-mood`
(wide-8's own id, gated for the first time as a record-closing check) fails (t -0.95, rank 6).
Count after wide-25's #221 (W41), merged before this one: one more mechanism (W43; W18 was
counted since wide-8) and two more gates: **110 mechanisms, 29 tested by a strategy, none
passed; 39 gates, two kill-only passes (W32, W36), each killed by its replication; family bar
p < 0.10 / 110 = 0.00091.** W43's dose is persistent (acf1 0.94), so gate-null-2's proposed
"both families" rule applied; the two families agreed (surrogates wider, SD 1.25 against
1.10). W18's dose is sparse (acf1 -0.001); its shifted null is narrower than normal (SD 0.87).
