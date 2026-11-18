# eu-2: `tsmom12` for a Dutch retail account: per-order fees, book size, currency hedge

Lane `eu-2` (DEEPER), night of 2026-11-18. Research only, fake money, train period only.
Branch `eu-2` from `eu-1`. Card: `cards/eu-2.md` (two amendments to the eu-1 card, each pushed
before its numbers). Tables: `results/eu-2-fees.md`, `results/eu-2-hedge.md`, data
`results/eu-2-data.md`.

**Why.** eu-1 showed the house rule keeps its character on European UCITS funds in euros, but
charged the Dutch broker as a percentage, and found the coin-free book trailing equal weight by
0.21 Sharpe in EUR (0.04 in USD), half of it currency. Two failure modes for a real Dutch
account: (1) real brokers charge a fixed amount per order, which bites small books; (2) the
dollar in an unhedged US equity fund changes what the trend filter sees.

## 1. Fixed per-order fees by book size (amendment 1)

**Fees (public pages, read 2026-11-18).** DEGIRO NL (`degiro.nl/tarieven`, "Peildatum
01.10.2025"): ETF core selection EUR 0 commission + EUR 1 handling fee per order; other ETFs
EUR 2 + EUR 1 = EUR 3; EUR 2.50 a year per exchange outside Euronext Amsterdam/Brussels (Xetra
here). Trade Republic (own page did not load; curvo.eu, 2026-09-18): EUR 1 per order when it is
the counterparty, EUR 2 per order routed to an exchange (since July 2026). Schedules: `dg1`
(EUR 1 + 2.50/yr), `tr2` (EUR 2), `dg3` (EUR 3 + 2.50/yr), and `slip` (no fee) as reference;
ETF slippage 0.05% a side in all; coins 0.25% + 0.05% (a Dutch exchange's percentage fee).

**Model.** A constant book of EUR 5k, 25k or 100k: every ETF order costs fee / book of equity
(the owner skims gains or tops up losses). The gym is untouched; `lib/eu2.py` wraps its order
step in-process and debits the fee after each batch of fills (with fee 0 it reproduces the gym
exactly; checked on every run of the script). The yearly fee is debited on the first order step
of each calendar year (the card said "first order day"; same amount, a day or two earlier).
86 rows in `tries.md`.

**Results (window W, 2012-2025; fee loss = `tsmom12`'s Sharpe lost against `slip`):**

| Book | Schedule | Break-even book, 1% band | Break-even, 5% band | Fee loss at 5k, 1% / 5% band | Fixed fees/yr at 5k, 1% band |
|---|---|---|---|---|---:|
| eu6 (with coins) | DEGIRO core EUR 1 | <= 5k | <= 5k | 0.04 / 0.02 | 0.9% |
| eu6 | Trade Republic EUR 2 | <= 5k | <= 5k | 0.08 / 0.04 | 1.6% |
| eu6 | DEGIRO other EUR 3 | ~6k | <= 5k | 0.12 / 0.05 | 2.5% |
| euw (no coins) | DEGIRO core EUR 1 | ~6k | <= 5k | 0.11 / 0.07 | 0.7% |
| euw | Trade Republic EUR 2 | ~10k | ~6k | 0.21 / 0.13 | 1.2% |
| euw | DEGIRO other EUR 3 | ~16k | ~10k | 0.32 / 0.19 | 1.9% |

Break-even = smallest book where the fee loss is at most 0.10 Sharpe (the card's line),
interpolated in 1/size. At EUR 25k every schedule costs at most 0.07 Sharpe, at EUR 100k at most
0.02: there the fixed fee is noise.

- **The coin book barely notices.** At 20% vol and 30% a year, even EUR 3 orders on EUR 5k
  (2.5% of the book a year with the 1% band) cost 0.12 Sharpe; `tsmom12` keeps its lead over
  equal weight (+0.08 vs +0.07 at no fee).
- **The coin-free book is where it hurts.** At 6% vol and ~3.5% a year, EUR 3 orders on EUR 5k
  eat 1.9% of the book a year: Sharpe 0.62 -> 0.29, CAGR 3.5% -> 1.6%, max drawdown 13% -> 21.5%,
  and the gap to equal weight widens from -0.15 to -0.36. Below about EUR 10-16k (EUR 3 orders)
  or EUR 6k (EUR 1 orders) the rule is not worth running on this book.

**The 5% band (the mitigation fixed in advance).** By the card's test it **does not pass** on
either book, for two different reasons:

- `eu6`: it cuts ETF orders from 42 to 11 a year (most orders on this book are top-ups forced by
  coin swings) and halves the fee loss at 5k and 25k (at 100k both losses round to 0.00-0.01,
  so "halves" fails there on rounding). But it also changes the rule: at no fee it lifts Sharpe
  by +0.06 (1.45 -> 1.51) and cuts max drawdown by 3.1 points (31.0% -> 27.9%), beyond the card's
  0.05 / 2-point limit for "same character". The change runs in the owner's favour on this
  sample (less trimming of winning coins), but it is a different rule, not a free fix; equal
  weight gains the same way (1.38 -> 1.46).
- `euw`: it cuts orders only from 30 to 21 a year: most orders here are the signal's own
  entries and exits (about 1.5 round trips per slot a year), which no band can skip. Fee loss
  falls by about 40%, not half (EUR 3 on 5k: 0.32 -> 0.19). Character at no fee is kept (Sharpe
  -0.01, drawdown +1.9 points).
- The 2.5% band (robustness) sits in between (eu6 17 orders/yr, euw 22).

What would help the coin-free book is fewer signal flips (e.g. monthly decisions) or fewer,
larger slots; neither was tested here (a new card).

## 2. Currency hedge (amendment 2)

Pending: runs after amendment 2 (pushed before any number).

## 3. Hedged lines: data

Yahoo's public chart API, EUR lines, raw responses under `<cache root>/eu-2/raw-<date>/`
(cache root from the git-ignored `research/macro.local.json`), read as data by
`uv run python -I research/lib/eu2_data.py build`; nothing downloaded is committed.

- **IUSE**, iShares S&P 500 EUR Hedged (Acc): the London EUR line (`IUSE.L`) from 2010-09-30 is
  used, so the line has a year of bars before W starts. The same fund on Xetra (IBCF, from
  2011-03-24) tracks it with a daily difference sd of 0.14%; IUSE.AS is not on Yahoo.
- **XAD1**, Xtrackers Physical Gold EUR Hedged ETC (Xetra), from 2010-06-15.
- NQSE (Nasdaq 100 EUR Hedged) starts 2018-09: too late for W.

No stale runs or bad prints beyond thin early volume (50-114 zero-volume bars, mostly the first
years). Calendar-year returns (`results/eu-2-data.md`): IUSE minus SPY in USD averages **-2.5%
a year** over 2012-2025, between +1.3% (2013) and -5.5% (2012). That is the hedge's cost: the
USD-EUR short-rate gap (not measured here; roughly zero in 2012-15, 1-2.7% in 2016-19 and
2022-25) plus the fund's costs (0.20% fee, a bit of withholding, hedge friction) and timing
noise between the London and New York closes (2012's -5.5% is mostly that: rates were level). IUSE minus SXR8 (hedged minus unhedged in EUR) averages -3.1% a year
and swings from -16% (2014, the dollar rose) to +12% (2017, the dollar fell): the currency bet
the hedge removes.

Rerun:

```sh
uv run python -I research/lib/eu2_data.py fetch
uv run python -I research/lib/eu2_data.py build
uv run python -I research/lib/eu2_data.py check
uv run --with numpy python research/lib/eu2.py fees
uv run --with numpy python research/lib/eu2.py hedge
```

## Variants counted

Amendment 1: 86 rows, amendment 2: 10 rows, all `robustness` or `baseline` (idea `eu-2`).
Disclosure: before the full amendment-1 run, one plumbing run with logging off on 2023-11 ..
2025-11 (`DRY=1`) was seen; its rows were not logged and are superseded by the full run.

## Verdict

Pending section 2.

Held-out year: unspent (nothing was selected).
