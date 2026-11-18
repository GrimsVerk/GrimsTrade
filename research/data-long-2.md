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

## 3. trend-where-long: does `where-vol` change the worst loss on bonds and gold before 2002?

Card `research/cards/trend-where-long.md` (commit `11beac0`, pushed before any number). Code
`research/lib/trend_where_long.py` (rule copied from trend-where, translated to monthly bars,
one-month gap between signal and traded return; tests `tests/test_trend_where_long.py`: all-yes
is `tsmom12` exactly, all-no is hold, answers and weights unchanged when later returns are
replaced). One run; 18 rows in `research/tries.md` (idea `trend-where`, books `*-m`). Tables:
`research/results/trend-where-long.md`. Held-out year not touched (last return 2025-10).

### In plain words

**On bonds the switch never drops the filter, so nothing changes. On gold it drops the filter
from 1986, and the worst loss gets deeper by 9 points before 2002 and by 18 points after.
2022 was not a one-off: wherever `where-vol` drops the filter on a non-stock slot, it gives up
the filter's protection in the next long fall.** Robustness of a rule that already failed its
bar; nothing is selected, nothing changes in the live rule.

| Worst loss (monthly) | `where-vol` | `tsmom12` | Hold | Deeper than `tsmom12`? |
|---|---:|---:|---:|---|
| Bond alone, 1954-06 to 2001 | 25.6% | 25.6% | 15.2% | no (identical) |
| Gold alone, 1972-02 to 2001 | **51.7%** | 42.6% | 62.1% | **yes, +9.1 pts** (1980-01 to 1999-07) |
| Gold alone, 2002-2025 | **39.3%** | 21.7% | 39.3% | **yes, +17.6 pts** (2011-09 to 2015-12) |
| Bond + gold book, 1972-02 to 2001 | 21.6% | 21.6% | 28.1% | no (both 1980-01 to 1982-01) |
| Bond + gold book, 2002-2025 | **21.3%** | 12.0% | 20.1% | **yes, +9.3 pts** (gold 2012-2015) |

- **Bonds: yes at all 71 refits (1954-2024).** On monthly 10y returns the out months were
  clearly rougher than the in months (Dec 1981: 8.1% against 4.7% a year; Dec 2000: 7.9% against
  6.1%; Dec 2024: 7.2% against 6.3%), so the filter stays. That differs from trend-where, where
  daily TLT (20+ year bonds) turned no from 2009; the gap is shrinking here too (7.2 vs 6.3 by
  2024), but 1954-1981 weighs on the evidence for decades. So on this data the bond answer is
  not the one that cost 2022.
- **Gold: no from the Dec 1985 refit on (40 of 53 refits no; 16 of 29 before 2002).** The first
  five years with enough out months (1981-85) already show out months calmer (17.8% against
  30.0%): gold's violent months were rallies, in months. Dropping the filter then held gold
  through 1987-1999 (about half lost on monthly averages, Dec 1987 to Jul 1999), where
  `tsmom12` was out part of the time.
  Sharpe to 2001: 0.47 against 0.51 (p 0.73); 2002-2025: equal to hold, 0.94 against 0.93.
- **In the two-asset book the pre-2002 worst loss does not move** (both 21.6%, the 1980-82
  gold-and-bond fall, before the gold answer turned no); after 2002 it is 9 points deeper.
- **Sensitivities (disclosed, not selectable).** With 12-month minimums gold turns no already
  from Dec 1977 and the worst loss is that of hold (62.1% alone; 34.9% against 21.6% in the
  pair book): the waiting period of the 60-bar minimum was protecting the rule. Without the gap
  month (`-lag0`), every trend rule looks better (bond `tsmom12` Sharpe 0.97 against 0.82, gold
  worst loss 32.5% against 42.6%): that is the monthly-average overlap, not skill; the
  where-vol-versus-`tsmom12` ordering is unchanged.
- **Side finding, bonds alone:** the trend filter itself did not shrink the bond worst loss
  before 2002. Hold fell 15.2% (1979-08 to 1980-03); `tsmom12` lost 25.6% from 1979-08 to
  1982-01, whipsawed in the Volcker years (in for the Oct 1979 and Feb 1980 falls, out for the
  Apr-Jun 1980 rally, in for the Jul-Sep 1980 fall, out for the Nov 1981 rally), Sharpe 0.82 against hold's 0.99 (p 0.01). On monthly
  averages with a one-month gap, a 12-month filter on 10y bonds paid for itself only in the
  2020-2023 shock (15.3% against 25.2%).

### How sure

- One run, card first, no tuning. Gold has two long falls in the span (1980-1999, 2011-2015)
  and the switch had dropped the filter for 1986-1999 and for 2011-2015: two more episodes on
  top of 2022, so the trend-where worry now rests on three. Bonds give no answer to the question,
  because the switch never fired.
- Monthly averages (gold) and a rebuilt 10y constant-maturity bond (Shiller) are not fund
  prices: levels of worst loss are shallower than on daily closes, and the one-month gap delays
  every rule more than a weekly rule would be. The comparison between rules is like for like.
- Cash earns 0 (repo convention): in the 1970s-80s bills paid 5-15%, so the rules that sit out
  (`tsmom12`) are understated on growth here; worst losses are not affected.

### What this means

1. The live rule stays (`tsmom12` with the filter everywhere); this confirms trend-where's own
   conclusion that the filter on the gold slot is insurance, now on 1972-2025 instead of 2022.
2. The walk-forward "rougher out than in" test reads gold wrongly for risk: gold's rallies are
   its rough months, so the test says "the filter buys no calm", yet the filter is what keeps the
   book out of gold's long bears. Volatility of out months is the wrong yardstick for an asset
   whose risk is long slow falls.

### Next

- trend-where can be closed: its open worst-loss question now has an answer on gold (deeper,
  three episodes) and none possible on US 10y bonds (the switch never fires on 1954-2024).
- If a third non-stock slot is wanted: retry FRED (`PPIACO` all-commodity index 1913-, timed out
  from this machine on 2026-11-18) and run `where-vol` on it unchanged, card first.
- Loaders for the paper book: Shiller bond from 1953-04 and datahub gold from 1971-01 are usable
  as monthly stress histories, with the one-month gap; neither is a substitute for daily data.
