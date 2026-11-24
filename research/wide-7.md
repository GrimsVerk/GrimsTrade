# Wide 7: event-study gates for wash-sale echo (W14) and festival gold (W13)

Research run wide-7, 2026-11-18. Branch `wide-7` (from `wide-6`), draft PR into `wide-6`.
Research only: fake money, public data, no change to the gym, the daily runner or the live
strategies.

Method as in ann-1 and wide-6: a cheap **event-study gate** first, its rule pushed before any
number. A gate is descriptive: it gets no `tries.md` row and does not count as a tested
mechanism. Only a pass gets a card and a train test, read against the family bar.

**Family count carried in:** 68 mechanisms, 16 tested by a strategy, none passed (wide-6, the
union of the wide and survey lines). A strategy test in this run would be read at
**p < 0.10 / 68 = 0.00147**.

Process rule from wide-6: no gate runs before its code (and any fix to it) is committed and
pushed, with the repo checks clean.

## Step 1. W14 `wash-sale-echo` (tax law)

### The idea

US tax law disallows a capital loss if the seller buys a "substantially identical" security
within 30 days before or after the sale (IRC section 1091, the wash-sale rule). An investor
who sells a losing ETF in December to book the loss and wants the exposure back must stay out
for 31 days or hold a substitute in between. If year-end tax-loss selling pushes losers down
and the sellers' own buying brings them back, the US rule moves that buying to about a month
after the selling: mid-January to early February, not the first days of January.
Automated harvesting by robo-advisers (from memory: Wealthfront and Betterment from about
2012) switches into a substitute fund at once and back into the original after 31 days, which
is the same delayed buy.

Spot coins are property for US tax, not securities, and the wash-sale rule did not cover them
in any train year (proposals to extend it, for example in the 2021 Build Back Better bill, did
not become law; from memory). A coin seller can sell and buy back the same day. So coins carry
the year-end selling, if any, but should not show the delayed buy: a built-in placebo.

### Literature check

Tags as in wide-6. `[search summary]` = what a web search's result summary said, not read in
the source.

- **Reinganum (1983)**, "The anomalous stock market behavior of small firms in January:
  empirical tests for tax-loss selling effects", Journal of Financial Economics 12(1),
  pp. 89-104. `[record]` Losers of the year earn high returns in the first January days; the
  tax-loss story explains part of the small-firm January premium, not all.
- **Chan (1986)**, "Can tax-loss selling explain the January seasonal in stock returns?",
  Journal of Finance 41(5), pp. 1115-1128. `[record]`
- **Grinblatt and Keloharju (2004)**, "Tax-loss trading and wash sales", Journal of Financial
  Economics 71(1), pp. 51-76 (NBER working paper 8745, 2002). `[search summary]` Finnish
  investors, where no wash-sale rule applies: losers are sold in December and bought back at
  once; the repurchase rate rises with the size of the loss and the nearness of the sale to
  the year end.

No study found that looks for the rebound on day 31 under the US rule; the 30-day shift is our
own derivation and no run here has cut returns by it. The years that can judge it fully are
2026 on (wide-6). Inside train, the gate asks for the effect in two halves with different
harvesting technology: **in-sample = tax years 1993-2011, post-sample = tax years 2012-2024**
(the window of tax year y falls in January-February of y+1; tax year 2025 needs bars after
train and is not read).

### Decision rule (fixed and pushed before any number)

Nothing below may change after the script's first run.

**Assets.** The 21 cached ETFs (dividend-adjusted closes, `research/data/adj/`: SPY, QQQ, IWM,
the nine sector SPDRs, EFA, EEM, VNQ, TLT, IEF, LQD, GLD, SLV, DBC) and, as the placebo, the
eight cached coins (BTC, ETH, LTC, XRP, BCH, ETC, DASH, XLM; daily closes). Train bars only.

**Unit.** One asset in one tax year y, if the asset has a close on or before the last trading
day of December of y-1 and the whole window below inside train.

**Dose.** YTD = log(close on the last bar of November y / close on the last bar on or before
31 December y-1). **Loss** L = max(0, -YTD). (Dividend-adjusted closes: the dose is a total
return, a little above the price loss a holder books; immaterial for a cross-section.)

**Selling date** S = the third Friday of December of y (the quarterly expiry, near the end of
the selling season). **Echo window** = calendar days S+31 .. S+45: the return R from the last
close on or before S+30 to the last close on or before S+45 (log). For S between 15 and 21
December, that is about mid-January to early February.

**Regression.** Pooled over asset-years, year fixed effects (so the common market move of each
window drops out), R = a(y) + b L + e, standard errors clustered by year (scores summed within
each year, no small-sample correction). ETFs and coins in separate regressions.

**Gate.** Pass only if, for the ETFs, **b > 0 with t >= 2 in both periods** (tax years
1993-2011 and 2012-2024), **and** the coins' b over 2013-2024 is below the ETFs' b over all
years (the placebo must not show the same echo). On a pass: a card for a `tsmom12` overlay
(idle cash into the November losers among the ETFs for the echo window), a train test with
rows in `tries.md`, read at p < 0.00147. On a fail: W14 dead by the gate, no card, no row.

**Shown, not gating.** The same regression on: the turn-of-year window (last close of December
y to the last close on or before 10 January y+1), where the classic January rebound sits and
where the US rule says the sellers cannot yet buy back; a late placebo window S+46 .. S+60;
the continuous YTD return in place of L; ETFs without year effects; each half for the coins;
the count of asset-years with L > 0 per period.

**My guess before any number.** ETF funds are diversified and liquid; tax-loss selling of
them is small next to their daily volume, and the January rebound of losers has faded since
the 1990s. Echo-window slope between -0.05 and +0.10 (a 20% loss adds at most 2% over two
weeks), |t| < 1.5 in each half; coins noisy in both directions. Chance the gate passes: 3%.

### What came out (one run, 2026-11-18; table `results/wash-sale-echo.md`)

**The gate fails. No echo on day 31: the ETF slope of the S+31..S+45 return on the November
loss is -0.003 (t -0.07) in tax years 1993-2011 and +0.023 (t 0.43) in 2012-2024, and the coin
placebo's slope (+0.049) is above the ETFs' (+0.006). W14 `wash-sale-echo` is dead by the gate:
no card, no strategy, no `tries.md` row.**

| Window (ETFs, slope on the loss, t by year) | Tax years 1993-2011 | 2012-2024 |
|---|---:|---:|
| Echo S+31..S+45 (gate) | -0.003 (-0.07) | +0.023 (0.43) |
| Turn of year 31 Dec..10 Jan (shown) | +0.043 (0.98) | +0.089 (3.91) |
| Late placebo S+46..S+60 (shown) | -0.154 (-4.09) | +0.112 (2.48) |

500 ETF asset-years (139 with a loss, 31 tax years); 58 coin asset-years (18 with a loss).

- **A 20% November loss adds nothing on days 31-45** (0.5% at most, in either half). If US
  harvesters of ETFs buy back after the 30-day bar, their buying does not move these funds.
- **Where a loser rebound does show, it is the classic turn of the year, not the echo:** a 20%
  loss went with +1.8% over 31 Dec..10 Jan after 2012 (t 3.9), +0.9% before (t 1.0). That is
  Reinganum's January effect on funds, in the window where the US rule says the sellers cannot
  yet be the buyers. It is a shown cell, seen now, so it is a lead and not a result.
- **The year-clustered t is fragile:** the late placebo window, which no story predicts,
  gives t -4.1 before 2012 and +2.5 after, with opposite signs. With 13-18 year clusters and
  half the losers concentrated in 2001, 2002, 2008 and 2022, a t of 3 to 4 in one cell is
  within what this design throws up by chance. The turn-of-year +3.9 must be read with that.
- **Coins:** too few asset-years for any test (12 before 2019, 46 after). The 2013-2018 cell's
  t is meaningless (most years hold one or two coins, so year effects leave almost no residual).
  Coins go the other way at the turn of the year (-0.086, t -3.2): coin losers keep falling
  into January.
- **Compared with my guess:** echo slope between -0.05 and +0.10 with |t| < 1.5 in each half:
  yes (-0.003, +0.023). 3% chance of a pass: no pass.

Disclosures: one dry run (`DRY=1`) printed only asset-year counts per sample (above), then one
run. The script and its tests were pushed before both (commit 6e0d283). The first tax year
with data is 1994 (SPY starts 1993-01-29), not 1993 as the rule's label says; nothing else
differs from the rule.

## Step 2. W13 `festival-gold` (anthropology of calendars)

### The idea

Households and jewellers in India buy gold before Dhanteras (two days before Diwali; the day
on which buying gold or metal is customary) and in China before the Lunar New Year. Both
festivals sit on a lunisolar calendar, so their Gregorian dates walk by about 11 days a year
and jump back by a month every two or three years: Diwali falls between 17 October and 14
November, the Lunar New Year between 21 January and 20 February. If festival buying moves the
gold price, the move must follow **event time** (the weeks before the festival, wherever it
falls), not **calendar time** (a fixed month). A plain monthly seasonal cannot tell the two
apart; the drift can.

### Literature check

- **Baur (2013)**, "The autumn effect of gold", Research in International Business and
  Finance 27(1), pp. 1-11, DOI 10.1016/j.ribaf.2012.05.001. `[search summary]` Daily gold
  spot and futures, January 1981 to December 2010: September and November are the only months
  with significantly positive returns (about +2.2% and +1.8% on average, as a secondary source
  quotes; not checked in the paper). Explanations offered: Indian wedding-season jewellery
  demand, hedging before the "Halloween" stock season, lower sentiment with shorter days. A
  calendar-month study: it did not separate festival dates from months.
- **Potrykus and Augustynowicz (2024)**, International Journal of Management and Economics
  60(3), pp. 157-172. `[search summary]` A later replication: the autumn effect in gold has
  reversed and been replaced by a winter effect.

So the calendar-month version held in its paper's years and, by one replication, not after.
The event-time cut is our own and no run here has computed it. GLD starts 2004-11-18 (the
monthly gold series in the cache is monthly only, useless for event time), so **in-sample =
GLD's days to 2010-12-31 (inside Baur's sample), post-sample = 2011-01-01 to 2025-11-10**.
The years that can judge it fully are 2026 on.

### Festival dates

Lakshmi Puja (Diwali) and Lunar New Year dates 2004-2025 written from memory into the script
(`research/lib/wide7_festival.py`), then checked against wide-6's mean new moons before any
price was read: all 21 Lunar New Year dates fall 0 or 1 day after a mean new moon (UTC; China
keeps UTC+8), and all 22 Diwali dates 1 or 2 days before one (one at 2), as the calendars
require (Diwali is the new moon of Ashvin/Kartika in Indian time). Correction made before any
price was read: 6 Diwali dates fall on the mean new moon, 15 one day before, 1 two days
before (the line above first misread the check). The 2025 Dhanteras (18
October) and Diwali (20 October) were confirmed in news reports; no full published table was
fetched (Wikipedia's pages list only recent years). Dhanteras = Diwali minus 2 days. A date
off by one day moves one session at each end of a 15-session window.

### Decision rule (fixed and pushed before any number)

**Series.** GLD dividend-adjusted closes, train bars only; daily log returns, 2004-11-19 to
2025-11-10.

**Event days.** E(t) = 1 if day t is one of the 15 trading sessions strictly before a festival
day F (Dhanteras for Diwali; the Lunar New Year day itself), else 0. Both festivals in one
indicator. (Gold buying is done before the day; the price on the day itself is not counted.)

**Regression.** r(t) = sum over the 12 calendar months of c(m) Month(m, t) + b E(t) + e;
Newey-West t with 10 lags. b is the extra daily return on festival-run days over the same
calendar month's mean: event time against calendar time.

**Gate.** Pass only if all three hold: (1) b > 0 with t >= 2 over the whole GLD sample;
(2) b > 0 in both the in-sample (to 2010) and the post-sample (2011 on) periods;
(3) the true dates rank in the top 3 of 15 shifts of all festival dates by k weeks,
k = -7 .. +7 (same regression for each). On a pass: a card for an overlay (idle cash into GLD
for the 15 sessions before each festival), a train test with rows in `tries.md`, read at
p < 0.00147. On a fail: W13 dead by the gate, no card, no row.

**Power, written before any number.** GLD's daily standard deviation is about 1.1%; about 600
of about 5,250 days are festival-run days, so the standard error of b is about 5 bps a day and
t >= 2 needs about 10 bps a day, 1.5% over a 15-session run. Baur's September mean is about
10 bps a day over a whole month, so the gate can see a festival effect only if it carries most
of the autumn effect.

**Shown, not gating.** b for each festival alone; b without the month terms (the raw festival
run); a 5-session run; mean GLD return by calendar month in each period (Baur's September and
November, out of his sample from 2011); the 15 shifted b values.

**My guess before any number.** b between -3 and +6 bps a day, t below 1.5; September and
November not special after 2010 (the replication). Chance of a pass: 3%.

### What came out (one run, 2026-11-18; table `results/festival-gold.md`)

**The gate fails on all three counts: festival-run days minus their month's mean -1.9 bps a
day (t -0.30) over 2004-2025, -8.6 to 2010 and +1.1 from 2011, rank 10 of 15 weekly shifts.
W13 `festival-gold` is dead by the gate: no card, no strategy, no `tries.md` row.**

| GLD, bps a day (t) | All 2004-11..2025-11 | To 2010 | 2011 on |
|---|---:|---:|---:|
| Both festivals, 15 sessions, month terms (gate) | -1.9 (-0.30) | -8.6 (-0.64) | +1.1 (0.16) |
| Dhanteras only | +0.9 (0.09) | -8.2 (-0.37) | +5.3 (0.49) |
| Lunar New Year only | -4.4 (-0.58) | -9.0 (-0.55) | -2.8 (-0.34) |
| Both, no month terms (raw run) | +2.9 (0.57) | -3.3 (-0.25) | +5.4 (1.13) |

- **No festival run in gold.** Neither festival shows one alone, before or after 2010; the
  true dates sit mid-pack among dates moved by up to seven weeks (shifted values from -4.9 to
  +6.9 bps a day; the true -1.9 ranks 10 of 15).
- **Baur's autumn effect is gone out of his sample, and reversed.** In GLD's years inside his
  sample (2004-11 to 2010), September and November are the two best months (+22 and +29 bps a
  day, about +4.6% and +6.2% a month). From 2011 they are among the worst (-8.6 and -6.6).
  January is the one month that stays strong in both (+19, +14), in line with the 2024
  replication's "winter effect"; that is a seen calendar mean, not a lead (a fifth published
  calendar effect gone after publication: `fomc-cycle`, `xtsmom`, pre-FOMC drift, lunar,
  autumn gold).
- **Compared with my guess:** b between -3 and +6 with t below 1.5: yes (-1.9, -0.30).
  September and November not special after 2010: yes, they turned negative. 3% chance of a
  pass: no pass.

Disclosures: one dry run (`DRY=1`) printed only day counts (5,277 days, 630 festival-run
days; 180 to 2010, 450 from 2011), then one run. Script and tests pushed before both (commit
ce01544).

## Step 3. W12 `rmd-december` (demography)

### The idea

US owners of traditional IRAs and 401(k)s must withdraw a required minimum distribution
(RMD) each year once past a legal age: the account at the end of the previous year divided by
a life-expectancy divisor (about 27 at the starting age, so about 4%). Many take it late in the
year, and an RMD from a fund account is a sale of fund shares. A cohort crossing an age line
on a fixed date is a demographer's flow (a Lexis diagram); here the flow is a forced sale with
a deadline of 31 December.

The decisive cut is not the December mean (the turn of the year and the "Santa" rally sit
there) but **the two years in which the law waived RMDs: 2009 (Worker, Retiree, and Employer
Recovery Act of 2008) and 2020 (CARES Act)** (from memory; both well documented). If RMD
selling depresses late December, late December should be stronger in those two years than in
the others.

### Literature check

None found in this run on RMD flows and December returns; not searched beyond the tax-loss
literature of step 1. The idea is our own (wide-6) and no run here has cut returns by waiver
years. The years that can judge it fully are those after the next start-age step (73 to 75
in 2033).

### Decision rule (fixed and pushed before any number)

**Series.** SPY (dividend-adjusted, Decembers 1993-2024) primary; TLT (Decembers 2002-2024)
second. Train bars only (December 2025 is not in train).

**Statistic per year y.** Window = the last ten trading sessions of December y: log return
from the close of the eleventh-last December session to the last December close. **Excess**
X(y) = window return minus 10 times the asset's mean daily log return over the other sessions
of year y (so a strong year, as 2009 and 2020 both were, does not count as a strong window).

**Gate statistic.** D = mean X over the waiver years {2009, 2020} minus mean X over the other
years. Exact permutation p = share of all pairs of years whose mean X is at or above the
waiver pair's (one-sided: RMD selling predicts D > 0).

**Gate.** Pass only if, for SPY, D > 0 with p <= 0.05 (the waiver pair in the top 5% of the
496 pairs), **and** TLT's D > 0. On a pass: a card for an overlay (late-December exposure
scaled by an RMD dose) with rows in `tries.md`, read at p < 0.00147; with two waiver years in
train, a pass would mostly say "watch the next waiver or start-age step". On a fail: W12 dead
by the gate, no card, no row.

**Shown, not gating.** The same for the S&P 500 index (GSPC, no dividends) over Decembers
1975-2024 (IRAs from 1975 under ERISA); X for SPY and TLT in each waiver year and its rank;
the first ten December sessions as a within-month placebo; the raw (not excess) window.

**Power, written before any number.** SPY's ten-session standard deviation is about 3.5%; with
two waiver years the standard error of D is about 2.5%, so p <= 0.05 needs D of about 4 to 5%
in ten sessions: far larger than any plausible RMD effect (US RMDs are of the order of a few
hundred billion dollars a year, spread over months, against tens of trillions of US
equities). The gate can only find a very large effect.

**My guess before any number.** D for SPY between -1.5% and +1.5%, p between 0.2 and 0.8; TLT
either sign. Chance of a pass: 2%.

### What came out (one run, 2026-11-18; table `results/rmd-december.md`)

**The gate fails: in the two RMD waiver years SPY's last ten December sessions were 0.06
points weaker, not stronger, than in the other years (excess D -0.06%, permutation p 0.51);
TLT likewise (-0.18%). W12 `rmd-december` is dead by the gate: no card, no strategy, no
`tries.md` row.**

| Series, Decembers | D, last ten sessions, excess (p) | 2009 rank | 2020 rank | First ten (placebo) |
|---|---:|---:|---:|---:|
| SPY 1994-2024 (gate) | -0.06% (0.51) | 20 of 31 | 11 of 31 | +1.07% (0.31) |
| TLT 2003-2024 | -0.18% (0.59) | 15 of 22 | 12 of 22 | -3.37% (0.89) |
| S&P 500 index 1975-2024 | -0.31% (0.57) | 35 of 50 | 19 of 50 | +1.02% (0.33) |

- The waiver years sit in the middle of the pack for every series: one above and one below
  the median for SPY, both below it on the index. Taking the RMD flow away for a whole year
  did nothing visible to late December.
- Read as power, not proof: with two waiver years the gate could only see an effect of about
  4-5% in ten sessions (written before the run). What it rules out is a late-December RMD
  effect large enough to trade.
- **Compared with my guess:** D between -1.5% and +1.5% with p 0.2-0.8: yes (-0.06%, 0.51).
  2% chance of a pass: no pass.

Disclosures: one dry run (`DRY=1`) printed only the year counts and the waiver years present,
then one run. Script and tests pushed before both (commit a2fafc4). The rule says Decembers
1993-2024 for SPY and 2002-2024 for TLT; each fund's first December has no close before
1 January of that year, so the samples start in 1994 and 2003 (31 SPY years: 465 pairs, not
the 496 the rule's text implied).

## Step 4. Two new mechanisms for the queue (not tested)

Written after the three gates, before any number on these two. Fields already used (the
`ideas.md` field column and `wide-1.md`): ecology, epidemiology, signal processing, control,
information theory, evolutionary game theory, statistical physics, queueing and reliability,
neuroscience, immunology, physics of pinning, hydraulics, astronomy and chronobiology,
seismology, Kelly, pharmacokinetics, actuarial science, materials fatigue, metrology,
behavioural ecology, topological data analysis, econophysics, demography, anthropology of
calendars, tax law, catastrophe meteorology, plus the finance and ML families. Two fields not
yet used: **heliophysics** and **software release engineering**.

| # | Field x tool | Mechanism in markets | Dose that should scale | Gate (event study first) and the years that can judge it | Prior |
|---|---|---|---|---|---|
| W16 `geomagnetic-storm` | heliophysics x the planetary geomagnetic index (Kp/Ap: a 3-hourly measure of how hard the solar wind shakes Earth's magnetic field; storms cluster near solar maximum on the 11-year cycle) | Krivelyova and Robotti (2003, Federal Reserve Bank of Atlanta working paper; from memory, check) report lower stock returns in the days after severe geomagnetic storms, through mood (storms are linked in medical studies to depression and sleep disruption). A physical clock no trader sets, with no calendar collision | The storm's daily Ap index (G1 to G5 on NOAA's scale); a dose-response is required: severe storms (Ap >= 100) must matter more than minor ones. Daily Kp/Ap since 1932 from GFZ Potsdam (keyless file; check) | SPY and the S&P 500 index excess return over the six sessions after storm days, regressed on Ap, against the same weekdays in calm weeks. The paper's sample ends about 2000; **post-sample train years 2003-2025 include solar cycles 24 and 25 (the May 2024 G5 storm)**, so the gate can run on train now; 2026 on (cycle 25's decline) after that | 1% |
| W17 `fork-premium` | software release engineering x scheduled releases with a fixed activation block (a release date set in code months ahead; a change with known scope) | Before a scheduled Ethereum network upgrade (about 18 since 2016: Byzantium, London, the Merge, Dencun, Pectra, ...) holders face a known date of protocol risk; a premium for that risk should show as a run-up into a well-tested upgrade and a fall after it ("sell the news"), larger when the upgrade changes the coin's supply (issuance cut, fee burn, proof-of-stake) than when it only fixes gas costs | The upgrade's scope, fixed before the date from its public specification: 1 if it changes issuance or consensus (Byzantium, Constantinople, London, the Merge, Shapella), 0 otherwise; the number of included improvement proposals as a second dose. BTC soft forks (SegWit 2017, Taproot 2021) as a second, tiny calendar | ETH excess over BTC over the 10 days before and the 10 days after each upgrade's activation, regressed on scope. About 18 events: weak. The unseen years are Fusaka (2025-12, just after train) and the 2026 upgrades on | 1% |

Neither is carded; each needs its gate first, as W11-W15 had.

## Family count

68 carried in; W12, W13, W14 closed by gates (gates do not raise the tested count); W16 and
W17 added. **70 mechanisms, 16 tested by a strategy, none passed. The next strategy test is
read at p < 0.10 / 70 = 0.00143.** Gates run so far: ann-1 (1), wide-6 (2), wide-7 (3), all
failed.

## What wide-7 adds

- **Three more ideas closed for the price of an event study, without spending the bar.** Each
  gate's rule, script and tests were pushed before any number; each ran once after a dry run
  that printed counts only. All three failed clearly and all three matched the guess written
  before the run.
- **The US wash-sale rule leaves no echo in ETF prices:** a 20% November loss adds nothing in
  days 31-45 after the selling peak (-0.003 and +0.023 per unit of loss in the two halves).
  The loser rebound that exists in funds is at the turn of the year after 2012 (t 3.9 by year
  clusters; a placebo window shows t of 2.5 to 4 too, so this is a lead, not a result).
- **Gold has no festival run; its published autumn effect reversed after its paper.** In
  GLD's years inside Baur's sample September and November were the best months (+22 and +29
  bps a day); since 2011 they are among the worst (-9 and -7). Published calendar effects are
  now 0 for 5 after publication here.
- **RMD waiver years look like any other December.**

## Status (2026-11-18)

**Done:** three gates (W14, W13, W12: rules, scripts, tests, one run each, write-ups), two
new mechanisms (W16, W17), the list, `ideas.md`, `next-steps.md`. No card, no strategy, no
`tries.md` row (gates get none). Held-out year untouched. Draft PR #81 (`wide-7` ->
`wide-6`).

**Doing:** nothing half-finished. No process running.
