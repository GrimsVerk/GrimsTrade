# e4-anatomy-1: where does `e4`'s lead over `tsmom12` come from?

Lane `e4-anatomy-1`, 2026-11-24 (night). Branch `e4-anatomy-1`, PR #168. Research only: fake
money, files already in the data cache (read-only), no change to the gym, the daily runner or
the live strategies. Train data only: pooled-1's and pooled-2's loaders stop at 2025-10-31.
A **descriptive re-score** of finished tries (pooled-1 #142, pooled-2 #159) on their own series
and rule code: no new rule, `e4` not retuned, nothing selected, not a new test of `e4`. Card
(pushed before any number, not amended): `cards/e4-anatomy-1.md`. Tables:
`results/e4-anatomy-1.md` (+ `.json`). Code: `lib/e4anatomy.py`, `lib/e4anatomy_core.py`;
tests `tests/test_e4anatomy.py`.

## The answer on one screen

**`e4`'s lead is the year after a market's low. Its faster legs buy back earlier than
`tsmom12`, which waits for the 12-month return to turn positive. Against `tsmom12` scaled down
to `e4`'s volatility (post hoc), the rebound gives +0.117 Sharpe a market on stocks (about 3 SE),
more than the whole lead of +0.063. It is positive on 39 of the 41 stock markets. `e4` gives part
of it back in slow bear markets (-0.037: it buys bear-market rallies) and in calm markets
(-0.043: it trims on dips). Fast crashes add little (+0.009); they are 1% of the time. Whipsaw
spells add a bit (+0.017). By leg, the 1-month signal does most of the early buying back and
most of the calm-market damage; the 6-month leg costs least.**

**The gap between stocks and other markets is not regime mix. By the card's rule (reading B)
it is the risk part: +0.052 of the +0.053 gap. The return parts are equal (-0.024 against
-0.025). `e4`'s part positions cut volatility by 12-15% in every class. That is worth more
Sharpe where `tsmom12` itself earns more per unit of risk: stocks 0.48, bonds and currencies
0.29.** With rebound falls scaled to each series' volatility, bonds and currencies gain about
as much in rebounds as stocks (+0.088 against +0.108, post hoc). They lose it again in calm
markets and slow bears.

Units: Sharpe points per market, `e4` minus `tsmom12`, equal-weight means over series, adding
up exactly to pooled-1's and pooled-2's D. The reproduction check passes: per-series d matches
pooled-2's to 5.6e-16. SE: joint 12-month block bootstrap with sigmas fixed (a description of
calendar sensitivity, not a test).

### Card split (reading A: insure-1's 25% zigzag; whipsaw = `tsmom12` flips twice within +-13 weeks)

D = risk part + return part; the return part is the sum of the regimes.

| Pool | D | Risk part | Return part | Fast crash | Slow bear | Rebound | Whipsaw | Calm |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Equity 41 | +0.063 | +0.087 | -0.024 | +0.022 | +0.003 | **+0.092** (SE 0.039) | +0.018 | -0.159 |
| Bonds + FX 21 | +0.010 | +0.035 | -0.025 | 0.000 | -0.020 | +0.028 | +0.036 | -0.069 |
| Commodities 8 | -0.019 | +0.047 | -0.066 | -0.002 | 0.000 | +0.043 | +0.002 | -0.110 |
| Time share, equity | | | | 0.01 | 0.20 | 0.20 | 0.14 | 0.45 |
| Time share, bonds + FX | | | | 0.00 | 0.22 | 0.05 | 0.16 | 0.58 |

### Post hoc: against a volatility-matched `tsmom12` (no risk part; d = sum over regimes)

| Pool | D | Fast crash | Slow bear | Rebound | Whipsaw | Calm |
|---|---:|---:|---:|---:|---:|---:|
| Equity 41 (labels A) | +0.063 | +0.009 | -0.037 | **+0.117** (SE 0.041) | +0.017 | -0.043 |
| Bonds + FX 21 (labels A) | +0.010 | 0.000 | -0.033 | +0.032 | +0.032 | -0.021 |
| Commodities 8 (labels A) | -0.019 | -0.003 | -0.030 | +0.050 | +0.003 | -0.039 |
| Equity 41 (labels B, vol-scaled) | +0.063 | +0.009 | -0.036 | +0.108 | +0.028 | -0.046 |
| Bonds + FX 21 (labels B) | +0.010 | -0.000 | -0.031 | +0.088 | +0.013 | -0.060 |

## Why the post hoc reading was added

In the card's split a pure scale-down (`e4` = 0.85 x `tsmom12`) would show a large positive
risk part and an equal negative return part, although it changes no Sharpe. So the card's
regime columns are measured against a baseline that holds more than `e4`. The calm column
(-0.159 on stocks) is mostly that scale effect, not bad timing. Comparing with `tsmom12`
scaled to `e4`'s own volatility (k = sd_e4 / sd_ts per series) removes it: then
d = sum over periods of (r_e4 - k r_ts) / sd_e4 x sqrt(P), exactly, with no risk part. I saw
this only after the card's run. It is reported apart, labelled post hoc. It changes none of
the card's numbers; both runs are deterministic and give identical card tables.

## Regimes

- **Rebound (the year after a 25% fall's low, capped at the next peak): where the lead is.**
  On stocks `e4` holds +0.17 more than `tsmom12` there (mean position gap). The legs split the
  rebound gain 1m +0.043, 3m +0.031, 6m +0.018. It is positive in every equity group (VA: US
  industries +0.10, developed +0.12, wider +0.15, ETFs +0.09). It is positive on 39 of the
  41 stock markets (A and VA). With volatility-scaled falls (B) it is positive on 40 of 41
  stock markets and on all 21 bond and currency series. The card's rule calls it "carrying"
  on stocks in readings A, B and W. Under insure-3's 15% zigzag (reading C) more time counts as rebound
  (36% instead of 20%) and the term is +0.060 (SE 0.048). This is the fast-reentry trade-off
  that `fast-reentry.md` and insure-1 describe (the cost of trend is the late buy-back). `e4`
  pays part of that cost back. Its faster legs buy back sooner, and it holds only part of a
  position, so the cost of buying a false start is smaller.
- **Slow bear markets (falls longer than 92 days): a cost against the matched twin** (-0.037
  stocks, -0.033 bonds + FX, all readings). The same fast legs buy rallies inside a bear
  market. In the card split this is hidden (+0.003), because `e4` holds less than `tsmom12`
  there anyway.
- **Fast crashes (92 days or less, peak to trough): about nothing.** Stocks +0.022 in the card
  split, +0.009 matched. They are 1% of the time (0% on bonds and currencies at 25%). `e4`
  holds a little less during the fall (-0.13), but a 1987 or 2020 is over before any leg
  moves much.
  So `e4` does not fix trend's known fast-crash weakness (insure-1, insure-3).
- **Whipsaw (`tsmom12` flips at least twice within +-13 weeks): small and positive.** Stocks
  +0.017 to +0.033, bonds + FX +0.011 to +0.036. Part positions soften the flips. With a
  +-26-week window (reading W) the stock term vanishes (-0.007), so it is not robust.
- **Calm (everything else, about half the time): the price.** Against the matched twin stocks
  -0.043, bonds + FX -0.021 (A) or -0.060 (B). The 1-month leg sells on ordinary dips in an
  uptrend.

## Legs

The card split, per leg: (h_L - h_12) / 4 x market return. Matched reading: the same legs plus
a scale term.

| Pool | 1m | 3m | 6m | Extra costs | Scale term (post hoc) | Sum (matched) |
|---|---:|---:|---:|---:|---:|---:|
| Equity 41 | -0.011 | -0.008 | -0.001 | -0.005 | +0.087 | +0.063 |
| Bonds + FX 21 | -0.003 | -0.005 | -0.006 | -0.011 | +0.035 | +0.010 |
| Commodities 8 | -0.019 | -0.015 | -0.019 | -0.013 | +0.047 | -0.019 |

No leg earns more return than the 12-month signal it replaces. Each is slightly negative, and
the 6-month leg is closest to zero on stocks. The lead comes from mixing them: four signals
that disagree give a smoother, smaller position (sd ratio `tsmom12` / `e4` 1.18 on stocks,
1.13 on bonds + FX). The return given up is less than what the lower risk buys. By regime the
1-month leg is the most extreme: the largest rebound gain (+0.043) and the largest calm loss
(-0.072). `e4` trades about twice as much. Its extra costs take 0.005 a market on stocks
and 0.011-0.013 elsewhere (pooled-2's higher cost assumptions). That is about the size of the
bonds + FX lead itself.

## Is the equity-vs-other gap regime mix?

Gap = D_equity - D_bonds+FX = +0.063 - 0.010 = **+0.053**. Exact split: mix (equity time shares
at bonds+FX rates) + rates + risk part, in both orders:

| Reading | Mix (2 orders) | Rates (2 orders) | Risk part | Card reading |
|---|---|---|---:|---|
| A (25%) | +0.107 / +0.135 | -0.107 / -0.134 | +0.052 | "mix" by the letter, see below |
| **B (vol-scaled, the card's basis)** | -0.029 / -0.003 | +0.030 / +0.004 | **+0.052** (SE 0.021) | **by the risk part** |
| C (15%) | +0.189 / +0.117 | -0.188 / -0.116 | +0.052 | "mix" by the letter |
| W (whipsaw +-26 weeks) | +0.105 / +0.130 | -0.104 / -0.129 | +0.052 | "mix" by the letter |
| VB (post hoc, matched) | +0.004 / +0.040 | +0.049 / +0.013 | 0 | mixed |

- **By the card's rule (applied to reading B), the gap is the risk part.** The return parts are
  the same, -0.024 and -0.025. The risk part is Sharpe(`tsmom12`) x (sd ratio - 1): 0.48 x
  0.18 on stocks against 0.29 x 0.13 on bonds + FX. Most of the difference is `tsmom12`'s own
  higher Sharpe on stocks, which drift up. That is the mechanical lift of part positions that
  pooled-1's drift-only null measured (+0.022 of its D).
- **Under the fixed thresholds (A, C, W) the rule's letter says "mix", but read as a
  measurement artefact.** Bonds and currencies spend only 5% of the time in a 25% rebound, so
  their rebound rate per unit of time is large. Moving the equity time shares onto it creates
  +0.11 of "mix" that the rate term takes back almost exactly (-0.11). The card foresaw this
  and fixed B as the basis.
- **Post hoc (matched, labels B): no single cause.** Mix gives +0.004 or +0.040 depending on
  the order, rates +0.049 or +0.013. Rebounds are about as profitable on bonds and currencies
  as on stocks (+0.088 against +0.108). Stocks keep more of it in calm markets (-0.046 against
  -0.060) and in whipsaw (+0.028 against +0.013).
- Commodities (shown, not judged) are behind stocks by +0.082: mix +0.023 to +0.085 (B and VB, both orders),
  risk part +0.040. Commodity spot spends more time in slow bears (0.32), where `e4` loses
  against the matched twin.

## How sure

- One deterministic re-score on pooled-1's and pooled-2's series and rules. Per-series d
  reproduces pooled-2's to 5.6e-16; pooled D are +0.0629, +0.0100 and -0.0194 as published.
  Tests check that the rules re-run with legs equal pooled-1's and pooled-2's returns
  exactly, that every split adds up, and the zigzag labels on a constructed path.
- The regime SEs come from a joint 12-month block bootstrap with each series' sigmas held at
  full-sample values. They show how much a term moves with the calendar. They do not make
  `e4` significant: D itself is still +0.063 with SE 0.045 on stocks and +0.045 (z 1.43)
  combined, as pooled-1 and pooled-2 found.
- Regimes are labelled with hindsight (the zigzag needs the later recovery to confirm a
  trough). That is fine for a description. A rule cannot use these labels.
- The stock markets share one crash calendar (pooled-1: 41 markets act like a handful). So
  the rebound term is a few dozen distinct post-crash years seen many times, not 41
  independent cases.
- "Whipsaw" is new, defined on the card from `tsmom12`'s own flips. It is the least robust
  term: the stock part vanishes with a 26-week window.
- Disclosure: the post hoc readings (VA, VB) and the table of `tsmom12` Sharpe and sd ratio
  were added to the code after the first run and the code was re-run. The card's tables are
  identical across the runs (deterministic; no card number changed).

## For the live rule

Nothing changes. `tsmom12` stays the rule. `e4` stays "unsettled, leaning positive", and this
lane does not move that. It explains the lean. `e4` is mostly a way to buy back sooner after a
crash, paid for in bear-market rallies and calm dips, plus the mechanical Sharpe lift of
smaller positions on assets that drift up. The first part is the known cost of trend (the late
buy-back, insure-1). Any future rule aimed at it needs its own card and new independent data.
The held-out year stays unspent.

## Logged

`tries.md`: one `note` row (a re-score of pooled-1's and pooled-2's logged tries, not a new
try), as gap-2002-1 did. Bar for scale (BAR.md): z >= 4.70, N 500. Not applicable: no test, no
pick.
