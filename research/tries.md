# Tries

Every backtest variant run in the idea lab, one row each, appended by `lib/harness.py` the moment
it runs (also when the result is bad). The M1 lane counts these rows in the deflated Sharpe.
Never edit or delete a row.

- `period`: `train` or `heldout`. The held-out period is checked at most once per idea.
- `kind`: `variant` (a strategy configuration that could have been selected), `baseline`
  (benchmark or naive comparator), `robustness` (the same configuration on other data or costs,
  run after the choice was made).
- Sharpe: daily, 365 days/yr, zero risk-free rate (the repo's convention).

| UTC time | Idea | Variant | Kind | Period | From | To | Sharpe | Return | Max DD | Turnover/yr |
|---|---|---|---|---|---|---|---:|---:|---:|---:|
