# Ideas 1: do the YouTube trading rules hold up?

Research run ideas-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-ideas-1.md`. Branch
`ideas-1` (from `rl-2`), draft PR #20. Source: the first YouTube harvest (8 videos), list in
`yt-harvest-1/docs/ideas/grimstrade-ideas.md`. The videos were inspiration, never truth.

## In plain words

**None of the eight rules beats the plain 12-month trend rule (`tsmom12`).** Each was written
down as a card with its pass mark before any test (`cards/yt-1.md`), run on 1994-2025, and judged
by the same bar as every earlier idea. All eight fail. The held-out year was not looked at.

| # | YouTube claim | Our rule | Verdict | Why |
|---|---|---|---|---|
| 1 | Weekly Bollinger Band Width Percentile above 95 marks a top within 0-2 months | out for 8 weeks after an upward band blow-out | **dead** | -0.04 Sharpe vs trend rule, behind it in every era. On Bitcoin it fired once (2021-01) and missed the 2017 and 2021-11 tops; on stocks it fired in strong bull years (1995-99, 2019-20). |
| 2 | Monthly stochastic RSI leaving "overbought" marks a cycle top | out for a year after the monthly K drops below 80 | **dead** | -0.23. It fires on every pause in a bull market: out of stocks and Bitcoin about half of all days. |
| 3 | Bitcoin tops ~100+ days after breaking the old all-time high | out from day 100 to day 464 after a breakout | **dead, nearest miss** | +0.08 (p = 0.18; needs < 0.10), ahead in 4 of 5 eras, smaller worst loss (29% vs 37%). But the whole gain comes from coins: four Bitcoin cycles, the same crypto winters as the halving folklore. On stocks alone it adds nothing (-0.01). Moving the window 30 days earlier removes the gain. |
| 7 | Stocks near highs while consumers are gloomy: stocks will lag | out of stocks for 6 months after the gap appears | **dead** | -0.09, behind in every era, loses on other ETFs and indexes. It fired through 2003-07, 2009-14 and 2023-25: good markets. |
| 8 | Oil supply shock (crude +50% in 6 months or doubling in a year): cut stocks | out of stocks during and 6 months after a shock | **dead** | +0.05 (p = 0.20), ties since 2003 (1.20 vs 1.20), loses on the S&P 500 1986-93 (1990 shock) and on two of three foreign indexes. It helped in 2000-09 and 2022-25 and hurt in 1994-99 and 2017-21, when the rebound from 2020 doubled oil without hurting stocks. |
| 9 | 10-year yield above ~4.6-4.8% is "debt stress": cut bonds and stocks | four versions: 3-month rise of 0.75 points, or level above 4.0 / 4.7 / 5.5% | **dead** | -0.04 to -0.01. The level has no fixed meaning: yields were above 4.7% through the good 1990s. Since 2003 the 4.7 and 5.5% lines fired only briefly (2004-07) and never after 2008, so they equal the trend rule there. |
| 10 | Stay long SPY, gold and Bitcoin while each is above its long average | 200-day and 10-month averages on SPY, GLD, BTC | **dead (it is our own plain twin)** | -0.01 and -0.03 vs `tsmom12` on the same three assets. This is the `sma200` baseline we already run. It is a fine rule; it is not a new one. |
| 12 | Contrarian on loud critics (stand-in: crypto Fear & Greed) | hold coins after "extreme fear" even against the trend; or drop them in "extreme greed" | **dead** | Buy fear -0.10 (and a worse worst loss, 48% vs 37%: it held coins in 2022's fall, era 2022-25 0.46 vs 0.88); sell greed -0.08 (behind in 2017-21, 1.19 vs 1.50: it left the rise early). Data only from 2018. |

**What this says about the videos.** The rules are plausible stories built on a handful of famous
episodes. Put into a fixed rule and run on all the history we have, each one either fires too
often (stochastic RSI, the sentiment gap, yield levels), too rarely to matter (band width on
Bitcoin), or helps in the episodes the story was told about and hurts in the others (oil shocks,
fear and greed). The trend rule already gets out when a top turns into a fall; these signals
mostly try to leave before that, and leaving early costs more than it saves.

**How sure.** The number of independent episodes is small for most of these: 4 Bitcoin cycles
for card 3 (and 4 stock bear markets on SPY), 7 oil-shock spells since 1994, 11 sharp yield
rises, 5-10 stochastic RSI exits per asset. With so few, a modest real effect could hide, and a
lucky one could show. What the tests do show: none of these adds a large, stable edge on top of
the trend rule on our book.

**For the RL agent.** Rules fail, but a few inputs are worth keeping as features (scored alone in
`results/yt-skill.md`; none is a forecast on its own, |rho| at most 0.18):

- **Days since breaking the old high** (card 3's clock): a cycle-phase input no other feature
  gives, and the one that came nearest to a pass. Use with suspicion on coins (four cycles).
- **Band width percentile** (card 1): says how stretched volatility is relative to the asset's
  own past; little overlap with the 12-month return on SPY (-0.11). Also covers the "squeeze"
  half of the claim, which a long-only rule cannot trade.
- **Distance from the 52-week high** and the **sentiment percentile** (`UMCSENT`, ALFRED vintages,
  built look-ahead safe here): regime inputs. Sentiment had the strongest single link, to bonds
  (TLT rho +0.10, t = 2.0), likely through inflation.
- **Oil 6-month change** and **10-year yield 3-month change**: regime inputs, both mildly negative
  for the next month of SPY (t about -1.6 to -1.9).
- Not worth adding: monthly stochastic RSI (rank correlation 0.6 with the 12-month return: it
  is the trend rule again) and Fear & Greed (eight years, built from price and volume the agent
  already sees).

## What was done

- `cards/yt-1.md`: the eight cards, with shared rules (gate shape, which assets each gate acts
  on, causality, twin, pass bar with bar 6 "not behind `tsmom12` since 2003", episode counting),
  committed before any indicator was computed (commit 8ac6754).
- `lib/idea_yt.py`: the runner. Price gates are computed once per panel from each asset's own
  bars, a signal counting from the first bar after its week or month ends; `idea_yt.py check`
  proves every variant gives the same weights as `gym.backtest` (which sees only visible bars)
  on five sample days. Macro inputs use `lib/macro.py`'s as-of rule: `UMCSENT` from ALFRED
  vintages, `DCOILWTICO` and `DGS10` from the day after. Fear & Greed from the day after.
- `lib/yt_skill.py` -> `results/yt-skill.md`: the indicators scored alone against the next 28
  days of SPY, TLT, GLD and BTC (method of `macro_skill.py`).
- `results/<card>.md` for bbwp, srsi, ath, gap, oil, y10, trend3, fng; `results/ath-robust.md`.
- `tries.md`: 18 card variants (+ the fng rerun, see below), their out-of-universe rows, 5
  robustness rows for card 3, and one `note` row per card naming the video id and the verdict.

## Results

Sharpe on the six assets, 1994-2025; `tsmom12` 1.05 (1.20 since 2003), equal weight 0.88.
d = Sharpe difference to `tsmom12` (paired bootstrap p). Out of universe = difference on the 8
other ETFs / 6 other coins / mean of the indexes. Spells = hostile spells 1994-2025 on SPY / BTC.

| Card | Primary | Sharpe | d (p) | Since 2003 | Worst loss | Eras ahead | Out of universe | Spells | Bars failed |
|---|---|---:|---:|---:|---:|---:|---|---|---|
| bbwp | `bbwp-and` | 1.01 | -0.04 (0.90) | 1.18 | 35.4% | 0/5 | +0.01 / -0.02 / -0.08 | 9 / 1 | 1, 2, 4, 6 |
| srsi | `srsi-and` | 0.82 | -0.23 (0.99) | 1.02 | 28.9% | 0/5 | -0.16 / +0.02 / -0.14 | 10 / 5 | 1, 2, 4, 5, 6 |
| ath | `ath-and` | 1.13 | +0.08 (0.18) | 1.37 | 28.9% | 4/5 | +0.02 / +0.09 / +0.03 | 4 / 4 | 1 |
| gap | `gap-and` | 0.95 | -0.09 (0.98) | 1.07 | 36.5% | 0/5 | -0.14 / - / -0.12 | 6 / - | 1, 2, 4, 6 |
| oil | `oil-and` | 1.10 | +0.05 (0.20) | 1.20 | 36.5% | 3/5 | +0.03 / - / -0.06 | 7 (global) | 1, 2, 4 |
| y10 | `y10chg-and` | 1.01 | -0.04 (0.98) | 1.18 | 36.5% | 1/5 | -0.01 / - / +0.06 | 11 (global) | 1, 2, 4, 6 |
| trend3 | `trend3-sma200` | 1.10 | -0.01 (0.56) | 1.25 | 34.7% | 2/5 | -0.07 / -0.04 / +0.04 | - | 1, 2, 4 |
| fng | `fng-buyfear` | 0.94 | -0.10 (0.96) | 1.04 | 47.8% | 0/5 | - / -0.10 / - | - | 1, 2, 3, 4, 6 |

`trend3` is measured on SPY, GLD and BTC only, against `tsmom12` on the same three (1.11; 1.18
since 2003); its out-of-universe rows are `sma200` against `tsmom12` on each set. Other variants:
`bbwp-alone` 0.82, `srsi-alone` 0.69, `ath-alone` 0.96, `gap-alone` 0.78, `oil-alone` 1.01 (1.32
since 2003, +0.12 against `tsmom12`, but 56% worst loss), `y10lvl40/47/55-and` 0.98 / 1.04 / 1.03,
`trend3-10m` 1.08, `fng-sellgreed` 0.97. The spell counts for `gap` apply to stocks only (the
gate never acts on coins); `oil` and `y10` are one US signal for all gated assets.

**Card 3 robustness** (`results/ath-robust.md`, after the verdict, logged as `robustness`):
window from day 70 +0.00, from day 130 +0.06, a shorter window (100-282) +0.01; acting on coins
only +0.09, on stocks only -0.01. The gain lives in the coin leg and in the exact window: the
pattern of a rule fitted to the few cycles the folklore was written about.

### Luck

18 new variants. The best gain over `tsmom12` is card 3's +0.08 (oil +0.05). Earlier runs put
the best of 52 variants at +0.24 from luck alone against equal weight; with the 13 macro and now
18 more variants that bar only rises. Nothing here comes near it.

## Assumptions and disclosures

- Prices re-fetched for this worktree on 2026-11-13 (`lib/fetch.py`); `tsmom12` and equal weight
  reproduce 1.05 and 0.88 (1.20 / 1.19 since 2003).
- Every threshold came from the video or the idea list (95th percentile, K 80, 100 days, +50% /
  doubling, 4.6-4.8%, extreme fear 24 / greed 75) or a stated convention (Bollinger 20/2, RSI 14,
  stochastic 14/3, 20% bear line, 25th percentile, 252 bars). Exit windows (8 weeks, a year, 6
  months) were the card's single choice each, from the claim's own horizon.
- Signals from a weekly or monthly bar count from the first bar of the next week or month (a
  day late at most, on the safe side); `check` proves no decision used a bar it could not see.
- Bug found and fixed: `fng-sellgreed` dropped coins before 2018, when the index has no data,
  instead of keeping the trend slot as the card says. Found by reading the first result (2010-16
  was behind `tsmom12`, impossible for a rule that equals it there), fixed, the card rerun. The
  first rows (05:49-05:50) stay in `tries.md` with a `note` row. The fix was not chosen by
  result: it makes the code match the card.
- Card file timestamp: first written as 06:10 UTC by a slip; the commit time is 05:45 UTC.
  Corrected after the tests; nothing else on the cards changed.
- A plumbing dry run (last 120 days, nothing logged) printed card 1's hostile spells before the
  logged run. Spells are not a performance number and the card was already committed.
- The `fng` cache file is the 2026-11-12 snapshot (`fear-greed/2026-11-12/fng.json`); a newer
  snapshot would need its folder name changed in `idea_yt.fng_step`.
- Not tested: #4 and #5 (vague), #6 (halving: macro-1), #11 (not in this batch), the hype list.

## Status (2026-11-13)

**Done:** eight cards, all tested on train and judged (all dead; card 3 the nearest miss), card 3
robustness, indicator skill table, this write-up, `tries.md` notes, `ideas.md` rows.

**Doing:** nothing half-finished.

**Next (not started):**

- RL agent: add days-since-breakout, band width percentile, distance from the 52-week high,
  `UMCSENT` percentile (ALFRED), oil 6-month change and 10-year 3-month change as inputs, with
  the as-of rules used here.
- Card 3 on coins can only be judged by watching: the next breakout after a 50% fall starts the
  clock again; one more cycle is one more episode.
- Harvest 2 (more videos) can reuse `cards/yt-1.md`'s shared rules and `lib/idea_yt.py`.
