"""Lane coin-drift-1: does letting held coin slots drift pay on cointop-1's coin book?
Card `research/cards/coin-drift-run.md`; write-up `research/coin-drift-1.md`.

    uv run python -I research/lib/coindrift1.py --synthetic   # plumbing on random prices only
    uv run python -I research/lib/coindrift1.py --log         # the one real run

The coin book is cointop-1's selection set (no BTC, ETH, LTC, XRP, BCH, ETC, XLM, DASH), its
universe, slots and Friday decisions unchanged; the account is traded daily as the gym trades,
with the band carried as a share of the slot (k = 0.06, 0.12, 0.30 = the gym's 0.01, 0.02,
0.05 on wide-16's 1/6 coin slot). Placebos: 40 shuffles each of P1 and P2. Train only.
Writes `research/results/coin-drift-run.md`; with `--log` appends rows to `tries.md`.
"""

from __future__ import annotations

import fcntl
import sys
import time
from datetime import UTC, date, datetime, timedelta
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import breadth_books as bb  # noqa: E402
import coindrift1_core as core  # noqa: E402
import cointop1  # noqa: E402
import harness  # noqa: E402
import stats  # noqa: E402

from grimstrade import gym  # noqa: E402

IDEA = "coin-drift-run"
KS = {"k06": 0.06, "band02": 0.12, "band05": 0.30}  # frozen in the card
N_SHUFFLES = 40
MIN_COINS = 10


class Book:
    """cointop-1's coin book, selection set, on the decision grid."""

    def __init__(self, book: bb.Book):
        self.book = book
        px = book.px
        n_days = px.shape[0]
        sel = np.array([nm not in cointop1.TEST_COINS for nm in book.names])
        dec, skip = bb.decisions(book, "weekly", bb.start_day(book))
        self.d = dec[dec + skip < n_days]
        self.b = self.d + skip
        self.univ = book.elig[self.d] & sel[None, :] & np.isfinite(px[self.b])
        # the account only ever holds coins that are in the universe at some decision
        self.cols = self.univ.any(0)
        self.sel = sel

    def day(self, row: int) -> date:
        return self.book.day0 + timedelta(days=int(row))

    def targets(self, up_rows: np.ndarray) -> np.ndarray:
        hold = self.univ & up_rows[self.d]
        n = self.univ.sum(1)
        with np.errstate(invalid="ignore", divide="ignore"):
            w = np.where(n[:, None] >= MIN_COINS, hold / np.maximum(n, 1)[:, None], 0.0)
        return w[:, self.cols]

    def run(self, px: np.ndarray, up_rows: np.ndarray, k: float, **kw: object) -> core.Account:
        return core.simulate(px[:, self.cols], self.targets(up_rows), self.b, k, **kw)  # type: ignore[arg-type]


def bill_rate(book: bb.Book, synthetic: bool) -> np.ndarray:
    n = book.px.shape[0]
    if synthetic:
        return np.full(n, 0.02)
    rates = harness.bill_rates()
    assert rates, (
        "no bill rates (research/data/bars/IRX.csv missing): the above-bills test needs them"
    )
    known = [t for t, _ in rates]
    return np.array([gym.cash_rate(rates, book.day0 + timedelta(days=i), known) for i in range(n)])


def years_of(cb: Book, acc: core.Account) -> np.ndarray:
    return np.array([cb.day(acc.first + 1 + i).year for i in range(len(acc.rets))])


def log_row(variant: str, kind: str, first: date, last: date, r: np.ndarray, turn: float) -> None:
    eq = np.cumprod(1 + r)
    row = (
        f"| {datetime.now(UTC):%Y-%m-%d %H:%M} | {IDEA} | {variant} | {kind} | train | {first} | "
        f"{last} | {stats.sharpe(r):.2f} | {eq[-1] - 1:+.1%} | {stats.max_drawdown(r):.1%} | "
        f"{turn:.2f} |\n"
    )
    with harness.TRIES.open("a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        f.write(row)


def null_line(d: np.ndarray, real: float) -> str:
    q = np.quantile(d, [0.05, 0.5, 0.95])
    rank = 1 + int((d >= real).sum())
    return (
        f"mean {d.mean():+.4f}, SD {d.std():.4f}, 5/50/95% {q[0]:+.4f} / {q[1]:+.4f} / "
        f"{q[2]:+.4f}, min {d.min():+.4f}, max {d.max():+.4f}; real {real:+.4f} ranks "
        f"{rank} of {len(d) + 1} (p {rank / (len(d) + 1):.3f})"
    )


def main() -> None:
    synthetic = "--synthetic" in sys.argv
    log = "--log" in sys.argv and not synthetic
    t0 = time.time()
    book = cointop1.synthetic_book() if synthetic else bb.cm_book()
    last_day = book.day0 + timedelta(days=book.px.shape[0] - 1)
    assert last_day <= harness.TRAIN_LAST_BAR, f"panel reaches {last_day}: past the train cut"
    cb = Book(book)
    up = core.trend_up(book.px, book.shift)
    if not synthetic:  # the book's own condition, rebuilt by the code the placebos use
        a, b = up[cb.d][:, cb.sel], book.up[cb.d][:, cb.sel]
        assert (a == b).all(), "trend condition differs from the book's"
    rate = bill_rate(book, synthetic)
    first, last = cb.day(int(cb.b[0]) + 1), last_day
    n_univ = cb.univ.sum(1)

    real: dict[str, core.Account] = {}
    bills: dict[str, core.Account] = {}
    gross: dict[str, core.Account] = {}
    for name, k in KS.items():
        real[name] = cb.run(book.px, up, k)
        bills[name] = cb.run(book.px, up, k, rate=rate)
        gross[name] = cb.run(book.px, up, k, costs=False)
    print(f"real books done {time.time() - t0:.0f}s", file=sys.stderr)

    shuffles = 4 if synthetic else N_SHUFFLES
    plac: dict[str, dict[str, np.ndarray]] = {"P1": {}, "P2": {}}
    plac_acc: dict[str, dict[str, list[core.Account]]] = {"P1": {}, "P2": {}}
    for kind, fn in (("P1", core.shuffle_p1), ("P2", core.shuffle_p2)):
        accs: dict[str, list[core.Account]] = {n: [] for n in KS}
        for s in range(1, shuffles + 1):
            ppx = fn(book.px, book.elig, cb.sel, s)
            pup = core.trend_up(ppx, book.shift)
            for name, k in KS.items():
                accs[name].append(cb.run(ppx, pup, k))
        plac_acc[kind] = accs
        plac[kind] = {n: np.stack([a.rets for a in v]) for n, v in accs.items()}
        print(f"{kind} done {time.time() - t0:.0f}s", file=sys.stderr)

    years = (len(real["k06"].rets)) / 365
    draws = 200 if synthetic else 2000
    out = [
        f"# {IDEA}: results (card `cards/coin-drift-run.md`)",
        "",
        "Generated by `research/lib/coindrift1.py`"
        + (" **on synthetic prices (plumbing only)**" if synthetic else "")
        + ". cointop-1's coin book, selection set (no "
        + ", ".join(c.upper() for c in cointop1.TEST_COINS)
        + f"); "
        f"returns {first} .. {last} ({years:.1f} years); {int(cb.cols.sum())} coins ever in the "
        f"universe; universe size per decision median {int(np.median(n_univ))} "
        f"(min {int(n_univ.min())}, max {int(n_univ.max())}). Gym costs (Kraken taker tiers on the "
        "book's 30-day coin volume, 0.05% slip), start 10,000 USD. Band k = share of the slot.",
        "",
        "## The real books",
        "",
        "| Book | k | Sharpe (cash 0) | Sharpe above bills | Sharpe, costs 0 | Growth/yr | Max DD "
        "| Coin share while held | Fills/yr (drift) | Fee/yr | Slip/yr | Fee per traded $ "
        "| Volume x equity/yr |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for name, k in KS.items():
        r, bl, g = real[name], bills[name], gross[name]
        out.append(
            f"| `{name}` | {k:.2f} | {stats.sharpe(r.rets):.3f} | "
            f"{stats.sharpe(bl.rets - bl.rf):.3f} | {stats.sharpe(g.rets):.3f} | "
            f"{stats.cagr(r.rets):.1%} | {stats.max_drawdown(r.rets):.1%} | {r.coin_share:.3f} | "
            f"{r.all_fills / years:.0f} ({r.fills / years:.0f}) | {r.fee / years:.2%} | "
            f"{r.slip / years:.2%} | {r.fee / max(r.volume, 1e-12):.3%} | {r.volume / years:.1f} |"
        )

    out += [
        "",
        "## The pair tests (each band against `k06`, the gym's default carried)",
        "",
        "Paired stationary bootstrap, 2,000 draws, mean block 20 days, seed 0. Excess = d(real) "
        "minus the mean d of the 40 placebo shuffles, all series resampled on the same dates.",
        "",
        "| Band | Reading | dSharpe | SE | z | p (one-sided) | Tracking error/yr | Corr |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    verdict: dict[str, dict[str, float]] = {}
    for name in ("band05", "band02"):
        a, b = real[name].rets, real["k06"].rets
        m = core.joint_boot(a, b, draws=draws)
        mb = core.joint_boot(
            bills[name].rets - bills[name].rf, bills["k06"].rets - bills["k06"].rf, draws=draws
        )
        mg = core.joint_boot(gross[name].rets, gross["k06"].rets, draws=draws)
        p1 = core.joint_boot(a, b, plac["P1"][name], plac["P1"]["k06"], draws=draws)
        p2 = core.joint_boot(a, b, plac["P2"][name], plac["P2"]["k06"], draws=draws)
        te = float((a - b).std() * np.sqrt(365))
        corr = float(np.corrcoef(a, b)[0, 1])
        verdict[name] = {"z": m["z"], "zb": mb["z"], "z1": p1["ex_z"], "z2": p2["ex_z"]}
        rows = [
            ("net, cash 0 (M1)", m["d"], m["se"], m["z"], m["p"]),
            ("net, above bills (M1)", mb["d"], mb["se"], mb["z"], mb["p"]),
            ("costs 0 (the drift part)", mg["d"], mg["se"], mg["z"], mg["p"]),
            ("excess over P1 (M2)", p1["excess"], p1["ex_se"], p1["ex_z"], float("nan")),
            ("excess over P2 (M2b)", p2["excess"], p2["ex_se"], p2["ex_z"], float("nan")),
        ]
        for label, d, se, z, p in rows:
            extra = f" | {te:.2%} | {corr:.4f} |" if label.startswith("net, cash") else " | | |"
            ps = "-" if np.isnan(p) else f"{p:.3f}"
            out.append(f"| `{name}` | {label} | {d:+.4f} | {se:.4f} | **{z:+.2f}** | {ps}{extra}")

    out += ["", "## The placebo nulls (dSharpe of each band against `k06`, cash 0)", ""]
    for kind in ("P1", "P2"):
        for name in ("band05", "band02"):
            dp = core.sharpes(plac[kind][name]) - core.sharpes(plac[kind]["k06"])
            dreal = stats.sharpe(real[name].rets) - stats.sharpe(real["k06"].rets)
            sh = core.sharpes(plac[kind][name])
            fees = np.array([a.fee / years for a in plac_acc[kind][name]])
            fees0 = np.array([a.fee / years for a in plac_acc[kind]["k06"]])
            out.append(
                f"- {kind}, `{name}`: {null_line(dp, dreal)}. Placebo book Sharpe mean "
                f"{sh.mean():.3f} (`k06` {core.sharpes(plac[kind]['k06']).mean():.3f}); fee/yr "
                f"mean {fees.mean():.2%} (`k06` {fees0.mean():.2%})."
            )

    out += ["", "## dSharpe per calendar year (cash 0, net; `band05` / `band02` minus `k06`)", ""]
    out += ["| Year | Days | `k06` Sharpe | `band05` | `band02` | `band05`, costs 0 |"]
    out += ["|---|---:|---:|---:|---:|---:|"]
    yrs = years_of(cb, real["k06"])
    for y in sorted(set(yrs)):
        m = yrs == y
        if m.sum() < 60:
            continue
        s0 = stats.sharpe(real["k06"].rets[m])
        s5 = stats.sharpe(real["band05"].rets[m])
        out.append(
            f"| {y} | {int(m.sum())} | {s0:.2f} | {s5 - s0:+.3f} | "
            f"{stats.sharpe(real['band02'].rets[m]) - s0:+.3f} | "
            f"{stats.sharpe(gross['band05'].rets[m]) - stats.sharpe(gross['k06'].rets[m]):+.3f} |"
        )

    out += ["", "## Pass bar (card)", ""]
    for name, v in verdict.items():
        m1 = v["z"] >= 2 and v["zb"] >= 2
        m2, m2b = v["z1"] >= 2, v["z2"] >= 2
        if m1 and m2:
            reading = "mechanism confirmed (own-coin drift)"
        elif m1 and m2b:
            reading = "coin-market drift only: not independent confirmation"
        elif m1:
            reading = "fewer trades or chance: not confirmed"
        else:
            reading = "not confirmed (M1 fails)"
        out.append(
            f"- `{name}`: M1 z {v['z']:+.2f} (cash 0), {v['zb']:+.2f} (above bills) "
            f"{'hold' if m1 else 'fail'}; M2 excess over P1 z {v['z1']:+.2f} "
            f"({'holds' if m2 else 'fails'}); M2b excess over P2 z {v['z2']:+.2f} "
            f"({'holds' if m2b else 'fails'}). **{reading}**"
        )
    text = "\n".join(out) + "\n"
    print(text)
    print(f"total {time.time() - t0:.0f}s", file=sys.stderr)
    if synthetic:
        return
    (harness.RESEARCH / "results" / f"{IDEA}.md").write_text(text)
    if log:
        turn = {n: real[n].volume / years for n in KS}
        log_row("k06@cm (cointop-1 coin book, band 0.06 of the slot)", "baseline", first, last,
                real["k06"].rets, turn["k06"])  # fmt: skip
        for name in ("band05", "band02"):
            log_row(f"{name}@cm (band {KS[name]:.2f} of the slot)", "robustness", first, last,
                    real[name].rets, turn[name])  # fmt: skip
        for kind in ("P1", "P2"):
            for name in KS:
                rs = plac[kind][name]
                i = int(np.argsort(core.sharpes(rs))[len(rs) // 2])  # the median shuffle
                acc = plac_acc[kind][name][i]
                log_row(f"{name}@cm placebo {kind} (median of {len(rs)} shuffles; mean Sharpe "
                        f"{core.sharpes(rs).mean():.2f})", "control", first, last, acc.rets,
                        acc.volume / years)  # fmt: skip


if __name__ == "__main__":
    main()
