# short-sleeve: a small SPY/QQQ downtrend short next to `tsmom12` (verdict)

Lane `short-sleeve`, 2026-11-19, branch `short-sleeve` from `ls-trend-1` (draft PR #99).
Card `cards/short-sleeve.md` (42ab4b1, before numbers), script `lib/shortsleeve1.py`
(f7440e9, before its run), one run: `results/short-sleeve.md`. Research harness only; the
gym, the live runner and the paper broker are unchanged.

**Books.** Both 90% `tsmom12` (the logged baseline, cash at the T-bill). `bill10`: 10% in
T-bills. `short10`: 5% short SPY and 5% short QQQ, each only while its own 12-month total
return is negative, else bills; proceeds and collateral at the bill, 1%/yr borrow, 5 bps a
side, one day later than the gym's fill. 1994-2025 train window.

| 1994-2025 | `bill10` | `short10` |
|---|---:|---:|
| Sharpe above bills | 0.933 | 0.922 (d -0.011, SE 0.014, z -0.78, p 0.79) |
| CAGR / max drawdown | +16.8% / 32.1% | +16.7% / 32.8% |
| 2008 / 2020-Q1 / 2022 | -0.0% / -5.9% / -9.9% | +2.5% / -6.9% / -8.8% |
| Dot-com bust (2000-03..2002-10) | -19.8% | -13.6% |
| Years the sleeve added | | 6 of 32 (2000, 2001, 2002, 2008, 2022, one other) |

**Insurance, insure-1 style** (log points, `short10` minus `bill10`), SPY's three 25% falls
(2000-02, 2007-09, 2020; 2022's fall was under 25% on total return): loss avoided in all three
(+7.4, +4.5, +0.3; sum +12.3), handed back in the year after the trough (-10.7) and in calm
markets (-5.2). **Premium 1.30** log points given up per point avoided (QQQ's eight falls:
1.17). Sleeve's worst years: 2009 -3.1%, 2020 -2.7%, 2003 -2.1%: the 12-month sign is still
short when the market turns.

## Verdict

1. **Edge: no.** d -0.011 above bills, z -0.78: far from the family bar (p < 0.00147) and the
   project bar (z >= 4.65, N_eff 433, Bonferroni p <= 1.2e-4).
2. **Insurance: not by the card's rule.** It helped in 2008 (+2.6 points of the book) and 2022
   (+1.1) and most in 2000-02 (+6.2), but lost in 2020-Q1 (-1.0): the V crash came before the
   12-month sign turned, and the sleeve was short into the rebound. Loss avoided in every slow
   bear market, but at a **premium above 1** (dearer than `tsmom12`'s own trend insurance, 1.07
   in insure-1). A reader who wants smaller slow-bear losses at that price could prefer it; that
   is **a risk preference, not a pick that clears the bar**. Nothing goes to the paper book.
3. As expected on the card: slow bear markets pay, V-shaped ones cost, whipsaw years cost. On
   two equity ETFs at 10% of the book the effect is small either way (sleeve -0.1% a year).

Count: 1 pick (`short10@bills`, variant) + 1 baseline (`bill10@bills`) in `tries.md`; no
`ledger/tries.jsonl` line (the gym cannot hold shorts). Family unchanged: 68 mechanisms, 16
tested, none passed (same mechanism as `tsmom12`). Held-out year unspent.

Disclosure: the card's stated time ("~00:05 UTC") is a slip; its commit is 00:00:03, the
script 00:02:01, the run 00:02.
