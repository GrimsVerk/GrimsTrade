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

(filling in)

## B. Project rules

(filling in)

## C. The risk choice for the paper book

(filling in)

## D. Small items

(filling in)
