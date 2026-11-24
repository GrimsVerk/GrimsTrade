# Decisions: grimstrade

Settled decisions and why, newest first. Don't relitigate; update an entry if the owner changes it.

- 2026-11-24 (own-vol 70% paper book, lane `ownvol70-1`; owner-decisions C2, answered by its
  default): one new live paper book, `own_vol_70` (`src/grimstrade/strategies/own_vol.py`),
  next to the presets; no live strategy changed. What: `tsmom12` (equal slots over the assets
  with a year of bars, a slot held while its 12-month return is positive, decided on Fridays)
  times a monthly share min(1, k / sigma), the rest in cash. sigma = `tsmom12`'s own volatility
  over the 52 complete weeks before the month; k solves mean(min(1, k / sigma_m)) = 70% over
  every monthly sigma known by the month's 1st (expanding window); share 70% until 24 sigmas
  exist or while the month's sigma is unknown; a sigma of 0 keeps the previous share; capped at
  100% (no leverage). This is exactly the no-look-ahead rule of risk-menu-3 (PR #110,
  `research/cards/risk-menu-3.md`, `research/lib/riskmenu3_run.py` `vt_expanding`); tests check
  the Friday weights, sigma and monthly share against that code on a fixture. Why: C2's default
  ("keep the presets, add one own-vol 70% book, no-look-ahead form"); the research form with
  look-ahead (k fitted on the whole window) is not used. Not an edge: on 1994-2025 its Sharpe
  lead over `tsmom12` (+0.10) is about one paired SE; it is a risk level (2007-2025: realised
  share 0.61, worst loss 15.7% against 24.6% for `tsmom12` at a fixed 70%,
  `research/risk-menu.md`).
  - Start window (assumption): the stored bars begin 2024-12, so the book's own sigma first
    exists for 2027-01 and the 24-sigma warm-up would hold it at a fixed 70% until about 2029,
    which would make it C2's option 2, not 3. So the expanding window starts with the research
    run's 362 monthly sigmas 1995-03..2025-10 (`PRIOR`, from `research/lib/ownvol_prior.py`,
    rounded to 6 decimals; k on them 0.083779, `vt_expanding`'s own last k on this checkout; the
    0.083859 risk-menu-3 printed predates the fee-tier and dividend gym changes). All of them
    come from bars that closed before 2025-11, so no decision sees past itself. Until 2027-01
    the book holds `tsmom12` at 70% ("no sigma yet"); from then the live sigmas join the window.
  - Small differences from the research harness: the live sigma uses close-to-close returns of
    the stored bars, without costs or the T-bill rate (the research sleeve was costed, measured
    over bills, on dividend-adjusted prices); a month's share is used from the first decision
    dated in that month (with the 22:30 UTC decision the reset fills on the 2nd, a day after the
    research reset); between resets the gym holds share x weights (1% band) instead of letting
    the share drift.

- 2026-11-18 (PROPOSED by lane forward-1, not yet decided by the owner): a forward-only shadow
  registry (`docs/forward-registry.md`, `src/grimstrade/forward.py`). A candidate rule is frozen
  as an append-only line in `research/forward/registry.jsonl`: sha256 of its code files,
  parameters and data source, one-sided metric, alpha, power, the effect assumed, and the minimum
  sample and years that effect needs. It counts as frozen from the commit that holds the line;
  it is scored only on bars that start after that; the verdict is read once, on exactly the
  first `min_sample` observations; a changed rule is a new id. Alpha is shared across a batch
  (four rules at 0.025 = 0.10 one-sided). Freezing a rule already counted in `research/tries.md`
  is not a new try. It runs as a separate offline command, never in the daily runner. Why:
  published effects vanished after publication three times in one night, held-out years are
  spent, and several candidates can only be judged on the future. Proposed first batch (not
  frozen): `carry-3-band@1` (~13 years needed), `fomc-bond-drift@1` (~78), `coin-stop-0.25@1`
  (~26), `eu-monthly-vs-weekly@1` (~32). Owner: adopt, and freeze which?

- 2026-11-18 (cash interest): Idle cash earns the 13-week US Treasury bill rate. Why: the gym
  paid nothing on cash, while a real account can park cash in T-bills (or a T-bill fund) and
  every backtest in the literature credits it; a book that sits in cash (e.g. trend models out
  of trend) looked worse than it would be. The rules, the same for the live record and backtests
  (`gym.simulate(rates=...)` is the one place interest is computed):
  - Rate: Yahoo's `^IRX` daily close (keyless, the same chart API as the ETF bars), the 13-week
    bill's discount rate in percent, used as an annual rate. A discount rate is a little below
    the bill's true yield (about 0.1 percentage point at 4%), which roughly pays for a T-bill
    fund's fee: the cautious side. A rate below zero is used as zero (US brokers and bill funds
    don't charge on cash).
  - Accrual: every calendar day (weekends and holidays too), on the cash held at the end of the
    UTC day, at rate / 365 (the repo's 365-day convention), credited into cash when the replay
    moves past that day, so it compounds daily. The last day of a replay (possibly still open)
    is credited by the next run. Interest is credited only once a strategy has a decision.
  - No look-ahead: the rate for day d is the newest rate known at d 00:00 UTC. A rate is known
    from its session's close (`data.close_time` for an ETF day, 21:00 UTC) in backtests, and in
    the live record from the later of that and the time the row was stored (`seen`), the way a
    decision counts from its commit (`ledger.in_force`). So the live record earns interest only
    from the day after the first run with this code; nothing earlier changes there.
  - Missing data: the last known rate carries forward (holidays, a failed fetch). Before the
    first known rate: no interest. A failed fetch is a problem line on every run until it works.
  - Negative cash (only float dust; the gym never borrows) is charged at the same rate, never
    credited.
  - Store: `data/rates.csv` (`date,rate,seen`) on the record branch, append-only like the bars:
    rows are only appended for sessions that closed at least 15 minutes ago, never rewritten.
    The first run fills it from the first stored bar (for the backtest report); `check_record`
    refuses rows no run writes (dates out of order, a weekend, a rate outside -5..30%, stored
    before its session closed or after now).
  - Sharpe is now measured above the cash rate the gym pays (the zero risk-free rate of
    2026-11-11 stays where no rate is passed). Without this a strategy that only holds cash
    would show a huge Sharpe from interest with almost no variance. Total return, drawdown and
    equity include the interest.
  Every score is replayed each run, so this changes backtests once (research train period
  1994-2025, `tsmom12` and `sixty_forty`: see PR `cash-interest`); no ledger line, bar or other
  stored row changes. Not modelled: a broker's spread below the bill rate (Interactive Brokers
  pays the benchmark minus 0.5% and nothing on the first 10,000 USD; a T-bill fund avoids that),
  and margin interest (the gym never borrows).

- 2026-11-18 (crypto fee tiers, replaces the flat 0.60% of audit G3): A crypto fill pays Kraken
  Pro's spot taker fee for the strategy's crypto volume in the 30 days before the fill (fills at
  the same open not counted). Each strategy is its own account; ETF trades are elsewhere and
  do not count. Schedule (kraken.com/pro/fees, read 2026-11-18, same as on 2026-11-12), 30-day
  spot volume in USD -> taker: 0 -> 0.80%, 2,500 -> 0.60%, 10,000 -> 0.38%, 25,000 -> 0.35%,
  50,000 -> 0.30%, 100,000 -> 0.25%, 250,000 -> 0.22%, 500,000 -> 0.20%, 1M -> 0.18%, 2.5M ->
  0.15%, 5M -> 0.12%, 10M -> 0.10% (and lower above 50M; all in `gym.KRAKEN_TAKER`). Not
  modelled: the page's 0.02% discount on "selected pairs" (it does not say whether BTC/USD and
  ETH/USD are among them; leaving it out charges more, the cautious side) and reaching a tier
  through assets held or futures volume (out of reach at 10,000 USD). Kraken's public
  `AssetPairs` endpoint lists empty fee tables now, so the page is the source. Why: the flat
  0.60% was the tier of the busiest live crypto strategy; a 10,000 USD account's tier really
  moves with what it trades: its first purchase pays 0.80%, and one that turns its crypto over
  about twice a month pays 0.38%. Every score is replayed with this table, so past results
  change once (record to 2026-11-17: `buy_hold_btc` live -17 USD, `equal_weight` -7,
  `risk_parity` and `xs_momentum` -3; backtests: `crypto_mean_reversion` +3.8% (it trades
  often enough for 0.38%), `equal_weight` -0.5%, `buy_hold_btc` -0.2%). Change the table only
  with a new entry here, giving the date the page was read.

- 2026-11-17 (audit G2): An unpaid buy waits for cash. Two rules in `gym._execute`, the same for
  live and backtests. (a) A buy the cash cannot fully pay for at its open stays pending with its
  target weight and is tried again at that asset's next open (re-sized to the equity then, band
  applied, buying only, never turned into a sell), until it fills or a newer decision of the
  same strategy replaces it. (b) At an open, when the decision's buys still pending and outside
  the band (any asset, at the latest known prices) need more than the cash on hand, every asset
  opening then that is above its target is sold down to it, even inside the 1% band. Why: each
  asset filled once at its next open and the rest was dropped. Crypto opens at 00:00 UTC, the
  ETFs at 13:30, so a switch from an ETF to crypto sat in cash until a later decision, and a
  fully invested `equal_weight` could never top up crypto that fell 1-1.6% behind: the buy found
  no cash and each ETF, alone inside the band, was never sold (health check 2026-11-17). Rule
  (b) is what a rebalancer does (sell to fund buys); with the live cron late (decision about
  03:00 UTC, ETFs open first) it is what makes the top-up happen at all. No look-ahead: every
  fill is still at an open after the decision, and a waiting buy fills at an open after the cash
  arrived. The record is not touched: every score is replayed from the ledger and the bars on
  each run, so past results change once, at the first run with this code (on the record to
  2026-11-17: `equal_weight` live +1.78 USD, `xs_momentum` +1.58, others unchanged; 700-day
  backtests of `equal_weight` -0.6% from more crypto top-ups and their fees). Not chosen:
  netting a decision into one batch at the first open (would fill ETFs at a crypto time).

- 2026-11-17 (audit G4): ETF distributions are paid into the gym as cash, on the ex-date, at
  that day's open, on the units held before the open (a unit sold at that open is paid, one
  bought there is not). Source: Yahoo's chart API with `events=div` (keyless, the same host as
  the bars; amounts per unit, split-adjusted like its prices). Stored append-only in
  `data/dividends.csv` (`symbol,ex_date,amount`) on the record branch; each daily run asks for
  the whole stored span of each ETF and appends what is new, so a failed or late answer is
  caught up next run (a failure is still a problem line). Refused, and a problem line: an
  ex-date with no stored session on and before it, an amount over 10% of the previous close.
  `check_record` refuses rows no run writes (a second payout for one day, a crypto symbol, a
  bad day or amount). Why the ex-date, not the pay date: the raw price drops at the ex-date's
  open, so paying then keeps a holder's equity whole on the day the drop shows; Yahoo gives no
  pay date. The price: the cash is spendable early (TLT and QQQ pay about a week after, SPY
  about six weeks after), at most one quarterly payout (about 0.3% of the position) a few
  weeks early, which is far smaller than the 1-4% a year missing before. The cash is not
  reinvested by itself: it sits in cash until the strategy's next decision buys back to target
  (band applied), as for a real account without automatic reinvestment. Meanwhile it earns the
  cash rate like any cash (since 2026-11-18, cash interest). Strategies do not see dividends (they decide on raw bars as before). Every score is
  replayed from the stored record each run, so stored payouts change past backtests once (700
  days to 2026-11-17: buy-and-hold SPY +2.1%, 60/40 +4.9%, equal weight +2.4%); the live
  record had no ex-date yet (it began 2026-11-11).

- 2026-11-13 (ingest 2): The finer data the daily job now collects (`grimstrade.intraday`:
  Coinbase 1-hour BTC-USD/ETH-USD, Yahoo 1-hour SPY/QQQ/GLD/TLT, Kraken Futures funding
  PF_XBTUSD/PF_ETHUSD) is **not published**: none of it goes on `paper-trail`. Terms read
  2026-11-13: Kraken Global Terms (last updated 2026-11-06) section 8 allows its content "only for
  your own benefit" and section 9 forbids to "distribute" or "make available to any third party";
  Yahoo's terms forbid using the services "to create any database, archive, ... data feed" and to
  "reproduce ... distribute" (OTOS 2(d)(10), 2(h)), and its API terms claim the API output;
  Coinbase's Market Data Terms of Use (they govern the Exchange market data API) answered 403 to
  our fetch, so unread, and unclear counts as no. Where it lives instead: a **GitHub Actions
  cache** of this repo, restored and re-saved under a new key (`intraday-<run>-<attempt>`) by the
  daily job after the record is pushed (four best-effort steps, `continue-on-error`). Why a
  cache: nobody outside can download it (there is no download API; only this repo's workflows
  restore it, and outside pull requests are off). Not artifacts: in a public repo anyone signed in
  to GitHub can download them, which is publishing, and they expire within 90 days. How long it
  survives: GitHub deletes a cache entry not read for 7 days and caps a repo at 10 GB; the daily
  job reads it every day and saves a full new copy (a few MB), so it lives as long as the daily
  job runs. A missed restore must not let a shorter fresh copy become the newest entry:
  `scripts/intraday-store.sh` skips the day when a store exists but did not restore. If the job
  stops for over a week the store is gone; the owner's local snapshots
  (`scripts/snapshot_rolling.py`, `docs/data-inventory.md`) are the backup. A cache can't be
  downloaded to a PC directly: reading it locally needs a manual job that encrypts it with a key
  the owner adds as a secret (not built; owner's call). Compared with the daily bars on
  `paper-trail`: those come from the same sources under the same terms but are public, permanent
  and tamper-evident in git, which the record needs (every score is recomputed from them); that
  existing practice stays the owner's call (`docs/data-sources.md`). The intraday files are not
  part of the record: nothing that trades or scores reads them (`tests/test_intraday_wiring.py`),
  so they need no tamper evidence. Yahoo's terms also frown on automated collection as such; the
  project already fetches Yahoo daily bars, so this adds no new kind of risk. The repository
  variable `INTRADAY_COLLECT=off` turns the collection off.

- 2026-11-12 (honesty audit 1, second review): What the record must look like, or the daily run
  refuses it (`run_daily.check_record`). One line of commits, never a merge; no commit dated
  before the one under it or in the future; no record file or folder that is a symbolic link;
  bar files with dates in order, no ETF bar on a weekend, no bar that has not closed. Only the
  daily job (`github-actions[bot]`) pushes to `paper-trail`, and only from the tip of `main`;
  any other push stops the next run until a person has looked and set `TRAIL_REVIEWED_UNTIL`.
  Accepted events are kept for good in `ledger/acknowledged-rewrites.txt`. Why: each of these
  was a way to show a result that never happened with every older check green. The price: one
  bad push stops the record until a person acts. A stopped record beats a doubtful one.
- 2026-11-12 (honesty audit 1, G3): The crypto fee is 60 bps (was 25). Why: fills at the open are
  market orders and pay the taker fee. Kraken Pro's fee page on 2026-11-12 (as served outside
  the US) lists taker 0.80% under 2,500 USD of 30-day volume, 0.60% from 2,500, 0.38% from
  10,000, 0.35% from 25,000, 0.30% from 50,000; 25 bps is below all of them. The busiest live
  crypto strategy turns its book over about 10 times a year (about 9,000 USD a month): the
  0.60% tier. One flat number is still a simplification: slower accounts really pay 0.80%,
  faster ones 0.38% or less (replaced by volume tiers on 2026-11-18, above). Every score is recomputed with
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
- 2026-11-18 (register-1, draft PR; revises the entry above): research tries are read from the
  code checkout and every local and remote branch except `paper-trail` and symbolic refs
  (`ledger.research_refs`), no longer `main` and `research-*` only, and also from the register
  `research/register/tries.jsonl` (same row rule). Why: lanes stopped using the `research-*` name
  on 2026-11-13, so the live N stopped at 307 tries while the project had logged 2,811 (dsr-1).
  A name pattern fails silently; every branch cannot. On 2026-11-18 the widened read gives 2,829
  research tries (was 285) and 534 train Sharpes (was 78). Any branch can only raise N: the
  cautious direction.
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
- 2026-11-11: Prices are raw (not dividend-adjusted). Why: adjusted history changes
  retroactively, which breaks append-only data. Dividends are paid separately as cash since
  2026-11-17 (audit G4, above).
- 2026-11-11: Sharpe uses 365 calendar days and a zero risk-free rate. Why: crypto trades every day;
  one convention for all strategies. (Since 2026-11-18 the risk-free rate is the cash rate the
  gym pays, see "cash interest".)
- 2026-11-11: No real-money broker, ever, without the owner's explicit decision. No keys in git.
- 2026-11-11: License is MIT. Why: owner's ruling.
- 2026-11-12: All three risk presets from the risk map run in paper side by side (owner: fake money,
  so no need to pick one yet). Careful and Middle are `preset_careful` / `preset_middle`, copied
  rule for rule from `research/lib/risk_map.py`; Bold is the `equal_weight` benchmark. The pick
  only matters for graduation.
- 2026-11-12: This repo is where the owner's unused usage goes. On a usage run, only the owner or
  an agreed stop (limit reset, set time) ends the work. Running out of ideas is not a stop: finish
  what is in flight, then widen the search (new fields, theories, data, new maths). Never redo
  finished analyses just to spend usage.
