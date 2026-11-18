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
