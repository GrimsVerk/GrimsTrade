# hedge-regime: hold the long bond out of trend while it hedges stocks

Field: statistical physics (an order parameter that says which phase the system is in). It is
mechanism F2 of `wide-1.md` step 1 ("the sign of the stock-bond correlation is an order
parameter that says which hedge works"), which wide-1 killed without a test as "a refinement
of `trend-to-safe`; one flip since TLT exists".
Written 2026-11-18 ~19:25 UTC, run wide-3, before any test or number of this card. Seen
before: every earlier result in `tries.md`, including `trend-to-safe` (empty slots to safe
assets in trend) and the wide-2 results. No stock-bond correlation has been printed by me.

## Claim

The sign of the correlation between stock and long-bond daily returns is the order parameter.
Below zero (the "hedge phase", flight to quality) a long bond pays off exactly when the stocks
the trend rule holds fall, and it earns the term premium the rest of the time; it is worth its
slot even when its own 12-month trend is down. Above zero (the "inflation phase": the 1970s,
2022) bonds and stocks fall together, and the bond must earn its slot by its trend like any
other asset.

## Why it might work

`tsmom12` drops TLT whenever TLT is below its level of a year ago. In the hedge phase those are
often slow bond sell-offs in good stock markets (2013, 2016-18), and the book then sits in cash
at 0 while it is long stocks without insurance. Cash earns 0 in the gym, the bond earns its
yield.

## Why it might not

- Power. Since TLT exists the sign was, as far as I remember, negative almost all the time until
  about 2021, then positive. The test is then close to "hold TLT always until 2021, then trend":
  one flip, one episode. A pass would rest on 2002-2021 bond drift as much as on the mechanism.
- The out-of-trend bond years can be long and costly (2013: about -13%); insurance that is not
  needed is a cost.
- A one-year correlation reacts slowly: in 2022 it may still have been negative when the bond
  crash began.

## Rule (fixed, no fitted parameter)

- Weekly decisions on Friday's close. Base weights are `tsmom12`'s (equal slots, cash when the
  365-day return is not positive).
- Bonds of the set: TLT (six assets); IEF and LQD (other ETFs). Stock reference of the set: the
  equal mean of the daily log returns of its eligible stock ETFs: SPY and QQQ (six); IWM, EFA,
  EEM and VNQ (other ETFs). Daily returns from the business-day grid (`View.grid_logret`).
- Order parameter rho = Pearson correlation of the bond's daily log returns with the stock
  reference over the last 252 grid rows. Undefined (rule = twin for that bond) if either side
  has a missing value in the window.
- If the bond is eligible and rho < 0, it holds its equal slot whatever its trend. Otherwise it
  follows `tsmom12`. Every other asset is the twin's. Exposure can only be higher than the
  twin's.

## Variants (all that will be run)

1. `hedge` (only variant): as above.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, the share of Fridays with rho < 0 for TLT, the number
of sign changes of rho (weekly), and the Fridays on which the rule holds TLT and the twin does
not, with TLT's return over those weeks.

## Out-of-universe

The rule applies to sets that hold both stocks and bonds. Only the 8 other ETFs do (IEF, LQD
against IWM, EFA, EEM, VNQ). The coins and the indexes have no bond: not applicable.

## Pass bar

The default in `protocol.md` for `hedge` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 46 = 0.0022**: every pick out of wide-1's list of 46 counts
   (`wide-3.md`, step 1).
2. Eras counted from 2000-09 (before TLT is eligible in 2003-07 the rule *is* its twin; the
   reading wide-1 used for its TLT rules): ahead in at least 3 of 4.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive, and positive on the one applicable out-of-universe set (other ETFs).
5. Beats equal weight on Sharpe.

Held-out year: once, `hedge` only, only if all bars pass.

## My guess before any number

Chance it passes: 2%. Difference to the twin: -0.04 to +0.05 Sharpe.

## Result

See `results/hedge-regime.md` once tested.
