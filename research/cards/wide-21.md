# wide-21 card: `solar-max-recession`, do US stocks earn less after high solar activity?

Lane wide-21, written 2026-11-25, **before any return was read for this rule** (card pushed
first; the commit time is in git). Field: solar physics x Jevons' sunspot theory of the trade
cycle. Candidate S1 of `research/wide-21.md`, step 2. Gate **W34** (the next free id on
`main`'s `gate-null.md`; provisional: a parallel lane may take the same number, the lead
renumbers).

## What was seen before this card (disclosed)

- SILSO monthly sunspot file, format probe: 3,334 rows, 1749-01 .. 2026-10; the first and last
  three rows were printed (three 2026 values: after the cut, never used).
- Shiller `ie_data.xls` (cache, 2026-11-12, from survey-4), format probe: header rows (Date, P,
  D, E, CPI, ...), 1,833 dated rows, the last dated 2023.09. No price, dividend or return value
  was read or computed.
- The literature only as search summaries (below).

## Hypothesis

Jevons (1875-1882) claimed commercial crises recur with the sunspot period. Gorbanev (MPRA
paper 40271, 2012; Journal of Scientific Exploration 2015) reports that G7 recessions start
disproportionately in the three years around and after solar maxima (from 1965 nearly three
fifths of them), and that the pattern is hard to reject as chance `[search summary]`. If high
solar activity raises the chance of a recession, and nobody prices the sun, US stocks earn
less in the months after high activity. **Prediction: b < 0.** Warning written now: Gorbanev
(MPRA 102163, 2020) placed the 2008-09 and 2020 crises near solar minima `[search summary]`,
so the claim's own author has wavered on the sign; the card tests the published 2012/2015
form.

Filters (wide-11 F1/F2, #109): F1 passes (a): the sunspot number is public, but the recession
it is said to cause is an unscheduled shock and no investor prices sunspots. F2 passes outright:
the sun does not answer prices, so the placebo calendars may move both ways (gate-null step 1).

## Data (keyless)

- Sunspots: SILSO (Royal Observatory of Belgium), monthly mean total sunspot number, version
  2.0, `https://www.sidc.be/SILSO/INFO/snmtotcsv.php`, fetched once into the shared cache
  `wide-21/silso/2026-11-25/SN_m_tot_V2.0.csv` (write-once, manifest), read as untrusted data
  with `python -I`. Licence CC BY-NC 4.0: only statistics are committed, never the series.
  Months after 2025-10 are never read. Publication lag: SILSO publishes a month's provisional
  mean on the first days of the next month; the dose of month m is used only for outcomes that
  start after month m+1 begins. Caveat fixed now: version 2.0 (2015) recalibrated the whole
  history (a level rescale, not a timing change), and recent months are provisional for a
  while: a small vintage effect on the dose size, none on its timing.
- Stocks, gate: Shiller's monthly S&P 500 (`ie_data.xls`, cache 2026-11-12): P = the month's
  average of daily closes, D = the annual dividend rate. A month whose D cell is not a number
  uses the last reported D. Months 1871-01 .. 2023-09 (the file ends there; nothing after
  2025-10-31 can be read).
- Stocks, shown: `harness.load_history("train")` (GSPC price index from its first cached day;
  SPY, QQQ, TLT, GLD, BTC, ETH), no bar after **2025-10-31**.

## Rule (frozen)

- Dose x(m) = (1/12) sum_{j=0..11} SN(m - j) / 100 (trailing 12-month mean sunspot number, in
  hundreds). NaN unless all 12 months exist.
- Outcome y(m) = ln((P(m+2) + D(m+2) / 12) / P(m+1)): the total return from the average price
  of month m+1 to that of month m+2. Every day averaged into P(m+1) and P(m+2) lies after the
  dose x(m) is published.
- Dose months m from 1871-01 to the last month with y defined (2023-07).
- Statistic: OLS y(m) = a + b x(m); t of b with Newey-West standard errors, 12 lags (monthly
  rows; Shiller's averaged prices add an MA(1), the dose is persistent).
- Predicted sign: **b < 0**.

## Placebo null (the decider, `research/gate-null.md`)

The sun does not answer prices: shifts both ways are allowed. x_k(m) = x(m - k), k in
+-{19, 23, 27, ..., 95} (step 4, 20 values each side): **40 placebos**. The mechanism's clock is
the solar cycle of about 11 years (132 months, 9-14 years per cycle); every |k| <= 95 is at
least 37 months from both 0 and 132, so no placebo is a lagged copy of the true dose in phase,
and the family covers phase shifts of about 50-260 degrees. For k < 0 the placebo needs sunspot
months after the cut for the last |k| rows: those rows drop (never read past 2025-10); for
k > 0 the sunspot record before 1871 (from 1749) supplies the early rows. Same function, same
code path, a `shift` argument.

## Gate (pass only if all hold)

1. b < 0.
2. t <= -2.
3. The true t ranks among the 2 lowest of 41 (empirical one-sided p = rank / 41 <= 0.049).

**Kill-only** (gate-null step 7): about 14 solar cycles (cycles 11-24) cover 1871-2023, so
about 14 independent swings of the dose; the smallest p a rank can show is 1/41 = 0.024, far
above the family bar (p < 0.10 / 102 = 0.00098) and the register's Bonferroni 9.9e-5. A fail
kills the idea; a pass says only "not dead yet".

**Replication fixed now, run only if the gate passes (R34)** (gate-null's "keep the
replication step for every pass"): Jorda-Schularick-Taylor R6 (cache `data-long-4/jst`, read
with the repo's `long_macro.parse_jst`), the 16 countries other than the US, annual equity
total return (`eq_tr`) in year t+1 as ln(1 + eq_tr) on the calendar-year-t mean sunspot number
/ 100, country intercepts, Driscoll-Kraay t over years, 2 lags, years t 1871-2019; prediction
b < 0, t <= -2, rank among the 2 lowest of 41 with placebos shifted k years, k in
+-{2..9, 13..20, 24..27} (20 each side; multiples of the cycle, 10-12 and 21-23, left out).

## Shown, not gating

- Gorbanev's window as an indicator: 1 in months from 12 months before to 24 months after a
  solar maximum (maxima = peaks of SILSO's 13-month smoothed series, found in the whole file:
  **look-ahead in the timing**, so shown only).
- Post-Gorbanev months only: dose months 2012-01 .. the end, GSPC month-end closes (Shiller
  ends 2023), y = ln(C(end of m+1) / C(end of m)) price only, NW 12.
- GSPC month-end, same y as above, from its first cached month to 2025-09 (dose months).
- 12-month horizon: y12(m) = ln of P(m+13) over P(m+1) plus D/12 summed, NW 18.
- Phase instead of level: dose = x(m) - x(m - 12) (rising versus falling activity).
- Crash timing: a linear probability, z(m) = 1 if min P over months m+1..m+12 is at most 0.8 x
  P(m+1) (a 20% fall within a year), NW 18; predicted b > 0.
- Live assets, month-end y as for GSPC: SPY, QQQ, TLT, GLD, BTC, ETH (from their first cached
  month).
- The null's width: SD of placebo t, share with |t| >= 2, 5/50/95% quantiles, extremes.

## Power and my guess (written before any number)

Shiller's monthly return sd is about 4% (a bit less with averaged prices); x has a sd near
0.55; with about 1,830 rows SE(b) is about 4 / (0.55 x 43) = 0.17% a month per unit, about
0.2% with NW. If high solar activity cost about 5% a year from the minimum (x near 0.1) to the
maximum (x near 1.5), b is about -0.3% a month per unit and t about -1.5. Guess: b of either
sign, |t| < 1.5, a middle rank, placebo t SD 1.2-1.7 (a cyclic dose against long equity swings:
about 14 independent draws). Prior of a pass: 1%.

## On the outcome

Pass: "not dead yet"; run R34 at once (fixed above) and report both. Fail: dead, one `screen`
row in `research/tries.md` (descriptive, not selectable); the solar-cycle class joins W16
(storms) and W3 (moon) as dead.
