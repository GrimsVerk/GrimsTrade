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

## Night lead 2026-11-24 (in flight; rewritten at handoff)

Merged tonight, each after a fresh review agent (fixes applied where it asked): #136, #133, #138,
#137, #134, #135, #140, #139, #143, #141, #147, #142, #148, #145, #144, #150, #154, #156, #152,
#157. Verdicts are in `research/SUMMARY.md` (night 4, #156).

**Held until after the 2026-11-25 daily run** (first run on tonight's new main; check it passed,
then merge in this order, each with `gh pr merge --merge`, then re-push the head branch, see
below): #149 gymreplay-1 (one simulator loop; review MERGE, CI green on the branch), #153
reconcile-daily-1 (daily live==gym check; review MERGE + try/finally fix applied), #155
scoreboard-note-1 (timing note; review wording fix applied), #161 runner-faults-1 (fault tests;
a half-written row now refuses the run with exit 2 naming the file and line instead of crashing;
review MERGE: the stricter check passes on the whole real record). Reviewers merged all four
locally: no conflicts, 892 tests pass, dry run exit 0 with 0 reconcile problems. #161's two open
findings (Kraken answering from a later day blocks the Coinbase fallback; duplicate same-day bars
in one answer, last wins) are strict xfails: next engineering lane.

Also merged after ~20:45: #154, #156, #152, #157, #159, #160, #158 (register-7: `--ref`, live
series keyed by code version; the next register regeneration must run `live` then `export` and
commit `research/register/returns/live.csv.gz`). Running at ~21:30 UTC: `gap-2002-1`
(per-series gap to holding since 2002; corrects SUMMARY's "But it has a price" line).

**Repo setting:** GitHub auto-deletes merged head branches (`delete_branch_on_merge`), against
the rule above; the owner was asked to turn it off. Until then, re-push each lane branch right
after merging it (`git push origin refs/heads/<lane>:refs/heads/<lane>`). AGENTS.md's
"`gh pr merge --rebase --delete-branch`" line conflicts with that rule too (owner/CoS to settle).

**Privacy (CoS):** commit with `TZ=UTC`; neutral framing (no country of residence, national tax
rules, or banks/brokers as "ours"); a history rewrite follows after the night run.

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
4. Research, DEEPER: `e4` is the only open lead (pooled-1 +0.063 on 41 equity markets; pooled-2
   +0.010 on bonds+FX; combined +0.045, z 1.43). Do not retune it. If tested again, pre-register
   on new independent data only.
5. Research, WIDER: fast-crash cover. insure-3: puts beat trend in fast crashes; insure-4 (running
   at ~21:45 UTC, check its PR) tests puts only while trend is in. Next: VIX-call overlays (VXTH
   was the only option index near trend's cost) on keyless CBOE data, statistics only (CBOE
   terms).
6. Data, owner only: the World Bank Pink Sheet (403 to scripts) and CBOE SPXTR (403) need a
   manual browser download if wanted (data-long-3, insure-3).
