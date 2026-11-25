# bear-legs: multi-leg bear markets and the price of trend insurance

Lane bear-legs, 2026-11-19 (night). Branch `bear-legs` (from `fast-reentry-2`), draft PR #103.
Descriptive, **no pick**. Card `cards/bear-legs.md` (pushed before any number), code
`lib/bearlegs.py` (one run, 30 s), tables `results/bear-legs.md`. Held-out year untouched.
**Logging: not at all** (no `tries.md` row; no strategy series or Sharpe is computed, so the
insure convention does not apply). 30 AUCs were looked at; a later card on any of them counts them.

## The answer on one screen

**Most 25% falls come in legs, and at the time a bear-market rally looks like the bottom.**
None of seven observables told the two apart better than chance (US AUC 0.47-0.54).
So the late buy-back is the price of the insurance, not a fixable flaw.

1. **Multi-leg is the rule.** 200 of 270 US episodes (74%) hold at least one 10% rally before
   the low (118 at 15%, 47 at 20%); 79 of 109 non-US (72%). Median rally 14% over 26 days, then
   a median 28% further fall to the trough. And 117 times a US series started a new 25% fall
   within a year of a 25% low (79 went below the old low): the 25%+ rally that "ended" a fall was
   itself a bear rally.
2. **The 3-month rules buy the rallies, `tsmom12` does not.** At US rally tops the 3-month signal
   was on in 52%, the 12-month in 32%. Out at the low and in during the rally: `or3-12` 25% of
   rallies, `arm3-12` 26%, `tsmom12` 9%.
3. **That is where the insurance leaks.** In single-leg first falls the 3-month re-entry cost
   nothing (dI -0.1, 41 episodes). With 10% rallies inside -5.2. In follow-on legs -8.1 (no rally
   inside) and -12.4 (rallies inside). 88% of `or3-12`'s summed US leak is in falls with 10%
   rallies (non-US 96%), 69% in follow-on legs (non-US 41%).
4. **At the time, the bottom does not look different** (US set A: a close 10% off the lowest
   close inside a confirmed 25% fall, 482 events, 267 bottoms, 50 effective falls). Prior fall,
   fall duration, rally speed, 21-day volatility, volatility ratio, 12-month return and breadth
   across industries: AUC 0.47-0.54. Cluster-bootstrap p 0.17-0.97, block-bootstrap placebo
   p 0.45-0.99. Non-US (211 events, 19 falls) is the same (AUC 0.45-0.57). By the card:
   **"not shown" for all seven.**
5. **Bear rallies are a little more common than chance.** 55% of US 10% rallies are the bottom,
   against 62% in the placebo (5-95%: 0.55-0.69). Non-US: 52% against 58%. Falls continue
   slightly more than a market without memory beyond a month would give. That persistence is
   what trend insurance harvests, and the same persistence makes an early re-entry leaky.
6. **At the 3-month re-entry moment** (set B, description): only fall duration passed both
   tests on US (AUC 0.62, p 0.047 / 0.036), and it failed outside the US (0.53). The 12-month
   return's distance from zero gave AUC 0.62 (bootstrap 0.009), but the placebo already gives
   0.55 (placebo p 0.062), and non-US gave 0.57 (p 0.084). Retracement (0.61) is less than its
   mechanical placebo value (0.66). Two p values below 0.05 in 30 looks is what chance gives
   (about 1.5).

## What it says about the price of trend insurance

`tsmom12`'s slowness is the insurance: it bought into 9% of bear rallies, the 3-month rules 25-26%.
Any re-entry fast enough to catch the rebound also catches the rallies. Nothing observed at the
time picks out which rally is the last one. So on these data the trade of insurance for rebound
(dI about -6, dB about +8 per US fall) is structural, and the premium of about 1.3-1.5 since
2002 (insure-1/2) is a fair price, not a leak to engineer away. Nothing changes for the live rule.

## Is any observable worth a future card?

**No.** None passes the card's own description label on the deciding set. The set B hits are
within multiple-testing noise and do not replicate outside the US. One more split, done after the
card, is weak: the follow-on flag (this fall began within a year of a 25% low), known when a fall
starts. US: `or3-12` minus `tsmom12` gives dN +4.5 in first legs and -2.4 in follow-on legs. But
non-US gives +3.9 and +4.0, it is post hoc, and it would be a third re-entry pick in a line
closed at two. A card on any observable would face the **project-wide bar (register-1,
`BAR.md`): 2,904 tries, N 1,012 for a new pick, Bonferroni p <= 4.9e-5** (DSR 0.95: z >= 4.90).
It would also have to count these 30 looks. An AUC of 0.62 over about 40 falls is two to three
orders of magnitude short of that bar.

## Next lanes (not started)

1. None for the insure or re-entry line: it stays closed.
2. If anyone revisits trend insurance: the same catalogue on total-return non-US country series
   (the price indices here flatter the level, not the comparison).

2026-11-25 (eng-nits-1, #218): `insure1.score` now sets rounding-sized I and B (below 1e-9 log points) to 0; `results/bear-legs.md` was regenerated and only three printed signs of zero changed (-0 / +0). No number or conclusion changed.
