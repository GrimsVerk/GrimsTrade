# eu-5: cut only the drift trades of the small coin-free EUR book

Lane `eu-5` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-5` from `eu-4`. Card `cards/eu-5.md` (pushed before any number). Code `lib/eu5.py`
(`check`, then `run`); table `results/eu-5.md`; 24 rows in `tries.md` (idea `eu-5`). Fees are
generic tiers: EUR 1, 2 or 3 per ETF order on a constant book (eu-2's schedules). Held-out year
unspent.

## 1. What was tested

eu-4 found `euw`'s 30 orders a year split in thirds: entries, exits and drift top-ups. eu-4's
signal-side reducers cut whipsaw but exited later in covid and failed the drawdown bar. eu-5
leaves the signal alone (every entry and exit on the same day as the house rule `R`) and only
trades drift less often:

- **D1 `flipreb`**: top up or trim held slots only on days a signal flips somewhere in the book
  (16.7 such days a year); in between, held slots drift freely.
- **D2 `band25r`**: top up or trim a slot only when it is off target by more than 25% of its
  target (3.57% of the book at 1/7). X comes from the "5/25" rebalancing rule of thumb (5
  points or 25% of target, whichever is smaller), fixed on the card; no other X was run.

D2 is the same mechanism as eu-2's 5% band (a wider gym band; 5% of the book = 35% of a 1/7
target). That band did not fail on `euw` for character: eu-2 required it to *halve* the fee
loss (it cut it ~40%), and it changed the rule on the coin book `eu6` (Sharpe +0.06, max DD -3.1
pts). eu-5 judges D2 by eu-4's character test and counts it in the family.

## 2. Results (no fixed fee, character test)

| `euw`, no fixed fee | Orders/yr | Entries / exits / drift | Sharpe | Max DD | Weight corr | Crash windows 2015-16 / 2018-Q4 / 2020 / 2022 | Keeps character |
|---|---:|---|---:|---:|---:|---|---|
| R `tsmom12` | 30.1 | 10.2 / 9.8 / 10.0 | 0.617 | 13.0% | - | -7.8 / -3.9 / -11.6 / +2.2% | (reference) |
| D1 `flipreb` | 25.3 | 10.2 / 9.8 / 5.3 | 0.609 | 13.7% | 1.00 | -8.2 / -3.9 / -11.7 / +2.1% | yes |
| D2 `band25r` | **21.1** | 10.2 / 9.8 / 1.1 | 0.624 | 13.6% | 0.99 | -8.2 / -4.2 / -12.2 / +1.7% | **yes (pick)** |

- **Both keep the character on `euw`**: Sharpe -0.01 / +0.01 (p 0.80 / 0.29, far from the
  family bar 0.01), max DD +0.7 / +0.6 pts (bar 2), realised weights correlate 1.00 / 0.99
  with `R`'s (mean gap 0.2% / 0.5% of the book per slot-day), crash signs vs equal weight 4/4,
  and no crash window more than 0.5 pts from `R` (covid -11.7 / -12.2% vs -11.6%). Unlike
  eu-4's reducers, the 2020 exit is not delayed: the signal is untouched.
- **Robustness.** `usw`: both keep Sharpe (+0.01 / +0.03) and drawdown. `eu6` (coins): D2 holds
  (Sharpe +0.035, p 0.08; max DD -0.5 pts; orders 42 -> 12), but **D1 breaks down**: with no
  trims between flips the coin slots grew unchecked, max DD 31% -> 65%, Sharpe -0.27. D1
  passes the card (robust on `usw`) but must never be used on a book with very volatile
  assets.
- **Pick (fewest orders): D2.** D2 removes 9 of the 10 drift orders a year. The remaining 20 are
  the signal's own entries and exits, which no drift rule can touch.

## 3. Minimum book per fee tier, and eu-3's verdict

Fee loss <= 0.10 Sharpe (strict reading), interpolated in 1/size; mechanical in brackets.

| Rule | EUR 1 tier | EUR 2 tier | EUR 3 tier | Keeps character |
|---|---|---|---|---|
| R `tsmom12` | ~6k | ~10k | ~16k | yes |
| V0 Friday trades (eu-3) | ~5k | ~10k | ~15k | yes |
| D1 `flipreb` | ~5k (4.7k) | ~9k (8.5k) | ~14k (13.2k) | yes (not on coin books) |
| **D2 `band25r`** | **<= 5k (3.9k)** | **~6k (7.0k)** | **~10k (10.9k)** | **yes** |

Verdict grid with only same-character rules:

| Tier | EUR 5k | EUR 10k | EUR 25k |
|---|---|---|---|
| EUR 1 | **yes (D2 only; loss 0.070)** | yes | yes |
| EUR 2 | no (D2 0.130) | yes (D2 0.062; R 0.104 no) | yes |
| EUR 3 | no (D2 0.209) | **on the line (D2 0.098; mechanical 0.110)** | yes |

**eu-3's verdict changes in two cells.** At the EUR 1 tier a EUR 5k coin-free book becomes worth
running with D2 (loss 0.07 vs R's 0.11). At the EUR 2 tier, 10k moves from borderline to clear
(0.06). At the EUR 3 tier, 10k is now exactly on the line (0.098 observed; the mechanical
formula says 0.11): read it as "about EUR 11k needed". EUR 5k at the EUR 2-3 tiers stays not
worth it. The minimum book falls by about a third at every tier, as the order count does (30 ->
21): fee loss stays mechanical (fees a year / vol).

What this is not: an edge. D2 is a cheaper way to run the same rule; at no fee it is the same
rule within noise. It is one pick from a family of 10, chosen by order count, not by Sharpe. The
coin-free book still trails equal weight in euros (gap -0.15 Sharpe at no fee, eu-1). Using D2
in a live or paper book needs its own card (it would change the runner's band) and the held-out
year.

## 4. eu-1 .. eu-5 in five lines (for a human)

1. The house trend rule can be copied with European UCITS funds in euros and behaves much the
   same (eu-1); without coins the book is calm (~6% vol), so fixed per-order fees matter a lot.
2. With fees of EUR 1 / 2 / 3 per order, the plain rule needs a book of about EUR 6k / 10k /
   16k before fees cost less than 0.10 Sharpe (eu-2, eu-3).
3. Trading less by deciding monthly, or by filtering out whipsaw signals, cuts orders but makes
   the rule exit crashes later, so it is a different rule; none was adopted (eu-3, eu-4).
4. Topping up a fund only when it is 25% off its target (the "5/25 band") leaves every buy and
   sell signal alone, keeps the rule's behaviour on three books, and cuts orders 30 -> 21 a
   year: minimum book about EUR 4k / 7k / 11k (eu-5).
5. None of this is extra return: it is the same rule, cheaper to run. The cheapest lever is
   still a EUR 1 order tier, and on this coin-free book the rule still trails simply holding
   all seven funds on Sharpe (0.62 vs 0.77), with a smaller worst fall (13% vs 20%).

## Rows counted

24 rows (idea `eu-5`): D1 and D2 on `euw` at no fee and 3 tiers x 3 books (20 `variant`), and
both at no fee on `eu6` and `usw` (4 `robustness`). The selectable family is now 10 (eu-3's
V0-V5, eu-4's C1, C2, eu-5's D1, D2); D2 is the pick by the card's mechanical rule.
