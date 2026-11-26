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

**Merges stopped at 02:02 UTC, resumed 2026-11-25 ~09:15 UTC:** GitHub's merge commits carry a
non-UTC offset and the bot account's own email; the owner OK'd both on 2026-11-25, so agents
merge again with `gh pr merge --merge` (re-push the head branch after each).

**Morning merges 2026-11-25 (CoS cleanup agent, 09:15-10:35 UTC):** #192 jst-autocorr-1, #193
panic-words-1 (keeps W34; tries.md merged by union), #194 wide-21 (renumbered W34 -> W35, R34 ->
R35 per the steps below; count 103 / 29 / 30, bar 0.00097; tries.md note row added), then the
runner PRs one at a time after the passing 2026-11-25 daily run (Actions run 04:57 UTC green,
paper-trail got rows, `dividends.csv` and `rates.csv` created, scoreboard updated;
`reconcile1.py` rerun: 0 late bars, 0 class (b)/(c), the 2026-11-25 snapshot equals the gym on
`main` for all 12 books, so the one-time (d) change happened): #149 gymreplay-1, #153
reconcile-daily-1, #155 scoreboard-note-1, #161 runner-faults-1. Each was merged with `main`
first (merge commit; DECISIONS.md conflicts resolved newest first), full tests passed and
a daily dry run on a copy of paper-trail exited 0 (reconcile: 12 books, 0 problems; intraday exit
0). SUMMARY updated by #195 summary-7 (the #186 timing correction below is done; review fixes
applied). This handoff (#185) merged last.

**Open PRs at handoff (history: all merged on the morning of 2026-11-25, see above; were
unmerged by the CoS's no-merge decision):** #185 (this handoff), #149, #153, #155, #161 (held for the
daily run), #192 jst-autocorr-1 (review result in its PR or the night log), and the last lanes'
PRs: #194 wide-21 (W34 solar-max-recession fails) and #193 panic-words-1 (W34 panic-words
fails). Both used gate id W34 and both count 102/29/29: whichever merges second becomes W35
and the count 103/29/30 (bar 0.10/103). **Review (02:55 UTC): #193 MERGE, #194 MERGE.** #193
was carded first, so it keeps W34; #194 becomes W35 (replication R35). Merge #193 first, then
on #194's branch: merge main (union for gate-null.md/tries.md), then W34->W35 and R34->R35 in
research/gate-null.md (its two rows, the cyclic-dose note, and the count paragraph: 30 gates,
W27-W35, 103/29/30, bar 0.00097), research/wide-21.md (plus 'renumbered from W34 at merge; the
card says W34 (provisional)'), research/lib/wide21.py, research/lib/wide21_events.py,
research/results/solar-max-recession.md:1, research/ideas.md (the wide-21 gate row); append a
tries.md note row 'wide-21's W34 = W35' (never edit the old row). Cards stay unchanged. #193's raw text cache (~30 GB, CC-BY newspaper text) sits
in the local data cache `panic-words-1/` and can be deleted; monthly counts are committed (check `gh pr list`; each needs a fresh review first unless the
night log says "review: MERGE"). #192 review: MERGE (no required fixes).

**SUMMARY correction (done in #195):** #186's "holds, narrowly on timing" must say
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

## Night lead 2026-11-25/26 (window 21:00 UTC -> weekly reset 09:00 UTC)

Lanes run in parallel, each with its own worktree and PR to main; every PR merged only after a
fresh Opus review found no required fix (fixes applied by the lane, then merged; runner PRs also
after a daily dry run on a copy of paper-trail). Head branches re-pushed after each merge; lane
worktrees removed after merge.

Merged: #196 reconcile-reuse-1, #197 fx-value-real-1, #198 e4-indep-1, #200
registry-lrv-1, #201 survey-8, #202 wide-22, #203 calm-drag-1, #204 jst-autocorr-2, #199
runner-faults-2 (three review rounds: per-request cap with `read1`, early-EOF `IncompleteRead`
restored; daily dry runs exit 0, 0 reconcile problems), #205 wide-23, #208 registry-moments-1,
#207 gate-null-2, #209 rl-7, #206 data-wide-2, #212 insure-1709-1, #211 summary-8 (SUMMARY night 6),
#210 jst-gates-1. Verdicts: `research/SUMMARY.md` (night 6).

Lead 2 (from ~22:50 UTC) merged: #214 asset-ledger-1, #213 lead-next-1126 (the night's handoff), #215
wide-24 (W40 dead), #216 survey-9, #217 summary-9, #218 eng-nits-1 (infer_pos flat-day fix, sign-test
ties), #219 insure-bonds-1, #220 stale-checks-1, #221 wide-25 (W41 dead), #222 fx-peg-1, #223
wide-26 (W43 dead, W18 closed dead), #225 insure-jstbonds-1, #224 dw2-dates-1 (data-wide-2 date
parse and BoE $/£ 1857-10 spike), #226 wide-27 (W44 dead; counts 111/29/40). SUMMARY night 6
covers #218-#226 (summary-10).

**For the owner (decisions, not acted on):**
- Yale ICF data (London Investor's Monthly Manual 1869-1929, NYSE 1815-1925, St Petersburg):
  terms: "supplied solely for academic research purposes; any commercial use or redistribution
  without the authorization of the authors and the International Center for Finance at Yale is
  prohibited". Cached locally by data-wide-2, counts
  only. No rule test may use them until the owner decides or Yale authorizes (#206).
- robots.txt: data.nber.org, api.db.nomics.world and Riksbank `*.xls` disallow scripts. The lead
  ruled no exemption for API hosts (DBnomics cache deleted, #206). Earlier lanes (data-long-1,
  e4-indep-1) fetched a few data.nber.org files by script before this was noticed; NBER files
  are manual-download only from now on.
- gate-null-2 (#207) PROPOSES (not adopted): for gate doses with lag-1 acf >= 0.8, a pass must
  also rank <= 2 of 41 among 40 phase-randomised surrogates (IAAFT for skewed doses), on top of the
  shifted calendars. "Both" beat surrogates alone by a margin within noise, and the 0.8 threshold
  rests on one borderline cell (about 0.3 SE).

## Lane queue (each from `main`)

1. ~~Open at the first handoff: #214, #213, wide-24, survey-9, summary-9~~: all merged (#213-#217).
2. Closed tonight, do not redo: `e4` (contradicted on pre-1927 stocks, #198: no longer a lead;
   the clean keyless independent monthly stock data are nearly used up, apart from the Yale IMM stocks, data-wide-2
   rank 2, which wait on the owner's ruling), real-rate FX value and
   sleeve swaps of #170's book (#197 kill rules), the RL line for price-only inputs (#209), the
   calm-drag split (#203), JST source timing (#204), the gate-null size study (#207), W36-W41, W43, W18, W44, the insurance
   on long bonds and floating FX (#219, #222, #225: exposure only) and the stale checks (#220). The previous
   night's do-not-redo list is in the night-lead 2026-11-24/25 section above and in SUMMARY.
3. DEEPER next: (a) a sovereign-bond pool (Yale IMM bonds) or the IMM stocks with its own crash calendar (data-wide-2 rank 1) only
   after the owner rules on the Yale terms; Norges Bank bonds and BoE consols done (#219), JST
   bonds (#225), floating FX (#222): the insurance there is exposure only; (b) ~~a peg filter
   before any currency trend test on the long FX histories~~: done in #222; (c) the US railroad stocks 1857-1870 (NBER: manual download) are the
   only unspent pre-1871 US stock months.
4. WIDER next: further fields per wide-21..24 conventions (events dated as the market could
   know them; robots.txt read before the first fetch; crawl delays kept); `crackdown-shock`
   (wide-23 C2) needs a hindsight-free dated list first. `strike-idleness` (still not
   run) needs BLS, which asks for a contact e-mail in the User-Agent: never send a personal one;
   skip it unless the owner provides a generic project contact.
5. Engineering: ~~`infer_pos` flat-day flips; `fetch_from` after `IncompleteRead` test; `REVISION_DAYS` repeat note~~: done in #218.
6. Data, owner only: World Bank Pink Sheet and CBOE SPXTR (403 to scripts), NBER ch. IV
   commodities and non-US bonds, IFS/OECD via DBnomics, Riksbank: manual browser download if
   wanted.
7. New from lead 2's lanes:
   (a) `patent-surge` (wide-27 O1, scored 6) is parked on data: it needs FRED release 486
   per-country patent grants once ALFRED/fredgraph answers scripts again.
   (b) MeasuringWorth's DJIA could replace stale-checks-1's OCR series (#220) only with
   permission for scripted use (owner).
   (c) ParlGov's licence was not read (Dataverse bot challenge): check it in a browser before
   redistributing anything derived from it (#221).
   (d) ~~W41's unpredicted negative 12-month side (t -2.60, post hoc) needs a new card on
   independent JST years 1921-1959 (b < 0), if anyone wants it~~: done in #229 (dead).
   (e) ~~mypy reports 21 errors in `tests/test_wide25.py` on main (from #221): fix in an
   engineering lane.~~ Done in this PR (eng-mypy-1).
