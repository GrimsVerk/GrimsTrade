# Card: breadth-anatomy-1 — why does a broader `tsmom12` book have a lower Sharpe?

Written 2026-11-25 before any number below is computed (no return, Sharpe or correlation of
any sleeve or book of this card looked at in this lane; the only numbers known are the ones
published in `research/breadth-book-1.md`). Lane `breadth-anatomy-1`. Descriptive only.

## Question

`breadth-book-1` (#143) found that adding ETFs to the six-asset `tsmom12` book lowers the
Sharpe above bills: `six` 1.19, `L-12` 0.96, `L-20` 0.83, `L-all` (35 assets) 0.65 (z -2.3 to
-2.6), 2008-2025. Diversification theory says adding weakly correlated trend sleeves with a
positive Sharpe should raise it. This card splits the fall into parts, using the same code,
the same bars and the same universes. Nothing new is chosen by results: no new rule, no new
set, no selection, no retuning, no candidate for the paper books. The counterfactual books
below (coins at a fixed weight, inverse-vol weights) exist only to split the difference; none
is a candidate and none gets a pass bar.

## Prior (stated now)

Most of the fall is coin dilution (`six`'s Sharpe is coin-driven and every added slot shrinks
the coins' share); the rest is that the added ETF sleeves have a low Sharpe (0.2-0.4) and a
correlation with the six's book high enough (0.4-0.6) that they fail the marginal test
SR_A > rho x SR_six, so no positive weight on them helps. Crisis correlations higher than calm
ones. Inverse-vol weighting shrinks the gap mainly because it also shrinks the coins in `six`.

## Data and window

- Bars: exactly `breadth-book-1`'s research cache (Yahoo dividend-adjusted ETFs, harness BTC
  and ETH, `^IRX` for bills), cut at **2025-10-31** (no later bar loaded; the held-out year is
  not touched). Decisions 2008-01-02 .. 2025-10-31 (window W). `breadth-book-1` ran to
  2025-11-09; step 0 reproduces its headline rows on W, so the 9-day difference is visible.
- Universes: `breadth-book-1`'s fixed sets, unchanged: `six` (SPY QQQ GLD TLT BTC ETH),
  `four` (SPY QQQ GLD TLT), `L-12`, `L-20`, `L-all` (the six plus the round-robin-ordered
  eligible ETFs, `bbook1_core.nested`), `E-all` (all 33 eligible ETFs). The **added sets**
  A-6, A-14, A-29 = `L-12`, `L-20`, `L-all` minus the six. `X-10`, `X-18`, `X-33` = `four`
  plus A-6, A-14, A-29 (`X-33` = `E-all`). `C` = BTC, ETH.
- Rule: the project's `tsmom12` exactly as on the bar (`bbook1.tsmom12()`: weekly Friday
  decisions, equal slot 1/N over assets with a year of bars, slot held while the 365-day log
  return is > 0, else cash; next-open fills; gym costs). Cash earns the 13-week bill.

## Measures

Every Sharpe is the Sharpe of the daily return above the bill on calendar days, 365-day year
(`bbook1.excess_calendar` + `bbook1_core.sharpe`, the series `breadth-book-1` used for its
edges). Differences carry `bbook1_core.paired` (stationary bootstrap, block 20, 2,000 draws,
seed 0) SEs. Cash-earns-0 Sharpe reported beside the main ones in step 0 only.

### Step 0: reproduction

`six`, `four`, `L-12`, `L-20`, `L-all`, `E-all` on W (both Sharpe conventions).

### (a) coin share

1. Mean coin weight (mean daily sum of BTC + ETH target weights) and the coins' share of the
   book's variance (cov(coin part, book) / var(book), coin part = the coins' weights times
   their above-bill returns, from the decisions' target weights) for `six`, `L-12`, `L-20`,
   `L-all`.
2. **Coins excluded from both**: `four` against `X-10`, `X-18`, `X-33`.
3. **Coins held at the same weight** (`K-12`, `K-20`, `K-all`, counterfactual): on each
   decision each coin slot gets the weight it has in `six` that day (1 / number of eligible
   six assets, held while its signal is on); the ETF budget `six` has that day
   (eligible-ETF count of the six / eligible six count) is split equally over the set's
   eligible ETFs (held while each one's signal is on). Same set as `L-k`, same signals.
4. Split of each gap: SR(`L-k`) - SR(`six`) = [SR(`K-k`) - SR(`six`)] (ETF breadth with the
   coin share fixed) + [SR(`L-k`) - SR(`K-k`)] (coin dilution), each with its SE.

### (b) the added markets' own `tsmom12` Sharpe

1. Per asset (all 35): `tsmom12` on that asset alone (slot 1 when the signal is on, cash
   otherwise), its Sharpe, annualised vol and mean exposure, plus buy-and-hold (weight 1) on
   the same days, from its first eligible decision in W. Class from `bbook1_core.CLASSES`.
2. Summary: mean and median sleeve Sharpe of the six, of A-6, A-14, A-29, and per class.
3. The books `A-6`, `A-14`, `A-29` (`tsmom12` on the added ETFs alone, equal slots).

### (c) correlation and the diversification arithmetic

Sleeve series = the daily above-bill returns of (b)1, summed into Friday-to-Friday weeks; a
week counts for a pair only when both sleeves are eligible.

1. Mean pairwise correlation within the six's sleeves, within A-29's sleeves, and between the
   two groups; participation ratio (`bbook1_core.participation`, eigenvalues clipped at 0) of
   the sleeve correlation matrix for the six and for all 35.
2. **Two-book blend** for each pair (`six`, `A-k`) and the coin-free (`four`, `A-29`): daily
   correlation rho of the two above-bill series, the marginal test SR_A > rho x SR_ref (if it
   fails, every positive weight on A lowers the Sharpe of a static mix), the max-Sharpe
   weight on A, w* = argmax over [0, 1] of SR(w x A + (1 - w) x ref), and SR(w) at w = 0,
   the `L-k`-like weights 6/12, 14/20, 29/35 (as weight on A: 0.5, 0.7, 0.83), w* and 1.
   SR(w) uses a static daily mix (an approximation of the book; its error is shown by
   comparing SR at the `L-k` weight with the actual `L-k`).
3. Per added sleeve: SR_i against rho_i x SR_six (rho_i = weekly correlation with the `six`
   book), count of the 29 that pass the marginal test; the same against `four`.
4. **Crises**: 1. and rho(`A-29`, `six`) on the weeks inside the harness STRESS windows that
   fall in W, two definitions fixed now: market crises (2008 crisis, covid crash, 2022 rate
   shock) and all seven windows in W (adding the three crypto winters), against the other
   weeks.

### (d) equal weight vs risk weight

`rw` form (counterfactual): same weekly decisions and signal; each eligible asset's slot is
(1 / sigma_i) / sum over eligible j of (1 / sigma_j), held while its signal is on;
sigma = the live runner's EWMA vol of daily simple returns (centre of mass 60,
`bbook1._ewma_vol`), annualised with 365 (coins) or 252 (ETFs). Books `six-rw`, `four-rw`,
`L-12-rw`, `L-20-rw`, `L-all-rw`, `E-all-rw`; report SR, mean coin weight, and the gaps
`L-k-rw` - `six-rw` and `E-all-rw` - `four-rw` against the equal-weight gaps.

### (e) period (one row; the post-2009 break by asset class is lane `tick-tier-1`'s)

SR in 2008-01-02 .. 2009-12-31 and 2010-01-01 .. 2025-10-31 for `six`, `four`, `L-all`,
`E-all`, `A-29`, `K-all`, and the gap `L-all` - `six` in each.

## Reading (fixed now)

- The answer names the share of the `L-all` gap that is coin dilution (a.4) vs ETF breadth
  with coins fixed, and, for the ETF part, whether the added sleeves fail the marginal test
  (b, c.2) because their Sharpe is low, because rho is high, or both (SR_A below 0.5 x SR_ref
  with rho < 0.5 = "low Sharpe"; rho >= 0.5 with SR_A >= 0.5 x SR_ref = "co-movement").
- (d): the gap "is a weighting artefact" only if `L-all-rw` - `six-rw` is within one SE of 0
  AND `E-all-rw` - `four-rw` is too; otherwise weighting is a partial or no explanation.
- (e) is reported, not interpreted beyond its sign.
- No pass bar: nothing here can become a book. The bar count N is not raised.

## Controls

- Tests (offline, `tests/test_banat1.py`): the blend functions (SR of a static mix, w*, the
  marginal test agree with the closed form on planted series; the test's sign matches whether
  a small weight raises SR), and the `K` and `rw` weight functions (weights sum to the
  budget, coins get the six's weight, inverse-vol proportions) on a synthetic panel.
- The script asserts no loaded bar is after 2025-10-31; `harness.check_against_gym` for
  `L-all` on two days.

## Logging

One `tries.md` row, kind `note`, "re-score (not a try)", as `gap-2002-1` and `e4-anatomy-1`
did; no ledger rows (no strategy try). Tables: `research/results/breadth-anatomy-1.md`;
write-up `research/breadth-anatomy-1.md`; one line in `research/ideas.md`. One run.
