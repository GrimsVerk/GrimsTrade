# xs-century-1: does a century-long long-short style book add to `tsmom12`? (card)

Lane `xs-century-1`, written 2026-11-24 (night) **before any return of the book, of any sleeve
or of the comparator was computed**. Branch `xs-century-1` from `origin/main` (`fac43c9`).
Research only: fake money, files already in the data cache (read-only), no change to the gym,
the daily runner or the live strategies. Nothing after 2025-10-31 is parsed (held-out year
untouched). Shorts are research-only (owner decision B7: the paper broker holds no shorts), and
Ken French portfolios are not tradable in the gym, so **the verdict is informational**: a pass
would not be a pick.

What was seen before this card: `power-map-1.md` (the IR bar), `alpha-form-1.md` (the alpha
statistic and its cautious SE rule), `data-long-3.md` and `pooled-2.md` (the long rates / FX /
commodity panel and its timing lags), `ls-trend-1/2.md` and `short-1.md` (long-short trend on
ETFs; shorts on coins), survey-6's numbers (paper Sharpe of value + momentum everywhere 1.59;
live long-short style premia 0.50 over 12 years). The French files' headers and the panel's
coverage table were looked at; no return of HML, UMD, a bond, a currency or a commodity was.

## Question

power-map-1 (PR #150, row C2): the only test where an honest pass is not absurd is a
long-short, multi-asset style book on about 100 years of data, scored in the **alpha form**
against `tsmom12` (does it add to `tsmom12`?), with a bar of **IR about 0.51 (50% power) to
0.60 (80% power)**. This lane runs exactly that one test.

## The book (one configuration, fixed now; parameters from the papers, nothing tuned)

Template: Asness, Moskowitz and Pedersen, "Value and Momentum Everywhere", JF 68(3) 2013
(AMP: signal definitions, rank weights); Koijen, Moskowitz, Pedersen and Vrugt, "Carry", JFE
127(2) 2018 (KMPV: carry definitions); Ilmanen, Israel, Moskowitz, Thapar and Lee, "How Do
Factor Premia Vary Over Time? A Century of Evidence", JOIM 19(4) 2021 (the century multi-asset
value / momentum / carry composite, each sleeve scaled to a volatility target, equal weight
across asset classes). Defensive (betting-against-beta) is left out: no keyless century data
for it in the cache.

### Asset classes and sleeves (primary book)

| Class | Assets (returns) | Value | Momentum | Carry | Lag (months of data a signal may not see) |
|---|---|---|---|---|---|
| US stock selection | Ken French monthly factors | **HML** (Fama-French 1993, as published) | **UMD** (`Mom`, Carhart 1997 / Jegadeesh-Titman, as published) | - | the factors are portfolios; no signal is computed here |
| Government bonds, country selection | 10: US 10y rebuilt from `GS10` (monthly average) minus the US bill (`us_short()`), and `GOV10-<cc>` for JP, GB, CH, CA, DE, AU, NZ, SE, NO (local excess over the local 3m rate, data-long-3's `panel()`) | AMP: 5-year change in the 10y yield, y(L) - y(L-60) (yield rose most = cheap = long) | AMP: compound excess return over the 11 months ending at min(t-2, L) | KMPV (term-spread approximation): y10(L) - y3m(L) | OECD inputs available at the start of m+3 (data-long-3): **L = t-3** |
| Currencies vs USD | 9: `FX-<cur>` (JPY, GBP, CHF, CAD, EUR, AUD, NZD, SEK, NOK; carry-inclusive excess, USD-funded) | AMP define it as the 5-year change in PPP; no CPI is cached, so **spot proxy** (a stated deviation, AMP's commodity form): log(mean spot over months L-65..L-54) - log(spot at L) | 11 months ending at L (= AMP's 12-1) | KMPV: i_f(L3) - i_us(L3) | spot **L = t-2** (H.10 weekly, DEM averaged); rates L3 = t-3 (OECD) |

FX starts in 1973-03 (floating; data-long-3's advice): no FX return or signal before 1973-03 is
used. A sleeve is live in month t when at least **4 assets** have both the signal and the
month-t return.

### Weights

1. **Rank weights (AMP eq. 1).** For a constructed sleeve: w_i = c (rank_i - mean rank), c such
   that the long side sums to 1 and the short side to -1 (gross 2, dollar-neutral). Ties: mean
   rank.
2. **Volatility scaling (Ilmanen et al. 2021: a constant volatility target).** Each sleeve's raw
   return series (rank-weighted book, or HML / UMD as published) is scaled to **10% a year**
   ex ante: s_t = 10% / (SD of the sleeve's raw gross monthly returns over the last 36 months
   ending t-1, x sqrt(12)); at least 24 months of raw history needed (until 36 exist, all
   available months are used); **s capped at 4** (a guard against tiny early volatility, fixed
   now). Sleeve return = s_t x (raw net return).
3. **Book.** Equal weight across the classes live in month t; inside a class equal weight
   across its live sleeves. Book return = sum of class weight x mean of its sleeves. No book-
   level rescaling (the IR is scale-free).

### Costs (primary; all per $ of notional, deducted every month)

- **HML: 0.05% a month; UMD: 0.65% a month** (Novy-Marx and Velikov, "A Taxonomy of Anomalies
  and Their Trading Costs", RFS 29(1) 2016, Table 3: value-weighted decile value and momentum
  strategies, 1963-2013, columns "T-costs"; read here from the NBER w20721 text). Applied to
  the scaled notional: cost_t = s_t x c. Earlier decades were dearer (Jones 2002) and later
  ones cheaper; one number for all is a stated simplification. Short-borrow fee on the stock
  sleeves: **0.5% a year** on the short notional (s_t x 1).
- Bonds and currencies (futures / forwards stand-ins): **5 bps per unit of one-way turnover**
  (sum |w_t - w_{t-1}| of the scaled weights), above pooled-2's 2 / 3 bps because the panel
  starts in the 1950s-70s. No borrow (excess returns are already financed).
- Rescaling turnover of the US stock sleeves (changes in s_t) is not charged (small, stated).

### Commodities (robustness only, not the primary book)

Commodity series are spot producer prices, not investable (data-long-3: month-end WTI spot beat
USO by 10 points a year, and the roll gap differs by commodity, so it does not cancel in a
cross-section). So they are **not** in the primary book. Robustness R4 adds a commodity class:
7 PPI series (grains, livestock, coal, natgas, crude, steel, primary nonferrous; no nested
ones), AMP value log(mean price L-65..L-54) - log(price L) and momentum (11 months ending at L),
**L = t-3** (PPI is a mid-month point price, public about the 16th of the next month), 10 bps
per unit of turnover, from 1926 where 4 series exist.

## Sample

Every month in which the book and the comparator both have a return, 1927-07 .. 2025-10 (the
first book month is set by the 24-month volatility history of HML, about 1928-07). About 97
years. Train data only.

## The comparator (`tsmom12` proxy, defined now)

`tsmom12` itself (six assets, 1994-2025) does not exist before 1994. The closest proxy that
exists for the whole century is **`tsmom12`'s own rule on the US stock market**: Ken French
`Mkt = Mkt-RF + RF` (total return, monthly), position p_t = 1 in month t when the compound
total return of months t-12..t-1 is > 0, else 0 (cash at the bill). That is trend-1926 /
insure-1's `tsmom12` on the market, at monthly instead of Friday decisions; the 40% volatility
cap of `tsmom12` is ignored (US market volatility above 40% is rare and brief), stated. It is
scored **above bills**: T_t = p_t x (Mkt_t - RF_t). The book is self-financing, so its return
is already an excess return (alpha-form-1's lesson: score above bills, or every cash-like slot
looks like alpha).

## Statistic and bar

- OLS over the sample months: B_t = a + b T_t + e_t. **IR = a / sd(e) x sqrt(12)**.
- **z = a / SE(a)**, SE the larger of (i) Newey-West (Bartlett), lag floor(4 (n/100)^(2/9)),
  and (ii) a circular block bootstrap of a (12-month blocks, 2,000 draws, seed 20261124). The
  larger SE decides (alpha-form-1's cautious rule).
- **Bar: z >= 4.70** (BAR.md, rows through 2026-11-24 20:01: 3,855 distinct tries, N_eff 500
  at measured rho 0.54, DSR 0.95). Not lowered for the different comparator (alpha-form-1). The
  ONC end, **z >= 3.29**, is reported beside it. In IR terms at about 97 years (power-map-1, k
  1.08): about **0.51 at 50% power, 0.60 at 80%**; reported next to the IR.
- Also reported (not deciding): the mix gain SR(best long-only mix of B and T) - SR(T); the
  correlation of B with T; the book's own Sharpe; gross (no cost) numbers; IR by sub-period.

## Verdict rules (fixed now)

- **Pass (informational)**: z >= 4.70 at primary costs **and** a > 0 in both halves,
  1927-07..1972-12 (US stocks only, then bonds) and 1973-01..2025-10 (multi-asset). Even then:
  not a pick (B7, French portfolios not tradable); it would say "a published style book adds
  to `tsmom12` over a century at the project bar", a case for the lead to weigh B7 and the
  comparator, and a candidate for one held-out test.
- **Near**: 3.29 <= z < 4.70.
- **Fail**: z < 3.29.
- Sub-periods, gross numbers and robustness rows describe; they cannot turn a fail into a pass
  or a pass into a fail (except the "both halves" rule above).

## Robustness rows (run after the primary, each logged; none decides)

- R1 gross (no costs, no borrow).
- R2 cost-mitigated momentum: UMD at 0.34% a month (Novy-Marx and Velikov 2016, Table 7:
  momentum with staggered partial rebalancing, a third of the book each month, "T-costs"
  column as read: the cheaper published version).
- R3 bonds / FX costs doubled (10 bps).
- R4 with the commodity class (above).
- R5 post-publication: 1994-01..2025-10 only (after Jegadeesh-Titman 1993 and Fama-French 1993).
- R6 comparator = the store's six-asset `tsmom12` (weekly returns, compounded to calendar
  months by the Friday's month), 1994-02..2025-10, above bills (the French RF).
- R7 book without the US stock class (bonds + FX only, 1960s-2025): does the non-equity part
  add on its own?

## Outputs

- `research/lib/xs_century.py` (pure functions: rank weights, vol scaling, alpha statistics;
  tests `tests/test_xs_century.py`, offline, synthetic data) and `research/lib/xs_century_run.py`
  (reads the cache, runs the book once, writes `research/results/xs-century-1.md` with
  statistics only: no prices, no return series, OECD/IMF-derived data not committed).
- Rows in `research/tries.md`: the primary as `variant` (idea `xs-century-1`), R1-R7 as
  `robustness`, the comparator as `baseline`. Sharpe there: monthly excess returns x sqrt(12)
  (stated in the Variant cell). No `ledger/tries.jsonl` line: the gym cannot hold shorts
  (ls-trend-2's precedent).
- `research/xs-century-1.md`: the answer on one screen; one line in `research/ideas.md`.
