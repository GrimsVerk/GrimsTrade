# Integration preview 1 (branch `integrate-1`, draft PR #115)

Landed as one merge (2026-11-24, GrimsTrade lead; owner rule "agents merge"). It merges the
open engineering PRs into one tree, one merge commit each (`git merge --no-ff`), in the order
below, with every conflict resolved and the full checks green. Merging this branch into `main`
lands PRs #13, #27, #29, #30, #32, #61, #67, #14 and #15 at once (GitHub marks each merged: its
head is in `main`); rebasing each one separately would have replayed the same resolutions nine
times. `git show <merge commit>` shows each resolved hunk.

Base: `main` at `9b1c45e`, then current `main` (`df9bf01`) merged in (row 10). Checks after every
step: `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy`, `uv run pytest` (the
CI set, see `AGENTS.md`).

## Baseline

`main` 9b1c45e: ruff and format clean, mypy clean (36 files), pytest 211 passed, 1 xfailed (the
xfail is audit G2, which #29 fixes).

## Merge order

| # | PR | Branch (head merged) | Merge commit | Conflicts | Checks after |
|---|----|----------------------|--------------|-----------|--------------|
| 1 | #13 data-search-1 | `f06230f` | `9bee95a` | none | 211 passed, 1 xfailed |
| 2 | #27 health-1 | `3add5e8` | `dccd2cd` | none | 212 passed, 1 xfailed |
| 3 | #29 g2-pending-buy | `98516ff` | `e093d3b` | next-steps | 218 passed |
| 4 | #30 g4-dividends | `d1623cf` | `da7b8f6` | next-steps, DECISIONS, DESIGN | 228 passed (+1 new: 229) |
| 5 | #32 fee-tiers | `cdad73a` | `4ccf883` | **gym.py**, next-steps, DECISIONS, DESIGN, BACKLOG; 1 test | 230 passed (+1 new: 231) |
| 6 | #61 cash-interest | `219da2b` | `b35f2ad` | **gym.py, report.py, run_daily.py**, test_run_daily, next-steps, DECISIONS, DESIGN; weekly text + 1 test | 255 passed (+2 new: 257) |
| 7 | #67 forward-1 | `59eb2d7` | `83be626` | next-steps, DECISIONS | 275 passed |
| 8 | #14 ingest-1 | `28e36b5` | `fb30505` | next-steps | 281 passed |
| 9 | #15 ingest-2 | `268412a` | `8ee5735` | run_daily.py imports, next-steps, DECISIONS | 290 passed |
| 10 | `main` (#127, #128: BACKLOG without the channel list, `local.toml.example`) | `df9bf01` | `3e80558` | `.gitignore` (both entries kept) | 290 passed |

Every pushed step was green: ruff, format and mypy clean, no failing test. Final: **290 passed**.

Why this order:

- #13 first: docs only, and #14 is stacked on it (it contains #13's commits).
- #27 early: one dictionary in `weekly.py`, no overlap with the gym.
- The four gym PRs (#29, #30, #32, #61) in PR-number order. #61 goes last of them on purpose: it
  conflicts with #29, #30 (code) and with #15, and it is the one with open questions, so it
  can wait without blocking the others. #30 lands cleanly on #29 (`gym.py` auto-merges); #32
  needs one real resolution against #29.
- #67 is research only (new module, not imported by the runner): it lands anywhere.
- #14 then #15: #15 is stacked on #14 and conflicts with #61 on `run_daily.py`, so it comes after.

Pairwise check (`git merge-tree` on every pair, before merging): every PR conflicts with every
other on `next-steps.md`; the code conflicts are only #29 x #32 (`gym.py`), #29 x #61 (`gym.py`),
#30 x #61 (`gym.py`, `report.py`, `run_daily.py`, `tests/test_run_daily.py`) and #61 x #15
(`run_daily.py`).

## Conflicts and how each was resolved

22 conflicted files over 7 merges (#13 and #27 merged cleanly), plus two semantic
conflicts that git did not flag (a test and the weekly wording). Most are documentation where
both sides add an independent entry; the code ones were mechanical (keep both parameters) except
3 that needed a real decision about behaviour (marked **decision**).

Documentation (both kept):

- `next-steps.md` (every merge from #29 on): both PRs' sections kept, in merge order. When the PRs
  land, each one's own section is deleted as its follow-ups get done, per `AGENTS.md`.
- `docs/DECISIONS.md` (#30, #32, #61, #67, #15): every entry kept, newest first.
- `docs/DESIGN.md`, "Costs" paragraph (#30, #32, #61): one paragraph with every rule: the
  tiered crypto fee (#32), the waiting buy (#29), dividends (#30) and cash interest (#61).
- `docs/BACKLOG.md` (#32): #30 deletes "credit dividends" and #32 deletes "crypto fee by volume
  tier" (each one is done); both lines are gone.

Code:

1. **decision** `gym._execute`, #32 onto #29. #29 makes trades 4-tuples (`target` for the waiting
   buy) and sizes a buy with `wanted = ... (1 + c.fee)`; #32 adds a per-asset-class fee rate from
   the 30-day volume and unpacks 3-tuples. Resolved: 4-tuples throughout, and the waiting buy
   is sized with the tier rate (`fee_rate`), not the flat `Costs.fee`, so "is this buy fully
   paid?" and the actual fee agree. New test:
   `test_a_buy_waiting_for_cash_pays_the_fee_tier_of_the_open_it_fills_at`.
2. **decision** test tolerance, #32 onto #29. `test_a_fully_invested_equal_weight_tops_up_crypto_that_fell_behind[late-cron-03:00-costs]`
   failed: with tiered fees the crypto ends 0.9% under target, and the test asked for 0.5%.
   That is the rule working as written: G2 tops up while an asset is outside the 1% band and
   then stops, and 0.9% is inside the band. On #32 alone (no G2) the same case ends 1.6% under,
   outside the band. The tolerance is now `gym.BAND` (1%), which still fails without G2. An
   owner who wants top-ups to the exact target would need a narrower band or a band rule for
   funded buys: a new decision, not part of any PR.
3. `gym.py`, #61 onto #29+#30+#32: docstring (all three rules), `Result` gets both `income`
   (dividends) and `cash_growth` (interest), `simulate(..., dividends=None, rates=())` takes both,
   G2's `_execute` call kept with #61's last-day comment. The event loop auto-merged: a
   dividend (`_DIVIDEND`, at the ex-date open) lands in cash and from then on accrues like any
   cash.
4. `report.py`, #61 onto #30: every replay (`live_results`, `restarted`, `yardsticks_beaten`,
   `backtest_results`, `backtest_scores`, `render_backtest`) now passes dividends **and** cash
   rates. `restarted` and `backtest_scores` take `dividends` then `cash`, both positional with
   defaults (no caller passes them positionally except `yardsticks_beaten` and `render_backtest`,
   which pass both).
5. `run_daily.py`, #61 onto #30: `check_record` checks both new append-only files
   (`data/dividends.csv`, `data/rates.csv`) for links and rewrites, and refuses bad rows in both;
   `run` fetches dividends, then rates. #15: import line has both `intraday` and `rates`.
6. `tests/test_run_daily.py`, #61 onto #30: the fake market answers both Yahoo requests (empty
   dividend events, and `^IRX` at 4%).
7. **decision** weekly page wording, #61 onto #30 (no textual conflict). #30 wrote "cash earns no
   interest" on the weekly page and in its DECISIONS entry; with #61 that is false. Now the page
   says cash earns the 3-month US Treasury bill rate, the G4 DECISIONS entry says paid-out
   dividends earn the cash rate, and `test_the_pages_say_how_high_the_deflated_sharpe_bar_is`
   checks the new wording. (#61's own PR body flags this.)
8. Noted, no change: #27's next-steps "watch" item (fully invested `equal_weight`
   cannot top up crypto) is what #29 fixes; whoever lands #29 can drop that item.

## Tests added (`tests/test_integration.py`)

Each rule has its own tests in its PR; these check that they compose:

- G2 x G4: `test_a_dividend_on_units_sold_to_fund_a_waiting_buy_is_spent_by_that_buy`: a switch
  from SPY to BTC on SPY's ex-date; the units sold at that open are paid first, and the waiting BTC
  buy spends sale + payout.
- G2 x fee tiers: `test_a_buy_waiting_for_cash_pays_the_fee_tier_of_the_open_it_fills_at`: the
  waiting buy pays 0.38% (the tier of the volume before its open), cash never below zero.
- G4 x interest: `test_a_dividend_paid_as_cash_earns_the_cash_rate`: the payout earns the rate
  every day after (weekends too), compounding, up to the replay's last day.
- G2 x interest: `test_cash_waiting_for_a_pending_buy_earns_interest_and_the_buy_spends_it`: the
  sale proceeds earn one night's interest, which the waiting buy spends.

When landing PR by PR, each test goes with the later of its two PRs (G2 x G4 with #30, G2 x fee
tiers with #32, both interest tests with #61).

## Research-tree PRs (#70 combo-1, #74 dsr-1): kept out, on purpose

Trial merge (a throwaway worktree, not pushed): both merge onto this branch with a conflict in
`next-steps.md` only, and all checks stay green (290 passed, ruff and format clean over the 148
files). So they do not block anything here. They are left out because:

- Neither touches live code (`src/`, the runner, the workflow), so they change nothing about the
  order or the conflicts above, and the gym PRs' review should not carry 200+ research files.
- #70 starts with a copy of the research stack (`research/lib`, `research/protocol.md`,
  `research/tries.md`, cards, ...). The open research-run PRs (#4, #7, #8, #9) add the same paths
  with different content: #70 x #9 conflicts on 7 files, among them `research/tries.md` and
  `research/protocol.md`. Whether `main` should hold a research tree at all, and which copy,
  is a separate decision (owner): landing #70 now would settle it by accident.
- #74 is small and self-contained (one script that imports only `grimstrade.stats`, one write-up)
  and conflicts with nothing but `next-steps.md`; it can land at any point, before or after this
  set. It reads `research/tries.md` from the research branches through git, so it does not need
  #70.

## Landing review fixes (2026-11-24, before the merge into `main`)

Three fresh review agents read the gym PRs, the ingest/workflow PRs and the rest. Required
fixes, applied in one commit on this branch:

1. Forward registry (#67): a rule's freeze time is now dated along HEAD's first-parent chain
   (`ledger.recorded_at(path, first_parent=True)`). Before, a registry line committed on a side
   branch with an old date and merged into `main` counted from the side commit's date. Test:
   `test_a_back_dated_side_branch_counts_from_its_merge`.
2. One example config: `local.example.toml` (#14) folded into `local.toml.example` (main), so
   `local.toml` has one template (`private_dir`, `[cache]`, `[alpaca]`, `[fred]`).
3. `docs/data-sources.md` and the honesty audit no longer say where the probes ran from (only
   "a local test machine, not a GitHub runner").
4. This file's header (landed as one merge, not PR by PR).

A dry run of the daily job (`run_daily --root <copy of paper-trail>`, then `--intraday`) passed
on this branch before the merge.

## Owner questions, answered by default (agent calls, 2026-11-24)

The items below were open for the owner. Under the rule "agents merge" (owner 2026-11-24) the
lead took each recommended default (`research/owner-decisions.md`, A1-A3); any of them can be
reversed by a later PR.


1. #61, open question 1: credit the full 13-week bill rate (assumes cash sits in a bill fund),
   or a spread or haircut below it? The integration uses the full rate, as #61 does. Changing it
   later is one number in `rates.steps` or `gym.cash_rate`, and every score replays.
   **Taken: full rate.**
2. #61, open question 2: scoreboard Sharpe is now above the bill rate, while research logs
   Sharpe against 0. Switch the research harness too? (Mixing only widens the deflated Sharpe's
   spread, the cautious direction.) **Taken: yes for new research rows; logged rows stay.**
3. #61, open question 3: a second, official source for the bill rate when Yahoo fails (until then
   the last rate carries forward). **Taken: yes, as a follow-up PR (BACKLOG).**
4. #15 changes `.github/workflows/daily.yml` (best-effort steps after the record push, and
   `actions: read`); the schedule is unchanged. Merging it changes what the live job does.
   **Taken: landed with the rest** (decisions-1 A3 suggested a week later; the dry run of both
   the record and the intraday steps passed, and every intraday step is best effort after the
   record push).
5. Each gym PR (#29, #30, #32, #61) changes every replayed score once. Landing all four in one
   day means one combined jump in the record instead of four.
6. G2 tops up to within the 1% band, not to the exact target (conflict 2 above). Fine as
   written; a narrower band for funded buys would be a new rule.
7. Whether `main` gets a research tree (#70 vs the research-run PRs #4, #7, #8, #9).
