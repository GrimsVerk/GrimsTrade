# omori-1: an Omori "aftershock clock" for `tsmom12`'s buy-back

Lane omori-1, 2026-11-25 UTC (night lane of the WIDER line, seismology). Branch `omori-1`
(from `main`). Research only. **Not run: killed in step 1 as a tested record in other words.**
No card, no numbers computed, no data read; the held-out year is untouched.

## The idea

After a crash the rate of large moves decays like aftershocks, n(t) ~ K / (t + c)^p (Lillo and
Mantegna 2003, Phys Rev E 68, 016119; Weber et al. 2007, Phys Rev E 76, 016109; Petersen et al.
2010, Phys Rev E 82, 036114). Proposed rule: exit as `tsmom12`; after the peak, fit K, c, p each
Friday on the large-move counts so far (|daily return| above a threshold) and buy back when the
fitted expected rate of further large moves falls below a fixed fraction of the pre-crash rate.
Hope: earlier than `tsmom12`, but only once the shock regime has decayed, so the bear-market
rallies are skipped.

## Why it is a record already

1. **The Omori rate is a volatility measure.** The papers count exceedances of a fixed
   threshold, and the rate of |r| > x is a monotone function of the current volatility. Weber
   et al. (2007) tie Omori decay after shocks of every size to the long memory of volatility
   (their title: volatility correlations and Omori processes on all scales). A fit of K / (t + c)^p to the counts since the peak, read at "now", is a
   parametric smoother of recent large-move frequency plus the time since the shock. The rule
   "rate below f times the pre-crash rate" is therefore "smoothed volatility ratio below a
   threshold, some time after the shock": a volatility-calm re-entry.
2. **Both of its inputs were tested at the moment that matters.** `bear-legs` (#103) asked
   whether a bear-market rally can be told from the bottom at the time, at a 10% rally off the
   low inside a confirmed 25% fall (US 482 events, 50 effective falls). 21-day volatility, the
   volatility ratio and fall duration were among the seven observables: AUC 0.47-0.54,
   placebo p >= 0.45, non-US the same. Duration alone at the 3-month re-entry moment gave US AUC
   0.62 but 0.53 outside the US. The Omori clock combines exactly these inputs, and a smooth
   function of inputs that carry no signal has no signal to find.
3. **The rule shape is `arm3-12`.** Exit as `tsmom12`, re-enter on a faster signal: the
   re-entry line closed at two picks (`fast-reentry.md`; pooled-1 #142 `arm3-12` +0.015,
   z 0.39, below its random-walk exposure effect). The leak is the buy-back in 1929-33-style
   bear rallies, which are high-volatility themselves.
4. **Its pieces failed on their own.** Self-excitation of crash days (`hawkes-clustering`):
   0.87 against equal weight's 0.88. The plain twin `vol-calm` (volatility below its own
   expanding median, `research/lib/common.py`): 0.74, it misses the rebounds. Financial
   turbulence (#134) died as "a volatility trigger in disguise" against a matched twin.

What the clock adds over a vol-calm re-entry is only the power-law shape of the smoother (and
the extrapolation one step ahead). The control the idea calls for, a re-entry on a matched
volatility ratio, would measure exactly that part; there is no reason in the papers to expect
it to carry information about which rally is the last one (they describe the decay, not the
direction of prices), and Petersen et al. measure it on intraday data over hours, far finer
than a weekly decision. Against the bar (`research/register/BAR.md`, rows through 2026-11-24
23:32: N 1,099, N_eff 504, z >= 4.70, +0.31 Sharpe for a rule close to `tsmom12`) and the
power result (#150), a second-order change to a dead family cannot pass.

## Closest records

`bear-legs` (volatility, volatility ratio, duration at the rally: not shown), `fast-reentry-2`
(`arm3-12`), `vol-calm`, `hawkes-clustering`, `turbulence-1`.

## Logged

One note row in `tries.md` (not run, not selectable), one line in `ideas.md`.
