# live-check: do our backtests look like the live funds of their family?

Source list: `survey-5.md` (live fund series, the AQR TSMOM factor, haircut literature H1-H4).
Written 2026-11-18, lane survey-5, **before any return of any fund, of the AQR factor, or of our
rules over these windows was computed** (what was seen: `survey-5.md`, "How the list was
made"). This is a **descriptive check, not a strategy test**: nothing is selected, no pass bar,
no held-out data, the family count does not change.

## Questions

1. Over the years the live funds exist, does our backtested `tsmom12` move with live
   trend-following funds (correlation), and how far apart are the Sharpe ratios? Same for two
   near-misses: `where-vol` (trend-where, 1.07) and `sixty-forty` (benchmark, 0.76) against
   live risk-parity funds.
2. How much does this family lose going from a published backtest to live money? Measured on
   the one clean same-manager pair keyless data allow (AQR's TSMOM factor, the paper's
   portfolio, against AQR's live managed-futures fund), and set beside the literature (H1-H4).
3. (For step 3.) What live Sharpe to expect from `tsmom12` after that haircut, and how many
   years a forward test needs to tell it apart from zero and from holding everything.

## Series (fixed now)

Ours: re-scores of configurations already in `tries.md`, through the research harness
(dividend-adjusted prices, the gym's fills and costs, train period only, nothing tuned):

- `tsmom12` (the live rule; six assets incl. BTC and ETH);
- `tsmom12-c00` (risk-map's variant: the same rule with no coins; the closest to what a fund
  can hold);
- `where-vol` (trend-where's variant; its code copied unchanged from branch `trend-where`);
- `sixty-forty` (60% SPY, 40% TLT, weekly).

Cash earns the 13-week T-bill (`cash_interest.rescored`), and every series is turned into a
**monthly excess return over the T-bill** (calendar months, compounded), because funds hold
their collateral in bills and the AQR factor is already an excess return.

Live: monthly total return from the adjusted close at each month's last bar, minus the same
T-bill month; a fund's first, partial month is dropped. Composites, equal weight across the
funds alive that month:

- **TC (trend composite)**: RYMFX, AQMIX, ASFYX, WTMF, PQTIX, ABYIX, DBMF, KMLM, CTA. LFMIX
  is shown alone (multi-manager macro, not pure trend).
- **RC (risk-parity composite)**: ABRZX, AQRIX, RPAR.
- Shown alone, no composite: SPLV, USMV, QSPIX, QRPIX.

Published backtest: AQR TSMOM factor (`TSMOM`, all assets), monthly excess returns.

## Windows (fixed now)

- **L (live window): 2010-02 to 2025-10.** AQMIX's first full month to the last full month
  before the held-out year (it starts 2025-11-11). **No month after 2025-10 of any series is
  read**, so the held-out year stays unspent for every idea.
- **L07: 2007-04 to 2025-10**, for RYMFX (the only fund through 2008) against our series.
- **P (the paper's sample): 1985-01 to 2009-12** for the AQR factor (Moskowitz, Ooi, Pedersen
  2012 use 1985-2009); our rules from 1994-02 to 2009-12.
- Each fund also over its own life up to 2025-10.

## Measures (all that will be computed)

1. Sharpe a year (monthly mean / sd x sqrt 12, excess) of every series in L, L07 (where alive)
   and each fund's own life; also our rules' repo-convention Sharpe (daily, 365, zero rate) in L
   for the `tries.md` row.
2. Correlation of monthly excess returns in L: each of our four series with TC, RC, every fund
   alive at least 36 months in L (over its months), the AQR factor, and SPY's excess return
   (context: how much of each is plain equity).
3. Calendar-year excess returns in the crash years **2008, 2020, 2022** (2008 only where
   alive: RYMFX, AQR factor, ours), and the 2020-02/03 two-month return.
4. Haircut, trend family:
   - (a) post-sample decay of the published portfolio: Sharpe of the AQR factor in P vs in L;
   - (b) implementation and fees: AQR factor in L vs AQMIX in L, and vs TC in L;
   - (c) total, the number step 3 uses: **h = 1 - Sharpe(AQMIX, L) / Sharpe(AQR factor, P)**;
   - (d) our own split: `tsmom12` and `tsmom12-c00` Sharpe 1994-2009 vs L.
   If Sharpe(AQR factor, P) <= 0, h is not defined and step 3 uses the literature only.
5. Sharpe gap in L: ours minus TC (trend rules) and minus RC (`sixty-forty`, `where-vol`).

## Reading rules (fixed now; descriptive, no pass or fail)

- Correlation with the family composite in L: **>= 0.5 "moves with its live family"; 0.3 to
  0.5 "partly"; < 0.3 "does not"**.
- If one of ours beats its family's live Sharpe in L by more than 0.3 and `tsmom12-c00` does
  not, the gap is the coins, not the trend rule: say so, and do not count it as evidence for
  the rule.
- Step 3's expected live Sharpe for `tsmom12` = its backtest Sharpe (1.05, repo convention,
  1994-2025) x (1 - h), shown for three haircuts: **h as measured in 4(c)** (central), **25%**
  (Harvey-Liu's ceiling for a Sharpe above 1, H2: the optimistic end), **73%** (the median of
  215 bank strategies, H1: the pessimistic end).
- Step 3's forward length: forward-1's `sharpe` formula (n = 1 + (1 - skew sr + (kurt - 1)/4
  sr^2) ((z(1-a) + z(power)) / sr)^2, per-week sr), weekly observations, power 0.8, one-sided
  alpha 0.025 (forward-1's per-rule alpha) and 0.10; skew and kurtosis from `tsmom12`'s weekly
  backtest returns. Two questions: (i) Sharpe > 0 at the expected live Sharpe; (ii) `tsmom12`
  ahead of holding everything (`hold-c17`): the weekly return difference, its backtest Sharpe
  haircut by the same h.

## What I expect (before any number)

- TC Sharpe in L about 0.2-0.4 (managed futures' weak 2010s and strong 2022 are common
  knowledge); AQR factor about 1.0 in P and 0.3-0.5 in L; AQMIX below the factor in L. So h
  probably 60-80%, near H1's median.
- `tsmom12` correlation with TC: 0.1-0.3 (long only, coins, no shorts). `tsmom12-c00`: 0.2-0.4.
  Biggest split in 2022 (funds up, ours down). `sixty-forty` with RC: 0.7 or more.
- Our backtests ahead of their live family in L by more than 0.3, much of it from coins and
  from the long-only equity bull market.

## How it is logged

One `tries.md` row per one of our four series, new kind **`live-check`** (defined in the
header: a descriptive re-score of an already logged configuration over a live-fund window; not
selectable, not a strategy try, not counted in the family). Window L, repo-convention Sharpe.
No row in `ledger/tries.jsonl` (no new strategy). Family stays 65 mechanisms, 16 tested.
