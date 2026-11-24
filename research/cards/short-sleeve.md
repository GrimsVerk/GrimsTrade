# short-sleeve: `tsmom12` plus a small SPY/QQQ downtrend short sleeve, judged against a same-size T-bill slot

Lane `short-sleeve`, written 2026-11-19 ~00:05 UTC, **before any return of the sleeve or of
the two books below was computed**. Base: `ls-trend-1` (`ls-trend-1.md`). What was seen
before this card: ls-trend-1's results (narrow long-short on SPY/QQQ/GLD/TLT: +24% / -11% / -4%
in 2008 / 2020-02..03 / 2022), survey-6's suggestion of a small equity downtrend short sleeve
judged as insurance, insure-1's method (25% zigzag episodes, loss avoided vs rebound given up),
diversifier-1's lesson (score above T-bills against a T-bill slot of the same size), and the
known US crash history. No series below has been computed.

This **is a pick** (one `variant` row, counted). Its comparator is logged as one `baseline`
row. One run, no tuning, no second variant. Held-out year (2025-11-11 on) not read.

## The two books (fixed now)

Both books: 90% of the book is `tsmom12` exactly as logged (`baselines/tsmom12`: six live
assets, equal slots, held when the trailing 365-day total return is positive, else cash;
Friday decisions; gym fills and costs), re-scored with **cash earning the 13-week T-bill
yield** (`cash_interest.rescored`, IRX, accrued per calendar day). The remaining 10% of the
book is the slot; the mix is reset to 90/10 every day (no drift).

- **Control `bill10`:** the 10% slot sits in T-bills.
- **Test `short10`:** the 10% slot is split into two fixed legs of 5% of the book each, one
  for SPY and one for QQQ. A leg is **short its ETF** (notional 5% of the book, 1x, no
  leverage) when that ETF's own trailing 365-day total return (`common.tsmom_signal`, the same
  signal `tsmom12` uses) is **negative** at the Friday decision; otherwise the leg sits in
  T-bills. A leg whose ETF has less than a year of history (QQQ before 2000-03) sits in
  T-bills; its 5% does not move to the other leg.
  - **Short economics (stated a priori):** the leg's collateral earns the T-bill yield; the
    short proceeds earn the T-bill yield too (rebate at the bill); a **borrow fee of 1.0% a
    year** on the short notional, accrued daily (ls-trend-1's figure; general-collateral SPY
    and QQQ usually cost less, so this is cautious). Dividends are paid by the short (total
    return prices). So a short leg's daily return over the bill slot is
    `w x (rf - 1%/365 - r_ETF)`, `w = 0.05`.
  - **Trading cost:** 5 bps of the leg's notional per side, charged each time a leg turns short
    or back to bills (above the gym's 2 bps for ETFs).
  - **Timing (no look-ahead):** the Friday decision (22:30 UTC, after the close) sees closes
    through that day; the position takes effect from the **close of the next trading day**
    (one day later than the gym's next open; cautious). Same-day weights are the harness's
    `decisions()` output, so visibility is the gym's.
- ETFs only; nothing levered, no inverse ETFs, no futures, no options. The sleeve is a paper
  series on adjusted closes (the gym cannot hold shorts); `tsmom12`'s part is the gym's run.

Window: `tsmom12`'s primary test, decisions 1994-02-01 .. 2025-11-09, bars to 2025-11-10.

## Metrics (fixed now)

1. **Crash windows** (total return of each book, and the difference): calendar **2008**,
   **2020-Q1** (2020-01-01 .. 2020-03-31), calendar **2022**. Also the harness's stress windows
   (dot-com bust, 2008 crisis, covid crash, 2022 rate shock) for context.
2. **Insurance, insure-1 style.** Episodes: every confirmed 25% fall of **SPY** (total-return
   close; zigzag 25% down then 25% up to confirm, insure-1's `zigzag`) inside the window: the
   US market. QQQ's 25% episodes reported as a second series. Per episode, in log points of
   `short10` minus `bill10`: insurance `I` over (peak, trough]; rebound `B` over (trough,
   min(trough + 365 days, next peak)]; calm `C` = everything else. Premium
   `P = -(sum B + C) / sum I` (log growth given up per log point of loss avoided; only read
   when `sum I > 0`). An unfinished fall at the window's end is reported, not scored.
3. **Sharpe above T-bills** (daily, 365 days, returns minus the bill), `short10` minus
   `bill10`: difference d, paired stationary bootstrap (2,000 draws, mean block 20 days, seed
   0; `stats` module's method) for the one-sided p and the SE (std of the bootstrap
   differences), z = d / SE. Also CAGR, volatility, max drawdown, worst calendar year, by era
   (harness eras), and the sleeve's share of time short per leg.

## Bars and reading rules (fixed now)

- **Family bar** (ls-trend-1: 68 mechanisms, 16 tested): one-sided p < 0.10 / 68 = **0.00147**.
  A short sleeve on the 12-month sign is the same mechanism as `tsmom12` (time-series
  momentum), so it adds no family member, but it is a counted pick.
- **Project-wide bar** (`register-2` `BAR.md`, rows through 2026-11-18 23:04: 3,023 tries,
  N 1,027 for a new pick, measured rho 0.58 -> **N_eff 433**): **z >= 4.65** on the edge over
  the comparator (DSR 0.95), Bonferroni **p <= 1.2e-4**. The close-rule edge in BAR.md
  (+0.30) assumes SE 0.065; here the measured SE is used with the z column.
- **Reading:**
  - **Edge** only if d > 0 clears both bars (bootstrap p < 0.00147 **and** z >= 4.65).
  - **Insurance real here** if `short10` beats `bill10` in all three crash windows **and**
    `sum I > 0` on the SPY episodes with `I > 0` in a majority of them; **cheap** if also
    P < 1 (it gives back less outside the falls than it saves inside them).
  - A pass on insurance alone is **a risk preference, not a pick that clears the bar**: it
    changes nothing in the paper book and is reported as a choice for whoever sets the risk.
  - Expectation written now: the sleeve gains in slow bear markets (2000-02, 2008), loses in
    the 2020 V (the 12-month sign turns after the fall and is short into the rebound), helps
    a little in 2022, and costs Sharpe in whipsaw years; d small and negative or near zero.
    If so: no edge, insurance at a premium above 1.

## Logging

- `tries.md`: `short-sleeve | short10@bills | variant | train` and
  `short-sleeve | bill10@bills | baseline | train`, Sharpe in the repo's row convention
  (daily, 365, zero risk-free; here cash and the slot earn bills, hence `@bills`). Turnover:
  0.9 x `tsmom12`'s plus the sleeve's sum of |weight change| a year.
- No `ledger/tries.jsonl` line (the gym cannot hold shorts; as ls-trend-2).
- Script `research/lib/shortsleeve1.py`, committed before its run; tables in
  `results/short-sleeve.md`; one-screen verdict in `short-sleeve.md`.
