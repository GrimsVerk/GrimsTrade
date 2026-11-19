# fast-reentry: does a quicker return after the low keep more of trend's crash insurance?

Lane fast-reentry, written 2026-11-18 23:15 UTC, **before any number of this lane was
computed** (no return, episode or position of the new rule on any series). Branch
`fast-reentry` (from `insure-2`). Research only: fake money, files already in the data cache, no
change to the gym, the daily runner or the live strategies. The held-out year is not touched:
nothing after 2025-10-31 is parsed (insure-1/insure-2 loaders, unchanged).

## Why

insure-1 and insure-2: `tsmom12` avoids about half of each 25%+ fall (US 50 effective falls,
1927-2025; 13 developed non-US indices, 19 effective falls), but it buys back late, so net of
the year after the low it is a coin flip (US 16 of 50 positive, mean -0.3 log points; non-US 7
of 19, -0.9), and since 2002 the premium (growth given up per log point of loss avoided) is
about 1.3-1.5. The cost sits in the rebound (`B`). A rule that returns sooner after the low
should keep more of `I` net of `B`, if it does not pay for it in bear-market rallies.

## The one rule (fixed now; no other variant is run)

**`or3-12`: hold if the 12-month return OR the 3-month return is positive, else cash.** Same
paper-series mechanics as `tsmom12` in insure-1/2 (trend-tune's `paper`: Friday decisions on
closes visible at the decision, applied from the next session; 2 bps a side; cash at 0). The
3-month return is the log return over the last 91 calendar days (`trend_tune.lookback_logret`,
`days_of(3)`); with less than 91 days of history the 3-month signal is off.

- Exits: when the 12-month return turns negative, `or3-12` leaves only if the 3-month return is
  negative too. In a fall the 3-month return almost always turns first, so exits should be
  nearly those of `tsmom12` (the write-up counts how many `tsmom12` exits are delayed).
- Re-entry: while the 12-month return is still negative, it buys back as soon as the 3-month
  return is positive: in the slow/fast language of Goulding, Harvey and Mazzoleni, it is long in
  the "Rebound" state (slow signal bearish, fast signal bullish).
- Why this rule and not another: it is the one direction trend-tune's 98-cell surface named as
  pointing up ("slow to leave, quick to return", `trend-tune.md` next lane 3: +0.01 Sharpe over
  1994-2025 on the six assets, +0.08 since 2003, in sample, one of 98 cells) and proposed for a
  pre-registered test where it had not been seen. Taking that rule as named avoids a new
  forking path. A purer "armed" version (re-enter only after the 3-month return has been
  negative since the exit) is not run.

### Mechanism

- **Time-series momentum at several horizons.** Hurst, Ooi and Pedersen (2017), "A Century of
  Evidence on Trend-Following Investing", Journal of Portfolio Management 44(1): 1-, 3- and
  12-month trend signals each work over 1880-2016; the fast ones turn sooner at turning points.
- **Turning points.** Goulding, Harvey and Mazzoleni (2023), "Momentum Turning Points", Journal
  of Financial Economics 149(3), 378-406 (working-paper versions 2020-2021 with Ashish Garg as
  first author, as the lane brief cites it): slow and fast momentum define Bull, Correction,
  Bear and Rebound states; per the paper's summaries, slower momentum does better after
  Correction months and faster momentum after Rebound months. (Checked from the journal record
  and secondary summaries, not the full text. Their fast signal is 1 month; 3 months is used
  here because it is the cell trend-tune named and is less noisy.)
- **Why it may fail (stated so it can be wrong).** Bear markets have sharp rallies (1930-32,
  2000-03, 2008). A 3-month signal turns positive in those and gets caught in the next leg, so
  `I` falls in multi-leg falls. Coin lanes found every faster re-entry gives back more after
  lows (stop-reentry, PR #82). Fast falls (three months or less) are where `tsmom12` loses most
  (net about -7 to -15 log points); a 3-month signal should help most there.

## Data and episodes (insure-1/insure-2, unchanged)

- **US (decides):** French daily market + 10 industries, 1927-07-02 .. 2025-10-31; insure-1's
  25% / 25% zigzag episodes on holding, market-anchored clusters (50 effective falls).
- **Non-US (decides, direction):** insure-2's 13 developed headline indices (Yahoo, price,
  local currency), episodes anchored on the US market's falls (19 effective falls).
- **Description only:** the 3 French total-return regions (USD, from 1991); eras 1927-1961,
  1962-2001, 2002-2025 on US data; speed buckets (fast <= 92 days, medium, slow > 365).
- **Comparator: `tsmom12`'s paper series** on the same closes (not insure-1's gym splice, which
  has no counterpart for the new rule). The script checks that its own `tsmom12` replay equals
  trend-tune's `paper` series exactly. Episodes depend only on holding's prices, so both rules
  are scored on identical episodes, clusters and calm spans.

## Metrics

Per episode (log points, rule minus holding, insure-1's definitions): `I` (peak -> trough),
`B` (365 days after the trough or to the next peak), `N = I + B`, share avoided `S`; calm `C`;
pooled premium `P = -(sum B + C) / sum I`. The lane's quantity: **`dN` = `N(or3-12)` -
`N(tsmom12)` per episode, averaged within each effective fall** (the same for `dI`, `dB`, `dS`).

## Tests and pass rule (fixed now)

Sign test and cluster bootstrap over effective falls exactly as insure-1 (10,000 draws, seed 0,
one-sided, H1: mean `dN` > 0).

| Verdict | When |
|---|---|
| **Keeps more of the insurance** | US: mean cluster `dN` > 0 with sign-test p < 0.05 **and** bootstrap p < 0.05; non-US: mean cluster `dN` > 0; full-period premium `P(or3-12)` < `P(tsmom12)` on both the US 11 and the 13 developed; and the insurance kept: US mean cluster `S` at least `S(tsmom12)` - 0.10 |
| **Gives back more (no help)** | US mean cluster `dN` <= 0, or US `P(or3-12)` >= `P(tsmom12)` |
| **In between** | otherwise |

Also reported (description, no pass rule): `dI`, `dB` and `dN` by speed bucket and era; the
premium by era (2002-2025 is the "today" number); rule minus holding per series-year over the
full period for both rules; worst loss; position flips a year; how many `tsmom12` exits
`or3-12` delays; the total-return regions.

## Bar and rows

- **Family count: a new pick in the insure line.** insure-1 and insure-2 selected nothing
  (`insure-check` rows only), so `or3-12` is the line's first pick: family count 1, family bar
  p < 0.05 (the pass rule above). trend-tune's 98 cells are a separate, descriptive surface.
- **Project-wide bar** (`git show origin/register-2:research/register/BAR.md`, rows through
  2026-11-18 23:04, register-2 PR #92): 3,023 distinct tries, N 1,027 for a new pick, **N 433
  effective trials (measured rho 0.58); Bonferroni p <= 1.2e-4**, DSR 0.95 needs z >= 4.65
  (a Sharpe edge over `tsmom12` of +0.30 for a close rule on the primary test). The write-up
  says whether the US `dN` p-values would clear 1.2e-4. A change to the live rule would need
  that bar on the primary six-asset test, where trend-tune already saw `or3-12` at +0.01 over
  `tsmom12`: no live change can come out of this lane, whatever the verdict.
- `tries.md`: idea `fast-reentry`; one `variant` row for the deciding series (US market,
  `or3-12@insure-Mkt`), `robustness` rows for the other 10 US industries
  (`or3-12@insure-<ind>`), the 13 developed indices and the 3 regions
  (`or3-12@insure-geo-<series>`): 27 rows, 1 selectable. Columns as insure-1 (Sharpe daily, 365
  days, turnover = position flips a year).

## What each answer means

- **Keeps more:** a quicker return after the low recovers part of the rebound give-back on
  stock indices without losing the insurance; the premium measured by insure-1/2 is partly the
  price of `tsmom12`'s 12-month re-entry, not of trend insurance as such. Next: the held-out
  year and the six-asset gym run, against the project-wide bar.
- **Gives back more:** the late buy-back is the price of the insurance; faster re-entry trades
  it for bear-market rally losses, as on coins. The insurance premium of about 1.3-1.5 stands.
- **In between:** the direction helps somewhere (likely fast falls) but not enough to count.
