# Honesty audit 1 (2026-11-12)

Auditor: lane C agent, branch `audit-1`. Scope: everything that could make the scoreboard say
something that is not true. Code audited: `main` at `8e26333` (M0), then `552e521` after the M1 merge
(merged into this branch on 2026-11-12). Record audited: `paper-trail` at
`0d3bc31` (one daily run, 2026-11-11 22:00 UTC), read-only.

## Summary for the owner

(Being written as findings land; see Status at the end for what is done.)

## Findings, ranked by how much they could mislead

Severity: **high** = the scoreboard can show a result that never happened, and nothing warns;
**medium** = numbers are biased or a safeguard is weaker than the docs say; **low** = small or
unlikely, worth knowing. Each finding names its test in `tests/test_audit_*.py`.

### L1. A decision written after the outcome is accepted (high)

- **What:** the ledger check only proves that old lines were not changed. It does not prove a
  line was written when it says it was. Anyone who can push to `paper-trail` (the three agents all
  act as GrimsBot, which has write access) can append "on day 1 at 22:31 I bought BTC" on day 4,
  after BTC doubled. The gym fills it at the day-2 open and the scoreboard shows +100%.
- **Evidence:** `tests/test_audit_ledger.py::test_a_backdated_decision_is_not_credited`.
  `gym.simulate` sorts decisions by their own `time` field; `check_append_only` passes because
  the file only grew. Nothing compares a line's `time` with the commit that first carried it.
- **Proposed fix:** (1) in the runner, refuse a ledger where a decision's `time` is not within
  ~30 minutes before the commit that introduced it; (2) since commit dates can be forged too, use
  GitHub's own push log as the outside witness: `gh api repos/GrimsVerk/GrimsTrade/activity?ref=refs/heads/paper-trail`
  already lists every push with a server-side timestamp (checked 2026-11-12: it shows the branch
  creation by `github-actions[bot]` at 22:00:52Z, 3 s after the first decisions); (3) owner:
  a ruleset on `paper-trail` (see L2).

### L2. History can be rewritten with an ordinary push (high) - FIXED in this branch

- **What:** `check_append_only` reads `git log -- <file>`. Git simplifies that log at merges: when
  a merge keeps one parent's version of the file, the other parent's history is skipped. So a
  forger builds a parallel history with a changed ledger, merges the honest branch into it keeping
  the forged file, and pushes. The result descends from the honest head, so it is a normal
  fast-forward push: no force-push needed, and a "block force pushes" rule would not stop it.
- **Evidence:** `tests/test_audit_ledger.py::test_a_rewrite_hidden_behind_a_merge_is_caught`
  (a losing all-in decision becomes "stayed in cash"; the check passes).
- **Fix (done, `ledger.py`):** `check_append_only` now walks every commit and compares the file
  with its version in each parent, instead of trusting the simplified log. A ledger deleted from
  the working tree is also refused now.

### L3. A force-push or delete-and-recreate of `paper-trail` leaves no trace in the repo (high)

- **What:** if the whole branch is replaced, the new history is self-consistent; no check that
  only reads the branch can know an older one existed. Today nothing stops it: the only ruleset
  (`protect-main`) covers the default branch only, and GrimsBot (all agents) has push rights.
- **Evidence:** `tests/test_audit_ledger.py::test_a_force_pushed_history_passes_the_check`;
  `gh api repos/GrimsVerk/GrimsTrade/rulesets` lists only `protect-main` with
  `include: ["~DEFAULT_BRANCH"]`.
- **Proposed fix:** (owner, needs admin) add a ruleset for `paper-trail`: block force pushes and
  deletion, no bypass. (Workflow, small) before running, ask GitHub's activity log for
  `force_push` / `branch_deletion` events on `paper-trail` and refuse to run if there are any:
  `tests/test_audit_workflow.py::test_the_job_checks_githubs_activity_log_for_a_rewritten_trail`.

### L4. Stored bars can be edited and nothing notices (high) - FIXED in this branch

- **What:** the scoreboard is recomputed from `data/bars/*.csv` on every run, so the bars are as
  much "the record" as the decisions. AGENTS.md forbids rewriting them, but only the two ledger
  files are checked. Changing one cell (the open a strategy bought at) rewrites its whole result.
- **Evidence:** `tests/test_audit_ledger.py::test_a_rewritten_bar_is_caught`: one edited open
  turns a small loss into +99%, and the next run accepts it.
- **Fix (done, `run_daily.py`):** the run applies the same append-only check to every file in
  `data/bars/` and refuses to run if a committed row changed.

### L5. A failed fetch starts a brand-new record (medium)

- **What:** the workflow does `git fetch origin paper-trail || git worktree add --orphan`. If
  the branch was deleted, the bot silently starts a fresh record and the old one is gone from
  the scoreboard. If the fetch only failed for a moment (network), it also builds an orphan; the
  push is then rejected, so that day's decisions are lost.
- **Evidence:** `.github/workflows/daily.yml` lines 33-37;
  `tests/test_audit_workflow.py::test_a_failed_fetch_does_not_start_a_new_record`.
- **Proposed fix (small, workflow):** ask `git ls-remote` whether the branch exists; create the
  orphan only when the remote answers "no such branch" and the run was started by hand with an
  explicit "start a new record" input.

### L6. Outside a git checkout the check silently checks nothing (low)

- **What:** with `--root` on a plain folder, or on a `trail/` folder that is not a worktree
  (`/trail/` is gitignored in the code repo), `check_append_only` returns 0 and the runner ignores
  that. Mostly a trap for local runs.
- **Evidence:** `tests/test_audit_ledger.py::test_outside_a_git_checkout_the_check_silently_checks_nothing`.
- **Proposed fix:** the runner prints how many committed versions it verified and refuses a
  non-empty ledger with none.

### L7. A decision does not say which code made it (medium)

- **What:** strategy names key the ledger, but a strategy's code or parameters can change under
  the same name. The scoreboard then shows one unbroken track record, and `tries.jsonl` counts one
  try, for what were really two strategies. The daily job runs whatever is on `main` that day.
- **Evidence:** `tests/test_audit_ledger.py::test_a_decision_records_the_code_version`; the
  first real ledger lines have no code reference.
- **Proposed fix (small, `ledger.py`):** write the commit SHA of the code (`GITHUB_SHA`) into
  each decision line. Later: the scoreboard starts a new row when a strategy's code changes.

### L8. The daily job can be started from any branch (medium)

- **What:** `workflow_dispatch` runs the workflow file and code of whatever branch is chosen
  (`gh workflow run daily.yml --ref m1`). That code then writes to the one official record:
  unmerged strategies, a different gym, a different report.
- **Evidence:** `.github/workflows/daily.yml` has no branch condition;
  `tests/test_audit_workflow.py::test_the_job_only_runs_code_from_main`.
- **Proposed fix (small, workflow):** `if: github.ref == 'refs/heads/main'` on the job.

### D1. A bar taken soon after the close is frozen, and later corrections are never seen (high)

- **What:** an ETF bar is stored once it is 15 minutes past 21:00 UTC and is never looked at
  again: the next run asks the source only for newer days. If the source's numbers for that day
  were not final yet, the record keeps the early ones for ever and nobody is told they differ.
  Every fill and every mark on that day uses them.
- **Evidence (real):** the first run stored the 2026-11-11 ETF bars at 22:00:49 UTC, one hour
  after the close. In all four ETF files that row is the only one of 481 whose volume is not a
  multiple of 100 (SPY 37,707,134), the mark of a row Yahoo had not finalised. At 01:38 UTC,
  4.5 hours after the close, Yahoo's chart API returned that same SPY row with `close: null` and
  the same volume: still being rewritten. Test: `tests/test_audit_data.py::test_a_revised_bar_is_reported`.
- **Proposed fix (medium, `run_daily.py` + `data.py`):** each run, re-fetch the last ~5 stored
  days and compare (with a small tolerance); never change stored rows, but write every difference
  to an append-only `data/revisions.jsonl` and to the run's problem list. Cheap extra safety: move
  the cron later (e.g. 23:30 UTC) so the row has had 2.5 hours instead of 1.5 to settle.

### D2. A stock split would be booked as a crash (high impact, unlikely for today's four ETFs) - GUARDED in this branch

- **What:** Yahoo's prices are split-adjusted backwards. After a split, new rows arrive in
  post-split prices; stored rows and the units a strategy holds are pre-split. The gym would show
  -50% overnight for a 2-for-1 split, for ever.
- **Evidence:** `tests/test_audit_data.py::test_a_split_is_not_stored_as_a_crash`. Real stored
  history is clean so far: the largest overnight gap in 481 days is 6.0% (GLD).
- **Guard (done, `data.py`):** `append` stores the bars before it and then refuses a bar whose
  open is more than 40% (`MAX_GAP`) away from the previous close; the run reports it every day
  until a person decides. Still open (larger): fetch split events (`events=div,splits`) and
  adjust held units, so a split is handled instead of only stopped.

### D3. No sanity check before a bar becomes permanent (medium) - FIXED in this branch

- **What:** zero, negative or inconsistent prices (low above open, and so on) go straight into
  the store. A zero open makes the gym divide by zero, so the daily run crashes every day and the
  bad row cannot be removed without breaking the append-only rule.
- **Evidence:** `tests/test_audit_data.py::test_a_nonsense_bar_is_not_stored`.
- **Fix (done, `sources.py`):** `fetch` runs `check_sane` on every bar (finite, positive, low
  and high consistent with open and close, 0.1% slack); a bad bar counts as a failed source, so
  the next source is tried and the problem is reported. All 3,324 real stored bars pass.

### D4. A hole in the middle of a source's answer becomes a permanent gap (medium) - FIXED in this branch

- **What:** `yahoo()` skips rows whose prices are null. That is right for the newest row (not
  published yet, retried tomorrow). But if a null row is followed by good rows, the good ones are
  stored and the skipped day can never be added, because only bars newer than the last stored one
  are appended. The gym then treats it as a market holiday.
- **Evidence:** `tests/test_audit_data.py::test_a_hole_in_the_sources_answer_is_not_skipped_silently`.
  Real stored history has no holes (crypto: 700 consecutive days; the four ETFs share one calendar).
- **Fix (done, `sources.py`):** an empty Yahoo day with priced days after it makes `yahoo()`
  raise, so the next source is tried and the run reports it; an empty newest day is still just
  retried tomorrow. Assumption: Yahoo lists no row at all for market holidays (true for all 481
  stored sessions); if it ever lists an empty one, ETF ingest stops loudly until someone adds an
  exception. Still open: a day the source omits completely (a calendar check across symbols).

### D5. The record does not say where a bar came from (low)

- **What:** when Kraken fails the bar comes from Coinbase (another exchange, slightly other
  prices: on 2026-11-10 BTC open 75,253.1 vs 75,257.8, low 72,584.6 vs 72,643.5, about 8 basis
  points apart at worst). When Yahoo fails it comes from Stooq, whose history is, as far as I
  know, dividend-adjusted where Yahoo's is raw (not verified, see D6). Nothing in `paper-trail`
  records which source was used, so a mixed series cannot be recognised later.
- **Evidence:** `tests/test_audit_data.py::test_the_record_says_which_source_each_bar_came_from`.
- **Proposed fix (small-medium):** an append-only `data/sources.jsonl`: one line per run and
  symbol (source, first and last date, rows).

### D6. The ETF fallback source does not work (medium, for "runs without anyone")

- **What:** on 2026-11-12 `https://stooq.com/q/d/l/?s=spy.us&i=d` answered HTTP 200 with a
  JavaScript "verify your browser" page instead of CSV. The code treats that as a failed source
  (good, and pinned by a test), so the ETFs have one working source. If Yahoo blocks GitHub's
  runners, ETF prices stop; strategies holding ETFs then look calm and flat (see S4).
- **Evidence:** live probe; `tests/test_audit_data.py::test_stooq_browser_check_page_is_an_error_not_data`.
- **Proposed fix:** a second real ETF source (Alpaca's free data is in the BACKLOG; needs a key
  as an Actions secret, the owner's call).

### S1. A Sharpe ratio is printed from day two (high, because it is the number people read)

- **What:** the table shows Sharpe to two decimals for any record of two days or more. For short
  records it is noise: four up-days read as "Sharpe 30"; a strategy that only paid 2 basis points
  of slippage once shows -4.6. After 30 days a strategy with no skill at all shows a Sharpe
  outside +-3.7 a third of the time (95% band +-7.3).
- **Evidence:** `tests/test_audit_stats.py::test_a_record_of_a_few_days_shows_no_sharpe_number`.
- **Proposed fix (small, `report.py`, M1 is editing it):** no Sharpe (and no ranking by it)
  under 30 days; from then on print it with its error band, e.g. `0.8 +-2.8`.

### S2. After six months the board still mostly measures luck (high)

- **What:** the graduation bar says "at least 6 months". The uncertainty of an annualised Sharpe
  from daily returns is about sqrt(365/days): +-3.7 (one standard error) at 30 days, +-1.4 at
  180 days, +-1.0 at one year, +-0.7 at two. With nine strategies of zero skill running for 180
  days, the best one shows a Sharpe of about 2.1 on average and above 2 in more than half of all
  cases. Returns are as noisy: over 180 days a BTC-like asset with no drift ends anywhere between
  -48% and +94% (5th to 95th percentile), a SPY-like one between -17% and +21%. "Beat buy-and-hold
  BTC by 10% over six months" is well inside luck.
- **Evidence:** `tests/test_audit_stats.py::test_nine_strategies_with_no_skill_after_six_months_the_best_looks_skilled`
  (seeded simulation, numbers above reproduced).
- **Proposed fix:** the M1 branch is adding the deflated Sharpe, which is the right tool; it
  should be the headline column, not a footnote. Print the error band next to every Sharpe.
  Change the graduation bar from "6 months" to "deflated Sharpe above 95%, and at least 6
  months": for a true Sharpe of 1 that takes roughly 3-4 years of daily data, and the owner should
  know that now rather than in May.

### S3. Returns over different periods are ranked in one table (medium)

- **What:** each row's return runs from that strategy's own first decision, and the table is
  sorted by it. Two strategies holding exactly the same thing rank apart by start date alone, and
  every M1 strategy starts later than the four benchmarks it has to beat.
- **Evidence:** `tests/test_audit_stats.py::test_the_same_strategy_started_later_ranks_differently`.
- **Proposed fix (`report.py`):** next to each strategy show every benchmark's return over that
  strategy's own period (same start day), and rank by the difference.

### S4. Frozen data looks like a calm strategy (medium)

- **What:** if a source stops (see D6), the gym keeps valuing that asset at its last price. The
  strategy's line goes flat: no losses, no swings, a better drawdown and a distorted Sharpe. The
  scoreboard never says how old each asset's newest bar is, nor how many days a strategy made no
  decision (missed or failed runs: GitHub's cron is best-effort and a rejected push loses the day).
- **Evidence:** `tests/test_audit_stats.py::test_the_scoreboard_says_how_fresh_each_assets_data_is`.
- **Proposed fix (`report.py`):** a "data through" line per asset with a loud warning when one
  is older than its last expected session, and a count of days without a decision.

### S5. The Sharpe formula assumes one equity point per calendar day (low today, a trap later)

- **What:** `score()` multiplies by sqrt(365) whatever the spacing of the points. The live record
  has a point every day because crypto has a bar every day; that case is correct, and it matches
  the usual 252-trading-day Sharpe for ETF-only strategies (checked: 1.26 vs 1.24 over 4 years).
  But any history without a daily crypto bar (an ETF-only backtest, a crypto data gap) gets fewer
  points and a Sharpe overstated by up to 20%.
- **Evidence:** `tests/test_audit_stats.py::test_sharpe_does_not_depend_on_how_many_calendar_days_have_a_point`
  (fails, 2.23 vs 1.89), `...::test_sharpe_with_365_days_matches_the_trading_day_convention_for_etfs`
  (passes).
- **Proposed fix (small, `report.py`):** annualise by the real time span:
  `sqrt(returns / years between first and last point)`.

### S6. The newest row of the scoreboard is provisional (low)

- **What:** at 22:30 UTC today's crypto bar is still open, so today's equity mixes today's ETF
  close with crypto at yesterday's close. The same date shows another number the next day.
- **Evidence:** `tests/test_audit_stats.py::test_todays_equity_is_provisional_and_changes_tomorrow`.
- **Proposed fix:** label the last row "provisional", or score only fully marked days.

### G1. NaN weights are accepted (medium, likely to bite M1's volatility maths) - FIXED in this branch

- **What:** `validate` checks `w < 0` and `sum > 1`; NaN passes both. The gym then neither buys
  nor sells that asset (every comparison with NaN is false), so the portfolio silently keeps what
  it had, and the ledger line contains `NaN`. A division by a zero volatility is all it takes.
- **Evidence:** `tests/test_audit_gym.py::test_non_finite_weights_are_rejected`.
- **Fix (done, `gym.py`):** `validate` rejects NaN and infinite weights. Note for M1: one
  strategy raising in the runner still stops the strategies after it for that day (`run_daily.py`
  has no per-strategy error handling); worth a try/except there that records the failure.

### G2. An order that cannot be paid for at its open is dropped (low, biased against the strategy)

- **What:** each asset's order executes at that asset's next open and is then forgotten. Moving
  from an ETF to crypto, BTC opens at 00:00 UTC, before the ETF can be sold at 13:30: the buy finds
  no cash and is dropped. The money sits in cash until a later decision repeats the order, a full
  day later in the live setup. The other direction (crypto to ETF) works at once.
- **Evidence:** `tests/test_audit_gym.py::test_a_switch_from_etf_to_crypto_ends_up_in_crypto`.
- **Proposed fix (medium, changes gym behaviour, so proposed only):** keep an unfilled buy
  pending until cash arrives. It makes rotation strategies look slightly worse than they would
  be, never better, so it is not urgent.

### G3. Crypto fee is set at the maker level (medium, not verified tonight)

- **What:** the gym charges 25 basis points plus 5 of slippage for crypto. A fill at the open is
  a market (taker) order. Kraken Pro's lowest tier was 0.25% maker / 0.40% taker when last I knew
  it; I could not confirm today's schedule (the fee page is script-rendered and the public API
  returns empty fee lists). If that still holds, each crypto trade is undercharged by 15 basis
  points: nothing for buy-and-hold, about 15% a year for a strategy that turns its book over 100
  times a year (crypto mean reversion).
- **Evidence:** `gym.COSTS`; no test (the fact is unverified).
- **Proposed fix:** the owner or M1 checks the venue's taker fee for a 10,000 USD account and
  sets it; when unsure, use the higher number.

### G4. Dividends are not credited (medium, known, now sized)

- **What:** a settled decision (raw prices, dividends "not credited yet") that DECISIONS.md calls
  "a little". Sized: TLT pays roughly 4% a year, SPY about 1.1%, QQQ about 0.5%. The 60/40
  benchmark is understated by about 2.3% a year, buy-and-hold SPY by 1.1%, equal weight by about
  1%; crypto by nothing. Cash earning 0% and the zero risk-free rate in Sharpe lean the same way.
  The yardsticks a strategy must beat are therefore set too low, most of all for strategies that
  hold crypto or cash while the benchmark holds bonds.
- **Evidence:** `tests/test_audit_gym.py::test_dividends_are_not_credited_which_costs_a_bond_fund_holder_about_4_percent_a_year`.
- **Proposed fix:** credit dividends as cash on the ex-date from Yahoo's `events=div` (it is in
  the BACKLOG). Until then say so under the scoreboard.

### T1. A decision can be filled before it could have been pushed (low)

- **What:** the timing rules themselves held up (see "Checked and sound"). One gap: a fill only
  has to be after the decision's own timestamp. A run that starts at 23:59:30 UTC is filled at the
  00:00:00 crypto open, but its commit reaches GitHub after that price exists. No information
  leaks (inputs are still cut off at the timestamp), but the promise "committed before the outcome
  exists" is no longer provable for that decision, and with the fix for L1 it would leave a
  30-minute window for a forger.
- **Evidence:** `tests/test_audit_timing.py::test_a_decision_is_not_filled_before_it_could_have_been_pushed`.
  GitHub's scheduled runs are often late; 22:30 leaves 90 minutes before 00:00.
- **Proposed fix (small, `gym.py`):** fill at the first open at least 30 minutes after the
  decision (the same 30 minutes L1 allows between decision and commit).

## Checked and sound

- **ETF session times.** Assumed open 13:30 UTC is never after the real open and assumed close
  21:00 UTC never before the real close, for every weekday of 2026-2028 in both daylight-saving
  cases; a bar's UTC date equals its New York date
  (`tests/test_audit_timing.py::test_assumed_etf_session_contains_the_real_one_all_year`).
- **Visibility and fills.** For 670 random and boundary decision times around both clock changes,
  a decision sees exactly the bars closed at or before it and fills at exactly the first open
  after it (`...::test_random_decision_times_never_see_or_fill_at_the_wrong_bar`). Weekends and
  holidays are just missing bars; orders wait.
- **Unfinished bars.** A bar is never stored before its close plus 15 minutes, for any clock
  time (`...::test_a_bar_still_in_progress_is_never_final`). Kraken's and Coinbase's days are UTC
  days; Yahoo's and Stooq's dates are exchange dates, equal to UTC dates for US sessions.
- **The gym's arithmetic.** Random trading at constant prices never creates money, cash never
  goes negative, positions never go short, fees and slippage are both charged; buy-and-hold earns
  exactly first-fill-open to last close (`tests/test_audit_gym.py`).
- **The real record so far.** `paper-trail` at `0d3bc31`: 700 consecutive crypto days, four ETFs
  on one identical calendar of 481 sessions, no bad or duplicate rows, no crypto open more than
  0.2% from the previous close. GitHub's activity log shows one event on the branch: its creation
  by `github-actions[bot]` at 2026-11-11 22:00:52 UTC, 3 seconds after the decisions' timestamp.

## Status

- **Done:** all areas audited; L1-L8, D1-D6, S1-S6, G1-G4, T1 written up with tests.
- **Doing:** small fixes, one commit each.
- **Next:** owner summary on top and final ranking; re-probe Yahoo for the final 2026-11-11 bars (D1).
