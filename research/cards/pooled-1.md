# pooled-1: are the near-miss trend variants a small real edge, pooled over 41 markets?

Lane `pooled-1`, written 2026-11-24 **before any number of this card is computed** (no variant
has been run on any of the markets below in this lane; data spans were read, nothing else).
Research only: fake money, files already in the data cache, no change to the gym, the daily
runner or the live strategies. Train data only: nothing after 2025-10-31 is parsed (the held-out
year from 2025-11-11 is untouched).

## Question

Several variants of `tsmom12` led it on the primary test (six live assets, 1994-2025) by about
one paired standard error or less: noise there, and one 30-year sample can never settle them.
**Pooled over many markets and long history, is any of them a real, if small, improvement over
plain 12-month trend on the same market, or are they all zero?**

## What was already run out of universe (step 1; nothing below is repeated)

| Variant (card) | First defined | In-sample lead on the six | Already out of universe | New here |
|---|---|---:|---|---|
| `e4` (`cards/ensemble-tsmom.md`) | weight = share of 30/91/182/365-day returns > 0 | +0.05 (p 0.21) | gym, per set: 8 other ETFs (book) +0.02, 6 other coins (book) +0.14, GSPC 1962-93 +0.10, N225 -0.02, FTSE -0.12, GDAXI +0.17 | US 10 industries 1927-2025, 10 more developed and 10 wider indices, per-ETF pairs; the pooled test |
| `or3-12` (`cards/fast-reentry.md`) | held if the 365-day OR the 91-day return > 0 | +0.01 (1994-2025), +0.08 since 2003; one of 98 cells (`trend-tune.md`) | US 11 series and 13 developed indices, scored only on 25% falls (insurance, rebound), never on Sharpe | every market, Sharpe; the pooled test |
| `arm3-12` (`cards/fast-reentry-2.md`) | exit as `tsmom12`; after an exit, re-enter when the 91-day return turns positive (state machine of `lib/fastreentry2.py`) | not scored on Sharpe | as `or3-12` (falls only) | every market, Sharpe; the pooled test |
| `vt-own-70-x`, `vt-own-26-x` (`cards/risk-menu-3.md`, #110) | `tsmom12` sleeve x min(1, k_d / sigma52), expanding-window k for a mean share T = 0.70 / 0.26, monthly reset, 24-month warm-up at T | +0.10 / +0.03 (1.04 / 0.97 vs 0.94) | nothing | every market; the pooled test |
| `tv40` (`cards/trend-vol.md`) | [365-day return > 0] x min(1, 0.40 / vol20) | -0.01 (p 0.57) | as `e4` (ETF book +0.01, coin book +0.10, indexes 0.00) | as `e4` |
| `fade-28` (`cointop-1.md`, Part B/C) | held while 365-day AND 28-day return > 0 | +0.04 (p 0.30), coin slots only | 6 other coins +0.01, BTC/ETH alone | every non-coin market; the pooled test |
| `stop-0.25` (`cointop-1.md`) | held while 365-day return > 0 AND log(close / 365-day high) / EWMA vol (halflife 60) >= -0.25 | +0.04 (p 0.33), coin slots only | 6 other coins -0.03 | as `fade-28` |

Also checked, not in this card: `trend-where` / `trend-where-long` (where-vol, where-dd: a
per-asset yes/no, already run on the ETF, coin and index sets and on long bonds and gold),
`trend-tune` (the 98-cell grid on the six), `insure-2` (only `tsmom12`, falls). `breadth-28`
needs the coin book and cannot exist on other markets. None of the eight has had a pooled
paired Sharpe test.

## Variants, frozen (no retuning)

The eight rules above, exactly as first defined: lookbacks in calendar days (91 = 3 months as
`trend_tune.days_of(3)`), `vol20` = sqrt(mean of the last 20 squared log returns x 252), EWMA
volatility as `common.vol_series` (halflife 60 sessions, 252 a year), own-vol sigma = standard
deviation (ddof 1) x sqrt(52) of the sleeve's 52 complete Monday-Sunday weekly sums of daily
returns before the reset day, k solved by bisection as `riskmenu3_run.solve_k`, a drifting share
between resets, 5 bps on the traded notional at a reset. Twin: `tsmom12` (held while the 365-day
return > 0). Every rule is applied to one market at a time (one slot, the rest in cash).
`fade-28` and `stop-0.25` were coin-slot rules; here they are carried unchanged to stocks,
bonds and commodities, so this tests them as general rules, not their coin effect. `tv40`'s cap
binds only when 20-day volatility exceeds 40%, which on stock indices is rare and mostly inside
crashes when `tsmom12` is often already out: its differences are expected to be near zero
mechanically, and a pooled zero would mean "no edge outside very volatile assets", not a test of
its coin effect.

## Markets (41, fixed now)

| Group | Markets | Data | Span (first day; last 2025-10-31) |
|---|---|---|---|
| US10 | Ken French 10 industries (value weighted) | daily total return, USD | 1926-07 |
| DEV13 | insure-2's 13 developed headline indices: Japan, Canada, UK, Australia, Hong Kong, Germany, Singapore, France, Switzerland, Belgium, Netherlands, Austria, Spain | Yahoo daily closes, local currency, price (DAX total return) | 1965 to 1993 |
| WIDE10 | insure-2's 10 more: Italy, New Zealand, Israel, Korea, Taiwan, India, Brazil, Mexico, Malaysia, Indonesia | as DEV13 | 1990 to 2003 |
| ETF8 | the harness's other ETFs: IWM, EFA, EEM, IEF, LQD, VNQ, DBC, SLV | dividend-adjusted daily closes | 2000 to 2006 |

Left out, and why: the six live assets and their index histories (the selection set; GSPC is
SPY's index), the US market (the industries' weighted sum), the three French regions and
Developed ex US (the same countries again in USD), the six other coins (in cointop-1's
292-coin selection set, and only eight years). Data is not cleaned (the layout check found 3
daily moves above 25% in 23 indices: Hong Kong 1, Brazil 2); price indices miss dividends and
high-inflation markets trend in local currency; both affect the variant and its twin alike.

## Engine (one market, paper series)

- Decisions each calendar Friday from the closes dated on or before it (`tt.paper`'s rule). A
  market is eligible once it has 252 bars and a defined 365-day return.
- **Fill one session late**: a position decided on Friday's close is traded at the close of the
  next session and earns from the session after. Stricter than the paper series (Friday's close)
  and the gym (next open); the same for the variant and its twin.
- 2 bps a side on every change of position (insure-2's index cost), cash earns 0.
- Weekly returns: daily returns compounded to weeks ending Friday. Sharpe = mean / std x sqrt(52).
- Scored window per market: from the first session `tsmom12` could earn to 2025-10-31, the same
  weeks for all nine rules.

## The pooled test (stated now)

- Per market m and variant V: d_m = Sharpe(V on m) - Sharpe(`tsmom12` on m), same weeks.
- **Pooled edge D_V = the equal-weight mean of d_m over the 41 markets.**
- **Standard error: a joint circular block bootstrap of calendar weeks**: one calendar of every
  Friday 1927-2025; blocks of 52 weeks drawn with replacement, the same draw applied to every
  market (so correlation between markets and within a year is kept); each market's Sharpes
  recomputed on its own weeks in the draw; D recomputed. 2,000 draws, seed 0. SE = standard
  deviation of the draws. z = D / SE; 95% interval D +- 1.96 SE (percentile interval shown too).
  Blocks of 13 and 104 weeks are reported as a check, not used for the verdict.
- Shown, not deciding: D and its SE per group; markets with d_m > 0; the same pool on weeks
  before 1994-02-01 only (markets with at least 260 scored weeks there), which lies wholly
  outside the primary test's window; the correlation of each variant's weekly returns with its
  twin's.

## Pass bar, verdicts (per variant)

Deflation for the variants tested here: 8 rules, Bonferroni one-sided at 0.05 / 8 = 0.00625,
**z >= 2.50**.

- **"Real small edge"**: z >= 2.50, AND D > 0 in at least 3 of the 4 groups, AND D > 0 before
  1994.
- **"Selectable candidate"** (the project bar, `research/register/BAR.md`, rows through
  2026-11-19 00:30: 3,130 tries, N = 486 effective, DSR 0.95 needs **z >= 4.69**, Bonferroni
  p <= 1.0e-4): pooled z >= 4.69 plus the conditions above. Even then nothing goes live from this
  lane: it would need its own card on the primary test and the held-out year.
- **"Killed"**: the upper end of the 95% interval below +0.03 (no edge of +0.03 Sharpe per
  market or more), or z <= -2.50 (worse than its twin).
- **"Still open"**: neither.

Per-market Sharpe differences are on single assets (Sharpe 0.3-0.6), not the six-asset book
(1.05), so a per-market d is not on the same scale as the leads in the table above.

## Power (before the numbers)

The SE of D depends on how correlated the per-market differences are, which is measured only by
the run. Prior, from earlier single-index runs (e4's 90% ranges on N225, FTSE, GDAXI: a paired
SE of about 0.08 for a close rule over 35 years, scaled with 1 / sqrt(years)) and these spans
(about 1,940 market-years):

| Correlation of d between markets | SE of D | Edge found 80% of the time at z 2.50 | at z 1.645 | at z 4.69 |
|---:|---:|---:|---:|---:|
| 0 | 0.013 | +0.04 | +0.03 | +0.07 |
| 0.1 | 0.027 | +0.09 | +0.07 | +0.15 |
| 0.3 | 0.044 | +0.15 | +0.11 | +0.24 |
| 0.5 | 0.056 | +0.19 | +0.14 | +0.31 |

So the pool can see a per-market edge of about +0.05-0.10 only if the differences are close to
independent across markets; a common crash calendar makes them correlated, and then it sees
+0.15 or more. Kill (upper end below +0.03) needs D clearly below zero at these SEs. The result
reports the realised SE and the edge it detects at 80% for each variant.

## Controls and checks

- Look-ahead tests (`tests/test_pooled1.py`): every rule's Friday decisions are unchanged when
  all later bars are removed; the one-session fill; own-vol's share uses only earlier sigmas;
  `arm3-12` leaves at every `tsmom12` exit; a variant identical to its twin gives D = 0 in every
  draw.
- Plumbing run on random prices (41 random walks on the same calendars): D near 0, z inside
  about +-2 for every variant. Reported, then the real run, once.

## Output and logging

- `research/pooled-1.md` (verdict per variant), `research/results/pooled-1.md` (tables), code
  `research/lib/pooled1_core.py` (engine, numpy only) and `research/lib/pooled1.py` (data, run).
- `research/tries.md`: per variant one `variant` row for the pooled test (`<v>@pooled-41`;
  Sharpe cell = mean per-market Sharpe, weekly with sqrt(52)); per market and rule one
  `robustness` row (8 variants and `tsmom12` x 41 markets). `research/ideas.md` lines for the
  variants touched.
