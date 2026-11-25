# e4-anatomy-1: where does `e4`'s lead over `tsmom12` come from?

Lane `e4-anatomy-1`, written 2026-11-24 **before any number of this card is computed** (no
decomposition below has been run on any series; what had been seen: the published tables of
pooled-1 (#142) and pooled-2 (#159), and the per-group D values in `results/pooled-2.json`).
Research only: fake money, files already in the data cache (read-only), no change to the gym,
the daily runner or the live strategies. Train data only: the loaders of pooled-1 and pooled-2
stop at 2025-10-31; the held-out year is untouched.

## What this is (and is not)

A **descriptive re-score** of finished tries, with their own code and series: no new rule,
`e4` is not retuned, nothing is selected, and it is not a new test of `e4` (the lane queue says:
test it again only on new independent data). The numbers explain the D that pooled-1 and
pooled-2 already reported; they cannot make it significant. Logged as one `note` row in
`tries.md` (as gap-2002-1 did).

## Question

pooled-1: `e4` (position = share of the 30/91/182/365-day returns that are > 0) leads
`tsmom12` by D = +0.063 Sharpe a market on 41 stock markets; pooled-2: +0.010 on 21 bond and
currency series (judged), -0.019 on 8 commodity spot series (shown). **Where does the lead come
from: in which market regime, through which signal leg, and is the equity-vs-other gap a matter
of regime mix (equities spend more time in the regimes where `e4` gains) or of rates (in the
same regime `e4` gains more on equities)?**

## Series and rules (unchanged)

- Equity 41: `pooled1.load_all()`, `pooled1_core` rules (weekly decisions, fill one session
  late, 2 bps a side, cash 0), weekly Sharpe (sqrt 52).
- Non-equity 29: `pooled2.load_nonequity()`, `pooled2.run_specs` costs and lags (weekly
  engine with publication lags on US bonds and 8 currencies; monthly engine on GOV9, FX-EUR,
  PPI and gold), excess over the bill, Sharpe at the series' frequency. Groups and pools as in
  pooled-2: judged = USB3 + GOV9 + FX9 (21), COM8 shown apart.
- Check (must hold, else stop and report): this lane's per-market d reproduces pooled-1's and
  pooled-2's d for every series to 1e-9, so the pools' D are +0.0629 (equity), +0.0100
  (judged), -0.0194 (COM8).

## Decomposition (exact identities, fixed now)

Per series, with weekly (or monthly) returns r_e4, r_ts of the scored span, means mu and
standard deviations sigma at the period frequency, annualised by sqrt(P) (P = 52 or 12):

    d = SR_e4 - SR_ts = (mu_e4 - mu_ts) / sigma_e4 * sqrt(P)          [return part]
                      + mu_ts * (1 / sigma_e4 - 1 / sigma_ts) * sqrt(P) [risk part]

- **Return part by regime:** (mu_e4 - mu_ts) = (1/T) sum over periods of dr_t, so the return
  part splits exactly into one term per regime k: c_k = (1/T) sum_{t in k} dr_t / sigma_e4 *
  sqrt(P). sum_k c_k = return part.
- **Risk part:** `e4` holds part positions, so it is less volatile; with mu_ts > 0 that raises
  its Sharpe even with equal mean return. Reported as one term (not split by regime). Also
  shown: each regime's share of the variance difference (descriptive).
- **By leg:** e4's position is (h_1 + h_3 + h_6 + h_12) / 4 with h_12 = `tsmom12`'s, so before
  costs dr = sum over L in {1, 3, 6} of (h_L - h_12) / 4 x (market return), one term per leg
  ("1-month", "3-month", "6-month" leg, each against the 12-month signal), plus a cost term
  (e4's costs minus `tsmom12`'s). On weekly series the legs are summed from daily returns and a
  compounding residual (weekly compounded dr minus the sum of daily dr) is reported, expected
  ~0. On monthly series the split is exact. Leg x regime table in the same units.
- Pool numbers are equal-weight means over series, so they add up to D exactly.

## Regimes (fixed now; insure-1/insure-2 definitions where they exist)

Labels are put on every session (weekly series) or month (monthly series) of each series' own
traded level (equities: the index or total-return level pooled-1 trades; bonds and currencies:
the excess-return level pooled-2 trades; monthly series: the cumulated monthly excess returns),
over the series' whole loaded history; a scored week takes the label of its last session.

1. **Fall:** zigzag 25% down / 25% up (insure-1 `PRIMARY`, insure-2 step 1): sessions
   (peak, trough].
   - **Fast crash:** trough - peak <= 92 calendar days (insure-1 `FAST`, insure-3 `FAST`).
   - **Slow bear:** trough - peak > 92 days (shown also as medium 93-365 / long > 365, insure-1
     `MEDIUM`).
   - An unfinished fall at the end of the history (peak, no confirmed trough) is calm.
2. **Rebound:** (trough, the earlier of trough + 365 days and the next peak] (insure-1
   `REBOUND`).
3. **Whipsaw (new, no earlier definition):** a session outside falls and rebounds is in a
   whipsaw spell if `tsmom12`'s own position (the 12-month leg) changes at least twice among
   the decisions within 13 weeks on either side of its week (27 Friday decisions; monthly
   series: 3 months on either side, 7 decisions). The idea: 12-month trend unclear, the rule
   flips in and out.
4. **Calm / trending:** everything else.

Priority: fall > rebound > whipsaw > calm, so the five labels cover every period once.

**Readings (all shown; the first is primary):**

- A. Primary: as above (25% / 25%).
- B. Volatility-scaled zigzag: down = up = 1.5 x the series' annualised volatility of its
  level (whole loaded history, log returns of the level at its own frequency); about 25% for
  a stock index at 17% volatility, about 10-15% for bonds and currencies, where 25% falls are
  rare. This is the fairer basis for the mix question, because under A non-equity series have
  almost no "falls" by construction.
- C. insure-3's 15% / 15% zigzag (fixed threshold, more episodes).
- Whipsaw window check: 26 weeks (6 months) on either side instead of 13 (reading A otherwise).

## Mix against rates (the equity-vs-other gap)

For pools g in {equity 41, judged 21} and regime k: S_gk = mean over series of the share of
scored periods in k; C_gk = mean over series of c_k; rate a_gk = C_gk / S_gk (return part per
unit of time share). Then exactly

    D_eq - D_judged = sum_k (S_eq,k - S_ju,k) a_ju,k          [mix: equity time shares at
                                                                non-equity rates]
                    + sum_k S_eq,k (a_eq,k - a_ju,k)            [rates]
                    + (risk part_eq - risk part_ju)             [risk]

and the reverse order (mix at equity rates) is shown too. **Reading fixed now:** the gap is
"explained by regime mix" if the mix term (both orders) is at least half of the gap under
reading B; "by rates" if the rate term is at least half in both orders; "by the risk part" if
that term is at least half; otherwise "mixed". COM8 is shown the same way, not judged.

## Uncertainty (description, not a test)

SE of each pool-level C_gk and of the mix / rate / risk terms from a joint circular bootstrap of
12-month blocks on one monthly calendar (pooled-2's calendar, 2,000 draws, seed 0), with each
series' sigmas held at their full-sample values (a linearisation: it measures how much the
regime split moves with the calendar, not a test of `e4`). A regime term is called "carrying"
the lead only if it is above 2 SE and above half of the pool's D; otherwise "within noise".

## Expectation, stated so it can be wrong

On equities most of D sits in the risk part and in rebounds after the low (the faster legs buy
back earlier, insure-1/fast-reentry), with fast crashes about zero or negative and whipsaw
positive (the part positions soften the flips); the 3-month and 6-month legs carry more than
the 1-month leg. The equity-vs-other gap is mostly rates and risk part, not mix (bonds and
currencies have little upward drift, so the risk part is small there).

## Output and rows

- `research/lib/e4anatomy.py` writes `results/e4-anatomy-1.md` (+ `.json`): per series, per
  group and per pool: d, return part by regime, risk part, legs, leg x regime, time shares,
  mix / rate / risk split, the four readings, and the reproduction check.
- Tests `tests/test_e4anatomy.py` (offline, synthetic series): the identities add up exactly,
  the leg sum equals e4 minus `tsmom12` before costs, labels cover every period once, the
  regime labels match insure-1's zigzag on a constructed path.
- One `tries.md` row of kind `note`, one `ideas.md` line. Bar for scale (BAR.md): z >= 4.70,
  N 500. Not applicable: no test, no pick.
