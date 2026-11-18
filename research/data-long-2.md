# Data long 2: gold loader, cross-check, trend-where on long bonds and gold

Lane `data-long-2`, 2026-11-18, branch `data-long-2` (from `data-long-1`, draft PR #48).
Research only, fake money, no raw data committed.

## 1. Gold loader

`research/lib/long_gold.py` reads `<cache_root>/datahub-gold/<YYYY-MM-DD>/monthly.csv` (newest
dated folder; download by hand from https://datahub.io/core/gold-prices/r/monthly.csv, PDDL).
Offline test `tests/test_long_gold.py` on a five-row fixture.

Spans read from the copy fetched 2026-11-18 (HTTP 200, 35,747 bytes, sha256
`f20720f3413b3dd114cd116951516f0fab577ff8c91e102a3a92549582ea9608`), parsed with `python -I`:

- 2,326 months, 1833-01 to 2026-10, consecutive (no gaps, no duplicates).
- 670 monthly returns from `FREE_FROM` = 1971-01 to 2026-10.
- Before 1971 the price moves in only 88 of ~1,650 months (fixed USD price 20.67, then 35 from
  1934; the 1968-70 two-tier market wiggles between 35 and 43). Not market risk.
- Prices are whole dollars into the 1970s and look like monthly averages, not month-end closes
  (checked in section 2).

Other caches used here (same root, not committed): Shiller `shiller/ie_data.xls` (sha256
`89c5c210...6d7`, lane data-long-1), Damodaran `damodaran/2026-11-18/histretSP.xls` (HTTP 200,
527,872 bytes, sha256 `28b81109...49c69`).

## 2. Cross-check against Damodaran annual (1928-2024)

Script `research/lib/long_check.py` (`uv run --with xlrd python -I research/lib/long_check.py`);
full year-by-year table `research/results/data-long-2-crosscheck.md`. 2025 is left out: it runs
into the held-out year (from 2025-11-11). Disclosure: Damodaran's 2025 row was printed once while
reading the sheet layout; no strategy number was computed from it.

Gap = monthly source compounded to a calendar year minus Damodaran.

| Series | Window | Mean gap | Mean abs gap | Largest | Years > 2 pts off | Corr |
|---|---|---:|---:|---:|---:|---:|
| Shiller bond, labels Jan-Dec | 1953-1999 | +0.41% | 1.80% | +10.4% (1982) | 16 of 47 | 0.968 |
| Shiller bond, labels **Dec-Nov** | 1953-1999 | +0.44% | **0.49%** | +3.6% | 1 of 47 | **0.998** |
| Shiller bond, labels Dec-Nov | 2000-2024 | +0.09% | 1.53% | +4.4% | 6 of 25 | 0.984 |
| Shiller bond, labels Dec-Nov | 1928-1952 | +0.01% | 1.23% | +3.4% | 7 of 25 | 0.794 |
| datahub gold, Dec/Dec | 1971-2024 | -0.15% | 2.92% | +14.1% (2009) | 27 of 54 | 0.988 |
| datahub gold, year avg/avg | 1971-2024 | -0.57% | 11.04% | +83.0% (1980) | 48 of 54 | 0.730 |
| datahub gold, year avg/avg | 1928-1970 | -0.09% | 0.14% | -3.0% | 1 of 43 | 0.998 |

What the gaps say, and the likely causes:

1. **Shiller's bond return labelled month t is the return from month t to month t+1.** Compounding
   labels Dec(y-1)..Nov(y) matches Damodaran's year-end-to-year-end return almost exactly in
   1953-1999 (mean abs gap 0.5 pts, corr 0.998); the calendar Jan-Dec labels are off by up to
   10 points in fast years (1982). So the return at label t is known only at the end of month
   t+1: a monthly trend rule must not apply a signal built from label t to label t+1 (see the
   card of section 3). Not a data error; a dating convention to respect.
2. **Remaining bond gap: averages against year-end, and the coupon convention.** GS10 is a
   monthly average yield, Damodaran uses the end-of-December yield, so Shiller's year ends
   about half a month early; this explains the 1.5-point mean abs gap after 2000 (2022: Shiller
   -11.9% Jan-Dec labels vs Damodaran -17.8%). A steady +0.4 pts a year in 1953-1999 fits a
   monthly-compounded coupon in Shiller's rebuild against Damodaran's single annual coupon.
3. **Before 1953 Shiller's monthly bond series is interpolated.** `Rate GS10` before 1953-04 is a
   straight line between January values (checked: 1900 falls by exactly 0.0042 a month; 1952
   rises by 0.0125 a month). So each month's return in a year already carries the next
   January's yield: **look-ahead built into the data.** Monthly signals on Shiller bonds are
   only honest from 1953-04. Annual returns are fine (corr 0.79 with Damodaran 1928-1952, mean
   gap ~0; the remaining scatter is two different pre-war long-yield sources).
4. **datahub gold is a monthly average, not a month-end price.** After 1971 Dec/Dec matches
   Damodaran (LBMA year-end) to a mean abs 2.9 pts, year-average/year-average does not (11 pts):
   so each month is one figure for that month, and December's average sits on average half a
   month before Damodaran's year-end close (2009 +14 pts: gold peaked in early December 2009 and
   closed the year about 10% lower, so December's average sat well above the year-end close). Averages smooth the series (worst losses read shallower than on closes) and make
   consecutive monthly returns overlap, which flatters any trend rule applied the next month.
5. **datahub gold before 1960 is one annual value repeated twelve times** (132 years, 1833-1967
   except 1960-62, have a single price for all months) and matches Damodaran's NMA annual
   averages to the cent 1928-1967, including the odd 1931 -17% (a quirk of that shared NMA
   source; the US price was fixed at 20.67). Gold before 1971 is neither monthly nor market risk.

**Usable for monthly tests:** Shiller bond from label 1953-04, gold from 1971-01, both with a
one-month gap between the last return a signal sees and the first return it trades.
