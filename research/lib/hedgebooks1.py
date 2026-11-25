"""hedge-books-1: Hedge (multiplicative weights) across the existing books (card
`research/cards/hedge-books-1.md`, committed before this script).

    uv run --with numpy python research/lib/hedgebooks1.py check   # rebuilds vs the store
    uv run --with numpy python research/lib/hedgebooks1.py run     # the one run (logs tries)
    DRY=1 ... run                                                  # last 200 days, no log

Hedge in the form of Cesa-Bianchi and Lugosi (2006), Theorem 2.2: loss in [0, 1]
l_{t,i} = 1 - x_{t,i} / max_j x_{t,j}, weights proportional to exp(-eta * cumulative loss),
eta = sqrt(8 ln K / T), T known from the calendar. Rounds end at the end of each Thursday (UTC);
weights from rounds 1..t are used from the Friday decision after round t's Thursday. The
combined target weights (sum of Hedge weight times each book's target weights) go through
`gym.simulate` as one account. Costs: the protocol's (25 + 5 bps crypto, 2 bps ETFs); the gym's
live costs as robustness. Train only: no bar after 2025-10-31.
"""

from __future__ import annotations

import bisect
import math
import os
import sys
from collections.abc import Callable, Mapping, Sequence
from concurrent.futures import ProcessPoolExecutor
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import harness  # noqa: E402  (puts src/ on the path)
import numpy as np  # noqa: E402
import stats  # noqa: E402

from grimstrade import gym, report, returnstore  # noqa: E402
from grimstrade.data import CRYPTO, ETF, Bar  # noqa: E402
from grimstrade.gym import Decision  # noqa: E402

IDEA = "hedge-books-1"
DRY = bool(os.environ.get("DRY"))
START = harness.TRAIN_START  # 1994-02-01
LAST = date(2025, 10, 31)  # last bar loaded and last decision (card: nothing after 2025-10-31)
THETA0 = date(1994, 2, 3)  # first Thursday: rounds end at the end of each Thursday
THETA_LAST = date(2025, 10, 30)
PROTO: dict[str, gym.Costs] = {
    CRYPTO: gym.Costs(fee=0.0025, slip=0.0005),
    ETF: gym.Costs(fee=0.0, slip=0.0002),
}
DRAWS = 2000
BLOCK = 20.0
SEED = 0
Z_BAR = 4.70  # BAR.md, N = 500 (2026-11-24 20:01)
SINCE = date(2003, 1, 1)
LATE = date(2022, 1, 1)

LIVE_BOOKS = [
    "buy_hold_btc", "buy_hold_spy", "sixty_forty", "equal_weight", "ts_momentum", "xs_momentum",
    "vol_target_spy", "risk_parity", "crypto_mean_reversion", "preset_careful", "preset_middle",
    "own_vol_70",
]  # fmt: skip
RESEARCH_BOOKS = ["tsmom12", "halving-alone", "where-vol", "stop-0.25"]
BOOKS = LIVE_BOOKS + RESEARCH_BOOKS
PAIR = ["tsmom12", "own_vol_70"]
# research book -> (store family, variant) of its stored series (card: rebuild must match)
STORED = {
    "tsmom12": ("baselines", "tsmom12"),
    "halving-alone": ("halving", "halving-alone"),
    "where-vol": ("trend-where", "where-vol"),
    "stop-0.25": ("cointop-1-stop", "stop-0.25"),
}

History = Mapping[str, Sequence[Bar]]


# --- Hedge (pure) ---


def thetas(first: date = THETA0, last: date = THETA_LAST) -> list[date]:
    """theta_0..theta_T: the Thursdays that end the rounds."""
    out = [first]
    while out[-1] + timedelta(days=7) <= last:
        out.append(out[-1] + timedelta(days=7))
    return out


def eta(k: int, t: int) -> float:
    """Cesa-Bianchi and Lugosi (2006), Theorem 2.2: the rate for a known horizon."""
    return math.sqrt(8 * math.log(k) / t)


def losses(x: np.ndarray) -> np.ndarray:
    """Rounds x books gross returns -> losses in [0, 1]: 1 - x / the round's best x."""
    return 1 - x / x.max(axis=1, keepdims=True)


def hedge_weights(x: np.ndarray, rate: float) -> np.ndarray:
    """W[t] = the weights after t rounds (W[0] uniform), from rounds 1..t only."""
    n, k = x.shape
    cum = np.vstack([np.zeros(k), np.cumsum(losses(x), axis=0)])
    z = -rate * cum
    z -= z.max(axis=1, keepdims=True)
    w = np.exp(z)
    out: np.ndarray = w / w.sum(axis=1, keepdims=True)
    return out


def round_returns(days: Sequence[date], equity: np.ndarray, ths: Sequence[date]) -> np.ndarray:
    """Gross return of each round (theta_{t-1}, theta_t] from end-of-day equity on `days`."""
    pos = {d: i for i, d in enumerate(days)}
    e = np.array([equity[pos[t]] for t in ths])
    out: np.ndarray = e[1:] / e[:-1]
    return out


def weights_on(d: date, ths: Sequence[date], w: np.ndarray) -> np.ndarray:
    """Hedge weights in force for the decision of day d: after the rounds that ended by the end
    of day d - 1 (theta_s <= d - 1, s >= 1)."""
    done = bisect.bisect_right(ths, d - timedelta(days=1), lo=1) - 1
    return w[min(max(done, 0), len(w) - 1)]


def combine(
    books: Sequence[Sequence[Decision]], ths: Sequence[date], w: np.ndarray
) -> list[Decision]:
    """Daily combined target weights: sum_i w_i(day) * book i's weights that day."""
    out = []
    for k, decs in enumerate(zip(*books, strict=True)):
        t = decs[0].time
        if any(d.time != t for d in decs):
            raise ValueError(f"decision {k}: books decide at different times")
        wd = weights_on(t.date(), ths, w)
        tgt: dict[str, float] = {}
        for share, d in zip(wd, decs, strict=True):
            for s, x in d.weights.items():
                tgt[s] = tgt.get(s, 0.0) + share * x
        out.append(Decision(t, harness.clean(tgt)))
    return out


def regret_game(x: np.ndarray, w: np.ndarray) -> dict[str, float]:
    """Regret on the experts' outcomes: in the theorem's loss units and in log wealth."""
    lo = losses(x)
    used = w[:-1]  # round t is played with W[t-1]
    hedge_loss = float((used * lo).sum())
    book_loss = lo.sum(axis=0)
    logw_books = np.log(x).sum(axis=0)
    logw_hedge = float(np.log((used * x).sum(axis=1)).sum())
    n, k = x.shape
    years = n * 7 / 365.25
    best = int(np.argmax(logw_books))
    return {
        "loss_regret": hedge_loss - float(book_loss.min()),
        "bound": math.sqrt(n * math.log(k) / 2),
        "best_loss_book": float(np.argmin(book_loss)),
        "loss_spread": float(book_loss.max() - book_loss.min()),
        "logw_regret": float(logw_books[best]) - logw_hedge,
        "logw_regret_yr": (float(logw_books[best]) - logw_hedge) / years,
        "best_logw_book": float(best),
    }


# --- books ---


def research_strategy(name: str):  # type: ignore[no-untyped-def]
    import common as c

    if name == "tsmom12":
        return c.weekly(c.slots(c.tsmom_signal))
    if name == "halving-alone":
        import macro
        import rules

        def hostile(d: date) -> bool:  # macro.Features.halving_bear, without the FRED loads
            return 548 <= macro.days_since_halving(d) < 913

        return c.weekly(rules.macro_gate(hostile, trend=False, coins_only=True))
    if name == "where-vol":
        import trend_where as tw

        return tw.Where("vol").strategy()
    if name == "stop-0.25":
        import cointop1_carry as ct

        return ct.rule(ct.stop_ok)
    raise KeyError(name)


def cut(hist: History, last: date) -> dict[str, list[Bar]]:
    return {s: [b for b in bars if b.date <= last] for s, bars in hist.items()}


def book_decisions(name: str, last: date, start: date) -> list[Decision]:
    """One decision a day at 22:30 UTC, bars closed by then (gym.backtest's rule)."""
    hist = cut(harness.load_history("train"), last)
    if name in RESEARCH_BOOKS:
        return harness.decisions(research_strategy(name), harness.Panel(hist), start, last)
    import lagcost1

    from grimstrade.strategies import LIVE

    return lagcost1.scheduled(LIVE[name], hist, start, last, gym.DECIDE_AT, 0)


def to_run(variant: str, decs: list[Decision], hist: History, costs: Mapping[str, gym.Costs]):  # type: ignore[no-untyped-def]
    res = gym.simulate(decs, hist, costs=costs)
    sc = report.score(f"{IDEA}/{variant}", res)
    days, equity = harness._calendar(res.equity)
    expo = float(np.mean([sum(d.weights.values()) for d in decs]))
    return harness.Run(IDEA, variant, "train", sc, days, equity, expo, decs)


# --- statistics ---


def paired(a: np.ndarray, b: np.ndarray) -> dict[str, float]:
    if len(a) != len(b):
        raise ValueError("series must cover the same days")
    rng = np.random.default_rng(SEED)
    ds = np.empty(DRAWS)
    for k in range(DRAWS):
        i = stats._stationary_indices(len(a), BLOCK, rng)
        ds[k] = stats.sharpe(a[i]) - stats.sharpe(b[i])
    d = stats.sharpe(a) - stats.sharpe(b)
    se = float(ds.std(ddof=1))
    return {"d": d, "se": se, "z": d / se if se > 0 else math.nan,
            "lo": float(np.quantile(ds, 0.025)), "hi": float(np.quantile(ds, 0.975))}  # fmt: skip


def describe(run) -> dict[str, float]:  # type: ignore[no-untyped-def]
    r = run.rets
    return {
        "sharpe": stats.sharpe(r),
        "cagr": stats.cagr(r),
        "mdd": stats.max_drawdown(r),
        "since03": stats.sharpe(run.rets_between(SINCE, run.days[-1])),
        "late": stats.sharpe(run.rets_between(LATE, run.days[-1])),
        "turnover": run.score.turnover,
        "logw": float(np.log(run.equity[-1] / run.equity[0])),
    }


# --- commands ---


def check() -> None:
    """Each research book rebuilt on its stored window (to 2025-11-09) at protocol costs must
    match its stored Sharpe to 0.005 (card)."""
    stored = {(r.idea, r.variant): r.sharpe for r in returnstore.read(harness.STORE)
              if r.start == START.isoformat()}  # fmt: skip
    hist = harness.load_history("train")
    for name in RESEARCH_BOOKS:
        decs = harness.decisions(
            research_strategy(name), harness.Panel(hist), START, harness.TRAIN_END
        )
        run = to_run(name, decs, hist, PROTO)
        got = stats.sharpe(run.rets)
        want = stored[STORED[name]]
        ok = abs(got - want) <= 0.005
        print(f"{name}: rebuilt {got:.4f}, stored {want:.4f} -> {'OK' if ok else 'MISMATCH'}")
        if not ok:
            raise SystemExit(f"{name}: rebuild does not match the store")


def main() -> None:
    start = LAST - timedelta(days=200) if DRY else START
    th0 = THETA0 if not DRY else start + timedelta(days=(3 - start.weekday()) % 7)
    ths = thetas(th0, THETA_LAST)
    T = len(ths) - 1
    hist = cut(harness.load_history("train"), LAST)
    with ProcessPoolExecutor(max_workers=3) as ex:
        decs = dict(
            zip(BOOKS, ex.map(book_decisions, BOOKS, [LAST] * len(BOOKS), [start] * len(BOOKS)),
                strict=True)
        )  # fmt: skip
    out: dict[str, dict[str, object]] = {}
    for tag, costs in (("", PROTO), ("/gymcost", gym.COSTS)):
        runs = {b: to_run(f"book/{b}{tag}", decs[b], hist, costs) for b in BOOKS}
        days = runs[BOOKS[0]].days
        if any(r.days != days for r in runs.values()):
            raise ValueError("books cover different days")
        x = np.column_stack([round_returns(days, runs[b].equity, ths) for b in BOOKS])
        xp = x[:, [BOOKS.index(b) for b in PAIR]]
        w16 = hedge_weights(x, eta(len(BOOKS), T))
        wp = hedge_weights(xp, eta(len(PAIR), T))
        u16 = np.full_like(w16, 1 / len(BOOKS))
        up = np.full_like(wp, 1 / len(PAIR))
        pair_decs = [decs[b] for b in PAIR]
        combos = {
            "hedge16": to_run(f"hedge16{tag}", combine([decs[b] for b in BOOKS], ths, w16),
                              hist, costs),
            "ew16": to_run(f"ew16{tag}", combine([decs[b] for b in BOOKS], ths, u16), hist, costs),
            "hedge-pair": to_run(f"hedge-pair{tag}", combine(pair_decs, ths, wp), hist, costs),
            "ew-pair": to_run(f"ew-pair{tag}", combine(pair_decs, ths, up), hist, costs),
        }  # fmt: skip
        out[tag or "proto"] = {"runs": runs, "combos": combos, "x": x, "xp": xp,
                               "w16": w16, "wp": wp}  # fmt: skip
    text = report_text(out, ths)
    path = harness.RESEARCH / "results" / (f"{IDEA}.dry.md" if DRY else f"{IDEA}.md")
    path.write_text(text)
    print(text)
    if DRY:
        return
    for key, o in out.items():
        tag = "" if key == "proto" else "/gymcost"
        runs: dict = o["runs"]  # type: ignore[no-redef]
        combos: dict = o["combos"]  # type: ignore[no-redef]
        for b in BOOKS:
            if tag and b != "tsmom12":
                continue  # gym-cost book replays are inputs only; tsmom12 is the comparator
            kind = "baseline" if (b == "tsmom12" and not tag) else "robustness"
            harness._log(runs[b], kind, start, LAST)
        for name, run in combos.items():
            if tag:
                if name == "ew-pair":
                    continue
                harness._log(run, "robustness", start, LAST)
            else:
                kind = "variant" if name.startswith("hedge") else "baseline"
                harness._log(run, kind, start, LAST)


def _f(x: float, spec: str = ".2f") -> str:
    return format(x, spec)


def report_text(out: dict[str, dict[str, object]], ths: Sequence[date]) -> str:
    lines = [
        "# hedge-books-1: Hedge across the existing books",
        "",
        "Card: `research/cards/hedge-books-1.md`. From `research/lib/hedgebooks1.py`. Daily "
        f"returns {START}..{LAST}, 365-day Sharpe, cash at 0, dividend-adjusted prices. "
        f"Rounds: {len(ths) - 1} weeks ending Thursdays {ths[0]}..{ths[-1]}. Paired stationary "
        f"bootstrap (block {BLOCK:.0f} days, {DRAWS} draws, seed {SEED}).",
        "",
    ]
    for key, o in out.items():
        runs: dict = o["runs"]  # type: ignore[assignment]
        combos: dict = o["combos"]  # type: ignore[assignment]
        x: np.ndarray = o["x"]  # type: ignore[assignment]
        xp: np.ndarray = o["xp"]  # type: ignore[assignment]
        w16: np.ndarray = o["w16"]  # type: ignore[assignment]
        wp: np.ndarray = o["wp"]  # type: ignore[assignment]
        label = "protocol costs (judged)" if key == "proto" else "gym live costs (robustness)"
        twin = runs["tsmom12"]
        tw_w = x[:, BOOKS.index("tsmom12")] - 1
        lines += [f"## {label}", ""]
        lines += [
            "| Book | Sharpe | vs `tsmom12` d (SE) z | vs EW d (SE) z | corr wk `tsmom12` "
            "| CAGR | Worst loss | Since 2003 | 2022-25 | Turnover/yr |",
            "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
        ]
        ew_of = {"hedge16": "ew16", "hedge-pair": "ew-pair"}
        verdicts = {}
        for name, run in [*combos.items(), ("tsmom12", twin)]:
            m = describe(run)
            p = paired(run.rets, twin.rets) if run is not twin else None
            vs = ""
            if name in ew_of:
                q = paired(run.rets, combos[ew_of[name]].rets)
                vs = f"{q['d']:+.3f} ({q['se']:.3f}) {q['z']:+.2f}"
                assert p is not None
                verdicts[name] = (p, q, m["sharpe"] > describe(combos[ew_of[name]])["sharpe"])
            wk = round_returns(run.days, run.equity, ths) - 1
            corr = float(np.corrcoef(wk, tw_w)[0, 1])
            pv = f"{p['d']:+.3f} ({p['se']:.3f}) {p['z']:+.2f}" if p else "-"
            lines.append(
                f"| `{name}` | {m['sharpe']:.3f} | {pv} | {vs or '-'} | {corr:.2f} | "
                f"{m['cagr']:+.1%} | {m['mdd']:.1%} | {m['since03']:.2f} | {m['late']:.2f} | "
                f"{m['turnover']:.2f} |"
            )
        lines += ["", "Verdict by the card (pass: z vs `tsmom12` >= 4.70 and Sharpe above its "
                  "EW twin):", ""]  # fmt: skip
        for name, (p, q, above) in verdicts.items():
            ok = p["z"] >= Z_BAR and above
            lines.append(
                f"- `{name}`: z vs `tsmom12` {p['z']:+.2f} (bar {Z_BAR}), "
                f"{'above' if above else 'not above'} its EW twin (z {q['z']:+.2f}): "
                f"**{'PASS' if ok else 'KILL'}**"
            )
        lines += ["", "Stand-alone books (the experts):", "",
                  "| Book | Sharpe | CAGR | Worst loss | log wealth | Hedge16 mean w | final w |",
                  "|---|---:|---:|---:|---:|---:|---:|"]  # fmt: skip
        for i, b in enumerate(BOOKS):
            m = describe(runs[b])
            lines.append(
                f"| `{b}` | {m['sharpe']:.3f} | {m['cagr']:+.1%} | {m['mdd']:.1%} | "
                f"{m['logw']:.2f} | {w16[:-1, i].mean():.3f} | {w16[-1, i]:.3f} |"
            )
        eff = 1 / (w16**2).sum(axis=1)
        lines += [
            "",
            f"Hedge16: eta {eta(len(BOOKS), len(ths) - 1):.4f}; largest weight ever "
            f"{w16.max():.3f} (`{BOOKS[int(np.unravel_index(w16.argmax(), w16.shape)[1])]}`); "
            f"effective number of books mean {eff.mean():.1f}, final {eff[-1]:.1f} (of 16). "
            f"Hedge-pair: eta {eta(2, len(ths) - 1):.4f}; final weights `tsmom12` "
            f"{wp[-1, 0]:.3f}, `own_vol_70` {wp[-1, 1]:.3f}; range of `tsmom12`'s weight "
            f"{wp[:, 0].min():.3f}..{wp[:, 0].max():.3f}.",
            "",
            "Regret (card section 'Regret actually achieved'):",
            "",
            "| Allocator | Loss regret | Bound sqrt(T ln K / 2) | Loss spread of the books | "
            "Best book (loss) | Log-wealth regret, game | per year | Best book (log wealth) "
            "| Log-wealth regret, gym vs best book by wealth | vs best by Sharpe |",
            "|---|---:|---:|---:|---|---:|---:|---|---:|---:|",
        ]
        for name, xx, ww, names in (("hedge16", x, w16, BOOKS), ("hedge-pair", xp, wp, PAIR)):
            g = regret_game(xx, ww)
            pool = {b: describe(runs[b]) for b in names}
            best_w = max(pool, key=lambda b: pool[b]["logw"])
            best_s = max(pool, key=lambda b: pool[b]["sharpe"])
            lw = describe(combos[name])["logw"]
            lines.append(
                f"| `{name}` | {g['loss_regret']:.2f} | {g['bound']:.2f} | {g['loss_spread']:.2f}"
                f" | `{names[int(g['best_loss_book'])]}` | {g['logw_regret']:.2f} | "
                f"{g['logw_regret_yr']:.3f} | `{names[int(g['best_logw_book'])]}` | "
                f"{pool[best_w]['logw'] - lw:.2f} (`{best_w}`) | "
                f"{pool[best_s]['logw'] - lw:.2f} (`{best_s}`) |"
            )
        lines.append("")
    return "\n".join(lines) + "\n"


def entry(cmd: str) -> None:
    commands: dict[str, Callable[[], None]] = {"check": check, "run": main}
    commands[cmd]()


if __name__ == "__main__":
    entry(sys.argv[1] if len(sys.argv) > 1 else "run")
