# Card insure-3: is trend cheaper or dearer crash insurance than buying puts?

Lane `insure-3`, 2026-11-24 (night). Written and pushed before any number is computed.
Descriptive comparison, **not a strategy pick**: nothing is selected, nothing is tuned.

## Question

`research/SUMMARY.md` calls `tsmom12` crash insurance with a price (about 2 points of growth a
year behind holding since 2002; fails in fast crashes). Insurance has a market price: put
options. Per unit of crash loss avoided, is trend cheaper or dearer than buying puts, in which
kind of crash, and does a 50/50 mix cover trend's fast-crash weakness?

## Data (keyless, plain requests, no bot-block evasion)

- **PPUT**, CBOE S&P 500 5% Put Protection Index: long the S&P 500 (total return), plus a
  one-month put 5% out of the money bought each month (third Friday). Daily from 1986-06-30.
  `https://cdn.cboe.com/api/global/us_indices/daily_prices/PPUT_History.csv` (307 redirect to
  `cdn-api.cboe.com`, then 200 to a plain request; probed 2026-11-24).
- Side set (same source, same check): **PUT** (PutWrite; daily only from 2007-01, 7 scattered
  points before, as survey-6 found), **BXM** (BuyWrite, from 2002-03), **CLL** (95-110 collar,
  from 2008-08), **VXTH** (S&P 500 plus VIX calls, a tail hedge, from 2006-04). `SPXTR` is
  refused (403): recorded, not retried. No other CBOE tail index is tried.
- **S&P 500 total return**: Yahoo `^SP500TR` daily (from 1988-01-04), fetched with period2 =
  2025-11-01 like insure-2. Before 1988 (needed for 1985-07..1987-12: the rule needs a year of
  history before its first decision): the cached Yahoo `^GSPC` price index plus Shiller's
  monthly dividend (cached `derived/survey-4/shiller_div.csv`), accrued per session as
  dividend / price / 252. Check (reported, not used to choose anything): the built series
  against `^SP500TR` over 1988-2025, CAGR gap and daily correlation.
- **Bills**: cached Yahoo `^IRX` (13-week bill yield), accrued per calendar day (yield / 365).
- Nothing after **2025-10-31** is kept: the fetch script drops later rows before it writes the
  CBOE files into the data cache (they come as whole files), so no held-out bar
  (after 2025-11-10) is ever stored or parsed. The probe on 2026-11-24 printed the last two
  lines of each file (2026 levels) to check the format; nothing from them is used.
- Terms of use: raw index levels stay in the data cache (git-ignored). Only derived statistics
  are committed. The terms found are quoted in `research/insure-3.md`.

## Series (window 1986-07-01..2025-10-31, daily closes, one per trading day of PPUT)

1. **hold**: S&P 500 total return.
2. **trend**: `tsmom12` on the S&P 500 total return exactly as the record defines it
   (`trend_tune.paper`, grid (12,)): on each Friday, hold if the 365-day log return of the
   closes visible before the decision is above 0, else cash; the position applies from the
   next session to the next Friday; eligible after a year of bars; 2 bps a side (the gym's ETF
   cost). Primary: idle cash earns bills (PPUT is always invested, and Sharpe is above bills).
   Robustness: cash at 0 (the gym's rule).
3. **PPUT** as published (no fees added; the index carries none).
4. **mix**: 50% trend (cash at bills) and 50% PPUT, rebalanced to 50/50 at each month's last
   close.

## Measures

- CAGR; Sharpe above bills (daily excess returns, x sqrt(252)), with SE
  sqrt((1 + SR^2 / 2) / years); worst loss (max drawdown on daily closes).
- **Falls**: insure-1/2's zigzag on hold's daily closes, 15% down / 15% up, inside the window.
  Per fall: each series' loss peak -> trough (simple %), loss avoided I = 100 x (log return of
  the series - log return of hold) over (peak, trough] in log points, share avoided
  I / |hold's log return|, and net of rebound (I plus the next 365 days, cut at the next
  peak), as insure-1.
- **Insurance cost** (the lead's measure): (CAGR hold - CAGR series), in points a year,
  divided by the mean I over the falls (log points per fall). Lower = cheaper. Also insure-1's
  pooled premium P = -(total log gap - sum I) / sum I (log points given up outside falls per
  log point saved inside them).
- **Fast crashes**: the card's subset is **1987 and 2020** (the falls whose trough lies in
  1987-10..1987-12 and 2020-02..2020-04), reported on their own. Second cut: every fall of 92
  days or less peak -> trough, against slower ones.

## Side table (wider, descriptive)

PUT, BXM, CLL, VXTH next to hold, trend, PPUT and mix, each from its first full month to
2025-10 (hold and trend on the same window as each): CAGR, Sharpe, worst loss, loss in each
15% fall inside that window, insurance cost. Not part of the answer rules below; a context row.

## Answer rules (fixed now)

- **Cheaper insurance** over the window: the lower insurance cost (lead's measure); if P points
  the other way, the answer says "depends on the measure".
- **Per kind of crash**: in 1987 and in 2020 separately, which of trend and PPUT lost less; for
  the fast (<= 92 days) and slower cuts, the mean share avoided of each.
- **Mix covers trend's fast-crash weakness** if in both 1987 and 2020 the mix lost less than
  trend, and its full-window insurance cost is no higher than trend's. "Partly" if only the
  first holds; "no" otherwise.
- Sharpe differences are described with their SE; no test is claimed. Episodes are few (about
  ten falls of 15% in 39 years, two fast named ones): the answer is a description of one
  history.

## Rows and bar

- `research/tries.md`, idea `insure-3`: one row per series (hold and PPUT `baseline`; trend,
  mix and the cash-at-0 forms `robustness`; side indices `baseline`), Sharpe in the file's
  convention (daily calendar, 365, zero rf). No selectable claim.
- The project-wide bar (`research/register/BAR.md`, rows through 2026-11-24 20:01): 3,855
  tries, N = 1,083 for a new pick, N_eff 500, z >= 4.70 (an edge of +0.31 over `tsmom12` for a
  close rule), Bonferroni p <= 1.0e-04. Quoted for scale only: this card picks nothing.

## Code

`research/lib/fetch_insure3.py` (fetch, truncates at 2025-10-31), `research/lib/insure3.py`
(one run, writes `research/results/insure-3.md`), `tests/test_insure3.py` (index alignment,
no look-ahead in the trend rule, mix rebalancing).
