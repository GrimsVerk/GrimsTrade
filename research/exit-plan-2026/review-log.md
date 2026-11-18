# Review log

Review loop: a fresh reviewer with no context (Opus, high effort, never the author)
reviews `report.md`; verdict `FINAL` or `CHANGES` with a list. On `CHANGES` every item is fixed
(the missing work done, not just reworded) and logged here; then a new fresh reviewer, given the
earlier rounds' requests. Max 5 rounds; if round 5 still says `CHANGES`, the open points go to the
CoS.

## Round 1 (2026-11-18 ~19:40 UTC, fresh Opus reviewer, high effort): CHANGES

Reviewed `report.md` at commit after "merged report draft for review round 1".

Required:
1. OBX-in-EUR figures wrong: `scripts/haven_crash_table.py` (~l.297) builds NOK/EUR as
   `v / usd_per_eur`; correct is NOK/USD x USD/EUR. Reviewer recomputed 2007-09: -61.7% (not
   -69.2%), own max drawdown -69.6% (not -80.5%). Every OBX-in-EUR cell affected; USD->EUR
   conversion is fine. Fix script, rerun, update haven-table, haven.md, report (summary, 2.3, 7.1).
2. "Past states like this one" uses the `late` sample (index within 5% of high), which no longer
   fits the US (S&P -6.1%, Nasdaq -11.9%). Post-hoc `now-like` (bt.md): S&P hold-to-fallback
   P(>5% worse) 10.7%, staged-half 1.7%, mean drift from waiting +1.43% (median +2.25); Nasdaq
   staged-half p5 -5.0, staged-half-sma200 -4.8; standalone `trig-sma200` fails in `late` (p5
   -5.57). Fix: per holding, which sample applies (Oslo ~ late/runup; note Oslo `late` uses US
   CAPE = runup); US/tech only post-hoc `now-like`; show both; state the expected-drift cost of
   "sell all US now" (~0.7-1.4% of the portfolio) and that it rests on a post-hoc combination.
3. Fallback dates assume T+2 exchange trades; funds (a likely holding) settle via fund manager
   cut-offs, 1-5 working days (a broker FAQ), 2-6 days for non-Nordic funds; no Oslo settlement
   24-25 Dec. Fix: research fund settlement on common retail platforms, state the platform
   assumption, give a separate earlier fund fallback (~Fri 11 Dec, before cut-off) and fund
   last-safe day; "next trading day" = "before the fund's cut-off" for funds.
4. Literature first and most, then investors, not visible in the report (no literature or
   investor section; breadth/concentration and sentiment indices not discussed; Goetzmann, GSY
   probabilities/features, trend evidence absent; Druckenmiller/Klarman/Templeton/Robertson only
   in 7.5). Fix: compact literature section (indicators with horizon and evidence quality incl.
   breadth and sentiment, ranked shortlist with thresholds, haven literature) and investor
   section (action vs talk table, lessons) before the playbook; show how the playbook follows;
   commonly heard ideas last.
5. "Sell all US now" rests on a 0.05% reading (17 Nov) that will be stale; tested rule sells all
   only if still below the line at day 0. Fix: rerun `bt_now.py` on the finalisation day, update
   section 2 and every date; phrase Step 1 relative to the investor's start day; say what to do if
   the index recrossed.

Optional (to do where cheap): card timestamps (exit-rules card says ~19:30/~20:30 UTC, commits
18:50/19:01); 5.1 omits 1937-02 tie; SOX at GSY flag needs net-of-market too; LVNAV "outflows"
not "lost"; Berkshire chair (Buffett stays chairman, Abel CEO from 2026-01-01; resolve row);
trig-vix `late` stats cover 1990 on only; `bt_now.py` sma10m False vs report "In"; Norges Bank
settlement open 31 Dec; US-share commission + FX fee at a non-euro broker; mark Brunnermeier-Nagel
Sept 1999 unverified inline; order type for thin Oslo stocks (limit near bid); 2025 first-day
return 29.3%.

Checked and correct (do not redo): weekdays and Oslo calendar; broker price list and fee
arithmetic, FX quote; `bt_window.py` Part A tables reproduce, timing and CAPE lag correct;
`bt_now.py` readings reproduce; card-before-numbers order in git and tries.md (208 rows =
108 + 68 + 32); re-entry figures and levels; historical checks (Greenspan, +97% since 2021,
Buffett op-ed, Fed first cuts, VIX 80.9); Berkshire 2000-02; Ritter IPO data; DNB (Dutch
central bank) on ATB;
ECB LVNAV; IEGE; USD->EUR conversion; proportionality and framing.

### Changes made after round 1

(filled in by the lead as fixes land)

Report integration (section numbers below are the new ones: 1 Summary,
2 Literature, 3 Investors, 4 How the playbook follows, 5 Readings, 6 Playbook, 7 Parking,
8 Re-entry, 9 Ideas assessed, 10 Cannot settle, 11 Sources).

- Item 4 (literature and investors first) -> drafted sections A-C inserted as 2, 3, 4 after the
  Summary; old 2-8 renumbered to 5-11 and every "section N" reference updated (inside 2-4 too);
  old 3.1 bullet "What the literature and the investors add" cut to a pointer to 4; inside 2-4:
  OBX 2007-09 now -62% in euros, LVNAV "outflows", gsy replication cited to
  `lanes/gsy-replication.md` (and 20 -> 19 rebound episodes 1933-35, counted in that file),
  SOX flag marked raw-only, C rows updated for per-holding step 1 and fund dates; 11.1 map rows
  for 2, 3, 4; gsy file and overlay write-up in 11.2; 10.5 gains Kritzman-Turkington (summary),
  practitioner concentration, Fisher-Statman, Cochrane R², Bouman-Jacobsen, the from-memory
  papers, Burry's +489% page. Backed by `lanes/report-sections-ABC.md` and
  `lanes/gsy-replication.md` (from gsy-1 35d155f).
- Item 1 (OBX in EUR) -> 2007-09 -61.7% (own max drawdown -69.6%), Lehman -54.2%, 2020 -42.2%,
  2022 -9.0% vs S&P -13.1%, Aug 2024 -6.6%, 2025 -8.5%; "more than the S&P in the deep crashes,
  less in 2022/2024/2025" -> summary, 4 (row 3), 5.3, 10.1 (Oslo row, bug noted). Backed by
  haven lane (`lanes/haven.md` correction, `lanes/haven-table.md`).
- Items 2 and 5 (sample fit per holding; stale 0.05% reading) -> summary step 1 and bullet 2
  rewritten per holding; 6.1 gains the per-holding table (Oslo = card `late`, which uses US CAPE
  so = `runup`; S&P/Nasdaq = post-hoc `now-like`), the drift cost of selling US/tech in full
  (about 0.7-1.4% of the portfolio vs staged-half; about 0.1% or less vs the tested rule) and the standalone `trig-sma200`
  fail in `late`; 6.2 step 1 phrased relative to the investor's start day with the exact tested rule
  (half at day-0 close, rest the day after the first close below from day 0, else day 22; closes
  before day 0 ignored; "sell all" moves half one day earlier; recross case); 5.1 says which
  closes, adds the `bt_now.py --fetch` refresh line, sma10m "in" = decision in force from 30 Oct;
  10.3 trig-vix `late` from 1990 only; 10.2 card-times correction (amendment 2) and post-hoc
  rows. Backed by bt lane ("Review round 1 fixes").
- Item 3 (fund settlement) -> summary step 2, 6.2 steps 0-4 (fund cut-offs, "next trading day"
  = before the cut-off, watch to Thu 10 Dec for funds, date table by holding type and platform
  with a stated platform assumption, Norges Bank open 31 Dec but funds closed 24/25/31 Dec and
  global funds 28 Dec), 6.3 (US-share commission and FX at a non-euro broker; limit orders for
  thin Oslo stocks), 6.4 checklist, 10.4 updated, sources added. Backed by park
  lane (`lanes/park.md` section 7).
- Optional: 1937-02 tie added to 8.1 ("1.0-3.3 times"); SOX raw-only flag (2.1, 5.1); LVNAV
  "outflows" (2.4, 7.2); Berkshire chair resolved to the sourced state (Buffett chairman, Abel
  CEO from 1 Jan 2026; AP via NY1 28 Feb 2026, in inv), TIKR claim marked unconfirmed (9.2,
  10.1, 11.2); Brunnermeier-Nagel Sept 1999 "detail unverified" inline (2.2) and the old 3.1
  mention removed; 2025 first-day return 29.3% just under 30% (9.1); Norges Bank 31 Dec, US-share
  fees, order type (6.2, 6.3); trig-vix coverage and card times (10.2, 10.3).
- Readings not yet refreshed: still the 17 Nov US / 18 Nov Oslo closes, stated as an example
  (5.1); the lead refreshes after the 18 Nov US close.

Lead, 2026-11-18 21:15 UTC (review item 5, final refresh): reran `bt_now.py --fetch` after the
18 Nov US close and updated the readings (summary, 5.1, 5.2, 6.1/6.2 examples, checklist, 8):
S&P 7,323.63, 0.31% below its 200-day average (2 closes below), Nasdaq 2.9% below, URTH 1.0%
below, OSEBX 3.2% above, VIX 24.3, VIX/VIX3M 1.007, HYG/LQD +0.53% vs 200-day. No state
changed versus 17 Nov; the 17 Nov numbers are kept in one dated line in 5.1.

## Round 2 (2026-11-18 ~22:10 UTC, fresh Opus reviewer, high effort): CHANGES

Reviewed `report.md` at 2d7f134 (branch `research/exit-1`), with `review-log.md` read first. None
of round 1's fixes are undone below. Reviewer scratch output (bt_now rerun, extracted source texts) was kept outside the repo.

Required:

1. **The step 3 fund row for 5-10 days breaks the report's own assumptions, and its "last safe"
   day is not safe.** The evidence is in report 6.2, step 3. That row says "Any fund paying out
   5-10 business days after the order", with fallback Fri 4 Dec, last safe Fri 11 Dec, and
   worst-case cash in NL "Mon 21 Dec / Wed 30 Dec". The assumptions paragraph under the table
   applies one chain to every row: "the broker pays out within 2 bank days at worst; converting
   and moving ... takes 1 day". The 2-5 and 2-6 rows use "paying out" to mean cash at the broker,
   with the 2 payout days still to come (park 7.3: D+5 -> +2 -> +1 = D+8).
   - The 5-10 row comes from park 7.3, which counts it differently: "Slow platform (5-10 days):
     cash worst D+10 -> euro account +1. Worst = D+11". That count drops the 2 broker-payout
     days. The same verb therefore means two different things in adjacent rows.
   - Under the stated chain, Fri 4 Dec gives D+10 = Fri 18 Dec, then payout on Mon 21 and Tue 22,
     and cash in a euro account on **Wed 23 Dec**, not Mon 21.
   - Under the same chain, Fri 11 Dec gives D+10 = Tue 29 Dec (Wed 30 for a global fund that
     skips 28 Dec). Adding 2 payout days and 1 transfer day puts the cash in **January 2027**.
   - Even under park's own D+11 count, a global fund that skips 28 Dec lands on Thu 31 Dec, with
     no spare day.
   - Fix: define "5-10 days" exactly (cash at the broker, or cash in your bank account). If it
     means cash at the broker, recompute: fallback Fri 4 Dec still lands Wed 23 Dec, but the last
     safe day becomes **Wed 9 Dec** (10 fund days end Wed 23 Dec; payout Mon 28 and Tue 29;
     euro account Wed 30). If it means cash in your bank, say so in the row label and add the
     global-fund 28 Dec caveat.
   - Use one verb with one meaning across all rows ("cash at the broker within N days"), and
     update the summary step 2, the checklist in 6.4 and section 4's row.

2. **Re-entry: the main rule's costs come from a different sample than the alternative's, which
   hides that the alternative did better in the sample that fits today.** The evidence is in
   report 8.2 and the summary step 5.
   - For `staged-24` the report gives "about 3-4% of 10-year wealth on average". That is the
     all-months mean (R 0.96-0.97). It then gives "median about 8% in high-valuation months;
     worst tenth 0.72".
   - For `dca12` it gives "median cost about 3%, worst tenth 0.90". Those are sample-B
     (high-CAPE) numbers.
   - In the reentry table (`lanes/reentry.md`, rules test) for sample B, the one that fits Nov
     2026:

     | Rule | Median R | Worst tenth | Share R > 1 |
     |---|---:|---:|---:|
     | `dca12` | 0.97 | 0.90 | 31% |
     | `staged-24` | 0.92 | 0.72 | 35% |

   - So in the sample that fits today, `dca12` beat `staged-24` on the median and on the worst
     tenth, which is the regret measure. `staged-24` wins only in a real bust (1.4-1.6x, a few
     episodes).
   - The report nonetheless makes `staged-24` the default. It frames `dca12` as "better if
     missing a rally would bother you more than missing a crash". But the data say `dca12` also
     had the milder bad tail.
   - Fix: give both rules side by side in the same sample (median, worst tenth, share above 1,
     and the result in real busts). Then either make `dca12` the default, or say plainly that
     `staged-24` is a bet that a real bust comes. That fits a strong view that a bubble will
     burst, but in the test it cost more in the typical case and in the bad tail. Make the same
     change in the summary step 5 and in section 4's row 5.

Optional:

- **The VIX readings were taken before the VIX close.** The refresh ran at 21:12 UTC, but VIX
  and VIX3M close at 16:15 ET (21:15 UTC), and `bt_now.py` lets US bars through from 16:10 NY.
  - My rerun at about 22:00 UTC gives VIX 24.56 (not 24.3), 1.378 times its 50-day mean (not
    1.36), and VIX/VIX3M 1.011 (not 1.007).
  - Every other reading reproduces exactly: closes, 200-day and 50-day averages, distance from
    the highs, the 10-month values, 12-month and 24-month returns, HYG/LQD +0.5%, CAPE 39.37,
    and the rule states.
  - Fix: update the summary, 5.1 and the checklist. Move the US cut to 16:20 NY, or drop
    VIX-type series before 16:20.
- **Stale Nasdaq note in 6.1.** It says "The Nasdaq at -11.85% sits at the edge ... a further
  0.2% fall puts it outside". At the 18 Nov close it is -11.49% (5.1 says -11.5%), so about a
  0.6% further fall is needed. The 2.1 table's VIX cell ("On 17 Nov: VIX 25.5") is also stale
  next to 5.1.
- **"Only euro cash never lost value" overstates the case.** 7.3 says savings, XEON/CSH and IEGE
  "kept their euro value in every crash and every window". But 7.1 lists XEON at -0.5% (2020),
  3-month Euribor cash at -0.1% (2022) and IEGE at -4.91% since launch. Better wording: "lost
  at most about 0.5% in any crash window".
- **Section 4, row 2 labels the crash figure wrongly.** It says "-5.0% to -1.4% (S&P, `late`)",
  but that figure is from all start days with a 10%+ fall (`crash-window`), as 6.1's column
  header says.
- **Summary bullet 2** says two steps "passed our pre-set test" but does not mention that the
  200-day speed-up the playbook uses is post hoc. Add three words.
- **The summary's crash list mixes currencies.** It gives the S&P 2007-09 fall as 52%, which is
  in euros, while 9.2 gives the S&P's -57% (in dollars) and Berkshire's -54% (in dollars). Say
  "(both in euros)" next to the OBX/S&P pair.
- **Funds' shorter window was not tested.** The fund fallback (Fri 11 Dec) is about trading day
  16-17, not day 22, so the six-week statistics apply only roughly. Say so in 6.1 or 10.3.
- **ETFs need a line in step 0.** An exchange-traded fund (ETF) settles like a share (T+2) and
  has no fund cut-off, so it follows the share rows. A non-expert may otherwise put it on the
  slower fund path.
- **Global fund tie-break.** If the S&P and `URTH` sit on different sides of their 200-day
  lines, say which one governs. Today both are below. `URTH` matches no tested sample (its high
  is older than 63 trading days).
- **The Berkshire round-trip cost of "0.58%" depends on the amount.** Park gives 0.5% plus EUR 4
  (so it holds for one amount only). State the formula.
- **Comparisons count.** 10.2 says "15 strategies x up to 11 sample cuts", but bt's honesty
  notes say "up to 14 sample cuts". Align them.
- **Oslo evidence is thin.** The summary's "9% to 1%" for Oslo rests on 10 spells (2013-2025).
  A clause in the summary ("10 spells") would keep the precision honest. 10.2 already says it.
- **IPO lead time.** 9.1's "lead time ... 0 to 39 months (1996 ...)" uses 1996, which is not
  one of the four years followed by a bear market within two years. Clarify what the range
  covers.

Checked and correct (do not redo):

- **Priority order.** Literature (section 2) comes first and is the largest section, then
  investors (3) with action-vs-talk, then a derivation table (4). Commonly heard ideas come last
  (9: IPO wave, Berkshire, savings account, small bonds). Tax is out of scope, and the framing
  is generic, with no personal details.
- **Readings re-fetched** (`bt_now.py --fetch`, 18 Nov close) match 5.1, 5.2 and the summary
  apart from the VIX point above: S&P 7,323.63 (-0.31% vs 200-day 7,346.55, 2 closes below,
  last cross 17 Nov). Nasdaq -2.87% (since 13 Nov). OSEBX +3.15%, OBX +1.92%, URTH -0.99%.
  Distances from highs -6.33 / -11.49 / -3.32 / -3.83. Faber month-end +3.78 / +1.81, live
  -0.26. Sample matching: Oslo `late`, S&P and Nasdaq `now-like-below200`, URTH none.
  The Nasdaq drawdown stop has been out since 2 Nov.
- **Part A tables in 6.1** match `lanes/bt.md` Part A, the amendment and "Review round 1
  fixes". That covers the `late`, `now-like` and crash-window rows, the per-holding table
  (OSEBX 9.3% -> 1.0%, S&P 10.7% -> 1.7%, Nasdaq 15.7% -> 5.0%), and the drift costs (0.71-1.02
  by the mean, 1.13-1.40 by the median; +0.06 / -0.26 in the below-the-line cuts).
- **No look-ahead in the tested rule.** In `bt_amend.outcomes_new`, the first close below the
  200-day average on day k means a sale at the close of day k+1, and closes before day 0 are
  ignored. `bt_rules` signals are shifted by 2 days. CAPE is lagged and ranked on an expanding
  window. Train period ends Nov 2025.
- **Weekdays and day counts.** `report_checks.py` reproduces them, and I checked the following:
  - Oslo trading day 22 = Fri 18 Dec counted from 18 Nov.
  - Thu 26 Nov is Thanksgiving.
  - Fri 29 Dec 2028 is a Friday, and 31 Dec 2028 a Sunday.
  - Fri 22 Apr 2022 (ATB) was a Friday.
  - The share chain (Fri 18 Dec -> Tue 29 Dec; Mon 21 -> Wed 30; Tue 22 settles Mon 28) holds.
  - The 2-5 and 2-6 day fund chains hold: Wed 16 / Tue 15 Dec -> Wed 30 Dec, and Fri 11 Dec ->
    Wed 23 / Mon 28 Dec.
- **Re-entry levels.** 6,255 / 5,473 / 4,691 are 20/30/40% below 7,819 (18 Nov close / (1 -
  6.33%) = 7,818.5). The 8% stop level of 7,193 is also right.
- **GSY (NBER w23191 full text).**
  - Turnover is elevated in run-ups that crash and in those that do not, and is "of little
    use". Sales growth does not help in the US (the abstract lists turnover, but the body
    supports the report's wording).
  - Of the 21 crashes, the peak came about 6 months and +30% after the flag.
  - The gsy-replication figures (38% / 51% / 15%, 104 / 51 episodes, 27% / 35% since 2002)
    match `lanes/gsy-replication.md`.
- **Goetzmann (2015) abstract.** "Only slightly higher" and "about 10%" after a doubling:
  confirmed.
- **Vanguard (2023) full text.** Lump sum ahead 68% of the time, 1976-2022, and "with higher
  loss aversion would be better off": confirmed.
- **Oaktree.** About $600m a week over the last 15 weeks of 2008: confirmed on the cited
  Oaktree page.
- **2026 events.** The AP 5 Nov sell-off (S&P -4.4%, Nasdaq -5.5%) and the Nasdaq Trader notice
  listing ANT for Thu 19 Nov 2026 are both confirmed.
- **Goyal-Welch-Zafirov 2024.** "Of those still significant in sample, half poor out of
  sample" is consistent with the abstract.
- **Historical numbers re-derived:**
  - Berkshire 1999 -19.9% vs S&P +21.0%; 2000-02 about +30% vs -38%; 2008 -31.8% vs -37.0%.
  - The Fed's first cuts: -42% and -56% to the lows.
  - Buffett's op-ed came 28.5% above the low.
  - The 1973-74 / 2000-02 / 2007-09 recovery months are counted from the trough.
- **Citation metadata** (journal, volume, issue) checked for about 25 papers in 11.2: no errors
  found.
- **`tries.md` count.** 226 rows dated 2026-11-18 = 208 + 18, as 11.1 states.
- **OBX-in-EUR conversion** in `haven_crash_table.py` is now NOK/USD x USD/EUR, with a range
  assertion.

### Changes made after round 2

(filled in by the lead as fixes land)

Fix agent, 2026-11-18 ~22:10-23:00 UTC. No new backtest or try (item 2 reads the existing
reentry table side by side; item 1 and the window days are calendar arithmetic in
`report_checks.py`), so no new card or `tries.md` row.

- Required 1 (fund 5-10 day row) -> 4aaf3f5. One meaning for every row: "cash at the broker
  within N business days of the order", then broker payout 2 bank days, then 1 day to a euro
  account. Re-derived with a new `sale_chains()` in `scripts/report_checks.py`, which also
  reproduces the share, 2-5 and 2-6 rows. Slow funds (5-10 days): fallback Fri 4 Dec -> euro
  account Wed 23 Dec (was "Mon 21 Dec"); last safe **Wed 9 Dec** -> Wed 30 Dec (was Fri 11 Dec,
  which lands in January 2027). A global 5-10 day fund that skips 28 Dec gives the same dates.
  The table's rows are relabelled "cash at the broker within ..."; the assumptions paragraph says
  what to do if a platform's figure means cash in the bank account. Updated: summary step 2,
  section 4 row (fallback/last safe), 6.2 step 3 table and assumptions, step 4, checklist 6.4,
  10.1 "Spare day" row, 10.4. `lanes/park.md` 7.3 corrected with a dated note (D+11 -> D+13).
- Required 2 (re-entry samples) -> cd36f74. 8.2 now shows `dca12` and `staged-24` side by side
  from `lanes/reentry-rules.txt` (10-year horizon): sample B median 0.97 vs 0.92, worst tenth
  0.90 vs 0.72, share above 1 31% vs 35%, mean 0.99 vs 0.97; from 1972 0.97/0.90 vs 0.90/0.68;
  tops before real busts 1.09-1.34 vs 1.40-1.61; sold 2-3 years early 0.88-0.93 vs 0.64-0.71;
  all months mean 0.98 vs 0.96; Nasdaq sample B 0.96/0.86/35% vs 0.89/0.69/5%. `dca12` (12
  monthly buys, January-December 2027) is now the default; `staged-24` (thirds at -20/-30/-40%,
  rest by Fri 29 Dec 2028, levels unchanged) is kept as an explicit bet that a real bust comes,
  with the cost stated. The choice of default is marked post hoc (sections 4 and 10.2).
  Updated: summary step 5, section 4 row 5 and the "chosen after seeing results" list, 8.2,
  10.2; dated note in `lanes/reentry.md`.
- Optional, VIX cut-off -> 389936f. `bt_now.py` US cut moved from 16:10 to 16:20 New York (VIX
  is cut at the S&P's last bar); reran `bt_now.py --fetch` at 22:12 UTC: VIX 24.56 (was 24.3),
  1.38 x its 50-day mean (was 1.36), VIX/VIX3M 1.011 (was 1.007), HYG/LQD +0.50% (was +0.53%).
  All index readings, sample matches and rule states unchanged. Updated: intro, summary, 2.1 VIX
  cell (was the stale "17 Nov: VIX 25.5"), 5.1; `lanes/bt.md` "Review round 2 fixes". The
  checklist carries no VIX number. ruff check and format pass.
- Optional, stale Nasdaq note -> 389936f. 6.1: -11.5% at the 18 Nov close, about 0.6% further
  fall leaves the `now-like` band (0.88 / 0.8851).
- Optional, "only euro cash never lost value" -> e1c9a28. Now "lost at most about 0.5%" (XEON
  -0.5% in 2020, 3-month Euribor cash -0.2% at worst in 2022, from negative rates) in the
  summary, 2.4, section 4 row 4, 7.3 and 9.3; 7.3 adds that IEGE was not in the crash table
  (-4.9% since launch over the negative-rate years).
- Optional, crash-list currencies -> e1c9a28. Summary: Berkshire "(in dollars)", OBX/S&P
  "(both in euros)"; same in section 4 row 3.
- Optional, smaller ones -> e476115: section 4 row 2 and the 6.1 bullet now say `crash-window`
  (all start days with a 10%+ fall); summary bullet 2 notes the 200-day speed-up is post hoc and
  Oslo rests on 10 spells (2013-2025); step 0 and the checklist say an ETF follows the share
  rows; 5.2 says the S&P 500 governs if it and `URTH` disagree (`URTH` matches no tested
  sample); Berkshire cost stated as 0.5% plus EUR 4 per round trip (7.1, 9.2) instead of
  0.58%; 9.1 IPO lead time measured from the peak-count year (1996 is not one of the four);
  10.2 comparisons "up to 14 sample cuts" as in bt's honesty notes; 10.3 notes the fund
  fallbacks are trading days 17 (Fri 11 Dec) and 12 (Fri 4 Dec), not 22, untested
  (`report_checks.py` now prints days 12 and 17).
- Report header now says "revised after review rounds 1 and 2" (this commit).
- Not done: none of the listed items skipped.

## Round 3 (2026-11-18 ~22:30 UTC, fresh Opus reviewer, high effort): FINAL

Reviewed `report.md` at 3529214 (branch `research/exit-1`), with `review-log.md` read first. None
of the round 1 or round 2 fixes are undone below, and I found no reason to doubt any item on
either round's "checked and correct" list. Scratch output (bt_now rerun, extracted PDFs) was kept
outside the repo. The repo was not modified.

Required:

None. I found no remaining error that would change what the investor does. The fund date chains
(6.2, step 3), the re-entry comparison (8.2) and the refreshed readings all reproduce from the
scripts and lane files (details under "Checked and correct").

Optional (in rough order of value):

1. **Summary step 5 overgeneralises "waiting for falls".**
   - The claim: the summary says the 12 monthly buys had "a better typical result and a milder
     bad tail than waiting for falls".
   - The evidence: in `lanes/reentry-rules.txt` (10-year horizon, sample B), the pure
     wait-for-a-fall rules had medians of 1.000 (`dd20`), 1.009 (`dd30`) and 1.000
     (`dd20-sma10`). `dca12` had 0.972. Their bad tails were far worse: p10 0.35-0.52, and `dd30`
     was never back in for 22% of months.
   - So `dca12` beats the thirds rule (`staged-24`) on both counts, but beats the no-deadline
     waiting rules only on the tail.
   - The fix: say "than buying in thirds on falls". Optionally add in 8.1 that the no-deadline
     waiting rules had a median of about 1.0 but a worst tenth of 0.35-0.52.
   - Related: 8.1's "worst tenth of 0.33-0.52" mixes samples. Sample B at 10 years gives 0.35-0.52.
     The 0.33 comes from sample A or from sample B from 1972.
   - Related: "No re-entry rule beat buying back at once" means "no rule passed the card's bar".
     `dd30`'s sample-B median is 1.009 and `dd20-sma10`'s mean is 1.008. Saying "passed the
     card's bar" once (summary or 8.1) heads off that objection.
2. **Summary step 2 does not say which fund gets which last-safe day.** It says "last safe Tue 15
   or Wed 16 Dec for a fund whose cash reaches your broker within 2-6 business days".
   - If a reader with a global 2-6-day fund picks Wed 16, the worst case misses 2026. The sixth
     fund day is Tue 29 Dec when 28 Dec is skipped, so the cash reaches a euro account in January.
   - The table in 6.2 and the checklist are correct.
   - The fix: "last safe Wed 16 Dec (cash at the broker within 2-5 days) or Tue 15 Dec (2-6 days,
     e.g. global funds)".
3. **Edge case in the `staged-24` alternative (8.2, item 2).** The test counts a month-end close
   20% or more below the high from the sale month itself on.
   - If the S&P has a month-end close at -20% or lower at end-Dec 2026, the test would buy that
     third at once. The investor cannot hold stocks on 31 Dec.
   - The fix: one clause, e.g. "a level already reached at the Dec 2026 month-end is bought on the
     first trading day of January 2027". This matches how `dca12` is shifted to January.
4. **Euribor figure differs between 7.1 and 7.3/2.4.**
   - 7.1 (savings row) says "3-month Euribor cash: at worst -0.1% over 2022". That is the
     whole-drawdown cell in `lanes/haven-table.md`.
   - 7.3 says "0.2% at worst in 2022". That is the own-max-drawdown cell, which the round 2 fix
     log also uses.
   - The fix: use -0.2% in both places.
5. **Robertson wording, lesson 1 (section 3).** "Robertson quit 20 days before he would have been
   proved right" does not match the table, which says Tiger's closure came 20 days *after* the
   Nasdaq peak. inv says "quit 3 weeks after the top". The fix: "Robertson quit 20 days after the
   top, just before the fall proved him right".
6. **The refresh command in 5.1 needs the local cache root.** Without `BT_CACHE`,
   `GRIMSTRADE_DATA` or `research/macro.local.json`, `bt_now.py --fetch` prints the index table
   and then exits with an error. It never prints the per-holding 200-day states or VIX that 5.1
   promises. The fix: one clause in 5.1 ("needs the cache root set up as in the script header;
   otherwise use a 200-day chart"). The chart fallback is already there.
7. **2028 holidays.** 8.2 says "(2028 exchange holidays not checked)", but 11.2 cites the NYSE
   2026-2028 holiday calendar. Fri 29 Dec 2028 is not on it. Either drop the caveat for NYSE or
   say "(Euronext 2028 not checked)".
8. **Lump sum as an explicit option in 8.2.** The literature (Vanguard) and the reentry table say
   that buying back at once in early January 2027 had the highest expected result. 8.2 offers
   only `dca12` and `staged-24`. One line ("highest expected value, largest regret if a crash
   follows; choose it if regret does not weigh on you") would make the choice complete. The
   report already says this implicitly in 8.1.
9. **OBX "lost less in 2022" depends on the window.** 5.3 and the summary use the S&P's 2022
   peak-to-trough window (OBX -9.0% vs S&P -13.1% in euros). By each index's own maximum drawdown
   in 2022, OBX fell more: -22.0% vs -18.0% (`lanes/haven-table.md`). One clause ("over the S&P's
   window") would keep it honest. It does not change the advice to convert promptly.

Checked and correct (do not redo):

- **Readings rerun.** I ran `bt_now.py --fetch` at about 22:20 UTC, with the cache root taken
  from another worktree's local config. Every number in 5.1, 5.2, the summary and 6.2 reproduces:
  - Index readings: S&P 7,323.63 (-0.31% vs 7,346.55; 2 closes below; last cross 17 Nov).
    Nasdaq 24,429.88 (-2.87%; since 13 Nov). OSEBX +3.15%, OBX +1.92%, URTH -0.99% (high 13
    Aug).
  - Averages and returns: 50-day -4.25 / -6.87 / -1.01 / -1.37. Distances from highs -6.33 /
    -11.49 / -3.32 / -3.83. Faber +3.78 / +1.81 / +7.24 / +6.57, live -0.26. 12-month and
    24-month returns as stated.
  - Volatility and credit: VIX 24.56 (1.378 times its 50-day mean, 92nd percentile).
    VIX/VIX3M 1.011, and the 5, 11-13 and 17 Nov ratios are as stated. HYG/LQD +0.5%.
  - Valuation: Baa 1.51, hostile above 1.946. CAPE 39.37 (98.3rd percentile; max 44.2 in Dec
    1999). Lagged CAPE 39.78.
  - Sample matching: Oslo `late`, S&P and Nasdaq `now-like-below200`, URTH none.
  - Part B rule states as in 5.1, including the Nasdaq dd8 stop out since 2 Nov.
- **Fund and share date chains (6.2, step 3).** I re-derived them by hand and with
  `report_checks.py`. The calendar assumptions: Oslo bank days skip 24-25 Dec, fund days also
  skip 31 Dec, and global funds also skip 28 Dec.
  - Shares: Fri 18 Dec -> settles Tue 22 -> euro account Tue 29 Dec. Mon 21 -> Wed 30.
  - 2-5-day fund: Fri 11 -> Fri 18 -> Wed 23. Wed 16 -> Wed 23 -> payout 28/29 -> Wed 30.
  - 2-6-day fund: Fri 11 -> Mon 21 -> Mon 28. Tue 15 -> Wed 23 -> Wed 30.
  - 5-10-day fund: Fri 4 -> Fri 18 -> payout 21/22 -> Wed 23. Wed 9 -> Wed 23 -> Wed 30. Same
    for a global fund.
  - Tue 22 Dec settles Mon 28 (no spare day). Mon 28 settles Wed 30. Wed 30 settles Mon 4 Jan.
  - Trading days 12, 17 and 22 are Fri 4, Fri 11 and Fri 18 Dec. The watch windows end Thu 3,
    Thu 10 and Thu 17 Dec.
  - The rows, summary step 2, section 4's row, the checklist and 10.1's "spare day" row agree.
  - Park 7.3 matches, including the dated D+13 correction.
  - The Dutch/TARGET side is open on 24 and 31 Dec, so the Oslo-calendar chain is conservative.
- **The two-week legal backstop for Oslo funds** (calendar days) still fits the Fri 11 Dec
  fallback (paid by Thu 24 Dec, payout 28/29, euro account Wed 30). So "the fallback is the
  plan" holds for that row.
- **The re-entry table in 8.2 against `lanes/reentry-rules.txt` (10 years).**
  - Sample B: `dca12` 0.972 / p10 0.899 / 31% / mean 0.988. `staged-24` 0.924 / 0.722 / 35% /
    0.967.
  - Sample B from 1972: 0.968/0.899 vs 0.901/0.683.
  - Named busts (1929-08, 1968-11, 1972-12, 2000-03, 2007-10): 1.09-1.34 vs 1.40-1.61.
  - Dec 1996 and Dec 1997: 0.88-0.93 vs 0.64-0.71.
  - Sample A mean 0.983 vs 0.963.
  - Nasdaq sample B: 0.959/0.859/35% vs 0.891/0.685/5%.
  - Both rules are on the reentry card's rule list. The post-hoc choice of default is stated in
    sections 4 and 10.2.
- **No look-ahead in the re-entry test.** `DD` is the month-end close over the running all-time
  high of daily closes, so the 7,819 base (6 Oct closing high) and the levels 6,255 / 5,473 /
  4,691 are the right reference. The high-CAPE flag uses an expanding 80th percentile of lagged
  CAPE. `staged-24` buys at month-end decisions only and is fully in at 24 months.
- **Weekdays checked:** Thu 19 Nov, Fri 30 Oct, Mon 30 Nov, Thu 5 Nov, Tue 6 Oct, Thu 17 Dec
  (ECB), Mon 1 Mar 2027, Fri 29 Dec 2028 (31 Dec 2028 is a Sunday).
- **Sources spot-checked this round (not checked before):**
  - Baur-Lucey WP abstract: "safe haven for stocks only for 15 trading days after an extreme
    shock"; in the body, gold is a haven for stocks but not for bonds.
  - Marks, "Is It a Bubble?" memo: "no one should go all-in ... no one should stay all-out ... A
    moderate position".
  - Grantham's "slim to none" (ThinkAdvisor, 20 Jan 2026; podcast around 19 Jan).
  - Bree-Joseph: 11 Hang Seng crashes 1970-2008, parameters in the post-hoc ranges for only 7.
  - Kritzman-Turkington via the Quantpedia summary: 49 industries, 1926-2025; "virtually none";
    the less-when-concentrated rule "reduces return and increases risk".
  - Cederburg et al. 2020: 103 equity strategies, no systematic real-time outperformance.
  - SpaceX IPO: USD 75bn, priced 11 Jun 2026, the largest ever.
  - Berkshire 2008 letter: $14.5bn in Wrigley, Goldman and GE paper (via inv's quote).
  - ECB: hikes in June and September 2026, held at 2.50% on 29 Oct, so "raising rates" is fair.
- **Internal consistency:**
  - Summary vs 6.1 per-holding numbers: 9.3->1.0, 10.7->1.7, 15.7->5.0; drift 0.7-1.4.
  - Summary vs 5.1 readings.
  - Section 4 rows vs 6.2, 7 and 8.2.
  - Checklist vs step 3 table.
  - The OBX/S&P euro crash figures in summary, 4, 5.3 and 10.1 match `lanes/haven-table.md`.
  - The Grantham "+97% by 17 Nov" figure (3,726.86 -> 7,340.53).
  - Nvidia -35.0%.
- **Priority order, scope and framing:** literature first and largest, then investors, then
  common ideas. Tax is out of scope. No personal details: percentages and generic brokers only.

### After round 3

Review loop ends: FINAL at 3529214. Optional items are polished by the lead where cheap and logged here; they do not reopen the review.

Round 3 optional items applied (each checked against the repo files first; no new backtests):

1. d0ffee7: summary step 5 now compares with "buying in thirds on falls"; 8.1 states the card's pass bar (the -30% rule's sample-B median 1.009, 51% above 1, still fails it) and gives the no-deadline waiting rules a median of about 1.0 and a sample-B worst tenth of 0.35-0.52 (was 0.33-0.52), with the -30% rule never back in for 22% of months.
2. d0ffee7: summary step 2, section 4 row and 10.1 "spare day" row now give Wed 16 Dec for 2-5-day funds and Tue 15 Dec for 2-6-day funds, matching the step 3 table and `report_checks.py`.
3. 00702f8: 8.2 item 2: a level already reached at the Dec 2026 month-end close is bought on the first trading day of January 2027 (the test's `rule_staged24` counts the sale month).
4. 3541869: 7.1 savings row now says 3-month Euribor cash -0.2% at worst in 2022 (own max drawdown cell in `lanes/haven-table.md`), as in 7.3.
5. 3541869: lesson 1 now says Robertson quit 20 days after the top, just before the fall proved him right.
6. edf29b4: 5.1 refresh note: the script needs the cache root via the git-ignored `research/macro.local.json` (copied from the committed `.example`) or `BT_CACHE`; otherwise it prints only the index table and stops; the 200-day chart fallback stays.
7. 00702f8: 8.2 caveat now reads: Fri 29 Dec 2028 is not an NYSE holiday on its 2026-2028 calendar (11.2); Euronext's 2028 calendar not checked.
8. edf29b4: 8.2 names the lump sum (first trading day of January 2027) as the plain option: higher mean than both rules (1 vs 0.99/0.97 sample B, 0.98/0.96 sample A), largest regret if a crash follows.
9. 3541869: summary and 5.3 say OBX lost less in 2022 only over the S&P's crash window (-9.0% vs -13.1%); by each index's own worst fall in 2022 OBX lost more (-22.0% vs -18.0%). 2025 holds either way (-15.1% vs -22.7% own drawdown).
