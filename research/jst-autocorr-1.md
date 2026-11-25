# jst-autocorr-1: is insure-1870-1's timing result an artefact of smoothed early indices?

Lane `jst-autocorr-1`, 2026-11-25 (night of 2026-11-24 UTC). Branch `jst-autocorr-1`, PR #192.
Descriptive, nothing selected. Card: [`cards/jst-autocorr-1.md`](cards/jst-autocorr-1.md)
(pushed before any number). Tables: [`results/jst-autocorr-1.md`](results/jst-autocorr-1.md).
Code: `lib/jstautocorr.py`, tests `tests/test_jstautocorr.py`. Statistics only: JST R6 is
CC BY-NC-SA 4.0 (Jorda, Schularick and Taylor 2017; Jorda, Knoll, Kuvshinov, Schularick and
Taylor 2019); Norges Bank's monthly stock price index (Klovland 2004, Norges Bank Occasional
Papers 35, ch. 8) and Shiller's monthly file are read locally, not committed.

## The answer on one screen

**Partly. Most of the timing gap is what the autocorrelation alone produces, but where the data
can be checked they are year-end, not averaged, so the autocorrelation is not shown to be a
smoothing artefact.** By the card's rule the reading is "smoothing could explain it", by a
narrow margin and only under full annual averaging, which smooths more than the data show.

- **(4) Simulation.** Measured returns with an AR(1) of 0.19 (realised acf 0.16, about the
  observed 0.17) give the rule a per-episode share avoided of 0.74 against 0.55 at random dates:
  a median gap of +0.20. Observed: 0.80 against 0.47, gap +0.32, the 98th percentile of that
  null (22 of 1,000 worlds as large). Full annual averaging of a monthly random walk (acf 0.22)
  gives a median gap of +0.24; the observed gap is its 94th percentile (64 of 1,000 worlds
  reach it), just under the card's 95th-percentile line. Under a random walk (phi 0) the median
  gap is +0.06 (the event definition alone gives a little) and no world of 1,000 reaches +0.32.
  So the AR(1) null's median gap is 61% of the observed gap (0.20 of 0.32); above the
  random-walk level it is about half (0.13 of 0.26). The rest is not explained by an AR(1) of
  this size.
- **If it were averaging, the timing would be fake.** In the averaging worlds, the same signal
  scored against the true year-end returns has a gap of +0.01 (S 0.53 vs 0.52): the whole edge
  exists only on the measured index.
- **(1) and (3): checked data are year-end.** The JST appendix (`RORE_documentation.pdf`,
  macrohistory.net, fetched without trouble) names each country's equity sources but says
  nothing per country about year-end vs averaged prices; the paper states the year-end
  convention. Two sources could be matched with monthly data:
  - **US:** JST `eq_tr` is Shiller's December-to-December total return (correlation 1.000, mean
    gap 0.2 log points, 1872-1926), where Shiller's December price is the month's average of
    daily closes. An annual-average version correlates only 0.63. Acf -0.07 (1872-1926), +0.12
    (1927-1965); the annual-average version would give +0.11 and +0.25.
  - **Norway 1921-1965:** JST `eq_capgain` is exactly the December-to-December change of
    Klovland's monthly index (correlation 1.000, mean gap 0.0), which records the latest bid of
    the month. Year-end, and still autocorrelated: acf +0.23 (annual averages would give
    +0.34).
- **Where the autocorrelation sits.** Highest in source periods built from early share-level
  microdata or narrow selections: Norway 1881-1920 (JST's own Oslo microdata) +0.60, Germany
  1890-1913 (Eube) +0.43, Denmark 1901-1922 (yearbook selection) +0.42, Portugal (Lisbon
  microdata) +0.36, Sweden (Waldenstrom) +0.35, Belgium (Buelens) +0.32. In thin markets stale
  last-trade prices can make even a year-end index autocorrelated; this could not be checked
  (no keyless monthly series for those periods was found in the time of the lane).
- **(2) The label split is uninformative.** Only the US differs from the paper-wide year-end
  label (plus 4 non-calendar or interpolated war years without episodes); the US has one episode
  (1907, a tie). The year-end-labelled group: acf +0.17, 37 episodes, S 0.82 vs 0.47 random, gap
  +0.34. By the card's rule that "survives on year-end data", but the label carries no
  per-country information, so this says little.

**What it means for insure-1870-1 and the SUMMARY claim.** The rotation test behind p_S 0.020
assumes timing-free returns; with a lag-1 autocorrelation of 0.17-0.19 a large part of the S gap
is mechanical. Whether that autocorrelation is real (an annual trend rule could have used it) or
an index artefact is open: real year-end data in Norway 1921-1965 still show it, the US shows
neither autocorrelation nor timing (its one fall is a tie), and the high-autocorrelation early
microdata periods are unverified. Read the early-data timing evidence as "consistent with the
autocorrelation of those indices, of unknown origin", not as an independent confirmation of
timing. The insurance count (losing less in 9 of 9 falls) is not affected: fixed exposure also
achieves it. Nothing changes for the live rule.

## How sure

- Card before numbers; one fixed set of scenarios; nothing tuned. The reading is close to its
  line (94th percentile against a 95th-percentile rule), so "could explain" is weak either way.
- **The simulated null is too narrow, which favours "not explained".** Worlds draw each segment
  independently and Gaussian; real falls are fat-tailed and common across countries (world wars,
  1929-32), so the real sample has fewer independent events and a wider distribution of the gap.
  With a wider null the observed gap would sit at a lower percentile.
- **Per-episode, not per-cluster.** This lane pools S over the 38 episodes (0.80 / 0.52 fixed /
  0.47 random), checked equal to insure-1870-1's own episode scoring; insure-1870-1's headline
  0.73 is the mean over 9 anchored clusters. The simulation has no anchors, so the per-episode
  version is the like-for-like one.
- **Averaging scenario overshoots.** Full 12-month averaging gives acf 0.22, more than observed;
  a mix of averaged and year-end countries would give gaps between the phi 0.19 and averaging
  rows.
- **Stale prices are not averaging.** A year-end index of thinly traded shares can lag by
  weeks or months; that gives a smaller autocorrelation at annual frequency than full
  averaging but is equally untradable. Not separated here.
- **Observed acf.** 0.165 demeaned per segment (0.187 not demeaned, matching insure-1870-1's
  0.19), 0.170 over bills.

## Logged

`tries.md`: one `note` row (idea `jst-autocorr-1`). No strategy try, nothing selectable.
