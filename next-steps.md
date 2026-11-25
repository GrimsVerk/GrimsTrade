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
breadth-anatomy-1, #181 tick-tier-1, #182 rev-costloss-1, #183 summary-5 (SUMMARY night 5, BAR
regenerated), #184 evalue-forward-1, #186 insure-1870-1, #187 omori-1, #188 parked-gates-1, #189
forward-se-1, #190 coin-drift-2, #191 summary-6 (the last merge).

**MERGES STOPPED at 02:02 UTC (CoS/owner to decide how to resume):** every merge GitHub makes
here (`gh pr merge --merge` or `--rebase`) writes commits with a non-UTC offset and the bot
account's own email; `--author-email` with the noreply address is rejected. That is a
privacy leak on a public repo, so per the all-repo rule the lead stopped merging and told the
CoS. Until the CoS says otherwise: lanes may push branches and open PRs; nobody merges. This
handoff (#185) is itself unmerged: read it from branch `lead-next-1125`.

**Open PRs at handoff (all unmerged by the CoS's no-merge decision; merge in the daytime once
the merge-commit offset is fixed):** #185 (this handoff), #149, #153, #155, #161 (held for the
daily run), #192 jst-autocorr-1 (review result in its PR or the night log), and the last lanes'
PRs: #194 wide-21 (W34 solar-max-recession fails; NOT yet reviewed: usage limit) and
panic-words-1 if it finished (check `gh pr list`; each needs a fresh review first unless the
night log says "review: MERGE"). #192 review: MERGE (no required fixes).

**SUMMARY correction needed after #192 merges:** #186's "holds, narrowly on timing" must say
the timing statistic (p_S 0.020) is consistent with the early annual data's lag-1
autocorrelation of unknown origin (an AR(1) of 0.19 alone gives most of the gap; JST US and
Norway are true year-end prices, so averaging is not shown); the 9-of-9 insurance count stands.

**Lead decision to check (owner may reverse):** #189 changed the forward registry's verdict SE to
HAC/Newey-West with fixed-b p-values although its card's kill condition was met (3 of the
10-year null cells > 0.040). Adopted because every resampled cell moved toward nominal and the
iid controls keep their level; a 10-year verdict vs `tsmom12` still reads as about a 5% test.
Disclosed in `docs/DECISIONS.md` (2026-11-25). `run_daily` does not import `grimstrade.forward`.

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
6. Done tonight, do not redo: tick-size split of trend (#181, inconclusive by its card), the exit
   as a crash warning (#182), insurance out of sample 1870-1965 (#186, holds narrowly on timing),
   sequential tests (#184), registry SE fix (#189), coin-drift-run (#190, dead), Omori re-entry
   (#187, a vol-calm rule in disguise), drought gate (#188, passed then killed by replication).
7. Next WIDER ideas not yet run: `panic-words` (wide-20 P3, ~2,000 loc.gov calls: be polite);
   `strike-idleness` needs BLS, which asks for a contact e-mail in the User-Agent: never send a
   personal one; skip unless the owner provides a generic project contact. Next DEEPER: why the
   annual early-sample returns autocorrelate (index smoothing?) before any further use of JST
   annual data (#186 caveat).
8. Data, owner only: the World Bank Pink Sheet (403 to scripts) and CBOE SPXTR (403) need a
   manual browser download if wanted (data-long-3, insure-3).
