# Trend 1926: does `tsmom12` pay on stocks as a property, or only because of 2000-2002?

Research run trend-1926, started 2026-11-18. Branch `trend-1926` (from `trend-tune`). Research
only: fake money, files already in the data cache, no change to the gym, the daily runner or the
live strategies.

Trend-tune found that `tsmom12` (hold an asset while its 365-day return is positive, else cash)
beats plain holding only on stocks, and review 1 found that its lead comes from 2000-2002. Both
rest on SPY and QQQ since 1993: two funds, three bear markets. This run asks the same question
of US stocks from 1926 to 1961, on the rule exactly as it is, with nothing tuned.

## In plain words (results, 2026-11-18)

**Yes over the whole period, but not as a property. `tsmom12` beat holding on US stocks
1927-1961 (Sharpe 0.88 against 0.55 on the market, worst loss 38% against 84%), and about two
thirds of that lead is the crash of 1929-1932. After the war (1946-1961) it trailed holding on
the market. By the card this is short of "a property": the stock slots have crash insurance,
not an edge.** One run of the pre-registered evaluation, nothing tuned, nothing rerun. Tables:
`results/trend-1926.md`; 96 rows in `tries.md` (24 baseline, 72 robustness). Held-out year not
involved.

Sharpe is return per unit of risk (higher is better). "Difference" is Sharpe of the rule minus
Sharpe of holding; p is the one-sided bootstrap chance of seeing that lead by luck.

| Question (card) | Answer | Number |
|---|---|---|
| (a) Ahead over 1927-07 to 1961-12, market? | Yes | 0.88 against 0.55: +0.33, p 0.02, 90% range +0.06 to +0.60 |
| (a) Ahead on the ten-industry book? | Yes | 1.07 against 0.62: +0.45, p below 0.01 |
| (a) On how many industries? | 9 of 10 | energy level (0.55 against 0.55); the eleven series are one bet |
| (a) Worst loss | Halved or better | market 38% against 84%; book 33% against 82% |
| (b) Were the days out rougher than the days in? | Yes, whole period | market 27% against 16% volatility, ratio 1.68, p 0.02; 10 of 10 industries |
| (c) 1927-1945 | Ahead | market +0.44 (p 0.03); book +0.47 |
| (c) 1946-1961 | Behind on the market | market -0.09 (1.11 against 1.20), same worst loss 28%; book +0.15 (p 0.09); days out rougher on 1 of 10 industries |
| (d) Without 1929-1932 (`d1`) | Positive, not clear of zero | market +0.11 (p 0.18); book +0.21 (p 0.03) |
| (d) From 1933 (`d3`) | Positive, not clear of zero | market +0.09 (p 0.22); book +0.19 (p 0.05) |
| (d) Peak to trough removed (`d2`) | The same | market +0.09 (p 0.27); book +0.18 (p 0.10) |
| Later fill, 10 and 50 bps, interest on cash | Holds | market +0.28, +0.32, +0.27, +0.32 (p 0.03 to 0.05) |

**Against the card's bar.** The whole-period p-values pass (0.02 on the market, below 0.01 on
the book; the same with a 125-day block). "A property" also needed the market ahead in both
eras, and it is behind in 1946-1961, so the outcome is not "a property" and nothing is called
an edge. It is not "one crash again" either, because the market's difference stays positive in
`d1` and `d3`. The card's table has no row for exactly this case; the script prints "something
remains, but short of the card's conditions for a property", and that is the honest label. The
card decided `d1` and `d3` on sign alone, and on the market neither is clear of zero (p 0.18
and 0.22), so "something remains" is weak. The mechanism read on its own gives the card's
second reading: present on the market and 10 of 10 industries in 1927-1945, on 1 of 10 in
1946-1961, which the card fixed in advance as "it was the 1930s".

**Where the lead comes from.** The rule left the market 28 times and was bought back higher 22
times. One spell did the work: out 1929-11-11, back 1933-04-08, bought back 67% lower. The
other eight spells of 13 weeks or more came back between 7% lower and 11% higher and net to a
small cost (about 9 log points); the 19 short spells cost 36 log points in price. Outside the great crash the rule
gives up a little price and gains by being calmer (in `d3`: 21% volatility out, 15% in), which
leaves a small positive Sharpe difference that the data cannot tell from zero.

**What it means for the live rule.** Nothing changes (the card fixed that no outcome would).
The reading of the stock slots moves from "pays on stocks" to "paid in the great collapses":
1929-1932 here, 2000-2002 and 2008 on SPY and QQQ. In the calm bull market of 1946-1961 the
filter cost a little Sharpe and did not shrink the worst loss. The case for the filter on
stocks is the smaller worst loss in a collapse (38% against 84%), a risk choice for the owner.

**How sure.**

- This was not blind data. Invest-1 had already seen the market monthly (ahead in the 1930s,
  level in the 1940s, behind in the 1950s); this run finds the same shape with the gym's own
  rule on daily data. The direction is a confirmation, not a discovery.
- One market, one collapse: the market, the book and the industries are one bet seen eleven
  ways. The whole-period p of 0.02 is mostly one event.
- The primary fill is slightly kind to the rule (it trades at the close it has just seen); the
  later fill gives +0.28 (p 0.04).
- Nobody could have bought these portfolios as one instrument then; the 50 bps row (+0.27) is
  description.
- Replay check (the gym against a paper series with no gym code): total log growth within
  0.002 on the market, 0.011 on durables over 34 years, with one day 1.5% apart on durables.
  Not chased down in this burst; small next to the differences above.
- Only one rule was run, exactly as pre-registered, so nothing was selected and nothing needs
  deflating.

**Next lanes (not started).**

1. `trend-where-it-pays`: the walk-forward switch must be tested on 1946-1961 as its hard case
   (on 1927-1945 the days-out test says "stocks qualify", and the filter then trailed on the
   market for 16 years).
2. `fast-reentry`: the cost here is whipsaws and late returns (22 of 28 exits), the same as in
   trend-tune; this period is now an out-of-universe set for it.
3. French daily market and industries 1962-1993 as one more out-of-era set, on its own card
   (the S&P 500 index there was 0.45 against 0.49).

Below is the card, unchanged.

## Card (fixed 2026-11-18, before any new number)

### What had been seen when this was written

- Everything in `trend-tune.md`, `results/trend-tune-anatomy.md`, review 1 and `protocol.md`.
- **Invest-1 already looked at this period monthly** (`invest-1.md` on branch `invest-1`): a
  monthly trend rule on half stocks, half bonds, cash at the T-bill rate, on Ken French's
  monthly market return. Sharpe above T-bills by decade, trend rule against holding stocks:
  1927-39 0.64 against 0.22, 1940s 0.68 against 0.64, 1950s 1.21 against 1.40; worst loss
  1927-89 19% against 84%. So the rough direction on the market is known: ahead in the 1930s,
  about level in the 1940s, behind in the 1950s. That rule had a bond half, monthly decisions
  and interest on cash, so it is not this test, but this is not blind data for the market.
- The S&P 500 index 1962-1993 (`results/baselines.md`): `tsmom12` 0.45 against 0.49 for holding.
- General knowledge an agent cannot unlearn: US stocks fell by more than 80% in 1929-1932, and
  published studies report that trend filters cut that loss.
- From the French daily files: only their layout (header lines, first eight rows, first and
  last date). No return statistic, no rule.
- New here: daily data, the gym's own rule and fills, the ten industries, the days-in against
  days-out mechanism, and the cuts without 1929-1932.

### Data

- **Market:** Ken French's daily `Mkt-RF + RF`: all US listed stocks, value-weighted, dividends
  included (CRSP). File `F-F_Research_Data_Factors_daily_CSV.zip`.
- **Industries:** `10_Industry_Portfolios_daily_CSV.zip`, the value-weighted block: NoDur,
  Durbl, Manuf, Enrgy, HiTec, Telcm, Shops, Hlth, Utils, Other (consumer staples, consumer
  durables, manufacturing, energy, technology, telecoms, shops, health, utilities, the rest).
  Dead companies are in (CRSP), so there is no survivor tilt.
- Both from the cache snapshot of 2026-11-12, read with `python -I`, never committed.
- **Loaded: 1926-07-01 to 1961-12-31. Nothing later is parsed.** The protocol's S&P 500 index
  set starts 1962-01-02, so the two do not overlap, and the held-out year is not near.
- Returns are printed to 0.01% a day; the rounding is noise of at most 0.005% a day.
- Each series becomes a total-return index (100 on the day before the first return). A value
  marked missing (-99.99 or -999) means no bar for that asset that day; the count is reported.
- **Sessions.** The New York exchange opened on Saturdays until 1952, so the early years have
  about 300 sessions a year. The brief suggested "365 days is about 252 trading days"; that
  would be 10 months before 1952. Not needed: the rule counts calendar days, and it is run on
  calendar days here, unchanged.

### The rule, the twin, the engine

- **Rule:** `tsmom12` exactly as the protocol's twin (`c.weekly(c.slots(c.tsmom_signal))`): the
  asset is held while its return over the last 365 calendar days is positive, else cash;
  decided on Friday's close; 1% rebalance band. Lookback 12 months. Nothing else is tried.
- **Twin:** holding (`c.weekly(c.equal_weight)`): buy once, keep.
- **Run on:** the market alone, each of the ten industries alone (the whole account in one
  asset), and the ten industries as one equal-slot book (`tsmom12` against equal weight).
- **Engine:** `grimstrade.gym.simulate`, unchanged, through `lib/harness.py`. The series are
  registered as ETF-class symbols in the research process only (`F-Mkt`, `F-NoDur`, ...).
- **Period:** decisions from 1927-07-02 (a year after the first bar, as for every
  out-of-universe set) to the day before the last bar of 1961. 34.5 years.
- **Fill (disclosed approximation).** French has no opening prices. Primary: each bar's open is
  set to the previous close, so the gym's "next open" fill happens at the price of the close
  the signal was computed from, and the new position earns from the next session's
  close-to-close return. This is the convention the protocol already accepts for the S&P 500
  index 1962-1993 (Yahoo's index open is the previous close on most days there). It is
  slightly kind to the rule (it trades at a price it has just seen). **Robustness `late`:** the
  open is set to the same day's close, so the fill comes one session later, at the next
  session's close. Both are shown side by side.
- **Costs:** 2 bps a side (the gym's ETF cost). Robustness: 10 bps a side, and 50 bps a side,
  which is nearer to what trading stocks cost then (commission plus spread near 1% for a round
  trip; from memory, not checked). The 50 bps row is description: nobody could have bought
  these portfolios as one instrument.
- **Cash:** earns 0, and Sharpe is against 0 (the gym's rule). Robustness: cash earns French's
  daily T-bill return (`RF`, same file) and Sharpe is measured on returns above it, for the
  rule and for holding. This is a re-scoring of the primary runs, as in
  `results/cash-interest.md`: no new gym run, no `tries.md` row.
- **Statistics:** Sharpe on all calendar days, 365 a year (protocol). Difference rule minus
  holding on the same days: paired stationary bootstrap, mean block 20 days, 2,000 draws, seed
  0, one-sided p and 90% range. For the market and the book the p is also shown with a mean
  block of 125 days, because positions last for months.

### `tries.md` rows (idea `trend-1926`)

- Primary: rule and twin on 11 series and the book: 24 rows, kind `baseline` (both are the
  protocol's plain twins on new data; nothing is selectable).
- `late` fill, 10 bps, 50 bps: the same 24 each, kind `robustness`. 96 rows in all.

### Questions, fixed now

Windows are cut from the primary runs' daily returns; "the difference" is Sharpe of the rule
minus Sharpe of holding.

**(a) Whole period, 1927-07 to 1961-12.** Is the difference positive on the market? On the
ten-industry book? On how many of the ten industries? Bootstrap p for each. Worst loss of rule
and twin next to it. The eleven series move together: they are one bet seen eleven ways. The
two tests are the market and the book; the count of industries is description.

**(b) The mechanism.** Per series, from the gym's own fills: the share of sessions the rule
held; the volatility of the asset's daily log returns over the sessions it held and over the
sessions it did not (annualised with that window's own sessions per year); their ratio; how
many of the 20 worst sessions fell while it was out; what the asset earned per year of in-time
and of out-time. Test of "days out are rougher": the in/out sequence is rotated against the
returns by a random offset (keeps the spells, breaks the timing), 2,000 rotations, seed 0; p =
the share of rotations with a ratio at least as large. The mechanism is **present** on a series
if the ratio is above 1 with p < 0.10.

**(c) Two eras.** 1927-07 to 1945-12 and 1946-01 to 1961-12: the difference and the volatility
ratio in each.

**(d) Without the great crash.** Three cuts:

- `d1`: calendar years 1929 to 1932 removed (those days dropped from both series, the rest
  joined).
- `d2`: peak to trough only, 1929-09-03 to 1932-07-08 removed (the Dow's high and low, dates
  from general knowledge, not from this data). This is review 1's kind of cut. It is harsh on
  the rule: the fall goes, the rebound it was late for stays.
- `d3`: 1933-01-01 to 1961-12-31, one unbroken window.

**Something remains** if the market's difference is positive in `d1` and in `d3`.

**Also shown (description):** per series, the number of spells out and how many were whipsaws
(bought back higher than sold); for the market, every spell out longer than 13 weeks with its
dates and the price move between the two fills.

### What each answer will mean (fixed now)

No outcome changes the live rule in this run: nothing here is a candidate, and the held-out
year is not involved. The outcome changes what the owner should believe about the stock slots.

| Outcome | When | What it means for the live rule |
|---|---|---|
| **A property** | Market difference positive over the whole period, in both eras, in `d1` and in `d3`; the book agrees in sign over the whole period and in `d1`; the mechanism is present on the market over the whole period and in `d3` | "Insurance on the stock slots" has now shown up on bear markets the rule was never looked at on. Keep the filter on SPY and QQQ with more confidence; `trend-where-it-pays` starts from "stocks qualify". It is called an edge only if p < 0.10 on the market and on the book over the whole period, and even then it is one bet. |
| **One crash again** | Market difference positive over the whole period, but not in `d1` or not in `d3` | The same shape as review 1: the lead is one giant collapse each time (1929-32 there, 2000-02 here). The rule is crash insurance that pays in multi-year collapses and ties or trails otherwise. The live rule stays as a risk choice; "pays on stocks" in our write-ups becomes "paid in the great collapses". If the mechanism is present all the same, the calm is real and the late return hands it back: the lane to work on is re-entry (`fast-reentry`), not the exit. |
| **No** | Market difference zero or negative over the whole period | The stock result of 1994-2025 does not repeat even with 1929-32 in the sample. Read SPY +0.09 and QQQ +0.11 as 2000-2002 and 2008. The filter on stocks is then justified only by a smaller worst loss, which this run reports; whether that is worth its cost goes to the owner as a risk choice and to `trend-where-it-pays` as a test. |
| **Too fragile to call** | The market and the book disagree in sign over the whole period, or the primary and `late` fills disagree in sign on the market | Treated as "no property shown". |

The mechanism (b) is also read on its own: present on the market and at least 8 of 10
industries, in both eras, means "rough days cluster in stock downtrends" is a property of
stocks whatever the Sharpe says; present only in 1927-45 means it was the 1930s.

### Assumptions

- "Excluding 1929-1932" is read three ways (`d1`-`d3`) because each has a known bias; `d1` and
  `d3` decide.
- The 50 bps row and the 125-day block are additions to the brief (which named 2 and 10 bps
  and the protocol's bootstrap).
- 1926-07 to 1927-06 is warm-up: the rule needs a year of history, so results start 1927-07.
