# Next steps

## Night lead 2026-11-18 (brief `chief-of-staff/briefs/grimstrade-night-2026-11-18.md`)

- 1. Exit research (owner priority, `chief-of-staff/briefs/grimstrade-exit-research.md`):
  DONE 2026-11-18 ~22:30 UTC: review round 3 = FINAL at 7048bad (log 770de50; rounds 1-2 were
  CHANGES, all fixed). Optional round-3 polish follows on the same branch. Was IN PROGRESS. Branch `research/exit-1` (worktree `grimstrade-exit1`), draft PR #50. Lanes since
  18:58 UTC, each `research/exit-1-<lane>` in `grimstrade-exit-<lane>`: lit, haven, bt, inv,
  reentry, park; notes land in `research/exit-plan-2026/lanes/`. Then merged `report.md` and the
  review loop (`review-log.md`). Mark DONE here when a reviewer says FINAL.
  - 19:40 UTC: all 6 lanes done and merged into `research/exit-1` (bt 176 + reentry 32 rows in
    `research/tries.md`; cards `exit-rules.md`, `reentry.md`). Writer merging into `report.md`.
- 2. Normal lanes started alongside (Opus):
  - DONE `data-long-2` (draft #51 -> data-long-1): gold loader (datahub, usable 1971-), Shiller
    and gold cross-checked vs Damodaran (Shiller monthly yields interpolated before 1953-04: no
    honest monthly signal earlier). `trend-where-long`: `where-vol` keeps the filter on 10y bonds
    (71/71 refits); on gold it drops it from 1986 and deepens worst loss (51.7% vs 42.6% to 2001;
    39.3% vs 21.7% 2002-25). Close trend-where; live rule unchanged. Next: FRED PPIACO retry.
  - DONE `rl-6` (draft #52 -> rl-5): RL/perp line CLOSED. Power: 246 train weeks detect only
    Sharpe >= 0.98 (p<0.10; 1.42 with 8 carry shapes counted), best seen 0.79; carry-3's held-out
    failure was price, not cost. 0 tries (no slow-carry card by the pre-set rule). Reopen only on
    the 4 triggers in `research/rl-6.md`.
  - DONE `coin-cap-2` (draft #53 -> coin-cap): 445 coin falls >= 60% on 197 coins = 21
    episodes (effective ~7.6). `stop-0.25` beats a matched-cost cap (f 0.663) on deepest loss in
    15/21 (sign p 0.039), 9/10 years; loses in fast crashes (weekly stop); Sharpe unchanged. Rule
    PR candidate: owner's call (see For the owner).
  - DONE `wide-3` (draft #54 -> wide-2): `hedge-regime` 1.05 (+0.003, p 0.39), `attention-peak`
    1.02, `opex-pin` 1.01 (trails its placebo): all fail vs `tsmom12` 1.05. List now 49
    mechanisms, 10 tested, 0 passed: next test needs p < 0.0020. (wide-2's "39 uncarded" was
    wrong: 35 of 46.)
  - `evo-1` build done (fast scorer within 0.04 Sharpe of `gym.simulate`; one full search ~2.5
    CPU-min, 40 replays ~2 CPU-h). Noise control flaw: zero log drift pays holders sigma^2/2, so
    lead chose (dated card note): zero-mean-simple-return worlds, rerun controls, 40 replays
    (<=1 at/above), then the one real search, train only.
  - DONE `coin-cap-3` (draft #56 -> coin-cap-2): daily-checked stop fixes 3 of the 6 episodes
    the weekly stop lost; gains return via cheaper re-entries, not shallower losses. Bug fixed:
    coin-cap-2's 4 tries rows really start 2015-09-23 (rows not edited). Next cards (not
    started): price-drawdown stop, 25% cap + stop, time under water.
  - evo-1 controls after fix: noise 0/3 found, but planted k=0.04 NOT found (search overfits
    past the true rule). Lead (card note): tune greed on fresh synthetic worlds only, confirm on
    new controls, then replays + real search; else close-or-redesign.
  - DONE `gsy-1` (draft #55 -> trend-1926): GSY replicates in direction, weaker: 49 French
    industries 1928-2014, P(40% crash in 2y) 38% after +100% (GSY 53%), 51% after +150% (GSY
    ~80%), base 15%; since 2002 27%/35% vs 12%. Overlay on `tsmom12`: `flag100-sma` +0.027
    (p 0.001), `flag100-vol` +0.030 (p 0.007) pass the Sharpe route pre-2002, fade after 2002
    (p ~0.2) and trail on sector ETFs; no worst-loss gain (`tsmom12` already out of 88% of
    industry crashes). Not a candidate; use run-up crash rates for risk description only.
  - DONE `evo-1` (#44): greed grid (penalty 0.01/0.03/0.06 x 30/10/5 gens) on fresh synthetic
    worlds: plant never found (best 0.20 vs ceiling ~0.22-0.24), noise 0/3; confirmation of the
    pre-picked setting FAILS. No replays, no real search, held-out untouched (154 control rows).
    Plant strength was not calibrated across worlds (0.72 vs 0.22). Lead: redesign as evo-2.
  - DONE `wide-4` (draft #57 -> wide-3): `tax-drain` (TT&L -> TGA shift late 2008, Santoro
    2012; drain real, +88 $bn on tax dates, t 13.7) fails: 1.03 vs 1.05 (p 0.88); new W4-W8
    from pharmacokinetics, seismology, actuarial, materials fatigue, metrology; W4
    `coupon-dose` fails (1.04, p 0.71). List 54 mechanisms, 12 tested, 0 passed: next needs
    p < 0.00185. FRED blocked here: DTS used instead.
  - DONE `evo-2` (draft #58 -> evo-1): 8 inputs, six-asset days, plant calibrated per world.
    Noise 0/3 (pass) but plant 0.8 found in 1/3 (two near-misses: 0.001, 0.03): gate FAILS. No
    replays, no real data ever used. Evo line CLOSED (recovery 0.45 of target vs evo-1 0.26).
  - DONE `eu-1` (draft #59 -> trend-tune): `tsmom12` on a EUR UCITS copy of the live six
    (SXR8, SXRV, 4GLD, IBGL, BTC/ETH in EUR; 2012-2025 train, Dutch costs): character holds
    (Sharpe 1.44 vs 1.37 US twin, max DD 31% vs 36.5%, same crash pattern). Coin-free 7-asset
    set: drawdown role holds, but trails equal weight by 0.21 Sharpe in EUR (currency + costs).
    SE of each Sharpe ~0.27. Follow-ups (not started): eu6 paper book (owner), fixed per-order
    fees, EUR-hedged vs unhedged US equity card.
  - DONE `cash-interest` (draft #61 -> main, never merged by agents): idle cash earns `^IRX`
    (13-week T-bill, keyless; negative -> 0), daily act/365 on end-of-UTC-day cash, newest rate
    known at d 00:00, append-only `data/rates.csv`; same `gym.simulate(rates=...)` for live and
    backtests; Sharpe now above cash. 24 tests; 235 pass. Train effect: `tsmom12` CAGR 17.64% ->
    18.19%, `sixty_forty` 8.09% -> 8.63%. Mechanical conflicts with #29/#30/#32.
  - DONE `eu-2` (draft #62 -> eu-1): fixed per-order fees (DEGIRO EUR 1/3, Trade Republic
    EUR 2): coin book eu6 worth it from EUR 5k (EUR 3 orders + band: ~6k); coin-free euw needs
    ~16k at EUR 3, ~10k at EUR 2, ~6k at EUR 1. >= EUR 25k fees cost <= 0.07 Sharpe. 5% band
    fails card (changes the rule). EUR-hedged S&P (IUSE) does not remove the drag (-0.21
    unchanged; hedge ~2.5%/yr): keep unhedged. 96 rows. Next: fewer signal flips for small
    coin-free books (new card); check DEGIRO core selection.
  - DONE `survey-2` (draft #60 -> wide-4): 19 sources 2023-2026, 7 new candidates (in
    `research/survey-2.md`). Top pick `fomc-cycle` (Cieslak-Morse-Vissing-Jorgensen 2019):
    replicates in-sample (SPY even-odd +11 bps/day 1994-2013, t 3.1) but reverses after
    publication (2017-2025 -5.7, t -1.2); stock slots in even weeks only: Sharpe 1.22 vs 1.05
    (p 0.03) but all from 1994-2016; FAILS (family 13 of 61 tested, bar p < 0.00164).
    Next: `xtsmom` (stocks only while bonds trend up, JFE 2020), no more Fed-calendar tests.
  - DONE `eu-3` (draft #63 -> eu-2): 6 variants on `euw` (Friday-only, monthly, monthly entry,
    4-week hold, 4 class funds, 4 funds monthly), 81 rows. Only Friday-only keeps the character
    (saves 2 orders/yr); the big cutters change the rule (monthly +0.14 Sharpe, p 0.03, not
    significant after 6; monthly lost on the US six 1994-2025). Verdict: euw not worth it at
    EUR 5k; at 10k only with EUR 1 orders; at 25k any fee. Next (owner): monthly-vs-weekly
    card on held-out year if wanted; DEGIRO core selection check.
  - DONE `survey-3` (draft #64 -> survey-2): `xtsmom` (Pitkajarvi-Suominen-Vaittinen JFE
    2020, citation checked) fails: primary Sharpe 1.05 vs 1.05 (p 0.49); paper's years in our
    data -0.2 bps/day, after sample +0.4 (t 0.1); b6 -0.03, full -0.04. Family 61, 14 tested,
    0 passed. Survey-2 list used up: only `announcement-premium` live (event study first).
  - DONE `ann-1` (draft #65 -> survey-3): FOMC day-0 premium replicates in-paper (SPY +30.9
    bps, t 3.06, 1994-2011, 138 meetings), gone after (2015-2025: -0.8, t -0.06; Lucca-Moench
    2 pm window +8.9, t 0.8). Dead by the pre-set rule; no card, no tries. Published calendar
    effects 0 for 3 after publication: new lists should favour mechanisms with post-sample
    years or forward-only checks. Family stays 61 / 14 tested / 0 passed.
  - DONE `trend-1926-fix` (draft #66 -> trend-1926): replay gaps = Friday-holiday weeks
    (`common.weekly` fills one session later than the paper series; no look-ahead; shared
    convention). No numbers changed beyond 0.012; era-1 energy flips sign (9 -> 10 of 10
    industries), verdict unchanged. 7 tests for era 2; docs cover both eras. Owner: move
    `common.weekly` to the calendar Friday (needs its own card; shifts every lane a little)?
  - DONE `forward-1` (draft #67 -> main): forward registry (`docs/forward-registry.md`,
    DECISIONS entry PROPOSED; `src/grimstrade/forward.py`, 18 tests; offline command only).
    Years needed at 80% power (alpha 0.025 each): carry-3 `band` 12.7 (7.3 alone), FOMC bond
    drift 78, coin stop 26 (~55 independent), monthly-vs-weekly 32. Only carry is judgeable
    forward; the rest are decided on other grounds. Candidates proposed, NOT frozen.
  - Nothing running at 20:45 UTC (5h 0.77 at 20:37: no new lanes until the 21:30 reset).
    (`grimstrade-trend1926b`: era-2 replay gaps, TREND_ERA=1962 test, docs) (`grimstrade-cashint`: interest on idle cash in the gym, draft PR
    -> main)
    (`grimstrade-evo2`: <=8 inputs, six-asset days only, plant calibrated per world, controls
    must pass before replays/real search) (`grimstrade-gsy1`, Greenwood-Shleifer-You
    run-up exit on French industries 1928-), `coin-cap-3` (daily-checked stop vs weekly).
- 22:10 UTC night-2 lead took over. Exit research: review round 2 running on the scrubbed
    report (cfb50fe). Lanes started (Opus): W `wide-5` (<- wide-4), W `survey-4` (<- ann-1,
    effects with post-publication survival), D `eu-4` (<- eu-3, whipsaw in small books),
    D `coin-cap-4` (<- coin-cap-3, BTC/fast-crash failure modes, last 3 cards as one set),
    D `combo-1` (<- main: failure map of existing models, complementary blends).
  - DONE `eu-4` (draft #68 -> eu-3): whipsaw is ~half of `euw`'s fee drag (30 orders/yr, a
    third each entries/exits/drift; 83% of signal flips reversed within 4 weeks; z moves ~0.21
    a week). Confirm-2-Fridays (Sharpe 0.62 = 0.62, orders 30 -> 20) and +-0.25 z dead zone
    (0.64, 16.6 orders) both FAIL the character card (max DD +3.3 / +2.4 pts, later 2020 exits).
    eu-3 verdict unchanged. 24 rows; family 8, none selected. Next: `eu-5` (drift third only).
  - 22:25 UTC `eu-5` started (D, <- eu-4): cut drift top-ups, signal untouched.
  - DONE `coin-cap-4` (draft #69 -> coin-cap-3): no candidate meets the bar (m 15: needs >= 17
    of 21 episodes, p < 0.0067). Price-drawdown stop 16/21 (p 0.013), looser on BTC/ETH (worst
    25.2% vs 17.7%); 25% cap + stop fails all 4 checks. Weekly stop fails in fast falls (still
    fully in after -38% first week, out at -44%), at hot tops (vol band loose) and on bounce
    re-entries. Verdict `research/coin-cap-verdict.md`: weekly `stop-0.25` as risk preference
    (coin-years worst loss 36.5% -> 17.7%; ~2 pts/yr growth cost). 6 rows. Coin line parked.
  - 22:35 UTC `dsr-1` started (D, <- main): project-wide tries census + Deflated Sharpe on
    `tsmom12` and the best near-misses.
  - DONE `wide-5` (draft #71 -> wide-4): new W9 `dealer-backlog` (queueing) 1.02 vs 1.05
    (p 0.95, slope wrong sign) and W10 `extension-dose` (control) 1.06 (p 0.19; gain is all
    2008-09) FAIL. List 56 / 14 tested / 0 passed; next bar p < 0.00179. Stop testing forced
    Treasury flows (4 failed). 6 rows.
  - 22:40 UTC `wide-6` started (W, <- wide-5): critical-slowing-down early-warning gate,
    `lunar` gate, 3-4 new mechanisms from unused fields.
  - DONE `combo-1` (draft #70 -> main, adds research tree to main): failure map: `trend-vol`,
    `stop-0.25`, `inverse-vol`, `sixty-forty` are one bet (excess corr +0.5..0.9; give back
    17-32%/yr after lows); `where-vol` fails elsewhere (corr 0.00 with stop). `blend-ws`
    (where-vol + stop-0.25) 1.13 vs 1.05 (p 0.059, worst loss 28.9% vs 36.5%) fails family bar
    (72) and eras (behind 2022-25); `blend-iv` 1.07. 8 rows. Closest miss in the repo so far.
  - 22:50 UTC `combo-2` started (D, <- combo-1): blends with T-bill interest (#61), one
    long-only partner for stock+bond co-falls (2022).
  - DONE `survey-4` (draft #72 -> ann-1): post-publication-survival angle; `ts-carry` 0.97 vs
    1.05 (p 0.78; carry sign has no timing info, the surviving premium is cross-country
    long-short) and `halloween` 0.96 (ahead 0 of 5 eras) FAIL. Published effects 0 for 5 here.
    Family 65 / 16 tested; bar p < 0.00154. 17 rows (3 from a disclosed gating bug, rerun).
  - 22:55 UTC `survey-5` started (W, <- survey-4): live fund track records as post-sample
    evidence; backtest-to-live haircut for `tsmom12`.
  - DONE `eu-5` (draft #73 -> eu-4): 5/25 rebalance band (D2: top up only when >25% off
    target) cuts `euw` orders 30.1 -> 21.1/yr (drift 10.0 -> 1.1) at the same rule (Sharpe
    +0.01, max DD +0.6 pts, crashes within 0.5); holds on `eu6`/`usw`. Min book EUR 1/2/3:
    ~4k/7k/11k (was 6k/10k/16k). D1 (flip-day rebalance only) unsafe with coins (eu6 DD 31 ->
    65%). Rule still trails holding the 7 funds (0.62 vs 0.77). 24 rows.
  - 23:00 UTC `eu-6` started (D, <- eu-5): trend vs buy-and-hold for a small coin-free EUR book.
  - DONE `dsr-1` (draft #74 -> main): census 2,811 distinct tries / 124 families (947
    selectable). `tsmom12` beats zero (Sharpe 1.05, DSR >= 0.95 up to ~59k trials) but so does
    equal weight; its lead over equal weight (+0.17, p 0.08) fails even uncorrected; DSR 0.48
    counting the 8 baselines it was picked from, 0.03 at 947. Top-5 near-misses: none worth a
    held-out year. Live scoreboard counts only 307 tries (`_RESEARCH_REFS` reads `research-*`
    only). 0 rows (no backtest).
  - 22:27 UTC `register-1` started (D, <- dsr-1): fix scoreboard refs, project-wide register +
    generated BAR.md, convention PROPOSED.
  - DONE `eu-6` (draft #77 -> eu-5): small coin-free EUR book 2012-2025 (5/25 band): trend
    Sharpe 0.62 / hold-the-seven 0.78 / 60-40 0.75 (gaps noise, SE 0.10-0.17); worst loss
    13.6% / 19.8% / 22.3%; trend best in all 6 crash windows (2008 US proxy -0.7% vs -23%;
    2022 +1.7% vs -7%) but 58 vs 31 months under water and 21 vs ~2 orders/yr. Trend = crash
    insurance only (book >= EUR 5k at EUR 1/order, >= 10k at EUR 2-3). 26 rows.
  - 22:29 UTC `eu-7` started (D, <- eu-6): trend on stock funds only; hold-seven + fixed cash.
  - DONE `wide-6` (draft #76 -> wide-5): critical-slowing-down gate fails (rising AC1 t 1.4
    to 2015, 0.1 after; rising variance adds nothing once recent vol is held fixed; last
    month's vol t 3.8 is the only predictor); `lunar` gate fails (1.6 bps/day, t 0.43). 0 rows
    (gates). Family reconciled: 68 mechanisms / 16 tested (wide and survey lists had split);
    next bar p < 0.00147. New W12-W15 queued.
  - 22:31 UTC `wide-7` started (W, <- wide-6): gates for W14 `wash-sale-echo`, W13
    `festival-gold`, W12 `rmd-december`.
  - DONE `combo-2` (draft #75 -> combo-1; merges #61 via merge commit 957fdd1): with T-bill
    interest no verdict changes (`blend-ws` 1.16 vs 1.08, p 0.051; above cash +0.06, p 0.108;
    bar p < 0.0014). `cofall-dbc` (DBC when SPY and TLT trends both down) 1.07 vs 1.08 (p 0.85),
    2022 worse (signal opened Apr 2022, DBC fell 24% after June). 1962-2025: in co-fall months
    T-bills +5.4%/yr, commodities lost. 15 rows; family 73. Combo line CLOSED.
  - 22:32 UTC `stop-reentry` started (D, <- coin-cap-4): one pre-committed coin re-entry rule.
  - DONE `survey-5` (draft #78 -> survey-4): live track records. `tsmom12` correlates 0.17
    with 9 live trend funds, 0.40 with SPY; Sharpe above T-bills 1.11 = holding the six (edge
    +0.29 in 1994-2009, 0.00 since). Paper-to-live decay: AQR TSMOM factor 1.41 -> 0.35, live
    fund 0.29 (~80%). Crash years 2008/2020Q1/2022: trend funds +7/+4/+18%, `tsmom12`
    -2/-14/-13%, holding -13/-12/-38%. Forward test cannot settle `tsmom12` vs holding (~107
    yrs). 4 `live-check` rows (not selectable).
  - 22:33 UTC `ls-trend-1` started (W, <- survey-5): is the missing crisis alpha the missing short
    side and narrow universe? (research harness only).
  - DONE `eu-7` (draft #80 -> eu-6): trend in fewer places loses the insurance. A (trend on
    stock funds only) 0.60 vs 0.62 on half the orders but -3.8% in 2022 (trend +1.7%; the 2022
    protection came from the bond slots). B (hold seven at 67% + 33% cash at 0) 0.79, worst
    loss 13.8% vs 13.6%, 31 vs 58 months under water, but -15.7% in 2008 (US proxy worst 22%
    vs 11%). Gaps noise (B-T +0.17, SE 0.13). 24 rows; eu family 12.
  - 22:37 UTC `eu-8` started (D, <- eu-7): T/B with euro cash interest; idea C (trend on stocks +
    long bonds) judged first on US proxies 1994-2011.
  - DONE `register-1` (draft #79 -> dsr-1): scoreboard read only `main`/`research-*` (285
    tries, 78 Sharpes); now every branch except `paper-trail` plus an append-only register
    `research/register/tries.jsonl` (reproduces dsr-1's census; today 2,904 tries, N 1,012 for a
    new pick). Generated `research/register/BAR.md`: a new pick needs +0.27..+0.59 Sharpe over
    `tsmom12`, Bonferroni p <= 5e-5. Regenerate: `uv run python -m grimstrade.register`.
    Convention PROPOSED in docs/DESIGN.md; DECISIONS 2026-11-12 rule revised (owner sign-off).
  - 22:39 UTC `summary-2` started (<- summary-1): rewrite `research/SUMMARY.md` for tonight's
    picture. Lane rules now require quoting BAR.md's project-wide bar.
  - DONE `summary-2` (draft #84 -> summary-1): `research/SUMMARY.md` rewritten as one page
    for tonight's picture (rule = holding + crash insurance; bar +0.27..+0.59 Sharpe; published
    effects 0 for 5). Merge into summary-1 is the owner's.
  - 22:41 UTC `insure-1` started (D, <- trend-1926-fix): is "trend = crash insurance" solid over
    1926-2025 (effective episodes, premium per unit of loss avoided)?
  - DONE `stop-reentry` (draft #82 -> coin-cap-4): `stop-cool-13` (13-week cool-off) wins 13
    of 21 (needs 17; p 0.19). Fixes bounce-buying (re-entries per fall 2.16 -> 0.52) but late
    re-entry gets worse (6 months after low +11.2% vs +16.8%). Coin years: worst loss 16.2% vs
    17.7% for 4.8 pts/yr less growth. 4 rows. Coin line stays PARKED; coin size = risk budget.
  - 22:43 UTC `rp-1` started (D, <- survey-5): `where-vol`'s 2022 loss vs live risk-parity funds.
  - DONE `wide-7` (draft #81 -> wide-6): gates W14 `wash-sale-echo` (slope t -0.07 / 0.43;
    coin placebo higher), W13 `festival-gold` (t -0.30; Baur's autumn gold effect reversed
    since 2010), W12 `rmd-december` (p 0.51) all fail. 0 rows. New W16 `geomagnetic-storm`,
    W17 `fork-premium`. List 70 / 16 tested; bar p < 0.00143. Lead to pre-register: turn-of-year
    ETF loser rebound after 2012 (t 3.9, placebos also high).
  - 22:44 UTC `wide-8` started (W, <- wide-7): forward pre-registration of the turn-of-year lead
    for 2026/27, W16 and W15 gates.
  - DONE `ls-trend-1` (draft #83 -> survey-5): crisis alpha needs BOTH shorts and a wide
    universe. Long-short vol-scaled 12-month trend on 34 keyless ETFs: +35% 2008, +25% 2020Q1,
    +13% 2022; corr 0.61 with live trend funds, 0.08 with `tsmom12`; 93-118% of crash gains from
    shorts. Long-only wide (+1/-5/-3%) and long-short narrow (+24/-11/-4%) do not reproduce it.
    Cost: Sharpe above T-bills 0.15 (2010-25), 3.7x gross, ~2%/yr costs+borrow. 4 rows
    (`replication`, not counted).
  - 22:48 UTC `ls-trend-2` started (D, <- ls-trend-1): `tsmom12` + wide long-short at <= 1x gross.
  - DONE `eu-8` (draft #85 -> eu-7): euro cash at EONIA/ESTR (ECB portal, keyless; avg +0.5%/yr
    2012-25) changes none of eu-6/eu-7's 8 conclusions (above-cash Sharpe T 0.57, B 0.73, hold
    0.72, 60/40 0.71). US proxy 1972-2025 with T-bill interest: T 0.78 vs 0.62. Idea C (trend on
    stocks + long bonds) fails both stages (US 1994-2011: 1 of 3 measures; EUR worst loss 15.9%
    vs 13.6%). 29 rows; eu family 13. eu line CLOSED; row choice in `research/eu-8.md` s.3 is
    a preference call.
  - 22:50 UTC `survey-6` started (W, <- survey-5): which strategy families paid LIVE since launch.
  - DONE `rp-1` (draft #86 -> survey-5): `where-vol` is not risk parity: equal-dollar slots,
    two coin slots carried 89% of its risk into 2022 (vol 24% vs live RP funds ~7%); coins cost
    17.3 pts in 2022. Carded fix `where-rp` (inverse-vol slots): Sharpe 1.05 = `tsmom12` (p 0.50),
    worst loss 24.5% vs 36.5% (a risk dial ~ `tsmom12` at 70%), 2022 -19.7% vs -12.8%. 4 rows.
    Do not revive `where-vol`/`blend-ws`.
  - 22:53 UTC `register-2` started (D, <- register-1): record length/skew/kurtosis in the register,
    estimated effective number of trials, per-length bar table.
  - DONE `insure-1` (draft #87 -> trend-1926-fix): 270 falls >= 25% (US market + 10
    industries, 1927-2025) = 50 independent falls. `tsmom12` lost less than holding in 48/50
    (p 1e-12), avoiding ~half of each fall; timing, not just holding less (random dates 0.27,
    fixed 73% 0.29, rule 0.50 > all 1,000 shifts). Net of the year-after-low rebound 16/50
    positive; cost per unit of loss avoided 1.07 (0.97 with T-bill cash) vs 1.63 for holding
    73%: the cheapest way to lose less. By era 0.86 / 1.38 / 1.34. Fails in fast falls
    (<= 3 months: 15/63 positive); long falls 79/80. 41 `insure-check` rows (not selectable).
  - 22:54 UTC `insure-2` started (D, <- insure-1): controls per era; same count on non-US indices.
  - DONE `ls-trend-2` (draft #89 -> ls-trend-1): `tsmom12` + wide long-short at 1x gross
    (equal risk, ~26% in `tsmom12`): Sharpe 0.97 vs 1.21 (2007-25, p 0.89) FAILS; crash windows
    2008/2020Q1/2022 +8.9/+2.2/+2.0% vs -1.6/-14.1/-12.9%, beating dilution and vol-matched
    controls (22-40% of the raw book's crash gains survive at 1x; costs 0.5%/yr). Risk choice,
    not edge. Side note: the `tsmom12`+bills control (same split) had Sharpe 1.26, max DD 5.6%
    (vol timing, not a pick; check overlap with `trend-vol` before any card). 1/3/12-month
    signal: Sharpe -0.09 at 29x turnover. 10 rows.
  - 22:59 UTC: usage data stale since 22:39 (endpoint rate-limited); holding new lanes.
  - DONE `wide-8` (draft #88 -> wide-7): year-clustered gate t-values are ~2x overdispersed
    (153 placebo windows: SD 2.18, 35% |t| >= 2), so wide-7's t 3-4 lead is ordinary. Proposed
    (not frozen) forward entry `turn-of-year-losers@1` for 2026/27 (`research/forward/
    proposed-wide8.jsonl`; pass t >= 4.87 vs stored placebos; power 8%). W16 geomagnetic
    (wrong sign, rank 29/31) and W15 hurricane claims (t 0.09) dead. New W18, W19. List 72 / 16.
  - 23:00 UTC 5h 0.63 (fresh), weekly 0.90. `wide-9` started (W, <- wide-8): W19, W17 gates,
    placebo-null method note. Reserve mode: no new lanes from 5h 0.80 until 02:15 UTC.
  - DONE `insure-2` (draft #90 -> insure-1): crash insurance holds across eras and countries
    and is cheaper than holding less, but costs more than it saves today. US premium per unit
    of loss avoided (trend / fixed / random): 1927-61 0.85/1.38/1.63, 1962-2001 1.38/2.15/2.60,
    2002-25 1.34/1.53/1.91 (1962-2025 timing test p 0.020; 2002-25 alone p 0.19). 13 developed
    non-US indices 1966-2025: lost less in 17/18 effective falls (p 7e-5), avoided 0.49,
    premium 1.11 vs 1.33/1.52. Expect ~1.3-1.5 premium (~2 log pts/yr behind holding); fails
    in fast falls. 27 `insure-check` rows. Next: `fast-reentry` on the 50 + 19 falls.
  - 23:08 UTC 5h 0.68, weekly 0.91: no new lane (would overshoot the 0.80 reserve line); running
    survey-6, register-2, wide-9.
  - DONE `register-2` (draft #92 -> register-1): trial correlation measured (mean pairwise
    0.58 over 294 weekly series 2012-25; 0.72 for 1994-2025) -> 1,027 tries = ~433 effective
    trials (old rho 0.9 assumption gave 102). New bar for a new pick: +0.30 (close) to +0.56
    (far) Sharpe over `tsmom12`, Bonferroni p <= 1.2e-4. Clustering (Lopez de Prado-Lewis) finds
    only ~2 bets (crypto-heavy vs rest). Record length dominates: on 10 years a rule needs
    +0.54..+1.00 over `tsmom12`. 410/1,016 selectable rows now carry weeks/skew/kurtosis.
    Regeneration needs local equity curves (`research/register2.local.json`, `.example`).
  - 23:08 UTC 5h 0.69: `fast-reentry` started (D, small, <- insure-2): one faster re-entry card
    judged net of the rebound over the 69 effective falls.
  - (Night-2 times above from 22:25 on ran ahead of the clock: eu-6 actually started ~22:20 UTC.)
- 3. Then the Lead 1 lane queue below.

## Lead 1 (usage run to the weekly reset, started 2026-11-17 ~22:45 UTC)

Brief: `chief-of-staff/briefs/grimstrade-lead-1.md`. One lead agent runs lanes through subagents.

- Done: lane 1 health check (all 11 live books decide and fill daily; weekly-report names fix,
  draft PR #27 -> `main`); lane 2 this summary (draft PR #28); lane 5 engineering holes as
  draft PRs to `main`: #29 G2 unfilled buy stays pending (+ sell-down inside the band to fund
  it), #30 G4 ETF dividends (ex-date cash, append-only `data/dividends.csv`), #32 Kraken fee
  tiers (lowest tier 0.80% > flat 0.60%). The three touch neighbouring `gym.py` lines: the later
  merge needs a small rebase. Interest on cash not done.
- Done overnight (all draft PRs to `carry-2` unless noted, held-out year unspent everywhere):
  - #35 `slow-1`: no input forecasts at 4 or 13 weeks (0 of 49 after correction); closest the
    dollar's 13-week change, coins only.
  - #36 `deep-1`: failure atlas of 52 models; no combination beats `tsmom12` (they hold the same
    assets and lose in the same weeks); 8 of its 10 worst drawdowns are coin tops.
  - #33 `wide-1`: 46 cross-field mechanisms, 4 carded, all fail; post-hoc: long bonds earn most
    of their return in the last 4 sessions of each month (needs its own card).
  - #34 `trend-tune`: walk-forward lookback tuning does not beat 12 months; the rule pays only on
    stocks (sits out rough stretches), re-enters ~23% above the low, 7 months late.
- Done in burst 1 (2026-11-18 11:00-11:30 UTC, the last 30 min of a 5-hour window):
  - #31 `carry-3`: the one held-out run: `band` FAILS the held-out year (pooled Sharpe -0.65,
    -8.1%, worst loss 18%); not costs, not funding (16% collected): ~22% lost on price. Held-out
    year now spent; carry-3 parked (so queue item `trend-carry` is dropped).
  - #38 `rl-4`: lasso passes the planted gate (+0.071 at IC 0.10, p 0.04); no RL variant
    passes; perp book fails (Sharpe 0.03 vs carry's 0.57).
  - #42 `rl-5` (-> rl-4): perp inputs screened by weekly return spread: none passes Holm (best
    p 0.087); lasso not run. 246 weeks detect only ~0.3%/week. Next: slower carry (cost) or
    close the RL lane.
  - #39 `usd-1` (-> slow-1): the dollar's 13-week change does not replicate (1971-1999 stock
    indexes S +0.013, p 0.44; the coin signal is an echo of BTC/ETH's 33 quarters).
  - #40 `cointop-1` (-> deep-1): coin-top exits (stop, fade, breadth) pass nowhere (BTC/ETH
    Sharpe 1.09 vs 1.05, p ~0.3; other coins ~0); they cut worst loss 36.5% -> 29-30% for 1-2
    points less growth a year: a smaller coin position, not a better rule.
  - #37 `trend-1926` (-> trend-tune): `tsmom12` beats holding on US stocks 1927-1961 (Sharpe
    0.88 vs 0.55, p 0.02; worst loss 38% vs 84%) but two thirds is 1929-1932: crash insurance,
    not an edge. Era 2 (1962-2001): Sharpe 0.88 vs 0.80 (p 0.26); without 1973-74 the lead is
    gone. Trend's lead on US stocks is 1929-32 and 1973-74 only. Open: unexplained one-day gaps
    in era 2's replay check (utilities 1.7%), no test for the `TREND_ERA=1962` path, ideas.md
    and README describe era 1 only.
  - #41 `volume-1`: own trading volume does not forecast (max |IC| 0.021 vs chance 0.048), nor
    across ~89 coins a week (max |IC| 0.020 vs 0.043). Lane closed.
  - #43 `trend-where` (-> trend-tune): per-asset walk-forward trend filter (`where-vol`) ties
    always-on `tsmom12` (1.07 vs 1.05, p 0.27); fails the bar; live rule unchanged.
    Follow-up on 1927-1961 industries: the switch kept the filter on for every industry-year
    (0 of 340 off; days out 1.3-1.8x as volatile): mechanism confirmed on stocks; the bond/gold/
    coin worst-loss question rests on 2022 alone and needs long pre-2002 bond/gold histories.
  - #44 `evo-1`: GP + Reality Check/SPA + 72 causal inputs built and tested (no real bars
    read). Toy finding: SPA over the rules a GP visited passes pure noise (p <= 0.006 in 4/4), so
    bar 3 is now a full-search replay on 20 bootstrap worlds (dated card note, before any real
    number). Lead's call: pass only if none of the 20 replays is at or above the real score
    (p < 0.05; or 40 worlds with at most one). Budget ~24 CPU-hours. Next: fast scorer vs
    `gym.simulate`, `evo_wf.py`/`evo_world.py`, controls, then the 20 replays before any search.
  - #45 `month-end-bonds` (-> wide-1): not replicated on clean data: LQD's last 4 sessions
    +10.5 bps/month after cost and drift (t 1.93, bar 2.0), Sharpe 0.52 vs 0.60 twin; TLT's first
    year -1.8 bps. Card's reading: do not spend the held-out year on it.
  - #46 `micro-1`: minute-bar features (10 years cached) do not forecast weekly: max IC 0.030 vs
    chance 0.064; best walk-forward 0.048 (bar 0.10). Can't tell 0.03-0.05 from zero.
  - #47 `wide-2` (-> wide-1): wide-1's "trend age / hazard rate" (`age4`: hold a slot only after
    4 Fridays on) fails train: Sharpe 0.99 vs 1.05, behind in 5 of 5 eras; skipping short spells
    costs more than it saves.
    Second pick E6 "patch-leaving" (`mvt`: hold only above-average in-trend assets) fails all
    five bars: Sharpe 0.85 vs 1.05, max drawdown 53% vs 37%, turnover 3.6x. Third pick G2
    `crowded-trend` (halve the book when all eligible assets trend) fails: Sharpe 0.98 vs 1.05,
    drawdown 29% vs 37% for 3 points less return a year. Picks so far: 3 of 42.
  - #48 `data-long-1`: free long histories verified: Shiller ie_data (monthly 1871-, 10y yield
    + bond total return; current file on shillerdata.com), Damodaran histretSP (annual 1928-2025,
    10y TR, Baa, gold), datahub gold monthly 1833-2026, JST R6 (annual, CC BY-NC-SA). Wire
    Shiller first; FRED timed out from this machine. Loader `research/lib/long_bond.py` done
    (1,870 monthly long-bond returns 1871-01..2026-10; needs `uv run --with xlrd`).
  - #49 `coin-cap` (-> cointop-1): a plain 10-25% cap on coin weight cuts `tsmom12`'s worst loss
    36.5% -> 28.9%, the same as `stop-0.25`, but that floor is the 2000-02 dot-com fall; a 25% cap
    costs ~1 point CAGR vs the stop's 2.2, yet inside coin-crash windows the stop beats any cap of
    the same cost (-72% vs -110% summed). Sharpe in noise; bar not met. Coin-years re-reading
    (2013-25): the stop wins (worst loss 17.7% vs 21-27% for caps of similar cost), but mostly on
    the single 2018-20 fall: close to one observation.
- Nothing running at the end of burst 1 (11:21 UTC); every lane pushed.
- Owner direction 2026-11-17: never stop early (only weekly 0.74, the reset or the Chief of
  Staff); always WIDER and DEEPER lanes. 2026-11-18: bursts use only the last 30 min of each
  5-hour window (`chief-of-staff/briefs/grimstrade-burst.md`), weekly stop 0.84.

### Lane queue (W = wider, D = deeper)

1. D `evo-1` next step: fast scorer vs `gym.simulate`, `evo_wf.py`/`evo_world.py`, timing test,
   noise/planted controls, then the 20 replay worlds; no real search before those.
2. W `data-long-1` -> gold (datahub monthly) and Damodaran cross-check next to the Shiller bond, then
   D `trend-where-long`: `where-vol` unchanged on bond/gold before 2002 (the worst-loss question
   now rests on 2022 alone).
3. D `coin-cap` follow-up: `stop-0.25` beats plain caps on coin years but on ~one episode; find
   more coin falls (the 100-coin book) before any rule PR.
4. W `wide-3`: next uncarded wide-1 mechanism; the bar counts every pick so far (4 of 42).
5. D `rl`: rl-5 says stop screening weekly perp inputs; close the RL lane or try slower carry
   (cost), both on train only (carry-3's held-out year is spent).
6. W long-horizon / other assets: trend-1926 shows trend is crash insurance on stocks; test the
   same on the long bond/gold histories once wired (needs item 2).

### For the owner

- Night 2026-11-18, register-2 (#92): accept the measured project-wide bar (433 effective
  trials; a new rule needs +0.30..+0.56 Sharpe over `tsmom12`)?
- Night 2026-11-18, wide-8 (#88): freeze the forward entry `turn-of-year-losers@1` (needs a
  `placebo_rank` metric in forward.py and changes how the registry splits its 0.10 alpha)? And
  W18 `elimination-mood` would use the 2026 World Cup, inside the held-out year: allow or not?
- Night 2026-11-18, rp-1 (#86) + eu-6..8: a smaller worst loss is available simply by holding
  `tsmom12` at a smaller size (e.g. ~70% invested); no new rule is needed. Want that?
- Night 2026-11-18, ls-trend-1 (#83): the crash gains of real trend funds need short positions
  and a wide set of assets. A forward test would need shorts in the paper broker (borrow fees,
  interest on short proceeds, leverage or rescale to 1x). Want that design change? (proposal only)
- Night 2026-11-18, register-1 (#79): adopt the project-wide tries register and "every card
  quotes BAR.md" (PROPOSED), which revises the 2026-11-12 counting rule? Once merged the live
  scoreboard's N jumps from ~300 to ~2,840 and every live deflated Sharpe drops.
- Night 2026-11-18, survey-5 (#78) + dsr-1 (#74): the live rule earns about what holding the
  same six assets earns, with smaller losses in long bear markets; no forward test settles
  "rule vs holding" in useful time. Treat it as a drawdown/risk choice, not an edge?
- Night 2026-11-18, combo-2 (#75): it merged cash-interest (#61) into its branch to test with
  T-bill interest; no verdict changed. Merging #61 into main stays your call.
- Night 2026-11-18, dsr-1 (#74): counting the whole project's search, `tsmom12` has no proven
  edge over simply holding the same assets equally (it makes money, but so does holding). The
  live scoreboard undercounts tries (307 vs ~2,811); `register-1` fixes that in a draft PR.
- Night 2026-11-18, eu-5 (#73): a 5/25 rebalance band cuts the coin-free EUR book's orders by
  a third without changing the rule. Use it in the paper runner (changes the runner's band)?
- Night 2026-11-18, forward-1 (#67, to main): adopt the forward registry and freeze
  `carry-3-band@1` (the only candidate judgeable in ~7-13 years)? Then a lane writes the
  forward adapter, and you decide whether to schedule a weekly scorer job.
- Night 2026-11-18, trend-1926-fix (#66): move `common.weekly` to the calendar Friday (own card;
  shifts every lane's numbers slightly)?
- Night 2026-11-18, cash-interest (#61, to main): (a) pay idle cash the full T-bill rate (as
  if in a T-bill fund) or a spread below it (IBKR: benchmark -0.5%, none on first USD 10k;
  Kraken: none on USD)? (b) switch the research harness's Sharpe to "above cash" too? (c) add
  the US Treasury daily bill-rate CSV as a second keyless source?
- Night 2026-11-18, eu-1 (#59): the live rule can be copied in the Netherlands with UCITS
  ETFs (US ETFs are not buyable for EU retail) and keeps its character in EUR. Want an "eu6"
  paper book in the live runner alongside the US one?
- Night 2026-11-18, coin-cap-2 (#53) + coin-cap-3 (#56): weekly `stop-0.25` on the coin slots
  of `tsmom12` gives a shallower worst loss in 15 of 21 coin-crash episodes at the same Sharpe,
  but with all 13 coin-cap picks counted the bar is p < 0.0077 and 15/21 (p 0.039) does not meet
  it; weak on BTC. A daily-checked stop (18/21, p 0.0007) adds return, not shallower losses, and
  most of it goes at double costs. So: a risk preference, not a proven rule. Rule PR? Your call.
- Burst 1 (2026-11-18): the carry book (`band`) failed its one held-out year (#31); the
  held-out year is spent there. month-end-bonds (#45) says not to spend a held-out year on it:
  that answers the earlier "owner's call". evo-1 (#44) will need ~24 CPU-hours for its replay
  worlds; say if that is too much for this machine.
- usd-1 (#39): one robustness check (the Fed's old dollar index) needs a FRED API key; it cannot
  change the verdict, so optional.
- Daily runs fire at 02:00-04:40 UTC, not 22:30 (GitHub delays scheduled jobs). No look-ahead,
  but crypto orders now fill ~22 h after the decision while backtests assume ~1.5 h. Accept, or
  move the schedule? (details: `health-1` next-steps, PR #27).
- `next-steps.md` on `main` is stale (still lists merged PR #5 as waiting).
- Engineering PRs #29 (G2), #30 (G4 dividends), #32 (fee tiers) are ready for review; merge is
  yours. Optional (trend-tune): a 2.5-5% rebalance band gave the same Sharpe with 15-25% less
  trading in backtest.
- Should the paper broker be able to fill at the close? Two wide-1 effects are worth more at the
  close than at the next open (design question).

## Summary 1 (done 2026-11-17, branch `summary-1`, draft PR #28 -> `carry-2`)

One screen for the owner on every research run so far: `research/SUMMARY.md` (what was tried, the
leads, the dead ends and why, what is not tested yet, how sure we are). Docs only, no new test. It
also covers the side branches (`ideas-1`, `invest-1`, `fm-1`, `review-1`); update it when a run ends.

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
