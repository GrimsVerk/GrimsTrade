# wide-30 card: `payout-ratio`, does the US market earn more after a high dividend payout ratio?

Lane wide-30, written 2026-11-26 (about 08:38 UTC), **before any return was read for this
rule** (card pushed first; the commit time is in git). Field: accounting (payout policy and
earnings measurement). Candidate Q1 of `research/wide-30.md`. Gate **W47** (W46 was
wide-29), replication **R47** fixed below. No second gate.

## What was seen before this card (disclosed)

- Robert Shiller's `ie_data.xls` (monthly S&P composite price, 12-month dividends D and
  earnings E, CPI, long rate; 1871 on), cached 2026-11-12 under `shiller/2026-11-12/` and read
  by other lanes (long-macro, insure-3, eu-6/7) for price and yield features. **No lane formed
  D/E**; this lane has not opened the file tonight. No ratio, growth or dose was computed.
- Ken French monthly and daily factors (cached 2026-11-12): read by other lanes many times,
  never against the payout ratio.
- A FRED download for another candidate failed (no connection from the script); no data seen.

## Hypothesis

Dividends are smooth and earnings are not, so a high payout ratio D/E marks earnings that are
temporarily low (a slump in profits that the market prices as risk). Lamont (1998, "Earnings
and expected returns") found that the payout ratio forecasts excess returns with a **positive**
sign once the dividend yield is held fixed `[memory]`. **When D/E is high relative to its
own past five years, the US market's excess return over the next twelve months is higher:
b > 0.** Published (post-sample 0 for 1947-1994; the gate's 1991-2024 rows overlap Lamont's
sample by four years).

Filters (wide-11): F1 passes as a premium (b), a state. F2 passes only with controls: D/E
falls in booms and rises in busts, and so follows past returns; the gate carries the
market's past 12-month return, last month's return and its realised variance; placebo
calendars use earlier doses only.

## Data (keyless, cached)

- Shiller `ie_data.xls`, sheet `Data`: for month m, D(m) and E(m) (the file's 12-month
  trailing dividend and earnings columns). Months with D or E missing, zero or negative are
  missing. **Dating**: S&P reports quarterly earnings up to about two months after a quarter
  ends, and the file interpolates quarters into months, so month m's E uses quarter-end
  values up to two months ahead; **row m enters at the end of month m+4** (two months of
  interpolation plus two of reporting). The file is the latest vintage; S&P's past earnings
  are not known to be revised in substance `[memory]`.
- Returns: French factors, monthly `Mkt-RF` and daily `Mkt-RF`, up to **2025-10**.

## Rule (frozen)

- **Dose.** P(m) = ln(D(m) / E(m)); H(m) = P(m) minus the mean of P over months
  m-60 .. m-1 (five-year detrended, past only). Defined where all 61 months are present.
- **Outcome.** y(m) = Mkt-RF(m+5) + ... + Mkt-RF(m+16), % (twelve months after entry).
- **Controls**: c12(m) = sum of Mkt-RF over m-7 .. m+4; c1(m) = Mkt-RF(m+4); rv(m) = ln of
  the sum of squared daily Mkt-RF over m+2 .. m+4. Constant.
- **Rows.** m = **1991-01 .. 2024-06** with H, controls and y defined (402 months if all are).
- **Statistic.** OLS of y on H, c12, c1, rv, constant; t of b with Newey-West (Bartlett) 12
  lags (`gatepower.dk_fit`); b in % over twelve months per unit of H.
- **Predicted sign: b > 0.** Ranks are taken on t (the most positive t ranks 1).

## Placebo nulls (as wide-28 / wide-29)

- **Shifted family**: H_k(m) = H(m - k), k = 25, 27, ..., 103 (40, odd); same rows and
  controls.
- **Surrogate family**: 40 surrogates of the full H series, `gatenull2.surrogate_doses`,
  seed 2747: phase, or IAAFT if the dry run shows |end - start| of H above one SD of H. The
  family gates if the dry run's lag-1 acf of H is 0.8 or more; otherwise shown only.

## Gate (pass only if all hold)

1. b > 0.
2. t >= 2.
3. t ranks among the 2 highest of 41 in the shifted family **and** (when gating) among the
   2 highest of 41 in the surrogate family.

**Kill-only** (gate-null step 7): smallest p a rank shows is 1/41 = 0.024, above the family
bar (0.10 / 114 = 0.00088 with this card) and the register's 9.8e-5.

**Replication R47, fixed now, run only if the gate passes** (earlier, non-overlapping
years): the same rule on rows m = **1932-01 .. 1989-12** (outcomes end 1991-04, before the
gate's first outcome month 1991-06), against the same 40 surrogates. Pass: b > 0, t >= 2,
t among the 2 highest of 41. (R47 overlaps Lamont's own sample: it checks the gate's
stability, not post-publication life.)

## Shown, not gating

- Horizons 3 months (NW 3) and 6 months (NW 6); no controls; without rv.
- With the log dividend yield ln(D/P) at entry as a further control (Lamont's form).
- Halves: rows 1991-01 .. 2007-12 and 2008-01 .. 2024-06; without rows 2008-07 .. 2010-06
  (the 2008-09 earnings collapse, when E nearly vanished and D/E spiked).
- The null's width in both families.

## Power and my guess (written before any number)

Twelve-month excess returns have an SD near 16%; the dose is slow (acf near 0.98) and its big
moves are three recessions (2001-02, 2008-09, 2020), so the result rests on a handful of
stretches, each one a recession followed by a rally, which the controls only partly absorb.
**Guess: b positive, t between +0.5 and +2.5, middle-to-high ranks; pass 5%.**
