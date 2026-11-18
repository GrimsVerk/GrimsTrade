# Macro 1: does knowing the macro phase help?

Research run macro-1, 2026-11-13. Brief: `chief-of-staff/briefs/grimstrade-macro-1.md`. Branch
`macro-1` (from `research-3`), draft PR #16. The first run with macro data; runs 1-3 used prices
only.

## In plain words

**No macro phase beat the 12-month trend rule in a way we can trust.** Six ideas were written
down with their pass mark before any test: step out of stocks and coins while the Fed is hiking,
while real interest rates rise fast, for a year after the yield curve inverts, while money supply
shrinks after inflation (or the Fed shrinks its balance sheet), while corporate credit spreads
widen, and, for coins only, in the "bear year" of Bitcoin's four-year halving cycle. All six fail
their bar. The held-out year was not looked at.

- **Fed, rates, money, credit: nothing.** Each of the five gates on top of the trend rule lands
  between 0.87 and 1.13 Sharpe against the trend rule's 1.05 over 1994-2025, and every one of
  them is behind the trend rule since 2003 (1.05 to 1.17 against 1.20). They cut the worst loss
  a little (29-33% against 37%) by sitting in cash more often, and they pay for it in growth
  (13-16% a year against 18%). That is the same trade a volatility cap already offers: a risk
  dial, not knowledge.
- **Why not:** the trend rule already reacts to these cycles. When the Fed tightens hard enough
  to hurt, or credit cracks, prices fall and the 12-month trend turns. The macro numbers arrive
  no earlier, and often later: inflation and money supply are published weeks after the month,
  and rate hikes mostly came in good markets (2004-06, 2017-18).
- **The nearest misses are one or two good calls each.** The yield curve gate was ahead of the
  trend rule over 1994-2025 (+0.08, not significant) because it was out of stocks through the
  dot-com bust and, by luck of timing, the covid crash; since 2003 it is behind, and it lost on
  the S&P 500 from 1962 to 1993. The Fed-hiking gate lost here but won on the S&P 500 in
  1962-1993 (+0.27, p = 0.06), the inflation decades. If inflation becomes the story again, Fed
  policy may matter again; that is a reason to keep watching it, not to trade it.
- **The Bitcoin halving cycle "works" and should not be believed.** Out of coins from 18 to 30
  months after each halving gave +0.15 Sharpe over the trend rule (+0.23 since 2003), and a
  worst loss of 29% against 37%. It formally fails the card's bar (ahead in only 3 of 5 eras,
  because the two eras before coins existed cannot differ). The deeper problem: it rests on
  three crypto winters, the 18-30 month window comes from folklore written by people who had
  watched exactly those three winters, and moving the window six months either way removes most
  or all of the gain. That is what a rule fitted to its own data looks like. The one cycle the
  folklore did not see has its window from 2025-10-19 to 2026-10-19, nearly all in the held-out
  year; it is one more episode, not a proof, whichever way it went.
- **How sure:** each result rests on few independent episodes: 5 to 7 hiking, inversion,
  liquidity and spread spells since 1994 (13 for the spread gate, which fires often and helps
  least), 3 halving winters. With so few, a real but modest effect could hide, and a lucky one
  could show. What we can say: none of these phases adds a large, stable edge on top of the
  trend rule on this book.

**For the RL agent (the owner's main goal):** macro features are still worth feeding it, for a
different reason than trading rules. A model can use them to know which regime it is in (high or
low rates, inflation or not, curve inverted or not), which no price feature tells it. Keep:
the fed funds level and its 6-month change, the real policy rate, the 10y-2y curve, the Baa
spread, real M2 growth, the unemployment rise (Sahm-like), CPI inflation, the 10-year yield, VIX,
and days since the last halving (for coins). Do not expect them to forecast next month's return:
scored alone (`results/macro-skill.md`), none has a rank correlation above 0.17 with the next
28 days of SPY, TLT, GLD or BTC. 11 of 68 feature-asset pairs have |t| above 2 where luck gives
about 3, mostly gold (it did better when rates were high, 2005-2025) and Bitcoin (labour-market
data, 2013-2025, few cycles): leads for an agent's inputs, not trading rules. They must come with the as-of rule built here (`lib/macro.py`): the same numbers taken
from today's revised data would leak the future.

## What was built

- `lib/macro.py`: the macro layer. ALFRED vintages for the six revised series (CPI, M2, payrolls,
  unemployment, industrial production, Fed balance sheet): a feature on day `d` comes from the
  vintage current on `d - 1`, never from today's revised numbers. Market series (fed funds,
  Treasury yields, curve, Baa spread, VIX) are used from the day after the observation. Before
  WALCL's first vintage (2011-07-07) its values count as public a week late. Standard library
  only. Cache path in `research/macro.local.json` (git-ignored; copy the `.example`) or
  `GRIMSTRADE_DATA`.
- `tests/test_macro_asof.py` (in the repo's checks): a value is not used on the day it was
  published, only from the next; a revision is not seen before its day; a later revision never
  reaches back; a brute-force "what did a reader see the day before" equals the fast path on
  random vintages with deleted values; scrambling every record from a date on changes nothing
  before it. The test found one bug on its first run (a vintage that dropped a value was not
  re-read until the next release), fixed before any backtest.
- `lib/macro_check.py`: the same check on the real cache (all four revised series checked match
  on 60 dates from 1995 to 2023; T10Y2Y uses the last observation strictly before the day).
- `protocol.md` "Macro tests" (written before any test): the as-of rule, risk and safe assets,
  rule shapes, card bar 6 (not behind `tsmom12` since 2003), episode counting.
- Six cards (`cards/fed-hiking.md`, `real-rate`, `yield-curve`, `liquidity`, `credit-spread`,
  `halving`), committed before any test (commit "six cards, before any test").
- `lib/idea_macro.py` runs a card: the standard test, then 2003-2025, bar 6 and the hostile
  spells. `lib/halving_shift.py`: the halving window moved six months either way (after the
  verdict, logged as robustness). `lib/macro_skill.py`: features scored alone.
- 13 variants logged in `tries.md` (plus robustness and out-of-universe rows: 48 rows).

## Results

Sharpe on the six assets; `tsmom12` 1.05 (1994-2025) and 1.20 (2003-2025), equal weight 0.88 and
1.19. dSharpe and p against `tsmom12` (paired bootstrap). Spells = hostile spells 1994-2025.
Out of universe = Sharpe difference to `tsmom12` on the 8 other ETFs / 6 coins / mean of 4 indexes.

| Card | Primary | 1994-2025 | d (p) | Since 2003 | Worst loss | Spells | Out of universe | Verdict |
|---|---|---:|---:|---:|---:|---:|---|---|
| fed-hiking | `hike-and` | 1.03 | -0.02 (0.58) | 1.09 | 28.8% | 7 | -0.11 / +0.15 / -0.01 (S&P 1962-93 +0.27) | dead |
| real-rate | `real-and` | 0.87 | -0.18 (0.99) | 1.05 | 33.0% | 14 | -0.11 / +0.06 / -0.06 | dead |
| yield-curve | `curve-and` | 1.13 | +0.08 (0.24) | 1.17 | 29.9% | 5 | -0.05 / -0.07 / -0.02 (S&P 1962-93 -0.17) | dead, nearest miss |
| liquidity | `m2-and` | 0.95 | -0.10 (0.98) | 1.11 | 36.5% | 6 | -0.05 / +0.00 / -0.11 | dead |
| liquidity | `walcl-and` | 0.95 | -0.10 (0.85) | 1.09 | 28.9% | 6 | - | dead |
| credit-spread | `spread-and` | 0.99 | -0.06 (0.77) | 1.06 | 38.8% | 13 | -0.04 / -0.06 / -0.01 | dead |
| halving | `halving-and` | 1.20 | +0.15 (0.00) | 1.42 | 28.9% | 3 | coins +0.33 (not independent) | fails bar 2; in-sample folklore |

The `-alone` forms (gate on equal weight, no trend test) answer "does the phase carry information
on its own?". Mostly no: the five non-coin gates give 0.58 to 0.97 over 1994-2025, all behind
`tsmom12`, and since 2003 all
behind equal weight except `hike-alone` (1.17) and the halving (1.52), which tie or beat it. The
gates on their own mostly remove exposure at random.

Details, stress windows, eras and spell dates: `results/<card>.md`; the shifted halving windows:
`results/halving-shift.md`; features alone: `results/macro-skill.md`.

### Luck

13 new variants. The best gain over `tsmom12` among them is the halving's (+0.15 primary, +0.23
`-alone`). Run 1-2's luck check put the best of 52 variants at +0.24 from luck alone against
equal weight; adding 13 more tries raises that bar. The halving's gain is within what luck plus
a window picked from the same data could give, which is the second reason not to trust it.

## Assumptions

- Prices re-fetched for this worktree on 2026-11-13 (`lib/fetch.py`); `tsmom12` and equal weight
  reproduce the runs' 1.05 and 0.88, and 1.20 / 1.19 since 2003.
- Thresholds (0.25 points of hikes over 182 days, a 1-point rise in the real rate over a year,
  any inversion in the last 365 days, real M2 below zero, half a point above the yearly low of
  the spread, days 548-912 after a halving) were set on the cards from the literature or the
  folklore, not tuned. Each card had one threshold.
- Safe assets (TLT, GLD, IEF, LQD) keep their trend slot under every gate.
- Monthly series older than their first vintage count as public 45 days after the 1st of the
  month. Inside 1994-2025 no series needed it; the S&P 500 1962-1993 test used it for CPI before
  1972-07 and M2 before 1980-02, with the earliest vintage's values (the first prints are not on
  record).
- FEDFUNDS (monthly) is not used; DFF (daily) is.
- Not used yet: the Treasury curve files, Shiller, Ken French, Cboe beyond VIX, Coin Metrics,
  Fear & Greed, Deribit. They are inputs for later work.

## Status (2026-11-13)

**Done:** macro layer with tests, protocol section, six cards, all tested on train and judged,
halving robustness, feature skill table, this write-up, `ideas.md` and `tries.md` updated.

**Doing:** nothing half-finished.

**Next (not started):**

- RL agent: use the features listed above as regime inputs, built with `lib/macro.py`.
- If anyone wants to test macro again, the S&P 500 1962-1993 Fed-hiking result (+0.27) is the
  one thread: a card on "hikes while inflation is above 4%" would have to be written knowing it,
  and judged on held-out data.
- The halving cycle can only be judged by watching: the next bear window opens about 548 days
  after the 2028 halving.
