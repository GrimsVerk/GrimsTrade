# PR map (open draft PRs, 2026-11-19)

One page to decide on the 104 open draft PRs (#4-#112) quickly. Written by the `pr-map` lane of
the night-3 usage run (draft PR #113); docs only, nothing merged or closed. State as of
2026-11-19 ~03:00 UTC (`gh pr list --state open --limit 200`). Verdicts come from each PR body and
its DONE line in `next-steps.md` on branch `summary-1`.

## In one screen

- **104 open PRs = 14 engineering changes aimed at `main` [E] + 90 research records [R].**
  Only the [E] ones change code that the live runner or scoreboard uses. 25 PRs also
  carry a question that only the owner can answer [O] (list in section 5).
- **The research PRs form one big stack** from `research-1` (#4) through `carry-2` (#26) into 8
  families. 64 of the 90 are **fully contained** in a descendant PR (`git merge-base
  --is-ancestor`), so they need no separate review. Only **26 research tips** hold all the work.
- **Merging all 26 tips into `main` was simulated locally** (never pushed): 22 of the 25 stack tips merge with only
  mechanical conflicts in three append-only or log files; 3 need a small hand fix; the
  `combo`/`register` chains need a hand merge of the research files they copied. The archive
  adds no `src/` or workflow change (only research tests, 3 fetch scripts and two dev
  dependencies).
- **Proposed landing:** (1) engineering PRs one by one, in the order of section 3 (the
  `integrate-1` lane is already building the conflict-resolved version); (2) all research in
  **one "research archive" PR**; (3) then close the 90 research PRs as "landed via the archive".
  Never delete their branches (the tries register counts every branch).

Legend: [E] engineering change to `main`, [R] research record, [O] waits on an owner decision
(item number in section 5), **tip** = no other open PR contains this branch.

## 1. Tree by base chain

- base `main`
  - #4 `research-1` [R]: Idea lab run 1: 14 classic ideas carded and tested; nothing beats `tsmom12`. Superseded (contained in every research PR).
  - #7 `research-2` [R]: Run 2, ML rung: 7 ML cards, all dead (Sharpe 0.67-0.94 vs 1.05). Superseded (contained in every research PR).
  - #8 `review-1` [R] **tip**: Independent review of runs 1-2: decisions hold, one headline does not.
  - #9 `research-3` [R]: Run 3, risk map: 20 variants, three presets (`research/risk-map.md`). Superseded (contained).
    - #16 `macro-1` [R]: macro-1: six macro cards, all fail; halving "passes on numbers" but not believed. Closed.
      - #17 `rl-1` [R]: rl-1: PPO agents 0.57-0.71 vs 0.99 out of sample. Closed.
        - #18 `rl-2` [R]: rl-2: residual RL tilt on `tsmom12`: 0.96-0.98 vs 0.99. Closed.
          - #19 `rl-3` [R]: rl-3: planted-signal control: inputs bind before the learner. Closed.
            - #21 `info-1` [R]: info-1: 23 new inputs, none useful at weekly IC. Closed.
              - #22 `breadth-1` [R]: breadth-1: wide books / hourly: one coin-book pass, does not carry over. Closed.
                - #23 `short-1` [R]: short-1: a short side on perps adds nothing; carry near miss. Closed.
                  - #24 `invest-1` [R]: invest-1: no slow signal passed for a monthly stock/bond/cash mix; `ecy-trend` parked; investing-agent sketch.
                    - #25 `fm-1` [R] **tip**: fm-1: zero-shot forecasting model = memorised history; IC ~0 out of memory. Closed.
                  - #26 `carry-2` [R]: carry-2: funding carry replicates weakly on unseen venues; gone at 30 bps. Base of the night stacks.
                    - #28 `summary-1` [R] **tip**: summary-1: first one-page summary; this branch also carries the leads' `next-steps.md` log (still moving).
                      - #84 `summary-2` [R]: summary-2: one-page summary after night 2 (contained in #107).
                        - #107 `summary-3` [R] **tip**: summary-3: SUMMARY.md refresh (end of night 2). Base of this PR.
                    - #31 `carry-3` [R] **tip**: carry-3: `band` FAILS the one held-out year (spent here). Carry parked.
                    - #33 `wide-1` [R]: wide-1: 46 cross-field mechanisms, 4 carded, all fail. Base of the wide/survey stack.
                      - #45 `month-end-bonds` [R] **tip**: month-end-bonds: not replicated on clean data; do not spend a held-out year.
                      - #47 `wide-2` [R]: wide-2: trend age, patch-leaving, crowded-trend: all fail.
                        - #54 `wide-3` [R]: wide-3: hedge-regime, attention-peak, opex-pin: all fail.
                          - #57 `wide-4` [R]: wide-4: tax-drain and coupon-dose fail.
                            - #60 `survey-2` [R]: survey-2: 2023-26 survey; `fomc-cycle` reverses after publication.
                              - #64 `survey-3` [R]: survey-3: `xtsmom` fails.
                                - #65 `ann-1` [R]: ann-1: FOMC day premium gone after publication.
                                  - #72 `survey-4` [R]: survey-4: ts-carry, halloween fail.
                                    - #78 `survey-5` [R][O]: survey-5: live trend funds vs `tsmom12`; the "~80% decay" is one same-manager pair, mostly the effect fading after its sample (`errata-2.md`). O8.
                                      - #83 `ls-trend-1` [R][O]: ls-trend-1: crisis alpha needs shorts AND a wide universe. O6.
                                        - #89 `ls-trend-2` [R][O]: ls-trend-2: wide long-short blend at 1x fails Sharpe; a risk choice. O6.
                                          - #98 `vol-timing` [R]: vol-timing: ls-trend-2's control is vol timing; no card; edge lanes CLOSED.
                                            - #101 `risk-menu` [R][O]: risk-menu: 11 risk dials side by side, no pick. O2.
                                              - #105 `risk-menu-2` [R][O]: risk-menu-2: menu on 1994-2025; ranking holds. O2.
                                                - #110 `risk-menu-3` [R][O] **tip**: risk-menu-3: own-vol target without look-ahead: menu order unchanged. O2.
                                        - #99 `short-sleeve` [R] **tip**: short-sleeve: 10% SPY/QQQ downtrend short fails; narrow sleeves CLOSED.
                                      - #86 `rp-1` [R][O] **tip**: rp-1: `where-vol` is not risk parity; smaller worst loss = smaller size. O5.
                                      - #91 `survey-6` [R]: survey-6: no live family beat its plain index after fees.
                                        - #95 `diversifier-1` [R] **tip**: diversifier-1: merger-arb slot fails once cash earns T-bills.
                                        - #104 `multi-signal` [R]: multi-signal: style signals on the six: breadth too small.
                                          - #106 `breadth-screen` [R] **tip**: breadth-screen: style signals on 34 ETFs all within chance; CLOSED.
                            - #71 `wide-5` [R]: wide-5: dealer-backlog, extension-dose fail.
                              - #76 `wide-6` [R]: wide-6: critical-slowing-down and lunar gates fail.
                                - #81 `wide-7` [R]: wide-7: wash-sale echo, festival gold, rmd-december gates fail.
                                  - #88 `wide-8` [R][O]: wide-8: gate t-values overdispersed; forward entry proposed, not frozen. O4.
                                    - #93 `wide-9` [R]: wide-9: W19, W17 dead; gate-null method note (placebo ranks).
                                      - #97 `survey-7` [R]: survey-7: seasonal-20y gate fails.
                                        - #102 `wide-10` [R]: wide-10: fed-purchase-flow, stablecoin-mint dead.
                                          - #109 `wide-11` [R][O]: wide-11: hedging-pressure dead; F1/F2 scoring filters; only crypto-carry left. O1.
                                            - #112 `wide-12` [R] **tip**: wide-12: candidates against F1/F2, custody-selling gate (night 3, may still be running).
                    - #34 `trend-tune` [R]: trend-tune: 12 months is not beaten; rule pays on stocks; re-entry late. Base of trend/eu/insure stacks.
                      - #37 `trend-1926` [R]: trend-1926: trend beats holding 1927-61, but it is crash insurance (1929-32, 1973-74).
                        - #55 `gsy-1` [R] **tip**: gsy-1: run-up crash flag replicates weakly; not a candidate.
                        - #66 `trend-1926-fix` [R][O]: trend-1926-fix: replay gaps explained (Friday holidays); era-2 tests. O12.
                          - #87 `insure-1` [R]: insure-1: trend lost less than holding in 20/21 US market falls (50 with industry-only falls), avoiding 0.50 of each vs 0.27 at random timing; cheaper than holding less shown only for 1927-1961 (`errata-2.md`).
                            - #90 `insure-2` [R]: insure-2: insurance holds across eras and 13 non-US indices; costs ~1.3-1.5 per unit saved.
                              - #94 `fast-reentry` [R]: fast-reentry: `or3-12` is a bigger position, not cheaper insurance.
                                - #96 `fast-reentry-2` [R]: fast-reentry-2: `arm3-12` in between; insure/re-entry line CLOSED.
                                  - #103 `bear-legs` [R] **tip**: bear-legs: bear-market rallies look like the bottom; line stays closed.
                      - #43 `trend-where` [R] **tip**: trend-where: per-asset trend filter ties `tsmom12`; closed by data-long-2.
                      - #59 `eu-1` [R][O]: eu-1: `tsmom12` on euro UCITS funds keeps its character. O13.
                        - #62 `eu-2` [R]: eu-2: fixed per-order fees by book size; hedged US equity does not remove the drag.
                          - #63 `eu-3` [R]: eu-3: order cutters change the rule; small coin-free book not worth it at the smallest sizes.
                            - #68 `eu-4` [R]: eu-4: whipsaw diagnosis; flip reducers fail the character card.
                              - #73 `eu-5` [R][O]: eu-5: 5/25 band cuts small-book orders by a third at the same rule. O10.
                                - #77 `eu-6` [R][O]: eu-6: trend vs holding for a small coin-free euro book: crash insurance only. O5.
                                  - #80 `eu-7` [R][O]: eu-7: trend in fewer places loses the insurance. O5.
                                    - #85 `eu-8` [R][O] **tip**: eu-8: euro cash interest changes nothing; eu line CLOSED. O5.
                    - #35 `slow-1` [R]: slow-1: no input forecasts at 4 or 13 weeks. Closed.
                      - #39 `usd-1` [R][O] **tip**: usd-1: dollar 13-week change does not replicate. Closed. Tip (optional check needs an API key, O18).
                    - #36 `deep-1` [R]: deep-1: failure atlas of 52 models; no combination beats `tsmom12`.
                      - #40 `cointop-1` [R]: cointop-1: coin-top exits pass nowhere; a smaller coin position, not a better rule.
                        - #49 `coin-cap` [R]: coin-cap: a plain cap on coin weight ~ same worst loss as the stop; bar not met.
                          - #53 `coin-cap-2` [R][O]: coin-cap-2: stop beats matched cap in 15/21 coin falls (p 0.039), below the family bar. O14.
                            - #56 `coin-cap-3` [R][O]: coin-cap-3: daily-checked stop adds return via cheaper re-entries, not shallower losses. O14.
                              - #69 `coin-cap-4` [R][O]: coin-cap-4: no candidate meets the bar; verdict page; coin line parked. O14.
                                - #82 `stop-reentry` [R] **tip**: stop-reentry: 13-week cool-off wins 13/21 (needs 17). Coin line parked.
                    - #38 `rl-4` [R]: rl-4: lasso passes the planted gate; no RL variant does. Closed.
                      - #42 `rl-5` [R]: rl-5: screened perp inputs: none passes Holm. Closed.
                        - #52 `rl-6` [R] **tip**: rl-6: power analysis; RL/perp line CLOSED (4 reopen triggers).
                    - #41 `volume-1` [R] **tip**: volume-1: own volume does not forecast. Closed.
                    - #44 `evo-1` [R]: evo-1: GP search: noise control and plant gate fail. Closed.
                      - #58 `evo-2` [R] **tip**: evo-2: calibrated plant found 1/3: gate fails. Evo line CLOSED.
                    - #46 `micro-1` [R] **tip**: micro-1: minute-bar features do not forecast weekly. Closed.
                    - #48 `data-long-1` [R]: data-long-1: free long bond and gold histories verified; loader.
                      - #50 `research/exit-1` [R] **tip**: exit-1: exit-rule and re-entry research; review FINAL.
                      - #51 `data-long-2` [R] **tip**: data-long-2: gold loader; trend-where closed on bonds/gold.
          - #20 `ideas-1` [R] **tip**: ideas-1: eight video-sourced rules, all fail.
  - #13 `data-search-1` [E]: Data-source catalogue (`docs/data-sources.md`), docs only.
  - #14 `ingest-1` [E] **tip**: Ingest 1: rolling-window snapshot + write-once local cache, backfill scripts; runner untouched. Has 1 commit not in #15.
    - #15 `ingest-2` [E] **tip**: Ingest 2: daily intraday collection inside the daily job (Actions cache, not published); edits the workflow.
  - #27 `health-1` [E][O] **tip**: Health 1: weekly page names the risk presets; live check notes. Open question on run schedule (O15).
  - #29 `g2-pending-buy` [E] **tip**: G2: an unpaid buy waits for cash; sells fund pending buys (live bug seen on 2026-11-17).
  - #30 `g4-dividends` [E] **tip**: G4: ETF dividends paid as cash on the ex-date (append-only dividend store).
  - #32 `fee-tiers` [E] **tip**: Crypto fee by 30-day volume tier (replaces the flat taker fee).
  - #61 `cash-interest` [E][O]: Cash earns the 13-week T-bill rate; Sharpe above cash (live + backtests). O9.
  - #67 `forward-1` [E][O] **tip**: forward-1: forward-only shadow registry (offline module, 18 tests, proposals not frozen). O11.
  - #70 `combo-1` [R]: combo-1: failure map; `blend-ws` closest miss (p 0.059). Based on `main` with a COPY of the research tree.
    - #75 `combo-2` [R] **tip**: combo-2: combo with T-bill cash (merges #61); combo line CLOSED. Tip; contains #61 and #70.
  - #74 `dsr-1` [R][O]: dsr-1: project-wide deflated Sharpe: `tsmom12` beats zero, not equal weight. Base of the register chain. O8.
    - #79 `register-1` [E][O]: register-1: scoreboard reads every branch; project-wide tries register + BAR.md (touches ledger/run_daily). O7.
      - #92 `register-2` [E][O]: register-2: measured trial correlation; bar +0.30..+0.56 Sharpe (touches ledger/register). O3.
        - #100 `register-3` [E]: register-3: harness logs try shape; family-capped correlation (touches register/tryshape).
          - #108 `register-4` [E]: register-4: committed weekly-returns store; BAR.md rebuilds on any checkout (touches register/returnstore).
            - #111 `register-5` [E] **tip**: register-5: register regenerated (3,130 tries, eff. N 486); harness writes weekly returns into the store. Tip of the register chain.

Opened after the snapshot (night 3, not in the counts above):

- #113 `pr-map` -> `summary-3` [R]: this map and the SUMMARY.md refresh.
- #114 `data-wide-1` -> `wide-11` [R] **tip**: keyless data sources for the F1/F2 filters (no
  gates, no returns).
- #115 `integrate-1` -> `main`: integration preview of the [E] PRs with conflicts resolved;
  review aid, **do not merge as-is** (section 3).
- #116 `weather-1` -> `wide-11` [R] **tip**: heating-degree-day surprise vs next-week natural
  gas: gate fails (t -0.29, rank 19 of 41). Count now 80 mechanisms / 19 tested / 0 passed.

## 2. Categories

**(a) Engineering changes aimed at `main` [E] (14).** Verified by the files each PR changes
against its base (anything outside `research/`):

| PR | Branch | Live code touched | Owner item |
|---|---|---|---|
| #27 | `health-1` | `weekly.py` (page names the risk presets) | O15 |
| #13 | `data-search-1` | docs only (`docs/data-sources.md`) | - |
| #29 | `g2-pending-buy` | `gym.py` (unpaid buy waits for cash) | O16 |
| #30 | `g4-dividends` | `gym.py`, `data.py`, `sources.py`, `report.py`, `run_daily.py`, `weekly.py` | O16 |
| #32 | `fee-tiers` | `gym.py` (crypto fee by 30-day volume tier) | O16 |
| #61 | `cash-interest` | `gym.py`, new `rates.py`, `report.py`, `run_daily.py` | O9 |
| #14 | `ingest-1` | new `cache.py`, `intraday.py`, backfill scripts (runner untouched) | - |
| #15 | `ingest-2` | `run_daily.py`, `.github/workflows/daily.yml` (intraday collection) | - |
| #67 | `forward-1` | new `forward.py` (offline only) | O11 |
| #79 | `register-1` | `ledger.py`, `run_daily.py`, new `register.py` (scoreboard N ~300 -> ~2,900) | O7 |
| #92 | `register-2` | `ledger.py`, `register.py` | O3 |
| #100 | `register-3` | `register.py`, new `tryshape.py` | - |
| #108 | `register-4` | `register.py`, new `returnstore.py` (+3.9 MB returns store) | - |
| #111 | `register-5` | research harness only (regenerated register) | - |

Not [E] although based on `main`: #70 `combo-1` and #74 `dsr-1` change only `research/`
(#70 copies the whole research tree onto `main`); #75 `combo-2` is research too but contains a
merge of #61, so landing #75 would also land #61. #4, #7, #8, #9 are research PRs into `main`.

**(b) Research records [R] (90).** Every other PR: card, write-up, `research/tries.md` rows,
research tests. Value is the record, not code. None changes `src/`, the workflow or the ledger.

**(c) Waiting on an owner decision [O] (25 PRs).** Tagged in the tree; questions in section 5.

## 3. Proposed review and merge order for (a)

The `integrate-1` lane (draft PR #115, branch `integrate-1`, "do not merge as-is") is building
a conflict-resolved integration branch of these PRs, with the resolutions written up in
`docs/integrate-1.md`; at 03:00 UTC it holds #13, #27, #29, #30 and a G2 x G4 test. Reviewing that branch
once is cheaper than rebasing each PR. Suggested order (smallest risk first, gym changes in one
row so each rebase is done once):

1. **#27 `health-1`**: 3 files, weekly page wording. No code conflicts.
2. **#13 `data-search-1`**: docs only.
3. **#29 G2 pending buy**: fixes a live bug seen 2026-11-17.
4. **#30 G4 dividends**: makes the fund yardsticks fair.
5. **#32 fee tiers**: conflicts with #29 in `gym.py` (neighbouring lines).
6. **#61 cash interest**: after O9 is answered. Conflicts with #29 and #30 in `gym.py`, with
   #30 in `report.py`, `run_daily.py`, `tests/test_run_daily.py`, with #15 in `run_daily.py`.
   Land it last of the gym four so it is rebased once. Unlocks fair "above cash" scoring.
7. **#14 then #15 ingest**: #14 has one commit not in #15 (#15's base is stale): merge #14
   first, then rebase #15. #15 edits the daily workflow (asks for `actions: read`): read it
   closely. Both conflict with the register chain in `.gitignore` only.
8. **#67 forward-1**: after O11. Offline module; conflicts only in `docs/DECISIONS.md`.
9. **Register chain as one merge of #111** (contains #74, #79, #92, #100, #108): after O7 and
   O3. Changes the live scoreboard's try count (every live deflated Sharpe drops). Conflicts
   with #75 `combo-2` in `research/lib/harness.py`.

Mechanical conflicts everywhere: every branch edits `next-steps.md` (each carries its own status
section) and most edit `docs/DECISIONS.md` / `docs/DESIGN.md` (append-style entries). Keep
both sides for the docs and one current log for `next-steps.md`. (Pairwise `git merge-tree`
check of all [E] PRs, 2026-11-19.)

## 4. Proposal for (b): land 90 research PRs without 90 reviews

Proposal only; nothing has been closed or merged.

**Facts (computed 2026-11-19):**

- Containment (`git merge-base --is-ancestor head(A) head(B)` for every pair): 64 research
  PRs are contained in a descendant; e.g. `carry-2` (#26) is inside 72 others. The 26 research
  tips are #8, #20, #25, #28, #31, #39, #41, #43, #45, #46, #50, #51, #52, #55, #58, #75, #82,
  #85, #86, #95, #99, #103, #106, #107, #110, #112 (plus #114, #116 and this #113, opened
  later; #113 contains #107).
- The research stack branched from an old `main` (before M1 and the audit). `main` has moved
  on, but only outside `research/`, so it does not conflict except in `next-steps.md`.
- Local simulation (detached worktree off `main`, never pushed): merging the tips one after
  another, 22 of the 25 stack tips merge with at most `next-steps.md` (keep one log) and
  `research/tries.md` / `research/ideas.md` (append-only: union merge) conflicts. Three need a
  hand fix: #43 `trend-where` (`research/lib/trend_1926.py`), #82 `stop-reentry`
  (`research/README.md`), #52 `rl-6` (`research/protocol.md`). #75 `combo-2` (a copy of the
  research tree on `main`) conflicts in 6 research files and `research/lib/harness.py`.
- What the archive would add outside `research/`: `pyproject.toml` dev deps `numpy`,
  `scikit-learn` (+ `uv.lock`), 3 fetch scripts in `scripts/`, 45 research test files (5.7k
  lines). No `src/`, workflow or ledger change. Total ~611 files, ~105k added lines. Research
  tests were not run in the simulation.

**Option A (recommended): one research-archive PR into `main`.**

1. A lane creates `research-archive` from `main` (after the [E] PRs it wants to sit on, or
   before; they do not overlap), merges the 26 tips in tree order, union-merges
   `research/tries.md` and `research/ideas.md`, hand-fixes the 3 files above, takes #75's
   research files from the stack version (keeping its combo write-up), and runs the checks.
2. The owner reviews ONE PR, mostly by reading `research/SUMMARY.md`, this map, and the diff
   outside `research/` (two dev deps, three scripts, tests).
3. After the merge, each research PR is closed with "landed via #<archive>" (GitHub will not
   auto-close them: their bases are other research branches, not `main`). A lane can post the
   comments; closing is the owner's call.
4. Branches stay. The register (`register-1`) counts tries on every branch; deleting branches
   would make the bar look lower than it is.

**Option B: archive branch, no merge to `main`.** Same as A, but `research-archive` stays a
branch and the PRs are closed against it. Keeps `main` small (research never runs live), at the
cost of research tests and the `research/` tree not being on `main`. Fine if the owner wants
`main` = live system only. Note: `research/register/` and BAR.md are read by the register
chain (#79-#111), so if the register lands on `main`, its inputs should land too (A).

**Option C: close the 64 contained PRs now, keep the 26 tips open.** Cuts the list to 40 open
PRs (26 research + 14 engineering) without any merge; then A or B for the tips. Safe because
every contained PR's commits stay reachable from its descendant branch.

Do not: merge the stack bottom-up (90 merges and retargets), or squash the stack (loses the
commit dates the protocol relies on: "card committed before numbers").

## 5. Owner decisions ([O] items, from "For the owner" in `next-steps.md` on `summary-1`)

- O1 (#109): allow perpetual futures in the paper gym? Only way to test `crypto-carry`, the last
  candidate passing the F1/F2 filters.
- O2 (#101, #105, #110): pick a risk level from `research/risk-menu.md` (main decision).
- O3 (#92): accept the measured bar (12..486 effective tries, the bar at the cautious 486: z >= 4.69, +0.30..+0.56 Sharpe over `tsmom12` for rules correlated 0.77-0.93 with it; #126)?
- O4 (#88): freeze forward entry `turn-of-year-losers@1`? Allow W18 to use a 2026 event inside
  the held-out year?
- O5 (#86, #77, #80, #85): want a smaller worst loss simply by holding `tsmom12` at a smaller
  size (~70% invested)?
- O6 (#83, #89): add shorts to the paper broker (borrow fees, interest, 1x rescale) for a
  forward test of a wide long-short trend book? (design change, proposal only)
- O7 (#79): adopt the project-wide tries register and "every card quotes BAR.md"?
- O8 (#74, #78): treat the live rule as a drawdown/risk choice, not an edge?
- O9 (#61, also inside #75): merge cash interest; (a) full T-bill rate or a spread below it,
  (b) research Sharpe "above cash" too, (c) a second keyless rate source?
- O10 (#73): use the 5/25 rebalance band in the paper runner?
- O11 (#67): adopt the forward registry and freeze `carry-3-band@1`?
- O12 (#66): move `common.weekly` to the calendar Friday (own card; shifts every lane slightly)?
- O13 (#59): add a euro-fund copy of the live six as a paper book?
- O14 (#53, #56, #69, #82): coin `stop-0.25` as a risk preference (not a proven rule): rule PR?
- O15 (#27): daily runs fire 02:00-04:40 UTC, not 22:30; crypto fills ~22 h after decision.
  Accept or move the schedule?
- O16 (#29, #30, #32): engineering PRs ready for review; merge is the owner's. (Optional from
  #34: a 2.5-5% rebalance band, same Sharpe, 15-25% less trading.)
- O17 (#33): should the paper broker be able to fill at the close?
- O18 (#39): optional robustness check needs a data API key; cannot change the verdict.

## 6. Lines closed vs still open

**Closed during night 2 (2026-11-18/19):** exit research (#50, review FINAL); evolved
rules (#58); RL / perps (#52); `trend-where` (#51); run-up flag (#55, not a candidate); blends
(#75); euro-book variants (#85); coin rules (parked: #69, #82; risk preference only); crash
insurance / faster re-entry (#96, #103); volatility timing as an edge (#98); narrow short
sleeves (#99); merger-arb slot (#95); style signals on keyless ETFs (#104, #106); forced
Treasury flows (#71); published calendar effects (0 for 5: #60, #64, #65, #72, #97).

**Closed before night 2:** ML (#7), macro (#16), RL 1-3 (#17-#19), new inputs (#21),
breadth (#22), short side (#23), foundation models (#25), funding carry (held-out year spent,
#31), slow inputs (#35, #39), atlas/combinations (#36), coin-top exits (#40), volume (#41),
minute bars (#46), month-end bonds (#45), wide-1/2 mechanisms (#33, #47).

**Still open:**

- Wide gates under the F1/F2 filters: `wide-12` (#112, night 3: W23 custody-selling dead,
  wrong sign; W24 inflation-disagreement running), `weather-1` (#116, dead), `data-wide-1`
  (#114, data only). Count 80 mechanisms / 19 tested / 0 passed.
- Register: `register-5` (#111, night 3); adoption waits on O7/O3.
- Risk menu (#101, #105, #110): waits on O2; a forward run of the chosen dial needs a monthly
  share reset in the runner.
- Forward registry (#67, #88): waits on O11/O4.
- Crash-gaining long-short book (#83, #89): waits on O6. `crypto-carry`: waits on O1.
- Engineering queue (section 3) and euro paper book (O13).

## Method and caveats

- Tree: `gh pr list --state open --limit 200 --json number,headRefName,baseRefName`, nested by
  base branch. Categories from `git diff --name-only origin/<base>...origin/<head>`.
- Containment and the merge simulation used `origin/*` refs fetched 2026-11-19 ~02:40 UTC.
  Lanes still running (#111, #112, `integrate-1`) may add commits; re-run the containment check
  before closing anything.
- #28 `summary-1` also carries the leads' running `next-steps.md` log, so it keeps moving until
  the night run ends; land it last.
- Privacy: this is a public repo; descriptions stay generic.
