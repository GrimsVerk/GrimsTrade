# rp-1: why `where-vol` lost more than live risk-parity funds in 2022

Research lane rp-1 (DEEPER), night 2026-11-18. Branch `rp-1` from `survey-5`, draft PR #86 into
`survey-5`. Research only: fake money, the price cache and survey-5's fund series already on
disk, no change to the gym, the runner or the live rules. Held-out year (2025-11-11 ..) untouched.

Why: `where-vol` (lane trend-where) is the near-miss partner in combo-1's best blend `blend-ws`
(Sharpe 1.13 vs `tsmom12` 1.05; 1.16 vs 1.08 with T-bill cash in combo-2), which fails the bar
and is behind in 2022-25. Survey-5's live check put `where-vol` in the risk-parity family and
found it lost -27.4% in 2022 (above bills) against -17.8% for the live risk-parity funds (RC =
ABRZX, AQRIX, RPAR), and advised checking that before any revival.

## Step 1: diagnosis (descriptive, 2026-11-18)

Tables: [`results/rp-1-diag.md`](results/rp-1-diag.md), from `lib/rp1_diag.py`. Two logged
configurations re-scored with `log=False` (they reproduce their logged Sharpe, `where-vol` 1.07,
`tsmom12` 1.05); no strategy run, nothing selectable, no `tries.md` row. Returns here are total
returns with cash at 0 (gym rule): `where-vol` -26.6% in calendar 2022, RC -16.1%, `tsmom12`
-12.8%. Fund exposures are trailing 63-day regressions on SPY, TLT, GLD, DBC (US proxies for
global books: approximate).

**In one line: `where-vol` is not a risk-parity book, and its 2022 gap to the funds is the coin
slot. Bonds, leverage, rebalance speed and the stock-bond correlation do not explain it.**

| Calendar 2022, arithmetic contribution | `where-vol` | `tsmom12` | RC (beta x factor) | `where-vol` minus RC |
|---|---:|---:|---:|---:|
| Stocks | -5.5 | -5.5 | -4.6 | -0.9 |
| Long bonds (TLT) | -5.9 | -0.8 | -9.4 | **+3.5** |
| Gold | +0.1 | -1.4 | +0.5 | -0.4 |
| Commodities (DBC) | 0 | 0 | +1.9 | -1.9 |
| Coins (BTC + ETH) | **-17.3** | -5.0 | 0 | **-17.3** |
| Fund residual (non-US assets, TIPS, credit, fees) | 0 | 0 | -5.3 | +5.3 |
| Sum (points) | -28.6 | -12.7 | -16.9 | -11.7 |

1. **Which slots.** At the 2022 refit `where-vol` held TLT, GLD and BTC with no filter (their
   past out-days were calmer than in-days: ratio 0.77, 0.86, 0.76) and kept the filter on SPY,
   QQQ and ETH. It entered 2022 fully invested in six equal slots of 1/6.
2. **Where the risk sat.** Going into 2022 the two coin slots, a third of the money, carried
   **89% of the book's risk** (BTC 39%, ETH 50%; 2021-H2 vols 61% and 76%); TLT carried 0%.
   The book's ex-ante volatility was 24%; the funds ran at 7-8%. Equal dollars is the opposite
   of equal risk.
3. **When it de-risked.** By the trend filter it cut SPY/QQQ in April-May and ETH in May:
   invested share 1.00 -> 0.50 by July. The half it kept was TLT, GLD and BTC, held all year.
   BTC alone cost -13.7 points (asset -64%), ETH before its exit -3.6.
4. **The funds did not de-risk at all in 2022.** RC's summed betas stayed at 0.82-0.86 through
   Q3 (0.73 at year end), its TLT beta rose from 0.22 to 0.30, and its volatility went from 7% to
   13%. Their smaller loss is a smaller book volatility to start with plus a commodity sleeve
   (+1.9 points), not faster selling.
5. **Bond duration is not the gap; it is in `where-vol`'s favour.** The funds carried about
   0.22-0.30 TLT-equivalent (RPAR 0.33-0.55) against `where-vol`'s 0.17 and lost -9.4 points on
   it against -5.9. Against `tsmom12`, though, the unfiltered TLT slot cost 5.1 points (the
   filter was out of TLT all year).
6. **The stock-bond correlation turned late.** The 63-day SPY-TLT correlation was negative
   until June 2022 and positive only from August (+0.08 .. +0.29), when most of the loss was
   in. `where-vol` makes no correlation assumption (equal slots), and its bond slot was never
   where its risk was. A correlation regime switch would not have changed 2022 much.

**Attribution of the 9.6-point gap survey-5 reported (here 10.5 total-return points, 11.7
arithmetic):** coins -17.3 (more than all of it), commodity sleeve -1.9, stocks -0.9; offset by
smaller bond exposure +3.5 and the funds' own non-US/fees residual +5.3. Against `tsmom12`
(13.8 points): coins -12.3, TLT -5.1, gold +1.5.

**Is the cause structural?** Yes, and it is one cause: `where-vol` sizes slots in equal dollars
and, once the filter is dropped on BTC (from 2019), nothing limits a 60-80%-volatility slot.
The trend-where card's yes/no reads each asset's own out-day versus in-day volatility, and a
coin's slow bear years look calm next to its bull runs, so the test removes the only risk
control the coin slot had. Survey-5's comparison with risk-parity funds was therefore a category
mismatch: the funds are risk-sized and unlevered coins are absent from them. But it points at
the risk-parity literature's own core idea (size by risk, not by dollars) as the fix to test.
Step 2 cards one.

## Step 2 card: `where-rp` (fixed 2026-11-18, before any number of this rule)

**What had been seen when this was written.** Step 1's 2022 tables above (2021-07 .. 2023-06
only); the full-train numbers already logged elsewhere: `where-vol` 1.07, `tsmom12` 1.05,
`trend-vol` (tv40, per-slot vol cap) 1.03, `inverse-vol` 0.85, equal weight 0.88; combo-1's
failure map and blends; survey-5's live check. No number of `where-rp` exists in any period.

**The fix, from the risk-parity literature.** Size slots by risk, not by dollars:

- Maillard, Roncalli and Teiletche, "The Properties of Equally Weighted Risk Contribution
  Portfolios", Journal of Portfolio Management 36(4), 2010, pp. 60-70 (doi
  10.3905/jpm.2010.36.4.060) `[secondary: bibliographic record and abstract]`. Equal risk
  contribution (ERC) portfolios; volatility between minimum variance and equal weight; when all
  pairwise correlations are equal the ERC weights are proportional to 1/volatility.
- Kirby and Ostdiek, "It's All in the Timing: Simple Active Portfolio Strategies that
  Outperform Naive Diversification", Journal of Financial and Quantitative Analysis 47(2),
  2012, pp. 437-467 `[secondary: abstract]`. Volatility timing: weights from estimated
  volatilities only (1/vol), low turnover, ahead of 1/N after costs in their tests.
- Qian, "Risk Parity Portfolios", PanAgora white paper, 2005 `[not checked]`: the origin of the
  name; equal risk shares instead of 60/40 dollar shares.

Correlation-aware ERC and a stock-bond correlation regime switch (the practitioner response to
2022) were considered and **not** chosen: step 1 shows the stock-bond correlation turned
positive only from August 2022 and `where-vol`'s bond slot carried 0% of its risk, so they act
on the wrong slot. The naive (1/vol) form is also the protocol's own `inverse-vol`, so no new
estimator or parameter is introduced.

**Rule `where-rp`.** `where-vol` exactly (same `Where("vol")` yes/no per asset, same refits,
same Friday `tsmom12` signals), with one change: an eligible asset's slot is the protocol's
`inverse-vol` weight (1 / EWMA volatility with 60-bar half-life on its own clock, normalised to
sum to 1 over all eligible assets) instead of 1 / (number of eligible assets). A slot is held at
that weight if the asset's answer is no, or if it is yes and its `tsmom12` signal is on; else
that weight sits in cash. Unlevered (invested share at most 1), no volatility target, no other
parameter. Friday decisions, the gym's fills and costs (protocol: 25 + 5 bps crypto, 2 bps
ETFs, 1% band), total-return prices, cash 0.

**Twin:** `tsmom12`. Also shown, not judged against: `where-vol`, `inverse-vol`, equal weight.
**Idea name** in `tries.md`: `rp-1`. Rows: one `variant` (six assets), three `robustness`
(8 other ETFs, 6 other coins, 4 indexes as one book; rule unchanged, refitted on each set's
own history). Run once.

**Pass bar (all must hold; six assets, train 1994-02-01 .. 2025-11-09):**

1. Sharpe beats `tsmom12`, paired stationary bootstrap (block 20 days, 2,000 draws), one-sided
   **p < 0.10 / 74 = 0.00135**. Family: combo-2's count of 73 (the `wide-*` lineage, survey-4,
   wide-5, deep-1's combinations, combo-1's two blends, combo-2's `cofall-dbc`) plus this one;
   the survey-5 lineage count (65 + 1 = 66, p < 0.00152) is looser, so the stricter is used.
   **Project-wide bar** (`origin/register-1:research/register/BAR.md`, rows through
   2026-11-18 22:34): 2,904 distinct tries, **N 1,012 for a new pick, Bonferroni p <= 4.9e-5**
   (z 3.89); DSR 0.95 needs an edge of about +0.32 Sharpe for a rule close to `tsmom12`. A
   family pass that misses the project-wide bar is reported as such and is not a pick.
2. Ahead of `tsmom12` on Sharpe in at least 4 of the 5 eras.
3. Worst loss not more than 5 points deeper than `tsmom12`'s.
4. Out of universe: Sharpe difference to `tsmom12` positive in at least 2 of the 3 sets.
5. Beats equal weight on Sharpe.
6. Since 2003-01-01: not behind `tsmom12` and not behind equal weight on Sharpe.

**Also read off (the reason for the card; not a bar):** total return in calendar 2022 and in the
protocol's 2022 rate-shock window for `where-rp`, `where-vol`, `tsmom12`; the 2022 slot
contributions as in step 1; average coin weight.

**Expected before looking.** The coin slots shrink from 1/6 each to roughly 1/20 (vols 60-80%
against 12-15%), so the 2022 loss should fall to about `tsmom12`'s or less. But the coins
carried most of the book's growth, and every risk-sizing of this book seen so far lost Sharpe
(`inverse-vol` 0.85 against equal weight 0.88; `trend-vol` 1.03 against `tsmom12` 1.05). So
the likely outcome is a shallower 2022 at a lower or equal Sharpe: a risk choice, not an
edge. Chance of passing bar 1: under 1%.

**What each outcome means for step 3.** `where-vol` / `blend-ws` are revived only if `where-rp`
passes all six bars; then a blend with `stop-0.25` would need its own card and the held-out
year one look, in a later lane. If `where-rp` fails, both stay closed and the 2022 question is
answered: `where-vol`'s extra loss was the coin slot's dollar size, a risk level, not a flaw a
risk-parity fix turns into an edge.

Held-out year (2025-11-11 .. 2026-11-09): not touched in this lane.

## Step 2 result: `where-rp` ties `tsmom12` and fails (one run, 2026-11-18)

Tables: [`results/rp-1.md`](results/rp-1.md), from `lib/rp1_run.py` (rule `lib/rp1_rule.py`,
test `tests/test_rp1.py`: all-no answers give exactly `inverse-vol`, all-yes filter it by
`tsmom12`, no later bar is read). Code pushed before the run (6190b78). 4 rows in `tries.md`
(1 `variant`, 3 `robustness`). Held-out year untouched.

| Six assets, 1994-2025 | Sharpe | vs `tsmom12` (p) | Growth/yr | Vol | Worst loss | 2022 | Since 2003 | 2022-25 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `where-rp` | 1.05 | +0.00 (0.50) | +12.4% | 11.8% | 24.5% | -19.7% | 1.31 | 0.98 |
| `where-vol` | 1.07 | +0.03 (0.27) | +18.9% | 17.5% | 35.3% | -26.6% | 1.23 | 0.83 |
| `tsmom12` | 1.05 | | +17.8% | 17.1% | 36.5% | -12.8% | 1.20 | 0.88 |
| RC (live risk-parity funds) | | | | | | -16.1% | | |

**Bar: fails bar 1** (+0.003 Sharpe, p 0.50 against p < 0.00135; project-wide p <= 4.9e-5 not
met either); passes the other five (4 of 5 eras, worst loss 24.5% vs 36.5%, out of universe
+0.08 / +0.08 / -0.01, above equal weight, since 2003 1.31 vs 1.20).

1. **The coin problem is fixed and a bond problem appears.** Coin weight fell to 7% on average
   (from up to 33%); 2022 coin loss -6.4 points instead of -17.3. But inverse-vol gives the
   calm, unfiltered TLT the largest slot, and TLT now costs -8.2 points (was -5.9). 2022:
   -19.7%, between the funds (-16.1%) and `where-vol` (-26.6%), still 7 points worse than
   `tsmom12` (-12.8%), whose filter was out of TLT and BTC all year. The 2022 rate shock is
   the same story as for the live risk-parity funds: risk-sizing loads up on the asset that
   was calm until it was not.
2. **Same Sharpe, lower risk: a risk dial, not an edge.** `where-rp` runs at 11.8% volatility
   against 17.1%; `tsmom12` scaled to 69% invested would have about the same Sharpe, volatility
   and worst loss (36.5% x 0.69 = 25%). The bootstrap range is wide (-0.18 .. +0.19) because
   the book is far from `tsmom12`, so nothing smaller than about +0.3 could ever clear the bar.
3. Out of universe the rule changes little (ETFs +0.08, coins +0.08: the same signs
   `where-vol` had; indexes -0.01).

The outcome is the one the card expected (a shallower worst loss at the same Sharpe).

## Step 3 verdict: do not revive `where-vol` or `blend-ws`

**Plain answer: no.** `where-vol`'s extra 2022 loss was not a risk-parity design error that a
risk-parity fix repairs. It was the trend-where idea itself: it drops the trend filter on the
slots whose past falls were calm (TLT, GLD, BTC), and in 2022 those were exactly the slots that
fell. Sized in dollars the loss came through BTC; sized by risk it comes through TLT. Either way
the book holds what `tsmom12` would have sold. The Sharpe edges are +0.03 (`where-vol`),
+0.00 (`where-rp`) and +0.08 (`blend-ws`, in-sample pick), against a family bar of about +0.15
and a project-wide bar of about +0.3.

**What evidence would revive them** (none of it exists, none of it is cheap):

- On train: a variant clearing p < 0.10 / 75 and the project-wide bar (N 1,012, p <= 5e-5) with
  2022-25 not behind `tsmom12`. Every variant of this line so far sits at +0.00 to +0.08.
- On new data: a non-stock history long enough to hold more than one joint bond-and-risk-asset
  fall with the filter dropped (bonds and gold before 2002; trend-where found none keyless).
  Without it the worst-loss question rests on 2022 alone.
- Forward: `blend-ws`'s excess over `tsmom12` (information ratio about 0.28) needs about a
  century to show at 80% power (combo-1), so a forward test cannot decide it either.

**What stands instead.** `where-rp` shows that this book can have `tsmom12`'s Sharpe with a
24.5% worst loss and 12.4% growth a year: a risk level, the same choice as holding less of
`tsmom12`. If the owner wants a shallower book, the plain way is a smaller `tsmom12`, not a new
rule. The survey-5 comparison is also settled: `where-vol` is not a risk-parity book (equal
dollars, coins 89% of its risk going into 2022), so the live risk-parity funds are not its
benchmark.

Count: family 74 (combo lineage; survey-5 lineage 66), none passed. Next test at
p < 0.10 / 75 = 0.00133; project-wide N 1,013 after these rows.
