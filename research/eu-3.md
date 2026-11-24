# eu-3: fewer orders for a small coin-free EUR book

Lane `eu-3` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-3` from `eu-2`. Card: `cards/eu-3.md` (pushed before any number; erratum at its
end). Tables: `results/eu-3.md`. Code: `lib/eu3.py`. 81 rows in `tries.md` (idea `eu-3`).

**Question.** On the coin-free book `euw` (SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY),
fixed per-order fees made `tsmom12` not worth running below about EUR 6k (EUR 1 orders), 10k
(EUR 2) or 16k (EUR 3) (eu-2). Can a slower decision clock or fewer, larger slots cut the
orders a lot **without changing the rule's character**, so the book is worth running at
EUR 5-10k?

## Design (card)

The signal is untouched (365-day return > 0). Six variants, fixed in advance, against the house
rule R (Friday signal, weights repeated daily, so drift is topped up any day; 1% band):

| Variant | What changes |
|---|---|
| V0 `w-fri` | trades only on Fridays (drift checked weekly, not daily) |
| V1 `m` | signal checked and trades placed only on the last Friday of each month |
| V2 `m-in` | entries only on last Fridays, exits any Friday (weekly risk check) |
| V3 `hold4w` | no exit within 28 days of an entry |
| V4 `c4` | 4 class funds at euw's class weights: IWDA 3/7, IBGM 2/7, 4GLD 1/7, EXXY 1/7 |
| V5 `c4-m` | V4 with V1's monthly clock |

Same character (at no fixed fee, vs R): Sharpe within 0.05, max drawdown within 2 points, crash
pattern vs equal weight matching in 3 of 4 windows (the eu-2 band test plus eu-1 test 4).
Worth running (per fee schedule and book size): same character, fee loss <= 0.10 Sharpe, gap
to equal weight within 0.15 of R's. Fees as in eu-2 (constant book; DEGIRO EUR 1 or 3 per
order + EUR 2.50/yr, Trade Republic EUR 2), books EUR 5k, 10k, 25k. With fee 0 and daily trades
the variant engine reproduces the house rule's weights exactly (checked on every run).

## Results (window W, 2012-2025)

**Orders and character at no fixed fee:**

| Rule | Orders/yr | (entries / exits / top-ups) | Sharpe | Max DD | dSharpe vs R (paired p) | Same character |
|---|---:|---|---:|---:|---:|---|
| R `tsmom12` | 30.1 | 10.2 / 9.8 / 10.0 | 0.62 | 13.0% | - | (reference) |
| V0 Friday trades | 27.9 | 10.2 / 9.8 / 7.9 | 0.63 | 13.2% | +0.01 (0.13) | **yes** |
| V1 monthly | 14.6 | 4.8 / 4.3 / 5.6 | 0.75 | 13.6% | +0.14 (0.03) | no (Sharpe) |
| V2 monthly entries | 21.9 | 7.4 / 6.9 / 7.6 | 0.65 | 15.5% | +0.03 (0.26) | no (DD +2.4) |
| V3 4-week hold | 24.6 | 8.4 / 8.0 / 8.1 | 0.70 | 12.6% | +0.08 (0.02) | no (Sharpe) |
| V4 class slots | 20.3 | 5.7 / 5.4 / 9.2 | 0.71 | 16.6% | +0.09 (0.19) | no (Sharpe, DD +3.5) |
| V5 class slots, monthly | 11.1 | 2.7 / 2.5 / 5.9 | 0.77 | 17.0% | +0.16 (0.08) | no (Sharpe, DD +4.0) |
| equal weight (house) | 15.6 | | 0.77 | 19.8% | | |

All seven keep the crash pattern (4 of 4). Orders split evenly between entries, exits and
drift top-ups; checking drift weekly instead of daily (V0) saves only 2 a year.

**Fee loss (strict reading, Sharpe) and break-even book:**

| Rule | EUR 1 (dg1) 5k / 10k | EUR 2 (tr2) 5k / 10k | EUR 3 (dg3) 5k / 10k | Break-even dg1 / tr2 / dg3 |
|---|---|---|---|---|
| R | 0.11 / 0.06 | 0.21 / 0.10 | 0.32 / 0.16 | ~6k / ~10k / ~16k |
| V0 | 0.10 / 0.05 | 0.19 / 0.10 | 0.30 / 0.15 | ~5k / ~10k / ~15k |
| V1 (other rule) | 0.06 / 0.03 | 0.10 / 0.05 | 0.16 / 0.08 | <= 5k / ~5k / ~8k |
| V5 (other rule) | 0.04 / 0.02 | 0.06 / 0.03 | 0.10 / 0.05 | <= 5k / <= 5k / ~5k |

The fee loss is mechanical: everywhere it equals fixed fees per year divided by the rule's
volatility to within 0.01 (column "Predicted" in the result). Halving the orders halves it.

## Verdict

1. **No: on this book, the decision clock and slot structure cannot cut orders a lot without
   changing the rule.** The only variant that keeps the character by the card's bar (V0,
   trades only on Fridays) saves 2 orders of 30 a year and moves no break-even by more than
   EUR 1k. Every variant that cuts orders substantially (monthly 30 -> 15, monthly entries
   -> 22, 4-week hold -> 25, class slots -> 20, class slots monthly -> 11) fails the bar.
2. **Per book size** (strict reading; same-character rules only):
   - **EUR 5k: not worth running** at any of the three fee levels (DEGIRO EUR 1 comes closest:
     loss 0.11 with R, 0.105 with V0).
   - **EUR 10k: worth it with EUR 1 orders** (R as is, loss 0.06); **borderline with EUR 2**
     (R 0.104, V0 0.098: on the line, call it break-even); **not with EUR 3** (0.15-0.16).
   - **EUR 25k: worth it at every fee level** (loss <= 0.07).
   Under the card's literal formula (see the erratum) V0 also scrapes through at EUR 5k with
   EUR 1 orders (0.092); the stricter reading is the verdict.
3. **The variants failed mostly by doing better, not worse, at no fee**: monthly +0.14 Sharpe
   (drawdown +0.6 points, same crash pattern), 4-week hold +0.08, class slots +0.09 with a
   deeper drawdown. That is a different rule, not a free fix (the eu-2 precedent for the 5%
   band), and it is probably luck: six variants were tried (the best single paired p-values, 0.02-0.03,
   become 0.12-0.18 after a Bonferroni correction for six tries), the Sharpe SE is 0.27, and on the US
   six over 1994-2025 monthly decisions did *worse* than weekly (Sharpe 1.00 vs 1.05, worst loss
   41% vs 36%; `results/trend-tune-anatomy.md` section 7). Class slots also drop the EM sleeve
   and carry more equity risk in a crash (2020: -15% vs -12%; 2022: -1% vs +2%).
4. **If the owner wants a EUR 5-10k coin-free book anyway**, the levers in order: (a) EUR 1
   orders (DEGIRO core selection or Trade Republic Best Price) — R is then fine from ~EUR 6k;
   (b) a monthly clock, which halves the fee drag mechanically (break-even ~EUR 5-8k even at
   EUR 3 orders) but is a rule change that needs its own card, other books and the held-out
   year before it could replace the weekly rule.

Nothing here argues for changing the house rule. Held-out year: unspent (nothing selected).

## Variants counted

81 rows: R `tsmom12` 10 (`robustness`), equal weight 10 + `ew-c4` 1 (`baseline`), V0-V5 60
(`variant`, six selectable rules each priced at 10 fee cells). No plumbing run showed a number.

Rerun (needs the eu-1 CSVs in `research/data/`; this worktree's copy came from the eu-2
worktree):

```sh
uv run --with numpy python research/lib/eu3.py check
uv run --with numpy python research/lib/eu3.py run
```
