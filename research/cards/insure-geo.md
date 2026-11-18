# insure-geo: does trend's crash insurance hold outside the US?

Lane insure-2, step 2, written 2026-11-18 23:05 UTC, **before any number of this step was
computed** (no episode, no rule return, no drawdown of any non-US series). Branch `insure-2`.
Research only: fake money, keyless public data, no change to the gym, the daily runner or the
live strategies. No new rule: `tsmom12` exactly as insure-1 ran it, on new data. The held-out
year is not touched: the downloads stop at 2025-10-31 (Yahoo `period2` = 2025-11-01 00:00 UTC)
and nothing later is parsed from the French files.

## Why

insure-1 and step 1 rest on one country: 50 effective US falls, 1927-2025. If "trend avoids
about half of each fall, more cheaply than holding less" is a property of trend and not of US
history, it should show on other stock markets, counted and judged the same way.

## What had been seen when this was written

- All of insure-1 and step 1 of this lane (`results/insure-2.md`): after 1962 on US data the
  rule's premium is 1.36 against 1.88 for a fixed exposure and 2.20 for random timing; 2002-2025
  alone "In between".
- The downloaded files' layout only: each index's first and last day, session count, gaps
  longer than 10 calendar days (all market holidays: Lunar New Year in Taiwan, Eid in
  Indonesia, Golden Week 2019 in Japan), flat stretches (Nikkei 225: one 21-session flat close,
  1972-03-31 .. 1972-04-28, kept and flagged; TA-125: holiday stretches of 5-8 sessions), and
  daily moves above 15% (dates only: 1987-10 in Australia and Hong Kong, 1989-06 Hong Kong,
  1990s Brazil and Malaysia). No return over any window, no drawdown, no rule position.
- General knowledge an agent cannot unlearn: the large non-US falls (Japan 1990-2003, Asia
  1997-98, 2000-03 and 2007-09 everywhere, Europe 2011, 2020).
- **Expectation, stated so it can be wrong:** the insurance shows outside the US too (`I`
  positive in most effective episodes); net of the rebound about zero or negative; premium
  between 1.1 and 1.5; cheaper than a fixed exposure, but the rotation tests weaker than on US
  data because the span is shorter (about 35 years against 98).

## Data

- **Primary set (13 developed markets, Yahoo chart API daily closes, local currency):** Japan
  `^N225` (from 1965), Canada `^GSPTSE` (1979), UK `^FTSE` (1984), Australia `^AORD` (1984),
  Hong Kong `^HSI` (1986), Germany `^GDAXI` (1987), Singapore `^STI` (1987), France `^FCHI`
  (1990), Switzerland `^SSMI` (1990), Belgium `^BFX` (1991), Netherlands `^AEX` (1992), Austria
  `^ATX` (1992), Spain `^IBEX` (1993). Rule fixed now: developed markets whose Yahoo headline
  index starts by 1993-12-31. To 2025-10-31.
- These are **price indices** (the DAX is a total-return index): dividends are missing. That
  understates holding's return in calm markets (when the rule is out it forgoes dividends too,
  but in the data it forgoes only price), so the premium is biased **down** (in the rule's
  favour). The total-return check below measures how much.
- **Total-return check (Ken French regional daily, US dollars, dividends included, market =
  Mkt-RF + RF):** Europe, Japan, Asia Pacific ex Japan, from 1990-07-02. Plus Developed ex US as
  one series, reported on its own.
- **Wider set (description):** every other downloaded index with daily history from 2005 or
  earlier: Italy `FTSEMIB.MI` (1997), New Zealand `^NZ50` (2003), Israel `^TA125.TA` (1992),
  Korea `^KS11` (1996), Taiwan `^TWII` (1997), India `^BSESN` (1997), Brazil `^BVSP` (1993),
  Mexico `^MXX` (1991), Malaysia `^KLSE` (1993), Indonesia `^JKSE` (1990). Sweden `^OMX` starts
  2008-11 and is left out; Norway `^OSEAX` did not download.
- Licence/keyless: Yahoo's chart endpoint needs no key (used by the project's daily runner);
  the French library is free for research use. Raw files stay in the data cache
  (`insure-2/raw-2026-11-18/`), never committed; read with `python -I`.

## Rule and metrics (insure-1's, unchanged)

- Rule: `tsmom12`, trend-tune's gym-free paper series (Friday decisions, 12-month lookback, 2
  bps a side, cash at 0), on each series' closes; first decision after a year of bars; the
  series' episodes and statistics start at its first decision.
- Episodes: 25% fall / 25% rise zigzag on holding's closes; `I`, `S`, `B` (365 days or the
  next peak), `N`, calm `C`, premium `P = -(sum B + C) / sum I`, exactly as
  `cards/crash-insurance.md` (the decomposition identity is checked again).
- Speed buckets (fast <= 92 days, medium, slow > 365), per era (episodes by peak: before 2002,
  2002-2025), sensitivity 20% and 40% falls: description.

## Effective episodes (counted the same way)

- **Primary, anchored:** insure-1 anchored industry falls on the US market's falls. Here the
  anchors are the same US market 25% episodes (French daily market, as scored in insure-1):
  the world's falls are mostly the US market's. A non-US episode joins the US episode whose
  `[peak, trough]` holds its trough, else its peak; the rest form their own clusters by single
  linkage on overlapping windows. A cluster's value is the mean over its **non-US** episodes
  only (the US episode is the label, not evidence); clusters without a non-US episode are
  dropped.
- **Strict, linked:** single linkage on overlapping `[peak, trough]` windows across the non-US
  episodes alone.

## Tests and pass rule (fixed now)

Sign test and cluster bootstrap as in insure-1 (10,000 draws, seed 0, one-sided).

| Outcome (primary set) | When |
|---|---|
| **Insurance generalises, and is kept after the rebound** | `I`: sign test p < 0.05 and bootstrap p < 0.05 under both clusterings; `N` the same under anchored clusters |
| **Insurance generalises, handed back in the rebound** | `I` passes as above; `N` does not |
| **Insurance not shown outside the US** | `I` fails under either clustering |

**Cheaper than holding less (card 2's controls on the primary set):** fixed exposure per
series at the rule's mean position; random timing by rotating every series' positions by one
common offset of `D` calendar days (`D` uniform in [365, L - 365], L the shortest series' span
from first decision to end; each series wraps within its own span; a rotated session takes the
position of the last session on or before its shifted date), return `pos * r - 0.0002 * flips`,
1,000 rotations, seed 0. The rule as its paper series.

| Outcome | When |
|---|---|
| **Timing, not just exposure** | rule `S` above rotations p < 0.05 and rule `P` below rotations p < 0.05, and rule `P` below `P_fix` |
| **Exposure, not timing** | neither p below 0.10 |
| **In between** | otherwise |

- The total-return check and the wider set get the same tables (description, no pass rule).
  "Agrees" if `I` passes there too and the premium order (rule below fixed) is the same.
- US comparison (description): insure-1's US premium in the same years (1962-2001 1.38,
  2002-2025 1.34; step 1's controls 1.88 fixed, 2.20 random for 1962-2025).

## Bar and rows

- Not a pick: no rule is selected, so the bar for a new pick does not apply; quoted for scale.
  Base lane insure-1: no family bar (descriptive). Project-wide (`git show
  origin/register-1:research/register/BAR.md`, rows through 2026-11-18 22:34): **2,904 tries,
  N 1,012 for a new pick, Bonferroni p <= 4.9e-5.** The write-up says whether the sign-test p
  would clear it.
- `tries.md`: one `insure-check` row per series computed (13 primary, 4 French regional, 10
  wider = 27), idea `insure-2`, variant `tsmom12@insure-geo-<series>`. Controls, thresholds
  and eras are re-scorings: no rows.

## What each answer means

- **Generalises + timing:** the US finding is a property of trend on stock markets; an
  investor can expect it in any broad stock index, at about the premium measured.
- **Generalises, exposure only:** outside the US trend loses less in falls, but no more cheaply
  than holding less.
- **Not shown:** the US result may be US history; the insurance claim should be stated for the
  US only.
- No outcome changes the live rule tonight.
