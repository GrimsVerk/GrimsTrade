# Multi-signal: do value, carry, XS momentum or low risk rank our six assets beyond `tsmom12`?

Research run multi-signal, 2026-11-19, branch `multi-signal` (from `survey-6`). Card
`cards/multi-signal.md` (eb76f36, before any number), script `lib/multisignal_ic.py` (c8715e2,
before its run), one run (030d250). Table: `results/multi-signal.md`. Descriptive screen only:
no backtest, no pick, no strategy try, held-out year not loaded. **Logged as 12 `screen` rows**
(idea `multi-signal-screen`: 5 signals + `tsmom12` reference, six assets and the four ETFs),
not selectable and not counted as strategy tries.

## In plain words

**No. None of the four style signals carries enough information beyond `tsmom12` to be worth a
card.** Of five signals (value, carry, cross-sectional momentum, low-vol, BAB), none passes the
card's bar and none comes near its size test (partial weekly IC >= 0.10). The only positive
one, cross-sectional momentum, is mostly `tsmom12` again (rank correlation 0.76 with its
signal, 0.90 with the 12-month return), and its extra is +0.035, about a third of the useful
level. Value and carry are noise; the two low-risk signals point the wrong way here.

| Signal (six assets, from 2003-08, ~4.9 assets a week) | IC week (95%) | IC month | Beyond `tsmom12`, week (99.5%) | corr `tsmom12` |
|---|---:|---:|---:|---:|
| value: -5-year return, AMP | -0.018 (-0.055..+0.020) | -0.023 | -0.008 (-0.056..+0.041) | -0.50 |
| carry: yield or -funding above bills, Koijen et al. | -0.023 (-0.055..+0.011) | -0.041 | -0.029 (-0.071..+0.013) | -0.06 |
| XS momentum: 12-1 month return, AMP | **+0.043** (+0.010..+0.077) | +0.039 | **+0.035** (-0.007..+0.080) | +0.76 |
| low-vol: -1-year vol | -0.059 (-0.093..-0.026) | -0.081 | -0.050 (-0.099..-0.001) | +0.11 |
| BAB: -beta to SPY, FP | -0.055 (-0.088..-0.021) | -0.124 | -0.028 (-0.080..+0.023) | -0.26 |
| reference: `tsmom12` / 12-month return | +0.014 / +0.025 | +0.007 / +0.029 | - | - |

- **XS momentum** is the one steady number: positive in all four eras beyond `tsmom12` (+0.071,
  +0.035, +0.002, +0.020), on the four ETFs alone too (+0.052, beyond +0.035), and outside both
  placebos (shuffled labels: chance 0.030; fixed relabels p 0.04). But it fails the 99.5%
  interval and the size test. What it adds is how strong each trend is relative to the others,
  not a new kind of information. rl-3's ceiling puts an IC of ~0.035 at about +0.02 Sharpe,
  against the +0.32 (close rule) to +0.59 (far) a new pick needs at N 1,012.
- **Low risk reversed.** The low-vol and low-beta assets (TLT, GLD) did *worse* than the risky
  ones week to week (raw IC -0.06), and on the risk-adjusted target low-vol is flat (-0.008)
  and BAB still negative (-0.044 week, -0.107 month). FP's premise (low beta earns more per
  unit of risk) does not hold across these six. Fixed relabels of the assets reach the same
  size often (placebo B p 0.07-0.19), so this is mostly the assets' average ordering (coins and
  QQQ earned most), not a signal.
- **Value and carry** sit inside the shuffled-label chance level (0.036, 0.033) and flip sign
  across eras. Carry's coin leg exists only from 2020 (Binance funding; BitMEX refused).
- **How sure.** Sure that nothing reaches 0.10: the intervals end at +0.08 at the most. Not sure
  about the small signs: about 4-5 assets a week means a single week's IC has SE ~0.45, and
  the scores move slowly, so there are far fewer independent bets than the 1,162 weeks suggest.

## Why breadth decides it

AMP, Koijen et al. and FP rank 10-40 markets inside each asset class and go long-short; the
live family that paid (survey-6's style-premia funds, Sharpe 0.50) does the same across
hundreds of instruments. Here a week's cross-section is SPY, QQQ, TLT, GLD and, from 2013, two
coins: four classes, one or two members each, so no signal can be ranked within a class. The
fundamental law (IR ~ IC x sqrt(independent bets)) with IC 0.035 and a handful of slowly
changing bets gives nothing a long-only, no-coin-short book can collect.

## Worth a card later?

**No**, by the card's bar (all four needed: beyond-`tsmom12` IC > 0 at 99.5% and the same sign
at a month; outside both placebos; same sign on the ETFs and in 3 of 4 eras; size >= 0.10). XS
momentum passes 2 and 3 only. Project-wide bar any later rule would face (register-1,
`BAR.md`, 2026-11-18 22:34): **2,904 tries, N 1,012, Bonferroni p <= 4.9e-5**. The only route
to these premia is breadth (survey-6's live long-short funds, or a wide book), which is an
owner risk-map question, not a test on the six.

## Assumptions (noted, not tuned)

- Value uses AMP's commodity measure for every asset (BE/ME is not keyless; AMP call the
  -5-year return close to their bond measure and to BE/ME); it needs 5.5 years of bars, so it
  ranks three assets only from 2008. Equity carry is the trailing (not futures-implied) dividend
  yield; TLT carry leaves out roll-down; gold's lease rate is taken as 0. BAB uses SPY as the
  market. Scores are divided by 1-year vol, since there is no within-class ranking.
- 1994-2003 has at most two assets a week, so every series starts in 2003 (BAB 2005, value 2008).
