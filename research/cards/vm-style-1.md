# vm-style-1: does market-volatility management (DeMiguel, Martin-Utrera and Uppal 2024) make `xs-century-1`'s style book add to `tsmom12`? (card)

Lane `vm-style-1`, written 2026-11-25 (night) **before any return of a managed sleeve, of a
mean-variance portfolio or of the market-volatility series was computed**. Branch `vm-style-1`
from `origin/main` (`fe627bb`). Research only: fake money, files already in the data cache
(read-only), no change to the gym, the daily runner or the live strategies. Nothing after
2025-10-31 is parsed (held-out year untouched). Shorts are research-only (owner decision B7) and
Ken French portfolios are not tradable in the gym, so **the verdict is informational**: a pass
would not be a pick.

What was seen before this card: `xs-century-1` (#170: write-up, card, code, its published
numbers: net IR +0.31, z 2.75; gross IR +0.88; at UMD 0.34%/mo z 4.44; sleeve-level net IRs),
`survey-7b.md` (branch `survey-7b`, item V1 and its card sketch) and the paper itself (below,
read from the open-access published PDF). The Ken French daily files' headers were looked at;
no daily return, no realised volatility and no new sleeve number was.

## The paper and its method (as published, verified from the text)

DeMiguel, Martin-Utrera and Uppal, "A Multifactor Perspective on Volatility-Managed Portfolios",
Journal of Finance 79(6), 2024, 3859-3891 (DMU). Read from the LBS Research Online copy of the
published article. What the text says (section and equation numbers are the paper's):

- **Conditioning variable (I.B, eq. 3):** realised **market volatility** sigma_t, "the sample
  volatility of the daily market returns in month t". Not variance: they use volatility "because
  ... using volatility can help reduce the transaction costs" (I.B). (The brief said "variance";
  the paper's own text decides, variance is a robustness row.)
- **Factor weights (eq. 2-4):** theta_k,t = a_k + b_k / sigma_t for every factor k; portfolio
  return r_p,t+1 = sum_k r_k,t+1 (a_k + b_k / sigma_t). Equivalently, a mean-variance portfolio
  on the 2K "extended" factors r_k and r_k / sigma_t (eq. 5).
- **Estimation (eq. 6):** eta = (a, b) maximises mu_ext' eta - TC(eta) - (gamma / 2) eta'
  Sigma_ext eta subject to **eta >= 0** (all a_k, b_k non-negative), with the sample mean and
  covariance of the extended returns over the estimation window and TC the window's average
  transaction cost of the strategy. No weights-sum constraint (zero-cost factors).
  **gamma = 5** (Table I note).
- **Out of sample (I.A, II.A):** expanding window, first window **120 months**, the return is
  scored in the month after each window (re-estimated every month).
- **Comparator in the paper (II.B):** the unconditional mean-variance portfolio UMV = the same
  problem with b_k = 0. Headline (Table II): out-of-sample net Sharpe 1.062 (CMV) vs 0.940 (UMV),
  +13%, p 0.006; alpha t 3.6 (Newey-West, 1 lag). Sample 1967-2020, out of sample 1977-01 ..
  2020-12. Nine US equity factors (MKT, SMB, HML, RMW, CMA, UMD, ROE, IA, BAB).
- **Costs (I.C):** stock-level half-spreads (Abdi-Ranaldo), trades netted across factors
  ("trading diversification"). Without netting, four of nine managed factors have a negative
  net mean (Table I, panel D).
- **Own-volatility variant:** DMU say (I.B, Internet Appendix X) timing each factor by its own
  volatility does even better. So the own-vol twin below is not a straw man; it is the paper's
  own alternative.

The paper's out-of-sample window 1977-2020 is **in-sample for the method** (the method was chosen
and published on it). The **out-of-paper sample** is everything else this book has: 1939 ..
1976-12 (before the paper's data) and 2021-01 .. 2025-10 (after it).

## The test (one configuration, fixed now)

### Sleeves: `xs-century-1`'s, unchanged

The eight sleeves of `xs-century-1`'s primary book, built by its code (`research/lib/xs_century_run.py`
`build`, primary costs; nothing retuned): US-value (HML), US-mom (UMD), bond value, bond
momentum, bond carry, FX value, FX momentum, FX carry. Each is already scaled to 10% a year ex
ante on 36 months and charged `xs-century-1`'s costs (HML 0.05%/mo, UMD 0.65%/mo, borrow 0.5%/yr,
bonds/FX 5 bps per unit of turnover). These eight net return series are DMU's "factors" r_k.
The market sleeve MKT is not added (it is not in the book; `tsmom12` is the market-side
comparator).

### DMU's conditional mean-variance portfolio (CMV, the primary)

- sigma_t: SD (ddof 1) of the daily US market total returns (Ken French daily `Mkt-RF + RF`)
  in calendar month t, no annualising. Used for the return of month t+1 (known at the end of t).
- theta_k,t+1 = a_k + b_k / sigma_t; CMV return of month t+1 = sum_k theta_k,t+1 r_k,t+1 minus the
  scaling-trade cost (below).
- At each month t+1, (a, b) is re-estimated on the window of months u <= t (all data up to the
  end of t): maximise (mu_ext - c)' eta - (5 / 2) eta' Sigma_ext eta, eta >= 0, with mu_ext and
  Sigma_ext (ddof 1) the sample mean and covariance of (r_k,u, r_k,u / sigma_u-1) over the window,
  and c the window's average scaling-trade cost per unit of eta (with eta >= 0 the cost is linear
  in b: c for a_k is 0, for b_k it is mean_u kappa_k G_k,u |1/sigma_u-1 - 1/sigma_u-2|). Solved
  exactly as a non-negative least-squares problem (Cholesky of Sigma_ext + 1e-12 I).
- **Eligibility and window (unequal histories; the paper has none):** a sleeve enters at month
  t+1 when it has at least 120 monthly returns up to t and a return in t+1. The estimation window
  is every month up to t in which all entered sleeves have a return (the paper's single common
  window; when a sleeve class enters, the window starts at that class's first month). The first
  out-of-sample month is the 121st month of the first sleeve pair (about 1939).
- No cap on leverage (the paper's main case has none).

### Costs of the scaling (charged, sleeve level)

DMU's netting of trades across factors needs stock holdings (not keyless), so costs are charged
per sleeve, without netting: harsher than the paper (it is their Table I panel D setting). Every
month and every sleeve: kappa_k x G_k,t x |theta_k,t - theta_k,t-1| (theta 0 when not held), G_k,t =
2 s_k,t (the sleeve's gross notional per unit of theta: long 1 + short 1, times its vol scale).
The sleeve's own running costs are already in r_k (approximately scaled by theta). Drift of theta
inside the month is ignored (stated).

- kappa for bonds and FX: **5 bps** per unit traded (`xs-century-1`'s rate).
- kappa for US stocks (HML, UMD): **0.50%** per unit traded one way. Set now, not from returns:
  a round middle of the one-way costs of large NYSE stocks (half-spread plus commission) that
  Jones (2002) reports, as recalled here and not re-read: around 1% before 1950, around 0.5% in
  the 1960s-70s, under 0.2% after 2000. Robustness rows take 0.25% and 1.0%.
- The same cost rule applies to every portfolio below (UMV and the twin re-estimate weights every
  month too, so they also trade).

### Controls (fixed now; each logged)

1. **UMV** (the paper's comparator): the same problem with b = 0 (weights a_k only), same window,
   same costs.
2. **Own-vol twin** (is it vol sizing in disguise?): theta_k,t+1 = a_k + b_k / sigma_k,t, each
   sleeve timed by its own realised volatility instead of the market's. sigma_k,t for HML and
   UMD: SD of the daily HML / `Mom` factor returns in month t (Ken French daily files). For the
   bond and FX sleeves no daily data exist: SD (ddof 1) of the sleeve's last 6 monthly raw
   (unscaled) returns ending t (the paper's Internet Appendix II uses six-month windows; a
   stated deviation). Same estimator, costs and window.
3. **The unmanaged book** (`xs-century-1`'s equal-weight book, unchanged) on the same months:
   the baseline the brief names.

## Statistic and bar

- The `xs-century-1` comparator, unchanged: `tsmom12`'s rule on the US market (Ken French,
  monthly, in when the 12-month total return is positive, else bills), scored above bills.
- OLS B_t = a + b T_t + e_t over the sample months; IR = a / sd(e) x sqrt(12); **z = a / SE(a)**,
  SE the larger of Newey-West (lag floor(4 (n/100)^(2/9))) and a 12-month circular block
  bootstrap (2,000 draws, seed 20261124): `xs_century.score`, unchanged.
- **Samples.** Full: every out-of-sample CMV month, first month (about 1939-01) .. 2025-10.
  **Out-of-paper (judged): the full sample minus 1977-01 .. 2020-12** (about 1939-1976 plus
  2021-01..2025-10, about 43 years). In-paper 1977-2020: described, never decides.
- **Bar: z >= 4.70** (BAR.md, rows through 2026-11-24 23:32: N 1,099, N_eff 504 at measured rho
  0.54, DSR 0.95). The ONC end, z >= 3.26, is reported beside it. Not lowered for the
  different comparator or for being a family member selected after `xs-century-1`'s near miss
  (it is the next try in that family and is counted as such).

## Verdict rules (fixed now)

- **Pass (informational)**: all of (1) out-of-paper z >= 4.70, (2) full-sample z >= 4.70, (3)
  out-of-paper CMV net Sharpe > UMV net Sharpe, (4) out-of-paper CMV net Sharpe > own-vol twin net
  Sharpe. Even then not a pick (B7, French portfolios not tradable): a case for the lead to weigh
  and a candidate for one held-out test.
- **Near**: out-of-paper z in [3.26, 4.70) with (3).
- **Fail**: anything else.
- **Kill rules (family `vm-style`, fixed now):**
  - K1: out-of-paper CMV net Sharpe <= UMV net Sharpe: DMU's conditioning does not replicate
    outside its sample on this book; market-volatility management of the style book is dead.
  - K2: out-of-paper CMV alpha z below the unmanaged book's alpha z on the same months:
    management (with its optimiser) hurts; dead.
  - K3: own-vol twin's out-of-paper net Sharpe >= CMV's: whatever works is own-volatility sizing;
    it belongs to the own-vol line, not to a new family.
- Robustness rows describe; none can turn a fail into a pass or a pass into a fail.

## Robustness rows (run after the primary, each logged; none decides)

- R1 gross: sleeves gross (`xs-century-1` R1) and no scaling-trade cost.
- R2 UMD at 0.34%/mo (`xs-century-1` R2's cheaper published momentum cost).
- R3a / R3b: kappa for US stocks 0.25% / 1.0%.
- R4 market **variance** (b_k / sigma_t^2) instead of volatility (Moreira-Muir's form; the brief's
  wording).
- Sub-periods (described): 1939-1976, 1977-2020 (the paper's), 2021-2025: CMV minus UMV net
  Sharpe and CMV's alpha vs the comparator.

## Outputs

- `research/lib/vm_style.py` (pure functions: market and own realised volatility, the DMU
  estimator, the out-of-sample walk with costs; tests `tests/test_vm_style.py`, offline, synthetic)
  and `research/lib/vm_style_run.py` (reads the cache via `xs_century_run`, runs once, writes
  `research/results/vm-style-1.md`, statistics only).
- Rows in `research/tries.md`, idea `vm-style-1`: CMV as `variant`; UMV and the own-vol twin as
  `variant` too (they are configurations that could be selected); the unmanaged book on the same
  months and the comparator as `baseline`; R1-R4 and the sample splits as `robustness`. Sharpe:
  monthly excess returns x sqrt(12) (stated in the Variant cell). No `ledger/tries.jsonl` line:
  the gym cannot hold shorts (`xs-century-1`'s precedent).
- `research/vm-style-1.md`: the answer on one screen; one line in `research/ideas.md`.
