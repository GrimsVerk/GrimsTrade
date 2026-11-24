# Card: breadth-book-1 — does a broader long-only universe raise `tsmom12`'s Sharpe?

Written 2026-11-24 ~19:45 UTC, before any number below is computed (no return, Sharpe,
correlation or volume of any candidate looked at in this lane). Lane `breadth-book-1`.

## Question and prior

Trend-following theory: a trend book's Sharpe grows with the number of roughly independent
markets (Hurst-Ooi-Pedersen use 60+ futures). `tsmom12` trades six. Does the same rule, unchanged,
on a wider keyless long-only universe give a higher Sharpe and a smaller worst loss?

What earlier lanes already showed (not redone, read before this card):
- `breadth-1` book B (33 markets, 2000-2025): `TS` (equal slots, trend on) 0.77-0.82, max DD
  27-28%. Not compared with the six-asset book on the same days.
- `baselines`: `tsmom12@etf` (the 8 other ETFs, 2001-2025) 0.60; `tsmom12@coin` (6 other coins,
  2017-2025) 0.54. `eu-1`: `usw` (7 US ETFs over 5 classes) 0.63 against the six's 1.37
  (2012-2025). `ls-trend-1`: long-only vol-scaled on 34 ETFs had Sharpe above bills 0.24
  (2010-2025) against 1.03 for the four live ETFs.
- `diversifier-1`: an always-held bond-like slot "beats" cash at the gym's cash-earns-0
  convention; score above T-bills from the card.

Prior, stated now: **low** that any broader book beats the live six, and near zero that one
clears the project bar. Two reasons. (1) Breadth saturates: with average pairwise correlation
rho, Sharpe grows like sqrt(N / (1 + (N - 1) rho)), at most 1 / sqrt(rho); long-only books of
mostly equity and bond ETFs have rho around 0.2-0.4, so going from 6 to 40 markets adds little
in theory. (2) The live six were picked in 2026 and hold this period's winners (QQQ, BTC, ETH);
a mechanical universe has no hindsight, and every extra slot dilutes the coins, which carried
most of the six-asset Sharpe since 2013. A broader book can still help on the worst loss.

## Data

- Train only. No bar after 2025-11-10 (`TRAIN_LAST_BAR`) is loaded; decisions to 2025-11-09.
  The held-out year is not looked at in this lane.
- ETFs: Yahoo daily bars (keyless), dividend-adjusted (total return), from the cached raw
  responses of earlier lanes (`research/data` for the harness sets; `ls-trend-1`'s raw JSON for
  the rest). BTC and ETH: the harness cache (Bitstamp/Coinbase, as every `tsmom12` row).
- Other coins: Coin Metrics community `PriceUSD` (snapshot `coinmetrics/full/2026-11-13`, which
  keeps dead coins), daily bars built as open = previous day's price, close = the day's price.
- T-bills: `^IRX` (`harness.bill_rates`).

## Candidate universes (fixed now, by rule; no return looked at)

### ETF pool and eligibility

**Pool**: every US-listed ETF named in a list an earlier card fixed for another purpose (so not
chosen for this question): the live four (SPY, QQQ, GLD, TLT), `harness.OOU_ETFS` (IWM, EFA,
EEM, IEF, LQD, VNQ, DBC, SLV), `harness.SECTORS` (XLK, XLF, XLE, XLV, XLY, XLP, XLI, XLB, XLU)
and `ls-trend`'s 34 (EWA, EWG, EWP, EWQ, EWI, EWJ, EWN, EWU, SHY, IEI, PPLT, PALL, CPER, DBB,
USO, BNO, UGA, UNG, CORN, WEAT, SOYB, CANE, DBA, FXE, FXY, FXB, FXA, FXC, FXF and the ones
above). 50 tickers. UCITS (European) listings are excluded: not US-listed.

**Eligible** if both, from bars dated on or before 2006-12-31 only:
1. first daily bar on or before 2006-07-03 (so the whole liquidity window below exists and the
   12-month signal exists at the first decision, 2008-01-02);
2. median daily dollar volume (raw close x volume) over 2006-07-01 .. 2006-12-31 of at least
   USD 1 million.

**Asset class** (fixed map): US equity = SPY, QQQ, IWM, VNQ, the nine sectors; bonds = TLT,
IEF, LQD, SHY, IEI; commodities = GLD, SLV, DBC, PPLT, PALL, CPER, DBB, USO, BNO, UGA, UNG,
CORN, WEAT, SOYB, CANE, DBA; international equity = EFA, EEM, the eight country ETFs;
currencies = the six FX trusts.

**Order** (for nested sets): round-robin over the classes in the fixed order US equity, bonds,
commodities, international equity, currencies; inside a class by the 2006-H2 median dollar
volume, largest first; a class that runs out is skipped. Robustness order (one row only):
pure 2006-H2 dollar volume, largest first, no classes.

### Coin list

Top coins by **market cap on 2019-12-31** (30-day median of `CapMrktEstUSD`, fallback
`CapMrktCurUSD`, ending 2019-12-31) among Coin Metrics assets that, on that date, (a) have a
`PriceUSD` on every day 2019-01-01 .. 2019-12-31 (a year of bars, so eligible at the first
decision), (b) are not stablecoins (annualised vol of daily log returns over the last 90 days
of 2019 >= 20%), (c) are not wrappers (90-day correlation of daily returns with BTC or ETH
< 0.95, BTC and ETH themselves kept). BTC and ETH keep the harness bars; the others use Coin
Metrics bars. Order = market cap, largest first. A coin whose price series stops is held at
its last price by the gym and drops out of the signal (count reported).

## Books (all the same rule, nothing tuned)

Primary rule = the project's `tsmom12` exactly as on the bar (`baselines.twins()["tsmom12"]`):
weekly (Friday) decisions, each eligible asset (a year of bars) gets an equal slot 1/N, the slot
is held while the asset's 365-day log return is > 0, else cash; fills at the next open; gym
costs (ETF 2 bps slippage; coins the Kraken taker tiers plus 5 bps); total-return ETF prices.

Robustness rule (the live runner's `ts_momentum` form): daily decisions, slot min(1, 40% / EWMA
vol, centre of mass 60) / N. Run only for the six and for `L-all` / `LC-all` (below).

Sets (N counts assets in the set; nested in the fixed order):

| Name | Assets | Window (decisions) |
|---|---|---|
| `six` (baseline) | SPY, QQQ, GLD, TLT, BTC, ETH | each window below |
| `four` (baseline) | SPY, QQQ, GLD, TLT | 2008-01-02 .. 2025-11-09 |
| `E-6`, `E-12`, `E-20`, `E-all` | first N eligible ETFs in the order | 2008-01-02 .. 2025-11-09 |
| `L-12`, `L-20`, `L-all` | the six, then the ordered eligible ETFs not already in, to N | 2008-01-02 .. 2025-11-09 |
| `C-2` (= BTC, ETH), `C-5`, `C-10` | first K coins of the coin list | 2020-01-01 .. 2025-11-09 |
| `LC-all` | `L-all` plus coins 3..10 of the coin list | 2020-01-01 .. 2025-11-09 |
| `L-all-vol` (robustness) | `L-all` in the pure dollar-volume order (same set if all eligible are in; then not run) | 2008-01-02 .. 2025-11-09 |

`E-all` and `L-all` hold the same ETFs; `L-all` adds BTC and ETH.

## Measures (on each window's common days; daily calendar returns, 365-day year)

1. **Sharpe above T-bills** (primary): cash earns the 13-week bill in the gym
   (`rates=bill_rates()`), Sharpe of the daily return minus the bill (`report.score`). Also the
   gym convention (cash earns 0), which is what the `tries.md` rows log.
2. **Paired difference** against `six` (and `E-*` against `four`, `C-*` against `C-2`): Sharpe
   difference, its SE from a paired stationary bootstrap (mean block 20 days, 2,000 draws, seed
   0), z = d / SE, one-sided p.
3. Worst loss (max drawdown), CAGR, worst calendar year, turnover (gym), mean exposure, and
   the return inside the harness stress windows that fall in the window.
4. **Effective number of independent bets**, at every month end from the trailing 104 weekly
   (Friday-close) log returns of the set's eligible assets: the participation ratio of the
   correlation matrix's eigenvalues, (sum l)^2 / sum l^2, and the average pairwise
   correlation; reported as the mean over month ends. Also the same on the assets the book holds
   at that month end.
5. Per era (`harness.ERAS` inside the window): Sharpe of the variant and of `six`.

## Pass bar (fixed now)

Project bar (`research/register/BAR.md`, rows through 2026-11-19): N = 486 effectively
independent trials (measured rho 0.53), **z >= 4.69** on the Sharpe edge over `tsmom12`,
Bonferroni p <= 1.0e-4. This card adds its selectable variants to that count; the bar is not
re-derived here.

A set **passes** (selectable as a new paper book) only if all hold: (a) above-bills Sharpe edge
over `six` with z >= 4.69 on the 2008-2025 window (`L-*`, `E-*`) or the 2020-2025 window
(`LC-all`); (b) worst loss not deeper than `six`'s on the same window; (c) ahead of `six` in a
majority of the eras in the window; (d) the gym-convention edge has the same sign.

**Comes close** (worth a forward paper book, not a pass): z >= 2.0 on (a) with (b) and (c). Then
the write-up gives a concrete paper-book spec (ticker list and why). A smaller worst loss with
a Sharpe edge z between -1 and 2 is reported as a **risk preference**, not an edge.

`E-*` against `four` and `C-*` against `C-2` are the clean breadth tests (no crypto dilution);
they are reported with their z but are not candidates for the paper book on their own
(`E-*` has no coins, so it competes with the live four-ETF book, not with `tsmom12`).

## Power (stated before numbers)

The primary window is ~17.9 years. A rule correlated 0.8-0.9 with the six has a paired SE of
roughly 0.10-0.15 Sharpe there (BAR.md: 0.065 on 32 years for a close rule, scaling with
1 / sqrt(years), more for less correlated rules). To reach z 4.69 the edge must be about
+0.5 to +0.7; at 80% power about +0.55 to +0.8. Breadth theory with rho 0.3 promises at most a
few tenths, and the coin dilution works the other way. So a pass is very unlikely even if
breadth helps; the useful outputs are the size and sign of the edge, the worst loss, and N_eff.
The coin window is 5.9 years: SE probably 0.2-0.3, so `C-*` and `LC-all` are descriptive.

## Survivorship

The ETF pool lists ETFs that trade today (lists written in 2026). The rule limits the damage:
membership and order use only 2006 data (existence and dollar volume), never later returns,
and the pool came from lists made for other questions. What it cannot fix: an ETF that
existed and was liquid in 2006 but later closed is missing (rare for the large US ETFs of 2006,
more likely for small currency or commodity trusts). The coin list is point in time
(2019-12-31 caps, dead coins kept in Coin Metrics); the remaining bias is Coin Metrics'
coverage. The live six carry the opposite bias (hindsight winners), which works against every
broader set here.

## Controls and look-ahead tests (in `tests/test_bbook1.py`, offline)

- Pool eligibility and order: changing any bar after 2006-12-31 does not change them.
- Coin list: changing any value after 2019-12-31 does not change it.
- N_eff at a month end: changing returns after that date does not change it; a planted
  set of k identical series plus independent ones gives about the right count.
- The fast research path gives the same weights as `gym.backtest` on sample days
  (`harness.check_against_gym`) for `L-all`.
- The script asserts no loaded bar is dated after 2025-11-10.

## Logging

One `tries.md` row per set and rule (gym convention, the harness's `run`): `six`, `four`, `C-2`
as `baseline`; `E-*`, `L-*`, `C-5`, `C-10`, `LC-all` as `variant`; the `ts_momentum`-form rows
and `L-all-vol` as `robustness`. The above-bills scores are the same decisions re-scored with
cash earning bills (`log=False`; same configuration, a scoring convention). Tables:
`research/results/breadth-book-1.md`. One real run.
