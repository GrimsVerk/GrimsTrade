# Owner decisions: one brief (decisions-1)

Lane `decisions-1`, 2026-11-19, draft PR #121 (-> `review-2`). Docs only; nothing merged,
closed or changed elsewhere. Source: the "For the owner" list in `next-steps.md` (branch
`summary-1`, about 20 entries), deduplicated against `research/pr-map.md` (O1-O18, #113),
`docs/integrate-1.md` (#115), `docs/research-archive-1.md` (#118) and
`research/reviews/review-2.md` (#119). Where review-2 corrected a number, the corrected one is
used and cited ("review-2 s.3b" = section 3b). No new numbers.

Each item: the question, options, what each option changes, evidence, a **recommended default**
with its reason, and what it unblocks. Saying "yes to the defaults" to every item is a
consistent set: no default contradicts another.

## If you only have 5 minutes

The five answers that unblock the most, in order. Each links to its full item below.

1. **[A4](#a4-research-archive-pr-118) Land the research record as one archive PR (#118, option
   A), then close the ~92 contained research PRs as "landed via #118" (branches kept).**
   Default: yes, after the engineering PRs. Clears ~92 of ~110 open PRs and settles whether
   `main` holds a research tree (#70).
2. **[A1](#a1-engineering-prs-landing-order) Land the engineering PRs in the `integrate-1`
   order: #13, #27, #29, #30, #32, #61, #67, #14, #15, the four gym PRs on one day.**
   Default: yes. Fixes the live G2 bug, adds dividends and fee tiers; every replayed score
   shifts once, not four times.
3. **[A2](#a2-cash-interest-61) Cash interest (#61): full T-bill rate; new research scored
   above cash; add the second rate source.** Default: yes to all three. Unblocks #61, #75
   `combo-2`, the landing slot of #15, and fair scoring of any rule that holds cash.
4. **[B1](#b1-project-wide-tries-register-and-the-bar) Adopt the project-wide tries register
   and the measured bar (#79 ... #111, one merge of #111).** Default: yes, with review-2's
   wording of the bar. Unblocks 5 register PRs and gives every later lane one bar to quote.
5. **[C2](#c2-the-risk-level-for-the-paper-book) The risk level: keep the three presets side by
   side and add one paper book, own-vol target (70%, no-look-ahead form).** Default as stated.
   Closes the risk-menu, smaller-size and own-vol questions (#101, #105, #110, #86, #77, #80,
   #85) and tells a lane what runner change to build.

One item has a calendar deadline: [B3](#b3-freeze-turn-of-year-losers1) (freeze the
turn-of-year forward test). Default is "no"; a "yes" must come before 2026-11-30.

## Index (all items)

| Id | Question (one line) | Default | Unblocks |
|---|---|---|---|
| A1 | Land the 9 engineering PRs in `integrate-1`'s order, gym PRs on one day? | Yes | #13 #27 #29 #30 #32 (+#61 #67 #14 #15 after A2/B2/A3) |
| A2 | Cash interest #61: (a) full bill rate? (b) research above cash? (c) second source? | Yes / yes for new work / yes | #61, #75, #15's slot, fair cash scoring, C2 |
| A3 | #15 adds steps to the live daily workflow: land it? | Yes, last, after a green week | #15 (and #14 before it) |
| A4 | One research archive PR into `main` (#118)? | Yes (option A), after A1 | ~92 PRs closable, #70 settled |
| A5 | Close contained research PRs as "landed via #118", branches kept? | Yes, after A4 | Clean PR list |
| B1 | Adopt the tries register, "every card quotes BAR.md", the measured bar? | Yes | #79 #92 #100 #108 #111 |
| B2 | Adopt the forward registry (#67); freeze `carry-3-band@1`? | Adopt; freeze nothing now | #67, queue item 5 |
| B3 | Freeze `turn-of-year-losers@1` (wide-8)? Deadline 2026-11-30 | No | Closes O4a |
| B4 | Move `common.weekly` to the calendar Friday? | No, keep and document | Closes O12 (#66) |
| B5 | Let W18 use the 2026 World Cup (inside the held-out year)? | No; gate on 2006-2024 only | Queue item 3 (W18 can run) |
| B6 | Allow perpetual futures in the paper gym (for `crypto-carry`)? | No | Closes queue item 4 |
| B7 | Add shorts to the paper broker (wide long-short trend book)? | Not now; after C2 | Closes O6 for now |
| C1 | Treat `tsmom12` as a risk choice, not an edge? | Yes | Frames C2-C4 |
| C2 | Risk level for the paper book (menu / smaller size / own-vol dial) | Keep presets + add own-vol 70% book | Risk-menu PRs; a runner lane |
| C3 | Coin `stop-0.25` as a rule PR? | No; coin size is the risk budget | Closes O14 |
| C4 | Euro-fund paper book, with the 5/25 band? Wider band for the US runner? | Not now; keep the 1% band | Closes O10, O13 for now |
| D1-D7 | Small items (schedule, fill at the close, API key, stale notes, ...) | See D | - |

## A. Landing the PRs

About 110 draft PRs are open: 14 engineering PRs aimed at `main` (they change code the live
runner or scoreboard uses) and about 90 research records (pr-map s.2). Merging stays the
owner's; agents never merge.

### A1. Engineering PRs: landing order

- **Question:** land the 9 main-bound engineering PRs one by one in the order `integrate-1`
  tested: #13 -> #27 -> #29 -> #30 -> #32 -> #61 -> #67 -> #14 -> #15?
- **Options:**
  1. Yes, in that order, with the four gym PRs (#29, #30, #32, #61) on the same day.
  2. Yes, but spread over days (four separate jumps in the replayed record).
  3. Hold some back (each PR can wait; only #32 and #61 depend on the earlier gym PRs).
- **What it changes:** #13 docs only; #27 weekly page names the presets; #29 an unpaid buy waits
  for cash (live bug seen 2026-11-17); #30 ETF dividends as cash on the ex-date (new append-only
  `data/dividends.csv`); #32 crypto fee by 30-day volume tier; #61 see A2; #67 see B2; #14/#15
  see A3. **Each gym PR changes every replayed score once** (integrate-1, "For the owner" 5).
  Landing all four on one day gives one combined jump instead of four. Conflicts are resolved in
  `integrate-1`'s merge commits (22 files, 3 real behaviour choices); copy them while rebasing.
  Checks after all 9: 290 passed (main: 211 + 1 xfail).
- **Evidence:** `docs/integrate-1.md` (#115, branch `integrate-1`), pr-map s.3.
- **Recommended default: option 1.** Reason: the order is tested green end to end, and one
  jump in the record is easier to read than four.
- **Note (no action needed):** with G2, a funded buy tops up to within the 1% band, not to the
  exact target (integrate-1 conflict 2). Fine as written; a narrower band would be a new rule.
- **Unblocks:** #13, #27, #29, #30, #32 directly; #61 after A2, #67 after B2, #14/#15 after A3;
  A4 (the archive is best refreshed on the new `main`).

### A2. Cash interest (#61)

This one item appears three times in the old list (integrate-1, combo-2 #75, cash-interest).

- **Question:** #61 pays idle cash the 13-week T-bill rate (`^IRX`, keyless) in live and
  backtests and measures the scoreboard Sharpe above that rate. Three sub-questions:
  - (a) pay the **full** bill rate (as if cash sits in a T-bill fund), or a broker-style spread
    below it (for example the benchmark minus 0.5%, or nothing on a first slice)?
  - (b) switch the **research harness** to Sharpe above cash too (it logs Sharpe against 0)?
  - (c) add the US Treasury's keyless daily bill-rate CSV as a **second rate source** (today a
    failed fetch carries the last rate forward)?
- **Options and what they change:**
  - (a) full rate: as built. A spread: one number in `rates.steps` or `gym.cash_rate`; every
    score replays again when it changes.
  - (b) yes: new research rows are scored above cash; logged rows stay as logged (they are
    never rewritten). Mixing the two conventions only widens the deflated Sharpe's spread, the
    cautious direction (#61 body). No: research keeps Sharpe against 0 while the scoreboard
    uses above-cash.
  - (c) yes: a small follow-up PR (keyless; no owner risk). No: carry-forward stays the
    fallback.
- **Effect (train 1994-2025, #61 body):** `tsmom12` CAGR 17.64% -> 18.19%, `sixty_forty` 8.09% ->
  8.63%; scoreboard Sharpes fall for every book (convention change, not a loss). The live
  record earns interest only from the day after the first run with this code; nothing earlier
  changes. With interest, combo-2 (#75) changed no verdict; diversifier-1 (#95) shows why it
  matters: a held merger-arb slot passed at z 4.86 with cash at 0 and failed at z 2.23 once cash
  earned T-bills.
- **Evidence:** #61 body ("Open questions"), `docs/integrate-1.md` items 1-3, combo-2 #75,
  diversifier-1 #95.
- **Recommended default: (a) full rate, (b) yes for new work only, (c) yes.** Reason: (a) a
  T-bill fund is available to a small investor and keeps one number for live and backtests;
  (b) lanes already score anything that holds cash against a same-size T-bill slot (lane
  queue rule since #95), so this only writes the rule down; (c) removes a silent stale rate at
  no cost.
- **Unblocks:** #61 merge (A1 slot 6); then #75 `combo-2` can merge (it contains #61) or close
  as landed; #15 lands after #61 (they touch `run_daily.py`); `combo2_*.py` can be re-run; C2's
  menu already assumes T-bill cash, so the live presets get the same footing.

### A3. #15 changes the live daily workflow (with #14)

- **Question:** #14 (`ingest-1`: rolling snapshot, write-once local cache, backfill scripts;
  runner untouched) and #15 (`ingest-2`: daily intraday collection inside the daily job). #15
  edits `.github/workflows/daily.yml` (best-effort steps after the record push, asks for
  `actions: read`); the schedule is unchanged. Land them?
- **Options:** (1) both, #15 last; (2) #14 only, #15 later; (3) neither.
- **What it changes:** #15 is the only PR in the set that changes what the live job does each
  night. Collection only: no intraday trading (VISION lists intraday trading before daily
  works as "not doing"; collecting data is not trading).
- **Evidence:** `docs/integrate-1.md` ("For the owner" 4; merge rows 8-9), pr-map s.3 item 7.
- **Recommended default: option 1, with #15 landed about a week after the gym PRs run green.**
  Reason: #14 is risk-free; #15 is low risk but touches the unattended job, so it should not land
  in the same week as the score-changing gym PRs.
- **Unblocks:** the ingest pair; nothing else waits on it.

### A4. Research archive (PR #118)

- **Question:** land all research in one merge (`research-archive-1`, #118) instead of about 90
  reviews?
- **Options (pr-map s.4):**
  - A: one archive PR into `main` (built: 89 of 90 research PRs contained; checks green, 549
    passed, 2 xfailed).
  - B: keep the archive as a branch; close the PRs against it; `main` stays live-system only.
  - C: close the 64 contained PRs now with no merge; decide A or B for the 26 tips later.
- **What each changes:**
  - A: `main` gets the research tree (711 files, ~125k lines), dev dependencies `numpy`,
    `scikit-learn`, `xlrd`, 4 fetch scripts, 58 research test files (~21 s, offline). **No change
    to `src/`, `.github/`, `ledger/`.** This also settles the #70 question (whether `main` holds a
    research tree): yes, and #70's copy is merged inside. #75 `combo-2` is left out on purpose
    (it contains #61; its research files are cherry-picked) and lands after A2.
  - B: `main` stays small, but the register chain (B1) reads `research/register/` on `main`; with
    B and B1 both, those inputs would have to land separately.
  - C: no risk, does not land anything; still needs A or B later.
- **Caveat:** old research scripts re-run on `main` give slightly worse numbers than logged
  (gym default crypto fee 0.60% vs 0.25% when they ran); the cards keep their logged numbers.
  The evo-1 fast-scorer test is marked xfail for that reason (research-archive-1, "Checks").
- **Evidence:** `docs/research-archive-1.md` (#118), pr-map s.4.
- **Recommended default: A, landed after A1, with a refresh first** (a lane re-merges onto the new
  `main`, adds the later tips #117, #119-#122, re-runs the checks and the containment table).
  Reason: one review instead of 90, consistent with B1, and the archive and the engineering PRs
  do not overlap.
- **Unblocks:** A5 (close ~92 PRs); B1's inputs on `main`; #70's question.

### A5. Close the contained research PRs

- **Question:** after A4 lands, close each contained research PR with "landed via #118"?
- **Options:** (1) yes, branches kept; (2) yes and delete branches; (3) leave them open.
- **What it changes:** 6 of them have base `main` and GitHub marks them merged by itself; the
  others are closed by hand (a lane can post the comments; closing is the owner's). Keep open:
  #75 until A2, the 14 engineering PRs, any newer lane. Retarget #79 to `main` before closing
  #74 (its base). **Never delete the branches:** the register counts tries on every branch, so
  deleting them would make the bar look lower than it is (option 2 breaks B1).
- **Evidence:** `docs/research-archive-1.md` ("After an owner merge"), pr-map s.4 step 4.
- **Recommended default: option 1, after re-running the containment check.** Reason: every
  closed PR's commits stay reachable; the list shrinks to the open work.
- **Unblocks:** a readable PR list.

## B. Project rules

### B1. Project-wide tries register and the bar

Merges two old entries: register-1 (#79, adopt the register and "every card quotes BAR.md")
and register-2 (#92, accept the measured bar).

- **Question:** count research tries on every branch (not only `main` and `research-*`) plus
  an append-only register `research/register/tries.jsonl`, have every card quote the
  project-wide bar from `research/register/BAR.md` before any number, and accept the measured
  bar for a new pick?
- **Options:**
  1. Adopt as proposed (convention in `docs/DESIGN.md`, PROPOSED; DECISIONS 2026-11-12 rule
     revised), with the bar worded as review-2 corrected it.
  2. Adopt the register (the count) but not a fixed bar; each card picks its own N.
  3. Keep the 2026-11-12 rule (reads `main` and `research-*` only).
- **What each changes:**
  - 1 and 2: the live scoreboard's N jumps from about 300 to about 2,900+ and **every live
    deflated Sharpe drops** (#79). `ledger.py`, `run_daily.py` and a new `register.py` change;
    the register chain lands as one merge of #111 (contains #74, #79, #92, #100, #108; adds a
    3.9 MB committed weekly-returns store so `BAR.md` rebuilds on any computer). Branches may
    never be deleted (A5).
  - 3: the live N stays at about 300 while the project has logged 3,130 tries (register-5):
    the undercount DECISIONS 2026-11-12 calls "the dishonest direction".
- **The bar, as review-2 corrected it (s.1):** N_eff about 486 is the **cautious end** of a
  measured range (12 by cluster count to 486 by average correlation), not a single measurement.
  At 486: z >= 4.69, which is **+0.30 to +0.56 Sharpe over `tsmom12` for rules correlated
  0.77-0.93 with it**; less correlated rules use the z column. Any counting choice puts the
  close-rule bar between +0.21 and +0.34 (+0.25 to +0.32 defensible), so "nothing has cleared
  it" holds either way. **Correction:** the largest lead seen on the main test is +0.23
  (`halving-alone`, z about 3.2-3.6), not +0.18; it fails at 4.69 but sits at the cluster-count
  bar (3.29), the one result where the counting method decides (review-2 s.1c). Lane `fix-2`
  (#122) is applying this wording to SUMMARY.
- **Evidence:** dsr-1 #74 (`research/dsr-1.md`), register-1..5 #79 #92 #100 #108 #111
  (`research/register/BAR.md` on `register-5`), review-2 s.1.
- **Recommended default: option 1.** Reason: VISION's first priority is the honesty of the
  record, and every branch can only raise N (the cautious direction); review-2 found the
  arithmetic sound.
- **Unblocks:** the register chain (#79, #92, #100, #108, #111) in the A1 queue after #15;
  every later card has one bar to quote; the live scoreboard counts the same tries as research.

### B2. Forward registry (#67)

- **Question:** adopt the forward registry (judge a frozen rule only on data after its freeze
  commit; `src/grimstrade/forward.py`, 18 tests, offline command) and freeze `carry-3-band@1`?
- **Options:**
  1. Adopt the rules, freeze nothing now; the other candidates stay descriptive.
  2. Adopt and freeze `carry-3-band@1` (the lane's recommendation).
  3. Do not adopt.
- **What each changes:** 1: #67 lands (new module, not imported by the runner; conflicts only in
  `docs/DECISIONS.md`). 2: also a lane writes a carry adapter that must snapshot the perp lists
  and commit **every week** for the test's life (venues drop delisted coins later), so it needs
  an owner-made schedule (a local timer or a new weekly workflow). 3: #67 closes.
- **Years needed at 80% power (alpha 0.025 each, forward-registry doc):** `carry-3-band` 12.7
  (7.3 as a lone test at 0.10), coin stop 26.2 (about 55 counting independent episodes),
  monthly-vs-weekly euro clock 31.5, FOMC bond drift 78.1. carry-3 `band` already failed its one
  held-out year (pooled Sharpe -0.65, #31); if the truth is half the train Sharpe, it needs four
  times the years.
- **Evidence:** `docs/forward-registry.md` (branch `forward-1`, #67), carry-3 #31, rl-6 #52.
- **Recommended default: option 1.** Reason: the registry's main use is as a filter ("anything
  that needs decades is decided on other grounds now"); a weekly job for 7-13 years on a rule
  that failed its held-out year is a poor use of it. Revisit freezing carry only if B6 ever
  changes.
- **Unblocks:** #67 (A1 slot 7); lane queue item 5 (forward items) gets its rules; B3.

### B3. Freeze `turn-of-year-losers@1`

- **Question:** freeze wide-8's proposed forward test of the turn-of-year rebound of ETFs that
  lost over the year (first unseen turn 2026/27)?
- **Options:** (1) no; keep the proposed entry as a record, and a lane may print the January 2027
  numbers as description only; (2) yes.
- **What "yes" changes:** `forward.py` needs a new metric (`placebo_rank`), and the registry's
  0.10 alpha is split five ways (0.02 each) instead of four. Deadline: freeze before the dose is
  known (end of November 2026, so before 2026-11-30); the hard limit is the window start,
  2026-12-31.
- **Evidence:** wide-8 #88 (`research/wide-8.md`, step 1): the empirical null over 153 placebo
  windows has SD 2.18; a pass needs t >= 4.87; **power 8%** at the lead's own slope (5% at half),
  so one turn will most likely say "fail" whatever the truth. A multi-turn version needs on the
  order of ten turns.
- **Recommended default: option 1.** Reason: with 8% power the verdict carries almost no
  information, and freezing costs code plus an alpha split for every other forward rule.
- **Unblocks:** closes O4's first half.

### B4. `common.weekly` on the calendar Friday?

- **Question:** move the shared weekly sampler `common.weekly` from "one session later on
  Friday-holiday weeks" to the calendar Friday?
- **Options:** (1) keep it, and write the convention into `research/protocol.md`; (2) move it,
  under its own card.
- **What each changes:** 2 shifts every lane's numbers a little; logged rows stay as logged, so
  old rows would no longer reproduce on new code. 1 changes nothing.
- **Evidence:** trend-1926-fix #66: the replay gaps were Friday-holiday weeks; no look-ahead; no
  number changed by more than 0.012; one era-1 sign flip (energy), verdict unchanged.
- **Recommended default: option 1.** Reason: no look-ahead and an effect of at most 0.012 do not
  justify making 3,000 logged rows irreproducible.
- **Unblocks:** closes O12.

### B5. The held-out year and the 2026 World Cup (W18)

- **Question:** may W18 `elimination-mood` use the 2026 World Cup (June-July 2026), which lies
  inside the held-out year 2025-11-11..2026-11-09?
- **Context:** carry-3 (#31) spent that year in its one held-out run. Every other lane still
  leaves it unread; the first year nobody has seen started 2026-11-10 (forward-registry doc).
- **Options:** (1) no: W18 runs its gate on the post-sample train tournaments 2006-2024 only;
  (2) yes: the 2026 tournament joins the gate.
- **What each changes:** 1: W18 can start now; about 25 eliminations of three countries, a weak
  design (wide-8), and by review-2 s.5a a clustered gate with so few episodes is **kill-only**
  (it can reject the idea, not confirm it). 2: a second look into a spent held-out year, for a
  handful of extra events.
- **Evidence:** wide-8 #88 (W18 row), review-2 s.5a, `research/protocol.md` (held-out year:
  once, one finalist).
- **Recommended default: option 1.** Reason: keeps the held-out rule simple ("unread except by
  its one finalist"), and the gate can only kill the idea anyway. Ask again only if it passes.
- **Unblocks:** lane queue item 3 (W18's gate can run now).

### B6. Perpetual futures in the paper gym?

- **Question:** allow perpetual futures (a short leg and funding payments) in the gym, the only
  way to test `crypto-carry`, the last candidate passing the F1/F2 scoring filters (wide-11)?
- **Options:** (1) no, the gym stays long-only spot; (2) yes, as a research-only gym mode; (3)
  yes, in the live paper broker.
- **What each changes:** 2 and 3 change `docs/DESIGN.md` (long-only), add funding data and a
  short leg; 3 also changes the live runner. 1 closes queue item 4.
- **Evidence:** wide-11 #109; carry-3 #31 (the carry book failed its held-out year: -0.65, about
  22% lost on price, not costs or funding); carry-2 #26 (weak replication, gone at 30 bps);
  short-1 #23; rl-6 #52 (246 training weeks detect only Sharpe >= 0.98; RL/perp line closed).
  DECISIONS 2026-11-12: carry not built because the gym is long-only spot.
- **Recommended default: option 1.** Reason: the one carry book tested failed its held-out year,
  and the available perp history can only detect a Sharpe near 1.
- **Unblocks:** closes O1 and queue item 4.

### B7. Shorts in the paper broker?

- **Question:** add shorts (borrow fees, interest on short proceeds, rescale to 1x) so a wide
  long-short trend book could be forward-tested?
- **Options:** (1) not now (proposal stays parked); (2) research-only short support; (3) shorts
  in the live paper broker.
- **What each changes:** 2 or 3: a design change to the long-only gym, 34 ETFs, about 500 orders
  a year (risk-menu row). 1: nothing.
- **Evidence:** ls-trend-1 #83: crash gains of real trend funds need shorts and a wide universe
  (93-118% of crash gains from shorts). ls-trend-2 #89: `tsmom12` plus the wide long-short book at
  1x: Sharpe 0.97 vs 1.21 (2007-2025, p 0.89, fails), but crash windows 2008 / 2020Q1 / 2022
  +8.9 / +2.2 / +2.0% vs -1.6 / -14.1 / -12.9%: a risk choice, not an edge. short-sleeve #99:
  narrow short sleeves fail. risk-menu #101: the equal-risk blend is the only row that gained in
  all three crash windows.
- **Recommended default: option 1, revisit after C2.** Reason: it is a risk choice (crash gains
  for Sharpe), so it belongs with C2, and it is the biggest design change on the list.
- **Unblocks:** closes O6 for now.

## C. The risk choice for the paper book

Today the live runner trades 11 books with fake money, among them `tsmom12` and the three risk
presets Careful, Middle and Bold side by side (DECISIONS 2026-11-12: "fake money, so no need to
pick one yet ... the pick only matters for graduation"). The items below build on that.

### C1. `tsmom12`: a risk choice, not an edge?

- **Question:** read the live rule as a drawdown/risk choice (crash insurance with a price), not
  as a proven edge over holding the same six assets?
- **Options:** (1) yes; (2) no, keep treating it as a candidate edge.
- **What it changes:** wording only (SUMMARY, the weekly page), and how the paper record is
  read at graduation: as a description of risk, not as proof of skill. No code.
- **Evidence:**
  - Edge: dsr-1 #74: `tsmom12` beats zero, but its lead over equal weight (+0.17, p 0.08) fails
    even uncorrected; deflated Sharpe 0.48 counting the 8 baselines it was picked from.
    survey-5 #78 and review-2 s.4a (recomputed): after 2009 it earned what holding earned
    (2010-2025 weekly Sharpe 1.36 vs 1.34); its lead is all from before 2010. No forward test
    settles "rule vs holding" in useful time (survey-5: ~107 years).
  - Insurance (with review-2's corrections, s.2): in **21 US market falls** of 25% or more since
    1927 it lost less than holding in **20** (50 episodes when industry-only falls are added); it
    avoided **0.50** of each fall against **0.27** for the same exposure at random dates (#87).
    "Cheaper than holding less" holds in direction everywhere but is shown statistically only
    for 1927-1961 and developed-market price indices, **not since 2002** (p 0.19). Price: about
    2 points of growth a year behind holding since 2002; fails in falls of three months or less
    (#90, #94, #96, #103).
- **Recommended default: option 1.** Reason: both the edge test and the live-fund evidence say
  "same as holding, smaller losses in long bear markets", and review-2 found those claims hold.
- **Unblocks:** frames C2-C4 and B7 as risk preferences; closes O8.

### C2. The risk level for the paper book

Merges three old entries that are one decision: "pick your risk level from the risk menu"
(#101, #105, #110), "a smaller worst loss simply by holding `tsmom12` at a smaller size"
(#86, #77, #80, #85) and the own-vol dial (#98, #110).

- **Question:** which risk dial(s) should the paper book run?
- **Options:**
  1. Keep the current set (presets side by side), no pick.
  2. Add a fixed smaller size: `tsmom12` at about 70% invested, the rest in T-bill cash (no new
     rule).
  3. Add own-vol targeting of `tsmom12` (share = min(1, k / recent volatility), k re-solved
     monthly from known data), target 70%.
  4. Pick one level now as "the" book for graduation.
- **Numbers (2007-2025, T-bill cash, risk-menu #101 with review-2 s.3b's corrections):**

  | Dial | Growth a year | Worst loss | Worst 12 months |
  |---|---:|---:|---:|
  | `tsmom12` at a fixed 70% | 17.6% | 24.6% | -20.6% |
  | Own-vol target "70%", no look-ahead (realised share **0.61**) | 13.8% | 15.7% | -7.6% |
  | Hold the six | 27.4% | 47% | (2022: -36.5%) |

  The trade-off for own-vol vs the fixed 70% is **3.8 points of growth a year for 8.9 points
  less worst loss**, not the 1.7 for 6 points the menu table and SUMMARY still quote (those are
  look-ahead figures; review-2 s.3b, being fixed by lane `fix-2`). Per unit of average share,
  own-vol's worst loss is still smaller (26 vs 35). Sharpe: no row is separable from the best
  (SE about 0.24 for one Sharpe; paired SE about 0.1; review-2 s.3c-d). Over 1994-2025 the
  ranking by worst loss holds (risk-menu-2 #105, tau 1.00); time under water depends on the
  window. The live preset Middle (trend rule, 10% per coin) already gives a smaller fixed book:
  worst drop 23% on 2003-2025 (`research/risk-map.md`).
- **What each changes:** 1: nothing. 2: one more live strategy (a try, N +1); little new
  information next to Middle. 3: one more live strategy plus a **monthly share reset in the
  runner** (new runner code, a lane's job). 4: graduation is judged on one book; the others stay
  as yardsticks or stop.
- **Evidence:** `research/risk-menu.md` (branch `risk-menu-3`, #101/#105/#110),
  `research/results/risk-menu-3.md`, vol-timing #98, rp-1 #86, eu-6..8 #77 #80 #85, review-2 s.3.
- **Recommended default: options 1 + 3** (keep the presets; add one own-vol book at a 70% target,
  in the no-look-ahead form risk-menu-3 names as the one to use). Reason: consistent with the
  2026-11-12 "no pick needed with fake money"; Middle already covers a smaller fixed size; own-vol
  is the menu's best-looking dial and the only one without a forward record. It is a risk level,
  not an edge.
- **Unblocks:** closes O2 and O5; lane queue item 5 (forward run of the chosen dial); a lane can
  build the monthly reset; B7 can be revisited with the risk level known.

### C3. Coin `stop-0.25` as a rule?

- **Question:** open a rule PR for a weekly 25% stop on the coin slots of `tsmom12`?
- **Options:** (1) no; treat coin size as the risk budget (the presets already cap coins at 5% or
  10% per coin); (2) yes, as a stated risk preference; (3) yes, daily-checked.
- **What each changes:** 2 or 3: a rule change in a live book (a new try). 1: nothing.
- **Evidence:** coin-cap-2 #53: shallower worst loss in 15 of 21 coin-crash episodes (p 0.039),
  short of the family bar (p < 0.0077 with all coin-cap picks counted); weak on BTC. coin-cap-3
  #56: a daily stop adds return via cheaper re-entries, not shallower losses, and most of it goes
  at double costs. coin-cap-4 #69: no candidate meets the bar; verdict page
  `research/coin-cap-verdict.md`: coin-years worst loss 36.5% -> 17.7% for about 2 points a year
  of growth. stop-reentry #82: 13 of 21 (needs 17). cointop-1 #40 and coin-cap #49: "a smaller
  coin position, not a better rule". combo-1 #70: the stop is the same bet as `trend-vol`,
  `inverse-vol` and 60/40. Forward test: 26 years (B2).
- **Recommended default: option 1.** Reason: no form met its bar, and a smaller coin share does
  the same job without a new rule; the presets already offer it.
- **Unblocks:** closes O14; the coin line stays parked.

### C4. A euro-fund paper book, and the rebalance band

Merges eu-1 (#59, a euro-fund copy of the live six), eu-5 (#73, the 5/25 band) and the older
optional trend-tune note (#34, a 2.5-5% band).

- **Question:** add a paper book of the live six in euro UCITS funds (the form a euro investor
  with a small portfolio can actually buy), with or without eu-5's 5/25 band; and should the
  live US runner's 1% band change?
- **Options:** (1) not now; keep the US runner's 1% band; (2) add the euro book with the 1% band;
  (3) add it with the 5/25 band; (4) also widen the US runner's band.
- **What each changes:** 2 or 3: a new live book (a try) and euro fund prices in the runner. 4:
  changes every live strategy's trading and is a new try for each (DECISIONS 2026-11-12: the 1%
  band is the only damping); the live record is days old, so it would restart comparability.
- **Evidence:** eu-1 #59: `tsmom12` keeps its character in EUR (Sharpe 1.44 vs 1.37 US twin, max
  drawdown 31% vs 36.5%, 2012-2025). eu-5 #73: the 5/25 band (top up only when more than 25% off
  target) cuts orders of the coin-free euro book from 30.1 to 21.1 a year at the same rule; holds
  on the coin book and the US six; trend-tune #34: a 2.5-5% band gave the same Sharpe with 15-25%
  less trading. eu-6 #77: for a small coin-free euro book trend is crash insurance only (Sharpe
  0.62 vs 0.78 holding the seven funds, gaps within noise; worst loss 13.6% vs 19.8%; best in all
  6 crash windows; but 58 vs 31 months under water and about 21 vs 2 orders a year). eu-8 #85:
  euro cash interest changes none of that; eu line closed (its row choice is a preference call,
  `research/eu-8.md` s.3).
- **Recommended default: option 1; revisit after C2.** Reason: the euro work is done and its
  answer is a preference (insurance vs fewer orders); a euro book would copy whichever dial C2
  picks, and changing the live band now would reset a days-old record.
- **Unblocks:** closes O10 and O13 for now.

## D. Small items

| Id | Item | Recommended default | Why |
|---|---|---|---|
| D1 | Daily runs fire at 02:00-04:40 UTC, not 22:30 (GitHub delays scheduled jobs). No look-ahead, but crypto orders fill about 22 h after the decision while backtests assume about 1.5 h (health-1 #27). Accept or move the schedule? | Accept and record it in DECISIONS; compare live with backtest only with this gap in mind | Moving the cron does not stop GitHub's delay; a second crypto-only run after 00:00 UTC is already in BACKLOG |
| D2 | Should the paper broker be able to fill at the close (two wide-1 effects were worth more at the close)? | No | Fills at the next open are a core rule (DESIGN); neither effect held up: the bond-auction dip was not confirmed (wide-1 #33) and the month-end bond rally did not replicate on clean data (#45) |
| D3 | usd-1 (#39): an optional robustness check needs a data API key | No | It cannot change the verdict; the project stays keyless |
| D4 | evo-1 (#44) would need about 24 CPU-hours | No decision needed | The evo line is closed (evo-2 #58) |
| D5 | month-end-bonds: spend a held-out year on it? | Already answered: no | #45's card says not to |
| D6 | `next-steps.md` on `main` is stale (lists merged PR #5 as waiting) | No decision needed | Whoever lands the next PR to `main` can drop the line |
| D7 | G2 tops up only to within the 1% band (integrate-1) | No decision needed | Rule working as written (A1 note) |

## How this brief was made

- Read the "For the owner" list and lane queue in `next-steps.md` (branch `summary-1`),
  `research/pr-map.md` (#113), `docs/integrate-1.md` (#115), `docs/research-archive-1.md` (#118),
  `research/reviews/review-2.md` (#119), `research/SUMMARY.md`, `research/risk-menu.md`
  (branch `risk-menu-3`), `docs/forward-registry.md` (branch `forward-1`), `research/wide-8.md`,
  #61's PR body, and `docs/DECISIONS.md` / `docs/VISION.md` on `main`.
- Deduplicated: #61 (three entries) -> A2; integrate-1's and pr-map's landing entries -> A1, A4,
  A5; register-1 + register-2 -> B1; wide-8's two questions -> B3 and B5; risk menu + smaller
  size + own-vol dial -> C2; coin-cap-2/3 and coin-cap-4 -> C3; eu-1 + eu-5 + trend-tune band ->
  C4; survey-5 + dsr-1 -> C1. pr-map's O1-O18 map as: O1 B6, O2 C2, O3 B1, O4 B3+B5, O5 C2,
  O6 B7, O7 B1, O8 C1, O9 A2, O10 C4, O11 B2, O12 B4, O13 C4, O14 C3, O15 D1, O16 A1+C4, O17 D2,
  O18 D3.
- Every number is quoted from the files above; where review-2 corrected one, the corrected
  number is used. The defaults are this lane's reading of the evidence; none is settled until the
  owner says so.
