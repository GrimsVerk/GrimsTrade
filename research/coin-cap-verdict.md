# Coin risk control for `tsmom12`: verdict (coin-cap 1-4 and stop-reentry, 2026-11-18)

**Question.** The coins (BTC, ETH) cause most of `tsmom12`'s deep losses. Is any coin risk
control worth adding, and which?

**Answer.** If one is wanted, the **weekly `stop-0.25` on the coin slots** (out of a coin while
it is more than 0.25 of its yearly volatility below its one-year high, read on Fridays). It is
a **risk preference, not a proven rule.** Nothing else tried beats it.

| Six assets, train | Worst loss, coin years 2013-25 | Growth a year, coin years | Days 10%+ under water | Worst loss, 1994-2025 |
|---|---:|---:|---:|---:|
| `tsmom12` as is | 36.5% | 31.4% | 39% | 36.5% |
| weekly `stop-0.25` | **17.7%** | 25.4% | 22% | 28.9% |
| cap coins at 25% | 27.2% | 28.4% | 35% | 28.9% |
| cap coins at 15% | 17.2% | 21.6% | - | 28.9% |
| stop + 13-week cool-off | 16.2% | 20.6% | 13% | 28.9% |

**What it costs.** About 2 points of growth a year over 1994-2025, 6 points a year in the coin
years. Sharpe is about the same (1.57 against 1.40 in the coin years; 1.09 against 1.05 over
the full train). It buys a shallower worst loss and half as much time deep under water.

**What it does not fix.**
- Crashes faster than a weekly close: BTC fell 64% in two days in April 2013; every rule tried
  was out only after that.
- BTC itself: ahead of a cap of the same cost in only 1 of BTC's 5 big falls (ETH: 6 of 6).
- Re-entering a bounce before a second leg down (BTC 2017-18).
- Late re-entry after the low: -21% a year against `tsmom12` in the six months after its ten
  deepest lows.
- Length of the long bad stretches: about 1,000 days under water with or without it.

**The bar, plainly.** Across 21 separate coin-crash episodes (445 coin falls), the weekly stop
lost less than a cap of the same cost in 15. Sixteen coin risk rules have now been tried in
this family, so a real edge needs at least **17 of 21** (one-sided sign test p < 0.10 / 16).
15 of 21 (p 0.039) does not reach it. Read it as "probably helps in slow falls", not as proof.

**Tried and not better** (each counted in the 16):
- A re-entry rule (stop-reentry, the last one carded): out 13 weeks after a stop-out, then the
  band read against the high since the exit. Fixes the bounce buying (falls with repeated
  re-entries: +5% against -3%) but re-enters even later after lows (turn -24.5% a year against
  -21.0%) and holds less: 13 of 21, 4.8 points a year less growth in the coin years for a worst
  loss of 16.2% instead of 17.7%. A tighter risk dial, not a fix.
- Reading the stop daily: 18 of 21, but only by re-entering cheaper, not by losing less, and
  the gain mostly goes at double costs.
- A price band (25% below the one-year high) instead of volatility units: 16 of 21; fixes the
  2017 summer falls, but on BTC and ETH it is a looser stop (worst loss 25.2%).
- A 25% cap on top of the stop: worst loss 17.9% against 17.7%, 2.6 points less growth a year.
- Caps alone (10% to 25%, picked walk-forward): cheaper than the stop but cut less; a 15% cap
  matches the stop's worst loss at 3.8 points a year more cost.

**Should the coin line stay parked? Yes.** Sixteen rules, none passes its card (only the
daily-read stop meets the sign bar, and it fails the rest), and the last open failure (re-entry) did
not yield to a carded rule: every variant that loses less in a fall pays it back after the low.
What is left is a size choice, not research: how much coin risk to carry (the weekly stop, or a
smaller coin slot), decided as a risk budget.

**If it goes ahead.** One rule change: weekly `stop-0.25` on the coin slots. The held-out year
is still unspent; spend it once, on this rule only, if the change is wanted.

Details: `research/coin-cap.md` (six readings), `research/cards/coin-cap.md`,
`research/results/coin-cap*.md`, `research/results/stop-reentry.md`.
