# breadth-book-1: does a broader long-only universe raise `tsmom12`'s Sharpe?

Research lane `breadth-book-1`, 2026-11-24. Card [`cards/breadth-book-1.md`](cards/breadth-book-1.md)
(2e97e89, pushed before any number), script `lib/bbook1.py` + `lib/bbook1_core.py` and
look-ahead tests `tests/test_bbook1.py` (3fe0aa3, pushed before the run), one logged run.
Tables: [`results/breadth-book-1.md`](results/breadth-book-1.md). Train only; the held-out year
was not loaded. Research only: the live runner and the paper books are untouched.

## In plain words

**No. On a mechanically chosen universe, more markets made `tsmom12` worse, not better.**
(Review note: the pool is 33 ETFs, about 70% equity sectors and countries, not a diversified
futures set. The fall of the six-plus-ETFs books is mainly coin dilution plus the hindsight in
the live six; the ETF-only books are the breadth test, and among the mechanical sets alone
Sharpe still falls, 0.61 with 6 ETFs to 0.37 with all 33.)
Adding ETFs to the six live assets lowered the Sharpe ratio (return per unit of risk) at every
size, from 1.19 to 0.96 (12 assets), 0.83 (20) and 0.65 (all 35), above T-bills, 2008-2025.
The worst loss fell (37.6% to 21-25%), but only because each extra slot shrinks the coins'
share: the book takes less risk and earns much less (growth 23.5% a year down to 6.6%). Even
the clean breadth test, without coins, went the wrong way: the four live ETFs scored 0.82, the
mechanical ETF sets 0.61 (6 ETFs), 0.40 (12), 0.34 (20) and 0.37 (all 33). More coins did not
help either: BTC+ETH 1.14 from 2020, the top 5 coins of 2019 0.88, the top 10 0.75.

**Why breadth did not pay here.** The theory needs *independent* markets with a trend premium
each. This pool gives neither: (1) the effective number of independent bets barely moves, from
3.1 for the six to 3.3-4.2 for 35-43 assets, because most of the added ETFs are US sectors and
country equity funds that move together (average correlation 0.11 for the six, 0.40 for all
35); (2) the added markets (emerging and foreign equity, the euro and pound, oil, broad
commodities, silver) mostly trended poorly for a long-only book in 2008-2025, while the live
six were picked in 2026 and hold this period's winners (QQQ, BTC, ETH). Real trend funds get
their breadth from futures across currencies, rates and commodities, long and short
(`ls-trend-1`): a long-only ETF list cannot copy that.

**For the backlog line "More universe: a few more liquid crypto (SOL, ...) and ETFs (IWM, EFA,
...)":** this run says don't, at least not for Sharpe. No set passes or comes close, so there is
no paper-book spec. Picking SOL, IWM or EFA by name today would be choosing with hindsight,
which is the very bias this card was built to avoid.

## Results (2008-01-02 .. 2025-11-09, Sharpe above T-bills; edge vs `six` with bootstrap SE)

| Set | N | Sharpe | Edge (SE, z) | Max DD | CAGR | N_eff (avg corr) | Eras ahead |
|---|---:|---:|---|---:|---:|---|---|
| `six` (`tsmom12`) | 6 | 1.19 | - | 37.6% | +23.5% | 3.1 (0.11) | - |
| `L-12` | 12 | 0.96 | -0.23 (0.09, -2.6) | 24.9% | +11.0% | 4.2 (0.21) | 0/4 |
| `L-20` | 20 | 0.83 | -0.35 (0.16, -2.3) | 20.6% | +8.0% | 4.2 (0.26) | 0/4 |
| `L-all` | 35 | 0.65 | -0.54 (0.20, -2.6) | 20.7% | +6.6% | 3.3 (0.40) | 0/4 |
| `four` (live ETFs) | 4 | 0.82 | -0.37 (0.25, -1.5) | 15.7% | +7.8% | 2.5 (0.13) | 0/4 |
| `E-6` / `E-12` / `E-20` / `E-all` vs `four` | 6-33 | 0.61 / 0.40 / 0.34 / 0.37 | -0.21 / -0.42 / -0.48 / -0.45 (z -2.4 to -2.9) | 10-18% | +3-5% | 3.0-3.7 | 0/4 each |

From 2020 (5.9 years; coin list = top 10 by 2019-12-31 market cap: BTC ETH XRP BCH LTC EOS BNB
BSV ADA XTZ, none died in the window):

| Set | N | Sharpe | Edge (SE, z) | Max DD |
|---|---:|---:|---|---:|
| `six` | 6 | 1.20 | - | 28.8% |
| `L-all` | 35 | 0.65 | -0.55 (0.28, -2.0) | 18.9% |
| `LC-all` (all ETFs + 10 coins) | 43 | 0.73 | -0.47 (0.21, -2.3) | 25.8% |
| `C-2` / `C-5` / `C-10` (coins only, vs `C-2`) | 2 / 5 / 10 | 1.14 / 0.88 / 0.75 | -0.26 (z -1.3) / -0.39 (z -1.8) | 57-63% |

The gym convention (cash earns 0, the `tries.md` rows) gives the same signs and similar sizes
(`L-all` -0.49, `E-all` vs `four` -0.45). The live runner's form of the rule (daily, slot capped
at 40% / volatility) gives the same answer: `L-all` 0.58 against 0.65, `LC-all` 0.85 against
`six`'s 1.24 in its own form.

## Verdict against the card

- **Pass bar** (BAR.md, N = 486: z >= 4.69 over `tsmom12`, Bonferroni p <= 1.0e-4): every set
  fails, and every edge is negative (z -1.3 to -3.1). Not a power problem: the edges have the
  wrong sign. **Comes close** (z >= 2): none. **Risk preference** (smaller worst loss with z
  between -1 and 2): none; the smaller losses come with Sharpe losses of z -2 to -2.6.
- The smaller worst losses of the `L-*` books are the same thing as a smaller coin slot, which
  the risk map already offers more cheaply (`risk-map.md`, the presets): lower risk, not better
  risk.
- Prior (card): low. Result: below the prior; breadth was neutral-to-negative even in the clean
  coin-free test.

Side note, not this card's question and not a selection: the live runner's vol-capped form on
the six scored above the bar's `tsmom12` on this window (1.32 vs 1.19, +0.13, SE 0.10, z 1.4;
from 2020 +0.05, z 0.4). That is the own-volatility sizing already reported as noise-sized in
`SUMMARY.md` (#110); it adds nothing new.

## Caveats

- The pool is the union of ETF lists earlier cards fixed for other questions (50 tickers; 33
  pass the 2006 rules). A full US-ETF census (all ~350 ETFs listed in 2006) was not built: it
  would need a symbol directory plus a few hundred downloads. It would add more of the same
  (sectors, countries, style funds), so it is unlikely to change the sign; untested.
- Survivorship: the pool lists ETFs that trade today. Membership and order use only 2006
  existence and dollar volume. ETFs that were liquid in 2006 and later closed are missing; that
  bias flatters the broad books, so it cannot explain their shortfall.
- The live six are a hindsight pick (bias against every broad set). `E-6`, the mechanical six
  ETFs (SPY TLT GLD EEM FXE QQQ), against the live four is the cleanest view of that: -0.21.
- Not decomposed per asset; "the added markets trended poorly" is the likely reading of the
  `E-*` rows, not a measured attribution.
- Coins other than BTC and ETH use Coin Metrics reference prices and the gym's Kraken fees;
  real alt-coin spreads are wider, which would only lower `C-5`, `C-10`, `LC-all` further.
- The coin window is short (5.9 years; SE 0.2-0.3).

## Disclosures

- The card's header says it was written "~19:45 UTC"; that is a slip. Its commit is 19:30 UTC,
  the script commit 19:35 UTC, the run rows 19:35 UTC, after both pushes.
- Before the logged run: `prep` printed the pool's 2006 dollar volumes, the order and the coin
  list (no returns); `smoke` ran three books on two three-month windows with logging off and
  printed only "ok" (plumbing check, tables discarded unread).
- Added beyond the card's table, as `robustness` rows: `L-all@2020` (the ETF part of `LC-all`
  on the coin window, to separate coins from ETFs) and the live-form `six` rows (the comparator
  for each live-form row). `L-all-vol` was not run: with every eligible ETF in, the volume order
  gives the same set (card).
- `harness.check_against_gym` (fast path = gym) and the live-form identity check against
  `ts_momentum.decide` passed inside the run.

**Logged:** 19 rows in `tries.md` (idea `breadth-book-1`): 4 baselines (`six@2008`,
`four@2008`, `C-2@2020`, `six@2020`), 10 variants (`E-6`, `E-12`, `E-20`, `E-all`, `L-12`,
`L-20`, `L-all` @2008; `C-5`, `C-10`, `LC-all` @2020), 5 robustness (live form x 4,
`L-all@2020`). Weekly returns in `register/returns/breadth-book-1.csv.gz`.

Reproduce: `uv run python -I research/lib/bbook1.py prep` then `... run` (needs the shared
cache via `research/macro.local.json`, the `ls-trend-1` raw Yahoo responses and the Coin
Metrics snapshot `2026-11-13`; `run` refuses a second logged run).
