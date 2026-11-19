# eu-4: whipsaw in the small coin-free EUR book, and reducers that keep the rule

Lane `eu-4` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-4` from `eu-3`. Code: `lib/eu4.py`. Fees are described as generic tiers: EUR 1, 2
or 3 per ETF order on a constant book (eu-2's three schedules, reused unchanged so the numbers
compare with eu-2 and eu-3).

## 1. Diagnosis: where `euw` spends its order budget (step 1, descriptive)

Table: `results/eu-4-diag.md` (`uv run --with numpy python research/lib/eu4.py diag`). This
replays eu-3's `tsmom12@euw/slip` (the house rule on SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY,
2012-2025, no fixed fee) and sorts its 417 ETF orders by cause. No rule was compared, so no
`tries.md` row.

- **Thirds.** 30.1 orders a year: 10.0 signal entries, 9.8 signal exits, 10.0 drift top-ups or
  trims (plus 4 start-up buys). At a EUR 10k book that is EUR 30 / 60 / 90 a year at the EUR
  1 / 2 / 3 tiers, a Sharpe drag of 0.05 / 0.10 / 0.15 on a 5.9%-vol book; each third costs a
  third of that.
- **Most flips are whipsaw.** Of the ~20 flip orders a year, 16.4 (83%) sit in spells that the
  next flip reverses within 4 weeks, 18.5 (94%) within 13 weeks. 88 of 267 closed spells last
  a single Friday; 150 last 4 weeks or less. Whipsaw within 4 weeks alone costs EUR 16 / 33 /
  49 a year at 10k (Sharpe 0.03 / 0.06 / 0.08), i.e. **about half of the whole fee drag**.
- **The whipsaws are shallow.** Inside a 1-week spell the 12-month return never got further
  from zero than a median 0.05 of the asset's own yearly vol (|z|); 94% stayed under 0.25.
  2-week spells: median 0.14, 83% under 0.25. Spells that last more than half a year reach a
  median |z| of 1.9. The weekly change of z has an sd of **0.21**, the same for every asset
  (0.20-0.22), as it should be for a one-year return in vol units: a week's noise is ~0.2.
- **Every asset whipsaws, the quiet trends most.** Flips a year: EXXY (commodities) 4.0, IBGL
  (long euro govts) 3.4, IQQE (EM) 3.2, EXSA (Europe) 3.1, 4GLD (gold) 2.7, SXR8 (S&P 500) 2.0,
  IBGS (short euro govts) 1.3. EXXY, IBGL, EXSA and IQQE carry 71% of the whipsaws of 13 weeks
  or less. It is not one bad asset: no slot can be dropped to fix this.
- **Whipsaws are not free in the market either** (in-spells lost ~1.1, out-spells missed ~1.4
  log points a year of book within 4 weeks), but those numbers are picked by hindsight (a spell
  is a whipsaw because the asset turned), so they are not a cost a rule could save.

What this says for step 2: the cheap orders to remove are the 1-2 week flips around zero, and
the noise that makes them is a known size (~0.2 in z units). A confirmation rule (a flip needs
the new sign two Fridays in a row) removes exactly the 1-Friday spells; a dead zone around zero
of about one week's noise removes most 1-2 week spells. Drift (a third of the orders) is not
touched by either; eu-3 found that checking drift weekly saves only 2 orders a year.

## 2. Two whipsaw reducers (step 2, card `cards/eu-4.md`, pushed before any number)

Table: `results/eu-4.md` (`uv run --with numpy python research/lib/eu4_run.py run`; `check`
first: with no confirmation and no dead zone the state machine gives the house rule's weights
exactly on `euw`, `eu6` and `usw`). 24 rows in `tries.md` (idea `eu-4`): 20 `variant` on `euw`,
4 `robustness` on `eu6`/`usw`. `R`, V0 and equal weight are eu-3's (and eu-1's, eu-2's) saved
runs, re-scored without new rows.

- **C1 `confirm2`**: switch only after two Fridays in a row with the new sign.
- **C2 `dz25`**: dead zone; enter above z = +0.25, leave below z = -0.25 (about one week's
  noise, step 1).

| `euw`, no fixed fee | Orders/yr | Signal flips/yr | Sharpe | Max DD | Position corr | Crash windows 2015-16 / 2018-Q4 / 2020 / 2022 |
|---|---:|---:|---:|---:|---:|---|
| R `tsmom12` | 30.1 | 19.8 | 0.62 | 13.0% | - | -7.8 / -3.9 / -11.6 / +2.2% |
| C1 `confirm2` | 20.0 | 9.8 | 0.62 | **16.3%** | 0.91 | -9.7 / -3.1 / -14.6 / +2.0% |
| C2 `dz25` | 16.6 | 6.9 | 0.64 | **15.4%** | 0.89 | -9.5 / -3.6 / -14.3 / +1.9% |
| equal weight | 15.6 | - | 0.77 | 19.8% | - | -14.6 / -3.2 / -18.7 / -7.6% |

**Both reducers fail the character test, on one count: the drawdown.** They do what they were
built for: signal flips halve (C1) or drop by two thirds (C2), orders fall from 30 to 20 or 17
a year, Sharpe is unchanged (0.00 and +0.03, p 0.48 and 0.36, far from the family bar of
0.0125), positions agree on 95-96% of slot-Fridays (correlation 0.91 / 0.89, bar 0.80), the
crash pattern against equal weight is kept (3/4 and 4/4) and no crash window is more than 3
points worse (C1 exactly 3.0 in covid). But the worst drawdown deepens by **3.3 points (C1)
and 2.4 points (C2)** against a 2-point bar. The cause is one crash: C2's worst fall is
covid (Feb-Mar 2020, -15.4% vs R's -11.6% in that window); C1's is the long 2015-2020 stretch
ending in covid. Waiting for confirmation, or for the 12-month return to clear -0.25 vol,
means getting out a week or two later in a fast crash: the same trade-off trend-tune found on
the US six ("the later exits cost what the fewer whipsaws save"), here visible as drawdown
rather than Sharpe.

Robustness (no fixed fee, against R on the same book): on `eu6` both keep Sharpe (-0.04,
-0.00) and drawdown (+1.7, +0.8 pts) with ~45-65% fewer flips; on `usw` C1 holds (-0.02, +1.1
pts) but C2 loses 0.07 Sharpe and 3.2 points of drawdown. Neither is "fragile" by the card
(each passes on at least one other book); they fail on `euw` itself.

## 3. Minimum book per fee tier, and the eu-3 verdict (step 3)

Fee loss (strict, eu-3's reading) and minimum book on `euw` (loss <= 0.10; interpolated in
1/size, and the mechanical value fees per year / (0.10 x vol)):

| Rule | EUR 1 tier | EUR 2 tier | EUR 3 tier | Keeps character |
|---|---|---|---|---|
| R `tsmom12` | ~6k | ~10k | ~16k | yes |
| V0 Friday trades (eu-3) | ~5k | ~10k | ~15k | yes |
| C1 `confirm2` | <= 5k (~4k) | ~7k | ~11k | **no** (DD +3.3) |
| C2 `dz25` | <= 5k (~3k) | ~6k | ~9k | **no** (DD +2.4) |

**The eu-3 verdict does not change.** With only same-character rules: EUR 5k is not worth
running at any tier; EUR 10k is worth it at the EUR 1 tier (R or V0) and on the line at the EUR
2 tier (V0 0.098); not at the EUR 3 tier; EUR 25k is fine at every tier. The fee loss stays
mechanical (observed within 0.01 of fees per year / vol in every cell).

Descriptive only (the card's bar waived; these are different rules by that bar): the dead zone
would bring the minimum book down by about 40% at every tier (EUR 3 tier: 16k -> 9k; EUR 2:
10k -> 6k), so a small coin-free book at the EUR 2-3 tiers would become workable, at the price
of a drawdown 2-3 points deeper in a covid-style crash. That is a risk choice, not a free fix.

## Verdict

1. Half of the small coin-free book's fee drag is whipsaw: flips around a 12-month return near
   zero that reverse within a month (83% of flip orders), spread over all seven assets.
2. Two pre-committed reducers that keep Sharpe and positions (C1 confirmation, C2 dead zone of
   one week's noise) cut orders by a third to a half, but both deepen the worst drawdown by
   more than the 2-point bar, through slower exits in the 2020 crash. By the card they change
   the rule. Neither is used; held-out year unspent.
3. Nothing changes the eu-3 verdict or argues for changing the house rule. The levers for a
   EUR 5-10k coin-free book stay: (a) the EUR 1 tier (R from ~6k), (b) accept a rule change
   (monthly clock or a dead zone) with its own card on other books and the held-out year.

## Rows counted

24 rows (idea `eu-4`): `C1-confirm2@euw` and `C2-dz25@euw` at no fee and 3 tiers x 3 books
(20 `variant`), and both at no fee on `eu6` and `usw` (4 `robustness`). The selectable family
is now 8 (eu-3's V0-V5, C1, C2); nothing was selected. The step-1 diagnosis added no row.
