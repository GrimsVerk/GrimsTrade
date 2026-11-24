# halving-2: does the halving phase rule transfer to other halving coins?

Status: **card only (2026-11-24 19:20 UTC), written and pushed before any price of the coins
below was read.** Branch `halving-2`. Research only: fake money, cached keyless data, no change
to the gym, the daily runner or the live strategies. Train data only (no bar after 2025-11-10).

## Card

### What was seen before

- `research/cards/halving.md`, `results/halving.md`, `results/halving-shift.md`: on the six live
  assets `halving-alone` (coins held except days 548-912 after the last Bitcoin halving, ETFs on
  `tsmom12`) has Sharpe 1.28 against `tsmom12`'s 1.05: **+0.23**, z about 3.2-3.6 (errata-2 1a),
  the largest lead seen on the main test. The edge sits in BTC's 2014, 2018 and 2022 winters; the
  window comes from folklore that had seen them; moved six months it halves or vanishes.
- The project-wide bar (`research/register/BAR.md`): **z >= 4.69** over `tsmom12` at N = 486
  effectively independent trials (+0.30 close rule, +0.56 far rule; Bonferroni p <= 1.0e-04).
  At the ONC-cluster count (N = 12) it would be z >= 3.29.
- No price of LTC, ZEC, BCH, BSV or ETC was read for this card. The halving dates were read
  from on-chain issuance (block reward per block, a non-price series) and a block explorer.
- From public memory of coin history (not computed): Litecoin rose many-fold in 2017 and in early
  2021, and those years sit inside its own windows (below). **Prior: the own-clock rule fails on
  LTC.** Stated so the result cannot be read as a surprise either way.

### Hypothesis

H1 (transfer, own timing). If halvings drive the cycle through supply, stepping out of a coin
in days 548-912 after **its own** last halving should improve its Sharpe, as it did for BTC.
The coins where this can be told apart from BTC's own cycle are those whose halvings fall at
least six months from BTC's: **Litecoin** (8.5-10.5 months before BTC's) and **Zcash** (6-7
months after).

H0 (BTC-beta). Altcoins follow BTC's cycle. Then the rule with **BTC's** dates works on them
and the rule with their own dates does not (or no better): `halving-alone` is a BTC calendar
effect resting on BTC's three cycles, and the alts add no independent evidence.

### Halving dates (verified; UTC day of the cut)

Source 1: Coin Metrics community daily metrics, `IssTotNtv / BlkCnt` (new coins per block,
derived from the chain itself): the date is the first daily bucket whose per-block issuance
falls below the old reward (the same convention as BTC's frozen dates in `lib/macro.py`, which
it reproduces exactly). Source 2: the protocols' heights (Bitcoin and forks 210,000 blocks;
Litecoin 840,000 blocks; Zcash ZIP 208/Blossom heights; ETC ECIP-1017 5,000,000-block eras),
and for BSV 2024, where Coin Metrics has no issuance, the WhatsOnChain explorer
(`api.whatsonchain.com/v1/bsv/main/block/height/840000`: 2024-04-13 17:37 UTC).

| Coin | Cut | Heights | Dates (train) | Role |
|---|---|---|---|---|
| BTC | 50% | 210k, 420k, 630k, 840k | 2012-11-28, 2016-07-09, 2020-05-11, 2024-04-19 | the frozen BTC clock |
| LTC | 50% | 840k, 1.68M, 2.52M | 2015-08-25, 2019-08-05, 2023-08-02 | **H1 test set** |
| ZEC | 50% | 1,046,400; 2,726,400 | 2020-11-18, 2024-11-23 | **H1 test set** |
| BCH | 50% | 630k, 840k | 2020-04-08, 2024-04-03 | shown only (dates within 6 weeks of BTC's) |
| BSV | 50% | 630k, 840k | 2020-04-09 (explorer: 04-10 00:48 UTC), 2024-04-13 | shown only (as BCH) |
| ETC | 20% | 5M, 10M, 15M, 20M | 2017-12-11, 2020-03-17, 2022-04-25, 2024-05-31 | shown only (not a halving) |
| DASH | 7.14% every 210,240 blocks (~383 days) | - | yearly | not run: the next cut comes before day 548, so the window never opens |

Not halvings and left out: Zcash's Blossom upgrade (2019-12-11: block time and reward per block
both halved, issuance per day unchanged); Dogecoin (six reward steps in 2014-2015, then fixed
issuance: one window, on thin early data). Monero (tail emission) has no schedule to use.

In-train own windows (days 548-912 after the coin's last halving):
LTC 2017-02-23..2018-02-22, 2021-02-03..2022-02-02, 2025-01-31..2025-11-09 (cut by train end);
ZEC 2022-05-20..2023-05-19; BCH 2021-10-08..2022-10-07 (+ 2025-10-03 on, 5 weeks); BSV
2021-10-09..2022-10-08 (+ 2025-10-13 on, 4 weeks). BTC's: 2014-05-30..2015-05-29,
2018-01-08..2019-01-07, 2021-11-10..2022-11-09, 2025-10-19 on.

### Rule (frozen exactly as on BTC; no retuning)

`halving-alone` on one coin: the coin's slot is held every week except when
548 <= (days since the coin's last halving) < 913; then the slot is cash. Before the first
halving the coin is held. Weekly decision on Friday (`common.weekly`), 365 bars of history
before a coin can be held (`common.eligible`), equal slots across eligible coins, fills and
fees from `grimstrade.gym` unchanged (next open, Kraken taker tiers), cash earns 0 (the original
test's convention). The window check is the same arithmetic as `macro.halving_bear`, with the
coin's own calendar (a test proves it equals `macro.halving_bear` on every day 2010-2026 when
given BTC's calendar).

Variants (all that will be run; idea `halving-2`, kind `robustness`, controls `baseline`):

- `alone-own`: the rule with each coin's own dates (H1).
- `alone-btc`: the rule with BTC's dates on the same coin (H0).
- `and-own`: own window AND the coin's `tsmom12` (the BTC card's primary form), shown only.
- Controls: `bh` (the coin's own buy-and-hold, same slots) and `tsmom12` (held while its 365-day
  return is positive).

Universes: `LZ` = LTC + ZEC as one equal-slot portfolio (**the judged test**); each coin alone
(LTC, ZEC, BCH, BSV, ETC: shown); BTC alone with the BTC clock (shown: a replication of the
known in-sample result on this data source, and its own placebo rank).

### Data

Coin Metrics community API (keyless), daily `PriceUSD`, snapshot 2026-11-13 in the shared cache
(`<cache_root>/coinmetrics/full/2026-11-13/assets/<coin>/page-000.json`, `macro.cache_root()`).
Bars: close of day d = `PriceUSD` of d (Coin Metrics fixes it at 00:00 UTC of d+1, the gym's
crypto close time), open = the previous day's close (coins trade around the clock), high/low =
max/min of the two, volume = reported spot volume. A decision on day d sees closes through d-1
and fills at the open of d+1: a one-day lag, no look-ahead. The loader never keeps a row dated
after 2025-11-10 (asserted, and tested). Each test starts when its first coin has 366 days of
prices and ends 2025-11-09.

### Statistics and placebos (per `research/gate-null.md`)

- S1 = annual Sharpe of `alone-own@LZ`. Placebo family: 40 placebos; in each, every coin's whole
  calendar is moved by its own shift s, drawn once with `numpy.random.default_rng(20261124)` as
  a uniform integer in [365, P_min - 365] days with a random sign (P_min = the coin's shortest
  spacing between halvings: LTC 1,441, ZEC 1,466, BTC 1,319), so no placebo window overlaps a
  true one. The shifted calendar is extended by one implied halving before the first and one
  after the last at the coin's mean spacing, so every placebo has windows across the sample.
  Halving dates are scheduled, not moved by prices, so both directions are allowed. Same code
  path (a `shift` argument). The rank decides: the true S1 must be among the 2 highest of 41.
- S2 = annual Sharpe of `alone-btc@LZ`, ranked against 40 placebos of the BTC calendar moved the
  same way (shifts in [365, 954]).
- C2 (own timing net of BTC): mean daily log return of the coin priced in BTC (`PriceUSD` coin /
  BTC) on days inside its own windows minus days outside, pooled over LTC and ZEC, from each
  coin's eligibility to 2025-11-09. Predicted negative. Ranked against the S1 placebo calendars
  (the same shifts); among the 2 most negative of 41 to count.
- Differences: paired stationary bootstrap (`stats.sharpe_diff_boot`, mean block 20 days, 2,000
  draws); z = difference / ((q95 - q05) / 3.29).
- Every placebo result prints the null's spread: SD, 5/50/95% quantiles, extremes, mean
  exposure of the placebos next to the true rule's.

### Pass bar (fixed now; all on `LZ`)

H1 "transfers, own timing" needs all of:

1. S1 ranks 1 or 2 of 41 (empirical p <= 0.049);
2. `alone-own` beats `bh` on Sharpe with z >= 2;
3. `alone-own` beats the coins' own `tsmom12` on Sharpe;
4. `alone-own` beats `alone-btc` on Sharpe, and C2 is negative and among the 2 most negative
   of 41.

Reading, written before the run:

- **All four hold:** the phase rule transfers on the coins' own clocks. Not dead; still not a
  pass of the project bar (below). Next step would be the forward watch (BTC's window that
  opened 2025-10-19; LTC's next halving about 2027-07).
- **H1 fails, and `alone-btc@LZ` ranks 1-2 of 41 among BTC-calendar placebos with z >= 2 against
  `bh`:** BTC-beta. The alts follow BTC's cycle; `halving-alone` is a BTC calendar effect on
  BTC's three cycles. The alt data add no independent evidence; the z gap stays open.
- **Both fail:** no transfer. `halving-alone` reads as a BTC-only, in-sample coincidence.

### Power caveat (why this gate is kill-only)

The judged set has about **3.75 own windows** in train (LTC 2017, 2021, ten months of 2025; ZEC
2022). A 365-day window on a ~4-year clock has only about four non-overlapping phase positions,
so neighbouring placebos are not independent draws, and all coins share the crypto market's
regime. The smallest honest p is therefore about 1/4 to 1/16, not 1/41, far above the family
bar and the register's 1.0e-04. **This gate is kill-only** (gate-null step 7): a fail kills the
transfer reading; a pass only says "not dead". No test on four episodes can lift
`halving-alone` over z 4.69; what this test can do is show whether its +0.23 has any support
outside BTC's own three cycles.

### What it means for `halving-alone` (pre-stated)

Its z of 3.2-3.6 is below the bar 4.69 and inside the band (3.29-4.69) where the counting
method decides. A transfer pass would be the first evidence from other halving schedules; it
would not change the trial count or the bar. A fail (either kind) means the lead has no support
beyond the three BTC cycles the window was taken from: treat it as a BTC-only coincidence and
stop spending tests on the halving family until the forward window is in.

## Result

Pending: script `research/lib/halving2.py` (core `research/lib/halving2_core.py`, tests
`tests/test_halving2.py`), one dry run (counts only), then one real run.
