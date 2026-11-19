# ls-trend-2: `tsmom12` plus the wide long-short trend book at gross <= 1

Lane `ls-trend-2` of the night run, 2026-11-18. Branch `ls-trend-2` from `ls-trend-1` (draft
PR #89 into `ls-trend-1`). Research harness only: the live runner and the paper broker are not
changed. Fake money only.

Why: ls-trend-1 found that `tsmom12`'s 12-month rule run long-short and volatility-scaled on 34
ETFs (wide-LS) gains in crash years (+35% 2008, +25% 2020-02..03, +13% 2022) and moves with the
live trend funds, at a Sharpe above bills of 0.15 and 3.7x gross. Its correlation with
`tsmom12` is 0.08, so the open question was whether a blend, held at most 1x gross, is better
than `tsmom12` alone, or only safer.

## Step 1: card (7bb600f, before any number)

[`cards/ls-trend-2.md`](cards/ls-trend-2.md). Part A, one blend: `tsmom12` as logged, plus
wide-LS with each month's weights divided by their gross (gross exactly 1), equal risk between
the two from the trailing 52 weeks' volatility only, reset monthly; combined gross <= 1.
Costs stated: 5 bps a side, 1% a year borrow, 5 bps on the split reset; stress at 10 bps and
3% borrow. Decided by **(a)** the Sharpe gap to `tsmom12` in P = 2007-04..2025-10, paired
stationary bootstrap, at the family bar p < 0.10 / 68 = 0.00147 (project-wide from
`register-1` BAR.md: 2,904 tries, N 1,012, p <= 4.9e-5). **(b)** smaller crash losses than
`tsmom12` in 2008, 2020-02..03 and 2022 is reported as a risk preference, not an edge; the
card said in advance that dilution alone nearly guarantees (b), and added two controls (b1:
`tsmom12` at the same split with the rest in bills; b2: `tsmom12` at the blend's volatility).
Part B: the 1/3/12-month signal, descriptive.

## Step 2: the blend (script 4b090ab, run 2026-11-18)

Tables: [`results/ls-trend-2-blend.md`](results/ls-trend-2-blend.md). Disclosure: the first
launch stopped with a division by zero before printing or logging anything (`tsmom12` sits in
cash in its first months, so its trailing volatility was 0). Fix, before any number: the
`tsmom12` sleeve starts on its first invested day, and a month where a sleeve's trailing
volatility is 0 keeps the previous split (6 months, all before P). The wide-LS raw book
reproduces ls-trend-1 exactly (+34.9% / +24.6% / +12.8%).

**Logged:** 6 rows in `tries.md` (`blend-er@L07` variant, the one that counts; three
robustness rows; `tsmom12-split-bills@L07` baseline; `wide-LS-g1@L07` replication). No
`ledger/tries.jsonl` line (the gym cannot hold shorts). Family unchanged: 68 mechanisms, 16
tested, none passed.

### Result

| | Blend | `tsmom12` | b1: `tsmom12` + bills, same split | wide-LS at gross 1 |
|---|---:|---:|---:|---:|
| Sharpe P (decides) | **0.97** | **1.21** | 1.26 | 0.14 |
| Sharpe L (2010-02..) | 1.13 | 1.32 | 1.46 | 0.09 |
| Volatility P | 5.4% | 18.3% | 3.6% | 5.1% |
| Max drawdown P | 8.8% | 38.3% | 5.6% | 16.2% |
| 2008 | **+8.9%** | -1.6% | +0.9% | +13.9% |
| 2020-02..03 | **+2.2%** | -14.1% | -2.4% | +5.5% |
| 2022 | **+2.0%** | -12.9% | -1.5% | +3.3% |

1. **(a) fails.** The blend's Sharpe is 0.24 **below** `tsmom12`'s in P (bootstrap p 0.89
   that it is better; 5%..95% -0.58..+0.09), and 0.18 below in L. Expected in the card (a 1.0
   and a 0.2 Sharpe at correlation 0.08 cannot mix to much above 1.0, and equal risk puts
   about three quarters of the capital in the weak one). Mean split to `tsmom12`: 0.26.
2. **(b) holds, and not only by dilution.** The blend gained in all three crash windows
   while `tsmom12` lost. Against the dilution control (b1) the wide sleeve added +8.0, +4.6 and
   +3.5 points; against `tsmom12` scaled to the same 5.4% volatility (b2, -0.4% / -3.8% /
   -3.9%) the blend is also ahead in all three. That is real crash insurance.
3. **Its price is the Sharpe.** The same capital in bills instead of the wide sleeve (b1)
   has Sharpe 1.26, above both: the equal-risk split by itself (volatility timing of
   `tsmom12`) helps, and the wide sleeve then costs about 0.3 of Sharpe in exchange for the
   crash gains. Correlation of the blend with the nine live trend funds 0.49 in L (`tsmom12`
   0.17), with SPY 0.23.
4. **Costs at <= 1x are small:** 0.50% a year in the blend (wide sleeve trading 0.11%, borrow
   0.32%, `tsmom12`'s gym costs 0.06% at its weight, split resets 0.02%). At 10 bps and 3%
   borrow the blend's Sharpe in P falls to 0.83 and its 2022 gain to +0.6%.
5. **How much crash help survives at gross 1:** wide-LS at gross 1 keeps 40% of its raw 2008
   gain, 22% of 2020's and 26% of 2022's (+13.9%, +5.5%, +3.3%; about 1/3.7 as expected, more
   in 2008 because the raw book's leverage was lower then). In the blend, at about three
   quarters weight, that is +8.0 / +4.6 / +3.5 points over the control.
6. **Size of returns at <= 1x.** The blend runs at 5.4% volatility, so about 5% a year above
   bills (Sharpe x vol), against about 22% for `tsmom12` at 18.3% volatility. Without leverage
   the blend is a small, steady book; it is not a way to keep `tsmom12`'s return and add
   insurance.

**Verdict (card's wording): a risk choice, not an edge.** Nothing is proposed for the book.

## Step 3: the 1/3/12-month signal for fast crashes (descriptive, not a pick)

Tables: [`results/ls-trend-2-hop.md`](results/ls-trend-2-hop.md). Card Part B, the
Hurst-Ooi-Pedersen signal (mean of the signs of the 1-, 3- and 12-month excess returns) on the
same 34 ETFs, otherwise wide-LS unchanged. 4 `replication` rows (not selectable, not counted).
After the run, one display fix only: the 1987 table first showed the position held on 1 October
(the August decision, the same for both cells) instead of the October position; it now shows
the position held through October, and the index's own September and October moves.

| | wide-LS (12-month) | 1/3/12 blend | Live funds (TC) |
|---|---:|---:|---:|
| 2020-02..03 at 10% vol | +15.0% | **+25.9%** | +3.6% |
| 2011-08..09 at 10% vol | -8.6% | -0.3% | -2.9% |
| 2018-10..12 at 10% vol | -1.8% | -1.5% | -3.6% |
| 2008 at 10% vol | +21.2% | +24.1% | +7.1% |
| 2022 at 10% vol | +7.8% | +4.0% | +17.6% |
| Sharpe L (daily) | 0.15 | **-0.09** | |
| Turnover a year, L | 13x | 29x | |
| Costs + borrow a year, L (raw leverage) | 2.5% | 2.7% | |
| Correlation with TC in L | 0.61 | 0.65 | |

Plain verdict for a human:

- **Faster signals do help in fast crashes, and they cost in normal years.** In February and
  March 2020 the 1/3/12 blend made about 11 points more than the 12-month rule at the same
  volatility (short oil and gas, short equities after February's fall, long bonds); in the
  August 2011 sell-off it lost almost nothing where the 12-month rule lost 9 points. But it
  trades twice as often, and from 2010 to 2025 its Sharpe above bills is below zero (-0.09;
  -0.04 at gross 1), against 0.15 for the 12-month rule. It gave up half of 2022's gain, a slow
  bear market where the 12-month signal is the right speed.
- **It is not a way to catch a one-day crash.** 1987 is before the ETFs exist; on the S&P 500
  alone, the 1/3/12 blend was still **long** going into October 1987 (September was down 2.4%,
  but the 3- and 12-month trends were up), at a third of the 12-month rule's position, so it
  lost a third as much (-16.5% vs -58.1% at the cells' 40% single-market sizing, about -4% vs
  -15% at 10% volatility). A crash that comes out of a calm up-trend is lost by every trend
  speed; faster signals only lose less because they are less sure.
- **Bottom line:** speed buys fast-crash protection with Sharpe. On these ETFs the trade looks
  worse than the 12-month rule overall. It moves slightly more with the live funds (0.65), which
  fits HOP's paper, where the funds use a mix of speeds.

## Count and next

Family unchanged: 68 mechanisms, 16 tested, none passed (p < 0.00147); project-wide
`register-1` N 1,012 before this lane (p <= 4.9e-5), plus this lane's 2 selectable rows
(`blend-er@L07` variant, `tsmom12-split-bills@L07` baseline). Rows added: 10 (1 variant, 3
robustness, 1 baseline, 5 replication). Held-out year unspent.

Next, each a card before numbers:
1. **Volatility timing of `tsmom12` alone** (control b1 had Sharpe 1.26 vs 1.21 with half the
   drawdown: an equal-risk split against bills is volatility targeting). Card: `tsmom12` at a
   fixed volatility target from trailing volatility, judged at the bar against `tsmom12`; the
   literature (Moreira-Muir 2017; Kim-Tse-Wald 2016) predicts small gains. Note b1 was not a
   pick here; testing it is a new try.
2. **Insurance sizing as a risk choice:** a menu of fixed splits between `tsmom12` and
   wide-LS-g1 (for example 90/10 to 50/50) shown on the risk map (worst year vs mean), not a
   test, for the owner to pick a crash profile.
3. **Shorts in the gym** (ls-trend-1 proposal item 2), if a crash sleeve is wanted forward;
   nothing in this lane needs it for research.
