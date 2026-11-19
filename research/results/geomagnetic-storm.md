# Geomagnetic storms: event-study gate (wide-8, W16)

Rule: `research/wide-8.md` step 2 (pushed before this ran). Script
`research/lib/wide8_geomag.py`. Daily Ap: GFZ Potsdam (CC BY 4.0). Daily log returns,
bps a day over calm sessions; Newey-West t, 5 lags. Severe: the largest Ap of the UT
days whose six-session window holds the session is >= 100; minor: 30-99.

## Gate

| Test | Value | Needed | Met |
|---|---:|---|---|
| SPY 2003-2025 b_sev (t) | +18.2 (+2.46) | < 0, t <= -2 | False |
| SPY 2003-2025 b_sev vs b_min | +18.2 vs +0.8 | b_sev < b_min | False |
| GSPC 1950-2002 b_sev | -4.4 | < 0 | True |
| Rank of true b_sev among 31 calendars (1 = most negative) | 29 | <= 2 | False |

**Gate: fail.**

## Shown

| Sample | b_sev (t) | b_min (t) | Sev at Ap >= 50 (t) | log(1+M) slope (t) | Raw 6-session mean after severe days (n) | Counts |
|---|---:|---:|---:|---:|---:|---|
| SPY 2003-2025 (gate) | +18.2 (+2.46) | +0.8 (+0.24) | +5.4 (+1.31) | +1.6 (+0.74) | +1.34% (19) | severe days 19, minor days 328, sessions 5752, severe sessions 84, minor sessions 1168 |
| GSPC 1950-2002 (gate, in-sample) | -4.4 (-1.05) | +2.7 (+1.58) | -1.5 (-0.71) | +0.5 (+0.39) | -0.11% (108) | severe days 108, minor days 1970, sessions 13328, severe sessions 526, minor sessions 5633 |
| GSPC 2003-2025 | +18.1 (+2.46) | +0.6 (+0.19) | +5.3 (+1.29) | +1.5 (+0.72) | +1.29% (19) | severe days 19, minor days 328, sessions 5752, severe sessions 84, minor sessions 1168 |
| SPY 1993-2002 | -28.7 (-1.77) | +6.6 (+1.38) | -6.3 (-0.89) | -1.2 (-0.31) | -1.62% (11) | severe days 11, minor days 284, sessions 2495, severe sessions 66, minor sessions 891 |

## Shifted calendars, SPY 2003-2025 b_sev (bps a day)

| Shift (days) | b_sev |
|---:|---:|
| -915 | +6.1 |
| -854 | -16.0 |
| -793 | +7.2 |
| -732 | +22.7 |
| -671 | -11.3 |
| -610 | -3.5 |
| -549 | +1.6 |
| -488 | -2.8 |
| -427 | +10.7 |
| -366 | -12.9 |
| -305 | +17.9 |
| -244 | -12.9 |
| -183 | +1.8 |
| -122 | +10.3 |
| -61 | +14.6 |
| +61 | -9.6 |
| +122 | +0.2 |
| +183 | -7.2 |
| +244 | -1.7 |
| +305 | +6.0 |
| +366 | +18.3 |
| +427 | -12.8 |
| +488 | +15.4 |
| +549 | -3.4 |
| +610 | -1.0 |
| +671 | +5.0 |
| +732 | +3.0 |
| +793 | -2.6 |
| +854 | -13.3 |
| +915 | -15.1 |
