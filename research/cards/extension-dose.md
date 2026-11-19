# extension-dose: the month-end bond window only when the index extends a lot

Field: control theory (an index fund is a tracking controller; at each month end its
setpoint, the index's maturity, steps by an amount fixed by the index rules and known days
ahead, so the fund's trade is a feedforward of a known step). It is W10, added to wide-1's
list by wide-5 (`wide-1.md`, last section) and picked there by a choice rule written before
any number. Written 2026-11-18, run wide-5, before any test or number of this card.

Seen before: every earlier result in `tries.md`; in particular **the month-end bond rally
itself** (wide-1, found post hoc: TLT +39 bps at closes and +32 at our fills over the last four
sessions, 2003-2025; `month-end-bonds`: LQD +10.5 bps net, t 1.93, not replicated by its bar).
So the calendar mean is seen. The index extension has never been computed in this repo; no
split of the month-end window by any month property has been printed by me or, as far as
`tries.md`, `ideas.md` and the `month-end-bonds` write-up show, by any earlier run. From the
auction download only row counts and dealer-field coverage (see `dealer-backlog`).

## Claim

Bond index funds and benchmarked managers must match their index's duration when the index is
rebuilt on the last business day of the month. The step in the index's maturity at that
rebuild ("extension") is set by rules: the new issues that settled during the month come in,
the bonds that fell below the bucket's lower limit go out. Their buying in the last days of
the month is proportional to the step. **If the month-end bond rally is index buying, TLT
earns more over the last four sessions in months with a larger extension of its 20+ year
bucket.**

## Why it might work

- The cause is written in index rules and the dose is computable from public data before the
  window opens (auction results, issue and maturity dates).
- The dose varies month to month (refunding months, reopenings, bonds aging out in clusters),
  and the low-extension months are the high-extension months' placebo on the same calendar:
  the seen mean lifts both equally.
- About 280 month ends since TLT began.

## Why it might not

- The month-end rally may have other causes (window dressing, cash from coupons and
  principal at month end, pension rebalancing) that do not scale with extension.
- Par-weighted average maturity is a crude stand-in for the index's market-value-weighted
  duration; a 20+ year bucket's duration moves little with a new 30-year issue.
- The rule's Sharpe against `tsmom12` is lifted by a mean found by looking at these very
  months: **bar 1 is not evidence here; bar 6 (against the placebo) and the slope are.**
- The gain is capped as for every idle-cash overlay: half the month ends, a quarter of the
  book, four sessions. **The bar of p < 0.00179 cannot be met by a gain that small.**

## Data

- Prices: the six assets and the 8 other ETFs, as every run.
- The auction file downloaded for `dealer-backlog` (`<cache_root>/downloads/wide-5/
  treasury-auctions/`), parsed by `lib/wide5_auctions.py` into
  `<cache_root>/derived/wide-5/auctions.csv`.

## Extension (fixed)

Nominal fixed-rate notes and bonds only.

- Outstanding amount of a CUSIP on a day = the sum of `total_accepted` of its auctions whose
  `issue_date` is on or before that day (reopenings add).
- Remaining maturity in years at day d = (maturity date - d) / 365.25.
- Bucket: **20+** = remaining maturity >= 20 (TLT's index); **7-10** = 7 <= remaining
  maturity <= 10.05 (IEF's index; 10.05 so that a new 10-year note is in).
- R = the last calendar day of month m; R' = that of month m-1.
- Old set = the securities in the bucket at R' with their amounts at R'. New set = the
  securities in the bucket at R with their amounts at R, counting only auctions whose
  `auction_date` is on or before the decision day (the close of T-4, below).
- **Extension E(m)** = par-weighted average remaining maturity of the new set at R minus that
  of the old set, also measured at R. In years.
- Known gaps, accepted: buybacks (2000-02) and the Fed's add-ons are not in the file;
  callable 1980s bonds are not flagged (they can sit in the 7-10 bucket until 2009-14 only).

## Rule (fixed, no fitted parameter)

- Base: `tsmom12` on the six assets, decided weekly as always.
- T = the last session of the month on the bond ETF's calendar. At a decision after the close
  of sessions T-4 .. T-1, if E(m) (known at T-4) is **above the median of E over the previous
  24 months**, the idle cash (1 minus the sum of the base weights) is added to TLT, if TLT is
  eligible. With next-open fills TLT then holds the extra weight from the open of T-3 to the
  open of T+1 (wide-1's window).
- The first 24 months of the bucket series have no median and no overlay.

## Variants (all that will be run)

1. `ext-high` (only variant): as above.
2. Placebo, logged as `robustness`, never selectable: `ext-low`, the same overlay in the months
   whose E(m) is at or below that median.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, `ext-low`, and an event study (descriptive, no
`tries.md` row):

- For TLT on the 20+ bucket and IEF on the 7-10 bucket: the log return from the open of T-3 to
  the open of T+1 (our fills), minus the average 4-session open-to-open log return of the same
  ETF from 2002-07-30 to the end of train.
- Mean, t and count for high and low months (the rule's split); the slope (OLS of the excess,
  in bps, on E(m), in years; HC1 t); each for all years, 2002-07 to 2013 and 2014 to the end of
  train. The median and spread of E(m) are printed.

## Out-of-universe

The 8 other ETFs as a `tsmom12` book with the same overlay into IEF, by the 7-10 bucket. Coins
and indexes: not applicable.

## Pass bar

The default in `protocol.md` for `ext-high` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 56 = 0.00179**. Biased upward by the seen month-end mean (above).
2. Eras counted from 2000-09, ahead in at least 3 of 4.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive, and positive on the ETF set.
5. Beats equal weight on Sharpe.
6. (card) `ext-high` beats its placebo `ext-low` on Sharpe.

Reading of the event study, fixed now: **the mechanism is supported** only if, for TLT at our
fills, (a) the slope on E(m) is positive with t >= 2, (b) the high-month mean is above the
low-month mean, and (c) the slope is positive in both halves. Either way it is evidence, not a
pass.

Held-out year: once, `ext-high` only, only if all bars pass.

## My guess before any number

Chance it passes: 2%. Difference to the twin: 0 to +0.02 Sharpe (lifted by the seen mean);
`ext-high` against `ext-low`: -0.01 to +0.01. Slope t -1 to +2. My best guess is that the
month-end rally does not scale with this crude extension.

## Result

See `results/extension-dose.md` once tested.
