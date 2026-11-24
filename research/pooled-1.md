# pooled-1: are the near-miss trend variants a small real edge, pooled over 41 markets?

Lane `pooled-1`, 2026-11-24 (night). Branch `pooled-1`, draft PR #142. Research only: fake
money, files already in the data cache, no change to the gym, the daily runner or the live
strategies. Train data only: nothing after 2025-10-31 parsed, held-out year untouched. Card
(pushed before any number, amendment 1 after the plumbing run and before the real run):
`cards/pooled-1.md`. Tables: `results/pooled-1.md` (+ `.json`); plumbing on random walks:
`results/pooled-1-plumbing.md`. Code: `lib/pooled1_core.py`, `lib/pooled1.py`; tests
`tests/test_pooled1.py`. One real run.

## The answer on one screen

**None of the eight near-misses is shown to be a real edge over plain 12-month trend. Two are
killed (`tv40`, `fade-28`). The re-entry rules (`or3-12`, `arm3-12`) show nothing beyond what
holding more often gives on any drifting market. Two stay open with a positive lean: `e4`
(ensemble of four horizons) and `vt-own-70-x` (own-vol targeting at 70%), both about 1.4 to 1.6
standard errors, far below the deflated bar. The pool sees a per-market edge of about +0.13 or
more for the price rules; it cannot see +0.05. More stock markets would not change that: the
markets fall together, so they count as only a few independent samples.**

Per market: Sharpe of the variant minus Sharpe of `tsmom12` on the same market and weeks. D = the
mean over 41 markets (10 US industries since 1927, 13 developed and 10 other stock indices, 8
ETFs). SE from a joint bootstrap of calendar years (52-week blocks), which keeps the
correlation between markets.

| Variant | Lead on the six (in sample) | Pooled D (95% range) | z | Groups > 0 | Before 1994 (17 markets) | Drift-only null (mean) | D beyond drift | Verdict (card) |
|---|---:|---|---:|---:|---|---:|---:|---|
| `e4`, four horizons | +0.05 | **+0.063** (-0.017..+0.142) | +1.55 | 4 of 4 | +0.086 (z +2.05) | +0.022 | +0.041 | still open |
| `vt-own-70-x`, own-vol 70% | +0.10 | **+0.022** (-0.009..+0.053) | +1.37 | 3 of 4 | +0.049 (z +1.97) | -0.012 | +0.033 | still open |
| `or3-12`, 12m OR 3m | +0.01 (+0.08 since 2003) | +0.018 (-0.059..+0.096) | +0.47 | 2 of 4 | +0.045 | +0.039 | -0.020 | still open |
| `arm3-12`, armed re-entry | not scored | +0.015 (-0.060..+0.090) | +0.39 | 3 of 4 | +0.046 | +0.029 | -0.014 | still open |
| `vt-own-26-x`, own-vol 26% | +0.03 | -0.012 (-0.069..+0.044) | -0.43 | 1 of 4 | +0.034 | -0.043 | +0.031 | still open |
| `stop-0.25`, coin stop | +0.04 | -0.066 (-0.164..+0.031) | -1.33 | 0 of 4 | -0.068 | -0.124 | +0.058 | still open (upper end 0.001 above the kill line) |
| `fade-28`, 12m AND 28d | +0.04 | -0.062 (-0.144..+0.020) | -1.48 | 0 of 4 | +0.028 | -0.093 | +0.031 | **killed** |
| `tv40`, trend with 40% vol cap | -0.01 | +0.002 (-0.003..+0.006) | +0.68 | 3 of 4 | +0.007 | +0.000 | +0.002 | **killed** |

Bars (card): "real small edge" needs z >= 2.50 (Bonferroni over these 8 rules), D > 0 in 3 of 4
groups and before 1994; the project bar for a selectable rule is z >= 4.69 (`BAR.md`: 3,130
tries, N = 486 effective trials). "Killed": the upper end of the 95% range below +0.03, or
z <= -2.50. No variant reaches z 2.50; the largest is 1.55.

## Variant by variant

- **`e4` (ensemble of 1/3/6/12-month signals): still open, the best lead, not shown.** Ahead in all
  four groups (US industries +0.03, developed +0.05, wider indices +0.13, ETFs +0.04), in 29 of
  41 markets, and before 1994 (+0.09, z 2.05), i.e. outside the window it was first seen on. But
  about a third of D is mechanical: holding part positions instead of all-or-nothing raises the
  Sharpe on any market that drifts up (the drift-only null gives +0.022, 95% quantile +0.042).
  What is left, +0.04 per market, is under one standard error. As on the six: as good as
  `tsmom12`, maybe a little better, twice the trading, not distinguishable.
- **`vt-own-70-x` (own-vol targeting at a 70% mean share): still open, leaning positive.** +0.022,
  z 1.37; ahead in the US industries (+0.06, z 2.3 alone), developed and wider indices, behind on
  the ETFs (-0.03). Random walks would give it -0.012 (sizing by a noisy sigma costs a little), so
  the real data are +0.033 better than no-skill sizing: the volatility clustering it was built for
  is real, but the gain in Sharpe is small. Its in-sample +0.10 on the six (a book, with coins)
  is not reproduced at that size on single markets. This is the rule the `ownvol70-1` branch
  wires as a book: it remains a risk dial with at most a small Sharpe gain, not a proven edge.
- **`or3-12` and `arm3-12` (faster re-entry): still open by the letter, no sign of a timing gain.**
  +0.018 and +0.015, both below what their extra time in the market gives on a random walk with
  the same drift (+0.039, +0.029). Whatever they win on rebounds they lose in bear-market rallies,
  as `fast-reentry.md` found on falls. Reading: the fast-reentry line stays closed; nothing here
  reopens it.
- **`vt-own-26-x` (own-vol at 26%): still open, no lead.** -0.012; better than no-skill sizing
  (+0.031) but the low share costs more Sharpe than the timing earns.
- **`stop-0.25` (cointop-1's coin stop, carried to all markets): still open only at the kill
  line.** -0.066, behind in all four groups and before 1994. On a stock index with 15-20%
  volatility the stop leaves on a 4-5% dip from the year's high: a very different rule from the
  coin one. It loses less than its lower exposure alone would cost (+0.058 beyond drift), so it
  times dips a little, not enough to pay.
- **`fade-28` (12-month AND 28-day up): killed as a general rule.** -0.062, behind in all four
  groups; the upper end of the range is +0.020. Like the stop it times a little (+0.031 beyond
  the drift-only null) but holds too little. On coins (its own setting) this lane says nothing.
- **`tv40` (trend with a 40% volatility cap): killed outside very volatile assets.** On stocks,
  bonds and commodities the cap almost never binds: correlation with `tsmom12` 1.00, D +0.002
  with a range of -0.003..+0.006. It is `tsmom12` there. Its drawdown effect on the six comes from
  the coin slots, which this pool does not hold.

## Power and what it means

- **Realised SE: 0.038-0.050 for the price rules, 0.016 / 0.029 for own-vol, 0.002 for `tv40`.**
  That matches the card's prior for a correlation of about 0.3 between markets' differences:
  41 markets act like a handful of independent ones, because they share the crash calendar
  (1929-32, 1973-74, 1987, 2000-02, 2008, 2020). Block length barely matters (13 and 104 weeks:
  SE within 0.006).
- **Edge the test finds 80% of the time: +0.13 to +0.17 per market for the price rules at z 2.50,
  +0.21 to +0.27 at the project bar; +0.05 / +0.09 for `vt-own-70-x`.** So the pool rules out
  large edges, and a per-market edge of +0.15 for any of them would have been seen. It cannot
  settle the leads of +0.02 to +0.06 that were asked about: those stay unsettled, now on about
  1,900 market-years instead of 32 years.
- **More of the same will not settle them.** Adding stock markets mostly adds the same crashes
  again; the SE floor is about sqrt(0.3) x the single-market SE, near 0.04. Only markets with
  their own calendar would help (currencies, rates, commodities over long history, as futures);
  keyless daily data for those before 2000 is not in the cache.

## How sure

- One run of the pre-registered evaluation; card, code and tests pushed before any real number.
  The card changed once, after the plumbing run on random walks and before the real run
  (amendment 1, the drift-only null, a reading aid that changed no verdict).
- Variants frozen as first defined; the code reimplements them in numpy step by step from their
  original modules (`rules.py`, `fastreentry2.py`, `riskmenu3_run.py`, `cointop1_carry.py`); the
  look-ahead tests check that no decision moves when later bars are removed or changed. Own-vol
  starts each market at its target share on day one (the original book starts at its first
  monthly reset), a difference of a few weeks.
- Fill one session after the decision (stricter than the paper series and the gym), 2 bps a
  side, cash at 0. Price indices miss dividends; high-inflation markets trend in local currency;
  the data are not cleaned (3 daily moves above 25% in 23 indices). Each affects the variant and
  its twin alike.
- The US industries and the ETFs overlap the primary test's years (1994-2025); the before-1994
  pool (17 markets, US industries and the oldest indices) is wholly outside that window and agrees
  in sign with the full pool for the two open leads.
- The drift-only null is an i.i.d. walk (no volatility clustering, no fat tails): fair as an
  exposure baseline for the price rules, rough for the volatility rules.
- Per-market differences are on single assets (`tsmom12` Sharpe 0.10-0.85 here), not the six-asset book (1.05):
  the pooled D is not on the same scale as the in-sample leads.

## For the live rule

Nothing changes. `tsmom12` stays the rule; none of the eight is selectable (best z 1.55 against
4.69). If the rule is ever revised, `e4` is the only variant with a consistent positive sign
across groups and eras; `vt-own-70-x` remains a risk choice with at most a small Sharpe gain.
The held-out year stays unspent.

## Logged

`tries.md`: 377 rows, idea `pooled-1`: 8 `variant` rows (`<v>@pooled-41`, Sharpe cell = mean
per-market weekly Sharpe) and 369 `robustness` rows (`<rule>@<group>-<market>`, the eight
variants and `tsmom12` on 41 markets; weekly Sharpe with sqrt 52, turnover = position change a
year, `-` for the own-vol overlays).

## Next lanes (not started)

1. None for the equity pool: it has done what it can.
2. If keyless long histories for rates, currencies or commodities turn up (monthly is enough for a
   monthly-decision version), `e4` and `vt-own-70-x` against `tsmom12` there, under this card's
   method, would add independent samples. Its own card first.
