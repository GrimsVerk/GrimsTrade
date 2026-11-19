# risk-map: the menu of risk choices, side by side

Field: allocation. Written 2026-11-12 07:20 UTC, research run 3, before any run of this menu.
Seen before: everything in `README.md` (runs 1-2) and `reviews/review-1.md` on branch
`review-1`. In particular: the trend rule's lead over holding everything comes from 2000-2002,
when the book held only SPY and QQQ; since 2003 the two tie on Sharpe.

## Claim

None. This card describes; it does not test an idea. The owner must choose how big a worst
drop to accept and how much crypto to hold. The menu shows what each choice did in the past.

## Rule (fixed)

Each Friday, two settings decide the book:

- **Slot sizes.** Each eligible coin (BTC, ETH) gets a fixed share: 0%, 5%, 10%, or an equal
  slot (1/n of the eligible assets: a sixth once all six exist). The eligible ETFs share the
  rest equally.
- **Rule on each slot.** `hold`: always held. `tsmom12`: held if the asset is up over the last
  365 days, else cash. `tv20`, `tv40`, `tv60`: as `tsmom12`, and the slot is scaled down by
  min(1, cap / 20-day volatility), with the cap at 20%, 40% or 60% a year (`tv40` is the
  `trend-vol` card's setting).

## Variants (all that will be run)

The 20 combinations, named `<rule>-c00`, `-c05`, `-c10`, `-c17` (equal slots). Decisions from
1994-02-01 to 2025-11-09 on the six live assets, dividend-adjusted prices, the gym's costs.
Six of them repeat rules already logged (`hold-c17` is equal weight, `tsmom12-c17` is
`tsmom12`, `tv40-c17` is `trend-vol/tv40`; `hold-c00/c05/c10` are `crypto-slot-size` run from
1994 instead of 2013).

## Reported

For each variant, over 1994-2025 and over 2003-2025 (the review's window; sliced from the same
run): growth per year, worst drop from a high, worst calendar year, longest time below an
earlier high. Also 2013-2025, the only years in which the crypto setting changes anything.

## Pass bar

None: reported, not passed or failed. No setting is to be picked for its Sharpe; the 20 rows
still count as tries. The held-out year is not used.

## Result

See `risk-map.md` and `results/risk-map.md`.
