# eu-3: fewer orders for a small coin-free EUR book (decision frequency and slot structure)

Field: execution structure of the house rule for a Dutch retail investor (not a new signal).
Lane `eu-3` (DEEPER), night of 2026-11-18, branch `eu-3` from `eu-2`. Written and pushed before
any eu-3 number existed. Seen before: everything in `eu-1.md`, `eu-2.md` and their result tables
(all `euw` numbers at the house structure, the fee table by book size, the band tests).

## Failure mode

On the coin-free book `euw` (SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY; 6% vol, ~3.5% a year),
fixed per-order fees make `tsmom12` not worth running below about EUR 6k (EUR 1 orders), 10k
(EUR 2) or 16k (EUR 3) (eu-2). The rule places ~30 ETF orders a year; a 5% rebalance band cut
that only to 21, because most orders are the signal's own entries and exits (about 1.5 round
trips per slot a year, some of them weekly whipsaws around a 12-month return near zero). The
question: can a slower decision clock or fewer, larger slots cut orders a lot **without changing
the rule's character**, so that `euw` is worth running at EUR 5-10k?

## What stays fixed

The signal (365-day total return > 0 holds the slot, else cash), equal-weight-by-design slots,
next-open fills, cash at 0, total-return prices, the 1% rebalance band, window W (decisions
2012-01-02 .. 2025-11-09; every member is eligible throughout), EUR, ETF slippage 0.05% a side.
Fixed fees as in eu-2 amendment 1 (`lib/eu2.py`, `fixed_fees`): a constant book, every ETF fill
costs fee / book of equity, DEGIRO's EUR 2.50 a year once per calendar year. The gym is not
changed. Nothing is fitted.

## Reference and variants (all that will be run; fixed now)

"Check" = the moment the rule looks at the signal; it decides on the check day's view (bars
closed by 22:30 UTC Friday) and fills at the next open. "Last Friday" = a Friday whose date + 7
days falls in the next month (a calendar fact, no data). Every Friday-structured run also gets
one decision on 2012-01-02 from the state of Friday 2011-12-30 (itself a last Friday), so all
runs start on the same day as the reference.

| Name | Signal checks | Entries | Exits | Trades (incl. drift top-ups) | Slots |
|---|---|---|---|---|---|
| `R` (reference, house) | every Friday | any Friday | any Friday | every day (Friday's weights repeated) | 7 x 1/7 |
| `V0 w-fri` | every Friday | any Friday | any Friday | Fridays only | 7 x 1/7 |
| `V1 m` | last Friday of the month | last Friday | last Friday | last Fridays only | 7 x 1/7 |
| `V2 m-in` | every Friday | last Friday only | any Friday (weekly risk check) | Fridays only | 7 x 1/7 |
| `V3 hold4w` | every Friday | any Friday | not before 28 days after the entry | Fridays only | 7 x 1/7 |
| `V4 c4` | every Friday | any Friday | any Friday | Fridays only | 4 class slots |
| `V5 c4-m` | last Friday of the month | last Friday | last Friday | last Fridays only | 4 class slots |

- `V0` isolates the trade clock (drift top-ups checked weekly instead of daily); `V2`, `V3`
  differ from `V0` only in when a slot may switch.
- `V2`: a slot that is in cash may be entered only on a last Friday (signal positive then); a
  held slot is exited on any Friday whose signal is negative. `V3`: a slot entered on Friday F
  may be exited only on a Friday >= F + 28 days with a negative signal; re-entry after an exit
  is allowed on any Friday (as `R`). Both are path-dependent and run as a state machine over
  Fridays.
- **Class slots** (`V4`, `V5`): one fund per asset class, at `euw`'s own class weights, so the
  mix is kept while the number of lines drops from 7 to 4: **IWDA** (iShares Core MSCI World,
  Amsterdam; developed-world equity, in place of SXR8 + EXSA + IQQE) at 3/7, **IBGM** (iShares
  Euro Govt Bond 7-10yr, Amsterdam; between IBGS and IBGL) at 2/7, **4GLD** at 1/7, **EXXY** at
  1/7. Each line has its own signal. Both lines are in the eu-1 data (`results/eu-1-data.md`;
  IWDA from 2009-09, IBGM from 2008). This drops the EM sleeve (IWDA has none); accepted, fixed
  now. Equal weight at class weights (`ew-c4`) is run at `slip` as a descriptive baseline.
- Plumbing check (no number shown): with daily trades and every Friday checked, the state
  machine must give exactly the reference's weights (`harness.decisions` of `eu1.TSMOM`).

## Fee rows

Schedules from eu-2: `slip` (no fee, reference), `dg1` DEGIRO core selection EUR 1/order +
EUR 2.50/yr, `tr2` Trade Republic Direct Price EUR 2/order, `dg3` DEGIRO other ETFs EUR 3/order
+ EUR 2.50/yr. Books: **EUR 5k, 10k, 25k** (constant). Each of R (tsmom12 and equal weight, the
house EW as in eu-2) and V0-V5 at `slip` and at 3 schedules x 3 sizes:
R 2 x 10 + V 6 x 10 + `ew-c4` 1 = **81 rows** in `tries.md` (idea `eu-3`; V rows `variant`, R
`tsmom12` rows `robustness`, EW rows `baseline`). Orders per year are counted (ETF fills / years),
split into entries (from zero), exits (to zero) and top-ups/trims.

## What counts

**Same character** (per variant, at `slip`, against `R` at `slip`; the eu-2 band test and eu-1
test 4):

1. Sharpe within 0.05 of R's (either direction).
2. Max drawdown within 2 points of R's (either direction).
3. In the four crash windows inside W (2015-16, 2018-Q4, 2020 covid, 2022; eu-1's dates), the
   sign of (variant minus equal weight at `slip`) matches R's in at least 3 of 4.

**Worth running** (per variant or R, schedule, size): same character (R by definition), and

- (a) **fee loss <= 0.10 Sharpe**, where fee loss = min(own Sharpe at `slip`, R's Sharpe at
  `slip`) minus Sharpe under the schedule. Taking the lower of the two means a variant gets no
  credit for being luckier than R at no fee: only the orders it saves count.
- (b) its Sharpe minus equal weight's (house EW, same schedule and size) is within 0.15 of R's
  gap at `slip` (eu-1 test 1, eu-2 (b)).

**Break-even book** per variant and schedule: the smallest book with fee loss <= 0.10,
interpolated linearly in 1/size between the tested sizes (eu-2's method); "<= 5k" / "> 25k"
outside.

**Verdict per book size (5k, 10k, 25k) and schedule**: `euw` is worth running if R or any
same-character variant is worth running there; the table names which. The lane succeeds if a
same-character variant makes `euw` worth running at EUR 5-10k on a schedule where R is not.

## Multiple testing

Six variants (V0-V5) are the selection set; R and the baselines are not selectable. The fee rows
are not extra choices: they are the same six rules priced at fixed fees. Selection bias is
bounded by the design: the character bar allows at most +-0.05 Sharpe at no fee, and test (a)
gives no credit for a variant's no-fee luck, so what a chosen variant can gain is its saved
orders x fee / book, which is mechanical. The result reports, for each variant, orders/yr and
the fee drag predicted from them next to the observed fee loss. Sharpe standard error on W is
~0.27 (eu-2); no Sharpe difference here is read as skill. The held-out year stays untouched:
this is a robustness/implementation choice, not a pass for a new idea.

## Result

`eu-3.md` and `results/eu-3.md` once run.

## Erratum and notes (added after the run, 2026-11-18 ~23:40 UTC)

- **Fee-loss formula.** The card wrote fee loss = **min**(own Sharpe at `slip`, R's) minus the
  Sharpe under the schedule, and said this gives a variant "no credit for being luckier than R".
  The min does the opposite: a variant luckier than R at no fee is measured from R's lower
  Sharpe, so its luck absorbs fees. The stated purpose needs the **max**. Seen only after the
  run. The result shows both readings; the verdict uses the max ("strict"), which is the
  stricter of the two and so cannot turn a fail into a pass. Under the card's literal min, one
  extra cell passes (V0 at DEGIRO EUR 1, EUR 5k: 0.092 vs 0.105 strict).
- **Holiday Fridays.** On a Friday with no bars (Good Friday), `common.weekly` keeps the
  previous Friday's decision until the next trading day; the state machine reproduces this
  exactly in daily mode (checked). In Friday-only mode the decision is made on the holiday
  Friday itself from Thursday's closes (same information, no look-ahead).
