# turbulence-1: does turbulence add anything a volatility trigger does not, as a crash overlay on `tsmom12`?

Lane `turbulence-1`, 2026-11-24. Branch `turbulence-1`, draft PR #134. Research only: fake
money, train data only (nothing after 2025-11-10 loaded), held-out year untouched. Card
(pushed before any number, 269b362): [`cards/turbulence.md`](cards/turbulence.md). Code and
look-ahead tests (pushed before the run, c7fb5da): `lib/turbulence1.py`,
`tests/test_turbulence1.py`. Tables: [`results/turbulence-1.md`](results/turbulence-1.md).

## The answer

**No. As a crash overlay on `tsmom12`, financial turbulence is a volatility trigger in
disguise, and its correlation part alone is worse than either. The line closes as dead.**

Overlay: on any day the trigger is on, `tsmom12`'s risk slots go to cash (next open). Turbulence
T = Mahalanobis distance of the day's return vector (trailing year, covariance shrunk a tenth
toward its diagonal, 5-day mean); trigger = above the 90th percentile of its own previous three
years. The twin uses the magnitude part M only (the same distance with correlations set to
zero: a plain cross-asset volatility measure), its percentile set so it is on just as often.

| | Six assets, 1994-2025 (primary) | Four indexes, 1962-2025 (`idx`) |
|---|---:|---:|
| `tsmom12` Sharpe | 1.04 | 0.72 |
| `turb` (T, 90th) | 0.95 | 0.83 |
| `mag-match` (M, on as often) | 0.99 | 0.82 |
| **`turb` - `mag-match`** | **-0.04 (p 0.84, z -1.0)** | **+0.01 (p 0.41, z +0.2)** |
| `corr` (C = T / M alone, 90th) | 0.97 | 0.62 |
| **`corr` - its matched twin** | **-0.07 (p 0.78)** | **-0.24 (p 0.99, z -2.4)** |
| `turb` - `tsmom12` | -0.09 (z -1.1) | +0.11 (z +1.4) |
| Trigger days shared by `turb` and `mag-match` (Jaccard, post hoc) | 0.70 | 0.80 |

- **Pass bar: both variants fail** (`turb`: 2 of 6 checks, `corr`: 2 of 6; both pass only the
  drawdown and equal-weight lines). Project bar (`register/BAR.md`, 3,130 tries, N 486
  effective trials): z >= 4.69 against `tsmom12`, an edge of +0.30. Measured: z -1.09 (`turb`)
  and -1.43 (`corr`), both behind `tsmom12` itself on the primary test.
- **Robustness at Kritzman and Li's top-quartile threshold** (`turb-q75`, out 25% of days):
  -0.01 against its matched twin (p 0.59), -0.16 against `tsmom12`.
- **Prior met.** The card put the chance of beating the matched twin at about 5%; it did not.

## Fast crashes: what the overlay does where `tsmom12` fails

Fall = S&P 500 index peak to trough inside fixed windows; rebound = the 91 days after the
trough. `idx` decides where both sets have the episode (the only set with 1987).

| Episode (peak..trough) | `tsmom12` fall | `mag-match` fall | `turb` fall | `corr` fall | `turb` - twin, fall + rebound |
|---|---:|---:|---:|---:|---:|
| 1987 (08-25..12-04), idx | -24.3% | **-6.7%** | -10.7% | -22.4% | -3.4 |
| 1998 (07-17..08-31), idx | -14.3% | -13.4% | -14.0% | -13.7% | -6.3 |
| 2011 (04-29..10-03), idx | -15.3% | -9.0% | **-6.0%** | -13.8% | +4.5 |
| 2015 (07-20..08-25), idx | -10.2% | -9.4% | -9.4% | -10.8% | +2.5 |
| 2018-Q4 (09-20..12-24), idx | -5.3% | -4.6% | -4.6% | -5.2% | 0.0 |
| 2020 (02-19..03-23), idx | -21.8% | -3.8% | -3.8% | -21.8% | 0.0 |
| 2020, six assets | -21.5% | +0.8% | -2.1% | -20.6% | -3.2 |

- **Turbulence against its twin: 1 clean win in the fall of 6 episodes** (2011; the script
  counts 2 because 2015 is a +0.0% tie; the card's reading needs 5), mean fall + rebound -0.5
  points. In 2018-Q4 and 2020 on `idx` the results are identical; in 2015 the fall is the same
  (-9.4%) but turbulence gets more of the rebound (+4.1% against +1.4%); 1987 and 1998 favour
  the twin. With six clustered episodes this is kill-only (`gate-null.md` step 7), and it
  kills.
- **The volatility overlay itself does cut the fast-crash falls.** Both `mag-match` and `turb`
  were out 3-4 business days after the 2020 peak and stayed out for most of the fall (on `idx`
  both on 88% of it, -21.8% -> -3.8%; on the six `mag-match` 88%, fall +0.8%, `turb` 83%, fall
  -2.1%, against `tsmom12`'s -21.5%), and in 1987 the trigger fired 36-37 business days after the August
  peak, days before 19 October (-24% -> -7% / -11%). That is the plain volatility part, not
  co-movement. It is not free: on the six assets the same overlay costs Sharpe overall (`mag`
  -0.05 against `tsmom12`, behind it in 4 of 5 eras, turnover 8.5 a year against 2.8), because
  most volatility spikes are not crashes and the trigger steps out and back in around them. On
  the indexes it gains +0.10 to +0.12 (p 0.08-0.11, z about 1.3-1.4). That is volatility timing
  of `tsmom12`, already filed as a risk dial and not an edge (#98, #110); it is a baseline here,
  not a pick, and far below the bar.
- **The late buy-back is untouched.** The overlay can only remove exposure; it never buys back
  sooner than `tsmom12`, and can stay out into the rebound (1998 on `idx`: `turb` -1.8% in the
  91 days after the trough against `tsmom12`'s +4.9%).

## Why turbulence adds nothing here

1. **With 1 to 6 assets the Mahalanobis distance is mostly magnitude.** log T and log M
   correlate 0.96 (six) and 0.98 (`idx`). On the six assets the signal had one asset on 19% of
   days (SPY alone until QQQ's first year, 1994-2000; turbulence is then exactly magnitude) and
   4+ on 63%. The days the two triggers disagree (142 of 811 on the six, 181 of 1,663 on
   `idx`; post hoc, see below) are not worse days: the next 20 days of the set returned +0.95% / +0.93% after
   turbulence-only days against +0.62% / +1.43% after magnitude-only days, no consistent sign
   (descriptive, no backtest).
2. **A crash moves assets the usual way.** Equities fall together and (since about 2000) bonds
   and gold hold up: that pattern is inside the trailing covariance, so the correlation
   surprise stays low exactly when `tsmom12` needs help. `corr` was on for 0-21% of each fall
   (21% of 1987 and 0% of 2020 on the indexes, 8% of 2020 on the six) and lost about what
   `tsmom12` lost. It fires on days when assets move apart, which were followed by better than
   average returns on the six (+2.13% over the next 20 days against +1.30% for all days; post
   hoc; on `idx` +0.69% against +0.55%), so it steps out of good weeks;
   turnover 11.5 (six) and 17.5 (`idx`) a year.
3. **The first big day moves everything.** In a fast crash the magnitude part crosses its
   threshold on the same day as the full distance; there is no head start for co-movement to
   give. This repeats `absorption-ratio`'s result (the eigenvalue-concentration signal lost to
   its plain volatility twin after 2010) with a second co-movement measure.

## How sure, and caveats

- One run, all 12 configurations fixed in the card. A plumbing dry run (`DRY=1`: last 120
  days, nothing logged; only its last line, an empty crash table, was looked at) came before it.
- Computed after the logged run, not in the card: the trigger-day overlap (Jaccard) and the
  20-day forward returns after trigger days (`lib/turbulence1_posthoc.py`, train only, no
  backtest, no rows; output under "Post hoc, after the run" in `results/turbulence-1.md`).
  Overlapping windows: description, not evidence.
- The matched twins set their percentile on the whole train window (90.14 for `turb`'s share
  on the six): controls, not rules anyone could have run. The same-percentile twin `mag` (a
  runnable rule) gives the same answer (`turb` - `mag` -0.05 / -0.01).
- The six-asset signal includes crypto from 2013 and 2017, whose own jumps set it off; `idx`
  (no crypto) gives the same answer, so this is not what kills it.
- `idx` uses price indexes without dividends, closes that are not simultaneous (the Nikkei
  closes before New York opens, which understates same-day correlation), and before about 2010
  Yahoo's index "open" is often the previous close, so a next-open fill there is kind to every
  overlay alike (it flatters the 1987 and 1998 rows of all overlays, not the comparison).
- The fast-crash windows are the card's own; the 2011 one (April to October) is a five-month
  fall, longer than the "three months or less" class. Six episodes, clustered: descriptive and
  kill-only.

## Rows and count

`tries.md`: 12 rows, idea `turbulence`. Six assets: 2 `variant` (`turb`, `corr`), 1
`robustness` (`turb-q75`), 4 `baseline` (`mag`, `mag-match`, `mag-match-c`, `mag-match-q75`).
`idx`: 2 `robustness` (`turb@idx`, `corr@idx`), 3 `baseline`. `tsmom12` and equal weight were
re-scored from the logged baselines (`log=False`). Weekly returns in
`register/returns/turbulence.csv.gz`, shapes in `tries-shape.jsonl`. No `ledger/tries.jsonl`
line (no live strategy). Held-out year unspent.

## For the live rule and next lanes

- Nothing changes for `tsmom12`. Its fast-crash failure stays the price of the rule, as the
  buy-back lanes found (#94, #96, #103).
- The `turbulence` line in `ideas.md` is closed (dead, tested). Together with
  `absorption-ratio` that is two co-movement signals that only repeat volatility: a third one
  (for example on a wider cross-asset panel) would need a reason to expect a different answer,
  not just more assets.
- Not proposed: a plain volatility overlay on `tsmom12` cut the 1987 and 2020 falls by about
  three quarters but cost Sharpe on the six assets. If the owner wants fast-crash cover as a
  risk choice, it belongs on the risk map next to own-volatility targeting (#110), with its
  own card and no claim of an edge.
