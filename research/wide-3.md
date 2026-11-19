# Wide 3: two more mechanisms from wide-1's list, and three new ones

Research run wide-3, 2026-11-18. Branch `wide-3` (from `wide-2`). Research only: fake money,
public data, no change to the gym, the daily runner or the live strategies.

## In plain words (results, 2026-11-18)

**All three ideas tested fail against the 12-month trend rule (`tsmom12`, Sharpe 1.05). The
held-out year was not looked at.**

| Idea (field) | In one line | Sharpe vs 1.05 | Why |
|---|---|---:|---|
| `hedge-regime` (physics, F2) | Keep TLT out of trend while it moves against stocks | 1.05 (+0.00) | The sign flipped once (2023); the added bond weeks earned nothing (+1 bp a week) |
| `attention-peak` (epidemiology, P2) | Leave a coin once its Wikipedia attention has surged and turned down | 1.02 (-0.03) | Caught the 2017 top, but attention peaked at the start of the 2021 rally, not its end; other coins 0.33 vs 0.54 |
| `opex-pin` (physics/control, new W1) | Idle cash into stocks for the option-expiry week | 1.01 (-0.04) | The expiry week is an average week since 1994 (-0.3 bps); buying stocks in a downtrend costs, whatever the week |

Three new mechanisms were added to wide-1's list (W1-W3); W2 `tax-drain` and W3 `lunar` are
written up with test plans and untested. Count: 49 mechanisms, 10 tested, none passed; the bar
for the next is p < 0.10 / 49.

What it adds to wide-1 and wide-2: the two remaining "different input" ideas on the list (a
correlation regime, outside attention data) fail the same way the price-only ones did, and the
trend rule's idle cash is not a free resource: it is idle because the assets it could buy are
falling.

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

## Pick 2 result: attention-peak (run once, 2026-11-18 19:11 UTC, train only)

**It fails: Sharpe 1.02 against 1.05 for `tsmom12` (difference -0.03, p 0.74), behind in
both eras in which it can act, and -0.21 on the six other coins. The held-out year was not
looked at.** Table: `results/attention-peak.md`; 2 rows in `tries.md` (1 variant, 1
robustness). Page views: 9 titles downloaded once (`lib/wide3_pageviews.py`), every series
from its first day to 2025-11-10; none was printed or plotted before the run.

| | `peak` | `tsmom12` |
|---|---:|---:|
| Sharpe, six assets, 1994-2025 | 1.02 | 1.05 |
| Difference (p; 90% range) | -0.03 (0.74; -0.09 to +0.03) | |
| 2017-21 / 2022-25 | 1.37 / 0.88 | 1.50 / 0.88 |
| Max drawdown | 37.6% | 36.5% |
| Crypto winter 2018 | -17% | -22% |
| Other coins | 0.33 against 0.54 (-0.21, p 0.85) | |

Bars 1, 2 and 4 fail; 3 and 5 pass.

**What it shows (from the spell table).**

1. **It saw the one classic mania.** BTC was out from 2017-12-15 to 2018-01-19, while BTC fell
   47% (log) and the twin held it the whole time. That is the epidemic story exactly, and it is
   why the 2018 winter cost 17% instead of 22%.
2. **Every other surge was a false alarm, and the costly ones were early in a run.** Attention
   peaked in January 2021 for both coins; the rule left ETH from 2021-01-15 to 2021-04-30 while
   ETH rose 109%, and BTC twice in early 2021 (+26%, -2%). In 2021 attention peaked at the
   *start* of the bull market (the first move above the old high), not at its end: the
   November 2021 top, the one that mattered, did not trigger the rule at all.
3. **Smaller coins surge and fade constantly.** 48 out spells on six other coins, turnover up
   from 4.6 to 6.8 a year at 60 bps a round trip, Sharpe 0.33 against 0.54.

So the mechanism fires on one real top in 2017 and on several starts of rallies. With four or
five distinct episodes the sign could have gone either way; here it went against.

**How sure.** Sure enough that it does not help: behind on the six assets and clearly behind
on the six other coins. Not proof that attention carries no information: English Wikipedia may
be the wrong audience after 2018 (the November 2021 top did not trigger it), and one form of the rule
was tested, on purpose.

**Compared with my guess** (card): 3%, -0.10 to +0.15. It came out at -0.03, inside the range.

## Step 3. Three new mechanisms, and a test of the best one

Both picks failed, so three mechanisms that are not in wide-1's list were written down before
any number (`wide-1.md`, last section; pushed in d63aade): **W1 `opex-pin`** (physics/control:
option dealers' hedging damps the market into the monthly expiry), **W2 `tax-drain`**
(hydraulics: tax dates drain bank reserves into the Treasury's account) and **W3 `lunar`**
(chronobiology). The family is now 49 and a test is read at p < 0.10 / 49 = 0.0020. W1 was
carded (`cards/opex-pin.md`, pushed in 3d0a81a) and tested.

## W1 result: opex-pin (run once, 2026-11-18 19:16 UTC, train only)

**It fails, and the mechanism is not there at the index level: the expiry week earned no more
than an average week on SPY over 1994-2025 (-0.3 bps, t -0.02, 381 weeks). The overlay is
behind the twin (1.01 against 1.05) and behind its own placebo week (1.03). The held-out year
was not looked at.** Table: `results/opex-pin.md`; 4 rows in `tries.md` (1 variant, 3
robustness: the placebo `pin-after` and the two out-of-universe sets).

| | `pin` | `pin-after` (placebo week) | `tsmom12` |
|---|---:|---:|---:|
| Sharpe, six assets | 1.01 | 1.03 | 1.05 |
| Difference to the twin (p) | -0.04 (0.76) | -0.02 (0.64) | |
| Max drawdown | 40.6% | 35.3% | 36.5% |
| Turnover a year | 9.4 | 9.4 | 2.7 |
| Other ETFs / indexes | -0.14 / -0.08 | | |

| Expiry week minus the average week (close to close) | Weeks | bps | t |
|---|---:|---:|---:|
| SPY 1994-2025 | 381 | -0.3 | -0.02 |
| SPY 1994-99 / 2000-09 / 2010-16 | 71 / 120 / 84 | +26 / +8 / +5 | +1.1 / +0.3 / +0.3 |
| SPY 2017-21 / 2022-25 | 60 / 46 | -38 / -26 | -1.1 / -0.7 |
| S&P 500 index 1962-01 to 1983-02 (placebo: no listed index options) | 254 | -0.2 | -0.02 |
| S&P 500 index 1983-03 to 1993-01 | 119 | +19 | +1.0 |

**What it shows.**

1. **The sign of the story, and its decay.** Nothing before listed index options (1962-1983),
   +19 bps a week in 1983-1993 and +26 in 1994-99, then a steady fade to below zero after 2017,
   when short-dated options and dealers' short positions grew. That is the shape the mechanism
   predicts if dealers were long options then and are not now, but no single period has t
   above 1.1. Not supported by the card's reading (t >= 2 on SPY 1994-2025).
2. **Idle cash in stocks is idle because stocks are out of trend.** The overlay buys stocks one
   week a month in bear markets: the dot-com bust cost 40% instead of 28%, and 2022 25% instead
   of 13%. The placebo week does the same with less damage, so most of the loss is the timing
   of *any* stock week in a downtrend, not the expiry week in particular. This is wide-1's
   lesson 3 seen from the other side: the trend rule's cash is not free money waiting for a
   use; it is cash because the obvious use is losing.

**How sure.** Sure the expiry week carries nothing at the index level in our period: 381 weeks
with a mean of zero. The 1983-1999 values are suggestive and could be chance (t about 1).

**Compared with my guess** (card): 2%, -0.01 to +0.03, event study +0 to +20 bps. It came out
at -0.04 and -0.3 bps: below both ranges.

## Status (2026-11-18)

**Done:** choice note, cards and one train run each for `hedge-regime` (F2), `attention-peak`
(P2) and the new `opex-pin` (W1); three new mechanisms in wide-1's list; `ideas.md`;
`next-steps.md`. All three fail; held-out year unspent. Draft PR #54 (`wide-3` -> `wide-2`).

**Count after this run:** 46 listed + 3 new = 49 mechanisms; 10 carded and tested (wide-1: 4,
wide-2: 3, wide-3: 3); none passed. Of the 46, 11 entries are covered by cards and 35 are not;
of the 3 new, W2 and W3 are untested. Any next pick is read at p < 0.10 / 49.

**Doing:** nothing half-finished. No process running.

## Disclosures

- **One run each, no dry run.** `hedge-regime` 19:08 UTC, `attention-peak` 19:11 UTC,
  `opex-pin` 19:16 UTC. Plumbing was checked by `tests/test_wide3.py` on
  synthetic bars and synthetic page views (each rule does what its card says; no bar or view
  after the decision is read).
- **Times on the choice note and the first two cards** were written as guesses ("~19:20" to
  "~19:30 UTC") and later than the real clock; after the first run they were corrected to the
  commit times (3dea3e7, f25b507). Nothing else on those cards changed.
- **The choice of picks used PR titles of other lanes** (`volume-1`, `month-end-bonds`,
  `cointop-1`, `slow-1`) to avoid testing the same thing twice. No PR body or result of
  those lanes was read.
- **Page views** were downloaded once, after the card was pushed; the download script printed
  only the number of days per title. A title with missing days counts 0 views on those days;
  `XRP_Ledger` has data only from 2018-08-24 and is summed with the old title, as the card says.
- **`attention-peak` eras.** The card's reading (2 of 2 eras from 2017-21) is stricter than
  any looser count; the rule cannot act before 2016-07.
- **`opex-pin` event study** uses closes (close of the pre-expiry Friday to close of the expiry
  Friday), not the gym's next-open fills; it has no row in `tries.md`. Third Fridays that are
  holidays are kept on the calendar Friday.
- **Price cache:** copied from the wide-2 worktree. `tsmom12` and equal weight reproduce 1.05
  and 0.88.
- **Not run:** the held-out year, for any of the three.
