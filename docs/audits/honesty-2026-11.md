# Honesty audit 1 (2026-11-12)

Auditor: lane C agent, branch `audit-1` (PR #5). Scope: every way this system could show a
result that is not true. Code audited: `main` at `8e26333` (M0), then at `552e521` after M1 was
merged during the audit (merged into this branch). Record audited, read-only: `paper-trail` at
`e7c43e0` (three runs: 2026-11-11 22:00 UTC, 2026-11-12 01:51 and 03:12 UTC).

## Summary for the owner

I tried to make the scoreboard lie.

**What held.** No strategy can see a price before the market has printed it: summer or winter
time, weekends and holidays included. The record so far (three runs) is clean.

**What did not.** The logbook could be made to lie in four ways: add a "decision" afterwards
with an old date, rewrite old lines behind a merge, edit a stored price, or replace the whole
record branch. The first three are closed in this branch. The fourth is now detected, but only
a setting of yours can prevent it. Two independent reviewers then found a way around one of my
own fixes (closed since). These checks are new and deserve another attack before they are
trusted.

**What the numbers can and cannot say.**

- Six months will not tell skill from luck. Nine strategies with no skill at all, run for six
  months: the best one looks like a star more often than not. The "deflated Sharpe" column
  corrects for that, and it is strict: a world-class strategy has an even chance of reading
  "95% sure" after about five years, a good one after about twenty. Six months can rule out
  disasters. It cannot prove skill.
- The yardsticks are set a little low: dividends are not counted (about 4% a year for the bond
  fund, 2.3% for 60/40, nothing for Bitcoin).
- Prices are stored an hour after the US close, before Yahoo's numbers are final. Stored
  prices are never changed; every later difference is now logged and counted on the scoreboard.
- The backup source for the four funds is dead. If Yahoo stops answering, their prices freeze;
  the scoreboard and the weekly page now say so in bold.

**What I need from you.**

1. A rule for the `paper-trail` branch: block force pushes and deletion (GitHub, Settings,
   Rules; two minutes; agents cannot do it).
2. A decision on what "graduation" means, given the first point above (finding S2).

## All findings at a glance

Severity: **high** = the scoreboard can show a result that never happened, or will be read wrongly,
and nothing warns; **medium** = numbers are biased or a safeguard is weaker than the docs say;
**low** = small or unlikely. Ranked by how much each could mislead, open ones first.

| # | Finding | Severity | State |
|---|---|---|---|
| S2 | Six months cannot separate skill from luck; the corrected number says "no" for years | high | open: owner decision |
| D1 | Bars are stored before the source is final; later corrections were never seen | high | differences now logged; cause open |
| L3 | The record branch can be replaced (force-push, delete) | high | detected; owner action open |
| G4 | Dividends not credited, cash earns nothing: yardsticks understated | medium | open: known, now sized |
| D6 | The ETF fallback source does not work | medium | open: owner decision |
| L7 | A decision did not say which code made it | medium | half fixed |
| G2 | An order that cannot be paid for at its open is dropped | low | open: proposed |
| S6 | The newest row of the scoreboard is provisional | low | open |
| L6 | Outside a git checkout the ledger check checks nothing | low | open |
| G5 | Small gym and table quirks (turnover, one-sided band, tiny weights) | low | open |
| L1 | A decision written after the outcome was accepted | high | fixed |
| L2 | History could be rewritten with an ordinary push | high | fixed |
| L4 | Stored bars could be edited unnoticed | high | fixed |
| S1 | A Sharpe ratio was printed from day two | high | fixed |
| D2 | A stock split would be booked as a crash | high, unlikely | guarded |
| G3 | Crypto trades were charged 0.25%; the real fee is 0.38% to 0.80% | medium | fixed (flat 0.60%) |
| D3 | No sanity check before a bar became permanent | medium | fixed |
| D4 | A hole in a source's answer became a permanent gap | medium | fixed |
| L5 | A failed fetch started a brand-new record | medium | fixed |
| L8 | The daily job could be started from any branch | medium | fixed |
| G1 | NaN weights were accepted | medium | fixed (also on main) |
| S7 | A fill on a strategy's first day was left out of Sharpe and drawdown | medium | fixed |
| S8 | The weekly page let a late starter "beat" a yardstick it merely copied | medium | fixed |
| S3 | Returns over different periods were ranked in one table | medium | fixed |
| S4 | Frozen data, or days without a decision, looked like a calm strategy | medium | fixed |
| D7 | An empty answer from a source counted as "no news" | medium | fixed |
| D8 | A day a source left out became a silent, permanent hole | medium | fixed (crypto), reported (ETFs) |
| D9 | A run's problems left no trace in the record | medium | fixed |
| S5 | Sharpe assumed a point every calendar day | low | fixed |
| L9 | A lost final newline glued record lines together for good | low | fixed |
| T1 | A decision could be filled before it could have been pushed | low | fixed |
| D5 | The record did not say where a bar came from | low | fixed |

Tests: `tests/test_audit_*.py`. A finding that is still open and has a crisp expected behaviour
is an `xfail(strict=True)` test (1 left: G2); findings about size or judgement are
ordinary tests that pin the numbers quoted here.

## Open findings

### S2. Six months cannot separate skill from luck (high)

- **What, part 1: the raw numbers flatter.** The uncertainty of a yearly Sharpe ratio measured
  from daily returns is about sqrt(365 / days): +-3.7 at 30 days, +-1.4 at 180 days, +-1.0 at one
  year, +-0.7 at two (one standard error; double it for a 95% band). Nine strategies with zero
  skill, run for 180 days: the best one shows a Sharpe of about 2.1 on average and above 2 in more
  than half of all cases. Returns are as noisy: over 180 days an asset like BTC with no drift at
  all ends anywhere between -48% and +94% (5th to 95th percentile), one like SPY between -17% and
  +21%. "Beat buy-and-hold BTC by 10% in six months" is well inside luck. The scoreboard still
  sorts by raw return.
- **What, part 2: the corrected number will say "no" for years.** M1 added the deflated Sharpe
  (the right tool) and counts every strategy "tried", which includes every backtest variant the
  research lane logs: 136, then 176, 219 and 256 in the first hours of 2026-11-12, and growing
  nightly. With 256 tries a strategy must show a Sharpe of 6.4 after six months, 4.5 after one
  year, 2.6 after three, 2.0 after five and 1.4 after ten before the column reads 95%. A strategy whose
  true Sharpe is 1.0 (very good) reads 95% after three years in fewer than 1 case in 100, after
  ten years in 1 in 10, and has an even chance only after about twenty. A world-class one (true
  Sharpe 2) has an even chance after five years. Even counting only the 9 live strategies the
  bar is 4.5 at six months and 1.8 at three years.
- **What, part 3: the 95% is about the wrong question.** The deflated Sharpe asks "is this
  better than doing nothing?", not "is it better than the yardstick?". In a long rally
  buy-and-hold itself would pass. `weekly.md` guards against that by also requiring the strategy
  to be ahead of every yardstick, but that part is a plain comparison of two noisy returns.
- **Evidence:** `tests/test_audit_stats.py::test_nine_strategies_with_no_skill_after_six_months_the_best_looks_skilled`,
  `...::test_the_deflated_sharpe_bar_is_out_of_reach_for_years` (both seeded, numbers as quoted).
- **Why it matters:** not a bug. Over-counting tries is the cautious direction (DECISIONS,
  2026-11-12) and stays. But DESIGN.md's graduation bar, "at least 6 months ... deflated Sharpe
  significant", cannot be met by any realistic strategy, and the owner will read "no sign of
  skill yet" about everything for years without knowing that this is what an honest board says.
- **Proposed:** (1) the owner decides what graduation means; an honest wording is "six months
  shows a strategy is not broken; proof of skill takes years". (2) Print the bar: "Sharpe needed
  for 95% today: x", next to each row. (3) Apply the deflated test to the return in excess of
  the best yardstick. (4) Consider counting, for the forward record, only strategies that
  entered the forward test: a strategy promoted from 200 backtests is one new forward try, and
  the forward record is exactly what protects against the other 199.

### D1. Bars are stored before the source is final (high; differences are now logged, the cause remains)

- **What:** an ETF bar is stored once it is 15 minutes past 21:00 UTC and was never looked at
  again: the next run asked the source only for newer days. If the source's numbers for that day
  were not final yet, the record keeps the early ones for ever, and nobody was told they differ.
  Every fill and every mark on that day uses them.
- **Evidence (real):** the first run stored the 2026-11-11 ETF bars at 22:00:49 UTC, one hour
  after the close. In all four ETF files that row is the only one of 481 whose volume is not a
  multiple of 100 (SPY 37,707,134), the mark of a row Yahoo had not finalised. Five hours after
  the close (02:00 UTC) Yahoo's chart API showed other numbers for the same day: QQQ open
  687.275 (stored: 687.280), QQQ volume 42,821,615 (stored 42,505,260), TLT volume 26,433,481
  (stored 26,421,050), and `close: null` for all four ETFs, i.e. the row was still being
  rewritten. The price difference is tiny this time (0.07 basis points on an open, the price
  fills use); the point is that the record already differed from its source after one day.
- **Fix (done, `data.py`, `run_daily.py`, 10 lines in `report.py`):** each run asks every
  symbol's first-choice source again for the last 5 stored days and compares prices (not volume,
  which changes daily). Stored rows are never changed; each difference is appended once to
  `data/revisions.jsonl`, the scoreboard shows how many bars differ and by how much at most, and
  a difference of 1 basis point or more is reported as a problem of that run. The second request
  is best effort: if it fails, nothing is logged that day. Tried live against a scratch copy of
  the real bars: runs clean (Yahoo's 2026-11-11 rows still had no close, so there was nothing to
  compare yet). Test: `tests/test_audit_data.py::test_a_revised_bar_is_reported`.
- **What is left:** the record still keeps the early numbers; the log makes that visible, it
  does not make them right. Whether to store ETF bars a day later (once final) is a design
  decision with a cost: every strategy would decide on day-old ETF prices. Moving the cron later
  is not obviously safer: Yahoo's row was complete at 22:00 and had lost its close again by 01:38.

### L3. The record branch can be replaced, and the repo itself cannot tell (high; detected, owner action open)

- **What:** if `paper-trail` is force-pushed, or deleted and recreated, the new history is
  self-consistent; no check that only reads the branch can know an older one existed. Nothing
  prevents it today: the only ruleset (`protect-main`) covers the default branch, and GrimsBot,
  which all agents act as, has push rights.
- **Evidence:** `tests/test_audit_ledger.py::test_a_force_pushed_history_passes_the_check`;
  `gh api repos/GrimsVerk/GrimsTrade/rulesets` lists only `protect-main` with
  `include: ["~DEFAULT_BRANCH"]`.
- **Guard (done, workflow):** before running, `scripts/check-trail-activity.sh` asks GitHub's
  activity log, which no pusher can edit, and refuses to run if `paper-trail` was ever
  force-pushed, deleted or created twice, or if any commit reached GitHub more than 10 minutes
  after the time it claims (a back-dated commit, see L1). Tried against the real repository: it
  passes; both real pushes arrived 1 second after their commits. If GitHub cannot be asked, the
  job goes on with a warning. After looking at a reported event a person sets the repository
  variable `TRAIL_REVIEWED_UNTIL` to move on. Agents can set that variable too (GrimsBot has
  write access), so it is deliberately not a silent switch: an accepted event is written into the
  trail and printed on the scoreboard on every run, a date in the future is refused, and each
  new event stops the job again. Tests: `tests/test_audit_workflow.py` (fake `gh`).
- **Not proven live:** the script ran with GrimsBot's token, not yet with the job's own token
  inside Actions. If that token may not read the activity log, the step prints a warning and
  checks nothing; look at the first run's log after merging.
- **Owner action (needs admin):** add a ruleset for `paper-trail` that blocks force pushes and
  deletion, with no bypass. The guard detects; only the ruleset prevents.

### G4. Dividends are not credited and cash earns nothing (medium, known, now sized)

- **What:** a settled decision (raw prices, dividends "not credited yet") that DECISIONS.md
  calls "a little". Sized: TLT pays roughly 4% a year, SPY about 1.1%, QQQ about 0.5%. The 60/40
  yardstick is understated by about 2.3% a year, buy-and-hold SPY by 1.1%, equal weight by about
  1%, crypto by nothing. Cash earning 0% and the zero risk-free rate in the Sharpe ratio lean the
  same way. The yardsticks are therefore easier to beat than they should be, most of all for a
  strategy that holds crypto or cash while the yardstick holds bonds.
- **Evidence:** `tests/test_audit_gym.py::test_dividends_are_not_credited_which_costs_a_bond_fund_holder_about_4_percent_a_year`.
- **Proposed fix:** credit dividends as cash on the ex-date from Yahoo's `events=div` (in the
  BACKLOG). `weekly.md` already says "dividends not yet credited"; add the size.

### D6. The ETF fallback source does not work (medium, for "runs without anyone")

- **What:** on 2026-11-12 `https://stooq.com/q/d/l/?s=spy.us&i=d` answered HTTP 200 with a
  JavaScript "verify your browser" page instead of CSV. The code treats that as a failed source
  (good, and pinned by a test), so the ETFs have one working source. If Yahoo blocks GitHub's
  runners, ETF prices stop.
- **Evidence:** live probe; `tests/test_audit_data.py::test_stooq_browser_check_page_is_an_error_not_data`.
- **Proposed fix:** a second real ETF source. Alpaca's free data is in the BACKLOG; it needs a
  key stored as an Actions secret, which is the owner's call.

### L7. A decision did not say which code made it (medium, half fixed)

- **What:** strategy names key the ledger, but a strategy's code or parameters can change under
  the same name. The scoreboard then shows one unbroken track record, and `tries.jsonl` counts
  one try, for what were really two strategies. The daily job runs whatever is on `main`.
- **Fix (done, `ledger.py`):** each new decision line carries `code`, the commit the daily job
  ran (`GITHUB_SHA`); a local run has no such field
  (`tests/test_audit_ledger.py::test_a_decision_records_the_code_version`).
- **Still open:** nothing reads it yet. The scoreboard should flag (or start a new row for) a
  strategy whose own file changed between two of its decisions, and count that as a new try.

### Low

- **G2. An order that cannot be paid for at its open is dropped.** Each asset's order executes at
  that asset's next open and is then forgotten. Moving from an ETF to crypto, BTC opens at 00:00
  UTC, before the ETF can be sold at 13:30: the buy finds no cash and is dropped; the money sits
  in cash until a later decision repeats the order, a day later in the live setup. It makes
  rotation strategies look slightly worse, never better. Test:
  `tests/test_audit_gym.py::test_a_switch_from_etf_to_crypto_ends_up_in_crypto` (xfail).
  Proposed (changes gym behaviour, so not done): keep an unfilled buy pending until cash arrives.
- **S6. The newest row of the scoreboard is provisional.** At 22:30 UTC today's crypto bar is
  still open, so today's equity mixes today's ETF close with crypto at yesterday's close; the
  same date shows another number the next day
  (`tests/test_audit_stats.py::test_todays_equity_is_provisional_and_changes_tomorrow`).
  Proposed: label the last row, or score only fully marked days.
- **G5. Small gym and table quirks** (found and reproduced by the independent reviewer; none
  flatters a strategy). Turnover per year annualises the one-off first purchase: a month-old
  buy-and-hold shows 11.8, a year-old one 1.0. With no cash left the 1% band works in one
  direction only: in the real 700-day replay `equal_weight` held ETH 1.1-2.6% of equity under
  target for 19 days in a row, because no other holding was 1% over target and so nothing was
  sold. Target weights under 1% never fill, silently. A duplicate date in a bar file would
  crash the gym (`data.append` prevents it; a hand-edited file would not be caught on load).
- **L6. Outside a git checkout the ledger check checks nothing.** With `--root` on a plain
  folder, or on a `trail/` that is not a worktree, `check_append_only` returns 0 and the runner
  ignores that (`tests/test_audit_ledger.py::test_outside_a_git_checkout_the_check_silently_checks_nothing`).
  A trap for local runs only. Proposed: refuse a non-empty ledger with no committed version.

## Fixed in this branch

One commit per fix, except the three workflow changes, which share the same lines of
`daily.yml`.

### L1. A decision written after the outcome was accepted (high)

- **What:** the ledger check only proves that old lines were not changed, not that a line was
  written when it says it was. Anyone who can push to `paper-trail` could append "on day 1 at
  22:31 I bought BTC" on day 4, after BTC doubled. The gym filled it at the day-2 open and the
  scoreboard showed +99%.
- **Fix (`ledger.py`, 3 lines in `report.py`):** a committed decision counts from its commit
  time when that is later than its own timestamp (`ledger.in_force`). The back-dated line is
  filled at the first open after it was committed, so hindsight buys nothing. Decisions recorded
  more than 30 minutes after their timestamp are "late" and the scoreboard says how many. On the
  real record nothing changes: its decisions were committed 2 and 22 seconds after their
  timestamps. Tests: `tests/test_audit_ledger.py::test_a_backdated_decision_is_not_credited` and
  three more beside it.
- **A hole in the first version of this fix,** found by the independent reviewer and closed:
  line positions were counted in text characters, commit sizes in bytes. Padding the ledger with
  blank Windows-style lines (two bytes, one character) moved a later line's position back into
  an older commit, so a back-dated decision counted as on time again. Positions are now counted
  in bytes and each row is parsed from the same bytes that date it
  (`...::test_padding_with_blank_lines_does_not_move_a_backdated_decision`). The lesson stands
  beyond this bug: this check is new, security-like code and deserves another adversarial pass.
- **What is left:** commit dates are written by whoever commits. The L3 guard closes most of
  that from outside: a commit that reaches GitHub more than 10 minutes after its claimed time
  stops the job. A forger is left with a 10-minute window, and with the L3 owner action undone
  could still replace the branch (which the guard then reports).

### L2. History could be rewritten with an ordinary push (high)

- **What:** `check_append_only` read `git log -- <file>`, which skips one side of a merge when
  the merge keeps the other side's version of the file. A forger builds a parallel history with
  a changed ledger, merges the honest branch into it keeping the forged file, and pushes. The
  result descends from the honest head, so it is a normal push: no force needed, and a "block
  force pushes" rule would not stop it.
- **Fix (`ledger.py`):** the check walks every commit and compares the file with its version in
  each parent. A ledger deleted from the working tree is refused too. Test:
  `tests/test_audit_ledger.py::test_a_rewrite_hidden_behind_a_merge_is_caught`.

### L4. Stored bars could be edited and nothing noticed (high)

- **What:** the scoreboard is recomputed from `data/bars/*.csv` on every run, so the bars are as
  much the record as the decisions, but only the ledger files were checked. One edited cell (the
  open a strategy bought at) turned a small loss into +99%.
- **Fix (`run_daily.py`, 2 lines):** the run applies the append-only check to every bar file.
  Test: `tests/test_audit_ledger.py::test_a_rewritten_bar_is_caught`.

### S1. A Sharpe ratio was printed from day two (high, because it is the number people read)

- **What:** four up-days read as "Sharpe 30"; a strategy that only paid 2 basis points of
  slippage once showed -4.6.
- **Fix (`report.py`):** no Sharpe under 30 days (the threshold the deflated Sharpe already
  had); after that it is printed with its standard error, e.g. `0.80 ±1.4`, and the footnote
  says what the ± means. Test: `tests/test_audit_stats.py::test_a_record_of_a_few_days_shows_no_sharpe_number`.

### D2. A stock split would be booked as a crash (high impact, unlikely for today's four ETFs)

- **What:** Yahoo adjusts its whole history backwards after a split. New rows arrive in
  post-split prices; stored rows and the units a strategy holds are pre-split. The gym would show
  -50% overnight for a 2-for-1 split, for ever.
- **Guard (`data.py`):** `append` stores the bars before it and then refuses a bar that opens
  more than 40% (`MAX_GAP`) from the previous close; the run reports it every day until a person
  decides. The whole real history passes (largest gap in two years: 6.0%, GLD). Test:
  `tests/test_audit_data.py::test_a_split_is_not_stored_as_a_crash`.
- **What is left:** a split is stopped, not handled. Handling it means fetching split events
  and adjusting held units.

### G3. Crypto trades were charged less than any real fee (medium)

- **What:** the gym charged 25 basis points per crypto trade, plus 5 of slippage. A fill at the
  open is a market order and pays the taker fee. Kraken Pro's fee page on 2026-11-12 (read twice,
  as served outside the US) lists taker 0.80% for an account that traded under 2,500 USD in the
  last 30 days, 0.60% from 2,500, 0.38% from 10,000, 0.35% from 25,000 and 0.30% from 50,000.
  25 was below every one of them.
- **Size:** the busiest live crypto strategy, `crypto_mean_reversion`, turned its book over 10.6
  times a year in the backtest: about 9,000 USD a month, the 0.60% tier. Undercharged by 35
  basis points a trade, that is about 3.7% a year, against a backtest return of about 5% a year.
  Buy-and-hold BTC: 0.55% once.
- **Fix (`gym.py`, one line, own commit; DECISIONS):** the crypto fee is 0.60%. The record has
  no scored fills yet, so no number shown so far changes; crypto backtests get a little worse,
  and the research lane's logged Sharpes were computed with the old fee.
  `tests/test_audit_gym.py::test_a_crypto_fill_pays_the_taker_fee`.
- **What is left:** it is one flat number. A slow account really pays 0.80% (0.2% too little
  charged on each of its few trades), a fast one 0.38% or less (too much charged). Fees by volume
  tier are in the BACKLOG. I could not read the US schedule (a search result says 0.40% taker at
  the lowest tier there). If the owner would trade elsewhere, that venue's fee belongs here.
  And the cost table is not part of the record: every score is recomputed with today's costs, so
  a later change alters all past results without a trace; DECISIONS now asks for an entry each
  time.

### D3, D4. Nonsense bars and holes were stored for ever (medium)

- **What:** nothing checked a bar before it became permanent. A zero open makes the gym divide
  by zero, so every later run would crash, and the row could not be removed. And when Yahoo
  listed a day without prices followed by priced days, the later days were stored and the hole
  could never be filled.
- **Fix (`sources.py`):** `fetch` runs `check_sane` on every bar (finite, positive, high and low
  consistent with open and close, 0.1% slack); `yahoo()` raises on an empty day that has priced
  days after it. Either counts as a failed source: the next one is tried and the run reports
  it. All 3,326 real stored bars pass. Assumption: Yahoo lists no row at all for market holidays
  (true for all 481 stored sessions). Tests: `tests/test_audit_data.py`.
- **What is left:** a day the source omits completely is still invisible. A calendar check
  across the four ETFs (they share one) and "crypto has every day" would catch it.

### D7, D8, D9. Data that stops or has holes, and nobody is told (medium; found by the independent reviewer)

- **D7. An empty answer counted as "no news".** A source replying with an empty list (Kraken
  with no rows, Yahoo with no timestamps) was a success: the second source was never asked, no
  problem was reported, nothing changed, nothing was committed. Frozen data behind green runs.
  **Fix (`sources.py`, `run_daily.py`):** when a source has nothing new the next one is asked
  too, and a symbol whose newest bar is older than it can honestly be (36 hours for crypto, two
  missed weekday sessions for ETFs) is a problem of the run.
  `tests/test_audit_data.py::test_an_empty_answer_is_not_taken_as_no_news`.
- **D8. A day the source left out.** D4 covered a day Yahoo lists without prices; a day simply
  absent from the answer was still stored around, and can never be added. **Fix (`data.py`,
  `run_daily.py`):** crypto trades every day, so an answer that skips a day is refused (the bars
  before the gap are kept). ETFs have holidays, so there a session one ETF lacks while the others
  have it is reported as a problem. The real history has neither.
  `tests/test_audit_data.py::test_a_day_the_source_leaves_out_is_not_skipped`.
- **D9. Problems left no trace in the record.** A failed source or a strategy that raised was
  only in that run's log and exit code; later, "held its position", "crashed" and "had no data"
  looked the same. **Fix (`ledger.py`):** each run's problems are appended to
  `ledger/problems.jsonl`; the scoreboard shows how many runs had problems and the latest ones,
  the weekly page says how many this week.
  `tests/test_audit_data.py::test_a_runs_problems_are_kept_in_the_record`.

### L5, L8. The daily job could start a new record by accident, or run unmerged code (medium)

- **What:** the workflow did `git fetch origin paper-trail || git worktree add --orphan`: a
  deleted branch, or just a network blip, made it build a fresh empty record. And a manual start
  could pick any branch, whose code then wrote into the one official record.
- **Fix (workflow):** `scripts/checkout-trail.sh` asks the remote whether the branch exists; a
  missing branch stops the job unless it was started by hand with "start a new record" ticked,
  an unreachable remote always stops it. The job has `if: github.ref == 'refs/heads/main'`.
  Tests: `tests/test_audit_workflow.py` (throwaway repos).

### S3, S7, S8. Start dates and start-up effects in the scores (medium; S7 and S8 found by the independent reviewer)

- **S7. A fill on the first day was left out.** `score()` used the first equity point as its
  baseline. Normally that is the untouched start cash. But a decision made before the US open
  fills ETFs the same day, and that day's result then vanished from Sharpe, deflated Sharpe and
  max drawdown (a one-day record even showed "Return +0.0%" next to a changed equity). This is
  not hypothetical: the five M1 strategies' first decisions were made by a manual run at 01:51
  UTC on 2026-11-12 and fill at that day's open. **Fix (`report.py`, `gym.py`):** every day's
  return is measured, the first from the start cash, which `Result` now carries.
  `tests/test_audit_stats.py::test_a_fill_on_the_first_day_counts_in_sharpe_and_drawdown`.
- **S3. Returns over different periods were ranked in one table.** Each row's return runs from
  that strategy's own first decision, and the scoreboard is sorted by it: two strategies holding
  exactly the same thing rank apart by start date alone, and the five M1 strategies started a
  day after the four yardsticks. **Fix (`report.py`):** the scoreboard has a "Beats yardsticks"
  column computed as in S8 below, and says under the table that rows are to be compared by it,
  not by Return. `tests/test_audit_stats.py::test_the_scoreboard_has_a_column_that_is_fair_to_late_starters`.
- **S8. A late starter could "beat" a yardstick it merely copied.** `weekly.md` compared each
  strategy with the yardstick's own curve from the end of the strategy's first day. That hands
  one of the two the move between the strategy's decision and its first fills, for good: for an
  exact copy of buy-and-hold SPY the reviewer measured, over 149 real start days, a mean gap of
  0.54% and up to 4.9 points. **Fix (`weekly.py`, `report.restarted`):** the yardstick is
  restarted with fresh cash at the moment the strategy started: same first prices, same costs.
  `tests/test_audit_stats.py::test_an_exact_copy_of_a_yardstick_never_beats_it`.

### S4. Frozen data, or days without a decision, looked like a calm strategy (medium)

- **What:** if a source stops (see D6), the gym keeps valuing that asset at its last price. The
  strategy's line goes flat: no losses, no swings, a better drawdown and a distorted Sharpe. The
  scoreboard never said how old each asset's newest bar is, nor on how many days a strategy made
  no decision (GitHub's cron is best-effort: the first scheduled run started 4 hours 42 minutes
  late; a rejected push loses the day; and a strategy that raises an error is skipped for the
  day and keeps its old position).
- **Fix, part 1 (`report.py`):** the scoreboard has a "Prices through" line with the newest bar
  of each asset and a bold **STALE** mark on any asset more than 2 days (crypto) or 5 days (ETFs)
  behind the newest one (`tests/test_audit_stats.py::test_the_scoreboard_says_how_fresh_each_assets_data_is`).
  `weekly.md`, the page the owner reads, shows the same line as a warning when anything is stale.
- **Fix, part 2 (`report.py`):** the scoreboard counts, per strategy, the days of new prices on
  which it made no decision, whatever the cause. Each decision records which bars it saw, so a
  jump of more than one day between two decisions, or stored days after the last one, were never
  decided on. A run that is only late skips nothing and is not counted. A retired strategy shows
  up here with a growing number, instead of looking alive. On the real record the count is zero
  (`...::test_the_scoreboard_counts_days_a_strategy_never_decided_on`).
- **What is left:** the count is on the scoreboard only, not on the weekly page.

### G1, S5, T1 (medium to low)

- **G1. NaN weights were accepted.** NaN is neither below 0 nor above 1, so it passed; the gym
  then kept the old position and the ledger recorded `NaN`. Fixed here and, independently, on
  `main` by M1 (which also made the runner carry on past a strategy that raises).
  `tests/test_audit_gym.py::test_non_finite_weights_are_rejected`.
- **S5. The Sharpe formula assumed a point every calendar day.** True for the live record
  (crypto has a bar every day; checked: the 365-day Sharpe of an ETF-only strategy then equals
  the usual 252-trading-day one, 1.26 vs 1.24). But a history without a daily crypto bar came out
  20% too high. Sharpe and turnover are now annualised by the real time span.
  `tests/test_audit_stats.py::test_sharpe_does_not_depend_on_how_many_calendar_days_have_a_point`.
- **D5. The record did not say where a bar came from.** When Kraken fails the bar comes from
  Coinbase, another exchange with slightly other prices (2026-11-10 BTC: open 75,253.1 vs
  75,257.8, low 72,584.6 vs 72,643.5, about 8 basis points apart at worst). When Yahoo fails it
  would come from Stooq, whose history is, as far as I know, dividend-adjusted where Yahoo's is
  raw (unverified: Stooq is unreachable). Now every run appends to `data/sources.jsonl` which
  source supplied which days of which symbol. The runs before this fix used Kraken and
  Yahoo (the stored values match those sources' formats and my live probes).
  `tests/test_audit_data.py::test_the_record_says_which_source_each_bar_came_from`.
- **L9. A lost final newline glued lines together for good** (independent reviewer). A ledger or
  bar file whose last line had lost its newline got the next line glued on; every later run
  failed to parse it, and restoring the newline counted as rewriting history. Appends now start
  on a fresh line; an empty bar file still gets its header; a time without a zone is refused
  instead of being read as local time. Not repairable even now: a last line cut off in the
  middle. `tests/test_audit_ledger.py::test_a_lost_final_newline_does_not_glue_lines_together`.
- **T1. A decision could be filled before it could have been pushed.** A run starting at
  23:59:30 UTC was filled at the 00:00:00 crypto open, though its commit lands after that price
  exists. Covered by the L1 fix: it now fills at the next open after its commit.
  `tests/test_audit_ledger.py::test_a_decision_counts_from_its_commit`.

## Checked and sound

- **ETF session times.** Assumed open 13:30 UTC is never after the real open and assumed close
  21:00 UTC never before the real close, for every weekday of 2026-2028 in both daylight-saving
  cases; a bar's UTC date equals its New York date
  (`tests/test_audit_timing.py::test_assumed_etf_session_contains_the_real_one_all_year`).
- **Visibility and fills.** For 670 random and boundary decision times around both clock changes,
  a decision sees exactly the bars closed at or before it and fills at exactly the first open
  after it (`...::test_random_decision_times_never_see_or_fill_at_the_wrong_bar`). Weekends and
  holidays are just missing bars; orders wait.
- **Unfinished bars.** A bar is never stored before its close plus 15 minutes, at any clock time
  (`...::test_a_bar_still_in_progress_is_never_final`). Kraken's and Coinbase's days are UTC
  days; Yahoo's dates are exchange dates, equal to UTC dates for US sessions. (What "final"
  means an hour after the close is D1.)
- **The gym's arithmetic.** Random trading at constant prices never creates money, cash never
  goes negative, positions never go short, fees and slippage are both charged; buy-and-hold earns
  exactly first-fill-open to last close (`tests/test_audit_gym.py`).
- **The real record so far** (checked again after the third run). 701 consecutive crypto days,
  four ETFs on one identical calendar of 481 sessions, no bad or duplicate rows, no crypto open
  more than 0.2% from the previous close. All nine files pass the new append-only check. All 13
  decisions count from their commit, 2 and 22 seconds after they were made; none is late.
  GitHub's activity log shows three events on `paper-trail`, all by `github-actions[bot]`: its
  creation at 2026-11-11 22:00:52 UTC and pushes at 2026-11-12 01:51:50 and 03:12:50 UTC, each
  at most one second after its commit. The third run wrote no decisions, rightly: no bar had
  closed since the second.
- **A late run cannot cheat.** GitHub started the first scheduled run (due 22:30 UTC) at 03:12
  UTC, 4 hours 42 minutes late. A late decision sees more closed bars and fills at later opens,
  never earlier ones; the cost is a crypto fill almost a day after the signal. Late or skipped
  runs are still not counted anywhere (S4).
- **Independent review.** Two reviewers (subagents with no sight of my conclusions beyond a list
  of titles) attacked the gym and scoring, and the ledger, runner and sources. Their new
  findings are S7, S8, G5, D7, D8, D9, L9 and the hole in L1. What they checked and found sound:
  fill timing and equal-timestamp ordering over 400 fuzzed runs; daily equity re-derived
  independently from fills and bars for all nine strategies over 699 real days (largest error
  0.000000 USD); the deflated Sharpe under a zero-skill null (reads 95% or more in at most 0.8%
  of worlds); the rule that skips a decision when no data is new; re-runs the same evening and
  across midnight; `append` with unordered, duplicate and older bars; each source's parsing.
- **The M1 strategies** use no clock, no randomness and no files: they see only the bars the
  runner hands them. I did not review their trading logic (the M1 lane had its own review).

## Status

- **Done:** all five areas of the brief audited (look-ahead, data, gym, ledger and workflow,
  statistics) against M0 and again after the M1 merge, then attacked once more by two independent
  reviewers. 32 findings: 20 fixed or guarded, 4 half done (D1, L3, L7, S4), 8 open (S2, G4, G3,
  D6 need a decision or outside facts; G2, S6, L6, G5 are low). All with tests except G3
  and G5. Checks green.
- **Doing (session 3, from 06:35 UTC, hard stop 08:40 UTC):** the second adversarial pass over
  `ledger.in_force`, `check_append_only` and the two trail scripts (two independent reviewers);
  re-checking the record after its third run (`paper-trail` at `e7c43e0`); then final summary
  and ranking, and PR #5 marked ready for review.
- **Not proven live:** the workflow changes. The first run after merging is the test: its log
  must show "GitHub's activity log agrees with the paper-trail history".
- **Changed for whoever starts a brand-new record:** the first run must be started by hand with
  "start a new record" ticked. The existing record is not affected.
- **Next, in order of value:** a second adversarial pass over `ledger.in_force` and
  `scripts/check-trail-activity.sh` (new code that guards the record); the second halves of L7
  and S4; G2.
- **To resume:** read this section, run the checks in `AGENTS.md`, look at the remaining `xfail`
  test (`uv run pytest -rx tests/`).
