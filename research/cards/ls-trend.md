# ls-trend: does a long-short, volatility-scaled TSMOM on a wider ETF set look like the live trend funds?

Lane `ls-trend-1`, written 2026-11-18, **before any return of the new series was computed**.
Literature: `ls-trend-1.md` step 1 (L1-L10). What was seen before this card: survey-5's
results (`results/live-check.md`, the funds' and `tsmom12`'s numbers) and, for the new ETFs,
only their names, first and last bars (`lib/lstrend1_fetch.py` prints nothing else).

This is a **descriptive replication of a published effect** (Moskowitz, Ooi, Pedersen 2012,
L1), built with negative weights and leverage that the paper broker cannot hold. It is **not a
candidate for the live book**: nothing is selected, there is no pass bar, no held-out data is
read, nothing is tuned. Its job is to answer one question: is `tsmom12`'s missing crisis alpha
the missing short side, the narrow universe, or both?

## The rule (fixed now; the paper's, not mine)

- **Signal:** sign of the asset's past 12-month **excess** return (total return from Yahoo's
  adjusted close, minus the 13-week T-bill compounded over the same days), computed from closes
  up to the last trading day of each month. L1 eq. 5, k = 12, h = 1.
- **Size:** each position has 40% ex ante annual volatility: weight = sign x 0.40 / sigma, sigma
  from L1 eq. 1: exponentially weighted daily squared (demeaned) returns, centre of mass 60
  days (delta = 60/61), times 261. Portfolio = **equal weight across the instruments alive**,
  i.e. each weight divided by N_t (L1's portfolio formula). No cap, no portfolio vol target.
- **Long-only variant (LO):** the same, with negative signs set to 0 (in or out, like
  `tsmom12`, but volatility-scaled).
- **Timing (no look-ahead):** weights decided at the month's last close take effect from the
  close of the **next** trading day (one day later than the paper; the repo's next-open rule,
  made conservative). Between rebalances the weights are held constant (daily rebalanced to
  target, as the paper's weight x monthly return).
- **Eligibility:** an asset enters once it has 12 months of history before the decision (and at
  least 60 daily returns for sigma). Nothing after **2025-10-31** is read (the held-out year
  starts 2025-11-11 and stays unspent).

## Universes (fixed now)

- **Wide** (34 ETFs, every one fetched by `lstrend1_fetch.py`; the list follows L1's four asset
  classes, not my choice of winners):
  - equity (9): SPY, EWA, EWG, EWP, EWQ, EWI, EWJ, EWN, EWU (L1's nine developed indexes:
    US, Australia, Germany, Spain, France, Italy, Japan, Netherlands, UK);
  - bonds (4): SHY, IEI, IEF, TLT (US Treasuries along the curve; no keyless non-US government
    bond ETF with a long enough hedged history);
  - commodities (15): GLD, SLV, PPLT, PALL, CPER, DBB, USO, BNO, UGA, UNG, CORN, WEAT, SOYB,
    CANE, DBA (single-commodity ETFs plus the base-metal and agriculture baskets; broad baskets
    such as DBC excluded as duplicates);
  - currencies (6): FXE, FXY, FXB, FXA, FXC, FXF (each against the US dollar; the trusts pay
    the foreign deposit rate, so excess return ~ the forward's return).
- **Narrow** (4): SPY, QQQ, GLD, TLT, the assets of `tsmom12-c00` (`tsmom12` without coins).

Four cells, a 2 x 2: **wide-LS** (the replication), **wide-LO**, **narrow-LS**, **narrow-LO**.

## Costs (fixed now)

- **Trading:** 5 bps per side on traded notional at each rebalance (above the gym's 2 bps for
  ETFs, because some of these ETFs are thin).
- **Shorting:** short notional pays a **borrow fee of 1.0% a year** (above general collateral
  for liquid ETFs; a round number meant to cover the harder-to-borrow commodity funds). Short
  sale proceeds earn the T-bill, so a short earns -(r - rf) - borrow.
- **Leverage:** long notional is financed at the T-bill (the papers' excess-return
  convention). Gross leverage is reported; the real cost of leverage above the bill is not
  modelled and is a known flattering of the replication (it is reported, not hidden).
- Returns are **excess over the T-bill**, as the funds' and the AQR factor's are compared in
  survey-5.

## Series compared (from survey-5, unchanged)

TC (nine live trend funds, equal weight alive), each fund alone, the AQR TSMOM factor (all and
its four asset-class columns TSMOM^CM, ^EQ, ^FI, ^FX), SPY, `tsmom12` and `tsmom12-c00`
(monthly excess series as computed by `survey5_live.py`).

## Measures (all that will be computed)

1. Sharpe a year (monthly excess, mean / sd x sqrt 12) in **L = 2010-02..2025-10** and
   **L07 = 2007-04..2025-10**; annual volatility, worst calendar year, mean gross leverage and
   mean net exposure (sum of weights), turnover and the yearly drag of costs and borrow.
2. Correlation of monthly excess returns in L with TC, each fund alive >= 36 months, the AQR
   factor, SPY, `tsmom12`, `tsmom12-c00`; and in L07 with RYMFX.
3. Crash returns (compounded monthly excess): **2008**, **2020-02..03**, **2022**; raw and
   **at 10% volatility** (times 10% / the series' own volatility in L07; a display scaling
   for comparing with funds that run 10-15% volatility, ex post, so descriptive only).
4. **Where the crash gains came from** (wide-LS and narrow-LS): additive daily P&L contribution
   summed over each crash window, by asset class x long/short leg (a position counts as long or
   short by its weight that day). Same crash windows for the AQR factor's four class columns
   (sum of monthly returns).
5. The 2 x 2 effects in each crash window and in L: **short effect** = LS - LO (each universe),
   **universe effect** = wide - narrow (each side), in crash returns at 10% vol and in
   correlation with TC.

## Reading rules (fixed now; descriptive, no pass or fail)

- wide-LS **"reproduces the funds' crash behaviour"** if its raw return is > 0 in **both** 2008
  and 2022 **and** its correlation with TC in L is >= 0.5 (survey-5's "moves with its live
  family"). 2020-02..03 is reported but not required (L2: too fast for a 12-month signal).
- The short side is **"the missing piece"** if wide-LS meets the rule above and wide-LO does
  not; the universe is **"the missing piece"** if wide-LS meets it and narrow-LS does not.
  Both can hold. If wide-LO already meets it, shorts are not needed; if wide-LS does not, the
  replication fails and the gap is something else (signal speed, fees, the funds' other
  sleeves), said plainly.
- Leg shares in measure 4 are read as "the short legs gave X% of the crash-window gain" only
  where the total is positive.

## What I expect (before any number)

- wide-LS: Sharpe in L 0.2-0.5 (between the funds' 0.19 and the AQR factor's 0.35, minus
  costs, plus no fees); correlation with TC 0.5-0.7, with the AQR factor 0.6-0.8; with SPY
  near 0. Positive in 2008 and 2022, about flat in 2020-02..03. 2008: most of the gain from
  short equity and short commodity legs plus long bonds; 2022: short bonds and long
  commodities, long USD (short FX ETFs).
- wide-LO: correlation with TC 0.3-0.5; small gain or loss in 2008, gain in 2022 from long
  commodities only.
- narrow-LS: 2022 gain from short TLT, 2008 from short SPY/QQQ and long TLT; correlation with
  TC lower than wide-LS (no commodities but gold, no currencies).
- narrow-LO: close to `tsmom12-c00` (correlation > 0.8), loses in 2022.
- Gross leverage of wide-LS 2-4x (SHY's 40% / ~2% vol, divided by N, is large): a sign that
  this cannot be held in the paper broker as it is.

## How it is logged

One `tries.md` row per cell (4 rows), a new kind **`replication`** (defined in the header: a
descriptive replication of a published effect built outside the live book's constraints, here
with shorts and leverage; not selectable, not a strategy try, not counted in the family).
Window L, Sharpe in the repo's convention (daily calendar series, 365, zero rate) on the
excess returns. No `ledger/tries.jsonl` row (no strategy for the paper book). The family stays
**68 mechanisms, 16 tested** (wide-6's reconciled count); the bar for any later strategy test
stays **p < 0.10 / 68 = 0.00147**, and long-short TSMOM is the same mechanism as `tsmom12`
(time-series momentum), so if it were ever proposed for the book it would be a variant of an
existing mechanism, judged forward, not a new family member.
