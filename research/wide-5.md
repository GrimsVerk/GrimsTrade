# Wide 5: dealer backlog and index extension, two structural flows in Treasuries

Research run wide-5, 2026-11-18. Branch `wide-5` (from `wide-4`), draft PR #71. Research only:
fake money, public data, no change to the gym, the daily runner or the live strategies.

(Write-up of steps 1-2 follows once step 3 is done.)

## Step 3. Where does the better of the two gain or lose against `tsmom12`? (fixed before looking)

Written 2026-11-18 after both verdicts, before any breakdown below was computed. The better
pick by its difference to the twin is `extension-dose` (`ext-high` +0.013, p 0.19; `backlog`
-0.026). Nothing is tuned: the same rule, placebo and twin as on the card, rerun without
`tries.md` rows (the configurations are already logged). Script `lib/wide5_deeper.py`.

Questions:

1. **By year** (2003-2025, TLT's full years): the return of `ext-high` minus that of
   `tsmom12`, and of `ext-low` minus `tsmom12`, in percentage points.
2. **Inside the windows or not**: the same yearly difference split into the days on which
   `ext-high` holds the extra TLT weight and all other days (outside the windows the two
   should only differ by trading costs).
3. **By regime**: TLT's excess over the last four sessions (the card's event-study number) in
   high minus low months, split by (a) bond bull and bear years (TLT's calendar-year return
   above or below zero), (b) 2003-2013 against 2014-2025, (c) months whose `tsmom12` book had
   at least a quarter idle against less (where the overlay is large or small).

Reading, fixed now: the gain is **consistent with the mechanism** only if the high-minus-low
excess is positive in both bull and bear bond years (index buying is a flow, not a bet on
direction) and not smaller after 2014 than before (passive bond assets grew several-fold).
If it lives only in bull years, it is TLT's drift; if only before 2014, it has faded or was
luck.
