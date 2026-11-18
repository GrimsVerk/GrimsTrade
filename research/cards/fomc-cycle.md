# fomc-cycle: hold the stock trend slots only in even weeks of the FOMC cycle

Source: Cieslak, Morse and Vissing-Jorgensen, "Stock Returns over the FOMC Cycle", Journal of
Finance 2019 (`survey-2.md`, S1), the top pick of survey-2's ranking note (pushed before this
card). Written 2026-11-18, lane survey-2, before any test or number of this card. Seen before:
every earlier result in `tries.md`, among them `opex-pin` (idle cash into stocks in the
option-expiry week: failed, behind its placebo week), `dip-rsi2` (SPY bounces after drops: real,
small, faded), and the first survey's note that the pre-FOMC drift is gone after 2015. No
return of any asset has been split by FOMC-cycle week by me or, as far as `tries.md`,
`ideas.md` and the other lanes' branches show, by any earlier run. The paper's own numbers
(1994-2013) are in `survey-2.md`.

## Claim

Since 1994 US stocks have earned their whole excess return in weeks 0, 2, 4 and 6 of the FOMC
cycle (counted from each scheduled announcement day) and about nothing in weeks -1, 1, 3, 5.
The paper's reading is a risk premium for news coming out of the Fed, which decides and leaks on
a two-week rhythm set by Board meetings. If that holds after the paper's sample, the stock slots
of the trend book carry the same return in half the time: same mean, less variance, higher
Sharpe.

## Why it might work

- The calendar is fixed a year ahead and the cycle is weekly: it fits weekly decisions and
  next-open fills exactly, and toggling SPY/QQQ costs 4 bps a round trip.
- The claimed effect is large (about +10 bps a day over odd weeks) against those costs, and was
  found in three sub-periods, before 1994, abroad, and in a three-year holdout by the authors.
- Our train holds 2017-2025, nine years after the published sample (which ends 2016): a
  post-publication test of a published rule.

## Why it might not

- Published anomalies lose about half after publication; the pre-FOMC drift (week 0's first
  day) is reported gone after 2015.
- Half of the even-week return is said to be bounces after declines: the "Fed put" may be
  priced faster now, and dip buying is small here.
- 2017-2025 holds about 70 FOMC cycles: a real but smaller effect may not reach the bar.
- The gate halves the time in stocks; if odd weeks earn anything, the gate loses return and
  Sharpe can fall.

## Data

- Prices: the six assets, the 8 other ETFs, the four indexes, as every run (train only).
- FOMC scheduled meeting dates 1994-2025, public, keyless: federalreserve.gov
  `monetarypolicy/fomchistorical{1994..2020}.htm` and `monetarypolicy/fomccalendars.htm`
  (2021 on), downloaded 2026-11-18 to `<cache_root>/downloads/survey-2/fomc/`, parsed with
  `python -I` by `lib/survey2_fomc.py` into `<cache_root>/derived/survey-2/fomc.csv`. The parser
  prints only counts and the first and last date.
- Scheduled meeting = a heading "... Meeting" without "(unscheduled)". Conference calls and
  notation votes are left out. The 2020-03-17/18 meeting, cancelled after the unscheduled one on
  2020-03-15, is kept: it was on the published calendar, and the calendar is what a rule knows
  in advance. Day 0 = the last day of the meeting (the announcement day).

## Cycle labels (fixed, from the paper)

Days are weekdays (Monday to Friday; holidays count as weekdays, as in the paper). For a date
`t`:

- if the next day 0 is 1 to 6 weekdays after `t`: `t` is in week 0 when it is 1 weekday
  before (day -1), else in week -1 (days -6 .. -2);
- otherwise, with `k` = weekdays since the last day 0 (day 0 itself: `k` = 0): even for `k` in
  0..3, 9..13, 19..23, 29..33; odd for 4..8, 14..18, 24..28; `k` >= 34 (the paper's rare
  "week 7", dropped there) counts as odd here;
- dates before the first meeting in the file have no label.

## Rule (fixed, no fitted parameter)

- Base: `tsmom12` on the six assets, decided weekly as always.
- Gate, decided daily (the calendar is known in advance, as `auction-concession`): at a
  decision after the close of session `d`, the stock slots (SPY, QQQ) keep their `tsmom12`
  weight only if the next session of that asset (`d+1`) is in an even week; else that weight is
  cash. Bonds, gold and coins are untouched. With next-open fills a slot then holds the
  sessions of even weeks from their open to the next open. A session without a label: no gate.

## Variants (all that will be run)

1. `even-gate` (primary): as above.
2. `even-overlay`: `tsmom12` unchanged; when the next session is in an even week, the idle
   cash (1 minus the base weights) is added in equal parts to the eligible stock ETFs (SPY,
   QQQ).
3. Placebo, logged as `robustness`, never selectable: `odd-gate`, the gate with even and odd
   swapped.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, `odd-gate`, and an event study (descriptive, no
`tries.md` row) for SPY and QQQ: the mean daily log return (bps) in even and in odd weeks and
the even-minus-odd spread with its t (Welch), for 1994-2013 (the first draft's sample),
2014-2016 (the authors' holdout) and 2017-01-01 to the end of train (after publication); both
close-to-close (the paper's measure) and next-open to next-open (what our fills earn: the
interval a decision after session `d` holds, labelled by `d+1`).

## Out-of-universe

- The 8 other ETFs as a `tsmom12` book, the gate on the stock ETFs IWM, EFA, EEM (the paper
  reports the cycle in non-US developed and emerging markets).
- The four indexes as one `tsmom12` portfolio (`idx`), the gate on all four (all are stock
  indexes) from 1994; labels by the weekday date, no time-zone shift (the paper uses the next
  day for non-US markets; accepted, it can only weaken the gate there).
- Coins: not applicable.

## Pass bar

The default in `protocol.md` for `even-gate` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 61 = 0.00164**: wide-1's list of 54 plus survey-2's 7 candidates
   (the `wide-*` lineage's way of counting; see `survey-2.md`).
2. Ahead of the twin in at least 4 of the 5 eras.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive on both applicable out-of-universe sets (ETFs, indexes).
5. Beats equal weight on Sharpe.
6. (card) Not behind `tsmom12` on Sharpe over 2017-01-01 to the end of train (after the
   published sample).
7. (card) SPY's close-to-close even-minus-odd spread over 2017-01-01 to the end of train is
   positive with t >= 2.
8. (card) `even-gate` beats its placebo `odd-gate` on Sharpe.

`even-overlay` is read on the same bars 1-6 and 8 (with `odd-gate` as placebo); it is a second
try, so either passing counts against the same family bar.

Held-out year: once, for the variant that passes (if both, `even-gate`), only if all bars pass.

## My guess before any number

Chance it passes: 5%. SPY spread after 2016: 0 to +6 bps a day (the paper: about +10 to +14).
Difference to the twin: -0.03 to +0.05 Sharpe for `even-gate`; `even-overlay` within +-0.02.

## Result

See `results/fomc-cycle.md` once tested.
