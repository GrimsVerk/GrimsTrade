# Card vix-call-1: does a VIX-call overlay cover the fast crashes trend misses, at a cost below what it adds?

Lane `vix-call-1`, 2026-11-24 (night). Written and pushed before any number is computed.
Two **variants** against `tsmom12` (selectable, train only), plus insure-3's descriptive
insurance measures. Follows insure-3 (`research/insure-3.md`, PR #160) and insure-4 (#165).

## Question

insure-3: `tsmom12` was much cheaper crash insurance than CBOE's PPUT (index puts), but puts won
the fast crashes trend misses (1987, 2020, and the falls where trend stayed in: 1998, 2010, 2011,
2025). insure-4: puts held only while trend is in cost nearly the full put bill (dead). In
insure-3's side table CBOE's VXTH (S&P 500 plus a small sleeve of VIX calls) was the only option
index whose insurance cost came near trend's, and it gained in March 2020 where trend lost.
**Does a VIX-call overlay on top of `tsmom12` cover the fast crashes trend misses, at a cost
below what it adds, and better than the matched-cost alternatives (less equity, or puts)?**

## Prior (stated now)

VXTH's record is carried by one fast crash (2020): VIX calls pay many times their premium in a
spike from a calm level and bleed the rest of the time. Expected: the overlay loses far less
than trend in 2020, a little less in 2010/2011/2025-type falls, and costs a steady drag outside
them. With 2020 in the window it may even beat trend on growth; without 2020 I expect it to be
a net cost. A paired Sharpe z near 4.70 is not expected.

**This card is effectively kill-only.** VXTH starts 2006-03-31, so 1987 is outside its history:
the window holds **one** named fast crash (2020) and a handful of falls of 15% or more where
trend stayed in. No result from so few independent episodes can pass a project bar of
z >= 4.70; the card can kill the overlay (it fails to cover, costs more than it adds, or a
matched-cost alternative covers as well), or leave it "not killed, not shown".

## Data (no new fetch)

insure-3's cache exactly (`research/lib/fetch_insure3.py`, raw files under the git-ignored data
cache `insure-3/raw-2026-11-24/`, read-only): CBOE **VXTH** daily (2006-03-31..), CBOE **PPUT**
(for the matched-cost put alternative), S&P 500 total return (Yahoo `^SP500TR`), bills (Yahoo
`^IRX`). Diagnostic only: CBOE `VIX_History.csv` already in the cache (`cboe/2026-11-12/`), for
the VIX level at each fall's peak. Nothing after **2025-10-31** is parsed (held-out year starts
2025-11-10). CBOE terms: raw levels stay in the cache; only derived statistics are committed,
as insure-3 and insure-4 did. No other CBOE index is fetched or tried.

VXTH's rule (CBOE): the S&P 500 (total return) plus one-month 30-delta VIX calls bought at each
monthly VIX expiration, weight set by the VIX futures level: 0% at 15 or below, 1% above 15 to
30, 0.5% above 30 to 50, 0% above 50. The weights were set with knowledge of 2008 (the index's
history before its publication is a backfill); this is stated, not corrected.

## Window and series (daily closes, VXTH's sessions 2006-03-31..2025-10-31)

Built through `insure3.load()` (the record's `tsmom12`: `trend_tune.paper`, grid (12,), on the S&P
500 total return, decided at Friday's close, applied from the next session, 2 bps a side, idle
cash at bills), restricted to VXTH's window as insure-3's side table does.

- **leg** (the VIX-call overlay, self-financed): leg_i = r_VXTH,i - r_hold,i (VXTH's daily return
  minus the S&P 500 total return's). Since VXTH = (1 - w) index + w calls, this is about
  w x (calls - index): the call sleeve funded by a sliver of the index; it is held at full
  size every session whatever trend's position (when trend is in bills the overlay is about w
  calls and -w index, w <= 1%).
- **V1 `tsmom12+vxleg`** (primary variant): r = r_trend + leg (trend with VXTH's VIX-call sleeve
  on top, at VXTH's own size, every session).
- **V2 `tsmom12-in-vxth`** (second variant, insure-4's shape): VXTH while trend is in, bills
  while out, 2 bps a side on each switch (insure-4's `protected` with VXTH in place of PPUT).
- Robustness (not selectable): **V1@x2** (r_trend + 2 x leg: double the sleeve);
  **V1@cost50** (V1 minus 0.50 points a year, deducted per session, a rough allowance for VIX
  option bid-ask that the index does not carry); **V1@cash0** (trend's idle cash at 0, the gym's
  rule).
- Context: hold (S&P 500 TR), `tsmom12`, VXTH (= hold + leg), PPUT, insure-3's 50/50 trend+PPUT
  mix (monthly rebalance), all on the same window.

## Matched-cost alternatives (insure-3's alternatives, set to V1's cost)

Let c = CAGR(trend) - CAGR(V1) on the window (V1's cost against trend, points a year).
If c <= 0 the overlay costs nothing in growth and the matched alternative is trend itself.
If c > 0:
- **A1 less equity**: trend held at exposure e in (0, 1] (the rest in bills, daily rebalanced:
  r = e x r_trend + (1 - e) x rf), e found by bisection so that CAGR(A1) = CAGR(V1).
- **A2 puts**: insure-3's mix, w x trend + (1 - w) x PPUT (monthly rebalance, `insure3.mix`),
  w found by bisection so that CAGR(A2) = CAGR(V1); if even w = 0 (all PPUT) is not that cheap
  or that dear, w is clipped to [0, 1] and said so.
Both solved on the whole window, once; reported as `control` rows.

## Falls and measures (insure-3's definitions)

- insure-3's zigzag (15% down / 15% up) on hold's daily closes inside the window; per fall each
  series' loss, loss avoided I (log points vs hold), share avoided, net of the next 365 days.
- **Trend-missed falls** (fixed by trend alone, before any overlay number): falls where
  `tsmom12` was in the market at the peak and its share avoided is below 0.5. The named fast
  crash **2020** (trough 2020-02..2020-04) is reported on its own; the <= 92-day cut as well.
- CAGR, Sharpe above bills with SE, worst loss, insurance cost (CAGR gap to hold / mean I per
  fall), insure-1's premium P.
- **Premium against trend**, P_T = -(G - S) / S, where G = total log growth of the series minus
  trend's (log points) and S = sum over all falls of (I_series - I_trend). P_T < 1 means the
  overlay paid back more inside the falls than it cost outside them (equivalently G > 0 when
  S > 0).
- **Leave 2020 out**: G and the Sharpe difference recomputed with the sessions of the 2020 fall
  (peak, trough] dropped from every series.

## Test and bars (fixed now)

- **Paired Sharpe test vs `tsmom12`** (insure-4's code, `insure4.paired_test`): d = Sharpe above
  bills (variant) - Sharpe above bills (`tsmom12`), same sessions; SE from a paired stationary
  block bootstrap of the daily excess returns, mean block 21 sessions, 2,000 draws, seed 0;
  z = d / SE. Side: mean block 63 (reported, not used to choose).
- **Project bar** (`research/register/BAR.md`, rows through 2026-11-24 20:01): 3,855 tries,
  N = 1,083 for a new pick, N_eff 500, **z >= 4.70**, Bonferroni p <= 1.0e-04. Own SE (other
  window and comparator), so the z column applies.

**Kill bars for V1** (any one kills "the VIX-call overlay is insurance worth its cost"):
1. V1 does not lose less than trend in the 2020 fall (fails to cover the one named fast crash).
2. V1's mean loss avoided over the trend-missed falls is not above trend's (no cover where trend
   misses).
3. Paired Sharpe z (V1 - trend) <= -1.645 (worse than `tsmom12`).
4. With 2020 left out, G <= 0 *and* the Sharpe difference d <= 0: the whole benefit rests on one
   crash. Labelled "rests on one crash" (kills the claim that the overlay pays for itself; the
   2020 cover itself stands as a description).
5. Matched cost (only if c > 0): A1 or A2 has a smaller mean loss over the trend-missed falls
   than V1 at the same CAGR (a cheaper way to buy the same cover exists).

**Pass** (a selectable claim, still not paper-tradeable: options are outside the paper broker):
z >= 4.70 and none of kills 1-5. Not expected.
Otherwise: **"not killed, not shown"** (descriptive cover, no claim).
Sharpe verdict labels as insure-4: z >= 4.70 "passes the bar"; 1.645 <= z < 4.70 "better but
not a pick"; |z| < 1.645 "no Sharpe difference shown"; z <= -1.645 "worse than `tsmom12`".
V2 gets the same Sharpe test and the same kills 1-4 (no matched-cost step), reported on its own.

## Rows

`research/tries.md`, idea `vix-call-1`: V1 and V2 `variant`; V1@x2, V1@cost50, V1@cash0
`robustness`; A1, A2 `control`. Sharpe in the file's convention (daily calendar, 365, zero rf).
The baselines (hold, `tsmom12`, VXTH, PPUT, mix) already have insure-3 rows and are not repeated.

## Code

`research/lib/vixcall1.py` (reuses `insure3.py`'s loading and measures and `insure4.py`'s
`protected` and `paired_test`; one run, writes `research/results/vix-call-1.md`),
`tests/test_vixcall1.py`: the overlay adds exactly the leg; V1 with a zero leg is trend; V2 with
VXTH replaced by the index is trend; the matched-cost bisection hits its target CAGR; dropping
sessions of a fall removes them from every series alike; no look-ahead (changing every price
after a decision Friday leaves V1's and V2's returns through the next Friday unchanged).
