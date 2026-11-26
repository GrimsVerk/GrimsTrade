# ownvol-indep-1: `own_vol_70` against `tsmom12` on stock data it had never seen

Lane `ownvol-indep-1`, 2026-11-26 (night). Branch `ownvol-indep-1`. Research only: fake money,
cached keyless data (no download), no change to the gym, the daily runner, the scoreboard, the
workflows, the live strategies or the `own_vol_70` paper book; nothing after 2025-10-31 read.
Card (pushed before any own-vol number, not amended after numbers): `cards/ownvol-indep-1.md`
(commits f5b50ac and 554db23, a header-time fix, both before the run). Tables:
`results/ownvol-indep-1.md` (+ `.json`). Code: `lib/ownvolindep1.py` (reuses `lib/e4indep1.py`
data, specs and segment rule, and `lib/pooled2_core.py`'s frozen monthly rules and bootstrap);
tests `tests/test_ownvolindep1.py`.

## The answer on one screen

**Not shown, and not contradicted at the 41's size. By the card's rule: "not confirmed, not
contradicted".** On e4-indep-1's four stock markets before 1927-07 (US, GB, DE, FR; 171
market-years that overlap nothing own-vol was scored on), own-vol (pooled-2's monthly
`vt-own-70-x`) trails `tsmom12` by **D = -0.007 Sharpe a market (SE 0.021, z -0.34)**. The
one-sided 95% upper bound is **+0.028**, just above the 41-market +0.022 (so not
contradicted), and **below #110's +0.06**: an edge of the six-asset size is unlikely on stocks
in general. Own-vol wins in 2 of 4 markets (GB +0.048, FR +0.015; US -0.083, DE -0.009).

- **What this does to "equity-only at best":** nothing changes in the label, but its content
  shrinks. The stock lean has no independent support (D about zero on clean data), the 41's
  +0.022 is neither confirmed nor ruled out, and anything as large as +0.06 on stocks is
  unlikely. Combined with the 41 (inverse variance, not deciding): **+0.012, SE 0.013, z
  +0.90**. Reading: a risk dial whose Sharpe edge on stocks, if any, is about +0.01. Not a
  retune trigger; nothing goes live or changes in the paper book from this lane.
- **It is the US, not Germany.** e4-indep-1's pool leaned on Germany; this one leans on the US
  (Shiller monthly averages, g 1): without US D is +0.018 (SE 0.020), without DE -0.007,
  without GB -0.026 (upper +0.015, the only leave-one-out cell below +0.022), without FR -0.015.
- **Warm-up dilution does not hide an edge.** Sized months only (each segment's first 60 + g
  scored months dropped): D +0.001 (SE 0.028).
- **Dividends help own-vol slightly.** US with Shiller's dividends: D +0.010 (SE 0.018), the
  same direction as e4-indep-1's dividend check (price-only returns understate the Sharpe of
  a fractional position).
- **Early and late halves differ.** 1867-1897: -0.078 (SE 0.051, 0 of 3 positive); 1898-1927:
  +0.024 (SE 0.016, z 1.48, 3 of 4 positive). Shown, not deciding; two halves of one test.
- **Secondary pool N5** (DK, FI, IE, NO, SE, French country files 1975-2025: new markets, the
  41's calendar): **D +0.010 (SE 0.026, z +0.39), 4 of 5 positive**, upper +0.052. Same
  reading: not confirmed, not contradicted; +0.06 unlikely.
- **The risk dial works as a risk dial.** In all nine markets own-vol has lower volatility and
  a lower maximum drawdown than `tsmom12` (P4: US 29% to 21%, GB 31% to 22%, DE 24% to 21%,
  FR 32% to 24%), at a mean share of 0.59-0.86. That is mostly the lower average share, not
  skill; it is what a 70% dial is expected to do.

## Results (P4 deciding; from `results/ownvol-indep-1.md`)

| Market | Years | `tsmom12` Sharpe | own-vol Sharpe | d | Mean share |
|---|---:|---:|---:|---:|---:|
| US (Shiller, g 1) | 55.3 | +0.412 | +0.329 | -0.083 | 0.59 |
| GB (NBER, g 0) | 50.8 | +0.394 | +0.442 | +0.048 | 0.76 |
| DE (NBER, g 1) | 42.8 | +0.541 | +0.533 | -0.009 | 0.86 |
| FR (NBER, g 0 / 1) | 21.8 | +0.355 | +0.370 | +0.015 | 0.64 |
| **P4 (deciding)** | 171 | | | **-0.007** (SE 0.021, z -0.34, upper +0.028) | |

`tsmom12`'s Sharpes equal e4-indep-1's to three decimals (same data and code: a consistency
check).

| Check (P4, not deciding) | D | SE | z | Upper |
|---|---:|---:|---:|---:|
| without US / GB / DE / FR | +0.018 / -0.026 / -0.007 / -0.015 | 0.020 / 0.025 / 0.024 / 0.028 | | +0.051 / +0.015 / +0.033 / +0.031 |
| sized months only | +0.001 | 0.028 | +0.05 | +0.047 |
| g = 1 for every series | -0.009 | 0.021 | -0.45 | +0.025 |
| cost 50 bps a side (sleeve) | -0.010 | 0.021 | -0.46 | +0.025 |
| blocks 6 / 24 months | -0.007 / -0.007 | 0.024 / 0.021 | | +0.032 / +0.027 |
| US with Shiller's dividends | +0.010 | 0.018 | +0.60 | +0.039 |
| 1867-1897 / 1898-1927 | -0.078 / +0.024 | 0.051 / 0.016 | -1.54 / +1.48 | +0.005 / +0.051 |
| N5 (secondary) | +0.010 | 0.026 | +0.39 | +0.052 |

## Card against run (deviations)

- None in the data, rules, statistic, threshold or cells. All named cells were computed.
- Power: the card expected SE 0.016-0.025 (from published SE ratios); the realised SE is
  0.021, inside that range. Power at +0.022 was 0.22-0.39 by the card, so "neither" was the
  likely outcome, as it came.
- The "sized months only" cell drops the first 60 + g scored months; sizing starts at scored
  month 59 + g (36 sigma months, then 24 sigmas at the target), so it also drops one sized
  month a segment. Negligible; reported as run.
- Mean share is below 0.70 in US and FR (0.59, 0.64): k is solved so that the mean of
  min(1, k / sigma) over the sigmas *seen so far* is 0.70; later sigmas need not average to
  that. Frozen behaviour, not changed.
- The card said warm-up months add no variance to d; consistent with that, the sized-only
  cell (fewer months, all of them sized) has a larger SE (0.028) than the full pool (0.021).

## Counts

32 rows in `tries.md`: 2 `variant` (P4 deciding, N5 secondary; selectable by kind, as
e4-indep-1 logged them), 18 `robustness` per market and rule (P4 4 x 2, N5 5 x 2), 12
`robustness` checks. The project bar (`research/register/BAR.md`, rows through 2026-11-25
23:32: N_eff 509, z >= 4.70) is not approached; `register/BAR.md` not edited.

## Caveats

- **Small.** Four markets; the US alone moves D by 0.025. The US series is a monthly average
  (g 1), which smooths the sigma own-vol sizes on and lags it a month.
- **Old data, price returns.** See e4-indep-1's caveats (France's patched, rounded index;
  Germany's unweighted early index; the 1914 closures). Dividends are only in the US check.
- **Monthly sigma.** The live rule uses a 52-week sigma from daily data; here 36 monthly
  returns (pooled-2's frozen form). A slower, coarser sigma is a weaker version of the rule;
  that the monthly form gave +0.022 on pooled-2's monthly markets (#159) suggests the form
  alone does not erase the effect, but it is a stated deviation, not tested here.
- **What is left.** e4-indep-1's list: a US-only pool before 1871 (NBER railroads, cached),
  GIP NYSE 1815-1925 (not checked), and Yale ICF data (owner decision on its terms pending,
  data-wide-2). Clean independent stock data for own-vol are otherwise spent.
