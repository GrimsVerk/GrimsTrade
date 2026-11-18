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
