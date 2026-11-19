# coupon-dose: idle cash into the long bond when Treasury cash is paid back mid-month

Field: pharmacokinetics (a scheduled dose is absorbed back into the compartment it came from
within days; the response rises with the dose). It is W4, one of five mechanisms added to
wide-1's list by wide-4 (`wide-1.md`, last section), picked there by a written note.
Written 2026-11-18, run wide-4, before any test or number of this card. Seen before: every
earlier result in `tries.md`, including `tax-drain` (wide-4: failed; the TGA rises tens of
billions on tax dates), `auction-concession` (TLT dips into long-bond auctions, recovers after)
and the post hoc month-end bond rally (wide-1, `results/wide-1-yields.md`). The Treasury's
auction file was used by wide-1 for dates only. No coupon amount, net payment or mid-month bond
return has been printed by me or, as far as `tries.md` and `ideas.md` show, by any earlier run.

## Claim

The Treasury pays coupons and repays maturing notes and bonds on fixed days: the 15th and the
last day of the month. The holders of long Treasuries, index funds above all, must put that
cash back into the same kind of bond to stay at their index's duration. When the net payment
(coupons plus principal minus new notes and bonds settling the same day) is positive, there is
a buy order for Treasuries of known size on a known date. Long bonds earn more in the four
sessions from that day than on average, and more the larger the net payment.

## Why it might work

- The flow is forced and its size is known in advance (maturities and coupons for years,
  settlements from the auction announcement a week or so before).
- The sizes vary several-fold from month to month (the 10- and 30-year pay coupons in
  Feb/May/Aug/Nov; refunding issues settle on the same day): a dose-response slope can be
  tested, not only a calendar mean.
- The rule puts idle cash into TLT, whose drift was positive in our period, at 4 bps a round
  trip.

## Why it might not

- Much of the cash goes to holders who do not reinvest in long bonds (the Fed's own holdings,
  foreign central banks, bill buyers), and dealers can pre-position.
- Net payments on the 15th are often negative (the deficit is financed by issues that settle
  on the same days), so the positive doses may be few and small.
- The gain is capped: idle cash is about a quarter of the book, for four sessions a month.
  A real +20 bps per event on that quarter is roughly +0.6% a year on the book, +0.03 Sharpe:
  **the bar of p < 0.00185 cannot be met by a gain that small**; the event study is where the
  mechanism can show.
- Coupon days in 2003-2007 also carried a smaller 30-year stock (none issued 2001-2006).

## Data

- Prices: the six assets and the 8 other ETFs, as every run.
- The Treasury's auction file (fiscaldata.treasury.gov `accounting/od/auctions_query`, public,
  keyless), downloaded again with the fields wide-1 did not keep: `cusip`, `security_type`,
  `original_security_term`, `inflation_index_security`, `floating_rate`, `announcemt_date`,
  `auction_date`, `issue_date`, `maturity_date`, `int_rate`, `total_accepted`. Saved to a new
  directory `<cache_root>/downloads/wide-4/treasury-auctions/`, parsed with `python -I` by
  `lib/wide4_coupons.py` into `<cache_root>/derived/wide-4/payments.csv`. The parser prints
  only row counts and date ranges.

## Net dose (fixed)

Nominal fixed-rate notes and bonds only (no bills, TIPS or floaters), as wide-1's file.

- Outstanding amount of a CUSIP on a day = the sum of `total_accepted` of its auctions whose
  `issue_date` is before that day (reopenings add).
- Coupons: semiannual, `int_rate` / 2 % of the outstanding amount, on the maturity's day of
  the month in the maturity month and six months from it, from the first such day after the
  first issue to maturity; a maturity on the last day of a month pays on the last day of the
  coupon month.
- Principal: the outstanding amount, on the maturity date.
- Settlements: minus `total_accepted`, on the `issue_date`.
- A payment date that is not an SPY session moves to the next session.
- **Mid-month payment day P**: the session that carries the payments dated the 15th. The net
  dose of P is the sum of the above for those payments, in $ billion, and as a share of all
  outstanding nominal notes and bonds (`dose`, in %). Month-end payments are not used (the
  month-end bond rally was found post hoc there).
- As of a decision: only auctions with `announcemt_date` on or before the decision day count
  (maturities and coupons of issued securities are known; settlements are known from the
  announcement).
- Known gaps, accepted: securities auctioned before the file starts (1979) and still paying in
  2002-2009 are missing; `total_accepted` excludes the Fed's add-ons (its rolled-over holdings).

## Rule (fixed, no fitted parameter)

- Base: `tsmom12` on the six assets, decided weekly as always.
- Overlay, decided daily (as `auction-concession`): at a decision after the close of sessions
  P-1, P, P+1 and P+2, if P's net dose (as known at P-1) is **positive**, the idle cash
  (1 minus the sum of the base weights) is added to TLT, if TLT is eligible. With next-open
  fills TLT then holds the extra weight for the returns of sessions P .. P+3.

## Variants (all that will be run)

1. `dose` (only variant): as above.
2. Placebo, logged as `robustness`, never selectable: `dose-neg`, the same overlay on the
   mid-month days whose net dose is zero or negative.

## Twin and baselines

Twin `tsmom12`. Also shown: equal weight, `dose-neg`, and an event study (descriptive, no
`tries.md` row): for TLT and IEF, the log return from the close of P-1 to the close of P+3,
minus the average 4-session return of 2002-07-30 to the end of train:

1. mean, t and count for positive and for non-positive doses;
2. the dose-response slope: OLS of that excess on `dose` (in %), slope and its t
   (heteroskedasticity-robust, HC1);
3. both for 2002-07 to 2013-12 and 2014-01 to the end of train.

## Out-of-universe

The 8 other ETFs as a `tsmom12` book with the same overlay into IEF. Coins and indexes: not
applicable (no Treasury bond in them).

## Pass bar

The default in `protocol.md` for `dose` against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 54 = 0.00185**: the list of 46 plus W1-W8.
2. Eras counted from 2000-09 (before TLT exists the rule is its twin), ahead in at least 3 of 4.
3. Max drawdown not more than 5 points worse than the twin's.
4. Positive, and positive on the ETF set (the only out-of-universe set that applies).
5. Beats equal weight on Sharpe.
6. (card) `dose` beats its placebo `dose-neg` on Sharpe.

Reading of the event study, fixed now: **the mechanism is supported** only if, for TLT, (a)
the dose-response slope is positive with t >= 2, (b) the positive-dose mean is above the
non-positive-dose mean, and (c) the slope is positive in both halves. Either way it is
evidence, not a pass.

Held-out year: once, `dose` only, only if all bars pass.

## My guess before any number

Chance it passes: 2%. Difference to the twin: -0.01 to +0.02 Sharpe. Positive doses on
roughly a third of mid-month days. TLT excess on positive doses: 0 to +25 bps; slope t 0 to 2.

## Result

See `results/coupon-dose.md` once tested.
