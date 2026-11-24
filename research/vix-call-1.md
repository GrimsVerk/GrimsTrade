# vix-call-1: a VIX-call overlay on `tsmom12`

Lane vix-call-1, 2026-11-24 (night). Branch `vix-call-1`, PR #167. Research only: fake money,
keyless public data (insure-3's cache, nothing new fetched), no change to the gym, the daily
runner or the live strategies. Card: [`cards/vix-call-1.md`](cards/vix-call-1.md) (pushed
before any number). Tables: [`results/vix-call-1.md`](results/vix-call-1.md). Code:
`lib/vixcall1.py` (reuses `lib/insure3.py` and `lib/insure4.py`), tests
`tests/test_vixcall1.py`. Train data only (nothing after 2025-10-31 parsed).

## The answer on one screen

**A VIX-call overlay covers the fast crashes trend misses (it is the best cover tested so far),
but over 2006-2025 it paid for itself through one crash only. Take out 2020 and it costs about
4 points of growth a year against `tsmom12` (Sharpe d -0.31, z -2.32). By the card: "rests on
one crash" (kill 4), for both forms. Not a pick (z -0.42 against the bar's 4.70).**

The overlay is CBOE VXTH's VIX-call sleeve: VXTH's daily return minus the S&P 500 total return's
(VXTH holds about 1% in one-month 30-delta VIX calls when VIX is 15-30, 0.5% at 30-50, none
otherwise). V1 adds it to `tsmom12` every session; V2 holds VXTH while trend is in and bills
while out (insure-4's shape, VIX calls in place of puts).

| 2006-04..2025-10 | CAGR | Sharpe above bills (SE) | Worst loss | 2020 fall | Mean loss avoided, 6 trend-missed falls | G vs trend, log pts | G without 2020 | Sharpe d vs trend (z) | d without 2020 (z) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Hold S&P 500 TR | 11.0% | 0.55 (0.24) | 55% | -33.8% | 0 | - | - | - | - |
| `tsmom12` (bills) | 9.5% | 0.61 (0.25) | 27% | -19.8% | +6.9 | - | - | - | - |
| VXTH | 10.3% | 0.58 (0.24) | 43% | +27.6% | +15.7 | - | - | - | - |
| **V1: `tsmom12` + VIX-call leg** | **8.2%** | **0.52 (0.24)** | **27%** | **+49.2%** | **+21.9** | **-23.2** | **-85.3** | **-0.09 (-0.42)** | **-0.31 (-2.32)** |
| **V2: VXTH while in, bills out** | **8.1%** | **0.60 (0.25)** | **19%** | **+24.0%** | **+18.3** | **-25.6** | **-69.2** | **-0.01 (-0.04)** | **-0.20 (-2.02)** |
| A1: `tsmom12` at 82% (V1's cost) | 8.2% | 0.61 (0.25) | 22% | -16.4% | +10.2 | -23.2 | -27.4 | 0.00 | 0.00 |
| A2: puts at V1's cost (= PPUT) | 8.3% | 0.54 (0.24) | 42% | -11.8% | +10.6 | -21.4 | -30.9 | -0.07 | -0.13 |

G = total log growth minus `tsmom12`'s. "Without 2020": the 23 sessions of the 2020 fall (peak
2020-02-19 to trough 2020-03-23) dropped from every series. Trend-missed falls (fixed by trend
alone: in at the peak, share avoided below 0.5): 2010, 2011, 2018, 2020, 2022 H1, 2025.

- **Cover: yes, and better than the matched-cost alternatives.** In the six falls trend missed,
  V1 avoided 21.9 log points per fall against trend's 6.9, A1's (less equity at the same growth
  cost) 10.2 and the puts' 10.6. It gained in 2020 (+49% while holding lost 34%), lost 2% in
  2010 (trend -16%), 8% in 2025 (trend -17%), 13% in 2011 (trend -19%). It did not help in the
  slow 2022 bear (-18.5% against trend's -14.4%: no VIX spike, the calls bled). Kills 1, 2, 3 and
  5 do not fire.
- **Cost: below what it adds only because of 2020.** Over the window V1 gave up 23 log points of
  growth against trend (1.3 points of CAGR a year) while gaining 110 inside the falls: premium
  against trend P_T 1.21 (above 1: it cost more outside the falls than it paid inside them, net).
  The 2020 fall alone added +62 log points. Without it G is -85 log points (about -4.4 a year)
  and the Sharpe difference -0.31 (z -2.32). Leaving out any other single fall changes G by
  at most 20 points; leaving out 2020 changes it by 62. That is kill 4: the benefit rests on one
  crash.
- **V2** (calls only while trend is in) is the same story with a smaller bill and a smaller
  payoff: Sharpe 0.60 against trend's 0.61 (z -0.04), worst loss 19% (the smallest here), 2020
  +24%; without 2020, d -0.20 (z -2.02). Also kill 4.
- **Size and cost robustness.** Doubling the sleeve (V1@x2) roughly doubles the bleed: CAGR
  5.4%, Sharpe 0.27, worst loss 44% (the leg's losses in calm years compound against it). A
  0.50-point-a-year allowance for VIX option bid-ask (V1@cost50) takes Sharpe to 0.48; trend's
  cash at 0 (V1@cash0) to 0.50. None is near trend.
- **Matched cost.** V1's growth cost against trend is c = 1.29 points a year. A1 holds trend at
  exposure 0.823 for the same CAGR: Sharpe unchanged (0.61), worst loss 22%, but 2020 -16%. A2
  (trend mixed with PPUT at the same CAGR) cannot get that dear: even all PPUT (w = 0, clipped as
  the card allowed) costs less growth (CAGR 8.31% against V1's 8.21%), so A2 is PPUT alone, and
  still covers the trend-missed falls less than V1.

## How sure

- **One crash.** The window holds one named fast crash (2020) and six trend-missed falls in all,
  of which 2020 is the only one where VIX went from a calm 14 to over 80. The card said this is
  kill-only; it is. The kill is robust in direction: with 2020 left out, every overlay form is
  behind trend by 69-185 log points.
- **Post-hoc check (computed after the run, no row):** the cut of 2020 stops at the trough; the
  calls' fall in value after it is still counted. Extending the cut by 21 / 63 / 126 sessions
  after the trough moves V1's G without 2020 from -85.3 to -85.3 / -84.2 / -81.9: the result
  does not come from where the cut is placed. Also post hoc: the leg's log return was about
  -2.5 points a year while trend was in and +0.7 while trend was out (the 2008 spike came while
  trend was already out of the market).
- **Additive overlay.** V1 adds the leg to trend's daily return (a constant sleeve sized against
  the whole portfolio, held in bills too). Its growth cost (1.3 points a year against trend) is
  larger than VXTH's gap to holding (0.7): adding the leg to trend's returns is not the same as
  holding VXTH in place of the index, and the difference was not decomposed. A real overlay
  would be reset at each monthly VIX expiry rather than held as a daily sleeve; not measured.
- **VXTH is an index, and partly a backfill.** No fees, no bid-ask on the VIX calls (the
  0.50-point robustness is a rough allowance, not a model). Its weight bands (none above VIX 50)
  were set with knowledge of 2008; its launch date was not checked here.
- **Turnover column** in tries.md: 13.63 for A2 adds trend's flips to PPUT's 12 rolls; with
  w = 0 A2 is PPUT alone (12 a year). Not corrected in the written-once row.
- **No look-ahead.** Trend's state is insure-3's `tsmom12` (decided at a Friday's close,
  applied from the next session); the leg is the index's own published return on the same
  session. Tests: a zero leg gives `tsmom12`; V2 with the index in place of VXTH is `tsmom12`
  (also asserted on the real data in the run); changing every level after a decision Friday
  leaves the positions through the next Friday and the returns up to it unchanged.
- **Order of steps.** Card pushed (5d349d1), then script and tests pushed (5ab2acc), then the
  one run (017fc6f). The post-hoc check above was run after and is labelled so.
- **Data and terms.** As insure-3: raw CBOE and Yahoo levels stay in the git-ignored cache; only
  statistics are committed.

## Count and bar

- `tries.md`: 7 rows, idea `vix-call-1`: V1 and V2 `variant`; V1@x2, V1@cost50, V1@cash0
  `robustness`; A1, A2 `control`. Sharpe there in the file's convention (daily calendar, zero
  rate).
- Bar (BAR.md, rows through 2026-11-24 20:01): 3,855 tries, N 1,083 for a new pick, N_eff 500,
  z >= 4.70, Bonferroni p <= 1.0e-04. V1 z -0.42, V2 z -0.04: far from it, and not reachable
  with one fast crash in twenty years.

## For the live rule

Nothing changes (options are outside the paper broker in any case). The record can now say:
VIX calls are the only insurance tested that covers the fast crashes trend misses better than
holding less at the same cost, but in 2006-2025 they paid for themselves only in 2020; outside
that one crash they cost about 4 points of growth a year on top of trend. Buying them is a bet
on the next fast crash from a calm level, not an edge.

## Next (not started)

1. A longer VIX-call history would need VIX option prices before 2006 (VIX options start
   2006-02), so the episode count cannot grow on this kind of data; the only extension is
   forward time. No further tries in this family on VXTH are worth the count.
