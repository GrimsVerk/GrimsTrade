# Card: calm-drag-1 (what the calm-market drag of `tsmom12` is made of)

Lane `calm-drag-1`, 2026-11-25 (night, UTC). Descriptive re-score of finished tries with their
own loaders and paper series: no new rule, no tuning, nothing selectable. Written and pushed
before any number of this lane is computed.

## Question

gap-2002-1 (#162) split `tsmom12` minus holding into fall gain I, rebound lag B and calm drag C
(by date) and found C is most of the net cost since 2002 (S&P 500 TR -1.65, French US market
-2.16, mean of 10 industries -1.85 log points a year, cash 0). Nobody has split C itself:
gap-2002-1, rev-costloss-1, e4-anatomy-1, reentry-reconcile-1 and lagcost-1 were checked
(e4-anatomy-1 and reentry-reconcile-1 split `e4` minus `tsmom12`, not `tsmom12` minus holding;
eu-4 counted whipsaw orders and fees on a different, EUR-listed book). What is C made of, per
asset: trading costs, time out at a cash rate below the asset's calm return, badly timed calm
exits (out, then back in higher), the late buy-back after shallow dips that never became
falls, or calm days still out after a real fall's rebound year?

## Data (all already in the cache; no download)

- The six live assets (SPY, QQQ, GLD, TLT, BTC-USD, ETH-USD): adjusted train bars, the paper
  series `trend_tune.paper` (Friday decisions, gym costs one way: ETFs 2 bps; coins the gym's
  crypto cost), positions recovered and checked exactly as rev-costloss-1's `six()`. Window:
  each asset's first eligible session to 2025-10-31.
- French daily US market (1927-07-02 .. 2025-10-31) and the 10 value-weighted industries,
  insure-1's paper series exactly as gap-2002-1's `french()`.
- S&P 500 total return, insure-3's series (`insure3.load()`, 1986-07-01 .. 2025-10-31).
- Bills: French RF for the French series, `^IRX` (insure-3's `bill_returns`, per calendar
  day) for the S&P and the six assets.

Rows of the main table: the six assets (own window), French US market (1927-2025 full, and
the eras 1927-1961, 1962-2001, 2002-2025), S&P 500 TR (1986-2025 and 2002-2025), and the mean
of the 10 industries 2002-2025 (side row). Both cash conventions: 0 (the gym's) and bills (the
paper broker's idle cash); cash 0 is primary.

## Definitions (fixed now)

**Calm.** Exactly gap-2002-1's labels: on each series' own total-return index over its whole
loaded history, zigzag 25% down / 25% up; fall = sessions (peak, trough]; rebound = (trough,
the earlier of trough + 365 days and the next peak]; calm = every other session. Windows count
returns of eligible sessions dated in the window; Y = window days / 365.25.

**Per session t**, in log points (x 100): h_t = ln(1 + r_hold), rule return r_t = pos_t bar_t -
c flip_t + (1 - pos_t) rf_t (rf = 0 at cash 0), d_t = ln(1 + r_t) - h_t. C = sum over calm
window sessions of d_t / Y (reproduces gap-2002-1's C on its rows: a check, a mismatch above
0.01 is reported, not fixed).

**Exact additive split of C** (every calm session is in exactly one cell; the parts sum to C):

1. **Cost K** = sum over calm sessions of ln(1 + r_t) - ln(1 + r_t + c flip_t): the trading
   cost on calm flip sessions (entries and exits).
2. **Out O** = sum over calm sessions with pos_t = 0 of ln(1 + rf_t) - h_t: the asset's calm
   return missed while out, net of the cash earned. On sessions with pos = 1 the rest of d_t
   is 0 (checked: residual below 1e-9).

O is split two ways, each exact:

**(i) Premium against timing.** x_t = h_t - ln(1 + rf_t), m = mean of x_t over all calm
window sessions (in or out), n = number of calm out-sessions. **Premium P** = -n m / Y: what
the same number of calm out-sessions at random calm dates would cost on average (candidate
(b): time in cash at a cash rate below the asset's calm return). **Timing T** = O - P = -sum
over calm out-sessions of (x_t - m) / Y: negative when the calm exits sat out better-than-
average calm sessions (whipsaw, candidate (a)), positive when they sat out worse ones.

**(ii) By out-spell.** An out-spell is a maximal run of eligible sessions with pos = 0 on the
full series (not clipped to the window; only its window sessions are counted).
- **Edge spells** touch at least one fall or rebound session. Their calm sessions split into
  **E-pre** (calm sessions before the spell's first fall or rebound session: out before the
  25% fall's peak) and **E-post** (calm sessions after its last one: still out after the
  rebound year, i.e. the late buy-back after a real fall spilling into calm).
- **Calm-only spells** (every session calm: dips that never became 25% falls). Each one's
  contribution -X_L, with X_j the cumulative x over its first j window sessions (X_0 = 0) and
  j* the argmin of X_j over j = 0..L, splits exactly into **dip gain G** = -X_{j*} >= 0 (from
  exit to the spell's low: avoided) and **lag loss L** = -(X_L - X_{j*}) <= 0 (from the low to
  re-entry: missed; candidate (d)). Also shown, by outcome (hindsight, descriptive): calm-only
  spells that re-entered above their exit level (X_L > 0, **whipsaw losses W-**) and the rest
  (**saved dips W+**); and by length: at most 13 weeks (91 calendar days, first to last out
  session; e4-anatomy-1's whipsaw horizon) and longer.

So C = K + O, O = P + T = E-pre + E-post + G + L = E-pre + E-post + W- + W+.

**Also shown per row:** share of calm sessions out, calm-only spells a year, median length,
calm flips a year.

## Statistic, pass/kill rule

None: a description. No rule is compared, no variant is selectable, nothing is picked. The
closing question ("which part could a future rule plausibly reduce without giving up the crash
insurance") is answered in words from the table, and any rule it suggests would need its own
card, its own family bar and the project bar.

**Expectation, stated so it can be wrong.** On the stock series P is the largest part of O (the
rule is out a small share of calm time but the calm equity premium is high); T is negative
(calm exits come near dip lows, re-entries above the exit); L outweighs G in calm-only spells;
K is small for ETFs (2 bps) and larger for coins; E-post is not negligible on the stock series
(slow buy-backs after 2001-2002 and 2008 carry into calm).

## Bar (for scale only)

Quoted from `research/register/BAR.md` (rows through 2026-11-25 01:16): 4,126 distinct tries,
N for a new pick 1,116 (z >= 4.93 independent; measured rho 0.55: N 506, z >= 4.70; Bonferroni
p <= 4.5e-05). Not applicable: no test, no pick. Family: none (re-score of logged tries).

## Output and rows

- `research/lib/calmdrag1.py` writes `research/results/calm-drag-1.md`; the record is
  `research/calm-drag-1.md`.
- `tries.md`: one `note` row per main-table series (six assets, French US market, S&P 500 TR);
  the industries side row and the era rows are reported inside the French row.
