# live-families: which strategy families paid investors live, net of fees?

Source list: `survey-6.md` (live funds per family, matched plain holdings, published factors).
Written 2026-11-19, lane survey-6, **before any return of any fund, holding, factor or index
in this list was computed** (what was seen: `survey-6.md`, "How the list was made", including
one declared slip). This is a **descriptive check, not a strategy test**: nothing is selected,
no pass bar, no held-out data, no family count of ours changes.

Bars to quote (lane rules): our own trend family stays 65 mechanisms, 16 tested, next test at
p < 0.00154 (survey-5). Project-wide (register-1, `research/register/BAR.md` on
`origin/register-1`, 2026-11-18 22:34): **2,904 tries, N 1,012 for a new pick, Bonferroni
p <= 4.9e-5 (z 3.89)**. Neither applies to these rows (not picks); both apply to any rule a
later lane builds from what this check finds.

## Questions

1. For each strategy family, did the live funds, after fees, earn more per unit of risk than
   the plain holding an investor would otherwise have held (same months)?
2. Where a published long-short factor stands behind the family, how much of its paper Sharpe
   is left in later years and in the funds (paper-to-live decay)?
3. Which families matter mostly as risk tools: low correlation with the stock market and gains
   (or small losses) in the crash windows?

## Series (fixed now)

Code: `lib/survey6_live.py` (pushed before its run). Monthly total return from the adjusted
close at each month's last bar (distributions reinvested; for a mutual fund the NAV, so
**after fees and real costs**; sales loads are not in NAV), minus the 13-week T-bill month.
First partial month dropped. **No month after 2025-10 is read** (held-out year unspent).

Cuts for mandate changes (verified in `survey-6.md`): SPHQ from 2010-07 (a Value Line fund
before), VDIGX from 2003-01 (a utilities fund before), GATEX from 1988-01 (index calls and puts
since 1988), VGPMX to 2018-08 (Global Capital Cycles after).

Families, members and matched holdings (the plain index fund an investor would hold instead;
`bills` = cash, for funds that are market-neutral by design):

| Family | Members (matched holding) |
|---|---|
| value | DFLVX (VFINX), DFSVX (NAESX), DFIVX (VGTSX), VIVAX (VFINX), IWD (IWB), IWN (IWM), VTV (VFINX), RPV (VFINX) |
| momentum | PDP (VTSMX), MTUM (VFINX) |
| quality | SPHQ (VFINX), QUAL (VFINX) |
| low-vol | SPLV (VFINX), USMV (VFINX), ACWV (ACWI), EEMV (EEM) |
| multi-factor | DFEOX (VTSMX), DFQTX (VTSMX), LRGF (VFINX), GSLC (VFINX) |
| dividend | DVY, SDY, VIG, VYM, SCHD, VDIGX (all VFINX) |
| style premia, long-short | QSPIX, QRPIX (bills) |
| FX carry | CEW (bills) |
| merger arbitrage | MERFX, ARBFX, MNA (VBMFX, a total bond index fund: similar risk) |
| option writing | GATEX, PBP, XYLD (VFINX), QYLD (QQQ) |
| tail hedge | TAIL, VIXY, BTAL (bills), SWAN (VBINX, a 60/40 index fund) |
| gold miners | INIVX, FSAGX, VGPMX (to 2018-08, before its mandate change), GDX, GDXJ (all GLD) |
| defensive sectors | XLP, XLU, XLV, SECT (all SPY) |
| trend (survey-5's nine) | RYMFX, AQMIX, ASFYX, WTMF, PQTIX, ABYIX, DBMF, KMLM, CTA (bills) |
| risk parity (survey-5's three) | ABRZX, AQRIX, RPAR (VBINX) |

**Family composite**: equal weight of the members alive each month; its matched holding is the
equal weight of those members' matched holdings in the same month (so the comparison follows
membership). Each member is also shown alone.

Context, not families: CBOE BXM (buy-write) and PUT (put-write) indexes from the keyless CBOE
files (BXM from 2002-04, PUT daily from 2007-02; the PUT file's earlier years are a handful of
scattered points, not usable), against VFINX. Index = paper: no fees, no costs.

Published factors (long-short paper portfolios, no fees), Ken French and AQR data libraries,
rebuilt by their authors at each update (today's version of the paper data):

| Factor | Family | Paper sample S | Journal year |
|---|---|---|---|
| HML, Fama and French 1993 | value | 1963-07..1991-12 | 1993 |
| UMD (French's Mom), Jegadeesh and Titman 1993 | momentum | 1965-01..1989-12 | 1993 |
| RMW, Fama and French 2015 | quality | 1963-07..2013-12 | 2015 |
| QMJ US, Asness, Frazzini and Pedersen | quality | 1957-07..2012-12 | 2019 |
| BAB US, Frazzini and Pedersen 2014 | low-vol | 1926-01..2012-03 (file from 1930-12) | 2014 |
| CMA, Fama and French 2015 | context (no fund family) | 1963-07..2013-12 | 2015 |

Every family's **paper Sharpe** for the decay is the printed one in `survey-6.md` (bold
there), fixed now; the code's in-sample Sharpe from today's data is shown beside it.
The **live counterpart** is fixed now too, by what the paper claims:

| Family | Paper Sharpe (printed) | Live counterpart (composite, its live months) |
|---|---:|---|
| value | HML 0.55 | IR against its holding |
| momentum | PR1YR 0.81 | IR against its holding |
| quality | QMJ 0.58 (WP) and RMW 0.40 | IR against its holding |
| low-vol | BAB 0.78 | IR against its holding |
| multi-factor | value + momentum everywhere 1.59 | style premia (QSPIX, QRPIX): Sharpe above bills; long-only multi-factor: IR |
| dividend | (D/P carry 0.36, long-short) | IR against its holding |
| FX carry | currency carry 0.68 | Sharpe above bills |
| merger arb | 0.57 (after costs) | Sharpe above bills |
| option writing | PUT gap to S&P +0.33 | gap to its holding |
| risk parity | gap to 60/40 +0.13 | gap to its holding (VBINX) |
| trend | 1.41 (survey-5) | Sharpe above bills (survey-5: AQMIX 0.29, TC 0.19) |
| tail hedge, gold miners, defensive sectors | none | - |

kept = live counterpart / paper Sharpe; h = 1 - kept (computed by hand in the write-up from
the results tables, not by code).

## Measures (all that will be computed)

Per family composite and per member, over its live months to 2025-10:

1. Sharpe a year of the excess return; the matched holding's Sharpe over the same months; the
   gap.
2. OLS of the excess return on the matched holding's: alpha a year, its t, beta, and IR
   (alpha over residual sd, a year). For `bills`-matched: the mean a year and its t.
3. Correlation with VFINX; maximum drawdown of the total return, and the matched holding's.
4. Mix: 80% VFINX + 20% the composite, rebalanced monthly, minus VFINX alone: change in
   Sharpe and in maximum drawdown (same months).
5. Total return in four crash windows, against VFINX: 2000-04..2002-09, 2007-11..2009-02,
   2020-02..03, calendar 2022 (only where alive the whole window).
6. Paper factors: Sharpe in S, after S (to 2025-10), from the January after the journal year,
   and over the family composite's live months; correlation of the factor with the family's
   active return (composite minus matched); the code's kept = family IR / today's Sharpe in S
   (a second view; the write-up's h uses the printed Sharpe and the live counterpart above).
7. CBOE indexes: Sharpe, gap to VFINX, correlation, drawdowns, over the file and after 2007-06.

## Reading rules (fixed now; descriptive, no pass or fail)

- Holding-matched family: **"beat its holding"** if gap >= +0.10 and alpha t >= 2;
  **"lagged its holding"** if gap <= -0.10; otherwise **"matched its holding (no edge)"**.
- Bills-matched family: **"paid"** if Sharpe >= 0.30 and t >= 2; **"did not pay"** if
  Sharpe < 0.10; otherwise **"paid little"**.
- Multiple testing: 15 composites; a family's t is called **robust** only at the Bonferroni
  one-sided 0.05/15 level (t >= 2.94). Anything a later lane builds from a family meets the
  project-wide bar above, not this one.
- **Risk tool**: correlation with VFINX <= 0.3 **and** either (a) at least 2 crash windows
  where it beat VFINX by 10 points or more, or (b) the 80/20 mix cut VFINX's maximum drawdown
  by 3 points or more while losing at most 0.05 of Sharpe.
- **Decay**: kept < 25% = "decayed to nothing (or nearly)"; 25-60% "kept part"; > 60% "kept
  most". Survey-5's trend pair (kept 21%) is the reference.
- Members with fewer than 60 live months are shown but not read alone.
- A family "paid live" in the step-3 ranking only if it beat its holding (or paid, if
  bills-matched); a family that matched its holding is a holding, not an edge.

## What I expect (before any number)

Stated so it can be discounted: I know in general that value had a poor 2007-2020, that
covered-call funds lagged the S&P 500 in the long bull market, that long-volatility ETFs lose
steadily outside crashes, that gold miners lagged gold, and that low-volatility funds held up
in 2022. I have not computed or seen these funds' numbers in this lane.

- value: lagged or matched its holding; HML's Sharpe after 1991 well below S (kept < 50%).
- momentum, quality, multi-factor, dividend: matched their holding (gap within 0.10); quality
  maybe slightly ahead. UMD decayed; RMW/QMJ kept more than HML.
- low-vol: matched on Sharpe (lower return, lower risk), shallower 2022; BAB kept part.
- merger arbitrage: paid (Sharpe 0.4-0.8 at low risk), beat bonds, but lost in 2008: not a
  tail hedge. FX carry (CEW): did not pay.
- option writing: lagged its holding (gap -0.1 to -0.3).
- tail hedge: did not pay (negative Sharpe), risk tool yes (crash gains).
- gold miners: lagged gold.
- defensive sectors: matched SPY on Sharpe, shallower in 2000-2002 and 2008.
- trend: paid little (0.19, survey-5), risk tool yes; risk parity: matched or lagged 60/40.
- Overall: one or two families beat their holding with t >= 2; none at t >= 2.94.

## How it is logged

One `tries.md` row per family composite, kind **`live-check`** (survey-5's kind; this lane
extends its header: `<family>@live-fund` rows are live fund composites over their own months,
Sharpe = monthly excess over bills, not the repo's daily convention, turnover `-`). Not
selectable, not a strategy try. No row in `ledger/tries.jsonl`.
