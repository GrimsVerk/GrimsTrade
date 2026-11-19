# Next steps

## Multi-signal (done 2026-11-19, branch `multi-signal`, draft PR #104 -> `survey-6`)

Descriptive IC screen of value, carry, cross-sectional momentum (AMP 2013), low-vol and BAB
(FP 2014) across the six assets against `tsmom12` (`research/multi-signal.md`; card
`cards/multi-signal.md` eb76f36 before any number; script c8715e2 before its run; table
`results/multi-signal.md`). 12 `screen` rows (`multi-signal-screen`), no strategy try, no pick.

- **Nothing is worth a card.** None passes the card's bar; none has a partial (beyond
  `tsmom12`) weekly IC near 0.10. Only XS momentum is positive: IC +0.043 (95% +0.010..+0.077),
  beyond `tsmom12` +0.035 (99.5% -0.007..+0.080), positive in all 4 eras and on the ETFs, but
  rank-correlated 0.76 with `tsmom12` (0.90 with the 12-month return): trend strength, not new.
- Value -0.018 and carry -0.023 are inside chance (0.03); low-vol -0.059 and BAB -0.055 point the
  wrong way (riskier assets earned more; the asset ordering, placebo B p 0.07-0.19).
- Breadth is the limit (4-5 assets a week, one per class). These premia need a wide long-short
  book (survey-6's live style-premia funds), an owner risk-map question.

- Doing: nothing. No process running.
- Next: (1) survey-6 next (1)-(2) stand (short-SPY/QQQ trend sleeve as insurance; defensive
  weights write-up); (2) if breadth is wanted, a descriptive screen of the same five signals on
  the out-of-universe ETFs + indexes (~16 markets, within-class ranks), not a test on the six;
  (3) nothing further on style signals within the six.
- Data: no new download. Uses the research price cache, cached FRED `DGS3MO`/`DGS10` and cached
  Binance funding zips (`<cache_root>/binance/futures/um/monthly/fundingRate/`). Rerun:
  `uv run python research/lib/multisignal_ic.py` (dry; `--log` would add rows again: don't).

## Survey 6 (done 2026-11-19, branch `survey-6`, draft PR #91 -> `survey-5`)

Which strategy families paid investors live, net of fees? 15 families, 60 live funds against
matched plain index funds (`research/survey-6.md`: list with inception, fees and mandate
changes verified; printed paper Sharpes with citations). Card before any number
(`cards/live-families.md`, dda9386), script before its run (db6eba0). Descriptive only: 15
`live-check` rows (`<family>@live-fund`) in `tries.md`; tables `results/live-families.md`.

- **No family beat its plain holding after fees** (none with gap >= +0.10 and t >= 2). The
  six long-only equity factor families (value, momentum, quality, low-vol, multi-factor,
  dividend) matched their index: gaps -0.06..+0.03, alpha t -1.6..0.9, over 14-33 years.
- Lagged: option writing -0.20 (paper indexes too: BXM -0.17, PUT -0.10), risk parity -0.30
  vs a 60/40 fund, gold miners -0.27 vs gold; tail hedges -0.54 a year; FX carry 0.
- Positive and uncorrelated: style premia long-short 0.50 (t 1.7, +28% in 2022), merger arb
  0.40 for 37 years (+14% in 2000-02, -3% in 2008-09), trend 0.17 (gained in every crash).
- Paper to live, kept: value 4%, momentum <0, dividend 8%, trend 12%, low-vol (BAB) 26%,
  style premia 31%, quality 43-63% (t 0.9), merger arb 70%; option writing and risk parity
  reversed. Median 8%.
- Card slip declared: Bonferroni for 15 is t 2.71, not 2.94; nothing reaches either.

- Doing: nothing. No process running.
- Next (judged on crash behaviour, not Sharpe): (1) a small short-SPY/QQQ trend sleeve
  (ETFs, no coin shorts) judged as insurance with this card's crash and 80/20-mix measures;
  (2) a write-up of defensive weights within the six as a drawdown choice (`risk-map.md`),
  no new test; (3) a descriptive IC screen of multi-asset style premia across the six
  (5-year reversal, carry, 12-month momentum, low vol), very low prior, project bar N 1,012.
- Data (git-ignored): `python -I research/lib/survey6_fetch.py <cache_root>` (Yahoo, French,
  AQR BAB/QMJ, CBOE BXM/PUT) into `<cache_root>/downloads/survey-6/` and
  `derived/survey-6/`. Rerun: `uv run --with openpyxl python -I research/lib/survey6_live.py
  <cache_root>` (no new rows; needs survey-5's `derived/survey-5/` too).

## Survey 5 (done 2026-11-18, branch `survey-5`, draft PR #78 -> `survey-4`)

Live track records as post-sample evidence. List of keyless live fund series pushed first
(`research/survey-5.md`: 10 trend funds, 3 risk-parity, 2 low-vol, 2 multi-style; DBV carry
delisted; SG/MLM indexes not keyless), card before any number (`cards/live-check.md`, 045422c),
script before its run. Descriptive only: no pick, 4 `live-check` rows in `tries.md`.

- `tsmom12` is not a trend fund: correlation 0.17 with nine live trend funds, 0.40 with SPY.
  Sharpe above bills 2010-2025: 1.11, the same as holding the six assets (1.11); live trend
  funds 0.19. Its lead over holding was +0.29 in 1994-2009 and 0.00 since.
- Haircut, same manager: AQR's paper TSMOM factor 1.41 (1985-2009) -> 0.35 (2010-2025);
  live AQMIX 0.29. h = 80% (literature: 73% median bank strategy, 25% Harvey-Liu ceiling).
- Crash years: trend funds +7% / +4% / +18% in 2008 / 2020-Q1 / 2022; `tsmom12` -2% / -14% /
  -13% (holding -13% / -12% / -38%). The rule cuts losses, it does not gain from falls.
- Plain statement (step 3): expect about holding's Sharpe with smaller bear-market losses.
  Sharpe > 0 forward: 7 years if the backtest is true, 170 at the measured haircut. Sharpe
  above holding: 107 years even at the backtest gap. A risk choice, not a forward verdict.

Count unchanged: 65 mechanisms, 16 tested, none passed (p < 0.00154).

- Doing: nothing. No process running.
- Next: (1) owner decision framed as risk: `tsmom12` vs holding is a drawdown choice (see
  `risk-map.md`), not an edge; (2) if anything is tested, prefer rules whose case is crash
  behaviour, judged on worst-year loss, not Sharpe; (3) `where-vol` lost more than the live
  risk-parity funds in 2022 (-27% vs -18%): check its 2022 bond/gold exposure before any
  revival.
- Data added (git-ignored cache): `<cache_root>/downloads/survey-5/` (Yahoo JSON, AQR TSMOM
  xlsx, Hurst et al. PDF text) and `<cache_root>/derived/survey-5/<TICKER>.csv`, made by
  `python -I research/lib/survey5_fetch.py <cache_root>`. Rerun:
  `uv run --with openpyxl python -I research/lib/survey5_live.py <cache_root>` (no new rows).

## Survey 4 (done 2026-11-18, branch `survey-4`, draft PR #72 -> `ann-1`)

New angle: effects with a documented record after publication or before their sample.
Sources (McLean-Pontiff 2016, Hou-Xue-Zhang 2020, Jensen-Kelly-Pedersen 2023, Harvey-Liu-Zhu
2016, Baltussen-Swinkels-van Vliet 2021 read as text, Koijen et al. "Carry" 2018 read as
text, Halloween papers), four candidates and a scored pick rule pushed before any number
(5310840); cards (3ad8ebd) and code before each run. **Both picks fail train; held-out year
unspent.** Write-up `research/survey-4.md`; tables `research/results/ts-carry.md`,
`research/results/halloween.md`; 17 rows in `tries.md` (3 are a disclosed bug run).

- `ts-carry` (stock and bond trend slots only while carry > 0): 0.97 vs 1.05 (-0.08, p 0.78);
  at the running mean 1.02 (-0.03). The stock leg is the loss (SPY out 54% of trend days; no
  timing information in its carry sign). The surviving carry premium is cross-country.
- `halloween` (stock slots only November-April): 0.96 vs 1.05 (-0.08), 0 of 5 eras; ahead
  only in R13's new-data years 1998-2012; SPY winter minus summer -0.5 bps a day after 2012.

Count: 65 mechanisms (61 + 4), 16 tested, none passed. Next test at p < 0.10 / 65 = 0.00154.

- Doing: nothing. No process running.
- Next: by the pre-set rule, `seasonal-20y` then `ts-value` (both prior under 1%); if run,
  `seasonal-20y` as an event study first (gate: same-month spread after 2016 with t >= 2).
  Published effects are 0 for 5 after publication in this book.
- Data added: `<cache_root>/derived/survey-4/shiller_div.csv` (from the cached Shiller
  `ie_data.xls`, `uv run --with xlrd python -I research/lib/survey4_shiller.py <cache_root>`).
  A fresh worktree also needs `research/macro.local.json` (copy the `.example`) and the price
  cache in `research/data/` (copy from another worktree).

## Ann 1 (done 2026-11-18, branch `ann-1`, draft PR #65 -> `survey-3`)

Survey-3's last live candidate, `announcement-premium`, checked by an FOMC event study before
any card. Decision rule pushed before any number (969f20e), script before its run (9e4f93b).
Write-up `research/ann-1.md`; table `research/results/ann-1.md`. No strategy, no `tries.md` row.

- Literature: Savor and Wilson (JFQA 2013: 1958-2009, 11.4 vs 1.1 bps on CPI/PPI/jobs/FOMC
  days; JFE 2014: beta priced only on those days); Lucca and Moench (JF 2015: S&P 500 +49 bps in
  the 24 h before FOMC, 1994-2011); their 2018 update (only at press-conference meetings);
  Kurov, Wolfe, Gilbert (FRL 2021: gone after 2015). Links and how far each was read in the note.
- SPY on FOMC day 0 minus other days: +30.9 bps (t 3.06, 138 meetings) in 1994-2011;
  -0.8 bps (t -0.06, 87 meetings) in 2015-2025. 2 pm to 2 pm from minute bars 2016-2025:
  +8.9 (t 0.8). Gate not met: **dead**, no card. CPI/payroll legs dropped by literature.
- Side cell, not a candidate: TLT day 0 +26.5 bps (t 2.3) after 2015, all in 2015-2019; that is
  `fomc-bond-drift` in its own sample years (still forward-only).

Count: 61 mechanisms, 14 tested by a strategy, none passed (unchanged). Next test at
p < 0.10 / 61 = 0.00164.

- Doing: nothing. No process running.
- Next: survey-2's list is fully spent (all seven closed or forward-only). Calendar effects from
  published papers are 0 for 3 after publication here; a new list should favour mechanisms with
  years after their sample, or forward-only checks.
- Data: none added. Needs `research/macro.local.json` (copy the `.example`), the FOMC calendar
  `<cache_root>/derived/survey-2/fomc.csv`, Yahoo daily snapshot `yahoo-1d/2026-11-12/` and
  the Alpaca SPY minute cache `alpaca/1m-sip/SPY/`.

## Survey 3 (done 2026-11-18, branch `survey-3`, draft PR #64 -> `survey-2`)

Card and train test of survey-2's rank 2, `xtsmom` (Pitkäjärvi, Suominen, Vaittinen, JFE
136(1) 2020, pp. 63-85: citation confirmed; sample 1980-2015, 20 countries, long-short).
Card and code pushed before any number. **Fails train, all three variants; held-out year
unspent.** Write-up `research/survey-3.md`; table `research/results/xtsmom.md`; 9 rows in
`tries.md`.

- `xtsmom` (stock slots only while the 10-year bond's 12-month return is positive): 1.05 vs
  1.05 (+0.00, p 0.49), 1 of 5 eras; it only lowers exposure. Paper's years in our data
  (1994-2015): SPY bond-up minus bond-down -0.2 bps a day; after (2017-2025): +0.4 (t 0.1),
  Sharpe -0.06 vs the twin. The effect exists only on the S&P 500 index in 1980-1993 (+21.5
  bps, t 2.2). 6-month bond (`xtsmom-b6`) and the paper's bond leg (`xtsmom-full`) worse.
- Ranked note on survey-2's other five: `announcement-premium` the only one left (1%; event
  study on FOMC days first); `fomc-bond-drift` forward-only (its sample covers our train);
  `turning-points`, `nonlinear-tsmom`, `crypto-corr` dead. `ideas.md` updated.

Count: 61 mechanisms, 14 tested, none passed. Next test at p < 0.10 / 61 = 0.00164.

- Doing: nothing. No process running.
- Next: survey-2's list is spent. If anything, an `announcement-premium` event study on FOMC
  days (no new data) before any card. Published effects whose sample covers our train get no
  honest train test: prefer ones with years after their sample.
- Data: none added. A fresh worktree needs `research/macro.local.json` (copy the `.example`;
  the FRED `DGS10` snapshot in the cache) and the price cache in `research/data/`.

## Survey 2 (done 2026-11-18, branch `survey-2`, draft PR #60 -> `wide-4`)

2023-2026 research read for ideas this book could use that the repo had not listed; 19 sources
(tagged by how far each was read), 7 new candidates ranked by prior in a note pushed before any
number; the top pick carded, coded and tested on train. **It fails; held-out year unspent.**
Write-up `research/survey-2.md`; table `research/results/fomc-cycle.md`; 7 rows in `tries.md`.

- `fomc-cycle` (Cieslak, Morse, Vissing-Jorgensen, JF 2019: the equity premium is earned in
  even weeks of the FOMC cycle): replicates in the paper's years (SPY even-minus-odd +11.0 bps
  a day 1994-2013, t 3.1; +17.8 in 2014-16) and reverses after publication (2017-2025: -5.7,
  t -1.2). Stock slots only in even weeks: 1.22 vs 1.05 on full train (p 0.03), all of it
  before 2017; -0.05 since. Fails the family bar and both post-publication bars.
- Ranked, untested: `xtsmom` (stocks only while bonds also trend up, 3%), `fomc-bond-drift`
  (2%), `announcement-premium` (2%), `turning-points`, `nonlinear-tsmom`, `crypto-corr` (<=1%).
- Literature found for listed ideas: Hartley and Schwarz (2019) on month-end Treasury returns
  (supports `month-end-bonds`); Harvey, Mazzoleni, Melone (NBER 2025) on front-run pension
  rebalancing (`rebalance-pressure`, already dead here).

Count: 61 mechanisms (54 + survey-2's 7), 13 tested, none passed. Next test at p < 0.10 / 61.

- Doing: nothing. No process running.
- Next: `xtsmom` is the cheapest next card (no new data, post-sample window 2016-2025). No
  more central-bank calendar tests before it.
- Data added (git-ignored cache): FOMC calendar pages (`<cache_root>/downloads/survey-2/fomc/`),
  parsed to `<cache_root>/derived/survey-2/fomc.csv` (256 scheduled meetings 1994-2025) by
  `python -I research/lib/survey2_fomc.py`. A fresh worktree also needs
  `research/macro.local.json` (copy the `.example`) and the price cache in `research/data/`.

## Wide 4 (done 2026-11-18, branch `wide-4`, draft PR #57 -> `wide-3`)

W2 `tax-drain` from the list, then five new mechanisms from unused fields and a test of the
best one. Fact check, choice note, cards and code were each pushed before any number. **Both
tested ideas fail train; held-out year unspent.** Write-up `research/wide-4.md`; tables
`research/results/tax-drain.md`, `research/results/coupon-dose.md`; 7 rows in `tries.md`.

- Fact (NY Fed, Santoro 2012): tax receipts sat in bank TT&L accounts with the Fed's account
  held near $5 billion until fall 2008; from 2008-12 the cash goes to the Fed. wide-3's date
  was right; the source adds that the drain only matters when reserves are scarce.
- `tax-drain` (W2, hydraulics): SPY, QQQ, TLT out for five sessions around each tax date
  from 2008-12-16: 1.03 vs 1.05 (-0.016, p 0.88). The drain is real (Treasury's Fed account
  +88 $bn over D-2 .. D+1 since 2008, t 13.7; +1 $bn before). Prices: right sign, right order
  by regime (SPY -62 bps while the Fed shrank reserves, t -1.3; ~0 before 2008), too weak.
- New W4-W8 in `research/wide-1.md` (last section): `coupon-dose` (pharmacokinetics),
  `tidal-trigger` (seismology), `payday-inflow` (actuarial science), `fatigue-damage`
  (materials fatigue), `snapshot-shrink` (metrology).
- `coupon-dose` (W4, picked): idle cash into TLT for four sessions when the Treasury's net
  payment on the 15th is positive: 1.04 vs 1.05 (-0.011, p 0.71). Positive-dose days +2 bps
  vs +18 on the others; wrong sign since 2014.

Count: 54 mechanisms (46 listed + W1-W8), 12 tested, none passed. The next test is read at
p < 0.10 / 54 = 0.00185.

- Doing: nothing. No process running.
- Next: W5 `tidal-trigger` is the only W entry with a prior above 1%, and it must be checked
  on a calendar not used to suggest it (forward, or the tax-date drain in future
  scarce-reserve years). Forced Treasury flows are now spent for this book. The `tax-drain`
  event study is worth re-running forward as a descriptive check, not as a trade.
- Data added (git-ignored cache): Daily Treasury Statement cash balances
  (`<cache_root>/treasury/dts-2026-11-18/`, parsed to `derived/wide-4/tga.csv`), the auction
  file with rates and amounts (`downloads/wide-4/treasury-auctions/`, parsed to
  `derived/wide-4/payments.csv`). FRED refuses automated downloads from this machine.

## Wide 3 (done 2026-11-18, branch `wide-3`, draft PR #54 -> `wide-2`)

Two more picks from wide-1's list, then three new mechanisms and a test of the best one. Choice
note, cards and code were each pushed before any number. **All three tested ideas fail train;
held-out year unspent.** Write-up `research/wide-3.md`; tables `research/results/`; 8 rows in
`tries.md`.

- `hedge-regime` (F2, stock-bond correlation as order parameter: keep TLT out of trend while
  it hedges): 1.05 vs 1.05 (+0.003, p 0.39); other ETFs -0.006. One sign flip (2023).
- `attention-peak` (P2, SIR on English-Wikipedia page views: leave a coin after its attention
  peak): 1.02 vs 1.05 (-0.03); other coins 0.33 vs 0.54. Caught 2017-12, wrong in 2021.
- `opex-pin` (new W1, option-expiry week, idle cash into stocks): 1.01 vs 1.05 (-0.04), behind
  its placebo week. SPY expiry week vs average week: -0.3 bps (t 0.0, 381 weeks).
- New, untested, with test plans in `research/wide-1.md` (last section): W2 `tax-drain`
  (reserve drain on tax dates, 1994-2007 as placebo), W3 `lunar` (lowest prior).

Count (corrected): wide-1's list has 46 entries; 10 cards now cover 11 of them plus one new
mechanism; 35 listed entries uncarded (wide-2's "39" counted cards, not entries). With the 3
new ones the family is 49; the next test is read at p < 0.10 / 49.

- Doing: nothing. No process running.
- Next: W2 `tax-drain` as an event study first (check when Treasury receipts moved from
  commercial-bank accounts to the Fed before writing its placebo). Of the 35 listed entries
  left, none has a better prior than the failures so far; the list looks exhausted for this
  book.

## Wide 2 (done 2026-11-18, branch `wide-2`, draft PR #47 -> `wide-1`)

One mechanism picked from the 42 that wide-1 listed and did not card: Q5, trend age (hazard
rate). Rule `age4`: hold a `tsmom12` slot only once the signal has been on for four Fridays.
**Fails train: 0.99 against 1.05 (difference -0.06, 90% range -0.11 to -0.01), behind in all
five eras; held-out year unspent.** Short spells are common (50 of 111 end within four weeks)
but cheap; the three missed weeks of lasting trends cost more. Write-up `research/wide-2.md`;
table `research/results/trend-age.md`; 7 rows in `tries.md`.

Second pick, same day: E6, patch-leaving (marginal value theorem). Rule `mvt`: the twin's
exposure, held only in the in-trend assets whose risk-scaled 12-month return is at least the
average. **Fails all five bars: 0.85 against 1.05 (difference -0.19, 90% range -0.36 to
-0.02), drawdown 53% against 37%, turnover 9.7 against 2.7; held-out year unspent.** Table
`research/results/patch-leaving.md`; 4 rows in `tries.md`. Both picks were read at
p < 0.10 / 42.

Third pick, same day: G2, crowded-trend (halve the book when at least three assets are eligible
and all are in trend). **Fails: 0.98 against 1.05 (difference -0.07, 90% range -0.16 to
+0.03), ahead in 1 of 5 eras; held-out year unspent.** Drawdown 29% against 37%, but 3 points
less return a year. Table `research/results/crowded-trend.md`; 4 rows in `tries.md`.

- Doing: nothing. No process running.
- Next: nothing from the three cards. 39 of wide-1's mechanisms stay uncarded; three price-only
  changes to the trend rule have now failed. wide-1's three lanes below stand as written.

## Wide 1 (done 2026-11-18, branch `wide-1`, draft PR #33 -> `carry-2`)

New hypotheses from ten other fields (ecology, epidemiology, signal processing, control,
information theory, game theory, physics, queueing, neuroscience, immunology). 46 mechanisms
sorted before any number; 33 collapse into ideas already killed; four got a card, each a bet on
someone else's mechanical trading. **All four fail their pre-set bar on train; held-out year
unspent.** Write-up `research/wide-1.md`; tables `research/results/`; 39 rows in `tries.md`.

- `auction-concession` (TLT out before 20/30-year Treasury auctions): book +0.01 over `tsmom12`
  (p 0.14). The dip is in TLT's closes (-34 bps, t 2.5) but half is lost at next-open fills;
  IEF goes the other way. Faint lead.
- `rebalance-pressure` (halve the month's stock/bond leader in the last five sessions): book
  -0.005. The raw spread has the predicted sign; not confirmed on 1962-2003 data.
- `contagion-catchup` (21 ETFs, hold those whose relatives moved and which did not): dead, 0.50
  vs 0.60. Relatives' moves do not spill over; plain one-week reversal is all there is.
- `vol-echo` (hold stocks when a shock leaves the 21-day volatility window): dead, SPY 0.25 vs
  0.63; the pre-2010 placebo looks the same.

Found after the tests (a hypothesis, not a result; `research/results/wide-1-yields.md`): long
bonds earned almost all their return in the last four sessions of each month (TLT +39 bps,
t 4.3, 2003-2025, both halves; +32 at next-open fills; from yields: nothing before 1990, +13
to +23 bps in 1990-2003).

Next lanes (each needs its own card; details at the top of `research/wide-1.md`):

1. `month-end-bonds`: idle cash into the long bond for the last four sessions of each month.
   Clean tests left: LQD (not looked at), TLT's first year, the held-out year once, forward paper.
2. A volume screen: the six assets' own trading volume has never been screened.
3. The month-end stock bounce after a bad month, with a mid-month placebo first.

### For the owner

- Nothing to change in the paper system.
- `month-end-bonds` would spend the held-out year on a pattern found by looking, not by a card.
  That is allowed only through a new card; whether to spend the year on it is your call.
- Flow effects of this size (15-40 bps per event) only pay with futures and modest leverage:
  the same broker gap the carry lead ran into.
- Two effects here are worth more at the close than at the next open (the auction dip keeps 45%
  at our fills, the month-end bond rally 83%). Whether the paper broker should be able to fill
  at the close is a design question.
- Paid data noted, nothing bought: token unlock schedules (price not checked).

## Carry 2 (done 2026-11-13, branch `carry-2`, draft PR #26 -> `short-1`)

Short-1's carry book, copied unchanged, on data it never saw: Binance perps outside the 30
(delisted included), Bybit, Hyperliquid (~550 coins, 2021-2025, 10 bps + every funding event).
Weak replication by the card: `ls-funding` passes all four bars (pooled Sharpe 0.69, p 0.04;
blend 0.37 vs twin 0.20, p 0.04; positive on every venue and era); `ls-premium`, the lead, does
not (pooled 0.44, p 0.15). Smaller than on short-1's 30 coins, a funding harvest with beta hedged
out, gone at 30 bps (turnover ~42x a year). Held-out year unspent (card: only if `ls-premium`
replicates). Write-up `research/carry-2.md`. Owner options: a cost card (real fills on small
perps, slower rebalance) or a held-out-only card for pooled `ls-funding`; neither matters while
the paper system stays long-only BTC/ETH on spot.

## Short 1 (done 2026-11-13, branch `short-1`, draft PR #23 -> `breadth-1`)

A short side on Binance USDT perps (30 pairs and BTC/ETH, 2020-2025, 10 bps + every funding
event): nothing passed. `tsmom12` that goes short in downtrends trails long-only (0.73 vs 1.03
spot on 30 coins; 0.76 vs 1.19 on BTC/ETH). Longs on perps paid ~12% a year in funding.
Dollar-neutral low-vol/size/turnover books lose (short legs of wild coins in the 2020-21 rally).
Near miss: a premium/funding carry book (short the most expensive perps), blend with `tsmom12`
1.25 vs 1.03 at 10 bps, but not at 30 bps. Held-out year unspent. Write-up `research/short-1.md`.
Owner options: a held-out-only carry card, or keep long-only BTC/ETH (recommended).

## Breadth 1 (done 2026-11-13, branch `breadth-1`, draft PR #22 -> `info-1`)

Wide books and hourly frequency, after 30 bps costs. One pass: in the wide Coin Metrics coin book
(top 100, dead coins included, 2019-2025), tilting toward low volume-to-market-cap coins inside
the trend rule lifted Sharpe from 0.72 to 1.06 (held-out year 0.61 against 0.31). It did not carry
over to the 30 liquid Binance pairs, and it stays below plain BTC `tsmom12` (~1.16), so it is
no case for widening the crypto slot. The 33-market pool and the hourly BTC/ETH rules add nothing
(hourly reversal is real, IC ~-0.08, but the costs are ten times the edge). Write-up
`research/breadth-1.md`. Open owner options: a short-side card on perpetuals with funding costs,
or a coin-book RL agent behind rl-3's gate. Neither matters while the paper system stays on
long-only BTC/ETH.

## Info 1 (done 2026-11-13, branch `info-1`, draft PR #21 -> `rl-3`)

23 new inputs (COT, Cboe options/vol and put/call, crypto funding/basis/DVOL, on-chain, Fear &
Greed, cross-asset) screened for weekly IC: none useful (best walk-forward gain over the trend
inputs +0.025; one candidate above chance in sample). Write-up `research/info-1.md`. Open
options for the owner: more independent bets (30 Binance perps, 33-market pool), a wider action
(short side), or a slower-horizon (4/13-week) screen as a new card.

## M0 status: built, not yet proven live

Done: template scaffold, data ingest (BTC, ETH, SPY, QQQ, GLD, TLT, append-only CSV), gym
(next-open fills, fees, slippage, long-only, 10,000 USD), 4 benchmark strategies, append-only
ledger + tries counter + git-history integrity check, daily runner + `.github/workflows/daily.yml`,
scoreboard (`python -m grimstrade.report --root trail [--backtest]`), owner README, MIT license.

## To finish M0 (needs someone with GitHub access)

- [ ] Merge this branch to `main` (via PR), then run "Daily paper trading" once by hand
      (workflow_dispatch). Unverified live: Kraken/Coinbase/Yahoo/Stooq formats are from docs,
      tested only on fixtures (dev container can't reach them). Yahoo may 429 from Actions; Stooq is
      the fallback. Check the first run creates the `paper-trail` branch and pushes to it.
- [ ] Check the Actions settings allow GITHUB_TOKEN write (contents: write is requested).
- [ ] If the `protect-main` ruleset is ever widened to all branches, exempt `paper-trail`
      (the bot pushes there directly).

## Assumptions (see docs/DECISIONS.md)

- CSV + stdlib only (no parquet/pandas). Raw prices; dividends not credited yet.
- Bot commits to orphan branch `paper-trail` because `main` requires PRs.
- Costs: crypto 25 bps fee + 5 bps slip; ETFs 0 fee + 2 bps slip; 1% rebalance band.
- Decisions at ~22:30 UTC see crypto bars through yesterday (today's still open) and ETFs through
  today. Fills show up a day later, once the fill bar has closed and been stored.
- A run with no new data since a strategy's last decision writes no new decision.
- Gymnasium env wrapper deferred (BACKLOG).

## M1 (next)

Classic strategies live in paper (time-series momentum, cross-sectional momentum, vol targeting,
risk parity, crypto mean reversion), each registered in `ledger/tries.jsonl`; deflated Sharpe in
the scoreboard; weekly one-screen summary for the owner.

## Macro 1 (research run, branch `macro-1`, started 2026-11-13 ~01:40 UTC)

Brief: `chief-of-staff/briefs/grimstrade-macro-1.md`. Question: does knowing the macro phase
(Fed policy, real rates, yield curve, money supply, credit spreads, the Bitcoin halving cycle)
add anything over `tsmom12`? Write-up: `research/macro-1.md`.

- Done: look-ahead-safe macro layer (`research/lib/macro.py`, ALFRED vintages; tests in
  `tests/test_macro_asof.py`), protocol section "Macro tests", six cards tested on train, all
  fail their bar (halving: passes on numbers but fails bar 2 and is not believed: three winters,
  folklore window). Feature skill table, write-up `research/macro-1.md`. Held-out year unused.
  Draft PR #16 (`macro-1` -> `research-3`), not merged.
- Doing: nothing.
- Next: macro features as regime inputs for the RL agent (list in `research/macro-1.md`). The
  owner may want to read the halving section before anyone trades a "four-year cycle".

## RL 1 (research run, branch `rl-1`, started 2026-11-13 ~01:50 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-1.md`. Question: can an RL agent (PPO, policy shared
across assets, prices + macro inputs) beat `tsmom12` out of sample? Plan and results:
`research/rl-1.md`; rules: `research/protocol.md` "Reinforcement-learning tests".

- Done: plan and protocol section before code; gym-exact batched simulator and environment
  with tests; 5 agents x 10 seeds x 13 walk-forward folds trained on the RTX 5080; evaluated
  through the real gym, 70 rows in `research/tries.md`; tables `research/results/rl-1.md`;
  write-up `research/rl-1.md`. Answer: no. All five fail (Sharpe 0.57-0.71 against
  `tsmom12` 0.99 out of sample 2000-2025, 0 of 50 seeds ahead). Held-out year unused.
  Draft PR #17 (`rl-1` -> `macro-1`), not merged.
- Doing: nothing. No process running.
- Next (not started): residual-policy rung (tsmom12 plus a bounded tilt, reward relative to
  tsmom12, coin cap); card and bar first. Details in `research/rl-1.md`, "What the next rung
  would need".

## RL 2 (research run, branch `rl-2`, started 2026-11-13 ~05:05 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-2.md`. Question: does an RL agent constrained to tilt
`tsmom12` (residual policy, active reward, early stopping, one variant pooled over 33 markets)
beat `tsmom12` out of sample? Plan and results: `research/rl-2.md`; rules: `research/protocol.md`
"Residual RL tests".

- Done: residual environment + tests (zero tilt == `tsmom12` exactly), trainer with purged
  validation and early stopping, on-chain inputs for coins (`research/lib/onchain.py`, as-of
  test), 4 variants x 10 seeds x 13 folds, evaluated through the gym, 56 rows in
  `research/tries.md`, tables `research/results/rl-2.md`, write-up. Answer: no. All four fail
  (Sharpe 0.96-0.98 against 0.99; active share 1.8-2.7%; at most 1 of 10 seeds ahead).
  Held-out year unused. Draft PR #18 (`rl-2` -> `rl-1`), not merged.
- Doing: nothing. No process running.
- Next (not started): planted-signal control of the residual pipeline (can it find a known
  weak signal?); then funding rates / basis for coins, which need shorting or futures in the gym.

## RL 3 (research run, branch `rl-3`, started 2026-11-13 ~05:30 UTC)

Brief: `chief-of-staff/briefs/grimstrade-rl-3.md`. Question: is RL 2's null the inputs or the
learner? A known weak signal (IC 0.00-0.20) was planted into one input of RL 2's residual
environment, to see at what strength the same pipeline beats `tsmom12`. Card and results:
`research/rl-3.md`; rules: `research/protocol.md` "Planted-signal controls".

- Done: card before code, planted input with tests, 10 planted configurations + 4
  pre-registered diagnostics x 10 seeds x 13 folds, ceiling rules, a post-hoc supervised check,
  183 `control` rows in `research/tries.md`, tables `research/results/rl-3.md` and
  `research/results/rl-3-inputs.md`, write-up. Answer: the pipeline finds only 0.20 (capturing
  9-21% of its +0.45 ceiling) and misses 0.10 (worth +0.16). More budget or no early stopping
  does not help; least squares misses it too, so the cause is too many noisy inputs for the data.
  Real inputs: weekly IC at most ~0.05 alone and ~0 together, below the 0.10 at which even a
  perfect learner gains anything on this book. Both limits are real; the inputs bind first.
  Held-out year unused. Draft PR #19 (`rl-3` -> `rl-2`), not merged.
- Doing: nothing. No process running.
- Next (not started): (1) gate every learner change on "finds 0.10 in the planted control" (few
  inputs, shrinkage, pooled books); (2) screen new inputs (funding/basis, open interest,
  minute-bar features, VIX term structure) with a cheap weekly-IC table before any RL run.
