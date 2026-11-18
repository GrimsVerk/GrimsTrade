# Wide 3: two more mechanisms from wide-1's list

Research run wide-3, 2026-11-18. Branch `wide-3` (from `wide-2`). Research only: fake money,
public data, no change to the gym, the daily runner or the live strategies.

## Step 1. Choice (pushed 2026-11-18 19:05 UTC, commit 3dea3e7, before any number of this run)

### The count, kept honest

wide-1's list has 46 numbered mechanisms (E1-E6, P1-P4, S1-S5, C1-C5, I1-I5, G1-G4, F1-F5,
Q1-Q6, N1-N3, M1-M3). Cards so far: 7 (wide-1: `auction-concession` = E5 and Q1,
`contagion-catchup` = P1 with F5 as its tool, `vol-echo` = S4, `rebalance-pressure` = C2;
wide-2: `trend-age` = Q5, `patch-leaving` = E6, `crowded-trend` = G2). Those 7 cards cover 9
of the 46 entries, so 37 entries were uncarded before this run, not 39 as wide-2 wrote (two
cards each cover two entries). This run adds 2 picks: **9 tests out of the list, 11 entries
covered, 35 left.**

**Bar 1 for this run: p < 0.10 / 46 = 0.0022.** The family the picks are drawn from is the
whole list of 46, whatever is left of it; wide-2 used 0.10 / 42, which this is slightly
stricter than. Bars 2-5 as in `protocol.md`.

### What I ruled out before choosing, and why

- **Lanes that other runs are already working on** (seen by PR title only, no PR body or
  result read): `volume-1` (#41) covers Q3 (price impact per dollar traded, volume);
  `month-end-bonds` (#45) covers S2 (lock-in on the monthly cycle); `cointop-1` (#40) and
  `slow-1` (#35) are near N2 (variance risk premium at slow horizons) and coin tops. Picking
  any of these would test the same thing twice.
- **Another change to when or how much of the trend book is held** (the coordinator's rule
  and wide-2's lesson): S1, C1, C5, I1, I2, G1, N3 (the 52-week-high anchor is a trend
  measure), M2.
- **The "step out of risk when X" gates**, which cannot be validated on 4-7 bear markets: P3,
  I4, F1, F4, M1.
- **Dead or killed by a measured number**: Q2 and G4 (reversal, costs), N1 and E2 (two
  sibling pairs, no cross-sectional edge), S3, S5, C4, E3, E4, P4, I3, I5, G3, F3, M3.
- **Data we do not have** or paid: E1, Q4, Q6.

That leaves three: **F2** (stock-bond correlation as an order parameter), **P2** (attention as
the infection, on free Wikipedia page views) and **C3** (volatility-control funds keep selling
after a spike). C3 is close to `dip-rsi2` (real and small) and to `vol-echo` (dead). I pick F2
and P2.

### Pick 1: F2, `hedge-regime` (statistical physics: order parameter)

- **Reason.** It is the only uncarded mechanism that changes *what* the idle part of the book
  holds rather than when the trend rule acts, and it reads a quantity no rule here has used as
  a rule: the sign of the stock-bond correlation. The mechanism has a clear physical reading:
  the sign is an order parameter. Below zero, bonds are insurance (flight to quality: their
  price rises when stocks fall), and insurance pays off in the weeks when the trend rule is
  still long stocks. Above zero (inflation regime: 1970s, 2022), bonds and stocks fall
  together and the bond must earn its slot by its own trend. `tsmom12` drops TLT whenever TLT
  is below its level of a year ago, even in a regime where it hedges the stocks it holds.
- **Why it is not a duplicate.** `trend-to-safe` gave empty slots to safe assets *in trend*;
  this holds the bond *out of trend*, and only when the order parameter says it hedges.
  wide-1 killed F2 as "a refinement of `trend-to-safe`; one flip since TLT exists". The second
  half is the real objection: since 2002 the sign was negative almost all the time until 2021,
  so the test is close to "hold TLT always until the flip". That is a power problem, stated
  here before the number.
- **Prior.** Low: about 2% that it passes; difference -0.04 to +0.05 Sharpe.

### Pick 2: P2, `attention-peak` (epidemiology: SIR on attention)

- **Reason.** It is the only uncarded mechanism whose data no run has ever read: Wikipedia page
  views, free and keyless from 2015-07. The SIR reading: a mania is an epidemic of attention;
  the price is carried by newly "infected" buyers, and once new infections fall after a surge,
  the pool of new buyers is used up and the price has nothing left to carry it. `tsmom12` exits
  coins about a year after the top (the 365-day return must turn negative), so an exit at the
  attention peak could matter a lot in the asset class that sets the book's drawdowns.
- **Why it is not a duplicate.** It reads attention, not price: the exit can come while the
  12-month trend is still strongly positive. It is a gate, which is the weak family, and wide-1
  parked it for that reason ("three manias, all coins at once"). It is picked anyway because
  its data is clean (never seen by any rule) and the payoff, if real, is large.
- **Prior.** About 3% that it passes; difference -0.10 to +0.15 Sharpe (wide range: few
  episodes).

Cards: `cards/hedge-regime.md`, `cards/attention-peak.md`, each pushed before any number.

## Pick 1 result: hedge-regime (run once, 2026-11-18 19:08 UTC, train only)

**It fails. Holding TLT out of trend while it hedges stocks changes nothing: Sharpe 1.05
against 1.05 for `tsmom12` (difference +0.003, p 0.39), and -0.006 on the other ETFs. The
held-out year was not looked at.** Table: `results/hedge-regime.md`; 2 rows in `tries.md`
(1 variant, 1 robustness).

| | `hedge` | `tsmom12` |
|---|---:|---:|
| Sharpe, six assets, 1994-2025 | 1.05 | 1.05 |
| Difference (p; 90% range) | +0.00 (0.39; -0.01 to +0.02) | |
| Eras ahead (from 2000-09) | 3 of 4 (by 0.00-0.04 each; behind in 2022-25 by 0.09) | |
| Max drawdown | 35.8% | 36.5% |
| 2022 rate shock | -17% | -13% |
| Other ETFs (IEF, LQD) | -0.006 (p 0.78) | |

Bars 1 and 4 fail; 2, 3 and 5 pass.

**What it shows.**

1. **The power problem was worse than stated on the card, and in a different place.** TLT's
   one-year correlation with stocks was below zero on 81% of Fridays and in every week of
   2008-2020; it turned positive only in 2023 (mean +0.14 in 2023, +0.16 in 2024), not in 2021
   as I remembered. One flip, as feared.
2. **The weeks the rule adds are worth nothing.** On the 267 Fridays where `hedge` holds TLT and
   the twin does not, TLT earned +1.2 bps a week (t 0.1), +3% in all. Out of trend, the bond
   was neither insurance that paid nor drift worth having: when TLT is below its level of a year
   ago in a hedge phase, the stocks it would hedge are usually doing fine.
3. **A one-year order parameter is too slow for the one flip that mattered.** In 2022 rho was
   still below zero on 85% of Fridays, so the rule held TLT into the bond crash (-17% against
   -13% for the twin). That is where the 2022-25 era is lost.

**How sure.** Sure that it adds nothing on these assets: the 90% range of the difference is
-0.01 to +0.02, and the out-of-universe bonds agree. Not a test of the phase idea on data with
many flips (1962-2000 bond yields would have some); our ETFs have one.

**Compared with my guess** (card): 2%, -0.04 to +0.05. It came out at +0.00, inside the range.
