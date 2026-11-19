# Breadth screen: do multi-signal's five signals get their published signs back on 34 ETFs?

Research run breadth-screen, 2026-11-19, branch `breadth-screen` (from `multi-signal`). Card
`cards/breadth-screen.md` (ad2ca1a, before any number), script `lib/breadth_screen.py`
(dbf014a, before its run), one run (3d54d58). Table: `results/breadth-screen.md`. Descriptive
screen only: no backtest, no pick, no strategy try, held-out year not loaded. **Logged as 6
`screen` rows** (idea `breadth-screen`, variants `@wide34`: 5 signals + `tsmom12`), not
selectable and not counted as strategy tries.

Universe (chosen in the card before computing): ls-trend-1's 34 cached keyless ETFs, not the
~16 out-of-universe markets: equity 9 (SPY + 8 developed-country funds), Treasuries 4 (SHY,
IEI, IEF, TLT), commodities 15, currencies 6. Signals exactly as in multi-signal's card. Ranks
are taken **within each class** (classes with >= 3 funds that week), and the weekly IC is the
mean over classes. About 24 funds and 3 classes a week from 1997 (multi-signal: 4.9 assets, no
class ranks).

## In plain words

**No. Breadth does not bring the published signs back for the card's five signals.** With five
times the cross-section, all five primary ICs sit within +-0.02 of zero, and the chance level
halves (shuffled-label 95th percentile 0.015, against 0.030 on the six), so this is a sharper
"nothing", not a noisier one. Cross-sectional momentum, the one positive signal on the six
(+0.043), is -0.005 here: its six-asset IC came from ranking across classes (coins and QQQ
against bonds), not from the within-class effect AMP describe. Low volatility still points the
wrong way.

| Signal (card's definition, / sigma) | IC week (95%) | IC month | Beyond `tsmom12`, week (99.5%) | Partial IC-IR | Published sign back? |
|---|---:|---:|---:|---:|---|
| value (AMP, -5-year return) | +0.005 (-0.015..+0.023) | -0.007 | -0.000 (-0.027..+0.025) | -0.01 | positive, not distinct from 0 |
| carry (Koijen et al.; no commodities) | -0.012 (-0.029..+0.006) | -0.027 | -0.007 (-0.031..+0.017) | -0.16 | no (inside 0) |
| XS momentum (AMP 12-1) | -0.005 (-0.022..+0.013) | -0.011 | -0.004 (-0.023..+0.015) | -0.09 | no (inside 0) |
| low-vol (-1-year vol) | -0.017 (-0.033..-0.000) | -0.019 | -0.020 (-0.043..+0.003) | -0.45 | no, reversed |
| BAB (FP, -beta to SPY) | +0.003 (-0.016..+0.023) | -0.008 | -0.001 (-0.026..+0.025) | -0.02 | positive, not distinct from 0 |
| reference `tsmom12` | -0.005 (-0.028..+0.018) | -0.028 | - | -0.09 | - |

None passes the card's bar (each fails 1, 2 and both size tests; value, XS momentum and BAB
fail 3 too). Placebos: value, carry, XS momentum and BAB sit inside shuffled-label chance
(p 0.14-0.67); low-vol is just outside it (p 0.02), but fixed relabels within class reach it
15% of the time.

## What the secondary looks show (4 extra looks, not in the bar, no placebo B)

- **Carry without the `/ sigma` scaling (Koijen et al.'s raw within-class ranks) has the
  published sign**: IC +0.029 (95% +0.012..+0.046), beyond `tsmom12` +0.026, positive in all
  four eras (+0.026..+0.046 partial) and at a month (+0.022, interval touches 0). It lives in
  Treasuries (+0.092: with an upward curve the longer funds have more carry and earned more,
  i.e. the term premium ranked along one curve) and currencies (+0.032, classic FX carry), not
  in equities (-0.009). Partial IC-IR +0.54, just under the 0.59 wide-book reading. The card's `/ sigma`
  turns it negative (Treasuries -0.040): with an upward curve it pushes SHY (small carry, tiny
  vol) to the top.
- **Value (raw) and BAB (FP's own class markets) are reversed**: -0.025 (-0.045..-0.006) and
  -0.029 (-0.046..-0.013). Raw value's reversal comes from Treasuries (-0.066) and equities
  (-0.020); in commodities it is +0.011.
- **XS momentum (raw)** +0.012 (-0.008..+0.033): the paper's sign, not distinct from 0.
- **On the risk-adjusted target** (return / sigma) the low-risk signals turn positive: low-vol
  +0.042, BAB against class markets +0.036, XS momentum +0.051 (week; no intervals computed).
  Low-risk funds earned less in raw terms but more per unit of risk, within class: FP's premise
  (a flat risk-return line) holds here, but only a levered long-short book collects it, which
  the paper broker cannot hold.

## Is anything large enough for a future wide book?

**No.** The size bar was a partial weekly IC >= 0.10 (multi-signal's) or a partial IC-IR >=
0.59 (the edge BAR.md asks of a far rule over `tsmom12`). The best primary IC-IR is -0.01;
the best secondary is raw carry at +0.54, which is (a) one of four post-card extra looks, (b)
in-sample over 1997-2025 with no placebo B, (c) an IC-IR, an upper bound on a rank-weighted
long-short book's Sharpe before costs, borrow and leverage, and (d) in Treasuries a duration
bet along one curve, not 10-40 independent bond markets. Any wide book built on it would be a
new pick and face the project-wide bar (register-1 `BAR.md`, rows through 2026-11-18 22:34):
**2,904 tries, N 1,012, Bonferroni p <= 4.9e-5; DSR edge +0.32 (close) / +0.59 (far) over
`tsmom12`, or an annual Sharpe of 1.32 against zero over 32 years.** Raw carry's weekly IC
series has a t of about 0.54 x sqrt(28) ~ 2.9 before the block structure, short of z 3.89.

## Why it still differs from the papers

The papers' breadth is 10-40 *independent markets per class* (country bond futures, country
equity futures, currency forwards, commodity futures with their own curves). Here a class is
US-listed funds: eight developed-country equity funds that move together, four Treasury funds
on one curve, commodity ETFs whose returns include roll costs that differ by fund. Breadth by
count (24) is far above the six; independent breadth is not. Keyless ETF data cannot rebuild
the papers' universes, so this screen bounds what a keyless ETF book could see: nothing at the
size that would matter.

## Assumptions (noted, not tuned)

- Commodities have no carry (the futures basis is not in the cached data; the card's GLD rule
  would rank only vol). Treasury carry uses cached `DGS2`/`DGS10` (IEI interpolated, IEF and TLT
  share `DGS10`). Equity and currency carry = trailing distribution yield minus the bill.
- QQQ left out (as in ls-trend-1's wide set). Placebo B is 2,000 random within-class relabels.
- The equity class qualifies from 1997 (country funds' first year), Treasuries from 2003,
  currencies from 2007, commodities from 2008.
