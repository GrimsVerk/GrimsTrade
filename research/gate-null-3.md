# gate-null-3: would gate-null-2's proposed surrogate rule have blocked the three passes?

Card: [`cards/gate-null-3.md`](cards/gate-null-3.md) (pushed before any number). Descriptive
retro-check, no new data, no new gate, no new verdict, **no adoption decision** (that is for
the lead and the owner). Code: `research/lib/gatenull3.py` (one number the records lacked:
W36's dose acf1), tests in `tests/test_gatenull3.py`.

**The rule checked** (gate-null-2, #207, proposed): for a gate whose dose has lag-1 acf >= 0.8
at the gate's own step, a pass must also rank <= 2 of 41 among 40 phase-randomised surrogates
(IAAFT for skewed or end-mismatched doses), on top of the shifted calendars.

## Result

| Pass | Dose acf1 | Rule applies | Surrogate rank (of 41) | Under the rule | Replication |
|---|---|---|---|---|---|
| W32 `drought-inflation` | 0.94 | yes | 1 phase / 1 IAAFT | **still a pass** | R32 failed |
| W36 `grid-load-premium` | **0.878** (new, below) | yes | **3** phase (seed 22) | **blocked** | R36 failed |
| W45 `arms-fear` | 0.935 | yes | 2 IAAFT (gating) / 1 phase | **still a pass** | R45 failed |

Sources: W32, `gate-null-2.md` re-score (rebuilt t -3.71, all three families rank 1).
W36, `results/grid-load-premium.md` cell (g), a shown cell in W36's own card, run at gate time
(true t -2.31; surrogates 19 and 21 at -2.62 and -2.57 sit past it; the surrogates were
drawn on g's full 622-month series, not on the 619 gate rows). W45, `wide-28.md` (its card
pre-registered the rule; |end - start| over the 1 SD switch, so IAAFT gated; 40 phase
surrogates, checked once after the review, rank it 1).

W36's acf1 was not in the records: computed now from the gate's 619 cached rows
(`uv run python -I research/lib/gatenull3.py`): **acf1 0.878, skew -0.40, |end - start| 0.37
SD**. So the rule applies. #207 gives no numeric skew cutoff; reading skew -0.40 as not skewed and
the end gap (0.37 SD on the gate rows, 0.17 on the 622-month series the surrogates used) as
under W45's 1 SD switch, the phase family gates. IAAFT was not drawn for W36: if IAAFT were
judged the right family, W36's outcome under the rule is unknown.

**Failed gates:** the rule only adds a condition to a pass, so it cannot turn a fail into a
pass or change any failed gate's verdict. gate-null-2 re-scored the gates on main (W20-W35,
weather-1/2) under phase, IAAFT and "both": no verdict changes. W43, W44 (and W45) already
gated under the rule.

## Conclusion

Of the three replication-killed kill-only passes, the proposed rule would have blocked **one
(W36)**, so it would have saved **1 of 3 replications** (R36). W32 and W45 rank 1-2 among
surrogates and would still have gone to replication and died there. The rule, where it binds,
moves a rejection earlier; it does not explain most of the false passes: two of three survive
it. This matches gate-null-2's own warning ('Do not expect it to stop passes dying in
replication'), and the replication step stays the decisive one. No adoption decision here.

## Limits

- Three cases; a count of 1 of 3 says little about the rule's general rate.
- W36's surrogate rank is one draw of 40 (seed 22); rank 3 vs 2 is a narrow margin, and another
  seed could have ranked it 2. Not redrawn: the stored gate-time rank is the answer the rule
  would have used.
- The surrogate family for W36 rests on a judgement call: #207 gives no numeric skew cutoff,
  and phase was chosen by reading skew -0.40 as not skewed and the end gap (0.37 SD on the
  gate rows, 0.17 on the 622-month series) as under W45's 1 SD switch. IAAFT was not drawn;
  if IAAFT were judged the right family, W36's outcome under the rule is unknown.
- W45 was gated under the rule already, so it is not a retro-check in the same sense as W32 and
  W36.
