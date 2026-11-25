# wide-22 card b: R36, the replication of W36 `grid-load-premium` on 1926-1955 (spliced NBER series)

Lane wide-22, written 2026-11-25 **after** the W36 gate number (W36 passed, kill-only:
`results/grid-load-premium.md`) and **before any number of this replication** (card pushed
first; the commit time is in git). Same role as `cards/parked-gates-1b.md` for R32.

## Why a second card

`cards/wide-22.md` fixed R36 on FRED `M01128USM247NNBR` (NBER Macrohistory m01128, electric
power production) "to the earlier of the series' end and 1955-12", and said: "If the series
cannot be fetched keylessly or has fewer than 240 usable months, R36 is reported as not
runnable." Fetched 2026-11-25 21:13 UTC (keyless `fredgraph.csv`): the series covers only
1919-01 .. 1938-12 (240 rows), so the usable usage months 1926-04 .. 1938-12 are 153: **R36 as
written is not runnable** (reported in the write-up). FRED's notes for the same NBER indicator
say it "is presented as two variables": 1919-1938 (`M01128USM247NNBR`) and 1936-1957
(`M0128AUSM247NNBR`, m01128a, fetched the same night; 1936-01 .. 1957-01, 253 rows; only the
date range and the first value of each file were printed, no growth rate or return computed).
This card splices the two on growth rates and keeps everything else of R36 unchanged.

## Rule (frozen)

- P1(m) = `M01128USM247NNBR` (billion kWh; public-use production plus electric railways and a
  few own-use plants), P2(m) = `M0128AUSM247NNBR` (billion kWh; public-use production of
  utilities and public projects, excluding railways and industrial own-use plants).
- Dose g(m) = 100 x ln(P1(m) / P1(m - 12)) for usage months m <= 1938-12, and
  100 x ln(P2(m) / P2(m - 12)) for m >= 1939-01 (each year-on-year ratio inside one series;
  the two coverage definitions never mix inside a ratio).
- Outcome y(m) = French `Mkt-RF` of month m + 3 (percent), as W36.
- Rows: usage months 1926-04 .. 1955-12 (outcomes 1926-07 .. 1956-03), about 357 rows.
- Statistic: OLS y = a + b g, Newey-West 3 lags (the W36 code path, `wide22.fit`).
- Placebos: earlier doses only, g(m - k), k = 25, 27, ..., 103 (40), each on its own rows.
- **Pass needs: b < 0, t <= -2, rank among the 2 lowest of 41.** A fail kills W36 (as R32
  killed W32).

## Shown, not deciding

- Without the Depression: usage months 1934-01 .. 1955-12 (the 1929-1933 collapse is one
  episode that could carry the whole slope).
- Each piece alone: 1926-04 .. 1938-12 (P1) and 1939-01 .. 1955-12 (P2).
- Phase-randomised surrogates of the spliced g (seed 22), rank of the true t.
- The null's width (SD, share |t| >= 2, quantiles, extremes).

## Honest limits, fixed now

Total utility production, not industrial sales (no keyless monthly industrial series of that
age is known to me); the industrial share of utility sales then was large but not all
`[memory]`. About 30 years: the 1929-1933 collapse, 1937-38, the war boom and demobilisation
(1945-46), 1948-49, 1953-54: about 6 independent swings. Kill-only like W36: a pass would say
"not dead yet" twice, not that the premium is real at the bar (p < 0.10 / 104 and the
register's 9.9e-5 are out of reach of a 41-rank design).

## My guess (before any number)

The Depression gives a huge swing in g (-20 to -30 points in 1931-32 `[memory]`) followed by
very high returns (1932-33) and a recovery in g; that pattern alone favours b < 0. Guess: b < 0,
t between -2.5 and -0.5, rank 1-10; without 1929-1933, |t| < 1.5. Prior of a pass: 30%.
