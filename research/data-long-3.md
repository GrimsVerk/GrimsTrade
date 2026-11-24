# Data long 3: keyless long histories for rates, currencies and commodities

Lane `data-long-3`, 2026-11-24 (night). Branch `data-long-3`. Research only, fake money, keyless
public data, no raw vendor data committed. No strategy is tested here (that is the next lane,
with its own card).

Why: pooled-1 (PR #142) pooled near-miss trend variants over 41 stock markets; they share one
crash calendar (cross-market correlation of the differences about 0.3), so its power stalled
near +0.13 Sharpe per market. Only asset classes with their own calendar add independent
samples: long histories of rates, currencies and commodities. None was in the cache
(data-long-1/2 gave one US 10y bond rebuilt from Shiller and datahub gold, both monthly
averages).

## Plan (written and pushed before any derived number is computed)

Sources to try, in order (spans as documented, to be read from the files):

1. **ALFRED keyless CSV**, vintage 2025-11-10 (`alfredgraph.csv?id=<ID>&vintage_date=2025-11-10`):
   the series as known on 2025-11-10, so the files hold nothing from the held-out year and no
   later revision. Plain `fredgraph.csv` timed out from this machine tonight (HTTP/2 reset, then
   no answer), as on 2026-11-18; ALFRED answered.
   - US Treasury constant-maturity yields: daily `DGS1`, `DGS2`, `DGS5`, `DGS7`, `DGS10`,
     `DGS20`, `DGS30`; monthly averages `GS1`, `GS5`, `GS10`; bills `DTB3`, `TB3MS`.
   - FX spot (Fed H.10 noon buying rates, New York): `DEXJPUS`, `DEXUSUK`, `DEXSZUS`,
     `DEXCAUS`, `DEXGEUS` (to 2001) + `DEXUSEU` (from 1999), `DEXUSAL`, `DEXUSNZ`, `DEXSDUS`,
     `DEXNOUS`.
   - Foreign short and long rates (OECD Main Economic Indicators via FRED, monthly):
     `IR3TIB01<cc>M156N` (3-month interbank), `IRLTLT01<cc>M156N` (10y government) for the
     same currencies.
   - Commodities: `PPIACO` and PPI commodity groups (BLS), `WTISPLC` (WTI monthly),
     `DCOILWTICO` (WTI daily from 1986).
2. **World Bank Commodity Price Data ("Pink Sheet")**, `CMO-Historical-Data-Monthly.xlsx`,
   monthly nominal USD prices of about 70 commodities from 1960.
3. **Yahoo daily ETF closes** for validation only: `IEF`, `TLT`, `SHY` (already cached
   2026-11-12) and the CurrencyShares trusts `FXE`, `FXY`, `FXB`, `FXF`, `FXC`, `FXA` (to fetch,
   cut at 2025-11-10).

Derived series and how each will be validated (method fixed now):

- **Bond total return from a constant-maturity yield.** Each period, buy a par bond of maturity
  M at yield y(t-1) (coupon = y(t-1), semiannual), hold it for one period, then reprice it at
  y(t) with maturity M - dt; return = price change + accrued coupon. Exact pricing, not a
  duration approximation (the duration-convexity form is shown next to it as a check). Daily
  (dt = 1/365 by calendar days) and month-end (from the last daily yield of each month).
  Validation: daily and monthly returns of the 10y (and a 7y/10y blend) against `IEF`, 20y
  against `TLT`, 2y against `SHY`, 2002/2003 to 2025-10: correlation, tracking error a year,
  mean gap a year, and the worst drawdown of each. "Good enough for a monthly trend test" means
  a monthly correlation of 0.95 or more and a mean gap within 1 point a year (an ETF pays fees
  of 0.15% and holds a spread of maturities, so a small gap is expected). Stated now; reported
  whatever it shows.
- **FX excess return (carry included).** Long the foreign currency against USD for one month,
  funded in USD: r = S(t)/S(t-1) x (1 + i_f(t-1)/12) / (1 + i_us(t-1)/12) - 1, with S in USD
  per foreign unit, i_f the foreign 3-month rate, i_us the 3-month T-bill (monthly averages
  of the month before, known at the start of the month). Spot-only returns reported next to it.
  Validation: against the CurrencyShares trusts (spot plus the deposit rate they earn, minus a
  0.40% fee), 2005/2007 to 2025-10, monthly: correlation and mean gap a year.
- **Commodities:** spot price returns only (monthly averages). A futures investor earns spot
  plus roll yield plus collateral interest; the Pink Sheet has none of the last two. Reported
  against the cached S&P GSCI series if its kind (spot, excess or total return) can be read,
  as a sign of how far spot and investable returns drift apart; no claim that spot is
  investable.

Not done here: any trend rule or strategy statistic on these series.
