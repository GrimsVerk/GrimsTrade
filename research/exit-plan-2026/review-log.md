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

Report integration, commit c1e0f39 (section numbers below are the new ones: 1 Summary,
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
  papers, Burry's +489% page. Backed by `lanes/report-sections-ABC.md` (4d67302) and
  `lanes/gsy-replication.md` (from gsy-1 35d155f).
- Item 1 (OBX in EUR) -> 2007-09 -61.7% (own max drawdown -69.6%), Lehman -54.2%, 2020 -42.2%,
  2022 -9.0% vs S&P -13.1%, Aug 2024 -6.6%, 2025 -8.5%; "more than the S&P in the deep crashes,
  less in 2022/2024/2025" -> summary, 4 (row 3), 5.3, 10.1 (Oslo row, bug noted). Backed by
  haven 12a3748 (`lanes/haven.md` correction, `lanes/haven-table.md`).
- Items 2 and 5 (sample fit per holding; stale 0.05% reading) -> summary step 1 and bullet 2
  rewritten per holding; 6.1 gains the per-holding table (Oslo = card `late`, which uses US CAPE
  so = `runup`; S&P/Nasdaq = post-hoc `now-like`), the drift cost of selling US/tech in full
  (about 0.7-1.4% of the portfolio vs staged-half; about 0.1% or less vs the tested rule) and the standalone `trig-sma200`
  fail in `late`; 6.2 step 1 phrased relative to the investor's start day with the exact tested rule
  (half at day-0 close, rest the day after the first close below from day 0, else day 22; closes
  before day 0 ignored; "sell all" moves half one day earlier; recross case); 5.1 says which
  closes, adds the `bt_now.py --fetch` refresh line, sma10m "in" = decision in force from 30 Oct;
  10.3 trig-vix `late` from 1990 only; 10.2 card-times correction (amendment 2) and post-hoc
  rows. Backed by bt 50c680f ("Review round 1 fixes").
- Item 3 (fund settlement) -> summary step 2, 6.2 steps 0-4 (fund cut-offs, "next trading day"
  = before the cut-off, watch to Thu 10 Dec for funds, date table by holding type and platform
  with a stated platform assumption, Norges Bank open 31 Dec but funds closed 24/25/31 Dec and
  global funds 28 Dec), 6.3 (US-share commission and FX at a non-euro broker; limit orders for
  thin Oslo stocks), 6.4 checklist, 10.4 updated, sources added. Backed by park
  4a0cd42 (`lanes/park.md` section 7).
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

Reviewed `report.md` at cfb50fe (branch `research/exit-1`), with `review-log.md` read first. None
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
     `staged-24` is a bet that a real bust comes. That fits the investor's stated AI-bubble
     belief, but in the test it cost more in the typical case and in the bad tail. Make the same
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
  (about EUR 5,000 implied). State the formula.
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
