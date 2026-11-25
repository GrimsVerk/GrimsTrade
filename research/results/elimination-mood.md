# W18 `elimination-mood` (record-closing check): results

Rule: [`cards/wide-26b.md`](../cards/wide-26b.md) (pushed before the match file was
fetched and before any return). Code: `research/lib/wide26_w18.py`,
`research/lib/wide26_events.py`. Outcome: the losing country's index log return on the
first session after the match day, minus the other cached markets' mean change; market
dummies; Driscoll-Kraay 5 lags; rows 2006-01-01 .. 2025-10-31.

- Eliminations of mapped teams: 74 (73 on gate rows); pooled dose acf1 -0.001 ('both families' rule does not apply).
- **b -0.081% per elimination, DK t -0.95, 122576 rows; rank 6 of 41 shifted calendars (lowest = 1).**
- Null: SD 0.87, 0% past |t| 2, 5/50/95% -1.20 / -0.20 / +1.37, extremes -1.77 / +2.00.
- **Verdict: FAIL.** R18 not run (the card runs it only after a pass).

## Shown cells (not gating)

| Cell | b, % | t | Rows |
|---|---:|---:|---:|
| **Gate** | **-0.081** | **-0.95** | **122576** |
| Round weight (match number - 3) | -0.032 | -0.87 | 122576 |
| Group-stage exits | -0.031 | -0.26 | 122576 |
| Knockout wins (placebo dose, predicted 0) | -0.093 | -1.09 | 122576 |
| Own return, no world subtraction | -0.048 | -0.34 | 122576 |
| World Cup only | -0.152 | -1.73 | 122576 |
| Two sessions (s0-1 close to s0+1 close) | -0.092 | -0.61 | 122551 |

## Eliminations by team (2006-2025)

England 8, Netherlands 7, Switzerland 7, Germany 7, France 7, Spain 5, Brazil 5, Belgium 5, Mexico 4, Italy 4, Sweden 3, United States 3, Japan 3, Australia 2, South Korea 2, Austria 2

## The five largest |y| event sessions

| Market | Session | y, % |
|---|---|---:|
| BVSP | 2014-07-10 | +2.37 |
| BVSP | 2022-12-12 | -1.93 |
| FTSEMIB.MI | 2016-07-04 | -1.84 |
| GDAXI | 2012-06-29 | +1.84 |
| N225 | 2010-06-30 | -1.73 |
