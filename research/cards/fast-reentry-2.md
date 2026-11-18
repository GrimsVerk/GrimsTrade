# fast-reentry-2: is `or3-12`'s lower premium timing or exposure, and does a pure re-entry rule keep the insurance?

Lane fast-reentry-2, written 2026-11-18 23:25 UTC, **before any number of this lane was
computed** (no control score of `or3-12`, and no return, position or episode of the new rule on
any series). Branch `fast-reentry-2` (from `fast-reentry`, PR #94). Research only: fake money,
files already in the data cache, no change to the gym, the daily runner or the live strategies.
Held-out year untouched: nothing after 2025-10-31 is parsed (insure-1/insure-2 loaders,
unchanged).

## Why

fast-reentry (`cards/fast-reentry.md`, results `research/fast-reentry.md`): `or3-12` (hold if
the 12-month OR the 3-month return is positive) won back +8.4 log points of the year after the
low per US fall, but lost 6.9 in the fall itself (share avoided 0.50 -> 0.35, the guard failed),
because it also stays in at 36% of `tsmom12`'s exits (3-month return still positive). Its
premium fell 1.07 -> 0.97 while its mean position rose 73% -> 83%. Two open questions, in the
order of that write-up's next lanes 1 and 2:

- (a) Is that lower premium timing, or just more exposure? Description only.
- (b) A rule that keeps `tsmom12`'s exits and changes only the re-entry: does it keep the
  rebound gain without paying for it in the fall? The one new pick.

## (a) `or3-12` against insure-1's card 2 controls (description, no pick, no rows)

Exactly insure-1's card 2 (`lib/insure1.py`, `control_stats` and the loop in `card2`, reused):
the 11 US series (French market + 10 industries, 1927-2025), card 1's 25% / 25% episodes and
market-anchored clusters, cash at 0, `or3-12`'s paper series (as already logged by
fast-reentry). Controls, both on the same episodes:

- **Fixed exposure:** hold x of each series all the time, x = `or3-12`'s own average position
  on that series (mean about 83%, as fast-reentry reported).
- **Random timing:** `or3-12`'s own position path rotated by a random offset (365 sessions to
  n - 365), same offset for all 11 series, 2 bps per flip, 1,000 rotations, insure-1's seed.

Reported: mean cluster share avoided S, mean cluster N, pooled premium P for `or3-12`, its fixed
exposure and its rotations (median, 5th-95th), and p = share of rotations at least as good. The
same table for `tsmom12` (insure-1's numbers, recomputed as a check) and for the new rule of (b)
(description). Reading, insure-1's card 2 wording applied as a label only: "Timing, not just
exposure" if p(S) < 0.05, p(P) < 0.05 and P below fixed exposure's; "Exposure, not timing" if
both p >= 0.10; else "In between". This scores an already logged configuration against
controls: not a pick, no `tries.md` rows, not counted in the family.

## (b) The one rule (fixed now; no other variant is run)

**`arm3-12`: exit exactly as `tsmom12`; after an exit, re-enter when the 3-month return turns
positive, even if the 12-month return is still negative; otherwise as `tsmom12`.** Same paper
mechanics as `tsmom12` and `or3-12` in fast-reentry (trend-tune's `paper`: Friday decisions on
closes visible at the decision, applied from the next session; 2 bps a side; cash at 0). Signals
as fast-reentry: slow = 12-month (365-day) log return > 0; fast = 3-month (91-day) log return >
0, off with less than 91 days of history (`trend_tune.signal`).

State per series at each Friday decision: the position and a flag `armed`.

1. Not eligible: cash, `armed` off.
2. Slow on: hold (as `tsmom12`), `armed` off.
3. Slow off and the rule is holding on a re-entry (held last week while slow was off): hold
   while fast is on, cash when it turns off.
4. Slow off otherwise (this is `tsmom12`'s exit week, or the rule is in cash): hold only if
   `armed` and fast is on; else cash.
5. After 3-4: if fast is off, `armed` on.

So at `tsmom12`'s exit the rule always leaves (unlike `or3-12`); it re-enters only once the
3-month return has been non-positive at a decision since the exit and is then positive again
("turns positive"). If the 3-month return is already non-positive at the exit, the re-entry is
`or3-12`'s. While re-entered with slow off it leaves when fast turns off (as `or3-12`); when
slow turns on it is `tsmom12` again. A rally that is under way at the exit does not count: the
rule waits for the next dip and recovery.

### Mechanism

- As fast-reentry's card: multi-horizon trend (Hurst, Ooi and Pedersen 2017, Journal of
  Portfolio Management 44(1)); slow-bearish / fast-bullish "Rebound" state (Goulding, Harvey and
  Mazzoleni 2023, Journal of Financial Economics 149(3)). This rule takes the Rebound-state
  re-entry and drops the slower exit, which fast-reentry found was where the insurance leaked.
- **Why it may fail.** Bear-market rallies (1930-32, 2000-03, 2008): the re-entry still buys
  them and rides the next leg down, which was most of `or3-12`'s largest losses (1929-1933,
  1992). Waiting for a dip-and-recovery after the exit may also miss V-shaped rebounds where the
  3-month return never turns non-positive after the exit.

## Data, episodes, metrics, tests (fast-reentry's card, unchanged)

US (decides): market + 10 industries, 1927-07-02 .. 2025-10-31, 50 effective falls. Non-US
(decides, direction): 13 developed price indices, 19 effective falls anchored on the US market's.
Description: 3 French total-return regions; eras; speed buckets. Comparator: `tsmom12`'s paper
series (replay checked equal to trend-tune's `paper`). Both rules scored on the same episodes.
Per episode `I`, `B`, `N = I + B`, `S`; calm `C`; pooled premium `P = -(sum B + C) / sum I`;
`dN` = `N(arm3-12)` - `N(tsmom12)` averaged within each effective fall (same for dI, dB, dS).
Sign test and cluster bootstrap over effective falls (10,000 draws, seed 0, one-sided, H1: mean
`dN` > 0).

## Pass rule (fixed now; family bar p < 0.025)

| Verdict | When |
|---|---|
| **Keeps more of the insurance** | US: mean cluster `dN` > 0 with sign-test p < 0.025 **and** bootstrap p < 0.025; non-US: mean cluster `dN` > 0; full-period premium `P(arm3-12)` < `P(tsmom12)` on both the US 11 and the 13 developed; and the insurance kept (guard): US mean cluster `S` at least `S(tsmom12)` - 0.10 |
| **Gives back more (no help)** | US mean cluster `dN` <= 0, or US `P(arm3-12)` >= `P(tsmom12)` |
| **In between** | otherwise |

Also reported (description): `dI`, `dB`, `dN` by speed bucket and era, premium by era, rule
minus holding per series-year, mean position, worst loss, flips a year; how many of `tsmom12`'s
exits had a positive 3-month return (where `arm3-12` and `or3-12` differ); `arm3-12` against
`or3-12` directly (mean cluster dN, description only).

## Bar and rows

- **Family count: the second pick in the insure line** (`or3-12` was the first; insure-1/2
  selected nothing): family bar p < 0.025 (Bonferroni over 2 picks), in the pass rule above.
- **Project-wide bar** (`git show origin/register-2:research/register/BAR.md`, rows through
  2026-11-18 23:04, register-2 PR #92): 3,023 distinct tries, N 1,027 for a new pick, **N 433
  effective trials (measured rho 0.58); Bonferroni p <= 1.2e-4**, DSR 0.95 needs z >= 4.65 (a
  Sharpe edge over `tsmom12` of +0.30 for a close rule on the primary test). The write-up says
  whether the US `dN` p-values would clear it. No live change can come out of this lane: that
  would need the six-asset primary test at that bar.
- `tries.md`: idea `fast-reentry` (same family); one `variant` row `arm3-12@insure-Mkt`, 26
  `robustness` rows (`arm3-12@insure-<ind>` for the 10 industries,
  `arm3-12@insure-geo-<series>` for the 13 developed indices and 3 regions). Part (a) adds none.

## What each answer means, and the line

- **Keeps more:** the late buy-back, not the exit, is what makes `tsmom12`'s insurance
  expensive; next the held-out year and the six-asset gym run against the project-wide bar.
- **Gives back more** or **In between:** two pre-registered re-entry rules have not beaten
  `tsmom12` net of the rebound; the late buy-back is the price of the insurance. **Close the
  fast-reentry line** (no third re-entry pick); the insure line's standing answer (premium about
  1.3-1.5 since 2002, cheaper than holding less) stands.
