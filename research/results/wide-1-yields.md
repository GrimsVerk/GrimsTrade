# wide-1, step 4: three post-hoc patterns on data no rule has seen

Definitions fixed in `wide-1.md` ("Step 4") before this data was read. Descriptive: no rule is selected, nothing is logged in `tries.md`. Bond returns are an approximation from FRED constant-maturity yields (`DGS10` from 1962, `DGS30` from 1977), close to close. "Unseen" = before 2003-08, when our TLT and IEF tests start. One deviation from the definition: carry is booked per calendar day elapsed (yield x days / 365), not as yield / 252 per session, so weekends are handled; the average is the same.

## Q1. The dip before auctions

Return of the matching par bond around each nominal auction, bps (t; events). Expected if real: negative in sessions A-4 .. A, positive in A+1 .. A+5.

| Auction | Period | Sessions A-4 .. A | Sessions A+1 .. A+5 | Sessions A-9 .. A-5 |
|---|---|---:|---:|---:|
| 30-year bond | 1980-1989 | -5.4 (-0.1; 37) | +8.4 (+0.3; 37) | -4.3 (-0.1; 37) |
| 30-year bond | 1990-2003/07 | +11.9 (+0.4; 34) | +47.9 (+2.4; 34) | +82.7 (+3.7; 34) |
| 30-year bond | unseen, pooled | +3.2 (+0.1; 72) | +26.7 (+1.5; 72) | +31.8 (+1.6; 72) |
| 30-year bond | seen 2003/08-2025 | -53.9 (-3.6; 210) | +22.4 (+1.5; 210) | +19.9 (+1.3; 210) |
| 10-year note | 1980-1989 | +11.9 (+0.4; 39) | +23.0 (+1.0; 39) | -0.5 (-0.0; 39) |
| 10-year note | 1990-2003/07 | +18.8 (+1.3; 57) | +33.7 (+2.3; 57) | +43.2 (+3.5; 57) |
| 10-year note | unseen, pooled | +16.7 (+1.1; 97) | +27.8 (+2.2; 97) | +21.4 (+1.9; 97) |
| 10-year note | seen 2003/08-2025 | -11.2 (-1.6; 250) | +11.1 (+1.5; 250) | +17.2 (+2.7; 250) |

## Q2. The month-end bond rally

Return of the par bond over the last four sessions of the month and the first three of the next, minus as many average days of the same period, bps (t; months). Expected if real: positive in the last four.

| Bond | Period | Last four sessions, excess | First three of next month, excess | Average day |
|---|---|---:|---:|---:|
| 10-year | 1962-1979 | -1.0 (-0.3; 216) | +6.8 (+1.8; 216) | +1.5 |
| 10-year | 1980-1989 | -2.7 (-0.2; 120) | +5.5 (+0.5; 120) | +4.7 |
| 10-year | 1990-2003/07 | +12.9 (+1.9; 163) | +7.1 (+1.0; 163) | +3.2 |
| 10-year | unseen, pooled | +3.1 (+0.8; 499) | +6.6 (+1.7; 499) | +2.8 |
| 10-year | seen 2003/08-2025 | +19.9 (+3.9; 267) | -14.0 (-2.4; 267) | +1.2 |
| 30-year | 1962-1979 | +3.6 (+0.3; 35) | +6.5 (+0.5; 35) | -0.1 |
| 30-year | 1980-1989 | -5.3 (-0.3; 120) | +9.3 (+0.6; 120) | +4.8 |
| 30-year | 1990-2003/07 | +23.2 (+2.2; 163) | +5.9 (+0.6; 163) | +3.4 |
| 30-year | unseen, pooled | +10.2 (+1.2; 318) | +7.2 (+0.9; 318) | +3.5 |
| 30-year | seen 2003/08-2025 | +39.2 (+3.8; 267) | -33.6 (-2.8; 267) | +1.4 |

## Q3. The month-end loser bounce

Months with |g| >= 2% at the close of T-5 (g = stocks minus the 10-year bond, month to date). Returns over sessions T-4 .. T, bps (t; months), signed so that positive is the expected direction: the month's leader falls, the month's loser rises.

| Period | Leader | Leader's side, sign flipped | Loser's side | Spread, signed |
|---|---|---:|---:|---:|
| 1962-1979 | stocks | -34.7 (-1.6; 55) | -2.3 (-0.3; 55) | -37.0 (-1.8; 55) |
| 1962-1979 | bonds | -10.4 (-1.1; 47) | +10.7 (+0.3; 47) | +0.4 (+0.0; 47) |
| 1962-1979 | either | -23.5 (-1.8; 102) | +3.7 (+0.2; 102) | -19.8 (-0.9; 102) |
| 1980-1989 | stocks | +34.2 (+1.0; 34) | -16.4 (-0.7; 34) | +17.7 (+0.5; 34) |
| 1980-1989 | bonds | -31.0 (-1.3; 34) | +52.3 (+1.3; 34) | +21.4 (+0.6; 34) |
| 1980-1989 | either | +1.6 (+0.1; 68) | +17.9 (+0.8; 68) | +19.6 (+0.8; 68) |
| 1990-2003/07 | stocks | +15.3 (+0.5; 50) | +36.5 (+2.4; 50) | +51.7 (+1.7; 50) |
| 1990-2003/07 | bonds | -32.2 (-2.2; 41) | +71.4 (+1.5; 41) | +39.2 (+0.7; 41) |
| 1990-2003/07 | either | -6.1 (-0.4; 91) | +52.2 (+2.2; 91) | +46.1 (+1.6; 91) |
| unseen, pooled | stocks | +0.1 (+0.0; 139) | +8.2 (+0.9; 139) | +8.3 (+0.5; 139) |
| unseen, pooled | bonds | -23.5 (-2.6; 122) | +42.7 (+1.7; 122) | +19.3 (+0.7; 122) |
| unseen, pooled | either | -10.9 (-1.2; 261) | +24.3 (+1.9; 261) | +13.4 (+0.9; 261) |
| seen 2003/08-2025 | stocks | +11.2 (+0.6; 114) | +29.6 (+3.8; 114) | +40.7 (+2.0; 114) |
| seen 2003/08-2025 | bonds | -7.0 (-0.5; 58) | +182.2 (+4.0; 58) | +175.1 (+3.6; 58) |
| seen 2003/08-2025 | either | +5.0 (+0.4; 172) | +81.0 (+4.7; 172) | +86.1 (+3.9; 172) |

## Cross-check on ETF closes, 2003-08 to 2025 (added after the first output)

The same close-to-close windows as Q1 and Q2, on the ETFs' own total-return closes instead of the yield series. bps (t; events).

| ETF | Window | Close to close | Excess over average days | Open to open (gym fills) |
|---|---|---:|---:|---:|
| TLT | 30-year auctions, sessions A-4 .. A | -33.7 (-2.5; 210) | -43.1 (-3.2; 210) | -15.5 (-1.1; 210) |
| TLT | 30-year auctions, sessions A+1 .. A+5 | +16.7 (+1.2; 210) | +7.3 (+0.5; 210) | +15.9 (+1.2; 210) |
| TLT | last four sessions of the month | +39.0 (+4.3; 267) | +31.5 (+3.5; 267) | +32.2 (+3.3; 267) |
| TLT | first three sessions of the month | -21.1 (-1.9; 267) | -26.8 (-2.4; 267) | -18.4 (-1.8; 267) |
| IEF | 10-year auctions, sessions A-4 .. A | -4.6 (-0.8; 249) | -12.0 (-2.1; 249) | -3.5 (-0.6; 249) |
| IEF | 10-year auctions, sessions A+1 .. A+5 | +9.2 (+1.5; 249) | +1.8 (+0.3; 249) | +5.0 (+0.8; 249) |
| IEF | last four sessions of the month | +23.6 (+5.4; 267) | +17.7 (+4.0; 267) | +21.4 (+4.5; 267) |
| IEF | first three sessions of the month | -6.1 (-1.2; 267) | -10.6 (-2.1; 267) | -3.8 (-0.8; 267) |

The same, by half of the period:

| ETF | Window | 2003-2013, close to close | 2014-2025, close to close |
|---|---|---:|---:|
| TLT | 30-year auctions, sessions A-4 .. A | -42.9 (-1.9; 68) | -29.3 (-1.8; 142) |
| TLT | 30-year auctions, sessions A+1 .. A+5 | +62.6 (+2.1; 68) | -5.2 (-0.4; 142) |
| TLT | last four sessions of the month | +39.7 (+2.8; 125) | +38.4 (+3.3; 142) |
| TLT | first three sessions of the month | -38.6 (-2.6; 125) | -5.7 (-0.4; 142) |
| IEF | 10-year auctions, sessions A-4 .. A | +3.2 (+0.3; 105) | -10.3 (-1.5; 144) |
| IEF | 10-year auctions, sessions A+1 .. A+5 | +24.3 (+2.4; 105) | -1.8 (-0.2; 144) |
| IEF | last four sessions of the month | +22.4 (+3.1; 125) | +24.8 (+4.5; 142) |
| IEF | first three sessions of the month | -12.6 (-1.8; 125) | -0.4 (-0.1; 142) |
