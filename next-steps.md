# Next steps

Running log of what is in flight on GrimsTrade. Lane logs before 2026-11-24 stay on their own
branches; the leads' night log is on branch `summary-1` (closed PR #28, branch kept).

## Rules since 2026-11-24 (owner: "agents merge")

- Every lane branches from current `main` and opens a PR to `main`. No lane on an unmerged lane.
- The GrimsTrade lead merges (rebase; a merge commit for long-diverged branches) when the checks
  pass and a fresh review agent finds no required fix. Changes to the daily runner, scoreboard or
  workflows also need a passing dry run of the daily job
  (`uv run python -m grimstrade.run_daily --root <copy of paper-trail>`, then `--intraday <dir>`).
- Research records land when the result is written, negative ones too.
- Never: push to `main` or `paper-trail`, rewrite `main`, delete a lane branch (the tries
  register counts branches).
- Public repo: no personal detail about the owner in files, commits or PR texts.

## Landing lead 1 (2026-11-24): clear the PR backlog

- DONE #115: engineering PRs #13 #27 #29 #30 #32 #61 #67 #14 #15 landed in one merge
  (`docs/integrate-1.md`; 291 tests; daily dry run passed).
- DONE #118: research archive (all research lanes; `docs/research-archive-1.md`); 81 contained
  research PRs closed or marked merged with "landed via #118".
- DONE #129: scoreboard footnote says Sharpe is above the cash rate.
- DONE #126: register chain (#79 #92 #100 #108 #111 + register-6) in one merge, with three
  review fixes (non-UTF-8 branch files cannot stop the daily run; try-shape logging only warns;
  `research/tries-shape.jsonl` merges by union). The returns store keeps buy-and-hold weekly
  series (weekly returns derived from Yahoo/exchange prices back to 1994): accepted as derived
  statistics, not bars (lead's call, `returnstore.py`).
- Owner decisions brief (`research/owner-decisions.md`): every item answered by its default as
  an agent call (section "Answers"); no owner question left.

## Night lead 2026-11-24/25 (handoff, lead 2; window 23:20-04:20 UTC)

Lead 1 (19:20-22:00 UTC) merged 26 PRs (#133-#165); lead 2 (23:20 UTC on) merged #166-#182 and
more (list below), each after a fresh review agent, review fixes applied before merging, head
branch re-pushed after each merge. Verdicts: `research/SUMMARY.md` (night 5, #183).

Lead 2 merged: #166 register-8, #167 vix-call-1, #168 e4-anatomy-1, #169 wide-18, #170
xs-century-1, #171 wide-17, #172 ownvol-anatomy-1, #173 wide-19, #174 data-long-4, #175
hedge-books-1, #176 wide-20, #177 survey-7b, #178 reentry-reconcile-1, #179 vm-style-1, #180
breadth-anatomy-1, #182 rev-costloss-1. LATE (see end of night log in this section).

**Held until after the 2026-11-25 daily run** (first run on tonight's new main; check it passed,
then merge in this order, each with `gh pr merge --merge`, then re-push the head branch): #149
gymreplay-1, #153 reconcile-daily-1, #155 scoreboard-note-1, #161 runner-faults-1. Reviewers
merged all four locally: no conflicts, dry run exit 0 with 0 reconcile problems. Main moved a lot
since (research files only, nothing in `src/`): expect clean merges, but re-run the checks.
#161's two open findings are strict xfails (next engineering lane, queue item 2).

**Repo setting:** GitHub auto-deletes merged head branches (`delete_branch_on_merge`); until the
owner turns it off, re-push each lane branch right after merging it
(`git push origin <sha>:refs/heads/<lane>`). AGENTS.md's "`gh pr merge --rebase --delete-branch`"
line conflicts with that (owner/CoS to settle).

**Privacy (CoS):** commit with `TZ=UTC`; all dates in files and PR text in UTC; neutral framing.

**Notes for the owner/CoS (not acted on):**
- `research/lib/long_x_fetch._get` (on main, older) sends a browser-like user agent to Yahoo;
  review of #174 flagged it as at odds with the no-evasion rule. Decide whether to change it.
- data-long-4 cached the JST Macrohistory R6 file (CC BY-NC-SA) from a plain script fetch made
  before the site began to 403 scripts; local cache only, nothing committed; the loader now
  treats it as a hand download (`--jst <path>`).

## Lane queue (each from `main`)

1. **After the 2026-11-25 daily run** (fires ~02:00-06:13 UTC): check it passed (Actions run
   green, `paper-trail` got the new rows, `reports/scoreboard.md` updated, `dividends.csv` and
   `rates.csv` created). Rerun `research/lib/reconcile1.py --work <scratch>` and confirm the
   one-time replay change it predicts (reconcile-1 table). Then merge #149, #153, #155, #161 one
   at a time (`gh pr merge --merge`, re-push the head branch after each). If the run fires after
   the 04:20 UTC hold, leave the merges for the next lead/day.
2. Engineering, after #161: fix its two strict xfails (Kraken answering from a later day must
   fall back to Coinbase; duplicate same-day bars in one answer must be refused or logged), and
   the smaller notes in #161's PR body (rate gap with no problem line; no overall fetch time cap).
3. Optional: `reconcile.py` reuses `gym.cash_rate` / `gym.interest` (review of #153).
4. Research, DEEPER: `e4` stays the only open lead (+0.063 on 41 stock markets, z 1.55). Its lead
   is explained (#168, #178): a graded buy-back after the low plus earlier partial exits; per fall
   its buy-back leaks like the old re-entry rules. Do not retune it; test again only on new
   independent data, pre-registered. The "legs agree" buy-back (+0.022/+0.028 in #178) is a
   diagnostic, not a lead, unless carded on independent data.
5. Research: fast-crash cover is closed for now (puts #160, puts-while-in #165, VIX calls #167:
   all a net cost). The century long-short style book (#170) is the closest thing to the bar
   (gross z 7.39, net 2.75; variance management #179 does not help). With data-long-4's real
   exchange rates (#174), a pre-registered rerun with the published currency-value definition
   would be a new counted try, not a fix: only if someone writes the card first and accepts it
   is close to retesting a failed book.
6. Survey-7b's other lead: tick-size split of trend (#181 tick-tier-1: by asset class the
   deciding statistic is inconclusive; against holding the paper's pattern is clear).
7. Evaluation: #184 evalue-forward-1 (anytime-valid sequential test for the forward registry):
   if it recommends adoption, an engineering lane implements it in `research/forward/`.
8. Data, owner only: the World Bank Pink Sheet (403 to scripts) and CBOE SPXTR (403) need a
   manual browser download if wanted (data-long-3, insure-3).
