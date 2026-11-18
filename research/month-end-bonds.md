# Month-end bonds: a clean test of wide-1's post-hoc pattern

Lane `month-end-bonds`, 2026-11-18, branch `month-end-bonds` (from `wide-1`). Research only:
fake money, public data already in the repo's cache, no change to the gym or the paper system.
Card: `cards/month-end-bonds.md`, pushed before any number. Tables:
`results/month-end-bonds.md`. Four rows in `tries.md` (two variants, two baselines). Each
variant was run once; nothing was rerun. The held-out year was not loaded.

## In plain words

**Not replicated, by the bar written down before the run.** wide-1 found, by looking, that TLT
and IEF earned most of their return in the last four sessions of each month. The same rule on
LQD, a fund wide-1 never looked at alone, shows the pattern in the raw numbers and misses the
bar once costs and LQD's ordinary drift are taken off. TLT's first year, the only new stretch
of time, shows nothing.

| Test | What was measured | Number | Bar | Result |
|---|---|---|---|---|
| LQD 2002-2025, 279 months | Window return at our fills, gross | +22.5 bps a month (t 4.1), up in 67% of months | none | present |
| LQD | The same, minus 4 bps cost and four average sessions | +10.5 bps (t 1.93) | t >= 2.0 | **fails, narrowly** |
| LQD | The same, by half | +12.0 to 2013, +9.1 from 2014 | both positive | passes |
| LQD | Sharpe of the rule against LQD held at a constant 19% | 0.52 against 0.60 (p 0.58) | ahead, p < 0.10 | **fails** |
| LQD | Sharpe of the rule against buy-and-hold LQD | 0.52 against 0.59 | ahead | **fails** |
| TLT first year, 11 months | Window return minus cost and four average sessions | -1.8 bps (t -0.04) | positive | **fails** (and says nothing: 11 months) |

## What it means

1. **About half of the raw number is not an effect.** LQD earns 2 bps on an average session, so
   any four sessions earn 8 bps; a round trip costs 4. Of the +22.5 bps, +10.5 is left, about
   1.3% a year.
2. **The four days are not a better bet than the other days, per unit of risk.** The rule earns
   2.2% a year for being in the market 18% of the time (buy-and-hold: 4.7%), but its Sharpe is
   below both the constant-weight twin and buy-and-hold. It concentrates the risk into days
   that are a little more volatile than average.
3. **LQD is not an independent test anyway.** Its month-end window return moves with TLT's in
   the same months (correlation +0.57). What shows up in LQD is in large part the Treasury
   move wide-1 already saw. That was written on the card before the run.
4. **The only new time says nothing.** TLT's first year: +14.8 bps gross, -1.8 after cost and
   drift, t about zero. LQD's own first year: +28.9 net (t 0.9). Eleven months cannot settle it
   either way; by the card's sign rule the TLT year counts as a contradiction.
5. One thing worth knowing, not a result: in 2022-2025 the rule's Sharpe on LQD was 0.56 while
   buy-and-hold made nothing (-0.02). One era, seen after the fact.

## Verdict (the reading fixed on the card)

"LQD fails bar 1 or 2: not replicated; the lane ends, and the held-out year should not be spent
on it." Bar 1 failed at t 1.93 against 2.0. The miss is narrow, and bars 3 and 4 fail clearly:
even read kindly, the pattern in LQD is real in the raw numbers and too small to trade alone at
our costs. The strong TLT numbers of wide-1 (+39 bps, t 4.3) stay what they were: found by
looking, on the data they were found in.

## Deviations and disclosures

- The card says TLT's first year has 12 months. It has 11 full windows: July 2002 starts one
  session before the month end, and July 2003's window ends after the cut at 2003-07-30.
- What was seen before the card is listed on the card (TLT and IEF from 2003-07-31, the yield
  series, and two earlier tests that contained LQD inside a wider window or a two-fund leg).
- Price bars are the repo's research cache as wide-1 used it (dividend-adjusted, copied from
  that worktree's git-ignored cache; nothing downloaded, nothing committed).
- The book version of the idea (idle `tsmom12` cash into TLT for four sessions) was not run: on
  the six assets it would be a test on the data the pattern came from.

## For the owner

- Nothing to change in the paper system.
- Recommendation: do not spend the held-out year on this. The card's own rule says so, and one
  year (12 windows) could not confirm a 10-40 bps monthly effect in any case.
- If the pattern is ever wanted again, the honest test is forward paper on TLT (free, slow), or
  a futures book where 10 bps a month matters; neither is started here.

## Reproduce

    uv run --with numpy python research/lib/idea_month_end_bonds.py

Needs `research/data/{bars,adj}/{LQD,TLT}.csv` (`research/lib/fetch.py`). The run appends to
`tries.md`; `RESCORE=1` reruns without logging. Test: `tests/test_monthend.py`.
