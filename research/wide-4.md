# Wide 4: the tax-date reserve drain, and five new mechanisms from unused fields

Research run wide-4, 2026-11-18. Branch `wide-4` (from `wide-3`), draft PR #57. Research only:
fake money, public data, no change to the gym, the daily runner or the live strategies.

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
