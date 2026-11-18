# combo-2, step 2: commodity proxies in US stock-bond co-falls, 1962-2025 (description)

Card: `combo-2.md`, step 2, "1970s-style co-falls". Not a test and not a try: monthly data, no gym, no costs. Gate at month end: US stocks' (Fama-French market) and a 10-year Treasury's (from FRED DGS10, par bond) 12-month total returns both <= 0; returns of the next month, % a year (mean monthly x 12). Gold: monthly average price, no yield. GSCI: Yahoo `^SPGSCI` (from 1985), a price index; the trend-gated column adds the T-bill to it as the collateral a futures fund earns (DBC's construction), and holds T-bills when the proxy's 12-month change is <= 0. None of these is what DBC earned.

| Years | Gate months | Stocks | T-bill | Gold | Gold if in trend, else bill | GSCI | GSCI + bill if in trend, else bill | Spells |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1962-1979 | 15 | -15.6 | +6.6 | -11.5 | -3.2 | - | - | 1966-09..1966-10, 1966-12..1966-12, 1969-07..1970-02, 1970-05..1970-06, 1973-08..1973-08, 1974-11..1974-11 |
| 1980-1993 | 5 | +21.1 | +9.5 | -14.9 | +17.8 | -51.1 | -46.4 | 1981-10..1981-10, 1984-05..1984-07, 1987-12..1987-12 |
| 1994-2005 | 2 | +37.5 | +4.9 | -3.2 | +4.9 | -12.0 | -10.9 | 1995-01..1995-02 |
| 2006-2025 | 13 | +3.5 | +2.6 | +12.4 | -4.5 | -24.8 | -16.7 | 2016-02..2016-02, 2022-05..2023-04 |
| 1962-2025 | 35 | -0.2 | +5.4 | -2.7 | -0.2 | -24.9 | -17.9 | 1966-09..1966-10, 1966-12..1966-12, 1969-07..1970-02, 1970-05..1970-06, 1973-08..1973-08, 1974-11..1974-11, 1981-10..1981-10, 1984-05..1984-07, 1987-12..1987-12, 1995-01..1995-02, 2016-02..2016-02, 2022-05..2023-04 |

Months with a 12-month history and a next month: 752 (to 2025-10).
