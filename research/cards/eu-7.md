# eu-7: keep trend's crash insurance, lose less of the rest?

Field: choice between pre-committed rules for a small coin-free euro book (two new rules, no
tuning). Lane `eu-7` (DEEPER), night of 2026-11-18, branch `eu-7` from `eu-6`. Written and
pushed before any number for the new runs below existed.

## Question

eu-6 found that for a small coin-free euro book (the seven `euw` funds, 2012-2025, 5/25 band)
trend (`T`, `tsmom12`) is crash insurance, not a better investment: Sharpe 0.62 vs hold-the-seven
(`H`) 0.78 (gap SE 0.14), worst loss 13.6% vs 19.8%, best in all 6 crash windows, but 58 vs 31
months under water and 21 vs 2 orders a year. Most of the smaller worst loss came from holding
less. Can a rule written down now keep trend's crash insurance and give up less of the rest
(Sharpe, waiting, orders)? Two rules, fixed here, nothing else run.

## Seen before writing this (eu-6, train window W)

- T: Sharpe 0.62, max DD 13.6%, longest under water 58 mo, worst 12 months -11.5%, 21.1
  orders/yr, average exposure 67% (mean of T's daily target weights; positions, not returns).
  Crash windows 2000-02 / 2008 / 2015-16 / 2018-Q4 / 2020 / 2022: +8.8 / -0.7 / -8.2 / -4.2 /
  -12.2 / +1.7%.
- H: Sharpe 0.78, max DD 19.8%, 31 mo, -11.4%, 1.9 orders/yr; windows -1.2 / -23.1 / -13.8 /
  -3.4 / -18.7 / -6.7%.
- H scaled to T's vol (73% invested, hindsight, descriptive): max DD 14.8%, Sharpe 0.78.
- trend-tune (US, 1994-2025): the filter paid on stocks only (SPY +0.09, QQQ +0.11 Sharpe vs
  holding); on gold -0.08, bonds -0.06. Commodities were not tested there.
- Not seen: any rule below, on any book.

## The two rules (all that will be run; fixed now)

Same as eu-6 everywhere unless stated: `euw` (SXR8, EXSA, IQQE, IBGS, IBGL, 4GLD, EXXY), EUR,
total-return prices, eu-2's costs (ETF slippage 0.05% a side), window W (decisions 2012-01-02 ..
2025-11-09), train only, cash at 0, next-open fills, daily target weights repeated from the
Friday decision, every trade through the gym with the 5/25 band.

- **A `trendstocks`** (trend only where it paid): seven 1/7 slots. The three stock funds
  (SXR8, EXSA, IQQE) are held only while their 365-day return is positive (the `tsmom12`
  signal, Friday decisions), else the slot is cash. The other four (IBGS, IBGL, 4GLD, EXXY) are
  held at 1/7 always. Band: 5/25 of a 1/7 slot = 3.57% of the book (as T).
  *Assumption, fixed now:* commodities (EXXY) count as "not stocks" and are held. Reason: the
  rule applies the filter only where it was shown to pay (stocks, trend-tune); commodities were
  never tested, so they get no filter. No variant with EXXY filtered is run.
- **B `hold7cash`** (hold less, by a rule): hold all seven at e/7 each, the rest (1 - e) in
  cash at 0. **e = T's average exposure on W**, computed in code from T's daily target weights
  (the mean over all decision days of the sum of T's weights), rounded to the nearest whole
  percent. eu-6 printed it as 67%, so e is expected near 0.67, cash share near 33%; whatever the
  code gives (rounded) is used, no other value is tried. Band: 5/25 of an e/7 slot =
  min(5%, 25% x e/7) of the book (about 2.4%).
- **The same e is used on every book** (one rule, fixed in advance; not recomputed per proxy).

Shown for reference, no new rows: T, H and M (60/40) from eu-6's saved runs, re-scored.

## Proxies for crashes before the funds existed (as eu-6)

- **2008** (2007-10-09 .. 2009-03-09): `usw` (SPY, EFA, EEM, IEF, TLT, GLD, DBC; USD, the
  gym's costs) from 2007-03-01. A = `tsmom12` slots on SPY, EFA, EEM; IEF, TLT, GLD, DBC held at
  1/7; band 3.57%. B = all seven at e/7 (e from `euw`), band min(5%, 25% x e/7).
- **2000-02** (months 2000-03 .. 2002-10): eu-6's long monthly proxy (Shiller S&P total
  return, Shiller 10y Treasury total return, gold), 1/3 slots, monthly, no fees, cash at 0.
  A = stock slot held when its trailing 12-month return (one-month lag, as eu-6's T) is
  positive, bonds and gold 1/3 always. B = e/3 in each, monthly rebalanced. Full 1972-2025
  numbers shown, not judged. 2008 second view on this proxy shown, not counted.

## Criteria (eu-6's, unchanged)

On W, no fixed fee unless stated: Sharpe (SE) and CAGR, vol; worst loss (max DD); longest time
under water (months); worst 12 months; the six crash windows (2000-02 proxy, 2008 proxy, 2015-16,
2018-Q4, 2020 covid, 2022 rate shock); fees at the EUR 1 / 2 / 3 tiers on books of EUR 5k / 10k
/ 25k (eu-2's schedules): Sharpe after fees, fee loss, orders a year, fixed fees a year; paired
stationary bootstrap of Sharpe differences (mean block 20 days, 2,000 draws, seed 0) for A-T,
A-H, B-T, B-H, A-B.

## The answer to the question (fixed now)

Each new rule X (A, B) is judged against T and H:

1. **Keeps the insurance** if both: (a) max DD no more than 2 points worse than T's; (b) in at
   least 5 of the 6 crash windows, X's return is no more than 3 points below T's.
2. **Loses less of the rest** if better than T on at least 2 of these 3: (a) no-fee Sharpe at
   least 0.05 above T (point estimate; "real" only with paired bootstrap p < 0.0083, the family
   bar below); (b) longest under water at least 3 months shorter; (c) at least 25% fewer orders
   a year at no fee.
3. **Worth a held-out-year card** only if X passes 1 and 2. If both pass, the one with the
   higher no-fee Sharpe on W is named (a mechanical pick, stated as such); the held-out year
   would then test only "X keeps the insurance and the rest" on 12 months, not an edge.
   If neither passes, the held-out year stays unspent.

Investor preferences (eu-6's P1-P5, now among T, A, B, H; at a tie the rule with fewer orders a
year at no fee wins): P1 best Sharpe after fees per tier and book (a lead is real only at p <
0.0083 vs the runner-up, else a tie); P2 smallest worst loss (lead under 2 points is a tie, then
worst 12 months); P3 shortest longest-time-under-water (lead under 3 months is a tie); P4 most
crash windows best (within 1 point of the best counts); P5 fewest orders a year. "Worth running
at this book and tier" additionally needs the winner's fee loss <= 0.10 Sharpe (eu-5's bar).
M (60/40) is shown in the tables as eu-6 ran it, not judged again.

## Rows and multiple testing (fixed now)

- `euw`: A and B, each at no fee (`variant`) and at 3 tiers x 3 books (`variant`): **20 rows**.
- `usw` from 2007-03-01: A, B (`robustness`): **2 rows**.
- Long monthly proxy 1972-2025: A, B (`robustness`): **2 rows**, eu-6's monthly format.
- **24 rows.** A and B are selectable rules for this book, so the eu family grows from 10 to
  **12**: a Sharpe lead of A or B over T or H counts as real only with p < 0.10 / 12 =
  **0.0083**. (eu-6's T/H/M comparison stays its own family of 3.)
- Held-out year: untouched by this card. Nothing here changes the live rule.
- Plumbing before any row (no number shown): T's and H's re-runs reproduce eu-6's saved
  equities; A's decisions equal T's on the three stock funds and hold exactly 1/7 in each of the
  other four on every day; B's decisions hold exactly e/7 in each of the seven on every day;
  e is a whole percent between 0 and 1; the monthly proxy A holds bonds and gold at 1/3 always.

## Result

`eu-7.md` and `results/eu-7.md` once run.
