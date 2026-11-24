# eu-8: does a euro money-market rate on idle cash change eu-6/eu-7's answers? And idea C

Field: robustness of finished comparisons (step 1, no new rule) and one post-hoc rule (step 2,
section C below, added before its numbers). Lane `eu-8` (DEEPER), night of 2026-11-18, branch
`eu-8` from `eu-7`. Step 1 is written and pushed before any number with interest on cash exists.

## Step 1: idle cash earns a euro money-market rate

### Why

eu-6 and eu-7 held idle cash at 0. Trend T (`tsmom12`, 5/25 band) is in cash about a third of
the time and rule B (hold the seven at 67%) always holds 33% cash, so their case could move when
cash earns interest. In 2012-2025 the euro rate was below zero from mid-2014 to mid-2022, so the
effect can go either way. Same rules, same runs, nothing re-chosen: only the accounting of cash.

### Seen before writing this

All of eu-6's and eu-7's numbers (`research/eu-6.md`, `research/eu-7.md`), cash at 0. The
US-only what-if `results/cash-interest.md` (six live assets, T-bill rate: no ranking change). Two
rate values seen while checking the download: EONIA monthly average 2012-01 +0.38%, 2016-01
-0.24% (no backtest number).

### The rate (keyless public source, raw files not committed)

- **EUR**: ECB Data Portal, no key. EONIA monthly average (series
  `FM.M.U2.EUR.4F.MM.EONIA.HSTA`) for days before 2019-10-01, the daily euro short-term rate
  (EUR STR, series `EST.B.EU000A2X2A25.WT`) from 2019-10-01 (a day without a print takes the last
  print). The daily EONIA series was not served by the API (404), so the monthly average stands
  in before EUR STR; the rate moves little inside a month. Accrual ACT/360 (the euro money-market
  convention): a calendar day earns rate / 360.
- **USD** (the 2008 `usw` proxy and the long monthly proxy): the 13-week T-bill yield `IRX`
  already in the research cache (as `lib/cash_interest.py`), daily rate / 365; monthly proxy:
  the month's average yield / 12.
- **Two versions of the euro rate** (both run, both logged): **(a) as is**, negative years
  included (a euro money-market fund before its fee; the primary view, this is what the step is
  about); **(b) floored at 0** (cash that never pays below zero, e.g. a savings or broker cash
  account paying the policy rate only when positive; shown, not used for any verdict).

### How interest is added (fixed now)

As `lib/cash_interest.py`: the gym runs unchanged; each day's return gets (cash share of the
book at the end of the previous day) x (that day's rate). Unlike `cash_interest.py`, the cash
share is the gym's **actual** cash (start cash plus every fill's cash flow, over end-of-day
equity), not the target, so band drift is counted. The interest is assumed reinvested pro rata
(a rescoring, not a new simulation); no fee on the money-market holding. A plumbing check
(no number shown) confirms the rebuilt cash path ends at the gym's final cash.

### Rules re-scored (no new rule, no new choice)

On `euw`, window W (decisions 2012-01-02 .. 2025-11-09), no fixed fee: **T** (eu-5's D2), **B**
(eu-7's hold7cash, e = 0.67), **H** (hold the seven, 5/25 band), **M** (60/40, 5% band). On the
`usw` proxy from 2007-03-01 (USD, IRX): T, B, H, M. On the long monthly proxy (1972-2025): T, B,
H, M with IRX. Fee tiers are not re-run: a fixed fee per order does not depend on how cash is paid,
so eu-6/eu-7's fee losses carry over (stated, not tested).

### Measures

eu-6's human criteria plus one: **Sharpe above the cash rate** (excess returns; the primary
Sharpe here, because the investor's alternative is the money-market fund) and Sharpe against 0
(as before); CAGR, vol, worst loss, longest under water, worst 12 months, the six crash windows.
Paired stationary bootstrap of excess-Sharpe differences (block 20, 2,000 draws, seed 0) for B-T,
H-T, M-T, B-H.

### Which conclusions are tested, and what counts as "changes" (fixed now)

Each with the primary rate (a), judged on `euw` unless stated:

1. **K1 Sharpe order** (eu-6/7: B ~ H > M > T, no gap real). Changes if any pair's order flips
   by more than 0.05, or a gap becomes real (p < 0.0083, the eu family bar of 12).
2. **K2 B - T Sharpe gap** (eu-7: +0.17, p 0.10). Changes if it shrinks below +0.05 or grows past
   real.
3. **K3 P2 smallest worst loss: B** (eu-7, tie band 2 pts, then worst 12 months). Changes if the
   winner differs.
4. **K4 P3 shortest time under water: H** (B tie). Changes if the winner differs.
5. **K5 P4 crash insurance: T** (most windows best of 6, within 1 pt). Changes if the winner
   differs.
6. **K6 trend's return cost**: T's CAGR below H's by 2.6 points a year. Changes if the gap
   shrinks by 1 point or more.
7. **K7 2008 proxy**: B's worst loss about twice T's on `usw` 2007- (22% vs 11%). Changes if B's
   worst loss is no longer at least 1.5 x T's.
8. **K8 long monthly proxy**: T's Sharpe at least H's (1.26 vs 1.20). Changes if H leads by
   more than 0.05.

P1 is judged at no fee only (fees carry over, above). The answer: a list of K1-K8, each "holds"
or "changes", and whether eu-7's plain answer (section 4) needs a new sentence.

### Rows and multiple testing (fixed now)

- `euw`: T, B, H, M x rate (a) and (b): **8 rows** (`robustness`).
- `usw` 2007-: T, B, H, M with IRX: **4 rows** (`robustness`).
- Long monthly proxy: T, B, H, M with IRX: **4 rows** (`robustness`, eu-6's monthly format).
- **16 rows**, none selectable: the eu family stays at 12 (bar p < 0.0083). The row's Sharpe
  column is against 0 (the tries.md convention); the result file gives both.
- Project-wide (register-1 `research/register/BAR.md`, 2026-11-18 22:34): 2,904 tries, N 1,012
  for a new pick, Bonferroni p <= 4.9e-5. No pick is made here.
- Held-out year: untouched.

## Step 2: idea C, trend on the stock and long-bond funds only (added before any C number)

### Why, and why it is suspect

eu-7 found that rule A (trend on the three stock funds, the rest held) lost trend's 2022
protection because it held the long euro bonds (2022: A -3.8%, T +1.7%). Idea C adds the long
bond fund to the filtered set. It was suggested by the 2012-2025 EUR years themselves (one
window, 2022), so it is post-hoc. To avoid fitting on those years it is **judged first on US
proxies 1994-2011** (before the euro funds existed), and only then on EUR 2012-2025. It counts
in the eu family.

### Seen before writing this

Everything in eu-6, eu-7 and step 1 above (all cash at 0 or with the rate; no C number). General
market history: in 2022 long bonds fell while gold and commodities rose; commodities fell hard in
2008, 2015-16 and 2020; 1-3y euro govts barely moved. No backtest of C on any book.

### The rule (fixed now; nothing else is run)

- **C `trendsl`**: seven 1/7 slots. The three stock funds **and the long-bond fund** are held
  only while their 365-day return is positive (the `tsmom12` signal, Friday decisions), else the
  slot is cash; the other three are held at 1/7 always. `euw`: filtered SXR8, EXSA, IQQE, IBGL;
  held IBGS (1-3y), 4GLD, EXXY. Band 5/25 of a 1/7 slot = 3.57% (as T and A). Everything else
  as eu-7 (costs, window W, next-open fills, daily target weights from the Friday decision).
- **`usw` proxy** (daily, USD, the gym's US costs): filtered SPY, EFA, EEM, TLT (20y+); held IEF
  (7-10y, the shorter bond slot, as `euw`'s IBGS position), GLD, DBC. Run from 2007-03-01 with
  bars cut after **2011-12-31** (no US bar after 2011 is loaded for C).
- **Long monthly proxy** (Shiller stocks, 10y Treasuries, gold; eu-6's): stock and bond slots on
  the lagged 12-month signal, gold 1/3 always; judged on months **1994-01 .. 2011-12** only.
- Cash at 0 for every verdict (eu-7's terms, so C is judged like A and B were); C on `euw` with
  rate (a) of step 1 is shown as a robustness row.

### Stage 1: US proxies 1994-2011 (judged first; T and H re-scored on the same windows, no rows)

C passes stage 1 only if both:

1. **Keeps the insurance**: (a) worst loss no more than 2 points above T's on both proxy windows
   (monthly 1994-2011, `usw` 2007-03 .. 2011-12); (b) in 2000-02 (monthly) and 2008 (`usw`),
   C's return no more than 3 points below T's.
2. **Loses less of the rest**, at least 2 of 3: (a) Sharpe at least 0.05 above T's on the
   monthly proxy 1994-2011; (b) longest under water at least 3 months shorter there; (c) at least
   25% fewer orders a year on `usw` 2007-2011.

### Stage 2: EUR 2012-2025 (eu-7's test, unchanged)

Keeps the insurance (max DD <= T + 2 points; at least 5 of the 6 crash windows within 3 points of
T, the 2000-02 and 2008 windows from the stage-1 proxies) and loses less of the rest (2 of 3:
Sharpe >= T + 0.05, under water >= 3 months shorter, >= 25% fewer orders). Preferences P1-P5 as
eu-7, among T, B, C, H (A shown, not judged; it won nothing in eu-7).

**C is worth a held-out-year card only if it passes stage 1 and stage 2.** Even then the year is
not spent in this lane: a separate card would test only "C keeps the insurance" on 12 months.
A Sharpe lead of C counts as real only at p < 0.10 / 13 = **0.0077** (eu family 13).

### Rows (fixed now)

- `euw`, no fee (`variant`) and 3 tiers x 3 books (`variant`): 10 rows.
- `usw` 2007-03-01 .. 2011-12-31 (`robustness`): 1 row. Monthly proxy 1994-2011 (`robustness`,
  eu-6's monthly format): 1 row. `euw` with rate (a) (`robustness`): 1 row.
- **13 rows.** eu family 12 -> **13** (bar p < 0.0077). Project-wide: 2,904 tries, N 1,012 for a
  new pick, Bonferroni p <= 4.9e-5 (register-1 `BAR.md`, 2026-11-18 22:34).
- Plumbing before any row (no number shown): C's decisions equal T's on the four filtered funds
  and hold exactly 1/7 in each of the other three on every day, on `euw` and `usw`; the `usw`
  history for C ends 2011-12-31; the monthly C holds gold at 1/3 always.
