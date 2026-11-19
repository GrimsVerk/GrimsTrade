# Wide 4: the tax-date reserve drain, and five new mechanisms from unused fields

Research run wide-4, 2026-11-18. Branch `wide-4` (from `wide-3`), draft PR #57. Research only:
fake money, public data, no change to the gym, the daily runner or the live strategies.

## In plain words (results, 2026-11-18)

**Both ideas tested fail against the 12-month trend rule (`tsmom12`, Sharpe 1.05). The
held-out year was not looked at.**

| Idea (field) | In one line | Sharpe vs 1.05 | Why |
|---|---|---:|---|
| `tax-drain` (hydraulics, W2) | Out of SPY, QQQ, TLT for five sessions around each federal tax date, since 2008 | 1.03 (-0.016, p 0.88) | The drain is real (the Treasury's Fed account jumps +88 $bn on tax dates since 2008, +1 $bn before), and prices fall a little in the predicted order (most while the Fed shrank reserves: SPY -62 bps, t -1.3), but not enough to pay for stepping out every time |
| `coupon-dose` (pharmacokinetics, new W4) | Idle cash into TLT for four sessions when the Treasury pays back cash net on the 15th | 1.04 (-0.011, p 0.71) | Bonds did no better on net-payment days than on net-issuance days (+2 against +18 bps); the wrong sign since 2014 |

Five new mechanisms (W4-W8: pharmacokinetics, seismology, actuarial science, materials
fatigue, metrology) were added to wide-1's list with test plans. Count: **54 mechanisms, 12
tested, none passed; the next test is read at p < 0.10 / 54 = 0.00185.** The fact wide-3 wrote
from memory (tax receipts moved from bank accounts to the Fed in 2008) is right, with a
condition the source adds: the drain only bites when reserves are scarce.

## Step 1. W2 `tax-drain` (hydraulics: a reservoir drained on dates fixed by law)

### The fact, checked before the card

wide-3 wrote from memory that tax receipts moved from commercial-bank accounts to the Fed in
2008. Checked against Santoro, "The Evolution of Treasury Cash Management during the Financial
Crisis", NY Fed *Current Issues* 18(3), 2012 (quotes and details on the card):

- Before Lehman the Treasury held its Fed account (TGA) near a $5 billion target (since 1988)
  and parked the rest in Treasury Tax and Loan accounts at banks, precisely so as not to drain
  reserves; the Fed offset what was left with open-market operations.
- From late 2008 (interest on reserves from October, the 0-0.25% target range from 2008-12-16)
  it paid the Treasury to keep its cash in the TGA; TT&L fell to about $2 billion, was kept
  until 2011-12-29, and the program was shut by 2012.
- The source adds a condition wide-3 did not have: with abundant reserves, TGA swings "did not
  put upward pressure on the funds rate". So the card split the period into A (TT&L era,
  placebo), B (TGA era, abundant reserves) and C (TGA era while the Fed shrank its balance
  sheet: 2018-19 and from 2022-06), before any number.

Card `cards/tax-drain.md` pushed in 6b17ce8; one amendment before any value was read
(491c15a: FRED refused automated downloads, so the first stage uses the Treasury's Daily
Treasury Statement, daily from 2005-10). Code pushed in 4717b0d before the logged run.

### Result (run once, 2026-11-18 19:28 UTC, train only)

**It fails: Sharpe 1.03 against 1.05 for `tsmom12` (difference -0.016, p 0.88), 4 of 6 bars
failed, behind its own placebo. The held-out year was not looked at.** Table:
`results/tax-drain.md`; 4 rows in `tries.md` (1 variant, 3 robustness: placebo `drain-ttl`,
other ETFs, S&P 500 index).

| | `drain` | `drain-ttl` (placebo) | `tsmom12` |
|---|---:|---:|---:|
| Sharpe, six assets, 1994-2025 | 1.03 | 1.04 | 1.05 |
| Difference to the twin (p) | -0.016 (0.88) | -0.008 (0.62) | |
| Eras 2010-16 / 2017-21 / 2022-25 | 1.42 / 1.49 / 0.99 | | 1.55 / 1.50 / 0.88 |
| Max drawdown | 37.9% | 36.5% | 36.5% |
| Turnover a year | 5.7 | 3.0 | 2.7 |
| Other ETFs / S&P 500 index | -0.013 / -0.005 | | |

**First stage: the drain is real and large.** The TGA's change from session D-2 to D+1, minus
an average 3-session change:

| Regime | Tax dates | Excess | t |
|---|---:|---:|---:|
| A, TT&L era (2005-10 to 2008-09 only) | 14 | +1.3 $bn | +2.0 |
| B, TGA era, abundant reserves | 56 | +72 $bn | +10.2 |
| C, TGA era, reserves shrinking | 27 | +122 $bn | +11.2 |

So the source's account is confirmed on the data: before 2008 a tax date barely moved the
Fed account; since then it pulls $70-130 billion of reserves out of the banks within days.

**Prices: the predicted sign, a dose-response, and not enough to clear the card's reading.**
Close of D-2 to close of D+3, minus an average 5-session return of the same regime (bps):

| | A (placebo) | B | C | B+C (t) |
|---|---:|---:|---:|---:|
| SPY | -9 | -11 | -62 (t -1.3) | -27 (-1.2) |
| TLT | +7 | -7 | -47 (t -1.4) | -20 (-1.2) |
| IEF | +7 | -14 | -22 (t -1.4) | -16 (-2.1) |
| LQD | +17 | -12 | -26 (t -1.3) | -17 (-1.6) |

Card's reading: (a) first stage yes, (c) placebo not more negative yes, (b) SPY with t <= -2
in B+C or C **no**. Mechanism **not supported**.

**What it shows.**

1. **All four assets line up the way the mechanism says**: about zero (bonds slightly
   positive) in the TT&L era, slightly negative with abundant reserves, most negative while
   the Fed shrank reserves. That ordering was written on the card before the run. But C has
   27 dates, and no single cell reaches t = 2 except IEF over B+C; four correlated assets are
   not four tests.
2. **The rule cannot harvest it.** It is out of three slots for five sessions on five dates a
   year, also in regime B where the effect is about -10 bps, and it doubles turnover. It loses
   0.13 Sharpe in 2010-16 (all regime B) and gains 0.11 in 2022-25 (mostly regime C). A rule
   active only in C would have looked better; that is post hoc and was not run.
3. **Lesson for the list**: verifying the institutional fact changed the test. wide-3's plan
   (placebo 1994-2007, effect 2008-2025) would have pooled the abundant-reserve years, which
   the source says should show nothing, with the years that matter.

**How sure.** Sure the rule as carded does not help (behind on all three books, behind its
placebo). Not sure the mechanism is absent: the price trace is consistent with it and the
first stage is overwhelming, but the regime in which it can bite is short. Worth a forward
look only as an event study in future regime-C years, not as a trade on this book.

**Compared with my guess** (card): 1-2%, -0.02 to +0.03, SPY in C -50 to +20 bps, A about
zero. It came out at -0.016, SPY in C -62 bps (just below the range), A -9 bps.

### Disclosures (step 1)

- **One dry run** (`DRY=1`, last 120 days, nothing logged) to check the plumbing, with its
  output sent to `/dev/null` and its result file deleted unread. Then one logged run.
- **Seen before the run**: the DTS account labels and which columns are empty (to parse the
  file), and the row counts printed by the parser. No balance, return or reserve value.
- **April dates moved by Emancipation Day** (to the 17th/18th) are not modelled (card); 2020
  uses 15 July for April and June.
- **Regime A of the first stage** starts in 2005-10 (DTS); the price event study uses all of
  1994-2008 for A (77 SPY dates; TLT, IEF and LQD from 2002-07, 30 dates).
- **Price cache**: copied from the wide-3 worktree. `tsmom12` and equal weight reproduce 1.05
  and 0.88.

## Step 2. Five mechanisms from fields the list had not used, and a test of the best one

The list's fields were checked first (wide-1's ten, W1-W3's pinning, hydraulics and
chronobiology, run 1's Hawkes model, which is seismology's self-excitation). Five new
mechanisms, W4-W8, were added to `wide-1.md` (last section) with a mechanism, the reason it
might survive costs on this book, a test plan and its data, and a written choice, all pushed
in 831dedc before any number:

| # | Field x tool | In one line | Prior |
|---|---|---|---|
| W4 `coupon-dose` | pharmacokinetics x scheduled dosing, dose-response | Treasury coupons and principal paid on the 15th must be reinvested in bonds: buy order of known size | 3% |
| W5 `tidal-trigger` | seismology x tidal triggering near critical stress | Small calendar flows move prices only when dealers are already stretched | 2% |
| W6 `payday-inflow` | actuarial science x contribution annuity | 401(k) money arrives on paydays and buys stocks mid-month | 1% |
| W7 `fatigue-damage` | materials science x Basquin S-N curve, Miner's rule | Oscillations wear out leveraged coin longs; buy once they have failed | 1% |
| W8 `snapshot-shrink` | metrology x snapshot sampling (Goodhart) | Foreign banks shrink balance sheets for quarter-end leverage snapshots; bonds weak | 1% |

**Picked: W4**, the only one whose dose varies in size and is known in advance, so a
dose-response slope (with a free placebo: the days with no net dose) can be tested; a forced
flow; idle cash goes to TLT rather than to stocks in a downtrend. Card `cards/coupon-dose.md`
pushed in 37d5a0a; code in 7d04fe3, before the logged run.

### W4 result: coupon-dose (run once, 2026-11-18 19:39 UTC, train only)

**It fails, and the mechanism is not there: mid-month days on which the Treasury paid back
cash net were no better for long bonds than the days on which it took cash in. Sharpe 1.04
against 1.05 (difference -0.011, p 0.71), 3 of 6 bars failed. The held-out year was not looked
at.** Table: `results/coupon-dose.md`; 3 rows in `tries.md` (1 variant, 2 robustness: placebo
`dose-neg`, other ETFs).

| | `dose` | `dose-neg` (placebo) | `tsmom12` |
|---|---:|---:|---:|
| Sharpe, six assets | 1.04 | 1.04 | 1.05 |
| Difference to the twin (p) | -0.011 (0.71) | -0.01 (0.80) | |
| Eras 2000-09 / 2010-16 / 2017-21 / 2022-25 | 0.24 / 1.49 / 1.53 / 0.73 | | 0.19 / 1.55 / 1.50 / 0.88 |
| Turnover a year | 6.3 | 5.9 | 2.7 |
| Other ETFs (into IEF) | -0.03 (p 0.89) | | |

Event study, TLT, close of P-1 to close of P+3, minus an average 4-session return (bps, t):

| Period | Positive net dose | Zero or negative | Dose-response slope (t) |
|---|---:|---:|---:|
| 2002-07 to 2025 | +2 (0.1), 146 days | +18 (1.3), 133 days | +18 bps per 1% of debt (1.0) |
| 2002-07 to 2013 | +31 (1.3) | +38 (1.8) | +23 (1.1) |
| 2014 to 2025 | -25 (-1.4) | -3 (-0.2) | -4 (-0.1) |

Card's reading: (a) slope t >= 2 no, (b) positive doses above the rest no, (c) slope positive in
both halves no. **Not supported on any of the three.** IEF says the same (positive doses -16
bps, t -2.1, since 2014: the wrong sign).

**What it shows.**

1. **Mid-month is not a smaller month end.** The month-end bond rally (TLT +39 bps over four
   sessions, wide-1) has no mid-month counterpart driven by cash paid back: the dose has the
   wrong sign since 2014. Whatever drives the month end (index extension is the usual
   explanation) is not reinvestment of Treasury cash in general.
2. **The net dose is small and mostly settlement-driven.** The median net payment on the 15th
   is +1.2 $bn and its spread is under 1% of the debt: new issues settling the same day cancel
   most of the coupons and maturities. A dose this small could not move a market that size
   unless its holders were all forced reinvestors, and most are not.
3. **Idle cash in TLT is not free either.** The overlay put TLT into the 2022 bond crash on
   positive-dose days (2022-25: 0.73 against 0.88), the bond version of `opex-pin`'s lesson.

**How sure.** Sure the rule does not help and that the dose carries no positive slope at our
fills: 279 events, wrong sign on the point estimate where it matters. The pre-2014 half has a
positive slope at t 1.1, which is noise at this count.

**Compared with my guess** (card): 2%, -0.01 to +0.02, positive doses on a third of days, TLT
excess 0 to +25 bps, slope t 0 to 2. It came out at -0.011, positive doses on 52% of days,
+2 bps, slope t 1.0 (but the wrong ordering of the means).

## Count after this run

wide-1's 46 listed mechanisms plus W1-W3 (wide-3) plus W4-W8 (this run) = **54**. Tested: 12
(wide-1 4, wide-2 3, wide-3 3, wide-4 2: W2 `tax-drain`, W4 `coupon-dose`); **none passed**.
Of the 46, 11 entries are covered by cards and 35 are not; of the eight W entries, W1, W2 and
W4 are tested, W3 and W5-W8 are not. **The next test is read at p < 0.10 / 54 = 0.00185.**

## What wide-4 adds

- **Forced Treasury cash flows are real in the plumbing and faint in prices.** The tax-date
  drain moves $70-130 billion of reserves in three sessions since 2008; the bond and stock
  returns around it have the right sign and order by regime but t of about -1.3. The coupon
  dose does not show at all. Both rules lose to the twin by about 0.01-0.02 Sharpe, mostly
  by doubling turnover and acting in years where the effect is absent.
- **Checking the institutional fact first was worth it**: it changed the regimes of the
  `tax-drain` test and the reading of its result.
- **On the list**: of the eight W mechanisms, the two with forced Treasury flows are now spent.
  W5 `tidal-trigger` is the most interesting left, but its calendars are all seen; it could
  only be confirmed on a calendar not used to suggest it (for example, the tax-date drain in
  future regime-C years, forward). The rest (W3, W6-W8) have priors of 1%.

## Status (2026-11-18)

**Done:** fact check, card, test and verdict for W2 `tax-drain`; five new mechanisms W4-W8
with test plans; choice note; card, test and verdict for W4 `coupon-dose`; `ideas.md`;
`next-steps.md`. Both fail; held-out year unspent. Draft PR #57 (`wide-4` -> `wide-3`).

**Doing:** nothing half-finished. No process running.

### Disclosures (step 2)

- **One dry run** (`DRY=1`, nothing logged), output to `/dev/null`, result file deleted unread;
  then one logged run.
- **Seen before the run**: the auction file's field names, which rows lack a rate or an amount
  (floating-rate notes and two auctions after train), and the parser's row counts.
- **Payment calendar** built from auctions since 1979 only; securities issued earlier and still
  paying in 2002-2009 are missing (card). The Fed's add-on amounts are not in `total_accepted`.
- **The card wrote "about 140" mid-month days** in a first draft of the W4 entry; corrected to
  about 270 before the card was written (279 came out).
