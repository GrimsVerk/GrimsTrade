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
