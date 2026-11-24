# insure-4: put protection only while trend is in the market

Lane insure-4, 2026-11-24 (night). Branch `insure-4`, draft PR #165. Research only: fake
money, keyless public data (insure-3's cache, nothing new fetched), no change to the gym, the
daily runner or the live strategies. Card: [`cards/insure-4.md`](cards/insure-4.md) (pushed
before any number). Tables: [`results/insure-4.md`](results/insure-4.md). Code:
`lib/insure4.py` (reuses `lib/insure3.py`), tests `tests/test_insure4.py`. Train data only
(nothing after 2025-10-31 parsed). insure-3's "Next" item 2.

## The answer on one screen

**Rule: when `tsmom12` says in, hold the S&P 500 as CBOE's PPUT (index plus a monthly 5%
out-of-the-money put); when out, bills. It is worse than `tsmom12` on Sharpe (0.47 against
0.58, paired z -1.67: "worse than `tsmom12`" by the card's rule, just past the -1.645 line) and
far from the bar (z >= 4.70). It does add the fast-crash cover trend lacks and has by far the
smallest worst loss (19%), but it costs about 2.9 points of growth a year against `tsmom12`:
nearly the whole price of holding the puts always, not half of it.**

| 1986-07..2025-10 | CAGR | Behind holding, pts a year | Sharpe above bills (SE) | Worst loss | Share of each 15% fall avoided | Insurance cost | Premium P |
|---|---:|---:|---:|---:|---:|---:|---:|
| Hold S&P 500 (total return) | 11.1% | - | 0.50 (0.17) | 55% | - | - | - |
| `tsmom12` (cash at bills) | 10.8% | 0.37 | 0.58 (0.17) | 33% | 0.56 | **0.02** | 1.05 |
| PPUT alone | 8.0% | 3.14 | 0.41 (0.17) | 42% | 0.37 | 0.28 | 1.60 |
| **PPUT while trend is in, bills when out** | **7.8%** | **3.29** | **0.47 (0.17)** | **19%** | **0.73** | **0.15** | **1.32** |
| same, 10 bps a side per switch | 7.7% | 3.38 | 0.46 | 19% | 0.73 | 0.16 | 1.33 |
| same, idle cash at 0 | 7.3% | 3.83 | 0.42 | 23% | 0.71 | 0.18 | 1.38 |

Paired Sharpe test against `tsmom12` (above bills, stationary bootstrap of daily excess
returns, 2,000 draws, seed 0): d = -0.110, SE 0.066, **z -1.67** (mean block 21 sessions);
block 63: SE 0.063, z -1.74. Robustness: 10 bps a side z -1.80, cash at 0 z -2.39. Against PPUT
alone +0.06 (z +0.70), against holding -0.03 (z -0.26): no difference shown.

- **Fast crashes: covered.** 1987 -11.0% (trend -33.0%, PPUT -11.0%: trend was fully in, so
  the rule is PPUT); 2020 -6.4% (trend -19.8%, PPUT -11.8%: trend got out partway and the puts
  covered the part it was in). The rule lost less than `tsmom12` in both, so by the card it
  "adds fast-crash cover". Also in the other falls where trend stayed in: 1998 -12% (trend
  -19%), 2010 -8% (-16%), 2011 -11% (-19%), 2025 -11% (-17%). In the slow bear markets it is
  trend (already in bills). Share of each fall avoided 0.73, the highest of the four; on the
  fast cut (<= 92 days, 10 falls) 0.77 against trend's 0.52.
- **Insurance cost: between trend's and the puts'** (0.15 against 0.02 and 0.28; premium 1.32
  against 1.05 and 1.60). Per unit of loss avoided it is about 7 times dearer than trend alone.
  Net of the year after each low it is no better than trend (mean -0.1 against +0.3 log points).
- **Why the prior was wrong.** The card expected the put bill to scale with the time in the
  market (70-75% by the card, measured 82%), i.e. roughly 2 points a year. It cost more: CAGR
  3.29 points behind holding, 2.9 behind `tsmom12`, slightly more than PPUT held always (3.14).
  Diagnostic (computed after the run, no row): PPUT's log return minus holding's was -2.67
  points a year on sessions when trend was in and only -0.20 on sessions when it was out. The
  puts pay off mainly in bear markets, which is when trend is already out; holding them only
  while invested drops the sessions where they paid and keeps nearly all the sessions where
  they bled. Trend and puts insure the same slow falls twice, and only the fast falls are not
  doubled.
- **What it buys.** Worst loss 19% (trend 33%, PPUT 42%, holding 55%) and CAGR / worst loss 0.42
  against trend's 0.33. That is a lower-risk profile, not a better one: the Sharpe is lower.
  Whether trend held at a lower fixed exposure (or vol-targeted) reaches the same worst loss
  at a higher CAGR was not tested here (see Next).

## How sure

- **One history.** 17 falls, two named fast crashes. The crash results are a description.
  The Sharpe verdict rests on z -1.67, just past the card's -1.645 line at block 21 (-1.74 at
  block 63): "worse" is the card's label, but "no better, likely worse" is the honest reading.
  Every robustness form is worse still. Nothing near a positive z, let alone 4.70.
- **PPUT is an index.** No fees, no bid-ask on the puts: a real put buyer pays more. Entering
  mid-month buys the put the index bought at its last roll (third Friday), marked at its price;
  its strike can then be far from 5% out of the money. Only 13 of the 44 switches fell on a
  roll Friday. The 10 bps-a-side robustness (a rough allowance for the put's spread when
  switching) costs 0.1 point a year; the real put cost while held is not modelled beyond the
  index.
- **No look-ahead.** The in/out state is insure-3's `tsmom12` (the record's rule): decided at a
  Friday's close from closes up to it, applied from the next session; the switch happens at
  PPUT's closing level that Friday. Tests: changing every S&P 500 price after a decision Friday
  leaves positions and returns through the next Friday unchanged; PPUT's levels never move a
  position; with the plain total return in place of PPUT the rule equals insure-3's `tsmom12`
  (also asserted on the real data in the run).
- **Order of steps.** Card pushed (a33e2ed), then script and tests pushed (c35d99b), then the
  one run (ab284f2). The one-line diagnostic above was computed after the run and is labelled
  so. insure3.py gained one line (`chk["pos"]`, the window positions); its results are unchanged.
- **Data and terms.** As insure-3: raw CBOE and Yahoo levels stay in the git-ignored cache;
  only statistics are committed.

## Count and bar

- `tries.md`: 3 rows, idea `insure-4`: `tsmom12-pput-bills@insure4` (`variant`, train; file
  convention Sharpe 0.75 against insure-3's `tsmom12` row 0.80), and the two robustness forms.
  Baselines already have insure-3 rows.
- Bar (BAR.md, rows through 2026-11-24 20:01): 3,855 tries, N 1,083 for a new pick, N_eff 500,
  **z >= 4.70**, Bonferroni p <= 1.0e-04. This card's own SE (0.066) applies with the z column:
  z -1.67. **Not selectable; dead as a pick.**

## For the live rule

Nothing changes. Options are outside the paper broker anyway. The record can now say: adding
puts to trend's in-market time fixes trend's fast-crash gap (1987, 2020) and cuts its worst
loss, but costs nearly the full put premium (about 2.9 points a year against trend), because
the puts' payoffs come mostly in bear markets where trend is already in cash. It is a risk
preference with a lower Sharpe, not an edge.

## Next (not started)

1. Control the post hoc question fairly: does `tsmom12` at a fixed lower exposure (or
   vol-targeted, risk-menu-3's `vt-own`) reach a 19% worst loss at a higher CAGR than this rule?
   Needs its own card; would be descriptive (no pick: exposure is a risk choice).
2. Puts only in the first weeks after trend re-enters, or only when implied volatility is low
   (cheaper puts): each a new variant against the bar, with little room left (z -1.67 to cover
   before 4.70). Low priority.
