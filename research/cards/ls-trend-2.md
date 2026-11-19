# ls-trend-2: does a blend of `tsmom12` and the wide long-short trend book, at gross <= 1, beat `tsmom12`?

Lane `ls-trend-2`, written 2026-11-18, **before any return of the blend, of the gross-1 book or
of the 1/3/12-month book was computed**. Base: `ls-trend-1` (`ls-trend-1.md`, `cards/ls-trend.md`,
`results/ls-trend.md`). What was seen before this card: ls-trend-1's tables (wide-LS at its
raw 3.7x gross: 2008 +34.9%, 2020-02..03 +24.6%, 2022 +12.8%, Sharpe 0.15 in L and 0.21 in L07,
16.5% vol, correlation 0.08 with `tsmom12`; `tsmom12` Sharpe 1.11 in L and 1.02 in L07, 22.5%
vol, crash windows -1.6% / -14.1% / -12.9%) and the ETFs' first bars.

Two parts. **Part A is a strategy test** with a pass rule (one blend, one try that counts).
**Part B is descriptive** (no pick): the Hurst-Ooi-Pedersen 1/3/12-month signal on the same
wide book, for fast crashes.

## Bars (quoted before any number)

- **Family bar** (the base lane's): 68 mechanisms, 16 tested, none passed; a strategy test
  passes at **p < 0.10 / 68 = 0.00147**. The blend is not a new mechanism (time-series momentum,
  long and long-short), so the family stays 68 / 16.
- **Project-wide bar** (`origin/register-1:research/register/BAR.md`, rows through 2026-11-18
  22:34; a PROPOSED convention): **2,904 distinct tries, N = 1,012 for a new pick**; Bonferroni
  one-sided p <= 0.05 / 1,012 = **4.9e-5** (z 3.89); deflated Sharpe 0.95 needs z >= 4.90 on
  the Sharpe edge over `tsmom12`. With this card's selectable rows N rises to about 1,014; the
  bar stays about 4.9e-5.
- **Which decides:** the family bar (the lane's instruction). A blend that passed the family bar
  but not the project-wide one would be written up as "family pass, not project-wide" and not
  proposed for the book.

## Part A: the blend (one configuration, fixed now)

### Sleeves

1. **`tsmom12`** exactly as logged (`baselines`, the six live assets with coins, weekly, the
   gym's costs), daily returns with cash earning the 13-week T-bill (`cash_interest.rescored`,
   as survey-5 and ls-trend-1 used). Long-only, gross <= 1.
2. **wide-LS at gross 1** ("wide-LS-g1"): ls-trend-1's wide-LS unchanged (34 ETFs, sign of the
   12-month excess return, 40% / ex ante vol, EWMA centre of mass 60 days, equal weight across
   the assets alive, decided at the month's last close, effective from the close of the next
   trading day), except that each month's target weights are **divided by their gross sum
   (sum of |w|)**, so the sleeve's gross is exactly 1 every day (weights are held at target
   between rebalances, as in ls-trend-1). Same rescaling for every month, no cap, no other
   change.

### Costs (stated now)

- wide-LS-g1: **5 bps a side** on traded notional at each monthly rebalance; **borrow 1.0% a
  year** on short notional; short proceeds and unused cash earn the bill (so a short earns
  -(r - rf) - borrow). At gross 1 nothing is financed (no leverage).
- `tsmom12`: the gym's own costs, already in its returns.
- Between sleeves: the split is reset monthly; within the month the sleeves drift. The reset
  trades |target - drifted| of capital in each sleeve; charged **5 bps a side** times that
  sleeve's gross (1 for wide-LS-g1, `tsmom12`'s invested share for `tsmom12`).
- Robustness (reported, does not decide): the same blend with **10 bps a side and 3% borrow**.

### Split (a rule that uses no returns' means)

**Equal risk between the two sleeves, from trailing volatility only.** At each month's last
calendar day, sigma_k = standard deviation of sleeve k's weekly excess returns (Monday-Sunday
weeks, sums of daily excess returns) over the trailing 52 complete weeks, x sqrt(52). Weight to
`tsmom12` a = (1/sigma_1) / (1/sigma_1 + 1/sigma_2), to wide-LS-g1 b = 1 - a, effective from the
next day. Both sleeves must have 52 weeks of returns; the blend starts the month after.

Why this and not a fixed split: the two sleeves differ about 4-5x in volatility (`tsmom12` about
22%; wide-LS-g1 about 16.5% / 3.7 = 4.5%), so a fixed 80/20 would give wide-LS about 5% of the
risk and could not show a crash effect; equal risk is the standard default for two sleeves of
unknown edge and is fixed by second moments only.

**Gross <= 1:** each sleeve's gross on its own capital is <= 1 (`tsmom12` long-only, wide-LS-g1
exactly 1), and the sleeves' capital adds up to the book, so the combined gross is <= 1 every
day (netting across sleeves can only lower it). Reported as a check.

### Window (train only)

- **Primary P = 2007-04-01..2025-10-31** (ls-trend-1's L07: the wide set has about 20 assets
  alive from 2007; contains all three crash windows). Daily calendar excess returns (weekends
  count as days; wide-LS-g1 has zero excess on non-trading days), Sharpe a year in the repo's
  convention (daily, 365).
- Secondary, reported: L = 2010-02-01..2025-10-31 and F = the blend's first full month..2025-10-31
  (before 2002 the wide set is SPY plus eight country ETFs; F is descriptive).
- Nothing after 2025-10-31 is read; the held-out year stays unspent.

### Pass rules

- **(a) Edge, decides.** Sharpe of the blend's daily excess returns in P is above `tsmom12`'s
  on the same days, one-sided paired stationary bootstrap (`stats.sharpe_diff_boot`, mean block
  20 days, **20,000 draws**, seed 0), **p < 0.00147**. Project-wide p <= 4.9e-5 reported next
  to it.
- **(b) Crash insurance, reported, does not decide.** The blend's compounded excess return is
  above `tsmom12`'s (a smaller loss or a gain) in **each** of 2008, 2020-02..03 and 2022.
  **(b) alone is a risk preference, not an edge.** It is nearly settled in advance: the blend
  holds `tsmom12` at a fraction a < 1 and wide-LS gained in all three windows, so dilution alone
  shrinks `tsmom12`'s losses. To make (b) say something, two descriptive controls, reported:
  - (b1) **dilution control:** `tsmom12` at the same daily split a, the rest in bills
    ("tsmom12-split-bills"). The blend minus this control is wide-LS-g1's own contribution.
  - (b2) **equal volatility:** `tsmom12` scaled by k = vol(blend) / vol(`tsmom12`) over P (a
    constant, ex post, descriptive), the rest in bills, crash windows compared.
- Verdict wording: (a) passes -> "edge at the family bar" (project-wide stated); (a) fails and
  (b) passes -> "a risk choice, not an edge"; both fail -> "neither".

### Measures (all that will be computed)

1. Sharpe in P, L, F; volatility; worst calendar year; max drawdown; for the blend,
   `tsmom12`, tsmom12-split-bills, wide-LS-g1 (and wide-LS raw, ls-trend-1's, for scale).
2. Split: mean, min, max of a; mean gross and mean net exposure of the combined book; max gross.
3. **Costs breakdown** a year in P: wide-LS-g1 trading, borrow, the split reset, `tsmom12`'s gym
   costs (from the gym's score if available, else "in its returns"), and at the blend's weights.
4. Crash windows 2008, 2020-02..03, 2022 (compounded monthly excess): blend, `tsmom12`, (b1),
   (b2), wide-LS-g1, wide-LS raw. **How much of the crash help survives at <= 1x:** wide-LS-g1
   / wide-LS raw in each window, and the blend's gain over (b1) in percentage points.
5. Monthly correlation in L of the blend with `tsmom12`, the nine-fund trend composite (TC) and
   SPY (survey-5's series).
6. Bootstrap difference, its p and 5%-95% interval, in P (decides) and in L (reported).

### What I expect (before any number)

- a about 0.15-0.25 (most of the capital in wide-LS-g1); blend volatility 5-7%.
- Blend Sharpe in P about 0.7-0.9, **below** `tsmom12`'s about 1.0: the maximum-Sharpe mix of a
  1.0 and a 0.2 Sharpe at correlation 0.08 is about 1.02, and equal risk is far from that mix.
  **(a) fails** with p near 1.
- wide-LS-g1 crash returns about raw / 3.7: 2008 about +9%, 2020-02..03 about +6%, 2022 about
  +3.5%; costs about 0.2% + borrow about 0.4% a year.
- (b) passes; (b1) passes (wide-LS-g1 positive in all three windows); (b2) the blend beats
  `tsmom12` at equal vol in 2020 and 2022, 2008 close.

### How it is logged (`tries.md`, idea `ls-trend-2`, period `train`)

- `blend-er@L07` **variant** (the one try that counts; P).
- `blend-er@L` and `blend-er@F` **robustness** (same configuration, other windows);
  `blend-er-cost2@L07` **robustness** (10 bps, 3% borrow).
- `tsmom12-split-bills@L07` **baseline** (dilution control; counted as selectable, which is
  conservative).
- `wide-LS-g1@L07` **replication** (the sleeve alone, not selectable).
- Sharpe in the rows: daily calendar excess returns, 365. No `ledger/tries.jsonl` line (the gym
  cannot hold shorts; nothing goes to the paper book).

## Part B: 1/3/12-month signal on the wide long-short book (descriptive, no pick)

Hurst, Ooi, Pedersen 2017 (L2) use an equal-weight combination of 1-, 3- and 12-month TSMOM.
Fixed now, the paper's specification on ls-trend-1's machinery, no tuning:

- Per asset, signal s = (sign(1-month excess) + sign(3-month excess) + sign(12-month excess)) / 3
  (values -1, -1/3, +1/3, +1), lookbacks 30, 91 and 365 calendar days back to the last bar on or
  before. Weight = s x 40% / sigma / N (the same sigma and N as wide-LS; eligibility unchanged:
  12 months of history). Monthly, same timing, same costs (5 bps, 1% borrow).
- Two scalings: raw ("hop-wide-LS", leverage financed at the bill as in ls-trend-1) and gross 1
  ("hop-wide-LS-g1", the Part A rescaling). HOP's 10% portfolio vol target is not built; crash
  returns are also shown at 10% vol (display scaling, ex post, as ls-trend-1).
- **Fast crashes** (compounded monthly excess): 2020-02..03 (the main one), 2018-10..12,
  2011-08..09, 2015-08..09; and for cost of speed, 2008 and 2022. Compared with wide-LS (12-month
  only) at the same scaling.
- **1987:** the ETF data start in 1993, so the wide book cannot reach it. One single-market line
  instead: S&P 500 price index (`GSPC`, from 1950; price only, no dividends, so excess is
  understated by the dividend yield), long-short, 12-month sign vs the 1/3/12 blend, monthly,
  40% / sigma, bills from IRX (from 1960; the line starts 1961), window 1987-10..1987-12 and
  1987-10 alone. Same costs, no borrow change.
- Also: Sharpe in L and L07, vol, turnover, costs a year, correlation in L with TC and with
  `tsmom12`.
- Reading (descriptive): the faster signal "helps in fast crashes" if hop-wide-LS's 2020-02..03
  return at 10% vol is above wide-LS's by more than 2 points; it "costs" if its Sharpe in L is
  lower. Both can hold.
- Logged as `replication` rows (not selectable, not counted): `hop-wide-LS@live-L`,
  `hop-wide-LS-g1@live-L`, `gspc-12m@1961` and `gspc-hop@1961`.

What I expect: hop-wide-LS turns over 2-3x more than wide-LS (costs up), Sharpe in L similar
(0.1-0.4), better in 2020-02..03 and 2018-Q4, worse in 2008 (whipsaw in the 2009 rebound is
outside the window; inside 2008 about equal); on the S&P alone, 1987-10 is a loss for both
(signals were long going into October) and the 1/3/12 blend loses less only if September was
down.
