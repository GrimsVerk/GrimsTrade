# Research archive 1 (branch `research-archive-1`, draft PR #118)

All research lanes in one merge into `main`, so the owner can land the research record with one
review instead of 90. Built by lane `archive-1` of the night-3 usage run (2026-11-19), following
option A of `research/pr-map.md` (section 4). Landed 2026-11-24 by the GrimsTrade lead (owner
rule "agents merge"), after the refresh below.

## Refresh before landing (2026-11-24)

- Merged the research tips opened after the first build: #117 `weather-2`, #125 `gate-power`
  (holds #120 `wide-13`), #121 `decisions-1` and #122 `fix-2` (both hold #119 `review-2`),
  #123 `risk-menu-4`, #124 `gate-null-2`, #28 `summary-1` (the leads' log; its `next-steps.md`
  stays on the branch).
- Merged `main` after #115 (the nine engineering PRs), then #75 `combo-2` itself (its #61 is on
  `main` now), so combo-2 is contained too.
- Conflicts: `next-steps.md` (rewritten as one short current log); `research/tries.md`,
  `research/gate-null.md`, `research/wide-1.md` (append-only: both sides kept; tries rows
  checked: none lost, none doubled).
- `tests/test_rl_env.py::test_batch_sim_equals_gym` marked xfail: the RL lanes' batch simulator
  copies the gym as it was; `main`'s gym now has waiting buys, dividends, fee tiers and cash
  interest. The RL line is closed and its logged results stand.
- `research/owner-decisions.md`: section "Answers" (each item's default taken as an agent call).
- Checks: ruff, format, mypy clean; pytest 646 passed, 4 xfailed. `docs/BACKLOG.md` is main's.
- Not in the archive: the register chain #79-#126 (it changes `ledger.py` and `run_daily.py`;
  its base #74 `dsr-1` is inside); it lands as its own engineering merge.

The rest of this file describes the first build (2026-11-19).

## In one screen

- Branch `research-archive-1` = `origin/main` (9b1c45e) + 30 research tips merged with `--no-ff`
  + combo-2's six research commits cherry-picked + one commit of mechanical check fixes.
- **Containment: 89 of the 90 research PRs** (pr-map's count) have their head commit inside the
  branch (`git merge-base --is-ancestor`). The one left out on purpose is **#75 `combo-2`**: its
  history contains the engineering PR #61 `cash-interest` (see "combo-2" below). Its research
  files are in the archive as cherry-picks, identical to the tip.
- **No engineering PR is inside** (#13 #14 #15 #27 #29 #30 #32 #61 #67 #79 #92 #100 #108 #111
  all checked: none is an ancestor). `integrate-1` (#115) handles those.
- **Checks green:** `ruff check`, `ruff format --check`, `mypy` (strict, src + tests), `pytest`:
  549 passed, 2 xfailed (one is main's own audit xfail, one new, below). `uv lock --check`
  clean.
- Outside `research/` the archive adds: dev dependencies `numpy`, `scikit-learn`, `xlrd` (+
  `uv.lock`), 4 fetch scripts in `scripts/`, 58 research test files and one fixture in
  `tests/`. **No change to `src/`, `.github/`, `docs/` (except this file), `ledger/` or
  `next-steps.md`** (except one pointer section). 711 files, ~125k lines added.
- Rerere was off for every merge (`git -c rerere.enabled=false merge ...`); the shared rr-cache
  holds no archive conflict.

## What to read to review it

1. `research/SUMMARY.md` (one page: what the research found).
2. `research/pr-map.md` (every PR, its verdict, the owner questions O1-O18).
3. This file (how the archive was built; what can be closed after a merge).
4. The diff outside `research/`: `pyproject.toml`, `uv.lock`, `scripts/fetch_*.py`, `tests/`.

## Merge order

Tree order of pr-map section 1, moving tips (`summary-*`, `pr-map`) last. "Contains" lists the
research PRs that come in with the tip (their heads are ancestors of it).

| # | Merged | PR | Contains | Conflicts and resolution |
|---|---|---|---|---|
| 1 | `review-1` | #8 | - | none |
| 2 | `fm-1` | #25 | #4 #7 #9 #16 #17 #18 #19 #21 #22 #23 #24 | next-steps (main's) |
| 3 | `ideas-1` | #20 | - | next-steps; ideas, tries (union) |
| 4 | `carry-3` | #31 | #26 | next-steps; ideas, tries (union) |
| 5 | `month-end-bonds` | #45 | #33 | next-steps; ideas, tries (union) |
| 6 | `risk-menu-3` | #110 | #47 #54 #57 #60 #64 #65 #72 #78 #83 #89 #98 #101 #105 | ideas, tries (union); next-steps auto-merged, reset to main's |
| 7 | `short-sleeve` | #99 | - | next-steps; tries (union) |
| 8 | `rp-1` | #86 | - | next-steps; tries (union) |
| 9 | `diversifier-1` | #95 | #91 | next-steps; tries (union, header fixed by hand in the next merge) |
| 10 | `breadth-screen` | #106 | #104 | next-steps; tries (union); tries header repair (see hand fixes) |
| 11 | `wide-12` | #112 | #71 #76 #81 #88 #93 #97 #102 #109 | next-steps; tries (union); **ideas by hand** |
| 12 | `gsy-1` | #55 | #34 #37 | next-steps; ideas, tries (union) |
| 13 | `bear-legs` | #103 | #66 #87 #90 #94 #96 | next-steps; tries (union) |
| 14 | `trend-where` | #43 | - | next-steps; tries (union); **`research/lib/trend_1926.py`, ideas by hand** |
| 15 | `eu-8` | #85 | #59 #62 #63 #68 #73 #77 #80 | next-steps; ideas, tries (union) |
| 16 | `usd-1` | #39 | #35 | next-steps; tries (union) |
| 17 | `stop-reentry` | #82 | #36 #40 #49 #53 #56 #69 | next-steps; ideas, tries (union); **README by hand** |
| 18 | `rl-6` | #52 | #38 #42 | next-steps; tries (union) |
| 19 | `volume-1` | #41 | - | next-steps; tries (union) |
| 20 | `evo-2` | #58 | #44 | next-steps; tries (union); **protocol, tries header by hand** |
| 21 | `micro-1` | #46 | - | next-steps; tries (union) |
| 22 | `research/exit-1` | #50 | #48 | next-steps; tries (union) |
| 23 | `data-long-2` | #51 | - | next-steps; tries (union) |
| 24 | `dsr-1` | #74 | - | next-steps reset to main's (not a pr-map tip: register-1 #79 contains it; merged directly so the research lands without the register chain) |
| 25 | `combo-1` | #70 | - | **hand merge** (copy of the research tree, below) |
| 26 | combo-2 (6 cherry-picks) | #75 | - | **cherry-picked without #61** (below) |
| 27 | `summary-3` | #107 | #84 | next-steps |
| 28 | `summary-1` | #28 | - | next-steps (summary-1 carries the leads' running log; merged at head d78a885) |
| 29 | `data-wide-1` | #114 | - | next-steps |
| 30 | `weather-1` | #116 | - | next-steps; tries (union) |
| 31 | `pr-map` | #113 | #107 | none |

#113, #114, #116 were opened after pr-map's snapshot (not in the 90); they are finished research
tips, so they are included. **Not included:** #117 `weather-2`, #119 `review-2`, #120 `wide-13`
(opened during this run, lanes still working). A refresh of the archive can merge them the same
way.

## Resolutions

**`next-steps.md`: main's file, untouched by every merge**, plus one pointer section at the top
("Research archive"). Each lane's own status section stays on its branch (and in
`summary-1`'s running log); copying 30 lane logs into `main`'s list of open tasks would bury it.
Where git auto-merged a lane's next-steps change without a conflict (risk-menu-3, dsr-1), it was
reset to main's version too.

**`research/tries.md` and `research/ideas.md`: union.** In each conflict hunk the archive keeps
its own lines, then the incoming branch's lines; a data row the archive already had (shared
history) is not added twice. From merge 5 on, hunks were taken in diff3 form; any hunk whose base
was not empty (a lane had edited an existing line, not appended) was stopped and resolved by
hand. Check after the last merge: every `tries.md` row of every merged tip is in the archive, 0
lost; the 12 rows that occur more than once occur equally often on a tip (repeated baseline
rows logged by the lanes themselves, kept as logged). `tries.md` has 3,131 rows. Every
`ideas.md` row of every tip is present verbatim except rows a later lane updated
(`critical-slowing`, `halloween`, `attention-sir`, `lunar`, `trend-1926`,
`trend-where-it-pays`); each appears once, in its latest form (`halloween` keeps its two rows in
two sections, as on the tips).

**Hand fixes:**

- `research/tries.md` header (merges 9-10): the union had split survey-6's extension of the
  `live-check` bullet from the bullet; repaired to survey-6's wording followed by ls-trend-1's
  `replication` bullet.
- `research/ideas.md` (merge 11, `wide-12`): wide-12 updated the `lunar` row; the archive keeps
  wide-12's row, the wide rows stay in the wide table, the survey-2/4/5 sections follow.
- `research/lib/trend_1926.py` (merge 14, `trend-where`, add/add): trend-where carried an
  unchanged copy of trend-1926's first commit (f725361); the archive keeps the later trend-1926
  line version. The five names trend-where uses (`load`, `universe`, `rule`, `hold`, `sym`) have
  the same signatures; trend-where's tests pass.
- `research/ideas.md` (merge 14): `trend-where-it-pays` takes trend-where's verdict;
  `trend-1926` keeps the later (trend-1926-fix) row.
- `research/README.md` (merge 17, `stop-reentry`): both lane paragraphs kept (trend-tune and
  trend-1926, then deep-1).
- `research/protocol.md` (merge 20, `evo-2`): both appended sections kept, in time order
  (rl-4's learner gate, 2026-11-17; evo-1's search tests, 2026-11-18).
- `research/tries.md` header (merge 20): rl-5's note goes back under the `screen` bullet; the
  kind bullets form one list.

pr-map's simulation named hand fixes in #43, #82 and #52; in this merge order they fell on
#43 (`trend_1926.py`), #82 (`README.md`) and #58 (`protocol.md`, which rl-6 and evo-2 both
extend), all resolved as above.

**combo-1 (#70), hand merge.** combo-1 starts from a copy of the research tree (commit f9cf713,
copied from coin-cap-3) on top of `main`, so it conflicts add/add with every research file the
stack changed since. Resolved as a 3-way merge with the copy commit as base: README, protocol,
risk-map and the coin-cap card and write-up keep the archive's (later) versions; ideas.md and
tries.md gain exactly combo-1's own 10 and 8 lines. The merge's net change equals combo-1's own
diff since f9cf713 (minus next-steps.md). #70's head is an ancestor.

**combo-2 (#75), cherry-picked, not merged.** combo-2 merges `cash-interest` (#61, an engineering
PR waiting on owner item O9: gym, rates, report, run_daily). Merging #75 would land #61's live
code through the archive (and GitHub would then count #61 as merged). Following pr-map
("landing #75 would also land #61"; "take #75's research files from the stack version, keeping
its combo write-up"), the archive cherry-picks combo-2's six commits after its #61 merge, with
their original authors, dates and messages (each records its source commit), leaving out
`next-steps.md` and the `rates` plumbing in `research/lib/harness.py` (it calls the gym API that
only #61 adds; without #61 it would break every harness run). The combo-2 write-up, results,
tries rows and `lib/combo2_*.py` are byte-identical to #75's head. Consequence: `combo2_*.py` can
be re-run only after #61 lands; then merge #75 itself (its harness change and #61 come with it;
expect trivial conflicts on the files that are already identical).

## Checks

Run in the worktree with `uv sync`, after the last merge (`8692e23`) and the fix commit:

| Check | Result |
|---|---|
| `uv run ruff check .` | pass (after the fix commit) |
| `uv run ruff format --check .` | pass (364 files) |
| `uv run mypy` | pass (94 source files, strict) |
| `uv run pytest` | 549 passed, 2 xfailed, 0 skipped, ~21 s, offline |
| `uv lock --check` | pass |

What failed before the fix commit (7451a19), and what was done (mechanical only; no research
number or result changed):

- ruff: 4 findings in scripts since moved out of the public repo (from `research/exit-1`, #50): two
  over-long f-strings split into shorter pieces (same output), two `zip()` calls given an
  explicit `strict=False` (same behaviour).
- pytest: `tests/test_evo_score.py::test_fast_scorer_matches_the_gym` (evo-1) failed: growth gap
  0.0050 against the card's tolerance 0.004. Cause: the tolerance was stated for the gym's 0.25%
  crypto fee; `main`'s gym defaults to 0.60% since the audit (G3, `docs/DECISIONS.md`). With the
  old fee restored in a throw-away pytest plugin, all three evo-score tests pass. Marked
  `xfail(strict=False)` with that reason; not deleted, numbers untouched.

All 58 research test files ran (pr-map's 45 plus 13 from later lanes); none needs network or
cached data, so nothing had to be skipped. One `RuntimeWarning` (divide by zero in a
`breadth_xs` test fixture) is from the lane's own test and harmless.

**Note for later re-runs (not changed here):** research code calls `gym.simulate` and
`harness.run` with `gym.COSTS` by default. On `main` that is the 0.60% crypto fee, so re-running
an old lane's script on the archive gives slightly worse numbers than the logged ones (logged
with 0.25%). `main`'s own next-steps already asks to tell the research lane; the cards' numbers
stay as logged.

## Containment (all 90 research PRs of pr-map)

`git merge-base --is-ancestor <PR head> origin/research-archive-1`, heads from `gh pr list` at
2026-11-19 ~03:05 UTC, after the last merge.

| PR | Branch | Head | In archive |
|---|---|---|---|
| #4 | `research-1` | 21a3a7d | yes |
| #7 | `research-2` | 0343bcb | yes |
| #8 | `review-1` | d8f3756 | yes |
| #9 | `research-3` | ef36478 | yes |
| #16 | `macro-1` | 8b97e42 | yes |
| #17 | `rl-1` | f7f7d23 | yes |
| #18 | `rl-2` | 3faa9f4 | yes |
| #19 | `rl-3` | b764f30 | yes |
| #20 | `ideas-1` | 01f4889 | yes |
| #21 | `info-1` | 3e076cf | yes |
| #22 | `breadth-1` | 9ee2e74 | yes |
| #23 | `short-1` | 2c4d55e | yes |
| #24 | `invest-1` | bbbca14 | yes |
| #25 | `fm-1` | 1547b02 | yes |
| #26 | `carry-2` | 93a0de3 | yes |
| #28 | `summary-1` | d78a885 | yes (still moving) |
| #31 | `carry-3` | a80d220 | yes |
| #33 | `wide-1` | 5cf48fd | yes |
| #34 | `trend-tune` | ca6c981 | yes |
| #35 | `slow-1` | 9fe1338 | yes |
| #36 | `deep-1` | e9a0d81 | yes |
| #37 | `trend-1926` | 3d3d6ff | yes |
| #38 | `rl-4` | 6f33168 | yes |
| #39 | `usd-1` | 0f4b735 | yes |
| #40 | `cointop-1` | 6413604 | yes |
| #41 | `volume-1` | 423896b | yes |
| #42 | `rl-5` | ca1439f | yes |
| #43 | `trend-where` | dc3c1fb | yes |
| #44 | `evo-1` | 7eba881 | yes |
| #45 | `month-end-bonds` | 0e8e0e6 | yes |
| #46 | `micro-1` | 1453f83 | yes |
| #47 | `wide-2` | 5759417 | yes |
| #48 | `data-long-1` | 3f0ad76 | yes |
| #49 | `coin-cap` | d6cdf09 | yes |
| #50 | `research/exit-1` | 19f9fc9 | yes |
| #51 | `data-long-2` | 94f783f | yes |
| #52 | `rl-6` | 59ae158 | yes |
| #53 | `coin-cap-2` | bb48351 | yes |
| #54 | `wide-3` | de28ac5 | yes |
| #55 | `gsy-1` | 35d155f | yes |
| #56 | `coin-cap-3` | c6d2a4f | yes |
| #57 | `wide-4` | 164a717 | yes |
| #58 | `evo-2` | cdc9d76 | yes |
| #59 | `eu-1` | 2ec2f7c | yes |
| #60 | `survey-2` | 52197f7 | yes |
| #62 | `eu-2` | 180a15d | yes |
| #63 | `eu-3` | fcc01d7 | yes |
| #64 | `survey-3` | b0b1ca5 | yes |
| #65 | `ann-1` | 837ed88 | yes |
| #66 | `trend-1926-fix` | 5b3cb41 | yes |
| #68 | `eu-4` | dc17c6a | yes |
| #69 | `coin-cap-4` | 09119fb | yes |
| #70 | `combo-1` | 573b595 | yes |
| #71 | `wide-5` | 3c0ddb9 | yes |
| #72 | `survey-4` | 31ff7a9 | yes |
| #73 | `eu-5` | dc09287 | yes |
| #74 | `dsr-1` | 875fd7a | yes |
| #75 | `combo-2` | 5a5fc2f | **no** (by design: contains #61; research files cherry-picked) |
| #76 | `wide-6` | 07ad3c0 | yes |
| #77 | `eu-6` | 39d8154 | yes |
| #78 | `survey-5` | d76575b | yes |
| #80 | `eu-7` | a69ba5c | yes |
| #81 | `wide-7` | ab8d20d | yes |
| #82 | `stop-reentry` | 4f76c33 | yes |
| #83 | `ls-trend-1` | 86159d7 | yes |
| #84 | `summary-2` | d328bef | yes |
| #85 | `eu-8` | 03a3c53 | yes |
| #86 | `rp-1` | 77addc7 | yes |
| #87 | `insure-1` | bd64961 | yes |
| #88 | `wide-8` | 9aafda7 | yes |
| #89 | `ls-trend-2` | ebe1f4c | yes |
| #90 | `insure-2` | 7f85ab8 | yes |
| #91 | `survey-6` | 04ab027 | yes |
| #93 | `wide-9` | 0f2aae0 | yes |
| #94 | `fast-reentry` | e34663f | yes |
| #95 | `diversifier-1` | 4092f3d | yes |
| #96 | `fast-reentry-2` | 032d429 | yes |
| #97 | `survey-7` | c4cb70b | yes |
| #98 | `vol-timing` | 0c1d48f | yes |
| #99 | `short-sleeve` | d585369 | yes |
| #101 | `risk-menu` | 1694c82 | yes |
| #102 | `wide-10` | 8137acd | yes |
| #103 | `bear-legs` | 4905fc6 | yes |
| #104 | `multi-signal` | 2fe7f66 | yes |
| #105 | `risk-menu-2` | 3f9f6ea | yes |
| #106 | `breadth-screen` | bcb0fa9 | yes |
| #107 | `summary-3` | f95859f | yes |
| #109 | `wide-11` | a700cae | yes |
| #110 | `risk-menu-3` | d1bcc86 | yes |
| #112 | `wide-12` | b513131 | yes |

Result: **89 / 90**. Also inside: #113 `pr-map`, #114 `data-wide-1`, #116 `weather-1`. Not
inside: all 14 engineering PRs, #115 `integrate-1`, and #117, #119, #120 (opened during this
run).

## After an owner merge: which PRs could be closed (proposal only)

Only if the owner merges this archive into `main` (option A). Re-run the containment check
first: `summary-1` (#28) and any lane still running may have moved past the archive.

- **Close as "landed via #118" (92 PRs):** the 89 contained research PRs above, plus #113, #114,
  #116. Six of them have base `main` (#4, #7, #8, #9, #70, #74): GitHub marks those merged by
  itself once `main` contains their heads. The others have research branches as base and must be
  closed by hand (a lane can post the comment; closing is the owner's call).
- **Keep open:** #75 `combo-2` until #61 (O9) is decided; then merge #75 (it brings #61 and the
  harness `rates` plumbing) or close it as landed if #61 lands on its own and the plumbing is
  re-applied. The 14 engineering PRs (integration in #115). #117, #119, #120 (newer research:
  refresh the archive or land them later the same way).
- **Watch:** #79 `register-1` has base `dsr-1` (#74). If #74 is closed, retarget #79 to `main`
  first (its diff then includes dsr-1's two files, which `main` would already have).
- **Never delete the branches:** the tries register (register-1) counts tries on every branch.

## Privacy

Public repo. `research/exit-1` (#50) is included like any other tip, as it stands on its
branch; this file quotes nothing from it beyond its title. The only
change to it here was the mechanical ruff fix above; its files later left the public repo.

## How to rebuild or refresh

Worktree off `origin/main`, then for each row of the merge table:
`git -c rerere.enabled=false -c merge.conflictStyle=diff3 merge --no-ff origin/<branch>`;
next-steps.md = `git checkout --ours`; tries.md/ideas.md = union per hunk (stop on any hunk
with a non-empty base); hand fixes as listed. combo-1: 3-way with f9cf713 as base. combo-2:
`cherry-pick --no-commit` of ad16186, 9417e2f, e08b7b6, a627194, baba20b, 5a5fc2f, dropping
`next-steps.md` and `research/lib/harness.py`. Then the containment check above.
