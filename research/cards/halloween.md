# halloween: hold the stock trend slots only from November to April

Sources: Bouman and Jacobsen, American Economic Review 92(5), 2002, pp. 1618-1635 (R12 in
`survey-4.md`); Andrade, Chhaochharia and Fuerst, Financial Analysts Journal 69(4), 2013,
pp. 94-105 (R13); Zhang and Jacobsen, Journal of International Money and Finance 110, 2021
(R14). Pick B of `survey-4.md` (score 5 of 5, second on the tie-break). Parked by the first
survey ("one observation a year"); counted now as one of survey-4's four new mechanisms.
Written 2026-11-18, lane survey-4, before any test or number of this card.

## Claim (as this book can use it)

Stock returns from November to April beat those from May to October in 36 of 37 markets in
1970-1998 (R12), by about 10 points a year again in the same markets on new data from
November 1998 to April 2012 (R13), and in UK data over three centuries (R14). Not in bonds
(R13). If it still holds, holding the stock trend slots only in the winter half cuts risk more
than return.

## Why it might work

- The best-documented post-publication record of any calendar effect: R13's new data are
  entirely after R12 and as strong. R13 ties it to a seasonal swing in risk appetite seen in
  several risk premiums, which publication need not remove.

## Why it might not

- One observation a year: our 32 years cannot separate a 5-point effect from luck; the family
  bar (p < 0.00154) is out of reach unless the effect is very large.
- `tsmom12` already leaves stocks in the long bear markets (2001-02, 2008), where much of the
  summer loss sat (2002, 2008). What remains is cutting every summer, with cash paying 0.
- Every calendar rule tested here failed (`month-end-liquidity`, `opex-pin`, `fomc-cycle`,
  `tax-drain`, `coupon-dose`), and every survey-2 effect died after publication.

## Data

Prices only, train period. The six assets; the 8 other ETFs; the four indexes.

## Rule (no fitted parameter)

- Weekly decisions on Friday's close, as always. The coming week is a **winter week** if the
  Monday after the decision (decision day + 3 calendar days) falls in November to April.
- `tsmom12` on the six assets; a stock slot (SPY, QQQ; in the other sets IWM, EFA, EEM and the
  four indexes) keeps its weight only in winter weeks; in summer weeks it is cash. TLT, GLD,
  coins (and IEF, LQD, VNQ, DBC, SLV): untouched.

## Variants (all that will be run)

1. `halloween` (primary): the gate above on top of `tsmom12`.
2. `halloween-alone`: R12's own rule for the stock slots: the full equal slot in winter weeks
   whatever the trend, cash in summer weeks; other assets plain `tsmom12`.

## Twin and baselines

Twin `tsmom12`; equal weight shown. Also shown (no extra row): each variant rescored with T-bill
interest on cash; a descriptive table: SPY mean daily open-to-open return in winter minus summer
weeks (by the rule's week assignment), Welch t, for 1994-1998-10 (in R12's sample), 1998-11 to
2012-04 (R13's new data), 2012-05 to the end of train (after every sample I could confirm); the
S&P 500 index close to close for 1962-1969 (before R12) and 1970-1993 (in it).

## Out of universe

- The 8 other ETFs as a `tsmom12` book, the gate on IWM, EFA, EEM.
- The four indexes as one `tsmom12` portfolio from 1962, the gate on all four.
- Coins: not applicable (no source claims it there).

## Pass bar

The default in `protocol.md` for each variant against `tsmom12`, with these readings:

1. (stricter) **p < 0.10 / 65 = 0.00154** (the lineage's family, 61 + survey-4's 4; this is the
   16th tested). Both variants are one mechanism's tries.
2. Ahead of the twin in at least 4 of the 5 eras.
3. Max drawdown not more than 5 points worse than the twin's.
4. Sharpe difference positive on both out-of-universe sets.
5. Beats equal weight on Sharpe.
6. (card, after the sample) Not behind `tsmom12` on Sharpe over 1998-11-01 to the end of train
   (after R12's sample).
7. (card, after the samples) Not behind `tsmom12` over 2012-05-01 to the end of train, and SPY's
   winter-minus-summer spread there positive.

Held-out year: once, for a variant that passes all seven (primary first), only then.

## My guess before any number

Chance any variant passes: 1%. `halloween` against the twin: -0.05 to +0.05 Sharpe, p far
above the bar; `halloween-alone` worse (holds stocks through the 2001-02 and 2008 winters).
SPY winter-minus-summer after 2012-05: positive but t < 2.

## Result

Tested 2026-11-18: **fails train, both variants** (`halloween` bars 1, 2, 6, 7). `halloween`
0.96 against 1.05 (-0.08, p 0.87), 0 of 5 eras; ahead only in 1998-11 to 2012-04 (+0.06), the
years of R13's new data; after 2012-05 -0.14. SPY winter minus summer: +5.9 bps a day (t 1.3)
in 1998-2012, -0.5 (t -0.1) after. Out of universe positive (ETFs +0.09, indexes +0.13, old
years). Table `results/halloween.md`; verdict `survey-4.md`. Held-out year unspent.
