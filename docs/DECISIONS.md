# Decisions: grimstrade

Settled decisions and why, newest first. Don't relitigate; update an entry if the owner changes it.

- 2026-11-12 (honesty audit 1, G3): The crypto fee is 60 bps (was 25). Why: fills at the open are
  market orders and pay the taker fee. Kraken Pro's fee page on 2026-11-12 (as served outside
  the US) lists taker 0.80% under 2,500 USD of 30-day volume, 0.60% from 2,500, 0.38% from
  10,000, 0.35% from 25,000, 0.30% from 50,000; 25 bps is below all of them. The busiest live
  crypto strategy turns its book over about 10 times a year (about 9,000 USD a month): the
  0.60% tier. One flat number is still a simplification: slower accounts really pay 0.80%,
  faster ones 0.38% or less; volume tiers are in the BACKLOG. Every score is recomputed with
  today's cost table, so changing it changes all past results too: change it only with a new
  entry here. If the owner would trade elsewhere, set that venue's taker fee.
- 2026-11-12 (honesty audit 1): Scoring conventions. (a) Every day in a record has a return, the
  first measured from the start cash, so a fill on the first day counts in Sharpe and drawdown.
  (b) Sharpe and turnover are annualised by the real time span (365 per year when there is a
  point every day). (c) No Sharpe is printed under 30 days; after that it carries its standard
  error. (d) `weekly.md` compares a strategy with each yardstick restarted with fresh cash at the
  strategy's own start (`report.restarted`), not with the yardstick's own curve. Why: each of the
  four made a number say more, or something else, than the record supports.
- 2026-11-12 (honesty audit 1): Stored bars are never corrected, but each run asks the
  first-choice source again for the last 5 stored days and appends every price difference to
  `data/revisions.jsonl`; the scoreboard counts them. Why: bars are stored about an hour after
  the close, before the source is final (the first stored day already differed).
- 2026-11-12 (honesty audit 1): The daily job runs only from `main`, never starts a new record
  unless started by hand with "start a new record", and first asks GitHub's activity log whether
  `paper-trail` was force-pushed, deleted or fed a back-dated commit
  (`scripts/check-trail-activity.sh`; the owner acknowledges an event with the repository
  variable `TRAIL_REVIEWED_UNTIL`). Why: nothing inside the branch can prove the branch itself
  was not replaced.
- 2026-11-12 (honesty audit 1): A decision counts from the time its commit was made, when that
  is later than its own timestamp (`ledger.in_force`, used by every score). Why: "append-only" did
  not stop a line being added afterwards with an old timestamp and filled at an open already
  known; the commit is the only evidence of when a line was written. Lines not yet committed
  (the run scoring its own fresh decisions) keep their timestamp. A decision recorded more than 30
  minutes after its timestamp is reported as late on the scoreboard. A decision is left out if a
  later line of the same strategy counts from the same moment or earlier. Commit dates can be
  forged by whoever can push, so GitHub's push log stays the outside witness (audit report, L1).
- 2026-11-12 (honesty audit 1): Ingest refuses a bar that opens more than 40% from the previous
  close (`data.MAX_GAP`) and any bar that fails `sources.check_sane`; an empty Yahoo day followed
  by priced days is an error. Why: stored rows can never be corrected, so a split, a glitch or a
  hole must be stopped and reported before it becomes permanent. Largest real gap in two stored
  years: 6%.
- 2026-11-12: Counting tries for the deflated Sharpe (N). N = strategies in `ledger/tries.jsonl`
  (benchmarks included; live strategies count before their first run) + the research lane's
  tries. Research tries = distinct (Idea, Variant) rows of any markdown table in
  `research/tries.md` (columns found by header name; every Kind counts, baselines and robustness
  runs included; a held-out run of a variant already counted is not a new try) + ideas in
  `research/ideas.md` whose Status is anything but `new` and that have no row in `tries.md`. Both
  files are unioned over the code checkout, `main` (local and remote) and every local/remote
  `research-*` branch. The daily runner appends every research try it sees (idea, variant, train
  Sharpe, time) to `ledger/research_tries.jsonl` on the record branch, and N and the Sharpes come
  from the union of that file and what is visible, so a deleted or unfetched branch cannot hide
  tries. Reports only read. Dead tries stay counted forever. Why:
  overcounting only makes us more cautious; undercounting is the dishonest direction.
  `ledger.research_tries` / `ledger.total_tries` implement it. (Revised after a Fable review
  found undercounting paths in the first version.)
- 2026-11-12: Deflated Sharpe inputs. Per-day Sharpe, skew and raw kurtosis of each strategy's
  daily equity returns; the variance of Sharpes across trials is the larger of 1/T (pure luck over
  T days) and the sample variance of the per-day Sharpes on the same table together with the
  research variants' logged train Sharpes (`research/tries.md`, Kind `variant`, Period `train`,
  divided by sqrt(365)). Mixing Sharpes of different lengths inflates that variance, the cautious
  direction. Shown only after 30 days. The backtest report is deflated with the same N.

- 2026-11-12: M1 classic strategies use the papers' standard parameters, never tuned on our data
  (every tuning run would be a hidden try). Where the paper doesn't fit a 6-asset, long-only,
  unlevered gym, the textbook default was picked once, here:
  - `ts_momentum` (MOP 2012): 12-month return sign, 40% vol target, EWMA vol with 60-day center
    of mass, 1/N per asset; negative signal = cash (no shorts); per-asset size capped at 1/N.
  - `xs_momentum` (J&T 1993): J=6/K=6, month-end formation, no skip week; winners = top third
    (a decile of 6 assets is empty); losers not shorted.
  - `vol_target_spy`: SPY only, Harvey et al. (2018) style: inverse vol toward a 10% target,
    re-decided daily, 21-trading-day equal-weight realized vol, capped at 100%. Not Moreira &
    Muir (2017), who scale by inverse variance of the past month, rebalance monthly and lever up
    in calm markets.
  - `risk_parity` (AFP 2012): inverse vol over the whole universe, 3-year window of daily
    returns, an asset joins after 1 year of history; unlevered (the paper levers).
  - `crypto_mean_reversion`: Connors RSI(2) < 10 (the common looser variant; the book's tested
    system uses < 5), close above 200-day SMA, exit when close above 5-day SMA, windows counted
    in daily crypto bars (calendar days); BTC and ETH, half each.
  - Vol is annualised per asset class: 365 bars/yr crypto, 252 ETFs (MOP use 261; the
    difference is under 2%). The Sharpe convention (365 days) is unchanged.
- 2026-11-12: Every strategy re-decides every day; the papers' monthly rebalancing (MOP 2012,
  AFP 2012) is not copied. The gym's 1% band is the only damping (more turnover, more whipsaw near
  a zero signal). `xs_momentum` still forms cohorts at month ends. Why: one daily decision time
  for all strategies keeps the runner simple; changing it would be a new try.
- 2026-11-12: Execution timing. Decisions run once a day at 22:30 UTC and fill at the next open.
  Crypto daily bars close at 00:00 UTC, so a crypto signal from bar d is filled at the open of
  d+2: about one day later than Connors' close-of-signal execution. `crypto_mean_reversion` is
  therefore "RSI(2) with one-day-delayed execution"; this costs it some edge and is the honest
  version of what we can run. A second, crypto-only run just after 00:00 UTC is in BACKLOG.
  `xs_momentum` counts a month as complete only once every crypto asset has its bar for that
  month end (a Fable review caught cohorts being re-picked the next day).
- 2026-11-12: Funding-rate carry is not built in M1. A keyless source exists (Kraken Futures
  `historicalfundingrates`), but carry needs a short perpetual leg and the gym is long-only spot.
  In BACKLOG.

- 2026-11-11: Daily bot writes to the `paper-trail` branch, not `main`. Why: `main` requires PRs;
  a data-only branch keeps the record's history clean and CI quiet.
- 2026-11-11: Bars and ledger are CSV/JSONL, stdlib only. Why: diff-able in git (the tamper
  evidence), no dependencies to break the unattended runner.
- 2026-11-11: Prices are raw (not dividend-adjusted); dividends are not credited yet. Why: adjusted
  history changes retroactively, which breaks append-only data. Understates SPY/TLT a little.
- 2026-11-11: Sharpe uses 365 calendar days and a zero risk-free rate. Why: crypto trades every day;
  one convention for all strategies.
- 2026-11-11: No real-money broker, ever, without the owner's explicit decision. No keys in git.
- 2026-11-11: License is MIT. Why: owner's ruling.
