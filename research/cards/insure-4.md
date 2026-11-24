# Card insure-4: put protection only while trend is in the market

Lane `insure-4`, 2026-11-24 (night). Written and pushed before any number is computed.
A **variant** against `tsmom12` (selectable, train only), plus the descriptive insurance
measures of insure-3. insure-3's "Next" item 2.

## Question

insure-3 (`research/insure-3.md`, S&P 500 1986-07..2025-10): `tsmom12` was much cheaper crash
insurance than CBOE's PPUT, but the puts won in the fast crashes (1987, 2020) and in the other
falls where trend stayed fully in (1998, 2010, 2011, 2025). Rule here: **when `tsmom12` says
in, hold the S&P 500 as PPUT (index plus a 5% out-of-the-money monthly put) instead of the plain
total return; when it says out, hold bills.** Does it keep trend's cheap slow-bear insurance and
add the puts' fast-crash cover, and at what price?

## Prior (stated now)

PPUT held always cost about 3.1 points of CAGR a year against holding (insure-3). Held only
while invested, the put bill scales with the time in the market; trend is in the market most of
the time (about 70-75% of sessions here), so expect roughly 2 points a year of extra drag, part
of it paid back in the in-market falls. Expected: lower CAGR and Sharpe than `tsmom12`, a smaller
1987 and 2020 loss, a worse insurance cost than trend's. A paired Sharpe z near 4.70 is not
expected; the likely outcome is a negative or insignificant Sharpe difference.

## Data (no new fetch)

insure-3's cache exactly (`research/lib/fetch_insure3.py`, raw files under the gitignored data
cache `insure-3/raw-2026-11-24/`, read-only): CBOE PPUT daily from 1986-06-30; S&P 500 total
return (Yahoo `^SP500TR` from 1988-01-04, before it the cached `^GSPC` price plus Shiller's
monthly dividends); bills from cached Yahoo `^IRX`. Nothing after **2025-10-31** is parsed (the
held-out year starts 2025-11-10). CBOE terms: raw levels stay in the cache; only statistics are
committed, as insure-3 did.

## Rule (fixed now)

- **Position**: `tsmom12` exactly as insure-3 builds it (`trend_tune.paper`, grid (12,), on the
  S&P 500 total return): on each Friday, in if the 365-day log return of the closes up to and
  including that Friday's close is above 0, else out; the position applies from the next session
  through the next Friday. So the in/out state that earns session i's return uses only closes
  before session i (the switch is at the decision day's close).
- **In**: earn PPUT's daily return (from its published index level; the switch into and out of
  PPUT happens at PPUT's closing level on the decision Friday). **Out**: earn bills.
- **Cost**: 2 bps a side on each switch (the gym's ETF cost, as `tsmom12` pays).
- **PPUT's monthly roll**: the index buys a new one-month put 5% below the index on each
  month's third Friday. A switch in on another Friday buys the index as it stands: the S&P 500
  plus the put bought at the last roll, marked at its price; its strike may then be well below
  or above 5% out of the money. A real buyer of that position pays the put's bid-ask, which the
  index does not carry. On a roll Friday the closing level already holds the new put.
- **Robustness** (not selectable): (a) switch cost 10 bps a side (a rough allowance for the
  put's spread when entering or leaving mid-month); (b) idle cash at 0 instead of bills (the
  gym's rule).

## Compared with (insure-3's series, rebuilt in the same run)

hold (S&P 500 TR), `tsmom12` (cash at bills), PPUT alone.

## Measures (insure-3's definitions)

- CAGR; Sharpe above bills (daily, x sqrt(252)) with SE sqrt((1 + SR^2/2)/years); worst loss.
- Loss in each 15% fall (insure-3's zigzag, 15% down / 15% up on hold's daily closes; the same
  17 episodes); share avoided; net of the next 365 days.
- Fast-crash subset: the named 1987 and 2020 falls; and the cut "<= 92 days peak -> trough".
- Insurance cost = (CAGR hold - CAGR series, points a year) / mean loss avoided per fall (log
  points); insure-1's pooled premium P.
- Diagnostic: share of sessions in the market; how many switches fall on a roll Friday.

## Test and pass bar

- **Paired Sharpe test vs `tsmom12`**: d = Sharpe above bills (rule) - Sharpe above bills
  (`tsmom12`) on the same sessions; SE from a paired stationary block bootstrap (Politis-Romano,
  `research/lib/stats.py`'s indices) of the daily excess returns, mean block 21 sessions, 2,000
  draws, seed 0; z = d / SE. Side: mean block 63 (reported, not used to choose).
- **Project bar** (`research/register/BAR.md`, rows through 2026-11-24 20:01): 3,855 tries,
  N = 1,083 for a new pick, N_eff 500, **z >= 4.70**, Bonferroni p <= 1.0e-04. This card uses its
  own SE (other data than the primary test), so the z column applies.
- **Verdict rules**: z >= 4.70 "passes the bar" (a selectable claim, still not paper-tradeable:
  options are outside the paper broker); 1.645 <= z < 4.70 "better but not a pick";
  |z| < 1.645 "no Sharpe difference shown"; z <= -1.645 "worse than `tsmom12`".
- **Insurance verdict** (descriptive): the rule "adds fast-crash cover" if it loses less than
  `tsmom12` in both 1987 and 2020; it is "cheaper insurance than trend" only if its insurance
  cost is at or below trend's; "between" if it lies between trend's and PPUT's.
- One history: 17 falls, two named fast crashes. The fall results are a description.

## Rows

`research/tries.md`, idea `insure-4`: `tsmom12-pput-bills@insure4` (`variant`, train), and the
two robustness forms (`robustness`). Sharpe in the file's convention (daily calendar, 365, zero
rf). The baselines (hold, `tsmom12`, PPUT) already have insure-3 rows and are not repeated.

## Code

`research/lib/insure4.py` (reuses `insure3.py`'s loading and measures; one run, writes
`research/results/insure-4.md`), `tests/test_insure4.py`: the rule's position on a session uses
only closes before it (changing every price after a decision Friday leaves the positions through
the next Friday unchanged), the in-market return is PPUT's level-to-level return, the out
return is bills, and with PPUT set equal to the total return the rule reproduces `tsmom12`.
