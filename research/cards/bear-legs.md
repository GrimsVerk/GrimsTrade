# bear-legs: multi-leg bear markets, and can a bear-market rally be told from the bottom at the time?

Lane bear-legs, written 2026-11-19, **before any number of this lane was computed** (no rally,
leg, feature or test value on any series). Branch `bear-legs` (from `fast-reentry-2`, PR #96).
Research only, **descriptive, no pick**: no rule is selected, fitted or run as a strategy. Fake
money, files already in the data cache, no change to the gym, the daily runner or the live
strategies. Held-out year untouched: nothing after 2025-10-31 is parsed (insure-1/insure-2
loaders, unchanged).

## Why

insure-1/insure-2: `tsmom12` avoids about half of each 25% fall but buys back late.
fast-reentry/fast-reentry-2: a 3-month re-entry (`or3-12`, `arm3-12`) wins back the rebound
(+8 log pts per US fall) but leaks the insurance (-6 to -7), worst in multi-leg bears (1929-33:
each rally bought, next leg ridden down). The insure and re-entry lines are closed for picks.
Open question, description only: how common are multi-leg bears, what did the signals do at
each rally top, and is there anything observable at the time that separated a bear-market rally
from the real bottom? If something is, it would be the input of a future card, not of this one.

## Data and episodes (insure-1/insure-2, unchanged)

- US: French daily market + 10 industries (value-weighted), 1927-07 to 2025-10, 11 series;
  insure-1's 25% / 25% zigzag episodes, market-anchored clusters (50 effective falls).
- Non-US: insure-2's 13 developed price indices (Yahoo, cache `insure-2/raw-2026-11-18/`),
  episodes as above, clusters anchored on the US market's falls (19 effective falls).
- Daily closes. Lookbacks in calendar days as `trend_tune`: 3-month = 91 days, 12-month = 365
  days (last close on or before the date minus the lookback). Signals: log return > 0.

## Step 1: catalogue (hindsight allowed, description)

- **Rally inside a fall:** inside each episode's [peak, trough], a rise of at least 10% from a
  local low (a 10% / 10% zigzag on closes) that is followed by a lower close before the
  episode's trough. Rally size = top / local low - 1; duration = calendar days low -> top.
  **Legs** = rallies + 1. **Multi-leg** = at least one rally. Sensitivity: 15% and 20% rallies.
- **Leg across episodes:** the same series starts a new 25% fall with its peak within 365 days
  of the previous episode's trough (the 25% rally that ended the episode was itself a
  bear-market rally in the wider sense). Reported with whether the new trough is below the old.
- At each rally top (inside a fall): 3-month and 12-month signal on or off; whether the 3-month
  signal turned on during the rally while the 12-month was off (a `or3-12`-type re-entry), and
  whether the 12-month signal turned on (a `tsmom12` re-entry bought into a bear rally).
- Per effective fall: the representative episode (the market's, else the cluster's deepest),
  legs, largest rally (size, days), signals at its tops; and over all member episodes: share
  multi-leg, mean legs. Tie to the closed rules: mean dI of `or3-12` and `arm3-12` against
  `tsmom12` (fast-reentry's paper series, recomputed with their code) per cluster, grouped by the
  representative episode's leg count (0 / 1 / 2+ rallies). Description only.

## Step 2: bear-market rally or bottom, with information at the time (description)

Two real-time event sets, per series, daily closes (each event uses only closes up to its day):

- **A (rally off the low):** while the close is in a confirmed 25% fall (running peak known; the
  lowest close since the peak, L, is at least 25% below it), the first close at least 10% above
  L. The next event needs a new lower L first. Label **bottom** if L is the episode's trough
  (no lower close before the 25% rise that ends the episode), else **bear rally**.
- **B (3-month re-entry moment):** Friday closes in a confirmed 25% fall, before the episode
  ends (close 25% above L), where the 3-month signal is on, was off the Friday before, and the
  12-month signal is off: the moment `or3-12` / `arm3-12` would buy. Same label.

Observables at the event close (fixed now; no other is examined):

1. Prior fall: log(peak / L).
2. Retracement (B only; in A it is a function of 1): log(close / L) / log(peak / L).
3. Fall duration: days peak -> L.
4. Rally speed: days L -> event.
5. Volatility: 21-session realized volatility of daily log returns, annualized.
6. Volatility ratio: 21-session over 252-session realized volatility.
7. 12-month log return (the slow signal's distance from zero).
8. Breadth: share of the set's series (US: the 10 industries; non-US: the 13 indices, those
   with a 3-month return) whose 3-month return is positive, closes on or before the event day.

(3-month return is not on the list: in B it is just above zero by construction.)

Statistic per observable: AUC = probability that a bottom event has a higher value than a bear-
rally event (0.5 = no information), events pooled over series. Reported with:

- **Honest sample sizes:** events, bottoms, bear rallies, and effective falls they come from.
- **Cluster bootstrap** (10,000 draws over the effective falls, insure-1's seed): 90% range of
  the AUC and two-sided p (twice the smaller share of draws on one side of 0.5).
- **Placebo (the permutation check):** 500 stationary-block-bootstrap histories of each set
  (daily log returns resampled in blocks of mean length 21 sessions, the same block draws for
  all series of a set on a common calendar, so cross-series correlation and short-run volatility
  clustering are kept but any longer-run path structure is broken), seed 0; events, labels and
  observables recomputed identically. Placebo p = share of placebo AUCs at least as far from 0.5
  as the real one. Also the placebo's share of A events that are bottoms (a driftless random walk
  gives about 0.43: from L x 1.10 the 25% barrier is log(1.25/1.10) up against log(1.10) down).
- A observable is **"distinguishes, in sample"** only if, on the US set A (decides), bootstrap
  p < 0.05 and placebo p < 0.05, and the AUC is on the same side of 0.5 on the non-US set A.
  Otherwise "not shown". The label is description; no threshold or rule is fitted or run.

Looks: 8 observables x 2 event sets x 2 regions (31 AUCs, retracement in B only); US set A is
the one stated in advance as deciding. A future card on any observable must count these 31 looks.

## Logging

**Not at all** (no `tries.md` row): nothing here is a strategy return series or a selectable
configuration; the insure convention (`insure-check`) re-scores an already logged rule's Sharpe
on new data, and no Sharpe is computed here. The 31 looks are recorded in this card and the
write-up instead.

## Bar (for any future card that takes an observable from here)

Project-wide (register-1, `research/register/BAR.md`, at 2026-11-18 22:34 UTC): 2,904 tries,
**N 1,012 for a new pick, Bonferroni p <= 4.9e-5** (DSR 0.95 needs z >= 4.90 independent).
The insure line is closed for picks (fast-reentry-2); a new card would open a new family and
must say how it differs from the two re-entry rules already tried.

## Outputs

`research/lib/bearlegs.py` (code), `research/results/bear-legs.md` (tables),
`research/bear-legs.md` (one-screen note: what this says about the price of trend insurance,
and whether any observable is worth a future card).
