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
3. **[A2](#a2-cash-interest-pr-61) Cash interest (#61): full T-bill rate; new research scored
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

(filling in)

## C. The risk choice for the paper book

(filling in)

## D. Small items

(filling in)
